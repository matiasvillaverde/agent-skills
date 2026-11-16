# Match Zig's compiler, build and profiler

## Resolve the actual version

Use the repository pin and selected compiler, not a tutorial's version. Inspect `zig version`,
`zig env` and the installed command help. Read matching stdlib source under the discovered library
directory; do not infer API existence from an empty documentation shell. Consult the current
[official download page](https://ziglang.org/download/) only to establish releases, not to upgrade
the project. Zig's current source is on Codeberg; the older GitHub release list can be stale.

At research time, stable 0.17.1 used canonical `debug`, `safe`, `fast`, `small` optimization names;
older projects use names such as `ReleaseSafe`. Exact 0.17.1 parser source still accepts some
legacy strings, but enum/API migration is separate. Do not mechanically rename a pinned build.
`safe` is optimized with safety checks; `fast`/`small` disable them. Preserve the product's mode
and semantics in performance comparisons.

For 0.17.1, these compiler forms were verified in tagged source, not executed locally:

```sh
zig build-exe --help
zig build-exe fixture.zig -O safe -fno-strip -femit-asm=fixture.s
```

That second command is for a standalone diagnostic fixture, not a substitute for the project's
build. `zig build -Doptimize=safe` requires a build script exposing that option. `-fllvm` /
`-fno-llvm`, `-fno-omit-frame-pointer`, `-funwind-tables` (synchronous),
`-fasync-unwind-tables`, and `-femit-llvm-ir` have compiler-specific meanings and target/backend
requirements. Apply only the chosen diagnostic settings through the existing build. Do not
invent equivalent `-D...` flags. `--time-report` in this release requires `--listen`; it is not
a general standalone runtime timer.

## Symbols, backend and code generation

Verify symbol/unwind quality using a known hot path. Keep the binary and matching debug artifacts
with the capture while investigating. Do not assume every optimized build strips symbols or
omits frame pointers: 0.17.1 defaults vary by optimize mode and target. Frame-pointer forcing
or asynchronous unwind tables may help a particular collector but can change code; record this.

Backend selection matters. Check what the target/mode actually selected rather than assuming
all Zig compilation uses LLVM. The tagged 0.17.1 configuration generally prefers LLVM outside
debug where supported. That version deliberately disables LLVM loop vectorization while retaining
other mechanisms such as SLP. Explicit vectors, SLP and loop vectorization are not interchangeable.
Read release notes and the relevant backend source before calling missing vectorization a source
bug; do not turn off a compiler correctness workaround as an optimization.

Inspect the real hot caller and emitted assembly for branches, loads, bounds checks, copies,
instruction selection and spills. Emitting LLVM IR requires the LLVM path. Preserve target CPU
and feature settings; a host-native target is not automatically safe for distributed artifacts.
Compile-time computation and inline specialization can remove work or increase code size, so
inspect code and measure the intended runtime task rather than the prettier source.

## Native captures and optional integrations

An optimized symbolized Zig executable can use the same platform sampling tools as other native
code. On macOS, discover `xcrun xctrace` templates/help and use a bounded Time Profiler/CPU Profiler
capture; on Linux discover `perf` events/unwinding support. Existing samply is another candidate.
Separate samples, wait states, PMU counts, allocator accounting and end-to-end timing.

Use existing Tracy integration if it answers a needed cross-thread/frame/GPU question. Match Zig
binding, native client and viewer versions; README minimum-version claims do not establish actual
compatibility with a newer Zig compiler. Do not add Tracy to every program. Current platform
sampling support differs from older blog posts and from manually emitted zones.

For zBench, testingx or another harness already used by the project, inspect the pinned manifest
and timing/counter implementation. Check warmup, hooks, timer units/resolution, output sinks,
allocation observation and automatic optimize mode. A default fast build may violate the target
comparison. A minimum supported version is not a successful build/test on the selected compiler.
Keep custom-allocator instrumentation separate from shipping-allocator timings.

Sources: [0.17.1 compiler help/parser](https://codeberg.org/ziglang/zig/src/tag/0.17.1/src/main.zig),
[optimization enum/parser](https://codeberg.org/ziglang/zig/src/tag/0.17.1/lib/std/lang.zig),
[compiler configuration](https://codeberg.org/ziglang/zig/src/tag/0.17.1/src/Compilation/Config.zig),
[module defaults](https://codeberg.org/ziglang/zig/src/tag/0.17.1/src/Module.zig),
[LLVM pipeline](https://codeberg.org/ziglang/zig/src/tag/0.17.1/src/zig_llvm.cpp),
[0.17 release notes](https://ziglang.org/download/0.17.0/release-notes.html),
[samply](https://github.com/mstange/samply), [Tracy](https://github.com/wolfpld/tracy).
