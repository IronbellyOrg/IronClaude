# sc:reflect UC-1 report: codegraph release monitor plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.82
citations_total: 109
citations_revalidated: 108
citations_dropped: 1
citations_inferred: 2
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

Plan: `.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/TASK-WF-followupCodegrap-20261030-153943.md` ("plan:"). Spec: `source.md` in the same package ("source.md:"). Tier 1 card `t1-card.md` (C 0.83 calibrated). Tier 2: three read-only reviewers, `reviewer-cards/reviewer-1-card.yaml` (sonnet, analyzer, C 0.82), `reviewer-2-card.yaml` (glm-5.3 in the haiku slot, qa, C 0.76), `reviewer-3-card.yaml` (fable, refactorer, C 0.81); calibrator opus, disjoint from the reviewers (same class as the plan's author). Every reviewer verdict: revise.

**Status `partial`, for one reason:** the adversarial merge did not run. Two `sc:adversarial` attempts (`adversarial/`, `adversarial-retry/`) each wrote `diff-analysis.md` and a verdict stub, then stalled because their advocate subagents never returned. F1 retry failed; F2 applied: the highest-calibrated reviewer card (reviewer 1) is the merge result (`merged-verdict-fallback.yaml`, `merge_method: single-reviewer-fallback`, `adversarial_unavailable: true`). The finding set below is the union of the Tier 1 findings as the reviewers adjudicated them plus every reviewer's new finding; severity disputes are settled by reviewer 1.

**Coverage.** Pass 1 parsed 0 ids (the spec labels requirements `R1`, `T0`, not `R-001`), so `coverage_degraded: parsed-sparse` forced Tier 2. Pass 2 inferred 338 quote-pinned rows (`artifacts/inferred-requirements.yaml`); containment matched 111 (`coverage_pct_union` 0.3284, `artifacts/coverage-matrix.yaml`) because plan tasks cite spec sections instead of restating them; by-reference triage (`artifacts/unmapped-triage.yaml`) covers 222 of the 227 unmatched rows. The 5 left are spec §2.1 (source.md:57-72): no task cites it, and the concrete gap behind them is the missing `tests` step (D-R2-02). `S_dev_density` 0.0148.

**Verdict: revise before `/sc:implement`.** 2 critical and 18 important deviations, 31 minor rows (some rows merge duplicate ids from several reviewers). Evidence validator: 108 of 109 anchors re-read and upheld, 1 dropped (external file, see Grounding Gaps), 4 corrections applied; 30 of 338 inferred rows sampled, 0 dropped.

## Deviations

Gold standard: the spec (source.md). regression = breaks a stated acceptance rule or constraint; drift = unauthorised omission or change; necessary = forced and documented; authorized = approved.

### Deviation D-T1-01: Task 1 cherry-picks a planning commit that does not exist
- **Location:** plan:35; source.md:219-221
- **Classification:** regression (critical; spec-inherited)
- **Evidence:** the planning files are untracked and no `docs(plan): codegraph release monitor` commit exists, so `test -n "$PLAN"` stops Task 1 (reviewer 2 confirmed).
- **Default remediation:** commit the planning files with subject `docs(plan): codegraph release monitor (#323)`; do the branch setup before `/sc:implement` in a new worktree (D-T1-27).

### Deviation D-T1-26: the job token stays in `.git/config` while `prove` runs third-party code
- **Location:** source.md:112,115; .github/workflows/test.yml:144
- **Classification:** regression (critical; spec-inherited; reviewer 2 proposed important, reviewer 1 kept critical)
- **Evidence:** the spec strips the token only from the prove step's env (source.md:115); `test.yml:133-144` keeps the token out of `.git/config` with `persist-credentials: false`, which the monitor design omits. (`actions/checkout`'s `persist-credentials` default `true` was read by the orchestrator with `gh api repos/actions/checkout/contents/action.yml`; that external anchor could not be re-read by the validator and is dropped as a citation.)
- **Default remediation:** `persist-credentials: false` on every checkout; the push step gets the token alone; static check.

### Deviation D-T1-02: plan evidence goes to the never-staged project-root `artifacts/`
- **Location:** plan:27,40,55,81,118,121-124,138; source.md:31
- **Classification:** drift (important; plan)
- **Default remediation:** `"$PKG/artifacts/..."` everywhere, `PKG` defined in each block.

### Deviation D-T1-03: `$PKG` unbound in separately-run blocks under `set -u`
- **Location:** source.md:223,233,296,336
- **Classification:** regression (important; spec-inherited)
- **Default remediation:** every block that uses `PKG` defines it first.

### Deviation D-R3-01: three plan acceptance lines are inverted or vacuous under `bash -e`
- **Location:** plan:53,96,121; source.md:245,305,336
- **Classification:** regression (important; plan)
- **Evidence:** "grep ... prints nothing" exits 1 when the criterion passes; bare `comm -13` exits 0 either way; the spec uses `if ...; then exit 1; fi` and `test -z "$(...)"`.
- **Default remediation:** use the spec's forms.

### Deviation D-T1-04: post-merge check accepts fetch-ok OR prove-pass
- **Location:** source.md:354; plan:135
- **Classification:** regression (important; spec-inherited)
- **Default remediation:** two separate greps; a command for "no PR and no issue".

### Deviation D-T1-05: `gh run list --limit 1` right after dispatch can pick the wrong run
- **Location:** source.md:351-353
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** timestamp before dispatch, bounded poll for a `workflow_dispatch` run created after it.

### Deviation D-T1-06: Task 8 has no mechanical merge gate
- **Location:** plan:130-132; source.md:347-357
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** first line asserts the PR state is `MERGED`, else stop as blocked.

### Deviation D-T1-14: push ordering contradicts the `always()` PR step
- **Location:** source.md:69,118,165,202
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** fixed order fetch ok, bump, commit, push, tests, prove, body, PR (`if: always()` and push succeeded); static check push precedes prove.

### Deviation D-T1-15: "stdlib only" conflicts with importing `install_mcp`
- **Location:** source.md:44,146-147; src/superclaude/cli/install_mcp.py:21,23; src/superclaude/cli/__init__.py:13
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** the script stays stdlib-only and reads `MCP_TOOLS` and the expected entry from a child `python -c`; AST import check against `sys.stdlib_module_names`.

### Deviation D-T1-16: sandbox HOME and PATH disagree
- **Location:** source.md:143,281-283; src/superclaude/cli/install_codegraph.py:67-68
- **Classification:** drift (important; spec-inherited; also R2-03)
- **Default remediation:** `HOME=<tmp>/home`, `PATH=<tmp>/home/.local/bin:/usr/bin:/bin`, `home=` reports `<tmp>/home`, cleanup removes `<tmp>`.

### Deviation D-T1-17: the infrastructure counter cannot fire and miscounts
- **Location:** source.md:100,101,166,197
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** count completed infra-tagged runs plus the current one; invalid input exits 1.

### Deviation D-T1-18: `check --tag` equal to the pin is undefined
- **Location:** source.md:101,127,197,351
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** allowed only with dry run; R16 case; Task 8 reads the pin.

### Deviation D-T1-21: the workflow's PR and issue actions are untested YAML
- **Location:** source.md:46,92,199,202
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** an `apply` subcommand executes `route` actions through `_gh` with `--repo` enforced; R-case.

### Deviation D-T1-27: the branch switch inside the plan breaks `/sc:implement`'s state
- **Location:** plan:35
- **Classification:** drift (important; plan)
- **Default remediation:** create the feature branch in a new worktree under `.dev/worktrees/` before `/sc:implement`, run it there.

### Deviation D-T1-34: Task 5 drops the two-line matrix and `dry_run` rules
- **Location:** plan:92,95; source.md:110
- **Classification:** drift (important; plan)
- **Default remediation:** add both; static check that side-effect steps are gated on dry run.

### Deviation D-T1-40: tasks point at spec commands instead of stating them
- **Location:** plan:35,55,68,110,118
- **Classification:** drift (important; plan)
- **Default remediation:** literal commands in each task.

### Deviation D-R1-01: hidden `1.6.3` literals break the first patch bump
- **Location:** tests/cli/test_install_codegraph.py:306,320; source.md:24,255
- **Classification:** regression (important; spec-inherited)
- **Evidence:** `_bump(monkeypatch, version="1.6.3")` and `vdir(box.home, "v1.6.3")`; a bump to v1.6.3 makes `test_u21` compare a directory with itself; the `9.9.9` mutation check cannot catch it.
- **Default remediation:** derive the next version from `cg.VERSION`; mutation check with the next patch, minor and major.

### Deviation D-R1-02: the idempotency gate has no owner
- **Location:** source.md:62,101,103,133-134
- **Classification:** drift (important; spec-inherited)
- **Default remediation:** `check` reads branch and PR state and emits `branch_exists`, `declined`, `reprove`; push and work gated on them.

### Deviation D-R2-02: the `tests` stage has no anchor (the five §2.1 rows)
- **Location:** plan:92,95; source.md:66,159,202
- **Classification:** drift (important; plan; also R3-02)
- **Default remediation:** name the step and its files in Task 5; add `tests` to the stage values; static check for a pytest step between bump and prove.

## Minor findings

| ID | Class | Origin | Location | Claim | Fix |
|---|---|---|---|---|---|
| T1-07 | drift | spec | source.md:355-357 | normal post-merge run never watched | resolve run id, watch, grep `result=none` |
| T1-08 | drift | spec | source.md:253-258 | failing mutation pytest leaves the worktree | cleanup `trap` before `worktree add` |
| T1-09 | drift | spec | source.md:269 | import grep misses lazy imports, flags `import os, sys` | AST check (with D-T1-15) |
| T1-10 | drift | spec | source.md:306 | line-based `--repo` grep; script never checked | join continuations; check the script too |
| T1-11 | drift | plan | plan:66,81,111,135 | four criteria have no command | give each a command |
| T1-12 / R3-03 / R1-03 | drift | plan | source.md:279; plan:81,118 | fetch writes no `result=` file; prove log vs `.out` | `--github-output` to `.out` files; grep those |
| T1-13 / R1-04 / R3-05 | drift | plan | plan:109-112; source.md:321 | Task 6 drops the `SuperClaude-Org/.../pull` negative check | add it |
| T1-19 | drift | spec | source.md:110,133 | fresh-master checkout vs re-prove at branch head | re-prove leg checks out the branch |
| T1-20 | drift | spec | source.md:44,103 | F6 omits `route` | add it |
| T1-23 | drift | spec | source.md:402-407 | §7 items numbered 1,2,3,6,4,5 | renumber |
| T1-24 | drift | spec | source.md:164,166,168 | fingerprint uses a branch SHA artifacts may lack | master HEAD for branchless artifacts |
| T1-25 | drift | spec | source.md:110-112,202 | `if:`/permissions on "the job" though there are two jobs | every job; static check each |
| T1-28 | drift | plan | plan:35 | "wait" cannot be followed by `/sc:implement`; #329 already merged (2f10a0e1) | "stop as blocked" |
| T1-29 | drift | spec | src/superclaude/cli/install_codegraph.py:280-281; source.md:143 | install proves only the runner's asset; child PATH lacks venv python | use `sys.executable`; say which asset in the body |
| T1-31 | drift | spec | source.md:112,202 | [INFERRED] attestation may need `attestations: read` | confirm in the post-merge dry run; update permissions and test together |
| T1-32 | drift | spec | source.md:129,138,185 | replay dates depend on time of day | `now` at the cron time; real `published_at` in the fixture |
| T1-33 | drift | plan | tests/unit/test_cli_doctor.py:3-15 | doctor test needs a new `install_codegraph` import | name it |
| T1-35 / R3-04 | drift | plan | plan:92; source.md:115,117-120 | Task 5 omits fetch-depth, commit format, `GH_TOKEN` scope, `stage=aborted`, CI link, summaries | list them |
| T1-36 | drift | plan | plan:95; source.md:202 | Task 5 static-check summary incomplete | list every check |
| T1-37 | drift | plan | plan:17-29; source.md:31,210 | Constraints drop `git status` rule and `MX-*` staging | add both |
| T1-38 | drift | plan | plan:76; source.md:148 | Task 4 drops log cap and process-group kill | name them |
| T1-39 | drift | plan | plan:48; source.md:43 | Task 2 drops the `install_codegraph.py:26-27` pointer | add it |
| T1-41 / T1-42 / T1-43 | drift | plan | plan:63,76,92 | Tasks 3-4 do not name `install_mcp.py`; Task 5 names `test.yml` only as the dispatch target, not as the setup block to mirror (test.yml:54-65,141-150); Task 4 has no live block | name them; inline the block |
| R1-05 | drift | spec | source.md:98,269 | allow-list omits stdlib modules the MCP client needs | AST check against `sys.stdlib_module_names` |
| R1-06 | drift | spec | source.md:96,126 | `--paginate` prints one JSON array per page | `--paginate --slurp`; two-page R-case |
| R1-07 | drift | spec | source.md:114-115; .github/workflows/test.yml:40,95 | [INFERRED] `uv run` may build a second env in CI | use the activated venv's python and pytest |
| R1-08 | drift | spec | source.md:66,105; plan:76,132 | no file list or stage for `tests`; v1.6.2 hard-coded | name files; read the pin |
| R1-09 | drift | spec | source.md:110,202 | dry run "no push, no PR, no issue" untested | static check of the gating |
| R2-01 | drift | plan | plan:55; source.md:252-259 | nothing writes `t2-mutation.log` | tee the block into `$PKG/artifacts/` |
| R2-04 | necessary | spec | source.md:51,224,329 | §1 says no `make sync-dev` needed, §4 runs it | reword §1 |
| R3-06 | drift | plan | plan:48; source.md:35 | Task 2 omits "locate by literal, not line" | add it |

## Refuted or downgraded

- T1-22 (20 vs 22 literal copies): downgraded to a nit; 20 is the count of sites T1 rewrites (reviewer 1, source.md:24,49,51,419). Wording clarified, not a defect.
- T1-30 (`ruff` not on PATH for R6): downgraded; `ruff==0.15.20` is in the dev extras (pyproject.toml:54) and on PATH in the venv. R6 still uses `shutil.which("ruff")` and skips with a reason when absent.
- T1-38 (fetch order): the fetch order is carried by the §2.2 pointer (reviewer 2); the log cap and process-group kill remain.
- T1-13 (YAML parse line): subsumed by the static test (reviewer 2); the pull-link check remains.
- R1-03: overstated per its calibrator; only fetch (source.md:279) and plan Task 7 (plan:118) omit `--github-output`.

## Inferred requirements (Pass 2)

338 rows in `artifacts/inferred-requirements.yaml` (id, verbatim quote, `source.md:<line>` citation, section); match results in `artifacts/coverage-matrix.yaml`, by-reference triage in `artifacts/unmapped-triage.yaml`. Rendering 338 rows here would duplicate those files; the five rows without any reference are INF-042, INF-043, INF-045, INF-046, INF-047 (spec §2.1, source.md:57-70), all addressed by D-R2-02. Validator postscript: see the evidence-validator result appended below.

## Grounding Gaps

One dropped citation: D-T1-26's external `actions/checkout` `action.yml` line numbers (outside the repo, not re-readable by the validator); the finding stands on source.md:115 and test.yml:133-144. T1-28's "#329 merged as 2f10a0e1" rests on `gh pr view 329` (state MERGED, 2026-10-30T15:23:26Z, merge commit 2f10a0e1) run by the orchestrator, not on a file anchor. Two findings carry `[INFERRED]` sub-claims (T1-31 attestation permission, R1-07 CI environment); both have a concrete check in the fix and do not block the plan.
