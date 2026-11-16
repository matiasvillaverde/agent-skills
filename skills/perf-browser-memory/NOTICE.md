# Source and adaptation notice

Reviewed and modified on 2026-11-13 for the shared personal skill library.
Original local instruction prose informed by the following pinned sources; this
is not an unmodified upstream installation or an upstream endorsement.

- [ChromeDevTools/chrome-devtools-mcp / skills/memory-leak-debugging](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/8ba2ac945ebaf1adb92208c29f3a30e73a920956/skills/memory-leak-debugging/SKILL.md), Apache-2.0.

Changes:
- Use available heap tools with lifecycle baselines, cleanup and retaining-owner evidence.
- No fixed repetition quota, automatic MCP installation, raw heap upload or blanket detached-node deletion.

The applicable upstream permission and copyright text is retained in [LICENSE](LICENSE).
No upstream executable, plugin, hooks, bundled profiler or missing companion skill is included.
Platform tools are runtime requirements to inspect when applying the skill.
