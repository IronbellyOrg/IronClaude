1209e2d53846e31d2ad2d81e901df0013556a06d
Review one task for spec compliance.

Task brief: ## Task 2: Update the design and runbook text for the Status rule

Edit `docs/designs/issue-watcher.md` (the lines naming Backlog: 15, 21, 692 and 884) and `docs/designs/issue-watcher-setup.md` (lines 189 and 366) so they state the allow-list of Task 1: Research, Spec, Plan and Debug act; Backlog, Ready, In progress, In review and Done never do; a new status is blocked until added. Line 15 of `issue-watcher.md` says the cycle finds issues "in the Project's Backlog column"; it is rewritten with the others. Add one sentence to `docs/designs/issue-watcher.md` that this reverses the original issue 331 rule ("Issues must be in Backlog status"), by owner decision of 2026-11-18.

Depends on: Task 1

Acceptance criteria:
- T2.AC1: `grep -n "Backlog" docs/designs/issue-watcher.md docs/designs/issue-watcher-setup.md` shows no line that says Backlog is the status that allows action, line 15 included.
- T2.AC2: Both files list the four allowed statuses by name.
- T2.AC3: `uv run pytest tests/docs -q` passes.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval label, the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the approval label after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 1209e2d53846e31d2ad2d81e901df0013556a06d
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-setup.md b/docs/designs/issue-watcher-setup.md
index 1a1fa2c2d..f162dacd3 100644
--- a/docs/designs/issue-watcher-setup.md
+++ b/docs/designs/issue-watcher-setup.md
@@ -186,7 +186,7 @@ gh issue edit 42 --repo IronbellyOrg/IronClaude --add-label issue-watch:approved
 
 Two more conditions are checked on every cycle, so prepare them before step 3:
 
-- The issue must be on the Project of `project_id`, in the Backlog status, and not archived. Otherwise it is skipped as `project_mismatch` (or `project_unreadable` when the Project cannot be read).
+- The issue must be on the Project of `project_id`, in one of the allowed statuses (Research, Spec, Plan or Debug; Backlog, Ready, In progress, In review and Done never act, and a new status is blocked until it is added), and not archived. Otherwise it is skipped as `project_mismatch` (or `project_unreadable` when the Project cannot be read).
 - Nothing may change after the approval. An edit to the issue body or title, or a comment by anyone other than the watcher's own login, made at or after the approval time makes the issue `edited_after_approval`. Finish all edits first, then approve.
 
 ## 7. Shadow rollout
@@ -363,7 +363,7 @@ The audit log accepts only the 59 names below (`REASON_TABLE` in the package's `
 | 0 | decision, skip | `events_incomplete` | The label history cannot be trusted: two label events in the same second, or no trigger label event found |
 | 0 | decision, skip | `events_unreadable` | The label history could not be read |
 | 0 | decision, skip | `edited_after_approval` | The issue body or title, or a comment by someone else, changed at or after the approval |
-| 0 | decision, skip | `project_mismatch` | The issue is not on the configured Project, not in Backlog, or archived |
+| 0 | decision, skip | `project_mismatch` | The issue is not on the configured Project, not in Research, Spec, Plan or Debug, or archived |
 | 0 | decision, skip | `project_unreadable` | The Project could not be read for this issue |
 | 0 | decision, skip | `unassigned` | The issue has no assignee |
 | 0 | decision, skip | `assigned_other` | The assignee set is not exactly the watcher's login |
diff --git a/docs/designs/issue-watcher.md b/docs/designs/issue-watcher.md
index ba80234a6..7134a1f62 100644
--- a/docs/designs/issue-watcher.md
+++ b/docs/designs/issue-watcher.md
@@ -12,13 +12,13 @@
 
 The binding requirements are `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (cited below as "spec", with section numbers and FR/NFR ids). `spec-refactor-log.md` in the same folder is context only. This document turns the spec into modules, interfaces, schemas, call contracts and tests. It contains no implementation code: signatures, dataclass field lists, JSON schemas and short pseudo-flow only.
 
-**What is built.** A poller that runs inside one person's Coder workspace. Every 5 minutes (cadence comes from a cron entry that is a follow-up, FU-2) it runs one cycle with that workspace's own `gh` login. A cycle finds issues on IronbellyOrg/IronClaude that are tagged, assigned exactly to the own login, approved by an allow-listed human, unchanged since approval and in the Project's Backlog column. For at most one such issue per cycle it starts one ordinary top-level agent session through `orca agent launch` with the prompt `/sc:issue --claim <N>`, after durably recording the dispatch.
+**What is built.** A poller that runs inside one person's Coder workspace. Every 5 minutes (cadence comes from a cron entry that is a follow-up, FU-2) it runs one cycle with that workspace's own `gh` login. A cycle finds issues on IronbellyOrg/IronClaude that are tagged, assigned exactly to the own login, approved by an allow-listed human, unchanged since approval and in one of the Project's allowed Status columns (Research, Spec, Plan or Debug; Backlog, Ready, In progress, In review and Done never act, and a status added to the board later is blocked until it is added to the allow-list). This reverses the original issue 331 rule ("Issues must be in Backlog status"), by owner decision of 2026-11-18. For at most one such issue per cycle it starts one ordinary top-level agent session through `orca agent launch` with the prompt `/sc:issue --claim <N>`, after durably recording the dispatch.
 
 **Guarantee (spec section 1).** At most one claim session per issue per intact, single dispatch store per login. A restored older backup (R11) or a second store on the same login (R12) breaks it; both are documented residual risks.
 
 | Root cause (spec RC) | What this design does about it | Where |
 |---|---|---|
-| RC1 No "ready" signal exists | Trigger label plus approval label, approval actor checked against an allow-list, Project Status `Backlog` | sections 6, 8 |
+| RC1 No "ready" signal exists | Trigger label plus approval label, approval actor checked against an allow-list, Project Status one of `Research`, `Spec`, `Plan`, `Debug` | sections 6, 8 |
 | RC2 The claim routes to whoever runs it | `is_intended_owner`: assignee set exactly {own login}; discovery pre-filters with `--assignee` | sections 5, 8 |
 | RC3 Nothing enforces at-most-once | Local dispatch record written durably (`pending`, `launches` + 1) before the spawn, plus the claim marker | section 7 |
 
@@ -689,7 +689,7 @@ The worst case is therefore 120 s of reads, then a 120 s launch, ending at 240 s
 | Comment author login | G4, G5 | `str`, compared with the own login | no | no |
 | Comment or issue body | never fetched as text | `bool` (`marker`) | no | no |
 | Timestamps | G3 to G5 | `datetime` after strict ISO parse | no | `approved_at` |
-| Project id, Status option | G6 | `str`, compared with config and `"Backlog"` | no | no |
+| Project id, Status option | G6 | `str`, compared with config and the allowed Status names (`Research`, `Spec`, `Plan`, `Debug`) | no | no |
 | `gh` stderr | runner | `str`, at most 500 bytes | no | no (stderr fallback lines carry a reason only) |
 | Orca stdout | launch | parsed JSON; only the operation id kept | no | `operation_id` after `^[A-Za-z0-9._:-]{1,128}$` |
 
@@ -881,7 +881,7 @@ All criteria run under `uv run pytest tests/issue_watch/` with fakes or PATH stu
 | AC-1 | One `once` runs the FR-001 order; `FakeRunner` sees G1 first and no argv after an exit decision | FR-001, FR-002 |
 | AC-2 | Discovery argv equals the FR-003 literal; 100 results or a repeated number exits 4 | FR-003, FR-004 |
 | AC-3 | Approval table: outsider, bot, unlabel, relabel, incomplete history, edit after approval each skip with their reason | FR-005, FR-006 |
-| AC-4 | Project and owner tables: wrong project, not Backlog, unassigned, other assignee skip | FR-007, FR-008 |
+| AC-4 | Project and owner tables: wrong project, a status that is not Research, Spec, Plan or Debug, unassigned, other assignee skip | FR-007, FR-008 |
 | AC-5 | An own-login marker comment yields `claimed` and no launch | FR-009 |
 | AC-6 | `pending` with `launches` 1 is saved before the launcher is called; the re-read failure skips | FR-010, FR-011 |
 | AC-7 | Every recorded prompt matches the D3 regex over the hostile corpus; non-int input raises | FR-012, NFR-001 |

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
