# Reviewer Card 1 — WS-0 Inline Pipeline + Flag Handling

Verdict: **FAIL**

Self-reported confidence: **0.89**

Scope reviewed: committed diff `0f9c8d36..HEAD` for `src/superclaude/cli/swarm/commands.py` plus direct checks of dispatch, normalize, reduce, bare-review lens, bare-review recipe, and preflight behavior relevant to the inline `swarm run --lens bare-review` path.

## Findings

### 1. IMPORTANT — Resume bare-review contracts remain missing the metadata/next-command enrichment the inline path now adds

- file:line: `src/superclaude/cli/swarm/commands.py:1814`
- claim: The inline-path comment says the return contract is enriched with caller metadata and the `--suspect-source` recommended-next-command so the bare-review contract is complete.
- evidence: The inline `reduce_wave3` call passes `lens`, `caller_metadata`, `recommended_next_command_template`, and `recommended_next_command_substitutions` at `src/superclaude/cli/swarm/commands.py:1877`, `src/superclaude/cli/swarm/commands.py:1878`, `src/superclaude/cli/swarm/commands.py:1879`, and `src/superclaude/cli/swarm/commands.py:1882`. The resume branch's `reduce_wave3` call passes only `combined`, `mode`, `output_dir`, `workers_requested`, `status_policy`, `job_id`, and `resume=True` at `src/superclaude/cli/swarm/commands.py:2302` through `src/superclaude/cli/swarm/commands.py:2310`. `reduce_wave3` defaults omitted metadata to empty values (`lens: str = ""`, `caller_metadata: Optional[CallerMetadata] = None`, `recommended_next_command_template: str = ""`) at `src/superclaude/cli/swarm/reduce.py:567`, `src/superclaude/cli/swarm/reduce.py:568`, and `src/superclaude/cli/swarm/reduce.py:572`, then stamps those defaults into the contract at `src/superclaude/cli/swarm/reduce.py:707`, `src/superclaude/cli/swarm/reduce.py:716`, and `src/superclaude/cli/swarm/reduce.py:717`.
- impact: A resumed bare-review run emits a degraded `return-contract.yaml` with empty `lens`, default/empty `caller_metadata`, and no rendered adversarial hand-off command, while the inline run emits the enriched shape. That violates the stated inline-vs-resume parity goal and leaves the resume branch functionally incomplete for the bare-review hand-off.
- suggested deviation_class: regression

### 2. IMPORTANT — Per-reviewer model provenance is dropped from every normalized bare-review body

- file:line: `src/superclaude/cli/swarm/commands.py:1828`
- claim: The inline code says `normalize_wave2` forwards a single `recipe_args` dict to every worker, and then constructs that dict without per-worker model fields.
- evidence: The inline `recipe_args` only sets `target` and `target_checksum` after copying any existing normalization args at `src/superclaude/cli/swarm/commands.py:1833` through `src/superclaude/cli/swarm/commands.py:1838`; it is passed once to `normalize_wave2` at `src/superclaude/cli/swarm/commands.py:1839` through `src/superclaude/cli/swarm/commands.py:1842`. `normalize_wave2` uses one `args = recipe_args or {}` at `src/superclaude/cli/swarm/normalize.py:548` and passes that same `args` to `_normalize_one` for every worker at `src/superclaude/cli/swarm/normalize.py:550` through `src/superclaude/cli/swarm/normalize.py:557`. The bare-review recipe reads `model_id` and `model_label` from `args`, defaulting to empty strings at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:253` and `src/superclaude/cli/swarm/recipes/bare_review_v1.py:254`, then writes them to frontmatter at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:298` and `src/superclaude/cli/swarm/recipes/bare_review_v1.py:299`. Dispatch does have per-worker model identity on each `WorkerResult` and logs it at `src/superclaude/cli/swarm/dispatch.py:321` through `src/superclaude/cli/swarm/dispatch.py:327`, but that data is never merged into recipe args.
- impact: A heterogeneous `openai_compat` run can fan out to multiple real models, but all `.final.md` files report blank `reviewer_model_id` and `reviewer_model_label`. That breaks MultiModelSwarm provenance in the artifact users inspect and pass downstream.
- suggested deviation_class: drift

### 3. IMPORTANT — `target_truncated`, `elapsed_ms`, and recipe-level `status` are also wrong because per-worker/preflight fields are not threaded into the recipe

- file:line: `src/superclaude/cli/swarm/commands.py:1833`
- claim: The inline path omits recipe fields that `bare_review_v1` consumes for truncation, elapsed-time, and parse-error salvage behavior.
- evidence: The inline `recipe_args` construction at `src/superclaude/cli/swarm/commands.py:1833` through `src/superclaude/cli/swarm/commands.py:1838` does not set `status`, `target_truncated`, or `elapsed_ms`. The recipe reads `status` with default `"success"` at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:249`, reads `target_truncated` with default `False` at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:252`, and reads `elapsed_ms` with default `0` at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:257`. It writes `target_truncated` and `elapsed_ms` into frontmatter at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:302` and `src/superclaude/cli/swarm/recipes/bare_review_v1.py:305`. Preflight calculates `_was_truncated` but discards it at `src/superclaude/cli/swarm/preflight.py:1796`, and `_read_truncated_target` also discards `_was_truncated` at `src/superclaude/cli/swarm/commands.py:943`.
- impact: Normalized artifacts always claim `target_truncated: false` and `elapsed_ms: 0`, and the recipe's `status == "parse_error"` salvage branch at `src/superclaude/cli/swarm/recipes/bare_review_v1.py:278` through `src/superclaude/cli/swarm/recipes/bare_review_v1.py:286` cannot observe actual worker status through `args`. Operators can wrongly believe reviewers saw the full target and cannot trust per-reviewer timing/provenance fields.
- suggested deviation_class: drift

### 4. IMPORTANT — `--reviewers` overwrites user-supplied `workers.models` for all input modes, not just lens defaults

- file:line: `src/superclaude/cli/swarm/commands.py:1645`
- claim: The `--reviewers` override correctly validates `[2,4]`, but it unconditionally replaces the model list with placeholder strings.
- evidence: The range check emits usage failure for values outside `[2,4]` at `src/superclaude/cli/swarm/commands.py:1637` through `src/superclaude/cli/swarm/commands.py:1644`. After that, the same block sets `workers_override["count"] = reviewers` at `src/superclaude/cli/swarm/commands.py:1646` and replaces `workers_override["models"]` with `lens-default-model-{i}` placeholders at `src/superclaude/cli/swarm/commands.py:1647` through `src/superclaude/cli/swarm/commands.py:1649`. This mutation is applied after `spec_dict` is resolved for all non-resume input modes, not gated to the `--lens bare-review` shortcut.
- impact: A spec-file/stdin caller that supplied real `workers.models` and also passes `--reviewers 2`, `3`, or `4` silently loses its model identities. That is a flag-handling correctness bug: a count override has an undocumented side effect of replacing caller-provided model selection.
- suggested deviation_class: regression

### 5. IMPORTANT — Target content is read twice, so the prompt can diverge from the checksum stamped into artifacts

- file:line: `src/superclaude/cli/swarm/commands.py:939`
- claim: `_read_truncated_target` re-reads the target from disk after preflight instead of reusing the exact truncated bytes that preflight checksummed.
- evidence: Preflight loads the target via `loader(job.target.path)` at `src/superclaude/cli/swarm/preflight.py:1764` through `src/superclaude/cli/swarm/preflight.py:1768`, then truncates those bytes at `src/superclaude/cli/swarm/preflight.py:1796` through `src/superclaude/cli/swarm/preflight.py:1798` before checksum/guard use. The inline prompt path separately calls `Path(job.target.path).read_bytes()` at `src/superclaude/cli/swarm/commands.py:939` through `src/superclaude/cli/swarm/commands.py:940`, truncates that second read at `src/superclaude/cli/swarm/commands.py:943` through `src/superclaude/cli/swarm/commands.py:945`, and injects it into the prompt at `src/superclaude/cli/swarm/commands.py:1794` through `src/superclaude/cli/swarm/commands.py:1795`. The checksum passed to normalization is still `preflight_result.manifest.preflight.target_checksum` at `src/superclaude/cli/swarm/commands.py:1835` through `src/superclaude/cli/swarm/commands.py:1837`.
- impact: If the target file changes between preflight and prompt assembly, reviewers receive content whose checksum does not match the checksum stamped into `.final.md` frontmatter and the contract. If the second read fails, `_read_truncated_target` returns an empty string at `src/superclaude/cli/swarm/commands.py:941` through `src/superclaude/cli/swarm/commands.py:942`, silently dispatching an empty-target prompt to live workers instead of failing the run.
- suggested deviation_class: regression

### 6. MINOR — `--target-line-cap` and `--timeout-sec` accept non-positive integers with surprising semantics

- file:line: `src/superclaude/cli/swarm/commands.py:1659`
- claim: Only `--reviewers` has explicit range validation; the sibling new numeric flags are assigned directly.
- evidence: `--target-line-cap` is assigned directly to `target.truncation.line_cap` at `src/superclaude/cli/swarm/commands.py:1659` through `src/superclaude/cli/swarm/commands.py:1662`. `--timeout-sec` is assigned directly to `workers.timeout_sec` at `src/superclaude/cli/swarm/commands.py:1670` through `src/superclaude/cli/swarm/commands.py:1671`. `_truncate_target` treats `line_cap <= 0` as disabling truncation at `src/superclaude/cli/swarm/preflight.py:878` through `src/superclaude/cli/swarm/preflight.py:883`.
- impact: `--target-line-cap 0` or a negative value disables truncation instead of rejecting an invalid cap. `--timeout-sec 0` or a negative value is accepted into the worker spec rather than rejected at CLI usage time. Even if lower layers apply defaults, the CLI flag surface silently accepts values that do not mean what an operator expects from a positive cap/budget.
- suggested deviation_class: necessary

### 7. MINOR — Terminal state can be written even when Wave 2/3 was skipped and no contract was emitted

- file:line: `src/superclaude/cli/swarm/commands.py:1818`
- claim: The inline normalize/reduce block is conditional on both `state_output_dir` and `recipe_name`, but terminal state is written unconditionally when `state_output_dir` exists.
- evidence: The only inline call to `normalize_wave2`/`reduce_wave3` is inside `if state_output_dir is not None and recipe_name:` at `src/superclaude/cli/swarm/commands.py:1818` through `src/superclaude/cli/swarm/commands.py:1884`. The terminal state write is outside that block and only checks `state_output_dir is not None` at `src/superclaude/cli/swarm/commands.py:1889` through `src/superclaude/cli/swarm/commands.py:1894`. `reduce_wave3` is the function that emits `return-contract.yaml` when `output_dir` is present, via `emit_contract(contract, Path(output_dir))` at `src/superclaude/cli/swarm/reduce.py:721` through `src/superclaude/cli/swarm/reduce.py:722`.
- impact: A spec-file/stdin run with output but no normalization recipe can end in `.swarm-state.json` state `terminal` without a normalized artifact or return contract. That is a misleading completion signal for the inline pipeline.
- suggested deviation_class: regression

### 8. MINOR — Recommended next command is advertised as copy-pasteable but is not shell-safe for output paths containing spaces or commas

- file:line: `src/superclaude/cli/swarm/commands.py:1845`
- claim: The code comment promises a copy-pasteable recommended next command, but the substitution joins raw paths without quoting or escaping.
- evidence: The comment at `src/superclaude/cli/swarm/commands.py:1844` through `src/superclaude/cli/swarm/commands.py:1847` says the contract carries a copy-pasteable `/sc:adversarial --compare ... --suspect-source ...`. The substitution builds `suspect_files` as `",".join(succeeded_final_paths)` at `src/superclaude/cli/swarm/commands.py:1860` through `src/superclaude/cli/swarm/commands.py:1862` and `compare_files` as a comma-joined list at `src/superclaude/cli/swarm/commands.py:1864` through `src/superclaude/cli/swarm/commands.py:1867`. The bare-review template places those raw strings directly after flags at `src/superclaude/cli/swarm/lenses/bare_review.py:65` through `src/superclaude/cli/swarm/lenses/bare_review.py:68`, and reduce renders them via `format_map` without shell quoting at `src/superclaude/cli/swarm/reduce.py:467` through `src/superclaude/cli/swarm/reduce.py:486`.
- impact: If `--output` contains a space, the emitted command splits the path into multiple shell words. If it contains a comma, the comma-delimited path list becomes ambiguous. The contract can therefore emit a recommended command that is not actually copy-pasteable.
- suggested deviation_class: drift

## Verified non-findings

- `dispatch_wave1` accepts the new inline call shape: `prompt` and `worker_spec` are real keyword parameters at `src/superclaude/cli/swarm/dispatch.py:334` through `src/superclaude/cli/swarm/dispatch.py:342`, and `_run_worker` passes `prompt` plus the effective `WorkerSpec` into `retry_policy` at `src/superclaude/cli/swarm/dispatch.py:457` through `src/superclaude/cli/swarm/dispatch.py:458`.
- `reduce_wave3` internally emits the return contract when `output_dir` is present: its signature accepts all inline arguments at `src/superclaude/cli/swarm/reduce.py:555` through `src/superclaude/cli/swarm/reduce.py:576`, and it calls `emit_contract` at `src/superclaude/cli/swarm/reduce.py:721` through `src/superclaude/cli/swarm/reduce.py:722`. No separate emit call is needed.
- `normalize_wave2` accepts the inline call shape (`recipe_name`, `recipe_args`) at `src/superclaude/cli/swarm/normalize.py:500` through `src/superclaude/cli/swarm/normalize.py:506`.
- The bare-review lens provides the expected `{target_content}` placeholder and recommended-next-command placeholders at `src/superclaude/cli/swarm/lenses/bare_review.py:53` through `src/superclaude/cli/swarm/lenses/bare_review.py:68`.
- `_stamp_inline_worker_paths` preserves dynamic `.body` after `dataclasses.replace` by reattaching it at `src/superclaude/cli/swarm/commands.py:1002` through `src/superclaude/cli/swarm/commands.py:1010`, and `normalize._read_raw` reads that dynamic body first at `src/superclaude/cli/swarm/normalize.py:334` through `src/superclaude/cli/swarm/normalize.py:336`.
- `--reviewers` out-of-range correctly exits with `EXIT_USAGE` at `src/superclaude/cli/swarm/commands.py:1637` through `src/superclaude/cli/swarm/commands.py:1644`.
- The inline path avoids the `expand_lens_defaults` equality-reset trap: `run_preflight` calls `materialize_lens_defaults` at `src/superclaude/cli/swarm/preflight.py:1735`, while the reviewed inline comments correctly identify that `expand_lens_defaults` is not on this path at `src/superclaude/cli/swarm/commands.py:1632` through `src/superclaude/cli/swarm/commands.py:1636` and `src/superclaude/cli/swarm/commands.py:1651` through `src/superclaude/cli/swarm/commands.py:1658`.
