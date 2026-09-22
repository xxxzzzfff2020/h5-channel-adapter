# Contributing

[简体中文](CONTRIBUTING.zh-CN.md) · [Back to the Skill](README.md)

Help make H5 publishing easier across platforms. Useful contributions include new platform profiles, updated listing requirements, reusable integration fixes, portable helper improvements and clearer examples.

The repository is public and welcomes issues and pull requests. An open-source license has not yet been selected.

## Start with a concrete change

Open an issue describing the platform, the task you want to complete and the missing or incorrect behavior. For rule changes, link the current official documentation or provide a redacted form excerpt and its date. For bugs, include a small reproducible example, operating system and relevant tool versions.

A discussion is useful before adding a new platform or a substantial dependency. Small fixes can go directly to a pull request.

## Where changes belong

| Change | Location |
| --- | --- |
| Agent purpose and routing | `SKILL.md` |
| Platform or workflow guidance | `references/` and `references/zh-CN/` |
| Shared listing and package limits | `assets/material-rules.json`, `assets/package-rules.json` |
| Official dependency links | `assets/platform-sources.json` |
| Reusable commands | `scripts/` |
| Helper behavior tests | `tests/` |

For a new platform, follow [extension guidance](references/extending.md). Use official platform Skills, CLI tools and MCP integrations as upstream dependencies. Contribute integration guidance here rather than a modified copy of their Skill.

## Keep contributions reusable

- Update English and Chinese together; keep numeric rules in the shared JSON rather than duplicating them in code.
- Distinguish required limits from recommendations and project preferences. Leave unknown limits explicit.
- Use generic examples. Keep game source, commercial artwork, private conversations, account IDs and credentials out of this repository.
- Write portable paths and commands for macOS and Windows. Keep project-specific choices in the game's own configuration.
- Preserve the original game, existing saves and previous packages. Content reduction requires the user's selected plan.

## Check the change

For documentation changes, review links and the corresponding translation. For helper or rule changes, first run the image/copy and package checks with Python 3.9+; FFmpeg is not needed:

```sh
python3 tests/no_ffmpeg.py
```

For video changes, also run `python3 tests/smoke.py` with ffmpeg/ffprobe available. On Windows PowerShell, replace `python3` with `py -3` or your verified `python` command. The tests generate temporary synthetic assets. Add focused cases when behavior changes; don't add tests that only match document wording.

The [CI template](ci/validate.github.yml) can run the same helpers on macOS and Windows when a maintainer enables it as `.github/workflows/validate.yml`.

## Submit a pull request

Explain the user-facing problem, the change and how you checked it. Include official references for changed platform requirements and identify anything that still needs a real host or device check. Update `CHANGELOG.md` for user-visible behavior; maintainers assign release versions.

Do not upload a complete private game as a reproduction. A minimal synthetic fixture or redacted example is easier to review and maintain.
