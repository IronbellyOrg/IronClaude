# Hypothesis Card: E1-PRD-cloud-file-misuse

## Lens

Runtime-entrypoint lens.

## Escape hypothesis

The defect escaped review because reviewers validated the PRD `--spec` feature at the configuration, prompt, and command-construction layers, but not at the actual headless runtime boundary where `PrdExecutor._run_subprocess_step()` instantiates `PrdClaudeProcess`, appends PRD-specific `extra_args`, and launches the shared `ClaudeProcess` subprocess. That left a false contract in place: PRD treated `claude --file <local_path>` as a local file-content attachment mechanism, while the CLI interpreted `--file` as a cloud file-download/session-token feature.

In other words, the reviewed surface proved that PRD could remember spec paths and place them into prompts, and that `_build_file_args()` produced the expected argv shape. It did not prove that the argv shape was valid for `claude --print --no-session-persistence` in a headless environment with no `CLAUDE_CODE_SESSION_ACCESS_TOKEN`.

## Evidence chain

1. The runtime crash is documented as a headless subprocess failure, not a static construction failure: `pr-targets-summary.txt` states that PRD passed local filesystem paths to `claude --file`; in a headless `--spec` run with no session token, the subprocess exited in about 0.3 seconds with `Error: Session token required for file downloads` and crashlooped at `scope-discovery`.

2. The current fixed runtime path confirms where the missing verification needed to execute. `src/superclaude/cli/prd/executor.py` builds the prompt, creates `PrdClaudeProcess`, calls `proc.start_with_retry()`, and then waits on the subprocess. `src/superclaude/cli/pipeline/process.py` constructs the real `claude` command and appends `self.extra_args` immediately before launch.

3. The pre-fix implementation put the invalid contract exactly on that runtime boundary. In the parent of fix commit `235f59ee101032606cccb315105191c428621531`, `src/superclaude/cli/prd/process.py` defined `_SPEC_FILE_STEPS = {"scope-discovery", "investigation"}`, built `file_args = self._build_file_args(config, step_id)`, passed those as `extra_args=file_args`, and extended the argv with `['--file', spec_path]` for configured `spec_files` on those steps. It also used `--file` for large refs.

4. The pre-fix tests exercised the wrong seam. The old `tests/cli/prd/test_spec_flag.py` contained assertions around `PrdConfig.spec_files`, prompt content, `_authoritative_specs_block()`, and `PrdClaudeProcess._build_file_args()`, including expected `['--file', path]` output. That proves tests locked in command construction rather than executing the headless subprocess path that would have rejected the flag.

5. The sibling-pipeline contract was already available but not swept into PRD. `pr-targets-summary.txt` records that roadmap/tasklist/validate already forbade `--file` and delivered content inline, while PRD was the only pipeline emitting it. The escape therefore required both a runtime-entrypoint miss and a cross-pipeline contract-enumeration miss.

6. The artifact audit independently classifies the pattern: runtime-entrypoint verification failed until late in the saga; E1 and E3 escaped artifacts that reasoned over source/test surfaces without executing the production/headless runtime path, and the later PRD-local-file task stated the symptom as local paths passed through Claude CLI `--file` causing headless `scope-discovery` failure.

## Why review missed it

Review was anchored on an internally plausible but externally unverified abstraction: “attach spec content to the agent.” Inside PRD, `_build_file_args()` looked like a reusable delivery mechanism and tests confirmed that the expected flags were generated for the expected phases. But the boundary that mattered was not PRD’s intent; it was Claude CLI’s runtime interpretation of `--file` under `--print`, `--no-session-persistence`, and no session token.

The reviewed artifacts therefore had a coverage illusion:

- Config verification showed `--spec` became absolute `PrdConfig.spec_files`.
- Prompt verification showed authoritative spec paths were visible to `scope-discovery`.
- Unit verification showed `_build_file_args()` emitted `--file` for `scope-discovery` and `investigation`.
- No verification spawned the real `claude` subprocess in the same headless mode the pipeline uses.

Because the invalid behavior lives after command construction, any test that stops at `build_command()` or `_build_file_args()` can pass while the production subprocess immediately fails. Because the issue was also inconsistent with sibling pipelines, a contract sweep across roadmap/tasklist/validate would likely have exposed PRD as the outlier before runtime.

## Confidence

High. The symptom, the pre-fix code path, the current fixed code path, and the post-fix summaries all point to the same escape mechanism: review validated PRD’s intended local-file delivery abstraction but did not validate Claude CLI’s actual headless runtime contract.

## What this hypothesis does not claim

This card does not propose a PRD patch. PR #151 already removed the `--file` emissions and inlined specs/refs. The review-escape claim is narrower: the failure escaped because the verification boundary ended before the subprocess runtime entrypoint and because sibling pipeline contracts were not enumerated against PRD.
