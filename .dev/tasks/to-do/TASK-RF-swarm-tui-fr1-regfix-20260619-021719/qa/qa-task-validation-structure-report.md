# QA Report — Task Integrity (Phase Structure Lens)

**Topic:** swarm --tui FR-1 REG-1 corrective remediation
**Date:** 2026-06-19
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

A code-remediation task with strong structural discipline. Phase ordering, anti-orphaning, POST-reflect form, and frozen-signature protection are all correct and verified against live source. The task FAILS the zero-tolerance gate on a TB-Add-7 heading-token form drift plus a factual imprecision in the DRIFT-1 out-of-scope note. None are CRITICAL or execution-blocking, but per task-integrity rules ANY issue = FAIL.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | `---` fences L1/L63; id/title/status/created_date/start_commit/executor_model_class/spec_path all present + non-empty (L2,3,6,12,18,19,20). `depends_on: []` valid. |
| 2 | Mandatory sections present (tmpl 02) | PASS | Task Overview, Key Objectives, Prerequisites & Dependencies, Execution Context, Detailed Task Instructions, Task Log/Notes all present (L67-309). Post-completion items live in Phase 4. |
| 3 | Phase deps logical (source→edge→test→validate) | PASS | P1 REG-1 source (tui/parallel/dispatch) → P2 FR-5 edges (commands.py) → P3 tests exercising P1+P2 → P4 validation. Tests come AFTER the source they exercise (3.1 audits 1.5 gating; 3.4/3.5 exercise 2.1/2.2). |
| 4 | Phase ordering progression | PASS | Phases 1-4 sequential, no gaps; per-phase Step numbering monotonic. |
| 5 | Completion items in final phase (anti-orphaning) | PASS | Step 4.4 (summary), 4.5 (reflect), 4.6 (status→Done) all in Phase 4. |
| 6 | Task Log section at bottom | PASS | `## Task Log / Notes 📋` L259 with Execution Log + per-phase Findings + Open Questions + Follow-Up + Deviations. |
| 7 | Item count reasonable for scope | PASS | 22 `- [ ]` items for ~4 source files + audit/PTY/2 regression tests + validation. Proportionate. |
| 8 | Open Questions / out-of-scope documented | PASS (caveat — Issue #3) | DRIFT-1 + NEC-1 recorded as out-of-scope follow-ups (L317-318); correctly NOT actioned. |
| 9 | POST reflect: FLAT, penultimate, recursion-breaker | PASS | Step 4.5 (L253): `superclaude reflect run <taskfile> --depth deep --fix --promote`; behind `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`; exit-code consumed (0 proceeds; 10/11/2 blocks); NO --base/--reflect/HEAD/agent-spawn; explicitly PENULTIMATE before 4.6. Not legacy/HALT form. |
| 10 | TB-Add-1: no TBD/TODO/FIXME, no title-only | PASS | grep found none. All items full self-contained paragraphs. (Task-Log `<!-- -->` are template scaffolding.) |
| 11 | TB-Add-3: blocked items ref Open Question by index | PASS (correct as N/A) | DRIFT-1/NEC-1 are NOTES not blockers; no item is blocked-on-question. Correct. |
| 12 | TB-Add-4: item deps form a DAG | PASS | Linear forward chain; no item references a later item as prerequisite. Acyclic. |
| 13 | TB-Add-5: XL/multi-file items split or justified | PASS | Step 1.5 (gate prints across 3 methods) bounded to one file + one mechanical `if not self.quiet:` transform with explicit print enumeration. 1.3/1.4/1.6 single-file single-edit. |
| 14 | TB-Add-6: uniform Verify/Acceptance form | PASS | All items use "ensuring..." + "If unable... log... Once done, mark this item as complete." Consistent. |
| 15 | TB-Add-7: Source Areas reappear; no file:line in header | FAIL (marginal) | See Issue #2: heading is `### Source Areas` not `**Source areas:**`; substantive invariant HOLDS (all areas reappear in items; grep confirms zero `py:NN` in L106-131). |
| 16 | TB-Add-8: per-item Context file path OR evidence-absence | PASS (re-classified) | See Issue #1: every code-surface item gives a path + a re-locate Grep anchor; lens permits approximate line numbers when a search anchor is present. Anchors present throughout. |
| 17 | FROZEN-SIGNATURE protected (class-attr not kwarg; 1.7 tripwire) | PASS | Step 1.4 (L173) mandates class-level `quiet: bool = False`, EXPLICITLY forbids an `__init__` kwarg; Step 1.7 (L185) re-runs `test_frozen_signatures_unchanged`. Verified vs test_run_tui_integration.py:622 asserting `["self","max_workers"]`. |

## Source-Truth Verification (live code cross-checks)
| Claim in task | Live evidence | Result |
|---|---|---|
| `ParallelExecutor.__init__(self, max_workers=10)` frozen | parallel.py:100 + test L622 asserts `["self","max_workers"]` default 10 | TRUE |
| Live() ctor in tui.py lacks redirect args | tui.py:221 `self._live = Live(` | location TRUE |
| dispatch `parallel_executor or ParallelExecutor(...)` | dispatch.py:424 | TRUE — `or` means `executor.quiet=True` flip covers BOTH injected + fresh (Step 1.6 claim sound) |
| DRIFT-4: Exit(130) BEFORE exc_box re-raise | commands.py:1986 (Exit 130) precedes 1990-1991 (exc_box raise) | TRUE — reorder is correct fix |
| DRIFT-3: readers outside the update try/except | commands.py:1944-1945 at loop level; try wraps only `tui_obj.update` | TRUE |
| Prints at ~110-232 in ParallelExecutor | parallel.py:110,111,164,165,176,177,183,191,196-200,225,232 | TRUE |
| `_TuiSymbolVisitor` + audit test | test_inv012_tui_opt_in.py:600,655 | TRUE |
| read_state raises in state.py | state.py:178 | exists |

## Summary
- Checks passed: 16 / 17 lens checks (TB-Add-8 re-classified to PASS on lens-tolerance grounds)
- Checks failed: 1 (TB-Add-7, marginal — substantive invariant satisfied)
- Additional content issue: 1 (DRIFT-1 note factual imprecision)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | NOTE (downgraded) | Steps 1.3,1.5,2.1,2.2 (L169,177,193,197) | Cited "around lines NNN" anchors are approximate vs live (1.3 Live "221-226"→actual 221; 2.2 "1984-1994"→Exit130 at 1986, exc_box 1990; 2.1 "1943-1995"→while at 1943). All within tolerance AND each item supplies a re-locate Grep anchor, which TB-Add-8 explicitly permits. Not a defect. | None required; anchors present. Informational. |
| 2 | IMPORTANT | Execution Context L115-122 | TB-Add-7 heading-token drift: section uses `### Source Areas` rather than the canonical `**Source areas:**` line the check keys on. Substantive invariant HOLDS — all six areas (tui.py, parallel.py, dispatch.py, commands.py, state.py, tests/swarm/) reappear in item Contexts, and the header carries NO file:line cites (grep: zero `py:NN` in L106-131). Only the heading FORM differs. | Optional: align `### Source Areas` with the `**Source areas:**` convention if the consumer keys on the literal token. Substance correct. |
| 3 | MINOR | Open Questions L317 (DRIFT-1 note) | Factual imprecision: note calls the import at `commands.py:1880` "eager"/module-level. Live code (commands.py:1878-1880) shows it is FUNCTION-LOCAL inside `run_cmd`, preceded by the comment "no Rich/TUI import side effects (FR-2)". The note's CONCLUSION (non-TTY runs still import Rich because the import at L1880 precedes the TTY gate at L1882) is defensible, but the "eager" premise is inaccurate. Out-of-scope note, not an actionable item — low impact. | Reword to "function-local-but-unconditional import at commands.py:1880 (fires before the TTY gate)" rather than "eager". Documentation-only. |

## Confidence Gate
- [x] VERIFIED: items 1-14, 16, 17 (tool evidence cited above)
- [x] VERIFIED (failing): item 15 (TB-Add-7) — condition verified, marginal drift confirmed
- [?] UNVERIFIABLE: 0
- [ ] UNCHECKED: 0

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 5 (each Bash batched targeted greps against the specific surfaces under verification — frozen sig, dispatch call site, Live ctor, poll loop, print locations, audit test, DRIFT-1 region)

Adversarial-mandate note: 3 issues surfaced. On rigorous re-examination against the lens's own tolerances, Issue #1 is within-tolerance (downgraded to NOTE) and Issue #2's substantive invariant is satisfied (only heading form drifts). Issue #3 is a genuine factual imprecision in an out-of-scope note. The task is structurally sound and EXECUTABLE; the FAIL verdict is driven by the zero-tolerance rule on cosmetic heading-form drift, not by any execution-blocking defect.

## Recommendations
- The task is EXECUTABLE as written — no defect would block or misdirect the executor. Source surfaces, frozen-signature protection, FR-5/REG-1 fix shapes, and POST-reflect form are all correct and verified against live code.
- Optional cosmetic fixes before execution: (a) align the `### Source Areas` heading with `**Source areas:**` (Issue #2); (b) reword the DRIFT-1 out-of-scope note for factual precision (Issue #3). Neither is execution-blocking.
- Strict zero-tolerance read: FAIL requiring one cosmetic fix cycle. Execution-impact read: effectively PASS-with-cosmetic-notes.

## QA Complete

---
VERDICT: FAIL — 0 CRITICAL, 1 IMPORTANT (TB-Add-7, marginal/substantively-satisfied), 1 MINOR (DRIFT-1 note), 1 NOTE (downgraded). No execution-blocking defects; FAIL driven by the zero-tolerance rule on cosmetic heading-form drift + an out-of-scope-note factual imprecision.
