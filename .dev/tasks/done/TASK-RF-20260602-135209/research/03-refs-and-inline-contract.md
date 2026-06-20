# Research: refs/ + inline §9 contract

Topic type: Integration Points (EXACT edit targets)
Scope: refs/{reflection-rubric,deviation-taxonomy,reviewer-spec,coverage-mapping}.md + SKILL.md §9.1 (inline return contract) + §9.2 (telemetry)
Status: In Progress
Date: 2026-06-02

---

## OQ-5 / refs/return-contract.yaml ABSENCE — CONFIRMED

`ls src/superclaude/skills/sc-reflect-protocol/refs/` returns 11 files:
cost-profile.yaml, coverage-mapping.md, deviation-taxonomy.md, grader-extensions.md,
input-resolution.md, ops-integration.md, promotion-adapters.md, reflection-rubric.md,
remediation-handoff.md, report-template.md, reviewer-spec.md.

There is NO `return-contract.yaml`. The return contract is INLINE in SKILL.md §9.1.
The telemetry schema is INLINE in SKILL.md §9.2. All FR contract/telemetry edits target
SKILL.md, not a separate ref file.

**Spec self-confirms this** — `04-spec-low-complexity.md:318` lists the file
`refs/return-contract.yaml *(if present — see OQ-5)*` with the conditional "if present",
and `04-spec-low-complexity.md:351` routes the contract additions to "§9.1 RETURN-CONTRACT
additions" (SKILL.md inline), not a YAML ref. CONCLUSION FOR TASK-BUILDER: the
"refs/return-contract.yaml" row in the §5 file-change matrix (spec line 318) is a NO-OP /
should be struck — those edits land in SKILL.md §9.1 inline instead.

---

## 1. reflection-rubric.md — S_dev_density sub-terms (FR-1, FR-6, FR-7)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md`

The `S_dev_density` **structural-signal definition** (range + threshold semantics) lives at
**reflection-rubric.md:102-112**, under heading `### S_dev_density` (line 102). The actual
**arithmetic** is deferred to coverage-mapping.md (see §2 below); this ref only defines the
signal and its tier thresholds. Current text (lines 102-112):

```text
### S_dev_density

**Definition.** For UC-2: `unmapped_diff_hunks / total_hunks`. For UC-1: `unmapped_spec_requirements / total_requirements`.

**Range.** Float `0.00-1.00`.

**Threshold semantics (from §5.3 / §5.5):**

- `≤ 0.05` — near-zero ambiguity, eligible for the strict T1 STOP rule
- `≤ 0.10` — eligible for the §5.3 rule-2 path (WARN above 0.05)
- `> 0.20` — automatic ESCALATE (rule 5): "at one in five unmapped artifacts, a single reviewer cannot adjudicate without ensemble pressure"
```

**Where FR sub-terms add** (per spec line 315 + line 404): a NEW sub-section/bullet block
must be inserted INSIDE the `### S_dev_density` section, after the existing "Threshold
semantics" bullets (i.e. after line 112, before the closing `---` at line 113). The three
sub-terms the spec mandates:

- **FR-1 (missing-implementor count):** S_dev_density gains an unmapped-implementor term —
  `missing_implementations` count (abstract symbols whose implementors are unaccounted)
  feeds the unmapped-artifact numerator for UC-1. (spec FR-1.3 line 152; §5 line 315/404)
- **FR-6 (onboarding-status weight):** grounding-confidence weight on S_dev_density keyed by
  `onboarding_status` — `not_bootstrapped` down-weights confidence; `unknown` is NO signal
  (NOT down-weighted, per FR-6.4 line 242). (spec line 233 description; line 315/404)
- **FR-7 (context-exclusion up-weight):** when an active Serena context excludes a
  chain-critical tool, S_dev_density is UP-weighted (FR-7.3 line 258) and
  `["serena:context-excluded"]` is added to `degraded_components`. (spec line 315/404)

EDIT TARGET: insert one new `**S_dev_density sub-terms (V3 Serena adoptions)**` block after
reflection-rubric.md:112. The §5.3 numeric thresholds (lines 108-112) stay AS-IS — these are
additive weighting inputs, not threshold changes.

---

## 2. coverage-mapping.md — S_dev_density arithmetic (FR-1/6/7 extend here)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md`

YES — the S_dev_density **computation** lives here, confirming R2's note that SKILL.md defers
the calculation to a ref. The authoritative math is at **coverage-mapping.md:89-111**, heading
`## S_dev_density calculation` (line 89). Current text (lines 89-101):

```text
## S_dev_density calculation

Per §5.2 of the merged requirements, `S_dev_density` is the **ratio of
unmapped artifacts to total artifacts**, computed per mode:

- **UC-1 (tasklist scope):**
  `S_dev_density = unmapped_requirements_count / total_requirements_count`
- **UC-2 (diff scope):**
  `S_dev_density = unmapped_diff_hunks_count / total_diff_hunks_count`

The value is clamped to `[0.0, 1.0]`. When `total_*_count == 0`, the value is
undefined — emit `S_dev_density: null` and rely on the `coverage_undefined`
route (see fallback below) for tier routing.
```

**Structure FR-1/6/7 extend:** the per-mode numerator/denominator formula (lines 94-97) is the
extension point. FR-1's missing-implementor count adds to the UC-1 `unmapped_requirements_count`
numerator (or a parallel `implementation_coverage` term). FR-6/FR-7 are *weighting* adjustments
to the clamped value, not numerator changes.

**TASK-BUILDER DISAMBIGUATION (cross-ref hazard):** the §5 matrix (spec line 315) names ONLY
`refs/reflection-rubric.md` as the S_dev_density edit target, but the actual arithmetic lives in
`coverage-mapping.md:89-111`. If FR-1's missing-implementor term changes the *formula* (not just
a weight), coverage-mapping.md MUST also be edited — the spec matrix under-specifies this. The
clean split: reflection-rubric.md gets the *threshold/weight semantics* (FR-6 weight, FR-7
up-weight); coverage-mapping.md gets any *numerator change* (FR-1 missing-implementor count if
it enters the ratio). Recommend the task-builder add coverage-mapping.md as a secondary edit
target for FR-1 OR keep FR-1 purely as an additive rubric weight (no formula change). OQ for the
task: does `implementation_coverage_pct` feed S_dev_density's ratio, or is it a parallel signal?
Spec line 121 says "S_dev_density consumes ROW 1/2/4/6/7 signals" — implying ROW 1 (FR-1) IS an
input, so coverage-mapping.md:94-97 likely needs the term.

---

## 3. deviation-taxonomy.md — Necessary (§10.2) + Drift (§10.3) classifier inputs (FR-4, FR-5)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`

NOTE ON NUMBERING: the ref uses category NAMES, not "§10.2/§10.3" numbers — those numbers are
SKILL.md spec-section anchors (SKILL.md:689 `### 10.2 Necessary deviation`, SKILL.md:704
`### 10.3 Drift`). The ref's equivalent sections:

- **Necessary** classifier: deviation-taxonomy.md heading `## Necessary` (line 41); its
  **Detection signals** list is **lines 44-49**. Current text:

```text
**Detection signals.**

- Diff hunk includes a TODO / NOTE / FIXME explaining why the original plan could not be followed.
- Commit message body (not subject) contains the rationale.
- Task log contains "blocked by X, deviated to Y" entry.
- The deviation does NOT contradict any acceptance criterion in the spec.
```

- **Drift** classifier: deviation-taxonomy.md heading `## Drift` (line 56); its **Detection
  signals** list is **lines 59-63**. Current text:

```text
**Detection signals.**

- Diff hunk does NOT map to any tasklist item.
- No commit-body rationale, no inline comment, no task-log entry explaining the change.
- Does NOT contradict any acceptance criterion (this is what distinguishes drift from regression).
```

**Where FR signals add** (per spec line 316 + line 404):

- **FR-4 `third_party_api_verified`** → add to the **Necessary** Detection-signals list
  (deviation-taxonomy.md:44-49). Spec FR-4.3 (line 207): "a `third_party_api_verified` flag
  feeds the §10.2 Necessary-deviation classifier." A verified external API resolution supports
  classifying an external-API divergence as Necessary (forced by a real constraint) rather than
  Drift. EDIT TARGET: append a bullet to the lines 44-49 list.
- **FR-5 `serena_summary_corroboration`** → add to the **Drift** Detection-signals list
  (deviation-taxonomy.md:59-63). Spec line 404: "the §10.3 Drift classifier gains
  `serena_summary_corroboration` (FR-5)." A `disagree` corroboration boosts Drift detection;
  `agree`/`partial`/`unavailable` per FR-5.2 (line 223). EDIT TARGET: append a bullet to the
  lines 59-63 list.

**MIRROR-EDIT HAZARD (cross-ref with R1/R2):** SKILL.md §10.2 (SKILL.md:693-698) and §10.3
(SKILL.md:708-712) carry IDENTICAL Detection-signals lists. The same two bullets must be added
in SKILL.md too, or the ref and SKILL.md drift. Confirm with R1 whether SKILL.md §10.2/§10.3
edits are in their scope; if not, the task-builder must add BOTH (ref + SKILL.md) as paired edits.

---

## 4. reviewer-spec.md — Step 3B.0 brief grounding-hunks (FR-1, FR-3)

**File:** `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`

Step 3B.0 brief structure spans **reviewer-spec.md:9-56** (`## Brief template`, line 9). The
three required brief sections are at lines 22-52. The target sub-section for FR-1/FR-3 is
`#### \`## Grounding hunks\`` at **line 31**, body **lines 33-37**. Current text (lines 31-37):

```text
#### `## Grounding hunks`

Reviewer-scoped grounding hunks: `file:line` excerpts pulled from Wave 1A's grounding pass. Each hunk is filtered to those the reviewer's persona will actually cite.

Example shape — the brief contains an H2 `## Grounding hunks` heading followed by one H3 per hunk; each H3 is the `file:line-range` ref, and the H3 body is the language-tagged fenced code block of the source excerpt. For example, an H3 like `### src/superclaude/pm_agent/confidence.py:42-58` is followed by a fenced python block containing the verbatim source between lines 42 and 58. The same shape is used for test files, e.g., H3 `### tests/pm_agent/test_confidence.py:101-115` followed by the corresponding fenced Python block.

Each hunk preserves the `file:line` ref so the `evidence-validator` agent can re-Read it at the Wave 5 final gate.
```

**Where FR-1/FR-3 add** (per spec line 317): "Add `find_implementations` list + extended-info
references to the per-reviewer brief grounding-hunks section (Wave 3 step 3B.0)."

- **FR-1:** the `find_implementations` implementor list (the polymorphic surface) must be
  injected into the `## Grounding hunks` section so reviewers see the abstract-symbol implementor
  set. EDIT TARGET: extend the lines 33-37 body with a paragraph/bullet on the implementor-list
  hunks.
- **FR-3:** the `find_referencing_symbols` extended-info (`include_info: true`, per FR-3 line
  180-197) references must surface into the same grounding-hunks block (richer reference context).
  EDIT TARGET: same block, lines 33-37.

The "Contract emission" line (`reviewer_briefs_materialized`, lines 54-56) is unaffected — no new
emission field required by FR-1/FR-3 here.

---

## 5. SKILL.md §9.1 inline contract — exact insertion points + version bump

**File:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md`

**contract_version current value = `1.0`** (string `"1.0"`). THREE sites for the bump to `1.1.0`
(matches R1's "3 sites"):

| Site | Line | Current text | New text |
|------|------|--------------|----------|
| Heading | SKILL.md:491 | `### 9.1 Stable contract (contract_version: 1.0)` | `### 9.1 Stable contract (contract_version: 1.1.0)` |
| YAML value | SKILL.md:494 | `contract_version: "1.0"` | `contract_version: "1.1.0"` |
| Trailer | SKILL.md:599 | `...Contract version is \`v1.0\`.` | `...Contract version is \`v1.1.0\`.` |

NOTE: current heading/value are 2-segment (`1.0`); spec mandates 3-segment SemVer `1.1.0`
(spec line 318, 351, 402, 471). The bump normalizes to 3 segments.

**§9.1 field insertion points** (inside the yaml block, lines 493-597):

- **FR-1 — UC-1 block.** The `# UC-1 specific` block is SKILL.md:503-507 (ends at
  `best_practice_grade` line 507, before `# UC-2 specific` line 509). INSERT after line 507:
  ```yaml
  implementation_coverage_pct: <float 0.0-1.0> | null   # FR-1
  missing_implementations:                              # FR-1
    - abstract_name_path: <string>
      expected_count: <int>
      found_count: <int>
  ```
- **FR-2 / FR-4 / FR-5 — UC-2 block.** The `# UC-2 specific` block is SKILL.md:509-517 (ends at
  `grounding_gaps_path` line 517, before `# Input integrity` line 519). INSERT after line 517:
  ```yaml
  hunk_to_declaration_map_path: <abs path>   # FR-2 (UC-2 only)
  third_party_api_grounding:                 # FR-4
    - api_name: <string>
      dep_version: <string>
      resolution_path: <string>
  third_party_api_verified: <bool>           # FR-4
  serena_summary_corroboration: agree | partial | disagree | unavailable   # FR-5
  ```
  (Spec line 358-365 confirms FR-2/FR-4/FR-5 are all UC-2-block fields.)

**§9.3 Consumer Field Map note:** per §9.3 "Field-deletion guard" (SKILL.md:636) and the
"Adding a field to a consumer's load-bearing row requires a contract version bump" rule
(SKILL.md:622) — these additions are NOT load-bearing for any existing §9.3 consumer row, so no
§9.3 table edit is forced. The minor bump (additive) is the correct §9.4 classification
(SKILL.md:645 "Minor (1.x.0): purely additive...").

---

## 6. SKILL.md §9.2 telemetry — FR-6/7/8 insertion point

**File:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md`

The §9.2 telemetry yaml block is **SKILL.md:603-618** (`### 9.2 Telemetry (non-stable)` at
line 601). The block currently ends with `memory_hits`/`memory_misses` (lines 616-617). INSERT
the FR-6/7/8 fields before the closing fence (line 618), after line 617. Exact fields (spec
lines 370-377):

```yaml
onboarding_status: bootstrapped | not_bootstrapped | unknown   # FR-6
serena_version: "<v1.5" | ">=v1.5" | "unknown"                 # FR-7 (required, three-valued — A4/C2)
serena_config_snapshot_path: <abs path>                        # FR-7
serena_active_context: <string>                                # FR-7
serena_active_modes: [<string>]                                # FR-7
memory_retention_actions: <int>                                # FR-8
memory_retention_skipped_readonly: <int>                       # FR-8
memory_retention_unbounded: <bool>                             # FR-8 (C1 loud-gap flag)
```

CRITICAL (spec line 402, review finding A3): these eight are TELEMETRY (§9.2), NOT contract
(§9.1), so they do NOT participate in the contract_version bump. Do NOT place them in the §9.1
block. The bump (FR-1/2/4/5) and the telemetry additions (FR-6/7/8) are deliberately separated.

NOTE: spec FR-6.2 (line 240) says `onboarding_status` is in "§9.2 telemetry" — confirms placement.
spec FR-8.2 (line 276) says `memory_retention_actions`/`memory_retention_skipped_readonly` are in
"the return contract" — but spec line 376-377 places them under the §9.2 TELEMETRY block header and
line 402 explicitly excludes FR-8 from the contract bump. AUTHORITATIVE: §9.2 telemetry (line 402
wins over the looser "return contract" phrasing in FR-8.2). `memory_retention_unbounded` likewise §9.2.

---

## 7. refs/return-contract.yaml absence — see top of file (CONFIRMED)

Covered in the OQ-5 section at the top: `ls refs/` returns 11 files, none named
`return-contract.yaml`. All §9.1/§9.2 edits target SKILL.md inline.

---

## Summary table (FR → file → line → change)

| FR | File | Line(s) | Change |
|----|------|---------|--------|
| FR-1 | SKILL.md §9.1 UC-1 | after :507 | add `implementation_coverage_pct`, `missing_implementations[]` |
| FR-1 | reflection-rubric.md | after :112 | add S_dev_density missing-implementor sub-term |
| FR-1 | coverage-mapping.md | :94-97 | (conditional) add missing-implementor to UC-1 numerator if it feeds the ratio |
| FR-1/3 | reviewer-spec.md | :33-37 | add find_implementations list + extended-info to `## Grounding hunks` |
| FR-2 | SKILL.md §9.1 UC-2 | after :517 | add `hunk_to_declaration_map_path` |
| FR-4 | SKILL.md §9.1 UC-2 | after :517 | add `third_party_api_grounding[]`, `third_party_api_verified` |
| FR-4 | deviation-taxonomy.md | :44-49 | add `third_party_api_verified` to Necessary Detection signals |
| FR-4 | SKILL.md §10.2 | :693-698 | MIRROR: add same bullet to SKILL.md Necessary signals |
| FR-5 | SKILL.md §9.1 UC-2 | after :517 | add `serena_summary_corroboration` |
| FR-5 | deviation-taxonomy.md | :59-63 | add `serena_summary_corroboration` to Drift Detection signals |
| FR-5 | SKILL.md §10.3 | :708-712 | MIRROR: add same bullet to SKILL.md Drift signals |
| FR-6 | reflection-rubric.md | after :112 | add onboarding-status weight sub-term |
| FR-6 | SKILL.md §9.2 | after :617 | add `onboarding_status` |
| FR-7 | reflection-rubric.md | after :112 | add context-exclusion up-weight sub-term |
| FR-7 | SKILL.md §9.2 | after :617 | add `serena_version`, `serena_config_snapshot_path`, `serena_active_context`, `serena_active_modes` |
| FR-8 | SKILL.md §9.2 | after :617 | add `memory_retention_actions`, `memory_retention_skipped_readonly`, `memory_retention_unbounded` |
| version bump | SKILL.md | :491, :494, :599 | `1.0` → `1.1.0` (3 sites; normalize to 3-segment SemVer) |

**Key disambiguations for task-builder:**
1. `refs/return-contract.yaml` does NOT exist — strike that §5-matrix row (spec line 318); contract edits go to SKILL.md §9.1 inline.
2. FR-6/7/8 are §9.2 TELEMETRY, NOT §9.1 contract — excluded from the version bump (spec line 402 authoritative over FR-8.2 phrasing).
3. deviation-taxonomy.md edits (FR-4/FR-5) MUST be mirrored in SKILL.md §10.2/§10.3 (identical Detection-signals lists) or the two drift.
4. S_dev_density math lives in coverage-mapping.md:89-111, NOT only reflection-rubric.md — spec §5 matrix (line 315) under-specifies; add coverage-mapping.md as conditional FR-1 target if `implementation_coverage_pct` feeds the ratio (spec line 121 implies it does).
5. contract_version current value is 2-segment `1.0`; bump normalizes to 3-segment `1.1.0`.

Status: Complete
