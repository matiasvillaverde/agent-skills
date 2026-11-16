# Source basis

Original instructions, reviewed 2026-11-15; no upstream runtime or scripts bundled.

- [gstack functional QA](https://github.com/garrytan/gstack/blob/0326b144af36676d599dcf63a9fad9a870d22ed6/qa/sections/system-functional.md): documented contracts, durable effects and explicit blocked/inconclusive coverage.
- [Real-infrastructure testing](https://github.com/pedro-angel/agent-methodology/blob/c0f65bc53c917d50786f8e57d3a889abcdb44087/skills/battle-testing-on-real-infra/SKILL.md): cross-process guarantees and tested artifact identity. Omit automatic provisioning and raw evidence in Git.
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) and [sampling](https://opentelemetry.io/docs/concepts/sampling/): correlated operations and limits of incomplete observations.
- [Apple performance analysis](https://developer.apple.com/documentation/xcode/improving-your-app-s-performance): select capture for the actual device/build and workload; consult installed Instruments/xctrace help.
- [Chrome memory problems](https://developer.chrome.com/docs/devtools/memory-problems): retained resources versus process memory growth.
- [MCP specification](https://modelcontextprotocol.io/specification/latest): choose the actual supported revision, transport, result and extension contracts.
- [Toxiproxy](https://github.com/Shopify/toxiproxy): controlled TCP faults in testing/development. Optional tool, not an installation requirement.

Sources describe capabilities and practices; their existence does not establish a passing run,
complete telemetry or a universal performance budget. Refresh version-specific APIs before use.
