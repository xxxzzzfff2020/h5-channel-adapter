# H5 Channel Adapter

[简体中文](README.zh-CN.md) · [Skill entry](SKILL.md) · [Changes](CHANGELOG.md)

A bilingual agent Skill for adapting an existing TapTap H5 game into independent channel source projects, runtime assets, listing kits and game ZIPs.

**Choose platforms → complete local preparation → identify missing configuration → bind and build → validate per platform.** Prepare what can be done without credentials first. A blocked channel does not stop the others.

This is an agent workflow with resource-inventory and material-validation helpers, not a one-command universal game converter. Source-specific coding and actual platform/device checks are still required.

## Platform status

| Platform | Current evidence |
| --- | --- |
| 233 Leyuan H5 | Experience from two game adaptations; material checker included |
| 4399 H5 minigames | Experience from two game adaptations; material checker included |
| NetEase Xingxia | Official docs reviewed; first port and real-host acceptance pending |
| Xiaohongshu MiniTool | Offline H5 constraints documented; current official rewrite command and first port required |
| Bilibili TOY | Official SDK/Skill reviewed; first port and real-host acceptance pending |

Default “all supported” includes **233 + 4399**. Other profiles are explicitly selected documentation-stage targets. Reviews are dated **2026-09-22**; recheck official rules before delivery.

## Install

The repository root is a standard Skill directory: `SKILL.md` with YAML name/description, `agents/`, `references/`, `scripts/` and `assets/`. One install serves both languages. Compatible agents can read the same Skill; Codex-specific UI questions fall back to ordinary text choices when unavailable.

The repository is private. The owner must grant repository access before friends can clone it. Authenticate Git/GitHub locally; never put a token in the clone URL or Skill. For a fresh Codex installation, clone into an **absent** destination:

macOS (zsh/bash):

```sh
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git "${CODEX_HOME:-$HOME/.codex}/skills/h5-channel-adapter"
```

Windows (PowerShell):

```powershell
$skillBase = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
git clone https://github.com/xxxzzzfff2020/h5-channel-adapter.git (Join-Path $skillBase 'skills/h5-channel-adapter')
```

If a Skill already exists there, inspect it before updating; do not overwrite custom work. For another agent, use that agent's documented Skill directory or installer and this repository URL. Platform toolkits are separate, optional dependencies selected for the task; this install does not install them or rewrite global agent settings.

## Use

```text
Use $h5-channel-adapter for the TapTap H5 game at <project path>.
Guide me through target-platform selection. First prepare independent source
projects and all listing assets, then tell me exactly which platform setup
information is still needed and continue packaging when I provide it.
```

```text
使用 $h5-channel-adapter，项目在 <项目路径>。
请先引导我选择目标平台，完成独立源码与全套上架物料，
再提示缺少的建项信息；收到信息后继续出包。
```

Inspect existing source, assets and permissions before asking questions. UI tools may provide single-choice cards; multi-platform selection can use grouped yes/no questions or one text list. No native multi-select support is assumed.

The default non-TapTap Android target is **Xiaomi 8 / Android 10**, configurable by the project owner. Actual host-engine requirements and device evidence remain separate.

## macOS and Windows

All Python helpers use standard-library Python **3.9+**. Locate an existing interpreter and `ffprobe` (FFmpeg distribution) on PATH; video generation/tests also use `ffmpeg`. The Windows launcher may be `py -3` instead of `python`. See [portable commands](references/portability.md).

Helpers inventory resources and validate known fields for all five platform manifests; they do not modify original game files. Reports refuse overwrite. Use explicit paths and quoted arguments, including paths with spaces/non-ASCII characters.

```sh
python3 scripts/inventory_project.py <game-root> --output <new-inventory.json>
python3 scripts/verify_materials.py <material-manifest.json> --report <new-report.json>
```

On PowerShell use the verified `py -3` or `python` in place of `python3`, and quote actual paths. Start manifests from [the example](assets/material-manifest.example.json); the example placeholders are not deliverable assets. Technical pass does not certify visuals, real ads, devices or release.

## Package budgets

Check the actual baseline and final game artifacts with `scripts/check_package_budget.py`. Known snapshots are Xiaohongshu 10 MB, Bilibili 140 MB, and Xingxia Track A 50 MB; unknown 233/4399 limits remain explicit. An over-limit report triggers a measured options question. No music/video removal occurs without the selected plan; an approved removal also updates settings, menus, playback and save compatibility. Listing promotional videos remain separate. See [budget workflow](references/package-budget.md) and [listing fields/examples](references/listing-fields.md).

## Follow official tools

Read the current official Skill, CLI help or MCP schema when performing platform operations. **Do not fork/vendor the official platform Skill into this one.** Compare installed vs upstream versions, notify about relevant updates, and use the official update mechanism within user authorization. See [update policy](references/upstream-tools.md) and [source registry](assets/platform-sources.json).

This is an on-use update check, not a background monitor. No game upload, paid API call or global settings change is implied by installing this Skill.

## Maintain and update

The repository contains the maintained source. Check `git status` before changes; keep local customizations safe. Clean installations can update with `git pull --ff-only` from their Skill directory. Conflicts or local edits need review, not force-reset.

Update English and Chinese references together, retain one machine rule file, and record changed behavior/evidence in `CHANGELOG.md`. Keep new profiles at documentation stage until tested with a representative project. Never commit game source/media, IDs, credentials, temporary preview URLs or private task history.

Run the portable synthetic helper checks from the repository root:

```sh
python3 tests/smoke.py
```

PowerShell: `py -3 tests/smoke.py` (or the verified `python`). Tests require `ffmpeg` and `ffprobe`; they create isolated synthetic media, not game assets. The [GitHub Actions template](ci/validate.github.yml) runs the same helper checks on macOS and Windows when enabled as `.github/workflows/validate.yml`. Activation requires repository workflow permission; a template is not a passed Windows run. Platform/device acceptance is tracked separately.

Distribution remains private; no public release or open-source license has been selected.
