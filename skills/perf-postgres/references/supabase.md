# Supabase PostgreSQL performance

Use this branch for hosted or self-hosted Supabase. PostgreSQL plan, correctness and
measurement rules still apply. Read the deployed major version and extensions; the
provider's current documentation does not establish the project's version.

## Inspect through the CLI

First read `supabase --version`, `supabase inspect db --help` and the selected
subcommand's `--help`. Verified locally with CLI **3.1.0 on 2026-11-15**: inspection
defaults to the local database; `--remote` selects the linked project, and
`--remote=<ref|branch|url>` selects another target. Some official reference pages still
show older `--linked`/`--db-url` flags. Follow installed help; do not mix generations.

Confirm project, environment, branch, region and primary/replica before a remote read.
Use a non-secret project/branch reference and existing authorized credentials; do not
put a password-bearing URL in command history or output. A profiling request does not
authorize relinking the checkout, creating credentials, granting broader access or
unblocking network bans. Inspect permission requirements and use an already permitted
read-only path if the CLI cannot operate within the selected scope.
CLI 3.1.0 help lists `database_write` among potentially required token scopes:
an inspection command does not prove that its credential is read-only.

Choose a few relevant commands, then follow the evidence:

| Question | `supabase inspect db` subcommand | Interpretation |
| --- | --- | --- |
| Which query families consume aggregate execution time? | `outliers` | Cumulative elapsed time and I/O attribution, not per-query CPU samples. |
| Is request volume causing repeated work? | `calls` | Correlate call-count deltas with workload volume and application traces. |
| What is running or waiting now? | `long-running-queries`, `blocking`, `locks` | A snapshot can miss short spikes; preserve wait reasons and timestamps. |
| Are indexes aligned with actual reads and writes? | `index-stats`, `table-stats` | Low use alone does not justify dropping a constraint, replica-used or seasonal index. |
| Is maintenance or storage contributing? | `vacuum-stats`, `bloat`, `db-stats` | Check dead tuples, maintenance, cache and WAL context; an estimate is not a repair order. |
| Are connections or replication creating pressure? | `role-stats`, `replication-slots` | Separate pool clients from server backends; never drop a slot from inspection alone. |
| Which tables contribute block I/O activity? | `traffic-profile` | Its read/write mix describes block operations, not API request proportions. |

For an already selected hosted project, CLI 3.1.0 command shapes are:

```sh
supabase inspect db outliers --remote=PROJECT_REF
supabase inspect db calls --remote=PROJECT_REF
supabase inspect db blocking --remote=PROJECT_REF
```

Replace the reference with the verified target. Keep bounded, timestamped output
privately and redact query literals, identifiers or tenant data as needed. Compare
counter snapshots only across the same statistics-reset interval. Missing permission,
unsupported command or disabled `pg_stat_statements` is a measurement gap, not zero
work. Do not reset shared statistics or enable extensions just to get a cleaner report.

## Understand CPU and service latency

The inspected CLI has **no `inspect db cpu` subcommand**. Get host CPU series from
Supabase Reports or the existing Metrics API collector in Datadog, Grafana or another
backend. Select the same instance and time window as query observations. Distinguish
user/system CPU, I/O wait, storage limits, memory pressure, connections and background
maintenance. High elapsed query time can be a wait; aggregate query times can overlap.

For hosted projects the Prometheus-compatible Metrics API can feed the team's existing
collector. Verify current series names, units, labels and availability before writing
queries or alerts. Prefer existing ingestion; a dedicated key can still be highly
privileged. Use the secret manager and collector's supported credential mechanism,
never print keys or use documentation examples that reveal them in arguments. The
hosted Metrics API is not available for self-hosted deployments; use their existing
PostgreSQL/host exporters. A dashboard average can hide saturation and tail latency.

Correlate database work with Data API/PostgREST or RPC duration, pool acquisition,
network/region latency, serialization and application request count. Record the
actual connection path: direct, session pooler or transaction pooler. Diagnose using
the application's path; a direct administrative query does not measure pool waits.
For replicas, measure their own load and replication lag and preserve read-after-write
requirements. Route non-database bottlenecks to the relevant existing performance skill.

## Improve without weakening the product

Measure representative JWT claims, role and RLS policies. An owner/service-role plan
can bypass the cost and visibility rules ordinary callers experience. Test allowed
and forbidden rows, joins, pagination and tenant skew after a query/policy change.
Do not disable RLS to make a benchmark faster. Apply row-independent init-plan
optimizations only when their semantics hold; review any security-definer function's
privileges and search path separately.

Use Performance Advisor and `index_advisor` suggestions as hypotheses. Verify an actual
plan and representative timings, including write/storage cost, before adopting them.
No automatic index builds, query cancellation, pool resizing, compute upgrades,
vacuum operations or deployment. Use existing change authorization and migration
ownership when those actions are part of the requested fix.

Report a baseline/candidate comparison under equal data, concurrency, compute, region
and cache conditions: end-to-end p50/tail latency, throughput, errors/timeouts, CPU,
I/O and pool waits relevant to the bottleneck. Accept an improvement only beyond noise
with the same results, authorization and durability. CLI help validation alone proves
neither hosted access nor performance improvement. Remove owned captures/fixtures after
retaining compact evidence; leave shared observability and caches running.

## Sources and limits

Reviewed 2026-11-15; original synthesis, no provider code imported. Recheck installed
help and official documentation when versions or hosting mode change.

- [Database inspection](https://supabase.com/docs/guides/observability/inspect) and
  [CLI reference](https://supabase.com/docs/reference/cli/introduction): command routing,
  counters and prerequisites. Local CLI 3.1.0 help resolves conflicting flag examples.
- [Reports](https://supabase.com/docs/guides/observability/reports) and
  [high CPU diagnosis](https://supabase.com/kb/troubleshooting/high-cpu-usage): resource signals.
- [Metrics API](https://supabase.com/docs/guides/observability/metrics) and
  [vendor-agnostic collection](https://supabase.com/docs/guides/observability/metrics/vendor-agnostic):
  hosted telemetry and integration; metric schemas can evolve.
- [Query statistics](https://supabase.com/docs/guides/database/extensions/pg_stat_statements),
  [index advisor](https://supabase.com/docs/guides/database/extensions/index_advisor),
  [RLS performance](https://supabase.com/docs/guides/database/postgres/row-level-security-performance)
  and [read replicas](https://supabase.com/docs/guides/platform/read-replicas): mechanism-specific guidance.
