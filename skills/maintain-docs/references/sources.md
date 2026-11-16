# Research basis

Reviewed 2026-11-15; original synthesis with no copied community prompt/code.

- [sync-documentation](https://github.com/tomzx/agents/blob/31f0fc756d0bbeddde013a51985880c24139f7a8/skills/sync-documentation/SKILL.md) (MIT): useful implementation/CLI/config reconciliation. Excluded universal path interpretation, HEAD-only broken-link judgments, mandatory tool installs and pipelines that can conceal producer failures.
- [Paperclip doc-maintenance](https://github.com/paperclipai/paperclip/blob/3244780bd03294c860e8cedea3bf8ea29e03cd1f/.agents/skills/doc-maintenance/SKILL.md) (MIT): factual minimal patches. Excluded mandatory cursor files, commit/push workflows and keyword classifications that disregard CI/dependency changes.
- Primary Diátaxis and Python doctest documentation are linked in the verification guide. Their scope does not establish that a product is implemented, deployed or correctly documented.

## Writing, operations and instructions expansion

The following original SKILL.md bodies were read on 2026-11-15. They informed decisions;
their prompts, scripts and templates were not imported or executed.

- [alexei-led/documenting-code](https://github.com/alexei-led/cc-thingz/blob/de984fb5ae485b4615da09128f1bf62f5b3a07e8/src/skills/documenting-code/SKILL.md), MIT license read at that revision: useful reader/task distinction and contracts rather than comment narration. Excluded mandatory bundled tooling, blanket historical-content deletion and treating current code as superior to accepted requirements.
- [Anthropic doc-coauthoring](https://github.com/anthropics/skills/blob/00756142ab04c82a447693cf373c4e0c554d1005/skills/doc-coauthoring/SKILL.md): useful fresh-reader testing. Excluded prescribed question counts, repeated stage approvals and section brainstorming for ordinary repository edits. No applicable license was resolved in the inspected root/skill paths at this revision; no content copied.
- [BjornMelin repo-docs-align](https://github.com/BjornMelin/dev-skills/blob/40370419f9a7d8272a6f755ed78106b9badcc882/skills/repo-docs-align/SKILL.md): useful authority-chain and affected-surface discovery. Excluded universal repository-wide expansion, scoring targets, automatic artifact directories and model-routing policy. Its README directs readers to per-skill licenses, but none was present in the inspected skill directory; no content copied.
- [Canonical documentation-diataxis](https://github.com/canonical/workshop/blob/1922a331f10aca7194492dc5c1cbf4ed067bef58/.github/skills/documentation-diataxis/SKILL.md): useful intended-reader versus actual-content review. Excluded compulsory single-quadrant classification for every page. A root license was not found at this revision; no content copied.

[Writing guidance](writing.md) links primary language documentation, Google technical writing,
Google SRE and AWS runbooks. [Instruction guidance](agent-instructions.md) links client/format
documentation and the versioned CTXbench paper; [verification](verification.md) covers proportional
checks. These sources support specific practices, not an automatic quality rating or universal
page/line count. The research record distinguishes the new review from the retained earlier
Paperclip provenance; current revisions may differ.
