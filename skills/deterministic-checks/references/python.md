# Python

Use the project's interpreter, resolved environment and configured formatter/type checker.
Do not run dependency resolution/build hooks from an unknown project merely to audit it.

- Existing Ruff/Black formatting checks and selected Ruff/Flake8/Pylint checks for undefined
  names, unused imports, exception mistakes, mutable defaults and actual correctness risks.
  Ruff `ALL` is not a measured adoption plan; formatting rules can conflict.
- One configured type checker (for example mypy, Pyright or ty) with the right package roots,
  stubs and supported Python version. Review ignored imports, untyped functions and suppressions
  before describing coverage. Ruff is not a substitute for type checking.
- Existing Bandit/Semgrep or focused security rules for unsafe deserialization, shell/query
  construction and relevant trust boundaries. Source matches need context; a type annotation
  is not validation or escaping.
- Schema/config tests and generated-output checks for the actual runtime contract; an import
  or syntax compilation does not validate data shapes or optional dependencies.
- Resolved dependency audit using the existing owner. Preserve environment markers/extras and
  advisory freshness; unknown versions or unsupported lockfiles remain coverage gaps.
- When relevant, targeted runtime development/asyncio/resource warnings for unawaited work,
  unclosed resources and event-loop misuse. Configure warning behavior deliberately and
  exercise the code; a silent import does not establish resource correctness.

Ruff currently has no third-party plugin API. For a genuinely project-specific rule, use
the existing framework's extension point, a focused Python AST/LibCST check or reviewed
Semgrep rule. AST shape alone does not resolve every import/type or interprocedural path.
Test one realistic bad case and plausible safe alternative before adding a CI gate.

Primary source, checked 2026-11-15: [Ruff FAQ, type-checker distinctions and plugin limits](https://docs.astral.sh/ruff/faq/).
Check the project's chosen type checker/security tool documentation for version-specific
flags; do not migrate the environment under a routine check request.
