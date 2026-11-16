# Categories and what an inconsistency means

Choose categories that affect the requested work. This is a comparison aid, not a requirement
to produce a score, new standard or finding for every row.

| Category | Compare within the same owner and role | Important exceptions or consequences |
| --- | --- | --- |
| Files and directories | Casing, suffixes, source/test/fixture placement, singular/plural terms, discoverability | Framework-reserved names, platform suffixes, generated files, public asset/import paths and case-sensitive deployment |
| Packages and modules | Namespace vocabulary, import direction, public entrypoints, private implementation locations | A folder is not automatically a package; visibility and module boundaries may be semantic |
| Types and symbols | Classes, structs, enums, protocols/traits/interfaces, variants, functions, fields and constants | Language-specific casing, foreign APIs, overrides, generated bindings and supported public names |
| Domain vocabulary | Same concept's name across UI, service, storage and tests; distinct concepts with similar names | A user, member and account may be different entities; establish meaning before standardizing |
| Operation contracts | Names expressing effect, conversion/ownership, asynchronous behavior, optionality, units and collection meaning | `get` may be local while `fetch` performs I/O; a duration type can already express units; mathematical notation can be clearer |
| API and data boundaries | Routes, flags, config keys, JSON fields, database columns, event names, versioning | External contracts are not cosmetic style. Source and wire names may intentionally differ |
| Errors and observability | Error vocabulary/codes, propagation/handling ownership, logging fields and severity, metric units | Different recovery needs may justify different error types. Audit-event identifiers and dashboard queries can be consumers |
| Tests and fixtures | Test discovery, behavior-oriented names, setup/fixture ownership, scenario terminology | Runner conventions, regression IDs and compatibility fixtures may intentionally differ from production code |
| Docs and agent instructions | Canonical owner, references, terminology, comments, nested instruction scope | Public docs, historical evidence and generated references have different lifecycles; do not rewrite history as current state |

An evidence note can be one sentence: **rule and scope → source → example → deviation → consequence**.
For example, an established `duration_ms` event field and a new seconds-valued `duration_ms`
field indicate a contract mismatch, not merely naming inconsistency. Conversely, `Duration`
values named `timeout` need not gain a redundant unit suffix.

Prioritize misleading semantics and broken discovery/contracts, then repeated local drift that
slows maintenance. A missing global file-casing rule in a healthy multilingual monorepo is not
itself a defect. Keep a new recommendation visibly separate from an established requirement.
If two legitimate styles coexist during migration, report the boundary and actual confusion;
do not choose a winner by majority or demand a repository-wide rename.
