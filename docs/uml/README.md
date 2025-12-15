# UML图使用说明

- 所有UML图以PlantUML源码形式存放于本目录（*.puml）。
- 导出方法：
  - 方式1（本地离线，推荐）：安装 Java 并下载 PlantUML jar 到 `docs/tools/plantuml.jar`，运行：
    - `set UML_FORMAT=png && python docs/uml/render_local.py`
    - 如需 JPG：`set UML_FORMAT=jpg && python docs/uml/render_local.py`
  - 方式2（VSCode）：安装 PlantUML 插件，右键导出PNG/SVG。
  - 方式3（在线）：Kroki/PlantUML在线服务（不稳定，仅备选）。
- 文件清单：
  - 用例图：`usecase.puml`
  - 包图：`package.puml`
  - 部署图：`deployment.puml`
  - 构件图：`components.puml`
  - 领域类图：`class_domain.puml`
  - 界面类图：`class_ui.puml`
  - 顺序图（导航/鉴权/注册/借阅/归还/续借/预约/罚金）：`sequence_navigation.puml`、`sequence_register.puml`、`sequence_borrow.puml`、`sequence_return.puml`、`sequence_renew.puml`、`sequence_reservation.puml`、`sequence_pay_fine.puml`
  - 活动图（登录/注册/借阅/归还/预约/续借）：`activity_login.puml`、`activity_register.puml`、`activity_borrow.puml`、`activity_return.puml`、`activity_reservation.puml`、`activity_renew.puml`
  - 数据设计类图：`data_design_class.puml`
  - 数据操作活动图：`data_operation_activity.puml`
  - 状态图（认证）：`state_auth.puml`

导出图片后请放入 `docs/uml/exports/` 目录并在报告中引用。

## 中文显示与编码说明

- 文件编码：为避免中文乱码，请将所有 `*.puml` 文件保存为 `GB2312` 编码（VS Code：右下角编码 → 重新以编码打开 → 另存为）。
- 字体统一：所有图在顶端 `!include _skin.iuml`，统一中文字体为 `Microsoft YaHei`，可按需改为其它中文字体。
- Graphviz 渲染：本地脚本会检测并使用 `dot.exe` 进行渲染，进一步减少中文兼容问题。
- 渲染命令（在 `docs/uml` 目录）：
  - `java -jar ..\tools\plantuml.jar -graphvizdot "C:\Program Files\Graphviz\bin\dot.exe" -tpng -o exports *.puml`

若仍存在中文显示问题，建议：
- 安装备用中文字体（如 `Noto Sans CJK SC` 或 `思源黑体`）并在 `_skin.iuml` 中替换字体名。
- 确认所有 `*.puml` 已保存为 `GB2312`（而非 UTF-8/UTF-16）。

