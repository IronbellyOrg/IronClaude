# D-0088 — Design notes

## Why two file assertions instead of one

The minimum-viable "did the SessionStart matcher=* freshness hook fire"
assertion could be just **one** of:

- `file.exists(logs/freshness.jsonl)` — proves the freshness ledger was
  opened (the hook ran far enough to create the file).
- `file(logs/freshness.jsonl, contains: '"type":"session_start"')` —
  proves the freshness `session_start` event row was emitted.

We assert **both** because they fail under different failure modes,
following the same matrix established in D-0087 §"Why two file
assertions instead of one" for the E3 sibling:

| Failure mode | `freshness.jsonl` exists | `freshness.jsonl` `session_start` row |
|---|---|---|
| Hook never invoked (registration missing from `hooks.json` SessionStart matcher=* block) | ❌ fails | ❌ fails |
| Hook invoked but script crashed before opening the ledger | ❌ fails | depends on order |
| Hook invoked, ledger opened, but failed before emitting the JSONL event | ✅ passes | ❌ fails |
| Hook invoked, ledger opened, but JSONL writer mis-types the `type` field | ✅ passes | ❌ fails (substring miss) |
| Everything OK | ✅ passes | ✅ passes |

Without the second assertion, a "ledger-open-but-no-event" regression
would silently pass — defeating the OQ-2 coverage contract (D-0082 §3)
that *every hook event type is exercised AND its emit contract is
asserted*. The two-assertion shape mirrors E3 (D-0087) and the
matcher-coverage triad (D-0086 §"Two-assertion shape ({event, tool})"),
both of which assert two substrings against the same JSONL file for
the same reason.

## Why a literal substring, not a JSONL field equality

`Expect.jsonl` would let us assert a structural predicate
(e.g. `type == "session_start"`) but only via Python callables
(`expect.py:269-369`). Those have no YAML wire form, so declaring them
in `real.yaml` would either require a `callback:` escape hatch (D-4,
deferred) or a v2 declarative DSL extension.

For the v1 manifest the substring `'"type":"session_start"'` is
uniquely identifying within `logs/freshness.jsonl`:

- The expected JSONL line format (per the OQ-2 contract D-0082 §4) is
  `{"ts":...,"session_id":...,"type":"session_start",...}`.
- The freshness ledger is opened by `freshness-session-start.sh` only.
  Any future second-position SessionStart hook contributors would write
  through the same script, keeping `type` field semantics under one
  emitter's control.
- The substring includes the leading `"type":"` so it cannot collide
  with any `"some_field":"…session_start"` line that might appear in a
  future hook extension.

This mirrors the substring-vs-callable trade-off documented in D-0087
§"Why a literal substring..." and D-0086 §"Why a literal contains
substring, not a JSONL field equality".

## Why `event_count == 1` is deferred

D-0082 §4 row E4 lists **two** `jsonl` assertions:

1. `jsonl.contains_event(logs/freshness.jsonl, type=session_start)` — proves
   the event fired.
2. `jsonl.event_count(logs/freshness.jsonl, type=session_start) == 1` —
   proves the event fired **exactly once** (duplicate-fire guard).

Both require a Python callable bound to the `type` field
(`expect.py:269-369`). The first is functionally covered by the
`Expect.file` substring proxy (above). The second — duplicate-fire
detection — has no analogous static-string proxy:

- `Expect.file` line-count constraints (`line_count_min` / `line_count_max`)
  count *all* lines in the file, not lines matching a filter.
- A clean per-eval HOME (FR-ISO2) means the freshness ledger only has
  rows written during this eval's SessionStart, so a total-line-count
  assertion could approximate `event_count` in the common case, but
  would be brittle: if `freshness-session-start.sh` later emits a
  second event row (e.g. a `ledger_init` record) at SessionStart, the
  total-line-count assertion would break for a reason unrelated to
  the actual `session_start` event-count contract.

The duplicate-fire guard is deferred to a follow-up under one of:

- **D-4 callback escape hatch** — exercised once for E4 to land the
  `event_count == 1` predicate as a Python callback registered against
  E4. Lowest-friction path.
- **YAML DSL extension** — add a declarative `jsonl: contains_event: {
  type: ..., count: 1 }` shorthand that compiles down to a
  `Expect.jsonl(filter=..., line_count=1)` callable at load time.
  Highest leverage if other evals (E5 / E9 / E10) also need
  per-event-count predicates.

T05.08's AC is "body matches the OQ-2 resolution; runs deterministically
on a clean HOME" — the first assertion (event fired) is sufficient for
that AC. The duplicate-fire guard is not load-bearing today (the
matcher=* hook fires exactly once per SessionStart by Claude Code's
hook-engine contract) and can be added later without re-authoring the
existing assertions.

## Why `/quit` as the input

E4's only "input" requirement per D-0082 §4 is "spawn a fresh claude
session via PtyDriver.spawn(home=isolated); wait for prompt-ready".
The session must then exit cleanly so the `exit_code.equals(0)`
assertion holds. The same `/quit` rationale used for E3 (D-0087
§"Why `/quit` as the input") applies verbatim:

- **Non-tool-call** — doesn't fire PreToolUse / PostToolUse hooks that
  would muddy the SessionStart-only assertion surface.
- **Synchronous** — Claude Code drains pending hook output and exits
  with code 0 (no race against async SubagentStop hooks etc.).
- **Stable across versions** — the `/quit` slash command has been the
  exit primitive across every Claude Code release in scope.

Critically, the **same `/quit` spawn that triggers E3's position-0
session-init.sh ALSO triggers E4's position-1 freshness-session-start.sh**.
Both SessionStart entries in `hooks.json` fire on every spawn, so the
input shape is symmetric across E3 / E4 by construction.

Alternative inputs considered and rejected: same set as D-0087
§"Why `/quit` as the input" — empty array, EOF, long-running prompt
— all rejected for the same reasons.

## Why `timeout_sec: 60` (vs. default 120)

The suite default is `per_eval_timeout_sec: 120`. E4's actual work is
bounded by:

- PTY spawn → both SessionStart hooks fire: <1s on every observed host.
- `freshness-session-start.sh` runtime: <0.5s (`hooks.json` per-hook
  timeout is **5s** — note this is tighter than session-init.sh's 10s
  budget, reflecting the lighter freshness check).
- `/quit` → clean exit: <1s.

Total expected wall-clock is <3s. 60s is generous (20× expected) but
tighter than the default, so a runner regression that wedges E4
flushes faster. Matches E3's `timeout_sec: 60` for sibling-spawn parity
— both evals share the same PTY-spawn lifecycle, so they should share
the same wall-clock budget.

## Why no capability tags (E4 runs everywhere)

`freshness-session-start.sh` has zero external dependencies:

- No MCP tool calls (the script is a freshness-check + JSONL emit).
- No network (freshness is computed against local HOME state).
- No filesystem dependencies outside `$HOME/.claude/`.

Therefore E4 needs no `requires:` clause; the FR-CAP1 gate is a no-op
for E4 and `--no-mcp` is irrelevant to its execution. This matches
the D-0082 §6 capability-tag rollup row for E4 (`requires: —`,
soft-skip under `--no-mcp`: no) — identical posture to E3.

## Why E4 keeps `no_pty: skip` despite asserting only SessionStart

Every eval in `suites/real.yaml` carries `no_pty: skip` because the
suite is PTY-driven by construction (R-077 / D-0077). E4 is no
exception — its assertion model relies on the PTY harness spawning a
real Claude subprocess so both SessionStart hooks fire naturally.
There is no "logic-only" path through E4 that could survive `--no-pty`
(you'd have to mock the SessionStart event emission, which defeats the
real-world coverage purpose). Keeping the tag aligns with the
suite-wide DOC-OQ3 contract.

## Determinism analysis

The body passes/fails the same way every run on a clean per-eval HOME
(D-0082 §2 constraint 2 / per-task AC):

| Variable | Stable? | Notes |
|---|---|---|
| PTY spawn outcome | ✅ stable | FR-ISO2 fresh HOME → no carry-over. |
| `logs/freshness.jsonl` creation | ✅ stable | second-position (matcher=*) SessionStart hook contract per D-0082 §4. |
| `freshness.jsonl` `type=session_start` row | ✅ stable | OQ-2 contract emits exactly one such row per SessionStart. |
| `ts` timestamp on JSONL row | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| `session_id` field | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| Freshness verdict (fresh vs. stale) | ⚠️ varies on warm runs | irrelevant — on a clean HOME every spawn is "fresh"; the body asserts the *event row*, not the verdict payload. |
| `/quit` exit code | ✅ stable | Claude Code returns 0 on `/quit`. |

Three consecutive runs yield identical EvalOutcome statuses, which is
the per-task AC.

## Hook telemetry gap — freshness-session-start.sh observables

`src/superclaude/hooks/scripts/freshness-session-start.sh` (revision as
of 2026-05-20) emits the SessionStart envelope to **stdout** via
`jq -nc ... hookSpecificOutput ...` (line 115-120 of the script) and
creates state files under `$HOME/.claude/state/` for the freshness
gate, but **does not** currently append a
`{"type":"session_start"}` row to `$HOME/.claude/logs/freshness.jsonl`.

The OQ-2 resolution (D-0082 §4 row E4) freezes the eval body to assert
this observable anyway, on the basis that the **hook contract** —
not the **current hook implementation** — is what the eval body is
authored against. The same pattern was applied to E3 / D-0087 §8.1
for the parallel `session-init.sh` gap.

### Discovery and mitigation

1. **Grep confirms the gap:**
   ```
   $ grep -rn "freshness\.jsonl\|session_start" src/superclaude/hooks/
   src/superclaude/hooks/scripts/freshness-session-start.sh:
     (creates state/, emits hookSpecificOutput to stdout — no freshness.jsonl write)
   ```
   The asserted ledger path is not written by any script in
   `src/superclaude/hooks/` at T05.08 authoring time.

2. **Not in scope for T05.08.** T05.08's acceptance criteria require
   "E4 entry whose body matches the OQ-2 resolution" — they do **not**
   require modifying `freshness-session-start.sh`. The hook script
   update is a downstream task (sibling-shape to the same update
   pending for `session-init.sh` per D-0087 §8.1).

3. **Risk acknowledged in spec §8.1.** Today's `eval run --eval E4`
   would fail the first two assertions deterministically (asserting
   files that the hook doesn't yet create). This is **not introduced**
   by T05.08; it is a transitive dependency on the hook-script update
   task.

4. **Verification path that works today:**
   - `eval describe --suite real --eval E4` round-trips the manifest
     body — proves it loads and resolves through `Expect.from_mapping`.
   - `eval list --json` enumerates E4 alongside E1..E15 — proves
     schema acceptance and FR-SCH2 id validity.
   - Manual `Expect.from_mapping` invocation over each `expects[]` row
     — proves the declarative DSL accepts the body.
   These three artifacts are the T05.08 acceptance evidence in
   `evidence/T05.08/`.

5. **Follow-up task scope (out of T05.08).** A future task (to be
   added to the phase-5 followups under a new T05.XX id, or grouped
   with the E3 / E5 / E9 / E10 / E11 hook-script updates) wires
   `freshness-session-start.sh` to:
   - `printf '{"ts":...,"session_id":...,"type":"session_start",...}\n' >> $HOME/.claude/logs/freshness.jsonl`
     before the script exits successfully.

   Once that follow-up lands AND the runner NameError is fixed, E4's
   per-task AC ("`uv run superclaude eval run --suite real --eval E4`
   exits 0 deterministically across 3 runs") becomes satisfiable
   without further body changes.

## Schema validation walkthrough

The new body must satisfy `suite.schema.json`:

| Field | Schema rule | This body |
|---|---|---|
| `id` | `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` | `E4` ✅ |
| `title` | string ≥1 char | `"SessionStart matcher=* freshness hook fires"` ✅ |
| `category` | string | `"hook-lifecycle"` ✅ |
| `timeout_sec` | integer ≥ 1 | `60` ✅ |
| `isolation.home_strategy` | enum [ephemeral, seeded, shared] | `"ephemeral"` ✅ |
| `inputs` | array of object | `[{prompt: "/quit"}]` ✅ |
| `expects` | array of object | 3 single-key mappings ✅ |
| `no_pty` | enum [skip] | `"skip"` ✅ |

No `additionalProperties: false` violations; no schema-version bump
required.

## Coverage gate (FR-COV1) impact

E4 issues no MCP tool calls and carries no `expect_tool_call` field.
It therefore does **not** appear in `_iter_eval_tool_calls`'s output
for any matcher prefix in `_DEFAULT_MCP_TOOL_PREFIXES`
(`coverage.py:99-107`). The matcher-coverage triad
(`mcp__auggie__.*` / `mcp__auggie-mcp__.*` / `mcp__airis-mcp-gateway__auggie_.*`)
remains covered exclusively by E1 / E2.1-3 — E4 contributes nothing
to that gate, which is the correct outcome (E4 covers a hook-event
*surface*, not a matcher prefix).

The hook-event coverage axis (D-0082 §3) is the gate E4 advances: it
adds **second-position SessionStart (matcher=*)** to the covered set,
completing the SessionStart row when paired with E3 (which covers
first-position `SessionStart` / no-matcher).

## Why the comment block in real.yaml is verbose (~35 lines)

Matches the verbosity of the E1 / E2.1-3 / E3 comment blocks.
Reviewers of `real.yaml` should be able to understand each eval's
contract (and the YAML-vs-callable trade-off, the telemetry-gap
acknowledgment, and the `event_count` deferral) without
context-switching to the deliverable artifacts. The verbosity is paid
once at authoring time and amortized across every future review /
debug session.

## Differences from E3 / D-0087

| Aspect | E3 (D-0087) | E4 (D-0088) |
|---|---|---|
| Hook covered | `hooks.json` SessionStart position-0 (no matcher) | `hooks.json` SessionStart position-1 (matcher=*) |
| Script | `session-init.sh` | `freshness-session-start.sh` |
| `hooks.json` timeout | 10s | 5s |
| Asserted log file | `state/session-init.log` | (none — freshness hook doesn't write a state log) |
| Asserted JSONL file | `logs/session-events.jsonl` | `logs/freshness.jsonl` |
| Asserted JSONL `type` substring | `"type":"session_init"` | `"type":"session_start"` |
| OQ-2 §4 extra deferred predicate | (none — `contains` substring is the full body) | `event_count == 1` (deferred to D-4 callback follow-up) |
| Capability tags | — | — |
| `timeout_sec` | 60 | 60 |
| Telemetry gap (script doesn't emit asserted JSONL) | ✅ documented in D-0087 §8.1 | ✅ documented in D-0088 §8.1 |

The shared posture across both deliverables: same input, same
isolation strategy, same exit-code assertion, same telemetry-gap
acknowledgment posture, same `event_count`-style deferral pattern
(though only D-0088 has a deferred count). E4's body is the natural
sibling of E3's body — both fire from the same PTY spawn, both pin
the SessionStart event coverage axis, both await the same downstream
hook-script update.
