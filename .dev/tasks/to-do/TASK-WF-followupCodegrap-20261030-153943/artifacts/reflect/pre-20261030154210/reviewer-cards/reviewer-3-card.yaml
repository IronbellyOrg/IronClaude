reviewer: 3
persona: refactorer
model: fable
self_confidence: 0.8
verdict: revise
t1_findings_checked:
  - id: T1-40
    status: corrected
    note: >-
      Confirmed at plan:118 ("same command as Task 1"), plan:55, plan:68, plan:110. Corrections: Task 8's gap is the
      `<id>` placeholder in `gh run watch <id>` (plan:132) whose lookup exists only at source.md:352; plan:35 ("with the
      exact command in source §4 T0") is a fifth instance; plan:111 is a prose criterion with no command. Severity holds:
      plan:26 requires every acceptance command to be a bash line.
    citation: "plan:26,35,55,68,110,111,118,132; source.md:31,225,252-258,269,319,352"
  - id: T1-41
    status: corrected
    note: >-
      Repo lines hold (install_mcp.py:804-806, 862-874; install_codegraph.py:26-43). Task 3 names "the real
      `install_codegraph.py`" at plan:69 without a path; Task 4 never names `install_mcp.py` although prove stage 5
      (source.md:147) calls `install_mcp._codegraph_entry`. Minor stands.
    citation: "plan:63,69,76,83; install_mcp.py:804-806,862-874; install_codegraph.py:26-43; source.md:143-147"
  - id: T1-42
    status: corrected
    note: >-
      Partly refuted: plan:92 names `test.yml` as the dispatch target. Missing: the path, its role as setup precedent
      (source.md:115) and dispatched-not-edited (source.md:51); plan:92 also drops `--repo "$GITHUB_REPOSITORY"` from the
      dispatch command (source.md:119). Minor stands.
    citation: "plan:92; source.md:51,115,119; .github/workflows/test.yml:8"
  - id: T1-43
    status: confirmed
    note: "plan:76 carries the live harness only as prose; the guard, home= parse, print-config capture and rm (source.md:277-284) are absent."
    citation: "plan:76,81; source.md:277-284"
new_findings:
  - id: R3-01
    severity: important
    origin: plan
    deviation_class: regression
    citation: "plan:26,53,96,121; source.md:31,245,305,336"
    claim: >-
      plan:53 and plan:96 ("... prints nothing" greps) exit 1 exactly when the criterion passes under bash -e; the spec
      writes both as `if cmd; then exit 1; fi` (source.md:245,305). plan:121 (`comm -13 ... prints nothing`) exits 0
      whether or not new failures exist; the spec wraps it in `test -z "$(...)"` (source.md:336).
    fix: "Use the spec's forms: `if git grep ...; then exit 1; fi`, `if grep -n ...; then exit 1; fi`, `test -z \"$(comm -13 ...)\"`."
  - id: R3-02
    severity: important
    origin: plan
    deviation_class: drift
    citation: "plan:76,92,95; source.md:66,110,159,202"
    claim: >-
      The `tests` stage of the §2.1 flow (source.md:66, :110, :159) is not a subcommand and Task 5's step list (plan:92)
      omits it; the static test (plan:95, source.md:202) does not check it. The spec does not name "the codegraph test
      files" (spec-inherited sub-gap). This is the gap behind the five §2.1 needs-review rows.
    fix: >-
      Task 5: a `tests` step after `bump` running `uv run pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py
      tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py`, failure =
      behaviour `stage=tests`; static check for a pytest step between bump and prove.
  - id: R3-03
    severity: minor
    origin: plan
    deviation_class: authorized
    citation: "plan:76,81,122; source.md:100,278-280,332"
    claim: >-
      plan:81 needs `live-fetch.txt` with `result=ok` but the live block's fetch has no --github-output (source.md:279);
      `result=` lines go to the --github-output file, not stdout (source.md:100). plan:81 and plan:122 grep `result=pass`
      in the .log files while the spec writes it to the .out file (source.md:280,332).
    fix: "Write each live call with `--github-output \"$PKG/artifacts/<name>\"` and grep the .out files."
  - id: R3-04
    severity: minor
    origin: plan
    deviation_class: drift
    citation: "plan:92; source.md:115,117,120"
    claim: "Task 5 omits `fetch-depth: 0`, the commit author and message format, and the step summary on every path."
    fix: "Add them to Task 5."
  - id: R3-05
    severity: minor
    origin: plan
    deviation_class: drift
    citation: "plan:109-112; source.md:321"
    claim: "Task 6 drops the spec's negative `SuperClaude-Org/SuperClaude_Framework/pull` link check."
    fix: "Add `if grep -n 'SuperClaude-Org/SuperClaude_Framework/pull' docs/user-guide/mcp-installation.md .github/workflows/README.md; then exit 1; fi`."
  - id: R3-06
    severity: minor
    origin: plan
    deviation_class: drift
    citation: "plan:48; source.md:35"
    claim: "Task 2 gives line numbers but omits the spec rule to locate each seam by literal, not by line."
    fix: "Append \"locate each by the literal, not by line (source §1 preamble)\" to Task 2."
calibration:
  calibrator: confidence-calibrator (opus, blind)
  dimensions: {citation_grounding: 0.88, coverage_completeness: 0.80, deviation_classification_clarity: 0.72, risk_surface_coverage: 0.75, recommendation_actionability: 0.88}
  C: 0.81
  spot_checks: {verified: 9, mismatched: 2}
  mismatched: ["R3-03: plan:81 says the prove output, not the .log (only plan:122 names the .log)", "T1-41: install_mcp.py:804-806 is _run_argv, relevance to the codegraph entry not shown"]
  missed_gap: "source.md:110 job matrix with max-parallel: 1 absent from plan:92 (already T1-34)"
