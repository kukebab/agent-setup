# Testing Rules

When to write tests, what they must cover, how they run.

## When tests are REQUIRED

Any change touching one of these → write or update tests **in the same commit**:

| Kind | Example | Why |
|------|---------|-----|
| **Engines / Validators** | core logic many callers depend on | Silent regressions = broken prod |
| **LLM post-processors** | parsing model output, classification | Model output is unstable. Tests pin our interpretation |
| **Dedup / merging logic** | dedup, classifier, conflict resolution | False matches = data corruption |
| **Security boundaries** | upload validation, size caps, allow-lists | Missing tests = attack surface |
| **Schema migrations** | non-trivial RLS, triggers, constraints | At minimum a smoke test hitting the new endpoint |
| **Regex / parsing** | URL matchers, filename parsers, format detectors | One edge case breaks everything |
| **Bugs** | Any fix to a reported issue | Write the failing test first, then fix |

## When tests are OPTIONAL

Skip tests (and say so explicitly) only when:

- One-off scripts (backfills, manual migrations)
- CLI wrappers that just call into a tested module
- Generated files (TypeScript types from schema, fixtures from audits)
- UI / dashboard polish where manual browser check is the real validator

When in doubt → write the test. 5 minutes now vs hours of trust loss later.

## Minimum Coverage Standard

Every tested module needs:

1. **Happy path** — the one-liner "it works" case
2. **At least 2 edge cases** — malformed input, empty input, boundary values, edge characters
3. **Failure modes** — bad input, missing file, network failure
4. **Security guards** — if the module has any (size limits, allow-lists, sanitization), test rejection works

## Fixture Patterns

**Prefer programmatic fixtures over binary files.**

Good:
```python
def _make_doc(texts):
    doc = Document()
    for t in texts: doc.add_paragraph(t)
    return doc
```

Bad:
```python
fixture = open("tests/fixtures/sample.docx", "rb").read()
```

**Why:** binary fixtures rot, bloat the repo, and hide what's being tested. Programmatic fixtures show intent inline.

Binary fixtures OK only when: the format produces edge cases programmatically that are hard to generate (legacy formats, real-world corruption). Check them in with a `README.md` explaining why each one exists.

## Run Isolation

**Default test run must be < 10 seconds with no network.**

- No live API calls in default run. Mark live-API tests with `@pytest.mark.integration` and exclude by default.
- No live DB. Mock at module boundaries.
- Default tests should not require `.env`. Pass dicts directly to functions.

## Naming Conventions

- `test_<module>.py` per module (`test_template_engine.py`, not `test_templates.py`)
- Classes group cases: `class TestRunBoundary:`, `class TestSafeOpen:`
- Method names: `test_<what>_<scenario>` — `test_missing_field_returns_empty`, not `test_missing_data`
- Skip via `@pytest.mark.skip(reason="...")`, not commented-out code

## Anti-Patterns (Never)

- **Testing only happy path.** "It works on my input" is a demo, not a test.
- **One giant test that sets up + runs + checks 10 things.** Split into focused cases.
- **`assert result` without context.** Compare to expected: `assert result == {...}`.
- **Real network in default runs.** Breaks CI, flaky, slow.
- **Copy-paste fixtures into every test.** Factor into a helper or `conftest.py`.
- **Catching exceptions to hide failure.** Let tests fail loudly.
- **Commenting out failing tests to "fix later".** Either fix or delete.

## When tests fail in CI / pre-deploy

Per `quality-gate.md` loop: fix + re-verify up to 3 times. After 3 failed attempts: stop, report root cause, don't keep patching blindly.

**Never deploy with red tests.** If a test is broken but the code is right, fix the test (or mark `skip` with reason) before deploying. A red test rots like commented-out code.
