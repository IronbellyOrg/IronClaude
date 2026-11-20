a4bb361e1c6375fe1dedddd00ccf6192329f8a51
Review one task for spec compliance.

Task brief:
## Task 9: Update the runbook and its handoff for the scripted path

Depends on: Task 7, Task 8

Edit `.dev/issues/442/observation-runbook.md`:
- Replace the two wrong statements: prompts are not representative of typed ones (runbook:765) and the claim's release `rm` must be run by a person (runbook:769). Prompts sent with `orca terminal send` reach the hooks as the same payload as typed ones, so injected prompts are representative. The LL-TAMPER block applies only to a governed session, so the claim's release `rm` is run from the driving agent's own shell.
- Update the neighbouring statements the scripted path makes partly false: the web-UI-only edit at runbook:767 (the script uses `gh_fork api -X PUT`) and any remaining person-only wording in lines 764-769.
- Change the "Starting the sessions" bullet (runbook:764) to record the owner's authorization of 2026-11-08 for T1 to T4.
- Add a section `## 6. Scripted path` that names each script in `.dev/issues/442/scripts/`, the order to run them in, the `--apply` rule of the cleanup, and the `NEEDS_INPUT` and `BLOCKED login-isolated-home` stops.

Add a short paragraph to `.dev/issues/442/handoff-runbook.md` under "What is left": the scripts exist, and the live run is this plan's Task 10.

Acceptance criteria:
- [T9.AC1] The old wording is gone: `grep -n 'not representative' .dev/issues/442/observation-runbook.md` prints nothing (it also prints nothing before the edit, so the real check follows), `grep -n 'must be.*typed by a person' .dev/issues/442/observation-runbook.md` prints nothing, and `grep -c 'orca terminal send' .dev/issues/442/observation-runbook.md` is at least 1; the last two fail before the edit, so the check cannot pass vacuously. Section 6 names every script file that exists in `.dev/issues/442/scripts/` (a self-test case compares the two lists).
- [T9.AC2] `bash .dev/issues/442/scripts/selftest.sh` still prints `SELFTEST_OK` after the edit, because the prompt and filter diffs read the edited runbook.

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

Start sha: a4bb361e1c6375fe1dedddd00ccf6192329f8a51
Diff against the start snapshot:
There is no usable git diff (the delivery files are untracked in this worktree; the start sha above is the snapshot tree of the task start). Review the CURRENT contents of these files (read them with Read; they include edits made by later tasks, and you judge only this task's acceptance criteria). Paths are relative to /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook:
.dev/issues/442/observation-runbook.md
.dev/issues/442/handoff-runbook.md
.dev/issues/442/scripts/runbook-selftest.sh
.dev/issues/442/scripts/selftest.sh
Evidence artifacts of this task and the package logs are under /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ (t9-selftest.txt and, where the plan names them, other logs). Do not read artifacts/retries/ or .dev/troubleshoot/.
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
