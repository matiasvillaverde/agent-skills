# Static and native analysis

Discover the project's checks before choosing another tool. Language parsing, rule
coverage and interprocedural analysis are separate capabilities. Check the installed
engine and actual syntax; product marketing support does not prove this invocation
analyzed every path. Review generated/vendor exclusions and source-selection changes.

## Local SAST

For an existing Semgrep installation and reviewed local rules, this shape was exercised
with 1.184.0 on synthetic Python fixtures. Establish absolute paths and private output
outside the target first:

```sh
semgrep scan --config "$security_rules" --metrics=off --disable-version-check \
  --oss-only --strict --error --json --output "$security_report_dir/sast.json" \
  "$security_source" >"$security_report_dir/sast.log" 2>&1
```

Capture status immediately. The fixture returned 1 for a finding, 0 for a checked safe
case, and 7 for missing rules. Also inspect errors and scanned-file counts. These flags
are not an OS network sandbox. Local reviewed rules avoid implicit registry selection;
inspect configuration/environment before making stronger privacy guarantees. Never use
a URL as an output destination accidentally. Raw reports may contain source excerpts.

Semgrep CE and commercial engines differ. Current documentation lists Swift and Rust
among community-supported languages; verify the installed parser/rules rather than
assuming native-language or cross-file coverage. Generic matching does not provide a
Zig or CUDA semantic analyzer. Rule severity alone does not establish product impact.

Use existing CodeQL workflows when available and appropriate. Confirm supported languages,
build/extraction mode, query pack revision and licensing; compiled-language database
creation may execute the build. No implicit hosted workflow or all-language claim.

## Select native checks against a concrete risk

| Stack | Useful evidence | Limits to state |
| --- | --- | --- |
| Swift/iOS/macOS | Existing compiler concurrency checks, Xcode sanitizers, focused XCTest/Swift Testing and supported device tests | Simulator success does not prove entitlements, Keychain sharing, device-only paths or production transport policy. Select compatible sanitizer/device configurations. |
| Go | Existing vet/static checks, `go test -race` for exercised concurrency, bounded native fuzzing | Race detection needs executed paths and a supported target; absence of reports is not absence of races. |
| Rust | Compiler/Clippy; targeted Miri or sanitizer checks where supported; bounded parser fuzzing | Safe Rust does not prevent logic/auth flaws. FFI, unsafe blocks and platform features need focused coverage; don't assume Miri runs arbitrary OS/FFI workloads. |
| Python/TypeScript | Existing SAST plus integration tests for permission/data boundaries; applicable type/lint checks | Types do not enforce runtime trust. Analyze request-to-sink flow and actual escaping/query APIs. |
| C/C++ | Existing Clang static analysis; ASan/UBSan, supported race checks and bounded fuzzing | Instrumented builds have runtime/coverage limitations and are not production hardening by themselves. |
| Zig | Runtime safety in appropriate build modes, allocator/leak checks, focused parser tests | ReleaseFast/ReleaseSmall can differ; explicitly compare deployed mode and foreign-library behavior. |
| CUDA | Compute Sanitizer memcheck/racecheck/initcheck/synccheck as relevant | Tool findings concern exercised device behavior, not authentication, dependency advisories or all possible schedules. |

Use current platform guidance and owning build commands; this table does not authorize
installing every tool or adding every check. Keep expensive analyses targeted or scheduled
where the CI owner allows, while retaining required release qualification.

Primary references: [Semgrep CLI](https://docs.semgrep.dev/cli-reference),
[CE language support](https://docs.semgrep.dev/semgrep-ce-languages),
[CodeQL language support](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/),
[Clang ASan](https://clang.llvm.org/docs/AddressSanitizer.html),
[Go race detector](https://go.dev/doc/articles/race_detector),
[Miri](https://github.com/rust-lang/miri),
[Zig runtime safety](https://ziglang.org/documentation/0.15.2/#Illegal-Behavior),
[Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html).
Match these to the target's actual versions; not every linked manual was read end to end.
