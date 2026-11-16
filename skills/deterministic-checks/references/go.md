# Go

Use the module/workspace's declared Go toolchain, build tags, CGO setting and target. Inspect
`go generate`, build scripts and test setup before execution; generated code has an owner.

- Formatting: check `gofmt` differences using the existing wrapper. `gofmt -l` prints names
  but does not itself fail just because a file needs formatting; verify wrapper behavior.
- Compile/build the real affected packages/tags. `go vet` adds checks such as printf argument
  mismatches, copylocks and lost cancellation; compilation alone does not cover all of these.
- Use selected Staticcheck/golangci-lint analyzers already owned by the project. Useful
  resource/error checks include ignored errors, unclosed response bodies/rows and lost
  context, when their actual API patterns are supported. Do not run the same analyzer twice
  through different wrappers or accept a default pack as proof every desired rule is active.
- Inspect golangci-lint's installed major version: v2 config and formatter commands differ
  from v1. Validate the config and read effective enabled linters/exclusions before relying
  on a passing run. Generated/test exclusions must match the product's intended coverage.
- Use `govulncheck` for known vulnerable dependencies/functions in the supported build
  context. It is different from gosec/source analysis and needs an advisory database.
- Use targeted `go test -race` for changed concurrent paths, subject to platform/CGO support.
  A clean race run covers executed interleavings, not all possible schedules. Keep stress or
  fuzz runs bounded and separate from cheap compile/lint feedback.
- Check existing protobuf/OpenAPI generation, SQL/query/schema contracts and config parsing
  where changed. Preserve machine output/API compatibility tests when the CLI/service owns them.

Custom semantic rules normally belong in `go/analysis` with `analysistest`; use type/package
identity when similarly named functions can be unrelated. Define the bad operation and
safe ownership/cancellation pattern before implementing detection. Error-path fixtures
often add more value than many variable-name variants.

Primary sources: [Go vet](https://pkg.go.dev/cmd/vet),
[golangci-lint configuration](https://golangci-lint.run/docs/configuration/),
[Go vulnerability management](https://go.dev/doc/security/vuln/),
[race detector](https://go.dev/doc/articles/race_detector),
[analysis framework](https://pkg.go.dev/golang.org/x/tools/go/analysis).
Commands depend on the installed toolchain and repository; do not upgrade by default.
