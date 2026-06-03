# QA Report — Phase 3 Gate (BoundaryIntegrityGate)

**Topic:** TASK-RF-20260602-sprint-auto-resume — Phase 3 (items 3.1–3.6), BoundaryIntegrityGate
**Date:** 2026-06-02
**Phase:** phase-gate
**Fix cycle:** 1
**Stance:** ADVERSARIAL / zero-trust. Core safety component. Every claim verified by Read + executed logic (`uv run python -c`).
**Target file:** `src/superclaude/cli/sprint/resume/integrity.py` (450 lines)

---

## Verification approach

Every acceptance criterion is attacked with an EXECUTED fixture (real tmp `results/` trees, real
`shutil.copy2`, real `restore_from_bundle`), not by reading code alone. Reused-helper signatures
were read from source (`rerun_tasks.py`, `recovery.py`, `summarizer.py`, `config.py`, `models.py`).

(Sections appended incrementally below.)

---

## Overall Verdict: PASS

The Phase 3 deliverable (`integrity.py`) is correct against all four acceptance criteria and
survives every adversarial attack run as an executed fixture. The two NFR safety invariants
(NFR-1 non-destructive default, NFR-3 advisory-isolation) are proven by snapshot-diff and
mock-driven probes, not by reading code alone. Reversibility is proven by a corrupt-then-restore
round trip through the EXISTING `restore_from_bundle`. One IMPORTANT finding is surfaced — a
PRE-EXISTING, out-of-scope `invoke_haiku` import regression that blocks item 3.6's checkpoint
*command* (not the Phase 3 code) — left unfixed per scope discipline with exact remediation given.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | (3.1) Last-completed double-validation = A ∧ B ∧ artifacts_ok; PASS re-checked not trusted | PASS | Executed: persisted PASS + transcript INCOMPLETE ⇒ `validated_last=False`, lc in suspects, `derived_status=INCOMPLETE`. PASS + missing declared deliverable ⇒ `validated_last=False`, `artifacts_present=False`. Fully-coherent ⇒ True. (`_validate_last_completed`, lines 89-133) |
| 2 | (3.1) Not-validated ⇒ lc in suspects, validated_last False | PASS | Executed (Attack 7): `report.suspects` contains role=last_completed; `report.passed=False` |
| 3 | (3.2) DEFAULT report-only: ZERO `results/` mutation | PASS | Executed (Attack 1): recursive `rglob` sha256 snapshot before==after (3 files, diff=∅); no `.resume-quarantine-*`, no `.recovery-locks` created |
| 4 | (3.2) Partial detected across BOTH classes + stray files; PHASE = whole-phase | PASS | Executed: transcript INCOMPLETE + declared-deliverable-exists + stray `phase-N-task-*` all `found`. `_partial_targets` globs T03.07+T03.08 in PHASE mode (Attack 13) |
| 5 | (3.3) Opt-in quarantine = `shutil.copy2`; ORIGINAL untouched; manifest shape matches | PASS | Executed (Attack 3): copy created under `.resume-quarantine-<ts>/preserved/`, original byte-identical after, manifest `entries:[{task_id,canonical,preserved}]` (superset of restore's `{canonical,preserved}`) |
| 6 | (3.3) Lock acquired; audit line written; reversible by `restore_from_bundle` | PASS | Executed: corrupt original then `restore_from_bundle(qdir, results_dir)` returned 1, original CONTENT restored byte-exact. `.recovery-locks/phase-3.lock` taken + released (no leftover) |
| 7 | (3.3) NEVER rename-in-place / NEVER delete | PASS | Source scan of `_quarantine`: `shutil.copy2` present; `.rename(` / `os.replace` / `shutil.move` / `unlink` / `rmtree` / `os.remove` all ABSENT (Attack 6). Original+copy both exist post-run |
| 8 | (3.4) Coherence read TASK-only, skipped for PHASE | PASS | Executed (Attack 8): PHASE path patches `invoke_sonnet` to raise if called — never raised; `coherence_warnings=[]` |
| 9 | (3.4) Appends to coherence_warnings ONLY; empty verdict ⇒ no-LLM-path identical | PASS | Executed (Attack 2 + 14): SUSPECT verdict ⇒ 1 warning appended, `validated_last`/`passed` UNCHANGED. `_coherence_read` returns `(False,"")` on empty `invoke_sonnet` |
| 10 | (3.5) `passed = accept_suspect or (validated_last and not unresolved_partial)`; pure deterministic | PASS | `_verdict` source = `return report.validated_last and not unresolved_partial` (+ `if accept_suspect: return True`). No coherence/sonnet/haiku/invoke token in body (Attack 2 source scan) |
| 11 | (3.5) coherence_warnings NEVER a term in passed | PASS | Executed: SUSPECT verdict on a deterministically-clean TASK ⇒ `passed=True`. `_advisory_coherence` ordered AFTER `report.passed=` assignment in `run()` (index proof) |
| 12 | (3.5) blocking_reasons populated + actionable on fail | PASS | Executed: fail ⇒ non-empty `blocking_reasons` citing `--start`/`--fresh` |
| 13 | NFR-1: quarantine NEVER reached without `cleanup_opted_in` (even with accept_suspect) | PASS | Executed (Attack 12): `_quarantine` patched to raise; `accept_suspect=True, cleanup_opted_in=False` ⇒ never raised. Source: call inside `if cleanup_opted_in:` |
| 14 | Lock safety: `acquire_recovery_lock` raises ⇒ no mutation, stay report-only | PASS | Executed (Attack 4): patched `acquire_recovery_lock` to raise `ClickException` ⇒ `results/` snapshot unchanged, `quarantined={}` |
| 15 | Lock ALWAYS released (finally) | PASS | `_quarantine` wraps body in `try/.../finally: release_recovery_lock(lock_path)` (lines 250-297). No leftover `.lock` after happy-path run |
| 16 | Double-stash race (DD-3): COPIES never renames ⇒ no collision with `stash_and_restore_deliverables` | PASS | COPY-only proven (check 7); rerun engine's stash also copies — no in-place rename on either side ⇒ no glob collision |
| 17 | Signal B independence: `_classify_transcript` actually called on transcript | PASS | Executed: persisted PASS overridden by transcript-derived INCOMPLETE. Missing transcript ⇒ `''` ⇒ INCOMPLETE ⇒ not validated (strict — see Observations) |
| 18 | PHASE granularity: coherence skipped + last-completed vacuous (no per-task lc) | PASS | Executed (Attack 8): no lc ⇒ `validated_last=True` vacuously; LLM never invoked; partial phase work still surfaced |
| 19 | accept_suspect override proceeds but stays non-destructive | PASS | Executed (Attack 9): `passed=True` with unresolved partial, yet `results/` snapshot unchanged |
| 20 | Reused-helper signatures correct | PASS | Read all 8: `_classify_transcript(text)->TaskStatus`, `_declared_deliverables(tasklist,id)`, `_preserved_dest(root,canon,results)`, `restore_from_bundle(bundle,results)`, `acquire/release_recovery_lock`, `write_recovery_audit_log(path,event)`, `invoke_sonnet(prompt,*,timeout)` |
| 21 | ruff clean | PASS | `ruff check src/superclaude/cli/sprint/resume/integrity.py` → All checks passed; whole `resume/` package clean |

## Summary

- Checks passed: 21 / 21
- Checks failed: 0
- Critical issues: 0
- Important issues: 1 (PRE-EXISTING, out-of-scope — does not affect Phase 3 code)
- Issues fixed in-place: 0 (the one finding is out of Phase 3 scope — see rationale)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT (out-of-scope, pre-existing) | `src/superclaude/cli/sprint/retrospective.py:34,337` + `tests/sprint/test_summarizer.py` + `tests/sprint/test_retrospective.py` | Commit `70ef6486` ("replace haiku defaults with sonnet across codebase") renamed `invoke_haiku`→`invoke_sonnet` in `summarizer.py` but missed `retrospective.py` and two test modules, which still import `invoke_haiku`. This is an ImportError at *collection* time, so item 3.6's checkpoint command `pytest tests/ -k "boundary or integrity or quarantine or coherence"` cannot reach green — it errors before selecting any test. The Phase 3 deliverable itself correctly uses `invoke_sonnet`. | Rename `invoke_haiku`→`invoke_sonnet` in `retrospective.py:34,337` and update the `invoke_haiku` references in `test_summarizer.py` + `test_retrospective.py`. This is a SEPARATE cleanup commit, not a Phase 3 change. With those two modules excluded, the Phase-3 selection runs **63 passed, 4 skipped, 0 failed**. |

## Actions Taken

No in-place fixes applied. Rationale: although `fix_authorization: true`, the single finding lives
entirely OUTSIDE the Phase 3 deliverable (`retrospective.py` + 2 test files, introduced by an
unrelated earlier commit). Per scope discipline (CLAUDE.md Core Rule 8), a Phase 3 safety gate must
not silently mutate unrelated source/test files. The exact remediation is documented above for a
dedicated cleanup commit. The Phase 3 code (`integrity.py`) requires NO changes — it is correct as
written.

## NFR Deep-Dive (the two attack-hardest invariants)

**NFR-3 (advisory isolation) — proven non-influence.** Three independent proofs: (1) runtime —
`invoke_sonnet` mocked to return `"SUSPECT: ..."` on a deterministically-validated TASK left
`validated_last=True` and `passed=True`, with the warning appended; (2) ordering — `run()` calls
`self._advisory_coherence(...)` at line 84, strictly AFTER `report.passed = self._verdict(...)` at
line 71 (index proof `i_adv > i_passed`); (3) data-flow — `_verdict` body references only
`validated_last`, `unresolved_partial`, `accept_suspect`; no `coherence`/`sonnet`/`haiku`/`invoke`
token appears. `_advisory_coherence` mutates only `report.coherence_warnings`. Conclusion: the LLM
verdict CANNOT reach `passed`.

**NFR-1 (non-destructive default) — proven zero mutation.** Recursive sha256 snapshot of `results/`
(via `rglob`, not top-level) before and after a DEFAULT-mode run over seeded partial work
(INCOMPLETE transcript + stray errors file + existing declared deliverable) was byte-identical;
no `.resume-quarantine-*` dir, no `.recovery-locks` dir created. The quarantine path is reachable
ONLY inside `if cleanup_opted_in:` — proven by patching `_quarantine` to raise and confirming
`accept_suspect=True, cleanup_opted_in=False` never triggers it. When the lock is held
(`acquire_recovery_lock` raises), the gate catches and returns report-only with zero mutation.

**Reversibility — proven round-trip.** Opt-in quarantine → corrupt the canonical original →
`restore_from_bundle(qdir, results_dir)` → original byte-content restored (returned count 1).
The gate's manifest (`{entries:[{task_id,canonical,preserved}]}`) is a SUPERSET of what
`restore_from_bundle` reads (`{canonical,preserved}`), and `qdir/preserved/manifest.json` is exactly
the path `restore_from_bundle` expects — no new restore verb required (DD-3 satisfied).

## Observations (non-blocking)

- **Signal B strictness (by design, noted per spawn instruction).** A MISSING last-completed
  transcript yields `''` ⇒ `_classify_transcript` returns INCOMPLETE ⇒ Signal B fails ⇒ the
  last-completed task is treated as suspect and the gate STOPs. This is the *correct, conservative*
  behavior for a safety gate (DD-2 R1: "a PASS claim is re-checked, never trusted" — and absence of
  the corroborating transcript is exactly a failure to corroborate). It could be argued as
  over-strict for a legitimately-completed task whose gitignored transcript was pruned, but the
  STOP is recoverable via `--start`/`--fresh`/`--yes` (accept_suspect), and the blocking_reasons
  explain it. Correct as-is; flagged only for visibility.
- **Design says "Haiku", code uses `invoke_sonnet`.** Not a defect: commit `70ef6486` replaced the
  Haiku default with Sonnet codebase-wide; the design doc's DD-2 "Haiku" wording is stale relative
  to that refactor. The spawn brief explicitly directs reuse of `summarizer.py (invoke_sonnet)`,
  which the code does correctly. The advisory-only contract is model-agnostic.
- `_partial_targets` PHASE branch uses an inline `import re` and tolerant `try/except OSError` — fine.

## Confidence

**Verified:** 21/21 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100.0%**

**Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 9 (incl. 4 executed multi-assertion fixture
scripts totalling 55+ runtime assertions, all green) | tavily_search: 0 | tavily_extract: 0 |
web_search_fallback: 0 | web_fetch_fallback: 0 (no external lookup required — verification was
entirely source-truth + executed local logic).

Tool-engagement minimum satisfied: 23 read/grep/bash-verification calls ≥ 21 checklist items; every
call mapped to a specific check (no padding). The 4 fixture scripts ran 55+ discrete `uv run python`
assertions (NFR-1 snapshot diffs, NFR-3 mock probes, restore round-trip, lock-raise, PHASE skip).

## Recommendations

1. **Phase 3 code: ship as-is.** No changes to `integrity.py` required. All four acceptance gates
   (3.1–3.5) and the 3.6 checkpoint intent (zero mutation / reversible / deterministic verdict) hold.
2. **Before Phase 5 tests land, fix the unrelated `invoke_haiku` regression** (Issue #1) in a
   separate commit so item 3.6's `pytest -k` command can reach green:
   - `src/superclaude/cli/sprint/retrospective.py:34,337`: `invoke_haiku` → `invoke_sonnet`
   - `tests/sprint/test_summarizer.py`, `tests/sprint/test_retrospective.py`: same rename
3. Phase 5 should add the dedicated `test_haiku_coherence_advisory_only` (design §9, DD-2 a/b/c) and
   `test_boundary_quarantine_nondestructive` (FR-2.5) suites — my fixtures prove the behavior but are
   ephemeral; the durable suite is a Phase 5 deliverable (TB-Add item 13: verification must be durable).

## QA Complete

VERDICT: PASS
