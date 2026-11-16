# Translate candidates into the actual runtime

Read this after [choosing an algorithm or representation](algorithms-and-data-structures.md).
Use the repository's selected versions and existing dependencies. These are candidates to
investigate, not instructions to add packages or replace every collection. Include construction,
conversion, mutation, iteration, destruction and peak/retained memory in the relevant workload.

## Swift and Apple clients

Start with the standard `Array`, `Dictionary` and `Set`. Investigate repeated front removal,
membership scans, repeated sorting, copying shared collections and unnecessary bridging when
they appear in the measured path. A queue may benefit from a deque; order-preserving uniqueness
needs different semantics from an unordered set. Preserve SwiftUI identity, ordering and observable
state behavior while changing backing storage.

[Swift Collections](https://github.com/apple/swift-collections/blob/88754449ab766a739610b660e117762115fabc9c/README.md)
provides deque, ordered, heap, bitmap and persistent hashed collections. CHAMP-based tree collections
are candidates for frequently mutated shared snapshots, not sorted-key range indexes. Check the
resolved package's public APIs and minimum compiler requirements; the reviewed main-branch README
also contains explicitly unstable features. Do not enable preview traits just to obtain a container.
Measure copy-on-write and ARC costs with realistic sharing. The [original deque comparison](https://www.swift.org/blog/swift-collections/)
also explains the tradeoff against contiguous arrays; its old hardware charts are not current app
speedup predictions. Use Instruments for the real interaction, not just a collection microbenchmark.

## Rust

Use the standard [collection operation table](https://doc.rust-lang.org/std/collections/) to select
`Vec`, `VecDeque`, `HashMap`, `BTreeMap` or `BinaryHeap` by operations and required order. Distinguish
expected and amortized bounds. A contiguous scan can remain appropriate for small inputs; a sorted
vector trades costly updates for compact lookup/range access. An entry API can avoid redundant
lookups, but preserve ownership and error behavior.

[HashMap's contract](https://doc.rust-lang.org/std/collections/hash_map/struct.HashMap.html) includes
key equality/hash invariants and default HashDoS resistance. Do not replace its hasher for
attacker-controlled keys solely to win a benchmark. Current iteration visits capacity, not just
live length: over-reserving can hurt scans and memory. Validate borrow/iterator invalidation and
stable-address requirements before changing storage; measure key cloning, allocations and drop cost.

## Go services

Consider slices, maps, sorted slices and the existing heap implementation before a custom concurrent
container. Preserve output order explicitly; map iteration cannot supply a stable presentation or
wire order. Include GC scanning/retention, allocation rate and synchronization cost, with realistic
request concurrency and cancellation. A slice-based queue must release obsolete references when
retention matters, and preserve backpressure rather than silently dropping work.

The official [Go Swiss-table account](https://go.dev/blog/swisstable) explains the Go 1.24 map
implementation and why growth is divided among bounded tables to limit insertion pauses. It does
not establish that all languages' Swiss tables share these properties or that every lookup workload
improves. Verify the deployed runtime; replacing a modern built-in map with an older custom one
needs evidence. Use `benchmem`, profiles and service measurements for their different scopes.

## Python

Use implemented containers and algorithms before a Python-level reimplementation. The documented
[deque](https://docs.python.org/3/library/collections.html#collections.deque) supports efficient end
operations, whereas list front insertion/removal moves elements. A bounded deque evicts items;
that changes correctness for a work queue. Individual thread-safe operations do not make a compound
check-and-pop protocol atomic.

[Bisect](https://docs.python.org/3/library/bisect.html) can find an insertion point cheaply, but
list insertion remains linear and comparison semantics differ from an equality lookup. Consider
heaps for repeated priority extraction or bounded top-k, preserving ties and final output order.
Include Python/native conversion and object overhead. A set/index must retain the original duplicate,
equality and ordering semantics; dictionary construction commonly retains a different duplicate
than a first-match search. Hashability, NaN/identity behavior and eager evaluation can also differ
from an explicit equality scan. Establish the accepted input contract and recheck the full operation.

## TypeScript and JavaScript

TypeScript annotations do not choose runtime storage. Start with arrays, `Map`, `Set` and suitable
typed arrays. Preserve key identity, missing values, insertion order and numeric representation.
The [ECMAScript Map/Set specification](https://tc39.es/ecma262/2025/multipage/keyed-collections.html)
requires average sublinear access, not a universal O(1) guarantee; its pseudocode is not an engine
implementation. Index construction and update invalidation can outweigh repeated scans on small
or one-shot inputs. Typed-array conversion can change precision or integer wrapping.

For V8, [elements kinds](https://v8.dev/blog/elements-kinds) explain packed/holey and value-type
specialization. The article's 2025 update adds an exception to an older one-way-transition claim;
do not turn historical engine internals into timeless lint rules. Measure the deployed Node or
browser engine, warmup and GC. Keep request/event-loop latency separate from inner-loop throughput.

## Zig, C and C++

Inspect version-matched container source and allocator/lifetime contracts. Contiguous arrays,
hash or ordered indexes, bitsets and field-separated storage are candidates. In Zig, verify the
actual `ArrayHashMap` removal ordering and pointer invalidation and `MultiArrayList` layout before
using them; API names and allocator plumbing vary by release. Zig's canonical source is now
[Codeberg](https://ziglang.org/news/migrating-from-github-to-codeberg/); the frozen GitHub repository
is historical, not a current standard-library reference. Installed standard-library sources are a
useful fallback when remote documentation is unavailable.
The [0.17.1 array-map source](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/array_hash_map.zig)
and [field-separated list source](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/multi_array_list.zig)
were inspected: removal order/cost, allocation-triggered invalidation and selected-field access
are consequential, while some old constructor names are deprecated. No Zig execution was tested.

In C/C++, measure the chosen implementation and value sizes. Dense/flat containers can invalidate
addresses that node storage preserved. Do not copy private library internals or introduce an
unmaintained container to avoid a small dependency without evaluating licensing, portability and
maintenance. Reuse the precise invalidation and locality references in the shared candidate guide.

## CUDA and other GPU paths

Map data layout to thread access, not just host collection APIs. Contiguous/coalesced access,
tiling, sparse representations and batching can change bandwidth use, but include conversion,
host-device transfers, synchronization and temporary storage. Preserve numerical order/tolerances
and sparse-index semantics. NVIDIA's [coalescing guidance](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#coalesced-access-to-global-memory)
ties transactions to access patterns and device capability. SoA is a hypothesis, not a universal
rule; inspect actual warp access and cache reuse. Qualify with the target GPU's profiler and the
complete operation. CUDA evidence does not establish Metal performance.

Sources reviewed 2026-11-15. Moving documentation can describe newer releases than the project;
the Rust collection index and detailed API page even returned different version headers during
this review. Follow the selected release for applicability. No cross-language benchmark or
universal container ranking is claimed here.
