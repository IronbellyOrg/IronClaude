58e1ddd15c7cc91a068b0820c93b5359079c9be9
Review one task for spec compliance.

Task brief: ## Task 9: Write the follow-up list of code that checks approvals

Depends on: Task 8

Write ./artifacts/follow-ups.md in this package. List docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (lines 717, 722 and 2204 restate the old rule and cite WORKER-CONTRACT.md:57 and qa.md:249 by line number) as a document that needs its own update, not edited here. For each of src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py and src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py, name the function or line range that checks an approval or Ruling, say what it checks today, and say what would have to change for it to accept a dashboard answer row. State plainly that none of these files was edited. Also list docs/designs/ files that restate the old rule, found by Grep for "executor-invented" and "another agent's message" under docs/designs/.

Acceptance criteria:
- ./artifacts/follow-ups.md exists and names all four code files with a read line range each.
- git diff --stat shows no change to those four files or to docs/designs/.
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 58e1ddd15c7cc91a068b0820c93b5359079c9be9
Diff against the start snapshot: 
--- new untracked file .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/follow-ups.md ---
# Follow-ups: code and documents that check or restate who may confirm

None of the four code files below, and nothing under docs/designs/, was edited by this change. Each entry names what the file checks today (read for this report) and what would have to change for it to accept a dashboard answer row as a person's confirmation. All of that work waits until the dashboard answer path is released (the release 1.8 gates).

| File and place | What it checks today | What would change for a dashboard answer row |
|---|---|---|
| src/superclaude/cli/issue_pipeline/cli.py lines 77-96 (`check-approval`) and 135-158 (`record-create`, option `--channel`) | `check-approval` matches the approval text of a plan reply against the plan files and prints `ok` or a closed refusal. `record-create` takes a channel from `approval_record.CHANNELS` (see below). | A new channel value for a dashboard answer row, and a check that the row was created under the person's own login and names the question id of the plan approval. |
| src/superclaude/cli/issue_pipeline/approval_record.py line 43 (`CHANNELS = ("label", "comment", "reply")`) | The approval row accepts only the label, comment and reply channels. This is the plan-approval path (GitHub evidence), which the WC-3 definition leaves unchanged. | Whether the plan-approval path should also accept a dashboard response is an owner decision; if yes, add a `dashboard` channel here and in the check above. |
| src/superclaude/cli/issue_pipeline/complete.py lines 1-5 (module docstring) and the `complete` function | Docstring says the verb runs only under the issue's grant row; the code does not itself read a grant row (the rule is the control, enforced by the coordinator and a launch-level text guard). | No code change needed for a dashboard grant row; the grant-row record is made by the agent from the confirmation (WC-3). A mechanical check of the row's provenance would be a new feature. |
| src/superclaude/cli/sweep/classify.py lines 97 and 126-127 (`_RULING_HALT_CODES = ("E-HALT-QA", "E-NO-RULING")`, `_ruling_halt`) and the use at lines 165-190 | Classifies a blocked worker contract as waiting for a person when its stop codes are a Ruling halt. It reads stop codes only and never reads who confirmed. | None for the confirmation channel. A dashboard answer would clear the halt through the same Ruling line and resume path. |
| src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py line 54 (`_RULING` regex) and `validate` (line 278 onward), lines 360-392 | Replays the ledger. A non-compliant task may be `complete` only if a matching `T<id>: Ruling:` line precedes it with unchanged verdict fields (`E-ARCHIVE-TASKS` otherwise). It checks the shape of the line, not the channel or provenance. | None for the shape: the dashboard example in refs/ledger.md matches the same regex. A provenance check (the answer row id exists and was created by the person's login) would need access to the dashboard store and is a new feature. |

Documents:

- docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md lines 717, 722 and 2204 restate the old chat-only rule and cite `WORKER-CONTRACT.md:57` and `qa.md:249` by line number. They are stale after this change and need their own update (not edited here).
- docs/designs/: Grep for "executor-invented" and "another agent's message" under docs/designs found no hit. The word "Ruling" in docs/designs/sc-closeout.md and orchestrator-mode.md means the owner's numbered Rulings, a different sense, so nothing there restates the rule.

Open owner question (not decided here): whether a dashboard response should also be accepted for the issue-pipeline plan approval (WC-17 and the "Plan approval" bullet of the issue-pipeline section), which today comes from GitHub evidence the coordinator reads.



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (the artifact is a Markdown report).
Context: git diff --stat over src/superclaude/cli, the implement skill scripts directory and docs/designs shows no change (empty). The report is a package artifact, not a delivery file.

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
