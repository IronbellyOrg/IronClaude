# Rejected Features Ledger — Phase 5 Synthesis (Terminal)

**Task:** T05.03 — Produce `transfer-manifest.md` and `rejected-features-ledger.md`
**Roadmap Item:** R-018
**Tier:** STANDARD
**Generated:** 2026-05-15
**Status:** TERMINAL — every entry below is a terminal rejection (REJECT) or a re-enabling-precondition deferral (DEFER) for the `/task` directional merge sprint. Per R-RULE-11, **no entry in this ledger may be silently re-proposed in Phase 6, Phase 7, or any downstream consumer.** Re-opening a verdict requires a new adversarial debate citing this ledger entry by ID and the specific reason the precondition is now met (or that prior rationale no longer holds).

**Companion artifact:** `transfer-manifest.md` — every ADOPT/ADAPT feature lives there, in execution order, with locked integration sketches and bound manifest exceptions.

**Inputs (1:1 referenced):**
- `stack-rank.md` (T04.05) — Primary stack rank (rows 1-27) + Catalog-derived dispositions (rows 28-42).
- `feature-dependency-matrix.md` (T05.01) — CR-1 through CR-16 conflict resolutions.
- `integration-sketches.md` (T05.02) — IS-DEFER-1 through IS-DEFER-9 precondition specs.
- `donor-feature-catalog.md` (Phase 1) — original Phase 1 NON-TRANSFERABLE / DUPLICATE-OF-EXISTING / ADAPTABLE tags.
- Per-feature debate artifacts under `TASKLIST_ROOT/artifacts/debate-*.md`.

---

## 0. Governing rules carried forward

- **R-RULE-11 (no silent re-litigation):** Every verdict below is terminal for this sprint. Re-debate may occur only in a future sprint, with explicit citation of this ledger and a fresh adversarial pass.
- **R-RULE-06 (absorb patterns, not implementation mass):** Multiple REJECTs and DEFERs below cite ceremony-without-behavioral-teeth as the rationale. Re-debate must establish a concrete in-repo consumer before re-evaluation.
- **R-RULE-05 (recipient invariants are inviolable):** Several REJECTs cite specific INV-NN collisions. Re-debate must demonstrate the proposed variant does not collide with the named invariant.
- **R-RULE-07 subjective override carry-forward:** One entry (LR-REJECT-1, D02/Layer A) was reached by R-RULE-06 override of arithmetic. The override is **re-affirmed** by the manifest's exception ME-9 — the override stands.

---

## 1. REJECT entries — terminal rationale (17 entries: 8 primary + 9 catalog-derived)

Each REJECT entry declares: **Donor ID + stack-rank row** | **Phase 4 / 1 verdict provenance** | **Terminal rationale** | **What stays out** | **Re-opening constraint**.

---

### LR-REJECT-1 — D02 / Layer A: `mcp-servers:` frontmatter advertisement

- **Donor ID:** D02 (split → Layer A only — Layer B is DEFER LR-DEFER-2).
- **Stack-rank row:** Row 13 (V=1, C=5, K=2, **arithmetic Net=2.5 → DEFER band; verdict REJECT under R-RULE-06 override**).
- **Provenance:** `debate-mcp-declarations.md`; arithmetic-vs-override flagged in `stack-rank.md:131`. Resolved in `feature-dependency-matrix.md` CR-6. **Re-affirmed in Phase 5 as `transfer-manifest.md` ME-9** (sole subjective override in this sprint).
- **Terminal rationale:** **R-RULE-06 ceremony-without-behavioral-teeth.** The donor proposes advertising an `mcp-servers:` list in skill frontmatter, but the recipient package has no in-repo consumer for the list — no loader reads it, no router consults it, no telemetry records it. Adopting the field would import donor ceremony with no behavioral effect, repeating the failure mode that R-RULE-06 exists to prevent.
- **What stays out:** The `mcp-servers:` frontmatter field, any associated declaration block in `task/SKILL.md`, and any documentation that would imply the field has runtime semantics.
- **Re-opening constraint:** A future sprint may re-debate **only if** a concrete in-repo consumer for the field exists (e.g., a loader pass that gates MCP availability, or an observability collector that records advertised MCPs). Cite `transfer-manifest.md` ME-9 + this ledger entry in the re-debate request.

---

### LR-REJECT-2 — D25: TFEP "3-strike FULL STOP" Escalation budget

- **Donor ID:** D25.
- **Stack-rank row:** Row 20 (V=2, C=2, K=3, Net=1.33 — REJECT by Net<1.5 threshold).
- **Provenance:** `debate-tfep.md`; `stack-rank.md:42`.
- **Terminal rationale:** **Duplicates the existing Phase-Gate QA fix loop.** Phase-Gate QA in `task/SKILL.md:182-211` already implements a 3-cycle adversarial fix loop (`rf-qa` adjudication, three iterations). D25's escalation budget would re-implement this semantic at a different layer, doubling the gate without adding new behavior — DUPLICATE-OF-EXISTING.
- **What stays out:** The donor's "after 3 escalations, FULL STOP" budget mechanism. TFEP escalation triggers (D22) route to `rf-qa` instead, which uses the existing 3-cycle loop (see `transfer-manifest.md` TU-7 § "Donor ceremony dropped").
- **Re-opening constraint:** A future sprint may re-debate only if Phase-Gate QA's 3-cycle loop is removed or restructured such that D25's pattern is no longer redundant.

---

### LR-REJECT-3 — D09b: Classifier (priority cascade + keyword tables)

- **Donor ID:** D09 split → D09b only (D09a `Tier:` field is ADOPTed — see `transfer-manifest.md` TU-1).
- **Stack-rank row:** Row 21 (V=2, C=2, K=5, Net=0.8 — REJECT by Net<1.5 threshold + R-RULE-06 structural mismatch).
- **Provenance:** `debate-tier-classification.md`; `stack-rank.md:43`.
- **Terminal rationale:** **R-RULE-06 structural mismatch.** D09b proposes a runtime classifier inside `/task` that ingests task content and emits a tier value via priority-cascade rules + keyword tables. This responsibility belongs upstream — at task-creation time (the `task-builder` skill), not at task-execution time (`/task`). `/task` is invoked on a file path with frontmatter already populated; building a runtime classifier inside it inverts the responsibility model and adds maintenance cost (keyword tables drift, cascades become hard to audit) for behavior that the author of the task file should declare explicitly via the `Tier:` field (D09a).
- **What stays out:** The classifier code, the keyword tables, the priority-cascade logic. **Routing note:** the *responsibility* for tier classification, if and when it becomes ambient, belongs to `task-builder` or `sc:tasklist`, not `/task`.
- **Re-opening constraint:** Cannot be re-opened **for `/task`**. A future sprint scoping `task-builder` or `sc:tasklist` may evaluate D09b's pattern there, but this is a fresh proposal in a different package — not a re-litigation of this ledger entry.

---

### LR-REJECT-4 — Compliance-gating Gate 5: Override flags

- **Donor ID:** part of the donor compliance-gating cluster ("Gate 5").
- **Stack-rank row:** Row 22 (V=1, C=2, K=3, Net=0.67 — REJECT, weakest sub-gate of the cluster).
- **Provenance:** `debate-compliance-gating.md`; `stack-rank.md:44`.
- **Terminal rationale:** **Silent-misuse failure mode.** Gate 5 proposes user-toggleable flags that bypass other gates ("force-override Gate 1", etc.). The failure mode is structural: any flag that bypasses an INV-protecting gate becomes a silent-misuse vector — agents toggle the flag, the gate is bypassed, INV is broken, no audit trail explains why. This contradicts the cluster's own safety-floor framing.
- **What stays out:** All override-flag mechanisms. The Critical/Trivial Path Override (TU-2) provides the *only* sanctioned path-override semantic and is path-glob-keyed (not flag-keyed), eliminating the silent-misuse vector.
- **Re-opening constraint:** A future sprint may re-debate only if a non-silent override mechanism is proposed (e.g., flags that are explicitly logged to Task Log AND require a justification field). Cite this ledger entry; do not re-propose user-toggleable flags as designed.

---

### LR-REJECT-5 — D03: Persona auto-activation list

- **Donor ID:** D03.
- **Stack-rank row:** Row 24 (V=2, C=1, K=4, Net=0.5 — REJECT; multiple INV violations).
- **Provenance:** `debate-persona-activation.md`; `stack-rank.md:46`. Phase 1 tag: NON-TRANSFERABLE.
- **Terminal rationale (multiple):**
  1. **R-RULE-05 INV-02 + N3 collision.** D03 proposes an auto-activation list keyed to task content (e.g., "if task mentions auth, activate `security-engineer`"). This auto-spawns sub-agents based on *content inspection*, which collides with INV-02 (loop control owned by F1, not by content-derived heuristics) and N3 (no implicit sub-agent spawning outside the explicit Spawn Protocol).
  2. **R-RULE-05 INV-05 collision.** Persona activation alters *what work is done* by injecting persona-specific behavior into the loop — INV-05 reserves work-definition for the checklist.
  3. **R-RULE-06 ceremony.** No in-repo consumer in `/task` for the persona list as data; the donor's pattern relies on a separate persona-routing layer the recipient does not have.
- **What stays out:** The persona auto-activation list, any heuristics that map task keywords to personas inside `/task`, any Spawn Protocol modification that admits implicit spawning.
- **Re-opening constraint:** Cannot be re-opened in its current shape. A future proposal that surfaces persona *suggestions* in the Task Log (informational, not auto-spawning) and routes to the explicit Spawn Protocol could be debated separately as a fresh feature — not a re-litigation of this entry.

---

### LR-REJECT-6 — D13: Auto-suggest keywords (no `/task` consumer)

- **Donor ID:** D13.
- **Stack-rank row:** Row 25 (V=1, C=1, K=2, Net=0.5 — REJECT; Phase 1 NON-TRANSFERABLE).
- **Provenance:** `debate-triggering-surface.md`; `stack-rank.md:47`. Phase 1 tag: NON-TRANSFERABLE — no `/task` consumer.
- **Terminal rationale:** **No `/task` consumer.** D13's auto-suggest keywords feed the donor's `sc-task-protocol` triggering surface, which selects between donor invocations. `/task` is Skill-invoked on an explicit file path — there is no triggering surface inside `/task` for keywords to feed. Adopting D13 would land orphan data with no consumer (R-RULE-06 ceremony).
- **What stays out:** Auto-suggest keyword tables, triggering-surface keyword maps.
- **Re-opening constraint:** A future sprint scoping a *triggering surface* for `/task` (e.g., a CLI dispatcher that decides between `/task` and other skills based on keywords) could re-debate D13 there — not in `/task`.

---

### LR-REJECT-7 — D15c: Layer 2 procedural step-lists in EXECUTE

- **Donor ID:** D15 split → D15c (D15a → TU-3 traceability; D15b → TU-4).
- **Stack-rank row:** Row 26 (V=2, C=1, K=5, Net=0.4 — REJECT; INV-01 + INV-05 collision).
- **Provenance:** `debate-per-tier-branching.md`; `stack-rank.md:48`. **Explicitly bound by `transfer-manifest.md` ME-5 (CR-13)** as auto-REJECT for any synthesis variant.
- **Terminal rationale:** **R-RULE-05 INV-01 + INV-05 collision.** D15c proposes synthesizing per-tier procedural steps *at execute-time inside F1 EXECUTE*. The synthesized steps would be runtime-generated checklist items the loop did not READ from disk — INV-01 (loop reads checklist; checklist is not generated by the loop) + INV-05 (work definition is the checklist; synthesis-at-execute redefines work mid-loop) both broken.
- **What stays out:** All execute-time procedure synthesis. TU-4 (D15b) provides the sanctioned form: tier-gated *additive pre-loop setup*, never per-item synthesis.
- **Re-opening constraint:** Cannot be re-opened. **Permanent auto-REJECT for any per-item synthesis variant** per ME-5. If a future need for tier-keyed setup arises beyond TU-4's pre-loop steps, the steps must be authored in the task file's checklist (not synthesized at runtime).

---

### LR-REJECT-8 — D06: Auto-trigger heuristics (direct `/task` attach)

- **Donor ID:** D06.
- **Stack-rank row:** Row 27 (V=1, C=1, K=4, Net=0.25 — REJECT; INV-05 collision; donor-rec REJECT).
- **Provenance:** `debate-triggering-surface.md`; `stack-rank.md:49`. Original donor recommendation: REJECT.
- **Terminal rationale:** **R-RULE-05 INV-05 collision + input-shape invariant.** D06 proposes auto-triggering `/task` from heuristics that scan user prompts (e.g., "if user says 'execute this checklist', auto-invoke `/task`"). This breaks the `/task` input-shape invariant (Skill-invoked on a specific file path, not on free-form prompts) and breaks INV-05 (work definition would be inferred from prompt shape, not from a checklist).
- **What stays out:** Auto-trigger heuristics, prompt-scanning attach mechanisms.
- **Re-opening constraint:** Cannot be re-opened in its current shape. A future *separate* feature that adds a prompt-recommendation layer (suggesting `/task <path>` to the user, not auto-invoking it) could be debated as a fresh proposal — not a re-litigation of this entry.

---

### LR-REJECT-9 (catalog row 28) — D04: Strategy axis of the orthogonal-dimensions model

- **Donor ID:** D04 (Strategy axis only; the Compliance axis is subsumed by TU-1).
- **Stack-rank row:** Catalog row 28 (Phase 1 tag: ADAPTABLE-partial; Strategy axis carry-forward = REJECT).
- **Provenance:** `donor-feature-catalog.md:50`; `stack-rank.md:59`.
- **Terminal rationale:** **No F1 analog.** D04's "Strategy" axis classifies tasks by execution strategy (e.g., "explorer" vs "fixer" vs "implementer"), assuming a strategy-routing layer the recipient does not have. F1 (the recipient's execution loop) does not branch by strategy — it iterates the checklist with a uniform action-to-tool mapping. Adopting the Strategy axis would land orphan classification data.
- **What stays out:** Strategy-axis classification, strategy-keyword mappings, strategy-routing logic. **Compliance axis is preserved** via TU-1 (D09a `Tier:` field + Gate 1 dispatch).
- **Re-opening constraint:** A future sprint authoring a strategy-routing layer in `/task` could re-debate the Strategy axis there. The current entry stays REJECT.

---

### LR-REJECT-10 (catalog row 29) — D05: Escalation philosophy ("better FP than FN")

- **Donor ID:** D05.
- **Stack-rank row:** Catalog row 29 (Phase 1 tag: NON-TRANSFERABLE).
- **Provenance:** `donor-feature-catalog.md:51`; `stack-rank.md:60`.
- **Terminal rationale:** **Philosophy statement, no attach point.** D05 is a value statement ("when in doubt, escalate; better false positive than false negative"). Recipient `task/SKILL.md` is a behavioral protocol; philosophy statements have no concrete attach surface and no observable post-condition. The *intent* of D05 is already encoded in the recipient's existing `rf-qa` 3-cycle loop and TFEP escalation triggers (TU-7).
- **What stays out:** The philosophy statement as a docblock or rule.
- **Re-opening constraint:** Cannot be re-opened — no shape to evaluate. If a future feature codifies the philosophy as a measurable policy (e.g., a specific FP/FN ratio target), that is a fresh proposal.

---

### LR-REJECT-11 (catalog row 30) — D07: Flag set (8 documented CLI flags)

- **Donor ID:** D07.
- **Stack-rank row:** Catalog row 30 (Phase 1 tag: ADAPTABLE; carry-forward = REJECT for `/task`).
- **Provenance:** `donor-feature-catalog.md:53`; `stack-rank.md:61`.
- **Terminal rationale:** **`/task` is Skill-invoked on a file path, not CLI.** D07's flag set assumes a CLI invocation surface (`--strict`, `--explain`, etc.). `/task` has no CLI surface — flag semantics belong to `task-builder` or `sc:tasklist` (which do have CLI invocation paths) if anywhere.
- **What stays out:** The flag set, flag-parsing logic, flag-documentation block.
- **Re-opening constraint:** Cannot be re-opened **for `/task`**. A future sprint scoping `task-builder` or `sc:tasklist` may evaluate D07's pattern there as a fresh proposal.

---

### LR-REJECT-12 (catalog row 31) — D11: Classification output examples (few-shot)

- **Donor ID:** D11.
- **Stack-rank row:** Catalog row 31 (Phase 1 tag: NON-TRANSFERABLE).
- **Provenance:** `donor-feature-catalog.md:57`; `stack-rank.md:62`.
- **Terminal rationale:** **Supports D08/D09 only.** D11 is a few-shot prompt block that demonstrates correct classifier output for D08 (header emission) and D09 (classifier). With D08 DEFER (LR-DEFER-5) and D09b REJECT (LR-REJECT-3), D11's consumers are absent. Adopting D11 in isolation would land few-shot ceremony with no caller.
- **What stays out:** The few-shot example block.
- **Re-opening constraint:** A future sprint that ADOPTs D08 (per LR-DEFER-5's parser-ships precondition) may re-evaluate D11 as a downstream artifact then. Until then, REJECT stands.

---

### LR-REJECT-13 (catalog row 32) — D12: Command-side Boundaries (Will/Will-Not)

- **Donor ID:** D12.
- **Stack-rank row:** Catalog row 32 (Phase 1 tag: DUPLICATE-OF-EXISTING).
- **Provenance:** `donor-feature-catalog.md:58`; `stack-rank.md:63`.
- **Terminal rationale:** **Duplicates F2 Prohibited Actions + F4 Modification Restrictions.** D12 enumerates command-side will/will-not behaviors that already live in `task/SKILL.md`'s F2 (Prohibited Actions) and F4 (Modification Restrictions) sections. Adopting D12 would either duplicate (DUPLICATE-OF-EXISTING) or, worse, drift from the canonical F2/F4 statements over time.
- **What stays out:** The D12 will/will-not block.
- **Re-opening constraint:** Cannot be re-opened — F2 + F4 are the canonical statements; D12 has no incremental value.

---

### LR-REJECT-14 (catalog row 38) — D28: Tool Coordination by phase

- **Donor ID:** D28.
- **Stack-rank row:** Catalog row 38 (Phase 1 tag: DUPLICATE-OF-EXISTING).
- **Provenance:** `donor-feature-catalog.md:79`; `stack-rank.md:69`.
- **Terminal rationale:** **Duplicates F1 EXECUTE action-to-tool mapping (`SKILL.md:89-96`) + Critical Rule 6 + Phase-Gate QA tool usage.** D28's tool-coordination matrix is already encoded across three existing recipient surfaces; importing it would create three sources of truth where one suffices.
- **What stays out:** The D28 coordination matrix.
- **Re-opening constraint:** Cannot be re-opened.

---

### LR-REJECT-15 (catalog row 39) — D29: Worked Examples (per-tier)

- **Donor ID:** D29.
- **Stack-rank row:** Catalog row 39 (Phase 1 tag: NON-TRANSFERABLE).
- **Provenance:** `donor-feature-catalog.md:80`; `stack-rank.md:70`.
- **Terminal rationale:** **Supports D09/D10/D15 only; has no independent shape.** D29's worked examples illustrate the donor's tier-keyed branching cluster (D09/D10/D15). With D09b REJECT (LR-REJECT-3), D15c REJECT (LR-REJECT-7), and D10 absorbed into TU-1 with the donor's separate command-layer dropped, the examples have no independent target to illustrate.
- **What stays out:** The worked-examples block.
- **Re-opening constraint:** Cannot be re-opened in its donor form. If TU-1 / TU-3 / TU-4 documentation needs worked examples in `/task`, those are fresh authored examples specific to the recipient's locked sketches — not a port of D29.

---

### LR-REJECT-16 (catalog row 40) — D30: Skill-side Boundaries (Will/Will-Not)

- **Donor ID:** D30.
- **Stack-rank row:** Catalog row 40 (Phase 1 tag: DUPLICATE-OF-EXISTING).
- **Provenance:** `donor-feature-catalog.md:81`; `stack-rank.md:71`.
- **Terminal rationale:** **Duplicates D12 + F2 Prohibited Actions.** Same shape as LR-REJECT-13.
- **What stays out:** The D30 will/will-not block.
- **Re-opening constraint:** Cannot be re-opened.

---

### LR-REJECT-17 (catalog row 41) — D31: Success Criteria metrics table

- **Donor ID:** D31.
- **Stack-rank row:** Catalog row 41 (Phase 1 tag: NON-TRANSFERABLE).
- **Provenance:** `donor-feature-catalog.md:82`; `stack-rank.md:72`. Resolved in `feature-dependency-matrix.md` CR-4 (precondition-partially-met not sufficient to upgrade).
- **Terminal rationale:** **Metrics measure D08/D09/D15; the measurement targets are not in scope.** D31's metrics package scores classifier accuracy (D09b — REJECTed), header emission rate (D08 — DEFERed), and tier-keyed branching (D15c — REJECTed). With the targets out, a metrics package has nothing to score. CR-4 explicitly resolved that the partial precondition match (D09a is ADOPTed) is *not* sufficient to upgrade D31; a future "measure D09a uptake" feature would be a fresh proposal.
- **What stays out:** The metrics table, metric definitions, metric collection logic.
- **Re-opening constraint:** A future telemetry feature scoped to `Tier:` field uptake is a fresh proposal — not a re-litigation of D31.

---

## 2. DEFER entries — re-enabling preconditions (9 distinct entries: 6 primary + 3 catalog-derived; row 15 = row 16 = one entry)

Each DEFER entry declares: **Donor ID + stack-rank row** | **Phase 4 / 1 verdict provenance** | **Re-enabling precondition (named)** | **What stays out** | **Re-debate trigger**.

---

### LR-DEFER-1 — Row 14: Compliance-gating cluster aggregate (cluster-as-written)

- **Stack-rank row:** Row 14 (V=4, C=3, K=5, Net=2.4 — DEFER, cluster-as-written).
- **Provenance:** `debate-compliance-gating.md`; `stack-rank.md:36`. Resolved in `feature-dependency-matrix.md` CR-1 (sub-gate verdicts win; cluster-as-written DEFER stands).
- **Re-enabling precondition:** **None — terminal DEFER.** The cluster-as-written package (donor's four-gate coordination layer with write-back contracts) is *not portable* in the recipient model. CR-1 settled this: the cluster-aggregate verdict is an audit roll-up; the operative transfers are the four sub-gate verdicts. Sub-gate dispositions: Gate 1 → ADOPT (TU-1), Gate 2 → ADAPT (TU-3), Gate 3 → DEFER (LR-DEFER-2), Gate 5 → REJECT (LR-REJECT-4).
- **What stays out:** The donor's four-gate write-back coordination ceremony, the cluster's coordination-layer envelope, any "import the cluster wholesale" approach.
- **Re-debate trigger:** A future sprint may re-propose only if a new attach surface for the coordination layer appears in `/task`. Phase 5 deems this implausible — cluster-aggregate is treated as terminal for practical purposes.

---

### LR-DEFER-2 — Rows 15 + 16: D27 / Layer B (per-tier MCP matrix) + Compliance-gating Gate 3 (MCP circuit-breaker)

- **Donor IDs:** D27 (Layer B) — same feature, two stack-rank views (Row 15 in MCP-declarations debate; Row 16 in compliance-gating cluster as Gate 3).
- **Stack-rank rows:** Row 15 (Net=2.25 DEFER) + Row 16 (Net=2.25 DEFER → ADAPT if Gate 1 ADOPTed).
- **Provenance:** `debate-mcp-declarations.md` + `debate-compliance-gating.md`; `stack-rank.md:37-38`. Resolved in `feature-dependency-matrix.md` CR-3 (Phase 4 verdict preserved despite precondition now operationally met; explicit re-debate note authorized).
- **Re-enabling precondition (now met, but verdict preserved per R-RULE-11):** **Gate 1 is now ADOPTed** (TU-1). With Gate 1 supplying the tier source, the marginal cost K drops from 4 to 3, raising arithmetic Net from 2.25 to 3.0 (ADAPT band). **CR-3 binding: Phase 5 does NOT silently upgrade.** A fresh adversarial re-debate in a future sprint may re-score with K=3 and decide ADAPT vs DEFER on its merits.
- **What stays out (this sprint):** D27/Layer B's per-tier MCP advertisement matrix; Gate 3's MCP circuit-breaker logic.
- **Re-debate trigger:** Future-sprint re-debate of D27 Layer B / Gate 3, citing this ledger entry. The re-debate must (a) score with K=3 in the rubric (not the original K=4); (b) verify that the per-tier MCP discipline pays its own cost; (c) confirm the circuit-breaker integrates with Gate 1's dispatch surface without violating ME-1 (PRE-LOOP DISPATCH ONLY).

---

### LR-DEFER-3 — Row 17: TFEP cluster aggregate (cluster-as-written)

- **Stack-rank row:** Row 17 (V=3, C=3, K=4, Net=2.25 — DEFER, cluster-as-written).
- **Provenance:** `debate-tfep.md`; `stack-rank.md:39`. Resolved in `feature-dependency-matrix.md` CR-2 (sub-feature verdicts win; cluster-as-written DEFER stands).
- **Re-enabling precondition:** **None — terminal DEFER.** Same shape as LR-DEFER-1. The cluster-as-written includes Step 5 heading-insertion (F4-violating), Step 6 resume-from-inserted-task (INV-01-violating), and D25 escalation budget (REJECT — LR-REJECT-2). The absorbable subset (D19/D20/D21/D22/D24) is operative via TU-5/TU-6/TU-7/TU-8.
- **What stays out:** The donor's full seven-step TFEP-as-designed wholesale; D23 step 5/6 mutations (separately DEFER as LR-DEFER-6); D25 escalation budget (REJECT as LR-REJECT-2).
- **Re-debate trigger:** Treated as terminal for practical purposes. If the donor's seven-step structure ever becomes individually transferable (after LR-DEFER-6 is itself re-enabled), a fresh debate would still need to revisit the cluster framing.

---

### LR-DEFER-4 — Row 18: D01: declared `allowed-tools` frontmatter

- **Donor ID:** D01.
- **Stack-rank row:** Row 18 (V=2, C=3, K=3, Net=2.0 — DEFER).
- **Provenance:** `debate-allowed-tools.md`; `stack-rank.md:40`. **Bound by `transfer-manifest.md` ME-8** (CR-16 / `stack-rank.md:246`).
- **Re-enabling precondition (two-clause; BOTH required):**
  1. **Skill loader semantics verified.** Confirm that the Skill loader (claude-code harness) honors `allowed-tools:` in skill frontmatter with **deny-by-default** semantics for `/task`'s tool namespace. Today this is unverified — adopting D01 without this check creates a ceremony-without-teeth failure (the field is declared but unenforced).
  2. **Critical Rule 6 retitled.** `task/SKILL.md` Critical Rule 6 is currently a tool-*preference* rule, not an exclusion rule. To make `allowed-tools:` semantically coherent, Rule 6 must be split: **exclusion → allowlist enforced by the loader; preference → narrative rule in SKILL.md.**
- **Outcome arithmetic:** If both clauses pass, V rises 2→3, Net = 3.0 (ADAPT band). If either clause fails, V collapses to 1, REJECT.
- **What stays out:** The `allowed-tools:` frontmatter declaration; any documentation that would imply `/task` enforces a tool allowlist today.
- **Re-debate trigger:** Future-sprint re-debate of D01 once both preconditions are verified. The re-debate should cite ME-8 and this ledger entry, attach the loader-semantics verification result, and confirm the Critical Rule 6 split has landed.

---

### LR-DEFER-5 — Row 19: D08: Classification header emission

- **Donor ID:** D08.
- **Stack-rank row:** Row 19 (V=2, C=3, K=3, Net=2.0 — DEFER).
- **Provenance:** `debate-classification-header.md`; `stack-rank.md:41`. **Bound by `transfer-manifest.md` ME-7** (CR-15 / `stack-rank.md:245`).
- **Re-enabling precondition:** **Downstream parser ships.** A transcript scanner / telemetry collector that consumes the classification header must exist and ship in a separate sprint. Examples of qualifying parsers: a CLI tool that aggregates `Tier:` distribution across tasks; an observability sink that records gate-1 dispatch outcomes; an analytics layer that uses the header to build classification-accuracy metrics. **Adopting D08 in isolation today repeats the R-RULE-06 ceremony-without-teeth failure mode that REJECTed D02/Layer A** (LR-REJECT-1).
- **Outcome arithmetic:** If precondition met, V rises 2→4, Net = 4.0 (ADAPT band).
- **What stays out:** The classification header emission block in `task/SKILL.md`.
- **Re-debate trigger:** Future-sprint re-debate of D08 once a downstream parser is in flight. Cite ME-7 and this ledger entry; attach evidence of the parser's consumer interface.

---

### LR-DEFER-6 — Row 23: D23: TFEP six-step execution flow with `/sc:forensic`

- **Donor ID:** D23.
- **Stack-rank row:** Row 23 (V=3, C=1, K=5, Net=0.6 — DEFER pending three preconditions).
- **Provenance:** `debate-tfep.md`; `stack-rank.md:45`.
- **Re-enabling precondition (three-clause; ALL required):**
  1. **`/sc:forensic` skill authored.** D23's reference to a `/sc:forensic` adjudication path requires that skill to exist as a callable target.
  2. **Step 5 redesigned (F4-safe).** Donor's Step 5 inserts a `## Failure Remediation Plan (Adjudicated)` heading into the task file — modifies task structure outside DYNAMIC CONTENT MARKER sections, violating F4 Modification Restrictions. Redesigned to use a DYNAMIC CONTENT MARKER section so the insertion is F4-safe.
  3. **Step 6 redesigned (INV-01-safe).** Donor's Step 6 has the loop resume from the inserted task, causing IDENTIFY to read items the loop did not author — violates INV-01. Redesigned to log the adjudication outcome but resume from the *next pre-existing* unchecked item.
- **What stays out:** The donor's six-step execution flow as written; any `## Failure Remediation Plan (Adjudicated)` heading insertion outside a DYNAMIC CONTENT MARKER; any resume-from-inserted-task semantic.
- **Re-debate trigger:** Future-sprint re-debate of D23 once all three preconditions are met. The re-debate must demonstrate Step 5 / Step 6 redesigns are F4 / INV-01 safe respectively and that `/sc:forensic` is callable.

---

### LR-DEFER-7 (catalog row 33) — D14: Human-readable confidence display bar

- **Donor ID:** D14.
- **Stack-rank row:** Catalog row 33 (Phase 1 tag: ADAPTABLE; carry-forward = DEFER).
- **Provenance:** `donor-feature-catalog.md:65`; `stack-rank.md:64`. Precondition narrative tightened in `feature-dependency-matrix.md` CR-5 (no verdict change; narrative reflects terminal D09b REJECT).
- **Re-enabling precondition (compound; BOTH required):**
  1. **D08 ADOPTs in a future sprint** (per LR-DEFER-5's parser-ships precondition).
  2. **A non-D09b classifier supplies the confidence number.** D09b is terminally REJECTed (LR-REJECT-3 — structurally mismatched, routed to `task-builder`), so D14's confidence input cannot come from D09b. The path forward requires a classifier source authored elsewhere (e.g., in `task-builder` if that scope expands to runtime classification, or as a separate feature that computes confidence from `Tier:` field provenance).
- **What stays out:** D14's confidence display bar.
- **Re-debate trigger:** Future-sprint re-debate of D14 once both preconditions are met. Cite this ledger entry; attach evidence of D08 ADOPT and the non-D09b classifier source.

---

### LR-DEFER-8 (catalog row 37) — D26: Feedback Collection

- **Donor ID:** D26.
- **Stack-rank row:** Catalog row 37 (Phase 1 tag: ADAPTABLE; carry-forward = DEFER).
- **Provenance:** `donor-feature-catalog.md:77`; `stack-rank.md:68`.
- **Re-enabling precondition:** **Calibration store authored.** D26's mechanism (collect classification outcomes, compare predicted vs actual, feed into a calibration-learning loop) requires a persistent store that `/task` does not currently have. A future sprint authoring this store — e.g., as a `~/.claude/cache/` schema, a YAML accumulator under the recipient package, or a remote telemetry sink — re-enables D26.
- **What stays out:** Feedback Collection mechanism, calibration-learning loop, store-write hooks.
- **Re-debate trigger:** Future-sprint re-debate of D26 once a calibration store is in scope. Cite this ledger entry.

---

### LR-DEFER-9 (catalog row 42) — D32: External configuration references

- **Donor ID:** D32.
- **Stack-rank row:** Catalog row 42 (Phase 1 tag: ADAPTABLE; carry-forward = DEFER).
- **Provenance:** `donor-feature-catalog.md:83`; `stack-rank.md:73`.
- **Re-enabling precondition:** **Tier-keyword YAML producer authored.** The donor references external YAML configuration files (`tier-keywords.yaml`, etc.) that do not exist. A future sprint scoping `task-builder` or `sc:tasklist` to *produce* these files re-enables D32 — at which point `/task` could optionally consume them. The externalization pattern itself is portable; it is premature only because no producer exists.
- **What stays out:** External-config reference declarations in the donor SKILL.md; any documentation that implies `/task` reads external YAML today.
- **Re-debate trigger:** Future-sprint re-debate of D32 once a producer is authored and shipping. Cite this ledger entry; attach evidence of the producer's output schema.

---

## 3. R-RULE-11 audit — terminality of every entry

Per R-RULE-11, no entry below may be silently re-proposed downstream. This section enumerates the verdict-preservation status:

| Entry | Verdict in this sprint | Terminality | Re-opening path |
|---|---|---|---|
| LR-REJECT-1 (D02/Layer A) | REJECT (R-RULE-06 override re-affirmed via ME-9) | Terminal unless an in-repo consumer is authored | Fresh debate citing ME-9 + this entry |
| LR-REJECT-2 (D25) | REJECT (Net<1.5; duplicates Phase-Gate QA) | Terminal unless Phase-Gate QA's 3-cycle loop is restructured | Fresh debate citing this entry |
| LR-REJECT-3 (D09b) | REJECT (R-RULE-06 structural mismatch) | Terminal **for `/task`** — responsibility routed to `task-builder` | Fresh proposal in `task-builder`, NOT a re-litigation here |
| LR-REJECT-4 (Gate 5) | REJECT (silent-misuse failure mode) | Terminal in current shape | Fresh debate of a non-silent override mechanism |
| LR-REJECT-5 (D03) | REJECT (R-RULE-05 INV-02/N3/INV-05 + R-RULE-06) | Terminal in current shape | Fresh proposal that surfaces persona suggestions informationally |
| LR-REJECT-6 (D13) | REJECT (no `/task` consumer) | Terminal **for `/task`** | Fresh debate in a sprint that authors a triggering surface |
| LR-REJECT-7 (D15c) | REJECT (R-RULE-05 INV-01 + INV-05 collision) | **Permanent auto-REJECT** per ME-5 | Cannot be re-opened |
| LR-REJECT-8 (D06) | REJECT (R-RULE-05 INV-05 + input-shape invariant) | Terminal in current shape | Fresh prompt-recommendation feature |
| LR-REJECT-9 (D04 Strategy axis) | REJECT (no F1 analog) | Terminal in current shape | Future strategy-routing layer |
| LR-REJECT-10 (D05) | REJECT (philosophy, no attach point) | Terminal — no shape | Fresh measurable-policy proposal |
| LR-REJECT-11 (D07) | REJECT (`/task` is Skill-invoked, not CLI) | Terminal **for `/task`** | Fresh proposal in `task-builder` / `sc:tasklist` |
| LR-REJECT-12 (D11) | REJECT (no consumers in scope) | Conditional on LR-DEFER-5 outcome | Re-evaluate if D08 ADOPTs |
| LR-REJECT-13 (D12) | REJECT (DUPLICATE-OF-EXISTING) | Terminal | Cannot be re-opened |
| LR-REJECT-14 (D28) | REJECT (DUPLICATE-OF-EXISTING) | Terminal | Cannot be re-opened |
| LR-REJECT-15 (D29) | REJECT (no independent shape) | Conditional on LR-DEFER-5 outcome | Fresh authored examples specific to TU-1/TU-3/TU-4 |
| LR-REJECT-16 (D30) | REJECT (DUPLICATE-OF-EXISTING) | Terminal | Cannot be re-opened |
| LR-REJECT-17 (D31) | REJECT (no measurement targets in scope) | Conditional on LR-DEFER-5 outcome | Fresh telemetry feature, not a re-litigation |
| LR-DEFER-1 (Cluster aggregate) | DEFER (cluster-as-written) | Terminal for practical purposes | Implausible re-opening |
| LR-DEFER-2 (D27 + Gate 3) | DEFER (verdict preserved despite precondition met — CR-3) | **Re-debate authorized in CR-3** | Future-sprint re-debate with K=3 |
| LR-DEFER-3 (TFEP cluster aggregate) | DEFER (cluster-as-written) | Terminal for practical purposes | Implausible re-opening |
| LR-DEFER-4 (D01) | DEFER (two-clause precondition; ME-8) | Re-enabling possible with both clauses | Future-sprint re-debate citing ME-8 |
| LR-DEFER-5 (D08) | DEFER (parser-ships; ME-7) | Re-enabling possible with parser | Future-sprint re-debate citing ME-7 |
| LR-DEFER-6 (D23) | DEFER (three-clause precondition) | Re-enabling possible with all three clauses | Future-sprint re-debate |
| LR-DEFER-7 (D14) | DEFER (compound: D08 ADOPT + non-D09b classifier) | Re-enabling possible | Future-sprint re-debate |
| LR-DEFER-8 (D26) | DEFER (calibration store) | Re-enabling possible | Future-sprint re-debate |
| LR-DEFER-9 (D32) | DEFER (tier-keyword YAML producer) | Re-enabling possible | Future-sprint re-debate |

**Verdict-preservation count:** 26 entries — every one preserves its Phase 4 / Phase 1 verdict. Zero silent re-litigations. One explicit re-debate authorization (LR-DEFER-2 / CR-3).

---

## 4. Coverage Audit — 1:1 partition with the donor catalog

This ledger covers 27 stack-rank rows (counting Row 15 + Row 16 as one feature with two views). The companion `transfer-manifest.md` covers the remaining 15 stack-rank rows. Together: 27 + 15 = 42 stack-rank rows = all 32 donor catalog rows accounted exactly once.

**REJECT entries (17):** Rows 13, 20, 21, 22, 24, 25, 26, 27 (primary; 8) + Rows 28, 29, 30, 31, 32, 38, 39, 40, 41 (catalog-derived; 9).

**DEFER entries (9 distinct; 10 stack-rank views counting Row 15 + Row 16):** Rows 14, 15+16, 17, 18, 19, 23 (primary; 6 distinct = 7 stack-rank views) + Rows 33, 37, 42 (catalog-derived; 3).

**1:1 partition confirmed.** No donor catalog row D01-D32 is missing from the union of {`transfer-manifest.md`, this file}; no row appears in both.

---

## 5. Acceptance Criteria Recap (T05.03)

This ledger satisfies the T05.03 acceptance criteria for `rejected-features-ledger.md`:

1. **`rejected-features-ledger.md` exists, lists every REJECT (terminal rationale) and DEFER (precondition) feature.** ✅ — 17 REJECT entries (LR-REJECT-1 through LR-REJECT-17), each with named terminal rationale and "what stays out" enumeration; 9 DEFER entries (LR-DEFER-1 through LR-DEFER-9), each with named re-enabling precondition and re-debate trigger.

2. **Every Phase 4 donor feature appears in exactly one of the two documents — no orphans, no duplicates.** ✅ — Section 4 coverage audit confirms the 27 ledger entries (covering Rows 13-32 + 33 + 37 + 38-42, with Row 15 = Row 16) + 15 manifest entries = 42 stack-rank rows = all 32 donor catalog rows exactly once.

3. **The ledger is terminal — Phase 6/7 may not silently re-propose its entries (R-RULE-11).** ✅ — Section 3's R-RULE-11 audit table enumerates each entry's terminality and explicit re-opening path. Zero silent re-litigations permitted; one explicit re-debate authorization (LR-DEFER-2) carries CR-3's narrative verbatim.

---

**T05.03 deliverable: COMPLETE (ledger half).** Phase 6 (merge plan) and Phase 7 (merge execution) consume this ledger as the binding terminal record of every REJECTed and DEFERed donor feature. The companion `transfer-manifest.md` is the binding affirmative record. Together, the two artifacts partition the Phase 4 verdict set 1:1 with the donor catalog.
