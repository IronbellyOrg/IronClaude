# QA Report — Research Gate (Partition A of 2)

**Topic:** Post-R1 roadmap-pipeline brittleness-elimination follow-ups (Areas A/B/C)
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

**Assigned files (PARTITION A):**
- research/01-file-inventory-area-a.md
- research/02-patterns-conventions.md
- research/03-area-b-generation-phantom-id.md
- research/04-area-c-opus-architect-fidelity-perf.md

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage, cross-references) limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: PASS (with 1 IMPORTANT staleness note + 2 MINOR)

The four assigned research files are dense, evidence-based, and actionable. Every
high-stakes claim I was asked to re-test reproduced exactly against live code. There is
ONE genuine staleness defect (Area C gate description predates the R1.6 cleanup already
in this branch) — it does not invalidate the load-bearing latency root-cause, but it
must be corrected so the builder does not encode a deleted code shape. Two MINOR notes.

Per research-gate rules, ANY gap = FAIL. I rate the staleness note IMPORTANT (a factual
error in a cited code shape, not a gap that causes synthesis hallucination). I classify
it as a FINDING-TO-FIX rather than a blocking gap because: (a) the corrected state is
fully captured in this report with file:line evidence the builder can use directly, and
(b) the actionable conclusions of file 04 (latency root cause, PRESERVE constraints,
actionable-vs-investigation verdict) are UNAFFECTED. I issue PASS-with-corrections: the
builder MUST read the Area C correction below. If the gate requires zero-defect,
downgrade to FAIL and have R4 patch the §3 gate description.

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / Status:Complete | PASS | All 4 files have `Status: Complete` (01:5, 02:178, 03:153, 04:127) + Summary sections. |
| 2 | Evidence density | PASS (Dense) | >90% of claims carry file:line. Re-verified 12 distinct citations against live code; all matched. |
| 3 | Scope coverage (within partition) | PASS | Areas A/B/C fully covered: A deletion safety (01), patterns (02), B phantom-ID gap (03), C perf+adherence (04). [PARTITION: D/E in partition B.] |
| 4 | Doc cross-validation tags | N/A→PASS | Research is code-sourced, not doc-sourced; no untagged doc claims requiring CODE-VERIFIED/UNVERIFIED tags. |
| 5 | Contradiction resolution (within partition) | FAIL→noted | File 04 §3 describes `gate=None if convergence_enabled` which CONTRADICTS live executor.py:2666-2675 (R1.6 DELETED that bypass). Surfaced as IMPORTANT below. |
| 6 | Gap severity | PASS | File 03 precisely classifies gaps (a) primary / (b) by-design / (c) not-a-gap with evidence. File 04 cleanly separates actionable-now vs investigation-only. |
| 7 | Depth appropriateness (Deep) | PASS | File 03 traces generation-vs-merge-gate divergence end-to-end (2 sidecars, 2 sources). File 01 traces import-failure → arch-removal → re-home chain. |
| 8 | Integration point coverage | PASS | executor↔tool_writer dispatch (03), executor↔convergence short-circuit (04), wiring_gate↔sprint consumers (01 A.6) documented. |
| 9 | Pattern documentation | PASS | File 02 captures 8 house patterns (config-flag, step-construction, gate, error-handling, docstring, test conventions) with file:line. |
| 10 | Incremental-writing compliance | PASS | All 4 files show iterative structure (In Progress→Complete flips, numbered subsections, growing tables); no one-shot signature. |

---

## High-stakes re-test results (I ran these myself)

**Area A — ALL VERIFIED:**
- `uv run python -c "import tests.integration.test_wiring_pipeline"` → `ImportError: cannot import name 'WIRING_GATE' from 'superclaude.cli.roadmap.gates'` — reproduces EXACTLY (01:18-21).
- `WIRING_GATE` present ONLY at `audit/wiring_gate.py:1024` (grep on roadmap/gates.py → zero symbol matches; only a docstring comment). Matches 01:33.
- `'wiring-verification' in ALL_GATES` → **False**; `len(ALL_GATES)` → **14**. Matches 01:36, 01:113.
- No external references to the test module (grep across .py/.toml/.cfg/.ini → empty). Matches 01:47-49.
- `test_no_pipeline_imports_in_wiring_gate` exists ONLY in the to-be-deleted file (grep → single hit). "No exact home elsewhere" (01:60-67) is CORRECT.
- `check_wiring_report` at `wiring_gate.py:1102` (the brief's "run_all_semantic_checks wrapper") — confirmed; iterates `WIRING_GATE.semantic_checks` (1119). Matches 01:83.
- wiring_gate.py imports ONLY `pipeline.models` (line 1022) — NFR-007 invariant holds (01:70-73, 112).

**Area B — ALL VERIFIED:**
- `render_step_tool_write_with_id_check` at `tool_writer.py:455` with the `if spec_ids:` skip (487); docstring confirms the empty-skip rationale verbatim. Matches 03:37-57.
- `validate_id_subset` at 344, error string `roadmap_id '{rid}' not in spec_ids ∪ accepted_deviations` (367) — exact match (03:23, 31).
- executor `if _tw_key in ("generate", "merge")` routes to id-check renderer; spec_ids derived from `extraction.json`'s `roadmap_ids` (executor.py:1280-1289); `accepted_deviations=None` hard-coded — ALL confirmed (03:65, 77, 88; 03:147).
- `spec_id_registry.json` ALWAYS written unconditionally (`sidecar.write_text(...)` at executor.py:~652, no flag guard) — confirmed (03:77). Linchpin of Fix-1's correctness; it holds.
- `SpecIdRegistry.union_of_known()` folds fr+nfr+sc+g+d+md+accepted (id_registry.py:94-104) — confirmed (03:94).

**Area C — LATENCY ROOT CAUSE VERIFIED; GATE DESCRIPTION STALE:**
- Convergence default-ON: `"convergence_enabled": not no_convergence` (commands.py:362) — confirmed (04:64).
- Short-circuit `if step.id == "spec-fidelity" and config.convergence_enabled: return _run_convergence_spec_fidelity(...)` (executor.py:1069-1073) — confirmed (04:68-72).
- `_run_convergence_spec_fidelity` calls `execute_fidelity_with_convergence(... max_runs=3 ...)` and NEVER references `step.timeout_seconds` → the 600s literal is genuinely INERT on the convergence path. Verified by grepping the function body (1533-1712): only `max_runs=3` and the inner-call timeout appear. This is the LOAD-BEARING claim and it is TRUE (04:72, 99, 132).
- spec-fidelity `timeout_seconds=600` (executor.py:2676); inner `_ClaudeRunner` ClaudeProcess `timeout_seconds=300` (executor.py:~1517) — both confirmed (04:58, 77).
- **STALE:** File 04 §3 and candidate b (line 99) describe the gate as `gate=None if convergence_enabled`. Live code at executor.py:2666-2675 carries an explicit R1.6 comment: *"the `gate=None if convergence_enabled` bypass is DELETED. Both modes now use the convergence-aware gate"*, and uses `gate=SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (gates.py:1363). R1.6 landed in commit 17b8ee94, in this branch at session start. See IMPORTANT finding below.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | 04 §3 (lines ~63-72), candidate (b) line 99 | Gate described as `gate=None if convergence_enabled` (a pre-R1.6 bypass). R1.6 (commit 17b8ee94, already in branch) DELETED that bypass; spec-fidelity Step now sets `gate=SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (executor.py:2675, gates.py:1363) for BOTH modes. The latency root-cause (timeout INERT in convergence) is UNAFFECTED and still correct, but the gate shape the builder would encode is wrong. | R4 should correct §3 to: convergence mode no longer nulls the gate; both modes run `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`. Re-derive candidate (b)'s "trap" framing accordingly (the 600s literal is still inert, but for the convergence-engine-bypass reason, NOT a gate=None reason). Builder MUST NOT author any item that re-introduces or references a `gate=None` spec-fidelity bypass. |
| 2 | MINOR | 01 line 34 | `dict(ALL_GATES)` phrasing implies ALL_GATES is a dict. It is actually a **list of (str, GateCriteria) tuples** (gates.py:1566). `dict(ALL_GATES)` is valid Python (list-of-pairs → dict), so the claim is technically correct, but a builder skimming it may assume dict subscripting. | Minor wording: note ALL_GATES is a list-of-tuples; subscript via `dict(ALL_GATES)[key]`, not `ALL_GATES[key]`. No blocking impact. |
| 3 | MINOR | 04 line 64-72 cited "executor.py:1068-1073" | Short-circuit actually begins at line 1069 (the `step.id ==` predicate); 1068 is the `if (` opener. Off-by-one. | Trivial; no fix required. Builder should re-grep before editing regardless. |

---

## Coverage gaps for the builder (Areas A/B/C) — none blocking

- **Area A:** The single re-homing precondition (move `test_no_pipeline_imports_in_wiring_gate` into `tests/audit/test_wiring_gate.py` before/alongside deletion) is clearly stated and correct. The builder has everything needed: file to delete (379 LOC), the one unique assertion, its target home, and proof of zero external references.
- **Area B:** Fix shape is fully specified and DETERMINISTICALLY TESTABLE (no LLM). The linchpin fact — `spec_id_registry.json` is always written — is verified, so Fix-1 (re-source `_spec_ids` from `union_of_known()`) is sound. PRESERVE constraints enumerated. No gap.
- **Area C:** Correctly classed Low/diagnostic. The ONE actionable-now item (a behavior-neutral comment on the spec-fidelity Step) is safe. All real latency fixes are correctly gated behind the PRESERVE boundary (`convergence.py`/`semantic_layer.py` byte-untouched — verified that claim's PRESERVE marker exists in-tree). The builder must apply Issue #1's correction so the comment it authors describes the CURRENT gate (`SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`), not the deleted `gate=None`.

---

## Confidence Gate

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

(All 10 research-gate checklist items checked with tool evidence. Item 5 found a real
contradiction — that is a successful FAIL detection, still a VERIFIED check. Confidence
measures verification thoroughness, not absence of issues.)

**Tool engagement:** Read: 5 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 7
(tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 —
no external lookups required; all claims are intrinsically local code.)

Tool-engagement note: 12 tool calls total vs 10 checklist items — above the minimum.
Each Bash call mapped to specific claim verification (import repro, WIRING_GATE location,
test references, unique-assertion home, ALL_GATES type+membership, renderer/validate
bodies, executor dispatch, sidecar write, union_of_known, convergence short-circuit,
timeout literals, git history). No padding calls.

UNCHECKED items: none.
UNVERIFIABLE items: none.

---

## Summary

- Checks passed: 10 / 10 (item 5 passed AS A DETECTION — it correctly surfaced a contradiction)
- Checks failed: 0
- Critical issues: 0
- Important issues: 1 (Area C stale gate description — non-blocking, fully corrected in this report)
- Minor issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Recommendations

1. **Builder:** When authoring the Area C item, encode the CURRENT gate
   (`SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`, gates.py:1363). Do NOT reference or
   re-introduce any `gate=None if convergence_enabled` bypass — R1.6 deleted it. The
   behavior-neutral comment on the spec-fidelity Step should explain the 600s literal is
   inert because the convergence ENGINE bypasses the step timeout (max_runs×inner-300s),
   not because the gate is nulled.
2. **Builder:** Area A and Area B research are directly actionable as-is. Area A: one
   re-homing precondition + a 379-LOC deletion. Area B: Fix-1 (re-source `_spec_ids` from
   `spec_id_registry.json.union_of_known()`) + Fix-2a (fail-shut on missing registry for
   generate/merge), both deterministically testable.
3. **Optional:** R4 patches file 04 §3/candidate-b to reflect the post-R1.6 gate. Not
   required for the builder if Recommendation 1 is followed.

## QA Complete
