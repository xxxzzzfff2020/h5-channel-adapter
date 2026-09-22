---
name: h5-channel-adapter
description: "Prepare an existing TapTap H5 game for multiple publishing platforms: independent source projects, listing assets, guided configuration and game packages. 将已有 TapTap H5 项目适配到多个发布平台，生成独立工程、上架物料与渠道包；支持增量更新和平台扩展。"
---

# H5 Channel Adapter / H5 多平台适配

Turn an existing H5 project and its TapTap materials into independent platform projects and listing kits. Guide platform selection, finish credential-independent work first, then collect missing configuration and build each platform's package. Apply this Skill to adaptation, channel updates and platform-profile maintenance.

从现有 H5 工程及 TapTap 物料生成各平台独立工程和上架资料。先引导选平台、完成不依赖凭证的工作，再补齐配置并分别出包；适用于首次适配、渠道更新和平台扩展。

## Start / 开始

Use the user's language and read one workflow, then only the selected platform references. If targets are absent, offer the platform list through available question tools or short text choices. Use explicit selections; do not silently add platforms or infer answers from defaults/timeouts. For “all platforms”, state the current five-platform list and apply each profile's requirements.

按用户语言读取一份流程，再按选定平台读取说明。未指定平台时通过可用提问工具或文字选项引导；沿用明确选择，不把默认选中或超时当回答。用户选择“全部平台”时列明当前五个平台，并分别处理其接入条件。

- **English:** [Workflow](references/workflow.md), [guided setup](references/guided-flow.md), [listing materials](references/materials.md).
- **简体中文：**[适配流程](references/zh-CN/workflow.md)、[引导配置](references/zh-CN/guided-flow.md)、[物料制作](references/zh-CN/materials.md)。

## Platforms / 平台入口

| Platform / 平台 | English | 简体中文 |
| --- | --- | --- |
| 233 Leyuan H5 / 233 乐园 H5 | [233](references/233.md) | [233](references/zh-CN/233.md) |
| 4399 H5 minigames / 4399 H5 小游戏 | [4399](references/4399.md) | [4399](references/zh-CN/4399.md) |
| Xiaohongshu MiniTool / 小红书小工具 | [MiniTool](references/xiaohongshu.md) | [小红书](references/zh-CN/xiaohongshu.md) |
| Bilibili TOY / B 站 TOY | [TOY](references/bilibili-toy.md) | [TOY](references/zh-CN/bilibili-toy.md) |
| NetEase Xingxia / 网易星匣 | [Xingxia](references/xingxia.md) | [星匣](references/zh-CN/xingxia.md) |

Check current requirements and project compatibility before committing to a feature. A platform profile supplies integration guidance; it does not guarantee a game's platform acceptance. Use the official Skill/CLI/MCP independently and check updates as described in [upstream tools](references/upstream-tools.md) / [官方工具](references/zh-CN/upstream-tools.md).

先核对当前规则与项目条件，再确定功能接入方式。平台说明用于指导实现，不能替代具体项目的平台测试。官方 Skill/CLI/MCP 独立使用并跟随更新。

## Delivery / 交付

1. **Prepare before asking for IDs.** Inventory source and local materials, preserve one source baseline, create independent channel projects and complete work that does not require missing configuration. Preserve originals, saves and previous packages. / **先准备，再补 ID**：盘点源码和本地物料，固定来源，创建独立工程；保护原工程、存档与旧包。
2. **Guide the next step per platform.** Provide ready-to-use listing copy, material paths, package status and the actual missing fields. Continue unblocked platforms. Keep server secrets out of frontend code and reports. / 按平台展示建项资料、文件、包状态与缺失字段，其他平台继续；服务端密钥不进前端或报告。
3. **Produce complete listing kits.** Follow [field mappings](references/listing-fields.md) / [字段映射](references/zh-CN/listing-fields.md). Separate game packages from listing kits. For 233/4399, combine promotional content and real gameplay in the delivered video. / 按平台生成文案与物料，游戏包和物料包分开；233/4399 视频包含宣传内容与真实操作。
4. **Ask before reducing content.** Check original and final package sizes using [package budgets](references/package-budget.md) / [包体流程](references/zh-CN/package-budget.md). On overflow, obtain a specific plan; an approved media removal must also update menus, playback and save compatibility. / 初始包和最终包均测大小；超限先选方案，删媒体时同步菜单、播放逻辑与旧档兼容。
5. **Fit the environment.** Follow [macOS/Windows guidance](references/portability.md) / [系统环境](references/zh-CN/portability.md). Default Android target: Xiaomi 8 / Android 10, unless overridden. Check host-engine constraints using [compatibility guidance](references/compatibility.md) / [兼容说明](references/zh-CN/compatibility.md). / 按系统执行，安卓默认小米 8、Android 10，并单独核对宿主内核。
6. **Report the actual result.** Distinguish local preparation, SDK/device testing and platform upload/review/release. Never fabricate rewarded-ad completion or borrow another game's IDs. Follow the user's scope for external actions. / 区分本地准备、SDK/真机测试与上传/审核/发布；不伪造广告完成、不借用其他游戏 ID；外部操作遵循用户范围。

To add or update a platform, read [extension guidance](references/extending.md) / [扩展说明](references/zh-CN/extending.md). Repository contributions start with [CONTRIBUTING](CONTRIBUTING.md) / [贡献指南](CONTRIBUTING.zh-CN.md). Keep reusable instructions independent of private project history.
