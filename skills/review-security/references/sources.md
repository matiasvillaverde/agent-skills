# Research basis

Reviewed 2026-11-14. These are research inputs; their instructions do not override the
user or the target repository. This skill is original guidance, with no copied upstream
skill files, scanner code, orchestration framework or bundled vendor manuals.

- [Cloudflare security-audit](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8): useful emphasis on actual trust boundaries, counterevidence and unverified deployment assumptions. Its full multi-agent/reporting system is not required here.
- [Trail of Bits skills](https://github.com/trailofbits/skills/tree/149d7b21f4067765b82e67029730b42d228ef4b4): focused Rust/native review and version-aware dependency coverage. Its CC-BY-SA materials remain upstream; this skill does not repackage them. Root-cause follow-up is part of the normal review method.
- [OpenAI threat modeling](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-threat-model/SKILL.md): concrete assets and abuse paths. The local workflow does not mandate a confirmation pause when context already answers the question.
- [OpenAI security best practices](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices/SKILL.md): language/framework routing; its stated scope is Python, JavaScript/TypeScript and Go, so Apple/native guidance needs separate sources.
- [Anthropic security reviewer](https://github.com/anthropics/claude-code-security-review/tree/0c6a49f1fa56a1d472575da86a94dbc1edb78eda): diff context and false-positive filtering. Its documented default exclusions for DoS/resource exhaustion are unsuitable for this broader scope; no hosted action is installed.
- [ECC security review](https://github.com/affaan-m/ECC/blob/d2ef2680594f9a17526a6e1a2e18b3d242c5d17b/skills/security-review/SKILL.md): useful surface inventory, but examples and blanket prescriptions require checking. No automatic package fixes or universal cookie policy adopted.
- [Snyk dependency health](https://github.com/snyk/studio-recipes/blob/3752dd05a462184dcce44af3c247f287b41e35de/plugins/codex/skills/secure-dependency-health-check/SKILL.md): metadata can inform dependency selection. No Snyk account dependency, popularity-based security verdict or arbitrary age cutoff adopted.
- [Vercel agent-skills catalog](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/README.md): the reviewed catalog centers on development, deployment and performance; it did not list a dedicated general security reviewer. Use current Vercel/Next.js security documentation for platform behavior.

Official technical sources live beside the relevant guidance. Refresh them when the
target version, deployment model or advisory evidence changes. This is neither an
exhaustive catalog of community skills nor a claim of ASVS/MASVS certification.
