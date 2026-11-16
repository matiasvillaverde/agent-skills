---
name: verify-feature
description: Verify a completed feature through its real UI, CLI, API, job, or artifact. Check relevant edge cases, network failures, telemetry, request counts, and resource cleanup with a small, meaningful set of probes before claiming completion.
license: MIT
---

# Verify a finished feature

Read the request, changed behavior, owning project instructions, and existing evidence. State a short behavior contract: the user task, observable success, consequential failure, and how to distinguish real success from a success message. Confirm the intended build/process and environment. This is source-informed verification unless an evaluator actually worked independently without implementation access.

## Choose checks by risk

Use representative success and the few failure/boundary cases most likely to reveal a consequential defect. Select from these prompts; do not run the whole list or its Cartesian product:

| Changed behavior | Useful probes |
| --- | --- |
| Input or transformation | Empty/missing, malformed, one meaningful boundary, encoding/locale/time boundary when relevant; check the actual result. |
| Network or dependency | Offline/refused/interrupted connection, deadline, auth rejection, rate limit, malformed/empty response, or server failure that the path can encounter. |
| Mutation or persistence | Refresh/reopen, duplicate submission, retry after ambiguous completion, concurrent/stale update, partial write; confirm downstream state and no duplicated effect. |
| Async lifecycle | Cancel/dismiss/shutdown, late completion, reconnect, repeated start/stop; check cleanup and bounded outstanding work. |
| UI or artifact | Real interaction, keyboard/accessibility, loading/empty/error states, long content, supported viewport; inspect produced files rather than their existence alone. |

Exercise the actual interface. Vary fixtures enough to expose stale/static output. Use controlled local/staging faults or existing fixtures; do not disrupt shared production services. Preserve existing authorization. Reconcile ambiguous mutations before retrying them.

## Observe work as well as output

For network/data changes, count requests or queries for one action and a representative larger input. Look for duplicate fetches, N+1 growth, excessive payloads, retries multiplying work, and polling after dismissal. Record cold/warm cache conditions. Confirm deadlines, cancellation, useful feedback, bounded retries, and eventual recovery.

For resource-sensitive changes, compare representative baseline and changed builds under matching workload, device, build mode, and cache state. Measure the relevant duration, CPU work, allocations, or retained resources. Inspect GPU/frame behavior only when rendering, media, or compute work warrants it; include completion rather than merely launch time. Profiling is not mandatory for a wording or styling fix with no plausible resource effect.

Probe leaks through repeated meaningful lifecycles: open/close, subscribe/unsubscribe, start/cancel, process/dispose. Inspect retained objects, tasks/goroutines, listeners, descriptors, connections, and background work as appropriate. Rising RSS alone is not proof of a leak. Use available platform tools and inspect whether the capture includes the correct process and operation. Repeat only enough to resolve material noise or uncertainty.

While exercising the same paths, inspect meaningful outcome/error telemetry, correlation, secret exclusion, required audit events, and duplicate reports. Check exporter failure if instrumentation delivery changed. Route deeper diagnosis to the relevant profiling or observability guidance rather than adding speculative infrastructure.

## Keep evidence proportionate

Run required owning checks and the smallest meaningful affected tests. Reuse valid results when code and dependencies have not changed. Keep exploratory probes disposable; add a permanent test for a credible regression gap. Prefer explicit cases with distinct failure reasons to parameterized matrices or tests that mirror helpers. Do not remove independent regression protection merely to reduce count.

After a repair, recheck its behavior and affected risks. Stop once acceptance checks and required checks pass and remaining uncertainty is understood. Report what ran, actual outcomes/measurements and conditions, evidence locations, and what was blocked or unmeasured. Never infer end-to-end correctness, absence of leaks, or performance improvement from source inspection alone.
