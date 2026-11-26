2a7b88e58a97f880e9155f3d02db7a78807d56e3
Review one task for spec compliance.

Task brief: ## Task 12: Write the handoff for Ryan .dev/issues/837/handoff-ryan.md

Depends on: Task 3, Task 8, Task 9, Task 10, Task 11

Write `.dev/issues/837/handoff-ryan.md` as defined in section 3.7 of `./source.md`, for IronHands-CLI, irondots and ironops-marketplace. Per repo: the 90-day audit Clay ran read-only (copy the command, `END`, the classified events and the fork-test result from the audit record); the admin-only pre-apply checks with exact commands (`hooks`, `keys`, `branches/main/protection`, the installations read, classic protection, and a request that Ryan confirm his admin role); the exact apply, read-back, scratch self-test, revert and break-glass commands with `REPO` set, taken from the guide section of Task 3; the tag ruleset, which is included where the repository has no `v*` tag and Clay's read-only workflow search found no tag mover (there is then nothing to break), with the result of that search; and what Ryan reports back (ruleset ids, dates and the read-back output as a comment on issue 837). For IronHands-CLI, a fork, the handoff gives the role rule (mirror only when `ahead_by` is 0 and Clay's written acceptance is quoted, otherwise the full role). Links to `.github/rulesets/other-repos/protect-main.json`, `.github/rulesets/other-repos/protect-main-mirror.json` and `.github/rulesets/protect-release-tags.json` use the single placeholder `<PUSHED-SHA>` in the URL path (a GitHub blob URL on IronbellyOrg/IronClaude). The file keeps the placeholder; the text that is posted as the issue comment has it replaced by the pushed SHA (Task 13, part one). End with a request that the lead hand the text to Ryan.

Acceptance criteria:
- `.dev/issues/837/handoff-ryan.md` has one section per Ryan repo with the parts above, and an opening section that says nothing was written to those repos.
- `<PUSHED-SHA>` appears only in file links, each link ending in one of the three ruleset file names, and the file says where it is replaced.
- Every command names its repository through `$REPO` set at the top of the repo section, and no command is a write except the apply, scratch self-test, revert and break-glass commands that Ryan runs himself.
- The IronHands-CLI section carries the fork role rule, and the file contains no private detail (see the constraints).
- The last paragraph is the request to the lead.
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
Start sha: 2a7b88e58a97f880e9155f3d02db7a78807d56e3
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/handoff-ryan.md


diff --git a/.dev/issues/837/handoff-ryan.md b/.dev/issues/837/handoff-ryan.md
new file mode 100644
index 000000000..ac3ee772b
--- /dev/null
+++ b/.dev/issues/837/handoff-ryan.md
@@ -0,0 +1,302 @@
+# Handoff for Ryan: branch protection rulesets on three IronbellyOrg repos (issue 837)
+
+Draft written in Phase 1. Nothing was written to IronHands-CLI, irondots or ironops-marketplace: Clay has only read access there, and everything below that Clay ran was a read-only GET. These three repos need your login (admin). The commands use `$REPO`, set at the top of each section. The apply happens only after Clay's checks and yours both come out clean; no ruleset is applied by this change.
+
+Ruleset files (pinned to the commit that was pushed to IronbellyOrg/IronClaude; the SHA placeholder in these three links is replaced by the pushed SHA in the text that is posted on issue 837, and only there):
+
+- Full role: https://github.com/IronbellyOrg/IronClaude/blob/<PUSHED-SHA>/.github/rulesets/other-repos/protect-main.json
+- Mirror role: https://github.com/IronbellyOrg/IronClaude/blob/<PUSHED-SHA>/.github/rulesets/other-repos/protect-main-mirror.json
+- Tag ruleset: https://github.com/IronbellyOrg/IronClaude/blob/<PUSHED-SHA>/.github/rulesets/protect-release-tags.json
+
+## IronHands-CLI
+
+```bash
+REPO=IronHands-CLI
+PARENT_OWNER=OpenHands
+```
+
+### 1. The 90-day audit Clay ran (read-only)
+
+`END` is 2026-11-26T15:58:31Z; `START` is 2026-08-28T15:58:31Z (90 days before). Audit record: `.dev/issues/837/audit/IronHands-CLI.md` (local to Clay's worktree).
+
+Command Clay ran, read-only (`REPO=IronHands-CLI`, `END` and `START` as above):
+
+```bash
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'
+```
+
+Events: 0 rows kept in the 90-day window (the endpoint also returned 12 older rows, all by `ironbelly`, the newest on 2026-03-17: they show that a person has pushed to this `main` directly, outside the window). Counts by class in the window: direct push by human 0, direct push by automation 0, sync 0, pr_merge 0, branch_creation 0.
+
+Fork test: `compare/OpenHands:main...main`: `ahead_by` 13, `behind_by` 73 (diverged). Role that follows: full role (`protect-main.json`): the fork is ahead of its parent, so the mirror does not fit.
+
+Role rule for this fork (a fork of OpenHands/OpenHands-CLI): the mirror (`protect-main-mirror.json`) only when `ahead_by` is 0 and Clay's written acceptance of the mirror's direct-push exposure is quoted on issue 837; otherwise the full role. Re-run the fork test on apply day: `gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by, .behind_by] | @tsv'`. Today `ahead_by` is 13, so the full role applies. Whether the Sync fork button is refused under a `pull_request` rule is UNVERIFIED.
+
+### 2. Admin-only checks to run before applying (Clay could not run them)
+
+```bash
+REPO=IronHands-CLI
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api repos/IronbellyOrg/$REPO/hooks --jq length
+gh api repos/IronbellyOrg/$REPO/keys --jq length
+gh api repos/IronbellyOrg/$REPO/branches/main/protection
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+gh api --paginate orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
+gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled, .allowed_actions] | @tsv'
+```
+
+Expected: login `ironbelly`; admin `true`, default branch `main`, not archived, public; both counts `0`; `branches/main/protection` answers 404 "Branch not protected" (no classic protection); an empty ruleset list (an existing ruleset stops this repo: update and delete nothing that pre-existed); and for the installations read, a review of every app with `contents: write` (an app that can push must use pull requests once the ruleset is on, because only the admin role bypasses). Please also confirm in a comment that you hold the admin role on this repository. The installations command needs the `admin:org` scope; if it fails, write "could not run" with the error text and stop until an organisation owner runs it or Clay accepts the gap in writing.
+
+### 3. Apply, read back, self-test, revert, break glass
+
+```bash
+REPO=IronHands-CLI
+BRANCH=main
+ID=<id printed by the create call of the ruleset you are reading back>
+PARENT_OWNER=OpenHands
+# from a checkout of IronClaude at the pushed commit; create only if the name is absent
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # tag ruleset first, if you decide to apply it
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
+# read back
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full role. Compare `rulesets/$ID` with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters. A ruleset that fails the read-back is deleted by id (only one you created) and reported. After a timeout, list the rulesets again before any retry; on the first 403, stop and report.
+
+Scratch self-test before the first real create (from a scratch clone of this repository, never from IronClaude; the throwaway branch is `zz-ruleset-selftest`; the scratch ruleset is `zz-selftest-<role>`):
+
+```bash
+REPO=IronHands-CLI
+ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
+jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/protect-main.json | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git commit --allow-empty -m "selftest: this push must be refused"
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+The empty-commit push must be refused (error GH013). The last command must show no name that starts with `zz-selftest-`. Delete only rulesets that you created.
+
+Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, with `$REPO` and `$ID`):
+
+```bash
+REPO=IronHands-CLI
+ID=<id of the ruleset you apply this to>
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
+# push the fix
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
+```
+
+Revert (rolls a ruleset back completely; run it on its own, never in the same run as the break-glass block, and only for a ruleset you created):
+
+```bash
+REPO=IronHands-CLI
+ID=<id of the ruleset to delete>
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+### 4. The tag ruleset
+
+No `v*` tag exists in the fork (0 `v*` refs, and no tag of any name; the parent's 25 tags have no `v` prefix). Clay's read-only search of its 14 workflows and the scripts they call found no producer that moves or deletes a `v*` tag. The tag ruleset would match nothing here today; apply it only if you want it in place for future `v*` tags, otherwise leave it out. Other IronbellyOrg repositories were not searched for a release token for this repository (UNVERIFIED).
+
+### 5. Report back
+
+What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `rules/branches/$BRANCH` and `rulesets/$ID`, the result of the scratch self-test, and the output of the admin-only checks above.
+
+## irondots
+
+```bash
+REPO=irondots
+```
+
+### 1. The 90-day audit Clay ran (read-only)
+
+`END` is 2026-11-26T16:29:23Z; `START` is 2026-08-28T16:29:23Z (90 days before). Audit record: `.dev/issues/837/audit/irondots.md` (local to Clay's worktree).
+
+Command Clay ran, read-only (`REPO=irondots`, `END` and `START` as above):
+
+```bash
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'
+```
+
+Events: 3 rows kept, all by `ironbelly` (a person): 2026-11-01T23:04:09Z `branch_creation`, 2026-11-04T12:21:18Z `pr_merge`, 2026-11-11T22:08:07Z `pr_merge`. Counts by class: direct push by human 0, direct push by automation 0, sync 0, pr_merge 2, branch_creation 1. The repository was created on 2026-11-01 (about 24 days old), so the 90-day window covers its whole life. Branches matching `dot/*` are excluded from protection and must stay deletable; the rulesets here target only `main`.
+
+Fork test: not a fork (no parent), so no fork test. Role that follows: full role (`protect-main.json`).
+
+### 2. Admin-only checks to run before applying (Clay could not run them)
+
+```bash
+REPO=irondots
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api repos/IronbellyOrg/$REPO/hooks --jq length
+gh api repos/IronbellyOrg/$REPO/keys --jq length
+gh api repos/IronbellyOrg/$REPO/branches/main/protection
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+gh api --paginate orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
+gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled, .allowed_actions] | @tsv'
+```
+
+Expected: login `ironbelly`; admin `true`, default branch `main`, not archived, public; both counts `0`; `branches/main/protection` answers 404 "Branch not protected" (no classic protection); an empty ruleset list (an existing ruleset stops this repo: update and delete nothing that pre-existed); and for the installations read, a review of every app with `contents: write` (an app that can push must use pull requests once the ruleset is on, because only the admin role bypasses). Please also confirm in a comment that you hold the admin role on this repository. The installations command needs the `admin:org` scope; if it fails, write "could not run" with the error text and stop until an organisation owner runs it or Clay accepts the gap in writing.
+
+### 3. Apply, read back, self-test, revert, break glass
+
+```bash
+REPO=irondots
+BRANCH=main
+ID=<id printed by the create call of the ruleset you are reading back>
+# from a checkout of IronClaude at the pushed commit; create only if the name is absent
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # tag ruleset first, if you decide to apply it
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
+# read back
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full role. Compare `rulesets/$ID` with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters. A ruleset that fails the read-back is deleted by id (only one you created) and reported. After a timeout, list the rulesets again before any retry; on the first 403, stop and report.
+
+Scratch self-test before the first real create (from a scratch clone of this repository, never from IronClaude; the throwaway branch is `zz-ruleset-selftest`; the scratch ruleset is `zz-selftest-<role>`):
+
+```bash
+REPO=irondots
+ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
+jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/protect-main.json | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git commit --allow-empty -m "selftest: this push must be refused"
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+The empty-commit push must be refused (error GH013). The last command must show no name that starts with `zz-selftest-`. Delete only rulesets that you created.
+
+Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, with `$REPO` and `$ID`):
+
+```bash
+REPO=irondots
+ID=<id of the ruleset you apply this to>
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
+# push the fix
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
+```
+
+Revert (rolls a ruleset back completely; run it on its own, never in the same run as the break-glass block, and only for a ruleset you created):
+
+```bash
+REPO=irondots
+ID=<id of the ruleset to delete>
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+### 4. The tag ruleset
+
+No `v*` tag exists (0 `v*` refs, no tag of any name). Its workflow `.github/workflows/gated-release.yml` only creates a tag (it refuses an existing one); creating a tag stays allowed under the tag ruleset, which has no creation rule. No workflow or script moves or deletes a tag. Whether that workflow's own token can still create a `v*` tag once the tag ruleset is on is UNVERIFIED: before you apply the tag ruleset, confirm it (read the token the workflow uses and check that it can still create a tag under a ruleset that has no creation rule); until then the tag ruleset is not confirmed safe. Other IronbellyOrg repositories were not searched for a release token for this repository (UNVERIFIED).
+
+### 5. Report back
+
+What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `rules/branches/$BRANCH` and `rulesets/$ID`, the result of the scratch self-test, and the output of the admin-only checks above.
+
+## ironops-marketplace
+
+```bash
+REPO=ironops-marketplace
+```
+
+### 1. The 90-day audit Clay ran (read-only)
+
+`END` is 2026-11-26T16:32:41Z; `START` is 2026-08-28T16:32:41Z (90 days before). Audit record: `.dev/issues/837/audit/ironops-marketplace.md` (local to Clay's worktree).
+
+Command Clay ran, read-only (`REPO=ironops-marketplace`, `END` and `START` as above):
+
+```bash
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'
+```
+
+Events: 0 rows kept in the window. The only event ever recorded for `main` is its `branch_creation` on 2026-05-28 (182 days before `END`); `main` holds a single commit. Counts by class: all 0.
+
+Fork test: not a fork (no parent), so no fork test. Role that follows: full role (`protect-main.json`).
+
+### 2. Admin-only checks to run before applying (Clay could not run them)
+
+```bash
+REPO=ironops-marketplace
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api repos/IronbellyOrg/$REPO/hooks --jq length
+gh api repos/IronbellyOrg/$REPO/keys --jq length
+gh api repos/IronbellyOrg/$REPO/branches/main/protection
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+gh api --paginate orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
+gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled, .allowed_actions] | @tsv'
+```
+
+Expected: login `ironbelly`; admin `true`, default branch `main`, not archived, public; both counts `0`; `branches/main/protection` answers 404 "Branch not protected" (no classic protection); an empty ruleset list (an existing ruleset stops this repo: update and delete nothing that pre-existed); and for the installations read, a review of every app with `contents: write` (an app that can push must use pull requests once the ruleset is on, because only the admin role bypasses). Please also confirm in a comment that you hold the admin role on this repository. The installations command needs the `admin:org` scope; if it fails, write "could not run" with the error text and stop until an organisation owner runs it or Clay accepts the gap in writing.
+
+### 3. Apply, read back, self-test, revert, break glass
+
+```bash
+REPO=ironops-marketplace
+BRANCH=main
+ID=<id printed by the create call of the ruleset you are reading back>
+# from a checkout of IronClaude at the pushed commit; create only if the name is absent
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # tag ruleset first, if you decide to apply it
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
+# read back
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full role. Compare `rulesets/$ID` with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters. A ruleset that fails the read-back is deleted by id (only one you created) and reported. After a timeout, list the rulesets again before any retry; on the first 403, stop and report.
+
+Scratch self-test before the first real create (from a scratch clone of this repository, never from IronClaude; the throwaway branch is `zz-ruleset-selftest`; the scratch ruleset is `zz-selftest-<role>`):
+
+```bash
+REPO=ironops-marketplace
+ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
+jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/protect-main.json | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git commit --allow-empty -m "selftest: this push must be refused"
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+The empty-commit push must be refused (error GH013). The last command must show no name that starts with `zz-selftest-`. Delete only rulesets that you created.
+
+Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, with `$REPO` and `$ID`):
+
+```bash
+REPO=ironops-marketplace
+ID=<id of the ruleset you apply this to>
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
+# push the fix
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
+```
+
+Revert (rolls a ruleset back completely; run it on its own, never in the same run as the break-glass block, and only for a ruleset you created):
+
+```bash
+REPO=ironops-marketplace
+ID=<id of the ruleset to delete>
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+### 4. The tag ruleset
+
+No `v*` tag exists (0 `v*` refs, no tag of any name) and the repository has no workflow at all (HTTP 404 on the workflows folder; Actions shows 0 workflows and 0 runs). Nothing can move or delete a tag, so the tag ruleset is safe to apply. Its README says its artifacts are built from a source repository that Clay did not read (UNVERIFIED); please check that nothing there pushes tags to this repository before applying the tag ruleset.
+
+### 5. Report back
+
+What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `rules/branches/$BRANCH` and `rulesets/$ID`, the result of the scratch self-test, and the output of the admin-only checks above.
+
+## Request to the lead
+
+Please hand this text to Ryan (`ironbelly`) as the instruction for IronHands-CLI, irondots and ironops-marketplace, and ask Ryan to report the ids, dates and read-back output on issue 837 once the rulesets are applied. Until Ryan reports, issue 837 stays open.


Codegraph context: index_state: fresh; checked_at: 2026-11-26T15:31:43Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files of this task are JSON and Markdown (not indexed) unless a Python file is named; dependents were checked with Grep.
Note on files the diff cannot show: paths under `.dev/issues/837/private/` are git-ignored, so they are absent from the diff; read them directly with Read when a task names them. Never print private content in your answer.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/issues/837/handoff-ryan.md b/.dev/issues/837/handoff-ryan.md
index d9e768c9c..ac3ee772b 100644
--- a/.dev/issues/837/handoff-ryan.md
+++ b/.dev/issues/837/handoff-ryan.md
@@ -52,6 +52,7 @@ Expected: login `ironbelly`; admin `true`, default branch `main`, not archived,
 ```bash
 REPO=IronHands-CLI
 BRANCH=main
+ID=<id printed by the create call of the ruleset you are reading back>
 PARENT_OWNER=OpenHands
 # from a checkout of IronClaude at the pushed commit; create only if the name is absent
 gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
@@ -68,6 +69,7 @@ Scratch self-test before the first real create (from a scratch clone of this rep
 
 ```bash
 REPO=IronHands-CLI
+ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
 git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
 jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/protect-main.json | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
 git commit --allow-empty -m "selftest: this push must be refused"
@@ -79,16 +81,24 @@ gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
 
 The empty-commit push must be refused (error GH013). The last command must show no name that starts with `zz-selftest-`. Delete only rulesets that you created.
 
-Revert and break glass (the same commands as the IronClaude guide, with `$REPO` and `$ID`):
+Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, with `$REPO` and `$ID`):
 
 ```bash
 REPO=IronHands-CLI
-gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+ID=<id of the ruleset you apply this to>
 gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
 # push the fix
 gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
 ```
 
+Revert (rolls a ruleset back completely; run it on its own, never in the same run as the break-glass block, and only for a ruleset you created):
+
+```bash
+REPO=IronHands-CLI
+ID=<id of the ruleset to delete>
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
 ### 4. The tag ruleset
 
 No `v*` tag exists in the fork (0 `v*` refs, and no tag of any name; the parent's 25 tags have no `v` prefix). Clay's read-only search of its 14 workflows and the scripts they call found no producer that moves or deletes a `v*` tag. The tag ruleset would match nothing here today; apply it only if you want it in place for future `v*` tags, otherwise leave it out. Other IronbellyOrg repositories were not searched for a release token for this repository (UNVERIFIED).
@@ -138,6 +148,7 @@ Expected: login `ironbelly`; admin `true`, default branch `main`, not archived,
 ```bash
 REPO=irondots
 BRANCH=main
+ID=<id printed by the create call of the ruleset you are reading back>
 # from a checkout of IronClaude at the pushed commit; create only if the name is absent
 gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
 gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # tag ruleset first, if you decide to apply it
@@ -153,6 +164,7 @@ Scratch self-test before the first real create (from a scratch clone of this rep
 
 ```bash
 REPO=irondots
+ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
 git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
 jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/protect-main.json | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
 git commit --allow-empty -m "selftest: this push must be refused"
@@ -164,19 +176,27 @@ gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
 
 The empty-commit push must be refused (error GH013). The last command must show no name that starts with `zz-selftest-`. Delete only rulesets that you created.
 
-Revert and break glass (the same commands as the IronClaude guide, with `$REPO` and `$ID`):
+Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, with `$REPO` and `$ID`):
 
 ```bash
 REPO=irondots
-gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+ID=<id of the ruleset you apply this to>
 gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
 # push the fix
 gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
 ```
 
+Revert (rolls a ruleset back completely; run it on its own, never in the same run as the break-glass block, and only for a ruleset you created):
+
+```bash
+REPO=irondots
+ID=<id of the ruleset to delete>
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
 ### 4. The tag ruleset
 
-No `v*` tag exists (0 `v*` refs, no tag of any name). Its workflow `.github/workflows/gated-release.yml` only creates a tag (it refuses an existing one); creating a tag stays allowed under the tag ruleset, which has no creation rule. No workflow or script moves or deletes a tag. The tag ruleset is therefore safe to apply, and there is nothing to break. Other IronbellyOrg repositories were not searched for a release token for this repository (UNVERIFIED).
+No `v*` tag exists (0 `v*` refs, no tag of any name). Its workflow `.github/workflows/gated-release.yml` only creates a tag (it refuses an existing one); creating a tag stays allowed under the tag ruleset, which has no creation rule. No workflow or script moves or deletes a tag. Whether that workflow's own token can still create a `v*` tag once the tag ruleset is on is UNVERIFIED: before you apply the tag ruleset, confirm it (read the token the workflow uses and check that it can still create a tag under a ruleset that has no creation rule); until then the tag ruleset is not confirmed safe. Other IronbellyOrg repositories were not searched for a release token for this repository (UNVERIFIED).
 
 ### 5. Report back
 
@@ -223,6 +243,7 @@ Expected: login `ironbelly`; admin `true`, default branch `main`, not archived,
 ```bash
 REPO=ironops-marketplace
 BRANCH=main
+ID=<id printed by the create call of the ruleset you are reading back>
 # from a checkout of IronClaude at the pushed commit; create only if the name is absent
 gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
 gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json   # tag ruleset first, if you decide to apply it
@@ -238,6 +259,7 @@ Scratch self-test before the first real create (from a scratch clone of this rep
 
 ```bash
 REPO=ironops-marketplace
+ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
 git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
 jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/protect-main.json | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
 git commit --allow-empty -m "selftest: this push must be refused"
@@ -249,16 +271,24 @@ gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
 
 The empty-commit push must be refused (error GH013). The last command must show no name that starts with `zz-selftest-`. Delete only rulesets that you created.
 
-Revert and break glass (the same commands as the IronClaude guide, with `$REPO` and `$ID`):
+Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, with `$REPO` and `$ID`):
 
 ```bash
 REPO=ironops-marketplace
-gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+ID=<id of the ruleset you apply this to>
 gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
 # push the fix
 gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
 ```
 
+Revert (rolls a ruleset back completely; run it on its own, never in the same run as the break-glass block, and only for a ruleset you created):
+
+```bash
+REPO=ironops-marketplace
+ID=<id of the ruleset to delete>
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
 ### 4. The tag ruleset
 
 No `v*` tag exists (0 `v*` refs, no tag of any name) and the repository has no workflow at all (HTTP 404 on the workflows folder; Actions shows 0 workflows and 0 runs). Nothing can move or delete a tag, so the tag ruleset is safe to apply. Its README says its artifacts are built from a source repository that Clay did not read (UNVERIFIED); please check that nothing there pushes tags to this repository before applying the tag ruleset.

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=scope at=.dev/issues/837/handoff-ryan.md:86 anchor=docs/developer-guide/branch-protection.md:183 chk=n,y,n,n family=break-glass-order fix=split revert and break glass into two labelled blocks first=A1 origin=new: The revert block runs DELETE before the two PUT calls although it is called the same commands as the guide, so a top to bottom run deletes the ruleset and the PUT calls then fail.
F1.2 sev=blocking trigger=B2 ac=scope at=.dev/issues/837/handoff-ryan.md:62 anchor=docs/developer-guide/branch-protection.md:98 chk=n,y,n,n family=id-undefined fix=set ID in each block first=A1 origin=new: ID is used in the read-back, the scratch DELETE and the revert block and never set, so the read-back reads rulesets/ and the scratch ruleset stays.
F2.1 sev=blocking trigger=B2 ac=scope at=.dev/issues/837/handoff-ryan.md:179 anchor=.dev/issues/837/audit/irondots.md:146 chk=n,y,n,n family=irondots-tag-token fix=qualify the statement and pass on the audit check first=A1 origin=new: The irondots tag section says the tag ruleset is safe to apply while the audit marks the workflow token behaviour UNVERIFIED.

Saved-probe re-check hit locations (may be empty): 55:ID=<id printed by the create call of the ruleset you are 
72:ID=<id of the zz-selftest- ruleset printed by the scratch
77:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/
88:ID=<id of the ruleset you apply this to>
89:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID
91:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID
98:ID=<id of the ruleset to delete>
99:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/
151:ID=<id printed by the create call of the ruleset you are
167:ID=<id of the zz-selftest- ruleset printed by the scratc
172:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets
183:ID=<id of the ruleset you apply this to>
184:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$I
186:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$I
193:ID=<id of the ruleset to delete>
194:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets
246:ID=<id printed by the create call of the ruleset you are
262:ID=<id of the zz-selftest- ruleset printed by the scratc
267:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets
278:ID=<id of the ruleset you apply this to>
279:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$I
281:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$I
288:ID=<id of the ruleset to delete>
289:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets
294:No `v*` tag exists (0 `v*` refs, no tag of any name) and


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
