# TapTap H5 目标平台

**2026-10-03** 已核对[官方 H5 MCP 安装说明](https://developer.taptap.cn/minigameapidoc/quick-start/mcp-guide/mcp-setup/)、[上游 MCP](https://github.com/taptap/instant-games-open-mcp)及当前工具 schema，使用时重查。H5 使用宿主注入的全局 `tap`，普通浏览器未必存在。Maker/UrhoX 与原生 Android/iOS/Unity SDK 是不同产品。

## 本地准备

来源可为普通 H5、TapTap H5 或其他平台 H5，先完成[范围选择](selection.md)。新 TapTap 渠道建立独立工程、接入层与存档作用域；已有 TapTap 渠道做三方增量更新，保留正式 key、schema、奖励回执、应用绑定与旧包。不凭目录名推断应用归属。

静态构建保留 `index.html`、正确相对资源和方向。当前上传工具接收经确认的**构建目录**，不是任意源码或物料 ZIP；另保留附 hash 的游戏候选 ZIP。包体限制需核对当前后台，JSON 中未知上限保持空值。预算与静态预检使用 `--channel taptap`；静态通过不证明 `tap` 注入或账号绑定。

TapTap 物料规格仍需核对当前 H5 建项表单。按选定范围准备真实名称、介绍、操作、图标／封面和实机截图；共享规则没有编造 TapTap 尺寸和数量。校验警告意味着不能宣称全套已齐。交付前核实必填字段、方向、格式、大小和视频要求；视频仍需主动选择。

## 分功能选择，再核对当前应用

| 功能 | 已确认路线与边界 |
| --- | --- |
| 广告 | 先读 `get_ads_integration_workflow`；核对当前应用／用户选择，再 `check_ads_status`，已生效且自动取得有效广告位才调用 `get_ad_integration_guide`。不索要、手抄或沿用旧广告位。真实成功回调与奖励落盘另验。 |
| 身份 | 从当前官方 H5 文档／工具确认真实运行时接口；开发者 OAuth、联机玩家 ID 不能替代账号身份。未知身份隔离本机游玩，冻结账号远端写。 |
| 本地／云档 | 本地持久化属于游戏实现；官方文件／档案路线读 `get_cloud_save_integration_guide`。保留同步策略，验证切号空云、冲突和写入结果未知。 |
| 排行榜 | 先读 `get_leaderboard_integration_guide`，固定指标、范围／编码／排序、资格、榜单命名空间和配置。不为研究能力新建榜单。 |
| 分享／振动 | 先读 `get_share_integration_guide`／`get_vibrate_integration_guide`。分享模板审核与设备效果单独验收；宿主全局接口不需要安装 SDK npm 包。 |
| 诊断／反馈 | 运行时摘要是可选游戏工作。`get_debug_feedbacks` 是开发者工具，默认改变处理状态并下载附件；通用或只读能力研究不调用。用户明确只读查看反馈时按当前 schema 设置 `fetch_and_mark_processed=false`。“已处理”不等于修复。 |
| 多人 | 已发现 `get_multiplayer_guide`，仅选中才读取；属于额外产品范围，不是 H5 适配必装项。服务端权威、身份与恢复另设计。 |
| 成就 | **H5 待核实。**[成就文档](https://developer.taptap.cn/docs/sdk/achievement/features/)列出 iOS/Android/Unity，不证明 H5 JS 路线。当前 MiniGame 工具清单未找到专用成就工具。 |
| 礼包／兑换码 | **H5 待核实。**[礼包文档](https://developer.taptap.cn/docs/sdk/tds-gift/)属于游戏服务；站内活动页、原生或服务端接口不能直接当 H5 客户端接入。先核对适用官方路线、服务端信任和幂等发放。 |
| 游戏内评价 | **H5 待核实。**[评价指南](https://developer.taptap.cn/docs/sdk/review/guide/)是原生 API；MCP 评价查询、点赞、回复是开发者操作，不是 H5 玩家评价 SDK。不得编造 `tap.openReview`。 |

发现官方指南仅是接口证据，不代表某游戏已配置。未知保持 `pending_verification`，有明确证据才标 `unsupported`。不得擅自用本地成就、兑换系统、签到或支付代替平台能力。可靠性与验收配方见[H5 合同](h5-reliability.md)。

## 官方 MCP 独立依赖

按[上游更新流程](upstream-tools.md)先发现已有工具。未连接时读取官方安装指南和当前仓库 README，核实 Node 要求及客户端配置格式。`assets/taptap-mcp.example.json` 是无凭证的**通用 MCP JSON 示例**，不是所有客户端可直接复制的格式。工作目录占位符换成当前游戏绝对路径；Windows 的 `npx` 解析失败按客户端／上游启动方案处理。不为维护 Skill 安装工具或改全局配置。

上游 npm 入口为 `npx -y @taptap/instant-games-open-mcp`；比较当前上游与已安装版本，在游戏证据中记录验证版本。用户自行完成 OAuth 设备授权，token／账号缓存不能进入仓库或前端。安装／更新后重连客户端 MCP 并重新发现 schema。不复制官方服务端／SDK 源码进 Skill，不混用 Maker MCP。

有应用范围的操作先 `get_current_app_info`。未选应用时 `list_developers_and_apps` 展示列表，由用户选定后 `select_app`；当前应用与目标冲突时先解决身份。缓存有应用不代表可以改变它。通用 Skill 维护无需这些操作。

已授权上传的顺序：核对应用与构建目录 → `prepare_h5_upload` → 展示实际应用／目录并取得要求的明确确认 → 按当前 schema 调用 `upload_h5_game`。提审、发布各自记录，准备上传或二维码预览不代表上线。不自动轮询未开通广告，不为研究能力建应用或切换账号。
