# Acme Notes — Mistakes

Recent corrections (last ~60–90 days) still likely to repeat. **Read this file every session.**

Append after every user correction. When the same root cause repeats 2+ times, promote it to a rule in
`patterns.md` and archive the individual mistakes to `archive.md`. Keep this file signal-dense (~300 lines max).

Format:

```
## YYYY-MM-DD — Short title
**Wrong:** what I did
**Correct:** what I should have done
**Why:** reason it matters
**Trigger:** when to recall this lesson
```

---

## 2026-04-28 — Stripe webhooks pointed to localhost in prod

**Wrong:** local dev set the webhook to ngrok, never reset the env var, prod missed 3 days of payment events.
**Correct:** add a `STRIPE_WEBHOOK_URL` assertion to the pre-deploy script.
**Why:** silent revenue blindness. 3 customers thought they paid but accounts didn't activate.
**Trigger:** any deploy touching `lib/billing/` — verify `STRIPE_WEBHOOK_URL` matches the prod hostname.

## 2026-04-20 — Shipped sync engine without conflict tests

**Wrong:** deployed CRDT merge logic to prod with a smoke test only, no conflict regression suite.
**Correct:** sync changes need a dedicated conflict test pass before any prod deploy.
**Why:** lost a design partner's data temporarily. Recovered from backups, but trust-eroding.
**Trigger:** any change to `sync/` or merge logic — gate must include conflict regression tests.
(Promoted to a hard rule — see `constraints.md`.)

## 2026-04-12 — Promised Bluefin a feature before scoping with Alex

**Wrong:** said "yes" to Bluefin's PDF export ask on a sales call without checking effort with Alex.
**Correct:** "great idea, let me confirm scope and get back to you tomorrow" — buys 24h to scope properly.
**Why:** burned trust when delivery slipped 2 weeks. Better to commit later but accurately.
**Trigger:** any new feature ask from a design partner during a call — never commit on the spot.
