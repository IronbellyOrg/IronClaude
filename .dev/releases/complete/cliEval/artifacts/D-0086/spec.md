# D-0086 — E2.3 Airis-MCP-Gateway Matcher Coverage Eval (Body)

**Deliverable ID:** D-0086
**Task ID:** T05.05 (Phase 5)
**Roadmap items:** R-085 (E2.3 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E2.3 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E2.3 — the third leg of
the E2.{1,2,3} auggie matcher-coverage triad (per D-0082 §3 hook
surface coverage map). E2.3 covers the
`mcp__airis-mcp-gateway__auggie_.*` branch of the PostToolUse
`auggie-flag-clear.sh` matcher; E2.1 covered `mcp__auggie__*`
(D-0084) and E2.2 covered `mcp__auggie-mcp__*` (D-0085).

The body must:

- invoke the real `mcp__airis-mcp-gateway__auggie_search` MCP tool
  (so the PostToolUse hook's `mcp__airis-mcp-gateway__auggie_.*`
  matcher branch fires);
- assert that the lifecycle observably ran with the *correct matcher
  branch* (`sticky_cleared` event + `tool` field naming the
  `mcp__airis-mcp-gateway__auggie_search` call) in
  `logs/auggie-first.jsonl`;
- soft-skip under `--no-mcp` via the existing
  `optional_capabilities[mcp_server.airis-mcp-gateway]` gate
  (FR-CAP1).

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
   matched. This second observable is what distinguishes E2.3 from
   E2.1 / E2.2 at assertion time: each entry asserts a different
   `"tool":"…"` substring against the *same* JSONL file, proving its
   matcher branch fired specifically.

**Glob-suffix nuance:** Unlike E2.1 / E2.2 — whose matcher branches
are simple prefix-globs `mcp__auggie__*` / `mcp__auggie-mcp__*` —
E2.3's branch is `mcp__airis-mcp-gateway__auggie_*` (note the
trailing `auggie_` literal). The airis gateway exposes many MCP tool
families (`tavily-*`, `context7-*`, etc.); only tools whose name
starts with `auggie_` (e.g. `auggie_search`, `auggie_history`) fire
the sticky-clear branch. Selecting `auggie_search` (not the gateway's
generic `search` or a `tavily-*` proxy) is therefore load-bearing for
matcher coverage.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E2.3 entry that
already carries the FR-CAP1 metadata. New body additions:

| Field | Value |
|---|---|
| **inputs[0].prompt** | `"Use mcp__airis-mcp-gateway__auggie_search to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."` |
| **inputs[0].expect_tool_call** | `mcp__airis-mcp-gateway__auggie_search` |
| **expects[0]** | `file: { path: logs/auggie-first.jsonl, exists: true, contains: '"event":"sticky_cleared"' }` |
| **expects[1]** | `file: { path: logs/auggie-first.jsonl, exists: true, contains: '"tool":"mcp__airis-mcp-gateway__auggie_search"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

The `expect_tool_call` value lights up the FR-COV1 coverage gate (per
`coverage.py:_iter_eval_tool_calls`) for the
`mcp__airis-mcp-gateway__auggie_.*` regex branch of the PostToolUse
matcher registration. E2.3 therefore registers as the *sole* covering
eval for the `mcp__airis-mcp-gateway__` prefix in the
`_DEFAULT_MCP_TOOL_PREFIXES` triad (`coverage.py:103-107`),
**completing the v1 matcher-coverage roster**.

**Tool choice (`auggie_search`):** The airis-mcp-gateway exposes
several `auggie_*` tools (`auggie_search`, `auggie_history`, plus
gateway-internal endpoints). `auggie_search` is the read-only
codebase-retrieval surface (analogous to
`mcp__auggie__codebase-retrieval`); it is deterministic, fast, and
has no scratch-state side effects. The alternatives either mutate
state (e.g. `auggie_history` writes session marks) or are
gateway-internal and not user-callable from a Claude subprocess.
Read-only is the right choice for a coverage-only eval.

## 4. Parameterize-expanded id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^E\d+(?:\.\d+)?$`. The literal id `E2.3` is enumerated by the
manifest and accepted by `eval describe --suite real --eval E2.3`,
which round-trips the new body verbatim (see `evidence.md`).

## 5. `--no-mcp` soft-skip behavior

E2.3 carries `requires: [mcp_server.airis-mcp-gateway]`. The
suite-level `optional_capabilities` block already gates that
capability behind `--no-mcp`:

```yaml
# real.yaml (unchanged)
optional_capabilities:
  - { name: mcp_server.airis-mcp-gateway, gate_flag: "--no-mcp", failure_mode: skip }
```

Under `--no-mcp`, the FR-CAP1 path in `commands.py` adds
`mcp_server.airis-mcp-gateway` to the disabled-capabilities set;
CapabilityGates returns SKIPPED with
`skip_reason="--no-mcp"` / `skip_flag_triggered="--no-mcp"` before
any HOME setup or PTY spawn. This matches D-0082 §2 constraint 5 and
mirrors the E2.1 / E2.2 wiring.

**Behaviour matrix:**

| Invocation | E2.3 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E2.3` (no flags) | RUNS | capability available, body executes |
| `eval run --suite real --eval E2.3 --no-mcp` | SKIPPED (`--no-mcp`) | FR-CAP1 soft-skip via `optional_capabilities` |
| `eval run --suite real --eval E2.3 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E2.3 --no-mcp --no-pty` | SKIPPED | `--no-pty` short-circuits first per `commands.py` |

## 6. Verification

Per phase-5-tasklist.md T05.05, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E2.3
```

**Today's runner state:** PTY prompt injection from
`inputs[0].prompt` is not yet wired in M-1; full execution of E2.3 is
gated on the downstream PTY-prompt-injection wiring task (same status
as E1 / E2.1 / E2.2 documented in D-0083 §6 / D-0084 §6 / D-0085 §6).
T05.05 authors the manifest body; observable verification is performed
via:

- (a) `eval describe --suite real --eval E2.3` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.05/describe-E2.3.txt`);
- (b) coverage-map enumeration showing E2.3 covers the
  `mcp__airis-mcp-gateway__auggie_.*` matcher branch alongside
  E1/E2.1/E2.2 — completing the v1 triad (see
  `evidence/T05.05/coverage-map.txt`);
- (c) `eval run --suite real --eval E2.3 --no-mcp` (FR-CAP1 soft-skip
  proof — currently blocked by the same pre-existing
  `_new_run_id` NameError in `commands.py` line 1418 documented at
  T05.03 / T05.04 time; see `evidence/T05.05/run-E2.3-no-mcp.txt`).

Full end-to-end PTY execution proof rolls into the runner-completion
task downstream of T05.05.

## 7. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts `E2.3` id |
| Depends on | T04.03 (Expect.file impl) | satisfied by current expect.py |
| Depends on | T04.10 (`--no-mcp` flag wiring) | satisfied by current commands.py |
| Sibling | T05.03 (E2.1) | shares hook contract / body shape |
| Sibling | T05.04 (E2.2) | shares hook contract / body shape |
| Unblocks | T05.06 (CP-P05-T01-T05 checkpoint) | E2.3 row must pass; completes the v1 triad gate |

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
