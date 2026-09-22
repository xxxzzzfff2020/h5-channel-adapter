# Bilibili TOY

Status: SDK/official Skill documentation reviewed 2026-09-22 after creator access was available; no port/upload/device test yet. Use [upstream tools](upstream-tools.md). Keep the official `bilibili/toy` Skill and CLI independent and current, not copied or rewritten into this repository.

## Local packaging and capabilities

TOY accepts built static H5 content. Package `index.html` at root or one unambiguous first-level directory. Relative asset URLs are essential under `/toy/<slug>/`; do not ship `/assets/...` or source-only projects. Hash routing and in-page anchors are supported; history routes need real corresponding HTML files. Preserve an existing slug; do not delete/recreate to rename an address.

Official SDK: `https://s1.hdslb.com/bfs/seed/toy/app/sdk/toy-sdk.js`, global `window.toy`. Feature-detect using `toy.isSupport(...)` and handle promise rejections. The inspected API supports cloud storage and rankings; it does not establish rewarded ads. Preserve local play and ask about material ad-dependent progression changes.

Cloud storage is scoped by signed-in user + TOY: up to 128 keys, value strings ≤1024 bytes, key ≤128 bytes with letters/digits/underscore/hyphen and no `__` prefix. An entire management-game save may not fit. Measure UTF-8 bytes, keep local recovery, and choose a bounded compact save design only after sizing; do not promise full cloud sync or split blindly across all keys. Batch writes at meaningful checkpoints; cache reads. Quotas are shared across all players of a TOY; handle `http_error` / 307044 with backoff. Published QPS thresholds are unavailable.

Rankings: board 1–5, integer score -16777216 through 16777215, absolute score, highest value retained, descending order. Test score semantics before mapping an existing leaderboard; do not clamp silently. `getMyRank().ranked` determines membership even for zero/negative scores. User consent/login and per-capability support still apply.

Container APIs are App-only. Subscribe before `setContainerMode` and confirm an observed matching state; a resolved Promise does not prove orientation/immersive mode changed. Use actual viewport/safe-area data. Camera/microphone are separate optional permissions, not required just to port a game.

## Materials and publication

Poster and icon are separate fields. Current official checklist supports PNG/JPG/JPEG, recommends a 4:3 poster around 1200×900, and defers icon limits to current CLI help. Treat the ratio as a recommendation. Other quotas and video requirements require live form/help verification; do not apply 233/4399 video rules automatically.

No frontend AppID/Secret requirement was established. First finish local preparation; creator login, chosen immutable slug and verified target ID are needed at publishing/update time. Inspect `toy --help-json` and command-specific help before constructing commands; use structured `--json` for API commands. Version/upgrade commands have their own behavior, so do not blindly append flags to all commands.

Use the current official preflight tool or documented manual checks before upload. Distinguish errors from warnings. For authorized publication, the official workflow creates an uploaded preview before review submission; `--yes` submits. A metadata-only update may submit directly. Follow current user authorization and the official Skill's applicable preview/review process; never interpret a preview as release or upload during a local-only request.

Sources: [SDK](https://www.bilibili.com/toy/publish/sdk), [official Skill entry](https://www.bilibili.com/toy/publish/sdk/skill), [upstream Skill](https://github.com/bilibili/toy/blob/main/skills/toy/SKILL.md), [content checks](https://github.com/bilibili/toy/blob/main/skills/toy/references/content-checklist.md). Upstream documentation is not vendored in this distribution.
