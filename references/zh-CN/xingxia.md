# 网易星匣

状态：2026-09-22 已核对官方文档，尚无本 Skill 的首个项目、宿主/真机和发布验收。调用官方工具前读 [上游工具](upstream-tools.md)，跟随官方 Skill/CLI，不维护改造副本。

## 初轮适配

可上传现成 HTML/JS/ZIP。轨道 A 文档限制单个上传文件 ≤50 MB；ZIP 根或恰好一级目录含 index.html。多文件游戏优先相对资源 ZIP；单文件需内联资源或允许的绝对 CDN，不能依赖未上传的相对文件。

SDK 仅用官方 CDN IIFE：`https://gz-vchar-pub.nosdn.127.net/star-letter/game-sdk/v2/sdk.iife.js`。`await window.GameSDK.init()` 的 gameId 由宿主注入，运行时读 `sdk.context.gameId`，不在 init 写死。不手拼 parent 协议，生产包不带 mock；调用捕获异常并使用官方错误类型守卫。

已读能力有 storage、oss、ai、exchange、日志和诊断；没有在该 API 索引中核实激励广告或排行榜。不能把广告奖励擅自换成收费兑换/AI；可关闭不可用的可选入口，涉及核心成长时询问产品取舍。

存档采用对象参数 `sdk.storage.get({key})` / `sdk.storage.set({key,value})`。接入页旧例仍有位置参数，与详细存档文档冲突，执行时以当前能力类型/接口为准。私有存档用 user scope，绝不能写共享 game scope。单值为序列化 UTF-8 JSON ≤256 KB，读写需登录；处理本地降级、体积错误、版本冲突和可见的失败重试，不无限分片。宿主管理全屏/方向，游戏只适配 iframe 尺寸，不自行 requestFullscreen 或锁屏。

## 物料与下一步

封面 JPG/PNG/WebP ≤5 MB，推荐 800×450 / 16:9，推荐不等于硬限制。名称 2–30 字符并按最新表单排除禁用符号；简介 ≤300；玩法分类 1–2 个；标签 1–5 个。选填关于 ≤1000 个 Markdown 源码字符、操作说明 ≤500。上述页面未确立截图/视频配额，不能套用 233。

本地包不需要先收 AppID。到平台预览/发布再按授权引导创作者登录、选择或建立目标作品。常规 `star-letter login` 设备登录无需用户手工建 API Key；发布管理的作品 ID 与运行时注入的 gameId 区分。AI 场景/兑换商品仅按需求另行配置。

`star-letter dev` 在平台宿主内按能力选模拟/真实；真实存档使用预览分区，AI/兑换真实档可能计费，不作为普通兼容验证自动启用。生产排除 `star-letter.mock.*`。草稿上传仍是外部写入，publish 不是本地构建。

官方来源：[上传](https://game.virtualoverapp.com/creator/center?section=guide&cat=create&doc=track-a-upload)、[字段](https://game.virtualoverapp.com/creator/center?section=guide&cat=rules&doc=fields)、[SDK](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=index)、[接入](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=embedding)、[存档](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=storage)、[本地测试](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=local-testing)、[官方 Skill](https://game.virtualoverapp.com/creator/center?section=guide&cat=create&doc=agent-skill)。
