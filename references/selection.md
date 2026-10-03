# Source, targets and capability selection

Use `assets/capabilities.json` as the shared option catalog. Selection is project scope, not proof of SDK support or permission to publish. Preserve answers in the game's existing delivery directory as `channel-selection.json`; never commit a real game's answers or account details to this Skill.

1. Inspect the actual source directory, runnable entry/build, Git changes and existing SDK hooks. Choose exactly one `source.kind`: `generic_h5`, `taptap_h5`, `other_platform_h5`. A previous platform port is valid source when explicitly chosen; freeze it before copying. Maker/UrhoX Lua requires a separate conversion project, not relabeling as H5.
2. Select one or more targets: TapTap H5, 233, 4399, Xiaohongshu MiniTool, Bilibili TOY, Xingxia. TapTap → TapTap means incremental maintenance of that channel; preserve its namespace, IDs, assets and old packages. Do not copy over the source or recreate an existing app.
3. For **each selected target**, collect a separate feature list. Show ads, identity, local/cloud saves, leaderboard, achievements, gifts/redeem, share, vibration, diagnostics, multiplayer and review prompt with that platform's evidence/gaps. The catalog lists requests users may make; it does not claim all platforms support all entries. Unsupported and unverified selections remain visible gaps, never fabricated implementations. An empty list is an explicit projects-only capability choice, not a missing answer.
4. Separately select game-logic work (offline progress, check-in, music, SFX, font/performance settings) and listing materials per target. These are not platform APIs. Existing game behavior must remain intact even if no *new work* on it is selected. Never remove music because listing-video work was not selected.
5. Use genuine multiselect if available. The current suggested-answer popup is single-select: use a numbered list accepting multiple numbers, then show a compact source/target/per-target-feature/material recap for explicit confirmation. Do not present a single-select popup as checkboxes. Reuse an already explicit, unambiguous user scope; do not ask them to answer twice. Timeout/default is no answer; only read-only inventory proceeds while required choices are missing.

Example text interaction: `Targets: 1 TapTap, 2 233, 3 4399, 4 MiniTool, 5 TOY, 6 Xingxia. Reply with several numbers. Then choose features separately for each selected target; reply “none” for no new integration.` Explain uncertain features before the final recap.

## Persist and resume

Prepare answers in the game delivery directory using this shape (example only, not user consent):

```json
{
  "confirmed": true,
  "source": {"kind": "generic_h5", "path": "<absolute-source-directory>", "inspection": "Verified build entry and existing hooks", "existing_integrations": []},
  "targets": ["taptap", "4399"],
  "features": {"taptap": ["local_save", "cloud_save"], "4399": ["ads"]},
  "materials": {"taptap": "projects_only", "4399": "images_copy"},
  "game_logic": []
}
```

`confirmed: true` records a real answer already received; the agent must not manufacture it. Source inspection is a human/agent evidence statement, not a filesystem check performed by the helper.

```sh
python3 <skill-dir>/scripts/selection.py create <answers.json> --output <delivery-dir>/channel-selection.json
python3 <skill-dir>/scripts/selection.py validate <delivery-dir>/channel-selection.json
python3 <skill-dir>/scripts/selection.py plan <delivery-dir>/channel-selection.json
```

Windows: use `py -3` or the verified Python executable. The helper only validates/persists scope; it never creates game directories, changes integrations or invokes platform tools. It rejects missing/duplicate/unknown choices, activation of an unselected feature and overwriting existing records. `plan` includes selected targets/features only. Use its output to constrain every copy, material, SDK and package step.

| Status | Meaning / next step |
| --- | --- |
| `not_selected` | No new integration work; preserve existing game behavior. |
| `pending_verification` | Selected, but verify current H5 API/configuration/dependencies before integrating. |
| `unsupported` | Current evidence says unavailable for this product/route; report the gap, do not integrate. |
| `configured` | Document current configuration and implementation evidence; runtime, device and release remain separate. |

Update a selected feature's status and `evidence` in this same file after verification; run `validate` before resuming. Both `configured` and `unsupported` require a dated reference or local evidence path. Unknown H5 support stays pending, not unsupported. `plan.next` distinguishes verification, reporting a gap and validating configured work. A chosen feature never silently enables dependencies: explain unresolved dependency requirements, reuse existing authorized integrations or obtain the missing scope. Offline work can continue while one remote feature is pending.
