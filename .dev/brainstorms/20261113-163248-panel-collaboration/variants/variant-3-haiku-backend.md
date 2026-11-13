# Requirements specification: reviewer collaboration during runs (variant 3, backend lens)

Sources read: the seed brief, the four enrichment files, `tools/run-reviewer.sh`, `HANDOFF-review-panel-unification-run2.md` (lines 1-363), and `COMBO-REPORT.md` (lines 380-507). Numbers below are from those files unless marked as an estimate.

## 1. Theories

Three theories explain the misses. T1 and T2 are refined from the seed brief. T3 is split into four parts. The reasoning-budget theory is tested and rejected as the main cause (see the end of this section).

**Legend (plain meaning of each defect, with the number of valid-era runs, out of 76, that found it):**

| ID | What is wrong in the plan (plain English) | Blocking in implement | Found in runs |
|---|---|---|---|
| B1 | Task 1 check demands a "complete" inventory with no stopping rule | yes | 0 |
| B2 | Task 1 names four files, but its check says only "found for O3" | yes | 0 |
| B3 | Task 9 test condition is undefined | yes | 68 |
| B5 | Task 8 exit report drops the "unavailable" rule, so it reports "released" after an engage halt | yes | 3 |
| B6 | "Aliases only" goal contradicts Task 5 slot ladder; the test cannot enforce it | yes | 1 |
| B7 | "Nothing is set" text contradicts a constraint | yes | 20 |
| B8 | "All other primitives use aliases" is false; the test skips files with no `model:` line | yes | 1 |
| I1 | Fold rule never sets the cause that the status map reads | no | 3 |
| I2 | resume signature lacks two inputs row 4 needs | no | 52 |
| I4 | Heading grep cannot match the heading the task names | no | 4 |
| I5 | CHANGELOG still says "43 members" after the change | no | 0 |
| I6 | User-guide text omits the "defaults file exports real ids today" clause | no | 0 |
| I7 | Test `test_worker_contract.py` pins exact lines the plan edits; no task updates it (control) | no | 9 |
| I8 | Read-back rule does not match the real API response (control) | no | 56 |

Sources: legend `COMBO-REPORT.md` lines 401-418; all-sets table lines 430-498 (valid era is the ALL-src row, 76 runs).

### T1 (refined): Plan-bounded search misses the reverse-dependency sweep

- Cheap models check only the files the plan names. The missing move is the reverse-dependency query (which tests and docs reference the files this plan edits?), not more search.
- Evidence: 7 of 8 DE runs that touched `test_worker_contract.py` reported I7; 0 of 225 that did not (`investigation-patterns.md` section 6). Haiku searched `tests/` in 81% of runs (5.2 searches per run) but opened the unnamed test file in 0 of 25 DE runs. Sonnet opened unnamed files at 3.1 per run versus ember 0.8 and luna 0.3.
- Refinement: search volume is not the variable. The variable is whether the search is a reverse-dependency query.

### T2 (refined): Right anchor, one-axis analysis

- Cheap reviewers anchor the right sentence and analyse one axis of it.
- Evidence: 16 findings anchored the GT10 CHANGELOG-adjacent Task 2 grep sentence, and all asked whether the grep over-matches, none asked where else the claim appears (`investigation-designspec.md` section 2c). Three GT5 findings analysed only the mode-off path, not the halt path. Zero of 98 cheap reports anchored Task 1 AC3 (`candidate.md:38`).
- Refinement: the miss is one missing axis (other input case, other direction, literal command). A peer can supply the axis without giving the answer.

### T3 (refined, four parts): The evidence environment and the rules hide defects

- **Sandbox is post-implementation.** `manifest.md:10` archives HEAD, which contains the repairs: `merge_guard.py:256` (fixes B5-related cause), `refs/merge-guard.md:146` (fixes the halt rule), `commands/pr-submit.md:81` (passes the heading grep). The narrowed `refs/tiers.md:42` was seen by 44 of 98 cheap alias reviewers, and none compared it with Task 7's wider text (`investigation-alias-control.md` section 2).
- **source.md is not used.** 156 of 665 valid runs never referenced it, including 81 of 209 ember runs (COMBO-REPORT R14, line 129).
- **Merge drops.** Anchors over 200 characters are dropped with no repair (`findings.py:104-110`, HANDOFF D1 line 162). 49 blocking findings were lost.
- **Grading rule.** An unstated requirement is graded Medium, and there is no missing-task category (`prompts:31, :60`). All 7 true I7 findings were non-blocking.
- **Leak.** `.dev/reflect/pre-design-20261108041729/REPORT.md` names I7 and sits in the sandbox. 2 of the 9 I7 credits read it (`investigation-alias-control.md` section 3).

### Rejected: reasoning budget (Theory A in `investigation-patterns.md`)

Thinking tokens correlate with hits across models (Spearman 0.64). Within ember and luna, hard-issue hits do not rise with thinking (ember 0.25 to 0.22; luna 0.09 to 0.09). Budget explains haiku's variance, not the ceiling of ember or luna.

## 2. Five redesigns

**Shared rules for all five.** Reviewers keep Edit, Write and NotebookEdit disabled (`run-reviewer.sh:48`). Each reviewer writes a sealed first-pass file (`pass1.md`) before it receives any peer content. A hook refuses to release peer content until the file exists. Messages use only a fixed enum of six generic moves, scope words and status words. There is no free-text field, so no defect text can cross between reviewers. The six moves:

| Move | Generic instruction (applies to any plan) |
|---|---|
| M1 | For each criterion that says every, all or complete, state the finite check that proves it. |
| M2 | Search the whole tree for files that reference each file the plan edits; open any test or doc the plan does not name. |
| M3 | For each all, only or every sentence, list the files it covers and count the exceptions. |
| M4 | Run each grep or command criterion against the exact text the plan tells the implementer to write. |
| M5 | For each changed claim, search where else in the repo the same claim appears. |
| M6 | Apply each constraint to every verbatim text the plan dictates. |

Model choice: ember, luna and sonnet only. Haiku (233 s median) and grok (790 s) alone break the +35% cap. Glm and Qwen are excluded. Opus is the blind judge only.

**Time arithmetic (common baseline).** The isolated panel (ember + 2x luna) takes about 116 s per package (348 s over three packages, per the seed brief). Its slowest reviewer is luna at about 102 s, so about 14 s is fixed harness overhead. The +35% cap is about +41 s, so the new total must stay at or below about 157 s. If the 348 s figure is a per-package figure instead, every budget here is conservative.

### R1. Sweep Relay (between-phase digest)

- **(a) Mechanism.** Phase 1 is the unchanged isolated run: ember, luna and luna. The harness builds a digest of which moves each reviewer ran and which no reviewer ran. It contains no findings. In phase 2, ember and one luna resume their own sessions with the digest. Ember runs the unrun moves quickly. Luna runs the deep reads. Each returns a complete replacement findings-v1 block, which the harness assembles from phase 1 and phase 2 findings.
- **(b) Schedule.** Trigger: all three phase-1 blocks exist. Max messages per reviewer per package: 1 digest in, 1 block out. Digest cap: 1,200 characters. Schema: `{"moves_run":{"M1":["ember"]},"moves_unrun":["M2","M5"]}`. Phase-2 addendum cap: 8 findings under the existing findings-v1 limits.
- **(c) Transport.** Between-phase digest, mediated by the harness (temp file, then `mv`). Phase 2 uses `claude -p --resume <session_id>` from the JSON result. Why: it needs no hooks or live channel, and it is deterministic and auditable. UNVERIFIED: resume with gateway model ids.
- **(d) Time.** Phase-2 luna capped at 30 s, digest 3 s, ember phase 2 runs in parallel at 25 s cap and is not on the critical path. New critical path: 102 + 14 + 3 + 30 = 149 s. Added +33 s, which is **+28%**.
- **(e) Contamination.** Shared: move coverage only. Withheld: all peer findings, anchors, claims, file names, phase-1 text. Independent first pass: phase 1 is untouched, and phase-2 findings are tagged so the merge can separate them. Blind-spot spread is blocked because no peer finding crosses. Convergence alarm: flag any run where more than 50% of phase-2 anchors duplicate phase-1 anchors, or where pairwise anchor Jaccard across reviewers exceeds 0.5 (baseline ember + luna 0.25; ember + haiku 0.47, `investigation-patterns.md` section 3).
- **(f) Gain (collaboration share only, issues of 14 per run).** Targets: I7 (M2), B8 (M3), I5 (M5), B5 (M1), I4 (M4). Assumptions: P(move run in phase 2) 0.6 to 0.9; P(issue found | move run) 0.15 to 0.4 for cheap models (estimate; sonnet's 7-of-8 rate is the upper reference). Expected: **0.4 low, 1.2 high**.
- **(g) Effort.** `tools/run-reviewer.sh` +45 lines (phase-2 call, cap, digest call). New `digest.py` about 60 lines with schema check. New phase-2 brief about 30 lines. Block assembly about 40 lines. Total about 175 lines in 3 files, 2 new. Merge contract unchanged (one block per reviewer).
- **(h) Failure modes.** Resume fails for gateway ids (UNVERIFIED), so phase 2 silently becomes no-op. Unrun-move digest pushes reviewers into false blockers (wrong blockers rise). The 30 s cap truncates a tool call mid-run. Session expiry between phases.

### R2. Move-Hint Board (mid-run, JSON board with hooks)

- **(a) Mechanism.** Each reviewer appends one line per move it completes to `$PANEL_BOARD/<id>.jsonl`. A PostToolUse hook injects peer lines as `additionalContext` after each tool call, but only after the reviewer's `pass1.md` exists. A Stop hook does one final read. Ember (fast, first to finish) posts the moves it ran; luna runs the complementary moves. Roles: ember is the early announcer, luna is the consumer.
- **(b) Schedule.** Triggers: write at each completed move; read at each tool call after seal; one final read at Stop. Max outbound messages per reviewer per package: 4. Line cap: 240 characters. Schema: `{"from":"ember","move":"M2","scope":"repo_wide","status":"ran"}`. Scope values: `plan_text`, `named_files`, `repo_wide`, `tests`. No file names in lines.
- **(c) Transport.** JSON board with PostToolUse and Stop hooks, passed per run with `--settings`. Why: model-agnostic on receive, durable audit log (the board is the record of the exchange), about 40 lines of bash, no new service. UNVERIFIED: hook commands inherit `PANEL_BOARD` and `PANEL_ID`.
- **(d) Time.** Hook overhead about 3 s over about 13 tool calls, plus about 15 s acting on hints. Luna: 102 + 14 + 20 = 136 s. Added +20 s, **+17%**. Ember's idle time (about 60 s while luna works) absorbs the posts.
- **(e) Contamination.** Shared: move names and scope words. Withheld: findings, anchors, claims, file names, peer conclusions. Independence: luna's seal precedes any release. Blind-spot spread: the enum rules out defect text. Alarms: a leak check (any board line containing a 12-character or longer substring of another reviewer's anchor is a hard failure) and the Jaccard alarm from R1.
- **(f) Gain.** Targets: B1 (M1), B2 (M1, M3), B5 (M1), I4 (M4), I5 (M5). Assumptions: P(hint acted on) 0.5 to 0.8; P(issue | acted) 0.1 to 0.3 (estimate). Expected: **0.2 low, 0.9 high**.
- **(g) Effort.** `panel-post` helper about 10 lines, `panel-read` about 15, hook script and JSON about 25, launcher changes about 25 (exports, `--settings`, seal check), prompt addition about 15. Total about 90 lines in 3 new files.
- **(h) Failure modes.** Hook environment inheritance fails, so the board is silently empty (UNVERIFIED). Luna ignores injected context (gateway model compliance). Injection arrives after the last tool call. Per-sender files avoid write races but a missing Stop hook leaves the final read undone.

### R3. Capped Sweep Specialist (sonnet with a 130 s hard cap)

- **(a) Mechanism.** One sonnet session starts at t=0 and runs only M2 and M3 sweeps, with a hard 130 s timeout and at most 6 board posts. It posts path lists and counts only, with no interpretation. Ember and luna run isolated and read sweep lines after their seal. Sonnet also writes a normal findings block. Role: sonnet is the long-reach sweeper (the study's sonnet opened 3.1 unnamed files per run). Ember and luna are consumers.
- **(b) Schedule.** Sonnet posts at each completed sweep (max 6). Consumers read at each tool call after seal. Line cap: 240 characters, with at most 10 paths per line. Schema: `{"from":"sonnet","move":"M2","scope":"repo_wide","paths":[{"p":"tests/skills/x.py","refs":3}]}`.
- **(c) Transport.** JSON board, same hooks as R2.
- **(d) Time.** The panel waits for sonnet's cap. Critical path: max(102, 130) + 14 = 144 s. Added +28 s, **+24%**. Cap must stay at or below 142 s to meet the +35% cap while the panel waits.
- **(e) Contamination.** Shared: path lists and counts, which are repo facts, not conclusions. Withheld: sonnet's findings and reasoning. The risk is that a path list points consumers at a specific file. Mitigation: the same sweep runs on any plan (generic), and the leak check applies. Convergence alarm: the Jaccard alarm, plus the share of luna findings that cite a sweep path.
- **(f) Gain.** Targets: I7 (M2), B8 (M3), B6 (M3 across tasks), I5 (M5). Assumptions: P(sweep completes its useful part in 130 s) 0.5 to 0.8; expected issues per completed sweep 0.8 to 1.2 (sonnet found I7 in 7 of 8 runs that opened the test file); consumers act on hits 0.5 to 0.8 (estimate). Expected: **0.3 low, 0.9 high**.
- **(g) Effort.** Specialist launcher role about 30 lines; the cap is one `timeout` line; sweep prompt about 25 lines; board from R2 about 90 lines. Total about 150 lines.
- **(h) Failure modes.** The 130 s cap truncates most sonnet runs (median 228 s). Repo-wide greps return large lists that drown the signal. Sonnet's sweep steers luna toward tests, which can raise wrong blockers. Token cost rises by about 46%.

### R4. Challenge Pair (cross-session messaging, ember and luna)

- **(a) Mechanism.** Ember and luna start with `--name` and `--settings '{"crossSessionInbound":"accept"}'`. After its seal (about 60 s), luna sends one challenge that asks ember to run one named move on the plan and report the result. Ember replies with the result and may send one challenge back. Role: ember is the fast checker, luna is the challenger. Challenges are moves, not defect text.
- **(b) Schedule.** Trigger: luna's seal. Max messages per reviewer per package: 3 each way. Reply cap: 240 characters plus one evidence path. Schema: `{"move":"M1","result":"ran","evidence":"candidate.md"}`. Ember must hold its session open until luna's final output or a 60 s window closes.
- **(c) Transport.** Cross-session SendMessage. Why: fewest changes (two flags and a prompt), mid-run delivery between tool calls. UNVERIFIED: gateway models call the tool with the right name, and what happens to messages that arrive after a session ends (held messages expire after 5 minutes).
- **(d) Time.** Ember's reply fits in luna's remaining run. Luna waits about 8 s to read it. Critical path 102 + 14 + 12 = 128 s. Added +12 s, **+10%**.
- **(e) Contamination.** Shared: move names and result words. Withheld: findings and reasoning. The risk is high: a peer's frame passes into the reply through the result text. Mitigation: replies carry only the move result, and luna's seal precedes the challenge.
- **(f) Gain.** Targets: B1, B2, B5, I4 (satisfiability and trace challenges). Assumptions: P(challenge yields a finding) 0.1 to 0.3 per target (estimate). Expected: **0.1 low, 0.6 high**.
- **(g) Effort.** Launcher `--name` and `--settings` about 15 lines; messaging prompt about 25 lines. No board. Total about 50 lines.
- **(h) Failure modes.** Ember exits before the challenge arrives. `ListAgents` shows every local session, so names must be unique per run. Gateway models misuse the tool. Held messages expire.

### R5. Coverage Claims (board, no content)

- **(a) Mechanism.** Before its first tool call, each reviewer claims up to 3 moves it will run. It reads peers' claims at each tool call. Unclaimed moves may be taken. No content is exchanged. Purpose: the panel runs all six moves once instead of the same moves three times. Roles: ember claims M4 and M5 (fast checks); luna claims M1, M6 and deep reads; second luna claims M2 and M3.
- **(b) Schedule.** Trigger: start (claim) and seal (one re-claim). Max messages per reviewer per package: 4. Line cap: 120 characters. Schema: `{"from":"luna","claim":"M1"}`.
- **(c) Transport.** JSON board with hooks (same as R2).
- **(d) Time.** About 5 s for claim writes and one extra hook read. Critical path 121 s. Added +5 s, **+4%**.
- **(e) Contamination.** Only claim lines cross. Claims are set before any reading, so no content can carry through. Spread risk is low. Alarm: a claimed move that no reviewer reports running is a flag (claim without execution).
- **(f) Gain.** Only through coverage of moves no reviewer ran in isolation. Targets: I7, B8, I5. Assumptions: P(claimed move actually run) 0.5 to 0.8; the gain then follows R1's rates. Expected: **0.1 low, 0.5 high**.
- **(g) Effort.** Board from R2 about 90 lines plus claim helper about 20 lines. Total about 110 lines (shares files with R2).
- **(h) Failure modes.** Claims ignored. Claims collide. A claimed move gets ticked without being run.

**Harness fixes (separate from all five designs, not collaboration):** source.md named by path in the brief (`run-reviewer.sh:10` is hard-coded to this worktree; the brief has no source placeholder, `prompts:17-21`); anchor limit raised or truncated with a logged warning (`findings.py:104-110`); sandbox at the plan's base commit, with `.dev/reflect`, `.dev/eval-workspaces` and `.dev/research` excluded. Estimated gain: **0.8 low, 2.1 high** issues per run. Assumptions: recovering dropped blocking findings, +0.2 to +0.5; source.md, +0.3 to +0.8 (GT5 and GT6 need it); base-commit checkout unmasking B5, B8 and I4, +0.3 to +0.7; reflect leak, +0 to +0.1. Overlap with collaboration assumed at 20%.

## 3. Comparison of the five redesigns

Overheads are against the isolated baseline (116 s and about 63.6k tokens per panel run, `COMBO-REPORT` R4). Gain is collaboration share only, issues of 14 per run. Harness fixes are separate (0.8 to 2.1).

| Redesign | Elapsed overhead | Token overhead | Expected gain (low to high) | Contamination risk | Effort (new lines, new files) | Reliability |
|---|---|---|---|---|---|---|
| R1 Sweep Relay | +28% (+33 s) | about +12% | 0.4 to 1.2 | Low | about 175 lines, 2 new files | High; resume for gateway ids UNVERIFIED |
| R2 Move-Hint Board | +17% (+20 s) | about +10% | 0.2 to 0.9 | Low to medium | about 90 lines, 3 new files | Medium; hook environment UNVERIFIED |
| R3 Capped Sweep Specialist | +24% (+28 s) | about +46% | 0.3 to 0.9 | Medium | about 150 lines | Medium to low; 130 s cap truncates |
| R4 Challenge Pair | +10% (+12 s) | about +6% | 0.1 to 0.6 | High | about 50 lines | Low; end-of-turn and tool use UNVERIFIED |
| R5 Coverage Claims | +4% (+5 s) | about +3% | 0.1 to 0.5 | Low | about 110 lines (shares R2 files) | Medium |

Reading the table: R1 gives the most gain within budget and the lowest contamination. R2 is the only one that tests live mid-run transport, which the seed brief asks about. R3 costs the most tokens. R4 is the cheapest to build but the most likely to spread a peer's frame.

## 4. Recommended first experiment

**Goal.** Measure whether mid-run move exchange adds issues beyond fixed harness behaviour, on the three existing packages (designSpec, alias, control), scored by the existing blind Opus judge (`judge-one.sh`, anonymised merges, `ground-truth.json`).

**Pre-condition (not optional).** Apply the harness fixes first, so Arm A0 measures the fixed harness.

| Arm | Design | Panel | Panel runs (each covers all 3 packages) |
|---|---|---|---|
| A0 | Fixed harness, isolated | ember + 2x luna | 10 |
| A1 | R1 Sweep Relay | ember + 2x luna | 10 |
| A2 | R2 Move-Hint Board | ember + 2x luna | 10 |

Total: 30 panel runs, 90 package runs. R3, R4 and R5 are deferred: R3 adds sonnet's token cost, R4 depends on unverified transports, and R5's gain is small. Reviewer-group size stays fixed at three so that the arms differ only in communication.

**Metrics.** Primary: defect-rich found out of 14 per panel run. Secondary: real blocking out of 8, wrong blockers per run, control found out of 2, elapsed time (from `cost.json` `total_wall_s`), tokens, leak count, and convergence flags.

**Decision rule** (A1 and A2 each compared against A0):
1. **Adopt** the arm if its mean found improves by at least +1.0, the bootstrap 95% interval of the difference excludes zero, real blocking does not fall, wrong blockers rise by no more than 0.5, control found does not fall by more than 0.5, elapsed stays within +35% of A0, and the leak count is zero.
2. **Extend** to 20 runs per arm if the improvement is between +0.5 and +1.0, or if the point estimate is at least +1.0 but the interval includes zero. Apply the same rule at 20 runs.
3. **Reject** collaboration if the improvement is below +0.5. Ship the harness fixes only.

**Power.** The study's standard deviation is about 0.94 (`COMBO-REPORT` line 424). At 10 runs per arm, power for a +1.0 difference is about 60% (estimate). The extension rule exists for this reason.

**Caveats that block product adoption.**
- The move enum was derived from these three misses. A result on these packages is in-sample. Freeze the enum (record its sha256 in the manifest) before the experiment, and require a fourth, unseen plan package to confirm before any product change.
- The judge is the same model family as the panels' referee role. Double-score a random sample with a second judge, as audit E did for 12 rows (`COMBO-REPORT` line 296).

## 5. Numbered, testable requirements (chosen designs: R1 and R2 in the first experiment; the others must meet the same tests if adopted later)

1. **Read-only reviewers.** `Edit`, `Write` and `NotebookEdit` stay in `--disallowedTools`. Test: grep of the launcher; a reviewer that attempts an edit gets a denial.
2. **No leaked material in the sandbox.** `.dev/reflect`, `.dev/eval-workspaces`, `.dev/research`, `ground-truth*.json` and judge files are absent. Test: a file listing of the sandbox must not match these names.
3. **Base-commit sandbox.** The sandbox is the plan's base commit (its sha recorded in `manifest.md`), not HEAD. Test: `git rev-parse` in the sandbox equals the recorded base sha; the test fails if `merge_guard.py` already contains the repaired `disabled_cause` assignment.
4. **source.md named in the brief.** The brief names the source path and has a placeholder. Test: at least 95% of transcripts show a Read of source.md.
5. **No silent finding drops.** An anchor over 200 characters is either accepted (limit raised to 300) or truncated with a logged warning. Test: the 49 known dropped blocking findings in the fixture all survive merge.
6. **findings-v1 unchanged for merge.** Collaboration output goes in a separate section outside the fenced block. Test: `superclaude review merge` runs unchanged, and every reviewer report has exactly one findings block.
7. **Closed message schema.** Board lines and digests use only the fixed fields and enum values; any other field is rejected. Test: a schema validator reports zero accepted free-text lines in the pilot.
8. **Size caps.** Board line 240 characters (120 for R5); R1 digest 1,200 characters. Test: a length check on every line; violations are rejected, not truncated.
9. **Message count caps.** Max outbound messages per reviewer per package: 4 (R2), 1 digest in (R1). Test: counted from the board files.
10. **Seal before release.** Peer content is released to a reviewer only after its `pass1.md` exists, and the first-pass file's timestamp is earlier than the first peer line it receives. Test: timestamp comparison for every run.
11. **No cross-reviewer anchor leakage.** A board line may not contain a 12-character or longer substring of another reviewer's anchor. Test: a hard failure on any match; the target is zero.
12. **Convergence alarm.** Flag a run when pairwise anchor Jaccard across reviewers exceeds 0.5, or when more than 50% of phase-2 anchors duplicate phase-1 anchors. Test: alarm count is written to each run's metadata and reported.
13. **Elapsed time cap.** Added elapsed time per package is at most 35% over the isolated A0 baseline measured on the same gateway load day. Test: `cost.json` `total_wall_s` comparison per package.
14. **Tokens reported.** Output and thinking tokens of every arm are reported as overhead against A0. Test: the report table lists both; no cap is imposed.
15. **Model allowlist.** Reviewers are ember, luna, haiku, sonnet or grok only. Glm, Qwen and Opus are never reviewers (Opus is the judge only). Test: `observed_model` in every `meta.json` is in the allowlist.
16. **Identity check kept.** `model_ok` stays required, and the fallback ladder is disabled for the experiment (`NOFALLBACK=1`). Test: a run with a fallback log is excluded and counted.
17. **Hooks scoped to the run.** Hooks and session settings are passed per run with `--settings`. The user's `~/.claude/settings.json` is untouched. Test: its sha256 is equal before and after the experiment.
18. **Move enum frozen.** The six-move enum file is hashed before arm A1 starts; any change invalidates the arms that used the old hash. Test: the hash is recorded in the manifest and checked at each run.
19. **Judge blind and auditable.** The Opus judge sees only the ground truth, the candidate and an anonymised merged report. Test: the API-error audit reports zero bad judge files, and a random 12-row sample is double-scored.
20. **Decision rule applied as written.** The decision uses section 4's rule, with the same metrics, and the extension (20 runs) is triggered only by the stated conditions. Test: the decision record lists each condition with its value.
21. **Hold-out before adoption.** No product default changes until a fourth, unseen package confirms the gain under the same rule. Test: a recorded result on that package.
