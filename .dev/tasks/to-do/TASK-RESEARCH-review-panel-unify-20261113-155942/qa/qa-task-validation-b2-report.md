# QA Report — Task Integrity (Lens: B2 Self-Containment)

**Topic:** Review Panel unification research task (E1 reflect Tier 2 / E2 tasklist study / E3 #346 loop)
**Date:** 2026-11-13
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report only)
**Task file:** /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/TASK-RESEARCH-review-panel-unify-20261113-155942.md
**Template:** /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.claude/templates/workflow/02_mdtm_template_complex_task.md

---

## Method

- Counted checklist items with `grep -nE '^\s*- \[[ x]\]'`: 104 items (task-file lines 163-460).
- Ran a per-line marker scan over every item: `ensuring` clause, the completion-gate sentence `cannot be marked as done`, a named Task Log findings section, full task-folder output paths, and back-reference phrases (`see above`, `see SKILL`, `previous item`, `same as item`, `continue from`). Result: every item has the completion gate and a named findings section; no item says "see above" or "see SKILL.md"; three items say "previous item" (242, 334, 394); seven items have no literal `ensuring` (246, 396, 410, 416, 436, 450, 458).
- Ran a per-line scan of the 12 Phase 2 items and 4 Phase 4 items for the embedded protocols: all 12 Phase 2 items carry the Incremental File Writing Protocol, Research Protocol, Documentation Staleness Protocol, "FIRST read" scope-slice instruction, numbered questions and their own output path; all 4 Phase 4 items carry the Incremental File Writing Protocol, Research Protocol and output path.
- Read every item in full (Phases 1-7), the B2 rules in the template (lines 147-213), the template's partitioning rule (line 1098), and BUILD-REQUEST.md (staleness warnings lines 22-32, granularity rule lines 88-94).
- B2 check 7 (no item built on [CODE-CONTRADICTED] / [UNVERIFIED] claims): grepped for `GT3`, `4 verdict flips`, `audits B`, `6-dimension`, `panel.py:` and `telemetry.py:` line refs. Every hit is inside a "do not build on" exclusion list or a question that frames the contradiction (item 190 Q3). Phase 2 agent 4 (line 188) uses the corrected `select_env :485-494` and `resolve_slot :500-556`; agent 3 (line 186) uses the corrected `telemetry.py:22`; agent 2 (line 184) frames D2 as the docstring at `:112` contradicting the clearing loop `:254-258`. PASS.
- Confirmed the research-notes sections the prompts cite exist: `EXISTING_FILES` (:30), `SOLUTION_RESEARCH` (:83), `SUGGESTED_PHASES` (:112), `AMBIGUITIES_FOR_USER` (:160).

## Phase-by-phase notes

- Phase 1 (163, 167): PASS. Context, action, outputs (frontmatter, Execution Log lines), verification, failure log and completion gate present.
- Phase 2 (182-204): PASS. Each of the 12 items embeds the full codebase research prompt verbatim with file line ranges and numbered questions; no reference to SKILL.md for the prompt.
- Phase 2 (208): PASS with note. "re-run only the matching Step 2.1 item (its embedded prompt is unchanged)" points at another item, but that item is in the same durable file and identified by its output filename, so it survives a session rollover.
- Phase 3 (216-234): PASS. Ten fully embedded prompts with partition, output path, lens checklist, severity and verdict rules.
- Phase 3 (238-252): PASS with minor notes (see Issues M-2, M-3, M-4).
- Phase 4 (260-270): PASS.
- Phase 5 (278-338): PASS with minor notes. The Step 5.2 ENTRY TEMPLATE (290) embeds a complete proposal prompt and the full `sc:adversarial` invocation, so each generated sub-checklist entry is self-contained.
- Phase 6 (346-348): PASS for the items themselves; item 348 introduces a conditional rule the downstream lens items do not restate (Issue B-1).
- Phase 6 (354-382): FAIL on B-1 (13 lens items).
- Phase 6 (386-440): PASS with minor notes (M-5, M-6, M-7, M-9).
- Phase 7 (446-460): PASS.

## Issues Found

| # | Severity | Location (task-file line) | Issue | Required Fix |
|---|----------|---------------------------|-------|--------------|
| B-1 | IMPORTANT (blocking) | 348 sets the rule; 354, 356, 358, 360, 362, 366, 368, 370, 372, 374, 378, 380, 382 must obey it | Item 348 says: if the report exceeds 3000 lines, record in Phase Gate Findings that "every Step 6.2-6.4 lens item must be run as two instances (instance a: Sections 1-5, instance b: Sections 6-10, outputs suffixed `-a` and `-b`) ... and run them that way". None of the 13 lens items mentions this condition, a section range, or the `-a`/`-b` output paths; their embedded prompts hard-code one whole-report instance and one output path. The phase note at line 352 does not mention it either. Only the consolidation item (386) knows `-a`/`-b` files may exist. After a session rollover between 348 and the lens items, an executor following each lens item as written spawns one unpartitioned agent, so the task's own partitioning rule (template line 1098) is silently skipped. This is the B1/B2 rollover failure the template exists to prevent: a later item depends on a prior item's outcome without restating it. The report is expected to exceed 1500 lines (item 362), so crossing 3000 is plausible. | Add one clause to each of the 13 lens items, for example: "If the ### Phase Gate Findings section records the Step 6.1 >3000-line partition rule, run this item as two instances with the same prompt plus `Assigned sections: 1-5` / `Assigned sections: 6-10` and output paths `qa/qa-lens-<lens>-a.md` / `-b.md`; the item is complete when both exist." |
| M-1 | MINOR | 218, 278, 280, 284, 298, 302, 312, 372 | The "do not build on known-contradicted claims" list names "the hand-off line numbers for D7/D11/D12" without the corrected values; only line 131 (Key Constraints, not an item) and item 216 give `telemetry.py:22`, `panel.py:536-543`, `panel.py:485-494`. An agent cannot tell which numbers are the stale ones. | Append the corrected values in each list, as item 216 does. |
| M-2 | MINOR | 240 | The Phase 3 fix agent commissions research agents "using the same Codebase Research Agent prompt as Phase 2" plus a parenthetical list of its parts. The fix agent's prompt does not carry the task-file path, so it cannot read the Phase 2 text; it must rebuild the prompt from the parenthetical. Every required element is named, so the item still runs. | Either give the task-file path and the Phase 2 item lines to copy, or embed the protocol text in the fix-agent prompt. |
| M-3 | MINOR | 242, 244, 334, 336 | "If no fix agent ran in the previous item / in this cycle" does not name the durable observable (the Execution Log line `Phase N consolidated: no blocking findings; no fix agent spawned`, or the existence of the current `## Cycle N` section in `qa/qa-fix-log-phaseN.md`). Executable by reading the Execution Log. Items 392/394 have the same shape with "Step 6.5 this cycle". | Name the Execution Log line or fix-log section the executor checks. |
| M-4 | MINOR | 246 | "re-executing the five Step 3.2 items above in order ... and then this item again": only four Step 3.2 items precede it (238, 240, 242, 244). The Phase 5 equivalent (338) correctly says "four". | Change "five" to "four". |
| M-5 | MINOR | 396, 416, 436 | The gate deciders name the cycle-1 verification filenames (`qa/qa-fix-verification.md`, `qa/qa-fidelity-verification-structural.md`, `qa/qa-anti-omission-verification-content.md`, etc.), while the verification items (392, 394, 414, 434) write `-cycle2` files on cycle 2. "the current cycle of" can be read as applying to all listed files, but a literal reading on cycle 2 would decide from the stale cycle-1 verdicts and could HALT on the hard cap after a passing cycle 2. | Add "(on cycle 2, the `-cycle2` files)" after each verification filename. |
| M-6 | MINOR | 414, 434 | Each item spawns TWO verification agents (rf-qa and rf-qa-qualitative) with one ROLE-templated prompt. BUILD-REQUEST lines 88-94 require one item per agent and validation step, and Phases 3, 5 and 6.6 split the two verifiers into separate items. The ensuring clause requires both reports, so tracking still works. | Split each into two items, matching 242/244 and 392/394. |
| M-7 | MINOR | 402, 404, 406, 408 | Fidelity prompts give `Research directory: <task dir>research/` (a placeholder) right after the full task-directory path, and item 408 lists `src/superclaude/skills/sc-auggie-review-protocol/` and `tests/review/` as "(files cited)". Resolvable, but not literal paths. | Spell out the research path; keep "(files cited)" only where the report defines the set. |
| M-8 | MINOR | 286 | The synth-07 prompt numbers its rules 1, 2, 3, 5, 6, 9, 11 (gaps). Cosmetic. | Renumber or note that the numbers mirror the shared rule list. |
| M-9 | MINOR | 396, 416, 436 | No `ensuring` / `ensure` verification clause (item 246, the Phase 3 equivalent, has "Ensure every decision is backed by the report text"). The decision rules are measurable, so verification is implicit. | Add the same "ensuring every decision is backed by the report text" clause. |

No issue found for B2 checks 3 (agent prompts embedded), 4 (specific paths, apart from M-7) or 7 (contradicted claims).

## Items Reviewed

Item id = task-file line number of the `- [ ]` line.

| Item | Step / purpose | Result | Note |
|------|----------------|--------|------|
| 163 | 1.1 status update | PASS | |
| 167 | 1.2 workspace + `git fetch` + E2 readable | PASS | |
| 182 | 2.1 agent 1 finding contract | PASS | full prompt, output `research/01-finding-contract.md` |
| 184 | 2.1 agent 2 ledger/merge/verdict | PASS | D2 framed as contradiction (:112 vs :254-258) |
| 186 | 2.1 agent 3 clustering | PASS | corrected `telemetry.py:22` |
| 188 | 2.1 agent 4 panel/identity | PASS | corrected `select_env :485-494`, `resolve_slot :500-556` |
| 190 | 2.1 agent 5 blocking/calibration | PASS | 6- vs 5-dimension framed as a question |
| 192 | 2.1 agent 6 input contract | PASS | |
| 194 | 2.1 agent 7 reflect merge contract | PASS | |
| 196 | 2.1 agent 8 run recording/telemetry | PASS | |
| 198 | 2.1 agent 9 consumer plug points | PASS | |
| 200 | 2.1 agent 10 future consumers | PASS | |
| 202 | 2.1 agent 11 evaluation evidence | PASS | |
| 204 | 2.1 agent 12 test pins | PASS | |
| 208 | 2.2 confirm outputs | PASS | note: re-run refers to Step 2.1 item in the same file |
| 216 | 3.1 analyst completeness p1 | PASS | |
| 218 | 3.1 analyst completeness p2 | PASS | M-1 |
| 220 | 3.1 analyst cross-validation p1 | PASS | |
| 222 | 3.1 analyst cross-validation p2 | PASS | |
| 224 | 3.1 rf-qa evidence p1 | PASS | |
| 226 | 3.1 rf-qa evidence p2 | PASS | |
| 228 | 3.1 rf-qa gaps p1 | PASS | |
| 230 | 3.1 rf-qa gaps p2 | PASS | |
| 232 | 3.1 qualitative depth p1 | PASS | |
| 234 | 3.1 qualitative depth p2 | PASS | |
| 238 | 3.2 consolidate | PASS | |
| 240 | 3.2 fix agent | PASS | M-2 |
| 242 | 3.2 structural verifier | PASS | M-3 |
| 244 | 3.2 qualitative verifier | PASS | M-3 |
| 246 | 3.2 cycle decider | PASS | M-4 |
| 250 | 3.3 gaps file | PASS | |
| 252 | 3.3 confirm gate | PASS | |
| 260 | 4.1 web W1 | PASS | |
| 262 | 4.1 web W2 | PASS | |
| 264 | 4.1 web W3 | PASS | |
| 266 | 4.1 web W4 | PASS | |
| 270 | 4.2 confirm web outputs | PASS | |
| 278 | 5.1 synth-01 | PASS | M-1 |
| 280 | 5.1 synth-02 | PASS | M-1 |
| 282 | 5.1 synth-03 | PASS | |
| 284 | 5.1 synth-04 | PASS | M-1 |
| 286 | 5.1 synth-07 | PASS | M-8 |
| 290 | 5.2 enumerate undecided + sub-checklist | PASS | ENTRY TEMPLATE is self-contained |
| 292 | 5.2 process sub-checklist | PASS | |
| 294 | 5.2 verify adversarial step | PASS | |
| 298 | 5.3 synth-05 | PASS | M-1 |
| 302 | 5.4 synth-06 | PASS | M-1 |
| 308 | 5.5 analyst accuracy p1 | PASS | |
| 310 | 5.5 analyst accuracy p2 | PASS | |
| 312 | 5.5 analyst tracing p1 | PASS | M-1 |
| 314 | 5.5 analyst tracing p2 | PASS | |
| 316 | 5.5 rf-qa structure p1 | PASS | |
| 318 | 5.5 rf-qa structure p2 | PASS | |
| 320 | 5.5 rf-qa content p1 | PASS | |
| 322 | 5.5 rf-qa content p2 | PASS | |
| 324 | 5.5 qualitative coherence p1 | PASS | |
| 326 | 5.5 qualitative coherence p2 | PASS | |
| 330 | 5.6 consolidate | PASS | |
| 332 | 5.6 fix agent | PASS | |
| 334 | 5.6 structural verifier | PASS | M-3 |
| 336 | 5.6 qualitative verifier | PASS | M-3 |
| 338 | 5.6 cycle decider | PASS | |
| 346 | 6.1 rf-assembler | PASS | |
| 348 | 6.1 measure report | PASS | defines the conditional rule B-1 depends on |
| 354 | 6.2 template-conformance lens | FAIL | B-1 |
| 356 | 6.2 internal-consistency lens | FAIL | B-1 |
| 358 | 6.2 evidence-quality lens | FAIL | B-1 |
| 360 | 6.2 completeness lens | FAIL | B-1 |
| 362 | 6.2 required-content lens | FAIL | B-1 |
| 366 | 6.3 actionability lens | FAIL | B-1 |
| 368 | 6.3 numbers-metrics lens | FAIL | B-1 |
| 370 | 6.3 crossref-chain lens | FAIL | B-1 |
| 372 | 6.3 domain-accuracy lens | FAIL | B-1; M-1 |
| 374 | 6.3 scope-discipline lens | FAIL | B-1 |
| 378 | 6.4 recommendation-feasibility lens | FAIL | B-1 |
| 380 | 6.4 finding-reproducibility lens | FAIL | B-1 |
| 382 | 6.4 implementation-concreteness lens | FAIL | B-1 |
| 386 | 6.5 consolidate | PASS | |
| 388 | 6.5 fix agent | PASS | |
| 392 | 6.6 structural verifier | PASS | M-3 |
| 394 | 6.6 qualitative verifier | PASS | M-3 |
| 396 | 6.6 cycle decider | PASS | M-5, M-9 |
| 402 | 6.7 fidelity 1 | PASS | M-7 |
| 404 | 6.7 fidelity 2 | PASS | M-7 |
| 406 | 6.7 fidelity 3 | PASS | M-7 |
| 408 | 6.7 fidelity 4 | PASS | M-7 |
| 410 | 6.7 consolidate | PASS | |
| 412 | 6.7 fix agent | PASS | |
| 414 | 6.7 two verifiers | PASS | M-6 |
| 416 | 6.7 cycle decider | PASS | M-5, M-9 |
| 422 | 6.7b anti-omission 1 | PASS | |
| 424 | 6.7b anti-omission 2 | PASS | |
| 426 | 6.7b anti-omission 3 | PASS | |
| 428 | 6.7b anti-omission 4 | PASS | |
| 430 | 6.7b consolidate | PASS | |
| 432 | 6.7b fix agent | PASS | |
| 434 | 6.7b two verifiers | PASS | M-6 |
| 436 | 6.7b cycle decider | PASS | M-5, M-9 |
| 440 | 6.8 final validation checklist | PASS | |
| 446 | 7.1 confirm final state | PASS | |
| 450 | 7.2 present to user | PASS | |
| 454 | 7.3 stage task folder | PASS | |
| 458 | 7.4 task summary + next step | PASS | |
| 460 | 7.4 frontmatter Done | PASS | |

Totals: 104 items; 91 PASS; 13 FAIL (all on B-1).

## B2 Self-Containment Checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 5 B2 components per item | PASS | marker scan: every item has the completion gate and a named findings section; context, action and output present on read-through; verification implicit in three deciders (M-9) |
| 2 | No unrestated reference to a prior item | FAIL | B-1 (13 lens items depend on item 348's conditional); minor M-3, M-5 |
| 3 | Agent prompts fully embedded | PASS | 12 Phase 2 + 4 Phase 4 prompts carry their protocols (scan); all QA/fix/verifier prompts are quoted in full; M-2 is a nested prompt summary |
| 4 | Specific file paths | PASS | full task-folder paths throughout; M-7 minor |
| 5 | Measurable verification | PASS | ensuring clauses name files, Status lines, sections, row counts, binary verdicts |
| 6 | No batch items | PASS | one item per agent everywhere except 414/434 (two verifiers each, M-6, minor) |
| 7 | Not built on [CODE-CONTRADICTED]/[UNVERIFIED] | PASS | grep: all hits are exclusion lists; corrected line numbers used in 184, 186, 188 |

## Summary

- Checks passed: 6 / 7
- Checks failed: 1 (check 2)
- Blocking issues: 1 (B-1, IMPORTANT)
- Minor notes: 9 (M-1 to M-9)
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 1 | Glob: 0 | Bash: 5 (Grep+Glob+Read total 10 is above the 7 checklist items)

## Recommendations

- Fix B-1 by adding the partition clause to the 13 lens items (354-382); this is one sentence per item.
- Optional: apply M-4 and M-5 in the same edit pass; they are one-word / one-phrase changes that remove a possible false HALT on cycle 2.

VERDICT: FAIL

## QA Complete

