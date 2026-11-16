# Measure the right interval and explain it

## Establish what a number means

For each result, retain the observer, units, start/end events, outcome policy, cohort,
sample count, time window and collection method. Prefer the existing user-facing SLI;
include useful completion/freshness even when the transport acknowledged earlier.
Mean duration can explain cost or capacity; tails reveal different problems. Neither
replaces successful throughput and failed, cancelled or incomplete work.

Match metric boundaries before comparisons. [OTel HTTP spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/)
can exclude connection setup and may end before response-body completion.
[k6 `http_req_duration`](https://grafana.com/docs/k6/latest/using-k6/metrics/reference/)
covers sending, waiting and receiving but excludes initial DNS/connection setup. Client
processing and display need their own observed boundary. For streaming, distinguish time
to first useful output from completion and cancellation; headers or an empty token may not
provide value. Verify actual instrumentation, not just the metric/span's name.

Treat timeouts as observed time until a deadline with no successful completion observed.
Do not invent their eventual completion duration, set them to zero or silently drop them.
Show success latency beside outcome counts/rates using explicit denominators. Caller-intended
cancellation can legitimately lack OTel Error status and still yield no completed user result.
Separate logical operations, attempts and successful completions.

## Distributions and comparisons

Aggregate compatible raw observations or histogram distributions before calculating a
combined percentile. Never average regional/replica p99s or add/subtract stage p99s to
reconstruct a request. Check units, population, window, buckets/resolution and query filters.
[Prometheus](https://prometheus.io/docs/practices/histograms/) explains why precomputed
summary quantiles cannot be combined that way; a histogram estimate also has resolution error.

Report counts and variation with tails. A computed p99 from a handful of probes does not
establish a precise population p99. Pick duration/repetitions to distinguish the effect that
matters; there is no universal sample quota. A million correlated requests in one run are
not a million independent before/after experiments. Use matched runs or time blocks and
appropriate uncertainty when a statistical decision is needed. Avoid cherry-picking the best
run, silently dropping outliers or changing geography/traffic mix between variants.

Compare population metrics independently of diagnostic trace selection where possible.
Latency/error-selected tail traces are not an unweighted traffic distribution. Known
probability sampling can support valid estimators, but verify inclusion probabilities,
losses and backend support before making that claim. Record policy changes between runs.
[OTel sampling](https://opentelemetry.io/docs/concepts/sampling/) and its
[probability guidance](https://opentelemetry.io/docs/specs/otel/trace/tracestate-probability-sampling/)
describe different strategies; the latter was Development at the 2026-11-13 review.

## Reconstruct the critical path

Use a suitable local monotonic timer for elapsed durations. Keep clock domains explicit;
cross-host wall timestamps do not establish precise one-way transit time without clock-error
evidence. Impossible ordering can be clock skew, missing data or wrong instrumentation.
Do not silently repair it into an asserted causal result.

Inspect a representative slow request with matched normal controls. Follow the actual
dependencies: what starts each task, what the response waits for, and which work continues
afterwards. Span parentage is not proof of temporal enclosure or a blocking join.
[OTel's API](https://opentelemetry.io/docs/specs/otel/trace/api/) permits children to outlive
parents; [CRISP](https://www.usenix.org/system/files/atc22-zhang-zhizhou.pdf) demonstrates
why total work, synchronization edges and clock skew matter to critical-path analysis.

Within one clock domain, use overlap/interval unions when accounting for covered time;
do not subtract every inclusive child from its parent. Preserve unexplained gaps. Distinguish
work saved from wall time saved: improving one parallel branch can expose another as the
limiter. Off-path work can still matter through shared resource contention. Avoid projecting
an exact speedup from an incomplete graph or assuming fan-out requests fail independently.

Use existing OTel context propagation across HTTP/RPC, async tasks and queues. Check actual
correlation at the boundary; [W3C Trace Context](https://www.w3.org/TR/2021/REC-trace-context-1-20211123/)
does not synchronize clocks or guarantee recording. Preserve producer/consumer relationships
and links when work is detached; do not fabricate a parent span just to make a neat tree.
Use stable operation/route names and bounded metadata. Keep identifiers out of metric labels
and secrets/payloads out of trace attributes. Check exporter drops and incomplete traces
before interpreting an absent span as absent work.

## Go deeper with the implicated runtime

| Surface | Useful evidence and important limit |
| --- | --- |
| Swift/native Apple | `URLSessionTaskMetrics` and ordered transaction metrics distinguish redirects, cache, protocol, reuse and phase timing. Missing timestamps are not zero. Correlate with signposts/Instruments for main-actor scheduling, decoding and presentation. HTTP Traffic capture includes unencrypted headers/body; prefer minimal metrics and protect scoped captures. |
| TypeScript/JavaScript browser | Resource/Navigation Timing plus interaction marks and browser traces. Cross-origin restrictions can mask fields; service workers and buffers affect coverage. Verify `Timing-Allow-Origin` and actual browser support before interpreting zero values. Include rendering and long main-thread work. |
| Node.js | Existing request spans plus event-loop delay/utilization and CPU/GC profiles. Event-loop utilization is not CPU utilization; loop-delay histograms are not per-request duration. Match units and sampling settings. |
| Go | `pprof` CPU for running work; block/mutex profiles and `runtime/trace` for synchronization, runnable delay, syscalls and GC. Request tasks help relate runtime activity to an operation. Collect only what is needed; profiles can interfere. |
| Rust async | Existing tracing plus runtime/task scheduling evidence. Tokio console, when already suitable, distinguishes busy polling, ready-to-run delay and idle wait. It needs compatible instrumentation/features; do not install or enable unstable diagnostics by default. |
| Python, C, C++, Zig and other runtimes | Use the installed runtime/platform profiler with symbols and operation context to distinguish CPU work, locks, I/O and scheduler waits. Include executor queues or GIL contention where applicable. Do not infer a cause from the language alone. |

[Apple metrics](https://developer.apple.com/documentation/foundation/urlsessiontasktransactionmetrics.md),
[HTTP Traffic capture](https://developer.apple.com/documentation/foundation/analyzing-http-traffic-with-instruments.md),
[Resource Timing](https://www.w3.org/TR/resource-timing/), [Node performance](https://nodejs.org/api/perf_hooks.html),
[Go diagnostics](https://go.dev/doc/diagnostics), [Go runtime tracing](https://pkg.go.dev/runtime/trace)
and [Tokio console](https://github.com/tokio-rs/console/tree/b59758e5a6effe3a9df3ec84a2f28d319d178234)
are source entrypoints, not prescribed dependencies. Match their advice to installed versions.

OS off-CPU analysis can reveal waits missed by CPU profiles, but filter to the request's
active context; idle workers are not user latency. Runnable delay, involuntary preemption
and missing symbols complicate attribution. [Off-CPU tracing](https://www.brendangregg.com/offcpuanalysis.html)
can itself create significant event/CPU/storage cost. Use scoped existing permissions,
short bounded capture and measured overhead; do not expose profiler endpoints publicly.

## Verify workload delivery when load evidence matters

Choose an [open or closed workload](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/)
according to the question. Fixed concurrency suits a finite user population but slows
arrivals as responses slow. Independent arrival schedules suit offered-rate questions,
yet finite generators can still start late or drop work. An iteration may contain several
requests; do not relabel iterations/second as requests/second.

Record scheduled starts, actual starts, admitted operations, attempts, completed/successful
operations, late starts and dropped work where observable. Check generator CPU/network,
connections, client pools, pacing and time fidelity as well as target capacity.
[k6 dropped iterations](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/)
are unsent work, not fast responses. A run that passes a latency threshold but misses its
intended load cannot support the configured-load claim. A valid overload test may fail its SLO.

Coordinated omission occurs when measurement scheduling stops observing demand during a
stall. Model actual arrivals and record start lateness; histogram correction is not a
substitute for unknown dropped traffic. Use ramps, bounded saturation or recovery scenarios
only when needed to test the changed behavior. Stop on the agreed budget or harm threshold.
Recheck the winner without diagnostic overhead under comparable conditions; do not turn
review of existing evidence into an automatic production load campaign.
