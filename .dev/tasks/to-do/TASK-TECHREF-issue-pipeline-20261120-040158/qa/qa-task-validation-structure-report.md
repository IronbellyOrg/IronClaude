# QA Report - Task Integrity (lens: phase-structure)

**Topic:** TASK-TECHREF-issue-pipeline-20261120-040158
**Date:** 2026-11-20
**Phase:** task-integrity
**Fix cycle:** N/A (fix_authorization: false)

**Task file:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/TASK-TECHREF-issue-pipeline-20261120-040158.md (2,365 lines)
**Lens:** phase-structure and phase ordering. **fix_authorization:** false (report only; no file other than this report was written).

## Checks performed (evidence)

| # | Lens check | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Frontmatter complete and well formed; `task_type: dynamic` allowed | PASS (Notes N1, N2) | Lines 1-61 match template 02 lines 1-61 key for key (id, title, status, type, priority, created_date, updated_date, assigned_to, related_docs, tags, template_schema_doc, task_type). Template I6 (template 02 lines 543-549) allows `task_type: dynamic` for tasks that add items at run time. The task has exactly two DYNAMIC CONTENT marker pairs (lines 900-902 `gate1-gapfill-cycle1`, 985-987 `gate1-gapfill-cycle2`), so `dynamic` is correct and needed. Implication: only Steps 3.4 and 3.9 may add items, and only inside those markers. |
| 2 | Mandatory template sections present | PASS (Note N3) | Headings (grep): Task Overview 65, Key Objectives 73, Prerequisites & Dependencies 83, Execution Context 100 (References 102, Source Areas 109, Key Constraints 118, Handoff 123, Frontmatter Update Protocol 130), Detailed Task Instructions 140, Phases 1-7, Task Log / Notes 2272 with Task Summary, Execution Log, Phase 1-6 Findings, Phase Gate Findings, Follow-Up, Deviations. `## Post-Completion Actions` is absent on purpose (anti-orphaning, check 5). |
| 3 | Phase dependencies logical, no cycles | PASS | Phase order 1 to 7 is linear; each phase consumes only earlier-phase files. Producer/consumer trace of template-digest, phase-2-output-summary, gaps-and-questions, gateN-decision and gateN-verdict, qa-completion-summary, final-verification: every consumer line is later than its producer line. |
| 4 | Order research, verify, web skipped, synthesis, gate, assembly, lens QA, fidelity, completion | PASS | Phase 2 research (2.1-2.7), Phase 3 Gate 1 (3.1-3.14), Phase 4 skip (4.1), Phase 5 synthesis 5.1-5.6 then Gate 2 5.7-5.22, Phase 6 assembly 6.1, Gate 3 6.2-6.18, Gate 4 6.19-6.30, Step 6d 6.31, Phase 7 7.1-7.6. Gate 4 is guarded by gate3-verdict PASS (line 2118). |
| 5 | Anti-orphaning | PASS | Steps 7.5 (Task Summary) and 7.6 (status Done, completion_date) are in Phase 7 (lines 2264-2270); no `## Post-Completion Actions` section. Matches task-builder SKILL lines 2296 and 2361 and tech-reference SKILL line 543. Step 7.6 is conditional on all gates PASS. |
| 6 | Task Log at bottom | PASS | `## Task Log / Notes` (line 2272) is the last H2; nothing follows the Deviations block (lines 2357-2364). |
| 7 | Item count reasonable | PASS | `^- [ ]` count = 83 (matches the stated 83): P1 4, P2 7, P3 12 (plus two dynamic containers 3.5 and 3.10 with no static item), P4 1, P5 22, P6 31, P7 6. No header claims an item count, so check 18 has nothing to mismatch. |
| 8 | Open questions and gaps documented | PASS (Note N8) | No `## Open Questions` section; research-notes `AMBIGUITIES_FOR_USER` (lines 129-130) says "None for intent" and its evidence limits are carried into Section 14.3 by the synth-06 prompt (line 1323). Builder Notes line 2318 records the one builder gap. |
| 9 | Gates follow M3/M4 and BUILD-REQUEST counts | PASS (Notes N4, N5, N6) | Gate 1: 3.1 rf-analyst, 3.2 rf-qa, 3.3 rf-qa-qualitative (3 agents, one PARALLEL SPAWNING paragraph, line 746); consolidation 3.4; verification pair 3.6/3.7 and 3.11/3.12. Gate 2: 5.7-5.12 = 3 lenses x 2 partitions (assigned synth-01..03 and synth-04..06, line 1342); consolidation 5.13; ONE rf-qa fix agent with `fix_authorization: true` (5.14, 5.19); verification pair 5.15/5.16 and 5.20/5.21. Gate 3: 6.2-6.4 rf-qa, 6.5-6.7 rf-qa-qualitative, 6.8 rf-qa domain lens = 7; consolidation 6.9; fix 6.10/6.15; verification 6.11/6.12 and 6.16/6.17. Gate 4: 6.19/6.20 = 2 fidelity agents; consolidation 6.21; fix 6.22/6.27; verification 6.23/6.24 and 6.28/6.29. Every gate has a decision item (3.8, 5.17, 6.13, 6.25) and a final-verdict item (3.13, 5.22, 6.18, 6.30) applying regression check first, then monotonicity, then hard cap, with the byte-exact halt lines. A scripted audit of all 40 fenced prompt blocks shows each carries the safety block and the incremental-write protocol, and every QA block carries the adversarial stance and `fix_authorization`. Max 2 fix cycles = fix 1 + fix 2, 3 reviews. |
| 10 | TB-Add-1 placeholders, title-only items | PASS (Note N7) | All 83 items contain "ensuring", the completion-gate sentence and a blocker clause (awk audit, 0 exceptions); none is title-only. Literal `TBD|TODO|FIXME` grep hits 6 lines (1017, 1442, 1479, 1739, 1782, 2250); every hit is a grep pattern or rule text inside an agent instruction, not a placeholder. |
| 11 | TB-Add-3 blocked items reference Open Question | INACTIVE | The task defines no Open Questions, so no item is blocked by one. |
| 12 | TB-Add-4 dependency DAG | PASS | Only back-references: 3.11 uses 3.6; 3.12 uses 3.7; 5.19 uses 5.14; 5.20/5.21 use 5.15/5.16; 6.15 uses 6.10; 6.16/6.17 use 6.11/6.12; 6.22 uses 6.10; 6.23/6.24 use 6.11/6.12. The forward mentions ("Step 3.5 below", "template that Step 3.11 reuses") are insertion targets and prose, not run-order dependencies. No cycle. |
| 13 | TB-Add-5 granularity | PASS (Note N9) | One agent per item for the 6 research agents, 6 synthesis agents, every lens agent, consolidation, fix agent and verification agent. No "spawn all agents" batch item. |
| 14 | TB-Add-6 uniform verification prefix | PASS (Note N10) | No item uses a `Verify:` prefix; all 83 use the same integrated "ensuring ..." clause of template 02 B2. Uniform. No Acceptance Criteria `- ✅` entries exist. |
| 15 | TB-Add-7 Execution Context | PASS (Note N11) | Block (lines 100-139) has no `path.py:NN` (regex `[A-Za-z_./-]+\.(py|sh|md|json):[0-9]+` over lines 100-139: 0 hits; any `:[0-9]+`: 0). The bare spot-check regex `src/|/.*:[0-9]+` gives 5 hits, all directory paths under `.../src/superclaude/`, none file:line. Every Source Area reappears in an item paragraph except `tests/issue_watch/`, which reappears only inside the fenced prompt blocks that belong to the items. |
| 16 | TB-Add-8 file:line in item Context | FAIL on literal reading (Medium M1) | `evidence-absence` count = 0. 15 item paragraphs cite code surfaces with no `.ext:N`, no `lines N-M` and no evidence-absence comment: Steps 1.2, 2.2, 2.4, 2.5, 3.2, 3.6, 3.7, 3.11, 5.2, 5.3, 5.4, 6.4, 6.6, 6.8, 7.1. The agents get line ranges in their fenced prompts; the deliverable is not affected. |

## Additional checks requested

| Check | Result | Evidence |
|-------|--------|----------|
| Every phase writes only inside the task folder or the one output file | PASS | Safety block (identical in all 40 prompt blocks) limits writes to the task folder plus the output file for assembler and fix agents. Gate 3 fix prompt (6.10, lines 1993-2020) is the only report-adjacent block without the "you must not write" clause, correctly, because it edits the output file; the assembler block (6.1) likewise. Agent 05's guard run is confined to `research/05-guard-run-sandbox/` inside the task folder (line 559) with a do-not-run fallback. Step 7.1 writes only `final-verification.md`. |
| Phase 1 creates nothing it should not | PASS | Step 1.2 (line 159) creates only `phase-outputs/reports/` and the file `phase1-scope-confirmation.md`; `mkdir -p` on the output directory is conditional and the directory already exists (Builder Notes line 2309). `research/`, `synthesis/`, `qa/`, `reviews/`, `scope/` already exist on disk (ls) and are only confirmed. `phase-outputs/` does not exist yet, so the mkdir is needed. Snapshot is touched only by `find`, read-only; the fingerprint is re-taken in Step 7.1. Removed commit and path verified readable: `git cat-file -t 01e7a9e23` prints `commit`; `git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/cli.py` prints its docstring; old WORKER-CONTRACT.md line 59 holds WC-17 and line 291 "Issue pipeline duties". |
| Every gate has HALT-escalation items naming team-lead | PASS | Per-item scan for `team-lead` and `HALT`: Gate 1 3.8 and 3.13, Gate 2 5.17 and 5.22, Gate 3 6.13 and 6.18, Gate 4 6.25 and 6.30; also 6.31. Each sets status "🔴 Blocked" with `blocker_reason`, sends ONE SendMessage naming the task file path and open BLOCKING findings, and STOPs. |
| Removed-code appendix required in synthesis and assembly content items | PASS | Step 5.6 (line 1289) requires Appendix B titled exactly "Removed on 2026-11-20", old-tree lines labelled `@01e7a9e23^`, WC-17 and "Issue pipeline duties" (B.5), guard rule 1 (B.6), removed tests (B.8). Assembler Step 6.1 and Step 7.1 check `## Appendix B: Removed on 2026-11-20`. |
| One-sentence PR 686 out-of-scope statement required | PASS | Step 5.1 (lines 1021, 1049) demands exactly one sentence in synth-01 and no other mention; Steps 5.7-5.12 check it; Gate 3 prompts and consolidation (1987) grade extra mentions BLOCKING; Step 7.1 greps `PR 686|rewrite design` and requires exactly one sentence in Section 1. |
| Phase 4 source lines named in Step 4.1 exist | PASS | BUILD-REQUEST.md line 46 begins "- Phase 4 (Web Research): SKIPPED"; research-notes.md line 115 begins "Web research (Phase 4): none." |
| Output file names agree with research-notes RECOMMENDED_OUTPUTS | PASS | research/01..06 and synth-01..06 names used in the task match research-notes lines 87-100 and 108-113. |

## Verdict

VERDICT: PASS

No finding is blocking. Executing the task as written produces the planned deliverable, keeps every gate, the four HALT-to-team-lead paths and the safety rules intact. Medium and Note items below are form and robustness points; none changes a deliverable.

## Issues (severity rated)

### Blocking
None.

### Medium
- **M1 (Items 1.2, 2.2, 2.4, 2.5, 3.2, 3.6, 3.7, 3.11, 5.2, 5.3, 5.4, 6.4, 6.6, 6.8, 7.1; TB-Add-8).** These item paragraphs name code surfaces (source files, `issue_watch/`, snapshot paths) with no `file:line` and no `<!-- evidence-absence: ... -->`; the file contains zero evidence-absence comments. Literal TB-Add-8 fails. Practical effect is nil because the task produces documentation and the line ranges live in each item's fenced prompt, but a mechanical validator will fail the item. Fix if desired: add a short `<!-- evidence-absence: whole-file read; line citations are produced by the spawned agent -->` to each of the 15 items.
- **M2 (Steps 5.19-5.21, 6.15-6.17, 6.22-6.24, 6.27-6.29, 3.11, 3.12; B2 item 5).** Cycle-2 and Gate 4 fix/verification items do not embed their own prompt; they say "use the prompt of Step 5.14 / 6.10 / 6.11 / 6.12 with these substitutions". This is a "see above" form, which the rf-qa item-5 rule and B2 discourage. It is disclosed in Builder Notes line 2312 and the referenced blocks exist earlier in the same file, so the executor can reproduce them; it only breaks if a later batch loses the earlier block (the file is on disk, so it does not). The B2 lens report covers this in depth.
- **M3 (Gate 2 start, line 1342 and Step 5.7).** I15 point 1 asks for an aggregation item before the lens agents. Gate 1 has 2.7 and Gate 3 has 6.1's measurement, but Gate 2 has none; the "Glob synthesis/synth-0*.md and confirm all six exist" check lives in the PARALLEL SPAWNING paragraph, not in a checklist item, and a rollover could lose it. Same pattern for the "Gate 4 runs only after Gate 3 PASS" guard (line 2118) and for "do not start Phase 5 unless gate1-verdict is PASS". Because every HALT stops execution, the practical risk is low. Fix if desired: move the Glob check into Step 5.7/5.8 text or add one aggregation item.

### Note
- **N1 (frontmatter).** rf-qa task-integrity item 1 lists required fields `created`, `template`, `tracks`; template 02 uses `created_date` and `template_schema_doc` and has no `tracks`. The task file follows template 02 exactly, so the checklist wording, not the file, is out of step.
- **N2 (frontmatter).** task-builder SKILL line 2168 says `reflect_post_mode` is always emitted; the key is absent here. `POST_REFLECT_GATE` is not enabled in BUILD-REQUEST, so no POST reflect item is required and the validator's mode branch has nothing to enforce.
- **N3 (template deviation).** Template I13/I17 describe a `## Post-Completion Actions` section; the task folds those items into Phase 7 per the anti-orphaning rule, and Step 7.3 records why I17 items 5-6 are met by Gates 3 and 4. Builder Notes line 2315 covers it but `### Deviations from Process` (line 2357) is empty; adding a one-line entry there at execution time would be clearer.
- **N4 (Gate 1 design).** Gate 1's "fix" step is N gap-fill agents (`general-purpose`), not ONE `fix_authorization: true` agent. This follows BUILD-REQUEST line 45 and the Gate 1 header (line 744); the items run in sequence, so there is no parallel edit of the same research file. Not a violation, but it differs from the Gates 2-4 pattern named in the lens brief.
- **N5 (Gate order after fixes).** Gate 4's fix agent can edit the document after Gate 3 closed; no lens QA is re-run. Step 7.1 mechanically re-checks structure, placeholders and the single PR 686 sentence, and Step 7.3 documents the decision. Acceptable under BUILD-REQUEST Phase 6 mapping.
- **N6 (HALT target).** All HALT items depend on SendMessage to an agent named `team-lead`; there is no fallback text if the name does not resolve in the executor's session (status Blocked and the Task Log entry still record the halt). The addressable-agent list in this QA session does not show `team-lead`, so I could not verify the name resolves; BUILD-REQUEST mandates it.
- **N7 (TB-Add-1 false positives).** The six literal `TBD/TODO` hits are grep patterns in agent instructions. A mechanical Grep validator would flag them; consider writing the pattern as `T.DO|T.D` or accept.
- **N8 (gap log).** Step 3.14 calls the file an "interim gap log" and no later step finalizes it; Step 7.2 only checks that it exists. Harmless, because Section 14 of the document is the final record.
- **N9 (granularity).** Step 1.2 bundles five read-only checks plus one report file (3,000 chars); it has one deliverable, so it is acceptable, but it is the item most likely to be partly done after a rollover.
- **N10 (TB-Add-6).** The lens text asks for a `Verify:` prefix; template 02 B2 uses the "ensuring" clause, and the task is uniform in using it.
- **N11 (TB-Add-7).** `tests/issue_watch/` and the hook/claim-flow test directories (named in research-notes EXISTING_FILES) are not all in the Source Areas list (lines 109-116), which only names `tests/issue_watch/`; the hook and skill tests appear in prompts but not in the header. Not drift in the harmful direction (header is a subset).
- **N12 (parser robustness).** The GAP-FILL ITEM TEMPLATE (line 893) contains an indented `- [ ]` line inside a code fence. A fence-unaware checklist parser would count 84 items; a fence-aware one counts 83.
- **N13 (cosmetic).** Step 4.1 says "a new `### Phase 4 - Web Research Findings` section" but the heading already exists (line 2341); Step 7.5 says "Create a `### Task Summary` section" while one already exists (line 2274); Phase 7 has no findings subsection, so its blockers go to the Phase 6 section.

## Confidence and tool engagement

- **Confidence:** Verified: 23/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (16 lens checks plus 7 additional checks; N6 is a documented limitation, not an unchecked item).
- **Tool engagement:** Read: 14 | Grep: 8 (one call returned `EACCES` for `rg`; the same searches were re-run through Bash `grep`) | Glob: 0 | Bash: 17.
- Tool calls exceed the checklist item count, so the engagement minimum is met.

## QA Complete
