---
name: perf-web
description: Measure and improve browser loading, responsiveness, and Core Web Vitals using field data and repeatable traces.
license: MIT
---

# Web performance

Start with the affected journey and user-visible delay. Preserve the project's framework, budgets, authorization, and existing instrumentation. Inspect the relevant versions and available browser/profiling capabilities before selecting commands. Use existing tools; this skill does not require new packages, MCP configuration, Playwright, or a performance framework.

When citing metric thresholds, scoring or tooling APIs, check current primary documentation
from web.dev, Lighthouse or Chrome DevTools. Tool estimates help prioritize an investigation;
they are not observed user savings.

## Establish the evidence

Keep these sources distinct:

| Evidence | What it establishes |
| --- | --- |
| CrUX or first-party RUM | Aggregated experience of the measured user population |
| Browser trace or Lighthouse run | One controlled load or interaction and its causes |
| Source inspection | A hypothesis requiring runtime confirmation |

When available, use field data to prioritize impact. Prefer URL-level data; label origin fallback explicitly. Record device cohort, p75, time window, and available sample information. Missing CrUX data is unavailable, not passing. Local, private, new, and low-traffic pages can still be diagnosed in the lab. Do not submit private URLs to external services merely to obtain field data.

For lab evidence, identify the exact build, route, page state, browser/tool version, viewport, network/CPU conditions, authentication/consent state, and cache behavior. A reload alone does not establish a cold cache; verify cache bypass and service-worker behavior when relevant. Preserve these conditions for comparison. Avoid reloading unsaved work or replaying consequential actions.

## Find the cause

Record the affected load or interaction, then inspect the few relevant insights:

- **LCP:** identify the actual candidate and separate document response, resource discovery, transfer, and render delay. Follow its request chain before adding preload, priority, caching, or rendering changes.
- **INP:** reproduce representative clicks, typing, or navigation. Separate input delay, handler processing, and presentation delay. Measure asynchronous time to usable results separately from next-paint responsiveness. A load-only run cannot establish interaction responsiveness. TBT is a lab blocking diagnostic, not field INP.
- **CLS:** inspect when shifts occur and what triggered them, including relevant post-load content. The visibly shifted element may be the victim.

Inspect network and main-thread costs implicated by the trace. Check duplicate requests, delayed discovery, expensive rendering, and third-party work. One session with no request to an origin does not prove it unused across other journeys. Avoid broad optimization checklists or unrelated accessibility/SEO audits.

If trace tools are missing, use an existing compatible lab tool or source evidence and state the measurement gap. Discover tool schemas rather than copying historical names or flags. If production RUM is requested, reuse its pipeline and allowlist attribution; keep URL parameters, private paths, DOM text, and payloads out of reports.

## Change and verify

Make the smallest change supported by the evidence. Reproduce the same journey under comparable conditions; repeat enough to assess variation, reporting the sample count and spread. Separate cold and warm results. Preserve behavior, security, cache isolation, and accessibility. Avoid new memoization, dependencies, or tests without a demonstrated benefit.

Report the bottleneck, observed before/after metric with units, conditions, and remaining uncertainty. Keep any retained trace references concise and private. Claim a lab improvement only when supported; field improvement remains pending until comparable new user data exists.

## Finish and clean up

Save the measurements and reproduction commands, then stop owned captures/servers and remove task-created traces, HAR files, temporary reports and isolated profiles/caches. Track exact task-owned paths; preserve shared caches, the user's browser state and application data. Restore throttling and temporary instrumentation/settings even on failure or cancellation. Retain only requested/required evidence or the minimum needed for unresolved failures. Verify cleanup and report any retained artifacts or leftovers with the reason.

Adapted from Addy Osmani's [performance and Core Web Vitals skills](https://github.com/addyosmani/web-quality-skills/tree/afa8da942115f2961fdbfa80807ea0b232ff6c00/skills), MIT; this version narrows scope and removes prescribed setup and generic optimization recipes.

Sources, modifications and licensing: [NOTICE.md](NOTICE.md).
