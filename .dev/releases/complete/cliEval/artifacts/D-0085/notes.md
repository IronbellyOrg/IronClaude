# D-0085 — Design notes

## Why `ask_question` and not `implement`

`mcp__auggie-mcp__` exposes two tools in the v1 IronClaude inventory:

| Tool | Side effects | Fit for coverage eval |
|---|---|---|
| `ask_question` | Read-only Q&A over the repo. | ✅ Deterministic, fast, no scratch state. |
| `implement` | Mutates the working tree (file writes + optional commit). Long-running. | ❌ Non-deterministic, side-effect heavy, slow. |

The eval only needs the PostToolUse hook to fire under the
`mcp__auggie-mcp__*` matcher branch — both tools satisfy that. Picking
the read-only call keeps the eval body free of cleanup obligations
(no need to roll back a mutated worktree) and keeps the per-eval HOME
isolation contract (FR-ISO2) trivially satisfied: there is no
non-HOME path the call could touch.

## Two-assertion shape ({event, tool}) vs. one ({event})

The minimal "did the matcher fire" assertion is just
`'"event":"sticky_cleared"'` — same byte-stream as E1. But that
assertion is **branch-agnostic**: any of the three matcher prefixes
emits the same `event:sticky_cleared` line. Without the second
assertion, the manifest would not distinguish E2.1 / E2.2 / E2.3 at
runtime, defeating the matcher-coverage purpose of the triad.

The hook script (line 28 of `auggie-flag-clear.sh`) embeds the
matched tool name in the JSONL line as `"tool":"<TOOL_NAME>"`. We
assert the *specific* prefix value (`mcp__auggie-mcp__ask_question`)
to pin the matcher branch, which is the contract D-0084 §2
established for the triad.

## Why a literal contains substring, not a JSONL field equality

`Expect.jsonl` would let us assert a structural predicate
(e.g. `tool == "mcp__auggie-mcp__ask_question"`) but only via Python
callables (`expect.py:269-369`). Those have no YAML wire form, so
declaring them in `real.yaml` would either require a `callback:`
escape hatch (D-4, deferred) or a v2 declarative DSL extension.

For the v1 manifest the substring `'"tool":"mcp__auggie-mcp__ask_question"'`
is uniquely identifying within `logs/auggie-first.jsonl`:

- the JSONL printf format is fixed in the hook script
  (`{"ts":...,"session_id":...,"event":"sticky_cleared","tool":"%s"}`);
- the `"tool":"…"` key only ever appears in `sticky_cleared` events;
- the substring includes the leading `"tool":"` so it cannot collide
  with any future `"some_field":"…ask_question"` line.

If the hook is later extended to emit additional event types that
incidentally use the `"tool":"…"` shape with the same suffix, this
substring assertion would need to tighten — flagged as
risk-low / followup-only (same shape as the D-0083 §1 followup).

## Why the prompt explicitly names the MCP tool

`inputs[0].prompt` is an English instruction to the Claude subprocess.
The chosen prompt — `"Use mcp__auggie-mcp__ask_question to summarise
the auggie-flag-clear hook in src/superclaude/hooks/scripts/."` —
explicitly names the MCP tool. Reasoning:

- The subprocess is biased toward the named tool (vs. picking
  `mcp__auggie__codebase-retrieval` or another close substitute).
- The eval exercises *that* tool specifically, so a mis-pick would
  silently degrade coverage signal.
- It documents intent to a human reader of the manifest.
- The PTY-driver wiring (downstream task) will feed this string
  verbatim, so the eval is self-describing.

`expect_tool_call` is the coverage-gate-consumed field; the prompt
text itself is non-load-bearing as long as it biases toward the named
tool.

## Why E2.2 keeps `requires: [mcp_server.auggie-mcp]` despite `no_pty: skip`

Same independence rationale as D-0083 §"Why E1 keeps `requires`":

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

## Open question for downstream wiring (not blocking T05.04)

The `mcp__auggie-mcp__` server is a separate MCP server registration
from `mcp__auggie__`. Whether `mcp_server.auggie-mcp` is a distinct
capability tag from `mcp_server.auggie` at runtime (vs. an alias) is
decided in the FR-CAP1 implementation under `commands.py`. The
manifest treats them as distinct (E2.1 requires `mcp_server.auggie`;
E2.2 requires `mcp_server.auggie-mcp`) so the per-eval skip semantics
match D-0082 §2 constraint 5 even if a future consolidation makes
them aliases. No action required at T05.04 time.
