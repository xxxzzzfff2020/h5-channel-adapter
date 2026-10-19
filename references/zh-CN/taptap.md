# TapTap H5 目标平台

**2026-10-03** 已核对[官方 H5 MCP 安装说明](https://developer.taptap.cn/minigameapidoc/quick-start/mcp-guide/mcp-setup/)、[上游 MCP](https://github.com/taptap/instant-games-open-mcp)及当前工具 schema，使用时重查。H5 使用宿主注入的全局 `tap`，普通浏览器未必存在。Maker/UrhoX 与原生 Android/iOS/Unity SDK 是不同产品。

## 本地准备

来源可为普通 H5、TapTap H5 或其他平台 H5，先完成[范围选择](selection.md)。新 TapTap 渠道建立独立工程、接入层与存档作用域；已有 TapTap 渠道做三方增量更新，保留正式 key、schema、奖励回执、应用绑定与旧包。不凭目录名推断应用归属。

静态构建保留 `index.html`、正确相对资源和方向。**手动 ZIP 上传与 MCP 构建目录上传是不同输入契约**，按下面的对应路线准备，另保留附 hash 的游戏候选 ZIP。静态通过不证明 `tap` 注入或账号绑定。

TapTap 物料先按下节读取当前 CLI 模块和官方物料要求，再准备选定范围的图文／视频。共享规则含已核实通用规格，但不能由技术检查推断当前应用全套已齐。

## TapTap 物料：按当前 CLI 核对

先用当前已配置的官方 TapTap CLI 读取 `basic-info`、`assets-upload`、`profile-promotion`；用户要求检查 PC 素材时再读 `windows-exclusive`。命令形态：

```sh
taptap-cli app get-app-module --dev-id <developerId> --app-id <appId> --data '{"module_id":"assets-upload"}'
taptap-cli app get-app-module --dev-id <developerId> --app-id <appId> --data '{"module_id":"windows-exclusive"}'
```

以当次 `fields`、`state`、`filled`、`collection_spec`、`image_spec`、`video_spec` 判断。空 Windows 模块表示当前没有可见槽位，不是缺图；不得为查规格自行开启 PC 分发或新增原生 Windows 包。分别列出「本地缺失」「本地已备待上传」「已上传未回填」「后台已回填」与「当前不适用」。素材库收录不等于资料字段已填写。

机器规则表 `assets/material-rules.json` 已补普通物料角色 `banner_4`、`square_promo_image`、`screenshots`、`trailer`、`gameplay_demo_video`，以及 `windows_logo`、`windows_cover`、`windows_cover_vertical`、`windows_library_hero`、`windows_logoless_banner`、`windows_logoless_vertical_banner`；Windows 角色的 `field_id` 是后台真实字段映射。旧 `cover/detail/video` 仅为兼容角色，不能推断具体槽位已满足。最终清单使用精确角色，或显式记录后台字段映射。

逐项读取当前官方 CLI `taptap-cli skills read taptap-cli references/material-requirements.md`，并核实[官方《游戏物料要求》v4](https://developer.taptap.cn/docs/store/release/publish/material/) 的相关章节：图标；电脑/主机封面与 Logo、背景壁纸；实机录屏和截图；推广物料。已核实的通用尺寸/容量只维护在机器规则表；实时字段规格优先，发生差异时在项目专用 `--rules` 文件覆盖，不直接把某个游戏的规格写成全局硬限制。共享 `requirements_verified:false` 保留，因为必填性、可见字段与推荐资格仍须逐应用确认。

区分 16:9 横版宣传图、竖版录屏使用的 1:1 方图、Windows 带标题横/竖封面，以及 Windows 无字横/竖宣传图；后两种 Windows 宣传图必须成对且不得有文字或 Logo，不能拿带标题封面冒充。Windows 壁纸不放文字；独立 Logo 为透明 PNG。横版普通宣传图和方图只放游戏名；方图的主体内容与横版一致。默认不生成不可见或未选平台的素材。

宣传片与实机录屏是不同槽位：带营销字幕的动态 UI 宣传片不得充当纯实机录像。实机内容需前5秒进入核心玩法并连续展示超过10秒，不额外配音/加字幕、不画中画或露出设备 UI；竖版实机录像需配 1:1 宣传图。视频仍按明确选择处理，不为图文盘点调用 FFmpeg。图像像素、机制内容、文案可读性和声音仍需人工核对，技术通过不能报成平台审核通过。首页编辑推荐图只在相关资格及当前工作流适用时准备，不是所有游戏的默认缺项。

## 手动上传 ZIP 的结构与大小

**2026-10-06，Owner 转交的 TapTap H5 后台手动上传表单**要求：“仅支持 .zip，最大 300 MB；解压后必须只有一个文件夹，且该文件夹下包含 index.html。”同一现场的根目录平铺包报错“压缩包根目录包含 7 个文件或目录”。这是后台手动 ZIP 路线的现场证据，使用时仍核对当前表单。

共享规则 `assets/package-rules.json` 将这一路线标为 `manual_zip`，按十进制保守口径记录 **300,000,000 字节**上限，比较实际 ZIP 文件大小。正确结构如下，`game/` 可换为本游戏的文件夹名：

```text
game.zip
└── game/
    ├── index.html
    ├── assets/
    └── audio/
```

先把验证过的构建内容放进一个干净的游戏文件夹，再压缩**整个游戏文件夹**；不要只选文件夹内的内容进行平铺压缩。`index.html` 必须直接位于唯一顶层文件夹内，不能放在 ZIP 根部或再多套一层。ZIP 根部不能另有 README、第二个文件夹（包括空文件夹）或任何其他文件。排除 `.DS_Store`、`__MACOSX`、无需发布的工程文件、凭证及测试文件，保留实际运行所需的 JS 和资源；目录穿越、绝对路径和符号链接也不能打入包。保留旧包，对新候选包执行两项检查：

```sh
python3 <skill-dir>/scripts/verify_game_package.py <game.zip> --channel taptap --report <new-preflight.json>
python3 <skill-dir>/scripts/check_package_budget.py <game.zip> --channels taptap --stage candidate --report <new-budget.json>
```

Windows 使用已核实的 `py -3` 或 `python`，真实路径加引号。预检拒绝错误层级和超限，包体报告给出实际字节、上限及资源占用；两者均为本地只读检查，不上传文件。

**MCP 路线：**当前工具接收经确认的**构建目录**，不是任意源码或物料 ZIP。按当前 `prepare_h5_upload`／`upload_h5_game` schema 确认目录入口和工具生成 ZIP 的结构，不把上述手动 ZIP 外包文件夹机械套到 MCP 输入上，也不凭手动路线推断 MCP 包体限制。`verify_game_package.py --channel taptap` 与包体表的 TapTap 项目前对应手动 ZIP 候选，不认证 MCP 构建目录或工具内部制品。233／4399 仍使用各自的 ZIP 根目录 `index.html` 规则，不套用此层级。

## 两阶段接入与发布边界

真机自动化仅在明确要求时读取[安卓真机流程](android-taptap-automation.md)，并先完成启动确认；普通接入不占设备、不安装环境。缺图及 CDN 子目录问题按[部署资源排查](deployed-assets.md)处理。

本节采用维护者于 **2026-10-06** 确认的后台接入顺序：**创建应用 → 接入所选非广告功能 → 本地首包 → 按当前分路线授权上传 → 后台设置横竖屏 → MCP 核验并接广告 → 再出候选包**。适用于本地开发约完成 90%、核心流程已能运行时启动适配；“90%”是交接时机，不是验收成绩。当前 `get_ads_integration_workflow` 另确认广告生效状态、方向和有效广告位是生成接入代码的前提；首包顺序按本工作流执行，具体后台行为在项目中核实。

**禁止为了开通或接入广告而发布应用。** 发布可能直接完成审核并提前对外可见，不能假定还有人工审核缓冲。创建应用、上传首包、设置方向、广告配置、提审、发布分别记录；接入授权不包含提审或发布。物料尚缺时尤其不能用“先发布再补”推进。即使 MCP／后台提示发布，也停在该动作前说明冲突，不代点发布、不调用等效 API，也不靠组合工具绕过；只继续独立的本地工作。正式提审／发布留到物料与相应验收齐备、Owner 明确授权后。

### 阶段一：先接非广告功能并生成首包

1. 核实来源、目标 `app_id`、既有工程和[已选功能](selection.md)。后台应用已创建后，按下文 MCP 应用核对流程确认目标；没有应用则先提供建项资料，按实际授权创建或由 Owner 完成，不发布。
2. 通过相应 MCP 指南，先完成**本轮已选、当前 H5 路线可用**的非广告功能，例如身份、云档、排行榜、分享和振动。保留产品规则、旧档和应用绑定。“除广告外”不表示强制加全套功能；待核实能力记录为待核实，不编造接口。
3. 新接入的广告保持未配置，按钮隐藏或明确不可用，不使用示例广告位或假完播发奖，也不让广告配置阻塞普通玩法。增量维护保留已有有效接入，不为套首包流程拆掉广告。按实际方向构建并检查 `index.html`、资源、关键功能和存档，生成附版本、大小及 SHA-256 的本地候选 ZIP；MCP 接收构建目录时，固定并记录对应目录清单／哈希与 ZIP 的关系。
4. 在已有交付记录列出已接功能、首包、待补物料和广告待办。按[分路线授权](h5-reliability.md#h5-上传与发布授权)核对目标、制品、用途与命令实际副作用；已授权 `taptap-cli` 纯上传不逐包二次确认。MCP 发布或可能组合提审／发布／线上覆盖的上传须按[影响边界](#自动提审与发布影响)取得本次具体确认。未知影响先核查，不以“测试包”保证安全；上传结果未知时只读核查，不自动重传、不以发布作为补救。

### 阶段二：上传后确认方向，再接广告

1. 确认同一应用已有成功上传的首包记录，再在后台完成横屏／竖屏选择，保存并核实实际值与游戏一致。Owner 已明确的方向直接沿用；如用 MCP `update_app_info` 设置 `screenOrientation`，先核对当前 schema 和本次修改授权，仅改方向，不附带发布操作。
2. 按当前 `get_ads_integration_workflow` 核对应用，再执行 `check_ads_status`；仅 `status === 1`、方向正确且本次查询自动匹配到有效广告位，才调用 `get_ad_integration_guide` 并接入所选广告类型。不手填广告位。未开通、封禁、方向缺失或服务端配置异常，只停广告接入，按返回原因处理；不得用发布解锁，也不自动轮询。
3. 按本页广告生命周期和奖励合同验证，重建含广告的候选包。新包按当前分路线授权执行；新的 MCP 发布／组合提审须本次具体确认，已授权 CLI 纯上传不再逐包确认。TapTap 宿主播放、真机、物料、提审和公开发布各有独立状态，缺少证据保持待验。

已有 TapTap 工程先只读核实首包、方向、广告状态与既有接入，复用已满足的步骤，不为“首包”重复上传或发布。未选择广告的任务在所选非广告功能及本地交付完成后收口，不强制走广告阶段。

### 开发对话交接模板

Owner 指定开发对话并要求转交时，填入已知项目资料后发送下面的完整工单；未指定接收方时交付可复制文本，不猜测对话或自动派单。流程正文仍以本页为准。

```text
使用 $h5-channel-adapter，为 <项目绝对路径> 接入 TapTap H5。
目标应用：<已确认 app_id 或待创建>；游戏方向：<横屏／竖屏或待确认>。
本轮功能和物料范围：<沿用现有明确选择；仅列实际缺项>。
先读 Skill 的 references/zh-CN/taptap.md“两阶段接入与发布边界”，按当前工程增量实施，保留旧档、应用绑定和既有有效接入。
应用创建后先通过 MCP 接好所选且已核实可用的非广告功能，本地验证并生成首包，交付版本、路径、大小、SHA-256、功能状态和待补物料。
上传前核对并记录目标、具体制品、用途及命令实际副作用；已授权 taptap-cli 纯上传无需逐包二次确认。MCP 发布／组合提审前须告知目标、版本／SHA-256、动作与影响，并取得本次具体确认。CLI 上传授权不含绑定／提审／发布／配置变更；不为接广告而提审或发布。
首包上传确认成功后，在后台设置并核对横竖屏，再按 MCP 工作流查询本应用广告状态与自动匹配的有效广告位，条件满足后才获取指南接入广告。
接广告后完成相关验证、重新打包；新包按分路线授权执行，MCP 发布／组合提审另做本次具体确认。已有首包和方向证据可复用，不重复上传。未选广告则跳过广告阶段。
在项目已有交付记录区分本地完成、宿主／真机待验、物料、上传、提审和发布状态，并给出下一步；接入完成不代表上线。
```

## 自动提审与发布影响

**2026-10-10** 项目现场记录了 `upload_h5_game` 实际进入审核，后台同时存在“过审后立即发布”设置。提交审核属于危险外部操作：发生前明确告知可能进入审核，审核通过可能直接对外可见。上传成功文字、刷新或看似安全的状态文字不能证明无风险或已撤审。这是该路线的实际观察，不泛化成所有工具版本必然相同行为。

MCP 调用可能把上传与提审／发布／线上覆盖合并时，先列出具体目标／app、制品版本／SHA-256、动作及影响，并取得 Owner 对本次动作的明确确认。设备启动同意、概括或既往上传授权不覆盖此动作。CLI 命令先核实是否纯上传；绑定／提审／发布／配置按各自具体授权执行，不能借用纯上传豁免。统一按[授权规则](h5-reliability.md#h5-上传与发布授权)处理，不先无授权提审再撤审。

撤审需独立明确授权，之后重新核实实际审核和公开状态；不能保证一定早于过审。执行前重新发现工具，没有暴露撤审工具就如实说明，已授权后台 UI 仅作为可能的补充，不承诺能力或自动代操作。禁止仅为开通广告而发布的边界继续适用。

## 窗口几何与安全区

于 **2026-10-16** 重读官方 [getWindowInfo](https://developer.taptap.cn/minigameapidoc/dev/api/base/system/tap.getWindowInfo/) 与 [getDeviceInfo](https://developer.taptap.cn/minigameapidoc/dev/api/base/system/tap.getDeviceInfo/)。前者提供窗口尺寸、`screenTop`，并明确 `safeArea` 是**竖屏正方向**的安全区域、部分机型可能缺失；后者提供平台／型号等基础信息，新型号可能显示 unknown。缺失／零值不证明屏幕无遮挡，设备信息也不是刘海尺寸测量。身份使用针对性的设备接口，不为本次布局修复追加旧 `getSystemInfo` 或新权限。

坐标换算、限定兜底与回归证据统一执行[安全区、宿主原点与胶囊合同](h5-reliability.md#安全区宿主原点与胶囊布局)。原生系统边距与局部右上角胶囊避让分开；案例尺寸是项目选择，不是 TapTap 默认值，替身／浏览器覆盖不能证明原生 iPhone 验收。按[验证记录](../../assets/validation-status.example.md)记录实际视口／应用矩形及另行核实的候选身份。

## 分功能选择，再核对当前应用

| 功能 | 已确认路线与边界 |
| --- | --- |
| 广告 | 按[两阶段流程](#两阶段接入与发布边界)先完成首包上传与后台方向核验，再按 `get_ads_integration_workflow` 核对当前应用、执行 `check_ads_status`；已生效且自动取得有效广告位才调用 `get_ad_integration_guide`。不索要、手抄或沿用旧广告位。真实成功回调与奖励落盘另验。 |
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

## 云档读取兼容与上传预算

**2026-10-19** 按宿主全局 `tap` 核对：官方 [H5 云档指南](https://developer.taptap.cn/minigameapidoc/dev/tutorial/open-capabilities/cloud-save-tutorial/)、[createArchive](https://developer.taptap.cn/minigameapidoc/dev/api/open-api/cloudsave/CloudSaveManager.createArchive/) 和 [updateArchive](https://developer.taptap.cn/minigameapidoc/dev/api/open-api/cloudsave/CloudSaveManager.updateArchive/) 规定创建／更新每分钟最多一次，超频错误码为 `400001`。[SDK v4 功能页](https://developer.taptap.cn/docs/sdk/tap-cloudsave/features/) 记载另一频率（每分钟 60 次），不能移用到 H5；使用时重查当前 H5 合同。仅有 errMsg 的回调不能证明发生了数字码 `400001`。

官方 [readFile](https://developer.taptap.cn/minigameapidoc/dev/api/file/FileSystemManager.readFile/) 使用回调、不支持 Promise 风格；不传 `encoding` 时返回二进制 `ArrayBuffer`。[getArchiveData](https://developer.taptap.cn/minigameapidoc/dev/api/open-api/cloudsave/CloudSaveManager.getArchiveData/) 接收已捕获的 `archiveUUID` 与 `archiveFileId`；不传 `targetFilePath` 时由宿主创建临时文件并返回路径。这些是文档接口，以下有界兜底和协调策略是工程建议，不是额外 SDK 保证。

- 分别诊断本地持久化、运行时身份、云列表／下载／文件读取／校验、配额预留及云提交。云端缺数据不证明 UID、实名或防沉迷被拒；本地 `QuotaExceededError` 不能证明身份失败。遵循[通用存储／冲突合同](h5-reliability.md#身份本地存档与云)。
- 主档读取独立于可选诊断／配额文件。先读 UTF-8；明确读取失败后最多一次二进制读取，严格 UTF-8 解码并拒绝非法字节。固定下载文件仍明确不可读时，最多一次由宿主选临时路径的重下载，保持**同一已捕获 UUID/fileId**，沿用一次 UTF-8／至多一次二进制读取，不再重下载。超时结果未知时不并发启动兜底。使用前按官方宿主存储根校验返回本地路径（拒绝越界或任意 URL）、字节上限、JSON、schema、checksum、归属／谱系，以及最终账号／请求身份。内容无效不是换档、制造空数据或覆盖云进度的理由。
- 按[默认停用诊断及隐私合同](h5-reliability.md#启动布局性能与诊断)处理。明确重新启用诊断时，保守统一协调同账号／游戏的适用 create/update：首次创建、手动／force、自动保存、诊断及重试。不同名称／UUID、独立计时器、串行执行或主档成功后短暂延迟都不证明配额隔离；主档优先，诊断可丢弃。服务端具体限流作用域仍需目标宿主证据；结构性竞争风险不等于所有线上失败的原因。
- 即使诊断关闭，所有主档路径仍遵守上述预算：手动／关键优先级、`force`、首次创建及替换均不豁免。按[队列与真实状态合同](h5-reliability.md#云保存队列与真实状态)处理；停用竞争写入方不能证明已有完整共享仲裁或跨设备安全。
- 不可读的旧诊断 pending 标记继续按未知操作保留，不能为开局将其删除或宣称已结算。独立受保护的主档仅可按目标已验证的恢复策略恢复提交：根据已核实限频保守设置单调时钟冷启动等待、取可信写入时间戳最大值、精确读回持久化时间／pending 预留、核对当前账号／token，且无并发操作。项目额外等待余量不是官方间隔或通用默认值；时间经过也不证明未知远端写已失败。没有持久标记后端时继续阻止云提交并保留本地进度，只读主档恢复保持独立。

在目标真实实现中验证仅 errMsg 错误、非法二进制、错误路径／归属、fileId／账号变化、未知超时、可选文件不可用、旧 pending 及停用诊断输入。区分本地替身和宿主／真机验收；后续上传／重开成功不能证明此前失败都同因，也不能证明另一设备的本地写失败已修复。

## 激励广告生命周期与漏奖励排查

**2026-10-06** 核对[官方激励视频说明](https://developer.taptap.cn/minigameapidoc/dev/tutorial/open-capabilities/ad/rewarded-video-ad/)、[创建接口](https://developer.taptap.cn/minigameapidoc/dev/api/ad/tap.createRewardedVideoAd/)、[关闭回调](https://developer.taptap.cn/minigameapidoc/dev/api/ad/RewardedVideoAd.onClose/)与[销毁接口](https://developer.taptap.cn/minigameapidoc/dev/api/ad/RewardedVideoAd.destroy/)。官方依据覆盖自动加载、就绪检查、显示失败后的加载恢复、布尔 `isEnded`、默认单例与可选 `multiton: true`。教程描述默认单例，创建接口明确给出多例选项。以下事务、事件乱序、超时和诊断策略属于工程建议，需目标项目验证，不是额外 SDK 保证；仅用于 H5／小游戏全局 `tap`，不套用 Maker/UrhoX 回调。

1. **加载与显示：**显示前绑定 load/error/close 监听并确保素材就绪。可等待 `load()`，也可复用确认已加载的素材；存在自动加载，不强制每次再 load。明确且可恢复的 show 失败，每个奖励请求最多一次 `load → show` 恢复。同一失败的 `onError` 与 Promise 拒绝合并为一次状态迁移、共用一次恢复预算。停在 `show.begin` 没有结果是未知，不能并发重开广告。
2. **实例所有权：**统一管理器维护单个有效奖励请求。可保留稳定的默认共享实例方案，也可按需用 `multiton: true` 创建请求独占实例；多例不等于允许并发广告。`requestId` 关联请求与回调，`attemptId` 区分显示／恢复尝试；两者都不能替代[奖励合同](h5-reliability.md#奖励确认与可恢复入账)中的具体权益领取键。本地 ID 不代表 SDK 回调携带 ID。旧请求未明确收口时，不能让新请求接管共享实例并把下一次 `onClose` 机械归给它；按已核实的实例／监听生命周期隔离迟到事件。仅移除自己绑定的同一监听函数和计时器，只销毁本人独占实例，不销毁其他入口共用实例；再次 create 本身不证明独占。两条路线均保留上文目标应用与 MCP 广告配置核验。
3. **外跳与取消：**隐藏或跳到外部 App 不是取消，不立即解绑或销毁。部分宿主不改变 `document.hidden`，须核实可用平台生命周期，统一处理并去重平台／DOM 通知。后台暂停前台等待预算，返回宽限单独配置，同时保留总请求过期策略和可操作的取消／恢复入口。返回仅恢复原请求等待，不发奖、不重新展示。UI 取消／超时不等于关闭或取消宿主广告。明确取消、终止、切号或换目标后，迟到回调不得给新请求发奖；此前已确认的权益按恢复合同处理。恢复 UI 不能假装宿主未决操作已结束，也不能无限等待或重叠请求。
4. **发奖判据与事件顺序：**只有 `onClose` 的布尔 `isEnded === true`，且原请求、身份、目标仍有效，才允许结算；false、缺失和字符串 `"true"` 均不是成功。已发起显示且回调归属有效时，即使 `show()` 仍未返回，也可接受完成确认；不能用仅在 `show().then(...)` 才置真的 `shown` 锁漏掉它。确认后迟到的 resolve／reject／error 不得重播广告或推翻已确认入账。覆盖这些乱序测试，不把它们写成官方回调顺序保证。`show()` 成功、外部 App 体验、广告里的“奖励已领取”、返回游戏和观看时长都不是奖励回执；对有效官方完成也不另加本地最低观看时长。始终没有成功终态时只能改善等待／恢复体验与取证，不自动补奖，不宣称平台根因已修复。
5. **持久化：**确认与已保存分开；跨刷新恢复、保存重试和旧档对账按[确认账本与权益合同](h5-reliability.md#奖励确认与可恢复入账)执行。已确认奖励的保存重试不能要求重新看广告。云列表、下载、文件读取、创建／更新分别记结果；读取失败不是空档，不能清空本地。奖励次数与进度分属多个存储实体时，逐个验证提交及恢复，见[存储合同](h5-reliability.md#身份本地存档与云)。
6. **有界诊断：**记录 create、load 开始／结果、show 开始／结果、hide／return、close／完成标记、奖励校验／去重、本地保存及云阶段，附 buildId、可用宿主版本、request／attempt ID 和时间／耗时；ID 不嵌账号信息。按[通用诊断白名单及默认关闭云诊断规则](h5-reliability.md#启动布局性能与诊断)处理，自由错误文本归一为固定类别，保留数字码是否存在及回调字段类型。可选 JSON 导出／复制近期诊断须有事件数和字节上限，验证宿主支持和失败反馈，不把导出变成无限原始日志。

诊断区分 `show.begin` 与已确认展示，并补齐有界的 `reward.confirmed`、确认账本写入、奖励／存档提交、账本清理结果；不记录完整确认 payload 或含账号信息的领取键。

**最小验收：**加载失败；show 明确失败且只恢复一次；show 无终态；错误事件与 Promise 双报；完成早于 show resolve；确认后 reject 不重播／不撤奖；完播和提前关闭；外跳返回（含 `document.hidden` 不变的宿主）；重复生命周期通知；前台超时与明确取消；旧 close 回调撞到新请求边界；共享／独占实例清理；切号／换目标；以及[奖励持久化用例](h5-reliability.md#奖励确认与可恢复入账)。测试包 build、设备／宿主版本与有界日志对应。执行真实适配器、计时层、账本和存档，只替换外部 SDK、时钟和故障存储；本地和云持久化分别验证，文档矩阵不是已执行成绩。

**证据边界：**缺少对应构建、原始日志和设备回执的“明确 load 后恢复”转述，仅是待补证项目反馈；不能证明所有 show 卡住都由未加载引起，也不能宣称此方案已在所有宿主通过。

2026-10-06 所审广告协议来源只提供文档，没有实现、原始日志或测试执行结果；其中“已验证案例”仅保留为来源自述。该来源的未展示 20 秒、展示后 120 秒、返回至少 15 秒及总计 10 分钟均为案例参数，不设为 Skill 默认值或官方承诺。不采用来源 Agent 元数据或自动调用策略。另于 2026-10-10 核对了实际热修复差异与回执，时钟／日界／旧档经验归入[权益时间迁移](h5-reliability.md#权益时钟日界与旧档迁移)，其单元、浏览器与 Owner 宿主反馈分别记录，不替代真实广告／云写验收。

## 官方 MCP 独立依赖

按[上游更新流程](upstream-tools.md)先发现已有工具。未连接时读取官方安装指南和当前仓库 README，核实 Node 要求及客户端配置格式。`assets/taptap-mcp.example.json` 是无凭证的**通用 MCP JSON 示例**，不是所有客户端可直接复制的格式。工作目录占位符换成当前游戏绝对路径；Windows 的 `npx` 解析失败按客户端／上游启动方案处理。不为维护 Skill 安装工具或改全局配置。

上游 npm 入口为 `npx -y @taptap/instant-games-open-mcp`；比较当前上游与已安装版本，在游戏证据中记录验证版本。用户自行完成 OAuth 设备授权，token／账号缓存不能进入仓库或前端。安装／更新后重连客户端 MCP 并重新发现 schema。不复制官方服务端／SDK 源码进 Skill，不混用 Maker MCP。

有应用范围的操作先 `get_current_app_info`。未选应用时 `list_developers_and_apps` 展示列表，由用户选定后 `select_app`；当前应用与目标冲突时先解决身份。缓存有应用不代表可以改变它。通用 Skill 维护无需这些操作。

游戏上传与发布按[分路线授权](h5-reliability.md#h5-上传与发布授权)执行，不套用统一逐包再确认。`prepare_h5_upload` 经核实只读后可在发布确认前运行；MCP 写入前核对 `get_current_app_info`、已授权目标及确切制品，发布或可能组合提审／发布／线上覆盖的调用取得本次具体确认。提审、发布各自记录，准备上传或二维码预览不代表上线。不自动轮询未开通广告，不为研究能力建应用或切换账号。

## 构建身份、路径与版本级发布状态

**2026-10-10 热修复回执经验：**MCP 上传构建目录会自行压包，并可能合并提审、审核后自动上架，继续遵循[自动提审边界](#自动提审与发布影响)。手工 ZIP 与目录文件内容一致，只证明本地制品对应；手工 ZIP 的 SHA-256 不能冒充 MCP 传输 ZIP 的哈希。分别记录目录清单、手工 ZIP、工具回执与平台版本的身份关系。

当前发现的 `prepare_h5_upload` schema 要求相对 `gamePath`，使用时重查。相对路径由 **MCP 实际工作目录**解析，不能用当前终端 cwd 或旧项目推断。先核实选中应用、工具工作目录、明确的构建路径和入口；在已确认 prepare 为只读时，核对它解析出的**绝对目录**与冻结候选一致，再执行已授权动作，并在适用时做 MCP 发布／组合提审的具体确认。没有足够返回信息时补只读核对或停在缺口，不猜目录、不盲传绝对路径、不把上传当路径探测。上传前路径及文件清单再次核对。

开发轮次与文件后缀不是版本序列：后续某轮 `r1` 可保留前轮 `r2` 的功能，不凭跨轮次后缀断言回退。比较实际 `buildId`、包内功能／文件哈希及上传回执；构建编号、平台版本号和包体 ID 不互相替代。

上传、主包绑定、提审、通过和发布分别保留回执。在当前授权内只绑定现场已就绪候选；当前 schema 提供 `package_slots.expected` 时核对其与目标主槽一致。审核准备快照、预检、提交须对应同一版本及明确发布计划，随后读回状态。“审核通过后立即发布”是计划，不是已通过／已发布。已保存回执只描述记录时点，不是后台实时状态；遵循[按路线授权](h5-reliability.md#h5-上传与发布授权)，不把旧确认延伸到新动作。

审核后查询**版本级**线上与草稿／审核信息，并映射到本次构建。应用级“已发布”可能仍指旧线上包，上传文字“发布成功”也可能同时说明新包在审核中。旧版本线上、新版本审核时，只报告新包已上传提审、等待审核／发布；测试二维码或 Owner 行为正常反馈不证明正式线上已切换。该来源最后回执处于此等待阶段，不作为当前实时状态或已上线证据。
