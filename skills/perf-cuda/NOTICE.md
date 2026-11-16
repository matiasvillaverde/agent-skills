# Source and adaptation notice

Reviewed and modified on 2026-11-13 for the shared personal skill library.
Original local instruction prose informed by the following pinned sources; this
is not an unmodified upstream installation or an upstream endorsement.

- [NVIDIA/TensorRT-LLM / .claude/skills/perf-nsight-systems](https://github.com/NVIDIA/TensorRT-LLM/blob/b66427ab720009a226718b6bb28e9ab317f26f24/.claude/skills/perf-nsight-systems/SKILL.md), Apache-2.0.
- [NVIDIA/TensorRT-LLM / .claude/skills/perf-nsight-compute-analysis](https://github.com/NVIDIA/TensorRT-LLM/blob/b66427ab720009a226718b6bb28e9ab317f26f24/.claude/skills/perf-nsight-compute-analysis/SKILL.md), Apache-2.0.

Changes:
- Combine system timeline and targeted kernel diagnosis; preserve asynchronous timing, lifetimes and numerical correctness.
- Treat occupancy/SOL as evidence, not universal targets; no automatic host privileges, clock changes or monitoring disruption.

## Inference and correctness extension — 2026-11-16

The two focused references are original local synthesis, with primary API/documentation links
in each file. They add compilation/capture ownership, shape/cache costs, transfer dependencies,
kernel selection, numerical/task-quality gates, quantization and scoped Compute Sanitizer use.
No additional upstream code, commands, bundled tools or companion skills were copied.

Community source review informed the questions and exposed advice that is deliberately rejected:
fixed utilization/block/tolerance thresholds, pointer-derived RNG, changing a correctness reference
to match TF32 error, and consuming asynchronous collective output before its dependency.

- [TensorRT-LLM CUDA graphs](https://github.com/NVIDIA/TensorRT-LLM/blob/071f9ab8c660a71e152de7710566dc11f1805ae8/.claude/skills/perf-torch-cuda-graphs/SKILL.md), [sync-free execution](https://github.com/NVIDIA/TensorRT-LLM/blob/071f9ab8c660a71e152de7710566dc11f1805ae8/.claude/skills/perf-torch-sync-free/SKILL.md), [host optimization](https://github.com/NVIDIA/TensorRT-LLM/blob/071f9ab8c660a71e152de7710566dc11f1805ae8/.claude/skills/perf-host-optimization/SKILL.md) and [Triton kernels](https://github.com/NVIDIA/TensorRT-LLM/blob/071f9ab8c660a71e152de7710566dc11f1805ae8/.claude/skills/kernel-triton-writing/SKILL.md).
- [NVIDIA Compute Sanitizer skill](https://github.com/NVIDIA/skills/blob/894f2d7dfee49085e84e21c1aad2513bc44a5b6d/skills/compute-sanitizer-diagnose-cuda-bugs/SKILL.md) and [cuTile performance skill](https://github.com/NVIDIA/skills/blob/894f2d7dfee49085e84e21c1aad2513bc44a5b6d/skills/tilegym-improve-cutile-kernel-perf/SKILL.md).

These references do not adopt upstream runtime, privilege, installation, reset or commit instructions.
No GPU experiment was performed while authoring them; a source-checked workflow is not a measured
speedup or model qualification. The existing skill license and attribution below remain unchanged.

The applicable upstream permission and copyright text is retained in [LICENSE](LICENSE).
No upstream executable, plugin, hooks, bundled profiler or missing companion skill is included.
Platform tools are runtime requirements to inspect when applying the skill.

Copyright (c) 2011-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
Both source skills declare Apache-2.0. The included license retains the relevant
Apache portion of the pinned root license. Its separate third-party exceptions apply
to other code paths, including LTX-2, none of which is included here.
