# Calibration Report

<!-- Returned by confidence-calibrator, persisted by parent on receipt 2026-11-08T02:09Z -->

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/tier2-root-cause-analyst-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T02:06:52Z

Declared: claim_class mixed (doc_contract + runtime_behavior), evidence_class log_evidence, verdict AFFIRM. No defaults; no misdeclaration.

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Load-bearing citations match: startup.ts:210 (result discarded), :196-197 (`void provisioning`), :223-233 (no seed handle), provisioning.ts:202-211 (deferred seed); core/CLAUDE.md:45-53 (line 51 ends "to use ccsession."); ~/.claude/CLAUDE.md read in full: no "Orca session launches" section. Five secondary citations unresolved (Notes), not contradicted. |
| Runtime check | 0.5 | mixed: doc_contract x log_evidence 1.0, runtime_behavior x log_evidence 0.5 → 0.5; falsification command but no captured output. |
| Symptom coverage | 0.5 | Own-use tab explained (N7, N8). Hand-off cases explained as "stale install plus existing --agent rule", inferred; hand-off creates ran 2026-11-01 to 11-04 and the installed file's mtime is 2026-11-05T13:13:32Z (N12); the card does not show the rule existed at those dates. Ironeye tab unaccounted. |
| Reproducibility fit | 0.5 | Deterministic (7 of 7), no live reproducer. |
| Fix directness | 0.5 | Exact location, but effect depends on reinstall and agents following text; late seed can survive the close. |
| Domain coherence | 0.5 | Installed instruction text, pinned-phrase test, install pipeline, plus Orca seeding. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.58 | 3.5 / 6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 0.80 | does not bind |
| gated_min | 0.58 | mean is lowest |
| verdict_cap | none | M3a needs runtime_behavior; card is mixed |
| **calibrated** | 0.58 | no structural cap |
| spot_check_unverifiable | none | no remote URLs |
| structural_flags | none | C1-C8 and C3b evaluated |

## Confidence

- **Self-reported (in card)**: 0.72 (not used; its own table averages 0.67)
- **Calibrated (this report)**: 0.58
- **Formula applied**: min(0.58, 1.30, 0.80) = 0.58
- **Delta**: -0.14 (Symptom coverage 1.0 → 0.5)

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3, confidence < 0.85; multi_domain also holds; source_only_dynamic_claim and not_reproducible do not fire.
- **Execution restriction**: none.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | headline not an enum; 0.58 not below 0.50 |
| C2 | no | — | — | no enum excluded |
| C3 | no | — | — | no control arm cited; M-CTRL has own CONTROL-PROOF (diagnosability-tasklist.md:19) |
| C3b | no | — | — | runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes) matches execution-locus.md |
| C4 | no | — | — | M-SEED, M-REUSE, M-CTRL predictions + mappings; V-CLOSE/V-JSON value pairs |
| C5 | no | — | — | card 02:05Z vs card_mtime 02:06:00Z |
| C6 | no | — | — | no threshold asserted; bracket.md absent and not needed |
| C7 | no | — | — | environment claims carry SAME-ENV: yes in runs-in line; read as the row citation (alternative reading in Notes) |
| C8 | no | — | — | cites behaviour-definition: row 1; Status non-empty |

## Notes

- Verified: startup.ts:210, :196-197, :223-233, :187 (`setup || defaultTabs || didSpawnStartup`), :192 (`request.awaitTerminalProvisioning`); provisioning.ts:202-211; core/CLAUDE.md:45-53; ccsession-tag/README.md:228-237 (mirror exists; different line breaks, place by content); tests/core/test_orca_session_launch_guidance.py:17-30 (12 phrases); CLAUDE.md:308; ~/.claude/CLAUDE.md (no section; agrees with parent's N12 grep 0); N1/N7/N8/N12 consistent with tier1-observation.md.
- spot_check_unresolved (no directory given; not located with Read): workspace-creation.ts:209, :239-268; agent-launch-worktree-creation.ts:102; worker-worktree-creation.ts:80; federated-worker-agent-launch.ts:82; orca_worktree.py:594-610, :951-953 (bare name). They support V-JSON-from-source and "only three call sites set awaitTerminalProvisioning". The "seed awaited inside the create (workspace-creation.ts:209)" claim may be mislabelled: the matching `try { await ports.createTerminal` is at startup.ts:209-210.
- The card calls V-JSON "settled from checkout source", but the tasklist keeps V-JSON pending; source is not an observation of the installed binary.
- No behaviour-definition row for the provisioning-path seed or for `terminal close --all` behaviour (informational; C8 tests only the cited row).
- producers.md not an input; "P1 (surviving=yes)" label not checked.
- C7 ambiguity: if "cite a 2x2 row" needs an explicit row id beyond runs-in/SAME-ENV, C7 fires and caps at 0.50; verdict unchanged; C1 not fired.
- No assertion skipped; all inputs supplied except bracket.md (not needed).
- Not checked: Orca runs, daemon queries, orca_worktree.py, when the section entered src/superclaude/core/CLAUDE.md.
