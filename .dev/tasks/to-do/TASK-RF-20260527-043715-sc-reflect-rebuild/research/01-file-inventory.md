# Research: File Inventory
**Topic type:** File Inventory
**Scope:** sc-reflect-protocol rebuild — CREATE/MODIFY/READ surfaces across src/, .dev/, Makefile
**Status:** Complete
**Date:** 2026-05-27
---

## Method

Every file path below is **CODE-VERIFIED via Bash(`ls`/`wc -l`)** unless explicitly tagged Unverified. Spec citations point to `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` (1706 lines, frozen).

Three buckets:

- **CREATE** — file does not exist on disk; must be authored fresh.
- **MODIFY** — file exists; must be rewritten or extended.
- **READ-ONLY DEP** — file exists and is consumed unchanged.

---

## Bucket A — CREATE (Skill Package)

Directory `src/superclaude/skills/sc-reflect-protocol/` does **NOT YET EXIST** (verified via `ls -d src/superclaude/skills/sc-reflect-protocol → No such file or directory`). Every path below must be created.

### A.1 Skill root

| # | Path | Anticipated lines | Spec source | Purpose |
|---|------|-------------------|-------------|---------|
| A1 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | 800-1400 | spec §1-§17, frontmatter line 1-21 | Behavioral protocol body. Frontmatter has 6 fields: `name: sc:reflect-protocol`, `description: ...` (long blurb on line 3 of spec), `version: 1.0.0`, `allowed-tools: ...` (literal list in spec line 5), Extended-metadata HTML comment block (lines 14-21). Body covers §1 Purpose, §2 Triggers, §3 Inputs, §4 Wave 0-7 architecture, §5 Tier-Decision Rubric, §6 Serena usage, §7 Agent Delegation Map, §8 Cross-Skill Integration, §9 Output Contract, §10 Deviation Taxonomy, §11 Hallucination Guardrails, §14 Error Handling Matrix, §14.5 Wave 7 Promotion Mutation, §15 Token Cost Profile, §17 Boundaries (Will / Will Not), §17.5 Ops Integration (~30 lines inline; rest in refs/ops-integration.md), §17.6 Testability Map, §17.7 Kill List, §18 Spec Reference, §19 v1.1 Deferred. Compare to neighbors: sc-troubleshoot-protocol/SKILL.md = 456 lines; sc-brainstorm-protocol/SKILL.md = 421 lines; sc-adversarial-protocol/SKILL.md = 3002 lines (outlier). |
| A2 | `src/superclaude/skills/sc-reflect-protocol/__init__.py` | 0 | (convention) | Empty marker matching `src/superclaude/skills/sc-adversarial-protocol/__init__.py` (zero bytes). Required for Python package discovery in `install_skills.py`. |

### A.2 refs/ (load-on-demand per wave; spec §16 enumerates exactly 11 refs)

Mirrors the existing pattern in `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (6 files) and `src/superclaude/skills/sc-adversarial-protocol/refs/` (4 files).

| # | Path | Anticipated lines | Spec §16 row | Wave consumer | Purpose |
|---|------|-------------------|--------------|---------------|---------|
| A3 | `src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md` | 80-150 | row 1 | Wave 0 | Mode auto-detection (6-rule first-match per §3.2), STOP conditions, slug generation. |
| A4 | `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` | 120-200 | row 2 | Wave 1D, 3C | 5-dimension calibration rubric (Citation grounding, Coverage completeness, Deviation-classification clarity, Risk surface coverage, Recommendation actionability). |
| A5 | `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | 150-250 | row 3 | Wave 1B (UC-2), Wave 5 | 4-category taxonomy (Authorized expansion / Necessary deviation / Drift / Regression) with detection signals, gold-standard refs, default remediations (per §10). |
| A6 | `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md` | 100-180 | row 4 | Wave 1B (UC-1) | Spec-to-tasklist coverage map algorithm; bipartite matching heuristics; `S_dev_density` calculation. |
| A7 | `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | 100-180 | row 5 | Wave 3A | Model + persona rotation rules; reviewer card template (per §7.1 reviewer composition rules). |
| A8 | `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md` | 150-300 | row 6 | Wave 5 | Final REPORT.md skeleton with Grounded vs `[INFERRED]` tagging. P4-MANDATORY `## Per-Task Verdicts` section when `per_task_verdicts.length ≥ 2`. |
| A9 | `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` | 80-150 | row 7 | Wave 6 | task-builder BUILD_REQUEST template; opt-in prompt. Note: a same-name ref exists at `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` — use as structural model, do NOT copy verbatim. |
| A10 | `src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md` | 200-350 | row 8 | build-time | Detailed Makefile target tables, full CI cadence, PreToolUse hook redirect message body, vendor-heterogeneity WARN body (per §4 Wave 0 step 0.6). |
| A11 | `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` | 150-300 | row 9 | eval-time | Python implementation sketch for `citation_resolves` with fixture-root remapping + 6 grader DSL semantic types + new `path_exists` / `path_does_not_exist` assertion types (per §14.5.7 §12.4). |
| A12 | `src/superclaude/skills/sc-reflect-protocol/refs/promotion-adapters.md` | 150-250 | row 10 | Wave 7 | Full adapter table (`task`, `sprint-release`, operator-added); collision-rule mechanics; `mv` invocation template; rollback command template (per §14.5). |
| A13 | `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` | 60-120 (YAML) | row 11 | pre-invocation (callers only) | **P7**: Static, machine-readable mirror of the §15 Token Cost Profile table. Callers (sprint TurnLedger, CI) read this BEFORE invoking reflect. Updated in lockstep with §15 via `make sync-cost-profile`. |

**Total refs/ count:** 11 files (10 .md + 1 .yaml), matching §16 row count exactly.

---

## Bucket B — CREATE (Command + per-machine append-only)

### B.1 `.dev/reflect/` runtime artifact directory

Path `.dev/reflect/` does **NOT EXIST** (verified). Per §15.1, reflect emits `<output>/metrics.json` per run AND appends a one-line summary to a global `.dev/reflect/runs.jsonl` for cross-run aggregation.

| # | Path | Anticipated lines | Spec source | Purpose |
|---|------|-------------------|-------------|---------|
| B1 | `.dev/reflect/runs.jsonl` | 0 (seed) | §15.1 + §9.3 meta-eval consumer row | Per-machine append-only run summary; one JSON-line per reflect invocation. Seeded empty by Wave 0 if missing. |
| B2 | `.dev/reflect/.gitignore` | 1-3 | (implied — per-machine append-only) | Ignore the whole dir contents (`*` + `!.gitignore`) so per-machine runs.jsonl does not pollute git. |

---

## Bucket C — CREATE (Eval Workspace — `.dev/eval-workspaces/sc-reflect/`)

Path `.dev/eval-workspaces/sc-reflect/` does **NOT EXIST** (verified). Per spec §12 + §13.2 + §14.5.7, the workspace mirrors `.dev/eval-workspaces/sc-brainstorm/` structurally.

### C.1 Workspace root (mirrors sc-brainstorm)

| # | Path | Anticipated lines | Spec source | Purpose |
|---|------|-------------------|-------------|---------|
| C1 | `.dev/eval-workspaces/sc-reflect/SPEC.md` | 600-1700 | §18 ("Full spec at .dev/eval-workspaces/sc-reflect/SPEC.md") | Design rationale + acceptance criteria + iteration history. **Option:** start as a copy of `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` (1706 lines), or generate a fresh design-rationale doc. Compare baselines: sc-brainstorm SPEC.md = 684 lines; sc-troubleshoot agent-design.md = ~42k bytes. |
| C2 | `.dev/eval-workspaces/sc-reflect/grader.py` | 350-600 | §12.4 + §13.2 ("copy from sc-brainstorm; extend per refs/grader-extensions.md") | Deterministic assertion grader. Copy `.dev/eval-workspaces/sc-brainstorm/grader.py` (279 lines) and extend with 6 semantic types (`citation_resolves`, `regex_present`, `regex_absent`, `yaml_list_contains`, `matrix_covers_items`, `checkpoint_logged`, `deviation_class_matches`) + 2 new assertion types per §14.5.7 (`path_exists`, `path_does_not_exist`) + `falsifier_skeleton_present` assertion per §12.5. |
| C3 | `.dev/eval-workspaces/sc-reflect/aggregate_iteration.py` | 150-250 | §13.2 sequenced build row 4 | Copy from `.dev/eval-workspaces/sc-brainstorm/aggregate_iteration.py` (163 lines). Per-iteration aggregator producing `grading.json` + benchmark deltas. |
| C4 | `.dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md` | ~111 | §12 line 945 ("frozen baseline = current src/superclaude/commands/reflect.md") | **Frozen snapshot** of the current legacy `src/superclaude/commands/reflect.md` (111 lines, verified). Baseline for iteration-1 comparisons. Compare to `.dev/eval-workspaces/sc-brainstorm/skill-snapshot/brainstorm-v1.md` = 206 lines. |

### C.2 evals/ (eval suite JSON + iteration runs)

| # | Path | Anticipated lines | Spec source | Purpose |
|---|------|-------------------|-------------|---------|
| C5 | `.dev/eval-workspaces/sc-reflect/evals/evals.json` | 150-400 | §12.3 + §14.5.7 | Eval suite manifest. v1.0 ships 3 pilot evals per §12.3 (`pre-trivial-coverage-gap`, `post-small-diff-clean`, `post-large-diff-mixed`) PLUS 14 promotion fixtures per §14.5.7 (`promotion-task-strict-pass`, `promotion-blocked-by-drift`, `promotion-blocked-by-frontmatter-missing`, `promotion-blocked-by-frontmatter-mismatch`, `promotion-blocked-by-grounding-gaps-empty-list`, `promotion-blocked-by-null-convergence`, `promotion-citation-revalidation-after-remediation`, `promotion-sprint-release-pass`, `promotion-collision-non-identical`, `promotion-collision-identical`, `promotion-no-promote-flag`, `promotion-promote-anyway-on-partial`, `promotion-dry-run`, `promotion-cross-fs-crash-recovery`, `promotion-log-pre-write-survives-crash`). Iteration-2 expands to 9-12 pilot evals. Compare: `.dev/eval-workspaces/sc-brainstorm/evals/evals.json` = 160 lines. |

### C.3 cases/falsifier-suite/ (v1.0 pre-seeded skeleton per §12.5)

| # | Path | Anticipated lines | Spec source | Purpose |
|---|------|-------------------|-------------|---------|
| C6 | `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/README.md` | 30-80 | §12.5 line 1009 | Describes the sufficiency-claim contract; explains the skeleton-pending → active promotion path. |
| C7 | `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-converges-on-wrong.yaml` | 40-80 | §12.5 lines 1018-1059 | **Skeleton with `status: skeleton-pending-iteration-3-fixture`** in v1.0 (per W-A8 spec-panel fix). Fixture content populated in iteration-3. Grader emits `skeleton_present: true` telemetry while skeleton-pending. |
| C8 | `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-judge-class-collision.yaml` | 30-60 | §12.5 line 1011 | **Skeleton** for the Khan ICML violation case (judge in reviewer pool). Skeleton-pending until iteration-3. |
| C9 | `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/fixtures/spec-with-deliberate-misclassification.md` | 30-100 | §12.5 line 1013 | Placeholder spec for v1; filled in iteration-3. |

### C.4 iterations/ scaffolding (filled by run_loop runs)

Empty directory stubs created at build time so iteration-1 runs land on existing paths. sc-brainstorm has `iterations/iteration-1/` and `iterations/iteration-2/`; sc-troubleshoot has up through `iteration-3/`. v1.0 ship target is iteration-2 per §12.3 convergence rule.

| # | Path | Anticipated lines | Spec source | Purpose |
|---|------|-------------------|-------------|---------|
| C10 | `.dev/eval-workspaces/sc-reflect/iterations/.gitkeep` | 0 | §13.2 row 2-5 | Reserve directory; iteration-N/ subdirs populated by skill-creator `run_loop.py` runs. |

---

## Bucket D — MODIFY

### D.1 `src/superclaude/commands/reflect.md`

| # | Path | Current lines | Target lines | Operation |
|---|------|---------------|--------------|-----------|
| D1 | `src/superclaude/commands/reflect.md` | **111** (verified) | 60-180 | **REWRITE.** Current file is legacy `think_about_*` surface (per spec line 20 supersedes). New version must dispatch `Skill sc:reflect-protocol` via `## Activation` section. Frontmatter must align with new skill identity. Spec §17.5 step 1 implies edits happen here. **Per CLAUDE.md ABSOLUTE RULE (lint-architecture Check 1/2/6/8/9):** command must have `## Activation` section pointing to skill `sc-reflect-protocol`; skill `sc-reflect-protocol` must have matching command `reflect.md`. Both must be present together for `make lint-architecture` to pass. **Snapshot pre-edit:** Capture verbatim copy as C4 (`.dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md`) BEFORE the rewrite (snapshot is the frozen baseline). |

### D.2 `Makefile`

| # | Path | Current lines | Target operation |
|---|------|---------------|------------------|
| D2 | `Makefile` | **528** (verified) | **ADD 3 new targets** per spec §17.5 line 1589 + §16 row 11. Existing targets verified: `lint-architecture` (line 362), `eval-skill` (line 482), `sync-dev` (line 109), `verify-sync` (line 166), `lint` (line 48), `test` (line 13). New targets to add: (1) **`reflect-eval`** — full eval (~2 min); runs all pilot + promotion + falsifier evals via `.dev/eval-workspaces/sc-reflect/grader.py`. (2) **`reflect-eval-quick`** — 3 pilot cases only, <30s; CI uses on every PR touching reflect skill/command. (3) **`sync-cost-profile`** — regenerates `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` from §15 table. Optionally include a check that fails CI if §15 and cost-profile.yaml drift. |

---

## Bucket E — READ-ONLY DEPENDENCIES (consumed unchanged)

### E.1 Agents (spec §7 Agent Delegation Map; "No new agents required" per §7.2)

All paths CODE-VERIFIED via `wc -l`. Spec line 492 explicitly states the skill creates ZERO new agents.

| # | Path | Lines | Purpose for reflect |
|---|------|-------|---------------------|
| E1 | `src/superclaude/agents/confidence-calibrator.md` | **118** | Wave 1D + Wave 3C: re-grade reviewer/reflection card confidence WITHOUT formation context (blind calibration per §11.3). Must be on disjoint model class from reviewers. |
| E2 | `src/superclaude/agents/evidence-validator.md` | **128** | Wave 5 final gate (non-negotiable per §11.2): re-Read every `file:line` citation; unfounded citations are *dropped, not downgraded*. |
| E3 | `src/superclaude/agents/root-cause-analyst.md` | **56** | Wave 1C: hypothesis card generation. Inline fallback if agent fails per §14 row. |
| E4 | `src/superclaude/agents/self-review.md` | **37** | Wave 3 reviewer slot candidate (single-agent self-review path). |
| E5 | `src/superclaude/agents/requirements-analyst.md` | **56** | UC-1 Wave 1: coverage-mapping (replaces rejected `coverage-mapper` per §17.7 row 1). |
| E6 | `src/superclaude/agents/audit-validator.md` | **145** | Wave 5: audit-log row validation. |
| E7 | `src/superclaude/agents/socratic-mentor.md` | **310** | Wave 6 user-decision flow when `needs_human_decision: true`. |
| E8 | `src/superclaude/agents/rf-qa.md` | **552** | Wave 3 reviewer slot — quantitative reviewer. Failure handling per §14 row. |
| E9 | `src/superclaude/agents/rf-qa-qualitative.md` | **1139** | Wave 3 reviewer slot — qualitative reviewer (largest agent in pool). |

### E.2 Skills (cross-skill integration per §8)

| # | Path | Lines | Purpose for reflect |
|---|------|-------|---------------------|
| E10 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | **3002** | Wave 4: Mode A debate + scoring + merge. Reflect delegates debate; never re-implements per §17 "Will". Failure rows F1/F2/F3 in §14. |
| E11 | `src/superclaude/skills/task-builder/SKILL.md` | **2190** | Wave 6 (Tier 3): corrective MDTM remediation. Opt-in per §17 "Will Not" (no auto-execute). |
| E12 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | **456** | Auto-trigger source per §2 (Wave 6 Phase B + Phase D). Reflect is *invoked by* sc-troubleshoot. |
| E13 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` | **421** | Structural baseline for reflect SKILL.md style; eval-workspace structural baseline (`.dev/eval-workspaces/sc-brainstorm/` is the canonical mirror per §12 line 945). |
| E14 | `src/superclaude/skills/sc-task-protocol/SKILL.md` | **396** | End-of-task hook trigger source per §2. |

### E.3 Eval workspace structural baselines (mirror, do not modify)

Per spec §12 line 945: "Modeled on `.dev/eval-workspaces/sc-brainstorm/`. Same layout."

| # | Path | Lines | Purpose |
|---|------|-------|---------|
| E15 | `.dev/eval-workspaces/sc-brainstorm/SPEC.md` | **684** | Structural baseline for C1. |
| E16 | `.dev/eval-workspaces/sc-brainstorm/grader.py` | **279** | Copy-source for C2. |
| E17 | `.dev/eval-workspaces/sc-brainstorm/aggregate_iteration.py` | **163** | Copy-source for C3. |
| E18 | `.dev/eval-workspaces/sc-brainstorm/skill-snapshot/brainstorm-v1.md` | **206** | Structural template for C4 (frozen baseline snapshot). |
| E19 | `.dev/eval-workspaces/sc-brainstorm/evals/evals.json` | **160** | Structural template for C5. |
| E20 | `.dev/eval-workspaces/sc-brainstorm/iterations/` | (dir) | Structural template for C10 — sc-brainstorm has `iteration-1/` + `iteration-2/`. |
| E21 | `.dev/eval-workspaces/sc-troubleshoot/` | (dir tree) | Secondary structural baseline (has iteration-3, meta-eval-test-is-wrong subdir, forensic-analysis subdir). |

### E.4 Promotion adapter target dirs (Wave 7 destinations)

All four paths CODE-VERIFIED to exist (no create needed).

| # | Path | Purpose for reflect |
|---|------|---------------------|
| E22 | `.dev/tasks/to-do/` | Source path glob for `task` adapter (§14.5.1). Exists. |
| E23 | `.dev/tasks/done/` | Destination for `task` adapter promotion (`mv .dev/tasks/to-do/TASK-* → .dev/tasks/done/TASK-*`). Exists. |
| E24 | `.dev/releases/current/` | Source path glob for `sprint-release` adapter. Exists. |
| E25 | `.dev/releases/complete/` | Destination for `sprint-release` adapter (`mv .dev/releases/current/<release>/ → .dev/releases/complete/<release>/`). Exists. |

### E.5 Templates

| # | Path | Lines | Purpose |
|---|------|-------|---------|
| E26 | `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` | **1204** | MDTM template the orchestrating task file (TASK-RF-20260527-043715-sc-reflect-rebuild) is built from. Not used by reflect itself, but is the template the task builder will instantiate. |

### E.6 CLI for TurnLedger interface discovery (P5 `--budget-remaining`)

| # | Path | Verified anchor | Purpose |
|---|------|-----------------|---------|
| E27 | `src/superclaude/cli/sprint/models.py` | `class TurnLedger:` at **line 693** | Source of the `TurnLedger` interface that callers (sprint executor) use. Per §3 / §4.0 step 0.9, callers pass `--budget-remaining <int>` derived from `TurnLedger.available()`. Reflect does not import this; sprint executor's invocation glue does. |
| E28 | `src/superclaude/cli/sprint/executor.py` | `from .models import ... TurnLedger ...` at **line 35** | Caller-side glue: how sprint passes `--budget-remaining` to reflect when reflect runs inside a sprint pipeline. Reflect needs the contract shape, not the code. |
| E29 | `src/superclaude/cli/sprint/kpi.py` | consumes `TurnLedger` at lines **23, 156, 192-197** | Reference for how `wiring_turns_used/credited` flow back into budget accounting. |

### E.7 Project constraints (consulted during build, not modified by build)

| # | Path | Lines | Purpose |
|---|------|-------|---------|
| E30 | `CLAUDE.md` (project) | **397** | ABSOLUTE RULES: never stage `.claude/`, PR target = fork, custom command skill invocation. Reflect skill must honor all three. |
| E31 | `.claude/settings.json` | **30** | PreToolUse hook that rejects writes to `.claude/skills/*-workspace/**` — must NOT be edited. Reflect's eval workspace MUST land at `.dev/eval-workspaces/sc-reflect/` to pass the hook (per §17.5 line 1579). |
| E32 | `.gitignore` | **226** | Matches `.claude/skills/*-workspace/` so any misplaced workspace cannot be committed. Confirms eval-workspace destination override. Also matches `.claude/` except `settings.json`. |
| E33 | `pyproject.toml` | **220** | Dependency manifest; reflect requires no new Python deps beyond what skills already use (PyYAML for grader-extensions, present). |

---

## Cross-reference: spec §16 Refs Table → CREATE rows

Spec §16 lists 11 refs (lines 1500-1512). All 11 are mapped 1:1 to CREATE rows A3-A13. No orphan refs. No missing refs.

| §16 row | CREATE row |
|---------|------------|
| `refs/input-resolution.md` | A3 |
| `refs/reflection-rubric.md` | A4 |
| `refs/deviation-taxonomy.md` | A5 |
| `refs/coverage-mapping.md` | A6 |
| `refs/reviewer-spec.md` | A7 |
| `refs/report-template.md` | A8 |
| `refs/remediation-handoff.md` | A9 |
| `refs/ops-integration.md` | A10 |
| `refs/grader-extensions.md` | A11 |
| `refs/promotion-adapters.md` | A12 |
| `refs/cost-profile.yaml` | A13 |

---

## Tally

- **CREATE: 25 files** = A1-A13 skill package (13) + B1-B2 runtime (2) + C1-C10 eval workspace (10).
- **MODIFY: 2 files** = D1 reflect.md REWRITE; D2 Makefile ADD 3 targets.
- **READ-ONLY DEPS: 33 paths** = E1-E33.

**Aggregate per-checklist-item granularity:** 27 actionable items (25 CREATE + 2 MODIFY). Each can be one MDTM checklist row.

---

## Summary

The sc-reflect-protocol rebuild requires authoring **a 13-file skill package** under `src/superclaude/skills/sc-reflect-protocol/` (SKILL.md + `__init__.py` + 11 refs per spec §16, ALL of which do not yet exist) plus **a 10-file eval workspace scaffold** under `.dev/eval-workspaces/sc-reflect/` (SPEC.md + grader.py + aggregate_iteration.py + frozen skill snapshot + evals.json + 4 falsifier-suite skeleton files + iterations/.gitkeep) plus **2 small runtime files** under `.dev/reflect/` (runs.jsonl seed + .gitignore). The build also REWRITES the existing 111-line legacy `src/superclaude/commands/reflect.md` into a thin dispatch command pointing at the new skill (snapshot first to C4 before overwrite) and ADDS 3 new Makefile targets (`reflect-eval`, `reflect-eval-quick`, `sync-cost-profile`) on top of the already-present `lint-architecture` (line 362) and `eval-skill` (line 482).

Zero new agents are required — all 9 dependency agents (confidence-calibrator 118L, evidence-validator 128L, root-cause-analyst 56L, self-review 37L, requirements-analyst 56L, audit-validator 145L, socratic-mentor 310L, rf-qa 552L, rf-qa-qualitative 1139L) exist on disk per spec §7.2's deliberate "no new agents" constraint. All 5 dependency skills exist (sc-adversarial-protocol 3002L, task-builder 2190L, sc-troubleshoot-protocol 456L, sc-brainstorm-protocol 421L, sc-task-protocol 396L). All 4 promotion-adapter target dirs (`.dev/tasks/{to-do,done}/`, `.dev/releases/{current,complete}/`) exist. The TurnLedger interface for P5 `--budget-remaining` lives at `src/superclaude/cli/sprint/models.py:693` (consumed by executor.py:35 and kpi.py:23/156/192-197).

The structural mirror baseline `.dev/eval-workspaces/sc-brainstorm/` is fully populated (SPEC.md 684L, grader.py 279L, aggregate_iteration.py 163L, skill-snapshot/brainstorm-v1.md 206L, evals/evals.json 160L) — reflect's workspace must mirror this exact shape per spec §12 line 945.

**Filepath of this research file:** `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/tasks/to-do/TASK-RF-20260527-043715-sc-reflect-rebuild/research/01-file-inventory.md`
