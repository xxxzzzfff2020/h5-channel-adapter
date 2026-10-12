# 小红书小工具

用于小红书小工具离线 H5 容器。适配前核对当前容器能力和上传页指引，不套用其他小游戏产品的 SDK。

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

2026-09-22用户上传表单已确认：名称≤14、简介≤14，图标PNG/JPG/JPEG≤5 MB且推荐1:1，仅ZIP且≤10 MB，必填版本、场景标签、所需权限。精确图标像素/版本号格式未给。仅选择实际用到的相册/摄像头/麦克风/本地存储能力，按官方流程映射；本片段没有上架视频或AppID/Secret要求。发笔记规则仍与上架分开，当前改写命令仍需取得。见[字段映射](listing-fields.md)与[包体超限流程](package-budget.md)。

来源：[官方容器能力](https://miniapp-sandbox.xiaohongshu.com/minitool/doc)。每次适配按当前上传页 Skill 执行。

## 原生启动与恢复

按[原生存储启动说明](native-storage-boot.md)处理 key 清单优先、严格限定的空标记容忍、原子可选迁移、未改变状态启动零写、单次预期 API 写、读回及玩家选择的零持久写临时会话。当前在线合同回调模式返回 undefined；兼容请求 handle 和 mock 哨兵不能冒充 SDK 保证。旧包真实 iOS 失败、隔离测试及最新候选手机待验分开记录。

## 音乐与官方资源审查

2026-10-13 读取转交的[官方构建器链接](https://fe-static.xhscdn.com/minitool/20260923133933/minitool-zip-builder-1.7.0.skill)：压缩包清单版本为 1.7.0，内部 SKILL.md 元数据为 1.6.0。记录 URL／哈希与两处实际元数据，读取 SKILL.md 和相应 reference，不凭文件名猜版本；执行时取得当前上传页口令，不复制修改官方包。

本次官方白名单仍未包含 MP3 等音频扩展名。把已选原曲表示为合法、有界的包内 JS 字节并用 WebAudio 解码，是需明确内容选择及资源审查的项目候选，不是普遍获准的绕过方式。不将二进制伪装成白名单后缀，不用外部／data／blob 音视频 URL。所读官方预算规定单条 Base64 解码后至多 1 MiB；超过 100 KiB 须记录审查并优先使用允许的独立资源，白名单冲突须解释，不能用本地审计替代平台许可。预检提示长引号 Base64 类字面量，分段／动态拼接仍需人工读源。

保留原曲来源与所选时长／编码，音量／静音、手势解锁、循环、后台／前台、迟到异步解码／播放取消和音频失败不阻塞。记录原始／编码／解码字节及启动／内存实测或未实测。执行实际官方目录与最终 ZIP 审计，加包体及预检；静态审计／解码与模拟器、Android／iOS 试听及平台审核分别记录，缺少手机或试听证据保持待验。
