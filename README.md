# 图书馆借阅系统（FastAPI + PostgreSQL + Vue3）

## 开发环境启动（Docker Compose）
- 安装 Docker 与 Docker Compose
- 在 `backend/.env.example` 按需修改后复制为 `.env`
- 运行：`docker compose -f ops/docker-compose.yml up --build`
- 后端：`http://localhost:8000/docs`，前端：`http://localhost:5173`

## 本地开发（不使用容器）
- 后端：`pip install -r backend/requirements.txt` → `uvicorn app.main:app --reload`
- 前端：`cd frontend && npm i && npm run dev`

## 文档与UML
- `docs/requirements.md`、`docs/report.md`、`docs/ppt/outline.md`
- UML（PlantUML）：`docs/uml/*.puml`

