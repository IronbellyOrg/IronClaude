c53ff83d1d5a2d201db4eb392c4df07489bbb758
Review one task for spec compliance.

Task brief: ## Task 10: Write the audit record for ironops-marketplace

Depends on: Task 8

Write `.dev/issues/837/audit/ironops-marketplace.md` with the same structure as Task 8 and `REPO=ironops-marketplace`: read-only blocks, the fork test if it has a parent, the `v*` count over every page, the workflow search, and the section "Checks Ryan must run (admin only)".

Acceptance criteria:
- `.dev/issues/837/audit/ironops-marketplace.md` exists with the read-only blocks and the admin-only section, and states whether any `v*` tag or tag-moving workflow exists.
- No write command is listed.
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
Start sha: c53ff83d1d5a2d201db4eb392c4df07489bbb758
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/audit/ironops-marketplace.md


diff --git a/.dev/issues/837/audit/ironops-marketplace.md b/.dev/issues/837/audit/ironops-marketplace.md
new file mode 100644
index 000000000..6ce4bc81b
--- /dev/null
+++ b/.dev/issues/837/audit/ironops-marketplace.md
@@ -0,0 +1,156 @@
+# Audit record: IronbellyOrg/ironops-marketplace
+
+Phase 1, read-only (issue 837, section 3.4 of the design). `REPO=ironops-marketplace`, `BRANCH=main`. This is a handoff repo: `clayphi` has read access only, and Ryan applies anything that is applied. Only `gh api` GET calls were made. **Nothing was written to this repository** (no ruleset, branch, tag, comment or file). Never staged.
+
+## Header
+
+| Item | Value |
+|---|---|
+| `END` | `2026-11-26T16:32:41Z` (from `date -u +%Y-%m-%dT%H:%M:%SZ`) |
+| `START` | `2026-08-28T16:32:41Z` (from `date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ`) |
+| Audited ref | `refs/heads/main` |
+| Who runs the apply | Ryan (`ironbelly`), not Clay |
+
+## Preflight (read access only)
+
+| Check | Result |
+|---|---|
+| `gh api user --jq .login` | `clayphi` |
+| `gh api repos/IronbellyOrg/ironops-marketplace --jq '[.fork,.parent.full_name,.default_branch,.archived,.private,.created_at] \| @tsv'` | `false`, (empty: no parent), `main`, `false`, `false`, `2026-05-28T04:42:40Z` (not a fork, default branch `main`, not archived, public) |
+| `permissions.admin`, `permissions.push`, `permissions.pull` | `false`, `false`, `true`: `clayphi` can read only, as Clay's recorded answer says. The admin preflight (G2) therefore cannot pass for `clayphi` and is Ryan's to run. |
+| `pushed_at`, `visibility` | `2026-05-28T04:42:41Z`, `public` |
+
+Age of the repository: it was created on 2026-05-28 (`created_at` `2026-05-28T04:42:40Z`), **182 days** before `END`. The 90-day window therefore lies entirely inside the repository's life, but the repository has had no activity at all since its first second: `pushed_at` is one second after `created_at`, and `main` was created at `2026-05-28T04:42:41Z`.
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
+| `main` (audited) | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha` | `784a2e06ccadc22dd9a45b0d51a5914269fba2b8` |
+
+The `main` tip equals the `after` SHA of its only event (the `branch_creation`) and is the only commit in the repository (message "Initial commit", by `ironbelly`, 2026-05-28T04:42:41Z). `main` is the only branch (`gh api repos/IronbellyOrg/$REPO/branches --paginate --jq '.[].name'` printed `main`), so no other branch is audited.
+
+## Events kept
+
+Command: `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'`. `time_period=quarter` was not used (its length is UNVERIFIED).
+
+Classification method: a `branch_creation` row is `branch_creation`; a `push` or `force_push` row by a person is `direct push by human`, by a bot or a known automation `direct push by automation`; a `pr_merge` row is `pr_merge`; a push that is a fast-forward of a parent's `main` is `sync` (not applicable: no parent).
+
+Rows kept in the window `START` to `END`: **0 rows**. The filter dropped 1 row: the same endpoint without the filter returned exactly 1 row for `refs/heads/main`, the `branch_creation` of 2026-05-28T04:42:41Z by `ironbelly` (account type `User`), which is 182 days before `END` and 92 days before `START`. The endpoint without a `ref` filter also returned only that 1 row for the year.
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| (none in the window) | | | | | |
+
+Counts by class in the window: direct push by human 0, direct push by automation 0, sync 0, pr_merge 0, branch_creation 0.
+
+Reading: `main` has not changed since the repository was created, so no direct push, force push or pull request merge exists to be broken by the full role. The `activity` endpoint's retention is not documented here; with `time_period=year` it covers the whole life of this repository (182 days), so the single row is the complete history of `main` as far as the endpoint shows (UNVERIFIED beyond that). Whether `ironbelly` bypasses the rulesets as an admin is by design (the files name the admin role as the bypass actor, in pull-request mode).
+
+## Tag evidence
+
+- Number of `v*` refs: **0**. Command: `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` printed one per-page count, `0` (one page); the sum of the per-page counts is 0.
+- The repository has **no tag of any name** (`git/matching-refs/tags --jq length` prints `0`) and no release (`gh api repos/IronbellyOrg/$REPO/releases --jq length` prints `0`).
+- There is no parent, so the comparison of recent `v*` tags with a parent's tags has nothing to compare.
+- The activity endpoint shows no tag events, so tag writes are invisible to this audit (INV-009). Because the repository has no tag at all today, a tag that was created and then deleted without trace cannot be excluded (UNVERIFIED), but no tag exists that a ruleset could break.
+- Consequence for the tag ruleset: `.github/rulesets/protect-release-tags.json` has target `tag` on `refs/tags/v*`. It would match no tag today, so applying it breaks nothing here.
+
+## Producer search
+
+| Place | Hit | How resolved |
+|---|---|---|
+| Workflows of the repository: `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows` | HTTP 404 `Not Found` (exit 1): **could not run as a listing, because the folder does not exist** | The 404 is read as "no `.github/workflows` folder", not as clean by itself. It is confirmed three ways: the repository tree (`git/trees/main`, not truncated) holds exactly 1 entry, the blob `README.md`, so no `.github` folder exists on `main`; `gh api repos/IronbellyOrg/$REPO/actions/workflows --jq .total_count` prints `0`; and `actions/runs` reports `total_count` 0. There is no workflow file to read and no script a workflow could call. Only `main` exists as a branch, so no workflow is hiding on another branch. |
+| `README.md` (2 lines) | search terms `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`, plus `--delete`, `git tag`, `refs/tags`, `contents: write`, `gh release`, `gh api`, `DELETE`, `curl`, `tag`, `push`, `release`, `sync`: no hit (grep exit 1) | Read in full (decoded into a private temporary directory under `/tmp`, searched there, then removed). It says only that the repository is the "IronOps DevOps Claude plugin marketplace" of artifacts "built from IronbellyOrg/IronOps". No instruction about tags. The absence of a grep hit was not relied on: the file is two lines and was read. |
+| Other IronbellyOrg repositories that hold a release token for this repository (E-2) | the README names a source repository (`IronbellyOrg/IronOps`) whose artifacts are published here | UNVERIFIED and not searched. This task runs no code search across the organisation, and the named source repository was not read. Nothing has been published into this repository yet (the only event is its creation), so no publisher has acted. Note for Ryan: whichever token or app will later publish into `main` must be checked against the full role before the apply, because the pull request rule lets only the admin role bypass (see "Blocks"). |
+| How tags arrive from a parent | not applicable | The repository is not a fork. |
+
+Verdict for Clay's read-only workflow search: **no `v*` tag exists, and no workflow exists (no workflow folder, no registered workflow, no run), so no workflow moves or deletes a `v*` tag.** Remaining UNVERIFIED: a release token or a publisher held in another repository (the README points at one source repository, not read); manual tag deletions or moves, which the audit cannot see (and with 0 tags, none that still shows).
+
+## Blocks
+
+| Ruleset | Missing check or event | Who clears it | What clears it |
+|---|---|---|---|
+| `protect-main` (full role, branch `refs/heads/main`) | Admin-only checks not run by Clay: `hooks`, `keys`, `branches/main/protection`, the organisation installations read (needs `admin:org`), the Actions permissions read, Ryan's admin role | Ryan; an organisation owner for the installations read | Ryan runs the commands in "Checks Ryan must run (admin only)" and records the output; for the installations read, an organisation owner's output or Clay's written acceptance of the gap quoted from `.dev/issues/837/issue-summary.md` (none is recorded there today) |
+| `protect-main` | G1 Authority: the repository is a handoff repo; Clay's recorded answer is "do not write to them" | Ryan applies | Ryan's own apply from the handoff; Clay writes nothing |
+| `protect-main` | G7: the list of existing rulesets is empty only as seen by a read-only login | Ryan | Ryan re-runs the list with admin inside the hour before the first write |
+| `protect-main` | The publisher of the artifacts named in the README (UNVERIFIED which token or app pushes to `main`); no push has happened yet, so the audit cannot show it | Ryan | Ryan identifies the actor (the installations and keys reads) and confirms that it uses pull requests or is the admin role before the pull request rule is on |
+| `protect-release-tags` (tag, `refs/tags/v*`) | The same admin-only installations read. The pattern matches no tag today (0 `v*` refs, 0 tags) and no tag mover was found | Ryan, with Clay | Ryan's admin-only checks. Applying is harmless here: there is nothing to break |
+| `protect-main-mirror` | G4: not a fork, and no written acceptance of the mirror is recorded | Not applicable | Not the candidate role for this repository |
+
+## Result
+
+**BLOCKED for Clay; the apply belongs to Ryan.**
+
+Clay's read-only part found: the repository is a public repository that is not a fork, created 2026-05-28 (182 days old), default branch `main`, not archived; the role is the full role `protect-main.json`; **0 events** on `main` in the 90 days (the only event ever is its creation 182 days ago, so no direct push by a human or by automation, no `sync`, no `pr_merge`); `main` is one commit on one branch; no ruleset visible to a read-only login; no `v*` tag (no tag, no release); and no workflow of any kind (the workflow folder does not exist). Clay did not run, and cannot run, the admin-only checks, and Clay writes nothing to this repository. Ryan runs the admin-only checks, re-runs the audit inside the hour before the first write, and applies, from the handoff.
+
+Tag ruleset line: no `v*` tag exists and no tag-moving or tag-deleting workflow exists, so the tag ruleset is included here: there is nothing to break. Other IronbellyOrg repositories were not searched (UNVERIFIED).
+
+## Checks Ryan must run (admin only)
+
+None of these was run by Clay. Run them with Ryan's login (admin on the repository) and record the output here before the apply. Set `REPO=ironops-marketplace`.
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
+gh api repos/IronbellyOrg/$REPO/actions/permissions --jq '[.enabled,.allowed_actions] | @tsv'
+```
+
+Expect: login `ironbelly` (Ryan); admin `true`, default branch `main`, not archived and public; both counts `0`; the `branches/main/protection` call answering HTTP 404 `Branch not protected`; an empty ruleset list (an existing ruleset stops the repo; nothing pre-existing is updated or deleted); and a review of every installed app with `contents: write` (an app that can push must use pull requests once the ruleset is on, because only the admin role bypasses). The installations call needs the `admin:org` scope; if it fails, write "could not run" with the error text, and the repository stays blocked until an organisation owner runs it or Clay accepts the gap in writing. Ryan also identifies which token or app will publish the artifacts that the README says are built elsewhere and confirms that it can still publish once the pull request rule is on (UNVERIFIED today).
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
+This record holds no write command. The revert commands for this repository are in Ryan's handoff (`.dev/issues/837/handoff-ryan.md`, Task 12) and in the guide section "Roll back and break glass". Nothing was written to this repository, so there is nothing to revert today.
+
+## Self-test of the record
+
+UNVERIFIED and not run: whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, whether the Sync fork button is refused under a `pull_request` rule (not applicable here: not a fork), whether a ruleset hidden from a read-only login exists, whether `time_period=quarter` is 90 days (not used), and whether the activity endpoint would show a tag event (it does not, INV-009).
+
+## Commands run
+
+All are read-only calls made with `gh api` (default GET); none uses a method flag, and none is a write. `REPO=ironops-marketplace`; `END` and `START` as in the header. Nothing was written to the repository. The README was decoded into a private temporary directory under `/tmp`, searched there, and the directory was then removed.
+
+1. `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)`; `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`
+2. `gh api user --jq .login`
+3. `gh api repos/IronbellyOrg/$REPO --jq '[.fork,.parent.full_name,.default_branch,.archived,.private,.created_at] | @tsv'`
+4. `gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin,.permissions.push,.permissions.pull,.pushed_at,.visibility,.html_url] | @tsv'`
+5. `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` (empty)
+6. `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha`
+7. `gh api repos/IronbellyOrg/$REPO/branches --paginate --jq '.[].name'`
+8. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`; `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags --jq length`; `gh api repos/IronbellyOrg/$REPO/releases --jq length`
+9. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows --jq '.[] | [.name,.path,.type,.size] | @tsv'` (HTTP 404, could not list: the folder does not exist); `gh api repos/IronbellyOrg/$REPO/actions/workflows --jq '.workflows[]|[.path,.state]|@tsv'` (empty) and `--jq .total_count` (0); `gh api repos/IronbellyOrg/$REPO/actions/runs --jq .total_count` (0)
+10. `gh api repos/IronbellyOrg/$REPO/contents --jq '.[] | [.name,.type] | @tsv'` (`README.md`); `gh api "repos/IronbellyOrg/$REPO/git/trees/main?recursive=1" --jq '.tree[] | [.path,.type] | @tsv'` (1 entry); `gh api repos/IronbellyOrg/$REPO/git/trees/main --jq '[.truncated,(.tree|length)] | @tsv'` (`false`, 1); `gh api "repos/IronbellyOrg/$REPO/commits?per_page=100" --jq '.[] | [.sha,.commit.author.date,.author.login,.commit.message] | @tsv'` (1 commit)
+11. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.before,.after] | @tsv'` (no row); the same without the `select` and with `.actor.type` (1 row, unfiltered cross-check)
+12. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?time_period=year&per_page=100" --jq '.[] | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'` (no ref filter; 1 row)
+13. `gh api repos/IronbellyOrg/$REPO/contents/README.md --jq .content | base64 -d`
+14. Local only: `grep`, `cat`, `wc`, `base64 -d` over the decoded README; `ls` and `jq` over `.github/rulesets/other-repos/*.json` and `.github/rulesets/protect-release-tags.json`; `grep` over `.dev/issues/837/issue-summary.md`; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/ironops-marketplace.md`.


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
