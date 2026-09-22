# Adaptation workflow

Prepare independent, rebuildable channel projects and complete listing materials from an existing TapTap H5 game. This is an agent workflow with validation helpers, not a universal source-to-source compiler.

## Scope and interaction

Identify the game root, authoritative TapTap source, selected channels, and whether the task is a first port, incremental update, documentation assessment or experience update. A discussion of the process is not permission to port a game. “All supported” means 233 and 4399 unless otherwise specified. Read only selected platform profiles.

Use [guided interaction](guided-flow.md) when targets or necessary fields are missing. While waiting for platform selection, inventory sources read-only. After selection, finish independent local work before asking for configuration. One channel waiting for an ID does not block another. Continue already-authorized uploads within their original scope; otherwise deliver local candidates and exact next inputs.

## Phase 1: credential-independent work

### Freeze the source and inventory assets

Read applicable instructions; inspect source version, Git branch/dirty files, active writers, existing channel directories and old packages. Without Git, capture file hashes. Use the confirmed product name, not a guessed folder name.

Search the game root and TapTap source for brand masters, icons, alternate aspect ratios, screenshots, promotional video, gameplay recordings, music, fonts, copy and licenses. Do not ask for files already present. Backups and timestamps do not establish authority.

```sh
python3 <skill-dir>/scripts/inventory_project.py <game-root> --output <evidence-dir>/inventory.json
```

Review relevant text, images and video frames; the helper cannot select the authoritative source. Freeze the same baseline for all channels, copying required source, runtime assets, lockfiles, build scripts and licenses. Never chain-copy from another changing channel. If source changes while copying, compare hashes and recopy affected files from one coherent baseline.

Before changing channel content, check the frozen artifact against selected [package budgets](package-budget.md). Over-limit platforms require an explicit reduction choice; continue other channels and independent assets while waiting. Recheck each actual final channel artifact.

### Create independent projects

Keep established folder names. A new layout can be:

```text
<game-root>/
  Taptap项目/                 # original source
  233项目/                   # complete channel source
    src/ assets/ build configuration and lockfiles
    上架物料/上传文件/        # final upload assets
    上架物料/制作记录/        # masters, recordings, edit provenance
    docs/渠道交付.md
    docs/SOURCE_BASELINE.json
    docs/待补充信息.md
    evidence/
    dist-233/ release/
  4399项目/                  # independent source and configuration
```

Equivalent localized names are fine. Deliver actual files, not empty folders or copy commands. Do not symlink mutable assets back to the source. Preserve the build stack: aliases for Vite, build-assembled adapters for plain JS/Python. Do not change stacks just to match an example.

Centralize SDK, capabilities, ads, saves, container behavior and checks. Preserve gameplay and reward values; do not add payments or leaderboards merely because a platform offers them. New channels need isolated save namespaces. Existing channels retain established keys, formats, versions, backups and reward receipts. Migration needs a known source, backup, validation and player choice; never silently import another channel's progress.

Missing IDs leave explicit empty configuration and block only dependent release checks. Still build preview, materials and compatibility changes. Never borrow example IDs or package mock rewards. SDK failure should not prevent ordinary gameplay where the platform permits fallback.

### Prepare all listing materials

Read [materials](materials.md) and the platform profile. Produce separate game and material archives, copy, provenance and review previews. For 233/4399, edit promotional/brand content and real gameplay into one video. First try capturing missing footage from an isolated runnable build; request device recordings only when necessary. Use available image tools for missing artwork; retain masters/prompts. Illustration is not a gameplay screenshot.

Unknown rules and unavailable assets must be explicit. Continue unrelated work. Do not call icons plus a game ZIP a complete kit, or defer independent materials until an AppID arrives.

### Verify and request next inputs

Run relevant builds, archive checks and critical behavior tests. Inspect final images, video joins, playback and representative gameplay. Default non-TapTap Android target is Xiaomi 8 / Android 10; inspect the host kernel and stricter platform requirements. Report device tests as pending if no device was used.

Report each channel's source version/hash, paths, material status, checks, gaps and rebuild command. Use a compact table: upload candidate ready; prepared awaiting configuration; candidate with unavailable features disabled; missing assets/rules.

After independent work, collect only necessary missing fields. 4399 may need AppID, ad/save permissions, and rank ID/rules only if a leaderboard is required. Established 233 IAA does not take a frontend AppID, though backend creation/binding and host tests remain necessary. Xingxia injects runtime gameId. Xiaohongshu needs the current upload-page rewrite command. Follow the profile instead of asking everyone for “AppID and Secret”.

Distinguish SecretID from SecretKey and verify their roles. Request a secure server-side configuration location when needed; never put server credentials in frontend bundles, logs, copy or this Skill. Do not block on credentials unused by the SDK.

## Phase 2: bind, build and validate

Confirm game/channel identity, fill required fields and enabled capabilities, rebuild, and produce `<game>_<channel>_v<version>_<date>.zip` plus a separate material ZIP. Record size, SHA-256, entry hash, file list and checks. Preserve old packages. Exclude placeholders, test bridges, demonstration saves, environment files and unrelated IDs.

Accept partial answers. Store non-secret IDs, permissions and gaps in existing channel notes; resume ready channels immediately. Pending permissions may allow a disabled-feature candidate; never claim those features work. New product systems require explicit scope.

Deliver clickable source, game ZIP, material ZIP, copy and validation records. If the user uploads, ask for the preview URL; if uploading is authorized, continue within scope. Do not preserve temporary preview tokens in reusable documentation.

Separate local, real-SDK, device, upload, review and release evidence. Verify completed/cancelled ads and save round trips on the real host. A selected upload, QR code or successful build is not publication.

## Incremental updates

Compare previous SOURCE_BASELINE, current TapTap and current channel in a three-way update. Merge upstream changes while preserving channel hooks, saves and compatibility. Rerecord changed UI; label older footage with its actual version. Reuse verified brand masters and recheck exports.

For new platform knowledge use [extension rules](extending.md), separating user decisions, official rules, observed implementation and assumptions.
