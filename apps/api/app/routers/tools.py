import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.tool import Tool
from app.schemas.tool import ToolResponse

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=list[ToolResponse])
async def list_tools(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tool).order_by(Tool.created_at.desc()))
    return result.scalars().all()


@router.post("/{tool_id}/test")
async def test_tool(tool_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    tool = await db.get(Tool, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    # Placeholder: execute tool test logic
    return {"status": "ok", "tool_id": str(tool_id), "message": f"Tool '{tool.name}' test passed"}


@router.patch("/{tool_id}", response_model=ToolResponse)
async def toggle_tool(tool_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    tool = await db.get(Tool, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    tool.enabled = not tool.enabled
    await db.commit()
    await db.refresh(tool)
    return tool
