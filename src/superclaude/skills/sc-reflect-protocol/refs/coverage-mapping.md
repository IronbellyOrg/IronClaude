# Coverage Mapping Algorithm

This reference defines the deterministic algorithm sc-reflect uses to compute
spec-to-tasklist coverage during **Wave 1B** of the protocol. The algorithm
produces three §9.1 contract fields: `coverage matrix`, `coverage_pct`, and
`unmapped_requirements`. It also derives the `S_dev_density` structural signal
consumed by the §5.3 tier-decision rubric.

The algorithm is **deterministic**: identical inputs (spec text + tasklist
text + flags) produce identical outputs. No LLM heuristic is permitted in the
matching loop — only regex extraction and rule-based ID normalization.

## Spec-to-tasklist coverage map algorithm

The pipeline runs in five stages:

1. **Parse spec.** Read the spec file and extract candidate requirement IDs
   using the regex patterns documented in *Requirement-ID parsing rules*
   below. Emit `R_spec = { id_1, id_2, ..., id_M }` as an ordered set
   (insertion-ordered for determinism).
2. **Parse tasklist.** Read the tasklist file (or tasklist directory's
   `index.md`) and extract task IDs and any requirement-ID references
   embedded in task descriptions. Emit `R_tasklist = { ref_1, ..., ref_K }`
   as an ordered set.
3. **Run bipartite matching.** For each `r ∈ R_spec`, search `R_tasklist`
   for a match (exact, then fuzzy if enabled). See *Bipartite matching
   heuristics* below. Emit a per-requirement match record
   `{ requirement_id, matched_task_ids: [...], match_method: exact|fuzzy|none }`.
4. **Emit coverage matrix.** Serialize the per-requirement match records as
   `coverage matrix` (a list, one row per spec requirement). This is the
   reviewer-facing artifact.
5. **Compute summary fields.** `coverage_pct = matched_count / total_count`
   (rounded to 4 decimals). `unmapped_requirements = [ids where match_method == none]`.
   When `total_count == 0`, see *Requirement-ID parsing rules* fallback below.

The matching loop runs in O(M × K) worst case. For typical specs
(M < 100) and tasklists (K < 200) this is well under one second of
CPU and requires no MCP calls.

## Bipartite matching heuristics

Matching has two passes:

**Primary pass — exact ID equality.** A spec requirement `R-007` matches
any tasklist line containing the literal token `R-007` (word-boundary
regex `\bR-007\b`). This is the only pass guaranteed to run.

**Secondary pass — fuzzy ID normalization (optional, `--fuzzy-ids` flag).**
When enabled, unmatched spec IDs are re-tried after normalization:

- Strip leading zeros: `R-001` → `R-1`
- Strip prefix variants: `REQ-7` ↔ `R-7` ↔ `SPEC-7` (when same numeric)
- Collapse whitespace inside IDs

If a normalized spec ID equals a normalized tasklist ID, mark
`match_method: fuzzy` and surface in the report header so a reviewer
can audit the normalization.

```text
Pseudocode (deterministic, no randomness):

def match(R_spec, R_tasklist, fuzzy=False):
    matrix = []
    for r in R_spec:                       # insertion order preserved
        matched = [t for t in R_tasklist if exact_match(r, t)]
        method = "exact" if matched else "none"
        if not matched and fuzzy:
            matched = [t for t in R_tasklist if norm(r) == norm(t)]
            method = "fuzzy" if matched else "none"
        matrix.append({"requirement_id": r,
                       "matched_task_ids": sorted(matched),
                       "match_method": method})
    return matrix
```

**Worked example.** Spec contains `R-001`, `R-002`, `R-003`. Tasklist
contains `T-100` (mentions `R-001`), `T-101` (mentions `R-2`),
`T-102` (mentions `R-001` and `R-003`), `T-103` (no requirement ref).

| Spec ID | Exact pass            | Fuzzy pass (`--fuzzy-ids`) | Final method | Matched tasks      |
|---------|-----------------------|----------------------------|--------------|--------------------|
| R-001   | T-100, T-102          | —                          | exact        | [T-100, T-102]     |
| R-002   | none                  | T-101 (via `R-2` ↔ `R-002`)| fuzzy        | [T-101]            |
| R-003   | T-102                 | —                          | exact        | [T-102]            |

Result: `matched_count = 3`, `total_count = 3`, `coverage_pct = 1.0000`.
With fuzzy disabled, `R-002` would be unmapped and `coverage_pct = 0.6667`.

## S_dev_density calculation

Per §5.2 of the merged requirements, `S_dev_density` is the **ratio of
unmapped artifacts to total artifacts**, computed per mode:

- **UC-1 (tasklist scope):**
  `S_dev_density = (unmapped_requirements_count + missing_implementations_count) / total_requirements_count`
- **UC-2 (diff scope):**
  `S_dev_density = unmapped_diff_hunks_count / total_diff_hunks_count`

The value is clamped to `[0.0, 1.0]`. When `total_*_count == 0`, the value is
undefined — emit `S_dev_density: null` and rely on the `coverage_undefined`
route (see fallback below) for tier routing.

**FR-1 missing-implementor term (UC-1).** `missing_implementations_count` is the
number of abstract symbols (kind ∈ {Interface, AbstractMethod, Protocol, Trait,
Class}) whose implementors are unaccounted, surfaced by §6.1 step 3b
`find_implementations`. It is added to the UC-1 unmapped numerator above so an
"interface added, implementor missing" gap raises structural ambiguity exactly
like an unmapped requirement. The clamp to `[0.0, 1.0]` and the
`null`-when-`total_requirements_count == 0` rule are unchanged. When the kind-guard
never fires (no eligible abstract symbol), `implementation_coverage_pct` is `null`
(C5) and `missing_implementations_count` contributes `0` — no numerator change.
(OQ for a future iteration: whether `implementation_coverage_pct` should instead
feed S_dev_density as a *parallel* weight rather than a numerator addend; this task
defaults to the numerator-addend form per the BUILD_REQUEST and keeps it consistent
with the `reflection-rubric.md` sub-term.)

**FR-4 verification-failure weight (lint/type channel — parallel weight).** Keyed on
`verification_failures` from the §6.1 step 5.5 verification triangle, **restricted to the
`ruff`/`mypy` lint/type-finding channel** (those tools' exit 1). This is NOT the §10.4
Regression channel (`pytest` exit 1 → `regression_present`) and NOT a numerator addend —
it is a **parallel up-weight** on the computed `S_dev_density` value: a verified lint/type
finding on a hunk the tasklist claimed clean increases structural ambiguity. It is
`null`-safe — when verification did not run (`verification_ran: false`) it contributes `0`,
and the clamp to `[0.0, 1.0]` is unchanged. This mirrors the `reflection-rubric.md`
S_dev_density sub-term so the formula and threshold docs do not diverge.

**FR-RV3-MED.1 hierarchy-gap weight (parallel weight).** Keyed on `hierarchy_gaps_found` /
`hierarchy_coverage_pct` from the §6.1 step 4.5 `type_hierarchy` retrieval, where
`hierarchy_coverage_pct = registered_subtypes / total_subtypes_in_hierarchy`. A type whose
transitive subtype family is under-registered (low `hierarchy_coverage_pct` / nonzero
`hierarchy_gaps_found`) increases structural ambiguity → a **parallel up-weight** on
`S_dev_density` (NOT a numerator addend). It is `null`-safe — when the backend is unavailable
or `--with-hierarchy` is unset (`hierarchy_coverage_pct: null`) it contributes `0`, and the
clamp to `[0.0, 1.0]` is unchanged. This mirrors the `reflection-rubric.md` hierarchy-gap
sub-term so the formula and threshold docs do not diverge.

**Threshold semantics (per §5.3 row 5).** Values `> 0.20` ESCALATE to T2
("too many unmapped artifacts for a single-pass verdict"). The 0.20
threshold is the structural-ambiguity trigger and is the default; it
cannot be relaxed below 0.20 without `--coverage-floor` override (which
controls the §5.3 row 1 floor, not this row).

Boundary rule: `> 0.20` (strict greater-than) is the escalation trigger,
matching the `≤`/`<` discipline established in §4 boundary clarifications.
A value of exactly 0.20 does NOT escalate via row 5.

## Requirement-ID parsing rules

Spec and tasklist parsing share one regex alternation, applied in
priority order (first match wins per token position):

```text
ID_REGEX = r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b"
```

Capture groups:

- `R-\d+` — short-form spec requirement (e.g., `R-001`)
- `REQ-\d+` — long-form spec requirement (e.g., `REQ-007`)
- `SPEC-\d+` — alternate spec form (e.g., `SPEC-12`)
- `T-\d+` — tasklist task identifier (e.g., `T-100`)

IDs are extracted from headings, list items, and inline prose. Code
blocks (fenced ` ``` ` regions) are skipped to avoid false positives
from example snippets.

**Zero-ID fallback (per §4 Wave 1B, Step 1B.2).** When BOTH `R_spec` and
the requirement references in `R_tasklist` are empty (the regex extracts
zero IDs across spec + tasklist), the algorithm sets:

- `coverage_undefined: true`
- `coverage_pct: null`
- `S_dev_density: null`
- Routes the contract directly to T2 (the 0.90 T1 floor cannot pass
  vacuously, per §4 line 269)

This route is **loud, never silent**: `coverage_undefined: true` appears
in the report header and in `tier_decision.yaml`. It is distinct from
the zero-task guard (Step 1B.1), which fires only in UC-1 when
`total_tasks == 0` and STOPs with `status: partial` before tier routing
runs.

## Open Question

§5.2 defines `S_dev_density` in terms of **unmapped artifacts** (hunks or
requirements). The brainstorm spec also references — but does not formalize —
a `changed_files / total_files_in_scope` variant for early-pipeline use
before hunk classification completes. This ref treats the §5.2 unmapped-ratio
definition as authoritative; the changed-files variant is left as a future
enrichment if Wave 1B telemetry shows the hunk count is unreliable on very
small diffs. Resolution should land in a follow-up to merged-requirements
§5.2 before this ref is amended.
