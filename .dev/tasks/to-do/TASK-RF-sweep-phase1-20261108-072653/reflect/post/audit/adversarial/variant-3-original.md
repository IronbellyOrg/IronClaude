# Reviewer 3 card with blind calibration (merge input, post run)

Weight findings by the calibration: findings the calibrator marked overstated carry the calibrated class and severity; supported findings keep theirs. Calibrator class opus (diversity degraded).

## Reviewer card
```yaml
# reviewer-3 card (persona refactorer, model class opus). Persisted by the orchestrator from the reflect-reviewer agent's returned YAML (agentId a5028abf5a94cdbbd); reasoning shortened, nothing dropped.
reviewer: 3
persona: refactorer
model_class: opus
lead_verdicts:
  DC-4: "confirmed: _git sets no core.fsmonitor override and the contract and ledger readers do not check for a regular file; untracked hardening gaps classed Drift (R3-F1, R3-F2), not none."
  DC-5: "modified: both wordings are copied word for word from DESIGN (HOW-WE-WORK bullet = DESIGN:717 R2, WC-16 = DESIGN:680); the gap comes from DESIGN itself, so Authorized and minor, not Necessary."
  DC-7: "confirmed: Authorized by the scoped addendum (docs/designs/orchestrator-mode.md:1052); SKILL.md:49 already falls back to ordinary formatting when the installed copy is stale."
  DC-9: "confirmed: Drift, minor. The third source row 'orca task-list --ready <run>' (probes.py:1033) names a call DESIGN section 6 already counts (:300); DESIGN 7.4 (:597) names two rows."
findings:
  - id: R3-F1
    title: "git status in an Orca-listed worktree can run that worktree's core.fsmonitor command or start the fsmonitor daemon"
    class: drift
    severity: medium
    lead_ref: DC-4
    evidence: [src/superclaude/cli/sweep/probes.py:304-310, src/superclaude/cli/sweep/probes.py:5-7, src/superclaude/cli/sweep/probes.py:1192-1203, CHANGELOG.md:11]
    authorization_source: null
    reasoning: "The argv is 'git --no-optional-locks -C <path> status ...' with no '-c core.fsmonitor=false'; paths come from Orca 'worktree ps'. A repo-local core.fsmonitor runs a configured hook or starts a daemon creating an IPC socket in .git. That contradicts the module docstring ('every subprocess is one allowlisted git status') and the CHANGELOG claim 'changes nothing in ... git or in any worktree'. No spec line addresses it. _git also lacks stdin=DEVNULL, unlike _orca (probes.py:262)."
    confidence: 0.8
  - id: R3-F2
    title: "Contract and ledger readers accept non-regular files: a FIFO blocks the run and defeats the byte limit"
    class: drift
    severity: medium
    lead_ref: DC-4
    evidence: [src/superclaude/cli/sweep/probes.py:557-567, src/superclaude/cli/sweep/probes.py:718-720, src/superclaude/cli/sweep/probes.py:837, .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:291]
    authorization_source: null
    reasoning: "Both readers apply the limit to os.stat().st_size (0 for a FIFO) and then read with no timeout. SPEC:291 says disk reads are untimed and bounded only by byte limits. A FIFO named progress.md or return-contract.yaml in a worktree hangs the read-only command until the skill's 120 s Bash kill. The transcript path checks is_file (probes.py:837); the two readers disagree with their sibling."
    confidence: 0.8
  - id: R3-F3
    title: "Subprocess output is fully buffered and checked after exit; SPEC requires chunked reads and a kill at 8 MiB"
    class: regression
    severity: medium
    lead_ref: NEW
    evidence: [.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:286, src/superclaude/cli/sweep/probes.py:257-273, src/superclaude/cli/sweep/probes.py:308-316, src/superclaude/cli/sweep/probes.py:936-937, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2992]
    authorization_source: "task file :2992 note (13), which names the departure but cites only the tasklist item; no DESIGN or owner approval found"
    reasoning: "SPEC:286 requires Popen with chunked reads, killing the process once combined output passes 8 MiB, reason 'output over 8 MiB'. The code uses subprocess.run(capture_output=True), so memory grows until the 10 s timeout. _git uses 'output over 8388608 bytes', and line 937 then replaces any non-timeout GitCallFailed with 'worktree not readable', so neither text nor git stderr detail reaches the report. DESIGN does not override this."
    confidence: 0.65
  - id: R3-F4
    title: "A ledger over the limit is searched in the tail only; SPEC and DESIGN say head and tail, and the test name still says head and tail"
    class: regression
    severity: medium
    lead_ref: NEW
    evidence: [src/superclaude/cli/sweep/probes.py:560-565, docs/designs/orchestrator-mode.md:548, docs/designs/orchestrator-mode.md:760, .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:114, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2992]
    authorization_source: null
    reasoning: "FR-020 (SPEC:114) and the DESIGN test row (DESIGN:760, GQ-105) say a ledger over 1 MiB is read as head and tail. The code seeks to size - LEDGER_SPLIT and drops the head. The task file records this as a run-time choice, not an approval. Practical risk is low (FINAL lines come last) but the behaviour contradicts a pinned criterion and test_ledger_over_the_limit_is_read_as_head_and_tail names behaviour the code lacks."
    confidence: 0.6
  - id: R3-F5
    title: "JSON report_path and worktree paths go through the Markdown sanitizer; a path containing [ ] \\ < > | is not the real path"
    class: drift
    severity: medium
    lead_ref: NEW
    evidence: [src/superclaude/cli/sweep/report.py:694, src/superclaude/cli/sweep/report.py:590-598, src/superclaude/cli/sweep/report.py:664, docs/designs/orchestrator-mode.md:593, src/superclaude/skills/sc-sweep-protocol/SKILL.md:25]
    authorization_source: null
    reasoning: "DESIGN:593 defines report_path as the absolute path of the published report. to_json applies sanitize(), turning [ into \\[ and < into &lt;. A checkout path with those characters yields a report_path the skill (step 3) cannot Read, and a JSON consumer receives altered worktree paths. FR-016 targets untrusted text in rendered cells; the path the command publishes is not untrusted input. (Matches the task's FID-F9 note.)"
    confidence: 0.6
  - id: R3-F6
    title: "The skill says to print 'the standard error line' on exit 1 or 2, but the command can emit several lines"
    class: drift
    severity: minor
    lead_ref: NEW
    evidence: [src/superclaude/skills/sc-sweep-protocol/SKILL.md:27, src/superclaude/cli/sweep/commands.py:219-221, src/superclaude/cli/sweep/commands.py:137-143, src/superclaude/cli/sweep/commands.py:282-285]
    authorization_source: null
    reasoning: "_PublishError can carry a second line ('left temp file ...') and click's own parse errors (exit 2) print a multi-line usage block; the singular wording can lead the agent to relay part of the error. (Task logged as FIN-F59.)"
    confidence: 0.7
  - id: R3-F7
    title: "Structural debt: the XDG state folder is computed in two places, and two public wrappers have only test callers"
    class: drift
    severity: minor
    lead_ref: NEW
    evidence: [src/superclaude/cli/sweep/commands.py:253, src/superclaude/cli/sweep/probes.py:1253-1255, src/superclaude/cli/sweep/probes.py:589-591, src/superclaude/cli/sweep/probes.py:944-947]
    authorization_source: null
    reasoning: "The --output overlap check and the tab-map read each derive the state folder separately; if one changes the check would guard a different folder. read_ledger and read_worktree have no production caller, only tests, so tests exercise a slightly different surface from collect. (Task logged as FIN-F44, FIN-F48.)"
    confidence: 0.75
  - id: R3-F8
    title: "Third per-Run source row and extra model fields beyond DESIGN 7.2 and 7.4"
    class: drift
    severity: minor
    lead_ref: DC-9
    evidence: [src/superclaude/cli/sweep/probes.py:1033, src/superclaude/cli/sweep/probes.py:1051-1054, docs/designs/orchestrator-mode.md:597, docs/designs/orchestrator-mode.md:300, src/superclaude/cli/sweep/probes.py:131-133]
    authorization_source: null
    reasoning: "The call is designed (DESIGN:300) but the source row name and share_shows' optional 'wanted' parameter are not in DESIGN 7.1 or 7.4. Behaviour unchanged for existing readers. Silent and unapproved, so Drift, not Necessary. Logged by the task as minor FIN-F10..F12."
    confidence: 0.7
  - id: R3-F9
    title: "Sweep chat-summary exception in pragmatic.md and SKILL.md"
    class: authorized
    severity: minor
    lead_ref: DC-7
    evidence: [docs/designs/orchestrator-mode.md:1050-1052, src/superclaude/skills/sc-sweep-protocol/SKILL.md:43-51]
    authorization_source: docs/designs/orchestrator-mode.md:1052
    reasoning: "The owner chose option (b) through the scoped addendum; skill and style state the same five conditions and SKILL.md:49 falls back to ordinary formatting when the installed style is stale."
    confidence: 0.85
  - id: R3-F10
    title: "HOW-WE-WORK says 'on every wake'; WC-16 says 'on every coordinator wake or wait timeout'"
    class: authorized
    severity: minor
    lead_ref: DC-5
    evidence: [src/superclaude/core/HOW-WE-WORK.md:405, src/superclaude/core/WORKER-CONTRACT.md:277, docs/designs/orchestrator-mode.md:717, docs/designs/orchestrator-mode.md:680]
    authorization_source: docs/designs/orchestrator-mode.md:717
    reasoning: "Each text copies its DESIGN source word for word. The narrower bullet points to WC-16 as the rule, so it does not contradict it. The plugin mirror has the same lines."
    confidence: 0.75
grounding_gaps:
  - what: "Whether any .claude/ path other than settings.json is staged"
    why_not_classifiable: "Read-only reviewer with no git access"
    next_evidence: "git diff --cached --name-only | grep ^.claude/ (orchestrator)"
  - what: "Byte identity of src/superclaude/core/HOW-WE-WORK.md and its plugin mirror"
    why_not_classifiable: "Only the sweep lines were compared with Grep"
    next_evidence: "tests/commands/test_routing_plugin_parity.py or cmp"
  - what: "Whether 'orca worktree ps' lists worktrees of other repositories (git status would then run outside this checkout's worktrees)"
    why_not_classifiable: "DESIGN:292 authorizes each distinct canonical path from worktree ps; Orca's scope was not captured"
    next_evidence: "step 1.0a capture of worktree ps --json on a host with two repositories"
inferred_claims:
  - "A 0-byte FIFO passes the st_size checks (standard POSIX stat behaviour, not tested)."
  - "core.fsmonitor=true makes git status start the built-in fsmonitor daemon (standard git behaviour, not tested)."
checked_clean:
  - "No src/superclaude/ or SuperClaude-Org reference in sweep.md, the sc-sweep-protocol skill, WORKER-CONTRACT.md, HOW-WE-WORK.md, pragmatic.md or cli/sweep/"
  - "/sc:sweep is on the never-as-worker list (WORKER-CONTRACT.md:23) as DESIGN section 8 specifies"
  - ".gitignore:255-256 ignores .dev/sweeps/; the CHANGELOG entry matches DESIGN R8"
  - "The --output checks reject a symlinked sweeps folder and overlap with the inputs; publication uses O_EXCL and os.link and never overwrites an existing report"
  - "The --agent-wait templates in ALLOWED_ORCA are owner-authorized (DESIGN:838 D10)"
self_reported_confidence: 0.72
```

## Blind calibration
```yaml
# Wave 3C blind calibration of reviewer-3-card.yaml (confidence-calibrator agent a6e63add429148b74, model class opus)
calibrator_model_class: opus
calibrator_diversity: degraded
dimension_scores: {citation_grounding: 0.88, coverage_completeness: 0.70, deviation_classification_clarity: 0.72, risk_surface_coverage: 0.82, recommendation_actionability: 0.55}
C: 0.73
self_reported_confidence: 0.72
citations_checked: 42
citations_failed:
  - {cite: "src/superclaude/cli/sweep/probes.py:837", finding: R3-F2, issue: "line 837 is the tab-map reader's is_file check, not the transcript reader; the point that a sibling reader checks is_file still holds"}
  - {cite: "src/superclaude/cli/sweep/commands.py:219-221", finding: R3-F6, issue: "weak: decorator lines, do not show multi-line error output; the _PublishError second line carries the finding"}
finding_verdicts:
  R3-F1: {verdict: supported, class: drift, severity: medium}
  R3-F2: {verdict: supported, class: drift, severity: medium}
  R3-F3: {verdict: overstated, calibrated_class: drift, calibrated_severity: medium, note: "recorded departure from SPEC :286, directed by the tasklist item, limit still enforced after the fact"}
  R3-F4: {verdict: overstated, calibrated_class: drift, calibrated_severity: low-to-medium, note: "head not read, practical risk low per the card itself"}
  R3-F5: {verdict: supported, class: drift, severity: medium}
  R3-F6: {verdict: supported, class: drift, severity: minor}
  R3-F7: {verdict: supported, class: drift, severity: minor}
  R3-F8: {verdict: supported, class: drift, severity: minor}
  R3-F9: {verdict: supported, class: authorized, severity: minor}
  R3-F10: {verdict: supported, class: authorized, severity: minor}
blocking_findings: none
escalate: true
```
