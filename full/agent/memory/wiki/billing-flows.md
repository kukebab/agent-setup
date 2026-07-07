# Billing Flows

> How Acme Notes handles Stripe billing — subscriptions, dunning, refunds. Currently in build for public launch (~2 months out).

## Subscription model

- Per-user pricing: $8/user/month
- Team discounts: 10% at 10+ users, 20% at 25+ users
- Annual billing: 2 months free
- 14-day trial, no credit card required

## Stripe integration

- Webhook events: `customer.subscription.*`, `invoice.*`
- Customer portal: hosted by Stripe, link from Settings → Billing
- Webhook URL must match prod hostname — see `learnings/mistakes.md` for the 2026-04-28 incident

## Dunning sequence

1. Day 0 (failed charge): retry next day
2. Day 4: retry + email + in-app banner
3. Day 7: retry + final warning email
4. Day 14: account paused (read-only)
5. Day 30: account suspended (data preserved 90 days)

## Refund policy

- 30-day refund window for annual plans
- Pro-rated refunds for downgrades
- No refunds on monthly plans (cancel anytime)

## Design partner conversion

At public launch (mid-July 2026):

- [[projects/bluefin-coffee]] — 50% off year 1 = ~$48/month, ~$528/year annual
- [[projects/tessera-studio]] — already converting at standard rate, ~$768/year annual

## Cross-links

- [[design-partner-program]] — partner-to-paid conversion plan

## Sources

- Stripe billing patterns guide (`raw/2026-04-10_stripe-billing-patterns.md`)
