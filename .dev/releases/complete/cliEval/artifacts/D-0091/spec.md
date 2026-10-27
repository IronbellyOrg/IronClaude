# D-0091 — E7 PreToolUse Write Matcher Hook Coverage Eval (Body)

**Deliverable ID:** D-0091
**Task ID:** T05.11 (Phase 5)
**Roadmap items:** R-090 (E7 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E7 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E7 — the fifth of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E7 covers the
**Write branch** of the PreToolUse matcher group
`Edit|Write|mcp__serena__*` in `src/superclaude/hooks/hooks.json` —
whose command is `freshness-pre-edit.sh` (timeout=5). This is the
second of three sibling evals fanning out across the matcher group:
E6 covers **Edit** (D-0090), E7 covers **Write** (this), E8 covers
`mcp__serena__*` (future, MCP-tagged).

The body must:

- spawn a fresh claude session via the PTY harness and inject a content
  prompt that triggers a single Write tool call against a scratch file
  under the per-eval HOME so the PreToolUse hook fires on the Write
  matcher branch;
- assert the hook's observable side-effects (freshness ledger present
  + `pre_edit` event row + `Write` matcher pin);
- assert the scratch file persists post-Write (proves the Write
  completed end-to-end);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit`;
- run with **no capability tags** — no MCP, no network, no shared
  state — so the body executes on every host regardless of MCP-server
  availability (D-0082 §6 capability-tag rollup row for E7).

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
OQ-2 resolution (D-0082 §4 / decisions.md OQ-2 row E7) splits the
matcher group into three coverage evals:

- **Edit branch** → covered by E6 (D-0090).
- **Write branch** → covered by **E7** (this).
- **`mcp__serena__*` branch** → covered by E8 (sibling, MCP-tagged).

The OQ-2 resolution freezes E7's body shape to assert the hook's
side-effects per the matched branch:

| Observable | Purpose |
|---|---|
| `logs/freshness.jsonl` exists | proves the freshness event ledger was opened by `freshness-pre-edit.sh` (or by a prior SessionStart hook on the same spawn) |
| `logs/freshness.jsonl` contains `"type":"pre_edit"` | proves the `pre_edit` event row was emitted to the freshness ledger by `freshness-pre-edit.sh` |
| `logs/freshness.jsonl` contains `"matcher":"Write"` | proves the **Write** branch of the matcher group fired specifically (vs. the sibling Edit / serena branches covered by E6 / E8) |
| `written.txt` exists | proves the scratch file persisted post-Write (end-to-end Write completion) |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end |

These five observables are independently sufficient and discriminate
five distinct failure modes: (a) the file existence pins that the
ledger was opened; (b) the `pre_edit` substring pins that the
PreToolUse hook **emitted its event row**; (c) the `Write` substring
pins that the **Write branch specifically** fired (not Edit / not
serena); (d) the scratch file persistence pins that the Write operation
completed; (e) the exit code pins that the session reached clean
shutdown.

The two-substring shape (`pre_edit` + `Write`) mirrors the E2.1-3
matcher-coverage triad pattern (D-0086 §"Two-assertion shape
({event, tool})") and the E6 (D-0090 §2) sibling — separating the
*event-fired* assertion from the *specific-matcher-fired* assertion
so a regression in matcher routing fails on the second substring even
if the first still passes.

The D-0082 §4 second assertion `event_count == 1` (matcher-pin singular
Write tool call) is functionally covered by combining the substring
assertion with the eval's input shape (exactly one Write prompt in
`inputs[]`); the precise per-input count predicate requires a Python
callable and is deferred — see §3 footnote on YAML expressibility.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E7 entry that previously
carried only stale scaffolding metadata (a placeholder title
"user_prompt_submit hook prepends auggie-first reminder" and no body).
T05.11 replaces the scaffolding with the frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"PreToolUse Write matcher fires"` (matches D-0082 §4 OQ-2 row E7) |
| **timeout_sec** | `60` (raised from defaults' 120s — two-prompt PTY round-trip is bounded by Write completion, typically <10s; 60s is generous; matches E3/E4/E5/E6 sibling for spawn-lifecycle parity) |
| **inputs[0].prompt** | Write fire: `"Use the Write tool to create a file named written.txt under the current working directory with the single line 'hello'."` — the Write invocation that fires the PreToolUse hook on the Write matcher branch. Unlike E6 (which needs a Write→Edit chain because Edit requires a pre-existing target), Write creates a new file directly via the `no_prior_read` `create_allowed` branch (`freshness-pre-edit.sh:78-87`); no seed prompt is required |
| **inputs[1].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract |
| **expects[0]** | `file: { path: logs/freshness.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"type":"pre_edit"' }` |
| **expects[2]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"matcher":"Write"' }` |
| **expects[3]** | `file: { path: written.txt, exists: true }` |
| **expects[4]** | `exit_code: { equals: 0 }` |

Capability tags: `[]` (no `requires:` clause). The eval runs on every
host regardless of `--no-mcp` posture; it is **not** soft-skipped by
the FR-CAP1 gate. (Note: E8, the `mcp__serena__*` sibling, **will**
carry `requires: [mcp_server.serena]` and soft-skip under `--no-mcp` —
that distinction is exactly why the matcher group was split into three
coverage evals.)

PTY-exclusion tag: `no_pty: skip` (carried forward from the scaffolding
entry — every eval in the `real` suite is PTY-driven per DOC-OQ3 /
R-077).

**Footnote — `event_count == 1` deferral.** D-0082 §4 row E7 lists a
secondary assertion `event_count(type=pre_edit, matcher=Write) == 1`
(exactly one Write-branch PreToolUse fire per the single Write prompt).
This predicate requires a Python callable filter (`expect.py:269-369`),
not expressible in declarative YAML. The E3 / E4 / E5 / E6 siblings
(D-0087/D-0088/D-0089/D-0090 §3) solved the same problem by using
`Expect.file` with the JSONL substring as a sufficient proxy for
`contains_event`; T05.11 follows the same precedent. The per-input
count aspect — a one-fire-per-Write-prompt guard — is deferred until
either (a) the YAML callback escape hatch (D-4) is exercised for E7,
or (b) a future schema bump adds a declarative `jsonl: contains_event:
{ type: ..., matcher: ..., count: N }` shorthand. Neither is in scope
for T05.11; the current body satisfies the OQ-2 minimum AC ("body
matches the OQ-2 resolution; runs deterministically on a clean HOME").

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E7` is
trivially accepted — `eval describe --suite real --eval E7` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new freshness ledger entry on every
  PreToolUse fire (FR-ISO2 fresh HOME per eval — no carry-over).
- The Write tool call creates `written.txt` with `'hello'` —
  deterministic content; deterministic file existence. The
  `no_prior_read` `create_allowed` branch of `freshness-pre-edit.sh`
  permits the Write on a not-yet-existing path without prior Read.
- The Write tool call fires PreToolUse on the Write matcher branch
  exactly once per the single Write prompt; emits one `pre_edit`-typed
  row with `matcher=Write` field. Both substring assertions hold.
- `written.txt` persists post-Write.
- The `/quit` input causes an immediate clean exit (exit code 0).
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored. The `ts`,
  `session_id`, `tool_call_idx`, `recent_read_age_sec`, and `decision`
  fields on the JSONL row are not asserted against.

Three consecutive `eval run --suite real --eval E7` invocations on a
clean HOME must therefore yield identical EvalOutcome statuses, which
is the per-task acceptance criterion.

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`). The two-element
  `inputs[]` array is accepted by the open-shape array schema.
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All five
  primitives used (4×`file`, 1×`exit_code`) are in
  `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported by
  `Expect.file._build` (`expect.py:186-265`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E7 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E7` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E7 --no-mcp` | RUNS | no `requires:` → FR-CAP1 gate is a no-op for E7 |
| `eval run --suite real --eval E7 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E7 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture differs from sibling E8 (`mcp__serena__*` branch) which
**will** soft-skip under `--no-mcp`: E8 must carry
`requires: [mcp_server.serena]` to fire its hook surface. E7's Write
matcher is built into Claude Code itself and does not require any MCP
server.

## 8. Verification

Per phase-5-tasklist.md T05.11, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E7
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 / T05.07 / T05.08 / T05.09 /
T05.10 evidence blocks all block any direct `eval run` invocation.
That blocker is the responsibility of the runner-completion task
(Phase-5 dependency of the CP-P05-T07-T11 checkpoint at T05.12).
T05.11 authors the manifest body; observable verification is therefore
via:

- (a) `eval describe --suite real --eval E7` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.11/describe-E7.txt`);
- (b) `eval list --json` continuing to enumerate suite `real` with
  17 evals (proves schema acceptance; see
  `evidence/T05.11/list-with-E7.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.11/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls into
the runner-completion task downstream of T05.11.

### 8.1 Risk note — freshness-pre-edit.sh telemetry gap

`src/superclaude/hooks/scripts/freshness-pre-edit.sh` (current
revision as of 2026-05-20, lines 108-119) emits a JSONL envelope to
**`$HOME/.claude/logs/freshness-hook.jsonl`** with the schema:

```json
{"ts":...,"event":"PreToolUse","tool":"Write","path":...,
 "session_id":...,"tool_call_idx":...,"decision":...,"reason":...}
```

The OQ-2 D-0082 §4 body shape — which T05.11 lands verbatim — asserts
**both a different path** (`logs/freshness.jsonl`) **and different
field names** (`type=pre_edit` and `matcher=Write`, not
`event=PreToolUse` and `tool=Write`). The script does NOT write to
`logs/freshness.jsonl` and does NOT use `type` / `matcher` field
names on its current telemetry path.

This gap is **not introduced** by T05.11; it predates the deliverable
and mirrors the identical telemetry gaps discovered for
`session-init.sh` during T05.07 (D-0087 §8.1),
`freshness-session-start.sh` during T05.08 (D-0088 §8.1),
`freshness-user-prompt.sh` during T05.09 (D-0089 §8.1), and the
**same `freshness-pre-edit.sh` script** during T05.10 (D-0090 §8.1).
The E6 and E7 evals share the underlying script, so the single
hook-script update that lands `logs/freshness.jsonl` with `type` /
`matcher` field names unblocks both E6 and E7 simultaneously (and E8
once it lands).

Acceptance criteria for T05.11 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E7` to exit 0 deterministically depends
transitively on (a) the runner NameError fix and (b) the
freshness-pre-edit.sh emit-observables update with the OQ-2 contract
field names.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E7` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.07 (E3 body) | first-position SessionStart hook (same comment-block template) |
| Sibling | T05.08 (E4 body) | second-position SessionStart matcher=* hook (same JSONL ledger) |
| Sibling | T05.09 (E5 body) | UserPromptSubmit no-matcher hook (same freshness JSONL ledger) |
| Sibling | T05.10 (E6 body) | PreToolUse Edit matcher (**same hook script and ledger**, different branch — pair shares all telemetry-gap follow-up) |
| Sibling | (future T05.XX) (E8 body) | PreToolUse `mcp__serena__*` matcher (same hook script, MCP-tagged) |
| Unblocks | T05.12 (CP-P05-T07-T11 checkpoint) | E7 must enumerate + describe; full-run verification follows runner fix |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
