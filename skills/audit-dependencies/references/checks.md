# Selecting dependency checks

Use installed, owner-approved tools and their current help. These are candidate entry
points, not commands to run indiscriminately. Record tool/database versions, selected
targets, extracted components, exclusions and actual exit semantics. Keep reports private;
even package names, private registry URLs and source paths can disclose information.

| Stack | Candidate | Coverage questions |
| --- | --- | --- |
| Rust | `cargo audit`; existing `cargo deny check` | Which Cargo.lock/features/targets ship? Separate advisory evidence from license, duplicate and source policy. Include build scripts/proc macros and vendored native libraries. |
| Go | `govulncheck ./...` | Which tags, GOOS/GOARCH and analysis mode? Compare deployed binary/module metadata; dynamic behavior and unbuilt targets can remain unknown. |
| TypeScript/JavaScript | Existing npm/pnpm/yarn audit or supported OSV lockfile scan | Which registry, workspace lock and installed/build artifact? Check both runtime and build dependencies. Do not send private metadata to an unapproved registry. |
| Python | `pip-audit` on an existing environment or supported resolved input; supported OSV lockfile | Resolution can execute package tooling. Avoid implicit installs/repair; inspect environment markers and native/shared-library coverage. |
| Swift/Apple | Package.resolved, Podfile.lock, Cartfile.resolved, binary frameworks and exact upstream/OSV/GHSA research | Verify extractor support instead of assuming every Swift package is scanned. Match canonical repository identity, binary SDK and deployed OS versions. |
| C/C++, Zig | Supported package/commit/SBOM scan plus vendor advisories | Include static/vendored libraries, compiler and build scripts. Conan or commit support does not imply every vcpkg/Zig manifest or custom archive is covered. |
| CUDA | Library/image inventory plus NVIDIA advisories | Match driver, toolkit, library, platform and branch independently. Compute Sanitizer diagnoses execution defects; it is not a CVE database. |
| Containers/OS | Existing Trivy/OSV image or SBOM workflow | Match an immutable artifact and OS distribution; check bundled language packages, vendored files and inventory omissions. Do not pull/run a production image implicitly. |

OSV-Scanner v2 supports explicit lockfiles, for example:

```sh
osv-scanner scan source --lockfile="$audit_lockfile"
```

Use the owning runner to capture status/output privately. Compare its extracted inventory
with the expected one. Recursive discovery respects ignore behavior; verify scope rather
than assuming every nested package was included. Offline databases need a recorded refresh
date and explicit freshness assessment. Version 1 and version 2 command syntax differs.

An image scan and a source-lock scan answer different questions. Trivy uses distribution
advisories for distribution packages, which matters for backported fixes. Keep runtime and
build-stage exposure distinct; a missing package in the final image can still have executed
during a credentialed build. Don't promote a source SBOM into proof of deployed contents.

Primary references:
- [OSV source scanning](https://google.github.io/osv-scanner/usage/scan-source) and [supported artifacts](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/)
- [Trivy vulnerability matching](https://trivy.dev/docs/latest/scanner/vulnerability/)
- [RustSec](https://rustsec.org/) and [cargo-deny](https://embarkstudios.github.io/cargo-deny/)
- [Go vulnerability tooling](https://go.dev/doc/security/vuln/)
- [pip-audit security model](https://github.com/pypa/pip-audit#security-model)

Reviewed 2026-11-14. This reference does not claim every listed tool or ecosystem was
executed during skill authoring. Refresh support tables for the actual installed version.
