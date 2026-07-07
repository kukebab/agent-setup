# Acme Notes — Business State

Last updated: 2026-05-03

## Active workstreams (by priority)

| # | Workstream | Status | Owner | Next action |
|---|------------|--------|-------|-------------|
| 1 | **Sync stability** | 🔴 P0 — critical | Alex | Conflict regression suite green; monitor iOS Safari for 7 days |
| 2 | **Stripe billing for public launch** | 🟡 P1 — gate item | Maya | Lock spec by Friday; build during next 6 weeks |
| 3 | **PDF export (Bluefin pilot)** | 🟢 P2 — design partner ask | Alex | MVP ETA Friday |
| 4 | **Mobile-responsive polish** | ⚪ P2 — deferred | Maya | Post-launch |
| 5 | **SAML SSO (Tessera renewal)** | ⚪ P3 — Q3 backlog | TBD | Spec by August, ship by October |

## Public launch

Target: ~2 months out (mid-July 2026). Gates:

- [ ] Stripe billing live + tested with 3 real charges
- [ ] Sync regression suite green on iOS Safari + Chrome + desktop
- [ ] 8/8 design partners signed off
- [ ] Onboarding funnel ≥ 25% conversion (currently 31%)

## Active design partners

See `projects/*.md` for full state. Quick summary:

- **Bluefin Coffee** — pilot, PDF export ask, see [[projects/bluefin-coffee]]
- **Tessera Studio** — active, renewing 2026-06-01, see [[projects/tessera-studio]]

## Team

- **Maya** — solo founder. Product + design + frontend + customer dev.
- **Alex** — part-time backend contractor (~20 hrs/week). Owns `sync/` + DB.
- **AI agent** — daily collaborator. Persona: see `USER.md` if defined.

## Blockers

None right now. Sync hotfix unblocked Bluefin and Tessera 2026-05-02.

## Recent wins (last 30 days)

- 2026-05-01 — Onboarding funnel rewrite: 12% → 31% conversion
- 2026-05-02 — iOS Safari sync bug fixed
- 2026-05-03 — Tessera confirmed renewal (signing 2026-06-01)
