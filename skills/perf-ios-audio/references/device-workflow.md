# Reproduce audio performance on an iPhone

## Select an actual target

Use the project's existing scheme/test plan, app identity and device reservation. Discover
the selected Xcode, tools and capabilities before adapting commands:

```sh
xcodebuild -version
xcrun xctrace version
xcrun xctrace list templates
xcrun xctrace list instruments
xcrun xctrace list devices
xcrun devicectl list devices
xcrun xctrace help record
xcrun xctrace help export
xcrun devicectl help device process launch
```

Inspect the device reality/type and current connection/readiness, not only its familiar name.
A paired remembered phone, Simulator or offline tunnel is not a usable physical-device run.
Keep identifiers private. Do not automatically pair, trust, enable Developer Mode, unlock,
change security or restart a device to overcome an unavailable target.

Record representative optimized build, matching dSYMs, device/OS, content, route, actual
session/rate/buffer configuration, volume, foreground/background and network path. Separate
built-in speaker/wired output, Bluetooth and AirPlay when relevant. USB attachment, charging,
debugger, logging, wireless device transport and competing workloads may alter the experiment.
Use one timed workload per target; report thermal/power conditions and disturbances. A listed
CPU counter or Power Profiler is not proof it works on that phone or measures app energy.

## Capture the cause, then remove profiler overhead

Reuse `perf-apple`'s Audio System Trace recipe and template. A command shape for an existing
selected process is below; replace placeholders with discovered values and a private unique
path. A bounded attach captures an in-app playback action, not initialization that preceded it.

```sh
xcrun xctrace record --template 'Audio System Trace' \
  --device '<selected-device>' --attach '<selected-pid>' \
  --time-limit 15s --output '<task-directory>/audio.trace'
xcrun xctrace export --input '<task-directory>/audio.trace' --toc
```

Inspect command status, intended process/device/time interval, symbols and populated tracks.
Use actual TOC schemas for export; an empty track or unsupported field stays unmeasured.
For app/engine initialization, use the installed launch/capture workflow that includes it.
Launching with devicectl and attaching afterward can miss exactly the cold path being studied.
Choose capture length for the symptom; the example is not a required duration.

| Question | Initial evidence; follow-up only if needed |
| --- | --- |
| Glitch or missed deadline | Audio Client/Server/Statistics with thread states; late start vs execution vs starvation. |
| Decode/convert/DSP CPU | Time Profiler or CPU Profiler; CPU Counters for supported target-specific hypotheses. |
| Priority inversion or helper wait | System Trace/Thread Activity; workgroup/thread membership and actual dependencies. |
| First payload/segment stalls | Network/HTTP Traffic, URLSession metrics and off-thread request/decode events. |
| Buffer retention/allocation churn | Allocations and memory lifecycle; VM activity for faults, not merely VM address inventory. |
| Sustained battery/thermal concern | Supported energy/power evidence plus CPU/wakeups/bytes and route/thermal state. |

The reviewed Power Profiler documentation requires iOS/iPadOS 26 or later and reports zero
overall system power while charging. App-impact values are not comparable across device
models; Xcode pairing can affect sleep. Verify the current tool's conditions before interpreting
zeros or cross-device differences. [Power Profiler](https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler).

Do not collect every instrument together. An Instruments audio warning is a diagnostic lead,
not an invented universal quality threshold. Correlate the relevant cycle and playback content.
System audio work is not all attributable to the app, and HTTP Traffic does not cover every
custom transport. HAR/HTTP traces can contain decrypted media, keys, tokens and personal URLs;
minimize capture, keep it private and redact summaries before sharing.

## Automate a few meaningful journeys

Use XCTest/XCUITest for device performance/UI automation and the existing Swift test harness
for deterministic parser, buffer and state-machine behavior. Keep stable accessibility IDs
and deterministic content; a Play tap or UI status change does not assert audio output.
An XCTest signpost interval measures the defined software interval, not automatic audibility.

Start with the affected cold/warm playback journey and one continuity/lifecycle scenario
that distinguishes the hypothesis. Add only relevant seek/cancel, slow delivery, missing or
malformed segment, interruption/route change, background resume or long-session recovery cases.
Use app fixtures or a controlled local server for deterministic delivery failures and a
separate real-network/device run for radio/CDN behavior. Do not mutate a production CDN or
global network configuration to inject failures. Restore any authorized test settings.

Reuse builds with `xcodebuild build-for-testing` and `test-without-building`, the actual
`.xctestrun`, selected destination and unique `.xcresult`. Disable parallel timing on one
device. Inspect executed tests, skips, failures and individual metric samples, not only an
exit code. See the existing [device regression workflow](../../perf-apple/references/regression-testing.md)
for verified CLI shapes, Release configuration and results extraction; no new runner needed.
RocketSim can help Simulator interaction where installed, but does not turn Simulator timing
into physical iPhone, Bluetooth, radio or acoustic measurements.

Compare paired baseline/candidate runs with the same route, content and state, preserving
bad runs and recording interventions. Run correctness/sanitizers separately from timing.
Validate the test with a known regression or controlled delay when creating a new gate; remove
the injected probe afterward. Reuse existing budgets; do not reset a baseline to make it green.

Retain compact counts, distributions, failure explanations and exact reproduction details.
Remove task-owned captures, network exports, test recordings, DerivedData/result bundles and
isolated caches after triage; preserve required failure evidence and shared artifacts. Stop
only owned tools and restore task-changed settings. No available phone or output rig means
the physical result is unverified, even if compilation and Simulator tests pass.
