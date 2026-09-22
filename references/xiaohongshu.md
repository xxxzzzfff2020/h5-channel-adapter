# Xiaohongshu MiniTool / 小红书小工具

Use this profile for offline H5 content in the MiniTool container. Confirm the current container capabilities and upload-page instructions before adaptation.

Before adaptation obtain the **current complete rewrite command from step one of the upload page** and read the official Skill it references. The capability page explicitly is not a substitute. Do not reuse a stale saved command or vendor a modified official Skill; follow [upstream tools](upstream-tools.md).

## Required changes

- Pure HTML/CSS/JS works offline. No network access, external media/fonts/scripts, WebSocket, WebRTC, workers, service workers, WASM, eval/new Function, iframes or external navigation.
- JavaScript must be package-local external `.js` files: no inline script, inline event handlers, javascript URLs or data/blob scripts. Inline CSS and local CSS are supported. All game dependencies must have a compatible local path.
- SDK is host-injected `window.xhs.miniTool`; do not insert a foreign CDN SDK. Canvas2D and pure WebGL rendering are supported subject to these restrictions.
- Documented package whitelist is html/css/js/png/jpg/jpeg/gif/webp/svg/woff/woff2/json, with one HTML entry. Audio/video tags are discussed but mp3/ogg/mp4 are absent from this whitelist. Check the current official validator before deciding how BGM/media can be packaged; do not assume arbitrary audio files are allowed.
- JavaScript/CSS baseline is Android 8.1's original Chrome/WebView 61 (JS ES2017), and documented iOS minimum is 18.4. Retain Xiaomi 8 / Android 10 as the device target while satisfying the stricter kernel baseline.

## Storage and capability decisions

Prefer native storage on client ≥9.46.0, with buildVersion and method checks. Documented limits: 1 MB/key and 10 MB total. Use current official async set/get/info/remove/clear APIs and consistent encryption options. Treat localStorage/sessionStorage/IndexedDB/cookies as unreliable fallbacks, handle unavailable/write-failure states and migration explicitly. File input only supports images/video, so a text-save import workflow needs redesign.

Exposed native APIs include note publishing, image saving, temporary files, launch options and storage. No rewarded-ad or leaderboard API is established by this capability list. Do not fake ad completion, silently grant rewards or advertise cloud saves. Material progression/economy changes require a product decision; offline ordinary gameplay can proceed separately.

The upload-form requirements recorded on 2026-09-22 specify name ≤14, description ≤14, an icon (PNG/JPG/JPEG ≤5 MB, recommended 1:1), ZIP-only upload ≤10 MB, version, scene tag and permissions. Exact icon pixel dimensions/version syntax are unspecified. Select only used album/camera/microphone/local-storage capabilities; map permission labels through the official workflow. No listing-video field or AppID/Secret requirement is currently recorded. In-game note rules are separate. The current rewrite command is still needed. See [listing fields](listing-fields.md) and [package budgets](package-budget.md).

Source: [official container capabilities](https://miniapp-sandbox.xiaohongshu.com/minitool/doc). Recheck the upload-page Skill and run its current checks during the first real port.
