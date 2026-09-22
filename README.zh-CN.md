# H5 多平台适配 Skill

[English](README.md) · [标准 Skill 入口](SKILL.md) · [更新记录](CHANGELOG.md)

把已有 TapTap H5 游戏转换为各平台可独立维护的源码工程、运行资源、全套上架物料和渠道 ZIP。

**选择平台 → 先完成本地初转与物料 → 展示真实缺口 → 补配置出包 → 分层验证。** 不依赖凭证的工作先做完，一个平台等待信息不阻塞其他平台。

这是 Agent 工作流和辅助校验工具，不是一个命令转换所有游戏的编译器。仍需针对源项目改代码，并完成真实平台/设备验证。

## 当前平台范围

| 平台 | 当前证据 |
| --- | --- |
| 233 乐园 H5 | 两个游戏适配经验，包含物料校验规则 |
| 4399 H5 小游戏 | 两个游戏适配经验，包含物料校验规则 |
| 网易星匣 | 已读官方文档，待首个项目与真实宿主验证 |
| 小红书小工具 | 已整理离线约束，需当时的官方改写命令和首个项目验证 |
| B 站 TOY | 已读官方 SDK/Skill，待首个项目与真实宿主验证 |

未另列目标时，“全部已支持”默认 **233＋4399**。新增三平台需显式选择，不能把读过文档等同于适配验收。文档核对日 **2026-09-22**，实际交付需复核最新规则。

## 安装与分享

仓库根目录就是标准 Skill：包含 YAML name/description 的 `SKILL.md`、`agents/`、`references/`、`scripts/`、`assets/`。中英文共用一次安装。其他兼容 Agent 可读取同一入口；没有 Codex 提问工具时退回文字选项。

仓库目前私有，朋友需要先取得仓库访问权限，再使用自己已认证的 Git/GitHub 克隆；不要把 token 写进地址或 Skill。首次安装到**尚不存在**的目标目录：

macOS（zsh/bash）：

```sh
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git "${CODEX_HOME:-$HOME/.codex}/skills/h5-channel-adapter"
```

Windows（PowerShell）：

```powershell
$skillBase = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git (Join-Path $skillBase 'skills/h5-channel-adapter')
```

已有同名 Skill 时先检查，不覆盖旧定制。其他 Agent 按其官方 Skill 安装目录/安装器使用本仓库；不会同时安装平台工具或改写全局 AGENTS/CLAUDE。

## 使用

```text
使用 $h5-channel-adapter，项目在 <项目路径>。
请先引导我选择目标平台，完成独立源码与全套上架物料，
再提示缺少的建项信息；收到信息后继续出包。
```

Agent 先找本地已有资源，再问真实缺口。当前弹窗可能是单选卡片，多平台用分组“做/不做”或一次文字列举；不假称原生多选已实现。

非 TapTap 安卓默认最低目标为**小米 8、Android 10**，项目负责人可明确覆盖。宿主内核要求和真机结果另行记录。

## Mac / Windows 工具

三个 Python helper 需 **Python 3.9+**，只用标准库；媒体检测需 FFmpeg 的 `ffprobe`，视频制作/夹具测试还需 `ffmpeg` 在 PATH。优先使用已有环境。Windows 通常用 `py -3` 或核实过的 `python`，不是直接照抄所有 Mac 命令。见[跨系统说明](references/zh-CN/portability.md)。

工具只读盘点游戏、校验五个平台已知物料字段，不修改原游戏，且拒绝覆盖旧报告。路径含空格/中文时引用。manifest 使用[示例结构](assets/material-manifest.example.json)并填写真实路径/哈希；示例占位并非可交付内容。

## 包体超限处理

`scripts/check_package_budget.py` 检查初始和最终实际游戏包。当前小红书10 MB、B站140 MB、星匣轨道A50 MB；233/4399未知上限保持显式待核。超限先展示大小/占用/方案并引导选择，不擅自删音乐视频；获选方案需同步改设置、菜单、播放点与旧档兼容。上架宣传视频独立保留。见[包体流程](references/zh-CN/package-budget.md)与[字段/示例](references/zh-CN/listing-fields.md)。

## 官方能力更新

平台官方 Skill、CLI、MCP **独立使用、跟随上游，不下载改造成我们的副本**。每次执行对应平台时检查当前官方文档、版本和接口 schema；有更新提示影响，并在实际授权内按官方方式更新。详见[上游机制](references/zh-CN/upstream-tools.md)与[来源表](assets/platform-sources.json)。

这里是使用时核对，不是后台监控；安装本 Skill 不意味着上传游戏、启用收费接口或修改全局设置。

## 后续维护

本仓库是维护源。更新前检查 `git status`；工作区干净的安装可在 Skill 目录执行 `git pull --ff-only`。存在本地改动/冲突时先处理，不能 force reset 覆盖定制。

同步维护中英文、共用唯一机器规则表；变更记录在 CHANGELOG。新平台经过代表项目验证后再提升状态。不提交游戏源码/媒体、实例 ID、凭证、预览 token 或私有对话记录。

在仓库根运行合成夹具检查（需 ffmpeg/ffprobe）：

```sh
python3 tests/smoke.py
```

Windows PowerShell 使用 `py -3 tests/smoke.py` 或已核实的 `python`。[GitHub Actions 模板](ci/validate.github.yml)启用到 `.github/workflows/validate.yml` 后，会在 macOS/Windows 运行同一套 helper 检查。启用需仓库 workflow 权限；模板存在不代表 Windows 实测通过，更不代表真机、真实广告或发布通过。

当前仅私有分发，尚未选择公开发布与开源许可证。
