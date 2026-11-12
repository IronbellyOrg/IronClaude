# Calibration Report

<!-- Returned by confidence-calibrator, persisted by parent on receipt 2026-11-08T02:03Z -->

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-08T02:01:14Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Cited lines match on spot-check: IronOrca runtime-local-worktree-terminal-startup.ts:202-214, :259-269; CLAUDE.md:308, :320 (303-325 has no --agent / first-terminal / terminal close text); core/CLAUDE.md:45-53 and ccsession-tag/README.md:228-237; design D2 :370, FO-18 :333; WORKER-CONTRACT.md:62; orca_worktree.py:594-610 bare create, :951-953 agent launch --surface terminal. |
| Runtime check | 0.5 | claim_class mixed (doc_contract + runtime_behavior), evidence_class log_evidence: min(1.0, 0.5) = 0.5. No executed reproducer; V-CLOSE and V-JSON pending. |
| Symptom coverage | 1.0 | Explains empty plain terminals after bare creates, both own-use and hand-off. |
| Reproducibility fit | 0.5 | Deterministic (7 of 7 daemon rows) but no Tier 1 reproducer; installed vs checkout equality unproven. |
| Fix directness | 0.5 | Right area but broader than the evidence line: two installed copies, project CLAUDE.md, one test; depends on agents following it; --all vs --terminal <handle> unresolved (V-JSON pending). |
| Domain coherence | 0.5 | Card declares a mixed claim; fix spans docs plus a pinned-phrase test (two related domains). 1.0 here would give 0.75, still below 0.85. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.67 | 4.0 / 6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.80 | not binding |
| gated_min | 0.67 | mean is the minimum |
| verdict_cap | none | M3a scoped to claim_class runtime_behavior; card is mixed; AFFIRM 0.84 would not bind anyway |
| **calibrated** | 0.67 | no structural cap fired |
| spot_check_unverifiable | none | no remote URLs |
| structural_flags | none | C1-C8 and C3b evaluated; none fired |

## Confidence

- **Self-reported (in card)**: 0.70 (not used as input)
- **Calibrated (this report)**: 0.67
- **Formula applied**: min(mean=0.67, EG+0.30=1.30, RC+0.30=0.80) = 0.67
- **Delta**: -0.03 (Domain coherence lowered from 1.0 to 0.5)

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: § Escalation decision rule 3: confidence < 0.85. multi_domain (Domain coherence ≤ 0.5) also holds; low_confidence matches first. source_only_dynamic_claim and not_reproducible do not fire.
- **Execution restriction**: none (no_escalate false, depth standard).

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | calibrated 0.67 not below 0.50 |
| C2 | no | — | — | card rejects fixes, not enum tokens (tier1-hypothesis.md:62-64); "no code defect" backed by verified P1 and orca_worktree.py:594-610 |
| C3 | no | — | — | card text says CONTROL-PROOF unknown, but supplied tasklist M-CTRL has `CONTROL-PROOF: yes: .../runtime-local-worktree-terminal-startup.ts:265` (verified createdWithAgent clause); N10 shows issue-473-claim created by worker-start --agent claude. Judgment call (Notes). |
| C3b | no | — | — | runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes), matches execution-locus.md |
| C4 | no | — | — | M-SEED, M-REUSE, M-CTRL have true/false values and outcome mappings; V-CLOSE, V-JSON have value-if pairs |
| C5 | no | — | — | card Timestamp 02:00Z vs card_mtime 02:00:51Z |
| C6 | no | — | — | no numeric threshold in headline |
| C7 | no | — | — | environment claim cites locus SAME-ENV: yes; version gap stated as unproven |
| C8 | no | — | — | card cites behaviour-definition: row 1; row 1 Status non-empty |

## Notes

- Card has no YAML frontmatter; classes read from bold header lines.
- Spot-check: all readable citations matched. Wording slip: the insertion anchor sentence ends mid-line in both copies (core/CLAUDE.md:50, README.md:233). Not re-verified: daemon rows, transcripts, N1-N10 counts, help captures, worktree-first-surface.ts. Pinned-phrase count 12 confirmed at tests/core/test_orca_session_launch_guidance.py:17-30.
- C3 judgment: only issue-473-claim is proven (N10); issue-331-github-issue-watcher and sc-issue-claim-pipeline-flag are not. If C3 is applied strictly to the card text, Symptom coverage 0.5, calibrated 0.58, verdict still ESCALATE.
- Weakness: the card rejects fixing orca_worktree.py because M-CTRL shows no leftover tab, but orca_worktree.py:602 names worktrees `issue-{number}` and none of the control worktrees matches, so M-CTRL says nothing about the script's own bare create (:594-610). By P1 it should seed a plain tab while `agent launch` (:951-953) opens a separate one: /sc:issue --claim may have the same symptom.
- Overreach: "every time" rests on 7 of 7 daemon rows (5 hand-off, 2 own-use); only 2 own-use worktrees show a live empty tab.
- Fix risk: `orca terminal close --all` after `agent launch` kills the agent; V-CLOSE and V-JSON are the only checks and both are pending.
- All optional inputs supplied. No files modified by the calibrator.
