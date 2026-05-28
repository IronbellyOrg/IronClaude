# QA Report — task-qualitative

**Topic:** PR #71 review remediation — TASK-RF-20260521133223
**Date:** 2026-05-21
**Phase:** task-qualitative
**Fix cycle:** 1

---

## Overall Verdict: FAIL

Three issues found (1 CRITICAL, 1 IMPORTANT, 1 MINOR). All three were fixed
in-place in the task file (fix_authorization: true). The verdict is FAIL per
the protocol (any issue = FAIL); the fixes are documented in Actions Taken.
A re-review after the applied fixes finds no unresolved issues.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-4 | FAIL | Step 8.3 smell-check (c) grep pattern `'\[\*:\\\\s\]\*'` returned exit 1 / 0 matches against CURRENT pre-refactor gates.py (verified: `git grep -n '\[\*:\\\\s\]\*' src/superclaude/cli/prd/gates.py` → exit 1). The literal in gates.py:50 is `[*:\s]*`. A check returning 0 even before the refactor cannot verify the refactor happened. |
| 2 | Project convention compliance | none | PASS | Task touches only `src/superclaude/cli/prd/` + `tests/cli/prd/`; never edits `.claude/` copies. `uv run pytest` used throughout (Steps 2.8, 3.6, 4.3, 5.2, 6.2, 7.4, 8.1). `make lint` used (8.2). Tests placed in `tests/cli/prd/` mirroring src. |
| 3 | Intra-phase execution simulation | none | PASS | Phase 1 captures symbol anchors before Phases 2-7 rely on them (Step 1.4 writes symbol-anchors.md). Phase 2 creates `_artifact_patterns.py` (2.1) before rewiring callers (2.2-2.7). |
| 4 | Function signature verification | none | PASS | All targeted symbols verified to exist at HEAD 7c4b26b0: `_check_verdict_field` gates.py:36; `_build_prompt` executor.py:1068; `_STAGE_A_STEPS` executor.py:362; `_execute_stage_b` executor.py:710; `build_investigation_prompt` prompts.py:572; `build_web_research_prompt` prompts.py:692; `build_synthesis_prompt` prompts.py:901; `_parse_agent_block` prompts.py:535; `build_task_file_prompt` prompts.py:316; `build_assembly_prompt` prompts.py:1093; `resume` commands.py:171. |
| 5 | Module context analysis | none | PASS | Step 3.1 instructs adding `import inspect`; Step 2.2 adds the `_artifact_patterns` import block. `_parse_agent_block`/`_slugify_agent_title` correctly noted as existing shared helpers (prompts.py:535,563). |
| 6 | Downstream consumer analysis | AX-3 | FAIL (folded into issue 2) | Phase 2 rewires both WRITE side (prompts builders) and READ side (executor Stage B detection). The real omission is in `_build_prompt`'s relation to the dual-mode builders — see item 13 / issue 2. |
| 7 | Test validity | none | PASS | Step 7.1 case (10) requires a real `buggy_builder` raising TypeError and asserts propagation; Step 7.2 case (7) does a real rename to prove RE authority. Tests exercise real behavior, not stubs. |
| 8 | Test coverage of primary use case | none | PASS | Step 7.1 covers config-mode dispatch end-to-end for all three builders; Step 7.2 covers `PrdExecutor.run()` + `_execute_stage_b` with realistic on-disk artifacts. H1's `_build_prompt` smoke test met by case (10). |
| 9 | Error path coverage | none | PASS | Step 7.1 cases (4)(5) cover missing-Agent-N and boundary false-match; Step 3.5 preserves the single fallback `except TypeError`. |
| 10 | Runtime failure path trace | AX-2 | FAIL (same root as item 1) | Trace: Phase 5 tightens the regex; Step 8.3 (c) is the ONLY gate verifying the over-loose form is gone. Malformed grep breaks `Phase 5 edit → Step 8.3 (c)` verification — (c) would report PASS regardless. |
| 11 | Completion scope honesty | none | PASS | No Open Questions flagging unknowns; spec §8 Open Decisions resolved and cited (2.1→OD#1, 3.1→OD#2, 7.1→OD#3). L3 correctly excluded. |
| 12 | Ambient dependency completeness | none | PASS | `_artifact_patterns.py` is a new internal module imported by `prompts.py` (2.2) and `executor.py` (2.5); no `__init__.py` export needed (underscore-private relative import). Frontmatter update protocol present. |
| 13 | Kwarg sequencing red flags | AX-2 | FAIL (drove issue 2) | Step 3.5's prescribed `inspect.signature` dispatch checks for a param "named `config`". The three dual-mode builders are `def build_*(*args, **kwargs)` — `inspect.signature` yields only VAR_POSITIONAL `args` + VAR_KEYWORD `kwargs`, NO `config` param. Literal compliance would route every dual-mode builder to the legacy arm, breaking Stage B. |
| 14 | Function existence verification | none | PASS | All "exists" claims grep-verified (item 4). `_artifact_patterns.py` correctly described as NEW — `ls` confirms absent. |
| 15 | Template cross-references | none | PASS | Spec §-references spot-checked: §4 Cluster 4 = lines 117-146 (task 2.1 cites 117-146 ✓); §4 Cluster 2 helper sig lines 76-91 (task 3.1 ✓); §4 Cluster 3 lines 113-115 (task 7.3 ✓). |

## Summary
- Checks passed: 11 / 15
- Checks failed: 4 (items 1, 6, 10, 13 — items 1 & 10 share one root cause; items 6 & 13 drove issue 2)
- Critical issues: 1
- Important issues: 1
- Minor issues: 1
- Issues fixed in-place: 3
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 5 | Grep/Bash: 4 | Glob: 0

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 8.3 smell-check (c) | `git grep -n '\[\*:\\\\s\]\*' src/superclaude/cli/prd/gates.py` returns 0 matches against the CURRENT pre-refactor source (verified `exit 1`). The literal in gates.py:50 is `[*:\s]*`. The task copied spec §6 line-206's pattern verbatim; that pattern is wrong for the actual literal. A smell-check returning 0 BEFORE the refactor cannot prove Phase 5 landed — a partial/failed Phase 5 would still pass the final gate. | Replace with a fixed-string grep matching the actual literal: `git grep -nF '[*:\s]' src/superclaude/cli/prd/gates.py | wc -l` — verified returns `1` on current source (correctly detects the smell), must return `0` after Phase 5. |
| 2 | IMPORTANT | Step 3.5 | Step 3.5 instructs branching on "a first parameter named `config`". The three dual-mode builders are `def build_*(*args, **kwargs)` (verified prompts.py:572-575, 692-695, 901-904) — `inspect.signature` exposes only VAR_POSITIONAL `args` + VAR_KEYWORD `kwargs`, no `config` param. An implementer following the literal instruction routes every dual-mode builder to the LEGACY positional arm, breaking Stage B. | Add explicit guidance: dual-mode builders keep `(*args,**kwargs)` post-Phase-2 (spec §2 Non-Goals); the inspect-signature branch must treat a VAR_POSITIONAL/VAR_KEYWORD-only builder as a config-form builder and call `builder_fn(config=self._config, step_id=step_id)`. The named-`config` branch applies only to static Stage-A builders. |
| 3 | MINOR | Step 3.5 phrasing | Step 3.5 propagates spec §4 Cluster 2 line-90's imprecision verbatim ("config-typed first parameter") without reconciling it against the actual `(*args,**kwargs)` shape. | Covered by the issue-2 fix (same Edit). |

## Actions Taken
- **Fixed issue 1 (CRITICAL)** — Edited Step 8.3 smell-check (c): replaced
  `git grep -n '\[\*:\\\\s\]\*' ... | wc -l` with
  `git grep -nF '[*:\s]' src/superclaude/cli/prd/gates.py | wc -l` and added a
  NOTE explaining it is a literal fixed-string match returning `1` pre-refactor
  and `0` post-Phase-5. Verified the replacement detects the smell on current
  source (`git grep -nF '[*:\s]' src/superclaude/cli/prd/gates.py` → 1 match).
- **Fixed issues 2 & 3 (IMPORTANT + MINOR)** — Edited Step 3.5: added a CRITICAL
  paragraph stating the dual-mode builders retain `(*args,**kwargs)` signatures
  post-Phase-2, and the `inspect.signature` dispatch must route
  VAR_POSITIONAL/VAR_KEYWORD-only builders to the config-form call (relying on
  the builder's internal `hasattr(config,"task_dir")` probe), never the legacy arm.

## Five Adversarial Axes — Coverage Summary
- **AX-1 Drift:** ACTIVE (GOAL captured verbatim in task R-001 / spawn TRACK GOAL).
  No task-side drift — scope matches the 11 findings; verbs preserved. Note:
  review M3 cites `prompts.py:856` for `build_synthesis_prompt` but actual is
  line 901 — a stale citation in the REVIEW; the task correctly uses 901.
- **AX-2 Contradictions:** fired on items 10 & 13 — Step 3.5's inspect-signature
  dispatch contradicts the actual `(*args,**kwargs)` builder shape (issue 2).
- **AX-3 Omissions:** fired on item 6 — folded into issue 2.
- **AX-4 Weakened criteria:** fired on item 1 — smell-check (c) is a
  trivially-passing verification (passes regardless of whether Phase 5 ran).
- **AX-5 Invented content:** none. Every named artifact traces to the spec or
  codebase. No scope creep; L3 correctly has zero items.

## Findings → Items Coverage Map
| Finding | Resolving Phase/Step | Status |
|---------|---------------------|--------|
| H1 (dual-mode test gap) | Phase 7 Steps 7.1, 7.2 (case 10 = `_build_prompt` smoke) | Covered |
| M1 (verdict regex) | Phase 5 Step 5.1 | Covered |
| M2 (triple except TypeError) | Phase 3 Step 3.5 | Covered (issue-2 caveat now fixed) |
| M3 (dispatch boilerplate ×3) | Phase 3 Steps 3.1-3.4 | Covered |
| M4 (resume-skip test gap) | Phase 7 Step 7.2 | Covered |
| M5 (resume docstring) | Phase 6 Step 6.1 | Covered |
| M6 (filename coupling) | Phase 2 Steps 2.1-2.7 | Covered |
| M7 (`*args/**kwargs` typing) | Phase 3 Steps 3.1-3.4 (consolidation; signatures kept per spec §2) | Covered |
| L1 (assembly glob depth) | Phase 4 Step 4.1 | Covered |
| L2 (read-before-name-check) | Phase 4 Step 4.1 | Covered |
| N1 (existing_note inline blocks) | Phase 4 Step 4.2 | Covered |
| L3 (path validation) | none | Correctly deferred |

All 11 in-scope findings have ≥1 resolving item. L3 has none (correct).

## Self-Audit
1. **Factual claims independently verified against source:** 15+ — every symbol
   existence claim (11 symbols / 4 files), the three `except TypeError` line
   positions, the `p.name[:2].isdigit()` location, the two `glob()` literals,
   the verdict regex literal, the test-directory layout, the existing
   `TestCheckVerdictField` class, and all three `git grep` smell-check patterns
   executed against live source.
2. **Files read:** prompts.py (full, 1406 lines), gates.py (full, 509 lines),
   commands.py (full, 216 lines), executor.py (full, 1179 lines), the task file
   (full, 382 lines), both research files, plus `tests/cli/prd/test_gates.py`
   and `test_resolve_step_content.py` heads via Bash.
3. **Why trust this review found real issues:** the CRITICAL finding was found
   by actually executing the task's own smell-check command and observing exit
   code 1 — a verbatim adversarial dry-run, not a reading judgment. The
   IMPORTANT finding was found by reading the actual `(*args, **kwargs)`
   declarations and reasoning about `inspect.signature` output.

### Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
**(a) Reliance list — rf-qa A.10 PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for Check 3 (checklist items self-contained).
- Relied on rf-qa PASS for Check 6 (sequencing honors spec §5).
- Relied on rf-qa PASS for Check 9 (no contradicted findings; L3 deferred).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Sequencing soundness (semantic counterpart of Check 6/8): rf-qa verified DAG
  structure; I independently verified the ordering hazard — Phase 3 edits the
  same three builders Phase 2 rewired — by reading prompts.py and confirming
  Phase 2's import-block (Step 2.2) is a prerequisite for Step 3.1. Sound.
- Finding-coverage completeness (semantic counterpart of Check 9): built the
  Findings→Items map above by reading each phase's items; all 11 in-scope
  findings resolve, L3 correctly absent.
- Executability (no structural analogue): grep-verified all 11 targeted symbols
  exist at HEAD 7c4b26b0 — a check rf-qa's structural pass does not perform.

## Recommendations
- The three issues are now fixed in the task file. A fix-cycle re-review of the
  edited task file finds no unresolved issues.
- During execution, the implementer must heed the Step 3.5 clarification: the
  `inspect.signature` dispatch must not route dual-mode builders to the legacy arm.

## QA Complete

VERDICT: FAIL
