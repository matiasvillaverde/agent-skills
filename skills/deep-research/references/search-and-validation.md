# Search and validate candidate evidence

Use these techniques when semantic search, list-building or repeated extraction would
help the investigation. They consolidate useful ideas from the former local `exa-search`
skill; the general research loop remains in `SKILL.md`.

## Search with a purpose

Describe the evidence or page you need: an implementation, a maintainer's reproduction,
a dated filing, or a study with a particular method. Change the evidence angle when a
query stalls; repeated synonyms do not establish wider coverage. Separate practitioner,
primary-source and counterexample searches when those sources answer different questions.

Inspect the available tool schema before using Exa or another provider. Use supported
date, domain, category and result-count controls rather than assuming inline query syntax
implements a filter. Resolve relative dates from today's date and verify the source's
publication and event dates. Keep results bounded to what can be inspected; expand when
new leads justify it. Do not impose a fixed query count or a particular agent model.

## Qualify before counting

For a requested list, establish the inclusion criteria and a small output schema. Keep
identity, a supporting source, the relevant observed facts and any uncertainty. Distinguish
an absent fact from evidence that the criterion is false. Search ranking, similarity and
an extracted field are not proof that a candidate qualifies.

Read the relevant original sources. For a person or company, resolve the identity and
time period before joining facts from different pages. For code, check repository, version
and actual implementation. For papers, distinguish metadata, abstracts and full text.
For news, separate the event date from the date an article repeats the story.

Deduplicate by the underlying entity or study, while retaining meaningful versions and
conflicts. Several URLs repeating one press release are one evidence chain. Report which
requested segments were covered and which remain unverified; do not replace missing facts
with a confident summary or count raw search slots as reviewed sources.

When a hosted research agent returns a report or structured data, apply the same identity,
source and coverage checks. Preserve continuation handles when needed and disclose actual
access or budget limits. Follow the user's provider constraints; otherwise a reported
provider failure can be followed by an available alternative.
