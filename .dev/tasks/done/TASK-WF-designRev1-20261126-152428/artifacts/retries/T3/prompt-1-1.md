8441a5c96b07c29ffc1fb2e0fce87fe081660444
Review one task for spec compliance.

Task brief: ## Task 3: Add the "Other IronbellyOrg repos" section to docs/developer-guide/branch-protection.md

Depends on: Task 1, Task 2

In `docs/developer-guide/branch-protection.md` add one H2 titled `Other IronbellyOrg repos` between the existing `## Break glass` and `## Tests` sections, with the sub-sections of section 3.3 of `./source.md`: Targets, Variables, Role of a fork's `main`, Before applying, Apply, Check, Self-test, and Roll back and break glass. Write every command with the variables `REPO`, `BRANCH`, `PARENT_OWNER`, `ID`, `END` and `START`, never with a repo name inside a command. Take the commands from sections 3.4 and 3.6 of `./source.md`: preflight, hooks and keys counts, `branches/main/protection`, the existing ruleset list, the 90-day audit with `time_period=year` and a `START` filter, the fork test that prints `ahead_by` and `behind_by`, create-only-if-absent with tags first then non-default branches then `main`, the read-back of `rules/branches/$BRANCH` and `rulesets/$ID`, the scratch ruleset named `zz-selftest-<role>` on the branch `zz-ruleset-selftest`, and the DELETE and `enforcement=disabled` commands. The Targets table has one row per repo: CPA-Manager-Plus and IronOrca (applier Clay; forks; branch role "mirror when the fork test gives 0 and Clay's written acceptance is quoted, full when it gives more"; tag ruleset applied only if the producer search clears it; an Owner column holding the rule "switch to `protect-main.json` when `ahead_by` is above 0"), coder_orca (Clay; `protect-main`; tag ruleset skipped), IronHands-CLI (applier Ryan; a fork, so the same role rule and Owner column as the Clay forks; tag ruleset in Ryan's handoff, conditional), and irondots and ironops-marketplace (applier Ryan; `protect-main`; tag ruleset in Ryan's handoff, conditional), with the excluded branches `dev`, `release/v*` and `dot/*` and a note that `aidev02` is protected only on Clay's written yes, which names the path `.github/rulesets/other-repos/protect-aidev02.json`. Say in the section that the organisation installations command needs the `admin:org` scope. Edit one sentence of the existing `## Tests` paragraph so it also names the files in `.github/rulesets/other-repos/`. Keep every other existing section, heading and command unchanged.

Acceptance criteria:
- The heading `## Other IronbellyOrg repos` sits after `## Break glass` and before `## Tests`, and the guide still contains the literal strings that `test_guide_has_apply_and_check_commands` asserts: `gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input`, `rules/branches/master`, `enforcement=disabled`, and `.github/rulesets/protect-master.json`, `.github/rulesets/protect-integration.json`, `.github/rulesets/protect-release-tags.json`.
- The new section contains `$REPO`, `$BRANCH`, `admin:org`, `ahead_by`, `zz-selftest-`, the paths `.github/rulesets/other-repos/protect-main.json`, `.github/rulesets/other-repos/protect-main-mirror.json` and `.github/rulesets/other-repos/protect-aidev02.json`, and the names CPA-Manager-Plus, IronOrca, coder_orca, IronHands-CLI, irondots and ironops-marketplace.
- No command in the new section contains a literal repo name after `repos/IronbellyOrg/`; each uses `$REPO`.
- The pages that link to the guide keep working because no existing heading is renamed: `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59, `docs/developer-guide/documentation-index.md` lines 37 and 168, and `docs/developer-guide/release-procedure.md` lines 24 and 215 still point at `branch-protection.md`.
- The section holds no dated audit numbers (those live in `.dev/issues/837/audit/`) and no word about the internals of any private repository.
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
Start sha: 8441a5c96b07c29ffc1fb2e0fce87fe081660444
Diff against the start snapshot: Changed files (name-status):
M	docs/developer-guide/branch-protection.md


diff --git a/docs/developer-guide/branch-protection.md b/docs/developer-guide/branch-protection.md
index addb45f3f..85a032bc1 100644
--- a/docs/developer-guide/branch-protection.md
+++ b/docs/developer-guide/branch-protection.md
@@ -62,6 +62,127 @@ Then comment on the tracking issue (or an incident issue) with who, when and why
 
 To roll a ruleset back completely: `gh api --method DELETE repos/IronbellyOrg/IronClaude/rulesets/<id>`. Re-apply it from the JSON file.
 
+## Other IronbellyOrg repos
+
+Six more public IronbellyOrg repositories get the same kind of protection for their `main` branch. The files are kept in `.github/rulesets/other-repos/`; the release-tag ruleset is the existing `.github/rulesets/protect-release-tags.json`. Nothing here is applied from this page without the audit and the gates below: each repo gets its rulesets only after its own 90-day check of direct pushes. The dated audit results are not kept here; they live in the audit records and the pull request that added this section.
+
+| File | Role | Rules |
+|---|---|---|
+| `.github/rulesets/other-repos/protect-main.json` | full | `deletion`, `non_fast_forward`, `pull_request` (0 approvals) on `refs/heads/main` |
+| `.github/rulesets/other-repos/protect-main-mirror.json` | mirror | `deletion`, `non_fast_forward` on `refs/heads/main`; no pull request is required, so a fork can still fast-forward from its parent |
+| `.github/rulesets/other-repos/protect-aidev02.json` | full, one branch | the full role on `refs/heads/aidev02`; this file exists only on Clay's written yes for `aidev02` |
+
+Both `main` files keep the one bypass actor of the IronClaude rulesets (the Repository admin role in `pull_request` mode). Whether the API accepts that bypass actor on the mirror, which has no `pull_request` rule, is UNVERIFIED; the self-test below answers it before anything real is created.
+
+### Targets
+
+| Repo | Applier | Branch role | Tag ruleset | Excluded branches | Owner |
+|---|---|---|---|---|---|
+| CPA-Manager-Plus | Clay | a fork: `protect-main-mirror.json` when the fork test gives 0 and Clay's written acceptance is quoted, `protect-main.json` when it gives more | applied only if the producer search clears it | `dev`, `release/v*` | Clay; standing rule: switch to `protect-main.json` when `ahead_by` is above 0 |
+| IronOrca | Clay | a fork: the same role rule as above; `aidev02` is protected only on Clay's written yes (`.github/rulesets/other-repos/protect-aidev02.json`) | applied only if the producer search clears it | `dev`, `release/v*` | Clay; standing rule: switch to `protect-main.json` when `ahead_by` is above 0 |
+| coder_orca | Clay | `protect-main.json` | skipped | none | Clay |
+| IronHands-CLI | Ryan | a fork: the same role rule as the other forks | in Ryan's handoff, conditional | none | Ryan; standing rule: switch to `protect-main.json` when `ahead_by` is above 0 |
+| irondots | Ryan | `protect-main.json` | in Ryan's handoff, conditional | `dot/*` | Ryan |
+| ironops-marketplace | Ryan | `protect-main.json` | in Ryan's handoff, conditional | none | Ryan |
+
+The applier writes to a repo only when the repo's audit record is `CLEAR` and every gate in the gate ledger passes. Repos where Clay has only read access (IronHands-CLI, irondots, ironops-marketplace) are never written to by Clay: the applier there is Ryan.
+
+### Variables
+
+Every command below uses these variables and never a repo name:
+
+```bash
+REPO=<repo name, for example CPA-Manager-Plus>
+BRANCH=main
+PARENT_OWNER=<owner of the parent repo, forks only>
+ID=<ruleset id printed by the create call>
+END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
+START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)
+```
+
+### Role of a fork's main
+
+A fork's `main` receives fast-forwards from its parent, which a `pull_request` rule would block. Print how far the fork is ahead of the parent:
+
+```bash
+gh api repos/IronbellyOrg/$REPO --jq .parent.full_name
+gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by, .behind_by] | @tsv'
+```
+
+If `ahead_by` is 0 the fork carries no work of its own and the mirror role fits, but only with Clay's written acceptance of the mirror's direct-push exposure. If `ahead_by` is above 0 the fork holds its own commits and gets the full role. Whether the Sync fork button is refused under a `pull_request` rule is UNVERIFIED.
+
+### Before applying
+
+```bash
+gh api user --jq .login
+gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'
+gh api repos/IronbellyOrg/$REPO/hooks --jq length
+gh api repos/IronbellyOrg/$REPO/keys --jq length
+gh api repos/IronbellyOrg/$REPO/branches/main/protection
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id, .name, .enforcement] | @tsv'
+gh api --paginate orgs/IronbellyOrg/installations --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'
+```
+
+Expect the admin value `true`, default branch `main`, not archived and public; both counts `0`; the `branches/main/protection` call answering 404; and an empty ruleset list (an existing ruleset stops the repo, nothing pre-existing is updated or deleted). The installations command needs the `admin:org` scope: without it the command fails, and that failure is written down as "could not run" and blocks the repo until an organisation owner runs it or Clay accepts the gap in writing.
+
+The 90-day audit of direct pushes (`time_period=quarter` is not used because its length is UNVERIFIED):
+
+```bash
+gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp, .ref, .activity_type, .actor.login] | @tsv'
+```
+
+Classify every kept row as direct push by human, direct push by automation, sync (a parent fast-forward on a fork), pr_merge or branch_creation. The activity endpoint shows no tag events, so tag writes are invisible to it.
+
+Producer search for the tag ruleset: read every workflow of the repo (`gh api repos/IronbellyOrg/$REPO/contents/.github/workflows`, then each file and the scripts it calls) and search them for `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete` and `--force`; look for other IronbellyOrg repos that hold a release token for the repo; check how tags arrive from a parent. Resolve every hit by reading it: no grep output proves nothing, because names built at run time defeat grep. The tag ruleset is applied only when the search is `CLEAR`.
+
+### Apply
+
+Create only if the ruleset name is absent, in this order: the tag ruleset, then non-default branches (`aidev02`), then `main`. Run each create from a checkout at the pushed commit that holds the files:
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/protect-release-tags.json
+gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
+```
+
+For a fork in the mirror role use `.github/rulesets/other-repos/protect-main-mirror.json` in the last command. After a timeout list the rulesets again before any retry. On the first 403 stop that repo and record the partial state.
+
+### Check
+
+```bash
+gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'
+gh api repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+The first command prints `deletion`, `non_fast_forward` and `pull_request` for the full role, and `deletion` and `non_fast_forward` for the mirror. Compare the second with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset compare the rule types. A ruleset that fails the read-back is deleted by id (only a ruleset this rollout created) and the repo is reported as skipped.
+
+### Self-test
+
+Before the first real create, test the role on a throwaway branch of the target repo, from a scratch clone (never from IronClaude): create the branch `zz-ruleset-selftest` with two commits, create a scratch ruleset from the role file, check that a push is refused, then delete the ruleset and the branch.
+
+```bash
+jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' <file> | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
+git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
+gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'
+```
+
+The full role must refuse an empty commit pushed to the branch (error GH013); the mirror must refuse a force push of the earlier commit. The last command must show no name that starts with `zz-selftest-`. The answer of the scratch create also settles whether the mirror's bypass actor is accepted. If the API refuses it, drop the bypass actor from `protect-main-mirror.json` and change the file, the test and this page together before anything is applied.
+
+### Roll back and break glass
+
+The commands are the same as for IronClaude, with `$REPO` and `$ID`:
+
+```bash
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
+# push the fix
+gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
+gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
+```
+
+Comment on the tracking issue with who, when and why each time. Delete only rulesets that this rollout created.
+
 ## Tests
 
-`tests/docs/test_branch_protection_rulesets.py` pins the three JSON files (targets, rule types, zero approvals, bypass actor) and the commands on this page. Changing a ruleset means changing its JSON, this page and that test together, then applying the new JSON with `gh api --method PUT repos/IronbellyOrg/IronClaude/rulesets/<id> --input <file>`.
+`tests/docs/test_branch_protection_rulesets.py` pins the three JSON files and the files in `.github/rulesets/other-repos/` (targets, rule types, zero approvals, bypass actor) and the commands on this page. Changing a ruleset means changing its JSON, this page and that test together, then applying the new JSON with `gh api --method PUT repos/IronbellyOrg/IronClaude/rulesets/<id> --input <file>`.


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
