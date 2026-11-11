# Refactoring Plan

## Overview
- Base variant: Variant 1 (reviewer-1, sonnet/analyzer) — adversarial/variant-1-original.md
- Incorporated variants: Variant 2 (reviewer-2), Variant 3 (reviewer-3), Round 2.5 invariant probe
- Planned changes: 12
- Rejected changes: 2
- Overall risk: Low (additive findings and grade changes; no base finding is removed except one withdrawn half)
- Output: merged reviewer card `../merged-verdict.md` (verdict FAIL, merged findings M-F1..), keeping the base card's field shape (id, grade, class, claim, evidence, tag, fix)

## Planned Changes

### Change #1: Strengthen the C-001 fix with V3's set edit and the plan:119 rewrite
- Source: V3 R3-F1; Round 2.5 INV-001; debate C-001 (V3 95%), A-001 (85%)
- Target: base R1-F1 fix field
- Approach: replace — fix becomes: in Task 5 add `"spec-panel-minfix"` to `_POST_REFRESH_ADDITIONS` in tests/recommend/test_routing_refresh.py (with a comment naming issue #346), add that file to the plan:124 regression run and to the files Task 5 touches, and rewrite plan:119 so this one listed test edit is allowed instead of "stops this task as blocked"; flag the edit to the owner as one source.md does not list. Drop test_model_alias_policy.py from the fix (X-002).
- Rationale: unanimous blocking; INV-001 HIGH shows the base fix alone cannot pass because plan:119 forces a stop
- Risk: Low

### Change #2: Add C-002 as a blocking finding
- Source: V2 R2-F1 plus Round 2 V2 (d) rebuttal; debate C-002 (V2 100%), A-002
- Target: new finding after R1-F1
- Approach: insert — reviewer-side "An exit 2 from the reviewer's own call is corrected once and re-run" (source.md:46) is absent from the literal block the plan ships (source.md:120 handles exits 3/4/5/70; the retry exists only for the reviser at source.md:127; plan:117 copies the block). Fix: append one owner-decision sentence inside the existing source.md:120 paragraph in Task 5 Region 4 (same channel plan:117 uses), add a pin in tests/skills/test_spec_panel_minfix.py; Task 7 inherits via its byte-identity AC (plan:147). Note: the auditor's own coverage matrix wrongly credited Task 8; that is an audit artifact error, not a plan claim (V2 conceded).
- Risk: Low

### Change #3: Add INF-032 as a blocking finding
- Source: Round 2.5 INV-003 (HIGH); T1 card INF-032
- Target: new finding after Change #2
- Approach: insert — source.md:46 "At `review: 3` the run escalates as 427 says, now also listing each budget escalation with its need and each `GRADE-CONFLICT`" has no plan task; Review Loop bullet 4 (spec-panel.md:261) escalates only "with the open blocking findings". Fix: one owner-decision sentence appended inside the same paragraph as Change #2, plus a pin.
- Risk: Low

### Change #4: Add C-009 as a blocking finding
- Source: V3 R3-F3 (upgraded by V3 in Round 1, calibrator), Round 2.5 INV-005, INV-006
- Target: new finding
- Approach: insert — importlib loading (plan:50) writes `scripts/__pycache__/*.pyc` carrying the absolute path; Task 4's `grep -rn 'src/superclaude' src/superclaude/skills/sc-fixcheck` (plan:104) then matches. Fix: use `grep -rnI --exclude-dir=__pycache__` in the Task 4 AC (works regardless of when the .pyc was written, INV-005); optionally set `sys.dont_write_bytecode` in the test; note the install copy (`cp -rn`, install_skill.py copytree) carries the harmless .pyc, or exclude it.
- Risk: Low

### Change #5: Carry INV-002 into R1-F2 (500-line ceiling)
- Source: Round 2.5 INV-002; debate C-004 (V1 90%)
- Target: base R1-F2 fix field
- Approach: append — the Change #2/#3 sentences must be appended inside existing paragraphs, since the variant already lands at exactly 500 lines; keep the `wc -l` <= 500 AC and `make lint-architecture`.
- Risk: Low

### Change #6: Add INV-004 (second exit 2 undefined) as a minor finding
- Source: Round 2.5 INV-004 (LOW)
- Approach: insert — state that a second exit 2 is handled like exit 3 (stop and escalate), in the Change #2 sentence.
- Risk: Low

### Change #7: Narrow R1-F6 to the 40-character rule
- Source: debate C-012 (V1 80%), V1 concession
- Approach: replace — drop the skill-path half (covered by plan:104); keep source.md:224 "40-character unique-substring quote match" vs plan:63.
- Risk: Low

### Change #8: Add Round 2 evidence to R1-F7
- Source: Round 2 V1 rebuttal (c)
- Approach: append — plan:52 pattern `^(import|from) ` is column-0 anchored and misses function-level imports; plan:50 subprocess runs only `hash`.
- Risk: Low

### Change #9: Add C-003/X-001 as a minor finding (declared deviation)
- Source: V2 R2-F2 reframed per V3 (debate C-003 V3 80%, X-001 V3 75%)
- Approach: insert — source.md:90 says "the first implementation task runs them"; the plan runs them in Task 5 (plan:119, :124), a necessary move (nothing to trip before Task 5) that the plan does not declare. Fix: state it as a deviation in Constraints.
- Risk: Low

### Change #10: Add C-008 (path-order pin ambiguity) as a minor finding
- Source: V3 R3-F2, narrowed (substring half dropped)
- Approach: insert — a whole-file reading of plan:122 fails on spec-panel.md:262 (project path first in bullet 5); scope the check to `## Fix Budget` with lookbehind `(?<!~/)\.claude/skills/sc-fixcheck/`; same for Task 4 (plan:103).
- Risk: Low

### Change #11: Add C-010 and C-011 as minor findings
- Source: V3 R3-F4, R3-F5 (+ Round 2 V3 (c))
- Approach: insert — probe fixtures for INSTALL.md (plan:163 vs Task 8 file list plan:158); write-verb audit constraint (test_worker_contract.py:1940-1950), Task 4 does not run that test (plan:106).
- Risk: Low

### Change #12: Merge self-audits and calibration notes; set verdict
- Source: all three self-audits; Round 2.5 INV-006, INV-007 (ADDRESSED enumerations)
- Approach: restructure — one Self-Audit listing what was verified (task order; tests that enumerate commands/skills and why they pass; sync targets skip __pycache__; brief sources exist; substitution holds) and what was not (95f2c6e4 bullet text, no tests run). verdict: FAIL; blocking count 4.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| X-002 | Add tests/skills/test_model_alias_policy.py to the regression run (originally V1's own) | Unanimous exclude: the test scans the new files but no assertion trips on them (Round 2 V1 (d)) |
| C-003 (as V2 originally framed) | Run the check-first tests at the start of Task 1 | Unanimous: before Task 5 nothing exists to trip them; kept only as a declared-deviation note (Change #9) |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| #1-#4 | Low | Adds/changes blocking findings the debate agreed unanimously or the probe raised HIGH | Remove the finding |
| #5-#12 | Low | Minor findings and wording | Remove the finding |

## Review Status
- Approval: auto-approved (non-interactive; `--interactive` not set; unattended)
- Timestamp: 2026-11-08T18:55:00Z
