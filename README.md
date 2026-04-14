<div align="center">

# ⚡ OpsFlow AI

**基于 LangChain / LangGraph 的开源 AI 任务执行工作台**

*Open-source AI Task Execution Workspace built with LangChain, LangGraph, RAG and Browser Tools*

让 AI 从"会回答"变成"会执行"

[English](#english) · [快速开始](#quick-start) · [架构](#architecture) · [演示场景](#demo)

</div>

---

## 这是什么？

OpsFlow AI 是一个面向企业运营场景的 AI Agent 执行工作台。

用户输入一句业务任务，系统自动完成：

**任务拆解 → 检索知识库 → 调用工具/API/浏览器 → 人工审批 → 输出结果 → 保留证据链和执行日志**

它不是一个聊天机器人，而是一个能把事做完的工作台。

## 核心能力

- 🧠 **任务驱动的 Agent** — 自然语言输入，自动拆解为可执行步骤
- 📚 **RAG 知识检索** — 文档上传、切片、向量检索、citation 引用
- 🔧 **工具调用** — SQL 查询、HTTP API、浏览器自动化、文件生成
- 👤 **人机协作** — 高风险操作自动暂停，等待人工审批后继续
- 📊 **全链路可观测** — 每步日志、工具输入输出、token 消耗、执行回放
- 🔄 **LangGraph 状态机** — Planner → Retriever → Executor → Reviewer → Approver

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Next.js, React, TypeScript, Tailwind CSS |
| 后端 | FastAPI, SQLAlchemy, PostgreSQL, Redis |
| AI/Agent | LangChain, LangGraph, OpenAI |
| 检索 | pgvector, 混合检索 |
| 浏览器 | Playwright |
| 部署 | Docker Compose |

## 适用场景

- 电商运营 — 退款分析、异常商品处理、工单生成
- 企业知识库 — SOP 执行、流程自动化
- 工单自动化 — 自动创建、填写、提交工单
- 后台操作 — 浏览器自动填报、表单提交
- 内部流程 — 入职流程、IT 开通、审批流转

<a id="quick-start"></a>
## 快速开始

### 环境要求

- Docker & Docker Compose
- OpenAI API Key

### 一键启动

```bash
# 克隆项目
git clone https://github.com/your-username/opsflow-ai.git
cd opsflow-ai

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 OPENAI_API_KEY

# 启动所有服务
cd docker
docker compose up -d

# 导入 demo 数据
docker compose exec postgres psql -U opsflow -d opsflow -f /demo/mock_data.sql
```

访问：
- 前端工作台：http://localhost:3000
- API 文档：http://localhost:8000/docs

### 本地开发

```bash
# 后端
cd apps/api
pip install -r requirements.txt
uvicorn app.main:app --reload

# 前端
cd apps/web
npm install
npm run dev
```

<a id="architecture"></a>
## 架构

```
用户输入任务
    │
    ▼
┌─────────┐
│ Planner │ ← 拆解任务为执行计划
└────┬────┘
     ▼
┌──────────┐
│Retriever │ ← 检索知识库 / SOP / FAQ
└────┬─────┘
     ▼
┌──────────┐
│ Executor │ ← 调用 SQL / API / Browser 工具
└────┬─────┘
     ▼
┌──────────┐
│ Reviewer │ ← 检查结果完整性和证据
└────┬─────┘
     ▼
┌──────────┐
│ Approver │ ← 高风险操作等待人工审批
└────┬─────┘
     ▼
  输出结果 + 证据链 + 执行日志
```

```
opsflow-ai/
├── apps/
│   ├── web/              # Next.js 前端
│   └── api/              # FastAPI 后端
├── packages/
│   ├── agent-core/       # LangGraph 工作流
│   ├── rag-core/         # RAG 检索引擎
│   ├── toolkits/         # 工具集
│   └── shared/           # 公共类型
├── workers/
│   ├── browser-runner/   # Playwright 执行器
│   └── ingestion-worker/ # 文档解析索引
├── docker/               # Docker 配置
└── examples/             # 演示数据和文档
```

<a id="demo"></a>
## 演示场景

### 场景 A：商品售后分析

> "帮我分析最近 7 天退款率异常的商品，结合售后 SOP 给出处理建议，并生成工单草稿。"

系统自动执行：SQL 查退款数据 → RAG 查售后 SOP → 分析异常原因 → 生成处理建议 → 创建工单草稿 → 等待审批

### 场景 B：入职流程执行

> "根据入职流程 SOP，帮我生成新员工 IT 系统开通申请表草稿。"

系统自动执行：检索入职 SOP → 提取所需字段 → 生成申请表 → 等待确认

## Roadmap

- [x] LangGraph 多节点工作流
- [x] RAG 知识检索 + citation
- [x] SQL / HTTP / Browser 工具
- [x] 人工审批节点
- [x] 执行日志与 trace
- [ ] 拖拽式工作流编辑器
- [ ] 多模型适配 (Claude, Gemini, 本地模型)
- [ ] 插件市场
- [ ] 多租户支持
- [ ] 评测看板 (Eval Dashboard)

## License

[Apache-2.0](LICENSE)
