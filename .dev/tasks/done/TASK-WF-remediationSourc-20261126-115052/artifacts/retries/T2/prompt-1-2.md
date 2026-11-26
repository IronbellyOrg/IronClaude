7f9f65b5e32ef5e1d5a066a5c728ff8748128d5c
Review one task for spec compliance.

Task brief: Task 2 of the plan .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/TASK-WF-remediationSourc-20261126-115052.md (lines 42-64). Task text (lines 46-54):
Read `./artifacts/t1-before.txt` and choose exactly one of three paths, in this order.

- Path earlier-call: the marker file `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.called` already exists, so an earlier attempt of this task may already have sent the call. Do not run the script. If the three environment variables are still unset, take the after readings; otherwise take none.
- Path run: the marker does not exist and the last line of `./artifacts/t1-before.txt` is `pre-conditions: pass`. Confirm again that the three environment variables are unset. If this second check finds any of them set, write no marker, run no script and take path stopped instead, with the variable name (never its value) as the failed pre-condition. Otherwise write the marker file with one line, a UTC timestamp from `date -u`, and only then run the script `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js` once with `node`, with no retry, and capture its standard output and error. Then take the after readings.
- Path stopped: the marker does not exist and either the last line of `./artifacts/t1-before.txt` starts with `pre-conditions: fail (`, or the second check of path run found a variable set. The failed pre-condition is copied from `./artifacts/t1-before.txt` or is the variable name. Do not write the marker, run no script and run no `orca` command.

The after readings repeat the readings of Task 1: the projectId from `orca worktree current --json`; `upstream`, `gitRemoteIdentity` and `repoIcon` from `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`; the ids of this repository's worktrees from `orca worktree list --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`, keeping only the ids that begin with `e8e07d51-c261-4936-815e-06aeceeb5bf8::` (if that command is rejected or prints no id of that repo, record the error or "none listed"; the `worktrees preserved:` line then reads `worktrees preserved: not checked`); and whether `orca repo list` still lists the repo with that id. On paths run and earlier-call with the variables unset, `./artifacts/t2-after.txt` records whether `orca worktree current --json` answered and whether `orca repo list` listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8, with the error text for a command that did not answer; a command that did not answer or a repo that is not listed counts as a failed reading for the outcome rule. Write `./artifacts/t2-after.txt` with a UTC timestamp from `date -u`, the path taken, the exact commands run, and: on path run, the script's result reduced to success or failure with its error text and, from its response, only the `upstream`, `gitRemoteIdentity` and `repoIcon` fields (the rest of the response is not saved); on path earlier-call, the marker's own timestamp and a line that the script output is not available; on every path but stopped and on earlier-call with a variable set, the after readings and a line `worktrees preserved: yes` when every worktree id listed in `./artifacts/t1-before.txt` is still listed, otherwise `worktrees preserved: no` with the missing ids; on path earlier-call with a variable set, the name of each variable found set (never its value), a line that no reading was taken and a line that the call may already have been sent; on path stopped, the failed pre-conditions copied from `./artifacts/t1-before.txt` or the variable name found set at the second check, and no readings.

Write `./artifacts/t2-outcome.md`. Its first line is exactly one of these three, chosen by this rule. `outcome: effective` when the after readings show upstream null and projectId github:ironbellyorg/ironclaude and the script, if it ran, did not report a failure. `outcome: not-applied` when the path is stopped, or the path is earlier-call and the readings show the upstream unchanged, or the script reported a failure and the readings show the upstream unchanged. `outcome: applied-not-effective` for every other combination, including readings that still show the upstream after a call that reported success, an upstream that reads missing instead of null, a script that reported a failure while the readings show the change landed, and a reading that failed; for these, quote the raw readings and the script error and say what was missing. On path earlier-call with a variable set no reading exists, so the rules above do not apply to it: its one defined outcome is `outcome: applied-not-effective`, because the call may have been sent and no effect was observed. Later lines state the path taken; that Orca was not restarted and the repo's Settings panel was not opened; that durability across a restart and after opening that panel is unverified; the two checks the owner should make (restart Orca and open the repo's Settings panel, then read the two states again); the rollback: the same `repo.update` call with `updates: { upstream: { owner: 'SuperClaude-Org', repo: 'SuperClaude_Framework' } }`, and the rollback record path `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json`. When the outcome is `not-applied` on path stopped, add a line that the override was not tried, that the failed pre-condition is fixed first and the override then tried, and that the decided fallback of changing Orca applies only if the override then does not hold. When the outcome is any other value but `effective`, except on path earlier-call with a variable set, add a line that the decided fallback is to change Orca and that the repo-icon change needs the owner's approval. On path earlier-call with a variable set, add instead a line that the readings are taken again with the three variables cleared before any fallback is chosen, and that the decided fallback of changing Orca applies only if those readings still show the upstream.

Acceptance criteria, AC ids in source order:
T2.AC1: `./artifacts/t2-after.txt` names exactly one path. On path run, the script command appears once, after the marker was written, and the marker file exists after the task; on paths earlier-call and stopped, no command in the file runs the script. Across every attempt the script has been started at most once.
T2.AC2: `./artifacts/t2-after.txt` lists every command that was run, and none carries a link flag (`--issue`, `--pr` or similar), a worktree creation or a git remote change.
T2.AC3: On paths run and earlier-call with the variables unset, `./artifacts/t2-after.txt` holds the after readings and the `worktrees preserved:` line, and the first line of `./artifacts/t2-outcome.md` is exactly one of the three outcome values and agrees with those readings by the rule above; on path run it also holds the reduced script result, and no part of the response beyond the three named fields is saved.
T2.AC4: On path earlier-call with a variable set, `./artifacts/t2-after.txt` holds no readings, the variable name (never its value) and the statement that the call may already have been sent, and the first line of `./artifacts/t2-outcome.md` is `outcome: applied-not-effective`. This path passes this task.
T2.AC5: On path stopped, `./artifacts/t2-after.txt` holds the failed pre-conditions (from `./artifacts/t1-before.txt` or the variable name found set at the second check) and the timestamp, no `orca` command and no script were run, and the first line of `./artifacts/t2-outcome.md` is `outcome: not-applied`. This path passes this task: a stop is a reported finding for the owner, not a failure of the plan.
T2.AC6: `./artifacts/t2-outcome.md` states that no Orca restart and no Settings panel opening took place, names the two owner checks, and gives the rollback call and the rollback record path.
T2.AC7: On paths run and earlier-call with the variables unset, `./artifacts/t2-after.txt` records whether `orca worktree current --json` answered and whether `orca repo list` listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8, with the error text for a command that did not answer. A command that did not answer or a repo that is not listed counts as a failed reading for the outcome rule and does not fail this criterion; `./artifacts/t2-outcome.md` says what was missing.
T2.AC8: If the outcome is not `effective`, the tracked source files are unchanged by this task and the reason is written in `./artifacts/t2-outcome.md`.
Global constraints: Plan ## Constraints (lines 17-26):

- Orca state is changed by exactly one repo.update call that carries only `upstream: null` for the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8. The Orca command line has no verb for it, so the call goes through the app's own client class in a one-off script. The call is sent at most once across every attempt of Task 2: a once-only marker file (named in Task 2) is written before the call and checked first, so a restart or retry of the task cannot send it again.
- The agent must not restart Orca (it hosts every running agent session) and must not open this repo's Settings panel. Durability across an Orca restart and after opening that panel therefore stays unverified and is reported as such.
- No Orca link flag (`--issue`, `--pr` or any other) is passed in any command, no worktree is created, no upstream git remote is added, and the upstream repository (SuperClaude-Org/SuperClaude_Framework) is not contacted.
- Every `orca` command in this plan is read-only and is run only after the three environment variables ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT are confirmed unset in that same step, because a set variable can point the Orca command line at a remote runtime. A variable that is set to an empty value counts as set. A set variable's value is never printed. The one-off node script is run only after the same check in the same step, because its client reads the same three variables; if any of them is set, the script is not run.
- Files that must not change: pyproject.toml, package.json, anything under src/superclaude, the Orca files orca-data.json and its backups, the Orca database (it is never edited directly; the one allowed call changes it through Orca's own client), any git remote, the captured fixtures tests/sweep/fixtures/captured-worktree-current.json and tests/sweep/fixtures/captured-worktree-list.json (they record the old id as history), and every part of CLAUDE.md outside the Orca paragraph.
- The second state change that also replaces the repo icon (step B of the REPORT.md Proposed Fix) is not run without the owner's approval. If the override does not take effect, the decided fallback is to change Orca, which is outside this plan and is reported for the owner.
- Evidence files are written under ./artifacts/ inside this package. The one-off script and its once-only marker are not delivery files: they live in the folder `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/` (the spec's own example location), stay untracked and are never staged or committed. `git add` is never run on that folder.
- Timestamps written into any evidence file are copied from the output of `date -u +%Y-%m-%dT%H:%M:%SZ`, never typed from memory.
Start sha: 7f9f65b5e32ef5e1d5a066a5c728ff8748128d5c
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-26T12:09:54Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-780; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-780. Call codegraph only when index_state: fresh, never to widen scope. Q2b: no code symbol changed; dependents: none.

Note from the orchestrator: this task's work is one live Orca call plus evidence files. The script and the once-only marker live in the folder named by the plan Constraints (line 25); you need not read that folder. State facts are below. Cite the evidence files as ./artifacts/<file>:<line>.

git diff against the start snapshot: no tracked file changed. New untracked files in this task's touched set, full contents with line numbers:

=== NEW FILE: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t2-after.txt ===
 1: t2-after.txt (Task 2: after state)
 2: timestamp: 2026-11-26T12:13:09Z
 3: path taken: run
 4: 
 5: ## commands run (in this order; none carries a link flag, creates a worktree or changes a git remote)
 6: 1. variable check (`${VAR+set}` for ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING, ORCA_ENVIRONMENT): all three unset, in the same step as the marker write and the script run
 7: 2. marker file written first: .dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.called (contents: 2026-11-26T12:13:00Z)
 8: 3. node .dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js   (run once, no retry)
 9: 4. variable check again (all three unset), then the after readings:
10:    orca worktree current --json
11:    orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json
12:    orca repo list --json
13:    orca worktree list --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json   (only ids beginning with e8e07d51-c261-4936-815e-06aeceeb5bf8:: kept)
14: 5. one extra read-only reading about 27 seconds later (not required by the plan; recorded because the first reading showed upstream null but an unchanged projectId): orca worktree current --json; orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json
15: 
16: ## script result (reduced to success or failure and the three named fields)
17: result: success (exit code 0, ok: true, no error text)
18: upstream: null
19: gitRemoteIdentity: {"canonicalKey":"github.com/IronbellyOrg/IronClaude","remoteName":"origin","remoteUrl":"https://github.com/IronbellyOrg/IronClaude"}
20: repoIcon: {"type":"image","src":"https://github.com/IronbellyOrg.png?size=64","source":"github","label":"IronbellyOrg/IronClaude"}
21: 
22: ## after readings (timestamp 2026-11-26T12:13:09Z)
23: orca worktree current --json answered: true
24: orca repo list listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8: yes
25: projectId: github:superclaude-org/superclaude_framework
26: repo show: {"upstream":null,"gitRemoteIdentity":{"canonicalKey":"github.com/IronbellyOrg/IronClaude","remoteName":"origin","remoteUrl":"https://github.com/IronbellyOrg/IronClaude"},"repoIcon":{"type":"image","source":"github"}}
27: worktree list: ok: true, totalCount: 32, truncated: false
28: ids of this repository's worktrees (only ids beginning with e8e07d51-c261-4936-815e-06aeceeb5bf8::), sorted, 32 listed:
29: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/IronClaude
30: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/Coordinator
31: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/cicd-ref-ironclaude
32: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/gaps-761-new-j
33: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/gaps-761-research
34: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/ic6-orchestrator
35: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-289
36: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-290
37: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-326
38: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-352
39: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-379
40: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-393
41: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-517
42: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-571
43: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-572-agent-usage
44: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-599
45: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-610
46: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-655-spec
47: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-676
48: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-758
49: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-764
50: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-765
51: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-779
52: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-780
53: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-826
54: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-834
55: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-837
56: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-838
57: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-848
58: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/issue-templates-plan-fields
59: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/iteration-3-e2-lead
60: e8e07d51-c261-4936-815e-06aeceeb5bf8::/home/coder/workspaces/worktrees/IronClaude/iteration-3-work-files
61: id-by-id comparison with ./artifacts/t1-before.txt (both lists sorted, compared with comm): ids in t1-before.txt but not listed now: none; ids listed now but not in t1-before.txt: none
62: worktrees preserved: yes
63: (every one of the 32 ids in ./artifacts/t1-before.txt is still listed; no id was added or lost)
64: 
65: ## extra reading (timestamp 2026-11-26T12:13:36Z, read-only)
66: projectId: github:superclaude-org/superclaude_framework
67: upstream: null

=== NEW FILE: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t2-outcome.md ===
 1: outcome: applied-not-effective
 2: 
 3: path taken: run. The one `repo.update` call (upstream null) was sent once and reported success, and the stored upstream now reads null. The projectId in `orca worktree current --json` still reads github:superclaude-org/superclaude_framework, both right after the call (2026-11-26T12:13:09Z) and about 27 seconds later (2026-11-26T12:13:36Z). By the outcome rule the override did not take effect on the project id. Raw readings are in ./artifacts/t2-after.txt: upstream null, projectId github:superclaude-org/superclaude_framework, worktrees preserved: yes (32 of 32).
 4: 
 5: What this does not show (unverified): whether the project id is only recomputed when Orca restarts or when its worktree records are rebuilt. The agent did not restart Orca and did not open the repo's Settings panel, so the id may still change after either, and the stored null may also be replaced when the Settings panel is opened (the panel asks GitHub again for a repo with a GitHub avatar icon). Durability across a restart and after opening that panel is unverified.
 6: 
 7: Owner checks (the two checks the owner should make): restart Orca and open the repo's Settings panel, then read the two states again with `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json`.
 8: 
 9: Orca was not restarted and the repo's Settings panel was not opened.
10: 
11: Rollback: send the same `repo.update` call with `updates: { upstream: { owner: 'SuperClaude-Org', repo: 'SuperClaude_Framework' } }`. The previous record is kept in `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json`.
12: 
13: The decided fallback is to change Orca (so the fork's own git remote wins over the stored upstream). The second state change that also replaces the repo icon (step B of the REPORT.md Proposed Fix) is not run and needs the owner's approval.
14: 
15: The tracked source files are unchanged by this task.

=== state facts checked by the orchestrator after the task ===
marker file override-upstream-null.called exists, contents: 2026-11-26T12:13:00Z; its timestamp (12:13:00Z) precedes t2-after.txt's timestamp (12:13:09Z)
the 32 ids in t2-after.txt are the sorted output of the 12:13:09Z orca worktree list --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json reading; the orchestrator compared them with the ids of ./artifacts/t1-before.txt with comm: no difference
git status --short, tracked files: [0 lines outside the always-staged .dev/tasks package]
Delta diff from the previous reviewed tree (empty on the first review): (git diff of the changed evidence file between the previous reviewed tree and this one; lines starting + are added)
diff --git a/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t2-after.txt b/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t2-after.txt
index 1285bf02b..2f07dee9d 100644
--- a/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t2-after.txt
+++ b/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t2-after.txt
@@ -25,7 +25,40 @@ orca repo list listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8: yes
 projectId: github:superclaude-org/superclaude_framework
 repo show: {"upstream":null,"gitRemoteIdentity":{"canonicalKey":"github.com/IronbellyOrg/IronClaude","remoteName":"origin","remoteUrl":"https://github.com/IronbellyOrg/IronClaude"},"repoIcon":{"type":"image","source":"github"}}
 worktree list: ok: true, totalCount: 32, truncated: false
-ids of this repository's worktrees (only ids beginning with e8e07d51-c261-4936-815e-06aeceeb5bf8::): 32 listed
+ids of this repository's worktrees (only ids beginning with e8e07d51-c261-4936-815e-06aeceeb5bf8::), sorted, 32 listed:
+id-by-id comparison with ./artifacts/t1-before.txt (both lists sorted, compared with comm): ids in t1-before.txt but not listed now: none; ids listed now but not in t1-before.txt: none
 worktrees preserved: yes
 (every one of the 32 ids in ./artifacts/t1-before.txt is still listed; no id was added or lost)
 
(plus 32 added lines of worktree ids beginning e8e07d51-c261-4936-815e-06aeceeb5bf8::, shown in full in the file contents above)
Earlier blocking findings of this start (empty on the first review): F1.1 ac=T2.AC3 at=./artifacts/t2-after.txt:28 anchor="holds the after readings and the `worktrees preserved:` line" chk=y,n,n,n family=evidence-after-worktree-ids fix=add the after ids of this repository's worktrees to t2-after.txt: t2-after.txt records only a count (32 listed) where the after readings must repeat the worktree-id reading.
Saved-probe re-check hit locations (may be empty): probe family evidence-after-worktree-ids: ./artifacts/t2-after.txt hit lines 13 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 

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
