# QA Report — Research Gate

**Topic:** Corrective MDTM task for sprint auto-resume reflection findings F-3/F-2/F-4 + spec contradiction CG-4
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS

The 5 research files are evidence-dense, every load-bearing claim independently re-verified against source, [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags correctly applied, the F-3 AC-4-vs-AC-5 tension and the F-4 planner/integrity co-dependency are both correctly identified and consistently propagated across files. No gaps of any severity that block the task builder. Two MINOR observations recorded below (neither blocks the build).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Evidence density (file:line, fn names) | PASS | Every claim in all 5 files carries a `file:line` or function anchor. Spot-checks below all confirmed against source. |
| 2 | drift.py confidence branches (177-187 same-ID ⇒ 0.9) | PASS | Read drift.py:1-282. Branch `178-187` returns `confidence=0.9, cosmetic_only=True` on identical ID set; branch `130-140` (PHASE/no-baseline) also 0.9; `142-155` removed_completed ⇒ 0.3; `157-175` added/removed_pending ⇒ 0.85; `107-126` parse-fail ⇒ 0.3. Table in research-01 §1 is exact. |
| 3 | drift only reaches Tier1 after Tier-0 hash miss | PASS | drift.py:46-59: Tier 0 returns 1.0 on exact match; only falls to `_tier1` on miss. Research-01's "hash already proved content changed" reasoning is sound. |
| 4 | _annotate_git never sets confidence (NFR-3) | PASS | drift.py:218-265: mutates only `changed_paths` + `tier`; never `confidence`. `git --ignore-all-space` at :249 is inside Tier-2 advisory only. Confirms research-01 §4/§6 NFR-3 claim. |
| 5 | integrity.py:314 `passed` verdict = `accept_suspect or validated_last` | PASS | integrity.py:306-314 verbatim `return accept_suspect or report.validated_last`. No partial-work term. Confirms research-02 §4 + research-05 §1b [CODE-CONTRADICTED]. |
| 6 | _detect_partial L134 returns list[Path], dropped on report-only | PASS | integrity.py:134-173 returns `sorted(found)` (set[Path]). Caller :63-67 forwards to `_quarantine` ONLY when `cleanup_opted_in`; else paths dropped. Confirms research-02/03 F-2 root cause. |
| 7 | _surface_partial L198 appends BoundaryTask only, no paths | PASS | integrity.py:197-208: appends a `BoundaryTask` (no path field) to `report.suspects`; return value discarded by caller (:65). Exact. |
| 8 | models.py BoundaryReport — NO partial-paths field | PASS | models.py:84-101: exactly 6 fields (`validated_last`, `suspects`, `quarantined`, `passed`, `blocking_reasons`, `coherence_warnings`). No partial-paths field. BoundaryTask (37-53) has no path field. Confirms research-02 §3 + research-05 §3a. |
| 9 | planner.py:158-169 PHASE hard-crash ⇒ boundary_tasks==[] | PASS | planner.py:158-169 verbatim: no task_results + empty `derived` ⇒ `granularity=PHASE`, `boundary==[]`, `_assign_roles([])` no-op. Confirms research-03 §1.3 / research-05 §4c. |
| 10 | commands.py:498 _print_resume_decision prints paths only via quarantined | PASS | commands.py:498-536: only path-printing loop is `r.quarantined.items()` (:533-534); empty on report-only. Call sites :293 (dry-run), :441 (interactive) both report-only (run(plan) at :400, no kwargs). Confirms research-03 §3. |
| 11 | F-3 data-availability claim (result.json only status + whole-file sha) | PASS | executor.py:2069-2078 payload: `task_results` (per-task status dicts) + `tasklist_sha256` (whole-file, `_content_sha256_excluding_rerun_block(phase.file)`). NO per-task content hash, NO checkpoint/deliverable baseline. Confirms research-01 §3 CRITICAL claim. |
| 12 | extract_checkpoint_paths parses CURRENT file only | PASS | checkpoints.py:40-98: reads `phase_file.read_text` (the given/current file). No baseline diff possible. Confirms research-01 §3 data-availability blocker. |
| 13 | research-05 CG-4 spec contradiction is real | PASS | design.md:293 `passed=True` (quarantine "if opted in"); design.md:186 `passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)`; merged-req:85-87 FR-2.4 requires (a) cleaned-or-accepted AND (b) doubly-validated. Both cite FR-2.4. Contradiction confirmed verbatim. |
| 14 | research-05 CODE-VERIFIED/CONTRADICTED/UNVERIFIED tags correct | PASS | §1a [CODE-VERIFIED] vs integrity.py:314 ✓; §1b [CODE-CONTRADICTED] vs :186 third conjunct absent ✓; §4a merged-req:141-143 [UNVERIFIED] (pure spec) ✓; §4c [CODE-VERIFIED]+[CODE-CONTRADICTED] vs planner:158-169 + integrity:97-101 ✓. All tags match source behavior. |
| 15 | design §2/§4(a)/§4(b) verbatim quotes accurate | PASS | design.md:85-92 BoundaryReport (6 fields, no paths) ✓; :148-154 §4(a) `lc = plan.boundary_tasks.role==last_completed` interrupted-scoped ✓; :172-180 §4(b) "report suspect paths in BoundaryReport (always)" ✓. All verbatim. |
| 16 | **F-4 CRITICAL consistency: _read_transcript keys on interrupted_phase** | PASS | integrity.py:112-114 `_read_transcript(results_dir, plan.interrupted_phase, lc.task_id)` — keys on `interrupted_phase`, NOT the prior phase. Research-03 §2.2 correctly flags planner-only fix is insufficient (needs BoundaryTask phase field). **No contradiction across files** — see Finding C below. |
| 17 | research-04 marked CG-3 source assumption Unverified | PASS | research-04 L331-332 + L400-401 mark "**Unverified** which source the fix reads P2's tail from (transcript vs result.json — `_complete_phase` writes `task_results: []`)". Verified `_complete_phase` does write `task_results: []` (test_resume.py:57). Honest flagging. |
| 18 | AC-4 vs AC-5 tension (F-3) — both land in branch 177-187 | PASS | test_resume.py:239-259 `test_drift_trailing_whitespace_high_conf`: `_P3 + "   \n"`, IDs unchanged, asserts `>=0.8` + `cosmetic_only is True` ⇒ lands in drift.py:177-187. Research-01 L51/L109 correctly identifies this AC-4 regression risk for any naive flip. Load-bearing for the builder. |
| 19 | CG-2 RED-test hash-strip premise | PASS | rerun_tasks.py:688-701 `_content_sha256_excluding_rerun_block` strips ONLY the `_RERUN_BLOCK_RE` (:661) provenance block. A deliverable/body edit DOES change the block-stripped hash ⇒ Tier-0 reliably misses. Confirms research-04 §3 hash-strip note. |
| 20 | NFR-3 (gate not git-dependent) + no-writes-in-planner addressed | PASS | Research-01 §6 explicitly forbids putting F-3 fix in `_annotate_git`. Research-03 §2.3 confirms `parse_tasklist_file`/`discover_phases` are read-only, fix mutates in-memory plan only, `test_planner_performs_no_writes` stays green. Both invariants covered. |

## Summary
- Checks passed: 20 / 20
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence Gate
- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 17 | Grep: 0 | Glob: 0 | Bash: 2 (grep). Tool calls (19) ≥ checklist items relevant; every Read/grep targeted a specific cited claim (drift.py, integrity.py, models.py, planner.py, checkpoints.py, executor.py, commands.py, design.md×5 ranges, merged-requirements.md×2, rerun_tasks.py, test_resume.py×4 ranges). No padding calls.

## Issues Found (non-blocking)
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| A | MINOR | research-01 header "drift.py (282 lines total)" | Cosmetic line-count claim — actual file is 282 lines (verified). Recorded only to show the claim was checked and is accurate. | None. |
| B | MINOR | research-02 L184-185 vs commands.py:407-434 | Research-02 §4 narrates "gate runs first (:400); if not passed → stop (:407-418); if drift <0.8 → stop (:420-434)". Source confirms this exact order (gate verdict at :407 BEFORE drift at :420). Accurate; no contradiction with research-03. | None. |

## Cross-File Consistency Findings (CRITICAL check #6 result)

**Finding C — F-4 fix-sufficiency is CONSISTENT across files (NO contradiction).** The spawn prompt warned that a contradiction here would be CRITICAL. I verified the opposite — the files agree:
- research-03 §2.2 (L87) states the planner-only fix is **insufficient**: integrity's `_read_transcript` keys on `plan.interrupted_phase` (verified integrity.py:112-114), so a prior-phase `last_completed` task would resolve its transcript under the WRONG phase number; a `BoundaryTask` phase field (or plan-level prior-phase number) is required. Flagged `[->r02]`.
- research-02 §5 (L213-225) independently reaches the SAME conclusion from the integrity side: "Any F-4 fix that wants the prior tail validated must either have the planner inject a synthetic `last_completed` BoundaryTask for the prior phase, OR add a prior-phase validation entry point to the gate."
- research-04 §5 (L326-332, L398-401) correctly defers the role-name and the tail-source (transcript vs result.json) to researcher-03's fix shape and marks the source **Unverified**.
- research-05 §4c records the spec basis (design §4(a) interrupted-phase-scoped vs merged-req AC-3 prior-tail) with correct [CODE-VERIFIED]/[CODE-CONTRADICTED] tags.

All four files treat F-4 as a **planner+integrity co-dependency requiring a BoundaryTask phase field**, none assumes it is a planner-only fix. This is the consistency the check demanded, and it holds. The `_read_transcript`-keys-on-`interrupted_phase` fact is independently verified at integrity.py:112-114.

## Coverage Assessment (for building the corrective task)

- **F-3 (drift):** Fully actionable. Exact branch (drift.py:177-187), the data-availability blocker (no baseline in result.json), the two fix options (conservative <0.8 vs whitespace-hash schema extension touching executor.py:2069-2078), and the AC-4 regression guard are all specified with file:line. The builder can write per-item checklist items directly.
- **F-2 (integrity/print):** Fully actionable. Option A (BoundaryReport.partial_paths field, models.py:84-101 + integrity.py:64 wiring) vs Option B (print at commands.py:520-536), with the §2 amendment dependency on research-05 named. Both research-02 and research-03 converge on Option A as preferred.
- **F-4 (planner/integrity):** Actionable with one EXPLICIT open dependency correctly surfaced — the BoundaryTask phase field + `_read_transcript` phase fix (co-dependency) and the tail-source (Unverified). The builder must create a checklist item for the phase-field addition; the research names exactly where (BoundaryTask model + integrity.py:112-114).
- **CG-4 (spec):** Fully actionable. Binary decision framed, verbatim spec lines (design §7:293, §4(c):186, FR-2.4:85-87) and a drop-in decision-record skeleton (research-05 §5). The builder can create a decision-resolution item.
- **NFR-3 (deterministic-core, no git in gate):** Addressed in research-01 §6 + §4 — the fix must NOT live in `_annotate_git`. **No coverage gap.**
- **No-writes-in-planner invariant:** Addressed in research-03 §2.3 — fix is in-memory only; recommends extending `test_planner_performs_no_writes`. **No coverage gap.**
- **Tests (CG-1/CG-2/CG-3):** research-04 supplies paste-ready test code reusing existing builders, with RED/GREEN transitions tied to each fix and AC-tag docstring linkage. CG-1 supplied in BOTH variants pending F-2's option choice. Actionable.

## Recommendations
- **Green light to proceed to synthesis / task building.** No gaps to remediate.
- Builder note: the F-4 BoundaryTask phase-field item and the F-2 §2-amendment item are the two cross-cutting items that multiple research files depend on — sequence them before the per-finding fix items so the dependent items (drift CG-2 test, integrity partial_paths) have their prerequisites.
- Builder note: per research-01, if the conservative F-3 fix (flip 177-187 to <0.8) is chosen without the whitespace-hash schema extension, it WILL break the existing AC-4 test (test_resume.py:239-259). The task must either adopt the schema-extension path or include an AC-4 test update — flag this as a hard execution-order constraint.

## QA Complete
