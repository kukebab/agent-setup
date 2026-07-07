# Acme Notes — Decisions

Decision log — what we chose and why. Append when a non-obvious decision is made, so future sessions don't
re-litigate it (and know *why* to revisit it if assumptions change). A decision is not a mistake — it's a
deliberate choice with a rationale.

Format:

```
## YYYY-MM-DD — Decision
**Chose:** X over Y
**Why:** the reasoning
**Revisit if:** the condition that would change the call
```

---

## 2026-04-22 — CRDT over OT for the sync engine

**Chose:** CRDT-based merge over Operational Transform.
**Why:** offline-first is a core use case; CRDTs converge without a central authority and survive flaky mobile connections. OT needs a server-side transform pipeline we don't have the team to maintain.
**Revisit if:** we add real-time cursors / presence at scale, where OT's tighter ordering may win. See `outputs/research/2026-04-22_crdt-libraries-comparison.md`.

## 2026-04-10 — Ship Stripe billing before SSO

**Chose:** Stripe billing as the public-launch gate; SAML SSO deferred to Q3.
**Why:** billing blocks revenue for every customer; SSO blocks only enterprise deals we're not chasing yet (one ask, from Tessera).
**Revisit if:** 2+ pipeline deals make SSO a hard requirement before Q3.
