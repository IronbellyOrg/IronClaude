73e7222bf868cf6e768960ad55d3fc6ceef0380a
Review one task for spec compliance.

Task brief: ## Task 9: Write the audit record for irondots

Depends on: Task 8

Write `.dev/issues/837/audit/irondots.md` with the same structure as Task 8 and `REPO=irondots` (the fork test only if the repo has a parent). Record the events of `refs/heads/main` (the repo is young: note when `main` was created), and record the events of the branches matching `dot/*` only as an exclusion note (they are excluded from protection and must stay deletable). Record whether its gated-release workflow is present; if it is, read it and record whether it only creates tags (creating a tag stays allowed under the tag ruleset); if it is not present, record that.

Acceptance criteria:
- `.dev/issues/837/audit/irondots.md` exists with the read-only blocks, the section "Checks Ryan must run (admin only)", the `dot/*` exclusion note and a finding about tag-creating workflows that names the workflow file when one exists.
- Events for `main` are classified, with the repo's age stated; no write command is listed.
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
Start sha: 73e7222bf868cf6e768960ad55d3fc6ceef0380a
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/audit/irondots.md


diff --git a/.dev/issues/837/audit/irondots.md b/.dev/issues/837/audit/irondots.md
new file mode 100644
index 000000000..711d82251
--- /dev/null
+++ b/.dev/issues/837/audit/irondots.md
@@ -0,0 +1,182 @@
+# Audit record: IronbellyOrg/irondots
+
+Phase 1, read-only (issue 837, section 3.4 of the design). `REPO=irondots`, `BRANCH=main`. This is a handoff repo: `clayphi` has read access only, and Ryan applies anything that is applied. Only `gh api` GET calls were made. **Nothing was written to this repository** (no ruleset, branch, tag, comment or file). Never staged.
+
+## Header
+
+| Item | Value |
+|---|---|
+| `END` | `2026-11-26T16:29:23Z` (from `date -u +%Y-%m-%dT%H:%M:%SZ`) |
+| `START` | `2026-08-28T16:29:23Z` (from `date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ`) |
+| Audited ref | `refs/heads/main` |
+| Who runs the apply | Ryan (`ironbelly`), not Clay |
+
+## Preflight (read access only)
+
+| Check | Result |
+|---|---|
+| `gh api user --jq .login` | `clayphi` |
+| `gh api repos/IronbellyOrg/irondots --jq '[.fork,.parent.full_name,.default_branch,.archived,.private,.created_at] \| @tsv'` | `false`, (empty: no parent), `main`, `false`, `false`, `2026-11-01T23:04:07Z` (not a fork, default branch `main`, not archived, public) |
+| `permissions.admin`, `permissions.push`, `permissions.pull` | `false`, `false`, `true`: `clayphi` can read only, as Clay's recorded answer says. The admin preflight (G2) therefore cannot pass for `clayphi` and is Ryan's to run. |
+| `pushed_at`, `visibility` | `2026-11-26T14:29:19Z`, `public` |
+
+Age of the repository: it was created on 2026-11-01 (`created_at` `2026-11-01T23:04:07Z`), **24 days** before `END`. The 90-day window therefore starts 65 days before the repository existed, and the audit covers its whole life. `main` was created at `2026-11-01T23:04:09Z` (a `branch_creation` event, two seconds after the repository).
+
+## Counts
+
+Not run by Clay: `hooks`, `keys`, `branches/main/protection`, the organisation installations read and the Actions permissions read are admin-only here. They are listed with their commands in "Checks Ryan must run (admin only)". Nothing is recorded as clean for them.
+
+## Existing rulesets
+
+`gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` printed nothing (exit 0): no ruleset is visible to a read-only login. A ruleset in `disabled` or `evaluate` mode may be hidden from a login without admin (UNVERIFIED), so Ryan re-runs this list with admin (G7) before any create.
+
+## Fork test
+
+| Item | Result |
+|---|---|
+| Fork | **no: not a fork** (`.fork` is `false`, `.parent.full_name` is empty) |
+| Parent (`PARENT_OWNER`) | none |
+| `compare/$PARENT_OWNER:main...main` | not run: there is no parent, so there is nothing to compare |
+
+Role that results (G4): not a fork, so the mirror role does not apply (it is for a fork `main` that only fast-forwards from its parent). The role is the **full role**, `.github/rulesets/other-repos/protect-main.json` (name `protect-main`, target `refs/heads/main`). `protect-main-mirror.json` is not the candidate. Clay's written acceptance of the mirror (G4) is not recorded: `.dev/issues/837/issue-summary.md` has 0 lines that mention "mirror". Clay's recorded answer for this repository, word for word from `.dev/issues/837/issue-summary.md`: "IronHands-CLI, irondots and ironops-marketplace need Ryan (Clay's login has only read there): do not write to them; prepare what Ryan must apply and ask the lead to hand it to Ryan."
+
+## Tips
+
+| Branch | Command | SHA (40 characters) |
+|---|---|---|
+| `main` (audited) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha` | `90763e3f99808ce0299f3f0783469dc6ada84867` |
+
+The `main` tip equals the `after` SHA of its newest `main` event (a `pr_merge` by `ironbelly` on 2026-11-11). No other branch is audited.
+
+## Events kept
+
+Command: `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`. `time_period=quarter` was not used (its length is UNVERIFIED).
+
+Classification method: a `branch_creation` row is `branch_creation`; a `push` or `force_push` row by a person is `direct push by human`, by a bot or a known automation `direct push by automation`; a `pr_merge` row is `pr_merge`; a push that is a fast-forward of a parent's `main` is `sync` (not applicable: no parent).
+
+Rows kept in the window `START` to `END`: **3** (the filter dropped 0 rows; the endpoint returned the same 3 rows without the filter). All three are by `ironbelly`, whose account type is `User` (a person, not a bot).
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| 2026-11-01T23:04:09Z | `refs/heads/main` | `branch_creation` | `ironbelly` | `6fee10100caa28fe65abd9650f97665c0a657167` | branch_creation |
+| 2026-11-04T12:21:18Z | `refs/heads/main` | `pr_merge` | `ironbelly` | `988ae8b61523c9a47e3e896af45cee70c11c314c` | pr_merge |
+| 2026-11-11T22:08:07Z | `refs/heads/main` | `pr_merge` | `ironbelly` | `90763e3f99808ce0299f3f0783469dc6ada84867` | pr_merge |
+
+Counts by class in the window: direct push by human 0, direct push by automation 0, sync 0, pr_merge 2, branch_creation 1.
+
+Reading: every change to `main` after its creation arrived by a pull request merge; the `before` SHA of each row is the `after` SHA of the row before it (an unbroken chain), so no direct push or force push to `main` is hidden between the rows. The full role (`protect-main.json`: no deletion, no non-fast-forward, pull request required) matches how `main` is already used. Whether `ironbelly` bypasses the rulesets as an admin is by design (the files name the admin role as the bypass actor, in pull-request mode); how the merges were made (which pull request) is UNVERIFIED and was not read.
+
+## `dot/*` exclusion note
+
+The ruleset `protect-main.json` includes only `refs/heads/main` (checked in the local file), so branches named `dot/*` are not matched. They are listed here only as an exclusion: they must stay creatable, pushable and deletable, so no ruleset may be widened to match them.
+
+Branches (`gh api repos/IronbellyOrg/$REPO/branches --paginate --jq '.[].name'`): `main` and the three below. A fourth `dot/` branch was created and deleted (see the activity).
+
+| Branch | Present now | Activity (all by `ironbelly`) |
+|---|---|---|
+| `dot/skill-source-sync-20261102` | no (deleted) | created 2026-11-02T19:37:13Z; 5 pushes (19:44:06Z, 20:11:02Z, 20:12:32Z, 22:34:41Z on 2026-11-02, 21:08:28Z on 2026-11-03); deleted 2026-11-04T12:21:30Z, 12 seconds after the `pr_merge` on `main` at 12:21:18Z |
+| `dot/adversarial-debate-20261104` | yes | created 2026-11-04T22:22:56Z; no other event |
+| `dot/public-skill-sync-20261111` | yes | created 2026-11-11T22:06:00Z; no other event; the `pr_merge` on `main` at 22:08:07Z followed 2 minutes later |
+| `dot/session-init-ledger-sync-20261126` | yes | created 2026-11-26T14:29:19Z; no other event |
+
+How they behave: a person creates a `dot/` branch, pushes to it (plain pushes, no `force_push` event), merges it into `main` by pull request, and at least once deletes the branch right after the merge. Which branch each `pr_merge` came from is UNVERIFIED. The activity endpoint was queried without a `ref` filter for the year and returned 10 rows on `dot/` branches (listed above) plus the 3 rows on `main`; nothing else.
+
+## Tag evidence
+
+- Number of `v*` refs: **0**. Command: `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` printed one per-page count, `0` (one page); the sum of the per-page counts is 0.
+- The repository has **no tag of any name** (`git/matching-refs/tags --jq length` prints `0`), so the release workflow below has never created a tag here.
+- There is no parent, so the comparison of recent `v*` tags with a parent's tags has nothing to compare.
+- The activity endpoint shows no tag events, so tag writes are invisible to this audit (INV-009).
+- Consequence for the tag ruleset: `.github/rulesets/protect-release-tags.json` has rules `deletion`, `non_fast_forward` and `update` on `refs/tags/v*`, with no `creation` rule. It would match no tag today. The release workflow below names its tags `v<version>`, so it fits the pattern, and creating a new tag stays allowed.
+
+## Producer search
+
+Workflows listed with `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows` (2 files). Each was read (decoded into a private temporary directory under `/tmp`, searched there, then removed), then the scripts and tests they call were read: `scripts/package_release.py`, `scripts/validate_registry.py` and the three files in `tests/`, plus `README.md` and `docs/release-process.md` for how tags are made. Search terms applied to every file: `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`, plus `--delete`, `git tag`, `refs/tags`, `contents: write`, `gh release`, `gh api`, `DELETE`, `-X`, `--method`, `curl`, `subprocess`. A hit is resolved by reading it. Workflow state (`actions/workflows`): both `active`.
+
+Gated-release workflow: **present**, `.github/workflows/gated-release.yml` (97 lines, name "Gated draft release"; trigger `workflow_dispatch` only; top-level `permissions: contents: read`; the one job `draft` has `contents: write`; runs on `[self-hosted, small]`; guarded by repository name, `refs/heads/main`, the typed confirmation and an `expected_commit` equal to the checked-out commit).
+
+| Place | Hit | How resolved |
+|---|---|---|
+| `gated-release.yml`, step "Create draft only; never overwrite an existing release" | `git/refs` (a read of `git/matching-refs/tags/v<version>` and a read of `git/ref/tags/v<version>`, and one create call on `git/refs`); `gh release create`; `contents: write` | Read in full. The step first counts the tags matching `v<version>` and exits with an error if any exists ("Refuse pre-existing tags"). It then **creates** the tag `v<version>` at the reviewed commit by one create call to the `git/refs` endpoint (the workflow's own text; quoted here only as a search finding, and Clay ran no such call), reads the tag back and checks that it is bound to the commit, then runs `gh release create` with `--draft` and `--verify-tag`. It never updates, moves or deletes a tag, never uses `--force` or `--clobber`, and never pushes to a branch. The workflow's own header comment and `docs/release-process.md` say the same: it "does not overwrite existing tags or releases", and the tag "may remain" if draft creation fails, to be handled by a person, not by deleting it. **Finding: this workflow only creates tags.** Creating a tag stays allowed under the tag ruleset (it has no `creation` rule), subject to UNVERIFIED: whether the workflow's own token is treated like any other actor by a ruleset that has `update` and `deletion` rules (a new tag is neither). |
+| `gated-release.yml`, other steps | `--force`, `git push`, `git tag -d`, `push --delete`, `gh release delete` | No hit. The checkout step sets `persist-credentials: false`; the verify step runs the two scripts and the unit tests; the last step removes only its own temporary directory under `$RUNNER_TEMP`. |
+| `registry-validation.yml` (39 lines; `push` to `main` and `workflow_dispatch`; `contents: read`) | none for any term | Read in full. It checks out the commit, runs the validation script and the unit tests, and writes a step summary. It writes nothing to a ref. |
+| `scripts/package_release.py` (61 lines) | none for any term | Read in full. It builds a ZIP, a checksum file and a manifest in a new output folder; no git or API call, as `docs/release-process.md` says. |
+| `scripts/validate_registry.py` (179 lines) | `urllib.parse` import; `visiting.remove(name)` | Read the hits: `urllib.parse` only splits URLs; `remove` removes a name from an in-memory set. No git, API or network call. |
+| `tests/` (3 files) | `subprocess` in `test_public_package_suites.py` | Read. It runs `python -m unittest discover` over package test folders with a 90 second timeout; no git or API call. |
+| `README.md`, `docs/` (3 files) | `tag`, `push`, `delete`, `force`, `sync` (case-insensitive) | Read the hits. `docs/release-process.md` describes the gated workflow above; `docs/source-publication.md` has a dated "synchronization" heading about content, not refs; no instruction to move or delete a tag. |
+| Other IronbellyOrg repositories that hold a release token for this repository (E-2) | not searched here | UNVERIFIED. This task runs no code search across the organisation, so a release token held as a secret elsewhere is not excluded. |
+| How tags arrive from a parent | not applicable | The repository is not a fork. |
+
+Verdict for Clay's read-only workflow search: **no workflow or called script found that moves or deletes a `v*` tag, and none that deletes any tag.** The only tag writer is `gated-release.yml`, which creates a new `v<version>` tag at a reviewed commit and refuses an existing one. Remaining UNVERIFIED: any release token held in another repository; manual tag deletions or moves, which the audit cannot see (and with 0 tags none has happened that still shows).
+
+## Blocks
+
+| Ruleset | Missing check or event | Who clears it | What clears it |
+|---|---|---|---|
+| `protect-main` (full role, branch `refs/heads/main`) | Admin-only checks not run by Clay: `hooks`, `keys`, `branches/main/protection`, the organisation installations read (needs `admin:org`), the Actions permissions read, Ryan's admin role | Ryan; an organisation owner for the installations read | Ryan runs the commands in "Checks Ryan must run (admin only)" and records the output; for the installations read, an organisation owner's output or Clay's written acceptance of the gap quoted from `.dev/issues/837/issue-summary.md` (none is recorded there today) |
+| `protect-main` | G1 Authority: the repository is a handoff repo; Clay's recorded answer is "do not write to them" | Ryan applies | Ryan's own apply from the handoff; Clay writes nothing |
+| `protect-main` | G7: the list of existing rulesets is empty only as seen by a read-only login | Ryan | Ryan re-runs the list with admin inside the hour before the first write |
+| `protect-release-tags` (tag, `refs/tags/v*`) | The same admin-only installations read; the pattern matches no tag today (0 `v*` refs). No tag mover found by the read-only search | Ryan, with Clay | Ryan's admin-only checks. Applying is harmless here (nothing to break, and the one tag writer only creates) |
+| `protect-main-mirror` | G4: not a fork, and no written acceptance of the mirror is recorded | Not applicable | Not the candidate role for this repository |
+
+## Result
+
+**BLOCKED for Clay; the apply belongs to Ryan.**
+
+Clay's read-only part found: the repository is a public repository that is not a fork, created 2026-11-01 (24 days old), default branch `main`, not archived; the role is the full role `protect-main.json`; 3 events on `main` in the window (1 `branch_creation`, 2 `pr_merge`; no direct push by a human or by automation and no `sync`); the `dot/*` branches are outside the ruleset's target and must stay deletable; no ruleset visible to a read-only login; no `v*` tag (no tag at all); and no workflow or script that moves or deletes a tag. Clay did not run, and cannot run, the admin-only checks, and Clay writes nothing to this repository. Ryan runs the admin-only checks, re-runs the audit inside the hour before the first write, and applies, from the handoff.
+
+Tag ruleset line: Clay's read-only workflow search found no producer that moves or deletes `v*` tags. The gated-release workflow `.github/workflows/gated-release.yml` only creates a tag, which stays allowed under the tag ruleset. Other IronbellyOrg repositories were not searched (UNVERIFIED).
+
+## Checks Ryan must run (admin only)
+
+None of these was run by Clay. Run them with Ryan's login (admin on the repository) and record the output here before the apply. Set `REPO=irondots`.
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
+gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled,.allowed_actions] | @tsv'
+```
+
+Expect: login `ironbelly` (Ryan); admin `true`, default branch `main`, not archived and public; both counts `0`; the `branches/main/protection` call answering HTTP 404 `Branch not protected`; an empty ruleset list (an existing ruleset stops the repo; nothing pre-existing is updated or deleted); and a review of every installed app with `contents: write` (an app that can push must use pull requests once the ruleset is on, because only the admin role bypasses). The installations call needs the `admin:org` scope; if it fails, write "could not run" with the error text, and the repository stays blocked until an organisation owner runs it or Clay accepts the gap in writing. The `actions/permissions` call is admin-only; Ryan also confirms there that the gated-release workflow's token is allowed to create a tag once the tag ruleset is on (UNVERIFIED).
+
+The two checks Ryan also repeats, which Clay ran read-only, so the apply day figures are fresh (R0). There is no parent, so there is no compare:
+
+```bash
+END=$(date -u +%Y-%m-%dT%H:%M:%SZ); START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)
+gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name] | @tsv'
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'
+```
+
+## Revert commands
+
+This record holds no write command. The revert commands for this repository are in Ryan's handoff (`.dev/issues/837/handoff-ryan.md`, Task 12) and in the guide section "Roll back and break glass".
+
+## Self-test of the record
+
+UNVERIFIED and not run: whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, whether the Sync fork button is refused under a `pull_request` rule (not applicable here: not a fork), whether a ruleset hidden from a read-only login exists, and whether the gated-release workflow's token can create a `v*` tag once a tag ruleset is on.
+
+## Commands run
+
+All are read-only calls made with `gh api` (default GET); none uses a method flag, and none is a write. `REPO=irondots`; `END` and `START` as in the header. Nothing was written to the repository. Workflow, script, test and document files were decoded into a private temporary directory under `/tmp`, searched there, and the directory was then removed.
+
+1. `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)`; `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`
+2. `gh api user --jq .login`
+3. `gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name,.default_branch,.archived,.private,.created_at] | @tsv'`
+4. `gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin,.permissions.push,.permissions.pull,.pushed_at,.visibility,.html_url] | @tsv'`
+5. `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` (empty)
+6. `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha`
+7. `gh api repos/IronbellyOrg/$REPO/branches --paginate --jq '.[].name'`
+8. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`; `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags --jq length`
+9. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows --jq '.[] | [.name,.path,.type,.size] | @tsv'`; `gh api repos/IronbellyOrg/$REPO/actions/workflows --jq '.workflows[]|[.path,.state]|@tsv'`
+10. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'` (3 rows); the same without the `select` and with `.actor.type` (3 rows, unfiltered cross-check)
+11. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?time_period=year&per_page=100" --jq '.[] | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'` (no ref filter; used for the `dot/*` note)
+12. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows/<name> --jq .content | base64 -d` for the 2 workflow files
+13. `gh api repos/IronbellyOrg/$REPO/contents --jq '.[] | [.name,.type] | @tsv'`; the same for `.github`, `scripts`, `tests` and `docs`
+14. `gh api repos/IronbellyOrg/$REPO/contents/<path> --jq .content | base64 -d` for `scripts/package_release.py`, `scripts/validate_registry.py`, the 3 files in `tests/`, `README.md` and the 3 files in `docs/`
+15. Local only: `grep`, `sed -n`, `cat`, `wc`, `sort`, `uniq`, `awk`, `base64 -d` over the decoded files; `ls` and `jq` over `.github/rulesets/other-repos/*.json` and `.github/rulesets/protect-release-tags.json`; `grep` over `.dev/issues/837/issue-summary.md`; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/irondots.md`.


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
