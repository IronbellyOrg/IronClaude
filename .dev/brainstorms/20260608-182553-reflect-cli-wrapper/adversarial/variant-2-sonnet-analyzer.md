# Variant 2 — Analyzer Design Spec: Fail-Closed Thin Reflect CLI Wrapper

## Problem

Task-builder tasklists currently end with a manual HALT item that asks an operator to run `/sc:reflect --mode post` in a fresh session, then copy the verdict back into task frontmatter. That preserves executor-disjoint review, but it is not autonomous.

The proposed wrapper exists to automate only the harness around that step:

1. resolve tasklist inputs and a deterministic POST depth;
2. launch a TOP-LEVEL `claude --print` subprocess that invokes the existing `/sc:reflect --mode post` skill command;
3. pin the reflect `--output` directory;
4. parse reflect's `return-contract.yaml` without reimplementing reflect logic;
5. write a compact `reflect_post` verdict back into the task file frontmatter; and
6. return an exit code that makes the final tasklist gate HALT on weak, partial, degraded, or human-decision states.

The central analyzer thesis is: the wrapper must never accept a silently degraded Tier-2 audit. Reflect itself may fail-open on missing MCPs or aliases for interactive use, but this wrapper is a gate consumer. A final tasklist gate is only useful if it distinguishes `full Tier-2 audit completed` from `reflect produced a report after losing the grounding/diversity mechanisms that made Tier 2 valuable`.

The wrapper is deliberately not `sc:cli-portify`. It does not port reflect waves, reviewer composition, evidence validation, deviation taxonomy, promotion logic, or remediation logic into Python. It treats `return-contract.yaml` as the sole machine-readable source of truth and adds a stricter consumer policy for tasklist completion.

## Failure-Mode Register

### FM-1: Agent-tool nesting limit silently disables Tier 2

**Condition:** The final tasklist item is executed inside an Agent-tool subagent, and that subagent tries to run `/sc:reflect`; reflect then attempts its own Tier-2 Task fan-out and hits the subagent-nesting boundary.

**Detection:** Wrapper records its launch surface and refuses any mode that does not spawn a new OS child process running the `claude` binary. Preflight asserts the child command is `claude --print ...`, not an in-process Skill invocation, not `Task(...)`, and not `/sc:reflect` in the current conversation.

**Required behavior:** Launch reflect only through the real CLI subprocess path. If the wrapper is invoked from a context that cannot spawn `claude`, set `reflect_post: {verdict: blocked, reason: subprocess-unavailable}` and exit non-zero. Do not fall back to inline reflect.

### FM-2: Child process is still treated as nested Claude Code

**Condition:** The parent environment leaks nested-session variables into the child, causing Claude Code to suppress expected top-level behavior.

**Detection:** Reuse `src/superclaude/cli/pipeline/process.py` semantics: child env is copied from `os.environ` after removing `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. Dry-run prints a redacted env audit showing those two keys absent.

**Required behavior:** Use `ClaudeProcess` or a thin adapter around it. Do not call `subprocess.Popen` directly unless the exact env-scrub/process-group/stdout-stderr separation semantics are preserved.

### FM-3: Headless MCP degradation weakens grounding but reflect still returns success

**Condition:** The subprocess lacks Serena and/or auggie. Reflect's protocol allows fail-open: Serena unavailable falls back to Grep/Glob, auggie unavailable weakens neighbour search, and verification triangle may skip when `execute_shell_command` is unavailable or read-only cannot be confirmed.

**Detection:** Parse the contract fields and telemetry, especially `degraded_components`, `neighbour_search_degraded`, `verification_ran`, `verification_skip_reason`, `serena_config_snapshot_path`, `serena_active_context`, `serena_active_modes`, `evidence_validator_ran`, `citations_dropped`, `needs_human_decision`, and `grounding_gaps_path`. Treat any chain-critical missing-MCP marker as gate-relevant, even if reflect status is `success`.

**Required behavior:** For a POST tasklist gate, fail closed on grounding degradation: write `reflect_post.verdict: halted` with `reason: degraded-grounding` and do not let the Done item proceed. The operator may inspect the report and manually override outside the wrapper, but the wrapper must not convert this into pass.

### FM-4: Model aliases do not propagate to subprocess

**Condition:** `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, or `ANTHROPIC_DEFAULT_HAIKU_MODEL` are missing in the child env. Reflect may route to T1-only or a degraded two-reviewer T2 without stopping.

**Detection:** Before spawn, count aliases in the exact env dict handed to the child. After reflect, parse `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity`, `reviewer_models`, `reviewer_vendors`, and `degraded_components: env-aliases`.

**Required behavior:** For medium/complex tasklists where TCS implies standard/deep and the POST floor forbids quick, require enough aliases for the intended tier. If expected Tier 2 but the contract says T1-only, `t2_model_class_diversity: degraded` with fewer than required reviewers, or `t2_effective_diversity: none`, halt as `degraded-tier2`. Single-vendor T2 is at least loud-warning in reflect; the wrapper should treat it as halt for this gate unless an explicit `--allow-single-vendor` is passed.

### FM-5: Explicit Tier 2 with zero aliases STOPs before contract exists

**Condition:** The wrapper passes `--tier 2` while zero aliases resolve. Reflect's Wave 0 is specified to STOP loudly because explicit Tier 2 cannot be satisfied.

**Detection:** Non-zero child exit, missing `return-contract.yaml`, stderr/stdout containing reflect STOP text, and preflight alias count of zero.

**Required behavior:** Write `reflect_post: {verdict: blocked, reason: zero-aliases-tier2-conflict}` and exit non-zero. Do not synthesize a success-shaped contract. Point to the child logs and the intended output dir.

### FM-6: Bad input makes reflect STOP before producing a usable contract

**Condition:** Missing `--diff`/`--task-log` for `--mode post`, missing input files, under-specified deep input, or forbidden output dir under `.claude/skills`, `.claude/agents`, or `.claude/commands`.

**Detection:** Wrapper preflight validates absolute `tasklist`, `spec`, `output`, and diff range before spawn. After spawn, missing or unparsable contract with child non-zero is classified as `reflect-stop`, not as a failed audit.

**Required behavior:** Fail before launch when possible. If reflect itself STOPs, write `reflect_post.verdict: blocked`, include `reason`, `stdout_path`, `stderr_path`, and `output_dir`, and exit non-zero.

### FM-7: Output-dir collision hides the artifact actually parsed

**Condition:** Reflect may append `-N` on output collision, while the wrapper expects the original path.

**Detection:** Wrapper creates a run-unique pinned output dir before spawn using a run id: `<task-dir>/validation/reflect-post/<task-id>-<timestamp>-<pid>/`. It passes exactly that absolute `--output` and records it. After spawn, the contract must live exactly at `<output>/return-contract.yaml`; a sibling suffixed dir is treated as unexpected.

**Required behavior:** Never parse a guessed sibling. If the exact contract is missing, halt as `contract-missing`. The wrapper owns output uniqueness, so reflect collision suffixing should be unreachable.

### FM-8: Reflect returns `status: partial`

**Condition:** Reflect finds input drift, evidence-validator partials, citation drops, grounding gaps, adversarial unavailable, audit-log partials, or budget-forced downgrade.

**Detection:** Parse stable `status` plus the flags that explain partial: `input_drift_detected`, `citations_dropped`, `needs_human_decision`, `budget_forced_tier_downgrade`, `adversarial_unavailable`, `verification_skip_reason`, etc.

**Required behavior:** Halt. Write the report path and reason summary, but never mark the final gate complete. `partial` is actionable human-review state, not pass.

### FM-9: Reflect returns `needs_human_decision` or `user_decision_required`

**Condition:** Grounding gaps or unresolved ambiguity require operator judgment.

**Detection:** Parse `needs_human_decision` and `user_decision_required`; also parse `grounding_gaps_path` for non-empty findings if present.

**Required behavior:** Halt. Do not auto-default, do not choose among options, do not proceed to Done. The frontmatter must make the pending decision obvious.

### FM-10: Regression or unauthorized deviation present

**Condition:** Reflect finds `regression_present: true`, `unauthorized_deviation_present: true`, or non-zero `deviation_count_by_class.regression` / `.drift`.

**Detection:** Parse those exact fields.

**Required behavior:** Halt. The wrapper can summarize the deviation counts in frontmatter, but no remediation or rollback is auto-executed. Tier 3 task-builder remediation remains opt-in/operator-driven.

### FM-11: Tier 2 adversarial merge collapses to null convergence

**Condition:** `adversarial_unavailable: true`, `merge_method: single-reviewer-fallback`, or Tier 2 ran with `adversarial_convergence_score: null`.

**Detection:** Parse `tier_reached`, `adversarial_unavailable`, `merge_method`, and `adversarial_convergence_score`.

**Required behavior:** For a final tasklist gate, halt as `degraded-adversarial-merge`. This mirrors reflect's promotion condition that Tier 2 with no merged adversarial verdict cannot promote.

### FM-12: Budget/timeout cuts off an 8-15 minute Tier-2 run

**Condition:** Child process exceeds timeout or reflect aborts mid-Wave-3 due to token budget.

**Detection:** `ClaudeProcess.wait()` returns 124 on timeout; reflect contract may be absent or partial. Also parse `budget_forced_stop`, `budget_forced_tier_downgrade`, and child logs.

**Required behavior:** Default timeout is 30 minutes for the wrapper, configurable with `--timeout-seconds`, with SIGTERM then SIGKILL through process group termination. Timeout writes `reflect_post.verdict: blocked`, `reason: timeout`, and paths to logs. Budget-forced downgrade halts as degraded, not pass.

### FM-13: Cross-session `summarize_changes` is unavailable by design

**Condition:** The top-level child is a fresh session, so Serena `summarize_changes` cannot summarize the parent executor's edits.

**Detection:** Contract field `serena_summary_corroboration: unavailable`.

**Required behavior:** Do not halt solely for this field. It is an expected consequence of escaping the nesting limit. The wrapper records it as an informational caveat and relies on `--diff` as the authoritative completed-work input.

### FM-14: Frontmatter write-back races with other sessions

**Condition:** Multiple Claude sessions share the same worktree and one process edits the task file while the wrapper is reading or writing `reflect_post`.

**Detection:** Before write, capture task file content hash and current `HEAD` / `git status --porcelain` snapshot. Use an atomic compare-before-replace: the bytes on disk must match the bytes read for frontmatter parsing. After write, re-stat and confirm only the intended frontmatter block changed.

**Required behavior:** On mismatch, do not overwrite. Write a sidecar result under the reflect output dir, set process exit non-zero, and tell the operator to re-run or merge manually. The wrapper must not use `git add`, commit, or manipulate the shared index.

### FM-15: Frontmatter is missing or unparsable

**Condition:** Task file has no YAML frontmatter, malformed frontmatter, duplicate `reflect_post`, or an incompatible schema.

**Detection:** Strict frontmatter parser before reflect spawn.

**Required behavior:** Fail before spending Tier-2 tokens unless `--contract-only` is passed. Write no partial mutation. Surface a repair instruction.

### FM-16: Final tasklist Done item proceeds after a non-pass verdict

**Condition:** Task executor treats the wrapper command's completion as success even though reflect halted.

**Detection:** Wrapper exit-code contract: only clean audit states exit 0. All degraded, partial, failed, blocked, timeout, or race states exit non-zero.

**Required behavior:** The final task item's completion gate must require both exit code 0 and `reflect_post.verdict: pass`. Any other value is HALT.

### FM-17: Reflect's default promotion path mutates repository state

**Condition:** `/sc:reflect --mode post --remediate` may offer remediation, and reflect has a Wave-7 promotion path unless suppressed.

**Detection:** Wrapper always includes `--no-promote` and expects `promotion_action: skipped` or `not-applicable` with `promotion_skip_reason: user-flag` when present.

**Required behavior:** Default audit-only. The wrapper never auto-commits, never stages, never promotes, and never runs Tier 3 task execution.

### FM-18: Wrapper accidentally becomes a second reflect implementation

**Condition:** Wrapper starts making its own deviation, citation, or confidence decisions beyond consumer routing.

**Detection:** Code review/test rule: wrapper may inspect contract fields only for gate routing and write-back. It must not parse diff hunks or classify deviations itself.

**Required behavior:** Keep wrapper thin. Any new audit logic belongs in `sc-reflect-protocol`, not in the wrapper.

## Functional Requirements

### FR-1: CLI surface

Provide a new installable Click subcommand under `src/superclaude/cli/reflect/`, registered as `superclaude reflect run`.

Minimal command shape:

```text
superclaude reflect run --tasklist /abs/task.md --diff <base>..HEAD [--spec /abs/spec.md] [--executor-model <class>] [--output /abs/dir] [--timeout-seconds 1800] [--attach|--no-attach] [--allow-single-vendor] [--dry-run]
```

### FR-2: Absolute path discipline

All paths accepted by the wrapper are resolved to absolute paths before validation, before spawn, and before writing to frontmatter. The wrapper writes absolute artifact paths into `reflect_post`.

### FR-3: Input derivation

If flags are omitted, derive:

- `tasklist`: required from explicit flag in v1; no implicit cwd guessing.
- `base`: frontmatter `start_commit`, else `git merge-base HEAD origin/master`, else fail with `base-unresolved`.
- `diff`: `<base>..HEAD`.
- `spec`: explicit `--spec`; otherwise tasklist frontmatter `related_docs` / `spec` only when it resolves to one absolute file; ambiguous matches are omitted with WARN.
- `depth`: deterministic TCS from task-builder rules, with POST floor `standard`; `deep` when TCS hard overrides force it.
- `executor-model`: explicit flag, else `EXECUTOR_MODEL_CLASS`, else `unknown` with loud warning.

### FR-4: Top-level subprocess launch

Invoke reflect through the real `claude` binary using the production `ClaudeProcess` path where practical. The prompt sent over stdin is the slash command string:

```text
/sc:reflect --mode post --remediate --no-promote --diff <base>..HEAD --tasklist <abs-tasklist> [--spec <abs-spec>] --depth <standard|deep> --executor-model <class> --output <abs-output>
```

Do not call `Skill sc-reflect-protocol` directly from the wrapper process.

### FR-5: Headless environment parity

The child receives the parent alias env vars, MCP settings, and Claude configuration needed for the same tool surface an operator would have in a top-level session. The env audit records whether `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL` are present.

### FR-6: Output contract parsing

After child exit, read exactly `<output>/return-contract.yaml`. Require `contract_version` compatible with `1.x`, `mode: post`, and `report_path` pointing inside the pinned output dir or an explicitly absolute report path that exists.

### FR-7: Gate routing

Map reflect contract to wrapper verdict:

- `pass`: only when reflect `status: success`, expected tier reached, no critical degradation, no human decision, no regressions/drift, no citation drops, no input drift, and no Tier-2 adversarial collapse.
- `halted`: reflect completed but found a gate-blocking condition.
- `degraded`: reflect completed but lost required Tier-2 diversity/grounding/adversarial mechanisms.
- `blocked`: reflect did not produce a usable contract, failed preflight, timed out, or hit STOP before contract.

Only `pass` exits 0.

### FR-8: Frontmatter write-back

Write a compact frontmatter object:

```yaml
reflect_post:
  verdict: pass|halted|degraded|blocked
  run_id: <timestamp-slug>
  status: success|partial|failed|dry-run|null
  tier_reached: 1|2|3|null
  report: /abs/path/to/REPORT.md
  contract: /abs/path/to/return-contract.yaml
  reason: <short slug>
  reviewed_at: <ISO-8601>
```

Preserve unrelated frontmatter fields and body content byte-for-byte.

### FR-9: Race-safe write

Use read-hash compare before write. On mismatch, do not overwrite; write `<output>/wrapper-result.yaml` and exit non-zero.

### FR-10: Window mechanic

Support two execution modes:

- default blocking mode: current process runs child and streams/tails logs to the current terminal;
- optional `--attach` mode: if tmux is available and not already inside tmux, create a tmux session/window that runs the wrapper foreground command, attach, then read a sentinel exit code.

The first implementation should prefer blocking foreground for simplicity; tmux attach can be a thin adapter using sprint's sentinel pattern.

### FR-11: Logs and observability

Write child stdout, stderr, env audit, command audit, wrapper routing result, and frontmatter-write status under the pinned output directory. Redact secrets from env audit.

### FR-12: Dry run

`--dry-run` performs input derivation, env preflight, command construction, output-path reservation check, and frontmatter parse, but does not launch reflect or edit the task file.

## Non-Functional Requirements

### NFR-1: Thinness

The wrapper must remain under the complexity envelope of an orchestration shim. It consumes reflect output; it does not duplicate reflect's audit algorithms.

### NFR-2: Fail-closed gate posture

Any inability to prove a full, non-degraded Tier-2 audit for a medium/complex POST gate routes to HALT.

### NFR-3: Reversibility

Task-builder template changes are minimal and can be reverted to the current manual HALT item without changing reflect.

### NFR-4: No repository mutation beyond frontmatter

The wrapper only writes the task file frontmatter and artifacts under reflect output. It never stages, commits, promotes, moves task directories, or edits source files.

### NFR-5: Timeout safety

Default timeout is long enough for expected Tier-2 (30 minutes), configurable, and enforced through process-group termination.

### NFR-6: Testability

Unit tests cover command construction, env audit, contract routing table, TCS depth derivation, output collision rejection, and atomic frontmatter write. Integration tests can stub `claude` with a fake binary that writes contracts.

### NFR-7: Absolute-path-only artifacts

All written report/contract paths in frontmatter are absolute to prevent prior relative-path mis-resolution.

### NFR-8: Unknown-field tolerance

The parser ignores unknown contract fields but fails on missing load-bearing fields.

## Design

### 1. Wrapper home

Implement as `src/superclaude/cli/reflect/` and register `superclaude reflect run` in `src/superclaude/cli/main.py`. This is more discoverable and testable than `scripts/`, and matches existing CLI surfaces. The command is a wrapper around the slash command, not a native reflect implementation.

### 2. Window mechanic

The default is blocking foreground execution from the final tasklist item:

1. wrapper preflights;
2. wrapper launches `claude --print` through `ClaudeProcess`;
3. wrapper waits up to timeout;
4. wrapper parses contract;
5. wrapper writes frontmatter;
6. wrapper exits with pass/halt code.

For operators who want a visible detached window, `--attach` uses the sprint tmux pattern: create a deterministic `sc-reflect-<hash>` tmux session running the same foreground wrapper command with `--no-attach`, attach, and read `.reflect-exitcode` from the pinned output dir after the session ends. The tmux layer does not own reflect logic.

### 3. Subprocess mechanics

Use `ClaudeProcess` for:

- `claude --print --verbose` command construction;
- prompt delivery over stdin to avoid argv length limits;
- stdout/stderr separation;
- process-group kill on timeout;
- env scrub of nested-session variables; and
- optional `--model` forwarding if the wrapper itself is configured to choose the top-level orchestrator model.

If cwd pinning or HOME isolation is needed, use the eval adapter pattern: merge extra env first, then isolation env, and chdir only around spawn.

### 4. Degradation detection

The wrapper has two checks: preflight and post-contract.

Preflight checks:

- child env has model aliases expected for Tier 2;
- `claude` binary is found;
- tasklist/spec/output paths are valid and absolute;
- output path is not under forbidden `.claude` distributable directories;
- frontmatter is parseable and writable;
- diff base resolves.

Post-contract checks:

- `status` is `success`;
- `mode` is `post`;
- expected tier was reached;
- `degraded_components` does not contain `serena`, `auggie`, `env-aliases`, `evidence-validator`, `serena:context-excluded`, `neighbour-search:auggie_unavailable`, or equivalent chain-critical markers;
- `verification_ran` is true unless explicitly exempted by a user flag;
- `t2_model_class_diversity == full` for expected full T2;
- `t2_vendor_diversity == multi` unless `--allow-single-vendor`;
- Tier 2 has a non-null adversarial result;
- `citations_dropped == 0`;
- `needs_human_decision == false`;
- `user_decision_required == false`;
- no drift/regression counts;
- no input drift.

This is intentionally stricter than reflect's interactive fail-open policy.

### 5. Write-back

The frontmatter update is a single compare-and-replace operation:

1. read task bytes;
2. parse frontmatter and body;
3. construct new frontmatter with only `reflect_post` changed;
4. verify current on-disk bytes still equal the originally read bytes;
5. write to a temp file beside the task file;
6. fsync temp;
7. atomic rename over the task file.

If the compare fails, no write occurs. If the write succeeds but post-write validation fails, the wrapper exits non-zero and leaves artifacts for manual inspection.

### 6. HALT routing

Exit codes:

- `0`: pass only.
- `10`: reflect completed and halted on audit findings.
- `11`: reflect completed but gate-critical degradation detected.
- `12`: preflight blocked.
- `13`: child failed or no contract.
- `14`: timeout.
- `15`: write-back race or frontmatter write failure.

Task-builder's final item should require exit 0 and `reflect_post.verdict: pass` before the Done item proceeds.

### 7. Contract sidecar

Always write `<output>/wrapper-result.yaml` with wrapper verdict, input derivation, env audit summary, child exit code, frontmatter write status, and the reason slug. This sidecar is especially important when frontmatter cannot be written.

## Resolved Open Questions

1. **Window mechanic:** Default blocking foreground wrapper; optional tmux attach uses sprint's sentinel pattern. Blocking is simpler and makes exit-code gating reliable; tmux is presentation only.
2. **Wrapper home:** New `superclaude reflect run` Click subcommand under `src/superclaude/cli/reflect/`, registered in the CLI. Not a standalone script.
3. **Input derivation:** Require explicit absolute `--tasklist`; derive base from `start_commit` then merge-base; derive depth from TCS with POST floor standard; derive executor-model from flag/env/log with unknown warning.
4. **Verdict write-back:** Parse `return-contract.yaml` and write `reflect_post` frontmatter. Exit code mirrors wrapper verdict. Completion gate consumes both.
5. **Headless env:** Reuse `ClaudeProcess` env scrub and optionally eval `HomeIsolation`/cwd adapter. Preflight aliases and post-parse degradation fields; halt on missing grounding/diversity.
6. **Runtime/budget:** Default 30-minute timeout; configurable. Timeout and budget-forced downgrades halt, never pass. No resume in v1 beyond re-run with same output-safe run id policy.
7. **Template integration:** Minimal opt-in replacement for the current manual HALT line: final item runs `superclaude reflect run ...` and halts unless exit 0. Keep manual paste-ready command as fallback text.
8. **Promotion:** Always pass `--no-promote` in v1. Default audit-only. No Wave-7 promotion through the wrapper.

## Scope Boundaries

In scope:

- CLI wrapper orchestration.
- Top-level `claude --print` launch.
- Deterministic input derivation.
- Contract parsing and stricter consumer routing.
- Race-safe frontmatter write-back.
- Minimal task-builder template wording to call the wrapper.

Out of scope:

- Porting reflect logic to Python.
- Running reflect inside Agent-tool subagents.
- Auto-remediation execution.
- Auto-commit, git staging, promotion, archive moves.
- Replacing reflect's return contract.
- Fixing missing MCP installation automatically.
- Solving shared-worktree concurrency beyond compare-before-write.

## Risks

1. **Over-strict degradation policy may halt runs reflect considered acceptable.** This is intentional for the tasklist completion gate. Provide explicit override flags only when the operator accepts weaker audit guarantees.
2. **Claude CLI flag drift.** Reusing `ClaudeProcess` centralizes command construction and limits drift.
3. **MCP availability differs between interactive and subprocess HOME.** The wrapper must log enough env/config state to debug this and should prefer inheriting the operator's known-good config unless tests require isolation.
4. **Frontmatter parser edge cases.** Keep write-back schema compact and test malformed, duplicate, empty, and emoji-containing fields.
5. **Output contract evolves.** Unknown-field tolerance handles additive changes; missing load-bearing fields halts and forces wrapper update.
6. **Parallel sessions still share files and git state.** The wrapper avoids index operations and uses compare-before-write, but it cannot prevent another process from changing code during reflect; reflect's own input drift guard must catch that.
7. **Single-vendor alias setups are common during local development.** The wrapper may feel noisy. That is preferable to silently accepting a homogeneous "Tier 2" ensemble.
8. **Operator confusion between reflect `status` and wrapper `verdict`.** Documentation and frontmatter names must make clear: reflect status is producer truth; wrapper verdict is consumer gate routing.
