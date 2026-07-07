# Rules

Auto-loaded behavioral policies for your AI agent. These shape how the agent works, not what it works on.

## How rules are loaded

Rules in this directory are referenced from the main schema (`AGENTS.md` / `CLAUDE.md`) and read at session start. They form an always-on context layer — the agent doesn't search for them, they're already loaded.

For tools that don't auto-load directories (Codex, Aider), the schema lists each rule explicitly. For Claude Code, the schema can use the rules directory directly.

## What's here

Generic, stack-agnostic rules:

- **`quality-gate.md`** — verification before completion, plan mode, bug-fix protocol
- **`agent-quality.md`** — agent dispatch protocol, memory loop scaling, verification iron law
- **`self-monitor.md`** — improvement loop, learnings format, correction protocol
- **`testing.md`** — when to write tests, fixtures, anti-patterns
- **`file-size-triggers.md`** — file hygiene, decomposition triggers
- **`cost-aware-llm.md`** — LLM API cost discipline, model routing patterns

## Templates (rename to use)

- **`identity.md.template`** — defines your AI's persona and tone
- **`language.md.template`** — communication preferences (response language, code language)

## Why so few

A starter ships only rules that translate across projects. Stack-specific or domain-specific rules (e.g. "how we deploy to our serverless platform") belong in your project, not the starter.

If you want more rules: copy a generic one as a template, or write your own. The pattern is simple — markdown with clear sections, kept under ~200 lines each.

## Adding rules

When you hit a recurring issue your AI keeps making, write a rule. The flow:

1. The mistake gets logged in `agent/memory/learnings/mistakes.md`
2. If the mistake repeats, promote the lesson to a rule here
3. Update the schema (`AGENTS.md`) to reference the new rule

Rules are for patterns the AI must follow on every task. One-off lessons stay in `agent/memory/learnings/mistakes.md`.
