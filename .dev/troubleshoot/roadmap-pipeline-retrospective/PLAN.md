# Roadmap Pipeline Retrospective + Refactor — Orchestration Plan

**Generated:** 2026-05-30
**Generator:** sc:spawn (task decomposition only; execution delegated)
**Driver question:** *What recurring failures in the roadmap pipeline reveal architectural flaws so deep that targeted patches will keep losing — and what would a ground-up rewrite or refactor have to look like to make the brittleness go away permanently?*
**Workspace root:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/`

---

## Epic

> **EPIC-RPR-1:** Catalogue every roadmap-pipeline failure and remediation across the project's history, synthesize the architectural-flaw thesis, and produce a validated remediation tasklist that either (a) refactors the pipeline surgically with a brittleness-elimination contract, or (b) justifies and scopes a ground-up rewrite.

---

## Strategy

- **Coordination strategy:** Adaptive (Wave 1 parallel × 12 → Wave 2 sequential synthesis → Wave 3 parallel × 3 → Wave 4 sequential chain).
- **Why adaptive:** Wave 1 and Wave 3 are partitioned across disjoint inputs and can run independently; Wave 2 and Wave 4 require fan-in synthesis.
- **Why 12 in Wave 1:** Matches the user's request and the natural thematic clustering of 64 releases + 77 tasks (~5–10 dirs/agent → fits one Agent context window per partition).
- **Why 3 in Wave 3:** Three orthogonal analytical lenses (architecture, process, recurrence) maximize coverage without diluting per-vector depth.

---

## Wave Hierarchy

```
EPIC-RPR-1
├── Wave 1 — Retrospective extraction (12 parallel Agent calls, ~30–60 min wall-clock)
│   └── 12 partition reports under wave1-partition-reports/
├── Wave 2 — Master report synthesis (1 sequential Agent call, gates on Wave 1)
│   └── master-report.md under wave2-master-report/
├── Wave 3 — Vector analysis (3 parallel Agent calls, gates on Wave 2)
│   ├── vector-A-architecture.md
│   ├── vector-B-process.md
│   └── vector-C-recurrence.md
└── Wave 4 — Remediation pipeline (sequential chain, gates on Wave 3)
    ├── 4.1 BUILD-REQUEST → /task-builder
    ├── 4.2 Generated tasklist → /sc:reflect --depth deep
    ├── 4.3 Critical/High/Medium issues refactored back into tasklist
    └── 4.4 Final tasklist → /task (parallel agent)
```

---

## Wave 1 — Retrospective Extraction (12 partitions)

### Common per-agent contract

Every Wave-1 agent receives this preamble appended to its specific partition:

> **Role:** Retrospective analyst. Mine the provided artifact directories for every roadmap-pipeline failure, every remediation attempt, and every documented success — then produce a structured retrospective report at the specified output path.
>
> **Methodology:**
> 1. Read each directory's top-level `README.md`, `findings*.md`, `summary*.md`, `phase*-*.md`, `*-report.md`, `*audit*.md` if present.
> 2. For each artifact, classify findings as: `FAILURE` (pipeline halted, gate rejected, output malformed), `REMEDIATION` (fix attempted, diff applied, config changed), or `SUCCESS` (cleanly passed, validated, shipped).
> 3. Use **Auggie MCP** (`mcp__auggie__codebase-retrieval`) to cross-reference each failure against the current `src/superclaude/cli/roadmap/` code to determine whether the failure mode is still possible today.
> 4. Use `grep -ri "roadmap" <dir>` on each partition directory to enumerate every roadmap-touching artifact before reading; do NOT rely on filename heuristics alone.
> 5. **Evidence standard (Rule 2, discovery-tier):** Support every finding with the artifact path + section/line reference. Findings that infer cause from absence-of-evidence must be tagged `INFERENTIAL` with the reasoning chain shown.
>
> **Output schema** (per-finding):
> ```
> ### F-<partition>-<seq>: <one-line title>
> - **Type:** FAILURE | REMEDIATION | SUCCESS
> - **Pipeline step:** extract | generate-* | diff | debate | score | merge | anti-instinct | wiring-verification | test-strategy | spec-fidelity | deviation-analysis | remediate | certify | OTHER
> - **Symptom:** <one paragraph>
> - **Root cause (claimed):** <as documented> — or `UNDOCUMENTED`
> - **Remediation applied:** <fix summary + commit/PR/task ref> — or `NONE`
> - **Outcome:** <did it actually fix? recurrence? regression?>
> - **Still possible today (Auggie check):** YES | NO | UNKNOWN — with file:line evidence
> - **Source artifacts:** <list of paths>
> ```
>
> **Report tail (mandatory):**
> ```
> ## Cross-cutting patterns within this partition
> - <list of 3–7 patterns this partition reveals>
>
> ## Brittleness drivers identified
> - <list of mechanisms — not symptoms — that this partition surfaces>
> ```

### Partition assignments

> All paths absolute. `<MAIN>` = `/config/workspace/IronClaude/.dev/`. Output paths are under `<WS>/wave1-partition-reports/` where `<WS>` = `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective`.

#### A1 — Roadmap Core (v1–v3)
**Dirs:** `<MAIN>releases/complete/v1.4-roadmap-gen/`, `v2.0-roadmap-v2/`, `v2.02-Roadmap-v3/`, `v.2.11-roadmap-v4/`, `v2.26-roadmap-v5/`, `v2.22-RoadmapRemediate/`
**Output:** `<WS>/wave1-partition-reports/A1-roadmap-core.md`
**Focus:** Evolution of the core generator across 5 major versions — what got rewritten between versions, why, and what failures triggered each rewrite.

#### A2 — Roadmap Reliability + Anti-instinct
**Dirs:** `<MAIN>releases/complete/v.2.17-roadmap-reliability/`, `v3.1_Anti-instincts__/`, `obligation-vocab-alignment/`, `reflect-path-regression/`
**Output:** `<WS>/wave1-partition-reports/A2-reliability-anti-instinct.md`
**Focus:** Anti-instinct gate's full history — every false-positive class identified, every layer added, every regression.

#### A3 — Pipeline Architecture Refactor
**Dirs:** `<MAIN>releases/complete/v2.01-Architecture-Refactor/`, `v2.13-CLIRunner-PipelineUnification/`, `v3.2_fidelity-refactor___/`
**Output:** `<WS>/wave1-partition-reports/A3-architecture-refactor.md`
**Focus:** Each architectural refactor and what new failure classes it eliminated vs. introduced.

#### A4 — Validation Gates (validate, spec-fidelity, audit-gating)
**Dirs:** `<MAIN>releases/complete/v2.19-roadmap-validate/`, `v2.24.5-SpecFidelity/`, `v3.0_unified-audit-gating/`, `v3.05_DeterministicFidelityGates/`, `unified-audit-gating-v1.2.1/`, `unified-audit-gating-v2/`
**Output:** `<WS>/wave1-partition-reports/A4-validation-gates.md`
**Focus:** Gate proliferation — what fails each gate, what bypasses exist, and the false-positive/false-negative pattern across gates.

#### A5 — Halt + Preflight + Accept (failure-mode handling)
**Dirs:** `<MAIN>releases/complete/v2.25.5-PreFlightExecutor/`, `v2.25.7-Phase8HaltFix/`, `v2.24.2-Accept-Spec-Change/`, `v3.7-turnledger-integration/`
**Output:** `<WS>/wave1-partition-reports/A5-halt-preflight.md`
**Focus:** How the pipeline behaves when it fails — halt semantics, resume semantics, accept-spec-change, turn-ledger gaps.

#### A6 — Tasklist + Sprint
**Dirs:** `<MAIN>releases/complete/v2.07-tasklist-v1/`, `v2.05-sprint-cli-specification/`, `cliEval/`
**Output:** `<WS>/wave1-partition-reports/A6-tasklist-sprint.md`
**Focus:** Downstream integration — where roadmap output → tasklist generation → sprint execution breaks down and what coupling assumptions fail.

#### A7 — CLI Portify (5 generations)
**Dirs:** `<MAIN>releases/complete/v2.15-cli-portify/`, `v2.18-cli-portify-v2/`, `v2.23-cli-portify-v3/`, `v2.24-cli-portify-cli-v4/`, `v2.24.1-cli-portify-cli-v5/`, `v2.25-cli-portify-cli/`
**Output:** `<WS>/wave1-partition-reports/A7-cli-portify.md`
**Focus:** Why CLI-portify needed 5+ iterations — the inference-to-deterministic conversion arc and what kept breaking each time.

#### A8 — Adversarial + Spec Panel
**Dirs:** `<MAIN>releases/complete/v1.7-adversarial/`, `v2.09-adversarial-v2/`, `v2.10-spec-panel-v2/`
**Output:** `<WS>/wave1-partition-reports/A8-adversarial-specpanel.md`
**Focus:** Adversarial debate as a gating step — when it has caught real issues vs. when it has rubber-stamped, and the spec-panel relationship.

#### A9 — Brainstorm + Convergence + Cleanup-audit
**Dirs:** `<MAIN>releases/complete/v2.21-sc-brainstorm-auggie/`, `roadmap-cli-skill-converge/`, `cleanup-audit-v2-UNIFIED-SPEC/`, `v.1.06-CleanupAudit/`, `v2.20-WorkflowEvolution/`
**Output:** `<WS>/wave1-partition-reports/A9-brainstorm-convergence.md`
**Focus:** Inputs to the pipeline — brainstorm/convergence quality and how upstream noise propagates to roadmap failures.

#### A10 — Release Split + Workflow + Misc
**Dirs:** `<MAIN>releases/complete/release-split/`, `release-split-workspace-rca/`, `task-builder-merge/`, `cross-framework-deep-analysis/`, `v3.65-prd-refactor/`, `v3.66-tdd-skill-refactor-v2/`, `sc-reflect-rescrutiny-design.md`, `sc-reflect-rescrutiny-workflow.md`
**Output:** `<WS>/wave1-partition-reports/A10-release-split-misc.md`
**Focus:** Release-split RCA + PRD/TDD refactor — input-quality and downstream-coupling failures.

#### A11 — Roadmap E2E + Research Tasks
**Dirs:** `<MAIN>tasks/done/TASK-E2E-20260326-tdd-pipeline/`, `TASK-E2E-20260327-prd-pipeline-e2e/`, `TASK-E2E-20260402-prd-pipeline-rerun/`, `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/`, `TASK-RESEARCH-20260403-anti-instinct/`, `TASK-RF-20260402-baseline-repo/`, `TASK-RF-20260403-baseline-full/`, `TASK-RF-20260326-e2e-modified/`, `TASK-RF-20260327-prd-pipeline/`, `TASK-RF-20260403-quality-comparison/`, `RESEARCH-PROMPT-anti-instinct-gate-failure.md`, `RESEARCH-PROMPT-roadmap-tasklist-architecture-overhaul.md`, `roadmap-pipeline-deep-trace.md`
**Output:** `<WS>/wave1-partition-reports/A11-e2e-research-tasks.md`
**Focus:** End-to-end runs — what failed on real specs, what the research prompts surfaced, and what the deep-trace already concluded.

#### A12 — Spec-fidelity, sc-reflect, cliEval tasks
**Dirs:** `<MAIN>tasks/done/TASK-RF-20260527055700-spec-fidelity-canonicalizer/`, `TASK-RF-20260527-043715-sc-reflect-rebuild/`, `TASK-RF-20260525-150000/`, `TASK-RF-20260526-102600/`, `TASK-RF-20260518-cliEval-P1-pty-isolation-gates/`, `TASK-RF-20260518-cliEval-P2-loader-models-expect/`, `TASK-RF-20260518-cliEval-P3-orchestrator-runner-reporter/`, `TASK-RF-20260518-cliEval-P4-wire-and-ship/`, `TASK-RF-20260518-181333/`, `TASK-RF-20260524-issue-60-ruff-debt/`, `TASK-RESEARCH-20260403-sprint-task-exec/`, `TASK-RESEARCH-20260403-tasklist-quality/`
**Output:** `<WS>/wave1-partition-reports/A12-fidelity-reflect-cliEval.md`
**Focus:** Adjacent-system tasks that exposed roadmap-pipeline coupling — spec-fidelity canonicalizer, sc-reflect rebuild, cliEval phases.

---

## Wave 2 — Master Report Synthesis (1 agent, sequential)

**Gates on:** All 12 Wave-1 reports written and readable.

**Output:** `<WS>/wave2-master-report/master-report.md`

**Prompt:**

> **Role:** Master synthesist. Read all 12 partition reports listed below and produce a consolidated roadmap-pipeline retrospective that captures the full failure-and-remediation history without losing per-finding evidence.
>
> **Inputs (12 files):**
> 1. `<WS>/wave1-partition-reports/A1-roadmap-core.md`
> 2. `<WS>/wave1-partition-reports/A2-reliability-anti-instinct.md`
> 3. `<WS>/wave1-partition-reports/A3-architecture-refactor.md`
> 4. `<WS>/wave1-partition-reports/A4-validation-gates.md`
> 5. `<WS>/wave1-partition-reports/A5-halt-preflight.md`
> 6. `<WS>/wave1-partition-reports/A6-tasklist-sprint.md`
> 7. `<WS>/wave1-partition-reports/A7-cli-portify.md`
> 8. `<WS>/wave1-partition-reports/A8-adversarial-specpanel.md`
> 9. `<WS>/wave1-partition-reports/A9-brainstorm-convergence.md`
> 10. `<WS>/wave1-partition-reports/A10-release-split-misc.md`
> 11. `<WS>/wave1-partition-reports/A11-e2e-research-tasks.md`
> 12. `<WS>/wave1-partition-reports/A12-fidelity-reflect-cliEval.md`
>
> **Cross-reference count (Rule 3):** 12 partition reports must all be cited; the master report's bibliography must reference all 12.
>
> **Evidence standard (Rule 2, verification-tier):** Every claim made in the master report must cite the partition report (and through it, the source artifact). Synthesized claims that go beyond what any single partition documented must be flagged as `META-INFERENCE` with the partitions that support each component of the inference.
>
> **Required sections:**
> 1. **Executive summary** (≤500 words) — the single most important architectural conclusion + 3 most-confident recurrence patterns.
> 2. **Failure taxonomy** — categorical breakdown of every documented failure, with frequency, severity, and which pipeline step is affected.
> 3. **Remediation taxonomy** — categorical breakdown of every fix attempt; which fixes stuck, which regressed, which were superseded.
> 4. **Recurrence matrix** — table of failures that appeared in ≥2 partitions, with the partition list and a `RECURRENT` or `RESOLVED-FOR-NOW` verdict.
> 5. **Pipeline-step heat map** — for each pipeline step (`extract`, `generate-*`, `diff`, `debate`, `score`, `merge`, `anti-instinct`, `wiring-verification`, `test-strategy`, `spec-fidelity`, `deviation-analysis`, `remediate`, `certify`), count failures, remediations, and current-codebase risk verdict.
> 6. **Architectural-flaw thesis** — 3–7 deep flaws synthesized from the patterns, each with the evidence chain across partitions.
> 7. **Bibliography** — all 12 partition reports + a flat list of every artifact cited across them.

---

## Wave 3 — Vector Analyses (4 parallel agents — Vector D added per user opt-in)

**Gates on:** Wave 2 master report written.

### Vector A — Architectural Vector
**Output:** `<WS>/wave3-vector-analyses/vector-A-architecture.md`

**Prompt:**

> **Role:** Senior systems architect. Read `<WS>/wave2-master-report/master-report.md` and the current code at `/config/workspace/IronClaude/.claude/worktrees/BareReview/src/superclaude/cli/roadmap/` and produce an architecture-focused critique answering:
>
> 1. What is the actual current architecture of the roadmap pipeline (component graph, data flow, state)?
> 2. Which of the master report's architectural flaws are inherent to the current design (i.e., no patch can fix them without changing the design)?
> 3. What design alternatives exist for each inherent flaw? Compare with prior-art (LangGraph, DAGster, Prefect, custom DAG, finite-state-machine, actor model).
> 4. If a ground-up rewrite is required, what is the minimum viable architecture that preserves the pipeline's product value while permanently eliminating the brittleness drivers?
> 5. What is the test/eval strategy that would prove the new architecture is *not* brittle?
>
> **Evidence standard (Rule 2, discovery-tier):** Cite master-report findings + current code file:line; `INFERENTIAL` tag for architecture-quality judgments not directly derivable from cited evidence.
>
> **Use Auggie MCP** to cross-check architectural claims against the live codebase.

### Vector B — Process / Workflow Vector
**Output:** `<WS>/wave3-vector-analyses/vector-B-process.md`

**Prompt:**

> **Role:** Process / workflow engineer. Read `<WS>/wave2-master-report/master-report.md` and produce a process-focused critique answering:
>
> 1. Which failures are *not* architectural but are caused by the workflow around the pipeline (input quality, spec drift, validation lag, human-in-the-loop gaps)?
> 2. What is the input-quality contract that upstream artifacts (specs, PRDs, TDDs, brainstorm outputs) currently honor — or fail to honor — when feeding the roadmap pipeline?
> 3. Where do the existing skill protocols (sc:brainstorm, sc:roadmap, sc:tasklist, sc:task, sc:reflect) create or fail to enforce the contract?
> 4. What process-level interventions (gates moved upstream, contracts made explicit, dry-run reviewer steps, escape hatches) would reduce the failure rate without touching pipeline internals?
> 5. Which failures are *people-flexible* (the user can rephrase the input) vs. *people-trapped* (no realistic input shape avoids the failure)?
>
> **Evidence standard (Rule 2, discovery-tier):** Cite master report + skill protocol files; `INFERENTIAL` tag for workflow-quality judgments.

### Vector C — Recurrence-Pattern Vector
**Output:** `<WS>/wave3-vector-analyses/vector-C-recurrence.md`

**Prompt:**

> **Role:** Quality engineer focused on regression and recurrence. Read `<WS>/wave2-master-report/master-report.md` and produce a recurrence-focused critique answering:
>
> 1. For each failure that recurred across ≥2 partitions, what was the gap in the original fix that allowed recurrence (incomplete test coverage, missing eval corpus case, wrong abstraction level, silent feature creep)?
> 2. What does the pattern of `Fix → Recurrence → Fix` reveal about the test/eval discipline of the project?
> 3. What missing test/eval/audit machinery would have caught each recurrence at the time of the original fix?
> 4. What is the **brittleness-elimination contract** — a checklist that any future fix to the roadmap pipeline must satisfy to be considered durable?
> 5. Where does the project's existing test suite, eval corpus, audit gating, and adversarial review cover and fail to cover the brittleness drivers?
>
> **Evidence standard (Rule 2, discovery-tier):** Cite master report + current `tests/` files + audit reports; `INFERENTIAL` tag for verdicts on durability.

### Vector D — Cost & Token-Efficiency Vector
**Output:** `<WS>/wave3-vector-analyses/vector-D-cost.md`

**Prompt:**

> **Role:** Token-economics engineer. Read `<WS>/wave2-master-report/master-report.md` and produce a cost-focused critique answering:
>
> 1. Which failure modes drive re-runs of expensive pipeline stages (`generate-opus-architect` ~780s, `generate-sonnet-architect` ~1320s, `merge` ~500s)? Estimate token-burn per recurrence.
> 2. Which dead-output artifacts (failed gate halts, abandoned drafts, superseded versions) sit in `.dev/releases/complete/` representing sunk token cost?
> 3. Where would early-failure detection (cheap pre-flight checks before expensive stages) prevent the most token burn? Rank by expected value.
> 4. Does the brittleness disproportionately affect specific input sizes / spec types? (e.g., large merged-requirements docs vs. small ones)
> 5. What is the cost-effectiveness ranking of Vector A's architectural alternatives, considering both build cost and steady-state operating cost?
>
> **Evidence standard (Rule 2, discovery-tier):** Cite master report + observable runtimes from log snippets in artifact directories; `INFERENTIAL` tag for cost projections.

---

## Wave 4 — Remediation Pipeline (sequential chain)

**Gates on:** All 3 vector analyses written.

### 4.1 — /task-builder invocation

**BUILD-REQUEST file:** Write to `<WS>/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md`

**BUILD-REQUEST contents (template — fill from Wave 3 outputs):**

```markdown
# BUILD-REQUEST: Roadmap Pipeline Brittleness-Elimination Refactor (or Rewrite)

## Goal
Eliminate the architectural and process flaws documented in:
- <WS>/wave2-master-report/master-report.md
- <WS>/wave3-vector-analyses/vector-A-architecture.md
- <WS>/wave3-vector-analyses/vector-B-process.md
- <WS>/wave3-vector-analyses/vector-C-recurrence.md

## Decision required up front
Vector A's analysis ranks the inherent-flaw count against the patch-fixable count.
If inherent-flaw count >= 3 and any single flaw scopes to "cross-cutting state",
this task is a REWRITE; otherwise it is a REFACTOR. Codify the decision in the
task's frontmatter `category` field before checklist generation.

## Brittleness-elimination contract (from Vector C)
<insert the contract Vector C produced verbatim>

## Scope
- In: src/superclaude/cli/roadmap/, tests/roadmap/, src/superclaude/skills/sc-roadmap-protocol/
- Out: src/superclaude/cli/sprint/, tasklist generation (those are downstream consumers)

## Acceptance gates
- All current passing tests in tests/roadmap/ still pass.
- The pipeline runs on every spec under .dev/releases/complete/*/spec*.md (or equivalents) without halting on anti-instinct false-positives of the classes catalogued in the master report's failure taxonomy.
- A new test/eval corpus added to tests/roadmap/eval-corpus/ contains one regression case for every RECURRENT failure in the master report's recurrence matrix.

## Evidence
All findings cited in scope come from the master-report + 3 vector analyses. The
task-builder must NOT invent new requirements; if a requirement cannot be
sourced to one of those four files, drop it.

## Notes
- Sync src/superclaude/ → .claude/ via `make sync-dev` before any commits.
- Pre-existing CLAUDE.md rules apply (PR target = IronbellyOrg, no .claude/ commits, etc.).
- This is a brittleness-elimination effort: every checklist item MUST cite the failure pattern it eliminates.
```

**Invocation:**
```
/task-builder <WS>/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md
```

**Expected output:** MDTM task file at `.dev/tasks/to-do/TASK-RF-<DATE>-roadmap-pipeline-rewrite/` containing the generated checklist + research files.

### 4.2 — /sc:reflect --depth deep validation

**Invocation:**
```
/sc:reflect --depth deep --target <task-file-path-from-4.1> --against <WS>/wave2-master-report/master-report.md,<WS>/wave3-vector-analyses/vector-A-architecture.md,<WS>/wave3-vector-analyses/vector-B-process.md,<WS>/wave3-vector-analyses/vector-C-recurrence.md
```

This is the UC-1 (pre-execution) mode of sc:reflect: validate the tasklist against the source specs for coverage, gaps, and best-practice compliance. Tier 2 (heterogeneous reviewer ensemble) is what `--depth deep` triggers.

### 4.3 — Refactor Critical/High/Medium issues back into the tasklist

Per the user's instruction: "refactoring all critical, high and medium issues". Two ways this can happen:

- **Option A (preferred per `feedback_prefer_simpler_proposals.md`):** /sc:reflect's Tier 3 hands off to /task-builder for a corrective MDTM remediation. Re-invoke that path until all critical/high/medium issues are addressed; loop terminates when Tier 2 reports zero such issues.
- **Option B:** Manually re-invoke /task-builder with a follow-up BUILD-REQUEST that explicitly addresses each issue from 4.2's report. Lower latency, higher cognitive load on the user.

### 4.4 — Final tasklist execution

**Invocation (must be a parallel/background agent so the user's foreground stays usable):**
```
Agent({
  subagent_type: "claude",
  description: "Execute roadmap-pipeline rewrite tasklist",
  prompt: "Execute the MDTM task at <final-task-path-from-4.3>. Use the /task skill. Follow the F1 execution loop. Spawn parallel subagents for independent checklist items. Report progress via frontmatter and task log. Do not stop on first failure — continue all independent items, then surface the cohort of failures at the end."
})
```

**Note on Workflow vs. Agent:** Wave-4 parallel execution could use the `Workflow` tool for deterministic orchestration. Per the workflow opt-in rule, that requires explicit user permission with the word "workflow" or ultracode mode. Default to a single background Agent unless the user explicitly opts into Workflow.

---

## Dependency graph

```
                      ┌──── A1 ────┐
                      ├──── A2 ────┤
                      ├──── A3 ────┤
                      ├──── A4 ────┤
                      ├──── A5 ────┤
[ inventory paths ] ──┼──── A6 ────┼──> [ Wave 2 master ] ──┐
                      ├──── A7 ────┤                         │
                      ├──── A8 ────┤                         │
                      ├──── A9 ────┤                         │
                      ├──── A10 ───┤                         │
                      ├──── A11 ───┤                         │
                      └──── A12 ───┘                         │
                                                             │
                                                             ▼
                                              ┌────── Vector A ──────┐
                                              ├────── Vector B ──────┤───┐
                                              └────── Vector C ──────┘   │
                                                                          │
                                                                          ▼
                                                          ┌── 4.1 /task-builder ──┐
                                                          ├── 4.2 /sc:reflect ────┤
                                                          ├── 4.3 refactor loop ──┤
                                                          └── 4.4 /task execute ──┘
```

---

## Per-wave gating contract

Before launching the next wave, verify the previous wave's outputs:

| Wave | Pre-launch check | Command |
|---|---|---|
| Wave 2 | All 12 partition reports exist and are non-empty | `ls -la <WS>/wave1-partition-reports/ \| wc -l` (≥13) and `find <WS>/wave1-partition-reports/ -name "*.md" -size -500c` (should be empty) |
| Wave 3 | Master report exists and contains all 7 required sections | `grep -c "^## " <WS>/wave2-master-report/master-report.md` (≥7) |
| Wave 4.1 | All 3 vector analyses exist and each contains its required questions answered | `for v in A B C; do grep -c "^[0-9]\." <WS>/wave3-vector-analyses/vector-$v-*.md; done` (each ≥5) |

If any gate fails, **do not proceed** — surface the gap and re-run only the failing partition/synthesis/vector, not the whole wave.

---

## Cost & duration estimate

| Wave | Agents | Per-agent runtime | Wall-clock | Notes |
|---|---|---|---|---|
| 1 | 12 parallel | 8–20 min | ~20 min | Bound by slowest partition (likely A11 or A12 with most artifacts) |
| 2 | 1 sequential | 15–30 min | ~25 min | Reads 12 markdown reports + synthesizes |
| 3 | 3 parallel | 20–40 min | ~35 min | Architecture vector is heaviest due to Auggie cross-check |
| 4.1 | 1 (/task-builder) | 10–20 min | ~15 min | Standard task-builder runtime |
| 4.2 | 1 (/sc:reflect --depth deep) | 25–45 min | ~35 min | Tier 2 heterogeneous ensemble |
| 4.3 | 1 (/task-builder loop) | varies | 0–60 min | Loop terminates when no Critical/High/Medium remain |
| 4.4 | 1 background agent | 1–5 hours | async | User can monitor via task notification |

**Total foreground wall-clock to Wave 4 launch:** ~2.5 hours (Waves 1+2+3 sequential gating).
**Wave 4.4 background execution:** decoupled; user is not blocked.

---

## What sc:spawn produces — and what it does NOT

Per the command's CRITICAL BOUNDARIES section:

**This document is the deliverable.** sc:spawn stops here.

**Next steps require user action:**

1. Review this plan for partition correctness and prompt sufficiency.
2. Approve to launch Wave 1 — paste the next-step prompt below, or hand the plan back to me in a new message saying "execute Wave 1".
3. After Wave 1 completes, repeat the launch ritual for Waves 2, 3, 4.1, 4.2, 4.3, 4.4.

**Recommended launch prompt for Wave 1** (paste back to me to execute):

```
Read /config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/PLAN.md
and launch Wave 1: spawn 12 parallel Agent calls per the partition assignments,
one per partition (A1–A12), using the common per-agent contract from the
"Wave 1 — Retrospective Extraction" section. Each agent writes to its
specified output path. Report when all 12 are done; do NOT auto-launch Wave 2.
```

---

## Open decisions for the user (before Wave 1 launches)

1. **Subagent type for Wave 1.** Default = `general-purpose` (broad tool access). Alternative = `Explore` (faster, read-only, no Write). Discovery work needs Write to produce reports, so `general-purpose` is correct unless you want me to do the writes from a fan-in synthesist instead.
2. **Worktree isolation for Wave 4.4.** The execution agent for the rewrite/refactor task should likely run in its own worktree to avoid contaminating this BareReview branch. Confirm or override.
3. **Workflow tool opt-in.** If you want Wave 1+3 to run via the `Workflow` tool (deterministic, resumable, journalled) instead of plain Agent calls, say so — that's the multi-agent escalation pattern and it requires explicit opt-in.
4. **Vector-D candidate.** Three vectors is per your spec, but a fourth — *Cost & Token-Efficiency Vector* — might be worth adding: it would assess whether the pipeline's brittleness is also a token-burn driver, not just a correctness driver. Cheap to add now, hard to retrofit later. Skip or add?
