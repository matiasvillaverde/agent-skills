---
name: perf-postgres
description: Diagnose and improve PostgreSQL and Supabase database performance using execution plans, CLI diagnostics, CPU metrics, query statistics, indexes, locks and connection pools.
---

# PostgreSQL performance

Identify the slow operation, selected server/environment, PostgreSQL major version,
schema, role/RLS and representative parameter distributions. Separate client/network,
connection-pool wait, database execution, locks and commit acknowledgement. Reuse existing
telemetry and benchmarks; define a bounded workload, correctness oracle and useful target.

Read [PostgreSQL profiling](references/profiling.md) for plan interpretation, query
statistics, cardinality, index selection, memory and waiting. Inspect available instrumentation
before enabling anything. Compare interval statistics without resetting shared counters.
A query-family mean can hide skew; choose relevant tenants, ranges and parameter types.

For Supabase, read [Supabase diagnostics](references/supabase.md). Use the installed
Supabase CLI for database inspection, matching its help to the selected project and
branch. Correlate those results with CPU and I/O metrics from Supabase or the existing
observability backend; query elapsed time alone does not measure CPU consumption.

Start with plan-only evidence. `EXPLAIN ANALYZE` executes the statement, including functions
and effects a transaction rollback may not undo. Use actual execution only on a safe bounded
read or an authorized disposable workload. Inspect rows, loops, buffers and waits in context;
a sequential scan or spill is a hypothesis, not automatically a defect.

Test one measured cause at a time. Prefer removing repeated queries or excess work and
correcting statistics/query/index alignment before increasing global memory, adding caches
or changing pooling. Account for operator/worker concurrency, write amplification and index
storage. Use the existing migration owner for schema changes; profiling alone does not
authorize a live index build or service restart.

Compare the same data and parameters under stated cache/concurrency conditions, separating
first-use and warm execution. Repeat enough to expose noise; measure uninstrumented timings
where capture overhead matters. Check exact result multiplicity, NULLs, ordering, precision,
RLS, isolation and durability. Do not improve latency by changing required results or commit
semantics. Include relevant write and concurrent-user costs, errors and timeouts.

Keep the change only when it improves the relevant budget beyond noise without violating
the contract. Run focused regressions and required project checks. Report before/after
distributions with units, workload, sample count and remaining coverage; a local plan or
microbenchmark does not establish production capacity.

Save compact evidence and reproduction privately. Stop owned profilers/load, restore scoped
settings and remove task-created traces, fixtures and caches after analysis, including on
failure. Preserve shared caches, production data and required unresolved evidence.
