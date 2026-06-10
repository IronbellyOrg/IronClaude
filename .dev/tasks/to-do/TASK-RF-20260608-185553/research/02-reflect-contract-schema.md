# Research: Reflect return-contract.yaml Schema

**Status:** Complete
**Date:** 2026-06-08
**Scope:** Data dictionary of every field reflect writes into `<output>/return-contract.yaml`. The `superclaude reflect run` wrapper parses exactly this file to derive its verdict (FR-5) and detect degradation (FR-11). This doc covers the DATA SHAPE (names, types, enums, source file:line, written-when). R08 owns which VALUE routes to which verdict.

---

## 0. TL;DR — pinned facts the wrapper must encode

| Fact | Value | Source |
|------|-------|--------|
| **Authoritative contract_version** | `"1.3.0"` (quoted string) | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:651`, `:654`, `:791` |
| **VERSION DRIFT (flag)** | `refs/report-template.md:14` still shows `contract_version: 1.2.0` (unquoted, older). The REPORT.md *human header* skeleton lags the §9.1 stable contract. The wrapper MUST trust §9.1's `1.3.0`, parsed from `return-contract.yaml`, NOT report-template.md's `1.2.0`. | `refs/report-template.md:14` vs `SKILL.md:654` |
| **File the wrapper parses** | `<output>/return-contract.yaml` (written AND returned inline) | `SKILL.md:649` |
| **gate_evaluation 11-field struct lives in a DIFFERENT file** | `<output>/promotion-log.yaml`, NOT `return-contract.yaml`. `return-contract.yaml` carries `promotion_*` scalar fields instead (§9.1 lines 776-788). See §5 below. | `SKILL.md:1454-1489`; `refs/promotion-adapters.md:154` |
| **Contract has two blocks** | §9.1 **stable** (load-bearing, version-governed) + §9.2 **telemetry** (non-stable, `degraded_components` lives HERE) | `SKILL.md:647-651`, `:793` |
| **Unknown-field tolerance (NFR-8 / §9.4)** | Consumers MUST read-and-ignore unknown top-level fields; minor bumps are additive-only. A parser that fails on an unknown field is non-conforming. | `SKILL.md:863`, `:881` |
| **`contract_version` gating (FR-5)** | `1.x` tolerant; unknown MAJOR (e.g. `2.x`) → `blocked` fail-loud. Patch/minor are forward-compatible. | spec `merged-requirements.md:25`, `:133`; `SKILL.md:862-864` |

**Version-drift note for the wrapper:** if the wrapper ever reads the REPORT.md header instead of return-contract.yaml, it will see `1.2.0` and could mis-gate. Parse `return-contract.yaml` only. The `1.2.0` in report-template.md is documentation lag, not a second contract.

---

## 1. Verbatim §9.1 stable contract block

This is the authoritative YAML the wrapper parses, quoted verbatim from `SKILL.md:653-789` (`### 9.1 Stable contract (contract_version: 1.3.0)`):

```yaml
contract_version: "1.3.0"
status: success | partial | failed | dry-run
mode: pre | post
tier_reached: 1 | 2 | 3
report_path: <abs path to REPORT.md>
audit_log_path: <abs path>
confidence_calibrated: <float 0.00-1.00>
escalation_rule_matched: <int 1-8> | null
onboarding_ran: <bool>                # FR-2 (Wave 0.7b one-shot --onboard bootstrap; false when gated off)

# UC-1 specific
coverage_pct: <float 0.0-1.0> | null
coverage_undefined: <bool>           # true when no parseable requirement IDs
unmapped_requirements: [<list>]
best_practice_grade: <int 0-5> | null
implementation_coverage_pct: <float 0.0-1.0> | null   # FR-1 (null when the kind-guard never fired — C5)
missing_implementations:                              # FR-1
  - abstract_name_path: <string>
    expected_count: <int>
    found_count: <int>
hierarchy_slice_path: <abs-path> | null               # FR-RV3-MED.1 (<output>/artifacts/hierarchy-slice.yaml; null when unavailable)
hierarchy_coverage_pct: <float 0.0-1.0> | null        # FR-RV3-MED.1 = registered_subtypes / total_subtypes_in_hierarchy; null when hierarchy empty or backend unavailable

# UC-2 specific
tasklist_completion_pct: <float 0.0-1.0> | null
deviation_count_by_class:
  authorized: <int>
  necessary: <int>
  drift: <int>
  regression: <int>
deviation_register_path: <abs path> | null
grounding_gaps_path: <abs path> | null    # parallel artifact for evidence-insufficient findings
hunk_to_declaration_map_path: <abs path>   # FR-2 (UC-2 only)
third_party_api_grounding:                 # FR-4
  - api_name: <string>
    dep_version: <string>
    resolution_path: <string>
third_party_api_verified: <bool>           # FR-4
serena_summary_corroboration: agree | partial | disagree | unavailable   # FR-5
verification_ran: <bool>                   # FR-4 (UC-2 verification triangle, §6.1 step 5.5)
verification_invocations: <int>            # FR-4 (count of verify-log invocation entries)
verification_failures: <int>               # FR-4 (exit_code != 0 count)
verification_regressions_detected: <int>   # FR-4 (taxonomy-classified Regression exits on a claimed-passing file)
verification_skip_reason: tool-unavailable|read-only-project|--no-verify|null   # FR-4

# Reuse-Miss neighbour sweep (FR-REUSE; UC-2). NO deviation_count_by_class.reuse_miss key (§17.7).
reuse_sweep_ran: <bool>
reuse_audit_path: <abs path> | null
reuse_miss_blocking: <int>                    # rung-L3 findings mapped to Drift/Regression (§10.8)
reuse_miss_advisory: <int>                    # rung ≤ L2 (non-gating)
reuse_verdict_count_by_type: { reuse_by_import: <int>, mirror_shape: <int>, extract_shared: <int>, distinct: <int> }
reuse_grounding_gap_count: <int>
neighbour_search_sampled: <bool>
neighbour_search_degraded: <bool>             # auggie-unavailable fallback used
max_overlap_score: <float 0.0-1.0> | null

# Input integrity
input_sha256:                         # legacy single-file hashes preserved for backward-compat
  tasklist: <hex>
  spec: <hex> | null
input_tree_sha256: <hex>              # AUTHORITATIVE: tree-hash over every input file
input_tree_file_count: <int>
input_tree_snapshot_path: <abs path>  # <output>/artifacts/input-snapshot.yaml
input_drift_detected: <bool>          # true if input_tree_sha256 mismatch at Wave 5 OR Wave 7 step 7.2
input_drift_diff: [<list of {path, old_sha, new_sha, change_kind: added|removed|modified}>] | null

# Hallucination guard
citations_total: <int>
citations_revalidated: <int>          # M; size of the re-Read subset; equals citations_total in full_reread mode
citations_dropped: <int>              # >0 forces status: partial; in sampled mode this is the SAMPLE COUNT (§11.5)
citations_dropped_extrapolated: <int> # population projection in sampled mode; recording-only, does NOT gate promotion
citations_inferred: <int>             # [INFERRED]-tagged; does not force partial
citation_budget_policy: full_reread | sampled
evidence_validator_ran: bool
citation_revalidation_at_promotion: bool   # true when Wave 7 step 7.2 re-Read cited files (Wave 6 ran)

# Tier 2 artifacts
reviewer_cards: [<list of paths>] | []
adversarial_artifacts_dir: <path> | null
adversarial_convergence_score: <float> | null
adversarial_unavailable: <bool>      # F3 path
merge_method: adversarial | single-reviewer-fallback   # F2 path
t2_model_class_diversity: full | degraded
t2_vendor_diversity: multi | single   # warn-only in v1.0
t2_effective_diversity: full | model-only | vendor-only | none   # derived
calibrator_diversity: full | degraded

# Tier 3
remediation_offered: bool
remediation_accepted: bool | null
task_file_path: <path> | null
handoff_memory_key: <serena-memory-name> | null   # FR-3

# Asymmetric-cost flags (downstream automation must respect these)
cannot_validate_without_user_input: bool
regression_present: bool                   # FR-4: verified-sourced from §6.1 step 5.5 exit-code taxonomy
unauthorized_deviation_present: bool
blocked_by_low_confidence: bool
spec_is_wrong: bool                        # UC-2 — code is correct, spec contradicts on-disk reality
user_decision_required: bool               # convergence < threshold AND no auto-route applies
needs_human_decision: bool                 # grounding-gaps.yaml non-empty

# Per-task verdict array (P1 + P2) — populated when UC-2 input is a multi-task tasklist
per_task_verdicts:                       # empty list for UC-1 or single-task UC-2
  - task_id: <string>
    status: success | partial | failed
    deviation_class: authorized | necessary | drift | regression | none
    citations_dropped: <int>
    per_task_validation_strength: <float 0.00-1.00>   # P2: calibrated, post-evidence-validator
    evidence_anchor: <abs path or task-log ref>

# Cross-task interaction-effects (P3) — UC-2 tasklist-scope only
interaction_effects_scanned: bool
interaction_effects_findings: <int>

# Budget pre-flight (P5)
budget_forced_tier_downgrade: bool
budget_forced_stop: bool
budget_check_skipped: bool
forced_tier: 1 | 2 | null

# Promotion (UC-2 only — §14.5)
promotion_action: moved | skipped | rejected | failed | already-promoted | resumed | dry-run | not-applicable
promotion_adapter: task | sprint-release | none | null
promotion_source: <abs path> | null
promotion_destination: <abs path> | null
promotion_log_path: <abs path> | null
promotion_gate_passed: bool | null         # null when mode == pre or Wave 7 skipped pre-gate
promotion_skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
promotion_fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
promotion_override_used: --promote-anyway | --promote-resume | null
promotion_rollback_command: <string> | null
promotion_checkpoint_path: <abs path> | null
promotion_cross_fs: bool
promotion_pending: bool
```

Field-count note: §9.3 (`SKILL.md:840`) states the stable contract has **60+ fields**. The §9.4 evolution rule (`SKILL.md:858-864`) governs which mutations bump major vs minor.

---

## 2. LOAD-BEARING field catalog — fields the wrapper's verdict map (spec §6) + FR-11 degradation checklist consume

Legend for **written-when**: `always` = every run; `UC-2` = post-mode only; `T2` = only when Tier 2 ran; `cond.` = conditional on the documented trigger. All citations are to `SKILL.md` unless noted.

### 2.1 Top-level verdict drivers (spec §6 verdict map at `merged-requirements.md:79-83`)

| Field | Type / enum | Meaning | Source file:line | Written-when |
|-------|-------------|---------|------------------|--------------|
| `contract_version` | `string` literal `"1.3.0"` | Pins contract shape. FR-5: `1.x` tolerant, unknown major → `blocked`. | `:654`, `:791` | always |
| `status` | `success \| partial \| failed \| dry-run` | Terminal verdict. `partial` forced by dropped citations / `--no-evidence-validator` / vacuous-success. `failed` and `partial` both block promotion. | `:655`; report-template `:29` | always |
| `mode` | `pre \| post` | UC-1 (pre) vs UC-2 (post). Wrapper launches `--mode post`. | `:656` | always |
| `tier_reached` | `1 \| 2 \| 3` | Reviewer topology actually reached. FR-11: expected-T2 but `==1` → `degraded`. NOTE enum is `1\|2\|3` here; report-template `:17` shows only `1\|2` (drift — Tier 3 is the remediation handoff). | `:657` | always |
| `regression_present` | `bool` | A previously-passing test now fails (verified via §6.1 step 5.5 exit-code taxonomy, not self-report). FR-8/§6 → `halted`. | `:749`, `:945` | UC-2 |
| `unauthorized_deviation_present` | `bool` | At least one Drift/Regression-class deviation lacking authorization. §6 → `halted`. | `:750` | UC-2 |
| `needs_human_decision` | `bool` | `grounding-gaps.yaml` non-empty (canonical "empty" def at `:1356`). §6 → `halted`; also blocks promotion (gate cond 8). | `:754` | always (UC-2 meaningful) |
| `user_decision_required` | `bool` | Convergence < threshold AND no auto-route applies. §6 → `halted`; blocks promotion (gate cond 8). | `:753` | always |
| `deviation_count_by_class` | map `{authorized:int, necessary:int, drift:int, regression:int}` | Per-class deviation counts. §6 → `halted` when `drift>0` OR `regression>0`. `authorized`/`necessary` are non-blocking. NO `reuse_miss` key (§17.7). | `:679-683`, `:1352` | UC-2 |
| `confidence_calibrated` | `float 0.00-1.00` | Calibrator-derived (NOT self-reported). Consumed by sc-task hook (`:846`); not in the wrapper's core verdict map but available. | `:660` | always |

### 2.2 FR-11 degradation checklist (spec `merged-requirements.md:31`, `:81`) → all route to `degraded` (HALT)

Each row is a chain-critical loss the wrapper treats as `degraded`. This is intentionally STRICTER than reflect's interactive fail-open.

| Field | Type / enum | Degradation trigger (→ `degraded`) | Source file:line | Written-when |
|-------|-------------|-----------------------------------|------------------|--------------|
| `degraded_components` | `list[str]` (TELEMETRY §9.2) | non-empty intersection with `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` (spec `:31`). Full member-token enum in §3 below. | `:802` (telemetry) | cond. (appended on each degrade event) |
| `tier_reached` | `1\|2\|3` | expected-T2 but `== 1` (lost the ensemble) | `:657` | always |
| `t2_model_class_diversity` | `full \| degraded` | `!= full` → reviewers not on distinct model classes | `:736` | T2 |
| `t2_vendor_diversity` | `multi \| single` | `== single` (unless `--allow-single-vendor`); warn-only inside reflect, but HALT in the wrapper | `:737` | T2 |
| `adversarial_unavailable` | `bool` | `true` → F3 path, no adversarial merge | `:734` | T2 |
| `merge_method` | `adversarial \| single-reviewer-fallback` | `== single-reviewer-fallback` → F2 path, ensemble collapsed to one reviewer | `:735` | T2 |
| `adversarial_convergence_score` | `float \| null` | `null` at T2 → no merged verdict. (Route on `merge_method` FIRST per `:640`; null compare is undefined behavior `:641`.) | `:733` | T2 |
| `verification_ran` | `bool` | `false` (unless exempted via `verification_skip_reason`) → Regression detection degraded to task-log claim | `:693` | UC-2 |
| `citations_dropped` | `int` | `> 0` → evidence-validator dropped unfounded citations (also forces `status: partial`). In sampled mode this is the SAMPLE count, NOT extrapolated. | `:723`, `:1091` | always |
| `input_drift_detected` | `bool` | `true` → input files mutated mid-run (tree-hash mismatch at Wave 5 / Wave 7 step 7.2) | `:717` | always |
| `serena_summary_corroboration` | `agree \| partial \| disagree \| unavailable` | **`unavailable` is EXPECTED cross-session and is NOT a halt (spec V2 FM-13, `merged-requirements.md:31`).** Only `disagree` (and possibly `partial`) is a signal; do NOT route `unavailable` to degraded. | `:692` | UC-2 |

### 2.3 Supporting fields referenced by FR-11 preflight / degradation context

| Field | Type / enum | Meaning | Source file:line | Written-when |
|-------|-------------|---------|------------------|--------------|
| `citations_total` | `int` | Total citations examined. Context for `citations_dropped` ratio. | `:721` | always |
| `citations_revalidated` | `int` (M) | Size of re-Read subset; `== citations_total` in `full_reread`. | `:722` | always |
| `citations_dropped_extrapolated` | `int` | Population projection in sampled mode. RECORDING-ONLY — does NOT gate; wrapper must NOT use this for the `citations_dropped > 0` check. | `:724`, `:807` | sampled mode |
| `citations_inferred` | `int` | `[INFERRED]`-tagged claim count. Does NOT force partial; soft WARN signal only. | `:725` | always |
| `citation_budget_policy` | `full_reread \| sampled` | `full_reread` when `citations_total ≤ 20`; tells the wrapper whether `citations_dropped` is sample- or absolute-count. | `:726` | always |
| `evidence_validator_ran` | `bool` | `false` ⇒ `--no-evidence-validator` used ⇒ `status: partial`. Note: validator membership in `degraded_components` is the FR-11 hook (`evidence-validator`). | `:727` | always |
| `verification_skip_reason` | `tool-unavailable \| read-only-project \| --no-verify \| null` | EXEMPTION reason for `verification_ran == false` (spec FR-11 "unless exempted"). | `:697` | UC-2 |
| `verification_regressions_detected` | `int` | Count of taxonomy-classified Regression exits; feeds `regression_present`. | `:696` | UC-2 |
| `t2_effective_diversity` | `full \| model-only \| vendor-only \| none` | Derived combo of model+vendor axes; richer than the two raw axes. | `:738` | T2 |
| `calibrator_diversity` | `full \| degraded` | Calibrator-side diversity (§11.0 sufficiency gate). | `:739` | T2 |
| `escalation_rule_matched` | `int 1-8 \| null` | Which §3.3 escalation rule fired. | `:661` | always |
| `report_path` | `abs path` | Path to human REPORT.md (wrapper may surface to user). | `:658` | always |
| `audit_log_path` | `abs path` | Path to audit.log. | `:659` | always |
| `tasklist_completion_pct` | `float 0.0-1.0 \| null` | Every checklist item verified-done. Promotion gate cond 3 requires `== 1.0`. | `:678`, `:1351` | UC-2 |
| `cannot_validate_without_user_input` | `bool` | Asymmetric-cost flag; reflect could not validate without the user. | `:748` | UC-2 |
| `spec_is_wrong` | `bool` | Code correct, spec contradicts on-disk reality. | `:752` | UC-2 |
| `blocked_by_low_confidence` | `bool` | Every actionable rec gated to `<0.70`. | `:751` | UC-2 |

---

## 3. `degraded_components` — complete member-token enumeration

`degraded_components` is a **TELEMETRY** field (§9.2, `SKILL.md:802`), a free-form `list[str]` that reflect *appends to* on each degrade event. The example at `:802` is `["auggie", "evidence-validator", "env-aliases"]` but the real token vocabulary is larger. Because it is telemetry (non-stable per §9.2), new tokens can appear without a contract bump — **the wrapper must match by substring/prefix family, not an exact closed set**, and must treat the FR-11 spec set `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` as the HALT-triggering subset (`merged-requirements.md:31`).

Every documented member token found in the reflect skill source:

| Token | Emitted when | Source file:line | In FR-11 HALT set? |
|-------|--------------|------------------|--------------------|
| `env-aliases` | 0 model-class aliases resolved (Tier 2 degraded to T1) | `:119`, `:220`, `:221`, `:1288` | YES |
| `serena:context-excluded` | a chain-critical Serena tool (e.g. `get_diagnostics_for_file`) excluded from active context (FR-7.3) | `:237` | YES |
| `auggie` | auggie/MCP unavailable (general grounding loss; example token at `:802`) | `:802` (example) | YES |
| `evidence-validator` | evidence-validator agent unavailable (example token at `:802`; gate degrades to inline re-Read + `status: partial`) | `:802` (example), `:1280` | YES |
| `serena` | serena MCP unavailable generally (FR-11 spec token; bare `serena`) | `merged-requirements.md:31` (spec set) | YES |
| `neighbour-search:auggie_unavailable` | reuse-auditor / auggie unavailable → inline grep fallback, findings capped at advisory L2 | `:463`, `:484` | family `auggie` (prefix) |
| `search_deps:lsp_unindexed` | LSP has not indexed a third-party dependency (no venv / unindexed package); claim stays `[INFERRED]` | `:476` | NO (claim-level, fail-open) |
| `get_current_config` | Serena `get_current_config` parse failure (Wave 0 fail-open); sets `serena_version: unknown` | `:238`, `:240` | family `serena` |
| `serena:onboarding-parse` | onboarding availability probe parse failure (fail-open) | `:271` | family `serena` |
| `serena:pre-v1.5-no-rename-propagation` | Serena `< v1.5` (or `unknown`) → write-only / no-retention; `rename_memory` mem-ref propagation skipped | `:533` | NO (retention-only degrade) |

**Wrapper guidance (data-shape only; R08 owns routing):** the FR-11 HALT set members are emitted as either bare tokens (`serena`, `auggie`, `env-aliases`, `evidence-validator`) or `serena:`-prefixed (`serena:context-excluded`). The reuse/deps/onboarding tokens (`neighbour-search:*`, `search_deps:*`, `serena:onboarding-parse`, `serena:pre-v1.5-*`, `get_current_config`) are fail-open degrades that are NOT in the spec's chain-critical HALT set — the wrapper should match the FR-11 set precisely rather than "any non-empty `degraded_components`", or it will over-HALT on benign fail-opens. R08 documents the exact predicate.

---

## 4. §9.2 Telemetry block (non-stable) — fields the wrapper MAY read but MUST tolerate as optional

Telemetry is explicitly **non-stable** (`SKILL.md:793`) — fields here can change/disappear without a contract bump. `degraded_components` (§3 above) lives here. Other telemetry fields relevant to degradation forensics:

| Field | Type / enum | Meaning | Source file:line |
|-------|-------------|---------|------------------|
| `degraded_components` | `list[str]` | see §3 | `:802` |
| `fallback_path` | `null \| F1 \| F2 \| F3` | Which fallback path executed (F2 = single-reviewer merge, F3 = adversarial-unavailable) | `:803` |
| `executor_class_source` | `flag \| env \| log-heuristic \| unknown` | How the executor model class was resolved (anti-self-confirmation) | `:804` |
| `executor_class_resolved` | `bool` | `false` → §7.1 anti-self-confirmation WARN | `:805` |
| `executor_exclusion_degraded` | `bool` | `true` → executor-class collision dropped reviewer count < 2 → T1 fallback | `:806` |
| `reviewer_models` / `reviewer_personas` / `reviewer_vendors` | `list[str]` | Actual ensemble composition | `:798-800` |
| `serena_version` | `"<v1.5" \| ">=v1.5" \| "unknown"` | Three-valued (FR-7, A4/C2) | `:811` |
| `verify_blocked` | `bool` | Any verify invocation rejected by the safety envelope | `:818` |
| `verify_blocked_reason` | `"verb '<v>' not in allowlist" \| metachar-denied \| mutation-denied \| null` | Why a verify call was blocked | `:819` |
| `verify_timeout_hit` | `bool` | A verify invocation hit timeout (exit 124) | `:820` |
| `verify_flaky_suspected` | `bool` | Single retry flipped the result → Grounding Gap, not Regression | `:821` |
| `deprecated_fields` | `list[str]` | (§9.4) names of fields slated for removal next major; signals migration window | `:871` |
| `deviation_aggregation_mode` | `per-file \| per-hunk` | >100-hunk diffs aggregate by file | `:891` |
| `hierarchy_backend` | `jetbrains \| lsp \| none \| lsp-disabled` | FR-RV3-MED.1 type-hierarchy backend | `:833` |

(Full telemetry list: `SKILL.md:795-836`. Wave-duration / token-usage / memory-hit fields are run analytics, not gate inputs.)

---

## 5. CRITICAL distinction: `gate_evaluation` 11-field struct is NOT in return-contract.yaml

The brief asks about the `gate_evaluation` struct (11 atomic fields). **This struct does NOT live in `return-contract.yaml`** — it lives in a sibling artifact `<output>/promotion-log.yaml` (`SKILL.md:1454`, written every time Wave 7 runs). The wrapper parses `return-contract.yaml`, so it sees the **scalar `promotion_*` fields** instead.

### 5.1 What `return-contract.yaml` carries (the promotion summary scalars — §9.1 lines 776-788)

| Field | Type / enum | Source file:line |
|-------|-------------|------------------|
| `promotion_action` | `moved \| skipped \| rejected \| failed \| already-promoted \| resumed \| dry-run \| not-applicable` | `:776` |
| `promotion_adapter` | `task \| sprint-release \| none \| null` | `:777` |
| `promotion_source` | `abs path \| null` | `:778` |
| `promotion_destination` | `abs path \| null` | `:779` |
| `promotion_log_path` | `abs path \| null` (→ points at promotion-log.yaml where gate_evaluation lives) | `:780` |
| `promotion_gate_passed` | `bool \| null` (null when mode==pre or pre-gate skipped) | `:781` |
| `promotion_skip_reason` | `user-flag \| gate-failed \| adapter-unresolved \| dry-run \| null` | `:782` |
| `promotion_fail_reason` | `source_disappeared \| destination_collision \| mv_error \| sha_mismatch \| null` | `:783` |
| `promotion_override_used` | `--promote-anyway \| --promote-resume \| null` | `:784` |
| `promotion_rollback_command` | `string \| null` | `:785` |
| `promotion_checkpoint_path` | `abs path \| null` | `:786` |
| `promotion_cross_fs` | `bool` | `:787` |
| `promotion_pending` | `bool` | `:788` |

### 5.2 The 11-atomic `gate_evaluation` struct (in promotion-log.yaml, `SKILL.md:1468-1479`)

Documented here for completeness because the brief asked, but the wrapper reads `promotion_gate_passed` / `promotion_skip_reason` from return-contract.yaml rather than this struct. Field order is fixed (`refs/promotion-adapters.md:154`):

| gate_evaluation key | Value | §14.5.2 condition |
|---------------------|-------|-------------------|
| `mode_post` | `pass \| fail` | cond 1 (`mode == post`) |
| `status_success` | `pass \| fail` | cond 2 (`status == success`) |
| `tasklist_completion_pct_1_0` | `pass \| fail` | cond 3 (`tasklist_completion_pct == 1.0`) |
| `no_drift_no_regression` | `pass \| fail` | cond 4 (`drift==0 AND regression==0`) |
| `frontmatter_present` | `pass \| fail` | cond 5a |
| `frontmatter_status_matches` | `pass \| fail` | cond 5b |
| `no_citations_dropped` | `pass \| fail` | cond 6a (`citations_dropped == 0`) |
| `no_grounding_gaps` | `pass \| fail` | cond 6b (grounding-gaps.yaml empty) |
| `no_input_drift` | `pass \| fail` | cond 7 (`input_drift_detected == false`) |
| `no_user_decision_pending` | `pass \| fail` | cond 8 (`needs_human_decision==false AND user_decision_required==false`) |
| `adversarial_result_present` | `pass \| fail \| n/a` | cond 9 (`convergence_score` not null when T2; `n/a` at T1) |

Plus `gate_evaluation_failures: [<list>]` (derived; keys whose value is `fail`; empty when `gate_passed: true`; `SKILL.md:1480`, `refs/promotion-adapters.md:155`) and `gate_passed: bool` (`:1481`).

Source-of-truth contract for these is `SKILL.md §14.5.6` (`refs/promotion-adapters.md:154` cites "L1213-1224"; the actual block is at `SKILL.md:1468-1481` in the current file — minor internal line-ref drift, flagged).

### 5.3 Per-task verdict array (`per_task_verdicts`, §9.1 lines 757-763) — IS in return-contract.yaml

Empty list for UC-1 or single-task UC-2. Each element:

| Sub-field | Type / enum | Source file:line |
|-----------|-------------|------------------|
| `task_id` | `string` | `:758` |
| `status` | `success \| partial \| failed` | `:759` |
| `deviation_class` | `authorized \| necessary \| drift \| regression \| none` | `:760` |
| `citations_dropped` | `int` | `:761` |
| `per_task_validation_strength` | `float 0.00-1.00` (calibrated, post-evidence-validator) | `:762` |
| `evidence_anchor` | `abs path \| task-log ref` | `:763` |

Sprint executor.py routes on `per_task_verdicts[].status`, `.per_task_validation_strength` (`<0.70` → re-execute), and `.deviation_class == regression` → rollback (`SKILL.md:845`). The wrapper's per-task handling, if any, would read the same sub-fields.

---

## 6. LOAD-BEARING vs OPTIONAL classification (NFR-8 unknown-field tolerance)

Per §9.4 (`SKILL.md:881`), **all consumers MUST treat unknown top-level fields as read-and-ignore**. So "optional" here means "absence is tolerated / field may be missing or null in valid runs" — the parser must NOT hard-fail on absence of optional fields. "Load-bearing" means the verdict/degradation logic depends on the value, and the wrapper SHOULD fail-loud (→ `blocked`) if it is missing or unparseable.

### 6.1 LOAD-BEARING — parser fails (→ `blocked`) if missing/unparseable

These are required by the §9.1 stable contract AND consumed by FR-5/FR-11:

- `contract_version` — gate first; unknown major → `blocked` (`merged-requirements.md:25`).
- `status` — primary verdict driver.
- `mode` — must be `post` for the wrapper's gate.
- `tier_reached` — degradation check (expected-T2 but `==1`).

(report-template.md:26 independently states the REPORT.md header is "invalid if any are missing" for `contract_version, status, mode, tier_reached, confidence_calibrated, citations_*, citation_budget_policy` — corroborating that these are non-optional.)

### 6.2 LOAD-BEARING (conditionally present) — required for the verdict but only emitted in the relevant mode/tier; absence in the WRONG context is itself a signal

- UC-2 verdict drivers: `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `deviation_count_by_class.{drift,regression}` — for a `--mode post` run these SHOULD be present; missing in a post run is anomalous → fail-loud.
- T2 degradation drivers: `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score` — only meaningful when `tier_reached >= 2`. At T1 they may be null/absent and that is NOT degradation (it's the expected T1 shape). The wrapper must guard the null comparison (`SKILL.md:641`) and route on `merge_method` FIRST (`:640`).
- `citations_dropped`, `input_drift_detected`, `verification_ran` — always-emitted gate inputs; treat as load-bearing.

### 6.3 OPTIONAL / tolerate-absence (NFR-8)

- All `§9.2 telemetry` fields **including `degraded_components`** — telemetry is non-stable; the wrapper reads `degraded_components` defensively (default to `[]` if absent) rather than hard-failing. (It is the one telemetry field the wrapper genuinely depends on for FR-11, so treat *absence* as `[]` = no degradation, but a malformed value as `blocked`.)
- UC-1-only fields (`coverage_pct`, `coverage_undefined`, `unmapped_requirements`, `best_practice_grade`, `implementation_coverage_pct`, `missing_implementations`, `hierarchy_*`) — irrelevant to the `--mode post` wrapper; ignore.
- Reuse-sweep fields (`reuse_*`, `neighbour_search_*`, `max_overlap_score`) — advisory; not in the verdict map.
- All `promotion_*` fields — the wrapper does NOT promote (it writes its own frontmatter verdict); these are informational. The wrapper passes its own `--output`; promotion is reflect's internal Wave 7.
- `citations_dropped_extrapolated` — RECORDING-ONLY; the wrapper must NOT use it for the `citations_dropped > 0` degradation check (`SKILL.md:724`, `:1359`).
- `serena_summary_corroboration: unavailable` — EXPECTED cross-session; NOT a halt (spec V2 FM-13, `merged-requirements.md:31`). The field is present but its `unavailable` value is benign.

### 6.4 Unknown-field forward-compat

Per §9.4 minor-bump rule (`SKILL.md:863`): a `1.4.0` contract may add new top-level fields. The wrapper's `contract.py` verdict function MUST read-and-ignore them (`:881`). Only an unknown MAJOR (`2.x`) routes to `blocked` (`merged-requirements.md:25`, `:133`).

---

## 7. `run_id` / `metrics.json` — NOT return-contract.yaml fields (clarification)

The brief listed `run_id`, `metrics.json`. These are **NOT** part of `return-contract.yaml`. They belong to the cross-run analytics stream:

- `run_id` appears in the per-run `runs.jsonl` meta-eval record (`refs/ops-integration.md:234`: `{"run_id": "...", ..., "skill_version": "1.0", "mode": "post", "tier_reached": 2, "status": "success", ...}`), and in the §16 emission contract (`SKILL.md:1544`: `"skill_version": "<contract_version from §9.1>"`). This is the §15.1 metrics export consumed by the meta-eval aggregator (`SKILL.md:852`), not by the wrapper's per-run gate.
- There is no `metrics.json` field inside the contract; metrics are the telemetry block (§9.2) plus the `runs.jsonl` aggregator. The CI grader (`make reflect-eval`) reads the contract's per-task array + `status` + `evidence_validator_ran` + `audit_log_path` (`SKILL.md:851`).

The wrapper does NOT need `run_id` to derive its verdict; it owns its own run-uniqueness via the pinned `--output` dir (FR-4, `merged-requirements.md:24`).

---

## 8. Summary

**Authoritative facts pinned:**

1. **`contract_version` = `"1.3.0"`** (quoted) per `SKILL.md:654`/`:791`. The `1.2.0` at `report-template.md:14` is a stale REPORT.md-header value (DRIFT flagged) — the wrapper parses `return-contract.yaml` (§9.1), never the REPORT.md header.
2. The wrapper parses exactly `<output>/return-contract.yaml` (`SKILL.md:649`), a **two-block** contract: §9.1 stable (60+ load-bearing fields) + §9.2 telemetry (non-stable, where `degraded_components` lives).
3. **Every FR-5 verdict-map field and FR-11 degradation field is present in §9.1** and cataloged with file:line in §2 above. Verbatim §9.1 block quoted in §1.

**Load-bearing vs optional:** §6 classifies them. Hard-required (→ `blocked` if missing): `contract_version, status, mode, tier_reached`. Conditionally load-bearing: UC-2 deviation flags + T2 diversity/adversarial fields (null/absent at T1 is normal, not degradation). Optional/tolerate-absence: all telemetry, UC-1 fields, reuse fields, promotion scalars. Unknown top-level fields → read-and-ignore (NFR-8 / §9.4 `:881`); unknown MAJOR version → `blocked`.

**Three gotchas the wrapper author must encode:**

- **`degraded_components` is telemetry, not stable** (§3): match the FR-11 HALT subset `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` precisely. Do NOT route on "any non-empty list" — benign fail-open tokens (`search_deps:lsp_unindexed`, `serena:pre-v1.5-*`, `serena:onboarding-parse`, `get_current_config`) appear there but are NOT chain-critical.
- **`serena_summary_corroboration: unavailable` is EXPECTED cross-session, NOT a halt** (§2.2; spec V2 FM-13 `merged-requirements.md:31`).
- **`gate_evaluation` (11 atomic fields) is in `promotion-log.yaml`, NOT `return-contract.yaml`** (§5). The contract carries `promotion_*` scalars + `promotion_gate_passed`/`promotion_skip_reason` instead. The wrapper does not promote, so these are informational only. `citations_dropped_extrapolated` is recording-only — use `citations_dropped` (sample-count) for the `>0` check.

**Coordination with R08:** this doc fixes the DATA SHAPE (names/types/enums/source). R08 owns which VALUE → which verdict {pass, halted, degraded, blocked}.

**Open / unverified:** `refs/promotion-adapters.md:154` cites the gate_evaluation source as "SKILL.md §14.5.6 (L1213-1224)", but in the current SKILL.md the block is at lines 1468-1481 — an internal line-ref drift in the ref, not a contract problem. Flagged, not load-bearing for the wrapper.
