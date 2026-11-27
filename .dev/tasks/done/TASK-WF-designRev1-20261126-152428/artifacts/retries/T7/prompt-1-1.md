8684a190601932c76b293925326a6c4f40428ed0
Review one task for spec compliance.

Task brief: ## Task 7: Write the audit record for IronOrca

Depends on: Task 5

Write `.dev/issues/837/audit/IronOrca.md` following section 3.4 of `./source.md` with `REPO=IronOrca` (a fork where `clayphi` has admin; expected parent `stablyai/orca`, so `PARENT_OWNER=stablyai`), read-only, with the same blocks as Task 6 and these additions. Audit `refs/heads/main` and also `refs/heads/aidev02` (events only, for the record; protecting `aidev02` needs Clay's written yes). For the producer search read every file in `.github/workflows`, note the guard on the write job of `release-cut.yml` (a write job that carries `if: github.repository == 'stablyai/orca'` never runs in the fork), note the scheduled workflows that do run in the fork, and record for each workflow whether it has an unfiltered `on: push` trigger (the runbook's scratch self-test pushes a throwaway branch; if any workflow would start on it, say which). Record the count of `v*` refs read over every page and how many are not plain `vX.Y.Z`, how tags arrive from the parent (a person importing them, or a workflow), and a check of recent `v*` tag targets against the parent's tags. Run the code search `gh api -X GET search/code -f q='IronOrca org:IronbellyOrg'`.

Acceptance criteria:
- `.dev/issues/837/audit/IronOrca.md` exists with every block of section 3.4, the fork test, the `main` and `aidev02` event tables and the tag evidence.
- Each workflow file in `.github/workflows` appears in the producer search table with its tag and push findings and its `on: push` status.
- The file states the apply-day role that the fork test implies (mirror if `ahead_by` is 0, full if above 0) as a note, and that the mirror needs Clay's written acceptance.
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
Start sha: 8684a190601932c76b293925326a6c4f40428ed0
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/audit/IronOrca.md


diff --git a/.dev/issues/837/audit/IronOrca.md b/.dev/issues/837/audit/IronOrca.md
new file mode 100644
index 000000000..129b9bdca
--- /dev/null
+++ b/.dev/issues/837/audit/IronOrca.md
@@ -0,0 +1,246 @@
+# Audit record: IronbellyOrg/IronOrca
+
+Phase 1, read-only (issue 837, section 3.4 of the design). `REPO=IronOrca`, `BRANCH=main` (and `aidev02`, events only), `PARENT_OWNER=stablyai`. Only `gh api` GET calls were made. Never staged.
+
+## Header
+
+| Item | Value |
+|---|---|
+| `END` | `2026-11-26T15:46:50Z` (from `date -u +%Y-%m-%dT%H:%M:%SZ`) |
+| `START` | `2026-08-28T15:46:50Z` (from `date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ`) |
+| Audited refs | `refs/heads/main` (candidate for a ruleset) and `refs/heads/aidev02` (events only, for the record) |
+| Other branches | the branch list shows 5 branches: `aidev02`, `main`, `clayphi/aidev02-safety-casts`, `ironbelly/agent-sleep-default`, `ironbelly/orca-idle-sleep`; only `main` is a ruleset candidate here |
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
+| `gh api --paginate orgs/IronbellyOrg/installations` | **could not run.** Real error text: `gh: Not Found (HTTP 404)` followed by `gh: This API operation needs the "admin:org" scope. To request it, run:  gh auth refresh -h github.com -s admin:org`. Not recorded as clean; it is listed in Blocks. |
+
+## Existing rulesets
+
+`gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` printed nothing (exit 0): no rulesets exist (expected).
+
+## Fork test
+
+| Item | Result |
+|---|---|
+| Fork | yes (`gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name,.parent.private] \| @tsv'` prints `true`, `stablyai/orca`, `false`) |
+| Parent (`PARENT_OWNER`) | `stablyai/orca` (so `PARENT_OWNER=stablyai`; the parent is public) |
+| `compare/stablyai:main...main` | `ahead_by` = **0**, `behind_by` = **1** (status `behind`) |
+| Fork created, last push | created `2026-10-27T13:51:17Z`; `pushed_at` `2026-11-26T15:42:31Z` (a sync push, see Events kept) |
+
+Implied role on apply day (note): `ahead_by` is 0, so the role that follows is the mirror file `protect-main-mirror.json` (`deletion`, `non_fast_forward`, no `pull_request` rule). The mirror needs Clay's written acceptance of its direct-push exposure (G4); `.dev/issues/837/issue-summary.md` records none (its "Decided for this work (iteration 3)" answer, line 37, covers the go for the repo and the 90-day check only), so G4 fails today and the branch ruleset is skipped and reported. If `ahead_by` is above 0 on apply day, the role switches to the full file `protect-main.json`. Both files may be candidates, so both have a revert line below. `aidev02` differs from the parent (`compare/stablyai:main...aidev02`: 27 ahead, 7081 behind, status `diverged`; `compare/main...aidev02`: 27 ahead, 7079 behind), so it is not a mirror of anything; protecting it needs Clay's written yes, which is not recorded (the file `.github/rulesets/other-repos/protect-aidev02.json` is not created).
+
+## Tips
+
+| Branch | Command | SHA (40 characters) |
+|---|---|---|
+| `main` (audited) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha` | `6e49dcea64bad7828798793cb772f36851378a16` |
+| `aidev02` (events only) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/aidev02 --jq .object.sha` | `5fa1a6608658947f5dbe56616fffa93f7802c90e` |
+| parent `main` (for comparison) | `gh api repos/stablyai/orca/git/ref/heads/main --jq .object.sha` | `17caa1a117e8d6ed8f7cce939941fbf71d927d56` |
+
+The fork's `main` tip `6e49dcea64bad7828798793cb772f36851378a16` is a commit of the parent ("fix(i18n): translate missing German strings for MCP servers and plugins (#49872)", committed `2026-11-26T15:39:47Z`, one parent, committer `web-flow`); the parent's `main` is one commit ahead of it.
+
+## Events kept
+
+Command (run once per branch): `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`. `time_period=quarter` was not used (its length is UNVERIFIED).
+
+Classification method: `activity_type` is read from each row. For a fork `main`, each pushed `after` SHA is compared with the parent: `gh api repos/stablyai/orca/commits/<sha>` returns the same SHA and `gh api "repos/stablyai/orca/compare/main...<sha>"` says `behind`, `ahead_by` 0, so the commit is part of the parent's history and the push is a parent fast-forward, class `sync`. A push that is not in the parent's history would be `direct push by human` or `direct push by automation`. For `aidev02`, a `push` whose `after` SHA is the `merge_commit_sha` of a merged pull request into `aidev02` is `pr_merge` (matched against `gh api "repos/IronbellyOrg/$REPO/pulls?state=closed&base=aidev02&per_page=10"`); a row with a zero `before` SHA is `branch_creation`.
+
+### `refs/heads/main`: 3 rows kept (window `START` to `END`; the same call without the date filter also returned 3 rows, so the filter dropped nothing)
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| 2026-11-26T15:42:31Z | refs/heads/main | push | ironbelly | 6e49dcea64bad7828798793cb772f36851378a16 | sync (parent commit, `ahead_by` 0 against parent `main`) |
+| 2026-10-28T02:41:06Z | refs/heads/main | push | ironbelly | e0f32dcac1d0669952bd5ec7c43fc94c9c0158df | sync (parent commit, `ahead_by` 0) |
+| 2026-10-27T14:43:41Z | refs/heads/main | push | ironbelly | dc57b3d6e81c9825446a520bf0aee8600a2f5586 | sync (parent commit, `ahead_by` 0) |
+
+The three rows chain (`before` of each row is `after` of the older one, starting at `f61e7f8bfe2ca576723364080dec8861436dbec9`, a parent commit made at `2026-10-27T13:50:25Z`, 52 seconds before the fork was created). Counts by class: direct push by human 0, direct push by automation 0, sync 3, pr_merge 0, branch_creation 0. Every commit is single-parent with committer `web-flow`. Whether these three pushes were made with the Sync fork button or with a command is UNVERIFIED (this endpoint shows the same row for both). The push of 2026-11-26 started six push-triggered workflows of the fork and the push of 2026-10-28 started five (see the producer search); no run is recorded for the push of 2026-10-27 (why is UNVERIFIED).
+
+### `refs/heads/aidev02`: 5 rows kept (events only, for the record)
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| 2026-11-26T14:16:06Z | refs/heads/aidev02 | pr_merge | clayphi | 5fa1a6608658947f5dbe56616fffa93f7802c90e | pr_merge (pull request 12, `merge_commit_sha` equal) |
+| 2026-11-08T04:22:13Z | refs/heads/aidev02 | pr_merge | ironbelly | 9cfecdd30b2a90c06e5178b1245cb31a97d11bac | pr_merge (pull request 11, equal) |
+| 2026-11-03T16:27:00Z | refs/heads/aidev02 | pr_merge | clayphi | 82a07da65a241945e8206a14f6aeb9354a797643 | pr_merge (pull request 9, equal) |
+| 2026-11-01T01:02:36Z | refs/heads/aidev02 | pr_merge | ironbelly | c3b42f5632438343dd5b67076259609044f28f3e | pr_merge (pull request 8, equal) |
+| 2026-10-30T20:52:16Z | refs/heads/aidev02 | branch_creation | clayphi | 1c6ac8c3c4d2c3dec2cb5966d225ca2a0e0471d3 | branch_creation (zero `before` SHA) |
+
+Counts by class: direct push by human 0, direct push by automation 0, sync 0, pr_merge 4, branch_creation 1. Only the filtered call was run for this branch; the branch was created on `2026-10-30`, inside the window, so the filter cannot hide rows.
+
+## Tag evidence
+
+- Number of `v*` refs: **1076**. Command: `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` printed one per-page count, `1076` (one page, because this endpoint returns every match at once); the sum of the per-page counts is 1076. The call without the `v` prefix (`.../git/matching-refs/tags/`) also gives 1076, so every tag of the fork starts with `v`. Of the 1076, 1071 are annotated (type `tag`) and 5 are lightweight (type `commit`).
+- Not plain `vX.Y.Z`: **648** (checked with the pattern `^refs/tags/v[0-9]+\.[0-9]+\.[0-9]+$`; plain tags: 428). All 648 have the form `vX.Y.Z-rc.N`.
+- The parent has 1126 `v*` refs (same command on `repos/stablyai/orca`). All 1076 fork tags exist in the parent with the same name, the same type and the same object SHA (0 differ); no `v*` tag exists only in the fork; 50 parent tags are not in the fork (31 are newer than `v1.4.245` by version order, up to `v1.4.278`; 19 are older and carry a special suffix, for example `.perf`, `.ghes` or an issue suffix).
+- Five newest `v*` tags of the fork by version order (`sort -V`), each compared with the parent's tag of the same name (type and SHA): `v1.4.241` (`01cf025e343d8d1a7a30a26082ccb34c67765b52`), `v1.4.242` (`0360ad49840ab10d6493aa6c26c7d066d641eb95`), `v1.4.243` (`9548f13248598270a8a80e7c571286c5a716aa93`), `v1.4.244` (`9096d705d84b8b8fd5d2d605ca2a27428cd74442`), `v1.4.245` (`7a5202ad17310bc22e1f03398a96a189a3b33f03`). All five are annotated tags and match the parent's tag object.
+- How tags arrive from the parent: no workflow in the fork imports them (no workflow fetches or pushes parent tags; every `git fetch` and every `REPO_URL` names the fork itself through `origin` or `github.repository`, and the only tag pushes are described in the producer search). The newest fork tag `v1.4.245` was made in the parent at `2026-10-30T04:58:28Z`, which is after the fork was created (`2026-10-27T13:51:17Z`), and the fork lacks all parent tags after it (the parent's `v1.4.246` is dated `2026-11-02T02:49:17Z`). So the tags were not all copied when the fork was created; they were most likely imported by a person once, on or after `2026-10-30` (the date of the newest imported tag; the branch `aidev02` was created at `2026-10-30T20:52:16Z`). Who imported them and with which command is UNVERIFIED, and later manual tag pushes are invisible to this audit. A tag import by a person creates new tags, which the tag ruleset (`deletion`, `non_fast_forward`, `update`) does not block; a force-import of a re-pointed parent tag would be refused. None of the 1076 differs today.
+- The activity endpoint shows no tag events, so tag writes are invisible to this audit (INV-009).
+
+## Producer search
+
+`gh api repos/IronbellyOrg/IronOrca/actions/runs --jq .total_count` prints **767**. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows` lists **67** workflow files; all 67 are `active` in `gh api --paginate repos/IronbellyOrg/$REPO/actions/workflows`. Repository Actions are `enabled` with `allowed_actions` `all`; the repository has `0` Actions secrets (environment secrets were not read: UNVERIFIED).
+
+How the files were read: every one of the 67 files was decoded (`gh api .../contents/.github/workflows/<name> --jq .content | base64 -d`, 13,922 lines in all). For every file the trigger block, the top-level and job-level `permissions`, every job `if` guard and every `needs` list were extracted with a YAML parser and read. The six search terms (`git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`) plus `git tag`, `refs/tags`, `gh release`, `gh api`, `-X`, `--method`, `DELETE`, `--cleanup-tag`, `deleteRef`, `createRef`, `updateRef`, `deleteRelease`, `createRelease`, `softprops`, `curl` with a write method and `git commit` were searched in every file and every matching line was read with its context. The 115,015-byte `release-cut.yml` was read around its guard (lines 40 to 56), its tag and push step (lines 596 to 640), its job and `needs` list and every tag or ref line. Not every one of the 13,922 lines was read one by one; a ref write built at run time from a variable could in principle escape the search (E-2), which is why each called script was also read. UNVERIFIED beyond that.
+
+Called scripts read (decoded, then searched for the same terms and read where they matched): `mobile/scripts/prepare-android-release.mjs`; all 25 non-test files under `config/scripts/release/` (they include `agent-state-rules/agent-state-rules-bundle.mjs` and `versioning/release-tag-patterns.mjs`, which were read for tag names, and `workflow-contracts/release-policy.mjs`); and all 43 files under `.github/scripts/` and `.github/actions/`. Scripts elsewhere in the tree that the test, benchmark and cache workflows call were not read (UNVERIFIED; those workflows have read-only permissions apart from the cache sweep). Terms found in them: `deleteRef` once (`config/scripts/release/workflow-contracts/release-policy.mjs`, a tag delete, resolved in the table below) and `DELETE` twice (an HTTP method on a storage lease in `.github/actions/cloud-sql-rollout-lease/storage-lease.mjs` that touches no ref, and a colour name in `.github/scripts/pr-test-loc-table.mjs`). None of `git push`, `git tag`, `push --delete`, `git/refs`, `release delete`, `--force`, `createRef`, `updateRef` appears in them.
+
+Overview of the guards. `release-cut.yml`: the write job `cut` carries `if: github.repository == 'stablyai/orca'` (comment in the file: fork schedules must not diverge their main), so it never runs in the fork, and the 19 other jobs of that file all have `cut` in `needs` (parsed), so none starts. Other jobs with the same guard: the jobs of `adhoc-mac-build.yml`, `daily-mac-build.yml`, `hourly-mac-build.yml`, `dev-channel-win-build.yml`, `dev-channel-win-publish.yml`, `release-mac-build.yml`, `release-policy.yml`, `readme-downloads-badge.yml`, `bot-app-catalog-smoke.yml` and the production job of `docs.yml`. Scheduled workflows that do run in the fork (with recorded runs): `ci-branch-cache-sweep.yml` (`actions: write`; deletes idle branch caches through the cache API, no ref), `ci-cache-warmup.yml`, `ci-runner-demand.yml`, `ci-xterm-cache.yml`, `computer-e2e.yml`, `computer-macos-native.yml`, `e2e.yml`, `node-next-compat.yml`, `node-server-tests.yml` and `performance-contracts.yml`; all of them have read-only permissions apart from the cache sweep. `orca-server-artifact.yml` has a schedule but no run is recorded for it (why is UNVERIFIED). The runs list also holds runs of workflow paths that are no longer in the tree (`wsl-orcad-e2e.yml`, `wsl-orcad-e2e-frozen-runner-retry.yml`, `terminal-perf.yml`, `terminal-ime-e2e.yml`, `packaged-browser-e2e.yml`); their files are not in `main` today and could not be read (UNVERIFIED).
+
+`on: push` check (the scratch self-test of the runbook pushes a throwaway branch `zz-ruleset-selftest`): **no workflow has an unfiltered `on: push` trigger**, so none would start on that branch. The workflows with a push trigger are all filtered: `main` only (`ci-cache-warmup.yml`, `ci-cache-warmup-platforms.yml`, `ci-xterm-cache.yml`, `cloud-verify.yml`, `main-blocking-work.yml`, `mobile.yml`), the branch `Jinwoo-H/windows-update-survival` (`win-update-e2e.yml`, `win-update-survival-e2e.yml`) or the tags `android-v*` and `mobile-ios-v*` (`mobile-android-release.yml`, `mobile-ios-release.yml`). A `pull_request` trigger would start only with a pull request, which the self-test does not open. The `main`-filtered workflows did start on the sync pushes of `main` (11 push runs recorded, all on `main`: 6 on 2026-11-26 and 5 on 2026-10-28).
+
+| Place | Triggers | `on: push` | Hit and how resolved | Runs recorded in the fork (event:conclusion) |
+|---|---|---|---|---|
+| `adhoc-mac-build.yml` | workflow_dispatch | no push trigger | `gh release delete ... --repo "$ADHOC_REPO" --yes` and `--cleanup-tag` (lines 595, 634): `ADHOC_REPO` is `stablyai/orca-adhoc`, a different repository. Resolved: not this repository; the resolve job and the build jobs carry the `stablyai/orca` guard. `git/matching-refs/tags/v` (line 162) is a GET. | no run recorded |
+| `agent-state-rules-publish.yml` | workflow_dispatch | no push trigger | No term in the workflow; its script `config/scripts/release/agent-state-rules/agent-state-rules-bundle.mjs` (read) runs `gh release create <tag> ... --target` or `gh release upload --clobber`. The tag has the form `agent-state-rules-engine-<N>-next` or `-stable` (regex in `release-tag-patterns.mjs`, read), never `v*`. Resolved: `workflow_dispatch` by a person, no repository guard; creates a prerelease tag outside `refs/tags/v*`. `contents: write`. | no run recorded |
+| `bot-app-catalog-smoke.yml` | schedule, workflow_dispatch (cron 23 13 * * 1) | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `ci-branch-cache-sweep.yml` | schedule, workflow_dispatch (cron 23 */3 * * *) | no push trigger | none of the six terms; no tag or ref write found | schedule:success x85 |
+| `ci-cache-warmup-platform-jobs.yml` | workflow_call | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `ci-cache-warmup-platforms.yml` | pull_request, push | filtered: branches ["main"], plus a paths filter | none of the six terms; no tag or ref write found | push:cancelled x1; push:n/a x1 |
+| `ci-cache-warmup.yml` | pull_request, push, schedule, workflow_dispatch (cron 41 */6 * * *) | filtered: branches ["main"], plus a paths filter | none of the six terms; no tag or ref write found | push:cancelled x1; push:n/a x1; schedule:cancelled x52; schedule:failure x14 |
+| `ci-closed-pr-caches.yml` | pull_request_target | no push trigger | none of the six terms; no tag or ref write found | pull_request_target:success x6 |
+| `ci-runner-demand.yml` | schedule, workflow_dispatch (cron 23 4 * * *) | no push trigger | none of the six terms; no tag or ref write found | schedule:failure x1; schedule:success x29 |
+| `ci-xterm-cache.yml` | push, schedule, workflow_dispatch (cron 17 5 * * *) | filtered: branches ["main"], plus a paths filter | none of the six terms; no tag or ref write found | push:cancelled x1; push:n/a x1; schedule:cancelled x29; schedule:failure x1 |
+| `cloud-verify.yml` | pull_request, push | filtered: branches ["main"], plus a paths filter | none of the six terms; no tag or ref write found | push:success x2 |
+| `computer-e2e.yml` | pull_request, schedule, workflow_dispatch (cron 0 6 * * *) | no push trigger | none of the six terms; no tag or ref write found | pull_request:success x3; schedule:failure x1; schedule:success x28 |
+| `computer-macos-native.yml` | pull_request, schedule, workflow_dispatch (cron 0 6 * * *) | no push trigger | none of the six terms; no tag or ref write found | schedule:failure x12; schedule:success x17 |
+| `computer-task-benchmark.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `daily-mac-build.yml` | schedule, workflow_dispatch (cron 15 18 * * *) | no push trigger | `gh release delete ... --repo "$DAILY_REPO"` with `--cleanup-tag` (lines 405, 440): `DAILY_REPO` is `stablyai/orca-daily`. Resolved: different repository; jobs `resolve-main` and `build-daily-mac` carry the guard (29 scheduled runs, all skipped). | schedule:skipped x29 |
+| `dependency-security.yml` | pull_request, workflow_call, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `dev-channel-win-build.yml` | workflow_call, workflow_dispatch | no push trigger | No term; `gh release view` on `stablyai/orca-<channel>` and a fetch of refs into a scratch clone (reads). Resolved: reads only; the job carries the guard. | no run recorded |
+| `dev-channel-win-publish.yml` | workflow_call | no push trigger | No term; `gh release upload --clobber --repo stablyai/orca-<channel>` (another repository). Resolved: not this repository; the job carries the guard. | no run recorded |
+| `docs.yml` | pull_request, release, workflow_dispatch | no push trigger | No term; `gh api repos/$GITHUB_REPOSITORY/git/ref/tags/$tag` and `git/tags/...` are GET reads (lines 149, 162). Resolved by reading them. The production job carries the `stablyai/orca` guard (line 78). | no run recorded |
+| `e2e.yml` | schedule, workflow_call, workflow_dispatch (cron 0 17 * * *) | no push trigger | none of the six terms; no tag or ref write found | schedule:cancelled x27; schedule:failure x1; schedule:n/a x1 |
+| `golden-e2e-experiment.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `homebrew-bump.yml` | workflow_call, workflow_dispatch | no push trigger | `git push -u origin "$branch" --force` (line 163): force-pushes a bump branch in the tap repository of the parent (checkout of another repository with a GitHub App token whose key is an Actions secret; the fork has 0 secrets). Resolved: it never writes to this repository, and has no `v*` tag. Called only by `release-cut.yml` or by hand. | no run recorded |
+| `hourly-mac-build.yml` | schedule, workflow_dispatch (cron 0 * * * *) | no push trigger | `gh release delete ... --repo "$HOURLY_REPO"` with `--cleanup-tag` (lines 367, 402): `HOURLY_REPO` is `stablyai/orca-hourly`. Resolved: different repository; job `preflight` carries the guard and the build jobs need it (106 scheduled runs, all skipped). | schedule:skipped x106 |
+| `issue-os-labeler.yaml` | issues | no push trigger | none of the six terms; no tag or ref write found | issues:success x2 |
+| `journal-file-lock.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `layout-owner-e2e.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `linux-wayland-gpu-sandbox.yml` | workflow_dispatch | no push trigger | `--force` in `git checkout --force "$GITHUB_SHA"` (line 80). Resolved: a local checkout, no ref write. | no run recorded |
+| `main-blocking-work.yml` | push, workflow_dispatch | filtered: branches ["main"] | none of the six terms; no tag or ref write found | push:success x1 |
+| `mobile-android-release.yml` | push, workflow_dispatch | filtered: tags ["android-v*"] | `git push origin "refs/tags/$tag"` (line 266): creates the tag `android-v<version>` only when it does not exist and the run was not started by an `android-v*` tag. Resolved: creation only, the name never matches `refs/tags/v*`; also `gh api .../generate-notes -X POST` (notes text, no ref write). The tag name comes from `mobile/scripts/prepare-android-release.mjs` (`android-v${currentVersion}`, read). The build needs signing secrets the fork does not have. | no run recorded |
+| `mobile-ios-release.yml` | push, workflow_dispatch | filtered: tags ["mobile-ios-v*"] | none of the six terms; no tag or ref write found | no run recorded |
+| `mobile-native-fingerprint.yml` | pull_request | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `mobile.yml` | pull_request, push | filtered: branches ["main"], plus a paths filter | none of the six terms; no tag or ref write found | pull_request:success x4; push:success x2 |
+| `node-next-compat.yml` | schedule, workflow_dispatch (cron 0 10 * * *) | no push trigger | none of the six terms; no tag or ref write found | schedule:cancelled x1; schedule:failure x2; schedule:success x26 |
+| `node-server-tests.yml` | pull_request, schedule, workflow_call, workflow_dispatch (cron 30 11 * * *) | no push trigger | `--force` in `docker rm --force orcad-alpine` (line 601). Resolved: a container, no ref write. | pull_request:success x6; schedule:failure x15; schedule:success x14 |
+| `orca-server-artifact.yml` | pull_request, schedule, workflow_call, workflow_dispatch (cron 45 11 * * *) | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `performance-contracts.yml` | pull_request, schedule, workflow_dispatch (cron 15 9 * * *) | no push trigger | none of the six terms; no tag or ref write found | schedule:cancelled x27; schedule:failure x1; schedule:n/a x1 |
+| `pi-owner-runtime.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `pi-provider-runtime.yml` | pull_request | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `pr-description.yml` | pull_request | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `pr-test-loc.yml` | pull_request | no push trigger | none of the six terms; no tag or ref write found | pull_request:success x6 |
+| `pr.yml` | pull_request | no push trigger | none of the six terms; no tag or ref write found | pull_request:failure x3; pull_request:success x3 |
+| `preflight-benchmark.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `preflight-critical-path-benchmark.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `pullfrog.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `qualified-orcad-template.yml` | workflow_call | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `readme-downloads-badge.yml` | release, schedule, workflow_dispatch (cron 17 */6 * * *) | no push trigger | `git push --force-with-lease` (line 65): pushes the branch `automation/readme-downloads-badge`. Resolved: no tag; the only job carries `if: github.repository == 'stablyai/orca'`, so it never runs in the fork (69 runs, all skipped). | schedule:skipped x69 |
+| `release-cut.yml` | workflow_dispatch | no push trigger | `git push origin "HEAD:refs/heads/main"` (line 624) and `git push origin "$TAG"` (line 634); `git tag -a "v$VERSION"` (line 611). Resolved by reading: the push job is `cut` with `if: github.repository == 'stablyai/orca'` and `contents: write` (guard at line 49, comment: fork schedules must not diverge their main); the other 19 jobs all list `cut` in `needs` (checked by parsing the file), so none starts in the fork. Only tag creation, no delete, no force. Not found: `git tag -d`, `push --delete`, `git/refs`. | no run recorded |
+| `release-javascript-benchmark.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `release-javascript.yml` | workflow_call | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `release-mac-build.yml` | workflow_dispatch | no push trigger | `gh release upload ... --repo "$GITHUB_REPOSITORY" --clobber` (line 261): replaces release assets, no tag write. Resolved: `workflow_dispatch` only; its `build-mac` job carries the `stablyai/orca` guard. | no run recorded |
+| `release-mirror-r2.yml` | workflow_call, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `release-policy.yml` | release | no push trigger | No term in the workflow itself, but the script it loads (`config/scripts/release/workflow-contracts/release-policy.mjs`) calls `github.rest.git.deleteRef` with `tags/<tag>` to remove a tag of an unauthorized release. **This is the only tag deleter found.** Resolved: trigger `release` (published, edited); the single job `enforce` carries `if: github.repository == 'stablyai/orca'`, so it never runs in the fork. | no run recorded |
+| `unit-module-cache-benchmark.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `unit-module-cache.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `unit-plan.yml` | workflow_call | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `unit-selection-evidence.yml` | workflow_call | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `unit-tests.yml` | workflow_call | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `win-crash-survival-e2e.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `win-orcad-serve-switch-e2e.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `win-update-e2e.yml` | push, workflow_dispatch | filtered: branches ["Jinwoo-H/windows-update-survival"], plus a paths filter | none of the six terms; no tag or ref write found | no run recorded |
+| `win-update-survival-e2e.yml` | push, workflow_dispatch | filtered: branches ["Jinwoo-H/windows-update-survival"], plus a paths filter | none of the six terms; no tag or ref write found | no run recorded |
+| `windows-native-preparation-benchmark.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `windows-signing-rehearsal.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `windows-typecheck-parity.yml` | pull_request, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `windows-wsl-e2e.yml` | workflow_call, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `zcode-account-contract.yml` | workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| `zcode-credential-contract.yml` | pull_request, workflow_call, workflow_dispatch | no push trigger | none of the six terms; no tag or ref write found | no run recorded |
+| Code search `gh api -X GET search/code -f q='IronOrca org:IronbellyOrg'` | not applicable | not applicable | `total_count` 174; 168 items returned over every page; hits in public repositories: **0**; hits in private repositories: 168, each **a hit in a private IronbellyOrg repository (details in `.dev/issues/837/private/IronOrca-code-search.md`)**. Each hit file was read through a filter for write-capable calls and for lines naming this repository. None is a mechanism that holds a release token for this repository, writes a ref of it, or moves or deletes its tags (conclusion only; nothing else about the hits is kept in this file). Code search cannot see Actions secrets of other repositories, so a token kept as a secret there is UNVERIFIED. | not applicable |
+| Tag import path (how tags arrive from the parent) | not applicable | not applicable | The fork's 1076 `v*` tags equal the parent's tags of the same name; no workflow imports them; the newest was made in the parent after the fork was created; the import was most likely done by a person (see Tag evidence). Who and how is UNVERIFIED. | not applicable |
+
+Producer search verdict for the tag ruleset (`refs/tags/v*`, rules `deletion`, `non_fast_forward`, `update`): **CLEAR**. The only tag deleter found (`release-policy.yml`, through `deleteRef`) and the only tag creators (`release-cut.yml`, `mobile-android-release.yml`, `agent-state-rules-publish.yml`) are either skipped in the fork by the `stablyai/orca` guard or create tags whose names do not match `v*` (`android-v*`, `agent-state-rules-engine-*`); nothing moves or deletes a `v*` tag in the fork; the tag creation in `release-cut.yml` (`v*`) never runs here and would not be blocked by this ruleset anyway. Remaining UNVERIFIED items: who imported the tags, line-by-line content of workflows beyond the searched terms, workflow files of the removed paths listed above, environment secrets, and any secret held by another repository. This verdict does not clear the installations read; see Blocks.
+
+## Blocks
+
+| Ruleset | Missing check or event | Who clears it | What clears it |
+|---|---|---|---|
+| `protect-main` (full role) or `protect-main-mirror` (mirror role) (branch, `refs/heads/main`) | `gh api --paginate orgs/IronbellyOrg/installations` could not run (needs the `admin:org` scope; `clayphi`'s token lacks it) | An organisation owner of IronbellyOrg, or Clay in writing | An organisation owner runs the read and records its output here, or Clay's written acceptance of the missing read is quoted from `.dev/issues/837/issue-summary.md` (no such acceptance is recorded there today) |
+| `protect-main-mirror` (mirror role) | G4: Clay's written acceptance of the mirror's direct-push exposure | Clay | Clay's acceptance quoted word for word in `.dev/issues/837/issue-summary.md`; without it the fork's branch ruleset is skipped and reported (no acceptance is recorded today) |
+| `protect-release-tags` (tag, `refs/tags/v*`) | The same installations read (the producer search itself is `CLEAR`) | An organisation owner of IronbellyOrg, or Clay in writing | As in the first row |
+| `protect-aidev02` (branch, `refs/heads/aidev02`; the file is not created) | Clay's written yes for protecting `aidev02` | Clay | Clay's written yes quoted word for word in `.dev/issues/837/issue-summary.md` (none is recorded); until then the file `.github/rulesets/other-repos/protect-aidev02.json` is not created and no ruleset is applied to `aidev02` |
+
+## Result
+
+**BLOCKED.**
+
+Reasons:
+1. The installations read could not run (HTTP 404, `admin:org` scope missing), and it is not recorded as clean. It is cleared by an organisation owner of IronbellyOrg, or by Clay's written acceptance quoted from `.dev/issues/837/issue-summary.md`; nothing there records that acceptance today.
+2. For the mirror role only: Clay's written acceptance of the direct-push exposure (G4) is not recorded. The fork test (`ahead_by` 0) implies the mirror role today.
+
+Branch ruleset result: BLOCKED (reasons 1 and 2). Tag ruleset result: producer search `CLEAR`, overall BLOCKED by reason 1 only. `aidev02`: no ruleset without Clay's written yes.
+
+For the record, the other checks are clean: `hooks` 0, `keys` 0, no classic branch protection, no existing ruleset, 0 direct pushes by a human or by automation on `main` in 90 days (3 `sync` pushes, no `pr_merge`), `ahead_by` 0, and 4 `pr_merge` plus 1 `branch_creation` and no direct push on `aidev02`. One thing to know before apply day: the fork's `main` is moved by single parent-commit pushes (last on `2026-11-26T15:42:31Z`); under the full role (`pull_request` rule) a plain push of that kind would be expected to be refused (UNVERIFIED, not tested), and whether the Sync fork button is refused under a `pull_request` rule is UNVERIFIED.
+
+## Revert commands
+
+Written before any write on this repository. The id column is empty until apply. A branch ruleset is created from one of two files (full or mirror, chosen on apply day), so each has a line; the tag ruleset has one line; the `aidev02` ruleset is not created without Clay's written yes.
+
+| Ruleset | Revert command | Id |
+|---|---|---|
+| `protect-main` (full role) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronOrca` | |
+| `protect-main-mirror` (mirror role) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronOrca` | |
+| `protect-release-tags` | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronOrca` | |
+| `protect-aidev02` | not created without Clay's written yes; if it is ever created: `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronOrca` | |
+
+## Self-test of the record
+
+UNVERIFIED and not run in Phase 1: whether `clayphi`'s token can create rulesets on this repository, whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, and whether the Sync fork button is refused under a `pull_request` rule.
+
+## Commands run
+
+All are read-only calls (none is POST, PUT, PATCH or DELETE; the only method flag is `-X GET`). `REPO=IronOrca`, `PARENT_OWNER=stablyai`; `END` and `START` as in the header. Workflow, script and code-search hit files were decoded or saved into private temporary directories under `/tmp` and searched there.
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
+10. `gh api repos/IronbellyOrg/$REPO/actions/secrets --jq .total_count`
+11. `gh api repos/IronbellyOrg/$REPO --jq '[.created_at,.pushed_at,.updated_at] | @tsv'`
+12. `gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by,.behind_by,.status] | @tsv'`; `gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...aidev02" --jq '[.ahead_by,.behind_by,.status] | @tsv'`; `gh api "repos/IronbellyOrg/$REPO/compare/main...aidev02" --jq '[.ahead_by,.behind_by,.status] | @tsv'`
+13. `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha`; the same for `aidev02`; `gh api repos/$PARENT_OWNER/orca/git/ref/heads/main --jq .object.sha`
+14. `gh api --paginate repos/IronbellyOrg/$REPO/branches --jq '.[].name'`
+15. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`; the same URL with `--jq '.[] | [.timestamp,.activity_type,.actor.login] | @tsv'` (unfiltered cross-check, 3 rows)
+16. The same call as 15 for `ref=refs/heads/aidev02` (filtered)
+17. `gh api repos/$PARENT_OWNER/orca/commits/<sha> --jq '[.sha,.commit.committer.date,(.commit.message|split("\n")[0])] | @tsv'`, `gh api "repos/$PARENT_OWNER/orca/compare/main...<sha>" --jq '[.status,.ahead_by,.behind_by] | @tsv'` and `gh api repos/IronbellyOrg/$REPO/commits/<sha> --jq '[.commit.committer.date,.committer.login,(.parents|length),(.commit.message|split("\n")[0])] | @tsv'` for the three `after` SHAs of the `main` rows and for the oldest `before` SHA; `gh api users/ironbelly --jq '[.login,.type,.name] | @tsv'`
+18. `gh api "repos/IronbellyOrg/$REPO/pulls?state=closed&base=aidev02&per_page=10" --jq '.[] | [.number,.merged_at,.user.login] | @tsv'` and with `select(.merged_at!=null)` printing `merge_commit_sha`
+19. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`, with `--jq '.[] | [.ref,.object.type,.object.sha] | @tsv'`, and the same without the `v` prefix (`--jq length`)
+20. `gh api --paginate repos/$PARENT_OWNER/orca/git/matching-refs/tags/v --jq '.[] | [.ref,.object.type,.object.sha] | @tsv'`
+21. `gh api repos/$PARENT_OWNER/orca/git/tags/<sha> --jq .tagger.date` for the parent's `v1.4.245` and `v1.4.246`
+22. `gh api repos/IronbellyOrg/$REPO/releases --jq length`
+23. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows --jq '.[] | [.name,.size,.type] | @tsv'`
+24. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows/<name> --jq .content | base64 -d` for each of the 67 workflow files
+25. `gh api repos/IronbellyOrg/$REPO/actions/runs --jq .total_count`; `gh api --paginate "repos/IronbellyOrg/$REPO/actions/runs?per_page=100" --jq '.workflow_runs[] | [.path,.event,.conclusion,.head_branch,.created_at] | @tsv'`; `gh api repos/IronbellyOrg/$REPO/actions/workflows` (first page and with `--paginate`, `--jq '.workflows[] | [.path,.state] | @tsv'`); `gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled,.allowed_actions] | @tsv'`
+26. `gh api "repos/IronbellyOrg/$REPO/git/trees/main?recursive=1" --jq ...` (paths only), then `gh api repos/IronbellyOrg/$REPO/contents/<path> --jq .content | base64 -d` for `mobile/scripts/prepare-android-release.mjs`, `config/scripts/release/agent-state-rules/agent-state-rules-bundle.mjs`, `config/scripts/release/versioning/release-tag-patterns.mjs`, the 25 non-test files under `config/scripts/release/` and the 43 files under `.github/scripts/` and `.github/actions/`
+27. `gh api -X GET search/code -f q='IronOrca org:IronbellyOrg' --jq '[.total_count, (.items|length)] | @tsv'`; the same call with `--paginate -f per_page=100 --jq '.items[] | [.repository.full_name,.repository.private,.path] | @tsv'` (output not recorded in this file); `gh api -H 'Accept: application/vnd.github.raw+json' repos/<hit repository>/contents/<hit path>` for each of the 168 hits (output not recorded in this file)
+28. Local only: `grep`, `sed -n`, `cat`, `sort`, `comm`, `join`, `awk`, `wc` over the decoded files; a local YAML parse of the 67 workflows (`uv run --with pyyaml python -I`); `cat` of `.github/rulesets/protect-release-tags.json`; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/IronOrca.md`.


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
