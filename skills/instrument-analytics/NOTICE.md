# Source and adaptation notice

Reviewed 2026-11-13. Original local synthesis for the shared personal developer
library. The following MIT-licensed skills informed selected ideas; this is not an
unmodified upstream installation or an endorsement by those authors.

| Source at reviewed commit | Ideas retained | Deliberate changes |
| --- | --- | --- |
| [Corey Haines analytics](https://github.com/coreyhaines31/marketingskills/blob/1f837447b20bb6f0e72d87b80ece1c221c362c7d/skills/analytics/SKILL.md) | Decision-first tracking, metric windows, useful validation | No mandatory platform/catalog; authoritative outcomes instead of success-page inference |
| [Accoil tracking plan](https://github.com/Accoil/product-tracking-skills/blob/91ae6a6267804e83a792b477f348d00c51d1a6cf/skills/product-tracking-design-tracking-plan/SKILL.md) | Sparse events, canonical emission point, current-state truth | No required `.telemetry` pipeline, CDP, scheduled snapshots or assumed identity joins |
| [Clamp event schema](https://github.com/clamp-sh/analytics-skills/blob/b9e06c5131a6060114e68893bc34fc77b65a9552/skills/event-schema-author/SKILL.md) | Typed contracts and a small provider interface | Reuse the existing schema source; no mandatory YAML, code generation or CLI |
| [PostHog product analytics](https://github.com/PostHog/skills/blob/f87c8afca37db929d41461026f35388cef7306e1/skills/omnibus/instrument-product-analytics/SKILL.md) and [tracing](https://github.com/PostHog/skills/blob/f87c8afca37db929d41461026f35388cef7306e1/skills/omnibus/instrument-tracing/SKILL.md) | Existing integration discovery, OTel API/export separation, useful boundaries | No provider setup, fixed file quota, extra destination, proxy or identity linkage by default |
| [Honeycomb GenAI instrumentation](https://github.com/honeycombio/agent-skill/blob/6bb09279fc3fb69abf113228be939dbb929e34f1/honeycomb/skills/otel-genai-instrumentation/SKILL.md) | Run/model/tool structure, streaming lifecycle, usage and evaluation linkage | Check current conventions; no unconditional tool payloads, invented conversation IDs or per-request synchronous flushing |

The shared [LICENSE](LICENSE) preserves their MIT copyright notices and permission
text. Instruction prose and references were written locally; upstream executables,
hooks, integration packs and workflow dependencies were not copied.

The references cite the authoritative OTel, W3C and CloudEvents standards and
provider documentation for behavior that is provider-specific. Architecture choices
are local recommendations. The dated review does not freeze future SDK support;
inspect the installed versions before applying exact conventions or controls.
