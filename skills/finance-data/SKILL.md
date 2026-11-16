---
name: finance-data
description: Retrieve and reconcile financial prices, histories, fundamentals, rates and economic series. Use when an analysis needs identified instruments, dated observations, comparable units or reliable data-source selection.
---

# Financial Data

Produce data that another analysis can safely use. A successful tool call is not proof
of the instrument, freshness, completeness or meaning of its numbers.

## Identify the request

Resolve the instrument or entity before joining sources: legal company, ticker and
exchange, share class/ADR ratio, ISIN or CIK when relevant, quote currency and unit.
A company, its several listings, its bonds and an ETF holding it are different objects.

Establish the requested period, frequency, session and as-of cutoff from the task.
For current data, read the actual observation timestamp and market calendar; for a
historical decision, exclude information published after the cutoff. Retrieval today
does not make an old close current or a later restatement historically available.

## Choose an available route

Discover the connected tool contracts and existing local integrations. Read
[source routes](references/sources.md) for the relevant source: quotes/history,
filings, economic series, rates or funds. Use an existing structured feed when it
fits, original issuer/regulator data for decisive definitions, and web discovery
to locate missing originals. A proprietary feed is not inherently more authoritative
than the filing it normalizes.

Use authenticated providers only with existing authorized access and suitable data
rights. Keep credentials in their native store. Missing access is a coverage gap;
choose a documented alternative where useful. Research does not authorize buying
subscriptions, creating/funding accounts, changing MCP configuration or placing orders.

## Preserve meaning when collecting

Capture the fields needed to retrace the observation, without imposing a schema on
every answer:

- Identity, source URL/series/filing identifier, value, currency and unit/scale.
- Observation timestamp or period start/end; timezone and session for prices.
- Publication/filing date, revision/vintage and retrieval time where they differ.
- Price type: trade, bid/ask, close, NAV, indicative quote, yield or reference rate.
- Adjustments and transformations: splits, dividends, FX, seasonality, annualisation.
- Coverage and limitations: delayed, stale, partial, estimated, revised or unavailable.

Keep missing values and provider errors distinct from zero. Retain the original
observation alongside calculations. Bound/paginate requests to the period needed;
check response limits, truncation and empty/error payloads even after HTTP success.

For price histories, sort and deduplicate by instrument/time, inspect gaps and
corporate actions, and compare like sessions. A partial daily bar is not yesterday's
close. A continuous futures series can change through contract rolls. State whether
returns include dividends, splits and FX; avoid double-adjusting data.

For statements, distinguish instant balance-sheet values from duration cash-flow or
income values; a nine-month cumulative figure is not one quarter. Inspect taxonomy,
units, fiscal dates, filing date, amendments and context before selecting a fact.
Read the filing when normalized data omit a segment or change a definition.

## Reconcile and deliver

When important sources disagree, compare identity, timestamps, adjustments, scale and
definitions before choosing one. Do not average incompatible observations. Recalculate
material ratios/returns with code or a spreadsheet and label assumptions. Use
[calculation checks](references/calculations.md) when computing returns or comparing yields.

Return the requested data or compact table with source and as-of information, explaining
only material gaps. Save larger datasets and provenance in the existing owner location;
private or licensed extracts stay outside Git/public reports. Preserve enough raw context
to audit a result without republishing a provider's licensed dataset.
