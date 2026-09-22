# Adding and maintaining a platform

A platform profile connects the shared workflow to one specific publishing product. Keep it focused on the decisions needed to adapt a game: supported runtime, packaging, capabilities, listing fields and setup steps.

1. Identify the exact H5/native product and official documentation, SDK and creator console. Similar platform names are not interchangeable.
2. Add focused English and Chinese references with official links and dates. Describe initial preparation, required configuration, optional capabilities, packaging and the host test route. Keep unknown requirements explicit.
3. Add known listing and package limits to the shared JSON files. Separate recommendations from hard limits; never reuse another platform's limits. Extend a helper only when a new format or behavior requires it.
4. Register the profile in `SKILL.md` and the README platform tables. Add official tool sources to `assets/platform-sources.json`. Describe which inputs are public IDs, account access, permission status or secure server configuration.
5. Keep commands portable across macOS and Windows. Follow the project's Android target and independently check host-engine constraints.
6. Check the workflow with a small reproducible project: missing configuration must not block independent preparation, originals and saves remain intact, and unsupported capabilities are reported clearly. Run relevant helper tests when executable behavior changes.

Use official platform Skills, CLI tools and MCP integrations through [upstream tools](upstream-tools.md), without maintaining modified copies here. A platform reference cannot authorize uploads, account changes or new paid services.

Maintain English and Chinese together, use one shared rule source, and record user-visible changes in `CHANGELOG.md`. Keep private project history and project-specific IDs, values and assets out of the Skill. See [CONTRIBUTING](../CONTRIBUTING.md) for the contribution process.
