# Artifact Keeper migration — verified requirements (2026-09-25)

Source: owner's IronClaude migration request in this session, verified against fetched `origin/master` at `53cf43e9170f59a617d564fb9b483ea51f67b9e2`. Reference implementation: `IronbellyOrg/Coder` `main` `1ace9c30c5434d70dff5ccbbf143b23b9ea6f763` (merged PR #212). This file is the review spec, not an assertion about unobserved infrastructure.

## Goal

Move every GitHub Actions *artifact* in this repository off GitHub artifact storage and onto Artifact Keeper. Never dual-write. Do not merge. Do not change the Keeper server, lifecycle policies, or GitHub secrets without owner authorization.

## Inventory (verified)

Repo-root `.github/` contains seven workflows and no composite actions. Native artifact/cache surface:

| Kind | Count | Location |
|---|---|---|
| `actions/upload-artifact@*` | **1** | `.github/workflows/readme-quality-check.yml:281` |
| `actions/download-artifact@*` | **0** | — |
| `actions/upload-pages-artifact@*` | **0** | — |
| `actions/cache@*` | **0** | — |
| Cross-repo reusable workflows (`uses: org/repo/.github/workflows/…`) | **0** | — |
| `workflow_call` | **0** | — |

Non-artifact lookalikes (do **not** migrate):

- `codecov/codecov-action@v4` in `test.yml` (coverage upload to Codecov, not GitHub artifacts).
- `setup-python@v5` `cache: 'pip'` in `publish-pypi.yml` (setup-python's GitHub *cache* backend, not `actions/cache` and not artifacts).
- `pypa/gh-action-pypi-publish` (PyPI, not artifacts).

Every job in every workflow is `runs-on: ubuntu-latest` (GitHub-hosted). Repo-level self-hosted runner list is empty (`total_count: 0`). Org runner/group APIs return 403 (`admin:org` required).

The single upload is forensics-only: nothing downloads it. The same job already writes `GITHUB_STEP_SUMMARY` and, on PRs, comments the score from the local JSON.

Live proof the native uploader is still writing GitHub artifacts: run `36084706468` (README Quality Check, `master`, 2026-09-25) has `total_count: 1` (`readme-quality-report`, 405 bytes). Latest Tests runs have `total_count: 0`.

No test, architecture-lint, or hash-pin asserts `actions/upload-artifact` or pins workflow SHAs for this uploader. `tests/swarm/test_merge_boundary_guards.py` pins `boundary-guard.yml` existence only. `tests/audit/*` uses a fictional `.github/workflows/ci.yml` path.

## Requirements

1. **Remove, do not convert, the GitHub-hosted upload.** Replace is forbidden on `ubuntu-latest` — only LAN self-hosted runners can reach Keeper; exposing Keeper to GitHub-hosted jobs is out of scope. There is no download consumer, so relocation onto a self-hosted runner is not required. Delete the `Upload quality report` step in `readme-quality-check.yml`. Leave the local JSON write, step summary, and PR comment. Optionally retarget the comment's "See the Actions tab" sentence at the job summary (already populated); do not invent a Keeper GET.

2. **Copy, do not rewrite, the proven composite and canary** from `IronbellyOrg/Coder@main`:
   - `.github/actions/upload-raw/action.yml` (git blob `aa1a16ba8146178d8e2dfea2e12634f474f07184`)
   - `.github/workflows/artifact-keeper-canary.yml` (git blob `602d4f41729bfc762ab711cfff4057d38ca1fa53`)
   Keep raw `curl PUT` to `$ARTIFACT_KEEPER_URL/api/v1/repositories/<owner>_<repo>/artifacts/<run_id>/retain-<N>d/<attempt>/<job>[/<matrix-key>]/<name>/<object>`. Token via curl stdin (`-K -`), never argv. Retention input `1|7` only. `/api/*` path only (`/generic/*` is not reachable). No dual-write. No download-raw action (zero consumers).

3. **Do not create or rotate secrets, Keeper repos, runner groups, or lifecycle policies.** Confirm with the owner before relying on them. Observed from this session's credentials (not a claim they cannot exist under another principal):
   - IronClaude Actions secrets: `total_count: 0`. Coder has `ARTIFACT_KEEPER_URL` and `ARTIFACT_KEEPER_TOKEN`.
   - IronClaude environments: none.
   - Keeper repository name must be `IronbellyOrg_IronClaude` if/when created.
   - Token scope required: `write:artifacts`.
   - Global Keeper retention is 7 days; `retain-1d` is a label unless a 1-day policy exists (do not add one).

4. **Canary stays dispatch-only.** Jobs: `auth_401`, `empty_glob`, `matrix_keys`, `large_put` (`[self-hosted, big]`), `always_after_failure`, `get_identical`. Do not add `push`/`pull_request` triggers. GitHub `workflow_dispatch` workflows must exist on the default branch to be listed; Coder proved feature-branch dispatch *after* the canary already existed on `main` (runs `36086719786` on `main`, then `36092865906` / `36094207269` on the Phase B branch). IronClaude has no canary on `master` today.

5. **Validate through this repo's existing GitHub Actions, plus the copied canary.** No one-off validation scripts. Proof of cutover:
   - `git grep -nE 'actions/(upload|download)-artifact' -- .github` returns nothing (no justified exceptions remain after the removal).
   - `gh api repos/IronbellyOrg/IronClaude/actions/runs/<id>/artifacts --jq .total_count` is `0` on every PR run of this change.
   - Dispatch the canary on the feature branch once secrets + runner reachability + default-branch presence are satisfied.

6. **Scope discipline.** Do not touch Keeper server, policies, or GitHub secrets. Do not migrate `setup-python` pip cache or Codecov. Do not add pytest guards that this repo does not already have. Do not merge. Preserve untracked work on the original checkout (`fix/pr-submit-attended-ci-monitor`); this work lives in `.dev/worktrees/artifact-keeper` on `feature/artifact-keeper`.

7. **Reflect / ship sequence.** Stage intended files, write a full diff artifact, `/sc:reflect --mode post` against this spec and the design. Fix and repeat until PASS. Then commit, push, `/sc:pr-submit --monitor 3 --base master --head feature/artifact-keeper`. After merge (report, do not do): other open PRs pick up the removal only on a NEW run whose merge ref includes the change.

## Owner blockers (must confirm before implement relies on them)

These are not design choices. Implement must stop if any remain unanswered:

- **B1 Secrets.** May the owner create repo secrets `ARTIFACT_KEEPER_URL` and `ARTIFACT_KEEPER_TOKEN` (`write:artifacts`) on `IronbellyOrg/IronClaude`? This agent must not create them.
- **B2 Keeper repo.** Does a Keeper repository named `IronbellyOrg_IronClaude` already exist, or should one be created (owner action)?
- **B3 Runner reachability.** Is this repo allowed to use org runners labeled `self-hosted` and `[self-hosted, big]`? Repo-level runner list is empty; org APIs 403.
- **B4 Canary precursor.** Authorize a canary-only merge to `master` so `workflow_dispatch` can target the feature branch, **or** accept that canary dispatch happens only after this PR merges to `master`?
- **B5 Removal vs relocate.** Confirm the `ubuntu-latest` README upload is **removed** (recommended; nothing downloads it) rather than relocated onto a self-hosted runner.

Until B1–B3 and B4 are resolved, the canary cannot be proven. The removal + composite copy can still land; Keeper PUT from this repo cannot.
