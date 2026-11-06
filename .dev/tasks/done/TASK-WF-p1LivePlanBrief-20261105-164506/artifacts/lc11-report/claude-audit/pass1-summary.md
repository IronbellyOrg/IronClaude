# Pass 1 Summary - Surface Scan of tests/pr_submit

**Date Range**: 2026-11-05 to 2026-11-05
**Total Batches**: 2
**Total Files Audited**: 81 / 81 in scope
**Coverage**: 100%
**Command**: `/sc:cleanup-audit tests/pr_submit --pass surface --unattended --report-dir .dev/p1-live/cleanup-audit/`

---

## Aggregate Summary

| Category | Count | % of Total |
|----------|-------|-----------|
| DELETE | 0 | 0% |
| REVIEW (Need Decision) | 5 | 6.2% |
| KEEP | 76 | 93.8% |
| **Total** | **81** | **100%** |

Add-to-.gitignore suggestions: 0. Wiring-flagged files (`REVIEW:wiring`): 0.

## What needs a person's decision (the 5 REVIEW items)

Five fixture files in `tests/pr_submit/fixtures/` are never loaded by any test. Each is named only in a comment or docstring (and in `.dev/` planning documents), and the comments say a later phase would swap them in for inline test data. That swap was never done.

| Fixture | Mentioned only at |
|---|---|
| `review-clean.json` | `test_detection_contract.py:10, 51, 59` |
| `review-with-findings.json` | `test_detection_contract.py:11, 71` |
| `review-non-augment.json` | `test_detection_contract.py:11, 292` |
| `review-interleaved.json` | `test_detection_contract.py:12, 321` |
| `rereview-then-decline.json` | `test_loop_guard.py:152` (docstring) |

Decision for a person: wire each into its test (the comments say that was the plan), or remove it. None is classed DELETE because comments and plans still point at them, and the audit rules require zero references for DELETE.

---

## Coverage Metrics

- **Files in scope**: 81 (from `repo-inventory.sh` run on `tests/pr_submit`; 43 `.py`, 37 `.json`, 1 `.z`)
- **Files audited**: 81 (50 in batch 1, 31 in batch 2)
- **Coverage percentage**: 100%
- **Files not reached**: 0
- **Default exclusions applied**: hidden paths, BMAD directories, `.claude-audit/` (none removed any file under `tests/pr_submit`)
- **Project exclusions applied**: (none; no `.claude-audit/SCOPE.md`)

---

## Cross-Agent Patterns

### Pattern 1: Planned-but-unwired fixtures

- **Observed in**: Batch 1
- **Description**: Four fixtures are named in `test_detection_contract.py` comments of the form `# Phase 10: swap for load_fixture("...")`; the fifth is named in a `test_loop_guard.py` docstring. The tests still use inline data.
- **Impact**: Five unused JSON files; the tests they were meant to feed do not use them.
- **Recommendation**: Wire or remove (see the table above).

### Pattern 2: Every `test_*.py` file is collected by pytest

- **Observed in**: Batches 1 and 2 (collection); a recorded passing run was cited for the batch 2 files only
- **Description**: `pyproject.toml:107-111` collects `tests/**/test_*.py`. The log `.dev/tasks/issue-302-handoff/pre-pr/full-pytest-rebased.log` shows passing results for the batch 2 files.
- **Impact**: No dead test modules found.
- **Recommendation**: None.

---

## Validation Results (Spot-Check)

- **Findings spot-checked**: 8 claims, covering all 5 REVIEW fixtures plus a sample of KEEP citations (10% sampling rule: 5 per 50 files gives 8 for 81 files)
- **Result**: 7 CONFIRMED, 1 PARTIAL, 0 REFUTED
- **Discrepancy details**: the partial was in the orchestrator's own grouped line list for the four `review-*` fixtures (it omitted `test_detection_contract.py:12` and grouped `review-interleaved.json` under line 11). The batch 1 report itself cites `:12` for `review-interleaved.json` and `:11` for the other two, so the report is correct. The finding that none of the four is loaded was confirmed.
- **Validation status**: PASS
- **Validator limits**: the validator was given the claims and told to try to refute them; it reran its own greps. It did not re-check all 76 KEEP citations.

---

## Deduplication Notes

No finding appeared in more than one batch.

---

## Quality Gate Status

| Gate | Status | Evidence |
|------|--------|---------|
| All batches complete | PASS | 2/2 batches completed |
| Required sections present | PASS | Safe to Delete, Need Decision, Keep, Add to .gitignore, Remaining, Summary in both reports |
| Mandatory profiles complete | N/A | Per-file profiles are a Pass 2 requirement |
| Spot-check validation | PASS | 0 refuted of 8 |
| Coverage threshold met | PASS | 81/81 = 100% |

**Overall Pass Status**: PASS

---

## Batch Reports Index

| Batch | Agent | Files | Status | Report Path |
|-------|-------|-------|--------|-------------|
| 1 | audit-scanner | 50 | Complete | `.claude-audit/pass1/batch-01.md` |
| 2 | audit-scanner | 31 | Complete | `.claude-audit/pass1/batch-02.md` |

---

## Notes for Next Pass and for the tool owners

- Next pass (if run): the five REVIEW fixtures need no structural audit; they need the wire-or-remove decision. `test_gate_helper_differentials.py` defines a module-level `HELPER_TEST_MAP` that its docstring calls "the enforced registry" and that `conftest.py` imports; the scanner did not flag it (name does not match the `*_REGISTRY` suffix list), but Pass 2 could look at it.
- Tool defect seen: `repo-inventory.sh` prints `[batch-1]` for all 81 files in its "BATCH ASSIGNMENTS" section even though its own summary says 2 batches. The batch counter is updated inside a piped `while` loop, which runs in a subshell, so the increment is lost. This run sharded the files by hand from the sorted in-scope list (`.claude-audit/pass1/batch-01-files.txt`, `batch-02-files.txt`). Not fixed here: the audit is read-only.
- Tool constraint seen: `audit-scanner` has only Read, Grep and Glob, so it cannot write its own batch report; the orchestrator wrote both reports from the scanners' returned text. The protocol text says agents write their reports to disk.
- Date: the scanners' and validator's clock reads differed by a day in one header (2026-11-06 vs the session's 2026-11-05); the session date is used.
- Nothing in the repository was modified by the audit. Outputs: `.claude-audit/` and `.dev/p1-live/cleanup-audit/return-contract.yaml`.
