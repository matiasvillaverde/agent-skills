# Structured output for Exa Agent

Use `outputSchema` for list-building, enrichment, finance/company research, and repeatable workflows.

Rules:

- Use a top-level object.
- Put list rows in a named array field.
- Add `maxItems` to arrays when possible.
- Include source/evidence fields, not just conclusions.
- Include stable identifiers: company name, website/domain, person LinkedIn URL, ticker, CIK, etc.
- Include an evidence-based rationale and unresolved gaps for fuzzy judgments; confidence labels are not calibrated probabilities.
- Keep required fields limited to what must exist.
- Use supported JSON Schema formats such as `uri` or `email`. Phone strings need a documented convention or pattern; do not assume a custom format is validated.

Example company-list schema:

```json
{
  "type": "object",
  "properties": {
    "companies": {
      "type": "array",
      "maxItems": 50,
      "items": {
        "type": "object",
        "properties": {
          "company_name": { "type": "string" },
          "website": { "type": "string", "format": "uri" },
          "segment": { "type": "string" },
          "why_it_qualifies": { "type": "string" },
          "evidence_url": { "type": "string", "format": "uri" },
          "confidence": { "type": "string", "enum": ["low", "medium", "high"] }
        },
        "required": ["company_name", "website", "why_it_qualifies", "evidence_url"]
      }
    },
    "coverage_notes": { "type": "string" },
    "known_gaps": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["companies", "coverage_notes"]
}
```

Example with Exa Connect:

```json
{
  "tool": "agent_run",
  "arguments": {
    "query": "Find 10 fast-growing B2B SaaS companies and return estimated monthly website visits from Similarweb.",
    "dataSources": [
      { "provider": "similarweb" }
    ],
    "outputSchema": {
      "type": "object",
      "properties": {
        "companies": {
          "type": "array",
          "maxItems": 10,
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "domain": { "type": "string" },
              "monthlyVisits": {
                "type": "number",
                "description": "Estimated monthly visits from Similarweb"
              }
            },
            "required": ["name", "domain", "monthlyVisits"]
          }
        }
      },
      "required": ["companies"]
    }
  }
}
```
