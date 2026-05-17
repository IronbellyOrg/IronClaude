# Research Notes: PR4 — Test fixture repair (tests/audit/ failures)

**Date:** 2026-05-17
**Scenario:** A (explicit)
**Depth Tier:** Standard (per-test triage required)
**Track Count:** 5 (this is track 4)
**Order:** PR1 → PR2 → PR3 → PR4 → PR5

---

## EXISTING_FILES

Worked example from BUILD_REQUEST:
- `src/superclaude/cli/audit/credential_scanner.py:18-49` — `_SECRET_PATTERNS` list; `generic_api_key` requires `[A-Za-z0-9_\-]{20,}` (≥20 chars).
- `tests/audit/test_credential_scanner.py:17-26` — `FIXTURE_CONTENT` includes `api_key = "FAKEAPIKEY"` (10 chars). Pattern cannot match → `result.real_secret_count == 2` (only `aws_access_key` + `generic_password`) → `assert result.real_secret_count >= 3` fails.
- Evidence file: `.dev/releases/complete/v3.7-turnledger-integration/v3.7-TurnLedger-Validation/tasklist/artifacts/D-0045/evidence.md:27-31` confirms PRE-EXISTING since v3.0 commit `f4d9035`.

Other failures from PR #35 CI run on Python 3.10 (job `76365604444`): the failure summary file shows additional `tests/audit/*` failures beyond the one worked example. The task file must include a discovery phase that enumerates ALL failing tests with classification.

## PATTERNS_AND_CONVENTIONS

- Tests in `tests/audit/` follow pytest class-based grouping: `class TestScanContent` etc.
- Fixture content is module-level (`FIXTURE_CONTENT = """..."""`) — straightforward to edit.
- The project does NOT have `conftest.py` autoload patterns that would surprise a fixture editor.
- `@pytest.mark.xfail(strict=True, reason="…")` is the project's idiom for "known broken, will fail loud if fixed accidentally" (used in e.g. tests/cli_portify/ where flaky cases occur).

## GAPS_AND_QUESTIONS

- **Full failure inventory unknown**: Need a discovery phase that runs `uv run pytest tests/audit/ -v` after PR1+PR2+PR3 land (so noise is reduced) and enumerates every failing test with: test path, assertion, classification (fixture-short / scanner-wrong / env-dependent / flaky).
- **xfail vs fixture fix**: Default action is fixture fix (matches user choice in /sc:brainstorm Q3). xfail is fallback for genuinely non-fixture-fixable failures.
- **Follow-up issue for xfail cases**: NFR4 says escalate to `/sc:task --compliance strict` if >20 distinct failures. The task file must include a sub-step: "if xfail count > N, open a GitHub issue listing each xfail with link to scanner code and a recommendation."

## RECOMMENDED_OUTPUTS

- Branch: `fix/ci-rot-pr4-test-fixture-repair`
- Single task file: `TASK-RF-track-4-20260517-032112.md`
- PR title: `fix(tests): repair tests/audit/ fixtures + xfail genuinely-broken cases`

## SUGGESTED_PHASES

1. Preparation: confirm PR1+PR2+PR3 merged + branch + dev-deps
2. Discovery: full `pytest tests/audit/ -v` failure inventory with classification table
3. Execute: per-failure fix
   - 3.1 Fix `test_credential_scanner.py` FIXTURE_CONTENT (worked example — api_key 10→≥20 chars)
   - 3.2 For each other fixture-short failure: lengthen fixture values
   - 3.3 For each scanner-wrong failure (if any): xfail + open issue
   - 3.4 For each env-dependent failure (if any): triage — fixture-pin or xfail
4. Verify: `pytest tests/audit/ -v` reports 0 failed/0 errors (xfail/xpass acceptable); AC3 satisfied
5. Commit + PR with in-line comment demonstrating the credential-scanner worked example (AC6)

## TEMPLATE_NOTES

- Template 02 (complex) — discovery before fix
- QA_GATE_REQUIREMENTS: PER_PHASE (after discovery, after each fix batch, final)
- VALIDATION_REQUIREMENTS: pytest tests/audit/ -v passes; full src/ test suite still passes (NFR2 transitivity)
- TESTING_REQUIREMENTS: UNIT (this PR fixes existing tests; no new tests beyond the fixture edits)

## AMBIGUITIES_FOR_USER

- **Follow-up issue threshold**: NFR4 says ">20 distinct test failures" triggers escalation. Document in task: if discovery shows >20 distinct failures, halt and split into sub-PRs by failure class. Default proceeds in-PR if ≤20.

---
**Status:** Complete
