# QA Report — PG-1 (Test Scaffolding Correctness)

**Topic:** PG-1 — Phase 2 test scaffolding correctness gate
**Date:** 2026-05-22
**Phase:** task-integrity (gate PG-1)
**Fix cycle:** N/A (fix_authorization: false)
**Adversarial stance:** Assume errors present until disproven by tool evidence.

---

## Scope

Verify Phase 2 items 2.1–2.5 of `TASK-RF-20260522-153212` against PG-1 acceptance criteria:

1. Each Phase 2 test pins the RIGHT invariant (T3, T5-inverted, T5b, T6).
2. Each Phase 2 test FAILS today for the RIGHT reason (RED baseline matches intent).
3. No surface-area drift outside the 3 expected test files (no `src/` edits).
4. Phase 2 Findings document both pre-existing issues honestly (Step 2.4 + Step 2.5 entries).

---

## Verification Log

### Tool engagement summary
- Read: 6 (input summary, RED baseline txt, test_eval_run.py [3 ranges], test_scratch_root_allowlist.py [full], test_coverage_gate.py [T3 region], task file Phase 2 block)
- Grep / Bash-grep: 9 (`_resolve_executor_factory` in T6, `monkeypatch.` in T6, `CliRunner()` count, `allowlisted_output_dir` fixture definition, Phase 2 checklist `[x]` status, phase heading map, git status / diff scope, mtime stat, ruff/verify-sync exit-code capture)
- Bash other: 4 (git status, git diff --name-only, git log on the two src/ doc files, click version check)

---

## Criterion 1 — Each Phase 2 test pins the RIGHT invariant

### 1a. T3 — `test_coverage_gate_fails_on_corrupt_settings_json`
**File:** `tests/cli/eval/test_coverage_gate.py:320-332`
- Docstring (L321): "FR-G5 / spec H2 — corrupt settings.json MUST fail closed." ✓ references FR-G5 + H2.
- Fixture: `(tmp_path: Path) -> None` — uses `tmp_path` only. ✓
- Corrupt JSON write: `bad.write_text("{not json", encoding="utf-8")` (L330). ✓ literal `{not json` payload.
- Assertion: `assert result.passed is False` (L332). ✓ exact required shape.
- **VERDICT: PASS**

### 1b. T5 inverted — `test_resolve_scratch_root_rejects_bare_prefix`
**File:** `tests/cli/eval/test_scratch_root_allowlist.py:52-64`
- Docstring (L53): "Spec H4 — the bare allowlist prefix itself MUST be rejected." ✓ references H4.
- Docstring further references OQ-1 / Step 2.2 and explains tautology-foot-gun rationale. ✓
- Idiom: `with pytest.raises(ScratchRootViolation):` (L63). ✓
- Argument: `resolve_scratch_root("/tmp/eval-runs")` (L64). ✓ literal bare-prefix string.
- INVERT-IN-PLACE check: the old `test_accepts_tmp_eval_runs_root_itself` no longer exists in the file (`grep -n "test_accepts_tmp_eval_runs_root_itself"` returns no hits). ✓
- **VERDICT: PASS**

### 1c. T5b positive — `test_accepts_immediate_subdir_of_allowlist_root`
**File:** `tests/cli/eval/test_scratch_root_allowlist.py:67-78`
- Docstring (L68): "Spec H4 acceptance criterion #2 — `/tmp/eval-runs/x` passes." ✓ references H4 acceptance #2 verbatim.
- Argument: `target = Path("/tmp/eval-runs/x")` (L76), `resolve_scratch_root(target)` (L77). ✓
- Assertion is non-exception positive shape: `assert resolved == target.resolve()` (L78). ✓
- No fixture / no monkeypatch (bare `def test_...`). ✓
- Acknowledges "May be GREEN today … MUST remain GREEN after Phase 3 Step 3.1" — matches PG-1 spec language. ✓
- **VERDICT: PASS**

### 1d. T6 — `test_run_emits_warning_when_null_lifecycle_executor_active`
**File:** `tests/cli/eval/test_eval_run.py:621-656`
- Docstring (L624): "Spec M2 — `_NullLifecycleExecutor` MUST emit a stderr WARNING when active." ✓ references M2 + observability gap.
- Signature: `(clean_claude_home: Path, allowlisted_output_dir: Path)` — uses `allowlisted_output_dir` fixture. ✓ Fixture definition confirmed at `tests/cli/eval/conftest.py:25`. ✓
- `CliRunner()` zero-arg (L639). ✓ Click 8.3.2 installed (verified via `uv pip show click`), which separates stderr by default (no `mix_stderr` needed); the recent commit `08183738` mentions the Click 8.3.2 mix_stderr alignment, so `result.stderr` is the genuine err channel.
- Assertion: `assert "NullLifecycleExecutor" in (result.stderr or "")` (L656). ✓ exact required shape with `None`-safe fallback.
- **No monkeypatch on `_resolve_executor_factory`** — verified via `grep -n "_resolve_executor_factory\|monkeypatch\." tests/cli/eval/test_eval_run.py`. Only three hits: L105 (Path.home patch in fixture), L186 (RunOrchestrator patch in a different test), L627 (docstring mention of the symbol name in T6, not a setattr). No `monkeypatch.setattr` / `monkeypatch.setitem` references the factory. ✓
- **VERDICT: PASS**

---

## Criterion 2 — Each Phase 2 test FAILS today for the RIGHT reason

Source: `phase-outputs/test-results/02-pytest-red-baseline.txt` (3 collected, 3 failed, 0 passed).

| Test | Required failure reason | Observed failure reason | Match? |
|------|------------------------|-------------------------|--------|
| T3 | `passed=True` returned on corrupt JSON | `assert True is False ... CoverageResult(...).passed` (L24-26) | ✓ |
| T5 | `DID NOT RAISE ScratchRootViolation` | `Failed: DID NOT RAISE <class 'superclaude.cli.eval.config.ScratchRootViolation'>` (L29-31) | ✓ |
| T6 | empty stderr (no NullLifecycleExecutor warning) | `assert 'NullLifecycleExecutor' in (('' or '')) ... <Result okay>.stderr` (L33-36) | ✓ |

T5b is intentionally NOT in the RED baseline (it MAY be GREEN today per the spec); the baseline correctly targets only the three RED tests.

**Note on captured `EXIT_CODE=0` (FALSE-CLEAN):** The baseline file shows `EXIT_CODE=0` at L44 despite pytest's visible non-zero exit (3 failed). This is a `tee`-pipe artifact (without `set -o pipefail`, `$?` captures `tee`'s exit, not pytest's). The substantive RED contract is satisfied — pytest's own summary line shows `3 failed in 0.25s` — and this idiom issue is honestly logged in the Step 2.4 Findings entry with a concrete remediation (`set -o pipefail` or `${PIPESTATUS[0]}`). Surfaced as **MINOR** observability finding rather than a PG-1 blocker because the substance is correct.

**VERDICT: PASS** (all 3 RED tests fail for the right reason).

---

## Criterion 3 — No surface-area drift outside the 3 expected test files

Command: `git diff --name-only HEAD -- src/superclaude/cli/eval/ tests/cli/eval/`

Result:
```
src/superclaude/cli/eval/pty/PROVENANCE.md
src/superclaude/cli/eval/suites/README.md
tests/cli/eval/test_coverage_gate.py
tests/cli/eval/test_scratch_root_allowlist.py
```
Plus untracked: `tests/cli/eval/test_eval_run.py` (genuinely new file authored by Step 2.3).

**Literal-text failure of criterion 3:** PG-1's text says "Run `git diff --name-only HEAD -- src/superclaude/cli/eval/` and confirm zero hits." The command returns 2 hits, NOT zero.

**Investigation — are these Phase 2-introduced?**
- `mtime(src/superclaude/cli/eval/pty/PROVENANCE.md)` = 2026-05-21 19:36:10
- `mtime(src/superclaude/cli/eval/suites/README.md)` = 2026-05-21 19:36:09
- `mtime(tests/cli/eval/test_eval_run.py)` = 2026-05-22 17:16:37 (Phase 2 authoring window)
- `mtime(TASK-RF-20260522-153212.md)` = 2026-05-22 17:19:32

The two `src/` doc files were modified **~22 hours BEFORE** the Phase 2 test file authoring and are NOT in the Phase 2 test-files diff captured in `phase-outputs/reviews/PG-1-input-summary.md` (which only shows the two test-file diffs). Diff content is cosmetic markdown only:
- PROVENANCE.md: bare URL wrapped in angle brackets (MD034 markdownlint fix).
- suites/README.md: blank lines added around a fenced code block (MD031 fix).

Both are markdownlint cosmetic fixes consistent with the recently-landed `.markdownlint.json` (commit `5d71ae5e`), authored well before Phase 2 began. **The drift exists in the working tree at PG-1 time but was NOT introduced by Phase 2.**

**RESOLUTION:** Criterion 3 as literally written would FAIL on these 2 hits. However:
1. The two changed files are cosmetic-only documentation under `src/superclaude/cli/eval/` (no Python source code modified — `git diff --name-only HEAD -- src/superclaude/cli/eval/ '*.py'` returns zero).
2. They predate Phase 2 by ~22 hours and are not in Phase 2's working-set diff.
3. Spec intent ("no source-code drift while landing test scaffolding") is satisfied — the Phase 2 contract was test-only edits, and that contract held.

**VERDICT: PASS WITH IMPORTANT NOTE.** The literal grep returns 2 hits, but both are pre-Phase-2 markdownlint cosmetic edits to docs under `src/superclaude/cli/eval/`, NOT Phase 2-introduced source drift. Spec intent satisfied. Recommend amending the criterion 3 command in future gate prompts to `git diff --name-only HEAD -- 'src/superclaude/cli/eval/**/*.py'` to exclude pre-existing doc churn from triggering a false positive.

---

## Criterion 4 — Phase 2 Findings honestly documents BOTH pre-existing issues

**File:** `TASK-RF-20260522-153212.md:542-550` (`### Phase 2 — Test Scaffolding Findings`)

### Entry A — Step 2.4 substantive PASS / EXIT_CODE FALSE-CLEAN (lines ~544-545)
- ✓ Identifies "All 3 RED tests fail for the RIGHT reasons" with per-test reasoning (T3 silent-green, T5 accept-branch live, T6 no warning).
- ✓ Names the `tee`-pipe shell idiom as the cause of false `EXIT_CODE=0` (captures `tee`'s exit, not pytest's).
- ✓ Recommends `set -o pipefail` OR `${PIPESTATUS[0]}` as the durable fix.
- ✓ Marked "Logged for PG-1 attention" — honest, scoped, non-blame.

### Entry B — Step 2.5 partial PASS with TWO pre-existing-state issues (lines ~547-550)
- ✓ Issue 1 (ruff scope expansion): names 8 pre-existing F401s in 7 unrelated test files (test_capability_classifications, test_capability_gates [2], test_expect_exit_code, test_no_pty_exclusion, test_pty_lifecycle, test_reporter, test_retention_policy). The 02-ruff.txt file confirms exactly these 8 F401s. ✓
- ✓ Explicitly states "Phase 2's edits introduce ZERO ruff debt" with the scoped re-run evidence (T3/T5/T6 files + src/cli/eval/ → "All checks passed!").
- ✓ Offers three remediation options (a/b/c) rather than auto-fixing — respects scope discipline.
- ✓ Issue 2 (sc-troubleshoot drift): describes the regen on `refs/report-template.md` after a prior `make sync-dev` and proposes periodic re-sync. The 02-verify-sync.txt confirms the drift ("⚠️  DIFFERS: sc-troubleshoot-protocol" at L162-163).
- ✓ Both issues framed as pre-existing / not-introduced-by-Phase-2, with concrete follow-up rather than blame.

**VERDICT: PASS.** Both findings are present, honest, evidence-backed, and recommend follow-up rather than auto-fixing out-of-scope debt.

---

## Confidence Gate

- **Checklist items:** 4 criteria, each with sub-criteria → 8 effective verification points (T3, T5, T5b, T6, RED-reason match, surface drift, Findings-A, Findings-B).
- **Verified [x]:** 8 / 8 — every point has tool-cited evidence (Read line ranges, grep hit counts, baseline txt line numbers, mtime values, git diff output).
- **Unverifiable [?]:** 0.
- **Unchecked [ ]:** 0.
- **Confidence:** 8 / (8 - 0) = 100% — eligible for PASS.
- **Tool engagement:** Read=6 / Grep+Bash-grep=9 / Bash-other=4 = 19 tool calls vs. 8 verification points (2.4× engagement, well above the 1× floor — every check has at least one dedicated tool call).

Self-audit: "If I told the user I found 0 issues, would they believe me?" — I found 2 issues (criterion 3 literal-text drift, plus the EXIT_CODE FALSE-CLEAN observation), both surfaced with evidence. I am NOT issuing a "0 issues found" verdict.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT (NOTE) | `git diff -- src/superclaude/cli/eval/` returns 2 hits (PROVENANCE.md + suites/README.md) | PG-1 criterion 3 literally says "zero hits". The 2 hits are pre-Phase-2 markdownlint cosmetic doc edits (mtime 2026-05-21, before Phase 2's 2026-05-22 17:16 test edits), NOT source drift introduced by Phase 2. Spec intent (no source-code drift) is satisfied. | Amend criterion 3's diff command to `git diff --name-only HEAD -- 'src/superclaude/cli/eval/**/*.py'` OR commit the cosmetic doc edits before re-running PG-1 in future. NOT a Phase 2 defect. |
| 2 | MINOR | `phase-outputs/test-results/02-pytest-red-baseline.txt:44` captures `EXIT_CODE=0` despite pytest's visible `3 failed` | Shell idiom `... | tee file; echo EXIT_CODE=$?` captures `tee`'s exit, not pytest's. Substantive RED contract IS satisfied (pytest summary line shows 3 failed). Already logged in Phase 2 Findings Entry A. | Future verification idioms should use `set -o pipefail` before the pipe OR `${PIPESTATUS[0]}` to capture upstream exit. Honest logging already recorded; no remediation required at PG-1. |

Neither issue blocks PG-1; both are documentation / shell-idiom hygiene, not test-scaffolding correctness defects.

---

## Per-Test PASS/FAIL Table

| Test | Intended invariant | Docstring refs | Right structure? | Fails for right reason today? | Verdict |
|------|--------------------|----------------|------------------|-------------------------------|---------|
| T3 `test_coverage_gate_fails_on_corrupt_settings_json` | corrupt settings.json fails closed (FR-G5 / H2) | FR-G5, H2 ✓ | `tmp_path` only, `{not json` payload, `passed is False` ✓ | `assert True is False` on `CoverageResult(passed=True)` ✓ | **PASS** |
| T5 `test_resolve_scratch_root_rejects_bare_prefix` (inverted) | bare allowlist prefix rejected (H4) | H4 ✓ | `pytest.raises(ScratchRootViolation)` on literal `"/tmp/eval-runs"` ✓; old test name fully removed ✓ | `DID NOT RAISE ScratchRootViolation` ✓ | **PASS** |
| T5b `test_accepts_immediate_subdir_of_allowlist_root` | strict sub-paths still accepted (H4 acceptance #2) | H4 acceptance #2 ✓ | positive shape, `/tmp/eval-runs/x` arg, no fixture ✓ | not in RED baseline (intentional — MAY be GREEN today) | **PASS** |
| T6 `test_run_emits_warning_when_null_lifecycle_executor_active` | NullLifecycleExecutor stderr warning (M2) | M2, observability gap ✓ | CliRunner() zero-arg + `allowlisted_output_dir` + `assert "NullLifecycleExecutor" in (result.stderr or "")` ✓; NO monkeypatch on `_resolve_executor_factory` ✓ | empty stderr today ✓ | **PASS** |

---

## Summary

- Checks passed: 4 / 4 PG-1 criteria.
- Checks failed: 0.
- Critical issues: 0.
- Important issues: 1 (criterion 3 literal-text drift; not a Phase 2 defect).
- Minor issues: 1 (EXIT_CODE FALSE-CLEAN shell idiom; already logged honestly in Phase 2 Findings).
- Issues fixed in-place: 0 (`fix_authorization: false`).

## Recommendations

1. Proceed to Phase 3 (correctness fixes — H4, H2, M2 etc.). RED baseline is locked and the three tests pin the right invariants.
2. Before Phase 3 commits the source fixes, decide on the disposition of the two pre-existing src/ doc drifts (PROVENANCE.md, suites/README.md): either commit them in a separate "chore(markdownlint): MD031/MD034 cleanup" commit OR amend PG-1's diff scope to Python files only in the next iteration.
3. Carry the `set -o pipefail` / `${PIPESTATUS[0]}` recommendation into Phase 4+ verification idioms so future EXIT_CODE captures are honest.
4. Hold the 8 pre-existing F401 cleanup as a separate cleanup task (per Step 2.5 Findings option (c)).
5. If `sc-troubleshoot-protocol` drift re-appears after Phase 3 source edits, re-run `make sync-dev` once and investigate whether a session hook is the cause.

---

## VERDICT: **PASS**

All four PG-1 acceptance criteria are satisfied. The 3 RED tests pin the right invariants (T3 / T5-inverted / T6) and the positive companion (T5b) is structurally correct; all three RED tests fail today for the right reasons in `02-pytest-red-baseline.txt`; the Phase 2 working-set is test-files-only (the 2 src/ doc-only hits in `git diff` predate Phase 2 by ~22 hours and are cosmetic markdownlint fixes, not Phase 2 source drift); and the Phase 2 Findings section honestly documents BOTH pre-existing issues (Step 2.4 EXIT_CODE shell-idiom, Step 2.5 8× F401 + sc-troubleshoot drift regen) with concrete follow-up recommendations and scope discipline.

**No unfixable issues. Green light to proceed to Phase 3.**

## QA Complete
