import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.skill import Skill, SkillRun, SkillEval
from app.schemas.skill import SkillRead, SkillRunRead, SkillEvalRead, SkillListResponse, SkillUpdate

router = APIRouter(prefix="/api/skills", tags=["skills"])

SKILLS_ROOT = Path(__file__).resolve().parents[4] / "skills"


@router.get("", response_model=SkillListResponse)
async def list_skills(
    category: str | None = None,
    risk_level: str | None = None,
    is_enabled: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Skill)
    if category:
        query = query.where(Skill.category == category)
    if risk_level:
        query = query.where(Skill.risk_level == risk_level)
    if is_enabled is not None:
        query = query.where(Skill.is_enabled == is_enabled)
    result = await db.execute(query)
    skills = result.scalars().all()
    return SkillListResponse(count=len(skills), skills=skills)


@router.get("/{skill_id}", response_model=SkillRead)
async def get_skill(skill_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("/{skill_id}/toggle", response_model=SkillRead)
async def toggle_skill(skill_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill.is_enabled = not skill.is_enabled
    await db.commit()
    await db.refresh(skill)
    return skill


@router.get("/{skill_id}/runs", response_model=list[SkillRunRead])
async def get_skill_runs(skill_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SkillRun).where(SkillRun.skill_id == skill_id).order_by(SkillRun.started_at.desc())
    )
    return result.scalars().all()


@router.get("/{skill_id}/evals", response_model=list[SkillEvalRead])
async def get_skill_evals(skill_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SkillEval).where(SkillEval.skill_id == skill_id))
    return result.scalars().all()


@router.post("/sync")
async def sync_skills(db: AsyncSession = Depends(get_db)):
    """Sync built-in skills from the filesystem into the database."""
    if not SKILLS_ROOT.is_dir():
        return {"synced": 0, "message": "Skills directory not found"}

    # Lazy import to avoid circular deps at module level
    from packages.skill_engine.manifest import load_manifest

    synced = 0
    for child in sorted(SKILLS_ROOT.iterdir()):
        if not child.is_dir() or not (child / "SKILL.yaml").exists():
            continue
        try:
            manifest = load_manifest(child)
        except Exception:
            continue

        result = await db.execute(select(Skill).where(Skill.name == manifest.name))
        existing = result.scalar_one_or_none()

        data = {
            "display_name": manifest.display_name,
            "description": manifest.description,
            "version": manifest.version,
            "category": manifest.category,
            "risk_level": manifest.risk_level,
            "is_builtin": True,
            "triggers": manifest.triggers,
            "input_schema": manifest.input_schema,
            "tools_allow": manifest.tools_allow,
            "knowledge_scope": manifest.knowledge_scope,
            "approval_required_for": manifest.approval_required_for,
            "output_schema": manifest.output_schema,
            "manifest_json": manifest.to_dict(),
        }

        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
        else:
            skill = Skill(id=str(uuid.uuid4()), name=manifest.name, **data)
            db.add(skill)
        synced += 1

    await db.commit()
    return {"synced": synced}


@router.post("/{skill_id}/test")
async def test_skill(skill_id: str, body: dict, db: AsyncSession = Depends(get_db)):
    """Test run a skill with sample input."""
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    user_input = body.get("input", "")
    run = SkillRun(
        id=str(uuid.uuid4()),
        skill_id=skill.id,
        skill_version=skill.version,
        input_json={"input": user_input},
        status="completed",
        tokens_used=0,
        output_json={"message": f"Test run for skill '{skill.display_name}' completed", "input": user_input},
    )
    db.add(run)
    await db.commit()
    return {"run_id": run.id, "status": "completed", "output": run.output_json}
