reviewer: 1
model_class: sonnet
persona: analyzer
agent_type: reflect-reviewer
units_audited: 46
adherent: 37
counts: {authorized: 0, necessary: 0, drift: 7, regression: 2}
deviations:
  - n: 1
    class: Regression
    severity: HIGH
    location: "plan:30, plan:95 (creating tasks); plan:86, plan:130 (late table rows)"
    finding: "Existing two-way inventory test is red between tasks: Task 1 creates scripts/orca_worktree.py but its SKILL.md row arrives in Task 4; Task 5 creates templates/launch-prompt.md but its row arrives in Task 7. Acceptance of Tasks 1, 2, 3, 5, 6 never runs the whole file. Confirms T1 F-1."
    evidence: ["tests/skills/test_issue_protocol.py:131-141", "plan:41, 62, 75, 106, 119 (-k or single-file filters)"]
  - n: 2
    class: Regression
    severity: HIGH
    location: "plan:30-33, 49-64, 95-108, 128-135"
    finding: "The plan never mentions the write-verb audit in tests/skills/test_worker_contract.py. It scans every file under src/superclaude skills, commands and agents for git add/commit/push/merge/stash/update-ref/worktree add|remove and gh pr|api; every hit must be classified by exact stripped line text in WRITE_VERB_CLASSIFICATION; test_every_write_verb_hit_is_classified and test_classification_table_has_no_stale_entries fail on an unclassified hit or an edited classified line. Task 5's template says 'Do not run ... git commit, git push' and 'git push'; Task 2's grep expects such text in the script. No task lists test_worker_contract.py. Red from Task 5 until the first full-suite run in Task 7, and an implementer is not told the fix is a new classification entry or not to edit classified lines in claim.md and SKILL.md."
    evidence: ["tests/skills/test_worker_contract.py:1090-1101 (AUDIT_ROOTS, WRITE_VERB_RE)", "tests/skills/test_worker_contract.py:2199-2208 (the two tests)", "plan:64, plan:105-107"]
    orchestrator_verification: "AUDIT_ROOTS, WRITE_VERB_RE, _scan_write_verbs and the two tests re-Read at tests/skills/test_worker_contract.py:1090-1155, 2199-2205"
  - n: 3
    class: Drift
    severity: MEDIUM
    location: "plan:57, plan:84"
    finding: "Skill prints 'untracked, do not stage' only when no file under <wt>/.dev/issues/<N>/ is tracked, but worktree output {status, path, branch, match_key, warning, detail} has no tracked-file field; tracked files are only named in free-text detail; the script owns all worktree git calls. Confirms T1 F-2."
    evidence: ["source.md:158", "source.md:165", "source.md:177", "source.md:195"]
  - n: 4
    class: Drift
    severity: MEDIUM
    location: "plan:116, plan:119"
    finding: "launch output has one warning field but W-ENFORCEMENT-ABSENT and W-LAUNCH-NOT-CCSESSION can both apply to a launched result; precedence unspecified. A temporary HOME has no hook script so enforcement_hook is missing in LA-5 too. For already_launched the design returns before step 3, so enforcement_hook has no defined value."
    evidence: ["source.md:203", "source.md:208-209", "source.md:212", "source.md:253"]
  - n: 5
    class: Drift
    severity: MEDIUM
    location: "plan:130 (ST-4)"
    finding: "ST-4 bans the FO-18 flags in skill, refs, command and script but gives no matching rule. A substring scan fails on existing text: refs/claim.md:49 and scripts/clickup_claim.py use --issue-url/--issue-number; the new script itself must contain --agent, --prompt, --surface. Needs a whole-token rule limited to orca command lines and an exclusion for the launch call."
    evidence: ["src/superclaude/skills/sc-issue-protocol/refs/claim.md:49", "src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:247-248", "source.md:350"]
  - n: 6
    class: Drift
    severity: MEDIUM
    location: "plan:86, 130, 119, 41-43"
    finding: "Four design test pins have no owning task: ST-6 (Wave 8 half, Wave 8 only exists after Task 7), ST-5 template row, LA-7, ARG-1 (only preflight in Task 1, and a missing-required-argument check cannot be tested on preflight)."
    evidence: ["source.md:340-341", "source.md:351-352"]
  - n: 7
    class: Drift
    severity: LOW
    location: "plan:70-72, 86, 130"
    finding: "Frontmatter description of commands/issue.md and SKILL.md still say the claim then stop(s); the design names the SKILL.md description (source.md:303) but plan Tasks 4 and 7 omit it; the design omits the command's description. Confirms T1 F-3."
    evidence: ["src/superclaude/commands/issue.md:3", "src/superclaude/skills/sc-issue-protocol/SKILL.md:3", "source.md:302-303"]
  - n: 8
    class: Drift
    severity: LOW
    location: "plan:70-71"
    finding: "Other stale claim text in the command file is not in Task 3: issue.md:71 ('After a claim, open next-steps.md and run its commands in your own session'), issue.md:100 (Related Commands), and the Outputs row will list launch-prompt.md although it is not written for --pipeline none."
    evidence: ["src/superclaude/commands/issue.md:68,71,100", "source.md:236"]
  - n: 9
    class: Drift
    severity: LOW
    location: "plan:116"
    finding: "Task 6 drops two design step 5 instructions: on a timeout detail must say to check Orca before re-running; hand_command must carry the note that a hand-started agent is not governed by the hook. LA-3 has no assertion for them."
    evidence: ["source.md:211", "source.md:377"]
correctness_gaps_advisory:
  - "Pending-store directory modes: os.makedirs(mode=0o700) applies only to the leaf; intermediate state directories get default modes; LA-2 asserts only the pending directory (source.md:120, 335)."
  - "already_launched time field: schema has launched_at, prose says 'its at time'; plan:116 does not say which field carries it (source.md:159, 203, 208)."
  - "-k filter over-match: -k 'FO or worktree' matches the module name test_issue_orca_worktree.py so selects the whole file (plan:62)."
reviewer_note_on_citation: "Reviewer cited tests/skills/test_issue_protocol.py:157 for the assert; the live line is :141 (orchestrator grep). Not used."
notes: ["pytest not run", "Task order 6 after 2 and 5, 7 after 4, 5, 6 is sound", "brainstorm folder exists with all parts"]
calibration:
  calibrator_model_class: opus
  calibrator_diversity: degraded     # all three Anthropic classes are reviewers; calibrator chosen to differ from this card's reviewer class where possible
  scores: {citation_grounding: 0.88, coverage_completeness: 0.75, deviation_classification_clarity: 0.82, risk_surface_coverage: 0.85, recommendation_actionability: 0.60}
  C: 0.78
  citations_wrong: ["plan:129 for ST-4 (live: plan:130) - fixed in card", "source.md:357 under finding 6 backs nothing there - removed"]
  citations_spot_checked: 31
