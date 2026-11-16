# Qualification and execution limits

Research and source checks were performed on 2026-11-16; no actual NVIDIA inference or
profiler run was performed for this skill. Published benchmarks are source evidence,
not reproduced measurements.

Two independent agents received the selected skill and raw synthetic fixtures, without the
author's conclusions or conversation. The author inspected both resulting reports.

- **Serving trial:** a six-request, 20-second fixture compared preserved baseline, larger
  batching and fewer diffusion steps. The agent produced a reproducible standard-library
  report, retained all six offered requests and rejected faster ticks as proof of improvement.
  Baseline qualified goodput was 0.30 requests/s/GPU; larger batching was 0.10 because first
  playable audio, underrun, timeout and timestamp failures disqualified four requests. It
  marked fewer steps unqualified due to the changed contract and unreviewed quality, not
  proven bad audio. Missing admissions and small-sample percentile limits stayed explicit.
- **CUDA trial:** static review found shared graph input/output corruption, D2H-before-CPU
  completion and premature host-pool reuse, mismatched shapes, unsafe pointer-derived seeds,
  a weakened reference proposal and missing capture preconditions. It rejected a sanitizer
  zero exit accompanied by errors and subtraction of overlapping CPU/GPU totals. The report
  proposed bounded real-hardware validation without claiming to execute it.

The serving report's hashes, arithmetic and deterministic regeneration were checked. This
is bounded instruction-following evidence, not a comprehensive evaluation of all models,
GPUs or agents. Synthetic quality labels do not qualify actual speech, and a static finding
does not prove a reproduced race. Target-hardware timing, numeric/task quality, real playback,
memory stability and distributed scaling remain required when applying these skills.
