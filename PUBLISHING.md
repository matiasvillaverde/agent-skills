# Maintaining the public copy

Keep updates focused on reusable instructions. Copy only the reviewed skill directories
and their necessary references, scripts and licenses; never mirror a private repository
or its history into this one.

Before publishing:

1. Inspect the complete diff, including executable helpers, fixtures, assets and metadata.
   Remove private project examples, absolute personal paths, internal endpoints, account
   identifiers, infrastructure details, credentials and operational or customer records.
2. Preserve upstream licenses, attribution and modification notices. Confirm redistribution
   terms for newly imported material. Link to external manuals rather than bundling them
   without permission.
3. Check skill names/frontmatter, relative links, referenced scripts and provenance digests.
   Run relevant helper tests when executable behavior changes. A documentation check does
   not prove a workflow works on every platform or device.
4. Run passive secret scans over the entire proposed public tree and any new public history.
   Store scanner output outside the repository. Inspect every candidate without printing
   credential values; do not validate discovered credentials against providers by default.
5. Inspect staged paths and commit metadata. Publish only the reviewed tree. Use an authorized
   public identity or GitHub-provided no-reply address for commits.

Example scan commands, after checking the installed tools' help:

```sh
gitleaks dir . --redact=100
trufflehog filesystem . --no-update --no-verification \
  --results=verified,unknown,unverified --fail --fail-on-scan-errors
```

Run these with stdout/stderr redirected to your private report directory: scanner output
can itself contain secrets. Distinguish synthetic fixtures and public identifiers from
credentials; do not add blanket test-directory exclusions or claim a scan proves secrecy.

Do not copy local source checkouts, review caches, scan reports or downloaded manuals into
release archives. Keep the existing focused references instead of adding duplicate policy files.
