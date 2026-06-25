# QA Report — Research Gate (RE-RUN, gap-fill round 2)

**Topic:** FR-RH2 headless ensemble — adversarial scoring seam (G1) + PreflightResult construction (G2)
**Date:** 2026-06-20
**Phase:** research-gate (fix-cycle re-verification)
**Fix cycle:** 2 (verifying gap-fill round 1 output)
**Fix authorization:** false (report-only)
**Lens:** gap-detection
**Stance:** ADVERSARIAL — assume gaps remain; verify the gap-fill actually closed G1 and G2.

---

## Scope

Re-verify the two blocking gaps from the prior research-gate FAIL:
- **G1 (CRITICAL):** ensemble.py → /sc:adversarial scoring seam uncovered; NFR-7 forbids Task/subagent/raw-subprocess for obtaining `adversarial_convergence_score`.
- **G2 (MINOR):** no PreflightResult construction recipe.

Gap-fill file under review:
`07-gap-fill-adversarial-seam-oi1-table.md`

---

## Tool engagement

Read: 6 (07-gap-fill, test_no_nesting_guard.py, dispatch.py, preflight.py, commands.py, contract.py, validate_executor.py) | Grep/Bash: 1 (find adversarial module + sed SKILL return-contract) | Glob: 0

Every cited source the gap-fill leans on was opened and cross-checked independently — not taken on the gap-fill's word.

---

## G1 (CRITICAL) — adversarial scoring seam — VERDICT: CLOSED

### What the gap-fill claims vs. what the source actually says (independently re-verified)

| Gap-fill claim | Cited locus | Independent verification | Holds? |
|---|---|---|---|
| No `cli/adversarial*` Python module; `/sc:adversarial` is a Claude-inference SKILL | `find src/superclaude/cli -iname '*advers*'` | Ran it. Returns ONLY `cli/eval/suites/adversarial_merge_consistency.yaml` (an eval YAML, not a code module). | YES |
| Guard bans `Task(`/`subagent`/`subprocess.run`/`Popen`/`anthropic` LITERALS and **asserts `ClaudeProcess` presence** | test_no_nesting_guard.py:98, 99-102 | Read the file. Line 98: `assert "ClaudeProcess" in src`. Lines 99-102 ban exactly `("import anthropic","from anthropic","subagent","Task(")`. Line 136: second `assert "ClaudeProcess" in src`. Lines 140-142: `_RAW_SUBPROCESS_CALL_RE`/`_IMPORT_SUBPROCESS_RE` assert ABSENCE of raw subprocess. | YES — exact |
| Raw-subprocess + agent-import bans scan `runner.py` ONLY; sprint/roadmap + async bans scan ALL `*.py` | test_no_nesting_guard.py:22, 24 | Line 22: `_RUNNER_SRC = _REFLECT_PKG / "runner.py"`. Line 24: `_REFLECT_PY = sorted(... glob("*.py") ...)`. `test_layer_b...` (95-102) + `test_apply_remediation...` (128-142) both scope to `_RUNNER_SRC`. `test_no_sprint_or_roadmap...` (105-113) + `test_no_async_await...` (116-125) iterate `_REFLECT_PY`. | YES — exact |
| A new `ensemble.py` is covered TODAY by async/import bans but NOT by the `Task(`/`subprocess`/`anthropic` bans | derived from 22/24 | Correct by construction: `ensemble.py` would be in `_REFLECT_PY` (async + sprint/roadmap bans) but NOT `_RUNNER_SRC` (Task/subprocess/anthropic bans). The gap-fill correctly flags this as needing `_RUNNER_SRC`-style extension (FR-RH2.8). | YES |
| `/sc:adversarial` emits `convergence_score`; reflect reads `adversarial_convergence_score` → rename needed | SKILL.md return-contract; contract.py:284 | SKILL return-contract block: `convergence_score: 0.75  # float 0.0-1.0`. contract.py:284: `if tier_reached == 2 and contract.get("adversarial_convergence_score") is None: return "null-convergence"`. Names genuinely differ → mapping layer must rename. | YES |
| validate_executor runs the adversarial merge as a `ClaudeProcess` Step, result parsed from the report file (the decisive precedent for Option b) | validate_executor.py:365-373 | Read :364-378. `merge_step = Step(id="adversarial-merge", prompt=build_merge_prompt(...), output_file=.../validation-report.md, gate=ADVERSARIAL_MERGE_GATE, ...)`; parsed by `_parse_report_counts` (:381). A claude-subprocess merge, not a Python scorer. | YES — exact |

### Is single-level `claude -p /sc:adversarial` genuinely NFR-7-legal?

**Yes.** Three independently-verified facts establish it:
1. The guard is a **static text grep** over reflect-package source (test_no_nesting_guard.py — no execution). A `ClaudeProcess` launch from `ensemble.py`/`runner.py` contains none of the banned literals (`Task(`/`subprocess.run(`/`Popen(`/`anthropic`), and `ClaudeProcess` is **affirmatively required** (`assert "ClaudeProcess" in src`).
2. The `/sc:adversarial` child's OWN internal `Task` usage lives in `sc-adversarial-protocol/SKILL.md`, NOT in the reflect package source — outside the guard's file set entirely. The guard cannot and does not see it.
3. The nesting defect (spec §1) bit only the DOUBLY-nested `claude -p → /sc:reflect Task-worker → Task` path. A fresh top-level `claude -p /sc:adversarial` is single-level — exactly the same nesting depth as the existing Tier-1 `/sc:reflect` child, which already nests Task legally. No new double-nesting is introduced (see G3 below).

### Is the human-decision flag the RIGHT outcome (CLOSED), not a remaining gap?

**Yes — this is the correct disposition, and it CLOSES the gap.** The gap-fill does not leave the seam as an unknown; it:
- Identifies a **concrete, NFR-7-legal mechanism** (Option b: second `ClaudeProcess` running `/sc:adversarial` Mode A, or an inline `build_merge_prompt`-style merge mirroring validate_executor), grounded in two real precedents.
- Correctly demonstrates the spec/TDD **under-specify** the seam with specific evidence: TDD §4.1 lists only swarm fan-out deps (`dispatch_wave1`/`_resolve_run_transport_factory`/`reduce_wave3`) with NO adversarial-scoring dependency; spec §9 NFR-7 reconciliation is silent on a second adversarial child; OI-4 unresolved.
- Encodes the residual as a **`needs_human_decision` item that must HALT** the dependent spec/gate mutation per `feedback_human_decision_items_must_halt` — never auto-defaulting a load-bearing architecture choice.

A properly-flagged, actionable HALT item over a genuinely under-specified load-bearing seam is the RIGHT engineering outcome. The seam is now actionable (a concrete legal mechanism + a bounded decision), not an open unknown. **G1 CLOSED.**

---

## G2 (MINOR) — PreflightResult construction — VERDICT: CLOSED

| Gap-fill claim | Cited locus | Independent verification | Holds? |
|---|---|---|---|
| `dispatch_wave1` reads EXACTLY ONE field: `preflight_result.manifest.preflight.workers_requested` | dispatch.py:412 | Read :405-419. Line 412: `workers_requested = preflight_result.manifest.preflight.workers_requested`. Confirmed it is the only PreflightResult attribute access in the dispatch body. | YES — exact |
| `PreflightResult` = `@dataclass(manifest, state, manifest_path=None, caller_metadata=...)` | preflight.py:239-263 | Read it. `manifest: Manifest` / `state: SwarmState` required; `manifest_path: Optional[str]=None`; `caller_metadata` default-factory. Only `manifest` + `state` positional. | YES — exact |
| Synthetic-construction precedent exists in `commands.py` resume path | commands.py:2415-2427 | Read :2410-2434. `synthetic_manifest = _Manifest(... preflight=_PreflightSummary(... workers_requested=len(remaining_indices) ...))`; `synthetic_state = _SwarmState(state="preflight_ok", ...)`; `synthetic_preflight = _PreflightResult(manifest=..., state=...)`. The synthetic-construction recipe is real. | YES (block at :2414-2427; gap-fill's :2415 start is off-by-one, immaterial) |

The construction recipe is now documented end-to-end: which single field dispatch reads, the minimal dataclass shape, and a working in-repo synthetic-construction precedent to mirror (`Manifest` with `preflight.workers_requested == reviewers` + `SwarmState(state="preflight_ok")`). The note that the `ModelPoolTooSmallError` pool guard is independent (raised by `_resolve_run_transport_factory`, not `dispatch_wave1`) is a correct, useful addition. **G2 CLOSED.**

---

## G3 — NEW gap introduced by the recommended seam? — NONE BLOCKING

Adversarially checked the three risks the brief named:

1. **Double-nesting reintroduced?** NO. A second `ClaudeProcess /sc:adversarial` launched from the reflect package is a **fresh top-level agent** — single-level nesting, identical depth to the existing Tier-1 `/sc:reflect` child. The original defect was the doubly-nested `claude -p → Task-worker → Task` path; a sibling top-level `claude -p` does not recreate it. Verified the guard cannot see the child's internal Task (it's in the SKILL, outside the reflect file set).
2. **Path-confinement contradiction?** NO — the gap-fill's Option (b) actually RESPECTS confinement better than Option (a): `ensemble.py` consumes the swarm `t2-swarm/` `final_path` artifacts and the adversarial child writes the reflect-side score; it does NOT make the reflect child parse the `t2-swarm/` contract directly (the thing spec §5.3 path_confinement forbids). The gap-fill explicitly disqualifies Option (a) on exactly this confinement ground.
3. **Score-field plumbing mismatch?** Surfaced, not introduced: the `convergence_score` → `adversarial_convergence_score` rename is a real, now-documented mapping requirement (verified both names in source). It is captured in the OI-1 provenance table (row 19) and the GAP-1 synthesis, not left implicit.

One residual (already correctly captured by the gap-fill, not new): the **on-disk path** the headless `/sc:adversarial` child writes its return contract to is unspecified by the SKILL (it "returns" the contract to the caller). The gap-fill folds this into the same `needs_human_decision` HALT item ("confirm the on-disk path the adversarial child writes its return contract to so `ensemble.py` parses `convergence_score`"). Appropriately scoped — part of the already-flagged decision, not a separate uncovered gap.

No NEW blocking gap is introduced by the recommended seam.

---

## Confidence Gate

- G1 closed — VERIFIED (test_no_nesting_guard.py read; `find` run; SKILL return-contract + contract.py:284 cross-checked; validate_executor.py:365-373 read).
- G2 closed — VERIFIED (dispatch.py:412, preflight.py:239-263, commands.py:2414-2427 all read).
- G3 no-new-gap — VERIFIED (nesting depth, path-confinement, rename all traced to source).

**Confidence:** Verified: 3/3 blocking determinations | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

Tool-engagement minimum satisfied: 7 tool calls (6 Read + 1 Bash) for 3 blocking determinations, each call mapped to a specific cited claim.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | G1: NFR-7-legal mechanism for `adversarial_convergence_score` exists | PASS | Option (b) second `ClaudeProcess /sc:adversarial`; guard asserts `ClaudeProcess` presence (test:98) and bans only literals (test:99-102) |
| 2 | G1: single-level `claude -p /sc:adversarial` is NFR-7-legal | PASS | Static-grep guard + child Task lives in SKILL not reflect pkg; single-level depth = existing Tier-1 child |
| 3 | G1: residual correctly flagged as HALTing `needs_human_decision` | PASS | Under-spec evidence (TDD §4.1, spec §9, OI-4) cited; HALT per feedback_human_decision_items_must_halt |
| 4 | G2: PreflightResult construction documented + spot-checked | PASS | dispatch.py:412 (one field), preflight.py:258-263 (dataclass), commands.py:2414-2427 (synthetic precedent) |
| 5 | G3: no new double-nesting / confinement / plumbing gap | PASS | Single-level sibling launch; Option (b) respects §5.3 confinement; rename captured in OI-1 row 19 |
| 6 | Citation accuracy (adversarial seam claims) | PASS | All 6 load-bearing citations re-opened; only deviation is a 1-line off-by-one on commands.py start line (immaterial) |

## Summary
- Blocking determinations passed: 3 / 3 (G1, G2, G3)
- Checks failed: 0
- Critical issues: 0
- Citation defects: 1 cosmetic (commands.py:2415 vs actual block start :2414 — off-by-one, does not affect correctness)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | (cosmetic, non-gating) | 07 §2 / commands.py | Gap-fill cites synthetic-construction at commands.py:2415-2427; the `synthetic_manifest =` assignment actually begins at line 2414 | None required (off-by-one line ref; block content is correct). Optional tidy in a later pass. |

No CRITICAL, IMPORTANT, or MINOR gaps remain. Both blocking gaps from the prior FAIL are closed, and the gap-fill correctly converts the under-specified load-bearing seam into an actionable HALTing human-decision item rather than burying it as an Open Question or auto-defaulting it.

## Recommendations
- Green light for synthesis, with one MANDATORY carry-forward into the task file: the GAP-1 adversarial-scoring seam MUST be authored as a `needs_human_decision` item that HALTS the dependent spec/gate mutation (per `feedback_human_decision_items_must_halt`) — do NOT let it become an auto-defaulted wiring step or a soft Open Question.
- Carry the `convergence_score` → `adversarial_convergence_score` rename (OI-1 row 19) and the FR-RH2.8 `_RUNNER_SRC`-style guard-extension for `ensemble.py` into the implementation plan as explicit steps.
- Cosmetic: correct the commands.py:2415 → 2414 line reference if the research file is revised.

## QA Complete

---

VERDICT: PASS — G1 CLOSED, G2 CLOSED, no new gap from the recommended seam. The properly-flagged HALTing human-decision item on the adversarial-scoring launch seam counts as CLOSED (actionable, not unknown). No remaining severity-rated gaps. One cosmetic off-by-one citation, non-gating.
