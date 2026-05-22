# D-0085 — E2.2 Auggie-MCP Matcher Coverage Eval (Body)

**Deliverable ID:** D-0085
**Task ID:** T05.04 (Phase 5)
**Roadmap items:** R-084 (E2.2 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E2.2 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E2.2 — the second leg of
the E2.{1,2,3} auggie matcher-coverage triad (per D-0082 §3 hook
surface coverage map). E2.2 covers the `mcp__auggie-mcp__*` branch of
the PostToolUse `auggie-flag-clear.sh` matcher; E2.1 covered
`mcp__auggie__*` (D-0084), and E2.3 will cover
`mcp__airis-mcp-gateway__auggie_*` (D-0086).

The body must:

- invoke the real `mcp__auggie-mcp__ask_question` MCP tool (so the
  PostToolUse hook's `mcp__auggie-mcp__*` matcher branch fires);
- assert that the lifecycle observably ran with the *correct matcher
  branch* (`sticky_cleared` event + `tool` field naming the
  `mcp__auggie-mcp__ask_question` call) in
  `logs/auggie-first.jsonl`;
- soft-skip under `--no-mcp` via the existing
  `optional_capabilities[mcp_server.auggie-mcp]` gate (FR-CAP1).

## 2. Hook telemetry contract (from `auggie-flag-clear.sh`)

`src/superclaude/hooks/scripts/auggie-flag-clear.sh` lines 22–32:

```bash
case "$TOOL_NAME" in
    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)
        STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
        if [ -f "$STICKY" ]; then
            rm -f "$STICKY" 2>/dev/null || true
            ...
            printf '{"ts":"%s","session_id":"%s","event":"sticky_cleared","tool":"%s"}\n' \
                "$NOW_ISO" "$SESSION_ID" "$TOOL_NAME" >> "$AUGGIE_LOG" ...
        fi
        ;;
esac
```

Two observables, both written to `$HOME/.claude/logs/auggie-first.jsonl`:

1. `"event":"sticky_cleared"` — proves the lifecycle ran (sticky
   pre-existed AND a matched tool call fired).
2. `"tool":"<TOOL_NAME>"` — records the *specific* tool name that
   matched. This second observable is what distinguishes E2.2 from
   E2.1 / E2.3 at assertion time: each entry asserts a different
   `"tool":"…"` substring against the *same* JSONL file, proving its
   matcher branch fired specifically.

Without the `"tool":"<name>"` assertion, all three E2.x entries would
be interchangeable — the matcher branch isn't pinned by `expects[]`,
only by `expect_tool_call` (which feeds coverage gate metadata but not
runtime assertion). The two-assertion shape (event + tool) is the
contract D-0084 §2 established for the triad.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E2.2 entry that
already carries the FR-CAP1 metadata. New body additions:

| Field | Value |
|---|---|
| **inputs[0].prompt** | `"Use mcp__auggie-mcp__ask_question to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."` |
| **inputs[0].expect_tool_call** | `mcp__auggie-mcp__ask_question` |
| **expects[0]** | `file: { path: logs/auggie-first.jsonl, exists: true, contains: '"event":"sticky_cleared"' }` |
| **expects[1]** | `file: { path: logs/auggie-first.jsonl, exists: true, contains: '"tool":"mcp__auggie-mcp__ask_question"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

The `expect_tool_call` value lights up the FR-COV1 coverage gate (per
`coverage.py:_iter_eval_tool_calls`) for the
`mcp__auggie-mcp__.*` regex branch of the PostToolUse matcher
registration. E2.2 therefore registers as the *sole* covering eval
for the `mcp__auggie-mcp__` prefix in the
`_DEFAULT_MCP_TOOL_PREFIXES` triad (`coverage.py:103-107`).

**Tool choice (`ask_question`):** `mcp__auggie-mcp__` advertises
`ask_question` and `implement` in the auggie-mcp server surface.
`ask_question` is the read-only / side-effect-free call; `implement`
mutates the working tree (and pulls a long-running git-aware
pipeline). For a coverage-only eval the read-only call is the
appropriate choice (deterministic, fast, no scratch repo state).

## 4. Parameterize-expanded id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^E\d+(?:\.\d+)?$`. The literal id `E2.2` is already enumerated
post-T05.03 manifest edit; `eval list --json` confirms it appears in
the manifest output and `eval describe --suite real --eval E2.2`
returns the body added by this deliverable (see `evidence.md`).

## 5. `--no-mcp` soft-skip behavior

E2.2 carries `requires: [mcp_server.auggie-mcp]`. The suite-level
`optional_capabilities` block already gates that capability behind
`--no-mcp`:

```yaml
# real.yaml (unchanged)
optional_capabilities:
  - { name: mcp_server.auggie-mcp, gate_flag: "--no-mcp", failure_mode: skip }
```

Under `--no-mcp`, the FR-CAP1 path in `commands.py` adds
`mcp_server.auggie-mcp` to the disabled-capabilities set;
CapabilityGates returns SKIPPED with
`skip_reason="--no-mcp"` / `skip_flag_triggered="--no-mcp"` before
any HOME setup or PTY spawn. This matches D-0082 §2 constraint 5 and
mirrors the E2.1 / E2.3 wiring.

**Behaviour matrix:**

| Invocation | E2.2 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E2.2` (no flags) | RUNS | capability available, body executes |
| `eval run --suite real --eval E2.2 --no-mcp` | SKIPPED (`--no-mcp`) | FR-CAP1 soft-skip via `optional_capabilities` |
| `eval run --suite real --eval E2.2 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E2.2 --no-mcp --no-pty` | SKIPPED | `--no-pty` short-circuits first per `commands.py` |

## 6. Verification

Per phase-5-tasklist.md T05.04, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E2.2
```

**Today's runner state:** PTY prompt injection from
`inputs[0].prompt` is not yet wired in M-1; full execution of E2.2 is
gated on the downstream PTY-prompt-injection wiring task (same status
as E1 / E2.1 documented in D-0083 §6 / D-0084 §6). T05.04
authors the manifest body; observable verification is performed via:

- (a) `eval describe --suite real --eval E2.2` rendering the new
  inputs/expects rows (manifest shape proof);
- (b) coverage-map enumeration showing E2.2 covers the
  `mcp__auggie-mcp__*` matcher branch alongside E1/E2.1 for
  `mcp__auggie__*`;
- (c) `eval run --suite real --eval E2.2 --no-mcp` (FR-CAP1 soft-skip
  proof — currently blocked by an unrelated `_new_run_id` NameError
  in `commands.py` line 1418 observed at T05.03 time; see
  `evidence.md`).

Full end-to-end PTY execution proof rolls into the runner-completion
task downstream of T05.04.

## 7. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts `E2.2` id |
| Depends on | T04.03 (Expect.file impl) | satisfied by current expect.py |
| Depends on | T04.10 (`--no-mcp` flag wiring) | satisfied by current commands.py |
| Sibling | T05.03 (E2.1) | shares hook contract / body shape |
| Sibling | T05.05 (E2.3) | shares hook contract / body shape |
| Unblocks | T05.06 (CP-P05-T01-T05 checkpoint) | E2.2 row must pass |

## 8. Schema validation

The body uses only:

- `inputs[].prompt: string` (additionalProperties: true under
  evalEntry.inputs.items per `suite.schema.json` line 139)
- `inputs[].expect_tool_call: string` (same; consumed by coverage gate)
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping`; the two `file` primitives use
  `path`, `exists`, `contains` kwargs (all supported by
  `Expect.file._build` per expect.py:186-265)

No schema-version bump required.
