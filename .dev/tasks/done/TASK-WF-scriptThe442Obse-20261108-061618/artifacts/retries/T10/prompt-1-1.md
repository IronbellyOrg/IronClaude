dda1a4f25199cdc5db67ac3eabc337219ed51589
Review one task for spec compliance.

Task brief:
## Task 10: Run the observations in the runbook order and record the results

Depends on: Task 9

Run the scripts against the real Orca and GitHub, in the order of runbook section 3.1 (lines 700-710): `setup.sh`, `session-a.sh`, `session-a2.sh`, `evidence.sh all`, then `setup-github.sh` and `session-gov.sh b`, `c`, `d` and `e`, and `evidence.sh all` after each session. Follow the stop rules of section 3.3 as the scripts enforce them. A gated skip is a valid recorded outcome: when the stop rules skip session `d` or `e`, or any session ends FAIL, record that outcome in the results file, do not run the remaining governed sessions, and go to Task 11 cleanup with the resources that exist; a pull request then never exists and later PR assertions apply only when one was created.

At each `NEEDS_INPUT`, read the saved screen and answer with `driver.sh answer <name> <key> <reason>`:
- answer a tool permission dialog only for a command whose target is this run's disposable set (the T1 to T4 issues, their worktrees and branches, the plan's own scripts, or `/tmp/ob`);
- answer nothing else;
- record every answer in `./artifacts/t10-run-log.md`.

`BLOCKED login-isolated-home` is the owner's decision: stop session A and ask. For each `needs reading` mark, record the reading and the screen file it is based on in the results file. Record the version and hash header fields from `/tmp/ob/preconditions.txt`.

Acceptance criteria:
- [T10.AC1] `.dev/issues/442/observation-results.md` has 12 item blocks. Each Result is PASS, FAIL or pending with its evidence lines, and no PASS lacks an evidence command and a log line or screen file.
- [T10.AC2] `$PKG_ART/ob-logs/` exists and passed the secret scan. `./artifacts/t10-run-log.md` lists every script run with its exit code and every `answer` call with its reason.
- [T10.AC3] The disposable pull request URL in the results file starts with `https://github.com/IronbellyOrg/IronClaude/pull/`, when a pull request was created; when the gates skipped session `e`, the results file records that skip instead. No issue other than T1 to T4 was claimed or commented on: `gh_fork issue list --search "ob-442 disposable"` lists exactly four issues, and the claim session screens show no other issue number.
- [T10.AC4] Any FAIL in OB-H2, OB-H3 or OB-CTX is stated at the top of the results file, with the section 3 consequence: no governed claim on a real issue.

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

Start sha: dda1a4f25199cdc5db67ac3eabc337219ed51589
Diff against the start snapshot:
The scripts and the runbook are untracked files, so there is no git diff. The touched set of Task 10 (files changed or produced during the live run, absolute paths; read them with Read) is:
/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md
/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-runbook.md
/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/ (all *.sh files listed below, and prompts/)
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/cleanup-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/cleanup.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/driver-helpers.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/driver-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/driver.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/evidence-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/evidence.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/lib-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/lib.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/runbook-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/session-a-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/session-a.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/session-a2.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/session-gov-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/session-gov.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/setup-github-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/setup-github.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/setup-selftest.sh
  /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/setup.sh
/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t10-run-log.md
/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs/ (copy of the run's logs, screens, state, gov-log; may be large, search it)
Live-run facts the AC text names: the run used issues 642 to 645 and pull request 654 on IronbellyOrg/IronClaude; session A2 (session-a2.sh) was deliberately not run, and the run log records why. The earlier accidental issues 593 to 596 are recorded in the run log. Read the run log first.
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
