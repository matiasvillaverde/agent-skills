---
name: perf-rust-cli
description: Measure and improve Rust CLI startup, command latency, streaming throughput, and memory use while preserving output and process behavior.
license: MIT
---

# Rust CLI performance

Start with the requested audit, measurement, or optimization. Name the command, input, metric, correctness contract, and experiment budget. Separate process startup, time to first useful output, total runtime, throughput, peak memory, and binary size. Optimize the metric that matters; faster parsing does not establish a faster command.

For a demonstrated CPU/cache, allocator, async-runtime or code-generation bottleneck, the
available `perf-rust` skill adds low-level investigation. Keep this skill's command/output
and process-lifecycle requirements when using that guidance.

## Measure the actual command

Build outside the timed region and run the executable directly. Record baseline and candidate paths/revisions, Rust toolchain, target, features, Cargo profile, relevant flags, arguments, input, environment, working directory, and output destination. Compare equivalent optimized builds. Debug builds can explain behavior but cannot stand in for release performance. Keep symbols for profiling; enable frame pointers only when needed, record that change, and recheck the shipping configuration.

Distinguish a fresh process from a cold filesystem or application cache. Warmup establishes a warm workload; it does not measure cold startup. Define each relevant condition explicitly and use isolated fixtures. Do not clear machine-wide caches, disable SIP, relax profiling permissions, or generate production/paid network traffic merely to benchmark.

Use an existing whole-command tool such as hyperfine, checking its installed version and help. Set shell behavior deliberately: direct execution avoids shell overhead, while pipelines and redirection require the intended shell. Include subprocess and output costs when they belong to the user operation. A null output sink, pipe, file, and terminal exercise different behavior. Fix the sample budget before comparing, retain variability, and account for execution-order drift instead of rerunning until results look favorable.

## Locate the cost

Choose the smallest useful observation. CPU sampling with available samply, perf, or Instruments can locate compute; syscall/I/O evidence, request counts, and wait timing can reveal repeated reads, child launches, network round trips, or blocking. Keep profiler overhead separate from end-to-end timings.

For memory, distinguish allocation churn, live allocations, retained capacity, mapped pages, and peak RSS. Use an appropriate available allocation profiler such as DHAT or heaptrack when needed. State whether measurements include children; a maximum individual-process RSS is not a simultaneous process-tree total. Compare representative input growth and repeated work when retention is suspected. High RSS alone does not prove a leak, and fewer allocations do not prove lower peak memory.

## Change only the demonstrated bottleneck

Prefer removing repeated initialization, parsing, formatting, copies, subprocesses, or requests. Stream growing data when semantics permit; bound records, queues, reorder buffers, captured child output, and concurrency together. Reusing a buffer retains its capacity, so account for an unusually large item.

For repeated small writes, consider locking stdout and buffering; preserve interactive latency, byte fidelity, backpressure, and final flush errors. Drain child stdout and stderr without deadlock, observe exit status, and stop/reap owned children on cancellation. For an existing async runtime, keep blocking work off executor threads and bound it; started Tokio blocking tasks cannot simply be aborted. Preserve ordering, deadlines, and retry limits.

Treat LTO, CPU tuning, allocators, SIMD, unsafe code, and new runtimes as separate evidence-backed choices, including portability and maintenance costs. Do not change panic, validation, or error semantics to improve a benchmark.

## Verify and report

For algorithm or collection candidates, use the shared [data-structure review](../perf-system/references/algorithms-and-data-structures.md)
when available. Include one-shot construction and teardown, streaming bounds and exact output
order; a faster warm lookup may lose in a short-lived command.

For implementation, use the existing harness and a few checks that exercise the changed mechanism. Compare the binary's exit status, stdout/stderr, and file effects; use exact bytes where required. Add short-write, late-flush, broken-pipe, slow-consumer, cancellation, or oversized-input checks only when the change can affect them. Keep fixtures, capture, timeouts, and child cleanup bounded.

An isolated microbenchmark needs realistic inputs and observable results; it supplements the command measurement. Keep a change only when the improvement exceeds noise and earns its complexity. Report commands, workload, build/cache conditions, before-and-after measurements, correctness evidence, and limits; retain the simpler implementation when evidence is inconclusive.

## Finish and clean up

Save the measurements and reproduction commands, stop/reap owned profiler and benchmark children, and remove task-created captures, scratch inputs/outputs, temporary binaries and isolated target/cache directories. Track exact task-owned paths; preserve shared Cargo caches, existing build outputs and user data. Remove temporary instrumentation and restore settings even on failure or cancellation. Keep only requested/required evidence or the minimum needed for unresolved failures. Verify cleanup and report any leftovers with the reason.

Adapted from [Dankosik's Rust CLI skills](https://github.com/Dankosik/rust-cli-skills/tree/aafca337dece65f312faaecd0fe9ee1c81f755df) (MIT). Check version-matched [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), [hyperfine](https://github.com/sharkdp/hyperfine#usage), [BufWriter](https://doc.rust-lang.org/std/io/struct.BufWriter.html), and [Tokio blocking-task semantics](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html) when those details apply.

Sources, modifications and licensing: [NOTICE.md](NOTICE.md).
