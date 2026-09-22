# 小红书小工具

状态：离线 H5 条件适配；2026-09-22 核对文档，页面更新日 2026-09-10，尚无沙盒项目/真机验收。这里是“小工具容器”，不假设它就是通用小游戏 SDK。

适配前必须取得**上传页第一步当前完整改写命令**，读取其指向的官方 Skill。能力页明确不能替代该命令。不复用旧命令、不保存改造后的官方 Skill；见 [上游工具](upstream-tools.md)。

## 必需改动

- 纯 HTML/CSS/JS，全部离线。禁网络请求、外链资源/字体/脚本、WebSocket/WebRTC、各类 worker、WASM、eval/new Function、iframe 和外部跳转。
- JS 必须是包内外置 `.js`；禁内联 script、onclick 等事件属性、javascript URL 和 data/blob 脚本。允许内联/本地 CSS。依赖全部转为兼容的本地资源。
- 宿主注入 `window.xhs.miniTool`，不加载别的平台 CDN SDK。支持 Canvas2D 和纯 WebGL 渲染，但仍受上述限制。
- 文档包扩展名白名单为 html/css/js/png/jpg/jpeg/gif/webp/svg/woff/woff2/json，且仅一个 HTML 入口。虽提到音视频标签，白名单未列 mp3/ogg/mp4；BGM/媒体打包必须核对当前官方检查器，不能假定任意音频文件可上传。
- JS/CSS 基线为 Android 8.1 出厂 Chrome/WebView 61（JS ES2017）；文档 iOS 最低 18.4。我们的设备目标仍是小米 8/Android 10，但产物另满足更严格内核限制。

## 存档和能力取舍

客户端 ≥9.46.0 优先使用原生存储，检查 buildVersion 与函数存在。单 key 1 MB、总计 10 MB；使用当前官方异步 set/get/info/remove/clear 和一致的加密选项。localStorage/sessionStorage/IndexedDB/cookie 仅作不可靠降级；明确处理不可用、写盘失败和迁移。文件选择仅图片/视频，文本存档导入需另设计。

公开能力含发笔记、存图片、临时文件、启动参数与存储；该清单未提供激励广告或排行榜。不能模拟广告成功、擅自免费发奖或宣传云存档。涉及核心成长/商业模式时需要产品取舍；普通离线玩法可独立准备。

此页没有明确上架图片尺寸、包大小、AppID/Secret 要求。发笔记字数/媒体数量是**游戏内笔记发布**规则，不是上架物料。后续索取当前改写命令和真实上传表单，不能统一索要凭证。

来源：[官方容器能力](https://miniapp-sandbox.xiaohongshu.com/minitool/doc)。首个项目需读取当时上传页 Skill 并运行其检查。
