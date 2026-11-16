---
name: perf-browser-memory
description: Diagnose browser JavaScript and DOM memory growth using repeatable lifecycles, heap comparisons, and retaining paths.
license: Apache-2.0
---

# Browser memory investigation

Start from a reproducible user lifecycle: opening and closing a view, subscribing and unsubscribing, navigating back, or starting and cancelling work. Identify the exact page, build, browser, and execution context. Browser heap evidence does not establish a backend, GPU, or native-process leak.

## Choose useful evidence

Discover the available browser memory tools and their current schemas. Prefer summaries, snapshot comparisons, allocation profiles, and retaining-path queries over reading enormous raw heap files. Chrome DevTools advanced heap tools may require its memory-debugging option; report missing capabilities without silently installing packages, adding MCP servers, or changing configuration. Do not introduce Playwright or another test framework.

Choose the measurement for the question:

- Process memory shows overall pressure but does not identify its cause.
- Allocation profiling identifies code creating objects; allocation volume is not retained memory.
- Heap comparisons and retainers explain what survives cleanup and why.
- DOM, listener, worker, timer, or subscription counts can expose specific lifecycle failures.

Rising RSS, a large heap, or a detached DOM node alone is insufficient proof. Garbage collection, allocator behavior, bounded caches, and browser internals can retain memory legitimately. DevTools consoles and inspected-object references can also keep objects alive.

## Reproduce a lifecycle

Warm up normal initialization and record a baseline at a defined resting state. Perform the relevant action, observe its working state, then undo or close it and let expected asynchronous cleanup finish. Compare the same resting state afterward. Repeat only enough to distinguish persistent growth from initialization, bounded caching, and noise; no fixed iteration count is required.

Keep build, fixture size, page state, and capture conditions comparable. Record whether garbage collection was requested and use that choice consistently; do not assume collection proves all resources were released. Confirm timers, listeners, subscriptions, detached views, and background requests stop when the feature promises they will.

Keep heap snapshots and traces in private, unique local paths. They may contain credentials, messages, or other application data. Summarize counts, sizes, object types, and relevant ownership paths without dumping object values or uploading snapshots to third-party services.

## Explain and fix retention

Compare snapshot summaries and class growth first. Drill into representative objects, retaining paths, and dominators only where growth supports the hypothesis. Distinguish shallow size from the objects retained through an owner; avoid adding overlapping retained sizes as independent totals.

Trace the reference back to application ownership and its intended lifetime. Check whether a cache is deliberately bounded or a listener is still needed before changing it. Fix the smallest lifetime error: release a subscription, stop a timer, remove a stale reference, or bound an evidenced cache. Do not scatter null assignments or introduce WeakMaps merely because an object survives.

Repeat the same lifecycle after the fix and verify behavior still works. Add a regression test only when it protects a stable lifecycle contract.

Report the reproduction, baseline and post-cleanup observations, retaining owner, fix, and verification limits. Say when evidence supports only a hypothesis.

## Finish and clean up

After saving the findings and measurements, close loaded snapshots, stop owned captures and remove temporary instrumentation, task-created heap snapshots, traces and isolated browser profiles/caches. Track their exact paths from creation; preserve the user's browser profile, shared caches and application data. Keep only requested/required evidence or the minimum needed for an unresolved investigation. Restore task-changed settings even on failure or cancellation. Verify cleanup and report retained artifacts or leftovers with the reason.

Modified adaptation of Chrome DevTools' [memory-leak-debugging](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/8ba2ac945ebaf1adb92208c29f3a30e73a920956/skills/memory-leak-debugging/SKILL.md), Apache-2.0; replaces fixed repetitions and setup assumptions with evidence-based choices.

Sources, modifications and licensing: [NOTICE.md](NOTICE.md).
