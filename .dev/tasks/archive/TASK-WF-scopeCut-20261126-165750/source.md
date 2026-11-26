# Scope cut: apply the three rulesets to the IronbellyGroup repos (issue 838)

Type: spec. Decided by the lead on 26 Nov 2026 (recorded in `.dev/issues/838/issue-summary.md`, section Decided): cut the scope. Issue 838 asks to apply the rulesets in `.github/rulesets/` to the IronbellyGroup repos, not to build a rollout framework. Build the smallest thing that does it: one small script with a dry run, plus an operator page. No persistent state store, no status machine, and no rollback engine beyond saving each repo's before state to a file. The seven owner points of the earlier plan review are not settled here; the parts that need them are dropped and listed as follow-ups.

## 1. Delivery boundary

The work delivers a script, its offline tests, an operator page and two links. It makes no live call to any IronbellyGroup repo; the owner runs the live rollout afterwards, one repo at a time, following the page. Clay's list of 17 repos is the go for each repo, and each repo needs its own 90-day check of direct pushes before any live write. So the pull request refers to issue 838 and lists what is left; it does not close it.

## 2. The script

`scripts/apply_org_rulesets.py`, Python 3.10, standard library only, ruff rules `E,F,I,N,W,TID` at line length 88. Shape copied from `scripts/merged_pr_log.py` (`main(argv, env, runner, now)`, every outside dependency passed in, an `if __name__ == "__main__"` guard) and from `Runner` in `scripts/worktree_cleanup.py` (a positive allowlist in `check_allowed`, a `RefusedCommand` error, a record of every accepted call, and `_execute` as the only method that starts a process).

Command line, one repo per run:

```text
apply_org_rulesets.py --org O --repo R [--out DIR] [--apply --confirm DIGEST]
```

Without `--apply` it is a dry run and makes no write. Exit codes as in `worktree_cleanup.py`: 0 ok, 64 usage error, 69 a refusal or a failed step. `--org` has no default. The script refuses the upstream org name `SuperClaude-Org` in any letter case, and holds no other org or repo name.

### 2.1 Rendering (pure)

- The rule files are read from `<root>/.github/rulesets/`, where `<root>` is the folder above `scripts/` resolved from the script's own location; no function reads the current working folder.
- For a branch `b`, the body is `protect-master.json` with `name` set to `protect-<b>` and `conditions.ref_name.include` set to `["refs/heads/<b>"]`, nothing else changed. For `master` and `integration` the result equals the two existing files as parsed JSON. A branch name that is empty, contains `*` or `~`, or starts with `refs/` raises. No output contains `~DEFAULT_BRANCH`.
- The tag body is `protect-release-tags.json` unchanged (its `update` rule is settled on `integration`).
- Branches protected: the default branch plus `master` and `integration` where they exist, no duplicates. Order of writes: the tag ruleset, then `integration`, then `master`, then any other default branch.
- The digest is the sha256 of the canonical JSON (sorted keys, fixed separators) of the bodies in that order.

### 2.2 Runner

`Runner.run(argv, stdin=None)` does, in order: `check_allowed`, the read-only check, record the call, then `_execute`. It accepts only `gh api` calls under `repos/<org>/<repo>` for these shapes: GET the repo, GET `branches/<b>`, GET `branches/<b>/protection`, GET `rulesets` and `rulesets/<id>`, GET `activity`, GET `commits` and `commits/<sha>/pulls`, GET `git/matching-refs/tags/v`; and POST `rulesets`. A runner built with `read_only=True` (the dry run) refuses POST before any process starts. The payload goes in on stdin (`--input -`). `_execute` passes a named timeout constant to `subprocess.run`; a timeout becomes one named result, never a hang. Tests use a `FakeRunner` that subclasses `Runner` and overrides only `_execute`, so every call goes through the real allowlist; an answer may be a callable that receives argv and stdin. Recorded calls are checked as a closed list of allowed shapes (repo-scoped `gh api` calls name `<org>/<repo>` in full).

### 2.3 Checks and dry run

1. Read the repo: canonical owner and name, `archived`, `default_branch`, `permissions.admin`. Archived, no admin, or no default branch: stop with a refusal naming it.
2. 90-day direct-push check, per protected branch. One UTC cutoff of now minus 90 days. Primary source: `activity?ref=refs/heads/<b>&time_period=quarter`, paginated, counting `push`, `force_push` and `branch_deletion` as direct pushes and ignoring `pr_merge`, filtered by timestamp against the cutoff. If that source is unavailable (403 or 404) or paginates past a cap, fall back to `commits?sha=<b>&since=<cutoff>` and, per commit, `commits/<sha>/pulls`; a commit with no merged pull request is a direct push; more than 200 lookups gives `incomplete`. Result: `pass` only for zero direct pushes on every branch; `blocked` for any direct push; `incomplete` when no source gives a full answer. `incomplete` is never turned into `pass`. Direct pushes by named people are not excused here (that needs an owner statement, a follow-up).
3. Existing state: classic branch protection on a branch of the set (GET `protection` answers 200) and a same-name ruleset already present are reported; the script never edits or deletes either. A classic-protection hit refuses `--apply`; a same-name ruleset is skipped with a printed line.
4. The dry run prints: repo facts, the push-check result per branch with its evidence count, the existing state, the number of `v*` tags (with a warning line that the tag ruleset blocks moving and deleting tags, so release workflows must be checked by hand first), the rulesets that would be created in order, the digest, and the exact command to apply.

### 2.4 Apply

`--apply` requires `--confirm DIGEST` equal to the digest of the rendered bodies, a push check of `pass`, no classic protection, and `--out DIR`. Then: write `<repo>-before.json` into `DIR` (it must not exist; it holds the full body of every existing ruleset read by id and the protection state of each branch of the set, a 404 recorded as `"none"`), then for each ruleset in order POST it, read it back by id and compare name, target, enforcement, conditions, bypass actors (as a set) and rules (type plus complete parameters; server metadata keys `id`, `source`, `source_type`, `node_id`, `created_at`, `updated_at`, `current_user_can_bypass`, `_links` ignored); stop at the first failure and print what was written. A timed-out POST is followed by a list call before anything else and a matching same-name ruleset is adopted; a POST is never repeated blindly. On success print the one-line comment for issue 838 (repo, date, ruleset ids by name). The script never posts the comment. No call ever writes to the ruleset ids 28081842, 28081844 or 28081845.

Rollback is manual: the script prints, and the page lists, the `gh api --method DELETE repos/<org>/<repo>/rulesets/<id>` command for each id it created; `<repo>-before.json` is the saved before state.

## 3. Tests

Folder `tests/org_rulesets/` with `__init__.py`, `conftest.py` (session fixture loading the script once, the pattern of `tests/worktree_cleanup/conftest.py` lines 26 to 37; shared fixtures defined only there; `FakeRunner`), `test_render.py`, `test_runner.py`, `test_checks.py`, `test_apply.py`, `test_cli.py`, `test_page.py`. Synthetic names only (`acme-one`); no real private repo name in any tracked file. Every task closes with `uv run pytest tests/org_rulesets/` (plus `tests/docs/test_branch_protection_rulesets.py` from the page task on), `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets`.

## 4. Operator page and links

`docs/developer-guide/branch-protection-multi-repo.md`: variables `OWNER` and `REPO`; the order per repo (dry run, read it, check release workflows for tag moves by hand, apply with the digest, comment ids on issue 838); the canary rule (start with one low-risk repo; the activity source must show complete coverage there before others rely on it); the manual rollback commands; the exit-status rule (a failed hooks, keys or installations check is "unknown", never "0"; the page tells the operator to read them as in the existing guide); the follow-ups. One link line in `docs/developer-guide/branch-protection.md` (after the introductory paragraph; its commands and the four pinned strings unchanged) and two link lines in `docs/developer-guide/documentation-index.md` (beside the entries at lines 37 and 168). The page names no real private repo or org login.

## 5. Dropped parts (listed as follow-ups in the pull request)

A persistent targets file with a status machine and a single writer; owner-evidence files and statements (push statements, accepted pushers, tag statements, tag exceptions); the tag-mutation scan and tag-deletion handling; the hooks, keys and installations review gate; a rollback engine; a `verify --all` completion check over the 17 repos; an allowlist file; the branch-only interim state; the seven owner points of the second plan review (`.dev/reflect/pre-TASK-WF-designR1-20261126-145124-20261126145705/REPORT.md`, section Owner-open).

## 6. Files

| File | Change |
|---|---|
| `scripts/apply_org_rulesets.py` | New |
| `tests/org_rulesets/` | New (`__init__.py`, `conftest.py`, six test files) |
| `docs/developer-guide/branch-protection-multi-repo.md` | New |
| `docs/developer-guide/branch-protection.md` | One link line |
| `docs/developer-guide/documentation-index.md` | Two link lines |
