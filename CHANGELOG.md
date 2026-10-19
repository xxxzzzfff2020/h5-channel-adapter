# Changelog / 更新记录

## 0.6.0 — 2026-10-19

`VERSION` is the canonical release identity. This release collects the dated maintenance entries below; their dates describe the work, not separate published versions. The earlier 2026-10-03 heading anticipated 0.6.0 while `VERSION` and the latest tag remained 0.5.0. / `VERSION` 为统一发布版本标识。本版汇总以下按日期记录的维护；日期是工作发生时间，不代表独立发布版本。2026-10-03 的旧标题提前记为 0.6.0，当时 `VERSION` 与最新标签仍为 0.5.0。

- Require installed-file freshness checks at each new adapter task; document safe updates, pinned tags and shared symlink versus independent-copy behavior without claiming existing chats have reloaded. / 新任务核对实际安装文件，说明安全更新、固定标签与符号链接／独立副本差异，不宣称既有聊天已重载。
- Correct the gameplay-video lower bound to strictly more than 15 seconds while retaining the inclusive trailer bound; remove an unrelated 4399 provenance-date drift. / 修正实机录屏须严格超过 15 秒，保留宣传片可等于 15 秒，并还原无关的 4399 来源日期漂移。

### 2026-10-19

- Add latest-intent queue recovery, hard-gated priority, lifecycle/account fencing and evidence-based bilingual save statuses, with an explicitly unexecuted behavioral acceptance matrix. Preserve existing cloud/reward/conflict safeguards; no runtime implementation or device acceptance is implied. / 补最新意图队列恢复、受硬门约束的优先级、生命周期／账号隔离与基于证据的双语保存状态，并增加明确未执行的行为验收矩阵；保留云档／奖励／冲突保护，不冒充运行时实现或真机验收。
- Clarify native durability, missing/corrupt/unknown reads, bounded TapTap read fallbacks and semantic conflict comparison versus strict stale-selection guards. Default separate diagnostic cloud archives off, preserve pending/main-save protections, and distinguish H5 upload budgeting from SDK v4 limits. Extend evidence records without importing game identifiers, case timings or device/release claims. / 明确原生持久化、缺失／损坏／未知读取、TapTap 有界读取兜底，以及语义冲突比较与严格防过期选择保护；独立诊断云档默认关闭，保留 pending／主档保护，区分 H5 上传预算与 SDK v4 限额；补证据记录，不导入游戏标识、案例等待值或真机／发布结论。

### 2026-10-16

- Route developer/Owner tools through Settings, isolate test rewards/saves and exclude production cheats/simulated ad completion; add narrow-screen, lifecycle/preferences and production-artifact acceptance guidance without claiming a game implementation. / 开发者／Owner 工具收纳到设置，隔离测试奖励／存档，生产排除作弊／模拟广告完成；补窄屏、生命周期／偏好和生产制品验收指导，不冒充游戏实现。
- Replace the blanket upload reconfirmation rule with the current Owner policy: authorized taptap-cli upload-only tasks need no per-artifact second confirmation; MCP publication/combined-submit actions require specific confirmation, while binding/review/release/configuration remain separately authorized. Synchronize workflow entry points. / 按当前 Owner 规则替换统一逐包再确认：已授权 taptap-cli 纯上传不二次确认，MCP 发布／组合提审须本次具体确认，绑定／提审／发布／配置仍按各自授权；同步流程入口。

- Add bilingual safe-area coordinate normalization, platform-scoped missing-data fallback, local capsule placement and observable regression guidance; distinguish project heuristics from official dimensions and browser fixtures/public testing from native-device/release acceptance. Link TapTap window/device APIs and extend the per-game validation record. / 补安全区坐标归一化、按平台限定的缺数据兜底、局部胶囊布局及可观察回归指导；区分项目启发式与官方尺寸、浏览器替身／公测与真机／发布验收，并补 TapTap 窗口／设备接口入口及逐游戏验证记录。

### 2026-10-15

- Add app-scoped TapTap CLI material inventory, precise mobile/Windows scene roles and official v4 defaults; validate paired logoless images, portrait-video square covers, screenshot ratio/count and video duration. Preserve conditional field visibility and upload-versus-draft binding boundaries. / 补 TapTap CLI 逐应用物料盘点、移动端与 Windows 精确素材角色和 v4 通用规则；校验无字图成对、竖录方图、截图比例数量与视频时长，保留动态可见性及上传／回填边界。

### 2026-10-13

- Add channel-specific music decisions, built branding checks and scoped 4399 upload name/2G field preflight. / 补逐平台音乐选择、成品竞品文案检查和 4399 上传文件名／2G 字段预检。
- Add native-store boot/recovery exception guidance, current XHS builder identity/resource review, explicit video geometry checks and organized artifact delivery. / 补原生存储异常指引、小红书构建器身份／资源审查、视频明确宽高检查与交付身份记录。

### 2026-10-12

- Enforce the Owner-reported 4399 video-cover limit with a conservative 500,000-byte cap, scoped to that image role; add byte/dimension and repair/recheck regressions. / 按 Owner 当前后台反馈为 4399 视频封面执行保守 500,000 字节上限，仅限该图片字段；补字节／尺寸与修复复查回归。
- Add bilingual 4399 listing copy with explicit game width, height and orientation, separate from promotional-media specifications; preserve unknown rejection reasons and pending Owner-corrected artifacts. / 新增含游戏宽高与方向的双语 4399 上架文案模板，与宣传物料规格分开；保留未知拒绝原因和 Owner 修正产物待验状态。

### 2026-10-10

- Incorporate inspected time-hotfix lessons: rollback sampling, save/journal day migration, bounded valid boosts, entitlement/offline/cloud time separation, live daily refresh and evidence boundaries; verify MCP-resolved build paths and version-level review versus online state. / 汇入已核对时间热修复经验：回拨采样、主档／日志日界迁移、合法加速、权益／离线／云时间隔离、长开跨日及证据边界；补 MCP 路径解析和版本级审核／线上核验。
- Add opt-in Android USB-device TapTap automation with full-flow startup confirmation, existing-tool/package reuse, fresh preview identity, conditional CDP and per-case read/write evidence; document observed automatic review and immediate-release risk plus CDN subdirectory resource diagnosis. / 新增按需安卓 USB 真机 TapTap 自动化：完整启动确认、复用工具与包、新鲜版本身份、有条件 CDP 及逐用例读写证据；纳入实测自动提审／立即发布风险与 CDN 子目录资源排查。

### 2026-10-06

- Correct TapTap manual ZIP packaging from the Owner-reported 2026-10-06 form: exactly one top-level folder with a direct index.html, at most 300 decimal MB; add dedicated preflight and regressions while preserving MCP build-directory and 233/4399 contracts. / 按 2026-10-06 Owner 转交后台表单修正 TapTap 手动 ZIP：唯一顶层文件夹内直接包含 index.html、最多十进制 300 MB；补专属预检及回归，保留 MCP 构建目录和 233／4399 独立契约。
- Add the TapTap onboarding sequence and developer handoff: selected non-ad features before the first package, per-artifact confirmed upload and backend orientation before ads, and no publication to enable ads; align workflow entry points with the upload gate (authorization policy superseded on 2026-10-16). / 新增 TapTap 两阶段接入及开发交接模板：首包前接所选非广告功能，逐包确认上传和后台方向核验后接广告，禁止为接广告发布；同步各流程入口的上传确认边界（授权规则已由 2026-10-16 条目替代）。
- Extend rewarded-ad guidance for completion before show resolves, optional owned instances, verified/deduplicated host lifecycle, entitlement-level idempotency and recoverable confirmation-ledger commits; keep source assertions and case timeouts separate from executed evidence and defaults. / 补充完成早于 show 返回、可选独占实例、宿主生命周期核验去重、权益级幂等与确认账本恢复；来源自述和案例时长不冒充执行证据或默认值。
- Historical upload-confirmation policy, superseded by the route-specific Owner policy on 2026-10-16; target/hash/purpose/effect checks remain. / 历史上传确认规则已由 2026-10-16 分路线 Owner 规则替代；目标／哈希／用途／影响核对继续保留。

### 2026-10-04

- Clarify TapTap rewarded-ad readiness, shared request ownership, external-jump handling, one recovery budget, durable reward commits and bounded diagnostics; separate official API evidence from uncorroborated device anecdotes. / 补充 TapTap 广告就绪、共享请求所有权、外跳、单次恢复预算、奖励持久化与有界诊断；区分官方接口证据和待补证设备转述。

### 2026-10-03 — originally labeled 0.6.0 / 原记为 0.6.0

- Accept generic, TapTap and other-platform H5 sources; add TapTap as the sixth target, including same-channel maintenance. / 接受普通、TapTap 与其他平台 H5 来源，新增 TapTap 第六目标及同渠道维护。
- Persist explicit per-target capability/material choices and validate resumed scope; unselected work never becomes enabled by default. / 保存逐平台功能与物料选择，恢复时校验范围，未选项目不默认启用。
- Add independent official MiniGame MCP setup and capability boundaries, plus reusable H5 reliability/acceptance recipes with coverage notes. / 补官方 MiniGame MCP 独立接入、能力边界及 H5 可靠性／验收配方与覆盖表。
- Extend package and material helpers for TapTap, leaving unverified platform limits explicit. / 检查脚本支持 TapTap，未知规格保持待核实。
## 0.5.0 — 2026-09-23

- Treat 4399's video export dimensions/codec and prepared detail-shot sizes/count as studio recommendations, not platform rejection rules. / 4399 宣传片导出尺寸与编码、预备详情图尺寸和数量只提醒，不再冒充平台硬限制。
- Add a bounded read-only game-package preflight for ZIP integrity, entry layout, static assets, common release residue and selected channel constraints. / 新增只读游戏包静态预检，检查 ZIP 完整性、入口、静态资源与常见发行残留。
- Add a compact per-game validation-state template. Real SDK, host, device and review results remain separate from static checks. / 增加简短的单游戏验证状态模板，静态检查不代替真实 SDK、宿主、真机与审核结果。

For stable internal use, pin a tested release tag; updating this Skill does not rebuild previously delivered game packages. / 内部稳定使用可固定已验证的发布标签；更新 Skill 不会自动重建已交付游戏包。

## 0.4.0 — 2026-09-22

- Make video processing opt-in during material selection; image/copy and project-only workflows do not require FFmpeg. / 物料选择新增可选视频，图文与仅工程流程无需 FFmpeg。
- Read PNG/JPEG/WebP dimensions with Python; default inventory skips audio/video probing. Material reports distinguish checked scope from deferred video. / Python 读取图片尺寸，盘点默认跳过音视频探测，报告明确待补视频。
- Add an FFmpeg-free test suite and refresh bilingual README navigation, artwork and official platform icons. / 新增无 FFmpeg 测试，润色双语首页并加入横幅与官方平台图标。

Migration: material manifests now default to `processing.video: false`; set it to `true` only for explicitly selected video work. / 清单现在默认不处理视频，明确选择后才设为 true。

## 0.3.0 — 2026-09-22

- Rework English and Chinese documentation around purpose, deliverables and quick start. / 中英文首页聚焦定位、交付与快速使用。
- Present all five platform profiles in guided selection and keep project-specific details outside the distribution. / 引导选择覆盖五个平台，项目专属内容不进入分发包。
- Add bilingual contribution guides and issue/PR templates for platform additions, rule updates and fixes. / 新增中英文贡献指南及 Issue、PR 模板。

## 0.2.0 — 2026-09-22

- Add Xiaohongshu, Bilibili TOY and Xingxia listing fields, formats, ratios, optional media and limits to shared material validation. / 收录三个后台表单字段和物料规则，推荐尺寸与强制要求分开。
- Add read-only actual-artifact budget reports and an explicit per-channel reduction-choice workflow, including complete media/settings/playback cleanup after a chosen removal. / 新增实际包体报告与超限方案选择，选定删减后同步资源、设置和播放逻辑。
- Keep listing media separate from game-package budgets; preserve unknown limits, original sources and upstream official-tool updates. / 区分宣传物料与游戏包体，保留未知项、原源和官方工具更新机制。

## 0.1.0 — 2026-09-22

- Publish the first private, portable Skill distribution with English and Simplified Chinese entry points, workflows and platform notes. / 首个私有可分享版本，提供中英文入口、流程与平台说明。
- Introduce the two-phase source/materials/configuration workflow and 233/4399 platform profiles. / 提供先源码物料、后补配置出包的两轮流程与 233/4399 平台说明。
- Add integration references for Xingxia, Xiaohongshu MiniTool and Bilibili TOY. / 新增星匣、小红书与 B 站 TOY 接入说明。
- Keep official Skills/CLI/MCP upstream; inspect versions and schemas at use time and surface relevant updates. / 官方工具独立维护，使用时核版本/schema 并提示更新。
- Add macOS/Windows guidance, explicit UTF-8 media-process decoding, ASCII-safe CLI JSON and portable synthetic helper checks. / 补跨系统说明、UTF-8 进程解码、兼容控制台 JSON 与合成工具测试。
- Remove personal paths, private task IDs and game-specific artifacts from the distributable source. / 分享源移除个人路径、私有任务 ID 和游戏专属制品。
