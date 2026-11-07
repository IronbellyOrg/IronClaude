reviewer: 3
model_class: opus
persona: refactorer
agent_type: reflect-reviewer
units_audited: 24
adherent: 14
counts: {authorized: 0, necessary: 0, drift: 9, regression: 1}
deviations:
  - n: 1
    class: Regression
    severity: HIGH
    location: "plan:30-32, 86, 99, 130"
    finding: "T1 F-1 confirmed. Task 1 creates the script, row only in Task 4; Task 5 creates the template, row only in Task 7; existing inventory test red in between. Task 1 acceptance never runs test_issue_protocol.py. Task 5 depends only on Task 1, so it may run before Task 4, then Task 4's own acceptance fails."
    evidence: ["tests/skills/test_issue_protocol.py:131-141", "plan:97 (Task 5 depends on Task 1 only)"]
  - n: 2
    class: Drift
    severity: MEDIUM
    location: "plan:66-76, 124, 153"
    finding: "Missing dependency edge: no task depends on Task 3 (command flags and STOP codes), yet Task 7 must update Will/Will Not 'to match the command file' and add E-CLAIM-ONLY-FLAG and E-SUBMIT-NEEDS-FULL, and Task 9 documents the same flags. Task 7 (depends on 4, 5, 6) and Task 9 (depends on 7) can run before Task 3."
    evidence: ["plan:124", "plan:130", "plan:153"]
  - n: 3
    class: Drift
    severity: MEDIUM
    location: "src/superclaude/skills/sc-issue-protocol/SKILL.md:3"
    finding: "Design requires updating the SKILL.md description; no task does. Confirms T1 F-3."
    evidence: ["source.md:303", "SKILL.md:3"]
  - n: 4
    class: Drift
    severity: MEDIUM
    location: "SKILL.md:87-88 vs plan:86, 130"
    finding: "Design requires SKILL.md claim steps 6 (Wave 5 additions) and 7 (Waves 7 and 8). Task 4 edits step 7 for Wave 7 only; Task 7's SKILL.md list omits step 6 and the Wave 8 part of step 7. SKILL.md would disagree with refs/claim.md."
    evidence: ["source.md:303", "plan:130"]
  - n: 5
    class: Drift
    severity: MEDIUM
    location: "plan:41-43, 119"
    finding: "ARG-1 and LA-7 are never named. Task 1 tests bad arguments while only preflight exists; Tasks 2 and 6 add worktree and launch with no bad-argument case. Task 6 lists LA-1 to LA-6; the 'missing or failing record gives W-LAUNCH-FAILED' path (plan:116) has no test id."
    evidence: ["source.md:340-341", "plan:119"]
  - n: 6
    class: Drift
    severity: LOW
    location: "plan:86, 130"
    finding: "ST-6 requires Wave 8 after Wave 7 and 'created or reused only'; Task 4 adds ST-6 before Wave 8 exists and Task 7 never extends it. ST-5 has the same gap for the template row."
    evidence: ["source.md:351-352"]
  - n: 7
    class: Drift
    severity: LOW
    location: "plan:116"
    finding: "Design step 5 hand_command note ('an agent started by hand is not governed by the hook; re-running the claim is preferred'), timeout 'check Orca' detail, and step 6 'the pending record stays' are absent from Task 6; LA-3 does not assert them."
    evidence: ["source.md:211-212"]
  - n: 8
    class: Drift
    severity: LOW
    location: "plan:139-149"
    finding: "Design section 16 puts design-doc B2 and B16 in Phase 1; the plan moves every design-doc edit to Task 8 (Phase 3) without stating why. Both phases ship in one PR."
    evidence: ["source.md:405"]
  - n: 9
    class: Drift
    severity: LOW
    location: "plan:162"
    finding: "make lint and the ruff format check run only in the last task; Tasks 1, 2, 5, 6 write substantial Python without a lint gate."
    evidence: ["plan:41-43, 62-64, 106-108, 119-120"]
  - n: 10
    class: Drift
    severity: LOW
    location: "plan:45-64"
    finding: "T1 F-5 confirmed: Task 2 is too large for one review. Split after design 8.3 step 4: copy, post-condition and record into a second task."
    evidence: ["source.md:189-197"]
correctness_gaps_advisory:
  - "ST-4 would fail on existing text: refs/claim.md:49, refs/tiers.md:25 (--model) and scripts/clickup_claim.py:247-248 contain banned prefixes; test must be limited to orca command lines with whole-token matching (--pr is a prefix of --prompt); neither plan nor spec says so."
  - "Wave 7 output lines need data the script never returns: untracked-do-not-stage line and make sync-dev hint ('the plan needs an unsynced primitive' undefined); FR-5 forbids the skill running git ls-files."
  - "Fork-safety scan does not cover the launch prompt: the submit block's 'check that no PR is already open' implies a gh pr call; neither plan nor spec requires --repo there; _FORK_FILES covers only SKILL.md, refs and agents."
notes:
  - "pytest -k matches the module name, so -k 'FO or worktree' selects every test in that file (not run, from pytest docs)."
  - "tests/commands/test_issue_command.py:99-103 fails if the literal --repo appears anywhere in commands/issue.md; Task 3 must avoid quoting 'orca_worktree.py worktree --repo <R>' there. (orchestrator re-Read: lines 99-103 confirm)"
  - "Task 6's dependency on Task 5 is not needed; Tasks 2 and 5 edit the same two files, so run them in sequence."
  - "SKILL.md is 155 lines; the 500-line limit is not at risk (orchestrator: wc -l = 155)."
calibration:
  calibrator_model_class: sonnet
  calibrator_diversity: degraded     # sonnet used for the opus card; the other two cards were calibrated by opus (a class in the reviewer set)
  scores: {citation_grounding: 0.90, coverage_completeness: 0.82, deviation_classification_clarity: 0.75, risk_surface_coverage: 0.85, recommendation_actionability: 0.70}
  C: 0.80
  citations_wrong: []
  note: "Finding 1 labelled Regression is a stretch for a transient red test inside a plan; finding 5 overstates (Task 1 has a bad-subcommand exit-2 case, Task 5 has --submit with worktree); the claim that _FORK_FILES covers only SKILL.md, refs and agents was not found by the calibrator (orchestrator saw it at tests/skills/test_issue_protocol.py near line 288)."
  citations_spot_checked: 17
