# Phase 2 -- Tier 1.5 Verification Add-on

**Phase Goal:** Land A5 (3-way delta sweep) as the post-Tier-1 add-on the Phase 5 matrix designates as the dominant-concern detector for doc-claim drift. Pairs with B1 from Phase 1: substrate + 3-way diff has Phase-4-estimated joint effectiveness ~0.97 on this bug.

### T02.01 -- 3-way delta sweep (spec <-> mirror <-> live)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | The §4.2 status doc claimed a sync that did not happen; A5 detects the spec-vs-mirror-vs-live divergence directly so a future "in-sync" claim can be falsified before the build runs. Rank 5 of 14 (Priority 0.836); designated Tier 1.5 by Phase 5. |
| Effort | M |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [█████████-] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential, Serena |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/notes.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `three_way_delta_sweep(spec_path, mirror_path, live_path)` subroutine that emits a side-by-side diff table and a `DISCREPANCY: claim-not-applied` finding when the spec asserts a hunk that the mirror lacks but the live source contains (or any other 2-of-3 mismatch).

**Steps:**
1. **[PLANNING]** Load `/sc:reflect` source and identify the existing claim-evaluation pipeline that should host the new sweep.
2. **[PLANNING]** Define the input contract: a (spec_path, mirror_path, live_path) triple plus an optional anchor token (line number or stable string) for region-bounded sweeps.
3. **[EXECUTION]** Implement the sweep: parse `+`/`-` hunks from `spec_path`, locate the anchor in `mirror_path` and `live_path`, and compute pairwise diffs across the three sources at the anchor region.
4. **[EXECUTION]** Emit a finding: `DISCREPANCY: claim-not-applied` with three quoted regions (spec/mirror/live) when the spec hunk is present in only one of the two non-spec sources.
5. **[EXECUTION]** Add a fixture invocation: spec=`phase4.2-move-artifacts-to-opt-docker.md:141-160`, mirror=`pipeline-script-phase3.1.groovy:280-310`, live=`<live counterpart resolved during PLANNING step 1; e.g., the active Jenkins job XML for pipeline-script-phase3.1 if available, otherwise a known-good post-§4.2 reference file>`; confirm the fixture reproduces the bug's "spec applied to live but not to mirror" state.
6. **[VERIFICATION]** Run the protocol on the fixture and verify the DISCREPANCY block names all three sources and the anchor.
7. **[COMPLETION]** Document the contract, fixture, and example output in `TASKLIST_ROOT/artifacts/D-0004/spec.md` and copy the run log to `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `three_way_delta_sweep` subroutine accepting (spec_path, mirror_path, live_path) and emitting `DISCREPANCY: claim-not-applied` blocks per the documented schema.
- Running the patched protocol against the §4.2 fixture emits a DISCREPANCY block that quotes all three regions and the anchor; AND a combined run (T01.01 + T02.01) on the same fixture emits both `DISCREPANCY: untracked-substrate` and `DISCREPANCY: claim-not-applied` on the same anchor, evidencing the {B1, A5} ~0.97 joint detection per Phase 5 line 74.
- Two consecutive runs on the same fixture produce byte-identical DISCREPANCY blocks (deterministic).
- Subroutine, contract, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0004/spec.md` and `evidence.md`.

**Validation:**
- Manual check: re-running the sweep with a spec hunk fully applied to both mirror and live produces zero DISCREPANCY rows.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0004/`.

**Dependencies:** T01.01 (Track-state audit) -- pairs with B1 to reach Phase-4-estimated joint effectiveness ~0.97 on this bug; not a hard ordering dependency but recommended to land after.
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 5 calls A5 the "Tier 1.5 add-on" and explicitly says "{B1, A5} per Phase 4's synergy section: substrate + 3-way diff. Joint effectiveness ~0.97 on this bug." Phase 5 also flags A5 as the right pick "if doc-claim drift is the dominant ongoing concern".

### Checkpoint: End of Phase 2

**Purpose:** Confirm A5 lands cleanly on top of the Phase 1 trio and the joint {B1, A5} pair reaches the promised ~0.97 effectiveness on the bug fixture.

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`

**Verification:**
- T02.01 Acceptance Criteria 1 and 2 satisfied with the named subroutine and fixture run logged at `TASKLIST_ROOT/artifacts/D-0004/`.
- A combined `/sc:reflect` run that exercises both T01.01 and T02.01 against the bug fixture produces both `DISCREPANCY: untracked-substrate` and `DISCREPANCY: claim-not-applied` findings on the same anchor.
- No regression in Phase 1 outputs (the three Phase 1 finding categories still emit on the bug fixture).

**Exit Criteria:**
- A5 patch merged; combined run-log evidence saved at `TASKLIST_ROOT/evidence/`.
- Phase 3 (Tier 2 propagation & discipline layer) is unblocked.
- Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P02-END.md` records Pass AND records a preliminary ship-vs-retire stance for T04.01 (`A2 ⊂ A5`) and T04.03 (`B5 ≈ A5`) per Phase 5 line 77; final decision is made at the relevant Phase 4 step.
