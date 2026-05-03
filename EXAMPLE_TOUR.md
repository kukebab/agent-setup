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

AI:  [auto-loads memory/STATE.md, learnings.md MISTAKES, wiki/INDEX.md,
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

The AI knows the project. It read `STATE.md` (priorities), `learnings.md` (don't repeat past mistakes), `wiki/` (durable knowledge about sync, billing, design partners), and the latest `daily/` (recent events). Zero context dump from you.

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
full/
├── AGENTS.md                ← schema (router, not a rule dump — 187 lines)
├── CLAUDE.md                ← mirror
├── memory/                  ← like starter/, plus:
│   ├── INDEX.md             ← top-level navigation
│   ├── USER.md.template     ← optional personal context
│   ├── clients/             ← per-client live state
│   │   ├── bluefin-coffee.md
│   │   └── tessera-studio.md
│   └── outputs/
│       ├── specs/2026-05-03_pdf-export-mvp.md
│       └── research/2026-04-22_crdt-libraries-comparison.md
└── agent-os/
    ├── rules/               ← 9 behavioral policies (auto-loaded)
    │   ├── quality-gate.md       ← THE most valuable rule
    │   ├── agent-quality.md      ← agent dispatch + memory loop scaling
    │   ├── self-monitor.md       ← improvement loop
    │   ├── testing.md, file-size-triggers.md, cost-aware-llm.md
    │   ├── identity.md.template  ← give your AI a persona
    │   └── language.md.template  ← communication preferences
    ├── agents/              ← domain specialists with persistent state
    │   └── backend-dev/
    │       ├── STATUS.md         ← events log
    │       ├── MEMORY.md         ← long-term gotchas
    │       ├── PROJECT_MAP.md    ← code map (REPLACE WITH YOUR STACK)
    │       └── RULES.md          ← hard rules for this domain
    ├── skills/              ← 9 reusable workflows
    │   ├── morning, endday, ingest, lint
    │   ├── create-spec, call-debrief, web-researcher
    │   └── create, swarm
    └── hooks/               ← runtime enforcement
        ├── session-start.sh
        └── commit-memory-reminder.sh
```

Plus `adapters/` for tool-specific wiring (Cursor, Aider, Windsurf) and `scripts/` for governance (staleness check at commit time, install.sh).

**~50 files total.** More moving parts, but each piece earns its place.

---

## What changes for you, day-to-day

**Sessions:**
- `/morning` → AI knows your priorities, proposes plan
- `/endday` → session saved to `daily/`, drift caught
- `/ingest <url>` → AI reads it, files raw source, updates wiki, logs daily
- `/lint` → wiki health check (orphans, broken links, stale claims)
- AI corrects itself → mistake auto-logged to `learnings.md`, never repeated

**Over weeks:**
- `wiki/` compounds — concepts get richer with every ingest
- `learnings.md` accumulates — your AI gets sharper, not flatter
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
