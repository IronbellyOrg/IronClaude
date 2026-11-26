# Design: branch protection rulesets for six more IronbellyOrg repos (issue 837)

- Type: architecture. Format: spec.
- Input: `merged-requirements.md` in this folder (adversarial status `partial`: two HIGH invariants, INV-014 and INV-016, are answered in its text but were not re-debated).
- Also read: Clay's recorded answer (`.dev/issues/837/issue-summary.md`, "Decided for this work (iteration 3)"), `.github/rulesets/*.json`, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py`.
- Grounding: index_state: fresh (checked_at 2026-11-26T12:59:50Z, worktree_root `/home/coder/workspaces/worktrees/IronClaude/issue-837`); codegraph tools used: `codegraph_status`, `codegraph_node` with `symbolsOnly` on `tests/docs/test_branch_protection_rulesets.py` (10 symbols; no other indexed file depends on it, which is a lead, not proof). The JSON and Markdown files are not indexed, so they were read directly.

## 1. What this design decides

The merged requirements fix what to build (FR-001 to FR-010, decisions D1 to D7). This design fixes how it fits together, in what order it runs, and which parts are allowed to write to GitHub.

| # | Decision | Why |
|---|---|---|
| 1 | Work runs in three phases. Phase 1 (files, test, guide, read-only audits, drafts) is what `/sc:implement` executes. Phase 2 is the story's commit, push and pull request. Phase 3 (applying rulesets to GitHub) runs after the pull request monitor settles, from a runbook, not as a plan step. | FR-007 applies from a pushed commit SHA, and the story pushes only after `/sc:implement`. Applying is an outward write with its own gates, so it must not hide inside a code-writing step. |
| 2 | No script and no render tool. Audits and applies are documented `gh api` commands with variables; results go into per-repo records. | Non-goal of the merged requirements; six repos do not justify a tool (A, B and C all agreed in Round 2). |
| 3 | Every possible write has an explicit gate decision, recorded in a ledger: `APPLY`, `SKIP(reason)` or `HANDOFF`. Nothing is applied by default. | Clay's answer is a go only "after each repo's own 90-day check"; the mirror, `aidev02`, the installations check and the restated done condition each need a decision it does not contain (INV-003, INV-014, INV-015). |
| 4 | Where a decision is missing, the design picks the safe default and says so: the fork branch rulesets and `aidev02` are skipped, and a check that could not run blocks the repo it covers. | Missing evidence is not a clean audit (D3). |
| 5 | The two Ryan-only outputs (handoff text, ruleset ids) are posted to issue 837 and the pull request body, never left only in `.dev/issues/`. | `.dev/issues/` is never staged (INV-016). |
| 6 | The pull request says `Refs #837`, and issue 837 stays open until Ryan reports. | The three Ryan repos are not applied by this change (INV-014). |
| 7 | IronClaude's three JSON files and the live IronClaude rulesets are not touched. In the guide only the "Tests" paragraph is edited (it must name the new files); every other existing section stays. In the test, every existing assertion stays and one glob becomes recursive; everything else is added beside them. | Smallest change; the IronClaude protection is live and the guide's existing commands are pinned by the existing test. |

## 2. Architecture

```text
 IronClaude repo (reviewed, committed)                       GitHub (outward, gated)
 ─────────────────────────────────────                       ───────────────────────
 .github/rulesets/
   protect-master.json ───── derive (test) ─┐
   protect-integration.json (unchanged)     ├─► other-repos/protect-main.json          (full role)
   protect-release-tags.json ─ reused ──────┘   other-repos/protect-main-mirror.json   (full minus pull_request)
                                                other-repos/protect-aidev02.json       (only on Clay's written yes)
 tests/docs/test_branch_protection_rulesets.py   pins files, derivation, target table, guide text
 docs/developer-guide/branch-protection.md       + "Other IronbellyOrg repos" section

 PHASE 1  (inside /sc:implement)        PHASE 2 (story steps 9-10)         PHASE 3 (after the monitor settles)
 ─ files, test, guide                   ─ commit + push  ──► SHA           per Clay repo (CPA-Manager-Plus, IronOrca, coder_orca):
 ─ audits, read-only, all 6 repos       ─ pull request, `Refs #837`           re-audit ─► gates ─► scratch self-test ─► snapshot
 ─ gate ledger (draft)                  ─ post handoff + ledger to               ─► apply (tags, branches) ─► read-back
 ─ handoff draft, apply runbook           issue 837 (SHA-pinned)                 ─► ids/dates/SHA ─► issue 837 + PR body
                                                                              ─► after last push: compare files to SHA, PUT if changed
 Ryan's three repos: Phase 1 produces the audit and the handoff; Phase 3 never writes to them.
```

State that moves between phases lives in four files under `.dev/issues/837/` (never staged; their content is copied to GitHub, section 3.7): `audit/<repo>.md`, `gates.md`, `handoff-ryan.md`, `apply-runbook.md`.

## 3. Components

### 3.1 C1: ruleset files (FR-001, D1, D4)

New folder `.github/rulesets/other-repos/`. The three existing files in `.github/rulesets/` are not changed. Formatting follows `protect-master.json` (two-space indent, one-line `ref_name` and `bypass_actors`).

| File | Always created? | Derivation from `protect-master.json` | Rule types it must print |
|---|---|---|---|
| `protect-main.json` | yes | `name` becomes `protect-main`; `conditions.ref_name.include` becomes `["refs/heads/main"]`; nothing else changes | `deletion`, `non_fast_forward`, `pull_request` |
| `protect-main-mirror.json` | yes | as `protect-main.json`, then `name` becomes `protect-main-mirror` and the `pull_request` rule object is removed | `deletion`, `non_fast_forward` |
| `protect-aidev02.json` | only if Clay's written yes for `aidev02` is quoted in `issue-summary.md` | `name` becomes `protect-aidev02`; `include` becomes `["refs/heads/aidev02"]` | `deletion`, `non_fast_forward`, `pull_request` |

Unchanged in all three: `target: branch`, `enforcement: active`, `exclude: []`, `bypass_actors` = the repository admin role (`actor_id` 5, `RepositoryRole`, `bypass_mode: pull_request`), and the five `pull_request` parameters with `required_approving_review_count: 0`. The tag file `protect-release-tags.json` is applied as it is (name `protect-release-tags`, `refs/tags/v*`, `deletion`, `non_fast_forward`, `update`, no bypass).

Open point carried from D4: whether the API accepts `bypass_mode: pull_request` on a ruleset that has no `pull_request` rule (the mirror) is UNVERIFIED. The scratch self-test (3.6, R1) creates a copy of the mirror file through `POST`, so it answers this before any real create; if the API refuses it, the mirror file drops the bypass actor and the test, guide and D4 are updated together before anything is applied.

### 3.2 C2: pinning test (FR-002, FR-003; INV-011)

File: `tests/docs/test_branch_protection_rulesets.py`. Every existing assertion stays, including the literal guide strings of `test_guide_has_apply_and_check_commands`. Changes:

| Item | Change |
|---|---|
| `test_no_default_branch_token_anywhere` | `_RULESETS.glob("*.json")` becomes `_RULESETS.rglob("*.json")` so `other-repos/` is covered (the current glob is not recursive, so a `~DEFAULT_BRANCH` there would escape it). |
| New constant `_OTHER` | `_RULESETS / "other-repos"`; a loader `_load_other(name)` reads from it (the existing `_load` reads only the root folder and stays as it is). |
| New constant `_TARGETS` | The target table: for each of the six repos, its applier (`clay` or `ryan`), the candidate branch files, and the tag entry (`conditional`, `skip` or `handoff`). A fork lists both `protect-main` and `protect-main-mirror`, because the role is chosen on apply day (D7). `protect-aidev02` is listed for IronOrca and marked optional. |
| New test: full role derived | `protect-main` (and `protect-aidev02` if the file exists) equals `protect-master` after replacing only `name` and `ref_name.include`; rule types are `deletion`, `non_fast_forward`, `pull_request`; bypass is the admin `pull_request` actor; zero approvals. |
| New test: mirror derived | `protect-main-mirror` equals `protect-main` after replacing `name` and removing the `pull_request` rule; rule types are `deletion` and `non_fast_forward`; same bypass. The mirror has its own expected list and does not join the three-type check. |
| New test: files match the table | The set of `*.json` in `other-repos/` equals the set of files named in `_TARGETS`, except that a file marked optional may be absent. A missing, unused or unlisted file fails. |
| New test: guide section | The guide contains the heading "Other IronbellyOrg repos", every repo name in `_TARGETS`, every `other-repos/` file path, `$REPO`, `$BRANCH`, `admin:org`, `ahead_by` and `zz-selftest-`. |

Run: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`. The codegraph shows no other indexed file depends on this test; that is a lead only, so the full suite is still run before the commit (`uv run pytest tests/docs -q`).

### 3.3 C3: guide section (FR-004; INV-001, INV-011)

File: `docs/developer-guide/branch-protection.md`. Add one H2, "Other IronbellyOrg repos", after "Break glass" and before "Tests". Edit one sentence of "Tests" so it also names the new files. All IronClaude sections and commands stay (the existing test pins them). The new section is written with variables, never with a repo name in a command:

| Sub-section | Content |
|---|---|
| Targets | The target table: repo, applier, role (full, or "mirror when the fork test gives 0"), tag ruleset (apply, skip, handoff), excluded branches (`dev`, `release/v*`, `dot/*`). For each fork an Owner column holding the standing rule "switch to `protect-main.json` when `ahead_by` is above 0" and the named person. |
| Variables | `REPO`, `BRANCH`, `PARENT_OWNER`, `ID`, `END`, `START`. |
| Role of a fork's `main` | The `compare` command that prints `ahead_by` and the rule that follows from it (D7). |
| Before applying | Preflight (login, admin, default branch), hooks and keys counts, `branches/main/protection` (404 expected), existing ruleset list (expected empty), the 90-day audit command, the producer search checklist, and the note that the organisation installations command needs the `admin:org` scope. |
| Apply | Create only if the name is absent; tags first, then non-default branches, then `main`. |
| Check | Rule types per branch, the full read-back of each ruleset, the tag ruleset check. |
| Self-test | The scratch ruleset on a throwaway branch (3.6, R1). |
| Roll back and break glass | The same commands as the IronClaude section with `$REPO` and `$ID`. |

The guide holds no dated audit numbers; those live in the audit records and the pull request body.

### 3.4 C4: audit record per repo (FR-005, FR-006; D3, D6; INV-006, INV-009)

One file per repo, `.dev/issues/837/audit/<repo>.md`, six in total. Phase 1 writes all six, read-only (Clay's read access is enough for the activity endpoint, P-3). The record is a fixed template, so a later reader can compare repos:

| Block | Content and command |
|---|---|
| Header | `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)` and `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`; both written down. |
| Preflight (the three Clay repos only) | `gh api user --jq .login` prints `clayphi`; `gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] \| @tsv'`. |
| Counts (Clay repos) | `gh api repos/IronbellyOrg/$REPO/hooks --jq length`, `.../keys --jq length`, `.../branches/main/protection` (404 expected), `gh api --paginate orgs/IronbellyOrg/installations` (expected to fail: no `admin:org`; written as "could not run" with the error text). |
| Existing rulesets | `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] \| [.id,.name,.enforcement] \| @tsv'`; empty expected. |
| Tips | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH --jq .object.sha` for `main` and any other audited branch. |
| Fork test (forks) | `gh api repos/IronbellyOrg/$REPO --jq .parent.full_name`, then `gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by,.behind_by] \| @tsv'`. |
| Events kept | `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '.[] \| select(.timestamp >= "'"$START"'") \| [.timestamp,.ref,.activity_type,.actor.login] \| @tsv'`. Each kept row is classified: `direct push by human`, `direct push by automation`, `sync` (a parent fast-forward on a fork `main`), `pr_merge`, `branch_creation`. `time_period=quarter` is not used (its length is UNVERIFIED). Issue 702's `git log` cross-check is not used on forks (it counts upstream history). |
| Tag evidence | Number of `v*` refs (`gh api repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`); the statement that the activity endpoint shows no tag events (so tag writes are invisible to this audit, INV-009); for a repo that has a parent, a check of each recent `v*` tag target against the parent's tag of the same name. |
| Producer search | A table "place, hit, how resolved" covering: every workflow of the repo (list them with `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows`, read each; follow called scripts); every IronbellyOrg repo that holds a release token for the target (E-2: `IronbellyOrg/Coder` for coder_orca); the way tags arrive from the parent. Search terms: `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`. A hit is resolved by reading it, never by absence of grep output (names built at run time defeat grep, E-2). |
| Blocks | A table "ruleset, missing check or event, who clears it, what clears it". The installations read always appears here for the three Clay repos. |
| Result | `CLEAR` or `BLOCKED` with the reasons. |
| Revert commands | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` for each ruleset that may be created, written before the first write on that repo, with the id column empty until apply. |

### 3.5 C5: gate ledger (D3, D7; INV-003, INV-014, INV-015)

One file, `.dev/issues/837/gates.md`: one row per (repo, ruleset) and one decision per row, `APPLY`, `SKIP(<first failing gate>)` or `HANDOFF`. The ruleset is applied only when every gate G1 to G9 passes for it. Phase 1 writes the draft with everything that can be decided read-only; Phase 3 re-evaluates G2 to G9 inside the hour before the first write.

| Gate | Passes when | If it fails |
|---|---|---|
| G1 Authority | The repo is CPA-Manager-Plus, IronOrca or coder_orca, and Clay's recorded answer (a go on those three, quoted in `issue-summary.md`) is present. | The three Ryan repos are always `HANDOFF`: no write of any kind. |
| G2 Preflight | Login is `clayphi`, `admin` is `true`, default branch is `main`, repo is not archived and is public. | `SKIP`; stop that repo. |
| G3 Audit | The audit record's result is `CLEAR` for the target ref: no automation pushes straight to it, every event is classified, and every check that could not run is cleared (an org owner's output of the installations read, or Clay's written acceptance quoted in `issue-summary.md`). | `SKIP`; the block names who clears it. |
| G4 Role | A non-fork gets `protect-main`. A fork gets `protect-main-mirror` when `ahead_by` is 0 **and** Clay's written acceptance of the mirror's direct-push exposure is quoted in `issue-summary.md`; it gets `protect-main` when `ahead_by` is above 0. | With no acceptance, the fork's branch ruleset is skipped and reported (the fallback of D7). |
| G5 `aidev02` | Clay's written yes is quoted in `issue-summary.md` and `protect-aidev02.json` exists. | `SKIP`; the file is not created. |
| G6 Tag producers | The producer search of the audit record is `CLEAR` and the repo is not coder_orca. | `SKIP` the tag ruleset (coder_orca always: E-2). |
| G7 Existing rulesets | The list is empty at the moment of the snapshot. | `SKIP`; nothing pre-existing is updated or deleted. |
| G8 Source | The files to apply are at a commit SHA that is pushed to `origin` and equals the branch head; the files have no uncommitted change. | `SKIP` until it holds. |
| G9 Self-test | The scratch self-test (3.6, R1) passed for the role about to be applied, and the API accepted the scratch copy. | `SKIP`; stop that repo. |

The ledger header also records two statements that are not gates but must be quoted before the issue is treated as done: Clay's written acceptance of the restated done condition (section "Done condition for this pull request" of the merged requirements), and `ironbelly`'s written confirmation of admin on the repo (the revert owner, D7 and Rollback).

### 3.6 C6: apply runbook (FR-006, FR-007, Verification; INV-002, INV-010)

Phase 1 writes it as `.dev/issues/837/apply-runbook.md` (the commands above with the variables filled in per repo, plus this order). Phase 3 follows it per repo, one repo at a time; a stop on one repo does not stop the others.

| Step | Action | Record |
|---|---|---|
| R0 | Re-run the audit and the fork test inside the hour; refresh `END`, tips and `ahead_by`; re-evaluate G2 to G9. | Audit file, ledger. |
| R1 | Scratch self-test for each role the ledger says `APPLY`, before the snapshot. In a scratch clone of the target repo (never IronClaude): create and push the throwaway branch `zz-ruleset-selftest` with two commits; create the scratch ruleset `zz-selftest-<role>` from the role file with `jq '.name="zz-selftest-<role>" \| .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' <file> \| gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -`; push an empty commit (full role: must be refused with GH013) or `git push --force origin HEAD~1:zz-ruleset-selftest` (mirror: must be refused); delete the scratch ruleset by id, then the branch (`git push origin --delete zz-ruleset-selftest`); confirm `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'` shows no name starting `zz-selftest-`. On IronOrca first read every workflow for an unfiltered `on: push` (Actions are active there, P-6); if one exists, name the branch so it cannot match or skip that repo's self-test and record why. | Result and the API answer to the scratch `POST` (this also settles whether the mirror's bypass actor is accepted, 3.1). |
| R2 | Snapshot: the existing ruleset list; stop the repo if it is not empty (G7). | List in the audit file. |
| R3 | Apply in order: tag ruleset (if `APPLY`), `aidev02` (if `APPLY`), `main` role. Before each: list the names; the name must be absent. Then `gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/<file>` from a checkout at the recorded SHA. After a timeout, list again before any retry. On the first 403, stop that repo and record the partial state (write permission has never been tried). | Id, date, SHA per ruleset. |
| R4 | Read back: `gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'`; `gh api repos/IronbellyOrg/$REPO/rulesets/$ID` compared with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset the rule types. A ruleset that fails the read-back is deleted by id (this rollout created it) and the repo is reported `SKIP(read-back)`. | Output in the audit file. |
| R5 | Record ids, dates, SHA and read-back in the audit file and the ledger; post the ledger table and ids as a comment on issue 837; add the same to the pull request body (section 3.7). | Comment URL. |
| R6 | After the pull request monitor has settled and the last push is made: for each applied file, `git diff --exit-code <SHA> -- .github/rulesets/other-repos/<file>`. A changed file means `gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input <file>` and a new SHA in the record. | Record. |
| R7 | For a mirror: name the owner and date of the first Sync fork on issue 837; the status is "pending" until it is run; if it is refused, delete the new ruleset by id and report. | Issue comment. |

### 3.7 C7: handoff, reporting and the pull request (FR-008, FR-009, FR-010; INV-014, INV-016)

| Output | Written in | Content | Reaches GitHub as |
|---|---|---|---|
| `handoff-ryan.md` | Phase 1 draft; finalised after the push in Phase 2 | Per Ryan repo: the 90-day audit Clay ran read-only (command, `END`, events, classification); the admin-only pre-apply checks (hooks, keys, `branches/main/protection`, the installations read, classic protection, Ryan's admin role); the exact apply, read-back, scratch self-test, revert and break-glass commands with `$REPO` set; the tag ruleset where D5 allows it, with Clay's read-only workflow search; links to `.github/rulesets/other-repos/protect-main.json` and `protect-release-tags.json` pinned to the pushed commit SHA; what Ryan reports back (ruleset ids and the read-back output, as a comment on issue 837). The text ends with a request that the lead hand it to Ryan. | A comment on issue 837, posted right after the push, and a pointer in the pull request body. |
| `gates.md`, `audit/<repo>.md` | Phase 1 and Phase 3 | As 3.4 and 3.5. | The ledger table and the audit results (a short table per repo) go in the pull request body and an issue 837 comment. The full files stay local. |
| Pull request body | Phase 2, edited in Phase 3 | Summary; the "Decided for this work" block word for word, including Clay's answer; files changed; per-repo result table (applied, skipped with reason, handed to Ryan); what is left (the three Ryan repos; the owner decisions); tests run; last line `Refs #837` (never `Fixes` or `Closes`). Edited after Phase 3 with `gh pr edit <number> --repo IronbellyOrg/IronClaude --body-file <file>`. | The pull request. |
| `result.md` | End of the run | Three lines as the story says. `outcome` is `partial` when any ruleset is `SKIP` or `HANDOFF`, which is the expected outcome (section 8). | Local only. |

## 4. Phases and sequencing against the story's steps

The story's steps 5 to 10 are fixed: plan, `/sc:implement`, confirm, commit and push, pull request. This design maps onto them without changing them.

| Phase | Story step | What happens | Writes outside this worktree? |
|---|---|---|---|
| 1 | 7 (`/sc:implement`) | T1 create `protect-main.json` and `protect-main-mirror.json` (no `protect-aidev02.json` without Clay's yes). T2 update the pinning test. T3 add the guide section and edit its "Tests" paragraph. T4 run the six read-only audits, the fork tests and the tag evidence (3.4). T5 run the producer search for the tag rulesets of CPA-Manager-Plus and IronOrca (coder_orca is a fixed skip, E-2) and write the "Producer search" block. T6 write the draft gate ledger. T7 write the draft handoff for Ryan. T8 write `apply-runbook.md`. T9 draft the pull request body. T10 run `uv run pytest tests/docs -q` and `make lint`. | No. Read-only `gh api` GET calls only. |
| 2 | 8 and 9 | Confirm the plan's progress file and run the related tests again. Stage the changed files: `.github/rulesets/other-repos/`, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py`, `.dev/tasks`, and this brainstorm folder (brainstorm folders are tracked in this repo by convention); never `.claude/` or `.dev/issues/`. Commit on a feature branch from `integration`, push to `origin`, record the pushed SHA. Post the handoff and the draft ledger as a comment on issue 837 with links pinned to the SHA. | Yes, to `origin` and issue 837 of IronClaude only. |
| 2 | 10 | `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "..." --body "..."`; the body is the template of 3.7, ending `Refs #837`. | Yes, the IronClaude pull request. |
| 3 | after 10 | When the monitor reports every check green and every comment handled: follow `apply-runbook.md` for each Clay repo (3.6). Then edit the pull request body and comment on issue 837 with the results. | Yes, to the three Clay repos, only for rulesets whose gates all pass. |

Why Phase 3 is not a plan step: `/sc:implement` runs before the push, so the SHA of G8 does not exist yet, and an outward write to repositories other than IronClaude must not be hidden inside an automated code step. `/sc:workflow` should therefore plan Phase 1 in full, include the Phase 2 preparation items (the staging list, the SHA record, the issue comment), and carry Phase 3 as a final "runbook, executed by the session after the pull request monitor settles, never by `/sc:implement`" item with no executable subtasks.

Dependencies inside Phase 1: T1 before T2 (the test reads the files) and before T3's table; T4 and T5 are independent of T1 to T3 and can run in parallel with them; T6 needs T4 and T5; T7 needs T4 and T6; T8 needs T6; T9 needs T6 and T7; T10 last.

## 5. Interfaces

All interfaces are `gh` and `git` commands. Every `gh` call names the repository explicitly (`repos/IronbellyOrg/$REPO/...`, `--repo IronbellyOrg/IronClaude`); no call uses a brace placeholder or the fork-parent default, and nothing touches `SuperClaude-Org/SuperClaude_Framework`.

| Interface | Command shape | Reads or writes |
|---|---|---|
| Identity and permission | `gh api user --jq .login`; `gh api repos/IronbellyOrg/$REPO --jq '...'` | read |
| Audit | `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq '...'` | read |
| Tips and tags | `.../git/ref/heads/$BRANCH`, `.../git/matching-refs/tags/v` | read |
| Fork test | `.../compare/$PARENT_OWNER:main...main --jq '[.ahead_by,.behind_by]'` | read |
| Workflow search | `.../contents/.github/workflows` and each file | read |
| Existing rulesets | `gh api repos/IronbellyOrg/$REPO/rulesets` | read |
| Create | `gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input <file>` | **write** (Phase 3 only, and R1 scratch) |
| Update | `gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input <file>` | **write** (Phase 3 R6 only) |
| Delete | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID` | **write** (revert, scratch cleanup; only rulesets this rollout created) |
| Read-back | `.../rules/branches/$BRANCH`, `.../rulesets/$ID` | read |
| Issue and pull request | `gh issue comment 837 --repo IronbellyOrg/IronClaude --body-file <file>`; `gh pr edit <n> --repo IronbellyOrg/IronClaude --body-file <file>` | **write** (IronClaude only) |
| Throwaway branch | `git push origin zz-ruleset-selftest`, `git push origin --delete zz-ruleset-selftest` in a scratch clone of the target repo | **write** (R1 only) |

Phase 1 uses only the read rows. A write row appears in no Phase 1 task.

## 6. Failure handling and rollback

| Failure | Detected by | Response | Rollback |
|---|---|---|---|
| First `POST` returns 403 | R3 | Stop that repo, no retry, record the partial state; report the repo as not applied. Other repos continue. | Delete any ruleset already created on that repo by id. |
| Timeout or ambiguous answer on `POST` | R3 | Read the ruleset list before any retry; create only if the name is still absent. | As above. |
| Existing ruleset found at the snapshot | R2 / G7 | Stop that repo; update and delete nothing that pre-existed. | None needed. |
| Read-back differs from the file | R4 | Delete the ruleset this rollout created, report `SKIP(read-back)`. | Delete by id. |
| Half-applied repo (tags created, branch `POST` fails) | R3 | The tag ruleset has no bypass; record the state and either apply the branch ruleset on a later run or delete the tag ruleset by id, whichever the revert owner decides in writing on issue 837. | Delete by id. |
| Scratch ruleset or throwaway branch survives | R1 | List `zz-selftest-*` rulesets and branches; delete; the real create waits until the list is clean. | Delete by id and `git push origin --delete`. |
| Sync fork refused after a mirror | R7 | Delete the new ruleset by id; report; the fork test and the standing switch rule are reviewed. | Delete by id. |
| A review fix changes an applied file | R6 | `PUT` the new file; record the new SHA. | Re-`PUT` the previous file. |
| A tag producer is found after the apply | later, by anyone | Delete the tag ruleset by id (the break-glass sequence in the guide); report. | Delete by id. |
| Evidence missing or a check cannot run | G3 | `SKIP` and name who clears it; never treated as clean. | None needed. |

Who reverts: the repo admin. `ironbelly`'s admin role on the three Clay repos is UNVERIFIED; until `ironbelly` confirms it in writing on issue 837, Clay is the revert owner and must be reachable on the day of the apply (Rollback section of the merged requirements, INV-004).

## 7. Verification and traceability

| Requirement | Built by | Checked by |
|---|---|---|
| FR-001 files exist, aidev02 only on a yes | 3.1 | Test "files match the table"; `ls .github/rulesets/other-repos/`; no `protect-aidev02.json` unless the ledger quotes the yes. |
| FR-002 derivation, mirror in the type table | 3.2 | New derivation tests (full, mirror, optional aidev02). |
| FR-003 target table, recursive glob, parameterised commands accepted | 3.2 | Table test; recursive `~DEFAULT_BRANCH` test; the existing literal-string test still passes. |
| FR-004 guide section | 3.3 | Guide-section test; reading the section against 3.4 to 3.6. |
| FR-005 audit per repo | 3.4 | Six files exist with every block filled; `END` and `START` set; tips recorded. |
| FR-006 preflight, producer search, existing list | 3.4, 3.5 | Audit blocks; ledger gates G2, G3, G6, G7. |
| FR-007 apply order, create-only-if-absent, SHA, 403 stop, drift check | 3.6 | Runbook R0 to R7; ledger row per ruleset with id, date, SHA. |
| FR-008 handoff reaches GitHub, SHA-pinned | 3.7 | Issue 837 comment URL recorded; links contain the pushed SHA. |
| FR-009 quotes and ids in the pull request body | 3.7 | The body contains the verbatim "Decided for this work" block and the ledger table. |
| FR-010 `Refs #837`, `/sc:pr-submit --monitor 3`, nothing merges | 3.7 | Body's last line; `gh pr view` shows open. |
| Done condition (INV-014) | 3.5 header, 3.7 | Restated per-repo table in the body; Clay's acceptance quoted or listed as open. |
| Invariant findings INV-001 to INV-016 | 3.1 to 3.7 | Each is a gate, a runbook step, a record block or a listed open decision; none is left only in the debate files. |

Quality checks before the commit: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `make lint`, `git diff --stat` shows only the staged list of Phase 2, and `git status` shows nothing under `.claude/` or `.dev/issues/` staged. After Phase 3, for each applied ruleset: the R4 read-back output is in the audit file.

## 8. Expected outcome of this run and what stays open

With the facts in hand today, the gates give this result. The state of the world can change before Phase 3; the runbook re-evaluates.

| Repo | Expected gate result today | Expected end state of this run |
|---|---|---|
| CPA-Manager-Plus | G3 fails (the installations read cannot run, so the audit is `BLOCKED` until it is cleared); G4 fails for the mirror (no acceptance quoted); G6 depends on the producer search. | Audit, ledger row `SKIP(G3)` for every ruleset, runbook ready. Nothing written to the repo. |
| IronOrca | Same as above; `aidev02` fails G5. | Same. |
| coder_orca | G3 fails the same way; the full role would otherwise pass G4; the tag ruleset is a fixed skip (G6). | Audit, ledger `SKIP(G3)` for `protect-main`, `SKIP(G6)` for the tag ruleset. |
| IronHands-CLI, irondots, ironops-marketplace | G1: `HANDOFF`. | Handoff text and audit posted on issue 837; nothing written to the repos. |

So the expected result of this run is: the files, test and guide changed and pushed, six audit records, the ledger, the handoff posted for Ryan, the runbook ready, the pull request open with `Refs #837`, **no ruleset applied**, and `outcome: partial`. This is the safe default of decisions 3 and 4, not a failure. It becomes an apply as soon as the clearances below exist; the runbook can then be run by the same session or by Clay.

Clearances that unlock Phase 3, each a written statement quoted in `issue-summary.md`. These are the decisions only a person can make:

| Clearance | Yes means | No or silence means |
|---|---|---|
| Clay accepts the installations check as not runnable with his token (or an org owner posts the output of `gh api --paginate orgs/IronbellyOrg/installations`) | G3 can pass on the three Clay repos; the rulesets that pass the other gates are applied. | Every ruleset on the three Clay repos stays `SKIP(G3)`. |
| Clay accepts the mirror rule set (no pull-request rule; direct pushes still allowed) on the fork `main` of IronOrca and CPA-Manager-Plus | G4 passes for the forks and the mirror is applied when `ahead_by` is 0. | The forks' branch rulesets stay skipped and reported; the tag rulesets are decided separately. |
| Clay says yes to protecting `aidev02` in IronOrca | `protect-aidev02.json` is created and may be applied. | The file does not exist. |
| `ironbelly` confirms admin on the three Clay repos | `ironbelly` is a named revert owner. | Clay is the only revert owner and must be reachable. |
| Clay accepts the restated done condition | The issue can be closed by hand once Ryan reports. | The issue stays open with the table as its status. |

Still UNVERIFIED and not answerable by design: whether the Sync fork button is refused under a `pull_request` rule (E-6), whether `clayphi`'s token can `POST` rulesets, whether a duplicate ruleset name is accepted by the API, and whether the mirror's bypass actor is accepted without a `pull_request` rule (answered by R1).

## 9. Out of scope

- Any write to IronHands-CLI, irondots or ironops-marketplace, or to the archived IronHands repo, or to any repository outside IronbellyOrg.
- A render tool, an audit script, a reconciliation framework, a second-pass-zero-changes check, or retry machinery beyond "list, then create if absent".
- Protecting `dev`, `release/v*` and `dot/*`; required approvals or status checks; changing IronClaude's three live rulesets or JSON files.
- Organisation-level rulesets (plan availability UNVERIFIED) and moving the files out of IronClaude.
- Making Sync fork work: the design only tests it after a mirror is applied and reverts if it is refused.
- Merging the pull request, closing issue 837, or editing `.claude/`.

## Revision 1: findings of the plan review that this design must now carry

The first plan built from this design was reviewed on 2026-11-26 (report `.dev/reflect/pre-TASK-WF-design-20261126-130537-20261126131151/REPORT.md`). The review found four Blocking findings, which the new plan must fix, and thirteen Medium findings, which the new plan must not repeat. Where this section and sections 1 to 9 differ, this section wins. It adds no phase and no new scope; it changes where evidence is kept, what a few acceptance checks say, and what the runbook contains.

### Blocking findings to fix

- **M-01, wrong test ids.** The pytest test `test_branch_rulesets` is parametrized on the two names `name,ref`, so pytest prints ids that join both values. The acceptance check of the task that extends `tests/docs/test_branch_protection_rulesets.py` must name `test_branch_rulesets[protect-master-refs/heads/master]` and `test_branch_rulesets[protect-integration-refs/heads/integration]`, or name the test functions, and its verifier is `uv run pytest tests/docs/test_branch_protection_rulesets.py --collect-only -q`, whose output must list them.
- **M-02, lost `make lint`.** Section 4 names `make lint` as the last Phase 1 check and section 7 as a pre-commit check. The test task keeps its one-file `uv run ruff check tests/docs/test_branch_protection_rulesets.py`. A task of Phase 1 or 2 of the plan must also run `make lint` and record its output; a failure on files that this change does not touch is recorded as pre-existing and named, never hidden. (`make lint` runs `lint-architecture` and a repository-wide `ruff check .`.)
- **M-03, private detail must not reach GitHub.** `IronbellyOrg/IronClaude` is public; `IronbellyOrg/Coder` is private (checked with `gh repo view` and `gh api` on 2026-11-26). `.dev/tasks` is always staged and pushed, so everything that follows holds for the plan package, the archived superseded plan, every log and QA output written under `.dev/tasks`, the pull request body and every issue comment.
  - The four state files of section 2 stay where section 2 puts them: `.dev/issues/837/audit/<repo>.md`, `.dev/issues/837/gates.md`, `.dev/issues/837/handoff-ryan.md` and `.dev/issues/837/apply-runbook.md`, never staged. Task outputs that the design places there are written there and not under the package `artifacts/` folder; the package `artifacts/` folder holds only the codegraph grounding note. This also removes the plan's earlier contradiction with section 2.
  - The producer search for coder_orca reads the private repository's release tooling to confirm that it deletes tags (E-2 of the merged requirements). The task reads it without printing or saving its lines: only a neutral conclusion is recorded in any file under `.dev/` that could be staged and in anything posted to GitHub: "release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca". Verbatim lines, line numbers, file names, folder names and function names of that tooling are written only to `.dev/issues/837/private/coder_orca-producer-evidence.md`, which is never staged. The file name, folder and function names themselves are not written in the plan: the plan points to E-2 of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md` for them.
  - The staging list of the runbook does not include the brainstorm folder. Story step 9 names only the changed files and `.dev/tasks`; the folder describes the private tooling (E-2 and D5 of the merged requirements). Whether to publish it is the user's decision and the runbook says so.
  - Part one of the runbook gets a pre-stage guard: print `gh repo view IronbellyOrg/IronClaude --json visibility -q .visibility`, then run `git diff --cached` and `grep -n -f .dev/issues/837/private/guard-patterns.txt` over the staged files; any hit stops the staging. `guard-patterns.txt` is a never-staged file that a Phase 1 task writes from E-2 (the file name, the folder name and the names of the tag-deleting functions). The only path the guard may exclude is the archived superseded plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/`, which names that tooling in two lines and cannot be edited; the runbook lists this as an open item for the lead.
- **M-04, runbook part one must always run.** Part one of the apply runbook (staging, the pre-stage guard, recording the pushed SHA, posting the handoff and the draft ledger as a comment on issue 837) runs right after the commit and push, whatever the ledger decides. Only part two, the gated apply, waits for the pull request monitor and for a ledger decision of `APPLY`. The expected run applies nothing (section 8), so part one must not depend on `APPLY`.

### Medium findings the new plan must not repeat

- **M-05.** The ledger header cites `.dev/issues/837/accuracy-check.md` line 13 (PR 844 merged, commit 206abea1c; live ruleset 28081842 with `update`) as the verification the lead asked for, and states the rule: if the `update` rule on the release-tag ruleset is not settled, every tag row is `SKIP(not settled)` and only the branch rulesets are copied.
- **M-06.** The ledger uses only `APPLY`, `SKIP(<first failing gate>)` and `HANDOFF` (section 3.5). No `PENDING` value: G8 and G9 give `SKIP` until they hold.
- **M-07.** The runbook carries the consequence of section 3.1 for a refused mirror bypass actor: drop the actor from the mirror file and change the file, the test, the guide and D4 together before anything is applied.
- **M-08.** The handoff task depends on the guide task, because it takes its commands from the guide section.
- **M-09.** With the state files in `.dev/issues/837/`, the R0 to R7 results go into the audit file and the ledger exactly as section 3.6 says; there is no separate apply-results file.
- **M-10.** The `<PUSHED-SHA>` placeholder is replaced in the text posted as the issue comment, not in a committed file. After any later push, the pinned links are re-pinned in a new comment (R6).
- **M-11.** The pull request body task names the path of the merged requirements: `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md`, read locally, section "Done condition for this pull request".
- **M-12.** The guide check in the test iterates over the `.json` files that exist in `other-repos/`, so an absent optional `protect-aidev02.json` does not fail it; the guide section lists the path of `protect-aidev02.json` in its note on `aidev02`.
- **M-13.** The acceptance check of the runbook task says which variables are filled now (`REPO`, `PARENT_OWNER`, `BRANCH` and the file the ledger decides); `ID`, `END` and `START` are set on apply day.
- **M-14.** Every write command of the runbook names its repository explicitly, including the scratch-clone pushes of R1: `git push https://github.com/IronbellyOrg/$REPO.git ...` from the scratch clone.
- **M-15.** IronHands-CLI is a fork. The Targets table and the handoff treat a fork of a Ryan repo like a fork of a Clay repo: the mirror file only when `ahead_by` is 0 and Clay's written acceptance (G4) is quoted, otherwise the full file; the handoff links both role files.
- **M-16.** The ledger has one row per ruleset; the pull request body has one row per repository that summarises its rows.
- **M-17.** The count of `v*` refs reads every page (`--paginate`), and the handoff text for the tag ruleset says: included where the repository has no `v*` tag and the read-only workflow search found no tag mover, because there is then nothing to break.

## Revision 2

- Replaces package: TASK-WF-designRev1-20261126-141220 (archived under .dev/tasks/archive/TASK-WF-designRev1-20261126-141220/)
- Review report: .dev/reflect/pre-TASK-WF-designRev1-20261126-141220-20261126141617/REPORT.md
- Fix map: ./artifacts/revision-log.md (diff: ./artifacts/plan.diff)
