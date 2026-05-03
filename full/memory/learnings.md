# Acme Notes — Learnings

Append-only record of mistakes (so we don't repeat them), wins (so we remember what worked), and patterns (durable insights). Read by your AI agent at session start.

---

## MISTAKES

Format:

```
## YYYY-MM-DD — Short title
**Wrong:** what I did
**Correct:** what I should have done
**Why:** reason it matters
**Trigger:** when to recall this lesson
```

### 2026-04-20 — Shipped sync engine without conflict tests

**Wrong:** deployed CRDT merge logic to prod with smoke test only, no conflict regression suite.
**Correct:** sync changes need a dedicated conflict test pass before any prod deploy.
**Why:** lost a design partner's data temporarily. Recovery from backups, but trust-eroding.
**Trigger:** any change to `sync/` or merge logic — gate must include conflict regression tests.

### 2026-04-28 — Stripe webhooks pointed to localhost in prod

**Wrong:** local dev set webhook to ngrok, never reset env var, prod missed 3 days of payment events.
**Correct:** add Stripe env URL assertion to pre-deploy script.
**Why:** silent revenue blindness. 3 customers thought they paid but accounts didn't activate.
**Trigger:** any deploy touching `lib/billing/` — verify `STRIPE_WEBHOOK_URL` matches prod hostname.

### 2026-04-12 — Promised Bluefin a feature before scoping with Alex

**Wrong:** said "yes" to Bluefin's PDF export ask on a sales call without checking with Alex on effort.
**Correct:** "great idea, let me confirm scope and get back to you tomorrow" — buys 24h to scope properly.
**Why:** burned trust when we had to push delivery 2 weeks. Better to commit later but accurately.
**Trigger:** any new feature ask from a design partner during a call — never commit on the spot.

---

## WINS

### 2026-05-01 — Onboarding rewrite: 12% → 31% conversion

4-step wizard replaced with single-page "your team in 30 seconds" flow.
Pattern: cut steps, frame as outcome ("your team setup in 30 seconds") not process ("step 1 of 4").

### 2026-04-15 — Bluefin signed pilot in single 30-min call

Sent them a 5-min Loom of the product before the call instead of doing a live demo.
Pattern: pre-call asynchronous demo lets them prep their questions; call is for closing, not pitching.

---

## PATTERNS

### Design partners are signal, not features

Two of our biggest near-disasters (sync data loss, sales overcommit) involved design partners.
Pattern: their problems are the real problems we'll have at 100x scale. Treat their incidents as canary alerts, not "edge cases for one customer."

### Sync incidents teach faster than feature work

Yesterday's iOS Safari bug forced us to build the regression infrastructure that should have existed from day one.
Pattern: the most expensive incidents pay back if they force the right test infrastructure. Don't just fix the bug — fix the gap.
