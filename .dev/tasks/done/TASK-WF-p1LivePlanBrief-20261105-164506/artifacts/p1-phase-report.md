# P1 phase report: Orca worker contract

Plan: `./TASK-WF-p1LivePlanBrief-20261105-164506.md` (live plan, revision 3). Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (pass rule at line 238: the phase passes only when both plans' checks pass).
Checkout: branch `ironbelly/OrcaCLICommandRefactor-P1`, HEAD `0b44374513780b69f59d9018c06cbf0b4af420ad` (`git rev-parse HEAD`, also `./artifacts/branch-tip.txt`). Run date: 2026-11-05. Orca runtime: `1.4.245-aidev02.dfe1eb410300` (`./artifacts/orca-version.txt`). Run id: `run_92b0ef27e086` (`./artifacts/live-run.json`).

## P1 verdict

**P1 verdict: FAIL.** Cause: two live checks recorded a FAIL. Both are recorded gaps in a command (a FAIL of AC-1.2 on a command), not repaired by this plan.
- **lc09 `/sc:adversarial`** (`./artifacts/lc09-result.md`, `lc09-step5.md`): step 5 condition 4 fails limit (a) of spec 7.2 step 5. Between the heartbeats sent at about 19:32:26 and 19:40:59 there were 6.4 minutes with no subagent running (limit: the 5-minute cadence). Limit (b) held (largest raw gap 8.6 min, limit 20). Owner decision H1 accepts a gap inside a command's own subagent fan-out; this stretch lies between the advocate round and the judge round with no subagent running, so it is recorded as a failure.
- **lc10 `/sc:brainstorm`** (`./artifacts/lc10-result.md`): the step 4 extra fails as written. The codebase-enrichment wave ran (`enrichment_used`: `codebase`, `quality_tier: fallback_1`) but no `nested/analyze-1/` directory exists, because the worker did not call `/sc:analyze` (the auggie tool was absent and codegraph search, Grep and Read were used). The other parts of the extra hold. `sc-brainstorm-protocol/SKILL.md:195` does not say what the fallback tier writes, so the plan's wording and the skill differ here; this is for the owner to read.

Result count: 23 live rows (lc01 to lc22 and ac-1.3): 21 PASS, 2 FAIL, 0 `not verifiable`, 0 `not run`. AC-1.8 (lc22) ran because the owner gave the instruction.

The phase passes only when this report and the static report both pass. The static report covers commit `7127c2478756c9444afc600af3e3066b3f7f24db`; these live checks ran on the branch tip `0b44374513780b69f59d9018c06cbf0b4af420ad` (`./artifacts/branch-tip.txt`), a descendant of that commit.

## Static part (from the passed static report)

Source: `.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md` (not re-run, evidence not copied). Its overall line: PASS (11 of 11).

| Check ID | Verdict recorded there |
|---|---|
| AC-1.1 | PASS |
| AC-1.4 | PASS |
| AC-C1 | PASS |
| AC-C2 | PASS |
| AC-C3 | PASS |
| AC-C4 | PASS |
| AC-C5 | PASS |
| AC-C6 | PASS |

(Also recorded there as PASS: lint, format and the mirror check.)

## Live part

Verdicts are taken from each `lc<NN>-result.md` or `ac-1.3.md` ("Overall verdict" or the file-creation result).

| Check | Spec check | Command | Verdict | Evidence file |
|---|---|---|---|---|
| lc01 | AC-1.2 | `/sc:analyze` | PASS | `lc01-result.md` |
| lc02 | AC-1.2 | `/sc:build` | PASS | `lc02-result.md` |
| lc03 | AC-1.2 | `/sc:business-panel` | PASS | `lc03-result.md` |
| lc04 | AC-1.2 | `/sc:design` | PASS | `lc04-result.md` |
| lc05 | AC-1.2 | `/sc:document` | PASS | `lc05-result.md` |
| lc06 | AC-1.2 | `/sc:explain` | PASS | `lc06-result.md` |
| lc07 | AC-1.2 | `/sc:index` | PASS | `lc07-result.md` |
| lc08 | AC-1.2 | `/sc:test` | PASS | `lc08-result.md` |
| lc09 | AC-1.2 | `/sc:adversarial` | **FAIL** (step 5 condition 4, limit a) | `lc09-result.md` |
| lc10 | AC-1.2 | `/sc:brainstorm` | **FAIL** (step 4 extra: no `nested/analyze-1/` for the codebase wave) | `lc10-result.md` |
| lc11 | AC-1.2 | `/sc:cleanup-audit` | PASS | `lc11-result.md` |
| lc12 | AC-1.2 | `/sc:graph` | PASS | `lc12-result.md` |
| lc13 | AC-1.2 | `/sc:impact` | PASS | `lc13-result.md` |
| lc14 | AC-1.2 | `/sc:index-repo` | PASS | `lc14-result.md` |
| lc15 | AC-1.2 | `/sc:init-lite` | PASS | `lc15-result.md` |
| lc16 | AC-1.2 | `/sc:workflow` | PASS | `lc16-result.md` |
| lc17 | AC-1.5 | `/sc:analyze` with no report directory | PASS | `lc17-result.md` |
| lc18 | AC-1.6 | `/sc:test --watch --unattended` | PASS | `lc18-result.md` |
| lc19 | AC-1.7 case 1 | brief guard, `/sc:analyze` without `--unattended` | PASS | `lc19-result.md` |
| lc20 | AC-1.7 case 2 | brief guard, `/sc:troubleshoot` (no section) | PASS | `lc20-result.md` |
| lc21 | AC-1.7 case 3 | brief guard, `/sc:help` (never-as-worker) | PASS | `lc21-result.md` |
| lc22 | AC-1.8 | `/sc:explain` with a granted local commit | PASS | `lc22-result.md` |
| ac-1.3 | AC-1.3 (file creation) | plain `/sc:analyze` and `/sc:explain` in `claude -p` | PASS | `ac-1.3.md` |

Each live row passed the install precondition (`preflight.md`: install line PASS, 62 paths compared, none differing).

## Heartbeat length (spec line 291)

Per check, from each `lc<NN>-step5.md` (run length and heartbeat count). Cadence quoted from the workers' preamble: "Send a heartbeat every 5 minutes while actively working on the task."

| Check | Run length (min) | Heartbeats | Check | Run length (min) | Heartbeats |
|---|---|---|---|---|---|
| lc01 | 0.9 | 1 | lc12 | 0.8 | 0 |
| lc02 | 1.0 | 1 | lc13 | 2.0 | 1 |
| lc03 | 2.5 | 1 | lc14 | 1.9 | 1 |
| lc04 | 2.1 | 1 | lc15 | 0.7 | 0 |
| lc05 | 0.8 | 0 | lc16 | 21.8 | 5 |
| lc06 | 1.2 | 1 | lc17 | 0.3 | 0 |
| lc07 | 0.7 | 0 | lc18 | 0.5 | 0 |
| lc08 | 0.7 | 0 | lc19 | 0.4 | 0 |
| lc09 | 23.2 | 5 | lc20 | 0.5 | 0 |
| lc10 | 13.9 | 6 | lc21 | 0.2 | 0 |
| lc11 | 5.4 | 3 | lc22 | 1.1 | 1 |

Checked runs longer than the 5-minute cadence: lc09 (23.2 min), lc16 (21.8 min), lc10 (13.9 min) and lc11 (5.4 min). Their condition 4 results: lc10 PASS (largest raw gap 5.1 min, largest non-agent stretch 2.0 min), lc11 PASS (largest non-agent stretch 1.0 min), lc16 PASS (largest raw gap 5.5 min, largest non-agent stretch 2.7 min), lc09 FAIL (6.4 min with no subagent running). All other runs are shorter than the cadence and pass condition 4 vacuously. In lc09 three of the five heartbeat `send` calls sit inside longer Bash calls; `lc09-step5.md` gives the refined send times, which do not change the result.

## Brief-guard refusal bodies and the WC-4 error text

- lc19 (case 1), first words: "guard refused: brief lacks --unattended." (`lc19-step3.json`)
- lc20 (case 2), first words: "guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)." (`lc20-step3.json`)
- lc21 (case 3), first words: "guard refused: /sc:help is on the never-as-worker list in ~/.claude/WORKER-CONTRACT.md (section 1, case 3), so it is never dispatched as a worker and has no --unattended mode." (`lc21-step3.json`)
- lc17 (AC-1.5), exact error text printed by `/sc:analyze` with no report directory: `unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag` (`lc17-result.md`; found in the worker's session file and in `lc17-transcript-1.json`).

In lc19 to lc21 the command was not invoked (`lc19-step5.md`, `lc20-step5.md`, `lc21-step5.md`).

## Branches that remain after removal

From the `lc<NN>-branch-after.txt` files: only lc22 left a branch, `ironbelly/p1-live-commit-grant`, at the worker's commit `c682bb2a26f75c99f554245b03d21aa7f067aea7` (`lc22-branch-after.txt`). `orca worktree rm` did not delete it, and the executor never deletes a branch. All other files are empty.

## Workers or worktrees left for the person

No worktree remains: every `lc<NN>-worktree-list-after.json` and `ac13-worktree-list-after.json` lacks its disposable worktree. Four workers were not released cleanly: `worker-release` answered `state: retained`, `reason: user_takeover`, `processAction: none` instead of `released` for lc07 (`ctx_c8adcb940377`, terminal `term_c8d5fdb2-67a8-4615-b051-ffb35cdbf7f9`), lc09 (`ctx_df434d14e765`, `term_c2a044ba-abb3-4864-b1f8-e1ed62f1288d`), lc11 (`ctx_c548258e9f0b`, `term_64fb8d96-bd33-447b-a88c-744846372926`) and lc16 (`ctx_6c10bde223ae`, `term_1a6fde09-00c4-42f2-9bda-edbd2b50899c`). In each, the step 7 pass rule (the reclaimable list returns no rows) held, and `worker-show` for lc07 reported the worker `exited`. Their terminals may still be open in Orca; the person can close them. Cause not found: nothing in these runs shows a user action.

## Staging found inside a disposable worktree

All 22 `lc<NN>-index-after.txt` files are empty: no worker staged anything (no WC-9 finding). In lc22 the granted worker ran `git add -- <two report files>` and `git add .dev/tasks` and committed with `git commit --only`; the commit is the authorized local commit, and the child's index was empty afterwards. The worker's `git add .dev/tasks` staged nothing (no `.dev/tasks` exists in the child).

## Open owner items

1. The manual part of AC-1.3 (not run by this plan), quoted from `ac-1.3.md`: "run `/sc:analyze <path>` and `/sc:explain <path>` in a plain interactive Claude Code session and in the coordinator session with `WORKER-CONTRACT.md` loaded, and confirm that today's prompts and defaults appear and that no brief-guard refusal occurs".
2. AC-1.8 was run (the owner's sentence is in the plan Constraints and in `lc22-brief.txt`); it is not an open item. Open for the owner: keep or delete the local branch `ironbelly/p1-live-commit-grant` (it holds the one granted commit; nothing was pushed).
3. For lc09: decide whether the 6.4-minute stretch with no subagent running counts under owner decision H1 (this report records it as FAIL).
4. For lc10: decide whether the nested `/sc:analyze` call is required when the codebase enrichment uses the fallback tier (this report records the extra as FAIL as written).

## Notes for the coordinator and owner

- Remote and pull requests: `git ls-remote origin` and `gh pr list --repo IronbellyOrg/IronClaude --author @me` were identical before and after lc22 (`lc22-before-lsremote.txt` and `lc22-after-lsremote.txt`; the PR lists are both empty). Nothing was pushed by this plan.
- Tip: the live checks ran on `0b44374513780b69f59d9018c06cbf0b4af420ad`; the static report covers `7127c247`. Both are on the same branch; the install precondition compared 62 files with no difference.
- Workers that made no Skill call (they read the command file and carried the command out in their top-level session; no Agent call): lc01, lc02, lc04, lc05, lc06, lc07, lc08, lc14, lc17, lc18 and lc22. Step 5 condition 2 was recorded PASS for them because the command was not run inside an Agent call; whether that satisfies WC-7 for a command that is normally a Skill call is for the owner to read.
- `worker-release` returned `retained` for lc07, lc09, lc11 and lc16 (see above); the step 7 pass rule as written still held.
- lc13 `/sc:impact`: the report and the contract's `report_path` and `artifacts` are absolute worktree paths, and the report was written to the command's default folder `.dev/impact/` (documented at `src/superclaude/commands/impact.md:38`), not under the report directory; the contract in the report directory is the command's own contract with the worker fields.
- lc14 `/sc:index-repo` modified the two tracked files `PROJECT_INDEX.md` and `PROJECT_INDEX.json` in its worktree (documented, `index-repo.md:178-189`). lc11 wrote `.claude-audit/` and lc16 wrote a new `TASK-WF-*` package and a `.dev/reflect/` run in their worktrees (documented artifacts); all were copied into `lc11-report/`, `lc16-report/` before removal.
- The P0 script `session-analysis.py` crashes with an `IndexError` on a run with 0 heartbeats (lc05, lc07, lc08, lc12, lc15, lc17, lc18, lc19, lc20, lc21). The remaining counts for those runs were computed with `jq` over the same session file and are in `lc<NN>-session-analysis-supplement.txt`.
- Session file lengths and sha256 in each `lc<NN>-step5.md` are the values at analysis time (the first recorded length). `lc01-step5.md` first recorded a later length by mistake; it was corrected after Task 2 completed (the file says so).
- Procedure deviation: step 3 says to read `worker-read` after a wait turn that ends with no message. For lc09 (empty turns 1 to 5; one `worker-read` after turn 4, not saved), lc10 (empty turns 1 to 3) and lc11 (empty turn 1) no `worker-read` output was saved for those empty turns; from lc12 on the driver saved it (`lc<NN>-wait-<k>-transcript.json`, `lc<NN>-step3-waits.txt`; lc16 shows a growing transcript on every empty turn). The outcome of those runs is not affected.
- Review notes: Task 19 (lc18) had two blocking review findings (`lc18-step4.txt` did not show the contract's `worker_status` and `reason`); one fix pass appended them from the saved contract copy and the re-review passed (`retries/T19/`). Minor findings of the other tasks are in `retries/T<id>/notes.md`.
- Heartbeat sends inside long Bash calls (lc09) and the `retained` release state are the two findings most likely to matter for P2.
- The `.dev/p1-live/`, `.dev/impact/` and `.claude-audit/` folders were created only inside disposable worktrees; the feature worktree's HEAD is unchanged (`head-final.txt` equals `branch-tip.txt`).

Recording status: complete (verdict recorded, not a task failure)
