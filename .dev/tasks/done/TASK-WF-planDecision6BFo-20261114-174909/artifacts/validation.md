# Stage 1 validation: Decision 6 = B (coordinator starts the plan-writing agent as a supervised worker)

Session: top-level design session, worktree `claim-handoff-b`, branch `ironbelly/claim-handoff-b`.
Base: `0406ef5b0` (= `origin/master` after `git fetch origin master`; status clean). Written 2026-11-14.
Read-only throughout: Orca `status`, `worktree list`, `worktree ps`, `skills get`, `--help`, `worker-list --help`, `run-current` (reply: `run: null`); `gh pr view 548` (GET). No agent started, no write verb run.
Evidence tags: V = read in a file or command output (file:line); M = measured read-only; U = UNVERIFIED (could not read or run it).

## VERDICT: works with changes, and one genuine owner choice blocks the plan (gate fired)

B's message route works as described on paper: `ask` and `reply` exist, the worker contract already gives them rules (V WORKER-CONTRACT.md:53-58, :61). But B collides with the launch-level guard (`launch-level-guard.sh`) in two places, and the two ways out are different designs with different safety. The brief says to stop at this gate. Stage 2 is not run.

### The collision (the finding that matters)

Today the claim's agent is "governed": its first prompt carries `[sc-launch:v1:<nonce>]`, the guard binds the session, and from then on the guard blocks commits, pushes, merges, GitHub writes and `/sc:implement` until a person approves (V launch-level-guard.sh:42-113, :318-330, :376-387; V orca_worktree.py:1762-1765).

1. A governed session cannot use the Orca verbs a worker needs. The guard classes any `orca` command as ESCAPE (blocked) except `status`, `help`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show` (V launch-level-guard.sh:458-478; message V :86-89). `orchestration send` (heartbeat, ack, `worker_done`) and `orchestration ask` are not on the list. So a governed worker could not heartbeat, ask or finish.
2. A governed session is released only by a user prompt: the whole prompt is `approved`, or its first line starts `/sc:implement`, `/sc:task` or `/task` (V launch-level-guard.sh:347-364). Under B the approval arrives as the result of the worker's own `ask` call, not as a user prompt, so the guard never records the approval (the `.ok` file, V :270). A governed worker would stay blocked from `/sc:implement` after approval.
3. If the worker is NOT governed (no marker in its prompt; the guard treats it as an ordinary session and never blocks it: V launch-level-guard.sh:366-368, header :4-7), there is no L1 guard at all. The L2 pre-push hook also only refuses a push to `main`/`master` for a governed actor or an unknown actor, and lets an ordinary push through (V launch-level-pre-push.sh:3-10). So the only limits left are the worker contract's text (WC-9: no push, PR, merge, GitHub post; V WORKER-CONTRACT.md:41), which is an instruction, not a block. The session runs with permission checks off (see Q5).

Two designs, and the owner has to choose (new Decision Q34, below):
- **G1, ungoverned worker.** Simplest. No guard code change. The owner accepts that a permission-free worker reading untrusted issue text is held back only by the contract text. Decision 1's written acceptance ("Accept off", both sessions) covers permission checks, not the loss of the guard; this is a bigger acceptance than Decision 1 states.
- **G2, governed worker.** Keep the guard. Needs a change to the guard script and its tests: allow `orchestration send|ask` (and `worker_done`) for a bound session, and accept the coordinator's approval as the release (for example through the same signed `approved <record-id> plan-sha256=<hash>` line the worker already checks, written to the session's `.ok`). Bigger change, touches a security hook, needs its own review (hook tests: tests/hooks/test_launch_level_guard.py and the five sibling files).
- Recommended: G1 for the one test issue only, with the added written acceptance, then G2 before the flow is used on any other issue. Default if unanswered: B stays unbuilt.

---

## 1. The B flow, step by step (plain words)

1. Watcher cycle claims an approved issue: it launches `/sc:issue --claim <N>` (no `--pipeline`) in the watcher's configured worktree through `orca agent launch` (V launch.py:84-116; V cycle.py:1054, :1099). The claim session runs at its default `worktree` level (V issue.md:43).
2. The claim (Waves 0-6) checks Orca, resolves the repo, assigns the issue, writes `scout.md`, `accuracy-check.md`, `issue-summary.md`, `recommend.md`, `next-steps.md`, posts two comments, all under `<watcher worktree>/.dev/issues/<N>/` (V SKILL.md:84-90; issue.md:77).
3. Today Wave 7 creates or reuses worktree `issue-<N>` and copies the folder in; Wave 8 launches the governed agent (V SKILL.md:91-92; orca_worktree.py:622-735, :1682-1820). Under B this changes (question 3).
4. The coordinator (person-opened, Decision 7) adopts the issue: it takes a per-issue lock, writes the approval record helper's first row, then starts the worker with `orca orchestration worker-start --spec <brief> --worktree path:<absolute issue-N path> --agent claude --json` (help text V: `--worktree` accepts `path:<path>`; "Current and existing worktrees never rerun setup; a fresh agent terminal is created"; exact-existing placement is also what the guide's placement reference describes). Receipt shape is U (question 7).
5. The worker's Task spec (the guide's contract: target, change, constraints, ownership, observable acceptance) names: the issue's folder, the plan commands to run up to the `Plan boundary` line, the report directory, `Local commit: not authorized`, `Outward actions: none`, and `On a blocked gate: report blocked` (V WORKER-CONTRACT.md:296-307).
6. The worker runs each plan command through its Skill (WC-7), writes the plan under its report directory (and `handoff/` notes, WC-15), and computes the plan hash.
7. The worker never posts to the issue (WC-9, V :41). It asks the coordinator with `orca orchestration ask --from <handle> --question "plan ready at <path>, sha256 <hash>: may I proceed?"` and waits (guide: ask timeout 10 min default, 30 max; resume by message ID; no heartbeat while blocked in `ask`; V WORKER-CONTRACT.md:58, guide worker-contract reference).
8. The coordinator reads the plan, posts the plan reply and the assignee mention on the issue (its own write under the pipeline grant row, Decision 8), moves Status, and waits for the assignee's approval label (Decision 3) or a person's approval in Orca. It re-reads GitHub at each check.
9. On approval it writes the record to disk first, then `reply --id <message_id> --body "approved <record-id> plan-sha256=<hash>"`.
10. The worker recomputes the hash, refuses on a mismatch, otherwise sends `status` with body `ack <message_id> applied` (V WORKER-CONTRACT.md:61) and continues with the commands after the boundary (still no commit, no push).
11. The worker writes its contract and sends one `worker_done` (WC-5, V :59). The coordinator opens the contract, mirrors label and Status, then releases or reuses the worker.

Who posts the plan reply: the coordinator, never the worker (WC-9, WC-13 V :41, :62). Whether `reply` stores type `status`, so a waiter with a narrow `--types` list can miss it, is an open lead in the contract itself (V WORKER-CONTRACT.md:196); the worker's `ask` is blocking, which should not depend on `--types`, but U until measured (FU-1 item c).

Gap found in step 5: `next-steps.md` is written for a person or a governed agent (V templates/next-steps.md). A worker needs `Command:` lines with `--unattended` and one report directory each, and passes a two-copy test per command first (V WORKER-CONTRACT.md:217-227). Several chain commands are not in the default converted set until a phase 2 live check passes (`/sc:troubleshoot`, from P2; V :313-314). And the chain commands carry issue-derived text (`"<topic> @<S>"`, `<symptom>`; V refs/chains.md), while merged spec 6.4 rule 9 says issue text never becomes a worker's command line. Fix to plan: the coordinator builds `Command:` lines from fixed templates that name the summary FILE (`@.dev/issues/<N>/issue-summary.md`), not issue words. Which chains are allowed at all is part of the plan, and `/sc:implement` is excluded from the first worker (it comes after approval).

## 2. How approval is bound to the plan version

Design (V merged-proposal.md "Design" item 3): plan version = SHA-256 over a named, ordered list of plan files; the coordinator prints the list and the hash in the plan reply; the record row holds it; the `reply` body is `approved <record-id> plan-sha256=<hash>`; the worker recomputes with the same function and refuses a mismatch or a bare `approved`. This is checkable and uses no Orca fact beyond `ask`/`reply` carrying a body. One extra rule B needs: the list of plan files must live inside the worker's report directory, so the hash input is exactly what WC-4 names. Not built: the hash function, the helper, the worker's check (all new; no Orca dependence, so they can start now).

## 3. The claim-side change B needs

Facts: `--pipeline none` stops after the comments, creates no worktree and launches no agent (V issue.md:16, :43, SKILL.md:90). Wave 7 is `orca_worktree.py worktree`: it looks the worktree up by marker/record/basename/branch, creates `issue-<N>` with `orca worktree create ... --no-parent` and no `--agent`, closes the plain first tab, copies `.dev/issues/<N>/` file by file with symlink and tracked-file guards, writes `worktree.json` (V orca_worktree.py:20-37, :436-501, :622-735). The watcher's prompt is pinned: `PROMPT_PATTERN` (V launch.py:33), `build_claim_prompt` (:84-92), 12-element argv (:95-116), `retry_argv` (:119-132).

### B1: watcher claims claim-only (`--pipeline none`); coordinator creates the worktree itself and copies the files
- Files: `launch.py` (pattern, builder), `docs/designs/issue-watcher.md`, `issue-watcher-setup.md`, coordinator protocol text. No claim code.
- Variant B1a (coordinator uses `worker-start --worktree new-top-level --name issue-<N>`): the worker starts before any copy can happen, so the files must be read from the watcher worktree by absolute path (cross-worktree read), and Wave 7's reuse lookup and guards are not applied; a second claim of the same issue could make `issue-<N>-2`. Rejected.
- Variant B1b (coordinator runs the EXISTING `orca_worktree.py worktree --repo --number --base --source` from the installed skill, then `worker-start --worktree path:<that path>`): no new claim code; Wave 7's tested behaviour is kept (including closing the plain first tab, so `worker-start` makes the only terminal). Costs: an LLM coordinator runs a skill script by hand; the script writes `worktree.json` into the watcher worktree's `.dev/issues/<N>/`. `uv run python ...` is not caught by the worktree-create hook (V require-orca-worktree-agent.sh:60 comment: scripts that call Orca themselves are outside it).
- Tests pinned that change: `tests/issue_watch/test_launch.py` `test_ac7_prompt_accepts_only_the_int_nine__fr012_nfr001` (:41), `..._launch_argv_equals_the_literal_twelve_elements__fr013` (:75), `..._retry_argv_puts_retry_launch_right_before_json__fr015` (:152), `..._launch_argv_has_no_extra_flag__fr013_t10` (:102); `tests/issue_watch/test_security_invariants.py` `test_prompt_regex_property` (:451) and the hostile-input tests (:522, :584, :621); `tests/issue_watch/test_no_text.py`, `test_cycle.py`, `test_cli_e2e.py` (they quote the prompt; 113 mentions of the prompt strings across 11 files).
- `retry_argv` and `dispatch.json`: the retry argv is the same launch with `--retry-launch <id>`; only the `--prompt` text changes. The at-most-once store (`dispatch.json`, `record.py:281`) is untouched: one entry per issue, `claimed` terminal. Pending entry is written before the launch (V cycle.py:1091-1092). Unchanged guarantees.
- Decision 1: the claim session still runs permission-free (first session, unchanged). The second session is a worker under G1/G2.

### B2: a NEW claim level that creates or reuses the worktree and copies files but launches no agent; the watcher passes it
- Files: `commands/issue.md` (flag table, STOP rules, outputs), `skills/sc-issue-protocol/SKILL.md` (Waves 6-8), `refs/claim.md` (final output), `scripts/orca_worktree.py` (`--level` choices at :1859, :1869, `cmd_prompt`/`cmd_launch` gating), watcher `launch.py` as in B1, docs, the protocol copy installed under `~/.claude`, and `make sync-dev` mirrors (never staged).
- Tests: everything in B1 plus `tests/skills/test_issue_protocol.py` (27 mentions of the flag/levels), `tests/skills/test_issue_orca_worktree.py`, `tests/commands` for the flag table, and the return-contract fields (`pipeline_level`, `worktree_status`, SKILL.md:124-130).
- Pro: one tested path creates the worktree whoever runs the claim; the claim stays self-contained for a person without a coordinator. Con: a fourth level to name, document and test, a larger watcher-visible contract change, and a claim that creates a worktree and then no agent contradicts the project rule that every worktree gets an agent (the coordinator's `worker-start` supplies it a moment later; if the coordinator is down the worktree sits empty).

### Recommendation: B1b
Smallest code change (watcher prompt pin only, which WA-01 already recommended as `--pipeline none`), reuses the one tested worktree step, claim command untouched. Revisit B2 only if the owner wants a person to run a claim without a coordinator and still get a worktree. Under B1b the claim's ship gates (OB-H1 item 1, OB-H2, OB-H3) stop applying to the first session because no governed claim runs; they come back as G2's prerequisites.

## 4. What the coordinator must do, and what its spec already covers
Read: merged-requirements.md 2.3 (lines 283-327), 6.3 (956-969), 6.4 (971-988), 6.8 (1042-1050). Not read in full: 6.x beyond these; SW-13's own text.
- Already covered: keeps a ledger; creates worktrees with agents and owns them; writes briefs from the template; reads results from disk; tracks PRs; never merges or posts without a grant row (6.3 coordinator row); workers never create worktrees or dispatch (6.4 rule 4); permission mode of every started session needs written acceptance (WA-07 (4), 6.4 rule 10).
- Partly: WA-07 is "DEFERRED: watcher hands an approved issue to an orchestrator", blocked by SW-13, SW-12, SW-10, WA-04 (V line 309). B makes it live, so it moves out of "deferred".
- New: adopt a claimed issue (discover via `.dev/issues/<N>/worktree.json` or Orca; reliability U, V merged-proposal.md "What stays unresolved"); lock per issue; approval-record helper; plan reply and mention; read GitHub at each check (stage-status verb); start the worker; answer the `ask`; mirror label and Status; revoke; a pipeline grant row per issue (6.8's table is per item and per action; a per-issue pipeline row is new); the brief builder from fixed templates (gap in 1); handling of "plan reply posted, then the label on a reused issue".
- Contradiction to settle in the plan: WORKER-CONTRACT.md puts `/sc:issue` on the never-as-worker list (:23). B runs the claim in the watcher's own session (not a worker), so no conflict; but the worker then runs `next-steps.md` steps, never `/sc:issue`.

## 5. Permission mode of a `worker-start` Claude session
- Verified: Orca's configured Claude command on this host is `ccsession-orca` (V ccsession-orca header; 37 mentions in `~/.config/orca/logs/daemon.log`, M). Its own comment says "Orca also starts supervised workers with this command" (V ccsession-orca lines 35-38). `ccsession` always adds `--allowedTools=Grep` and, unless `CCSESSION_PERMISSIONS=default`, `--dangerously-skip-permissions` (V ccsession:119-120, :137-138). Running Claude sessions here show exactly those flags (M `ps`, pid 21959 and four more).
- So a worker launched by `worker-start --agent claude` should run with permission checks off, same as the two earlier fresh sessions.
- UNVERIFIED: that `worker-start` (as opposed to `agent launch`) goes through the same command; the real argv of a worker; whether `CC_CLAUDE_FLAGS` or `CCSESSION_PERMISSIONS` is set in the environment Orca gives a worker. Step: FU-1 item (a) below, `ps` on the started worker.
- Note: `ccsession-orca` fails a supervised worker whose Claude is not ready in 60 s (V ccsession-orca header). A Session Name question is skipped when a task/prompt is carried (V :71-76), so a worker should not stall there; U until seen.

## 6. Visibility to `worker-list`, the sweep and the dashboard
- A `worker-start` worker is a Dispatch on the coordinator's Run, so it should appear in `orchestration worker-list --run <id>` with `projection.liveness` (V guide; help V). The dashboard reads `worker-list` pages (V observe/adapter.py:29, :194, :362) and the sweep's worker rows come from the same data per merged spec. The plan-reply "agent" looks like any worker: its status, heartbeat token, Task title.
- Today the watcher-launched claim session is Run-less and shows as `could not determine` (V merged-requirements.md:291). Under B the claim session stays Run-less; only the second session becomes visible. UNVERIFIED: the exact row fields for a worker in this build (no live worker exists to read: `run-current` returned `run: null`).

## 7. What the first live test (FU-1) must measure before B is trusted (each a precondition)
| # | Precondition | Exact step |
|---|---|---|
| a | `worker-start` argv and permission flags | after one throwaway test start: `ps` the worker's process; record `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS`; compare with Decision 1's acceptance |
| b | `worker-start --worktree path:<existing worktree a script made>` works and creates exactly one terminal | run it on a throwaway worktree created by `orca_worktree.py worktree`; read `terminal list` before and after |
| c | `ask`/`reply` round trip for a worker started with a prompt (spec) | test worker asks; coordinator `reply`; worker's `check`/ask result shows the body; also whether `reply` arrives as type `status` and a narrow `check --wait --types` misses it |
| d | the launch receipt shape and Dispatch id | read the `worker-start --json` reply; pin as a fixture |
| e | the plan hash survives (the worker and the coordinator compute identical hashes) | unit test, no Orca |
| f | guard interaction (G1 or G2) | with G1: start the worker with no marker and confirm no guard binds (`ls ~/.claude/state/launch-level/sessions` unchanged); with G2: confirm `send`/`ask` blocked today, then after the guard change allowed |
| g | `ask` timeout and resume by message ID | let one `ask` time out; resume with `--resume <message_id>` |
| h | coordinator down while the worker waits | stop the coordinator wait; confirm the worker stays in `ask` (and that `worker-list` shows it alive) |
| i | worktree reuse | run the claim twice for one issue number; confirm one `issue-<N>` only |
| j | stage-status facts from Q02 step 2 (who moved a Project Status; label events) | read-only GitHub reads, as listed in final.md section 6 step 2 |

## 8. What B removes and what it does not fix
Removes: typing the approval line into the agent's waiting prompt (route A) and its exception to "never answer a person prompt" (V WORKER-CONTRACT.md:121, :136); with Decision 9, plain `approved` in the agent's session (once B's route works; under G1 there is no guard hook left to honour it anyway).
Does NOT fix: forgery of the approval label on one GitHub login (Decision 4, accepted); the first claim session running permission-free over untrusted issue text (`--pipeline none` removes only the second agent; V merged-requirements.md:314); coordinator down means no progress (Decision 5); same-host sessions typing into the coordinator terminal (U); a worker's `ask` waiting up to 30 min per round; the guard gap above.

## 9. Risks and mitigations
- Coordinator down: nothing starts; the worker waits in `ask`; on return the coordinator reads its record, resumes the message ID.
- Worker dead: Orca stall proofs only (WC-6, V :73-79); record shows "recorded, not delivered"; no automatic relaunch.
- Duplicate dispatch for one issue: lock per issue plus write-ahead record row before `worker-start`; the row key is (issue, stage, plan version); `dispatch.json` stays at-most-once for the claim itself.
- Plan edited after approval: the worker recomputes the hash; a mismatch is refused.
- Worktree reuse collision: B1b reuses Wave 7's lookup (marker, record, basename, branch).
- Same login for both channels: Decision 4 accepted; stage predicates still check order and edits.
- `ask` timeout: resume the same message ID (V WORKER-CONTRACT.md:58).
- New: ungoverned worker (the gate above); issue text reaching a worker command line (gap in 1).

## Facts not verified
No worker exists to run `worker-start`, `ask`, `reply` against; every Orca runtime fact in section 7 is U. `next-steps.md` chain commands' unattended support for P2 commands is U until their live check.
