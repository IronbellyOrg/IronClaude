# Reflect report — UC-1 pre-execution check of TASK-WF-revisedPlanRefac-20261102-213941

```yaml
contract_version: 1.8.0
status: partial            # the adversarial merge returned partial (post-merge re-scan found one stale resolution note; 7 medium invariant warnings carried as findings); no citation was dropped
mode: pre
tier_reached: 2
confidence_calibrated: 0.80   # mean of the three blind-calibrated Tier-2 cards (0.84, 0.75, 0.80); Tier-1 card was 0.77
citations_total: 121
citations_revalidated: 121
citations_dropped: 0
citations_inferred: 2
citation_budget_policy: full_reread   # stricter than required: every citation was re-read; 1 wrong line corrected, 2 wording caveats applied
coverage_degraded: parsed-sparse
plan_verdict: revise-before-execution   # 0 high, 8 medium, 7 low deviations; 1 regression (D-105)
```

## Verdict

The revised plan resolves all 14 deviations from the previous report at plan level, and every one of the 41 spec obligations maps to a task. It still needs one more revision before execution, because its `scripts/eval_runner.py` rewrite (Task 2) cannot be carried out as written:
- The regression test's cited loader crashes on import before testing anything (scripts/eval_runner.py:10, :46-47; shell evidence section 5).
- The failure path of the new temporary checkout is unspecified (plan line 62).
- The new `main()` wiring is untested, and a setup failure still exits 0 (scripts/eval_runner.py:313).
- The tests would write a report into the real checkout (scripts/eval_runner.py:35-43, :307-309).
- The forced removal deletes the outputs the end-to-end scripts write inside the checkout (scripts/eval_1.py:456-459). This is the only regression.

Task 4's upstream ban, read literally, forbids the Orca calls that Task 3 makes mandatory (plan lines 86, 105, 111). The plan also leaves unnamed a CLAUDE.md sentence its own check rejects (CLAUDE.md:50); it says only to edit kept text "where they contradict the rules above" (plan line 113). Task 8's rerun branch leaves no evidence (plan line 176). Seven low findings are wording, stale facts or extra checks; one of them shows that the two old checkouts the plan names no longer exist (plan line 27).

Counts: 15 deviations, 8 medium and 7 low; 13 drift, 1 regression (D-105), 1 authorized (D-113), 0 necessary, 0 high.

How the verdict was reached:
- Tier 1: one inline card, blind-calibrated C 0.77. It escalated because the spec has no requirement IDs (coverage_degraded: parsed-sparse) and the plan spans four domains (docs, config, tests, code).
- Tier 2: three read-only reviewers on different model classes: sonnet (analyzer lens), the haiku slot (glm-5.3, qa lens) and opus (refactorer lens). Blind-calibrated confidence was 0.84, 0.75 and 0.80.
- Merge: `/sc:adversarial` at standard depth chose base reviewer-1 (combined 0.825 against 0.821, tiebreaker on debate wins 4.5 to 0). All 16 debate points were agreed (CONVERGED).
- The merge returned `partial`. The invariant probe raised 7 medium unaddressed items, all carried into the findings below. The post-merge re-scan found one stale note: the merged card's D-004 resolution row still points at a CLAUDE.md:64 half that the merge removed. It was flagged, not hand-patched.

Artifacts (paths relative to this report's directory): `t1-card.md`, `artifacts/` (input snapshot, pass-2 rows, coverage matrix, shell evidence, tier decision, `inf-table.md`), `reviewer-briefs/`, `reviewer-cards/` (cards and calibrations), `adversarial/merged-findings.md`, `adversarial/merged-verdict.yaml`, `adversarial/return-contract.yaml`, `adversarial/adversarial/` (diff analysis, round files, debate transcript, invariant probe, qualitative passes, base selection, refactor plan, merge log), `audit.log`.

## Inferred requirements (Pass 2)

Pass 1 found 0 labeled requirement IDs. Pass 2 (requirements-analyst agent) inferred 41 quote-pinned rows. All cite `.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/source.md:1`, the spec's only line. Match uses the deterministic containment rule (threshold 0.6). "Content-level" is the Tier 1 card's verdict, which reviewer 2 independently re-checked (it tried to refute each one and failed). The table is generated from `artifacts/pass2-inferred.yaml` and `artifacts/coverage-matrix.json` (`artifacts/inf-table.md`).

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "Refactor IronClaude to Orca's default worktree paths" | source.md:1 | containment, Task 1 (0.8571) |
| INF-002 | "replace the .dev/worktrees rule in CLAUDE.md" | source.md:1 | containment, Task 3 (1.0) |
| INF-003 | "every tracked file that encodes .dev/worktrees or git worktree add (git grep -E '\.dev/worktrees\|git worktree add' -- ':!.dev')" (the backslash before the pipe is a Markdown table escape) | source.md:1 | containment, Task 3 (0.7) |
| INF-004 | "Classify each hit as project worktree (move to Orca-created worktrees at Orca's default location) or internal temporary checkout used by a CLI or test (keep working without Orca)." | source.md:1 | containment, Task 1 (0.8421) |
| INF-005 | "project worktree (move to Orca-created worktrees at Orca's default location)" | source.md:1 | containment, Task 1 (0.8889) |
| INF-006 | "internal temporary checkout used by a CLI or test (keep working without Orca)" | source.md:1 | containment, Task 1 (0.7778) |
| INF-007 | "Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with." | source.md:1 | containment, Task 4 (0.9) |
| INF-008 | "Source of truth is src/superclaude" | source.md:1 | containment, Task 6 (1.0) |
| INF-009 | "run make sync-dev" | source.md:1 | containment, Task 7 (1.0) |
| INF-010 | "never stage .claude mirrors" | source.md:1 | none lexically (best Task 4, 0.5); content-level COVERED: plan lines 21, 160, 179 |
| INF-011 | "This revision supersedes plan .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md" | source.md:1 | none lexically (best Task 1, 0.4545); content-level COVERED: plan line 19 |
| INF-012 | "must resolve all 14 deviations in its advisory reflect report .dev/reflect/pre-refactorIronClau-20261102175540/REPORT.md" | source.md:1 | none lexically (best Task 1, 0.2727); content-level COVERED: every D-id named across Tasks 1-8 and Constraints line 24 |
| INF-013 | "Owner decision (2026-11-02): rewrite scripts/eval_runner.py so it creates its master checkout in a temporary directory and removes it when done, making it an internal temporary checkout that works without Orca." | source.md:1 | containment, Task 2 (0.7727) |
| INF-014 | "Owner decision: keep POST-REFLECT-TASK.md unchanged as a third class, Historical record." | source.md:1 | containment, Task 1 (0.75) |
| INF-015 | "D-001 scripts/eval_runner.py:138-147 list-argument git worktree add, never removed, invisible to the spec grep (apply the owner decision" | source.md:1 | containment, Task 2 (0.8095) |
| INF-016 | "add a list-argument search to the inventory and the final residual check" | source.md:1 | none lexically (best Task 2, 0.5); content-level COVERED: plan lines 20, 35, 172, 177 |
| INF-017 | "D-002 Task 3 must name and rewrite CLAUDE.md pre-PR check 1 (bare gh repo view, CLAUDE.md:64)" | source.md:1 | containment, Task 4 (0.9412) |
| INF-018 | "check 3 (close it immediately, CLAUDE.md:66) so the agent stops and reports and the user closes a misrouted PR" | source.md:1 | containment, Task 4 (0.7143) |
| INF-019 | "must list the allowed forms for gh commands that take a positional repo" | source.md:1 | containment, Task 4 (1.0) |
| INF-020 | "D-003 nine list-argument worktree add lines (8 plus eval_runner.py:143) need their own search total" | source.md:1 | containment, Task 1 (0.6316) |
| INF-021 | "a class per file without breaking the count check" | source.md:1 | containment, Task 1 (0.6667) |
| INF-022 | "D-004 the repository has only an origin remote, so word the upstream rule without depending on a remote named upstream" | source.md:1 | containment, Task 4 (0.8182) |
| INF-023 | "record the source of Orca's project id as unverified" | source.md:1 | containment, Task 4 (0.8571) |
| INF-024 | "D-005 narrow 'no tool call or link' to tool calls and gh or Orca link flags" | source.md:1 | containment, Task 4 (0.8) |
| INF-025 | "state that static references in docs and test fixtures are out of scope" | source.md:1 | containment, Task 4 (0.875) |
| INF-026 | "decide the CLAUDE.md:251 issue link explicitly" | source.md:1 | containment, Task 4 (0.8571) |
| INF-027 | "D-006 note in the inventory that POST-REFLECT-TASK.md is Blocked and its paths are intentionally stale" | source.md:1 | containment, Task 1 (1.0) |
| INF-028 | "reported first in the summary" | source.md:1 | containment, Task 1 (0.6667) |
| INF-029 | "D-007 label the .gitignore row rewrite comment only" | source.md:1 | containment, Task 1 (0.875) |
| INF-030 | "keep the entry as a retired-path guard" | source.md:1 | containment, Task 1 (1.0) |
| INF-031 | "D-008 prove internal checkouts still work by running their tests with -rs and requiring zero skips or a recorded reason" | source.md:1 | containment, Task 8 (0.75) |
| INF-032 | "a rerun in a full-depth, non-root checkout" | source.md:1 | containment, Task 8 (0.8333); rerun leaves no evidence (D-108) |
| INF-033 | "D-009 the fetch and pull ban is a literal reading" | source.md:1 | containment, Task 4 (1.0) |
| INF-034 | "the dated Orca project-id note is an authorized addition" | source.md:1 | containment, Task 4 (0.8571) |
| INF-035 | "D-010 add the Orca flags --json, --issue and --pr to the confirmed command list" | source.md:1 | containment, Task 4 (0.8182) |
| INF-036 | "D-011 add tests/skills/test_sc_recommend_routing_contract.py to the sync and parity test run" | source.md:1 | containment, Task 7 (0.9286) |
| INF-037 | "D-012 describe the /sc:post-release tag checkout as an optional read-only checkout removed after the scan" | source.md:1 | containment, Task 3 (1.0) |
| INF-038 | "D-013 say in the new worktree rule what happens to the two existing checkouts under the retired .dev/worktrees location" | source.md:1 | containment, Task 3 (0.9333) |
| INF-039 | "(do not move or remove them in this plan)" | source.md:1 | none lexically (best Task 1, 0.5); content-level COVERED: plan line 27 (now stale, see D-109) |
| INF-040 | "D-014 note docs/swarm/runbook.md:34's .claude/worktrees path" | source.md:1 | containment, Task 1 (1.0) |
| INF-041 | "The eval_runner.py rewrite is a behaviour change and needs a regression test." | source.md:1 | containment, Task 2 (0.7778); test not runnable as written (D-101, D-103) |

Coverage: coverage_pct null (no parsed IDs), coverage_pct_union 0.878 (36 of 41 lexical), S_dev_density 0.122. Content level: all 41 covered. The deviations below are about how well the plan meets them, not about missing obligations.

Note on ids: the source's own "D-001..D-014" are the previous report's deviations. This report numbers its deviations D-101..D-115 to keep the two sets apart.

## Deviations

"Plan" below means `.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md`. These are deviations of the PROPOSED plan from its spec, found before execution. Classes are from the 4-category taxonomy; in pre-execution mode "regression" means the plan as written would remove existing behaviour. Merged finding ids from `adversarial/merged-findings.md` are in brackets.

### Deviation D-101: Task 2's test loader crashes on import, so the before and after runs test nothing [R1-1]

- **Location:** plan line 67
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:1, INF-041 "needs a regression test"
- **Evidence:** Plan line 67: "It loads the script with `importlib.util.spec_from_file_location` (the pattern at tests/swarm/test_bare_review_golden_regen.py:153)". That pattern (tests/swarm/test_bare_review_golden_regen.py:157-158) runs `module_from_spec` then `exec_module` with no `sys.modules` entry. scripts/eval_runner.py:10 is `from __future__ import annotations` and :46-47 is `@dataclass` / `class RunResult:`. Shell evidence section 5 (artifacts/t1-shell-evidence.txt:25-27): the unregistered load fails with "AttributeError 'NoneType' object has no attribute '__dict__'"; the registered load succeeds.
- **Classification:** drift
- **Classification rationale:** The plan's cited method cannot meet its own test requirement; nothing authorizes the gap. All three advocates agreed on `drift` (X-003, 100%).
- **Default remediation:** In Task 2, register the module with `monkeypatch.setitem(sys.modules, spec.name, module)` before `exec_module`, and require that `./artifacts/t2-fail-before.txt` fail on the missing `master_checkout`, not on the AttributeError.

### Deviation D-102: The temporary checkout's failure path is unspecified [R1-2]

- **Location:** plan lines 62, 64
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:1, INF-013 "creates its master checkout in a temporary directory and removes it when done"
- **Evidence:** Plan line 62: "On a non-zero exit it raises an error carrying git's stderr. In `finally` it runs `git worktree remove --force <that directory>` (never `rm -rf`)". Plan line 64 names no exception type for the `global-setup` path. scripts/eval_runner.py:70 runs pytest with `timeout=120`. Shell evidence section 6 (artifacts/t1-shell-evidence.txt:29-30): removing a directory that was never registered exits 128 and leaves the directory. The repo's own teardown model guards each step separately (tests/troubleshoot/backtest/git_replay.py:199-205).
- **Classification:** drift
- **Classification rationale:** A failed add would leak the temporary directory and could replace git's error. A broad catch would report a pytest timeout as a setup failure, and a failing teardown could hide the body's exception (debate C-002, X-004 medium; invariant INV-004).
- **Default remediation:** Specify a dedicated `MasterCheckoutError`. On a failed add, remove the directory while tolerating its absence, then raise before any try/finally. Put try/finally around the `yield` only, log teardown failures without raising them, and have `main` catch only `MasterCheckoutError`.
- **[INFERRED] notes:** [INFERRED] git may already delete the target directory on some add failures, so a plain `os.rmdir` could raise `FileNotFoundError` (INV-003).

### Deviation D-103: The new `main()` wiring is untested, and a setup failure still exits 0 [M-1]

- **Location:** plan lines 64, 68-71, 74; scripts/eval_runner.py:267-269, :294-295, :313
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:1, INF-041
- **Evidence:** Plan line 64: "append a `RunResult` named `global-setup` with `errors=1` ... do not fail silently." Plan lines 68-71 list four tests, all on `master_checkout()` or a source grep. Plan line 74: "the same tests fail against the pre-change `scripts/eval_runner.py`". scripts/eval_runner.py:269 is `args = parser.parse_args()`. Lines :294-295 hold the `IronClaude-eval-master` path and the `if worktree_path.exists():` guard. Line :313 counts only runs whose names start with "local".
- **Classification:** drift
- **Classification rationale:** The `global-setup` path, the `run_global(run_id, checkout)` signature and the end-to-end block are never exercised. Three of the four tests fail before the change only because the function is missing. A test that pins the current exit code would pass before the change too, breaking plan line 74 (debate C-003, X-005; invariants INV-005, INV-006, INV-014).
- **Default remediation:** Add a `main()` test with `--mode global` and `sys.argv` patched, asserting a `global-setup` result with errors=1. State the exit-code rule for line 313, name what replaces the guard at lines 294-295, and let plan line 74 exempt named characterization tests. Say that using local `master` is deliberate.

### Deviation D-104: The tests are not isolated from the real checkout [M-2]

- **Location:** plan line 67; scripts/eval_runner.py:35-43, :150-156, :297-298, :307-309
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:1, INF-041
- **Evidence:** Plan line 67 points only `REPO_ROOT` at the throwaway repo. `RESULTS_DIR` is computed from `REPO_ROOT` when the module loads (scripts/eval_runner.py:35-43), and `main()` writes `eval-report.json` there (:307-309). `git check-ignore .dev/releases/current/v3.0_unified-audit-gating/eval-results/eval-report.json` exits 1, so nothing ignores it (orchestrator, 22:54Z). The fixture has none of the eval files or end-to-end scripts, so `run_global` returns early (:150-156) and the end-to-end loop skips every script (:297-298). The repo's test convention strips `GIT_*` variables and sets `GIT_CONFIG_GLOBAL=/dev/null` (tests/skills/test_implement_retry_revert.py:33-34).
- **Classification:** drift
- **Classification rationale:** A `main()` test would leave an untracked file under the real `.dev/releases/`, which plan line 20 forbids, and the body of `with master_checkout()` is never reached (invariants INV-001, INV-010, INV-015).
- **Default remediation:** Patch `RESULTS_DIR` to `tmp_path`, and seed the fixture with one eval file and one script stub. Build it with `git init -b master`, a local identity and a clean git environment, and assert `git status --porcelain` of the real repo is unchanged.

### Deviation D-105: The forced removal deletes the end-to-end scripts' outputs [M-3]

- **Location:** plan lines 62, 64; scripts/eval_runner.py:300; scripts/eval_1.py:456-459
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:1, INF-013
- **Evidence:** Plan line 64 wraps the global end-to-end scripts in `with master_checkout()`. Plan line 62 removes the checkout with `--force`. scripts/eval_runner.py:300 runs each script with the checkout as its working directory. scripts/eval_1.py:456-459 writes to `eval-results/...` relative to that directory unless `--output-dir` is given. scripts/eval_runner.py:118 keeps only the last 500 characters of stderr.
- **Classification:** regression
- **Classification rationale:** The old persistent checkout kept these outputs; the plan as written deletes them at teardown, removing existing behaviour (invariant INV-013).
- **Default remediation:** In Task 2, pass `--output-dir` (or copy `eval-results/`) to a folder under the real `RESULTS_DIR` before teardown, or state explicitly that the outputs are discarded.

### Deviation D-106: Task 4's upstream ban, read literally, forbids the Orca calls Task 3 requires [R1-3]

- **Location:** plan lines 86, 88, 105, 111
- **Mapped tasklist item:** Task 3, Task 4
- **Spec section:** source.md:1, INF-002 and INF-007
- **Evidence:** Plan line 86 makes `orca worktree create --name <name>` the only way to create a project worktree. Plan line 88 forbids Orca link flags outright. Plan line 105 bans any "tool call (gh, git or Orca) ... that resolves to" the upstream repo. Plan line 111 records that Orca identifies this project as `github:superclaude-org/superclaude_framework` and bans link flags only "until" that changes.
- **Classification:** drift
- **Classification rationale:** Because Orca's project id names the upstream repo, a literal reader cannot use Orca at all. The same rule also appears at three strengths across two tasks (invariant INV-012; reviewer-1 R1-3).
- **Default remediation:** Qualify plan line 105 so only link flags and calls that reach the network count as interacting with upstream, and use one wording for the link-flag rule in Tasks 3 and 4.

### Deviation D-107: The plan keeps two CLAUDE.md sentences that conflict with its new rules [R1-4]

- **Location:** plan lines 113, 117; CLAUDE.md:50, CLAUDE.md:70
- **Mapped tasklist item:** Task 4
- **Spec section:** source.md:1, INF-017 and INF-019
- **Evidence:** Plan line 113 keeps the `/sc:pr-submit` instruction and the Rationale paragraph, "editing them only where they contradict the rules above", but names neither line below. Plan line 117 requires every `gh` line in the section to name `IronbellyOrg/IronClaude`. CLAUDE.md:50 reads "It opens the PR with `gh pr create --repo <repo>`, where `<repo>` comes from the `origin` remote". CLAUDE.md:70 reads "only this CLAUDE.md rule + explicit `--repo` on every invocation does."
- **Classification:** drift
- **Classification rationale:** Line 50's placeholder fails the plan's own check, and the plan leaves its rewrite to the executor's judgment instead of naming it; line 70 contradicts the positional `gh repo view` form the plan allows (debate C-004).
- **Default remediation:** Name CLAUDE.md:50 and :70 in Task 4. Rewrite line 50 to say the repo is resolved from origin and must be `IronbellyOrg/IronClaude`, and line 70 to "the repo named explicitly on every gh call".

### Deviation D-108: Task 8's rerun branch leaves no evidence [R2-F1]

- **Location:** plan lines 170, 176
- **Mapped tasklist item:** Task 8
- **Spec section:** source.md:1, INF-031 and INF-032
- **Evidence:** Plan line 176 allows a recorded skip followed by a rerun "in a full-depth ... non-root ... checkout with no SKIPPED line" but names no file for it. Plan line 170 records the depth and user probes only for the first run. This checkout is already full-depth and non-root (artifacts/t1-shell-evidence.txt:8-9).
- **Classification:** drift
- **Classification rationale:** Once a skip exists, the only passing path cannot be checked afterwards, and it does not say how to get a different checkout (uncontested in both debate rounds).
- **Default remediation:** Save the rerun to `./artifacts/t8-internal-checkouts-rerun.txt` with that checkout's `git rev-parse --is-shallow-repository` and `id -u`. Name how it is obtained: a local full clone or linked worktree of this repo, never a fetch from the upstream repo.

### Deviation D-109: The two old checkouts the plan names no longer exist [M-4]

- **Location:** plan lines 27, 44, 51, 90
- **Mapped tasklist item:** Task 1, Task 3
- **Spec section:** source.md:1, INF-038 and INF-039
- **Evidence:** Plan line 27 lists `/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates` and `.../markdownlint-issue-body-files` from `git worktree list` on 2026-11-02. At 22:40Z, `git worktree list` had no `/.dev/worktrees/` line and neither directory existed (orchestrator check).
- **Classification:** drift
- **Classification rationale:** A plan fact went stale after it was written. Task 1's section would be empty, its check (plan line 51) would pass vacuously, and the rule at plan line 90 would describe nothing (invariant INV-009).
- **Default remediation:** Have Task 1 record the live worktree list, and reword plan lines 27 and 90 to "any checkout found at the retired location".

### Deviation D-110: No check for a leftover eval checkout from past runs [R2-F3]

- **Location:** plan line 44; scripts/eval_runner.py:138
- **Mapped tasklist item:** Task 1
- **Spec section:** source.md:1, INF-015 "never removed"
- **Evidence:** Plan line 44 records only `/.dev/worktrees/` lines. scripts/eval_runner.py:138 creates `REPO_ROOT.parent / "IronClaude-eval-master"`. At 22:23Z no such checkout existed on this host (orchestrator check).
- **Classification:** drift
- **Classification rationale:** This is a completeness gap only: the plan would not notice a leftover on another machine.
- **Default remediation:** Have Task 1 record any `IronClaude-eval-master` entry and either remove it or record it with a reason.

### Deviation D-111: The teardown check greps source formatting [R3-F8]

- **Location:** plan line 75
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:1, INF-013
- **Evidence:** Plan line 75: "`grep -n 'worktree", "remove"' scripts/eval_runner.py` prints the teardown line".
- **Classification:** drift
- **Classification rationale:** If the argument list is formatted one item per line, the grep fails although teardown exists.
- **Default remediation:** Rely on the behavioural `git worktree list` test at plan line 68, or loosen the grep to `"remove"`.

### Deviation D-112: The gh-line check matches ordinary words and the whole file [R1-5]

- **Location:** plan line 117
- **Mapped tasklist item:** Task 4
- **Spec section:** source.md:1, INF-019
- **Evidence:** Plan line 117 saves the check from `grep -n 'gh ' CLAUDE.md`.
- **Classification:** drift
- **Classification rationale:** `gh ` also matches "through ", "though " and "enough ", and the criterion is about one section, not the whole file.
- **Default remediation:** Use `awk '/^## ABSOLUTE RULE: PR Target/,/^## ABSOLUTE RULE: Never Hardcode/' CLAUDE.md | grep -n -w 'gh'` and save that output.

### Deviation D-113: The pr-submit scripts' guarded fallback is out of scope [R1-6]

- **Location:** src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:34-35
- **Mapped tasklist item:** unmapped (out of scope)
- **Spec section:** source.md:1, INF-007
- **Evidence:** poll-ci-checks.sh:34 resolves the repo from `git remote get-url origin`; line 35 falls back to a bare `gh repo view` only when that is empty. The same pattern is at poll-augment-review.sh:21-22, retrigger-review.sh:49-50 and reply-resolve-thread.sh:56-57. The spec asks to tighten "the CLAUDE.md rule".
- **Classification:** authorized
- **Classification rationale:** Leaving the scripts unchanged is within the spec's CLAUDE.md scope; reviewer 3 conceded this in Round 2 (debate X-001).
- **Default remediation:** Optionally add one sentence to Task 4 saying the guarded fallbacks are not covered by the allowed-forms list and stay unchanged.

### Deviation D-114: Task 8's residual check has no class for files created after Task 1 [R3-F6]

- **Location:** plan lines 46, 177
- **Mapped tasklist item:** Task 2, Task 8
- **Spec section:** source.md:1, INF-016
- **Evidence:** Plan line 46 reclassifies new hits only inside Task 1. Plan line 177 requires every remaining Search A line to be in a classified file.
- **Classification:** drift
- **Classification rationale:** Task 2 creates `tests/unit/test_eval_runner_master_checkout.py` after the inventory (invariant INV-007).
- **Default remediation:** Have Task 2 add an inventory row for the new test file, and have Task 8 re-run both searches and classify any new file before the residual check.
- **[INFERRED] notes:** [INFERRED] The new test file will contain text that matches one of the searches.

### Deviation D-115: Three "no change" checks use plain `git diff` [R3-F5]

- **Location:** plan lines 119, 148, 178
- **Mapped tasklist item:** Task 4, Task 6, Task 8
- **Spec section:** source.md:1, INF-031
- **Evidence:** Plan lines 119, 148 and 178 use `git diff` or `git diff --stat`, which compare the working tree with the index. The executor snapshots in a temporary index and is told not to `git add` to the user index (src/superclaude/skills/sc-implement-protocol/SKILL.md:111, :125). The plan stages only `.dev/tasks/` (plan lines 29, 179).
- **Classification:** drift
- **Classification rationale:** The checks go blind only if someone stages source files by hand, so this is low hardening (debate, round2-v3.md).
- **Default remediation:** Use `git diff HEAD` and `git diff HEAD --stat` at plan lines 119, 148 and 178.

## Inferred-claim audit
- `citations_inferred: 2` (D-102: git may delete the target directory on a failed add; D-114: the new test file will match a search)
- Inferred-fraction: `2 / 121` = 0.02

Evidence-validator (full re-read, 22:53Z): 121 of 121 citations re-read; 0 unfounded; 1 wrong line corrected (D-104 `:150` -> `:150-156`); 1 runtime claim re-probed by the orchestrator at 22:54Z (`git check-ignore` on the exact report path, exit 1); 2 wording caveats applied (D-107 and the Verdict now quote plan line 113's "editing them only where they contradict the rules above"; D-111's quote lost the YAML backslash escapes). The validator independently confirmed the runtime claims behind D-105, D-109 and D-110.

## Recommendations

### Recommendation R-101: Make Task 2's regression test runnable and isolated

- **File:** .dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md (Task 2, lines 62-76)
- **Change:** Add module registration in `sys.modules` and a typed `MasterCheckoutError` with a teardown that never raises over the body. Add a `main()` global-setup test with argv and `RESULTS_DIR` patched, a seeded fixture with a clean git environment, an exit-code decision for scripts/eval_runner.py:313, a named replacement for the guard at :294-295, and a fail-before rule that exempts named characterization tests.
- **Verifier:** In the next plan, Task 2's text names each item. On execution, `./artifacts/t2-fail-before.txt` fails on the missing `master_checkout` (no AttributeError), and `git status --porcelain` of the real repo is unchanged after the test run.
- **Linked deviation(s):** D-101, D-102, D-103, D-104
- **Priority:** P0

### Recommendation R-102: Decide what happens to the end-to-end outputs

- **File:** same plan, Task 2 (lines 62, 64)
- **Change:** Either pass `--output-dir` under the real `RESULTS_DIR` to each global end-to-end script, or state that their outputs are discarded.
- **Verifier:** The next plan's Task 2 names the choice; on execution, `eval-results` output from a global run exists outside the removed checkout, or the plan says it is discarded.
- **Linked deviation(s):** D-105
- **Priority:** P0

### Recommendation R-103: Make the Orca rule and the upstream ban agree, and fix the kept CLAUDE.md lines

- **File:** same plan, Tasks 3 and 4 (lines 86-90, 105-119)
- **Change:** Qualify plan line 105 so only link flags and network calls count as interaction. Use one link-flag wording in both tasks, name and rewrite CLAUDE.md:50 and :70, and use the section-scoped whole-word gh check.
- **Verifier:** After execution, `awk '/^## ABSOLUTE RULE: PR Target/,/^## ABSOLUTE RULE: Never Hardcode/' CLAUDE.md | grep -n -w 'gh'` shows only lines naming `IronbellyOrg/IronClaude` or stating a prohibition.
- **Linked deviation(s):** D-106, D-107, D-112
- **Priority:** P1

### Recommendation R-104: Make Task 8's evidence checkable

- **File:** same plan, Task 8 (lines 170-179)
- **Change:** Save the rerun with its probes to `./artifacts/t8-internal-checkouts-rerun.txt`, re-run both searches and classify new files before the residual check, and use `git diff HEAD` at lines 119, 148 and 178.
- **Verifier:** The next plan's Task 8 acceptance criteria name the rerun artifact and `git diff HEAD`.
- **Linked deviation(s):** D-108, D-114, D-115
- **Priority:** P1

### Recommendation R-105: Refresh stale facts and small checks

- **File:** same plan, lines 27, 44, 75, 90, 113
- **Change:** Replace the two named old checkouts with "any checkout found at the retired location", record any leftover `IronClaude-eval-master` entry, replace the teardown grep with the behavioural test, and optionally note that the pr-submit fallbacks stay unchanged.
- **Verifier:** `git worktree list` output saved in Task 1 matches the plan's wording.
- **Linked deviation(s):** D-109, D-110, D-111, D-113
- **Priority:** P2
