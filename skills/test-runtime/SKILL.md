---
name: test-runtime
description: Verify a running feature's real effects, failure recovery and resource use by correlating actions with logs, traces and state. Use for operational testing across apps, CLIs, APIs, MCPs and jobs.
---

# Test runtime behavior

Determine whether a feature does the promised work, handles consequential failures and releases
resources. This role may inspect source and operational internals. It complements user-interface
testing; it does not redesign the product or add an observability platform.

## Bind observations to the work

Identify the user operation, required outcome, actual build/process, dependencies and authorized
environment. Read owning instructions, current tool help and relevant platform documentation.
Separate real integrations from fixtures and mocks. Use a disposable fixture/account and explicit
workload; keep initial state and run/correlation IDs so unrelated activity is not attributed to it.

Choose the relevant [runtime surfaces](references/surfaces.md). Inspect existing observability
before changing instrumentation. Start with the cheapest signal that can resolve the question;
use bounded temporary diagnostics only when necessary and permitted. Keep credentials, customer
payloads and unrelated logs out of evidence. Record capture gaps, sampling, dropped events and
clock/timebase limits. Quiet logs or an empty query do not prove that no failures occurred.

## Follow an operation to its final effect

Exercise a representative success through the real entrypoint and follow it across the boundaries
it actually crosses: client, transport, server, queue, worker, storage or external provider.
Correlate records with operation identity, not approximate timing alone. Distinguish accepted,
queued, started, completed, persisted and consumed; check the terminal outcome the contract promises.
Read back state or artifact content through a sufficiently independent observer. A completion log
written before a commit, a flushed exporter queue or a successful tool envelope is not final proof.

For relevant network/data work, count actual attempts, requests, queries and effects. Inspect
payload sizes, pagination, duplicate fetching, retries that multiply work, queue growth and polling
after dismissal. Use a small and a representative larger input when growth is the concern. Never
derive scenario/request counts from how many issues were found.

Select plausible controlled faults: delay/refusal/disconnect, upstream rejection, partial write,
worker interruption, cancellation or concurrent completion. Confirm the fault reached the intended
boundary. Check user-visible outcome, terminal state, bounded retry/deadline behavior, duplicate
effects and recovery. Inject only within owned or explicitly authorized test resources. Preserve
state and reconcile uncertain mutations before retrying; do not disrupt shared production or
automatically provision infrastructure. Unavailable fault controls are a coverage gap.

## Measure resource behavior proportionately

Compare equivalent baseline and changed workloads when claiming a regression or improvement:
same build mode, device, input, cache conditions and observation interval. Record cold/warm behavior
where relevant. Measure completion latency and tail behavior with enough samples for the claim;
one fast request cannot establish a percentile or SLO. Report counts and uncertainty without
inventing a universal acceptable CPU, memory, request or latency threshold. Use an existing budget
or justified baseline; otherwise report measurements and the unresolved acceptance decision.

For a plausible lifecycle issue, repeat meaningful start/finish/cancel or open/close cycles and
inspect remaining tasks, threads/goroutines, children, listeners, descriptors, connections or
allocations. Distinguish cache warm-up and allocator reservation from retained live resources;
rising RSS alone is not a leak. Check GPU/frame/audio/hardware work only when the feature uses it.
Heavy profiling can change the behavior being measured; disclose that and confirm with lighter
measurement when it matters. Deeper investigations can use the appropriate performance skill.

Verify useful outcome/error correlation, expected audit events and redaction on exercised paths.
Distinguish diagnostic verbosity from required audit delivery. Check sink failure or bounded export
queues when relevant; adding noisy logs or disabling a failing alert is not a test fix.

## Deliver operational evidence

Report each tested claim as **passed, failed, blocked, not run, inconclusive**, or **not applicable
with a reason**. Include workload/build/environment, actual observation and its limits, state or
artifact evidence, measurements with units/counts, and a reproducible failure when found.
Separate product defects from unavailable tools, capture errors and unrelated background activity.
Do not turn a source hypothesis into a reproduced failure. Route suspected issues for independent
adjudication when needed; do not quietly patch behavior or change the acceptance budget.

After an authorized repair, repeat the affected experiment under comparable conditions and inspect
its final effect and cleanup. Keep a permanent test only for useful regression protection; preserve
required owning checks. Retain compact redacted findings and reproduction details, then stop only
owned captures/processes/fault injection, restore owned test configuration and remove task-created
fixtures, transient traces and caches. Preserve required failure evidence and unrelated/shared
caches. Report leftovers and any uncertainty that prevents a completion claim.

[Research and platform sources](references/sources.md). This skill runs independently; it does not
require a fixed agent team or every profiler for every feature.
