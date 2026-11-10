# S5 ANALYSIS: incident I5, four final reviews of the P0 live-check plan package

Produced by `/sc:analyze` (invoked through the Skill tool at the start of this job) on 2026-11-08. Scope: static analysis of recorded evidence only; nothing was run against the incident, no reviewer or `/sc:spec-panel` was started. Target: the past incident I5 in `phase1/REPORT.md`. Focus: process and recreation quality (not code quality). Depth: deep. Format: report.

Notation. `AA` = the executor session log `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/aaee1ebf-4ec9-494f-85e0-52f3697170b5.jsonl` (5,569 lines); `agent-<id>.jsonl` = a reviewer log in its `subagents/` folder; `L<n>` = jsonl line number. Document paths `artifacts/...:n` refer to the package; the state at the start of review k is rebuilt in `inputs/` (see `inputs/SOURCES.md`). Every pointer below was checked against a file on disk. Reviewer final reports are copied to `baseline-reference/` (`R<k>-reviewer-final-report...`).

## 1. Result in one paragraph

A managed `/sc:implement` run finished tasks T1 to T5 of a plan that records three live Orca worker checks and a phase report. The protocol's archive gate then runs a fresh independent final review of the whole package. That review returned `FINAL: issues` three times, each time for one or two newly found defects in the delivered evidence text, and `FINAL: pass` the fourth time. Between reviews the executor stopped, reported to the owner, and made only the fixes or rulings the owner approved. All 23 task criteria were met in every one of the four reviews; every blocking finding was about a false sentence or a plan-rule breach, never an unmet task criterion. The loop took 4 reviews and 3 fix cycles, one more review than the cap of 3 the executor worked under (that cap comes from its output-style instructions, not from the protocol files); the owner approved the extra review explicitly.

## 2. What was reviewed and by what

| Item | Value | Evidence |
|---|---|---|
| Document under review | Task package `TASK-WF-writeTheP0LivePl-20261103-215902`: plan (151 lines), source, ledger `progress.md`, 121 files, 767,470 bytes at the start | `inputs/package-R1/`, `baseline-metrics.json` `M4_document_size` |
| Command that started it | `/sc:implement .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md`, no flags | `AA` L19 (`briefs/00a-command-L19.txt`) |
| Protocol skill | `Skill sc:implement-protocol` with the plan path | `AA` L50; text loaded at L54 (`briefs/01-skill-load-L54-sc-implement-protocol.md`) |
| Reviewer for each round | One fresh `general-purpose` subagent via the Agent tool, prompt = "Your complete instructions are in the file /tmp/ironclaude-p0live/final-prompt[-N].md. Read it in full and follow it exactly. Return the result in the format it specifies." No `model`, no `run_in_background`, no other parameter | `AA` L2001, L2157, L2342, L2499 (`briefs/R*-spawn-prompt-*.txt`). Model recorded in the reviewer logs: `claude-sonnet-5-5` (executor too) |
| State helper before each spawn | `uv run --no-project python ~/.claude/skills/sc-implement-protocol/scripts/archive_workspace.py --root "$(pwd)" --package "$(pwd)/.dev/tasks/to-do/<id>" --print-state > /tmp/ironclaude-p0live/state<N>.json` (N = 1, 3, 5, 7 for rounds 1 to 4) | `AA` L1974, L2142, L2335 (via L2320), L2487 (via L2478) |
| Archive step after the pass | same helper without a flag | `AA` L2537 |
| `/sc:spec-panel` used? | **No.** The reviewer is the managed FINAL review of `/sc:implement`. No `Skill` call to spec-panel exists in the executor session or in any of the four reviewers; the only mentions of spec-panel or the routing guide in the executor log are in the later PR work (L3015, L3172, L3482, L3556, after the loop ended at L2559) | jq scan of `AA` and the four reviewer logs |

## 3. Round by round

Times are UTC on 2026-11-04. "Blocking" counts are the reviewer's own, under the severity test in section 5.

### Round 1: spawn `AA` L2001 09:09:08, report 09:19:52, verdict **issues**, 1 blocking

- Brief: `briefs/R1-reviewer-brief-L1988-final-prompt.md` (5,635 bytes), state file `state1.json`. The result is the reviewer's final message, `agent-a0d4eb0d0b16b7e1f.jsonl` L441 (`FINAL: issues`), 67 tool calls.
- Blocking F1 (false claim): "six" raw heartbeat gaps over 5 minutes should be "seven", in `artifacts/lc2-result.md:27`, `artifacts/lc2-step5.md:22` and `:25` (all three lines exist in `inputs/package-R1/`). No criterion depends on the count. The reviewer re-derived the seven values 9.4, 5.9, 7.7, 8.2, 9.5, 14.5, 6.1 from `artifacts/lc2-session-analysis.txt`.
- Non-blocking (8): `lc1-step5.md:27` says "68 commands" but the real number is 52 Bash tool calls (68 was a line count); unsaved counts at `ac-0.6.md:13` and `lc1-step6.md:13`; a stray empty bare `python3` call by the executor at 08:27:10 judged non-blocking in this round; `p0-phase-report.md:49` "always while subagents were running" is loose; and four smaller items.
- Executor action: ledger line `FINAL: issues ...` appended (`AA` L2038, 09:20:16), `E-ARCHIVE-BLOCKED` stop, report to the owner (`AA` L2051).
- Owner reply 12:10:22 (`AA` L2058, `briefs/afterR1-owner-revise-L2058.txt`): fix the counts (six to seven in three places, 68 to 52), run a fresh final review, archive if it passes, do not commit or push.
- Fix cycle 1: four `Edit` calls (`AA` L2099, L2103, L2107, L2111); package +286 bytes.

### Round 2: spawn `AA` L2157 12:11:17, report 12:21:19, verdict **issues**, 2 blocking

- Brief: `briefs/R2-reviewer-brief-L2142-final-prompt-2.md` (6,011 bytes) = round 1 brief with `state1.json` replaced by `state3.json` plus one paragraph ("this is a new archive attempt ... do not rely on [the earlier FINAL]"). Result at `agent-ad1d95b612f2d9bd6.jsonl` L444, 62 tool calls. The count fix passed.
- Blocking F1 (false claim): `artifacts/lc3-step5.md:18` and `artifacts/lc3-session-analysis.txt:96` say the only Orca verbs were `check` and `send`; the worker's subagents also ran read-only `orca-ide` commands (`worker-list`, `skills get orchestration`, `--version`; reviewer anchor `agent-a19c787c363ddf7e6.jsonl:161,168` in the adversarial worker session). The executor's search pattern could not match `orca-ide`.
- Blocking F2 (quoted-constraint breach): the empty bare `python3` call at 08:27:10.643Z (`AA` L1325) breaks the plan Constraint "UV for every Python command" (plan line 23). Round 1 had graded the same call non-blocking; round 2 graded it blocking. Same fact, different grade: a reviewer-to-reviewer inconsistency, and text edits cannot cure it.
- Executor action: `FINAL: issues` appended (`AA` L2180), stop, report (`AA` L2193), pointing out the two-fix-cycle cap.
- Owner reply 12:28:32 (`AA` L2204): fix the check 3 sentences, disclose the call in the phase report, record the owner's acceptance in the ledger as a scoped `ARCHIVE: Ruling:`, run the third and final review.
- Fix cycle 2: five `Edit` calls (`AA` L2242, L2246, L2261, L2302, L2316) and the first ruling line (`AA` L2280, `inputs/round-deltas/ledger-ruling-1.txt`); package +2,291 bytes.

### Round 3: spawn `AA` L2342 12:29:53, report 12:44:04, verdict **issues**, 1 blocking

- Brief: `briefs/R3-reviewer-brief-L2335-final-prompt-3.md` (7,128 bytes) = base brief with `state5.json` plus a longer paragraph asking the reviewer to check that the recorded acceptance matches the real evidence and to re-check every "only", "no", "all" claim in all three `lc<N>-step5.md` files. Result at `agent-a88ad232bf783d3a3.jsonl` L606, 86 tool calls.
- Blocking F1: the first final reviewer (`agent-a0d4eb0d0b16b7e1f`) itself ran 22 read-only bare `python3` Bash commands between 09:10:02Z and 09:16:29Z (anchor `agent-a0d4eb0d0b16b7e1f.jsonl:142`). So `artifacts/p0-phase-report.md:71` ("every other Python call of the run used `uv run --no-project python -I`") and the ruling line `progress.md:15` ("every other Python call used uv run") are false, and the accepted exception is too narrow. This is the only finding caused by a previous fix: the sentence was written in fix cycle 2 (`AA` L2302); it is absent from the rebuilt R1 and R2 states. The underlying calls, though, were made by round 1's reviewer.
- Non-blocking (7), among them: `p0-phase-report.md:49` still loose; `lc3-result.md:25` calls a 5.9-minute last-heartbeat-to-`worker_done` interval a "heartbeat gap"; the reviewer confessed one empty `python3 -c 1` of its own (the executor dated it 12:35:19Z, `AA` L2415).
- Executor action: `FINAL: issues` appended (`AA` L2370), stop, report (`AA` L2378): a fourth review needs the owner's say-so because it exceeds the cap.
- Owner reply 12:45:50 (`AA` L2390): widen the acceptance to the 22 helper calls plus the one empty call, narrow `p0-phase-report.md:71` to the executor's own calls, run one more review.
- Between rounds: the executor paused at 12:46:42 (`AA` L2415) because its call-log scan found a 24th bare call, round 3's own `python3 -c 1`. Owner reply 12:55:21 (`AA` L2427): cover all three groups in one ruling and tell the next reviewer to use only `uv run`.
- Fix cycle 3: one `Edit` (`AA` L2464, the note 7 rewrite) and the second ruling line (`AA` L2478, `inputs/round-deltas/ledger-ruling-2.txt`, which replaces ruling 1); package +1,626 bytes.

### Round 4: spawn `AA` L2499 12:56:21, report 13:21:21, verdict **pass**, 0 blocking

- Brief: `briefs/R4-reviewer-brief-L2487-final-prompt-4.md` (8,373 bytes) = base brief with `state7.json`, a "HARD RULE" paragraph (the reviewer must not run bare python), the description of the 24-call exception, and a sharper rule for wording slips (false claim with a valid anchor is blocking; a stale line number or loose phrase is not). The spawn prompt (`AA` L2499, 327 bytes) repeats the uv-only rule. Result at `agent-a40f02e69785bb0f5.jsonl` L684 (`FINAL: pass`), 96 tool calls, 25 minutes.
- The reviewer confirmed exactly the 24 accepted calls and no other bare call in the executor tree; one more bare `python3 -` trio in the workflow worker's own subagent (08:15:21Z) was listed as non-blocking because it is the worker's business. 12 non-blocking items (wording looseness such as `p0-phase-report.md:49`, a time stamp "06:49" that should read 06:51:49Z, "last 3 minutes" that is 3 min 41 s).
- Executor action: `FINAL: pass ...` appended (`AA` L2528 13:21:29), archive helper run (`AA` L2537 13:21:32) which moved the package to `.dev/tasks/done/<id>/`, post-archive staging check (`AA` L2550), report (`AA` L2559). Cross-check: the same 121 files are in git commit `b5c09e90` / `f3c1ef06` (#368).

## 4. Reviewer tool and flags, round by round

| Round | Tool | Exact call | Flags / parameters |
|---|---|---|---|
| all | `/sc:implement` managed archive gate (command typed once, `AA` L19) | the executor, not the user, started each review inside the same session | command: path only, no `--resume`, no `--skip-final-review`, no `--ledger` |
| 1 | Agent tool | `{"description":"Independent final review of the package","subagent_type":"general-purpose","prompt":<167 chars>}` (`AA` L2001) | none |
| 2 | Agent tool | `{"description":"Second independent final review","subagent_type":"general-purpose","prompt":<169 chars>}` (`AA` L2157) | none |
| 3 | Agent tool | `{"description":"Third independent final review", ...}` (`AA` L2342) | none |
| 4 | Agent tool | `{"description":"Fourth independent final review","subagent_type":"general-purpose","prompt":<327 chars>}` (`AA` L2499) | none; prompt adds the uv-only rule |

The duplicate-looking lines `AA` L2006, L2161, L2351, L2503 carry the same tool-use ids as the spawn lines; each round had one spawn.

## 5. Severity rule in force

The same test every round, pasted into every brief and defined in `inputs/evidence/protocol-as-loaded/qa.md` (identical to git `80f934de`): return `issues` only for a blocking defect; a defect is blocking only if one of four checks is yes: (a) an AC's required output is absent or contradicted, (b) a delivered claim is false against live source, (c) the run wrote or deleted tracked data or mutated state outside its declared outputs, (d) a plan Constraint or explicit task instruction was violated. Minor wording, cosmetic and "consider changing" items are non-blocking and never fail a review (`qa.md` "Severity model", "FINAL derived test" lines 290 to 300; "Managed FINAL review" line 308 to 310). Origin classes (`qa.md` lines 148 to 172): a defect in text that existed in an earlier reviewed tree and was not flagged there has origin `late` and "blocks at every attempt; never capped" (line 167).

Cap in force: at most 2 fix cycles and 3 reviews, then escalate with the open blocking findings; "never run a fourth review" (output-style text, recorded in the executor's request at `AA` L2131; applied by the executor at L2193 and L2378). The owner overrode it once (`AA` L2390, L2427). The cap does not come from the protocol file; a search of `qa.md`, `managed-workspace.md` and `ledger.md` for review-count wording finds no cap for the managed FINAL, only the `E-ARCHIVE-BLOCKED` stop after every `issues` (`managed-workspace.md` line 61).

What changed between rounds is only the paragraph appended to the brief (section 3 and `baseline-metrics.json` `severity_rule_in_force_each_round`).

## 6. Why the loop did not converge faster (analyst's reading, labelled as such)

1. **A fresh reviewer re-audits everything, so old defects surface late.** The protocol requires "one fresh subagent per archive attempt (never reused)" (`qa.md` line 310). Round 2's two findings were already in the delivered text in round 1 (F1 sentence present in the rebuilt R1 state; F2 call dated 08:27:10Z, `AA` L1325) and were simply not found or not graded blocking earlier. Evidence: 0 of 2 round-2 findings were caused by fix 1. This is one of the two causes phase 1 listed for I5 ("old defects found late").
2. **The review changes the evidence it audits.** Reviews 2 to 4 audit the executor session tree, and that tree contains the earlier reviewers' own tool calls. Round 1's reviewer used bare `python3` 22 times; round 3 found it. Round 3's reviewer used `python3 -c 1` once; the executor found it before round 4. Round 4 passed after the executor told the reviewer to use only `uv run`. So the one prevented defect was prevented by a brief change, not by a document change.
3. **The same fact was graded inconsistently.** The empty `python3` call was non-blocking in round 1 (round 1 report, check 1) and blocking in round 2 (F2).
4. **Fixes were narrow by design.** The executor edited only the sentences the owner approved and wrote new disclosure text (note 7 grew from one paragraph to a three-group list). The new text made new exclusivity claims ("every other Python call ...") which the next reviewer verified against raw logs; one of them was false (round 3).
5. **Size is not the cause.** The package grew by 0.59 percent over the loop (4,551 bytes). Nothing about document size explains the extra rounds.

How it ended: a pass in round 4 because the owner's rulings made the plan rule's exception cover the real set of 24 calls, the brief forbade new ones, and no other false exclusivity claim survived the reviewer's search. The pass is not evidence that the package improved in substance: all 23 criteria and the P0 PASS verdict were unchanged since round 1.

## 7. Findings of this analysis (severity-rated)

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | **High** | PR 427 cannot affect this scenario. It changes `/sc:spec-panel`, the routing guide and two release guides; this incident's reviewer is `/sc:implement`'s final review. Expect zero delta; any measured delta is run-to-run noise. S5 is useful only as a negative control and noise-floor measurement. | `git show --name-only 95f2c6e4` lists 8 non-`.dev` files, none under `sc-implement-protocol` or `commands/implement.md`; no spec-panel call in the loop (section 2) |
| A2 | **High** | A replay on master cannot see the same material unless five reference files are overlaid. The reviewers read the old spec (7.2 step 5 before PR #368), the old `WORKER-CONTRACT.md`, `workflow.md`, `adversarial.md` and `return-contract.md`; all five differ on master at 95f2c6e4. | `inputs/SOURCES.md` table; the old step-5 sentence appears in all four reviewer logs and the new one in none |
| A3 | **High** | Master already contains the finished package at `.dev/tasks/done/<id>/` (merged by #368). A replay worktree based on master would show reviewers the answer and block the archive helper (`E-ARCHIVE-CONFLICT` when both locations exist). It must be removed from the replay worktree before the run. | `git ls-tree -r 95f2c6e4` has the package paths; `archive_workspace.py` `clear_marker`/`validate` conflict rule |
| A4 | Medium | The protocol differs between the original run and master by three commits unrelated to 427 (`4eb75698` model aliases, `055132ff` prompt blank-line drift tolerance, `e032994f` symlinked prompts folder). `qa.md` changed by 21 lines, `ledger.md` and `managed-workspace.md` by a few. A master-based treatment arm therefore differs from the baseline in more than 427. The cleaner control is the original commit with 427 applied: `git merge-tree --write-tree --merge-base=95f2c6e4^ 8db29f11 95f2c6e4` reports a clean merge (tree `7d5e67506441...`). | `git diff --stat 80f934de HEAD -- src/superclaude/skills/sc-implement-protocol`; merge-tree run |
| A5 | Medium | The non-convergence mechanism is partly stochastic and tied to the executor's session tree (which bare-python calls were made, when). A fresh reviewer may never make them, so a replay can pass in round 1 for reasons unrelated to any framework change. Two replicates will usually differ from each other. | section 6, points 2 and 3 |
| A6 | Medium | Original reviewer logs remain under `~/.claude/projects/...`. The rendered briefs point reviewers to copies, but a reviewer that lists `~/.claude/projects` (round 2 did, `agent-ad1d95b612f2d9bd6.jsonl`) can find the real verdicts. | readset scan |
| A7 | Low | Task-criteria counts disagree in the sources: reviewer 3 prose says 18, the executor's report says 22 (`AA` L2378) and 23 (`AA` L2193); the plan and every reviewer's list have 23. `baseline-metrics.json` uses the counted 23. | regex count over the four reports |
| A8 | Low | The original package digests cannot be reproduced (file modes are not in git). Not a replay blocker. | `inputs/SOURCES.md` known limit |
| A9 | Info | Recreation strengths: all four briefs and all four owner messages exist verbatim; the starting document is rebuilt from git plus the logged edits and matches Claude Code's own file-history backups byte for byte for every edited file; the evidence the reviewers audited (worker sessions, executor session as of each spawn) is copied out. | `briefs/INDEX.md`, `inputs/SOURCES.md` |

## 8. Quality metrics (baseline)

Summary of `baseline-metrics.json` (M1 to M5 as defined in `DECISIONS.md` D5):

| Round | Verdict | M2 blocking | M3 caused by previous fix | M4 delivery files (57) bytes after the round's fix | M5 reviewer tool calls / output tokens / minutes |
|---|---|---|---|---|---|
| 1 | issues | 1 | n/a (first) | 275,920 | 67 / 87,649 / 10.7 |
| 2 | issues | 2 | 0 of 2 (re-derived) | 277,419 | 62 / 78,978 / 10.0 |
| 3 | issues | 1 | 1 of 1 (re-derived, caveat in section 3) | 277,842 | 86 / 94,021 / 14.2 |
| 4 | **pass** | 0 | n/a (no findings) | 277,842 (final) | 96 / 118,523 / 25.0 |

M1 = 4 reviews to a clean pass (3 fix cycles). Start size 275,813 bytes (delivery files) / 767,470 bytes (whole package); growth over the loop 0.736 percent / 0.593 percent. Reviewer effort in total: 311 tool calls, 379,171 output tokens, 59.9 minutes of reviewer time; the executor made 42 tool calls in the same windows. Which numbers are read from the evidence and which are re-derived is stated per number in `baseline-metrics.json`.

Consequences for the significance bar in `DECISIONS.md` D6: the baseline's last round has zero blocking findings, so criterion (a) can only be met by a clean pass in 3 reviews or fewer; criterion (b) needs growth of at most 0.52 percent (delivery files) which is dominated by the owner's ruling and disclosure text.

## 9. Recommendations

1. Run S5 as a negative control, not as a test of 427: the recreation is sound (grade B) but 427 has no path to this reviewer. If the coordinator wants evidence about 427 itself, spend the replicate budget on the spec-panel scenario (S1) and treat S5's spread as the noise floor.
2. If S5 is replayed, use the setup in `REPLAY.md` exactly: remove the leaked finished package, overlay the five old reference files, render the briefs with `inputs/tools/render_briefs.py`, and drive the loop with the verbatim owner messages. Prefer the "original commit plus 427" arm to the master arm so that nothing but 427 differs.
3. Record the stop reason of each replicate: a pass in round 1 with no blocking findings and an unchanged document means the reviewer simply did not find the latent defects; it must not be scored as an improvement.
