# Patch Checklist

Generated: 2026-05-07
Total edits: 14 across 4 phase files + 1 index file

## File-by-file edit checklist

- `phase-1-tasklist.md`
  - [ ] Change T01.02 Effort from `L` to `M` (M1)
  - [ ] Replace T01.02 Step 2 "confirm `docs/migrations/` directory location with the user" with "create `docs/migrations/` per Phase 5 line 55 if it does not already exist" (L1)
  - [ ] Reword T01.03 Step 2 to mark the comment-syntax fallback as implementation-defined (L2)
  - [ ] Replace third Exit Criterion of "Checkpoint: End of Phase 1" with the joint-confidence ≥0.95 attestation requirement (M2)
- `phase-2-tasklist.md`
  - [ ] Raise T02.01 Confidence from `[███████---] 70%` to `[█████████-] 85%` (M3)
  - [ ] Add measurable joint-detection AC for {B1, A5} ~0.97 (replacing existing AC3 to keep count at 4) (L3)
  - [ ] Replace `<live equivalent>` placeholder in T02.01 Step 5 with explicit resolution rule (L4)
  - [ ] Replace third Exit Criterion of "Checkpoint: End of Phase 2" with retirement-stance recording for T04.01 and T04.03 (L5)
- `phase-3-tasklist.md`
  - [ ] Append B4 ⊃ B3 dominant-pair note to T03.01 Notes (L6)
  - [ ] Change T03.04 `Requires Confirmation` from `No` to `Yes` and append B4-coverage confirmation requirement to Notes (L7)
  - [ ] Fix End-of-Phase 3 checkpoint Purpose joint-confidence attribution (H1)
- `phase-4-tasklist.md`
  - [ ] Reword T04.01 Why to restore Phase 5's "reconsider" framing and add a Step 0 ship-vs-retire decision (M4)
  - [ ] Add ship-vs-retire decision step to T04.03 Step 1 (M5)
  - [ ] Decouple T04.06 from T04.05 mid-phase checkpoint; tie ship/Defer decision to "independent ledger initiative" (M6) -- affects T04.06 Dependencies and Phase 4 mid-phase checkpoint Exit Criteria
- `tasklist-index.md`
  - [ ] Update Deliverable Registry row D-0002 Effort from `L` to `M` (M1, propagation)
  - [ ] Update Traceability Matrix row R-005 Confidence from `70%` to `85%` (M3, propagation)

## Cross-file consistency sweep

- [ ] Confirm Effort field for D-0002 is `M` in both `phase-1-tasklist.md` (T01.02) and `tasklist-index.md` (Deliverable Registry).
- [ ] Confirm Confidence for T02.01 / R-005 is `85%` in both `phase-2-tasklist.md` and `tasklist-index.md` Traceability Matrix.
- [ ] Confirm "Tier 1 + Tier 1.5 + Tier 2" wording is removed; replaced with the roadmap-faithful Tier-2-on-top-of-Tier-1 framing wherever it appeared.

## Suggested execution order (highest-impact first)

1. H1 (End-of-Phase 3 checkpoint joint-confidence attribution) -- correct factual misattribution before any reader builds expectations from it.
2. M4, M5, M6 (Phase 4 ship-or-retire decision gates and de-coupling) -- these guard the most expensive work in the program.
3. M1, M3 (Effort and Confidence calibration) -- propagate to index simultaneously.
4. M2, L5 (checkpoint Exit Criteria for measurable joint-confidence and retirement-stance recording).
5. L1, L2, L3, L4, L6, L7 (wording precision and Note completeness; fast).

---

## Precise diff plan

### 1) `phase-1-tasklist.md`

#### Section/heading to change
- T01.02 metadata table; T01.02 Steps; T01.03 Steps; "Checkpoint: End of Phase 1" Exit Criteria

#### Planned edits

**A. T01.02 Effort L -> M (M1)**
Current issue: Effort field set to `L` overstates the ~130-180 LOC trio's per-task share.
Change: Set Effort field to `M`.
Diff intent:
- Before: `| Effort | L |`
- After: `| Effort | M |`

**B. T01.02 Step 2 invented user-confirmation step (L1)**
Current issue: Step 2 says "confirm `docs/migrations/` directory location with the user".
Change: Replace with creation directive based on roadmap line 55.
Diff intent:
- Before: `Define the registry frontmatter schema (fields: ...); confirm \`docs/migrations/\` directory location with the user.`
- After: `Define the registry frontmatter schema (fields: ...); create \`docs/migrations/\` per Phase 5 line 55 if it does not already exist.`

**C. T01.03 Step 2 invented comment-syntax fallback (L2)**
Current issue: Step 2 lists `# ssh:`/`# container:` comments alongside `HOST_*`/`CTR_*` constants as the "non-tagged context" rule; comment syntax is implementation-defined, not in roadmap.
Change: Mark comment-syntax option as implementation-defined.
Diff intent:
- Before: `... isn't immediately preceded by a \`HOST_\`/\`CTR_\` constant or an \`# ssh:\`/\`# container:\` comment.`
- After: `... isn't immediately preceded by a \`HOST_\`/\`CTR_\` constant. (Implementation may extend with a comment-syntax convention; this is implementation-defined.)`

**D. End-of-Phase 1 Checkpoint Exit Criterion (M2)**
Current issue: Purpose names the Phase-4 ≥0.95 promise but Exit Criteria do not require evidence of it.
Change: Replace the third Exit Criterion with an attestation requirement, keeping the count at exactly 3.
Diff intent:
- Before (third bullet): `Phase 2 (Tier 1.5 A5 add-on) is unblocked; checkpoint report at \`TASKLIST_ROOT/checkpoints/CP-P01-END.md\` records Pass.`
- After (third bullet): `Checkpoint report at \`TASKLIST_ROOT/checkpoints/CP-P01-END.md\` records Pass AND records a joint-confidence attestation ≥0.95 for the Tier 1 trio against the §4.2 bug fixture (per Phase 5 line 54), with method documented; Phase 2 (Tier 1.5 A5 add-on) is unblocked.`

### 2) `phase-2-tasklist.md`

#### Section/heading to change
- T02.01 metadata table; T02.01 Steps; T02.01 Acceptance Criteria; "Checkpoint: End of Phase 2" Exit Criteria

#### Planned edits

**A. T02.01 Confidence 70% -> 85% (M3)**
Current issue: Confidence understates Phase 5's explicit Tier 1.5 designation and ~0.97 synergy.
Change: Raise to 85%.
Diff intent:
- Before: `| Confidence | [███████---] 70% |`
- After: `| Confidence | [█████████-] 85% |`

**B. T02.01 Acceptance Criterion 3 -> measurable {B1, A5} joint-detection (L3)**
Current issue: ~0.97 synergy is mentioned in Notes/Phase goal but not measurable.
Change: Replace existing AC3 (the determinism criterion is currently AC3) -- but the protocol requires AC count = 4 with specific roles (functional, quality, determinism, documentation). Solution: append a measurable joint-detection clause to AC1 OR replace AC2 (quality bullet) with the joint-detection metric, since AC2 already speaks to "DISCREPANCY block that quotes all three regions and the anchor" -- this is the natural place to add the combined-run extension. Choosing: replace AC2.
Diff intent:
- Before AC2: `Running the patched protocol against the §4.2 fixture (spec asserts hunk applied to mirror; mirror lacks the hunk) emits a DISCREPANCY block that quotes all three regions and the anchor.`
- After AC2: `Running the patched protocol against the §4.2 fixture emits a DISCREPANCY block that quotes all three regions and the anchor; AND a combined run (T01.01 + T02.01) on the same fixture emits both \`DISCREPANCY: untracked-substrate\` and \`DISCREPANCY: claim-not-applied\` on the same anchor, evidencing the {B1, A5} ~0.97 joint detection per Phase 5 line 74.`

**C. T02.01 Step 5 placeholder resolution (L4)**
Current issue: `live=<live equivalent>` left as placeholder.
Change: Replace with explicit resolution rule.
Diff intent:
- Before: `live=\`<live equivalent>\``
- After: `live=\`<live counterpart resolved during PLANNING step 1; e.g., the active Jenkins job XML for pipeline-script-phase3.1 if available, otherwise a known-good post-§4.2 reference file>\``

**D. End-of-Phase 2 Checkpoint third Exit Criterion (L5)**
Current issue: Does not record retirement stance for T04.01/T04.03.
Change: Replace third Exit Criterion.
Diff intent:
- Before: `Checkpoint report at \`TASKLIST_ROOT/checkpoints/CP-P02-END.md\` records Pass.`
- After: `Checkpoint report at \`TASKLIST_ROOT/checkpoints/CP-P02-END.md\` records Pass AND records a preliminary ship-vs-retire stance for T04.01 (A2 ⊂ A5) and T04.03 (B5 ≈ A5) per Phase 5 line 77; final decision is made at the relevant Phase 4 step.`

### 3) `phase-3-tasklist.md`

#### Section/heading to change
- T03.01 Notes; T03.04 metadata table; T03.04 Notes; "Checkpoint: End of Phase 3" Purpose

#### Planned edits

**A. T03.01 Notes appendix on B4 ⊃ B3 dominant pair (L6)**
Current issue: T03.04 mentions `B3 ⊂ B4` but T03.01 has no symmetric note.
Change: Append a sentence to T03.01 Notes.
Diff intent:
- Before (Notes): `Phase 4 redundancy note: B3 ⊂ B4 -- when shipping B4, B3 may be retired downstream.`
- After (Notes): `Phase 4 redundancy note: B3 ⊂ B4 -- when shipping B4, B3 may be retired downstream. Mirror: shipping T03.01 may permit retiring T03.04; record the decision in \`feedback-log.md\` after T03.04 evaluation (per Phase 5 line 77).`

**B. T03.04 Requires Confirmation No -> Yes; Notes addendum (L7)**
Current issue: Conditional nature of B3 not surfaced via Requires Confirmation.
Change: Flip flag and add note.
Diff intent:
- Before: `| Requires Confirmation | No |`
- After: `| Requires Confirmation | Yes |`
- Notes addendum: `Confirm B4 (T03.01) coverage is insufficient before committing T03.04 effort -- record the confirmation in \`feedback-log.md\`.`

**C. End-of-Phase 3 Checkpoint Purpose joint-confidence attribution (H1)**
Current issue: Attributes ~0.99 to "Tier 1 + Tier 1.5 + Tier 2"; roadmap attributes it to Tier 2 stack on top of Tier 1.
Change: Replace the offending phrase.
Diff intent:
- Before: `Confirm Phase 3 lands cleanly and joint confidence on similar-shape regressions reaches the Phase-5-promised ~0.99 with the full Tier 1 + Tier 1.5 + Tier 2 stack.`
- After: `Confirm Phase 3 lands cleanly and joint confidence on similar-shape regressions reaches the Phase-5-promised ~0.99 with the Tier 2 stack shipped on top of Tier 1 (per Phase 5 line 58-59).`

### 4) `phase-4-tasklist.md`

#### Section/heading to change
- T04.01 Why; T04.01 Steps (insert Step 0); T04.03 Step 1; T04.06 Dependencies; Mid-phase checkpoint Exit Criteria

#### Planned edits

**A. T04.01 Why -- restore "reconsider" framing (M4)**
Current issue: Reframes "reconsider" as "becomes viable".
Change: Restore Phase 5's conditional language and add retirement option.
Diff intent:
- Before: `A2 detects when a spec's \`+\`/\`-\` hunks are not present in the named target file by parsing the spec hunks and re-grepping; Phase 5 notes "A2 has a real false-positive class without C2; if shipping C2 anyway, reconsider". With T03.07 (C2) shipped in Phase 3, this becomes viable. Rank 11 of 14 (Priority 0.666).`
- After: `A2 detects when a spec's \`+\`/\`-\` hunks are not present in the named target file by parsing the spec hunks and re-grepping; Phase 5 says A2 should be reconsidered once C2 ships -- the reconsideration may favor retirement (\`A2 ⊂ A5\` redundancy, line 77) rather than shipping. Confirm ship-vs-retire decision in \`feedback-log.md\` before executing. Rank 11 of 14 (Priority 0.666).`

**B. T04.01 add Step 0 ship-vs-retire decision (M4)**
Current issue: No decision step gating execution.
Change: Insert a Step 0 (renumbering existing 1-6 to 1-7).
Diff intent: Prepend `1. **[PLANNING]** Decide ship-vs-retire for A2 against the A5 (T02.01) shipped state per Phase 5 line 77 redundancy; record decision in \`feedback-log.md\`. Abort task if decision is Retire.` and renumber the existing six steps to 2-7.

**C. T04.03 Step 1 add A5-redundancy decision (M5)**
Current issue: B5 ≈ A5 only mentioned in Notes.
Change: Insert decision into Step 1.
Diff intent:
- Before Step 1: `Load \`/sc:reflect\`; load the fetcher decision from T04.02 (\`D-0013/spec.md\`); abort if T04.02 selected option (c) Deferred.`
- After Step 1: `Load \`/sc:reflect\`; load the fetcher decision from T04.02 (\`D-0013/spec.md\`); abort if T04.02 selected option (c) Deferred. If A5 (T02.01) shipped and is judged sufficient by \`feedback-log.md\`, prefer retiring B5 -- record rationale in \`D-0014/spec.md\` and abort. Proceed only if reconciliation against live Jenkins XML provides value beyond A5's spec/mirror/live sweep.`

**D. T04.06 Dependencies decoupling (M6)**
Current issue: Couples to T04.05 mid-phase checkpoint outcome.
Change: Tie to "independent ledger initiative" only.
Diff intent:
- Before: `Dependencies: None hard; Phase 5 says "defer unless an independent ledger is built for other reasons" -- consider the T04.05 mid-phase checkpoint outcome.`
- After: `Dependencies: None hard; ship only if an independent ledger initiative exists for other reasons (per Phase 5 line 64-65); otherwise Defer.`

**E. Mid-phase checkpoint T04.06 Exit Criterion (M6)**
Current issue: Couples T04.06 decision to mid-phase checkpoint.
Change: Replace Exit Criterion bullet wording.
Diff intent:
- Before: `Decision on T04.06: ship (independent ledger benefit confirmed) or Defer (cost-not-worth-it per Phase 5 §"Tier 3").`
- After: `Decision on T04.06: ship only if an independent ledger initiative exists for other reasons (per Phase 5 line 64-65); otherwise Defer.`

### 5) `tasklist-index.md`

#### Section/heading to change
- Deliverable Registry row D-0002; Traceability Matrix row R-005

#### Planned edits

**A. D-0002 Effort propagation L -> M (M1)**
Diff intent:
- Before: `| D-0002 | T01.02 | R-002 | ... | STRICT | Sub-agent (quality-engineer) | ... | L | Medium |`
- After: `| D-0002 | T01.02 | R-002 | ... | STRICT | Sub-agent (quality-engineer) | ... | M | Medium |`

**B. R-005 Confidence propagation 70% -> 85% (M3)**
Diff intent:
- Before: `| R-005 | T02.01 | D-0004 | STANDARD | 70% | \`TASKLIST_ROOT/artifacts/D-0004/\` |`
- After: `| R-005 | T02.01 | D-0004 | STANDARD | 85% | \`TASKLIST_ROOT/artifacts/D-0004/\` |`
