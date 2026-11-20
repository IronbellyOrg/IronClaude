4bf8f84e56b01a644fcb81014084a87af9447026
Review one task for spec compliance.

Task brief:
## Task 6: Write the governed session scripts B to E

Depends on: Task 5

Create `.dev/issues/442/scripts/session-gov.sh` with subcommands `b`, `c`, `d` and `e`. Each subcommand follows its runbook section in order, and its prompt files go in `.dev/issues/442/scripts/prompts/`, copied byte for byte.

Session `b` (section 2.2.1, lines 536-642):
- Step 1 first makes the backup itself: `cp "$WT_T1/.claude/settings.local.json" /tmp/ob/t1-local.json` (runbook:541); it refuses to continue when that copy is missing or empty. Then it runs the two preflight refusals: it writes the bad JSON and then `disableAllHooks` into `$WT_T1/.claude/settings.local.json` from its own shell, sends the claim to the claim session, and runs the three checks at lines 549-551 after each refusal. It then restores the file from `/tmp/ob/t1-local.json`; the restore never runs when the backup step failed. A self-test asserts the restored file is byte-equal to the backup.
- The real claim follows. The governed terminal handle is the `terminal` key of the claim result, set from the recursive `handle` search (`orca_worktree.py` lines 49, 1031-1046, 1289, 1313), read from the claim output or the `launch` record of `.dev/issues/<T1>/worktree.json`, and recorded with `driver.sh adopt`. Fallback: when the claim output lacks `terminal`, the script records the whole record in the run log and stops for the operator.
- `GSID` is read from the probe log.
- Step 3 sends the prompts at lines 586, 592 and 598, then repeats the commit prompt.
- Step 4 sends the prompts at lines 606, 610, `/clear` and 625, and runs the `identify` checks at lines 616-620 and 629-633. It then follows the runbook's mid-step order exactly: the guarded release `rm` for this run's recorded `GSID` runs at line 635, before the final `identify` at line 638 on `sleep 241`, which must print `ordinary` with reason `released`. OB-CTX needs that case recorded (line 641); without it the item can never reach PASS.

Session `c` (section 2.2.2): it sends the `/sc:implement <plan path>` prompt, using the plan path read from the screen, and then the commit prompt.

Session `d` (section 2.2.3): it sends the claim with `--pipeline full`. It waits up to 90 minutes for the agent's final `git status --short`, then sends the commit prompt.

Session `e` (section 2.2.4, lines 657-697):
- It sends the claim with `--pipeline full --submit`. It checks that the pull request URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`, and stops with `FAIL misrouted-pr` if it does not.
- For O-10, during monitoring, it changes `ob-442/T4.txt` on the pull request branch with `gh_fork api -X PUT repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt`. This stands in for the web UI edit; whether `/sc:pr-submit` reacts the same way is UNVERIFIED, and the step's result says so.
- O-10 edit trigger: the `gh_fork api -X PUT` fires once the pull request URL first appears in the governed session's screen or its `h2-T4` log, and only then. Cycle end: the cycle counts as ended only after a `Stop` event follows the `/sc:pr-submit` final report in that log, bounded by a timeout that leaves the O-10 count `pending` on expiry.
- Before the push setup it records `worktreeConfigPre=true|unset` in the state file, reading `git -C "$WT_T4" config --get extensions.worktreeConfig` first, so cleanup step 3 unsets the key only when this run set it.
- After the cycle it runs the push URL commands at lines 668-672. It sends the push prompt (line 678) only after re-checking inline, immediately before the send, that `git remote get-url --push origin` in `$WT_T4` prints `/tmp/ob/bare-push.git` (a run-time check in the script, not only a self-test case), then sends the merge prompt (line 684) and runs the restore at lines 690-691.

Release:
- Subcommands `c`, `d` and `e` end by running the claim's printed `release` `rm` line from the script's shell; session `b` releases mid-step 4 at runbook line 635, as its step 4 says. Release is idempotent: an `rm` whose target is already absent counts as released, never as an error.
- It runs that line only when the path is `~/.claude/state/launch-level/sessions/<GSID>` or `<GSID>.ok` for this run's recorded `GSID`.

Stop rules: every subcommand (`b`, `c`, `d` and `e`) at entry reads OB-H1 item 5 from the results file and refuses to launch unless it is PASS; `d` and `e` also require item 1 PASS (runbook section 3.3, lines 720-726).

Acceptance criteria:
- [T6.AC1] With the stub `orca` and `gh` and scripted screens, the self-test shows session `e` refusing the push prompt when the push URL is not `/tmp/ob/bare-push.git`, and refusing a pull request URL outside `IronbellyOrg/IronClaude`.
- [T6.AC2] The self-test shows the release step refusing an `rm` path that is not this run's `GSID` or its `.ok` file, and treating an already-absent target as released.
- [T6.AC3] The self-test shows `b` and `c` refusing to start when item 5 is not PASS, and `d` refusing when item 1 is not PASS.
- [T6.AC4] Every prompt file matches its runbook `text` block byte for byte (a self-test diff over lines 536-697).

Global constraints:
## Constraints

- Owner authorization (2026-11-08, this session): an agent may start Claude sessions for the observations and run governed claims on the four disposable issues T1 to T4 only. Creating those four issues (Task 5) and the one disposable pull request (session `e`), both on `IronbellyOrg/IronClaude`, is inside this authorization; the owner's execution order of 2026-11-09 confirmed it. No claim, launch or comment on any other issue. The runbook's section 3 gate still holds: no governed claim on a real issue, whatever the results.
- GitHub: every `gh` call passes `--repo IronbellyOrg/IronClaude`; every `gh api` path spells `repos/IronbellyOrg/IronClaude/...`. Nothing ever targets `SuperClaude-Org/SuperClaude_Framework`. No Orca `--issue` or `--pr` flag. Never `gh pr merge`.
- Python only through `uv run`. Worktrees only through Orca (the claim creates them; cleanup removes them with `orca worktree rm`).
- Safety list of runbook section 5.1 (lines 773-783) applies to every script: no probe in the real `~/.claude/settings.json`; no prompt starting with `[sc-launch:v1:`; a marker inside a prompt only at the LL-NOBIND step of session A; no `superclaude install` during the run; the claim session starts with `env -u CLICKUP_API_TOKEN claude`; no script prints or logs `env` output or a token.
- Settings, hook, git config and launch-store changes are made by the scripts from the driving agent's own shell, never by a prompt typed into an observed Claude session (LL-TAMPER).
- Terminal injection is representative: a prompt sent with `orca terminal send` reaches the hook as the same UserPromptSubmit payload as a typed one (hook payloads carry no origin field, design V6). An agent sending `approved` is therefore the R15 risk the design names; it is allowed here only because the owner authorized it for T1 to T4.
- Orchestration skill: investigated and not used. Evidence from the version-matched guide (`orca skills get orchestration`, read 2026-11-08): `worker-start` injects a lifecycle preamble as the first prompt and obliges heartbeats and `worker_done`, which would change the very UserPromptSubmit and PreToolUse payloads under observation and, in a governed session, add Bash calls the guard judges; governed sessions must come from the claim's own `orca agent launch --surface terminal` with a leading marker (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` docstring line 46), and a second launch path would not test it; the guide's own routing sends terminal control, lightweight prompts and reading or waiting on terminals to `orca-cli`; and this session is a settled dispatched worker whose lifecycle IDs must not be reused (guide lines 100-101). The independent check of each task is already the `/sc:implement` reviewer, so a supervised Orca reviewer would add nothing. The driver uses plain `orca terminal create|send|read|wait|list|close`.
- Every script: bash, `set -u -o pipefail`, `umask 077`, and every external call bounded by `timeout`. An item without evidence is `pending`, never PASS.
- Scripts live in `.dev/issues/442/scripts/` of this checkout; scratch state stays under `/tmp/ob` as the runbook defines. No change to `src/` or `tests/`.

Start sha: 4bf8f84e56b01a644fcb81014084a87af9447026
Diff against the start snapshot:
There is no usable git diff (the delivery files are untracked in this worktree; the start sha above is the snapshot tree of the task start). Review the CURRENT contents of these files (read them with Read; they include edits made by later tasks, and you judge only this task's acceptance criteria). Paths are relative to /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook:
.dev/issues/442/scripts/session-gov.sh
.dev/issues/442/scripts/session-gov-selftest.sh
.dev/issues/442/scripts/selftest.sh
.dev/issues/442/scripts/prompts/g01-b-implement.txt
Evidence artifacts of this task and the package logs are under /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ (t6-selftest.txt and, where the plan names them, other logs). Do not read artifacts/retries/ or .dev/troubleshoot/.
Delta diff from the previous reviewed tree (empty on the first review):
Earlier blocking findings of this start (empty on the first review):
Saved-probe re-check hit locations (may be empty):

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
