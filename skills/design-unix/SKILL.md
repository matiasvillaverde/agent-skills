---
name: design-unix
description: Design or review composable tools, CLIs and libraries using coherent responsibilities, predictable interfaces and Unix stream conventions.
license: MIT
---

# Unix design

Use Unix principles as design questions. Preserve the project's supported platforms,
established interfaces and product experience.

- Give each component one coherent responsibility that it handles completely.
  Splitting it into thin layers or separate processes is not automatically simpler.
- Separate reusable mechanism from policy when actual callers need different policy.
  Keep useful defaults; do not expose configuration for every internal choice.
- Make components compose through a small, documented contract. An in-process typed
  interface is often sufficient. Text, JSON, binary formats and schemas each have
  valid uses; choose for the actual consumers, scale and compatibility needs.
- Prefer existing conventions over new options and parallel configuration systems.
  Keep precedence explicit and diagnostics useful without exposing secret values.
- Keep public interfaces small. Do not add plugin discovery or extension hooks before
  a real use case justifies their lifecycle, versioning and trust obligations.

## CLI boundaries

For commands intended to compose, put requested data on stdout and diagnostics on
stderr. Preserve documented exit codes. Provide a stable machine-readable format
when scripts or agents need structured output; human formatting may remain separate.
Handle stdin, file arguments and the `--` separator according to the command's contract.

Do not prompt when the command cannot receive interactive input. Return an actionable
error or use an already supplied noninteractive option. Respect terminal detection,
existing color conventions and cancellation. Bounded shutdown should release owned
resources and report incomplete work truthfully.

Keep routine success quiet when the caller can already infer it. User-facing apps
still need useful progress and outcome feedback. Logs should help answer operational
questions; do not flood pipes or emit routine status at every layer.

## Check composition

Test the actual promised usage: a pipe, structured output parsing, error exit status,
cancellation or configuration precedence when changed. Check compatibility with real
callers. Do not add a generic CLI framework or a universal test matrix for a small tool.
