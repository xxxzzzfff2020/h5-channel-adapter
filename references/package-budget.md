# Game-package budgets and user-selected reduction

Check package size twice: the frozen TapTap artifact at intake, then each actual channel artifact after building. Use `assets/package-rules.json` as the dated limit registry. Current known snapshots: Xiaohongshu ZIP 10 MB; Bilibili ZIP/HTML 140 MB; Xingxia existing-game Track A 50 MB from official docs. The later workshop-managed form does not establish a new upload limit. 233/4399 package limits remain unknown. Never confuse a promotional-video limit with the game-package limit. MB is interpreted conservatively as decimal bytes; refresh the real form at use time.

## Measure before asking

Use the existing authoritative TapTap ZIP when available; otherwise build an isolated baseline with the existing build process. Do not compare the entire source folder or a material archive to an upload limit. Record source version/hash and actual artifact bytes. Each target may bundle differently: an initially small package can grow, and an initially large one may fit after packaging. Recheck each final artifact.

```sh
python3 <skill-dir>/scripts/check_package_budget.py <TapTap-game.zip> --channels xiaohongshu bilibili-toy xingxia --report <new-budget-report.json>
python3 <skill-dir>/scripts/check_package_budget.py <channel-game.zip> --channels xiaohongshu --stage candidate --report <new-final-budget-report.json>
```

On Windows use the verified `py -3` or `python` interpreter and quoted paths. The helper is read-only, has no ffmpeg dependency and never changes game content. It reports actual archive bytes, known/unknown limits, overage, compressed/uncompressed category totals, largest entries and bounded embedded-media markers. Categories cannot distinguish music from sound effects, optional from essential videos, or all inline/base64 payloads; inspect source/build code before proposing removals. No full CRC, runtime or upload acceptance is implied.

Exit codes: 0 = within known limits; 1 = over a known limit, user decision required; 2 = invalid input/candidate; 3 = incomplete because a limit is unknown. Do not retry exit 1/3 as transient failures or label an unknown limit “unlimited”.

## Required decision when over limit

As soon as a selected platform is over its known limit, notify the user and ask which plan to use **before applying content reductions**. Do not wait for AppID. Finish other selected platforms and independent materials while waiting. Respect an already explicit, still-applicable per-channel choice; never infer it from silence, a default selection or another channel's decision.

Show current size, limit, overage, main contributors, and realistic plans with evidence-based estimated savings and gameplay effects. A scratch measurement build may estimate savings without changing the authoritative source. Do not claim an estimate guarantees compliance. Offer only relevant plans, for example:

- Preserve all functions: remove proven unused/duplicate runtime files and optimize encoding/compression within agreed quality limits. ZIP-recompression of already-compressed media may save little.
- Remove background music, retaining sound effects, if the user selects this precise scope.
- Remove optional in-game video playback, while preserving essential tutorials/story by an agreed replacement.
- Combine specific approved changes, or defer this platform and keep the full version elsewhere.

If the selected plan still exceeds the limit, show the new measured result and ask about the next reduction; do not escalate to additional removals automatically. Never move Xiaohongshu resources to a remote CDN, because its container is offline. For other platforms remote hosting needs verified platform support and user scope, not an assumed size workaround.

## Execute a chosen removal completely

Work only in that channel's independent source. Record the choice, affected features/resources, before/after hashes and bytes, and retain the original TapTap source and previous package.

Removing music/video means updating assets **and** imports, manifests, preload/progress totals, decoders/players, playback triggers, lifecycle/ad-resume hooks, scene scripts, settings toggles/sliders, menus, help text and related fallback branches. Do not merely delete files or hide a settings row. Retain sound effects if only BGM was removed. Required gameplay/story/tutorial dependencies need a reviewed alternative, not silent omission.

Keep old saves readable: obsolete media preferences may be tolerated/ignored, but do not erase progression or rewrite unrelated fields. Test fresh and old saves, startup, navigation, settings, relevant scenes, background/foreground and ad return where applicable. Confirm no missing-file requests, dead buttons, silent waits, stale claims or unnecessary bundled media remain, then check the real rebuilt ZIP size.

**Listing promotional media is separate.** Removing in-game videos does not remove upload-page promotional videos or the 233/4399 promotional+gameplay composite requirement. Update screenshots/copy to reflect the selected channel's actual features; do not claim music, video or cloud features that were disabled.
