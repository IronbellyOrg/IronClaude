# BUILD REQUEST: Programmatic Tasklist Generation CLI Pipeline

## GOAL

Build `superclaude tasklist generate` as a full CLI pipeline command — the missing programmatic link between `superclaude roadmap run` (produces roadmap) and `superclaude sprint run` (executes tasklist). Currently tasklist generation is inference-only via the `/sc:tasklist` skill with zero programmatic orchestration, no gates, no retries, no state tracking. This task builds the same level of subprocess management that the roadmap pipeline has.

## WHY

The pipeline has a programmatic gap:

```
superclaude roadmap run spec.md     → roadmap.md          (programmatic, 10+ steps, gates, state)
/sc:tasklist                        → tasklist-index.md   (inference-only, no gates, no state)
superclaude tasklist validate dir/  → fidelity report     (programmatic, gates, state)
superclaude sprint run index.md     → execution results   (programmatic, phases, state)
```

Step 2 is the only part of the pipeline that can't be scripted, can't be gated, can't be retried, and can't be chained. A user must manually invoke `/sc:tasklist` in Claude Code and hope the output is correct. There's no structural validation, no retry on malformed output, and no state file for downstream consumers.

This means:
- You can't script the full roadmap → tasklist → sprint pipeline end-to-end
- Tasklist output quality is unchecked until `tasklist validate` runs separately
- The TDD/PRD enrichment we just built (`build_tasklist_generate_prompt`) has no CLI entry point — it only works during inference
- Auto-wire from `.roadmap-state.json` works for `tasklist validate` but there's no generation step that reads it

## DEPENDENCIES

This task MUST be done AFTER:
1. **PRD pipeline integration** (`TASK-RF-20260327-prd-pipeline`) — DONE. Adds `--prd-file`, `--tdd-file`, auto-wire, `build_tasklist_generate_prompt`
2. **E2E PRD pipeline tests** (`TASK-E2E-20260327-prd-pipeline-e2e`) — should be done first to confirm PRD integration works before building on top of it

## SCOPE

### CLI Layer (new code)

**`src/superclaude/cli/tasklist/commands.py`** — Add `generate` subcommand:
- `superclaude tasklist generate <ROADMAP_DIR> [OPTIONS]`
- Options: `--output`, `--tdd-file`, `--prd-file`, `--model`, `--max-turns`, `--dry-run`, `--depth [quick|standard|deep]`
- Auto-wire `--tdd-file` and `--prd-file` from `.roadmap-state.json` in `ROADMAP_DIR` (same pattern as `tasklist validate`)
- Read `roadmap.md` from `ROADMAP_DIR` as primary input

**`src/superclaude/cli/tasklist/models.py`** — Add `TasklistGenerateConfig` dataclass:
- `roadmap_file: Path` (resolved from ROADMAP_DIR)
- `output_dir: Path` (where tasklist files are written)
- `tdd_file: Path | None = None`
- `prd_file: Path | None = None`
- `model: str | None = None`
- `max_turns: int = 100`
- `dry_run: bool = False`
- `depth: Literal["quick", "standard", "deep"] = "standard"`

**`src/superclaude/cli/tasklist/executor.py`** — Add generation pipeline:
- `execute_tasklist_generate(config: TasklistGenerateConfig)` — main entry point
- `_build_generate_steps(config)` — step construction:
  - Step 1: Generate tasklist-index.md and phase files from roadmap (uses `build_tasklist_generate_prompt`)
  - Step 2: Structural validation of generated phase files (file count, naming convention, checklist format)
  - Step 3: Auto-run `tasklist validate` on the generated output (reuse existing validation pipeline)
- Each step is a `ClaudeProcess` subprocess (same pattern as roadmap executor)
- Gate validation after each step
- State file: write `.tasklist-state.json` with `roadmap_file`, `tdd_file`, `prd_file`, `generated_phases`, `validation_result`

**`src/superclaude/cli/tasklist/gates.py`** — New file or extend existing:
- `TASKLIST_GENERATE_GATE`: validates generated tasklist-index.md has YAML frontmatter, phase file references, correct structure
- `TASKLIST_PHASE_GATE`: validates each generated phase file has checklist items, follows naming convention
- `TASKLIST_STRUCTURAL_GATE`: validates the full tasklist bundle (all phases referenced in index exist, no orphans, no circular deps)

**`src/superclaude/cli/tasklist/prompts.py`** — `build_tasklist_generate_prompt` already exists. May need:
- Additional prompt for structural validation step
- Additional prompt for phase-level generation (if generation is multi-step: index first, then phases)

### Skill Layer (updates to existing)

**`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`** — Update to reference the new CLI command:
- Document `superclaude tasklist generate` as the programmatic path
- Document how it chains with `roadmap run` (reads `.roadmap-state.json`) and `sprint run` (produces tasklist-index.md)
- Document the gate system for generated tasklists
- Update the TDD/PRD enrichment sections (4.4a, 4.4b) to note they apply to both CLI generation and skill-protocol generation

**`src/superclaude/commands/spec-panel.md`** — May need update to reference tasklist generation as a downstream step

### Test Layer

**`tests/tasklist/test_generate_cli.py`** — CLI flag parsing, config wiring
**`tests/tasklist/test_generate_executor.py`** — Step construction, gate integration
**`tests/tasklist/test_generate_prompts.py`** — Prompt builder (may already exist from PRD work, extend)
**`tests/tasklist/test_generate_gates.py`** — Gate validation logic

### Integration

The end state should enable this full scripted pipeline:

```bash
# Generate roadmap from TDD+PRD
uv run superclaude roadmap run tdd.md --prd-file prd.md --output ./release-v1/

# Generate tasklist from roadmap (auto-wires TDD+PRD from state)
uv run superclaude tasklist generate ./release-v1/

# Validate the generated tasklist
uv run superclaude tasklist validate ./release-v1/

# Execute the sprint
uv run superclaude sprint run ./release-v1/tasklist-index.md
```

No manual `/sc:tasklist` step. No inference gap. Full programmatic chain.

## DESIGN CONSIDERATIONS

1. **Single-step vs multi-step generation**: The roadmap pipeline generates two variants and merges them (adversarial). Should tasklist generation do the same? Or is a single generation pass sufficient with validation as the quality gate?

2. **Phase-by-phase generation**: Should the pipeline generate tasklist-index.md first, then generate each phase file in a separate subprocess? This would allow per-phase gates and retries. Or generate everything in one pass?

3. **Gate strictness**: What constitutes a valid generated tasklist? At minimum: index file exists, references N phase files, all phase files exist, each phase file has checklist items. Should it also validate item format (B2 self-contained pattern)?

4. **Retry strategy**: If generation produces malformed output, how many retries? The roadmap pipeline uses 2 retries per step. Same here?

5. **State file chaining**: `.roadmap-state.json` → read by `tasklist generate` → writes `.tasklist-state.json` → read by `sprint run`? Or extend `.roadmap-state.json` with tasklist state?

6. **Depth levels**: `quick` = minimal tasklist (fewer phases, coarser items), `standard` = full tasklist, `deep` = detailed tasklist with sub-items and verification criteria per item?

## TEMPLATE

02 (complex — new CLI command, executor, gates, state management, multi-file output, integration testing)

## CONTEXT FILES

| File | Why |
|------|-----|
| `src/superclaude/cli/roadmap/executor.py` | **Pattern reference** — the roadmap executor is the gold standard for how to build a CLI pipeline with steps, gates, state, and retries |
| `src/superclaude/cli/roadmap/commands.py` | **Pattern reference** — Click command structure with `--tdd-file`, `--prd-file`, auto-wire |
| `src/superclaude/cli/tasklist/commands.py` | **Extend** — add `generate` subcommand alongside existing `validate` |
| `src/superclaude/cli/tasklist/executor.py` | **Extend** — add generation pipeline alongside existing validation pipeline |
| `src/superclaude/cli/tasklist/prompts.py` | **Extend** — `build_tasklist_generate_prompt` already exists, may need additional prompts |
| `src/superclaude/cli/tasklist/models.py` | **Extend** — add `TasklistGenerateConfig` alongside `TasklistValidateConfig` |
| `src/superclaude/cli/roadmap/gates.py` | **Pattern reference** — gate definition structure |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | **Update** — document CLI generation path |
| `.dev/tasks/to-do/TASK-RF-20260327-prd-pipeline/phase-outputs/reports/final-integration-report.md` | **Context** — what PRD integration implemented (especially `build_tasklist_generate_prompt`) |

## ESTIMATED SCOPE

| Category | Files | Lines (est.) |
|----------|-------|-------------|
| Commands | `tasklist/commands.py` | ~40 |
| Models | `tasklist/models.py` | ~20 |
| Executor | `tasklist/executor.py` | ~200-300 |
| Gates | `tasklist/gates.py` (new) | ~80-120 |
| Prompts | `tasklist/prompts.py` | ~30-50 (additional validation prompts) |
| Skills | `SKILL.md` | ~50 |
| Tests | `tests/tasklist/` | ~200-300 |
| **Total** | **~7-8 files** | **~620-880 lines** |
