# Research: Baseline Pipeline Capabilities

- **Researcher**: Integration Points (Baseline Pipeline Capabilities)
- **Status**: Complete
- **Scope**: `src/superclaude/cli/roadmap/` at master commit `4e0c621` vs current branch `feat/tdd-spec-merge`
- **Date**: 2026-04-02

## Objective

Determine what pipeline steps, CLI flags, and artifacts exist in the baseline (master) vs what was added on the current branch. This informs E2E Test 3 expectations.

---

## 1. Baseline CLI Flags (master `4e0c621`)

The `superclaude roadmap run` command at baseline accepts:

| Flag | Type | Default | Present in Baseline? |
|------|------|---------|---------------------|
| `SPEC_FILE` (positional) | `Path` (single file) | required | YES |
| `--agents` | `str` (comma-sep) | `opus:architect,haiku:architect` | YES |
| `--output` | `Path` | spec_file.parent | YES |
| `--depth` | `Choice[quick,standard,deep]` | `standard` | YES |
| `--resume` | flag | false | YES |
| `--dry-run` | flag | false | YES |
| `--model` | `str` | `""` | YES |
| `--max-turns` | `int` | 100 | YES |
| `--debug` | flag | false | YES |
| `--no-validate` | flag | false | YES |
| `--allow-regeneration` | flag | false | YES |
| `--retrospective` | `Path` | None | YES |
| `--input-type` | `Choice[auto,tdd,spec,prd]` | - | **NO** (added on branch) |
| `--tdd-file` | `Path` | - | **NO** (added on branch) |
| `--prd-file` | `Path` | - | **NO** (added on branch) |

### Key Difference: Positional Argument

- **Baseline**: `SPEC_FILE` -- single required positional `click.Path(exists=True)`
- **Branch**: `INPUT_FILES` -- variadic `nargs=-1, required=True` accepting 1-3 files

This means E2E Test 3 (baseline) invocation is:
```bash
superclaude roadmap run spec.md --output ./output
```
NOT:
```bash
superclaude roadmap run spec.md tdd.md --input-type auto  # branch syntax
```

## 2. Baseline Pipeline Steps (master `4e0c621`)

The baseline `_build_steps()` docstring says "9-step pipeline" but actually produces 11 step IDs (including `remediate` and `certify` which are conditionally built). Here is the complete step sequence:

| # | Step ID | LLM? | Output File | Gate |
|---|---------|------|-------------|------|
| 1 | `extract` | Yes | `extraction.md` | `EXTRACT_GATE` |
| 2a | `generate-{agent_a.id}` | Yes | `roadmap-{agent_a.id}.md` | `GENERATE_A_GATE` |
| 2b | `generate-{agent_b.id}` | Yes (parallel with 2a) | `roadmap-{agent_b.id}.md` | `GENERATE_B_GATE` |
| 3 | `diff` | Yes | `diff-analysis.md` | `DIFF_GATE` |
| 4 | `debate` | Yes | `debate-transcript.md` | `DEBATE_GATE` |
| 5 | `score` | Yes | `base-selection.md` | `SCORE_GATE` |
| 6 | `merge` | Yes | `roadmap.md` | `MERGE_GATE` |
| 7 | `anti-instinct` | **No** (deterministic Python) | `anti-instinct-audit.md` | `ANTI_INSTINCT_GATE` |
| 8 | `test-strategy` | Yes | `test-strategy.md` | `TEST_STRATEGY_GATE` |
| 9 | `spec-fidelity` | Yes | `spec-fidelity.md` | `SPEC_FIDELITY_GATE` |
| 10 | `wiring-verification` | **No** (deterministic, trailing gate) | `wiring-verification.md` | `WIRING_GATE` |
| 11* | `remediate` | Conditional | `remediation-tasklist.md` | `REMEDIATE_GATE` |
| 12* | `certify` | Conditional | `certification-report.md` | `CERTIFY_GATE` |

*Steps 11-12 are conditionally appended based on spec-fidelity findings.

### Step IDs from `_get_all_step_ids()` (baseline):
```
extract, generate-{a}, generate-{b}, diff, debate, score, merge,
anti-instinct, test-strategy, spec-fidelity, wiring-verification,
remediate, certify
```

## 3. Key Questions Answered

### Does baseline have `--output` flag?
**YES** -- `--output` / `output_dir` option. Defaults to `spec_file.parent`.

### Does baseline have `--input-type` flag?
**NO** -- Added on branch. Baseline takes a single `SPEC_FILE` positional arg.

### Does baseline have `spec-fidelity` step?
**YES** -- Step 9 in the pipeline. Uses `SPEC_FIDELITY_GATE`. Can optionally use convergence engine when `config.convergence_enabled=True`.

### Does baseline have `wiring-verification` step?
**YES** -- Step 10 in the pipeline. Uses `WIRING_GATE` from `audit.wiring_gate`. Runs in `GateMode.TRAILING` (shadow/advisory mode). Deterministic (no LLM).

### Does baseline have `deviation-analysis` step?
**YES in gates.py** -- `DEVIATION_ANALYSIS_GATE` is defined in baseline `gates.py`. However, it is NOT a separate pipeline step in `_build_steps()`. The deviation analysis capability is embedded within the `spec-fidelity` convergence path (`_run_convergence_spec_fidelity`), not as an independent pipeline step.

### What fidelity prompt language does baseline use?
**"You are a specification fidelity analyst."** -- Confirmed at line 326 of baseline `prompts.py`:
```python
"You are a specification fidelity analyst.\n\n"
```

## 4. Baseline Gates Defined (master `4e0c621`)

All gates present in baseline `gates.py`:
- `EXTRACT_GATE`
- `GENERATE_A_GATE`, `GENERATE_B_GATE`
- `DIFF_GATE`
- `DEBATE_GATE`
- `SCORE_GATE`
- `MERGE_GATE`
- `ANTI_INSTINCT_GATE`
- `TEST_STRATEGY_GATE`
- `SPEC_FIDELITY_GATE`
- `WIRING_GATE` (imported from `audit.wiring_gate`)
- `DEVIATION_ANALYSIS_GATE`
- `REMEDIATE_GATE`
- `CERTIFY_GATE`

### New gate added on branch:
- `EXTRACT_TDD_GATE` -- TDD-specific extraction gate with 6 extra frontmatter fields

## 5. Baseline Artifacts Produced

For a standard run (no convergence, no failures requiring remediation), the baseline produces:

### Primary artifacts:
1. `extraction.md` -- requirement extraction from spec
2. `roadmap-opus-architect.md` -- variant A roadmap
3. `roadmap-haiku-architect.md` -- variant B roadmap
4. `diff-analysis.md` -- structural diff between variants
5. `debate-transcript.md` -- adversarial debate
6. `base-selection.md` -- scored base selection
7. `roadmap.md` -- merged final roadmap
8. `anti-instinct-audit.md` -- deterministic obligation/contract/fingerprint audit
9. `test-strategy.md` -- test strategy
10. `spec-fidelity.md` -- fidelity analysis report
11. `wiring-verification.md` -- component wiring verification

### Conditional artifacts (only if spec-fidelity finds HIGH issues):
12. `remediation-tasklist.md` -- remediation tasks
13. `certification-report.md` -- post-remediation certification
14. `deviation-registry.json` -- convergence engine state (only if convergence enabled)

### State file:
15. `.roadmap-state.json` -- pipeline state for `--resume`

## 6. Baseline RoadmapConfig Model (master `4e0c621`)

```python
@dataclass
class RoadmapConfig(PipelineConfig):
    spec_file: Path
    agents: list[AgentSpec]  # default: [opus:architect, haiku:architect]
    depth: Literal["quick", "standard", "deep"] = "standard"
    output_dir: Path
    retrospective_file: Path | None = None
    convergence_enabled: bool = False
    allow_regeneration: bool = False
```

### Fields added on branch:
```python
    input_type: Literal["auto", "tdd", "spec", "prd"] = "auto"
    tdd_file: Path | None = None
    prd_file: Path | None = None
```

## 7. Changes on Branch (6 commits)

Commits modifying `src/superclaude/cli/roadmap/` since master:
```
b942d50 feat: enhance roadmap executor, task skill, and test coverage
a74cb83 feat: add tech-reference skill, auto-detection task, E2E fixes
96ca649 merge: integrate remote changes + add templates and updated RF agents
a9cf7ee feat: add --prd-file supplementary input to roadmap and tasklist pipelines
8eda3ce CLI Patche with some fixes and doc reorg
c5a874e refactor(cli): resolve unwired components P1-P4 with gate enforcement and audit cleanup
```

Key additions on branch:
1. **Multi-file positional input** (`INPUT_FILES` nargs=-1 replaces single `SPEC_FILE`)
2. **`--input-type` flag** (auto/tdd/spec/prd)
3. **`--tdd-file` and `--prd-file` flags**
4. **`_route_input_files()` function** in executor -- auto-detection and routing logic
5. **`detect_input_type()` function** in executor -- weighted signal detection for PRD/TDD/spec
6. **`EXTRACT_TDD_GATE`** -- TDD-specific extraction gate
7. **`build_extract_prompt_tdd()`** prompt builder
8. **User feedback echo** showing resolved routing in commands.py
9. **TDD compatibility warnings** for deviation-analysis step

## 8. Implications for E2E Test 3

### Baseline invocation syntax:
```bash
superclaude roadmap run <spec.md> --output <output-dir> [--dry-run]
```

### Expected baseline output count:
- **Minimum 11 artifacts** (standard run, no remediation needed)
- **Up to 15 artifacts** (if spec-fidelity triggers remediation + certification)

### Flags NOT available in baseline:
- `--input-type` -- do not pass
- `--tdd-file` -- do not pass
- `--prd-file` -- do not pass
- Multi-file positional args -- pass exactly ONE spec file

### Comparison points for Test 2 vs Test 3:
- Test 2 (branch) can pass TDD/PRD files; Test 3 (baseline) cannot
- Both should produce the same core 11 artifact files
- Both use `SPEC_FIDELITY_GATE` and "specification fidelity analyst" prompt language
- Both have `wiring-verification` as a trailing gate step
- Baseline has no `EXTRACT_TDD_GATE`; only `EXTRACT_GATE`

---

*Research complete. All key questions answered with evidence from git diff/show commands.*
