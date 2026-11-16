# Investigate and improve Metal workloads

Use after `gpu` or GPU-backed `ml` evidence identifies relevant work. Apply the
[acceptance contract](acceptance.md): preserve image/model quality, output and hardware support.
Consult the [official Metal PDFs](sources.md#apple-cpu-and-metal-references) selectively: MPP
for matrix primitives, the language specification for shader semantics, feature tables for family
capabilities. Verify actual SDK/device support before adopting a feature.

## Locate the critical path

Use Metal System Trace or Game Performance to relate CPU submission, waits, GPU execution and
presentation. Separate first-use pipeline compilation from steady work. A GPU gap may be caused
by CPU preparation, dependencies or presentation; high GPU activity alone does not locate a
bottleneck. For compute, time completed useful results, including required copies and synchronization.
[System workflow](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app).

Capture the smallest representative bad frame or compute interval in the Metal debugger, retaining
preceding work only when resource history matters. Use matching shader sources/symbols. Record
build, GPU family/device, OS, inputs, dimensions/formats, thermal/power state and capture settings.
A replay on different hardware is not a measurement of the original target. Open Summary/Insights,
profile if timing is absent, and follow timeline dependencies to the command delaying completion.
[Metal debugger](https://developer.apple.com/documentation/xcode/metal-debugger).

Record overlap and GPU performance state. Serial replay and isolated per-pass counter collection
help attribution but do not represent concurrent runtime timing. Recheck the full application under
representative conditions. [Profiling modes](https://developer.apple.com/documentation/xcode/optimizing-gpu-performance),
[counter collection](https://developer.apple.com/documentation/xcode/analyzing-apple-gpu-performance-using-counter-statistics).

## Reuse a CLI session

Inspect the installed help and manual before adapting commands:

```sh
xcrun --find gpudebug
xcrun gpudebug --help
man gpudebug
```

The reviewed Xcode 27 installation has `gpudebug` v1.0. Its manual includes `-c` command execution,
which short help omits, plus sessions, JSON, output directories and idle timeouts. A command shape:

```sh
xcrun gpudebug -t /private/task/frame.gputrace --json \
  -o /private/task/gpu-resources --timeout 120 -c 'list'
xcrun gpudebug -s '<returned-session-id>' --json -c 'list'
```

Follow returned nodes/actions with `go`, inspect state, and fetch only needed resources. Do not
guess pass/draw paths from another trace. Reuse the session rather than paying repeated trace
loading costs with `--oneshot`. Keep textures, buffers, shaders and exports private. Terminate only
the owned session when done:

```sh
xcrun gpudebug --terminate '<owned-session-id>'
```

Use the UI and label the automation gap if the CLI/operation is unavailable. CLI discovery here
was verified without a product trace; capture/replay remains workload-specific validation.
[Apple's agent workflow](https://developer.apple.com/documentation/xcode/investigating-gpu-issues-with-ai-agents).

## Test one supported optimization

| Evidence | Follow-up |
| --- | --- |
| GPU idle while completion waits | Inspect CPU preparation, submissions, dependencies and presentation before adding queues |
| Expensive/repeated passes or draws | Inspect redundant work, resource dependencies and pipeline creation; preserve required ordering/results |
| Memory/texture limiter or shader waits | Inspect access patterns, bandwidth, copies, formats and lifetime; preserve precision/quality constraints |
| Occupancy, register or threadgroup pressure | Inspect the active limiter and pipeline limits; experiment with workgroup/tile size and memory use, not occupancy as a score |
| Costly shader lines or divergence | Inspect pipeline/compiler statistics and representative inputs; reduce repeated work or improve locality with equivalent output |
| Resource growth or CPU/GPU stalls | Follow allocation and completion ownership; bounded reuse is valid only after dependent work finishes |
| First-use stalls | Separate compilation/loading from execution; account for prewarming/cache startup, memory and invalidation costs |

Counters depend on GPU family and mode. Compare relevant absolute work/time, not percentages
alone. Inspect `threadExecutionWidth`, maximum threads and threadgroup-memory limits for the
actual pipeline before changing dispatch dimensions. More threads, unrolling or buffering can
increase pressure. Unified memory does not remove resource lifetime, bandwidth or synchronization
requirements. Counter evidence is a hypothesis to corroborate with the critical path.

For MPP, hold matrix shapes/layouts, accumulation precision, tails and numerical tolerances fixed.
Compare the existing implementation with applicable library primitives before building a custom
kernel. Try tiling, cooperative work or fusion only when support and measurements justify it.
MPP GPU neural accelerators are distinct from the Neural Engine; a faster matrix kernel does not
prove faster end-to-end inference.

## Accept and clean up

Verify output and affected UI/interaction, then repeat the completed workload without heavy
capture/validation overhead. Check relevant frame pacing/latency, CPU/GPU work, footprint and
sustained thermal behavior. Compare the same measurement mode; serial replay totals cannot be
compared with concurrent runtime. Keep only improvements beyond noise and within resource budgets.
Use a small regression test for a real failure, such as odd-sized dispatch tails or premature
resource reuse; do not add exhaustive tile-size matrices to routine CI.

Report critical path, hypothesis, conditions and result. Restore capture/validation settings,
terminate owned sessions and remove task-owned traces/resource exports/isolated caches after
retaining findings. Preserve reusable PDFs, original inputs and required failure evidence.
