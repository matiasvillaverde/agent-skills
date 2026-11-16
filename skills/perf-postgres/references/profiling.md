# PostgreSQL performance

Discover server version and existing instrumentation first. If `pg_stat_statements` is
available, compare bounded interval snapshots by database/user/query ID, including call
counts, total and mean execution, rows and block/temp/WAL metrics relevant to the complaint.
Check resets and entry eviction. Aggregated means are not percentiles; normalized query text
can hide parameter skew. Don't reset shared statistics or restart a server to enable an
extension merely for an investigation. Use available request traces/query logs when needed.

Begin with plan-only `EXPLAIN`. When actual execution is authorized and bounded, an example
shape for a known safe read is:

```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS, TIMING OFF, FORMAT JSON)
SELECT ...;
```

Verify options on the target major version. Compare estimated versus actual rows, loops,
filtering, buffers, spills, partition pruning and parallel work. Node times/rows are averaged
per loop where applicable; parent metrics include children, so summing nodes can double-count.
A shared-buffer read may be served by the OS cache. Capture client time separately: even
serialization-aware EXPLAIN does not measure network delivery.

Follow the observed cause:

- **Wrong cardinality:** inspect statistics freshness, distribution and correlated columns;
  targeted `ANALYZE` or extended statistics may help. Refreshing stats can change plans and
  consumes resources. Compare representative parameters and prepared generic/custom plans.
- **Too much read work:** test predicate/index alignment, index type, key order, partial
  conditions and covering columns. Sequential scans can be right for broad access. Additional
  indexes add write/storage costs; an index-only plan still depends on visibility conditions.
- **Sort/hash spills:** reduce unnecessary rows/width first. Evaluate scoped memory changes
  under expected concurrency; `work_mem` applies to multiple operators/workers, not one shared
  per-server allowance. A spill alone does not justify raising global memory.
- **Waiting:** correlate request timing with `pg_stat_activity`, wait events and blockers.
  Pool saturation, long transactions and lock waits are not fixed by a query index alone.
  Preserve transaction semantics; don't terminate unrelated sessions as a profiling shortcut.

Check RLS/role, search path, bind types, collation and client preparation when reproducing.
Optimizer disabling/forcing can test a hypothesis in a scoped experiment; it is not proof
that the forced plan is a robust production fix. Schema changes need the normal migration path.

Primary references: [EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html),
[plan interpretation](https://www.postgresql.org/docs/18/using-explain.html),
[pg_stat_statements](https://www.postgresql.org/docs/18/pgstatstatements.html),
[statistics](https://www.postgresql.org/docs/18/planner-stats.html),
[resource settings](https://www.postgresql.org/docs/18/runtime-config-resource.html),
[locking](https://www.postgresql.org/docs/18/explicit-locking.html).


Research basis: original synthesis reviewed 2026-11-15, with no copied upstream code.
[Supabase PostgreSQL guidance](https://github.com/supabase/agent-skills/blob/c9be0e931b7930f7d02126d04774d904c381e7d7/skills/supabase-postgres-best-practices/SKILL.md)
(MIT) informed plan/query-family/locking topics. Scan and spill examples remain hypotheses;
shared statistics resets and extension installation are not defaults. Match primary docs
to the server version. Research and a local fixture do not establish production capacity.
