# QA Report — Task File Qualitative Review

**Topic:** Remediate validated PR #112 + #111 review findings R1-R5
**Date:** 2026-06-02
**Phase:** task-qualitative
**Fix cycle:** N/A (initial)
**Fix authorization:** true

---

## Overall Verdict: FAIL (3 issues found — ALL FIXED IN-PLACE)

A FAIL verdict is rendered because issues were found (no severity level is exempt per
the task-qualitative gate). All three issues were fixed in-place in the task file under
`fix_authorization: true`. After the fixes, the task is operationally sound and would
succeed if executed. Re-running the gate against the patched task would PASS.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | All make targets / pytest / grep / probe commands map to real preconditions; UV-only honored; `python -m` only under `uv run` (sanctioned). |
| 2 | Project convention compliance | none | PASS | R4 edits src/ skill side + `make sync-dev`/`make verify-sync` (5.8); never stages `.claude/`; MD body only in contracts.ID_PATTERNS; arch_lint scope (src/cli/) means tools/ + contracts/ edits cannot self-trip. |
| 3 | Intra-phase execution order simulation | AX-3 | FAIL→FIXED | Phase 4 ordering OK (4.5 field before 4.6-4.8 consumers), but missed envelope.py/test_pipeline_envelope construction sites — see Issue #1. Fixed. |
| 4 | Function signature verification | none | PASS | `_roadmap_ids_within_spec`→`bool\|str` (gates.py:1052); `execute_roadmap(config, resume=False,…)` (L3399); fail-shut `payload.get(...,())` (L1069-1098); all R2/R5 anchors resolve. |
| 5 | Module context analysis | none | PASS | `ID_PATTERNS` Final dict (L64-70), anchor-free bodies confirmed; `_REQUIREMENT_PATTERNS` comprehension (L329); canonicalizer (L295) reviewed. |
| 6 | Downstream consumer analysis | AX-3 | FAIL→FIXED | `to_dict()` adds md_ids → consumers: gates read (4.9 ✓), schema tests (4.10 ✓), conftest (4.11 ✓) — BUT envelope.py `envelope_from_dict` + test_pipeline_envelope NOT traced. See Issue #1. Fixed. |
| 7 | Test validity | none | PASS | R5 oracle tests ported verbatim from 861047c2; R2 single-test-body regression correctly avoids autouse-reset masking; R4 behavioral fail-before/pass-after. |
| 8 | Test coverage of primary use case | none | PASS | R5 reproduction (Phase 2) + ported oracle tests + disk fixture (4.13) cover the M{n}-D{nn} primary case end-to-end; R2 cross-run leak covered. |
| 9 | Error path coverage | none | PASS | R4 malformed-EXCLUDE error path is the whole point of the fix; R2 preserves fail-shut STRING on None/missing/unreadable/malformed. |
| 10 | Runtime failure path trace | AX-1 | FAIL→FIXED | R4 caller `exit 1 + diagnostic` is dead code under `set -e` command-substitution — see Issue #2. Fixed. |
| 11 | Completion scope honesty | none | PASS | R5 decision gate genuinely branches on captured evidence; CLOSE/PROCEED both fully handled; Open Questions resolved in-task by Phase 2/3; R3 honestly droppable. |
| 12 | Ambient dependency completeness | none | PASS | imports/setter import pattern (executor.py:662); arch_lint green item (4.15); sync (5.8). Construction-site gap is the AX-3 issue, now fixed. |
| 13 | Kwarg sequencing red flags | none | PASS | Field added (4.5) BEFORE consumers (4.6-4.8); no "pass kwarg before signature" inversion. |
| 14 | Function existence claims verified | none | PASS | All "exists at X" / "absent" claims grep-verified: ID_PATTERNS, _REQUIREMENT_PATTERNS, _canonicalize_requirement_id, check_signatures, _isolate_gates_state, _merge_gate_id_registry_sidecar, schema tests, _write_id_fixture, scan_file/ast.walk/Rule2, recurrence_case, fixtures all present. Absent: md_ids/MD/_MD_TRAILING_D_RE/_NON_REF (correctly claimed absent). |
| 15 | Cross-reference accuracy | AX-1 | FAIL→FIXED | Step 4.1 rationale ("dict ordering gives MD precedence") is inaccurate vs actual extract_requirement_ids semantics — see Issue #3 (MINOR). Fixed. |

## Summary
- Checks passed: 12 / 15 (3 failed then fixed in-place)
- Checks failed: 3 (all FIXED)
- Critical issues: 1 (FIXED)
- Important issues: 1 (FIXED)
- Minor issues: 1 (FIXED)
- Issues fixed in-place: 3

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 4.5 (R5 path-b lockstep) | `SpecIdRegistry(` has FIVE construction sites, not three. Adding a required `md_ids` field breaks `envelope.py:381` (`envelope_from_dict`) and `tests/roadmap/test_pipeline_envelope.py:62` (`sample_envelope` fixture) with `TypeError: missing required arg 'md_ids'`. These R1.2-PipelineEnvelope sites (commit 90a8fa67, landed after PR #111/#112; research inventory missed them) are NOT in the path-b lockstep → runtime TypeError + failing envelope test surfacing as a Phase-6 baseline regression with NO item to fix it. | Added explicit envelope.py + test_pipeline_envelope.py coverage into Step 4.5 (anchor by `def envelope_from_dict` / `spec_ids = SpecIdRegistry(`; add `md_ids=tuple(spec_ids_d.get("md_ids", ()))`; and `def sample_envelope` add `md_ids=(...)`). Also added `test_pipeline_envelope.py` to the Step 4.14 mandatory test surfaces. |
| 2 | IMPORTANT | Step 5.7 (R4 shell fix) | Under `#!/bin/sh` + `set -e`, the callers use `FILE_LIST=$(… \| apply_scope)` command substitution. A non-zero substitution aborts the script IMMEDIATELY at the assignment — before any caller-side `rc=$?` + `exit 1` diagnostic runs. So the prescribed "capture rc after substitution, then exit 1 naming SCOPE.md" is UNREACHABLE dead code; the SCOPE.md-naming diagnostic (an explicit acceptance criterion) NEVER fires (operator sees only grep's raw "Invalid regular expression" + exit-2). Verified by shell simulation. | Rewrote Step 5.7 to mandate the `if FILE_LIST=$(… \| apply_scope); then :; else rc=$?; if [ "$rc" -ge 2 ]; then echo "ERROR: … in $SCOPE_FILE" >&2; exit 1; fi; fi` construct (the `if`-condition is the only context that suppresses `set -e` for a non-zero substitution), applied at BOTH L49 and L66; verified working by simulation (exit 1 + diagnostic fires). |
| 3 | MINOR | Step 4.1 (MD contracts entry) | Rationale claims ordering `"MD"` before `"D"` "assigns MD precedence over bare-D" in the spec_parser dict-comprehension. Verified false: `extract_requirement_ids` iterates each family pattern independently into its own result key; the bare-D pattern still matches `D01` inside `M1-D01` regardless of order. The real dedup is the `_MD_TRAILING_D_RE` strip pass in Step 4.2. Misleading rationale could lead the executor to rely on ordering and skip/weaken the 4.2 dedup. | Added accuracy note clarifying ordering is cosmetic/convention only and Step 4.2 is the mechanism that closes the FP. |

## Actions Taken (fix_authorization: true)
- Fixed Issue #1 (CRITICAL) in Step 4.5 by adding the two missing `SpecIdRegistry(...)` construction-site updates (envelope.py `envelope_from_dict` + test_pipeline_envelope.py `sample_envelope`) with `.get("md_ids", ())` round-trip safety, plus a blast-radius note; and added `test_pipeline_envelope.py` to Step 4.14's mandatory test surfaces.
  - Verified by: `grep -rn "SpecIdRegistry(" src/ tests/` (5 sites), `Read envelope.py:370-399`, `Read test_pipeline_envelope.py:55-75`.
- Fixed Issue #2 (IMPORTANT) in Step 5.7 by replacing the dead-code caller guard with the `set -e`-safe `if FILE_LIST=$(…); then :; else rc=$?; …` construct at both callers.
  - Verified by: two shell simulations (`/tmp/r4test2.sh` reproduced the abort-before-diagnostic; `/tmp/r4fix.sh` confirmed the corrected construct emits the SCOPE.md diagnostic and exits 1).
- Fixed Issue #3 (MINOR) in Step 4.1 by appending an accuracy note correcting the dict-ordering "precedence" claim.
  - Verified by: `Read spec_parser.py:329-346` (independent per-family iteration).

## Core Semantic Checks (from spawn prompt) — Results
1. **R2 operational reality:** PASS. Traced execute_roadmap real flow: dry-run early-return guard (L3492) → `if resume: _apply_resume` (L3497-3500) → `execute_pipeline` (L3539). Step 5.3's insertion window (after dry-run return, before execute_pipeline) exists and anchors resolve. Resume-awareness (reset-only-when-extract-runs OR re-derive from existing sidecar JSON) is implementable from the post-`_apply_resume` `steps` list. Fail-shut (gates.py:1069-1098) and `Callable[[str],bool\|str]` signature preserved as instructed.
2. **R5 reproduce step:** PASS. Live probe on THIS branch returned `{'D': ['D01','D02']}` — confirms the tokenizer extracts bare-D from `M{n}-D{nn}` AND collapses `M1-D01`/`M2-D01` to a single `D01`. No other code path already handles MD (greps confirm absence). The decision gate (Step 3.1) has a real, evidence-evaluable criterion (phantom_id/id_schema_drift attributable to milestone mis-tokenization).
3. **R5 path-b lockstep:** FAIL→FIXED. Original 7-site lockstep (field/union/to_dict/build/gates-read/schema-tests/conftest) covered all sites the research found, BUT missed two real `SpecIdRegistry(` sites in the R1.2 envelope (Issue #1). Now covered.
4. **R4 exit-2 under sh+set -e:** FAIL→FIXED. The original mechanism is shell-incorrect (dead-code guard, Issue #2). Corrected construct verified working by simulation.
5. **QA/VALIDATION/TESTING requirements present:** PASS. FINAL_ONLY QA gate = Phase Gate PG.1-PG.3 (rf-qa task-integrity). VALIDATION = make lint-architecture (6.1) + make verify-sync (6.2) + baseline-delta (6.3). TESTING per surface = 4.14 (R5, now incl. envelope), 5.2 (R1), 5.6 (R2), 5.9 (R4 behavioral), 5.12 (R3), 6.3 (full suite). All present.
6. **Make-target/command precondition ordering:** PASS. Phase 1 captures baseline before edits; 5.8 sync-dev precedes 6.2 verify-sync; 6.1/6.2/6.3 after all edits; R5 reproduction (Phase 2) before decision (Phase 3) before impl (Phase 4). No command depends on an unsatisfied earlier precondition.

## Self-Audit (PR-04 / INV-019)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS #1 (frontmatter), #2 (no items before Phase 1), #3 (item self-containment), #4 (R5 granularity), #7 (Open Questions present), #9 (item count), TB-Add-1..8 (TBD/bounds/DAG/XL-split/uniform-verify/exec-context/file:line) — did not re-verify document structure, section numbering, or item shape.

**(b) Independent semantic checks where rf-qa PASS was INSUFFICIENT and my own tool work was required:**
- rf-qa #5 marked "Evidence-based; paths re-anchored by symbol = PASS." INSUFFICIENT: rf-qa verifies anchors RESOLVE, not that the lockstep is COMPLETE. My `grep -rn "SpecIdRegistry("` found 5 construction sites; the task covered 3 explicitly + 2 in-scope target files, MISSING envelope.py:381 and test_pipeline_envelope.py:62 → CRITICAL Issue #1. Tool evidence: `grep` (5 hits), `Read envelope.py:370-399`.
- rf-qa #6 marked "No items on contradicted findings; absent _MD_TRAILING_D_RE = PASS." INSUFFICIENT: structural absence-of-finding ≠ operational correctness of the proposed fix. My shell simulation of the R4 caller under `set -e` proved the prescribed mechanism is dead code → IMPORTANT Issue #2. Tool evidence: `Bash /tmp/r4test2.sh` (abort-before-diagnostic), `/tmp/r4fix.sh` (corrected works).
- rf-qa #3 marked "items self-contained = PASS." INSUFFICIENT: self-contained ≠ technically accurate. My `Read spec_parser.py:329-346` showed Step 4.1's "dict ordering = precedence" rationale is false → MINOR Issue #3.

## Confidence
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 4 | Glob: 0 | Bash: 6
- Tool-engagement note: (Read+Grep+Glob+Bash) = 19 ≥ 15 checklist items. Every call mapped to a specific check (source-file reads for signature/module/existence verification; greps for construction-site/anchor enumeration; bash for runtime FP probe + shell-correctness simulation). No padding calls.
- Web research: none performed (all verification was local-file + runtime-probe bound). Tavily-first rule N/A this review.

## Self-Audit (mandatory questions)
1. Independently verified ~30+ factual claims against source (every anchor line, every construction site, the live tokenizer behavior, the shell semantics).
2. Files read: contracts/__init__.py, id_registry.py, repo-inventory.sh, spec_parser.py, structural_checkers.py, executor.py (3 regions), conftest.py (2 regions), test_spec_roadmap_id_containment.py, envelope.py, plus greps across src/ and tests/.
3. Not a 0-issue review — found 3 issues including a CRITICAL blast-radius omission and an IMPORTANT shell-correctness defect, both proven with tool evidence (grep enumeration + executed shell simulations), not asserted.
4. No web research performed; Tavily-first N/A.

## Recommendations
- The task is now executable as patched. The executor should pay particular attention to: (a) running `test_pipeline_envelope.py` under PROCEED (now in 4.14); (b) using the `if FILE_LIST=$(…); then…else` construct for R4 (Step 5.7); (c) treating Step 4.1 ordering as cosmetic and relying on Step 4.2 for the FP fix.
- MINOR watch-item (not blocking, no fix applied): Step 4.13's new recurrence fixture coexists with the existing `spec_roadmap_drift_case.expected.json` (which lacks `md_ids`). The `recurrence_case` loader returns the raw expected dict; comparison is per-test. If any consuming test does full registry-dict equality, the existing fixture's expected.json may need `md_ids` too. The executor should confirm during 4.14 that no existing recurrence test breaks.

## QA Complete

VERDICT: FAIL (3 issues found: 1 CRITICAL, 1 IMPORTANT, 1 MINOR — ALL FIXED IN-PLACE). No unfixable issues. Task is operationally sound as patched; a re-run of the gate would PASS.
