# Refactoring Plan: Merge into Base (Variant 2)

## Overview
- Base: Variant 2 (haiku:qa), file `variant-2-original.md` (reviewer-2; calibrated C = 0.92)
- Incorporating strengths from: Variant 1 (sonnet:analyzer, `variant-1-original.md`; calibrated C = 0.90), plus fault-finder merge actions from invariant-probe.md (Round 2.5)
- Planned changes: 13 (Change 13 is listed after the anchor-omission table)
- Risk level: Medium overall (wording edits inside existing entries; no keys added or removed; one verifier rewritten for INV-006)
- Context: debate status BLOCKED_BY_INVARIANTS (INV-006 HIGH UNADDRESSED). This is a force-selected merge. Change 1 carries the INV-006 correction, but the invariant stays listed as unaddressed in the return contract because the debate did not adjudicate it.
- Output target: `<skill output dir>/merged-card.yaml` = `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/adversarial/merged-card.yaml`

## Global constraints for the merged card
- G-1 Shape: valid YAML with EXACTLY the base top-level keys in base order: `reviewer`, `persona`, `findings`, `grounding_gaps`, `agreements_with_t1`, `disagreements_with_t1`, `risks`, `recommendations`, `verdict`, `self_reported_confidence`. Each grounding_gaps row keeps exactly `hunk_ref`, `evidence_missing`, `why_not_classifiable`, `next_evidence_needed`, `owner`, `decision_needed_by_user`. Each recommendation keeps exactly `file`, `change`, `verifier`, `priority`. `verdict` keeps exactly `tasklist_completion_pct`, `regression_present`, `status_recommendation`. Do NOT add keys (e.g. no `needs_human_decision` or `deviation_count_by_class` key). Those facts go into list text and comments (see Changes 9 and 11).
- G-2 Provenance: YAML `#` comments only. Header block at top:
  `# Provenance: produced by Skill sc:sc-adversarial-protocol (Mode A), merge executed by sc:merge-executor`
  `# Base: Variant 2 (haiku:qa, reviewer-2) — force-selected under BLOCKED_BY_INVARIANTS (INV-006)`
  `# Merge date: <ISO-8601>`
  `# Bare paths resolve under the frozen snapshot S=<.../reviewer-snapshot/root>; task-diff-map.yaml/git-inventory.txt under S/__run_evidence__/artifacts/; deviation-taxonomy.md under <plugin>/skills/sc-reflect-protocol/refs/.`
  Every grounding gap, agreement, disagreement, risk, recommendation and verdict field gets an inline or preceding requirement-level tag, in this form: `# Source: <Base (original) | Base (original, modified) — Change #N | Variant 1 (sonnet:analyzer) V1:<lines> — Change #N>; Anchor: <id/anchor>; Disposition: <preserved-exact | modified | merged-from-multiple>[; Decision basis: <diff point / INV id>]`.
- G-3 Concrete-over-generic: keep every file:line citation, requirement ID (R-001..R-003), task ID (T-101..T-103), hunk ID (H1) and number from the base verbatim unless a change below says otherwise.
- G-4 Reviewer identity: keep `reviewer: 2` and `persona: qa` (base identity; the header comment states it is merged from reviewers 1 and 2). Keep `self_reported_confidence: 0.8` (base) with a comment that it is self-reported by the base reviewer and is NOT the calibrated confidence (calibrated: V1 0.90, V2 0.92).
- G-5 Do not edit any variant or any file under the snapshot or audit root. Write only merged-card.yaml and merge-log.md.

## Planned Changes

### Change 1: Replace the pytest verifier with the full exit-code mapping (from Variant 1, corrected per INV-006)
- **Source**: Variant 1, recommendations[1].verifier (V1:91); deviation-taxonomy.md:105-113; invariant-probe.md INV-006, INV-014
- **Target**: Base recommendations[1] (V2:47-50), the `tests/test_greeting.py` entry (replace `change` and `verifier`; keep `file` and `priority: high`)
- **Rationale**: Both R2 advocates endorsed grafting V1:91 in place of V2:49 (transcript R2; V2 advocate "Verifier point: Concede"). The fault-finder showed (INV-006, HIGH) that V1:91 alone omits taxonomy rows :109/:111/:112/:113 and treats any exit 1 as Regression. The orchestrator verified this against deviation-taxonomy.md:105-113 and sc-reflect-protocol SKILL.md:1487 ("Regression candidate"). INV-014: adding a package marker or config creates an unmapped hunk (Drift signal, deviation-taxonomy.md:62).
- **Integration**: replace. New `change` text (wording may be tightened; content must be kept):
  "User action (reviewers may not execute tests): from the audit root, run `python -m pytest tests -q` and plain `pytest tests -q` and record both outputs. Prefer clearing an import failure by invocation (`python -m pytest` from the audit root) over adding files. Adding src/__init__.py, conftest.py or pytest config maps to no task or spec line (completed.md:6-8; spec.md:6/9/12) and would show up as an unmapped hunk (Drift signal, deviation-taxonomy.md:62) unless the user records the decision or amends the tasklist first."
  New `verifier` text:
  "Classify each exit per deviation-taxonomy.md:105-113: 0 clears G2; 1 is a Regression only if pytest actually collected and ran the tests and an assertion failed (a tool or interpreter error such as 'No module named pytest' is a Grounding Gap, not a Regression); retry once on failure before classifying (flaky -> Grounding Gap, :112); 2/3 -> Grounding Gap (:108); 5 (no tests collected) -> Drift/coverage (:109); 124 timeout -> Grounding Gap (:111); any other exit -> Grounding Gap (:113). If the two invocations disagree, G2 stays open. A clean run clears G2 only; it closes neither G1 nor G3. Do not treat execution.log:5 as a run."
- **Risk**: Medium (rewrites an existing verifier)
- **Concrete anchors preserved**: commands `python -m pytest tests -q`, `pytest tests -q`; "2 passed" may remain as the expected success detail; exit codes 0/1/2/3/5/124; deviation-taxonomy.md:105-113, :108, :109, :111, :112, :113, :62; execution.log:5.

### Change 2: Add the no-Drift-signal basis to the no-deviation agreement (from Variant 1, reworded per INV-011)
- **Source**: Variant 1 comment block V1:6-9 and G1 why_not_classifiable V1:22-26; invariant-probe.md INV-011
- **Target**: Base agreements_with_t1[0] (V2:26) (modify)
- **Rationale**: Both R2 advocates proposed adding the Drift definition next to V2:26 (S-001 resolved for V2; V1 kept the reasoning edge). INV-011: :62 is one signal and :58 is the definition, so the text must not state it as the definition.
- **Integration**: append to the existing string: "With no verification run (task-diff-map.yaml:38) and unmapped_hunks: [] (task-diff-map.yaml:29), none of the Drift signals at deviation-taxonomy.md:62/:65/:67/:109 fire; Drift needs an unmapped hunk or a run-derived signal, and neither exists."
- **Risk**: Low (additive)
- **Concrete anchors preserved**: changes.patch:5-9, task-diff-map.yaml:29, deviation-taxonomy.md:89-97 (base) plus :38, :62/:65/:67/:109 (added).

### Change 3: Correct the diff-regeneration recommendation (target, scope, H1 preservation) (C-009 tie, A-002, INV-001, INV-015, INV-017a)
- **Source**: Debate consensus C-009 (neither card targets task-diff-map.yaml:3), A-002 (both advocates QUALIFY: `--scope src/`, task-diff-map.yaml:27); invariant-probe.md INV-001, INV-015, INV-017(a)
- **Target**: Base recommendations[0] (V2:43-46) (modify all three text fields; keep `priority: high`)
- **Integration**:
  - `file`: absolute audit-root diff path from task-diff-map.yaml:3, i.e. `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project/changes.patch`
  - `change`: "Regenerate the audited diff (audit root, task-diff-map.yaml:3; the frozen snapshot copy is read-only and must not be edited) as ONE patch covering both src/greeting.py and tests/test_greeting.py:1-13, with the scope widened beyond `--scope src/` (task-diff-map.yaml:27 records the test file as outside that scope). Same-scope regeneration reproduces G1. With no HEAD and every file untracked (git-inventory.txt:2-9), a tests-only intent-to-add would drop the existing H1 hunk."
  - `verifier`: "After the Wave 1B map is rebuilt: H1 still maps to T-101/T-102 and a new hunk whose body matches tests/test_greeting.py:1-13 maps to T-103 (no longer mapped_hunks: [], task-diff-map.yaml:26). G1 can then close; R-003 execution evidence still requires the Change 1 run."
- **Risk**: Medium (modifies existing)
- **Concrete anchors preserved**: tests/test_greeting.py:1-13, task-diff-map.yaml:3/:26/:27, git-inventory.txt:2-9, H1, T-101/T-102/T-103.

### Change 4: G1 scope note, owner unchanged (A-002, INV-005)
- **Source**: A-002 (both advocates, both rounds); INV-005
- **Target**: Base grounding_gaps[0] (V2:7-12) (modify `why_not_classifiable` and `next_evidence_needed`; keep `owner: user`, `decision_needed_by_user: true`, keep `evidence_missing` verbatim)
- **Integration**: append to why_not_classifiable: "The missing hunk is explained by audit scope (task-diff-map.yaml:27: test file 'outside --scope src/'), so this is an evidence-supply gap, not proof of non-delivery." Next_evidence_needed: keep the base text and prefix "A regenerated diff with the scope widened beyond src/ (see recommendations[0]) containing..." Owner stays `user` (deviation-taxonomy.md:145 allows only user/reviewer; do not emit `orchestrator`).
- **Risk**: Low

### Change 5: G2 absence evidence cites the audit-root inventory (A-001, INV-003)
- **Source**: A-001 (both advocates QUALIFY); INV-003; V1 advocate R1/R2 (git-inventory.txt:2-8 is an untracked-files=all listing)
- **Target**: Base grounding_gaps[1].evidence_missing (V2:14) (modify)
- **Integration**: append: "git-inventory.txt:2-8 (untracked listing of the whole audit root) also shows no package marker or pytest config, so the absence is not an artifact of the snapshot glob. The snapshot is not a complete mirror (proposed.md, git-inventory.txt:5, is not in it)."
- **Risk**: Low (additive)

### Change 6: G3 forces partial; `decision_needed_by_user: false` only marks it as not urgent (INV-004)
- **Source**: invariant-probe.md INV-004 (deviation-taxonomy.md:149-152, :146); C-001/X-002 consensus (G3 stays a grounding gap)
- **Target**: Base grounding_gaps[2].why_not_classifiable (V2:21) (modify; all other fields verbatim, `decision_needed_by_user: false` kept)
- **Integration**: append: "As a grounding_gaps row it still forces status partial and needs_human_decision (deviation-taxonomy.md:149-152); decision_needed_by_user: false only marks it as not urgent. The advisory correctness-gaps channel does not apply: it needs two sibling symbols (deviation-taxonomy.md:175) and src/greeting.py defines one function."
- **Risk**: Low

### Change 7: completed.md recommendation covers line 8, re-snapshot, G3 exit criterion (INV-002, INV-017c)
- **Source**: invariant-probe.md INV-002, INV-017(c); C-006 (V2 won)
- **Target**: Base recommendations[2] (V2:51-54) (modify `change` and `verifier`; keep `file: "completed.md"`, `priority: high`)
- **Integration**: change: "User action: keep completed.md:2 (status) and the completed.md:8 [x] T-103 checkbox from asserting done (set status partial and uncheck T-103) until the test hunk is in the diff and a real run is recorded. Any edit to the audit root makes snapshot S stale; take a fresh snapshot before re-audit." Verifier: "completed.md:2 says done and completed.md:8 is checked only after both artifacts exist. Note that the reflect status stays partial while any grounding gap (including G3) remains (deviation-taxonomy.md:149)."
- **Risk**: Medium

### Change 8: R-002 spec-clarification recommendation is spec-first, priority low (C-007 tie, INV-016)
- **Source**: C-007 (tie, both advocates R2); INV-016; V1 recommendations[2] priority calibration (V1:93-96)
- **Target**: Base recommendations[3] (V2:55-58) (modify `change`, `verifier`, `priority`)
- **Integration**: change: "Clarify spec.md:9 first: state whether None/non-str should raise TypeError or ValueError and whether whitespace-only names count as empty. Change src/greeting.py:2 and add assertions only after the spec states it. Do not edit src/greeting.py before then." Verifier: "spec.md:9 amended; each newly stated case then has a passing assertion." Priority: `low` (both advocates agreed the base medium priority outran spec.md:9 and the non-urgent G3 flag; the boundary stays visible in risks).
- **Risk**: Low

### Change 9: proposed.md recommendation and risk rewritten: snapshot hole kept, extra-MUST inference dropped (U-001, A-001)
- **Source**: V2 advocate R2 (concedes the content fear; fixtures/project/proposed.md:3-10 restates T-101/T-102/T-103 only, which the orchestrator verified); V1 advocate R1/R2
- **Target**: Base risks[5] (V2:41) and recommendations[4] (V2:59-62) (modify)
- **Integration**: risks[5] -> "git-inventory.txt:5 lists ?? proposed.md, which is not in the snapshot, so the snapshot is not a complete mirror of the audit root. Its audit-root copy (proposed.md:3-10) only restates T-101/T-102/T-103 and adds no MUST beyond spec.md:6/9/12." recommendations[4] -> keep `file: "proposed.md"`, `priority: low`. change: "Include proposed.md in future snapshots so snapshot-absence claims stay sound." Verifier: "proposed.md is readable inside the snapshot."
- **Risk**: Low

### Change 10: Add a needs_human_decision / zero-deviation-count agreement (INV-017d, INV-012), expressed in text, not as new keys
- **Source**: invariant-probe.md INV-017(d), INV-012; deviation-taxonomy.md:152
- **Target**: Base agreements_with_t1[5] (V2:31) (modify, append)
- **Integration**: append: "needs_human_decision is true (deviation-taxonomy.md:152). Deviation counts by class are all zero (authorized 0, necessary 0, drift 0, regression 0). G1-G3 are ordinal labels for the grounding_gaps rows."
- **Risk**: Low

### Change 11: Verdict status comment states the 3-row forcing basis (INV-008)
- **Source**: invariant-probe.md INV-008
- **Target**: Base verdict (V2:63-66) (comment only; values verbatim)
- **Integration**: inline comment on `status_recommendation: partial`: `# forced by non-empty grounding_gaps (3 rows: G1, G2, G3) per deviation-taxonomy.md:149-152; needs_human_decision: true`. Comment on `tasklist_completion_pct: 0.667`: `# 2/3 tasks diff-backed (task-diff-map.yaml:34); completed.md claims 3/3; executed coverage 0/3`. Do NOT carry V1's "(G1, G2)" comment.
- **Risk**: Low

### Change 12: Disagreement list gains the INV-006 caution on T1's verifier shape (from Variant 2 advocate R2 / INV-006)
- **Source**: V2 advocate R2 ("T1's success criterion (t1-card.md:89) is the same success-only shape"); INV-006
- **Target**: Base disagreements_with_t1 (V2:33-34) (append one entry; keep existing entry verbatim)
- **Integration**: new entry: "T1's run recommendation (t1-card.md:89) is success-only. A verification run must be classified per deviation-taxonomy.md:105-113; a bare 'exit 1 = Regression' rule would let an environment failure set regression_present (see recommendations[1])."
- **Risk**: Low (additive)

## Threshold / numeric preservation

| Source variant | Value | Location | Target disposition |
|---|---|---|---|
| V2 | 0.667 | verdict.tasklist_completion_pct | preserved-exact |
| V2 | 2/3, 0.667 | agreements_with_t1[5] | preserved-exact |
| V2 | 0/3 executed coverage | risks[2] | preserved-exact |
| V2 | "2 passed" | recommendations[1] | preserved (may stay as success detail inside the Change 1 verifier) |
| V2 | 0.8 | self_reported_confidence | preserved-exact (comment: not calibrated) |
| V2 | 13 lines (tests/test_greeting.py:1-13) | grounding_gaps[0], recommendations[0] | preserved-exact |
| V1 | exit codes 0 / 1 / 2/3 | V1:91 | merged-from-multiple (extended with 5, 124, flaky, unmapped per deviation-taxonomy.md:105-113; Decision basis INV-006) |
| V1 | 66.7 | V1:99 | dropped-with-rationale (X-001: violates `<float 0.0-1.0>`, SKILL.md:1136; V1 advocate conceded) |
| V2 | priority medium | recommendations[3] | modified -> low (C-007 tie; Change 8) |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-001 | V1 9-line `#` rationale comment block before grounding_gaps | V2 won (both advocates R2): the basis belongs in structured agreements. The Drift-signal reasoning is carried as text (Change 2), not as a free comment block. |
| S-002 | V1 folded block scalars | Tie, cosmetic. Base quoting style kept. |
| C-001 / X-002 | V1 routes G3 to advisory correctness-gaps.yaml | V2 won (V1 conceded R2): the correctness-gaps channel needs siblings (deviation-taxonomy.md:175). The G3 row is kept and clarified (Change 6). |
| C-002 | V1 "no commits, so no tracked-state signal" G1 rationale | V2 won (unanimous): untracked status is tree-wide (git-inventory.txt:2-9). |
| C-003 | V1 "weakly grounded / not a likely failure" grade on G2 | V2 won (V1 withdrew the grade R2): no likelihood grade without a run. |
| C-004 / X-003 | V1 risk #5 "I did not read git-inventory.txt, reuse-audit.yaml or execution.log" | V2 won: base citations verified against S. This V1 risk is dropped. Anchor: V1:82, evidence-gap self-disclosure. Reason: contradicts the citations and is inapplicable to the base, which read the files. Debate evidence: transcript R1 C-004 and R2 V1 concession 2. |
| C-008 | V1 "adequate for R-003 but weak as a regression guard" | V2 won (V1 conceded R2): V2:39 is the precise, checkable version. Kept. |
| X-001 | V1 `tasklist_completion_pct: 66.7` | V2 won (V1 conceded): out of contract range. |
| C-009 (V1 side) | V1 absolute frozen-snapshot path as rec #1 target | Rejected: the frozen copy is read-only. Replaced by the audit-root path (Change 3). |
| — | New verdict keys `needs_human_decision`, `deviation_count_by_class` (INV-012/INV-017 options) | Not added as keys, to preserve the reviewer-card shape (G-1). The facts are expressed in agreements_with_t1 and verdict comments (Changes 10-11). |
| — | V1 G1 owner/user statement "owner could be the orchestrator" (advocates [INFERRED]) | Rejected: not a legal owner value (deviation-taxonomy.md:145; INV-005). |

Anchor-level omissions from Variant 1 (not carried, with reason):
- V1:36 "The audit root's pyproject.toml and pytest config are not in the snapshot". Anchor type: named file. Reason: factual error; no pyproject.toml exists in audit_repo_root (Step 3 K1 re-evaluation). Debate evidence: base-selection.md position-bias log.
- V1:80 concrete example `"Hello,   !"` for whitespace input. Anchor type: worked example. Disposition: preserved by Change 13 below (V1's literal is copied exactly).

### Change 13: Carry V1's worked whitespace example into base risks[4] (concrete-over-generic)
- **Source**: Variant 1 risks[2] (V1:80)
- **Target**: Base risks[4] (V2:40) (append)
- **Integration**: append " For example, src/greeting.py:4 returns \"Hello,   !\" for a whitespace-only name (V1:80)." (copy V1's literal).
- **Risk**: Low (additive)

(Planned changes total: 13.)

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Verifier could misclassify an environment failure as a Regression (INV-006) | Revert to base V2:49 and flag INV-006 in merge-log |
| 2 | Low | Additive text only | Remove appended sentence |
| 3 | Medium | Wrong regeneration target or H1 loss | Revert to base V2:43-46 |
| 4 | Low | Scope note missing | Remove appended sentence |
| 5 | Low | Additive | Remove appended sentence |
| 6 | Low | Additive | Remove appended sentence |
| 7 | Medium | Incomplete false-completion correction | Revert to base V2:51-54 |
| 8 | Low | Priority misstatement | Revert to base V2:55-58 |
| 9 | Low | Loses the A-001 evidence | Revert to base V2:41, 59-62 |
| 10 | Low | Additive | Remove appended sentence |
| 11 | Low | Comment only | Remove comments |
| 12 | Low | Additive entry | Remove entry |
| 13 | Low | Additive | Remove appended sentence |

## Review Status
- [x] Auto-approved (default; non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-25T00:00:00Z
