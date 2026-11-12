# Calibration Report

<!-- Returned by confidence-calibrator, persisted by parent on receipt 2026-11-08T02:09Z -->

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/tier2-quality-engineer-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T02:06:52Z

Declared: claim_class mixed (doc_contract + runtime_behavior), evidence_class source_static, verdict AFFIRM. Not redetermined.

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Every checked file:line matches; runtime-local-worktree-terminal-startup.ts:187-201 and :202-214 as quoted; card's own gaps disclosed. |
| Runtime check | 0.5 | Cross-tab mixed = min(doc_contract/source_static 0.5, runtime_behavior/source_static 0.0) = 0.0; source_static override to 0.5 applied because the card includes runnable commands with no captured output (terminal list, terminal close --terminal, pytest line, V-JSON/V-CLOSE pending). Borderline: those commands test the fix, not the setup-race / --all claim. |
| Symptom coverage | 1.0 | Bare create seeds a plain tab and no rule says to close it; 7 of 7 daemon rows (M-SEED). |
| Reproducibility fit | 0.5 | Deterministic in logs; no reproducer run; installed vs checkout unproven. |
| Fix directness | 0.5 | Right area but 3 doc files + test + sync + separate issue; wording and test contradict each other; terminal-list timing unsettled. |
| Domain coherence | 0.5 | Orca runtime behaviour in instructions plus a test pin. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.67 | 4.0/6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 0.80 | not binding |
| gated_min | 0.67 | mean is the minimum |
| verdict_cap | 0.84 (not binding) | mixed includes runtime_behavior, runtime_check < 1.0, AFFIRM |
| **calibrated** | 0.67 | final |
| spot_check_unverifiable | none | no remote URLs |
| structural_flags | none | C1-C8 and C3b evaluated; none fired |

## Confidence

- **Self-reported (in card)**: 0.72 (not used)
- **Calibrated (this report)**: 0.67
- **Formula applied**: min(0.67, 1.30, 0.80) = 0.67; AFFIRM cap 0.84 not binding; no structural cap.
- **Delta**: -0.05

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3, confidence < 0.85; multi_domain also matches. C1 not fired.
- **Execution restriction**: none.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | 0.67 not below 0.50; headline names no enum token |
| C2 | no | — | — | no enum excluded; alternatives are fix options |
| C3 | no | — | — | card cites no control arm; M-CTRL has its own CONTROL-PROOF (diagnosability-tasklist.md:19) |
| C3b | no | — | — | runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes) |
| C4 | no | — | — | M-SEED, M-REUSE, M-CTRL have true/false values and mappings; V-CLOSE/V-JSON have value pairs and pending reasons |
| C5 | no | — | — | 02:06Z within card_mtime 02:06:21Z + 5 min |
| C6 | no | — | — | no numeric threshold in headline |
| C7 | no | — | — | installed vs checkout named only as an unproven gap; runs-in/SAME-ENV line present (borderline) |
| C8 | no | — | — | cites behaviour-definition: row 1; row 1 Status non-empty |

## Notes

- Verified: runtime-local-worktree-terminal-startup.ts:187-214, :259-269; tests/core/test_orca_session_launch_guidance.py:14-31 (12 phrases, section to next `\n## `, both copies); tests/core/test_claude_md_routing_block.py:21-50 (level-table only); core/CLAUDE.md:45-53; core/CLAUDE.md:51 differs from README.md:234-235; project CLAUDE.md:303-325; orca_worktree.py:594-610 (no --agent/--setup/--activate); tests/skills/test_issue_orca_worktree.py:794-820 (test_fo18_exact_commands_and_no_forbidden_flag), :1035-1071 (launch_calls, test_la1_launch_argument_list_is_exact).
- Fix wording contradicts its own test: the sentence says "Never use `--all`" and the test asserts `"--all" not in section` — the assertion would fail.
- The README section, split on `"\n## "`, extends through `#### The one question rule` to the next H2; a `--all` check scans all of it (not scanned for `--all`).
- Not re-verifiable with Read alone: absence claims (no plugins mirror, no test pinning project CLAUDE.md:303-325) and N3/N7/N8 quotes (read only as captured).
- Behaviour-definition gap: only row 1 (the seed) exists; `terminal close --all` vs `--terminal` and `terminal list` timing rest on help text (N3) with no definition row.
- Row mismatch: diagnosability-tasklist.md:25 defines V-CLOSE with `--all`; the card proposes V-CLOSE with `--terminal`.
- Sensitivity: rejecting the 0.5 override gives Runtime check 0.0 and calibrated min(0.58, 1.30, 0.30) = 0.30; verdict unchanged (ESCALATE, low_confidence + source_only_dynamic_claim).
- Not checked: other repos' CLAUDE.md rules (N12); provisionArgs / defaultTabs path.
- All optional inputs supplied; bracket.md not needed.
