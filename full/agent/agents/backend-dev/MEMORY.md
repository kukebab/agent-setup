# backend-dev — Memory

Long-term lessons, gotchas, decisions with rationale. The kind of knowledge that would take a new agent hours to rediscover.

---

## Platform gotchas

### iOS Safari WebSocket BFCache

Discovered 2026-05-02. iOS Safari's BFCache (Back-Forward Cache) restores a page **without** firing `load` or `visibilitychange`. Only `pageshow` with `event.persisted === true` reliably indicates BFCache restore.

**Implication:** WebSocket connections appear "alive" to the page state but are actually dead. Standard reconnect logic fails because the socket object exists in memory but the underlying connection is broken.

**Fix:** listen for `pageshow` with `persisted: true`, then explicitly close + reopen the WebSocket.

### CRDT op-log size

We assumed CRDT op-logs would stay small (<10 KB per doc). At >100 ops/doc, op-log size starts dominating sync payload. Compaction is needed.

**Plan:** snapshot + GC ops older than 24h on the server. Not yet implemented. Backlog item — important if we hit 1000+ paying users.

### Postgres connection limits on Neon

Neon's free tier caps at ~10 concurrent connections. Easy to hit during burst writes. We use a connection pooler (PgBouncer) — make sure new code goes through it, not direct PG connection.

---

## Architectural decisions

### Custom CRDT vs Yjs / Automerge

Decision date: 2026-04-22. We stayed custom. Full reasoning: `agent/memory/outputs/research/2026-04-22_crdt-libraries-comparison.md`.

**Re-evaluation triggers:**

1. Hit 1000+ paying users (more incidents = more pain)
2. Adding real-time presence indicators (Yjs makes this easier)

If neither triggered by 2026-12, default to staying custom.

### `lib/billing/` separated from `api/`

Stripe code is its own module, not mixed into routes. Why: webhook signing requires raw request body — easier to handle in a dedicated module than have every route deal with it.

**Don't move billing logic into routes** even if it seems cleaner. The webhook signature verification depends on body parsing being deferred.

### Migration discipline

ALL migrations go through staging first. No exceptions, including "trivial" index adds. Why: 2026-03 incident where a "trivial" index on a 5M-row table locked the table for 8 minutes during deploy.

**Trigger:** any `CREATE INDEX` / `ALTER TABLE` / `DROP` → run on staging copy first, confirm execution time, then prod during low-traffic window.

---

## Deploy gotchas

### Stripe webhook URL env var

Past incident (`agent/memory/learnings/mistakes.md` 2026-04-28): localhost webhook URL got promoted to prod, missed 3 days of payment events.

**Mitigation:** pre-deploy script asserts `STRIPE_WEBHOOK_URL` matches prod hostname. If you ever bypass that check, update both the assertion AND the env.

### `puppeteer` size

Adding `puppeteer` to the backend container adds ~150MB. Monitor build sizes on Vercel — if we cross deployment limits, evaluate alternatives (Gotenberg, lambdas, etc).
