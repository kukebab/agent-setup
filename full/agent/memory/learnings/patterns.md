# Acme Notes — Patterns

Durable rules graduated from repeated mistakes, plus insights about what works. Always-on; stays unless invalidated.

Format: a short rule name, then **Rule / Why / Trigger** (or just a paragraph for an insight).

---

## Design partners are signal, not edge cases

**Rule:** treat a design partner's incident as a canary alert for what breaks at 100x scale, not as "one customer's edge case."
**Why:** two of our biggest near-disasters (sync data loss, sales overcommit) both surfaced through design partners first.
**Trigger:** when tempted to deprioritize a partner-reported bug as "rare" — it's a preview, fix the class not the instance.

## Incidents that force the right infrastructure pay for themselves

**Rule:** when an incident exposes a missing safety net, fix the *gap*, not just the bug.
**Why:** the iOS Safari sync bug forced the conflict-regression infrastructure that should have existed from day one — the most expensive incident bought the most valuable test suite.
**Trigger:** post-incident — ask "what infrastructure would have caught this?" and build that, not only the one-line fix.

## Pre-call async demo beats live demo for closing

Sending a 5-minute Loom before a sales call (instead of demoing live) let Bluefin prep their questions; the call became closing, not pitching. Bluefin signed a pilot in a single 30-minute call.
Pattern: async demo first, synchronous time for decisions.

## Frame onboarding as outcome, not process

The onboarding rewrite (12% → 31% conversion) replaced a 4-step wizard with a single-page "your team in 30 seconds" flow.
Pattern: cut steps; frame the result ("your team set up in 30 seconds"), not the procedure ("step 1 of 4").
