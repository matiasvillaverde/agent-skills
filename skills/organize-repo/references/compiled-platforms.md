# Compiled platforms and their path contracts

Read only the relevant platform. Resolve defaults against the repository's pinned toolchain,
actual manifests and owning check commands. None of these ecosystems requires the same tree.

## Swift, Xcode and Tuist

`Package.swift` owns SwiftPM targets, products and dependencies. Conventional target directories
under `Sources`/`Tests` can be overridden by target `path`, `sources` and `exclude`; inspect the
resolved target inventory before moving files. Preserve tools-version compatibility and public
module names. [Manifest API](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html).
[SwiftPM discovery examples](https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/CreatingSwiftPackage.md).

Resources are target-scoped. A `Resources/` folder is optional; `.process` and `.copy` have
different flattening/preservation behavior. Preserve asset/localization names and package data
declarations; verify representative resources through `Bundle.module`, not guessed bundle paths.
[Apple package resources](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package).
DocC catalogs belong alongside their target's sources; moving every Markdown-related asset to
root `docs/` can break discovery. Verify documentation builds when catalogs move.
[DocC placement](https://www.swift.org/documentation/docc/documenting-a-swift-framework-or-package),
[Apple documentation](https://developer.apple.com/documentation/xcode/documenting-apps-frameworks-and-packages).

An Xcode navigator group can be logical or folder-backed; moving a group is not necessarily a
disk move. Folder synchronization, file references, build phases and target membership matter.
Preserve schemes, Info.plist/entitlement paths, assets and supported destinations. Buildable
folders are version-sensitive; do not convert project format merely to tidy the tree.
[Apple file management](https://developer.apple.com/documentation/xcode/managing-files-and-folders-in-your-xcode-project).

For generated projects, edit generator inputs. Tuist manifests/helpers, globs or buildable
folders determine membership; its example `Projects/App` hierarchy is optional. Update inputs,
regenerate when required by the pinned toolchain, compare target/resource membership and run
the owning build/test commands. Do not hand-maintain generated `.xcodeproj` changes.
[Tuist structure](https://tuist.dev/en/docs/guides/features/projects/directory-structure),
[Tuist project guidance](https://tuist.dev/en/docs/guides/features/projects/best-practices).

## Rust and Cargo

Cargo discovers conventional `src/lib.rs`, `src/main.rs`, binaries, examples, integration tests
and benches; manifest target `path` and auto-discovery settings can override them. Rust module
declarations separately determine the logical module tree. `foo.rs` and `foo/mod.rs` are valid
alternatives, not grounds for a wholesale style conversion. Preserve public module paths.
[Cargo layout](https://doc.rust-lang.org/cargo/guide/project-layout.html),
[module loading](https://doc.rust-lang.org/reference/items/modules.html).

Each `tests/*.rs` file normally becomes an integration crate. Moving unit tests there changes
visibility; flattening `tests/common/mod.rs` can create an unintended test target. Compare
Cargo metadata and intended test cases, including relevant features and doctests.
[Cargo targets](https://doc.rust-lang.org/cargo/reference/cargo-targets.html).

Update workspace members/path dependencies, target paths, package include/exclude lists and
embedded inputs. `include_str!` resolves relative to its source file. `build.rs` normally runs
from the package root and writes into `OUT_DIR`; moved inputs need correct rebuild tracking.
Check fresh output when stale generation could mask a failure, and package contents if shipped.
[Include paths](https://doc.rust-lang.org/std/macro.include_str.html),
[build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html),
[manifest](https://doc.rust-lang.org/cargo/reference/manifest.html).

## Go

A package directory contributes to its import path. `cmd/` is optional, `pkg/` has no special
visibility, and a small root package is legitimate. `internal` restricts imports by the path
prefix above it; moving that boundary can change who may import a package. Adding `go.mod`
creates a module boundary, not just a folder. [Official layout guidance](https://go.dev/doc/modules/layout),
[Go command rules](https://pkg.go.dev/cmd/go).

Preserve `_test.go`, build tags, OS/architecture suffixes, generated inputs and `testdata`.
`//go:embed` is package-relative, cannot use `..` or cross module boundaries, and must still
match the intended payload after a move. API/package documentation belongs with its source.
[Embedding](https://pkg.go.dev/embed), [documentation comments](https://go.dev/doc/comment).
List and test each affected module with its supported tags; one parent `go test ./...` does
not cover nested modules. Check fixture behavior from the test runner's actual working directory.

## Zig

Read the exact compiler version's documentation. `build.zig` constructs a graph and selects
`root_source_file`; `src/` is a convention, not compulsory. Update module roots/imports, generated
inputs and install edges together. `build.zig.zon` package paths determine included content.
Do not assume a minimum-version field actually selects the compiler.
[Build-system guide](https://ziglang.org/learn/build-system/),
[versioned package metadata example](https://github.com/ziglang/zig/blob/0.15.2/doc/build.zig.zon.md).

Relative `@import` and `@embedFile` paths and test declaration discovery can change after a move.
A file under `tests/` does not automatically execute. Compare discovered cases and run the
declared build/test/install steps for supported targets. The following is a versioned reference,
not a request to change versions: [Zig 0.15.2 reference](https://ziglang.org/documentation/0.15.2/).

## C, C++ and CUDA

Identify the actual build system; CMake guidance does not automatically apply to Bazel, Meson
or Make-only projects. In CMake, target sources, subdirectory traversal, include/file-set bases
and install/export rules are authoritative. `src/`, `include/` and `tests/` are optional names.
Preserve public header spellings and consumer requirements. Use the existing presets/toolchain
and a separate build directory; do not replace explicit sources with broad recursive globs.
[Source/build trees](https://cmake.org/cmake/help/latest/manual/cmake.1.html),
[target sources](https://cmake.org/cmake/help/latest/command/target_sources.html),
[include interfaces](https://cmake.org/cmake/help/latest/command/target_include_directories.html).

Trace generated headers, copied resources and test working directories. CTest needs registration;
putting code in `tests/` does not register a test. Configure/build, compare registered cases and
execute relevant tests; verify a staged install or consumer build when public packaging changes.
[CMake tests](https://cmake.org/cmake/help/latest/command/add_test.html),
[configured files](https://cmake.org/cmake/help/latest/command/configure_file.html).

For CUDA, retain `.cu` language treatment, supported Toolkit/host compiler, architecture targets
and device-link behavior. Splitting device code across files can require separate compilation;
do not enable it universally. Build/link the actual target and run the existing GPU smoke case
when hardware is available; distinguish compile-only evidence from runtime qualification.
[NVIDIA compiler guide](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/),
[CMake separate compilation](https://cmake.org/cmake/help/latest/prop_tgt/CUDA_SEPARABLE_COMPILATION.html).
