# Research Notes: Implement sc:reflect V3 Serena Low-Complexity Adoptions (FR-RV3-LOW.1–8)

**Date:** 2026-06-02
**Scenario:** A (Explicit — exhaustive spec with FR list, insertion anchors, implementation order, OQ preconditions)
**Depth Tier:** Deep
**Track Count:** 1 (single track — all 8 FRs touch the same `SKILL.md` + shared refs with hard inter-FR dependencies; NOT independent work streams)
**Source spec:** `.dev/releases/current/Reflect-V3-Serena/04-spec-low-complexity.md`
**Target skill:** `src/superclaude/skills/sc-reflect-protocol/`

---

## EXISTING_FILES

### Primary integration surface (MODIFIED)
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — **1585 lines**. The protocol body. Key anchors VERIFIED in scope discovery:
  - Frontmatter `allowed-tools` (line ~1): currently lists `find_symbol, find_referencing_symbols, get_symbols_overview, get_diagnostics_for_file, read_memory, write_memory, list_memories, search_for_pattern, activate_project`. Does NOT list the 7 tools to add. Correctly does NOT list `check_onboarding_performed` (FR-6.3 invariant already holds).
  - `## 6. Modern Serena Tool Usage` (~line 350)
  - `### 6.1 Mandatory evidence-gathering chain (Wave 1A)` (~line 358-371) — steps 1-6, ends at re-Read. **No** find_implementations/find_declaration/include_info/search_deps/summarize_changes. Confirms FR-1/2/3/4/5 insertion points.
  - `### 6.3 Memory pattern` (~line 373-383) — retention rule "keep last 20 / expire >90d" STATED but only read/write/list wired. No delete/rename/edit. Confirms FR-8.
  - `### 6.5 Fail-open policy` (~line 397-399).
  - `### 9.1 Stable contract (contract_version: 1.0)` — **line 491** (OQ-2 RESOLVED POSITIVE).
  - `### 9.2 Telemetry (non-stable)` — **line 601** (OQ-2 RESOLVED POSITIVE).
  - `### 10.2 Necessary deviation` — **line 689** (OQ-2 RESOLVED POSITIVE).
  - `### 10.3 Drift` — **line 704** (OQ-2 RESOLVED POSITIVE).
  - §4.0 Wave 0 (~:172-225), §4.1 Wave 1B.3 (~:233-241) — spec citations consistent with discovery.
- `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` — 9150 B. EXISTS. Gains `S_dev_density` sub-terms (FR-1/6/7).
- `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` — 7995 B. EXISTS. Gains `third_party_api_verified` (FR-4) + `serena_summary_corroboration` (FR-5) classifier inputs.
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` — 7008 B. EXISTS. Gains find_implementations list + extended-info into Wave 3 per-reviewer brief.

### OQ-5 RESOLVED
- `refs/return-contract.yaml` **DOES NOT EXIST**. The return contract is **inline in SKILL.md §9** (lines 491-600+). → §5 contract additions + `contract_version` bump to `1.1.0` edit **SKILL.md §9.1**, NOT a separate YAML file. The spec §4.2 row was marked "(if present — see OQ-5)"; confirmed absent.

### Eval workspace (NEW case dirs to create)
- `.dev/eval-workspaces/sc-reflect/cases/` EXISTS. Existing cases: `falsifier-suite`, `post-large-diff-mixed`, `post-small-diff-clean`, `pre-trivial-coverage-gap`, `promotion`.
- Case structure: `expected.yaml` + `input/` (UC-2: `diff.patch` + `tasklist.md`; UC-1: `spec.md` + `tasklist.md`).
- `grader.py` (20939 B) + `aggregate_iteration.py` + `SPEC.md` (155 KB) at workspace root.
- 6 NEW case dirs required (per spec §4.1 / §8.1): `serena-find-implementations`, `serena-find-declaration`, `serena-search-deps`, `serena-wave0-config`, `serena-memory-retention`, `serena-summarize-changes`.

### Per-run runtime artifacts (NOT committed source — contract completeness only)
- `<output>/serena-config-snapshot.yaml` (FR-7), `<output>/serena-change-summary.md` (FR-5).

### Supporting context (READ-ONLY inputs)
- `.dev/releases/current/Reflect-V3-Serena/01-matrix-low-complexity.md` (59 KB) — the 8-row matrix + per-row deep dives the spec derives from. All `01-matrix:NNN` citations point here.
- `.dev/releases/current/Reflect-V3-Serena/03-conversation-context.md` (10 KB) — read-only posture (§3), deviation taxonomy (§4), exclusions (§5).
- `.dev/releases/current/Reflect-V3-Serena/04-spec-low-complexity.md.review.md` (19 KB) — spec-panel critique: R1-R6, A1-A5, C1-C5 findings + State Variable Registry. Spec already incorporates these ("resolves review finding X" annotations).

### MDTM template
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` (and src mirror) — Template 02. Builder reads PART 1.

---

## PATTERNS_AND_CONVENTIONS

- **Per-step audit emit convention** (SKILL.md §4 ~:124): every wave step emits one `audit.log` row. Every new tool call MUST emit `<tool>_invoked` + telemetry fields on BOTH success and degraded paths (NFR-2).
- **Fail-open envelope** (§6.5 ~:397-399): missing/error → `degraded: [<tool>]` audit entry → native Grep/Glob fallback → continue; never abort. Every new call inherits this (NFR-1).
- **degraded_components tokens** introduced by this work: `find_implementations:lsp_unsupported`, `find_declaration`, `search_deps:lsp_unindexed`, `get_current_config`, `serena:context-excluded`, `serena:pre-v1.5-no-rename-propagation`.
- **Telemetry-vs-contract split** (resolves A3): §9.1 contract fields are versioned (`contract_version` 1.0.x → 1.1.0 minor bump covers FR-1/2/4/5 only); §9.2 telemetry fields (FR-6/7/8) are observability, NOT contract — added without a bump.
- **SoT discipline**: ALL edits land in `src/superclaude/` then `make sync-dev`; `make verify-sync` before commit. NEVER touch `.claude/` paths directly. (CLAUDE.md ABSOLUTE RULE.)
- **Citation freshness** (§6.2 / CLAUDE.md S1): any new `file:line` citation re-Read within last 5 tool calls (NFR-4).

---

## GAPS_AND_QUESTIONS

OQ items the spec §10 explicitly directs task-builder to turn into precondition research items. Status after orchestrator scope discovery:

- **OQ-1** (FR-3): Is `find_referencing_code_snippets` still standalone or absorbed into `find_referencing_symbols(include_info)`? → RUNTIME PROBE against live Serena MCP; merge precondition for FR-3. UNRESOLVED — researcher must document the probe procedure + the matrix evidence.
- **OQ-2** (FR-1.3/4.3/5.2/5.3 anchors): **RESOLVED POSITIVE** in scope discovery — §9.1/§9.2/§10.2/§10.3 all exist. Researcher confirms exact line ranges for builder anchoring.
- **OQ-3** (FR-5): exact `summarize_changes` signature/param shape (prompt-based, "not surfaced"). → pilot in eval case before promoting. Researcher documents what's known + the pilot procedure.
- **OQ-4** (FR-7): `get_current_config` return shape (inferred, "not version-stable"). → defensive field-presence parse + runtime probe. Researcher documents known shape + defensive-parse requirement.
- **OQ-5** (refs structure): **RESOLVED** — no return-contract.yaml; contract inline in SKILL.md §9.
- **OQ-6** (FR-1.4): `find_implementations` empty-vs-error disambiguation via `get_diagnostics_for_file`. → resolved in FR-1 eval case (eval-authoring time, NOT task-build). Note as eval-case requirement.
- **OQ-7** (global Serena floor): v1.3.0 (symbol tools) vs v1.5.0 (memory/onboarding). → decided in Phase 1 via FR-7 fingerprint; per-FR floors (FR-1/2=v1.3.0, FR-6/8=v1.5.0). Note for FR-7 phase.

Task-build-time probes/checks the builder must create as precondition items: **OQ-1, OQ-2, OQ-3, OQ-4, OQ-5**. OQ-6/OQ-7 are eval-authoring/Phase-1 concerns, NOT task-build preconditions.

---

## RECOMMENDED_OUTPUTS

Research files (codebase-grounded, evidence-based with file:line):

| # | File | Topic |
|---|------|-------|
| 01 | `research/01-skill-insertion-points.md` | Exact current SKILL.md anchors/line-ranges for every FR insertion point + frontmatter |
| 02 | `research/02-patterns-conventions.md` | House style: wave-step phrasing, audit.log emit, fail-open envelope, telemetry/degraded conventions |
| 03 | `research/03-refs-and-inline-contract.md` | reflection-rubric.md / deviation-taxonomy.md / reviewer-spec.md structure + inline §9.1/§9.2 contract block |
| 04 | `research/04-eval-workspace-conventions.md` | Eval case dir schema, expected.yaml, grader.py yaml_field assertions, existing-case scaffolds |
| 05 | `research/05-mdtm-template-and-examples.md` | Template 02 PART 1 rules + prior TASK-RF example patterns |
| 06 | `research/06-serena-surface-oq-probes-review.md` | Matrix per-row deep dives, Serena CHANGELOG facts, OQ-1/3/4 probe procedures, R/A/C review findings |

---

## SUGGESTED_PHASES

6 parallel researchers (Deep tier), single track, all spawned in one message:

1. **Researcher 1 — File Inventory (SKILL.md insertion points)**: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. Catalog EXACT current line ranges for: frontmatter `allowed-tools`; §4.0 Wave 0 (0.5 alias, 0.7 activate); §4.1 Wave 1B.3; §6.1 steps 1-6; §6.3 memory; §6.5 fail-open; §9.1 contract; §9.2 telemetry; §10.2/§10.3 classifiers; §4 audit emit convention. Per insertion point: which FR plugs in, what the surrounding text looks like, the precise sub-step number to add. Output → `research/01-skill-insertion-points.md`. Others cover: refs (R3), patterns (R2), eval (R4), template (R5), Serena surface (R6).
2. **Researcher 2 — Patterns & Conventions**: Read 4-6 representative SKILL.md wave steps + the §6.5 envelope + existing telemetry rows. Extract: how a conditional step is phrased, how audit.log rows are written, fail-open phrasing template, degraded-token format, telemetry field naming. Output → `research/02-patterns-conventions.md`.
3. **Researcher 3 — refs/ + inline §9 contract**: Read `refs/reflection-rubric.md` (locate S_dev_density), `refs/deviation-taxonomy.md` (§10.2/§10.3 classifier inputs), `refs/reviewer-spec.md` (Wave 3 brief / step 3B.0), and SKILL.md §9.1 (line 491+) / §9.2 (line 601+) inline contract block. Document exact edit targets + current contract_version + where each new field lands. Output → `research/03-refs-and-inline-contract.md`.
4. **Researcher 4 — Eval-workspace conventions**: Read `grader.py` (yaml_field assertion mechanism for NFR-2), `expected.yaml` schema across 2-3 existing cases, the input/ layout (UC-1 vs UC-2), `aggregate_iteration.py`. Document how to scaffold the 6 new `serena-*` cases + how telemetry assertions are graded. Output → `research/04-eval-workspace-conventions.md`.
5. **Researcher 5 — Template & Examples**: Read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (A3 granularity, A4 iterative, B2 self-contained, L1-L6 handoff). Check `.dev/tasks/to-do/TASK-RF-*` for a complex-task example. Output → `research/05-mdtm-template-and-examples.md`.
6. **Researcher 6 — Serena surface + OQ probes + review findings**: Read `01-matrix-low-complexity.md` (per-row deep dives for rows 1-8), extract Serena CHANGELOG facts (v1.3.0 symbol tools 2026-05-11; v1.5.0 memory mem: propagation + check_onboarding_performed deletion 2026-05-18; v1.2.0 path-traversal guard), document OQ-1/OQ-3/OQ-4 runtime-probe procedures, and pull the R/A/C findings from `04-spec-low-complexity.md.review.md` (esp. C1 unbounded-memory, C2 unknown-version, C3 trait-as-Class). Output → `research/06-serena-surface-oq-probes-review.md`.

---

## TEMPLATE_NOTES

- **Template: 02 (Complex Task)** — discovery (OQ probes) before building; multiple distinct activity phases (Wave-0 wiring, symbol-chain wiring, memory wiring, refs/contract edits, eval-case authoring, sync+verify, QA gates); version-conditional flows (FR-6/8 gated on FR-7 fingerprint); fail-open conditionals.
- **Tier: Deep** — 8 FRs, ≥5 modified files (SKILL.md + 3 refs + inline §9), 6 new eval cases, 5 task-build-time OQ preconditions.
- Phase ordering MUST follow spec §4.6 (authoritative, maps 1:1 to §9 rollout): OQ probe preconditions → FR-7+FR-6 (Wave-0) → FR-1+FR-2 (symbol chain) → FR-4 (search_deps) → FR-8 (memory CRUD) → FR-3 (probe-gated) → FR-5 (pilot last). Each phase ends with `make sync-dev` + `make verify-sync` and the relevant eval-case scaffold.
- QA_GATE_REQUIREMENTS: **PER_PHASE** (spec is correctness-sensitive, version-gated, fail-open contracts). VALIDATION: `make verify-sync` + markdownlint on edited .md + frontmatter `allowed-tools` static assertions (FR-6.3). TESTING: eval-workspace cases (NONE in the pytest sense; the "tests" are eval cases scaffolded per FR — author the case dir + expected.yaml, not execute the full eval here).
- **Granularity**: per-FR build items, per-file edit items, per-new-eval-case items, per-OQ-probe precondition items. NOT batch "wire all 8 FRs."
- **EXECUTION_CONTEXT_REQUIREMENTS**: AUTO (≥3 source areas: SKILL.md, refs/, eval-workspaces — block should emit; NO file:line in the header).

---

## AMBIGUITIES_FOR_USER

- **Scope of "implement"**: The task file covers wiring all 8 FRs into SKILL.md + refs + frontmatter, scaffolding the 6 eval-case dirs (dir + input fixtures + expected.yaml), and the OQ probe preconditions — but NOT executing the full eval-workspace grader run, and NOT opening the 6 per-phase PRs (the spec's §9 "one PR per phase" is a rollout recommendation; the MDTM produces the changes, the user manages PR splitting). This is the most reasonable interpretation of "build a task for the spec"; flagged here for confirmation at A.11. If the user wants the eval grader actually executed or per-phase PRs auto-created, that is a larger scope.
- Otherwise intent is clear from the spec and codebase context.
