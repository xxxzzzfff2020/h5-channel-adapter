# Changelog / 更新记录

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
