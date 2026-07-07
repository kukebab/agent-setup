# data-eng — Hard Rules

Inviolable rules for this agent. Update only when establishing a new rule from painful experience.

## Pipelines

1. **No backfill against prod without a dry run first.** Verify row counts and spot-check output on a sample.
2. **Schema changes go through staging first.** No "trivial" exceptions.
3. **Rollback plan documented before any pipeline change** that touches production data.

## Data quality

4. **Never silently drop or coerce bad rows.** Log or quarantine them for review.
5. **PII fields are documented and access-controlled**, never logged in plaintext.

## Cross-domain handoffs

6. **No application code edits.** When a task needs backend/frontend changes, hand back to the orchestrator.

## State updates

7. **Update `STATUS.md` after every task** with a dated entry. Even small fixes.
8. **Update `MEMORY.md` only when the lesson is non-obvious.** Routine work doesn't pollute MEMORY.
9. **Update `PROJECT_MAP.md` only on structural changes.** New pipelines, renamed schemas, removed files.
