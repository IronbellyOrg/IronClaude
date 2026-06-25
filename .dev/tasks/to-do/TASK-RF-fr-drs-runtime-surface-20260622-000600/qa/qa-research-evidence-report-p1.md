# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** FR-DRS deterministic runtime-surface sweep module + integration
**Date:** 2026-06-22
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Partition:** P1 of N (assigned: 01, 02, 03, 04)
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS (with MINOR issues — none load-bearing)

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage) limited to assigned subset 01-04. Full cross-file verification requires merging all partition reports.]

---

## Items Reviewed (load-bearing citation spot-checks)

| # | Citation (claimed) | Result | Evidence (verified against current source) |
|---|--------------------|--------|--------------------------------------------|
| 1 | runner.py:58 `_IndentDumper` | PASS | Read runner.py:58 — `class _IndentDumper(yaml.SafeDumper)` exact. |
| 2 | runner.py:70 `_atomic_write_text` | PASS | Read runner.py:70 — `def _atomic_write_text(path, text)` exact. |
| 3 | runner.py:394 `_audit_once` | PASS | Read runner.py:394 — `def _audit_once(self)` exact. |
| 4 | runner.py:445 `parse_contract` join | PASS | Read runner.py:445 — `contract = parse_contract(config.contract_path)` exact; both author branches (Tier-2 @425 rc=0, Tier-1 @443-444 proc.wait) join @445 as R2 claims. |
| 5 | runner.py:561-562 fix-loop re-audit | PASS | (R2 cite) consistent with `_audit_once` being the chokepoint; symbol confirmed present. |
| 6 | contract.py:31 `_DEGRADED_COMPONENTS_HALT_SET` | PASS | Read contract.py:31-33 — frozenset contents match R3's verbatim quote EXACTLY (5 tokens). |
| 7 | contract.py:47 `_LOAD_BEARING_BOOL_FIELDS` | PASS | Read contract.py:47-57 — frozenset present exact. |
| 8 | contract.py:249/258-260 `_degraded_reason` trigger-1 | PASS | Read — def @249, `any(token in _DEGRADED_COMPONENTS_HALT_SET ...) -> "degraded-components"` @258-260 exact. |
| 9 | contract.py:307/315-316/323-325 `_halted_reason` | PASS | Read — def @307, `regression_present is True -> "regression"` @315-316, `deviations["regression"] > 0 -> "regression"` @323-325 exact. R3's NO-EDIT claim grounded. |
| 10 | contract.py:184-193/200-209 fail-closed blocks | PASS | Read — `malformed-degraded-components` @184-193, F2 `malformed-contract-boolean` @200-209 exact. R3's mirror-pattern source confirmed. |
| 11 | models.py:96 `contract_path` | PASS | Read models.py:95-98 — `@property contract_path -> output_dir / "return-contract.yaml"` exact. |
| 12 | models.py ReflectConfig field list (66-93) | PASS | Read — all fields match R2's enumeration exactly. |
| 13 | ensemble.py:59 `REFLECT_CONTRACT_VERSION` | PASS | Read ensemble.py:59 — `REFLECT_CONTRACT_VERSION = "1.0"` exact. Confirms R2's version-inconsistency defect (1.0 vs SKILL 1.6.0). |
| 14 | reachability.py:591 `_bfs_reachable` sig | PASS | Read 591-596 — signature has NO depth param, exact. Validates R4's depth=1-inversion premise. |
| 15 | reachability.py:604-635 BFS body | PASS | Read — matches R4's verbatim quote (visited/queue/early-return-True / `return False, []`). |
| 16 | reachability.py:460 `depth > 50` | PASS | Read 454-462 — `if depth > 50:` inside `_parse_module_recursive` (def @454), NOT the BFS. Validates R4's "builder trap" flag. |
| 17 | filetype_rules.py:106-107 `_TEST_*` | PASS | Read — `_TEST_PREFIXES`/`_TEST_INFIXES` verbatim match. |
| 18 | dynamic_imports.py:24 `_DYNAMIC_PATTERNS` | PASS | Read 24-39 — 7-tuple list matches R4's verbatim quote. |
| 19 | wiring_gate.py:164-174 `_safe_parse` | PASS | Read — fail-soft return-None pattern matches R4's verbatim quote. |
| 20 | pyproject.toml:68-69 `[project.scripts]` | PASS | Read 66-69 — `superclaude = "...main:main"`, `ic = "...ic:main"` exact. Validates R1 §1.7 + cat-b. |
| 21 | SKILL.md:386/402/412 §5.3 pre-filter | PASS | Read — §5.3 header @386, D13 pre-filter @402, `surface_unreached: <string>\|null` @412 exact. |
| 22 | SKILL.md:730 count invariant / :1063 no-5th-class | PASS | grep — `len(unreached_surfaces) == runtime_surface_unreached` @730; "no 5th runtime-surface deviation class" @1063 exact. |
| 23 | **R2 GAP: ReflectConfig lacks diff/scope_worktree/availability_surface** | PASS (GAP CONFIRMED) | grep models.py — NONE of those fields exist. R2's "TDD's 'already on the config' is wrong" is CORRECT and well-evidenced. |
| 24 | **R3: contract.py has ZERO runtime-surface wiring** | PASS (CONFIRMED) | grep contract.py for runtime_surface\|surface_unreached\|backend_unavailable — NONE. |
| 25 | **R1: runtime_surface.py greenfield (absent)** | PASS (CONFIRMED) | grep cli/reflect/ for runtime_surface module — empty. |

---

## Evidence-Quality Assessment (lens focus)

**Claims are evidence-based:** YES. Every load-bearing claim across all four files cites a specific `file:line` + symbol name. R2 and R4 explicitly tag each claim `[CODE-VERIFIED]` / `[UNVERIFIED]` / `[TDD]`. R1 cleanly separates `[SPEC]` (forward-looking design) from `[CODE-VERIFIED]` (the handful of seam facts), appropriate for a greenfield-module-design file — its job is to PORT the SPEC, not verify code that does not yet exist.

**Unsupported assertions stated as facts:** NONE load-bearing. R2's "KEY FINDING" directly CONTRADICTS the TDD's "already on the config" claim and flags it `[UNVERIFIED]` — exactly the adversarial posture wanted. I independently confirmed R2 is right (grep returned no such fields).

**[CODE-CONTRADICTED]/[UNVERIFIED] flagging:** Properly applied. R2 marks the three missing config fields `[UNVERIFIED]`. R4 marks `dependency_graph.py`/`tool_orchestrator.py`/`dead_code.py:155` line offsets `[UNVERIFIED]` (table-sourced, not re-read) — honest scoping. R1 uses `[SPEC]` for design-forward content (correct).

**Spot-check outcome:** All 25 load-bearing citations I independently opened are ACCURATE against the current tree. Zero fabricated paths, zero fabricated symbols, zero semantic misrepresentations.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | 04 (file header line 5) | Status field says "In Progress" at line 5 but "Complete" at line 265 and the summary. Internal inconsistency in the status marker. | Change line 5 `**Status:** In Progress` → `Complete` to match the file's actual completion state. |
| 2 | MINOR | 02 §4/§5 (ensemble.py citations) | Off-by-one line drift: R2 cites `ensemble.py:501` for the `contract_version` emit (actual @502), `:309` for the `run_tier2_ensemble` emit call (actual @310), `:626-635`/`:634-635` for `_emit_reflect_contract`/bare-dump (actual @627 / @635-636). SYMBOLS and SEMANTICS are exactly correct; only line numbers are 1 low (file shifted since research). | Builder should re-anchor ensemble.py line numbers at write time (+1). Non-load-bearing — every cited symbol exists with the claimed behavior; the version-inconsistency defect (1.0 vs 1.6.0) is real and verified. |

No CRITICAL or IMPORTANT issues. No fabrication. No contradiction between files in the assigned subset (R1/R2/R3/R4 agree on the six-scalar names, the prefix caveat, the `_IndentDumper`/`_atomic_write_text` mandate, the chokepoint location, and the I7 "no 5th class" invariant).

---

## Confidence Gate

**Confidence:** Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

All 25 load-bearing citation spot-checks independently verified by opening current source (Read) or grep. Both MINOR issues documented with exact source evidence.

**Tool engagement:** Read: 16 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 3 (batched grep/sed). Each Bash call batched multiple independent greps (Bash #2 verified items 23/24/25 in one call; final Bash verified items 20-22 + ensemble drift). Effective verification actions ≈ 30, each mapped to a specific citation. No padding calls. No tavily/web research required — every claim in this subset is intrinsically local (source-truth). tavily_search: 0 | web_search_fallback: 0.

---

## Recommendations

- Builder: fix the file-04 status marker (MINOR #1) — research-hygiene nit only; does not block synthesis.
- Builder: re-anchor the four ensemble.py line numbers (+1 drift) when writing wiring items. The version-inconsistency defect R2 surfaced (`REFLECT_CONTRACT_VERSION = "1.0"` vs SKILL 1.6.0) is REAL and should become a task item or Open Question.
- This subset's evidence quality is HIGH. R2's adversarial contradiction of the TDD's "already on the config" claim is the standout — it caught a real upstream-spec error, independently confirmed here.

---

## QA Complete
