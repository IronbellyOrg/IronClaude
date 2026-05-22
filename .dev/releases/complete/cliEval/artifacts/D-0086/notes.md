# D-0086 — Design notes

## Why `auggie_search` and not another gateway tool

`mcp__airis-mcp-gateway__` is a wrapper gateway that proxies many MCP
tool families (tavily, context7, sequential, magic, etc.) plus
gateway-native endpoints. Only the `auggie_*`-prefixed tools fire the
PostToolUse matcher branch under analysis here:

| Candidate tool | Side effects | Fires `auggie_.*` branch? | Fit |
|---|---|---|---|
| `auggie_search` | Read-only codebase-retrieval proxy. | ✅ matches `mcp__airis-mcp-gateway__auggie_.*` | ✅ Deterministic, fast, no scratch state. |
| `auggie_history` | Writes session marks. | ✅ | ❌ Mutates state. |
| `tavily_search` | Web search (read-only). | ❌ — name lacks `auggie_` literal | ❌ Wrong matcher branch. |
| `context7_get-library-docs` | Doc retrieval (read-only). | ❌ | ❌ Wrong matcher branch. |

The matcher's trailing `auggie_*` literal is the load-bearing
constraint — the eval would silently degrade to "no coverage" if a
sibling `mcp__airis-mcp-gateway__tavily_search` were chosen, because
the case-arm in `auggie-flag-clear.sh:23` would not match and no
JSONL event would be emitted. `auggie_search` is the unique
read-only / side-effect-free choice that pins the matcher branch.

## Two-assertion shape ({event, tool}) vs. one ({event})

The minimal "did the matcher fire" assertion is just
`'"event":"sticky_cleared"'` — same byte-stream as E1 / E2.1 / E2.2.
But that assertion is **branch-agnostic**: any of the three matcher
prefixes emits the same `event:sticky_cleared` line. Without the
second assertion, the manifest would not distinguish E2.1 / E2.2 /
E2.3 at runtime, defeating the matcher-coverage purpose of the
triad.

The hook script (line 28 of `auggie-flag-clear.sh`) embeds the
matched tool name in the JSONL line as `"tool":"<TOOL_NAME>"`. We
assert the *specific* prefix value
(`mcp__airis-mcp-gateway__auggie_search`) to pin the matcher branch,
which is the contract D-0084 §2 established for the triad.

## Why a literal contains substring, not a JSONL field equality

`Expect.jsonl` would let us assert a structural predicate
(e.g. `tool == "mcp__airis-mcp-gateway__auggie_search"`) but only via
Python callables (`expect.py:269-369`). Those have no YAML wire form,
so declaring them in `real.yaml` would either require a `callback:`
escape hatch (D-4, deferred) or a v2 declarative DSL extension.

For the v1 manifest the substring
`'"tool":"mcp__airis-mcp-gateway__auggie_search"'` is uniquely
identifying within `logs/auggie-first.jsonl`:

- the JSONL printf format is fixed in the hook script
  (`{"ts":...,"session_id":...,"event":"sticky_cleared","tool":"%s"}`);
- the `"tool":"…"` key only ever appears in `sticky_cleared` events;
- the substring includes the leading `"tool":"` so it cannot collide
  with any future `"some_field":"…auggie_search"` line.

If the hook is later extended to emit additional event types that
incidentally use the `"tool":"…"` shape with the same suffix, this
substring assertion would need to tighten — flagged as
risk-low / followup-only (same shape as the D-0083 / D-0085 followup).

## Why the prompt explicitly names the MCP tool

`inputs[0].prompt` is an English instruction to the Claude subprocess.
The chosen prompt — `"Use mcp__airis-mcp-gateway__auggie_search to
summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."`
— explicitly names the MCP tool. Reasoning:

- The subprocess is biased toward the named tool (vs. picking
  `mcp__auggie__codebase-retrieval` or `tavily-search` — both would
  satisfy the user-intent of "summarise" but fail to fire the
  gateway-prefixed matcher branch).
- The eval exercises *that* tool specifically, so a mis-pick would
  silently degrade coverage signal.
- It documents intent to a human reader of the manifest.
- The PTY-driver wiring (downstream task) will feed this string
  verbatim, so the eval is self-describing.

`expect_tool_call` is the coverage-gate-consumed field; the prompt
text itself is non-load-bearing as long as it biases toward the named
tool.

## Why E2.3 keeps `requires: [mcp_server.airis-mcp-gateway]` despite `no_pty: skip`

Same independence rationale as D-0083 §"Why E1 keeps `requires`" /
D-0085 §"Why E2.2 keeps `requires`":

- `requires` + `optional_capabilities` → FR-CAP1 (MCP server present?)
- `no_pty: skip` → R-077 (PTY harness usable?)

The two gates fire independently. Removing the capability tag would
break the `--no-mcp` soft-skip behavior under §5 of `spec.md`.

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

## Completing the v1 matcher-coverage triad

D-0082 §3 enumerates exactly three v1 matcher prefixes in
`auggie-flag-clear.sh`:

1. `mcp__auggie__*` — covered by E2.1 / D-0084
2. `mcp__auggie-mcp__*` — covered by E2.2 / D-0085
3. `mcp__airis-mcp-gateway__auggie_*` — covered by E2.3 / D-0086 (this)

With D-0086 landed, the coverage-map enumeration shows all three
matcher branches have at least one covering eval. The CP-P05-T01-T05
checkpoint (T05.06) verifies this triad collectively — and the
roadmap-recorded "Matcher coverage gate (T04.14) recognises all 3 v1
matchers (`auggie`, `auggie-mcp`, `airis-mcp-gateway`)" exit
criterion is met by the post-T05.05 manifest state.

## Open question for downstream wiring (not blocking T05.05)

The `mcp__airis-mcp-gateway__` server is a separate MCP server
registration from `mcp__auggie__` and `mcp__auggie-mcp__`. Whether
`mcp_server.airis-mcp-gateway` is a distinct capability tag at
runtime (vs. being satisfied transitively because the gateway proxies
both auggie servers) is decided in the FR-CAP1 implementation under
`commands.py`. The manifest treats them as distinct so the per-eval
skip semantics match D-0082 §2 constraint 5 even if a future
consolidation makes them aliases. No action required at T05.05 time.
