# spec-panel critique — 04-spec-low-complexity.md

- **Mode**: critique · **Format**: detailed · **Iterations**: 1
- **Focus**: requirements, architecture, correctness
- **Panel**: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Nygard, Fowler, Adzic, Crispin, Whittaker (correctness)
- **Review date**: 2026-06-02

## Findings summary

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| MAJOR | 10 |
| MINOR | 5 |

---

## === REQUIREMENTS ANALYSIS ===

### R1 — Open-Items numbering gap + incomplete downstream list (MAJOR · Wiegers · High)

**Issue**: §11 Open Items enumerates OQ-1, OQ-3, OQ-4, OQ-5, OQ-6, OQ-7 — **OQ-2 does not exist**. Separately, §10 "For sc:tasklist" tells task-builder to create runtime-probe items for "OQ-1, OQ-3, OQ-4, OQ-5" but omits OQ-6 and OQ-7, which are also unresolved.
**Recommendation**: Either renumber OQ-3…OQ-7 → OQ-2…OQ-6, or add an explicit OQ-2. Make the §10 list match the full set of probe-gated items (add OQ-6, OQ-7 or state why they are excluded). Traceability between the open-item registry and its downstream consumer must be complete.
**Quality impact**: completeness +0.4, consistency +0.3.

### R2 — NFR-RV3-LOW.3 token budget is not measurable as written (MAJOR · Wiegers · High)

**Issue**: Target = "≤ +15% of T1 band midpoint (6 turns)" (a *turn* count), Measurement = "orchestration-token delta … assert within band" (a *token* count). The unit of the target (turns) ≠ the unit of measurement (tokens); 15% of 6 turns = 0.9 turns, which is not a token threshold. The baseline ("before") is also undefined — before which adoption? aggregate or per-feature?
**Recommendation**: State the target in tokens (e.g., "≤ +1,000 Claude-orchestration tokens aggregate over the T1 path, baseline = current main on the FR-1 eval fixture") with a named baseline artifact. Keep one unit end-to-end.
**Quality impact**: testability +0.6.

### R3 — Frontmatter quality_scores asserted without basis (MINOR · Wiegers · Low)

**Issue**: `quality_scores` (clarity 8.5, completeness 8.0, …) are self-assigned pre-review with no rubric trace.
**Recommendation**: Acceptable as a draft self-estimate, but annotate "draft self-estimate; authoritative scores set post-spec-panel" or lower until this review's findings are resolved.

### R4 — FR-4 trigger predicate undefined (MAJOR · Adzic · High)

**Issue**: FR-4 fires "when the tasklist OR spec cites a third-party API by name". There is no concrete, example-able definition of "cites a third-party API by name." Is it any backtick-quoted identifier? A dependency named in `pyproject.toml`? An import? Without a detection rule, FR-4.1 ("`search_deps_invocations ≥ 1`") cannot be deterministically validated — the eval case cannot construct a guaranteed-positive input.
**Recommendation**: Add a Given/When/Then-style detection definition, e.g. "WHEN a spec/tasklist line contains a symbol whose `find_declaration` resolves to an `<ext:…>` path, THEN that symbol is a third-party-API citation." Tie FR-4.1's `≥1` assertion to that operationalised predicate.
**Quality impact**: testability +0.5, clarity +0.3.

### R5 — FR-5 "same MCP session" not operationalised for the harness (MINOR · Adzic · Medium)

**Issue**: FR-5.1 requires invocation "within the same MCP session as the edits" and FR-5.4 distinguishes a "fresh session". The eval harness has no stated mechanism to *establish* or *assert* session identity, so neither the positive (5.1) nor the negative (5.4) case is reproducibly constructible.
**Recommendation**: Specify how the eval case pins/forces session boundary (or mark FR-5 acceptance as "pilot-only, manual" consistent with its deferred status and OQ-3).

### R6 — FR identifier scheme is inconsistent (MINOR · Cockburn · Low)

**Issue**: Headings use `FR-RV3-LOW.N`; acceptance criteria use `FR-N.M` (e.g. "FR-1.1"). Two identifier schemes for the same requirements harms traceability for downstream task-builder ID mapping.
**Recommendation**: Use one scheme. Recommend `FR-RV3-LOW.N.M` for criteria, or declare "FR-N.M ≡ FR-RV3-LOW.N criterion M" once explicitly.

---

## === ARCHITECTURE ANALYSIS ===

### A1 — §4.6 Implementation Order contradicts §9 Rollout ordering (MAJOR · Fowler · High)

**Issue**: §4.6 places **FR-6 at step 2** (early, parallel with FR-1+2). §9 places **FR-6 at Phase 5** (late). Two authoritative ordering tables disagree on when FR-6 ships. Downstream sc:roadmap/sc:tasklist will pick one and silently diverge from the other.
**Recommendation**: Make §4.6 and §9 consistent. Given FR-6 depends only on FR-7's version signal, either is defensible — choose one and propagate.
**Quality impact**: consistency +0.6.

### A2 — FR-7 scheduled in two rollout phases (MAJOR · Fowler · High)

**Issue**: §9 lists FR-7 in **Phase 1** ("FR-7 `get_current_config` first") *and* **Phase 5** ("FR-6 + FR-7 Wave-0 calibration finalization"). A feature cannot ship in two phases; the Phase-5 reference is either a duplicate or an undocumented split.
**Recommendation**: Phase 5 should reference FR-6 only (FR-7 already shipped Phase 1), or explicitly scope what FR-7 sub-work remains for Phase 5 (e.g., "FR-7 telemetry-field finalization").

### A3 — contract_version 1.1.0 rationale omits FR-6/FR-7 fields (MAJOR · Newman · High)

**Issue**: §5 and §4.5 state the minor bump "bundles FR-1/2/4/8". But §4.5's own data model adds `onboarding_status` (FR-6) and `serena_config_snapshot_path` / `serena_active_context` / `serena_active_modes` (FR-7) to the §9.2 contract block. The version-bump rationale undercounts the additive fields, and the "additive only → 1.0.x consumers tolerate" backward-compat claim is asserted over an incomplete field set.
**Recommendation**: List all six FRs that add contract fields (1/2/4/6/7/8) under the 1.1.0 bump, or justify why FR-6/7 telemetry fields are exempt from the contract version (e.g., "§9.2 telemetry is non-contractual"). If telemetry-vs-contract is the distinction, state it explicitly.

### A4 — FR-7.4 version field underspecified yet load-bearing (MAJOR · Nygard · High)

**Issue**: FR-7.4 exposes the Serena version "(a derivable `serena_version` field **or equivalent**)". This field gates FR-6 and FR-8 (both v1.5-sensitive). A load-bearing interface contract specified as "or equivalent" leaves the gating key's name and shape open — compounded by OQ-4 (the entire `get_current_config` return shape is "not surfaced"). Two downstream FRs branch on a field that may not exist in the parsed output.
**Recommendation**: Define `serena_version` as a required derived field with an explicit fallback value when it cannot be parsed (e.g., `serena_version: unknown`), and make FR-6/FR-8 gates branch on the three-valued `{<v1.5, ≥v1.5, unknown}` domain (see C2).

### A5 — §4.1 conflates runtime artifacts with committed source (MINOR · Fowler · Low)

**Issue**: §4.1 "New Files" lists `<output>/serena-config-snapshot.yaml` and `<output>/serena-change-summary.md` (per-run artifacts) alongside committed eval-case dirs. The note acknowledges this, but mixing the two in one "New Files" table is structurally muddy.
**Recommendation**: Split into "New committed files" vs "New per-run artifacts," or move the `<output>/…` rows into §5/§4.5 where contract artifacts live.

---

## === CORRECTNESS ANALYSIS ===

*Mandatory artifacts for `--focus correctness` follow the findings.*

### C1 — Memory-retention invariant is unprovable under read-only accumulation (CRITICAL · Whittaker + Fowler, Pipeline Dimensional Analysis · High)

**Attack (FR-2.5 Accumulation + Pipeline dimensional mismatch)**: I can break this specification by an **Accumulation Attack** on the FR-8 retention pipeline. The invariant at **FR-8 / §6.3 "keep last 20 entries per key"** fails when read-only memories dominate the slug-prefixed set.

**Concrete attack with count trace**:
```
[list_memories: N=40 total]
   → filter slug-prefix "reflect/last-pass-{slug}/": M=25 items
       of which 24 match read_only_memory_patterns
   → sort by recency
   → delete oldest while count>20:  deletable = M − readonly = 25 − 24 = 1
   → after sweep: 24 (readonly, skipped) + 0 = 24 items remain  ❰ INVARIANT VIOLATED ❱
```
FR-8.5 *counts* skipped read-only memories (`memory_retention_skipped_readonly`) but never defines behavior when the skip makes the "≤20" target unreachable. The downstream operational-hygiene guarantee in §1 problem statement ("prevents unbounded memory growth") assumes the count is always reducible to 20 — a count-conservation assumption the pipeline violates. Per Pipeline Dimensional Analysis (FR-19), an unhandled count divergence is CRITICAL.

**Recommendation**: Add an explicit branch: when `(M − readonly) > 20` after the sweep, emit `memory_retention_unbounded: true` + a WARN to audit, and define the intended posture (accept-and-warn, or escalate). State that read-only memories are excluded from the "last 20" budget so the invariant becomes "keep last 20 *deletable* entries" — which is provable.

### C2 — FR-8.4 v1.5 gate does not cover "version unknown" (MAJOR · Nygard, guard completeness · High)

**Attack (FR-2.1 Zero/Empty)**: FR-7's fail-open path (line 257) yields `degraded: ["get_current_config"]` and *skips the snapshot* — so `serena_version` is unknown. FR-8.4's guard is "**on a Serena fingerprint < v1.5**". The value `unknown` is in neither `{<v1.5}` nor `{≥v1.5}`. The guard is incomplete: when the config probe fails, FR-8's rename behavior is undefined.
**Recommendation**: Make the gate three-valued. Treat `unknown` as `<v1.5` (conservative: write-only-no-retention, no rename-propagation). State this explicitly in FR-8.4 and FR-7's fail-open clause.

### C3 — FR-1 kind-guard misses traits misreported as Class (MAJOR · Whittaker, Divergence/Sentinel · High)

**Attack (FR-2.2 Divergence)**: The matrix research the spec is built on (01-matrix:69) documents that "non-Python languages may report `Class` instead of `Interface` for traits/Protocols." FR-1's guard fires only when `kind ∈ {Interface, AbstractMethod, Protocol, Trait}`. A Rust trait or TS interface reported by the LSP as `Class` therefore **skips `find_implementations` entirely** → its implementors are never enumerated → the exact "interface added, implementor missing" Drift the FR exists to catch is silently missed. FR-1.4 only handles the *empty-result + Class* case, not the *impl-bearing + Class* case (the guard never even ran).
**Recommendation**: Either (a) invoke `find_implementations` opportunistically on `Class` kinds too and treat an empty result as "genuinely none" (cheap, fail-open already covers cost), or (b) add a language→kind-mapping note and a FR-1 acceptance criterion covering the misreported-trait fixture. Cross-link to OQ-6.

### C4 — Empty/degenerate cases for the retention guard unspecified (MAJOR · Nygard, Zero/Empty boundary · Medium)

**Attack (FR-2.1 Zero/Empty)**: FR-8's guards (`count > 20`, `age > 90d`) are well-formed at the 20/90 boundary, but the **zero case** (no slug-prefixed memories exist — first-ever run for a project) and the **all-stale case** (every entry > 90d) are not specified. Does a zero-memory sweep emit `memory_retention_sweep_invoked: true` with all-zero counts, or skip silently? An all-stale sweep could delete *every* memory, including the just-written current-pass entry if ordering is wrong.
**Recommendation**: Specify the zero case (emit invoked:true, zero counts) and protect the current-pass entry from the age sweep (the entry written this run must be exempt — order the write *after* the sweep, or exclude it by recency rank).

### C5 — UC-1 no-abstracts degenerate path uncovered (MINOR · Adzic, degenerate input · Low)

**Issue**: When a UC-1 spec references no abstract/interface symbols, FR-1's step 3b never fires. No acceptance criterion covers this no-op (should it emit `find_implementations_invoked: false`, or omit the field?). Absence-of-signal vs not-run is ambiguous for the grader.
**Recommendation**: Add FR-1 criterion: "WHEN no symbol of kind ∈ {Interface,…} is located, emit `find_implementations_invoked: false`; `implementation_coverage_pct: null`."

---

## Mandatory Artifact: State Variable Registry (FR-15.1)

| Variable Name | Type | Initial Value | Invariant | Read Operations | Write Operations |
|---------------|------|---------------|-----------|-----------------|------------------|
| `serena_version` (FR-7.4) | enum `{<v1.5, ≥v1.5, unknown}` | `unknown` | MUST be one of the three values before FR-6/FR-8 gating reads it | FR-6 gate, FR-8.4 gate | FR-7 Wave 0.5c parse |
| `slug_memory_count` (FR-8) | int ≥ 0 | actual count from `list_memories` | After sweep: `deletable_remaining ≤ 20` (see C1 — currently violable) | FR-8.2 guard | FR-8 delete sweep, Wave 5 `write_memory` |
| `degraded_components` (§9.2) | list[str] | `[]` | append-only within a run; no duplicates | rubric `S_dev_density`, report | FR-1.4, FR-2, FR-4.4, FR-7 fail-open, FR-8.4 |
| `onboarding_status` (FR-6) | enum `{bootstrapped, not_bootstrapped, unknown}` | `unknown` | `unknown` ⇒ no `S_dev_density` down-weight (FR-6.4) | rubric calibration | FR-6 Wave 0.7 parse |
| `S_dev_density` (§5.2) | float 0.0–1.0 | computed Wave 1B | monotonic under up-weighting sub-terms; stays ≤ 1.0 | Wave 2 rubric (§5.3) | FR-1, FR-6, FR-7 sub-terms |
| `implementation_coverage_pct` (FR-1.3) | float 0.0–1.0 \| null | `null` | `null` when guard never fired (C5); else 0.0–1.0 | return contract, rubric | FR-1 step 3b |
| `serena_summary_corroboration` (FR-5.2) | enum `{agree,partial,disagree,unavailable}` | `unavailable` | `unavailable` on session mismatch ⇒ no Drift boost | §10.3 Drift classifier | FR-5 step 7' |

## Mandatory Artifact: Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| retention count | FR-8.2 | Zero/Empty | `count=0` | false (≤20) | **unspecified** (sweep on empty set) | GAP (→C4) |
| retention count | FR-8.2 | One/Minimal | `count=1` | false | no delete | OK |
| retention count | FR-8.2 | Typical | `count=25` | true | delete oldest 5 | OK |
| retention count | FR-8.2 | Boundary | `count=20` / `count=21` | false / true | keep all / delete 1 | OK |
| retention count | FR-8.2 | Max/Accumulation | `count=25, readonly=24` | true | **invariant unreachable** | GAP (→C1, CRITICAL) |
| retention count | FR-8.2 | Sentinel (current-pass entry) | this-run's entry is oldest-by-write | true | **may delete current entry** | GAP (→C4) |
| retention age | FR-8.2 | Boundary | `age=90d` / `age=91d` | false / true | keep / delete (`>` strict) | OK |
| retention age | FR-8.2 | All-stale | every entry `>90d` | true ∀ | **delete-all unspecified** | GAP (→C4) |
| version gate | FR-8.4 | `<v1.5` | `v1.3` | true | write-only-no-retention | OK |
| version gate | FR-8.4 | `≥v1.5` | `v1.5` | false | full rename-propagation | OK |
| version gate | FR-8.4 | Unknown (probe failed) | `unknown` | **undefined** | **no branch** | GAP (→C2, MAJOR) |
| impl kind-guard | FR-1 | Typical | `kind=Interface` | true | invoke find_implementations | OK |
| impl kind-guard | FR-1 | Divergence (misreport) | `kind=Class` (actually Trait) | false | **skip → coverage missed** | GAP (→C3, MAJOR) |
| impl kind-guard | FR-1 | Empty + ambiguous | `kind=Class`, result empty | n/a | degrade + Grep fallback | OK |
| impl kind-guard | FR-1 | Zero (no abstracts) | no matching symbol | false ∀ | **no-op unspecified** | GAP (→C5, MINOR) |
| 3rd-party predicate | FR-4 | Detection | "cites API by name" | **undefined predicate** | non-deterministic trigger | GAP (→R4, MAJOR) |
| onboarding source | FR-6.4 | Inconclusive | neither source resolves | `unknown` | no down-weight | OK |

**Completion-gate note (FR-8/FR-9/FR-10)**: GAP rows above each generate a finding at MAJOR minimum (the count-divergence row escalates to CRITICAL per Pipeline Dimensional Analysis FR-19). Table is complete; synthesis gate satisfied.

## Mandatory Artifact: Quantity Flow Diagram (pipelines present)

Two multi-stage pipelines with count divergence are present.

```text
PIPELINE 1 — FR-8 memory retention (Wave 5)
[Source: N memories from list_memories]
      --> [Stage 1: filter slug-prefix] --> [M items, M <= N]
            --> [Stage 2: exclude read_only] --> [D = M - readonly  DELETABLE]
                  --> [Stage 3: sort by recency + delete count>20] --> [keep min(D,20)]
                        |
                        v
            [Consumer: §1 "prevents unbounded growth" assumes final <= 20]
            [Reality: final = readonly + min(D,20) which can exceed 20]  <-- MISMATCH (C1, CRITICAL)

PIPELINE 2 — Wave 1B.3 cross-task symbol scan (UC-2, >=3 tasks) [pre-existing; FR-2 changes input]
[Source: all touched symbols across tasks: N]
      --> [Stage 1: top-30 cap] --> [min(N,30) symbols]   <-- divergence when N>30
            --> [Stage 2: find_referencing_symbols per node] --> [confirmed edges]
                  --> [Consumer: "for each confirmed interaction"]
            [Interaction edges among the dropped (N-30) symbols are silently unscanned] <-- MAJOR (pre-existing cap)
```

**Pipeline 1 consistency check (Whittaker)**: CRITICAL — see C1. The "≤20" guarantee is not count-conserving under read-only skip.
**Pipeline 2 consistency check**: MAJOR — the top-30 cap is inherited from the existing SKILL (not introduced here), but FR-2 re-anchors the scan's input. The spec should note that declaration-anchoring does not change the top-30 truncation, and that interaction effects beyond rank-30 remain out of scope (cite the existing cap as accepted).

---

## Expert consensus

- The spec is **strong on grounding and fail-open discipline** — every adoption is fact-cited to matrix line numbers and SKILL anchors, and the two upstream-drift corrections (FR-3 absorbed, FR-6 deleted) are genuinely valuable risk reductions.
- The **dominant correctness hole is the memory-retention invariant (C1)** — the one provably-wrong item; it must be fixed before task-builder consumption.
- The **ordering/versioning inconsistencies (A1, A2, A3)** are the highest-leverage requirements fixes — they will otherwise propagate divergence into roadmap/tasklist.
- Several MAJORs (R4, A4, C2, C3) stem from the same root: **runtime-shape uncertainty** in the Serena surface. They are individually fixable by making guards total (three-valued) and operationalising predicates; the residue is already tracked in OQ-1/3/4.

## Improvement roadmap

- **Immediate (resolve before task-builder)**: C1 (CRITICAL); A1, A2, A3 (ordering/versioning contradictions); C2, C3 (total guards).
- **Short-term**: R1, R2, R4, A4, C4 — measurability + guard completeness.
- **Opportunistic**: R3, R5, R6, A5, C5 — cosmetic / degenerate-path clarity.
