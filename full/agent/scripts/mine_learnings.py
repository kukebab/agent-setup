"""Mine an AI coding-session transcript for candidate learnings → review queue.

Detects (a) user-correction turns + the assistant's pivot, (b) repeated tool failures.
Writes CANDIDATES to agent/memory/inbox/learnings-candidates.md ONLY — never to agent/memory/learnings/.
Promotion to mistakes.md is human-in-the-loop via the /mine-learnings skill.

Pure, testable functions + a thin argparse CLI. No network at import time, and `--no-llm`
runs with zero setup. The transcript format targeted here is Claude Code's JSONL session log
(`~/.claude/projects/<encoded-cwd>/<session>.jsonl`); for other tools, pass `--transcript PATH`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE = REPO_ROOT / "agent/memory/inbox/learnings-candidates.md"
DEFAULT_MISTAKES = REPO_ROOT / "agent/memory/learnings/mistakes.md"


def claude_transcript_dir() -> Path:
    """Best-effort path to Claude Code's transcript dir for the current project.

    Claude Code encodes the absolute project path into the dir name by replacing every
    non-alphanumeric character with '-' (e.g. `/Users/me/My Project` → `-Users-me-My-Project`).
    Other tools store transcripts elsewhere — use `--transcript PATH` for those.
    """
    encoded = re.sub(r"[^A-Za-z0-9]", "-", str(REPO_ROOT))
    return Path.home() / ".claude/projects" / encoded


# Correction markers. Recall-favoring (output is a reviewed queue, so false positives are cheap).
# ADD YOUR OWN LANGUAGE HERE — these are English defaults; append markers for whatever language
# you actually correct your agent in (the queue is reviewed by a human, so over-matching is fine).
CORRECTION_MARKERS = [
    r"\bwrong\b", r"\bnot\s+that\b", r"\bnot\s+right\b", r"\bincorrect\b",
    r"\bredo\b", r"\bundo\b", r"\brevert\b", r"\broll\s+it\s+back\b",
    r"\bdon'?t\s+do\b", r"\bthat'?s\s+not\b", r"\bstop\b", r"\bnope\b",
    r"\bno\b", r"\bnot\s+what\s+i\b",
]
# Phrase-level negatives — drop the match if the turn is really one of these.
NEGATIVE_PHRASES = [
    r"no\s+problem", r"\bcannot\b", r"known\s+issue",
    r"stop\s*word", r"no\s+such\s+file", r"no\s+worries",
]
ERROR_RE = re.compile(
    r"error|failed|traceback|exit code [1-9]|no such|not found|exception", re.I
)

_MARKER_RES = [re.compile(p, re.I | re.U) for p in CORRECTION_MARKERS]
_NEGATIVE_RES = [re.compile(p, re.I | re.U) for p in NEGATIVE_PHRASES]


@dataclass
class Turn:
    idx: int
    kind: str  # "user" | "assistant" | "tool_result" | "other"
    text: str = ""
    tool_uses: list = field(default_factory=list)  # [{"id","name"}]
    tool_use_id: str = ""
    is_error: bool = False


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _flatten_content(content) -> str:
    """tool_result content may be a str OR a list of {type:text,text} blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                parts.append(str(b.get("text", "")))
            else:
                parts.append(str(b))
        return " ".join(p for p in parts if p)
    return ""


def _classify_entry(entry: dict, idx: int) -> Turn:
    """Map one JSONL entry to a Turn with a TRUE kind.

    Genuine user turn: type=="user" AND content is str AND toolUseResult absent
    AND promptSource=="typed". A tool_result (role:"user" but tool output) → kind=tool_result.
    """
    entry_type = entry.get("type", "")
    msg = entry.get("message", {}) or {}
    content = msg.get("content", "")

    if entry_type == "assistant":
        texts = []
        tool_uses = []
        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                bt = block.get("type", "")
                if bt == "text":
                    texts.append(block.get("text", ""))
                elif bt == "tool_use":
                    tool_uses.append(
                        {"id": block.get("id", ""), "name": block.get("name", "")}
                    )
        elif isinstance(content, str):
            texts.append(content)
        return Turn(idx=idx, kind="assistant", text=" ".join(texts).strip(),
                    tool_uses=tool_uses)

    if entry_type == "user":
        # tool_result: role "user" but it's tool OUTPUT, never a user correction.
        # Assumption (holds in real transcripts): typed user turns always have str content,
        # so list content here is tool output, not a typed message.
        if entry.get("toolUseResult") is not None or isinstance(content, list):
            tool_use_id = ""
            is_error = False
            text = ""
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        tool_use_id = block.get("tool_use_id", "")
                        is_error = bool(block.get("is_error", False))
                        text = _flatten_content(block.get("content", ""))
                        break
                else:
                    text = _flatten_content(content)
            else:
                text = _flatten_content(content)
            return Turn(idx=idx, kind="tool_result", text=text,
                        tool_use_id=tool_use_id, is_error=is_error)

        # Genuine user turn: str content + typed prompt.
        if isinstance(content, str) and entry.get("promptSource") == "typed":
            return Turn(idx=idx, kind="user", text=content)

        # slash-command / meta turns (promptSource None/absent) → not a user message.
        return Turn(idx=idx, kind="other", text=content if isinstance(content, str) else "")

    return Turn(idx=idx, kind="other")


def parse_transcript_entries(entries: list[dict]) -> list[Turn]:
    """Classify a list of already-parsed JSONL dicts → Turns. In-memory helper (tests)."""
    return [_classify_entry(e, i) for i, e in enumerate(entries) if isinstance(e, dict)]


def parse_transcript(path) -> list[Turn]:
    """JSONL → ordered Turns. Skips unparseable lines (never crashes)."""
    p = Path(path)
    if not p.exists():
        return []
    turns: list[Turn] = []
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(entry, dict):
            continue
        turns.append(_classify_entry(entry, i))
    return turns


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def _matches_marker(text: str) -> bool:
    if any(rx.search(text) for rx in _NEGATIVE_RES):
        # phrase-level negative present — only suppress if it accounts for the match.
        # Strip the negative phrases, re-test markers on the remainder.
        stripped = text
        for rx in _NEGATIVE_RES:
            stripped = rx.sub(" ", stripped)
        return any(rx.search(stripped) for rx in _MARKER_RES)
    return any(rx.search(text) for rx in _MARKER_RES)


def _prev_assistant_gist(turns: list[Turn], idx: int) -> str:
    for j in range(idx - 1, -1, -1):
        if turns[j].kind == "assistant" and turns[j].text:
            return turns[j].text[:300]
    return ""


def _next_assistant_pivot(turns: list[Turn], idx: int) -> str:
    for j in range(idx + 1, len(turns)):
        if turns[j].kind == "assistant" and turns[j].text:
            return turns[j].text[:300]
    return ""


def find_corrections(turns: list[Turn]) -> list[dict]:
    """Over kind=='user' turns ONLY. Marker match AND not a pure negative phrase."""
    out = []
    for i, t in enumerate(turns):
        if t.kind != "user" or not t.text.strip():
            continue
        if not _matches_marker(t.text):
            continue
        out.append({
            "type": "correction",
            "prev_assistant_gist": _prev_assistant_gist(turns, i),
            "correction_text": t.text.strip()[:600],
            "next_assistant_pivot": _next_assistant_pivot(turns, i),
            "turn_index": t.idx,
        })
    return out


def _error_class(text: str) -> str:
    """Cheap bucket for an error string so identical failures group together."""
    text = (text or "").lower()
    for key in ("traceback", "modulenotfounderror", "no such file", "not found",
                "permission denied", "timeout", "connection", "syntaxerror",
                "command not found", "exit code"):
        if key in text:
            return key
    m = ERROR_RE.search(text)
    if m:
        return m.group(0).lower()
    return "unknown"


def find_repeated_tool_failures(turns: list[Turn]) -> list[dict]:
    """Over kind=='tool_result' with is_error. Group by (name, error-class); >=2 → candidate."""
    id_to_name: dict[str, str] = {}
    for t in turns:
        if t.kind == "assistant":
            for tu in t.tool_uses:
                if tu.get("id"):
                    id_to_name[tu["id"]] = tu.get("name", "?")

    groups: dict[tuple, dict] = {}
    for t in turns:
        if t.kind != "tool_result" or not t.is_error:
            continue
        name = id_to_name.get(t.tool_use_id, "?")
        ecls = _error_class(t.text)
        key = (name, ecls)
        g = groups.setdefault(
            key, {"name": name, "error_class": ecls, "count": 0, "samples": []}
        )
        g["count"] += 1
        if len(g["samples"]) < 2:
            g["samples"].append((t.text or "").strip()[:300])

    out = []
    for (name, ecls), g in groups.items():
        if g["count"] >= 2:
            out.append({
                "type": "tool_failure",
                "tool_name": name,
                "error_class": ecls,
                "count": g["count"],
                "samples": g["samples"],
            })
    return out


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def default_llm_fn(prompt: str) -> str:
    """Optional polishing pass via OpenRouter (Haiku by default). Network only here.

    Requires `OPENROUTER_API_KEY`. Model override: `MINE_LLM_MODEL`. Run with `--no-llm`
    to skip this entirely (zero setup, raw candidates).
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
    r = client.chat.completions.create(
        model=os.environ.get("MINE_LLM_MODEL", "anthropic/claude-haiku-4.5"),
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content or ""


def _offline_candidate(raw: dict) -> dict:
    """Raw/offline candidate — no network. Title = first 60 chars of the signal."""
    date = datetime.now().strftime("%Y-%m-%d")
    if raw.get("type") == "correction":
        ctext = raw.get("correction_text", "").strip()
        title = (ctext[:60] or "correction").strip()
        return {
            "date": date,
            "title": title,
            "wrong": raw.get("prev_assistant_gist", "") or "(assistant action before correction)",
            "correct": raw.get("next_assistant_pivot", "") or "(assistant pivot after correction)",
            "why": "User pushed back: " + ctext,
            "trigger": title,
            "_source": "correction",
            "_raw": raw,
        }
    # tool_failure
    name = raw.get("tool_name", "?")
    ecls = raw.get("error_class", "?")
    cnt = raw.get("count", 0)
    title = f"{name} repeated failure: {ecls}"[:60]
    sample = (raw.get("samples") or [""])[0]
    return {
        "date": date,
        "title": title,
        "wrong": f"Ran {name} that failed with '{ecls}' {cnt}× without changing approach.",
        "correct": "After the same tool fails twice, diagnose root cause / switch approach before retrying.",
        "why": f"Repeated identical failure ({cnt}×). Sample: {sample}",
        "trigger": f"{name} {ecls}",
        "_source": "tool_failure",
        "_raw": raw,
    }


_LLM_PROMPT = """You convert a raw AI coding-session signal into a single learnings entry.
Return ONLY valid JSON with EXACTLY these keys (all non-empty strings):
{{"date":"{date}","title":"short imperative title <=70 chars","wrong":"what the AI did wrong",
"correct":"what it should have done","why":"the reason","trigger":"when to recall this lesson"}}

Raw signal (JSON):
{raw_json}
"""


def format_candidate(raw: dict, llm_fn=None) -> dict:
    """Format a raw signal into the 6-key mistakes.md schema.

    llm_fn is None  → offline candidate (NO network — tests rely on this).
    llm_fn provided → ask it for JSON; fall back to offline on any parse failure.
    """
    if llm_fn is None:
        return _offline_candidate(raw)

    date = datetime.now().strftime("%Y-%m-%d")
    prompt = _LLM_PROMPT.format(date=date, raw_json=json.dumps(raw, ensure_ascii=False))
    try:
        resp = llm_fn(prompt) or ""
        if "```" in resp:
            m = re.search(r"```(?:json)?\s*(.*?)```", resp, re.DOTALL)
            if m:
                resp = m.group(1)
        data = json.loads(resp)
        out = {
            "date": (str(data.get("date") or date)).strip(),
            "title": str(data.get("title", "")).strip(),
            "wrong": str(data.get("wrong", "")).strip(),
            "correct": str(data.get("correct", "")).strip(),
            "why": str(data.get("why", "")).strip(),
            "trigger": str(data.get("trigger", "")).strip(),
            "_source": raw.get("type", "correction"),
            "_raw": raw,
        }
        if all(out[k] for k in ("title", "wrong", "correct", "why", "trigger")):
            return out
    except (json.JSONDecodeError, ValueError, TypeError, KeyError):
        pass
    return _offline_candidate(raw)


# ---------------------------------------------------------------------------
# Dedup
# ---------------------------------------------------------------------------

_DATE_PREFIX = re.compile(r"^\s*\d{4}-\d{2}-\d{2}\s*[—\-–]\s*")
_TOKEN_RE = re.compile(r"[a-zA-Zа-яёА-ЯЁ0-9]+", re.U)
_TEMPLATE_HEADINGS = {
    "mistakes",
    "short title",
    "wins",
    "patterns",
}


def _norm_heading(h: str) -> str:
    """Strip '## ', leading 'YYYY-MM-DD —', lowercase."""
    h = h.strip()
    if h.startswith("## "):
        h = h[3:]
    elif h.startswith("##"):
        h = h[2:]
    h = _DATE_PREFIX.sub("", h)
    return h.strip().lower()


def _tokens(s: str) -> set:
    return {t for t in _TOKEN_RE.findall((s or "").lower()) if len(t) > 2}


def _overlap(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _existing_norm_headings(existing_mistakes_text: str) -> list[set]:
    out = []
    for line in (existing_mistakes_text or "").splitlines():
        if not line.startswith("## "):
            continue
        norm = _norm_heading(line)
        if not norm or norm in _TEMPLATE_HEADINGS:
            continue
        out.append(_tokens(norm))
    return out


def dedup(candidates: list[dict], existing_mistakes_text: str,
          queued_text: str = "", threshold: float = 0.6) -> list[dict]:
    """Token-overlap dedup (no LLM) vs existing mistakes.md headings + already-queued."""
    existing = _existing_norm_headings(existing_mistakes_text)
    existing += _existing_norm_headings(queued_text)
    kept: list[dict] = []
    for c in candidates:
        cand_tokens = _tokens(c.get("title", "")) | _tokens(c.get("trigger", ""))
        dup = False
        for ex in existing:
            if _overlap(cand_tokens, ex) >= threshold:
                dup = True
                break
        if not dup:
            # also dedup within this batch
            for k in kept:
                ktok = _tokens(k.get("title", "")) | _tokens(k.get("trigger", ""))
                if _overlap(cand_tokens, ktok) >= threshold:
                    dup = True
                    break
        if not dup:
            kept.append(c)
            existing.append(cand_tokens)
    return kept


# ---------------------------------------------------------------------------
# Rendering + writing
# ---------------------------------------------------------------------------

QUEUE_HEADER = """# Learnings candidates — review queue

Populated by `/mine-learnings` (engine: `agent/scripts/mine_learnings.py`). Each entry below is a
**CANDIDATE** mined from a session transcript — NOT an approved learning. Nothing here is
auto-promoted. You review each via `/mine-learnings`: PROMOTE → `agent/memory/learnings/mistakes.md`
(or `patterns.md`), or DISCARD. The miner writes ONLY to this file; it never touches
`agent/memory/learnings/`.
"""


def render_queue_md(candidates: list[dict], session_id: str, now=None) -> str:
    now = now or datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M")
    lines = [f"\n## Session {session_id or '?'} — mined {ts}", ""]
    if not candidates:
        lines.append("_No candidates detected._")
        lines.append("")
        return "\n".join(lines)
    for i, c in enumerate(candidates, 1):
        src = c.get("_source", "?")
        lines.append(f"### Candidate {i} [{src}] — {c.get('title','')}")
        lines.append(f"- **date:** {c.get('date','')}")
        lines.append(f"- **Wrong:** {c.get('wrong','')}")
        lines.append(f"- **Correct:** {c.get('correct','')}")
        lines.append(f"- **Why:** {c.get('why','')}")
        lines.append(f"- **Trigger:** {c.get('trigger','')}")
        lines.append(f"- _status:_ PENDING (PROMOTE → mistakes.md / patterns.md / DISCARD)")
        lines.append("")
    return "\n".join(lines)


def append_to_queue(queue_path, md: str) -> Path:
    p = Path(queue_path).resolve()
    if "agent/memory/learnings" in p.as_posix():  # HARD GUARD — never write curated learnings.
        raise ValueError(f"refusing to write learnings file: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(QUEUE_HEADER + md, encoding="utf-8")
    else:
        with p.open("a", encoding="utf-8") as f:
            f.write(md)
    return p


def find_latest_transcript() -> Path | None:
    d = claude_transcript_dir()
    if not d.exists():
        return None
    jsonls = sorted(
        d.glob("*.jsonl"),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )
    return jsonls[0] if jsonls else None


def _load_env():
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Mine a session transcript for candidate learnings.")
    ap.add_argument("--transcript", help="path to a transcript JSONL (default: newest Claude Code session for this project)")
    ap.add_argument("--session-id", help="session id label for the queue block")
    ap.add_argument("--no-llm", action="store_true", help="skip the LLM formatting pass (offline, zero setup)")
    ap.add_argument("--dry-run", action="store_true", help="print, do not write the queue")
    ap.add_argument("--queue", default=str(DEFAULT_QUEUE), help="queue file path")
    ap.add_argument("--mistakes", default=str(DEFAULT_MISTAKES), help="existing mistakes.md (for dedup)")
    args = ap.parse_args(argv)

    transcript = Path(args.transcript) if args.transcript else find_latest_transcript()
    if not transcript or not Path(transcript).exists():
        print("[mine] no transcript found — pass --transcript PATH "
              "(Claude Code logs live in ~/.claude/projects/<encoded-cwd>/)")
        return 1

    session_id = args.session_id or Path(transcript).stem

    turns = parse_transcript(transcript)
    raws = find_corrections(turns) + find_repeated_tool_failures(turns)

    llm_fn = None
    if not args.no_llm:
        _load_env()
        llm_fn = default_llm_fn

    candidates = [format_candidate(r, llm_fn=llm_fn) for r in raws]

    mistakes_text = ""
    mp = Path(args.mistakes)
    if mp.exists():
        mistakes_text = mp.read_text(encoding="utf-8", errors="replace")

    queued_text = ""
    qp = Path(args.queue)
    if qp.exists():
        queued_text = qp.read_text(encoding="utf-8", errors="replace")

    candidates = dedup(candidates, mistakes_text, queued_text)

    md = render_queue_md(candidates, session_id)

    n_corr = sum(1 for r in raws if r["type"] == "correction")
    n_fail = sum(1 for r in raws if r["type"] == "tool_failure")
    print(f"[mine] transcript={Path(transcript).name} turns={len(turns)} "
          f"corrections={n_corr} tool_failures={n_fail} → candidates={len(candidates)} "
          f"(llm={'off' if args.no_llm else 'on'})")
    print(md)

    if args.dry_run:
        print("[mine] --dry-run: not written")
        return 0

    written = append_to_queue(args.queue, md)
    print(f"[mine] appended to {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
