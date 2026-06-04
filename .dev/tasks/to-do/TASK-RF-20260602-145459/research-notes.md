# Research Notes: Implement 4 Medium-Complexity Serena Adoptions (FR-RV3-MED.1–4) into sc-reflect-protocol

**Date:** 2026-06-02
**Scenario:** A (Explicit — driven by a spec-panel-reviewed release spec)
**Depth Tier:** Deep (6 researchers)
**Track Count:** 1 (single track — all 4 FRs edit the shared `sc-reflect-protocol/SKILL.md` surface + refs; not independent file sets)
**Source spec (BUILD_REQUEST):** `.dev/releases/current/Reflect-V3.5-Serena_Mediums/05-spec-medium-complexity.md`

---

## EXISTING_FILES

**Primary integration surface (source of truth — edit here, then `make sync-dev`):**
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1585 lines). Verified anchors:
  - §6.1 Mandatory evidence-gathering chain — header `:354`; step 4 `find_referencing_symbols` `:362`; step 5 `get_diagnostics_for_file` `:363`; step 6 re-Read `:364`. → FR-1 step 4.5 inserts after `:362`; FR-4 step 5.5 inserts between `:363` and `:364`.
  - §4 Wave architecture — `:122`; per-step audit-emit convention `:124`; Wave 0 steps `:127-135` (0.7 activate `:134`); Wave 6 task-builder `:152`.
  - §4.0 Wave 0 detail `:172-225`; §4.1 Wave 1 (1B.3 cross-task scan) `:233-241`; §4.5 Wave 5 `:249-257`.
  - §6.3 memory pattern `:373-383`; §6.5 fail-open `:397-399`.
  - §7 agent delegation (task-builder Wave 6 `:417`); §8 cross-skill (task-builder `:458`).
  - §9.1 stable contract `:491-599` (`regression_present` `:557`); §9.2 telemetry `:601-618` (`degraded_components` `:610`); §9.3 consumer field map `:620-636`.
  - §10.4 Regression `:718-730` (detection signals; `--rerun-tests` opt-in `:725` — VERIFIED); §10.5 precedence `:732`; §10.6 Grounding Gaps `:736-755`.
  - §14 Error Handling Matrix `:1015-1071` (Serena unavailable `:1042`; `write_memory` fails at Wave 5 `:1067`); §14.5.2 promotion gate cond 4 `:1097`.
  - §15 Token Cost Profile `:1266-1276` (T1 ~3-8k, T2 ~35-70k; hard-kill 1.25× `:1274`).
- refs/ directory (CONFIRMED present): `reflection-rubric.md`, `deviation-taxonomy.md`, `reviewer-spec.md`, `ops-integration.md`, `report-template.md`, `promotion-adapters.md`, `input-resolution.md`, `grader-extensions.md`, `cost-profile.yaml`, `coverage-mapping.md`, **`remediation-handoff.md`** (the FR-3 Wave 6 handoff surface — already documents the task-builder BUILD_REQUEST chain).
- **OQ-M8 RESOLVED**: `refs/return-contract.yaml` is **ABSENT**. The return contract is **inline in SKILL.md §9**. → All §5 contract additions edit SKILL.md §9.1/§9.2, NOT a separate YAML file.

**Eval workspace (CONFIRMED):** `.dev/eval-workspaces/sc-reflect/` with `cases/` (existing: `falsifier-suite`, `post-large-diff-mixed`, `post-small-diff-clean`, `pre-trivial-coverage-gap`, `promotion`), `grader.py`, `aggregate_iteration.py`, `SPEC.md`, `evals/`, `iterations/`. New cases = dir-per-case under `cases/`.

**MDTM template (CONFIRMED):** `.claude/templates/workflow/02_mdtm_template_complex_task.md` (Template 02 — complex).

**Cross-spec dependency partner (CONFIRMED in-flight):** `.dev/tasks/to-do/TASK-RF-20260602-135209/` = "Implement 8 Low-Complexity Serena Adoptions (FR-RV3-LOW.1–8)". FR-RV3-LOW.7 (`get_current_config`) is the version-fingerprint/backend/availability substrate this medium spec's FR-1/FR-2/FR-4 consume (spec OQ-M5). Its research set (`research/01-07`) covers shared insertion-point/refs/eval ground and can be cross-referenced.

## PATTERNS_AND_CONVENTIONS

- Per-step audit emit (SKILL.md:124): fixed 5-field row `{wave, step, timestamp, outcome, evidence_ref}` → complex per-invocation data goes to an artifact referenced by `evidence_ref` (this is why FR-4 `verify_invocations[]` must be an artifact, per spec M-ARC1).
- Fail-open (§6.5): missing/excluded/error → `degraded:[tool]` → fallback → never abort.
- Telemetry vs contract split (§9.4): contract fields bump `contract_version`; telemetry fields don't.
- Frontmatter `allowed-tools` lists the Serena tool surface — new tools (`type_hierarchy`, `onboarding`, `prepare_for_new_conversation`, `execute_shell_command`) must be added; `check_onboarding_performed` must NOT (low-spec concern).
- SoT discipline (CLAUDE.md): edit `src/superclaude/`, then `make sync-dev`; NEVER edit `.claude/` mirror or stage it.

## GAPS_AND_QUESTIONS

These map to the spec's 10 Open Questions (OQ-M1–M10). Research must verify/resolve where possible:
- OQ-M8 (return-contract location) → **RESOLVED: inline in SKILL.md §9** (no separate yaml).
- OQ-M1 (`prepare_for_new_conversation` signature) — verify against live Serena MCP surface; if unresolvable at research time, document as runtime probe.
- OQ-M2 (`execute_shell_command` default timeout + `--rerun-tests` migration) — confirm `--rerun-tests` is referenced only at SKILL.md:725 (VERIFIED) and map the deprecation surface.
- OQ-M3 (LSP `type_hierarchy` coverage) — runtime/empirical; document as probe.
- OQ-M5 (low-spec FR-7 availability) — the partner task folder exists; confirm whether FR-7 `get_current_config` is built/merged or whether the medium task must ship a minimal inline probe.
- OQ-M9/M10 (exit-code taxonomy completeness; input-hash artifact-exclude set) — verify §10.4 detection signals + §4.0 input_tree_sha256 construction (SKILL.md:174,193).

## RECOMMENDED_OUTPUTS

6 research files in `research/`:
- `01-skill-insertion-points.md` — exact SKILL.md anchors + insertion text neighborhoods for all 4 FRs.
- `02-patterns-conventions.md` — audit-emit, fail-open, telemetry/contract split, flag declaration, allowed-tools editing pattern.
- `03-refs-and-handoff-surface.md` — which refs each FR edits; deep read of `remediation-handoff.md` (FR-3), `reflection-rubric.md`, `deviation-taxonomy.md`, `reviewer-spec.md`, `ops-integration.md`; confirm inline §9 contract (OQ-M8).
- `04-eval-workspace-conventions.md` — existing eval-case structure, grader.py, SPEC.md; how to scaffold the 6 new cases.
- `05-mdtm-template-and-examples.md` — Template 02 PART 1 rules (A3 granularity, B2 self-contained, L1-L6); the low-spec task file as a worked example.
- `06-cross-spec-and-oq-probes.md` — low-spec FR-7 dependency status; OQ-M1/M2/M3/M5/M9/M10 resolution/deferral; §10.4 + §14.5.2 + input_tree_sha256 verification.

## SUGGESTED_PHASES

(Builder will structure; suggested skeleton for a Template-02 task file)
- Phase 1: Preparation (read spec, SKILL.md anchors, confirm OQ resolutions, cross-spec FR-7 status)
- Phase 2: FR-4 `execute_shell_command` (ship FIRST) — safety envelope, exit-code taxonomy, §6.1 step 5.5, §10.4/§14.5.2 wiring, §9 contract fields, allowed-tools, ops-integration WARNs, refs/rubric — per-sub-requirement items
- Phase 3: FR-2 `onboarding` — Wave 0.7b, `--onboard`, NFR-7 budget
- Phase 4: FR-3 `prepare_for_new_conversation` — Wave 6 / remediation-handoff.md, handoff schema, write_memory fallback, retention-prefix extension (cross-spec)
- Phase 5: FR-1 `type_hierarchy` (ship LAST) — §6.1 step 4.5, Wave 1B.3, backend probe, `--with-hierarchy`
- Phase 6: Eval cases (6 dirs) + telemetry-completeness + Serena-disabled/read-only integration
- Phase 7: sync-dev + verify-sync + QA gates + completion
- Open Questions: OQ-M1/M3 (runtime probes) documented as task-level risks, not item bases.

## TEMPLATE_NOTES

- Template **02** (complex) — discovery + multi-FR build + eval-authoring + verification phases.
- Tier **Deep** — 4 FRs, ~7 source files + 6 eval dirs, cross-spec dependency, contract/schema changes, 8 NFRs, 10 OQs.
- Granularity (A3): individual items per FR sub-requirement (each acceptance criterion / each safety-envelope control / each eval case its own item) — NOT "implement FR-4" as one item.
- QA_GATE_REQUIREMENTS: PER_PHASE (Template 02). VALIDATION: `make sync-dev` + `make verify-sync` + markdownlint on edited SKILL.md/refs. TESTING: eval-case authoring (the "tests" for a skill protocol) — NONE in the pytest sense, but eval cases are mandatory.

## AMBIGUITIES_FOR_USER

- The spec ships the 4 FRs as **separate PRs** (FR-4 → FR-2 → FR-3 → FR-1). This task file builds ONE MDTM covering all 4 in phase order; the executor/operator can still land them as separate PRs per phase. If the user wants 4 separate task files (one PR each), that would be a multi-track split — but the FRs share the SKILL.md surface and a common contract bump, so single-track-with-phases is the correct default. Flagging for awareness; proceeding single-track.
- OQ-M1 (`prepare_for_new_conversation` signature) and OQ-M3 (LSP `type_hierarchy` coverage) are genuine runtime unknowns the spec already flagged — these will be task-level risks/probe-first items, not silently assumed.
