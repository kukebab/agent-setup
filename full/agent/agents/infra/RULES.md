# infra — Hard Rules

Inviolable rules for this agent. Update only when establishing a new rule from painful experience.

## Deploys

1. **No direct prod changes without a plan review.** Always show a plan/diff before applying infra changes.
2. **Production changes during low-traffic windows only**, unless it's an emergency fix.
3. **Rollback plan documented before any infra change** that affects a running service.

## Secrets

4. **Never log secrets or credentials.** Not even partially.
5. **Secrets live in the secrets manager, never in code or plain config files.**

## Cross-domain handoffs

6. **No application code edits.** When a task needs backend/frontend changes, hand back to the orchestrator.

## State updates

7. **Update `STATUS.md` after every task** with a dated entry. Even small fixes.
8. **Update `MEMORY.md` only when the lesson is non-obvious.** Routine work doesn't pollute MEMORY.
9. **Update `PROJECT_MAP.md` only on structural changes.** New pipelines, renamed dirs, removed files.
