# Adversarial Debate — Per-Tier Flow Branching (D10 + D15)

**Task:** T04.02 — `/sc:adversarial` debates: TFEP & per-tier flow branching
**Roadmap Item:** R-012
**Source feature characterization:** `feature-per-tier-branching.md` (Phase 2 / T02.02)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17`
**Donor catalog tags:** D10 = ADAPTABLE (command-side dispatch, `donor-feature-catalog.md:56`); D15 = ADAPTABLE — partial match (skill-side per-tier execution workflows, `donor-feature-catalog.md:66`)
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-01 (F1 loop semantics) and INV-05 (refusal of definition) collision-risk analysis below cites `extension-point-contracts.md:13-17` plus the row-4 reject criteria at lines 86-94 and the N3 negative-space row at lines 256-262.

---

## Position A — Steelman for Inclusion

Per-tier flow branching is the **only mechanism that translates a tier label into observable cost differentiation**. Without it, a `Tier:` field is metadata with no behavioral consequence — exactly the R-RULE-06 ceremony failure mode the donor's D02 was REJECTed for. The donor delivers the cost-gradient routing in two layers (`feature-per-tier-branching.md:11-18`):

- **Layer 1 (D10, command-side dispatch):** A four-way switch on tier (`src/superclaude/commands/task.md:95-101`) — EXEMPT/LIGHT execute inline; STANDARD/STRICT invoke `Skill sc:task-protocol`. Selects the executor.
- **Layer 2 (D15, skill-side per-tier workflows):** Four step-lists at `src/superclaude/skills/sc-task-protocol/SKILL.md:76-109` — STRICT (11 steps), STANDARD (5), LIGHT (4), EXEMPT (2). Selects the procedure inside the executor.

The standalone value claim (`feature-per-tier-branching.md:139-146`) is concrete: for a 20-item mixed-tier batch — 5 typos (LIGHT), 5 explanations (EXEMPT), 8 features (STANDARD), 2 security migrations (STRICT) — per-tier branching is the difference between paying STRICT cost on all 20 items (≈100K verification tokens) and paying it on 2 (≈10K), with the other 18 paying ≈4K total: **a 6-7× total verification-cost reduction.**

**Integration sketch (LAYER 1 only — Layer 2 is upstream-of-`/task` or merges with the compliance-gating cluster):**

- **Layer 1 — task-entry dispatch (not per-item):** Attach at row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`). After validation succeeds and the optional `Tier:` field is read (D09a), the validator routes the task into one of two execution shapes: (a) for LIGHT/EXEMPT, a lightweight execution profile that skips Phase-Gate QA's heavy verification but otherwise runs the F1 loop normally; (b) for STANDARD/STRICT, the full F1 + Phase-Gate QA + Post-Completion Validation pipeline. **This is exactly the compliance-gating cluster's Gate 1 (Dispatch task-entry, ADOPT, Net=7.5)** — Layer 1 and Gate 1 are the same feature seen from different donor sub-rows.
- **Layer 2 — DEFERRED to upstream-or-skip:** The four per-tier step-lists at `SKILL.md:76-109` are donor-side execution profiles. On the recipient side, the F1 loop is *the* execution profile — there is no native room for four parallel step-lists indexed by tier. Layer 2's value is partially absorbed by Gate 2 (Verification routing, ADAPT, Net=4.0) which varies the verification *cost budget* by tier; the remaining Layer 2 content (serena activate, git-clean check, codebase-retrieval, memory check) is *pre-flight scaffolding* that belongs at row 2 (First Item Protocol) as additive setup steps, gated by tier.
- **Scope of this debate:** Per-tier flow branching's *dispatch* part (Layer 1) is the absorbable core; the *step-list* part (Layer 2) is partially absorbed elsewhere (Gate 2 + row 2 additions) and partially deferred.

**Why this might be a net upgrade over the status quo:**

`/task` today is single-track: every task runs the same F1 + Phase-Gate QA + Post-Completion Validation pipeline regardless of risk. A typo fix pays the same verification overhead as a `migrations/` change. Layer 1 (= Gate 1) closes that gap by *skipping* the heavy verification path on EXEMPT/LIGHT. The cost-gradient claim is real and quantifiable on heterogeneous mixes.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**

- **The homogeneous-tier-mix non-value condition is real** (`feature-per-tier-branching.md:152`). For a 20-item all-STANDARD tasklist (the default tier), Layer 1 always dispatches to the same execution shape; branching is *evaluated* but never *branches anywhere different*. The 6-7× cost reduction collapses to 0.
- **Layer 1 IS Gate 1.** Position A is not asking for a *second* dispatch ADOPT — Layer 1 is already covered by the compliance-gating cluster's Gate 1 (Net=7.5, ADOPT). Adopting D10 as a separate row would double-count the same surface.
- **Layer 2 (four step-lists indexed by tier) does not have a native attach** on `/task`. The F1 EXECUTE step's action-to-tool mapping at `src/superclaude/skills/task/SKILL.md:89-96` is a *per-item-action* dispatch, not a *per-tier-procedure* dispatch. Adopting Layer 2 as written would require either (a) wrapping every F1 EXECUTE invocation in a tier-aware pre-step (verbosity), (b) authoring four parallel skills indexed by tier (proliferation), or (c) inlining the tier-keyed branches inside EXECUTE (mutates F1 loop dispatch semantics → **INV-01 risk**).
- **The six coupling burdens** (`feature-per-tier-branching.md:160-174`) include three that touch `/task` invariants directly: burden #1 (two-track executor model that doesn't exist), burden #4 (Phase-Gate QA tier-sensitivity — INV-03 collision risk), burden #6 (LIGHT/EXEMPT skip-verification semantic vs `/task`'s always-run Phase-Gate QA — INV-03 collision risk).
- **MCP availability gate** (burden #5) requires inventing a tier-aware MCP probe at task entry — this is the same Gate 3 (MCP circuit-breaker, DEFER, Net=2.25 conditional on Gate 1) the compliance-gating cluster already debates. Not new work, but transitively coupled.

---

## Position B — Steelman for Rejection (with explicit INV-01 and INV-05 attachment-safety analysis per T04.02 acceptance criteria)

**INV-01 (F1 loop semantics: EXECUTE exactly as written) attachment-safety analysis:**

INV-01 at `extension-point-contracts.md:13` is: "READ first unchecked `- [ ]`, EXECUTE exactly as written, UPDATE to `- [x]`, REPEAT. No skipping, reordering, or out-of-band substitution." Layer 2's four per-tier step-lists *replace* the executed item's content with a tier-keyed step-list (`SKILL.md:80-91` for STRICT, etc.). Translated to `/task`: if a STRICT item's text says "Implement the auth-token refresh logic," but Layer 2 says STRICT executes 11 specific steps (serena activate, git status, codebase-retrieval, memory check, etc.), the executor is no longer "executing exactly as written" — it is executing **a tier-substituted procedure** that overrides the item's literal text.

Row 4 (F1 EXECUTE item-type dispatch) reject criteria at `extension-point-contracts.md:89-93` are unambiguous on this:
> - Action verbs whose completion is unverifiable (no disk artifact, no command output). → INV-02
> - Action verbs that decide *which item* to execute next (override IDENTIFY). → INV-05, INV-01.
> - Action verbs that complete asynchronously without a synchronous re-read at completion. → INV-04.

A tier-keyed action verb that *substitutes* the item's content with a procedure is structurally equivalent to "deciding what to execute" — an INV-05 + INV-01 collision. **Layer 2 as written collides with INV-01 if implemented as a per-item tier-keyed substitution inside EXECUTE.** The only INV-safe shape for Layer 2 is *to not implement it at all* on the recipient side — the four step-lists are donor-internal execution profiles that translate to `/task` as "things task-builder should put in the checklist explicitly, item by item" or as "Gate 2 verification-routing parameters" (the latter is what the compliance-gating cluster covers).

**INV-05 (refusal of definition) attachment-safety analysis:**

INV-05 at `extension-point-contracts.md:17` is: "`/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*." Layer 1's branching on tier consumes a tier value the file provides (clean — no INV-05 collision). But Layer 2's per-tier step-lists *define* what the executor does for each tier — they encode procedural intent that should live in the task file itself, not in the executor. **A `/task` that implements "for STRICT items, do these 11 steps" is making a what-to-do decision that INV-05 prohibits.** The task file should specify the 11 steps as 11 explicit checklist items if they are needed; the executor should not synthesize them from a tier value.

This is the same failure mode `debate-persona-activation.md` REJECTed under R-RULE-05 (per-item auto-inference of persona content). Layer 2 is structurally identical: per-item auto-substitution of *procedure* content. Auto-REJECT under R-RULE-05.

**The donor catalog's own framing isolates Layer 2 as ADAPTABLE-PARTIAL-MATCH** (`donor-feature-catalog.md:66`): "STRICT's 'spawn verification agent (quality-engineer)' sub-step is a partial duplicate of `/task`'s Phase-Gate QA at `SKILL.md:182-211` (`rf-qa` adversarial stance, fix authorization, 'ensuring...' clause extraction, 3-cycle fix loop). The remaining donor sub-steps — serena activate, git-clean check, codebase-retrieval, memory check, affected-file identification, import tracing, pytest, adversarial questions — have **no `/task` analog** and are net-new pre-loop / pre-EXECUTE scaffolding that would attach at the Task File Validation gate `SKILL.md:64-73` or First Item Protocol `SKILL.md:100-102`." The catalog itself routes Layer 2 to row 1 / row 2 as *pre-flight scaffolding*, not as in-loop dispatch.

**Six coupling burdens, four of which collide with invariants if implemented sloppily** (`feature-per-tier-branching.md:160-174`):

| # | Burden | INV impact |
|---|---|---|
| 1 | Two-track executor model | INV-01 risk if F1 loop is wrapped in a per-item tier-dispatch (loop semantics mutate) |
| 2 | `Tier:` field per-item or per-task | Clean — shared with D09a (already ADOPT) |
| 3 | Way to invoke four different workflows from inside F1 EXECUTE | INV-01/INV-05 risk — Layer 2 implementation surface |
| 4 | Phase-Gate QA tier-sensitivity | INV-03 risk — shared with Gate 2 manifest exception |
| 5 | MCP-availability gate matching circuit breaker | Clean if attached at row 1; transitively coupled to Gate 3 |
| 6 | LIGHT/EXEMPT "skip verification" semantic | INV-03 risk — Phase-Gate QA must become tier-aware without replacing `rf-qa` |

Four of six burdens (#1, #3, #4, #6) touch invariant neighborhoods. The clean two (#2, #5) are already covered by D09a and Gate 3 respectively.

**Realistic failure mode #1 (Layer 2 implemented as per-item EXECUTE substitution → INV-01 collision):** A `/task` STRICT-tier item reads "Update the auth-token refresh logic." The executor consults Layer 2 and substitutes the item with the 11-step STRICT workflow (serena activate, git status, codebase-retrieval, memory check, etc.) — none of which is "Update the auth-token refresh logic." The executed work is *adjacent to* but *not equal to* what the item says. INV-01 ("EXECUTE exactly as written") fires; row 4 reject criteria at `extension-point-contracts.md:89-93` trigger C1 auto-REJECT.

**Realistic failure mode #2 (Layer 1 implemented as per-item dispatch instead of task-entry → INV-01 collision):** Per-item dispatch on a `Tier:` annotation inside F1 EXECUTE creates a *control-surface inside the loop* that the loop itself does not own. The "EXECUTE exactly as written" guarantee no longer holds — the loop's behavior is now governed by an out-of-band tier annotation. The compliance-gating cluster's Gate 1 manifest exception #1 names this exact failure mode (`debate-compliance-gating.md`:158): "Pre-loop dispatch (Gate 1): Dispatch fires once at task-entry, never per-item inside F1 EXECUTE. Per-item per-tier dispatch is auto-REJECT under INV-01."

**Realistic failure mode #3 (LIGHT/EXEMPT skip verification vs always-run Phase-Gate QA → INV-03 collision):** `/task`'s Phase-Gate QA runs between every phase (`SKILL.md:182-211`); the donor's LIGHT/EXEMPT branches skip verification entirely (`SKILL.md:118-119`). If the recipient implements the skip naively (Phase-Gate QA refuses to run on LIGHT/EXEMPT phases), the always-run invariant breaks — INV-03 fires. The Phase 5 manifest exception must commit to either (a) supplementing Phase-Gate QA with tier-aware *cost budget* without skipping (preserves INV-03), or (b) keeping Phase-Gate QA always-on with a much lower budget on LIGHT/EXEMPT (also preserves INV-03 but partially loses the donor's cost-skip value).

**Duplication with compliance-gating cluster:** Layer 1 (D10) is structurally identical to Gate 1 of the compliance-gating cluster. Gate 1 already carries V=3, C=5, K=2, Net=7.5, ADOPT with a binding manifest exception #1 (pre-loop dispatch, never per-item). Layer 2 (D15) is partially absorbed by Gate 2 (Verification routing, V=4, C=3, K=3, Net=4.0, ADAPT). **Adopting D10 as a separate row would double-count Gate 1; adopting D15 as a separate row would double-count Gate 2** plus add the four-step-lists-inside-EXECUTE INV-01 risk that Gate 2 does not carry. The right disposition is to merge: D10 *is* Gate 1; D15's pre-flight scaffolding subset attaches at row 2 with tier-gating; D15's verification-stance subset *is* Gate 2; D15's remainder (the procedural step-lists) is REJECT (INV-01 + INV-05 collision).

**Net effect on Phase 1 catalog (`donor-feature-catalog.md:56, 66`):** Both rows are tagged ADAPTABLE; the catalog's framing for D10 is "tiered dispatch would need to gate which per-item workflow runs in EXECUTE" — which is exactly the per-item path Position B is REJECTing. The catalog's framing for D15 is "partial match on one sub-step only" — confirming the catalog itself sees most of Layer 2 as non-absorbable.

---

## Evidence-Based Weighing

**Position A's strongest point (cost-gradient routing on heterogeneous tier mixes):** A 6-7× total verification-cost reduction for a realistic 20-item heterogeneous batch is real, quantifiable, and bound to this feature's existence. Without per-tier branching, all `/task` invocations pay STRICT-tier verification cost regardless of risk.

**Position B's answer:** Accepted as the value-claim, *but* the value is delivered by Gate 1 (Layer 1 absorbed) + Gate 2 (Layer 2 verification-stance absorbed) of the compliance-gating cluster, which already carry ADOPT/ADAPT verdicts. Per-tier branching as a *separate* Phase 4 row is double-counting. The remaining Layer 2 content — the four procedural step-lists inside EXECUTE — collides with INV-01 + INV-05 and is auto-REJECT under R-RULE-05. The cost-gradient value belongs to the compliance-gating cluster, not to a parallel per-tier-branching row.

**Position B's strongest point (Layer 1 IS Gate 1 — double-counting risk; Layer 2's procedural step-lists collide with INV-01 + INV-05; donor catalog itself routes Layer 2 to row 1/row 2 as pre-flight scaffolding, not as in-loop dispatch):** Three convergent restriction lines. Per-tier flow branching as a separate ADOPT row is structurally not a separate feature; it is the union of Gate 1 + Gate 2 + (REJECTed) Layer 2 procedural substitution.

**Position A's answer:** Concedes Layer 1 = Gate 1 (same surface, no double-count). Concedes Layer 2's verification-stance subset is absorbed by Gate 2. Concedes Layer 2's procedural step-lists are INV-01/INV-05 colliders and should not enter `/task` as a per-item substitution. The remaining piece Position A wants to keep is Layer 2's *pre-flight scaffolding* (serena activate, git-clean check, codebase-retrieval, memory check, baseline) as additive setup steps at row 2 (First Item Protocol, C5), gated by tier. Position A narrows the verdict to: D10 = MERGE-WITH-GATE-1 (no separate row in the stack rank); D15 = SPLIT (verification-stance → MERGE-WITH-GATE-2; pre-flight scaffolding → ADOPT at row 2 with tier-gating; procedural step-lists → REJECT).

**Unanswered point against Position A:** The pre-flight scaffolding subset Position A wants to absorb (serena activate, git-clean, codebase-retrieval, memory check, baseline) has its own load-bearing dependencies — serena availability, auggie availability, a writable test baseline (D21 — already separately ADOPTed under `debate-tfep.md`). The pre-flight subset duplicates D21 (baseline) and Gate 3 (MCP availability), creating a third double-counting opportunity. Position A did not show the pre-flight subset has *unique* value beyond what D21 + Gate 3 + the existing Task File Validation gate cover.

**Unanswered point against Position B:** Position B's "Layer 1 IS Gate 1" framing is structurally correct, but Position A's "the same surface seen from two donor rows" framing is also valid — the donor presented two separate sub-features (D10 command-side + D15 skill-side) that the recipient absorbs as one cluster row. The stack-rank decision is whether to (a) carry per-tier branching as a separate row with explicit MERGE-WITH-GATE-1/Gate-2 cross-references, or (b) drop the per-tier branching row entirely and route all value through the compliance-gating cluster rows. Position B's preferred option (b) is cleaner; Position A's preferred option (a) preserves donor-row traceability. Either is defensible.

**Net effect:** Per-tier flow branching partitions into:
- **D10 (Layer 1, command-side dispatch):** STRUCTURALLY IDENTICAL to compliance-gating cluster Gate 1. No separate stack-rank row; MERGE-WITH-GATE-1.
- **D15 (Layer 2, skill-side per-tier workflows):** PARTITIONED:
  - **Verification-stance subset:** Absorbed by compliance-gating cluster Gate 2. MERGE-WITH-GATE-2.
  - **Pre-flight scaffolding subset (serena activate, git-clean, codebase-retrieval, memory check):** Mostly duplicated by Gate 3 (MCP availability) + D21 baseline + existing Task File Validation. Marginal unique value (~25%). DEFER as a small future row 2 extension; not a Phase 4 ADOPT.
  - **Procedural step-lists (four tier-keyed multi-step procedures inside EXECUTE):** INV-01 + INV-05 collision (`extension-point-contracts.md:89-93` reject criteria; INV-05 label). Auto-REJECT under R-RULE-05.

---

## Scored Verdict

Per-tier flow branching is scored as a **cluster with sub-verdicts** because D10 and D15 partition into already-absorbed and not-absorbable subsets.

### D10 — Command-side dispatch / flow branching (Layer 1)

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **3** | Same value as Gate 1 — task-entry tier-conditioned dispatch enables LIGHT/EXEMPT cost-skip and STRICT/STANDARD full-verification. |
| **C (Complementarity, 1–5)** | **5** | Row 1 (Task File Validation gate, C5) admits tier-aware dispatch at task entry. |
| **K (Cost, 1–5)** | **2** | Small — reads `Tier:` field (D09a) and routes execution shape. No new mechanism beyond Gate 1's. |
| **Net = (V × C) / K** | **(3 × 5) / 2 = 7.5** | |

**Verdict: ADOPT (via MERGE-WITH-GATE-1).** D10 is structurally the same feature as Gate 1 of the compliance-gating cluster (V=3, C=5, K=2, Net=7.5, ADOPT). No separate Phase 5 implementation work; the stack-rank row exists for donor-row traceability only.

### D15 — Skill-side per-tier execution workflows (Layer 2), partitioned

| Sub-feature | V | C | K | Net | Verdict |
|---|---|---|---|---|---|
| **D15a — Verification-stance subset** | 4 | 3 | 3 | 4.0 | **ADAPT (via MERGE-WITH-GATE-2)** — same surface as Gate 2 (Verification routing). |
| **D15b — Pre-flight scaffolding subset (serena activate, git-clean, codebase-retrieval, memory check)** | 2 | 5 | 3 | 3.33 | **ADAPT** — narrow unique value (~25% beyond D21 + Gate 3); attaches at row 2 with tier-gating. Phase 5 should bind to tier-gated execution only. |
| **D15c — Procedural step-lists (4 tier-keyed multi-step procedures inside EXECUTE)** | 2 | 1 | 5 | 0.4 | **REJECT** — INV-01 (`extension-point-contracts.md:89-93`) + INV-05 (`extension-point-contracts.md:17`) collision. R-RULE-05 auto-REJECT for any per-item substitution implementation. |

### Composite verdict for D10 + D15

- **D10:** ADOPT via MERGE-WITH-GATE-1 (no separate work).
- **D15a:** ADAPT via MERGE-WITH-GATE-2 (no separate work).
- **D15b:** ADAPT — small new row 2 (First Item Protocol) extension with tier-gating.
- **D15c:** REJECT — INV-01 + INV-05 collision.

**Stack-rank inputs (for T04.05):**

The cluster is rolled forward as **four separate rows in the stack rank** (one per sub-feature), with explicit MERGE-WITH annotations for the absorbed pieces:

- **D10 / Layer 1 dispatch:** V=3, C=5, K=2, Net=7.5, **ADOPT (MERGE-WITH-GATE-1 of compliance-gating cluster — no separate implementation).**
- **D15a / Layer 2 verification-stance:** V=4, C=3, K=3, Net=4.0, **ADAPT (MERGE-WITH-GATE-2 of compliance-gating cluster — no separate implementation).**
- **D15b / Layer 2 pre-flight scaffolding:** V=2, C=5, K=3, Net=3.33, **ADAPT** (small row 2 extension with tier-gating).
- **D15c / Layer 2 procedural step-lists:** V=2, C=1, K=5, Net=0.4, **REJECT** (INV-01 + INV-05 collision; R-RULE-05 auto-REJECT).

**Integration sketch for D15b (the only NEW Phase 5 work in this debate):**

- **Where:** Row 2 (First Item Protocol, C5; `extension-point-contracts.md:69-75`). Add tier-gated additive setup steps to run once before F1's first iteration.
- **Tier-gated steps (STRICT only):** serena activate (if available), `git status` (clean-tree check), `codebase-retrieval` of relevant code (if available), `list_memories`/`read_memory` for relevant prior context, baseline collection (carries with D21 / TFEP debate).
- **Tier-gated steps (STANDARD):** `codebase-retrieval` of relevant code, baseline collection.
- **LIGHT/EXEMPT:** no pre-flight scaffolding (zero-cost setup).
- **Shape of change:** ~15-25 lines added to `src/superclaude/skills/task/SKILL.md`'s First Item Protocol section. No F1 EXECUTE change. No invariant collision.

**Phase 5 manifest exceptions per R-RULE-07 (load-bearing commitments):**

The per-tier branching cluster's INV safety is contingent on the same commitments the compliance-gating cluster binds, plus one new one:

1. **PRE-LOOP DISPATCH (inherited from Gate 1):** Dispatch fires once at task-entry, never per-item inside F1 EXECUTE. Per-item per-tier dispatch is auto-REJECT under INV-01.
2. **`rf-qa` SUPPLEMENTED NOT REPLACED (inherited from Gate 2):** Tier-conditioned verification routing widens the existing Phase-Gate QA; `quality-engineer` is added as an *additional* verifier. Replacing `rf-qa` is auto-REJECT under INV-03.
3. **NO PER-ITEM EXECUTE SUBSTITUTION (new):** D15c's procedural step-lists do NOT enter F1 EXECUTE as item substitution. If a task needs to run "serena activate → git status → codebase-retrieval → memory check → ...", those are 5+ explicit checklist items in the task file, not a tier-keyed procedural substitution computed by the executor. Any implementation that uses a tier value to *generate* item content at execute-time is auto-REJECT under INV-05.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The INV-01 collision argument for per-item dispatch is sourced from `extension-point-contracts.md:89-93` (row 4 reject criteria) plus the INV-01 label at line 13. The INV-05 collision argument for procedural-step-list substitution is sourced from `extension-point-contracts.md:17` (INV-05 label) plus the row 4 reject criteria — "Action verbs that decide *which item* to execute next (override IDENTIFY). → INV-05, INV-01." A worked failure-mode example in `invariant-bounds.md` would strengthen the audit trail but does not change the verdicts — the row-4 reject criteria and the donor catalog's own routing of Layer 2 to row 1/row 2 are dispositive.
