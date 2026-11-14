# Reviewer 1 card with blind calibration (merge input, post run)

Weight findings by the calibration: findings the calibrator marked overstated carry the calibrated class and severity; supported findings keep theirs. Calibrator class opus (diversity degraded).

## Reviewer card
```yaml
# reviewer-1 card (persona analyzer, model class sonnet). Persisted by the orchestrator from the reflect-reviewer agent's returned YAML (agentId af7f1d8ba661d8fa4; the agent hit its 50-turn limit once and was resumed to return its card); reasoning shortened, nothing dropped.
reviewer: 1
persona: analyzer
model_class: sonnet
lead_verdicts:
  DC-1: "modified: Rule 5 inert confirmed and authorized (FINAL-GATE-halt-resolution-decision.md:18-19 edited DESIGN :491 and open item 6 :997; test_classify.py:368-376 pins it). The agent-wait feed of rule 4(a) is dead on live data (probes.py:432-434): necessary deviation, 1.0a-facts.md:35 says the live name is unverified; DESIGN :491 and open item 6 declare only Rule 5 inert. Residual confirmed: SP24_LINE (report.py:42-45) names only stalled and fenced, so `working: 0` has no caveat."
  DC-2: "confirmed: a worker-list row with a missing, non-string or empty dispatchId yields only a source row (probes.py:1105-1119); the FR-010 origin guard reads only `orca worker-list <run>` and `orca task-list <run>` (classify.py:690-694) and builds its Dispatch-row set from kept rows (classify.py:733-740). No test covers it, no decision authorizes it. Rated medium, not low: when every row of a Run is invalid, `rows` is empty, so guard cases 2 and 4 do not fire and a no-entry transcript can become True."
  DC-3: "confirmed: both seams use subprocess.run(capture_output=True) and test the limit after the child exits (probes.py:257-263, check :270; :308-310, check :315). SPEC section 8 (merged-requirements.md:286) prescribes Popen, chunked reads, kill past 8 MiB. DESIGN 7.1 states only the result; no D-row; research/05-test-verification.md:49 only guesses it. Drift, not regression: no acceptance criterion fails and the boundary tests pass because they fake subprocess.run. The memory bound is real for up to 10 s."
  DC-9: "modified: reserved model fields authorized by FINAL-GATE-halt-resolution-decision.md:19 and SPEC SP-15 (mtime, agent_wait_since); share_shows(wanted) by DESIGN section 6 `worker-show min(D, 50)` (:341). The third per-Run source row `orca task-list --ready <run>` (probes.py:1033, :1054) is minor drift: DESIGN section 6 counts the call, 7.4 (:597) names two rows; FIN-F12 (qa/final/consolidated-findings-cycle0.md:125) records it as open, which is not an authorization. No behaviour change."
  DC-12: "modified: wording divergence confirmed (`_git` raises `output over 8388608 bytes` at probes.py:316; `_orca` prints `8 MiB` at :271-273; the test pins the byte form at tests/sweep/test_probes_allowlist.py:1454). The reason never reaches the report: `_read_worktree` maps every GitCallFailed that is not a budget-cut timeout to `worktree not readable` (probes.py:936-937), as DESIGN 7.2 :513 prescribes. DESIGN wins: minor drift confined to exception text."
findings:
  - id: R1-F1
    title: "Rule 5 (working) is inert by owner decision; the DESIGN section 13 table was not updated and the footnote is silent on working"
    class: authorized
    severity: minor
    lead_ref: DC-1
    evidence: [src/superclaude/cli/sweep/classify.py:251-257, src/superclaude/cli/sweep/report.py:42-45, tests/sweep/test_classify.py:368-376, docs/designs/orchestrator-mode.md:491, docs/designs/orchestrator-mode.md:997, docs/designs/orchestrator-mode.md:840]
    authorization_source: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md:17-19 (owner: 'All 3 approved')"
    reasoning: "SPEC FR-006 says each class is reached at least once, so this deviates from the SPEC. DESIGN :491 and :760 were edited by the owner and DESIGN wins per its section 15.2, so the deviation is authorized. The owner decision left section 13 unchanged at 10 rows (:840). The footnote still says only 'stalled and fenced', so every live healthy worker lands in could not determine and `working: 0` carries no caveat."
    confidence: 0.8
  - id: R1-F2
    title: "agent-wait branch of rule 4(a) cannot match on live data because parse_worker_show reads no agentWait"
    class: necessary
    severity: minor
    lead_ref: DC-1
    evidence: [src/superclaude/cli/sweep/probes.py:431-444, src/superclaude/cli/sweep/classify.py:228-236, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md:35]
    authorization_source: null
    reasoning: "The live name of agentWait is not captured (1.0a-facts.md:35) and the omission is documented inline at probes.py:432-434. Rule 4(a) is still tested through hand-built models. DESIGN open item 6 lists only Rule 5 as inert, so the 4(a) consequence is not called out in DESIGN or any decision; the inline comment is the only record."
    confidence: 0.65
  - id: R1-F3
    title: "Worker-list rows with a missing or empty dispatchId are dropped from rows and invisible to the FR-010 origin guard"
    class: drift
    severity: medium
    lead_ref: DC-2
    evidence: [src/superclaude/cli/sweep/probes.py:1105-1119, src/superclaude/cli/sweep/classify.py:690-694, src/superclaude/cli/sweep/classify.py:733-740]
    authorization_source: null
    reasoning: "SPEC FR-005 says every Orca row is listed. FR-010 and NFR-008 say that when a relevant list is unscanned an unjoined transcript is never True. The per-row source row `orca worker-list <run> row <i>` is unscanned but `_origin_unknown` never reads it. If every row of a Run lacks a valid id, a no-entry transcript can reach True (with the 'origin not proved' note) and then idle or Historical. Narrow, no test, no acceptance criterion shown to fail: drift, not regression."
    confidence: 0.55
  - id: R1-F4
    title: "Subprocess seams buffer all output and test the 8 MiB limit after exit; the child is never killed on size"
    class: drift
    severity: medium
    lead_ref: DC-3
    evidence: [src/superclaude/cli/sweep/probes.py:257-263, src/superclaude/cli/sweep/probes.py:270, src/superclaude/cli/sweep/probes.py:308-310, src/superclaude/cli/sweep/probes.py:315, .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:286]
    authorization_source: null
    reasoning: "SPEC section 8 says Popen, chunked reads, kill once combined output exceeds 8 MiB. The code uses subprocess.run(capture_output=True) and checks after exit, so memory is not bounded within the 10 s timeout. The final result matches for output that ends within the timeout, which is why the boundary tests pass. DESIGN is silent and has no D-row. Arguable as regression against the SPEC text; classed drift because no acceptance criterion fails."
    confidence: 0.6
  - id: R1-F5
    title: "_git over-limit reason prints bytes instead of 8 MiB, is pinned by a test, and never reaches the report"
    class: drift
    severity: minor
    lead_ref: DC-12
    evidence: [src/superclaude/cli/sweep/probes.py:316, src/superclaude/cli/sweep/probes.py:271-273, src/superclaude/cli/sweep/probes.py:936-937, tests/sweep/test_probes_allowlist.py:1454]
    authorization_source: null
    reasoning: "SPEC section 8 says the worktree status is unread with reason `output over 8 MiB`. The seam message says `output over 8388608 bytes`, unlike `_orca`, and the test pins the divergent text. `_read_worktree` collapses it to `worktree not readable` as DESIGN 7.2 :513 says, so users never see either string."
    confidence: 0.65
  - id: R1-F6
    title: "Third per-Run source row `orca task-list --ready <run>` is not named in DESIGN 7.4"
    class: drift
    severity: minor
    lead_ref: DC-9
    evidence: [src/superclaude/cli/sweep/probes.py:1033, src/superclaude/cli/sweep/probes.py:1054, docs/designs/orchestrator-mode.md:597, docs/designs/orchestrator-mode.md:340, .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/final/consolidated-findings-cycle0.md:125]
    authorization_source: null
    reasoning: "DESIGN section 6 counts the ready call (:340) so the call is authorized. Section 7.4 names two source rows per Run. QA record FIN-F12 notes the gap and was left open, so DESIGN was not amended. classify reads only the two named rows, so behaviour is unchanged."
    confidence: 0.6
  - id: R1-F7
    title: "Reserved and extra model fields (agent_wait_since, ContractRecord.mtime, freshness_age_s, four constants) beyond DESIGN 7.2"
    class: authorized
    severity: minor
    lead_ref: DC-9
    evidence: [src/superclaude/cli/sweep/models.py:103-104, src/superclaude/cli/sweep/models.py:147-148, src/superclaude/cli/sweep/models.py:21-29]
    authorization_source: ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md:19; .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:238 (SP-15)"
    reasoning: "mtime and agent_wait_since serve the SP-15 age rule and the owner decision covers the reserved marking. The constants are plumbing for contract discovery and budget reasons. No behavioural contradiction found. Authorization for `freshness_age_s` specifically is not shown (grounding gap)."
    confidence: 0.6
  - id: R1-F8
    title: "summary.total_is_lower_bound is always True; DESIGN section 6 makes it conditional"
    class: necessary
    severity: minor
    lead_ref: NEW
    evidence: [src/superclaude/cli/sweep/classify.py:972, docs/designs/orchestrator-mode.md:346, docs/designs/orchestrator-mode.md:517, tests/sweep/test_report.py:1030-1036]
    authorization_source: null
    reasoning: "DESIGN :346 says true when any list is truncated or unscanned. DESIGN :517 says the remote hosts source is never scanned, so the Scope line is always a lower bound. The code hardcodes True with an inline 'shortcut' comment and a test pins it. The two DESIGN lines are consistent only through remote hosts. Documented inline, not in section 13; the JSON field is never False."
    confidence: 0.55
grounding_gaps:
  - what: "Whether any recorded decision or the tasklist authorizes subprocess.run in place of Popen (DC-3)"
    why_not_classifiable: "Grep of the task package for Popen and 'chunks' hit only test-guard text and research notes; tasklist matches were long lines not read."
    next_evidence: "Tasklist items for steps 1.4 and 1.4a (task file around lines 1473 and 1537) and any FIN finding naming the Popen deviation."
  - what: "Authorization of SessionRow.freshness_age_s (DC-9)"
    why_not_classifiable: "Where the field is consumed in report.py and any decision naming it were not found."
    next_evidence: "Grep freshness_age_s in src/superclaude/cli/sweep/report.py and the REPORT step 1.2 ten-dimension text."
  - what: "Sections 7.1-7.4 coverage not completed"
    why_not_classifiable: "probes.py 770-852 and 1283-1400, commands.py and report.py bodies were not read; FR-013/FR-014 per-condition tests and NFR-007's fake-timeout test were not verified."
    next_evidence: "Read those ranges and grep test_classify.py for the FR-013 and FR-014 fixtures."
inferred_claims:
  - "Python 3.10 fromisoformat rejects fractional seconds that are not 3 or 6 digits, so parse_time (probes.py:377-401) would return None for forms _TIME_RE accepts. Not tested; likely minor."
  - "last_record_ts uses the last record that has both timestamp and sessionId (probes.py:748-761); SPEC line 237 says the last complete record, else st_mtime. Not checked whether a decision allows the difference."
  - "On the first Orca call, an `output over 8 MiB` call_failed becomes unavailable via probes.py:355-357, slightly beyond the SPEC wording. Not re-Read for a citation."
  - "share_shows hands leftover shows to any Run that still needs them (probes.py:131-155); matches DESIGN :341 min(D, 50), treated as authorized."
  - "All DESIGN section 11 named tests exist by name in tests/sweep; assertion strength not read."
self_reported_confidence: 0.6
```

## Blind calibration
```yaml
# Wave 3C blind calibration of reviewer-1-card.yaml (confidence-calibrator agent a1529cbeb18711dab, model class opus)
calibrator_model_class: opus
calibrator_diversity: degraded
dimension_scores: {citation_grounding: 0.85, coverage_completeness: 0.60, deviation_classification_clarity: 0.65, risk_surface_coverage: 0.70, recommendation_actionability: 0.45}
C: 0.65
self_reported_confidence: 0.60
citations_checked: 32
citations_failed:
  - {cite: "FINAL-GATE-halt-resolution-decision.md:18-19 (lead_verdicts DC-1)", problem: "line 18 edits DESIGN :491 and :760 (the owner-edited test_classify.py row is :761), not open item 6 :997; the quote 'All 3 approved' is at :13"}
finding_verdicts:
  R1-F1: {verdict: supported, class: authorized, severity: minor, note: "the footnote gap (`working: 0` has no caveat) is not covered by the decision; it is open QA finding FIN-F15 (qa/final/consolidated-findings-cycle0.md:128); that part is drift"}
  R1-F2: {verdict: supported, class: necessary, severity: minor}
  R1-F3: {verdict: supported, class: drift, severity: medium, note: "probes.py:1115 keeps a row only for a non-empty string id; classify.py:690-694 never reads `orca worker-list <run> row <i>`; with every row dropped the guard cases are False and classify.py:759-762 returns True with 'origin not proved'. Drift defensible: no acceptance criterion shown to fail; no test"}
  R1-F4: {verdict: supported, class: drift, severity: medium}
  R1-F5: {verdict: supported, class: drift, severity: minor, note: "SPEC :286 wants `output over 8 MiB`; DESIGN :513 itself narrows the SPEC to `worktree not readable`"}
  R1-F6: {verdict: supported, class: drift, severity: minor}
  R1-F7: {verdict: overstated, calibrated_class: drift-for-constants-and-freshness_age_s / necessary-for-mtime-and-agent_wait_since, severity: minor, note: "FINAL-GATE:19 only approves marking unused fields reserved; FIN-F10 (consolidated-findings-cycle0.md:123) records the additions as a DESIGN 7.2 deviation"}
  R1-F8: {verdict: overstated, calibrated_class: aligned, note: "DESIGN :346 plus :517 (remote hosts never scanned) make 'always True' what DESIGN asks for; no defect"}
escalate: true
```
