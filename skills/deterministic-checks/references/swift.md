# Swift and Apple targets

Use the project's Xcode/Swift version, actual schemes/destinations, SDKs, deployment targets,
compiler flags and source-generation order. `swiftc -typecheck` on a snippet cannot replace
the application build, asset compilation, extensions or conditional target branches.

Useful checks to choose according to the changed risk:

- Existing formatter check mode and selected SwiftLint correctness rules. Read nested
  configs, include/exclude paths, baseline and exit behavior. File discovery must include
  new files; a successful helper with no selected files proves nothing.
- Build/typecheck for signatures, exhaustive switches, availability, generics and actor
  isolation. Verify the actual Swift language/concurrency mode; adding `Sendable` labels
  or running a newer compiler does not prove complete data-race checking is enabled.
- SwiftLint analyzer rules where supported, using the real compiler log/context. Syntax-only
  `lint` and compiler-backed `analyze` are different operations.
- Existing localization/catalog generation, asset/resource names, plist/entitlement schema,
  package resource/bundle checks and reproducible generated sources where these own contracts.
  Do not invent generic regex lint for localizable presentation already covered by an AST gate.
- API/ABI or public-interface checks only for an actual compatibility promise. A package's
  supported consumer toolchains matter more than making every warning in the newest compiler fatal.
- Focused ASan/TSan or runtime exclusivity checks for unsafe/FFI/concurrent code, on supported
  schemes and destinations. TSan coverage depends on execution and supported device/simulator
  combinations; availability is not identical across Apple targets.

Use the project's warning policy. Avoid global autocorrect, force-unwrap bans detached from
context or enabling every style rule. Treat warnings from generated/vendor code at their
owner rather than modifying third-party source indiscriminately.

For a custom rule, distinguish spelling from syntax and type identity. SwiftSyntax can
inspect structure; symbol/type/actor facts may need compiler information. Test aliases,
closures and lookalike APIs only where they affect the invariant. Preserve parse failures.

Primary sources: [Swift migration/concurrency guide](https://www.swift.org/migration/documentation/migrationguide/),
[SwiftLint](https://github.com/realm/SwiftLint),
[Apple runtime issues](https://developer.apple.com/documentation/xcode/diagnosing-memory-thread-and-crash-issues-early).
Check installed help/SDK for exact commands and availability; these links are not an
instruction to upgrade or enable unsupported modes.
