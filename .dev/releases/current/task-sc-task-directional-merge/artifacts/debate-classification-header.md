# Adversarial Debate — Classification Header Emission (D08)

**Task:** T04.01 — `/sc:adversarial` debates: tier classification & classification header emission
**Roadmap Item:** R-011
**Source feature characterization:** `feature-classification-header.md` (Phase 2 / T02.01)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17`
**Donor catalog tag:** D08 = ADAPTABLE (`donor-feature-catalog.md:54`) — Phase 1 framing: "concept of a pre-loop telemetry header is portable; `/task` currently has no such header, no first-output rule, and no equivalent dispatch consumer — would attach pre-loop at the Task File Validation gate but requires inventing a parallel sentinel."
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`.

---

## Position A — Steelman for Inclusion

The classification header turns an *internal LLM decision* into a *machine-parseable artifact* — the donor's clearest small-surface contribution. Three concrete value points (`feature-classification-header.md:88-93`):

1. **Telemetry / A/B testing surface.** A single `grep` over conversation transcripts answers "what is our tier-mix?" — without re-running the classifier or asking the LLM to self-report. The five fields (`TIER, CONFIDENCE, KEYWORDS, OVERRIDE, RATIONALE`) are exactly the audit set a calibration loop needs.
2. **Dispatch contract.** The `TIER` value is the parser anchor for the two-track branch (`src/superclaude/commands/task.md:97-100`). Without the header as the contract surface, dispatch logic must carry the tier as in-memory state through to the dispatch step — which is exactly the kind of LLM-discretion failure mode the donor was trying to avoid.
3. **Audit trail.** Post-hoc "why did this task run STRICT?" becomes a transcript grep rather than an inference re-run.

**Integration sketch:**

- **Primary attach:** `/task`'s Task File Validation gate at row 1 (C5; `extension-point-contracts.md:60-67`) is the natural emission point. A "Pre-Loop Telemetry Header" sub-step, run *after* validation succeeds but *before* the F1 loop entry, emits a sentinel-bracketed block carrying the task-level `Tier:` (and optional confidence/keywords) read from the task file frontmatter. The block is text-only (no tool call); the validator's "produce a user-facing diagnostic" admit clause covers diagnostic-style text emission.
- **Sentinel choice:** `<!-- TASK:CLASSIFICATION -->` open / `<!-- /TASK:CLASSIFICATION -->` close — different from the donor's `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` namespace to avoid downstream parser confusion (the donor's parser, if it exists in some upstream tool, should still distinguish `/sc:task` emissions from `/task` emissions).
- **Granularity:** one header per task-file invocation, not per F1 iteration and not per phase. The task-level `Tier:` is the only field strictly required; CONFIDENCE/KEYWORDS/RATIONALE are populated when the upstream `task-builder` writes them, omitted otherwise (header degrades to a minimal `TIER: <value>` block).
- **Non-emission guard:** if the task file carries no `Tier:` (e.g., legacy task files), emit a header with `TIER: STANDARD` (the donor's default) and `RATIONALE: tier-defaulted-no-frontmatter-value`, so downstream parsers always have a row.

**Why this might be a net upgrade over the status quo:**

`/task` today emits no machine-parseable classification artifact. Reviewing what tier a task ran requires either (a) reading the entire conversation transcript by eye, (b) asking the user, or (c) inferring from which Phase-Gate QA stance was applied. The header is a 60-100 token write-once artifact that turns those expensive reviews into a single grep. For a team running hundreds of tasks per week, the aggregation value is real.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**

- **No downstream parser exists in the repo today** (`feature-classification-header.md:99`). `grep -r "SC:TASK-UNIFIED:CLASSIFICATION" src/` finds emission sites and worked examples; no telemetry collector, no A/B test harness, no transcript scanner. Until a parser is written, the headers are *write-only artifacts* — they cost tokens (~80-120 per emission) and add zero information beyond what the dispatch logic already reveals through its observable behavior.
- **The donor's "FIRST OUTPUT" rule cannot be honored on `/task`'s side.** `/task`'s actual first output is the Task File Validation gate's report (frontmatter check, schema check, B2 conformance — `src/superclaude/skills/task/SKILL.md:64-73`). Suppressing it to give the header first-position would lose observability; reordering would move the validation gate; weakening the "FIRST OUTPUT" rule silently breaks the donor's contract. None of these is clean (`feature-classification-header.md:107`).
- **The granularity decision is forced and lossy.** Donor emits one header per `/sc:task` turn. Recipient may have a task file with items of different effective tiers (if D17/D18 Critical/Trivial Path Override fires per-item). One header per file loses per-item granularity; one per F1 iteration changes loop output discipline; one per phase doesn't match either source's semantic (`feature-classification-header.md:109`).
- **The tier source must come from somewhere.** If the recipient does not absorb D09a (`Tier:` field schema), there is nothing to populate the header with. The header alone is *inert* — it depends on D09a being adopted.
- **The fallback emission rule is hard to design.** Donor's failsafe says "if the command layer didn't emit, the skill emits" (`src/superclaude/skills/sc-task-protocol/SKILL.md:9`). On the recipient side, the skill *is* the entry point; there is no command above it. The non-emission/fallback contract has to be re-designed from scratch.

---

## Position B — Steelman for Rejection

**R-RULE-06 (ceremony without behavioral teeth) is the load-bearing question for D08.** The donor characterization itself admits the headers have *no consumer* in the repo today (`feature-classification-header.md:99`): "The headers are emitted but no telemetry collector, A/B test harness, or transcript-scanner is checked in." A 60-120 token write-once artifact with no reader is precisely the failure mode R-RULE-06 prevents. Position A's three value claims all rest on consumers that **do not exist**:

1. **"Telemetry / A/B testing"** — there is no telemetry pipeline checked into this repo. The aggregation value is hypothetical; it requires *first* authoring a transcript scanner. Until that exists, every emitted header is dead tokens.
2. **"Dispatch contract"** — `/task`'s dispatch (Phase-Gate QA, F1 loop) does not parse the header. The dispatch is governed by the existing extension-point contract, not by a sentinel-bracketed block. The "dispatch contract" value is real on the *donor's* side because the donor's command layer emits the header and then reads its own emission; the recipient has no such read-emit cycle.
3. **"Audit trail"** — `/task` already produces an audit trail: the task file itself is the durable record (INV-04 file-as-truth). Item completion status (`- [x]`), phase findings logged in the UPDATE step (row 6, `extension-point-contracts.md`), and post-completion validation outputs are all file-resident and persist beyond the conversation transcript. The header's audit value is *transcript-only*; the existing audit trail is *file-resident* — a strictly better persistence model.

**The donor's "FIRST OUTPUT" rule is structurally incompatible with `/task`.** `/task`'s Task File Validation gate runs first (`src/superclaude/skills/task/SKILL.md:64-73`); its output is a structured validation report. Inserting a header before that report requires either:
- Moving the validation gate (touches the F5 lifecycle order, near-INV-territory)
- Reframing the header as "first output after validation" (weakens the donor's contract — Position A's own concession)
- Suppressing the validation report (loses observability — Position A's own concession)

None of these is admissible at C5; the cleanest variant (header after validation) is C3 at best and dilutes the donor's claim that the header is a positionally-deterministic parser anchor.

**Invariant collision (R-RULE-05 / INV-05) on dynamic-content variants:** Position A's "non-emission guard" suggests writing `TIER: STANDARD` with `RATIONALE: tier-defaulted-no-frontmatter-value` when the task file lacks a `Tier:` field. This is benign for the default case, but a related implementation pattern — "infer tier from the first item content and emit" — collides with INV-05 (the executor must not derive operating stance from content; the file must specify it). The header's *emission* per se is INV-safe; the *content-source* for the emission is the load-bearing question. If the source is "read frontmatter," fine; if it is "infer from item text," INV-05 fires. This collision is one design-decision away.

**Realistic failure mode #1 (write-only artifact accumulation):** A `/task` invocation emits the header. The conversation transcript captures it. The user closes the session. No tool ingests the transcript. Tokens spent: ~100. Information gained: zero. Scale this across a team of 10 developers running 50 tasks/week each: 25-50K tokens/week emitted into transcripts that are never aggregated. Position A would need to show the aggregation infrastructure *is being built* (not "could be built") for the header to clear the R-RULE-06 ceremony bar.

**Realistic failure mode #2 (granularity drift):** Position A chose "one header per task-file invocation" — but `/task` runs multi-phase tasks where the effective tier per phase may differ (e.g., a research phase that is mostly STANDARD work, then an implementation phase touching `auth/` that becomes effectively STRICT via Critical Path Override). The single per-task header silently misrepresents the phase-level routing. Per-item or per-phase headers would correct this but change the granularity in ways the donor never specified and that downstream parsers (still hypothetical) would need to be designed against.

**Realistic failure mode #3 (sentinel namespace drift):** Position A picked `<!-- TASK:CLASSIFICATION -->` to avoid donor-side parser confusion. But the donor's parser (if it exists upstream) might *expect* `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` and silently miss the recipient's emissions. The recipient could match the donor's sentinel — at the cost of polluting the donor's namespace with emissions from a different skill. There is no clean choice; both options introduce ambiguity downstream.

**Duplication with existing audit surfaces:** `/task`'s Phase Findings logging at the UPDATE step (row 6, `extension-point-contracts.md:118-129`) already produces structured, file-resident audit data per item. The header would be a *parallel*, transcript-resident audit surface. Two audit surfaces, one of which is durable and one of which is transcript-bound, is worse than one — readers must remember which to consult, and the inconsistency creates drift hazard.

**Phase 1 frame:** D11 (worked examples for D08/D09, NON-TRANSFERABLE per `donor-feature-catalog.md:57`) confirms the donor itself recognizes the header's downstream-consumer dependence: D11 is NON-TRANSFERABLE because "if D08/D09 are not adopted, these examples have no referent." The inverse also holds: if D08 is adopted without D09b (the classifier, which we REJECTed) and without a downstream parser, the header has no *generator* and no *consumer* — it is a sentinel with no contract on either side.

---

## Evidence-Based Weighing

**Position A's strongest point (machine-parseable audit surface enabling future aggregation):** A small, well-specified text artifact whose attach point is admissible (row 1, C5) and whose cost is bounded (~100 tokens per emit). Even today's no-consumer state, the artifact is forward-compatible — when a downstream parser ships, every historical task file's transcript becomes queryable.

**Position B's answer:** The "forward-compatibility" argument is exactly the R-RULE-06 trap: paying implementation mass now in expectation of a behavioral pattern shipping later. The donor's D02 (mcp-servers frontmatter, already REJECTed in `debate-mcp-declarations.md` Layer A) used the same argument and lost it. The "future consumer might exist" reasoning does not differentiate D08 from D02; both are ceremony unless a consumer is in flight. Position A did not produce evidence that a transcript scanner / telemetry collector is being built — and without that, D08 collapses to D02's R-RULE-06 REJECT shape.

**Position B's strongest point (R-RULE-06 ceremony without a consumer + existing audit surface duplication + FIRST-OUTPUT rule structurally incompatible):** Three convergent rejection lines: (1) no in-repo consumer; (2) Phase Findings logging already provides file-resident audit; (3) FIRST OUTPUT rule cannot be honored without compromising validation gate observability.

**Position A's answer:** Concedes the FIRST OUTPUT rule must weaken to "first output after validation" (C3 territory). On the consumer question: argues the header is *cheap* (one emission per task file, ~100 tokens) and the aggregation infrastructure could be a small future skill, not a major build. Acknowledges the Phase Findings logging is file-resident but argues it is *per-phase*, not *per-task* — the header would fill the per-task summary gap. Position A's answer narrows the value claim from "telemetry + dispatch + audit" to "per-task summary header" — which is much smaller.

**Unanswered point against Position A:** Position B's R-RULE-06 ceremony argument is unrefuted at its core. Position A offered "the consumer could be small" but did not produce evidence of any in-flight work to build it. Under R-RULE-06's net-upgrade test, "small future consumer that might land" is not the basis for absorbing implementation mass; the donor's own D02 was REJECTed under exactly this rule.

**Unanswered point against Position B:** Position B's "Phase Findings logging already provides audit" argument is partially true but does not cover the *per-task summary* angle Position A retreated to. Phase Findings are per-phase and per-item; a one-line "this task ran at tier X" rollup is genuinely absent. Whether that absence matters depends on whether anyone wants per-task summaries — which Position B did not contest directly. This counts against Position B (mildly): if the per-task summary use case is real, the header has some narrow value not duplicated by existing surfaces.

**Net effect:** D08 fails R-RULE-06 in its current state because the consumer that would extract value from the header does not exist. The retreat position ("per-task summary header") is genuinely narrow value not duplicated by Phase Findings, but it is also not the donor's claim — the donor's claim is a *machine-parseable telemetry surface for A/B testing the classifier*, which depends on D09b (REJECTed) and on a downstream parser (absent). Without those, what remains is a small per-task summary header with no consumer.

---

## Scored Verdict

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **2** | The donor's three value claims (telemetry, dispatch, audit) collapse: (1) telemetry needs a parser that does not exist; (2) dispatch is already governed by extension-point contracts, not by a sentinel; (3) audit is duplicated by existing Phase Findings logging at row 6. The retreat-position "per-task summary header" is genuinely narrow value (filling a per-task rollup gap) but is not the donor's claim. V=2 reflects the narrow value of the retreat position only. |
| **C (Complementarity, 1–5)** | **3** | Attaches at row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`) as a post-validation diagnostic emission — admissible if the emission is *after* the validation report (donor's FIRST OUTPUT rule is *not* preserved). C-band C3 reflects "extension surface exists but must be widened" — the widening is "validator now also emits a structured diagnostic sentinel after the report." No INV collision when source is task-file frontmatter; if source is inferred from item content, INV-05 fires (Position B failure mode addressing the implementation-decision risk). C=3 not C5 because the FIRST OUTPUT contract cannot be honored. |
| **K (Cost, 1–5)** | **3** | Four burdens (`feature-classification-header.md:107-115`): first-output discipline, granularity decision, tier-source data path, non-emission/fallback contract. Granularity decision is forced (failure mode #2). Tier-source depends on D09a being ADOPTed (which it is, per `debate-tier-classification.md`). Plus the sentinel-namespace decision (failure mode #3). |
| **Net = (V × C) / K** | **(2 × 3) / 3 = 2.0** | |

**Verdict: DEFER** (Net = 2.0 falls in DEFER band, `1.5 ≤ Net < 3`).

**Rationale for DEFER over ADAPT or REJECT:**

- **Not REJECT** — the retreat-position "per-task summary header" is genuinely narrow value not duplicated by Phase Findings; D08 has a non-zero floor.
- **Not ADAPT** — the donor's value claim requires a downstream parser that does not exist; R-RULE-06 prevents adopting implementation mass for a hypothetical future consumer.
- **DEFER is contingent on whether the transcript-parser infrastructure ships.** If a transcript scanner / telemetry collector is in flight (a separate sprint, not this one), D08 re-scores: V rises to 4, Net becomes 4.0, and the verdict flips to ADAPT. Until then, DEFER.

**Stack-rank inputs (for T04.05):**
- D08: V=2, C=3, K=3, Net=2.0, **DEFER** (R-RULE-06 contingent — adopt when a downstream parser is in flight; until then ceremony without behavioral teeth).

**Integration sketch (forward-loaded for the eventual ADAPT, not for this sprint):**

- **Where:** Row 1 (Task File Validation gate) emits a structured diagnostic sentinel after the validation report passes. Block format: `<!-- TASK:CLASSIFICATION -->\nTIER: <value>\n<!-- /TASK:CLASSIFICATION -->` at minimum; optional fields (CONFIDENCE, KEYWORDS, RATIONALE) populated when the task file's frontmatter carries them.
- **Source rule:** all values come from task-file frontmatter (no inference, no item-content reading). If `Tier:` is absent, emit `TIER: STANDARD` with `RATIONALE: tier-defaulted-no-frontmatter-value`. This commitment is load-bearing for INV-05 safety.
- **Granularity:** one header per `/task` invocation (per task file), emitted once after Task File Validation, before F1 loop entry. Not per-phase, not per-item.
- **Sentinel namespace:** `<!-- TASK:CLASSIFICATION -->` (distinct from the donor's `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`).

**Phase 5 manifest exception (R-RULE-07):** D08's DEFER verdict is contingent on a downstream parser being authored. If Phase 5 (or a downstream sprint) confirms parser work is in flight, D08 re-scores as ADAPT (V=4, C=3, K=3, Net=4.0). Phase 5 should *not* ship D08 in isolation — adopting without the parser repeats the R-RULE-06 ceremony failure mode the donor's D02 was REJECTed for.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The INV-05 collision risk for content-inferred header values cites `extension-point-contracts.md:17` and `:65` plus the row 1 reject criteria. The verdict's R-RULE-06 line (the dispositive argument) does not depend on a worked INV failure mode; it is sourced from the donor characterization's own admission of no-consumer at `feature-classification-header.md:99`.
