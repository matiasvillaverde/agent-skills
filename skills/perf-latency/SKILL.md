---
name: perf-latency
description: Diagnose and improve end-to-end and tail latency across clients, networks, services and data stores. Use for slow requests, geographic differences, tracing gaps, queueing, replica placement or latency experiment review.
---

# Latency performance

Find what delays the user's result, identify the causal bottleneck, and keep changes that
improve representative measurements without sacrificing correctness or reliability.
Match the work to the request: reviewing existing evidence does not require a new load test.

## Define the delay and preserve the baseline

Identify the operation, product/environment, affected users and required outcome. Define
start and finish: input to usable result, RPC response, first byte, first useful streamed
output, full completion or data freshness. Keep these distinct; a fast acknowledgement
does not prove completed work. Use an existing latency objective or establish a justified
one from the task; do not impose universal millisecond targets.

Inspect existing code paths, topology, traces, field measurements and performance checks.
Record the build, endpoint/workload, payload size, client/device, origin network/region,
cache/connection state, concurrency or arrival pattern and time window. Split relevant
cold/warm, hit/miss, success/error and regional cohorts; do not change the population to
make a comparison look better.

Use duration distributions and sample counts alongside offered/admitted/completed work,
successful throughput, timeouts, cancellations and resource use. State missing evidence.
Do not average replica/region percentiles, add stage p99s, treat timeouts as successful
completions or claim stable tails from a few probes. Read
[measurement and attribution](references/measurement-and-attribution.md) before interpreting
percentiles, traces or a load-test result.

## Follow the causal path

Map the actual request: client scheduling → DNS/connection/TLS → edge/routing → service
queue → execution → downstream calls/data → response transfer → client processing/display.
Include redirects, retries, connection-pool waits, fan-out joins and asynchronous completion
when present. This is an evidence map, not a requirement to instrument every function.

Compare representative normal and slow requests from the same cohort. Use existing
OpenTelemetry instrumentation and context propagation; add only missing meaningful
boundaries. Validate propagation across async work, process hops and queues. Preserve
sampling policy, trace completeness and clock limitations when interpreting the result.

Identify which dependent work gates completion. Parallel, nested and background spans
cannot be summed into wall time; uninstrumented time is unexplained, not automatically CPU
or network time. A large total-work contributor may have little effect on the critical path.
Follow the bottleneck down one level with the relevant evidence:

- **Network:** actual timing phases, connection reuse, protocol, redirects, bytes, retries
  and destination/proxy information. TTFB includes more than server execution.
- **Queue/runtime:** admission and pool waits, runnable delay, event-loop/task blocking,
  locks, GC, CPU throttling and saturation. A low average CPU value does not exclude waiting
  or a single saturated worker. Correlate profiles with the slow operation.
- **Data/dependencies:** query plan and execution, lock/I/O waits, number of round trips,
  cache state, downstream tails, retry attempts and where data actually lives.
- **Client:** decoding, rendering, main-thread/actor work and the final useful result.
  A completed network span does not cover these automatically.

Keep observations, hypotheses and next discriminating measurements separate. Request a
missing trace/profile only when it can change the decision; do not infer causes from names.

## Compare geography and topology deliberately

For geographic differences or replica/routing proposals, read
[global probes and topology](references/global-probes-and-topology.md). Use real authorized
vantage points and record their network context. Local throttling or a location header does
not simulate another country's route; datacenter probes do not establish mobile-user latency.

Distinguish app replicas, read replicas, leaders and synchronous quorum members. Place work
with attention to the whole dependency chain. More nearby compute can increase remote data
round trips; more replicas can multiply connections, lose cache locality or shift contention.
Preserve freshness, read-your-writes, failover and residency requirements.

## Change one supported cause and verify

Prefer removing unnecessary serial work, duplicate requests, excess round trips or repeated
computation when implicated by evidence. Consider query improvements, connection reuse,
bounded concurrency, caching, routing or capacity only for the measured mechanism. Each
needs its correctness and overload tradeoff. Retries and hedges can amplify load; moving
work behind an acknowledgement can merely hide the wait.

Choose a bounded experiment with a baseline, hypothesis, expected affected interval,
correctness constraints and stop conditions. Use existing tools and authorized targets.
Production load, paid/global probes, capacity changes and routing/replica mutations require
scope-specific authorization already present in the task; skill invocation alone does not
authorize them. Public probe services may expose targets and results. Keep raw traces
private and bound instrumentation overhead, duration, volume and diagnostic lifetime.

Compare like workloads and account for run-to-run variation. Recheck tails, successful
throughput, errors, resource/cost effects and freshness under relevant load, including a
meaningful saturation or failure case when that behavior changed. Verify the load generator
actually delivered the intended work. Reject gains explained by dropped work, stale data,
less validation or measurement bias; revert complexity without a demonstrated benefit.

Add only a stable, owned regression check or latency budget that protects the changed
contract. Reuse existing tests/telemetry; avoid a benchmark or snapshot for every function.
Report the boundary/cohort, baseline and result with units/counts, causal evidence,
keep/revert decision and gaps. Separate a lab result, a topology hypothesis and a production
improvement; claim only what was measured.

## Finish and clean up

Save the compact causal findings, measurements and reproduction commands. Stop task-owned
load generators/probes, restore temporary instrumentation/network settings and remove
task-created traces, packet captures, exports, fixtures and isolated caches by exact owned
path. Preserve shared application/CDN caches and required telemetry/incident evidence.
Keep only requested/required artifacts or the minimum needed for unresolved failures.
Stop owned work and restore settings even on failure or cancellation; verify cleanup and
report any retained artifacts, active resources or leftovers with the reason.
