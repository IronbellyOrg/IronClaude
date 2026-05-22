# D-0083 — Design notes

## Why the JSONL `contains` proxy beats a literal `file_absent`

The cleanest verifier-side wording for the lifecycle would be "sticky
file existed pre-call AND is absent post-call". But neither half is
directly expressible today:

1. **Pre-call snapshot** — the runner only invokes `expects[]` after
   the subprocess has exited (`runner.py` step 6 of 7). There is no
   "freeze FS at t=spawn" primitive.
2. **Post-call file path** — the path contains the orchestrator-allocated
   `session_id`, which is not known at YAML-author time. The loader
   does not template-substitute `{session_id}` against
   `EvalContext.home_isolation.session_id`.

The `auggie-flag-clear.sh` hook, by its `if [ -f "$STICKY" ]` guard,
collapses the two-step assertion into one **observable outcome**: the
`sticky_cleared` JSONL line is emitted IFF the lifecycle ran. Because
the JSONL path (`logs/auggie-first.jsonl`) is fixed (not
session-templated), `Expect.file(contains='"event":"sticky_cleared"')`
covers the entire contract under the current primitive surface.

## Why `Expect.file` and not `Expect.jsonl` for the event predicate

`Expect.jsonl` requires `assert_each` or `assert_any` predicates as
Python callables (`expect.py:275-276`). These have no YAML wire form
and would need either a `callback:` escape hatch (D-4) or a v2
declarative DSL extension. Pushing E1 onto either of those would
either delay the eval until a v2 DSL ships or bloat the suite with a
callback module for a tautological substring check.

The substring `'"event":"sticky_cleared"'` is uniquely identifying
within `logs/auggie-first.jsonl` (the hook script's only event type
in v1) and the JSONL byte-stream is a clean text file, so
`Expect.file` is the v1-correct primitive choice. If the hook is
extended in a later release to emit additional event types that
incidentally contain the substring `sticky_cleared`, this would need
a tightening pass — flagged as risk-low / followup-only.

## Why a concrete prompt string and not a placeholder

`inputs[0].prompt` is presented as a real English instruction
("Use mcp__auggie__codebase-retrieval to summarise the
auggie-flag-clear hook in src/superclaude/hooks/scripts/.") rather
than a placeholder, because:

- The PTY-driver wiring will eventually feed this string verbatim to
  the Claude subprocess.
- The chosen instruction biases the subprocess toward calling the
  named MCP tool, which is what the eval exercises.
- It documents intent to a human reader of the manifest.

The exact wording is non-load-bearing: any prompt that biases the
subprocess to call `mcp__auggie__codebase-retrieval` exactly once
will satisfy the eval. The `expect_tool_call` field is what the
coverage gate consumes.

## Why E1 keeps `requires: [mcp_server.auggie]` despite `no_pty: skip`

The two flags gate independent dimensions:

- `requires` + `optional_capabilities` → FR-CAP1 (MCP server present?)
- `no_pty: skip` → R-077 (PTY harness usable?)

A run with `--no-mcp` but not `--no-pty` still skips E1 via the
capability gate (correct). A run with `--no-pty` but not `--no-mcp`
skips E1 via the PTY gate (also correct — every body in the "real"
suite drives a PTY). Both gates can fire independently; FR-CAP1 must
not be removed just because `no_pty: skip` happens to cover the
common case.

## Determinism

The body is deterministic in the "passes/fails the same way every
run on a clean per-eval HOME" sense:

- the auggie tool call is the same every run (prompt is static);
- the hook's `sticky_cleared` event is the same every run when the
  sticky pre-existed;
- the JSONL byte-stream is fresh per-eval (HomeIsolation, FR-ISO2);
- the timestamp on the JSONL line varies but is not asserted against.

3-run determinism is the per-task acceptance criterion (D-0082 §2.2).
