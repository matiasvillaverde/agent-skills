# Agent skills

75 practical skills for building, simplifying, testing and improving software with coding agents.
Maintained by [Matias Villaverde](https://github.com/matiasvillaverde), combining original
workflows with attributed adaptations from the community.

The emphasis is on readable code, useful tests, measured performance, quiet observability
and preserving product behavior. Skills inspect the current project and documentation;
they should not impose a new framework or process without a concrete reason.

## Find a skill

Browse the [full catalog](CATALOG.md), or start with:

| Need | Skills |
| --- | --- |
| Simplify finished work | [deslop](skills/deslop/SKILL.md) |
| Investigate and clarify | [deep-research](skills/deep-research/SKILL.md), [clarify](skills/clarify/SKILL.md) |
| Design an interface | [design-directions](skills/design-directions/SKILL.md), [design-system](skills/design-system/SKILL.md), [design-swiftui](skills/design-swiftui/SKILL.md), [design-ui](skills/design-ui/SKILL.md) |
| Find incomplete or broken behavior | [test-behavior](skills/test-behavior/SKILL.md), [test-runtime](skills/test-runtime/SKILL.md), [review-test-evidence](skills/review-test-evidence/SKILL.md) |
| Improve performance | [perf-system](skills/perf-system/SKILL.md), plus the language, platform and database specialists in the catalog |
| Review security | [review-security](skills/review-security/SKILL.md), [scan-secrets](skills/scan-secrets/SKILL.md), [audit-dependencies](skills/audit-dependencies/SKILL.md), [test-security](skills/test-security/SKILL.md) |
| Keep engineering work understandable | [maintain-docs](skills/maintain-docs/SKILL.md), [organize-repo](skills/organize-repo/SKILL.md), [review-conventions](skills/review-conventions/SKILL.md) |
| Choose what to apply next | [skill-menu](skills/skill-menu/SKILL.md) |

## Use

Each `skills/<name>/` directory is a self-contained skill. Read its `SKILL.md` before
installing it. Copy or link the entire directory, including references and license files,
into your agent's supported skill directory. Install the skills relevant to your work;
there is no need to load the whole library.

For example, clone this repository and link one skill for clients that discover
`~/.agents/skills` (including supported Codex and Grok Build versions):

```sh
git clone https://github.com/matiasvillaverde/agent-skills.git
cd agent-skills
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/deslop" "$HOME/.agents/skills/deslop"
```

For Claude Code, use `~/.claude/skills/deslop` as the destination instead. The command
intentionally does not replace an existing installation. Other clients and versions
may use different discovery locations; consult their current documentation.

Invoke the skill by name using your client's skill mechanism. Tool availability,
authentication, model selection, SDKs and real devices remain requirements of the
individual workflow. In particular, the review helper's inherited model defaults may
not be available to your account; use its explicit model option when appropriate.
Installing a skill does not authorize deployments, purchases or credential changes.

## Public distribution

This is an independent, curated copy with fresh Git history. It contains reusable
workflows and public references, not private project instructions, machine inventories,
credentials, operational receipts or customer data. Project-specific guidance has been
removed or generalized. Changes here do not automatically synchronize with another repository.

Apple PDFs, including the CPU optimization guide, are not bundled. The Apple performance
references link to official downloads; access and document terms remain Apple's.

Before updating this collection, follow the short [publication guide](PUBLISHING.md).
Security scanners can flag deliberate synthetic values in the review helper's tests
and hexadecimal revisions in source links. Review each finding; do not exempt all tests.

## License and attribution

Original material is under the [MIT license](LICENSE). Imported and adapted material
retains its own license and copyright notices. The [third-party index](THIRD_PARTY.md)
identifies these directories; notably, `test-properties` remains **CC-BY-SA-4.0**, and
several skills remain **Apache-2.0**. The root license does not replace those terms.

Skill notices and the [provenance manifest](community-skills.json) record sources and
adaptations. Linked documentation, vendor tools and reference assets have their own terms.
No upstream endorsement or universal security, correctness or performance guarantee is implied.
