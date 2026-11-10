# S4 ANALYSIS: BMAD first-use research report (incident I4), review-gate loops

Produced by `/sc:analyze` (invoked through the Skill tool as `sc:analyze`, flow: discover, scan, evaluate, recommend, report), 2026-11-08, by the S4 recreation analyst. Analysis and packaging only: nothing was run against the incident and nothing under `~/.claude` or in the Coder worktree was changed.

Brief given to `/sc:analyze`: "Review the past incident I4 (evidence listed in phase1/REPORT.md) and recreate the scenario as exactly as possible, with the original run as the baseline. Output a replay package that lets a fresh session re-run the scenario with the same starting document and the same instructions."

Path keys used below:
- `BM` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global/189f8649-3921-4435-bc6b-a15182a20399.jsonl` (main session log, 5,392 lines). `L<n>` = 1-based jsonl line.
- `SA` = the sibling folder `.../189f8649-3921-4435-bc6b-a15182a20399/subagents/` (71 agent logs: 65 started by the main session, 6 started by a fix agent). Agent ids per brief are in `briefs/INDEX.md`.
- `QA` = the baseline review outputs, copied unchanged into `evidence/baseline-qa-outputs/` (original: `<Coder worktree>/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/qa/`). `QA/x.md:n` = line n of that file.
- `TF` = the task file; `TF:n` = its line n, in the state saved as `inputs/task-file/...v2-at-2026-11-07T15-38-37Z`.
- Times are UTC, same clock as the logs.

## 0. Result in eight lines

1. The incident is not one review loop but five quality gates of one `tech-research` run, each allowed 2 fix cycles (3 reviews). Four of the five stopped at the cap with blocking findings still open (Gates 1, 2, 3, 5). Gate 4 passed cleanly at review 2. Phase 1 reported three halted gates and one exception; the gate decision files show four halted gates and one user exception each (section 2).
2. Blocking findings per review (consolidated): Gate 1 9, 6, 1; Gate 2 8, 3, 2; Gate 3 18, 5, 2; Gate 4 1, 0; Gate 5 4, 3, 1. Counts fall every round, but never reach zero inside the cap.
3. Every blocking finding of reviews 2 and 3 (23 of 23, Gates 1, 2, 3, 5) is caused, exposed, or left half-fixed by the previous fix cycle (section 7). That is the same shape as issue 346.
4. The reviewers are `rf-qa`, `rf-qa-qualitative` and `rf-analyst` agents started with the Claude Code `Agent` tool from the `tech-research` and `task` skills. No `/sc:spec-panel` was used anywhere in the 71 agent logs or the main log. PR 427 (95f2c6e4) changes only `/sc:spec-panel` text, the routing guide, two release guides, one design doc and one test, so it cannot change this scenario (section 5).
5. The starting documents are not stored per gate, but they are exactly reproducible: replaying every logged Write, Edit and heredoc append reproduces the Gate 3 end state byte for byte against the Claude Code file-history backup, and the final files on disk; 21 of the 33 rebuilt gate-start states also exist as staged git objects in the Coder repo, which confirms them independently (section 6, `tools/`).
6. All briefs (the main-session user brief, 65 agent wrappers, 64 embedded task-file prompts, the 2 skill calls that start the run) are recovered verbatim. Only the prompts that the Gate 1 fix agent wrote for its own 6 gap researchers are not extracted (agent-written; REPLAY.md section 7).
7. The loop does not end by a rule that a replay can reuse: each halt was ended by a user-accepted exception plus a manual edit with no fourth review. A replay must fix its own stop rule (REPLAY.md).
8. Recreation grade B. The bulk of the cost is the run itself: the five gates took 58 agent runs, 3,972 agent tool calls and 2.87 million output tokens (about 6 hours elapsed).

## 1. Scope and method

`/sc:analyze` was run on the evidence of incident I4 in `phase1/REPORT.md` (section "I4 BMAD first-use research report", lines 196-239). I did not trust its numbers: every number below was re-read from the baseline outputs or re-derived, and each says which.

Steps taken:
1. Discover: listed the run's artifacts (task folder with 80 `qa/` files, 8 research files, 4 synthesis files, the report; 71 agent logs; 8 file-history backups; Coder git objects).
2. Scan: extracted all 69 Agent/Skill calls from `BM` (script `tools/extract_briefs.py`), the census of every mutating tool call (`tools/census.py`: 1,974 rows), per-agent costs (`tools/agent_costs.py`).
3. Evaluate: read all five gate decision files, the cycle-2 consolidated files and the verification reports for origin statements; replayed edits to rebuild document states (`tools/reconstruct.py`, `tools/reverse_notes.py`) and checked them against independent copies.
4. Recommend and report: this file, `baseline-metrics.json`, `REPLAY.md`.

Cross-check with the tasklists team's report (`exp346-p1-tasklists/.../phase1/REPORT.md`): its incident I4 is a different incident (ccsession handoff document); it has no mention of BMAD, `tech-research` or `rf-qa` (searched). So there is nothing to cross-check for S4; the logs report is the only source.

## 2. What the incident is, and corrections to phase 1

The run: dispatch `ctx_cafa62af9b4a`, started 2026-11-07T13:24Z, resumed the research for issue 478 in the Coder repo (`IronbellyOrg/Coder`, branch `ironbelly/bmad-ponytail-global`). Brief: `BM` L13 (verbatim in `briefs/S-user-resume-brief_L13.md`). The skills were called at `BM` L138 (`tech-research`) and `BM` L156 (`task`, the executor); both skill texts as loaded are saved in `inputs/skills/`. The task file (`TF`) holds the whole procedure, including the long prompt of every agent.

The five gates (task file `TF:211-271` Gate 1, `TF:285-357` Gate 2, `TF:358-476` Gates 3 to 5):

| Gate | What is reviewed | Reviews | Outcome |
|---|---|---|---|
| 1 research completeness | 5 research files (`research/01..05`) | 3, FAIL x3 | HALT at cap, user exception, manual 2-line edit |
| 2 synthesis quality | 4 synthesis files | 3, FAIL x3 | HALT at cap, user exception, manual edits |
| 3 report, 7 lenses | the assembled report | 3, FAIL x3 | HALT at cap, user exception, manual edits |
| 4 source fidelity | the report | 2, FAIL then PASS | clean PASS |
| 5 anti-omission | the report | 3, FAIL x3 | HALT at cap, user exception, one manual edit |

Corrections to `phase1/REPORT.md` (the phase 1 text is not changed):
- Gates halted: phase 1 says "FAIL-HALT x3 (Gates 1-3)" and "a one-time exception for Gate 3". The decision files show Gate 5 also halted (`QA/qa-gate5-decision.md:43`) and each halted gate got its own exception: Gate 1 (`QA/qa-gate1-decision.md:44-48`, ask `msg_acc5015c9601`, `BM` L1247), Gate 2 (`QA/qa-gate2-decision.md:44-48`, `BM` L2377), Gate 3 (`QA/qa-gate3-decision.md:58-62`, `BM` L3462), Gate 5 (`QA/qa-gate5-decision.md:45-49`, ask `msg_8c3d61e635e2`, `BM` L4513). The exception in the resume brief (`BM` L13) was a different, earlier one: the Gate 4 web-source-table wording, applied at 13:25 before the run (task-file log line `TF:535`).
- Growth: phase 1 says report growth "about 1 percent". That is the line count (1,785 to 1,807). In bytes the report grew 11.8 percent (364,593 to 407,656). The Gate 1 research files grew 67.7 percent in bytes (255,114 to 427,771) because the fix agent adds addenda; phase 1 did not measure them.
- Gate 1 R2 counts: phase 1 says "6 new". Confirmed: `QA/qa-consolidated-findings-phase3-cycle2.md:1` is `BLOCKING_COUNT: 6`.
- "Report is 1,785 lines at assembly": confirmed by replay (1,785 newline characters, section 6).

## 3. Evidence map (every pointer below exists)

| Evidence | Where |
|---|---|
| Main session | `BM` (5,392 lines); user brief L13; skill calls L138, L156 |
| Agent spawns | 65 Agent calls, list with lines and agent ids in `briefs/INDEX.md` |
| Agent logs | `SA/agent-<id>.jsonl` (71) |
| Decision files | `QA/qa-gate1-decision.md` ... `QA/qa-gate5-decision.md` |
| Consolidated findings | `QA/qa-consolidated-findings-phase3.md` (+`-cycle2`), `-phase5`, `-phase6`, `qa-fidelity-consolidated-findings.md`, `qa-anti-omission-consolidated-findings.md` (+`-cycle2` each; first line `BLOCKING_COUNT: n`) |
| Document backups | `~/.claude/file-history/189f8649-3921-4435-bc6b-a15182a20399/`: `32d05845d5285d52@v1,@v2` (task file), `ae5475a180c7c83a@v1` (research 05 at 17:18), `b1f12dba87654e26@v1`, `3e4a4f8f424a5b4d@v1`, `4bee01eff428f97f@v1` (synth 04, 02, 03 at 18:56), `7c3e47725f1b55c6@v1` (a consolidated findings file at 19:22), `ca7857aee503d1e6@v1` (report at 19:56, end of Gate 3 fix 2) |
| Git | Coder repo, HEAD at run start `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1` (`BM` L23 "Recent commits: f1ac0c93 Merge pull request #476"; `BM` L868 "the exact commit of this worktree"). The run committed nothing; `86c827af` (2026-11-08T01:26Z) came after |
| Worktree on disk | `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/` (final state; staged, not committed) |

Correction to phase 1: the backup `ca7857aee503d1e6@v1` is the report at the end of Gate 3 fix cycle 2 (19:56, 387,624 bytes, 1,795 lines), not "after Gate 3 fix 1" (it equals the replayed state after fix 2, section 6). The other five backups likewise are "end of gate" states, not starts.

## 4. Round by round

Rounds: R1 = first review, F1 = single fix agent of cycle 1, R2 = verification after F1 (this is review 2), F2 = fix cycle 2, R3 = verification after F2 (review 3). Agent types come from the `Agent` calls (`subagent_type`); per-agent lines are in `briefs/INDEX.md`. "Blocking" = CRITICAL or IMPORTANT. Counts are consolidated unless marked raw. Full detail with sources per number: `baseline-metrics.json`.

### Gate 1: research completeness (documents: `research/01..05`)

| Round | UTC | Agents (wrapper line in BM) | Result | Blocking |
|---|---|---|---|---|
| R1 | 15:52-16:04 | `rf-analyst` completeness (L676), `rf-qa` evidence (L680), `rf-qa-qualitative` depth (L684); embedded prompts `TF:218`, `TF:222`, `TF:226` | all 3 FAIL: I2/m8, I5/m4, I5/m2 (`QA/qa-gate1-decision.md:13-15`) | raw 12, consolidated 9 (`QA/qa-consolidated-findings-phase3.md:1`); consolidated by the orchestrator itself (`TF:230`), no agent |
| F1 | 16:05-16:19 | `rf-qa` fix agent, `fix_authorization: true` (L841, `TF:234`); it started 6 `rf-task-researcher` gap researchers | 9 fixed of 9 (`QA/qa-gate1-decision.md:17`) | |
| R2 | 16:19-16:26 | `rf-qa` structural (L924, `TF:238`), `rf-qa-qualitative` content (L928, `TF:242`) | FAIL: structural I2/m3, content I4/m8; all 9 confirmed fixed (`:18-19`) | 6 (`QA/qa-consolidated-findings-phase3-cycle2.md:1`): F1-a, F1-b, F4-a, X-1, N1, N2 |
| F2 | 16:32-16:38 | `rf-qa` fix agent (L1075, `TF:254`) | 6 of 6 | |
| R3 | 16:38-16:47 | `rf-qa` structural (L1120, `TF:258`), `rf-qa-qualitative` content (L1124, `TF:262`) | structural PASS (I0/m3), content FAIL (I1/m7) (`:36`) | 1: New-1 (`QA/qa-gate1-decision.md:40`) |
| End | | HALT asked at `BM` L1247 (16:47:59); answer by 17:18 | `GATE1_FINAL: FAIL - HALT` then `PASS (user-accepted exception ...)` (`QA/qa-gate1-decision.md:42, 48`; first written `BM` L1173, L1476) | executor edited lines 376 and 408 of research file 05, no fourth review |

### Gate 2: synthesis quality (documents: `synthesis/synth-01..04`)

| Round | UTC | Agents | Result | Blocking |
|---|---|---|---|---|
| R1 | 18:12-18:23 | `rf-analyst` accuracy (L1899, `TF:308`), `rf-qa` structure (L1903, `TF:312`), `rf-qa-qualitative` coherence (L1907, `TF:316`) | analyst PASS I0/m8; structure FAIL I4/m11; qualitative FAIL I5/m10 (`QA/qa-gate2-decision.md:13-15`) | raw 9, consolidated 8 (31 rows; one MINOR upgraded to IMPORTANT, no downgrades) |
| C1 | 18:24-18:28 | `rf-analyst` consolidation (L1985, `TF:320`) | `QA/qa-consolidated-findings-phase5.md` | |
| F1 | 18:28-18:36 | `rf-qa` fix agent (L2018, `TF:324`) | 8 of 8 | |
| R2 | 18:36-18:40 | verification structural (L2061, `TF:328`), qualitative (L2065, `TF:332`) | structural PASS I0/m4; content FAIL I3/m2; 7 of 8 resolved, finding 6 partly | 3: N-1, N-2, N-3 (`QA/qa-consolidated-findings-phase5-cycle2.md:1`) |
| F2 | 18:41-18:45 | `rf-qa` fix agent (L2202, `TF:344`) | | |
| R3 | 18:46-18:49 | verification structural (L2244, `TF:348`), qualitative (L2248, `TF:352`) | structural PASS I0/m3; content FAIL I2/m4 (`QA/qa-gate2-decision.md:33`) | 2: V-1, V-2 |
| End | | HALT asked at `BM` L2377 (18:49:40) | `GATE2_FINAL: FAIL - HALT`, then `PASS (user-accepted exception ...)` (`:42, :48`; written `BM` L2308, L2742) | executor made the V-1/V-2 edits in synth-02/03/04, no fourth review |

### Gate 3: report validation, 7 lenses (document: `RESEARCH-REPORT-bmad-first-use.md`, assembled 18:58-19:00 by an `rf-assembler`, `BM` L2758)

| Round | UTC | Agents | Result | Blocking |
|---|---|---|---|---|
| R1 | 19:00-19:15 | 7 lenses: `rf-qa` template-conformance (L2802, `TF:371`), internal-consistency (L2806, `TF:373`), evidence-quality (L2810, `TF:375`); `rf-qa-qualitative` actionability (L2814, `TF:379`), domain-accuracy (L2818, `TF:381`), crossref-chain (L2822, `TF:383`), finding-reproducibility (L2826, `TF:387`) | all 7 FAIL; raw Important 2+4+1+8+1+9+2 = 27, minor 68 (`QA/qa-gate3-decision.md:21-27`) | consolidated 18 of 69 rows (`QA/qa-consolidated-findings-phase6.md:1`); consolidator downgraded 7 Important to Minor, orchestrator restored 2, so 5 stayed downgraded (`:5-15`) |
| C1 | 19:16-19:22 | `rf-analyst` consolidation (L2965, `TF:391`) | | |
| F1 | 19:23-19:41 | `rf-qa` fix agent (L3080, `TF:393`); 179 tool calls | 18 of 18 fixed | |
| R2 | 19:42-19:49 | verification structural (L3122, `TF:397`), qualitative (L3126, `TF:399`) | structural FAIL I1/m5 (17 of 18 fixed); qualitative FAIL I4/m3 (18 of 18 fixed in substance) | 5: F-1, B-1, B-2, B-3, B-4 (`QA/qa-consolidated-findings-phase6-cycle2.md:1`) |
| F2 | 19:50-19:56 | `rf-qa` fix agent (L3289, `TF:405`) | 5 of 5 | |
| R3 | 19:56-20:01 | verification structural (L3332, `TF:407`), qualitative (L3336, `TF:409`) | structural PASS I0/m7; qualitative FAIL I2/m5 (`QA/qa-gate3-decision.md:47`) | 2: N-1, N-2 |
| End | | HALT asked at `BM` L3462 (20:01:40) | `GATE3_FINAL: FAIL - HALT`, then `PASS (user-accepted exception ...)` (`:56, :62`; written `BM` L3395, L3702) | 12 `Edit` calls by the main session at 20:14 (census), no fourth review |

### Gate 4: source fidelity (same report)

| Round | UTC | Agents | Result | Blocking |
|---|---|---|---|---|
| R1 | 20:15-20:25 | 3 `rf-qa` fidelity agents (L3718 `TF:417`, L3722 `TF:419`, L3726 `TF:421` with a web check) | PASS I0/m5, PASS I0/m10, FAIL I1/m4 (`QA/qa-gate4-decision.md:13-15`) | 1 (`qa-fidelity-consolidated-findings.md:1`, row 16) |
| C1, F1 | 20:25-20:35 | consolidation `rf-analyst` (L3804, `TF:423`), `rf-qa` fix (L3841, `TF:425`) | 1 fixed | |
| R2 | 20:35-20:37 | verification structural (L3883, `TF:427`), qualitative (L3887, `TF:429`) | PASS, PASS (`:18-19`) | 0 |
| End | | | `GATE4_FINAL: PASS (1 review cycle)` (`:23`; `BM` L3936) | |

The task file lists 3 fidelity agents (`TF:417-421`), the build request says 2 (`inputs/task-file/BUILD-REQUEST.md:42`). The task file is what ran.

### Gate 5: anti-omission (same report, checked against research and synthesis files)

| Round | UTC | Agents | Result | Blocking |
|---|---|---|---|---|
| R1 | 20:38-21:00 | `rf-analyst` x3 started with wrong task-file line numbers: "agent 1" (L3986) told `TF:449`, "agent 2" (L3990) told `TF:451`, "agent 3" (L3994) told `TF:453`, but the three prompts are `TF:447`, `TF:449`, `TF:451` (`TF:453` is the consolidation step and has no prompt). Result: agents L3986 and L3990 both wrote `qa-anti-omission-report-2.md` (one overwrote the other); agent L3994 noticed ("Brief error: the agent-3 prompt is on line 451", last message of `SA/agent-a2db640f53a99c857.jsonl`) and wrote report 3; a re-run "slice 1" on `TF:447` (L4031) wrote `qa-anti-omission-report-1-slice1.md` | slice 1 FAIL I2/m21; report 2 PASS m35; report 3 FAIL I4/m27 (`QA/qa-gate5-decision.md:15-17`) | raw 6, consolidated 4 (95 rows; OM-3, OM-4 downgraded Important to Minor, `:5-9`). Baseline R1 for this gate is contaminated by the brief error (see section 8, finding 6) |
| C1 | 21:01-21:07 | consolidation `rf-analyst` (L4113, `TF:453` consolidation item) | | |
| F1 | 21:07-21:13 | `rf-qa` fix (L4153, `TF:455`) | 4 of 4 | |
| R2 | 21:14-21:21 | verification structural (L4196, `TF:457`), qualitative (L4200, `TF:459`) | structural FAIL I1/m3; content FAIL I3/m7 | 3: I-1, I-2, I-3 (`QA/qa-anti-omission-consolidated-findings-cycle2.md:1`) |
| F2 | 21:21-21:23 | `rf-qa` fix (L4299, `TF:465`) | | |
| R3 | 21:23-21:26 | verification structural (L4342, `TF:467`), qualitative (L4346, `TF:469`) | structural PASS I0/m1; content FAIL I1/m2 (`:35`) | 1: N-1 |
| End | | ask `msg_8c3d61e635e2` (`BM` L4513) | `GATE5_FINAL: FAIL - HALT`, then `PASS (user-accepted exception ...)` (`:43, :49`; written `BM` L4382, L4601) | one edit by the executor (report L1542), no fourth review |

After the gates: a final validation checklist agent (`BM` L4631, `TF:475`) wrote `validation-checklist-result.md`, then the `sc-workflow-protocol` and `sc-reflect-protocol` skills ran (`BM` L5109, L5306). Those are outside the loops and outside this replay.

## 5. Reviewer tool, command and flags per round; severity rule; does PR 427 reach this?

**Tool and command.** There is no review command with flags. The run was `Skill tech-research` (`BM` L138, args: "Resume (do not rebuild) the existing task file ... at the same depth it was built; execute it with the /task skill.", file `briefs/S-skill-tech-research_L138.json`), then `Skill task` (`BM` L156, args = the task file path, `briefs/S-skill-task_L156.json`). The `task` skill executes the task file; every review step is an `Agent` tool call. Across all 65 Agent calls the only input fields are `subagent_type`, `description`, `prompt`: no model, isolation, or background option was set (counted with `jq` over `BM`). The agents ran as background agents (`requestShape: background` in `SA/agent-*.meta.json`); the usage records name model `claude-sonnet-5-5` for the main session and the agents (`pickedEffortModel: claude-gw-tier1b[1m]` in the meta files is the proxy alias; UNVERIFIED which real model sits behind it).

The only "flag" is a convention written inside each prompt: `fix_authorization: false` for the 38 report-only agents and `true` for the 9 fix agents (`BM` L841, L1075, L2018, L2202, L3080, L3289, L3841, L4153, L4299; counted by `rg` over `briefs/`).

| Gate | Round | Agent type (count) | Task-file lines |
|---|---|---|---|
| 1 | R1 | `rf-analyst`, `rf-qa`, `rf-qa-qualitative` (1 each) | 218, 222, 226 |
| 1, 2, 3, 5 | F1, F2 | `rf-qa` with `fix_authorization: true` (1 each; Gate 1 F1 started 6 `rf-task-researcher`) | 234, 254; 324, 344; 393, 405; 455, 465 |
| 1-5 | R2, R3 | `rf-qa` (structural) + `rf-qa-qualitative` (content), 1 each per round | 238-262; 328-352; 397-409; 427-429; 457-469 |
| 2 | R1 | `rf-analyst`, `rf-qa`, `rf-qa-qualitative` | 308, 312, 316 |
| 3 | R1 | `rf-qa` x3 (template-conformance, internal-consistency, evidence-quality), `rf-qa-qualitative` x4 (actionability, domain-accuracy, crossref-chain, finding-reproducibility) | 371-387 |
| 4 | R1 | `rf-qa` x3 (agent 3 adds a web check) | 417, 419, 421 |
| 5 | R1 | `rf-analyst` x3 (+1 re-run) | 447, 449, 451 |
| 2-5 | C1 | `rf-analyst` consolidation (Gate 1: the orchestrator did it, `TF:230`) | 320, 391, 423, 453 |

The agent definitions used (`~/.claude/agents/rf-*.md`) and both skills (`~/.claude/skills/tech-research/SKILL.md`, `~/.claude/skills/task/SKILL.md`) are dated 2026-11-05 13:13, two days before the run, so they were the versions used (file dates; the `tech-research` text loaded at `BM` L142 equals the installed file apart from front matter, checked by `diff`).

**Severity rule in force.** One rule, the same in every round of every gate (task file `TF:130` Key Constraints, repeated at `TF:214` for Phase 3 and `TF:361` for Phase 6, and in each agent prompt, e.g. `TF:218`): "Maximum 2 fix cycles (3 reviews), then HALT and escalate to the user with the open blocking findings. Only blocking findings (CRITICAL/IMPORTANT) fail a gate; MINOR findings are notes and are never rechecked." The `rf-qa` prompt (`TF:222`, file `briefs/taskfile-L222_embedded-prompt.md`) says: "CRITICAL or IMPORTANT is blocking (a real defect: wrong behaviour, a false claim, a missing required deliverable, a security or data-loss risk); MINOR is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim", with verdicts only PASS or FAIL. Re-grading: the consolidator may change a severity if it gives a file:line reason in a `## Severity changes` section; the orchestrator counts downgrades in `SEVERITY_DOWNGRADES: <n>` (`TF:230`, `TF:246`). Downgrades happened in Gate 3 (5, after the orchestrator restored 2) and Gate 5 (2); none elsewhere. MINOR findings were never rechecked, as the rule says.

**Does PR 427 reach this scenario? No.** (1) No `/sc:spec-panel` call exists in the main log or in any of the 71 agent logs: the only mentions of "spec-panel" in `BM` are the skill list in the system prompt (lines 19, 29, 4771, 4785, 4818); no agent tool call contains it. (2) PR 427 (`95f2c6e4`) changes `src/superclaude/commands/spec-panel.md`, its plugin mirror, `src/superclaude/core/HOW-WE-WORK.md` and its mirror, two release guides, `docs/designs/spec-panel-review-loop.md` and `tests/skills/test_spec_panel_review_loop.py` (`git show --name-only 95f2c6e4`). (3) None of those is read by `tech-research`, `task` or the `rf-*` agents (`rg -c spec-panel` over those files: 0 hits). (4) The work repo is Coder, not IronClaude, and the skills and agents come from the installed `~/.claude`, which 427 does not touch. Expected effect of 427 on S4: zero by construction. S4 can only show the run-to-run spread of the existing 3-review-cap pipeline.

## 6. How the starting documents were recovered, and how well that is verified

Problem: the logs hold edits, not documents, and the QA gates stored no copy of the file under review. Method: replay. Every Write, Edit and `cat >> file <<'EOF'` heredoc append on a file is in the logs (the main log and the 71 agent logs), together with the assembler's `sed -n ... >> report` commands that built the report body from the synthesis files. `tools/reconstruct.py` replays them in timestamp order with the Edit tool's rules and prints size, newline count and sha256 at chosen times. Nothing is run in the Coder worktree; replay happens in a sandbox under `/tmp`.

| State | How rebuilt | Independent check | Result |
|---|---|---|---|
| Report at end of Gate 3 fix 2 (19:56, 387,624 bytes, 1,795 lines) | Write stub + 5 assembler `sed`/heredoc steps + the Edit calls of the assembler, Gate 3 fix 1 and fix 2 | file-history `ca7857aee503d1e6@v1` | identical, sha256 `48bd1484ace25d6c...` |
| Report final (407,656 bytes, 1,807 lines) | same, to the end | file on disk in the Coder worktree | identical, sha256 `0b21d61bd796ebe1...` |
| Report at assembly = Gate 3 start (364,593 bytes, 1,785 lines) | same, up to 19:00:30 | line count 1,785 stated in `BM` L2844; no stored copy | consistent, RECONSTRUCTED |
| 13 files: research 01-05, web-01, web-02, gaps, synth 01-04, report | full replay | each equals the file on disk now | all 13 identical |
| `research/research-notes.md` before Gate 1 (16,653 bytes) | no Write exists; 10 Gate 1 edits reversed from the file on disk, then replayed forward to the disk hash | git object with the same hash exists in the Coder repo | exact |
| Gate 2 start: 7 research files + gaps (8) and Gate 3 start: the same 8 + 4 synthesis files (12) | replay | all 20 hash to objects that exist in the Coder repo (staged by `git add .dev/tasks` during the run) | exact |
| Gate 1 start: research 01-05; Gate 2 start: synth 01-04; Gate 3/4/5 start: report | replay only | none stored. For Gate 1 the replay line counts are 364/380/236/267/291 newlines, and the Gate 1 analyst quotes 365/381/237/268/292 for the same files (`QA/analyst-completeness-report.md:180`), which is the same numbers plus one for the missing final newline | consistent, RECONSTRUCTED |

So 21 of the 33 starting states are confirmed against a stored git object (1 at Gate 1, 8 at Gate 2, 12 at Gate 3). The other 12 are replay-only: 5 Gate 1 research files, 4 Gate 2 synthesis files, and 3 report states (Gate 3, 4, 5 start). Every replay chain ends at a byte-identical stored file (the report at the end of Gate 3 equals the file-history copy; the 13 final files equal the files on disk). The replay is deterministic and the script prints its own failures: 0 failed edits and 0 unhandled Bash writes for every file.

## 7. How each loop ended and why

- Gate 1: review 3 left one IMPORTANT finding, New-1 (`QA/qa-gate1-decision.md:40`): lines 376 and 408 of research file 05 still said the option-C wrapper is not exercised by test-57. Cause: fix 2 corrected line 318 and two matrix rows but not the two other places that repeat the claim (`QA/qa-verification-phase3-cycle2-content.md:34`). The task file says HALT at the cap; the orchestrator asked the user (`BM` L1247, options "Accept: fix the 2 lines myself, no 4th review, continue (Recommended) / Allow a third fix cycle with a full 4th review / Stop and report failed"); the user accepted; the executor edited the two lines and ran no review.
- Gate 2: V-1 and V-2 (`QA/qa-gate2-decision.md:39-40`): an unlabelled inference ("Stage 0 satisfies the CLI reading") repeated in 9 places, and plan rows still unconditional under that reading. Both come from the text the earlier fixes wrote to resolve finding 6. Same ask, same answer (`BM` L2377).
- Gate 3: N-1 and N-2 (`QA/qa-gate3-decision.md:53-54`): the same "B3 and D3 are modules.tf only" claim survived in three other places; a memlog rule was half-fixed. Same ask (`BM` L3462), same answer.
- Gate 4: clean at review 2. One finding in review 1 (row 16, the web-source check), fixed, verified.
- Gate 5: N-1 (`QA/qa-gate5-decision.md:41`): a test fixture added by fix 2 made the skill count off by one. Ask `msg_8c3d61e635e2`, user accepted, one edit.

Three reviews were run in each of Gates 1, 2, 3 and 5; a fourth was never run. The "clean pass" in the decision files (`GATE1_FINAL: PASS (user-accepted exception, 3 reviews plus two-line manual fix; no fourth review)` and the same for 2, 3, 5) is therefore not a reviewed pass. The text edited under the exceptions was not reviewed by any agent; the report says so itself in its section "Quality Gates and User-Accepted Exceptions" ("The text edited under these two exceptions was not reviewed by a further agent", written by the assembler command at `SA/agent-a9c6678fe08ab2dda.jsonl` L124).

Pattern across gates (M3): of the 23 blocking findings in reviews 2 and 3 (Gate 1 6+1, Gate 2 3+2, Gate 3 5+2, Gate 5 3+1; Gate 4 had none), all 23 are, by the reviewers' own wording or my reading of it, introduced (text the fix wrote), exposed (the fix made two parts disagree), or residual (the fix covered some but not all places of the same defect). Split: introduced 11, exposed 4, residual 8. Reviewer-tagged origin exists for 12 of the 23 (Gate 1: X-1 and New-1; Gate 2: N-1 to N-3; Gate 3: all 7); the other 11 are my re-derivation from the finding text and the consolidated tables (Gate 1 R2: five findings besides X-1, which the coordinator also called fix-written at `BM` L1093; Gate 2 R3: V-1, V-2; Gate 5: all 4). Each is marked in `baseline-metrics.json` (`source_type`).

## 8. Findings (severity-rated, per /sc:analyze)

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | High | S4 does not use `/sc:spec-panel`; PR 427 cannot change it. A "427 active" arm is identical to the baseline replay for every file this pipeline reads. | section 5 |
| 2 | High | The loops are closed by a user decision, not by a rule. A replay without a human must pre-set the stop rule and not accept the exception, or it cannot reach a comparable end state. | `BM` L1247, L2377, L3462, L4513; section 7 |
| 3 | Medium | Every blocking finding after review 1 traces to the previous fix cycle (23 of 23). This is the failure shape of issue 346, in a different tool. | section 7 |
| 4 | Medium | The fix agent grows the document by adding addenda, not by editing in place: Gate 1 research files +67.7 percent in bytes (255,114 to 427,771) in two cycles; Gate 2 +4.6; Gate 3 +6.7; Gate 5 +4.2. Phase 1's "about 1 percent" counted lines of the report only. | `evidence/m4-sizes.tsv`, `baseline-metrics.json` |
| 5 | Medium | Phase 1 understated the incident: four halted gates and four user exceptions (not three and one). | section 2 |
| 6 | Medium | Gate 5 review 1 had brief errors (line numbers off by two; two agents wrote the same file, one re-run). Baseline Gate 5 R1 counts are therefore not clean; Gate 5 is the weakest gate to compare. | `briefs/G5-R1-*`, `SA/agent-a2db640f53a99c857.jsonl` last message |
| 7 | Low | Not reproducible by replay: the model's research and review text (non-deterministic), the answers of the user to the asks (text not located in the log; the decision files only say "the user"), web access (Tavily was absent; WebSearch/WebFetch used), and `/opt/uv/tools/superclaude` and `bmad` 6.9.0 as read on this machine (installed 2026-11-06, still present; UNVERIFIED that nothing changed since). | `phase1/REPORT.md:235`, `ls -ld /opt/uv/tools/superclaude` |
| 8 | Low | The task file's ticked boxes and Task Log at each gate start were not recoverable per gate; `tools/make_gate_entry.sh` ticks every box before the gate's first step. | `inputs/task-file/`, REPLAY.md |
| 9 | Info | Cost of the baseline: gates 1-5 = 58 agent runs, 3,972 agent tool calls, 2.87 million output tokens, 14.7 million fresh input tokens; Gate 3 alone: 14 agents, 1,083 tool calls, 868k output tokens, 61 minutes. | `evidence/agent-costs.tsv` |

## 9. Metrics summary (full detail and sources: `baseline-metrics.json`)

| Gate | Blocking R1 / R2 / R3 | Raw Important in R1 | Fix-caused share R2 / R3 | Document bytes: start, R2, R3, end (growth) | Agent tool calls R1 / R2 / R3 |
|---|---|---|---|---|---|
| 1 | 9 / 6 / 1 | 12 | 6 of 6 / 1 of 1 | 255,114; 418,963; 427,363; 427,771 (+67.7%) | 288 / 191 / 149 |
| 2 | 8 / 3 / 2 | 9 | 3 of 3 / 2 of 2 | 370,900; 381,278; 385,713; 387,829 (+4.6%) | 261 / 82 / 68 |
| 3 | 18 / 5 / 2 | 27 | 5 of 5 / 2 of 2 | 364,593; 382,659; 387,624; 389,044 (+6.7%) | 603 / 109 / 89 |
| 4 | 1 / 0 | 1 | 0 of 0 | 389,044; 391,163 (+0.5%) | 374 / 77 |
| 5 | 4 / 3 / 1 | 6 | 3 of 3 / 1 of 1 | 391,163; 403,660; 405,371; 407,656 (+4.2%) | 224 / 93 / 71 |

M1 (reviews to clean pass): Gate 4 = 2; Gates 1, 2, 3, 5 = none within the cap of 3 (null in the JSON, with the reason). M2 last-round blocking: 1, 2, 2, 0, 1. Document sizes use the newline count for "lines".

## 10. What this means for the replay (REPLAY.md has the runbook)

- Replay unit: one gate at a time, entered from the rebuilt state (`tools/make_gate_entry.sh 1|2|3`), not the whole 8.5-hour pipeline, because the pipeline's first half (research and synthesis agents with web search) cannot be repeated to the same text.
- Primary replay: Gate 3 (one document, byte-exact stored endpoints, 7 parallel reviewers, 3 clean rounds of baseline data). Secondary: Gate 2, Gate 1. Gates 4 and 5 have inputs but no validated runbook.
- Because PR 427 cannot affect S4, use S4 as a control (noise floor) in the experiment, not as a spec-panel scenario, unless the coordinator wants a different swap (REPLAY.md, "Does PR 427 matter here").

## 11. UNVERIFIED and limits

- The user's answer text to the HALT asks is not in `BM` as a message I could find; I rely on the decision files (`QA/qa-gate1-decision.md:46`, and the equivalents).
- The M3 origin of 11 of the 23 findings (and the whole introduced/exposed/residual split) is my reading of the finding text, not a reviewer tag.
- I did not re-count every finding row in the 80 `qa/` files; counts come from the decision files' tables and the `BLOCKING_COUNT:` first lines, which I read directly.
- Orchestrator-session cost per round (in the JSON) is by time window and includes waiting-free work only; it is an approximation.
- Nothing was run: no reviewer, no `/sc:spec-panel`, no live loop. The tools only read logs and copy files.
