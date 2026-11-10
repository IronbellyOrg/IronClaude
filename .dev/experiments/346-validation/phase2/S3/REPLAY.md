# S3 REPLAY runbook: launch-level hook refactoring plan (incident I3, issue 394)

Package root (all relative paths below): `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S3/`. Companion files: `ANALYSIS.md` (what happened, with evidence), `baseline-metrics.json` (the original run's M1 to M5), `inputs/` (+ `MANIFEST.sha256`, `SOURCES.md`), `briefs/` (verbatim briefs), `baseline/` (the ORIGINAL run's outputs: never show them to a re-run agent), `tools/` (helper scripts).

Nothing in this package has run the scenario. This file tells a fresh session how to do it.

## 0. Read this first

1. **Can PR 427 affect this scenario? No, not as the original ran it.** The reviewer in every round was a plain `Agent` call (`subagent_type: general-purpose`, `model: sonnet` or `opus`) with a free-text brief, not `/sc:spec-panel`. PR 427 (`95f2c6e4`) changed `/sc:spec-panel`, one routing-guide sentence, two release-guide lines, a design doc and a test. None of those files is read by any agent in this loop (ANALYSIS.md section 5). The expected delta is zero. S3 is a **negative control**: its spread between replicates is the noise floor for D6(c). It cannot count toward "427 proven" unless the optional spec-panel arm (section 9) is run and labelled.
2. **Label conflict to settle.** `DECISIONS.md` D2 calls "S2" the issue-394 hook plan and "S3" the review-severity-rule plan, but in the logs report that numbering is reversed (I2 = review-severity-rule plan, I3 = hook plan). This package follows the task text ("S3 = I3") and covers the **hook plan**. Check that no other analyst packaged the same incident, and that the review-severity-rule plan (logs I2, reviewed with `/sc:reflect`) is covered by someone (ANALYSIS.md section 6.3).
3. **Two modes.** Mode H (round by round) uses only verbatim briefs and the original document of each round: exact, but not a loop. Mode L (chained loop) is the only one that measures M1 and growth over a loop (D6a, D6b); it needs three reconstructed briefs, all labelled. Use Mode L for the D6 comparison and Mode H as a per-round cross-check.
4. The result will probably be "not significant". The baseline last round has 10 blocking findings and the plan grew 66.9 percent in bytes; any re-run with the same briefs will probably also fail round 3 (ANALYSIS.md 3.3).

## 1. Baseline in one table (full detail: `baseline-metrics.json`)

| Round | Reviewed version | Verdict | Blocking / minor | Plan before the fix (bytes, lines) | After the fix | Review: tool calls, output tokens | Fix: tool calls, output tokens |
|---|---|---|---|---|---|---|---|
| 1 | v0 | FAIL | 8 / 14 | 136,216 / 1,053 | 174,471 / 1,138 (+28.1 %) | 27, 116,316 | 114, 130,891 |
| 2 | v1 | FAIL | 8 / 12 | 174,471 / 1,138 | 227,399 / 1,313 (+30.3 %) | 39, 113,287 | 177, 194,173 |
| 3 | v2 | FAIL | 10 / 11 | 227,399 / 1,313 | none (cap reached) | 47, 142,080 | none |

M1 = no clean pass in 3 reviews. Loop growth +66.9 % bytes, +24.7 % lines. Loop cost (reviews and fixes, not the draft): 404 tool calls, 696,747 output tokens, 127 minutes of wall time. The draft step before it: 33 minutes, 49 tool calls, 186,979 output tokens.

## 2. Commits and environment

| Item | Original run | Re-run |
|---|---|---|
| Repo commit | **8b4858f7** (master, 2026-11-05T10:24:11-06:00, "docs(onboarding): add the onboarding deck ..."). Evidence: Orca reflog of branch `ironbelly/hook-launch-level-394`: "Created from refs/remotes/origin/master" at 2026-11-05 17:01:24Z; the first commit 9aa7b4f9 (22:28:14Z, after the loop) has parent 8b4858f7; the session started 17:02Z (`H4.jsonl` L12). The worktree was clean apart from new brainstorm files during the loop. | **`95f2c6e4`** (the PR 427 squash) is the recommended base: it is "master at or after 95f2c6e4" with the least drift. `origin/master` today is 6782eee1 (8 commits later, one of which, 3b344dd4, is the finished hook; do not use it). `git merge-base --is-ancestor 8b4858f7 95f2c6e4` is true, 20 commits apart. |
| Last master commit without 427 | `ec1babd9` (per DECISIONS D3) | not used |
| Installed `~/.claude` | skills equal the 8b4858f7 tree (verified for `sc-pr-submit-protocol`, `sc-implement-protocol`, `sc-adversarial-protocol` refs, `WORKER-CONTRACT.md`); `commands/sc/spec-panel.md` is the pre-427 text (sha256 prefix e7b1a2c66f96be1f) | unchanged on this host; do not run `superclaude install` (rule: never edit `~/.claude`) |
| Claude Code | 2.1.318 | 2.1.319 on this host at packaging time (record yours with `claude --version`) |
| Orchestrator model | `claude-sonnet-5-5` (during the loop) | record yours |
| Agent models | `opus` = claude-opus-5-5 (draft, both fixes, review 3); `sonnet` = claude-sonnet-5-5 (reviews 1 and 2) | pass the same `model` strings |
| Host tools | bash 5.2, GNU sed 4.9, GNU tr 9.7, jq 1.7, git 2.47.3 (from the review headers) | identical today: bash 5.2.37, sed 4.9, tr 9.7, jq-1.7, git 2.47.3; `/tmp` must be writable (reviewers build throwaway repos there) |

### Drift between 8b4858f7 and 95f2c6e4 that touches files the agents read (not caused by PR 427)

`src/superclaude/hooks/hooks.json` (+ plugin copy), `src/superclaude/cli/install_hooks.py`, `tests/cli/test_install_hooks.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/skills/sc-pr-submit-protocol/` (SKILL.md, ci-poll.md, conflict-mechanical.md, state-machine.md, poll-ci-checks.sh), `src/superclaude/skills/sc-implement-protocol/` (ledger.md, managed-workspace.md, qa.md, archive_workspace.py), plus new files (`launch-job-identity.sh`, its test). `tools/prepare_replay_worktree.sh` restores these paths to 8b4858f7 in the replay worktree only, and removes the new hook files. PR 427's files are not touched by it.

## 3. Set up a replay worktree (once per replicate)

All steps use only the experiment worktree; nothing is committed, pushed or posted.

```bash
PKG=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S3
# 1. A fresh worktree through Orca (project rule; no raw `git worktree add`, no --issue/--pr flags).
orca worktree create --name s3-rerun-a --base-branch 95f2c6e4      # then the second replicate: s3-rerun-b
WT=<path printed by `orca worktree list` for s3-rerun-a>
git -C "$WT" merge-base --is-ancestor 95f2c6e4 HEAD && echo "427 present"
# 2. Remove everything that would show the answer and restore the files the agents fact-check (dry run first).
bash $PKG/tools/prepare_replay_worktree.sh "$WT"            # prints what it would do
bash $PKG/tools/prepare_replay_worktree.sh "$WT" --apply
# 3. Project copy of the commands and skills (DECISIONS D4).
(cd "$WT" && make sync-dev)
# 4. Integrity checks.
(cd $PKG/inputs && sha256sum -c MANIFEST.sha256)                 # every line must say OK
cmp /home/coder/workspaces/IronClaude/.dev/issues/394/issue-body.md $PKG/inputs/issues/394/issue-body.md && echo "issue body unchanged"
rg -c '^## Review Loop' "$WT/.claude/commands/sc/spec-panel.md"    # 1 = the 427 text is in the project copy
rg -c '^## Review Loop' ~/.claude/commands/sc/spec-panel.md        # prints nothing (exit 1) = the installed copy is still pre-427 (expected; only matters for section 9)
# 5. Render the briefs for this worktree (the ONLY change is the worktree path inside each brief; a round-trip check runs).
bash $PKG/tools/render_briefs.sh $PKG "$WT" "$WT/.dev/replay/s3/briefs"
```

Do not commit the worktree. If the leakage check printed by the `--apply` step still lists files, remove them or write down why they stay before running anything. Tested on a throwaway local clone at 95f2c6e4 (2026-11-08): after `--apply` the check listed only `.dev/tasks/archive/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/research/03-wrapper-cli-plumbing.md`, an unrelated June file (a test note about "a launch-level assertion" in a CLI mock); it may stay. Two more files may stay because they existed before the original run started: `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-prompt.md` (the owner's brief) and `.../launch-levels-addendum.md` (the feature requirements the brief tells the session to read). The package itself lives in the untracked `.dev/experiments/` of the `exp346-p1-logs` worktree; keep that folder until the experiment ends, the replay worktree does not contain it.

### Leakage and drift

The answer is on disk in this repository: the finished plan and its three reviews, the merged spec `docs/designs/sc-issue-launch-level-hook.md`, the hook script and its tests, `.dev/codegraph-migration/evidence/P2-hook-session.md`, the original run's own result file, and three `.dev/tasks` packages that cite the design. The prepare script removes them from the replay worktree. It cannot stop an agent from searching elsewhere on this host (the surviving brainstorm folder `/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/`, and the original session logs under `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-hook-launch-level-394/`). After each replicate run the validity check in section 7; a replicate that touched those paths is void.

## 4. How the writer and reviser steps are done

- **Writer (draft).** Not re-run. The starting document is `inputs/brainstorm/adversarial/adversarial/refactor-plan.md` (v0, 136,216 bytes, 1,053 lines, sha256 c130ba4d...). It was produced by the brief `briefs/R0-writer-draft-plan-L895.md` (`Agent`, general-purpose, `opus`, description "Step 4 draft refactor plan") from the 18 pipeline files in the same folder. A re-draft (Mode D, optional, to measure draft variance only) would send that brief, rendered, to a fresh `opus` agent after staging `CHAIN`; its output is a different v0 and is not comparable to the baseline's round 1.
- **Reviser.** One `Agent` call per fix cycle (general-purpose, `opus`), brief = the reviser brief, the agent edits `refactor-plan.md` in place and appends a "Revision log". The original reviser briefs contain the orchestrator's finding-specific steering and cannot be reused verbatim when the findings differ (ANALYSIS.md A2). Mode H uses them verbatim with the original review as input; Mode L uses the neutral reconstruction.
- **Reviewer.** One `Agent` call per review, brief verbatim (Mode H) or generalised (Mode L). The reviewer writes only its review file and may build scratch repositories in `/tmp`.
- **Orchestrator (you).** Send the briefs unchanged. Do not read a review and add advice to the next brief. Do not run the merge step, `/sc:design`, any `/sc:*` command, or a fourth review. Write down every deviation.

## 5. The exact review command, flags and brief per round

There is no CLI command or flag. Each step is one `Agent` tool call with these four parameters; `prompt` is the file content, unchanged apart from the rendered worktree path. The harness runs them as background agents.

| Step | `description` | `subagent_type` | `model` | `prompt` (Mode H, verbatim) | `prompt` (Mode L, chained) |
|---|---|---|---|---|---|
| Review 1 | Step 4 review of refactor plan | general-purpose | sonnet | `briefs/R1-reviewer-L919.md` | same file (verbatim: nothing in it depends on earlier output) |
| Fix cycle 1 | Fix cycle 1 revise refactor plan | general-purpose | opus | `briefs/R1-reviser-fix-cycle-1-L947.md` | `briefs/RECONSTRUCTED-R1-reviser-fix-cycle-1-neutral.md` |
| Review 2 | Plan re-review round 2 | general-purpose | sonnet | `briefs/R2-reviewer-L975.md` | `briefs/RECONSTRUCTED-R2-reviewer-generic.md` |
| Fix cycle 2 | Fix cycle 2 revise refactor plan | general-purpose | opus | `briefs/R2-reviser-fix-cycle-2-L1000.md` | `briefs/RECONSTRUCTED-R2-reviser-fix-cycle-2-neutral.md` |
| Review 3 | Plan final review round 3 | general-purpose | opus | `briefs/R3-reviewer-L1032.md` | `briefs/RECONSTRUCTED-R3-reviewer-generic.md` |

The file name of every verbatim brief carries the `H4.jsonl` line it was copied from; `briefs/*.meta.json` holds the tool-use id, time, model and the agent log it started. `briefs/R*-orchestrator-note-*.md` are the orchestrator's own messages between rounds (not briefs); they show the steering style and are not to be sent.

**Which severity rule is in force in each round:** one family, binary PASS/FAIL, blocking vs minor, 2 fix cycles (3 reviews) then stop. The wording of "blocking" is in the brief of each review and widens from round to round; do not edit it (ANALYSIS.md sections 3.3 and 4).

### Mode L, step by step (chained loop; use two replicates)

```bash
bash $PKG/tools/stage_step.sh $PKG "$WT" CHAIN        # folder = 18 pipeline files + v0 as refactor-plan.md
git -C "$WT" status --short | rg -v '^\?\? \.dev/replay/' > "$WT/.dev/replay/s3/status-before.txt"   # for the validity check in section 7
```
1. Review 1 (verbatim brief). Snapshot `refactor-plan.md` and `plan-review.md` into `$WT/.dev/replay/s3/<run>/round1/`. Measure (section 6). If the verdict is PASS: stop; M1 = 1.
2. Fix cycle 1 (neutral brief). Snapshot the plan as `round1/after-fix.md`.
3. Review 2 (generic brief). Snapshot; measure; if PASS stop (M1 = 2).
4. Fix cycle 2 (neutral brief). Snapshot.
5. Review 3 (generic brief). Snapshot; measure. **Stop whatever the verdict** (cap). Record the open blocking findings. Do not start the merge step.

### Mode H, step by step (one round at a time, original documents)

For each step: run `stage_step.sh $PKG "$WT" <step>`, send the brief with the verbatim file, snapshot the folder, then restage for the next step. The steps are independent of each other; the original documents of the earlier rounds come from `baseline/`.

| Step | Stage | Brief (verbatim) | Compare with |
|---|---|---|---|
| H1 review of v0 | `H1` | R1-reviewer-L919 | 8 blocking, 14 minor |
| H2 fix 1 | `H2` (v0 + original `plan-review.md`) | R1-reviser-fix-cycle-1-L947 | 174,471 B / 1,138 lines |
| H3 review of v1 | `H3` | R2-reviewer-L975 | 8 blocking, 12 minor |
| H4 fix 2 | `H4` (v1 + both original reviews) | R2-reviser-fix-cycle-2-L1000 | 227,399 B / 1,313 lines |
| H5 review of v2 | `H5` | R3-reviewer-L1032 | 10 blocking, 11 minor |

## 6. What to record per round (metrics M1 to M5 of DECISIONS D5)

Per review, run (from the package root, with `<plan>` the plan the reviewer saw and `<review>` its report):

```bash
uv run python -I $PKG/tools/measure_round.py <plan> <review>    # verdict, blocking, minor, plan bytes and lines (M2, M4)
```
If a re-run review does not use the "Blocking findings: N" header lines, `measure_round.py` prints `null`; count the findings by hand and write "hand-counted".

| Metric | How to get it | Mark as |
|---|---|---|
| M1 rounds until a clean pass or the stop | the first review whose verdict is PASS, else "no pass in 3 (cap)" | read |
| M2 blocking per round | `blocking` from `measure_round.py` (also minor) | read |
| M3 share caused by the previous fix | for each blocking finding after a fix cycle, ask: does the mechanism or sentence it attacks exist in the earlier plan version (`rg` on the snapshots)? Report a range: clear cases / clear + partial cases, exactly as `baseline-metrics.json` does. If the review states an origin itself, quote it as "reviewer tag" | derived (say so) |
| M4 document size | bytes and lines of the plan before review 1 and after each fix (`wc -c -l` on the snapshots); growth percent per cycle and over the loop | derived |
| M5 cost | `uv run python -I $PKG/tools/run_costs.py ~/.claude/projects/<slug of WT>/<session id>/subagents` gives agent, model, API messages, tool calls, wall seconds and output tokens per agent | derived |
| Confounders | orchestrator model, Claude Code version, the brief file used per step (verbatim or RECONSTRUCTED), any deviation, host load | read |

Compare with `baseline-metrics.json` under D6: (a) last-round blocking at most 5 (half of 10) or a clean pass in fewer rounds; (b) plan growth over the loop at most 46.9 percent in bytes (70 percent of 66.9); (c) larger than the spread between the two replicates.

## 7. Stop conditions and validity checks

- Stop at the first PASS, or after review 3 whatever its verdict. Never run a fourth review. Never run the merge step or `/sc:design`.
- Stop and write down the failure if an agent errors out, is refused by a hook, or runs for more than 90 minutes (the longest original step was 46 minutes).
- Validity check after each replicate (all must hold, else the replicate is void):
```bash
SUB=~/.claude/projects/<slug of WT>/<session id>/subagents
rg -l 'issue-394-launch-level-hook|hook-launch-level-394/42ae46e0|sc-issue-launch-level-hook|P2-hook-session' $SUB   # must print nothing
diff <(git -C "$WT" status --short | rg -v '^\?\? \.dev/replay/') "$WT/.dev/replay/s3/status-before.txt"              # must print nothing (no agent edited anything outside the staged folder)
```
The first command looks for agents that went to the finished work or the original logs. The second compares the worktree with its state right after staging (edits inside the untracked staged folder do not show, which is intended).

## 8. Cost to plan for

One Mode L replicate is about what the original loop cost: roughly 2 hours of wall time (127 minutes in the original), about 400 tool calls and 700,000 output tokens across 5 agents. Mode H costs about the same again. Two replicates of Mode L plus Mode H: about 6 hours of agent time.

## 9. Optional treatment arm that does put PR 427 in the path (clearly labelled, not a baseline replay)

PROPOSED, not from the original run. Replace each reviewer step by `/sc:spec-panel` run on the plan, in a worktree where the project copy carries the 427 text (section 3 step 4 must show 1). From the command's Usage line at `95f2c6e4`: `/sc:spec-panel @<plan> --mode critique --focus requirements,architecture,correctness`; for review 2 and 3 add `--re-review <prior findings file> --baseline <copy of the plan saved before the fix>`. Keep the reviser briefs as in Mode L. Check first that the invoked command text is the 427 text (ask the panel to quote its `## Review Loop` heading); the installed `~/.claude` copy is pre-427, and which copy wins over the project copy is UNVERIFIED here. The tool changes, the briefs change and the review job changes, so compare only the end-to-end measures (M1, last-round blocking, growth), and say it is a different design. A spec-panel verdict line (`verdict: PASS|FAIL`) and its `review: N of 3` header are the 427 contract.

## 10. Sections that are reconstructed or unknown

| Item | Status |
|---|---|
| Starting document v0 | REPLAYED from the recorded edits; line text confirmed by review 1's own reads (0 of 1,053 lines differ); bytes derived |
| v1 (used only in Mode H) | REPLAYED, line-verified against review 2's reads (0 of 1,138); v2 REPLAYED and byte-equal to the file on disk |
| Review 1 brief, all verbatim briefs | VERBATIM (byte-equal to the log; equal to the first user message of each agent log) |
| Reviser steering (Mode L) | RECONSTRUCTED: the original steering was written by the orchestrator after reading each review (`briefs/R1-orchestrator-note-after-review-1-L946.md`, `R2-...-L999.md`); the neutral briefs keep the owner's criterion and drop the finding-specific points (`tools/make_neutral_briefs.py` prints what was cut) |
| Reviewer briefs 2 and 3 (Mode L) | RECONSTRUCTED: only finding ids, counts and the examples of the original's first attacks generalised, plus one added line telling the reviewer to skip items the plan does not contain (`diff briefs/R2-reviewer-L975.md briefs/RECONSTRUCTED-R2-reviewer-generic.md`) |
| The orchestrator's decisions between rounds | NOT REPLAYABLE (a model reading each review); Mode L removes them, Mode H supplies the originals |
| Model sampling | NOT REPRODUCIBLE; hence two replicates |
| `~/.claude/settings.json` and other host state | not frozen (environment values); small fidelity gap |
| Orchestrator model, Claude Code version | differ or unknown; record them |

## 11. Pointer check

`bash tools/check_pointers.sh` (from the package root) re-checks the headings and phrases quoted at the file:line pointers in ANALYSIS.md. Then:
```bash
jq . baseline-metrics.json > /dev/null && echo json-ok
(cd inputs && sha256sum -c MANIFEST.sha256)
```

## RECREATION GRADE: B

**B: minor reconstructed parts, listed.** Verbatim: all six original briefs (byte-equal to the session log), every pipeline input (sizes equal the original agent's own `wc -c`), the tool and parameters (`Agent`, general-purpose, same `model` per step), the repo commit (8b4858f7) and installed skills. Line-verified: the starting document v0. Reconstructed and labelled: (1) the two reviser briefs' steering and the generalised ids in reviewer briefs 2 and 3, used only in the chained Mode L; (2) v0 and v1 byte counts (derived by replay). Not reproducible: the orchestrator's between-round decisions and model sampling, host settings, Claude Code and orchestrator model versions. It is not A because the chained loop cannot use the original reviser briefs unchanged; it is not C because every document and every reviewer instruction was recovered and the tool is the same. S3 can be re-run now; it cannot test PR 427 (section 0).
