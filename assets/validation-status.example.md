# Per-game validation / 单游戏验证状态

Copy one row per selected channel and capability into that game's delivery notes. Use `unknown` until the named layer was actually exercised. Add the tested package version, date and a redacted local evidence path or platform receipt to each completed cell. Keep account secrets and private evidence out of this public Skill repository.

按本次选择的渠道与能力复制行到游戏交付文档。未实际验证的层级写 `未知`；完成的格子附候选包版本、日期和脱敏证据路径或平台回执。账号密钥与私人证据不进入公开 Skill 仓库。

| Channel + capability / 渠道与能力 | Current docs / 当前文档 | Local candidate / 本地候选 | Host / 平台宿主 | Device / 真机 | Upload, review, permission / 上传审核权限 |
| --- | --- | --- | --- | --- | --- |
| `<selected channel>: <feature>` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` |

For selected storage/cloud work, follow [storage contracts](../references/h5-reliability.md#identity-storage-and-cloud) / [存储合同](../references/zh-CN/h5-reliability.md#身份本地存档与云) and the [TapTap read/budget contract](../references/taptap.md#cloud-read-compatibility-and-upload-budget) / [TapTap 读取与预算合同](../references/zh-CN/taptap.md#云档读取兼容与上传预算). Record the exercised sync/callback write/readback, absent/corrupt/unknown classification, optional-file independence, bounded read route, owner/token guards, semantic comparison versus strict selection snapshots, unknown pending recovery and diagnostic zero-call result. Keep local test counts attributed to their source build; they do not establish device acceptance or a historical root cause. / 记录实际验证的同步／回调写入与读回、缺失／损坏／未知分类、可选文件独立性、有界读取路径、归属／token 保护、语义比较与严格选择快照、未知 pending 恢复及诊断零调用结果。本地测试数量归于对应来源构建，不证明真机验收或历史根因。

Keep upload, main-package binding, review submission/state, approval, release schedule and publication separate, with receipt observation time. An immediate-after-approval schedule or dated `reviewing` receipt is not a current approval/publication query. / 上传、主包绑定、提审／审核状态、通过、发布计划、正式发布分列，附回执观察时间；通过后立即发布计划或历史 `reviewing` 回执不等于当前已通过／已发布查询。

For selected safe-area/layout work, use the [canonical contract](../references/h5-reliability.md#safe-areas-host-origins-and-capsule-placement) / [安全区合同](../references/zh-CN/h5-reliability.md#安全区宿主原点与胶囊布局) and record:

- Actual CSS viewport, relevant visual viewport/offsets and final app/header/control rectangles; host, device/platform and orientation. / 实际 CSS 视口、相关可视视口／偏移、最终应用／标题栏／控件矩形，以及宿主、设备／平台和方向。
- Native geometry present/missing/invalid, already-consumed insets, selected source and any bounded project fallback; identify fixture versus real measurements. / 原生几何有效／缺失／异常、已消耗边距、采用来源及有界项目兜底；区分替身与真实测量。
- Separate fixture, settled browser visual, native SDK, physical-device and Owner outcomes, with evidence paths. Unknown or denied cases stay pending; do not bypass a denied action. / 分列替身、稳定后的浏览器视觉、原生 SDK、物理真机及 Owner 结果与证据；未知或被拒的情况待验，不绕过拒绝。
- Local candidate version/hash and independently read-back uploaded version/artifact, testing, review and release states. A processed feedback or public-test report is not repair or formal-release acceptance. / 本地候选版本／哈希，与独立读回的上传版本／制品、测试、审核及发布状态；反馈已处理或进入公测不代表修复验收／正式发布。

For selected developer/Owner tools, follow [the Settings/debug-build contract](../references/h5-reliability.md#developer-and-owner-tools) / [设置与调试版合同](../references/zh-CN/h5-reliability.md#开发者与-owner-工具). Record the exact build/version, actual narrow viewport, Settings route, ordinary-screen obstruction/hit-area result, test-reward labeling/save isolation, pause/background/ad/mute restoration and production cheat/simulation exclusion. Keep instruction-only, project implementation and executed visual/device results distinct. / 记录确切构建／版本、实际窄屏视口、设置路径、普通页面遮挡／点击结果、测试奖励标识／存档隔离、暂停／后台／广告／静音恢复及生产版作弊／模拟入口排除；技能指令、项目实现和实际视觉／真机结果分开。

## Cloud queue and status acceptance / 云队列与状态验收

For selected cloud work, copy this **requirement matrix for later execution**, not as passed results. Apply the [queue/status contract](../references/h5-reliability.md#cloud-save-queue-and-truthful-status) / [队列与状态合同](../references/zh-CN/h5-reliability.md#云保存队列与真实状态). Exercise the actual queue, serializer, lifecycle/account gates and status rendering with controlled SDK/storage/clock faults; record host/device checks separately. / 已选云存档工作复制本表作为**后续执行要求**，不能直接记为通过；使用实际队列、序列化、生命周期／账号门及状态渲染，控制 SDK／存储／时钟故障，宿主／真机另记。

| Scenario / 场景 | Required observation / 必须观察 | Result + evidence / 结果与证据 |
| --- | --- | --- |
| Burst saves, continued activity / 连续保存与持续操作 | Latest state serialized at eligible dispatch; bounded coalescing cannot starve or bypass quota/reconciliation. / 执行时序列化最新状态；合并有界且不绕配额／对账。 | `not run / 未执行` |
| Failed in-flight attempt, no newer save / 请求失败且无新保存 | Intent retained and bounded retry scheduled, or explicit reconciliation/recovery block; no silent consumption. Include provider/serialization and early-rejection faults. / 保留意图并安排有界重试，或明确阻止并待对账／恢复；覆盖 provider／序列化及提前拒绝。 | `not run / 未执行` |
| Failed attempt with newer intent; old success with newer intent / 失败期间有新意图；旧请求成功时有新意图 | Newest work survives failure; old success cannot clear or label newer progress synced. / 失败不覆盖最新待写；旧成功不清掉或误报新进度已同步。 | `not run / 未执行` |
| Hard quota, retry exhaustion, first create, manual/critical and competing controllers / 硬配额、重试耗尽、首次创建、手动／关键及控制器竞争 | Every actual write obeys budget; honest deferral and safe action, no force bypass. Cross-device acceptance remains separate. / 每次实际写入守预算；真实延期及安全动作，不靠 force 绕过；跨设备另验。 | `not run / 未执行` |
| Background, switch, teardown, revalidation failure and late callbacks / 后台、切号、销毁、重验证失败及迟到回调 | Progress/intent retained in its real durability tier; no old-account provider or callback writes into the new account, including memory/cloud-only paths. / 按实际持久层保留进度／意图；仅内存／仅云端路径也不能用旧账号任务写新账号。 | `not run / 未执行` |
| Unknown write, late remote success, recovery / 未知写入、远端迟到成功与恢复 | Reconcile owner/receipt/payload before retry; preserve unknown legacy diagnostic pending, lineage, strict snapshots and reward once-only protections. / 重试前核对归属／回执／载荷；保留旧诊断未知 pending、谱系、严格快照及奖励防重复保护。 | `not run / 未执行` |
| All durability/status combinations and both locales / 各持久化／状态组合及双语 | Local durable/failed, memory-only, cloud-only, unsupported, pending/queued, checking/downloading/verified, uploading/acknowledged/readback, consistent, error/unknown reflect actual evidence and generation. / 各状态文案对应实际证据与代次，不把下载核验报成最新进度已上传。 | `not run / 未执行` |
| Long wait and recovery UI / 长等待与恢复界面 | Gameplay remains usable; no save-toast spam/endless spinner/exact countdown promise; retain correctly qualified success time and a working safe action. / 游玩不阻塞，不刷保存提示／无限转圈／承诺准确倒计时；保留含义正确的成功时间及可用安全入口。 | `not run / 未执行` |

For each executed row, record build/hash, durability tier, local/intent/in-flight/confirmed generations, actual call ordering/times, rendered label/action and bounded evidence path. Distinguish source review, synthetic execution, real host/device and Owner acceptance; delay arithmetic or source-string assertions alone do not close a row. / 每个已执行行记录构建／哈希、持久层、本地／意图／请求／已确认代次、实际调用顺序／时间、所见文案／动作及有界证据路径。源码审查、替身执行、真实宿主／真机和 Owner 验收分开；仅算式或字符串断言不能关闭验收项。
