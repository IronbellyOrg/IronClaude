# QA Report: task-qualitative (lens: qa-gate-sufficiency)

**Topic:** QA gate sufficiency across all 14 phases of TASK-RF-sweep-phase1-20261108-072653
**Date:** 2026-11-08
**Phase:** task-qualitative
**Fix cycle:** N/A
**fix_authorization:** false (report only; the task file was not edited)

---

## Overall Verdict: FAIL

Blocking findings: QS-01 (CRITICAL), QS-02 (IMPORTANT). Eight MINOR notes do not fail the gate.

## Drift baseline (BUILD_REQUEST.GOAL, captured verbatim from BUILD-REQUEST.md:9)

"Build the MDTM task file for issue #339 Phase 1 (orchestrator mode). The task, when run by `/task`, first closes five required design items on `docs/designs/orchestrator-mode.md`, then implements, exactly as that design specifies: ..." QA_INTENSITY full, QA_GATE_REQUIREMENTS PER_PHASE, and "Size the gates by output size" (BUILD-REQUEST.md:28-35). AX-1 is active.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Every phase that produces output has a gate (PER_PHASE) | none | PASS | 14 gate folders created in item 1.2 (task:217). Phases 2 to 14 each end with a gate-decision item (r3-b1 2.25, r3-b2 3.23, r3-b3 4.24, r4 5.30, r5 6.22, decisions 7.37, impl-core 8.29, impl-cli 9.21, tests 10.24, cmd-skill 11.21, contract 12.21, docs 13.25, final 14.28, fidelity 14.41). Phase 1 (setup) has no gate; see QS-06 (MINOR). |
| 2 | Agent floors, scaled by output size per I19 | AX-4 | FAIL | Design gates: 4+4+1 domain against the 500-1500 row for the 1013-line DESIGN (task:292), meets floor. Code gates impl-core, impl-cli, tests, cmd-skill, contract, docs: at least 6 without domain lenses (M2 template:1056), meet floor. Decisions: 3+3+2, meets. Fidelity: 3 source agents + 1 contradiction agent, meets I21 3-4. Final gate: sized at the 500-1500 row using the DESIGN size (task:2501), but the gate's subject is the whole change set; see QS-01. |
| 3 | Each agent has a specific, distinct lens, a fully embedded prompt and adversarial framing | none | PASS | 112 report-only spawns carry the preamble verbatim (grep count 112). Every lens prompt names concrete targets (for example task:342 Python 3.10 `fromisoformat` and `Z`; task:1523 argv allowlist; task:1862 "name a one-line code change that would still pass"). Notes QS-03 (no N-count framing) and QS-07 (docs gate lens overlap) are MINOR. |
| 4 | M3 sequence: parallel report-only lenses, consolidation, ONE fix agent, verification, at most 2 cycles, escalation at cap | none | PASS | Per gate: parallel spawn rule (task:191, e.g. task:293), consolidation with dedup (task:356), one fix agent per cycle (28 fix items = 14 gates x 2, grep), 2 verifiers per cycle (task:368-380), regression then monotonicity then hard cap (task:384, task:412); `HALT after 2 fix cycles` present 14 times and escalates open findings to the user. Notes QS-04, QS-05 are MINOR. |
| 5 | Fidelity gate present per I21, reads sources and outputs, at least 2 agents | AX-4 | FAIL | Present (14.29 to 14.41), after the final M3 gate, 4 agents, each reading DESIGN, SPEC, the final inventory and the files it lists (task:2634). But the fidelity fix agent may edit `docs/`, which contains the DESIGN source, with no rule against it (task:2670); see QS-02. |
| 6 | Each gate records its PASS set and F-count for the monotonicity and regression halts | none | PASS | `cycle-0 PASS set = every check id` 14 times; cycle ledger header `| Cycle | PASS set | F set | |F| | Outcome |` (task:356); `F_1`, `F_2` and PASS sets built in the decision items (task:384, task:412); verifiers must list every prior PASS id (task:372). |
| 7 | Minor-never-fails rule stated in each gate | none | PASS | In every report-only preamble (112), every fix preamble (28) and every gate-decision item (`MINOR findings never fail the gate.` 14 times). Note QS-09 is MINOR. |

## Summary

- Checks passed: 5 / 7
- Checks failed: 2
- Critical issues: 1
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Axis | Location | Issue | Required Fix |
|---|----------|------|----------|-------|-------------|
| QS-01 | CRITICAL | AX-4 | Final gate items 14.10 to 14.19, Sizing line (task:2501 and repeats) | The final gate is sized at the I19 500-1500 row ("4 rf-qa + 4 rf-qa-qualitative = 8, plus 2 domain lenses") because DESIGN is 1013 lines. I19 sizes by the output under review (template:708-715). The final gate reviews every path in `final-inventory.md` (task:2495-2497): the revised DESIGN itself (over 1013 lines) plus six new sweep modules, the tests, the command, the skill and the contract and doc edits. That is over 1500 lines even with very little code (the sibling `issue_watch` package is about 5000 lines). The 1500-3000 row needs 5 + 5 = 10 BEFORE domain lenses; the gate has 4 standard structural, 4 content and 2 domain lenses, so the content column (4) is below its floor of 5 and the standard total (8) is below 10. If the inventory is over 3000 lines the floor is 6 + 6 = 12. The inherited PASS compared against 3+3, not the size row. | Add a measuring step to item 14.9 (`wc -l` over the inventory files plus diff line counts) and size the final gate from that number. At the 1500-3000 row add one rf-qa structural lens (for example evidence-quality or completeness) and one rf-qa-qualitative content lens (for example actionability or numbers-metrics), keeping the 2 domain lenses on top (12 total), and update 14.20 to "twelve reports". Add two more of each if the count is over 3000. Correct the Sizing sentence. |
| QS-02 | IMPORTANT | AX-4 | Fidelity fix items 14.34 and 14.38 (task:2670, task:2698); final fix items 14.21 and 14.25 (task:2579, task:2607) | The fidelity gate checks the delivery against DESIGN and SPEC, but its fix agent may edit all of `docs/`, which includes the DESIGN source `docs/designs/orchestrator-mode.md`. Only SPEC is protected. A "requirement with no delivery" finding can be closed by deleting or rewording the requirement in DESIGN, and the verifiers would mark it RESOLVED. The decisions gate shows the right pattern ("may never change a decision's `Chosen:` line", task:1356), and the design-fix gates fence the fix agent to DESIGN only; the final and fidelity gates have no such fence. The same hole lets the final design-conformance lens be satisfied by editing DESIGN. | In 14.21, 14.25, 14.34 and 14.38 add: "The fix agent fixes the delivery, never DESIGN `docs/designs/orchestrator-mode.md`. A finding that can only be closed by changing DESIGN is left OPEN with that reason (it needs a design revision or owner decision)." Optionally add a verifier check that `git diff` of DESIGN is unchanged since the end of Phase 6. |
| QS-03 | MINOR | AX-4 | Report-only preamble (task:188, 112 copies) | I19 (template:733) asks every lens prompt for "Assume this document has at least N errors focused on your lens" with N by size (10 for 500-1500). The preamble says "Assume the work is wrong until you prove it right", which is adversarial, but there are 0 N-count framings in the file. | Add the N-count sentence to the preamble. |
| QS-04 | MINOR | AX-3 | Agent-failure clauses ("fails twice, log the blocker ... and stop", 181 hits) | These stops do not apply the shared HALT rule (task:192), so the task can stop with status still "Doing" and no `blocker_reason`. | Change "and stop" to "and apply the HALT rule". |
| QS-05 | MINOR | AX-3 | Regression and monotonicity branches (a) and (b) in every cycle-1 decision and gate-decision item (e.g. task:384, task:412) | Only the hard-cap branch (d) says to escalate the open BLOCKING and MAJOR findings to the user. Branches (a) and (b) halt with a one-line reason only. | Add "and list the open findings in `blocker_reason`" to (a) and (b). |
| QS-06 | MINOR | AX-3 | Phase 1, item 1.4 anchor inventory (task:229-234) | PER_PHASE: Phase 1 writes the load-bearing anchor inventory, which code items use when a status is MOVED, but no gate reviews it. It has a self-check (18 rows, quoted text), and the r4 and code gates re-check anchors. | Accept as a note, or add the inventory to the r4 gate inputs. |
| QS-07 | MINOR | AX-4 | Docs gate lenses 13.9 to 13.16 | Five of the eight lenses (primitive-path, command and skill contract, contract-rule, read-only-claims, conventions) repeat lenses from the cmd-skill and contract gates (11.6, 11.7, 11.9, 11.11, 11.12, 12.6, 12.11). They also cover the Phase 13 files, and `.gitignore` is checked (item 13.7), so coverage holds, but fewer lenses are new. | Optionally swap one repeated lens for a CHANGELOG and user-guide accuracy lens. |
| QS-08 | MINOR | AX-4 | Fidelity agent 14.32 | M4 Step 3 (template:1117) asks for an rf-qa contradiction agent that reads sources only; 14.32 is rf-qa-qualitative and also reads the delivery. verify-1 already accepted this M4 note. | None required. |
| QS-09 | MINOR | AX-2 | Gate-decision items, last sentence (e.g. task:412) | "Copy every MINOR finding to `### Phase N Findings`" comes after the cycle-2 branches, so on the early PASS path (SKIPPED or PASS at cycle 1) it is unclear whether MINOR notes get copied. | Move the sentence before the first branch. |
| QS-10 | MINOR | AX-4 | impl-core and tests gate Sizing (task:1508, task:1833) | The domain lens is counted toward the code-gate floor of 6; without it the gates still have 6, so the floor holds. Neither gate measures its output size; if I19 size scaling were applied to code gates, a large `classify.py` plus `probes.py` could exceed 1500 lines. | Note only; M2 sets 6 for code gates. |

## Actions Taken

None. fix_authorization is false; the task file was not edited.

## Confidence

- Confidence: Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 10 | Grep: 11 | Glob: 0 | Bash: 3
- Web research: none performed (no Tavily or fallback calls).

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for V-02 (impl-cli has 5 rf-qa + 3 rf-qa-qualitative, 9.12 present, 9.13 expects 8).
- Relied on rf-qa PASS for the gate title tallies of all 14 gates.
- Relied on rf-qa PASS for phase order and the END PHASE markers.
- Relied on rf-qa PASS for the POST reflect runner prompt being identical to SKILL.md:2223-2231.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Final gate floor row: the inherited count (6+4) was measured against a 3+3 floor. I read the final gate Sizing text (task:2501), the inventory scope (task:2495-2497), I19 (template:708-717) and research/09 Gap 5 (research/09:182, :193), and measured DESIGN (1013 lines) and a sibling CLI package (`wc -l`, about 5000 lines). The gated output is over 1500 lines, so the count is below the size-row floor (QS-01).
- Fidelity fix scope: grep of every "The fix agent edits only" clause (task:363 to 2698) and a grep for any DESIGN-edit ban (one hit only, task:996, in the R5 branch). The fidelity and final fix agents may edit DESIGN (QS-02).
- Lens distinctness: I extracted all lens prompts (grep -o) and compared the docs gate lenses with the cmd-skill and contract gate lenses (QS-07), and confirmed `.gitignore` coverage in item 13.7.
- Escalation and halt wiring: grep counts for the hard-cap line (14), monotonicity halt (14), regression halt, PASS set (14), MINOR rule (14) and fix agents (28), plus a full read of the r3-b1 and final gate sequences (task:291-415, task:2563-2672).
- R5 gate lenses assume option (b): checked that branch (a) halts and re-runs /task-builder before the gate (task:996), so the (b)-only lenses are correct.

VERDICT: FAIL
