# Acme Notes — Constraints

Hard "always / never" rules. Curated and inviolable — not a dumping ground. An entry earns its place here only
after a painful incident proved the rule. Keep this list short; if it grows past a screen, some of it is really a
pattern, not a constraint.

---

- **NEVER deploy a change to `sync/` or merge logic without a green conflict regression suite.** (Cost us a design partner's data — see `mistakes.md` 2026-04-20.)
- **NEVER commit secrets, API keys, or tokens to the repo.** Use `.env` (git-ignored). The pre-commit hook blocks common key patterns, but the rule is yours to hold.
- **ALWAYS verify `STRIPE_WEBHOOK_URL` points to the prod hostname before a billing deploy.** (3 days of missed payment events — see `mistakes.md` 2026-04-28.)
- **NEVER commit on the spot to a design-partner feature ask during a call.** Buy 24h to scope.
