# Variant 4 — ARCHITECT (Gate-Placement) — Reuse-and-Consolidation Detection

> **Lens:** Where the verdict surfaces and the *advisory-vs-blocking escalation boundary*.
> The distinctive contribution of this variant is **not** the search step itself — every
> variant has one — but the **gate mechanics**: a single confidence/overlap → severity →
> disposition ladder that makes the *same* Reuse-Miss finding **advisory at pre-stage** and
> **blocking at post-stage**, riding entirely on the §10 deviation taxonomy and the §14.5.2
> promotion gate that *already exist*. No new gate machine. The detector hooks the existing
> escalation rails.

---

## 0. Design thesis (the gate-placement argument)

The seed's core failure is not "agents don't search." It is that **a reuse miss has no
home in any existing gate**, so even when noticed it has nowhere to escalate to. Every other
variant will propose a search step and a similarity metric; the architectural question this
variant answers is: **once you have a Reuse-Miss finding with a confidence and an overlap
score, what does it *do*, and where does it bind?**

Three placement decisions drive the whole design:

1. **Pre-stage is constitutionally advisory; post-stage is constitutionally blocking.**
   This is not a tunable — it falls out of *what each surface can act on*. `/tdd` and
   `sc:reflect --mode pre` operate on an *intention* (a design / a proposed tasklist). There
   is no shipped artifact to gate; the only honest disposition is "recommend reuse before you
   build." `sc:reflect --mode post` operates on *shipped code*. A duplicate that shipped
   **despite** the pre-stage advice is, by definition, an unauthorized silent addition — which
   is exactly what §10.3 **Drift** already means, and Drift already blocks §14.5.2 promotion.
   The advisory→blocking transition is therefore **the same finding crossing the build
   boundary**, not two separate detectors.

2. **Reuse-Miss is NOT a 5th deviation class.** §10.6 already records that a 5th category was
   rejected (§17.7 Kill List). Adding `reuse-miss` as a peer of Drift/Regression would
   re-open that decision and, worse, create a *parallel* blocking path the §14.5.2 gate
   doesn't read. Instead, Reuse-Miss is a **finding modifier** that *maps onto* the existing
   4 classes by evidence — exactly the way §10.4's exit-code taxonomy maps a non-zero exit
   onto Regression *by evidence, not by assignment*. A shipped duplicate with no rationale →
   **Drift**. A shipped duplicate that re-implements a capability whose original carries a
   spec invariant the copy violates (e.g. mirrors `_inject_*` but drops the idempotency
   guard) → **Regression**. A shipped duplicate with an inline rationale that does not
   contradict any criterion → **Necessary deviation** (non-blocking, documented). This reuses
   the §10.5 precedence ladder verbatim.

3. **The blocking bar is high; the advisory bar is low.** Asymmetric cost (the same logic
   §5.3 rule 3 uses for Regression) runs *backwards* here: a false-positive *block* on a
   legitimately-distinct component will get the gate disabled, which is catastrophic, while a
   false-positive *advisory* note costs one ignored sentence. So the two dispositions get two
   *different* thresholds (§4 below), and the high bar is the one wired to promotion.

Everything else in this spec serves those three placements.

---

## 1. The escalation ladder (the centerpiece)

A Reuse-Miss candidate carries two measured scalars and one categorical:

- `overlap` ∈ [0,1] — structural/semantic similarity to the nearest prior-art symbol
  (definition in §6; composite of capability-tag match + skeleton shape + auggie rank).
- `confidence` ∈ [0,1] — the calibrated confidence that this *is* a reuse miss (distinct
  from overlap: overlap measures "how similar," confidence measures "how sure the detector
  is the similarity is meaningful and not coincidental").
- `verdict` ∈ {`reuse-by-import`, `mirror-shape`, `extract-shared`, `distinct`} — §7.

The ladder is evaluated **first-match-wins**, identically computed at pre- and post-stage;
**only the bottom rung's disposition differs by stage**:

| Rung | Predicate | Pre-stage disposition (`/tdd`, reflect `--mode pre`) | Post-stage disposition (reflect `--mode post`) |
|------|-----------|------------------------------------------------------|-----------------------------------------------|
| L0 | `verdict == distinct` OR `overlap < 0.55` | **Suppress** (no finding; logged to telemetry only) | **Suppress** (same) |
| L1 | `0.55 ≤ overlap < 0.75` OR `confidence < 0.70` | **ADVISORY note** ("near-neighbour exists; consider mirroring") | **ADVISORY note** in REPORT.md; **does NOT gate** promotion |
| L2 | `overlap ≥ 0.75` AND `0.70 ≤ confidence < 0.85` | **ADVISORY-STRONG** (reuse audit section flags it as a recommended change before build) | **Drift candidate** → counted toward §14.5.2 cond-4 only if it *also* satisfies the §10.3 Drift signals (unmapped + no rationale); else ADVISORY-STRONG |
| L3 | `overlap ≥ 0.75` AND `confidence ≥ 0.85` AND `verdict ∈ {mirror-shape, extract-shared, reuse-by-import}` | **ADVISORY-BLOCKING-PREVIEW** — recorded as a *predicted* blocking finding so the design doc warns "shipping this as-is will block promotion at reflect --mode post" | **BLOCKING** → mapped onto §10.3 **Drift** (or §10.4 Regression if an invariant of the original is violated); increments `deviation_count_by_class.drift`/`.regression`; fails §14.5.2 cond 4 |
| L4 | L3 predicate AND the deviation maps to **Regression** (copy violates a spec invariant/acceptance criterion the original satisfies) | (pre-stage cannot reach Regression — no shipped behaviour to contradict; treated as ADVISORY-BLOCKING-PREVIEW) | **BLOCKING + ESCALATE** → hooks §5.3 **rule 3** (Regression candidate → mandatory Tier-2 debate by ≥2 reviewers) |

**The advisory→blocking transition, stated precisely:**

> A Reuse-Miss finding is **advisory** whenever there is no shipped artifact to gate
> (every pre-stage finding, and every post-stage finding below L3). It becomes **blocking**
> at exactly one transition: **`--mode post` AND rung ≥ L3 AND the §10.3 Drift signal set is
> satisfied** (the duplicate is unmapped to any tasklist item and carries no inline rationale
> — i.e. it shipped *despite* the cheaper reuse path, with no recorded justification). At that
> point the finding is *not* a new gate — it is a Drift entry, and Drift already blocks
> promotion via the unmodified §14.5.2 cond 4. If the duplicate additionally contradicts an
> invariant the original guarantees, it is a Regression and additionally fires the §5.3 rule-3
> Tier-2 escalation. The gate placement is therefore **load-bearing-by-reuse**: the reuse
> detector dogfoods the very principle it enforces by reusing the Drift/Regression rails
> instead of building a parallel gate.

**Why L3 requires BOTH high overlap AND high confidence AND a non-`distinct` verdict before
blocking:** this is the high-bar guardrail. Overlap alone (two functions share a skeleton)
is not enough — coincidental skeletons exist. Confidence alone is not enough — the detector
can be confidently wrong about coincidence. And `verdict == distinct` (§7) is an absolute
veto: if the module-boundary analysis concluded there is no legitimate reuse path, the
finding is suppressed regardless of overlap. Three independent signals must agree before a
build is blocked.

---

## 2. Mandatory neighbour-search step — placement in both protocols

### 2.1 sc-reflect — extend the existing §6.1 chain (do NOT add a parallel subsystem)

The §6.1 Wave-1A evidence chain *already* runs auggie + serena per touched file/spec-module.
The neighbour search is **one new step in that chain**, scoped to *new* symbols only (OQ-4
cost control), so it adds a bounded number of auggie calls, not a per-file blow-up.

Insert as **step 7.5** of the §6.1 chain (after step 7' summarize_changes, before re-Read
gate):

```
7.5. mcp__auggie__codebase-retrieval  (NEIGHBOUR-SEARCH — FR-REUSE.1)
     Scope: for each NEW symbol in this run (UC-2: symbols added by the diff;
            UC-1: symbols the proposed tasklist says it will create),
     Query: "existing function/class that does <capability-tag of the new symbol>"
            where capability-tag = verb+object distilled from the new symbol's
            docstring/skeleton (NOT its name).
     Budget cap (OQ-4): at most ceil(min(N_new, 12)) retrieval calls per run;
            symbols beyond the cap are sampled by descending diff-hunk size and the
            rest recorded as `neighbour_search_sampled: true` with `sampled_count`.
     Output: per new symbol, the top-3 prior-art candidates with {path, line,
            auggie_rank, capability_tag}. Persisted to
            <output>/artifacts/neighbour-candidates.yaml.
     Fail-open (OQ-5): auggie unavailable → deterministic fallback =
            serena find_symbol by capability-tag tokens + ripgrep skeleton grep;
            emit degraded_components: ["neighbour-search:auggie_unavailable"];
            findings from the fallback are CAPPED at rung L2 (never blocking) because
            the weaker substrate cannot clear the L3 high bar. This is the graceful
            degrade: the mandatory step still runs, but it can only advise, never block.
```

The L3 cap on the auggie-unavailable path is itself a gate-placement decision: **a weaker
evidence substrate may not block a build.** This prevents the mandatory step from becoming a
liability when the substrate is down — it degrades to advisory, never to a hard STOP.

### 2.2 tdd — extend Phase 2, surface in Phase 5 (pre-stage = advisory by construction)

`/tdd` Phase 2 (Deep Investigation, L142) already spawns parallel subagents that "read actual
source files, trace actual architectures." The neighbour search is **one mandatory
investigation assignment** every TDD run gets, regardless of scenario:

- **Phase 2 addition (FR-REUSE.2a):** a dedicated `reuse-audit` investigation topic is
  ALWAYS enumerated by `rf-task-builder` (added to the §A.4 planned-research breakdown). Its
  subagent runs the same capability-tag → auggie/serena neighbour search as §2.1, scoped to
  *each component the TDD proposes to build*, and writes `reuse-candidates.md`.
- **Phase 5 addition (FR-REUSE.2b):** the synthesized TDD gains a mandatory
  **"## Reuse & Consolidation Audit"** section (template delta in §8.2). Because `/tdd` is
  pre-build, every finding here is **advisory** — but L3 findings are rendered with the
  explicit **ADVISORY-BLOCKING-PREVIEW** banner: *"If built as a new component, this will be
  classified Drift and block promotion at `sc:reflect --mode post`. Recommended verdict:
  `<mirror-shape|extract-shared>`."* This is the design-time warning that the post-stage gate
  exists, making the eventual block predictable rather than surprising.

---

## 3. Model-after-for-consistency check (shape divergence)

Both protocols, after the neighbour search returns a high-overlap candidate, run a
**shape-divergence sub-check** (FR-REUSE.3): when a new symbol's nearest prior art has
`overlap ≥ 0.75` but the new symbol diverges in **naming family** or **skeleton ordering**
from that neighbour, emit a `shape_divergence: true` flag on the finding.

Concrete to the ground-truth case: `_bind_specs` has `overlap ≥ 0.75` with the `_inject_*`
family but diverges in naming (`_bind_*` vs `_inject_*`) and is a *third* copy of the
read→idempotency→inject→rewrite skeleton. `shape_divergence: true` raises the recommended
verdict from `distinct` toward `mirror-shape` and is the signal that distinguishes "you wrote
something genuinely new" from "you wrote the same thing with a different coat of paint."

`shape_divergence` is an **advisory-only amplifier at pre-stage** (it strengthens the
recommendation banner) and a **rung-promotion input at post-stage** (it is one of the three
L3 signals: a shape-divergent third copy is strong evidence the reuse path was available and
ignored).

---

## 4. Consolidation heuristic — thresholds + the precise gate

**The consolidation question** (OQ-2) — "when do N local copies justify a shared component" —
is itself answered with a gate-placement, not just a count:

| Configuration | Count rule | Disposition |
|---------------|-----------|-------------|
| **2 copies in ONE module**, overlap ≥ 0.75 | N=2 in-module | **ADVISORY-STRONG** (rung L2) — e.g. roadmap's `_inject_*` ×2. Recommend `extract-shared` *within* the module. Not blocking: intra-module duplication is cheaper to consolidate later and lower-risk. |
| **2 copies ACROSS sibling pipelines**, overlap ≥ 0.75 | N=2 cross-module | **rung L3 at post-stage → BLOCKING Drift** when the 2nd copy shipped unmapped+unrationalised. Cross-pipeline divergence is the expensive, hard-to-undo case (the seed's core pain). |
| **3+ copies anywhere**, overlap ≥ 0.75 | N≥3 | **rung L3 → BLOCKING + `consolidation_required: true`** regardless of module spread. Three copies is the threshold at which `extract-shared` stops being optional. The ground-truth `_bind_specs` (3rd copy of the idiom) lands here. |

**The numeric gate, copy-pasteable:**

```
consolidation_overlap_threshold = 0.75      # below this → not a duplicate
consolidation_count_block       = 3         # N≥3 high-overlap copies → blocking at post-stage
consolidation_count_advise      = 2         # N=2 high-overlap copies → advisory (L2)
cross_module_block_at           = 2         # N=2 ACROSS modules → blocking (cross-pipeline asymmetric cost)
```

**Mapping onto §10 and §14.5 (no new gate):**

- A consolidation finding that reaches blocking is recorded as a §10.3 **Drift** entry (the
  new copy is the unmapped/unrationalised addition) → increments
  `deviation_count_by_class.drift` → fails §14.5.2 **cond 4** (`drift == 0`) → promotion
  blocked. **No change to the 9-condition gate's structure is required** — only a new *source*
  of Drift entries.
- If the new copy violates an invariant the canonical copies guarantee (e.g. drops the
  `"dedup, order-preserving, idempotent"` guarantee the `_inject_*` family carries) → §10.4
  **Regression** → fails cond 4 AND fires §5.3 rule 3 (Tier-2 debate).

---

## 5. Pre-stage vs post-stage — the structural differentiation

| Axis | Pre-stage (`/tdd`, reflect `--mode pre`) | Post-stage (reflect `--mode post`) |
|------|------------------------------------------|------------------------------------|
| **Operates on** | Intention: a proposed component / design / tasklist item | Shipped code: a diff hunk introducing a new symbol |
| **Evidence** | "A neighbour at `file:line` already does this; model after it / don't build it." | "This new symbol at `file:line` duplicates the capability at `prior:line`; classify the deviation." |
| **Max disposition** | ADVISORY-BLOCKING-**PREVIEW** (a *prediction* of a future block) | **BLOCKING** Drift/Regression that actually fails §14.5.2 |
| **Gate binding** | None — `/tdd` produces a doc, reflect `--mode pre` validates coverage; neither mutates/promotes | §14.5.2 cond 4 (Drift/Regression) + §5.3 rule 3 (Regression → Tier-2) |
| **Remedy offered** | Recommend `mirror-shape`/`extract-shared` in the design before code exists | §10.3 "Authorize-or-revert decision required"; if `--remediate`, Tier-3 task to consolidate or backfill spec |
| **False-positive cost** | One ignorable recommendation | A blocked promotion → the high bar (L3: 3 agreeing signals) applies here ONLY |

The single most important structural claim: **the pre-stage ADVISORY-BLOCKING-PREVIEW and the
post-stage BLOCKING Drift are the same finding observed on either side of the build boundary.**
Pre-stage says "this *will* block if you ship it"; post-stage says "it shipped, it's blocking
now." The detector computes one rung; the build boundary decides whether that rung's
disposition is a prediction or an enforcement.

---

## 6. False-positive guardrails (high bar to block, low bar to advise)

`overlap` is a composite, never a name match (seed C3):

```
overlap = 0.45 * capability_tag_match     # Jaccard over {verb, object, side-effect} tags
                                          #   distilled from docstring + skeleton, NOT name
        + 0.35 * skeleton_shape_match     # normalized AST/control-flow skeleton similarity
                                          #   (read→guard→mutate→write ⇒ same shape)
        + 0.20 * auggie_semantic_rank     # normalized top-candidate rank from §2.1 retrieval
```

Guardrails (gate-placement framing — the bar is *asymmetric* by disposition):

- **G1 — verb-only is `distinct`.** Two symbols sharing only a verb (`validate_x`,
  `validate_y`) score `capability_tag_match` low (no object/side-effect overlap) → `overlap`
  cannot clear 0.55 → suppressed at L0. This is the seed's explicit non-duplicate case.
- **G2 — blocking needs three independent agreements (L3):** `overlap ≥ 0.75` AND
  `confidence ≥ 0.85` AND `verdict != distinct`. No single signal can block.
- **G3 — `distinct` verdict is an absolute block-veto.** If §7's module-boundary analysis
  yields `distinct`, the finding never blocks regardless of overlap — a high skeleton overlap
  between two intentionally-separate components (e.g. two unrelated `read→write` flows) is
  suppressed when there is no legitimate reuse path.
- **G4 — auggie-down caps at L2.** The deterministic fallback (§2.1) cannot block; weaker
  evidence may only advise.
- **G5 — advisory bar is deliberately low (0.55).** Crying wolf *softly* is acceptable; the
  cost of a missed near-neighbour at design time exceeds the cost of one ignorable note.
- **G6 — `confidence` is calibrated through the existing §5.2 / `reflection-rubric.md`
  machinery** (the same calibrator that gates Tier escalation), so Reuse-Miss confidence is
  not a bespoke number — it rides the protocol's existing calibration discipline.

---

## 7. Reuse verdict vocabulary (honours NFR-PRD.7)

Four-valued, computed *after* overlap clears 0.55, by a module-boundary check (FR-REUSE.7):

| Verdict | Predicate | Ground-truth example |
|---------|-----------|----------------------|
| `reuse-by-import` | Prior art is import-reachable AND no dependency-ban (`NFR-*` docstring invariant) forbids the edge | (not available for `_bind_specs` — see below) |
| `mirror-shape` | Prior art exists but an import is **forbidden** by a verified module-boundary invariant; the cheap path is to name+structure the new symbol after it for cross-pipeline consistency | `_bind_specs` → mirror the `_inject_*` family (NFR-PRD.7 forbids prd→roadmap import) |
| `extract-shared` | N≥`consolidation_count_block` copies, OR cross-module copies that *both* sides legitimately need; promote skeleton to a boundary-neutral module both may depend on | the read→idempotency→inject→rewrite skeleton → `superclaude.cli.pipeline.*` |
| `distinct` | overlap < 0.55, OR capability tags diverge on object/side-effect, OR no legitimate reuse path exists | `validate_x` vs `validate_y` |

**NFR-PRD.7 enforcement is mechanical, not advisory:** the verdict computer reads the target
module's docstring `NFR-*: No imports from <pkg>` invariants (confirmed present in 8 prd
files) and **downgrades `reuse-by-import` → `mirror-shape`** whenever the would-be import
crosses a banned edge. A detector that ever emits `reuse-by-import` across a banned boundary
is non-conforming (seed C2). This is the architectural correctness guarantee: the gate cannot
recommend a change that violates the architecture it is protecting.

---

## 8. Concrete spec deltas (copy-pasteable)

### 8.1 sc-reflect-protocol/SKILL.md

**(D1) §6.1 chain — insert step 7.5** (after step 7' at L460, before step 6 re-Read at L458 is
renumbered; place as the new neighbour-search step):

> ```
> 7.5. mcp__auggie__codebase-retrieval  (NEIGHBOUR-SEARCH, FR-REUSE.1) — for every NEW symbol
>      (UC-2: diff-added; UC-1: tasklist-declared), query prior art by capability-tag
>      (verb+object+side-effect distilled from docstring/skeleton, NOT name). Budget cap:
>      ≤12 retrieval calls/run; overflow sampled by hunk size (`neighbour_search_sampled`).
>      Persist top-3 candidates/symbol to <output>/artifacts/neighbour-candidates.yaml.
>      Fail-open: auggie down → serena+ripgrep fallback, findings CAPPED at advisory rung L2,
>      emit degraded_components: ["neighbour-search:auggie_unavailable"]. Mandatory step;
>      never STOPs the run.
> ```

**(D2) §10 — new sub-section §10.8 "Reuse-Miss finding modifier"** (insert after §10.6
Grounding Gaps, before §10.7 Reporting):

> ### 10.8 Reuse-Miss (finding modifier, NOT a 5th class)
>
> A Reuse-Miss is a new symbol that duplicates a capability already implemented at a cited
> `file:line`, where a cheaper reuse path (`reuse-by-import` / `mirror-shape` /
> `extract-shared`) was available and not taken. **Reuse-Miss is not a deviation class** — it
> is a modifier that maps onto the existing 4 classes *by evidence* (mirroring §10.4's
> exit-code-by-evidence rule), so it consumes the §10.5 precedence and §14.5.2 gate unchanged:
>
> - Shipped duplicate, unmapped to any tasklist item, no inline rationale → **§10.3 Drift**.
> - Shipped duplicate that violates an invariant/acceptance-criterion the original guarantees
>   (e.g. drops a documented idempotency guard) → **§10.4 Regression** (precedence respected
>   by evidence).
> - Shipped duplicate with an inline rationale that contradicts no criterion → **§10.2
>   Necessary deviation** (non-blocking, documented).
>
> **Blocking bar (high — three independent agreements):** a Reuse-Miss is mapped to a blocking
> class (Drift/Regression) ONLY when `overlap ≥ 0.75` AND `confidence ≥ 0.85` AND
> `verdict != distinct` (rung L3, §reuse-ladder). Any weaker signal, or an auggie-unavailable
> fallback finding, surfaces as an **advisory** REPORT.md note that does NOT gate promotion.
> `verdict == distinct` is an absolute veto: such a finding is never recorded as a deviation.
>
> **Verdict vocabulary** (`reuse-by-import` | `mirror-shape` | `extract-shared` | `distinct`):
> the verdict computer reads target-module `NFR-*: No imports from <pkg>` docstring invariants
> and downgrades `reuse-by-import` → `mirror-shape` across any banned edge. Emitting
> `reuse-by-import` across a banned boundary is non-conforming.
>
> **Default remediation.** Drift-mapped: "Authorize-or-revert OR consolidate
> (`mirror-shape`/`extract-shared`) decision required"; if `--remediate`, Tier-3 task offers
> consolidate / backfill-spec / revert. Regression-mapped: unconditional Tier-3 offer +
> §5.3 rule-3 Tier-2 escalation.

**(D3) §5.3 rubric — new row** (insert as rule 3.5, after the Regression rule at L387):

> | 3.5 | UC-2 AND a Reuse-Miss finding at rung L3 mapped to **Drift or Regression** (§10.8) | **ESCALATE** (a shipped high-confidence cross-module/N≥3 duplicate is debated by ≥2 reviewers before the report ships — same asymmetric-cost logic as rule 3; a wrongly-blocked build is as costly as a missed regression) |

**(D4) §14.5.2 cond 4 — clarifying clause** (append to condition 4 at L1309, NO structural
change to the gate):

> *Reuse-Miss findings (§10.8) that map to Drift or Regression at rung L3 increment
> `deviation_count_by_class.drift`/`.regression` like any other deviation of that class and
> gate promotion through this unmodified condition. Advisory Reuse-Miss findings (rung ≤ L2,
> or any auggie-unavailable fallback finding) do NOT increment these counters and do NOT gate
> promotion.*

**(D5) §9.1 output contract — new UC-2 fields** (insert after `verification_skip_reason` at
L683):

> ```
> reuse_miss_findings: <int>                 # FR-REUSE: total Reuse-Miss findings surfaced
> reuse_miss_blocking: <int>                 # rung-L3 findings mapped to Drift/Regression
> reuse_miss_advisory: <int>                 # rung ≤ L2 (non-gating) findings
> reuse_candidates_path: <abs path> | null   # <output>/artifacts/neighbour-candidates.yaml
> consolidation_required: <bool>             # true when any N≥3 high-overlap cluster found
> neighbour_search_ran: <bool>
> neighbour_search_sampled: <bool>           # budget-cap overflow occurred
> neighbour_search_degraded: <bool>          # auggie-unavailable fallback used (caps at L2)
> ```

### 8.2 tdd/SKILL.md

**(D6) Phase 2 — mandatory investigation topic** (append to the Phase-2 description at L142
and to the §A.4 planned-research breakdown at L274):

> Every TDD run MUST include a mandatory **`reuse-audit`** investigation assignment (added by
> `rf-task-builder` regardless of scenario). Its subagent runs a capability-tag neighbour
> search (auggie `codebase-retrieval`, serena+ripgrep fallback) over *every component the TDD
> proposes to build*, scoped to new components only, and writes `reuse-candidates.md` with, per
> proposed component: nearest prior art `file:line`, `overlap`, recommended verdict
> (`reuse-by-import` | `mirror-shape` | `extract-shared` | `distinct`, honouring `NFR-*` import
> bans), and `shape_divergence`.

**(D7) Phase 5 — mandatory TDD section** (template delta; add to the synthesized document):

> ## Reuse & Consolidation Audit  *(mandatory — pre-build / advisory)*
>
> For each component this design proposes to build:
>
> | Proposed component | Nearest prior art (`file:line`) | overlap | Verdict | Disposition |
> |---|---|---|---|---|
> | `<name>` | `<path:line>` | `<0-1>` | `mirror-shape` \| `extract-shared` \| `reuse-by-import` \| `distinct` | ADVISORY \| ADVISORY-STRONG \| **ADVISORY-BLOCKING-PREVIEW** |
>
> **ADVISORY-BLOCKING-PREVIEW** entries carry the banner: *"Building this as a new component
> will be classified Drift (or Regression) and BLOCK promotion at `sc:reflect --mode post`.
> Recommended action before build: `<verdict>`."* This is the design-time warning that the
> post-stage gate exists — making the eventual block predictable, not surprising. Because
> `/tdd` is pre-build, ALL entries here are advisory; none block the TDD itself.
>
> Import bans (`NFR-*: No imports from <pkg>`) MUST be honoured: never recommend
> `reuse-by-import` across a banned module edge — downgrade to `mirror-shape`.

**(D8) Phase 5 cross-reference** (one sentence, ties the two protocols together):

> The recommended verdict recorded here is the same verdict `sc:reflect --mode post` will
> recompute against the shipped diff. A design that adopts the recommended `mirror-shape` /
> `extract-shared` here will clear the post-stage reuse gate; a design that ignores it and
> ships a new component will trip §10.8 Drift.

---

## 9. OQ resolutions (gate-placement answers)

- **OQ1 (metric/threshold):** composite `overlap` (§6); duplicate at ≥0.75, distinct <0.55,
  advisory band 0.55–0.75.
- **OQ2 (consolidation count):** N=2 in-module → advisory; N=2 cross-module → blocking at
  post-stage; N≥3 anywhere → blocking + `consolidation_required` (§4).
- **OQ3 (where + blocking vs advisory):** §10.8 Drift/Regression mapping + §14.5.2 cond 4
  (post) / TDD Reuse-Audit section (pre); blocking iff rung L3 AND post-stage AND Drift-signal
  set satisfied (§1, §5).
- **OQ4 (cheap-enough mandatory):** ≤12 retrieval calls/run, new-symbols-only scope, sampling
  overflow (§2.1).
- **OQ5 (auggie-down):** serena+ripgrep fallback, findings capped at advisory L2 — degrades to
  advisory, never STOPs, never blocks (§2.1, G4).
- **OQ6 (shared sub-spec):** YES — a single `refs/reuse-audit.md` (the ladder, overlap
  formula, verdict computer) referenced by BOTH SKILL.md files; this is itself an
  `extract-shared` decision and dogfoods the heuristic.

---

## 10. Summary of distinctive gate-placement choices

1. **One ladder, two dispositions by build boundary** — the *same* L0–L4 rung computation
   yields ADVISORY-BLOCKING-PREVIEW pre-build and BLOCKING Drift/Regression post-build.
2. **Reuse-Miss is a finding modifier, not a 5th class** — it maps onto existing
   Drift/Regression *by evidence* and rides the unmodified §14.5.2 gate and §5.3 rule-3
   escalation; zero new gate machinery.
3. **High bar to block (3 agreeing signals at L3), low bar to advise (0.55)** — asymmetric
   thresholds keep the gate trusted instead of disabled.
4. **Auggie-down degrades to advisory-only (L2 cap)** — a weaker substrate may never block a
   build.
5. **NFR-PRD.7 is mechanically enforced** — the verdict computer downgrades
   `reuse-by-import → mirror-shape` across banned edges, so the gate cannot recommend a change
   that violates the architecture it protects.
