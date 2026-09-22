# Guided selection and missing configuration

Use available conversation questions, not a new website or approval system. If `request_user_input_async` is present, each suggested-answer question is single-select with free-text input. Never claim native checkboxes, treat a default as submitted, or infer consent from timeout. Follow the actual tool schema; use numbered text choices when no question tool is available.

## Select platforms

Only ask when the user actually requests adaptation and has not named targets. For the two case-backed channels, offer “233 + 4399”, “233 only”, “4399 only”. Other combinations can be typed. With more choices, group 2–3 platform-specific yes/no questions and label documentation-stage profiles accurately. “All supported” defaults to 233/4399. Do not silently include new platforms.

While waiting for a required selection, inventory source/assets read-only. Do not create unselected channel projects. If several source games are possible, offer known game names rather than guessing from a studio directory. Do not ask users to choose ordinary implementation details.

## Prepare and report

Create actual source projects, copy runtime assets, adapt/test, prepare listing copy and materials. First look for missing assets locally or capture them. Questions may ask for existing paths; text-only tools cannot request attachment uploads.

After phase one show each platform's source/material status, game ZIP and next action. Distinguish a ready local upload candidate, preparation awaiting required identity, a candidate with disabled pending capabilities, and missing materials/rules. A ZIP does not prove real SDK, device, review or release success.

## Collect only necessary fields

Provide the verified creation URL and ready-to-copy name/description/controls/images. For missing 4399 configuration ask AppID, ad status (enabled/pending/not requested) and save API status. Ask rank ID and score/order only if a leaderboard is in scope. Do not imply a positive status through default selections.

233 IAA has no frontend AppID argument. Xingxia injects runtime gameId and uses creator login only when needed. Xiaohongshu requires the current upload-page rewrite command. TOY uses creator login plus a verified slug/target ID when publishing/updating. Do not ask all platforms for an AppID/Secret questionnaire.

Accept a combined free-text answer, extract fields and resume without making the user repeat a form. Ask only about unresolved identity conflicts or real gaps. Server secrets belong in secure configuration, not chat forms or frontend files.

## Resume per channel

Persist selected platforms, non-secret IDs, permissions, candidate paths, gaps and next actions in existing delivery notes. Partial responses unblock ready channels. Pending capabilities may be safely disabled when allowed, but do not invent reward success or silently change product economics.

Do not recopy source, replace saves or remake unchanged materials just because the user returns later. Continue ordinary local steps without further approvals. For external writes, use the actual user's authorization and applicable platform workflow.

## Over-limit package question

Follow [package budgets](package-budget.md) immediately when a selected channel exceeds its limit. Show actual size/limit/overage and measured resource contributors; offer only feasible options (preserve content and optimize, remove BGM while keeping SFX, remove optional in-game video, an explicit combination, or defer). Wait for a specific choice before changing content. Reuse an already-authorized matching choice, never a default/timeout. The question is needed because reducing features changes the delivered game, not because ordinary local packaging requires approval.
