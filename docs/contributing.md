# Contributing to OpsFlow AI

感谢你对 OpsFlow AI 的关注！

## 开发环境搭建

### 前置要求

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ (with pgvector extension)
- Redis 7+

### 本地启动

```bash
# 1. 启动基础设施
cd docker
docker compose up postgres redis -d

# 2. 启动后端
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. 启动前端
cd apps/web
npm install
npm run dev
```

## 项目结构

- `apps/api/` — FastAPI 后端
- `apps/web/` — Next.js 前端
- `packages/agent-core/` — LangGraph 工作流引擎
- `packages/rag-core/` — RAG 检索引擎
- `packages/toolkits/` — 工具集
- `packages/shared/` — 公共类型和常量

## 提交规范

使用 Conventional Commits：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具变更

## 开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feat/your-feature`)
3. 提交代码
4. 创建 Pull Request

## Good First Issues

查看标记为 `good first issue` 的 Issue，适合首次贡献者。
