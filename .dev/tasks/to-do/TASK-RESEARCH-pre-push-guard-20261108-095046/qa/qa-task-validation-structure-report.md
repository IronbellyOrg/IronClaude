# QA Report — Task Integrity (Lens: phase-structure)

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false (report only; task file not edited)
**Task file:** `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/TASK-RESEARCH-pre-push-guard-20261108-095046.md` (408 lines)
**Template:** `~/.claude/templates/workflow/02_mdtm_template_complex_task.md`

---

## Overall Verdict: FAIL (6 IMPORTANT, 8 MINOR)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete and well-formed | PASS (note) | Lines 1-60 parse as one YAML block; every template 02 key (template lines 1-61) is present with `created_date`, `template_schema_doc`, `reflect_pre`, `reflect_post`, `task_type`. The rf-qa generic names `created`, `template`, `tracks` are absent, but template 02 does not define them (issue 8). |
| 2 | Mandatory template sections present | PASS | Task Overview (64), Key Objectives (70), Prerequisites (81, 83, 88), Execution Context with References/Source Areas/Key Constraints/Handoff/Frontmatter Protocol (97-140), Detailed Task Instructions (142), Phase 1 (146), Task-Specific Context Files (156), Post-Completion Actions (308), Task Log with Summary, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up, Deviations (316-406). The Testing phase is correctly left out (documentation only, recorded by item 311). |
| 3 | Phase dependencies logical | FAIL | Phases 2 to 6 follow the skill order and each states its entry condition (205, 215, 242). Phase 7 and Post-Completion have ordering defects: Done comes before the post-completion checks (issue 1), the user summary comes before the reflect gate (issue 2), and the report is edited after Gate 3 with no lens re-check (issue 3). |
| 4 | Phase ordering (research, synthesis, assembly; QA after the work) | FAIL | Research (2), Gate 1 (3), web (4), synthesis plus Gate 2 (5), assembly plus Gates 3-5 (6) are in order. But the Gate 4/5 fixes (275, 285), the 6.9 fix pass (289) and the 7.2 `--remediate` (297) all change the report after Gate 3 checked it (issue 3). Web research output never passes a research gate (issue 9). |
| 5 | Task completion items in final phase (anti-orphaning) | FAIL | Step 7.4 (303) sets `🟢 Done`, then 5 Post-Completion items (310-314) run after it, and 312 and 314 can set `🔴 Blocked`. Template 02 lines 1443-1445 put Task Summary and Done as the LAST Post-Completion items (issue 1). |
| 6 | Task Log section at bottom | PASS | `## Task Log / Notes` at 316 through 408 is the last section, with the Phase Gate table at 378-384. |
| 7 | Estimated item count reasonable | PASS (note) | 60 `- [ ]` items: Phase 1 = 2, Phase 2 = 4, Phase 3 = 8, Phase 4 = 2, Phase 5 = 9, Phase 6 = 25, Phase 7 = 5, Post-Completion = 5 (awk count). BUILD-REQUEST line 61 asks for 4 research + 2 web + 4 synth items, and all are present. Item size is very large (issue 10). |
| 8 | Open Questions and remaining gaps documented | PASS | `### Open Questions` (406) is reserved for reflect notes by comment 408; research gaps go to `gaps-and-questions.md` (202) and report S9. Staleness notes are recorded at 401-404. |
| 9 | QA gates follow M3/M4 and match BUILD-REQUEST counts | FAIL | Counts match: Gate 1 = 3 (189-191), Gate 2 = 3 (231), Gate 3 = 7 (252-258: 3 rf-qa + 4 rf-qa-qualitative, matching the table at 382), Gate 4 = 2 (269-270), Gate 5 = 2 (279-280); serialized fix; max 2 cycles (144, 199). Failures: Gate 2 agents and every verification pair are batched in single items (issue 4); the Step 6.2 header is passed by reference with an unresolved `<N>` (issue 5); the regression check cannot run because cycle history is overwritten (issue 6). |
| 10 | TB-Add-1 placeholder scan | PASS (note) | Grep `TBD|TODO|FIXME` hits 246, 252 and 289 only as instructions to check the report for those tokens, not as placeholders. No title-only items: all 60 items contain `ensuring` and `mark this item` (grep for items missing either returned 0). |
| 11 | TB-Add-3 clarification adjacency | PASS (inactive) | No numbered Open Questions exist (grep `OQ-[0-9]+` and `Open Question [0-9]+` returned 0), so no item can be blocked by one. |
| 12 | TB-Add-4 DAG / circular dependency | PASS (note) | Data flow is forward only: 2.x to 3.x, 3.4 `gaps-and-questions.md` to 4.x, 4.x to 5.x, 5.x to 6.1, 6.1 to 6.2+. The only back-edges are the bounded gate loops ("repeat Steps 3.2-3.3 by unchecking those items", 199; also 239, 266, 276, 286), capped at 2 cycles, so there is no deadlock (issue 14). |
| 13 | TB-Add-5 granularity / XL splitting | FAIL (minor) | Item lengths: 182 = 8151 chars, 231 = 6980, 297 = 6724, 179 = 5865. Items 289 and 297 each bundle several distinct actions, and no item carries a justification comment (issue 10). |
| 14 | TB-Add-6 Verify/Acceptance format consistency | PASS | 0 `Verify:` prefixes; all 60 items use the template 02 `ensuring ...` integrated-verification form (60/60), so the format is consistent. |
| 15 | TB-Add-7 Execution Context source areas reappear in items | PASS (note) | Every Source Area appears in items: launch-level-guard.sh (176,189,219,225,246,256,269), launch-job-identity.sh (173,...,269), design doc (179,246,270), orca_worktree.py (179,...,270), install_hooks.py (179,...,270), git-scm/RelNotes/man7 (209,212). The block has 0 `path:NN` references; the over-broad spot-check regex `src/|/.*:[0-9]+` matches 4 directory-path lines (issue 12). |
| 16 | TB-Add-8 per-item file:line evidence binding | FAIL (minor) | Phase 2 items cite lines (173: lines 202-207, 164-174; 179: lines 489-578, 1012-1029; spot-checked: `publish()` is at launch-job-identity.sh 164-174 and section 19 starts at design line 489). Items 189, 190, 195 and 269 name `l2_status`, `identify`, `proc`, `publish`, install_hooks.py with no file:line, and the file has 0 `evidence-absence` comments (issue 11). |

## Issues Found

Line numbers refer to the task file. Blocking = CRITICAL or IMPORTANT.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 7.3 (300), Step 7.4 (303), Post-Completion (310-314) | The status is set to `🟢 Done` and the Task Summary is written BEFORE the five Post-Completion items run. Those items check that deliverables exist (310), confirm the gates passed (312), remove the /tmp sandbox (313) and confirm no src/docs edit (314). Items 312 and 314 can then set `🔴 Blocked` on a task already marked Done, and the Task Summary never includes their results. Template 02 (lines 1443-1445) makes Task Summary and Done the last Post-Completion items. This breaks anti-orphaning. | Move items 310-314 ahead of Step 7.3 (into Phase 7 or a Post-Completion block placed before 7.3/7.4), or move Steps 7.3 and 7.4 to the end of Post-Completion Actions. Step 7.4 must also check that no Post-Completion item set Blocked. |
| 2 | IMPORTANT | Step 7.1 (294) vs Step 7.2 (297) | The summary is shown to the user and `user-summary.md` is written before the POST reflect gate runs. That gate runs with `--remediate` (it may edit the report) and can HALT with `🔴 Blocked`. So the user can get findings and gate verdicts that the reflect gate later changes or overturns. | Put Step 7.1 after Step 7.2, and after the Post-Completion safety checks, so the summary reflects the final, gated state of the report. |
| 3 | IMPORTANT | Phase 6 preamble (242), item 312, items 275, 285, 289, 297 | Line 242 and item 312 say Gates 3-5 satisfy the I17 "final-state" post-completion lens QA. But the report is changed after Gate 3 by the Gate 4 fix (275), the Gate 5 recovery fix (285), the 6.9 validation fix pass (289) and the 7.2 reflect remediation (297), and the 7-lens gate never re-checks it. The final state is never lens-checked, so the I17 record in 312 would be false. | Either add a final lens re-check (at least the template-conformance, internal-consistency and evidence-quality lenses) scoped to sections changed after Gate 3 PASS, or reword 242 and 312 so they no longer claim final-state coverage and log the deviation in `### Deviations from Process`. |
| 4 | IMPORTANT | Item 231 (Gate 2); items 198, 238, 265, 275, 285 (verification rounds) | BUILD-REQUEST line 61: "create individual checklist items for ... every QA/validation agent. No batch items." Gate 2's three agents (rf-analyst, rf-qa, rf-qa-qualitative) are spawned from ONE item, and every verification round puts 2 agents in one item. Gates 1, 3, 4 and 5 already use one item per agent (189-191, 252-258, 269-270, 279-280), so the file is also inconsistent with itself. If one agent fails, the executor cannot mark the others complete separately. | Split item 231 into three items (5.5a-c) and each verification item into one item per agent, keeping the "spawn in ONE message" instruction in the step preamble as Gates 1/3/4/5 already do. |
| 5 | IMPORTANT | Step 6.2 preamble (250), items 252-258 | Line 250 says "Each item below embeds that header ... in full", but items 252-258 actually say "passing it the Step 6.2 header with LENS_NAME ...": the prompt text sits in a non-checkbox paragraph, which breaks B2 self-containment and checklist item 5 (no "see above"). The header also contains `<N>` "from ### Phase 6 Findings", but no item writes N there, so the placeholder stays unresolved. | Inline the full header and output format into each of the 7 lens items with a concrete N (for example 5, matching the fidelity and anti-omission prompts), and delete the false "embeds ... in full" sentence. |
| 6 | IMPORTANT | Gate decision items 199, 239, 266, 276, 286; consolidation items 194, 234, 261, 273, 283; Phase Gate table 378-384 | Step (1) of the Retry Monotonicity Protocol needs the per-item PASS set of cycle n to detect a regression at cycle n+1. But every cycle rewrites `qa-consolidated-findings-<gate>.md` and the `*-fix-verification*.md` reports under the same fixed names, verification agents re-check only "the changed sections" (198), and the Phase Gate table stores only counts. The cycle-n PASS set is therefore lost, so the byte-exact regression halt cannot be evaluated. | Use cycle-suffixed filenames (for example `qa-consolidated-findings-phase3-cycle<n>.md` and `qa-research-fix-verification-cycle<n>.md`) and record the per-cycle PASS/FAIL set (finding or check IDs) in `### Phase Gate Findings`. |
| 7 | MINOR | Handoff convention (120) vs 294, 297, 310 | Line 120 says the task uses the tech-research layout "instead of a generic `phase-outputs/` tree", yet Step 7.1 writes `phase-outputs/reports/user-summary.md`, and Step 1.2 (154) never creates that folder. | List `phase-outputs/reports/` in the Handoff convention and create it in Step 1.2, or write the summary to `qa/` or the task root. |
| 8 | MINOR | Frontmatter 1-60 | rf-qa task-integrity item 1 names `created`, `template` and `tracks`; the file has `created_date` and `template_schema_doc` and no `tracks` (for example `tracks: issue-441`). The file follows template 02, so this is a naming difference, not a defect. | Optional: add `tracks: "issue-441"`. |
| 9 | MINOR | Phase 4 (204-212) | The web research files (web-01, web-02) never pass a research-completeness gate; Gate 1 runs before them and Gate 2 sees them only through synthesis. This is the order the skill prescribes, but uncited web claims reach synthesis without a check. | Optional: extend the Gate 2 accuracy prompt (231) so it explicitly verifies URL evidence in the web-01 and web-02 files. |
| 10 | MINOR | Items 182, 231, 289, 297 (TB-Add-5) | These XL items have no split and no justification comment. Item 289 runs the validation, a conditional fix-agent spawn and a re-run. Item 297 computes values, stages `.dev/tasks`, spawns the runner, writes frontmatter, verifies on disk and loops up to 2 re-spawns. | Split 289 into a validate item and a conditional fix item; add a one-line justification comment on the embedded-prompt items. |
| 11 | MINOR | Items 189, 190, 195, 269 (TB-Add-8) | They name `l2_status`, `identify`, `proc`, `publish`, `install_hooks.py` and the push-plumbing regex without file:line, and there is no `<!-- evidence-absence: ... -->` comment (0 in the file). The line numbers already exist in items 173 and 179. | Add the existing citations (for example `publish` at launch-job-identity.sh lines 164-174, `l2_status` at orca_worktree.py lines 1012-1029) or an evidence-absence comment. |
| 12 | MINOR | Execution Context 97-117 (TB-Add-7) | The consumer spot-check regex `src/|/.*:[0-9]+` matches 4 lines, but they are directory/file paths in the template-mandated Source Areas format; 0 `path:NN` citations. | None needed; recorded for traceability. |
| 13 | MINOR (unverified) | Step 7.2 (297) | The item stages `.dev/tasks` "so the task package ... is visible to the diff", then passes `--diff {BASE}..HEAD`, a commit range. Staged files that are not committed are not in a commit range, so this reason may not hold. I could not confirm how sc-reflect-protocol resolves `--diff` (its SKILL.md line 80 only says "git ref ... or path to a diff file"). | Confirm how reflect handles the index, or pass a diff file produced by `git diff --cached {BASE}`. |
| 14 | MINOR | Gate loops 199, 239, 266, 276, 286 vs line 148 | "Repeat Steps x-y by unchecking those items" is a deliberate bounded back-edge, but it conflicts with the Phase 1 rule "complete EVERY item ... IN ORDER" and makes resume after a session rollover ambiguous (which cycle a checked item belongs to). | Optional: state in the Gate rules paragraph (144) that unchecking for a fix cycle is the sanctioned exception, and record the cycle number in Phase Gate Findings before unchecking. |

## Summary

- Checks passed: 10 / 16 (several with notes)
- Checks failed: 6 (#3, #4, #5, #9 blocking; #13, #16 minor only)
- Critical issues: 0
- Important issues: 6 (issues 1-6)
- Minor issues: 8 (issues 7-14; notes, not blocking)
- Issues fixed in-place: 0 (fix_authorization: false)

## Actions Taken

None. Report only; the task file was not edited.

## Recommendations

1. Reorder Phase 7 and Post-Completion: run the post-completion checks (310-314) first, then the reflect gate (7.2), then the user summary (7.1), then Task Summary (7.3) and Done (7.4) last (issues 1, 2).
2. Add a final lens re-check after the last report edit, or remove the "final-state QA" claim at 242 and 312 (issue 3).
3. Split item 231 and the verification-pair items into one item per agent (issue 4).
4. Inline the Step 6.2 header with a concrete N into each lens item (issue 5).
5. Make gate artifacts cycle-suffixed and record per-cycle PASS sets (issue 6).

## Confidence Gate

- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. (Issue 13 is a finding marked unverified, not a checklist row.)
- **Tool engagement:** Read: 7 | Grep: 1 | Glob: 0 | Bash: 9. Read+Grep+Glob (8) is below the 16 checklist rows. Most checks were verified with batched read-only Bash grep/awk runs (item counts per phase, checkbox format, placeholder tokens, `ensuring`/`mark this item` presence, `Verify:` count, phase-outputs references, file:line patterns, source-area reappearance, the Execution Context regex, and spot-checks of the cited source lines), so the low dedicated-tool count is not padding, but it is flagged as the rule requires.
- **Scope note:** Phase-structure lens. The 60 items were inspected through targeted reads (lines 1-204 and 287-408 in full) and openings of 231, 250, 252, 258, 261, 262, 269 and 279. The embedded prompt bodies of Phase 2, 4 and 5 items were not audited line by line for content accuracy (other lenses cover that).

VERDICT: FAIL

## QA Complete
