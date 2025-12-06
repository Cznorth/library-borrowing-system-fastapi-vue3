## 目标与范围
- 交付一个前后端分离的图书馆借阅系统，覆盖课程考核全部要求：需求、UML、架构与详细设计、代码实现、测试、PPT与报告、Git版本管理。
- 技术栈：后端 `FastAPI`、数据库 `PostgreSQL`、前端 `Vue3 + Pinia + Vue Router + Vite`、鉴权 `JWT`、ORM `SQLAlchemy`、迁移 `Alembic`、测试 `pytest + FastAPI TestClient`、前端测试 `Vitest + Playwright`。

## 评分点对齐
- 需求：完整获取与分析、自然语言需求、用例图与用例描述（前置/后置/基本/异常流程）。
- 架构：包图、部署图、构件图、UI原型、类图（界面元素）、顺序图（界面跳转）。
- 详细设计：类属性/方法/关系、活动图（算法细节）、数据设计类图与数据操作活动图、子系统设计顺序图与类图。
- 实现与测试：测试计划、覆盖核心功能的测试用例、缺陷记录与修复说明。
- 汇报：PPT、现场答辩材料、完整实验报告、源码、Git提交记录。

## 核心功能
- 用户注册/登录、角色管理（读者、管理员/馆员）。
- 图书管理：录入/编辑/下架、批量导入（CSV）、分类/标签、副本管理（馆藏副本）。
- 检索与浏览：关键词搜索、按分类/作者筛选、分页、书籍详情。
- 借阅与归还：借阅规则（每人上限N本、借期、续借次数）、续借、超期与罚金计算。
- 预约与队列：已借出书籍的预约队列、到书通知。
- 我的借阅：历史记录、当前借阅、预约列表、罚金缴纳记录（记录型，演示可模拟支付）。
- 后台：用户管理、图书与副本管理、借阅/归还流水、预约管理、统计报表（按月借阅量、热门图书TopN）。

## 角色与权限
- 读者：浏览/搜索/预约/借阅（符合规则）/续借/归还/查看个人记录。
- 管理员/馆员：图书与副本CRUD、用户管理、借阅流水管理、预约出入队、数据统计。
- 权限控制：基于 `JWT` 与角色的后端路由守卫；前端路由基于角色重定向与隐藏菜单。

## 体系结构
- 前端：`Vue3` 组件化 + `Pinia` 状态管理 + `Router` 路由守卫；`API` 封装、`UI` 原型与页面。
- 后端：分层架构（API层 → Service层 → Repository层 → ORM/DB）；统一错误处理中间件、`Pydantic` 模型输入输出。
- 数据库：规范化设计（实体与关系、约束与索引）；使用 `Alembic` 迁移管理。
- 鉴权：`JWT` 认证，密码哈希 `passlib`；刷新令牌可选（先实现短期访问令牌）。

## 技术栈与规范
- 代码规范：后端 `black/flake8`，前端 `ESLint + Prettier`；提交前钩子可选 `lint-staged`。
- 接口文档：`FastAPI` 自带 `OpenAPI/Swagger`；额外在文档中提供端点表。
- 日志与异常：结构化日志（`logging`），统一异常响应（错误码与提示）。

## 数据库设计（核心表）
- `users`：`id`，`username`，`email`，`password_hash`，`role`，`created_at`，唯一约束与索引。
- `books`：`id`，`isbn`，`title`，`author`，`publisher`，`year`，`category`，`tags`，`summary`，`cover_url`。
- `book_copies`：`id`，`book_id`，`barcode`，`shelf_location`，`status`（在馆/借出/下架），唯一 `barcode`。
- `loans`：`id`，`copy_id`，`user_id`，`loan_date`，`due_date`，`return_date`，`renew_count`，状态派生。
- `reservations`：`id`，`book_id`，`user_id`，`status`（排队/通知/过期/取消），`created_at`；队列按 `created_at` 排。
- `fines`：`id`，`loan_id`，`user_id`，`amount`，`status`（未缴/已缴），`created_at`，`paid_at`。
- `audit_logs`（可选）：`id`，`actor_id`，`action`，`entity`，`entity_id`，`created_at`。
- 约束：外键、唯一键（`isbn` 可唯一）、常用索引（`title/author/category`）。

## API设计（示例）
- 鉴权：`POST /auth/register`，`POST /auth/login`，`GET /auth/me`。
- 用户：`GET /users`（admin），`POST /users`，`PATCH /users/{id}`，`DELETE /users/{id}`。
- 图书：`GET /books`，`GET /books/{id}`，`POST /books`（admin），`PATCH /books/{id}`（admin），`DELETE /books/{id}`（admin）。
- 副本：`GET /books/{id}/copies`，`POST /books/{id}/copies`（admin），`PATCH /copies/{id}`（admin）。
- 借阅：`POST /loans`（借出某副本），`POST /loans/{id}/return`，`POST /loans/{id}/renew`，`GET /loans/me`。
- 预约：`POST /reservations`，`GET /reservations/me`，`POST /reservations/{id}/cancel`；由后台触发到书通知。
- 罚金：`GET /fines/me`，`POST /fines/{id}/pay`（模拟支付）。
- 统计：`GET /stats/top-books`，`GET /stats/monthly-loans`（admin）。
- 统一分页与筛选参数：`page`，`page_size`，`q`（关键词）等。

## 前端设计（页面与原型）
- 公共：登录、注册、首页（搜索与推荐）、书籍详情。
- 读者：我的借阅、我的预约、我的罚金、个人资料。
- 管理员：仪表盘、图书管理、副本管理、用户管理、借阅管理、预约管理、统计报表。
- 路由守卫：未登录跳转登录；角色不匹配跳转首页或后台首页。

## UML设计清单
- 需求：用例图（读者、管理员），每个用例的详细描述（前置/后置/基本/异常流程）。
- 架构：包图（前端/后端/数据库/公共模块）、部署图（浏览器—前端—后端—数据库）、构件图（API服务、鉴权组件、数据访问组件）。
- UI设计：原型示意图；界面元素类图（页面组件层次）；页面跳转顺序图（登录→首页→详情→借阅/预约等）。
- 详细设计：领域类图（User/Book/BookCopy/Loan/Reservation/Fine 等类与关系）；
- 活动图：借阅流程、归还与罚金计算、预约队列处理、管理员入库流程。
- 子系统：用户子系统、图书与副本子系统、借阅子系统、预约子系统的顺序图与类图。

## 测试计划
- 单元测试：业务服务（借阅规则、罚金计算、预约队列）。
- 集成测试：API端到端（`TestClient` + 临时数据库）。
- 前端：组件与页面逻辑 `Vitest`；关键流程 `Playwright`（登录、搜索、借阅、归还）。
- 测试数据：`pytest` fixtures/seed，前端 `mock` API 或测试环境接口。
- 覆盖率与缺陷记录：覆盖核心路径；缺陷单、重现步骤、修复提交关联。

## 项目结构（单仓库，多包）
- 根目录：`/backend`（FastAPI）、`/frontend`（Vue3）、`/docs`（需求/UML/报告/PPT）、`/ops`（Docker Compose、环境示例）、`/tests`（端到端脚本可选）。
- 后端：`app/api`、`app/services`、`app/repositories`、`app/models`、`app/schemas`、`app/core`（配置/安全/依赖）、`app/utils`、`migrations`。
- 前端：`src/pages`、`src/components`、`src/stores`、`src/router`、`src/services/api.ts`、`src/assets`、`src/utils`、`tests`。
- 文档：`docs/requirements.md`、`docs/usecases/`、`docs/uml/`（StarUML/Draw.io 源文件与导出）、`docs/report.md`、`docs/ppt/`。

## Git工作流与版本管理
- 初始化仓库（GitHub），开启分支保护与Issues/PR模板。
- 分支策略：`main`（稳定）、`dev`（集成）、功能分支 `feat/*`、修复分支 `fix/*`。
- 提交规范：语义化提交信息（`feat: ...`、`fix: ...`、`docs: ...`），每个阶段配套提交记录。
- PR与代码审查：最小可审查单元、关联Issues与任务清单。

## 文档与交付物
- 实验报告：按照评分点编排（需求→架构→详细设计→实现→测试→总结），含关键图与说明。
- UML与原型：源文件与导出图片，图名与版本号标注。
- PPT：15分钟讲解版（问题→目标→架构→核心流程→演示→测试与结果→总结与展望）。
- 源码：可运行说明、环境变量样例、启动与测试步骤。
- Git提交记录：过程性截图与链接（报告附录）。

## 部署与运行
- 开发：本地 `Docker Compose`（PostgreSQL、pgAdmin、backend、frontend），`.env.example` 提供配置。
- 生产演示：同构 Compose，或学校内网服务器；反向代理 `nginx` 可选。
- CI：`GitHub Actions`（后端 `pytest`、前端 `vitest`、`eslint`、构建检查）。

## 实施步骤（里程碑）
- 阶段1（需求与原型）：需求梳理、用例与用例描述、UI低保真原型。
- 阶段2（架构与数据库）：UML架构图、数据库表与迁移、接口契约。
- 阶段3（后端核心）：鉴权、图书/副本、借阅/归还/续借、预约、罚金与统计。
- 阶段4（前端页面）：公共页、读者页、管理员页、路由与状态管理。
- 阶段5（测试与修复）：单元/集成/端到端、缺陷记录与修复、覆盖率报告。
- 阶段6（交付打包）：文档与UML整理、PPT与报告定稿、运行与演示脚本。

## 风险与质量保障
- 数据一致性：事务与约束、借阅/归还并发锁（按 `book_copies` 状态更新）。
- 安全：密码哈希、JWT过期与刷新策略、角色鉴权、输入校验与速率限制可选。
- 可维护性：分层与单元测试、日志追踪、配置化借阅规则。

确认后，我将：
- 创建GitHub仓库与基本项目骨架（FastAPI + Vue3 + PostgreSQL + Docker Compose），
- 完成数据库迁移与示例数据，逐步实现后端/前端功能与测试，
- 生成UML图与文档、PPT与报告，并提交可运行源码与Git过程记录。