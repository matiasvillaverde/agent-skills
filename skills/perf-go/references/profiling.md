# Go profiling and experiments

## Match the profile to the question

Go runtime profiles and distributed traces answer different questions. CPU sampling attributes
running work; it does not account for all network, queue or lock waiting. A Go execution trace
records runtime scheduling and events; it is not an OpenTelemetry distributed trace.

| Evidence | Meaning and interpretation trap |
| --- | --- |
| CPU | Sampled CPU cost. Check absolute totals, capture duration, useful work, flat vs cumulative cost and labels. A wider relative frame may follow removal of other work. |
| Heap `inuse_space` / `inuse_objects` | Sampled live allocation bytes/objects at the profile's GC accounting point. They are not process RSS, cgroup memory or proof that every retained object is needed. |
| Heap/alloc `alloc_space` / `alloc_objects` | Cumulative sampled allocation volume/count, including freed objects. Compare aligned windows/deltas; a longer-lived instance naturally accumulates more. |
| Goroutine | Current stacks/grouping. Compare equivalent lifecycle phases; idle workers can be healthy. Count and stack state alone do not prove ownership or a leak. |
| Block | Sampled time blocked on supported synchronization operations. It is not a full wall-time or network-wait profile. |
| Mutex | Sampled contention attributed to the end of the critical section, such as unlock. Multiple waiters can contribute more delay than elapsed wall time. |
| Execution trace | Running/runnable/blocked transitions, GC and supported task/region events; useful when aggregate samples hide causality. |

Use version-matched [runtime/pprof](https://pkg.go.dev/runtime/pprof),
[runtime controls](https://pkg.go.dev/runtime) and [diagnostics](https://go.dev/doc/diagnostics).
Check available profiles with `pprof.Profiles()` or the authorized endpoint rather than assuming
every newer profile exists. Heap snapshots can lag recent frees; requesting `gc=1` forces GC and
changes the experiment. Keep it explicit, especially on a latency-sensitive service.

## Collect on the service, analyze privately

Use an existing continuous-profiler backend or approved diagnostic path. Preserve exact binary,
build metadata, instance, interval and workload identity for analysis. Copy only scoped captures
through the existing secure transport; the server needs the runtime instrumentation, not the Go
compiler. Analyze with a compatible local Go toolchain and matching executable where needed.

`net/http/pprof` registers on `http.DefaultServeMux` when imported. A public server using that
mux can accidentally expose diagnostics. Use the existing restricted admin surface or an explicit
separate mux/listener with the required authentication/access control. Allowlist only needed
handlers; do not publish command lines, arbitrary profile/debug output or an unauthenticated
`/debug/pprof/` route. Loopback inside a shared network namespace is not an authentication boundary.
Verify the public listener cannot reach diagnostics. [HTTP pprof](https://pkg.go.dev/net/http/pprof).

For an already-authorized endpoint reached through a private local connection, illustrative
bounded commands are:

```sh
curl --fail --max-time 25 --output '<private-dir>/cpu.pb.gz' \
  'http://127.0.0.1:<admin-port>/debug/pprof/profile?seconds=15'
go tool pprof -top '<matching-binary>' '<private-dir>/cpu.pb.gz'
go tool pprof -top -sample_index=inuse_space '<matching-binary>' '<private-dir>/heap.pb.gz'
go tool pprof -top -sample_index=alloc_space '<matching-binary>' '<private-dir>/heap.pb.gz'
go tool trace -pprof=sched '<private-dir>/trace.out' > '<private-dir>/sched.pprof'
go tool pprof -top '<private-dir>/sched.pprof'
```

Acquire the heap/trace files separately through the supported handler or application API; do not
infer their existence from these analysis examples. Keep files private, set `PPROF_TMPDIR` to the
owned capture directory when fetching through pprof, and inspect help before opening a local
viewer. Bind viewers privately and stop them after use. Do not put credentials in command lines.

Only one Go CPU profiler can run in a process at once. Coordinate existing SDK/continuous
profiling with ad hoc capture. Block and mutex sampling require their own enabled settings:
`SetBlockProfileRate` uses nanoseconds of blocked time per expected sample; `SetMutexProfileFraction`
uses approximately one in N contention events. They are not interchangeable rates. Recording
everything can be expensive. Reuse the installed configuration owner and restore it afterwards;
the block setter does not return the previous setting. Do not guess an unknown previous value.

Choose one costly diagnostic at a time unless a specific supported combined capture is needed.
Report its overhead. Short traces and supported flight recording can capture scheduler/GC events
around intermittent symptoms; bound buffer/storage, trigger rate and concurrent writes. Flight
recording APIs and coexistence rules are version-sensitive; read the selected
[runtime/trace](https://pkg.go.dev/runtime/trace) API. A nominal buffer target is not proof of a
hard process-memory cap. Preserve minimal failure evidence before clearing task artifacts.

## Benchmark and optimize from representative evidence

Build and prepare inputs outside the timed operation when they are not part of its contract.
Use runtime-like inputs, visible outputs and the existing harness. Discover current
`go help testflag`, `testing` and compiler behavior. `testing.B.Loop` is available from Go 1.24;
its compiler handling changed in Go 1.26, so do not repeat old no-inlining advice as a current
guarantee. RunParallel, timer boundaries, setup/cleanup and allocation counts need their actual
API semantics. [Testing](https://pkg.go.dev/testing), [Go 1.26](https://go.dev/doc/go1.26).

Use repeated paired/interleaved measurements and an existing compatible `benchstat` to compare
noise, distributions and effect size. Predeclare the meaningful effect and sampling plan; do not
repeat until significance appears. A confidence interval for the median is not run-to-run spread,
and a nonsignificant result does not establish equivalence. [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat).
No universal run count, coverage target or percentage gain
substitutes for the operation's budget. A closed-loop client can suppress arrivals during stalls;
record offered load, completions, queueing, timeouts and client saturation before trusting server
tail-latency results. Keep load generators bounded and outside production unless authorized.

Use representative CPU profiles for PGO, recording profile provenance and target workload mix.
Inspect implicit `default.pgo` inputs; compare equivalent builds with explicit PGO state and
remeasure less frequent critical operations. Stale or unrepresentative profiles can mislead.
Do not promise published benchmark gains for this application. Read the
[Go PGO guide](https://go.dev/doc/pgo) before proposing compiler/profile changes.
