# Sources and scope

Reviewed 2026-11-16. Original synthesis; no serving framework, upstream script, model weights,
container or cloud deployment is bundled. Check installed versions and current model recipes
before use. Pin the exact architecture and workload behind a performance claim.

- [NVIDIA Dynamo performance guidance](https://github.com/ai-dynamo/dynamo): source/serving
  critical paths, useful throughput and preserved delivery semantics. The serving reference
  links current routing, disaggregation and planner documentation.
- [vLLM official skills](https://github.com/vllm-project/vllm-skills): useful engine-native
  deployment/benchmark discovery; do not inherit unbounded load or stale default arguments.
- [NVIDIA voice-agent skill](https://github.com/NVIDIA/skills/blob/894f2d7dfee49085e84e21c1aad2513bc44a5b6d/skills/nemotron-voice-agent-builder/SKILL.md):
  read the entrypoint; useful existing-project routing, current model/profile lookup and a real
  spoken-exchange boundary. No scaffolder, fixed pipeline or repeated approval ritual is imported.
- [NVIDIA Compute Sanitizer skill](https://github.com/NVIDIA/skills/blob/894f2d7dfee49085e84e21c1aad2513bc44a5b6d/skills/compute-sanitizer-diagnose-cuda-bugs/SKILL.md):
  tool-specific correctness coverage and nonzero error exits; primary-checked mechanics belong
  to the existing `perf-cuda` references.
- [VibeVoice](https://github.com/microsoft/VibeVoice/tree/16fb2cb1217c9934a886e1948ffb06120caa2df5):
  README and Realtime design read; variant-specific ASR/TTS, streaming and diffusion/codec
  boundaries. Public installation examples are not authorization for privileged containers.
- [NVIDIA TTS benchmarks](https://docs.nvidia.com/nim/speech/latest/reference/performances/tts/performance.html):
  first/inter-chunk metrics and closed-loop test procedure, not a universal capacity target.
- [AIPerf metrics](https://docs.nvidia.com/aiperf/reference/ai-perf-metrics-reference) and
  [GenAI-Perf goodput](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/docs/goodput.html):
  distinguish request counters, arrival/stream timing, ASR input-duration RTFx and SLO-goodput.
  Model quality, playable output and semantic completeness require their own checks.

The serving reference contains focused primary papers and runtime-specific links; `perf-cuda`
owns compilation, graph and kernel sources. Avoid copying vendor benchmark numbers, occupancy
targets or tolerance examples as acceptance criteria. Current support can differ from an indexed
documentation version or a model-family checkbox.

An authorized private application source/history audit supplied additional failure hypotheses.
Only generic engineering lessons were synthesized here; private source, operational settings,
historical measurements and identifiers remain outside the shared library. Recorded history was
not rerun and is not proof of current deployment or achievable speedup.

Qualification is described in [verification](verification.md). This is a bounded source and
workflow review, not an exhaustive ranking or an executed GPU benchmark.
