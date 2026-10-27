---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Opus vs Haiku Roadmap Variants

## Round 1 — Initial Positions

### Variant A (Opus, 16-week, protocol-before-policy)

**Position on Timeline (D1):** A 16-week schedule is the realistic floor, not a buffered luxury. M7 alone owns 34 deliverables spanning 9 subcommands, 3 observability layers, 3 monitoring patterns, resume rehydration, detached lifecycle, and the non-precluding contract surface — Haiku's 1-week M7 ignores that this single milestone is larger than any wave milestone in the project. M5 (dispatch) and M6 (merge boundary) each carry high-risk items (R-01 merge erosion, R-09 IMM-5 boundary, R-05 ThreadPool surprise) that benefit from the 2-week wave cadence to allow author-review-rework cycles.

**Position on Recipe Placement (D2):** Recipes must land in M2 as a *protocol-first* foundation milestone. Every `LensEntry` in M3 declares `recipe_name`; if recipes don't exist by M3, the validator (FR-009/SC-013) can't actually verify the recipe-resolution invariant. Haiku's M5 placement means M3's `validate-lenses` is structurally aspirational — it cannot enforce its strongest guarantee until weeks later.

**Position on OQ-007/OQ-008 (D3):** Both must resolve in M1 design. `status_policy` is a JobSpec field (DM-001) and `WorkerSpec.count` interacts directly with the floor; deferring resolution means M5 dispatch design (Haiku M4) inherits unstable fields. Field churn in dataclasses cascades to schema, preflight, reduce, and every test fixture — paying the resolution cost upfront is strictly cheaper.

**Position on Detached Mode (D5):** `tmux.py` belongs in M7 alongside `attach`/`kill`. Haiku's split — `tmux.py` in M4, attach/kill in M7 — creates a 3-week zombie window where detached infrastructure exists but has no driving subcommands. SC-014 (end-to-end detached lifecycle) cannot pass until both halves land, so the M4 work is functionally unverified until M7.

**Position on CLI Surface (D6):** Concentrate the CLI surface in M7 so waves M4-M6 remain pure mechanism. Threading flags through every wave (Haiku's pattern) means the dispatch milestone must concurrently reason about `--amalgamation-mode`'s downstream merge semantics — a layering violation.

**Position on AC Traceability (D8):** Every AC-001..AC-017 should surface as a line item with an owning milestone. Haiku's pattern of "implicit AC satisfaction via parent FR/NFR" is unverifiable in code review — the reviewer has no checklist to tick.

### Variant B (Haiku, 12-week, vertical-slice)

**Position on Timeline (D1):** Twelve weeks reflects what the work actually requires. Opus inflates wave milestones to 2 weeks each on the assumption that the *mechanism* is the hard part — but the mechanism is well-specified (parent spec IMM-N invariants, ThreadPoolExecutor pattern from `sprint/`, recipes ported verbatim from `t2_normalize.py`). The risk lives in *integration*, which M8's dedicated 2-week integration milestone explicitly addresses. Opus is buffering risk that is already mitigated.

**Position on Recipe Placement (D2):** Recipes should co-evolve with their Wave 2 consumer in M5. Building 6 recipes in M2 before the dispatcher exists means recipe design happens *without* the calling context — leading to interface churn when Wave 2 finds the protocol awkward. Haiku's M2 ships `RecipeProtocol` interface + `passthrough` stub for lens validator wiring, and lets the 5 real recipes land alongside their dispatcher. The `validate-lenses` interim check (M2-M5) validates recipe *name registration*, not full execution — sufficient for the lens-registry gate.

**Position on OQ-007/OQ-008 (D3):** These are narrow contracts, not pervasive ones. `status_policy.floor` and worker-count guard semantics affect preflight error paths and reduce status determination — both isolated to M3/M4 in Haiku's plan. Forcing M1 resolution means data-model design happens without the preflight/dispatch context that would inform it. Field stability is achievable with sound dataclass design (Optional/Literal types), not by forcing premature decisions.

**Position on Detached Mode (D5):** `tmux.py` in M4 reflects that detached mode is *dispatch infrastructure* — the process-lifecycle wrapper is invoked by `run --detached`, which is fundamentally a dispatch concern. Attach/kill are subsequent lifecycle operations belonging in M7's CLI surface milestone. The "zombie window" Opus describes is real but tested via stub harness in M4; full E2E (SC-014) gates in M8.

**Position on CLI Surface (D6):** Vertical-slice delivery is how production systems actually ship — each milestone produces a callable, testable feature. Opus's "mechanism then surface" pattern means M4-M6 produces 14 weeks of un-callable code; integration risk explodes when wiring happens all at once in M7.

**Position on AC Traceability (D8):** ACs are *constraints*, not deliverables. AC-001 (3-layer separation) is satisfied by *module boundaries*, not by a line item in any one milestone. Treating ACs as line items inflates the milestone list and obscures the real work; structural ACs are verified at PR-review time and via the SC-NNN test suite.

## Round 2 — Rebuttals

### Variant A rebuts Variant B

**On Timeline:** Haiku's "risk lives in integration, M8 handles it" claim doesn't survive deliverable counting. Haiku's M8 has 18 deliverables in 2 weeks — the same density as Opus's M7 (34 in 3 weeks), but on more complex content (16 SC-NNN tests + invariant-suite + full pipeline integration). If M8's 2 weeks are realistic, then Opus's wave 2-week cadence is too — Haiku cannot have it both ways. The honest reading: Haiku front-loaded compression by shrinking *wave* milestones, then absorbed the unaddressed risk into a denser M8.

**On Recipe Placement:** Haiku's interim "recipe name registration" check is exactly the structural aspiration we flagged. The whole point of FR-009/SC-013 is to *catch* recipe-resolution failures *before* dispatch — a name-only check passes when the recipe is unimplemented, which is precisely the failure mode that bites at M5. The "interface churn from no calling context" concern is real but addressed by Opus's M2 stub-driven transport (M2 ships both Transport and Recipe protocols against the stub harness — they *do* have a calling context, just not Wave 1's real one).

**On OQ-007/OQ-008:** "Optional/Literal types absorb resolution" misses the point. The question isn't whether `status_policy` *fits* in DM-001 — it's whether the *defaults* (`floor=2`, `success_first=true`) and the warn-vs-STOP semantics are stable enough to write tests against. If M3 preflight design discovers we need a third semantic mode, every M1 fixture rewrites.

**On Detached Mode:** "Tested via stub harness in M4" is precisely what we mean by zombie work — code that passes its own tests but has no real driver until M7. SC-014's E2E gate means M4's tmux.py work cannot be marked truly complete until M7 finishes, so the milestone boundary is illusory.

**On CLI Surface:** "14 weeks of un-callable code" is a strawman. Opus's M4-M6 produces a fully-functional dispatch pipeline callable via the M1 `swarm validate` + spec-file path; the *user-facing flag surface* is what concentrates in M7, not the underlying dispatch capability.

**On AC Traceability:** AC-005 (ParallelExecutor reuse) and AC-009 (no scored merge) are *operational* not structural — they require active enforcement (grep audits, LOC caps, CI rules). Treating them as "constraints satisfied by module boundaries" is exactly how merge boundary erosion happens (R-01/R-02).

### Variant B rebuts Variant A

**On Timeline:** Opus's M7 deliverable count (34) is inflated by counting every AC and NFR line-item as a milestone deliverable. Strip the AC-NNN/NFR-NNN audit items (which are verification, not implementation), and M7 is closer to 20 real-work items — fitting comfortably in 1-2 weeks. Opus is double-counting verification work that M8 already owns.

**On Recipe Placement:** Opus claims M2 stub-driven recipes have "calling context" via the stub transport, but the stub returns *fixed strings* — it cannot exercise the parse-error salvage path (FR-030), the byte-equivalence requirement (COMP-027 ↔ t2_normalize.py), or the deterministic-path atomic-write coupling (FR-029). The "calling context" Opus claims is structural, not behavioral; real validation still waits for M5.

**On OQ-007/OQ-008:** "Every M1 fixture rewrites" assumes M1 ships test fixtures against `status_policy`. It doesn't — M1's tests are dataclass round-trip and import audits (per M1 exit criteria). Status-policy-semantic tests live in M6 (SC-004). The blast radius of late OQ resolution is bounded to schema + reduce, not M1 fixtures.

**On Detached Mode:** Opus's own integration-points table for M5 has `ParallelExecutor` flowing into M8's SC-002 — the same "tested in milestone N, gated in M8" pattern Opus is criticizing for M4 tmux. Either the pattern is acceptable (and Haiku's M4 placement is fine) or it isn't (and Opus's own structure violates it).

**On CLI Surface:** Opus's "M4-M6 callable via spec-file path" admission concedes Haiku's point — if dispatch is callable without flags, then the flag surface is genuinely surface, and surface work doesn't deserve 3 weeks. The 3-week M7 is buffering review burden, not real implementation work.

**On AC Traceability:** Opus conflates *enforcement mechanism* with *milestone line-item*. AC-005 is enforced by a grep audit (a CI rule), AC-009 by a LOC ceiling test (SC-012) and CI rule. These mechanisms live in M8 (test) and CI (continuous). Adding "AC-005" as a line item in M5 doesn't enforce it — the test in M8 does. Opus's pattern produces line-item theater.

## Convergence Assessment

### Areas of Substantial Agreement

Both variants converge on every architectural fundamental — the disputes are about *sequencing* and *granularity*, not *substance*:

- **Architecture:** Three-layer separation, ThreadPoolExecutor via ParallelExecutor, bundled lens dataclasses, mechanical merge ≤30 LOC, manifest-as-source-of-truth — full agreement.
- **Invariant treatment:** Same 16 SC-NNN tests, same parent-spec inheritance, same risk topology (R-01..R-09 substantially overlap).
- **Migration strategy:** Same M9 endgame — thin caller, A/B parity, scripts deletion.
- **Resolution shape for D7 (Integration-Points depth):** Opus's deeper tables are uncontroversially better; Haiku would not resist adoption.
- **Resolution for D9 (Decision Summary):** Substantive parity; both decision tables are sound.

### Remaining Disputes (Genuine Disagreement)

1. **Timeline (D1):** Unresolved. Opus's deliverable-count defense is strong but partially overlaps with verification work; Haiku's M8 density argument cuts both ways. **Recommended resolution:** 14 weeks as compromise — keeps Opus's 3-week M7 (largest surface) but compresses wave milestones to 1.5 weeks each.

2. **Recipe Placement (D2):** Opus's position is stronger. Haiku's rebuttal (stub returns fixed strings) is true but doesn't defeat the structural argument: the failure mode of unimplemented recipes biting at M5 is exactly what `validate-lenses` is supposed to prevent. **Recommended resolution:** Adopt Opus's M2 placement.

3. **OQ Resolution Timing (D3):** Haiku's bounded-blast-radius argument is technically correct but understates downstream churn risk. **Recommended resolution:** Resolve OQ-007/OQ-008 by M1 exit (Opus position), but defer to M2 if architect signals confidence in field-stability.

4. **Detached Mode Split (D5):** Haiku's tu-quoque rebuttal (Opus does the same with ParallelExecutor) lands. Both patterns ("build in M_X, gate in M8") are acceptable when the milestone has a real driver. The honest question: does M4 have a real driver for `tmux.py`? Without `--detached` as a subcommand option, no. **Recommended resolution:** Adopt Opus's M7 placement OR add `swarm run --detached` to M4 explicitly (Haiku's implicit assumption).

5. **CLI Surface Granularity (D6):** Genuine team-structure trade-off. **No universal winner.** Vertical-slice (Haiku) is right for small teams shipping incrementally; mechanism-first (Opus) is right for larger teams with separable review surfaces.

6. **AC Traceability (D8):** Opus is correct that *operational* ACs (AC-005, AC-009, AC-011) need active enforcement and benefit from line-item visibility. Haiku is correct that *structural* ACs (AC-001, AC-002, AC-004) are module-boundary properties. **Recommended resolution:** Split the AC class — operational ACs get line items (Opus), structural ACs become milestone preambles (Haiku).

### Convergence Score Rationale: 0.72

- ~85% architectural convergence (all fundamentals agreed)
- ~60% process convergence (sequencing disputes substantive but bounded)
- Three disputes resolve cleanly toward Opus (D2, D7, D8-operational)
- Two disputes are genuine team-structure choices with no universal answer (D1, D6)
- One dispute (D5) reduces to a clarifying question rather than a substantive disagreement
- Both variants would produce a working system; the merge target is achievable without forcing artificial convergence
