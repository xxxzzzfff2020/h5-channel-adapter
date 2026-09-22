# B 站 TOY

状态：2026-09-22 已登录读取 SDK 与官方 Skill 文档，尚无本 Skill 的项目/上传/真机验证。先读 [上游工具](upstream-tools.md)，官方 `bilibili/toy` Skill 和 CLI 独立安装、跟随更新，不在这里复制改造。

## 本地包与能力

支持构建后的静态 H5。ZIP 根或唯一明确的一级目录含 index.html。页面在 `/toy/<slug>/` 下运行，资源必须相对路径，不用 `/assets/...`，不把框架源码当运行包。hash 路由和页内锚点可用，history 路由需对应真实 HTML。已有 slug 保持不变，不能为改地址擅自删除重建。

SDK 为 `https://s1.hdslb.com/bfs/seed/toy/app/sdk/toy-sdk.js`，全局 `window.toy`。先用 `toy.isSupport(...)` 检测，捕获 Promise 错误。已核实云存储和排行，未从当前列表核实激励广告；保留本地普通玩法，涉及广告成长再确认产品取舍。

云存储按登录用户+TOY 隔离：最多 128 key，字符串 value ≤1024 字节，key ≤128 字节，仅字母/数字/下划线/连字符，不能 `__` 开头。完整经营游戏存档可能放不下，先测 UTF-8 大小，保留本地恢复，再确定有界的精简方案，不能盲目分满所有 key 或承诺完整云同步。关键节点批量写、读后缓存；全 TOY 玩家共享调用额度，`http_error` /307044 需退避，官方未公开 QPS 数字。

排行 board 1–5，整数 -16777216～16777215，提交绝对分数，保留历史最高、固定降序。先核分数语义，不静默截断。是否上榜看 `getMyRank().ranked`，零/负分仍可能上榜。登录/用户确认/能力检测按接口要求。

容器接口仅 App 支持；先监听再 setContainerMode，以匹配的实际状态确认方向/沉浸生效，Promise 返回不代表成功。使用实际 viewport/safeArea。摄像头/麦克风是可选功能，不作为移植前提。

## 物料与发布

2026-09-22用户后台表单确认上传 ZIP/HTML，当前包体上限140 MB。封面/图标为独立 JPG/PNG/JPEG 字段：封面比例4:3，推荐1200×900；图标比例1:1，推荐500×500。本次表单把比例作为要求，像素尺寸仍是推荐。图片字节上限/名称字数未给，需名称与页面地址slug，本片段未给宣传视频字段。见[字段映射](listing-fields.md)与[包体超限流程](package-budget.md)。

未建立前端 AppID/Secret 要求。先完成本地，发布/更新阶段再创作者登录、确认不可变 slug 与目标 ID。构造命令前读取 `toy --help-json` /子命令 help，API 调用用 `--json`；版本/升级命令单独核对，不机械附加所有 flag。

上传前使用当前官方预检或其手工清单，区分错误与建议。已授权发布时，官方流程先上传生成预览，再提交审核；`--yes` 会提交，纯元数据更新可能直接提审。按当前用户授权与适用官方 Skill 的预览/提审流程执行，预览不等于发布，本地请求不触发上传。

来源：[SDK](https://www.bilibili.com/toy/publish/sdk)、[Skill 入口](https://www.bilibili.com/toy/publish/sdk/skill)、[官方 Skill](https://github.com/bilibili/toy/blob/main/skills/toy/SKILL.md)、[内容检查](https://github.com/bilibili/toy/blob/main/skills/toy/references/content-checklist.md)。本仓库不内置官方 Skill 副本。
