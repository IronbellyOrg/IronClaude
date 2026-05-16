# Adversarial Debate — Tier Classification Model (D09)

**Task:** T04.01 — `/sc:adversarial` debates: tier classification & classification header emission
**Roadmap Item:** R-011
**Source feature characterization:** `feature-tier-classification.md` (Phase 2 / T02.01)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17` (sprint specification verbatim)
**Donor catalog tag:** D09 = ADAPTABLE (`donor-feature-catalog.md:55`) — Phase 1 forwarded the net-upgrade question: "tier model itself is the donor's most valuable contribution but needs to attach to either the tasklist generator or the per-item F1 IDENTIFY step rather than to whole-task entry."
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-NN references in this debate use the one-line sprint-spec labels carried in `extension-point-contracts.md:13-17`.

---

## Position A — Steelman for Inclusion

The tier classification model is the **root mechanism** that makes every downstream cost-routing feature work. Without a tier label, per-tier branching (D10/D15), verification routing (D16), TFEP gating (D19-D25), MCP circuit-breaker (D27), and the Critical/Trivial Path Override (D17/D18) have nothing to dispatch on. The donor catalog's own framing is unambiguous: D09 is "the donor's most valuable contribution" (`donor-feature-catalog.md:55`). The standalone value claim (`feature-tier-classification.md:81`) is concrete and quantifiable — a 4-5× token-budget reduction on heterogeneous 10-item tasklists *if and only if* the tier mix is heterogeneous.

The Phase 1 catalog already pre-resolves the architectural question: classification should attach **upstream of `/task`**, not inside it. `/task` is invoked on a *built* task file — by the time the F1 loop starts reading, the work has already been scoped and partitioned into items. Classification at that point is too late to affect upstream scoping decisions; what it can affect is per-item routing.

**Integration sketch (split by attach surface, not "drop into /task"):**

- **Primary attach (preferred):** Tier classification belongs in `task-builder` (the skill that builds the task file from a request) — `task-builder-adjacency.md` §3 identifies this as the natural producer for tier-shaped fields. The classifier runs once per task file build, populates a `Tier:` value into the task file frontmatter (Layer 1: per-task) and/or into each checklist item via a `Tier:` annotation (Layer 2: per-item). `/task` then *consumes* the field rather than computing it. The R-RULE-05 invariant (refusal of definition — `extension-point-contracts.md:17`) is preserved: `/task` reads tier from the file, not from the prompt.

- **Secondary attach (only the field, not the classifier):** Extend `/task`'s required frontmatter schema at row 13 (C5; `extension-point-contracts.md:169-175`) to recognize an optional `Tier:` field. The pre-loop validator at row 1 (C5; `extension-point-contracts.md:60-67`) accepts `Tier ∈ {STRICT, STANDARD, LIGHT, EXEMPT}` and refuses the task on invalid values. This is an additive field; no F1 change.

- **Tertiary attach (per-item):** Extend F1 EXECUTE item-type dispatch at row 4 (C3; `extension-point-contracts.md:86-94`) to read an item-level `Tier:` annotation when present, falling back to the task-level field. The dispatch reads the field; the per-tier behavior (cost gradient) is implemented separately under D10/D15 (per-tier branching) and D16 (verification routing).

**Why this might be a net upgrade over the status quo:**

`/task` today has no model of risk per item. A 10-item tasklist mixing a typo fix with a `migrations/` change runs both through the same Phase-Gate QA stance — `rf-qa` spawned with the same adversarial budget either way. Adopting tier-as-field gives the recipient the *data* it needs for downstream routing features (Gate 2 verification routing, Critical/Trivial Path Override) to deliver their cost-gradient value. Even if the *classifier* lives in `task-builder`, the *field* must live in `/task`'s schema for the consumer features to attach.

The strongest piece of this feature — the priority cascade itself (STRICT > EXEMPT > LIGHT > STANDARD with explicit precedence) — is a small, well-specified rule table (`src/superclaude/commands/task.md:71-89`). Re-encoding it as a JSON/YAML lookup in `task-builder` or as a deterministic post-validator in `/task` is mechanically straightforward; the donor has already done the design work.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**

- **The donor mechanism is text-only LLM inference, not a deterministic classifier.** `feature-tier-classification.md:75` is explicit: Critical Rule 1 forbids tool calls during classification (`src/superclaude/commands/task.md:53`); the donor relies on the LLM to *estimate* file count, *recognize* compound phrases like "fix security" as compounds, and *guess* whether a path matches `auth/`. The recipient inheriting this design inherits the same estimation risk: a 12-file refactor with the word "minor" in the prompt is classifiable as LIGHT.
- **The "homogeneous tier mix" non-value condition is real and unbounded.** `feature-tier-classification.md:86-88` admits that for a 20-task tasklist where every item maps to STANDARD (the default for `implement, add, create, update, fix, build, modify, change`), classification spends ~3-6K cumulative tokens and changes zero routing decisions. The value claim collapses entirely.
- **The five coupling burdens (`feature-tier-classification.md:92-104`) are not negotiable.** Lifecycle extension, schema extension, data-flow contract, configuration discipline, interactive-surface for low-confidence stalls — each is a real cost the recipient inherits. Position A is asking the recipient to take on five extensions to enable a feature whose value depends on the mix being heterogeneous and the LLM's estimates being accurate.
- **The classifier itself does not exist as code.** The keyword tables are inline prose in the donor's command file. The `config/tier-keywords.yaml` externalization target (`feature-tier-classification.md:73`) does not exist (D32 in catalog). Adopting the model means re-shipping the prose tables (carrying their drift cost) or authoring the missing YAML (taking on a new config-loading surface).
- **The donor catalog's own framing rejects whole-`/task` attach.** Phase 1 says explicitly the classifier "needs to attach to either the tasklist generator or the per-item F1 IDENTIFY step rather than to whole-task entry." Position A is not arguing for whole-task attach — but every "attach to task-builder" argument structurally moves the feature out of this debate's scope.

---

## Position B — Steelman for Rejection

**The Phase 1 catalog already routes D09 out of `/task` proper** (`donor-feature-catalog.md:55`): the classifier "needs to attach to either the tasklist generator or the per-item F1 IDENTIFY step." Position A's "primary attach" is in `task-builder`, not `/task`; the "secondary attach" is just *the field*, not the classifier; the "tertiary attach" reads the field, doesn't compute it. The debate question for this sprint — should `/task` absorb the tier classification model? — has a structural answer: **the classifier itself is not a `/task` feature.** What `/task` could absorb is *the consumer surface* (a `Tier:` field plus downstream routing). That is a much smaller question and is already partly answered by the compliance-gating cluster (Gate 1 — Dispatch task-entry, V=3, C=5, K=2, Net=7.5, ADOPT).

**Invariant collision risk (R-RULE-05 / INV-05):** A classifier that runs *inside* `/task` and infers tier from the task description or first item content is making a *what-to-do* decision — exactly the kind of inference INV-05 (`extension-point-contracts.md:17`) prohibits. The donor's classifier infers from prompt content; transposed to `/task`, it would infer from item text or task-file content. That is structurally identical to D03's per-item-auto-inference failure mode (`debate-persona-activation.md` §Position B), which was REJECTed under R-RULE-05. Position A's "secondary attach" (field only, validated at row 1) avoids this collision; Position A's "tertiary attach" (item-level read) also avoids it; **but neither is the donor's classifier — both are just field plumbing.** The classifier as a behavioral unit cannot enter `/task` without colliding with INV-05.

**Five coupling burdens, only two of which `/task` can absorb cleanly:**

The five burdens enumerated at `feature-tier-classification.md:92-104` partition cleanly into "field/schema work `/task` can absorb at row 1/row 13" and "classifier work that belongs upstream":

| # | Burden | Scope owner | Verdict |
|---|---|---|---|
| 1 | Pre-loop classification step inside the session lifecycle | `task-builder` (build-time) | Not `/task`'s burden |
| 2 | `Tier:` field per-item or per-task in schema | `/task` (row 13 / row 1) | Absorb — small, C5 |
| 3 | Resolution of compound-phrase / context-booster non-determinism | `task-builder` (build-time) | Not `/task`'s burden |
| 4 | Keyword-table location decision | `task-builder` (build-time) | Not `/task`'s burden |
| 5 | Confidence-threshold + low-confidence stall path | Either — but interactive stalls in F1 collide with non-interactivity | Reject for `/task`; absorb in `task-builder` if anywhere |

Only burden #2 is a `/task`-absorbable unit. Burden #5 (interactive low-confidence stall) is structurally hostile to F1 (the loop is non-interactive by design — Critical Rule 12 + INV-01). Burdens #1, #3, #4 are upstream-of-`/task` work.

**Realistic failure mode #1 (classifier inside `/task` collides with INV-05):** A contributor implements the classifier as a pre-loop step that reads the task file's `description:` field and the first checklist item, then writes a `Tier:` value back to the frontmatter. The pre-loop validator at row 1 admits "validators that … produce a user-facing diagnostic and write nothing to the task file beyond a refusal message" (`extension-point-contracts.md:60-67`) — but this implementation *writes* a derived field to the file. The validator has stepped from "is this task file well-formed?" to "what tier should this task run at?" — INV-05 fires. Row 1's reject criteria explicitly prohibit "validators that interpret items to decide *what* work to do" (`extension-point-contracts.md:65`). The classifier-in-`/task` implementation collides with the row 1 reject criteria.

**Realistic failure mode #2 (homogeneous-tier waste):** `feature-tier-classification.md:86-88` admits that for a 20-task tasklist of all-STANDARD items, the classifier costs 3-6K tokens and changes zero routing decisions. The donor's prompt model has one classification per turn; the recipient's tasklist model has one per item, multiplying waste linearly. For a 50-item tasklist mostly in the STANDARD default, classifier overhead can dwarf the savings on the 2-3 STRICT items.

**Realistic failure mode #3 (LLM estimation error):** The donor classifier's compound-phrase recognition and context-booster estimation are LLM judgment calls under Critical Rule 1's text-only constraint (`src/superclaude/commands/task.md:53`). A prompt "make a minor refactor to the auth module" matches `minor` (LIGHT, P3) and `auth` (path-based STRICT boost +0.4). The priority cascade resolves to STRICT, but the LLM's confidence calculation could go either way. On `/task`'s side, the item text is more structured (an MDTM checklist item, not a free-form prompt), but the LLM still has to read and interpret it without grepping the actual file count.

**Duplication risk (with compliance-gating cluster):** The compliance-gating cluster's Gate 1 (Dispatch — task-entry, V=3, C=5, K=2, Net=7.5, ADOPT per `debate-compliance-gating.md`) already covers the *consumer* side of D09: at task-entry, read a `Tier:` value and route the heavy verification path on/off. If Gate 1 is ADOPTed, `/task` has already gained the consumer surface; the remaining unaddressed piece is *where the tier value comes from*. That belongs to `task-builder`, not to a second `/task` feature.

**Maintenance cost:** The keyword tables are policy-as-prose (`src/superclaude/commands/task.md:72,78,83,88`). Every keyword change is an edit to a prose file shipped through `make sync-dev`. The recipient inheriting this design inherits ongoing matrix maintenance. The tier-keyword matrix is large (~40 keywords across 4 tiers) and prone to drift as new domain terms become security-sensitive.

---

## Evidence-Based Weighing

**Position A's strongest point (D09 is the root feature for downstream cost routing):** Without a tier label, every downstream tier-aware feature (Gate 1, Gate 2, Critical/Trivial Override, TFEP gating, per-tier MCP requirements) has nothing to dispatch on. The 4-5× token-budget reduction on heterogeneous tasklists is real value bound to this feature's existence.

**Position B's answer:** Accepted in part, but the *consumer side* is what enables downstream cost routing — and the consumer side (a `Tier:` field plus dispatch) is already absorbed cleanly by Gate 1 of the compliance-gating cluster (Net=7.5, ADOPT). What D09 adds *beyond* Gate 1 is the *classifier itself* — the priority cascade, keyword tables, context boosters, low-confidence stall. The classifier inside `/task` collides with INV-05 (failure mode #1); the classifier inside `task-builder` is not a `/task` feature. The downstream-cost-routing value of D09 is achievable without absorbing the classifier into `/task`.

**Position B's strongest point (the classifier is structurally not a `/task` feature; INV-05 collision on direct attach; classifier value is delivered by the Tier field + Gate 1, not by absorbing the classification logic):** Three convergent rejection lines: (1) Phase 1 catalog itself routes D09 upstream; (2) classifier-inside-`/task` collides with INV-05; (3) consumer-side value is already covered by Gate 1 of compliance-gating cluster.

**Position A's answer:** Concedes the classifier itself belongs to `task-builder`. Maintains that `/task` should still absorb the *field* (burden #2) — and that absorbing the field is a real Phase 4 disposition, not a Phase 5 trivial extension. Pushes back on the "Gate 1 already covers this" framing: Gate 1 is *dispatch on a tier value*, but the *field schema extension* that gives Gate 1 something to read is its own piece of work. Position A narrows D09's verdict from "absorb the classifier" to "ADOPT the field schema + REJECT the classifier (route to `task-builder`)" — that narrowing is the position A is actually defending.

**Unanswered point against Position A:** Position B's "homogeneous-tier waste" argument (failure mode #2) is unrefuted. For a `/task` consumer that runs tasklists generated by `task-builder` for users who mostly write standard implementation/fix work, the tier-mix heterogeneity that justifies D09's value is empirically uncertain. Position A could not produce telemetry showing the mix is heterogeneous in practice. The value claim is conditional on a tier mix the sprint has no measurement of.

**Unanswered point against Position B:** Position B's "classifier-inside-`/task` collides with INV-05" failure mode (#1) assumes the implementation writes a derived field back to the file. A read-only inference that *recommends* a tier without writing it (e.g., emits a diagnostic "this looks like STRICT — consider re-tiering") does not write to the file and does not collide with row 1's reject criteria. Position B did not address the read-only variant. This counts against Position B (mildly) — a read-only inference inside `/task` is admissible at row 1 if it doesn't mutate the task file. But this also collapses D09 to a diagnostic-only feature, which the donor catalog already anticipates as a partial-value outcome.

**Net effect:** D09 partitions into (a) the classifier (belongs to `task-builder`, not `/task`) and (b) the `Tier:` field schema extension (`/task` can absorb at row 1 / row 13, C5). Disposition (a) is not a `/task` feature — REJECT in this sprint, forward to `task-builder` work in a future sprint. Disposition (b) is real `/task` work and ADAPTs cleanly. The compliance-gating cluster's Gate 1 (ADOPT) consumes (b); without (b) being absorbed, Gate 1 has nothing to read. The two are paired.

---

## Scored Verdict

D09 is scored in **two sub-verdicts** because the feature partitions cleanly into a `/task`-absorbable sub-feature and an upstream-of-`/task` sub-feature.

### Sub-verdict 1 — `Tier:` field schema extension (`/task`-side)

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **4** | The field is *load-bearing for Gate 1* (compliance-gating, ADOPT, Net=7.5) — without it, the cluster's ADOPT verdict cannot land. Standalone value: a tier annotation is also consumable by Critical/Trivial Path Override (D17/D18, ADOPT, Net=20.0) and Gate 2 verification routing (ADAPT, Net=4.0). Multi-consumer field. |
| **C (Complementarity, 1–5)** | **5** | Native fit at row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`) — additive optional field, no F1 change. Validation attaches at row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`) as a closed-enum check (`Tier ∈ {STRICT, STANDARD, LIGHT, EXEMPT}`). Both extension points admit this directly. |
| **K (Cost, 1–5)** | **2** | Small — schema extension (one field) + enum validator (one line) + Skill-loader recognition verification. No new mechanism. |
| **Net = (V × C) / K** | **(4 × 5) / 2 = 10.0** | |

**Sub-verdict 1: ADOPT** (Net = 10.0).

### Sub-verdict 2 — Classifier (priority cascade + keyword tables + context boosters + low-confidence stall)

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **2** | Classifier *inside* `/task` is structurally narrow — pre-built task files arrive with scope already resolved; classifying at consume-time is too late to affect upstream scoping. The donor's prompt-driven classification is high-value for a prompt-driven entry point; `/task` is file-driven. The value belongs to `task-builder`, not to `/task` proper. |
| **C (Complementarity, 1–5)** | **2** | Read-only inference (diagnostic emit only) is admissible at row 1 but collapses the feature to a recommender. Write-back inference (populating the `Tier:` field from interpretation) collides with row 1 reject criteria at `extension-point-contracts.md:65` ("Validators that interpret items to decide *what* work to do") → INV-05. C-band C2 (between C1 and C3): the only admissible variant is a non-mutating recommender. |
| **K (Cost, 1–5)** | **5** | Five distinct burdens (`feature-tier-classification.md:92-104`): lifecycle extension, schema extension (already counted in sub-verdict 1), data-flow contract, configuration discipline, interactive-surface for low-confidence stall. Burden #5 (interactive stall) is hostile to F1 non-interactivity. Burdens #1, #3, #4 are upstream-of-`/task` work that the recipient would inherit if the classifier lived in `/task`. |
| **Net = (V × C) / K** | **(2 × 2) / 5 = 0.8** | |

**Sub-verdict 2: REJECT** (Net = 0.8 < 1.5; also fails R-RULE-05 invariant gate for the write-back variant via INV-05 collision at row 1).

**Phase 5 forwarded question:** The classifier *as a piece of work* belongs in `task-builder`. A future sprint scoped to `task-builder` should debate whether the priority cascade + keyword tables + context boosters should attach there. That sprint should also debate whether the low-confidence stall (burden #5) belongs at `task-builder` build-time (where interactivity is natural) or is dropped entirely.

### Composite verdict for D09

- **D09a (Tier: field schema extension):** ADOPT (Net = 10.0).
- **D09b (Classifier — priority cascade + keyword tables + context boosters):** REJECT (Net = 0.8, structural mismatch — belongs to `task-builder`).

**Stack-rank inputs (for T04.05):**
- D09a / Tier field: V=4, C=5, K=2, Net=10.0, **ADOPT**.
- D09b / Classifier: V=2, C=2, K=5, Net=0.8, **REJECT** (R-RULE-06 — structurally not a `/task` feature; Phase 1 catalog routes it to `task-builder`; INV-05 collision on write-back variant).

**Integration sketch for D09a (the ADOPT row):**

- **Where:** `/task`'s required frontmatter schema (row 13) gains an optional `Tier:` slot accepting `{STRICT, STANDARD, LIGHT, EXEMPT}`. The pre-loop validator (row 1) gains a closed-enum check on the value when present. Item-level `Tier:` annotations on individual checklist items are also recognized (row 4 dispatch reads the per-item value when present; fall back to task-level).
- **Shape of change:** ~3-5 lines added to `src/superclaude/skills/task/SKILL.md`'s frontmatter requirements section; ~5-10 lines added to the Task File Validation gate. No F1-loop change.
- **Producer side (out of scope for this sprint, but load-bearing for Gate 1 to actually fire):** `task-builder` populates the field at build-time. Until then, the field is optional and Gate 1 degrades gracefully (no tier → assume STANDARD → run the existing single-method Phase-Gate QA, no behavior change).

**Phase 5 manifest exception (R-RULE-07):** The D09a verdict is bound to the compliance-gating cluster's Gate 1 (ADOPT). If Gate 1 is *not* implemented, D09a is still admissible as inert metadata, but its value drops to 1 (no consumer) and the verdict would re-score to V=1, C=5, K=2, Net=2.5, DEFER. Phase 5 must ship Gate 1 and D09a together or ship neither.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The INV-05 collision argument for the classifier write-back variant cites `extension-point-contracts.md:65` (row 1 reject criteria — "Validators that interpret items to decide *what* work to do") plus the INV-05 label at line 17. A worked failure-mode example in `invariant-bounds.md` would strengthen the argument but does not change the verdict — D09a is ADOPT independently (Net=10.0), and D09b's REJECT lands on Net=0.8 + R-RULE-06 (structural mismatch) without needing the INV-05 argument to carry the verdict.
