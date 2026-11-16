# Choose the next evidence source

Choose by the question that remains, not by a fixed provider checklist. These routes were
reviewed on 2026-11-13; check current tool schemas, access and source versions when used.
Provider documentation describes capabilities, not proof that this session can call them.

## Web and software

| Need | Useful route | Check before relying on it |
| --- | --- | --- |
| Broad discovery or a new angle | [Exa](https://exa.ai/docs/reference/search), [Firecrawl search](https://docs.firecrawl.dev/features/search), available native web search | Use the chosen tool's actual filters/query syntax. Semantic matching, keyword search and indexed code search are different. An excerpt is a lead. |
| Read a known source | [Exa contents](https://exa.ai/docs/reference/get-contents), [Firecrawl scrape](https://docs.firecrawl.dev/features/scrape), native page/PDF reader | Check page identity, relevant content, freshness, truncation and retrieval failure. Read tables/figures when they carry the evidence. A successful request can return an error page. |
| Find pages within a known site | [Firecrawl map](https://docs.firecrawl.dev/features/map); a bounded [crawl](https://docs.firecrawl.dev/features/crawl) when needed and available | Map discovers URLs; it does not read them or prove complete coverage. Bound crawl paths/pages/depth and record failures. Do not launch a site-wide crawl by default. |
| Verify implementation or a reported fix | GitHub connector, [code search](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax), [issues/PRs](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests), releases and tests | Pin claims to source revision and affected/released version. A closed issue or merged PR does not prove a released fix. Public code is not automatically licensed for reuse. Read code without running untrusted setup scripts. |

Existing Brave, Tavily or another search connector can fill a concrete coverage gap; this
skill does not require installing or subscribing to them. Hosted research services can
produce candidate findings, but their generated reports still need source and coverage
checks. Report provider failures and actual returned costs. Preserve continuation IDs when
the tool requires them; honor throttling and access/budget errors instead of blind retries.

## Papers and scholarly records

Start with relevant seed papers, then follow their references for foundations and their
citers for extensions, replications, criticism and corrections. Re-seed from newly useful
work. Combine this with fresh topic queries: citation neighborhoods can miss newer or
disconnected work. Citation count and citation direction do not establish agreement.

| Source | Best use | Important distinction |
| --- | --- | --- |
| [OpenAlex](https://help.openalex.org/api/) and its [citation graph](https://help.openalex.org/data/works/citations/) | Broad discovery, reference/citer expansion and work identifiers | Graph coverage is incomplete and imports other indexes. CC0 metadata does not license the underlying articles. Check current authentication/pagination limits. |
| [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | DOI identity, references, publication relations and [update/retraction metadata](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/) | Verify the original notice when status matters. Metadata may lag or conflict; an absent flag is not proof of no correction. Use the production service, not stale Labs data. |
| [Semantic Scholar](https://www.semanticscholar.org/product/api) | Alternative citation graph and related-work discovery when useful | Abstracts, TLDRs and PDF links are not full-text reads. Check current API access, attribution and [use terms](https://api.semanticscholar.org/license/). |
| [arXiv](https://info.arxiv.org/help/api/user-manual.html) | Versioned preprints in supported fields | Preserve the exact version read and check later revisions/withdrawals. A preprint is not peer-review confirmation; the metadata API is not a complete citation graph. |
| [PubMed](https://pubmed.ncbi.nlm.nih.gov/help/), [PMC](https://pmc.ncbi.nlm.nih.gov/tools/developers/) and [Europe PMC](https://europepmc.org/RestfulWebService) | Biomedical indexing, fielded queries, notices and permitted full-text retrieval | PubMed abstracts and PMC full text differ. Use supported retrieval routes and article permissions; do not bulk-scrape PMC HTML. |
| [OpenReview](https://docs.openreview.net/getting-started/using-the-api) | Submissions, revisions, available reviews/replies and venue decisions | Check existing account/connector access. Submission, acceptance and review comments are different evidence; unavailable reviews stay a gap. |

Firecrawl's ordinary `research` search category filters web results. Its separately
documented [paper workflow](https://github.com/firecrawl/skills/blob/1d4b0728d0f448cafef2eb8370c907fde7cb6f42/skills/workflows/firecrawl-research-papers/SKILL.md)
uses dedicated paper tools with bounded corpus coverage. Discover whether those tools
are available; do not infer paper-index access from a successful web search.

Resolve identities before merging: DOI, arXiv ID/version, PMID/PMCID or venue record.
Link a preprint, journal article, supplement and correction as related versions, while
preserving what changed. Multiple reports can describe one study. Read the relevant
methods/results and supporting data before making a decisive technical claim. A real DOI
does not prove that a paper supports the sentence citing it. Label metadata-only,
abstract-only, truncated and inaccessible evidence explicitly.

A systematic review additionally needs a declared search/screening protocol, appropriate
databases and coverage accounting. Ordinary adaptive web research does not establish that.

## Other evidence routes

- **Official documentation and standards:** use the owning issuer and applicable version.
  Check amendments, errata and status; for example, an [RFC](https://www.ietf.org/process/rfcs/)
  is not necessarily an Internet Standard.
- **Datasets, study registries and artifacts:** inspect methodology, provenance, access and
  versioned records. [DataCite relationships](https://datacite-metadata-schema.readthedocs.io/en/4.6/properties/relatedidentifier/)
  can distinguish a dataset version, parent concept and related paper.
- **Practitioner discussions:** use maintainer discussions, forums and firsthand reports
  to find failure modes and reproduction leads. Their authority depends on the claim;
  popularity and repeated anecdotes do not substitute for verification.
- **Historical snapshots:** useful for what a page said at a particular time. Keep snapshot
  date separate from event date; an archived page does not establish current behavior.
- **Local or connected material:** useful for user-specific constraints and existing evidence.
  Keep its access boundary and identify when the reader cannot independently inspect it.

For each important finding, retain enough context to retrace it: source identity, version/date,
supporting location, what was actually read and the limitation. Add fields only when useful.
Source independence matters more than the number of providers returning the same material.
