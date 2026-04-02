---
title: "PRD: Port sc:tasklist to CLI Runner Pipeline"
version: v4.xx
status: draft
generated: 2026-03-25
scope: tasklist-cli-port
migration: hard cutover (no backward compatibility)
---

# PRD: Port sc:tasklist to CLI Runner Pipeline

## 1. Problem Statement

`sc:tasklist` is a 10-stage LLM-interpreted markdown protocol. Its core algorithms (ID assignment, tier scoring, phase bucketing, effort/risk mapping) are deterministic by specification but non-deterministic in practice because they execute as LLM prompt instructions, not Python code. This causes:

1. **Output variance** across runs with identical input
2. **No codebase awareness** — the protocol treats the roadmap as the only source of truth and never reads source code, producing vague tasks ("ensure X", "align Y") that require downstream agents to re-derive architectural decisions
3. **No complexity-gated review** — all tasks are treated equally regardless of integration risk
4. **No programmatic gate enforcement** — validation is LLM-judged, not structurally checked

## 2. Solution

Port `sc:tasklist` to the CLI runner pipeline (same architecture as `src/superclaude/cli/roadmap/`). Use `superclaude cli-portify run` to generate the initial port scaffold, then refactor to address the 4 gaps identified in the process analysis.

### 2.1 Porting strategy

1. Run `superclaude cli-portify run sc:tasklist` to generate the initial CLI pipeline scaffold
2. Refactor the generated scaffold to implement deterministic Python stages
3. Add the 3 new stages (code-read, adversarial, decision-record input mode)
4. Hard cutover: replace `sc:tasklist` command to invoke CLI pipeline instead of skill protocol

## 3. Target Architecture

The ported pipeline lives at `src/superclaude/cli/tasklist/` following the established CLI runner pattern:

```
src/superclaude/cli/tasklist/
  __init__.py
  commands.py          # Click CLI: superclaude tasklist run
  executor.py          # Step list builder + step runner dispatch
  gates.py             # GateCriteria per step
  models.py            # TasklistConfig, data models
  prompts.py           # Prompt builders for LLM steps only
  parser.py            # Roadmap parser (deterministic)
  bucketer.py          # Phase bucketing (deterministic)
  converter.py         # Roadmap items -> tasks (deterministic)
  enricher.py          # Tier/effort/risk/complexity scoring (deterministic)
  renderer.py          # Markdown + JSON output writers (deterministic)
  code_reader.py       # Stage 0: codebase reader + decision lock
  adversarial.py       # Stage 6.5: complexity-gated review orchestrator
  validator.py         # Stage 7: parallel validation agent spawner
  patcher.py           # Stages 8-9: patch plan + execution
  verifier.py          # Stage 10: spot-check
```

## 4. Stage Pipeline (13 stages)

### Stage 0: Code-Read + Decision Lock (NEW)
- **Type:** Deterministic Python + Auggie MCP
- **Input:** `--codebase <paths>` (optional, auto-detected, or explicit)
- **Does:**
  - Reads specified source files via Auggie MCP for semantic search + direct file reads
  - Traces function call chains, identifies dead code, maps producer/consumer relationships
  - Produces structured decision record: canonical names, execution model per item, inter-step data format, resume behavior
- **Output:** `decision-record.json` + `decision-record.md`
- **Gate:** Zero unresolved items. Every referenced file exists. Every decision locked.
- **Skip condition:** No `--codebase` flag and no codebase references detected in roadmap

### Stage 1: Input Ingest
- **Type:** Deterministic Python
- **Input:** Roadmap file (+ optional spec file)
- **Does:** Read, validate non-empty, parse structure
- **Output:** Raw parsed input context
- **Gate:** Non-empty input, required sections present

### Stage 2: Parse + Phase Bucketing
- **Type:** Deterministic Python
- **Input:** Raw roadmap text
- **Does:** Parse roadmap items (`R-###`), bucket into phases, normalize phase numbering
- **Output:** Phase buckets + roadmap item registry (JSON sidecar)
- **Gate:** Every item assigned once, no gaps, phase count >= 1

### Stage 3: Task Conversion
- **Type:** Deterministic Python
- **Input:** Phase buckets + decision record (if Stage 0 ran)
- **Does:**
  - Convert roadmap items to task stubs (`T<PP>.<TT>`)
  - **Mode A (no decision record):** Standard conversion from roadmap text
  - **Mode B (decision record present):** Tasks pre-populated with mechanical specs (file, symbol, change, before/after, verification command) from decision record. No vague language permitted.
  - Insert clarification tasks for missing info
- **Output:** Task skeletons per phase (JSON sidecar)
- **Gate:** All items converted, IDs collision-free, Mode B tasks have no unresolved "ensure/align/verify" without mechanical spec

### Stage 4: Enrichment
- **Type:** Deterministic Python
- **Input:** Task skeletons
- **Does:**
  - Existing: Effort (XS-XL), Risk (Low-High), Tier (STRICT/STANDARD/LIGHT/EXEMPT), confidence scoring
  - **New:** Complexity scoring (1-5) per task:
    - 1: Single file, no coupling
    - 2: One file/function, no state implications
    - 3: Multi-file, well-defined contract
    - 4: Shared state, resume logic, or execution ordering
    - 5: Cascading architectural decision
  - Scoring inputs: file count from decision record, dependency count, state-touching keywords, cross-step coupling
  - Flag `adversarial_review` tier based on complexity:
    - Complexity 1-2: `none` (no review)
    - Complexity 3: `inline` (lightweight inline debate)
    - Complexity 4-5: `adversarial_quick` (delegate to `/sc:adversarial --depth quick`)
  - Deliverable IDs, traceability links, verification routing
- **Output:** Fully enriched tasks (JSON sidecar)
- **Gate:** Every task has all metadata populated including complexity score and review tier

### Stage 5: File Emission
- **Type:** Deterministic Python
- **Input:** Enriched task bundle
- **Does:** Write `tasklist-index.md` + `phase-N-tasklist.md` files + JSON sidecars
- **Output:** N+1 markdown files + N+1 JSON files under `TASKLIST_ROOT`
- **Gate:** Index exists, all phase files exist, JSON sidecars exist

### Stage 6: Self-Check
- **Type:** Deterministic Python
- **Input:** Generated bundle
- **Does:** 17 structural/semantic assertions (existing spec)
- **Output:** Pass/fail
- **Gate:** All checks pass

### Stage 6.5: Complexity-Gated Review (NEW)
- **Type:** Mixed (inline Python + LLM agents for high complexity)
- **Input:** All tasks with `adversarial_review != "none"`
- **Does:**
  - **Tier `inline` (complexity 3):** Lightweight programmatic challenge:
    - Check: does the task touch files also touched by other tasks? (coupling risk)
    - Check: does the task modify shared state (state keys, config, models)?
    - Check: are input/output contracts explicitly defined?
    - If any check fails: auto-flag with warning + specific concern in task metadata
    - No LLM invocation. Pure Python heuristics based on adversarial best practices.
  - **Tier `adversarial_quick` (complexity 4-5):** Spawn adversarial debate agent:
    - Frame: "The proposed mechanical change for [task] is [summary]. Challenge failure modes, edge cases, integration conflicts."
    - 2-3 rounds max
    - Collect ACCEPT/REFACTOR verdict
    - For REFACTOR: replace task spec with adversarial alternative
  - Produce adversarial review artifact: `adversarial-review.md` + `adversarial-review.json`
- **Output:** Updated task bundle + review artifact
- **Gate:** All flagged tasks have verdict. No unresolved REFACTOR.
- **Skip condition:** `--skip-adversarial` flag

### Stage 7: Roadmap Validation (parallel agents)
- **Type:** LLM (2N parallel agents)
- **Input:** Roadmap + all phase files
- **Does:** Drift, contradiction, omission, weakened criteria, invented content checks
- **Output:** Merged findings list
- **Gate:** All agents complete, findings deduped

### Stage 8: Patch Plan Generation
- **Type:** Deterministic Python
- **Input:** Stage 7 findings
- **Does:** Generate `ValidationReport.md` + `PatchChecklist.md`
- **Output:** Validation artifacts in `TASKLIST_ROOT/validation/`
- **Gate:** Both artifacts written
- **Short-circuit:** Zero findings = clean report, skip stages 9-10

### Stage 9: Patch Execution
- **Type:** LLM (delegated)
- **Input:** PatchChecklist.md
- **Does:** Execute checklist edits
- **Output:** Patched phase files
- **Gate:** All checklist items addressed

### Stage 10: Spot-Check Verification
- **Type:** Mixed (targeted re-read + LLM verification)
- **Input:** Patched files + prior findings
- **Does:** Targeted re-check of each finding
- **Output:** Verification results appended to ValidationReport.md
- **Gate:** All findings reviewed (unresolved logged, no loop)

## 5. CLI Interface

```bash
superclaude tasklist run <roadmap-path> \
  [--spec <spec-path>] \
  [--output <output-dir>] \
  [--codebase <paths>] \
  [--skip-adversarial] \
  [--gate-mode shadow|soft|full] \
  [--resume] \
  [--dry-run] \
  [--debug]
```

| Flag | Description |
|------|-------------|
| `<roadmap-path>` | Required. Path to roadmap file. |
| `--spec` | Optional supplementary spec/context file |
| `--output` | Output directory (auto-derived from roadmap if omitted) |
| `--codebase` | Paths to read for Stage 0 decision lock. Triggers code-aware mode. |
| `--skip-adversarial` | Skip Stage 6.5 entirely |
| `--gate-mode` | Gate enforcement: shadow (log), soft (warn), full (block). Default: full |
| `--resume` | Resume from last completed stage |
| `--dry-run` | Print step plan without executing |
| `--debug` | Verbose logging |

## 6. Data Models

### Decision Record (Stage 0 output, extends DeviationRegistry)
```python
@dataclass
class DecisionRecord:
    """Extends DeviationRegistry schema with locked mechanical decisions."""
    files_read: list[str]                    # Source files analyzed
    decisions: list[Decision]                # Locked decisions
    unresolved: list[str]                    # Must be empty for gate pass
    schema_version: int = 1

@dataclass
class Decision:
    id: str                                  # D-001, D-002, ...
    category: str                            # "canonical_name", "execution_model", "data_format", etc.
    file: str                                # Target file path
    symbol: str                              # Function/class/line range
    current_state: str                       # What exists now
    target_state: str                        # What it should become
    rationale: str                           # Why this decision
```

### Complexity Score (Stage 4 enrichment extension)
```python
@dataclass
class ComplexityScore:
    score: int                               # 1-5
    file_count: int                          # Files touched
    state_touching: bool                     # Modifies shared state
    cross_step_coupling: int                 # Number of other tasks touching same files
    review_tier: str                         # "none" | "inline" | "adversarial_quick"
```

### JSON Sidecar Convention
Every `.md` artifact has a corresponding `.json` sidecar:
- `tasklist-index.json` — structured metadata, registries, traceability
- `phase-N-tasklist.json` — task objects with all enrichment fields
- `decision-record.json` — Stage 0 output
- `adversarial-review.json` — Stage 6.5 verdicts

## 7. Gate Criteria Summary

| Stage | Gate Type | Key Checks |
|-------|-----------|-----------|
| 0 | STRICT | `unresolved` list empty, all files exist, schema valid |
| 1 | STANDARD | Non-empty input, readable file |
| 2 | STANDARD | All items assigned, no gaps, phase count >= 1 |
| 3 | STRICT | IDs collision-free, Mode B no vague language |
| 4 | STANDARD | All metadata populated |
| 5 | STANDARD | File count matches, JSON sidecars present |
| 6 | STRICT | 17 self-check assertions pass |
| 6.5 | STRICT | All flagged tasks have verdict, no pending REFACTOR |
| 7 | STANDARD | All agents complete |
| 8 | STANDARD | Artifacts written (or clean short-circuit) |
| 9 | STANDARD | Checklist addressed |
| 10 | LIGHT | All findings reviewed |

## 8. Migration Plan (Hard Cutover)

1. Port generates `src/superclaude/cli/tasklist/` via cli-portify
2. Refactor into 13-stage pipeline per this spec
3. Update `src/superclaude/commands/tasklist.md` to invoke CLI pipeline instead of skill protocol
4. Delete `src/superclaude/skills/sc-tasklist-protocol/` after port is validated
5. No dual-mode. No backward compatibility shim.

## 9. Non-Functional Requirements

| NFR | Requirement |
|-----|-------------|
| NFR-1 Determinism | Stages 0-6 produce identical output for identical input (no LLM in core algorithm) |
| NFR-2 Performance | Stages 1-6 < 30s for 200-item roadmap. Stage 0 < 60s for 20 source files. |
| NFR-3 Testability | Every deterministic function independently testable. Full pipeline testable with mock runners. |
| NFR-4 Resumability | All stages support `--resume` via gate-check skip logic |
| NFR-5 Observability | Every stage emits structured log events. TUI shows progress. |

## 10. Open Questions (Resolved)

| # | Question | Resolution |
|---|----------|------------|
| 1 | Auggie MCP for code-read? | Yes — use Auggie for semantic search in Stage 0 |
| 2 | Adversarial implementation? | 3-tier: none (1-2), inline heuristic (3), sc:adversarial --depth quick (4-5) |
| 3 | Decision record format? | Extend existing DeviationRegistry schema |
| 4 | Migration path? | Hard cutover. No backward compatibility. |
