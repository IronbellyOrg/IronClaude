c0c4c531706e593c1bf70f6fd5e66a05631eb518
Review one task for spec compliance.

Task brief: ## Task 6: Write the audit record for CPA-Manager-Plus

Depends on: Task 5

Write `.dev/issues/837/audit/CPA-Manager-Plus.md` following section 3.4 of `./source.md` with `REPO=CPA-Manager-Plus` (a fork where `clayphi` has admin; the parent is read from `gh api repos/IronbellyOrg/CPA-Manager-Plus --jq .parent.full_name`, expected `seakee/CPA-Manager-Plus`, so `PARENT_OWNER=seakee`), read-only. Use the same blocks as Task 5 and add: the fork test (`compare/$PARENT_OWNER:main...main`, recording `ahead_by` and `behind_by`); the events for `refs/heads/main`, and for any other branch you audit, with `time_period=year` filtered to `START`; the count of `v*` refs over every page and a check of the targets of the most recent `v*` tags against the parent's tags of the same name; and the producer search for the tag ruleset: list `.github/workflows` and read each workflow, record `gh api repos/IronbellyOrg/CPA-Manager-Plus/actions/runs --jq .total_count`, search for `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete` and `--force`, resolve each hit by reading it, and look for other IronbellyOrg repos that hold a release token for it with the read-only call `gh api -X GET search/code -f q='CPA-Manager-Plus org:IronbellyOrg'` (if that call fails, write "could not run" and block). Record the excluded branches `dev` and `release/v*` as exclusions, not protected.

Acceptance criteria:
- `.dev/issues/837/audit/CPA-Manager-Plus.md` exists with every block of section 3.4, including the fork test with the parent name, `ahead_by` and `behind_by`.
- The producer search table has one row per place searched (each workflow file, the code search, the tag import path) with the hit and how it was resolved, and an overall `CLEAR` or `BLOCKED` for the tag ruleset.
- The result line says `BLOCKED` while the installations read could not run, and names who clears it.
- The last section lists every command run, none of them POST, PUT or DELETE.
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
Start sha: c0c4c531706e593c1bf70f6fd5e66a05631eb518
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/audit/CPA-Manager-Plus.md


diff --git a/.dev/issues/837/audit/CPA-Manager-Plus.md b/.dev/issues/837/audit/CPA-Manager-Plus.md
new file mode 100644
index 000000000..517e7de38
--- /dev/null
+++ b/.dev/issues/837/audit/CPA-Manager-Plus.md
@@ -0,0 +1,163 @@
+# Audit record: IronbellyOrg/CPA-Manager-Plus
+
+Phase 1, read-only (issue 837, section 3.4 of the design). `REPO=CPA-Manager-Plus`, `BRANCH=main`, `PARENT_OWNER=seakee`. Only `gh api` GET calls were made. Never staged.
+
+## Header
+
+| Item | Value |
+|---|---|
+| `END` | `2026-11-26T15:41:40Z` (from `date -u +%Y-%m-%dT%H:%M:%SZ`) |
+| `START` | `2026-08-28T15:41:40Z` (from `date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ`) |
+| Audited ref | `refs/heads/main` |
+| Other branches | `dev` and `release/v*` exist; they are exclusions, not protected (see Tips) |
+
+## Preflight
+
+| Check | Result |
+|---|---|
+| `gh api user --jq .login` | `clayphi` |
+| `permissions.admin`, `default_branch`, `archived`, `private` | `true`, `main`, `false`, `false` (public repository, `clayphi` has admin) |
+
+## Counts
+
+| Read | Result |
+|---|---|
+| `repos/IronbellyOrg/$REPO/hooks --jq length` | `0` |
+| `repos/IronbellyOrg/$REPO/keys --jq length` | `0` |
+| `repos/IronbellyOrg/$REPO/branches/main/protection` | HTTP 404, `{"message":"Branch not protected"}` (expected: no classic protection) |
+| `repos/IronbellyOrg/$REPO/actions/secrets --jq .total_count` | `0` |
+| `gh api --paginate orgs/IronbellyOrg/installations` | **could not run.** Real error text: `gh: Not Found (HTTP 404)` followed by `gh: This API operation needs the "admin:org" scope. To request it, run: gh auth refresh -h github.com -s admin:org`. Not recorded as clean; it is listed in Blocks. |
+
+## Existing rulesets
+
+`gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` printed nothing (exit 0): no rulesets exist (expected).
+
+## Fork test
+
+| Item | Result |
+|---|---|
+| Fork | yes (`gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name,.parent.private] \| @tsv'` prints `true`, `seakee/CPA-Manager-Plus`, `false`) |
+| Parent (`PARENT_OWNER`) | `seakee/CPA-Manager-Plus` (so `PARENT_OWNER=seakee`) |
+| `compare/seakee:main...main` | `ahead_by` = **0**, `behind_by` = **198** (status `behind`) |
+| Fork created, last push | created `2026-10-05T10:52:31Z`; `pushed_at` `2026-10-05T11:36:31Z` |
+
+Implied role on apply day: `ahead_by` is 0, so the role that follows from D7/G4 is the mirror file `protect-main-mirror.json` (`deletion`, `non_fast_forward`, no `pull_request` rule). The mirror needs Clay's written acceptance of its direct-push exposure (G4); `.dev/issues/837/issue-summary.md` records none (a search for "mirror" and "accept" finds no such answer), so G4 fails today and the branch ruleset is skipped and reported. If `ahead_by` is above 0 on apply day, the role switches to the full file `protect-main.json`. Both files may be candidates, so both have a revert line below.
+
+## Tips
+
+| Branch | Command | SHA (40 characters) |
+|---|---|---|
+| `main` (audited) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha` | `fb3e8f501f47a29b0fa66a5bf31f0f36739750d3` |
+| parent `main` (for comparison) | `gh api repos/seakee/CPA-Manager-Plus/git/ref/heads/main --jq .object.sha` | `dcfa8bc0af4770bb86f4dae9f1176a1ce884daca` |
+| `dev` (exclusion) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/dev --jq .object.sha` | `d1de5489da658f939b578012b2b1a30df4c398ab` |
+
+The fork's `main` tip `fb3e8f501f47a29b0fa66a5bf31f0f36739750d3` exists in the parent (`gh api repos/seakee/CPA-Manager-Plus/commits/<sha>` returns the same SHA), is the merge commit of 2026-10-04 "promote v1.14.3 to main", and is the target of tag `v1.14.3`. The fork's `main` is therefore a strict ancestor of the parent's `main`.
+
+Excluded branches (exclusions, not protected): `dev` and `release/v*`. The branch list (`gh api --paginate repos/IronbellyOrg/$REPO/branches --jq '.[].name'`) shows `dev` and seven `release/v*` branches: `release/v1.13.0`, `release/v1.13.1`, `release/v1.13.2`, `release/v1.14.0`, `release/v1.14.1`, `release/v1.14.2`, `release/v1.14.3` (confirmed with `git/matching-refs/heads/release/v`). It also holds `update-channel` and `v2` and many `feat/*`, `fix/*`, `chore/*`, `docs/*`, `test/*` branches; they are outside this audit and are not covered by the rulesets, which name `refs/heads/main` only.
+
+## Events kept
+
+Command: `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`. `time_period=quarter` was not used (its length is UNVERIFIED).
+
+Classification method: `activity_type` is read from each row. `branch_creation` rows are classed `branch_creation`. A `push` row is classed `direct push by human` unless the actor is a bot or known automation (`direct push by automation`); a push that is a merge made through a pull request is `pr_merge`; a push whose `after` SHA is a fast-forward of the parent's `main` (compare the pushed SHA with the parent, `compare` or `repos/seakee/CPA-Manager-Plus/commits/<sha>`) is `sync`.
+
+Rows kept in the window `START` to `END`: **0**. The same endpoint with no date filter (the whole `time_period=year` answer for `refs/heads/main`) also returned 0 rows (the raw answer is `[]`), so the filter dropped nothing.
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| (none) | | | | | |
+
+Counts by class: direct push by human 0, direct push by automation 0, sync 0, pr_merge 0, branch_creation 0. Consistent with the other facts: the fork was created `2026-10-05`, its `pushed_at` (`2026-10-05T11:36:31Z`) equals the creation of a feature branch and not a push to `main`, and its `main` tip is still the parent's commit of `v1.14.3`. Whether a Sync fork would appear in this endpoint is UNVERIFIED (no such event exists to test with). The endpoint without a `ref` filter returned two rows for the whole repository in the year, both `branch_creation` by `clayphi` on `feat/*` branches on 2026-10-05; they are not on the audited ref and are not kept.
+
+## Tag evidence
+
+- Number of `v*` refs: **72**. Command: `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` printed one per-page count, `72` (one page); the sum of the per-page counts is 72. Of the 72, 56 are lightweight tags (type `commit`) and 16 are annotated (type `tag`).
+- The parent has 79 `v*` refs (same command on `repos/seakee/CPA-Manager-Plus`). All 72 fork tags exist in the parent with the same name and the same object SHA (0 differ); no `v*` tag exists only in the fork; 7 parent tags are not in the fork.
+- Five newest `v*` tags of the fork by version order (`sort -V`), each compared with the parent's tag of the same name (type and SHA): `v1.13.2` (`1fa5e8a79ce067350d9a5ba6dd5a7b1843cc77f4`), `v1.14.0` (`eea422fd6a19ddb90f117b79b80d1f785a3b6a83`), `v1.14.1` (`aa8c5e9886b42ec82d78a419a1e1f59700ca90c5`), `v1.14.2` (`05ebb7f275dbe575211cb886436d4b99936c1cd9`), `v1.14.3` (`fb3e8f501f47a29b0fa66a5bf31f0f36739750d3`). All five match the parent's target.
+- The activity endpoint shows no tag events, so tag writes are invisible to this audit (INV-009).
+
+## Producer search
+
+`gh api repos/IronbellyOrg/CPA-Manager-Plus/actions/runs --jq .total_count` prints `0`: no workflow run has ever happened in the fork. `gh api repos/IronbellyOrg/$REPO/actions/workflows` lists no workflows (why is UNVERIFIED; workflows of a fork are usually disabled until someone enables them), repository Actions are `enabled` with `allowed_actions` `all`, and the repository has `0` Actions secrets. Search terms applied to every file: `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`, plus HTTP methods (`--request`, `-X`, `method:`), `contents: write`, `gh api` and `gh release`. A hit is resolved by reading it.
+
+| Place | Hit | How resolved |
+|---|---|---|
+| `.github/workflows/demo-pages.yml` (72 lines) | none for the terms; `push` is only the trigger; permissions `contents: read`, `pages: write` | Read in full. It builds and deploys pages; touches no ref. |
+| `.github/workflows/issue-check.yml` (110 lines) | none; permission `issues: write`; uses issue label and comment calls only | Read in full. No ref or release call. |
+| `.github/workflows/main-promotion.yml` (133 lines) | none for the terms; it retargets pull requests to `dev` through a GitHub App token with `permission-pull-requests: write` and checks that PRs into `main` come from `dev` | Read in full. Edits pull request bases only; no ref write. Relevant to the full role: PRs into `main` must come from the repo's own `dev`. |
+| `.github/workflows/pr-check.yml` (357 lines) | `push:` trigger and `docker/build-push-action` with `push: false` | Read the trigger, every permission block (`contents: read`, `pull-requests: read`) and every line that matched the terms. No ref write. |
+| `.github/workflows/pr-template.yml` (68 lines) | none; permission `contents: read` | Read in full. |
+| `.github/workflows/release.yml` (893 lines; triggers: push of tags `v*`, and `workflow_dispatch`) | `git/refs` in the script it calls (`bin/release/authorize-release-dispatch.mjs`, job `release_gate`, `contents: write`): a single `POST /git/refs` with `ref: refs/tags/<tag>` (tag **creation**, and only on a manual publish); `softprops/action-gh-release` with `tag_name` (draft and publish of a release); `curl --request PATCH` on a release (`draft: false`, `make_latest`); no `git push`, no `git tag -d`, no `push --delete`, no `--force`, no `DELETE` anywhere | Read the trigger, the permissions, the `release_gate` job and the lines of every release, `curl` and method hit; read the called scripts in `bin/release/` (see the next rows). The only ref write is a tag create. The `deletion`, `non_fast_forward` and `update` rules of the tag ruleset do not block creating a tag. |
+| `.github/workflows/release-publish-recovery.yml` (1310 lines; `workflow_dispatch`) | `--request PATCH` on a release (publish a verified draft); `git fetch --tags origin` and `git rev-parse refs/tags/...` (reads); no tag write | Read the trigger, the permissions, every line that matched the terms and the method hits. It does not write, move or delete a tag. |
+| `.github/workflows/release-telegram-recovery.yml` (167 lines; `workflow_dispatch`) | `git fetch --no-tags origin`, `git rev-parse`, `git show`, `git merge-base` (reads); permission `contents: read` | Read the git and `curl` lines and permissions. No ref write. |
+| `.github/workflows/update-index-publish.yml` (37 lines) and `update-index-recovery.yml` (26 lines) | permission `contents: write`; run `node bin/release/publish-update-index.mjs` | Read in full, then read the script: it uses `PATCH /git/refs/heads/update-channel` with `force: false` or `POST /git/refs` for `refs/heads/update-channel` (a branch, not a tag), `PATCH /releases/<id>` and tree and commit creation. No tag write. |
+| Other called scripts in `bin/release/` (11 files, all read through search for `git/refs`, `DELETE`, `method`, `force`, `refs/tags`, `git tag`) | `authorize-release-dispatch.mjs`: tag `POST` (create); `publish-update-index.mjs`: branch `update-channel` update without force; the others (`validate-release.mjs`, `verify-published-release.mjs`, `generate-release-info.mjs`, `update-contract.mjs`, `validate-release-contributors.mjs`, `package-native.sh`, `send-telegram-release.sh`, `check-*.mjs`) have no ref write | Resolved by reading the matched lines; no `DELETE` and no force flag exist in any script. `bin/native/*` and `bin/install-cpamp.sh` are end-user install and control scripts and are not called by any workflow (UNVERIFIED beyond the workflow search). |
+| Code search `gh api -X GET search/code -f q='CPA-Manager-Plus org:IronbellyOrg'` | 4 hits, all in private IronbellyOrg repositories; hits in public repositories: 0. For each hit: a hit in a private IronbellyOrg repository (name kept out of this file) | Each hit was read. None is a mechanism that holds a release token for this repository or moves its tags (conclusion only; nothing else about the hits is kept in this file). Code search sees only indexed files and cannot see Actions secrets of other repositories, so a token kept as a secret there is UNVERIFIED. |
+| Tag import path (how tags arrive from the parent) | The fork's 72 `v*` tags equal the parent's tags of the same name; no workflow in the fork fetches the parent (every `git fetch` names `origin`, the fork itself); there are no secrets and no runs | The fork has no automated import of parent tags. How the 72 tags got into the fork (copied with the fork at creation, or pushed by a person) is UNVERIFIED, and later manual pushes are invisible to this audit (INV-009). A re-pointed parent tag imported by force would be refused by the `update` and `non_fast_forward` rules; none of the 72 differs today. |
+
+Producer search verdict for the tag ruleset: **CLEAR**. The only tag write in the fork's workflows is creation of a new `v*` tag, which the tag ruleset (`deletion`, `non_fast_forward`, `update`) does not block; nothing deletes or moves a tag; the fork has never run a workflow and has no secrets. Remaining UNVERIFIED items: why the workflow list is empty, how tags were imported, and any secret held by another repository. This verdict does not clear the installations read; see Blocks.
+
+## Blocks
+
+| Ruleset | Missing check or event | Who clears it | What clears it |
+|---|---|---|---|
+| `protect-main` (full role) or `protect-main-mirror` (mirror role) (branch, `refs/heads/main`) | `gh api --paginate orgs/IronbellyOrg/installations` could not run (needs the `admin:org` scope; `clayphi`'s token lacks it) | An organisation owner of IronbellyOrg, or Clay in writing | An organisation owner runs the read and records its output here, or Clay's written acceptance of the missing read is quoted from `.dev/issues/837/issue-summary.md` (no such acceptance is recorded there today) |
+| `protect-main-mirror` (mirror role) | G4: Clay's written acceptance of the mirror's direct-push exposure | Clay | Clay's acceptance quoted word for word in `.dev/issues/837/issue-summary.md`; without it the fork's branch ruleset is skipped and reported (no acceptance is recorded today) |
+| `protect-release-tags` (tag, `refs/tags/v*`) | The same installations read (the producer search itself is `CLEAR`) | An organisation owner of IronbellyOrg, or Clay in writing | As in the first row |
+
+## Result
+
+**BLOCKED.**
+
+Reasons:
+1. The installations read could not run (HTTP 404, `admin:org` scope missing), and it is not recorded as clean. It is cleared by an organisation owner of IronbellyOrg, or by Clay's written acceptance quoted from `.dev/issues/837/issue-summary.md`; nothing there records that acceptance today.
+2. For the mirror role only: Clay's written acceptance of the direct-push exposure (G4) is not recorded.
+
+For the record, the other checks are clean: `hooks` 0, `keys` 0, no classic branch protection, no existing ruleset, 0 events on `main` in 90 days (no direct push by a human or by automation, no `sync`, no `pr_merge`), `ahead_by` 0, and the tag producer search is `CLEAR`.
+
+## Revert commands
+
+Written before any write on this repository. The id column is empty until apply. A branch ruleset is created from one of two files (full or mirror, chosen on apply day), so each has a line; the tag ruleset has one line.
+
+| Ruleset | Revert command | Id |
+|---|---|---|
+| `protect-main` (full role) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=CPA-Manager-Plus` | |
+| `protect-main-mirror` (mirror role) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=CPA-Manager-Plus` | |
+| `protect-release-tags` | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=CPA-Manager-Plus` | |
+
+## Self-test of the record
+
+UNVERIFIED and not run in Phase 1: whether `clayphi`'s token can create rulesets on this repository, whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, and whether the Sync fork button is refused under a `pull_request` rule.
+
+## Commands run
+
+All are read-only calls (none is POST, PUT, PATCH or DELETE; the only method flag is `-X GET`). `REPO=CPA-Manager-Plus`, `PARENT_OWNER=seakee`; `END` and `START` as in the header. Workflow and script files were decoded into private temporary directories under `/tmp` and searched there.
+
+1. `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)`; `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`
+2. `gh api user --jq .login`
+3. `gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'`
+4. `gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name,.parent.private] | @tsv'`
+5. `gh api repos/IronbellyOrg/$REPO/hooks --jq length`
+6. `gh api repos/IronbellyOrg/$REPO/keys --jq length`
+7. `gh api repos/IronbellyOrg/$REPO/branches/main/protection` (HTTP 404)
+8. `gh api --paginate orgs/IronbellyOrg/installations` (HTTP 404, `admin:org` scope missing)
+9. `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'`
+10. `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha`
+11. `gh api --paginate repos/IronbellyOrg/$REPO/branches --jq '.[].name'`
+12. `gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by,.behind_by,.status] | @tsv'`
+13. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`
+14. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | [.timestamp,.activity_type,.actor.login] | @tsv'` (the unfiltered cross-check) and the same URL without `--jq` (raw `[]`)
+15. `gh api "repos/IronbellyOrg/$REPO/activity?time_period=year&per_page=100" --jq length` and the same with `--jq '.[] | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'` (no ref filter)
+16. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`, and with `--jq '.[] | [.ref,.object.type,.object.sha] | @tsv'`
+17. `gh api --paginate repos/seakee/CPA-Manager-Plus/git/matching-refs/tags/v --jq '.[] | [.ref,.object.type,.object.sha] | @tsv'`
+18. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows --jq '.[] | [.name,.path,.type] | @tsv'`
+19. `gh api repos/IronbellyOrg/$REPO/actions/runs --jq .total_count`
+20. `gh api -X GET search/code -f q='CPA-Manager-Plus org:IronbellyOrg' --jq '[.total_count, (.items|length)] | @tsv'`; the same call with `--jq` listing each hit's repository and `private` flag, piped to `sort | uniq -c`; and the same call with `-H 'Accept: application/vnd.github.text-match+json'` to read each hit (output not recorded in this file)
+21. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows/<name>.yml --jq .content | base64 -d` for each of the ten workflow files
+22. `gh api repos/seakee/CPA-Manager-Plus/commits/fb3e8f501f47a29b0fa66a5bf31f0f36739750d3 --jq .sha`; `gh api repos/IronbellyOrg/$REPO/commits/fb3e8f501f47a29b0fa66a5bf31f0f36739750d3 --jq '[.commit.committer.date,.commit.message] | @tsv'`
+23. `gh api repos/seakee/CPA-Manager-Plus/git/ref/heads/main --jq .object.sha`; `gh api repos/seakee/CPA-Manager-Plus/git/ref/heads/dev --jq .object.sha`; `gh api repos/IronbellyOrg/$REPO/git/ref/heads/dev --jq .object.sha`
+24. `gh api repos/IronbellyOrg/$REPO --jq '[.created_at,.pushed_at,.updated_at] | @tsv'`
+25. `gh api repos/IronbellyOrg/$REPO/git/matching-refs/heads/release/v --jq '.[].ref'`
+26. `gh api repos/IronbellyOrg/$REPO/contents/bin/release --jq '.[] | [.name,.size] | @tsv'`; `gh api repos/IronbellyOrg/$REPO/contents/bin --jq '.[] | [.name,.type] | @tsv'`; `gh api repos/IronbellyOrg/$REPO/contents/bin/ci` and `.../bin/native` (names only); `gh api repos/IronbellyOrg/$REPO/contents/bin/release/<name> --jq .content | base64 -d` for each of the 11 files
+27. `gh api repos/IronbellyOrg/$REPO/actions/secrets --jq '[.total_count] | @tsv'`; `gh api repos/IronbellyOrg/$REPO/actions/workflows --jq '.workflows[] | [.path,.state] | @tsv'` (empty); `gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled,.allowed_actions] | @tsv'`
+28. Local only: `grep`, `sed -n`, `cat`, `sort`, `join`, `comm` over the decoded files; `jq` over `.github/rulesets/other-repos/*.json` and `.github/rulesets/protect-release-tags.json`; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/CPA-Manager-Plus.md`.


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
