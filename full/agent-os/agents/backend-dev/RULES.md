# backend-dev — Hard Rules

Inviolable rules for this agent. Update only when establishing a new rule from painful experience.

## Migrations

1. **All migrations through staging first.** No "trivial" exceptions. See `MEMORY.md` for the 2026-03 incident.
2. **Production migrations during low-traffic windows only.** Identify your traffic pattern; for Acme Notes that's currently 02:00-06:00 UTC.
3. **Locking migrations require explicit Maya approval.** Anything that takes a write lock on a >1M-row table.

## Sync engine

4. **No deploy to `sync/` without conflict regression tests passing.** The full suite at `tests/sync/conflict_*.test.ts` must be green.
5. **Rollback plan documented before any `sync/` deploy.** Even minor changes — sync issues silently corrupt user data.
6. **`sync/` changes require post-deploy monitoring** for at least 24 hours. Watch error rates + sync incident reports.

## Billing

7. **Webhook URL env var assertion before deploy.** `STRIPE_WEBHOOK_URL` must match production hostname. See `learnings.md` 2026-04-28.
8. **Never log full Stripe payloads.** They contain customer payment metadata. Log event type + customer ID only.
9. **Stripe webhook signature verification is non-optional.** All webhook endpoints must verify before processing.

## Auth

10. **Clerk session tokens never logged.** Even partial. They're as sensitive as passwords.
11. **`require_auth` middleware on every API route.** No exceptions. Public routes are explicitly opted out.

## Cross-domain handoffs

12. **No frontend code edits.** When a task needs frontend changes, hand back to the orchestrator. Don't try to make minor `web/` tweaks "while you're there."
13. **Don't touch `web/`.** Even if it would be "trivial." Boundary discipline matters more than ad-hoc convenience.

## State updates

14. **Update `STATUS.md` after every task** with a dated entry. Even small fixes.
15. **Update `MEMORY.md` only when the lesson is non-obvious.** Routine work doesn't pollute MEMORY.
16. **Update `PROJECT_MAP.md` only on structural changes.** New modules, renamed dirs, removed files.
