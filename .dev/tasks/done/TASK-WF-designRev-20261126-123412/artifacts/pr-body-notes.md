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
