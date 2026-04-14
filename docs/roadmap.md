# OpsFlow AI Roadmap

## v0.1 — MVP (当前)

- [x] 项目骨架搭建
- [x] FastAPI 后端 + PostgreSQL + Redis
- [x] LangGraph 5 节点工作流 (Planner/Retriever/Executor/Reviewer/Approver)
- [x] RAG 知识检索 + citation
- [x] SQL / HTTP / Browser / File 工具
- [x] 人工审批节点
- [x] SSE 实时推送
- [x] 执行日志 trace
- [x] Next.js 前端工作台
- [x] Docker Compose 一键部署
- [x] 电商运营 demo 场景

## v0.2 — 增强

- [ ] 混合检索 (向量 + 关键词)
- [ ] Rerank 模型集成
- [ ] 任务执行回放 (Replay)
- [ ] 基础评测看板 (Eval Dashboard)
- [ ] 失败重试机制
- [ ] 工具调用超时处理
- [ ] 文档解析增强 (PDF, DOCX)

## v0.3 — 扩展

- [ ] 多模型支持 (Claude, Gemini, 本地模型)
- [ ] 工作流可视化编辑器
- [ ] 自定义工具注册
- [ ] Webhook 通知
- [ ] 批量任务执行

## v1.0 — 生产就绪

- [ ] 多租户 + 权限管理
- [ ] 插件市场
- [ ] API Key 管理
- [ ] 审计日志
- [ ] 性能优化与缓存
- [ ] 生产部署文档 (K8s)
