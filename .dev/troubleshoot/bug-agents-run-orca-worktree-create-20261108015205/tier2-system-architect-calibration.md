# Calibration Report

<!-- Returned by confidence-calibrator, persisted by parent on receipt 2026-11-08T02:09Z -->

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/tier2-system-architect-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T02:06:52Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | All readable citations matched: startup.ts:202-210, :264-265, :147-148; provisioning.ts:189, :203; worktree-create-args.ts:87; CLAUDE.md:307-310, :312, :318-324, :320; core/CLAUDE.md:45-53; N1, N8, N12. Three absence claims not checkable with Read (Notes). |
| Runtime check | 0.5 | mixed: doc_contract x log_evidence 1.0, runtime_behavior x log_evidence 0.5 → 0.5. V-CLOSE sequence present, no captured output; "Runtime check performed?: no". |
| Symptom coverage | 0.5 | Cause well evidenced, but the fix reaches only sessions loading this repo's CLAUDE.md; N12: 4 of 5 hand-offs in Coder/IronOrca; Ironeye empty tab (N7) untraced. |
| Reproducibility fit | 0.5 | Deterministic (7 of 7 rows), no reproducer; installed vs checkout unproven. |
| Fix directness | 0.5 | Small local edit at CLAUDE.md:307-310 / :318-324, but depends on agents obeying; close command unverified; `--all` can kill an agent started there. |
| Domain coherence | 0.5 | mixed; Orca runtime in an external repo plus instruction file plus new test; "one file" conflicts with its "Test (new)" line. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.58 | 3.5 / 6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 0.80 | does not bind |
| gated_min | 0.58 | mean is the minimum |
| verdict_cap | none | M3a only for runtime_behavior; card is mixed |
| **calibrated** | 0.50 | 0.58, then C7 cap 0.50 |
| spot_check_unverifiable | none | no remote URLs |
| structural_flags | uncited | C7 fired (cap 0.5) |

## Confidence

- **Self-reported (in card)**: 0.66 (not used)
- **Calibrated (this report)**: 0.50
- **Formula applied**: min(0.58, 1.30, 0.80) = 0.58; C7 cap → 0.50
- **Delta**: -0.16 (Domain coherence 1.0 → 0.5; C7 cap)

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3, confidence < 0.85; multi_domain also holds. C1 not fired (0.50 not below 0.50).
- **Execution restriction**: none.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | final 0.50 not below 0.50 |
| C2 | no | — | — | excludes options B, C, D, not enums; C's rejection cites provisioning.ts:189, :203, worktree-create-args.ts:87 |
| C3 | no | — | — | no control arm cited; M-CTRL carries CONTROL-PROOF yes: startup.ts:265 |
| C3b | no | — | — | runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes) |
| C4 | no | — | — | M-SEED, M-REUSE, M-CTRL predictions + mappings; V-CLOSE/V-JSON value pairs; no enabling task |
| C5 | no | — | — | 02:06Z vs card_mtime 02:06:41Z |
| C6 | no | — | — | no threshold in headline |
| C7 | yes | `uncited` | calibrated capped at 0.5 (0.58 → 0.50) | card asserts "the installed copy on this host is stale" and names installed 1.4.245-aidev02 vs checkout dc57b3d6e8; tasklist has no 2x2 row for either (diagnosability-tasklist.md:13-19) |
| C8 | no | — | — | cites behaviour-definition row 1; row Status non-empty |

## Notes

- Claim classes read from header lines; no defaults.
- Unverified absence claims (Read only): no `setupOnly`/`setup-only` under IronOrca/src/cli; no test pins CLAUDE.md:303-325; B carries 12 pinned phrases in two copies. Validator should check.
- Overstatement: "most empty tabs come from ... cd (11 of 17)" counts creates, not tabs; of four live empty tabs (N7) two trace to own-use creates.
- Inconsistency: "one file, 2 edits" vs "Test (new)".
- Scope limit: N12 shows 4 of 5 hand-offs in Coder or IronOrca, unreachable by a project-only bullet.
- Pending proof: V-CLOSE; N3 says `--all` stops every terminal in the workspace.
- Structural flags fired: uncited (C7). No assertion skipped.
