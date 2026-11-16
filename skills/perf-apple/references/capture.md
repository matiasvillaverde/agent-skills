# Capture recipes, native templates and automation

Use the [instrument catalog](instruments.md) to choose the question and workflow.
The 17 entries in [capture-recipes.json](../assets/capture-recipes.json) pair this skill's
modes with **installed Apple templates**. They are portable CLI recipes, not binary
`.tracetemplate` files. `covers` assigns documentation ownership; it does not enable every
listed instrument in one recording. This distinction keeps overhead and trace volume bounded.

## Discover the actual environment

```sh
xcode-select -p
xcrun xctrace version
xcrun xctrace list templates
xcrun xctrace list instruments
xcrun xctrace list devices
xcrun xctrace help record
xcrun xctrace help export
```

Keep explicit `DEVELOPER_DIR` consistent across build, CLI, Instruments, simulators and
automation. Prefer a signed optimized app with matching dSYMs. A selected offline device,
missing framework events, unsupported counter or inaccessible process is a coverage gap.
Do not treat successfully listing an instrument as qualification for that target.

The inventory reviewed on 2026-11-14 has 25 standard templates:

| Templates | Purpose |
| --- | --- |
| Activity Monitor; Time Profiler; CPU Profiler; CPU Counters; Processor Trace | Process trends, CPU sampling and hardware analysis |
| Allocations; Leaks; Game Memory | Heap ownership and application/GPU footprint |
| Animation Hitches; SwiftUI; App Launch | Frame pacing, view updates and startup |
| System Trace; Swift Concurrency | Scheduling, waits, actors and tasks |
| File Activity; Data Persistence | Filesystem/storage and SwiftData/Core Data |
| Network; Audio System Trace | HTTP/connections and audio deadlines |
| Metal System Trace; Game Performance; Game Performance Overview; RealityKit Trace | Graphics, sustained rendering and spatial workloads |
| Power Profiler; Core AI; Foundation Models; Logging | Power, model execution, agentic requests and event context |

**Blank** is also offered by the GUI, but is not a 26th standard template returned by
`xctrace list templates`. A template is a configured collection of instruments, not another
measurement type. A saved user template is a reusable configuration, not a captured trace.

## Preview, configure, then record

Paths below are examples; substitute an existing private task directory and actual target.
Run from this skill's directory, or use the script's absolute path.

```sh
python3 scripts/capture.py --list
python3 scripts/capture.py cpu --show-options
python3 scripts/capture.py cpu --pid 12345 --seconds 15 --output /private/task/baseline.trace
```

The last command **prints** a shell-quoted command. Add `--run` to record within the user's
authorized scope. The helper checks installed names, requires a selected process or launch
target, rejects existing output paths, preserves xctrace's prompts/exit status, and does not
append runs, use a shell or choose all processes. It does not guarantee device capability.

```sh
python3 scripts/capture.py cpu --pid 12345 --seconds 15 \
  --output /private/task/baseline.trace --run

python3 scripts/capture.py launch --launch /path/to/App.app --seconds 15 \
  --output /private/task/launch.trace --run

python3 scripts/capture.py concurrency --instrument 'GCD Performance' --show-options
python3 scripts/capture.py ml --template 'Time Profiler' --instrument 'Core ML' --show-options
python3 scripts/capture.py gpu --instrument 'SceneKit Application' --show-options
```

Pass launch arguments after `--`; pass `--device '<actual-name-or-UDID>'` for a selected
device. The local existence check for `--launch` is for host executables/apps; for remote
launch use the actual installed xctrace/device workflow after inspecting help, or install
and launch with devicectl and attach to the resulting PID for **steady-state** measurement.
Do not call attach-after-launch a startup capture.

Xcode 27 supports `--show-recording-options` without starting a recording. Instruments
with no configurable options are omitted from the returned JSON. Save and edit only the
specific option discovered on this toolchain, then pass `--recording-options file.json`.
For example, SwiftUI exposes `enableLayoutTracing`; Time Profiler exposes sampling/waiting
options. Do not copy a complete options object blindly across Xcode versions or enable
all diagnostic modes. Older Xcodes may require the GUI for configuration.

## Read the result

Record command exit status **and** inspect the resulting run's end reason, target, duration,
symbols and populated tracks. A usable trace may accompany an unsuccessful process/command;
that is partial evidence, not a clean pass. A zero exit status with empty relevant data is
also insufficient. Preserve the actual status and do not automatically retry an ambiguous run.

```sh
xcrun xctrace export --input /private/task/baseline.trace --toc \
  --output /private/task/toc.xml
xcrun xctrace export --input /private/task/baseline.trace \
  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="time-profile"]' \
  --output /private/task/samples.xml
```

The XPath is an example **only when that table appears in the actual TOC**. Parse XML with
an XML parser resolving `id`/`ref`, and verify units. Instrument names and private package
schema descriptions are not a stable export API. Missing/unexportable tables stay partial;
use the GUI for analysis when needed. `--har` can export HTTP data with the same privacy
requirements as the trace. Check installed help before using release-note-only flags.

## Make a native user template

For a usable baseline library matching the 17 recipe names, run:

```sh
python3 scripts/install_templates.py
python3 scripts/install_templates.py --install
xcrun xctrace list templates
```

The first command previews; the second creates `perf-apple-<mode>.tracetemplate` **symlinks**
in the user's Instruments Templates directory to the selected Xcode's Apple templates.
No Apple archives are copied or patched, and conflicting existing user templates are left
unchanged. Close/reopen the template chooser to refresh its User tab. These are named
baseline presets with Apple's default composition and descriptions, not customized instrument
sets or settings. Keep the skill's matching recipe/catalog alongside them. After moving or
upgrading Xcode, inspect stale links and deliberately recreate them for the selected version;
do not silently overwrite user-customized templates.

To customize a baseline for a repeatable workload:

1. Open Instruments for the selected Xcode; create a new document from the recipe's standard
   template (or Blank). Choose an explicit target for recording, without starting it yet.
2. Add only the relevant optional instruments through **+ Instrument**. Inspect Next Recording
   options; retain ordinary sampling and add expensive diagnostics only for the current question.
3. Choose **File → Save As Template…**. Use a distinct name such as
   `perf-apple-<mode>-<workload>.tracetemplate` (never overwrite a baseline symlink), and put
   the owning skill/mode, intended workload and required hardware in its description.
4. Save in the user Templates folder, normally `~/Library/Application Support/Instruments/Templates/`.
   Reopen through the **User** chooser and verify its instruments/settings. Confirm no unintended
   target, executable path, environment or sensitive content is carried into a shared artifact.
5. Exercise a representative workload; on unavailable hardware mark the template configuration
   inspected, with recording validation pending. Keep the native file tied to its Xcode version.

Xcode 27 can import an externally opened `.tracetemplate` into the User folder. Its binary
archive format is not a public authoring API: do not construct or patch archives by guessing
internal keys. The CLI recipes remain usable if native saving is unavailable. A custom
**instrument package** is different: it defines domain data/modelers, not just selected tracks.
Use [Creating Custom Instruments](https://developer.apple.com/videos/play/wwdc2018/410/) and
[Modeling in Custom Instruments](https://developer.apple.com/videos/play/wwdc2019/421/) only
when repeated domain analysis justifies that additional maintenance.

## UI automation and real devices

For a reusable benchmark or CI gate, follow [performance regression testing](regression-testing.md)
for fixture boundaries, device isolation, build/result identity, baselines and noise handling.

Use XCUITest for repeatable user interactions and assertions. Build a stable fixture, launch
arguments and accessibility identifiers; wait on observable readiness rather than fixed sleeps.
Run the same navigation/scroll/teardown sequence before and after a change. Inspect the
installed `xcodebuild -help` and actual destinations, then use `test` or build-for-testing /
test-without-building with a unique `.xcresult` path. Use XCTest metrics suited to the claim:
clock/CPU/memory, launch, signposts or hitch metrics. Check API availability on the deployment
target. Swift Testing does not replace XCTest's UI/performance facilities.

For result extraction inspect `xcrun xcresulttool get test-results metrics --help`; schema and
test selectors vary. Keep failure attachments until triage is complete. One successful UI run
does not establish stable performance: compare repeated distributions under matched conditions.

For a physical device, check Developer Mode, pairing, signing and accessibility of the selected
device through Xcode/`devicectl`. Use `xcrun devicectl help` and its JSON output options instead
of parsing human output. Never erase an existing simulator or restart unrelated apps to get a
profile. Simulator automation is useful for behavior; qualify CPU/GPU/memory/energy on devices.

RocketSim's CLI can inspect accessibility, take screenshots, issue gestures, wait for state,
and inspect/control simulator networking. Discover its actual `help`, `status` and target
selection. Treat it as simulator tooling, not proof that a physical device was exercised.
Restore any network conditions changed for the test.

## Finish the session

Follow [the skill's cleanup rules](../SKILL.md#finish-and-clean-up): retain concise measurements,
commands and limitations, stop owned profilers/helpers, close captures, delete exact task-owned
traces/exports/probe builds/isolated caches, and restore settings. The helper deliberately does
**not** auto-delete a capture before analysis or erase shared caches. Keep the recipe and any
intentionally delivered native template; these are reusable artifacts, not temporary captures.
