---
name: observability
description: Add or review quiet, useful logging, metrics, tracing, error handling, alerts, and audit events. Use when diagnosing visibility gaps or instrumenting a changed operation with configurable detail and bounded overhead.
license: MIT
---

# Observability

Start with the question someone must answer: what failed, why is it slow, who changed it, or when must we act? Inspect existing instrumentation and the operation's ownership. Reuse the installed logger, error types, context propagation, and deployment controls. A local tool does not automatically need a collector or dashboard.

Read only the relevant language reference: [Rust](references/rust.md), [Swift](references/swift.md), [TypeScript](references/typescript.md), [Python](references/python.md), [Zig](references/zig.md), [Go](references/go.md), [C](references/c.md), or [C++](references/cpp.md). Match APIs to the project's actual versions. For delivery, sampling, audits, or alert design, consult [operational policy](references/operations.md).

## Add the smallest useful signal

- Record an operation's actual terminal outcome once where useful. Include stable event/operation names, outcome, duration, and available correlation. Avoid every function entry, item, polling tick, and successful subcall. Do not manufacture trace IDs for unrelated work.
- Propagate typed failures and useful causes. One handling boundary owns the error report; intermediate layers add context without duplicate stack traces. Expected misses, recovered retries, and intentional cancellation need their own semantics.
- Use low-cardinality outcome counters and duration distributions for aggregate health. Keep user IDs, full URLs, request IDs, and error messages out of metric labels. Trace meaningful I/O and asynchronous boundaries when they answer a question.
- Allowlist bounded fields. Exclude secrets, payload dumps, raw query strings, and arbitrary object/error serialization. Check error text too. Redaction is a second defense, not permission to collect everything.

## Control detail and cost

The executable owns sinks, severity/component controls, sampling, and lifecycle. Libraries use those facilities. Default to quiet output; allow scoped diagnostic detail through supported configuration. Say whether a change needs restart. Temporary debug settings should expire. Display filters, runtime filtering, and instrumentation removed at compile time are different controls.

Guard expensive debug-only preparation before computing it. Keep queues, batches, event sizes, retries, and shutdown flushing bounded. Define drop or backpressure behavior and expose lost diagnostic records without recursive failure logging. A broken exporter must not consume unbounded resources or stall unrelated work.

Required audit events have an independent policy: actor, action, target, time, outcome, correlation, access, retention, integrity, and behavior on persistence failure. Diagnostic verbosity and sampling must not disable them. Queue acceptance or a successful flush alone does not prove durable storage. Add durable delivery only when the actual contract requires it.

Page for actionable user harm or imminent irreversible loss. An ERROR record alone is not a paging policy. Reuse meaningful SLOs, grouped alerts, owners, and runbooks; account for missing data, low traffic, and recovery. Avoid an alert for every metric.

## Verify the signal

Exercise the changed operation and a few relevant failures. Check useful correlation, one owning error report, redaction, level controls, and required audit output. Probe exporter outage or saturation when delivery code changed. Measure hot-path overhead when relevant. Keep focused regression tests for concrete contracts; do not multiply levels, sinks, and failures into a matrix. Report observed behavior, cost evidence, and gaps.
