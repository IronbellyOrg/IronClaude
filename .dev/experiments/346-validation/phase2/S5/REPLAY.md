# S5 REPLAY runbook: incident I5 (four final reviews of the P0 live-check plan package)

Folder: `.dev/experiments/346-validation/phase2/S5/` (all paths below are relative to it unless absolute). Evidence behind every statement: `ANALYSIS.md`, `inputs/SOURCES.md`, `briefs/INDEX.md`. Python only through `uv run --no-project python -I ...`.

## 0. Read this first: can PR 427 affect this scenario?

**No.** The reviewer in this incident is the managed final review of `/sc:implement`: a fresh `general-purpose` subagent that reads a prompt file (`AA` L2001, L2157, L2342, L2499). It never calls `/sc:spec-panel`. PR 427 (squash `95f2c6e4`) changed only `src/superclaude/commands/spec-panel.md`, the routing guide (`core/HOW-WE-WORK.md` and its plugin mirror), the plugin `spec-panel.md` mirror, two release guides, one design doc and one test (`git show --name-only 95f2c6e4`). Nothing under `src/superclaude/skills/sc-implement-protocol/` or `commands/implement.md` changed. So the expected effect of 427 on S5 is zero, and any measured difference between the baseline and a re-run is run-to-run variation of fresh reviewer sessions. Use S5 as a negative control and a noise-floor estimate (DECISIONS.md D4, "known limit"). Do not count it toward "427 proven" unless the coordinator decides otherwise.

## 1. What is replayed

The final-review loop only, on the stored package: review, scripted owner reply, fix, review again, until a pass or the fourth review. The expensive part of the original (T1 to T5 with three live Orca worker runs of 32 to 87 minutes each) is NOT re-run; the package already holds its evidence. Original cost for the loop: 4 reviews, 311 reviewer tool calls, about 380,000 reviewer output tokens, about 60 minutes of reviewer time (`baseline-metrics.json`).

## 2. Commits

| Purpose | Commit | Notes |
|---|---|---|
| Original run | repo HEAD `8db29f11` (branch `ironbelly/OrcaCLICommandRefactor-Specs`, checkout since deleted); protocol text byte-identical to git `80f934de` (`inputs/evidence/protocol-as-loaded/`); the last master commit without 427 is `ec1babd9` | `AA` L2193 "HEAD is unchanged at 8db29f11"; protocol bytes verified against the executor's Reads at `AA` L72, L96, L100 |
| **Arm A (as DECISIONS.md D4 requires)** | master at or after `95f2c6e4` (current master tip when this was written: `21fe3564`, which contains it), then `make sync-dev` and `make verify-sync` | Differs from the original by 427 AND by three other protocol commits (`4eb75698`, `055132ff`, `e032994f`) and by later Orca spec edits (see section 3, step 4) |
| **Arm B (recommended extra; isolates 427)** | worktree on `8db29f11`, then `git cherry-pick --no-commit 95f2c6e4`, then `git reset -q` (keeps the 427 edits in the working tree, HEAD stays `8db29f11`, index clean), then `make sync-dev` | `git merge-tree --write-tree --merge-base=95f2c6e4^ 8db29f11 95f2c6e4` reports a clean merge (tree `7d5e67506441...`). The cherry-pick recipe itself was NOT executed here (no worktree was created); treat it as untested beyond the merge check |

Create replay worktrees through Orca (project rule), never with raw `git worktree add`, and never pass `--issue` or `--pr`:
`orca worktree create --name exp346-s5-<arm>-<replicate> --base-branch <origin/master | 8db29f11>` then `orca worktree list` for the real path. Two replicates per arm, each in its own worktree and its own fresh Claude Code session (DECISIONS.md D6).

## 3. Setup (per replicate)

Let `ROOT` = the replay worktree path, `S5` = this folder's absolute path, `EV` = a scratch folder outside the repo (for example `/tmp/s5-<arm>-<rep>/ev`), `OUT` = `/tmp/s5-<arm>-<rep>/out`, `ID=TASK-WF-writeTheP0LivePl-20261103-215902`.

1. `cd $S5/inputs && sha256sum -c MANIFEST.sha256` must print only `OK`.
2. In `$ROOT`: Arm A: `git fetch origin && git merge-base --is-ancestor 95f2c6e4 HEAD && echo ok`. Arm B: the cherry-pick recipe above, then `git log -1 --format=%h` must print `8db29f11`. Then `make sync-dev && make verify-sync` (both arms; this is what carries the 427 spec-panel text into the project `.claude/` copy).
3. **Remove the leaked answer (Arm A only; master has it):** `rm -rf $ROOT/.dev/tasks/done/$ID` (replay worktree only; never commit that deletion). Without this the reviewers can read the finished package and the archive helper stops with `E-ARCHIVE-CONFLICT` once both locations exist. Check: `ls $ROOT/.dev/tasks/done | rg -c $ID` prints nothing.
4. **Overlay the old reference files (Arm A only; no-op for Arm B), after `sync-dev`:** `cp -r $S5/inputs/evidence/repo-snapshot-8db29f11/. $ROOT/`. This restores the 8db29f11 versions of the Orca spec, `WORKER-CONTRACT.md`, `workflow.md`, `adversarial.md` and `return-contract.md`, which the original reviewers read (they saw the pre-#368 step-5 wording). Never commit it.
5. Starting document: `mkdir -p $ROOT/.dev/tasks/to-do && cp -a $S5/inputs/package-R1/$ID $ROOT/.dev/tasks/to-do/$ID`. Verify: `(cd $ROOT/.dev/tasks/to-do/$ID && find . -type f ! -path ./progress.md | sort | xargs sha256sum) | diff - $S5/inputs/expected-states/R1-start.files.sha256` prints nothing. Stage the package only: `cd $ROOT && git add .dev/tasks/to-do/$ID` (not all of `.dev/tasks`: in Arm B that would also stage the unrelated task package that 427 carries and change the staged-file count the reviewers compare with `artifacts/staged.txt`, which lists 121 paths).
6. Unpack evidence:
   `mkdir -p $EV && tar -xzf $S5/inputs/evidence/worker-sessions.tar.gz -C $EV`
   `for k in 1 2 3 4; do mkdir -p $EV/executor-asof-R$k && tar -xzf $S5/inputs/evidence/executor-session-asof-R$k.tar.gz -C $EV/executor-asof-R$k --strip-components=1; done`
   `cp -r $S5/inputs/evidence/protocol-as-loaded $EV/protocol-as-loaded`
7. Render the briefs (paths only; every other byte is as logged): `uv run --no-project python -I $S5/inputs/tools/render_briefs.py $S5/briefs $ROOT $EV $OUT`. This writes `$OUT/R<k>-brief.md`, `$OUT/R<k>-spawn-prompt.txt` (verbatim apart from the path) and `$OUT/R<k>-spawn-prompt+pointer.txt` (see "Reconstructed parts", item 4). Nothing under `$OUT/` may be inside `$ROOT`.
8. Keep copies of the document at the start of every round for M3 and M4: `cp -a $ROOT/.dev/tasks/to-do/$ID $OUT/state-R<k>` immediately before spawning review k.
9. Do not open, list or search `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/` (the original reviewers' logs, including the verdicts) in the driver session, and scan every reviewer log afterwards (section 6, contamination check).

## 4. The loop

The replay driver is the fresh session. It plays the executor; it is not told the baseline results. For k = 1, 2, 3, 4:

1. Run the state helper and keep its output where the brief expects it (the brief names `state1.json`, `state3.json`, `state5.json`, `state7.json` for rounds 1 to 4):
   `uv run --no-project python $ROOT/src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py --root $ROOT --package $ROOT/.dev/tasks/to-do/$ID --print-state > $OUT/state/state<2k-1>.json` (the output must say `"status": "state"` with 57 files at round 1).
2. Spawn the reviewer with the Agent tool, exactly: `description` = `Independent final review of the package` (k=1), `Second independent final review` (k=2), `Third independent final review` (k=3), `Fourth independent final review` (k=4); `subagent_type` = `general-purpose`; `prompt` = the contents of `$OUT/R<k>-spawn-prompt+pointer.txt` for k = 1 to 3 and `$OUT/R<k>-spawn-prompt.txt` for k = 4; no `model`, no `run_in_background`. Do not add anything else to the prompt. Do not run `/sc:spec-panel` and do not pass any 427-specific flag (D4).
3. Save the reviewer's final message as `$OUT/R<k>-final-report.txt`. Its first line is `FINAL: pass` or `FINAL: issues`.
4. Re-run the state helper to `$OUT/state/state<2k>.json`; if the `state` value differs from step 1, the package changed during the review: discard and repeat the round. Otherwise append to the ledger, after all task lines (format from `managed-workspace.md` line 58): `FINAL: <pass|issues> evidence=<the reviewer's anchors, comma separated> state=<sha256 from the helper>` (see lines 13, 14, 16, 18 of `baseline-reference/original-final-ledger.progress.md` for the original shape).
5. If `FINAL: pass`: stop. Running the archive helper (`archive_workspace.py` with no flag) is optional; skip it unless the replicate must end in `done/`, because it moves the package.
6. If `FINAL: issues` and k < 4: stop as the protocol does (`E-ARCHIVE-BLOCKED`), give the scripted owner reply for round k (section 5), do the fix step, then continue with k+1.
7. If `FINAL: issues` and k = 4: stop and report the open blocking findings (the original owner's standing instruction at `AA` L2427: "If it returns issues, stop and report").

### Fix step (the "reviser")

Default, **Mode D (deterministic, recommended):** after an `issues` verdict from review k (k = 1, 2, 3) run `uv run --no-project python -I $S5/inputs/tools/apply_round.py $ROOT/.dev/tasks/to-do/$ID <k> $S5/inputs/round-deltas`. It applies the original executor's logged edits for that fix cycle (each `old_string` must match exactly once) and, for k = 2 and 3, appends the owner-accepted `ARCHIVE: Ruling:` line to the ledger. The resulting file states equal the original states (checked against `inputs/expected-states/R<k+1>-start.files.sha256`: `cd` into the package, `find . -type f ! -path ./progress.md | sort | xargs sha256sum | diff - <file>`). Effect: the document trajectory is identical to the original, so each round measures how a fresh reviewer judges the same document; replicates differ only in reviewer behaviour. If review k passes, stop; do not apply later deltas.

Optional, **Mode F (adaptive):** the driver makes the fixes the new findings call for, under the owner reply of section 5. Use only as a secondary arm; its replies are partly RECONSTRUCTED (section 5) and the document trajectory will differ from the baseline.

## 5. Scripted owner replies (verbatim files in `briefs/`)

| After review | Reply file (send as the user's instruction to the driver) | Log line |
|---|---|---|
| 1 | `briefs/afterR1-owner-revise-L2058.txt` | L2058 |
| 2 | `briefs/afterR2-owner-revise-L2204.txt` | L2204 |
| 3 | `briefs/afterR3-owner-revise-L2390.txt`, then, only if the driver stops again with a further finding, `briefs/afterR3-owner-revise2-L2427.txt` | L2390, L2427 |

In Mode D these replies only set the stage; the edits come from `apply_round.py`. In Mode F the verbatim file applies literally only when the new blocking finding is the same as the original one (round 1: the "six" miscount; round 2: the `orca-ide` sentence plus the empty bare `python3` call; round 3: the 22 helper calls). For any other finding use this text, RECONSTRUCTED from the four originals: "The owner says: approve. Fix the blocking findings of the last review narrowly (text corrections or disclosure only; no live-check rerun). If a finding is a plan-rule breach that text cannot cure, record the owner's acceptance in the ledger as a scoped `ARCHIVE: Ruling:` line before the next review. Run a fresh final review and archive if it passes. If it returns issues, stop and report. Do not commit or push."

## 6. What to record per round

Create `replay/<arm>-<replicate>/` (inside this folder or the coordinator's results folder) with `R<k>-final-report.txt`, the ledger, `state-R<k>` copies and one `replay-metrics.json` shaped like `baseline-metrics.json` (`rounds[]`, `M1`..`M5`). For every number say READ, COUNTED or RE-DERIVED.

| Metric | How |
|---|---|
| M1 | Number of reviews until the first `FINAL: pass`. If review 4 still says `issues`, write "not converged at the 4-review cap" and count 4 with a flag. |
| M2 | Blocking findings per round: entries in the reviewer's blocking list (before its `non-blocking:` list); also record the non-blocking count and the number of `Ti.ACk met` lines (23 expected). Do not re-grade. |
| M3 | For each blocking finding, check whether the anchored text exists in `state-R<k-1>` (then it is not fix-caused) or was written by fix cycle k-1 (`diff -r $OUT/state-R<k-1> $OUT/state-R<k>`; then it is). Say RE-DERIVED, and note when the cause is the previous review's own tool use (as in baseline round 3). Round 1 and any pass: null. |
| M4 | Bytes and lines of the package (all files) and of the 57 delivery files at the start of each round and after round 4: `uv run --no-project python -I $S5/derivation-scripts/m4.py <dir with R1..R4/$ID copies> <final package dir> <delivery list json>`; the delivery list is the `files` output of the state helper. Baseline growth over the loop: 0.593 percent (package), 0.736 percent (delivery files). |
| M5 | Per reviewer: `uv run --no-project python -I $S5/inputs/tools/reviewer_usage.py ~/.claude/projects/<replay project>/<session>/subagents/agent-<id>.jsonl` (tool calls, tokens, minutes; same counting rules as the baseline). Executor-side calls: count the driver's own tool calls between spawns. |
| Contamination check | Run the command in the block below the table on each reviewer log. Inspect every hit by hand: it is contamination only if a command reads from the original session folder `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/` or from a finished `done/<id>` copy. Absolute paths copied out of the package's own evidence files (they name the old checkout) are not contamination. A contaminated replicate is not used. |
| Stop reason | pass in round k / cap reached / contaminated / aborted. A pass in round 1 with no blocking findings means the reviewer missed latent defects; record it, do not read it as an improvement of the framework. |

Contamination check command (one reviewer log per run):

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use") | (.input | tojson)' <reviewer-log.jsonl> \
  | rg 'projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs|tasks/done/TASK-WF-writeTheP0LivePl'
```

## 7. Reconstructed parts (everything that is not byte-for-byte the original)

1. **Starting document.** Rebuilt from git (`b5c09e90`) by reversing ten logged `Edit` calls and cutting the ledger to 12 lines. Each rebuilt file at the start of each round equals a Claude Code file-history backup byte for byte, and the ledger prefixes equal `progress.md` backups (`inputs/SOURCES.md`). Only the permission bits and therefore the original package digests are lost.
2. **Machine paths in the briefs.** `render_briefs.py` replaces the original checkout path, `/tmp/ironclaude-p0live/`, the three worker-session folders, the executor-session path and the `qa.md` path. Nothing else is touched. The `state<N>.json` files are regenerated by the helper.
3. **Evidence copies.** Worker sessions are complete (they ended before the first review). The executor session is cut at each spawn time; `tool-results/` is not included.
4. **Executor-session pointer (rounds 1 to 3).** The original reviewers 1 to 3 found the executor log by listing the project folder of the checkout path (round 2 `agent-ad1d95b612f2d9bd6.jsonl` L258, round 3 `agent-a88ad232bf783d3a3.jsonl` L130). In a replay that folder holds the replay driver's own session, so `R<k>-spawn-prompt+pointer.txt` adds one sentence pointing at the as-of copy. This is the only addition to any prompt. Without it, checks about the executor's behaviour (the empty `python3` call, the earlier reviewers' python calls) audit the wrong log. Round 4's brief already names the executor session.
5. **Old reference files (Arm A).** Overlaid from git `8db29f11`. The installed `~/.claude/WORKER-CONTRACT.md` on the replay machine may still differ from the 8db29f11 copy in four lines unrelated to WC-10 and WC-13.
6. **Reviser.** Mode D uses the logged edits and rulings verbatim; Mode F cannot be verbatim (the original reviser was the executor model choosing its own fixes). Owner replies are verbatim files, but the generic text in section 5 is RECONSTRUCTED.
7. **Live-state checks cannot be reproduced.** The original reviewers also checked the live machine: HEAD `8db29f11`, which packages were staged, mtimes of protected folders, the worktree list. A replay has different values (Arm A: a different HEAD; both arms: other staged paths). A reviewer may raise findings from this that the original did not. Record such findings and mark them "replay artifact" when the anchor is live repo state; keep them in M2 but also report M2 without them.
8. **Model and sampling.** The logs record `claude-sonnet-5-5` for the executor and all four reviewers; the Agent calls carried no model parameter, so reviewers inherit the driver's model. Use the same model for the driver if the setup allows, and state the model used. No seed exists; reviewer behaviour is not repeatable.
9. **Protocol drift (Arm A).** Master's `sc-implement-protocol` differs from the original by commits `4eb75698`, `055132ff`, `e032994f` (`qa.md` by 21 lines, `ledger.md`, `managed-workspace.md`, `retry.md`, `archive_workspace.py`). The reviewer briefs do not read those files except `qa.md` (rendered to the as-loaded copy), but the driver's helper does. Arm B has no drift.

## 8. Stop conditions (summary)

`FINAL: pass` (success) · review 4 returned `issues` (report open findings) · contaminated reviewer log · helper `E-ARCHIVE-CONFLICT` (step 3 was skipped: fix and restart the replicate) · any step needing the live Orca worker checks to be re-run (never: the evidence is stored).

## RECREATION GRADE: B

**Grade B: minor reconstructed parts, listed in section 7.** The reviewer briefs for all four rounds and the four owner replies exist verbatim, the review tool and its parameters are known exactly (an `Agent` call to `general-purpose`, no flags), the starting document is rebuilt and verified against Claude Code's own backups, and every file the reviewers audited is copied out. It is not an A because (1) the document at the start is rebuilt rather than copied, (2) paths in the briefs are substituted and one pointer sentence is added to three spawn prompts, (3) the original reviser was a model making its own fixes, which can only be replayed as logged edits, and (4) live machine state the reviewers also checked cannot be restored. It is not a C because none of these changes what the reviewers are asked to do or what they read, and the logged edits reproduce the original document trajectory exactly. Separately from the grade: PR 427 cannot affect this scenario (section 0), so S5 can only serve as a negative control.
