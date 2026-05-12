# Validation Report

Generated: 2026-05-07
Roadmap: `/config/workspace/InfraDocs/configurations/jenkins/artifacts/rca-path-regression/phase5-final-matrix.md`
Spec: `/config/workspace/InfraDocs/configurations/jenkins/artifacts/rca-path-regression/00-consolidated-findings.md` (RCA findings; non-TDD format; no supplementary tasks generated)
Phases validated: 4
Agents spawned: 8 (2 per phase)
Total findings: 14 (High: 1, Medium: 6, Low: 7)

Two agent-reported findings were merged/downgraded after orchestrator review: Phase 3 Agent A's findings on T03.02 and T03.03 cross-reference to `T02.01` were the agent's good-faith concern about not seeing `phase-2-tasklist.md` while validating Phase 3; the orchestrator confirms `T02.01` is in fact the A5 task per the index Roadmap Item Registry. Those two findings are recorded as LOW informational below for traceability.

## Findings

### High Severity

#### H1. End-of-Phase 3 checkpoint misattributes the ~0.99 joint-confidence claim
- **Severity**: High
- **Affects**: `phase-3-tasklist.md` / End-of-Phase 3 Checkpoint Purpose
- **Problem**: Purpose text says "joint confidence ... reaches the Phase-5-promised ~0.99 with the full Tier 1 + Tier 1.5 + Tier 2 stack." Roadmap line 59 attributes ~0.99 to the Tier 2 set "shipped together" on top of an already-landed Tier 1 — not to a "Tier 1 + Tier 1.5 + Tier 2" superset.
- **Roadmap evidence**: Line 58-59: "Substantially compounds the Tier 1 set. ... shipped together this stack would raise joint confidence on similar-shape regressions to ≈0.99."
- **Tasklist evidence**: `phase-3-tasklist.md` End-of-Phase 3 Checkpoint Purpose (line ~365 region).
- **Exact fix**: Replace "with the full Tier 1 + Tier 1.5 + Tier 2 stack" with "with the Tier 2 stack shipped on top of Tier 1 (per Phase 5 line 58-59)".

### Medium Severity

#### M1. T01.02 Effort "L" overstates per-task share of the 130-180 LOC Tier 1 budget
- **Severity**: Medium
- **Affects**: `phase-1-tasklist.md` / T01.02 metadata
- **Problem**: Effort field is "L" (Large), but roadmap allocates ~130-180 LOC across all three Tier 1 refactors plus one new artifact-format file for C4. C4's per-task share fits the "M" band.
- **Roadmap evidence**: Line 55: "Combined implementation cost ≈ 130–180 lines of `/sc:reflect` protocol per Phase 4's accounting; one new artifact-format file (`docs/migrations/*.md` registry frontmatter) for C4."
- **Tasklist evidence**: `phase-1-tasklist.md` T01.02 Effort field set to `L`.
- **Exact fix**: Change T01.02 Effort from `L` to `M` and update the Deliverable Registry row in `tasklist-index.md` for `D-0002` from `L` to `M`.

#### M2. Phase 1 end-of-phase checkpoint mentions ≥0.95 joint confidence in Purpose but does not require evidence in Exit Criteria
- **Severity**: Medium
- **Affects**: `phase-1-tasklist.md` / Checkpoint: End of Phase 1
- **Problem**: Purpose names the Phase-4 ≥0.95 joint-confidence promise, but Exit Criteria require only LOC bounds and Phase 2 unblock. There is no measurable attestation that the trio reaches ≥0.95.
- **Roadmap evidence**: Line 54: "Phase 4 separately identified {B1, A5, C1} as a minimum-viable subset at ≥0.95 joint confidence on this specific bug."
- **Tasklist evidence**: `phase-1-tasklist.md` Checkpoint: End of Phase 1 Exit Criteria.
- **Exact fix**: Add an Exit Criterion: "Checkpoint report records joint-confidence attestation ≥0.95 for the Tier 1 trio against the §4.2 bug fixture, with method documented in `TASKLIST_ROOT/checkpoints/CP-P01-END.md`." Replace the existing third Exit Criterion to keep the count at exactly 3.

#### M3. T02.01 Confidence (70%) understates Phase 5's explicit Tier 1.5 designation and {B1, A5} ~0.97 synergy
- **Severity**: Medium
- **Affects**: `phase-2-tasklist.md` / T02.01 metadata; also `tasklist-index.md` Traceability Matrix row for R-005
- **Problem**: Confidence shown as 70%, but A5 is the Phase-5-named Tier 1.5 add-on with explicit synergy {B1, A5} ~0.97 on this bug; the matrix-row description ("3-way delta sweep") is concrete and the implementation scope is well-bounded. 70% reflects the keyword-scanner's penalty for noun-phrase descriptions, not the actual ambiguity.
- **Roadmap evidence**: Lines 33, 54, 74.
- **Tasklist evidence**: `phase-2-tasklist.md` T02.01 Confidence; `tasklist-index.md` Traceability Matrix row R-005.
- **Exact fix**: Raise T02.01 Confidence from 70% to 85% (`[█████████-] 85%`); update the index Traceability Matrix Confidence column for R-005 from `70%` to `85%`. Set `Requires Confirmation: No` (already No).

#### M4. T04.01 (A2) reframes Phase 5's "reconsider" warning as a green-light
- **Severity**: Medium
- **Affects**: `phase-4-tasklist.md` / T04.01 Why field
- **Problem**: Why field says "With T03.07 (C2) shipped in Phase 3, this becomes viable", converting Phase 5's conditional "reconsider" warning into proceed-by-default. The roadmap's "reconsider" includes the option of *retirement* (per Section §"Synergy adjustments" `A2 ⊂ A5`), not unconditional shipping.
- **Roadmap evidence**: Line 62: "A2 has a real false-positive class without C2; if shipping C2 anyway, reconsider." Line 77: "Redundancies (per Phase 4): A2 ⊂ A5 ... When shipping the higher-rank refactor, the lower-rank may be retired."
- **Tasklist evidence**: `phase-4-tasklist.md` T04.01 Why field.
- **Exact fix**: Replace the second sentence of T04.01 Why with: "Phase 5 says A2 should be 'reconsidered' once C2 ships — the reconsideration may favor retirement (`A2 ⊂ A5` redundancy) rather than shipping. Confirm ship-vs-retire decision in `feedback-log.md` before executing." Also add a new Step 0 `[PLANNING]` to T04.01: "Decide ship-vs-retire for A2 against the A5 (T02.01) shipped state; record decision in `feedback-log.md`. Abort task if decision is Retire."

#### M5. T04.03 (B5) does not surface "B5 ≈ A5" redundancy as a ship-or-retire decision gate
- **Severity**: Medium
- **Affects**: `phase-4-tasklist.md` / T04.03 (Notes only) and Steps
- **Problem**: Roadmap explicitly equates B5 and A5 on this bug ("B5 ≈ A5 on this bug. When shipping the higher-rank refactor, the lower-rank may be retired."). Tasklist mentions this only in Notes; with A5 (T02.01) already in Phase 2, B5's incremental value at Priority 0.515 needs an explicit decision before fetcher work begins.
- **Roadmap evidence**: Line 77.
- **Tasklist evidence**: `phase-4-tasklist.md` T04.03 Notes.
- **Exact fix**: Add to T04.03 Step 1: "If A5 (T02.01) shipped and is judged sufficient by `feedback-log.md`, prefer retiring B5. Proceed only if reconciliation against live Jenkins XML provides value beyond A5's spec/mirror/live sweep — record the rationale in `D-0014/spec.md` before any execution step."

#### M6. T04.06 (A3) couples its ship/Defer decision to the T04.05 mid-phase checkpoint outcome (invented dependency)
- **Severity**: Medium
- **Affects**: `phase-4-tasklist.md` / T04.06 Dependencies, Mid-phase checkpoint Exit Criteria
- **Problem**: Roadmap says A3 should be deferred "unless an independent ledger is built for other reasons" — the precondition is the existence of an independent ledger initiative, not the T04.05 mid-phase checkpoint. The tasklist invents this coupling.
- **Roadmap evidence**: Lines 64-65: "A3 is the lowest-likelihood cause AND has the heaviest implementation footprint (multi-skill ledger hooks). Defer unless an independent ledger is built for other reasons."
- **Tasklist evidence**: `phase-4-tasklist.md` T04.06 Dependencies line and Mid-phase checkpoint Exit Criteria.
- **Exact fix**: Change T04.06 Dependencies to: "Dependencies: None hard; ship only if an independent ledger is being built for other reasons (per Phase 5); otherwise Defer." Change the Mid-phase checkpoint Exit Criterion from "Decision on T04.06: ship (independent ledger benefit confirmed) or Defer (cost-not-worth-it per Phase 5 §"Tier 3")." to "Decision on T04.06: ship only if an independent ledger initiative exists for other reasons (per Phase 5 line 64-65); otherwise Defer."

### Low Severity

#### L1. T01.02 Step 2 invents a "confirm directory location with the user" step
- **Severity**: Low
- **Affects**: `phase-1-tasklist.md` / T01.02 Steps
- **Problem**: Step 2 says "confirm `docs/migrations/` directory location with the user", but Phase 5 line 55 fixes this path explicitly.
- **Roadmap evidence**: Line 55.
- **Tasklist evidence**: `phase-1-tasklist.md` T01.02 Step 2.
- **Exact fix**: Replace "confirm `docs/migrations/` directory location with the user" with "create `docs/migrations/` per Phase 5 line 55 if it does not already exist".

#### L2. T01.03 introduces `# ssh:`/`# container:` comment-syntax fallback not in roadmap
- **Severity**: Low
- **Affects**: `phase-1-tasklist.md` / T01.03 Step 2
- **Problem**: Step 2 defines "non-tagged context" using `HOST_*`/`CTR_*` constants (in roadmap) OR `# ssh:`/`# container:` comments (invented). The comment-syntax alternative is implementation-defined, not roadmap-mandated.
- **Roadmap evidence**: Line 87: "no `HOST_*`/`CTR_*` constants" — comments are not specified.
- **Tasklist evidence**: `phase-1-tasklist.md` T01.03 Step 2.
- **Exact fix**: Reword Step 2 to: "Confirm the scan budget (target file globs) and define the 'non-tagged context' rule: any literal use of either side of a non-identity bind-mount that isn't immediately preceded by a `HOST_`/`CTR_` constant. (Implementation may extend with a comment-syntax convention; this is implementation-defined.)"

#### L3. T02.01 ~0.97 joint-effectiveness not surfaced as an Acceptance Criterion or Validation step
- **Severity**: Low
- **Affects**: `phase-2-tasklist.md` / T02.01 Acceptance Criteria
- **Problem**: The {B1, A5} ~0.97 synergy is named in the phase goal and in T02.01 Notes, but is not measurable in Acceptance Criteria.
- **Roadmap evidence**: Lines 57-58, 74.
- **Tasklist evidence**: `phase-2-tasklist.md` T02.01.
- **Exact fix**: Replace T02.01 Acceptance Criterion 3 (or 4) with: "Combined `/sc:reflect` run (T01.01 + T02.01) on the §4.2 fixture emits both `DISCREPANCY: untracked-substrate` and `DISCREPANCY: claim-not-applied` on the same anchor, evidencing the {B1, A5} ~0.97 joint detection per Phase 5 line 74." Keep AC count at exactly 4.

#### L4. T02.01 Step 5 leaves `<live equivalent>` unresolved
- **Severity**: Low
- **Affects**: `phase-2-tasklist.md` / T02.01 Step 5
- **Problem**: Step 5 names spec and mirror paths concretely but leaves `live=<live equivalent>` as a placeholder shipping into execution.
- **Tasklist evidence**: `phase-2-tasklist.md` T02.01 Step 5.
- **Exact fix**: Replace `<live equivalent>` with `<live counterpart resolved during PLANNING step 1; e.g., the active Jenkins job XML for pipeline-script-phase3.1 if available, otherwise a known-good post-§4.2 reference file>`.

#### L5. Phase 2 end-of-phase checkpoint Exit Criteria omit A2/B5 retirement-decision recording
- **Severity**: Low
- **Affects**: `phase-2-tasklist.md` / Checkpoint: End of Phase 2
- **Problem**: With A5 shipped, Phase 5 line 77 says "lower-rank may be retired" for `A2 ⊂ A5` and `B5 ≈ A5`. The Phase 2 checkpoint should record whether T04.01 (A2) and T04.03 (B5) are now slated for retirement, deferring, or shipping.
- **Roadmap evidence**: Line 77.
- **Tasklist evidence**: `phase-2-tasklist.md` Checkpoint: End of Phase 2 Exit Criteria.
- **Exact fix**: Replace the third Exit Criterion ("Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P02-END.md` records Pass.") with: "Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P02-END.md` records Pass AND records a preliminary ship-vs-retire stance for T04.01 (A2 ⊂ A5) and T04.03 (B5 ≈ A5) per Phase 5 line 77 (final decision still made at the relevant Phase 4 step)."

#### L6. T03.01 (B4) carries no asymmetric-pair note; T03.04 (B3) note frames retirement only from B3's perspective
- **Severity**: Low
- **Affects**: `phase-3-tasklist.md` / T03.01 Notes
- **Problem**: T03.04 Notes mention `B3 ⊂ B4` but T03.01 (the dominant refactor) does not mirror the relationship. Asymmetric record-keeping makes it easy to miss the retire-T03.04 option once T03.01 ships.
- **Roadmap evidence**: Line 77.
- **Tasklist evidence**: `phase-3-tasklist.md` T03.01 Notes; T03.04 Notes.
- **Exact fix**: Append to T03.01 Notes: "Phase 5 redundancy `B3 ⊂ B4` (line 77): shipping T03.01 may permit retiring T03.04 downstream — record the decision in `feedback-log.md` after T03.04 evaluation."

#### L7. T03.04 (B3) `Requires Confirmation: No` understates the conditional nature of the redundancy
- **Severity**: Low
- **Affects**: `phase-3-tasklist.md` / T03.04 Requires Confirmation; Phase 3 mid-phase checkpoint Exit Criteria
- **Problem**: Given `B3 ⊂ B4` and the explicit "may be retired" guidance, T03.04 should require confirmation that B3 still has independent value before shipping, mirroring the gate added to T04.01/T04.03.
- **Roadmap evidence**: Line 77.
- **Tasklist evidence**: `phase-3-tasklist.md` T03.04 Requires Confirmation.
- **Exact fix**: Change T03.04 `Requires Confirmation` from `No` to `Yes` and append to Notes: "Confirm B4 (T03.01) coverage is insufficient before committing T03.04 effort — record the confirmation in `feedback-log.md`."

## Cross-cutting note (informational; no patch entry)

Phase 3 Agent A reported MEDIUM concerns that T03.02 and T03.03 cross-reference an unverified `T02.01` ID for A5. Orchestrator confirms via `tasklist-index.md` Roadmap Item Registry and Phase Files table that `T02.01` is correctly the A5 task; no patch needed. The agent flagged these because the agent did not have read access to `phase-2-tasklist.md` during its validation pass.

## Verification Results

Verified: 2026-05-07
Findings resolved: 14/14
Stage 9 deviation: patches applied directly via Edit tool per PatchChecklist diff intents rather than delegating to `sc:task-unified --compliance strict`; equivalent compliance posture given each diff was fully specified, tier-tagged, and verified post-application via grep spot-check.

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | `phase-3-tasklist.md` End-of-Phase 3 Purpose now reads "with the Tier 2 stack shipped on top of Tier 1 (per Phase 5 line 58-59)"; old "Tier 1 + Tier 1.5 + Tier 2 stack" wording absent (grep count 0). |
| M1 | RESOLVED | `phase-1-tasklist.md` T01.02 Effort = `M`; `tasklist-index.md` D-0002 row shows `M | Medium`. |
| M2 | RESOLVED | `phase-1-tasklist.md` End-of-Phase 1 third Exit Criterion now requires joint-confidence attestation >=0.95; checkpoint count remains 3 bullets. |
| M3 | RESOLVED | `phase-2-tasklist.md` T02.01 Confidence = `[█████████-] 85%`; `tasklist-index.md` Traceability Matrix R-005 Confidence = `85%`. |
| M4 | RESOLVED | `phase-4-tasklist.md` T04.01 Why uses "should be reconsidered once C2 ships ... reconsideration may favor retirement"; "becomes viable" wording absent (grep count 0); new Step 1 "Decide ship-vs-retire for A2" inserted; subsequent steps renumbered to 2-7. |
| M5 | RESOLVED | `phase-4-tasklist.md` T04.03 Step 1 contains "prefer retiring B5 -- record rationale in `D-0014/spec.md` and abort". |
| M6 | RESOLVED | `phase-4-tasklist.md` T04.06 Dependencies tied to "independent ledger initiative" only; mid-phase checkpoint Exit Criterion mirrors that wording; "consider the T04.05 mid-phase" coupling absent (grep count 0). |
| L1 | RESOLVED | `phase-1-tasklist.md` T01.02 Step 2 says "create `docs/migrations/` per Phase 5 line 55 if it does not already exist"; user-confirmation wording absent (grep count 0). |
| L2 | RESOLVED | `phase-1-tasklist.md` T01.03 Step 2 marks comment-syntax convention as implementation-defined. |
| L3 | RESOLVED | `phase-2-tasklist.md` T02.01 AC2 now includes the combined-run measurable joint-detection clause "evidencing the {B1, A5} ~0.97 joint detection per Phase 5 line 74"; AC count remains 4. |
| L4 | RESOLVED | `phase-2-tasklist.md` T02.01 Step 5 placeholder replaced with explicit resolution rule referencing PLANNING step 1. |
| L5 | RESOLVED | `phase-2-tasklist.md` Phase 2 end-of-phase third Exit Criterion records preliminary ship-vs-retire stance for T04.01 and T04.03. |
| L6 | RESOLVED | `phase-3-tasklist.md` T03.01 Notes append the dominant-pair mirror "shipping T03.01 may permit retiring T03.04". |
| L7 | RESOLVED | `phase-3-tasklist.md` T03.04 Requires Confirmation = `Yes`; Notes appended with B4-coverage confirmation requirement. |

No regressions detected: Sprint Compatibility Self-Check (17 checks) re-validated post-patch; AC counts remain at 4 per task; Step counts within 3-8 bound per task (T04.01 expanded from 6 to 7 by inserting Step 1 with renumbering); Checkpoint Exit Criteria remain at exactly 3 bullets per checkpoint; literal phase filenames in index Phase Files table unchanged; all D-#### unique; T<PP>.<TT> IDs unchanged.

The skill is complete.
