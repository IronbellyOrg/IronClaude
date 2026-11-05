# Returned by reflect-reviewer (read-only); persisted by the orchestrator.
# Orchestrator note: R3-F1 matches the import probe in artifacts/t1-shell-evidence.txt section 5 (confirmed).
reviewer: 3
persona: refactorer
model_class: opus
findings:
  - id: R3-F1
    headline: "Task 2's cited import pattern crashes when it loads eval_runner.py, so the before and after runs fail on import instead of testing anything"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:67"
    classification: necessary
    severity: medium
    evidence: "plan:67 'It loads the script with `importlib.util.spec_from_file_location` (the pattern at tests/swarm/test_bare_review_golden_regen.py:153)'; test_bare_review_golden_regen.py:157-158 'module = importlib.util.module_from_spec(spec)' / 'spec.loader.exec_module(module)'; scripts/eval_runner.py:10 'from __future__ import annotations', :18 'from dataclasses import dataclass, field', :46-48 '@dataclass' / 'class RunResult:' / 'name: str'"
    rationale: "dataclasses reads sys.modules[cls.__module__].__dict__ for string annotations; an unregistered module raises AttributeError before any test runs."
    recommendation: "Task 2: register `sys.modules[spec.name] = module` (or monkeypatch.setitem) before exec_module; t2-fail-before.txt must fail on the missing `master_checkout`, not on `'NoneType' object has no attribute '__dict__'`."
  - id: R3-F2
    headline: "The fail-before check is vacuous, and the new wiring in main() is never tested"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:74"
    classification: drift
    severity: medium
    evidence: "plan:74 'the same tests fail against the pre-change `scripts/eval_runner.py`'; plan:68-71 (all four tests target `master_checkout()` or a source grep); plan:64 'If the checkout cannot be created, append a `RunResult` named `global-setup` with `errors=1` ... do not fail silently'"
    rationale: "Three tests fail before only because master_checkout does not exist; the global-setup path, the run_global(run_id, checkout) signature and the E2E block inside the with block are untested."
    recommendation: "Task 2: add a main() test with --mode global (run_pytest, run_e2e_script, RESULTS_DIR patched; REPO_ROOT at a no-master repo) asserting a 'global-setup' run with errors=1 and git stderr; and a master-present test asserting no 'IronClaude-eval-master' under REPO_ROOT.parent and `git worktree list` back to one entry."
  - id: R3-F3
    headline: "master_checkout's failure path is not specified: cleanup can hide git's error, leak the temp directory, or turn errors from the body into global-setup"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:62"
    classification: drift
    severity: medium
    evidence: "plan:62 'On a non-zero exit it raises an error carrying git's stderr. In `finally` it runs `git worktree remove --force <that directory>` (never `rm -rf`)'; plan:64 'wrap the whole global block ... in one `with master_checkout() as checkout:`. If the checkout cannot be created, append a `RunResult` named `global-setup`'; scripts/eval_runner.py:70 'proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)'"
    rationale: "A finally covering a failed add runs remove on an unregistered dir (exit 128, confirmed), can replace git's add stderr, and leaks the mkdtemp dir; no exception type is named, so a broad except would turn body errors (e.g. the 120 s pytest timeout) into a false global-setup result."
    recommendation: "Task 2: a dedicated MasterCheckoutError; on failed add, os.rmdir the empty dir and raise before any try/finally; try/finally around the yield only; main catches only MasterCheckoutError; pin the no-master test to git's add message and check the mkdtemp dir is gone."
  - id: R3-F4
    headline: "Task 4's gh-line check fails on the /sc:pr-submit sentence the plan says to keep, and the new 'allowed gh forms' list contradicts the mandated tool's scripts"
    location: "CLAUDE.md:50"
    classification: drift
    severity: medium
    evidence: "CLAUDE.md:50 'It opens the PR with `gh pr create --repo <repo>`, where `<repo>` comes from the `origin` remote'; plan:117 'Every line in the section that runs a `gh` command names `IronbellyOrg/IronClaude` ... or states a prohibition'; plan:113 'Keep the `/sc:pr-submit --monitor 3` instruction ... editing them only where they contradict'; src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:22 '[ -n \"$REPO\" ] || REPO=\"$(gh repo view --json nameWithOwner -q .nameWithOwner ...)\"'"
    rationale: "Line 50 names a placeholder, so it fails the criterion unless the executor edits a kept sentence; the pr-submit scripts' bare `gh repo view` fallback is a form plan:110 forbids."
    recommendation: "Task 4: say how line 50 is rewritten (repo resolved from origin and must be IronbellyOrg/IronClaude; halts on a wrong-owner URL); limit the allowed-forms list to gh commands the agent types itself, noting pr-submit resolves from origin first; evidence via `awk '/^## ABSOLUTE RULE: PR Target/,/^## ABSOLUTE RULE: Never Hardcode/' CLAUDE.md | grep -n '\\bgh '`."
  - id: R3-F5
    headline: "The 'no change' and 'no added line' checks use plain `git diff`, which shows nothing once files are staged"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:178"
    classification: drift
    severity: medium
    evidence: "plan:178 '`git diff --stat` shows no change to `POST-REFLECT-TASK.md`, `docs/swarm/runbook.md`, or any internal-checkout file'; plan:119 '`git diff CLAUDE.md` shows no change to the section heading line'; plan:148 'No line added in `git diff -- src/superclaude/commands/recommend.md ...` contains `/home/`'"
    rationale: "Plain `git diff` compares the working tree to the index; staged changes do not show, so the criteria can pass while the requirement fails."
    recommendation: "Use `git diff HEAD` / `git diff HEAD --stat` at plan lines 119, 148 and 178."
  - id: R3-F6
    headline: "Task 8's residual check has no class for files created or tracked after Task 1"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:177"
    classification: drift
    severity: low
    evidence: "plan:177 'Every remaining Search A line is in a file classified ... in `./artifacts/worktree-hit-classification.md`'; docs/memory/reflect/deviation-patterns-orca-default-worktree-paths.md:4 contains '`[\"git\", \"worktree\", \"add\", ...]`' (untracked today)"
    rationale: "The new test file from Task 2 will likely match a search; the untracked memory note matches Search B if added."
    recommendation: "Task 2 appends an inventory row for tests/unit/test_eval_runner_master_checkout.py; Task 8 re-runs `-c` on both searches and classifies any new file before the residual check."
  - id: R3-F7
    headline: "The test fixture repo setup leaves out the branch name and git identity, so the master-based tests are host-dependent"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:67"
    classification: drift
    severity: low
    evidence: "plan:67 'builds a throwaway git repo in pytest `tmp_path` with a commit on `master`'; plan:70 'a repo with no `master` branch makes `master_checkout()` raise'"
    rationale: "init.defaultBranch=main breaks the positive tests and makes the no-master test pass trivially; commits fail without user.email."
    recommendation: "Task 2: `git init -b master`, `git -c user.email=t@t -c user.name=t commit --allow-empty -m init`; no-master case via `git init -b trunk`; tests pass with GIT_CONFIG_GLOBAL=/dev/null."
  - id: R3-F8
    headline: "The teardown grep depends on formatting and can fail when the requirement is met"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:75"
    classification: drift
    severity: low
    evidence: "plan:75 '`grep -n 'worktree\", \"remove\"' scripts/eval_runner.py` prints the teardown line'"
    rationale: "One-element-per-line formatting defeats the grep."
    recommendation: "Replace with `grep -n -E '\"remove\"' scripts/eval_runner.py` plus the behavioural worktree-list test."
  - id: R3-F9
    headline: "A global-setup failure still exits 0 in --mode global"
    location: "scripts/eval_runner.py:313"
    classification: drift
    severity: low
    evidence: "scripts/eval_runner.py:313 'if any(r.failed > 0 or r.errors > 0 for r in runs if r.name.startswith(\"local\")):'; plan:64 'do not fail silently'"
    rationale: "Exit-code-only automation sees success when the master checkout cannot be created."
    recommendation: "Task 2 decides explicitly whether global-setup errors set a non-zero exit, covered by the main() test."
t1_findings_disputed:
  - {t1_id: S1, reason: "Git commands work, but Task 2 is not executable as written (R3-F1, R3-F2, R3-F3)."}
  - {t1_id: S3, reason: "Understated: CLAUDE.md:50 fails the criterion while plan:113 keeps it, and allowed-forms contradicts pr-submit's fallback; Medium (R3-F4)."}
self_confidence: 0.8
inferred_claims:
  - "[INFERRED, CONFIRMED by orchestrator probe] dataclasses import crash without sys.modules registration."
  - "[INFERRED] The executor stages source files during or after steps, making plain `git diff` checks vacuous."
  - "[INFERRED] tests/unit/test_eval_runner_master_checkout.py will mention `git worktree add` or `\"worktree\", \"add\"`."
  - "[INFERRED] `git worktree remove --force` deletes ignored content such as a .venv created by `uv run` inside the temporary checkout."
