---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-designRev1-20261126-151358
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Branch protection rulesets for six more IronbellyOrg repos: files, guide, test, read-only audits, gate ledger, Ryan handoff, apply runbook and pull request body (issue 837), revision 1

Source: ./source.md
Goal: IronClaude holds the ruleset files, the guide section and the pinning test for the other IronbellyOrg repos, and the local working files (six read-only audit records, a gate ledger, a handoff text for Ryan, an apply runbook and a drafted pull request body) sit in `.dev/issues/837/`, so that the later steps (commit, push, pull request, gated apply) can run without further design. No ruleset is applied by this plan, and nothing that describes a private repository's internals reaches a file that is staged or posted.

## Constraints

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

## Phase 1: Ruleset files, guide section and pinning test

## Task 1: Create .github/rulesets/other-repos/protect-main.json

Create the new folder `.github/rulesets/other-repos/` and the file `protect-main.json` in it, as described in section 3.1 of `./source.md`: a copy of `.github/rulesets/protect-master.json` where `name` becomes `protect-main` and `conditions.ref_name.include` becomes `["refs/heads/main"]`. Nothing else changes: `target` stays `branch`, `enforcement` stays `active`, `exclude` stays `[]`, `bypass_actors` stays the repository admin role (`actor_id` 5, `actor_type` `RepositoryRole`, `bypass_mode` `pull_request`), the rules stay `deletion`, `non_fast_forward` and `pull_request` with the same five parameters and `required_approving_review_count` 0. Keep the formatting of `protect-master.json` (two-space indent, one-line `ref_name` and `bypass_actors`).

Acceptance criteria:
- `.github/rulesets/other-repos/protect-main.json` exists and `uv run python -c "import json,sys; json.load(open('.github/rulesets/other-repos/protect-main.json'))"` exits 0.
- A JSON comparison of `.github/rulesets/protect-master.json` and the new file shows exactly two differences: `name` and `conditions.ref_name.include`.
- `git status --short .github/rulesets` shows the new folder as untracked and no change to `protect-master.json`, `protect-integration.json` or `protect-release-tags.json`.
- The file contains no `~DEFAULT_BRANCH` token.

## Task 2: Create .github/rulesets/other-repos/protect-main-mirror.json

Depends on: Task 1

Create `.github/rulesets/other-repos/protect-main-mirror.json` as described in section 3.1 of `./source.md`: the content of `protect-main.json` with `name` changed to `protect-main-mirror` and the whole `pull_request` rule object removed, so the only rules are `deletion` and `non_fast_forward`. The bypass actor stays as in `protect-main.json` (decision D4: one shape everywhere). Whether the GitHub API accepts `bypass_mode: pull_request` on a ruleset without a `pull_request` rule is UNVERIFIED and is answered by the scratch self-test of the runbook (Task 13), not here.

Acceptance criteria:
- The file `.github/rulesets/other-repos/protect-main-mirror.json` exists, parses as JSON and has `name` equal to `protect-main-mirror`.
- Its rule types, sorted, are exactly `deletion` and `non_fast_forward`; `target`, `enforcement`, `conditions` and `bypass_actors` are identical to those of `protect-main.json`.
- A JSON comparison with `protect-main.json` shows exactly two differences: `name` and the missing `pull_request` rule.
- The file contains no `~DEFAULT_BRANCH` token.

## Task 3: Add the "Other IronbellyOrg repos" section to docs/developer-guide/branch-protection.md

Depends on: Task 1, Task 2

In `docs/developer-guide/branch-protection.md` add one H2 titled `Other IronbellyOrg repos` between the existing `## Break glass` and `## Tests` sections, with the sub-sections of section 3.3 of `./source.md`: Targets, Variables, Role of a fork's `main`, Before applying, Apply, Check, Self-test, and Roll back and break glass. Write every command with the variables `REPO`, `BRANCH`, `PARENT_OWNER`, `ID`, `END` and `START`, never with a repo name inside a command. Take the commands from sections 3.4 and 3.6 of `./source.md`: preflight, hooks and keys counts, `branches/main/protection`, the existing ruleset list, the 90-day audit with `time_period=year` and a `START` filter, the fork test that prints `ahead_by` and `behind_by`, create-only-if-absent with tags first then non-default branches then `main`, the read-back of `rules/branches/$BRANCH` and `rulesets/$ID`, the scratch ruleset named `zz-selftest-<role>` on the branch `zz-ruleset-selftest`, and the DELETE and `enforcement=disabled` commands. The Targets table has one row per repo: CPA-Manager-Plus and IronOrca (applier Clay; forks; branch role "mirror when the fork test gives 0 and Clay's written acceptance is quoted, full when it gives more"; tag ruleset applied only if the producer search clears it; an Owner column holding the rule "switch to `protect-main.json` when `ahead_by` is above 0"), coder_orca (Clay; `protect-main`; tag ruleset skipped), IronHands-CLI (applier Ryan; a fork, so the same role rule and Owner column as the Clay forks; tag ruleset in Ryan's handoff, conditional), and irondots and ironops-marketplace (applier Ryan; `protect-main`; tag ruleset in Ryan's handoff, conditional), with the excluded branches `dev`, `release/v*` and `dot/*` and a note that `aidev02` is protected only on Clay's written yes, which names the path `.github/rulesets/other-repos/protect-aidev02.json`. Say in the section that the organisation installations command needs the `admin:org` scope. Edit one sentence of the existing `## Tests` paragraph so it also names the files in `.github/rulesets/other-repos/`. Keep every other existing section, heading and command unchanged.

Acceptance criteria:
- The heading `## Other IronbellyOrg repos` sits after `## Break glass` and before `## Tests`, and the guide still contains the literal strings that `test_guide_has_apply_and_check_commands` asserts: `gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input`, `rules/branches/master`, `enforcement=disabled`, and `.github/rulesets/protect-master.json`, `.github/rulesets/protect-integration.json`, `.github/rulesets/protect-release-tags.json`.
- The new section contains `$REPO`, `$BRANCH`, `admin:org`, `ahead_by`, `zz-selftest-`, the paths `.github/rulesets/other-repos/protect-main.json`, `.github/rulesets/other-repos/protect-main-mirror.json` and `.github/rulesets/other-repos/protect-aidev02.json`, and the names CPA-Manager-Plus, IronOrca, coder_orca, IronHands-CLI, irondots and ironops-marketplace.
- No command in the new section contains a literal repo name after `repos/IronbellyOrg/`; each uses `$REPO`.
- The pages that link to the guide keep working because no existing heading is renamed: `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59, `docs/developer-guide/documentation-index.md` lines 37 and 168, and `docs/developer-guide/release-procedure.md` lines 24 and 215 still point at `branch-protection.md`.
- The section holds no dated audit numbers (those live in `.dev/issues/837/audit/`) and no word about the internals of any private repository.

## Task 4: Extend tests/docs/test_branch_protection_rulesets.py

Depends on: Task 1, Task 2, Task 3

Extend `tests/docs/test_branch_protection_rulesets.py` as in section 3.2 of `./source.md`. Keep every existing assertion and the existing `_load` (callers `test_branch_rulesets` at line 30 and `test_tag_ruleset` at line 47, both unchanged). Change `test_no_default_branch_token_anywhere` (the function starting at line 66) from `_RULESETS.glob("*.json")` to `_RULESETS.rglob("*.json")`. Add the constant `_OTHER` (`_RULESETS / "other-repos"`), a loader `_load_other(name)` that reads from it, and the constant `_TARGETS`: for each of the six repos its applier (`clay` or `ryan`), its candidate branch files (a fork lists both `protect-main` and `protect-main-mirror`, and IronHands-CLI is a fork as well as CPA-Manager-Plus and IronOrca; irondots, ironops-marketplace and coder_orca list `protect-main`; `protect-aidev02` is listed for IronOrca and marked optional) and its tag entry (`conditional`, `skip` or `handoff`). Add four tests with these names: `test_other_repos_full_role_derived` (`protect-main`, and `protect-aidev02` if the file exists, equal `protect-master` after replacing only `name` and `ref_name.include`, with rule types `deletion`, `non_fast_forward`, `pull_request`, the admin `pull_request` bypass actor and zero approvals), `test_other_repos_mirror_derived` (the mirror equals `protect-main` after replacing `name` and removing the `pull_request` rule, with rule types `deletion` and `non_fast_forward` and the same bypass), `test_other_repos_files_match_targets` (the set of `*.json` files in `other-repos/` equals the set named in `_TARGETS`; a file marked optional may be absent; a missing, unused or unlisted file fails) and `test_guide_has_other_repos_section` (the guide contains the heading `Other IronbellyOrg repos`, every repo name in `_TARGETS`, the path of every `*.json` file that exists in `other-repos/`, the path `.github/rulesets/other-repos/protect-aidev02.json`, `$REPO`, `$BRANCH`, `admin:org`, `ahead_by` and `zz-selftest-`). Because the test reads the files that exist, an absent optional `protect-aidev02.json` does not fail it. Dependents: no other indexed file imports this test (graph lead, not proof), so the full `tests/docs` folder is run too.

Acceptance criteria:
- `uv run pytest tests/docs/test_branch_protection_rulesets.py --collect-only -q` lists `test_branch_rulesets[protect-master-refs/heads/master]`, `test_branch_rulesets[protect-integration-refs/heads/integration]`, `test_tag_ruleset`, `test_no_default_branch_token_anywhere`, `test_guide_has_apply_and_check_commands` and the four new tests named above.
- `uv run pytest tests/docs/test_branch_protection_rulesets.py -v` passes, `uv run pytest tests/docs -q` passes, and `uv run ruff check tests/docs/test_branch_protection_rulesets.py` reports no error. The repository-wide `make lint` is run and recorded by Task 14, not here, because it also runs `lint-architecture` over every file.
- Reading the test shows `rglob("*.json")` in `test_no_default_branch_token_anywhere`, an unchanged `_load` and no change to `_BRANCH_FILES`.
- The files-match-the-table test would fail for a missing `protect-main-mirror.json` or for an extra unlisted `*.json` in `other-repos/` (shown by reading the assertion; `protect-aidev02.json` must not exist after this task).

## Phase 2: Read-only audits of the six repositories

## Task 5: Write the audit record for coder_orca

Write `.dev/issues/837/audit/coder_orca.md` following the block list of section 3.4 of `./source.md` with `REPO=coder_orca` (a non-fork repo where `clayphi` has admin), using only read-only `gh api` GET calls. Record in order: the header (`END` from `date -u +%Y-%m-%dT%H:%M:%SZ` and `START` 90 days before it); the preflight (`gh api user --jq .login`, and `permissions.admin`, `default_branch`, `archived`, `private` of the repo); the counts (`hooks`, `keys`, `branches/main/protection`, and `gh api --paginate orgs/IronbellyOrg/installations`, written as "could not run" with the real error text if it fails); the existing ruleset list; the tip SHA of `main`; the events of `refs/heads/main` for the 90 days from the activity endpoint with `time_period=year`, each classified as direct push by human, direct push by automation, sync, pr_merge or branch_creation; the tag evidence (count of `v*` refs read over every page with `--paginate`, summing the per-page counts; the statement that the activity endpoint shows no tag events); the producer search; the blocks table; the result `CLEAR` or `BLOCKED`; and the revert commands with an empty id column.

For the producer search the tag ruleset is a fixed skip for this repo (E-2 of the merged requirements). Confirm it by reading the private repository's release tooling that E-2 names, with the read-only contents call, and keep the decoded text out of every output: redirect it to a file or a shell variable, never print it, and write what matched only to `.dev/issues/837/private/coder_orca-producer-evidence.md` (never staged). In the audit file record only the neutral sentence of the constraints, a yes or no for "the tooling deletes `v*` tags" and the number of matching lines, and whether `.github/workflows` exists in coder_orca. Also write `.dev/issues/837/private/guard-patterns.txt`, one fixed string per line with no blank line, holding the file name, the folder name and the names of the tag-deleting functions that E-2 lists; Task 13 uses it as a pre-stage guard. Neither private file may be staged.

Acceptance criteria:
- `.dev/issues/837/audit/coder_orca.md` exists and has every block of section 3.4 (header, preflight, counts, existing rulesets, tips, events kept, tag evidence, producer search, blocks, result, revert commands); the fork test block says "not a fork".
- `END` and `START` are written down, the `main` tip SHA is a 40-character value, and every kept event row has a classification.
- The installations read is recorded as "could not run" with the error text (or its output if it ran), and the blocks table lists it with who clears it.
- The tag ruleset decision for this repo is "skip" with the neutral sentence, and `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/coder_orca.md` prints 0.
- `.dev/issues/837/private/coder_orca-producer-evidence.md` and `.dev/issues/837/private/guard-patterns.txt` exist, `test -s .dev/issues/837/private/guard-patterns.txt` succeeds, `wc -l` of that file equals the number of names E-2 lists (one line per name, no blank line), and `git status --short .dev/issues/837` is the only place they show (the folder is never staged).
- The last section of the audit file lists every command run, and none is POST, PUT or DELETE; the private contents read is written there only as "contents read of the private release tooling (path in `private/`)", with no path, file or folder name.

## Task 6: Write the audit record for CPA-Manager-Plus

Depends on: Task 5

Write `.dev/issues/837/audit/CPA-Manager-Plus.md` following section 3.4 of `./source.md` with `REPO=CPA-Manager-Plus` (a fork where `clayphi` has admin; the parent is read from `gh api repos/IronbellyOrg/CPA-Manager-Plus --jq .parent.full_name`, expected `seakee/CPA-Manager-Plus`, so `PARENT_OWNER=seakee`), read-only. Use the same blocks as Task 5 and add: the fork test (`compare/$PARENT_OWNER:main...main`, recording `ahead_by` and `behind_by`); the events for `refs/heads/main`, and for any other branch you audit, with `time_period=year` filtered to `START`; the count of `v*` refs over every page and a check of the targets of the most recent `v*` tags against the parent's tags of the same name; and the producer search for the tag ruleset: list `.github/workflows` and read each workflow, record `gh api repos/IronbellyOrg/CPA-Manager-Plus/actions/runs --jq .total_count`, search for `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete` and `--force`, resolve each hit by reading it, and look for other IronbellyOrg repos that hold a release token for it with the read-only call `gh api -X GET search/code -f q='CPA-Manager-Plus org:IronbellyOrg'` (if that call fails, write "could not run" and block). Record the excluded branches `dev` and `release/v*` as exclusions, not protected.

Acceptance criteria:
- `.dev/issues/837/audit/CPA-Manager-Plus.md` exists with every block of section 3.4, including the fork test with the parent name, `ahead_by` and `behind_by`.
- The producer search table has one row per place searched (each workflow file, the code search, the tag import path) with the hit and how it was resolved, and an overall `CLEAR` or `BLOCKED` for the tag ruleset.
- The result line says `BLOCKED` while the installations read could not run, and names who clears it.
- The last section lists every command run, none of them POST, PUT or DELETE.

## Task 7: Write the audit record for IronOrca

Depends on: Task 5

Write `.dev/issues/837/audit/IronOrca.md` following section 3.4 of `./source.md` with `REPO=IronOrca` (a fork where `clayphi` has admin; expected parent `stablyai/orca`, so `PARENT_OWNER=stablyai`), read-only, with the same blocks as Task 6 and these additions. Audit `refs/heads/main` and also `refs/heads/aidev02` (events only, for the record; protecting `aidev02` needs Clay's written yes). For the producer search read every file in `.github/workflows`, note the guard on the write job of `release-cut.yml` (a write job that carries `if: github.repository == 'stablyai/orca'` never runs in the fork), note the scheduled workflows that do run in the fork, and record for each workflow whether it has an unfiltered `on: push` trigger (the runbook's scratch self-test pushes a throwaway branch; if any workflow would start on it, say which). Record the count of `v*` refs read over every page and how many are not plain `vX.Y.Z`, how tags arrive from the parent (a person importing them, or a workflow), and a check of recent `v*` tag targets against the parent's tags. Run the code search `gh api -X GET search/code -f q='IronOrca org:IronbellyOrg'`.

Acceptance criteria:
- `.dev/issues/837/audit/IronOrca.md` exists with every block of section 3.4, the fork test, the `main` and `aidev02` event tables and the tag evidence.
- Each workflow file in `.github/workflows` appears in the producer search table with its tag and push findings and its `on: push` status.
- The file states the apply-day role that the fork test implies (mirror if `ahead_by` is 0, full if above 0) as a note, and that the mirror needs Clay's written acceptance.
- The last section lists every command run, none of them POST, PUT or DELETE.

## Task 8: Write the audit record for IronHands-CLI

Depends on: Task 5

Write `.dev/issues/837/audit/IronHands-CLI.md` following section 3.4 of `./source.md` with `REPO=IronHands-CLI`, a handoff repo where `clayphi` has only read access, read-only. Record: the header; `gh api repos/IronbellyOrg/IronHands-CLI --jq '[.fork,.parent.full_name,.default_branch,.archived,.private] | @tsv'`; the fork test (it is a fork: `compare/$PARENT_OWNER:main...main`, recording `ahead_by` and `behind_by`), and the role that results: Ryan applies the mirror only when `ahead_by` is 0 and Clay's written acceptance of the mirror (gate G4) is quoted, otherwise the full role; the tip of `main`; the events of `refs/heads/main` for the 90 days, classified; the count of `v*` refs over every page; the workflow list read-only with the search for tag and push verbs, so Clay's workflow search for Ryan's tag ruleset is complete. Do not run the admin-only checks (`hooks`, `keys`, `branches/main/protection`, installations, classic protection): list them in a section "Checks Ryan must run (admin only)" with their commands. The result line says what Clay's read-only part found and that the apply belongs to Ryan.

Acceptance criteria:
- `.dev/issues/837/audit/IronHands-CLI.md` exists with the blocks that read access allows, a section "Checks Ryan must run (admin only)" with the exact commands using `REPO=IronHands-CLI`, and the fork test result with the parent name.
- The tag ruleset line says whether Clay's read-only workflow search found any producer that moves or deletes `v*` tags.
- No command in the file is a write, and the file states that nothing was written to the repo.

## Task 9: Write the audit record for irondots

Depends on: Task 8

Write `.dev/issues/837/audit/irondots.md` with the same structure as Task 8 and `REPO=irondots` (the fork test only if the repo has a parent). Record the events of `refs/heads/main` (the repo is young: note when `main` was created), and record the events of the branches matching `dot/*` only as an exclusion note (they are excluded from protection and must stay deletable). Record whether its gated-release workflow is present; if it is, read it and record whether it only creates tags (creating a tag stays allowed under the tag ruleset); if it is not present, record that.

Acceptance criteria:
- `.dev/issues/837/audit/irondots.md` exists with the read-only blocks, the section "Checks Ryan must run (admin only)", the `dot/*` exclusion note and a finding about tag-creating workflows that names the workflow file when one exists.
- Events for `main` are classified, with the repo's age stated; no write command is listed.

## Task 10: Write the audit record for ironops-marketplace

Depends on: Task 8

Write `.dev/issues/837/audit/ironops-marketplace.md` with the same structure as Task 8 and `REPO=ironops-marketplace`: read-only blocks, the fork test if it has a parent, the `v*` count over every page, the workflow search, and the section "Checks Ryan must run (admin only)".

Acceptance criteria:
- `.dev/issues/837/audit/ironops-marketplace.md` exists with the read-only blocks and the admin-only section, and states whether any `v*` tag or tag-moving workflow exists.
- No write command is listed.

## Phase 3: Gate ledger, Ryan handoff and apply runbook

## Task 11: Write the gate ledger .dev/issues/837/gates.md

Depends on: Task 5, Task 6, Task 7, Task 8, Task 9, Task 10

Write `.dev/issues/837/gates.md` as defined in section 3.5 of `./source.md`. Start with a header that names the gates G1 to G9 in one line each and quotes where Clay's recorded answer is (`.dev/issues/837/issue-summary.md`, "Decided for this work (iteration 3)"), cites `.dev/issues/837/accuracy-check.md` line 13 as the verification of the release-tag ruleset's `update` rule that the lead asked for and states the rule that follows (if that rule is not settled, every tag row is `SKIP(not settled)` and only the branch rulesets are copied), and records the two statements that are not gates (Clay's written acceptance of the restated done condition, and `ironbelly`'s written confirmation of admin on each Clay repo) as "not recorded". Then one row per (repo, ruleset): CPA-Manager-Plus (branch role and tag ruleset), IronOrca (branch role, tag ruleset and `aidev02`), coder_orca (`protect-main`, tag ruleset), and for each Ryan repo (`protect-main`, tag ruleset). Columns: repo, ruleset file, decision, first failing gate, evidence path under `.dev/issues/837/audit/`. The only decisions are `APPLY`, `SKIP(<first failing gate>)` and `HANDOFF`. In this Phase 1 draft: `HANDOFF` for the three Ryan repos; `SKIP(Gn)` where a gate fails now (G3 while the installations read could not run, G4 for a mirror without Clay's quoted acceptance, G5 for `aidev02`, G6 for coder_orca's tag ruleset and for any tag ruleset whose producer search is not `CLEAR`); `SKIP(G8)` for a row whose G1 to G7 pass now, because G8 (pushed SHA) and G9 (scratch self-test) can only be evaluated later. Put no private detail in the file (see the constraints). End with the expected end state of this run from section 8 of `./source.md` and the list of clearances that unlock the apply, each with its "yes means" and "no or silence means".

Acceptance criteria:
- `.dev/issues/837/gates.md` has one row for every (repo, ruleset) named above, each with exactly one decision of `HANDOFF`, `SKIP(Gn)` or `APPLY` and a link to the audit file that supports it.
- No row says `APPLY` and no row says `PENDING`.
- Every `SKIP` row names its first failing gate and the audit block that shows it; the three Ryan repos are all `HANDOFF`.
- The header cites `accuracy-check.md` line 13 and states the "not settled" rule.
- The file lists the five clearances of section 8 with what each unlocks.

## Task 12: Write the handoff for Ryan .dev/issues/837/handoff-ryan.md

Depends on: Task 3, Task 8, Task 9, Task 10, Task 11

Write `.dev/issues/837/handoff-ryan.md` as defined in section 3.7 of `./source.md`, for IronHands-CLI, irondots and ironops-marketplace. Per repo: the 90-day audit Clay ran read-only (copy the command, `END`, the classified events and the fork-test result from the audit record); the admin-only pre-apply checks with exact commands (`hooks`, `keys`, `branches/main/protection`, the installations read, classic protection, and a request that Ryan confirm his admin role); the exact apply, read-back, scratch self-test, revert and break-glass commands with `REPO` set, taken from the guide section of Task 3; the tag ruleset, which is included where the repository has no `v*` tag and Clay's read-only workflow search found no tag mover (there is then nothing to break), with the result of that search; and what Ryan reports back (ruleset ids, dates and the read-back output as a comment on issue 837). For IronHands-CLI, a fork, the handoff gives the role rule (mirror only when `ahead_by` is 0 and Clay's written acceptance is quoted, otherwise the full role). Links to `.github/rulesets/other-repos/protect-main.json`, `.github/rulesets/other-repos/protect-main-mirror.json` and `.github/rulesets/protect-release-tags.json` use the single placeholder `<PUSHED-SHA>` in the URL path (a GitHub blob URL on IronbellyOrg/IronClaude). The file keeps the placeholder; the text that is posted as the issue comment has it replaced by the pushed SHA (Task 13, part one). End with a request that the lead hand the text to Ryan.

Acceptance criteria:
- `.dev/issues/837/handoff-ryan.md` has one section per Ryan repo with the parts above, and an opening section that says nothing was written to those repos.
- `<PUSHED-SHA>` appears only in file links, each link ending in one of the three ruleset file names, and the file says where it is replaced.
- Every command names its repository through `$REPO` set at the top of the repo section, and no command is a write except the apply, scratch self-test, revert and break-glass commands that Ryan runs himself.
- The IronHands-CLI section carries the fork role rule, and the file contains no private detail (see the constraints).
- The last paragraph is the request to the lead.

## Task 13: Write the apply runbook .dev/issues/837/apply-runbook.md

Depends on: Task 11

Write `.dev/issues/837/apply-runbook.md` from sections 3.6, 4, 5 and 6 of `./source.md`. State at the top that nothing in the runbook has been executed, that part one runs right after the commit and push whatever the ledger decides, and that part two runs only after the pull request monitor has settled and only for rulesets whose ledger decision becomes `APPLY`.

Part one covers the story steps after this plan. First the pre-commit checks, each with its output recorded: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `make lint` (a failure on files this change does not touch is recorded as pre-existing and named), `git diff --stat` (only the staging list below), and `git status` (nothing under `.claude/` or `.dev/issues/` staged). STOP before any staging: do not stage, commit or push until the lead's written decision on the archived first plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/` is quoted in `.dev/issues/837/issue-summary.md`; the guard's exclusion of that folder is not permission to publish it. Then the staging list (`.github/rulesets/other-repos/`, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py` and `.dev/tasks`; never `.claude/` and never `.dev/issues/`), with the line that the brainstorm folder `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos` is not staged because it describes a private repository (the story names only the changed files and `.dev/tasks`; whether to publish that folder is the user's decision). Then the pre-stage guard: print `gh repo view IronbellyOrg/IronClaude --json visibility -q .visibility`, then run `grep -c -F -f .dev/issues/837/private/guard-patterns.txt` over the files of `git diff --cached` and over the files to be staged; any hit stops the staging; the only path the guard excludes is the archived superseded plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/`, which names that tooling in two lines and cannot be edited, and the runbook lists that as the open item for the lead that the STOP above waits on. Then `git fetch origin` and `git log HEAD..origin/integration`, a rebase onto `origin/integration` if it has commits the branch lacks, the commit, the push, and recording the pushed SHA. Then the comment file, which holds the handoff text with `<PUSHED-SHA>` replaced by the pushed SHA (the committed files keep no placeholder) followed by the draft ledger; run `grep -c -F -f .dev/issues/837/private/guard-patterns.txt <file>` on it (it must print 0), and post it as one comment on issue 837 with `gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>`. Only then run the `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "<title>" --body "<body>"` line. After the monitor settles, and after any later push, run `git diff --exit-code <SHA> -- .github/rulesets/other-repos/ .github/rulesets/protect-release-tags.json docs/developer-guide/branch-protection.md` with the SHA in the posted comment; if anything changed, post a NEW comment, built and posted as above, with the links and the copied commands refreshed from the final head.

Part two is the gated apply for CPA-Manager-Plus, IronOrca and coder_orca with steps R0 to R7 as in section 3.6, the results recorded in the audit file and the ledger as that section says, the variables filled now per repo (`REPO`, `PARENT_OWNER` for the two forks, `BRANCH=main`, and the file to apply as decided by the ledger; `ID`, `END` and `START` are set on apply day), the stop rules, the failure table of section 6, and the interfaces table of section 5 marked read or write. The scratch self-test of R1 pushes with `git push https://github.com/IronbellyOrg/$REPO.git ...` from the scratch clone, so every write command names its repository, and it carries the consequence of section 3.1 for a refused mirror bypass actor: drop the actor from the mirror file and change the file, the test, the guide and D4 together before anything is applied.

Acceptance criteria:
- `.dev/issues/837/apply-runbook.md` has part one with the pre-commit checks (including `make lint`), the staging list that excludes `.claude/`, `.dev/issues/` and the brainstorm folder, the pre-stage guard, the issue comment step (before the pull request command), the pull request command, and part two with R0 to R7 for each of the three Clay repos with `REPO`, `PARENT_OWNER`, `BRANCH` and the ledger-decided file filled.
- It contains the failure table of section 6, the stop rules (first 403 stops that repo; list before any retry; a pre-existing ruleset stops the repo; delete only rulesets this rollout created) and the mirror-refusal consequence.
- Every write command in it names its repository explicitly and none uses a brace placeholder.
- The opening statement says nothing has been executed and says that part one does not depend on `APPLY`.
- Part one, not R6, holds the re-pin step: after the monitor settles and after any later push, `git diff --exit-code <SHA> -- <paths>` against the SHA in the posted comment, and a NEW comment with refreshed links and commands when anything changed; it runs when no ruleset is `APPLY`.
- The file contains no private detail (see the constraints).

## Phase 4: Pull request material

## Task 14: Draft the pull request body .dev/issues/837/pr-body.md

Depends on: Task 4, Task 11, Task 12, Task 13

Write `.dev/issues/837/pr-body.md` from the template of section 3.7 of `./source.md`. Sections: Summary; "Decided for this work (iteration 3)", copied word for word from the matching block at the end of `.dev/issues/837/issue-summary.md` including the line that records Clay's answer (copy the block with a command, never retype it); What this change adds (the files of Tasks 1 to 4); Audit and gate results (one row per repository, summarising its ledger rows from `.dev/issues/837/gates.md`: applied, skipped with the first failing gate, or handed to Ryan, and that nothing is applied yet); The restated done condition per repo (read locally from the section "Done condition for this pull request" of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md`: the issue's literal condition is met by none of the six repos under this design, and issue 837 stays open until Ryan reports); What is left (the three Ryan repos, and the clearances that unlock the apply); Tests run (paste the real output summary lines of `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `uv run ruff check tests/docs/test_branch_protection_rulesets.py` and `make lint`); and as its last line `Refs #837`. The body carries no private detail (see the constraints) and says where the handoff comment on issue 837 is.

Acceptance criteria:
- `.dev/issues/837/pr-body.md` contains the "Decided for this work (iteration 3)" block and a diff of that block against the one in `.dev/issues/837/issue-summary.md` shows no difference.
- The file ends with the line `Refs #837` and contains neither `Fixes #837` nor `Closes #837`.
- The per-repo table has one row for each of the six repos and matches the decisions in `.dev/issues/837/gates.md`.
- The Tests run section shows output copied from commands run in this task, including `make lint`, not typed from memory; a `make lint` failure on files this change does not touch is named as pre-existing.
- `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/pr-body.md` prints 0.
