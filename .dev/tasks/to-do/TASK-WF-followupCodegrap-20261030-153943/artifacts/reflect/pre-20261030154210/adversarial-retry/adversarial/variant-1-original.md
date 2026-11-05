reviewer: 1
persona: analyzer
model: sonnet
self_confidence: 0.78
verdict: revise
notes: "No Bash; could not re-check #329 merge state, git log, ruff or gh."
t1_findings_checked:
  - {id: T1-14, status: confirmed, citation: "source.md:19,69,118,165,202", note: "Push before/after prove is ambiguous; both orders pass the static test."}
  - {id: T1-15, status: corrected, citation: "src/superclaude/cli/__init__.py:13; src/superclaude/cli/install_mcp.py:21,23,804; source.md:44,146-147", note: "Wider: importing superclaude.cli runs __init__ which imports main (click, rich); install_mcp imports click; the prove runner _run_argv lives in install_mcp."}
  - {id: T1-16, status: confirmed, citation: "source.md:143,281-283; src/superclaude/cli/install_codegraph.py:67-68", note: "PATH entry wrong for HOME=<tmp>."}
  - {id: T1-17, status: corrected, citation: "source.md:100,101,166,197", note: "(a),(c),(d) hold; (b) inferred from the exit-1 contract, not stated."}
  - {id: T1-18, status: confirmed, citation: "source.md:101,127,197,351", note: "--tag equal to the pin undefined; T7 hardcodes v1.6.2 (see R1-08)."}
  - {id: T1-19, status: confirmed, citation: "source.md:110,133"}
  - {id: T1-20, status: confirmed, citation: "source.md:44,103; plan:76"}
  - {id: T1-21, status: confirmed, citation: "source.md:46,92,199,202"}
  - {id: T1-22, status: corrected, citation: "source.md:24,49,51,419", note: "20 is defensible (the rewritten sites); ambiguous, nit."}
  - {id: T1-23, status: confirmed, citation: "source.md:402-407"}
  - {id: T1-24, status: confirmed, citation: "source.md:164,166,168"}
  - {id: T1-25, status: confirmed, citation: "source.md:110-112,202"}
  - {id: T1-26, status: confirmed, citation: "source.md:112,115; .github/workflows/test.yml:133-144"}
  - {id: T1-27, status: confirmed, citation: "plan:35", note: "[INFERRED] ledger timing."}
  - {id: T1-28, status: confirmed, citation: "plan:35; source.md:402; src/superclaude/cli/install_codegraph.py:26,271"}
  - {id: T1-29, status: confirmed, citation: "src/superclaude/cli/install_codegraph.py:273,293; source.md:143"}
  - {id: T1-30, status: corrected, citation: "pyproject.toml:54; .github/workflows/test.yml:23,95; source.md:187", note: "ruff pinned in dev extras and on PATH in the venv; nit."}
  - {id: T1-31, status: confirmed, citation: "source.md:112,202", note: "[INFERRED]"}
  - {id: T1-32, status: confirmed, citation: "source.md:22,129,138,185"}
  - {id: T1-33, status: confirmed, citation: "tests/unit/test_cli_doctor.py:3-15,241,287; tests/cli/test_update_command.py:339"}
new_findings:
  - id: R1-01
    severity: important
    origin: spec-inherited
    deviation_class: regression
    citation: "tests/cli/test_install_codegraph.py:306,320; source.md:24,204,255,419; plan:48,55"
    claim: >-
      tests/cli/test_install_codegraph.py:306 `_bump(monkeypatch, version="1.6.3")` and :320 `vdir(box.home, "v1.6.3")` are not in the
      replace list (fact 3 grepped only 1.6.2). A bump to v1.6.3 makes test_u21 compare a dir with itself and fail, so the first patch
      bump ends as a behaviour draft. The 9.9.9 mutation check cannot reveal it.
    fix: "Derive the _bump default and vdir tag from cg.VERSION (patch+1); run the mutation check with next patch, minor and major; guard against any semver literal >= pin; name the guard test's file."
  - id: R1-02
    severity: important
    origin: spec-inherited
    deviation_class: drift
    citation: "source.md:62,101,103,133-134,199,202"
    claim: >-
      The idempotency gate has no owner: check emits no branch/PR state and route runs after the outcome. A daily rerun rebuilds and
      pushes to an existing branch (non-fast-forward, false red into the infra counter); a declined tag re-downloads and re-proves daily.
    fix: "Add a gate in check (or a gate subcommand) emitting branch_exists, declined, reprove; gate push and work on them; R-cases and a static check."
  - {id: R1-03, severity: minor, origin: plan, deviation_class: drift, citation: "plan:81,118,123; source.md:279,332,337", claim: "Task 4/7 criteria read result= lines that the commands as written do not produce (no --github-output).", fix: "Run fetch and prove with --github-output to .out files and check those."}
  - {id: R1-04, severity: minor, origin: plan, deviation_class: drift, citation: "plan:108-112; source.md:321", claim: "Task 6 drops the negative SuperClaude-Org pull-link check.", fix: "Add the source.md:321 line."}
  - {id: R1-05, severity: minor, origin: spec-inherited, deviation_class: drift, citation: "source.md:98,269; plan:68", claim: "The import allow-list omits stdlib modules the design needs (select/selectors/threading/queue for the MCP client; dataclasses, collections, contextlib ...).", fix: "AST check against sys.stdlib_module_names."}
  - {id: R1-06, severity: minor, origin: spec-inherited, deviation_class: drift, citation: "source.md:96,126", claim: "[INFERRED] gh api --paginate prints one JSON array per page; merging is unspecified.", fix: "Use --paginate --slurp or decode concatenated arrays; one two-page R-case."}
  - {id: R1-07, severity: minor, origin: spec-inherited, deviation_class: drift, citation: "source.md:66,114-115; .github/workflows/test.yml:40,95,109-112", claim: "[INFERRED] uv run in the workflow may build a second env; test.yml uses the activated venv's bare pytest.", fix: "State the workflow uses the activated venv's python and pytest."}
  - {id: R1-08, severity: minor, origin: spec-inherited, deviation_class: drift, citation: "source.md:66,105,159,165,214,351; plan:35,76,132", claim: "No file list for the tests step and no tests stage value; Tasks 4 and 8 hardcode v1.6.2 though Task 1 allows another pin.", fix: "Name the test files, add stage tests, read the pin with read_pin for Tasks 4 and 8."}
  - {id: R1-09, severity: minor, origin: spec-inherited, deviation_class: drift, citation: "source.md:110,202,199; plan:92,136", claim: "dry_run 'no push, no PR, no issue' has no static check or R-case.", fix: "Static check that every push, gh pr create, gh issue create and gh workflow run step is gated on inputs.dry_run != true."}
calibration:
  calibrator: confidence-calibrator (opus, blind)
  dimensions: {citation_grounding: 0.85, coverage_completeness: 0.75, deviation_classification_clarity: 0.80, risk_surface_coverage: 0.85, recommendation_actionability: 0.85}
  C: 0.82
  spot_checks: {verified: 10, mismatched: 1}
  mismatched: ["R1-03 overstates: check (source.md:278) and prove (:280,:332) pass --github-output; only fetch (:279) and plan Task 7 (plan:118) omit it"]
