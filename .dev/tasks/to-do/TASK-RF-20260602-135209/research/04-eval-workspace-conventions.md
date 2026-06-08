# Research: Eval-Workspace Conventions

Topic type: Test & Verification
Scope: `.dev/eval-workspaces/sc-reflect/` — grader.py, aggregate_iteration.py, existing cases/ dirs, expected.yaml schema. Scaffolding the 6 NEW serena-* eval-case dirs (FR-RV3-LOW.1–8, spec §4.1/§8.1).
Status: Complete
Date: 2026-06-02

---

## 0. CRITICAL FINDING — where assertions actually live (read this first)

There are **two distinct artifacts** and the builder must not conflate them:

1. **`cases/<name>/expected.yaml`** — a **human-readable contract document**. Free-form
   YAML describing the case's expected outcome (mode, use_case, deviation_counts,
   per_task_verdicts, etc.). The grader **does NOT read these**. They are documentation
   that a downstream iteration uses to author the machine assertions. Every existing one
   is a `# STUB` (e.g. `cases/post-small-diff-clean/expected.yaml:1`).

2. **`evals/evals.json`** — the **machine-graded assertion registry**. Each eval object
   carries an `assertions: [...]` array whose elements are the grader's assertion dicts
   (`type`, `target`, `field`, `expected`, ...). At runtime the harness copies each eval's
   `assertions` into a per-iteration `eval-<name>/eval_metadata.json`; `grader.py` reads
   **`eval_metadata.json`** (grader.py:414-420; `aggregate_iteration.py` `build_benchmark`
   reads `eval_dir / "eval_metadata.json"`), NOT `expected.yaml`, NOT `evals.json` directly.

So **"author the expected.yaml assertions"** in this task means TWO deliverables per case:
- write `cases/<name>/expected.yaml` (human contract — STUB-acceptable shape), **and**
- add an eval object with an `assertions[]` array to `evals/evals.json` (the graded surface).

NFR-2's phrasing ("grader `yaml_field` assertion over audit.log + return contract") maps to
**`assertions[]` entries of `type: yaml_field`** in `evals/evals.json`, NOT to `expected.yaml`
keys. Evidence: NFR-RV3-LOW.2 at `04-spec-low-complexity.md:432`; grader dispatch at
`grader.py:336-346`.

`eval_metadata.json` is generated per-iteration (no committed copy exists — `find . -name
eval_metadata.json` returns nothing in the source tree). **Scaffolding a case does NOT
require generating it.**

---

## 1. Case-dir structure (from 3 existing cases)

Workspace root: `.dev/eval-workspaces/sc-reflect/`. Two case shapes exist:

**UC-2 (post-execution) case** — e.g. `cases/post-small-diff-clean/`, `cases/post-large-diff-mixed/`:
```
cases/<name>/
├── expected.yaml          # human contract doc (STUB header line 1)
└── input/
    ├── diff.patch         # unified git diff (the "completed work" under audit)
    └── tasklist.md        # the tasklist the work was supposed to fulfil
```

**UC-1 (pre-execution) case** — e.g. `cases/pre-trivial-coverage-gap/`:
```
cases/<name>/
├── expected.yaml          # human contract doc (STUB header line 1)
└── input/
    ├── spec.md            # requirements spec (R-001..R-NNN)
    └── tasklist.md        # the proposed tasklist to validate FOR COVERAGE vs spec
```

**Input-file shapes** (content shape, not full content):
- `input/diff.patch` — real `diff --git a/... b/...` hunks with `@@` line ranges. Each hunk
  maps to a tasklist item. `post-large-diff-mixed/input/diff.patch` (47 lines) deliberately
  plants 1 regression + 2 drift + 1 necessary + 1 authorized hunk. STUB header at line 1
  (`# STUB — iteration-1 follow-up...`). (`cases/post-small-diff-clean/input/diff.patch:1-38`)
- `input/tasklist.md` — bulleted `- Task N: <imperative>` lines, one per diffed file/hunk.
  UC-1 tasklists annotate `(covers R-00X)`; deliberately omit some R-IDs to create a coverage
  gap. (`cases/pre-trivial-coverage-gap/input/tasklist.md:5-10`)
- `input/spec.md` (UC-1 only) — `- R-NNN: System SHALL ...` requirement bullets under a
  `## Requirements` heading. The grader's `matrix_covers_items` parser reads `items` from a
  YAML source, but the existing UC-1 case points `source: input/spec.md` (markdown) — see §3
  note on that mismatch. (`cases/pre-trivial-coverage-gap/input/spec.md:5-14`)

**Other case shape — single-file YAML cases** (NOT dir-based): the `promotion/` and
`falsifier-suite/` cases are single `.yaml` files referenced via `case_file:` (not `case_dir:`)
in evals.json. The 6 new serena cases are **dir-based** (`case_dir:`), matching the pilot
UC-1/UC-2 pattern, per spec §4.1 which lists trailing-slash directory paths
(`04-spec-low-complexity.md:299-304`).

---

## 2. expected.yaml schema (full field list across cases)

`expected.yaml` is free-form; fields vary by mode. Observed union across the 3 pilot cases:

| Field | Cases | Meaning |
|-------|-------|---------|
| `mode` | all | `pre` (UC-1) or `post` (UC-2) |
| `use_case` | all | `UC-1` or `UC-2` |
| `coverage_pct` | UC-1 | float 0-1 expected coverage |
| `total_requirements` / `covered_requirements` | UC-1 | int counts |
| `missing_requirements` | UC-1 | list of R-IDs expected uncovered |
| `escalation_reason` | both | `null` or e.g. `regression_present` |
| `report_must_mention` | UC-1 | strings the REPORT must contain |
| `deviations` / `deviation_counts` | UC-2 | `{authorized, necessary, drift, regression}` int map |
| `tier_reached` | both | 1 / 2 / 3 |
| `regression_recall` / `regression_recall_min` | UC-2 | float |
| `calibrated_confidence_min` | both | float floor |
| `per_task_verdicts` | UC-2 | `[{task_id, verdict, hunk_id?}]` |
| `remediation_recommendation` | UC-2 | `required` / etc. |

**Representative quote** (`cases/post-large-diff-mixed/expected.yaml:3-30`):
```yaml
mode: post
use_case: UC-2
deviation_counts:
  authorized: 1   # Task 14 StatsD addition
  necessary: 1    # Task 11 PKCE verifier expansion
  drift: 2        # Task 7 process-pool vs thread-pool; Task 9 capacity 512 vs 128
  regression: 1   # Task 5 changes public API return shape silently
tier_reached: 3   # Regression class triggers unconditional Tier 3 per §10.4
escalation_reason: regression_present
calibrated_confidence_min: 0.80
regression_recall_min: 0.85
per_task_verdicts:
  - task_id: 5
    verdict: regression
    hunk_id: users-list-shape
  ...
remediation_recommendation: required
```

For the serena cases this document captures the **expected telemetry/contract values**
(e.g. `find_implementations_invoked: true`, `serena_version: ">=v1.5"`) in human-readable
form. The machine truth is the evals.json assertion array (§3).

---

## 3. grader.py — assertion vocabulary (the `yaml_field` mechanism + all 18 types)

`grader.py` is the dispatcher. Each assertion is a dict with a `type` and type-specific keys.
The dispatch table is `check_assertion(assertion, base_dir)` at **grader.py:294-408**.
`base_dir` is the `eval-<name>/` directory; `target` paths are relative to it (the grader
prepends `with_skill/` or `old_skill/` via the `target` prefix — see grader.py:422-423).

### The `yaml_field` mechanism (NFR-2's primary surface) — grader.py:336-346

```python
if a_type == "yaml_field":
    content = read_text(target_path)
    y = parse_yaml_simple(content)         # FLAT parser — grader.py:58-77
    field = assertion["field"]
    expected = str(assertion["expected"])  # coerced to string
    actual = y.get(field, "")
    if actual == expected: PASS
```

A case declares "assert field X present with value Y" as:
```json
{ "type": "yaml_field",
  "target": "with_skill/outputs/audit.log",
  "field": "find_implementations_invoked",
  "expected": "true",
  "text": "<human description>" }
```
**Three gotchas the builder MUST encode:**
1. `parse_yaml_simple` (grader.py:58-77) is a **flat, top-level-only** parser: it skips any
   line starting with a space (`line.startswith(" ")` → `continue`, grader.py:71). So
   `yaml_field` can only assert **top-level scalar keys**. Nested fields (e.g.
   `missing_implementations[].found_count`) need `yaml_list_contains` or `regex_present`.
2. `expected` is compared as a **string** (`str(...)`, grader.py:343). `expected: "true"`,
   `expected: "1"` — booleans/ints must be quoted strings in the assertion.
3. `target` must start with `with_skill/` or `old_skill/` or the assertion is dropped from
   both buckets (grader.py:422-423 partition on prefix).

### Full assertion vocabulary (18 types) — grader.py + evals.json `grading_criteria`

8 baseline (inherited from sc-brainstorm) — grader.py:300-384:
- `file_exists` {target}
- `frontmatter_field` {target, field, expected} — case-insensitive
- `section_present` {target, section_pattern}
- `section_enumerated` {target, section_pattern, min_items}
- **`yaml_field`** {target, field, expected} — top-level scalar string-equality
- `yaml_field_min` {target, field, min_value} — numeric ≥
- `yaml_substring` {target, field, substring_any:[...]}
- `dir_count` {target, min_files}

10 extensions — grader.py:387-406 (helpers 120-286):
- `citation_resolves` {report, fixture_root, expected_snippets?} — every `file:line` in the
  report resolves against fixture_root ±5-line window (grader.py:120-149)
- `regex_present` {target, pattern} — MULTILINE|DOTALL (grader.py:152-159)
- `regex_absent` {target, pattern} (grader.py:162-169)
- `yaml_list_contains` {target, field_path, value} — **proper `yaml.safe_load`**, dotted
  path with int-index support; asserts `value in list` (grader.py:172-187). **This is how a
  case asserts a NESTED field** (e.g. `field_path: degraded_components`, `value:
  find_implementations:lsp_unsupported`).
- `matrix_covers_items` {matrix, source, threshold} — coverage ratio ≥ threshold
  (grader.py:190-209)
- `checkpoint_logged` {audit_log, checkpoint_name} — JSONL audit row with
  `checkpoint == name` (grader.py:212-229)
- `deviation_class_matches` {annotated_fixture, report, diff_hunk_id} — compares expected vs
  reported `deviation_class` for a hunk (grader.py:232-248)
- `path_exists` {target} (grader.py:251-258)
- `path_does_not_exist` {target} (grader.py:261-267)
- `falsifier_skeleton_present` {case_yaml} — accepts `status:
  skeleton-pending-iteration-3-fixture` (grader.py:270-286)

Unknown type → `(False, "Unknown assertion type")` (grader.py:408). All 18 are enumerated in
`evals/evals.json` `grading_criteria[]` — adding a new type would require editing grader.py,
which **none of the 6 serena cases need** (yaml_field + yaml_list_contains + regex_present +
file_exists + citation_resolves cover everything).

### audit.log telemetry vs return-contract — both via the same assertion types

The grader is **file-agnostic**: it does not distinguish "telemetry" from "contract". Both are
just `target` files holding YAML/text. A case asserts:
- **telemetry** (`audit.log`) — `yaml_field` over the audit row, OR `checkpoint_logged` /
  `regex_present` if the row is JSONL/nested. Note `audit.log` is **JSONL** in the grader's
  `checkpoint_logged` helper (grader.py:218-226 `json.loads(raw)` per line). For flat
  `<tool>_invoked: true` telemetry the spec's FR criteria phrase it as a YAML field, so a
  flat `audit.log`-derived YAML (e.g. `outputs/audit-summary.yaml`) or `regex_present` over
  the JSONL is the robust target. **Recommend `regex_present` against `audit.log` for
  `<tool>_invoked` fields** to avoid the flat-parser limitation.
- **return contract** (`outputs/contract.yaml`) — `yaml_field` for top-level scalars
  (`tier_reached`, `serena_version`, `third_party_api_verified`), `yaml_list_contains` for
  nested (`third_party_api_grounding[].api_name`, `missing_implementations[]`).

**"find_implementations_invoked: true on BOTH success AND degraded path"** is expressed as
**two separate eval objects** (or two assertions in one eval, pointed at two different
`with_skill/outputs/` fixtures representing the two runs) — the grader has no notion of
"path"; you encode each path as a distinct output fixture and assert against each. The
existing pattern: one eval = one fixture-run = one assertion set. So success-path and
degraded-path become **two eval-case dirs OR two `with_skill/outputs/` snapshots**. For
scaffolding, the simplest valid encoding is **one eval per FR with the success-path
assertions, plus a `regex_present`/`yaml_field` degraded assertion pointing at a
`degraded`-flavored fixture** the case authors alongside.

---

## 4. aggregate_iteration.py — how case results aggregate (brief)

`aggregate_iteration.py` runs AFTER grading. `build_benchmark(iter_dir)` globs `eval-*/`,
reads each `eval_metadata.json` for `eval_id`, then `run_record()` reads
`<config>/run-1/grading.json` + `timing.json` and produces per-run pass_rate/tokens/time.
It groups by `old_skill` / `with_skill`, computes mean/stddev (`summarize`), and writes
`benchmark.json` + `benchmark.md` + `review.html`. **Relevance to authoring a case: none
beyond requiring each eval to have a unique integer `eval_id`** (used as the sort/group key,
`aggregate_iteration.py` `build_benchmark`). The new serena cases need `id: 21..26+` in
evals.json (existing ids run 1-20). No other aggregation coupling.

---

## 5. What "scaffold a case" minimally requires (deliverable 7)

These cases are **scaffolded, not executed** (no full grader run, no `with_skill/outputs/`
produced by an actual reflect run). A scaffolded case is **valid** when:

1. **Case dir exists** at `cases/<name>/` (spec §4.1 path, trailing slash).
2. **`input/` fixtures exist** and parse: UC-2 → `diff.patch` + `tasklist.md`; UC-1 →
   `spec.md` + `tasklist.md`. (FR-specific extras noted per-case below.) STUB header line 1
   matching the existing convention (`# STUB — ...`) is acceptable for fixture bodies, but
   the fixture must contain enough structure for the assertion to be authorable (e.g. an
   abstract symbol for FR-1; an `<ext:...>`-resolving import for FR-4).
3. **`expected.yaml` exists** with at least `mode` + `use_case` + the FR's expected
   telemetry/contract values as human-readable keys (STUB-acceptable, like the 3 pilots).
4. **An eval object is appended to `evals/evals.json`** with: unique integer `id`, `name`,
   `case_dir`, `mode`, `use_case`, `spec_ref` (FR id), `description`, `inputs{}`, `expected:
   "expected.yaml"`, and an `assertions: [...]` array of well-formed grader dicts (each with
   a `type` in `grading_criteria` and a `text`). The assertion `target`s point at
   `with_skill/outputs/...` paths that a FUTURE run will produce — they need not exist now.
5. **All assertion `type`s already exist in grader.py** (no grader edit needed — verified
   against grader.py:294-408 for all 6 cases below).

A scaffolded case is NOT required to: generate `eval_metadata.json`, produce
`with_skill/outputs/`, run `grader.py`, or pass. (`yaml_field` etc. would simply report
"File not readable" until a real run populates outputs — expected for a scaffold.)

The builder should also confirm `evals.json` top-level `iteration`/`scope`/`notes` are
updated to mention the new cases (the existing `notes` documents pilot/promotion/falsifier
scope; appending serena scope keeps the registry self-describing — non-blocking but
house-style).

---

## 6. Per-case scaffold spec (the 6 NEW cases) — builder turns each row into items

Sources: spec §4.1 (`:299-304`), §8.1 Validates column (`:457-463`), §5 audit fields
(`:400`), §4.5 contract/telemetry (`:350-378`), per-FR acceptance criteria (`:144-287`).
`audit.log` `<tool>_invoked` fields → use `regex_present` (JSONL/flat-parser safe);
`outputs/contract.yaml` top-level scalars → `yaml_field`; nested contract lists →
`yaml_list_contains`.

### Case 1 — `serena-find-implementations` (FR-1, UC-1)
- **FR / mode**: FR-RV3-LOW.1 / UC-1 (coverage audit of an abstract symbol).
- **input fixture shape**: `spec.md` referencing an **abstract symbol** (Interface/Protocol/
  Class) whose polymorphic surface a coverage audit must enumerate; `tasklist.md`. Add a
  **misreported-trait fixture** (LSP kind `Class` that is actually a trait, FR-1.5/C3) and an
  **LSP-error fixture** path for the degraded assertion (FR-1.4).
- **key assertions** (§8.1 "find_implementations_invoked emitted; interface-coverage Drift
  caught; LSP-unsupported fallback"):
  - `file_exists` `with_skill/outputs/REPORT.md`
  - `regex_present` audit.log `find_implementations_invoked.*true` (FR-1.1)
  - `regex_present` audit.log for `implementations_found` + `unmapped_implementations` (FR-1.2)
  - `yaml_field`/`yaml_list_contains` contract `implementation_coverage_pct` + nested
    `missing_implementations[]` (FR-1.3)
  - degraded path: `yaml_list_contains` `degraded_components` ∋ `find_implementations:lsp_unsupported` (FR-1.4)
  - degenerate no-op: `yaml_field` `implementation_coverage_pct: null` + `find_implementations_invoked: false` when no eligible symbol (FR-1.6/C5)

### Case 2 — `serena-find-declaration` (FR-2 + FR-3 shared, UC-2)
- **FR / mode**: FR-RV3-LOW.2 / UC-2 (diff-hunk anchoring). **FR-3 shares this dir** per §8.1
  line 459 (`serena-referencing-extended-info` case → same dir).
- **input fixture shape**: `diff.patch` with hunks whose identifiers have a **name collision**
  (two symbols same name, different scope) to prove 1B.3 anchors to resolved declaration not
  text (FR-2.4); `tasklist.md`. Include a hunk with **no resolvable declaration** for the
  `find_declaration_no_match` assertion (FR-2.2).
- **key assertions** (§8.1 "diff-hunk anchoring; find_declaration_no_match recorded; no
  name-collision false positives; FR-3 references_extended_info_used emitted; Wave 0 inventory
  probe"):
  - `regex_present` audit.log `find_declaration_invoked.*true` (FR-2.1)
  - `regex_present` audit.log `declaration_resolutions` + `find_declaration_no_match` (FR-2.2)
  - `yaml_field` contract `hunk_to_declaration_map_path` present (FR-2.3)
  - `regex_absent` REPORT.md for name-collision false-positive overlap edge (FR-2.4)
  - `regex_present` audit.log `references_extended_info_used.*true` (FR-3.1)
  - `regex_present` audit.log Wave-0 tool-inventory note re `find_referencing_code_snippets` (FR-3.2)

### Case 3 — `serena-search-deps` (FR-4, UC-2)
- **FR / mode**: FR-RV3-LOW.4 / UC-2 (third-party API grounding). Depends on FR-2 output.
- **input fixture shape**: `diff.patch` + `tasklist.md` where a symbol resolves to an
  **`<ext:...>` path** (third-party dep import) — the deterministic trigger (spec §FR-4
  trigger predicate, `:201`). Include an **un-indexed-venv** scenario for the degrade path
  (FR-4.4).
- **key assertions** (§8.1 "search_deps_invocations≥1; third_party_api_grounding populated;
  un-indexed-venv degrade"):
  - `regex_present` / `yaml_field_min`-style audit.log `search_deps_invocations` ≥ 1 (FR-4.1)
  - `regex_present` audit.log `external_symbols_resolved` + `external_resolution_failures` (FR-4.2)
  - `yaml_list_contains` contract `third_party_api_grounding[].api_name` populated + `yaml_field` `third_party_api_verified` (FR-4.3)
  - degraded: `yaml_list_contains` `degraded_components` ∋ `search_deps:lsp_unindexed` + claim stays `[INFERRED]` via `regex_present` REPORT.md (FR-4.4)

### Case 4 — `serena-wave0-config` (FR-6 + FR-7, UC-1 or UC-2)
- **FR / mode**: FR-RV3-LOW.6 + FR-RV3-LOW.7 / either UC (Wave 0 is mode-agnostic). Pick UC-2
  to keep one fixture style; `diff.patch` can be minimal.
- **input fixture shape**: minimal `diff.patch` + `tasklist.md`. The discriminating signal is
  **Serena config state**, expressed via the expected `outputs/` the case documents: an
  active context that **excludes** a chain-critical tool (`get_diagnostics_for_file`) for the
  context-exclusion assertion (FR-7.3), plus an `activate_project`-message variant for
  onboarding parse (FR-6.1).
- **key assertions** (§8.1 "onboarding parse (no defunct tool); config snapshot;
  context-exclusion → degraded_components; version fingerprint"):
  - `regex_present` audit.log `serena_context` + `serena_modes` + `serena_tool_count` + `serena_excluded_tools` (FR-7.1)
  - `path_exists`/`file_exists` `with_skill/outputs/serena-config-snapshot.yaml` + `yaml_field` contract `serena_config_snapshot_path`/`serena_active_context` (FR-7.2)
  - `yaml_list_contains` `degraded_components` ∋ `serena:context-excluded` (FR-7.3)
  - `yaml_field` contract `serena_version` ∈ {`<v1.5`,`>=v1.5`,`unknown`} present (three-valued, FR-7.4)
  - `regex_present` audit.log `onboarding_status` + `onboarding_status_source` (FR-6.1)
  - **`frontmatter_field` / `regex_absent`** static guard: `allowed-tools` in SKILL.md does
    NOT contain `check_onboarding_performed` (FR-6.3) — note this is a static assertion
    against the SKILL.md frontmatter, distinct from runtime output.

### Case 5 — `serena-memory-retention` (FR-8, UC-2)
- **FR / mode**: FR-RV3-LOW.8 / UC-2 (Wave 5 retention sweep). Depends on FR-7 version gate.
- **input fixture shape**: `diff.patch` + `tasklist.md`, plus a documented **pre-existing
  memory set** of >20 deletable slug-prefixed entries + some read-only-pattern-matched
  entries (the case `expected.yaml` describes the memory inventory the run operates on; the
  fixture encodes it as a seed-memory list the run reads). Include a **slug-migration**
  scenario (rename) and a **pre-v1.5** version scenario.
- **key assertions** (§8.1 ">20-entry prune; rename_memory ref-propagation; pre-v1.5
  write-only fallback; readonly skip"):
  - `regex_present` audit.log `memory_retention_sweep_invoked.*true` + `memories_deleted`/`memories_renamed`/`memories_edited` (FR-8.1)
  - `yaml_field` contract `memory_retention_actions` + `memory_retention_skipped_readonly` (FR-8.2/8.5)
  - `regex_present` proof `rename_memory` used (not delete+write) + `mem:` refs resolve (FR-8.3)
  - degraded: `yaml_list_contains` `degraded_components` ∋ `serena:pre-v1.5-no-rename-propagation` on `serena_version ∈ {<v1.5,unknown}` (FR-8.4)
  - loud-gap: `yaml_field` `memory_retention_unbounded: true` + WARN in audit.log when read-only dominates (FR-8.6/C1)
  - degenerate: `regex_present` all-zero counts + `sweep_invoked: true` on empty first-run set (FR-8.7/C4)

### Case 6 — `serena-summarize-changes` (FR-5, UC-2; pilot)
- **FR / mode**: FR-RV3-LOW.5 / UC-2 (drift corroboration; prompt-based; ship-last pilot).
- **input fixture shape**: `diff.patch` + `tasklist.md` where the **Serena summary names a
  file absent from the supplied diff** (and vice-versa) to feed Drift/Necessary sets (FR-5.3).
  Plus a **cross-session** scenario (reflect in fresh session) for the `unavailable` path
  (FR-5.4). Expected runtime artifact: `<output>/serena-change-summary.md`.
- **key assertions** (§8.1 "UC-2 corroboration; cross-session → unavailable"):
  - `regex_present` audit.log `summarize_changes_invoked.*true` + `file_exists`-style assertion that `summarize_changes_path` points at `outputs/serena-change-summary.md` (FR-5.1)
  - `yaml_field` contract `serena_summary_corroboration` ∈ {agree,partial,disagree,unavailable} (FR-5.2)
  - `regex_present` REPORT.md: summary-only files feed §10.3 Drift / §10.2 Necessary set (FR-5.3)
  - cross-session: `yaml_field` `serena_summary_corroboration: unavailable` + main verdict unchanged (FR-5.4)

### Coverage cross-check (case → FR)
| Case dir | FRs covered | UC | spec §4.1 | spec §8.1 |
|----------|-------------|----|-----------|-----------|
| serena-find-implementations | FR-1 | UC-1 | :299 | :457 |
| serena-find-declaration | FR-2 (+FR-3 shared) | UC-2 | :300 | :458-459 |
| serena-search-deps | FR-4 | UC-2 | :301 | :460 |
| serena-wave0-config | FR-6, FR-7 | UC-1/2 | :302 | :462 |
| serena-memory-retention | FR-8 | UC-2 | :303 | :463 |
| serena-summarize-changes | FR-5 | UC-2 | :304 | :461 |

**Note**: 6 case dirs cover all 8 FRs (FR-3 shares the find-declaration dir; FR-6+FR-7 share
wave0-config). This matches spec §4.1's 6 listed dirs and §8.1's 7 test rows (the 7th being
FR-3 sharing dir 2).

---

## 7. Builder item decomposition guidance (granularity)

Each case → at minimum **3 items** (matching the scaffold-validity criteria in §5):
1. Create `cases/<name>/input/` fixtures (FR-specific shapes per §6).
2. Author `cases/<name>/expected.yaml` (human contract with FR's expected telemetry/contract values).
3. Append the eval object + `assertions[]` to `evals/evals.json` (unique `id`, `case_dir`,
   FR `spec_ref`, the §6 assertions).

These are **not** in `src/superclaude/` — `.dev/eval-workspaces/` is committed source but
NOT sync-dev'd (no SoT mirror), so the CLAUDE.md `src/ → make sync-dev → .claude/` rule does
**not** apply to eval-workspace edits. (Verified: eval-workspace lives under `.dev/`, outside
`src/superclaude/` and `.claude/`.)

Optional 4th item across all cases: update `evals/evals.json` top-level `iteration` + `scope`
+ `notes` to register the serena case batch (house-style, non-blocking).

---

Status: Complete
