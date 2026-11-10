# S2 REPLAY runbook (incident I2: review-severity-rule plan, three `/sc:reflect --mode pre` reviews)

Read `ANALYSIS.md` first (what happened, evidence pointers) and `baseline-metrics.json` (the numbers to compare against). `P` below is this folder, `.dev/experiments/346-validation/phase2/S2/` in the exp346-p1-logs worktree. Nothing in this package has been run against the incident.

## 0. Plain answer: can PR 427 affect this scenario?

No, not directly. The original reviewer was `/sc:reflect` in pre mode (UC-1) with its own reviewers and the `sc-adversarial-protocol` merge, never `/sc:spec-panel` (ANALYSIS.md section 3). PR 427 (squash 95f2c6e4) changes only `src/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md` (and its `plugins/superclaude/skills/sc-recommend/refs/` mirror), `plugins/superclaude/commands/spec-panel.md`, two release guides, one design doc and one test. None of them is read by `/sc:reflect`, `/sc:workflow` or `/sc:adversarial`. Expected delta: about zero (DECISIONS.md D4 already says so). Use S2 as a control that shows how far 427 reaches, not as a test of 427. If the coordinator wants a scenario that 427 can move, the only one in the phase-1 logs report is I1 (S1).

## 1. What to replay (two modes)

- **Mode R, reviewer-only replay (recommended, deterministic inputs).** Run the three reviews on the three RECORDED plan versions (plan v1, v3, v4), each with its recorded inventory snapshot. No live reviser. Isolates the reviewer side, which is the only side a review-loop contract could change. Everything it needs is verbatim in `P/inputs/round{1,2,3}/`.
- **Mode F, full loop (secondary).** Start from plan v1 only, review, revise with a live reviser, re-review, up to 3 reviews. The reviser step is RECONSTRUCTED (section 6) because the original reviser was the worker session itself, not a briefed agent.

Run both modes only if budget allows. Baseline cost for scale (baseline-metrics.json, M5): review 1 about 470 tool calls (78 main + 393 subagent), review 3 about 510, review 2 about 212; each fix cycle 78 and 67 calls.

## 2. Repository commit (read this before creating a worktree)

- **Original:** commit `f90877be1db0fc68c40205a763bd6b7d874aa0db` ("fix(implement): stop minor findings blocking QA via late promotion and line drift (#338)", 2026-10-31), equal to origin/master at 2026-11-01 22:46Z. Evidence: restart spec line 11 (`P/inputs/common/t11b-severity-rule-restart-spec.md`), session-start git status in MAIN L20 ("Recent commits: f90877be"). The worktree was clean except untracked `.dev/` files. `git cat-file -t f90877be` prints `commit` in this repo.
- **The last master commit before PR 427** is `ec1babd9` (DECISIONS D3). That is NOT the original base: 48 commits lie between f90877be and 95f2c6e4, including PR #343 (80f934de), which is the very fix this plan describes.
- **DECISIONS D4 as written ("base the worktree on master at or after 95f2c6e4") breaks this scenario.** At 95f2c6e4, `git grep -i 'of any severity'` over `src plugins commands agents` returns 0 hits (14 at f90877be); `pragmatic.md` already carries the new rule; the plan's acceptance checks and site lists describe edits that already exist; and the reviewers would apply the new rule from the tree they read. Running there measures a different scenario.
- **Recommended arms (needs the coordinator's OK because it departs from D4):**
  - **Arm T (treatment):** worktree at f90877be, then `git cherry-pick 95f2c6e4` (a trial merge `git merge-tree --write-tree --merge-base=95f2c6e4^ f90877be 95f2c6e4` exits 0, so it applies cleanly), then `make sync-dev` so the project `.claude/` copy carries the 427 spec-panel text. This is "f90877be plus exactly 427".
  - **Arm C (control, same tree without 427):** worktree at f90877be, `make sync-dev`. Recommended because the original baseline ran under whatever `~/.claude` was installed on 2026-11-02, and today's global files (output style, skills) are newer and contain the new severity rule. Without Arm C the recorded baseline and Arm T differ in more than 427.
  - **Arm M (D4 as written):** only if the coordinator insists; label every result "scenario invalid: fix already in tree".
- Create the worktree through Orca at its default location (CLAUDE.md rule), e.g. `orca worktree create --name exp346-s2-armT --base-branch f90877be --no-parent` (check with `orca worktree list`; whether a bare SHA is accepted as `--base-branch` is UNVERIFIED, fallback: `git branch exp346-s2-base f90877be` and pass that branch name). Never pass `--issue` or `--pr` for this repo. Do not use `EnterWorktree`.

## 3. Setup, per replicate session

1. Open a fresh Claude Code session with cwd at the new worktree root. Use the same model split as the original if possible: orchestrator `claude-opus-5-5`; Tier 2 reviewers sonnet (`claude-sonnet-5-5`), qa persona on the `haiku` alias (it resolved to `glm-5.3` originally), refactorer opus; calibrators opus (source: R1-REPORT line 22 and the audit.log note in MAIN L1910). Record what each alias resolves to in the new environment (names only; copy no environment values or tokens into any report).
2. Place the recorded inputs for round N and get the exact review command: `bash P/replay-setup.sh <worktree-root> N` (N = 1, 2 or 3). It copies plan, `source.md`, `inventory.md` (and `cap-sites.md`, `cap-edits.yaml` for rounds 2 and 3) to their original relative paths, `FINDINGS.md` to `.dev/qa-loop-investigation/`, the two spec files to `/tmp` (no overwrite), and rewrites the old absolute prefix `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule` to the new root in the placed copies (path-only change; `P/inputs/` keeps the original bytes; SHA-256 in `inputs/MANIFEST.sha256`). Tested on scratch directories only.
3. Do not stage `.dev/` replay files in the experiment worktree unless the coordinator asks; never commit, push or open a PR from a replay worktree.

## 4. Exact review command and flags per round (what the original did)

The original issued exactly one Skill call for the review: `Skill sc-reflect-protocol`, args `--mode pre --spec <pkg>/source.md --tasklist <pkg>/<plan>.md` (MAIN L460, `P/briefs/R1-reflect-skill-invocation-args__L460.txt`). It set no `--tier`, `--depth`, `--reviewers`, `--output` or `--no-*` flag, so the tier was chosen by the protocol (Tier 2 by rule 4 in all three rounds). Rounds 2 and 3 re-executed the loaded protocol inline without a new Skill call. The slash-command equivalent to run in a replay, once per round:

```text
/sc:reflect --mode pre --spec <root>/.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-<ID>/source.md --tasklist <root>/.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-<ID>/TASK-WF-removeTheAnyIssu-<ID>.md
```

| Round | `<ID>` (document) | Files placed by `replay-setup.sh` |
|---|---|---|
| 1 | `20261101-225635` (plan v1, 14 tasks, 23,890 B) | plan, source, inventory (213 lines) |
| 2 | `20261102-042031` (plan v3, 19 tasks, 31,868 B) | plan, source, inventory (215 lines), cap-sites (361 lines) |
| 3 | `20261102-053741` (plan v4, 20 tasks, 32,107 B) | plan, source, inventory (216 lines), cap-sites, cap-edits.yaml (1,399 lines) |

Invoke each round as a real `/sc:reflect` call (Skill tool), not by reading the command file; the original also reached the protocol through the Skill tool (MAIN L460). The installed skill text at f90877be equals what the worker loaded (ANALYSIS.md section 3). The reflect run writes its own coverage matrix, Tier 1 card, reviewer briefs, cards and REPORT.md; those are regenerated, not injected. The recorded versions are in `P/briefs/` and `P/baseline-outputs/` for comparison only. Do not edit the inventory during a round (the original round 2 stopped on exactly that, `input_drift`).

Severity rule in force in every round of the original: blocking/minor grading, only blocking findings fail, minor findings are notes, at most 2 fix cycles (3 reviews) then escalate with the open blocking findings (ANALYSIS.md section 4). In a replay, give the session the same two sentences the worker had: restart spec lines 15-16 and 26 (`P/inputs/common/t11b-severity-rule-restart-spec.md`). Under Arm T/C at f90877be the repo's own output style still says "any issue of any severity fails", exactly as in the original tree, so say in the first prompt that the rule above governs the run. Do not add `--re-review` or any other 427-only flag in the main arms (DECISIONS D4); a separately labelled extra arm may.

## 5. Loop mechanics and stop conditions

- Mode R: three independent reviews, one per placed round, each in its own fresh session or a clearly separated `/clear`ed context so one review does not see another's report.
- Mode F: review 1 on plan v1 -> if blocking findings exist, run the reviser (section 6) -> review 2 on the new plan -> reviser -> review 3.
- Stop conditions (same as the original): (a) a review with zero blocking findings = clean pass, stop; (b) three reviews done = cap, stop, record the open blocking findings and "escalate" (no fourth review, no further fix cycle); (c) a review that stops with `status: partial` is recorded as such and counted as a review.
- Do not answer the cli-portify question from the original round 2 yourself. In mode R the round-2 and round-3 inventory snapshots already contain the decided answer ("1 iteration", MAIN L2181); in mode F, if the reviewer asks, answer with the recorded text in `P/briefs/R2-coordinator-ask-cli-portify-ANSWER__result-of-L2175.txt`.

## 6. Reviser step (Mode F only)

The original reviser was the worker itself regenerating the plan as a new `/sc:workflow` package; its recorded outputs are verbatim (`inputs/round2/`, `inputs/round3/`), its instruction is not a stored brief.

RECONSTRUCTED reviser brief (not verbatim; built from R1-REPORT recommendation R-001 (lines 54-58), restart spec line 26, and the worker's narration at MAIN L1686, L1777, L2254):

> Fix cycle N of the plan review loop (cap: 2 fix cycles). Read the review report REPORT.md of the last review. Regenerate the plan as a new package with `/sc:workflow` from an inline source that keeps the requirements R-001..R-010 and folds in every BLOCKING finding by id, naming each affected file by quoted text. Do not fix minor findings. Run a repo-wide scan so the new plan names every site of the same kind, then pre-review the new plan (review N+1 of at most 3).

For comparison, the verbatim helper briefs used in the originals are `P/briefs/FC1-cap-site-classifier__L1709.md` and `P/briefs/FC2-literal-cap-edit-table__L2255.md`; the verbatim source text of the regenerated plans is `inputs/round2/source.md` and `inputs/round3/source.md`.

## 7. What was recovered verbatim (index of `P/briefs/`)

Every file name ends with the jsonl line (`MAIN` = session d6112a25, `sub-<id>` = the reviewer's own log).

| Role / round | Files | Status |
|---|---|---|
| Worker dispatch, restart, plan prompt | `00-orca-dispatch-brief__L10.txt`, `00-restart-message__L626.txt`, `00-sc-workflow-invocation-args__L308.txt` | VERBATIM |
| Review invocation | `R1-reflect-skill-invocation-args__L460.txt` | VERBATIM |
| Reviewer spawn prompts, rounds 1-3 | `R{1,2,3}-reviewer-{1,2,3}-*-spawn__L*.md` (334/318 chars each, point to the brief files) | VERBATIM |
| Reviewer brief files, rounds 1-3 | `R1-*-brieffile__L870/875/880`, `R2-*-brieffile__L2069/2074/2079`, `R3-*-brieffile__sub-*` | VERBATIM (R1 and R2 reviewer 1 checked equal to what the reviewer Read; R3 taken from the reviewers' own Read results) |
| Coverage matrix, Tier 1 calibrators, card calibrators | `R{1,2,3}-coverage-matrix-*`, `R*-tier1-blind-calibrator__*`, `R1-card-calibrator-*`, `R3-card-calibrator-*` | VERBATIM. Round 2 has no card calibrators (run stopped). |
| Adversarial merge, evidence validation | `R1-adversarial-*`, `R1-merge-executor`, `R1-evidence-validator`, `R3-adversarial-*`, `R3-merge-executor`, `R3-evidence-validator` | VERBATIM. None in round 2. |
| Fix-cycle helper agents | `FC1-cap-site-classifier__L1709.md`, `FC2-literal-cap-edit-table__L2255.md` | VERBATIM |
| Reviser instruction (the worker's own regeneration) | none stored | NOT RECOVERABLE as a brief; RECONSTRUCTED in section 6; outputs are verbatim |
| Coordinator exchanges | `R2-coordinator-ask-*`, `R3-escalation-*`, `POST-coordinator-decision-*` | VERBATIM |
| The Bash heredoc that generated the round-3 reviewer briefs | MAIN L2615 | the generated text is recovered (above); the generator command itself is not reproduced |

## 8. What to record per round for M1 to M5 (same definitions as `baseline-metrics.json`)

- **M1** verdict of the review (PASS/FAIL, `status` from the reflect contract) and, over the loop, the first round with zero blocking findings (or "cap reached"). Source: the run's `REPORT.md` header and Summary.
- **M2** number of blocking findings and number of minor findings after the merge (R1 had 11 and 17, R2 7 and not counted, R3 10 and 12). Record whether the run was partial. Grade by the definition in the S1 sentence of the rule, not by labels.
- **M3** share of blocking findings caused by the previous fix. The reflect reviewers do not tag origin, so classify each blocking finding as "defect written or left ineffective by the last fix" or "pre-existing site missed", from the report text and the previous plan; mark the basis (R = re-derived). Mode R has no live fix, so for rounds 2 and 3 classify against the recorded fix. Baseline: round 2 = 4 of 7, round 3 = 2 of 10 (basis R; classification lists in baseline-metrics.json).
- **M4** document size at start and after each round: `wc -c -l <plan>` (baseline: 23,890 B / 202 lines / 14 tasks; 31,868 / 264 / 19; 32,107 / 275 / 20). In mode R sizes are fixed by the inputs; in mode F they are measured on the reviser's output. Growth = percent over plan v1.
- **M5** tool calls and tokens per round from the session jsonl (main plus subagent logs). Method used for the baseline: count `tool_use` blocks and sum final `usage` per assistant message id; fresh input = input + cache creation, cache reads excluded.
- Also keep each round's REPORT.md and reviewer cards in the replicate folder so M2 and M3 can be re-checked.

Replicates: DECISIONS D6 needs two replicate sessions per arm. Name outputs `phase2/S2/replay/<arm>-<replicate>/round-N/`.

## 9. Known confounds to state in any result

1. Installed `~/.claude` files differ from the original run's (not recoverable; only the reflect skill text was matched to f90877be).
2. Model aliases may resolve differently; reviewer diversity (the `glm-5.3` qa reviewer) may change.
3. LLM variance: the baseline is one recorded run; the spread between two replicates is the noise bar (D6c).
4. Round 2 of the baseline is a partial run (no merge), so its blocking count is not like-for-like; compare round 2 with a replay that also stops, or compare only rounds 1 and 3 on M2.
5. Path rewrite in placed copies (section 3 step 2) changes plan bytes slightly versus `inputs/`.
6. `cap-sites.md` for round 3 is assumed equal to round 2 (no recorded change; ANALYSIS.md section 7).
7. Today's reviewers read a repo that is at f90877be (Arms T, C) only if the replay worktree is based there; any other base changes the findings.

## RECREATION GRADE: B

Grade B (minor reconstructed parts, listed). Why not A: the reviser step has no stored brief and is RECONSTRUCTED for Mode F (section 6); the reviewers' briefs are regenerated by the review run rather than injected (the recorded copies are for comparison); the installed `~/.claude` of the original session and the model-alias resolution cannot be restored; one coordinator answer was injected mid-loop; `cap-sites.md` for round 3 is assumed; the old worktree path is rewritten. Why not C: the starting document, its source, the specs and the inventory snapshots are byte-exact (compared with what the reviewers Read); the review tool, flags and personas are known; all reviewer, helper and coordinator briefs are verbatim; the recorded fix outputs (plans v3 and v4) allow an exact reviewer-only replay (Mode R); the original commit f90877be is in git. Separate from the grade: this scenario cannot exercise PR 427's spec-panel changes (section 0), and the D4 base instruction (master at or after 95f2c6e4) must be changed to f90877be plus a cherry-pick of 95f2c6e4 for the scenario to mean anything (section 2). Because the grade is B, no `candidate-swap.md` is provided.
