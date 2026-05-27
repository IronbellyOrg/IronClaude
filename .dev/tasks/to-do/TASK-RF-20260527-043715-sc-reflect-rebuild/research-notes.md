# Research Notes: Build sc-reflect-protocol skill (tiered reflection, Wave 0-7, 4-category deviation taxonomy, promotion mutation)

**Date:** 2026-05-27
**Scenario:** A (Explicit) — BUILD_REQUEST is a 1707-line frozen merged-requirements.md spec with section-by-section directives, named refs, frozen contract fields, and named eval fixtures.
**Depth Tier:** Deep
**Track Count:** 1 (single cohesive deliverable; all components serve one skill)
**Status:** Complete

---

## EXISTING_FILES

### Spec inputs (sources, read-only)

- `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` (1707 lines) — **canonical spec** (already incorporates spec-panel-review fixes via inline `<!-- spec-panel fix (…) -->` comments). Sections §1–§19 enumerate every protocol decision, ref, eval fixture, return-contract field, and deferred item.
- `.dev/brainstorms/sc-reflect-rebuild/spec-panel-review.md` (872 lines) — 11-expert critique; most findings already merged into the spec. Treat as historical context, NOT a source of additional task items.
- `.dev/brainstorms/sc-reflect-rebuild/return-contract.yaml` — brainstorm output contract (provenance only).
- `.dev/brainstorms/sc-reflect-rebuild/seed-brief.md` (192 lines) — origin brief (provenance only).
- `.dev/brainstorms/sc-reflect-rebuild/enrichment/codebase-context.md` (1074 lines) — pre-brainstorm code survey (reference for §3.9 4-rejected-agents reasoning).
- `.dev/brainstorms/sc-reflect-rebuild/enrichment/research-deep.md` (~7400 words) — external research (reference for §1 thesis citations: Mehta 2026, Khan ICML 2024 Oral, Kenton NeurIPS 2024).
- `.dev/brainstorms/sc-reflect-rebuild/integration-analysis.md` — downstream-consumer field map (informs §9.3 Consumer Field Map).

### Surfaces to be CREATED (output targets)

- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — main skill body (anticipated ~1500-2000 lines after refs extraction; full spec content distilled per §16 refs split)
- `src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md` (§16 Wave 0)
- `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` (§16 Waves 1D, 3C — 5-dim calibration rubric)
- `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` (§16 Wave 1B/5 — 4-category taxonomy + detection signals + gold-standard refs + per-file aggregation rule for >100 hunks per §10)
- `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md` (§16 Wave 1B UC-1 — bipartite spec→tasklist matching + S_dev_density formula)
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` (§16 Wave 3A — model+persona rotation rules including executor-class exclusion, reviewer card template)
- `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md` (§16 Wave 5 — REPORT.md skeleton + Grounded/[INFERRED] tagging + mandatory `## Per-Task Verdicts` section when N≥2)
- `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (§16 Wave 6 — task-builder BUILD_REQUEST template, opt-in prompt)
- `src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md` (§16 build-time — Makefile targets, CI cadence, vendor-heterogeneity WARN body, PreToolUse hook redirect body)
- `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` (§16 eval-time — Python sketch for `citation_resolves` + 6 semantic grader types + new `path_exists`/`path_does_not_exist` per §14.5.7)
- `src/superclaude/skills/sc-reflect-protocol/refs/promotion-adapters.md` (§16 Wave 7 — task + sprint-release adapter table, collision-rule mechanics, `mv` template, rollback template)
- `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` (§16 pre-invocation — machine-readable mirror of §15 cost profile for caller pre-flight)
- `src/superclaude/commands/reflect.md` — REWRITE (currently 111 lines, legacy `think_about_*` surface). New shape: command frontmatter + body delegating to `Skill sc-reflect-protocol`. **Frozen baseline** of current file MUST be saved first per §13.2.
- `.dev/eval-workspaces/sc-reflect/` (workspace per CLAUDE.md plugin override):
  - `SPEC.md` (full design rationale + acceptance criteria + iteration history, per §18)
  - `evals/evals.json` — 3 pilot fixtures (§12.3 iteration-1)
  - `iterations/iteration-1/` (skeleton)
  - `grader.py` (copy from sc-brainstorm + extend per refs/grader-extensions.md)
  - `aggregate_iteration.py` (copy from sc-brainstorm baseline)
  - `skill-snapshot/reflect-v1.md` — frozen copy of `src/superclaude/commands/reflect.md` BEFORE rewrite (per §13.2 phase 1)
  - `cases/falsifier-suite/README.md` (per §12.5)
  - `cases/falsifier-suite/T2-converges-on-wrong.yaml` (SKELETON, `status: skeleton-pending-iteration-3-fixture`)
  - `cases/falsifier-suite/T2-judge-class-collision.yaml` (SKELETON)
  - `cases/falsifier-suite/fixtures/spec-with-deliberate-misclassification.md` (placeholder)
- 3 pilot eval fixtures under `.dev/eval-workspaces/sc-reflect/cases/` per §12.3:
  - `pre-trivial-coverage-gap/` (UC-1; tasklist missing 2/8 spec reqs; T1 expected)
  - `post-small-diff-clean/` (UC-2; 3-file diff clean; T1 expected)
  - `post-large-diff-mixed/` (UC-2; 15-file diff with 1 Regression + 2 Drift + 1 Necessary + 1 Authorized; T2 expected)
- 14 promotion-eval fixtures under `.dev/eval-workspaces/sc-reflect/evals/promotion/` per §14.5.7 (promotion-task-strict-pass, promotion-blocked-by-drift, promotion-blocked-by-frontmatter-missing, promotion-blocked-by-frontmatter-mismatch, promotion-blocked-by-grounding-gaps-empty-list, promotion-blocked-by-null-convergence, promotion-citation-revalidation-after-remediation, promotion-sprint-release-pass, promotion-collision-non-identical, promotion-collision-identical, promotion-no-promote-flag, promotion-promote-anyway-on-partial, promotion-dry-run, promotion-cross-fs-crash-recovery, promotion-log-pre-write-survives-crash)
- `Makefile` — add targets `reflect-eval`, `reflect-eval-quick`, `sync-cost-profile`, `lint-architecture` (per §17.5)

### Surfaces to be READ but NOT modified (dependencies — already exist)

- `src/superclaude/agents/confidence-calibrator.md` (118 lines) — reused by Wave 1D/3C; existing 5-dim rubric already shipped under sc-troubleshoot's `refs/escalation-rubric.md` (NB: reflect needs its OWN `refs/reflection-rubric.md` with 5 dims tailored to reflection per §5.2 vs troubleshoot's escalation rubric — confirmed read; the dims are NAMED differently).
- `src/superclaude/agents/evidence-validator.md` (128 lines) — reused by Wave 5 evidence gate; existing contract supports `file:line` re-Read + drop-not-confirm policy; v1 toolset Read/Grep/Glob only (no Bash) — confirmed adequate for reflect's needs.
- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` — Wave 4 delegation target via `Skill sc-adversarial-protocol with --compare ...`. Confirmed installed.
- `src/superclaude/skills/task-builder/SKILL.md` — Wave 6 (T3) delegation target. Confirmed installed.
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — reverse-direction caller (its Wave 6 Phase B/D auto-invokes reflect). Read for invocation-shape conventions; reflect's contract must satisfy what troubleshoot consumes.
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` — structural template/baseline for protocol skill layout (refs/, return-contract, fallback paths, Wave 0 prereq probe).
- `src/superclaude/skills/sc-task-protocol/SKILL.md` — reverse-direction caller (end-of-task hook).
- `src/superclaude/agents/root-cause-analyst.md` — Wave 1C agent (UC-2).
- `src/superclaude/agents/self-review.md` — Wave 1C agent (UC-2 low-stakes, S_scope ≤ 3 AND --depth quick).
- `src/superclaude/agents/requirements-analyst.md` — Wave 1B agent (UC-1).
- `src/superclaude/agents/audit-validator.md` — Wave 5 agent (when ≥20 findings, 10% spot-check).
- `src/superclaude/agents/socratic-mentor.md` — Wave 1C agent (UC-1 deep, optional).
- `src/superclaude/agents/rf-qa.md` — Wave 3B (UC-2 structural).
- `src/superclaude/agents/rf-qa-qualitative.md` — Wave 3B (UC-2 documents).
- `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` — authoritative MDTM template 02 (NOT in `.claude/templates/`; `src/superclaude/templates/workflow/` is canonical surface).
- `Makefile` — existing targets `dev`, `test`, `lint`, `format`, `sync-dev`, `verify-sync`, `verify`, `doctor`, `build-plugin`, `sync-plugin-repo`, `mcp` — must extend without breaking.
- `pyproject.toml` — existing entry points (CLI `superclaude`, pytest plugin `superclaude`) — no schema changes needed.
- `CLAUDE.md` (project) — defines source-of-truth = `src/superclaude/`; `.claude/` is sync-dev output; PR target = fork; never commit `.claude/{skills,commands,agents,hooks,templates}/*`; eval-workspace plugin override forces `.dev/eval-workspaces/<skill-name>/`.
- `.claude/settings.json` — PreToolUse hook rejects `.claude/skills/*-workspace/**` writes (per §17.5).
- `.gitignore` — matches `.claude/skills/*-workspace/` (per CLAUDE.md).
- `.dev/eval-workspaces/sc-brainstorm/` — structural baseline to copy from (SPEC.md, evals/, iterations/, grader.py, aggregate_iteration.py per §13.1).
- `.dev/eval-workspaces/sc-troubleshoot/` — structural baseline.

### Resources that DO NOT yet exist (must verify NOT created — STOP signals)

- `src/superclaude/skills/sc-reflect-protocol/` — confirmed NOT present (only `src/superclaude/skills/sc-troubleshoot-protocol/` exists as nearest sibling).
- `.dev/eval-workspaces/sc-reflect/` — confirmed NOT present.
- `.dev/reflect/` (global runs.jsonl directory per §15.1) — does NOT yet exist; gitignored when created.

## PATTERNS_AND_CONVENTIONS

(To be filled by researchers — high-level pointers from quick scan:)

- **Skill directory convention** (per `src/superclaude/skills/sc-troubleshoot-protocol/`): `SKILL.md` at root, `refs/<topic>.md` siblings, no `agents/` (delegates by name from sibling `src/superclaude/agents/`).
- **SKILL.md frontmatter convention** (per sc-troubleshoot, sc-brainstorm): `name`, `description` (multi-sentence rationale for skill triggering), `version`, `allowed-tools` (explicit list including MCP tool names like `mcp__serena__find_symbol`). NB: per §6.4 R3 C-007 consensus, the `think_about_*` Serena tools are deliberately NOT listed in frontmatter `allowed-tools` for reflect.
- **Command-side frontmatter convention** (per `src/superclaude/commands/`): `name`, `description`, `category`, `complexity`, `mcp-servers`, `personas`. Command body is short — just delegates to skill via `Skill <name>` invocation pattern.
- **Refs naming**: lowercase-kebab-case `.md` files under `refs/`, named by load-context (input-resolution, reflection-rubric, etc.) — never by section number.
- **Return contract emission**: written to `<output>/return-contract.yaml` AND returned inline; two-block (stable + telemetry) per §9.1.
- **Audit log shape**: per-step rows `{wave, step, timestamp, outcome, evidence_ref}` (§4) appended to `<output>/audit.log` (one line per step).
- **Fail-open MCP policy**: each MCP call falls back to Grep/Glob with `degraded: [<mcp-name>]` in audit (per §6.5 sc-validate-roadmap convention).
- **Output dir convention**: `<output>` defaults to `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`; under `.dev/` never `.claude/skills/`.
- **Spawn convention**: cross-skill via `Skill <name>` (never `/sc:<command>`); intra-skill via `Task` tool with explicit input paths (per agent definitions).
- **Sync model**: edit `src/superclaude/` → run `make sync-dev` → `make verify-sync` exits 0 → stage ONLY `src/` and `.dev/` paths. NEVER stage `.claude/`.

## GAPS_AND_QUESTIONS

(Items the parallel researchers must investigate or verify; specific to this build.)

- **G1.** Exact line counts and structural layout of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` and `sc-brainstorm-protocol/SKILL.md` to confirm size band reflect targets (the §13.2 comment "keeping SKILL.md within the sc-troubleshoot/sc-brainstorm band" suggests sc-troubleshoot/sc-brainstorm SKILL.md is the structural baseline, but actual line counts must be confirmed).
- **G2.** Existing `refs/` file naming conventions in sc-troubleshoot-protocol (per §16's ref table for reflect) — copy file-naming conventions verbatim.
- **G3.** `sc-adversarial-protocol` invocation surface — exact flag names (`--compare`, `--depth`, `--focus`, `--output`) must match what's currently shipped, otherwise reflect's Wave 4 invocation fails.
- **G4.** `task-builder` skill BUILD_REQUEST shape — exact field names reflect's Wave 6 BUILD_REQUEST template must follow (per `refs/remediation-handoff.md`).
- **G5.** `sc-troubleshoot-protocol` Wave 6 Phase B/D invocation shape — exact flag names troubleshoot uses when calling reflect (the reverse-direction integration test). Per Sam Newman §2.7 spec-panel finding, the integration is fragile if flag names diverge.
- **G6.** sprint executor.py (`src/superclaude/cli/`) — exact location and TurnLedger surface that consumes `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`, `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade` per §9.3.
- **G7.** Existing `.dev/eval-workspaces/sc-brainstorm/` structure (SPEC.md, evals/, iterations/, grader.py, aggregate_iteration.py) — full file-by-file inventory so the reflect eval workspace mirrors it exactly per §13.2.
- **G8.** Confirm `confidence-calibrator.md` and `evidence-validator.md` are NOT modified by this task (they ship as-is; reflect uses them via `Task`). Confirmed in EXISTING_FILES.
- **G9.** Verify `.dev/tasks/{to-do,done}/` and `.dev/releases/{current,complete}/` directory structures exist as the promotion adapters expect (§14.5.1). `.dev/tasks/to-do/` confirmed exists; `.dev/tasks/done/` should exist; `.dev/releases/current/` and `.dev/releases/complete/` need verification.
- **G10.** Existing Makefile targets — confirm `make sync-dev`, `make verify-sync`, `make lint`, `make test` are all present so the new `make reflect-eval`/`make reflect-eval-quick`/`make sync-cost-profile`/`make lint-architecture` targets don't collide.
- **G11.** Pre-commit hook — confirm it runs `make verify-sync` (per §17.5) so reflect's sync workflow doesn't break it.
- **G12.** `.claude/settings.json` PreToolUse hook redirect message body — exact byte content of the redirect message that the hook emits, since `refs/ops-integration.md` is supposed to contain its body verbatim.
- **G13.** Existing analogous task-folder examples for skill rebuilds — `.dev/tasks/to-do/TASK-RF-20260525-150000/` (sc-brainstorm-rebuild?) is the most analogous prior work; structural patterns from its task file should inform this build.
- **G14.** Whether sc-brainstorm-protocol exposes a similar 4-rejected-agents Kill List structure that reflect's §17.7 can mirror.
- **G15.** Does the project have an existing `make lint-architecture` target, or is this NEW (per §17.5)? If new, its definition must be specified.
- **G16.** What is the existing pattern for SKILL.md sections that need MCP tool docs vs refs separation — confirm that listing all MCP tools in frontmatter `allowed-tools` is the established pattern, AND confirm the §6.4 exclusion of `think_about_*` from frontmatter is unique to reflect (vs sc-troubleshoot which may include them).

## RECOMMENDED_OUTPUTS

Research files to create under `${TASK_DIR}research/` — one per topic, named with NN- prefix:

| # | Topic | File |
|---|-------|------|
| 01 | File Inventory — surfaces to create + dependencies to read | `01-file-inventory.md` |
| 02 | Patterns & Conventions — protocol-skill structural baseline | `02-patterns-and-conventions.md` |
| 03 | Integration Points — cross-skill invocation shapes (sc-adversarial, task-builder, sc-troubleshoot, sprint, sc-task) | `03-integration-points.md` |
| 04 | Doc Cross-Validator — verify spec claims against actual code state | `04-doc-cross-validator.md` |
| 05 | Template & Examples — MDTM template 02 + analogous task-folder examples | `05-template-and-examples.md` |
| 06 | Spec Decomposition — map every §1-§19 section to a concrete file-creation/edit unit | `06-spec-decomposition.md` |
| 07 | Test & Verification — eval-workspace baseline (sc-brainstorm), grader.py patterns, Makefile target shapes | `07-test-and-verification.md` |
| 08 | Data Flow Tracer — Wave-by-Wave data flow including agent inputs/outputs and consumer field map | `08-data-flow-tracer.md` |

## SUGGESTED_PHASES

Per-researcher assignment (all 8 spawned in parallel per A.7):

- **Researcher 01 (File Inventory)** — Scope: existing `src/superclaude/{skills,commands,agents,templates}/`, existing `.dev/{tasks,releases,eval-workspaces,reflect,brainstorms}/`. Output: `01-file-inventory.md`. Goal: enumerate every file that must be CREATED, MODIFIED, or READ (with line counts where relevant); confirm presence/absence of dependency files. Other researchers cover: 02 (patterns from those files), 04 (verification of claims about those files).
- **Researcher 02 (Patterns & Conventions)** — Scope: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` + `refs/`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` + `refs/`; `src/superclaude/commands/troubleshoot.md`; `src/superclaude/commands/brainstorm.md`. Output: `02-patterns-and-conventions.md`. Goal: extract structural conventions (frontmatter shape, refs/ naming, Wave structure framing, fail-open patterns, return-contract layout, fallback path naming) that reflect must mirror. Other researchers cover: 01 (inventory), 03 (integration shapes).
- **Researcher 03 (Integration Points)** — Scope: `sc-adversarial-protocol/SKILL.md` (Wave 4 caller surface — `--compare`/`--depth`/`--focus`/`--output`), `task-builder/SKILL.md` (Wave 6 BUILD_REQUEST shape), `sc-troubleshoot-protocol/SKILL.md` (reverse caller flags), `sc-task-protocol/SKILL.md` (reverse caller), `src/superclaude/cli/` (sprint executor.py TurnLedger surface). Output: `03-integration-points.md`. Goal: produce exact invocation strings reflect must emit/accept. Other researchers cover: 02 (style), 06 (spec ↔ integration mapping).
- **Researcher 04 (Doc Cross-Validator)** — Scope: spec claims about file paths, agent contracts, MCP tools, Makefile targets, hook semantics. Output: `04-doc-cross-validator.md`. Goal: for every CODE-referenced claim in merged-requirements.md, verify with Read/Grep/Glob; tag [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED]. Other researchers cover: this is the staleness gate that protects all others' work.
- **Researcher 05 (Template & Examples)** — Scope: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 fully — A3 granular, B2 self-contained, L1-L6 handoff if present); analogous task folders: `.dev/tasks/to-do/TASK-RF-20260525-150000/`, `.dev/tasks/to-do/TASK-RF-20260522-151622/`, `.dev/tasks/to-do/TASK-RF-20260521133223/`. Output: `05-template-and-examples.md`. Goal: extract template rules + analogous-task-folder structural patterns. Other researchers cover: 01 (file presence), 02 (skill structure).
- **Researcher 06 (Spec Decomposition)** — Scope: `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` (the canonical spec) sections §1-§19. Output: `06-spec-decomposition.md`. Goal: map every section/sub-section to a CONCRETE build unit (e.g., "§5.3 rubric → SKILL.md §5.3 paragraph + refs/reflection-rubric.md `## 5.3 Decision logic` subsection"); identify every distinct file-creation/edit/append item that needs its own MDTM checklist row. **MOST GRANULAR researcher** — output should be the spine of the per-file checklist items. Other researchers cover: 01 (inventory provides file paths; 06 provides what content goes where).
- **Researcher 07 (Test & Verification)** — Scope: `.dev/eval-workspaces/sc-brainstorm/` (full file-by-file inventory + grader.py reading); `.dev/eval-workspaces/sc-troubleshoot/`; `Makefile` (target shapes for existing `test`, `lint`, `sync-dev`, `verify-sync`, `dev`, `verify`); `pyproject.toml` (entry-point conventions); pre-commit hook config (if exists). Output: `07-test-and-verification.md`. Goal: produce the verification pattern for every build item (lint command, sync command, eval command, fixture-format). Other researchers cover: 04 (verifies these paths exist), 06 (decomposition uses verification commands).
- **Researcher 08 (Data Flow Tracer)** — Scope: Wave 0→Wave 7 data flow per merged-requirements.md §4. For every wave: input artifacts, agent invocations (with `Task`-tool argument shapes from agent definitions), output artifacts, consumer-side data shape. Output: `08-data-flow-tracer.md`. Goal: produce wave-by-wave I/O graph that informs SKILL.md's prose accuracy. Cross-reference: §9.3 Consumer Field Map, §17.6 Testability Map.

## TEMPLATE_NOTES

- **MDTM template selection: 02 (Complex Task)** — non-negotiable. The build involves discovery (research is already done; but SKILL.md drafting still requires iterative section-by-section composition), parallel subagent spawning (per §13.2 phase 2 skill-creator run_loop.py), multiple phases with different activities (frozen baseline snapshot → skill body → refs → command rewrite → eval workspace → sync → verify), conditional flows (eval iteration convergence at <5% improvement per §12.3), quality gates (make verify-sync, make reflect-eval-quick, pre-commit hook).
- **Tier selection: Deep** — non-negotiable. Spec is 1707 lines; 13 surface files to create plus eval workspace plus 14 promotion eval fixtures plus 3 pilot eval fixtures plus skill snapshot plus integration with 5 downstream consumers. Multi-subsystem (skills + commands + agents + eval-workspace + Makefile + CI). The 6-8 researcher fan-out is required, not optional.
- **MDTM features the generated task file should use:**
  - **Per-file checklist items** (A3 granular breakdown): each ref file, each eval fixture, each Makefile target, the skill body, the command, the frozen baseline copy — every artifact gets its own item.
  - **Phase ordering rule (A4 iterative):** Phase 1 (preparation: read spec + frozen-baseline snapshot + workspace creation), Phase 2 (skill body authoring), Phase 3 (refs authoring — one item per ref), Phase 4 (command rewrite), Phase 5 (eval workspace setup), Phase 6 (sync to .claude/), Phase 7 (quality gates: lint, verify-sync, reflect-eval-quick, eval-iteration-1), Phase 8 (completion: status flip, commit prep).
  - **L1-L6 subagent handoff pattern (template 02 specific):** parallel sub-spawn opportunities flagged where research-runtime allows (e.g., refs authoring can be parallelized per ref file in a future task-execution pass — but the current build doesn't need to enforce that since the work is sequential authoring).
  - **B2 self-contained items:** each checklist row has Context (what executor needs to know), Action (exact command/edit), Output (what gets created), Verification (how to confirm), Completion gate (when it's done). Verification commands MUST include `make verify-sync` and per-target eval-runner commands.
- **QA gate posture (BUILD_REQUEST.QA_GATE_REQUIREMENTS):** PER_PHASE — verification items after every phase (Phase 2 verify SKILL.md frontmatter parses + lint; Phase 3 verify each ref file Read-back; Phase 4 verify command file lint + bidirectional command↔skill link; Phase 5 verify eval-workspace path is under `.dev/eval-workspaces/sc-reflect/` not `.claude/skills/`; Phase 6 verify `make verify-sync` exits 0; Phase 7 verify `make reflect-eval-quick` passes 3 pilot evals; Phase 8 verify all 14 promotion-eval fixtures wired into evals/promotion/). Plus a final QA gate before status flip.
- **Validation posture (BUILD_REQUEST.VALIDATION_REQUIREMENTS):** `make lint && make verify-sync && make lint-architecture && make reflect-eval-quick` MUST pass before completion. Plus the §17.5 "stage ONLY src/ and .dev/" check before any git operation.
- **Testing posture (BUILD_REQUEST.TESTING_REQUIREMENTS):** mostly authoring (no Python test code to write), but **eval fixtures ARE tests** for this skill — they get their own items per §12.3 + §14.5.7. Use the eval-runner via `make reflect-eval-quick` (or equivalent) as the verification command for each fixture.
- **Execution Context block (BUILD_REQUEST.EXECUTION_CONTEXT_REQUIREMENTS):** AUTO. Source areas inferable from research (≥3): `sc-reflect-protocol skill body`, `sc-reflect refs files`, `reflect command surface`, `sc-reflect eval workspace`, `MDTM-template-driven authoring`, `sc-adversarial / task-builder / sc-troubleshoot integration shapes`. AUTO heuristic will emit the 3-bullet block.

## AMBIGUITIES_FOR_USER

Genuine open questions about user intent that cannot be inferred from the codebase or the merged-requirements.md spec — surface to the user via Open Questions in the generated task file. The user reviews them before `/task` execution.

- **U1. v1.0 ship-scope boundary (Janet Gregory §2.10 spec-panel finding, still open in spec):** does this task ship the FULL v1.0 (SKILL.md + all 11 refs + command + eval workspace + frozen baseline + Makefile targets + 3 pilot evals + 14 promotion eval fixtures + falsifier suite skeleton), or does it ship just the **draft v1 phase** per §13.2 (SKILL.md + refs + command + eval workspace skeleton; iteration-1 evals + iteration-2 expansion handled separately)? Default assumption for the task file: ship full v1.0 SKILL.md + refs + command + eval-workspace SKELETON + falsifier-suite SKELETON + 3 pilot-eval STUBS + 14 promotion-eval STUBS, but DEFER the actual eval-runner execution (`make reflect-eval`) and iteration-2 expansion to a follow-up task. The task file marks iteration-1 fixture authoring as a follow-up.
- **U2. Sync-dev autopilot vs manual:** per CLAUDE.md, source-of-truth is `src/superclaude/`; `.claude/` is sync-dev output. Should the task file include a `make sync-dev` checklist item AFTER every `src/` edit, or batch them at end-of-phase? Default: batch at Phase 6 (single sync after all src/ authoring complete) + pre-commit hook auto-runs `make verify-sync`.
- **U3. Frozen baseline location:** §13.2 phase 1 says `skill-snapshot/reflect-v1.md` under `.dev/eval-workspaces/sc-reflect/`. Default assumption: copy `src/superclaude/commands/reflect.md` (the legacy 111-line file) verbatim to `.dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md` BEFORE rewriting `src/superclaude/commands/reflect.md`. The frozen snapshot is git-tracked under `.dev/` per CLAUDE.md.
- **U4. PR / branch posture:** current branch is `feat-reflect-v2` (per session-context). This task assumes commits land on `feat-reflect-v2`; the user opens the PR (`gh pr create --repo IronbellyOrg/IronClaude --base master --head feat-reflect-v2 ...`) at the end. The task file does NOT auto-commit or auto-PR.
- **U5. Frontmatter `allowed-tools` enumeration for SKILL.md:** spec §6.4 says `think_about_*` Serena tools are deliberately NOT in `allowed-tools`. The full allowed-tools list must enumerate every other tool reflect uses (Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, MCP tools). The task file should list every tool from `merged-requirements.md` line 5 (existing frontmatter draft already enumerates these — verify reflect researchers don't drift from this list).
- **U6. v1.1 deferred items posture in task file:** the §19 deferred items (vendor heterogeneity tightening, sufficiency claim hardening, auto-rollback, streaming verdicts, cross-tasklist memory) are explicitly OUT OF SCOPE for v1.0. The task file mentions them only in the "Follow-Up Items" Task Log section, not as checklist items.
- **U7. Does iteration-1 eval RUN as part of this task, or only the eval-workspace SETUP?** Default: SETUP only (per U1). Iteration-1 RUN (`make reflect-eval-quick`) is a verification item to confirm the workspace structure works, but actual iteration-2 expansion and iteration-3 falsifier hardening are follow-up tasks.
