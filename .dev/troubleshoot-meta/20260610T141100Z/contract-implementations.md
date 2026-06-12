# Contract implementations: PRD saga gate/evaluator map

## Scope

Role: A2 contract cartographer. Dataset is the PRD troubleshoot/debug saga; this file intentionally does not modify product, skill, or source code.

Primary contracts examined:

- `SemanticCheck`: content predicate contract, `Callable[[str], bool | str]`, with optional `advisory` bit.
- `GateCriteria`: gate data contract: required frontmatter, min lines, tier, semantic checks, code assertions.
- Gate evaluator/runtime contract: turn a step artifact/content plus `GateCriteria` into pass/fail and decide whether to halt.
- Trailing gate contract: evaluate gates asynchronously/off-path and report failures without blocking the main path.

## Executive finding

The PRD runtime does **not** call the generic `pipeline/gates.py:gate_passed()` evaluator or `pipeline/trailing_gate.py:TrailingGateRunner` for its normal `superclaude prd run` path. It calls the bespoke PRD evaluator `src/superclaude/cli/prd/executor.py:PrdExecutor._evaluate_gate()` after resolving disk artifact content.

That matters because PR #155 made `parallel_instructions` advisory in the `SemanticCheck` data model and made the generic `gate_passed()` honor `check.advisory`, but the actual PRD runtime evaluator still iterates `gate.semantic_checks` and returns `False` on any non-`True` result without checking `advisory`. This is the likely meta-pipeline escape: the fix was applied to an off-path evaluator, while the runtime entrypoint uses another implementation of the same contract.

## Runtime entrypoint and actual call chain

| Step | Evidence | Contract implication |
|---|---|---|
| CLI command constructs `PrdExecutor` | `/config/workspace/IronClaude/src/superclaude/cli/prd/commands.py:112-141` imports `PrdExecutor`, constructs it, and calls `executor.run()` for `superclaude prd run`. | The PRD CLI is not using `execute_pipeline()` from the generic pipeline package. |
| `PrdExecutor.run()` drives Stage A | `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:500-551` creates task dirs, registers steps, then calls `self._execute_step(...)` for each Stage A step. | Runtime step execution is bespoke to PRD. |
| Gate content and gate criteria are resolved inside `_execute_step` | `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:741-764` resolves `gate_content` from disk and obtains `gate = GATE_CRITERIA.get(step_id)`. | PRD gates are data from `prd/gates.py`, but evaluation is not delegated to `pipeline.gates.gate_passed`. |
| Actual PRD gate call | `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:761-778` calls `self._evaluate_gate(step_id, gate, gate_content)`. | This is the PRD runtime gate evaluator. |
| PRD halt behavior | `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:765-770` marks `STRICT` failures as `HALT`; non-STRICT failures as `VALIDATION_FAIL`. `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:572-589` halts on hard failures or STRICT gate failures. | A false fail from a STRICT PRD gate halts the run. |

## Implementation inventory

### 1. Data contracts: `SemanticCheck` and `GateCriteria`

| Implementation | Path | What it implements | Evidence | Runtime for PRD? |
|---|---|---|---|---|
| `SemanticCheck` dataclass | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:81-94` | Content-only check with `name`, `check_fn`, `failure_message`, and `advisory: bool = False`. Docstring says advisory checks warn and never fail the gate. | Lines 81-94. | Yes as data: PRD gates import and instantiate this class. |
| `GateCriteria` dataclass | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/models.py:138-160` | Required frontmatter, min lines, enforcement tier, semantic checks, code assertions. Docstring says code assertions dispatched by `pipeline/gates.py:gate_passed` after semantic checks. | Lines 138-160. | Yes as data: PRD `GATE_CRITERIA` uses it. Code assertions are not used in PRD gates observed here. |

Contract discrepancy: the `SemanticCheck.advisory` docstring is evaluator-dependent. It is true for generic `gate_passed()` but not for PRD `_evaluate_gate()`.

### 2. Generic blocking gate evaluator: `pipeline/gates.py:gate_passed`

| Implementation | Path | Behavior | Evidence | Runtime for PRD? |
|---|---|---|---|---|
| `gate_passed(output_file, criteria, *, envelope=None, repo_root=None)` | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:23-140` | Tiered file gate: EXEMPT pass; LIGHT file exists/non-empty; STANDARD adds min lines/frontmatter; STRICT adds semantic checks; code assertions optionally after semantic checks. | Lines 23-88 for tier flow; lines 89-110 for semantic loop; lines 112-140 for code assertions. | No for normal PRD runtime. Used by generic pipeline consumers. |
| Advisory handling in generic evaluator | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:89-110` | If a semantic check fails and `getattr(check, "advisory", False)` is true, logs warning and continues instead of returning failure. | Lines 91-106. | Off-path for PRD runtime. |
| Frontmatter sub-check | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py:143-182` | Uses canonical frontmatter parser and checks exact keys or tuple OR-groups. | Lines 143-182. | Not called by PRD `_evaluate_gate()`; PRD evaluator only checks min lines and semantic checks. |

Consumers found:

- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:63-88` documents that generic `execute_pipeline()` calls `gate_passed()` for each step.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:191-239` starts single-step execution; subsequent gate handling uses `gate_passed()` and remediation paths.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py:115-156` defaults its `gate_check` parameter to `gate_passed`.
- Roadmap/tasklist/validate runners call `execute_pipeline()` (`grep` evidence: `roadmap/executor.py`, `roadmap/validate_executor.py`, `tasklist/executor.py`), but PRD does not.

### 3. PRD runtime gate evaluator: `prd/executor.py:PrdExecutor._evaluate_gate`

| Implementation | Path | Behavior | Evidence | Runtime for PRD? |
|---|---|---|---|---|
| `_evaluate_gate(step_id, gate, content) -> bool` | `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:825-862` | Checks min lines against already-resolved content, then iterates `gate.semantic_checks`; records/logs first failure; returns `False`; otherwise returns `True`. | Lines 833-862. | Yes. This is the actual PRD runtime evaluator. |
| No frontmatter enforcement in PRD evaluator | Same path, lines 833-862 | The body has min-lines and semantic-check loops only; no `required_frontmatter_fields` check is present. | Lines 833-862. | Yes; PRD frontmatter criteria in `GATE_CRITERIA` are not enforced by this evaluator. |
| No advisory handling in PRD evaluator | Same path, lines 849-859 | The semantic loop converts any non-`True` result to `msg`, records/logs it, and returns `False`; there is no `check.advisory` branch. | Lines 849-859. | Yes; this is the key mismatch with PR #155 intent. |

### 4. Trailing/off-path evaluator: `pipeline/trailing_gate.py`

| Implementation | Path | Behavior | Evidence | Runtime for PRD? |
|---|---|---|---|---|
| `TrailingGateRunner.submit(step, gate_check=gate_passed)` | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py:115-187` | Spawns a daemon thread. If no gate, queues pass. Otherwise prefers `.compressed.md` sidecar, calls `gate_check(target, step.gate)`, and queues `TrailingGateResult`. | Lines 115-187. | No for PRD runtime. |
| `TrailingGatePolicy` protocol | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py:241-274` | Consumer-owned hooks for remediation step construction and file-change tracking. | Lines 241-274. | No PRD usage found. |
| Remediation prompt builder | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py:282-346` | Builds a focused prompt from gate failure reason, gate criteria, semantic check names, and paths. | Lines 282-346. | No PRD usage found. |
| Generic executor sync point | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:99-103` creates runner when `grace_period > 0`; `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:175-187` waits and logs failures. | Used by generic pipeline, not PRD. | No for PRD runtime. |

### 5. Cosmetic remediation semantic dispatch in generic executor

| Implementation | Path | Behavior | Evidence | Runtime for PRD? |
|---|---|---|---|---|
| First-failing semantic check finder | `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:299-329` | Reads gate target, runs each `sc.check_fn(...)` directly to identify a failing semantic check for cosmetic remediation, then re-checks via `gate_passed`. | Lines 299-329. | No for PRD runtime. This is another independent semantic-check loop that should be included in unmask-and-sweep thinking. |

### 6. PRD gate criteria and semantic check implementations

All PRD semantic check functions live in `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py` and are wrapped by `_make_semantic_check(...)` unless noted.

| Check / helper | Path | Contract | Evidence |
|---|---|---|---|
| `_check_verdict_field` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:37-62` | Accept JSON or markdown verdict field with PASS/FAIL. | Lines 37-62. |
| `_check_no_placeholders` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:65-84` | Reject TODO/TBD/PLACEHOLDER/[INSERT]/[FILL]. | Lines 65-84. |
| `_check_no_truncation_marker` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:87-90` | Reject `[TRUNCATED` or trailing ellipsis. | Lines 87-90. Note: present but not wired into observed `GATE_CRITERIA` lines 353-569. |
| `_check_parsed_request_fields` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:98-114` | Require GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO. | Lines 98-114. |
| `_check_research_notes_sections` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:128-141` | Require seven research-note sections. | Lines 128-141. |
| `_check_suggested_phases_detail` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:144-161` | Require detail items under Suggested Phases. | Lines 144-161. |
| `_check_task_phases_present` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:164-174` | Require at least two phase headings. | Lines 164-174. |
| `_check_b2_self_contained` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:177-194` | Reject external-reference phrases in checklist items. | Lines 177-194. |
| `_check_parallel_instructions` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:197-264` | Require phase >=2 sections to include parallel/concurrent/simultaneously/batch, except final sequential completion/presentation phase. | Lines 197-264. |
| `_check_prd_template_sections` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:276-288` | Require critical PRD sections. | Lines 276-288. |
| `_check_qa_verdict` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:291-293` | Delegate to verdict-field check. | Lines 291-293. |
| `_safe_check` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:301-312` | Convert exceptions into error strings. | Lines 301-312. |
| `_make_semantic_check` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:315-331` | Wrap check in `_safe_check` and set `advisory`. | Lines 315-331. |
| `GATE_CRITERIA` | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:353-569` | Maps step IDs to `GateCriteria`. | Lines 353-569. |
| `build-task-file.parallel_instructions` advisory wiring | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:416-448` | Sets `parallel_instructions` advisory=True; other build-task-file checks remain halting. | Lines 416-448. Test lock at `/config/workspace/IronClaude/tests/cli/prd/test_gates.py:351-365`. |

PRD gate table summary:

| Step | Tier | Runtime checks actually enforced by PRD `_evaluate_gate` | Notes |
|---|---:|---|---|
| check-existing | EXEMPT | min_lines only if >0; no semantic checks | Since min_lines=0 and no semantic checks, passes if status is success. |
| parse-request | STRICT | `parsed_request_fields` | No frontmatter check. |
| scope-discovery | STANDARD | min_lines 50 | Nonfatal `VALIDATION_FAIL`; warn may fire when specs were bound. |
| research-notes | STRICT | min_lines 100; `research_notes_sections`; `suggested_phases_detail` | Required frontmatter fields are declared but not enforced by PRD evaluator. |
| sufficiency-review | STRICT | `verdict_field` | No min lines. |
| template-triage | EXEMPT | none | Passes if status success. |
| build-task-file | STRICT | min_lines 400; `task_phases_present`; `b2_self_contained`; `parallel_instructions` | `parallel_instructions` is data-marked advisory but PRD runtime still treats non-True as failure. |
| verify-task-file | STRICT | `verdict_field` | No min lines. |
| preparation | LIGHT | none | PRD evaluator does not implement generic LIGHT file/non-empty behavior. |
| investigation | STANDARD | min_lines 50 | Dynamic Stage B uses same `_execute_step`/`_evaluate_gate` path. |
| research-qa | STRICT | min_lines 20; `qa_verdict` | Disk QA report selected via `_STEP_ARTIFACT_FILES`. |
| web-research | STANDARD | min_lines 30 | Nonfatal validation fail. |
| synthesis | STANDARD | min_lines 80 | Nonfatal validation fail. |
| synthesis-qa | STRICT | min_lines 20; `qa_verdict` | Strict. |
| assembly | STRICT | min_lines 800; `prd_template_sections`; `no_placeholders` | Required frontmatter declared but not enforced by PRD evaluator. |
| structural-qa | STRICT | min_lines 20; `qa_verdict` | Strict. |
| qualitative-qa | STRICT | min_lines 20; `qa_verdict` | Strict. |
| present-complete | LIGHT | none | PRD evaluator does not implement generic LIGHT file/non-empty behavior. |

## Saga commits / PR refs tied to these contracts

| PR / commit | Evidence | Contract touched | Relevance |
|---|---|---|---|
| PR #155, merge `eb9a2633bfc49b96f2a677fd907a68976f2a5fd9` | `gh pr view 155 --repo IronbellyOrg/IronClaude` returned title `fix(prd): make parallel-instructions gate advisory (warn, don't halt)`, branch `fix/prd-parallel-gate-advisory`, merged to master. | `SemanticCheck.advisory`, `pipeline.gates.gate_passed`, PRD `GATE_CRITERIA` wiring. | Fix intent targets PRD symptom but one implementation (`PrdExecutor._evaluate_gate`) remains off-sweep. |
| PR #154, merge `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e` | `gh pr view 154 --repo IronbellyOrg/IronClaude` title `fix(prd): exempt sequential completion phase from parallel-instructions gate`. | `_check_parallel_instructions` heuristic. | Earlier semantic-check bug/fix in same contract. |
| Commit `ff65a278` | `git log` title `fix(prd): word-boundary completion-signal match in parallel gate`. | `_check_parallel_instructions` matching. | Shows repeated edits to the same semantic check, increasing need for unmask-and-sweep across all evaluators. |
| PR #149, merge `f131592fe3094e222aad17cf82a5b0309ffcdb89` | `gh pr view 149 --repo IronbellyOrg/IronClaude` title `fix(prd): harden artifact-read crash paths (F2/F4/F5) + halt-on-hard-failure plumbing`. | PRD `_execute_step` content resolution and failure/halt plumbing. | Relevant to runtime entrypoint verification: gate input comes from disk-resolved `gate_content`. |
| PR #147, merge `b05e0fe1fddf3152009db51436d67438447dff56` | `gh pr view 147 --repo IronbellyOrg/IronClaude` title `fix(prd): pin canonical output paths + harden recovery for document-capture gate failure`. | PRD artifact capture / canonical path resolution. | Relevant because PRD gate evaluator validates resolved artifact content, not generic output file path. |

## Meta-pipeline lessons against the four global principles

1. Runtime-entrypoint verification: missed or insufficient. The runtime entrypoint for PRD is `PrdExecutor._evaluate_gate`, not `gate_passed`. Any proposed PRD gate fix must first prove the call chain from `superclaude prd run` to the evaluator under test.
2. Contract-implementation enumeration: incomplete. At least four semantic/gate execution loops exist: generic `gate_passed`, PRD `_evaluate_gate`, trailing gate runner via injected/default `gate_check`, and generic cosmetic-remediation semantic dispatch.
3. Unmask-and-sweep: incomplete. Once `SemanticCheck.advisory` was added, every evaluator that consumes `gate.semantic_checks` needed sweeping. The PRD-specific evaluator remained inconsistent with the data contract.
4. Heterogeneous, off-path review: should have explicitly reviewed the fix against a runtime call graph, not only against unit tests for data wiring and generic evaluator behavior.

## Concrete escape candidates for parent investigation

- `EC-A2-001`: PRD advisory fix likely landed on off-path generic evaluator. Symptom: PR #155 intent says warn/don't halt, but `PrdExecutor._evaluate_gate` still returns `False` for any failed semantic check, ignoring `check.advisory`.
- `EC-A2-002`: Frontmatter contract diverges between PRD and generic pipeline. `GATE_CRITERIA` declares required frontmatter for PRD steps, but PRD `_evaluate_gate` does not enforce required frontmatter fields; generic `gate_passed` does.
- `EC-A2-003`: Semantic check loops are duplicated in generic pipeline executor remediation, trailing gates, generic blocking gates, and PRD runtime. Future contract changes need a grep/Auggie sweep for `semantic_checks` consumers, not only the named function under repair.

## Artifact paths

- This report: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md`
