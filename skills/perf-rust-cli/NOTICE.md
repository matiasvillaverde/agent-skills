# Source and adaptation notice

2026-11-15: linked the optional low-level `perf-rust` specialist while retaining the
whole-command, output and process-lifecycle contract below.

Reviewed and modified on 2026-11-13 for the shared personal skill library.
Original local instruction prose informed by the following pinned sources; this
is not an unmodified upstream installation or an upstream endorsement.

- [Dankosik/rust-cli-skills / skills/rust-performance](https://github.com/Dankosik/rust-cli-skills/blob/aafca337dece65f312faaecd0fe9ee1c81f755df/skills/rust-performance/SKILL.md), MIT.
- [Dankosik/rust-cli-skills / skills/rust-memory](https://github.com/Dankosik/rust-cli-skills/blob/aafca337dece65f312faaecd0fe9ee1c81f755df/skills/rust-memory/SKILL.md), MIT.
- [Dankosik/rust-cli-skills / skills/rust-io](https://github.com/Dankosik/rust-cli-skills/blob/aafca337dece65f312faaecd0fe9ee1c81f755df/skills/rust-io/SKILL.md), MIT.
- [Dankosik/rust-cli-skills / skills/rust-processes](https://github.com/Dankosik/rust-cli-skills/blob/aafca337dece65f312faaecd0fe9ee1c81f755df/skills/rust-processes/SKILL.md), MIT.
- [Dankosik/rust-cli-skills / skills/rust-concurrency](https://github.com/Dankosik/rust-cli-skills/blob/aafca337dece65f312faaecd0fe9ee1c81f755df/skills/rust-concurrency/SKILL.md), MIT.
- [Dankosik/rust-cli-skills / skills/rust-cli-testing](https://github.com/Dankosik/rust-cli-skills/blob/aafca337dece65f312faaecd0fe9ee1c81f755df/skills/rust-cli-testing/SKILL.md), MIT.

Changes:
- Consolidate performance-relevant Rust CLI guidance into one standalone skill.
- Measure startup/first output/end-to-end work with version-aware timing, bounded streams/children and observable CLI correctness.

The applicable upstream permission and copyright text is retained in [LICENSE](LICENSE).
No upstream executable, plugin, hooks, bundled profiler or missing companion skill is included.
Platform tools are runtime requirements to inspect when applying the skill.
