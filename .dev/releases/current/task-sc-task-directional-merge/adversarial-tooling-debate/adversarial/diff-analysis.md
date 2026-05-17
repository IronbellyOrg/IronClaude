# Diff Analysis: sc:tasklist vs task-builder (Skill Spec Comparison)

## Metadata
- Generated: 2026-05-17T02:50:00+00:00
- Variants compared: 2
- Variant A: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1,390 lines)
- Variant B: `src/superclaude/skills/task-builder/SKILL.md` (1,838 lines)
- Mode: A (compare existing files)
- Focus: determinism, evidence-basis, output-schema, validator-coverage, compliance-tier-integration, execution-downstream, parallelism, suitability-for-current-roadmap
- Total differences: 6 structural, 8 content, 1 contradiction, 6 unique, 4 shared assumptions
- Note: These artifacts represent two different problem-classes; "diff" enumerates *operational asymmetries* relevant to a tool-choice decision.

## Structural Differences

| # | Area | Variant A (sc:tasklist) | Variant B (task-builder) | Severity |
|---|------|-------------------------|--------------------------|----------|
| S-001 | Output cardinality | N+1 files (1 index + N phase files), where N = phase count from roadmap | 1 file (single MDTM task) + research artifacts + QA reports in `${TASK_DIR}` | High |
| S-002 | Input contract | "Exactly one input: the roadmap text" (deterministic transform) | GOAL + WHY + WHERE + optional BUILD_REQUEST file (free-form, requires triage) | High |
| S-003 | Phase model | Roadmap milestones → numbered phases (no gaps; missing Phase 8 rule) | Single phase via F1 execution loop; no phase decomposition | High |
| S-004 | Output tree shape | `TASKLIST_ROOT/{tasklist-index.md, phase-N-tasklist.md, artifacts/, evidence/, checkpoints/, validation/, execution-log.md, feedback-log.md}` | `${TASK_DIR}/{${TASK_ID}.md, research/, qa/, research-notes.md}` | Medium |
| S-005 | Persistence root | `.dev/releases/current/<segment>/` (auto-derived from roadmap content via 3-step priority) | `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/` (timestamped, no roadmap binding) | High |
| S-006 | Validator integration | `superclaude tasklist validate` CLI subcommand validates output against source roadmap with drift detection + auto-patch | rf-analyst + rf-qa subagents validate research; rf-qa task-integrity validates task file; rf-qa-qualitative validates operational soundness | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Determinism guarantee | "Same input → same output" stated as hard objective; deterministic algorithm (Section 4) with explicit tie-breakers (4.9) and no policy forks | Determinism not asserted; output shaped by parallel-subagent research findings (probabilistic by construction); template selection is human-judgment | High |
| C-002 | Evidence basis | Roadmap is the **only source of truth**; "no file/system access claims"; "no invented context"; "no external browsing" — hard rule. Optional --spec TDD enrichment, --prd-file PRD enrichment | "Evidence-based codebase research — parallel agents read actual source files, trace actual dependencies, document with file paths and line numbers"; rf-analyst verifies completeness | High |
| C-003 | Tier classification | Built into every task as a first-class field: STRICT/STANDARD/LIGHT/EXEMPT; verification routing per tier (Section 4.10); tier conflict resolution (4.9) with priority `STRICT > EXEMPT > LIGHT > STANDARD` | Not present. Tasks have phases, not tiers. Compliance routing is the responsibility of the executor (`/task` skill) | High |
| C-004 | Parallelism model | None at generation time (deterministic single-pass) | Heavy: 3-8 parallel researchers + rf-analyst + rf-qa in parallel via Agent tool; up to 5 parallel tracks for multi-deliverable requests | High |
| C-005 | Quality gates | Post-generation: validate against roadmap → drift detection → auto-patch → spot-check verify (Stages 7-10 inferred from "Roadmap-validated" claim) | Multi-stage: research sufficiency review (A.5) → rf-analyst + rf-qa research gate (A.8) → optional web research (A.8.5) → rf-qa task-integrity validation (A.10) → rf-qa-qualitative operational validation (A.10.5) | High |
| C-006 | Downstream consumer | Sprint CLI (`superclaude sprint run <tasklist-index.md>`) — phase files discovered via regex on naming convention (`phase-N-tasklist.md`); each task dispatched to `/sc:task` with tier-classified compliance routing | `/task` skill (F1 execution loop) — checklist items processed sequentially; subagents spawned per item; progress tracked via frontmatter and task log | High |
| C-007 | Resume/idempotence | Pipeline state via `.roadmap-state.json` (auto-wires TDD/PRD on resume); validation reports persisted in `validation/` | Multi-checkpoint resume (A.1) — folder-state introspection determines resume point: research → QA → builder → structural validation → qualitative validation → present | Medium |
| C-008 | Clarification handling | Inserts **Clarification Task** rows in the tasklist when info missing (4.6); confidence-triggered clarification when tier confidence <0.70 | Asks user a 4-question clarification template inline before proceeding; "Do NOT interrogate" rule for non-essential questions | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Treatment of source-document access | "No file/system access claims. You must not claim to have read, searched, opened, or modified any files, repos, tickets, or external resources unless their contents are explicitly included in the user-provided input." | "Evidence-based codebase research — parallel agents read actual source files, trace actual dependencies, and document actual behavior with file paths and line numbers." | High — fundamental philosophical opposition. A enforces hermetic/transform purity from a single input; B mandates broad codebase reads as evidence. Both are correct for their respective use cases; the contradiction is *between use cases*, not within either skill. |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A | Sprint-CLI compatibility (regex-discoverable `phase-N-tasklist.md` filenames) | High — enables `superclaude sprint run` orchestration over 132-task roadmap |
| U-002 | A | Tier classification baked into every task at generation time (no post-hoc tagging) | High — drives downstream compliance enforcement per tier in `/sc:task` |
| U-003 | A | Atomicity-binding awareness via deterministic compound-deliverable preservation (per recent validator finding: "atomic-by-design clusters") | High — directly relevant to current roadmap's ME-6/S-2/S-3 atomic-landing requirements |
| U-004 | B | Zero-trust QA at three gates (rf-analyst, rf-qa, rf-qa-qualitative) — each "assumes everything is wrong until independently verified" | High for novel implementations; lower marginal value for already-validated roadmaps |
| U-005 | B | Multi-track parallelism (up to 5 tracks) for genuinely independent deliverables | Medium — relevant only when the request decomposes into independent work streams; not the case here (single roadmap, atomic landings) |
| U-006 | B | Web research as conditional capability (rf-task-researcher with WebSearch) — fills external knowledge gaps | Medium — useful when roadmap items reference unknown external standards; not load-bearing for current roadmap |

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Promoted |
|---|------------|------------------|----------------|----------|
| A-001 | The user's input artifact (roadmap or GOAL) is the authoritative scope boundary | Both refuse to invent context beyond input | STATED | No (explicit in both) |
| A-002 | Markdown is the canonical output format | Both write `.md` artifacts exclusively | STATED | No |
| A-003 | An executor will consume the output and run it later (the skill itself does not execute) | Both stop at file generation; both reference an executor skill (`/sc:task` vs `/task`) | STATED | No |
| A-004 | The user can articulate intent well enough to be processed without iterative clarification | A: roadmap is "deterministic input"; B: triages but says "Do NOT interrogate" | UNSTATED → PROMOTED | Yes — A-004 [SHARED-ASSUMPTION] |

### Promoted Assumption A-004

When the roadmap is high-quality (well-structured, IDs assigned, dependencies explicit, atomicity bindings declared) — as is the case for the current 132-task roadmap with `tasklist_ready: true` — both skills' implicit "intent is clear" assumption holds. When the roadmap is *not* high-quality, A's deterministic transform produces low-information output (vague tasks); B's research process can compensate by reading actual code. **For the current roadmap, A-004 is satisfied.**

## Summary

- Total structural differences: 6 (3 High, 2 Medium, 1 High)
- Total content differences: 8 (6 High, 2 Medium)
- Total contradictions: 1 (High — philosophical, not erroneous)
- Total unique contributions: 6 (4 High value)
- Total shared assumptions surfaced: 4 (STATED: 3, UNSTATED→PROMOTED: 1, CONTRADICTED: 0)
- Highest-severity items: S-001, S-002, S-003, S-005, C-001, C-002, C-003, C-004, C-005, C-006, X-001, U-001, U-002, U-003, U-004

**Total diff points (for convergence denominator): 25** (6 + 8 + 1 + 6 + 4 promoted assumptions — only A-004 is promoted, so 25 total: S=6, C=8, X=1, U=6, A=4 = 25)
