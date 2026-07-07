"""Unit tests for mine_learnings — programmatic fixtures, mocked LLM, NO network.

Run: `pytest full/agent/scripts/test_mine_learnings.py` (or from an installed project, `pytest agent/scripts/`).
JSONL dict shapes match Claude Code's real session-transcript shapes.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mine_learnings as ml


# ---------------------------------------------------------------------------
# Fixture builders — JSONL shapes matching real transcripts
# ---------------------------------------------------------------------------

def user_msg(text: str) -> dict:
    """Genuine typed user turn: content is a str, NO toolUseResult, promptSource typed."""
    return {"type": "user", "message": {"role": "user", "content": text},
            "promptSource": "typed"}


def assistant(text: str = "", tool_uses=None) -> dict:
    content = []
    if text:
        content.append({"type": "text", "text": text})
    for tu in (tool_uses or []):
        content.append({"type": "tool_use", "id": tu["id"], "name": tu["name"], "input": {}})
    return {"type": "assistant", "message": {"role": "assistant", "content": content}}


def tool_result(tool_use_id: str, text: str, is_error: bool = False) -> dict:
    """Tool output: role 'user' but carries a tool_result block + toolUseResult key."""
    return {
        "type": "user",
        "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_use_id,
             "content": text, "is_error": is_error},
        ]},
        "toolUseResult": {"stdout": "", "stderr": text},
    }


def meta_user(text: str) -> dict:
    """Slash-command / meta entry: type user but promptSource absent → not a user message."""
    return {"type": "user", "message": {"role": "user", "content": text}}


def write_jsonl(tmp_path: Path, entries: list[dict]) -> Path:
    p = tmp_path / "session.jsonl"
    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in entries),
                 encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# AC1 — correction → 1 candidate with pivot captured
# ---------------------------------------------------------------------------

def test_ac1_correction_with_pivot():
    turns = ml.parse_transcript_entries([
        assistant("I added a field to the schema and deployed"),
        user_msg("no, that's wrong, revert it"),
        assistant("Understood, rolling back the schema change"),
    ])
    corrs = ml.find_corrections(turns)
    assert len(corrs) == 1
    c = corrs[0]
    assert "wrong" in c["correction_text"].lower()
    assert "rolling back" in c["next_assistant_pivot"]
    assert "added a field" in c["prev_assistant_gist"]


# ---------------------------------------------------------------------------
# AC2 — short "redo" correction → 1
# ---------------------------------------------------------------------------

def test_ac2_redo_correction():
    turns = ml.parse_transcript_entries([
        assistant("I deployed to prod"),
        user_msg("undo that, redo it the other way"),
        assistant("Reverting the deploy now"),
    ])
    corrs = ml.find_corrections(turns)
    assert len(corrs) == 1
    assert "redo" in corrs[0]["correction_text"].lower()


# ---------------------------------------------------------------------------
# AC3 — false positives suppressed → 0
# ---------------------------------------------------------------------------

def test_ac3_false_positives_suppressed():
    for phrase in ["no problem, continue", "no worries, keep going",
                   "cannot reproduce, all good", "that's a known issue not a bug"]:
        turns = ml.parse_transcript_entries([
            assistant("did the thing"),
            user_msg(phrase),
        ])
        assert ml.find_corrections(turns) == [], f"false positive on: {phrase}"


def test_ac3_real_correction_with_negative_still_caught():
    # "no problem" suppresses, but a true "that's not right" must survive even if a
    # negative phrase co-occurs.
    turns = ml.parse_transcript_entries([
        assistant("done"),
        user_msg("no problem with the lib, but what you did is not right, redo it"),
    ])
    assert len(ml.find_corrections(turns)) == 1


# ---------------------------------------------------------------------------
# AC4 — repeated tool failure ×2 → 1; ×1 → 0
# ---------------------------------------------------------------------------

def test_ac4_repeated_tool_failure_twice():
    turns = ml.parse_transcript_entries([
        assistant("run it", tool_uses=[{"id": "toolu_1", "name": "Bash"}]),
        tool_result("toolu_1", "ModuleNotFoundError: no such file", is_error=True),
        assistant("retry", tool_uses=[{"id": "toolu_2", "name": "Bash"}]),
        tool_result("toolu_2", "ModuleNotFoundError: no such file", is_error=True),
    ])
    fails = ml.find_repeated_tool_failures(turns)
    assert len(fails) == 1
    assert fails[0]["tool_name"] == "Bash"
    assert fails[0]["count"] == 2


def test_ac4_single_failure_zero():
    turns = ml.parse_transcript_entries([
        assistant("run it", tool_uses=[{"id": "toolu_1", "name": "Bash"}]),
        tool_result("toolu_1", "ModuleNotFoundError: no such file", is_error=True),
    ])
    assert ml.find_repeated_tool_failures(turns) == []


# ---------------------------------------------------------------------------
# AC5 — dedup vs existing heading → dropped
# ---------------------------------------------------------------------------

def test_ac5_dedup_against_existing_heading():
    cand = {"date": "2026-05-03", "title": "stripe webhook url pointed to localhost",
            "trigger": "stripe webhook url pointed to localhost", "wrong": "x",
            "correct": "y", "why": "z", "_source": "correction", "_raw": {}}
    existing = (
        "## 2026-04-28 — Stripe webhook URL pointed to localhost in prod\n"
        "**Wrong:** never reset the env var\n"
    )
    out = ml.dedup([cand], existing)
    assert out == [], "candidate overlapping an existing heading should be dropped"


def test_ac5_dedup_keeps_unrelated():
    cand = {"date": "2026-05-03", "title": "onboarding wizard too many steps",
            "trigger": "onboarding wizard too many steps", "wrong": "x",
            "correct": "y", "why": "z", "_source": "correction", "_raw": {}}
    existing = "## 2026-04-28 — Stripe webhook URL pointed to localhost in prod\n"
    assert len(ml.dedup([cand], existing)) == 1


# ---------------------------------------------------------------------------
# AC6 — format_candidate with stub llm_fn → 6 keys non-empty
# ---------------------------------------------------------------------------

def test_ac6_format_candidate_with_stub_llm():
    raw = {"type": "correction", "prev_assistant_gist": "did X",
           "correction_text": "no, that's wrong", "next_assistant_pivot": "did Y",
           "turn_index": 1}

    def stub_llm(prompt: str) -> str:
        return json.dumps({
            "date": "2026-05-03", "title": "Do Y not X",
            "wrong": "did X", "correct": "did Y",
            "why": "user corrected", "trigger": "when about to do X",
        })

    out = ml.format_candidate(raw, llm_fn=stub_llm)
    for key in ("date", "title", "wrong", "correct", "why", "trigger"):
        assert out.get(key), f"missing/empty key: {key}"


# ---------------------------------------------------------------------------
# AC7 — never writes mistakes.md; queue guard
# ---------------------------------------------------------------------------

def test_ac7_append_guard_rejects_learnings_path(tmp_path):
    bad = tmp_path / "agent" / "memory" / "learnings" / "mistakes.md"
    bad.parent.mkdir(parents=True)
    with pytest.raises(ValueError):
        ml.append_to_queue(bad, "## block\n")
    assert not bad.exists(), "guard must not have created the file"
    # Guard keys on the agent/memory/learnings/ DIR, not the basename: a mistakes.md-named
    # file elsewhere is allowed (pins intent against a future basename-only check).
    ok = tmp_path / "my_mistakes.md"
    ml.append_to_queue(ok, "## block\n")
    assert ok.exists()


def test_ac7_append_writes_queue_and_leaves_mistakes_untouched(tmp_path):
    mistakes = tmp_path / "mistakes_baseline.md"
    mistakes.write_text("## 2026-04-28 — baseline\n", encoding="utf-8")
    before = mistakes.read_bytes()

    queue = tmp_path / "inbox" / "learnings-candidates.md"
    p = ml.append_to_queue(queue, "\n## Session abc — mined now\nbody\n")
    assert p.exists()
    assert "Session abc" in p.read_text(encoding="utf-8")
    # mistakes baseline untouched
    assert mistakes.read_bytes() == before


# ---------------------------------------------------------------------------
# AC8 — --no-llm path: spy NOT called
# ---------------------------------------------------------------------------

def test_ac8_no_llm_does_not_invoke_llm(tmp_path, monkeypatch, capsys):
    calls = []

    def spy(prompt: str) -> str:
        calls.append(prompt)
        return "{}"

    monkeypatch.setattr(ml, "default_llm_fn", spy)

    transcript = write_jsonl(tmp_path, [
        assistant("I deployed to prod"),
        user_msg("no, that's wrong"),
        assistant("reverting"),
    ])
    queue = tmp_path / "queue.md"
    rc = ml.main([
        "--transcript", str(transcript),
        "--no-llm", "--dry-run",
        "--queue", str(queue),
        "--mistakes", str(tmp_path / "nope.md"),
        "--session-id", "test",
    ])
    assert rc == 0
    assert calls == [], "llm spy must NOT be called under --no-llm"
    out = capsys.readouterr().out
    assert "candidates=" in out


# ---------------------------------------------------------------------------
# AC9 — tool_result is NOT a correction (the critical one)
# ---------------------------------------------------------------------------

def test_ac9_tool_result_not_a_correction():
    # role "user" but it's tool output containing a correction-marker word ("no such file").
    turns = ml.parse_transcript_entries([
        assistant("grep it", tool_uses=[{"id": "toolu_x", "name": "Grep"}]),
        tool_result("toolu_x", "fatal: no such file or directory; not found",
                    is_error=True),
    ])
    # NOT seen by the correction detector
    assert ml.find_corrections(turns) == []
    # but IS eligible for the tool-failure stream (one failure → 0, but it's classified)
    tr = [t for t in turns if t.kind == "tool_result"]
    assert len(tr) == 1 and tr[0].is_error


def test_ac9_meta_user_not_a_correction():
    # slash-command / meta entry (promptSource absent) must not count as a user correction
    turns = ml.parse_transcript_entries([
        assistant("did it"),
        meta_user("<command-name>/sync</command-name> no that's not right"),
    ])
    assert ml.find_corrections(turns) == []


# ---------------------------------------------------------------------------
# Classification sanity (user vs tool_result vs assistant)
# ---------------------------------------------------------------------------

def test_classification_kinds():
    turns = ml.parse_transcript_entries([
        user_msg("hello"),
        assistant("hi", tool_uses=[{"id": "t1", "name": "Bash"}]),
        tool_result("t1", "ok", is_error=False),
        meta_user("<local-command-stdout>x</local-command-stdout>"),
    ])
    kinds = [t.kind for t in turns]
    assert kinds == ["user", "assistant", "tool_result", "other"]
