# Bash Inspection Batching Policy

**Status:** Proposed normative guidance; not mechanically enforced until wired into active agent/tasklist sources
**Date:** 2026-09-17
**Decision:** Set `N = 4`; the mandatory trigger is **more than four serial, eligible Bash commands**, so a known sequence of five or more must be batched. Same-turn parallel tool calls are exempt because they already consume one model round trip.

## Standing rule

> When an agent's tasklist, runbook, plan, or in-flight sequence calls for **more than four serial eligible Bash commands against known paths**, the agent MUST transfer those commands to a generated batch script under `/tmp` and create, execute, and clean up that script in **one Bash tool call**. The agent MUST NOT batch mutations, interactive steps, or commands whose arguments or continued execution require interpretation of earlier output.

This is a latency-optimization rule subordinate to security, data safety, freshness, and correctness—not a security mechanism. It does not turn an unsafe command into a safe one and must never be used to bypass a denied permission or hook. `MUST` is normative guidance: until a validator or read-only sandbox exists, compliance depends on agent/tasklist review and must not be represented as mechanical enforcement.

## Why `N = 4`

The incident establishes that shell execution was not the bottleneck:

- 20 read-only inspections consumed about 112 seconds of agent round trips: **5.6 seconds per call**.
- Replaying the same inspections as one script took **0.048 seconds total**, or about **2.4 ms per inspection**.
- At the stated 5–19 second round-trip range, replacing five separate calls with one saves roughly **20–76 seconds**, before script-composition cost.
- For the 20-call incident, batching from the start would remove approximately 19 round trips: about **106 seconds** at the measured 5.6-second average.

A sample of the newest 45 project transcripts available during this analysis (2026-09-16 17:25 through 2026-09-17 22:56; IronClaude, IronOps, and InfraDocs) contained 322 Bash events in 184 **mechanical** streaks, where any non-Bash tool event ended a streak. About 97% were length 1–4; only 5–6 streaks crossed length four, while those long streaks contained about 20% of Bash events. Four is therefore a provisional observed elbow for runtime telemetry: it preserves short adaptive investigations and catches the long, expensive tail. A threshold of two would affect about 12% of streaks, including many legitimate three-step probes.

The policy's semantic inspection wave is intentionally broader than that mechanical transcript metric: cosmetic narration or a tool switch does not excuse a known five-command plan. Consequently, the sample supports `N = 4` as a starting threshold, not a proven optimum or a direct measurement of semantic-policy violations. The mathematical break-even is normally two or three commands, but wall-clock break-even alone ignores interactivity, script-review cost, and false positives. Agents MAY voluntarily batch two to four only when the same safety contract applies.

## Definitions

### Consecutive

A serial inspection wave in which each Bash call would otherwise require a new agent round trip and no genuine agent judgment, user decision, or mutation must occur between commands. Narration, a cosmetic tool switch, or splitting one command into equivalent fragments does not reset the semantic sequence. Bash calls submitted together as one same-turn parallel tool batch are exempt: they already avoid serial round trips and forcing them through a shell script adds risk without latency benefit.

### Known paths

Every target path and command scope can be written before the batch starts. A path is not known when it must be selected, discovered, or judged from earlier output.

### Eligible Bash command

A command is eligible only when all are true:

1. It is read-only in effect, including its options, redirections, subprocesses, and remote effects.
2. Its arguments and target paths are known before execution.
3. Its result cannot change whether or how another command in the same batch should run, except for an explicit mechanical guard such as `test -e` followed by inspect-or-skip.
4. It is bounded in expected runtime and output.
5. It requires no interactive input, pager, prompt, credential exchange, or permission escalation.
6. It does not weaken or bypass a freshness, permission, sandbox, or review control.

### Judgment boundary

A point at which an agent must inspect output and decide the next action. A judgment boundary ends the current batch candidate even when the next command is read-only.

## Trigger semantics

### Planned sequences

If five or more eligible calls are foreseeable, batch them **before the first call**. Do not spend four calls and wait for the fifth-call hook warning.

### In-flight sequences

If the fifth eligible call becomes foreseeable only after execution has started, batch the fifth and all remaining eligible commands **when at least two eligible calls remain**. If legitimate new information reveals only a singleton fifth call, run it separately and record that the remaining sequence was below batch break-even. Do not rerun the first four merely to manufacture a batch. If the five-call sequence was already known at the outset, late recognition is a policy violation and the singleton exception does not apply.

### Sequence reset

A sequence resets only at a real boundary:

- agent interpretation of output before deciding the next action, whether or not the eventual plan changes;
- user input or approval;
- a write, mutation, or interactive command kept outside the batch;
- a state change that invalidates the remaining inspections;
- a required checkpoint between bounded batch chunks; or
- completion of the inspection wave.

A non-Bash tool call resets a mechanical counter but does not excuse threshold gaming when it is inserted only to split an otherwise known Bash sequence.

## Read/write separation

### Freely batchable when otherwise eligible

Typical examples include:

- `grep` or equivalent bounded searches;
- `sed -n`;
- `git diff`, `git show`, `git log`, `git status`;
- `ls` and bounded `find` without action options;
- `cat` of known, regular, size-bounded text files;
- `stat`, `wc`, `file`, and checksums;
- independent existence or metadata checks.

Dedicated `Read`, search, MCP, and parallel tool calls remain preferred when they provide better structure, freshness tracking, or same-turn parallelism. This policy does not force work into Bash.

### Never batch as inspection work

Keep these as individually reviewed agent calls:

- `sed -i`, formatters, or any in-place edit;
- `git merge`, `add`, `commit`, `push`, `reset`, checkout/switch, or branch mutation;
- `gh` mutations;
- `rm`, `mv`, `cp` to project or system paths, permission/ownership changes;
- installs, service restarts, deployments, database changes, or remote mutations;
- output redirection, `tee`, or heredocs that write anywhere except the private `/tmp` batch workspace;
- write-capable options such as `find -delete`, `sort -o`, `curl -o`, archive extraction, synchronization, raw-device writes, or apply/install subcommands;
- general interpreters or build tools (`python -c`, `sh -c`, `make`, package scripts, and equivalents) unless a mechanical validator can prove the complete payload is read-only;
- tests/builds that create caches, artifacts, fixtures, snapshots, or external state;
- network, remote-host, recursive filesystem, and streaming-log commands, even when they appear bounded; keep these individual or place them in a separately reviewed purpose-built batch;
- any command requiring interactive input or agent interpretation before the next step.

Pipes are not automatically mutating, but every stage must be read-only. `| tee`, output redirection, command substitution, process substitution, dynamic evaluation, and write-capable downstream stages make the command ineligible. Fixed literal arguments are required; neither quoted nor unquoted `$(...)` is allowed.

### Housekeeping exception

Creating the private script and its temporary diagnostic files under its own `/tmp` directory is the sole routine write allowed in an inspection batch. This exception never extends to project, user, service, Git, or remote state.

## State-dependency detection rule

For every candidate command, answer:

1. Can its complete arguments, target, and acceptable outcomes be specified now?
2. Could any earlier command's output change whether it should run or what it should target?
3. If yes, is that dependency a predetermined mechanical guard with no interpretation?

If answer 1 is **no**, or answer 2 is **yes** and answer 3 is **no**, the command starts a new wave after an agent checkpoint and MUST NOT be included in the current batch.

Allowed mechanical dependency:

- If a known file exists, print a bounded excerpt; otherwise emit a `SKIP` marker.

Disallowed semantic dependency:

- Search for a deployment name, select the suspicious result, then inspect that deployment.
- Read a diff, decide which caller is risky, then inspect that caller.
- Discover a credential, PID, host, branch, or path and interpolate it into later commands.

Each command runs in its own subshell with an explicit working directory and absolute or pre-resolved targets. Do not rely on `cd`, `export`, aliases, shell variables, or side effects from another block. Subshell isolation does not provide a filesystem or service snapshot: if concurrent state changes could alter a consequential conclusion, keep the inspections individual or revalidate the decisive fact immediately at the next judgment boundary.

## Batch-script contract

### Location and lifecycle

1. Set `umask 077` and create a unique private directory with `mktemp -d /tmp/ironclaude-batch.XXXXXXXX`; predictable PID-based names are forbidden.
2. Generate exactly one task-scoped script **per bounded chunk** in that directory. A wave above 15 commands becomes multiple Bash calls, with an agent checkpoint between chunks.
3. In the same Bash tool call: create the directory, install an exit/signal cleanup trap, write the script with a single-quoted heredoc, run it with `bash`, capture its aggregate status, remove the private directory, and return the aggregate status.
4. Keep the full script body visible in the Bash tool input. Do not execute an opaque pre-existing `/tmp` script.
5. Never use a predictable shared filename and never allowlist broad wrappers such as `bash /tmp/*`, `bash -c`, or `sh *`.
6. Cleanup removes only the directory created by that invocation. No broad `/tmp` deletion is permitted. If cleanup fails, emit `CLEANUP_FAIL path=<exact-path>` and return nonzero even when inspections succeeded.
7. `EXIT`/signal traps do not survive `SIGKILL` or host loss. Such a kill may leave an orphan. This proposal does not claim automatic crash cleanup; an implementation that needs that guarantee must add a separately reviewed, ownership-checked, age-bounded sweeper for the exact `ironclaude-batch.*` namespace.

### Size and timeout bounds

Split a batch at the earliest applicable limit:

- maximum **15 commands** per script;
- enforced aggregate runtime of **30 seconds** per chunk;
- enforced aggregate emitted output of **100 KiB**, with a per-command capture/truncation budget and an explicit `TRUNCATED <id> bytes=<n>` marker;
- any network, remote, recursive, log-stream, or otherwise unbounded inspection;
- any judgment boundary.

Use `timeout` for every command and for the aggregate script; do not merely predict the deadline and do not raise it to make a larger batch fit. Capture each block's output in the private workspace, measure it, then emit only the bounded portion so a chatty command cannot consume later sections. A timeout, truncation, signal exit, or missing final marker means incomplete/unknown, not success. After a size-triggered chunk, the agent MUST inspect the footer before starting the next chunk.

### Failure reporting

Independent inspection batches use continue-and-report semantics:

- top level: `set -u -o pipefail`, **not** `set -e`;
- each command runs in an isolated block/subshell;
- every block emits `BEGIN <id>` and exactly one terminal marker:
  - `OK <id> rc=0`
  - `NO_MATCH <id> rc=1` for an explicitly declared search-no-result outcome
  - `FAIL <id> rc=<n>`
  - `SKIP <id> reason=<reason>`
  - `TIMEOUT <id> rc=124`
  - `SIGNAL <id> rc=<128+n>` when the wrapper observes signal termination
- expected nonzero statuses are mapped to a named success-class marker such as `NO_MATCH`, never hidden with unconditional `|| true`;
- `SKIP` and declared `NO_MATCH` do not increment the failure count; `FAIL`, `TIMEOUT`, `SIGNAL`, `TRUNCATED`, missing markers, and cleanup failure do;
- stderr remains attributable to its command;
- dependent mechanical checks skip their dependent block after failure;
- independent blocks may continue;
- the script prints `BATCH_OK failures=0` and explicitly `exit 0`, or prints `BATCH_FAIL failures=<n>` and explicitly `exit 1` after cleanup status has been incorporated.

One failure must neither silently poison later results nor erase independent evidence. Fail-fast is reserved for setup/integrity failure—failure to create the private directory, write the exact script, or establish cleanup—not for an ordinary missing inspection target.

## Security and review under `bypassPermissions`

This repository commonly runs unattended agents with `permissionMode: bypassPermissions`; therefore human approval prompts and transcript visibility are not dependable pre-execution controls. Inline visibility is retained for audit, but it is not described as approval or enforcement.

Until a mechanical validator or read-only sandbox exists, unattended/bypass batches are restricted to a **simple-command subset**: fixed read-only executables from the eligible list, literal quoted arguments, no pipelines, functions, aliases, interpreters, substitutions, dynamic variables, sourced content, or nested shell. If an inspection cannot fit that subset, keep it as an individual call. The policy also requires:

- script body visible inline in the tool call and transcript for post-hoc audit;
- read-only effect classification of the full command, not merely its leading executable;
- no broad wrapper permission rule;
- batch limits, enforced deadlines/output caps, and per-command markers;
- no downgrade of existing sandbox, hook, or freshness requirements.

A Bash batch does not count as a tracked `Read` for the freshness-before-edit rule unless the actual freshness system explicitly records it. Before a later edit, use the required `Read` mechanism even if `cat`, `sed -n`, or `grep` already displayed the file. Orchestrators must apply `N = 4` to the whole planned inspection wave before delegation; distributing four calls to each of several subagents is threshold gaming, not compliance.

## Enforcement decision

### Adopt first as normative guidance, not a mechanical gate

This artifact is a proposal and does not itself alter active agents. Adoption requires adding the rule to the appropriate source-of-truth agent guidance and tasklist/runbook generators under `src/superclaude/`, then syncing by the repository's normal process. Those surfaces can reason prospectively about a whole plan and should flag five-plus eligible calls written as separate steps, but they remain prompt-policy controls. They MUST NOT be described as a security boundary or automatic enforcement.

### Optional next step: advisory counter hook

A PreToolUse hook may measure likely violations, but it cannot fully enforce this policy:

- it sees calls as they occur, not the agent's future plan;
- a counter cannot prove that a command is read-only, independent, or against a known path;
- a Bash-only matcher cannot observe intervening non-Bash calls and therefore cannot establish consecutiveness;
- a hard block at call five adds another agent round trip and may pressure agents into unsafe batches;
- parallel same-turn Bash calls can look consecutive unless debounced.

If telemetry shows material noncompliance, add an **advisory, fail-open proxy** patterned after the existing freshness hooks:

1. Use PostToolUse(Bash) or another completion event to increment only completed Bash calls; PreToolUse alone cannot know completion.
2. Observe non-Bash tool events to reset the **mechanical** streak; maintain separate session/agent state with locking and explicitly label the metric as a proxy for the broader semantic wave.
3. Exclude recognized policy-generated batch invocations where possible; otherwise record them separately so a compliant batch does not look like the fifth isolated call.
4. Debounce same-turn parallel fan-out and never label it a violation.
5. At the attempted fifth isolated call, emit at most one informational reminder per mechanical streak and still allow execution. It is not proof that the command is eligible or that a violation occurred.
6. Never rewrite, combine, classify, or execute commands.
7. Keep a one-second hook timeout and fail open on malformed input, missing identity, lock failure, or corrupt state.
8. Record only metadata needed for measurement; do not log full command bodies.

A local benchmark of the existing `freshness-pre-edit.sh` pattern ran 100 invocations in 3.209 seconds, about **32 ms each**. That is approximately 0.6% of the incident's 5.6-second average round trip and operationally negligible. The harder problem is semantic false positives, not hook CPU time.

### Do not adopt: hard-blocking counter

A hard counter would enforce a number rather than the policy. It cannot recognize legitimate adaptive loops, cannot prove safety of a generated script, and would turn a warning into another expensive round trip. Hard blocking requires a real shell parser/validator and evidence from an advisory rollout; it is not justified by current data.

## Rollout and validation

1. **Policy phase:** wire the guidance into active source-of-truth agent and tasklist instructions. Audit long Bash waves for two weeks or at least 20 sessions.
2. **Telemetry phase, if needed:** run an advisory hook silently first, then remind once per qualifying mechanical streak.
3. Measure two distinct populations: mechanical runtime streaks from telemetry and semantic five-plus waves found by tasklist/transcript review. Never use one as if it measured the other.
4. Keep `N = 4` when:
   - fewer than 5% of mechanical Bash streaks trigger;
   - median estimated savings among triggered streaks is at least 30 seconds;
   - hook p99 remains below 50 ms;
   - fewer than 40% of reminders are ignored after 20 reminders;
   - no increase appears in failed, timed-out, truncated, or rerun inspections.
5. Reconsider the threshold or enforcement when reminders exceed 15% of Bash calls, p99 exceeds 100 ms, or batching makes inspection-heavy sessions slower.
6. Do not move to hard blocking merely because reminders are ignored; first determine whether they are false positives, compliant batch calls, write boundaries, parallel fan-out, or legitimate judgment boundaries.

## Compliance examples

**Compliant:** A plan has eight known, independent `git show`, `git diff`, and bounded text inspections. Generate one sectioned `/tmp` script and execute it in one Bash call.

**Compliant:** Three adaptive diagnostic commands are run separately because each next target depends on interpreting the prior output. The threshold is not reached and the commands are ineligible anyway.

**Compliant:** Six inspections are known, but one is an unbounded network call. Batch the five bounded local reads and run the network inspection separately.

**Violation:** Five `git show` calls against known revisions are issued serially because the agent inserts narration between them.

**Violation:** An agent puts `git add` or `sed -i` into an inspection script to save a round trip.

**Violation:** A tasklist describes five separate read-only Bash verification steps against already-known paths instead of one batch step.

**Violation:** A script discovers filenames in step one and interpolates them into shell commands in later steps without returning to the agent for interpretation.
