---
topic: "Design enforceable reuse-and-consolidation detection for the sc:reflect protocol (src/superclaude/skills/sc-reflect-protocol/SKILL.md) and the tdd skill (src/superclaude/skills/tdd/SKILL.md)"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
created: 2026-06-05T01:11:11+00:00
---

# Seed Brief: reuse-and-consolidation detection for sc:reflect + /tdd

## Problem Statement

Across the SuperClaude pipelines, agents repeatedly **build a brand-new
component** instead of one of the three cheaper, more consistent options:
(a) reusing an existing component verbatim, (b) calling it directly, or
(c) extracting a shared helper that both call-sites use. Neither
`sc:reflect` (in either `--mode pre` or `--mode post`) nor the `/tdd`
design phase ever flags this duplication as a problem or course-corrects.
The result is N parallel local implementations of the same capability,
divergent shapes/naming for what should be one pattern, and silent
technical-debt accumulation that no existing gate catches.

We need **enforceable detection** — a concrete, spec-level change to both
`SKILL.md` protocols that (1) makes an agent search its neighbours for
prior art before/after introducing a new component, (2) flags shape/naming
divergence from an established neighbour it should mirror, and (3) decides
when N local implementations justify a centralized shared component —
with defined thresholds, a decision rule, and a clear place where the
verdict surfaces (finding severity / a tdd "reuse audit" section /
blocking-vs-advisory gate).

## Known Context (claims to verify in Wave 2A before any design)

The driving concrete case — **to be independently verified via auggie +
Read before designing**, not taken on faith:

- `prd --spec` added a **new** `_bind_specs` / `_persist_bound_specs`
  binding in `src/superclaude/cli/prd/executor.py`.
- **Prior art #1 (sibling pipeline):**
  `src/superclaude/cli/roadmap/executor.py:678-752` already implements the
  SAME post-LLM artifact-injection pattern
  (`_inject_provenance_fields` / `_inject_pipeline_diagnostics`: read
  persisted artifact → idempotency-check → inject what the LLM cannot be
  trusted to produce → rewrite).
- **Prior art #2 (same module):** prd's OWN
  `src/superclaude/cli/prd/process.py:92-190` already has a deterministic
  file-binding mechanism (`_build_file_args` + `_PHASE_ALLOWED_REFS` +
  `_FILE_SIZE_THRESHOLD` inline-vs-`--file` cutoff) that the planned
  Phase-2 "inline-with-cap" work would reinvent.
- **The subtle constraint:** `NFR-PRD.7` forbids `prd` from importing
  `roadmap`. So "reuse" here sometimes means **mirror the shape / extract
  a shared helper**, NOT `import`. The detection logic MUST distinguish
  "you could have imported this" from "you should have mirrored this
  shape" from "this should become a shared module both depend on".

## Constraints

- **C1 — Two distinct protocol surfaces, two timings.** `/tdd` runs at
  *design time* (pre-build: catch before the duplicate is written).
  `sc:reflect --mode pre` validates a *proposed* strategy/tasklist
  (pre-build). `sc:reflect --mode post` audits *completed* work
  (post-build: catch the duplicate that already shipped). The detection
  must be specified differently for pre-stage vs post-stage.
- **C2 — Import bans are real architecture, not laziness.** A detector
  that says "just import roadmap from prd" would be WRONG (violates
  NFR-PRD.7). Reuse verdicts must respect module-boundary / dependency
  constraints and downgrade `import` to `mirror-shape` or `extract-shared`
  when an import is forbidden.
- **C3 — Must not produce false positives on legitimately-distinct
  components.** Two functions that merely share a verb ("validate",
  "load") are not duplicates. The heuristic needs a similarity signal
  strong enough to avoid crying wolf on every new function.
- **C4 — Grounded in real evidence (file:line).** A finding MUST cite the
  existing implementation as "X already does this at `file:line`" — never
  an unverified assertion. This rides on the existing auggie-first +
  freshness discipline already baked into the repo.
- **C5 — auggie-mcp is the search substrate.** The neighbour-search step
  is built on `mcp__auggie__codebase-retrieval` (free, semantic,
  whole-repo), with a deterministic fallback when auggie is unavailable.
- **C6 — Severity must map to the existing taxonomies.** `sc:reflect`
  UC-2 already has a 4-category deviation taxonomy (Authorized expansion /
  Necessary deviation / Drift / Regression). New reuse findings must slot
  into (or cleanly extend) that taxonomy, not invent a parallel one. `/tdd`
  has design-section structure the reuse audit must fit into.
- **C7 — Blocking vs advisory must be principled.** A blocking gate that
  fires on weak signal will be disabled by users; an advisory note on a
  clear duplicate will be ignored. The escalation rule (advisory →
  blocking) must be tied to a measurable confidence/overlap threshold.

## Success Criteria

- **SC1 — Concrete spec deltas.** Exact new phase/step text, gate wording,
  and finding-taxonomy entries for BOTH `sc-reflect-protocol/SKILL.md` and
  `tdd/SKILL.md` — copy-pasteable into the specs, not hand-wavy intent.
- **SC2 — A mandatory neighbour-search step** in both protocols: for each
  new system/component/function introduced, query surrounding modules +
  sibling pipelines and surface "X already does this at file:line" as a
  first-class finding/deviation.
- **SC3 — A model-after-for-consistency check** that flags when a new
  component diverges in shape/naming from an established neighbour pattern
  it should mirror (e.g. `_bind_specs` vs the `_inject_*` family).
- **SC4 — A consolidation heuristic** with concrete thresholds and a
  decision rule answering "at what count/overlap does N local
  implementations of one capability justify a centralized shared
  component", plus where the verdict surfaces (reflect finding severity /
  tdd reuse-audit section / blocking vs advisory).
- **SC5 — Pre vs post differentiation** explicitly specified: how
  pre-stage (catch before build) and post-stage (catch after build)
  detection differ in inputs, evidence, and remedy.
- **SC6 — False-positive guardrails** explicitly specified: the
  similarity/overlap signal and the "legitimately distinct" exclusion
  rule so the gate is trusted rather than disabled.
- **SC7 — Respects module boundaries:** verdict vocabulary distinguishes
  `reuse-by-import` / `mirror-shape` / `extract-shared` / `distinct`, and
  honours bans like NFR-PRD.7.

## Open Questions (to be resolved across the 5 proposals + merge)

- OQ1: What is the concrete similarity/overlap metric? (capability-tag
  match? signature shape? call-graph role? auggie semantic rank score?
  a composite?) And what numeric threshold separates "duplicate" from
  "distinct"?
- OQ2: What is the consolidation count/overlap threshold — N=2 with high
  overlap? N=3 regardless? Weighted by cross-module spread? — and is the
  rule the same for "two copies in one module" vs "copies across sibling
  pipelines"?
- OQ3: Where exactly does the verdict surface in each protocol, and what
  makes it blocking vs advisory? (e.g. pre-stage advisory in /tdd that
  becomes a blocking sc:reflect --mode post Regression if shipped anyway?)
- OQ4: How does the neighbour-search step stay cheap enough to be
  *mandatory* without ballooning every reflect/tdd run? (scoping the
  search to changed/new symbols only? a budget cap?)
- OQ5: How does the detector handle the auggie-unavailable case so the
  mandatory step degrades gracefully instead of blocking the whole run?
- OQ6: Should the two protocols share one detection sub-spec (a single
  "reuse-audit" ref both SKILL.md files point at) — which is itself a
  consolidation decision, and a nice dogfood of the very heuristic being
  designed?

## Enrichment Context (codebase, quality_tier: primary — VERIFIED)

Full artifact: `enrichment/codebase-context.md`. The concrete case is
**confirmed by direct Read + auggie**:

- **New duplicate:** `prd/executor.py` `_bind_specs` (L1196) +
  `_persist_bound_specs` (L1245, called L480) — read `parsed-request.json`
  → idempotent prepend (comment L1234: "dedup, order-preserving,
  idempotent") → rewrite. Same read→idempotency→inject→rewrite shape as
  the roadmap injectors.
- **Prior art #1:** `roadmap/executor.py:678-752` —
  `_inject_pipeline_diagnostics` (L678) + `_inject_provenance_fields`
  (L715). **Already 2 copies of the idiom in one file** → live test case
  for the consolidation threshold.
- **Prior art #2:** `prd/process.py:92-190` — `_PHASE_ALLOWED_REFS` (L95)
  + `_FILE_SIZE_THRESHOLD` (L115) + `_build_file_args` (L163) = the
  inline-vs-`--file` cutoff Phase-2 "inline-with-cap" would reinvent.
- **NFR-PRD.7 confirmed** in 8 prd module docstrings: "No imports from
  superclaude.cli.sprint or superclaude.cli.roadmap." → reuse here =
  **mirror-shape / extract-shared**, NOT import.

**Integration surfaces:** sc-reflect §6.1 (auggie+serena chain already
exists → extend it), §10 deviation taxonomy L860-966 (slot a "Reuse Miss"
finding), §5 rubric L351-420 (hook escalation), §14.5 promotion gate
L1309 (blocking-vs-advisory). auggie is ALREADY an allowed-tool in
sc-reflect (L5). tdd Phases 1-7 (L141-147) — reuse audit extends Phase 2
investigation, surfaces in Phase 5 synthesis; `/tdd` is pre-build by
nature.
