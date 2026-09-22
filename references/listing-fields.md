# Listing manifest fields

Listing requirements were recorded from creator forms on 2026-09-22. `assets/material-rules.json` is the shared machine source for all five platforms; `assets/package-rules.json` covers game upload size separately. Field snapshots are not permanent API contracts. Refresh official tooling/form requirements at use time.

## New-platform mapping

| Channel | text | metadata | files[].role |
| --- | --- | --- | --- |
| xiaohongshu | name, description, version (required) | scene, permissions (required) | icon (one) |
| bilibili-toy | name, slug (required) | no additional fields currently recorded | poster + icon (one each) |
| xingxia | name, description (required); about, controls (optional) | categories (1–2), tags (1–5); game_type/orientation optional | cover (one); promo_media (0–8 images/videos combined) |

Use the example manifests in assets for shape only. Fill real project copy, file paths and provenance. Use the current game’s name, features and tags. Imported H5 uses the applicable existing-game upload route; workshop-managed publishing is a separate route.

Xiaohongshu name and description are each ≤14; version syntax was not specified. Scene options are the seven categories in the shared rules. Permission values in our manifest (`album`, `camera`, `microphone`, `storage`) are internal metadata labels, not asserted SDK identifiers: select only used capabilities, map through the current official workflow and verify whether the backend requires an explicit no-permission option. Do not request all permissions by default.

Bilibili 4:3 poster and 1:1 icon ratios are checked as form requirements; 1200×900 and 500×500 are recommended export sizes. No byte limits or name limit were supplied. A missing description/video field does not imply another undocumented requirement. Preserve an existing slug.

Xingxia covers use JPG/PNG, at most 5 MB. 800×450 is recommended. Optional promotional images/videos share one total of eight, not eight of each. Images accept JPG/PNG/WebP ≤5 MB. Videos accept MP4/WebM/OGG ≤100 MB and ≤60 seconds; 1024×556 is a recommended ratio. Do not require a video or promotional+gameplay composition where this form does not. A video must contain a visual stream; audio-only OGG is not a promotional video.

Only hard dimensions/ratios fail validation; recommendations produce warnings. New text lengths use conservative UTF-16 units (astral characters count twice); backend counters remain authoritative. Optional absent copy/media remains optional. Arrays reject duplicate selections. Required product text must come from the current game's source materials, never fabricated feature promises.

Every output needs sources with path/hash. Gameplay captures also need a version; video sources use source_seconds/output_seconds. `promo_media` accepts truthful promotional artwork or actual captures; do not label illustrations as screenshots. The 233/4399 composite-video requirement stays channel-specific.

A technical pass covers encoded rules only. Unknown fields, live permissions, visual quality, platform validation and device tests remain separately reported.

Examples / 示例：[xiaohongshu](../assets/material-manifest.xiaohongshu.example.json) · [bilibili-toy](../assets/material-manifest.bilibili-toy.example.json) · [xingxia](../assets/material-manifest.xingxia.example.json)
