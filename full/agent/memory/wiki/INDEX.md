# Wiki Index

Topic pages for Acme Notes. Cross-linked via `[[topic-name]]`.

## Pages

- [[sync-engine]] — how Acme Notes syncs across clients (CRDT-based, conflict resolution)
- [[billing-flows]] — Stripe integration patterns, dunning, refund policy
- [[design-partner-program]] — closed beta program, current partners, exit criteria
- [[onboarding-funnel]] — current onboarding flow, conversion metrics, redesign history

## How this works

When you ingest a new source (article, transcript, doc), your AI agent updates relevant pages and adds new ones as needed. When you query, your AI reads pages here first.

Pages start with a one-paragraph summary in blockquote, then go deeper. Every page links back to its `raw/` sources at the bottom under `## Sources`.

## Conventions

- One topic per page.
- Blockquote summary as first content.
- Cross-link liberally with `[[topic-name]]`.
- Cite sources at the bottom.
- Keep it light — wiki pages summarize, raw sources hold the full text.
