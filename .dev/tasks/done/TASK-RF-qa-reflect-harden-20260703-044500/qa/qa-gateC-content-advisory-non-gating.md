# QA Report — Gate C: FX1 Correctness-Gap Slot — Advisory / Non-Gating

**Topic:** FX1 no-spec correctness slot — can it auto-gate?
**Date:** 2026-07-03
**Phase:** task-qualitative (LENS: fx1-advisory-non-gating)
**Fix cycle:** N/A
**fix_authorization:** false (REPORT ONLY)
**Adversarial stance:** ASSUME the slot CAN auto-gate; prove it can or cannot; construct a counterexample.

---

## Overall Verdict: PASS

The FX1 no-spec correctness slot is **advisory (raised-for-triage) and can NEVER auto-gate.**
I traced the escalation path end-to-end across all three gate-trigger surfaces
(§5.3 tier-escalation table, `regression_present` setters, `status: partial` forcing
conditions) and all four downstream gating consumers. The correctness-gap signal
(`correctness_gap_raised`, `correctness-gaps.yaml`) is **disjoint from every one** — it is an
orphaned-by-design advisory telemetry channel with zero gating consumers. The counterexample
hunt (four distinct attack paths) failed to produce any path where the slot forces a gate.

## Five Required Non-Gating Properties (all VERIFIED)

| # | Required property | Result | Grounding evidence |
|---|-------------------|--------|--------------------|
| 1 | NEVER sets `regression_present` | PASS | reflect-reviewer.md:30, :115; deviation-taxonomy.md:162, :166 (table row → "NOT `regression_present`"). Repo-wide grep: `regression_present` is set ONLY by pytest-exit-1 taxonomy (SKILL.md:1073) and real-boot `reachability_unreachable` (SKILL.md:1087, :1160) — never by the correctness-gap. |
| 2 | NEVER enters the unconditional Tier-2 escalation path | PASS | The unconditional-escalation lever is **Regression only** (deviation-taxonomy.md:85; SKILL.md:1095, §5.3 rule 3 at SKILL.md:415). The routing table (deviation-taxonomy.md:166 vs :167) is a clean discriminator: **spec-silent → class `none (advisory)`**; **spec-anchored (documented invariant / acceptance criterion) → Regression by evidence, NOT this channel**. The advisory channel by construction never maps to Regression, so it never trips rule 3. reflect-reviewer.md:115 + deviation-taxonomy.md:162 state this explicitly. |
| 3 | NEVER increments `verification_regressions_detected` | PASS | reflect-reviewer.md:30, :115; deviation-taxonomy.md:162, :166. Grep confirms the counter is incremented only by the exit-code taxonomy and reachability_unreachable (SKILL.md:1073, :1087, :1160). |
| 4 | Stays OUT of the 4-class Adherence counts (separate section / parallel artifact) | PASS | reflect-reviewer.md:30 ("ONLY in the separate *Correctness gaps* section … NEVER in the 4-class Deviations table"); reflect-reviewer.md:101-103 ("separate from the 4-class Deviations table … NEVER feeds the Adherence counts"). Adherence summary (reflect-reviewer.md:89-93) counts only the 4 classes from the Deviations table. Artifact separateness: deviation-taxonomy.md:180 (`correctness-gaps.yaml` distinct from `deviation-ledger.yaml` and `grounding-gaps.yaml`; "the three files never share rows"). |
| 5 | Does NOT force `status: partial` (more advisory than Grounding-gaps) | PASS | reflect-reviewer.md:30, :115; deviation-taxonomy.md:162 ("does NOT force `status: partial` or `needs_human_decision` … strictly *more* advisory than the Grounding-gaps artifact above, which DOES force `status: partial`"). Grep of all ~15 `status: partial` forcing sites in SKILL.md (input_drift :223, zero-task :323, F3 :356, surface_unreached pin :425, validator :619/:1200, null-convergence :690, citations_dropped :800/:1197/:1199, grounding-gaps :1121, DEGRADE :1148) — **none** reference the correctness-gap. Distinct artifact means it cannot trip the "grounding-gaps.yaml non-empty" force at deviation-taxonomy.md:148-153. |

## Escalation-Path Trace (end-to-end)

The correctness-gap must clear **every** gating surface to be non-gating. Traced each:

**Stage 0 — Reviewer layer (reflect-reviewer.md).** The reviewer is structurally incapable of
gating: it is read-only and RETURNS findings; the orchestrator persists and decides
(reflect-reviewer.md:36, :38, :57, :67). A correctness gap is emitted to the *Correctness
gaps* section (reflect-reviewer.md:101-115), which is explicitly separate from the Deviations
table and never feeds Adherence counts. **No gate possible at the reviewer layer.**

**Stage 1 — Classification / routing (deviation-taxonomy.md `## Correctness-gap`, :156-180).**
Two-row routing table (:164-167):
- Row :166 — sibling-symbol disagreement + **spec silent** → class `none (advisory)`;
  effect = `correctness_gap_raised += 1` + write `correctness-gaps.yaml` row; explicitly
  "NOT `regression_present`; NO `status` / `needs_human_decision` change."
- Row :167 — disagreement violates a **documented invariant or acceptance criterion** →
  **Regression** by evidence, routed to the existing Regression class, **NOT this channel**.

The discriminator is deterministic on the "spec silent" predicate. A finding in the advisory
channel is by definition no-spec, so it can only be class `none (advisory)`. **The advisory
channel never produces a Regression; a spec-anchored gap is simply a normal Regression doing
its normal job — which is correct behavior, not the advisory slot gating.**

**Stage 2 — Signal → `regression_present` (SKILL.md).** `regression_present` is set at exactly
two sites: pytest-exit-1 taxonomy (SKILL.md:1073) and real-boot `reachability_unreachable`
(SKILL.md:1087, :1160). Repo-wide grep for `correctness_gap_raised` returns **one hit**
(deviation-taxonomy.md:166, the definition) and **zero consumers**. The counter is inert with
respect to `regression_present`. **No gate.**

**Stage 3 — §5.3 tier-escalation table (SKILL.md:409-421).** This is the sole tier gate. The
six ESCALATE triggers are: Regression candidate (rule 3), Reuse-Miss→Drift/Regression (3a),
`S_domains ≥ 3` (4), `S_dev_density > 0.20` (5), `C < 0.85` (6), `--strategy enterprise` (7).
**None reference `correctness_gap_raised` or `correctness-gaps.yaml`.** It is not a conjunct,
pre-filter, or trigger in any row. **No gate.**

**Stage 4 — `status: partial` forcing conditions.** Enumerated all ~15 sites via grep
(SKILL.md:187/223/323/356/425/515/527/619/690/800/896/1121/1148/1197/1199/1200). None
reference the correctness-gap. Its artifact is distinct from `grounding-gaps.yaml`
(deviation-taxonomy.md:180), so it cannot trip the grounding-gaps-non-empty force
(deviation-taxonomy.md:148-153). deviation-taxonomy.md:162 states it is *more* advisory than
grounding-gaps precisely because it does NOT force partial. **No gate.**

**Stage 5 — Downstream gating consumers (SKILL.md consumer matrix :955-968, task hook :963).**
- sc-troubleshoot Wave 6 (:961): gates on `regression_present` / `status` / `needs_human_decision`.
- sprint executor.py (:962): gates on `status` / `deviation_class == regression` / validation strength.
- sc-task-protocol hook (:963): gates on `deviation_count_by_class.regression > 0` / `needs_human_decision`.

The correctness-gap is not in `deviation-ledger.yaml` (so no `deviation_class`/`deviation_count_by_class`
entry), does not set `regression_present`, does not set `needs_human_decision`, does not change
`status`. **Every downstream consumer gates on fields the correctness-gap never touches. No gate.**

**Conclusion:** the correctness-gap signal is disjoint from all five gating surfaces plus the
reviewer layer. It is advisory / raised-for-triage by construction and **can never auto-gate.**

## Counterexample Hunt (adversarial — attempted to FORCE a gate)

| Attack path | Attempt | Blocked by |
|-------------|---------|-----------|
| A. Reviewer misclassifies a real no-spec gap as Regression | Would trip §5.3 rule 3 | Routing table (deviation-taxonomy.md:166/:167) is a deterministic spec-silent discriminator; a no-spec gap can only be `none (advisory)`. A spec-anchored gap is a genuine Regression (correct, not the slot gating). No forced gate from the advisory channel. |
| B. Orchestrator adds "non-empty consequences" to `correctness-gaps.yaml` like grounding-gaps | Would force `status: partial` | No such block exists. Unlike grounding-gaps (deviation-taxonomy.md:148-153), there is NO non-empty-consequences clause for correctness-gaps; :162 + :180 explicitly deny status/needs_human_decision changes and mandate artifact separateness. Grep confirms zero consumers. |
| C. Reviewer layer gates directly | Reviewer emits a FAIL/gate | reflect-reviewer is read-only, RETURNS only (reflect-reviewer.md:36/38/57/67). Cannot gate. |
| D. `persona_lens: no-spec-correctness` changes output routing to a gating channel | Lens forces escalation | persona_lens is free-form attention guidance, not a closed enum (reflect-reviewer.md:56); it merely *directs the pass toward* the advisory channel. Output still lands in the non-gating Correctness gaps section. No routing change to a gating surface. |

**All four attack paths failed.** No path forces a gate.

## Advisory Observations (NOT gating defects — do not affect this verdict)

These reinforce non-gating; none creates a gating path, so none is a FAIL for the
fx1-advisory-non-gating lens.

- **O-1 (reinforces PASS).** The embedded taxonomy inside `SKILL.md` (§10.4/§10.5 region,
  ~:1065-1160) does NOT carry a `## Correctness-gap` section; only the on-demand ref file
  `deviation-taxonomy.md` does (grep for `correctness_gap_raised` returns the ref file only).
  This is consistent with the named FX1 edit scope (Role + Output-Format + `persona_lens` in
  reflect-reviewer.md; `## Correctness-gap` in deviation-taxonomy.md — SKILL.md was NOT in the
  FX1 edit set per research/04 §5). From a non-gating standpoint this REINFORCES the verdict:
  the orchestrator's SKILL.md gating logic has no correctness-gap wiring to gate on. If future
  work wants the advisory counter surfaced in the return contract, that would be an additive,
  still-non-gating telemetry field — out of scope here.
- **O-2 (reinforces PASS).** `correctness_gap_raised` is an orphaned-by-design counter: one
  definition site, zero consumers repo-wide. Even an unbounded number of raised correctness
  gaps changes no gating field. This is the strongest form of the non-gating guarantee
  (belt-and-suspenders beyond the explicit "does NOT set/force" prose).
- **O-3 (minor asymmetry, non-material).** reflect-reviewer.md:115 says correctness gaps
  "MUST NOT enter the unconditional Tier-2 / **Tier-3** escalation path"; deviation-taxonomy.md:162
  names only "Tier-2." Both are consistent (Tier-3 is also Regression-triggered, :85), and the
  reviewer text is strictly stronger. Not a contradiction; no gate.

## Confidence

Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

- All 5 required non-gating properties verified with file:line + grep evidence.
- Escalation path traced through 6 layers (reviewer + 5 gating surfaces); all disjoint.
- Counterexample hunt exhausted 4 attack paths; all blocked.

## Tool engagement

Read: 4 | Grep: 4 (via Bash) | Glob: 0 | Bash: 3

- Read: research/04-fx2-fx1-briefs.md, reflect-reviewer.md, deviation-taxonomy.md, SKILL.md §5.3 slice.
- Grep (Bash): `correctness_gap_raised` / `correctness-gap` / `correctness gap` sweep; §5.3 escalation;
  `status: partial` forcing sites; `regression_present` setters.
- No web research performed (all verification is local-file-bound). Tavily-first N/A this review.

## Self-Audit

**(a) Reliance list — rf-qa (structural) PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in this spawn prompt; this is a
  standalone semantic review of a single gating property. Per Critical Rule #11 fallback,
  I performed independent verification and relied on no inherited structural PASS.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Escalation-path disjointness — verified by grepping every `regression_present` setter,
  every §5.3 escalation trigger, and every `status: partial` force in SKILL.md, then
  confirming `correctness_gap_raised` / `correctness-gaps.yaml` appear in none of them
  (Bash grep evidence above). Structural presence of the section is not enough; I verified
  the *semantic* wiring (or absence thereof) end-to-end.
- Routing-table discriminator soundness — verified deviation-taxonomy.md:166 vs :167 form a
  deterministic, mutually-exclusive spec-silent partition, so the advisory channel can never
  emit a Regression (the only unconditional-escalation class).

### Self-audit answers

1. **Independently verified claims:** 5 required properties + 6-layer escalation trace + 4
   counterexample paths — every one grounded at file:line and cross-checked with grep.
2. **Files read:** research/04-fx2-fx1-briefs.md; src/superclaude/agents/reflect-reviewer.md
   (full); src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md (full);
   src/superclaude/skills/sc-reflect-protocol/SKILL.md (§5.3 slice + targeted greps).
3. **Why trust a PASS here:** the verdict is not "I didn't see a gate" — it is a positive
   disjointness proof. I enumerated every gate-trigger surface in the pipeline and showed the
   correctness-gap signal is absent from all of them, and that its counter has zero consumers.
   A gate would require a consumer that does not exist.
4. **Web research:** none performed; verification is entirely local-file-bound.

## Recommendations

- **None blocking.** FX1 correctness slot passes the advisory / non-gating lens.
- **Optional (non-blocking, future):** if the advisory counter should be visible to operators
  in `return-contract.yaml`, add it as a read-and-ignore telemetry field (§9.4 forward-compat)
  — this stays non-gating and is out of the current FX1 scope (see O-1).

## QA Complete
