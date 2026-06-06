# Variant 5 — Analyzer Precision Spec: Composite Reuse Signal With False-Positive Guardrails

## Lens

This variant optimizes for **trustworthy precision**. The detector must catch real reuse misses such as the `_bind_specs` / `_persist_bound_specs` post-LLM artifact-injection duplicate without flagging every pair of `validate_*`, `load_*`, dataclasses, or generic read/write helpers. The central design is a **Composite Similarity Signal** that requires agreement across three evidence families before a hard finding is allowed:

1. **Capability tag** — what business/architecture capability the component provides.
2. **Structural skeleton / signature shape** — how it accomplishes the capability, reduced to role-level operations rather than exact syntax.
3. **Auggie semantic neighbour rank** — repository-wide semantic evidence that an existing implementation already does this, grounded to `file:line`.

Low-confidence or evidence-insufficient cases never become hard deviations. They route to `grounding-gaps.yaml` in `sc:reflect` and to a TDD `Reuse Questions / Ambiguities` section in `/tdd`.

---

## 1. Detection vocabulary

All reuse decisions use exactly one of these verdicts:

| Verdict | Meaning | Allowed remediation |
|---|---|---|
| `reuse-by-import` | The neighbour is in an allowed dependency direction and provides the same capability directly enough to call or import. | Replace new local implementation with call/import. |
| `mirror-shape` | Direct import is forbidden or inappropriate, but an established neighbour pattern should be mirrored for naming, structure, field order, idempotency, error semantics, or artifact shape. | Keep local implementation but align with the model implementation. |
| `extract-shared` | Two or more local implementations provide the same capability with high overlap and dependency rules permit a neutral shared module. | Extract common helper into a boundary-neutral module; both call-sites depend on it. |
| `distinct` | Similarity is surface-level only or the capability/semantics differ materially. | No reuse finding. Optionally document why distinct. |

Dependency constraints are authoritative. For the verified PRD case, `NFR-PRD.7` forbids PRD importing roadmap/sprint, so a roadmap neighbour can produce `mirror-shape` or `extract-shared`, not `reuse-by-import`.

---

## 2. Composite Similarity Signal (precision core)

### 2.1 Candidate generation

Run candidate generation only for **new or materially changed components**:

- New function/method/class/dataclass/module.
- Existing function whose responsibility changed materially.
- New artifact writer/reader, pipeline stage, executor hook, validation gate, binding mechanism, diagnostics injection, mapper, parser, or protocol step.

Do not run the expensive comparison for unchanged helpers or pure call-site-only edits.

For each candidate, extract a compact `reuse_candidate_card`:

```yaml
symbol: <name_path or proposed component name>
file: <path>
line_range: <start-end or proposed location>
mode: pre | post
capability_phrase: <one sentence, no implementation detail>
inputs: [<role-level inputs>]
outputs: [<role-level outputs / mutated artifacts>]
side_effects: [read_artifact, write_artifact, call_llm, emit_report, validate_input, none]
structural_skeleton: [<ordered role-level operations>]
idempotency_or_error_semantics: <none | idempotent-prepend | frontmatter-guard | threshold-routing | etc.>
dependency_boundary_notes: [<import bans, layer constraints, package direction>]
```

### 2.2 Auggie neighbour search query

For every `reuse_candidate_card`, issue one mandatory auggie query scoped to the repository and the candidate's sibling modules:

```text
Find existing code that already provides this capability or a closely related model implementation.
Candidate: <symbol/proposed component>
Capability: <capability_phrase>
Inputs/outputs: <inputs> -> <outputs>
Side effects: <side_effects>
Structural skeleton: <structural_skeleton>
Search especially sibling pipelines, same package, shared helpers, and prior implementations with similar idempotency/error semantics.
Return at most 5 neighbours. For each neighbour, provide file:line, symbol name, why it is similar, and whether similarity is capability-level or only surface-level.
```

The report may only cite a neighbour after direct source re-Read of the cited `file:line` range under the existing freshness discipline.

### 2.3 Scoring dimensions

Each candidate-neighbour pair receives three scores plus explicit exclusions.

#### A. Capability score `C_cap` (0.00-1.00)

| Score | Criteria |
|---|---|
| 1.00 | Same domain capability and same trigger point; e.g., post-LLM artifact injection into persisted pipeline output. |
| 0.80 | Same capability, different artifact or phase; e.g., deterministic file binding in another PRD phase. |
| 0.60 | Related capability but different lifecycle role; e.g., both normalize metadata but one is user input parsing and one is report writing. |
| 0.30 | Shared verb/category only; e.g., two `validate_*` functions with different invariants. |
| 0.00 | Different capability. |

#### B. Structural skeleton score `C_shape` (0.00-1.00)

Compare role-level operations, not exact syntax. Generic calls only count if embedded in the same skeleton.

| Score | Criteria |
|---|---|
| 1.00 | Same ordered skeleton and same control semantics: read persisted artifact → normalize/locate target section → idempotency guard → inject deterministic fields → rewrite. |
| 0.80 | Same skeleton with one benign variation: JSON vs frontmatter, per-field vs batch idempotency, same mutation phase. |
| 0.60 | Same high-level read/transform/write shape plus one shared semantic control such as idempotency, threshold routing, or invariant preservation. |
| 0.30 | Generic CRUD/read-write shape only, no shared semantic control. |
| 0.00 | Different operational shape. |

#### C. Auggie semantic rank score `C_aug` (0.00-1.00)

Auggie is used as the whole-codebase semantic search substrate, but not as a sole decider.

| Score | Criteria |
|---|---|
| 1.00 | Auggie returns the neighbour in rank 1-2 and states same capability with grounded `file:line`. |
| 0.80 | Auggie returns the neighbour in rank 3-5 with same capability or rank 1-2 with near capability. |
| 0.60 | Auggie returns the neighbour but labels similarity as partial/model-only. |
| 0.30 | Auggie finds only same naming family or generic pattern. |
| 0.00 | No relevant neighbour or auggie unavailable. |

### 2.4 Composite score

```text
S_reuse = (0.45 * C_cap) + (0.35 * C_shape) + (0.20 * C_aug)
```

Capability carries the highest weight to avoid false positives from shared implementation mechanics. Shape carries the second-highest weight to avoid false positives from shared names. Auggie rank is an evidence multiplier, not an authority override.

### 2.5 Threshold tiers

| Tier | Rule | Verdict handling |
|---|---|---|
| `confident-duplicate` | `S_reuse >= 0.82` AND `C_cap >= 0.80` AND `C_shape >= 0.70` AND no exclusion applies | Hard reuse finding. Must choose `reuse-by-import`, `mirror-shape`, or `extract-shared`. |
| `maybe-related` | `0.65 <= S_reuse < 0.82` OR exactly one of `C_cap`, `C_shape` is below confident floor | No hard finding. Route to Grounding Gap / TDD Reuse Question unless additional evidence raises score. |
| `distinct` | `S_reuse < 0.65` OR any exclusion applies | No finding. May record `distinct` in audit if it was a likely false positive. |

A candidate cannot become `confident-duplicate` unless both capability and shape floors pass. This is the primary false-positive guard.

---

## 3. Explicit false-positive exclusions

Apply exclusions after scoring; any exclusion forces `distinct` unless the reviewer can cite a stronger, specific capability match.

1. **Shared verb exclusion.** Same name prefix/suffix (`validate_*`, `load_*`, `build_*`, `inject_*`, `parse_*`) is insufficient. If `C_cap < 0.80`, force `distinct` regardless of name similarity.
2. **Generic CRUD exclusion.** `read_text`/`write_text`, database CRUD, JSON load/dump, dataclass construction, list comprehension, logging, or path normalization do not count unless paired with the same semantic control (idempotency, threshold routing, invariant preservation, same artifact contract).
3. **Shape-without-capability exclusion.** Same skeleton but different domain object or invariant is not duplicate. Example: two read-transform-write functions where one updates user config and one writes a validation report.
4. **Capability-without-shape exclusion.** Same business capability but intentionally different phase, performance envelope, security boundary, or external API contract is not duplicate unless the model-after check shows divergence from an established pattern is itself harmful.
5. **Framework/protocol boilerplate exclusion.** Dataclasses, Click command declarations, pytest fixtures, CLI option parsing, common exception wrappers, markdown report assembly, and YAML serialization are excluded unless the capability is a named project-specific pattern.
6. **Import-prohibited exclusion for `reuse-by-import` only.** If architecture forbids the import, suppress `reuse-by-import`; re-evaluate as `mirror-shape` or `extract-shared` instead of calling it `distinct`.
7. **Insufficient-grounding exclusion.** If auggie returns no grounded `file:line` and direct Read cannot verify the neighbour, no hard finding is allowed. Route to Grounding Gap.

---

## 4. Consolidation heuristic

After pairwise scoring, evaluate clusters by capability tag.

### 4.1 Cluster formation

A cluster is a set of implementations where every member has at least one edge to another member with:

```text
S_reuse >= 0.82 AND C_cap >= 0.80 AND C_shape >= 0.70
```

### 4.2 Consolidation decision rule

| Condition | Recommendation |
|---|---|
| `N >= 3` confident implementations across any modules | `extract-shared` unless dependency boundaries forbid a neutral module; if forbidden, `mirror-shape` plus explicit shared convention. |
| `N == 2` confident implementations in the same file or same package | `extract-shared` if the shared helper would reduce complexity without worsening readability; otherwise `mirror-shape` and document why extraction is not worth it. |
| `N == 2` confident implementations across sibling pipelines with import ban | `mirror-shape`; upgrade to `extract-shared` only if a neutral shared package is allowed by architectural constraints. |
| `N == 2` confident implementations across allowed dependency direction | `reuse-by-import` if one implementation is canonical; `extract-shared` if neither should own the helper. |
| Any `maybe-related` edge | No consolidation recommendation; route uncertainty. |

### 4.3 Applied to the verified case

- `_inject_pipeline_diagnostics` and `_inject_provenance_fields` already form an `N == 2` same-file cluster for post-LLM artifact injection. That is at least a same-file consolidation candidate.
- `_bind_specs` / `_persist_bound_specs` adds a third implementation of the read → idempotency → inject → rewrite skeleton, but `NFR-PRD.7` forbids PRD importing roadmap.
- Correct verdict: `extract-shared` if a neutral `superclaude.cli.pipeline.*` or equivalent layer is allowed; otherwise `mirror-shape` with explicit naming/shape alignment to the `_inject_*` family. Incorrect verdict: `reuse-by-import` from roadmap into PRD.

---

## 5. Pre-stage vs post-stage behavior

### 5.1 `/tdd` and `sc:reflect --mode pre`

Pre-stage inputs are intentions: proposed components, tasklist items, design sections, PRD-derived capabilities, and planned file changes. The detector asks:

- Does the design propose a component that a neighbour already provides?
- Should the new component call/import, mirror, or extract shared logic before implementation begins?
- Does the TDD name a model implementation to follow?

Pre-stage findings are primarily **course-correction** findings. They block only when the planned design explicitly says it will build a new implementation while a confident `reuse-by-import` or `extract-shared` verdict is available and no architectural constraint justifies local duplication. `mirror-shape` pre-stage findings are advisory unless the tasklist mandates incompatible naming/shape.

### 5.2 `sc:reflect --mode post`

Post-stage inputs are completed diffs and artifacts. The detector asks:

- Did the work introduce a new implementation where a prior one already existed?
- Did it fail to model after an established neighbour pattern?
- Has the cluster crossed a consolidation threshold?

Post-stage confident duplicates become taxonomy entries. If the duplicate is unmapped to the tasklist/spec and has no rationale, classify as `Drift`. If it contradicts an explicit reuse/consolidation requirement or architectural constraint, classify as `Regression`. If the task log documents a valid boundary constraint, classify as `Necessary deviation` with `mirror-shape` or `extract-shared` recommendation.

---

## 6. Concrete spec delta — `src/superclaude/skills/sc-reflect-protocol/SKILL.md`

### 6.1 Add to §6.1 Mandatory evidence-gathering chain after current Step 4

```markdown
4a. mcp__auggie__codebase-retrieval <reuse-neighbour-query>  # reuse/consolidation neighbour search
4b. Re-Read each returned neighbour file:line before citation # ground "X already does this at file:line"
```

Add explanatory text immediately after the existing Step 4 paragraph:

```markdown
Step 4a (Reuse neighbour search) is mandatory for every UC-2 new/materially changed symbol and every UC-1 proposed component or tasklist item that introduces a new system component. The orchestrator builds a `reuse_candidate_card` containing capability phrase, role-level inputs/outputs, side effects, structural skeleton, idempotency/error semantics, and dependency-boundary notes, then issues one `mcp__auggie__codebase-retrieval` query asking: "what already does this, and where?" The query MUST ask for grounded `file:line` neighbours and MUST distinguish capability-level similarity from surface-level name or CRUD similarity.

Step 4b grounds every neighbour citation. A reuse finding may not say "X already does this at file:line" unless that neighbour range has been freshly Read under §6.2. If auggie is unavailable, returns no grounded neighbour, or the Read cannot verify the cited capability, the detector MUST NOT create a hard deviation; it writes a §10.6 Grounding Gap row with `evidence_missing: reuse-neighbour-grounding`.
```

### 6.2 Add new §6.1.2 Reuse Candidate Card and Composite Similarity Signal

```markdown
### 6.1.2 Reuse Candidate Card + Composite Similarity Signal

For each new/materially changed symbol (UC-2) or proposed component (UC-1), build:

```yaml
symbol: <name_path or proposed component>
file: <path or planned path>
line_range: <line-range|null>
mode: pre | post
capability_phrase: <one-sentence capability, no implementation detail>
inputs: [<role-level inputs>]
outputs: [<role-level outputs / mutated artifacts>]
side_effects: [read_artifact, write_artifact, call_llm, emit_report, validate_input, none]
structural_skeleton: [<ordered role-level operations>]
idempotency_or_error_semantics: <semantic control or none>
dependency_boundary_notes: [<import bans / layer constraints>]
```

Compare each auggie neighbour with the Composite Similarity Signal:

- `C_cap` capability match: 1.00 same capability/trigger; 0.80 same capability different artifact/phase; 0.60 related lifecycle role; 0.30 shared verb/category only; 0.00 different capability.
- `C_shape` structural skeleton match: 1.00 same ordered skeleton and same control semantics; 0.80 same skeleton with one benign variation; 0.60 same read/transform/write shape plus one shared semantic control; 0.30 generic CRUD shape only; 0.00 different shape.
- `C_aug` auggie semantic rank: 1.00 rank 1-2 same capability; 0.80 rank 3-5 same capability or rank 1-2 near capability; 0.60 partial/model-only; 0.30 name/generic only; 0.00 no grounded neighbour.

`S_reuse = (0.45 * C_cap) + (0.35 * C_shape) + (0.20 * C_aug)`.

Tiering:

- `confident-duplicate`: `S_reuse >= 0.82` AND `C_cap >= 0.80` AND `C_shape >= 0.70` AND no exclusion applies.
- `maybe-related`: `0.65 <= S_reuse < 0.82` OR exactly one of `C_cap`, `C_shape` is below the confident floor.
- `distinct`: `S_reuse < 0.65` OR an exclusion applies.

Hard reuse findings are allowed only for `confident-duplicate`. `maybe-related` routes to §10.6 Grounding Gaps and never increments drift/regression counts. `distinct` is audit-only.

False-positive exclusions: shared verb, generic CRUD/read-write/dataclass/framework boilerplate, shape-without-capability, capability-without-shape, import-prohibited-for-reuse-by-import, and insufficient grounding. These exclusions force `distinct` or Grounding Gap unless stronger capability+shape evidence is cited.
```

### 6.3 Add to §5.3 Tier-Decision Rubric

Add a structural signal to §5.2:

```markdown
- `S_reuse_confident` — count of `confident-duplicate` reuse findings from §6.1.2.
- `S_reuse_maybe` — count of `maybe-related` reuse candidates routed to Grounding Gaps.
```

Add a new decision row before current Regression row:

```markdown
| 3a | UC-2 AND `S_reuse_confident > 0` AND any finding's recommended verdict is `reuse-by-import` or `extract-shared` | **ESCALATE** (a shipped high-confidence reuse miss must be debated by ≥2 reviewers before blocking classification) |
```

Renumbering can be avoided by naming it `3a`; existing rule numbers remain stable for compatibility.

### 6.4 Add to §9.1 Stable contract under UC-2 fields

```yaml
reuse_audit_path: <abs path> | null
reuse_verdict_count_by_type:
  reuse_by_import: <int>
  mirror_shape: <int>
  extract_shared: <int>
  distinct: <int>
reuse_confident_duplicates: <int>
reuse_maybe_related: <int>
```

Add to telemetry:

```yaml
reuse_candidate_count: <int>
reuse_auggie_queries: <int>
reuse_exclusions_applied: <int>
reuse_grounding_gap_count: <int>
```

### 6.5 Add taxonomy entry after §10.3 Drift or as §10.3.1 Reuse Miss signal

```markdown
### 10.3.1 Reuse Miss (Drift/Regression signal, not a fifth category)

**Definition.** A new or materially changed component duplicates an existing grounded implementation or established model pattern when the work should have reused, mirrored, or extracted shared logic.

Reuse Miss is NOT a fifth deviation category. It is a detection signal that maps into the existing taxonomy:

- `Regression` when the duplicate violates an explicit spec/tasklist requirement, architectural constraint, or stated consolidation/reuse requirement.
- `Drift` when the duplicate is unmapped to the tasklist/spec and lacks a documented rationale.
- `Necessary deviation` when a boundary constraint prohibits direct import but the implementation documents why local/mirrored shape is required.
- `Authorized expansion` when the tasklist/spec/user explicitly approved a separate implementation despite the neighbour.

**Required evidence for a hard Reuse Miss.**

1. A freshly Read neighbour citation: "`<symbol>` already does this at `<file:line>`".
2. Composite Similarity Signal tier `confident-duplicate` from §6.1.2.
3. One verdict from `reuse-by-import | mirror-shape | extract-shared | distinct`.
4. Dependency-boundary check showing whether import is allowed.

**Low confidence.** `maybe-related` and insufficient-grounding candidates MUST route to §10.6 Grounding Gaps instead of `deviation-ledger.yaml`.
```

### 6.6 Extend §10.6 Grounding Gaps schema

Add optional fields to the required row schema:

```yaml
  reuse_candidate: <symbol|null>
  nearest_neighbour: <file:line|null>
  similarity_tier: maybe-related | insufficient-grounding | null
  composite_scores:
    C_cap: <float|null>
    C_shape: <float|null>
    C_aug: <float|null>
    S_reuse: <float|null>
```

Add wording:

```markdown
Reuse candidates with `maybe-related` scores are evidence-insufficient by design. They force `status: partial` like other Grounding Gaps only when the missing decision affects promotion or implementation choice; otherwise they are reported as advisory questions with `decision_needed_by_user: false`.
```

### 6.7 Extend §14.5.2 promotion gate condition 4 and 6

Amend condition 4:

```markdown
A `confident-duplicate` Reuse Miss classified as Drift or Regression contributes to the existing drift/regression counts and therefore blocks promotion under this condition. A `mirror-shape` recommendation classified as Necessary deviation does not block by itself.
```

Amend condition 6:

```markdown
Reuse `maybe-related` entries in `grounding-gaps.yaml` block promotion only when `decision_needed_by_user: true`; advisory reuse questions do not block unless they prevent classification of a shipped hunk.
```

---

## 7. Concrete spec delta — `src/superclaude/skills/tdd/SKILL.md`

### 7.1 Update Execution Overview Stage A

Replace Stage A step 3 with:

```markdown
3. Perform scope discovery — map component files, plan assignments, and run mandatory reuse-neighbour search for proposed new components (A.3)
```

### 7.2 Add to A.3 Discovery steps after current step 2

```markdown
2a. **Mandatory reuse-neighbour search** — for each proposed new component/service/helper/pipeline step implied by the request or PRD, issue one `mcp__auggie__codebase-retrieval` query asking what already provides the same capability in the codebase. The query MUST include capability phrase, expected inputs/outputs, side effects, and any known structural skeleton. Record grounded neighbours as: "`<existing symbol>` already does this at `<file:line>`". Do not cite a neighbour unless the file:line has been Read.

2b. **Model-after-for-consistency check** — when a grounded neighbour is not directly reusable because of dependency boundaries or scope differences, decide whether the new design should model after its naming, shape, idempotency semantics, artifact format, or error handling. Record the model implementation and the exact shape elements to mirror.

2c. **Composite similarity triage** — score each candidate-neighbour pair with the reuse signal: capability match, structural skeleton/signature shape, and auggie semantic rank. Only `confident-duplicate` candidates become reuse directives. `maybe-related` candidates become TDD reuse questions/ambiguities. `distinct` candidates are not surfaced unless needed to explain why a tempting neighbour was rejected.
```

### 7.3 Extend Research Notes categories in A.4

Change "8 categories" to "9 categories" and add before `AMBIGUITIES_FOR_USER`:

```markdown
## REUSE_AUDIT
[Mandatory. For each proposed new component/helper/pipeline step:
- Proposed component: name/path if known
- Capability phrase
- Auggie query summary
- Grounded neighbours: symbol + file:line + why relevant
- Composite scores: C_cap, C_shape, C_aug, S_reuse
- Similarity tier: confident-duplicate / maybe-related / distinct
- Verdict: reuse-by-import / mirror-shape / extract-shared / distinct
- Dependency-boundary notes: import allowed? import banned? neutral shared module possible?
- Model-after requirements: naming/shape/idempotency/artifact/error semantics to mirror
- Decision: incorporate into TDD, ask user, or no action]
```

Update sufficiency gate A.5 with new item 9:

```markdown
9. Is REUSE_AUDIT populated for every proposed new component/helper/pipeline step, including explicit `distinct` or `maybe-related` handling for tempting neighbours? If any hard reuse verdict lacks a grounded file:line citation, research is insufficient.
```

### 7.4 Add builder instruction to A.7 BUILD_REQUEST

Add this required field to the BUILD_REQUEST payload:

```markdown
REUSE_AUDIT_REQUIREMENTS:
- The task file MUST include a Phase 2 reuse-neighbour investigation item for each proposed new component not already resolved in research notes.
- The task file MUST include Phase 5 synthesis instructions to render a "Reuse & Consolidation Audit" section in the TDD.
- Any `confident-duplicate` verdict must become a design constraint: `reuse-by-import`, `mirror-shape`, or `extract-shared`.
- Any `maybe-related` verdict must become an explicit design question/assumption, not a hard reuse mandate.
- The builder MUST NOT instruct implementation to import across documented architecture bans; use `mirror-shape` or `extract-shared` instead.
```

### 7.5 Add Phase 5 synthesis requirement

Add to the Phase 5 description:

```markdown
Phase 5 synthesis MUST include a `Reuse & Consolidation Audit` section with:

| Proposed component | Existing neighbour (`file:line`) | Similarity tier | Verdict | Design action |
|---|---|---|---|---|

For `reuse-by-import`, cite the canonical component to call. For `mirror-shape`, cite the model implementation and list shape/naming/idempotency elements to mirror. For `extract-shared`, name the neutral shared layer and both call-sites. For `distinct`, include only when a likely false positive was evaluated and rejected. For `maybe-related`, list the unresolved evidence and whether user decision is needed.
```

### 7.6 Add pre-build blocking rule

```markdown
**Pre-build reuse gate.** A TDD may not recommend building a brand-new component when REUSE_AUDIT has a `confident-duplicate` verdict of `reuse-by-import` or `extract-shared` unless the TDD also documents the architectural reason not to reuse. `mirror-shape` verdicts are advisory design constraints: they do not prohibit a local implementation, but the TDD must specify the model-after shape to preserve consistency.
```

---

## 8. Worked confusion-matrix example

| Scenario | Naive detector result | Composite signal result | Why |
|---|---|---|---|
| `_bind_specs` / `_persist_bound_specs` vs roadmap `_inject_pipeline_diagnostics` + `_inject_provenance_fields` | Might miss because names differ (`bind` vs `inject`) or might flag only by `read_text/write_text`. | `confident-duplicate`; verdict `mirror-shape` or `extract-shared`. | Same post-LLM artifact-injection capability (`C_cap >= 0.80`), same read → idempotency → inject → rewrite skeleton (`C_shape >= 0.80`), grounded auggie neighbour (`C_aug >= 0.80`). Import ban suppresses only `reuse-by-import`. |
| Two functions named `validate_config` and `validate_tasklist` | False positive because both start with `validate`. | `distinct`. | Shared verb exclusion; likely `C_cap <= 0.30` unless they validate the same invariant for the same artifact. |
| Two functions both call `read_text` and `write_text` | False positive because both are read/write. | `distinct` or `maybe-related`. | Generic CRUD exclusion; `C_shape` cannot exceed 0.30 without same semantic control like idempotency/invariant preservation. |
| Two dataclasses with `path`, `status`, `created_at` fields | False positive because same generic shape. | `distinct`. | Framework/boilerplate exclusion; dataclass shape alone is not a project-specific capability. |
| PRD `_build_file_args` vs a proposed PRD inline-with-cap binder | Could miss because one is process-layer and the other is executor-layer. | Likely `confident-duplicate` or high `maybe-related` depending proposed details; verdict `reuse-by-import` if same package dependency allowed, otherwise `mirror-shape`. | Same deterministic file-binding capability and threshold-routing semantics; shape has threshold cutoff and allowed refs, not generic file IO. |
| Roadmap injector vs PRD binder | Naive detector says "import roadmap helper". | `mirror-shape` / `extract-shared`, never `reuse-by-import`. | Dependency-boundary check honors `NFR-PRD.7`. |

---

## 9. Why this variant is precise

This design prevents false positives by requiring **capability and shape agreement simultaneously**. Names and common library calls are explicitly weak evidence. Auggie's role is to surface grounded neighbours cheaply, but auggie rank cannot override low capability or generic shape. The detector therefore catches the real `_bind_specs` / `_inject_*` duplication while suppressing the noisy cases that make users disable gates: shared verbs, generic CRUD, dataclass boilerplate, and framework patterns.
