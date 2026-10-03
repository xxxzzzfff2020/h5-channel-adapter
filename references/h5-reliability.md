# H5 reliability contracts and acceptance recipes

Reusable engineering guidance, **not a platform specification or a shipped library**. Adopt only the selected work after inspecting existing code, save/economy rules and current official APIs. Do not replace a working architecture for uniformity. Project-specific IDs, slot names, limits, timeouts and historical pass counts are deliberately excluded.

## Identity, storage and cloud

- Unknown runtime identity may continue in isolated local scope, but must not write account cloud, boards or achievements. Network recovery is not identity confirmation. Keep platform account, archive UUID, local key, save lineage and request generation distinct.
- Guard the storage **getter**, reads and writes, including startup preferences. Separate in-memory play, verified local persistence and cloud success in the UI. Validate candidates before commit; retain a checksum-verified backup before migration/import/cloud replacement. Checksums detect corruption, not cheating. Future schema must not be overwritten by an older client.
- Rewards and completion receipts are one persistence transaction. On save failure, rollback or retain a non-consumable confirmed-but-unsaved state with explicit recovery. Never show durable success solely because memory changed. A compatible mirror failing does not invalidate an already committed authoritative slot.
- Cloud startup is single-flight, with generation and settled-once checks after timeout/reset/account switch. Read failure is not empty cloud. Switching A → B with empty cloud must not upload A's local save into B. Preserve manual versus automatic sync product decisions.
- Reconcile only a provable sequence within the same lineage; show actual divergence for player choice and back up before replacement. Bigger balances, newer timestamps or unrelated revisions are not sufficient. Use returned archive IDs; missing create acknowledgment requires reread/reconciliation, not blind duplicate create.
- A UI timeout/cancel invalidates local handling; an already issued remote write may still finish. Keep unknown-result state, reread before another write and avoid overlapping retries. Client preflight, leases or read-revision-then-write are not server CAS/atomic locks.
- Main saves and diagnostics sharing platform quota need one arbiter, main saves first. Coalesce latest pending state and serialize at actual submission; classify failures and bound retry/backoff using verified current quota.

**Tests:** getter/read/write exceptions, quota exhaustion, inconsistent readback, corrupt primary/backup, future schema, old schema migration, alternating windows, reward save failure and refresh. For cloud: two real accounts/sessions/devices, empty/old/forked saves, switch during request, missing create receipt, upload timeout followed by actual remote success, diagnostics contention. Synthetic tests do not close real-account gates. Use isolated test saves.

## Offline progress, check-in and ads

These are distinct product contracts; do not add them merely because the target supports cloud or ads.

- Cold start and same-session foreground return share one offline settlement policy. Process each interval once using a high-water mark; cover rollback, repeated returns, midnight and caps. Preserve economy gates and the policy for discarded over-cap time.
- Where unclaimed rewards exist, keep separate time, money and ad ledgers: old unclaimed money must not freeze construction/time or erase new rewards. Direct-credit games need no artificial carried-money field. Ad-hidden time must not become duplicate offline progress; reset the frame clock on return.
- Check-in defines timezone, consecutive versus cumulative days, first-day eligibility and completion. Reward, claim flag and count commit together. Restoring older same-lineage saves retains anti-duplicate high-water marks without max/adding balances. A changed day boundary/activity version needs migration; daily tasks and ad quotas keep separate ledgers. Local clock guards are not trusted server time.
- Ads: verify eligibility → freeze target and unique attempt ID → persist pending if the product requires refresh recovery → show → accept only documented terminal success for current account/attempt/target → persist reward plus receipt → report saved success. Never infer completion from duration, focus or a timer. Resettable daily counters cannot be unique IDs. Late/duplicate/cancelled/failed/no-callback outcomes do not grant another reward. Refresh semantics must be explicit; client deduplication is not distributed exactly-once.

**Tests:** retained old receipt plus new interval, segmented versus whole settlement, repeated same-day ad attempts, pending target changes, duplicate/late callbacks, cancellation/no callback, pending/reward storage failure, refresh and audio recovery; day-boundary migration, old-save restore, rollback and cross-account isolation.

## Leaderboards

Freeze board ID, integer metric/range, encoding version, order, ties, overwrite/merge policy and eligibility. Do not coerce huge wealth into unsafe JS Number or encode hidden decimals without an agreed contract. Review/dev/imported-special saves require explicit eligibility. Unknown identity cannot submit.

Scope submission state by identity, save lineage and board namespace; changing board must permit its first submission. A successful callback confirms only the submitted snapshot, never a newer score queued during the request. Best-ever boards and current-state boards do not always merge with max. Invalidate old generations on account/save/board changes. Keep queued/syncing/synced/failed/range-limited/unsupported states truthful.

**Tests:** boundaries/illegal values, ties/increase/decrease, new board first submit, score changes during submission, never-returning callback, stale callbacks, retry, actual readback, nickname/avatar/self row. Opening a board is not a successful submission; client scores are not server authority or anti-cheat.

## Audio and settings

- One controller owns user intent, scene, background/ad interruption and actual playback state. Long BGM may use a reused native media element; short SFX may use WebAudio. Preserve a stable existing backend unless measurement justifies changing it. Encoded bitrate is not decoded PCM memory.
- First play happens directly within a user gesture. Fence stale play promises/resource events; autoplay rejection waits for another gesture. Unexpected stalls get bounded recovery, not endless new contexts/reloads. A loading `suspend` event is not proof of playback pause. Volume zero/muted, user pause and temporary ad ducking are different states.
- Fixed synthesized loops can be prerendered **from the project's own music** to decouple scheduling from rAF. Preserve loop tails and audition the seam. Dynamic composition, note interaction and rhythm timing need a different design; do not mandate one format/duration/sample rate.
- Loop clock wrap is progress. When testing main-thread blocking, read media time in a later event-loop task, account for wrap and record new synthesis nodes. Advancing clocks/running flags are not proof of audible uninterrupted sound. Diagnostics must not unlock audio and change the failure being observed.
- Separate music/SFX switches and volumes; persist preferences with failure handling. Specify whether cloud restore carries settings or device preferences win. Respect mute/pause on gesture, focus and ad return. Font scaling covers buttons/modals/canvas, long text and narrow screens at max size; font loading failure gets readable fallback. General font-family switching is not proven by a size control.
- Power-saving/motion settings change presentation only, not economy/simulation. Unsupported vibration degrades safely. Reset preferences, restart game, erase local save and erase cloud are distinct actions.

**Tests:** cold start, first gesture, switch scene/music, loop and seam, mute/zero, pause/restart/refresh, settings failure, play rejection/stall, stale promise, loading failure, ad success/cancel, background/lock/call interruptions, max-font narrow screen. Real iOS/Android host listening and long sessions remain separate from browser counters; one historical phone listening pass does not certify another game.

## Startup, layout, performance and diagnostics

An independent minimal HTML boundary covers module download/parse, sync/async initialization and timeout; show build/error code and retry by reload without clearing saves. Retire guards once usable UI or cloud preflight exists. Build target does not polyfill every DOM/Intl/storage API. Test same-origin HTTP builds; opening development source with file:// is not a player-device failure diagnosis.

Use one coordinate contract for viewport, DPR, render scale, safe insets and input inverse transforms; don't multiply DPR twice or paste Maker NanoVG calls into DOM/canvas code. Capture a consistent event snapshot. Test narrow/tall/tablet layouts, safe areas, max text, rotation and actual pointer/touch hit areas. Duplicate input suppression and reward idempotency are separate; verify runtime synthetic events rather than relying on arbitrary debounce timers.

Measure fresh, middle and advanced saves. Separate JS/layout/paint/input from product pacing. Reduce duplicate models, DOM measurements/writes and layout reads first; cache display calculations but revalidate purchases against current state. Presentation throttling/scroll quiet windows must preserve simulation, saving and full structure resynchronization. In the **same page instance**, test first unlock → stage transition → reset/rebirth → reappearing controls → late game. Refreshing between every stage can hide stale hidden-state bugs. Avoid universal frame-rate prescriptions or claiming a device root cause from an FPS screenshot.

Diagnostics is a bounded optional side channel: independent schema/slot excluded from game restore, UUID assigned by the platform, fixed whitelist, bounded strings/counters and final UTF-8 wrapped-byte limit. Record build and available host/device fields plus small state summaries; no UID, save body, token, signed URL, arbitrary exception payload or unbounded event log. Missing fields stay absent. Main-save priority and shared budget apply; failures must not block gameplay. Document purpose/access/retention in the game. No promise of capture before the main module starts or after OS termination.

**Tests:** missing APIs/modules/resources, storage failure before entry, sync/async throw, recover without erasure; actual layout/input and same-instance lifecycle; multibyte/emoji payload bounds, serialization/file-write errors, SDK no callback, shared quota, account switch, first-create race and diagnostics failure without gameplay regression.

## Evidence and coverage

For each selected area record **already covered / adopted / not applicable / pending verification**, target code/evidence and next check. Configuration, synthetic rules, browser visual inspection, real SDK, device listening, multi-account recovery and upload/review/release are independent layers. Package hashes connect evidence to the delivered candidate; never inherit another game's PASS.

| Experience area reviewed | Disposition in this Skill |
| --- | --- |
| Unknown identity, storage transactions, cloud reconciliation | Adopted in the contracts above; every target still requires implementation/tests. |
| Offline ledgers, check-in calendar/migration, ad transactions | Adopted only as selected game-work recipes; no default new systems. |
| Leaderboard encoding, eligibility, namespace and submission race | Adopted; actual score readback and display remain pending per target. |
| Native BGM/WebAudio SFX, own-loop prerendering, settings/font | Adopted with measurement/fit conditions; device listening is pending. |
| Startup boundary, same-instance structural regression, performance | Adopted; project-specific frequencies/caps excluded. |
| Diagnostic isolation, privacy, UTF-8 budget and shared arbiter | Adopted; official quotas and backend accessibility still verified at use. |
| Source/save/old-package protection, material provenance, evidence layers | Already covered by workflow/material/preflight guidance; retained. |
| Viewport/DPR/safe-area/input principles | Adopted generically; host geometry and synthetic input behavior pending. |
| Maker Lua/UrhoX APIs, NanoVG implementation, keyboard preview bridge, Maker UUID/build identity | Not applicable to H5 directly; no API/code copied. |
| Persistent-world/server authority and recovery | Pending separate product scope and real platform validation; no multiplayer system added. |
| Achievements, gifts and review prompt H5 route; live limits/tool revisions | Pending official verification; native examples and dated snapshots are not proof. |
| Historical audio/device/feedback observations | Evidence boundaries retained; no cross-project device or release guarantee. |

This table covers engineering topics, not a claim to ship implementations. Public distribution contains generalized contracts only, no private source documents, account/player data, internal task links or project assets.
