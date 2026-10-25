<!-- Tier-2 reviewer 2. agent: sc:reflect-reviewer; persona: qa; requested slot: haiku (alias ANTHROPIC_DEFAULT_HAIKU_MODEL=grok-4.7[1m]); agent-reported model: grok-4.7[1m]; agentId a4f87e29c307e9751. Persisted verbatim by orchestrator. Citations are relative to reviewer-snapshot/root (map: reviewer-snapshot/provenance-manifest.json). -->
# Reflect Reviewer — Deviation Findings

**Reviewer persona**: qa (coverage / acceptance / verification)
**Grounding root**: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root`
**Diff scope**: `changes.patch` (single new-file hunk, `src/greeting.py`); no `base...head` git range in the snapshot
**Timestamp**: 2026-10-24
**Total deviations**: 0
**Model actually running**: grok-4.7[1m] (brief slot haiku; alias resolves to grok-4.7)

T1 is right that the 4-class ledger is empty, and wrong if that is read as acceptance. R-001 and R-002 are statically closed. R-003 is not accepted. Non-empty grounding gaps force `status: partial` and `needs_human_decision: true`. Zero deviation rows is not a pass.

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|----------|----------|---------------|----------------------|----------|
| — | — | — | No 4-class divergence. The only hunk maps to T-101 and T-102 and does not contradict R-001 or R-002. R-003 is unevidenced, which is a Grounding Gap, not Drift or Regression. | `changes.patch:1-9`; `spec.md:6`, `spec.md:9`, `spec.md:12` | — |

Precedence checked (Regression > Drift > Necessary > Authorized). No acceptance-criterion contradiction on the hunk. Drift's "unmapped hunk" signal does not match. No inline rationale is required because nothing departs from R-001/R-002. Verification did not run, so the pytest exit-code table cannot mint a Regression.

## Coverage findings (acceptance lens)

| ID | Location (snapshot) | Class or gap | Signals | Tag |
|----|---------------------|--------------|---------|-----|
| F-001 | `src/greeting.py:4` | none — R-001 adherent (static) | `return f"Hello, {name}!"` yields exactly `Hello, Ada!` for `Ada`. Spec text is `spec.md:6`. Task `completed.md:6` (T-101). Diff-backed `changes.patch:9`. | Grounded |
| F-002 | `src/greeting.py:2-3` | none — R-002 adherent (static) for `""` | `if not name: raise ValueError("name required")`. `not ""` is true, so an empty string raises `ValueError`. Spec requires type, not message (`spec.md:9`). Task `completed.md:7` (T-102). Diff-backed `changes.patch:7-8`. | Grounded |
| F-003 | `tests/test_greeting.py:4-5` and `:8-13` | Grounding Gap (not a 4th-class row) | Both required cases are present in source: `assert greet("Ada") == "Hello, Ada!"` and `greet("")` treated as pass only on `ValueError`. Spec `spec.md:12` says tests MUST exercise those cases. Presence is not execution. File is absent from `changes.patch:1-4` (only `src/greeting.py`). | Grounded for presence and patch absence; exercise result unevidenced |
| F-004 | `completed.md:2` | Grounding Gap | `status: done` with T-101..T-103 all `[x]` (`completed.md:6-8`). Claimed 3/3. Static presence 3/3. Execution evidence 0. A done stamp is not acceptance evidence for R-003. | Grounded |

Static closure of R-001 does not depend on the unexecuted test. The f-string is deterministic. The test at `tests/test_greeting.py:5` is a second, unrun oracle for the same string, not the only evidence.

## T1 challenge (do not treat agreement on the empty ledger as agreement on acceptance)

Agreed, after re-Read:

- Patch body `changes.patch:6-9` matches `src/greeting.py:1-4` exactly. One hunk, one file header (`changes.patch:1-4`).
- T-101/T-102 citations in the T1 card and in `__run_evidence__/artifacts/task-to-diff-map.md:17-18` match the source.
- `greet` is an undecorated function (`src/greeting.py:1`). It is not on the runtime-surface Python allowlist (CLI/HTTP/Click/Typer/route decorators). Empty `runtime_surface_requirements` is correct. Spec has no side-effect or durable-sink requirement (`spec.md:5-12`), so a reachability skip is not a gap.
- Classifying the missing pytest run as Regression would violate the taxonomy: exit 1 is Regression only after a run; no run degrades to a Grounding Gap.

Challenged:

- T1's "no divergence found" (`__run_evidence__/t1-card.md:22`) is ledger-true and acceptance-false. R-003 remains open. QA does not sign the work off.
- T1's "both files are 4 lines" is loose. `src/greeting.py` is 4 lines. `changes.patch` is 10 lines; the identical body is `changes.patch:6-9`, not the `:5-9` range (line 5 is the `@@` header). Byte-identity of the body still holds.
- T1 recommendation 3 (add `tests/__init__.py`) does not fix `from src.greeting import greet` (`tests/test_greeting.py:1`). A tests package marker does not put the project root on `sys.path`. The import works only if that root is already on the path (`python -m pytest` from the fixture root, or an explicit `pythonpath`). Snapshot listing has no `src/__init__.py`, `tests/__init__.py`, `conftest.py`, `pytest.ini`, or `pyproject.toml` (8 snapshot files; none of those). Collection outcome stays `[INFERRED]`. Do not pre-classify it as Drift or Regression. A future plain-pytest exit 2/3 would stay a Grounding Gap under the exit-code table; exit 1 would be Regression; exit 5 would be Drift/coverage; exit 0 would close the exercise gap.

## Grounding gaps

```yaml
- hunk_ref: tests/test_greeting.py:1-13 (no hunk in changes.patch)
  evidence_missing: pytest exit code (verification triangle not run; no verify-logs). No task log. No diff hunk for the test file (changes.patch:1-4 is only src/greeting.py).
  why_not_classifiable: R-003 "exercise" (spec.md:12) is not decidable from presence. Exit 1 would be Regression, exit 5 Drift/coverage, exit 2/3 a further Grounding Gap, exit 0 would close it. None of those codes exists.
  next_evidence_needed: pytest from the fixture project root, both `python -m pytest tests/test_greeting.py` and plain `pytest tests/test_greeting.py`, with exit codes kept. Plus a diff or task-log entry proving tests/test_greeting.py is in the audited change.
  owner: user
  decision_needed_by_user: true
- hunk_ref: completed.md:2 and completed.md:6-8
  evidence_missing: No task log and no self-reported test state behind status done.
  why_not_classifiable: Regression detection degrades to a log claim when verification is unavailable, and there is no claim to compare. The done stamp is not itself a spec contradiction.
  next_evidence_needed: Task log or the verification run above.
  owner: user
  decision_needed_by_user: false
```

Not upgraded to Drift: Drift requires an unmapped diff hunk. T-103 is a task with no hunk, which is missing provenance, not extra work. Not upgraded to Regression: `src/greeting.py:2-4` does not contradict `spec.md:6` or `spec.md:9`, and no previously-passing test has been shown to fail.

## Adherence summary

- Spec units audited: 3 (R-001, R-002, R-003)
- Fully adherent: 2 (R-001, R-002, static)
- Authorized expansion: 0 | Necessary deviation: 0 | Drift: 0 | Regression: 0
- Unclassifiable (grounding gaps, not in the counts above): 1 (R-003 / T-103)
- `regression_present`: false (no exit-1 evidence, no spec contradiction)
- S_dev_density on the diff: 0/1 (the single hunk is mapped). This does not mean requirement acceptance is 100%.

## Risks

| # | Risk | Tag |
|---|------|-----|
| 1 | R-003 can still fail closed as Regression, Drift/coverage, or another gap once pytest actually runs. The empty deviation ledger does not retire that. | Grounded that no run exists (brief verification line; no verify-logs in the snapshot). `[INFERRED]` which exit code would appear. |
| 2 | `from src.greeting import greet` (`tests/test_greeting.py:1`) has no path config in the snapshot. Plain pytest may exit 2 at collection. | Grounded for the import line and for the missing config files (snapshot file list). `[INFERRED]` for the failure mode. |
| 3 | `if not name` (`src/greeting.py:2`) also rejects `None`, `0`, and other falsy values, and it accepts whitespace-only names. Spec R-002 says "empty" only (`spec.md:9`). | Grounded for the condition. `[INFERRED]` that anyone intended those cases. Not a contradiction, not a sibling-symbol correctness gap (`greet` has no sibling). |
| 4 | `test_empty` (`tests/test_greeting.py:8-13`) passes on any `ValueError` and does not use `pytest.raises`. It still matches R-002, which requires the type, not the message `"name required"`. | Grounded. Weaker oracle, not a spec miss. |

No advisory correctness-gap section. The test and `greet` agree on `""` → `ValueError` and on `"Ada"` → `Hello, Ada!`. Spec silence on whitespace and non-strings is not a sibling-contract split.

## Recommendations

1. **File:** none (verifier only). **Change:** from the fixture project root, run `python -m pytest tests/test_greeting.py` and plain `pytest tests/test_greeting.py`; keep both exit codes. **Verifier:** taxonomy table — 0 closes R-003 exercise, 1 is Regression, 2/3 stays a Grounding Gap, 5 is Drift/coverage.
2. **File:** `changes.patch` or a task log. **Change:** put `tests/test_greeting.py` in the audited diff or cite a task-log entry, and stop treating `--scope src/` as covering T-103. **Verifier:** a hunk maps T-103 to `tests/test_greeting.py`.
3. **File:** pytest config at the fixture root (not `tests/__init__.py`). **Change:** only if plain pytest exits 2, set `pythonpath = .` (or equivalent) so `from src.greeting import greet` resolves. Do not treat `tests/__init__.py` as that fix. **Verifier:** plain `pytest` collects 2 tests.
4. **File:** `spec.md` R-002. **Change:** say whether whitespace-only and non-string names are empty. **Verifier:** spec review. Only if the answer is yes, extend `tests/test_greeting.py` and re-run recommendation 1.

## Notes

- Could not verify test execution. The brief states the verification triangle was not run, and the snapshot has no `verify-logs` or task log. That is the R-003 gap, not a skipped Read.
- Reachability and runtime-surface skips were checked against `spec.md` and `runtime-surface.md` §1. They are telemetry skips, not gaps.
- Reuse audit (`__run_evidence__/artifacts/reuse-audit.yaml`) reports `greet` distinct, `S_reuse: 0.0`. No coverage impact.
- Live `audit_repo_root` was not read. Citations are snapshot paths only.

## Self-reported confidence

**0.76**

Static R-001/R-002 adherence, patch/disk identity, and the empty 4-class ledger were re-read from source and are strong. Confidence is capped because R-003 has no execution evidence, the test file has no diff provenance, and the import-collection outcome is inference. The model actually running is grok-4.7[1m].
