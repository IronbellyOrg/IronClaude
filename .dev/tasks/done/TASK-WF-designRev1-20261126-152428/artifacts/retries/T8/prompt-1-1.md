350491022cacf81329f71e46bdaadd2a48c23ca6
Review one task for spec compliance.

Task brief: ## Task 8: Write the audit record for IronHands-CLI

Depends on: Task 5

Write `.dev/issues/837/audit/IronHands-CLI.md` following section 3.4 of `./source.md` with `REPO=IronHands-CLI`, a handoff repo where `clayphi` has only read access, read-only. Record: the header; `gh api repos/IronbellyOrg/IronHands-CLI --jq '[.fork,.parent.full_name,.default_branch,.archived,.private] | @tsv'`; the fork test (it is a fork: `compare/$PARENT_OWNER:main...main`, recording `ahead_by` and `behind_by`), and the role that results: Ryan applies the mirror only when `ahead_by` is 0 and Clay's written acceptance of the mirror (gate G4) is quoted, otherwise the full role; the tip of `main`; the events of `refs/heads/main` for the 90 days, classified; the count of `v*` refs over every page; the workflow list read-only with the search for tag and push verbs, so Clay's workflow search for Ryan's tag ruleset is complete. Do not run the admin-only checks (`hooks`, `keys`, `branches/main/protection`, installations, classic protection): list them in a section "Checks Ryan must run (admin only)" with their commands. The result line says what Clay's read-only part found and that the apply belongs to Ryan.

Acceptance criteria:
- `.dev/issues/837/audit/IronHands-CLI.md` exists with the blocks that read access allows, a section "Checks Ryan must run (admin only)" with the exact commands using `REPO=IronHands-CLI`, and the fork test result with the parent name.
- The tag ruleset line says whether Clay's read-only workflow search found any producer that moves or deletes `v*` tags.
- No command in the file is a write, and the file states that nothing was written to the repo.
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
Start sha: 350491022cacf81329f71e46bdaadd2a48c23ca6
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/audit/IronHands-CLI.md


diff --git a/.dev/issues/837/audit/IronHands-CLI.md b/.dev/issues/837/audit/IronHands-CLI.md
new file mode 100644
index 000000000..14da61593
--- /dev/null
+++ b/.dev/issues/837/audit/IronHands-CLI.md
@@ -0,0 +1,177 @@
+# Audit record: IronbellyOrg/IronHands-CLI
+
+Phase 1, read-only (issue 837, section 3.4 of the design). `REPO=IronHands-CLI`, `BRANCH=main`, `PARENT_OWNER=OpenHands`. This is a handoff repo: `clayphi` has read access only, and Ryan applies anything that is applied. Only `gh api` GET calls were made. **Nothing was written to this repository** (no ruleset, branch, tag, comment or file). Never staged.
+
+## Header
+
+| Item | Value |
+|---|---|
+| `END` | `2026-11-26T15:58:31Z` (from `date -u +%Y-%m-%dT%H:%M:%SZ`) |
+| `START` | `2026-08-28T15:58:31Z` (from `date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ`) |
+| Audited ref | `refs/heads/main` |
+| Who runs the apply | Ryan (`ironbelly`), not Clay |
+
+## Preflight (read access only)
+
+| Check | Result |
+|---|---|
+| `gh api user --jq .login` | `clayphi` |
+| `gh api repos/IronbellyOrg/IronHands-CLI --jq '[.fork,.parent.full_name,.default_branch,.archived,.private] \| @tsv'` | `true`, `OpenHands/OpenHands-CLI`, `main`, `false`, `false` (a fork of a public parent, default branch `main`, not archived, public) |
+| `permissions.admin`, `permissions.push`, `permissions.pull` | `false`, `false`, `true`: `clayphi` can read only, as Clay's recorded answer says. The admin preflight (G2) therefore cannot pass for `clayphi` and is Ryan's to run. |
+| `created_at`, `pushed_at` | `2026-02-27T20:58:09Z`, `2026-03-17T03:43:32Z` |
+
+## Counts
+
+Not run by Clay: `hooks`, `keys`, `branches/main/protection` and the organisation installations read are admin-only here. They are listed with their commands in "Checks Ryan must run (admin only)". Nothing is recorded as clean for them.
+
+One extra read was tried and refused: `gh api repos/IronbellyOrg/$REPO/actions/permissions` returned HTTP 403, **could not run**, real error text: `gh: You must have repository read permissions or have the repository Actions policies fine-grained permission. (HTTP 403)`. It is not needed for the result; whether Actions are enabled for the repository as a whole is UNVERIFIED (the per-workflow states below were readable).
+
+## Existing rulesets
+
+`gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` printed nothing (exit 0): no ruleset is visible to a read-only login. A ruleset in `disabled` or `evaluate` mode may be hidden from a login without admin (UNVERIFIED), so Ryan re-runs this list with admin (G7) before any create.
+
+## Fork test
+
+| Item | Result |
+|---|---|
+| Fork | yes |
+| Parent (`PARENT_OWNER`) | `OpenHands/OpenHands-CLI` (public; so `PARENT_OWNER=OpenHands`) |
+| `compare/OpenHands:main...main` | `ahead_by` = **13**, `behind_by` = **73** (status `diverged`) |
+
+Role that results (G4): `ahead_by` is 13, above 0, so the fork carries its own commits on `main` and the mirror role does not fit. The role is the **full role**, `.github/rulesets/other-repos/protect-main.json` (name `protect-main`, target `refs/heads/main`). `protect-main-mirror.json` is not the candidate. The mirror would in any case also need Clay's written acceptance of its direct-push exposure, and `.dev/issues/837/issue-summary.md` records none (a case-insensitive search for "mirror" in that file finds 0 lines). The rule is: the mirror only when `ahead_by` is 0 and Clay's written acceptance is quoted, otherwise the full role. Clay's recorded answer for this repository, word for word from `.dev/issues/837/issue-summary.md`: "IronHands-CLI, irondots and ironops-marketplace need Ryan (Clay's login has only read there): do not write to them; prepare what Ryan must apply and ask the lead to hand it to Ryan." Ryan re-runs the compare in R0.
+
+## Tips
+
+| Branch | Command | SHA (40 characters) |
+|---|---|---|
+| `main` (audited) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha` | `8bf4a3eee8805f0b89955688d71b0cdb82f36d92` |
+| parent `main` (for comparison) | `gh api repos/OpenHands/OpenHands-CLI/git/ref/heads/main --jq .object.sha` | `283c6ac3610f4299f405f7389f65766dcb83e12a` |
+
+The fork's `main` tip equals the `after` SHA of its newest `main` event (a push by `ironbelly` on 2026-03-17). No other branch is audited.
+
+## Events kept
+
+Command: `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`. `time_period=quarter` was not used (its length is UNVERIFIED).
+
+Classification method: `branch_creation` rows are `branch_creation`; a `push` or `force_push` row by a person is `direct push by human`, by a bot or a known automation `direct push by automation`; a `pr_merge` row is `pr_merge`; a push whose commit is a fast-forward of the parent's `main` is `sync` (decided by comparing the pushed SHA with the parent).
+
+Rows kept in the window `START` to `END`: **0**. The filter dropped 12 rows, all older than the window (the newest is 2026-03-17T03:43:32Z, 254 days before `END`), so the window holds no event on `main`.
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| (none in the window) | | | | | |
+
+Counts by class in the window: direct push by human 0, direct push by automation 0, sync 0, pr_merge 0, branch_creation 0.
+
+For context only, not kept (outside the 90 days): the same endpoint for `refs/heads/main` returned 12 rows from 2026-02-28 to 2026-03-17, all by actor `ironbelly`: 5 `push`, 4 `pr_merge`, 3 `force_push`. They are not classified here because they are outside the window. They show that a person has pushed to this `main` directly and force-pushed it before, so Ryan should expect the full role to change how he works on `main`; whether `ironbelly` bypasses the rulesets as an admin is UNVERIFIED. The endpoint without a `ref` filter returned 21 rows for the year; the other 9 are on feature or fix branches (creation, push, deletion) and are not on the audited ref. Whether a Sync fork would appear in this endpoint is UNVERIFIED (no such event exists to test with).
+
+## Tag evidence
+
+- Number of `v*` refs: **0**. Command: `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` printed one per-page count, `0` (one page); the sum of the per-page counts is 0.
+- The fork has **no tag of any name** (`git/matching-refs/tags --jq length` prints `0`). The parent `OpenHands/OpenHands-CLI` has 0 `v*` refs and 25 tags in total, named without a `v` prefix (newest `1.16.0`, then `1.15.1`, `1.15.0`, `1.14.0`, `1.13.1`). The repository's own release document says so: "This project uses tags **without** a `v` prefix (e.g., `1.13.0`, not `v1.13.0`)."
+- The comparison of the five newest `v*` tags with the parent's tags of the same name has nothing to compare: there is no `v*` tag in the fork or in the parent, and the fork holds no tag at all, so no parent tag has been imported.
+- The activity endpoint shows no tag events, so tag writes are invisible to this audit (INV-009).
+- Consequence for the tag ruleset: `.github/rulesets/protect-release-tags.json` matches `refs/tags/v*`, so on this repository it would match no existing tag and none of the parent's tag names. Whether to change the pattern for this repository is a decision for Clay and Ryan; it is not made here.
+
+## Producer search
+
+Workflows listed with `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows` (14 files). Each was read (decoded into a private temporary directory under `/tmp` and searched there), then the files they call were read: `build.sh`, `.github/scripts/update_pr_description.sh`, and the three prompt files in `.github/prompts/` that an agent step is given. `RELEASE_PROCEDURE.md` was read for how tags are made. Search terms applied to every file: `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`, plus `--delete`, `git tag`, `-X`, `--method`, `--request`, `DELETE`, `gh api`, `gh release`, `refs/tags`, `contents: write`. A hit is resolved by reading it. Workflow state in the fork (`actions/workflows`): `check-package-versions`, `lint` and `pypi-release` are `active`; `good-first-issue-labeler` and `stale` are `disabled_fork`; the other nine are `disabled_manually`. `actions/runs` reports a `total_count` of 16.
+
+| Place | Hit | How resolved |
+|---|---|---|
+| `bump-version.yml` (187 lines; `workflow_dispatch`; permissions `contents: read`) | `git push origin "$BRANCH_NAME"` | Read. It pushes the new branch `bump-version-<version>` (created in the same job with `git checkout -b`) and opens a draft pull request by `curl -X POST` on `/pulls`. No push to `main`, no tag. |
+| `bump-agent-sdk-version.yml` (151 lines; `workflow_dispatch`; `contents: read`) | `git push origin "$BRANCH_NAME"` | Read. It pushes the new branch `bump-agent-sdk-<version>` and opens a pull request by `curl -X POST` on `/pulls`. No push to `main`, no tag. |
+| `update-install-website.yml` (135 lines; `release: published` or `workflow_dispatch`; `contents: read`) | `git push origin "$BRANCH_NAME"` and `curl -X POST` | Read. The push runs after `cd website-repo`, a clone of a different repository (`All-Hands-AI/install-openhands-website`); the `POST` opens a pull request there. It writes nothing to this repository. |
+| `cli-build-binary-and-optionally-release.yml` (133 lines; triggers: push to `main`, push of any tag, pull request; `contents: write`) | `tags: '*'` trigger; `contents: write`; `startsWith(github.ref, 'refs/tags/')`; `softprops/action-gh-release@v2` | Read. It reacts to a tag that already exists (build, then create a **draft** release with the built binaries). It does not create, move or delete a tag. It is `disabled_manually` in the fork. |
+| `pypi-release.yml` (51 lines; `workflow_dispatch` or push of any tag; `id-token: write`) | `tags: '*'` trigger | Read in full. It builds and publishes the package. It does not touch a ref. `active` in the fork. |
+| `type-checking-report.yml` (218 lines; weekly schedule and `workflow_dispatch`; `contents: write`, `issues: write`, `pull-requests: write`) | `contents: write`; `gh issue create`; two agent steps that run the CLI with a prompt file | Read the workflow and the called prompts. The first prompt only analyses and writes a report; the second (`auto-fix-low-hanging.md`) tells the agent to create branches named `fix/code-quality/<name>`, push them and open pull requests with `--base main`, at most 3 per run. No instruction to push to `main`, to create or delete a tag, or to force. `disabled_manually` in the fork. |
+| `check-package-versions.yml`, `lint.yml`, `tests.yml`, `good-first-issue-labeler.yml`, `pr-review-by-openhands.yml`, `pr-review-evaluation.yml`, `stale.yml`, `update-pr-description.yml` | `push:` triggers only (`check-package-versions`, `lint`, `tests`); no hit for any other term | Read the triggers, permissions and every `run` block. All are `contents: read` or have no write step to a ref. `update-pr-description.yml` calls `.github/scripts/update_pr_description.sh`, which uses `gh api` on `pulls/<n>` only (read the pull request, then update its description). |
+| `build.sh` | none for the terms | Read in full. It installs a build tool and runs the build script; no git or API call. |
+| `RELEASE_PROCEDURE.md` | `git tag 1.13.0` and `git push origin --tags` | Read. This is the manual release step: a person tags the version-bump branch and pushes the tag. It **creates** a tag (a tag name without a `v`); it does not move or delete one. A person's manual pushes of tags are invisible to this audit (INV-009). |
+| Other IronbellyOrg repositories that hold a release token for this repository (E-2) | not searched in Task 8 | UNVERIFIED. Task 8 does not run a code search across the organisation, so a release token held as a secret elsewhere is not excluded. |
+| How tags arrive from the parent | none found | No workflow in the fork fetches the parent. The fork holds no tag while the parent has 25, so no tag import has happened. Whether a person imports them later is UNVERIFIED. |
+
+Verdict for Clay's read-only workflow search: **no workflow or called script found that moves or deletes a `v*` tag, and none that deletes any tag**. The only tag writes found are a person's manual tag creation (`RELEASE_PROCEDURE.md`) and workflows that react to a tag push. Because the repository has no `v*` tag and its release tags have no `v`, the ruleset's `refs/tags/v*` pattern would match nothing here today (see Tag evidence). Remaining UNVERIFIED: any release token held in another repository; manual tag deletions or moves, which the audit cannot see.
+
+## Blocks
+
+| Ruleset | Missing check or event | Who clears it | What clears it |
+|---|---|---|---|
+| `protect-main` (full role, branch `refs/heads/main`) | Admin-only checks not run by Clay: `hooks`, `keys`, `branches/main/protection`, the organisation installations read (needs `admin:org`), Ryan's admin role | Ryan; an organisation owner for the installations read | Ryan runs the commands in "Checks Ryan must run (admin only)" and records the output; for the installations read, an organisation owner's output or Clay's written acceptance of the gap quoted from `.dev/issues/837/issue-summary.md` (none is recorded there today) |
+| `protect-main` | G1 Authority: the repository is a handoff repo; Clay's recorded answer is "do not write to them" | Ryan applies | Ryan's own apply from the handoff; Clay writes nothing |
+| `protect-main` | G7: the list of existing rulesets is empty only as seen by a read-only login | Ryan | Ryan re-runs the list with admin inside the hour before the first write |
+| `protect-main-mirror` | G4: `ahead_by` is 13, and no written acceptance of the mirror is recorded | Clay (acceptance); not applicable while `ahead_by` is above 0 | Not the candidate role while the fork is ahead of its parent |
+| `protect-release-tags` (tag, `refs/tags/v*`) | The same admin-only installations read; and the pattern matches no tag here (no `v*` tag, release tags have no `v`) | Ryan, with Clay | Ryan's admin-only checks, and a decision whether to apply a ruleset that matches nothing or to change the pattern for this repository |
+
+## Result
+
+**BLOCKED for Clay; the apply belongs to Ryan.**
+
+Clay's read-only part found: the repository is a public fork of `OpenHands/OpenHands-CLI` with default branch `main`, not archived; `ahead_by` 13 and `behind_by` 73 (diverged), so the role is the full role `protect-main.json`; no event on `main` in the 90 days (0 rows kept, so no direct push by a human or by automation, no `sync`, no `pr_merge`); no ruleset visible to a read-only login; no `v*` tag; and no workflow or script in the repository that moves or deletes a tag. Clay did not run, and cannot run, the admin-only checks, and Clay writes nothing to this repository. Ryan runs the admin-only checks, re-runs the audit inside the hour before the first write, and applies, from the handoff.
+
+Tag ruleset line: Clay's read-only workflow search found no producer that moves or deletes `v*` tags. The ruleset would match no tag in this repository today, and other IronbellyOrg repositories were not searched (UNVERIFIED).
+
+## Checks Ryan must run (admin only)
+
+None of these was run by Clay. Run them with Ryan's login (admin on the repository) and record the output here before the apply. Set `REPO=IronHands-CLI`.
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
+gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled,.allowed_actions] | @tsv'
+```
+
+Expect: login `ironbelly` (Ryan); admin `true`, default branch `main`, not archived and public; both counts `0`; the `branches/main/protection` call answering HTTP 404 `Branch not protected`; an empty ruleset list (an existing ruleset stops the repo; nothing pre-existing is updated or deleted); and a review of every installed app with `contents: write` (an app that can push must use pull requests once the ruleset is on, because only the admin role bypasses). The installations call needs the `admin:org` scope; if it fails, write "could not run" with the error text, and the repository stays blocked until an organisation owner runs it or Clay accepts the gap in writing. The `actions/permissions` call is the one that returned HTTP 403 for `clayphi`.
+
+The two checks Ryan also repeats, which Clay ran read-only, so the apply day figures are fresh (R0):
+
+```bash
+END=$(date -u +%Y-%m-%dT%H:%M:%SZ); START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)
+gh api "repos/IronbellyOrg/$REPO/compare/OpenHands:main...main" --jq '[.ahead_by,.behind_by] | @tsv'
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'
+```
+
+## Revert commands
+
+Written before any write on this repository, and to be run by Ryan only after a create by Ryan. The id column is empty until apply. The branch ruleset is created from one file (the full role is the candidate, the mirror is not), so each file has a line; the tag ruleset has one line.
+
+| Ruleset | Revert command | Id |
+|---|---|---|
+| `protect-main` (full role) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronHands-CLI` | |
+| `protect-main-mirror` (mirror role, only if the rule above allows it on apply day) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronHands-CLI` | |
+| `protect-release-tags` | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronHands-CLI` | |
+
+## Self-test of the record
+
+UNVERIFIED and not run: whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, whether the Sync fork button is refused under a `pull_request` rule, and whether a ruleset hidden from a read-only login exists.
+
+## Commands run
+
+All are read-only calls made with `gh api` (default GET); none is POST, PUT, PATCH or DELETE, and no method flag was used. `REPO=IronHands-CLI`, `PARENT_OWNER=OpenHands`; `END` and `START` as in the header. Nothing was written to the repository. Workflow, script and document files were decoded into a private temporary directory under `/tmp` and searched there.
+
+1. `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)`; `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`
+2. `gh api user --jq .login`
+3. `gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name,.default_branch,.archived,.private] | @tsv'`
+4. `gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin,.permissions.push,.permissions.pull,.parent.private,.created_at,.pushed_at] | @tsv'`; `gh api repos/IronbellyOrg/$REPO --jq '[.html_url,.visibility] | @tsv'`
+5. `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` (empty)
+6. `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha`
+7. `gh api "repos/IronbellyOrg/$REPO/compare/OpenHands:main...main" --jq '[.ahead_by,.behind_by,.status] | @tsv'`
+8. `gh api repos/OpenHands/OpenHands-CLI/git/ref/heads/main --jq .object.sha`
+9. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'` (no row)
+10. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | [.timestamp,.activity_type,.actor.login,.after] | @tsv'` (unfiltered cross-check, 12 rows)
+11. `gh api "repos/IronbellyOrg/$REPO/activity?time_period=year&per_page=100" --jq '.[] | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'` (no ref filter)
+12. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`, and with `--jq '.[] | [.ref,.object.type,.object.sha] | @tsv'`
+13. `gh api --paginate repos/OpenHands/OpenHands-CLI/git/matching-refs/tags/v --jq length`, and the same with the `@tsv` filter
+14. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags --jq length` and `--jq '.[].ref'`; the same two calls on `repos/OpenHands/OpenHands-CLI`
+15. `gh api repos/IronbellyOrg/$REPO/contents --jq '.[] | [.name,.type] | @tsv'`; `gh api repos/IronbellyOrg/$REPO/contents/.github --jq '.[] | [.name,.type] | @tsv'`
+16. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows --jq '.[] | [.name,.path,.type,.size] | @tsv'`
+17. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows/<name> --jq .content | base64 -d` for each of the 14 workflow files
+18. `gh api repos/IronbellyOrg/$REPO/contents/.github/scripts` and `.../.github/prompts` (names), then `gh api repos/IronbellyOrg/$REPO/contents/<path> --jq .content | base64 -d` for `.github/scripts/update_pr_description.sh`, the three files in `.github/prompts/`, `build.sh` and `RELEASE_PROCEDURE.md`
+19. `gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled,.allowed_actions]|@tsv'` (HTTP 403, could not run); `gh api repos/IronbellyOrg/$REPO/actions/workflows --jq '.workflows[]|[.path,.state]|@tsv'`; `gh api repos/IronbellyOrg/$REPO/actions/runs --jq .total_count`
+20. Local only: `grep`, `sed -n`, `cat`, `sort`, `comm`, `wc` over the decoded files; `ls` and `jq` over `.github/rulesets/other-repos/*.json` and `.github/rulesets/protect-release-tags.json`; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/IronHands-CLI.md`.


Codegraph context: index_state: fresh; checked_at: 2026-11-26T15:31:43Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files of this task are JSON and Markdown (not indexed) unless a Python file is named; dependents were checked with Grep.
Note on files the diff cannot show: paths under `.dev/issues/837/private/` are git-ignored, so they are absent from the diff; read them directly with Read when a task names them. Never print private content in your answer.
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
