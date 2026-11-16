# MetricKit collection, storage and interpretation

Reviewed 2026-11-14 against current Apple documentation and selected Xcode 27 SDK declarations.
This is workflow guidance, not a new storage schema. Contents: availability, storage boundary,
analysis rules, verification and sources.

## Select the actual API and platform

Inspect deployment targets, SDK declarations and the existing collector before proposing a change.
On supported OS 27 targets, `MetricManager` exposes async metric and diagnostic sequences and
Codable reports. Older integrations use `MXMetricManager` and `MXMetricManagerSubscriber`.
Do not register both for the same data or raise the deployment target merely to adopt newer APIs.
Retain the collector/consumer tasks for their intended lifecycle; keep serialization and upload
off the UI-critical path. Verify cancellation/restart behavior rather than creating another consumer
on every view appearance. [Current framework](https://developer.apple.com/documentation/metrickit),
[collection model](https://developer.apple.com/documentation/metrickit/monitoring-app-performance-with-metrickit).

Framework availability is not metric availability. Apple documents diagnostics on macOS 12+ but
daily metrics via the legacy manager on macOS 26+; visionOS supports diagnostics rather than the
same daily metric set. Check each selected API and platform. Legacy delivery can produce separate
payloads from different sources and previously undelivered days; “once per day” is not a dedup key.
Diagnostics being available promptly does not guarantee immediate backend delivery after a crash,
offline period or suspended execution. [Legacy manager](https://developer.apple.com/documentation/metrickit/mxmetricmanager).

In the newer model, interval and app-state entries are complementary views of reported work.
Empty state entries can mean no StateReporting adoption or no active state; they do not mean no
work occurred. Use a few bounded feature states when needed, without request/user IDs in state
labels. A label alone does not establish exclusive causal attribution.
[StateReporting example](https://developer.apple.com/documentation/metrickit/track-performance-by-app-state-using-metrickit).

## Keep one small storage boundary

Read the existing contract and map these concepts; do not introduce another schema registry,
provider SDK in feature code, or a backend abstraction hierarchy just to support this skill.

| Concept to preserve | Why it matters |
| --- | --- |
| App/environment, native API/schema, normalization version | Separate products, parsing rules and incompatible representations |
| Source interval/event time and receipt/processing times | Late reporting cannot masquerade as fresh runtime activity |
| Measured app/build, OS/device, mixed/unknown-version status | An uploader's current build or session may differ from the measured one |
| Metric identity, value type, original unit, counts/bins and compatible exposure | Permit valid comparisons and reproducible aggregation |
| Stable delivery/report identity and source/domain | Suppress transport replay without discarding distinct reports sharing a date |
| Private diagnostic reference, image UUIDs, architecture, offsets and available stacks | Enable access-controlled symbolication without dumping stacks into routine logs |
| Explicit absence, drop, rejection, quarantine and freshness state | Missing measurements must remain distinguishable from healthy zeroes |

Use existing durable storage when full reports are needed for symbolication/reprocessing; otherwise
keep the smallest adequate projection and disclose lost detail. Preserve raw bytes only under the
product's access/retention policy. Set size limits for both compressed and expanded input. Keep a
bounded queue with stable retry identity, acknowledgement-based removal and visible drops; reuse
the product's consent/account-transition rules. No business operation should wait for export.

Reprocessing must replace a report's prior contribution under an explicit normalization version,
not increment it again. An export retry must not double-count a metric. Preserve source time in
storage even when the destination cannot ingest historical metric points. A publication-time
snapshot is acceptable only when its completed source window and freshness are clearly identified.

## Aggregate without creating a false improvement

These are analysis rules, applied only to available compatible data:

| Evidence | Handling |
| --- | --- |
| Full-day, shorter interval and state views | Choose one compatible representation; do not sum overlapping views or assume states/domains partition time |
| Histograms | Merge compatible bins and counts. Different bins require a defensible common representation or separate cohorts. Report bucket/quantile approximation; never average payload p95s |
| Means with sample counts | Weight by the population represented by those counts; missing counts do not authorize an unweighted fleet mean |
| Peak footprint | Compare distributions of report peaks; do not sum them or call their average the fleet peak |
| CPU, GPU, bytes and disk writes | Preserve units and divide only by compatible useful work or exposure; no per-feature allocation from an unsegmented daily total |
| Hang/hitch measurements | Keep Apple's supplied metric semantics. Do not silently substitute an unadjusted ratio or average ratios with unequal/unknown exposure |
| Mixed-build legacy payloads | Respect `includesMultipleApplicationVersions`; `latestApplicationVersion` is the version at the end, not attribution for every sample |
| Diagnostics and terminations | Count distinct events with explicit identity/coverage; compare rates only with a valid denominator and retain unsymbolicated cases |

Apple's typed measurements, distributions and average statistics are described in
[report analysis](https://developer.apple.com/documentation/metrickit/analyzing-app-performance-with-metrickit).
The [legacy payload](https://developer.apple.com/documentation/metrickit/mxmetricpayload) owns version
and timestamp semantics. Compare mature windows with similar exposure and collection policy;
release adoption, consent, sampling, device mix and reporting delay can all change apparent results.
Keep no-data and stale-data states separate from a performance alert; use existing product budgets.

## Verify the pipeline proportionately

Use a few meaningful integration fixtures at the existing ingestion/query boundary: a native and
legacy report where supported, replay of the same delivery, mixed-version attribution, overlapping
views, absent/zero exposure, one meaningful unit conversion and a diagnostic with matched/missing
symbols. Exercise offline/retry and queue limits only when transport changes. Verify a rejected or
partially parsed payload stays visible; new enum cases must not silently become zeroes.

Injected/Xcode-simulated reports prove handling, not actual app performance. For live qualification,
follow a genuine physical-device report through durable acceptance, the stored representation and
the final backend read, with its measured build/window preserved. Verify a diagnostic and symbol
lookup if claiming diagnostic coverage. A receipt counter establishes receipt, not full collection.
Do not generate a real crash or perform a production write merely to author or review this skill.
