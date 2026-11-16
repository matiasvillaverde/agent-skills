# Kernel selection and correctness

Use after identifying consequential kernels/communication in a representative timeline.
The objective remains the complete operation with its existing quality and resource contract.

## Select the smallest applicable change

Prefer an existing supported implementation or compiler fusion before custom code. Distinguish
Triton the GPU language/compiler from NVIDIA Triton Inference Server. CUTLASS/CuTe, cuBLAS,
cuDNN, PyTorch SDPA, FlashAttention and FlashInfer have different roles and compatibility.
Check the selected implementation's actual GPU capability, toolkit/driver, dtype, head dimensions,
mask, stride/layout, alignment and build requirements; a family name such as Blackwell is insufficient.
Record unsupported combinations and fallbacks instead of forcing an incompatible fast path.

For fusion/layout/tiling candidates, measure avoided global-memory traffic and launches against
extra conversion, registers, shared memory, spills, temporary storage and compile cost. Keep
one bounded hypothesis per experiment. High occupancy, FLOPS, large blocks or newer hardware
do not establish faster end-to-end execution. Test all materially different GPU/workload cohorts.

Autotuning executes candidates repeatedly. Reset/restore mutable buffers and RNG state where
the intended contract requires it, prevent external effects, and bound configurations/time/memory.
Separate first-use tuning/JIT from warmed timing; confirm measured launches are the final kernel.

## Preserve numerical and application semantics

Keep an independent reference and operation-specific tolerances before optimizing. Exercise
real shapes plus relevant tails, empty/degenerate inputs, strides, padding, masks, aliasing,
extreme magnitudes, reductions, NaNs/infinities and accumulation precision. Select meaningful
cases for the operation; do not blindly generate every Cartesian combination.

Attention replacements must preserve query/KV length handling, causal/window masks, head ratios,
positional operations, layout, cache page tables and output semantics. Verify supported inputs
and fallback behavior. Include cache planning, conversions and memory overhead in final timing.
For CUDA graph wrappers, apply [buffer ownership and planning rules](compilation-and-graphs.md).

Do not force TF32, flush-to-zero, approximate math or lower precision and then weaken the oracle
to agree. Never seed RNG from `data_ptr` or other allocation accidents. Approximate kernels,
sparsity, quantization and different sampling can change product quality; they are not transparent
performance substitutions. Keep changes within an established quality budget or present them
as a separate product tradeoff requiring the appropriate decision.

Autocast chooses operation-specific types; indiscriminate `.half()` is not equivalent. For
quantization, verify the backend's supported format/granularity, calibrate with representative
data when required, and evaluate held-out task quality separately. Record model/calibration/scales,
export, runtime and hardware identity. Calibration examples with random data or a fixed sample
count do not establish deployment-quality calibration. Include dequantization, sensitive-layer
fallback and conversion cost. A kernel-level close result cannot establish model-level quality.

Load only trusted compiled kernels and engines. TensorRT engine deserialization executes native
code; retain existing artifact integrity and compatibility controls. Inspect context/thread ownership,
workspace/runtime limits and failure recovery rather than treating an engine as a portable data file.

## Check memory and synchronization errors

Inspect installed `compute-sanitizer --help`, version/support and existing test entrypoints first.
Use a small reproduction with known executed kernels and inputs. Choose the tool for the suspected
failure, then broaden only when changes or evidence justify it:

| Tool | Useful coverage | Limit |
| --- | --- | --- |
| `memcheck` | Invalid/misaligned accesses and relevant allocation/API errors | Not numerical correctness or a general race detector |
| `racecheck` | Shared-memory access hazards | Not proof of absence of all global-memory or host races |
| `initcheck` | Reads of uninitialized global memory | Does not replace memory-access checking |
| `synccheck` | Misuse of synchronization primitives | Not application-level dependency correctness |

Select `--tool TOOL` and set `--error-exitcode 1` (or another deliberately chosen nonzero code):
the default zero can let an otherwise successful application hide sanitizer findings from CI.
Also inspect application exit, startup/injection failures, filtered processes/kernels and launch
coverage. A report with zero errors and zero relevant launches is not a pass. Preserve enough
private evidence to distinguish errors from unsupported tooling or a timeout.

Use line information for source attribution where supported. Debug builds or forced blocking
change execution; forced blocking can reduce error reporting. Sanitizer runs are not performance
benchmarks. Fix the reproduction, check the affected cases, then run the uninstrumented workload.

## Communication mechanics

Batch small collectives/P2P only when rank ordering, buffers and latency requirements permit.
Group reuse requires matching membership/lifetime; removing a barrier requires proof of the
remaining dependency, not a rule that forward-pass barriers are always redundant. Reduce-scatter
is applicable only when consumers actually need shards instead of the full reduction.

With asynchronous collectives, establish the required `Work`/stream dependency before consuming
or recycling the result. In PyTorch CUDA collectives, `wait()` orders completion on the active
stream; a consumer on another stream needs the correct dependency too. Overlap independent work,
not a layer reading an unfinished reduction. Confirm behavior against the installed API and
timeline; private coalescing APIs are not stable cross-version instructions.

## Primary references

Reviewed 2026-11-16. These are compatibility/method sources, not universal speedup claims.

- [Triton fusion tutorial](https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html) and [autotune state mutation](https://triton-lang.org/main/python-api/generated/triton.autotune.html)
- [CUTLASS/CuTe overview](https://docs.nvidia.com/cutlass/latest/overview.html)
- [FlashAttention pinned version/hardware guidance](https://github.com/Dao-AILab/flash-attention/blob/328dd7b5a6905c75500a9bce334ac012763409a9/README.md)
- [FlashInfer v0.7.4 decode source](https://github.com/flashinfer-ai/flashinfer/blob/v0.7.4/flashinfer/decode.py)
- [PyTorch 2.15 AMP](https://docs.pytorch.org/docs/2.15/amp.html)
- [TensorRT 11.4.1 quantization](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/quantized-types-workflows.html) and [engine practices](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/best-practices.html)
- [Compute Sanitizer tools/options](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html)
- [PyTorch async collective semantics](https://docs.pytorch.org/docs/2.15/distributed.html#synchronous-and-asynchronous-collective-operations)
