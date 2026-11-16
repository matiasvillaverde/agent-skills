# Swift code, module graphs and parallel work

## Use the actual critical path

Inspect target edges and executed actions, not just the folder tree or summed compile duration.
Remove accidental dependencies after checking imports, linked symbols, runtime registration,
resources and scripts. Missing real edges can produce races or stale products. A large target
may benefit from cohesive splits, but a long chain of small targets still serializes work and
adds module scanning/emission, linking and maintenance.
[Apple parallelization](https://developer.apple.com/videos/play/wwdc2022/110364/),
[incremental-build contracts](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds).

Compare a private implementation edit, a public interface edit and fresh artifacts before
accepting a graph change. Prefer stable shared vocabulary and feature boundaries with observed
change locality. Keep dependency cycles and broad umbrella imports visible. Do not impose
interface/implementation/mock/example/test targets for every feature solely to populate cores.

A focused feature host, preview or generated workspace can reduce build and indexing scope
when the architecture already supports it. Preserve full-app integration and release checks;
verify that the focused target exercises the intended feature. A faster graph with disconnected
required targets is invalid evidence. Airbnb's Dev Apps are a useful pattern; Uber Poet showed
why a plausible graph refactor can fail and omitted reachable work can create a false gain.
[Airbnb's development workflow](https://medium.com/airbnb-engineering/designing-for-productivity-in-a-large-scale-ios-application-9376a430a0bf),
[Uber's counterexample](https://www.uber.com/us/en/blog/uber-poet/).

## Fix source and generated-work costs selectively

Use compiler evidence to locate difficult overload inference, large expressions/result builders,
generic expansion, macro work and repeated imports. Clear intermediate values and explicit types
at ambiguous boundaries can reduce solver work while improving readability. Break a measured
expensive SwiftUI body into coherent views only with identity, state and behavior preserved.
Do not add `AnyView`, unsafe casts, blanket `@inlinable` or access-control changes as compile-time
shortcuts. Small source text can expand into expensive work; line count is a weak proxy.

For mixed Swift/Objective-C code, inspect bridging headers, public headers, forward declarations,
implementation-only details and module maps. Inconsistent flags can create multiple variants
of the same module. Normalize only genuinely equivalent settings; architecture, language mode,
availability and conditional definitions may be semantically necessary differences.
[Apple coding practices](https://developer.apple.com/documentation/xcode/improving-build-efficiency-with-good-coding-practices).

Explicit-module builds separate scanning, dependency-module compilation and source compilation;
they are not Tuist's prebuilt-target module cache. Inspect variants and effective settings for
the selected Xcode and interoperability modes before tuning. A private edit does not guarantee
zero dependent compilation; verify actual graph/interface output.
[Apple explicit modules](https://developer.apple.com/documentation/xcode/building-your-project-with-explicit-module-dependencies).

Declare true script/plugin inputs and outputs, including file lists and external tools where
the build system supports them. Keep output deterministic and avoid touching unchanged files.
Verify missing outputs regenerate and real input edits invalidate. A stamp file that hides
untracked inputs or a silent failed generator is not a performance improvement. Do not disable
dependency analysis or script sandboxing to silence an inconvenient build diagnostic.

## Parallelism and prevention

Use dependency-order scheduling and the installed build system's job controls. Count concurrent
builds, Swift frontend batches, native compilation, indexing, previews and simulators together.
A few measured job budgets are more useful than setting every layer to the full core count.
Observe memory pressure, contention and interactive responsiveness as well as elapsed time.
Verify effective driver/backend scheduling as well as the requested outer job count; one
SwiftPM/Xcode limit does not prove every compiler subprocess uses that same thread budget.

Keep the existing Debug/Release modes and debug-capable workflow unless a measured, authorized
tradeoff justifies change. Old whole-module/batch-mode recipes and assumptions about a file
per compiler process do not transfer automatically to new Xcode/Swift Build versions. Changing
static/dynamic/mergeable linkage needs runtime startup, resources and packaging checks too.

Use existing lint/build checks for actual contracts: undeclared graph edges, generated-output
drift, incompatible flags or scripts missing their true inputs. SwiftLint length rules are not
compiler-time measurements. Compiler timing warnings are diagnostic leads whose thresholds
vary with caches/hardware, not a universal deterministic CI gate. Keep a small repeatable edit
scenario for an observed regression when maintaining it is worthwhile.
