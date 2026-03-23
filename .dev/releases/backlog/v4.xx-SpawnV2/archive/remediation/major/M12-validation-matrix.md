# M12 Remediation Proposal — Expanded Validation Matrix for `/sc:spawn`

## Goal

Replace the current 2-item manual checklist with a validation matrix that exercises the command surface area implied by the spec: Standard Mode, Pipeline Mode, BranchNMerge dynamic expansion, error handling, and resume behavior.

## Validation Scope

This matrix covers:
- Standard Mode flags: `--dry-run`, `--no-delegate`, `--strategy`, `--depth`, `--resume`
- Pipeline Mode flags: `--pipeline`, `--pipeline-seq`, `--pipeline-resume`, `--prompt`, `--agents`
- Dynamic phase types: `generate-parallel`, `compare-merge`
- Error paths called out in review findings and boundary analysis
- Resume behavior for both Serena checkpoints and pipeline manifests

## Assumptions / Test Fixtures

Use the following test assets during manual validation:
- A small repo or sandbox task that is safe to plan against
- A valid linear pipeline YAML fixture
- A valid BranchNMerge YAML fixture
- An invalid cyclic pipeline YAML fixture
- A writable output directory for manifests/artifacts
- A prior interrupted run for resume scenarios

Where the spec is still ambiguous, pass criteria below are written to force the intended contract to become explicit.

---

## Expanded Validation Matrix

### Standard Mode

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| S01 | Standard dry-run baseline | `/sc:spawn "audit auth flow" --dry-run` | Enters Standard Mode, performs decomposition/planning preview, does not create tasks or delegate work. | Output clearly shows preview/plan-only behavior; no spawned tasks; no side effects beyond preview artifacts/logging. |
| S02 | Plan-only without delegation | `/sc:spawn "audit auth flow" --no-delegate` | Produces hierarchy/plan in Standard Mode without delegating to sub-agents. | Task hierarchy is produced; no delegation occurs; result is explicitly marked as plan-only. |
| S03 | Dry-run plus no-delegate | `/sc:spawn "audit auth flow" --dry-run --no-delegate` | Safest preview path; should show decomposition intent without execution. | No task creation, no delegation, and no execution side effects; output reflects combined preview semantics without contradiction. |
| S04 | Strategy override: wave | `/sc:spawn "migrate legacy auth" --strategy wave --dry-run` | Uses wave coordination path instead of adaptive default. | Output/preview explicitly reflects wave-based grouping or staged orchestration rather than default adaptive behavior. |
| S05 | Depth shallow | `/sc:spawn "stabilize CI pipeline" --depth shallow --dry-run` | Produces coarse decomposition with limited granularity. | Preview shows fewer/larger work units than deep mode; no evidence of deep decomposition detail. |
| S06 | Depth deep | `/sc:spawn "stabilize CI pipeline" --depth deep --dry-run` | Produces more granular decomposition and richer planning detail. | Preview is materially more detailed than shallow mode; deeper hierarchy or more phases/tasks are visible. |
| S07 | Resume from Serena checkpoint | `/sc:spawn "continue migration" --resume` | Reads saved checkpoint and resumes from last incomplete Standard-Mode boundary. | Prior completed work is not re-run; resumed output identifies continuation point; resumed plan/execution proceeds from first incomplete checkpointed stage. |
| S08 | Both task description and pipeline provided | `/sc:spawn "legacy text prompt" --pipeline "analyze -> test" --dry-run` | Must follow the defined precedence rule: pipeline mode wins, and task description is either ignored or treated as prompt per remediation decision. | Behavior is deterministic and documented in output; no ambiguous mixed-mode execution; the precedence rule is observable and repeatable. |

### Pipeline Mode

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| P01 | Inline pipeline shorthand baseline | `/sc:spawn --pipeline "analyze -> design | implement -> test" --dry-run` | Parses inline DAG correctly, preserving serial and parallel relationships. | Preview shows analyze first, design+implement parallel second, test last; no parse errors. |
| P02 | Pipeline from YAML file | `/sc:spawn --pipeline @/ABS/PATH/pipeline-valid.yaml --dry-run` | Loads DAG from YAML and previews executable phases. | YAML is accepted; phases and dependencies match fixture definition; preview is structurally correct. |
| P03 | Force sequential pipeline execution | `/sc:spawn --pipeline "analyze -> design | implement -> test" --pipeline-seq --dry-run` | Converts or schedules the pipeline as sequential execution despite parallel-capable structure. | Preview/execution order shows no parallel dispatch; all phases are serialized deterministically. |
| P04 | Pipeline prompt injection | `/sc:spawn --pipeline "analyze -> test" --prompt "Focus on auth regressions" --dry-run` | Prompt text is propagated to pipeline phases according to spec. | Preview or generated phase commands visibly include the supplied prompt exactly once in the intended place. |
| P05 | Pipeline resume from manifest | `/sc:spawn --pipeline @/ABS/PATH/pipeline-valid.yaml --pipeline-resume` | Reads manifest, skips completed phases, resumes from first incomplete phase. | Manifest is loaded; completed phases are skipped rather than repeated; resumed phase is the first incomplete one. |
| P06 | Pipeline YAML with parallel fan-out and join | `/sc:spawn --pipeline @/ABS/PATH/pipeline-parallel-join.yaml --dry-run` | Preserves many-to-one dependency structure through preview. | Output shows fan-out phases blocked on the predecessor and join phase blocked on all required inputs. |

### BranchNMerge / Dynamic Expansion

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| B01 | BranchNMerge with 2 agents | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents opus:architect,haiku:analyzer --prompt "compare remediation options" --dry-run` | Expands `generate-parallel` into 2 concrete agent phases, then routes outputs to merge. | Preview shows exactly 2 generated phases; downstream compare/merge phase expects 2 artifacts. |
| B02 | BranchNMerge with 3 agents | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents opus:architect,sonnet:backend,haiku:qa --prompt "compare remediation options" --dry-run` | Expands to 3 concrete agent branches and one merge path. | Preview shows exactly 3 generated phases; merge stage consumes all 3 outputs. |
| B03 | BranchNMerge with 10+ agents / batching | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents a1:architect,a2:architect,a3:architect,a4:architect,a5:architect,a6:architect,a7:architect,a8:architect,a9:architect,a10:architect,a11:architect --prompt "stress test fanout" --dry-run` | Applies concurrency cap behavior to oversized parallel group. | Preview or execution plan shows sub-batching/splitting at the defined cap instead of a single oversubscribed dispatch group. |
| B04 | Agent spec with persona and instruction | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents 'opus:architect:"focus on migration risk"',haiku:qa --prompt "compare remediation options" --dry-run` | Parser accepts full `model[:persona[:"instruction"]]` shape and preserves embedded instruction. | Expanded branch definition preserves model, persona, and custom instruction without mangling quotes or truncating fields. |
| B05 | Compare-merge artifact routing | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents opus:architect,haiku:analyzer,sonnet:backend --prompt "merge best plan"` | Collects branch outputs and runs merge/comparison stage with all expected artifacts surfaced or locatable. | Merge completes; merged output path is exposed; supplementary artifacts are discoverable via manifest/output directory contract. |

### Error Paths

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| E01 | Missing task description in Standard Mode | `/sc:spawn --dry-run` | Stops immediately because neither task description nor pipeline was provided. | Command fails fast with explicit actionable error; no planning, no task creation, no hidden default behavior. |
| E02 | Invalid empty `--agents` value | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents "" --prompt "x" --dry-run` | Rejects empty parsed agent set rather than continuing with zero branches. | Clear validation error states that at least one valid agent spec is required; no phase expansion occurs. |
| E03 | Invalid malformed agent spec | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents "not:a:valid:spec:extra" --prompt "x" --dry-run` | Rejects malformed agent grammar. | Error message identifies invalid spec format and points to accepted grammar; no partial execution. |
| E04 | Missing `--agents` for generate-parallel pipeline | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --prompt "x" --dry-run` | Stops because dynamic parallel generation lacks required agent definitions. | Clear validation error mentions missing `--agents`; no fallback to empty/default agent list. |
| E05 | Cyclic YAML pipeline | `/sc:spawn --pipeline @/ABS/PATH/pipeline-cycle.yaml --dry-run` | Detects cycle and refuses execution. | Cycle is detected before dispatch; error identifies dependency cycle or invalid DAG; nothing runs. |
| E06 | Compare-merge with fewer than 2 artifacts | `/sc:spawn --pipeline @/ABS/PATH/BranchNMerge.yaml --agents haiku:analyzer --prompt "x" --dry-run` | Expansion may produce one branch, but compare/merge must stop because merge requires at least 2 inputs. | Validation/preflight clearly states merge requires >=2 artifacts; no invalid merge stage execution. |
| E07 | Missing pipeline file | `/sc:spawn --pipeline @/ABS/PATH/does-not-exist.yaml --dry-run` | Fails with file resolution/loading error. | Error explicitly names missing file path; no fallback or misleading parse failure. |

### Resume / Recovery

| ID | Scenario | Invocation | Expected behavior | Pass criteria |
|---|---|---|---|---|
| R01 | Standard resume after interrupted run | Step 1: run a long Standard Mode orchestration and interrupt after checkpoint. Step 2: `/sc:spawn "continue migration" --resume` | Resumes Standard Mode from latest checkpoint boundary without redoing completed work. | Previously completed wave/group is not repeated; resumed output references recovered checkpoint state. |
| R02 | Pipeline resume after partial completion | Step 1: run pipeline until one later phase remains incomplete. Step 2: `/sc:spawn --pipeline @/ABS/PATH/pipeline-valid.yaml --pipeline-resume` | Loads manifest and restarts from first incomplete phase only. | Completed phases remain marked completed; only pending/failed incomplete work is re-entered. |
| R03 | Resume with no checkpoint available | `/sc:spawn "continue migration" --resume` in a clean environment | Fails cleanly or reports that no resumable checkpoint exists. | User receives explicit "no checkpoint/manifest found" guidance; command does not invent state or silently start a fresh unrelated run. |
| R04 | Resume preserves output/manifest continuity | Resume a previously interrupted pipeline run using the same output location. | Resumed run appends/updates the existing manifest rather than replacing history incoherently. | Manifest remains internally consistent, phase statuses are preserved, and new completion timestamps/results continue the same pipeline record. |

---

## Recommended Replacement Checklist Text

Replace the current migration checklist validation section with a requirement like:

- [ ] Execute and record the M12 validation matrix covering Standard Mode, Pipeline Mode, BranchNMerge, error handling, and resume behavior (minimum 20 scenarios: S01-S08, P01-P06, B01-B05, E01-E07, R01-R04 as applicable to implemented scope)
- [ ] Confirm every flag in the options table is exercised by at least one validation scenario
- [ ] Confirm every documented STOP/error condition is exercised by at least one negative-path scenario
- [ ] Confirm both resume mechanisms (`--resume`, `--pipeline-resume`) are validated against real interrupted state

## Coverage Crosswalk

| Surface area | Covered by |
|---|---|
| `--dry-run` | S01, S03, S04, S05, S06, P01, P02, P03, P04, B01, B02, B03, E01-E07 |
| `--no-delegate` | S02, S03 |
| `--strategy` | S04 |
| `--depth` | S05, S06, B01-B03 |
| `--resume` | S07, R01, R03 |
| `--pipeline` | S08, P01-P06, B01-B05, E02-E07, R02, R04 |
| `--agents` | B01-B05, E02-E04, E06 |
| `--prompt` | P04, B01-B05, E02-E06 |
| `--pipeline-seq` | P03 |
| `--pipeline-resume` | P05, R02, R04 |
| Standard Mode | S01-S08 |
| Pipeline Mode | P01-P06 |
| BranchNMerge | B01-B05 |
| Error handling | E01-E07 |
| Resume/recovery | R01-R04 |

## Exit Criteria

M12 should be considered resolved only when:
1. The migration checklist references an expanded validation matrix, not 2 ad hoc commands.
2. The implemented/manual test evidence demonstrates coverage across all major execution families.
3. At least one scenario validates each documented flag and each documented failure boundary.
4. Resume behavior is validated using real interrupted state, not only dry-run previews.
5. BranchNMerge is validated at normal scale and concurrency-cap scale.
