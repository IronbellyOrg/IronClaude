# QA Report — Task Integrity (Structure + Phase Ordering Lens)

**Topic:** Differential backtest harness (troubleshoot hardening evals E1-E5)
**Date:** 2026-06-11
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Template:** 02

---

## Overall Verdict: PASS (with 3 MINOR + 1 IMPORTANT advisory notes)

The task file is structurally sound. Phase ordering, dependency ordering, anti-orphaning,
POST-reflect placement, frontmatter completeness, and the SHA tables are all correct and
independently verified against git history and the authoritative research/08 reconciliation.
One IMPORTANT placeholder defect (`{EXECUTOR_CLASS}` unresolved in the reflect command) and
three MINOR notes are recorded below. None block execution, but the IMPORTANT one should be
resolved before the POST-reflect item runs.

---

## Items Reviewed (Phase-Structure Lens + TB-Add Gate)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete + spec_path set | PASS | spec_path (L18) → real 51902-byte RELEASE-SPEC (verified exists); id/title/status/created/type/template_schema_doc/tracks-equiv all present + non-empty; reflect_pre block (L19-26) + reflect_post:"" (L27) present |
| 2 | All mandatory template-02 sections present | PASS | Task Overview, Key Objectives, Prerequisites, Execution Context, Detailed Task Instructions, 6 Phases, Risks & Assumptions, Open Questions, Task Log (grep of `^## ` L59-525) |
| 3 | Phase dependencies logical + match research ORDER 1-5 | PASS | P1 setup → P2 git-replay helper → P3 ReplayExecutor+report → P4 per-escape runners → P5 pytest wiring; maps to ORDER setup→skeleton→helper→runner→report→wiring (report model in P3 precedes its P4.8 consumer) |
| 4 | Helper/report before consumers; OLD=MISS before NEW=CATCH | PASS | P3 model(3.2)→writer(3.3)→schema(3.4)→tests(3.5-3.6); P4 guard(4.1)→path(4.2)→runners(4.3-4.7)→aggregation(4.8); each runner sub-step (a)=OLD=MISS precedes (b)=NEW=CATCH `requires_impl_ref` |
| 5 | Completion items inside final phase (anti-orphaning) | PASS | Step 6.5 (status→Done) is the last item (L508) inside Phase 6 (L460) |
| 6 | POST reflect penultimate, SELF-RUN, git add -A | PASS | Step 6.4 (L502/504) penultimate before 6.5 Done; spawns reflect subagent, records {verdict,run_id,report}→reflect_post; explicit "NOT a human-handoff/HALT"; preceded by `git add -A`; uses merge-base diff (dogfoods the E5 fix) |
| 7 | Task Log section at bottom | PASS | `## Task Log / Notes` (L525) + Execution Log + 6 Phase Findings subsections (L527-545) |
| 8 | Item count reasonable (~77/6) | PASS | exactly 77 items / 6 phases (grep `^- [ ]`) |
| 9 | Open Questions / gaps documented | PASS | OQ-1 (impl-refs-not-landed → NEW=CATCH skips by design), OQ-2 (E4 fix b97c9960 UNMERGED → pin parent 1b0264f1) L522-523 |
| 10 | QA gates follow MDTM M3 + M4 | PASS | per-gate: 7 report-only lens (fix_authz:false) → 1 fix agent (fix_authz:true) → 2 verify; 6 total fix agents (P2,P3,P4,P5,6.2.5,6.3.2); M4 fidelity gate 6.3 with 2 agents |
| 11 | TB-Add-1: no TBD/TODO/FIXME, no title-only | PASS* | only "TODO" hit (L474) is the substring "no placeholder/TODO remains" inside a QA lens description — a meta-reference, not a placeholder token. See IMPORTANT-1 for `{EXECUTOR_CLASS}` |
| 12 | TB-Add-3: blocked items reference blocking OQ | PASS | OQ-1/OQ-2 are designed-skip / informational, not hard blockers; NEW=CATCH skip-guard is encoded structurally (requires_impl_ref), not as a blocked item awaiting an OQ resolution |
| 13 | TB-Add-4: item-to-item deps form a DAG | PASS | each item reads only earlier-created files (P2 helper → P2 tests; P3 model → P3 writer/tests; P4 guard → P4 runners → P4.8 agg); no back-reference to a later item |
| 14 | TB-Add-5: XL/multi-file items split | MINOR | longest items ~2500 chars (Step 3.2 L258, Step 2.1 L196); each scopes ONE file, but 3.2 creates EscapeResult+CatchRateReport+derive+post_init in one item (borderline multi-symbol). See MINOR-1 |
| 15 | TB-Add-6: uniform Verify: prefix + Acceptance Criteria | MINOR | 0 `Verify:` prefixes / 0 `Acceptance Criteria`; this RF template-02 dialect embeds verification in each item's "ensuring..." clause — consistent across all 77 items, but no distinct verification field. See MINOR-2 |
| 16 | TB-Add-7: Source areas reappear; block has no file:line | PASS | all 5 escape callables (_build_file_args, _check_parallel_instructions, gate_passed, _evaluate_gate, POST-reflect) reappear in item bodies; Execution Context span L106-161 has 0 `path:NN` refs |
| 17 | TB-Add-8: per-item Context file:line OR evidence-absence | PASS | items cite concrete file:line (e.g. `process.py` L17, `runner.py:136-156`, `models.py:835-946`); new-file-creation items carry the target path (evidence-absence implicit) |

---

## SHA Table Cross-Validation (independent git verification)

Although outside the strict phase-structure lens, the SHA tables are load-bearing for phase
correctness, so I verified them against live git history (zero-trust):

| Escape | fix_sha | claimed parent | `git rev-parse fix^` | Match |
|--------|---------|----------------|----------------------|-------|
| E1 | 7601ad25 | 94d5baa0 | 94d5baa0 | ✓ |
| E2 | e97aa4fd | 10723863 | 10723863 | ✓ |
| E3 | eb9a2633 | e97aa4fd | e97aa4fd | ✓ |
| E4 | b97c9960 (UNMERGED) | 1b0264f1 | 1b0264f1 | ✓ |
| E5 | 10723863 | d878bc6d | d878bc6d | ✓ |

- The apparent "two different tables" (G1 Key-Constraint L125 vs Step 1.4/2.1) is NOT a
  contradiction: G1 lists only PARENT shas (consistent); Steps 1.4/2.1 add the FIX shas, which
  form an interleaved chain (E5 fix `10723863` = E2 parent; E2 fix `e97aa4fd` = E3 parent).
  research/08 L56-64 explicitly documents and confirms this interleaving.
- `b97c9960` (E4 fix) confirmed UNMERGED into master; `20693bb8` (the HEAD heal) exists and is
  distinct — the E4 pin to parent `1b0264f1` (NOT HEAD) is correct.
- G1 no-caret rule is enforced (checkout target = bare parent, no `^`); the double-decrement
  hazard (`94d5baa0^` = ac80f176) is correctly called out.

VERDICT on SHA tables: internally consistent + git-verified. No defect.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| IMPORTANT-1 | IMPORTANT | Step 6.4 (L504) | The reflect command contains the literal unresolved placeholder `--executor-model {EXECUTOR_CLASS}`. The item also says "the spec + tasklist paths are passed verbatim" — so `{EXECUTOR_CLASS}` would be passed verbatim as a literal, which is not a valid model name and will make the reflect spawn fail or mis-route. | Resolve `{EXECUTOR_CLASS}` to a concrete executor-model class (e.g. `sonnet`/`opus`/`haiku`) consistent with the I22 standard-intensity executor, OR drop the `--executor-model` flag to use the reflect default. |
| MINOR-1 | MINOR | Step 3.2 (L258) | Borderline atomicity: one item creates EscapeResult + CatchRateReport + `_derive_backtest_status` + `__post_init__` (multi-symbol, ~2524 chars). Executable but dense. | Optionally split into 3.2a (EscapeResult) and 3.2b (CatchRateReport + derive + post_init). Not blocking — all live in one file `catch_rate.py`. |
| MINOR-2 | MINOR | whole file | No `Verify:` prefix or `Acceptance Criteria` field (TB-Add-6). Verification is embedded in each item's "ensuring..." clause. | Consistent across all items, so acceptable for this RF B2 dialect; flagged only for cross-skill TB-Add-6 alignment. No action required unless the consuming gate mandates the literal `Verify:` token. |
| MINOR-3 | MINOR | Phase 4 (4.3-4.7) | All 5 per-escape OLD=MISS tests are "real-git replay, CI-skip-guarded" → on CI's shallow clone they ALL skip, so the per-escape negative witnesses give ZERO CI coverage (only the P2 subprocess-mock + P3 schema tests run unconditionally on CI). | Documented in Risks (G2) + OQ-1, and reconciled by the "green = passes-or-correctly-skips" definition, so not a defect of the task file. Noted so the executor does not mistake the local-only OLD=MISS coverage for CI coverage. |

---

## Confidence Gate

- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 8
  - Note: Read calls cover the full task file (3 paginated reads) + this report. The 8 Bash
    calls carried the grep/git-verify load; each maps to a specific checklist item or SHA-row
    verification (item counts, phase ordering, SHA git-verify, placeholder scan, source-area
    reappearance, format/Task-Log, QA-structure). Every TB-Add/structure check has a dedicated
    evidence line above; no item is unverified.

## Actions Taken

None — fix_authorization: false (report-only).

## Recommendations

1. Resolve IMPORTANT-1 (`{EXECUTOR_CLASS}` placeholder in Step 6.4) before the POST-reflect item
   executes — substitute a concrete model class or drop the flag.
2. MINOR-1/2/3 are advisory; no change required to pass the structure/phase-ordering gate.

---

## VERDICT: PASS

Structure and phase ordering are correct and git-verified. One IMPORTANT placeholder defect
(`{EXECUTOR_CLASS}`) and three MINOR advisory notes recorded; none block execution, but
IMPORTANT-1 should be resolved before Step 6.4 runs.

## QA Complete
