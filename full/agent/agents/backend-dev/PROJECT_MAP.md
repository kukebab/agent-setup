# backend-dev — Project Map

Last updated: 2026-05-03

<!-- ============================================================
     REPLACE WITH YOUR STACK
     ============================================================
     This map describes the Acme Notes example backend (Next.js +
     Postgres + Neon + Clerk + Stripe + custom WebSocket sync).

     When adapting this template to your project:
     1. Replace the directory structure below with yours
     2. Update the file responsibilities to match your code
     3. Keep the format — file paths, one-line descriptions

     The format is what matters; the specific paths are example.
     ============================================================ -->

## Top-level layout

```
acme-notes/
├── web/                # Next.js 15 frontend (NOT this agent's domain)
├── api/                # ★ Node backend — this agent owns
├── sync/               # ★ WebSocket sync service — this agent owns
├── db/migrations/      # ★ Postgres schema migrations — this agent owns
├── lib/billing/        # ★ Stripe integration — this agent owns
├── lib/auth/           # Clerk integration (light — this agent touches sparingly)
├── tests/              # Test suites
└── package.json
```

## `api/` — REST endpoints

| Path | Responsibility |
|---|---|
| `api/notes/` | CRUD for notes |
| `api/teams/` | Team management (create, invite, settings) |
| `api/billing/webhook.ts` | Stripe webhook receiver |
| `api/billing/portal.ts` | Stripe customer portal session creator |
| `api/exports/pdf.ts` | PDF export endpoint (in build, ETA 2026-05-08) |

## `sync/` — WebSocket sync service

| Path | Responsibility |
|---|---|
| `sync/server.ts` | WebSocket connection handler |
| `sync/crdt.ts` | CRDT merge logic |
| `sync/protocol.ts` | Wire format (JSON-based, see [[agent/memory/wiki/sync-engine]]) |
| `sync/auth.ts` | Token verification on socket open |
| `sync/snapshot.ts` | Full doc snapshot for reconnects |

## `db/migrations/` — Postgres schema

Naming: `YYYY-MM-DD_<description>.sql`

| Recent migrations | What it did |
|---|---|
| `2026-04-30_notes_team_id_index.sql` | Compound index `(team_id, updated_at DESC)` for team note lists |
| `2026-04-15_billing_subscriptions.sql` | Initial subscriptions table for Stripe sync |
| `2026-03-22_notes_full_text_search.sql` | tsvector column + GIN index for search |

## `lib/billing/` — Stripe integration

| Path | Responsibility |
|---|---|
| `lib/billing/stripe.ts` | Stripe client init, webhook signature verification |
| `lib/billing/sync.ts` | Webhook event → DB update logic |
| `lib/billing/portal.ts` | Customer portal helpers |
| `lib/billing/dunning.ts` | Failed-payment retry sequence (see [[agent/memory/wiki/billing-flows]]) |

## Test layout

| Path | What's tested |
|---|---|
| `tests/api/` | API route handlers |
| `tests/sync/` | CRDT merge logic, conflict scenarios |
| `tests/sync/conflict_*.test.ts` | Conflict regression suite (mandatory before any `sync/` deploy) |
| `tests/billing/` | Stripe webhook handling, dunning sequence |

## Key dependencies

- **Stripe SDK** — `stripe` (Node)
- **DB driver** — `pg` via Neon's pooler
- **Auth** — `@clerk/clerk-sdk-node`
- **WebSocket server** — `ws`
- **PDF generation** — `puppeteer` (added 2026-05-03 for PDF export)
