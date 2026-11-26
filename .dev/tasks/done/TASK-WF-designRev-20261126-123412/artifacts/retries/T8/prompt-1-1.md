060e9d10b1836239af7eb329ee26273157a85595
Review one task for spec compliance.

Task brief: ## Task 8: Run the final tests and write the pull request evidence notes

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7

Files written: ./artifacts/final-tests.log and ./artifacts/pr-body-notes.md (./source.md sections 4, 5 and 6). Run the 16 test files listed in ./source.md section 5 with `uv run pytest <files> -q` and save the output to ./artifacts/final-tests.log. Do not cite `make verify-sync` as evidence for the guide: its target does not compare core files.

./artifacts/pr-body-notes.md holds the material for the pull request body:
- The decisions table (owner decisions D1 to D6, the last owner question Q1, meeting rules M1 to M4, review row V1, all defined in `.dev/brainstorms/20261126-031900-primitive-contribution-rules/merged-requirements.md`), each mapped to the file that carries it; D6 (skill-creator fork) reads "deferred, no follow-up issue established; recorded here only".
- Baseline and final test results side by side, and the form schema check result for `feature_request.yml` (from ./artifacts/baseline-tests.log, ./artifacts/final-tests.log and ./artifacts/form-schema-check.md), with a line saying that the operator checks both forms at commit 2.
- The statement that the pull request template section appears only on pull requests opened in the GitHub web interface, because `/sc:pr-submit` passes `--body`.
- A request for a merge commit, because squash and rebase merges rewrite the commit that the deck footer names and both are enabled on the repository.
- The commit-time steps, in this order, for the operator:
  - Start only after `/sc:implement` reports the package archived.
  - Commit 1: the guide and its plugin copy, with explicit paths (`git commit -m "<message>" -- src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`) so that a staged `.dev/tasks` is not swept in.
  - Commit 2: `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms and the pull request template. Check zero deletions on all of them except `.github/ISSUE_TEMPLATE/feature_request.yml`, which replaces exactly one line (the `proposal` description); run `yaml.safe_load` and the schema check on both forms. Commit these five files with explicit paths (`git commit -m "<message>" -- <the five files>`), for the same reason as commit 1.
  - Run `git fetch origin`. If `git merge-base --is-ancestor origin/integration HEAD` exits non-zero, run `git rebase --autostash origin/integration`; it sets aside the uncommitted deck edit and any staged files and re-applies them. If git prints 'Applying autostash resulted in conflicts', resolve the markers so that the eyebrow, heading, intro and second card of slide `s12` equal Task 7's text, then find the kept 'autostash' entry by the SHA git printed at 'Created autostash:' (`git stash list --format='%h %gd'`; read the position again right before dropping, because the stash list is shared) and drop only that entry; never run `git stash pop`. If the rebase itself stops on a conflict in commit 1 or commit 2, resolve it and run `git rebase --continue`; the autostash is applied only after the rebase ends. After the rebase, copy the guide over the plugin twin if `cmp` reports a difference (commit the twin on its own), then re-run `cmp` and the 16 test files. Check scope with `git diff --name-only origin/integration...HEAD -- . ':(exclude).dev/tasks'`: it lists the files committed so far (seven before commit 3, eight after it, and no others even after review-fix commits).
  - Redo the slide review in ./artifacts/deck-slide-review.md against the guide at commit 1.
  - Move the footer only when that review is all "consistent" after the rebase: set it to the output of `git rev-parse --short=8` for commit 1. Otherwise leave the footer unchanged, mark the footer requirement in the pull request notes "pending, blocked by recorded mismatches", and name the follow-up issue to file.
  - Commit 3: the deck.
  - Run the two guide-equality checks `git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md` and `git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md`, where `<sha>` is the `git rev-parse --short=8` form of commit 1 as it stands after any rebase; both must exit 0 (the first passes trivially when `<sha>` is the newest guide commit; the second and the footer comparison are the real guards), and the footer must equal `<sha>` unless it is marked pending. After any later rebase (done as the rebase step above) or review-fix commit, set `<sha>` to `git rev-parse --short=8 $(git log -1 --format=%H origin/integration..HEAD -- src/superclaude/core/HOW-WE-WORK.md)`, the newest branch commit that changed the guide; if it prints nothing, stop and report. If the footer differs from `<sha>` and is not marked pending, redo the slide review against the guide at `<sha>` and apply the footer step above with `<sha>` in place of commit 1: move the footer and commit the deck only when the review is all 'consistent', otherwise leave it and mark it pending. Then run the two checks once more.
  - Stage only the eight files of commits 1 to 3 (the guide, its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, the two issue forms, the pull request template and the deck) and `.dev/tasks`; never `.claude/` or `.dev/issues/`.
  - Re-publishing the deck to the same link is an operator step to verify after merge.
- Manual checks, all marked "operator, after push, not run by the executor", each with the result "pending": the five scenarios of ./source.md section 5 (a missing-skill request, a broken-skill report answering "solution unknown", a non-primitive request, a primitive pull request, a non-primitive pull request showing "Not applicable"), and slide `s12` at narrow, wide and print widths. The width check exists because the new card is longer than its neighbour in a two-column grid.
- The owner inputs still missing, copied verbatim from ./source.md section 6.
- The six owner follow-ups not done here, copied from ./source.md section 6: a routing-table row sending "propose or change a skill, command or agent" to `/sc:issue --create` (accepted risk: `/sc:recommend` never reads section 4); making `/sc:pr-submit` include the primitive section; the same pointer in root `CLAUDE.md`, `README.md` and `docs/developer-guide/README.md`; fixing the stale `--base master` in `CONTRIBUTING.md`; a permanent policy test; and the monolith-or-modules question.
- The two additions beyond the files the issue names (the bug form sentence and the `CONTRIBUTING.md` paragraph), with the reason.

Acceptance criteria:
- ./artifacts/final-tests.log exists, and every one of the 16 test files passes or fails only where ./artifacts/baseline-tests.log shows the same failure.
- ./artifacts/pr-body-notes.md contains every item listed above, names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing "your lead" are allowed), and states that these checks prove wording and agreement of the surfaces, not that the future gate works.
- `git diff --name-only <base> -- . ':(exclude).dev/tasks'`, where `<base>` is the SHA in ./artifacts/base-sha.txt, lists exactly these eight files and no path under `.claude/`: `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/onboarding/ironclaude-onboarding.html`.
- `git ls-files --others --exclude-standard -- . ':(exclude).dev'` prints nothing.

AC ids (source order):
T8.AC1: ./artifacts/final-tests.log exists, and every one of the 16 test files passes or fails only where ./artifacts/baseline-tests.log shows the same failure.
T8.AC2: ./artifacts/pr-body-notes.md contains every item listed above, names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing "your lead" are allowed), and states that these checks prove wording and agreement of the surfaces, not that the future gate works.
T8.AC3: `git diff --name-only <base> -- . ':(exclude).dev/tasks'`, where `<base>` is the SHA in ./artifacts/base-sha.txt, lists exactly these eight files and no path under `.claude/`: `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/onboarding/ironclaude-onboarding.html`.
T8.AC4: `git ls-files --others --exclude-standard -- . ':(exclude).dev'` prints nothing.
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: 060e9d10b1836239af7eb329ee26273157a85595
Diff against the start snapshot: 
--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/pr-body-notes.md (full contents, 96 lines)
# Pull request evidence notes for issue 290

Material for the pull request body. Written by Task 8 of this package. Sources: ./artifacts/baseline-tests.log, ./artifacts/final-tests.log, ./artifacts/form-schema-check.md, ./artifacts/deck-slide-review.md and ./source.md sections 4 to 6.

## What these checks prove

These checks prove wording and agreement of the five surfaces (the guide, the contribution guide, the issue forms, the pull request template and the deck), not that the future gate works. The gate is not available yet: its metric, its threshold and its approving role are not set.

## Decisions table

Defined in `.dev/brainstorms/20261126-031900-primitive-contribution-rules/merged-requirements.md`. Owner = the owner's comment 6492018865 on the issue; meeting = 2026-10-22; review = the 2026-11-23 comment (a recommendation, not a decision).

| ID | Decision (source) | Carried by |
|---|---|---|
| D1 | Basics live in HOW-WE-WORK; the contributing guide is a pointer (owner) | `src/superclaude/core/HOW-WE-WORK.md` section 4; `docs/developer-guide/contributing-code.md`; `CONTRIBUTING.md` |
| D2 | New members only file issues until a CI-triggered evaluation exists (owner) | the guide; the contribution guide; `.github/PULL_REQUEST_TEMPLATE.md`; the deck slide s12; `CONTRIBUTING.md` |
| D3 | Future primitive pull requests use a pull request template; a reviewer approves first, then a CI evaluation must meet an ROI threshold (owner) | the guide; `.github/PULL_REQUEST_TEMPLATE.md` |
| D4 | Add intake for a missing or broken skill, including improvements (owner) | the guide; `.github/ISSUE_TEMPLATE/feature_request.yml`; `.github/ISSUE_TEMPLATE/bug_report.yml` |
| D5 | Dependent skills are found and revalidated through a skills registry (owner) | interim: issues name known callers; the pull request template asks that they be rechecked |
| D6 | Fork skill-creator (owner) | deferred, no follow-up issue established; recorded here only |
| Q1 | The owner's last question: monolith first or modular blocks first | recorded only, out of scope |
| M1 | Do not create new skills or commands yet; file an issue saying why (meeting) | the guide |
| M2 | Run `/sc:recommend --plugin` first (meeting). Corrected: it searches outside sources only, so check locally first | the guide; the improvement form |
| M3 | Changes go in `src/superclaude/` and reach users through the installer (meeting). Corrected: not "only after update" | the guide |
| M4 | A change needs evidence it adds value, not bloat; a change can break callers (meeting) | the pull request template |
| V1 | Keep the contributing guide's maintainer detail; extend the existing form and pull request template; replace only the contribution card (review) | the contribution guide; the forms and the template; the deck |

## Test and schema results

| Run | Result | Log |
|---|---|---|
| Baseline, the 16 test files on the unedited tree | 647 passed in 4.82s | ./artifacts/baseline-tests.log, line 36 |
| Final, the same 16 test files after all edits | 647 passed in 4.76s | ./artifacts/final-tests.log, line 36 |

Form schema check for `feature_request.yml`: valid against the public GitHub issue-form JSON schema (0 errors); the ids are `problem`, `proposal`, `alternatives`, `primitive`, `reuse_search` and `affected_callers`; the three new fields are optional; exactly one line was replaced (the `proposal` description). See ./artifacts/form-schema-check.md. The executor also validated `bug_report.yml` against the same schema (0 errors; ./artifacts/t5-checks.log). The operator checks both forms again at commit 2.

## Pull request template note

The new pull request template section appears only on pull requests opened in the GitHub web interface, because `/sc:pr-submit` passes `--body` and so does not use the template.

## Merge request

Request a merge commit. Squash and rebase merges rewrite the commit that the deck footer names, and both are enabled on the repository.

## Commit-time steps, in this order, for the operator

- Start only after `/sc:implement` reports the package archived.
- Commit 1: the guide and its plugin copy, with explicit paths (`git commit -m "<message>" -- src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`) so that a staged `.dev/tasks` is not swept in.
- Commit 2: `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms and the pull request template. Check zero deletions on all of them except `.github/ISSUE_TEMPLATE/feature_request.yml`, which replaces exactly one line (the `proposal` description); run `yaml.safe_load` and the schema check on both forms. Commit these five files with explicit paths (`git commit -m "<message>" -- <the five files>`), for the same reason as commit 1.
- Run `git fetch origin`. If `git merge-base --is-ancestor origin/integration HEAD` exits non-zero, run `git rebase --autostash origin/integration`; it sets aside the uncommitted deck edit and any staged files and re-applies them. If git prints 'Applying autostash resulted in conflicts', resolve the markers so that the eyebrow, heading, intro and second card of slide `s12` equal Task 7's text, then find the kept 'autostash' entry by the SHA git printed at 'Created autostash:' (`git stash list --format='%h %gd'`; read the position again right before dropping, because the stash list is shared) and drop only that entry; never run `git stash pop`. If the rebase itself stops on a conflict in commit 1 or commit 2, resolve it and run `git rebase --continue`; the autostash is applied only after the rebase ends. After the rebase, copy the guide over the plugin twin if `cmp` reports a difference (commit the twin on its own), then re-run `cmp` and the 16 test files. Check scope with `git diff --name-only origin/integration...HEAD -- . ':(exclude).dev/tasks'`: it lists the files committed so far (seven before commit 3, eight after it, and no others even after review-fix commits).
- Redo the slide review in ./artifacts/deck-slide-review.md against the guide at commit 1.
- Move the footer only when that review is all "consistent" after the rebase: set it to the output of `git rev-parse --short=8` for commit 1. Otherwise leave the footer unchanged, mark the footer requirement in the pull request notes "pending, blocked by recorded mismatches", and name the follow-up issue to file.
- Commit 3: the deck.
- Run the two guide-equality checks `git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md` and `git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md`, where `<sha>` is the `git rev-parse --short=8` form of commit 1 as it stands after any rebase; both must exit 0 (the first passes trivially when `<sha>` is the newest guide commit; the second and the footer comparison are the real guards), and the footer must equal `<sha>` unless it is marked pending. After any later rebase (done as the rebase step above) or review-fix commit, set `<sha>` to `git rev-parse --short=8 $(git log -1 --format=%H origin/integration..HEAD -- src/superclaude/core/HOW-WE-WORK.md)`, the newest branch commit that changed the guide; if it prints nothing, stop and report. If the footer differs from `<sha>` and is not marked pending, redo the slide review against the guide at `<sha>` and apply the footer step above with `<sha>` in place of commit 1: move the footer and commit the deck only when the review is all 'consistent', otherwise leave it and mark it pending. Then run the two checks once more.
- Stage only the eight files of commits 1 to 3 (the guide, its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, the two issue forms, the pull request template and the deck) and `.dev/tasks`; never `.claude/` or `.dev/issues/`.
- Re-publishing the deck to the same link is an operator step to verify after merge.

## Deck footer status

The slide review (./artifacts/deck-slide-review.md, run against the guide as edited by Task 1) recorded four mismatches, so the deck footer requirement is "pending, blocked by recorded mismatches": the footer stays at its current value and no task edited it. The follow-up issue to file lists the four mismatches. None was edited here, because Task 7 records mismatches on other slides and the worktree card of slide s12 must stay byte-identical (issue 289 is out of scope).

- s1 (deck line 181 and footer line 580): says the guide does not hold `--plugin` ("the one exception"), but the new guide section 4 bullet names `/sc:recommend --plugin`; this one is partly new, caused by this change.
- s4 (deck line 268): says a command is a thin front door to a skill; the guide says commands whose file names no skill (for example `/sc:help`) run from their own file.
- s7 (deck lines 382 and 400 to 403): puts "Review: automatic on the PR" before "Open PR"; the slide reviewer reads guide section 3.11 as opening the pull request first and then waiting for the review app, which can be absent. This is the reviewer's reading; it has not been re-checked by a second reader.
- s12, first card (deck line 523): says where worktrees live is still being worked out; guide line 366 already says Orca creates worktrees at its default paths.

## Manual checks

All marked "operator, after push, not run by the executor"; each result is "pending".

- A missing-skill request: file the improvement form for a skill that does not exist (result: pending).
- A broken-skill report that answers "solution unknown" in the improvement form (result: pending).
- A non-primitive request through the improvement form, leaving the three new fields blank (result: pending).
- A pull request that changes a skill, command or agent, opened in the web interface (result: pending).
- A pull request that changes none, showing "Not applicable" (result: pending).
- Slide s12 at narrow, wide and print widths (result: pending). The width check exists because the new card is longer than its neighbour in a two-column grid.

## Owner inputs still missing

Copied verbatim from ./source.md section 6: Owner inputs still missing (named, not filled): evaluation success metric; numeric ROI threshold; approving role and who triages proposal issues; what "new team member" means and when the restriction ends; proof that a CI evaluation runs on primitive PRs (issue 487 is open); owner of caller discovery and revalidation without a registry; issue numbers for the skills registry and the skill-creator fork.

## Owner follow-ups not done here

- A routing-table row sending "propose or change a skill, command or agent" to `/sc:issue --create` (accepted risk: `/sc:recommend` never reads section 4).
- Making `/sc:pr-submit` include the primitive section.
- The same pointer in root `CLAUDE.md`, `README.md` and `docs/developer-guide/README.md`.
- Fixing the stale `--base master` in `CONTRIBUTING.md`.
- A permanent policy test.
- The monolith-or-modules question.

## Additions beyond the files the issue names

- The bug form sentence (`.github/ISSUE_TEMPLATE/bug_report.yml`): without it a member who finds a broken skill would use the bug form, which does not ask the reuse and caller questions.
- The `CONTRIBUTING.md` paragraph: GitHub links this file from the new-issue and new-pull-request pages, and without the pointer it would stay silent on the rule while the guide states it.

Both are additive one-line changes that stop two entry points from contradicting the rule.


--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t8-checks.log (full contents, 32 lines)
# T8 checks

## final log summary line:
============================= 647 passed in 4.76s ==============================
## baseline log summary line:
============================= 647 passed in 4.82s ==============================
## git diff --name-only <base> -- . ':(exclude).dev/tasks' (must be exactly the eight files):
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/PULL_REQUEST_TEMPLATE.md
CONTRIBUTING.md
docs/developer-guide/contributing-code.md
docs/onboarding/ironclaude-onboarding.html
plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
src/superclaude/core/HOW-WE-WORK.md
SCOPE EQUALS THE EIGHT FILES
## any path under .claude/ in the diff (must print nothing):
## git ls-files --others --exclude-standard -- . ':(exclude).dev' (must print nothing):
## notes file items present (count of matching lines):
## Decisions table: 1
## Test and schema results: 1
## Pull request template note: 1
## Merge request: 1
## Commit-time steps: 1
## Manual checks: 1
## Owner inputs still missing: 1
## Owner follow-ups not done here: 1
## Additions beyond the files the issue names: 1
not that the future gate works: 1
deferred, no follow-up issue established; recorded here only: 1
## notes mention of percent or ROI number (must print nothing):
## end


--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/final-tests.log (full contents, 36 lines)
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-290
configfile: pyproject.toml
plugins: anyio-4.16.0, superclaude-6.1.0
collected 647 items

tests/unit/test_cli_install.py ......................................... [  6%]
.....................................................                    [ 14%]
tests/skills/test_sc_recommend_routing_contract.py ..................... [ 17%]
......                                                                   [ 18%]
tests/skills/test_spec_panel_review_loop.py ............................ [ 23%]
................                                                         [ 25%]
tests/skills/test_issue_protocol.py .................................... [ 31%]
........................................................................ [ 42%]
........................................................................ [ 53%]
.....                                                                    [ 54%]
tests/skills/test_review_brief_placement.py .....                        [ 54%]
tests/skills/test_review_prompt_overrides.py ........................... [ 59%]
...                                                                      [ 59%]
tests/recommend/test_routing_refresh.py ................................ [ 64%]
........................................................................ [ 75%]
.......................................                                  [ 81%]
tests/recommend/test_cache.py ...............                            [ 83%]
tests/docs/test_onboarding_deck.py ...                                   [ 84%]
tests/commands/test_routing_plugin_parity.py .....                       [ 85%]
tests/commands/test_worktrees_command.py ............                    [ 87%]
tests/core/test_claude_md_routing_block.py ......                        [ 87%]
tests/core/test_default_branch_agreement.py .                            [ 88%]
tests/core/test_how_we_work_routing_table.py ........................... [ 92%]
...................................                                      [ 97%]
tests/commands/test_help_command.py ......                               [ 98%]
tests/cli/test_how_we_work_install.py .........                          [100%]

============================= 647 passed in 4.76s ==============================


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: no source file is edited by this task; it writes ./artifacts/final-tests.log, ./artifacts/pr-body-notes.md and ./artifacts/t8-checks.log only; the eight edited files are the products of T1 to T7 and are listed in t8-checks.log

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
