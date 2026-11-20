037a20427733cd81a9a0cc2989110c4500579e1c
Review one task for spec compliance.

Task brief: ## Task 13: Close the Full Submit hole in the launch-level guard

Depends on: Task 6

Change `src/superclaude/hooks/scripts/launch-level-guard.sh` and its tracked mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` together (never `.claude/`). The H3 case today puts `issue create`, `issue edit` and `issue comment` in the SUBMIT row (line 653) and SUBMIT is allowed at Full Submit, so a Full Submit agent can write to issues today.

Make these changes in the guard. Remove the three issue verbs from line 653, so it reads `'pr create' | 'pr edit' | 'pr comment' | 'pr ready') LL_CLASSES+='SUBMIT ' ;;`. After the read-allow row at line 652 insert `'project item-list' | 'project field-list') ;;` and then `'issue '* | 'label '* | 'project '*) LL_CLASSES+='ISSUE ' ;;`, so the class fires wherever `gh` appears (not only in command position, unlike the UNKNOWN row at line 654) while `gh issue view`, `list` and `status` stay allowed. Add `ISSUE` to the `for LL_C in` list at line 786, after `GHWRITE`, because a class missing from that list is never evaluated; add `ISSUE:W | ISSUE:WA | ISSUE:F | ISSUE:FS) ll_deny LL-ISSUE ;;` to the case table. Add an `LL-ISSUE` block to the message printer with three parts: Blocked (a GitHub issue, label or project write), Why (only the coordinator writes; a launched session reports through `.dev/issues/<N>/result.md`), You can (write the result file and let the coordinator post). Reword the `LL-SUBMIT` text (lines 70 to 71) from "pull request or issue" to "pull request". Extend the coordinator-only pattern at line 444 with `*issue-pipeline[[:space:]]complete[[:space:]]*` and `*issue-pipeline[[:space:]]complete` (the verb word anchored by spaces, with its own end-of-text form), `*issue_pipeline.complete*`, `*issue_pipeline/complete.py*`, `*issue_pipeline*import*complete*` and `*issue_pipeline*complete.run*`. Never use `*issue-pipeline*complete*`, which refuses `plan-hash` for a path that contains the word completed, or `*issue_pipeline*complete*`, which refuses `uv run pytest tests/issue_pipeline/test_complete.py` in a launched session. The matcher runs on the command text with quotes and backslashes deleted and runs of `/` squeezed (guard line 428), so each alternative is a substring match on that text. The pattern is best effort, not a control; the grant-row rule (`WORKER-CONTRACT.md` line 300) is the control. Accepted over-match, with a test row: a governed command that names `issue_pipeline/complete.py` (`sed`, `git diff`, `ruff`) is refused. Known unmatched forms, stated in the task: string-built names (`getattr`, `importlib` with a split name). The refusal case `p.complete.run()` is written as a full statement that imports the module, because a bare `p.complete.run()` cannot run and no alternative matches it. Add `*.config/superclaude*` to the tamper tokens at line 764 (owner decision of 2026-11-19), with the stated over-match that any governed command whose text mentions that path is refused, reads included. Raise the version stamp from 1 to 2 together in line 10 of the guard and of the mirror, `GUARD_VERSION_LINE` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (line 839) and the three test pins (`tests/hooks/test_launch_level_guard.py` line 251, `tests/skills/test_issue_orca_worktree.py` lines 1283 and 1914 to 1916), so a host with the old guard fails the install preflight. The release note says hosts run `superclaude install --force` before the next claim. `stage-status` stays unclassified and the task says so.

Acceptance criteria:
- T13.AC1: `tests/hooks/test_launch_level_guard.py` moves the three issue rows (lines 2743 to 2745) out of the SUBMIT oracle into a new `ISSUE` row with `LL-ISSUE` at all four levels, removes them from the T-GH-5 list (lines 2875 to 2876), and adds the class to the expected-result grid. At Worktree, Worktree-allow, Full and Full Submit these are refused with `LL-ISSUE`: `gh issue create`, `gh issue edit 5 --add-label issue-watch:approved`, `gh issue comment 5`, `gh issue close 5`, `gh label create x`, `gh project item-edit`, `true && gh issue comment 5` and the `-R o/r` forms. These stay allowed at every level: `gh issue view 5`, `gh issue list`, `gh project item-list`, `gh project field-list`; `gh pr comment 5` still passes at Full Submit.
- T13.AC2: `tests/hooks/test_launch_level_guard.py` also asserts each new code prints a non-empty three-part message, that an edit or shell redirect on `issue-watch.json` under the config directory is refused, and that a guard stamped 1 is refused after the bump. It adds the unbound-session-allowed test, labelled "documents, does not endorse".
- T13.AC3: `tests/hooks/test_launch_level_guard_worker.py` shows these are refused with the tamper code: `superclaude issue-pipeline complete --repo o/r --issue 5`, the `uv run` form, `python -m superclaude.cli.issue_pipeline.complete`, `from superclaude.cli.issue_pipeline import complete`, `from superclaude.cli.issue_pipeline.complete import run`, `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` and `superclaude issue-pipeline complete` at the very end of the command text; and these stay allowed: `issue-pipeline plan-hash`, `check-approval`, `uv run pytest tests/issue_pipeline/test_complete.py`, `uv run pytest tests/issue_pipeline/test_complete_cli.py`, `plan-hash` with a path containing "completed" and `git commit -m "docs: complete the fu1 design"`. The accepted over-match has its own rows: governed `sed`, `git diff` and `ruff` on `issue_pipeline/complete.py` are refused.
- T13.AC4: `uv run pytest tests/hooks tests/skills tests/issue_pipeline tests/issue_watch -q` passes, `make verify-sync` is clean and no `.claude/` path is staged.
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
Start sha: 037a20427733cd81a9a0cc2989110c4500579e1c
Diff against the start snapshot: diff --git a/docs/designs/sc-issue-launch-level-hook.md b/docs/designs/sc-issue-launch-level-hook.md
index 064538caf..122c895a0 100644
--- a/docs/designs/sc-issue-launch-level-hook.md
+++ b/docs/designs/sc-issue-launch-level-hook.md
@@ -93,9 +93,9 @@ Valid id: a **top-level JSON string** matching `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}
 | NONE | A | A | A | A |
 | IMPL, TURN | B | A | A | A |
 | SUBMIT, COMMIT, PUSH, SKILL | B | B | B | A |
-| REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG | B | B | B | B |
+| REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, ISSUE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG | B | B | B | B |
 
-Message id is `LL-<class>`; PUSHFORM gives LL-PUSH-FORM, GHWRITE gives LL-GH-WRITE. Any blocked class blocks the call. Message precedence: BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL.
+Message id is `LL-<class>`; PUSHFORM gives LL-PUSH-FORM, GHWRITE gives LL-GH-WRITE. Any blocked class blocks the call. Message precedence: BIG, TAMPER, MERGE, GHWRITE, ISSUE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL.
 
 **Patterns (MR 6.2 rows).** Governed sessions; ordinary sessions always allow silently. Cells give A or the id without `LL-`. Full examples: MR 6.2 (DD-7).
 
@@ -107,6 +107,7 @@ Message id is `LL-<class>`; PUSHFORM gives LL-PUSH-FORM, GHWRITE gives LL-GH-WRI
 | 11 | CronCreate, ScheduleWakeup | TURN | TURN | A | A | A |
 | 5, 20, 21 | Skill `sc:pr-submit`; `gh pr comment 5`; `gh pr ready 5`; `gh pr create --repo "$REPO" ...` | SUBMIT | SUBMIT | SUBMIT | SUBMIT | A |
 | 22 | `gh pr create --title x` | SUBMIT, REPO | SUBMIT | SUBMIT | SUBMIT | REPO |
+| 20a (plan Task 13) | `gh issue create`; `gh issue comment 5`; `gh issue edit 5`; `gh issue close 5`; `gh label create x`; `gh project item-edit`. The reads `gh issue view`, `gh issue list`, `gh project item-list` and `gh project field-list` stay NONE. | ISSUE | ISSUE | ISSUE | ISSUE | ISSUE |
 | 7 | Skill with no name | SKILL | SKILL | SKILL | SKILL | A |
 | 13 | `git commit -m x`; `git revert x`; `sh -c "git commit -m x"`; ``git$'' commit -m x`` [B-2]; `git status && echo "I am done"` | COMMIT | COMMIT | COMMIT | COMMIT | A |
 | 14 | `git push -u origin feature`; `git push origin <sha>:feature` | PUSH | PUSH | PUSH | PUSH | A |
@@ -168,7 +169,7 @@ A git word outside command position gets no G3 class. **G4:** compute S with the
 
 No match: PUSHFORM. Match: destination is capture 5, else 3, minus one `refs/heads/` or else `heads/`; `master` or `main` gives PROTECTED; `HEAD` gives PUSHFORM. Accept: PA1 `git push origin feature`, PA4 `git push origin 3f2a9c1e:feature/x`, PA6 `git push origin feature/main:feature/main`. Reject: PR1 backtick, PR3 `git-push`, PR6 `--force`, PR13 `upstream`, PR15 `cd x && ...`, PR24 `origin --all`; PD1 `git push origin main` (PROTECTED). Full lists in MR.
 
-**gh (FR-L-35 to FR-L-39).** H1: group is the first non-option word after a gh word (skip `-R`, `--repo` values); action the next. H2: G holds a gh word and `api`: GHWRITE unless (1) raw `cmd` matches `^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$`, (2) no word after `api` matches `^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$`, (3) the endpoint exists, is not `graphql`, and does not end `/merge` or `/merges`. H3, first match wins: `api` no class; no group with `--version`/`--help` NONE; action `merge`, `update-branch`, `sync` MERGE anywhere [B-3]; group `alias`, `extension` or `$` in group or action UNKNOWN anywhere [B-3]; group `search status auth browse help completion` or action `view list status diff checks watch checkout` NONE; `pr create|edit|comment|ready`, `issue create|edit|comment` SUBMIT anywhere; else UNKNOWN in command position. H4: for each recognized `pr create` occurrence, require a nonempty operand after `-R`/`--repo`, or nonempty suffix in `--repo=<value>`, in that occurrence's segment; otherwise add REPO. A detached operand must not be another option. This replaces the anywhere-presence test, but normalization still loses quoted argument boundaries: option-looking title/body text can collide. That is a stated lexical limit, not validated repository selection; O-12 still does not compare the value to origin. H5: no gh word in the segment and a word with `repos/` ending `/merge(s)`: MERGE; a word with `api.github.com` or `uploads.github.com`: GHWRITE [B-7].
+**gh (FR-L-35 to FR-L-39).** H1: group is the first non-option word after a gh word (skip `-R`, `--repo` values); action the next. H2: G holds a gh word and `api`: GHWRITE unless (1) raw `cmd` matches `^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$`, (2) no word after `api` matches `^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$`, (3) the endpoint exists, is not `graphql`, and does not end `/merge` or `/merges`. H3, first match wins: `api` no class; no group with `--version`/`--help` NONE; action `merge`, `update-branch`, `sync` MERGE anywhere [B-3]; group `alias`, `extension` or `$` in group or action UNKNOWN anywhere [B-3]; group `search status auth browse help completion` or action `view list status diff checks watch checkout` NONE; `project item-list` and `project field-list` NONE; group `issue`, `label` or `project` ISSUE anywhere (plan Task 13: only the coordinator writes to an issue, a label or a Project); `pr create|edit|comment|ready` SUBMIT anywhere; else UNKNOWN in command position. H4: for each recognized `pr create` occurrence, require a nonempty operand after `-R`/`--repo`, or nonempty suffix in `--repo=<value>`, in that occurrence's segment; otherwise add REPO. A detached operand must not be another option. This replaces the anywhere-presence test, but normalization still loses quoted argument boundaries: option-looking title/body text can collide. That is a stated lexical limit, not validated repository selection; O-12 still does not compare the value to origin. H5: no gh word in the segment and a word with `repos/` ending `/merge(s)`: MERGE; a word with `api.github.com` or `uploads.github.com`: GHWRITE [B-7].
 
 **Tamper (FR-L-49 to FR-L-51).** T, or an edit path after the same `/` squeeze, contains `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config` or `.config/git` [B-4]. Bash only: a word ending `.claude` or `.claude/`; a `superclaude` or `superclaude.*` word followed later in the segment by `install` [B-9]; a word containing `install_hooks`. Edit tools only: a `/../` segment or trailing `/..`. Contents, prompts and arguments are never checked.
 
@@ -240,7 +241,8 @@ To stderr, then exit 2. Header: `Launch-level guard: this session was started by
 | LL-PROTECTED | a push to master or main. | No launch level may change the main branch. | Push the feature branch by name, then merge it through a reviewed pull request. |
 | LL-MERGE | a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool). | No launch level may merge; only a person reviews and merges. | Leave the merge to a person. To update the branch, run git fetch, then git rebase. |
 | LL-GH-WRITE | a gh api call that is not one plain read command (it sets a method, a field or an input, calls graphql or a merge endpoint, or uses variables, quotes, pipes or other commands around it), or a gh command whose text mentions api, or a direct call to the GitHub API [B-7]. | In a launched session gh api may only read, and only in a form the guard can check: a gh api write can merge, comment or change the main branch. | Run the read as one plain command with every value written out, for example gh api repos/o/r/pulls/5 --jq .state, or use a gh command for the step (gh pr view --json, gh pr comment, gh pr create --repo ...) at a level that allows it, or ask the person. |
-| LL-SUBMIT | /sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue). | Publishing work needs a launch with --pipeline full --submit. | Run it yourself in your own session, or claim the issue again with --pipeline full --submit. |
+| LL-ISSUE | a GitHub issue, label or project write (gh issue create, edit, comment or close, gh label, gh project item-edit). | Only the coordinator writes to an issue, a label or a Project, under that issue grant row; a launched session reports through its result file. | Write .dev/issues/<N>/result.md (outcome, artifacts, pull_request) and let the coordinator post it. |
+| LL-SUBMIT | /sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request). | Publishing work needs a launch with --pipeline full --submit. | Run it yourself in your own session, or claim the issue again with --pipeline full --submit. |
 | LL-REPO | gh pr create without --repo. | Without --repo, gh can open the pull request on the parent repository of a fork. | Retry with --repo <owner>/<name> (or -R). |
 | LL-UNKNOWN | a git or gh command the guard does not recognise (an unknown subcommand, a git alias definition, or a subcommand built from a variable or a substitution), or a line continuation inside a word [B-1]. | In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge. | Use the standard command written out (for example git status, git diff, git add), or ask the person to run it. Write the command on one line [B-1]. |
 | LL-MCP | a GitHub write through an MCP tool. | The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh. | Use git or gh for this step. |
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 536ccaefe..1e36b607a 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -7,7 +7,7 @@
 # governed; every other session is ordinary and never blocked (FR-L-53).
 # Ten-part layout (DD-1); part 8 holds the section 5.2 classifiers (Skill, Bash,
 # Monitor, edits, Agent/Task, Cron/Schedule, escape and MCP tools); others NONE.
-# launch-level-guard-version: 1
+# launch-level-guard-version: 2
 
 # 1. Settings
 export LC_ALL=C
@@ -68,9 +68,13 @@ ll_say() {
         w='In a launched session gh api may only read, and only in a form the guard can check: a gh api write can merge, comment or change the main branch.'
         y='Run the read as one plain command with every value written out, for example gh api repos/o/r/pulls/5 --jq .state, or use a gh command for the step (gh pr view --json, gh pr comment, gh pr create --repo ...) at a level that allows it, or ask the person.' ;;
     LL-SUBMIT)
-        b='/sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue).'
+        b='/sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request).'
         w='Publishing work needs a launch with --pipeline full --submit.'
         y='Run it yourself in your own session, or claim the issue again with --pipeline full --submit.' ;;
+    LL-ISSUE)
+        b='a GitHub issue, label or project write (gh issue create, edit, comment or close, gh label, gh project item-edit).'
+        w='Only the coordinator writes to an issue, a label or a Project, under that issue grant row; a launched session reports through its result file.'
+        y='Write .dev/issues/<N>/result.md (outcome, artifacts, pull_request) and let the coordinator post it.' ;;
     LL-REPO)
         b='gh pr create without --repo.'
         w='Without --repo, gh can open the pull request on the parent repository of a fork.'
@@ -441,7 +445,14 @@ if [ "$LL_BRANCH" = tool ]; then
             # G2: the coordinator-side issue-pipeline commands write the approval rows and the
             # worker's release (.ok) file; a bound worker must not run them (plan-hash and
             # check-approval stay allowed: the worker needs them).
-            case $T in *release-worker* | *release_worker* | *issue-pipeline*adopt-* | *issue-pipeline*record-* | *issue_pipeline*release* | *issue_pipeline*approval_record*) LL_CLASSES+='TAMPER ' ;; esac
+            # `issue-pipeline complete` writes the result comment and moves the Status; it is the
+            # coordinator's alone. The verb word is anchored by a space (with its own end-of-text
+            # form) so `plan-hash` on a path containing "completed" and `pytest
+            # tests/issue_pipeline/test_complete.py` stay allowed. Best effort, not a control: the
+            # grant-row rule of WORKER-CONTRACT.md is the control. Accepted over-match: a governed
+            # command that names issue_pipeline/complete.py (sed, git diff, ruff) is refused.
+            # Not matched: names built from strings (getattr, importlib with a split name).
+            case $T in *release-worker* | *release_worker* | *issue-pipeline*adopt-* | *issue-pipeline*record-* | *issue_pipeline*release* | *issue_pipeline*approval_record* | *issue-pipeline[[:space:]]complete[[:space:]]* | *issue-pipeline[[:space:]]complete | *issue_pipeline.complete* | *issue_pipeline/complete.py* | *issue_pipeline*import*complete* | *issue_pipeline*complete.run*) LL_CLASSES+='TAMPER ' ;; esac
             LL_CL=0 LL_CF=0 LL_SA=0 # a claude word; a claude launch flag word (whole command); an orca send or ask word
             LL_GLOB=0 # once per command: a glob character in the text
             case $T in *[\*\?\[\{]*) LL_GLOB=1 ;; esac
@@ -650,7 +661,9 @@ if [ "$LL_BRANCH" = tool ]; then
                             'alias '* | 'extension '* | *'$'*) LL_CLASSES+='UNKNOWN ' ;;
                             'search '* | 'status '* | 'auth '* | 'browse '* | 'help '* | 'completion '*) ;;
                             *' view' | *' list' | *' status' | *' diff' | *' checks' | *' watch' | *' checkout') ;;
-                            'pr create' | 'pr edit' | 'pr comment' | 'pr ready' | 'issue create' | 'issue edit' | 'issue comment') LL_CLASSES+='SUBMIT ' ;;
+                            'project item-list' | 'project field-list') ;;
+                            'issue '* | 'label '* | 'project '*) LL_CLASSES+='ISSUE ' ;;
+                            'pr create' | 'pr edit' | 'pr comment' | 'pr ready') LL_CLASSES+='SUBMIT ' ;;
                             *) [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
                             esac
                             # H4: each pr create needs a nonempty repo operand in its own segment.
@@ -761,8 +774,11 @@ if [ "$LL_BRANCH" = tool ]; then
     # FR-L-49: the tamper tokens in T or the edit path; the store part is
     # built from LL_S1 and LL_S2, so this text never names it joined.
     case $LL_TT in
-    *"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git*) LL_CLASSES+='TAMPER ' ;;
+    *"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git* | *.config/superclaude*) LL_CLASSES+='TAMPER ' ;;
     esac
+    # *.config/superclaude* (owner decision of 2026-11-19) protects the watcher config and the
+    # approvers file. Accepted over-match: any governed command whose text mentions that path
+    # is refused, reads included.
     # FR-050..FR-052 (#441): the git pre-push hook, its data file, --no-verify
     # and hook config, lowercased so case changes do not slip past. The config
     # transports (--config-env, GIT_CONFIG_*) are left to their L1 classes (SD-2).
@@ -783,7 +799,7 @@ if [ "$LL_BRANCH" = tool ]; then
 
     # 9. One case on CLASS:LEVEL, taken in message precedence; any blocked class
     # blocks the call with the first blocked class's message.
-    for LL_C in BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL; do
+    for LL_C in BIG TAMPER MERGE GHWRITE ISSUE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL; do
         case $LL_CLASSES in *" $LL_C "*) ;; *) continue ;; esac
         case $LL_C:$LL_LEVEL in
         IMPL:WA | IMPL:F | IMPL:FS | TURN:WA | TURN:F | TURN:FS) ;;
@@ -796,6 +812,7 @@ if [ "$LL_BRANCH" = tool ]; then
         PROTECTED:W | PROTECTED:WA | PROTECTED:F | PROTECTED:FS) ll_deny LL-PROTECTED ;;
         MERGE:W | MERGE:WA | MERGE:F | MERGE:FS) ll_deny LL-MERGE ;;
         GHWRITE:W | GHWRITE:WA | GHWRITE:F | GHWRITE:FS) ll_deny LL-GH-WRITE ;;
+        ISSUE:W | ISSUE:WA | ISSUE:F | ISSUE:FS) ll_deny LL-ISSUE ;;
         UNKNOWN:W | UNKNOWN:WA | UNKNOWN:F | UNKNOWN:FS) ll_deny LL-UNKNOWN ;;
         MCP:W | MCP:WA | MCP:F | MCP:FS) ll_deny LL-MCP ;;
         ESCAPE:W | ESCAPE:WA | ESCAPE:F | ESCAPE:FS) ll_deny LL-ESCAPE ;;

Re-review scope: only F1.1 (design doc line 172 now names ISSUE). Check it against src/superclaude/hooks/scripts/launch-level-guard.sh H3 case rows and report any other design-doc sentence that still contradicts the guard.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 037a20427733cd81a9a0cc2989110c4500579e1c
tree=none
F1.1 ac=scope at=docs/designs/sc-issue-launch-level-hook.md:172 anchor="`pr create|edit|comment|ready`, `issue create|edit|comment` SUBMIT anywhere" chk=n,y,n,n family=design-doc-h3-stale fix=rewrite the H3 sentence sev=blocking trigger=B4 first=start origin=new: the H3 prose still said the issue verbs are SUBMIT

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
