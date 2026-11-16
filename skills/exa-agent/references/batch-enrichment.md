# Batch enrichment over known inputs

Use this mode when known rows need many same-shape API requests and existing authorized
Exa API access is available. An authenticated MCP connection does not necessarily expose
credentials for direct scripts. If direct access is absent, use the supported MCP surface
within its limits or report the gap; do not extract connector credentials.

Read the current API contract before implementing a small script in the task's existing
scratch/output location. Keep stable input IDs and deterministic output order, bounded
concurrency, per-call deadlines, a total request/time/cost envelope and checkpoints.
Retry transient failures only within the API's retry contract and budget. Reconcile an
ambiguous run-creation outcome before starting another paid run.

Resume from completed input IDs rather than repeating the entire batch. Preserve
per-row error categories and evidence privately without logging credentials or full
sensitive responses. Keep missing data distinct from zero or an empty successful result.
Read and validate the output before synthesis; a script exiting zero is not coverage.
Use Exa Agent instead when discovery, multi-hop research or deciding the next query is
the substantive work. Do not create an API framework for a one-off batch.
