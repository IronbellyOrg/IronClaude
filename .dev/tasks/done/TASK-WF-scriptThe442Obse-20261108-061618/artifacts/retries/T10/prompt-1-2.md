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
Changed since the first review (read the files; there is no git diff, they are untracked or logs):
- /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md: header notes for the saved copy and the issue count; item 1 log lines; the three needs-reading marks replaced by readings with screen files; the OB-CTX log path note.
- /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/evidence.sh and evidence-selftest.sh: the copy step now also saves gov-log, preconditions and baselines; item 1 cites the evidence rows.
- .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t10-run-log.md: two sections appended at the end (exit codes; issue count check).
- .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs/session-output/ and .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs/gov-log-reconstructed.txt: new, rebuilt from the saved session outputs because /tmp/ob/gov-log.txt was removed by cleanup.
Not changed and known: T10.AC3's phrase "lists exactly four issues" cannot hold while both the first attempt's closed issues 593 to 596 and the rerun's 642 to 645 carry the same title; the run log and the results file record this openly as a deviation for the owner to accept.
Earlier blocking findings of this start (empty on the first review):
F1.1 ac=T10.AC2 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t10-run-log.md:45-70 anchor="lists every script run with its exit code" chk=y,n,n,n family=runlog-exit-codes fix=add an exit-code line for each run that has none. In the final run these are: evidence.sh all at L:45/46/47, after B (L:59), after C (L:63), after D (L:66) and after E (L:70); setup-github.sh first run (L:48, stopped, no code); session-gov.sh b first pass (L:53, stopped, no code); the plan-only cleanup run behind t11-cleanup-plan.txt (L:70). The earlier run has the same gaps at L:17, L:19, L:26 and L:31. Use the real code or write "killed by me, no code" for a run that was stopped covers="every script run with its exit code": only some runs carry exit=N; the evidence.sh runs after sessions B, C, D and E and several stopped runs have none.
F1.2 ac=T10.AC3 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md:9 anchor="`gh_fork issue list --search \"ob-442 disposable\"` lists exactly four issues" chk=y,n,n,n family=disposable-issue-count fix=run the list command, paste its output in the results file and the run log, and state why it shows eight issues (593-596 from the accidental 2026-11-17 run, adopted as T1-T4 and claimed and commented at L:5,33-35, closed 2026-11-17T18:42Z; 642-645 from the rerun, closed 2026-11-18T19:39Z). The AC as written cannot hold with both sets on GitHub, so either record this deviation openly or have the orchestrator reword the AC; as it stands no row records a count check and R:9 lists only 642-645 covers="lists exactly four issues": the live search with --state all returns 8 issues, the open-only default returns 0, and no check is recorded.
F1.3 ac=T10.AC1 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs/logs/h1.jsonl:6 anchor=OB/logs/h1.jsonl:6 and :11 hold the two item-1 evidence rows (PreToolUse Bash with agent_id afec0ca3385c21677 and a85b8013a874ad75a); results line 33 cites "lines 2,3,4", which are the prompt, the Agent PreToolUse and the Agent PostToolUse with no agent_id chk=n,y,n,n family=evidence-citation fix=change the item 1 log line to 6 and 11, and add one line near the header saying the /tmp/ob/logs/... paths in the file are kept at OB/logs/... covers="no PASS lacks an evidence command and a log line or screen file": the cited lines do not hold the evidence shown (R:33).
F1.4 ac=T10.AC1 at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md:741 anchor="no PASS lacks an evidence command and a log line or screen file" chk=y,n,n,n family=evidence-file-missing fix=OB has no gov-log.txt (evidence.sh:412 copies only logs, screens and state.env, and /tmp/ob is gone), so the OB-CTX PASS parts "sleep 241 and sleep 242 told apart", "released case" and the OB-H3 .ok-file parts cannot be checked against the log file R:741 cites (/tmp/ob/gov-log.txt). Recover the gov-log text from the pasted rows into a file under OB, or re-record those parts with evidence that still exists; /tmp/ob/preconditions.txt is also gone covers="a log line or screen file": the log file cited for OB-CTX PASS does not exist in the delivered ob-logs.
F1.5 ac=scope at=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-results.md:469 anchor="For each `needs reading` mark, record the reading and the screen file it is based on in the results file." chk=n,n,n,y family=needs-reading-unrecorded fix=read the saved screens in OB/screens (sA-*, gB-*, gC-*, gE-*) and record the three readings with evidence.sh --reading u20, ac7 and retry-f7-f8 (each with its screen file), or write that no screen shows the block message; mind that evidence.sh all replaces the file on a rerun covers="record the reading and the screen file": R:469 (U20), R:535 (retry-f7-f8) and R:536 (AC-7) are still "needs reading" with no reading and no screen file, and OB-H3's "What you saw in the tab" (R:523) is empty.
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
