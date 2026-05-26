# Adversarial Debate — Compliance Gating (D04 + D07 + D10 + D16 + D27)

**Task:** T04.03 — `/sc:adversarial` debates: MCP, persona, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-013
**Source feature characterization:** `feature-compliance-gating.md` (Phase 2 / T02.03)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17`
**Donor catalog tags:** D04 ADAPTABLE; D07 ADAPTABLE; D10 ADAPTABLE; D16 ADAPTABLE; D27 ADAPTABLE — all five sub-features carry the same tag class.
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-01..INV-03 collision claims below cite the labels at `extension-point-contracts.md:13-17` plus row-level reject criteria.

**Scope reminder:** Compliance gating is the aggregation of five sub-gates (Dispatch, Verification routing, MCP circuit-breaker, TFEP, Override flags) per `feature-compliance-gating.md:13-19`. This debate scores the cluster *as a package* because the sub-gates share the tier-source prerequisite and reinforce each other; sub-verdicts are noted where they diverge from the aggregate.

---

## Position A — Steelman for Inclusion

Compliance gating is the load-bearing safety architecture of the donor (`feature-compliance-gating.md:125`). The collective value of the five gates is that they convert a single classification into a *coordinated set of policy decisions* spanning dispatch, MCP requirements, verification depth, and failure-mode response — each scaled to risk. This is the donor's most valuable contribution because it is what makes `/sc:task`'s safety claims falsifiable rather than aspirational.

**Concrete value to `/task` (the recipient):**

1. **Risk-proportional cost.** Today `/task` runs *every* item through the same pipeline: Phase-Gate QA with `rf-qa` adversarial stance, max-3 fix cycles, Post-Completion Validation with `rf-qa` + `rf-qa-qualitative`. For an `auth/login.py` change this is appropriate; for a `README.md` typo fix it is overkill (the cost is the same). Compliance gating gives the recipient a way to spend 0 tokens on doc updates and 5K tokens on auth migrations.
2. **A safety mode `/task` lacks today.** `/task` has no notion of "this is a security-critical change; refuse to run if reasoning MCPs are down." The donor's Gate 3 (MCP circuit breaker, `feature-mcp-declarations.md`) closes that gap. `/task` has no notion of "test failure on a STRICT item must trigger forensic triage rather than log-and-continue." The donor's Gate 4 (TFEP) closes that gap. The two together are a *defense-in-depth* upgrade.
3. **Critical/Trivial Path Override** (`src/superclaude/skills/sc-task-protocol/SKILL.md:121, 123`) — pattern-based escalation/de-escalation independent of the prompt classifier. `auth/`, `security/`, `crypto/`, `models/`, `migrations/` paths force CRITICAL verification regardless of tier; `*.md`, `docs/`, `*test*.py` permit skipping verification regardless of tier. This is a robust safety floor and ceiling that the recipient does not currently have.

**Integration sketch (the cluster, package view):**

The recipient already has a single per-task `Tier:` field at the upstream tasklist-bundle layer (`donor-feature-catalog.md` D04 row: "the per-task `Tier:` field used in the upstream `sc:tasklist`-generated tasklist bundles is a conceptual mirror of the donor's Compliance axis"). Compliance gating attaches via:

- **Gate 1 — Dispatch at task entry**, *not* at per-item dispatch. Attaches at extension-point row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`). EXEMPT/LIGHT tasks skip the Phase-Gate QA and Post-Completion Validation paths entirely; STANDARD runs them as today; STRICT layers TFEP and MCP circuit-breaker on top. **No per-item dispatch inside F1 EXECUTE** — this is the critical commitment that keeps the cluster inside INV-01.
- **Gate 2 — Verification routing** attaches at extension-point row 10 (Phase-Gate QA Verification, C3; `extension-point-contracts.md:141-149`) as a routing refinement: the existing `rf-qa` invocation gains a tier-conditioned token-budget and timeout. LIGHT/EXEMPT skip the gate (consistent with row 10's admit rule that the gate may be *widened*, not bypassed for STANDARD/STRICT). The recipient keeps `rf-qa` adversarial-stance; the donor's `quality-engineer` agent type can be added to row 15's roster as an *additional* verifier for STRICT, not a replacement.
- **Gate 3 — MCP circuit-breaker** attaches at extension-point row 1 (Task File Validation gate, C5) **pre-loop, not per-item** — see `debate-mcp-declarations.md` Layer B verdict.
- **Gate 4 — TFEP** attaches at extension-point row 8 (Error Handling / blocker logging, C5/C3; `extension-point-contracts.md:123-131`). On test failure inside STRICT items, the existing "log and continue" branch is supplemented (not replaced) with a TFEP triage option — the item is logged as blocked, a `context.yaml` is written, and a forensic-tasklist insert is queued. The F1 loop continues to mark `- [x]` per existing rules; TFEP runs as a side-channel side-effect, preserving INV-01.
- **Gate 5 — Override flags** are re-encoded as **task-file frontmatter** fields (`tier: strict`, `skip_compliance: true`, `force_strict: true`, `no_escalation: true`). Row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`) is the native attach surface. The recipient is flagless by design; the cluster does not need to introduce a flag-parser.

**Why this is a net upgrade (and survives the invariant gate at the cluster level):**

- Gates 1, 3, 5 attach pre-loop and pre-EXECUTE; no INV-01 or INV-02 collision.
- Gate 2 attaches at the existing Phase-Gate QA surface (row 10, C3 admit); the donor's verification routing widens the existing single-method gate into a tier-conditioned multi-method gate — admissible per row 10's admit criteria.
- Gate 4 attaches at the existing Error Handling surface (row 8, C5/C3 admit); the donor's TFEP supplements (does not replace) the existing "log and continue" branch — admissible per row 8's admit criteria for "new failure-routing policies inside the existing taxonomy."

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**

- **Six distinct burdens** (`feature-compliance-gating.md:144-160`) — this is the largest coupling cost of any single feature in the donor catalog. The cluster is not free; it is the highest-cost feature on the table.
- **All five gates depend on the same upstream classification.** A misclassification at D09 propagates through every gate without correction (`feature-compliance-gating.md:139`). If the LLM classifies a 12-file refactor as LIGHT (because the prompt says "minor cleanup"), all five gates align to *zero* safety: inline dispatch, no MCP check, no verification, no TFEP, no override prompt. The cluster fails closed on safety only if classification is right; otherwise, it fails open at every gate simultaneously.
- **No gate has automated enforcement; all rely on LLM discipline** (`feature-compliance-gating.md:140`). "Block STRICT" (Gate 3) is prose, not code. The VIOLATION-level prohibitions in Gate 4 are prose. The dispatch switch in Gate 1 is prose. If the LLM decides — under context pressure, or after an `--skip-compliance` it has misinterpreted as `--skip-classification` — to bypass a gate, nothing in this repo intercepts.
- **The override flag set creates legitimate bypasses for *all* safety guarantees** (`feature-compliance-gating.md:141`). `--skip-compliance` bypasses Gates 2-4 entirely. `--no-escalation` explicitly "voids TFEP protection." A user habituated to typing escape-hatch flags during quick iteration cycles will silently downgrade their own safety.
- **Two-track dispatch creates knowledge bifurcation** (`feature-compliance-gating.md:142`). EXEMPT/LIGHT execute inline; STANDARD/STRICT execute through the deeper gate stack. Reviewers reading only the early-exit path see only half of the gating.
- **TFEP integration is non-trivial.** Gate 4 requires the recipient to (a) decide when `/task` switches from "log and continue" to "halt and forensically triage" — probably per-item-tier, (b) verify `/sc:forensic` exists in the repo (it does not; `feature-compliance-gating.md:156`), (c) extend DYNAMIC CONTENT MARKER mutation to accept TFEP's remediation block format. Each is non-trivial.

---

## Position B — Steelman for Rejection

**The cluster's coupling cost is uniquely large and several gates carry real invariant-collision risks if implemented sloppily.**

**Six coupling burdens** (`feature-compliance-gating.md:144-160`):

1. **A tier source** — shared with every other tier-conditioned feature; the most fundamental prerequisite. `/task`'s frontmatter schema at `src/superclaude/skills/task/SKILL.md:69` has no `Tier:` slot. The recipient must extend the schema (or the upstream task-builder pipeline) before any gate can run.
2. **A two-tier execution model inside the F1 loop.** Gate 1 routes EXEMPT/LIGHT to inline execution and STANDARD/STRICT to a deeper skill. `/task`'s F1 loop is single-track. **If Gate 1 attaches per-item inside F1 EXECUTE** (changing the loop's uniformity to a tier-conditioned per-item branch), it collides with INV-01 (`extension-point-contracts.md:13`: "EXECUTE exactly as written. No skipping, reordering, or out-of-band substitution.") — auto-REJECT per R-RULE-05.
3. **A verification-routing layer compatible with `/task`'s Phase-Gate QA.** Gate 2 maps tier → (verification method, token cost, timeout). The donor's table names `quality-engineer` for STRICT and direct Bash test execution for STANDARD; `/task`'s existing Phase-Gate QA uses `rf-qa` adversarial-stance with max-3 fix cycles. **If Gate 2 replaces `rf-qa` with the donor's verifiers**, INV-03 is at risk (`extension-point-contracts.md:15`: "Phase-gate `rf-qa` between phases" + `extension-point-contracts.md:144-148`: "Gates that bypass `rf-qa` invocation. → **INV-03**. Gates that downgrade adversarial stance to 'summarize what was done' (no zero-trust). → **INV-03**.") — also auto-REJECT.
4. **An MCP circuit breaker** — discharged separately in `debate-mcp-declarations.md` (Layer B). Sub-verdict there: DEFER, contingent on the cluster.
5. **TFEP integration** — Gate 4 enforces three VIOLATION rules on test failure. The donor's TFEP halts, freezes, writes `context.yaml`, invokes `/sc:forensic`, consumes `return-contract.yaml`, inserts a remediation block. **`/sc:forensic` does not exist in the repo** (`feature-compliance-gating.md:156`). Adopting Gate 4 forces the recipient to either build `/sc:forensic` (a new skill/command of unknown scope) or define a `/sc:forensic`-shaped contract that some other agent fulfils. The donor characterization for TFEP also has its own debate (`debate-tfep.md`, T04.02).
6. **An override flag set on a flagless skill.** Position A's mitigation (re-encode flags as task-file frontmatter) is workable but extends the schema by four fields; each field's interaction with the cluster's gates is its own micro-contract.

**Invariant-collision analysis (R-RULE-05 surfacing — required per task spec):**

- **Gate 1 INV-01 collision risk** is real if the implementer chooses per-item dispatch. The donor's Gate 1 fires "post-classification routing" — for a per-task tier, that is pre-loop and safe; for a per-item tier (the case where `/task` tasklist bundles carry per-item `Tier:` fields), it lands inside F1 EXECUTE and collides. The cluster does not specify which it is. **Position A commits to "pre-loop, not per-item" in its integration sketch** — that commitment is load-bearing for the cluster's verdict, and losing it forces C1 / auto-REJECT.
- **Gate 2 INV-03 collision risk** is real if the implementer replaces `rf-qa` rather than supplementing it. Position A commits to "supplementing, not replacing" — that commitment is load-bearing. If the donor's `quality-engineer`-based verification replaces `rf-qa`'s adversarial stance, the post-completion zero-leniency rule at `src/superclaude/skills/task/SKILL.md:248` is degraded (per `extension-point-contracts.md:148`), and INV-03 fails.
- **Gate 4 INV-02 collision risk.** TFEP's "halt and freeze" pattern is one design-decision away from "halt the F1 loop." If TFEP halts the loop on a test failure (rather than logging the item as blocked and side-channeling the forensic insert), the loop's progress guarantee (INV-01 "REPEAT") is broken, *and* the F2 prohibited action "Assuming completion" / "Skipping items" can be triggered when the loop is resumed with the TFEP block partially applied. Position A commits to "side-channel side-effect, preserving INV-01" — that commitment is load-bearing.

**These three load-bearing commitments are NOT specified in the donor characterization.** The donor prose says "block task execution" (Gate 3), "spawn quality-engineer sub-agent" (Gate 2), and "halt, freeze, write context.yaml" (Gate 4) without specifying the granularity (per-task vs per-item), the relationship to the existing `rf-qa` invocation (replace vs supplement), or the F1-loop integration (halt-loop vs side-channel). The cluster's invariant survival depends on three design decisions the donor did not make.

**Realistic failure mode #1 (cluster-level — fail-open on misclassification):** A 12-file refactor of `auth/login.py` is prompted as "small cleanup in login.py." The classifier (D09) emits LIGHT confidence 0.85. Gate 1 dispatches inline. Gates 2-4 are skipped. The `auth/` path *should* have triggered the Critical Path Override at `src/superclaude/skills/sc-task-protocol/SKILL.md:121`, but the override is implemented in the *donor* skill and the recipient is now executing inline. The override doesn't fire. A real auth change runs with zero verification, zero MCP check, zero TFEP. The cluster's safety is a function of classifier accuracy — and classifier accuracy is the donor's least-evidenced behavior (`feature-classification-header.md` etc.).

**Realistic failure mode #2 (Gate 4 INV-02 collision):** A STRICT item runs tests; tests fail. TFEP triggers per Gate 4. The donor's TFEP halts execution, writes `context.yaml`, and inserts a remediation tasklist block. The F1 loop is mid-iteration. The remediation block is inserted into the task file *outside* a DYNAMIC CONTENT MARKER section (donor's prose doesn't specify markers, because the donor doesn't have them). The F4 modification restriction (`src/superclaude/skills/task/SKILL.md:144-158`) is violated by the donor's own mechanism — INV-02 fails. On resume, the F1 loop READs a task file whose checklist has been mutated by a non-loop actor; mental-model drift is guaranteed.

**Realistic failure mode #3 (override-flag re-encoding misuse):** Position A's mitigation is `skip_compliance: true` as a task-file frontmatter field. A future task author copy-pastes the field across many task files thinking it means "this task is exempt from QA"; they intend EXEMPT but they have actually disabled Phase-Gate QA *and* Post-Completion Validation *and* the MCP circuit-breaker (`feature-compliance-gating.md:89`). The field's effect spans three INVs (INV-03 most prominently) and is invisible in the task file's checklist. The damage is silent.

**Maintenance cost:** Compliance gating is the largest feature in the donor catalog by surface area. Its policy is policy-as-prose (tier matrices, TFEP rules, override-flag semantics, MCP requirements). Every update drifts through `make sync-dev` and every drift is multi-surface. The recipient is taking on a permanent maintenance load proportional to the donor's gate count.

**R-RULE-06 secondary argument:** Aggregating five sub-gates into a single "cluster" is itself a form of ceremony — the *coordination behavior* between gates is what creates value (the donor argues that the gates fire in a sequenced order, `feature-compliance-gating.md:91-97`). The recipient already coordinates Phase-Gate QA + Post-Completion Validation + Error Handling around the F1 loop. Adopting the donor's *sequencing pattern* (override → classification → dispatch → MCP → verification → TFEP) means re-architecting the recipient's existing coordination — a structural change that the donor cannot reduce to a simple "absorb pattern" because the sequencing is the pattern.

---

## Evidence-Based Weighing

**Position A's strongest point (risk-proportional cost + safety modes `/task` lacks):** `/task` today over-spends on doc updates and lacks an MCP-availability circuit breaker or a TFEP-style forensic-triage path. The cluster supplies both. The Critical/Trivial Path Override gives a robust safety floor and ceiling independent of classifier confidence.

**Position B's answer:** Accepted as real value, but conditional on three load-bearing implementation commitments (pre-loop dispatch, supplement-not-replace `rf-qa`, side-channel TFEP), none of which the donor specifies. The recipient is *not* adopting the donor as written — the recipient is committing to a *design refinement* the donor did not make. If the refinement is unspecified at adoption time, the implementation is one design-decision away from C1 auto-REJECT on three separate gates. The risk-proportional-cost upgrade is real, but it can be delivered with much narrower surface area — e.g., just Gates 2 + 4 (verification routing + TFEP) — without inheriting the full six-burden cluster. The Critical/Trivial Path Override could be added to row 1 (Task File Validation gate) as a small standalone extension; it does not require the cluster.

**Position B's strongest point (invariant-collision in 3 of 5 gates if implemented sloppily + classification-dependence + flag-bypass + non-existent `/sc:forensic`):** Three gates have real invariant-collision risk; the cluster's safety value is gated by classifier accuracy; the override-flag set is a built-in safety bypass; Gate 4 requires `/sc:forensic` which does not exist in the repo.

**Position A's answer:**
- On the three load-bearing commitments: Position A's integration sketch already states them. The verdict should bind those commitments as preconditions for adoption — i.e., adopt the cluster *only* if the implementer commits to pre-loop dispatch + supplement-not-replace + side-channel TFEP. Phase 5 should encode these as manifest exceptions / preconditions per R-RULE-07.
- On classification-dependence: agreed, this is a real fragility. The Critical/Trivial Path Override (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) is the only defense, and it works *only* if integrated at the gate that fires regardless of classification verdict. Position A commits to wiring the override at row 1 as a pre-classification override pass. This raises K (cost) but preserves value.
- On the flag-bypass: agreed; the recipient should *not* adopt `skip_compliance` and `no_escalation`. The override flag set is the weakest part of the donor; adopting Gates 1-4 without Gate 5 is the right surface-narrowing.
- On `/sc:forensic`'s non-existence: agreed; Gate 4's TFEP integration is contingent on `debate-tfep.md`'s separate verdict. If TFEP is REJECTed in T04.02's debate, the cluster's Gate 4 is excised, and the cluster's coupling cost drops from 6 burdens to 5. If TFEP is ADOPTed or ADAPTed, Gate 4 is integrated under its own contract.

**Unanswered point against Position A:** Position B's failure mode #1 (fail-open on misclassification) is unrefuted at the cluster level — Position A acknowledges classifier-accuracy is the load-bearing input but cannot make it less load-bearing without re-architecting around classification. The Critical/Trivial Path Override mitigates the worst case but does not eliminate it. The cluster's safety has a structural ceiling at the classifier's accuracy floor. This is a real, persistent fragility Position A cannot dissolve.

**Unanswered point against Position B:** Position B's "the cluster can be narrowed to Gates 2 + 4 + Critical/Trivial Override" undercuts its own anti-cluster argument — if the cluster can be narrowed, the cluster's worst-case coupling cost is paid only if the recipient chooses to adopt the wide form. The cluster's pieces are separable, contrary to Position B's "package view" framing. The right question is *which gates*, not *whether the cluster*.

**Net effect:** The cluster's value is real and proportional to the gates adopted. The cluster's risk is real and proportional to the load-bearing commitments lost. The cluster is *separable* into per-gate adoption decisions — Gates 2 and the Critical/Trivial Path Override are the strongest sub-features; Gate 3 (MCP) is deferred separately (`debate-mcp-declarations.md`); Gate 4 (TFEP) is deferred separately (`debate-tfep.md`); Gate 1 (Dispatch) is admissible only at task-entry granularity; Gate 5 (Override flags) is the weakest sub-feature and should not transfer.

---

## Scored Verdict

Compliance gating is scored as a **package with per-sub-gate sub-verdicts** because the donor presents it as a unified feature but the sub-gates are separable.

### Cluster-aggregate score

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **4** | Risk-proportional cost (EXEMPT/LIGHT skip overhead; STRICT layers TFEP + MCP); Critical/Trivial Path Override (`src/superclaude/skills/sc-task-protocol/SKILL.md:121, 123`) gives a classification-independent safety floor; verification routing widens the existing single-method Phase-Gate QA. Real and substantial value. |
| **C (Complementarity, 1–5)** | **3** | C-band C3 at the cluster level: every sub-gate has a native or near-native attach point (row 1, row 8, row 10, row 13, row 15), **but only if** the three load-bearing commitments hold (pre-loop dispatch, supplement-not-replace `rf-qa`, side-channel TFEP). A sloppy implementation collides with INV-01 (Gate 1 per-item), INV-03 (Gate 2 `rf-qa` replacement), and INV-02 (Gate 4 loop-halt) — three separate C1 / auto-REJECT paths. C=3 reflects "extension surface exists but must be widened with new hooks" (`extension-point-contracts.md:25`) plus the design-precondition risk. |
| **K (Cost, 1–5)** | **5** | Six distinct burdens (`feature-compliance-gating.md:144-160`), the largest in the catalog. Plus three load-bearing implementation commitments that must be encoded as manifest exceptions per R-RULE-07. Plus ongoing maintenance of policy-as-prose across multiple surfaces. |
| **Net = (V × C) / K** | **(4 × 3) / 5 = 2.4** | |

**Cluster-aggregate verdict: DEFER** (Net = 2.4 falls in DEFER band).

### Per-sub-gate sub-verdicts

| Sub-gate | V | C | K | Net | Verdict | Notes |
|---|---|---|---|---|---|---|
| **Gate 1 — Dispatch (task-entry)** | 3 | 5 | 2 | 7.5 | **ADOPT** | At task-entry granularity (NOT per-item), pre-loop, attaches at row 1 (C5). EXEMPT/LIGHT skip the heavy verification path. INV-safe. |
| **Gate 2 — Verification routing** | 4 | 3 | 3 | 4.0 | **ADAPT** | Attaches at row 10 (C3) as a *widening* of existing Phase-Gate QA — tier-conditioned budget + timeout. **Bind commitment: `rf-qa` is supplemented, not replaced.** |
| **Gate 3 — MCP circuit-breaker** | 3 | 3 | 4 | 2.25 | **DEFER** | See `debate-mcp-declarations.md` Layer B — contingent on the cluster (this debate). With cluster ADAPTed, marginal cost drops; Layer B Net rises to 3.0 (ADAPT threshold). |
| **Gate 4 — TFEP** | TBD | TBD | TBD | TBD | **CONTINGENT on T04.02** | See `debate-tfep.md`. If TFEP is REJECTed there, Gate 4 is excised. If ADOPTed/ADAPTed, integrate via row 8 with side-channel commitment. |
| **Gate 5 — Override flags** | 1 | 2 | 3 | 0.67 | **REJECT** | Flag-bypass-of-safety-guarantees is the donor's weakest surface (`feature-compliance-gating.md:141`); re-encoding as frontmatter fields creates silent-misuse failure mode (failure mode #3 above). Do not transfer. |
| **Critical/Trivial Path Override** | 4 | 5 | 1 | 20.0 | **ADOPT** | Path-pattern-based classification-independent override at `src/superclaude/skills/sc-task-protocol/SKILL.md:121, 123`. Attaches at row 1 (C5) as a pre-classification override pass; tiny cost; high value (mitigates the cluster's classification-dependence). Strongest sub-feature in the cluster. |

### Composite verdict

The cluster's *aggregate* Net is DEFER, but the *sub-gates separate cleanly*:

- **Gate 1, Gate 2, Critical/Trivial Path Override** are the strongest pieces — these should advance to Phase 5 as ADOPT (Gate 1, Critical/Trivial Override) and ADAPT (Gate 2) with binding integration sketches.
- **Gate 3 (MCP)** advances as DEFER, contingent on whether the upstream tier source is established by Gate 1's adoption (it is, in the ADOPT verdict above). With that contingency resolved, Gate 3 effectively rises to ADAPT in Phase 5.
- **Gate 4 (TFEP)** advances as CONTINGENT on `debate-tfep.md`.
- **Gate 5 (Override flags)** advances as REJECT.

**Stack-rank inputs (for T04.05):**

The cluster is rolled forward as **five separate rows in the stack rank** (one per sub-gate), not one aggregate row, because the verdicts diverge materially:

- **Cluster aggregate**: V=4, C=3, K=5, Net=2.4, **DEFER (cluster-as-written)**.
- **Gate 1 (Dispatch / task-entry)**: V=3, C=5, K=2, Net=7.5, **ADOPT**.
- **Gate 2 (Verification routing)**: V=4, C=3, K=3, Net=4.0, **ADAPT**.
- **Gate 3 (MCP circuit-breaker)**: V=3, C=3, K=4, Net=2.25, **DEFER** → upgrades to **ADAPT** if Gate 1 is adopted.
- **Gate 4 (TFEP)**: contingent on `debate-tfep.md` (T04.02).
- **Gate 5 (Override flags)**: V=1, C=2, K=3, Net=0.67, **REJECT**.
- **Critical/Trivial Path Override**: V=4, C=5, K=1, Net=20.0, **ADOPT**.

**Phase 5 manifest exceptions per R-RULE-07 (load-bearing commitments):**

The cluster's INV-safety is contingent on three implementation commitments. If Phase 5 cannot bind these in the integration sketches, the per-sub-gate verdicts collapse:

1. **PRE-LOOP DISPATCH (Gate 1):** Dispatch fires once at task-entry, never per-item inside F1 EXECUTE. Per-item per-tier dispatch is auto-REJECT under INV-01.
2. **SUPPLEMENT-NOT-REPLACE `rf-qa` (Gate 2):** Tier-conditioned verification routing widens the existing Phase-Gate QA; `quality-engineer` is added to row 15's roster as an additional verifier, not as a replacement. Replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03.
3. **SIDE-CHANNEL TFEP (Gate 4, contingent):** If TFEP is adopted, its halt/freeze/insert pattern runs as a side-channel side-effect; the F1 loop continues to mark `- [x]` per existing rules. Halting the loop or mutating outside DYNAMIC CONTENT MARKER sections is auto-REJECT under INV-01 / INV-02.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The three load-bearing commitments are sourced from `extension-point-contracts.md` row-level reject criteria (rows 1, 8, 10, 15 — pages 60-225) plus the one-line INV labels at lines 13-17. Worked failure-mode examples in `invariant-bounds.md` would strengthen the audit trail for failure modes #1–#3 above but do not change the verdicts — the row-level reject criteria are sufficient to carry the commitments.
