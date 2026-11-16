# SQLite and SwiftData upgrades

## SQLite

Use the SQLite version bundled with the deployed application, not merely the developer CLI.
Inspect the existing migrator's transaction and foreign-key behavior before adding wrappers.
Reopen an on-disk fixture to verify persistence; an in-memory test cannot establish file/WAL
recovery or runtime-version compatibility.

Prefer a supported `ALTER TABLE` when it preserves the intended meaning. SQLite supports
column removal with restrictions, and newer versions add further operations; don't rely on
old claims that every constraint or column change requires a rebuild. If a rebuild is needed,
follow the documented create-new, copy, drop-old, rename-new sequence inside the appropriate
transaction. Preserve columns, row identifiers, indexes, triggers, views and relationships.
Copying through an inner join or `INSERT OR IGNORE` can silently discard records.

Foreign-key enforcement is connection-scoped; changing `PRAGMA foreign_keys` inside a
transaction is a no-op. Use the runner's supported procedure or the documented rebuild
sequence. Inspect `foreign_key_check` results before commit and abort on violations. After
commit, restore and verify the original enforcement setting outside any transaction; do
the same after rollback. Do not attempt to re-enable it only before commit.
`integrity_check` does not replace relationship/value checks. SQL errors or returned violation
rows must cause the runner to abort; issuing a diagnostic PRAGMA alone does not enforce this.
Avoid editing `sqlite_schema` or disabling error checks as a routine migration shortcut.

For an active store, use a consistent backup mechanism such as the online backup API.
Copying just the main file of a live WAL database can omit committed changes. Preserve the
application's journal/synchronous policy; changing it is a durability decision, not migration
housekeeping. Budget temporary space for both old/new tables and journal/WAL growth.

Sources: [ALTER TABLE and rebuild sequence](https://www.sqlite.org/lang_altertable.html),
[foreign-key controls](https://www.sqlite.org/pragma.html#pragma_foreign_keys),
[backup API](https://www.sqlite.org/backup.html), [WAL](https://www.sqlite.org/wal.html).

## SwiftData

Keep schema evolution at the SwiftData API boundary; do not change its underlying SQLite
tables directly. Inspect model/container configuration, deployment targets, store URL, app
extensions and CloudKit use. Preserve released schemas in `VersionedSchema` definitions and
connect the ordered `SchemaMigrationPlan` to the actual `ModelContainer`.

Choose lightweight migration for supported changes and custom stages for data transformations.
Check which schema/context is available before and after each stage. For example, resolve
duplicate identities under an explicit merge policy before adding uniqueness; adding a unique
attribute is not permission to overwrite conflicting user records. Preserve renamed properties
through the supported mapping, rather than accidentally treating them as new empty fields.

Test supported old-store versions, skipped upgrades and reopening through the production
container path on supported OS versions. Verify relationships, external storage, identity and
sync compatibility where used. A container-open failure is not permission to delete the store
or fall back to an empty one. Keep recovery copies coherent with all store-managed files.

Sources: Apple's [schema/migration walkthrough](https://developer.apple.com/videos/play/wwdc2023/10195/)
and [SwiftData updates](https://developer.apple.com/videos/play/wwdc2024/10137/).
