# Algorithms and data structures: choose by workload

Use this branch when measured work or a credible growth model points to repeated lookup,
sorting, traversal, allocation, aggregation or data movement. For an ideas-only request,
produce a short ranked set of hypotheses; do not replace containers or install a library.
There is no globally fastest structure. Prefer an existing standard-library implementation
unless a measured requirement justifies a maintained dependency or owned implementation.

## Model the operation before choosing its representation

Record input size and distribution, key/value size, read/write/iteration mix, hit/miss ratio,
reuse lifetime, concurrency and memory limit. Preserve the actual contract: ordering and
tie-breaking, first/last duplicate resolution, equality/collation, stable handles, ownership,
mutation visibility, exactness, cancellation and thread safety. A map is not a substitute
for an ordered sequence simply because both can answer a lookup.
Preserve short-circuiting and failure behavior too: eagerly indexing every record can inspect
invalid or effectful data that the previous lookup never touched.

Separate worst-case, expected and amortized costs. Hashing and equality may depend on key
length; an amortized constant-time append can still resize on a latency-sensitive operation.
Include construction, updating, conversion, destruction and retained capacity in the cost.
Use `build + queries × lookup + updates × maintenance` as a comparison model, with measured
costs when available; one lookup can favor a scan over building an index.
The [MIT interface and amortization notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/79a07dc1cb47d76dae2ffedc701e3d2b_MIT6_006S20_lec2.pdf)
and [hashing notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ce9e94705b914598ce78a00a70a1f734_MIT6_006S20_lec4.pdf)
explain the distinction between the required operations and their implementation.

## Candidate matrix

`n` is stored items, `u` the integer universe size, `k` selected items. These are candidates
to compare with the current implementation, not rewrite rules. Exact guarantees depend on
the implementation and machine model.

| Observed problem | Candidates worth testing | Conditions and costs that can reject them |
| --- | --- | --- |
| Repeated linear lookup or nested membership | Reuse a hash index; sorted contiguous storage plus binary search; direct-index array for bounded IDs | Pay build/update cost and memory. Preserve duplicates and order. Tiny or single-use collections may favor scanning. Untrusted keys need collision-resistance appropriate to the threat model. |
| Ordered lookup, ranges or expensive pointer chasing | Sorted vector for mostly static data; B/B+ tree for mutable ordered data; existing flat/node hash variants for unordered data | Sorted inserts move elements. Flat and B-tree implementations can invalidate pointers/iterators; large or expensive-to-move values can reverse a benchmark result. |
| Dense integer membership or repeated temporary sets | Bitset for dense bounded IDs and wordwise algebra; sparse-set representation for cheap reset and member iteration | Bitsets cost space in `u`, not just members. Classical sparse sets also allocate by universe size; logical clear does not automatically destroy owned objects. Swap removal changes iteration order. |
| Large integer unions/intersections with mixed density or runs | Sorted merge/galloping, plain bitmap, maintained Roaring implementation | Compare actual density, clustering, operation mix, build/serialization and conversion costs. Roaring is not a universal replacement for a small set or arbitrary string-key map. |
| Full sort solely to find minimum or a small top-k | Single pass for one extremum; bounded binary heap for streaming top-k; selection/partition for a batch | Heap top-k typically uses `O(n log k)` work and `O(k)` space; sorted output adds work. Preserve stable ties, comparator rules and input mutation guarantees. For large `k`, ordinary sort can be simpler and faster. |
| FIFO front-removal shifts or allocation per queued item | Existing deque; ring buffer with explicit capacity policy | Preserve FIFO, wraparound, retained-reference release and overflow behavior. A bounded ring needs an agreed full-buffer policy; a custom lock-free queue adds separate correctness/reclamation obligations. |
| Repeated prefix/range searches on keys | Sorted key ranges first; trie/ART for a demonstrated prefix-heavy index | Account for key length, encoding/collation and node overhead. A research index optimized for one processor/workload is not automatically the right portable library. |
| Repeated static range sums or cumulative queries | Precomputed prefix sums; Fenwick tree when point updates must remain cheap | Precomputation uses memory and becomes stale after updates. Fenwick prefix queries and point updates are logarithmic; boundaries, overflow and inverse-operation assumptions matter. |
| Large graph traversals with pointer overhead | Compact adjacency arrays/CSR for mostly static topology; ordinary adjacency lists for frequent structural updates | Include construction and rebuild cost. CSR favors traversal/locality; individual topology changes and reverse-edge queries may need different storage. Vertex remapping must preserve external IDs. |
| Repeated merging and connectivity queries | Union-find with the appropriate balancing/compression variant | Fits incremental connectivity, not arbitrary edge deletion, path retrieval or rollback. Do not attach a path-compression bound to an implementation that omits it. |
| Huge membership/count summaries where approximation is allowed | Bloom prefilter before exact lookup; Count-Min sketch for approximate frequencies | A positive Bloom result requires exact confirmation when correctness is exact. Define error, update/delete/expiry and merge semantics; sketches cannot silently replace billing, authorization or exact deduplication. |
| Repeated whole-record loads when only a few fields are used | Compact contiguous representation, hot/cold field split, SoA or blocked layout; batched library primitives | Verify access pattern, bytes moved, SIMD/coalescing and conversion cost. Whole-record access can favor AoS. Layout changes must preserve ABI, serialization and ownership where those are contracts. |

Relevant foundations and implementation contracts:

- [Abseil containers](https://abseil.io/docs/cpp/guides/container), [Swiss table design](https://abseil.io/about/design/swisstables),
  and [B-tree tradeoffs](https://abseil.io/about/design/btree): locality and storage choices have observable API consequences.
- [Briggs and Torczon, sparse sets (1993)](https://www.dcs.gla.ac.uk/~pat/ads2/papers/sparseSets.pdf)
  and [Roaring, version 2 (2016)](https://arxiv.org/html/1603.06549v2): different set workloads need different representations.
- [MIT binary heaps](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/40d4851e550507ca14dc778b9b2266cc_MIT6_006S20_lec8.pdf),
  [Fenwick's cumulative-frequency paper](https://doi.org/10.1002/SPE.4380240306),
  [Boost CSR contracts](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/graph_classes/compressed_sparse_row.html),
  and [Princeton union-find](https://algs4.cs.princeton.edu/15uf/): choose the required operation set before a specialized structure.
- [ART (2013)](https://db.in.tum.de/~leis/papers/ART.pdf) and [HOT (2018)](https://dbis.uibk.ac.at/sites/default/files/2018-04/hot-height-optimized-author-version.pdf)
  are deeper index-design leads. Read methods, key distributions, hardware and update/synchronization costs before proposing one.
- [Bloom filtering notes](https://courses.grainger.illinois.edu/cs473/sp2017/notes/06-bloom.pdf)
  and [Cormode/Muthukrishnan on Count-Min](https://www.cs.ox.ac.uk/people/graham.cormode/pubs/papers/cmsoft.pdf)
  explain probabilistic answers and their assumptions; approximation is a product decision.

## Reduce work before adding machinery

Search only the relevant path: repeated scans inside loops, repeated sorting/key extraction,
duplicate subproblems, needless materialization and data-layout conversions. Read callers and
profile evidence; search matches are leads. A grouped/indexed pass or reuse of a stable
intermediate can beat a sophisticated new container. Three linear passes remain `O(n)`;
fewer passes are a constant-factor/allocation hypothesis, not an asymptotic improvement.

For a problem needing more than a container swap, identify its classical form: matching,
shortest path, connectivity, interval queries, dynamic programming or streaming. Verify the
algorithm's prerequisites. For example, a greedy choice needs a correctness argument, and
reusing subproblem results needs valid state keys and bounded lifetime. Do not invent a
novel algorithm or force an approximation solely to promise sublinear work.

Memory transfers can dominate instruction counts. [Demaine's cache-oblivious survey](https://www.cs.cmu.edu/afs/cs/project/pscico-guyb/realworld/www/slidesS18/Demaine02.pdf)
distinguishes CPU work from block transfers and states ideal-cache assumptions. Use it to
reason about contiguous scans, blocking and reuse; it does not predict a specific modern
CPU's timing. [Blelloch's scan chapter](https://www.cs.cmu.edu/afs/cs/academic/class/15451-s14/www/LectureNotes/PrefixSumBlelloch.pdf)
explains parallel prefix operations under associative operators. Reassociation can change
floating-point results; a faster parallel reduction must satisfy the actual numeric contract.

## Propose and verify a small shortlist

For each promising idea report: location and workload, current work/cost, candidate,
expected mechanism, semantic constraints, added memory/maintenance cost and the smallest
experiment that could reject it. Mark an unmeasured proposal as a hypothesis; do not give
an invented speedup. A useful outcome can be keeping the current representation.

Measure the complete operation as well as a focused microbenchmark. Include tiny/typical/large
inputs and the distributions that can change the decision: duplicates, misses, skew, churn,
long keys, resizing, sparse/dense IDs or full queues. Choose only applicable cases. Separate
build from lookup when both matter, then account for their actual frequency. Prevent dead-code
elimination; keep inputs, allocator, optimization, warmup and concurrency comparable. Use
runtime/OS tools from the owning performance skill for allocations, retained bytes, CPU,
cache/memory stalls and relevant tail latency. Hardware counters diagnose mechanisms; they
do not replace end-to-end measurements.

Verify against the old behavior or a simple independent oracle. Select meaningful invariants
such as ordered output with duplicate keys, comparator boundaries, queue wraparound or
random update/query sequences; reuse existing tests before adding new ones. A checksum of
one fixture is not a proof over all inputs. Preserve validation and collision defenses.
Keep the candidate only when its representative benefit outweighs its complexity and costs;
record limits and remove task-only benchmarks/captures using the main skill's cleanup rules.
