# Source basis

Original instructions, reviewed 2026-11-15. Community sources informed decisions; no upstream
runtime, scripts or templates are bundled. Source review is not a claim of measured efficacy.

- [OpenClaw behavior-validator](https://github.com/openclaw/agent-skills/blob/91bf14bc19e8e4c1d5ba9a11c3cfb753dc759711/skills/behavior-validator/SKILL.md): contract-only exploration, varying fixtures and real effects. A prompt/work directory does not enforce isolation.
- [Vercel dogfood](https://github.com/vercel-labs/agent-browser/blob/53384771fbafc261ba67608ac806dd5aa70b84f0/skill-data/dogfood/SKILL.md): evidence captured during browser exploration. Omit bug quotas, obligatory videos and dismissal of intermittent failures.
- [Exploratory testing](https://github.com/bdfinst/agentic-dev-team/blob/6ab4e9c9de63cc05dc165f9a08c8f832326304d2/plugins/dev-team/skills/exploratory-testing/SKILL.md): adaptive, bounded experiments. Omit fixed probe quotas and automatic mutation replay.
- [Apple XCTest](https://developer.apple.com/documentation/xctest): UI and performance testing; use the installed Xcode's supported commands and device capabilities.
- [MCP specification](https://modelcontextprotocol.io/specification/latest), [legacy lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle), [2026 versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning), [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools): version-specific discovery, capabilities and result semantics. Recheck the target revision when applying; do not force an upgrade as part of testing.
- [TestPrism / TestHelix](https://arxiv.org/html/2610.12289v2): separate exploration and assertion adjudication. Benchmark preprint; not a product-reliability guarantee.
