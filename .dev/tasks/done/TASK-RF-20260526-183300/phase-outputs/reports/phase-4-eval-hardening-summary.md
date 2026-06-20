---
phase: 4
title: Eval Hardening and Validation Logic — Change Summary
status: complete
created_date: 2026-05-26
task_id: TASK-RF-20260526-183300
source_files:
  - .dev/eval-workspaces/sc-brainstorm/evals/evals.json
  - .dev/eval-workspaces/sc-brainstorm/grader.py
  - .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py
---

# Phase 4 — Eval Hardening Summary

This report maps every Phase 4 hardening requirement to specific evidence in the edited eval workspace files. Cases 4-11 are the default compared acceptance set; case 12 (`architecture-graphql-public-api`) is INTENTIONALLY EXCLUDED until `Unknown skill: sc:brainstorm-protocol` registry compatibility is brought into scope by a separate decision.

No source-of-truth skill files (`src/superclaude/`) and no `.claude/` mirror files were edited in Phase 4. Eval workspace edits are confined to the three files listed in the frontmatter `source_files`.

## Table 1 — Eval Assertions (`evals.json`)

| Assertion target | Where in `evals.json` | Coverage | Notes |
|------------------|-----------------------|----------|-------|
| **Seed depth** (`expected_depth` per case + `seed_brief_frontmatter_has_depth`) | Per-case `expected_depth` keys added on cases 4-11 with values quick/standard/deep; `assertions_cases_4_11_acceptance.seed_brief_assertions[0]` lists `seed_brief_frontmatter_has_depth` | ✅ | Resolves case 4 quick-vs-standard failure (`comparison-against-iteration-2.json:92-96`) |
| **Seed proposal_count** (`expected_proposal_count` + `seed_brief_frontmatter_has_proposal_count`) | Per-case `expected_proposal_count` preserved; `assertions_cases_4_11_acceptance.seed_brief_assertions[1]` adds explicit assertion | ✅ | Resolves cases 4,6,7,10,11 missing proposal_count failures |
| **Seed interactive_mode** (`expected_interactive_mode` + `seed_brief_frontmatter_has_interactive_mode_when_expected`) | Per-case key added (c10 true, others false); assertion at `seed_brief_assertions[2]` | ✅ | Resolves case 10 interactive tagging failure |
| **Seed blind_mode** (`expected_blind_mode` + `seed_brief_frontmatter_has_blind_mode_when_expected`) | Per-case key added (c11 true, others false); assertion at `seed_brief_assertions[3]` | ✅ | Resolves case 11 blind mode failure |
| **Seed Context Anchors / Intent Summary / Must Preserve / Out of Scope sections** (Phase 2 protocol additions) | `seed_brief_assertions[4-7]` | ✅ | Aligns eval assertions with Phase 2 SKILL.md + socratic-templates.md schema |
| **Merged-requirements frontmatter** spec_type / adversarial_status / proposal_count | `merged_requirements_assertions[0-2]` | ✅ | Resolves case 4 all three failures, case 10 adversarial_status+proposal_count, case 11 `adversarial_status='success'` vs `pass` divergence |
| **Merged-requirements blind_mode** when expected | `merged_requirements_assertions[3]` | ✅ | Resolves case 11 merged blind_mode failure |
| **Merged-requirements Provenance section** (dedicated `## Provenance`) | `merged_requirements_assertions[4]` | ✅ | Resolves repeated failure across cases 4, 7, 8, 10, 11 |
| **Risks section counts tables OR lists** | `merged_requirements_assertions[5]` (`merged_requirements_risks_section_counts_tables_or_lists`) | ✅ | Resolves cases 7, 8, 9 zero-item false negatives caused by table-shaped Risks sections |
| **Merged Functional Requirements / Non-Functional Requirements / fit_to_intent sections** (Phase 2 canonical contract) | `merged_requirements_assertions[6-8]` | ✅ | Aligns with canonical six-section schema |
| **Return contract status_success / domain / proposal_count / agent_spec personas + model aliases / handoff_action** | `return_contract_assertions[0-4]` | ✅ | Resolves cases 4, 6, 8, 11 return-contract failures |
| **Return contract Phase 2 fields**: `seed_schema_version`, `merged_requirements_schema_version`, `context_anchors_count`, `fit_to_intent`, `source_of_truth_paths` | `return_contract_assertions[5-9]` | ✅ | Aligns with Phase 2 return-contract schema additions |
| **Blind labels** (anonymized agent_spec + debate transcript) | `blind_mode_assertions[0-1]` | ✅ | Resolves case 11 Agent A-E label failures |
| **Live timing/token telemetry presence** when in scope | `telemetry_and_quality_assertions[0]` + `telemetry_scope_note` | ✅ | Explicitly scoped: enforced only when timing.json or equivalent is present; absence reported as explicit gap (`status: unavailable`) — never silent pass |
| **Strict quality grading presence** for compared cases | `telemetry_and_quality_assertions[1]` + `strict_quality_scope_note` | ✅ | Explicitly scoped: enforced when `iterations/iteration-2/quality-grading.json` covers cases 4-11; absence reported as `status: unavailable, reason: 'strict quality grading currently covers cases 1-3 only'` |
| **Default case set 4-11** | Top-level `remediation_acceptance_scope: [4,5,6,7,8,9,10,11]` + per-case `acceptance_scope: "remediation"` | ✅ | Codified as explicit metadata, not derived |
| **Intentional case 12 exclusion** | Top-level `remediation_deferred_cases: [12]` + `remediation_case_12_deferral_note` naming registry blocker + per-case `acceptance_scope: "deferred"` + per-case `deferral_reason` | ✅ | Excluded with explicit reason; not silently dropped; assertion block has `case_12_note` re-asserting exclusion |
| **Legacy `assertions_v2` preserved** | Top-level `assertions_v2` array untouched | ✅ | Backwards compatibility — new assertions are ADDITIVE under `assertions_cases_4_11_acceptance`, not replacements |

## Table 2 — Grader Assertion Support (`grader.py`)

| Capability | Where in `grader.py` | Coverage | Notes |
|------------|----------------------|----------|-------|
| **Robust YAML parsing** for nested mappings + lists | `parse_yaml_robust()` (new function) + `_walk_yaml_strings()` helper | ✅ | Stack-of-frames algorithm with deferred list-vs-dict materialization; no PyYAML dependency; correctly extracts `agent_spec.personas` and `agent_spec.models` as lists |
| **Multiline/recursive YAML/text assertions for return contracts** | New assertion type `yaml_contains_any_recursive` in `check_assertion()` — walks parsed YAML structure and searches all string leaves | ✅ | Enables `agent_spec personas include architect` and `model aliases include claude-opus-4-7` checks without the flat-substring fragility |
| **`section_items_or_table_rows`** for Risks/Acceptance/Questions sections | `count_section_items_or_table_rows()` (new function) + new assertion branch | ✅ | Counts enumerated bullets PLUS markdown table data rows (header + separator excluded). Smoke-tested: 3 for table-only, 2 for bullets-only, 4 for mixed |
| **`frontmatter_field_in`** for normalized vocabularies | New assertion branch in `check_assertion()` | ✅ | Case-insensitive `allowed_values` membership; documented to be used ONLY when contract intentionally allows multiple values (do NOT use to paper over schema bugs) |
| **`yaml_field_in`** YAML equivalent | New assertion branch in `check_assertion()` | ✅ | Same scope-discipline note |
| **`text_contains_any`** for non-YAML files | New assertion branch in `check_assertion()` | ✅ | Used for `debate-transcript.md` blind-label checks (`Agent A`/`Agent B` markers) |
| **`text_not_contains_any`** for negative checks | New assertion branch in `check_assertion()` | ✅ | Used for blind-mode anonymization: confirms real persona names (`architect`, `security`) are ABSENT from blind transcripts |
| **Backwards compatibility for existing 9 assertion types** | All existing branches (`file_exists`, `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, `dir_count`) UNCHANGED | ✅ | No behavior change to existing assertions; old `grading.json` output schema `{expectations, summary}` preserved (verified — `build_grading()` and `main()` not edited) |
| **Unknown assertion types fail loudly** | Final `return False, f"Unknown assertion type: {a_type}"` line still reached for any non-matched type | ✅ | New branches added BEFORE the hard-fail line; unknown types still hard-fail |

## Table 3 — Comparison Quality / Telemetry Handling (`compare_live_runs.py`)

| Behavior | Where in `compare_live_runs.py` | Coverage | Notes |
|----------|---------------------------------|----------|-------|
| **Default case set 4-11** | `CASE_IDS = set(range(4, 12))` (unchanged value, now backed by module docstring stating the scope) | ✅ | Pre-existing behavior preserved; intent now documented |
| **Intentional case 12 exclusion** | Module docstring + `EXCLUDED_CASE_IDS = {12}` + `EXCLUDED_CASE_REASON` constants | ✅ | Names the registry blocker (`Unknown skill: sc:brainstorm-protocol`) and warns against broadening `CASE_IDS` without a separate scope decision |
| **Sync validation between script and evals.json** | `_validate_evals_sync()` (new helper) called from `load_evals()` | ✅ | Emits stderr WARNING if `remediation_acceptance_scope` or `remediation_deferred_cases` in evals.json diverges from script constants; smoke-tested for both no-warn and warn paths |
| **Strict-quality comparison for cases 4-11 when artifacts exist** | `quality_score_for()` (pre-existing) reads `iterations/iteration-2/quality-grading.json` | ✅ | Unchanged behavior — returns `{status: 'available', total, scores, rubric_version}` when matching, `{status: 'unavailable', reason: '...'}` when not |
| **Quality unavailable reported as explicit gap** | `summarize()` adds `quality_unavailable_count` + `availability_gaps.quality` ("explicit gap" vs "covered"); markdown writer emits dedicated `### Availability gaps` subsection with normative text | ✅ | Inflation prevention: README-level statement that "unavailable quality and unavailable telemetry MUST NOT be treated as remediation acceptance" |
| **Live timing/token telemetry handling** | `live_timing()` (pre-existing) globs for `timing.json` and returns `{status: 'available', ...}` or `{status: 'unavailable', reason: '...'}` | ✅ | Pre-existing behavior preserved |
| **Telemetry unavailable reported as explicit gap** | `summarize()` adds `telemetry_unavailable_count` + `availability_gaps.timing_tokens`; markdown writer surfaces both available AND unavailable counts | ✅ | Same inflation-prevention discipline as quality |
| **Output paths preserved** | `main()` writes `LIVE_ROOT / "comparison-against-iteration-2.json"` and `.md` (unchanged) | ✅ | Pre-existing output paths intact; no fabrication |
| **Per-case comparison table preserved** | `write_markdown()` per-case table loop UNCHANGED | ✅ | Backwards-compatible markdown structure; only header and summary sections extended |
| **None-mean-pass-rate handling** | `write_markdown()` replaces `.2%` formatter with `"n/a"` fallback when `mean_baseline_pass_rate` / `mean_live_pass_rate` is None | ✅ | Prevents crash when no live cases exist |

## Verification

- `uv run python -c "import json; d=json.load(open('.dev/eval-workspaces/sc-brainstorm/evals/evals.json')); ..."` → JSON_VALID, 12 cases, acceptance_scope [4-11], deferred [12], new assertions block has 5 sub-lists (seed_brief_assertions ×8, merged_requirements_assertions ×9, return_contract_assertions ×10, blind_mode_assertions ×2, telemetry_and_quality_assertions ×2).
- `uv run python -c "import py_compile; py_compile.compile('.dev/eval-workspaces/sc-brainstorm/grader.py', doraise=True)"` → SYNTAX_OK. Imported and smoke-tested: NESTED_LIST_OK (parse_yaml_robust extracts agent_spec.personas as `['architect','security','refactorer']` and agent_spec.models as `['claude-opus-4-7','claude-sonnet-4-6']`), WALK_OK, FLAT_PLUS_LIST_OK, TABLE_ROW_COUNT_OK (3/2/4 for table-only/bullets-only/mixed), FLAT_PARSER_BACKWARDS_COMPAT_OK.
- `uv run python -c "...compare_live_runs..."` → SYNTAX_OK; CASE_IDS=[4..11], EXCLUDED_CASE_IDS=[12]; `_validate_evals_sync()` no warning for in-sync input; expected stderr WARNING for out-of-sync input.
- `grep -c "TODO\|FIXME\|TBD\|XXX"` on all three edited files returns 0.
- `git diff --stat .dev/eval-workspaces/sc-brainstorm/` shows `evals/evals.json +96 lines` and `grader.py +294 lines` (compare_live_runs.py was untracked pre-Phase-4 — see Step 1.0 worktree state — and is now expanded with the new docstring/constants/validation helper/availability-gap fields).
- `git diff --stat src/superclaude/` shows no Phase 4 edits (Phase 2/3 src edits remain from earlier phases).
- `git diff --stat .claude/skills/sc-brainstorm-protocol/ .claude/skills/sc-adversarial-protocol/` shows no Phase 4 edits.
- Cases 4-11 acceptance scope is the same in evals.json (`remediation_acceptance_scope`), compare_live_runs.py (`CASE_IDS`), and the protocol contracts edited in Phase 2 (which require the new schema fields). Case 12 exclusion is documented in all three locations with the same `Unknown skill: sc:brainstorm-protocol` reason.

## Unresolved Blockers

None. All Phase 4 hardening requirements have explicit metadata in `evals.json`, explicit parser/assertion-type support in `grader.py`, and explicit availability-gap reporting in `compare_live_runs.py`. Telemetry assertions are scoped (enforced only when artifacts exist) so this Phase 4 does NOT require the protocol to start writing `timing.json` immediately — that would be a follow-up if telemetry is brought into the acceptance scope; absence remains an explicit availability gap, not a silent pass.
