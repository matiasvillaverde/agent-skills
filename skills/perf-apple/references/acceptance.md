# Accepting an Apple performance change

Use this before changing code and when deciding whether to keep the result. These are local
acceptance rules; linked Apple guidance informs measurement, not a universal product budget.

## Define the result before optimizing

Record a compact contract in the task's existing notes:

| Field | What to establish |
| --- | --- |
| Operation | User-visible start/end, representative input size, concurrency and lifecycle |
| Environment | Device/chip, OS, app revision, compiler/build flags, display refresh, power/thermal state |
| Baseline | Cold, first-use and warm populations separately; repetitions, units and variability |
| Target | Existing SLO or regression budget; relevant statistic and minimum worthwhile improvement |
| Invariants | Observable behavior, UI, accessibility, output quality, correctness and resource ownership |
| Guardrails | Relevant memory, CPU, GPU, energy, I/O, requests, errors and maintenance cost |

Use the product's existing budget. If none exists, establish a baseline and state a provisional,
workload-specific target; do not invent a universal percentage or silently turn that target into
product policy. A measured improvement can be reported while the absolute product budget remains
unassessed. A successful recording or an instrument with no warnings is not an acceptance result.

## Preserve the product

Performance work preserves observable behavior unless the user explicitly includes a product
change. In particular, preserve:

- Layout, typography, colors, images, visual effects, animation design, navigation, scrolling
  position and state. Faster completion is intended; removing UI or changing its presentation is not.
- Accessibility semantics, focus, keyboard/touch interaction, hit targets, Dynamic Type, reduced
  motion and supported localization behavior on affected paths.
- Results, ordering guarantees, data freshness, persistence/durability, offline behavior, errors,
  retries, cancellation, background transitions, privacy and security checks.
- Audio/video fidelity and timing, model/task quality, supported hardware/OS fallbacks and public
  API contracts. Preserve existing numerical/perceptual tolerances instead of demanding irrelevant
  bitwise equality or relaxing tolerances to make the optimization pass.

Do not manufacture a win by lowering resolution or refresh rate, removing effects, dropping work,
reducing model precision, hiding errors, weakening synchronization, or reporting completion before
the operation is usable. Such tradeoffs are separate product decisions. Caches and prefetching
must retain invalidation, cancellation, freshness and bounded resource use.

Verify affected behavior with the existing integration/UI harness and appropriate visual or
accessibility comparisons. Exercise the critical normal path plus failure, cancellation or
teardown paths affected by the change. Reuse tests; add a small regression test only where it
catches a meaningful failure. Screenshots alone do not verify interaction or accessibility.

## Select acceptance evidence by workflow

All 17 catalog modes have a measurement and a corresponding correctness check below. Choose the
rows implicated by the change; there is no requirement to run every instrument or every test.

| Mode | Useful acceptance evidence | Reject or investigate the apparent win when… |
| --- | --- | --- |
| `cpu` | Absolute CPU work and end-to-end time per operation; representative throughput | Only sample share fell; work moved to another process/resource; output changed |
| `scheduling` | Interaction delay, blocked/runnable intervals, wakeups and completion tails | Busy-waiting, priority escalation or extra threads hide contention or starve other work |
| `concurrency` | Completion latency, task count, queue growth and cancellation completion | Fan-out is unbounded; actor isolation, ordering, backpressure or cancellation breaks |
| `memory` | Peak footprint plus post-warmup lifecycle trend; retaining owners and release | A short leak-free trace hides persistent growth, excessive caching or invalid ownership |
| `launch` | Cold and warm time to first usable content, plus first interaction | Work was moved just beyond the measurement endpoint or required content is missing |
| `scroll` | Hitch frequency/duration and frame pacing during the same gesture/content | Average FPS hides stalls; appearance, scroll state or intended animation changed |
| `swiftui` | Update causes/counts and expensive body/layout duration with interaction timing | Fewer updates come from stale state, incorrect identity or missing UI updates |
| `io` | Bytes/operations, descriptor lifecycle and I/O latency for equivalent work | Writes are deferred past the durability contract; descriptors or buffers accumulate |
| `persistence` | Fetch/fault/save work and latency against the same dataset | Query results, ordering, atomicity, consistency or save semantics changed |
| `network` | End-to-end and phase latency, request/byte counts, errors and retry cost | Caching serves stale results; retries amplify load; cancellation or offline behavior regresses |
| `audio` | Callback duration/jitter against the actual buffer deadline; underruns over a stated window | Format, latency, route changes or interruption handling degrade; a quiet window is called proof of no glitches |
| `gpu` | CPU/GPU frame timelines, frame pacing, resource memory and sustained work | Visual quality falls; CPU waits or retained resources increase; a faster isolated shader slows the frame |
| `spatial` | App/render/compositor or streaming deadlines on the target device | Reprojection/generated frames hide missed work; pose response or visual comfort changes |
| `energy` | Equivalent completed work over a representative sustained interval | Speed gains rely on unsustainable thermal/power conditions; incomparable device scores are compared |
| `ml` | Load/setup/inference latency, memory and compute usage on fixed inputs | Model/output quality or fallback behavior changes; estimated placement is treated as a recorded fact |
| `foundation-models` | First useful output, full completion, tool latency and token/work counts | Shorter prompts or outputs reduce task quality; streaming hides slow or incorrect completion |
| `logging` | Capture usefulness with bounded runtime, volume and cardinality overhead | Errors/audit evidence disappear, sensitive data leaks, or instrumentation dominates the workload |

For audio, frames divided by sample rate gives the buffer interval; callback work has to leave
room for the rest of the actual render pipeline. For memory there is no universal safe RSS limit;
use the device/workload budget and lifecycle evidence. Zero observed failures always needs an
exposure duration/count, and does not establish zero possible failures.

Apple gives rough responsiveness guides: discrete interaction delays become noticeable around
100 ms; 120 Hz and 60 Hz imply approximately 8.3 ms and 16.7 ms frame intervals. Main-thread work
shares those budgets with other pipeline stages; Apple's guidance says under 5 ms of screen-update
work is usually timely. These are starting points, not universal gates, and an instrument's hang
detection threshold is not an acceptable interaction budget. Use actual refresh and workload
requirements. [Apple responsiveness guidance](https://developer.apple.com/documentation/xcode/improving-app-responsiveness).

## Make a trustworthy comparison

Use the same representative workload, build configuration, symbols, device and state. Repeat
and interleave baseline/candidate runs when practical to expose thermal drift or background
interference. Document exclusions; never discard slow runs merely because they weaken the claim.
Keep cold and warm measurements separate. Report absolute values and variation as well as deltas;
use enough observations to support a claimed tail percentile, not p99 from a handful of runs.

Use traces to explain a mechanism, then time the candidate without heavy diagnostic overhead.
Apple recommends representative Release performance tests without debugger, coverage or runtime
sanitizers; keep required correctness/sanitizer runs separately. XCTest needs an actual baseline
and tolerance to evaluate regressions; a measurement without a baseline is not a passing budget.
Do not reset baselines to conceal a regression.
[Apple performance-test guidance](https://developer.apple.com/documentation/xcode/writing-and-running-performance-tests).

Compare relevant secondary costs and implementation complexity. Prefer the smallest supported
fix; avoid a new cache, custom scheduler or abstraction when a simpler correction meets the
budget. An unmeasured resource is a coverage gap, not proof of no regression. Extend existing
CI/hardware benchmarks for the critical path when stable and useful; do not multiply tiny tests
or make noisy timing gates run on uncontrolled shared hosts.

## Decide and report

Label each claim **accepted**, **inconclusive**, **regressed** or **not verified**. Accept a change
when its declared target is supported beyond observed noise, affected invariants pass, and
measured guardrails remain within budget. Narrow the claim if device, quality or resource coverage
is incomplete. Do not retain an unjustified optimization as a success; revise or revert your own
change when appropriate, preserving unrelated work.

Report operation/environment, before/after with units and repetitions, budget/noise, behavior/UI
evidence, secondary costs, and gaps. Distinguish a synthetic probe from a product benchmark and a
local improvement from fleet or production qualification. Apply the skill's artifact cleanup
rules after saving this compact evidence.
