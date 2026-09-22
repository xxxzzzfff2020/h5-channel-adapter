# Evidence and provenance

Reviewed: 2026-09-22. The 233 and 4399 profiles were distilled from four authorized adaptation tasks covering two independent TapTap H5 games. The reusable distribution intentionally excludes task/session identifiers, private source paths, game assets, application IDs and account data. No access to those projects is required to use this Skill.

## Reusable observations

- Both games retained plain JavaScript/Python build systems; porting does not require changing stacks.
- Platform-specific reward completion codes, deduplication, late-callback isolation and persistence retries materially affect correctness.
- New channel saves were isolated; already-shipped save keys had to remain compatible.
- Game builds and listing videos sometimes had different versions. Metadata must not relabel old footage as current.
- Promotional+gameplay composites varied in length; neither sample duration is a universal requirement.
- A prior material folder or successful upload discussion did not prove every local listing file was present.

## Official sources

- 233 IAA: https://cdn.233xyx.com/h5ad/metah5ad_v1.min.js (script reachable during review; not a real-ad test). Listing sizes were supplied from creator forms; refresh before delivery.
- 4399: [ads](https://open.4399.cn/docs/h5mini/api/rewardad.md), [saves](https://open.4399.cn/docs/h5mini/api/archive.md), [ranking](https://open.4399.cn/docs/h5mini/api/ranking.md), [FAQ](https://open.4399.cn/docs/h5mini/faq.md).
- Xiaohongshu: [MiniTool capabilities](https://miniapp-sandbox.xiaohongshu.com/minitool/doc).
- Xingxia: [existing-game upload](https://game.virtualoverapp.com/creator/center?section=guide&cat=create&doc=track-a-upload), [Agent Skill](https://game.virtualoverapp.com/creator/center?section=guide&cat=create&doc=agent-skill), [SDK](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=index).
- Bilibili: [SDK](https://www.bilibili.com/toy/publish/sdk), [Skill entry](https://www.bilibili.com/toy/publish/sdk/skill), [official Skill repository](https://github.com/bilibili/toy).

New platform profiles are based on documentation inspection only. No new platform application, upload, paid call, device acceptance or review was performed as part of preparing this distribution. The user subsequently supplied MiniTool, TOY and Xingxia creator forms on the same date. Their known material fields now have machine checks; package budgets are separately tracked. This is schema/helper evidence, not a completed port.

## Helper validation

Initial development exercised synthetic valid 233/4399 materials and failure cases: missing roles, unknown roles, excessive text, wrong ratios, absent gameplay provenance, changed source hash, path escape, false file suffix, CLI operation and read-only inventory with credential/symlink exclusions. Existing project media were also probed read-only. None of this certifies gameplay authenticity, a full game build or physical-device behavior.

The repository's reproducible test command is documented in README.md. Synthetic fixtures are not commercial game assets and do not count as live-host evidence. All helpers need Python 3.9+; media validation requires ffprobe, and the test fixtures use ffmpeg.

## Version 0.2.0 validation

On macOS, 40 synthetic scenarios passed, covering all five material profiles and the actual-artifact budget helper: optional vs required fields, hard vs recommended ratios, mixed-media count, 60-second and byte limits, WebP/WebM inspection, audio-only OGG rejection, original-source immutability, budget boundaries, unknown limits and CLI non-overwrite behavior. OGG video decoding was not separately exercised because the local FFmpeg lacks a Theora encoder. Windows execution remains pending; the portable CI template is not an execution receipt. Skill-format, Python/JSON syntax and bilingual-reference/link checks passed.
