# Onboarding Funnel

> The flow new teams take from signup to first useful note. Recently rewritten 2026-05-01 — conversion bumped from 12% to 31%. Now monitoring for stability.

## Current flow (post-rewrite)

Single page: "Your team in 30 seconds"

1. Email + team name (1 input)
2. Invite teammates (skip-able, default 3 input fields)
3. First note auto-created with onboarding tips
4. Land on the editor

That's it. No wizard, no multi-step.

## Conversion (last 30 days)

- **Pre-rewrite (April):** 12% trial → activation
- **Post-rewrite (May):** 31% trial → activation

Activation = at least 3 notes created, 1 teammate invited, within 24h.

## What changed

- 4-step wizard → single page
- "Step 1 of 4" framing → "your team in 30 seconds" outcome framing
- 11 form fields → 4 (email, team name, optional 3 teammate emails)
- Removed welcome video (nobody watched)
- Removed plan selection (everyone gets trial, plan picked at end)

## Metrics to watch

- Trial → activation rate (target: stay >25%)
- Time to first note (target: <60 seconds median)
- Teammate invite rate (target: >50% invite ≥1)

## Cross-links

- [[design-partner-program]] — partners helped validate the simpler flow
- [[billing-flows]] — plan picker now lives at end, not start

## Sources

- A/B test results (`outputs/research/2026-04-29_onboarding-ab-test.md`)
