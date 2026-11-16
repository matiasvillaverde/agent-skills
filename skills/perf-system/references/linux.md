# Native performance on Linux

Use this for Rust, Zig and other native binaries on Linux, including x86-64 and ARM64 servers,
workstations, containers and VMs. Profile where the work executes. Cross-compilation, emulation
or a successful macOS profile does not establish Linux performance. Keep the existing shipping
target, libc, allocator and safety behavior unless changing one is the explicit experiment.

## Establish the execution environment

Record kernel/distribution, CPU model and topology (`uname`, `lscpu` where installed), actual
compiler/target, executable identity, and container/VM status. Discover installed profiler versions,
supported events and permissions; a tool name in a skill is not an installation guarantee.
Use the target's effective affinity and resource limits, not the host's advertised core count.
Virtualized CPU features, clocks, PMUs and NUMA topology can differ from the physical host.

For the selected PID, resolve cgroup membership through `/proc/<pid>/cgroup` and the visible
mount hierarchy. Inspect effective CPU/memory sets and ancestor limits as permitted. In cgroup v2,
`cpu.max` is a bandwidth quota/period, not dedicated cores. Compare `cpu.stat` throttling deltas,
`memory.current`, `memory.events`, applicable limits and `io.stat` over the same workload interval.
Version-match counter semantics and account for ancestor limits. A container's low CPU usage
does not exclude throttling. Do not change quotas, affinity, governor, huge pages or host settings
as a hidden benchmark prerequisite. [Kernel cgroup documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html).
The fraction of throttled periods is not the fraction of application time lost; throttling
duration accounting can span multiple CPU run queues. Correlate it with request latency instead
of converting it directly into a promised speedup. [Bandwidth accounting](https://docs.kernel.org/scheduler/sched-bwc.html).

Check CPU/memory/I/O pressure through `/proc/pressure/` or the selected cgroup's pressure files
when available. PSI describes time lost to contention; it does not identify a function or prove
which task caused contention. Compare interval deltas and workload scope. System-level CPU
`full` is not a usable signal. [PSI definitions](https://docs.kernel.org/accounting/psi.html).
Container-visible `/proc/pressure` may cover a broader scope than the selected cgroup's pressure
files; verify the source before attributing stalls to that container.

## CPU samples and counters

Build once, outside timing. For Rust, use the intended optimized Cargo profile with debug info
and usable symbols; put profile settings in the workspace root. For Zig, use the project's exact
compiler and mode names with symbols retained. Check the resulting ELF/build ID and matching
debug information using available `file`/`readelf` tools. Stripping, split debug files, shared
libraries and container paths can break attribution even when the application runs correctly.

Use the bounded native commands in [the shared guide](native.md#record-a-bounded-profile).
On a host allowing only userspace events, select supported `cycles:u`, `instructions:u`, and
other relevant `:u` events; these exclude kernel work and must be labeled accordingly. Check
`perf list`, actual event-open success and the installed command help. Software `cpu-clock:u`
sampling can be a fallback when hardware sampling is unavailable **and** permissions permit it;
it supplies CPU stacks, not hardware cycles/cache measurements. A restricted `perf_event_open`
can deny software events too. Failed/not-counted events are unavailable, never zero.

Example for an already permitted, bounded workload with supported DWARF unwinding:

```sh
perf record -e cpu-clock:u -F 99 --call-graph dwarf \
  -o '<private-task-directory>/cpu.data' -- '<absolute-binary>' <args>
perf report --stdio -i '<private-task-directory>/cpu.data'
```

Frame-pointer sampling is useful only when the relevant stack frames preserve frame pointers;
DWARF needs a compatible perf build and adequate captured stack data. Validate target samples,
resolved functions, unwind depth and lost events. Diagnose missing frames before ranking callers.
Preserve the matching executable/debug files until analysis is complete; do not publish captures
or start a public symbol server. [perf recording contract](https://github.com/torvalds/linux/blob/23c62304dde29abe92013d85910d03a77dada35d/tools/perf/Documentation/perf-record.txt).

Use CPU-specific PMU definitions. Intel PEBS/LBR/PT, AMD IBS and Arm SPE are distinct optional
mechanisms, not portable switches. Guest exposure and kernel/tool support matter. Consult the
[hardware references](native.md#interpret-hardware-evidence), `perf list` and target documentation
before using raw events. Check multiplexing and event scope before ratios. IPC or miss-rate changes
need matching absolute work and latency; neither alone proves an improvement.

## Memory, locality and allocation

Use heaptrack for supported allocation stacks/churn, Massif for supported memory experiments,
or existing allocator accounting when those tools cannot observe the allocator. Execute the built
program, not `cargo run` or the Zig compiler. Interposition may miss static binaries, custom
allocators, direct mappings and arena suballocations. Do not replace the shipping allocator just
to make a chart appear; label a diagnostic build and remeasure the original configuration.
[Heaptrack](https://github.com/KDE/heaptrack), [Massif](https://valgrind.org/docs/manual/ms-manual.html).

For the owned process, `smaps_rollup` can distinguish aggregate resident/proportional memory;
`status`, `io` and fault counters answer narrower questions with different semantics. RSS/PSS,
allocator live bytes and cgroup memory are different accounting boundaries. File cache, mappings,
retained arenas and fragmentation require lifecycle evidence before calling growth a leak.
Avoid frequent expensive map walks and never collect `/proc/<pid>/environ` or memory contents as
routine profiling. [Process accounting documentation](https://www.kernel.org/doc/html/latest/filesystems/proc.html).

Check NUMA topology, allowed memory nodes and first-touch placement before changing thread/data
placement. `numastat` or supported memory-access sampling may help when already available. NUMA
policy applies within cpuset restrictions; moving a worker does not automatically relocate its
existing data. Distinguish remote access, bandwidth saturation and false sharing. Padding or
binding every worker can increase footprint or hurt another workload. [NUMA policy](https://www.kernel.org/doc/html/latest/admin-guide/mm/numa_memory_policy.html).

## Scheduling, syscalls and I/O

CPU stacks show running work. For wall-time gaps distinguish blocked waits, runnable queue delay,
CPU throttling and VM steal. Use permitted thread/scheduler evidence, existing operation spans,
or narrowly scoped `perf sched`/eBPF tooling where available. A futex wait is not automatically
wasted time; correlate the owner/wakeup, deadline and useful throughput before changing locks.
Rust executor metrics supplement OS evidence; a worker thread's sleep does not identify the
async task responsible for latency.

Use `strace` for selected owned-process syscalls when permitted; summaries/counts can reveal
excess work, while duration/correlation helps separate calls from completion. Tracing perturbs
timing and can expose paths/payloads: filter to the necessary syscall families and prefer bounded
aggregate output. Queued writes, page-cache hits, `fsync` and network responses have different
completion contracts. Preserve the one the product requires. [strace](https://strace.io/).

For eBPF/BCC/bpftrace, inspect the installed version, available probes and fields. Scope by the
owned PID/cgroup, aggregate instead of printing every event, bound duration/map growth and
retain dropped-event evidence. Kernel probes and hardware events may need privileges; do not
add capabilities, relax seccomp/Yama/perf restrictions or trace the whole host as a workaround.
[bpftrace language/probes](https://bpftrace.org/docs/release_024/language),
[kernel perf access model](https://docs.kernel.org/admin-guide/perf-security.html).

## When the profiler is unavailable

Report exactly what is absent or denied. Use existing application spans, allocator counters,
owned-process resource accounting and repeated bounded wall/CPU measurements to narrow the
question. These do not replace symbolized samples or PMU evidence. Keep the performance finding
inconclusive where the missing observation is decisive; name the smallest missing capability.
Installing a tool, changing host security or moving to a production host is not an automatic
fallback. Do not turn a coverage gap into a claim that the bottleneck is absent.

Compare on the same execution environment with equivalent shipping settings. Keep behavior,
correctness and resource budgets intact; validate representative input sizes and concurrency.
Stop owned collectors and remove their traces, binaries and isolated caches after keeping the
minimal findings/reproduction evidence. Preserve shared caches and unrelated processes.

Source scope: selected primary sections reviewed 2026-11-15; exact installed tool/kernel help
takes precedence for supported syntax and fields. Documentation coverage does not claim that
every listed profiler, CPU family or target has been exercised.
