# Runtime profiling

Use the project's actual Node binary and built JavaScript/source maps. Record `node
--version`, `process.versions`, launch flags and deployment limits; a TypeScript runner
or development transpiler can dominate a test. Inspect `node --help` before using flags.

| Symptom | Useful evidence | Interpretation limit |
| --- | --- | --- |
| CPU-heavy request | Core `--cpu-prof`, sampled stacks, per-process CPU | CPU samples omit time waiting; profile relevant workers separately |
| Main loop stalls | `monitorEventLoopDelay`, ELU deltas, CPU trace | Timer resolution and sampling method affect the histogram |
| Slow response, low loop work | Trace spans, pool/queue wait, DNS/TLS and upstream timing | Async stacks and span elapsed time are not CPU attribution |
| Native work dominates | Symbols plus OS profiler; libuv pool queue and task types | A JS frame alone cannot identify native internal cost |
| CPU quota saturation | cgroup throttling, scheduler pressure, host contention | Host core count is not the process's CPU entitlement |
| Slow startup | Fresh process wall/CPU, import/load/init attribution | Do not silently remove startup from CLI measurements |

For a bounded local workload that terminates normally:

```sh
node --cpu-prof --cpu-prof-dir="$capture_dir" --cpu-prof-name=run.cpuprofile workload.js
node --heap-prof --heap-prof-dir="$capture_dir" --heap-prof-name=run.heapprofile workload.js
```

`capture_dir` must be a precreated private task directory; filenames must not overwrite
existing evidence. Inspect the actual profile and symbol mapping. These are separate
diagnostic runs, not benchmark commands. Forced termination can lose exit-written data.
Choose duration from the workload, then enforce an outer timeout and stop owned children.

`performance.eventLoopUtilization(previous)` returns a window delta when supplied a
previous reading. Active/idle values are milliseconds. ELU measures time outside the
event provider, not CPU: synchronous waiting can leave ELU high with little CPU work.
`monitorEventLoopDelay({resolution: ...})` takes resolution in milliseconds but returns
nanosecond histogram values; divide by 1e6 for milliseconds. Enable before the measured
window, allow the sampler to run, record sample count, then disable/reset. Empty samples
are missing evidence. Confirm the sampler covers the measured phase and allow post-work
observation before disabling; a nonempty count alone does not prove a blocked interval
was captured. Match sampling mode/resolution across comparisons; version-specific
per-iteration sampling is not interchangeable with interval sampling.
[Node perf_hooks](https://nodejs.org/api/perf_hooks.html).

Inspect synchronous I/O, large JSON parsing/serialization, pathological regular expressions,
long loops and recursive microtask/nextTick scheduling when a trace supports them. Promises
do not make CPU work parallel. libuv worker-pool contention can involve filesystem, DNS,
crypto and compression; inspect the actual API and version before changing pool size.
[Node event-loop guidance](https://nodejs.org/learn/asynchronous-work/dont-block-the-event-loop).

Keep the inspector on loopback/private approved transport; it enables execution in the
process. Never expose it publicly to make profiling convenient. Capture access, source
paths, arguments and data may be sensitive.
[Inspector security](https://nodejs.org/learn/getting-started/debugging).

CPU deltas from `process.cpuUsage()` use microseconds and can exceed wall time when
multiple threads work. Container CPU throttling and event-loop delay require separate
evidence. Diagnostic reports and verbose GC traces are bounded incident tools, not
unlimited per-request logs. [Process API](https://nodejs.org/api/process.html).
