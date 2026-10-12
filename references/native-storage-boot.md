# Native storage boot and recovery

Use for selected native-storage adaptation, especially Xiaohongshu. These are engineering safeguards and an exception-test matrix, not a shipped storage implementation. Preserve the game's keys, schemas, progression and existing recovery policy. Verify the current [official API contract](https://miniapp-sandbox.xiaohongshu.com/minitool/doc) before implementing platform code.

## Establish storage state before parsing or writing

- Obtain authoritative native key inventory and validate its response before interpreting an absent key. Inventory/read failure means unknown, not an empty store. A missing-key sentinel is not a valid recovery journal.
- Only tolerate a listed empty recovery marker (empty string, JSON null or empty object) when verified inventory proves there is neither a primary save nor recovery backup. This is a narrowly selected fresh-store policy; preserve genuine corrupt main/journal/backup data and expose retry/recovery rather than deleting it.
- A valid existing native save does not need optional browser migration. Unavailable localStorage getters, enumeration or reads must not block a confirmed fresh/valid native store. If migration starts, gather and validate the complete candidate before committing; partial reads cannot produce a partial save. Retain originals and channel isolation.
- Unchanged startup recovery is read-only. Do not write an unchanged main/journal solely because boot succeeded. Treat Promise results and callback results according to the actual SDK contract; a returned request handle is not response data. Use one settlement path and invoke each write once, including mixed/duplicate notifications.
- On writes, validate acknowledgment and readback. Keep the latest pending progression on failure/mismatch, and never claim saved success from changed memory alone. Retry remains available without clearing keys or losing pending progress.
- After a genuine read failure, an explicitly player-selected temporary session may allow play. It performs no persistent/native writes, no migration or automatic backup; its UI must explain that progress is unsaved. Merely changing its label is insufficient: all write paths must be isolated.

The current Xiaohongshu contract separates Promise calls from callback calls (callbacks return undefined); `getStorage` returns data and `getStorageInfo` returns key inventory. Keep encryption options consistent and validate current version/method availability. Observed legacy request handles and mock sentinel shapes are compatibility cases, not extra official response guarantees.

## Exception tests on the actual target implementation

Replace only external SDK, browser storage, clock and faults; execute the game's real boot, migration, recovery and save code. Assert writes, retained bytes, UI claims and pending progression, not merely a fake SDK's return value.

| Input / fault | Required observation |
| --- | --- |
| Fresh native inventory; browser getter blocked | Play can start; no mandatory migration or boot write |
| Valid native save; browser storage unavailable | Native progress retained; browser never required |
| Inventory failure or malformed inventory | State unknown; no empty initialization/migration |
| Missing response data with a listed save | Read failure retained; no fabricated empty save |
| Empty listed marker; no main/backup | Selected fresh-store policy only; unchanged boot writes zero |
| Empty marker with an existing main/backup | Do not discard the existing data |
| Corrupt main, journal or backup | Original bytes retained; useful phase/version error and retry |
| Browser migration partly readable | No partial native commit; original browser data preserved |
| Interrupted transaction with validated recovery | Follow existing transaction recovery; no duplicate credit |
| Callback-only API / request handle | Await the callback; handle is not response data |
| Promise plus duplicate callback/error | One settlement; one intended write |
| Write failure or mismatched readback | Unsaved status; latest pending progression retained |
| Temporary session after read failure | All persistent writes zero; no saved/backup claim; retry available |
| Previous package fails on a real phone | New isolated passes do not certify the new phone/package |

Record source version/hash, actual tested layer and bounded phase diagnostics in project evidence. Real iOS startup failure for an older build remains real evidence; a later mock suite cannot close it. Bind platform simulator and Android/iOS retests to the latest exact package before claiming native acceptance.
