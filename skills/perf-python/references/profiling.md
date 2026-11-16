# Profilers and measurement

Check the actual interpreter with `python -VV` and tool help before forming a command.
Run only a safe bounded workload in a private capture directory; no production credentials
in examples. Profile and benchmark in separate runs.

| Question | Candidate | Limitation |
| --- | --- | --- |
| Which Python calls dominate? | `python -m cProfile -o "$capture_dir/run.prof" workload.py`; inspect via `pstats` | Deterministic overhead biases comparisons; cumulative time includes callees/waits |
| Which stacks are active? | Installed compatible sampling profiler, including Python 3.15 `profiling.sampling` | Sampling mode, target support and attach permissions determine coverage |
| Where do traced allocations grow? | `tracemalloc` snapshot differences | Covers traced allocations since start, not all native/GPU memory |
| Native allocation or native CPU | Compatible Memray/native sampler, symbols and OS tools | Python-only stacks cannot explain every extension |
| Async request/queue latency | Task-aware stacks, traces and queue timing | Suspended task duration is not CPU time |
| Improvement beyond noise? | Existing benchmark runner or installed `pyperf` | Profiles and static complexity estimates do not prove a speedup |

Inspect local sampling help. A supported Python 3.15 command can run a safe script:

```sh
python -m profiling.sampling run --duration 2 --sampling-rate 100 \
  --collapsed --output "$capture_dir/stacks.txt" workload.py
```

The profiler and target require compatible minor versions/builds; prereleases require
tighter matching. Wall, CPU and GIL modes have different denominators. Async-aware mode
needs asyncio loaded and has flag restrictions; include suspended tasks only when that
is the question. It reconstructs await relationships, not CPU use. The native placeholder
option is not a full C/C++ stack unwinder. Blocking sampling pauses target threads and
changes overhead. Denied attach is a gap: choose an allowed in-process fallback without
automatic sudo/ptrace changes. [Python sampling](https://docs.python.org/3.15/library/profiling.sampling.html).

Python 3.15 introduced the `profiling` namespace; `cProfile` remains available as an alias
for the tracing implementation. Do not require the new namespace on older supported
targets. Distinguish `tottime` from cumulative time and call counts from sample counts.
Profile startup separately if imports are the issue.
[Profiling](https://docs.python.org/3.15/library/profiling.html),
[tracing profiler](https://docs.python.org/3.15/library/profiling.tracing.html).

For performance comparisons, keep GC behavior representative: `timeit` disables cyclic
GC by default and its minimum is an idealized lower bound, not a latency distribution.
Use independent process runs where allocator/JIT/cache history matters; record warmup,
sample count and dispersion. `pyperf` stability/significance reports help but do not
substitute for practical effect size or correctness. Do not automatically tune host CPU
frequency, disable system services or pin cores on a shared machine.
[timeit](https://docs.python.org/3/library/timeit.html),
[pyperf analysis](https://pyperf.readthedocs.io/en/latest/analyze.html).

Check optional profiler maintenance, supported Python/OS builds, license and artifact
privacy before installation. Use provider-neutral outputs where practical; a profiler's
detector score is a lead, not verified causation. Linux containers may restrict process
visibility or ptrace; macOS attach can be denied independently of normal file access.
