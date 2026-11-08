# persisted by the orchestrator from the reviewer's final message
reviewer: 1
persona: analyzer
model_class: sonnet
findings:
  - id: R1-001
    severity: minor
    category: coverage_gap
    claim: >
      T-2 is implemented and tested only in substance. The tasklist never names the token "T-2". The function
      step (Step 4.1c) states the time condition but drops the design's second conjunct, `attempts` < 3. A
      literal executor can therefore write a `backoff_elapsed` that ignores `attempts`. The T-2 and T-3
      boundary at `attempts` == 3 then rests on `fail` (T-3) alone. The cycle step that applies the backoff
      (Step 6.2) and its test (Step 6.7) cover the behaviour.
    evidence:
      - "docs/designs/issue-watcher.md:479 - now >= `updated_at` + 10 min and `attempts` < 3 | eligible | none (re-runs every check)"
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:336 - backoff_elapsed(entry, now)` (now >= `updated_at` + 10 min)"
    tag: grounded
    fix: >
      In the Step 4.1c description and the Step 4.4 boundary test, add the `attempts` < 3 conjunct. Also add
      one test row that a `failed` entry with `attempts` == 3 is never eligible, named with its T-2 token.
  - id: R1-002
    severity: minor
    category: sequencing
    claim: >
      The POST reflect runs with `--remediate` over BASE..HEAD, which is the one checkpoint commit. Any
      source or test edits that remediation makes land after that commit. Step 10.7 stages only `.dev/tasks`,
      so the edits stay unstaged and uncommitted. No item re-runs G-1 to G-11 after remediation. The Done
      status can therefore describe a tree that differs from the one the gates and the commit covered.
    evidence:
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:864 - args: \"--mode post --remediate --diff <BASE SHA>..HEAD --tasklist"
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:875 - run `git add .dev/tasks` from the repository root (staging only: no second commit, no push, no PR"
    tag: inferred
    fix: >
      Add to Step 10.7 a precondition. If remediation changed any file outside `.dev/tasks`, re-run G-1 and
      G-5, then HALT for the owner (who decides on a second commit) rather than marking Done.
  - id: R1-003
    severity: minor
    category: contradiction
    claim: >
      The withdrawn-commit branch conflicts with Step 10.6. Step 10.2 says to run Step 10.6 "over a base the
      owner names", or over a working-tree diff against HEAD when none is named. Step 10.6 requires its prompt
      to be passed verbatim, with `<BASE SHA>` read from `base-sha.txt`. That file is never written in this
      branch. The `<BASE SHA>..HEAD` form cannot express a working-tree diff. Step 10.6 has no alternative
      argument text, so an executor must either break "verbatim" or invent an argument. The branch is
      contingent, so this is not blocking.
    evidence:
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:848 - run Step 10.6 over a base the owner names instead of `plans/base-sha.txt`"
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:860 - do not paraphrase, summarize, reorder or omit any part"
    tag: grounded
    fix: >
      In Step 10.6, state the permitted substitution for the withdrawn branch. Either use the owner-named
      SHA in place of `<BASE SHA>`, or use the exact `--diff` argument text for the working-tree case. Mark
      this as the only allowed change to the verbatim prompt.
  - id: R1-004
    severity: minor
    category: wrong_citation
    claim: >
      Step 8.10 says xdist is supplied "exactly as `test.yml:29` does". CI does it with `uv pip install -e
      ".[dev]" "pytest-xdist>=3.5,<4"`. The gate instead uses `uv run --offline --with "pytest-xdist>=3.5,<4"`.
      The version pin is the same but the mechanism differs. The `--offline` flag means resolution fails if
      xdist is not in the local uv cache. The item handles that by logging a blocker, so it is a precision
      problem, not an unexecutable item.
    evidence:
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:611 - supplied ad hoc exactly as `.github/workflows/test.yml:29` does"
      - ".github/workflows/test.yml:29 - uv pip install -e \".[dev]\" \"pytest-xdist>=3.5,<4\""
    tag: grounded
    fix: >
      Reword to "same version pin as test.yml:29, supplied through `uv run --with`". Add a Phase 1 preflight
      that proves xdist resolves offline, like the `ruff@0.15.20 --version` check at tasklist line 170.
  - id: R1-005
    severity: minor
    category: gate_weakness
    claim: >
      Gate G-10 uses `git diff --exit-code pyproject.toml Makefile`. That compares the working tree with the
      index only, so a change that was already staged passes it. In Step 9.15 the staged-path listing is
      checked only for `.claude/`. A staged `pyproject.toml` change would therefore not be caught until the
      P10 allowlist, which is a late HALT. The P10 allowlist does catch it, so there is no safety hole.
    evidence:
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:723 - `git diff --exit-code pyproject.toml Makefile; echo \"EXIT=$?\"`"
      - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:723 - the third lists no path under `.claude/`"
    tag: inferred
    fix: >
      Use `git diff --exit-code HEAD -- pyproject.toml Makefile .github/` in Step 9.15, or also require that the
      `--cached --name-only` listing names none of those paths.
coverage_judgements:
  - {requirement: T-1, judgement: covered, task_items: ["Step 4.1c (record.fail)", "Step 4.4", "Step 6.2"], note: "Token T-1 appears at tasklist lines 111, 336 and 345."}
  - {requirement: T-2, judgement: partially_covered, task_items: ["Step 4.1c (backoff_elapsed)", "Step 4.4 (boundary test)", "Steps 6.2 and 6.7 (DF-43)"], note: "Function, boundary test and cycle use are present. The literal token and the attempts<3 conjunct are missing. See R1-001."}
  - {requirement: T-3, judgement: covered, task_items: ["Step 4.1c (inside fail)", "Step 4.4"], note: "Token covered through the T-1..T-13 ranges at tasklist lines 336 and 345."}
  - {requirement: T-4, judgement: covered, task_items: ["Step 4.1c (mark_pending)", "Step 4.4"], note: "Judged from the item text of 4.1c, not from line-by-line comparison with the design."}
  - {requirement: T-5, judgement: covered, task_items: ["Step 4.1c (mark_launched)", "Step 4.4"], note: "Same basis as T-4."}
  - {requirement: T-6, judgement: covered, task_items: ["Step 4.1c (mark_unknown)", "Step 4.4"], note: "Same basis as T-4."}
  - {requirement: T-7, judgement: covered, task_items: ["Step 4.1c (mark_spawn_error)", "Step 4.4"], note: "Same basis as T-4."}
  - {requirement: T-8, judgement: covered, task_items: ["Step 4.1c (sweep)", "Step 4.4", "Step 8.4 (C3, C4)"], note: "The crash reruns exercise the sweep to abandoned pending_orphan."}
  - {requirement: T-9, judgement: covered, task_items: ["Step 4.1c (mark_claimed)", "Step 4.4"], note: "Same basis as T-4."}
  - {requirement: T-10, judgement: covered, task_items: ["Step 4.1c (reset_entry)", "Step 4.4", "Step 7 (reset)"], note: "Same basis as T-4."}
  - {requirement: T-11, judgement: covered, task_items: ["Step 4.1c", "Step 4.4"], note: "Same basis as T-4."}
  - {requirement: T-12, judgement: covered, task_items: ["Step 4.1c", "Step 4.4"], note: "Same basis as T-4."}
  - {requirement: T-13, judgement: covered, task_items: ["Step 4.1c", "Step 4.4"], note: "Token present at tasklist lines 111, 336 and 345."}
  - {requirement: INF-006 (enabled false, no cron until FU-1), judgement: covered, task_items: ["Step 9.2 section 8", "Step 9.1 section 0", "Key Constraints"], note: "The runbook says enabled stays false until FU-1 and that the cron entry is follow-up FU-2."}
  - {requirement: INF-008 (D1 option A, D2 claim-only, D3 integer-only), judgement: covered, task_items: ["Task Overview", "Step 8.3 (prompt regex property test)"], note: "D3 is enforced by a test. D1 and D2 are recorded as context and enforced by the package scope."}
  - {requirement: INF-009 (poller never assigns, comments or moves Project items), judgement: covered, task_items: ["Step 8.3 (REST calls use --method GET, no mutation constant, no POST)", "Key Constraints"], note: "NG-2 is guarded by an argv scan."}
  - {requirement: INF-016 (non-goals NG-1..NG-5), judgement: partially_covered, task_items: ["Step 8.3 (NG-2 only)", "Key Constraints"], note: "Only NG-2 has an explicit guard. The other non-goals are covered by the absence of features."}
  - {requirement: INF-022 (NFR-014 dependency rules, contracts.__all__ rebinding), judgement: covered, task_items: ["Step 8.8", "Gate G-4 (make lint includes lint-architecture)", "tasklist lines 194, 230, 282"], note: "The architecture lint covers the rebinding rule. The AST test covers the import table."}
  - {requirement: INF-037 (project_id regex ^PVT_), judgement: covered, task_items: ["tasklist line 245"], note: "The regex appears in the tasklist. I did not read the item's test."}
  - {requirement: INF-042 (unknown config keys rejected, exit 2), judgement: covered, task_items: ["Step 9.1 section 2", "Phase 7 config and check-config items"], note: "The runbook states it. The test coverage is assumed from the Phase 7 items and is not line-verified."}
  - {requirement: INF-044 (exit 2 reason set), judgement: covered, task_items: ["Phase 7 exit mapping (DF-41, reason table drives exits)", "Step 9.2 section 10"], note: "Mapping is table-driven, so the set is covered by the table pin test."}
  - {requirement: INF-051 (exit precedence 2, 6, 7, 5, 3, 4; 75 only alone), judgement: covered, task_items: ["Step 9.2 section 10", "Phase 7 exit tests"], note: "The runbook states the precedence. I did not re-read the exit-code test."}
  - {requirement: INF-055 (github.py builds argv from constants, classifies replies), judgement: covered, task_items: ["Phase 3 github items", "Step 8.3 argv scan"], note: "The Phase 3 items were not re-read in this session. The coverage claim is based on the summary of earlier reading."}
  - {requirement: INF-089 (project id compared in Python, never in argv), judgement: covered, task_items: ["Step 8.3 argv scan", "Phase 3 and Phase 6 predicate items"], note: "Argv allowed-forms scan forbids per-project argv forms. Not line-verified."}
  - {requirement: INF-101 (never-keys list in audit and status), judgement: covered, task_items: ["Step 8.7 (closed audit key set, sentinel scan)"], note: "The closed key set is asserted in test_no_text."}
  - {requirement: INF-108 (11 cross-cutting test files), judgement: covered, task_items: ["Steps 8.2 to 8.8", "Phase 7 and Phase 2 items for origin_parity, marker_contract, find_orca_parity, slo_helper", "Step 10.1 (the 19-name list)"], note: "Step 10.1's list of 19 test files matches design section 11's 8 + 11 names."}
  - {requirement: INF-123 (make test as a gate), judgement: partially_covered, task_items: ["Step 9.5 (G-2 affected subset)", "Step 9.19 ('full suite: CI only')", "OQ-5 (DF-05)"], note: "Declared deviation DF-05. It is weaker than make test and says so openly. G-3 adds xdist and zero skips on the new suite."}
  - {requirement: INF-124 (make lint plus pinned ruff), judgement: covered, task_items: ["Step 9.7 (make lint)", "Step 9.8 (pinned ruff check and format --check src/ tests/)", "OQ-8 (DF-09)"], note: "The pinned format check on src/ and tests/ is at least as strict as the design's unpinned one."}
  - {requirement: INF-128 (max_launches_per_cycle 1), judgement: covered, task_items: ["Phase 6 cycle items (Step 6.2)", "Step 8.3"], note: "Not re-read in detail."}
  - {requirement: INF-129 (call cap 35, 3 reserved), judgement: covered, task_items: ["Phase 3 CallBudget items"], note: "Not re-read in detail. CallBudget was seen in the design and in earlier reading."}
  - {requirement: INF-135 (approval table skip reasons), judgement: covered, task_items: ["Phase 2 predicates items", "Phase 2 and Phase 6 tests"], note: "Not re-read in detail."}
  - {requirement: INF-139 (prompts match the D3 regex over a hostile corpus), judgement: covered, task_items: ["Step 8.3 (2,000 seeded draws, seed 331)"], note: "The regex and the seed are stated at tasklist line 590."}
  - {requirement: INF-142 (budget, day cap and consumed_log hold through reset), judgement: covered, task_items: ["Step 6.7 acceptance property", "Phase 4 reset tests"], note: "Not re-read in detail."}
  - {requirement: INF-147 (shared-input exit mapping), judgement: covered, task_items: ["Phase 7 CLI tests"], note: "Not re-read in detail."}
  - {requirement: INF-151 (sleeping stub ends with gh_timeout), judgement: covered, task_items: ["Step 8.2 (AC-19 split per DF-55)", "test_runner timeout unit test", "in-process cycle tests"], note: "Step 8.2 states the AC-19 sleeping-stub timeout is deliberately not tested in the e2e file."}
best_practice_grade: 4
self_confidence: 0.7
self_audit: >
  Findings: I found no blocking defect. Five minor findings are reported (R1-001 to R1-005).
  Coverage of my own checks:
  - Check 1: T-1..T-13 mapped. T-2 is covered in substance but thin (R1-001). T-1 and T-13 tokens appear at
    tasklist lines 111, 336 and 345. A Grep for "T-2" returned no standalone token.
  - Check 2: More than 12 concrete claims were verified against real files and held up.
    - install_user_setup.py:198-221 (_find_orca).
    - main.py:559-565.
    - swarm/atomic.py:14 and :33.
    - origin_repo.py, claim.md and claim-comment.md.
    - tests/skills/test_issue_repo_resolution.py:15-19.
    - tests/swarm/test_cli_registration.py and tests/cli/test_cli_registration.py (read in full this session).
    - Makefile lines 109, 166, 356 and the lint target.
    - .pre-commit-config.yaml:74-88 (the markdownlint hook and its exclude list).
    - tests/skills/test_model_alias_policy.py lines 23, 48 and 50.
    - Existence of tests/docs/test_retired_docs_absent.py and tests/recommend/test_cli_registration.py.
    - The design's reason count of 57 (OQ-2 says the pin test has 57 names).
    - The 29 DEVIATION ids in Step 9.18, which I counted as 29.
    - The Phase 9 and Phase 10 findings-section headings match the Task Log headings exactly.
    - The claim in Step 10.4 that no local hook is installed. This holds: only .sample hooks exist under the common .git/hooks.
  - Check 3: Gate commands are executable as written, given a populated uv cache. The risk is --offline
    resolution of xdist (R1-004). The ruff pin is preflighted at tasklist line 170.
  - Check 4: Phase 10 is internally consistent for the normal path. BASE is captured in 10.2, the commit is
    in 10.4, rev-list checks one commit, the POST reflect in 10.6 is penultimate, and Done in 10.7 is last.
    The `.dev/tasks` staging rule is honoured. The remaining issues are R1-002 and R1-003.
  - Check 5: Judgements are given for every row in the brief's Coverage slice (T-1..T-13 plus 22 INF rows).
    Several INF rows were judged from item purpose, not from a line-level read of the item and its test. The
    judgement notes say so.
  - Declared deviations I did not treat as defects: DF-01 (runner cwd keyword), DF-05 (affected-subset gate),
    DF-06 (five commands, six usage forms), DF-09 (pinned uvx ruff), DF-10 (stubs written at test time, not
    committed), DF-29 (registration), DF-55 (AC-19 split).
  Not read in this session: tasklist Phases 1-3, Gates A-D, the Final gate and M4 gate items (lines 737-837),
  the frontmatter, and research/06. Residual risk is concentrated there, which is why self_confidence is 0.7.
citations:
  - "docs/designs/issue-watcher.md:476-480"
  - "docs/designs/issue-watcher.md:90"
  - "docs/designs/issue-watcher.md:800"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:336"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:577-618"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:611"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:674-736"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:838-876"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:899-912"
  - ".dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/reviewer-briefs/reviewer-1.md:5-19"
  - ".github/workflows/test.yml:29"
  - ".pre-commit-config.yaml:74-88"
  - "Makefile:109"
  - "Makefile:166"
  - "Makefile:356"
  - "tests/skills/test_model_alias_policy.py:23"
  - "tests/skills/test_model_alias_policy.py:48-50"
  - "tests/swarm/test_cli_registration.py:127"
  - "tests/cli/test_cli_registration.py:31-49"
  - "tests/skills/test_issue_repo_resolution.py:15-19"

calibration:
  calibrated_confidence: 0.75
  calibrator_model_class: opus
  calibrator_diversity: degraded
  dimension_scores:
    citation_grounding: 0.9
    coverage_completeness: 0.6
    deviation_classification_clarity: 0.75
    risk_surface_coverage: 0.65
    recommendation_actionability: 0.85
  finding_confidence:
    R1-001: 0.8
    R1-002: 0.75
    R1-003: 0.65
    R1-004: 0.7
    R1-005: 0.85
