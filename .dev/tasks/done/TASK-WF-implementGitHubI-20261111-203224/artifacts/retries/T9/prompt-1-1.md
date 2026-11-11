74241494f4c1294617e42235b477f053ee266f96
Review one task for spec compliance.

Task brief: 
## Task 9: Sync the development copies and confirm the mirrors and path rule

Depends on: Task 5, Task 6, Task 8

Run `make sync-dev`, then `make verify-sync`. Run `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` and compare with the same grep on `git show origin/master` content (`git stash` is not allowed; use `git diff -U0` on the touched files instead) so any new hit is justified. Stage `.dev/tasks` only with `git add .dev/tasks`; never stage a path under `.claude/`.

Acceptance criteria:
- T9.AC1: `make verify-sync` exits 0 and `git status --porcelain` shows no `.claude/` path staged.
- T9.AC2: `git diff -U0` of the five edited files adds no line containing `src/superclaude/` in the contract or the routing guide.
- T9.AC3: `git diff --name-only origin/master` lists only the five files named in the Constraints plus the `.dev/` paths.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: 74241494f4c1294617e42235b477f053ee266f96
Diff against the start snapshot: 

--- new file .dev/tasks/to-do/TASK-WF-implementGitHubI-20261111-203224/artifacts/t9-verify-sync.log ---
=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
rc=0

--- new file .dev/tasks/to-do/TASK-WF-implementGitHubI-20261111-203224/artifacts/t9-scope.log ---
# staged .claude paths (expect 0):
0
# added lines containing src/superclaude/ in the five edited files (expect 0):
0
# git diff --name-only origin/master, non-.dev paths:
docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
src/superclaude/core/HOW-WE-WORK.md
src/superclaude/core/WORKER-CONTRACT.md
tests/skills/test_worker_contract.py


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
