# Design: multi-repo ruleset rollout tool (issue 838)

Grounding: index_state: fresh (checked_at 2026-11-26T13:23:59Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/issue-838). `codegraph_node` with `symbolsOnly:true` located the patterns in `scripts/merged_pr_log.py` and `scripts/worktree_cleanup.py`; every symbol cited below was then confirmed with Grep or Read. Graph rows were treated as leads only.

Type: architecture. Format: spec. Input: `.dev/brainstorms/20261126-120633-apply-branch-rulesets-ironbellygroup/merged-requirements.md` (called "the requirements" below; ids FR-n, S-n, G-n, AC-n, Decision n, INV-n and O-n are theirs).

## 1. Status of the input

The requirements ended with adversarial status `partial`: agreement passed the threshold, but five HIGH invariant findings (INV-001, INV-003, INV-009, INV-010, INV-037) were open, and the merge added text for them that was not debated. This design implements that text as written and lists in section 11 every place where it had to choose, fill a gap or depart from the requirements wording. Those items need the owner's review before `/sc:implement` is trusted on them.

## 2. Delivery boundary

This design delivers the tool, its tests and its operator page. It does not run any live call against an IronbellyGroup repo, and the implementation steps must not either.

| Delivered by the pull request | Done afterwards by the owner (Clay), following the operator page |
|---|---|
| `scripts/org_rulesets.py` with `plan`, `apply`, `verify` | Step 0 live read, per-repo 90-day and tag checks |
| `tests/org_rulesets/` (offline, fake runner) | The owner statements and approvals the gates need (G2, G3, canary exit) |
| `docs/developer-guide/branch-protection-multi-repo.md` and two links | The canary, then the other repos one at a time, then `verify --all` |

Reason: the requirements make Clay the person who runs each apply, and several gates need a written statement or confirmation only he can give (INV-009, INV-010, Decision 3, canary exit). Clay's answer in `issue-summary.md` is the go for the 17 repos, not a waiver of those gates (O-1). So the pull request refers to issue 838 and says what is left; it does not close it.

## 3. Existing structure the design builds on

| Existing thing | What it gives the design |
|---|---|
| `.github/rulesets/protect-master.json`, `protect-integration.json`, `protect-release-tags.json` | The only source of rule content. Never edited (AC-4). |
| `docs/developer-guide/branch-protection.md` | The apply order, check commands and break-glass steps to adapt. Its four strings pinned by `tests/docs/test_branch_protection_rulesets.py` stay untouched. |
| `scripts/merged_pr_log.py` | The script shape to copy: stdlib only, `main(argv, env, get, put, now)` taking every outside dependency as an argument, and an `if __name__ == "__main__"` guard. |
| `scripts/worktree_cleanup.py` | The runner shape to copy: a `Runner` whose `check_allowed` is a positive allowlist, a `RefusedCommand` error, a `CommandRecord` log of every command, and a `Result(returncode, stdout, stderr)`. Reused as a pattern, not imported, because its allowlist is specific to its own verbs. |
| `tests/merged_pr_log/` | The test layout to copy: `__init__.py` plus a test file that loads the script with `importlib.util.spec_from_file_location` (scripts/ is not a package). |
| `pyproject.toml` | Python 3.10 target, ruff rules `E,F,I,N,W,TID`, pytest `testpaths = ["tests"]`. `.dev/` is excluded from ruff. |
| `docs/developer-guide/documentation-index.md` | Lists `branch-protection.md` at two places; the new page is added beside both. |

No `tests/org_rulesets/`, `scripts/org_rulesets.py` or `docs/developer-guide/branch-protection-multi-repo.md` exists yet (checked by listing the folders).

## 4. Architecture

```text
                      .github/rulesets/*.json  (IronClaude, read only)
                                  |
                                  v
  names.txt --init-->  [ render ]  profile + branch -> ruleset body, payload digest
                                  |
   targets.json  <--- [ store ] --+--  single writer, lock file, rev check, atomic rename
   (per repo state)        ^
                           |
  gh api (read) -> [ facts + gates ] -> plan     (read only; writes facts, checks, pending->checked)
  gh api (read/write) -> [ apply ]   -> apply    (one repo; snapshot, write, read back, rollback mode)
  gh api (read) -> [ verify ]        -> verify   (one repo, or --all)
                           ^
          every gh call goes through [ runner ]: allowlist by method + path, call log,
          read-only mode for plan and verify
```

One file, `scripts/org_rulesets.py`, in this order of sections: constants and profile table; `render`; `Runner`; targets store; facts and gate evaluation; `apply`; `verify`; command line and `main`. One file matches the repo's two existing scripts and keeps one import in the test. The expected size is about 900 lines (an estimate, not a measurement).

## 5. Data model

### 5.1 Targets file

JSON, passed with `--targets`; this work's copy is `.dev/issues/838/rollout/targets.json`, which is never staged, so private repo names stay out of git. The script holds no repo or org name (FR-5, FR-6).

```text
{ "schema": 1,
  "org_facts": { "login", "plan", "facts_read_at", "installations": [...], "inventory": {family: pass|403} },
  "applier": { "login", "checked_at" },
  "source": { "source_sha", "tag_rule_settled": true|false },
  "repos": [ { name, default_branch, branches_present[], archived, admin, pushed_at,
               facts_read_at,
               tag_profile: tags-full|tags-no-update, tag_check{result, checked_at, evidence},
               push_check{result: pass|blocked|incomplete, cutoff, source, checked_at, evidence},
               owner_evidence_sha256, payload_sha256,
               status, reason, intent{action, ruleset, payload_sha256, snapshot_path},
               ruleset_ids{name: id}, last_verified_bodies{name: body},
               approved_by, approved_at, rev, coverage (derived, written by verify),
               scratch_ruleset_ids (canary only) } ] }
```

Rules the schema test pins: unknown status rejected; `name` must be in the allowlist and compared case-insensitively, stored in GitHub's canonical spelling; `ruleset_ids` keys must be in the repo's rendered set (1 to 4 rulesets); `push_check.result: pass` together with an `incomplete` finding is rejected (INV-009); a missing field is rejected.

### 5.2 Status machine

| From | To | Written by | Condition |
|---|---|---|---|
| (new) | `pending` | `plan --init-from names.txt` | name appears in the allowlist file |
| `pending`, `deferred` | `checked` | `plan` | Step 0 facts fresh; G1, G2, G3, G4, G7 pass |
| `pending`, `checked` | `deferred` | `plan` | archived, no admin, empty repo, push check `blocked` or `incomplete`, tag check unresolved; `reason` recorded |
| `checked` | `applied` | `apply` | every ruleset of the set written and read back by id |
| `checked` | `partial` | `apply` | stopped after at least one write |
| `applied` | `verified` | `verify` | full-body compare passes |
| `partial`, `applied`, `verified` | `rolled-back` | `apply --rollback` | per S-4 |
| `partial`, `rolled-back` | `pending` | `plan --reset <repo> --by <login> --reason <text>` | recorded review (S-6), then a fresh Step 0 read moves it on to `checked` |

`coverage` is never typed: `verify` derives `strict` (all selected branch rulesets and `tags-full` active and body-verified), `exception` (`tags-no-update`), `interim` (branch rulesets only) or `none`. `applied` is never reported as success (FR-5).

### 5.3 Owner evidence file

A per-repo file the owner writes by hand, `.dev/issues/838/rollout/<repo>-owner.json`, read-only for the script: `push_statement{by, at, text}` (pushes by named people were made by hand, INV-010), `accepted_pushers[]`, `tag_statement{by, at, text}` (who moves tags and from where), `tag_exception{approved_by, approved_at, reason}`, `follow_up_owner`. The script stores the file's sha256 in the repo entry, so an edited statement invalidates an earlier approval.

## 6. Interfaces

### 6.1 Command line

```text
org_rulesets.py plan   --org O --targets T [--repo R ...] [--init-from names.txt] [--reset R --by L --reason TEXT]
org_rulesets.py apply  --org O --targets T --repo R --approved-by L --confirm DIGEST [--rollback disable|delete|restore]
org_rulesets.py verify --org O --targets T (--repo R | --all)
```

`--org` is required with no default and the script refuses the upstream org name in any letter case (FR-6). `apply` takes exactly one `--repo` and refuses a list. Exit codes follow `worktree_cleanup.py`: 0 ok, 64 usage, 69 failure; a gate refusal is 69 with the failed gate named.

### 6.2 Runner

`Runner.run(argv, stdin=None) -> Result` accepts only `gh api` calls whose method and path match one allowlist pattern, plus `git rev-parse HEAD` and `git status --porcelain -- .github/rulesets` for the source commit. Every accepted call is appended to `Runner.commands`. A runner built for `plan` and `verify` refuses POST, PUT and DELETE before any process starts. Payloads go in on stdin (`--input -`). Tests pass a fake with the same `run` signature and canned answers.

| Family | Methods and paths (all under `repos/<org>/<repo>` unless noted) |
|---|---|
| Org and identity | GET `orgs/<org>`, GET `orgs/<org>/repos`, GET `orgs/<org>/installations`, GET `user` |
| Repo facts | GET `repos/<org>/<repo>`, GET `.../branches/<b>`, GET `.../branches/<b>/protection`, GET `.../hooks`, GET `.../keys` |
| History | GET `.../activity`, GET `.../commits`, GET `.../commits/<sha>/pulls`, GET `.../git/matching-refs/tags/v` |
| Files to scan | GET `.../contents/<path>` for `.github/workflows` and release scripts |
| Rulesets read | GET `.../rulesets`, GET `.../rulesets/<id>`, GET `.../rules/branches/<b>` |
| Rulesets write (`apply` only) | POST `.../rulesets`, PUT `.../rulesets/<id>`, DELETE `.../rulesets/<id>` |

No call targets `IronbellyOrg/IronClaude` in write form, and the script never posts an issue comment: `verify` prints the one-line comment text for issue 838 and the operator posts it (DD-5). A test asserts that no recorded write names ruleset ids 28081842, 28081844 or 28081845.

### 6.3 Functions (names and contracts, not code)

| Function | Contract |
|---|---|
| `render(profile, branch=None)` | Pure. `branch` profile: load `protect-master.json`, set `name` to `protect-<branch>` and `conditions.ref_name.include` to `["refs/heads/<branch>"]`, change nothing else. `tags-full`: the tag file. `tags-no-update`: the tag file without `update`. Unknown profile or bad branch name (empty, contains `*` or `~`, starts with `refs/`) raises. Output never contains `~DEFAULT_BRANCH` (FR-1 to FR-3). |
| `branch_set(facts)` | Default branch plus `master` and `integration` where they exist, deduplicated; records `integration: absent` (FR-4). |
| `payload_digest(rendered)` | sha256 of the canonical JSON (sorted keys, fixed separators) of all rendered bodies of the repo, in apply order. |
| `Store.update(repo, owner_fields, fn)` | The one write path (FR-5a): create `targets.json.lock` exclusively, re-read, check `rev`, change only the fields the caller owns, write a temp file in the same folder, rename over the original, remove the lock. A held lock or a stale `rev` refuses. One-machine lock only. |
| `read_facts(runner, org, repo)` | Step 0 reads for one repo (section 7.1). |
| `check_push(runner, repo, branches, now)` | Section 8.1. Returns `pass`, `blocked` or `incomplete` with evidence. |
| `check_tags(runner, repo, owner_file)` | Section 8.2. |
| `gates(entry, org_facts, source, now)` | Evaluates G1 to G4, G7 and returns a list of failures with names. |
| `snapshot(runner, repo, branches)` | S-1: write-once `<repo>-before.json` with full ruleset bodies and branch protection (404 recorded as `"none"`). |
| `apply_repo(...)`, `rollback_repo(...)`, `verify_repo(...)`, `verify_all(...)` | Sections 7.2 to 7.4. |
| `compare_bodies(rendered, remote)` | FR-10: compares `name`, `target`, `enforcement`, `conditions`, `bypass_actors` as a set and `rules` as a set of type plus complete parameters. Ignores only a fixed list of server metadata keys (`id`, `source`, `source_type`, `node_id`, `created_at`, `updated_at`, `current_user_can_bypass`, `_links`), to be confirmed from the canary's real response and tested. Any other extra key, rule or bypass actor is a mismatch. |

## 7. Flows

### 7.1 `plan` (read only)

1. Read the org (`orgs/<org>`), print login and plan name, require the login to equal `--org` case-insensitively, list org repos and report allowlisted repos not found and live non-archived repos not on the list (never enlarging it).
2. Capability inventory: one read-only call per family, recording pass or 403; a failed family blocks the gates that need it. Record the applier login and admin permission (G8).
3. Source commit: `git rev-parse HEAD`, refuse when `.github/rulesets/*.json` has uncommitted edits, confirm `deletion`, `non_fast_forward` and `update` are in `protect-release-tags.json`; if not, `source.tag_rule_settled` is false and only branch rulesets are planned (O-3).
4. Per repo: canonical owner and name, `archived`, `default_branch`, `pushed_at`, `permissions.admin`, branch presence (confirming the default branch exists, else `deferred: empty-repo`), `facts_read_at`.
5. Run `check_push` and `check_tags`, read hooks and keys with exit-status checks (a non-zero exit is `incomplete`, never "0", INV-012), evaluate gates, write the result and the status transition through `Store.update`.
6. Print the payload digest the operator must confirm at `apply`.

### 7.2 `apply` (one repo)

1. Refuse unless status is `checked`, `facts_read_at`, both checks' `checked_at` and the org read are under 24 hours old (UTC), the recomputed digest equals the planned one, `--confirm` equals that digest, G6 holds (no repo is `applied` but not `verified`, none is `partial`), and G8 holds. Record `approved_by` and `approved_at`.
2. Snapshot (S-1). Classic protection on a branch in the set sends the repo to review before any write.
3. List rulesets with `--paginate`. A same-name ruleset is managed only if its id is in `ruleset_ids`; unrecorded same-name, several candidates, inherited or org-level rulesets go to review and get no PUT (FR-8).
4. In FR-9 order (tags, `integration`, `master`, any other default branch): write the intent entry (action, name, digest, snapshot path); POST or PUT; add the returned id beside the intent; read the ruleset back by id; compare with `compare_bodies`; store the last verified body. A timed-out POST is followed by a new list, and a matching same-name ruleset is adopted; a POST is never repeated blindly. Before any PUT, read the ruleset by id and compare it with the stored verified body; a difference stops the repo.
5. A non-success response stops the repo with status `partial`; a 403 after Step 0 passed stops the whole run (S-6). Success sets `applied`.

`apply --rollback disable|delete|restore` (DD-2): `disable` is a PUT of `enforcement=disabled`; `delete` removes only ids in `ruleset_ids`; `restore` PUTs the full snapshot body. Each reads back and compares complete bodies, records partial failures, never touches unrecorded or classic protection, and sets `rolled-back`.

### 7.3 `verify`

For one repo: read each ruleset by id, run `compare_bodies`, set `verified` and `coverage`, write ids, date and check results, print the one-line issue comment (repo, date, ids keyed by ruleset name, tag profile, audit result, coverage, evidence path, any exception or rollback reason).

### 7.4 `verify --all`

Read-only. Reads every allowlisted repo live and prints counts: strict, exception, interim, blocked or incomplete, deferred. Exits 0 only when all 17 are strict (INV-037). It states plainly that the design cannot guarantee 17 of 17.

## 8. Check logic

### 8.1 90-day push check (Decision 4)

- Cutoff: one UTC value, now minus 90 days, recorded, applied by timestamp filter to both sources (INV-020). `time_period=quarter` is not trusted as 90 days until the canary proves it.
- Primary source: `activity?ref=refs/heads/<b>&time_period=quarter`, paginated, counting activity types `push`, `force_push` and `branch_deletion` as direct pushes and ignoring `pr_merge` (UNVERIFIED on Team-plan private repos; the canary must show complete coverage before other repos rely on it).
- Fallback: `commits?sha=<b>&since=<cutoff>` and, for each commit, `commits/<sha>/pulls`; a commit with no merged pull request is a direct push. More than 500 lookups (DD-8, a chosen parameter) gives `incomplete`.
- Workflow scan: read `.github/workflows` for `git push`; a hit blocks the repo like a bot push.
- Result: `blocked` for any bot or workflow push; `incomplete` for unavailable history, truncated pagination or an unclassifiable commit; `pass` for zero direct pushes, or for named human pushes only when the owner file holds `accepted_pushers` and a `push_statement` that they were made by hand (INV-010). `incomplete` is never turned into `pass` by any text (INV-009); it leaves the repo `deferred: incomplete-audit`.

### 8.2 Tag check (Decision 3)

List `v*` tags with `git/matching-refs/tags/v` (paginated). Scan `.github/workflows/`, a root `Makefile`, `scripts/` and root release files for tag-mutating patterns (`git tag -f`, `--force` on a tag push, `--delete`, `:refs/tags/`, `gh release delete`, re-tagging, floating tags such as `v1`). The result is `tags-full` only when the scan is clean and the owner file has a `tag_statement` naming who moves tags and from where; an empty tag list proves nothing. A hit or a statement that tags move gives `tags-no-update` only with `tag_exception` (approver, time, reason). A repo that deletes tags waits unless an authorized branch-only interim state is recorded; interim never counts as complete.

## 9. Test design

Folder `tests/org_rulesets/` with `__init__.py`; files: `test_render.py`, `test_store.py`, `test_gates.py`, `test_apply.py`, `test_verify.py`, `test_runner.py`, `test_page.py`, `conftest.py` (the fake runner and synthetic repo facts). Synthetic names only (for example `acme-one`); no real private repo name appears in any tracked file.

| Requirement | Test |
|---|---|
| FR-1 | Rendered `master` and `integration` bodies equal the two existing files as parsed JSON |
| FR-2, FR-3 | Every profile renders; unknown profile raises; `tags-no-update` has exactly `deletion` and `non_fast_forward`; bad branch names rejected; no `~DEFAULT_BRANCH` in any rendered output |
| FR-4 | Three cases: `master` only; `main` with no `integration`; `integration` default with `master` present; empty repo is `deferred` |
| FR-5, FR-5a | Missing field, unknown status, name off the allowlist, stray `ruleset_ids` key, `pass` with `incomplete` are rejected; a `plan` that read before `apply` recorded an id never drops it; held lock and stale `rev` refuse |
| FR-6 | Every recorded call has full owner and repo; none contains `SuperClaude-Org` in any case; upstream `--org` refused |
| FR-7 | `plan` records no POST, PUT or DELETE; `apply` with two repos or a non-`checked` repo exits 69; stale facts, stale checks, digest mismatch and dirty rule files refuse |
| FR-8, FR-9 | No second POST; unrecorded same-name gets no PUT; timed-out create re-lists first; changed baseline stops a PUT; recorded call order is tags, `integration`, `master` |
| FR-10 | Any difference exits non-zero, including an extra rule and an extra bypass actor; the ignored-key list is tested |
| S-1, S-4 | Snapshot has full bodies even when the list returns summaries; write-once; rollback deletes only recorded ids and restores from the snapshot |
| Failure cases | Unavailable history, truncated pagination, duplicate rulesets, partial application, full-body mismatch, zero writes on a second run |
| AC-4, AC-6 | No write names ids 28081842, 28081844, 28081845; `tests/docs/test_branch_protection_rulesets.py` is untouched and passes |
| FR-11 | `test_page.py` pins the page's `OWNER`/`REPO` variables, its links, and that the existing guide and index link to it |

Command: `uv run pytest tests/org_rulesets/ tests/docs/test_branch_protection_rulesets.py -v`, then `make lint`.

## 10. Files

| File | Change |
|---|---|
| `scripts/org_rulesets.py` | New |
| `tests/org_rulesets/__init__.py`, `conftest.py`, `test_*.py` | New |
| `docs/developer-guide/branch-protection-multi-repo.md` | New operator page: variables, Step 0, canary, per-repo order, owner file format, rollback and break glass, the exit-status rule, the `verify --all` end state |
| `docs/developer-guide/branch-protection.md` | One link line to the new page; no command changes |
| `docs/developer-guide/documentation-index.md` | Two link lines beside the existing entries |
| `.dev/issues/838/rollout/` | Created by the operator at run time; never staged |

## 11. Design decisions and items for the owner

| Id | Decision | Why it is a decision |
|---|---|---|
| DD-1 | `plan` owns the facts, the two checks and the `pending, deferred -> checked, deferred` transition; `apply` and `verify` own the rest. | The requirements say `apply` needs status `checked` but name no writer for it, and FR-5a says `plan` writes only `facts*`. This amends FR-5a. Owner to confirm. |
| DD-2 | Rollback is `apply --rollback`, not a fourth subcommand. | FR-7 names three subcommands; S-4 needs a repeatable path. |
| DD-3 | Human statements live in a read-only owner file whose sha256 is stored in the entry. | Keeps a single writer for `targets.json` and binds approvals to evidence (INV-007). |
| DD-4 | Approval is `apply --approved-by L --confirm DIGEST`. | The requirements bind approval to the digest but give no input path. |
| DD-5 | The script prints the issue comment and never posts. | FR-10 says "drafts"; keeps every write inside the target org. |
| DD-6 | One module, a runner allowlisted by method and path, read-only mode for `plan` and `verify`. | Matches `worktree_cleanup.py` and makes FR-7's no-write test enforceable. |
| DD-7 | Python 3.10, standard library only. | `pyproject.toml` target. |
| DD-8 | Commit-lookup cap of 500, over it `incomplete`. | A chosen parameter; the requirements only say truncation is `incomplete`. |
| DD-9 | The files scanned for tag moves are fixed in section 8.2. | The requirements say "workflows and release scripts" without a list. |
| DD-10 | Tests use synthetic names; `targets.json` is never staged. | Private repo names must not enter git. |
| DD-11 | `plan --init-from names.txt` creates the entries. | Hand-writing the targets file is error-prone and bypasses the writer. |

Still open for the owner, unchanged from the requirements: whether the commit-and-pull-request fallback may only raise `blocked` or `incomplete` (INV-011); whether `verify` should flag "source changed" for repos done before a later rule change (INV-008); the substitute path when the installations read fails for the operator (INV-038); whether Clay may authorize a repo on incomplete evidence (INV-009, not assumed); and the canary rule, which departs from the issue's "most recent push first" (Clay may overrule it).

## 12. Traceability

| Requirements | Design section |
|---|---|
| FR-1 to FR-4 | 6.3 `render`, `branch_set`; 9 |
| FR-5, FR-5a | 5.1, 5.2, 6.3 `Store.update` |
| FR-6 | 6.1, 6.2 |
| FR-7 | 6.1, 7.1, 7.2 |
| FR-8, FR-9 | 7.2 |
| FR-10 | 6.3 `compare_bodies`, 7.3, 7.4 |
| FR-11 | 10 |
| S-1 to S-6 | 6.3 `snapshot`, 7.1, 7.2 (rollback), 8 |
| G1 to G8 | 6.3 `gates`, 7.1 steps 1 to 3, 7.2 step 1 |
| Decisions 1 to 6 | 4, 6.3, 8.1, 8.2, 7.1 |
| AC-1 to AC-7 | 7.4, 7.3, 9, 10 |
| O-1 to O-3 | 2, 5.1, 7.1 step 3 |

## 13. Risks of this design

| Risk | Mitigation |
|---|---|
| The activity API or `commits/<sha>/pulls` do not behave as assumed on private Team repos | Both are marked UNVERIFIED; the canary must prove coverage; a failure gives `incomplete`, not `pass` |
| The tool is large for a single story | Section 4 keeps one module; the plan phases it: render and runner, store and gates, apply and rollback, verify, page and index |
| A one-machine lock does not stop two operators on two machines | Stated in the page; one applying process per repo is an operator precondition |
| A wrong ignored-key list in `compare_bodies` hides a real difference or flags a harmless one | The list is fixed from the canary's real response and tested both ways |
| The requirements' NOT DEBATED text is wrong in a detail | Section 11 lists each choice; the owner reviews before the live rollout |
