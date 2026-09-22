# H5 多平台适配 Skill

**让 AI Agent 从一个 H5 游戏项目，完成多个平台的适配与上架准备。**

[English](README.md) · [开始使用](#开始使用) · [参与贡献](CONTRIBUTING.zh-CN.md) · [更新记录](CHANGELOG.md)

将已有 TapTap H5 项目的源码、图片、视频和上架文案放在项目目录中，告诉 Agent 项目位置并选择目标平台。Skill 会引导它完成代码适配、物料制作和出包，并在需要时向你收集平台配置。

## 能帮你做什么

- **生成独立平台工程**：每个平台有自己的源码、运行资源和构建方式，保留原始项目。
- **制作上架物料**：读取现有素材，按平台要求生成图标、封面、截图、宣传视频和文案。
- **引导平台配置**：告诉你哪些包已准备好、哪些平台需要建应用，以及缺少哪些 AppID 或能力开通信息。
- **处理包体超限**：先说明大小和可选方案，由你决定是否压缩或删减音乐、视频等功能。
- **持续同步更新**：主项目迭代后，更新已有渠道工程及受影响的物料。

Skill 为 Agent 提供流程、平台接入说明和辅助工具，由 Agent 结合当前项目执行修改。具体可交付的能力取决于平台支持、账号权限和项目兼容情况。

## 平台范围

| 平台 | 适配内容 |
| --- | --- |
| 233 乐园 H5 | H5 打包、激励广告接入、上架物料 |
| 4399 H5 小游戏 | H5 打包、AppID 配置、广告、存档及可选排行榜 |
| 小红书小工具 | 离线 H5 适配、权限配置、小体积 ZIP 与上架字段 |
| B 站 TOY | 静态 H5 打包、TOY SDK 接入、封面与图标 |
| 网易星匣 | 已有游戏导入、SDK 接入、图文与宣传媒体 |

可以选择一个或多个平台。Agent 会先根据当前平台要求判断项目适配条件；广告、云存档、排行榜等能力按平台支持与应用实际开通情况接入。

## 开始使用

### 1. 安装 Skill

在 Codex 中，将仓库克隆到 skills 目录。仓库目前私有，你的 GitHub 账号需要先获得访问权限。

macOS — zsh/bash：

```sh
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git "${CODEX_HOME:-$HOME/.codex}/skills/h5-channel-adapter"
```

Windows — PowerShell：

```powershell
$skillBase = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git (Join-Path $skillBase 'skills/h5-channel-adapter')
```

其他支持 `SKILL.md` 的 Agent，按其安装方式将本仓库作为一个 Skill 安装；中英文共用一次安装。已有同名目录时更新现有安装，避免覆盖。Git 工作区干净时，可在 Skill 目录运行 `git pull --ff-only` 更新。

### 2. 准备项目

把游戏源码、构建说明、TapTap 上架文案和已有图片、视频放在项目主目录中。可以保留原有子目录，无需提前整理成固定格式；有当前游戏 ZIP 也一起保留。

Agent 会先搜索已有资源，再询问缺失项。账号凭证放在本地安全配置中，与游戏源码和物料分开。

### 3. 告诉 Agent 你要做什么

让 Skill 引导选择平台：

```text
使用 $h5-channel-adapter，项目在 <项目路径>。
请先引导我选择目标平台，再生成独立工程与上架物料，
并告诉我还需要补充哪些平台建项信息。
```

也可以直接指定：

```text
使用 $h5-channel-adapter，把 <项目路径> 适配到 4399 和 B 站 TOY。
TapTap 文案、截图和宣传视频都在项目目录里。
```

## 使用流程

**选择平台 → 准备工程和物料 → 补充缺失配置 → 生成平台包。**

第一轮先完成不依赖账号凭证的工作，给出各平台的工程、物料位置、可用包和下一步。你补充必要的 AppID、广告或存档开通状态后，Agent 继续对应平台的出包；一个平台等待信息，其他平台可以继续。

包体超限时，Agent 会列出实际大小和主要占用，再提供适用方案：保留功能优化、去掉背景音乐但保留音效、移除可选游戏内视频，或暂缓该平台。选定删减后，会同步处理菜单、设置和播放逻辑。上架宣传视频与游戏内视频分别处理。

## 运行环境与官方工具

同一个 Skill 可用于 **macOS 和 Windows**。辅助脚本需要 Python 3.9+，媒体检查和视频制作使用 FFmpeg；Agent 会按当前系统查找工具。安卓默认目标为小米 8 / Android 10，可按项目调整。

平台官方 Skill、CLI、MCP 从官方渠道获取，并在使用时检查相关更新；本仓库维护各平台共用的适配流程。详见[系统环境](references/zh-CN/portability.md)与[官方工具接入](references/zh-CN/upstream-tools.md)。

## 参与贡献

欢迎补充新平台、更新上架要求、改进适配流程、修复 Windows/macOS 兼容问题，或完善文档。可以阅读[贡献指南](CONTRIBUTING.zh-CN.md)，也可以先[提交 Issue](https://github.com/xxxzzzfff2020/h5-channel-adapter/issues/new/choose)。

仓库采用标准 Skill 结构：[Agent 执行入口](SKILL.md)、存放平台说明的 `references/`、共用规则与示例的 `assets/`，以及辅助工具 `scripts/`。中英文文档同步维护。

目前仍为私有仓库，正在为后续公开发布整理；正式公开前会确定开源许可证。
