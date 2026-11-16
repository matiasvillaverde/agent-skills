# Attribution and local adaptation

Reviewed and adapted on 2026-11-13 for the personal developer skill library.
These are local adaptations, not upstream endorsements. Original source licenses
are included; supplementary primary documentation is linked where used.

- [affaan-m/ECC / skills/benchmark-optimization-loop](https://github.com/affaan-m/ECC/blob/d2ef2680594f9a17526a6e1a2e18b3d242c5d17b/skills/benchmark-optimization-loop/SKILL.md), MIT.
- [addyosmani/agent-skills / skills/performance-optimization](https://github.com/addyosmani/agent-skills/blob/301b02b12bff98e4688e6984af6556802322bbde/skills/performance-optimization/SKILL.md), MIT.
- [steipete/agent-scripts / skills/instruments-profiling](https://github.com/steipete/agent-scripts/blob/d210c0a77c8f9ae5e1d939b13238a75e87cdb69a/skills/instruments-profiling/SKILL.md), MIT.

Measured baseline and profiling reference; bounded work, noise-aware comparison, no mandatory exhaustive benchmark suite.

No upstream executable helpers, hooks, orchestration, package installation or automatic
updates are included. Supporting references are local synthesis, not copied manuals.

2026-11-15: added original native-profiling guidance for Rust/Zig/C/C++, grounded in
current platform, compiler and hardware documentation. Community method comparisons and
rejected advice are recorded in the dated shared research; no additional upstream code
or expressive text was imported.

2026-11-15 follow-up: original Linux-specific reference adds ELF/symbol handling, x86-64/ARM64,
cgroups/VMs, scheduler pressure, NUMA, allocator visibility and restricted-tool fallbacks.

2026-11-15: added optional routing to the original perf-go runtime/service specialist.

2026-11-15: added optional routing to original perf-node, perf-python and perf-database
specialists. The generic measurement method and existing attribution remain unchanged.

2026-11-15 follow-up: replaced the database umbrella route with perf-postgres,
perf-clickhouse, perf-sqlite and perf-swiftdata at the owner's request. The engine research
and qualified references are retained in the respective original specialists.
