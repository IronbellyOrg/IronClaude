# Bash Inspection Batching Policy

This is standing IronClaude behavioral guidance for main sessions, subagents,
tasklists, runbooks, and Sprint execution. It optimizes agent round trips; it is
not a security boundary and never overrides permission, sandbox, freshness, or
project-specific safety rules.

## Mandatory trigger

When a plan contains **five or more serial Bash inspections** whose targets and
arguments are already known, transfer the eligible inspections to one generated
script under `/tmp` and create, execute, report, and clean it up in **one Bash
tool call**.

Apply the rule prospectively, before the first known call. If the fifth call is
discovered legitimately in flight, batch the remaining work only when at least
two eligible inspections remain; do not rerun completed work to manufacture a
batch. Apply the threshold to the whole planned wave before delegating—splitting
four calls across several subagents is not an exemption.

Same-turn parallel tool calls are exempt because they already avoid serial model
round trips. Prefer dedicated Read, search, MCP, or parallel tools when they
provide structured output or tracked freshness.

## Eligibility

A Bash inspection is eligible only when all are true:

1. It is read-only in effect, including every option, pipeline stage, redirect,
   subprocess, and remote effect.
2. Its complete command, literal target, and acceptable outcomes are known
   before execution.
3. Earlier output cannot change whether it runs or what it targets, except for a
   predetermined mechanical guard such as inspect-if-present.
4. Runtime and output are bounded.
5. It requires no prompt, pager, credential exchange, elevation, or agent
   interpretation before the next command.

A judgment boundary ends the batch candidate even when the next command is
read-only. Separate subshells prevent shell-state leakage but do not provide a
filesystem or service snapshot; revalidate consequential facts after concurrent
changes.

## Never batch as routine inspection

Keep these as individual, reviewed calls:

- edits, formatters, mutations, installs, service/database/deployment actions;
- Git or GitHub mutations, file deletion/moves/copies, permission changes;
- write redirection, `tee`, heredocs outside the private batch workspace;
- write-capable options such as `find -delete`, `sed -i`, `sort -o`, `curl -o`,
  extraction, synchronization, apply, or install subcommands;
- interpreters, nested shells, dynamic variables, command/process substitution,
  sourced or generated shell;
- tests/builds that create caches, artifacts, fixtures, or external state;
- network, remote-host, recursive-filesystem, or streaming-log work;
- commands whose next target depends on interpreting prior output.

For unattended or `bypassPermissions` execution without a mechanical validator
or read-only sandbox, use only simple fixed read commands with literal quoted
arguments—no pipelines, functions, aliases, interpreters, substitutions, or
nested shell. If a command cannot fit that subset, keep it individual.

## Batch contract

- Set `umask 077` and use `mktemp -d /tmp/ironclaude-batch.XXXXXXXX`.
- Put one visible, single-quoted-heredoc script in the private directory per
  bounded chunk. Never execute an opaque pre-existing script or allowlist broad
  wrappers such as `bash /tmp/*`, `bash -c`, or `sh *`.
- Limit each chunk to 15 commands, 30 seconds aggregate runtime, and 100 KiB
  emitted output. Enforce per-command and aggregate timeouts; capture and bound
  each command's output. Inspect the footer before starting another chunk.
- Use `set -u -o pipefail`, not blanket `set -e`. Run commands in isolated
  blocks and attribute stdout/stderr to each block.
- Emit `BEGIN <id>` followed by exactly one of `OK`, `NO_MATCH`, `SKIP`, `FAIL`,
  `TIMEOUT`, `SIGNAL`, or `TRUNCATED` with the command ID and status details.
- `SKIP` and declared `NO_MATCH` are non-failures. `FAIL`, `TIMEOUT`, `SIGNAL`,
  `TRUNCATED`, missing markers, and cleanup failure make the aggregate fail.
- Print `BATCH_OK failures=0` and exit 0, or `BATCH_FAIL failures=<n>` and exit
  nonzero after cleanup status is included.
- Install an exit/signal cleanup trap and remove only the exact private
  directory. If cleanup fails, emit `CLEANUP_FAIL path=<exact-path>` and fail.
  `SIGKILL` or host loss may leave an orphan; do not claim otherwise.

## Freshness and enforcement

Bash output from `cat`, `sed -n`, `grep`, or the batch script does **not** count
as a tracked Read for freshness-before-edit. Use the required Read mechanism
before a later edit.

This policy is normative prompt/tasklist guidance. It does not mechanically
prove that a script is read-only. Do not add a hard fifth-call counter: a counter
cannot infer eligibility, known paths, semantic dependencies, or safe review.
