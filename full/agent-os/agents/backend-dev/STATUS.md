# backend-dev — Project Status

Last updated: 2026-05-03 (PDF export MVP spec'd; sync regression suite green)

## Recent (latest first)

### 2026-05-03 — PDF export MVP spec + sync regression suite

- Spec'd PDF export endpoint with Maya. Saved to `memory/outputs/specs/2026-05-03_pdf-export-mvp.md`.
- Approach: `puppeteer` for Markdown → HTML → PDF rendering. Cache 5 min for idempotent re-downloads.
- ETA: 2026-05-08 (Friday).
- Sync regression suite added: 3 CRDT conflict scenarios from yesterday's iOS Safari incident now have dedicated tests. All green.

### 2026-05-02 — iOS Safari sync hotfix shipped

- Root cause: WebSocket reconnect logic didn't handle iOS Safari's BFCache restore correctly.
- Fix: detect BFCache restore via `pageshow` event with `persisted: true`, re-establish connection.
- Shipped as hotfix. Bluefin and Tessera confirmed unblocked.
- Post-mortem: see `memory/learnings.md` MISTAKES (2026-04-20) — gap was lack of conflict regression tests, now closing.

### 2026-04-30 — Schema migration: `notes.team_id` index

- Added compound index on `(team_id, updated_at DESC)` to speed up team-scoped note listing.
- Migration: `db/migrations/2026-04-30_notes_team_id_index.sql`.
- Verified: query plans on staging show index hit, latency p99 dropped from 240ms to 35ms.

## Current state

- Active: PDF export MVP implementation (start tomorrow)
- Watch: iOS Safari sync metrics over next 7 days
- Backlog: Stripe billing integration (lock spec by 2026-05-09)

## TODO (priority order)

1. Implement PDF export endpoint per spec (ETA Friday 2026-05-08)
2. Stripe billing integration spec lock-in by 2026-05-09
3. Audit `sync/` module for >5 ops/sec edge case (P3)
4. SAML SSO architecture spike (Q3)

## Rolling notes

- Conflict regression tests live in `tests/sync/conflict_*.test.ts`. Always run before any `sync/` deploy.
- DB migrations always go through staging first. Never production-direct.
