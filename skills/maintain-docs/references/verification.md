# Verify the claim, not only the page

| Claim | Evidence to inspect |
| --- | --- |
| CLI flag/default/exit behavior | Actual supported binary help plus parser/config and a safe invocation |
| API request/response | Owned schema, handler and representative contract/runtime check |
| Setup or recovery | Prerequisites and an isolated permitted rehearsal; mark unrehearsed steps |
| Deployed capability | Deployment/config evidence, not a merged commit alone |
| Generated reference | Generator inputs and repeatable output; fix source before generated file |
| Performance/security guarantee | Matching measurements or security evidence, with limits |

Find affected guidance by concepts, routes and user-visible names, not only code symbols
or commit categories. Dependency, CI or infrastructure changes can alter supported setup.
Internal comments, code spans, examples and external URLs are not automatically repository
paths. Resolve relative links against their document location; check fragments using the
actual renderer's heading rules. Preserve redirects that are intentional.

Prefer existing doc commands in check mode. Inspect scripts/config before running and
capture the producer's real exit status; piping a failing command through `tail` or `tee`
can hide failure. Missing tool, zero examples or excluded paths are explicit coverage gaps.
Doctest and similar runners execute code; inspect I/O, network and credentials first.
Exact-output examples can depend on versions, time, ordering or locale. Separate a
stable semantic assertion from intentionally illustrative output.
[Python doctest](https://docs.python.org/3/library/doctest.html).

Select checks by the changed claim rather than running every documentation tool:

- Rendered navigation and local references: the existing docs build/link checker, including
  anchors and generated pages. Inspect actual changed output where layout affects usability.
- API comments: the owning DocC/rustdoc/Go/TypeDoc/Sphinx/Doxygen/Zig documentation workflow,
  supported by the installed version. A formatter alone does not verify rendered contracts.
- Executable examples: an existing focused example/doctest target in an isolated environment.
  Check examples were actually discovered; compilation alone does not verify asserted output.
- Prose consistency: existing terminology/spelling rules where they catch real ambiguity.
  Scope them to prose and provide deliberate exceptions for code, identifiers, legal text and
  quotations. [Vale scopes](https://docs.vale.sh/topics/scopes) are one implementation; check
  version support instead of treating every Markdown byte as prose or adding a tool by default.
- Operational use: a permitted rehearsal and observable outcome, or a recorded coverage gap.
  A dry-run parser check does not validate actual rollback, credentials or deployed behavior.

External link checks should distinguish inaccessible/authenticated/rate-limited resources
from confirmed removal. HEAD may be unsupported while GET works. Keep requests bounded;
do not leak private URL query strings or credentials to public checkers. For an unavailable
authority, record what could not be verified and retain an honest source link.

Prevent recurrence only where a stable deterministic check earns its upkeep: generated
schema/reference drift, checked CLI examples, local navigation or structured configuration.
Avoid enforcing prose word counts, identical headings everywhere or a new docs framework
for one edit. Documentation can serve tutorial, how-to, reference or explanation needs
without creating four pages for every feature. [Diátaxis](https://diataxis.fr/).

For reader testing, give a concrete task and the normal entrypoint, not the expected answer.
Have the reader identify prerequisites, perform only permitted steps, interpret results and
find the failure/escalation route. Fix missing context revealed by the attempt. Do not turn
every small typo fix into a multi-agent test or accept an unexecuted command as a passing runbook.
