# Swift build instrumentation

## Establish identity and collect the smallest useful evidence

Record selected developer directory, `xcodebuild -version`, `xcrun swift --version`, scheme/
product, configuration, destination/architecture and effective flags. Inspect installed help
before applying a documented option. Preserve the project's existing flags and resolution rules.
For generated projects, include generation time and identify the manifest that owns settings.

Xcode's Report navigator and Build With Timing Summary expose task timing; the Build Timeline
helps identify scheduling and dependencies. An existing command-line build can add
`-showBuildTimingSummary`. For example, adapt this shape to real inspected values:

```sh
xcodebuild -workspace 'App.xcworkspace' -scheme 'App' \
  -configuration Debug -destination '<selected destination>' \
  -derivedDataPath '<task-owned DerivedData>' \
  -resultBundlePath '<new private result path>.xcresult' \
  build -showBuildTimingSummary
```

Use the same output directory for warm/edit runs; a fresh one each time changes the experiment.
Result paths must be new where the tool requires it. Preserve command exit status if formatting
or teeing logs. Distinguish compile tasks, dependency waits, scripts, links and signing; task
totals can overlap and are not outer wall time or CPU utilization.
[Apple incremental-build measurement](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds),
[Apple build parallelization](https://developer.apple.com/videos/play/wwdc2022/110364/).

For SwiftPM, use the installed `swift build`/`swift test` options and selected product/target.
`--scratch-path` isolates build state, `--cache-path` is a different layer and `--jobs` controls
build concurrency where supported. Keep the backend fixed. SwiftPM 6.4 changed the default
to Swift Build and changed artifact layout; discover binaries with `swift build --show-bin-path`
using the same relevant options rather than assuming `.build/debug`. A successful `--product`
build is not proof that every independent package target was built or tested.
SwiftPM 6.4 also makes `--use-integrated-swift-driver` a deprecated no-op; old flag recipes
do not prove a change. [SwiftPM 6.4 notes](https://docs.swift.org/latest/documentation/packagemanagerdocs/6.4/).

## Locate expensive compiler work

Use actual slow frontend invocations/target evidence before adding diagnostics. Installed
compiler help determines support. Common focused tools include:

- Frontend `-warn-long-function-bodies=<milliseconds>` and
  `-warn-long-expression-type-checking=<milliseconds>` for leads, with thresholds chosen for
  this workload rather than a universal lint budget.
- Frontend `-debug-time-function-bodies` / `-debug-time-expression-type-checking` for timing
  detail. Imports and lazy work can be charged to the expression that first triggers them;
  these timers do not cover all SIL/LLVM/codegen or linker costs.
- Driver `-driver-show-incremental` with verbose output for rebuild reasoning, and
  `-driver-time-compilation` for driver task timing where supported.
- Driver `-stats-output-dir <existing-private-directory>` for supported compiler statistics.
  Discover actual keys and units; distinguish wall/user/system measurements and do not assume
  a fixed JSON schema across compiler builds.

Frontend options need the appropriate `-Xfrontend` forwarding when using the driver. SwiftPM
forwarding and Xcode OTHER_SWIFT_FLAGS inheritance are separate layers: merge diagnostics into
the real invocation without discarding existing values, then restore them. Changed flags can
invalidate the build and distort comparison. Confirm final results without heavy diagnostics.
Missing warnings do not clear a slow module. Use a scoped process/native CPU profile when
compiler statistics cannot explain where time is spent, without profiling unrelated processes.
[Swift compiler performance guide](https://github.com/swiftlang/swift/blob/main/docs/CompilerPerformance.md),
[timer attribution caveats](https://forums.swift.org/t/potential-contributions-to-compilation-time-reporting/7055).

## XCLogParser, XCMetrics and recorded Tuist runs

Use an available compatible parser against an exact selected build log. Installed
XCLogParser 0.2.50 accepted this command shape at the 2026-11-15 review:

```sh
xclogparser parse --file '<selected>.xcactivitylog' \
  --reporter json --output '<private output directory>' --redacted
```

Inspect its help, supported reporters and output before scripting analysis. Redaction is not
a guarantee that all private commands, paths or source text disappeared. Do not upload raw logs
automatically. Verify parser/Xcode compatibility and sanity-check task totals against the original
build; missing/truncated/unrecognized data is a coverage gap. A clean/incremental classification
is an inference, not evidence that the requested caches were empty.
[XCLogParser upstream](https://github.com/MobileNativeFoundation/XCLogParser).

XCMetrics adds ingestion/storage/aggregation around build logs. Use an existing installation's
compatible records if available; deploying a new backend is not required to diagnose one build.
At review it was not archived but its latest published release was from 2023 and last push
from 2024, so evaluate current compatibility/maintenance before adopting it. Separate its
classification, sampling and cohort definitions from controlled local scenarios.
[XCMetrics upstream](https://github.com/spotify/XCMetrics),
[published release](https://github.com/spotify/XCMetrics/releases/tag/v0.0.13).

For existing Tuist data, compare exact run IDs, source, scheme/configuration, machine, compiler,
edit scenario and cache state before task/cache deltas. Use installed CLI/API capabilities,
paginate where needed and label inferred invalidation cascades. Latest runs on different
branches are leads, not matched measurements. Do not introduce accounts or telemetry uploads
just to produce a dashboard.
`tuist inspect build` can report/upload build data; it is not simply an offline parser.
Post-actions and collectors can omit failed/cancelled builds or add latency, so inspect their
coverage and execution boundary before using aggregate metrics.
[Tuist build insights](https://tuist.dev/en/docs/guides/features/build-insights/xcode).
