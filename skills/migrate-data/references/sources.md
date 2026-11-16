# Sources and scope

Original synthesis, reviewed 2026-11-15. No upstream implementation, scripts or examples
were imported. The primary engine sources are linked beside their guidance; consult the
target version before applying a procedure.

Community workflows reviewed:

- [db-migration-safe](https://github.com/alexbobkovv/db-migration-safe/blob/63b55b35bb34141b63e54343b24743c9b1249f83/SKILL.md),
  Apache-2.0. Useful lock/transaction distinctions; no linter installation, generated inverse
  rollback, fixed timeout or mandatory online rewrite is inherited.
- [Axiom database migration](https://github.com/charleswiltgen/axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/.claude-plugin/plugins/axiom/skills/axiom-data/skills/database-migration.md),
  MIT. Useful actual-migrator upgrade tests and copy-first rebuild order. Blanket additive-only
  or existence-check rules are replaced with compatibility, data validation and ledger semantics.
- [SwiftData agent skill](https://github.com/vanab/SwiftData-agent-skill/blob/4819a5381fa5fdce894451822917b1135c19e050/swiftdata-expert-skill/SKILL.md),
  MIT. Useful container, migration and context boundaries. Deployment target and collision
  policy remain application-specific.

These sources informed decisions; their popularity and example tests do not qualify a real
migration. A passing rehearsal establishes only its tested engine, fixtures and failure paths.
