# Zig allocation, kernels and I/O

## Establish lifetime and observation boundaries

Identify each allocation's owner, capacity, initialized range, invalidation points and lifetime
end. Slices borrow storage; growing a container can invalidate pointers; copying a container
header does not create independent ownership. Check cleanup on success, error and cancellation.
Allocator thread safety does not make the container or arena reset thread-safe.

Use the exact compiler's allocator API. Tagged Zig 0.17.1 deprecated `DebugAllocator` in favor
of `SafeAllocator`, while its language reference still showed the older recommendation. In that
version, `SafeAllocator.deinit()` returns a `usize` leak count, not the old `.ok/.leak` result.
Inspect options and backing-allocator requirements rather than pasting a remembered recipe.
Do not silently upgrade an older repository to these APIs.

Measure allocation requests, backing allocator calls, total requested bytes, peak/live bytes,
retained capacity and process RSS as different quantities. An outer wrapper around an arena's
backing allocator sees different work from a wrapper around the application's request allocator.
Run leak checks after the intended frees/defers, while the necessary diagnostic state still exists.
Allocator instrumentation can change locking, layout, reuse and timing; remeasure the shipping
allocator without it.

Arena reset modes can free storage, retain capacity, or retain up to a limit. Verify which one
is used and that no references survive reset/deinit. Test a representative large burst followed
by small requests when high-water retention matters. Grouping lifetimes can reduce allocation
calls without bounding memory. Do not replace arenas, fixed buffers, safe allocators or scalable
allocators by policy: measure lifetime, contention and retained-memory tradeoffs.
Check reset/shrink return values and actual capacity against the owning budget; requesting a
retention limit does not prove it was met on an allocation-failure path. Include allocator
bookkeeping and other scratch stores when the budget covers them.

## Layout and SIMD

Measure `@sizeOf`, `@alignOf`, stride and access patterns on the actual target. Consider hot/cold
separation or AoS/SoA only for a measured access cost; include conversion, extra storage and
ownership overhead. Cache-line padding can help independent writers yet worsen bandwidth/cache
footprint. Packed representation is a layout/ABI choice, not a promise of faster access.

Retain a scalar/reference implementation with independently checked outputs. A `@Vector` may
lower to one instruction, multiple instructions or scalar operations. `std.simd` width suggestions
are heuristics dependent on CPU and backend. Inspect generated code and measure multiple relevant
sizes, including tails and boundary lengths; wider is not automatically better.

Preserve overflow/widening, FP reassociation/NaN/rounding, first-match/tie order, legal aliasing,
alignment and initialized range. Masking the result of a load is not proof that an out-of-bounds
load was safe. Arrays and vectors have different representation guarantees; do not use unsupported
pointer reinterpretation. Match CPU-feature dispatch and scalar fallback to deployment targets,
including the build flags used to compile the fallback.

## Scheduling and I/O

Use operation IDs/spans and OS states to distinguish running, runnable and blocked work. Inspect
the actual version's I/O/executor APIs and cancellation semantics; don't transplant a historical
Zig async example or another language runtime's model. Bound task fan-out, queues and output
retention. Batch size needs a wait/deadline bound as well as a throughput target.

Count actual calls/bytes through completion, including short reads/writes, flush/fsync, retries,
page faults and cancellation. mmap does not eliminate faults, file-lifetime concerns or copies
elsewhere. Zero-copy buffers must remain valid until the consumer completes. Direct I/O,
io_uring, CPU affinity, huge pages and NUMA placement need target-specific evidence and deployment
authority; do not make hidden global changes from a library optimization.

Check relevant error paths and races with a few meaningful tests. Safety-enabled execution can
find illegal behavior but is not proof that every lifetime/race bug is absent. Compare optimized
builds under equivalent semantics and confirm the real workload, not only a tiny kernel.

Sources, read at tag 0.17.1:
[allocator exports](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/heap.zig),
[SafeAllocator](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/heap/SafeAllocator.zig),
[arena reset](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/heap/ArenaAllocator.zig),
[scalable allocator](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/heap/SmpAllocator.zig),
[SIMD heuristics](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/simd.zig), and
[language semantics](https://ziglang.org/documentation/0.17.1/) (vectors, ownership and illegal behavior).
These are versioned findings, not permanent API names for every Zig project.
