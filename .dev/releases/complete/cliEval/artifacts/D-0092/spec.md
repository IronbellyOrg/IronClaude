# D-0092 — E8 PreToolUse serena Matcher Hook Coverage Eval (Body)

**Deliverable ID:** D-0092
**Task ID:** T05.13 (Phase 5)
**Roadmap items:** R-091 (E8 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E8 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E8 — the sixth of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E8 covers the
**`mcp__serena__*` branch** of the PreToolUse matcher group
`Edit|Write|mcp__serena__*` in `src/superclaude/hooks/hooks.json` —
whose command is `freshness-pre-edit.sh` (timeout=5). This is the
third and final of the sibling evals fanning out across the matcher
group: E6 covers **Edit** (D-0090), E7 covers **Write** (D-0091),
E8 covers **`mcp__serena__*`** (this).

Unlike E6 / E7, E8 carries `requires: [mcp_server.serena]` and
soft-skips under `--no-mcp` per FR-CAP1, because firing the
`mcp__serena__*` matcher branch requires invoking a real serena MCP
tool — which only exists when the serena MCP server is reachable.

The body must:

- spawn a fresh claude session via the PTY harness, seed a scratch
  file with a single Write prompt (serena's `replace_content`
  requires a pre-existing file), then inject a content prompt that
  triggers `mcp__serena__replace_content` against the scratch file
  so the PreToolUse hook fires on the `mcp__serena__*` matcher branch;
- assert the hook's observable side-effects (freshness ledger present
  + `pre_edit` event row + `mcp__serena__replace_content` matcher pin);
- assert the scratch file persists post-replace_content (proves the
  serena call completed end-to-end);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit`;
- soft-skip under `--no-mcp` via the `requires: [mcp_server.serena]`
  capability tag (FR-CAP1 — D-0082 §6 row E8).

## 2. Hook-surface contract (from `hooks.json` + OQ-2 D-0082 §4)

`src/superclaude/hooks/hooks.json` PreToolUse block:

```jsonc
"PreToolUse": [
  {
    "matcher": "Edit|Write|mcp__serena__*",
    "hooks": [
      { "type": "command",
        "command": "~/.claude/hooks/freshness-pre-edit.sh",
        "timeout": 5 }
    ]
  }
]
```

The single PreToolUse matcher block fires once per qualifying tool
invocation — for any of Edit, Write, or `mcp__serena__*` calls. The
OQ-2 resolution (D-0082 §4 / decisions.md OQ-2 row E8) splits the
matcher group into three coverage evals:

- **Edit branch** → covered by E6 (D-0090).
- **Write branch** → covered by E7 (D-0091).
- **`mcp__serena__*` branch** → covered by **E8** (this).

The OQ-2 resolution freezes E8's body shape to assert the hook's
side-effects per the matched branch:

| Observable | Purpose |
|---|---|
| `logs/freshness.jsonl` exists | proves the freshness event ledger was opened by `freshness-pre-edit.sh` (or by a prior SessionStart hook on the same spawn) |
| `logs/freshness.jsonl` contains `"type":"pre_edit"` | proves the `pre_edit` event row was emitted to the freshness ledger by `freshness-pre-edit.sh` |
| `logs/freshness.jsonl` contains `"matcher":"mcp__serena__replace_content"` | proves the **`mcp__serena__*` branch** of the matcher group fired specifically (vs. the sibling Edit / Write branches covered by E6 / E7) |
| `modified.txt` exists | proves the scratch file persisted post-replace_content (end-to-end serena completion) |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end |

These five observables are independently sufficient and discriminate
five distinct failure modes: (a) the ledger existence pins that the
JSONL file was opened; (b) the `pre_edit` substring pins that the
PreToolUse hook **emitted its event row**; (c) the
`mcp__serena__replace_content` substring pins that the
**`mcp__serena__*` branch specifically** fired (not Edit / not
Write); (d) the scratch file persistence pins that the serena
operation completed; (e) the exit code pins that the session
reached clean shutdown.

The two-substring shape (`pre_edit` + `mcp__serena__replace_content`)
mirrors the E2.1-3 matcher-coverage triad pattern (D-0086
§"Two-assertion shape ({event, tool})") and the E6 / E7 siblings
(D-0090 §2 / D-0091 §2) — separating the *event-fired* assertion
from the *specific-matcher-fired* assertion so a regression in
matcher routing fails on the second substring even if the first
still passes.

The D-0082 §4 row E8 specification phrases the matcher pin as
`matcher=mcp__serena__*` (the hooks.json matcher *pattern*); the
implementation here asserts `matcher=mcp__serena__replace_content`
(the actual *tool name* that fired) consistent with the E6 / E7
sibling pattern. Per D-0082 §4 row E8 note "or other
`mcp__serena__*` variant in the matcher" — `replace_content` is one
acceptable choice; it keeps the body symmetric with E6 (both modify
an existing file's contents).

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E8 entry that
previously carried only stale scaffolding metadata (a placeholder
title `"verify-sync detects drift between src/ and .claude/"` from
the pre-OQ-2 numbering and no body). T05.13 replaces the scaffolding
with the frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"PreToolUse serena matcher fires"` (matches D-0082 §4 OQ-2 row E8) |
| **category** | `hook-lifecycle` (sibling to E6 / E7; was `installer` in stale stub) |
| **requires** | `[mcp_server.serena]` — distinguishes E8 from E6 / E7 (`[]`); FR-CAP1 soft-skip under `--no-mcp` |
| **timeout_sec** | `60` (raised from defaults' 120s — three-prompt PTY round-trip is bounded by serena round-trip, typically <30s; 60s is generous; matches E3/E4/E5/E6/E7 sibling for spawn-lifecycle parity) |
| **inputs[0].prompt** | Seed Write: `"Use the Write tool to create a file named modified.txt under the current working directory with the single line 'before'."` — pre-creates the file because serena's `replace_content` requires a pre-existing target (mirrors E6 Write→Edit chain) |
| **inputs[1].prompt** | Serena fire: `"Use mcp__serena__replace_content on modified.txt to replace 'before' with 'after'."` + `expect_tool_call: mcp__serena__replace_content` — the serena invocation that fires the PreToolUse hook on the `mcp__serena__*` matcher branch |
| **inputs[2].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract |
| **expects[0]** | `file: { path: logs/freshness.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"type":"pre_edit"' }` |
| **expects[2]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"matcher":"mcp__serena__replace_content"' }` |
| **expects[3]** | `file: { path: modified.txt, exists: true }` |
| **expects[4]** | `exit_code: { equals: 0 }` |

PTY-exclusion tag: `no_pty: skip` (carried forward from the
scaffolding entry — every eval in the `real` suite is PTY-driven
per DOC-OQ3 / R-077).

T05.13 also adds `mcp_server.serena` to the manifest's
`optional_capabilities` block so the FR-CAP1 gate recognises the
capability and `eval doctor` (T01.13) can probe its reachability.
The declarative `gate_flag: "--no-mcp"` + `failure_mode: skip`
matches the existing auggie / auggie-mcp / airis-mcp-gateway rows.

**Footnote — `event_count` deferral.** D-0082 §4 row E8 lists a
secondary assertion `event_count(type=pre_edit,
matcher=mcp__serena__*) == 1` (exactly one serena-branch PreToolUse
fire per the single serena prompt). This predicate requires a
Python callable filter (`expect.py:269-369`), not expressible in
declarative YAML. The E3 / E4 / E5 / E6 / E7 siblings
(D-0087/D-0088/D-0089/D-0090/D-0091 §3) solved the same problem by
using `Expect.file` with the JSONL substring as a sufficient proxy
for `contains_event`; T05.13 follows the same precedent. The
per-input count aspect — a one-fire-per-serena-prompt guard — is
deferred until either (a) the YAML callback escape hatch (D-4) is
exercised for E8, or (b) a future schema bump adds a declarative
`jsonl: contains_event: { type: ..., matcher: ..., count: N }`
shorthand. Neither is in scope for T05.13; the current body
satisfies the OQ-2 minimum AC ("body matches the OQ-2 resolution;
runs deterministically on a clean HOME").

Note: the seed Write prompt (`inputs[0]`) will also fire the
PreToolUse hook on the Write matcher branch, producing a row with
`"matcher":"Write"` in `logs/freshness.jsonl`. The E8 assertions
use `Expect.file.contains` which only requires the substring to
appear somewhere in the file — both the Write-row and the
serena-row coexist, and the assertion succeeds when at least the
serena-row substring is present. The Write co-fire is harmless;
E7 already pins the Write branch independently.

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E8` is
trivially accepted — `eval describe --suite real --eval E8` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new freshness ledger entry on every
  PreToolUse fire (FR-ISO2 fresh HOME per eval — no carry-over).
- The Write seed creates `modified.txt` with content `'before'` —
  deterministic content; deterministic file existence.
- The `mcp__serena__replace_content` call modifies `modified.txt`
  from `'before'` to `'after'` — fires PreToolUse on the
  `mcp__serena__*` matcher branch exactly once per the single
  serena prompt; emits one `pre_edit`-typed row with
  `matcher=mcp__serena__replace_content` field. Both substring
  assertions hold.
- `modified.txt` persists post-replace_content (the file is
  modified in-place; existence is invariant).
- The `/quit` input causes an immediate clean exit (exit code 0).
- No time-of-day, network, or shared-state dependencies — D-0082
  §2 constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored. The
  `ts`, `session_id`, `tool_call_idx`, `recent_read_age_sec`, and
  `decision` fields on the JSONL row are not asserted against.

Three consecutive `eval run --suite real --eval E8` invocations on
a clean HOME with serena reachable must therefore yield identical
EvalOutcome statuses, which is the per-task acceptance criterion.

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`). The
  three-element `inputs[]` array is accepted by the open-shape
  array schema. The `expect_tool_call` field on `inputs[1]` is
  accepted by the open-shape (mirrors E1 / E2.1-3 usage).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All five
  primitives used (4×`file`, 1×`exit_code`) are in
  `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported
  by `Expect.file._build` (`expect.py:186-265`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `requires: [mcp_server.serena]` is an array of strings per
  `evalEntry.requires` schema; `mcp_server.serena` is now declared
  in the manifest's `optional_capabilities` block.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E8 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E8` (no flags, serena reachable) | RUNS | capability tag `mcp_server.serena` resolves; PTY harness present on host |
| `eval run --suite real --eval E8 --no-mcp` | SKIPPED (`--no-mcp`) | `requires: [mcp_server.serena]` + `gate_flag: --no-mcp` → FR-CAP1 soft-skip with `skip_reason` populated |
| `eval run --suite real --eval E8` (serena unreachable) | SKIPPED (capability) | `failure_mode: skip` on unreachable mcp_server.serena |
| `eval run --suite real --eval E8 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077); `--no-pty` short-circuits before FR-CAP1 |
| `eval run --suite real --eval E8 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture is the inverse of sibling E6 / E7 (Edit / Write
branches), which run regardless of `--no-mcp` because the Edit
and Write tools are built into Claude Code itself. The
`mcp__serena__*` branch necessarily requires a connected serena
MCP server — that distinction is exactly why the matcher group
was split into three coverage evals (per D-0082 §6).

## 8. Verification

Per phase-5-tasklist.md T05.13, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E8
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 / T05.07 / T05.08 / T05.09 /
T05.10 / T05.11 evidence blocks all block any direct `eval run`
invocation. That blocker is the responsibility of the
runner-completion task (Phase-5 dependency of the CP-P05-T13-T17
checkpoint at T05.18). T05.13 authors the manifest body;
observable verification is therefore via:

- (a) `eval describe --suite real --eval E8` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.13/describe-E8.txt`);
- (b) `eval list --json` continuing to enumerate suite `real`
  with 17 evals (proves schema acceptance; see
  `evidence/T05.13/list-with-E8.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.13/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls
into the runner-completion task downstream of T05.13.

### 8.1 Risk note — freshness-pre-edit.sh telemetry gap

`src/superclaude/hooks/scripts/freshness-pre-edit.sh` (current
revision as of 2026-05-20, lines 108-119) emits a JSONL envelope
to **`$HOME/.claude/logs/freshness-hook.jsonl`** with the schema:

```json
{"ts":...,"event":"PreToolUse","tool":"mcp__serena__replace_content","path":...,
 "session_id":...,"tool_call_idx":...,"decision":...,"reason":...}
```

The OQ-2 D-0082 §4 body shape — which T05.13 lands verbatim —
asserts **both a different path** (`logs/freshness.jsonl`) **and
different field names** (`type=pre_edit` and
`matcher=mcp__serena__replace_content`, not `event=PreToolUse`
and `tool=mcp__serena__replace_content`). The script does NOT
write to `logs/freshness.jsonl` and does NOT use `type` /
`matcher` field names on its current telemetry path.

This gap is **not introduced** by T05.13; it predates the
deliverable and mirrors the identical telemetry gaps discovered
for `session-init.sh` during T05.07 (D-0087 §8.1),
`freshness-session-start.sh` during T05.08 (D-0088 §8.1),
`freshness-user-prompt.sh` during T05.09 (D-0089 §8.1), and the
**same `freshness-pre-edit.sh` script** during T05.10 (D-0090 §8.1)
and T05.11 (D-0091 §8.1). The E6 / E7 / E8 evals share the
underlying script, so the single hook-script update that lands
`logs/freshness.jsonl` with `type` / `matcher` field names
unblocks all three siblings simultaneously.

Acceptance criteria for T05.13 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E8` to exit 0 deterministically
depends transitively on (a) the runner NameError fix, (b) the
freshness-pre-edit.sh emit-observables update with the OQ-2
contract field names, and (c) the serena MCP server being
reachable during the test run.

### 8.2 Risk note — `mcp_server.serena` reachability probe

`mcp_server.serena` is now declared in the manifest's
`optional_capabilities` block but is NOT in the static
`_DEFAULT_CAPABILITY_SPECS` roster in
`src/superclaude/cli/eval/capabilities.py:184-214`. With the
default `PermissiveCapabilityResolver`, E8's `requires` clause
resolves trivially at load time. With a stricter resolver (e.g.
`CapabilityGates`), the unknown capability name would need to be
added to the roster so `eval doctor` can probe its reachability.
T05.13 leaves that addition to a future capabilities task — the
manifest declaration alone is sufficient for FR-CAP1 soft-skip
once the gate is upgraded.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E8` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.07 (E3 body) | first-position SessionStart hook (same comment-block template) |
| Sibling | T05.08 (E4 body) | second-position SessionStart matcher=* hook (same JSONL ledger) |
| Sibling | T05.09 (E5 body) | UserPromptSubmit no-matcher hook (same freshness JSONL ledger) |
| Sibling | T05.10 (E6 body) | PreToolUse Edit matcher (**same hook script and ledger**, different branch — trio shares all telemetry-gap follow-up) |
| Sibling | T05.11 (E7 body) | PreToolUse Write matcher (**same hook script and ledger**, different branch — trio shares all telemetry-gap follow-up) |
| Unblocks | T05.18 (CP-P05-T13-T17 checkpoint) | E8 must enumerate + describe; full-run verification follows runner fix |
| Unblocks | T05.14..T05.17 (E9..E12 bodies) | the E8 authoring template lands the serena-capability declaration that downstream evals can reference |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
