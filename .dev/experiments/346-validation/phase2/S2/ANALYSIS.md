# S2 ANALYSIS: incident I2, review-severity-rule plan (run through /sc:analyze)

Produced by the `/sc:analyze` skill, invoked top-level through the Skill tool, on the brief: "Review the past incident I2 (evidence listed in phase1/REPORT.md) and recreate the scenario as exactly as possible, with the original run as the baseline." Analysis and packaging only; nothing was run against the incident.

Naming note (needs a coordinator look): DECISIONS.md D2 lists "S2 issue-394 launch-level hook plan" and "S3 review-severity-rule plan", but the task text, the folder name `phase2/S2/` and phase-1 REPORT.md define S2 = I2 = the review-severity-rule plan. The issue-394 plan is I3 in the logs report. This package follows the task text (I2).

## 0. Path prefixes and conventions

- `RS` = `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude--dev-worktrees-review-severity-rule`.
- `MAIN` = `RS/d6112a25-4a8a-4e17-927c-5d7b39e2f6af.jsonl` (8,329 lines, the worker session that ran the loop). `S1` = `RS/5341a799-b69c-4a19-86b3-9f7c63853f28.jsonl` (2,308 lines, the earlier stalled worker). `SUB:<id>` = `RS/d6112a25-4a8a-4e17-927c-5d7b39e2f6af/subagents/agent-<id>*.jsonl`. Line numbers are 1-based jsonl lines.
- `P` = this folder (`.dev/experiments/346-validation/phase2/S2/`). `R1/R2/R3-REPORT` = `P/baseline-outputs/R{1,2,3}-REPORT.md`, rebuilt from the Write (and Edit) calls at MAIN L1572+L1639+L1644, L2235, L3149+L3311+L3316+L3321.
- "Verified" means I read the line or compared bytes myself in this analysis. Statements without that are marked UNVERIFIED.

## 1. What the incident is

A worker (model `claude-opus-5-5`, Orca task `task_2f56bc9b8728`, branch `fix/review-severity-rule`) was told to remove the review rule "any issue of any severity fails" and cap review loops at 2 fix cycles (3 reviews), starting with a written plan: `/sc:workflow "<prompt>" --depth standard --handoff none` (MAIN L308 and L324, args in `P/briefs/00-sc-workflow-invocation-args__L308.txt`, 4,569 chars). The task brief is MAIN L10 (`P/briefs/00-orca-dispatch-brief__L10.txt`): "Read /tmp/t11b-severity-rule-restart-spec.md in full and carry it out". The plan was pre-reviewed with `/sc:reflect` pre mode (UC-1) three times. Every review returned FAIL with new blocking findings (11, 7, 10), the cap was reached, and the worker escalated to the coordinator instead of passing the plan (MAIN L3368).

The document under review is a plan (a tasklist of 14 tasks at the start), not a spec. The reviewer is `/sc:reflect`, not `/sc:spec-panel` (section 3 and REPLAY.md say what this means for PR 427).

## 2. Round by round

Timeline (UTC, from the line timestamps in MAIN): plan v0/v1 generated 2026-11-01 22:53-22:58; API connection loss 22:59:18 (MAIN L620); restart message 2026-11-02 03:07:52 (MAIN L626, `P/briefs/00-restart-message__L626.txt`: "Your last turn died on an API connection error at 22:59 during the pre-review of package TASK-WF-removeTheAnyIssu-20261101-225635. Continue the task from there per /tmp/t11b-severity-rule-restart-spec.md."). The worker session continued with its context.

### Round 0 (outside the counted loop)

The earlier worker (S1) had pre-reviewed a superseded package `TASK-WF-removeTheAnyIssu-20261031-235404`: Tier 1, status partial (input drift), 4 blocking findings C1-C4 and 3 minor (`P/inputs/common/prior-pre-review-REPORT-20261031235716.md` lines 3, 13-26). The restart spec told the new worker to fold those in (`P/inputs/common/t11b-severity-rule-restart-spec.md` line 8). It is not counted in M1 and the document differs. I note it because the real count of review rounds behind this plan is 4, not 3.

### Plan generation (starting document)

- First generation: package `...20261101-225338`, 14 tasks, 23,435 bytes (Write MAIN L390; `P/inputs/round1/reference/`). A review was started on it with `Skill sc-reflect-protocol` args `--mode pre --spec <pkg>/source.md --tasklist <pkg>/<plan>.md` (MAIN L460, `P/briefs/R1-reflect-skill-invocation-args__L460.txt`).
- The worker then regenerated the package "with parseable requirement ids (Wave 0 again)" (MAIN L526): package `...20261101-225635`, source Write MAIN L540 (4,645 bytes, requirements R-001..R-010), plan Write MAIN L554. This is plan v1, the STARTING DOCUMENT: 23,890 bytes, 202 lines, 14 tasks (measured; byte-equal to the full Read by reviewer `SUB:a11975dd` L26, verified with `cmp`).
- The review run folder `.dev/reflect/pre-removeTheAnyIssu-20261101225845` was set up for 225635 at MAIN L606 and did not need a new Skill call after the restart.

### Round 1: review 1 of plan v1 (MAIN L626-L1675)

| Step | Pointer |
|---|---|
| Tool and flags | `Skill sc-reflect-protocol`, args `--mode pre --spec <pkg>/source.md --tasklist <pkg>/TASK-WF-removeTheAnyIssu-20261101-225635.md` (no `--tier`, `--depth`, `--reviewers`; auto tier). The loaded skill text (MAIN L465) equals `git show f90877be:src/superclaude/skills/sc-reflect-protocol/SKILL.md` except its 7-line front matter (diff checked: 12 diff lines, all front matter). |
| Coverage matrix | agent `requirements-analyst`, MAIN L652 (`P/briefs/R1-coverage-matrix-requirements-analyst__L652.md`): 10/10 parsed requirements covered |
| Tier 1 card and calibration | card Write MAIN L761 (4 blocking, 1 minor); blind calibrator MAIN L775, result 0.67; Tier 2 chosen by rule 4 (R1-REPORT line 22) |
| Tier 2 reviewers | `reflect-reviewer` agents MAIN L894 (sonnet, analyzer), L898 (haiku alias = glm-5.3, qa), L902 (opus, refactorer), spawned 03:14:35-39. Each spawn prompt is 334 chars and points to a brief file written at MAIN L870, L875, L880. |
| Reviewer cards | MAIN L941 (reviewer 3: 3 blocking, 2 minor), L969 (reviewer 1: 5 and 5), L994 (reviewer 2: 3 and 6) |
| Calibration | `confidence-calibrator` x3, MAIN L1008-L1016; mean 0.80 (R1-REPORT line 8) |
| Adversarial merge | `Skill sc-adversarial-protocol` MAIN L1099; advocates L1145/L1149/L1153; rebuttals L1279/L1306/L1339; invariant probe L1380; `merge-executor` L1482; 26/26 diff points 3-0, convergence BLOCKED_BY_INVARIANTS (R1-REPORT line 23) |
| Report | Write MAIN L1572 (`.dev/reflect/pre-removeTheAnyIssu-20261101225845/REPORT.md`); `evidence-validator` MAIN L1577: 50 citations, 0 dropped |
| Result | FAIL, 11 blocking (B-01..B-11), 17 minor (M-01..M-17) (R1-REPORT lines 24, 28-38, 42) |

Reviewer lens in this round (brief L870, line 5): "correctness of the plan's instructions ... Grade each finding blocking ... or minor". Verified in `P/briefs/R1-reviewer-1-analyzer-brieffile__L870.md`.

### Fix cycle 1 (MAIN L1686-L1909): plan v1 -> plan v3

The reviser is the worker session itself, not a separate agent. It scanned the repo for every cap wording (Bash MAIN L1687, L1701), had one helper agent classify 160 hits into in-scope and out-of-scope (MAIN L1709, brief `P/briefs/FC1-cap-site-classifier__L1709.md`), wrote `cap-sites.md`, then wrote the new source (MAIN L1792, `P/inputs/round2/source.md`) and plan (MAIN L1806). Plan v3: package `...20261102-042031`, 31,868 bytes, 264 lines, 19 tasks (+33.4 percent bytes). There is no single "revise brief"; the effective revise instruction is the new `source.md` plus the R1 report recommendation R-001 (R1-REPORT lines 54-58: "Regenerate the plan with the 11 blocking fixes ... fold B-01..B-11 into the tasks named in each fix").

### Round 2: review 2 of plan v3 (MAIN L1910-L2273)

| Step | Pointer |
|---|---|
| Tool and flags | same protocol, same flags, "protocol re-executed from the sc-reflect-protocol text loaded earlier this session" (audit.log note inside the Bash at MAIN L1910); no new Skill call. Run folder `pre-removeTheAnyIssu-20261102042426`. |
| Coverage, Tier 1 | coverage agent MAIN L1920 (brief checks "each R-id and each B-01..B-11"); Tier 1 card MAIN L1989 (1 blocking: lite at-cap "Open Questions" sentences), calibrated 0.81 (MAIN L1994) |
| Tier 2 reviewers | MAIN L2093 (sonnet), L2097 (haiku alias), L2101 (opus), 04:35:55-58; briefs written at MAIN L2069, L2074, L2079. The briefs add: "Already found (do not re-report; extend or dispute only): see Grounding hunks" (verified, brief L2069 line 6). Lens: CAP tasks 12-16 and pinned-line tasks. |
| Cards | MAIN L2137 (2 blocking, 6 minor), L2165 (2 and 7), L2212 (1 and 1, written by a Bash heredoc) |
| Mid-loop external input | The worker asked the coordinator how many cli-portify iterations equal the cap (`orca orchestration ask`, MAIN L2175) and got "1 iteration" (answer in the result, MAIN L2181; `P/briefs/R2-coordinator-ask-cli-portify-*`). It recorded the answer in `inventory.md` (MAIN L2187). |
| Stop | Because the input tree changed, the run stopped as `status: partial` at the pre-synthesis guard (R2-REPORT lines 5, 22; MAIN L2235, L2240, L2273). Calibration, adversarial merge and evidence validation did not run. |
| Result | status partial, plan FAIL, 7 blocking (P2-B1..P2-B7), minor items not counted (R2-REPORT lines 26-36) |

Round 2 is not like-for-like with rounds 1 and 3 (no merge). Its 7 comes from the Tier 1 card, the coverage matrix and 3 uncalibrated reviewer cards.

### Fix cycle 2, the last (MAIN L2254-L2505): plan v3 -> plan v4

The worker had a helper agent turn the cap list into a literal old/new edit table (MAIN L2255, brief `P/briefs/FC2-literal-cap-edit-table__L2255.md`, output `P/inputs/round3/cap-edits.yaml`, 1,399 lines), wrote the new source (MAIN L2450) and plan (MAIN L2464). Plan v4: package `...20261102-053741`, 32,107 bytes, 275 lines, 20 tasks (+34.4 percent bytes over v1, +0.75 percent over v3; byte-equal to the Read by `SUB:a9d60b6d` L26).

### Round 3: review 3 of plan v4, the last allowed (MAIN L2506-L3399)

| Step | Pointer |
|---|---|
| Tool and flags | same as round 2. Run folder `pre-removeTheAnyIssu-20261102054021` (setup Bash MAIN L2506). |
| Coverage, Tier 1 | coverage agent MAIN L2515 (15/15 requirements mapped); Tier 1 card MAIN L2550, calibrated 0.75 (R3-REPORT line 8) |
| Reviewers | briefs generated by the Bash loop at MAIN L2615 (text recovered from the reviewers' own Reads: `SUB:a9d60b6d` L16, `SUB:a2cab2cb` L24, `SUB:a56faadb` L16); spawns MAIN L2628 (sonnet), L2632 (haiku alias), L2636 (opus), 05:54:57-05:55:01. Lens in brief 1: "correctness of Tasks 1-11 (severity edits) and Task 6". |
| Cards, calibration, merge | cards MAIN L2670, L2718, L2763; calibrators L2777-L2785 (0.79, 0.77, 0.84); advocates L2903-L2911; probe L3011; `merge-executor` L3083; report Write MAIN L3149; `evidence-validator` L3154: 64 citations, 0 dropped |
| Result | FAIL, 10 blocking (B3-01..B3-10), 12 minor (M3-01..M3-12), status partial because the merge was BLOCKED_BY_INVARIANTS (R3-REPORT lines 5, 23-24, 28-37, 41) |
| End | "Three reviews and two fix cycles are spent. Escalate B3-01..B3-10" (R3-REPORT lines 54-56). Escalation sent at MAIN L3368 (`P/briefs/R3-escalation-body__Write-L3358.txt`). |

### After the loop (not part of the metrics)

The coordinator replied with the owner's decision at MAIN L4141 (`P/briefs/POST-coordinator-decision-msg_9d0fe67f82c7__L4141.json`): add all 10 findings to the plan and implement, no fourth plan review, plus a recorded site-sweep and a static test. The plan grew to 21 tasks, 38,073 bytes, 291 lines (replay of the 18 Write/Edit calls on the plan file, all applied; `P/baseline-outputs/post-loop-final-plan-21-tasks.md`; MAIN L6760 says "all 21 tasks"). The fix landed as commit 80f934de (#343) on 2026-11-02 and is a parent of the PR 427 commit (`git merge-base --is-ancestor 80f934de 95f2c6e4` is true).

## 3. Which reviewer, tool and flags each round used

| Round | Review command | Reviewer personas / models | Notes |
|---|---|---|---|
| 1 | `sc-reflect-protocol --mode pre --spec .../source.md --tasklist .../TASK-...-225635.md` | analyzer/sonnet (`claude-sonnet-5-5`), qa/haiku alias (`glm-5.3`), refactorer/opus (`claude-opus-5-5`); calibrators opus | aliases from the audit.log line in MAIN L1910 and R1-REPORT line 22 |
| 2 | same, re-run inline | same | stopped early (input drift) |
| 3 | same, re-run inline | same | merge BLOCKED_BY_INVARIANTS |

`/sc:spec-panel` was never used in this incident: the main log's Skill calls are exactly `sc:workflow`, `sc-workflow-protocol`, `sc-reflect-protocol`, `sc-adversarial-protocol` (all in the loop) and, after the loop, `sc:implement`, `sc-implement-protocol`, `sc-troubleshoot-protocol`, `sc:pr-submit`, `sc-pr-submit-protocol` (counted with `jq`); no tool call in the main log mentions "spec-panel" (`jq` test over all tool_use inputs). `git grep -i spec-panel` over the reflect, workflow and adversarial skills and commands finds one hit at both f90877be and 95f2c6e4: a table row in `src/superclaude/commands/adversarial.md:180` ("/sc:spec-panel | Augment panel with adversarial review"), a documentation row that 427 did not change. PR 427 changed `src/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md` and its plugin mirror, `plugins/superclaude/commands/spec-panel.md`, two release guides, one design doc and one test (`git show --name-only 95f2c6e4`). None of these is read by `/sc:reflect`, `/sc:workflow` or `/sc:adversarial`. The reviewers could not have been affected by 427 text; the only path for an effect is indirect (HOW-WE-WORK.md routing advice the worker might read), and the logs show no read of it in this loop (not exhaustively searched; UNVERIFIED).

## 4. Which severity rule was in force each round

- The rule the loop applied, every round: findings are graded blocking or minor; only blocking findings fail; minor findings are notes and are not fixed in extra rounds; at most 2 fix cycles (3 reviews), then escalate with the open blocking findings. Evidence: restart spec lines 15-16 and 26 (`P/inputs/common/t11b-severity-rule-restart-spec.md`: "Apply the new rule to your own run: minor findings from your plan's reviewers are noted, not fixed in extra rounds"), original spec lines 16-19 and 28, plan v1 Constraints line 16 of `P/inputs/round1/source.md`, each reviewer brief ("Grade each finding blocking (...) or minor"), R1-REPORT lines 40, 58 and MAIN L1909 ("review 2 of at most 3").
- The same rule in all three rounds; what changed is the cap counter (R1 "fix cycle 1", R2 "review 2 of at most 3", R3 "review 3 of 3 (final)", R3-REPORT line 24).
- The repo text at f90877be still carried the OLD rule (`git grep` finds 14 "of any severity" hits in src/plugins/commands/agents at f90877be and 0 at 95f2c6e4; `pragmatic.md:225` is the old bullet). That is what the plan edits, not the rule that governed the loop. Whether the worker's own session had the old rule active through its installed output style is UNVERIFIED (the system prompt is not in the log).

## 5. How the loop ended and why

It ended by the cap, not by convergence: three FAIL verdicts, escalate (R3-REPORT line 56: "Each review found real misses outside the site lists (review 1: 11, review 2: 7, review 3: 10)"). Reading the evidence, the causes are:

1. A "list every site" plan whose site lists were built with grep patterns. Each round's reviewers found sites the pattern could not match (P2-B3: 11 lines CAP_PATTERN cannot detect; B3-01..B3-04, B3-07, B3-08, B3-10: further existing wordings). New blocking findings are mostly existing repo sites missed by both the plan and the previous reviewers, not defects the previous fix wrote. My count (basis: reading the reports, see baseline-metrics.json): 4 of 7 in round 2 and 2 of 10 in round 3 trace to the previous fix.
2. A rotating reviewer lens. Round 1 brief: correctness of instructions; round 2: cap tasks and pinned-line tasks; round 3: Tasks 1-11 and Task 6 (briefs, line "Lens:"). A different lens finds different defects, so "no new blocking finding" was never reachable by repetition. Rounds 2 and 3 did pass the earlier finding ids to the coverage agent (round 2 brief line 11) and told reviewers not to re-report, which is a weak form of a re-review contract; there was no diff-only restriction ("only lines changed since the last round").
3. The reviser rewrote the whole plan twice (document +33.4 percent in cycle 1), which gave the next round new text to attack.
4. A mid-loop input change (the cli-portify decision) stopped round 2 half way, so round 2 had no merge and its numbers are thinner.

## 6. Findings of this analysis (severity-rated, per /sc:analyze)

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | High (for the experiment) | The reviewer in I2 is `/sc:reflect`, so PR 427 cannot change this loop directly. Expect about zero delta; use I2 as a control for 427's reach, not as a test of it. | section 3 |
| F2 | High | Re-running on master at or after 95f2c6e4 (DECISIONS D4 as written) invalidates the scenario: PR #343, the fix this plan describes, is already in that tree (14 hits of the old wording at f90877be, 0 at 95f2c6e4), so the plan's acceptance checks and site lists describe edits that are already made, and the active rules now say "minor findings never fail". The scenario needs base f90877be, with 427 added by cherry-pick (`git merge-tree --write-tree --merge-base=95f2c6e4^ f90877be 95f2c6e4` exits 0, i.e. a clean merge). | `git grep` counts; REPLAY.md step 2 |
| F3 | Medium | The reviser step is not a briefed agent; it is the worker's own regeneration. The recorded plans v3 and v4 and their sources are verbatim, so a reviewer-only replay is exact; a live reviser is a reconstruction. | section 2 FC1/FC2 |
| F4 | Medium | One external decision was injected mid-loop (cli-portify = 1 iteration, MAIN L2181); a replay must either inject the same answer or use the round-2 inventory snapshot, which already contains it. | section 2 round 2 |
| F5 | Medium | Round 2's inventory changed during the review and halted it; replay with the fixed snapshots avoids repeating that stop. | R2-REPORT line 22 |
| F6 | Low | Phase-1 left "v1 tasks UNVERIFIED"; now measured: 14 tasks (plan v1), 19 (v3), 20 (v4), 21 post-loop. | baseline-metrics.json |
| F7 | Low | The model alias `haiku` resolved to `glm-5.3`, a non-Anthropic model; a replay in another environment may resolve it differently, which changes reviewer diversity. | MAIN L1910 audit note |

Recommendations are in REPLAY.md (runbook, recreation grade). Baseline numbers are in `baseline-metrics.json`, each tagged read-from-evidence (E), derived (D) or re-derived by reading (R).

## 7. Self-audit (what was checked, what was not)

Checked: jsonl pointers for all spawns and Writes (listed by script and read back); bytes of plan v1, v3, v4 and source.md against the reviewers' own Reads (`cmp`); that reviewer brief files equal what reviewers Read (R1 and R2, reviewer 1); that the reflect skill text equals the repo at f90877be; that 427 does not touch reflect/workflow/adversarial files; the sizes in baseline-metrics.json (recomputed with `wc`).

Not checked or weak: the inventory.md reconstruction by replaying Write/Edit calls failed on 4 edits, so I used the reviewers' full Read results instead (exact for what they saw); `cap-sites.md` in round 3 is assumed equal to round 2 (no recorded change); the installed `~/.claude` framework files of the original session were not recoverable except the reflect skill text; M3 origin attribution for rounds 2 and 3 is my reading, not the reviewers' tag; I did not read the full text of every reviewer return, only the reports and cards; the other 164 of the 202 subagent logs (outside the 38 loop-related ones: 17 + 1 + 5 + 1 + 14 by round, per baseline-metrics.json) were not opened (post-loop implement work).
