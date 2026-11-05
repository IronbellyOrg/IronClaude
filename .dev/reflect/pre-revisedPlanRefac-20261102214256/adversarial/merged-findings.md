<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer-1, sonnet, analyzer) -->
<!-- Merge date: 2026-11-02T22:43:17Z -->

```yaml
reviewer: merged
base: variant-1
# Orchestrator verification carried from the base (2026-11-02 ~21:49Z, artifacts/t1-shell-evidence.txt sections 5-6):
#   R1-1 CONFIRMED: the unregistered importlib load of scripts/eval_runner.py raises
#         "AttributeError 'NoneType' object has no attribute '__dict__'"; with sys.modules[spec.name] = module it loads.
#   R1-2 CONFIRMED: `git worktree remove --force <unregistered mkdtemp dir>` exits 128 and the directory remains.
findings:
  # ---------------- medium ----------------
  - id: R1-1
    headline: "Task 2's test loader pattern can crash on import because eval_runner.py uses @dataclass under `from __future__ import annotations`"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:67"
    classification: drift
    severity: medium
    evidence: "Plan :67 'It loads the script with `importlib.util.spec_from_file_location` (the pattern at tests/swarm/test_bare_review_golden_regen.py:153)'. tests/swarm/test_bare_review_golden_regen.py:157-158 'module = importlib.util.module_from_spec(spec) / spec.loader.exec_module(module)' (no sys.modules). scripts/eval_runner.py:10 'from __future__ import annotations'; scripts/eval_runner.py:46-47 '@dataclass / class RunResult:'."
    rationale: "A module executed without being put in sys.modules crashes @dataclass processing of string annotations, so the regression test would fail at import for a reason unrelated to the feature (confirmed by the orchestrator)."
    recommendation: "In Task 2's test description add: register the module in sys.modules before `exec_module`, using `monkeypatch.setitem(sys.modules, spec.name, module)` so pytest removes it at teardown. `./artifacts/t2-fail-before.txt` must fail on the missing `master_checkout`, not on `'NoneType' object has no attribute '__dict__'`."
    provenance: "Base V1 R1-1; recommendation sharpened from V3 R3-F1 (failure-string criterion, monkeypatch.setitem). Debate C-001 (V3 content, V1 label, 95%), X-003 (`drift`, 100%). Change 1."
  - id: R1-2
    headline: "Task 2's master_checkout failure path is unspecified: a failed add leaks the mkdtemp directory, a failing teardown can hide the body's exception, and a broad catch would report body errors as global-setup"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:62"
    classification: drift
    severity: medium
    evidence: "Plan :62 'On a non-zero exit it raises an error carrying git's stderr. In `finally` it runs `git worktree remove --force <that directory>` (never `rm -rf`)'. Plan :64 'If the checkout cannot be created, append a `RunResult` named `global-setup` with `errors=1` and git's stderr in `failures`; do not fail silently.' Plan :70 'a repo with no `master` branch makes `master_checkout()` raise with git's stderr'. scripts/eval_runner.py:70 'proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)'. tests/troubleshoot/backtest/git_replay.py:200 'Best-effort teardown. Each subprocess step is wrapped in its OWN try/except (P2-1):'."
    rationale: "If `git worktree add` fails the directory is not a registered worktree, so `git worktree remove` fails (exit 128, confirmed), can replace git's add stderr, and the temp directory stays. Plan :64 names no exception type, so an executor may write a broad catch that turns a body error such as the 120 s pytest timeout (eval_runner.py:70) into a false global-setup result. The plan does not say whether a failing teardown may replace the body's exception; the repo's own model (git_replay.py:199-205) guards each teardown call separately. A plain `os.rmdir` could raise FileNotFoundError if the directory is already gone [INFERRED, INV-003]."
    recommendation: "Task 2: raise a dedicated `MasterCheckoutError`. On a failed add, remove the mkdtemp directory while tolerating its absence (`shutil.rmtree(..., ignore_errors=True)` or `contextlib.suppress(FileNotFoundError)`) and raise before any try/finally. Put try/finally around the `yield` only. Log teardown failures and never raise them over the body's exception. `main` catches only `MasterCheckoutError`. Pin the no-master test to git's add message and assert the mkdtemp directory no longer exists."
    provenance: "Base V1 R1-2 (leak and masking points); restructured with V3 R3-F3 (typed error, narrow catch, eval_runner.py:70 timeout); INV-003, INV-004. Debate C-002 (V3, 95%), X-004 (medium, 90%; V1 conceded in round2-v1.md). Severity low -> medium. Change 2."
  - id: M-1
    headline: "Task 2's new main() wiring and global-setup path are untested, the fail-before rule cannot hold for them, and a global-setup failure still exits 0"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:64"
    classification: drift
    severity: medium
    evidence: "Plan :64 'If the checkout cannot be created, append a `RunResult` named `global-setup` with `errors=1` and git's stderr in `failures`; do not fail silently.' Plan :74 'the same tests fail against the pre-change `scripts/eval_runner.py`'. Plan :68-71 (all four tests target `master_checkout()` or a source grep). scripts/eval_runner.py:269 'args = parser.parse_args()'. scripts/eval_runner.py:294-295 'worktree_path = REPO_ROOT.parent / \"IronClaude-eval-master\"' / 'if worktree_path.exists():'. scripts/eval_runner.py:313 'if any(r.failed > 0 or r.errors > 0 for r in runs if r.name.startswith(\"local\")):'."
    rationale: "Three of the four tests fail before the change only because `master_checkout` does not exist; the global-setup path, the `run_global(run_id, checkout)` signature and the E2E block inside the `with` are never exercised. `main()` parses `sys.argv` (eval_runner.py:267-269), so under pytest it exits 2 unless argv is patched (INV-005). The exit code counts only `local*` runs (eval_runner.py:313), so a global-setup failure exits 0, and a characterization test of that behaviour passes before the change too, which breaks plan :74 as written (INV-006). The plan does not name what replaces the `if worktree_path.exists()` guard at eval_runner.py:294-295. Local `master` can lag `origin/master` (A-001)."
    recommendation: "Task 2: add a `main()` test with `--mode global` and `sys.argv` patched (REPO_ROOT at a no-master repo; run_pytest, run_e2e_script and RESULTS_DIR patched) asserting a `global-setup` RunResult with errors=1 and git's stderr. Decide and state the exit-code rule at eval_runner.py:313. Name the replacement for the `if worktree_path.exists()` guard (eval_runner.py:294-295). Restate plan :74 so every new test must fail before the change or be named as a characterization test. Say the eval checkout deliberately uses local `master`."
    provenance: "New. V3 R3-F2 and R3-F9 (exit code); V2 R2-F2; round2-v1.md new evidence eval_runner.py:294-295; INV-005, INV-006, INV-014 (gate chain); A-001 caveat. Debate C-003 (V3, 95%), X-005 (medium, 90%). R3-F9 folded in per 'Changes NOT being made'. Change 3."
  - id: M-2
    headline: "Task 2's tests are not isolated from the real checkout and never reach the body of `with master_checkout()`"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:67"
    classification: drift
    severity: medium
    evidence: "Plan :67 'builds a throwaway git repo in pytest `tmp_path` with a commit on `master`, and points the module's `REPO_ROOT` at it.' scripts/eval_runner.py:35-36 'REPO_ROOT = Path(__file__).resolve().parent.parent' / 'RESULTS_DIR = ('. scripts/eval_runner.py:307-309 'RESULTS_DIR.mkdir(parents=True, exist_ok=True)' / 'report_path = RESULTS_DIR / \"eval-report.json\"' / 'report_path.write_text(json.dumps(report, indent=2))'. scripts/eval_runner.py:150 'missing = [f for f in EVAL_FILES if not (worktree_path / f).exists()]'. scripts/eval_runner.py:297-298 'script_path = worktree_path / script' / 'if script_path.exists():'. tests/skills/test_implement_retry_revert.py:33-34 'env = {k: v for k, v in os.environ.items() if not k.startswith(\"GIT_\")}' / 'env[\"GIT_CONFIG_GLOBAL\"] = \"/dev/null\"'. Orchestrator 22:40Z: `git check-ignore` exits 1 for .dev/releases/current/x."
    rationale: "RESULTS_DIR is computed at import from the real repo, so patching REPO_ROOT does not move it; a `main()` test writes an untracked eval-report.json under the real .dev/releases/, which plan :20 forbids and plan :178 `git diff --stat` would not show (INV-001). The fixture has none of EVAL_FILES or E2E_SCRIPTS, so `run_global` returns early at :150-156 and the E2E loop skips every script at :297-298; teardown after real work is never exercised (INV-010). Without `git init -b master` and a local identity the fixture depends on the host's init.defaultBranch and user config (R3-F7, kept as hygiene); the repo convention also strips GIT_* and sets GIT_CONFIG_GLOBAL=/dev/null (INV-015)."
    recommendation: "Task 2: patch `RESULTS_DIR` to `tmp_path`. Seed the fixture with at least one EVAL_FILES entry and one E2E script stub, or test the `with` body separately. Build the fixture with `git init -b master`, a local identity, `GIT_*` removed and `GIT_CONFIG_GLOBAL=/dev/null`. Assert nothing new appears under the real repo (`git status --porcelain` unchanged)."
    provenance: "New. INV-001, INV-010, INV-015 (probe); V3 R3-F7 folded in per 'Changes NOT being made'. Change 4."
  - id: M-3
    headline: "Removing the temporary checkout with `--force` deletes the outputs the global E2E scripts wrote inside it"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:64"
    classification: regression
    severity: medium
    evidence: "Plan :64 'wrap the whole global block (`run_global(\"A\")`, `run_global(\"B\")` and the global E2E scripts) in one `with master_checkout() as checkout:`'. Plan :62 'In `finally` it runs `git worktree remove --force <that directory>`'. scripts/eval_runner.py:300 'e2e_runs.append(run_e2e_script(script, \"global\", worktree_path))'. scripts/eval_1.py:456-459 'if args.output_dir:' / 'output_dir = Path(args.output_dir)' / 'else:' / 'output_dir = Path(f\"eval-results/eval-1-wiring-gate/{args.branch}-{timestamp}\")'. scripts/eval_runner.py:118 'result.failures.append(f\"Exit code {proc.returncode}: {proc.stderr[-500:]}\")'."
    rationale: "The E2E scripts run with the checkout as cwd and write `eval-results/...` relative to it; `RunResult` keeps only the last 500 characters of stderr. The old persistent checkout kept these outputs; the new forced removal deletes them, so the plan as written removes existing behaviour (INV-013). eval_1.py's default `--spec-file` (eval_1.py:432) is also relative to cwd, so it resolves inside the checkout; whether that file exists on master is [INFERRED]."
    recommendation: "Task 2: pass `--output-dir` (or copy `eval-results/`) to a location under the real `RESULTS_DIR` before teardown, or state explicitly that global E2E outputs are discarded."
    provenance: "New. INV-013 (probe; orchestrator-confirmed 22:40Z). Change 5."
  - id: R1-3
    headline: "Tasks 3 and 4 state the Orca rule at different strengths, and plan :105 read literally forbids the local Orca calls plan :86 requires"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:88"
    classification: drift
    severity: medium
    evidence: "Plan :86 'every project worktree is created through Orca with `orca worktree create --name <name>`'. Plan :88 'Forbid Orca link flags (`--issue`, `--pr`) for this repo, pointing to the fork rule edited in Task 4.' Plan :105 'no tool call (gh, git or Orca) and no gh or Orca link flag that resolves to it.' Plan :111 'Orca identified this project as `github:superclaude-org/superclaude_framework` in `orca worktree current --json` on 2026-11-02' and 'until `orca worktree current --json` shows the fork's project id, `--issue`, `--pr` and other Orca link flags are never passed for this repo.'"
    rationale: "The same CLAUDE.md would carry three different strengths for one rule, and a reader cannot tell when the ban lifts. Because Orca's project id names the upstream repo, every Orca call on this project can be read as one that 'resolves to' upstream, so a literal reading of plan :105 forbids the `orca worktree create` path that plan :86 makes mandatory (INV-012)."
    recommendation: "Task 4: qualify plan :105 so only link flags and calls that reach the network count as interaction with upstream. Use one wording for the Orca link-flag rule in Tasks 3 and 4 (for example, Task 3 says 'Orca link flags are governed by the fork rule below')."
    provenance: "Base V1 R1-3 (U-001); merged with INV-012 (probe). Severity low -> medium. Change 8."
  - id: R1-4
    headline: "Two kept lines of the fork section conflict with the new rules, and the plan names neither: CLAUDE.md:50 fails the gh-line check and CLAUDE.md:70 demands `--repo` on every invocation"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:113; CLAUDE.md:50; CLAUDE.md:70"
    classification: drift
    severity: medium
    evidence: "Plan :113 'Keep the `/sc:pr-submit --monitor 3` instruction, the fallback `gh pr create --repo IronbellyOrg/IronClaude ...` block, pre-PR check 2 and the Rationale paragraph, editing them only where they contradict the rules above.' Plan :117 'Every line in the section that runs a `gh` command names `IronbellyOrg/IronClaude` (by `--repo`, positionally, or in an `api` path) or states a prohibition'. CLAUDE.md:50 'It opens the PR with `gh pr create --repo <repo>`, where `<repo>` comes from the `origin` remote'. CLAUDE.md:70 'only this CLAUDE.md rule + explicit `--repo` on every invocation does.'"
    rationale: "CLAUDE.md:50 names a placeholder, so it fails plan :117 unless the executor edits a sentence plan :113 says to keep. CLAUDE.md:70 in the kept Rationale says `--repo` on every invocation, contradicting the positional form for `gh repo view`; plan :118 is a judgment-only check."
    recommendation: "In Task 4 name CLAUDE.md:50 and say how it is rewritten: the repo is resolved from origin and must be IronbellyOrg/IronClaude, and /sc:pr-submit halts on a wrong-owner URL. Name CLAUDE.md:70 and change it to 'the repo named explicitly on every gh call'."
    provenance: "Base V1 R1-4 (CLAUDE.md:70 half kept; CLAUDE.md:64 half dropped per calibration, plan :108 already rewrites check 1); V3 R3-F4 first half (CLAUDE.md:50 vs plan :117/:113). Scripts half of R3-F4 not merged (X-001). Debate C-004 (merge, 95%). Severity low -> medium. Change 6."
  - id: R2-F1
    headline: "Task 8's conditional zero-skip rerun has no required artifact, so D-008's 'no SKIPPED line' rerun is unverifiable post-hoc and no mechanism for the full-depth non-root checkout is given"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:176"
    classification: drift
    severity: medium
    evidence: "plan:176 'The internal-checkout run passes with no SKIPPED line, or every skip reason is recorded in `./artifacts/t8-internal-checkouts.txt` and the run is repeated in a full-depth (`git rev-parse --is-shallow-repository` prints `false`), non-root (`id -u` is not 0) checkout with no SKIPPED line.' plan:170 saves the probes only for the first checkout. tests/troubleshoot/backtest/test_git_replay_integration.py:56-57 'pytestmark = pytest.mark.skipif(_GIT_UNAVAILABLE or bool(_MISSING),'; tests/skills/test_implement_retry_revert.py:357 '@pytest.mark.skipif(os.geteuid() == 0, reason=\"root ignores directory permissions\")'."
    rationale: "An executor can assert a clean rerun with no saved evidence, so the criterion can pass while the D-008 rerun requirement fails. This checkout is already full-depth and non-root (shell section 2: is-shallow false, uid 1000), so any skip here has another cause and the rerun branch either repeats in the same checkout or in one the plan never says how to obtain (round2-v2.md). Deselection is not a concern: addopts has no `-m` (INV-011)."
    recommendation: "Task 8: save the rerun to ./artifacts/t8-internal-checkouts-rerun.txt with that checkout's `git rev-parse --is-shallow-repository` and `id -u`, and name how the full-depth checkout is obtained (a local full clone or linked worktree of this repo, never a SuperClaude-Org fetch)."
    provenance: "V2 R2-F1 (recommendation verbatim); round2-v2.md (medium holds); INV-011. Uncontested in both rounds (U-003). Change 9."
  # ---------------- low ----------------
  - id: M-4
    headline: "The two retired-location checkouts the plan names no longer exist, so the Task 1 section is empty, its check passes vacuously, and the Task 3 rule describes nothing"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:27, :44, :51, :90"
    classification: drift
    severity: low
    evidence: "Plan :27 'The two existing checkouts under the retired location, `/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates` and `/home/coder/workspaces/IronClaude/.dev/worktrees/markdownlint-issue-body-files` (`git worktree list`, 2026-11-02), are recorded only.' Plan :44 'every `git worktree list` line containing `/.dev/worktrees/`, with the note \"left in place; not moved or removed by this plan\".' Plan :51 'the second lists every `/.dev/worktrees/` line from `./artifacts/t1-worktree-list.txt`.' Plan :90 'they may stay until their branch is merged, then are removed with `git worktree remove`; no new checkout may be created there.' Orchestrator 22:40Z: `git worktree list` has no /.dev/worktrees/ line and /home/coder/workspaces/IronClaude/.dev/worktrees/* does not exist."
    rationale: "The plan was written against a worktree list that has since changed; the constraint and rule name two specific paths that are gone (INV-009)."
    recommendation: "Task 1 records the live `git worktree list`. Reword the plan :27 constraint and the plan :90 rule to 'any checkout found at the retired location', not the two named paths."
    provenance: "New. INV-009 (probe; orchestrator-confirmed 22:40Z). Change 13."
  - id: R2-F3
    headline: "No disposition for a possibly existing leaked IronClaude-eval-master worktree from past runs"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:44"
    classification: drift
    severity: low
    evidence: "plan:44 'A section \"Existing checkouts at the retired location\": every `git worktree list` line containing `/.dev/worktrees/`, with the note \"left in place; not moved or removed by this plan\".' scripts/eval_runner.py:138 'worktree_path = REPO_ROOT.parent / \"IronClaude-eval-master\"'. source.md:1 D-001 'list-argument git worktree add, never removed'. Orchestrator 22:23Z: `git worktree list` has no IronClaude-eval-master entry and neither /home/coder/workspaces/IronClaude-eval-master nor /home/coder/workspaces/worktrees/IronClaude/IronClaude-eval-master exists, so no such checkout exists today."
    rationale: "The plan does not check for a leftover checkout from past runs; no search or criterion would surface one. This is a plan-completeness note only: the premise is not present on this host."
    recommendation: "Task 1: record any `git worktree list` entry named IronClaude-eval-master; if present, remove it in Task 2 or record it as a pre-existing leftover with a reason."
    provenance: "V2 R2-F3 with the orchestrator annotation (premise not present on this host); round2-v2.md (kept as low completeness note). Change 14."
  - id: R3-F8
    headline: "The teardown grep depends on formatting and can fail when the requirement is met"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:75"
    classification: drift
    severity: low
    evidence: "plan:75 '`grep -n 'worktree\", \"remove\"' scripts/eval_runner.py` prints the teardown line'"
    rationale: "One-element-per-line formatting of the argument list defeats the grep."
    recommendation: "Prefer the behavioural `git worktree list` assertion (the plan :68 test) over a source grep. If a grep stays, use `grep -n -E '\"remove\"' scripts/eval_runner.py`."
    provenance: "V3 R3-F8. Kept low (weak per calibration). Change 12."
  - id: R1-5
    headline: "The Task 4 gh-line check greps for `gh ` with a trailing space, which also matches ordinary words"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:117"
    classification: drift
    severity: low
    evidence: "Plan :117 'the check is saved as `./artifacts/t4-gh-lines.txt` from `grep -n 'gh ' CLAUDE.md`.'"
    rationale: "`gh ` matches 'through ', 'though ', 'enough '; the whole file is searched although the criterion is about one section."
    recommendation: "Required, not optional: replace the check with the section-scoped whole-word form `awk '/^## ABSOLUTE RULE: PR Target/,/^## ABSOLUTE RULE: Never Hardcode/' CLAUDE.md | grep -n -w 'gh'` and save that output as `./artifacts/t4-gh-lines.txt`."
    provenance: "Base V1 R1-5; marked required per round2-v3.md; section-scoped awk form from V3 R3-F4. Debate C-004. Change 7."
  - id: R1-6
    headline: "The pr-submit scripts' bare `gh repo view` fallback is real but outside the plan's spec scope (partial dispute of T1 F1)"
    location: "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:35"
    classification: authorized
    severity: low
    evidence: "poll-ci-checks.sh:34-35 'REPO=\"${REPO:-$(git remote get-url origin ...)}\" / [ -n \"$REPO\" ] || REPO=\"$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)\"'. source.md:1 'Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with.'"
    rationale: "The fallback runs only after the origin lookup returns nothing; the spec scopes the tightening to CLAUDE.md and D-002 names only CLAUDE.md:64 and :66."
    recommendation: "Optional: one sentence in Task 4 saying the guarded fallbacks in sc-pr-submit-protocol scripts are not covered by the allowed-forms list and are unchanged."
    provenance: "Base V1 R1-6, unchanged. Debate X-001 (V1, 95%; V3 conceded the scripts half of R3-F4 in round2-v3.md). Kept per 'Changes NOT being made'."
  - id: R3-F6
    headline: "Task 8's residual check has no class for files created or tracked after Task 1"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:177"
    classification: drift
    severity: low
    evidence: "plan:177 'Every remaining Search A line is in a file classified \"internal temporary checkout\" or \"historical record\" in `./artifacts/worktree-hit-classification.md`'. Plan :46 'If either live total differs from the 2026-11-02 baseline in the Constraints, classify every new hit with the same three classes and note the difference at the top.'"
    rationale: "Reclassification happens only in Task 1 (plan :46), but Task 2 creates tests/unit/test_eval_runner_master_checkout.py, which will likely match a search [INFERRED], so plan :177 can fail for a file no task classified (INV-007)."
    recommendation: "Task 2 appends an inventory row for tests/unit/test_eval_runner_master_checkout.py; Task 8 re-runs `-c` on both searches and classifies any new file before the residual check."
    provenance: "V3 R3-F6 merged with INV-007; the untracked memory-note example dropped (calibration: untracked, invisible to git grep). Change 11."
  - id: R3-F5
    headline: "The 'no change' and 'no added line' checks use plain `git diff`, which shows nothing once files are staged"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:178"
    classification: drift
    severity: low
    evidence: "plan:178 '`git diff --stat` shows no change to `POST-REFLECT-TASK.md`, `docs/swarm/runbook.md`, or any internal-checkout file'; plan:119 '`git diff CLAUDE.md` shows no change to the section heading line'; plan:148 'No line added in `git diff -- src/superclaude/commands/recommend.md src/superclaude/skills/sc-recommend src/superclaude/skills/sc-post-release-protocol` contains `/home/` or `src/superclaude/`'. src/superclaude/skills/sc-implement-protocol/SKILL.md:125 'Do not `git add` to the user index for this snapshot'. Plan :29 '`.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `./artifacts/`.'"
    rationale: "Plain `git diff` compares the working tree to the index, so staged changes do not show. The executor snapshots in a temporary index (SKILL.md:111, :125) and the plan stages only `.dev/tasks/` (plan :29, :160, :179), so these checks are vacuous only if someone stages source files by hand. Low hardening."
    recommendation: "Use `git diff HEAD` / `git diff HEAD --stat` at plan lines 119, 148 and 178."
    provenance: "V3 R3-F5; severity medium -> low per round2-v3.md (sc-implement-protocol SKILL.md:111, :125, orchestrator-verified). Debate U-006. Change 10."
deviations_resolution:
  - {deviation: D-001, resolved: "yes, with required fix", plan_location: "Task 2, Task 1, Task 8, Constraints Search B", note: "Resolved at plan level; Task 2 needs R1-1, R1-2, M-1, M-2, M-3 before it can be executed as written"}
  - {deviation: D-002, resolved: yes, plan_location: "Task 4", note: "R1-4 (now incl. CLAUDE.md:50), R1-5 remain"}
  - {deviation: D-003, resolved: yes, plan_location: "Constraints, Task 1", note: "Search A 108/17, Search B 9/7 confirmed"}
  - {deviation: D-004, resolved: yes, plan_location: "Constraints, Task 4", note: "line-64 parenthetical in R1-4"}
  - {deviation: D-005, resolved: yes, plan_location: "Task 4", note: "narrowed; #419 kept with diff check"}
  - {deviation: D-006, resolved: yes, plan_location: "Task 1", note: "Historical record first; Blocked noted"}
  - {deviation: D-007, resolved: yes, plan_location: "Task 1, Task 5", note: "row label correct"}
  - {deviation: D-008, resolved: yes, plan_location: "Task 8", note: "-rs, zero skips or recorded reason + rerun; R2-F1: the rerun has no required artifact"}
  - {deviation: D-009, resolved: yes, plan_location: "Task 4", note: "literal reading + authorized Orca bullet"}
  - {deviation: D-010, resolved: yes, plan_location: "Constraints", note: "flags added"}
  - {deviation: D-011, resolved: yes, plan_location: "Task 7", note: "contract test in pytest command"}
  - {deviation: D-012, resolved: yes, plan_location: "Task 3, Task 6", note: "optional read-only, removed after scan"}
  - {deviation: D-013, resolved: yes, plan_location: "Task 3, Task 1, Constraints", note: "stay until merged; not moved; M-4: the two named checkouts no longer exist"}
  - {deviation: D-014, resolved: yes, plan_location: "Task 1", note: "recorded out of scope; Task 8 checks unchanged"}
t1_findings_disputed:
  - {t1_id: F1, reason: "Real and guarded, but the spec scopes the tightening to CLAUDE.md and D-002 names only :64/:66; out-of-scope low (R1-6), not drift."}
  - {t1_id: F3, reason: "source.md:1 tells the plan to decide CLAUDE.md:251 explicitly; authorized, not necessary."}
  - {t1_id: S1, reason: "Git commands work, but Task 2 is not executable as written: the cited loader crashes on import (R1-1, confirmed by shell section 5), the failure path is unspecified (R1-2), and the main() wiring is untested (M-1)."}
  - {t1_id: S3, reason: "Understated, narrowed to CLAUDE.md:50: it fails the plan:117 criterion while plan:113 keeps it; medium (R1-4). The pr-submit scripts half is out of scope (R1-6)."}
inferred_claims:
  - "[INFERRED, now CONFIRMED by orchestrator] R1-1 import crash without sys.modules registration."
  - "[INFERRED, now CONFIRMED by orchestrator] R1-2 git worktree remove on an unregistered path exits non-zero and leaves the directory."
  - "[INFERRED] R1-5 the pattern `gh ` matches words such as 'through '."
  - "[INFERRED] git worktree add --detach into an existing empty directory behaves as Task 2 assumes (orchestrator separately confirmed it does; artifacts/t1-shell-evidence.txt section 1)."
  - "[INFERRED, reproduced independently by Variant 2] Search A 108 lines / 17 files and Search B 9 lines / 7 files, including the tuple-form hit at tests/cli/reflect/test_isolate_reviewers_cli.py:147."
  - "[INFERRED, CONFIRMED by live rerun 22:36Z, INV-008] The Search A 108/17 and Search B 9/7 baselines in the plan's Constraints are still valid."
```
