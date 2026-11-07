reviewer: 2
model_class: haiku
persona: qa
agent_type: reflect-reviewer
units_audited: 60          # 56 matrix units plus 4 found in the spec body
adherent: 55
counts: {authorized: 0, necessary: 0, drift: 5, regression: 0}
deviations:
  - n: 1
    class: Drift
    severity: MEDIUM
    location: "plan:116 (Task 6)"
    finding: "Task 6 drops two required launch-failure safeguards: a timeout detail must warn an agent may already exist and require checking Orca before retrying; the marker-free hand command must warn that a hand-started agent is not governed by the hook. Acceptance criteria do not require either. Absent from the coverage slice (INF-035 captures only the model/effort restriction)."
    evidence: ["source.md:211"]
  - n: 2
    class: Drift
    severity: MEDIUM
    location: "plan:119 (Task 6)"
    finding: "Task 6 lists LA-1 to LA-6 and omits LA-7 (a failed worktree record makes no launch call). Task 7 carries the orchestration rule and ST-9 but not this test, so the negative test can be missing while every acceptance passes."
    evidence: ["source.md:340"]
  - n: 3
    class: Drift
    severity: LOW
    location: "plan:42 (Task 1)"
    finding: "The bad-argument check is in Task 1 when only preflight is registered; later tasks add three subcommands without requiring ARG-1 (bad arguments of every subcommand exit 2)."
    evidence: ["source.md:341"]
  - n: 4
    class: Drift
    severity: LOW
    location: "plan:86 (Task 4)"
    finding: "Assigned skill edits omit the SKILL.md frontmatter description (says 'then stops') and claim step 6 (Wave 5 summary would omit prompt rendering and the plan boundary). No acceptance criterion detects either."
    evidence: ["source.md:303", "src/superclaude/skills/sc-issue-protocol/SKILL.md:3", "src/superclaude/skills/sc-issue-protocol/SKILL.md:87"]
  - n: 5
    class: Drift
    severity: LOW
    location: "plan:17 (Constraints)"
    finding: "Plan lacks P1's blanket prohibition on code, warnings, options or text added only for non-Orca projects. Confirms T1 F-4."
    evidence: ["source.md:39", "plan:19-26"]
notes: ["Several apparent matrix misses (hook not built, fake external services) are covered by plan Constraints and not counted", "No tests or commands run"]
calibration:
  calibrator_model_class: opus
  calibrator_diversity: degraded
  scores: {citation_grounding: 0.95, coverage_completeness: 0.85, deviation_classification_clarity: 0.85, risk_surface_coverage: 0.75, recommendation_actionability: 0.45}
  C: 0.77
  citations_wrong: []
  note: "Finding 3 slightly overstated: Task 5 (PR-3) does test one bad-argument exit (--submit with worktree). Low actionability score reflects that the card format had no recommendation field."
  citations_spot_checked: 11
