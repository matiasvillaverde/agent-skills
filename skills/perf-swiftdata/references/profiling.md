# SwiftData performance

Start from the user operation and actual `ModelContainer`: schema, store URL/type, context
ownership, autosave/undo, CloudKit and extensions. Check deployment targets and selected SDK
declarations before recommending APIs. A fast in-memory preview does not qualify a persistent
store, older OS or physical device.

Measure fetch, relationship traversal, model materialization, UI updates and save separately.
The existing `perf-apple` persistence guidance owns Instruments/Data Persistence capture;
use it when available rather than inventing a second profiler. Correlate repeated fetches,
faults and saves with one action, and check caller/thread, duration and retained model count.

- Push supported filtering/sorting to `FetchDescriptor`/`@Query` when it preserves behavior.
  Bound fetches by the actual screen/task and maintain stable ordering. A fetch limit that
  silently omits required rows is not an optimization.
- Use count or identifier fetches when those are the required outputs. Consider selected
  properties and relationship prefetching for demonstrated materialization/fault cost;
  prefetching can replace many small faults with excessive memory and work.
- Preserve `includePendingChanges` semantics. Results including unsaved edits differ from
  store-only reads. Offset pagination under concurrent changes can duplicate/omit items;
  any alternative cursor must preserve ordering and supported predicates.
- Evaluate `#Index` for measured filter/sort patterns. Verify OS availability and migration
  behavior; indexes add write/storage cost. Do not add `#Unique` as an indexing substitute:
  uniqueness/upsert behavior changes collision semantics.
- Keep `ModelContext`/model isolation correct when moving work off the UI actor. Use the
  supported actor/context APIs and identifier/value handoff; do not pass mutable persistent
  models across contexts to avoid a fetch. Background work still consumes resources and can
  contend with saves or synchronization.
- Batch imports/saves only within the required atomicity, undo and durability window. Changing
  autosave or delaying explicit `save()` changes when data survives termination. Verify
  completion errors, cancellation, reopening and observed UI state after the change.

Use public SwiftData APIs for stores it owns. Do not apply raw SQLite indexes, PRAGMAs or
schema edits to its backing files. Schema changes follow the app's versioned migration plan;
preserve CloudKit compatibility when enabled.

Primary sources: [query/index updates](https://developer.apple.com/videos/play/wwdc2024/10137/),
[schema/migration semantics](https://developer.apple.com/videos/play/wwdc2023/10195/),
[FetchDescriptor](https://developer.apple.com/documentation/swiftdata/fetchdescriptor).
The 2026-11-15 review also inspected Xcode 27.0 (27A266a) SwiftData SDK declarations for
fetch limits/offsets, pending changes, property/prefetch lists, and `#Index`/`#Unique`
availability (macOS 15 / iOS 18). Declaration availability is not behavioral qualification.


Research basis: original synthesis reviewed 2026-11-15; no upstream code imported.
[SwiftData agent skill](https://github.com/vanab/SwiftData-agent-skill/blob/4819a5381fa5fdce894451822917b1135c19e050/swiftdata-expert-skill/SKILL.md)
(MIT) informed context/fetch/deployment topics. Query limits and uniqueness remain subject
to app semantics. Source/SDK review does not qualify persistent-store behavior, CloudKit,
older OS versions or device performance; those need the actual app and workload.
