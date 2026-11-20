12a14d86d0beedf92c5b30ac5f82cc753e42a5db
Review one task for spec compliance.

Task brief: ## Task 4: Record the owner's observation of the value times

Depends on: Task 3

This task needs the owner's hands: a field change is a GitHub write, which no agent may run (Constraints). The owner changes the Pipeline, then the Status, then sets the `Approved` issue field to `Yes` (R35), in this order, on one throwaway issue in a test Project. After each owner step, the executor runs the read-only query of Task 3 for that issue's Project item and records the Status and Pipeline value times in `./artifacts/t4-updatedat-observation.md`: before any change, after the Pipeline change, after the Status change and after the `Approved` field is set. The last read also runs the GraphQL timeline read of Task 4a for the issue and records the `IssueFieldAddedEvent` for `Approved` (actor, createdAt, value). Reads 0 to 2 are already in the file (issue 642 in Project 2: Pipeline set to Worktree, Status moved from Done to Spec); only the `Approved` step remains. The task asks the owner in chat for each step and does not continue until the owner answers. The file ends with an outcome line. Field change moves the matching value time and setting `Approved` moves neither: rule R31 stands as written. A field change that moves no time: the rule would fail open, so the task stops and returns the R31 fallback (an approval value specific to the level) to the owner. Setting `Approved` that moves a Status or Pipeline value time: every approval would be voided, so the task stops with the same fallback. An `Approved` event that lacks the actor, the time or the value stops the task the same way, because Task 4a could not name who approved.

Acceptance criteria:
- T4.AC1: `./artifacts/t4-updatedat-observation.md` exists, holds the four recorded reads with their timestamps and ends with exactly one outcome line naming one of the three outcomes above.
- T4.AC2: When the outcome is not "rule stands", no later task that reads the value times starts, and the fallback is reported to the owner in chat.
- T4.AC3: No real issue, Status, label or field is changed by the executor, and the throwaway issue and Project are named in the file.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- This plan applies requirement R35 (owner decision of 2026-11-19): the approval is no longer the label `issue-watch:approved`. It is the organization issue field `Approved` (single select, one option `Yes`, field id 50144115 on `IronbellyOrg`) set to `Yes` by an allowed approver (IronBelly, Clay or a maintainer, the approvers file of today). The trigger label `issue-watch:trigger` stays. Who set the field and when comes from the issue's GraphQL timeline events `IssueFieldAddedEvent`, `IssueFieldChangedEvent` and `IssueFieldRemovedEvent` (each carries `actor`, `createdAt`, `issueField` and the value; verified read-only on 2026-11-19 against issue 675 with another field), because the REST events endpoint names the event but not the field or the value. Task 4a builds the read; the approval predicates, the approval-void rule and the claim-time refusal keep their logic and see the field events as label events named by `approval_label`. A real label with the old name never approves. Task 4 is amended to observe the field instead of the label; the plan was copied from `TASK-WF-requirements-20261119-143917` (Tasks 1 to 3 complete there) and edited by owner instruction, and `source.md` still carries the label wording of the requirements file (Task 28 updates the requirements file).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval (the `Approved` issue field set to Yes, R35), the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the `Approved` field after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 4a, 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 4a, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 4a, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 12a14d86d0beedf92c5b30ac5f82cc753e42a5db
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917-2/artifacts/t4-updatedat-observation.md b/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917-2/artifacts/t4-updatedat-observation.md
new file mode 100644
index 000000000..1c344070c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917-2/artifacts/t4-updatedat-observation.md
@@ -0,0 +1,55 @@
+# T4: observation of the Status and Pipeline value times
+
+Throwaway issues (chosen by the executor from the 100 items of Project 2 "Ironclaude - Development", id PVT_kwDODPJUp84Bo16j, owner's instruction "pick the most useful ones"): 
+- IronbellyOrg/IronClaude#642 (primary) and #643 (repeat). Both are closed "[ob-442 disposable T1]" and "[ob-442 disposable T2]" launch-level observation issues, Status Done, no Pipeline value.
+- Why these: they are the issues made to be disposable, they are closed, and their item has a Status value whose updatedAt already differs from createdAt. Every other item either is a real open issue or is not disposable.
+- The Pipeline field exists on the Project (options None, Worktree, Full, Full Submit); no item in the Project has a Pipeline value yet (checked on all 100 items listed).
+- Reads are the read-only GraphQL of Task 3 (Status and Pipeline createdAt and updatedAt of the issue's Project item). The executor changes nothing; the owner makes each change.
+
+### Issue #642, read: 0 before any change (read at 2026-11-19T16:43:19Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-18T19:39:55Z"},"pipeline":null}]}
+```
+
+### Issue #643, read: 0 before any change (read at 2026-11-19T16:43:19Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:28:03Z","updatedAt":"2026-11-18T19:39:56Z"},"pipeline":null}]}
+```
+
+### Issue #642, read: 1 after the owner set Pipeline to Worktree (read at 2026-11-19T17:11:11Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-18T19:39:55Z"},"pipeline":null}]}
+```
+
+### Issue #642, read: 1b re-read, same step (read at 2026-11-19T17:11:16Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-18T19:39:55Z"},"pipeline":null}]}
+```
+
+### Issue #642, read: 1c after the owner set Pipeline to Worktree (second attempt) (read at 2026-11-19T17:20:34Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Spec","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-19T17:20:09Z"},"pipeline":{"name":"Worktree","createdAt":"2026-11-19T17:20:06Z","updatedAt":"2026-11-19T17:20:06Z"}}]}
+```
+
+Note on reads 1, 1b and 1c: the first attempt (reads 1 and 1b, taken at 17:11) showed no Pipeline value, so no change had been saved then. After the owner's second attempt, read 1c shows the Pipeline set to Worktree at 17:20:06 and the Status already moved from Done to Spec at 17:20:09 (Status createdAt unchanged, updatedAt moved). Whoever made the Status move did it three seconds after the Pipeline change, so reads "after the Pipeline change" and "after the Status change" could not be taken apart; read 1c serves as both. The Status change moved only updatedAt, so the change time of a value is the later of createdAt and updatedAt (the rule Task 3 implements).
+
+### Issue #642, read: 2 after the owner created the approved field (no label applied) (read at 2026-11-19T17:27:39Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Spec","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-19T17:20:09Z"},"pipeline":{"name":"Worktree","createdAt":"2026-11-19T17:20:06Z","updatedAt":"2026-11-19T17:20:06Z"}}]}
+```
+
+### Issue #642, read: 3 after the owner set Approved to Yes (read at 2026-11-19T17:43:03Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Spec","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-19T17:20:09Z"},"pipeline":{"name":"Worktree","createdAt":"2026-11-19T17:20:06Z","updatedAt":"2026-11-19T17:20:06Z"}}]}
+```
+
+### Issue #642, read: 3b after the owner set Approved to Yes (second attempt) (read at 2026-11-19T18:24:35Z)
+```json
+{"labels":[],"items":[{"status":{"name":"Spec","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-19T17:20:09Z"},"pipeline":{"name":"Worktree","createdAt":"2026-11-19T17:20:06Z","updatedAt":"2026-11-19T17:20:06Z"}}]}
+```
+
+Field event read (read 3b, GraphQL timelineItems of issue 642, taken 2026-11-19 after the owner set the field): `IssueFieldAddedEvent`, createdAt 2026-11-19T18:23:59Z, actor `ironbelly` (User, databaseId 7361222), issueField `Approved`, value `Yes`. The REST `issue_field_values` of the issue now holds `Approved` = `Yes`. Read 3 (first attempt) found no value because the owner had set the issue type instead; read 3b is the valid last read.
+
+Comparison: between read 2 and read 3b the Status value (createdAt 2026-11-18T16:27:18Z, updatedAt 2026-11-19T17:20:09Z) and the Pipeline value (createdAt and updatedAt 2026-11-19T17:20:06Z) did not change, so setting `Approved` moved neither value time. The Pipeline set moved its own time (a new value has createdAt = updatedAt), and the Status move changed its updatedAt only. The `Approved` event carries the actor id, the time, the field name and the value, which Task 4a needs.
+
+Outcome: rule stands (R31 as written): a Status or Pipeline change moves the matching value time, setting `Approved` moves neither, and the field event names who set it and when. Observed on issue 642 in Project 2, a disposable closed issue; the executor changed nothing.

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
