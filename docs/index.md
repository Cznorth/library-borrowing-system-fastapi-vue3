# 图书馆借阅系统 — 文档首页

## 项目概览
- 技术栈：后端（FastAPI、SQLAlchemy、PostgreSQL）、前端（Vue3、Pinia、Vue Router、Axios）
- 主要功能：检索、借阅/归还/续借、预约、罚金；管理员维护书目/副本与用户
- 运行方式：Docker Compose 或本地开发（见根目录 `README.md`）

## 快速开始
- 后端：`pip install -r backend/requirements.txt` → `uvicorn app.main:app --reload`
- 前端：`cd frontend && npm i && npm run dev`
- 访问地址：后端 `http://localhost:8000/docs`，前端 `http://localhost:5173`

## 截图预览
- 首页

  ![首页](./screenshots/home.png)

- 登录页

  ![登录页](./screenshots/login.png)

- 管理员首页

  ![管理员首页](./screenshots/admin.png)

- 我的借阅

  ![我的借阅](./screenshots/my_loans.png)

- 我的预约

  ![我的预约](./screenshots/my_reservations.png)

- 我的罚金

  ![我的罚金](./screenshots/my_fines.png)

## 结构与设计
- UML 图集：用例、包、部署、构件、领域类、数据设计、活动与顺序（见左侧导航“UML图集”）
- 实验报告：完整过程与成果说明（见左侧导航“实验报告”）
- 用例详述：登录/注册/搜索/借阅/归还/续借/预约/罚金/管理后台（见左侧导航“用例详述”）

## 演示与汇报
- PPT 源文件与导出：`docs/ppt/slides.md`、`docs/ppt/slides.pptx`
- 截图自动化：前端 `npm run test:e2e`，脚本位于 `frontend/tests/screenshots.spec.ts`

