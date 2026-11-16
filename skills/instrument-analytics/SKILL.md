---
name: instrument-analytics
description: Add or review product analytics and OpenTelemetry instrumentation with a small provider boundary. Use for meaningful event tracking, funnels, identity, or agent-harness outcome, latency, resource and cost signals.
license: MIT
---

# Instrument analytics

Start with the decision the measurement should support. Inspect the changed flow, existing event definitions, telemetry, dashboards, privacy contract and installed SDK versions. Keep the requested scope; reuse working instrumentation. An analytics request does not authorize a new vendor account, destination, identity join or broader collection.

Separate product events, operational telemetry, evaluation evidence and required audit records. They answer different questions and have different delivery, retention and access requirements. Sampled traces cannot supply complete conversion counts; best-effort analytics cannot replace a transaction or audit ledger.

## Choose useful facts

Write the smallest tracking-plan delta in the existing owner: question, event meaning, authoritative trigger, allowed properties, identity unit and useful query. State the numerator, denominator and observation window for rates. Prefer delivered value, activation, time to value and meaningful return use over raw activity counts. There is no required event catalog or event quota.

Record completion where its outcome becomes authoritative. Keep attempts separate when they explain abandonment or failures. Do not infer success from a click, accepted request or success-page view. Preserve logical event identity through retries; choose one producer per fact. Read [product events](references/product-events.md) for funnels, schema evolution, deduplication, offline delivery or identity changes.

## Keep the boundary small

Use a narrow application-owned typed event function or interface, one adapter for the selected provider, and a cheap disabled/recording sink where needed. Reuse an existing equivalent. Prefer ordinary functions, enums and dependency injection already used by the language/project. Keep one event-schema source of truth; avoid a parallel YAML catalog, generated framework or generic plugin bus without a concrete need.

Put provider imports, property mapping, consent, retries and network delivery in that boundary. Emit from an existing use-case completion, established event consumer or lifecycle hook. Keep pure domain calculations free of telemetry dependencies; a clear semantic call at an application boundary is preferable to hidden inference or duplicated business rules. Do not add domain-event infrastructure solely to hide analytics calls.

Use OpenTelemetry's API directly for traces, with SDK/exporter configuration at application startup. OTel already supplies the tracing abstraction. Reuse automatic instrumentation and add only missing meaningful boundaries. Read [OTel](references/otel.md) for propagation, sampling, exporter lifecycle and standards compatibility. For model/tool loops, read [agent harnesses](references/agent-harness.md); an API success or final answer does not establish task success.

## Bound collection and overhead

Allowlist bounded fields before recording. Exclude raw user content, prompts, responses, tool arguments/results, secrets, full URLs and arbitrary object/error dumps by default. Respect the product's actual consent, identity, deletion and retention rules; pseudonymous identifiers still require care. Do not enable autocapture, session replay or identity enrichment incidentally.

Configure collection enablement, trace sampling, diagnostic detail and payload limits independently where useful. Use existing configuration conventions rather than inventing a telemetry control framework. Disable expensive preparation when unused. Bound queues, batches, bytes, retries and flush deadlines; expose dropped data without recursive logging. Best-effort telemetry failure must not fail or indefinitely delay the business operation. Durable delivery belongs only to an explicit requirement. Keep metric dimensions bounded and IDs out of labels.

## Verify what the signal means

Use the existing test framework and a recording sink/in-memory exporter. Select cases that exercise distinct risks: committed outcome versus rollback, retry deduplication, consent/account switching, context across async work, cancellation/stream completion, or an unavailable exporter. Inspect actual permitted transport when SDK behavior matters. Avoid combinatorial matrices, implementation-shaped tests and parameterized tests unless the project requires them or they materially improve clarity.

Check a representative query against known outcomes, including its denominator and missing data. Measure added CPU, allocations, memory, request count or payload volume when the changed path warrants it. Keep only tests that protect an important contract. Report the event/query changes, collection controls, observed evidence and gaps; instrumentation alone does not prove product or agent quality.

Reviewed inspiration and licensing: [NOTICE.md](NOTICE.md).
