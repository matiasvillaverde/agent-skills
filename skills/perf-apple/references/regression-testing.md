# Make Apple performance regressions reproducible

Use for a completed feature or a regression worth protecting. Reuse the integration/UI harness
and [acceptance criteria](acceptance.md). Keep a few representative user operations, plus focused
algorithm tests where useful. Avoid helper-by-helper microbenchmarks, parameterized device/cache
matrices, or merging different failure contracts just to reduce test count.

## Define the operation and its evidence

Record observable start/end, fixture/input, app/build/symbol identity, device/OS, configuration and
metric. Include usable completion: interactive content, audible output, displayed frame or completed
computation. Enqueueing a request, showing a placeholder or submitting GPU commands is not completion.

Separate fresh process, first-use initialization and warmed work. Document the application state
reset; process restart does not clear OS/storage caches. Never sweep shared caches to manufacture
a cold result. Use controlled fixtures for repeatability and label real network/backend tests
separately. Wait on observable readiness rather than arbitrary sleeps.

Use XCTest performance metrics and XCUITest interactions; Swift Testing does not replace these
facilities. Choose supported clock, CPU, memory, launch, signpost or hitch/scroll metrics matching
the claim. If excluding setup with explicit measurement boundaries, explain why it is outside the
user operation. Do not move required work outside timing to make a result pass.

## Control timing conditions

Apple recommends representative Release builds without an attached debugger, code coverage or
runtime sanitizers for performance measurements. Keep required correctness/sanitizer runs in a
separate plan. Use physical devices for device CPU/GPU/memory/energy claims; Simulator can verify
behavior and the harness, with its timing limits stated.
[Performance-test guidance](https://developer.apple.com/documentation/xcode/writing-and-running-performance-tests).

Match hardware, OS, display, power/thermal state, toolchain and input. Schedule one timed workload
per device, without competing jobs; independent build/functional jobs can remain parallel elsewhere.
Interleave baseline/candidate runs when useful. Record run order and disturbances, not only the best
samples. Report unavailable/cooling devices as a gap rather than claiming a completed comparison.

## Reuse builds and inspect actual results

Use the project's existing command owner, scheme/test plan and Tuist integration when present.
Inspect `xcodebuild -help`, destinations and the generated `.xctestrun` before adapting these shapes.
Do not migrate project generation or install a new runner merely to use this workflow.

```sh
xcodebuild build-for-testing -workspace '<workspace>' -scheme '<scheme>' \
  -testPlan '<performance-plan>' -configuration Release \
  -destination 'id=<device-id>' -derivedDataPath /private/task/DerivedData

xcodebuild test-without-building -xctestrun '<actual-generated-file.xctestrun>' \
  -destination 'id=<device-id>' -only-testing:'<target>/<case>/<method>' \
  -parallel-testing-enabled NO -resultBundlePath /private/task/candidate.xcresult

xcrun xcresulttool get test-results metrics --help
xcrun xcresulttool get test-results metrics --schema
xcrun xcresulttool get test-results metrics \
  --path /private/task/candidate.xcresult --compact
```

Keep baseline/candidate builds separate and verify the `.xctestrun` identifies the intended artifact
and configuration. A compatible cached build is useful; cached test results are not fresh timing.
Use unique result paths. Inspect exit status, failures/skips, executed test identity and samples,
not just the metrics JSON. The reviewed `xcresulttool` advertises schema 0.4.0; discover the installed
schema instead of inventing JSON fields. [Measurement options](https://developer.apple.com/documentation/xctest/xctmeasureoptions)
control iteration count and invocation boundaries; choose them for the workload rather than assuming
default iterations validate every statistic.

## Compare without hiding noise

Use the existing environment-specific baseline/tolerance and meaningful product budget. An XCTest
measurement without a baseline is not a passing regression budget. Record baseline revision and
any authorized rebaseline rationale; never reset it automatically to make a candidate green.

Retain repetitions and variability. A handful of iterations cannot establish p99; average FPS
does not rule out hitches. XCTest's standard-deviation tolerance is not a universal significance
test. If noise hides the expected effect, improve the fixture/environment or label it inconclusive
instead of relaxing the threshold, discarding slow runs or selecting the best retry.

Check behavior, output quality and secondary resources beside speed. Keep cold/warm populations
and device families separate. A faster path with retained tasks, extra requests, memory growth,
stale output or reduced media quality is not an accepted improvement.

## Fit the checks into CI

Keep deterministic correctness and lightweight harness checks in the existing fast path. Run
device timing in an owned, controlled lane at a cadence justified by cost/risk; reuse existing
device reservations rather than adding a fleet scheduler. Validate selected versus executed tests
and preserve per-device failures/skips. Choose a minimum meaningful supported/affected device set.
Use `perf-ci` for build/cache scheduling when available; runtime acceptance remains here.

Calibrate a new/changed gate with one known slowdown or prior regression fixture in an isolated
setup, then remove the probe. Retries retain first-attempt failures. Separate runner faults from
product regressions. Production cohort verification is another stage and can use
`perf-apple-production` when available; local success does not prove rollout success.

Report operation, revisions, conditions, sample count, values/variation, baseline/budget, behavioral
evidence and accepted/inconclusive/regressed/not-verified status. Retain compact results and required
failure attachments; remove exact task-owned DerivedData, result bundles, traces and isolated
caches after triage. Preserve shared caches/baselines, restore task-changed device/network settings,
and stop only owned runners and profilers.
