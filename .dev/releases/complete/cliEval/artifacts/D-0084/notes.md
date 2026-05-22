# D-0084 — Design notes

## Why `codebase-retrieval` and not another `mcp__auggie__` tool

`mcp__auggie__` exposes `codebase-retrieval` as its primary read-only
context-engine tool in the v1 IronClaude inventory. It returns
deterministic, side-effect-free results when invoked against a fixed
working directory (the per-eval HOME via FR-ISO2) and is cheap.

Other tools under the same prefix would either mutate state or
introduce LLM-side variability that would degrade 3-run determinism
(D-0082 §2.2). The eval only needs the PostToolUse hook to fire under
the `mcp__auggie__*` matcher branch — `codebase-retrieval` satisfies
that with the smallest deterministic footprint.

## Two-assertion shape ({event, tool}) vs. one ({event})

The minimal "did the matcher fire" assertion is just
`'"event":"sticky_cleared"'` — same byte-stream as E1. But that
assertion is **branch-agnostic**: any of the three matcher prefixes
emits the same `event:sticky_cleared` line. Without the second
assertion, the manifest would not distinguish E2.1 / E2.2 / E2.3 at
runtime, defeating the matcher-coverage purpose of the triad.

The hook script (line 28 of `auggie-flag-clear.sh`) embeds the
matched tool name in the JSONL line as `"tool":"<TOOL_NAME>"`. E2.1
asserts the *specific* prefix value
(`mcp__auggie__codebase-retrieval`) to pin the matcher branch. This
is the contract D-0085 / D-0086 carry forward (each pinning its own
prefix).

## Why E2.1 exists alongside E1 (both cover `mcp__auggie__`)

E1 and E2.1 both register as covering `mcp__auggie__.*` per
`coverage-map.txt`. The distinction is intent, not redundancy:

| Eval | Category | Purpose |
|---|---|---|
| E1 | `hook-lifecycle` | "Set → clear" lifecycle proof — exercises the full sticky lifecycle including the file-state precondition. |
| E2.1 | `hook-coverage` | Matcher-branch coverage proof — pins the `mcp__auggie__` regex branch via the `tool` field substring. |

E1 only asserts `sticky_cleared` (branch-agnostic). E2.1 asserts
`sticky_cleared` AND the `tool=mcp__auggie__codebase-retrieval`
substring. The category split (`hook-lifecycle` vs. `hook-coverage`)
also lets the matcher-coverage gate enumerate the E2 triad as a
unit when validating that all three v1 matcher branches are
exercised.

## Why a literal contains substring, not a JSONL field equality

`Expect.jsonl` would let us assert a structural predicate
(e.g. `tool == "mcp__auggie__codebase-retrieval"`) but only via Python
callables (`expect.py:269-369`). Those have no YAML wire form, so
declaring them in `real.yaml` would either require a `callback:`
escape hatch (D-4, deferred) or a v2 declarative DSL extension.

For the v1 manifest the substring
`'"tool":"mcp__auggie__codebase-retrieval"'` is uniquely identifying
within `logs/auggie-first.jsonl`:

- the JSONL printf format is fixed in the hook script
  (`{"ts":...,"session_id":...,"event":"sticky_cleared","tool":"%s"}`);
- the `"tool":"…"` key only ever appears in `sticky_cleared` events;
- the substring includes the leading `"tool":"` so it cannot collide
  with any future `"some_field":"…codebase-retrieval"` line.

If the hook is later extended to emit additional event types that
incidentally use the `"tool":"…"` shape with the same suffix, this
substring assertion would need to tighten — flagged as
risk-low / followup-only.

## Why the prompt explicitly names the MCP tool

`inputs[0].prompt` is an English instruction to the Claude subprocess.
The chosen prompt — `"Use mcp__auggie__codebase-retrieval to
summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."`
— explicitly names the MCP tool. Reasoning:

- The subprocess is biased toward the named tool (vs. picking
  `mcp__auggie-mcp__ask_question` or another close substitute).
- The eval exercises *that* tool specifically, so a mis-pick would
  silently degrade coverage signal.
- It documents intent to a human reader of the manifest.
- The PTY-driver wiring (downstream task) will feed this string
  verbatim, so the eval is self-describing.

`expect_tool_call` is the coverage-gate-consumed field; the prompt
text itself is non-load-bearing as long as it biases toward the named
tool.

## Why E2.1 keeps `requires: [mcp_server.auggie]` despite `no_pty: skip`

Same independence rationale as D-0083 §"Why E1 keeps `requires`":

- `requires` + `optional_capabilities` → FR-CAP1 (MCP server present?)
- `no_pty: skip` → R-077 (PTY harness usable?)

The two gates fire independently. Removing the capability tag would
break the `--no-mcp` soft-skip behavior under §5 of `spec.md`. A run
with `--no-mcp` but not `--no-pty` still skips E2.1 via the
capability gate (correct). A run with `--no-pty` but not `--no-mcp`
skips E2.1 via the PTY gate (also correct — every body in the "real"
suite drives a PTY).

## Why a static row, not a `parameterize:` block

D-0082 §3 frames E2 conceptually as a parameterize over the three
matcher prefixes, but the manifest splits the row into three static
entries (E2.1 / E2.2 / E2.3). Reasoning:

1. **Per-entry `requires:` capability tags differ** — FR-CAP1
   (D-0082 §6) requires each prefix's matching server to gate
   independently (`mcp_server.auggie`, `mcp_server.auggie-mcp`,
   `mcp_server.airis-mcp-gateway`). A single parameterize block
   cannot carry three different `requires:` lists.
2. **No runtime template-substitution layer** — `loader._expand_entry`
   (loader.py:600 docstring) does not perform `{{prefix}}` token
   substitution against the inputs/expects strings; rolling parameter
   values into the prompt and the `contains` substring would require
   a template-pass that doesn't exist in v1.

Both constraints push the triad to three static rows. The static
shape also makes `eval describe --eval E2.1` work without
expansion-time surprises.

## Determinism

The body is deterministic in the "passes/fails the same way every
run on a clean per-eval HOME" sense:

- the prompt is static, so the subprocess's tool pick is stable;
- the hook's `sticky_cleared` event + `tool` field is the same every
  run when the sticky pre-existed;
- the JSONL byte-stream is fresh per-eval (HomeIsolation, FR-ISO2);
- the `ts` timestamp on the JSONL line varies but is not asserted
  against.

3-run determinism is the per-task acceptance criterion (D-0082 §2.2)
and the body shape carries no inputs that would introduce variance.
