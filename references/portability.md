# macOS and Windows portability

Keep the same Skill, rules and Python helpers on both systems. Paths come from the user's project/Skill location; never require the author's home directory, `/tmp`, Homebrew or a macOS shell.

## Runtime discovery

- Detect OS and shell. On macOS, locate `python3`. On Windows PowerShell, use `Get-Command python, py -ErrorAction SilentlyContinue`; check the actual interpreter with `python --version` or `py -3 --version`. The Windows Store alias is not proof that Python is installed.
- Helpers require Python ≥3.9, standard library only. Image/copy workflows and package checks do not require FFmpeg. Inventory reads PNG/JPEG/WebP headers by default and does not probe audio/video. `--no-probe` also disables image metadata. Only selected audio/video work discovers ffprobe/ffmpeg: `--probe-av` enables inventory probing; `processing.video: true` enables material-video checks. Video editing and the optional full media tests use ffmpeg.
- Only check/install a media tool when the selected task needs it. Prefer installed/bundled runtimes. If missing, use the user's approved package manager or official distribution with the correct OS/architecture; do not run macOS `brew` or Unix curl-pipe-shell installers on Windows. Some official platform tools offer a Windows executable/PowerShell installer instead; fetch the current upstream instructions.
- Quote paths containing spaces or Chinese characters. Use `pathlib` and argument arrays, not shell-concatenated paths, Unix-only copy commands or mandatory symlinks. Use explicit UTF-8 for stored text and subprocess JSON. Windows package paths must not use reserved filename characters or device names.

## Equivalent helper commands

macOS/zsh (replace paths):

```sh
python3 "/path/to/skill/scripts/inventory_project.py" "/path/to/game" --output "/path/to/evidence/inventory.json"
python3 "/path/to/skill/scripts/verify_materials.py" "/path/to/materials/manifest.json" --report "/path/to/evidence/materials-check.json"
```

Windows/PowerShell (use `python` instead if that is the verified interpreter):

```powershell
py -3 "C:\Tools\h5-channel-adapter\scripts\inventory_project.py" "D:\Games\My Game" --output "D:\Evidence\inventory.json"
py -3 "C:\Tools\h5-channel-adapter\scripts\verify_materials.py" "D:\Materials\manifest.json" --report "D:\Evidence\materials-check.json"
```

Manifest paths may use portable forward slashes relative to the manifest. Delivery outputs must stay in its directory tree. JSON serialization handles Windows backslashes; do not build JSON by hand with unescaped paths. Existing reports are not overwritten: choose a new evidence filename.

## Builds, browsers and acceptance

Respect the game's actual stack and lockfile. Detect Node/npm if needed and use the platform's documented build command. Never assume a Mac-only developer tool is available; report a platform's tooling restriction separately from what can be built locally.

Use available isolated browser automation or a user-authorized host preview. Do not require the Codex desktop popup API, a particular browser driver or native OS automation on all agents. Fall back to text questions and explicit verification gaps when those capabilities are unavailable.

Run `python3 tests/no_ffmpeg.py` for image/copy checks; it removes media tools from subprocess PATH. Run `python3 tests/smoke.py` only for the full media suite with FFmpeg. On Windows use `py -3` or the verified interpreter. The CI template includes both suites; helper checks do not replace host or device testing.
