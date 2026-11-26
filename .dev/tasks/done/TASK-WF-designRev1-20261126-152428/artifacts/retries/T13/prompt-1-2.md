256f8cf05c9304e648363a0a43b19b5cca8fda4d
Review one task for spec compliance.

Task brief: ## Task 13: Write the apply runbook .dev/issues/837/apply-runbook.md

Depends on: Task 11

Write `.dev/issues/837/apply-runbook.md` from sections 3.6, 4, 5 and 6 of `./source.md`. State at the top that nothing in the runbook has been executed, that part one runs right after the commit and push whatever the ledger decides, and that part two runs only after the pull request monitor has settled and only for rulesets whose ledger decision becomes `APPLY`.

Part one covers the story steps after this plan. First the pre-commit checks, each with its output recorded: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `make lint` (a failure on files this change does not touch is recorded as pre-existing and named), `git diff --stat` (only the staging list below), and `git status` (nothing under `.claude/` or `.dev/issues/` staged). STOP before any staging: do not stage, commit or push until the lead's written decision on the archived first plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/` is quoted in `.dev/issues/837/issue-summary.md`; the guard's exclusion of that folder is not permission to publish it. Then the staging list (`.github/rulesets/other-repos/`, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py` and `.dev/tasks`; never `.claude/` and never `.dev/issues/`), with the line that the brainstorm folder `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos` is not staged because it describes a private repository (the story names only the changed files and `.dev/tasks`; whether to publish that folder is the user's decision). Then the pre-stage guard: print `gh repo view IronbellyOrg/IronClaude --json visibility -q .visibility`, then run `grep -c -F -f .dev/issues/837/private/guard-patterns.txt` over the files of `git diff --cached` and over the files to be staged (the patterns are the file name, the folder name and each function name in its call form, so ordinary words cannot hit); any hit stops the staging, the executor prints only the NAMES of the files that hit with `grep -l -F -f .dev/issues/837/private/guard-patterns.txt` over the same files (never the matched lines), and the lead decides before anything is staged; the only path the guard excludes is the archived superseded plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/`, which names that tooling in two lines and cannot be edited, and the runbook lists that as the open item for the lead that the STOP above waits on. Then the commit, then `git fetch origin` and `git log HEAD..origin/integration`, a rebase onto `origin/integration` only if it has commits the branch lacks, the push, and recording the pushed SHA. Then the comment file, which holds the handoff text with `<PUSHED-SHA>` replaced by the pushed SHA (the committed files keep no placeholder) followed by the draft ledger; run `grep -c -F -f .dev/issues/837/private/guard-patterns.txt <file>` on it (it must print 0), and post it as one comment on issue 837 with `gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>`. Only then run the `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "<title>" --body "<body>"` line. After the monitor settles, and after any later push, run `git diff --exit-code <SHA> -- .github/rulesets/other-repos/ .github/rulesets/protect-release-tags.json docs/developer-guide/branch-protection.md` with the SHA in the posted comment; if anything changed, post a NEW comment, built and posted as above, with the links and the copied commands refreshed from the final head.

Part two is the gated apply for CPA-Manager-Plus, IronOrca and coder_orca with steps R0 to R7 as in section 3.6, the results recorded in the audit file and the ledger as that section says, the variables filled now per repo (`REPO`, `PARENT_OWNER` for the two forks, `BRANCH=main`, and the file to apply as decided by the ledger; `ID`, `END` and `START` are set on apply day), the stop rules, the failure table of section 6, and the interfaces table of section 5 marked read or write. The scratch self-test of R1 pushes with `git push https://github.com/IronbellyOrg/$REPO.git ...` from the scratch clone, so every write command names its repository, and it carries the consequence of section 3.1 for a refused mirror bypass actor: drop the actor from the mirror file and change the file, the test, the guide and D4 together before anything is applied.

Acceptance criteria:
- `.dev/issues/837/apply-runbook.md` has part one with the pre-commit checks (including `make lint`), the staging list that excludes `.claude/`, `.dev/issues/` and the brainstorm folder, the pre-stage guard, the issue comment step (before the pull request command), the pull request command, and part two with R0 to R7 for each of the three Clay repos with `REPO`, `PARENT_OWNER`, `BRANCH` and the ledger-decided file filled.
- It contains the failure table of section 6, the stop rules (first 403 stops that repo; list before any retry; a pre-existing ruleset stops the repo; delete only rulesets this rollout created) and the mirror-refusal consequence.
- Every write command in it names its repository explicitly and none uses a brace placeholder.
- The opening statement says nothing has been executed and says that part one does not depend on `APPLY`.
- Part one, not R6, holds the re-pin step: after the monitor settles and after any later push, `git diff --exit-code <SHA> -- <paths>` against the SHA in the posted comment, and a NEW comment with refreshed links and commands when anything changed; it runs when no ruleset is `APPLY`.
- The file contains no private detail (see the constraints).
Global constraints: ## Constraints

- This plan only writes files in this worktree and runs read-only `gh api` GET calls. No task may send POST, PUT or DELETE to any GitHub ruleset, create a branch or ruleset in another repository, comment on an issue or edit a pull request. Applying rulesets is "Phase 3" of `./source.md` section 4 and is carried out from the runbook that Task 13 produces, after the pull request monitor has settled, never by `/sc:implement`.
- Never write to IronHands-CLI, irondots, ironops-marketplace, the archived IronHands repo, or any repository outside IronbellyOrg. Every `gh` call names its repository in full (`repos/IronbellyOrg/<repo>/...`, or `--repo IronbellyOrg/IronClaude`) except `gh api user`; never rely on the fork-parent default and never touch `SuperClaude-Org/SuperClaude_Framework`.
- Where `./source.md` section 2 names the four state files, this plan writes them there and nowhere else: `.dev/issues/837/audit/<repo>.md`, `.dev/issues/837/gates.md`, `.dev/issues/837/handoff-ryan.md` and `.dev/issues/837/apply-runbook.md`. They are never staged. The drafted pull request body goes to `.dev/issues/837/pr-body.md`. The package `./artifacts/` folder holds only the codegraph grounding note. The results of the later apply are recorded in the audit file and the ledger, as section 3.6 of `./source.md` says; there is no separate apply-results file.
- IronClaude is public and `IronbellyOrg/Coder` is private (Revision 1 of `./source.md`). Nothing that describes the internals of the private repository's release tooling (its file name, folder, function names, lines or line numbers) may be written to any file under `.dev/tasks/`, to any log or QA output captured there, to the pull request body or to an issue comment. The only neutral sentence allowed in such places is: "release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca". Task 5 reads the tooling without printing or saving its lines and keeps the evidence only in `.dev/issues/837/private/`, which is never staged. Those names are not written in this plan: E-2 of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md` lists them.
- Do not create `.github/rulesets/other-repos/protect-aidev02.json`: it needs Clay's written yes for `aidev02`, which is not recorded in `.dev/issues/837/issue-summary.md`.
- IronClaude's three existing files `.github/rulesets/protect-master.json`, `protect-integration.json` and `protect-release-tags.json` and the live IronClaude rulesets stay unchanged. Every existing assertion in `tests/docs/test_branch_protection_rulesets.py` stays.
- Facts that nobody verified stay labelled UNVERIFIED in every file this plan writes: whether the Sync fork button is refused under a `pull_request` rule, whether `clayphi`'s token can create rulesets, whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, and whether `time_period=quarter` is 90 days (it is not used).
- A check that cannot run (for example `gh api --paginate orgs/IronbellyOrg/installations`, which needs the `admin:org` scope) is written down as "could not run" with the real error text and blocks the repo it covers; it is never recorded as clean.
- Clay's recorded answer is in `.dev/issues/837/issue-summary.md` under "Decided for this work (iteration 3)". It is quoted word for word wherever a task says to quote it, never paraphrased. The lead's note in it, that the release-tag ruleset has its `update` rule on integration (pull request 844 merged), was verified before this plan: `.dev/issues/837/accuracy-check.md` line 13 records commit 206abea1c and the live ruleset 28081842 with `update`.
- This plan does not commit or push. Those are later story steps.
Start sha: 256f8cf05c9304e648363a0a43b19b5cca8fda4d
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/apply-runbook.md


diff --git a/.dev/issues/837/apply-runbook.md b/.dev/issues/837/apply-runbook.md
new file mode 100644
index 000000000..c94cf0ada
--- /dev/null
+++ b/.dev/issues/837/apply-runbook.md
@@ -0,0 +1,394 @@
+# Apply runbook for issue 837 (draft written in Phase 1)
+
+Nothing in this runbook has been executed. Part one runs right after the commit and push, whatever the gate ledger decides: it does not depend on any ruleset being `APPLY`. Part two runs only after the pull request monitor has settled (`/sc:pr-submit --monitor 3` reports every check green and every comment handled) and only for rulesets whose decision in `.dev/issues/837/gates.md` has become `APPLY`. Today no row is `APPLY`, so part two is ready but not run. This file is local and never staged. It holds no private detail; where a placeholder is needed it is written with angle brackets (never with braces).
+
+## Part one: after the plan (commit, push, comment, pull request)
+
+Run these steps in order from the IronClaude worktree. Record each command's output.
+
+### 1. Pre-commit checks
+
+```bash
+uv run pytest tests/docs/test_branch_protection_rulesets.py -v
+uv run pytest tests/docs -q
+uv run ruff check tests/docs/test_branch_protection_rulesets.py
+make lint
+git diff --stat
+git status
+```
+
+A `make lint` failure on files this change does not touch is recorded as pre-existing and named. `git diff --stat` and `git status` run again after staging (step 4), because every new file is untracked until then.
+
+### 2. STOP before any staging
+
+Do not stage, commit or push until the lead's written decision on the archived first plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/` is quoted in `.dev/issues/837/issue-summary.md`. That folder names a private repository's release tooling in two lines and cannot be edited; the guard below excludes it, and the exclusion is not permission to publish it. This is the open item for the lead.
+
+### 3. Staging list
+
+Stage only these paths: `.github/rulesets/other-repos/`, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py` and `.dev/tasks`. Never stage `.claude/` and never stage `.dev/issues/`. The brainstorm folder `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos` is not staged, because it describes a private repository (the story names only the changed files and `.dev/tasks`; whether to publish that folder is the user's decision).
+
+### 4. Pre-stage guard
+
+```bash
+gh repo view IronbellyOrg/IronClaude --json visibility -q .visibility
+LIST=$(git diff --name-only -- .github/rulesets/other-repos docs/developer-guide/branch-protection.md tests/docs/test_branch_protection_rulesets.py .dev/tasks; git ls-files --others --exclude-standard -- .github/rulesets/other-repos docs/developer-guide/branch-protection.md tests/docs/test_branch_protection_rulesets.py .dev/tasks | grep -v '^.dev/tasks/archive/TASK-WF-design-20261126-130537/')
+printf '%s\n' $LIST | xargs grep -c -F -f .dev/issues/837/private/guard-patterns.txt
+```
+
+Every file must print `:0`. The patterns are the file name, the folder name and each function name in its call form, so ordinary words cannot hit. Any hit stops the staging: print only the NAMES of the files that hit (never the matched lines) with `printf '%s\n' $LIST | xargs grep -l -F -f .dev/issues/837/private/guard-patterns.txt`, and the lead decides before anything is staged. After staging, repeat the check over `git diff --cached --name-only` and run:
+
+```bash
+git diff --cached --stat
+git diff --cached --name-only
+```
+
+Nothing under `.claude/` or `.dev/issues/` may appear, and the archived first plan folder may not appear until the lead's decision is quoted.
+
+### 5. Commit, rebase check, push, record the SHA
+
+```bash
+git commit
+git fetch origin
+git log HEAD..origin/integration
+git push https://github.com/IronbellyOrg/IronClaude.git <feature-branch>
+git rev-parse HEAD
+```
+
+Commit on the feature branch with a conventional message. If `git log HEAD..origin/integration` lists commits, rebase the branch onto `origin/integration` before the push (the commit comes first, so the rebase has a clean tree). Record the pushed SHA from `git rev-parse HEAD`; it is the SHA of the links below.
+
+### 6. Comment file, guard, one comment on issue 837
+
+```bash
+sed "s/<PUSHED-SHA>/<the pushed SHA>/g" .dev/issues/837/handoff-ryan.md > .dev/issues/837/comment-handoff.md
+cat .dev/issues/837/gates.md >> .dev/issues/837/comment-handoff.md
+grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/comment-handoff.md
+gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file .dev/issues/837/comment-handoff.md
+```
+
+The comment file holds the handoff text with the placeholder replaced by the pushed SHA (the committed files keep no placeholder) followed by the draft ledger. The `grep -c` must print 0 before the comment is posted. The comment is posted before the pull request command so that the pull request body can name where it is.
+
+### 7. Pull request
+
+```bash
+/sc:pr-submit --monitor 3 --head <feature-branch> --base integration --title "<title>" --body "<body>"
+```
+
+The body is `.dev/issues/837/pr-body.md`; its last line is `Refs #837` and it never says `Fixes` or `Closes`. Verify that the returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/<number>`.
+
+### 8. Re-pin after the monitor settles and after any later push
+
+```bash
+git diff --exit-code <the pushed SHA> -- .github/rulesets/other-repos/ .github/rulesets/protect-release-tags.json docs/developer-guide/branch-protection.md
+```
+
+Run it with the SHA that is in the posted comment. If it exits non-zero, post a NEW comment built and posted as in step 6, with the links and the copied commands refreshed from the final head. This step runs also when no ruleset is `APPLY`; it is not part of R6.
+
+## Part two: gated apply for the three Clay repos
+
+Run per repo, one repo at a time; a stop on one repo does not stop the others. A ruleset is applied only when its ledger decision is `APPLY`. Today: none. Variables per repo are filled below; `ID`, `END` and `START` are set on apply day. The file to apply is the one the ledger decides: for a fork, `protect-main-mirror.json` when `ahead_by` is 0 and Clay's written acceptance of the mirror is quoted in `.dev/issues/837/issue-summary.md`, otherwise `protect-main.json`; for coder_orca, `protect-main.json`.
+
+### Stop rules
+
+- The first 403 on a write stops that repo; record the partial state; no retry.
+- After a timeout or an ambiguous answer, list the rulesets before any retry and create only if the name is still absent.
+- A ruleset that already exists at the snapshot stops that repo; update and delete nothing that pre-existed.
+- Delete only rulesets that this rollout created.
+- Evidence missing or a check that cannot run is never recorded as clean: write `SKIP` and name who clears it.
+
+### The consequence of a refused mirror bypass actor
+
+Whether the API accepts `bypass_mode: pull_request` on a ruleset that has no `pull_request` rule (the mirror) is UNVERIFIED. The scratch self-test (R1) creates a copy of the mirror through POST, so it answers this before any real create. If the API refuses it, drop the bypass actor from `.github/rulesets/other-repos/protect-main-mirror.json` and change the file, the test (`tests/docs/test_branch_protection_rulesets.py`), the guide and decision D4 together before anything is applied.
+
+#### CPA-Manager-Plus
+
+```bash
+REPO=CPA-Manager-Plus
+PARENT_OWNER=seakee
+BRANCH=main
+FILE=protect-main-mirror.json   # the ledger candidate while ahead_by is 0 and Clay's written acceptance is quoted; use protect-main.json when ahead_by is above 0 or no acceptance is quoted
+ID=<set on apply day>
+END=<set on apply day, date -u +%Y-%m-%dT%H:%M:%SZ>
+START=<set on apply day, 90 days before END>
+```
+
+R0. Re-run the audit and the fork test inside the hour; refresh `END`, the tips and `ahead_by`; re-evaluate gates G2 to G9 and record them in `.dev/issues/837/audit/CPA-Manager-Plus.md` and `.dev/issues/837/gates.md`.
+
+```bash
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by, .behind_by] | @tsv'
+gh api repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH --jq .object.sha
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp, .ref, .activity_type, .actor.login] | @tsv'
+```
+
+R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repository (never IronClaude). Actions are listed as enabled on this repo, and the Task 6 audit read two workflow files with a push trigger (`demo-pages.yml` and `pr-check.yml`; no branch filter was recorded). The fork has no registered workflow and no run, so they are probably disabled (UNVERIFIED). On apply day read every workflow for an unfiltered `on: push` first; if one would start on the throwaway branch, name the branch so it cannot match, or skip this repo's self-test and record why.
+
+```bash
+REPO=CPA-Manager-Plus
+ID=<id of the zz-selftest- ruleset printed by the scratch create call>
+RULESET_FILE=<absolute path of the role file in a separate checkout of IronClaude at the pushed commit>
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
+jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' "$RULESET_FILE" | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git commit --allow-empty -m "selftest: this push must be refused"
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+git push --force https://github.com/IronbellyOrg/$REPO.git HEAD~1:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+Full role: the empty-commit push must be refused (error GH013). Mirror: skip the empty commit and the force push of the earlier commit must be refused. The last command must show no name that starts with `zz-selftest-`; the real create waits until it is clean. Record the result and the API answer to the scratch POST (it also settles whether the mirror's bypass actor is accepted).
+
+R2. Snapshot the existing rulesets and stop the repo if the list is not empty (G7); record the list in the audit file.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+```
+
+R3. Apply in this order: the tag ruleset (if `APPLY`), the `main` role. Before each: list the names; the name must be absent. Run from a checkout of IronClaude at the recorded SHA.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # only if the ledger says APPLY for the tag ruleset
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/$FILE
+```
+
+Record the id, the date and the SHA of each ruleset. After a timeout, list again before any retry. On the first 403, stop this repo and record the partial state (write permission has never been tried).
+
+R4. Read back, and compare with the file.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+Compare on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset compare the rule types. A ruleset that fails the read-back is deleted by id (this rollout created it) and the repo is reported `SKIP(read-back)`:
+
+```bash
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+R5. Record ids, dates, the SHA and the read-back output in the audit file and in the ledger (the results are recorded there; there is no separate apply-results file). Post the ledger table and the ids as a comment on issue 837 and add the same to the pull request body:
+
+```bash
+gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>
+gh pr edit <number> --repo IronbellyOrg/IronClaude --body-file <file>
+```
+
+R6. After the pull request monitor has settled and the last push is made: for each applied file run `git diff --exit-code <SHA> -- .github/rulesets/other-repos/<file>`. A changed file means:
+
+```bash
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input .github/rulesets/other-repos/$FILE
+```
+
+and a new SHA in the record.
+
+R7. For a mirror: name the owner and the date of the first Sync fork on issue 837; the status is "pending" until it is run. If it is refused, delete the new ruleset by id and report. Not applicable for the full role.
+
+
+#### IronOrca
+
+```bash
+REPO=IronOrca
+PARENT_OWNER=stablyai
+BRANCH=main
+FILE=protect-main-mirror.json   # the ledger candidate while ahead_by is 0 and Clay's written acceptance is quoted; use protect-main.json when ahead_by is above 0 or no acceptance is quoted
+ID=<set on apply day>
+END=<set on apply day, date -u +%Y-%m-%dT%H:%M:%SZ>
+START=<set on apply day, 90 days before END>
+```
+
+R0. Re-run the audit and the fork test inside the hour; refresh `END`, the tips and `ahead_by`; re-evaluate gates G2 to G9 and record them in `.dev/issues/837/audit/IronOrca.md` and `.dev/issues/837/gates.md`.
+
+```bash
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by, .behind_by] | @tsv'
+gh api repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH --jq .object.sha
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp, .ref, .activity_type, .actor.login] | @tsv'
+```
+
+R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repository (never IronClaude). Actions are active on this repo: first read every workflow for an unfiltered `on: push` (the Task 7 audit found none, 67 workflows); if one has appeared, name the throwaway branch so it cannot start that workflow, or skip the repo's self-test and record why.
+
+```bash
+REPO=IronOrca
+ID=<id of the zz-selftest- ruleset printed by the scratch create call>
+RULESET_FILE=<absolute path of the role file in a separate checkout of IronClaude at the pushed commit>
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
+jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' "$RULESET_FILE" | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git commit --allow-empty -m "selftest: this push must be refused"
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+git push --force https://github.com/IronbellyOrg/$REPO.git HEAD~1:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+Full role: the empty-commit push must be refused (error GH013). Mirror: skip the empty commit and the force push of the earlier commit must be refused. The last command must show no name that starts with `zz-selftest-`; the real create waits until it is clean. Record the result and the API answer to the scratch POST (it also settles whether the mirror's bypass actor is accepted).
+
+R2. Snapshot the existing rulesets and stop the repo if the list is not empty (G7); record the list in the audit file.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+```
+
+R3. Apply in this order: the tag ruleset (if `APPLY`), `aidev02` (if `APPLY`: only with Clay's written yes and `protect-aidev02.json` present), then the `main` role. Before each: list the names; the name must be absent. Run from a checkout of IronClaude at the recorded SHA.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # only if the ledger says APPLY for the tag ruleset
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/$FILE
+```
+
+Record the id, the date and the SHA of each ruleset. After a timeout, list again before any retry. On the first 403, stop this repo and record the partial state (write permission has never been tried).
+
+R4. Read back, and compare with the file.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+Compare on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset compare the rule types. A ruleset that fails the read-back is deleted by id (this rollout created it) and the repo is reported `SKIP(read-back)`:
+
+```bash
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+R5. Record ids, dates, the SHA and the read-back output in the audit file and in the ledger (the results are recorded there; there is no separate apply-results file). Post the ledger table and the ids as a comment on issue 837 and add the same to the pull request body:
+
+```bash
+gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>
+gh pr edit <number> --repo IronbellyOrg/IronClaude --body-file <file>
+```
+
+R6. After the pull request monitor has settled and the last push is made: for each applied file run `git diff --exit-code <SHA> -- .github/rulesets/other-repos/<file>`. A changed file means:
+
+```bash
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input .github/rulesets/other-repos/$FILE
+```
+
+and a new SHA in the record.
+
+R7. For a mirror: name the owner and the date of the first Sync fork on issue 837; the status is "pending" until it is run. If it is refused, delete the new ruleset by id and report. Not applicable for the full role.
+
+
+#### coder_orca
+
+```bash
+REPO=coder_orca
+BRANCH=main
+FILE=protect-main.json
+ID=<set on apply day>
+END=<set on apply day, date -u +%Y-%m-%dT%H:%M:%SZ>
+START=<set on apply day, 90 days before END>
+```
+
+R0. Re-run the audit and the fork test inside the hour; refresh `END`, the tips and `ahead_by`; re-evaluate gates G2 to G9 and record them in `.dev/issues/837/audit/coder_orca.md` and `.dev/issues/837/gates.md`.
+
+```bash
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH --jq .object.sha
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp, .ref, .activity_type, .actor.login] | @tsv'
+```
+
+R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repository (never IronClaude). The repo is not a fork and has no workflow folder (Task 5 audit).
+
+```bash
+REPO=coder_orca
+ID=<id of the zz-selftest- ruleset printed by the scratch create call>
+RULESET_FILE=<absolute path of the role file in a separate checkout of IronClaude at the pushed commit>
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
+jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' "$RULESET_FILE" | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git commit --allow-empty -m "selftest: this push must be refused"
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+git push --force https://github.com/IronbellyOrg/$REPO.git HEAD~1:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+Full role: the empty-commit push must be refused (error GH013). Mirror: skip the empty commit and the force push of the earlier commit must be refused. The last command must show no name that starts with `zz-selftest-`; the real create waits until it is clean. Record the result and the API answer to the scratch POST (it also settles whether the mirror's bypass actor is accepted).
+
+R2. Snapshot the existing rulesets and stop the repo if the list is not empty (G7); record the list in the audit file.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+```
+
+R3. Apply in this order: the tag ruleset (if `APPLY`), the `main` role. Before each: list the names; the name must be absent. Run from a checkout of IronClaude at the recorded SHA.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/$FILE
+```
+
+Record the id, the date and the SHA of each ruleset. After a timeout, list again before any retry. On the first 403, stop this repo and record the partial state (write permission has never been tried).
+
+R4. Read back, and compare with the file.
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+Compare on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset compare the rule types. A ruleset that fails the read-back is deleted by id (this rollout created it) and the repo is reported `SKIP(read-back)`:
+
+```bash
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+R5. Record ids, dates, the SHA and the read-back output in the audit file and in the ledger (the results are recorded there; there is no separate apply-results file). Post the ledger table and the ids as a comment on issue 837 and add the same to the pull request body:
+
+```bash
+gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>
+gh pr edit <number> --repo IronbellyOrg/IronClaude --body-file <file>
+```
+
+R6. After the pull request monitor has settled and the last push is made: for each applied file run `git diff --exit-code <SHA> -- .github/rulesets/other-repos/<file>`. A changed file means:
+
+```bash
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input .github/rulesets/other-repos/$FILE
+```
+
+and a new SHA in the record.
+
+R7. Not applicable: this repo is not a fork and gets the full role; its tag ruleset is skipped by decision (G6).
+
+
+### Failure handling and rollback
+
+| Failure | Detected by | Response | Rollback |
+|---|---|---|---|
+| First POST returns 403 | R3 | Stop that repo, no retry, record the partial state; report the repo as not applied. Other repos continue. | Delete any ruleset already created on that repo by id. |
+| Timeout or ambiguous answer on POST | R3 | Read the ruleset list before any retry; create only if the name is still absent. | As above. |
+| Existing ruleset found at the snapshot | R2 / G7 | Stop that repo; update and delete nothing that pre-existed. | None needed. |
+| Read-back differs from the file | R4 | Delete the ruleset this rollout created, report `SKIP(read-back)`. | Delete by id. |
+| Half-applied repo (tags created, branch POST fails) | R3 | The tag ruleset has no bypass; record the state and either apply the branch ruleset on a later run or delete the tag ruleset by id, whichever the revert owner decides in writing on issue 837. | Delete by id. |
+| Scratch ruleset or throwaway branch survives | R1 | List `zz-selftest-*` rulesets and branches; delete; the real create waits until the list is clean. | Delete by id and `git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest`. |
+| Sync fork refused after a mirror | R7 | Delete the new ruleset by id; report; the fork test and the standing switch rule are reviewed. | Delete by id. |
+| A review fix changes an applied file | R6 | PUT the new file; record the new SHA. | Re-PUT the previous file. |
+| A tag producer is found after the apply | later, by anyone | Delete the tag ruleset by id (the break-glass sequence in the guide); report. | Delete by id. |
+| Evidence missing or a check cannot run | G3 | `SKIP` and name who clears it; never treated as clean. | None needed. |
+
+Who reverts: the repo admin. `ironbelly`'s admin role on the three Clay repos is UNVERIFIED; until `ironbelly` confirms it in writing on issue 837, Clay is the revert owner and must be reachable on the day of the apply.
+
+### Interfaces
+
+Every `gh` call names its repository explicitly (`repos/IronbellyOrg/$REPO/...` or `--repo IronbellyOrg/IronClaude`); no call uses the fork-parent default and nothing touches `SuperClaude-Org/SuperClaude_Framework`.
+
+| Interface | Command shape | Reads or writes |
+|---|---|---|
+| Identity and permission | `gh api user --jq .login`; `gh api repos/IronbellyOrg/$REPO --jq '...'` | read |
+| Audit | `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '...'` | read |
+| Tips and tags | `repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH`, `repos/IronbellyOrg/$REPO/git/matching-refs/tags/v` | read |
+| Fork test | `repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main --jq '[.ahead_by, .behind_by]'` | read |
+| Workflow search | `repos/IronbellyOrg/$REPO/contents/.github/workflows` and each file | read |
+| Existing rulesets | `gh api repos/IronbellyOrg/$REPO/rulesets` | read |
+| Create | `gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input <file>` | **write** (part two and the R1 scratch only) |
+| Update | `gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input <file>` | **write** (R6 only) |
+| Delete | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID` | **write** (revert and scratch cleanup; only rulesets this rollout created) |
+| Read-back | `repos/IronbellyOrg/$REPO/rules/branches/$BRANCH`, `repos/IronbellyOrg/$REPO/rulesets/$ID` | read |
+| Issue and pull request | `gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>`; `gh pr edit <number> --repo IronbellyOrg/IronClaude --body-file <file>` | **write** (IronClaude only) |
+| Throwaway branch | `git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest`, `git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest` in a scratch clone of the target repo | **write** (R1 only) |


Codegraph context: index_state: fresh; checked_at: 2026-11-26T15:31:43Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files of this task are JSON and Markdown (not indexed) unless a Python file is named; dependents were checked with Grep.
Note on files the diff cannot show: paths under `.dev/issues/837/private/` are git-ignored, so they are absent from the diff; read them directly with Read when a task names them. Never print private content in your answer.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/issues/837/apply-runbook.md b/.dev/issues/837/apply-runbook.md
index 05a6667ad..c94cf0ada 100644
--- a/.dev/issues/837/apply-runbook.md
+++ b/.dev/issues/837/apply-runbook.md
@@ -105,7 +105,7 @@ Whether the API accepts `bypass_mode: pull_request` on a ruleset that has no `pu
 REPO=CPA-Manager-Plus
 PARENT_OWNER=seakee
 BRANCH=main
-FILE=<protect-main-mirror.json when ahead_by is 0 and Clay's acceptance is quoted, otherwise protect-main.json>
+FILE=protect-main-mirror.json   # the ledger candidate while ahead_by is 0 and Clay's written acceptance is quoted; use protect-main.json when ahead_by is above 0 or no acceptance is quoted
 ID=<set on apply day>
 END=<set on apply day, date -u +%Y-%m-%dT%H:%M:%SZ>
 START=<set on apply day, 90 days before END>
@@ -121,7 +121,7 @@ gh api repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH --jq .object.sha
 gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp, .ref, .activity_type, .actor.login] | @tsv'
 ```
 
-R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repository (never IronClaude). The repo has no workflow with a push trigger that a throwaway branch could start (Task 6 audit).
+R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repository (never IronClaude). Actions are listed as enabled on this repo, and the Task 6 audit read two workflow files with a push trigger (`demo-pages.yml` and `pr-check.yml`; no branch filter was recorded). The fork has no registered workflow and no run, so they are probably disabled (UNVERIFIED). On apply day read every workflow for an unfiltered `on: push` first; if one would start on the throwaway branch, name the branch so it cannot match, or skip this repo's self-test and record why.
 
 ```bash
 REPO=CPA-Manager-Plus
@@ -192,7 +192,7 @@ R7. For a mirror: name the owner and the date of the first Sync fork on issue 83
 REPO=IronOrca
 PARENT_OWNER=stablyai
 BRANCH=main
-FILE=<protect-main-mirror.json when ahead_by is 0 and Clay's acceptance is quoted, otherwise protect-main.json>
+FILE=protect-main-mirror.json   # the ledger candidate while ahead_by is 0 and Clay's written acceptance is quoted; use protect-main.json when ahead_by is above 0 or no acceptance is quoted
 ID=<set on apply day>
 END=<set on apply day, date -u +%Y-%m-%dT%H:%M:%SZ>
 START=<set on apply day, 90 days before END>
@@ -278,7 +278,7 @@ R7. For a mirror: name the owner and the date of the first Sync fork on issue 83
 ```bash
 REPO=coder_orca
 BRANCH=main
-FILE=<protect-main.json>
+FILE=protect-main.json
 ID=<set on apply day>
 END=<set on apply day, date -u +%Y-%m-%dT%H:%M:%SZ>
 START=<set on apply day, 90 days before END>

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=T13.AC1 at=.dev/issues/837/apply-runbook.md:124 anchor=.dev/issues/837/audit/CPA-Manager-Plus.md:88 chk=n,y,n,n family=r1-workflow-claim fix=replace the sentence with the accurate push-trigger wording first=A1 origin=new: The CPA-Manager-Plus R1 text says the repo has no workflow with a push trigger, but the audit records push triggers in demo-pages.yml and pr-check.yml.
F1.2 sev=blocking trigger=B1 ac=T13.AC1 at=.dev/issues/837/apply-runbook.md:108 anchor=the ledger-decided file filled chk=y,n,n,n family=variables-not-filled fix=fill FILE for each repo first=A1 origin=new: FILE is a conditional placeholder in angle brackets for CPA-Manager-Plus and IronOrca and angle-bracketed for coder_orca, so the ledger-decided file is not filled and R3 reads --input .github/rulesets/other-repos/$FILE.

Saved-probe re-check hit locations (may be empty): 124:R1. Scratch self-test for each role the ledger says `APP
211:R1. Scratch self-test for each role the ledger says `APP
106:PARENT_OWNER=seakee
107:BRANCH=main
108:FILE=protect-main-mirror.json   # the ledger candidate w
193:PARENT_OWNER=stablyai
194:BRANCH=main
195:FILE=protect-main-mirror.json   # the ledger candidate w
280:BRANCH=main
281:FILE=protect-main.json


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
