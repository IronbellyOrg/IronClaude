<!-- Variant: opus:architect — "full structural unification; treat both commands as siblings to be re-derived; accept breaking changes if justified" -->
<!-- Generated from FINAL-REPORT.md (11 sections) -->

# RELEASE SPEC — v3.75 RigorflowMerger / task-unified-v3 (Full Unification Variant)

**Stance.** Treat `/sc:task` and the historical `/sc:task-unified` as **co-equal sibling lineages** to be unified at the design level, not legacy-vs-canonical. The v3.7 canonicalization gave us the right command **name**; this release gives us the right command **semantics**. Adopt the full FINAL-REPORT best-of-breed slate in a coherent structural redesign. Breaking changes are accepted where the structural payoff exceeds the migration cost; clear deprecation runways accompany each.

**Source.** FINAL-REPORT.md (11 sections, including §10 Shared Assumptions and §11 TUI Improvement Bundle).

**Note on naming.** The v3.7 hard constraint is preserved: `/sc:task` remains the only **command name**. "Structural unification" means re-deriving the **semantics** behind `/sc:task` so it carries the full historical merit of both lineages — not adding `/sc:task-unified` back as a live command.

---

## 1. Release identity & scope

### 1.1 Name and version

- **Release ID:** `v3.75-RigorflowMerger-task-unified-v3`
- **Version bump:** `/sc:task` command file metadata bumps from `version: "2.0.0"` to `version: "3.0.0"` (major bump to signal breaking changes are present).
- **Surface affected:** `/sc:task` command file, `sc-task-protocol` skill (substantially restructured), `core/ORCHESTRATOR.md` classification logic, `sc-tasklist-protocol` (drift consolidation), `cli/sprint/` runtime, TUI rendering, audit/telemetry infrastructure.

### 1.2 In-scope (this release)

The unification variant **adopts the full best-of-breed slate** from FINAL-REPORT §6, with explicit breaking-change runways where required:

**Task-side — all 7 TU candidates:**
- **TU-001** CRITICAL FAIL conditions (3 conditions, programmatic enforcement).
- **TU-002** Output-type discrimination axis (`code|analysis|documentation|opinion`) with per-type gate tables.
- **TU-003** Six universal quality principles (NFR + checklist + prompt).
- **TU-004** Deterministic BLOCKED state at confidence <0.70.
- **TU-005** Classification-logic consolidation to single source of truth (`config/tier-keywords.yaml`).
- **TU-006** Materialize the missing skill sub-files (`refs/`, `rules/`, `templates/`, `config/`).
- **TU-007** Mandatory completion checklist.

**Sprint-side — all 6 SE candidates:**
- **SE-001..SE-005** as documented in FINAL-REPORT §6.2.
- **SE-006** `--auto-diagnostic-threshold N` flag (DEFER in surgical variant, but ADOPT here because the structural redesign creates the right hook for it).

**Naming consolidation (breaking-change runway):**
- **Q1 (sentinel rename):** `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` → `<!-- SC:TASK:CLASSIFICATION -->`, with telemetry-compat shim.
- **Q2 (forensic-caller rename):** `--caller task-unified` → `--caller task`, with telemetry-compat shim.

Both renames ship under a **deprecation runway**:
1. **v3.75:** Both old and new strings supported. The new strings become the **emitted default**; the old strings are still **accepted** if they appear in test fixtures or downstream consumers.
2. **v3.8 (next major):** Old strings removed.

**TUI bundle (P-series, FINAL-REPORT §11):** All top-5 (P-05, P-02, P-03, P-07, P-01) ship in the recommended order.

### 1.3 Out-of-scope (non-goals)

- **NG-1.** Reintroduce `/sc:task-unified` as a live command. **Hard constraint** — never reversed even in full unification, because v3.7 already established `/sc:task` as the canonical command name and reverting would regress N1-N12.
- **NG-2.** Resurrect `task-unified.md` or `sc-task-unified-protocol/` directories.
- **NG-3.** Replace IC's keyword-based classifier with semantic NLP (separate redesign, not this release).
- **NG-4.** Adopt LW's bash-orchestrator / Python-from-bash patterns.
- **NG-5.** TypeScript plugin work (v5.0 scope).
- **NG-6.** Backward-compatible-only operation. **Explicitly out** for this variant: this release accepts breaking changes where structural payoff exceeds migration cost. Each breaking change ships with a deprecation runway and migration guide.

### 1.4 Release-split recommendation

Per FINAL-REPORT §9.3 / Q8: **YES, apply the release-split protocol**. The unification variant proposes a **three-release split**, not two:

- **R1 (Task-surface rigor):** TU-001, TU-003, TU-004, TU-007. (Same as surgical variant's R1.)
- **R2 (Sprint-side + TUI):** SE-001..SE-006 + TUI top-5. (Sibling to R1.)
- **R3 (Structural consolidation):** TU-002, TU-005, TU-006, Q1+Q2 renames with deprecation runway. (**Depends on R1+R2** because TU-002 routes off the rigor framework and TU-005 consolidates across SoT files that R1+R2 touch.)

Rationale: R3 is the dedicated cleanup release that the surgical variant punted to "a future release." The unification variant **plans** R3 explicitly, so it isn't infinitely deferred. R3 effort: ~5-7 dev-days (TU-002 M, TU-005 M, TU-006 S, Q1/Q2 S with shim).

**If split is not adopted:** the unification variant collapses to a single v3.75 release of ~12-18 dev-days. `[inference]`

---

## 2. Surface contract (what stays, what changes, what is added, what breaks)

### 2.1 Stays (no change)

- Command name: `/sc:task`.
- The 8 existing CLI flags (`--strategy, --compliance, --verify, --skip-compliance, --force-strict, --parallel, --delegate, --no-escalation`).
- Strategy axis values (`systematic, agile, enterprise, auto`).
- Compliance tier values (`strict, standard, light, exempt`).

### 2.2 Changes (modified behavior, same flags)

- **TU-004 (BLOCKED state):** As in surgical — soft `confidence < 0.70` prompt becomes deterministic BLOCKED with explicit re-invocation requirement. Header schema adds `BLOCKED` as a fifth TIER value.
- **TU-007 (completion checklist):** Six-condition gate before `complete` status.
- **Auto-tier behavior:** With TU-005 consolidation, the keyword tables driving `--compliance auto` widen to match the previously-tasklist-only set (`password, credential, secret, jwt, transaction, query` added to STRICT; LIGHT compounds + STANDARD additions reconciled). **Behavior change:** some tasks previously classified STANDARD will now classify STRICT.

### 2.3 Additions (new behavior + new surface)

- **TU-001 (CRITICAL FAIL):** New `CriticalFailCondition` dataclass; three STRICT conditions.
- **TU-002 (output-type axis):** New `output_type ∈ {code, analysis, documentation, opinion}` axis. Detection rules embedded in `core/ORCHESTRATOR.md` and `task.md`:
  - All `*.md` → documentation.
  - Comparison/analysis reports → analysis.
  - Code changes → code.
  - Filename keyword `recommendation|opinion|verdict` (or `--output-type opinion` flag) → opinion.
  - **Per Q3 resolution:** output-type is a **modifier** on tier (option (a)). Tier is selected first; output-type selects which gate table applies. Per-output-type gate tables (per FINAL-REPORT §6.1 TU-002):
    - `code`: compile/test required.
    - `analysis`: evidence citation required; no lint.
    - `documentation`: structure check only; no code testing.
    - `opinion`: CEV structure required; no automated verification.
- **TU-003 (six principles):** NFR section + checklist artifact + verification-agent prompt binding (Q14 (c) both).
- **TU-005 (single source of truth):** New file `src/superclaude/skills/sc-task-protocol/config/tier-keywords.yaml`. All four consumers (`task.md`, `ORCHESTRATOR.md`, `sc-tasklist-protocol/SKILL.md`, `sc-tasklist-protocol/rules/tier-classification.md`) load from it via `make sync-dev`.
- **TU-006 (skill sub-files):** `sc-task-protocol/` gains `refs/`, `rules/`, `templates/`, `config/` subdirectories. The broken `SKILL.md:359-365` references resolve to real files.
- **New flag `--output-type {code|analysis|documentation|opinion|auto}`** with default `auto`. Adds a 9th flag to `/sc:task`.
- **Audit log infrastructure** (Q11): append-only JSON log of every classification + override + escape-hatch use.
- **SE-001..SE-006 sprint-side changes** as documented in FINAL-REPORT §6.2.
- **SE-006 `--auto-diagnostic-threshold N`** as a new sprint CLI flag (default 3, range 1-10).

### 2.4 Breaks (with deprecation runway)

| Break | Migration | Runway |
|-------|-----------|--------|
| `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel renamed to `<!-- SC:TASK:CLASSIFICATION -->` | v3.75 emits new sentinel; parser accepts both. v3.8 removes old. | 1 release |
| `--caller task-unified` (TFEP forensic) renamed to `--caller task` | v3.75 emits new value; forensic side accepts both. v3.8 removes old. | 1 release |
| STRICT keyword set widened (`password, credential, secret, jwt, transaction, query` added) | Tasks previously STANDARD that now classify STRICT will receive a one-line warning in classification header: `MIGRATION: tier widened from STANDARD to STRICT in v3.75; use --compliance standard --reason "..." to override`. | No removal; behavior is new from v3.75 onward |
| Classification header schema adds `BLOCKED` as valid TIER value | Downstream parsers must handle. Provided regex update in migration guide. | No removal; additive |
| New `--output-type` flag default `auto` | Existing invocations without `--output-type` default to `auto`; behavior is detected. May reclassify doc-tasks to lower scrutiny. | No removal; behavior change at default |
| Skill sub-directory structure (`refs/, rules/, templates/, config/`) materialized | Downstream tooling that depends on the empty-sub-file structure of `sc-task-protocol/` may need to add the new paths. | No removal; additive |

**All breaks are gated behind the deprecation runway.** v3.75 supports both old and new; v3.8 cleans up. This gives downstream consumers one full release cycle to migrate.

---

## 3. Protocol changes (sc-task-protocol skill restructured)

### 3.1 New sub-directory structure (TU-006)

```
src/superclaude/skills/sc-task-protocol/
├── SKILL.md                         # Top-level protocol (edited)
├── __init__.py
├── refs/
│   ├── tier-classification.md       # Mirror of canonical tier logic
│   ├── output-type-detection.md     # TU-002 detection rules
│   └── critical-fail-conditions.md  # TU-001 condition catalog
├── rules/
│   ├── tier-keywords.yaml -> ../config/tier-keywords.yaml (symlink)
│   ├── critical-fail-rules.md       # TU-001 gate evaluator rules
│   ├── quality-principles.md        # TU-003 NFR text
│   └── completion-checklist.md      # TU-007 six conditions
├── templates/
│   ├── classification-header.md.tmpl
│   ├── blocked-header.md.tmpl
│   └── completion-report.md.tmpl
├── config/
│   └── tier-keywords.yaml           # TU-005 single source of truth
└── scripts/
    └── validate_classification.py   # CI helper
```

After this restructure, the `SKILL.md:359-365` references (currently broken per R7 §5 item 2) all resolve.

### 3.2 SKILL.md restructured

The top-level `SKILL.md` is reorganized into eight sections (was 5):

1. **Entry rule** (existing).
2. **CRITICAL FAIL conditions (TU-001)** — references `refs/critical-fail-conditions.md` + `rules/critical-fail-rules.md`.
3. **Quality Principles NFR (TU-003)** — references `rules/quality-principles.md`.
4. **Tier classification (TU-005 link)** — references `refs/tier-classification.md` (which is the single SoT view).
5. **Output-type classification (TU-002)** — references `refs/output-type-detection.md`.
6. **MCP requirements** (existing).
7. **Tool coordination** (existing, with TU-001 hook).
8. **Completion checklist (TU-007)** — references `rules/completion-checklist.md`.

TFEP semantics are preserved unchanged.

### 3.3 Single source of truth (TU-005)

`config/tier-keywords.yaml` schema:

```yaml
tiers:
  STRICT:
    weight: 0.4
    keywords:
      - security
      - authentication
      - authorization
      - database
      - migration
      - refactor
      - breaking change
      - encrypt
      - token
      - session
      - oauth
      # Reconciled from sc-tasklist-protocol (Q12 (a) widen):
      - password
      - credential
      - secret
      - jwt
      - transaction
      - query
    compound_phrases:
      - "fix security"
      - "add authentication"
      - "update database"
      - "change api"
    boosters:
      files_gt_2: 0.3
      paths_match: ["auth/", "security/", "crypto/"]
      path_boost: 0.4
    critical_path_override: ["auth/", "security/", "crypto/", "models/", "migrations/"]

  STANDARD:
    weight: 0.2
    keywords: [implement, add, create, update, fix, build, modify, change]
    # Q12 (a) widen:
    additional_keywords: [remove, delete, deprecate]

  LIGHT:
    weight: 0.3
    keywords: [typo, comment, whitespace, lint, docstring, formatting, spacing, minor]
    compound_phrases:
      - "quick fix"
      - "minor change"
      - "fix typo"
      - "refactor comment"
      # Q12 (a) widen:
      - "small update"
      - "update comment"
      - "fix spacing"
      - "fix lint"
      - "rename variable"
    boosters:
      files_eq_1: 0.1
      lines_le_50: 0.05

  EXEMPT:
    weight: 0.4
    keywords: [explain, search, commit, push, plan, discuss, brainstorm, what, how, why]
    boosters:
      is_read_only: 0.4
      is_git_operation: 0.5
      all_doc_files: 0.5
    path_overrides:
      docs: 0.5
      md_only: 0.5

  BLOCKED:
    # Synthetic tier emitted only by TU-004 deterministic block
    # No keyword set; produced when max(tier_scores) confidence < 0.70

priority_order: [STRICT, EXEMPT, LIGHT, STANDARD]

compound_match_boost: 0.15

confidence_thresholds:
  block_below: 0.70
  reduce_if_top_two_within: 0.1  # -0.15
  boost_compound: 0.15
  reduce_no_keywords: 0.30
  cap_max: 0.95

output_types:
  code:
    detection: [code_change, src_path]
    gates: [compile, test_required, lint]
  analysis:
    detection: [filename_contains: "comparison|analysis|report"]
    gates: [evidence_citation_required, no_lint]
  documentation:
    detection: [all_md, docs_path]
    gates: [structure_check_only, no_code_test]
  opinion:
    detection: [filename_contains: "recommendation|opinion|verdict", flag: "--output-type opinion"]
    gates: [cev_structure_required, no_automated_verification]
```

All consumers load this YAML at startup. `make sync-dev` includes the YAML in the sync target.

### 3.4 CRITICAL FAIL evaluator (TU-001)

`rules/critical-fail-rules.md` defines three conditions:

```yaml
critical_fail_conditions:
  mcp_unavailable:
    applies_to: [STRICT]
    check_when: [task_entry, after_each_turn]
    fail_message: "Required MCP server unavailable: {server_name}"
    always_blocks: true

  empty_output_after_max_turns:
    applies_to: [STRICT]
    check_when: [after_final_turn]
    fail_message: "Output file absent after {max_turns} turns"
    always_blocks: true

  missing_classification_header:
    applies_to: [STRICT]
    check_when: [after_first_turn]
    fail_message: "Classification header absent in STRICT output"
    always_blocks: true
```

Skill internals implement `CriticalFailCondition` dataclass and the gate evaluator loop.

### 3.5 BLOCKED state (TU-004)

Same as surgical variant §3.5 — extended header schema, deterministic halt at <0.70 confidence, `--skip-compliance --reason "..."` override.

### 3.6 Output-type axis (TU-002)

New evaluator in `core/ORCHESTRATOR.md`:

```
step_6_output_type (added after step_5_confidence):
  1. If user passed --output-type, use that.
  2. Else apply detection rules from rules/output-type-detection.md.
  3. Selected output_type drives which gate table from config/tier-keywords.yaml applies.
  4. Tier × output_type → effective gate set.
```

### 3.7 Completion checklist (TU-007)

`rules/completion-checklist.md` enumerates the six conditions. Same caveat as surgical: must be verified against LW original before merge. This variant goes further and **adds a script-side check** (`scripts/validate_classification.py`) that asserts the checklist is complete and the LW source has been cited.

### 3.8 Audit log infrastructure (Q11)

New file: `src/superclaude/skills/sc-task-protocol/audit.py` (small helper module).

Schema (per audit log entry):
```json
{
  "timestamp": "ISO-8601",
  "task_id": "uuid",
  "computed_tier": "STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED",
  "confidence": 0.85,
  "user_override": null,
  "skip_compliance": false,
  "reason": null,
  "force_strict": false,
  "output_type": "code"
}
```

Persisted to `.dev/audit/sc-task-{date}.jsonl`. Append-only; rotates daily.

---

## 4. Naming & deprecation (Q1/Q2 renames with runway)

### 4.1 Hard constraints (non-negotiable)

- `/sc:task` is the only canonical command name.
- N1-N12 rename map (v3.7) remains green.
- No `name: task-unified` reintroduction.

### 4.2 Q1 — Sentinel rename

**Decision:** RENAME with shim.

- **v3.75:** Emit `<!-- SC:TASK:CLASSIFICATION -->` (new). Parser in `validate_classification.py` accepts **both** `SC:TASK:CLASSIFICATION` and `SC:TASK-UNIFIED:CLASSIFICATION` (compat shim).
- **v3.8:** Remove `SC:TASK-UNIFIED:CLASSIFICATION` from parser.

**Validation pre-merge:** A-005 investigation (enumerate `/sc:forensic` consumers of the sentinel string) **must** complete and confirm no consumer pattern-matches on the literal `TASK-UNIFIED` token. If a consumer is found, the rename is **deferred until that consumer is updated**. The investigation is a blocking pre-merge gate.

### 4.3 Q2 — Forensic-caller rename

**Decision:** RENAME with shim.

- **v3.75:** TFEP invocation becomes `/sc:forensic --tier {tier} --intent {intent} --caller task`. Forensic skill accepts both `task-unified` and `task` as caller values.
- **v3.8:** Remove `task-unified` from forensic parser.

**Validation pre-merge:** Same A-005 investigation as Q1. The two renames are gated on the same investigation.

### 4.4 Header schema (additive + extended)

```
TIER: [STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED]
OUTPUT_TYPE: [code|analysis|documentation|opinion]
```

The `OUTPUT_TYPE` field is **new** (TU-002 addition). It is required for STRICT and STANDARD; optional for LIGHT and EXEMPT.

### 4.5 Deprecation surface (formal list)

| Item | v3.75 status | v3.8 status |
|------|--------------|-------------|
| `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` | DEPRECATED (parser accepts; emit `SC:TASK:CLASSIFICATION` instead) | REMOVED |
| `--caller task-unified` | DEPRECATED (forensic accepts; emit `--caller task`) | REMOVED |
| Soft `confidence < 0.70` prompt | REPLACED by BLOCKED state | n/a |
| Empty-output STRICT completion (was permitted, will now FAIL) | BREAK (TU-001 #2) | n/a |
| Missing classification-header STRICT completion (was permitted, will now FAIL) | BREAK (TU-001 #3) | n/a |
| Tasklist-only STRICT keywords absent from `task.md` | RECONCILED via TU-005 SoT (behavior widened) | n/a |
| Empty-sub-file `sc-task-protocol/` structure | EXPANDED to canonical `refs/, rules/, templates/, config/` | n/a |

Each deprecation is documented in `MIGRATION-v3.75-to-v3.8.md`.

---

## 5. Test strategy

### 5.1 New tests for full slate (TU-001..007 + SE-001..006)

**TU-001:** Same as surgical §5.1.

**TU-002 (NEW for unification variant):**
- `tests/skills/test_output_type_detection.py`
  - `test_detects_code_for_code_changes`
  - `test_detects_documentation_for_md_files`
  - `test_detects_analysis_for_comparison_filename`
  - `test_detects_opinion_for_recommendation_filename`
  - `test_user_flag_overrides_detection`
  - `test_per_output_type_gate_table_selection`
  - `test_documentation_skips_compile_gate`
  - `test_analysis_requires_evidence_citation`
  - `test_opinion_requires_cev_structure`

**TU-003:** Same as surgical §5.1.

**TU-004 (BLOCKED):** Same as surgical §5.1.

**TU-005 (SoT YAML):**
- `tests/skills/test_tier_keywords_yaml.py`
  - `test_yaml_loads_without_error`
  - `test_all_required_tiers_present`
  - `test_consolidated_strict_keywords_include_password_credential_secret_jwt`
  - `test_widened_light_compounds_included`
  - `test_widened_standard_keywords_remove_delete_deprecate`
  - `test_priority_order_strict_first`
  - `test_all_4_consumers_load_same_yaml` (parameterized over the 4 SoT consumers)

**TU-006 (sub-files):**
- `tests/skills/test_sc_task_protocol_sub_files.py`
  - `test_refs_directory_exists_and_populated`
  - `test_rules_directory_exists_and_populated`
  - `test_templates_directory_exists_and_populated`
  - `test_config_directory_contains_tier_keywords_yaml`
  - `test_skill_md_359_to_365_references_resolve`

**TU-007:** Same as surgical §5.1; plus `test_completion_checklist_cites_lw_source` (validates the script-side check).

**SE-001..SE-006:** As surgical §5.4 + new test `tests/sprint/test_auto_diagnostic_threshold.py` for SE-006.

### 5.2 Naming-rename runway tests (Q1/Q2)

- `tests/skills/test_sentinel_renamed.py`
  - `test_v3_75_emits_new_sentinel`
  - `test_parser_accepts_both_old_and_new_sentinel` (compat shim)
  - `test_v3_8_removal_path_documented` (skip-marker test confirming the v3.8 plan)
- `tests/skills/test_forensic_caller_renamed.py`
  - `test_v3_75_emits_new_caller`
  - `test_forensic_accepts_both_caller_values`

### 5.3 A-005 investigation gate

A **pre-merge** investigation task (not a test) must enumerate all `/sc:forensic` consumers of `--caller task-unified`. Outputs:
- `docs/a-005-forensic-consumers.md` listing every grep-match in `src/`, `.claude/`, `.dev/`.
- Verdict: "no consumer pattern-matches on TASK-UNIFIED" OR "consumer X depends on the literal; rename deferred."

The investigation is **blocking** for Q1/Q2 rename merge. The other TU-001..007/SE-001..006 work can proceed in parallel.

### 5.4 Regression tests

Same baseline as surgical §5.2:
- `tests/sprint/`: 921 passed, 57 failed baseline.
- TUI Waves 1-2 + tmux + summarizer + retrospective: 125/125 pass.
- `test_process.py::TestClaudeProcess`: 16/16.
- `TEST-SPEC.md:34-80`: no `/sc:task-unified` strings in `ClaudeProcess.build_prompt`.
- Wave-4 checkpoint heading parser: +3 tests.

Additional unification-specific:
- All four SoT consumers (`task.md`, `ORCHESTRATOR.md`, `sc-tasklist-protocol/SKILL.md`, `sc-tasklist-protocol/rules/tier-classification.md`) produce identical classifications on a fixed test set after TU-005. This is a **net-new** invariant from this release.

### 5.5 TUI tests

Same as surgical §5.5. P-01 mandatory mitigations (FINAL-REPORT §11.3) apply.

### 5.6 Coverage target

- **85% line coverage** on all new code (TU-001..007 + SE-001..006). Higher than surgical because more new surface.
- **100% on `audit.py`** (security-sensitive write path).
- **100% on `validate_classification.py`** (CI gate).

---

## 6. Backward compatibility & risk

### 6.1 Compat guarantees

- **CLI command name:** unchanged (`/sc:task`).
- **CLI flags:** **one new flag added** (`--output-type`); all 8 existing flags preserved.
- **Existing flag values:** all preserved.
- **Header sentinel string:** parser accepts old; emit new.
- **Forensic caller string:** parser accepts old; emit new.

### 6.2 Breaks summarized

See §2.4 table. The unification variant has **more breaks** than the surgical variant, but each is gated behind:
1. A compat shim during v3.75.
2. A documented removal in v3.8.
3. A migration guide entry.

### 6.3 New risks (in addition to FINAL-REPORT §7)

| ID | Risk | Sev | Like | Mitigation |
|----|------|-----|------|------------|
| RK-U-1 | TU-002 routing change reclassifies historically-STRICT doc tasks to lower scrutiny. | Medium | Medium | Emit before/after tier in classification header (RK-08 mitigation extends to output_type). Stage rollout via `--output-type auto` default; users can pin to `--output-type code` to retain old behavior. |
| RK-U-2 | TU-005 SoT YAML adds a load-time dependency. If the YAML is malformed, every `/sc:task` invocation fails. | High | Low | YAML schema validation in CI; ship with frozen baseline; `make verify-sync` checks YAML round-trip. |
| RK-U-3 | Q1/Q2 renames depend on A-005 investigation. If A-005 finds a hidden consumer, the rename is deferred but the rest of the unification ships, creating a partial unification. | Medium | Medium | Investigation is a pre-merge blocker for Q1/Q2 only; TU-001..007 + SE-001..006 are independent. If A-005 finds a consumer, ship the rename in v3.76 with consumer migration. |
| RK-U-4 | Skill sub-file materialization (TU-006) creates ~10 new files; CI sync (`make sync-dev` / `make verify-sync`) needs to handle the expanded structure. | Low | Medium | Update the sync script's `INCLUDED_PATHS` allowlist; add `test_verify_sync_handles_subfiles` regression test. |
| RK-U-5 | The widened STRICT keyword set (`password, credential, secret, jwt, transaction, query`) may reclassify many existing tasks. Telemetry could spike STRICT classifications by 15-30% in the first week. `[inference]` | Medium | High | Include a 1-week soft-launch window where the wider keywords emit a `MIGRATION:` warning but do not yet escalate tier. After the window, full enforcement. |
| RK-U-6 | TU-002 + TU-005 + TU-006 all touch the same SKILL.md restructure. Merge conflicts likely. | Medium | High | Land in this dependency order: TU-006 (sub-file scaffolding) → TU-005 (YAML SoT) → TU-002 (output-type routing). Single PR is acceptable but cumbersome; preferred: 3 sequential PRs. |

All FINAL-REPORT §7 risks (RK-01 through RK-18 + RK-OOS-1..3 + RK-TUI-01..05) remain applicable; the unification variant adds the six above.

### 6.4 Risk delta vs. surgical variant

The unification variant accepts **more risk** in exchange for **completeness**:
- Surgical defers TU-002/005/006/Q1/Q2 → low risk, partial closure.
- Unification ships all → higher risk, full closure.

Both variants pass FINAL-REPORT §7's RK-15 + RK-16 gates the same way (Wave-4 parser tests + live-run validation prerequisite).

---

## 7. Release split (Q8 commitment, §9.3)

### 7.1 Three-release proposal

**R1: Task-surface rigor (~3-5 dev-days)**
- TU-001, TU-003, TU-004, TU-007.
- Audit log infrastructure.

**R2: Sprint-runtime + TUI (~7-10 dev-days)**
- SE-001..SE-006.
- TUI top-5.
- Wave-4 parser regression suite must pass.

**R3: Structural consolidation (~5-7 dev-days)**
- TU-002 output-type axis.
- TU-005 SoT YAML.
- TU-006 sub-file materialization.
- Q1/Q2 renames (after A-005 investigation).

**Dependencies:**
- R3 depends on R1 (CRITICAL FAIL hooks referenced by TU-002 gate tables; quality principles enforced through TU-002 gate logic).
- R3 depends on R2 (sprint-side may consume the consolidated YAML for its own classification).
- R1 ⊥ R2 (siblings; independent).

**Total effort:** 15-22 dev-days across three releases. `[inference]`

### 7.2 Why three releases (vs. surgical two)

The unification variant adds R3 because:
1. **TU-002 is a routing-logic change.** It deserves its own review and rollout window separate from rigor changes.
2. **TU-005/TU-006 require A-005 investigation.** Coupling Q1/Q2 renames to the SoT consolidation gives a single coherent cleanup.
3. **R3 unblocks downstream releases.** Once the SoT YAML exists, future tier-keyword tweaks are one-file edits, not four-file edits.

### 7.3 Release-split protocol invocation

Per Q8: **invoke `sc-release-split-protocol`** to verify the three-release seam. `[inference]` This adds adversarial validation that the splits are sound. If the protocol disagrees, fall back to two releases (R1 + combined R2+R3). The unification variant's contract is: **adopt the protocol's recommendation**, even if it differs from the proposed split.

---

## 8. Open questions (carried from FINAL-REPORT §8)

| Q | Recommendation | Status in this release |
|---|----------------|------------------------|
| Q1 (sentinel rename) | RENAME with shim | **ADOPTED** (§4.2, v3.75 → v3.8 runway) |
| Q2 (forensic-caller rename) | RENAME with shim | **ADOPTED** (§4.3) |
| Q3 (output-type precedence) | (a) modifier | **(a) ADOPTED** (§3.6) |
| Q4 (output-type=opinion detection) | (a)+(c) filename + override flag | **(a)+(c) ADOPTED** (§2.3) |
| Q5 (BLOCKED message format) | (a)+(b) CLI prompt + inline header | **(a)+(b) ADOPTED** (§3.5) |
| Q6 (override BLOCKED via flag) | (c) yes with `--reason` + audit log | **(c) ADOPTED** (§2.2, §3.5, §3.8) |
| Q7 (`config/tier-keywords.yaml`) | (a) create SoT | **(a) ADOPTED** (§3.3 TU-005) |
| Q8 (release split) | YES | **ADOPTED with 3-release proposal** (§7) |
| Q9 (severity-enum scope) | (c) map TFEP → Sev | **(c) ADOPTED** (§2.3 SE-005) |
| Q10 (legacy result file migration) | (a) graceful fallback | **(a) ADOPTED** (§2.3 SE-003) |
| Q11 (`--skip-compliance` metering) | (a) add metering now | **(a) ADOPTED** (§3.8 audit log) |
| Q12 (keyword reconciliation) | (c) TU-005 SoT — adopted now (not deferred) | **(c) ADOPTED in R3** (§3.3) |
| Q13 (v3.7 follow-ups) | (c) `--checkpoint-gate-mode` + live-run | **(c) ADOPTED**; live-run is hard prereq for R2 |
| Q14 (six-principles enforcement) | (c) both prompt + checklist | **(c) ADOPTED** (§3.2 + audit log) |

**Newly opened by this variant:**
- **A-005 investigation result.** Pre-merge blocker for Q1/Q2; not a blocker for the rest.
- **TU-007 six-condition list verification.** Carried from FINAL-REPORT §6.1 known gap; remains a pre-merge blocker.
- **Telemetry baseline.** The widened STRICT keyword set may shift baseline metrics. Need a pre-rollout vs. post-rollout comparison plan.

---

## 9. Acceptance criteria

This release ships when:

1. **All new tests in §5.1 + §5.2 pass.**
2. **All regression baselines in §5.4 remain green.**
3. **TU-007 six-condition list verified against LW source.** `[inference]` known gap.
4. **A-005 investigation complete.** Result documented in `docs/a-005-forensic-consumers.md`.
5. **YAML SoT (TU-005) round-trips correctly** across all four consumers.
6. **Skill sub-file structure (TU-006) created** and CI sync handles it.
7. **Audit log infrastructure capturing all classifications** + escape-hatch use.
8. **`MIGRATION-v3.75-to-v3.8.md` published** with every deprecated item.
9. **Release notes** include:
   - "Breaking changes" section enumerating §2.4 items.
   - "Migration guide" cross-reference.
   - Behavior-shift announcement for widened STRICT keywords.
10. **If TUI bundle is included:** P-01 ships only after P-05/P-02/P-03+P-07; `test_monitor_reset_between_tasks.py` passes.

---

## 10. Coverage notes

- **All 11 FINAL-REPORT sections incorporated:** §1 Scope (→ §1), §2 Sources (referenced throughout, especially §3.3 YAML keyword sources), §3 task-unified inventory (→ §2.3, §3.x), §4 /sc:task inventory (preserved + extended in §2.1, §3.x), §5 Overlap matrix (drove §1.2 in-scope decisions for ALL O1-O47 rows), §6 Best-of-breed (full slate adopted, §2.3, §3.x), §7 Risks (→ §6, plus new RK-U-1..6), §8 Open questions (→ §8, all 14 resolved including Q1/Q2/Q3/Q7), §9 Prior-art constraints (→ §4 hard constraints, §1.3 NG list), §10 Shared assumptions (A-001..A-005 carried; A-005 promoted to blocker investigation §5.3), §11 TUI bundle (→ §5.5).
- **Hard constraint compliance:** `/sc:task` is the only canonical command name (§4.1); N1-N12 rename map green (§5.4 baseline); carry-overs renamed with runway, not regressed; no `name: task-unified` reintroduced.
- **`[inference]` callouts:** All FINAL-REPORT `[inference]` tags propagated. Specific to this variant: telemetry impact of widened keywords (RK-U-5); 3-release effort estimates; release-split-protocol fallback behavior.

**Variant signature:** Full structural unification. Adopts complete best-of-breed slate. Q1/Q2 renamed with deprecation runway. TU-002 output-type axis introduced. TU-005 SoT YAML for tier keywords. TU-006 skill sub-file structure materialized. Three-release split proposal. Breaking changes accepted under runway discipline.
