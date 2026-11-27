reviewer: refactorer (simplicity, ordering, reuse)
model_class: opus
findings:
  - id: F-1
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 6 says BudgetExhausted and model_mismatch stop the run, and that any non-ok status gets one rerun. But ask() catches BudgetExhausted and returns refused/budget_exhausted. model_mismatch arrives as status invalid, and dry runs return refused/dry_run, so the plan's rule would rerun all of these before any stop."
    evidence: "TASK-WF-designSpec-20261126-144507.md:119; jevlib/client.py:114-117, 127-131, 170-174; jevlib/validate.py:32-33"
    consequence: "The runner must check Result.status and error for systemic codes before it reruns, so the stop logic changes."
  - id: F-2
    grade: Blocking
    blocking_reason: Missing
    claim: "The spec requires a whole-run spend estimate before the first request. Task 6 only guards each request on its own. Budget.reserve_phase already provides the whole-run check."
    evidence: "source.md:82; TASK-WF-designSpec-20261126-144507.md:119,124; jevlib/budget.py:63-70"
    consequence: "Adds a reserve_phase call before the first request, plus a test for it."
  - id: F-3
    grade: Blocking
    blocking_reason: Missing
    claim: "No step or gate.py subcommand writes the manifest at freeze time. The gate \"writes and checks\" the manifest itself, so its hash checks can compare against values it just wrote. The tests_passed event carries one evidence hash, but Gate 2 checks it against several current files. Task 8 asks for gate.py subcommands that no task defines."
    evidence: "TASK-WF-designSpec-20261126-144507.md:101,103,156; source.md:49-56"
    consequence: "Needs a defined freeze or manifest command, and a tests_passed event that records the code hashes."
  - id: F-4
    grade: Blocking
    blocking_reason: Missing
    claim: "The spec gives README the job \"how to rescore\". Task 8's README contents and its acceptance criteria leave it out."
    evidence: "source.md:34; TASK-WF-designSpec-20261126-144507.md:153,156-157"
    consequence: "Adds a README section and an acceptance criterion for it."
  - id: F-5
    grade: Blocking
    blocking_reason: Decision
    claim: "The check that git status shows changes only under the experiment folder and the package folder fails as written. The untracked .dev/brainstorms/...611, .dev/issues/611 and .dev/reflect/pre-designSpec-... folders sit outside both."
    evidence: "TASK-WF-designSpec-20261126-144507.md:159; session git status snapshot"
    consequence: "The check must be measured against a baseline or list those paths."
  - id: F-6
    grade: Medium
    blocking_reason: null
    claim: "The dependency order is inverted. Task 4's verdict needs the manifest and events formats from Task 5 (changed-file and missing-gate reasons). Task 5 depends on Task 4 only to hash a file."
    evidence: "TASK-WF-designSpec-20261126-144507.md:82,84,97"
    consequence: "Run Task 5 before Task 4, or define those formats first."
  - id: F-7
    grade: Medium
    blocking_reason: null
    claim: "The spec says the loader owns hashing. The plan still has events.py and gate.py compute SHA-256 without requiring loader.sha256_file. events.py also rebuilds an appender that jevlib.Journal already provides, with timestamp, key redaction and fsync."
    evidence: "source.md:68; TASK-WF-designSpec-20261126-144507.md:101,103; jevlib/journal.py:16-33"
    consequence: "Less duplicate code, and redaction applies to events too."
  - id: F-8
    grade: Medium
    blocking_reason: null
    claim: "Task 1 greps for \"keyword\", which cannot detect cue words. The required type names `build` and `deployment` themselves contain cues from the table."
    evidence: "TASK-WF-designSpec-20261126-144507.md:39,47; SKILL.md:154,156"
    consequence: "Grep for the real cue words, and exempt the option names."
  - id: F-9
    grade: Medium
    blocking_reason: null
    claim: "The spec lists runs/<run-id>/run-record.md, but no task creates it. The plan also moves report.md under runs/ and turns decision-record.md into a hand-written template, while the spec has the scorer produce both."
    evidence: "source.md:42,44; TASK-WF-designSpec-20261126-144507.md:84,151"
    consequence: "Settle the paths and who writes each file."
  - id: F-10
    grade: Medium
    blocking_reason: null
    claim: "The runner \"refuses to start unless --live\" yet also runs a dry run without --live. It is not stated whether a dry run needs the gates."
    evidence: "TASK-WF-designSpec-20261126-144507.md:119; source.md:82"
    consequence: "One rule for dry-run entry."
  - id: F-11
    grade: Note
    blocking_reason: null
    claim: "\"Imports ... from jevlib\" is loose wording. jevlib/__init__.py re-exports only MODEL, API_URL and KEY_ENV, so the imports must come from its submodules. KeyMissing and KeyRejected are also missing from the import list."
    evidence: "jevlib/__init__.py:5; TASK-WF-designSpec-20261126-144507.md:117"
    consequence: "Wording only."
coverage_assessment: "The whole-run spend estimate (source.md:82), README \"how to rescore\" (source.md:34), run-record.md (source.md:42) and the PR body rule \"Refs #611 and list B to E as left\" (source.md:104) have no task. INF-001, INF-002 and INF-003 are covered by the plan's Constraints (lines 19, 21) and Task 6, and INF-021 by Task 8's open items."
checked_and_found_clean:
  - "smallest passing b for c 0..6 (5,7,9,10,12,13,15) recomputed by hand"
  - "MAX_RETRIES and ATTEMPT_TIMEOUT_S read at call time (client.py:158,192)"
  - "live=False returns dry_run before the transport (client.py:127-131)"
  - "KEY_ENV is JEV_API_KEY (config.py:9)"
  - "privacy patterns github_url and path_home (manifest.py:14,19)"
  - "the loader's type-coverage checks are required by FR-002, so they are not over-built"
  - "Result.latency_ms includes local work (client.py:81,87)"
  - "keyscan --fake prints KEYSCAN OK (keyscan.py:104)"
  - "testpaths is tests (pyproject.toml:108)"
recommendations:
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
    change: "In Task 6, stop the run on refused/budget_exhausted and invalid/model_mismatch with no rerun, and add a reserve_phase whole-run check."
    verifier: "Task 6 text names those status/error pairs and reserve_phase."
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
    change: "Add a gate.py freeze subcommand, record code hashes in tests_passed, and run Task 5 before Task 4."
    verifier: "Task 5 names its subcommands, and Task 4 depends on Task 5."
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
    change: "Add README rescore instructions and run-record.md, and make the git-status check relative to a baseline."
    verifier: "Task 8 acceptance criteria mention rescore, run-record.md and the baseline."
