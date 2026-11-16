---
name: perf-sqlite
description: Diagnose and improve SQLite query, transaction and embedded-store performance using query plans, statement work, indexes, WAL/checkpoints and contention measurements. For SwiftData-owned stores, use its public API performance workflow.
---

# SQLite performance

Identify the application operation and its actual SQLite library/driver, compile options,
connections, store size and journal/synchronous policy. A system CLI may differ from the
shipped library. Use an owned on-disk fixture or authorized target and a bounded workload;
copy active stores coherently, including committed WAL state through a supported backup.

Read [SQLite profiling](references/profiling.md) for query plans, CLI diagnostics, indexes,
statement reuse, transaction costs, contention and checkpoint behavior. Trace application
calls first: repeated prepares/queries or per-row commits can dominate the SQL itself.
For a SwiftData-managed store, select `perf-swiftdata` when available and operate through
SwiftData APIs; do not tune its backing database as an independently owned SQLite store.

Inspect actual SQL, bind types, parameter skew and ordering with `EXPLAIN QUERY PLAN`.
Use supported statement/CLI counters to test a hypothesis. Plans are diagnostic output,
not a stable exact-text test API. Time the relevant operation independently of diagnostic
overhead and check returned data, not only elapsed-time lines.

Try the smallest evidence-backed query/index/batching change. Preserve row identity,
multiplicity, NULLs, collation, ordering, relationships, visibility and failure semantics.
Indexes add write/storage costs; batching changes lock duration and transaction scope.
WAL still has one writer at a time. Do not lower durability or disable foreign-key checks
for a supposedly equivalent speedup. Schema changes use the existing migrator.

Compare equivalent data/cache/statistics/concurrency states with repeated measurements and
independent result checks. A fresh connection or process does not mean cold filesystem
caches. Include relevant busy/lock waits, commit latency, WAL growth and checkpoint work;
an in-memory SELECT cannot establish persistent-store or multi-connection behavior.
Verify reopening after changes that affect persistence.

Report baseline/candidate distributions, sample count, storage/write tradeoffs, errors and
limits. Keep only meaningful improvements that preserve behavior; run focused regressions
and required gates. Save compact results/reproduction, close owned connections and remove
owned database/WAL/SHM fixtures, traces and task-only caches after analysis. Preserve shared
stores/caches and necessary unresolved evidence; perform cleanup on failure too.
