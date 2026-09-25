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

2. **Skip the entire canary phase (owner B6, 2026-09-25).** Do not keep `.github/actions/upload-raw/` or `.github/workflows/artifact-keeper-canary.yml`. This repo has no production Keeper caller (all jobs are `ubuntu-latest`; the only native upload is removed, not converted). Copying Coder's composite with nothing to call it is dead code. Re-copy from Coder when a self-hosted job actually needs a PUT.

3. **Do not create or rotate secrets, Keeper repos, runner groups, or lifecycle policies.** Confirm with the owner before relying on them. Observed from this session's credentials (not a claim they cannot exist under another principal):
   - IronClaude Actions secrets: `total_count: 0`. Coder has `ARTIFACT_KEEPER_URL` and `ARTIFACT_KEEPER_TOKEN`.
   - IronClaude environments: none.
   - Keeper repository name must be `IronbellyOrg_IronClaude` if/when created.
   - Token scope required: `write:artifacts`.
   - Global Keeper retention is 7 days; `retain-1d` is a label unless a 1-day policy exists (do not add one).

4. **No canary.** Owner skipped dispatch, secrets, Keeper repo, and the canary files themselves.

5. **Validate through this repo's existing GitHub Actions only.** No one-off validation scripts. Proof of cutover:
   - `git grep -nE 'actions/(upload|download)-artifact' -- .github` returns nothing.
   - `gh api repos/IronbellyOrg/IronClaude/actions/runs/<id>/artifacts --jq .total_count` is `0` on every PR run of this change.

6. **Scope discipline.** Do not touch Keeper server, policies, or GitHub secrets. Do not migrate `setup-python` pip cache or Codecov. Do not add pytest guards that this repo does not already have. Do not merge. Preserve untracked work on the original checkout (`fix/pr-submit-attended-ci-monitor`); this work lives in `.dev/worktrees/artifact-keeper` on `feature/artifact-keeper`.

7. **Reflect / ship sequence.** Stage intended files, write a full diff artifact, `/sc:reflect --mode post` against this spec and the design. Fix and repeat until PASS. Then commit, push, `/sc:pr-submit --monitor 3 --base master --head feature/artifact-keeper`. After merge (report, do not do): other open PRs pick up the removal only on a NEW run whose merge ref includes the change.

## Owner blockers (must confirm before implement relies on them)

These are not design choices. Implement must stop if any remain unanswered:

- **B1 Secrets.** May the owner create repo secrets `ARTIFACT_KEEPER_URL` and `ARTIFACT_KEEPER_TOKEN` (`write:artifacts`) on `IronbellyOrg/IronClaude`? This agent must not create them.
- **B2 Keeper repo.** Does a Keeper repository named `IronbellyOrg_IronClaude` already exist, or should one be created (owner action)?
- **B3 Runner reachability.** Is this repo allowed to use org runners labeled `self-hosted` and `[self-hosted, big]`? Repo-level runner list is empty; org APIs 403.
- **B4 Canary precursor.** Authorize a canary-only merge to `master` so `workflow_dispatch` can target the feature branch, **or** accept that canary dispatch happens only after this PR merges to `master`?
- **B5 Removal vs relocate.** Confirm the `ubuntu-latest` README upload is **removed** (recommended; nothing downloads it) rather than relocated onto a self-hosted runner.

Owner B6 (2026-09-25): skip the entire canary phase; real migration is the README upload removal only. B1–B4 are moot for this PR.
