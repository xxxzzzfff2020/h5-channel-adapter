# NetEase Xingxia / 星匣

Status: documentation reviewed on 2026-09-22; no representative port, host/device test or release yet. Read [upstream tools](upstream-tools.md) before invoking platform tooling; use the official live Skill/CLI without maintaining a modified copy.

## Phase-one adaptation

Existing HTML/JS/ZIP games are supported. The uploaded file limit documented for Track A is 50 MB; ZIP has `index.html` at root or one first-level directory. Prefer a ZIP with relative local resources for multi-file games. Single-file uploads must inline assets or use allowed absolute CDN references; local relative dependencies will be missing.

SDK integration uses only the official CDN IIFE `https://gz-vchar-pub.nosdn.127.net/star-letter/game-sdk/v2/sdk.iife.js`. Call `await window.GameSDK.init()`; the host injects gameId, read it from `sdk.context.gameId`. Do not hardcode it in init, embed mocks or construct the underlying parent-message protocol. Wrap calls in try/catch and use the SDK error guard.

Current documented capabilities include storage, oss, ai, exchange, logging and diagnostics. The inspected API index does not establish rewarded-ad or leaderboard APIs. Do not replace TapTap ads with paid exchange/AI or silently alter the economy. Disable unavailable optional entry points and ask about materially affected progression.

Storage uses object inputs: `sdk.storage.get({key})`, `sdk.storage.set({key,value})`. The embedding page's older positional example conflicts with the detailed storage API: use the current capability types/signatures. Private saves use `user` scope, never shared `game` scope. The documented single-value limit is 256 KB of serialized UTF-8 JSON; login is required. Handle local fallback, conflicts/version checks, size failures and retries with visible status. Do not introduce unbounded sharding. The host controls fullscreen/orientation; resize within its iframe, without requesting fullscreen or orientation lock from the game.

## Materials and next inputs

The user-supplied 2026-09-22 form narrows cover formats to JPG/PNG; the prior verified ≤5 MB limit remains recorded. 800×450 is recommended. Name 2–30 characters, description ≤300, classifications 1–2, tags 1–5; optional about ≤1000 Markdown-source characters and controls ≤500. Promotional images/videos are optional, up to eight combined: images JPG/PNG/WebP ≤5 MB; videos MP4/WebM/OGG ≤100 MB and ≤60 seconds. 1024×556 is recommended, not required. The supplied workshop-managed example is not a requirement to use that route or copy its game text/tags. Read [listing fields](listing-fields.md) and [package budgets](package-budget.md).

Local packages do not need an AppID questionnaire. For platform previews or publishing, use creator login and select/create the intended game only within authorization. Official CLI supports `star-letter login`; normal device login does not require manually creating an API key. Creation/publish binding IDs belong to creator tooling, not hardcoded runtime init. AI scenes/exchange items are separate, opt-in features.

`star-letter dev` supports platform-host previews with per-capability simulated/real modes. Test storage in its preview partition. Real AI/exchange may incur charges, and must not be activated as part of generic compatibility checks. Production excludes `star-letter.mock.*`. A draft upload is still an external write; plain publish is not a local build.

Sources: [upload](https://game.virtualoverapp.com/creator/center?section=guide&cat=create&doc=track-a-upload), [fields](https://game.virtualoverapp.com/creator/center?section=guide&cat=rules&doc=fields), [SDK](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=index), [embedding](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=embedding), [storage](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=storage), [local testing](https://game.virtualoverapp.com/creator/center?section=guide&cat=sdk&doc=local-testing), [official Skill](https://game.virtualoverapp.com/creator/center?section=guide&cat=create&doc=agent-skill).
