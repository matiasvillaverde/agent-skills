---
name: perf-apple-production
description: Investigate Apple app performance in production using MetricKit reports and diagnostics from the existing telemetry backend. Compare releases and device cohorts, verify collection quality, and turn field evidence into a reproducible local investigation. Includes optional Datadog/Pup guidance.
---

# Investigate Apple performance in production

Start with the affected operation, app/build, environment, measurement period and user impact.
Inspect the project's telemetry contract, collector, stored records and retention policy before
querying. Distinguish deployed behavior from a proposed design or a local checkout. Default to
scoped reads; an investigation does not authorize adding telemetry, changing retention/alerts,
deploying an exporter or altering product behavior.

## Discover the evidence

Identify which data actually exists: native MetricKit reports, selected diagnostic summaries,
normalized aggregates, RUM events, logs, or a mixture. RUM vitals and receipt counters are not
substitutes for complete MetricKit reports. Follow a representative record from its source
window through normalization and export; report unavailable stages instead of inventing fields.

Use [MetricKit collection and analysis](references/metrickit.md) for API availability, delayed
delivery, version attribution, histograms, diagnostics and a small provider-independent boundary.
For Datadog, also use [Datadog with Pup](references/datadog-pup.md). For another backend, use its
existing read interface and map the same concepts to its schema; no Datadog dependency is required.
Keep credentials, tenant names and product-specific query mappings in their existing project owner.

Bound the query by app/environment, source period and relevant cohort. Retrieve a small structural
sample, then aggregate at the backend when its semantics are suitable. Inspect query status,
pagination, sampling, retention and freshness. Save only necessary redacted evidence privately.

## Compare the same population

Separate source measurement time, receipt time and processing/publication time. Compare compatible
builds, OS versions, device families, foreground/background and feature state, with exposure and
coverage beside the result. Delayed uploads after an upgrade do not belong to the current build.
Mixed-version or unknown attribution must remain visible, outside a single-build comparison.

Check duplicates and overlapping representations before aggregating. Merge compatible histogram
counts rather than averaging daily percentiles. Keep memory peaks, weighted averages, counters
and rates distinct. Missing, unsupported, sampled-out or stale data is unknown, not zero.
Inspect crash/memory-termination evidence alongside surviving reports to avoid survivor bias.

Rank a few actionable issues by impact, affected exposure, regression size and evidence strength.
Treat cohort correlation as a lead; validate the denominator and competing explanations before
attributing a cause. Do not create a universal score or alert threshold from unrelated metrics.

## Connect production evidence to a fix

For a diagnostic, verify the recorded build, architecture, image UUIDs and matching symbols.
Separate symbolicated evidence from unresolved addresses. Correlate only with compatible time,
build and operation evidence; never attach a historical diagnostic to today's user/session.

Create a bounded local reproduction matching the affected workload and hardware. Use the
`perf-apple` workflow matching the bottleneck when available, or the project's existing native
profiler. Preserve UI, accessibility, functionality, data freshness, media/model quality and
supported hardware. Keep a fix only when controlled measurements and relevant behavior checks
support it. Validate the affected cohort after rollout within the user's authorized release scope;
local success alone does not establish a production improvement.

## If collection or export must change

Reuse the existing collector, queue, ingestion endpoint and backend. Keep normalization and the
provider mapping outside business logic; one small mapping/transport boundary is usually enough.
Preserve native report meaning, source time, units, version attribution and diagnostic identity.
Bound buffering, retries, payload size, CPU/disk/network work and tag cardinality. Check privacy
and current consent at admission and delivery. Test the few consequential failure paths described
in the reference; do not introduce a telemetry framework or a large parameterized test matrix.

## Report and clean up

Report the query scope, data source, source window, coverage/freshness, cohort/exposure, findings,
symbolication state and next discriminating measurement. Label evidence as observed, inferred,
inconclusive or unverified. A successful upload or dashboard read is not end-to-end qualification.

Retain compact findings and reproduction/query commands. Delete exact task-owned raw exports,
temporary traces, symbol copies and isolated caches after analysis; stop owned helpers and restore
task-changed settings. Preserve shared references, original server-side records, symbol archives
and evidence required for unresolved failures or retention. Report any retained artifacts.
