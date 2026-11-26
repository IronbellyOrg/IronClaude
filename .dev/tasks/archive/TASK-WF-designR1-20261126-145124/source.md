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

## Revision 1 (regenerate route of the plan review)

The first plan generated from this design (`.dev/tasks/to-do/TASK-WF-design-20261126-132702`, now archived once this plan passes its gate) was reviewed and failed with 9 Blocking, 12 Medium and 3 Note findings. This revision lists what the new plan must do. It does not change the design text above. Every addition below is a proposal for the owner's section 11 review, like DD-1 to DD-11 (spec line 9).

### R1.1 Blocking findings the new plan must fix

**R1-B1 (was MF-1, Blocking): The allowlist has no source after `plan --init-from`.**
- Defect: Three steps consume an allowlist, but no task stores it or reads it from the command line. So after `--init-from` the check "`name` must be in the allowlist" has no defined input, and a repo added to `targets.json` by hand can pass it.
- Required in the plan: - Task 5: `init_entries` writes a top-level `allowlist` (canonical spelling) into `targets.json`. `OWNERS` lets only the `--init-from` path write it. - Task 4: `validate_targets` reads the allowlist from the file and rejects any entry whose name is not on it. - Tasks 7 and 14: `report_allowlist` and `verify_all` use the same field. - Verifier: a `test_cli.py` case where `apply --repo <hand-added name>` exits `EXIT_FAILED` with no write call. - Spec 5.1 has no such field, so record the field as a decision for the owner's section-11 review (spec:9).

**R1-B2 (was MF-2, Blocking): A tag-deletion hit gets `tags-no-update`, which still blocks deletion.**
- Defect: Task 9 maps any scan hit, deletion patterns included, to `tags-no-update` whenever a `tag_exception` exists. That profile keeps the `deletion` rule. The spec says a repo that deletes tags waits unless an authorized branch-only interim state is recorded.
- Required in the plan: - Task 9 separates the deletion patterns (`--delete`, `:refs/tags/`, `gh release delete`) from the other tag-moving patterns. A deletion hit returns its own result that keeps the repo `deferred`, whatever `tag_exception` says. - Task 10 lets such a repo proceed only through the branch-only path of MF-9, and only when an owner authorization for a branch-only interim is recorded. - The owner evidence file has no key for that authorization today (previous plan line 109, spec:99). Add one, for example the proposed name `branch_only_interim{approved_by, approved_at, reason}`, and record it as a decision for the owner's review. - Acceptance: a deletion hit with a `tag_exception` stays `deferred`. With the authorization, the repo plans branch rulesets only and its coverage is `interim`.

**R1-B3 (was MF-3, Blocking): The stored owner-evidence hash is never compared before `apply` writes.**
- Defect: The spec stores the owner file's sha256 "so an edited statement invalidates an earlier approval" (spec:99). The plan only computes and stores that hash. Task 12's precondition list never re-reads the owner file or compares the hash, so an owner who edits or withdraws a statement after `plan` cannot stop `apply`.
- Required in the plan: Task 12 adds a precondition. It calls `load_owner_evidence` on `<repo>-owner.json` and refuses, naming the gate, when the file's sha256 differs from the entry's `owner_evidence_sha256`. Acceptance: editing one character of the owner file after `plan` makes `apply` refuse with zero write calls.

**R1-B4 (was MF-4, Blocking): `verify --all` can report the rollout done for an empty or short set of repos.**
- Defect: Task 14 exits 0 "only when every repo is strict" and tests only "all repos strict". An empty or 16-repo set satisfies that too, while the spec exits 0 only when all 17 are strict.
- Required in the plan: `verify_all` exits 0 only when the allowlist from MF-1 is non-empty and every allowlisted repo is read and strict. The strict count must equal the allowlist size, which is 17 for this rollout. Acceptance cases: an empty population exits non-zero; 16 of 17 strict exits non-zero; 17 of 17 strict exits 0. This change depends on MF-1.

**R1-B5 (was MF-5, Blocking): Task 5's `OWNERS` for `plan` makes Task 10's acceptance impossible to pass.**
- Defect: Task 5 gives `plan` only "the `pending, deferred -> checked, deferred` status transition", with no `reason` or reset fields, and a write outside the owned fields raises. Yet Task 10 requires `plan` to record reason `incomplete-audit`, and requires `plan --reset` to record `by` and `reason` and set `pending`, as spec 5.2 requires.
- Required in the plan: - Task 5's `OWNERS["plan"]` lists `reason` and the status transitions spec 5.2 gives to `plan`: new to `pending`; `pending` or `deferred` to `checked`; `pending` or `checked` to `deferred`; `partial` or `rolled-back` to `pending`. - Add the fields `reset_by` and `reset_reason` to the repo entry. Spec 5.1 lacks them, so record them for the owner's review. - Acceptance in `test_store.py`: `plan` performs `checked -> deferred` with a `reason`, and performs the reset, without raising. - DD-1 (spec:223) repeats the short wording, but the spec 5.2 table rows (spec:88 for `pending` and `checked` to `deferred` written by `plan`, spec:93 for `partial` and `rolled-back` to `pending`), spec 6.1's `--reset` (spec:106) and the plan's own Task 10 all need the fuller set, so the fix follows the table. DD-1 is already marked "Owner to confirm".

**R1-B6 (was MF-6, Blocking): Nothing produces the hooks, keys and installations reads that gate G4 judges.**
- Defect: G4 needs hooks, keys and installations reads with their exit status checked, but no task produces them. Task 7 implements only spec 7.1 steps 1 to 4. `plan_command` runs only "the per-repo reads and checks of Tasks 7 to 9". The repo entry has no field for the hooks or keys results. The installations read has no producer and no acceptance check.
- Required in the plan: - Task 7 adds `read_hooks_keys(runner, org, repo)` and, as a proposed name, `read_installations(runner, org)`. Each returns its data with the exit status. - Task 4 adds a repo-entry field for the hooks and keys results. - Task 5's `OWNERS["plan"]` owns that field and `org_facts.installations`. - Task 10 adds the acceptance check "a non-zero installations exit gives G4 `incomplete`". Verifier: `test_facts.py` and `test_plan.py`. - Do not invent a substitute path for a failed installations read. Spec section 11 leaves that to the owner (INV-038, spec:235).

**R1-B7 (was MF-7, Blocking): `apply` never reads the `needs_review` flag, so a repo with classic protection gets written.**
- Defect: The spec stops a repo with classic protection before any write, but the plan only sets a `needs_review` flag in the snapshot, and Task 12 writes after the snapshot without reading it.
- Required in the plan: in Task 12, when the snapshot result has `needs_review`, stop the repo before any write, record the reason, and name it on stderr. Acceptance: a repo whose snapshot finds classic protection gets zero POST and PUT calls.

**R1-B8 (was MF-8, Blocking): The two-repo `apply` exit code differs from the spec's acceptance table (Owner-open O-1).**
- Defect: Task 15 requires `apply` with two repos to exit `EXIT_USAGE` (64), but the spec's test table says it exits 69. The spec's own CLI section treats 64 as usage and says `apply` refuses a list. So the spec contradicts itself, and the plan picked a side without saying so.
- Required in the plan: Task 15 states which code applies and why, and the owner confirms it (O-1). Recommended: keep 64, cite spec:111 and requirements:154, and record that spec:198's 69 applies to the non-`checked` case only. Once confirmed, the acceptance check stays as previous plan line 255. The constants are `EXIT_OK` 0, `EXIT_USAGE` 64 and `EXIT_FAILED` 69.

**R1-B9 (was MF-9, Blocking): An unsettled tag rule blocks every repo instead of planning branch rulesets only (Owner-open O-2).**
- Defect: The spec says that when `protect-release-tags.json` lacks any of its three rules, `tag_rule_settled` is false and only branch rulesets are planned. The plan instead makes `tag_rule_settled` part of G7, requires G7 for `checked`, and has no branch-only plan or apply path. So the `interim` coverage that the plan counts can never be reached.
- Required in the plan: the owner decides (O-2). Recommended: - G7's `tag_rule_settled` gates tag rulesets only. - When it is false, `plan` moves the repo to `checked` for branch rulesets only, Task 12 applies only the branch rulesets, and `verify` reports `interim`. - Once the tag rule is settled, a tag-only apply follows (requirements:306: an `interim` repo "returns to `checked` for a tag-only apply"). - Acceptance: with a tag file lacking `update`, a repo that passes G1 to G4 reaches `checked` with a branch-only set, and `apply` writes no tag ruleset. - Urgency: today `.github/rulesets/protect-release-tags.json:10-12` holds `deletion`, `non_fast_forward` and `update`, so the path matters only if that file changes. That lowers urgency, not the grade.

### R1.2 Decisions this revision takes where the design contradicts itself

- **O-1, exit code of `apply` with two repos.** Use 64 (`EXIT_USAGE`): spec line 111 says `apply` takes exactly one `--repo` and refuses a list, which is a usage error. Spec line 198 (69) is read as the case of a repo that is not `checked`. The plan states this in Task 15 and lists it for the owner.
- **O-2, G7 and the unsettled tag rule.** G7 gates the tag ruleset only. When the tag rule is unsettled (`tag_rule_settled` false), `plan` moves a repo that passes G1 to G4 to `checked` for the branch rulesets only, `apply` writes the branch rulesets only, and `verify` reports the repo `interim`. Once the tag rule is settled, a tag-only apply follows. Today `.github/rulesets/protect-release-tags.json` already holds the update rule (pull request 844 is merged), so this path matters only if that file changes.
- **Fields the fixes add that spec 5.1 lacks** (each is a proposal for the owner): the top-level `allowlist` in the targets file (R1-B1), `reset_by` and `reset_reason` (R1-B5), the hooks and keys result field and `org_facts.installations` (R1-B6), and an owner authorization key for a branch-only interim state of a repo that deletes tags (R1-B2).

### R1.3 Medium findings the new plan must not repeat

Each of these was a real defect of the first plan. The new plan carries the fix in the named task, with its acceptance check.

**R1-M1 (was MF-10, Medium): Rollback entry rules and its CLI options are not stated.**
- Defect: Task 13 states no preconditions, and Task 15 does not say whether `--approved-by` and `--confirm` apply under `--rollback`.
- Required in the plan: Task 13 states that rollback starts only from `partial`, `applied` or `verified` (spec:92), that G6 does not apply, and whether `--approved-by` and `--confirm` are required. Task 15 adds a usage test for `--rollback`.

**R1-M2 (was MF-11, Medium): Snapshot, owner-file and rules locations have no rule.**
- Defect: The CLI has only `--targets`, while Task 11 takes `out_dir` and Task 6 takes a `path`, with no rule for how `main` derives them. Task 1 loads `.github/rulesets/*.json` with no root defined, while Task 3 runs git in the current directory.
- Required in the plan: `<repo>-before.json` and `<repo>-owner.json` live next to `--targets`. The repo root is resolved from the script's own location, and git runs there. Tasks 1, 3, 11 and 15 state this rule. Verifier: a test run from a different working directory.

**R1-M3 (was MF-12, Medium): Task 12's acceptance omits checks for four behaviours its own text names.**
- Defect: Task 12's text names G6, G8, "a 403 after Step 0 passed stops the whole run" and "several candidates ... go to review and get no PUT", and spec 9 lists duplicate rulesets as a failure case. Task 12's acceptance tests none of these.
- Required in the plan: add four acceptance cases to Task 12: - a G6 refusal; - a G8 refusal; - a 403 after Step 0 that stops the whole run; - two same-name rulesets that go to review with zero PUT.

**R1-M4 (was MF-13, Medium): `verify --all` does not print the "cannot guarantee 17 of 17" statement.**
- Defect: The spec says `verify --all` states plainly that the design cannot guarantee 17 of 17 (spec:171 reads as an output), but Task 14 requires only the counts and the exit status. The requirements word the same idea as design prose (requirements:306).
- Required in the plan: Task 14 prints the statement, and its test asserts the text.

**R1-M5 (was MF-14, Medium): The owner's review before `/sc:implement` and the non-closing pull request are not carried in the plan.**
- Defect: The spec requires two things the plan's Constraints do not carry: the owner's review of the section-11 items before `/sc:implement` is trusted on them, and a pull request that refers to issue 838 without closing it.
- Required in the plan: add two Constraints lines: - the section-11 items need the owner's recorded review before `/sc:implement` runs on them; - the pull request refers to issue 838 and does not close it. - Verifiers: the recorded review and the pull-request wording.

**R1-M6 (was MF-15, Medium): Task 4 does not list the required fields.**
- Defect: Task 4 rejects "a missing field" without saying which fields are required. Yet `init_entries` creates bare `pending` entries without `approved_by`, `intent`, `coverage` and the other fields that are set later, and `scratch_ruleset_ids` is "canary only".
- Required in the plan: Task 4 lists the fields every entry must have and the fields that become required at each status, and marks `scratch_ruleset_ids` optional. Acceptance: an `init_entries` output validates, and a `checked` entry missing `payload_sha256` is rejected.

**R1-M7 (was MF-16, Medium): Task 10's `--init-from` and printed digest are unchecked, and `plan_command` has no signature.**
- Defect: Task 10 requires `--init-from` and requires printing the payload digest the operator confirms at `apply`, but its acceptance checks neither. `plan_command(...)` also has no defined signature, although Task 15 must call it.
- Required in the plan: give `plan_command` a fixed signature in Task 10. Add checks that `--init-from` creates entries through `init_entries` and that the printed digest equals `payload_digest` for the repo.

**R1-M8 (was MF-17, Medium): The test loader and the fake runner do not follow the repo's multi-file test pattern.**
- Defect: The plan copies the per-file module loader of a one-file test folder for about 11 test files plus `conftest.py`. Its `FakeRunner` shares only the `run` signature and the read-only flag. So no offline test sends the tool's own calls through the real allowlist check.
- Required in the plan: load the script once in `conftest.py` through a session-scoped fixture. Make `FakeRunner` a subclass of `Runner` that overrides only the step that starts a process. Task 3 adds a check that an off-list call sent through `FakeRunner` raises `RefusedCommand`.

**R1-M9 (was MF-18, Medium): Tasks 2 to 14 run only their own test file.**
- Defect: Each of Tasks 2 to 14 runs only its own test file, and the whole folder first runs in Task 15. A task that breaks an earlier test file or adds lint errors is therefore found late.
- Required in the plan: end each task's acceptance with `uv run pytest tests/org_rulesets/` and `uv run ruff check scripts/org_rulesets.py tests/org_rulesets`.

**R1-M10 (was MF-19, Medium): The page test does not pin the canary coverage-proof rule.**
- Defect: Task 16 includes the canary rule by reference to spec section 8, whose activity-source clause requires the canary to show complete coverage before other repos rely on it. But `test_page.py` does not check that the page states this.
- Required in the plan: Task 16's acceptance asserts that the page states the canary must prove complete activity coverage before other repos rely on it.

**R1-M11 (was MF-20, Medium): Nothing produces the tag check's `checked_at`, which G1 reads.**
- Defect: `check_tags` takes no `now` and returns only a profile, `unresolved` or `incomplete`. Meanwhile spec 5.1 stores `tag_check{result, checked_at, evidence}`, G1 refuses a tag check older than 24 hours, Task 10 tests "an old tag check", and Task 8, by contrast, takes `now` and returns `checked_at`.
- Required in the plan: Task 9 adds `now` to `check_tags` and returns `result`, `checked_at` and `evidence`, like Task 8. Task 9's acceptance asserts the returned `checked_at`.

**R1-M12 (was MF-21, Medium): `apply` does not re-check for uncommitted edits to the ruleset files.**
- Defect: The requirements and the spec's test table make `apply` refuse when `.github/rulesets/*.json` has uncommitted edits. The plan checks this only in `read_source` at `plan` time, and Task 12's preconditions and acceptance leave it out. The recomputed payload digest (previous plan line 203) already refuses any edit that changes a rendered body; what is left is provenance (`source_sha` no longer names the bytes on disk) and a test the spec names.
- Required in the plan: Task 12 adds a precondition that runs `git status --porcelain -- .github/rulesets` (already allowed by the runner, previous plan line 62) and refuses on any output, naming G7. Acceptance: dirty rule files make `apply` refuse with zero write calls.

### R1.4 Note findings (optional, no rework forced)

- Task 7's acceptance gives the `deferred` status to a plain-data reader: reword the Task 7 criterion to assert the reason codes `archived`, `no-admin` and `empty-repo`.
- Two pieces of logic are described twice: name one shared freshness helper in Task 10 and one shared file reader in Task 8, and say that Tasks 12 and 9 reuse them.
- Task 6's dependency on Task 4 looks unneeded: drop the dependency, or name what Task 6 uses from Task 4.

### R1.5 Constraints the new plan must carry

- The section 11 items need the owner's recorded review before `/sc:implement` is trusted on them; the pull request refers to issue 838 and does not close it (spec lines 9 and 21).
- A line number or task number cited in this section refers to the first plan, not to the new one. The new plan cites its own lines.

