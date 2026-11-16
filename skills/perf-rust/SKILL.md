---
name: perf-rust
description: Diagnose and improve low-level Rust CPU, allocation, memory-layout, concurrency, I/O and code-generation performance using measured native profiles. Use for Rust libraries, services and compute-heavy application code.
---

# Rust performance

Find the cost that matters to the requested operation, then change only a demonstrated
bottleneck. Preserve user-visible behavior, UI, output quality, ordering, cancellation,
durability and safety. This applies to libraries, servers, embedded native components and
programs on Linux (x86-64 and ARM64) and macOS, not just CLIs. Select tools for the execution
host; Apple Silicon results do not qualify a Linux deployment. The available `perf-rust-cli` adds command startup, pipes and process
behavior when those are the question; it is not required for every Rust investigation.

## Establish the experiment

Read the owning instructions, actual Cargo workspace/profile, lockfile and toolchain. Record
`rustc -Vv`, Cargo version, target/CPU, features, allocator, build flags, workload, concurrency
and cache/thermal conditions. Use the product's latency, throughput, CPU, memory or energy
budget. If absent, establish a baseline and label a proposed target; never invent universal
acceptable IPC, memory, allocation or runtime numbers.

Build outside the timed region and profile the resulting executable or its real host. Compare
equivalent optimized builds with usable symbols. Read [build and codegen](references/build-and-codegen.md)
when preparing symbols, inspecting assembly or testing PGO/LTO/SIMD. Online stable docs may be
newer than the selected toolchain: verify flags and APIs against installed help and matching
source. Do not upgrade the project merely to make an example compile.

## Select the evidence

| Concern | First useful evidence |
| --- | --- |
| Hot computation, branches, cache/TLB or bandwidth | Native CPU samples, then supported hardware counters for the hot path. Use Instruments on macOS, perf on Linux, or an available compatible native profiler. |
| Allocations, copies, retained capacity or fragmentation | Allocation stacks/counts/bytes, peak/live bytes and lifecycle ownership; check custom allocator visibility. |
| Async latency, wake storms, contention or oversubscription | OS thread states and existing spans; supported Tokio Console diagnostics for poll, scheduled and idle time. |
| Network/filesystem overhead | Actual requests/syscalls/bytes, queueing, completion, retry and fsync behavior. |
| Code size, dispatch, vectorization or compiler regression | Actual optimized caller/binary, emitted assembly/IR and compiler remarks, then representative runtime measurements. |

Use the existing tool and smallest capture that answers the question. The shared library's
[native profiling guide](../perf-system/references/native.md) provides OS recipes, counter
interpretation and hardware references; official tool documentation remains the fallback if
that companion is unavailable. On Linux, read its [Linux workflow](../perf-system/references/linux.md)
for symbols, containers/VMs, scheduling, NUMA and restricted-counter fallbacks.
Read [memory and concurrency](references/memory-and-concurrency.md)
for Rust-specific attribution and lifetime traps. Missing tools, PMUs, symbols or permissions
are coverage gaps; do not install profilers or relax host security by default.

## Investigate and improve

Follow the observed path into relevant public APIs, exact-version implementation, ownership,
layout and generated code. Distinguish CPU work from waiting, allocation churn from live memory,
and reduced instruction counts from faster completion. A sample-share increase can result from
other work disappearing. Missing stacks or dropped events remain limitations.

Prefer less repeated parsing, copying, formatting, allocation, synchronization and I/O. Test
data layout or batching only with locality, lifetime, latency and memory consequences understood.
Do not assume iterator vs loop, stack vs heap, static vs dynamic dispatch, or one allocator
always wins. Avoid blanket inlining, cache-line padding, unchecked indexing and new runtimes.

For algorithm or collection candidates, use the shared [data-structure review](../perf-system/references/algorithms-and-data-structures.md)
when available. Compare operation mix, ordering, hashing trust, allocation and invalidation;
use version-matched standard-library contracts as the fallback. Suggestions remain hypotheses.

For SIMD, unsafe code, atomics, mmap or FFI changes, retain a trustworthy scalar/previous oracle
and the relevant invariants: bounds/tails, alignment, aliasing, overflow/FP semantics, CPU feature
dispatch, lifetime, synchronization and cancellation. Never weaken validation, panic behavior,
memory ordering or portability solely to improve a score. Use a few checks aimed at the changed
mechanism and preserve required owning checks; sanitizers/Miri/loom can supplement supported
cases but their runtime is not a performance baseline.

## Decide from comparable results

Repeat bounded representative workloads, including relevant input growth and concurrency. Keep
cold start and warm steady work separate. Define benchmark setup/destruction boundaries; use
runtime-like inputs and consumed outputs, and inspect suspiciously tiny measurements for removed
work. Interleave baseline/candidate runs when drift matters. A microbenchmark improvement is a
lead until the real operation improves without consequential regressions.

Retest the shipping configuration without heavy diagnostics. Report commands, build/workload
identity, before/after values and variability, correctness evidence, tradeoffs and unmeasured
paths. Classify the change as accepted, regressed, inconclusive or not verified. Keep simpler
code when measured benefit does not justify the complexity.

Save compact redacted findings and reproduction commands. Stop owned profilers/children, remove
temporary instrumentation and task-owned traces, scratch binaries and isolated target/cache
directories, and restore task changes even on failure. Preserve shared Cargo caches, existing
build artifacts, reference PDFs and evidence still required for unresolved failures. Verify and
report leftovers. [Source basis and version limits](references/sources.md).
