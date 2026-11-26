c4746625edd447c9bd3b729e6a884dc6957f6809
Review one task for spec compliance.

Task brief: Task 4 of the plan .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/TASK-WF-remediationSourc-20261126-115052.md (lines 85-98). Task text (lines 89):
Write `./artifacts/t4-pr-note.md`, the text the pull request description is made from. It holds these labelled parts: the outcome (the first line of `./artifacts/t2-outcome.md` with one sentence of meaning, and the path taken); the evidence (on paths run and earlier-call with the variables unset, the before and after readings (with each worktree id replaced by the count of this repository's worktrees, plus the `worktrees preserved:` line) copied from `./artifacts/t1-before.txt` and `./artifacts/t2-after.txt`, or, on path stopped and on earlier-call with a variable set, only the recorded stop (the failed pre-condition, the variable name found set, or that no `orca` command was run) and the before readings when Task 1 took them); the owner checks that remain (restart Orca and open the repo's Settings panel, then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id github:ironbellyorg/ironclaude); the fallback (on path stopped, fix the failed pre-condition and try the override, and only if it then does not hold change Orca; on earlier-call with a variable set, take the readings again with the three variables cleared before any fallback is chosen, and change Orca only if those readings still show the upstream; otherwise, if the id reverts, the next try is the second state change that also replaces the repo icon, which needs the owner's approval, then changing Orca); a line that issue 769 (trimming the CLAUDE.md startup context) also touches the same paragraph and asks for fresh identity evidence, which this note supplies; the rollback call and record path from `./artifacts/t2-outcome.md`; and the keyword line, which says to write `Refs #780` and not `Fixes #780`, because durability is unverified and the link-flag ban stays until the owner agrees to lift it. The note also carries the decided route word for word: Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca. The last part, labelled `Pull request body`, is the exact text to pass as the `--body` of `/sc:pr-submit`: the outcome line, the decided route sentence, the evidence, the owner checks, the fallback, the issue 769 line and the keyword line. The note also says that the folder `.dev/troubleshoot/` (script and marker) is not staged. The note and the `Pull request body` carry only the count of this repository's worktrees and the `worktrees preserved:` line, never worktree ids.

Acceptance criteria, AC ids in source order:
T4.AC1: `./artifacts/t4-pr-note.md` exists and holds the outcome, the evidence, the owner checks, the fallback, the issue 769 line, the rollback and the keyword line, each as its own labelled part, and ends with the part labelled `Pull request body`.
T4.AC2: The decided route sentence appears in the note word for word as written in this task, and again inside the `Pull request body` part.
T4.AC3: On paths run and earlier-call with the variables unset, the note holds the before and after readings, equal to the readings in `./artifacts/t1-before.txt` and `./artifacts/t2-after.txt` except that worktree ids appear only as a count of this repository's worktrees plus the `worktrees preserved:` line, and makes no claim of durability.
T4.AC4: On path stopped and on earlier-call with a variable set, the note holds only the recorded stop (the failed pre-condition, the variable name found set, or that no `orca` command was run) and the before readings when Task 1 took them (a stop caused by a set variable at Task 1 has none); it needs no after readings and makes no claim of durability.
T4.AC5: No worktree id appears in the note or in the `Pull request body`.
T4.AC6: The note's keyword line says `Refs #780`, and the note names what is left (the two owner checks and the lifting of the link-flag ban).
T4.AC7: `git status --short .dev/troubleshoot/` shows the folder as untracked (`??`) and no path under it as staged.
Global constraints: Plan ## Constraints (lines 17-26):

- Orca state is changed by exactly one repo.update call that carries only `upstream: null` for the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8. The Orca command line has no verb for it, so the call goes through the app's own client class in a one-off script. The call is sent at most once across every attempt of Task 2: a once-only marker file (named in Task 2) is written before the call and checked first, so a restart or retry of the task cannot send it again.
- The agent must not restart Orca (it hosts every running agent session) and must not open this repo's Settings panel. Durability across an Orca restart and after opening that panel therefore stays unverified and is reported as such.
- No Orca link flag (`--issue`, `--pr` or any other) is passed in any command, no worktree is created, no upstream git remote is added, and the upstream repository (SuperClaude-Org/SuperClaude_Framework) is not contacted.
- Every `orca` command in this plan is read-only and is run only after the three environment variables ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT are confirmed unset in that same step, because a set variable can point the Orca command line at a remote runtime. A variable that is set to an empty value counts as set. A set variable's value is never printed. The one-off node script is run only after the same check in the same step, because its client reads the same three variables; if any of them is set, the script is not run.
- Files that must not change: pyproject.toml, package.json, anything under src/superclaude, the Orca files orca-data.json and its backups, the Orca database (it is never edited directly; the one allowed call changes it through Orca's own client), any git remote, the captured fixtures tests/sweep/fixtures/captured-worktree-current.json and tests/sweep/fixtures/captured-worktree-list.json (they record the old id as history), and every part of CLAUDE.md outside the Orca paragraph.
- The second state change that also replaces the repo icon (step B of the REPORT.md Proposed Fix) is not run without the owner's approval. If the override does not take effect, the decided fallback is to change Orca, which is outside this plan and is reported for the owner.
- Evidence files are written under ./artifacts/ inside this package. The one-off script and its once-only marker are not delivery files: they live in the folder `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/` (the spec's own example location), stay untracked and are never staged or committed. `git add` is never run on that folder.
- Timestamps written into any evidence file are copied from the output of `date -u +%Y-%m-%dT%H:%M:%SZ`, never typed from memory.
Start sha: c4746625edd447c9bd3b729e6a884dc6957f6809
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-26T12:09:54Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-780; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-780. Call codegraph only when index_state: fresh, never to widen scope. Q2b: no code symbol changed; one new Markdown evidence file.

git diff against the start snapshot: no tracked file changed by this task. New untracked file in this task's touched set, full contents with line numbers:

=== NEW FILE: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115052/artifacts/t4-pr-note.md (cite as ./artifacts/t4-pr-note.md:<line>) ===
  1: # Pull request note for issue 780 (Orca project id of this repository)
  2: 
  3: Source readings: ./artifacts/t1-before.txt and ./artifacts/t2-after.txt. This note carries only a count of this repository's worktrees and the `worktrees preserved:` line, never worktree ids. The folder `.dev/troubleshoot/` (the one-off script and its once-only marker) is not staged and is not part of the pull request.
  4: 
  5: ## Outcome
  6: 
  7: `outcome: applied-not-effective` (path taken: run). The one `repo.update` call that stores upstream null for this repository was sent once and reported success, and the stored upstream now reads null. The project id in `orca worktree current --json` still reads `github:superclaude-org/superclaude_framework`, right after the call (2026-11-26T12:13:09Z) and about 27 seconds later (2026-11-26T12:13:36Z). So the override did not correct the id as far as these readings show.
  8: 
  9: ## Decided route
 10: 
 11: Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca.
 12: 
 13: ## Evidence
 14: 
 15: Before the call (2026-11-26T12:10:36Z):
 16: 
 17: ```text
 18: projectId: github:superclaude-org/superclaude_framework
 19: {
 20:   "upstream": {
 21:     "owner": "SuperClaude-Org",
 22:     "repo": "SuperClaude_Framework",
 23:     "host": "github.com"
 24:   },
 25:   "gitRemoteIdentity": {
 26:     "canonicalKey": "github.com/IronbellyOrg/IronClaude",
 27:     "remoteName": "origin",
 28:     "remoteUrl": "https://github.com/IronbellyOrg/IronClaude"
 29:   },
 30:   "repoIcon": {
 31:     "type": "image",
 32:     "source": "github"
 33:   }
 34: }
 35: worktrees of this repository: 32 (count only)
 36: ```
 37: 
 38: After the call (2026-11-26T12:13:09Z):
 39: 
 40: ```text
 41: orca worktree current --json answered: true
 42: orca repo list listed the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8: yes
 43: projectId: github:superclaude-org/superclaude_framework
 44: repo show: {"upstream":null,"gitRemoteIdentity":{"canonicalKey":"github.com/IronbellyOrg/IronClaude","remoteName":"origin","remoteUrl":"https://github.com/IronbellyOrg/IronClaude"},"repoIcon":{"type":"image","source":"github"}}
 45: worktrees of this repository: 32 (count only)
 46: worktrees preserved: yes
 47: ```
 48: 
 49: Extra read-only reading (2026-11-26T12:13:36Z): projectId `github:superclaude-org/superclaude_framework`, upstream null.
 50: 
 51: ## Owner checks that remain
 52: 
 53: Restart Orca and open the repo's Settings panel (the agent did neither), then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id `github:ironbellyorg/ironclaude`. Durability across a restart and after opening the Settings panel is unverified, and so is whether the id is only recomputed after a restart.
 54: 
 55: ## Fallback
 56: 
 57: If the id still shows the upstream, or reverts, the next try is the second state change that also replaces the repo icon, which needs the owner's approval, then changing Orca so the fork's own git remote wins. The decided fallback of changing Orca applies because the override did not correct the id in these readings.
 58: 
 59: ## Issue 769
 60: 
 61: Issue 769 (trimming the CLAUDE.md startup context) also touches the same Orca paragraph in CLAUDE.md and asks for fresh identity evidence. The Evidence part above supplies it: the stored upstream before (SuperClaude-Org/SuperClaude_Framework) and after (null), and the project id before and after (unchanged).
 62: 
 63: ## Rollback
 64: 
 65: Send the same `repo.update` call with `updates: { upstream: { owner: 'SuperClaude-Org', repo: 'SuperClaude_Framework' } }`. The previous record is kept in `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json`.
 66: 
 67: ## Keyword line
 68: 
 69: Write `Refs #780` and not `Fixes #780`, because durability is unverified, the id is not shown to be corrected, and the link-flag ban stays until the owner agrees to lift it. What is left: the two owner checks above (restart Orca; open the repo's Settings panel and read the two states again) and the lifting of the link-flag ban.
 70: 
 71: ## Pull request body
 72: 
 73: Outcome: `outcome: applied-not-effective`. The one-time override stored upstream null for this repository and the stored upstream now reads null, but `orca worktree current --json` still shows project id `github:superclaude-org/superclaude_framework` right after the call and 27 seconds later. The change in this pull request is the Orca paragraph of CLAUDE.md, which now states the verified cause and this result without claiming the id was corrected.
 74: 
 75: Decided for this work: Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca.
 76: 
 77: Evidence: before the call the stored upstream was SuperClaude-Org/SuperClaude_Framework and the project id was `github:superclaude-org/superclaude_framework`; after the call the stored upstream is null (gitRemoteIdentity unchanged: github.com/IronbellyOrg/IronClaude, remote origin) and the project id is still `github:superclaude-org/superclaude_framework` (readings at 2026-11-26T12:13:09Z and 12:13:36Z). The repository has 32 worktrees before and after; worktrees preserved: yes.
 78: 
 79: Owner checks that remain: restart Orca and open the repo's Settings panel, then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id `github:ironbellyorg/ironclaude`. Durability is unverified.
 80: 
 81: Fallback: if the id still shows the upstream, the next try is the second state change that also replaces the repo icon (needs the owner's approval), then changing Orca so the fork's git remote wins. Rollback: the same `repo.update` call with the upstream object `SuperClaude-Org/SuperClaude_Framework`.
 82: 
 83: Issue 769 (trimming the CLAUDE.md startup context) also touches the same Orca paragraph and asks for fresh identity evidence; the evidence above is that evidence.
 84: 
 85: Refs #780 (not Fixes): the id is not shown to be corrected, durability is unverified, and the Orca link-flag ban stays until the owner agrees to lift it.

=== checks run by the orchestrator ===
occurrences of the string '::' in the note (a worktree id contains it): 0; occurrences of the repo id followed by '::': 0
occurrences of the decided-route sentence word for word: 2
git status --short .dev/troubleshoot/: ?? .dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/  ; staged paths under it: 0
the readings of the note were compared by the orchestrator against ./artifacts/t1-before.txt:10-26 (before) and ./artifacts/t2-after.txt:22-26 and 64-67 (after); worktree ids are replaced by the count 32 as the task allows. The first line of ./artifacts/t2-outcome.md is: outcome: applied-not-effective; the path taken is run.
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
