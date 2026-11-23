# QA Report - Task Integrity (lens b2-self-containment)

**Topic:** observer visual parity tech-research task file
**Date:** 2026-11-18
**Phase:** task-integrity (B2 lens)
**Fix cycle:** N/A (fix_authorization: false)

## Scope read

Whole task file read (480 lines, 82 `- [ ]` items, confirmed by `grep -c '^- \[ \]'` = 82). Embedded claims also spot-checked against source (see checklist 7).

## Findings

### B-1 (Blocking) Five cycle-2 fix-agent items do not embed their prompt

| Item | File line | Text that fails B2 / checklist 3 |
|---|---|---|
| Step 3.3, fix cycle 2 (Gate 1) | 180 | "using the same fix-agent prompt as Step 3.2 (...)" |
| Step 5.9, fix cycle 2 (Gate 2) | 258 | "using the same fix-agent prompt as Step 5.8 (...)" |
| Step 6.6, fix cycle 2 (Gate 3) | 310 | "using the same fix-agent prompt as Step 6.5 (...)" |
| Step 6.7, fix cycle 2 (Gate 4) | 336 | "using the same fidelity fix-agent prompt as in the cycle-1 fix item above (...)" |
| Step 6.8, fix cycle 2 (Gate 5) | 360 | "using the same anti-omission fix-agent prompt as in the cycle-1 fix item above (...)" |

Evidence: each item spawns an `rf-qa` agent with `fix_authorization: true` but gives only a parenthetical paraphrase of the cycle-1 prompt, then says "but reading <cycle2 file> and writing its log to <cycle2 log>". Lines 336 and 360 literally say "above". The paraphrase drops parts of the cycle-1 prompt: the opening role sentence, "Fix only blocking findings; leave minor findings as notes", "create it first with Write containing a header only", the per-fix log-line contents, and (Gates 1 and 2) the rules for spawning targeted research agents and the Documentation Staleness Protocol. Line 118 promises every agent prompt is "complete and must be passed ... verbatim"; the executor cannot do that here.

Consequence: in the cycle where a gate is already failing and a HALT is one step away, the fix agent runs on a prompt the executor must rebuild by hand. That risks a fix pass without the self-check or the log-file protocol, and the monotonicity guard then reads an incomplete log. Breaks checklist items 2 and 3 of this lens.

Required fix: write the full fix-agent prompt into each of the five items, with the cycle-2 input and log paths substituted.

### Notes (non-blocking)

| # | Where | Observation |
|---|---|---|
| N-1 | Lines 198, 202 (Steps 4.1, 4.2) | Prompts contain a literal `[paste your 5-10 line summary here]` slot. It is a required runtime substitution, but line 118 says "substituting nothing" and the items say "no placeholder text remains". Workable (the item says to pass the summary in that field) but the statements conflict. |
| N-2 | Lines 316, 340, 364 | Gate-decision items list bare file names (`qa-fix-verification-qualitative.md`, `qa-fidelity-verification-1.md`, ...) after naming the qa directory once. Unambiguous but not absolute per file. |
| N-3 | Lines 240, 322, 324 and the 6.2-6.4 prompts | Prompts say "blocking or minor per I16" (undefined to the spawned agent) and Gate 3 lens prompts carry no PASS/FAIL rule (the rule sits only in the header paragraph at line 276). The agents' own definitions likely cover this and the output format asks for a verdict. |
| N-4 | Lines 212-232 | Synthesis prompts say "write the sections in the exact format they should appear in the final report" but the Report Structure template is not embedded; table shapes are given piecemeal (Step 5.6: "three tables as in the report structure"). Workable because each prompt lists its sections and columns. |
| N-5 | Line 372 (Step 7.1) | One item bundles four verifications (Glob of all outputs, read this file for `[x]`, blocker-resolution check, `git status`). Batch item under checklist 6, but each part has a stated gate and it is a closing validation. |
| N-6 | Lines 376, 384 | Step 7.2 verification ("every statement taken from the report") is not measurable; the NON-BLOCKING suggestion item (384) has no verification (intentional per its text). |
| N-7 | Line 382 vs Builder Notes line 411 | Cross-lens: the final item sets status Done unconditionally while O-1 and OPEN-1 to OPEN-3 are left open by design. This belongs to integrity checklist item 14, not B2; noted for the merge only. |

### Checklist results

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Every item has context, action, output, verification, completion gate | PASS with note | All 82 items end with the "if unable ... log blocker ... Once done, mark complete" gate; each names its output path and a verify clause. Exception: N-6 (item 384). |
| 2 | No item relies on a prior item without restating | FAIL | B-1 (five items). Cycle-2 read/branch items (lines 178, 256, 308, 334, 358) restate the halt guards in full, so they pass. |
| 3 | Agent-spawning items have fully embedded prompts | FAIL | B-1. All other spawn items (2.1-2.5, 3.1 x3, 4.1-4.2, 5.1-5.6, 5.7 x3, 6.1-6.4, 6.6 x2, 6.7 x2, 6.8 x2, cycle-1 fix/verification items, cycle-2 verification items) carry a full prompt. |
| 4 | File paths specific and absolute | PASS with note | N-2. Checked with `ls` / `wc`: the observe source files, `tests/observe` (28 .py plus 2 goldens), visual-parity `inputs/{mockups,current,tools}` and `merged/FINDINGS.md`, the spec folder, `pr-591-comment.md`, `/home/coder/.config/zellij/{config.kdl,themes/aidev02.kdl,layouts/agent.kdl,layouts/default.kdl}` and `/usr/local/bin/zellij` all exist. |
| 5 | Verification measurable | PASS with note | Exact headers, file existence, Status: Complete, counts and verdict strings are checkable; N-6 for Step 7.2. |
| 6 | No batch items | PASS with note | Spawn items are one agent each; N-5 for Step 7.1. |
| 7 | No items based on CODE-CONTRADICTED / UNVERIFIED findings | PASS | `research-notes.md` has no such tags (grep: no matches), so nothing is built on a contradicted claim. Spot check of numbers embedded in prompts: line counts render.py 531, view.py 1204, terminal.py 160, sanitize.py 48, commands.py 500, export.py 274, collector.py 361, questions.py 142, keys.py 235 all match `wc -l`; `color_system=None if policy.no_color else "standard"` is at terminal.py:121; `console.export_text()` at commands.py:242; the per-line `Text(..., no_wrap=True, overflow="crop")` in `render()` is near render.py:524-529. The prompts mark these as approximate and tell the agent to re-verify. |

Confidence: Verified 7/7 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%
Tool engagement: Read: 9 | Grep: 2 | Glob: 0 | Bash: 4

## Summary

- Blocking findings: 1 (B-1, five items)
- Notes: 7 (N-1 to N-7)
- Items with no defect in this lens: the other 77 of 82

VERDICT: FAIL (one blocking finding: B-1)

