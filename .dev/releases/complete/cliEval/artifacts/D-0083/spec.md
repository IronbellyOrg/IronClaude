# D-0083 — E1 Auggie-First Sticky Lifecycle Eval (Body)

**Deliverable ID:** D-0083
**Task ID:** T05.02 (Phase 5)
**Roadmap items:** R-084 (E1 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E1 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E1 — the first of the
E1 / E2.1-3 auggie-first sticky lifecycle quartet (per D-0082 §4 hook
surface coverage map). E1 covers the singleton `mcp__auggie__*`
matcher branch of the `auggie-flag-clear.sh` PostToolUse hook; E2.1-3
cover matcher coverage across the three auggie prefixes.

The body must:

- invoke the real `mcp__auggie__codebase-retrieval` MCP tool (so the
  PostToolUse hook's matcher fires);
- assert that the lifecycle observably ran (`sticky_cleared` event
  recorded in `logs/auggie-first.jsonl`);
- soft-skip under `--no-mcp` via the existing
  `optional_capabilities[mcp_server.auggie]` gate (FR-CAP1).

## 2. Hook telemetry contract (from `auggie-flag-clear.sh`)

The post-tool-call hook (`src/superclaude/hooks/scripts/auggie-flag-clear.sh`)
fires for `mcp__auggie__*`, `mcp__auggie-mcp__*`, and
`mcp__airis-mcp-gateway__auggie_*`. Its observable side-effects in the
per-eval HOME are:

```
$HOME/.claude/state/auggie-first-pending/<session_id>.txt   (input)
$HOME/.claude/logs/auggie-first.jsonl                       (output)
```

The hook's load-bearing branch (script line 25) is:

```bash
STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
if [ -f "$STICKY" ]; then
    rm -f "$STICKY" 2>/dev/null || true
    ... printf '{"ts":..., "session_id":..., "event":"sticky_cleared", "tool":...}' >> "$AUGGIE_LOG" ...
fi
```

**Implication:** the hook only emits `sticky_cleared` IF the sticky
pre-existed. Therefore asserting the JSONL event is a **sufficient
proxy** for the full "set → clear" lifecycle:

- `sticky_cleared` present ⇒ sticky was present before the tool call
  (set) AND the tool call matched the hook's matcher (clear).
- `sticky_cleared` absent ⇒ either no matching tool call OR no sticky
  existed pre-call — either way the lifecycle did NOT complete.

This proxy is what makes the body shape expressible under the current
Expect.* primitive surface (D-4 / T04.0x) **without** session-id
template substitution (see §4).

## 3. Frozen body shape

The body shape lands in `suites/real.yaml` under the E1 entry that
already carries the FR-CAP1 metadata. New body additions:

| Field | Value |
|---|---|
| **inputs[0].prompt** | `"Use mcp__auggie__codebase-retrieval to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."` |
| **inputs[0].expect_tool_call** | `mcp__auggie__codebase-retrieval` |
| **expects[0]** | `file: { path: logs/auggie-first.jsonl, exists: true, contains: '"event":"sticky_cleared"' }` |
| **expects[1]** | `exit_code: { equals: 0 }` |

The `expect_tool_call` value lights up the FR-COV1 coverage gate (per
`coverage.py:_iter_eval_tool_calls`), so the PostToolUse
`mcp__auggie__*` matcher receives the eval-credit needed for E1 to
register as "covered" alongside E2.1.

**Rationale for `contains` substring (not `jsonl.assert_any`):** the
v1 Expect.jsonl primitive's `assert_each` / `assert_any` arguments are
Python callables (`expect.py:269-283`) and have no YAML representation.
Expressing the event-presence assertion via `Expect.file(contains=...)`
against the JSONL byte-stream is the YAML-friendly equivalent for v1
and matches D-0082 §2 constraint 4 ("Expect.* primitive only").

## 4. Documented gap — literal `file_absent(state/.../<sid>.txt)`

The original design-spec §5.1 sketch for E1 included a literal
`file.exists(path="state/auggie-first-pending/{session_id}.txt")` /
`file.absent(...)` pre/post pair. That assertion is **deferred** at
T05.02 for two reasons:

1. **No template substitution layer:** `session_id` is allocated by the
   orchestrator at runtime (HomeIsolation.session_id, stamped into
   `CLAUDE_SESSION_ID`) and is not known at YAML-author time. The
   current YAML manifest has no `{session_id}` template-resolution
   pass.
2. **No pre/post snapshot mechanism:** Expect.* primitives all execute
   in the **post-execution** phase (per `runner.py` 7-step lifecycle).
   There is no "pre-tool-call snapshot" primitive that would let the
   YAML assert "before the matched tool call, the sticky file existed".

Both gaps are tracked as follow-ups (not blocking T05.02):

- **FU-T05.02-A** — add `{session_id}` placeholder substitution in
  `loader.py` so manifests can reference `home_path /
  state/auggie-first-pending/{session_id}.txt` literally.
- **FU-T05.02-B** — extend Expect.* with a pre-hook snapshot primitive
  (or an EvalContext field carrying the pre-spawn FS image) so
  pre/post differential assertions are expressible.

Until those land, the §3 body shape (sticky_cleared event + exit 0) is
the verifiable contract; the literal file_absent assertion is a
documentation-only contract.

## 5. `--no-mcp` soft-skip behavior

The existing suite-level wiring carries E1's capability gate:

```yaml
# real.yaml (unchanged)
optional_capabilities:
  - { name: mcp_server.auggie, gate_flag: "--no-mcp", failure_mode: skip }

evals:
  - id: E1
    requires: [mcp_server.auggie]
    ...
```

When the runner is invoked with `--no-mcp`, the FR-CAP1 path in
`commands.py` adds `mcp_server.auggie` to the disabled-capabilities
set; CapabilityGates therefore returns SKIPPED with
`skip_reason="--no-mcp"` / `skip_flag_triggered="--no-mcp"` before any
HOME setup or PTY spawn. This matches D-0082 §2 constraint 5.

**Net behaviour matrix:**

| Invocation | E1 outcome | Why |
|---|---|---|
| `eval run --suite real` (no flags) | RUNS | capability available, body executes |
| `eval run --suite real --no-mcp` | SKIPPED (skip_reason=`--no-mcp`) | FR-CAP1 soft-skip via `optional_capabilities` |
| `eval run --suite real --no-pty` | SKIPPED (skip_reason=`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E1 --no-mcp --no-pty` | SKIPPED | `--no-pty` short-circuits first per `commands.py` |

## 6. Verification

Per phase-5-tasklist.md T05.02:

```bash
uv run superclaude eval run --suite real --eval E1
```

**Today's runner state:** the M-1 runner does not yet drive PTY-based
prompt injection from `inputs[0].prompt` — that wiring lands later in
Phase 5 (per the design-spec §6 PTY harness component). T05.02
authors the manifest body; verification is therefore performed via:

- (a) `eval describe --suite real --eval E1` rendering the new
  inputs/expects rows; and
- (b) `eval run --suite real --eval E1 --no-mcp` resolving to
  SKIPPED with `skip_reason="--no-mcp"` (proves capability gate wiring
  intact and body is loadable).

Full end-to-end PTY execution proof is rolled into the relevant
runner-completion task (downstream of T05.02).

See `evidence.md` for the verification command transcripts.

## 7. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T04.03 (Expect.jsonl impl) | satisfied by current expect.py |
| Depends on | T04.04 (Expect.file impl) | satisfied by current expect.py |
| Depends on | T04.10 (`--no-mcp` flag wiring) | satisfied by current commands.py |
| Unblocks | T05.03 (E2.1-3 parameterize body) | shares hook contract |
| Follow-ups | FU-T05.02-A, FU-T05.02-B | §4 |

## 8. Schema validation

The body uses only:

- `inputs[].prompt: string` (additionalProperties: true under
  evalEntry.inputs.items per `suite.schema.json` line 139)
- `inputs[].expect_tool_call: string` (same; consumed by coverage gate)
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping`

No schema-version bump required.
