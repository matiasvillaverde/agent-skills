# PostgreSQL migrations

Check the server major version, extensions, partitioning, migration runner and active writers.
Inspect the SQL actually executed. The following guidance was checked against PostgreSQL 18;
syntax and lock behavior must match the target version.

- Ordinary `ALTER TABLE` often needs `ACCESS EXCLUSIVE`; a queued lock can affect traffic
  even when the eventual metadata change is quick. Use workload-specific lock and statement
  timeouts, inspect blockers, and retry only after reconciling the first outcome. Don't set an
  unlimited statement timeout as a generic safety measure.
- Determine whether the exact operation rewrites or scans the table. Adding a column with a
  nonvolatile default can avoid a rewrite on supported versions; nullable-first plus a
  backfill is useful when meaning or compatibility requires it, not compulsory for every field.
- `NOT VALID` and later `VALIDATE CONSTRAINT` can separate adding an eligible constraint
  from scanning existing rows. Eligibility and locks depend on constraint type and version;
  don't attach these clauses indiscriminately to UNIQUE or older NOT NULL syntax. Inspect
  existing invalid data before validation and verify the constraint is validated afterward.
- `CREATE INDEX CONCURRENTLY` permits writes but still consumes resources and waits for
  transactions. It cannot run inside a transaction block. A failed build may leave an invalid
  index, including one that still enforces uniqueness: inspect it before repairing or retrying.
  Partitioned parents need their supported per-partition/attachment procedure. Ordinary index
  creation may be simpler for a disposable or offline table.
- Backfill deterministic batches in short transactions when a full transaction exceeds the
  workload budget. A cursor alone does not protect newer application values: define a guarded
  update or write-coordination rule, progress checkpoints, and final reconciliation. Monitor
  WAL growth, replica lag, locks and vacuum pressure as well as rows completed.

For mixed-version releases, establish old/new read and write compatibility before switching.
Retire old fields only after remaining writers, jobs and supported rollbacks no longer need
them. Verify keys, foreign keys, nullability, uniqueness, defaults, triggers, generated values,
row-level security and privileges that the migration touches.

`EXPLAIN ANALYZE` executes its statement. A surrounding rollback does not undo sequence
advancement or external effects from functions. Rehearse modifying statements in a disposable
database or with explicitly approved effects; a plan-only `EXPLAIN` is a different observation.

Primary references: [ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html),
[locking](https://www.postgresql.org/docs/18/explicit-locking.html),
[CREATE INDEX](https://www.postgresql.org/docs/18/sql-createindex.html),
[EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html),
[sequence rollback semantics](https://www.postgresql.org/docs/18/functions-sequence.html).
