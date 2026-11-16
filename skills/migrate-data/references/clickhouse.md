# ClickHouse migrations

Establish engine, database engine, server version, partitions, replicas/shards, materialized
views and the authoritative source of records. An analytical copy and a system of record
have different reconciliation and recovery requirements. Do not assume PostgreSQL transaction
or uniqueness semantics because the interface is SQL.

Classify the actual operation: metadata-only change, background mutation, new-table copy,
partition operation or distributed DDL. Verify completion on the required nodes. An accepted
DDL request, completed local mutation and fully converged replicas are distinct outcomes.
Use the applicable system mutation, replica and distributed-DDL status, with bounded waits.

- `ALTER ... UPDATE` is normally asynchronous and can rewrite affected parts; key-column
  changes have restrictions. Newer lightweight update/delete mechanisms differ by version and
  engine. Check current support and eventual physical cleanup rather than treating all updates
  as equivalent or replacing the table engine automatically.
- `MODIFY ORDER BY` supports restricted metadata changes, not an arbitrary resort of existing
  data. For an incompatible ordering/layout change, create the intended table and perform a
  bounded explicit-column copy, with a defined capture/catch-up boundary for concurrent writes.
- Preserve numeric/time precision, nullable meaning, TTL/deletion rules, codecs and required
  deduplication semantics. `ReplacingMergeTree` background merges do not enforce immediate
  uniqueness; ordinary reads, `FINAL` and version-aware aggregation can return different results.
- Inserts have guarantees scoped to engine, blocks, partitions, shards and acknowledgement
  settings. Do not wrap a multi-step copy in a presumed portable `BEGIN/ROLLBACK`. Reconcile
  an uncertain insert before retrying; existing deduplication only helps within its actual scope.

For a table swap, check dependencies and target engine support for the chosen operation.
Reconcile keys, versions, counts and business aggregates against one coherent watermark.
Define how writes during validation reach the final table and how recovery avoids losing them.
Keep the source until the owning cutover and retention conditions are met.

Avoid forcing `OPTIMIZE TABLE ... FINAL` as a migration completion check. It can cause heavy
rewrites; it is separate from the query-time `FINAL` semantics needed by some table engines.

Primary references: [transaction guarantees](https://clickhouse.com/docs/guides/developer/transactional),
[mutations](https://clickhouse.com/docs/sql-reference/statements/alter/update),
[ordering-key restrictions](https://clickhouse.com/docs/sql-reference/statements/alter/order-by),
[OPTIMIZE FINAL](https://clickhouse.com/docs/best-practices/avoid-optimize-final).
