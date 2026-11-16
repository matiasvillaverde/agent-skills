---
name: migrate-data
description: Plan, implement, and verify data or schema migrations while preserving records, compatibility, and recovery. Use for backfills, schema changes, store upgrades, or data transfers; reuse the project's migration mechanism.
---

# Migrate data

Start with the required change, selected product/environment, source and destination,
engine/runtime versions, and existing migration owner. Inspect actual schema, deployed
migration history, reader/writer versions, data volume and relevant constraints. Distinguish
preparing a migration from applying it; proceed with actions already authorized for that target.

Choose the smallest migration that satisfies the change. A direct supported alteration can
be enough for a local store or compatible additive field. Use staged expand/backfill/cutover/
retire only when mixed versions, availability or data conversion require it. Reuse the
existing runner, ledger and deployment sequence; do not add a migration framework by default.

## Preserve meaning and recovery

Specify what must survive: identifiers, relationships, duplicates, NULL versus defaults,
ordering, precision, time zones, permissions, deletion behavior and concurrent writes.
Make lossy conversions and conflict resolution explicit. Counts alone cannot establish that
the right records or values survived; check identities, relationships and representative values.

Keep shipped migrations immutable. Add a corrective migration. Let the existing ledger
prevent reapplication; an `IF NOT EXISTS` check alone can hide a mismatched definition or
an unfinished backfill. On interruption, inspect committed steps and target state before
resuming. Never blindly repeat a migration whose outcome is unknown.

Define recovery for the actual failure boundary: transaction rollback, compatible application
rollback, forward repair or restore. A reverse DDL script cannot recover dropped values or
new writes. Before an irreversible cutover, verify the existing recovery checkpoint and its
restore procedure, including changes since that checkpoint. Retain source/recovery data until
the owning retention and cutover criteria permit retirement; don't create permanent duplicate stores.

## Execute the engine's contract

Read only the relevant reference:

- [PostgreSQL](references/postgresql.md): lock acquisition, rewrites, concurrent indexes and backfills.
- [ClickHouse](references/clickhouse.md): parts, asynchronous mutations, replicated/distributed scope and cutover.
- [SQLite and SwiftData](references/sqlite-swiftdata.md): embedded-store upgrades and model-owned migrations.

Inspect generated SQL and transaction boundaries, including ORM behavior. Bound lock waits,
execution, batch size and disk growth to the selected workload. For resumable backfills, use
a stable cursor and durable checkpoint; guard against overwriting newer writes and reconcile
inserts/updates/deletes during copying. A final catch-up or paused writer boundary must be
defined where concurrent changes can otherwise escape the copy. Do not quietly weaken
constraints, isolation, durability or acknowledgements to make the migration pass.

## Verify through the real path

Use original fixtures or an authorized protected copy with the actual migrator. Exercise a
fresh install and supported upgrade paths, including skipped versions when relevant. Check
meaningful edge records, constraints and application reads/writes after reopening the store.
For staged work, rehearse interruption/resume at committed boundaries and compatibility while
old and new clients overlap. Use the engine's integrity checks as supporting evidence.

Apply within the selected target and authorization after preparation and rehearsal. Stop on
unexpected schema/data drift, failed invariants, exceeded budgets or an ambiguous outcome;
reconcile before continuing. Ask only when missing target authority or an unapproved
irreversible consequence actually blocks the next step.

Report the implemented sequence, verification, recovery boundary and any remaining cutover
or retirement work. Keep sensitive records and raw diagnostics private. Stop task-owned
helpers and remove disposable fixtures after saving compact evidence and reproduction steps.

Research and source limitations: [sources](references/sources.md).
