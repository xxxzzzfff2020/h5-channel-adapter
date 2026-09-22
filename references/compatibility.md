# Android baseline and acceptance

Default non-TapTap target: **Xiaomi 8 / Android 10**, unless the project owner explicitly overrides it. This is a workflow target, not a platform minimum or a passed test. Honor stricter platform engine requirements.

Android version does not identify the QQ/X5, UC, WebView or channel-app kernel. Record host/engine versions when available. Historical targets (Chrome 57/ES2015 for one 4399 build, Chromium 70/ES2018 for one 233 build) are examples, not properties of Xiaomi 8. Use evidence-backed conservative targets and feature detection without blocking initial work on repeated questions.

## Compatibility checks

- Transform and parse all generated scripts, including hand-assembled bootstrap code. Check official SDK syntax too, without rewriting vendor SDKs blindly.
- Syntax targeting does not supply API polyfills. Add only needed fallbacks for APIs such as globalThis, Object.fromEntries/hasOwn, Array.at/flatMap, String.replaceAll, queueMicrotask, CSS.escape, ResizeObserver and replaceChildren. See [esbuild targets](https://esbuild.github.io/api/#target).
- Check used CSS features: color-mix, dvh/svh, safe-area, flex gap, aspect-ratio, inset/logical properties, clamp and :has(). Keep base declarations and progressive enhancement; cssTarget does not verify layout.
- If needed, use scoped touch fallbacks when PointerEvent is absent. Stop movement on release/cancel/background, while lists still scroll. Test short screens, orientation, browser bars, iframe resizing, overlays, bottom controls and large text.
- Test first-gesture audio, ads/background recovery, mute, volume and track changes. Audio bitrate alone does not prove decoded-memory or interruption causes.

If converting color-mix, count source declarations independently; counts must match conversion coverage, with no unexplained skips. Zero source declarations is a valid result. Handle minified lines, media-query colons, strings/comments, final declarations without semicolons and spacing; never rewrite string literals. Inspect dynamic/inline CSS and variable scope/theme semantics; a last declaration is not necessarily the global base theme.

## Evidence

Ads: completion, cancellation, failure/no fill, timeout, duplicate/late callbacks, persistence failure and restart-safe single rewards. Saves: refresh, corrupt primary, unwritable storage, old versions, multiple windows and channel isolation. Play meaningful actions with a new save; preserve old-save unlock/tutorial state.

Check actual release ZIP contents, CRC, root entry, relative resources, forbidden markers and hashes; smoke-test that artifact. Modern Chromium with an old UA/viewport or fault-injected APIs is not an old kernel or physical Xiaomi 8. Mock ads do not verify real rewards.

If users still see an old version, compare delivered HTML/ZIP hashes and isolated fresh vs existing save flags before touching progress or blaming caches.

Report `passed_local`, `pending_platform`, `pending_device`, `blocked_missing_input` or `not_applicable` with evidence. Upload, review and publication require distinct receipts.
