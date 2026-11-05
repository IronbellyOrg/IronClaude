```yaml
contract_version: 1.8.0
status: success                      # the reflection ran to completion and every citation held; the PLAN verdict is FAIL (see Verdict)
mode: pre
tier_reached: 2
confidence_calibrated: 0.85          # mean of the two reviewer-card calibrations (0.82, 0.87), rounded; the Tier-1 card calibrated 0.73
citations_total: 50
citations_revalidated: 50            # the validator re-read every range, although >20 would allow sampling
citations_dropped: 0                 # 5 imprecise references were corrected in this file after validation (see Validation note)
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (pre-execution): plan for issue 390, CCSESSION_PERMISSIONS=default

Short names used below: PLAN = `.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/TASK-WF-implementGitHubI-20261105-170815.md`; SPEC = `.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/source.md`; `PLAN:<n>` and `SPEC:<n>` mean line n of those files. All other paths are repo-relative.

## Verdict

**FAIL: do not approve the plan as written.** Two independent reviewers (a sonnet-class and a haiku-class model) both reached FAIL; an adversarial merge and a fault-finder probe confirmed it. There are 3 blocking findings and 7 minor ones. All are fixable in a corrected plan; none challenges the design the user chose (option B). The three blocking findings:

1. Task 5 would either make `ccsession --help` print the whole script or fail its own acceptance check (M-F1).
2. Task 1's red-run acceptance wording contradicts one of its own tests (M-F2).
3. Task 1's `bypass` test, built the way the plan says, can run the real `claude` with the bypass flag during the red run (M-F3).

## Run facts (what ran, what degraded)

- Tier 2 ran because the spec has no labeled requirement IDs (parse-density guard) and because three or more domains are touched (rule 4 of the tier rubric) with an unmapped share above 0.20 (rule 5).
- Reviewers: 2 (sonnet class, haiku class). The default is 3. Two were used so the calibrator (opus class) stays disjoint from the reviewers. The plan author's own model class was not resolved, so the anti-self-confirmation guarantee is weaker than designed (`executor_class_resolved: false`).
- Model aliases resolved to 3 distinct models across 2 vendors (`t2_model_class_diversity: full`, `t2_vendor_diversity: multi`).
- Adversarial merge ran for real (not the fallback): `adversarial/merged-verdict.yaml` has `merge_method: adversarial`; two calibrated reviewer cards are in `reviewer-cards/`. Convergence 0.9583 (23 of 24 points) against the 0.80 threshold. **Caveat:** four shared assumptions (A-001, A-003, A-005, A-006) were never debated and were counted as agreed; counted as unresolved the score is 19/24 = 0.79, below the threshold. One point (A-004, whether the variable should stay exported into Claude's environment) is unresolved and is an owner decision.
- Fault-finder probe: 22 findings, 10 addressed, 12 unaddressed (0 high, 5 medium, 7 low). Three of the medium ones became findings M-F3, M-F5 and M-F6; two merged cards' claims were narrowed after the debate (see the merge log).
- No test, `--help` run or red run was executed by any reviewer: every claim about what passes or fails on the old launcher is reasoned from the source.
- Input drift: none. The input tree hash was identical at the start and before this report (`artifacts/input-snapshot.yaml`).
- Not set: `reachability_*` (UC-1; the contracted-sink gate is UC-2 only).

## Coverage matrix and inferred requirements (Pass 2)

The spec is one line with no labeled IDs, so all rows are inferred and quote-pinned to `SPEC:1`. Deterministic containment matching over the Task sections gave `coverage_pct_union` = 0.7143 (5 of 7); `coverage_pct` (parsed-only) is null.

| INF id | Verbatim quote (SPEC:1) | Citation | Match result |
|---|---|---|---|
| INF-001 | a new explicit opt-in environment variable CCSESSION_PERMISSIONS=default | SPEC:1 | Task 1 (0.67) |
| INF-002 | When set, ccsession adds no permission-bypass flag (no --dangerously-skip-permissions) on all six launch lines while keeping shim and tier-model routing | SPEC:1 | Task 1 (0.69) |
| INF-003 | when unset, behavior is unchanged for everyone | SPEC:1 | Task 9 (0.75) |
| INF-004 | Do NOT change how an empty CC_CLAUDE_FLAGS is handled (the :- default stays) | SPEC:1 | none (0.57) |
| INF-005 | Tests must fail on the old code: set -> no bypass flag and shim/model routing kept; unset -> unchanged | SPEC:1 | Task 1 (1.0) |
| INF-006 | Document the variable where ccsession's other variables are documented | SPEC:1 | Task 7 (1.0) |
| INF-007 | Unblocks Coder PR 458 | SPEC:1 | none (0.25) |

Two reviewers and the merge agree that INF-004 and INF-007 are covered by the plan even though the word-count matcher says "none": INF-004 is in the plan's empty-`CC_CLAUDE_FLAGS` constraint (PLAN:20) and in Task 1's tests (PLAN:36); INF-007 is a pull-request description item carried as a delivery note (PLAN:25). No requirement-bearing span of the spec is missing from the matrix.

## Findings (merged card: `adversarial/merged-verdict.yaml`)

Classes use the four-category deviation taxonomy (Authorized expansion, Necessary deviation, Drift, Regression) applied to plan steps that depart from the spec or from an existing guarantee.

### Finding M-F1 (blocking): Task 5 breaks or fails `ccsession --help`

- **Location:** PLAN:95, PLAN:97, PLAN:100 (Task 5)
- **Spec section:** SPEC:1 ("Document the variable where ccsession's other variables are documented")
- **Evidence:** `show_help` prints the header only up to the first line matching `^# The wrapper always runs` (`src/superclaude/skills/ccsession-tag/ccsession:1652`), which is line 109, the very sentence Task 5 rewrites (`src/superclaude/skills/ccsession-tag/ccsession:109`). The permissions paragraph (`src/superclaude/skills/ccsession-tag/ccsession:109-114`) is therefore never in `--help` output; usage entries such as `CCSESSION_SHOW_ALL_MODELS=1` sit above it (`src/superclaude/skills/ccsession-tag/ccsession:96-98`). Rewriting the sentence without the word "always" makes the stop pattern stop matching, so awk prints the entire script. The existing help tests only check substrings (`tests/unit/test_ccsession_tag.py:157-169`, `tests/unit/test_install_ccsession.py:224-238`), so nothing would catch it.
- **Classification:** regression
- **Classification rationale:** the planned edit contradicts the plan's own acceptance criterion and an existing guarantee (`--help` prints a short usage block).
- **Default remediation:** put the new usage entry above the stop line next to line 96; keep line 109's start, or change the pattern at line 1652 in the same edit; reword the criterion at PLAN:100; add a test that `--help` contains `CCSESSION_PERMISSIONS=default` and neither `set -e` nor `CLAUDE_BIN=`.

### Finding M-F2 (blocking): Task 1's red-run criterion contradicts its own test

- **Location:** PLAN:36, PLAN:39 (Task 1)
- **Spec section:** SPEC:1 ("Tests must fail on the old code")
- **Evidence:** the criterion says every test that sets `CCSESSION_PERMISSIONS=default` must fail on the unchanged launcher, but the same task mandates a `CC_CLAUDE_FLAGS=--verbose` plus `default` test; on the old launcher a non-empty `CC_CLAUDE_FLAGS` already replaces the default (`src/superclaude/skills/ccsession-tag/ccsession:124`), so that test passes on old code. The phrase "empty-`CC_CLAUDE_FLAGS` tests pass" is also ambiguous (one such test must fail).
- **Classification:** regression (orchestrator consistency call on the taxonomy; the debate treated it as Drift)
- **Classification rationale:** the plan as written cannot be executed to its own definition of done.
- **Default remediation:** reword to: every test asserting the new default-flag behavior or the bad-value error fails on old code; the `CC_CLAUDE_FLAGS` override test, the empty-variable test and the empty-`CC_CLAUDE_FLAGS`-with-variable-unset test pass.

### Finding M-F3 (blocking): the `bypass` test can start the real `claude` in the red run

- **Location:** PLAN:36, PLAN:39 (Task 1)
- **Spec section:** n/a (safety of the plan's own test method)
- **Evidence:** PLAN:36 models the test on `test_help_and_unknown_profile_list_data_profiles`, which sets only `HOME` (`tests/unit/test_ccsession_tag.py:1145-1153`); `_label_launch` sets a fake `CLAUDE_BIN` and `CCSESSION_ENV_FILE` (`tests/unit/test_ccsession_tag.py:1177-1184`). On the old launcher the variable is ignored, `CLAUDE_BIN` defaults to `claude` (`src/superclaude/skills/ccsession-tag/ccsession:123`) and the launcher execs it with the default flags (`src/superclaude/skills/ccsession-tag/ccsession:1868`), which start with `--dangerously-skip-permissions`; PLAN:39 requires running that test against the unchanged launcher. What the real process then does was not executed.
- **Classification:** drift
- **Classification rationale:** a plan step that is not backed by the spec and risks an unwanted side effect; no spec criterion is contradicted.
- **Default remediation:** build the test on `_label_launch`'s environment through the new `extra_env` argument, add `stdin=subprocess.DEVNULL` and a timeout, and assert the fake Claude did not run.

### Finding M-F4 (minor): the bad-value exit 2 is global and unstated

- **Location:** PLAN:22, PLAN:73-81 (Constraints, Task 4)
- **Evidence:** the plan puts the check at line 124 (PLAN:73; today that line only assigns the default flags, `src/superclaude/skills/ccsession-tag/ccsession:124`), before the whole argument dispatch (`src/superclaude/skills/ccsession-tag/ccsession:1671`), so a typo makes every invocation exit 2, `--help` included. No bypass leaks (`src/superclaude/skills/ccsession-tag/ccsession-orca:247`, `src/superclaude/skills/ccsession-tag/ccsession-orca:249`), but `ccsession-orca` drops a valid session name with a misleading message (`src/superclaude/skills/ccsession-tag/ccsession-orca:132-137`), the hook calls become silent no-ops (`src/superclaude/skills/ccsession-tag/hooks/session-name.sh:196-212`) and the installer's name migration is skipped silently (`src/superclaude/cli/install_ccsession.py:104-113`).
- **Classification:** drift (the plan never justifies the scope; both reviewers' differing labels were settled by the debate)
- **Default remediation:** state "every invocation, including `--help`" in Constraints and add one test (bad value plus `ccsession --help` exits 2), or defer only the exit to the launch paths under M-F5.

### Finding M-F5 (minor, latent): launch-scoping the check can break two plan rules

- **Location:** PLAN:20, PLAN:23 (Constraints)
- **Evidence:** if the whole `case` moved below the env-file sourcing (`src/superclaude/skills/ccsession-tag/ccsession:847-849`), an env-file value would start choosing the flags (against PLAN:23) and an env-file `CC_CLAUDE_FLAGS=""` would take the default (against PLAN:20 and SPEC:1). Add-on profiles can also run before that point (`src/superclaude/skills/ccsession-tag/ccsession:819-836`).
- **Classification:** regression (latent; the plan as written does not do this)
- **Default remediation:** if the check is launch-scoped, keep computing the flags at line 124 and defer only the `exit 2`; say so in Constraints.

### Finding M-F6 (minor): the Goal overstates "through ccsession-orca"

- **Location:** PLAN:15 (Goal)
- **Evidence:** `ccsession-orca` passes Orca's own arguments through unchanged (`src/superclaude/skills/ccsession-tag/ccsession-orca:14-17`) and every launch line appends them (`src/superclaude/skills/ccsession-tag/ccsession:1799`, `src/superclaude/skills/ccsession-tag/ccsession:1868`); the tests model Orca's default option as `--dangerously-skip-permissions` (`tests/unit/test_ccsession_tag.py:1806-1811`), so an Orca tab with the variable set still runs with the bypass. Add-on profiles and the env file can also reassign `CC_CLAUDE_FLAGS` after line 124. The spec's own wording ("ccsession adds no permission-bypass flag", SPEC:1) still holds, and the Coder print-mode path in Task 2 passes no such flag.
- **Classification:** drift
- **Default remediation:** reword the Goal to "ccsession adds no `--dangerously-skip-permissions`" and add one sentence to the Task 5 text, the Task 6 README row and the Task 9 bullet: flags the caller passes, and flags from `CC_CLAUDE_FLAGS`, an add-on profile or the env file, still apply.

### Finding M-F7 (minor): the "not settable from ccsession.env" claim is untested

- **Location:** PLAN:23, PLAN:121, PLAN:148 (Constraints, Tasks 7 and 9)
- **Evidence:** the claim is true by construction (`src/superclaude/skills/ccsession-tag/ccsession:124` runs before the env file is sourced at `src/superclaude/skills/ccsession-tag/ccsession:847-849`), but Task 9 requires every behavior in the changelog bullet to match a test in Tasks 1 to 3 (PLAN:148), and none covers it. PLAN:121 ("this file is read after the launch flags are chosen") is also imprecise.
- **Classification:** regression (orchestrator consistency call; the debate treated it as Drift)
- **Default remediation:** add a Task 1 test that sets the variable inside a `CCSESSION_ENV_FILE` and asserts the argv still starts with `--dangerously-skip-permissions`, or drop the clause from Task 9's acceptance; reword PLAN:121 to "the variable is read before this file is sourced".

### Finding M-F8 (minor): Task 3 and other tests are not isolated from the developer's shell

- **Location:** PLAN:59-60, PLAN:63 (Task 3; PLAN:59-60 show it clears only `CCSESSION_PERMISSIONS`, and PLAN:63 needs the control run to start with the bypass flag, which holds only when `CC_CLAUDE_FLAGS` is unset)
- **Evidence:** the tier tests copy the whole environment (`tests/unit/test_ccsession_tiers.py:362`) and their isolation fixture's delete list does not clear `CC_CLAUDE_FLAGS` (`tests/unit/test_ccsession_tiers.py:112-122`), unlike the existing launch test that Task 1 builds on, which removes it per test (`tests/unit/test_ccsession_tag.py:1251`). A bad exported `CCSESSION_PERMISSIONS` would also make `tests/unit/test_install_ccsession.py:224-238` and `tests/cli/test_update_command.py:198-208` fail (these two sites come from the debate and were not re-read by the orchestrator).
- **Classification:** drift
- **Default remediation:** clear `CC_CLAUDE_FLAGS` and `CCSESSION_PERMISSIONS` in the tier fixture (or pass them explicitly in the new test), and in the two install and update tests, or launch-scope the check under M-F5.

### Finding M-F9 (minor): Task 3's "an existing --tier launch" is ambiguous

- **Location:** PLAN:60 (Task 3)
- **Evidence:** two neighbouring tests pass `--dangerously-skip-permissions` explicitly to `ccsession-orca` (`tests/unit/test_ccsession_tiers.py:445`, `tests/unit/test_ccsession_tiers.py:500`), so copying them would make "contains no bypass flag" unpassable; the plain tier launches do not (`tests/unit/test_ccsession_tiers.py:525`). The risk is low because the plan points at the `_launch` helper.
- **Classification:** drift
- **Default remediation:** name the control invocation (`_launch(tmp_path, "work", "--tier", "tier0")`) and forbid explicit flags in both runs.

### Finding M-F10 (minor): Task 8 leaves a false clause and a stale citation in D08

- **Location:** PLAN:130, PLAN:135 (Task 8)
- **Evidence:** the D08 sentence continues "Claude Code then runs tools without asking", false for an opted-in launch (`docs/testing/v5.0.0/user/D08-ccsession.md:23`); E01 lacks that clause (`docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md:21`). The sentence's `ccsession:78-83,93` citation is stale; the lines are now `src/superclaude/skills/ccsession-tag/ccsession:109-114` and `src/superclaude/skills/ccsession-tag/ccsession:124`.
- **Classification:** drift
- **Default remediation:** tie the clause to the default launch ("by default Claude Code then runs tools without asking") and fix the line citation, keeping to one changed line per file.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 50` = 0.00

## Validation note

The independent evidence-validator (sonnet class, fresh context) re-read all 50 distinct citations: 0 dropped, 7 of 7 quoted requirement spans verbatim in `SPEC:1`. It flagged five imprecise references, corrected in this file: the Task 4 check lines (`PLAN:73-81`, not `PLAN:75`), the range of the tier fixture's delete list (`tests/unit/test_ccsession_tiers.py:112-122`), the origin of the `CC_CLAUDE_FLAGS` clearing in `tests/unit/test_ccsession_tag.py:1251` (an existing test, not Task 1's new ones), the indirect link of `PLAN:63`, and the wording that line 124 already contains the check (it is the plan's proposed replacement). Two second-hand citations (`tests/unit/test_install_ccsession.py:224-238`, `tests/cli/test_update_command.py:198-208`) were re-read and confirmed: both run `ccsession --help` with the inherited environment and `check=True`. The validator's own report is not saved as a file; this note is its record.

## Recommendations

### Recommendation R-001: Rewrite Task 5 around the `--help` stop line

- **File:** PLAN
- **Change:** put the usage entry above `src/superclaude/skills/ccsession-tag/ccsession:109`, keep or move the stop pattern at line 1652 together with the sentence, and add the `--help` guard test.
- **Verifier:** a new test asserting `ccsession --help` contains `CCSESSION_PERMISSIONS=default` and not `set -e`; `uv run pytest tests/unit/test_ccsession_tag.py -k help -q` passes.
- **Linked deviation(s):** M-F1
- **Priority:** P0

### Recommendation R-002: Fix Task 1's criterion and make the `bypass` test safe

- **File:** PLAN
- **Change:** reword the red-run criterion at PLAN:39 and build the `bypass` test on `_label_launch`'s fake `CLAUDE_BIN`, with `stdin=subprocess.DEVNULL`, a timeout, and an assertion that the fake Claude did not run.
- **Verifier:** the saved red log lists exactly the tests that assert new behavior as failing, and no real `claude` process starts during it.
- **Linked deviation(s):** M-F2, M-F3
- **Priority:** P0

### Recommendation R-003: Isolate and pin the tests (Tasks 1 to 3)

- **File:** PLAN
- **Change:** clear `CC_CLAUDE_FLAGS` and `CCSESSION_PERMISSIONS` in the tier fixture and in the install and update tests that run `ccsession`; name the Task 3 control launch; add the env-file test and the `--help` bad-value test.
- **Verifier:** run the suite with `CC_CLAUDE_FLAGS=--verbose` and `CCSESSION_PERMISSIONS=typo` exported and confirm only the intended bad-value test fails.
- **Linked deviation(s):** M-F4, M-F7, M-F8, M-F9
- **Priority:** P1

### Recommendation R-004: State the scope and limits in the plan and the docs

- **File:** PLAN
- **Change:** reword the Goal at PLAN:15, state the "every invocation" scope and the launch-scoping constraint in Constraints, add the "caller flags still apply" sentence to Tasks 5, 6 and 9, and fix the D08 clause and citation in Task 8.
- **Verifier:** re-run `/sc:reflect --mode pre` on the regenerated plan (or re-read PLAN:15, PLAN:22 and the Task 5, 6, 8 and 9 text) and confirm each sentence is present.
- **Linked deviation(s):** M-F4, M-F5, M-F6, M-F10
- **Priority:** P1

### Recommendation R-005: Decide whether the variable stays exported to nested launches

- **File:** n/a (owner decision, unresolved diff point A-004)
- **Change:** record in Constraints whether `CCSESSION_PERMISSIONS` is unset before the final `exec` or deliberately inherited.
- **Verifier:** the regenerated plan's Constraints state the decision and one test covers it.
- **Linked deviation(s):** none (proactive)
- **Priority:** P2
