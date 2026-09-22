# H5 Channel Adapter

**An AI Agent Skill for taking one H5 game to multiple publishing platforms.**

[简体中文](README.zh-CN.md) · [Get started](#get-started) · [Contribute](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

Start with your existing TapTap H5 project, artwork and listing copy. Tell your agent where the project lives and choose your target platforms. The Skill guides it through code adaptation, listing-material production and packaging, then asks for platform configuration when it is needed.

## What you get

- **Independent platform projects** — source code, runtime assets and build instructions for each selected platform, while preserving the original project.
- **Listing kits** — platform-sized icons, covers, screenshots, promotional videos and copy, using the source material in your project folder.
- **Guided setup** — a clear list of platforms ready for upload and those waiting for an AppID, account setup or capability access.
- **Package-size choices** — if a package exceeds a platform limit, see the options before music, video or functionality is removed.
- **Repeatable updates** — bring later source changes into existing channel projects and update the affected materials.

The Skill gives your agent the workflow, platform references and helper tools. The agent performs project-specific edits using the tools available in your environment. Platform accounts, permissions and host compatibility determine which features can be delivered.

## Platforms

| Platform | Adaptation scope |
| --- | --- |
| 233 Leyuan H5 | H5 packaging, rewarded-ad integration and listing materials |
| 4399 H5 minigames | H5 packaging, AppID setup, ads, saves and optional leaderboards |
| Xiaohongshu MiniTool | Offline H5 adaptation, permissions, compact ZIP and listing fields |
| Bilibili TOY | Static H5 packaging, TOY SDK integration, covers and icons |
| NetEase Xingxia | Existing-game import, SDK integration and listing media |

Choose one platform or several. The agent checks the selected platform's current requirements against your project before adapting it. Features such as ads, saves and rankings depend on the platform and your application's enabled capabilities.

## Get started

### 1. Install the Skill

For Codex, clone this repository into your skills directory. The repository is currently private; your GitHub account needs access.

macOS — zsh/bash:

```sh
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git "${CODEX_HOME:-$HOME/.codex}/skills/h5-channel-adapter"
```

Windows — PowerShell:

```powershell
$skillBase = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git (Join-Path $skillBase 'skills/h5-channel-adapter')
```

For other agents that support `SKILL.md`, install this repository as one Skill using that agent's installation method. English and Chinese share the same installation. If the destination already exists, update it instead of cloning over it. Clean Git installations can update with `git pull --ff-only` from the Skill directory.

### 2. Prepare your project

Keep the game source, build instructions, TapTap listing copy and available artwork/video in the main project folder. Existing subfolders are fine; no mandatory input layout is required. Include a current game ZIP if available.

The agent searches the folder first and asks only for missing material. Put account credentials in your secure local configuration, separate from game source and listing assets.

### 3. Ask your agent

Let the Skill guide platform selection:

```text
Use $h5-channel-adapter for the game at <project path>.
Guide me through choosing platforms, then prepare the independent projects
and listing materials. Tell me what platform setup information is still needed.
```

Or name the platforms directly:

```text
Use $h5-channel-adapter to adapt <project path> for 4399 and Bilibili TOY.
The TapTap copy, screenshots and promotional footage are in the project folder.
```

## How it works

**Choose platforms → prepare projects and materials → fill missing configuration → build platform packages.**

The first round completes work that does not depend on account credentials. You receive each platform's project and material locations, available packages and next steps. After you provide the necessary AppID or capability status, the agent continues that platform's build. One platform waiting for information does not hold up the others.

If a package is too large, the agent reports its size and the main contributors, then offers relevant choices: optimize while keeping features, remove background music while retaining sound effects, remove optional in-game video, or defer that platform. An approved removal also updates menus, settings and playback logic. Listing videos remain separate from in-game media.

## Environment and official tools

Use the same Skill on **macOS or Windows**. The helpers require Python 3.9+; media inspection and video production use FFmpeg. The agent locates these tools for your operating system. The default Android target is Xiaomi 8 / Android 10 and can be changed for your project.

Platform-owned Skills, CLI tools and MCP integrations are used from their official sources. The agent checks for relevant updates when they are needed; this repository maintains the shared adaptation workflow. See [environment setup](references/portability.md) and [official-tool integration](references/upstream-tools.md).

## Contribute

Help add a platform, update listing requirements, improve adaptation guidance, fix Windows/macOS compatibility, or clarify the documentation. Start with the [contribution guide](CONTRIBUTING.md) or [open an issue](https://github.com/xxxzzzfff2020/h5-channel-adapter/issues/new/choose).

The repository uses a standard Skill layout: [agent instructions](SKILL.md), `references/` for platform guidance, `assets/` for shared rules and examples, and `scripts/` for helpers. English and Chinese documentation are maintained together.

The repository remains private during preparation for public release. An open-source license will be selected before that release.
