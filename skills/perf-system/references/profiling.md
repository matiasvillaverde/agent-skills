# Choosing useful profiling evidence

Select the smallest tool that answers the current question. Use the installed
toolchain's supported commands and official documentation; do not install another
profiler or elevate host-wide permissions by default.

| Question | Evidence to collect |
| --- | --- |
| CPU work or busy polling | CPU samples/cycles, call stacks, wall vs CPU time, idle baseline |
| Blocking or contention | Off-CPU/wait samples, lock ownership, runnable threads, queue delay |
| Allocation churn | Allocation count/bytes and allocating stacks per operation |
| Retained memory or leaks | Live object/heap growth across repeated lifecycle cycles after warmup; ownership and release paths |
| Excess GPU work | Frame/GPU timing, repeated passes, overdraw/resource lifetime where supported; compare the same visual workload |
| Too many requests | Requests and bytes per user action, initiator/call site, duplicate inflight work, retries and cache behavior |
| Latency under concurrency | p50/p95/p99 with sample count, throughput, queue depth, cancellations and errors |

RSS alone does not establish a leak: allocators, caches and runtime retention can keep
pages resident. A rising live-heap/object count after repeated open/close or start/stop
cycles is a more useful lead. Confirm the retaining owner before prescribing a fix.
For runtimes with collectors, avoid comparing different collection/warmup states.

On Apple platforms use the available Instruments CPU, allocation/leak, signpost and
Metal tools for the relevant target. On Linux use scoped `perf`/runtime profiles where
permitted; richer eBPF collection needs a specific question and existing authorization.
Go has runtime/pprof; browser tooling can correlate JS, rendering and network work.
Rust, Zig, C and C++ often use native platform profilers with symbols; optimization and
inlining change attribution. Check the selected build and symbol settings.

Sampling, tracing and debug builds can perturb the workload. Capture only what is needed,
bound trace duration/size and protect private data. Separate instrumented diagnosis from
the final representative measurement. Do not expose a profiling HTTP endpoint publicly.

Primary tool entrypoints: [Apple performance](https://developer.apple.com/documentation/xcode/improving-your-app-s-performance),
[Metal tools](https://developer.apple.com/metal/tools/),
[Linux perf security](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html),
[Go diagnostics](https://go.dev/doc/diagnostics),
[Chrome performance](https://developer.chrome.com/docs/devtools/performance/).
