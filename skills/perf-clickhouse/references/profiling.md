# ClickHouse performance

Inspect engine/version, `SHOW CREATE TABLE`, ordering/primary/partition keys, parts,
projections, skip indexes and relevant settings. Server and `clickhouse-local` evidence have
different coverage; a local fixture does not measure distributed execution or replicas.

For a server, use a bounded time window in existing `system.query_log`. Separate successful
`QueryFinish` entries from exceptions and initial client queries from shard work; don't sum
both as independent requests. Compare duration, rows/bytes read, result size, memory and
relevant `ProfileEvents`. Group normalized query shapes for discovery, then check parameters,
skew and multiple representative runs. Log flushing/sampling and unavailable nodes limit coverage.

Use `EXPLAIN` to inspect pruning and the pipeline, then actual resource measurements to test
the hypothesis. For supported versions, inspect `EXPLAIN indexes = 1 SELECT ...`; current docs
require `use_query_condition_cache=0, use_skip_indexes_on_data_read=0` for useful index output
from 25.9 onward. Record these diagnostic overrides and restore/omit them for the intended
runtime comparison. Verify observed parts/granules/rows rather than assuming an index helped.
Validate the counter source: the tested 26.3 `clickhouse-local` returned zero JSON read
counters despite reading data. Separate CLI ProfileEvents diagnostics exposed `SelectedRows`,
`SelectedBytes` and `SelectedMarks`; their costs are not cold physical-device I/O.

- Align ordering with frequent selective filters and compression opportunities; the sparse
  primary index is not a unique constraint. Low-cardinality-first is a candidate to test,
  not a rule that outranks query patterns. Partitioning has lifecycle and pruning tradeoffs.
- Skip indexes help when data distribution lets them exclude granules. Test selectivity and
  read reduction; adding an index to every filter column can add maintenance without benefit.
- Reduce unnecessary columns and early data volume when semantics permit. Compare join
  algorithms under actual key multiplicity and memory pressure. `ANY` joins, default-value
  null handling, approximate aggregates and removing `FINAL` can change the result.
- Measure part creation, merge backlog and latency when changing insert batches or async
  inserts. Batch size and `wait_for_async_insert` affect acknowledgement/failure behavior;
  do not adopt a universal row count or fire-and-forget setting to improve a chart.
- Materialized views/projections precompute work and cost storage/ingestion/backfill effort.
  Verify freshness and update/delete propagation for the chosen design before adopting them.

Distinguish result cache, query-condition cache, mark/uncompressed/filesystem caches and OS
cache. Query-result caching can allow stale answers. Compare equivalent cache policy and
data freshness; don't clear a live server's caches to simulate cold work. Avoid using
`OPTIMIZE TABLE ... FINAL` as routine tuning; query-time `FINAL` is a separate operation.

For an isolated local fixture, inspect `clickhouse local --help` and use explicit owned
`--path`, configuration and temporary storage. Defaults can persist data or load existing
configuration. Bound threads, query memory, execution and temporary disk, with an external
timeout; query memory accounting is not total process RSS. `max_threads` limits query work,
not every background pool. Check logging against actual output so verbose diagnostics do not
contaminate timing trials. Generate deterministic local data, avoid remote table functions,
capture results as well as timings, and remove owned files.

Sources: [diagnosis](https://clickhouse.com/docs/guides/clickhouse/performance-and-monitoring/diagnose-slow-queries),
[EXPLAIN](https://clickhouse.com/docs/sql-reference/statements/explain),
[primary keys](https://clickhouse.com/docs/best-practices/choosing-a-primary-key),
[query cache](https://clickhouse.com/docs/operations/query-cache),
[OPTIMIZE FINAL](https://clickhouse.com/docs/best-practices/avoid-optimize-final),
[local CLI](https://clickhouse.com/docs/concepts/features/tools-and-utilities/clickhouse-local).


Research basis: original synthesis reviewed 2026-11-15, with no imported upstream code.
[ClickHouse best practices](https://github.com/ClickHouse/agent-skills/blob/d3b2b5ba43a8b80c2d08858b68d53edc701b5ace/skills/clickhouse-best-practices/SKILL.md)
(Apache-2.0) informed layout/pruning/ingestion topics. Mandatory whole-catalog reviews, fixed
batch/cardinality thresholds, semantic substitutions and the overbroad claim that every
ordering-key modification is impossible were excluded. Match docs to the deployed version;
local mechanism tests do not establish distributed or production capacity.
