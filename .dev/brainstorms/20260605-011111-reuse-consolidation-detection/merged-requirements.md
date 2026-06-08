<!-- Provenance: produced by /sc:brainstorm → sc-adversarial-protocol (Mode B, 4 variants, deep) -->
<!-- Base: Variant 4 (opus:architect, gate-placement). Grafts: V2 signal rigor, V5 precision+Grounding-Gaps, V1 shared sub-spec. -->
<!-- Merge date: 2026-06-05T11:52:00Z. Convergence 0.82. fallback_mode: true (variant-3 haiku/qwen vendor failure). -->
---
title: "Enforceable Reuse-and-Consolidation Detection for sc:reflect and /tdd"
status: merged-requirements
adversarial_status: converged
convergence_score: 0.82
targets:
  - src/superclaude/skills/sc-reflect-protocol/SKILL.md
  - src/superclaude/skills/tdd/SKILL.md
  - src/superclaude/skills/_shared/refs/reuse-audit.md  # NEW shared sub-spec
created: 2026-06-05
---

# Enforceable Reuse-and-Consolidation Detection — Merged Requirements

## 0. Thesis (why this design, in one paragraph)

The duplicate that motivated this work — prd's `_bind_specs`/`_persist_bound_specs`
(`executor.py:1196,1245`) re-implementing the roadmap `_inject_*` post-LLM
artifact-injection idiom (`roadmap/executor.py:678,715`) — is **invisible to
every existing gate** for two reasons: it is **spec-conformant** (it does what
the tasklist asked, so no §10 deviation classifier fires) and **name-divergent**
(`_bind_*` vs `_inject_*` share zero name tokens, so any name-keyed check
misses). Therefore detection must be **behavioural, not lexical**, must run as an
**outward neighbour search** (not the existing inward symbol-walk), and must
**ride the gate rails that already exist** rather than add a parallel gate. The
design is delivered as ONE shared, versioned sub-spec (`refs/reuse-audit.md`)
that both protocols reference — itself an `extract-shared` decision, dogfooding
the very heuristic. <!-- src: V2 §0 root-cause; V4 base; V1 §1 -->

**Two facts were verified against the codebase before finalizing (load-bearing):**
- **§17.7 Kill List item 6** of `sc-reflect-protocol/SKILL.md` (L1742) *explicitly
  rejects a 5th deviation category*; evidence-insufficient findings must route to
  `grounding-gaps.yaml` (§10.6). ⇒ **Reuse Miss is a finding *modifier* that maps
  onto the existing Drift/Regression classes by evidence — never a new counted
  class.**
- `superclaude.cli.pipeline` exists and **prd already imports from it**
  (`from superclaude.cli.pipeline.{process,models} import …`). NFR-PRD.7 bans only
  `sprint`/`roadmap`. ⇒ the `extract-shared` verdict has a **real, legal home**
  (`superclaude.cli.pipeline.artifact_injection`); it is actionable today.

---

## 1. Reuse verdict vocabulary (SC7, C2 — unanimous across variants)

Every reuse decision carries exactly ONE verdict:

| Verdict | Meaning | NFR-PRD.7-class behaviour |
|---|---|---|
| `reuse-by-import` | neighbour is import-reachable and no module-boundary ban forbids the edge → call/import it | suppressed when the import crosses a banned edge |
| `mirror-shape` | import forbidden (or inappropriate), but an established neighbour pattern should be matched for naming/structure/idempotency/error-semantics | the **downgrade target** for a banned import |
| `extract-shared` | N≥3 copies, or cross-module copies both sides legitimately need → promote the skeleton to a boundary-neutral module both depend on | always legal (target is neutral, e.g. `cli.pipeline.*`) |
| `distinct` | similarity is surface-level only, or capability/semantics differ materially | no finding |

**Mechanical NFR enforcement (not advisory).** The verdict computer reads the
subject module's docstring `NFR-*: No imports from <pkg>` markers (verified present
in 8 prd files) and any project `import-boundaries.yaml`; it **downgrades
`reuse-by-import` → `mirror-shape`** across any banned edge, and prefers
`mirror-shape` whenever a cross-package edge's legality is *uncertain* (INV-004
safe direction — the gate may never recommend a change that violates the
architecture it protects). <!-- src: V4 §7; V2 §5; V5 §1 -->

---

## 2. The detection signal — composite, behavioural, never a name match (SC6, OQ1)

### 2.1 Capability Fingerprint (CFP) — extracted from real source, not the name
<!-- src: V2 §1.1 -->
For each candidate (a new/changed symbol in post-stage; a proposed component in
pre-stage), build a fingerprint from the evidence the §6.1 chain already gathers:

| Facet | Captures | Extracted via | `_bind_specs` value |
|---|---|---|---|
| F1 I/O skeleton | read→transform→write data-flow shape | serena overview + Read body | read_text(artifact)→mutate→write_text |
| F2 idempotency idiom | guard-then-mutate pattern | grep body (`dedup`, `not in`, `startswith("---`) | "dedup, order-preserving, idempotent" (L1234) |
| F3 persistence target | artifact read/written | Read body, resolve path | parsed-request.json |
| F4 call-graph role | when in the pipeline it fires | serena `find_referencing_symbols` | post-LLM injection (called L480) |
| F5 trust rationale | *why* it exists | docstring/lead comment | "inject what the LLM can't be trusted to produce" |
| F6 domain nouns | entities operated on (verbs stop-listed) | tokenize identifiers | {spec, parent-dir, bound, artifact} |

### 2.2 Composite score (capability + shape dominate; auggie supports, never decides)
<!-- src: merged from V2/V4/V5 — all converge on cap+skel ≥0.80, auggie ≤0.20 -->
```
C_cap   = capability match (F1 trigger-point + F4 role + F5 rationale agreement)
C_shape = structural skeleton match (F1 ordered ops + F2 idempotency idiom)
C_aug   = auggie semantic neighbour rank (normalized; supporting evidence only)

S_reuse = 0.45·C_cap + 0.35·C_shape + 0.20·C_aug
```
- Capability+shape carry 80% because they are what *actually* duplicates and the
  hardest to fake; **auggie rank ≤0.20 and is never decisive**, so the detector
  degrades gracefully when auggie is down (§5).
- `confidence` is a **separate** scalar from `S_reuse` (overlap = "how similar";
  confidence = "how sure the similarity is *meaningful*, not coincidental"),
  calibrated through the existing §5.2 / `confidence-calibrator` machinery — not a
  bespoke number. <!-- src: V4 U-001 -->

### 2.3 Threshold tiers (C-001 — two-floor guard is the strongest FP defence)
<!-- src: V5 §2.5 -->
| Tier | Rule | Handling |
|---|---|---|
| `confident-duplicate` | `S_reuse ≥ 0.82` **AND** `C_cap ≥ 0.80` **AND** `C_shape ≥ 0.70` **AND** no exclusion | hard reuse finding → pick reuse-by-import / mirror-shape / extract-shared |
| `maybe-related` | `0.65 ≤ S_reuse < 0.82`, OR exactly one of C_cap/C_shape below floor | **route to §10.6 Grounding Gaps** — never a hard finding, never increments drift/regression |
| `distinct` | `S_reuse < 0.65`, OR any exclusion applies | no finding (audit-only) |

A candidate cannot reach `confident-duplicate` unless **both** capability and shape
floors pass — the primary false-positive guard.

### 2.4 Worked example (canonical acceptance test — proves the metric fires) <!-- src: V2 §1.3 -->
`_bind_specs` vs `_inject_provenance_fields`: F1=1.0, F2=1.0, F4=1.0, F5=1.0,
F6=0.33, F3=0.5 ⇒ **C_cap≈1.0, C_shape≈1.0, C_aug≈0.8 ⇒ S_reuse ≈ 0.88** →
`confident-duplicate`. A pure name match (`_bind_*` vs `_inject_*` = 0 shared
tokens) scores **0** and misses entirely. That contrast is the whole proof.

---

## 3. False-positive guardrails (SC6 — the trusted-gate requirement)
<!-- src: V5 §3,§8 + V2 §7 -->
Applied **after** scoring; any exclusion forces `distinct` (or Grounding Gap)
unless a stronger, specific capability+shape match is cited:

1. **Shared-verb exclusion** — `validate_*`/`load_*`/`build_*`/`inject_*` name
   overlap is insufficient; if `C_cap < 0.80`, force `distinct`. Verbs are
   stop-listed out of F6 noun-overlap so a shared verb *cannot* contribute.
2. **Generic-CRUD exclusion** — `read_text`/`write_text`, JSON load/dump, DB CRUD,
   dataclass construction, logging, path normalization do **not** count unless
   paired with the same semantic control (idempotency / threshold-routing /
   invariant preservation / same artifact contract).
3. **Shape-without-capability** — same skeleton, different domain object/invariant
   (e.g. one writes user config, one writes a validation report) → not a duplicate.
4. **Capability-without-shape** — same business capability, intentionally different
   phase/perf/security/API boundary → not a duplicate.
5. **Framework/protocol boilerplate** — Click decls, pytest fixtures, CLI option
   parsing, exception wrappers, markdown/YAML assembly → excluded unless a named
   project-specific pattern.
6. **Import-prohibited (for `reuse-by-import` only)** — a ban suppresses
   `reuse-by-import` and re-evaluates as `mirror-shape`/`extract-shared`, NOT
   `distinct`.
7. **Insufficient-grounding** — no grounded `file:line`, or Read can't verify the
   neighbour → no hard finding; route to Grounding Gap.

**Confusion matrix (acceptance):** `_bind_specs` vs `_inject_*` → confident-duplicate;
`validate_config` vs `validate_tasklist` → distinct (verb); two `read_text/write_text`
fns → distinct/maybe (CRUD); two `{path,status,created_at}` dataclasses → distinct
(boilerplate); roadmap injector vs prd binder → mirror-shape/extract-shared, NEVER
reuse-by-import (NFR-PRD.7). <!-- src: V5 §8 -->

---

## 4. Consolidation heuristic (SC4, OQ2)
<!-- src: V4 §4 + V2 §3.2 + V5 §4; N from bounded neighbour set per INV-005 -->
`N` = self + count(neighbours with pairwise `confident-duplicate`), read from the
bounded neighbour-query return set (≤5) — no separate repo census.

| Configuration | Verdict / disposition |
|---|---|
| **N ≥ 3** (any module spread) | `extract-shared` (legal neutral home) or, if forbidden, `mirror-shape` + shared convention. **Blocking-eligible** at post-stage. |
| **N = 2, cross-module (sibling pipelines)** | advisory by default; **blocking-eligible only under the full L3 conjunction** (§5) + Drift-by-evidence. Cross-pipeline divergence is the expensive, hard-to-undo case. |
| **N = 2, same module/file** | advisory `extract-shared` candidate (local helper) — never blocking; intra-module dup is cheap to consolidate later. |
| any `maybe-related` edge | no consolidation recommendation; route uncertainty to Grounding Gaps. |

**Live test:** roadmap already has `_inject_*` ×2 (N=2 in-module = advisory). With
`_bind_specs` the idiom reaches **N=3 cross-module** → `extract-shared` REQUIRED to
`superclaude.cli.pipeline.artifact_injection` (legal — X-002); `reuse-by-import` is
forbidden by NFR-PRD.7.

---

## 5. The escalation ladder + gate model (SC4/C7, OQ3) — base: V4
<!-- src: V4 §1,§4; the load-bearing spine -->
A finding carries `overlap`(=S_reuse), `confidence`, `verdict`. **Identical
computation pre and post; only the bottom rung's disposition differs by build boundary:**

| Rung | Predicate | Pre-stage (`/tdd`, `--mode pre`) | Post-stage (`--mode post`) |
|---|---|---|---|
| L0 | `verdict==distinct` OR `S_reuse<0.65` | suppress | suppress |
| L1 | `0.65≤S_reuse<0.82` OR `confidence<0.70` | advisory note | advisory REPORT note; **does not gate** |
| L2 | `S_reuse≥0.82` AND `0.70≤confidence<0.85` | advisory-strong (recommended change) | Drift-candidate *only if* the §10.3 Drift signal set also holds; else advisory-strong |
| L3 | `S_reuse≥0.82` AND `confidence≥0.85` AND `verdict≠distinct` | **ADVISORY-BLOCKING-PREVIEW** (predicts the post block) | **BLOCKING** → maps to §10.3 Drift (or §10.4 Regression if the copy violates an invariant the original guarantees) |
| L4 | L3 AND copy violates a spec invariant/criterion | preview only | **BLOCKING + ESCALATE** → hooks §5.3 rule-3 (≥2-reviewer Tier-2 debate) |

**Advisory→blocking transition, precisely:** a finding is advisory wherever there
is no shipped artifact to gate (all pre-stage; all post-stage below L3). It becomes
blocking at exactly: **`--mode post` AND rung ≥ L3 AND the §10.3 Drift signal set is
satisfied** (duplicate unmapped to any tasklist item AND no inline rationale). At
that point it is **not a new gate** — it is a Drift entry, and Drift already blocks
§14.5.2 cond-4. **Zero new gate machinery.** <!-- src: V4 §1; conforms to §17.7 -->

**Why L3 needs three independent agreements before blocking:** overlap alone admits
coincidental skeletons; confidence alone can be confidently wrong; `verdict==distinct`
is an absolute veto. High bar to **block** (so the gate isn't disabled), low bar to
**advise** (0.65). <!-- src: V4 §6 G1–G6 -->

---

## 6. Pre-stage vs post-stage differentiation (SC5)
<!-- src: V4 §5 + V2 §4 + V5 §5 -->
| Axis | Pre-stage (`/tdd`, `reflect --mode pre`) | Post-stage (`reflect --mode post`) |
|---|---|---|
| Operates on | *intentions* — proposed component / design / tasklist item | *shipped code* — diff hunk introducing a new symbol/file |
| CFP source | partial — from the design description (F1/F2 may be `planned`) | full — from real shipped source |
| Evidence | "neighbour at file:line already does this; model after it / don't build it" | "this shipped symbol at file:line duplicates file:line; classify the deviation" |
| Max disposition | **ADVISORY-BLOCKING-PREVIEW** (a prediction) | **BLOCKING** Drift/Regression that fails §14.5.2 |
| Remedy | edit the design before code exists (cheapest fix) | §10.3 authorize-or-revert; Tier-3 consolidation task when `--remediate` |
| FP cost | one ignorable recommendation | a blocked promotion → the L3 3-signal high bar applies **here only** |

Pre is **always advisory** (no debt has shipped; a blocking pre-gate gets disabled).
Post **escalates to blocking** only at L3 (the debt now exists and compounds). The
pre-stage PREVIEW and the post-stage BLOCK are the *same finding* on either side of
the build boundary — the detector computes one rung; the boundary decides prediction
vs enforcement. Because post-stage **re-detects independently**, the block does not
depend on any pre→post handoff channel (INV-003). <!-- src: V4 §5 -->

---

## 7. Model-after-for-consistency check (SC3)
<!-- src: V2 §6 + V4 §3 + V5 §7.2 -->
Even when a new component is *not* a full duplicate, if it lands in the
`maybe-related`/L2 band against a **dominant neighbour family** (≥2 existing members
sharing `confident-duplicate` with each other) AND diverges in naming/skeleton from
that family's convention, emit `shape_divergence: true`. Finding text:
`"<C at file:line> diverges from the established <family> pattern (<member file:lines>):
prefix '<C-prefix>' vs family '<F-prefix>', <structural delta>. Mirror the family
shape for cross-pipeline consistency."` This catches `_bind_specs` vs the `_inject_*`
family **even in the world where you decide not to consolidate** — at minimum make
the shapes consistent. `shape_divergence` is an advisory amplifier pre-stage and one
of the L3 signals post-stage.

---

## 8. Cost control + graceful degradation (OQ4, OQ5)
<!-- src: V4 §2.1 + V2 §2.3 + V1 §3.4 -->
- **Scope (mandatory but bounded):** runs ONLY on candidates = new/body-changed
  symbols (post) or proposed components (pre), incl. **new files/modules**
  (INV-002/A-003), never the whole tree. One auggie query per candidate; cap at
  **12 candidates/run**, overflow sampled by diff-hunk size with
  `neighbour_search_sampled: true`. auggie is free → cost is latency, bounded by cap.
- **auggie-unavailable (fail-open, never STOP):** fall back to serena
  `find_symbol` by capability tokens + ripgrep skeleton grep; compute C_cap/C_shape
  from structure only (renormalize, drop C_aug); **findings are capped at advisory
  L2 — a weaker substrate may never block a build**; emit
  `degraded_components: ["neighbour-search:auggie_unavailable"]`. <!-- src: V4 G4 -->
- **Evidence discipline:** every neighbour is **re-Read at its file:line** (§6.2)
  before citation; a hit that doesn't survive re-Read is discarded
  (`reuse_hit_unverified`). No finding without a live citation. <!-- src: V2 §2.2 -->

---

## 9. Concrete spec deltas — `sc-reflect-protocol/SKILL.md`

**(R1) §6.1 chain — insert step 4a/4b** (after step 4 `find_referencing_symbols`,
because F4 call-graph role is needed to build the query):
```
4a. mcp__auggie__codebase-retrieval <capability-keyed neighbour query>   # FR-REUSE.1
    For each candidate (UC-2 new/body-changed symbol incl. new file; UC-1
    proposed component): build the Capability Fingerprint (F1–F6) from steps 2–4
    evidence; fire the NAME-AGNOSTIC capability query (refs/reuse-audit.md §Query);
    cap ≤12 candidates/run (overflow → neighbour_search_sampled).
4b. Re-Read each returned neighbour file:line (§6.2) before citation; compute
    C_cap/C_shape/C_aug → S_reuse (refs/reuse-audit.md §Signal). Retain ≥0.65.
    Fail-open: auggie down → serena+ripgrep fallback, findings CAPPED at advisory
    L2, degraded_components += "neighbour-search:auggie_unavailable"; NEVER STOP.
    Audit row: reuse_sweep_invoked, candidates_scanned, neighbours_found, max_overlap.
```

**(R2) §10 — insert §10.8 "Reuse-Miss (finding modifier — NOT a 5th class)"**
(after §10.6 Grounding Gaps; conforms to §17.7):
```
### 10.8 Reuse-Miss (finding modifier, NOT a 5th deviation class)
A new/changed symbol that implements a capability an existing neighbour already
provides (confident-duplicate, refs/reuse-audit.md §Signal), where a cheaper reuse
path was available. Per §17.7, Reuse-Miss is NOT a deviation class — it MAPS onto
the existing 4 by evidence (mirroring §10.4's exit-code-by-evidence rule):
 - shipped duplicate, unmapped to any tasklist item, no inline rationale → §10.3 Drift
 - shipped duplicate that violates an invariant/criterion the original guarantees → §10.4 Regression
 - shipped duplicate with an inline rationale contradicting no criterion → §10.2 Necessary
 - tasklist/spec/user explicitly approved a separate impl → §10.1 Authorized expansion
Blocking bar (high): mapped to a blocking class ONLY at rung L3 (S_reuse≥0.82 ∧
confidence≥0.85 ∧ verdict≠distinct). Weaker signal, or any auggie-unavailable
fallback finding, OR maybe-related/insufficient-grounding → §10.6 Grounding Gaps
(NEVER deviation-ledger.yaml). Verdict vocabulary: reuse-by-import | mirror-shape |
extract-shared | distinct, with mechanical NFR-import-ban downgrade.
Default remediation: Drift-mapped → "authorize-or-revert OR consolidate"; if
--remediate, Tier-3 consolidate/backfill/revert. Regression-mapped → Tier-3 +
§5.3 rule-3 Tier-2 escalation.
```

**(R3) §5.3 rubric — new row 3a** (no renumber):
```
| 3a | UC-2 AND a Reuse-Miss at rung L3 mapped to Drift or Regression (§10.8) |
   ESCALATE (a shipped high-confidence duplicate is debated by ≥2 reviewers —
   same asymmetric-cost logic as rule 3 Regression) |
```

**(R4) §14.5.2 cond-4 — clarifying clause (NO structural change):**
```
Reuse-Miss findings (§10.8) mapped to Drift or Regression at rung L3 increment
deviation_count_by_class.drift/.regression like any deviation of that class and
gate promotion through this UNMODIFIED condition. Advisory Reuse-Miss findings
(rung ≤ L2, or any auggie-unavailable fallback) do NOT increment these counters
and do NOT gate.
```

**(R5) §9.1 output contract (UC-2) — additive fields (NO `deviation_count_by_class.reuse_miss`):**
```
reuse_sweep_ran: <bool>
reuse_audit_path: <abs path> | null
reuse_miss_blocking: <int>        # rung-L3 findings mapped to Drift/Regression
reuse_miss_advisory: <int>        # rung ≤ L2 (non-gating)
reuse_verdict_count_by_type: {reuse_by_import, mirror_shape, extract_shared, distinct}
reuse_grounding_gap_count: <int>  # maybe-related/insufficient routed to §10.6
neighbour_search_sampled: <bool>
neighbour_search_degraded: <bool> # auggie-unavailable fallback used (caps at L2)
max_overlap_score: <float> | null
```
(`contract_version` minor bump; §9 unknown-field tolerance covers older consumers.)

**(R6) §10.6 Grounding Gaps — extend row schema** with `reuse_candidate`,
`nearest_neighbour: <file:line>`, `similarity_tier: maybe-related|insufficient-grounding`,
`composite_scores: {C_cap, C_shape, C_aug, S_reuse}`. <!-- src: V5 §6.6 -->

---

## 10. Concrete spec deltas — `tdd/SKILL.md` (pre-stage, advisory)
<!-- src: V4 §8.2 + V2 §8.6-8.8 + V5 §7 -->
**(T1) Stage A.3 — mandatory reuse-neighbour search** (new discovery step 2a/2b/2c):
for each proposed new component/helper/pipeline-step, issue one
`mcp__auggie__codebase-retrieval` capability query; record grounded neighbours as
"`<symbol>` already does this at `<file:line>`" (cite only after Read); run the
model-after check + composite triage. `confident-duplicate` → design directive;
`maybe-related` → TDD Reuse Question; `distinct` → surfaced only to explain a
rejected tempting neighbour.

**(T2) A.4 Research Notes — new mandatory `## REUSE_AUDIT` category** (per proposed
component: capability phrase, grounded neighbours+file:line, C_cap/C_shape/C_aug/S_reuse,
tier, verdict, dependency-boundary note, model-after requirements, decision).

**(T3) A.5 sufficiency gate — new item 9:** REUSE_AUDIT populated for EVERY proposed
new component (incl. explicit `distinct`/`maybe-related` for tempting neighbours);
any hard verdict lacking a grounded file:line ⇒ research insufficient.

**(T4) A.7 BUILD_REQUEST — `REUSE_AUDIT_REQUIREMENTS`:** task file MUST carry a Phase-2
reuse-neighbour investigation item per proposed component and a Phase-5 synthesis
instruction to render the audit section; `confident-duplicate` verdicts become design
constraints; `maybe-related` become design questions; **builder MUST NOT instruct
importing across a documented ban — use mirror-shape/extract-shared.**

**(T5) Phase 5 synthesis — mandatory "## Reuse & Consolidation Audit" section**
(advisory by construction; `/tdd` is pre-build):
```
| Proposed component | Nearest prior art (file:line) | tier | Verdict | Disposition |
```
L3 rows carry the **ADVISORY-BLOCKING-PREVIEW** banner: "Building this as a new
component will be classified Drift and BLOCK promotion at `sc:reflect --mode post`.
Recommended action before build: `<verdict>`." Cross-ref: "the verdict recorded here
is the same one `--mode post` recomputes against the shipped diff."

---

## 11. Shared sub-spec `refs/reuse-audit.md` (OQ6 — extract-shared dogfood)
<!-- src: V1 §1,§8; minus the §10.8-counted-class defect -->
ONE versioned file both SKILLs reference (load-on-demand pointer per each skill's
existing refs convention). Sections: **§Contract** (the finding schema), **§Stage**
(pre/post table + the same-finding-across-boundary rule), **§Signal** (CFP + composite
+ two-floor tiers + worked Ω=0.88), **§Verdict** (import-ban-first decision tree),
**§Guards** (7 exclusions + confusion matrix), **§Consolidation** (N rule),
**§Fallback** (auggie-down → advisory-L2 cap), **§Query** (the name-agnostic template).
This is itself an `extract-shared` decision (N=2 protocols would otherwise duplicate
the metric spec) — the design dogfoods its own N≥2→extract-shared rule.

**Kept extension points (2, lean):** (1) verdict vocabulary is an open enum (1.x bump,
no SKILL edits); (2) `import_allowed` source is pluggable (docstring markers today,
`import-boundaries.yaml` later).

---

## 12. Deferred (Simplicity-Guard — compensates for the lost refactorer lens)
Not load-bearing for catching the ground-truth case; explicitly deferred:
- version-contract minor-bump ceremony beyond the single `reuse_audit_contract_version`;
- the pre→post **×1.1 bridge multiplier** (INV-003: needs a cross-invocation channel
  that doesn't exist; post re-detects independently);
- the full 5-item extension-point catalogue (kept 2);
- a standalone `superclaude reuse-audit` CLI.

**Minimal viable set that still catches `_bind_specs`:** one mandatory auggie
capability-query per new symbol → composite signal with two floors →
confident-duplicate → extract-shared (legal home verified) → Drift@post →
blocks §14.5.2 cond-4. Everything else is enhancement.

---

## 13. Open items for the implementing tasklist
- O1 (C-002): final disposition of N=2 cross-module — ship as advisory-with-L3-escalation; revisit after eval data. *(needs_human_decision if a stricter default is wanted.)*
- O2 (INV-004): whether to add an `import-boundaries.yaml` reader now or defer to docstring-markers-only v1.
- O3: exact `refs/reuse-audit.md` location under the skills tree (each skill's refs/ vs a shared `_shared/refs/`) — a real reuse decision to make consistently with how other shared refs are handled.
