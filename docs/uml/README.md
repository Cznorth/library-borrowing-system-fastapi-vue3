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
  - 顺序图（导航/借阅）：`sequence_navigation.puml`、`sequence_borrow.puml`
  - 活动图（借阅/归还/预约）：`activity_borrow.puml`、`activity_return.puml`、`activity_reservation.puml`
  - 数据设计类图：`data_design_class.puml`
  - 数据操作活动图：`data_operation_activity.puml`

导出图片后请放入 `docs/uml/exports/` 目录并在报告中引用。

