# SQLite performance

Inspect the application's SQLite library version, compile options, driver, connection count,
journal/synchronous settings, database size and query bindings. The system CLI can differ
from the library shipped in an app. Copy active databases with a coherent backup mechanism;
do not detach a WAL database from its committed WAL state.

Start with `EXPLAIN QUERY PLAN` for the actual SQL and parameter types. Inspect scan versus
selective search, covering indexes, join order and temporary B-trees. This is a diagnostic
format, not a stable application API; don't build brittle exact-plan-text tests.

Use installed CLI capabilities (`.help timer`, `.help stats`, `.help scanstats`) before
constructing measurements. `.timer` reports execution time; `.stats`/scan-status can expose
VM steps, full scans and sort work. Instrumentation adds overhead and compile support varies.
Prevent unneeded startup customization with the installed CLI's supported initialization
control. Capture output equality and deterministic ordering, not only timer lines.

- Test indexes against predicates, equality/range ordering, requested ordering and collation.
  A covering index can remove table lookups but enlarges writes/storage. Broad scans may
  still be appropriate; don't force index use to make the plan look better.
- Compare statement reuse and transaction batching when prepare or per-commit cost dominates.
  Batching changes lock hold time, visibility and failure scope; choose a size that preserves
  the operation's contract. Busy timeouts bound waiting but don't remove writer contention.
- In WAL mode readers and a writer can overlap, but there is still one writer at a time.
  Long reader snapshots can delay checkpoint progress. Measure WAL/checkpoint behavior,
  commit latency and locks under the actual access pattern, not only single-thread SELECTs.
- `synchronous`, journal mode and checkpoint policy affect durability/latency. Do not lower
  them or disable foreign keys for a purported equivalent speedup. Checkpointing is work and
  may move latency elsewhere rather than remove it.
- Planner statistics can change plans. On supported versions, `PRAGMA optimize` provides
  selective statistics maintenance; it is not a read-only inspection. Record when statistics
  change and don't compare a stale baseline to a freshly analyzed candidate without saying so.

Define cache state honestly. A new connection, new CLI process or fresh database copy does
not clear filesystem caches. Test on-disk persistence and representative rows/skew; a tiny
memory-store result does not establish disk, contention or durability performance.

Sources: [query plans](https://www.sqlite.org/eqp.html),
[CLI diagnostics](https://www.sqlite.org/cli.html),
[statistics maintenance](https://www.sqlite.org/lang_analyze.html),
[WAL](https://www.sqlite.org/wal.html), [backup API](https://www.sqlite.org/backup.html).


Research basis: original synthesis of the primary references above, reviewed 2026-11-15.
No upstream code/examples imported. Bounded on-disk fixtures exercised plans, indexes,
result equality and write/storage tradeoffs; they do not rank database engines or establish
production/device capacity. Match documentation to the application's SQLite library.
