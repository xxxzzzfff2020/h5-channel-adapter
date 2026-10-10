# Opt-in Android-device TapTap H5 automation

Read and execute this route only when the Owner **explicitly requests Android-device automation for adaptation or testing**. Ordinary platform integration, local ports, Skill maintenance and read-only audits do not start it, install tools, occupy devices or upload. Project evidence on 2026-10-10 verified a USB device → ADB/existing Node → official MCP version information → QR → TapTap H5 → conditional CDP → a read-only native-board opening through game UI. It does not certify every device, release WebView, emulator or SDK case.

## Explain the full flow and obtain startup confirmation

Prepare the complete flow from existing project records and tool inventory, then use an **actually available user-input popup permitted for confirmation**, such as `request_user_input_async` when supported. Offer “Continue the described flow” and “Cancel,” and wait for an explicit Owner answer. Defaults, silence, timeout and messages from other chats are not consent. If tool restrictions prohibit approval questions or no popup is available, state that limitation and wait for text confirmation of the same full description; never claim a popup occurred. Maintaining this reference does not trigger the popup or device flow.

Fill the following popup-content template with actual details; it is not an instruction to call a tool now:

```text
Continue this Android-device automation flow?
Project/target app_id: <verified target>; device: <Owner-selected device, or discovery only without control>.
Current package: <path, version, SHA-256 or directory-manifest hash>; reuse an existing upload first.
Steps: detect existing ADB/Node/official MCP → verify USB authorization and host → obtain the current-version QR → transfer QR and control scanning/restart through ADB → verify actual URL, runtime version and entry hash → execute the SDK cases below → save evidence and release resources created by this run.
SDK cases: <each case, read/write classification, real credentials or whitelist, save/reward protection>; startup telemetry/sync: <known effects or unknown>.
External actions: <any upload, automatic review, publication or other remote writes; unapproved actions stay pending and stop before execution>.
Review submission can enter review; “publish immediately after approval” may make the app public. Startup consent does not cover artifact upload/review/publication, which require separate confirmation.
Choices: Continue the described flow / Cancel.
```

## Detect and reuse existing capabilities

- Prefer a USB Android device. Verify a unique device, USB-debugging authorization, Android/TapTap/available engine versions and one device-control owner. Resolve multiple-device or shared-control conflicts instead of choosing the first device. Run ADB device commands only after startup confirmation.
- Detect actual ADB, Node and official MCP tools/versions. Missing Mobile MCP does not mean no route exists. Do not build a new environment, install global tools or change Providers for this workflow. Report missing capabilities and stop dependent steps; test required Node features such as WebSocket.
- After USB failure, an emulator is a separately explained and verified fallback. An emulator starting, an ADB connection or a visible CDP target does not establish TapTap H5, physical-device or SDK acceptance.
- Authorized ADB control can include image transfer/media indexing, UI actions, necessary restart, screenshots and bounded logs. Do not erase app/account/player data or reset the shared ADB service. Remove only this run's forwards and temporary files, then return device control.

Follow current [official ADB documentation](https://developer.android.com/tools/adb) for USB authorization and supported commands. This reference itself grants no connection, control or installation permission.

## Reuse packages, refresh identity and obtain an entry

1. Prefer existing uploaded packages, real app bindings and approved cases. New uploads follow the [TapTap automatic-review boundary](taptap.md#automatic-review-and-publication-impact) and [per-artifact gate](h5-reliability.md#h5-external-upload-confirmation). Never reupload to obtain an entry or refresh a version; startup consent does not replace those confirmations.
2. Distinguish `app_id`, `miniapp_id`, preview `version_id` and the backend package ID. Force-refresh official app information using the current schema, for example the discovered `get_current_app_info(ignore_cache=true)`. Obtain fresh version information from actual returns, an exposed raw tool or the cache file identified by that return. Verify target, freshness and official field meaning; never read auth files, hardcode private cache paths/nested structures or unconditionally interpret `package_id` as a version ID. A tool appearing in source does not mean this session exposes it.
3. Verify the QR endpoint, environment/type and version parameters against current official capabilities. Check each parameter's meaning if constructing a URL. Bind the entry to the version/package hash and reverse-decode the QR to verify its encoded URL. Keep QR material, cache, tokens and real IDs in project evidence only.
4. Scan through actual TapTap UI on the authorized device. Exit the old game instance and, when necessary, fully exit/restart TapTap before scanning a changed package. Compare **actual loaded URL, runtime version/build marker and original entry-byte hash** with the frozen build. A title, successful scan, QR version parameter or refresh action does not prove the new package loaded. Do not clear progress to fix caches.

The official [MCP tool definitions](https://github.com/taptap/instant-games-open-mcp/blob/main/src/features/app/tools.ts) expose the refresh parameter; rediscover return shapes and QR contracts at use time. Distinguish raw HTTP bytes from CDP-serialized resource content; a stylesheet representation difference alone does not prove a wrong build.

## CDP is conditional observation

Discover the current H5 process and its actually accessible DevTools sockets. Forward the observed socket, enumerate targets and match one H5 target by expected URL/version. Never fix `chrome_devtools_remote`, a PID/port or select by title alone. Connect existing Node to the returned WebSocket with bounded timeouts/fields; do not inject game state by default.

[Official WebView debugging guidance](https://developer.chrome.com/docs/devtools/remote-debugging/webviews/) requires the host to enable debugging. CDP/Appium cannot force it on in a release WebView or guarantee JS execution. Use authorized UI, screenshots, backend records and existing game diagnostics instead; leave unverifiable version/hash/cases pending rather than claiming PASS.

## SDK cases and evidence layers

Before starting, list each case's read/write nature, real test account/credentials/whitelist, save/reward protection and expected receipt. Read-only board opening, score submission, cloud writes, achievement unlocks and completed-ad rewards are separate cases. Unapproved remote writes stay pending; a read-only SDK case does not imply normal startup telemetry/sync is absent.

Opening a native board through game UI and returning proves only that case, not ads, cloud saves, achievements, iOS, emulators or full experience. Diagnose missing images with [deployed-resource checks](deployed-assets.md); bind a fixed package to new version/evidence.

Record target/device/tool versions, startup confirmation, package/entry identity, each case's read/write nature and result, necessary screenshots/bounded logs, actual backend state and gaps in existing project delivery notes. Separate local, real-host/device, upload, review and release evidence; one device receipt does not close other acceptance layers.
