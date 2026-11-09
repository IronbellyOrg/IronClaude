reviewer: reviewer-1
persona: analyzer
model_class: sonnet
mode: pre
findings:
  - id: F1
    class: Regression
    severity: MEDIUM
    title: Severity-rule green check cannot see untracked new files, so the acceptance criteria pass vacuously
    citation: [plan:89, plan:104, plan:25, tests/skills/test_review_severity_rule.py:36-56]
    detail: _tracked_text() builds its file set from git ls-files; new spec-panel-diffgate.md and sc-diffgate/** are untracked until staged, so the banned-phrase test (line 172) and CAP_REGRESSION test (line 320) never read them.
    fix: Before running that test in Tasks 5, 6 and 10, git add -N (or git add) the new src/ and tests/ files (never .claude/); put this in the acceptance text.
  - id: F2
    class: Regression
    severity: MEDIUM
    title: Task 5 requires the subcommand table verbatim yet alters its check row; the test demands an exact substring
    citation: [plan:83, plan:86, source.md:105-110]
    fix: Keep the table verbatim and define proxy_all in a sentence directly under it; test both separately.
  - id: F3
    class: Drift
    severity: MEDIUM
    title: Source of Task 5's expected verbatim blocks unspecified (source.md moves on archive; .dev/tasks may be absent in CI)
    citation: [plan:86, plan:110]
    fix: State that the expected blocks are literals embedded in tests/skills/test_diffgate_script.py.
  - id: F4
    class: Drift
    severity: LOW
    title: Task 7 drift guard does not exempt the edited ## Usage section (nor name Review Loop / Diffgate as exceptions)
    citation: [plan:110, source.md:72, source.md:156, src/superclaude/commands/spec-panel.md:19-24]
    fix: List exceptions explicitly (Usage after token swap, Review Loop and Diffgate pinned by bullet checks, Tool Coordination minus the Read clause, Unattended absent).
  - id: F5
    class: Drift
    severity: LOW
    title: T10 template ships a brief the diffgate design says must not run (review-3 FAIL means halt, no third fix)
    citation: [plan:172, source.md:32, source.md:33, source.md:206]
    fix: Do not ship T10-R3-reviser.txt as a template; keep the original under source/ and have README state T10 is excluded from the diffgate arm.
  - id: F6
    class: Drift
    severity: LOW
    title: Reviser-line insertion point ambiguous (appended after "Finish with worker_done")
    citation: [plan:171, plan:178, source.md:189-193]
    fix: Insert the line immediately before "Finish with worker_done", as a single line, and match the diff AC; or let README hand the position to the coordinator.
  - id: F7
    class: Regression
    severity: LOW
    title: README omits that the plain-command blindness audit is exempt from the "plain /sc:spec-panel ran" validity void
    citation: [plan:173-174, source.md:209, source.md:229]
    fix: Add one README sentence exempting the separate blindness-audit session.
  - id: F8
    class: Drift
    severity: LOW
    title: Task 1 allows raising stubs yet requires one JSON object per path and CLI-level exit 2/3 tests
    citation: [plan:37, plan:41]
    fix: Stubs print {ok:false, exit:2, message:"not implemented"} and limit/read validation run in main before dispatch, or move CLI exit 2/3 cases to Task 4.
  - id: F9
    class: Authorized expansion
    severity: LOW
    title: Tasks 11/12 add the pre-run gate and plan-authored T11 blindness-audit text; base-commit 2cb683f5 classification claim unverified
    citation: [plan:19, plan:155, plan:173, source.md:201, source.md:209]
    fix: Add the pre-run gate to the Constraints list; mark T11 as coordinator-reviewable draft; phrase the rule as "differs from the loop's starting spec" unless the commit claim is checked.
  - id: F10
    class: Drift
    severity: LOW
    title: No lint step for the new Python files
    citation: [plan:143-149, CLAUDE.md (make lint)]
    fix: Add make lint on the new files to Task 10 with output saved under ./artifacts/.
correctness_gaps_advisory:
  - Task 4 hardens "about 35 script tests" into a floor (plan:77, source.md:242); parametrization can inflate it.
confirmed_ok:
  - Parent spec-panel.md anchors match (486 lines; title 10; Usage 22-23; Tool Coordination 218; Read bullet 220; Review Loop 256; Output Formats 266; Unattended 451; Boundaries 463).
  - The only src/superclaude string in the parent is the Read bullet at line 220.
  - tests/recommend/test_routing_refresh.py:33 and :648 match; CANONICAL_CAP_TEXT and AT_CAP_CLAUSES importable.
  - tests/skills/test_worker_contract.py:831-839 counts only files with the heading, so the owner ruling holds.
  - list_available_skills() at install_skill.py:115.
  - tests/skills/test_workflow_archive.py:22-28 matches the loader pattern.
  - Originals T07 and T09 each contain "any finding of any severity is FAIL" once; T05-T10 carry no --re-review/--baseline clause.
verdict: refactor
self_confidence: 0.78
calibration:
  calibrator_model_class: opus
  dimensions: {citation_grounding: 0.88, coverage_completeness: 0.80, deviation_classification_clarity: 0.70, risk_surface_coverage: 0.80, recommendation_actionability: 0.88}
  per_finding:
    F1: {verified: true, reason: "test_review_severity_rule.py:36-51 uses git ls-files; tests at 172 and 320 never read untracked new files"}
    F2: {verified: true, reason: "plan:83 verbatim + extra proxy_all vs plan:86 substring assertion against source.md:108"}
    F3: {verified: true, reason: "plan:86 gives no source for expected blocks; plan:110 says it for Task 7 only"}
    F4: {verified: true, reason: "## Usage (spec-panel.md:19-24) is edited; drift guard at plan:110 names only Unattended and Tool Coordination"}
    F5: {verified: partial, reason: "plan:172/174 already flag T10 as a coordinator decision; gap smaller than stated"}
    F6: {verified: partial, reason: "position stated (appended), but lands after the finish instruction: badly placed, not ambiguous"}
    F7: {verified: true, reason: "source.md:229 voids on plain /sc:spec-panel; README at plan:174 has no audit exemption"}
    F8: {verified: partial, reason: "conflict real; main() validating before dispatch resolves it"}
    F9: {verified: partial, reason: "base commit 2cb683f5 is named at source.md:199, so 'unverified' is overstated"}
    F10: {verified: true, reason: "plan:143-149 has no make lint"}
  calibrated_confidence: 0.81
  notes: ["F1/F7 are not Regressions (vacuous test; validity-rule gap); F10 is an omitted step"]
