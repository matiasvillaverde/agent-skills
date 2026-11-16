# Compilation, host overhead and CUDA graphs

Use when the timeline suggests CPU submission, synchronization, allocation, compilation or
graph management contributes to the real operation. Confirm installed APIs before applying
examples: PyTorch and kernel libraries change graph support between releases.

## Establish runtime behavior

- Record GPU model/compute capability, driver, CUDA runtime, framework/compiler, kernel-library
  versions and build flags. Identify device/process ownership, workers, stream topology and
  representative shape, stride, dtype and concurrency distributions.
- Keep `model.eval()` distinct from gradient control. `inference_mode()` does not disable
  dropout or select batch-normalization evaluation behavior. It is thread-local, restricts
  later autograd use of its tensors and disables forward-mode AD. Use the appropriate mode
  in the actual worker; keep `no_grad()` where its less restrictive contract is required.
- Preserve output semantics, RNG/sampling, masks and normalization. Precision policy requires
  [kernel and task-quality validation](kernels-and-correctness.md), not just successful execution.
- Separate model load, compilation/autotuning, warmup, first accepted request, steady execution
  and new-shape costs. Record cache hits/misses and peak allocated/reserved/device memory.

## Diagnose before compiling

Correlate CPU ranges and CUDA APIs with the GPU timeline. Repeated scalar reads (`item()`),
logging, tensor-to-CPU conversion, data-dependent host branches, allocation and small launches
are leads, not automatic defects. A required CPU decision may be on the critical path.
Avoid summing overlapping CPU/GPU durations or treating low utilization as proof of launch cost.

Try the smallest supported compiled region with an eager baseline. Inspect graph breaks,
guards, recompiles, fallback and cold latency using the installed compiler's diagnostics.
`fullgraph=True` demands one captured graph; it is useful for finding breaks but not a universal
production default. Dynamic tracing may still specialize. Compare relevant compiler modes
including their memory and autotuning costs. `reduce-overhead` may use CUDA graphs and cache
workspace; a mode name is not evidence of a win. Do not disable guards to hide recompile issues.

Key cache identity to the compiler/runtime, target architecture, model/configuration, dtype,
shape guards and other actual compatibility inputs. Keep the existing artifact owner and
invalidation rules; never share executable caches from untrusted sources. Measure bounded
shape sets before adding buckets: padding, graph pools and compilation can exceed the saved work.

## Capture and replay safely

Use the existing supported graph integration before hand-writing capture machinery. Capture
only a region with a demonstrated benefit; leave unsupported preprocessing/control flow eager.

1. Warm up the actual operations outside capture on a suitable side stream; establish its
   dependencies. A fixed iteration count is not proof that JIT/autotuning or allocations ended.
2. Coordinate process-wide capture: only one capture at a time and no unrelated uncaptured
   CUDA work from another thread. Follow the installed runtime's capture constraints.
3. Keep input/output, workspace and metadata buffers alive. Captured tensor shape/layout and
   virtual addresses remain fixed. Copy new values into the correct static inputs, then replay.
4. Protect each request's input copy, replay and output consumption as one ownership lifecycle.
   Copy/consume output before later replay overwrites it. CUDA orders repeated launches of the
   same executable graph; that alone does not protect surrounding buffer operations.
5. Budget all shape/batch buckets and private graph pools. Share pools only with proven compatible
   order and nonconcurrency. Define unsupported-shape and exhausted-capacity behavior: use an
   existing correct eager route or reject visibly, rather than silently capturing more graphs.
6. Test new shapes, repeated reuse, concurrent requests, cancellation and errors before accepting
   the change. Do not recycle buffers until all streams and transfers that use them have completed.

CPU work is not replayed. CPU synchronization (including scalar reads) cannot be captured.
Ordinary dynamic control flow is prohibited; supported GPU `torch.cond` is a version-specific
exception, not general permission for host branching. Multistream capture must branch from
and rejoin the original capture stream. Raw CUDA graph objects are not thread-safe.

Preserve random-generator semantics. Use documented graph-safe generator handling where
needed; never derive seeds from addresses or replace required randomness with a constant.
Test intended repeatability and stream independence rather than requiring identical random
outputs under every scheduling change.

FlashInfer and similar wrappers have separate planning and execution contracts. For example,
v0.7.4 paged-decode graph mode fixes batch size and auxiliary-buffer capacity; `plan()` remains
outside capture and `torch.compile`. Inspect the exact wrapper/backend/version, not a similar
API name. Include planning, metadata transfers and recapture in end-to-end cost.

## Transfer and synchronization changes

`non_blocking=True` is not proof of overlap. Keep pinned host inputs unchanged/alive until H2D
completion and wait before CPU access to asynchronous D2H output. Use the narrowest correct
stream/event dependency; a device-wide synchronize is a diagnostic, not the default hot-path fix.
Account for pinning/copy cost and pinned-RAM growth. Moving logging or scalar reads outside a
kernel loop still has request cost. Replacing a host branch with `where` may compute both paths;
replacing ragged selection with masking may change shape and semantics.

Validate correctness and original unprofiled request performance after each selected change.
Retain only improvements beyond noise and maintenance cost. Follow the parent skill's cleanup:
remove exact task-owned capture and isolated cache paths, preserving shared caches and artifacts.

## Primary references

Reviewed 2026-11-16; use installed-version counterparts when they differ.

- [PyTorch 2.15 inference mode](https://docs.pytorch.org/docs/2.15/generated/torch.autograd.grad_mode.inference_mode.html)
- [PyTorch 2.15 compile](https://docs.pytorch.org/docs/2.15/generated/torch.compile.html)
- [PyTorch CUDA graph constraints](https://docs.pytorch.org/docs/2.15/notes/cuda.html#cuda-graphs)
- [CUDA Graph APIs and lifetimes](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html)
- [PyTorch pinned/nonblocking transfer correctness](https://docs.pytorch.org/tutorials/intermediate/pinmem_nonblock.html)
- [FlashInfer v0.7.4 decode implementation](https://github.com/flashinfer-ai/flashinfer/blob/v0.7.4/flashinfer/decode.py)
