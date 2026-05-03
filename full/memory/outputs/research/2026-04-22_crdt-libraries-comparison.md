# CRDT Libraries Comparison

**Date:** 2026-04-22
**Author:** AI agent (commissioned by Maya)
**Question:** Should we keep our custom CRDT or migrate to Yjs / Automerge?

## TL;DR

**Stay custom for now.** Migration cost is high (3-4 weeks), and our specific conflict rules don't map cleanly to Yjs/Automerge defaults. Re-evaluate at 1000+ paying users.

## Comparison

| | Our custom | Yjs | Automerge |
|---|---|---|---|
| Maturity | Internal, 6 months | Production at scale (Linear, Notion) | Production-ready |
| Doc size | Small (1-3 KB/op) | Small | Larger (full history) |
| Network format | Custom JSON | Y-protocol binary | Custom (Loro, etc.) |
| Conflict rules | Last-write-wins | LWW per-op | LWW per-op |
| Undo/redo | Not implemented | Built-in | Built-in |
| Offline | Works | Works | Works |
| Migration cost | N/A | 3-4 weeks | 4-5 weeks |

## Why we'd consider migrating

- Undo/redo we'd build ourselves anyway (40 hrs estimate)
- Battle-tested merge logic (we're 1 incident away from another data loss)
- Network format optimized

## Why we'd stay custom

- Our conflict rules (e.g. "structural conflicts → keep both, flag in UI") don't match Yjs defaults
- Already invested 6 months
- Simpler than supporting another dependency

## Recommendation

**Defer.** The right time to re-evaluate is:
1. After we hit 1000+ paying users (more incidents = more pain)
2. Or when we add real-time presence indicators (Yjs makes this easier)

For now, invest in conflict regression test infrastructure (already underway after [[wiki/sync-engine]] iOS Safari incident).

## Sources

- Yjs documentation (raw/2026-04-20_yjs-docs.md)
- Automerge 2.0 announcement (raw/2026-04-21_automerge-2.md)
- Internal sync incident reports
