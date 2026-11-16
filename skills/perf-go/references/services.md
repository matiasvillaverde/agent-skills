# Go backend performance and observability

## Locate time across the operation

Correlate an operation across ingress, admission/queueing, handler work, DB/cache, outbound HTTP/RPC,
background work and final completion. Record service/version/environment, replica, target and
interval; compare equivalent traffic mixes. Aggregate metrics identify a symptom, distributed
traces locate dependency/queue delay, and Go/runtime profiles explain resource costs inside a
process. Clock skew and partial sampling limit subtraction across machines. Do not infer that
all replicas are healthy from a profile of one instance.

Start with a small useful set: request/job rate, error/cancel/timeout/rejection outcomes, duration
distributions, in-flight work/queue age, dependency/pool waits, CPU, memory and relevant runtime
metrics. Keep histograms useful for the service's latency range and SLO. Counts/percentiles from
tiny samples are not tail-latency guarantees. Page for actionable user harm or imminent exhaustion,
not every GC cycle or a universal goroutine count. Reuse the existing alert owner/runbook.

## Instrument boundaries with existing interfaces

For OpenTelemetry, use the application's existing provider/exporter setup and supported HTTP,
RPC and database instrumentation. Applications configure SDKs; libraries normally depend on the
API. Small transport/interceptor/job adapters and a few meaningful internal spans keep business
logic readable. Do not create a provider-neutral interface for every OTel operation or duplicate
spans already emitted by an installed integration. [Go instrumentation](https://opentelemetry.io/docs/languages/go/instrumentation/).

Pass the operation's `context.Context` through outbound calls and owned goroutines; observe its
cancellation. A new background context severs both cancellation and correlation. Detached durable
jobs need their actual lifecycle and trace-link semantics, not a leaked request context.
`RecordError` does not itself set span status; apply failure/cancellation policy at its owning
boundary. Keep sensitive error text and payloads out of attributes. Use the existing slog bridge
or approved trace/span fields: context-aware logging alone does not attach them automatically.

`otelhttp.NewHandler` can instrument a server boundary and `NewTransport` an outbound client.
Retain connection reuse and response-body lifecycle; verify route-template span names and avoid
raw paths with IDs. RPC interceptors require the same propagation and outcome checks. Match the
integration's module/semantic-convention version and test emitted attributes; do not blindly copy
the newest semconv import into an older module. [otelhttp](https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp),
[HTTP conventions](https://opentelemetry.io/docs/specs/semconv/http/http-metrics/).

Prefer the existing OTLP export/Collector path when supported. Keep endpoints, transport/auth,
sampling, verbosity and exporter lifecycle in application configuration; backend changes should
not require editing business code. Standard exporter variables work only where the selected
SDK/exporter actually reads them. Do not assume setting an environment variable starts an SDK.
[Go exporters](https://opentelemetry.io/docs/languages/go/exporters/).

Use bounded attributes: normalized routes/operations and finite outcome categories. Request,
trace, user, tenant IDs, full URLs and SQL text do not belong in metric label sets. Trace/profile
labels also have cost/privacy limits. Sampling should preserve parent decisions according to
policy; head sampling may miss rare failures, and tail sampling adds buffering/processing and
cannot reconstruct spans dropped before the collector. Avoid blanket AlwaysSample in production.
[Go sampling](https://opentelemetry.io/docs/languages/go/sampling/).

Bound queues, batches, timeouts and retries; observe dropped telemetry without recursive logging.
On shutdown, stop admission, finish/cancel owned work, then flush within a fresh bounded shutdown
context before exit. An exporter outage must not create an unbounded queue or unexpectedly stall
business requests. Required audit records have separate durability/retention; trace sampling is
not an audit policy. The available `observability` skill owns that broader contract.

## Continuous profiling and zero-code choices

Use the backend already present: scoped pprof collection, a compatible continuous profiler such
as Pyroscope or Datadog, or supported platform tooling. Confirm which profile types/labels are
actually collected, one CPU-profiler owner, interval, retention, overhead, dropped uploads and
shutdown behavior. More enabled profile types are not automatically better. Backend-specific
trace/profile correlation needs an explicit supported integration; `pprof.Do` labels are not
automatic distributed span IDs. [Pyroscope Go](https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/go_push/),
[Datadog Go profiler](https://docs.datadoghq.com/profiler/enabling/go/).

At the 2026-11-15 research snapshot, OTel Go traces/metrics are stable, logs release candidate,
and the OTel profiles signal is alpha. These are separate stability states; check installed
modules and current docs. A vendor accepting pprof does not establish stable OTLP-profile support.
[Go status](https://opentelemetry.io/docs/languages/go/),
[profiles status](https://opentelemetry.io/docs/concepts/signals/profiles/).

Go zero-code choices include Linux eBPF OBI and compile-time `otelc`; evaluate their actual
version, supported libraries, privileges/build changes and emitted coverage. Neither proves
complete business-context visibility. When combining eBPF spans with manual instrumentation,
follow the Auto SDK integration rather than replacing its global provider. Avoid double collection.
Do not install a privileged daemon or rewrite build pipelines merely because manual instrumentation
is inconvenient. [Choosing Go instrumentation](https://opentelemetry.io/docs/zero-code/go/choosing-auto-instrumentation/).

## Investigate common backend costs

- **HTTP/RPC:** reuse supported clients/transports. Separate connection-pool wait, DNS, connect,
  TLS, request transmission, time-to-first-byte and body completion. Existing `httptrace` hooks
  can answer phase questions; callbacks may be concurrent, and a round trip is not an entire
  redirect chain. Close bodies correctly and retain streaming/cancellation behavior. Avoid
  unlimited draining of untrusted bodies solely to preserve connection reuse.
  [httptrace](https://pkg.go.dev/net/http/httptrace), [net/http](https://pkg.go.dev/net/http).
- **Database:** `sql.DB` is already a concurrent pool. Correlate `DB.Stats` wait deltas, in-use/idle
  connections, query latency and database capacity. More open connections can overload the DB;
  a small limit can serialize or deadlock nested acquisition. Preserve transaction/rows cleanup,
  query contexts and actual consistency. [Connection management](https://go.dev/doc/database/manage-connections),
  [DBStats](https://pkg.go.dev/database/sql#DBStats).
- **Jobs/queues:** distinguish admission, queue age, processing, retries and acknowledged/durable
  completion. Bound fan-out and retries under one deadline/load budget; preserve idempotency and
  ordering. Batch size is a latency/memory tradeoff. Backpressure must be visible, not silently
  dropped work that makes throughput look better.
- **Serialization/cache:** profile the actual payload mix and hit/miss behavior. Avoid zero-copy
  aliases escaping pooled buffers, unbounded caches, lost validation or changed JSON semantics.
  Keep ownership and error behavior explicit; a library swap is not an automatic optimization.

Verify a representative successful operation and affected failure/cancellation/overload paths:
correlation, outcome counts, redaction, bounded labels, no duplicate spans, release of workers/
connections, and exporter failure/shutdown where changed. Measure instrumentation overhead with
equivalent traffic and settings. Keep the smallest tests protecting those contracts.
