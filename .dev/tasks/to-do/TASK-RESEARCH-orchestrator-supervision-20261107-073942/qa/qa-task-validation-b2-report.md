# QA Report — Task Integrity (B2 self-containment lens)

**Topic:** Orchestrator mode research for issue #339 (task file TASK-RESEARCH-orchestrator-supervision-20261107-073942.md)
**Date:** 2026-11-07
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report only; task file not edited)

---

## Overall Verdict: FAIL

## Summary

- Checks passed: 2 / 7 (checks 6 and 7, with notes)
- Checks failed: 5 (checks 1, 2, 3, 4 and 5)
- Blocking issues: 10 (B1-B10, all IMPORTANT; none CRITICAL)
- Minor notes: 9 (M1-M9; these do not fail the gate)
- Issues fixed in-place: 0 (fix_authorization false)
- Passed structural observations: the frontmatter has the required fields; every item uses the `- [ ]` format; there are no nested checkboxes; all 79 items have a blocker clause and a "mark this item as complete" gate; the phase item counts add up (2 + 6 + 15 + 2 + 20 + 28 + 6 = 79); parallel spawning is stated; the TBD/TODO matches on lines 270 and 274 are instructions to search for placeholders, not placeholders.

## Progress

- Review of all 443 lines is complete. The Issues Found table lists B1-B10 (blocking) first and then the M1-M9 notes; B10 appears after the notes because of append order.

## Findings (incremental)

### Items Reviewed (B2 checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 5 B2 components (context, action, output, verification, completion gate) | FAIL | Bash grep: 79/79 items end with "Once done, mark this item as complete." and 79/79 have an "If unable to complete" clause. 74/79 have an "ensuring ..." verification clause. The 5 without one are the cycle-control items on lines 180, 260, 310, 324 and 338, which also hand off their action by reference (see B2). |
| 2 | No "see above" references | FAIL | Lines 180, 260 and 310 ("the verification item above"); 324 and 338 ("repeat the consolidate-fix-verify items"); 330-334 ("same anti-omission prompt as agent 1"); 206-226 (the literal "[the phase context above]"). |
| 3 | Agent prompts fully embedded | FAIL | Anti-omission agents 2-4 (330-334) point to agent 1's prompt. The qualitative verifiers on 178, 258 and 308 are described but not given a prompt. The Phase 5 prompts depend on the phase blockquote on line 202. |
| 4 | Specific file paths | FAIL | Line 130 cites `tests/core/test_routing_refresh.py`, which does not exist (the real file is `tests/recommend/test_routing_refresh.py`). The fix and verifier prompts on 322, 324, 336 and 338 use bare `qa/...` paths with no task directory. The Phase 5 prompts use an undefined `${TASK_DIR}` and bare `research/...` paths. |
| 5 | Measurable verification | FAIL | The 7.5 reflect gate (356) diffs `{BASE}..HEAD`, but the task never commits. 7.3(f) (350) has no git-status baseline. 3.2.5 (182) and 5.6 (226) read headings the scope files do not have. |
| 6 | No batch items | PASS (with notes) | No item covers many independent files in one action. Lines 322, 324, 336 and 338 each combine two steps (minor atomicity note). |
| 7 | No items built on [CODE-CONTRADICTED] / [UNVERIFIED] findings | PASS (with notes) | No item builds on option A4 (CODE-CONTRADICTED), and 5.4 says "Do not assume A1 wins". However, 5.5 (222) hardcodes an A1 plan (B5) and 2.6 (142) carries a wrong label (B8). |

### Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | IMPORTANT (blocking) | Step 6.7b, lines 330, 332, 334 | Anti-omission agents 2-4 say "with the same anti-omission prompt as agent 1". Their prompts are not embedded, and the parenthetical summary leaves out parts of agent 1's checklist and method. An executor spawning agent 3 alone cannot rebuild the prompt without reading line 328. | Copy agent 1's full prompt (checklist, method, severity scale, verdict rule, output path) into each of the items on 330, 332 and 334, changing only the assigned section range and output file name. |
| B2 | IMPORTANT (blocking) | Cycle-control items, lines 180, 260, 310, 324, 338 | They re-run other items by reference: "re-run the fix item and the verification item above" (180, 260); "re-run Step 6.5's fix item and the verification item above" (310); "repeat the consolidate-fix-verify items with -cycleN file names" (324, 338). The -cycleN output names for the fidelity and anti-omission cycles are never spelled out. These 5 items are also the only ones without an "ensuring ..." verification clause (Bash grep: 74/79). | In each cycle item, write out the full fix and verifier prompts (or name the exact earlier item by Step number and give its exact cycle-N input and output paths, e.g. `${TASK_DIR}qa/qa-fidelity-consolidated-cycle1.md`) and add a measurable verification clause (file exists, ends with a `VERDICT:` line, and the count of blocking findings is recorded against the monotonicity check). |
| B3 | IMPORTANT (blocking) | Phase 5 synthesis items 5.1-5.6, lines 206, 210, 214, 218, 222, 226 | Each prompt contains the literal placeholder "[the phase context above]" and uses `${TASK_DIR}`, which only the phase blockquote on line 202 defines. The prompts also mix in bare relative paths (`research/scope-02-...`) that a subagent resolves from the repo root, not the task folder. The spawned agent receives an unresolved placeholder. | Replace "[the phase context above]" with the actual context text in each prompt, and write every input and output as an absolute path (`.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/research/...`). |
| B4 | IMPORTANT (blocking) | Fix and verifier prompts, lines 178, 258, 308, 322, 324, 336, 338 | The fidelity fix prompt (322) and anti-omission fix prompt (336) use only `qa/...` and `RESEARCH-REPORT-...` relative names. The shared verifier prompts (324, 338) do not name the report path. The qualitative verifiers (178, 258, 308) are described ("re-checks the qualitative findings") rather than given a prompt, with no input paths. | Give each spawned agent a full prompt with the task directory and the absolute paths of the report, the consolidated findings file and its output file. |
| B5 | IMPORTANT (blocking) | Step 5.5, line 222 | The implementation-plan synthesis hardcodes an A1-style plan (CLI registration in `main.py`). It runs in parallel with 5.4, which is told "Do not assume A1 wins", so 5.5 cannot read synth-04 and may contradict the recommendation. 5.5 also leaves out `research/scope-02-...`, `05-orca-row-schema`, `06-orca-open-questions` and `gaps-and-questions.md`, the core Orca read evidence a read-only sweep needs. | Either order 5.5 after 5.4 and have it read `synth-04` and build the plan for the recommended option, or make it option-neutral (one plan per surviving option). Add the missing research inputs to its read list. |
| B6 | IMPORTANT (blocking) | Step 7.5 reflect gate, line 356 | It runs `--diff {BASE}..HEAD` with `BASE = git merge-base HEAD master`. The task never commits and all its outputs are untracked (`?? .dev/tasks/to-do/TASK-RESEARCH...`), so the diff holds none of the task's work. With the stale local master (merge-base 80f36180, HEAD e8db2fe6), the diff instead holds the unrelated commits #410-#420. The gate measures the wrong thing. | Point the reflect gate at the task's actual outputs (pass the task folder or the explicit file list as the target), or record a baseline before Phase 1 and diff against the working tree. Do not use `merge-base HEAD master`. |
| B7 | IMPORTANT (blocking) | Step 7.3(f), line 350 | It checks "no change outside ${TASK_DIR} made by this task", but no item records a `git status --porcelain` baseline. `.dev/brainstorms/20261107-073115-orchestrator-mode/` and `.dev/issues/339/` were already untracked before the task, so the check cannot tell task changes from earlier ones. | Add a baseline capture to item 1.2 (write `git status --porcelain` to `${TASK_DIR}baseline-git-status.txt`) and make 7.3(f) compare against that file. |
| B8 | IMPORTANT (blocking) | Step 2.3, line 130; Step 2.6, line 142 | 2.3 cites `tests/core/test_routing_refresh.py`, which does not exist (`tests/recommend/test_routing_refresh.py` does). Because the item's blocker clause treats a missing source as blocking, this item will stop on a bad path. 2.6 labels WORKER-CONTRACT.md lines 133-136 as "frozen worker", but those lines ("After an /sc:implement stop (decision D2)") describe a frozen plan, not a frozen worker. | Correct the test path to `tests/recommend/test_routing_refresh.py`. Relabel the 2.6 citation as "frozen /sc:implement plan (D2)" or cite the right lines for frozen-worker handling. |
| B9 | IMPORTANT (blocking) | Step 6.7b, lines 328 and 336 | The anti-omission verdict rule is "PASS (0 omitted)" (328), and the fix item (336) makes every unjustified omission blocking. That contradicts the task's own rule that MINOR findings never fail a gate, so the gate can fail on a cosmetic omission and use up the 2-cycle cap. | Grade omissions by the review severity rule: an omitted load-bearing finding is blocking, and an omitted wording-level detail is a MINOR note. Change the verdict rule to "PASS when 0 blocking omissions". |
| M1 | MINOR (note) | Handoff convention, line 96; Step 1.2 | The reflection output goes to `${TASK_DIR}reflect/post/`, but item 1.2 does not create that folder (the reflect skill probably creates it). | Add `reflect/post/` to the folders 1.2 creates. |
| M2 | MINOR (note) | Handoff convention, line 96 | `gaps-and-questions.md` sits at the task root, which the handoff convention does not list. | Add it to the convention. |
| M3 | MINOR (note) | Phase 7, lines 344-358 | Phase 7 items have no Step headers, yet 7.4 and 7.6 are referred to by number. | Add Step headers 7.1-7.6. |
| M4 | MINOR (note) | Lines 322, 324, 336, 338 | Each item combines consolidate+fix or verify+cycle control (atomicity). | Split each into two items. |
| M5 | MINOR (note) | Step 6.7, lines 316-320 | Fidelity agent prompts 2-4 give no severity scale and no verdict rule. | Add the same scale and verdict line as agent 1. |
| M6 | MINOR (note) | Phase 6 lens prompts, lines 274-298 | `[N]` is filled in by the executor and is defined only in the phase blockquote. | Write the cycle number placeholder rule into each prompt. |
| M7 | MINOR (note) | Step 2.x citing orca-capabilities.md lines 148-151 | The "peer sessions" label is inherited from research-notes:41. Those lines cover supervision, the preamble and caller identity, and the word "peer" does not appear in the file. | Relabel the citation as "supervision / preamble / caller identity". |
| M8 | MINOR (note) | Step 5.7 qualitative agents | They read only the synthesis files, not the research files, so they cannot spot synthesis drift from evidence. | Optionally add the research directory to their inputs. |
| M9 | MINOR (note) | Phase 6 rf-qa lens spawns | The phase names "report-lens-*" are not defined rf-qa phases; each prompt does embed its own checklist, so the run still works. | Use `report-validation` as the phase and keep the lens as a separate field. |
| B10 | IMPORTANT (blocking) | Step 3.2.5, line 182; Step 5.6, line 226; 3.1 completeness agents | 3.2.5 and 5.6 read "every `## Gaps and Questions` section", and the 3.1 completeness agents require a "Key Takeaways" section. Grep shows that none of the four scope files has either heading (they use `## Open questions`), and the Phase 2 verify items do not add them. The gates will predictably fail, or the reads will find nothing. | Match the headings the research files actually use (`## Open questions`), or have the Phase 2 items require `## Gaps and Questions` and `## Key Takeaways` and verify they exist. |


## Recommendations

- Fix B1-B10 in the task file before execution starts. B3, B4, B6 and B10 will fail at run time, not just at review time.
- Then re-run this B2 lens review (fix cycle 1 of at most 2).

## Confidence

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 3 | Glob: 0 | Bash: 7
- No web research was performed.

## QA Complete

VERDICT: FAIL
