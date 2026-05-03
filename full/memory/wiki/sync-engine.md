# Sync Engine

> Acme Notes syncs notes across web, desktop, and mobile clients in real time. Built on a custom CRDT-based protocol over WebSocket. Conflict resolution is automatic for non-overlapping edits, last-write-wins for true conflicts.

## Architecture

- **Transport:** WebSocket (custom service in `sync/`)
- **Document model:** CRDT (Conflict-Free Replicated Data Type) — operations commute
- **Reconnection:** exponential backoff, full snapshot resync on disconnects >30 seconds

## Conflict rules

- Non-overlapping edits → merged automatically.
- Concurrent edits to the same paragraph → last-write-wins (timestamp-based).
- Structural conflicts (block deleted vs edited) → keep both, flag in UI for user resolution.

## Known issues

- iOS Safari WebSocket reconnect bug — fixed 2026-05-02 (see `daily/2026-05-02.md` and the post-mortem in `outputs/research/2026-04-22_crdt-libraries-comparison.md`).
- High-frequency edits (>5 ops/sec) can drop ops on slow networks. Backlog item.

## Heavy users (watch closely)

- [[clients/bluefin-coffee]] — 12-person ops team, real-time SOPs across cafes
- [[clients/tessera-studio]] — 8-person agency, real-time client-brief collaboration

## Cross-links

- [[design-partner-program]] — partners drive sync priorities
- [[billing-flows]] — sync features gated behind paid plans (post-launch)

## Sources

- Yjs CRDT design notes (`raw/2026-03-15_yjs-design.md`)
- iOS Safari sync incident report (`raw/2026-05-02_ios-safari-incident.md`)
