# Research: Data Flow Tracer
**Topic type:** Data Flow Tracer
**Scope:** Wave 0-7 runtime I/O + consumer field map
**Status:** Complete
**Date:** 2026-05-27

---

## Overview

This document maps the runtime data flow through the 7 review waves + 1 mutation wave of the rebuilt `sc-reflect-protocol` skill, per `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md`. Per-wave matrices show INPUTS, AGENTS/SKILLS/MCP invoked, OUTPUTS (artifacts), CONTRACT FIELDS populated, AUDIT ROWS emitted. Consumer field map cross-validates §9.3 against integration-analysis.md.

**Wave-count framing (§4, lines 161-177):** "6 review waves (0-6, all read-only outside `<output>/`) + 1 mutation wave (7)." Wave 7 is the SOLE wave that mutates repo state outside the `<output>/` directory. Every per-step audit row has shape `{wave: <N>, step: <M>, timestamp: <ISO-8601>, outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}` (§4 line 131).

---

## Wave 0 — Parse + Validate + Activate + Hydrate

**Spec range:** §4 lines 134-142, §4.0 lines 179-260.

### Inputs

- CLI flags: `--tasklist <path>`, `--spec <path>`, `--diff <range>`, `--mode {pre|post}`, `--tier {1|2|auto}`, `--depth {quick|standard|deep}`, `--coverage-floor <float>`, `--reviewers <int>`, `--budget-remaining <int>`, `--executor-model <class>`, `--strategy <enterprise|...>`, `--no-promote`, `--promote-anyway`, `--promote-dry-run`, `--promote-mode <auto|task|sprint-release|none>`, `--promote-resume <checkpoint-path>`, `--no-evidence-validator`, `--output <dir>`, `--remediate` (T3 opt-in).
- ENV: `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `EXECUTOR_MODEL_CLASS`.
- Filesystem: existence of `--tasklist`, `--spec`, and (in UC-2) the tasklist's work-unit directory (e.g., `.dev/tasks/to-do/TASK-NNN/`).

### Agents/Skills/MCP

- `mcp__serena__activate_project` (§6.1 line 411) — once, idempotent.
- `mcp__serena__list_memories` (§6.3 line 432) — Wave 0 memory inventory.
- `mcp__serena__read_memory key=reflect/last-pass-{slug}` (§6.3 line 428).
- `mcp__serena__read_memory key=reflect/deviation-patterns-{slug}` (§6.3 line 429).
- Probe for `sc-adversarial-protocol` installation via `mcp__serena__list_memories` OR `Skill('sc-adversarial-protocol', args='--help')` (§14 referenced; mechanism in §4.5 step 5.0).
- `Read` tool for input-path existence + tree-hash file reads (Step 0.4).

### Outputs (artifacts under `<output>/`)

- `<output>/audit.log` opened with machine-readable header (Step 0.8).
- `<output>/artifacts/input-snapshot.yaml` — file list + per-file sha256 + tree-hash (Step 0.4, lines 197-209). Shape: `input_tree_sha256`, `file_list[]`, `file_count`.

### Contract fields populated

- `mode: pre | post` (§3.2 mode selection routing applied at Step 0.1).
- `input_sha256.tasklist`, `input_sha256.spec` (legacy, derivable subset; §4.0 line 216).
- `input_tree_sha256` (AUTHORITATIVE; §9.1 line 578).
- `input_tree_file_count`, `input_tree_snapshot_path`.
- `t2_model_class_diversity: full | degraded` (Step 0.5, line 230).
- `t2_vendor_diversity: multi | single` (Step 0.6, line 238).
- `t2_effective_diversity` (derived; §9.1 line 602).
- `budget_forced_tier_downgrade`, `budget_forced_stop`, `budget_check_skipped`, `forced_tier` (Step 0.9, lines 245-257).
- `executor_class_source: flag | env | log-heuristic | unknown` (telemetry, §9.2 line 668; resolution at Step 0.5b per §7.1 line 478).
- `executor_class_resolved: bool` (§9.2 line 669).
- `executor_exclusion_degraded: bool` (§9.2 line 670; set true if executor removal drops reviewer count below N=2).
- `degraded_components: [<list>]` (telemetry; e.g., `["env-aliases"]`, `["vendor-heterogeneity"]`).
- `memory_hits`, `memory_misses` (telemetry, §9.2 lines 672-673).
- STOP-condition fields: when alias-routing zero + `--tier 2` explicit → `stop_reason: "zero-aliases-tier2-conflict"` (line 225). When `--budget-remaining < 5` → `budget_forced_stop: true`.

### Audit rows

One per numbered step (0.1-0.9): `{wave: 0, step: 1..9, ...}`. Notable rows:

- Step 0.3 outcome: ok (sc-adversarial probe success) or warn (fallback flagged).
- Step 0.4 outcome: ok (snapshot written).
- Step 0.5 outcome: warn (degraded routing) or fail (zero-aliases STOP).
- Step 0.6 outcome: warn (single-vendor) or ok (multi).
- Step 0.9 outcome: warn (budget downgrade) or fail (budget STOP).

---

## Wave 1 — Tier 1 Grounded Single-Agent Reflection

**Spec range:** §4 lines 143-148, §4.1 lines 261-282; §6.1 chain lines 406-419.

### Inputs

- `<output>/artifacts/input-snapshot.yaml` (read-only reference).
- Tasklist, spec, diff hunks from Wave 0 paths.
- Serena memory hits hydrated in Wave 0.

### Agents/Skills/MCP

- **Step 1A (real-code grounding):**
  - `mcp__auggie__codebase-retrieval` — broad context loading per CLAUDE.md rule 9 ("Auggie first").
  - `mcp__serena__get_symbols_overview <file>` — structural map for each touched/spec-referenced file.
  - `mcp__serena__find_symbol <relevant-symbol>` — symbol body.
  - `mcp__serena__find_referencing_symbols <symbol>` — downstream impact.
  - `mcp__serena__get_diagnostics_for_file <file>` — LSP-level issues.
  - `Read` tool re-reading cited file:line ranges (citation-grounding, anti-staleness).
  - `mcp__serena__think_about_collected_information` (scripted checkpoint per §6.4 line 442; output to `<output>/serena-checkpoints.log`, NOT load-bearing).
- **Step 1B (mode-specific evidence):**
  - UC-1: `Task` invocation of `requirements-analyst` agent (§7 line 465) — coverage map.
  - UC-2: inline orchestrator analysis — `git diff` parse + tasklist parse + bipartite match (§7.2 line 498).
  - Step 1B.1 zero-task guard: STOP with `status: partial` if `total_tasks == 0` (UC-1, line 265).
  - Step 1B.2 coverage_undefined route: skip-T1, route to T2 directly if zero requirement IDs (line 269).
  - Step 1B.3 cross-task interaction scan (UC-2 ≥3 tasks, lines 273-281):
    - `mcp__serena__find_symbol` against each task's diff hunks.
    - `mcp__serena__find_referencing_symbols` for each overlap edge.
- **Step 1C (single-agent reflection):**
  - UC-2: `Task` of `root-cause-analyst` (§7 line 463), OR `self-review` agent (§7 line 464) when `S_scope ≤ 3 files` AND `--depth quick`.
  - UC-1 deep: `Task` of `socratic-mentor` (§7 line 472).
  - `mcp__serena__think_about_task_adherence` (UC-1, end of 1C, §6.4 line 444).
- **Step 1D (blind calibration):**
  - `Task` of `confidence-calibrator` agent (§7 line 466) — calibrator model class disjoint from reviewer class per §11.3 line 890-902. Inline fallback marker `calibration: inline-fallback`.

### Outputs (artifacts under `<output>/`)

- `<output>/grounding/` — file:line excerpts captured during Step 1A.
- `<output>/reflection-card.yaml` — T1 reflection card with calibrated scores (per §11.3 line 900).
- `<output>/coverage-map.yaml` (UC-1) — spec-to-tasklist matrix.
- `<output>/deviation-ledger.yaml` (UC-2) — initial 4-category classifications from root-cause-analyst.
- `<output>/grounding-gaps.yaml` (UC-2) — parallel artifact for evidence-insufficient findings (§10.6 line 819).
- `<output>/serena-checkpoints.log` — think_about_* nudge outputs (§6.4 line 447).
- `<output>/interaction-effects.yaml` (UC-2 ≥3 tasks) — cross_task invariant probe entries (line 279).

### Contract fields populated

- `coverage_pct: <float> | null` (UC-1, set null when `coverage_undefined`).
- `coverage_undefined: bool` (Step 1B.2).
- `unmapped_requirements: [...]` (UC-1).
- `tasklist_completion_pct: <float> | null` (UC-2).
- `deviation_count_by_class: {authorized, necessary, drift, regression}` (UC-2 initial).
- `interaction_effects_scanned: bool` (Step 1B.3, line 281).
- `interaction_effects_findings: <int>` (§9.1 line 631).
- `calibrator_diversity: full | degraded` (§9.1 line 603; from Wave 1D).
- `confidence_calibrated: <float>` — initial T1 calibration.
- STOP-condition fields (zero-task): `status: partial`, `coverage_pct: null` with `coverage_undefined: true` (line 265).

### Audit rows

`{wave: 1, step: 1A|1B|1B.1|1B.2|1B.3|1C|1D, ...}`. Step 1A produces per-file evidence rows. Step 1B.1 zero-task fail row halts; Step 1B.2 coverage_undefined warn row routes to T2; Step 1B.3 emits `interaction_effects_scanned: true` evidence row.

---

## Wave 2 — Tier-Decision Gate

**Spec range:** §4 line 149, §5 lines 309-396.

### Inputs

- `<output>/reflection-card.yaml` (calibrated `C` from 1D).
- Structural signals from Wave 1B: `S_scope`, `S_domains`, `S_dev_density`.
- `coverage_pct`, `coverage_undefined` flag.
- CLI hard overrides (`--tier 1|2`, `--depth quick|deep`, `--no-escalate`, `--strategy enterprise`).
- `coverage-floor` (default 0.90).

### Agents/Skills/MCP

- **Inline orchestrator logic** — no Task invocations. Deterministic first-match rule per §5.3 lines 339-350.

### Outputs

- `<output>/artifacts/tier_decision.yaml` (§5.4 lines 360-371). Shape: `selected_tier`, `fired_rule_number`, `composite_score`, `per_signal_breakdown` (scope_size, task_count, blast_radius, spec_density, ambiguity_signals), `escalation_reason`.

### Contract fields populated

- `tier_reached: 1 | 2` (initial; may upgrade to 3 in Wave 6).
- `escalation_rule_matched: <int 1-8>` (§9.1 line 556).

### Audit rows

`{wave: 2, step: gate, evidence_ref: artifacts/tier_decision.yaml}`. The escalation_decision block (§5.6 lines 386-396) is also logged.

**Branching:** PASS_T1 → skip Waves 3, 4; jump to Wave 5. ESCALATE → Wave 3.

---

## Wave 3 — Tier 2 Parallel Heterogeneous Reviewers (conditional)

**Spec range:** §4 lines 150-154, §4.3 lines 283-293; §7.1 lines 474-490.

### Inputs

- `<output>/reflection-card.yaml` (T1 card to be sliced for briefs).
- `<output>/grounding/` — file:line excerpts.
- `<output>/coverage-map.yaml` OR `<output>/deviation-ledger.yaml`.
- Resolved alias-set + executor class from Wave 0.

### Agents/Skills/MCP

- **Step 3A (compose reviewer spec):** inline orchestrator selects model+persona rotation (§7.1 table line 482-486). Executor-class exclusion (§7.1 line 478) removes executor model from rotation.
- **Step 3B.0 (materialize briefs):** writes `<output>/reviewer-briefs/reviewer-<N>.md` (§4.3 line 287). Per brief: T1 card slice + scoped grounding hunks + coverage-matrix slice.
- **Step 3B (spawn N reviewers in parallel via Task):**
  - `Task` of `rf-qa` agent (§7 line 467) — structural QA, `fix_authorization: false`, adversarial-stance.
  - `Task` of `rf-qa-qualitative` agent (§7 line 468) — when artifact is a document (PRD/TDD/tech-ref).
- **Step 3C (per-card blind calibration, ×N parallel):**
  - `Task` of `confidence-calibrator` × N in parallel — disjoint-set rule per §11.3 line 890.
- **Step 3D (distill verdicts):** inline orchestrator merge of N calibrated cards.

### Outputs

- `<output>/reviewer-briefs/reviewer-1.md`, `reviewer-2.md`, ..., `reviewer-N.md`.
- `<output>/reviewer-cards/card-1.md`, `card-2.md`, ..., `card-N.md` (per-reviewer verdicts).
- `<output>/calibration/calibration-1.yaml`, ..., `calibration-N.yaml` (per-card calibrator output).

### Contract fields populated

- `reviewer_cards: [<list of paths>]` (§9.1 line 595).
- `reviewer_models: [...]`, `reviewer_personas: [...]`, `reviewer_vendors: [...]` (telemetry §9.2 lines 662-664).
- `calibrator_diversity: full | degraded` (refreshed per Wave 3C).

### Audit rows

`{wave: 3, step: 3A|3B.0|3B|3C|3D, ...}`. Step 3B emits one row per reviewer spawn (N rows). Step 3C emits N calibration rows.

---

## Wave 4 — Adversarial Merge via sc-adversarial-protocol (conditional)

**Spec range:** §4 line 155, §8 lines 511-535.

### Inputs

- `<output>/reviewer-cards/card-1.md`, `card-2.md`, `card-3.md` (from Wave 3).

### Agents/Skills/MCP — **CROSS-SKILL HANDOFF**

- `Skill sc-adversarial-protocol` (Mode A `--compare`) invocation (§8 lines 521-526):
  ```
  Skill sc-adversarial-protocol with
    --compare <output>/reviewer-cards/card-1.md,card-2.md,card-3.md
    --depth standard
    --focus correctness,coverage,deviation-classification
    --output <output>/adversarial/
  ```
- F1/F2/F3 fallback path orchestrated in Wave 5 step 5.0 (§4.5 lines 297-305) — Wave 4 itself attempts the call; failure cascades to Wave 5's pre-invocation probe.

### Outputs

- `<output>/adversarial/` — debate transcript + merged verdict + scoring (sc-adversarial owns the contents).
- `<output>/adversarial/merged.md` (canonical merged-output path; sc-brainstorm convention `merged_output_path`).

### Contract fields populated

- `adversarial_artifacts_dir: <path>` (§9.1 line 596).
- `adversarial_convergence_score: <float> | null` (§9.1 line 597; null when F3 fires).
- `adversarial_unavailable: bool` (F3 path, §9.1 line 598).
- `merge_method: adversarial | single-reviewer-fallback` (F2 path, §9.1 line 599).
- `fallback_path: null | F1 | F2 | F3` (telemetry §9.2 line 667).

### Audit rows

`{wave: 4, step: invoke|merge, evidence_ref: adversarial/merged.md}`. F1/F2/F3 retries each emit one row.

**Branching to Wave 5:** `convergence_score: null` (F3 path) flows into Wave 5 routing — see "Null convergence sentinel-collision trace" below.

---

## Wave 5 — Synthesis + Evidence-Validator + Report

**Spec range:** §4 lines 156-158, §4.5 lines 295-305, §11.2 lines 869-880, §11.5 lines 910-926.

### Inputs

- T1 path: `<output>/reflection-card.yaml`.
- T2 path: `<output>/adversarial/merged.md` (or single-reviewer fallback verdict if F2).
- All grounding hunks from Wave 1A.
- `<output>/grounding-gaps.yaml` (UC-2, may have been populated in Wave 1).
- `<output>/deviation-ledger.yaml` (UC-2).
- `<output>/coverage-map.yaml` (UC-1).
- `<output>/artifacts/input-snapshot.yaml` (for drift re-verify).

### Agents/Skills/MCP

- **Step 5.0 (sc-adversarial pre-invocation probe, F1/F2/F3 fallback)** — only when T2 ran but Wave 4 call deferred (lines 299-305).
- **Step 5.x (input_sha256 drift guard)** — re-read input tree, recompute `input_tree_sha256`, compare to Wave 0 snapshot (§4.0 lines 210-215; §4 line 158).
- **Citation re-Read pass (§11.5 lines 910-926):** `Read` tool re-reads every cited `file:line` per the 5-tool-call window. Budget policy: `full_reread` if citations ≤20, `sampled` if >20.
- **Inline orchestrator synthesis** — no new agent per §7.2 line 499.
- **`Task` of `evidence-validator` agent (§7 line 470, §11.2 lines 869-880)** — non-negotiable final gate. Drops unfounded items.
- **`Task` of `audit-validator` agent (§7 line 469)** — when ≥20 findings, 10% spot-check (lighter alternative).
- `mcp__serena__think_about_whether_you_are_done` (§6.4 line 445; scripted, logged but NOT gating).
- `mcp__serena__write_memory key=reflect/last-pass-{slug}` (§6.3 line 430).
- `mcp__serena__write_memory key=reflect/deviation-patterns-{slug}` (§6.3 line 431).

### Outputs

- `<output>/REPORT.md` — final synthesized report.
- `<output>/grounding-gaps.yaml` — updated to include dropped citations from evidence-validator (§11.2 line 877).
- `<output>/deviation-ledger.yaml` — finalized 4-category classifications.
- `<output>/return-contract.yaml` — main contract artifact.
- `<output>/serena-checkpoints.log` — updated with whether_you_are_done output.
- Updated serena memories (last-pass, deviation-patterns).

### Contract fields populated (this wave finalizes most stable contract fields)

- `status: success | partial | failed` (§9.1 line 550; final routing).
- `tier_reached: 1 | 2` (finalized).
- `report_path: <abs path to REPORT.md>` (§9.1 line 553).
- `audit_log_path: <abs path>` (§9.1 line 554).
- `confidence_calibrated: <float>` (finalized).
- `citations_total`, `citations_revalidated`, `citations_dropped`, `citations_dropped_extrapolated`, `citations_inferred` (§9.1 lines 585-589).
- `citation_budget_policy: full_reread | sampled` (§9.1 line 590).
- `evidence_validator_ran: bool` (§9.1 line 591).
- `input_drift_detected: bool` (§9.1 line 581).
- `input_drift_diff: [...]` (§9.1 line 582) — populated when drift detected.
- `deviation_count_by_class.{authorized, necessary, drift, regression}` (finalized).
- `deviation_register_path: <abs path>` (§9.1 line 571).
- `grounding_gaps_path: <abs path>` (§9.1 line 572).
- All asymmetric-cost flags: `cannot_validate_without_user_input`, `regression_present`, `unauthorized_deviation_present`, `blocked_by_low_confidence`, `spec_is_wrong`, `user_decision_required`, `needs_human_decision` (§9.1 lines 612-618).
- `per_task_verdicts[]` (§9.1 lines 621-627) — UC-2 multi-task tasklist only.
- `best_practice_grade: <int 0-5>` (UC-1, §9.1 line 562).
- Wave durations + token usage (telemetry §9.2 lines 660-661).

### Audit rows

`{wave: 5, step: 5.0|5.x|reread|validator|synthesis|finalize, ...}`. Notable:

- Step 5.0 F1/F2/F3 retries: warn or fail outcomes.
- Step 5.x drift guard: ok or fail (fail → STOP with `input_drift: true`, `status: partial`).
- Evidence-validator: ok (zero-drop with `zero-drop-flag: true` marker) or warn (≥1 drop, `status: partial`).
- `evidence_validator_ran: false` (fall-back path) → forces `status: partial`.

**Branching to Wave 6:** T3 fires only if user opts in via `--remediate`.
**Branching to Wave 7:** UC-2 only, conditional on §14.5.2 9-condition gate (default-on, suppress via `--no-promote`).

---

## Wave 6 — Tier 3 Remediation Handoff (conditional, opt-in)

**Spec range:** §4 line 159, §8 line 512.

### Inputs

- `<output>/REPORT.md`.
- `<output>/deviation-ledger.yaml`.
- `<output>/grounding-gaps.yaml`.
- `needs_human_decision: bool` (from §9.1 line 618).

### Agents/Skills/MCP — **CROSS-SKILL HANDOFF**

- `Skill task-builder` invocation (§8 line 512). Generates corrective MDTM task file. Reads `report_path`, `deviation_register_path`, `grounding_gaps_path` (§9.3 row 6).
- Gated on `--remediate` opt-in (§4.5 line 303, F3 path).

### Outputs

- `<output>/remediation/` — task-builder workspace.
- `<repo-rooted>/.dev/tasks/to-do/TASK-NNN/tasklist-index.md` — the materialized task file.

### Contract fields populated

- `tier_reached: 3` (upgraded from 2 when Wave 6 ran).
- `remediation_offered: bool` (§9.1 line 606).
- `remediation_accepted: bool | null` (§9.1 line 607).
- `task_file_path: <path> | null` (§9.1 line 608).

### Audit rows

`{wave: 6, step: handoff|generated, ...}`.

**Cross-skill note:** Wave 6 mutates files OUTSIDE `<output>/` (the new task file under `.dev/tasks/to-do/`). This is the **only** SRP-boundary exception in the review waves (Waves 0-6), and it is justified because the file produced is itself an opt-in user-authorized artifact (`--remediate` flag), not a state mutation of existing files. Wave 6 also INVALIDATES Wave 5 citations — see Wave 7 step 7.2 re-Read requirement (§14.5.2 cond 6a, line 1218; W-A4 telemetry).

---

## Wave 7 — Promotion Mutation (UC-2 only)

**Spec range:** §4 lines 160-175, §14.5 lines 1185-1367.

### Inputs

- `<output>/return-contract.yaml` (all 9 gate condition fields — see §14.5.2 below).
- `<output>/artifacts/input-snapshot.yaml` (for re-verify drift).
- Source path: resolved from `--tasklist` or `--scope`.
- Tasklist frontmatter (for cond 5a/5b checks).
- Override flags from Wave 0: `--no-promote`, `--promote-anyway`, `--promote-dry-run`, `--promote-mode`, `--promote-resume`.

### 9-condition strict gate (§14.5.2 lines 1198-1214)

| # | Field consumed | Pass condition |
|---|---|---|
| 1 | `mode` | `== post` |
| 2 | `status` | `== success` (override: `--promote-anyway` allows `partial`) |
| 3 | `tasklist_completion_pct` | `== 1.0` |
| 4 | `deviation_count_by_class.{drift, regression}` | both `== 0` |
| 5a | tasklist frontmatter presence | parseable + `status` field present |
| 5b | tasklist frontmatter status | `== done` (terminal value) |
| 6a | `citations_dropped` | `== 0` (sample-count, NOT extrapolated, in sampled mode) |
| 6b | `grounding_gaps_path` empty per canonical YAML-parse | `findings: []` or absent |
| 7 | `input_drift_detected` | `== false` |
| 8 | `needs_human_decision`, `user_decision_required` | both `== false` |
| 9 | `convergence_score` not null when `tier_reached == 2` | non-null OR `tier_reached == 1` (vacuous) |

### Agents/Skills/MCP

- **Step 7.1 (resolve adapter):** inline orchestrator selects `task` | `sprint-release` | `none` from source path per §14.5.1 table (line 1187).
- **Step 7.2 (re-verify 9 conditions):** if Wave 6 ran, re-Read every cited file:line via `evidence-validator` agent re-invocation; recompute `citations_dropped` against current file state (§14.5.2 line 1218, W-A4).
- **Step 7.3 (collision check):** filesystem inspection of destination path.
- **Step 7.3.5 (cross-fs only):** write `<output>/promotion-checkpoint.yaml` with `state: pending` (§14.5.5 line 1261).
- **Step 7.3.6:** append `pending: true` row to `<output>/promotion-log.yaml` BEFORE the mv (W-A6, line 1287).
- **Step 7.4 (MUTATE):** invoke `mv <source> <destination>` (atomic same-fs via POSIX `rename(2)`; copy+verify+remove+fsync cross-fs — §14.5.5 line 1259).
- **Step 7.5 (SHA verify):** re-read moved tree; compute tree-hash; assert match vs `source_sha256_before`.
- **Step 7.6 (finalize):** flip log `pending: false`; transition checkpoint `state: move-complete`; emit audit.log row.
- **Step 7.7:** write all `promotion_*` fields into `<output>/return-contract.yaml`.

### Outputs

- `<output>/promotion-log.yaml` (always; §14.5.6 lines 1305-1341).
- `<output>/promotion-checkpoint.yaml` (cross-fs only).
- Repository mutation: source directory removed from `.dev/tasks/to-do/TASK-*` OR `.dev/releases/current/<release>/`; destination created at `.dev/tasks/done/TASK-*` OR `.dev/releases/complete/<release>/`.
- Updated `<output>/return-contract.yaml` with `promotion_*` block.

### Contract fields populated (full promotion block, §9.1 lines 640-652)

- `promotion_action: moved | skipped | rejected | failed | already-promoted | resumed | dry-run | not-applicable`.
- `promotion_adapter: task | sprint-release | none | null`.
- `promotion_source: <abs path>`.
- `promotion_destination: <abs path>`.
- `promotion_log_path: <abs path>`.
- `promotion_gate_passed: bool`.
- `promotion_skip_reason`, `promotion_fail_reason`.
- `promotion_override_used: --promote-anyway | --promote-resume | null`.
- `promotion_rollback_command`.
- `promotion_checkpoint_path` (cross-fs only).
- `promotion_cross_fs: bool`.
- `promotion_pending: bool` (only true in crashed-mid-run log entry).
- `citation_revalidation_at_promotion: bool` (§9.1 line 592, set true if Wave 6 ran).

### Audit rows

`{wave: 7, step: 7.1|7.2|7.3|7.3.5|7.3.6|7.4|7.5|7.6|7.7, ...}`. Step 7.4 outcome decides everything downstream:

- ok → `promotion_action: moved` or `resumed` or `already-promoted`.
- fail (`destination_collision`, `source_disappeared`, `mv_error`, `sha_mismatch`) → `promotion_action: rejected` or `failed`.

---

## Consumer Field Map (§9.3 — verified against integration-analysis.md)

§9.3 Consumer Field Map is at lines 676-695. The table below verifies each row against the actual integration-analysis.md findings.

### Row 1 — `sc-troubleshoot-protocol` Wave 6 (Phase B/D)

**Surface:** Skill-to-skill invocation.
**Load-bearing fields (5):** `status`, `tier_reached`, `confidence_calibrated`, `regression_present`, `needs_human_decision`.
**Routing semantics:**
- `status: failed` → halts troubleshoot.
- `regression_present: true` → forces Tier-3 troubleshoot path.
- `needs_human_decision: true` → surfaces to user before continuing.

**Integration verify:** integration-analysis.md Executive Summary line 12 confirms only `sc-troubleshoot-protocol/refs/report-template.md` (Tier 3 post-`/task` recommendation) references reflect externally. Reverse-direction invocation per §8 line 516.

### Row 2 — `superclaude sprint run` (executor.py TurnLedger)

**Surface:** CLI consumer of `return-contract.yaml`.
**Load-bearing fields (5):** `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`, `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade`.
**Routing semantics:**
- `status: partial OR failed` → halts the phase.
- `per_task_validation_strength < 0.70` → flags task for re-execution.
- `deviation_class == regression` → triggers TurnLedger rollback.
- `budget_forced_tier_downgrade: true` → adjusts subsequent reflect-call budget.

**Integration verify:** integration-analysis.md confirms `executor.py:1605` (notify_phase_complete) and `:1728` (notify_sprint_complete) are wiring points. Cleanest wiring point pseudocode (lines 106-122) reads `reflect_result.status` and `reflect_result.deviation_class` — matches the load-bearing fields. **Minor divergence:** the §9.3 row lists `per_task_verdicts[].per_task_validation_strength` but integration-analysis.md pseudocode reads `reflect_result.summary` (a generic field, not in §9.1 contract). The contract is more specific than the analysis hand-wave; §9.3 is correct.

### Row 3 — `sc-task-protocol` end-of-task hook

**Surface:** Inline post-execution.
**Load-bearing fields (5):** `status`, `tier_reached`, `deviation_count_by_class`, `confidence_calibrated`, `needs_human_decision`.
**Routing semantics:**
- `status: success AND confidence_calibrated ≥ 0.85` → mark task done.
- `deviation_count_by_class.regression > 0` → escalate to troubleshoot.
- `needs_human_decision: true` → surface Grounding Gaps to user.

**Integration verify:** integration-analysis.md "Cross-Pipeline Recommendation" Change 3 (lines 335-341) wires reflect AS the Post-Completion Step 3 in `task/SKILL.md:240`. The Variant A pseudocode (lines 283-297) reads `status`, `promotion_action`, deviation register — matches except `confidence_calibrated` and `tier_reached` are not explicitly enumerated in the pseudocode. §9.3 is authoritative.

### Row 4 — `sc:roadmap` validation gate

**Surface:** Roadmap pipeline post-step.
**Load-bearing fields (4):** `status`, `coverage_pct`, `unmapped_requirements`, `best_practice_grade`.
**Routing semantics:**
- `coverage_pct < 0.90 OR unmapped_requirements != []` → roadmap re-runs spec coverage.
- `best_practice_grade < 3` → flag for review.

**Integration verify:** integration-analysis.md "Roadmap pipeline" section (lines 158-230) confirms roadmap currently does NOT invoke reflect; integration is a NEW wiring point (Change 2, lines 325-333). §9.3 lists the fields that the FUTURE wiring would consume.

### Row 5 — `sc:tasklist` generator gate

**Surface:** Tasklist pipeline post-step.
**Load-bearing fields (4):** `status`, `coverage_pct`, `unmapped_requirements`, `coverage_undefined`.
**Routing semantics:**
- `coverage_undefined: true` → tasklist generator emits "spec too sparse" warning.
- `coverage_pct < 0.90` → emit warning.

**Integration verify:** integration-analysis.md does not include a dedicated `sc:tasklist` section. This row in §9.3 is FORWARD-LOOKING (planned consumer). **DIVERGENCE noted:** §9.3 names this consumer but integration-analysis.md doesn't validate it — implied via roadmap-to-tasklist downstream chain (line 220 mentions tasklist generation consuming the roadmap). This row should be flagged for explicit integration-analysis follow-up.

### Row 6 — `task-builder` skill (Wave 6 handoff)

**Surface:** Wave 6 (T3) handoff.
**Load-bearing fields (4):** `report_path`, `deviation_register_path`, `grounding_gaps_path`, `needs_human_decision`.
**Routing semantics:**
- Reads three paths to materialize BUILD_REQUEST.
- `needs_human_decision: true` → BUILD_REQUEST prompts user resolution.

**Integration verify:** §8 line 512 + §4 line 159 confirm task-builder is invoked at Wave 6. The three paths are produced by Wave 5. This is the canonical T3 handoff — internal consumer.

### Row 7 — Wave 7 promotion adapters (in-skill internal consumer)

**Surface:** Internal consumer.
**Load-bearing fields:** ALL 9-condition-gate inputs (`mode`, `status`, `tasklist_completion_pct`, `deviation_count_by_class.{drift,regression}`, `citations_dropped`, `input_drift_detected`, `needs_human_decision`, `user_decision_required`, `convergence_score`, `tier_reached`, frontmatter check).
**Routing semantics:** all 9 must pass for mutation; any fail → `promotion_action: skipped/rejected`.

**Integration verify:** matches §14.5.2 lines 1198-1214 exactly.

### Row 8 — CI (`make reflect-eval` / `make reflect-eval-quick`) → grader.py

**Surface:** grader.py.
**Load-bearing fields:** all `per_task_verdicts[]` sub-fields + `status` + `evidence_validator_ran` + `audit_log_path`.
**Routing semantics:** scores 6 grading dimensions per §12.1, asserts thresholds per iteration's `grading.json`.

**Integration verify:** §12.4 grader DSL extensions (line 989) and §12.1 grading dimensions (line 947) confirm. Per researcher 07's scope.

### Row 9 — Meta-eval (`runs.jsonl` aggregator, §15.1)

**Surface:** Cross-run analytics.
**Load-bearing fields:** `status`, `tier_reached`, `wave_durations_ms`, `token_usage`, `convergence_score`, `t2_model_class_diversity`, `t2_vendor_diversity` (from telemetry).
**Routing semantics:** aggregated across runs, not per-run.

**Integration verify:** §15.1 metrics export (line 1385) is the source for this row. Telemetry block §9.2 lines 660-674 supplies these fields.

### §9.3 vs integration-analysis.md divergence summary

| Row | Divergence | Severity |
|---|---|---|
| 2 (sprint) | analysis uses `result.summary`; contract uses specific `per_task_verdicts[]` sub-fields | low — contract is authoritative |
| 3 (sc-task) | analysis pseudocode is incomplete enumeration vs §9.3 | low — analysis is illustrative |
| 5 (sc:tasklist) | analysis lacks dedicated section; row is forward-looking | medium — flag for integration follow-up |
| 4 (sc:roadmap) | analysis confirms wiring is NEW (not current state) | none — both agree consumer is planned |

Overall the §9.3 table is **substantively consistent** with integration-analysis.md but is **more authoritative** than the analysis: when they disagree on field-name precision, the contract wins. The §9.3 table fulfills its spec-panel F-2 directive (lift implicit coupling out of integration-analysis.md into the maintained contract — §9.3 preamble line 680).

---

## Bonus 1: `input_sha256` tree-hash flow

**Spec range:** §4.0 Step 0.4 lines 183-216; §9.1 lines 575-582.

### Files hashed at Wave 0 (Step 0.4)

The tree consists of (line 184-188):

1. `tasklist_path` itself (always present in UC-2).
2. `spec_path` (when `--spec` provided).
3. Every file referenced by relative/absolute path FROM the tasklist body (link-following, depth = 1).
4. For UC-2 tasklist inputs that resolve under a work-unit directory (e.g., `.dev/tasks/to-do/TASK-NNN/`), every file under that directory tree (`find <work-unit-dir> -type f`).

Computation (lines 191-195):
```
file_list = sorted([(rel_path, sha256(read(abs_path))) for path in input_tree])
input_tree_sha256 = sha256(serialize_as_json(file_list))
```

Persisted to `<output>/artifacts/input-snapshot.yaml` (lines 197-208).

### Files re-hashed at Wave 5 / Wave 7.2

- **Wave 5 (Step 5.x, §4 line 158):** re-read input tree, recompute `input_tree_sha256`, compare to snapshot.
- **Wave 7 step 7.2 (§4 line 165-166, §14.5 cond 7):** same re-hash invariant check.

### Drift guard firing

When the recomputed tree-hash differs (any file added, removed, modified, renamed):

1. STOP with `input_drift` flag (§4.0 line 210).
2. Emit BOTH old + new SHAs.
3. Emit per-file diff (which files changed) into `input_drift_diff`.
4. Route to `status: partial` (§9.1 line 581).
5. Promotion gate cond 7 `no_input_drift: pass | fail` fails — blocks Wave 7 mutation.

### Backward-compat (line 216)

Legacy `input_sha256: {tasklist: <hex>, spec: <hex>}` is preserved as a derivable subset (first two entries of `file_list`). Both fields emitted in v1.0. The tree-hash is the authoritative invariant; the legacy field is for backward-compat consumers per §9.4 evolution policy.

---

## Bonus 2: `convergence_score: null` (F3 path) sentinel-collision trace

**Spec range:** §4.5 Step 5.0 lines 295-305 (F1/F2/F3 fallback); §8 lines 530-535 (null routing); §14.5.2 cond 9 line 1214.

### Origin — Wave 4 fail

- Wave 4 attempts `Skill sc-adversarial-protocol` invocation.
- If the skill is uninstalled or unavailable, Wave 5 step 5.0 probe fires (line 299):
  - **F1:** retry probe once after short backoff (line 301).
  - **F2:** on second probe failure, use highest-calibrated single Tier 2 reviewer verdict as fallback merged result; emit `merge_method: single-reviewer-fallback` (line 302).
  - **F3:** route to Tier 3 only if user explicitly opts in via `--remediate`; otherwise emit `adversarial_unavailable: true` and `status: partial` (line 303).

### Wave 5 routing on F3

- `convergence_score: null` enters return contract (§8 line 530).
- `adversarial_unavailable: true` (§9.1 line 598).
- `status: partial` (§4.5 line 303).
- Downstream consumers MUST treat `null` as a distinct state, NOT silently route as `< 0.60` or `≥ 0.75` (§8 lines 532-535):
  - Consumers route on `merge_method` FIRST: if `single-reviewer-fallback`, use single-reviewer verdict's calibrated confidence as routing input.
  - A null comparison is undefined behavior; implementations MUST guard explicitly.
  - For sprint executor.py: null `convergence_score` → `status: partial` AND `next_action: halt-phase-for-review`.

### Wave 7 promotion gate cond 9 (line 1214)

- `tier_reached == 2 AND convergence_score == null` (F3 path) → cond 9 fails → promotion blocked regardless of other conditions.
- T1-only runs satisfy cond 9 vacuously (`tier_reached == 1` means adversarial-result clause does not apply).
- Promotion-log `gate_evaluation.adversarial_result_present: fail` for F3 + T2; `n/a` for T1 (§14.5.6 line 1330).

### Why this is "Whittaker Attack 3" hardening

Sentinel collision: a naive consumer treating `null < 0.60` as "PASS" (truthy fallback) or `null < 0.60` as "FAIL" (falsy comparison) would silently mishandle F3. The spec mandates explicit null guards at every consumer surface, and the promotion gate blocks mutation entirely rather than risk silent promotion of an unmerged verdict.

Acceptance test exists: §14.5.7 `promotion-blocked-by-null-convergence` eval case (line 1352) — `tier_reached == 2 AND convergence_score == null` (F3 simulated) → `action: rejected`, `adversarial_result_present: fail`.

---

## Summary

**Artifacts produced (file paths, all absolute):**

- `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/tasks/to-do/TASK-RF-20260527-043715-sc-reflect-rebuild/research/08-data-flow-tracer.md` (this file)

**Key findings (load-bearing for SKILL.md prose):**

1. **Wave count is "6 review + 1 mutation"** — SRP boundary is intentional: only Wave 7 mutates outside `<output>/`. Wave 6 is an opt-in user-authorized exception (writes a new task file under `.dev/tasks/to-do/` via task-builder handoff).
2. **Per-step audit convention** — every numbered step (not every wave) emits one row to `<output>/audit.log`. This resolves the 9-wave vs 7-wave structural debate per §4 line 131.
3. **§9.3 Consumer Field Map is substantively consistent with integration-analysis.md** — minor divergences exist (row 2 field-name precision, row 5 forward-looking) but §9.3 is authoritative per spec-panel F-2 directive.
4. **Cross-skill handoffs are TWO:** Wave 4 → `sc-adversarial-protocol` (with F1/F2/F3 fallback owned by Wave 5 step 5.0); Wave 6 → `task-builder` (gated on `--remediate` opt-in).
5. **MCP graph is dominated by serena** in Waves 0-1 (memory + symbol chain) and again in Wave 5 (write_memory persist). Auggie fires once at Wave 1A for broad context loading. No MCP calls in Waves 2, 3 (orchestrator-only logic + parallel Task spawns), 4 (sc-adversarial owns its tool surface), 6 (task-builder owns), 7 (filesystem operations only).
6. **input_tree_sha256 is hashed once (Wave 0 Step 0.4) and re-verified twice** (Wave 5 step 5.x AND Wave 7 step 7.2). Drift → `status: partial` + `input_drift_detected: true` + gate cond 7 fail.
7. **`convergence_score: null` (F3 path) is a hardened sentinel** — all consumers MUST explicitly guard against null; promotion gate cond 9 blocks T2-with-null-convergence regardless of other conditions. Acceptance test `promotion-blocked-by-null-convergence` validates the hardening.
8. **The 9-condition promotion gate maps 1:1 to 11 atomic gate_evaluation fields** in `promotion-log.yaml` (conditions 5 and 6 are split into 5a/5b and 6a/6b per spec-panel W-1 + C1).
9. **Citation revalidation at promotion** (`citation_revalidation_at_promotion: bool`) — when Wave 6 ran, Wave 7 step 7.2 MUST re-Read every cited file:line via evidence-validator and recompute `citations_dropped` against current file state (NOT trust Wave 5 result). W-A4 fix.
10. **Per-wave contract-field population is roughly:** Wave 0 sets input/env-routing fields (~12); Wave 1 sets coverage/deviation/calibration fields (~10); Wave 2 sets `tier_reached` + `escalation_rule_matched`; Wave 3 sets reviewer telemetry; Wave 4 sets `adversarial_*` (~5); Wave 5 sets the bulk of stable contract (~25 fields including `status`); Wave 6 sets T3 fields (~4); Wave 7 sets `promotion_*` block (~13).
