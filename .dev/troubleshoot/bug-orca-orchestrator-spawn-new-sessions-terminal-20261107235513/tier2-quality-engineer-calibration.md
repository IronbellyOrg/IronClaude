# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier2-quality-engineer-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T00:14:12Z
(Returned by confidence-calibrator; persisted by the parent. Notes condensed by the parent; scores, trace and rule rows as returned.)

Declared (inline bold fields): `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: AFFIRM`.

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.5 | Most Orca citations matched on Read (explicit-worker-terminal-validation.ts:49-54, dispatch-methods.ts:136-142, worker-topology.ts:67-76, worker-start-readiness-settlement.ts:107-147, local-worker-start.ts:122-130, worker-start-validation.ts:59-63, worker-start-agent-placement.ts:115-126, definitions-core-2.ts:69-74 and 83-87, guide 122-124, 145-161, 163-165). They show how an empty tab arises, not the reporter's case. "No silent-stall path exists" is an absence claim with several citations unchecked; three citations are off or misattributed (Notes). |
| Runtime check | 0.0 | (`runtime_behavior`, `source_static`) = 0.0; "Runtime check performed?: no"; no reproducer or captured output. |
| Symptom coverage | 0.5 | Explains the empty tab (P1) and recasts the wait as a normal `check --wait`; dismisses the user's "shortcut" cause as a human keypress on absence evidence only; P2 and P3 "not excluded". C3 also caps at 0.5. |
| Reproducibility fit | 0.5 | The seed is deterministic and observed once (O3); coexistence of an empty tab and a live worker tab never observed; whether an orchestrator chooses a bare create is an LLM choice. |
| Fix directness | 0.5 | Targets CLAUDE.md:308/320 (small, local), but it is a wording change that cannot force the choice and does nothing if P4 is real. The claim that `worktree create --agent claude` suppresses the seed has no cited code and no behaviour row. C4 fires. |
| Domain coherence | 0.5 | Orca runtime topology, project instruction text, LLM behaviour: two related domains. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.42 | (0.5+0.0+0.5+0.5+0.5+0.5)/6 |
| gate_M1: evidence_grounding + 0.30 | 0.80 | |
| gate_M2: runtime_check + 0.30 | 0.30 | binding |
| gated_min | 0.30 | |
| verdict_cap | 0.84 | M3a (runtime_behavior, runtime_check < 1.0, AFFIRM); not binding |
| **calibrated** | 0.30 | no C6/C7/C8 cap fired |
| spot_check_unverifiable | none (no remote URLs) | |
| structural_flags | locus_unknown, control_unproven, no_prereg_falsifier, headline_definite_low_confidence | C3b, C3, C4 at ceilings; C1 forces ESCALATE |

## Confidence

- **Self-reported (in card)**: 0.40 (not used as input)
- **Calibrated (this report)**: 0.30
- **Formula applied**: min(0.42, 0.80, 0.30) = 0.30; AFFIRM cap 0.84 not binding.
- **Delta**: -0.10

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: C1 (headline names P1; calibrated 0.30 < 0.50); rubric rule 3 independently. `source_only_dynamic_claim` and `multi_domain` also hold. Not marked `split_pending` by the calibrator (parent did not supply that context); the card and the Tier 1 card (P4) assert competing mechanisms, which is the parent's call under Wave 3 step 4.5.
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | yes | `headline_definite_low_confidence` | forced ESCALATE (`low_confidence`) | card headline names P1; calibrated 0.30 |
| C2 | no | — | — | two exclusions carry file:line exits (`--terminal` into a plain shell, `dispatch --inject`); P2, P3, P4 "not excluded" |
| C3 | yes | `control_unproven` | Symptom coverage ≤ 0.5 (already 0.5) | card cites O3 counter-case and "all supervised worker tabs are Claude" with no `CONTROL-PROOF: yes: <file:line>`; tasklist M-C records `CONTROL-PROOF: unknown` |
| C3b | yes | `locus_unknown` | Runtime check ≤ 0.5 (already 0.0) | card `runs-in=unknown` |
| C4 | yes | `no_prereg_falsifier` | Fix directness ≤ 0.5 (already 0.5) | discriminator form preregisters predictions, but the CLAUDE.md edit has a verification step and no rollback and cites no linked measurement row |
| C5 | no | — | — | Timestamp 2026-11-08T00:12:39Z earlier than card_mtime 00:13:53Z + 5 min |
| C6 | no | — | — | no numeric threshold or bracket |
| C7 | no | — | — | card names only `runs-in=unknown` and cites O3/O4; asserts no environment property as established |
| C8 | no | — | — | rows 1, 2, 3 exist with Status `fetched:local-source` |

## Notes

- Citations off or misattributed (headline unaffected): the guide reference table row is on line 208, not 209; `worker-worktree-creation.ts:85-93` — `callerProvidesInitialSurface` keys on `createdWithAgent` (line 82), with `runHooks:false` (78) and `activate:false` (93); the `startupAgent` block at 85-91 is conditional on `withAgentTerminal`. The `worker-start --worktree new-top-level` suppression is supported; the `worktree create --agent claude` suppression ("Both suppress") has no cited code and no behaviour row (row 2 says the `agent launch` side was not Read).
- Not verified: terminal-workspace-keydown.ts:71, use-tab-bar-runtime-model.ts:99, QuickLaunchButton.tsx:79, src/cli/handlers/terminal.ts:202, and the "no `newTerminal` in `src/main`" grep claim; the P3 exclusion rests on that absence claim.
- Verified: orca_worktree.py:27 documents "no link flag, no agent flag"; line 42 is the `orca agent launch --surface terminal` mention.
- Discriminator-form defects: (1) the observable (tab titled `worker-<taskId>`) does not show the worker started (`worker-topology.ts:73` sets the title at `createTerminal` time, before readiness); (2) row 5 (a comment) means a P4 case could still leave a `worker-<taskId>` tab; (3) the table row "true -> B refuted: so the worker started" overreaches; (4) Hypothesis A says a tab titled "Claude Code" but the observable checks `worker-<taskId>` (different titles; O3 shows live tabs end "· Claude Code"); (5) B includes a `recovery_shell` effect, which can co-occur with a worker tab, so A and B are not mutually exclusive. Reading the tab screen or `isTerminalRunningAgent` or the title suffix would separate them better.
- Unflagged environment assumption: every Orca source citation is from the local IronOrca checkout (HEAD dc57b3d6e8), not proven equal to installed 1.4.245-aidev02.
- Missing pieces behind the low scores: no executed probe, no CONTROL-PROOF line, no rollback, no linked measurement IDs on the fix.
- The "what orchestrators follow" evidence is /tmp/orch-skill-guide.md; the local IronOrca skill differs.
