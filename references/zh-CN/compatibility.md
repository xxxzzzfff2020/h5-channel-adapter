# 最低安卓目标与验收

用户 2026-09-22 确定非 TapTap 平台最低目标 **小米 8、Android 10**，这是目标，不是设备已验收。

安卓版本不能唯一确定 QQ/X5、UC、WebView 或渠道 App 内核。能获取时记录宿主/内核版本；没有则先做保守构建和能力检测，不反复询问阻塞第一轮。案例 B历史 4399 使用 Chrome 57/ES2015，233 使用 Chromium 70/ES2018，是各自构建目标，不能宣称小米 8 就是这些版本；新宿主按依据选取并记录暂定目标。

## 兼容检查

- 语法：包括手工拼接、启动保护在内的全部产物脚本降级并解析，不只处理主 bundle。外部官方 SDK 也检查目标语法，不擅自改写 SDK。
- API：按真实使用补齐/降级 globalThis、Object.fromEntries/hasOwn、Array.at/flatMap、String.replaceAll、queueMicrotask、CSS.escape、ResizeObserver、replaceChildren 等，不无差别注入。语法 target 不提供 API polyfill，见 [esbuild](https://esbuild.github.io/api/#target)。
- CSS：按使用处理 color-mix、dvh/svh、safe-area、flex gap、aspect-ratio、inset/逻辑属性、clamp、:has()；保留基础声明，渐进增强。cssTarget 不证明布局通过。
- 输入：PointerEvent 缺失时局部触摸回退；松手/取消/后台停止移动，列表仍能滚动。测短屏、旋转、工具栏伸缩、iframe 高度变化、弹层、底栏及大字。
- 音频：首次手势、广告/后台恢复、静音、音量、切曲；码率不是解码内存或中断原因的直接证据。

color-mix 独立统计当前源码的**声明数**，与注入数一致、跳过为 0；一声明多个函数不作多声明。源码为 0 就记录 0，不套用旧案例 67 条。转换需处理单行压缩、media prelude 冒号、字符串/注释、末声明无分号扫描到 `}`、冒号前空格，不能改字符串文字。动态/内联 CSS 覆盖另查。变量提取的最后定义可能是末阶段主题色，须核对作用域/基座主题，不能全局覆盖动态主题。

## 验证与证据

广告覆盖完成、取消、失败/无填充、超时、重复和迟到回调，写盘失败重试与重启后单次持久化。存档覆盖刷新、坏主档、不可写、旧档、多窗口与渠道隔离。新档实际完成关键玩法一段，旧档保留解锁/教学；只看弹窗不足验收。

核验正式 ZIP 内容/CRC/根入口/相对资源/禁止标记/哈希，使用该入口烟测。现代 Chromium 改 UA/视口、移除 API/CSS 的故障注入不是真旧内核或小米 8；mock 不能证明真广告。

“仍像旧版”先比线上 HTML/ZIP 版本哈希，再隔离新档与旧档对照引导旗标，最后调查手机缓存。案例 B同一 0.6.6 包因旧档已看教学保留旧开始页，不能先清玩家档或猜测改包。

逐项标 passed_local、pending_platform、pending_device、blocked_missing_input、not_applicable 并附依据。上传、审核、发布分别取后台回执，不互相替代。
