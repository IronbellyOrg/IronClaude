# S1 ledger variant: validity

Recorder: independent, measurement only (task_2f23e0439839). One replicate. Pointers: REV = `reviews/review/`, LED = `reviews/review-ledger/`, SESS = `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-exp346-v-ledger/<id>.jsonl`, S1V = `exp346-p1-logs/.dev/experiments/346-validation/phase5/s1v-log.md`. Each check is PASS, FAIL or PARTIAL against the REPLAY.md section 7 definition adapted to this variant (the variant command is `/sc:spec-panel-ledger`, not `/sc:spec-panel`).

| Check | Result | One-line reason |
|---|---|---|
| V1 tool load and markers | PARTIAL | Every review and the sweep called the Skill; R3 also read the command file by hand first; R3 has no `verdict:` last line and no Reviser brief (escalated) |
| V2 start and frozen endpoint | PASS | v1 sha256 equals the manifest; live spec = v3 = r3 snapshot = sweep input |
| V3 answer-key exposure (covariate) | PASS (covariate 0) | No step read origin/master, `git show`, `~/.claude/WORKER-CONTRACT.md` or prior-run answers; the file was present on disk |
| V4 briefs | PARTIAL | Hashes match S1V; listed substitutions only, but the T08 range was filled too widely and corrected by a coordinator answer |
| V5 environment and model | FAIL | Review 3, the second half of revise 2 and three scripted steps ran on gpt-6.1-sol after `/model` was typed into the terminals; not recorded in S1V |
| V6 install, isolation, post-delivery | PARTIAL | spec-panel sha256 unchanged, nothing committed, no loop-file edit after its owning step; but people or processes typed into six worker terminals |

## V1 Review-tool load (Skill call vs command-file read) and report markers
Facts per review (SESS tool_use records; REV line numbers):

| Review | Session | Skill call | Command file read by hand | `review: N of 3` | Reviser brief | Last line |
|---|---|---|---|---|---|---|
| R1 (T05) | 82591fac | `Skill sc:spec-panel-ledger` with the brief's args, then `Skill sc-review-ledger` | no | present, line 3 (worker copied it from `status`) and line 138 (script tail) | present, line 160 `### Reviser brief` (script tail; level-3 heading, not `##`) | `verdict: FAIL` (166) |
| R2 (T07) | a1163fbb | same | no | present only in the script tail, line 199 | present, line 237 `### Reviser brief` | `verdict: FAIL` (243) |
| R3 (T09) | 5f820c85 | `Skill sc:spec-panel-ledger` | yes: `Read ~/.claude/commands/sc/spec-panel-ledger.md` BEFORE the Skill call | present only in the script tail, line 246 | absent (cap reached, loop escalated) | `loop: ESCALATE (sweep pending)` (288); no `verdict:` line; body says `**FAIL.**` (189) |
| Sweep (T09b) | 7f1440da | `Skill sc:spec-panel-ledger ... --sweep`, then `sc-review-ledger` | `sed -n '255,265p'` of the same file inside a batch script, after the Skill call | not applicable | not applicable | `verdict: FAIL` (172) |

The `review:` headers, Reviser briefs and verdict lines are written by `review_ledger.py close`/`sweep` (the "review-ledger tail" blocks), not by the reviewers. By design `tail_text` (SCRIPT:1917-1950) writes `### Reviser brief` and `verdict: FAIL` only when the decision is CONTINUE; for ESCALATE or PASS it writes `loop: <decision> (sweep pending)` and the final `verdict:` line goes to the sweep report. So R3's missing verdict line is the script's format, not a reviewer omission. Revisers: T06 grep'ed and sed'ed the command file and read the skill (no Skill call needed for a reviser brief); T08 sed'ed lines 250-275 of the command file and called `Skill orchestration`. No step spawned a subagent (no Agent/Task tool_use; no subagent folders).
Result PARTIAL: the variant text was loaded through the Skill tool in every review and the sweep; R3 read the command file by hand before its Skill call (a read alone would not count as loading the command; here the Skill call followed), and R3's report has no `verdict:` line by the script's design. The R3 reviewer was gpt-6.1-sol (V5), so "the command was loaded" does not mean the same model applied it.
## V2 Start document identity and frozen endpoint
| Artifact | bytes / lines | sha256 | Equals |
|---|---|---|---|
| v1 `specs/history/spec-v1-draft.md` | 57763 / 285 | d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d | `phase2/S1/inputs/MANIFEST.sha256` repo-overlay line; LED/snapshots/r1.md; brief's stated hash |
| v2 `spec-v2-after-round1.md` | 66484 / 288 | 347e32c26f7dc0249df835d8c2557045b60ed7a19c1f3e2a290fd0321234d9bd | LED/snapshots/r2.md |
| v3 `spec-v3-after-round2.md` | 70565 / 288 | 030b7a941cd3498bf3c568232ae039ba2e267bd99c86417708f47add4d6a4e0c | LED/snapshots/r3.md, live `specs/orca-worker-contract-spec.md`, sweep input `/tmp/review-ledger-sweep-3s8rdl6a/orca-worker-contract-spec.md` |

Method: `sha256sum` of the `cp -p` copies in `reviews/` and `cmp` of every copy against its source (no mismatch), 2026-11-09 about 05:14Z. Script check: `post_terminal_edit.changed=false` with doc sha256 = last snapshot sha256 (L7 status). Live file mtime 01:20:28Z (T08's last edit) precedes snapshot r3 (01:36:14Z, L4 `begin`). The original v1 is an untracked overlay absent from commit 2cb683f5, so it was not recovered from git; the identity rests on the manifest hash. No external revision of the live spec in this worktree (unlike the diffgate worktree, S1V 01:30:21Z); no drift flag needed. Endpoint measured = frozen r3.
Result PASS.
## V3 Answer-key / origin/master exposure (covariate)
Method: every tool_use input of the 15 step sessions (this recorder's session excluded) searched with jq for `origin/master`, `WORKER-CONTRACT`, `git show`, `git log`, `git diff ... master`, `spec-panel-round`, `disposition`, `ledger.json`, `plan-r<N>`, `snapshots/`, `specs/history`, `review/spec-panel`.
- origin/master / git: no `git show`, no `git log` of origin/master, no read of origin/master files. Only hit: the sweep's `git log -1 --format='%H %cd'` (HEAD). The sweep's batch script contains the string `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md` quoted from the spec's AC-0.3 text (searched as a literal); its execution as a git command was not confirmed (UNVERIFIED either way, no hit on its output). `origin/master` appears 3-9 times per session file only inside the injected CLAUDE.md text (attachment and api-request-blob entries).
- `~/.claude/WORKER-CONTRACT.md`: present on disk for the whole run (install-log.md; mtime 2026-11-08 07:07:59Z; sha256 now 5fbf2f2e201b...). No step read it. Every `WORKER-CONTRACT` string in the session files comes from the spec text (the spec plans `src/superclaude/core/WORKER-CONTRACT.md`), from the @-attached spec or tool results of spec reads. Phase 4 runs had it moved aside (install-watch.log `absent` during arms); here it was present: a covariate difference, not observed as used.
- Prior loop artifacts: T07 read `review/spec-panel.md`, `disposition.md`, `plan-r2.md`; T09 read `spec-panel-round2.md`, `disposition-round2.md`, `plan-r3.md`. Both are required by their briefs. The sweep read none of them (see metrics.json `sweep.blindness_check`; it listed file names only).
- Findings citing origin/master content: 0 in R1, R2, R3 and sweep.
Result PASS as a covariate (0 peeks). Limit: tool_result content was searched only for the WORKER-CONTRACT string, not for every new-command name.
## V4 Briefs vs canonical text, substitutions, deviations
Dispatched brief files: `/tmp/impl/s1v/briefs/ledger/`. Every sha256 prefix in S1V rows matches the file on disk (T05 e530912504a3, T06 28fdd09ed70b, T07 e6ecb70bbc6c, T08 fc17a83d1dc6, T09 7b2476287eb9, T09b 252f792c6abb, L0 e9702ce7aac8, L1 b28bc9870e0c, L2 93f485a82e16, L3 708cfe80d3c3, L4 0cd46115a2ea, L5 26511cc477a8, L6 34a5b6a2eb63, L7 d22c9baf8e2b). Order and completion: `/tmp/impl/s1v/seq-ledger.txt` and `driver-ledger.log` (SEQUENCE COMPLETE 05:10:39Z). Canonical text: `phase2/S1/briefs/task-text/` and `templates/` (read-only; not modified, mtimes 2026-11-08 02:22-02:25Z).

| Brief | Differences from canonical (diff of the files) |
|---|---|
| T05 | `/sc:spec-panel` replaced by `/sc:spec-panel-ledger --ledger <ledger dir> --revert-unclaimed`; rest identical. Repo root replaced at dispatch (S1V "repo-root subst 1"). |
| T06 | byte-identical to canonical (28fdd09ed70b); repo root replaced at dispatch. |
| T07 | `{{R1_COUNT}}` = 17 (all round-1 findings, including the 4 deferred MINOR); command replaced as in T05. |
| T08 | `{{R2_FIRST_ID}}-{{R2_LAST_ID}}` = R18-R33; "the {{R2_CITATION_COUNT}} overstated citations" = "every overstated citation"; template's "section 5" and "section 3" pointers left as written (the report's findings are in section 3 and citations in section 2; the reviser noted this, REV/disposition-round2.md:43). |
| T09 | R18-R33 and "every overstated citation"; command replaced as in T05. |
| T09b | new sweep brief (no canonical): sweep command on the frozen copy, same output/ownership boundary text as T09. |
| L0-L7 | coordinator scripted-step briefs (no canonical in phase 2); written 2026-11-08 23:48Z before the run. |

Deviation preserved (T08): the coordinator filled the range with R18-R33, wider than the ledger reviser contract (blocking rows only). The reviser asked through `orca orchestration ask` and recommended option (a), apply all confirmed findings; the coordinator answered (b): fix only R18, R19, R21-R25 and give each deferred row a not-answerable disposition row (S1V 00:26:06Z; driver log 00:25:42Z question, 00:26:41Z resume; REV/disposition-round2.md:13-18). Outcome: 7 applied, 9 rejected-deferred rows.
Read-only ownership: no step wrote outside its assigned file(s) by tool_use evidence (T05/T07/T09/T09b wrote only their report; T06/T08 edited only the spec and their disposition; ledger writes were done by L-steps through the script).
Result PARTIAL: briefs are traceable and hash-exact, but the T08 fill was wrong at dispatch and changed by a mid-step answer.
## V5 Environment and per-message model
Claude Code 2.1.319 in all 16 session files (field `version`); git branch `ironbelly/exp346-v-ledger`, HEAD 2cb683f5 throughout. Orca: T09 ran `orca --version` = `1.4.245-aidev02.780594c521aa` (REV/spec-panel-round3.md:8); other steps did not record it. Requested model per D10/D11 and S1V: claude-opus-5-5, "same model" on every resume.

Actual per-message model (`message.model` of assistant entries; `<synthetic>` = 429 error stubs):

| Step | Launch model | Actual messages | Model change evidence |
|---|---|---|---|
| setup, L0, T05, L1, T06, L2, T07, L3, L7 | claude-opus-5-5 | claude-opus-5-5 only | none (L3: `/model` typed after delivery at 01:18:05Z, output "Kept model as `Opus 5.5`") |
| T08 revise 2 | claude-opus-5-5 | 47 opus (00:24:57-00:33Z), 2 x 429, then 43 gpt-6.1-sol (01:17:59-01:22:32Z) | 00:52:18Z coordinator resume text "same model"; 01:17:53Z `/model` -> "Set model to `Tier 1b: Claude Sonnet 5.5, GPT 6.1 Sol, Muse Wonder Full 1.0` and saved as your default for new sessions"; 01:17:55Z `resume` |
| L4 | claude-opus-5-5 (429) | 19 gpt-6.1-sol | 01:35:36Z `/model` Tier 1b; `resume` |
| T09 review 3 | claude-opus-5-5 (429 at 01:42:12Z) | 102 gpt-6.1-sol, 0 opus | 01:59:31Z `/model` -> "Tier 2: GPT 6.1 Sol, GLM 5.3, Grok 4.7, Qwen 3.8 Max, Muse Wonder 1.0, Muse Spark 1.3 ... with `high` effort"; `resume` |
| L5 | claude-opus-5-5 (429) | 16 gpt-6.1-sol | 02:13:04Z `/model` Tier 1b |
| L6 | claude-opus-5-5 (429) | 14 gpt-6.1-sol | 02:23:55Z `/model` Tier 1b; `resume` |
| T09b sweep | claude-opus-5-5 | 6 x 429 (02:39-04:32Z), then 47 opus (05:00:36-05:09:09Z) | six coordinator resumes "same model"; no `/model` |

Mismatch with prose: S1V says "same model" (00:52:31Z row) and "no model substitution" (sweep rows), which is true for the sweep but not for T08, L4, T09, L5, L6. S1V does not record the five `/model` commands. Who typed them is UNVERIFIED (they are local terminal commands, recorded as user entries in each session). Consequences: the whole round-3 review (the R3 proxy) and the second half of revise 2 came from gpt-6.1-sol (T08 Edit/Write calls by timestamp and message model: spec 8 by opus 00:29:09-00:30:14Z and 5 by gpt-6.1-sol 01:18:41-01:20:28Z; disposition-round2.md 1 opus stub write and 9 gpt-6.1-sol edits ending 01:22:11Z; call attempts, individual success not checked), a non-Claude model reached through the Tier routing, not from claude-opus-5-5 as in every control and Arm B step. Token fields from gpt-6.1-sol report `cache_creation_input_tokens` 0 and large `input_tokens`, so token totals are not comparable across providers.
Worker system prompt (blocking/minor rule, 3-review cap): not present in session files; not measured.
Result FAIL (model not held constant; undocumented in the run log).
## V6 Install state, isolation, post-delivery edits
- User-level command text: install-log.md records `spec-panel.md` before = after = 4115f2a979800af8... and the additive variant files (spec-panel-ledger.md 4624c31f3375..., review_ledger.py 2d45c85a4edc...). On 2026-11-09 05:14Z the same three hashes are on disk (`sha256sum`), with mtimes 2026-11-08 07:07:59Z (spec-panel.md) and 23:42:21Z (variant files), before the first ledger step (23:44:50Z). No change during the run. The phase-4 watcher log (`phase4/install-watch.log`) ends 2026-11-08 13:57:47Z and does not cover this run: monitoring gap, covered only by the start/end hash equality and mtimes (an edit-and-restore inside the window would not be visible).
- `~/.claude/WORKER-CONTRACT.md`: present (phase 4 arms had it absent). See V3.
- Git: HEAD 2cb683f5 unchanged; reflog shows no commit after 2026-10-30; `git status --short` shows only untracked `.dev/experiments/` and `.dev/orca-command-refactor/`. Nothing committed or pushed from this worktree by evidence available here.
- Post-delivery edits to loop files (mtime vs owning step end): spec-panel.md 23:58:20Z (L1 close tail, L1 ended 23:58:46Z); disposition.md 00:10:27Z (T06 ended 00:10:44Z); spec-panel-round2.md 00:23:29Z (L3 close, ended 00:23:46Z); live spec and history v3 01:20:28Z (T08, ended 01:22:32Z; history copied with `cp -p` at 01:22:30Z); disposition-round2.md 01:22:11Z (T08); spec-panel-round3.md 02:13:40Z (L5 close, ended 02:14:44Z); spec-panel-sweep.md and ledger.json 05:10:11Z (L7 sweep ingest, ended 05:10:41Z). No loop file changed after the step that owns it; script tails intact (`tails_intact=true`). The sweep copy in /tmp has mtime 02:24Z (L6 prepare) and the r3 hash.
- Typing into worker terminals: coordinator resume prompts in T08 (00:52:18Z) and T09b (02:41Z to 04:59Z, six) are logged in S1V. Not logged: `/model` plus `resume` in T08 (01:17:53Z), L4 (01:35:36Z), T09 (01:59:31Z), L5 (02:13:04Z), L6 (02:23:55Z), and `/model` in the already finished L3 terminal (01:18:05Z). These changed the model mid-task (V5). Actor UNVERIFIED.
- Re-dispatch: none; T08 and T09b were resumed in the same session and dispatch (driver log "resuming wait on existing dispatch").
Result PARTIAL: install state and loop files held; terminals were touched outside the logged resumes.
## Failed validation attempts (negative evidence)
1. First batch extraction of session metrics wrote its output under a private /tmp directory that its exit trap removed; the full output survived only as the harness's persisted tool result (`cb9e31be.../tool-results/bt94g0svm.txt`). Numbers were taken from that file; not a data problem, recorded for traceability.
2. Who typed the `/model` commands: searched S1V, driver-ledger.log and the session files; the commands appear only as local terminal commands with no author field. UNVERIFIED.
3. The worker system prompt (whether it carried the blocking/minor rule and the 3-review cap): not stored in the session files; not measurable from here.
4. Install monitoring during this run: no watcher log exists for 2026-11-08 23:42Z to 2026-11-09 05:10Z (phase4/install-watch.log stops 13:57:47Z). Only start (install-log.md) and end (05:14Z) hashes were compared.
5. Execution of `git diff -U0 master...HEAD` inside the sweep's batch script: the string is present; whether it ran as a command or was only a literal search string was not resolved from the bounded extract.
6. Control R3 reviews were full-document panels; the ledger R3 new-defect pass is hunk-limited. No way exists in the data to count what a full panel at R3 would have found in this run, except the sweep (a separate blinded session on claude-opus-5-5, whose R3-equivalent view differs from the R3 reviewer's).
