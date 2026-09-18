# Bash Inspection Batching Policy — Risk Register

**Date:** 2026-09-17
**Scope:** Proposed `N = 4` policy requiring five or more consecutive eligible Bash inspections against known paths to run as a generated `/tmp` batch in one tool call.

## Rating scale

- **Severity:** Low / Medium / High / Critical
- **Likelihood:** Low / Medium / High
- Residual ratings assume the mitigations selected by `POLICY.md`; alternatives are listed so implementation can choose based on measured rollout data.

## Summary

| ID | Risk | Severity | Likelihood | Residual target |
|---|---|---:|---:|---:|
| R1 | Loss of interactivity and adaptation | High | High | Medium |
| R2 | One bad command poisons later results | High | Medium | Low–Medium |
| R3 | One wrong script scales an error across many targets | High | Medium | High until validator/sandbox; then Low–Medium |
| R4 | Reduced security and human review under `bypassPermissions` | Critical | Medium | High until validator/template gate |
| R5 | Hidden state/data dependency makes batching semantically wrong | High | High | Low–Medium |
| R6 | Whole-batch timeout or output truncation loses useful work | Medium | Medium | Medium until caps are enforced |
| R7 | Threshold gaming and metric-driven behavior | High | Medium | Medium |
| R8 | Hook latency, false positives, and concurrency miscounts | Medium | Medium | Medium |
| R9 | `/tmp` race, leakage, or orphaned artifacts | High | Low–Medium | Medium for forced-kill path |
| R10 | Wrapper permission rules become a universal bypass | Critical | Medium | Medium until mechanically gated |

## R1 — Loss of interactivity and adaptation

**Failure mode:** The 2,300× replay ratio compares shell execution, not end-to-end reasoning quality. In separate calls, the agent reads command A before deciding whether B is useful or safe. A batch freezes the plan and may run irrelevant commands, inspect the wrong targets, or miss an early stop condition.

**Detection signals:**

- Later calls rerun commands already present in a batch.
- A post-batch command's target or arguments were discovered in the batch output.
- More than half of a follow-up wave is a corrected version of the prior batch.

**Alternative mitigations:**

1. **Selected:** Batch only when all complete command arguments and continuation decisions are known in advance; stop at every semantic dependency.
2. Cap batches at 10–15 commands and require a checkpoint between chunks, even when more commands are predictable.
3. Permit an explicit `--interactive-inspection` exemption in a runbook, with a reason recorded before the fifth call and reviewed in telemetry.

**Residual risk:** Medium. Some information value is unknowable until output arrives, so eligibility remains a judgment call.

## R2 — One bad command poisons later results

**Failure mode:** With `set -e`, one missing file aborts all later inspections. Without structured handling, continuing may mix stderr/stdout, hide failures, or let later steps consume invalid state. A pager, FIFO, binary file, huge glob, or hanging command can starve the batch.

**Detection signals:**

- Missing `BATCH_OK` or `BATCH_FAIL` footer.
- Two or more unexplained nonzero statuses.
- Unattributed stderr, timeout markers, or a single oversized section.

**Alternative mitigations:**

1. **Selected:** Use `set -u -o pipefail` without `set -e`; isolate commands, emit per-command markers and return codes, continue only independent blocks, and return nonzero aggregate status for unexpected failures.
2. Use fail-fast for the entire batch, but keep batches small and automatically create a follow-up batch for unexecuted commands.
3. Generate one script that launches independent inspections concurrently and collects each status separately; use only when output attribution and resource bounds are reliable.

**Residual risk:** Low–Medium. Continue-and-report preserves evidence but produces more output and requires correct wrapper logic.

## R3 — One wrong script scales an error across many targets

**Failure mode:** A command misclassified as read-only—such as `find -delete`, `sed -i`, `sort -o`, `tee`, or a write redirection—executes once against many targets before the agent sees any result. A quoting or path-generation error is amplified across the whole batch.

**Detection signals:**

- Write tokens or action flags in a declared inspection batch.
- Project/Git/system mtime changes during the batch window.
- Script exceeds the command-count or size bound.

**Alternative mitigations:**

1. **Selected:** Keep mutation classes out of batches; use quoted literal paths, one subshell per command, inline-visible script bodies, and a maximum of 15 commands.
2. Add a static validator with a narrow allowlist of executable-plus-option templates and reject any unparsed shell construct.
3. Run inspection scripts inside a read-only sandbox or mount namespace, with only the private `/tmp` workspace writable.

**Residual risk:** High under prompt-only classification; Low–Medium only after mechanical validation or a read-only sandbox exists.

## R4 — Reduced security and human review under `bypassPermissions`

**Failure mode:** Forty commands hidden behind `bash /tmp/script.sh` receive less scrutiny than forty visible calls. In this repository, several agents use `permissionMode: bypassPermissions` and may run unattended in the background, so approval prompts and pre-execution transcript review may not exist at all. Prompt injection or a mistaken generator can hide a write among routine reads. A related freshness-laundering error occurs when an agent treats batched `cat`/`sed -n` output as satisfying the separate tracked-`Read` requirement before an edit.

**Detection signals:**

- A batch executes an opaque pre-existing script whose body is absent from the tool input/transcript.
- Batching is enabled with no script-content audit under `bypassPermissions`.
- A batch contains a command never seen in the displayed script body.

**Alternative mitigations:**

1. **Selected:** Create and execute the script in one Bash call with a single-quoted heredoc so the complete body is visible; prohibit dynamic evaluation and broad wrapper allowlists.
2. Disable free-form batching under `bypassPermissions`; permit only fixed, mechanically validated read-only templates.
3. Log xtrace with line numbers to the private workspace, compare executed lines to the generated script, and retain the trace only when validation fails.

**Residual risk:** High for unattended or `bypassPermissions` agents until fixed templates, a mechanical validator, or a read-only sandbox gates execution. Visibility is post-hoc audit evidence, not human approval or a security boundary.

## R5 — Hidden state or data dependency

**Failure mode:** A separate Bash call starts with fresh shell state, while commands in one script share cwd, variables, aliases, traps, and process state. More importantly, a later target may depend on interpreting earlier output. The batch can therefore produce different evidence than the intended serial investigation.

**Detection signals:**

- Use of `cd`, `export`, `source`, `.`, `eval`, or cross-block variables.
- A later target, PID, host, revision, or path is parsed from earlier stdout.
- A sampled command produces different output when rerun independently under the same filesystem state.

**Alternative mitigations:**

1. **Selected:** Apply the three-question dependency test; run every command in its own subshell with explicit cwd and pre-resolved targets.
2. Add a static dataflow lint forbidding references to variables or files created by earlier blocks.
3. Allow only declarative batch manifests—argv arrays plus cwd/time/output limits—and let a trusted runner execute each item without shared shell state.

**Residual risk:** Low–Medium. Semantic dependency detection cannot be fully inferred by a simple hook.

## R6 — Whole-batch timeout or output truncation

**Failure mode:** A single recursive search, network command, log stream, or blocked reader can consume the outer Bash timeout. Completed output may be truncated, and all commands may need rerunning. One large combined result also creates a single context-window truncation cliff.

**Detection signals:**

- Outer timeout, signal termination, or missing final marker.
- Batch wall time exceeds 70% of its tool timeout.
- Output exceeds 100 KiB or a section lacks its terminal marker.

**Alternative mitigations:**

1. **Selected:** Exclude unbounded/network inspections; cap predicted runtime at 30 seconds, output at 100 KiB, commands at 15, and use per-command timeouts.
2. Write each completed section to a private result file and print a compact manifest; read selected files afterward.
3. Split by runtime class: fast metadata commands in one batch, potentially slow searches in individually timed calls or smaller batches.

**Residual risk:** Medium while bounds are predictions. It falls to Low only when aggregate/per-command deadlines and output caps are mechanically enforced and truncation is marked.

## R7 — Threshold gaming

**Failure mode:** An agent can split a five-command wave with narration or an unrelated tool call to stay below the threshold. An orchestrator can multiply the loophole by assigning four calls to each of several subagents. Conversely, it can pad a sequence to qualify for a less visible wrapper path. A numerical rule may optimize compliance appearance rather than latency or safety.

**Detection signals:**

- Repeated streaks ending at exactly four followed shortly by the same inspection objective.
- Spikes at the threshold or threshold plus one.
- Novel or write-capable commands appear only inside batches.

**Alternative mitigations:**

1. **Selected:** Define consecutiveness semantically; cosmetic narration/tool calls do not reset the policy, and individual and batch paths retain the same safety requirements.
2. Review whole tasklist/runbook waves rather than runtime streaks; flag five-plus separate eligible steps during generation.
3. Remove the fixed threshold after collecting data and use a cost rule: batch only when estimated saved round-trip time exceeds a configured minimum.

**Residual risk:** Medium. Runtime hooks observe events, not intent, so review and telemetry are still needed.

## R8 — Hook latency, false positives, and concurrency miscounts

**Failure mode:** A Bash-only PreToolUse hook cannot see intervening tools and overcounts. A match-all hook can add latency to every tool. Parallel Bash calls can look like a serial streak. A hard block may interrupt legitimate adaptive diagnosis and cost another 5–19 seconds.

**Detection signals:**

- p99 hook latency above 50 ms or timeout/error rate above 1%.
- Warning rate above 5% of streaks or 15% of Bash calls.
- Warning on same-turn parallel fan-out or on a sequence containing a real judgment boundary.

**Alternative mitigations:**

1. **Selected:** Start with prompt/tasklist policy; if needed, use a match-all, fail-open, advisory hook with session/agent-scoped locking, serial-turn debounce, and one warning per streak.
2. Use PostToolUse events to count only completed Bash calls and reset on every non-Bash event; accept delayed warning at the next boundary.
3. Keep enforcement entirely offline: analyze transcripts after sessions and improve tasklist/agent instructions rather than adding runtime hooks.

**Residual risk:** Medium for an advisory proxy because semantic false positives, batch-call counting, and same-turn concurrency remain unresolved. A local benchmark of the existing freshness-hook pattern averaged about 32 ms, negligible beside agent round trips; CPU latency is not the dominant concern.

## R9 — `/tmp` race, leakage, or orphaned artifacts

**Failure mode:** Predictable names in a shared `/tmp` allow symlink/name-squatting or replacement between write and execution. Scripts can leak paths, hostnames, revisions, or inspection intent. Forced termination can bypass cleanup. `noexec` mounts may also break direct execution.

**Detection signals:**

- Batch files not owned by the current UID, permissive modes, or predictable names.
- Batch directories older than the session or still present after normal completion.
- Script hash changes between creation and execution.

**Alternative mitigations:**

1. **Selected:** Secure unique directory, restrictive umask, create/write/run/cleanup in one call, execute via `bash <path>` rather than requiring executable `/tmp`, and remove only the exact private directory.
2. Avoid a durable script and feed a quoted script to `bash -s`; use only if the standing requirement for a generated `/tmp` script is relaxed.
3. Use a per-user runtime directory outside shared `/tmp`, with an age-bounded sweeper for crash leftovers.

**Residual risk:** Low on normal exit after `mktemp -d`, restrictive permissions, and same-call cleanup; Medium for forced-kill/host-loss paths until an ownership-checked, age-bounded sweeper exists.

## R10 — Wrapper permission rules become a universal bypass

**Failure mode:** The visible command becomes `bash /tmp/<name>`. If that wrapper is broadly allowlisted to reduce prompts, any command—including mutations that policy says must remain individual—can ride through it. The wrapper defeats prefix-based command rules and makes the inspection/mutation distinction honor-system only.

**Detection signals:**

- Permission entries matching broad `bash /tmp/*`, `bash -c`, or `sh *` wrappers.
- A batch contains `rm`, `mv`, `tee`, write redirection, `sed -i`, `curl -o`, Git mutation, or remote mutation.
- The script body is not present in the submitted Bash command.

**Alternative mitigations:**

1. **Selected:** Never allowlist a broad shell wrapper; inline the script body in the one tool call and preserve normal sandbox/hook controls.
2. Gate execution on a content hash produced by a fail-closed static validator that accepts only a narrow read-only grammar.
3. Replace shell scripts with a trusted batch-inspection runner that accepts structured argv/cwd entries and exposes no arbitrary shell evaluation.

**Residual risk:** Medium under prompt policy because a wrapper rule can still be added outside this document; Low only with a mechanical configuration gate plus validator or structured runner.

## Cross-risk decision

Three risks compose into the principal failure chain:

1. threshold gaming moves a command into the batch path (R7);
2. reduced visibility under `bypassPermissions` hides it (R4);
3. a broad wrapper rule lets it execute outside the intended review surface (R10).

Therefore the policy is sound only if the batch path is **never weaker than the individual path**. The initial proposal satisfies this procedurally by keeping script bodies inline, forbidding wrapper allowlisting, separating writes, and retaining existing controls. A future hard-enforcement implementation must validate script content mechanically before it can claim to close the residual security risk.
