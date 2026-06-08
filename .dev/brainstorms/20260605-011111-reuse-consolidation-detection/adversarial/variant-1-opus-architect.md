---
variant: 1
lens: architect
title: "Reuse & Consolidation Detection — Architect Variant (shared sub-spec, extension-scaffolded)"
targets:
  - src/superclaude/skills/sc-reflect-protocol/SKILL.md
  - src/superclaude/skills/tdd/SKILL.md
created: 2026-06-05
---

# Variant 1 — ARCHITECT: Reuse-and-Consolidation Detection

## 0. Design thesis (the architect's load-bearing decision)

The single most important structural choice in this variant: **the detector
is specified ONCE, in a shared, version-pinned sub-spec
(`refs/reuse-audit.md`), and BOTH protocols point at it.** Neither
`sc-reflect-protocol/SKILL.md` nor `tdd/SKILL.md` re-states the detection
algorithm, the verdict vocabulary, the similarity metric, or the
consolidation thresholds. They each contribute only the **integration glue**
appropriate to their stage (pre-build design audit in tdd; post-build
deviation audit in reflect) and reference the shared `Reuse-Audit
Contract v1.0.0`.

This is a deliberate dogfood of the very heuristic being designed: a
duplication-detector whose own spec is duplicated across two SKILL.md files
would be the anti-pattern it exists to stop. OQ6 ("should the two protocols
share one detection sub-spec") is answered **yes** — and answered *because*
the consolidation heuristic in §4 below, applied to "two protocols both
needing reuse detection," returns `extract-shared`.

The detector is built as an **extension of existing chains, never a new
subsystem** (seed takeaway D.4):
- In reflect: it is **Step 8 appended to the §6.1 Wave-1A evidence chain**
  (which already runs auggie+serena), and a **new §10.8 deviation category**
  that slots into the existing 4-category taxonomy machinery.
- In tdd: it is a **new research-assignment type** consumed in Phase 2 and a
  **dedicated synthesis section** surfaced in Phase 5 — reusing the existing
  parallel-investigation substrate rather than adding a parallel search loop.

Everything below is copy-pasteable spec delta. Section §8 is the shared
sub-spec; §6 and §7 are the per-protocol glue.

---

## 1. The shared contract: `Reuse-Audit Contract v1.0.0`

A single versioned data contract that both protocols emit and consume. It is
defined in `refs/reuse-audit.md` (new file, referenced by both SKILL.md
files) and carries `reuse_audit_contract_version: "1.0.0"`.

```yaml
# A single reuse finding (one per new/changed symbol that triggered detection)
- subject_symbol: <name_path>            # e.g. "PrdExecutor/_bind_specs"
  subject_ref: <file:line>               # e.g. "src/superclaude/cli/prd/executor.py:1196"
  capability_tag: <slug>                  # normalized capability (see §3.1), e.g. "post-llm-artifact-injection"
  neighbours:                             # ranked prior-art matches
    - ref: <file:line>                    # "src/superclaude/cli/roadmap/executor.py:678"
      symbol: <name_path>                 # "_inject_pipeline_diagnostics"
      similarity: <float 0.0-1.0>         # composite signal, §3.2
      relationship: sibling-pipeline | same-module | shared-ancestor
      import_allowed: <bool>              # false ⇒ NFR-PRD.7-class ban applies
  verdict: reuse-by-import | mirror-shape | extract-shared | distinct   # §5
  consolidation:                          # §4
    local_impl_count: <int>               # N copies of this capability now in tree (incl. subject)
    cross_module_spread: <int>            # distinct modules the copies live in
    recommend_centralize: <bool>
    centralize_target: <module-path> | null   # e.g. "superclaude.cli.pipeline.artifact_injection"
  severity: advisory | blocking           # §6.4 / §7.4 gate mapping
  confidence: <float 0.0-1.0>             # detector confidence, gates blocking (§6.4)
  stage: pre | post                       # which protocol/timing produced it (§2)
  remedy: <one-line actionable>           # "mirror _inject_* shape" | "extract to pipeline.*" | "import X"
  evidence_grounded: <bool>               # subject_ref AND each neighbour ref re-Read this run (C4)
```

**Forward-compat rule (mirrors reflect §9 unknown-field tolerance):** every
consumer treats unknown top-level fields as read-and-ignore. New verdict
values or signals ship as a `1.x` minor bump.

---

## 2. Stage model — pre vs post as a first-class axis (SC5)

The contract's `stage` field is the spine of the pre/post differentiation.
The detection algorithm in §3 is **identical** across stages — what differs is
**input, evidence source, and remedy**, captured in this table (it lives in
`refs/reuse-audit.md §2` and is referenced, not duplicated, by each SKILL).

| Dimension | **Pre-stage** (`/tdd` Phase 2; `reflect --mode pre`) | **Post-stage** (`reflect --mode post`) |
|---|---|---|
| **Operates on** | *Intentions* — a proposed component/design or a tasklist item that will create a new symbol | *Shipped code* — a new/changed symbol in the diff under audit |
| **Subject source** | Design doc's "new components" list (tdd) / tasklist item verbs like "add/create/build" (reflect pre) | Diff hunks introducing a new top-level symbol (reflect post §6.1 step 2a `find_declaration`) |
| **Evidence** | "A neighbour already does this at `file:line` — model after it / don't build it" | "This new symbol `file:line` duplicates `file:line`; classify the deviation" |
| **Verdict use** | Advisory recommendation injected into the design BEFORE build (cheapest fix point) | Deviation classified under §10.8; can escalate to blocking |
| **Remedy** | Rewrite the design section: reference the neighbour, mark as mirror-shape/extract-shared/reuse-by-import | Tier-3 remediation offer (revert duplicate → reuse) OR documentation note, per §10.8 posture |
| **Failure cost if missed** | A duplicate gets written | A duplicate ships and accrues debt; next reflect post catches it as a higher-severity finding |

**The escalation bridge (architect's extension point):** a Reuse Miss that
`/tdd` or `reflect --mode pre` flagged as `advisory` but that *shipped anyway*
is detected by `reflect --mode post` and upgraded — `severity: blocking`,
`confidence` recomputed against shipped code. The pre-stage advisory and the
post-stage blocking finding share the same `capability_tag`, so the post pass
can cite "this was flagged pre-build as advisory and built anyway" as a
severity multiplier (§6.4). This is the OQ3 answer: advisory at design time
→ blocking Regression-adjacent at post time if ignored.

---

## 3. The detection algorithm (shared, in `refs/reuse-audit.md §3`)

### 3.1 Capability tagging (the normalization layer — the heart of the FP guard)

Each candidate symbol is reduced to a **capability tag** — a normalized
descriptor of *what the code does structurally*, NOT what it is named. The tag
is a composite of three observable features, computed deterministically:

1. **I/O skeleton** — the ordered sequence of structural operations, drawn
   from a fixed vocabulary: `{read-artifact, parse, idempotency-guard,
   transform, inject, write-artifact, size-branch, lookup-map, spawn-subproc,
   validate}`. Example: `_bind_specs` and `_inject_*` both reduce to
   `read-artifact → idempotency-guard → inject → write-artifact`.
2. **Role in call-graph** — `post-llm-injector | file-binder | validator |
   loader | orchestrator | …` (drawn from a fixed enum).
3. **Domain object** — the persisted artifact or entity touched
   (`parsed-request.json`, frontmatter, `--file` args, …).

The tag is `<role>:<skeleton-hash>` — e.g.
`post-llm-injector:read-idemp-inject-write`. Two symbols share a tag **only
when role AND skeleton match**, which is what makes "shared verb, different
shape" (`validate_x` vs `validate_y`) resolve to **different tags** → never a
false positive (C3, SC6).

### 3.2 The composite similarity signal (OQ1)

`similarity ∈ [0,1]` is a weighted composite — NOT a name match, NOT auggie
rank alone:

```
similarity = 0.45 * skeleton_match      # I/O-skeleton sequence overlap (Jaccard on the operation vocabulary)
           + 0.30 * role_match          # 1.0 if call-graph role enum equal, else 0
           + 0.15 * auggie_semantic_rank # normalized mcp__auggie__codebase-retrieval rank score
           + 0.10 * domain_object_match # 1.0 if same persisted artifact/entity touched
```

- **`skeleton_match` is the dominant term (0.45)** by design: structural shape
  is the strongest duplicate signal and the hardest to fake with naming.
- **`auggie_semantic_rank` is a *supporting* term (0.15), never decisive** —
  so the algorithm degrades gracefully when auggie is unavailable (OQ5): drop
  the term, renormalize the remaining weights to sum to 1.0, and stamp
  `degraded: ["reuse-audit:auggie-unavailable"]`. The structural terms
  (skeleton + role + domain = 0.90 of the weight) are computed from
  serena/Read alone, so the detector **never blocks on auggie absence** — it
  loses only its semantic tiebreaker.

### 3.3 Thresholds (OQ1 numeric cut)

| `similarity` | Verdict band | Default severity |
|---|---|---|
| `≥ 0.80` | duplicate — emit reuse finding, run §5 verdict + §4 consolidation | per §6.4/§7.4 |
| `0.60 – 0.79` | near-duplicate — emit **advisory** finding only, never blocking | advisory |
| `< 0.60` | **distinct** — suppress (no finding) | — (C3 guard) |

### 3.4 Scoping for cost (OQ4 — keep the mandatory step cheap)

The step is mandatory but **bounded**: it runs ONLY on symbols that are
**new or signature-changed in the unit under audit** (the diff for reflect
post; the proposed-components list for tdd / reflect pre) — never on the whole
tree. Per-symbol it issues **at most one** `mcp__auggie__codebase-retrieval`
query (the capability tag as the query string) plus the serena symbols already
fetched by §6.1 steps 2-4. A hard cap of **20 candidate symbols per run**
(emit `reuse_audit_truncated: true` + rank-by-diff-size beyond that) keeps the
worst case bounded. Because §6.1's auggie+serena calls already ran for these
symbols, the marginal cost is one query per new symbol — small enough to be
mandatory.

---

## 4. Consolidation heuristic (SC4, OQ2 — the centralize decision)

The verdict in §5 answers "what should THIS symbol have done." The
consolidation heuristic answers the orthogonal question: **"do the now-N copies
of this capability justify a centralized shared component, and where does that
verdict surface?"**

### 4.1 Decision rule (deterministic, in `refs/reuse-audit.md §4`)

Let `N = local_impl_count` (copies sharing a capability tag, including the
subject) and `M = cross_module_spread` (distinct modules those copies span).

```
recommend_centralize = TRUE when:
  (N >= 3)                                  # three strikes — any spread
  OR (N == 2 AND M >= 2)                     # two copies across module boundaries (cross-pipeline duplication)
  OR (N == 2 AND M == 1 AND similarity >= 0.92)  # two near-identical copies in ONE module
otherwise FALSE (advisory "watch" note only)
```

- **`N >= 3` cross-module** is the strong case: the prd `_bind_specs` third
  copy of the inject idiom (roadmap already has two `_inject_*`) lands here →
  `recommend_centralize: true`, `centralize_target:
  "superclaude.cli.pipeline.artifact_injection"`.
- **`N == 2 AND M >= 2`** catches cross-pipeline duplication early (one copy
  in roadmap, one in prd) before a third appears.
- **`N == 2 AND M == 1 AND similarity ≥ 0.92`** is the in-module case (the two
  roadmap `_inject_*` functions): high bar because two near-identical helpers
  in one file is a *local refactor*, not a *shared-module* decision — it
  recommends extract-to-local-helper, not a new cross-module package.

### 4.2 Where the verdict surfaces (OQ3)

| Protocol/stage | Surface | Blocking? |
|---|---|---|
| `/tdd` (pre) | Dedicated **"Reuse & Consolidation Audit"** section in the synthesized TDD (Phase 5), plus a `reuse-audit.yaml` artifact in the task folder | **Advisory only** — tdd is design-time; it informs the design, never halts it |
| `reflect --mode pre` | A finding row in the UC-1 coverage report; feeds the §5 rubric as a structural signal | Advisory unless `recommend_centralize AND confidence ≥ 0.85` → WARN |
| `reflect --mode post` | A **§10.8 Reuse Miss** deviation entry in `deviation-ledger.yaml`; counted in `deviation_count_by_class.reuse_miss` | **Blocking per §6.4** when `verdict != distinct AND recommend_centralize AND confidence ≥ 0.85` |

The architect's principled blocking-vs-advisory rule (C7): **pre-stage is
always advisory** (cheapest fix, no reason to halt design); **post-stage blocks
only on the conjunction of high confidence AND a centralize recommendation** —
a single low-spread near-duplicate is advisory even post-build, so the gate
fires only on real, measured, structural duplication and is therefore trusted
rather than disabled.

---

## 5. Reuse verdict vocabulary (SC7, C2 — honour import bans)

Four-valued, resolved by a deterministic decision tree in
`refs/reuse-audit.md §5`. The tree's first branch is the **module-boundary
check**, so import bans are respected structurally:

```
if similarity < 0.60:
    verdict = distinct                      # FP guard — not a duplicate at all

elif import_allowed(subject_module, neighbour_module) is False:
    # NFR-PRD.7-class ban: prd MUST NOT import roadmap
    if recommend_centralize:                # §4 says N/M justify a shared home
        verdict = extract-shared            # promote skeleton to boundary-neutral module both depend on
    else:
        verdict = mirror-shape              # name+structure after the neighbour for cross-pipeline consistency

else:  # import is architecturally allowed
    if recommend_centralize:
        verdict = extract-shared
    else:
        verdict = reuse-by-import           # just call the existing one
```

**`import_allowed(a, b)`** is computed from declared module-boundary
invariants. The detector reads them from **module-docstring NFR markers**
(the verified mechanism: `NFR-PRD.7: No imports from
superclaude.cli.sprint or superclaude.cli.roadmap.` appears in 8 prd
docstrings) and from any project `import-boundaries.yaml` if present. A ban
**downgrades** the verdict from `reuse-by-import` to `mirror-shape` /
`extract-shared` — never recommends the forbidden import (C2 satisfied).

For the verified case: `_bind_specs` vs roadmap `_inject_*` →
`import_allowed == false` (NFR-PRD.7) AND `recommend_centralize == true`
(N=3 cross-module) → **verdict = `extract-shared`**, target
`superclaude.cli.pipeline.artifact_injection`. Had N been 2 in-module, the
verdict would be `mirror-shape` ("name and shape `_bind_specs` after the
`_inject_*` family").

---

## 6. sc-reflect-protocol/SKILL.md — concrete spec deltas (post + pre)

### 6.1 §6.1 chain — append Step 8 (the mandatory neighbour-search; SC2)

Insert after the existing Step 7' in the §6.1 chain block:

```
8. REUSE-AUDIT (per refs/reuse-audit.md §3) — for each NEW or
   signature-changed top-level symbol resolved by step 2a:
   8a. compute capability_tag (§3.1) from the serena symbol body (step 3) + I/O skeleton
   8b. mcp__auggie__codebase-retrieval information_request=<capability_tag + "existing implementations of this capability">
       directory_path=<repo root>        # one query per candidate symbol; fail-open per §6.5
   8c. for each returned neighbour: re-Read its file:line (§6.2 anti-staleness),
       compute similarity (§3.2), set import_allowed from module-docstring NFR markers (§5)
   8d. emit one reuse-audit row (Reuse-Audit Contract v1.0.0) to
       <output>/reuse-audit.yaml + one audit.log row reuse_audit_invoked: true
       per the §4 per-step convention
```

This is an **addition to the existing chain, not a new system** — it consumes
the serena symbol bodies and auggie substrate already wired at L444-461.
Fail-open identical to steps 3b/7: auggie-absent → degrade per §3.2
(structural-only similarity), never STOP.

### 6.2 §10.8 — new deviation category "Reuse Miss" (SC2, C6)

Insert as new subsection after §10.7, and register it in the §10 taxonomy
machinery as a **5th-named-but-evidence-grounded** category that maps onto the
Drift/Regression precedence spine (it does NOT become a parallel scheme):

```markdown
### 10.8 Reuse Miss

**Definition.** A new or changed symbol that introduces a local
implementation of a capability an existing neighbour already provides
(`similarity ≥ 0.80` per refs/reuse-audit.md §3.3), where the correct verdict
(§5) was reuse-by-import, mirror-shape, or extract-shared — but the code
built a divergent new component instead.

**Detection signals.**
- §6.1 step 8 reuse-audit emits a row with `verdict != distinct`.
- The subject symbol has no inline rationale citing why a fresh
  implementation was required (a NOTE/TODO "intentionally distinct because X"
  downgrades to §10.2 Necessary deviation — see precedence below).
- `recommend_centralize == true` (§4) when N≥2 copies now exist.

**Gold-standard reference.** The neighbour implementation(s) at the cited
`file:line` (re-Read this run, C4) + the module-boundary NFR markers that
determine `import_allowed`.

**Precedence interaction (extends §10.5).** Reuse Miss sits **below
Regression, above Drift**: `Regression > Reuse Miss > Drift > Necessary >
Authorized`. Rationale: a duplicate that *also* contradicts a spec criterion
is a Regression first; an undocumented duplicate that violates no criterion is
a Reuse Miss (more specific than bare Drift). An inline "intentionally
distinct because X" rationale with no contradicted criterion downgrades to
Necessary deviation (§10.2) — rationale authorises a *distinct* build but does
not authorise a *contradiction*.

**Default remediation.** When `verdict == extract-shared` OR
(`recommend_centralize AND confidence ≥ 0.85`): Tier-3 remediation offer in
Wave 6 when `--remediate` (consolidate the N copies into
`centralize_target`). Otherwise: `Documentation note` recommendation
proposing the mirror-shape/import fix. A Reuse Miss with
`severity == blocking` (§6.4) is the only Reuse-Miss case that, like
Regression, forces escalation to Tier 2 per §5.3 (debated by ≥2 reviewers).
```

### 6.3 §5.3 rubric — hook the existing escalation machinery

Insert a new rule between current rules 3 and 4 (renumber downstream),
reusing the Regression-escalation mechanism rather than inventing a new one:

```
| 3a | UC-2 AND any reuse-audit row has `severity == blocking`
       (verdict != distinct AND recommend_centralize AND confidence ≥ 0.85)
     | **ESCALATE** (a high-confidence consolidation-grade Reuse Miss is
       debated by ≥2 reviewers, same structural mechanism as rule 3 Regression) |
```

### 6.4 §6.4 severity computation (where blocking is decided; C7)

A reuse-audit row's `severity` is set:

```
severity = blocking  IFF  stage == post
                          AND verdict != distinct
                          AND recommend_centralize == true
                          AND confidence >= 0.85
                     ELSE advisory
```

`confidence` = `similarity` adjusted by two multipliers: `× 1.1` (cap 1.0) if
the same `capability_tag` was flagged advisory at pre-stage and built anyway
(the §2 escalation bridge); `× 0.8` if auggie was unavailable
(structural-only similarity is slightly less certain). Pre-stage rows are
**always advisory** by construction.

### 6.5 §14.5.2 promotion gate — add condition 4b

Extend the strict gate so blocking Reuse Misses bar promotion, consistent
with drift==0 AND regression==0:

```
4b. `deviation_count_by_class.reuse_miss_blocking == 0` — any reuse-audit row
    with severity==blocking bars promotion. Advisory reuse misses
    (near-duplicates, low spread) do NOT bar promotion — they surface in
    REPORT.md only. *(maps to gate_evaluation.no_blocking_reuse_miss)*
```

### 6.6 §9.1 output-contract additions (1.2.0 → 1.3.0)

```yaml
# Reuse-audit (FR-REUSE)
reuse_audit_ran: <bool>
reuse_audit_path: <abs path to reuse-audit.yaml> | null
reuse_audit_truncated: <bool>                 # >20-candidate cap hit (§3.4)
deviation_count_by_class:
  authorized: <int>
  necessary: <int>
  reuse_miss: <int>                           # NEW — total §10.8 rows
  drift: <int>
  regression: <int>
reuse_miss_blocking: <int>                    # subset with severity==blocking (gates §14.5.2 cond 4b)
reuse_audit_degraded: [<list>]                # e.g. ["auggie-unavailable"]
```

Bump `contract_version` to `"1.3.0"` (additive minor; unknown-field tolerance
in §9 means older consumers ignore the new fields).

---

## 7. tdd/SKILL.md — concrete spec deltas (pre-stage, always advisory)

`/tdd` is design-time/pre-build. The reuse audit is an **extension of Phase 2
investigation** (reusing the parallel-subagent substrate) surfaced as a
**dedicated section in the Phase 5 synthesis** — no new search loop.

### 7.1 New research-assignment type (insert into the A.3 table, ~L228)

```markdown
| **Reuse Auditor** | Detect prior art for each NEW component the design proposes | For every component the design introduces, compute its capability_tag (refs/reuse-audit.md §3.1), query mcp__auggie__codebase-retrieval + sibling pipelines for existing implementations, classify each match (reuse-by-import / mirror-shape / extract-shared / distinct) honouring module-boundary NFR markers, and write a reuse-audit.yaml row per match. |
```

### 7.2 Phase 2 mandatory step (insert after L142 Phase 2 description)

```markdown
- **Phase 2 — Reuse Audit (mandatory, advisory).** Before any "new component"
  enters the design, the Reuse Auditor agent runs refs/reuse-audit.md §3
  against each proposed component. For each, it surfaces "X already does this
  at file:line" as a first-class research finding. This is pre-stage: the
  cheapest possible fix point — the duplicate is caught *before it is
  written*. Output: ${TASK_DIR}research/NN-reuse-audit.md + a
  reuse-audit.yaml the synthesis phase consumes. Degrades gracefully if
  auggie is unavailable (structural-only similarity, refs/reuse-audit.md §3.2).
```

### 7.3 Phase 5 dedicated synthesis section (insert into A.4 synthesis mapping / Phase 5)

```markdown
- **Reuse & Consolidation Audit** (mandatory TDD section). Synthesized from
  the Phase 2 reuse-audit.yaml. For each proposed component: the verdict
  (reuse-by-import / mirror-shape / extract-shared / distinct), the cited
  neighbour `file:line`, the import-ban note (if any NFR forbids the obvious
  import), and — when refs/reuse-audit.md §4 returns recommend_centralize —
  an explicit "Consolidation Recommendation" naming the shared target module.
  This section is **advisory**: it shapes the design but never blocks TDD
  delivery (pre-stage rule, §4.2).
```

### 7.4 A.5 sufficiency gate — add reuse-audit checkpoint (insert at ~L301, item 9)

```markdown
9. **Reuse audit present?** For every NEW component the design introduces, is
   there a reuse-audit.yaml row with a verdict and (if verdict != distinct) a
   cited neighbour file:line? A design that proposes a new component WITHOUT a
   reuse verdict fails this gate — add the Reuse Auditor assignment and
   re-review. (Honours the 2-round gap-fill cap in A.5.)
```

### 7.5 Phase Loading Contract — register refs/reuse-audit.md (L416 table)

Add `refs/reuse-audit.md` to the **builder's** declared loads (Stage A.7
builder row) and to **Stage B** (`/task` execution) declared loads, since the
Reuse Auditor agent prompt embedded in the task file references it. It is
**forbidden** at Invocation / A.1–A.6 (orchestrator does not need the
detection algorithm during scope discovery). This keeps the new ref under the
existing FR-TDD-R.6c phase-isolation contract rather than loading it eagerly.

---

## 8. The shared sub-spec file (`refs/reuse-audit.md`) — outline

New file, the single source of truth both protocols reference. Sections:

- **§1 Contract** — the `Reuse-Audit Contract v1.0.0` YAML schema (this doc §1).
- **§2 Stage model** — pre/post table + escalation bridge (this doc §2).
- **§3 Detection algorithm** — capability tagging, composite similarity,
  thresholds, scoping/cost cap, auggie-unavailable degrade (this doc §3).
- **§4 Consolidation heuristic** — N/M decision rule + surface table (this doc §4).
- **§5 Verdict decision tree** — import-ban-first 4-valued resolver (this doc §5).
- **§6 Degrade & fail-open matrix** — every external dependency (auggie,
  serena, NFR-marker absence) mapped to a graceful-degrade behaviour, so the
  mandatory step NEVER blocks a run (OQ5).

Both SKILL.md files reference it with a load-on-demand pointer
(`> Loaded at runtime from refs/reuse-audit.md — shared reuse-and-consolidation
detection contract, algorithm, and verdict vocabulary`), matching the existing
refs-pointer convention in each skill.

---

## 9. Extension points engineered for the future (architect's scaffolding)

1. **Verdict vocabulary is an open enum** — adding a 5th verdict (e.g.
   `adapter-wrap`) is a `1.x` contract bump, no SKILL.md edits.
2. **`import_allowed` source is pluggable** — reads module-docstring NFR
   markers today; an `import-boundaries.yaml` provider can be added without
   touching the verdict tree.
3. **Similarity weights are named constants in `refs/reuse-audit.md §3.2`** —
   tunable from eval data without re-specifying either protocol.
4. **`capability_tag` skeleton vocabulary is a fixed enum in one place** —
   extending it (new structural ops) is localized to the shared ref.
5. **Both protocols consume one contract** — a future third consumer (e.g. a
   pre-commit `superclaude reuse-audit` CLI) reuses the same ref and schema
   with zero protocol changes. This is the dogfood payoff: the detector's own
   architecture models the reuse-by-shared-module verdict it recommends.

---

## 10. How the verified case flows end-to-end (worked example)

1. **Pre (had /tdd run on the prd --spec design):** Reuse Auditor computes
   `_bind_specs` tag = `post-llm-injector:read-idemp-inject-write`. auggie +
   sibling-pipeline scan finds roadmap `_inject_pipeline_diagnostics`
   (L678) and `_inject_provenance_fields` (L715). similarity ≈ 0.88
   (skeleton match high, role match exact, same persisted-artifact pattern).
   `import_allowed == false` (NFR-PRD.7). N=3 cross-module ⇒
   `recommend_centralize`. Verdict = **extract-shared**, target
   `superclaude.cli.pipeline.artifact_injection`. Surfaced **advisory** in the
   TDD's Reuse & Consolidation Audit section — fix point BEFORE build.
2. **Post (reflect --mode post on the shipped diff):** §6.1 step 8 re-detects
   the same tag against `executor.py:1196`. similarity ≈ 0.88, verdict
   extract-shared, recommend_centralize, confidence 0.88 ≥ 0.85 ⇒
   **severity blocking** → §10.8 Reuse Miss → §5.3 rule 3a ESCALATE →
   §14.5.2 cond 4b bars promotion until consolidated or explicitly
   authorized. If the pre-stage advisory existed and was ignored, confidence
   gets the ×1.1 bridge multiplier.
3. **Remedy:** Wave-6 Tier-3 offer (when `--remediate`) to extract the
   read→idempotency→inject→rewrite skeleton into the boundary-neutral
   `pipeline.artifact_injection` module that prd, roadmap (and any future
   pipeline) depend on — collapsing N=3 copies to 1.
