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

## Native boot and recovery

Read [native storage boot](native-storage-boot.md) for key-inventory-first absence handling, narrow empty-marker policy, atomic optional migration, read-only unchanged boot, exactly one intended API write, verified readback and player-selected zero-write temporary sessions. The current online contract specifies callback calls return undefined; compatibility request handles and mock sentinel shapes must not become SDK guarantees. Keep real iOS failure of an older package separate from isolated tests and the latest candidate's pending phone acceptance.

## Music and official resource review

On 2026-10-13, the supplied [official builder URL](https://fe-static.xhscdn.com/minitool/20260923133933/minitool-zip-builder-1.7.0.skill) returned archive manifest version 1.7.0 while internal SKILL.md metadata said 1.6.0. Record URL/hash and both actual metadata values; read SKILL.md and relevant references instead of inferring version from the filename. Obtain the current upload-page command at use time; do not vendor or silently replace the official package.

The inspected whitelist still omitted MP3/audio extensions. A selected original loop represented as valid bounded local JS bytes and decoded by WebAudio is a project-specific candidate requiring explicit content/resource review, not a universally approved workaround. Never disguise a binary with a whitelisted suffix or use external/data/blob audio/video URLs. The inspected official budget limits a single decoded Base64 resource to 1 MiB; above 100 KiB requires documented review and prioritizing a permitted independent resource. Reconcile whitelist constraints rather than treating a local audit as platform permission. Our preflight flags large quoted Base64-like literals; split/generated payloads still need manual source review.

Retain original music provenance and selected duration/encoding, volume/mute, gesture unlock, looping, foreground/background lifecycle, cancellation of stale async decode/play, and non-blocking audio failure. Record original, encoded and decoded bytes plus startup/memory measurements or unmeasured status. Run the actual official directory and final-ZIP audits, plus our size/preflight checks. Static audit/decode success is separate from simulator, Android/iOS listening and platform review; missing device/listening evidence stays pending.
