---
name: perf-swiftdata
description: Diagnose and improve SwiftData fetch, relationship, model-context, save and persistence performance in Apple apps. Use for excessive fetches/faults, main-actor work, retained models, imports or slow saves while preserving app behavior.
---

# SwiftData performance

Start with the user journey and actual `ModelContainer`: schema, store type/URL,
deployment targets, OS/SDK, context ownership, autosave/undo, extensions and CloudKit.
Define a bounded representative workload and preserve visible UI, product behavior,
pending edits, persistence and synchronization semantics. An in-memory preview is not
evidence about the shipped persistent store or physical device.

Read [SwiftData profiling](references/profiling.md) for fetch descriptors, query/index
availability, relationship materialization, context isolation and saves. Verify APIs in
the target SDK and documentation before changing them. Use public SwiftData APIs for its
stores; do not apply raw SQLite indexes, PRAGMAs or schema edits to backing files.

Measure fetch, faults/relationship traversal, model materialization, UI updates and save
separately. Correlate work with one reproducible action, caller/thread and retained model
count. Use `perf-apple` when available for Instruments/Data Persistence capture and device
profiling; keep the query/model diagnosis here rather than creating another capture system.

Test the smallest cause supported by evidence: repeated fetches, unnecessarily broad
materialization, unsupported filtering, relationship access, UI-actor work or save frequency.
Bound fetches to the actual task without omitting required rows. Prefetching, indexes,
background contexts and batches each need measured benefit and correct ownership/lifecycle.
Use identifiers/values and supported isolation APIs when handing work between contexts.

Preserve pending-change visibility, ordering/pagination, uniqueness/collision behavior,
undo and termination durability. `#Unique` changes semantics; it is not just a faster index.
Delaying saves or moving work off the UI actor can hide latency or change when data survives.
Schema changes follow the app's versioned migration owner and CloudKit constraints.

Compare equivalent store contents, devices, OS/build modes and lifecycle/cache phases.
Repeat enough to expose noise; include latency, main-thread occupancy, allocations/retention
and relevant write/storage costs. Verify actual UI results, errors/cancellation and reopening
after persistence changes. Run focused regressions and required product checks without
claiming OS/device or production coverage that was not exercised.

Report the bottleneck, retained change, measurements and gaps. Save compact reproduction
and results; stop owned captures/helpers, restore temporary settings and remove task-owned
traces, scratch stores and caches after analysis. Preserve user stores, shared caches and
required unresolved evidence; verify cleanup on failure too.
