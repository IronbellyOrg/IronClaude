# Research Notes: Make CanonicalFixtureParity + brainstorm skill test pass in clean CI

**Date:** 2026-06-04
**Scenario:** A (explicit — fix fully diagnosed in REPORT.md with file:line evidence)
**Depth Tier:** Quick
**Track Count:** 1

Research for this task is supplied pre-verified by the `/sc:troubleshoot` Tier 1 diagnosis
at `.dev/troubleshoot/test-audit-canonical-brainstorm-ci-20260604043148/REPORT.md`
(status: success, confidence 0.96). Every claim below was reproduced by running the tests
and `git check-ignore` during that diagnosis — no re-discovery needed.

---

## EXISTING_FILES

**Audit tests (Bug A — tests are CORRECT, fixtures untracked):**
- `tests/audit/test_slow_shrink_continues.py` — `CANONICAL_LOG` at lines 66-75 → `REPO_ROOT/.dev/releases/complete/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log`; `canonical_log_text` fixture (171-172) is a bare `read_text()` with no skip guard; `TestCanonicalFixtureParity` at 364; `test_canonical_log_present` (371-375) asserts `CANONICAL_LOG.is_file()`.
- `tests/audit/test_monotonicity_halt_F_5_5_5.py` — fixture `D-0056/fixture-F-5-5-5-halt-cycle-2.log` (lines 64-71); `TestCanonicalFixtureParity` at 304.
- `tests/audit/test_synthetic_dnsp_dedup_not_regression.py` — fixtures `D-0059/fixture-cross-cycle-dedup-shrinking.log` (87-89) + `D-0059/fixture-cross-cycle-dedup-non-shrink.log` (98-100); `TestCanonicalFixtureParity` at 446.
- `tests/audit/test_regression_halt_pass1_fail2.py` — fixtures `D-0057/fixture-pass1-fail2-shrinking.log` (79-81) + `D-0057/fixture-pass1-fail2-non-shrinking.log` (90-92); `TestCanonicalFixtureParity` at 417.

**6 canonical fixtures (exist on disk, tracked=N, all under `.dev/releases/complete/task-builder-merge/artifacts/`):**
- D-0056/fixture-F-5-5-5-halt-cycle-2.log
- D-0057/fixture-pass1-fail2-shrinking.log
- D-0057/fixture-pass1-fail2-non-shrinking.log
- D-0059/fixture-cross-cycle-dedup-shrinking.log
- D-0059/fixture-cross-cycle-dedup-non-shrink.log
- D-0060/fixture-slow-shrink-F-5-4.log

**`.gitignore`** — line 79 `*.log` is the blanket rule catching all 6 fixtures (confirmed via `git check-ignore -v` → `.gitignore:79:*.log`). Comment near line 231 already documents that `.dev/releases/` artifacts are meant to be tracked.

**Brainstorm test (Bug B — test is WRONG):**
- `tests/cli_portify/test_brainstorm_gaps.py:24-30` — imports `check_brainstorm_skill_available` into the test module namespace (local binding).
- `tests/cli_portify/test_brainstorm_gaps.py:82-89` — `TestSkillAvailability::test_skill_not_available_returns_false` patches `…brainstorm_gaps.check_brainstorm_skill_available` (module attr) then calls the LOCAL name → patch is a no-op; real function runs.
- `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py:52-62` — `check_brainstorm_skill_available()` reads `Path(os.path.expanduser("~/.claude/skills"))` and returns True if `sc-brainstorm` or `sc-brainstorm-protocol` dir exists → environment-coupled.

## PATTERNS_AND_CONVENTIONS

- `.dev/releases/**` artifacts are tracked by project policy (`.gitignore` comment ~L231); the blanket `*.log` (L79) is the only thing excluding these specific fixtures. Negation `!.dev/releases/**/artifacts/**/fixture-*.log` re-includes them (VERIFIED: `git check-ignore` reports the 6 fixtures UN-IGNORED, while `twine.log` and `.dev/releases/**/results/phase-*-output.txt` stay ignored).
- Hermetic pytest pattern: use `monkeypatch.setenv("HOME", str(tmp_path))` to redirect `os.path.expanduser("~")`; CI is Linux so `HOME` is authoritative for `expanduser`.
- CI runs BOTH `ruff check` AND `ruff format --check src/ tests/` separately (per project memory — `make lint` only does the former).
- ABSOLUTE: never stage `.claude/` paths. These fixtures are `.dev/` — staging is permitted and policy-aligned.

## GAPS_AND_QUESTIONS

None — fix fully specified and reproduced.

## RECOMMENDED_OUTPUTS

A single-track MDTM task file (template 02) with phases:
1. Fix A — .gitignore negation + verify un-ignore/no-leak
2. Fix A — stage + commit the 6 fixtures; run the 27 parity tests
3. Fix B — rewrite the hermetic test + add companion present-case test; run brainstorm skill tests
4. Validation — full ruff check + ruff format --check + targeted test runs; confirm no `.claude/` staged
5. Completion

## SUGGESTED_PHASES

See RECOMMENDED_OUTPUTS. Bug A and Bug B are independent but small — single track, sequential phases.

## TEMPLATE_NOTES

Template 02 (complex) per the `--fix` chain request (>3 files). Most files are data-fixture `git add`s, not code edits — granularity should still give each logical change its own item (gitignore edit, fixture commit, each test rewrite).

## AMBIGUITIES_FOR_USER

None — intent is clear from the REPORT.md and reproduced evidence.
