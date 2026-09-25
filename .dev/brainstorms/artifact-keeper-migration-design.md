# Artifact Keeper migration — implementation design and checklist

Baseline: fetched `origin/master` `53cf43e9170f59a617d564fb9b483ea51f67b9e2` (2026-09-25). Driving spec: `artifact-keeper-migration-requirements.md` beside this file. Reference: `IronbellyOrg/Coder@main` `1ace9c30c5434d70dff5ccbbf143b23b9ea6f763` (PR #212). Design is **one removal + two file copies**, never a mirror/dual-write.

Worktree: `/config/workspace/IronClaude/.dev/worktrees/artifact-keeper` on `feature/artifact-keeper`. Original dirty checkout `fix/pr-submit-attended-ci-monitor` is untouched.

## 0. Owner rulings (2026-09-25, post UC-1)

| ID | Ruling |
|---|---|
| B1/B2 | Skip Keeper repo and secrets. Skip canary **dispatch** this PR. Land copies + README upload removal. No claim that Keeper works for IronClaude. |
| B3 | Self-hosted yes, **no `big` label**. Copy canary but drop `large_put`; remove it from `get_identical.needs`. |
| B4 | No precursor merge. Canary dispatch only after this PR merges (report-only; this session will not dispatch). |
| B5 | **Remove** the `ubuntu-latest` README upload. Do not relocate. |
| B6 | Skip the **entire** canary phase. Do not keep `artifact-keeper-canary.yml` or `upload-raw` in this repo (no production Keeper caller). Real migration = the README upload removal only. |

## 1. Current-master inventory (every `.github` workflow)

### 1.1 Native artifact upload (the only conversion row)

| # | Workflow, job, step | `runs-on` | Existing `if` / step continue-on-error | Existing name / path | Retention / `if-no-files-found` | Matrix | Downloaded? | Decision |
|---|---|---|---|---|---|---|---|---|
| 1 | `readme-quality-check.yml`, `readme-quality-check`, **Upload quality report** | `ubuntu-latest` | `always()` / none | `readme-quality-report` / `readme-quality-report.json` | **30** / default (`warn`) | none | **No.** Same job reads the local JSON for the PR comment (`actions/github-script@v7`) and already writes `GITHUB_STEP_SUMMARY`. No `download-artifact`, no later job `needs:` this artifact. | **REMOVE the step.** GitHub-hosted cannot reach Keeper. Retention 30 is not a Keeper policy (`1\|7` only). Relocate-to-self-hosted is YAGNI. |

Live GitHub artifact: run `36084706468` `total_count: 1`.

### 1.2 Workflows with zero artifact I/O (no code change)

| Workflow | Jobs | `runs-on` | Notes |
|---|---|---|---|
| `test.yml` | `test` (py 3.10/3.11/3.12), `swarm-marker-matrix` (imm/inv), `lint`, `plugin-check`, `verify-deps`, `doctor-check`, `test-summary` | `ubuntu-latest` | Coverage goes to Codecov, not artifacts. |
| `quick-check.yml` | `quick-test` | `ubuntu-latest` | |
| `boundary-guard.yml` | `flag-boundary-touch` | `ubuntu-latest` | Path-filtered; tests assert this file exists, not artifact steps. |
| `contract3-generator-constraint-lint.yml` | `generator-constraint-considered` | `ubuntu-latest` | |
| `publish-pypi.yml` | `build-and-publish`, `test-installation` | `ubuntu-latest` | `setup-python` `cache: 'pip'` is GitHub *cache*, not `actions/cache`, not artifacts. Out of scope. |
| `pull-sync-framework.yml` | `sync-and-isolate` | `ubuntu-latest` | Schedule + dispatch. Commits to the checkout; no artifacts. |

### 1.3 Cache / pages / reusable

- `actions/cache`: none.
- `actions/upload-pages-artifact`: none.
- Cross-repo reusable workflows / `workflow_call`: none.
- `.github/actions/`: does not exist yet; will be created by the copy.

```
                  GitHub-hosted (ubuntu-latest)
  ┌─────────────────────────────────────────────────────────┐
  │  test / quick-check / boundary / contract3 /            │
  │  publish-pypi / pull-sync  ──  no artifact I/O          │
  │                                                         │
  │  readme-quality-check                                   │
  │    write JSON ──► step summary + PR comment (keep)      │
  │    upload-artifact@v4 ──► GitHub storage (DELETE)       │
  └─────────────────────────────────────────────────────────┘

                  LAN self-hosted (org runners; unproven for this repo)
  ┌─────────────────────────────────────────────────────────┐
  │  artifact-keeper-canary (dispatch only; COPY)           │
  │    upload-raw ──PUT /api/v1/repositories/               │
  │      IronbellyOrg_IronClaude/artifacts/<key>            │
  │    GET round-trip in-job                                │
  └─────────────────────────────────────────────────────────┘
```

## 2. Implementation (shortest diff that meets the spec)

### 2.1 Remove the native uploader

In `.github/workflows/readme-quality-check.yml`, delete the step:

```yaml
    - name: Upload quality report
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: readme-quality-report
        path: readme-quality-report.json
        retention-days: 30
```

Keep:

- `generate_report()` writing `readme-quality-report.json` (PR comment still needs it).
- `GITHUB_STEP_SUMMARY` write.
- PR comment step. Optional one-line copy tweak: "See the job summary for the detailed report." instead of "See the Actions tab for the detailed report." (the JSON will no longer appear as an Actions artifact; the summary will).

Do **not** add `./.github/actions/upload-raw` to this job. Do **not** change `runs-on`.

### 2.2–2.3 Superseded by B6

Do **not** copy `upload-raw` or the canary. Nothing in this repo PUTs to Keeper.

### 2.2 Copy `upload-raw` verbatim (historical — do not implement)

Create `.github/actions/upload-raw/action.yml` as a byte copy of Coder `main` blob `aa1a16ba8146178d8e2dfea2e12634f474f07184`.

Contract (do not "improve"):

| Input | Rule |
|---|---|
| `name`, `path`, `keeper-url`, `keeper-token` | required (url/token required true) |
| `if-no-files-found` | `error\|warn\|ignore`, default `warn` |
| `retention-days` | `1\|7` only, default `7`; encoded as `retain-Nd` path segment |
| `matrix-key` | optional; appended before `/{name}/{object}` |

- PUT `$ARTIFACT_KEEPER_URL/api/v1/repositories/${GITHUB_REPOSITORY//\//_}/artifacts/$key`
- Token via `printf 'header = "Authorization: Bearer %s"\n' "$TOKEN" | curl -K -` (never argv)
- Skip hidden/empty paths like `actions/upload-artifact`
- Single file → raw bytes; multi-file → tar via NUL-delimited stdin list
- Fail closed if token would appear in url/key/name outputs
- Outputs: token-free `url` (GET `/download/{key}`) and `key`

No JS action, no GitHub CreateArtifact, no `/generic/*`.

### 2.3 Copy the canary, adapt only if a blocker forces it

Create `.github/workflows/artifact-keeper-canary.yml` as a byte copy of Coder `main` blob `602d4f41729bfc762ab711cfff4057d38ca1fa53`.

Keep `on: workflow_dispatch` only, `permissions: contents: read`, jobs:

| Job | `runs-on` | What it proves |
|---|---|---|
| `auth_401` | `self-hosted` | PUT without token → 401/403; host is not GitHub |
| `empty_glob` | `self-hosted` | nff error/warn/ignore; empty dir; hidden-only dir; mixed dir tar excludes `.hidden` |
| `matrix_keys` | `self-hosted` (`cell: [a,b]`) | `matrix-key` uniqueness + GET round-trip + retain-1d in key |
| `large_put` | `[self-hosted, big]` | 157 MB PUT+GET `cmp` |
| `always_after_failure` | `self-hosted` | `if: always()` after a failed step |
| `get_identical` | `self-hosted` | needs the three PUT jobs; host-is-not-GitHub |

`actions/checkout@v6` in the canary is Coder's proven pin; do not downgrade to this repo's `@v4` without a failure. Repo-safe key prefix is derived from `github.repository` (`IronbellyOrg_IronClaude`) — no hard-coded Coder repo name in the canary.

Adapt **only** if owner says this repo cannot use `[self-hosted, big]`: drop or skip `large_put` and drop it from `get_identical.needs`. That is a documented gap, not a silent edit. Default: copy verbatim.

### 2.4 Tests / guards

None assert the old uploader. Do not add a pytest grep suite (cutover proof is `git grep` + Actions `total_count`). Do not touch `tests/swarm/test_merge_boundary_guards.py`.

### 2.5 Files that change (intended set)

| Path | Action |
|---|---|
| `.github/workflows/readme-quality-check.yml` | delete upload step; optional comment wording |
| `.github/actions/upload-raw/action.yml` | **do not add** (B6) |
| `.github/workflows/artifact-keeper-canary.yml` | **do not add** (B6) |
| `.dev/brainstorms/artifact-keeper-migration-requirements.md` | **new** (this spec) |
| `.dev/brainstorms/artifact-keeper-migration-design.md` | **new** (this file) |
| `.github/workflows/README.md` | optional one-line note that README report is job-summary only; skip unless the upload-step comment is already being edited |

Nothing else.

## 3. Validation

1. `git grep -nE 'actions/(upload|download)-artifact' -- .github` → empty.
2. Existing PR Actions (`Tests`, `Quick Check`, `Contract`, `README Quality Check` if README paths change — they will, because this PR edits `readme-quality-check.yml` itself? Path filter is `README*.md` and `Docs/**/*.md`, **not** `.github/workflows/readme-quality-check.yml`. So README Quality Check will **not** run on this PR unless we also touch a README. Tests + Quick Check + Contract will. That is enough to prove `total_count == 0` on those runs; README Quality Check is path-filtered and will only prove the removal on a later README-touching run **or** a `workflow_dispatch` of that workflow.
3. Dispatch README Quality Check (`workflow_dispatch` exists on that file and **is already on master**) from the feature branch after push, to prove that job's `total_count == 0`. This is the production-path proof for the removal and does **not** need Keeper.
4. **No canary dispatch** (B6).
5. No one-off scripts. Report pre-existing CI failures separately from new ones.

## 4. Rollback

Revert this PR's three workflow/action files. Restoring `actions/upload-artifact@v4` re-consumes org artifact quota; only do that if quota is actually cleared. Copied canary/action are inert without secrets+runners. No GitHub artifacts are deleted by this PR. No Keeper objects need cleanup for the removal path.

## 5. Runner-reachability and other gaps (not proven)

| Gap | Evidence | Impact |
|---|---|---|
| **No repo secrets** | `GET /repos/IronbellyOrg/IronClaude/actions/secrets` → `total_count: 0`. Coder has `ARTIFACT_KEEPER_URL` + `ARTIFACT_KEEPER_TOKEN`. | Canary PUT/GET cannot authenticate. Owner must create secrets (agent must not). |
| **Keeper repo `IronbellyOrg_IronClaude` unknown** | Not queried (would require Keeper URL, which we do not have). | First authenticated PUT will 404 if missing. Owner creates or confirms. |
| **Self-hosted runner access unknown** | Repo runners `total_count: 0`. Org runners/groups 403. Coder canary succeeded on `self-hosted` and `[self-hosted, big]` from the same org (`36086719786`). | Canary jobs queue forever or fail if this repo is not in the runner group. `large_put` additionally needs `big`. |
| **Canary not on `master`** | Workflow list has no `artifact-keeper-canary`. Coder feature-branch dispatch worked only because Phase A already landed on `main`. | `gh workflow run` of a brand-new dispatch workflow typically 404s until it exists on the default branch. |
| **README Quality Check path filter** | `on.pull_request.paths: README*.md, Docs/**/*.md` | PR CI will not exercise the deleted step. Use `workflow_dispatch` on that workflow (already on master) against the feature ref. |
| **`retain-1d` is a label** | Owner constraint; global policy is 7d. | Canary uses `retention-days: "1"`; objects may live 7d. Do not add a 1-day policy. |
| **Unexercised jobs after merge** | All remaining production jobs are GitHub-hosted and upload nothing. | No production Keeper PUT will run unless a future self-hosted job is added. Composite is inventory for that future; canary is the only exercise. |
| **Quota-workaround commits** | This repo's uploader has no `continue-on-error`. | Nothing to drop. |

## 6. Execution checklist

- [ ] **Stop on blockers B1–B5** from the spec if the owner has not answered. Removal + file copies do not require secrets; canary dispatch and any claim of Keeper reachability do.
- [ ] Delete the `Upload quality report` step. Do not add Keeper credentials to `readme-quality-check.yml`. Optional PR-comment wording fix.
- [x] **B6:** do **not** copy `upload-raw` or the canary. Real migration is the README upload removal only.
- [ ] `git grep -nE 'actions/(upload|download)-artifact' -- .github` empty. Confirm no `download-artifact`, no pages artifact, no `actions/cache`.
- [ ] Review YAML. Run this repo's existing PR Actions. Dispatch README Quality Check against the feature ref; assert that run's artifact `total_count == 0`. Dispatch canary only if B1–B4 are green.
- [ ] Stage only the intended set in §2.5. Capture a complete staged/untracked-intended diff artifact. `/sc:reflect --mode post` against the spec + this design. Resolve material regressions and re-reflect.
- [ ] After PASS: commit + push `feature/artifact-keeper`. `/sc:pr-submit --monitor 3 --base master --head feature/artifact-keeper --title "ci: move artifacts to Artifact Keeper"`. `--repo IronbellyOrg/IronClaude`. Do not merge.

## 7. After merge (report, do not do)

Other open PRs pick up the removed uploader only on a **new** run whose merge ref includes this change. `gh api -X PUT repos/IronbellyOrg/IronClaude/pulls/<N>/update-branch -f expected_head_sha=<sha>`. Close/reopen and re-run can reuse a stale merge ref and still upload to GitHub. No quota-workaround commits exist here to drop.
