# Tour — agent-os-starter

5-minute walkthrough using the fictional Acme Notes example.

## The fictional project

**Acme Notes** is a collaborative notebook SaaS for small teams (5–50 people). Closed beta with 8 design partners. Public launch in ~2 months. Solo founder Maya + part-time backend contractor Alex.

The example data fills out every file in `starter/` and `full/` so you can see what a working install actually looks like — before replacing it with your own.

---

## Before agent-os

Without persistent memory, every session restarts:

```
You: "What's on my plate today?"
AI:  "I don't know. Tell me about your project."
You: [explains for 5 minutes — what Acme Notes is, who Bluefin is, what Stripe
     integration means here, why the iOS Safari sync incident matters,
     what 31% conversion is in context...]
AI:  "Got it. Here's what I'd prioritize..."

[next session, next day]
You: "What's on my plate today?"
AI:  "I don't know. Tell me about your project."
```

Every session repeats the context dump. Nothing compounds.

---

## After agent-os

```
You: "morning"

AI:  [auto-loads memory/STATE.md, learnings/mistakes.md, wiki/INDEX.md,
      latest daily/]

     Top priorities:
     1. Sync stability (P0) — Alex on it, regression suite green
     2. Stripe billing for public launch — lock spec by Friday
     3. PDF export MVP for Bluefin — ETA Friday

     Active blockers: none. Sync hotfix unblocked Bluefin and Tessera 2026-05-02.
     Watchpoints: Tessera renewal 2026-06-01.

     Today's plan:
     1. Start PDF export implementation (Alex)
     2. Lock Stripe billing spec — public launch in 2 months
     3. Bluefin demo prep

     Start with #1?
```

The AI knows the project. It read `STATE.md` (priorities), `learnings/` (don't repeat past mistakes), `wiki/` (durable knowledge about sync, billing, design partners), and the latest `daily/` (recent events). Zero context dump from you.

---

## Tour by file (Simple Mode)

```
starter/
├── AGENTS.md                ← your AI reads this first (the schema)
├── CLAUDE.md                ← mirror for Claude Code
└── memory/
    ├── STATE.md             ← current priorities, "Last updated" date
    ├── learnings.md         ← MISTAKES (don't repeat) + WINS + PATTERNS
    ├── daily/2026-05-03.md  ← today: actions, decisions, insights, tomorrow
    ├── wiki/
    │   ├── INDEX.md
    │   ├── sync-engine.md   ← cross-linked topic page
    │   ├── billing-flows.md
    │   └── design-partner-program.md
    ├── outputs/README.md    ← where generated specs/research go
    └── raw/README.md        ← immutable source dumps
```

**12 files.** Drop them into your project, replace Acme Notes data with yours, your AI has memory. That's it.

---

## Tour by file (Advanced Mode)

```
your-project/
├── AGENTS.md                ← thin stub, points at agent/AGENTS.md
├── CLAUDE.md                ← mirror stub
└── agent/                   ← everything lives here, one folder
    ├── AGENTS.md            ← canonical schema (router, not a rule dump)
    ├── VERSION.md           ← installed schema version, for updates
    ├── memory/              ← like starter/, plus:
    │   ├── INDEX.md             ← top-level navigation
    │   ├── USER.md.template     ← optional personal context
    │   ├── learnings/           ← single learnings.md split by lifecycle:
    │   │   ├── mistakes.md      ← the hot file (read every session)
    │   │   ├── patterns.md · decisions.md · constraints.md
    │   │   └── archive.md       ← stale lessons + wins (not auto-loaded)
    │   ├── inbox/               ← /mine-learnings candidate queue
    │   │   └── learnings-candidates.md
    │   ├── projects/            ← per-project / per-client live state
    │   │   ├── bluefin-coffee.md
    │   │   └── tessera-studio.md
    │   └── outputs/
    │       ├── specs/2026-05-03_pdf-export-mvp.md
    │       └── research/2026-04-22_crdt-libraries-comparison.md
    ├── rules/               ← 9 behavioral policies (auto-loaded)
    │   ├── quality-gate.md       ← THE most valuable rule
    │   ├── agent-quality.md      ← agent dispatch + memory loop scaling
    │   ├── self-monitor.md       ← improvement loop
    │   ├── testing.md, file-size-triggers.md, cost-aware-llm.md
    │   ├── identity.md.template  ← give your AI a persona
    │   └── language.md.template  ← communication preferences
    ├── agents/              ← domain specialists with persistent state — install-time prompt asks which to include
    │   └── backend-dev/          ← the worked example; frontend-dev/, infra/, data-eng/ also ship as blank templates
    │       ├── STATUS.md         ← events log
    │       ├── MEMORY.md         ← long-term gotchas
    │       ├── PROJECT_MAP.md    ← code map (REPLACE WITH YOUR STACK)
    │       └── RULES.md          ← hard rules for this domain
    ├── skills/              ← reusable workflows
    │   ├── morning, endday, ingest, lint
    │   ├── review-learnings, mine-learnings   ← learnings lifecycle + trace→learnings loop
    │   ├── create-spec, call-debrief, web-researcher
    │   └── create, swarm
    ├── hooks/               ← runtime enforcement
    │   ├── session-start.sh
    │   └── commit-memory-reminder.sh
    └── scripts/             ← governance + tooling
        ├── context.sh, mine_learnings.py (+ tests)
        └── git-hooks/       ← staleness check at commit time
```

Plus `adapters/` in the source repo for tool-specific wiring (Cursor, Aider, Windsurf) — those write outside `agent/`, into whatever path each tool auto-loads.

**~60 files total**, all under one `agent/` folder. More moving parts than Simple Mode, but each piece earns its place, and nothing is scattered across your project root.

---

## What changes for you, day-to-day

**Sessions:**
- `/morning` → AI knows your priorities, proposes plan
- `/endday` → session saved to `daily/`, drift caught
- `/ingest <url>` → AI reads it, files raw source, updates wiki, logs daily
- `/lint` → wiki health check (orphans, broken links, stale claims)
- `/mine-learnings` → mine the session transcript for corrections + repeated tool failures → review queue
- AI corrects itself → mistake logged to `learnings/mistakes.md`, never repeated

**Over weeks:**
- `wiki/` compounds — concepts get richer with every ingest
- `learnings/mistakes.md` stays curated (promote → `patterns.md`, archive stale) — your AI gets sharper, not flatter
- Agent state stays continuous — `backend-dev` remembers the sync incident from 3 weeks ago
- Pre-commit hook catches stale state markers before they ship

---

## What it does NOT do

- Replace your code editor or IDE
- Generate code by itself (your AI does that; agent-os just gives it persistent context)
- Solve focus or discipline (still on you to ship)
- Work without memory hygiene (you have to actually update `STATE.md` when priorities shift — or use the hooks to nudge yourself)

---

## Next

- [`README.md`](README.md) — the 30-second pitch for humans
- [`INSTALL_PROMPT.md`](INSTALL_PROMPT.md) — paste into your AI agent for auto-install
- [`INSTALL.md`](INSTALL.md) — manual install walkthrough
