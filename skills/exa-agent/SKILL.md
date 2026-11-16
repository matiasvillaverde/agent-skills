---
name: exa-agent
description: Run multi-step research, list-building and enrichment through Exa Agent, with structured evidence, bounded continuation and coverage validation. Use when Exa Agent is requested or its hosted research workflow fits the task.
---

# Exa Agent research

Use the available `agent_run` tool and inspect its current schema before constructing
requests. Choose ordinary search for a small lookup; use Exa Agent for discovery,
multi-hop investigation, structured research or refinement of a completed run.
For many same-shape operations over known rows, read
[batch enrichment](references/batch-enrichment.md) when authorized direct API access exists.

## Scope the run

Establish the objective, qualifying universe, relevant segments/date window, requested
fields, evidence requirements, exclusions and useful coverage target from the task.
Scale this record to the request; not every research question needs a company-count quota.
Resolve relative dates from the current date. Keep private data out of hosted inputs
unless the task and provider access authorize it.

Use the user's or environment's existing request/time/cost budget. Choose the default
`low` effort unless requested depth or a concrete gap warrants another supported level.
A sparse result is a reason to reassess coverage, not permission for unlimited new runs.

For structured lists or enrichment, define `outputSchema` before running. Prefer a top-level
object, bounded arrays, stable entity identifiers and source/evidence fields. Require only
fields the evidence can supply; allow unknowns rather than inventing data. Read
[structured output](references/structured-output.md) for the schema and provider examples.

## Choose data sources only when needed

Discover supported providers in the current tool contract. The reviewed self-serve set is:

| Provider | Useful data |
| --- | --- |
| `fiber` | B2B companies, people, jobs and contact enrichment |
| `financial_datasets` | Ticker-based news for US public companies |
| `similarweb` | Estimated web traffic, rankings and competitors |
| `baselayer` | US business verification, officers, registrations and KYB |
| `affiliate` | Product catalogs, pricing and merchant links |
| `particle` | Podcast transcripts with speakers and timestamps |
| `jinko` | Travel destination discovery ranked by fare |

Pass `dataSources` only for needed, available providers, and name the required data in
the query/schema. Tool support does not establish this account's entitlement or a
subscription budget. Do not enable a provider or buy access incidentally. Provider
estimates need source/as-of context; do not present them as audited facts.

## Run, resume and validate

1. Start with `query`, using `input.data` for known rows and `input.exclusion` for entities
   already returned or disallowed. Save the returned run ID immediately.
2. If the result is still running, use that ID in `runId` to check or continue the same
   run, following the tool's polling contract. Do not send `query` with `runId` or start
   another run simply because a call timed out or was interrupted.
3. Read the returned terminal status, structured result and grounding/evidence. A
   completed run does not establish exhaustiveness or factual correctness. Check actual
   row count, segment/date coverage, duplicate entities, missing fields and source support.
   Open decisive original sources where needed instead of trusting generated grounding alone.
4. For a completed retained run, `previousRunId` can provide context for a new refinement;
   it is not the polling field. Use exclusions and a specific remaining question. Independent
   segments may need new runs, with their combined cost and deduplication accounted for.

Retention and streaming behavior depend on the team's current mode. Do not assume
`runId` or `previousRunId` recovery exists for a Zero Data Retention run. Check returned
capabilities and current provider guidance; a missing result is a coverage gap, not proof
that no work ran or no cost was incurred.

## Handle failure without duplicating work

Treat tool interruption and explicit upstream cancellation as different events. If the
objective/schema must change, use a supported cancellation operation when available and
verify the resulting status. Aborting a local stream does not prove cancellation. If the
run cannot be reconciled, preserve its ID and uncertainty; do not silently create a
replacement paid run. Continue independent useful analysis within the remaining scope.

For a terminal failure, inspect the actual error, correct a supported input/access issue,
and retry only within existing authorization and budget. Redact credentials and private
payloads from errors. If Exa is unavailable, disclose that and use another available
research route only when the user's constraints allow it; do not claim the fallback was
an Exa Agent result.

## Deliver attributable results

Lead with the answer and structured results, then the actual coverage and material gaps.
Distinguish requested rows, returned rows, deduplicated entities and verified evidence.
Claim exhaustiveness only for a bounded universe with checked coverage; otherwise report
best-effort discovery. Preserve source dates and separate facts, estimates and inference.
Report costs only when returned. Save useful run IDs and compact evidence privately for
continuation; a successful tool envelope is not a completed research outcome.
