# Listing materials

`assets/material-rules.json` (relative to the Skill root) is the single machine-readable rule set. It contains the known listing fields for the five platform profiles. Read [listing fields](listing-fields.md) for text/metadata/role mapping and examples. Unknown limits must remain unknown. Workflow export defaults are not platform requirements.

## Scope and optional video

Use the material choice from [guided setup](guided-flow.md). Produce only selected work. For image/copy work, set `"processing": {"video": false}` in the manifest; this is the default when absent. Video processing requires an explicit `true`. Projects-only mode skips this workflow. Do not install, look for or invoke FFmpeg/ffprobe on the image/copy path.

The inventory reads PNG/JPEG/WebP dimensions with Python and lists/hashes audio/video without probing. Add `--probe-av` only for selected audio/video inspection. Material validation uses image headers for image format/dimensions; a visual review is still needed, since headers do not prove full pixel decoding. Selected video validation uses ffprobe; video editing/decoding uses ffmpeg.

With video off, video entries and missing video/cover deliverables appear under `deferred`; `technical_status: pass` covers the checked scope only. `profile_complete: false` indicates deferred work or failed checks. Keep platform requirements unchanged: a required video stays pending, while the project package and selected images can be delivered. Neither field certifies current backend requirements or publication. A supplied video is not fully checked merely because it was copied.

## Provenance and images

Inventory the game root and TapTap source. Map roles to source paths/hashes, version, orientation and reuse/convert/recapture/missing status. The helper skips dependencies, backups, generated caches, credentials and symlinks; inspect a backup separately if it holds the only source. It cannot choose the newest authoritative asset or edit images.

Prefer confirmed brand masters and actual current gameplay, then verified supplied assets, fresh channel captures, and generated artwork for missing compositions. Never infer authority from timestamps/names. Export platform variants from high-resolution masters with correct aspect ratios and safe areas; do not stretch. Follow the active image tool's editing constraints, and visually review exact outputs.

Only a detail hero may be branded artwork; other gameplay screenshots must show real execution. Identify older versions honestly. Wait for rendering/fonts/loading and avoid blank/loading/debug/obstructed frames. Use isolated test saves; legitimate demo progress may show unlocked content but must have provenance and never affect player saves. Distinguish browser, host-client and physical-device captures.

## Video

When video processing is selected, for 233 and 4399 deliver one edited video combining promotional/brand content with actual gameplay operations, not two unjoined files. Prefer existing promotional footage; use brand opening/closing frames if needed. The default export is 1920×1080, 30 fps, H.264, yuv420p, AAC, faststart; platform-specific limits win.

Portrait footage may be centered or arranged in panels with an honest branded background. Preserve proportions and meaningful UI; repeated stills are not gameplay. Choose durations based on the content and platform limits. Use authorized music and identify recorded vs added sound. Keep genuine operation speed; avoid idle stretches and page-loading gaps.

Record originals, source/output time intervals, layout, audio source, source/target versions and hashes. Unknown host/version remains unknown. Probe metadata, decode the whole video (`ffmpeg -v error -i <video> -f null -`), inspect opening/middle/joins/end and listen to playback.

## Deliver and check

Provide independent source, game ZIP (preview only if required config is absent), material ZIP, copy, upload order and provenance/check reports. Include only final uploads and necessary guidance in the material ZIP; retain masters/cache in the production folder.

Create a manifest from `assets/material-manifest.example.json`. Output paths are relative to the manifest directory; fill real paths/hashes/versions. The example is not upload-ready. Then run:

```sh
python3 <skill-dir>/scripts/verify_materials.py <manifest.json> --report <evidence-dir>/materials-check.json
```

The helper checks actual encoding, size/ratio/dimensions, roles/counts, text limits and source records. MB uses decimal bytes. It does not watch video, certify authenticity/branding/audio or verify live backend rules. `pass` means encoded technical rules only. Report manual review, host and device validation separately; suffixes must match actual encodings.
