# S1 REPLAY runbook: re-run the I1 review loop (Orca worker-contract spec)

For a fresh session or coordinator. Everything needed is in this folder. Do not run any of it from the analysis worker. The recreation grade is the last section.

Pointer keys: `PJ`, `BO`, `B`, `CO` as in `ANALYSIS.md` section 0. `S1` = this folder (`.dev/experiments/346-validation/phase2/S1/`).

## 1. Does PR 427 affect this scenario? (plain answer)

**Yes, but only in 3 of the 7 original reviews, and only through part of what 427 added.**

- The original reviewer used `/sc:spec-panel` in rounds 1 to 3: R1 through the `Skill` tool (`PJ/699ae853` L56, args `@.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`); R2 and R3 only read `~/.claude/commands/sc/spec-panel.md` and followed it by hand (`PJ/aff19d65` L39, `PJ/1c9a7ec8` L142). Tasks 11 to 17 were told not to run the panel.
- PR 427 changes only `src/superclaude/commands/spec-panel.md` (462 to 472 lines; new `## Review Loop`, new `--re-review <file> --baseline <copy>` usage form), the `plugins/` mirror, the routing guide and two release guides (`inputs/tool-text/spec-panel-427.diff`).
- The original briefs pass neither `--re-review` nor `--baseline`, so the diff-scoped re-review does not engage. With verbatim briefs 427 acts through its grading (CRITICAL/FR-8/FR-9 blocking, minor never fails), the `verdict: PASS|FAIL` last line, the `review: N of 3` header with a cap at 3 reviews, and the rule that a brief cannot grade a minor finding as blocking. The R2/R3 briefs say "any finding of any severity is FAIL", so 427's rule and the brief disagree by design; that is the effect being measured.
- 427 does not touch the writer, the revisers or Tasks 11 to 17. Expect roughly zero delta from anything outside the three panel reviews.

## 2. What the original run was (baseline facts)

| Item | Value | Evidence |
|---|---|---|
| Repo commit, rounds 1 to 3 | `2cb683f5c1f0dfbd3c5f169a8b64a432931f718e` (master of 2026-10-30), branch `ironbelly/OrcaCLICommandRefactor-Specs`, worktree `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs`. The branch was fast-forwarded to `c118b5a5` at 2026-11-02T15:25:37Z, after Task 11 | `git reflog show --date=iso ironbelly/OrcaCLICommandRefactor-Specs`; `PJ/*.jsonl` fields `gitBranch`, `cwd` |
| Framework text of the command | 462-line `spec-panel.md`, identical at `2cb683f5` and `ec1babd9` (last master commit before 427) | `inputs/tool-text/spec-panel-pre427-ec1babd9.md` |
| Claude Code / model | `2.1.316` / `claude-opus-5-5` for all 17 worker sessions | `PJ/*.jsonl` `version`, `message.model` |
| Orca build | `1.4.237-aidev02.0e4491a95e92` (live `--help` output the reviewers cited) | `BO/spec-panel-round3.md:19` |
| Worker model | one Orca worker per task, each a fresh top-level Claude session | `B/task-text/*`, preamble "You are a dispatched worker" |
| Starting document | spec v1, 57,763 bytes, 285 lines | `inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |

## 3. Choose the re-run environment (a coordinator decision)

D4 says: base the worktree on master at or after `95f2c6e4`, run `make sync-dev`. This analysis found that this has two problems for this scenario. Pick the arm before starting; run both if budget allows.

| | Arm T-literal (D4 as written) | Arm T-pinned (recommended; needs coordinator OK because it deviates from D4's base) |
|---|---|---|
| Base | `95f2c6e4` exactly (preferred, 472-line spec-panel) or later master (tip `21fe3564` adds the inert `--unattended` text, 486 lines) | `2cb683f5` (the original base) plus ONLY the 427 diff on `spec-panel.md` |
| 427 text | from `make sync-dev` | from `git apply inputs/tool-text/spec-panel-427.diff`, then `make sync-dev` (checked: result is byte-identical to the `95f2c6e4` file) |
| Evidence drift | 25 of 45 command files changed since `2cb683f5`; 19 of 37 `cmd/*.md` files the spec cites changed; spec evidence E5 ("no command ... calls Orca today", v1 line 25) is false; `WORKER-CONTRACT.md` exists. Reviewers will report citation defects unrelated to loop convergence | none: identical to what the original reviewers saw |
| Answer-key contamination | **178 tracked files under `.dev/orca-command-refactor/` (all original reviews, dispositions, final spec) plus 192 other `.dev/tasks` and `.dev/reflect` files naming the incident** | none: 0 hits at `2cb683f5` |
| Isolation work | remove those paths from the worktree before dispatch (section 4, step 3) | none |
| What it measures | "427 as installed in today's repo", with drift and contamination controls | "427 text only", everything else as in the original |

If only one arm is run, run T-pinned. If the coordinator insists on D4 as written, the T-literal arm must do the isolation in step 3; without it the arm is invalid.

## 4. Setup (per arm and per replicate; one worktree each)

1. Create the worktree through Orca at its default location (never `git worktree add`, never link flags `--issue/--pr`):
   `orca worktree create --name s1-<arm>-<replicate> --base-branch <ref>` where `<ref>` is `95f2c6e4` (T-literal) or `2cb683f5` (T-pinned). Read the real path with `orca worktree list`.
2. 427 text:
   - T-literal: `make sync-dev` (the 427 text is already tracked at `95f2c6e4`).
   - T-pinned: `git apply --check <S1>/inputs/tool-text/spec-panel-427.diff && git apply <S1>/inputs/tool-text/spec-panel-427.diff`, then `make sync-dev`.
   - Do NOT run `superclaude install` and do not edit `~/.claude` (D7). The installed `~/.claude/commands/sc/spec-panel.md` on the machine is the pre-427 text (identical to `ec1babd9`); see validity check V1.
3. Isolation (mandatory for T-literal; in T-pinned only the 427 diff from step 2 needs committing):
   - T-literal: `git rm -r -q -- .dev/orca-command-refactor .dev/tasks .dev/reflect` (these hold the original reviews and 192 files naming the incident; none is needed as evidence).
   - Both arms: make ONE local commit of what steps 2 and 3 changed (`git commit -q -am "s1 replay isolation, experiment only, never pushed"`; T-literal needs no `-a` after `git rm`). Reason: the briefs' README says `git status --short` must show no modified tracked file caused by the worker, so the tree must start clean, as the original did. Record the new `HEAD`. Never push.
   - T-literal check: `git grep -l -E 'orca-worker-contract-spec|spec-panel-round[23]'` prints nothing. (The spec and `commands-b.md` mention `.dev/tasks/to-do/` and `.dev/reflect/` 7 times as output-folder conventions, not as `path:line` citations of files; removing the folders does not break a citation.)
   - Gate G1 (both arms): `rg -c '^## Review Loop' .claude/commands/sc/spec-panel.md` prints `1`; `wc -l < .claude/commands/sc/spec-panel.md` prints `472` (`95f2c6e4`, or T-pinned; `486` on later master because of the inert `--unattended` section). If not, stop.
4. Copy the overlay (starting document and shared inputs): `cp -r <S1>/inputs/repo-overlay/. <worktree>/`. Then `sha256sum .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` must equal the v1 line of `inputs/MANIFEST.sha256`. Create empty `.dev/orca-command-refactor/review/` and `.dev/orca-command-refactor/specs/history/`. `git status --short` must list only `?? .dev/orca-command-refactor/` (the original tree looked the same: only `.dev` untracked, `BO/spec-panel-round3.md:21`).
5. Record the start state: `git rev-parse HEAD`, `claude --version`, the model, `orca --version` if available, `wc -c -l` of the spec.

## 5. The loop (core: 3 reviews, 2 fix cycles)

Each step is a new Orca Task with its own fresh worker session (agent `claude`), dispatched from the replay worktree, exactly like the original. The coordinator writes the task text from the files below; Orca adds its own wrapper and preamble. Follow the guide `orca-ide skills get orchestration` for the verbs; this runbook does not restate flags. Wait for each `worker_done` before the next step. Do not tell any worker anything beyond the task text.

| Step | Task text to dispatch | Tool the worker is told to use | Flags in the text | Output to expect |
|---|---|---|---|---|
| R0 | none: the writer (Task 4) is not re-run; v1 is the input | | | spec v1 |
| R1 review | `B/task-text/T05-R1-reviewer-L11-699ae853.txt` verbatim | `/sc:spec-panel` | `@.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` | `.dev/orca-command-refactor/review/spec-panel.md` |
| R1 revise | `B/task-text/T06-R1-reviser-L10-3bb70411.txt` verbatim | none | | spec edited; `review/disposition.md` |
| after R1 | save `cp` of the spec as `specs/history/spec-v2-after-round1.md` | | | |
| R2 review | `B/task-text/T07-R2-reviewer-L11-aff19d65.txt` if the replay R1 found exactly 24 findings; otherwise `B/templates/T07-R2-reviewer.TEMPLATE.txt` with `{{R1_COUNT}}` filled | `/sc:spec-panel` (same flags as R1) | same | `review/spec-panel-round2.md` |
| R2 revise | `B/task-text/T08-...txt` if the R2 reviewer numbered findings N1-N13 plus 2 citations; otherwise `B/templates/T08-R2-reviser.TEMPLATE.txt` | none | | spec edited; `review/disposition-round2.md` |
| after R2 | save `specs/history/spec-v3-after-round2.md` | | | |
| R3 review | `B/task-text/T09-...txt` if the ids match N1-N13; otherwise `B/templates/T09-R3-reviewer.TEMPLATE.txt` | `/sc:spec-panel` (same flags) | same | `review/spec-panel-round3.md` |
| STOP (core) | after the R3 review is recorded | | | |
| optional extension | R3 revise: `B/templates/T10-R3-reviser.GUARDRAILS-ONLY.RECONSTRUCTED.txt`. Tasks 11 to 17 are not replayed (no panel; 427 cannot act) | | | |

Verbatim means byte-for-byte the file in `B/task-text/`. Fill `{{...}}` only with the numbers/ids that the replay's own reports produced; change nothing else; record every substitution in the run log.

Stop conditions: (a) a review ends with PASS (clean; record M1 = the round number); (b) the third review ends FAIL (cap reached; M1 = none); (c) a worker ends `failed` or `blocked`: record it, do not re-brief, re-dispatch the same task text once as a new Task and record both attempts. No coordinator edits to the spec or reports at any time.

Replicates: D6 needs two replicates per arm, each in its own worktree and fresh sessions, started from the same overlay.

### Arm B (separate, clearly labelled; D4 allows it): 427-specific flags

Same as above, but the R2 and R3 review task text adds the 427 flags to the panel command and nothing else:
- R2 review: `... --re-review .dev/orca-command-refactor/review/spec-panel.md --baseline .dev/orca-command-refactor/specs/history/spec-v1-draft.md` (save the v1 copy to that path in step 4 for this arm).
- R3 review: `... --re-review .dev/orca-command-refactor/review/spec-panel-round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2-after-round1.md`.
Label every result "Arm B: 427 flags added by the experiment".

## 6. What to record per round (M1 to M5)

Write one `metrics.json` per replicate in the same shape as `baseline-metrics.json` (keys `M2` to `M5` per round, `m1_rounds_until_clean_pass`).

| Metric | How, so it is comparable with the baseline |
|---|---|
| M1 | first review whose verdict is PASS; else `null` with reason (cap/failed). Record the verdict line text |
| M2 | from the review's findings list: count all findings, CRITICAL, MAJOR, MINOR; report `critical_plus_major` as the proxy (`baseline-metrics.json` `proxy_definition`). If the 427 grading is in force the report will also grade blocking/minor: record that count separately and say which grading produced each number |
| M3 | for each finding take the reviewer's origin tag (R3-style `Origin:` line, or 427 `origin=changed|unchanged`); group strict / partial / pre-existing as in the baseline; state "read from tag" or "re-derived" |
| M4 | `wc -c -l` of the spec at round start and after each revision; growth % = (after - start) / start; also cumulative vs v1. Compare against +59.6% (after two fix cycles) and +54.2% (after the third revision) |
| M5 | tool calls and tokens per session, same jq as the baseline: `jq -c --slurp '[.[]\|select(.type=="assistant")] as $a \| {turns:($a\|map(.message.id)\|unique\|length), tool_calls:($a\|map(.message.content[]?\|select(.type=="tool_use"))\|length), usage:($a\|group_by(.message.id)\|map(.[-1].message.usage))}' <session>.jsonl`, then sum `output_tokens`, `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`. Plus wall minutes first to last timestamp |
| Reviewer tool mode | per review: did the worker call `Skill sc:spec-panel`, or `Read` the command file (`~/.claude/...` or project `.claude/...`)? This decides whether 427 text could have been loaded (V1) |

Treatment-effect rules are in `DECISIONS.md` D6; this runbook adds none. Thresholds to remember: last-round blocking at most 50% of the baseline's last round (baseline R3: 8 on the proxy, 14 any-severity), growth at most 70% of +59.6% = +41.7%, both replicates in the same direction, effect larger than the replicate spread.

## 7. Validity checks (a failed check voids that replicate for the 427 comparison)

| # | Check | How |
|---|---|---|
| V1 | The 427 text was actually loaded by each review | the report's last line is `verdict: PASS` or `verdict: FAIL` and its header says `review: N of 3`; or the worker's log shows the `## Review Loop` text. A worker that reads `~/.claude/commands/sc/spec-panel.md` gets the pre-427 text, because the machine's install is pre-427. If absent, record "427 not loaded in round N" and treat the replicate as a control, not a treatment |
| V2 | Start document identical | sha256 of v1 equals `inputs/MANIFEST.sha256` |
| V3 | No answer-key access | in the worker logs, no `Read`/`Grep` hits on `spec-panel-round`, `disposition`, `final-diff-review`, `round4-review` outside files the replay itself wrote; T-literal: the isolation check of step 3 passed |
| V4 | Briefs unchanged | diff each dispatched task text against `B/task-text/` or the template; only the listed substitutions (and Arm B's flag clause) differ |
| V5 | Environment recorded | commit, Claude Code version, model, Orca version in the run log; differences from section 2 are listed |
| V6 | Worker isolation | each task ran in its own fresh session; nothing was committed or pushed; `~/.claude` untouched |

## 8. Known differences between original and replay (cannot be removed)

1. Orca wrapper/preamble ids (`term_...`, `task_...`, `ctx_...`, `pasted_content id`) are new per run; the text is the same (masked-id hashes of Tasks 5, 7, 9 are equal).
2. LLM nondeterminism: finding counts and ids will differ; hence the templates.
3. Live Orca `--help` output may differ from build `1.4.237-aidev02.0e4491a95e92`.
4. Whether R2/R3 workers invoke the Skill or read the command file is the worker's choice; the original did both (R1 Skill, R2/R3 Read).
5. R1's any-severity pass bar was not in the brief and its source is unlogged (UNVERIFIED); a replay R1 worker may apply a different bar. Record it.
6. The original workers ran with the user's global instructions of 2026-11-02; today's global instructions (for example the PR #343 blocking/minor rule, present in today's sessions) may differ.
7. The coordinator's mid-loop judgments (stop after R3, targeted rollback) are not replayed.

## 9. If Orca is not available

Workers are plain top-level Claude sessions (spec evidence E2). Open one fresh session per step in the replay worktree, paste the task text, and tell it nothing else. The generated wrapper/preamble and the `worker_done` report are absent; the briefs' sentence "Finish with worker_done --report-path ..." then has no effect. Record this as a deviation (V5); results are usable but the arm is not "same dispatch".

## 10. Baseline files to compare against (do not show to workers)

`baseline-metrics.json`; the original reports in `baseline-outputs/` (`spec-panel.md`, `spec-panel-round2.md`, `spec-panel-round3.md`, dispositions, Task 11/13/15/17 reviews).

## RECREATION GRADE

**B: minor reconstructed parts, listed.**

Verbatim and verified: the starting document (byte-exact, two independent sources); the shared inputs (byte-identical to what the writer read); all 17 briefs (task text verbatim, with jsonl line numbers); the review command and flags per round; the pre-427 command text; the exact original repo commit (`2cb683f5`, from the reflog); the 427 diff (verified to reproduce the `95f2c6e4` file).

Reconstructed or approximate (each listed above):
1. Orca wrapper/preamble ids per run (section 8.1).
2. Briefs T07 to T09 need numbers/ids substituted if the replay finds a different set of findings; Task 10's brief exists only as a RECONSTRUCTED guardrails-only form (`B/templates/`), and only for the optional extension.
3. Evidence tree: exact only in Arm T-pinned (original commit plus the 427 overlay). Arm T-literal, as D4 words it, carries evidence drift (19 of 37 cited command files changed) and an answer key in the tree (178 + 192 files); done without the step-3 isolation, **that arm would grade C**.
4. Not freezable: live Orca help output; global instructions in force in 2026; source of R1's pass bar; the original working tree beyond "only `.dev/` untracked" (UNVERIFIED).
5. Whether 427 text is loaded depends on the worker's choice of Skill versus reading `~/.claude/...` (validity check V1).

No candidate-swap.md is needed (grade is not C or D).

RECREATION GRADE: B
