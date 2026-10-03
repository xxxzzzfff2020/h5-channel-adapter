# TapTap H5 target

Reviewed **2026-10-03** against the official [H5 MCP setup](https://developer.taptap.cn/minigameapidoc/quick-start/mcp-guide/mcp-setup/), [upstream MCP](https://github.com/taptap/instant-games-open-mcp) and enabled tool schemas. Refresh before use. This is the H5 route with host-injected global `tap`; ordinary browsers may lack it. Maker/UrhoX and native Android/iOS/Unity SDKs are different products.

## Prepare locally

Accept generic H5, TapTap H5 or another platform H5 baseline. Follow [selection](selection.md) before creating outputs. For a new TapTap target, isolate platform hooks and saves in an independent project. For an existing TapTap target, perform a three-way update and retain established keys, schema, reward receipts, app binding and old packages. Do not infer app ownership from a directory name.

Keep a runnable static build with `index.html`, relative resources and correct orientation. The current upload tool takes the verified **build directory**, not arbitrary source or a listing ZIP. Also retain a checksummed game ZIP as a local candidate; do not infer current upload size limits. Shared package rules leave the unknown limit unset. Run budget/preflight checks with `--channel taptap`; static success does not prove injected APIs or account binding.

TapTap listing rules remain pending current creator-form verification. Prepare truthful name, description, controls, icon/cover and gameplay images when selected; `assets/material-rules.json` intentionally imposes no invented TapTap dimensions/counts. Its warnings mean the kit is not certified complete. Verify current required fields, orientation, sizes and video scope before delivery; video remains opt-in.

## Select capabilities, then verify this application

| Selection | Confirmed route / boundary |
| --- | --- |
| Ads | Read `get_ads_integration_workflow` first. Confirm current app/user choice, then `check_ads_status`; only active status plus a valid automatically resolved space ID permits `get_ad_integration_guide`. Never ask for/manual-copy/reuse an ad-space ID. Real rewarded success and saved reward need host tests. |
| Identity | Confirm actual H5 identity API from current official API docs/tools; developer OAuth and multiplayer player IDs are not interchangeable with runtime account identity. Unknown identity isolates local play and blocks account writes. |
| Local/cloud saves | Local persistence is game implementation; use `get_cloud_save_integration_guide` for the official file/archive route. Preserve existing sync policy and validate account switches, empty cloud, conflicts and unknown write outcomes. |
| Leaderboard | Read `get_leaderboard_integration_guide` first; pin metric, range/encoding/order, eligibility, board namespace and configuration. Do not create a board merely to inspect capabilities. |
| Share / vibration | Read `get_share_integration_guide` / `get_vibrate_integration_guide`; share template review/configuration and device behavior are separate gates. No SDK npm install for the host global. |
| Diagnostics / feedback | Runtime summaries are optional game work. `get_debug_feedbacks` is a developer operation with a default processed-state mutation and downloads; do not call it during generic/read-only capability research. For explicitly requested read-only feedback, use the current schema's `fetch_and_mark_processed=false`. “Processed” is not “fixed”. |
| Multiplayer | The MCP exposes `get_multiplayer_guide`; request it only when selected. This is substantial product scope, not a mandatory H5 adaptation feature. Server authority, identity and recovery must be designed separately. |
| Achievements | **Pending H5 verification.** [TapSDK achievement docs](https://developer.taptap.cn/docs/sdk/achievement/features/) list native iOS/Android/Unity support; this does not establish a H5 JavaScript route. No dedicated achievement tool was found in the checked MiniGame registry. |
| Gifts / redemption | **Pending H5 verification.** [Gift docs](https://developer.taptap.cn/docs/sdk/tds-gift/) belong to the game-service family. A platform campaign page or native/server API is not an established H5 client integration. Verify an applicable official route, server trust and idempotent grant contract before implementation. |
| In-game review prompt | **Pending H5 verification.** [Review guide](https://developer.taptap.cn/docs/sdk/review/guide/) describes native APIs; developer review-list/like/reply MCP tools do not expose a H5 player review SDK. Do not invent `tap.openReview`. |

Supported official guides are **API evidence**, not configured status for a particular game. Unverified support stays `pending_verification`; use `unsupported` only with explicit current evidence. Do not add local achievements, redemption logic, check-in or purchases as silent substitutes. For reliability and acceptance recipes read [H5 contracts](h5-reliability.md).

## Independent official MCP dependency

Follow [upstream refresh](upstream-tools.md). Use the currently enabled registry first. If absent, consult the official setup and current [package README](https://github.com/taptap/instant-games-open-mcp) for Node requirements and the client's configuration format. `assets/taptap-mcp.example.json` is a credential-free **generic MCP JSON example**, not a drop-in format for every client. Replace its workspace placeholder with this game's absolute directory; on Windows follow the client/upstream launcher guidance if `npx` resolution fails. Do not install or alter global client configuration just to update this Skill.

The upstream npm command is `npx -y @taptap/instant-games-open-mcp`; compare the installed package/version with current upstream and record the tested revision in game evidence. OAuth device authorization belongs to the user; keep tokens and account cache outside the repo and frontend. Reconnect/restart the client's MCP session and rediscover tools after installation/update. Never vendor official server/SDK code into this Skill or mix it with Maker MCP.

Before app-dependent actions call `get_current_app_info`. If no app is selected, `list_developers_and_apps`, display choices and let the user select, then `select_app`. If selected identity conflicts with the target, resolve it before writes. Existence of a selected app does not authorize changing it. Generic Skill maintenance needs none of these scoped operations.

For an authorized upload: verify identity and build directory → `prepare_h5_upload` → show its actual app/directory summary and obtain the required explicit confirmation → `upload_h5_game` using its current schema. Keep review submission and publication distinct; never claim them from a prepared upload or QR preview. Do not auto-refresh inactive ads or create/switch applications while merely researching.
