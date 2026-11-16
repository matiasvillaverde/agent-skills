# Read MetricKit evidence through Datadog and Pup

Optional adapter; the [core workflow](../SKILL.md) and [MetricKit semantics](metrickit.md) also work
with databases, object storage, telemetry APIs or another provider. Reviewed with local **Pup 2.4.3**
help on 2026-11-14. No live tenant data or upload path was qualified by this documentation work.

## Discover the actual mapping

Read the project's Datadog runbook, collector/exporter and logging/metric contract. Use raw `pup`
where the project requires it. Select the existing authenticated organization/site and environment;
do not install a wrapper, switch tenants, print tokens or acquire broader credentials for a query.

Determine whether MetricKit is stored as logs, RUM diagnostic attributes, custom metric aggregates,
or private reports linked from Datadog. Do not infer a full native-report pipeline from RUM Mobile
Vitals, a diagnostic summary or a payload-count field. Distinguish implemented collection from a
proposed schema. Map source window and measured build separately from the exporter service/version.

Inspect installed command help before adapting these templates:

```sh
pup --version
pup logs search --help
pup logs aggregate --help
pup metrics query --help
pup rum aggregate --help
```

Replace every placeholder with discovered values. Start with a small structural sample, using
an explicit UTC query window broad enough for expected delivery delay:

```sh
pup --read-only --org '<existing-org>' logs search \
  --query 'service:<service> env:<environment> <verified-report-selector>' \
  --from '<UTC-start>' --to '<UTC-end>' --limit 20
```

Use `service:`/`env:` tags and `@attribute` syntax as appropriate to the actual record. Escape
query values using [Datadog search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
Keep samples private and bounded; report structural fields or redacted aggregates rather than
copying raw user content. Pup supports `--jq`, but inspect its current raw-response root and retain
error, truncation and pagination metadata. A filtered output can hide required evidence.

Then use the matching surface; these are shapes, not existing metric names or interchangeable
query languages:

```sh
pup --read-only --org '<existing-org>' logs aggregate \
  --query '<verified-query>' --from '<UTC-start>' --to '<UTC-end>' \
  --compute count --group-by '<approved-cohort-facets>' --limit 20

pup --read-only --org '<existing-org>' metrics query \
  --query '<validated-metric-query>' --from '<UTC-start>' --to '<UTC-end>'
```

`count` counts matching records, not necessarily reports, affected users or diagnostic events.
Do not apply a percentile to a field already containing per-report percentiles. Use the stored
aggregate contract or fetch compatible bins/counts through the existing private report interface.
For RUM-only data, use its supported command and preserve RUM sampling/session semantics.

Inspect cursors and limits, excluded/indexed data, storage tier, retention, query warnings and
facet top-N truncation. Follow supported cursors within the budget or label the result partial.
An empty search may mean wrong mapping, restricted access, delayed delivery or absent indexing.
Check pipeline freshness before interpreting it as no incident. Expand scope only to resolve a
specific gap; a fleet-wide raw-log dump is unnecessary.

## Keep delayed metrics honest

Current [historical-metric documentation](https://docs.datadoghq.com/metrics/custom_metrics/historical_metrics/)
requires historical ingestion to be enabled for old points and supports counts/rates/gauges,
not distributions or log-generated custom metrics. Verify current account/type support before
backdating delayed MetricKit data. Do not replay histogram buckets as fresh individual samples.

If using current-time snapshot gauges, label them as the latest completed source window and expose
window boundaries, eligible report/exposure counts and freshness. Their Datadog timestamps represent
publication, not the device event. A trend of those snapshots is not automatically a daily event-time
trend. Reuse the existing exporter and keep its mapping independent of app business logic.

Keep cohort tags bounded; report/device/user IDs belong in controlled records when needed, not
custom-metric dimensions. Preserve authenticated diagnostic links and original symbol identity.
Avoid full payloads/stacks in ordinary RUM attributes, and verify export retries do not multiply data.

## Evidence and cleanup

Save the exact redacted query, organization/environment selection, retrieval time, source window,
units, mapping version, coverage and pagination state. Distinguish readable data from verified
end-to-end delivery. Leave dashboards, monitors, ingestion configuration and retention unchanged
unless the user requested those changes. Delete task-owned exports after retaining findings;
preserve backend records and required diagnostic evidence.

CLI sources: [Pup](https://github.com/DataDog/pup),
[command reference](https://github.com/DataDog/pup/blob/main/docs/COMMANDS.md).
Datadog's [Apple Mobile Vitals](https://docs.datadoghq.com/real_user_monitoring/application_monitoring/ios/mobile_vitals/)
describes its RUM measurements; their existence does not prove native MetricKit report storage.
