---
name: perf-clickhouse
description: Diagnose and improve ClickHouse query and ingestion performance using query logs, ProfileEvents, sparse-index pruning, sorting keys, parts, merges and scoped resource measurements.
---

# ClickHouse performance

Identify the slow query or ingestion operation, selected server/environment, version,
table engines and topology. Inspect schema, ordering/primary/partition keys, parts,
projections and workload skew. Define the required result/freshness/acknowledgement contract
and a bounded representative experiment. Local mode does not qualify replicas or shards.

Read [ClickHouse profiling](references/profiling.md) for query-log interpretation, EXPLAIN,
pruning, ingestion, caches and local fixtures. Separate initial queries from distributed
work and successful completions from failures. Inspect actual ProfileEvents/counter coverage;
zero counters may mean unavailable measurement. Selected rows/bytes are not physical disk I/O.

Follow observed work: excessive read granules/columns, joins, memory pressure, part creation,
merge backlog, queueing or remote waits. Test query shape and data layout against actual
selectivity before adding skip indexes, projections or precomputation. Bound execution,
query memory, temporary disk and concurrency; query limits are not a process RSS guarantee.

Preserve multiplicity, NULL/default behavior, ordering, precision, freshness and durability.
`ANY` joins, approximate aggregates, removing `FINAL` or changing async-insert acknowledgement
can change the product contract. A sparse primary index is not a uniqueness constraint.
Schema/layout changes need the owning migration process and target authorization.

Compare like data, settings and cache states; separate cold/first-use from warm measurements.
Use repeated trials and equivalent results, recording latency, reads, memory and ingestion/
storage/merge costs relevant to the change. Separate diagnostic overrides from the intended
runtime configuration. Do not clear live caches, routinely force merges or start production
load to create a favorable benchmark.

For local experiments, explicitly isolate configuration, data and temporary paths so the
CLI cannot load or change an existing store. Check installed help, enforce an outer timeout
and verify result equality. Treat timeouts and rejected work as outcomes, not fast successes.

Report evidence, the retained change, workload limits and remaining distributed/production
gaps. Run focused regressions and required gates. Save compact reproduction/results, stop
owned processes/load, restore temporary settings and remove owned traces, databases and
caches after analysis. Preserve shared data and necessary unresolved failure evidence.
