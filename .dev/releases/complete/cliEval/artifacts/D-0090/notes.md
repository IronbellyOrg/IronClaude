# D-0090 — Design notes

## Why three inputs instead of two

E3, E4, and E5 used one or two inputs. E6 requires **three**:

1. **Write seed** — `"Use the Write tool to create a file named
   edited.txt under the current working directory with the single line
   'before'."` Creates the scratch file so the subsequent Edit has a
   target.
2. **Edit fire** — `"Use the Edit tool on edited.txt to replace
   'before' with 'edited'."` Triggers the PreToolUse hook on the Edit
   matcher branch — the assertion target.
3. **Clean exit** — `"/quit"` Lets `exit_code.equals(0)` pin the PTY
   teardown contract (same pattern as E3 / E4 / E5).

Why not just one Edit prompt against a nonexistent file? The
`freshness-pre-edit.sh` script gates Edit on a prior Read of the
target (the "freshness" check that gives the hook its name). Without
either a prior Read or a prior Write that creates the file, the Edit
PreToolUse hook would either:

- (a) deny the operation (the agent never reaches a "real" Edit call),
  or
- (b) fall open via the `no_prior_read` branch at lines 78-87 of
  `freshness-pre-edit.sh` (the "create_allowed" path — but only if
  the path doesn't exist yet, which contradicts an Edit on a
  pre-existing file).

The seeding Write threads the needle: it creates the file (so the Edit
has a target), and because the file is created *by the same session*,
the `no_prior_read` branch falls open on the Write itself (path
doesn't exist yet → `create_allowed`), then the Edit follows with the
freshness-check satisfied via the in-session write history.

Alternatives considered and rejected:

| Alternative | Why rejected |
|---|---|
| `[{prompt: "Edit foo"}, {prompt: "/quit"}]` (single Edit, no seed) | the agent must Read or Write the target first — no Read = blocked; no Write = no target. Edit alone produces a deny or a `no_prior_read` route that doesn't fire the Edit-branch matcher cleanly. |
| `[{prompt: "Read X"}, {prompt: "Edit X"}, {prompt: "/quit"}]` (Read seed) | requires a pre-existing scratch file in the per-eval HOME. Adds setup complexity (where does the file come from?) and conflicts with FR-ISO2 fresh-HOME determinism. |
| `[{prompt: "Edit nonexistent.txt"}, {prompt: "/quit"}]` (nonexistent target) | fires the `no_prior_read` `create_allowed` branch — but Edit on a nonexistent file produces an error, not a successful Edit. The assertion `file.exists(edited.txt)` would fail. |
| `[{prompt: "Write A"}, {prompt: "Edit B"}, {prompt: "/quit"}]` (mismatched paths) | the seed creates a different file than the Edit target — Edit then routes through `no_prior_read` create-or-fail rather than firing on an existing target. |

The chosen `[Write, Edit, /quit]` shape is the minimum viable input
that simultaneously: (a) creates a target the Edit can hit; (b) fires
the PreToolUse hook **on the Edit matcher branch** (not on Write, which
goes through the same hook script but with `matcher=Write`); (c)
produces a deterministic post-Edit file state that the
`file.exists(edited.txt)` assertion can verify.

## Why two assertions for matcher discrimination

The minimum-viable "did the PreToolUse hook fire" assertion could be
just one of:

- `file.exists(logs/freshness.jsonl)` — proves the ledger was opened.
- `file(logs/freshness.jsonl, contains: '"type":"pre_edit"')` — proves
  a `pre_edit` event row was emitted.
- `file(logs/freshness.jsonl, contains: '"matcher":"Edit"')` — proves
  the Edit branch specifically fired.

We assert **all three** because they fail under different failure
modes, following the matrix established in D-0086 §"Two-assertion
shape" and extended for matcher-group discrimination:

| Failure mode | `freshness.jsonl` exists | `"type":"pre_edit"` substring | `"matcher":"Edit"` substring |
|---|---|---|---|
| Hook never invoked (matcher block missing from `hooks.json`) | ❌ (assuming SessionStart didn't open ledger) | ❌ | ❌ |
| Hook invoked but script crashed before ledger open | depends on order | ❌ | ❌ |
| Hook invoked, ledger opened, but failed before emitting event | ✅ | ❌ | ❌ |
| Hook invoked, event emitted, but with wrong `type` value | ✅ | ❌ | ❌ |
| Hook invoked, `type=pre_edit` emitted, but `matcher` field missing | ✅ | ✅ | ❌ |
| Hook invoked, `type=pre_edit` emitted, but matcher routed wrong branch (e.g. Write instead of Edit) | ✅ | ✅ | ❌ |
| Hook invoked, all fields correct (E6 success) | ✅ | ✅ | ✅ |

**The third assertion is the matcher-discrimination row.** Without it,
a regression that wires the PreToolUse hook only to Write but not Edit
(or vice versa) would pass the first two assertions but break the
matcher-coverage contract. Since E7 and E8 will independently assert
`"matcher":"Write"` and `"matcher":"mcp__serena__*"` respectively
against the *same hook script and same ledger file*, E6's `Edit`-
specific assertion is what distinguishes the three coverage evals.

This mirrors the D-0086 §"Two-assertion shape ({event, tool})" pattern
used for the E2.1-3 matcher-coverage triad: the first substring pins
the **event class**, the second pins the **matcher-routed instance**.

## Why a literal substring, not a JSONL field equality

`Expect.jsonl` would let us assert structural predicates
(`type == "pre_edit"`, `matcher == "Edit"`) but only via Python
callables (`expect.py:269-369`). Those have no YAML wire form, so
declaring them in `real.yaml` would either require a `callback:`
escape hatch (D-4, deferred) or a v2 declarative DSL extension.

For the v1 manifest the substrings `'"type":"pre_edit"'` and
`'"matcher":"Edit"'` are uniquely identifying within
`logs/freshness.jsonl`:

- The expected JSONL line format (per the OQ-2 contract D-0082 §4) is
  `{"ts":...,"session_id":...,"type":"pre_edit","matcher":"Edit",...}`.
- The freshness ledger writers in scope for the Edit matcher branch is
  only `freshness-pre-edit.sh` — no other hook emits `pre_edit`-typed
  rows.
- The substrings include the leading `"type":"` and `"matcher":"` so
  they cannot collide with adjacent fields (e.g. a hypothetical
  `"some_other_field":"…pre_edit"` line wouldn't match because the
  prefix `"type":"` would not match).

This mirrors the substring-vs-callable trade-off documented in
D-0086 / D-0087 / D-0088 / D-0089.

## Why `event_count == 1` is deferred

D-0082 §4 row E6 lists a secondary assertion
`event_count(type=pre_edit, matcher=Edit) == 1` — exactly one
Edit-branch PreToolUse fire per the single Edit prompt.

This predicate requires a Python callable bound to two JSONL fields
(`type` + `matcher`), expressible only through
`Expect.jsonl(filter=..., line_count=...)`. Same YAML-expressibility
limit as the E3/E4/E5 deferral.

The substring assertions cover the "at least one matched row" semantic;
the precise per-input cardinality (`== len([p for p in inputs if p
matches Edit])`) is deferred until either:

- **D-4 callback escape hatch** — exercised for E6 to land the
  `event_count == 1` predicate as a Python callback registered
  against E6. Lowest-friction path.
- **YAML DSL extension** — add a declarative `jsonl: contains_event:
  { type: ..., matcher: ..., count: 1 }` shorthand that compiles down
  to `Expect.jsonl(filter=..., line_count=...)` at load time. Highest
  leverage if E7 / E8 / E9-E11 also need count predicates.

T05.10's AC is "body matches the OQ-2 resolution; runs deterministically
on a clean HOME" — the substring assertion (event fired at least
once with the correct matcher) is sufficient for that AC. The exact
count guard is not load-bearing today (one Edit prompt → one
PreToolUse fire by hook-engine contract) and can be added later
without re-authoring the existing assertions.

## Why `file.exists(edited.txt)` is the fourth assertion

E3/E4/E5 used three assertions (file exists + type substring + exit
code). E6 adds a **fourth**: `file.exists(edited.txt)`.

The fourth assertion proves the Edit operation completed end-to-end.
Without it, a regression where the PreToolUse hook fires but the Edit
itself is silently dropped (e.g. the hook returns a malformed
`hookSpecificOutput` envelope that Claude Code interprets as "skip the
tool call") would pass the first three assertions — the hook still
fired and emitted its row — but the user's intent (the Edit happening)
wouldn't be realized. The scratch file would still contain `'before'`
not `'edited'`, OR the file might not exist if the seeding Write was
also dropped.

The assertion is **existence-only**, not content-equality, because:

- The Edit's success is bounded by Claude Code's Edit-tool semantics
  (replace `'before'` with `'edited'`), which is itself implementation-
  dependent — the hook contract is what's under test, not the Edit
  tool's correctness.
- Content equality would require asserting the file contains
  `'edited'` (post-Edit) and NOT `'before'` (which would still match a
  partial-edit failure mode). Two-substring content assertions on a
  small file are brittle to whitespace / newline variation.
- Existence is the minimum proof that "the agent did *something*" to
  the file — the hook fired AND the action propagated to the
  filesystem. Combined with the JSONL row substrings, this is
  sufficient AC coverage.

`_resolve_path` (expect.py:79-91) resolves the relative path against
`ctx.home_path`, so `edited.txt` evaluates to
`<per-eval-HOME>/edited.txt`. The seeding Write creates it in the
agent's CWD, which is `ctx.home_path` (the per-eval scratch root).

## Why `timeout_sec: 60` (vs. default 120)

The suite default is `per_eval_timeout_sec: 120`. E6's actual work is
bounded by:

- PTY spawn → both SessionStart hooks fire: <1s.
- Write prompt submission → UserPromptSubmit fires → agent reasons →
  Write tool call → PreToolUse fires (matcher=Write) → Write succeeds:
  ~5-15s depending on agent reasoning.
- Edit prompt → UserPromptSubmit fires → agent reasons → Edit tool
  call → PreToolUse fires (matcher=Edit) → Edit succeeds: another
  ~5-15s.
- `/quit` → clean exit: <1s.

Worst-case wall-clock is dominated by agent reasoning between prompts.
For an offline / no-MCP host the agent uses canned reasoning; for a
host with MCP it might invoke tools to "decide" what to do, but the
core path remains bounded.

60s is generous (well above the observed steady-state of <30s for
this 3-prompt sequence) but tighter than the default, so a runner
regression that wedges E6 flushes faster.

Matches E3 / E4 / E5's `timeout_sec: 60` for sibling-spawn parity —
all four evals share the PTY-spawn lifecycle.

## Why no capability tags (E6 runs everywhere)

The Edit tool is built into Claude Code itself — no MCP server
required. `freshness-pre-edit.sh` is a local-only script with zero
external dependencies:

- No MCP tool calls (the script is a freshness-check + JSONL emit).
- No network.
- No filesystem dependencies outside `$HOME/.claude/`.

Therefore E6 needs no `requires:` clause; the FR-CAP1 gate is a no-op
for E6 and `--no-mcp` is irrelevant to its execution. This matches
the D-0082 §6 capability-tag rollup row for E6 (`requires: —`,
soft-skip under `--no-mcp`: no) — identical posture to E3 / E4 / E5,
and distinct from sibling E8 which will require
`mcp_server.serena`.

## Why E6 keeps `no_pty: skip`

Every eval in `suites/real.yaml` carries `no_pty: skip` because the
suite is PTY-driven by construction (R-077 / D-0077). E6 is no
exception — its assertion model relies on the PTY harness spawning a
real Claude subprocess and **injecting tool-eliciting prompts via
the PTY write channel** so the PreToolUse hook fires naturally on
the agent's actual tool invocation. There is no "logic-only" path
through E6 that could survive `--no-pty` (you'd have to mock both
the tool-call event emission AND the file-system side-effect, which
defeats the real-world coverage purpose).

## Determinism analysis

The body passes/fails the same way every run on a clean per-eval HOME
(D-0082 §2 constraint 2 / per-task AC):

| Variable | Stable? | Notes |
|---|---|---|
| PTY spawn outcome | ✅ stable | FR-ISO2 fresh HOME → no carry-over. |
| `logs/freshness.jsonl` creation | ✅ stable | the freshness ledger is opened by `freshness-session-start.sh` on every spawn; E6 doesn't depend on which hook opened it. |
| Write tool call success | ✅ stable | per-eval HOME has empty CWD; Write creates `edited.txt` with `'before'` deterministically. |
| Edit tool call success | ✅ stable | preceding Write seed makes the Edit-on-pre-existing-file path deterministic. |
| `freshness.jsonl` `type=pre_edit` row | ✅ stable | OQ-2 contract emits one such row per PreToolUse Edit fire. |
| `freshness.jsonl` `matcher=Edit` row | ✅ stable | Edit branch of the matcher group fires on each Edit tool invocation. |
| `edited.txt` existence | ✅ stable | seeded by Write, modified by Edit, persists. |
| `ts` timestamp on JSONL row | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| `session_id` field | ⚠️ varies | **not asserted against**. |
| `tool_call_idx` field | ⚠️ varies | **not asserted against**. |
| `recent_read_age_sec` field | ⚠️ varies | **not asserted against**. |
| `decision` / `reason` fields | ⚠️ varies | **not asserted against**. |
| Agent reasoning text | ⚠️ varies | **not asserted against** — body only pins observables. |
| `/quit` exit code | ✅ stable | Claude Code returns 0 on `/quit`. |

Three consecutive runs yield identical EvalOutcome statuses, which is
the per-task AC. Note the deterministic surface here is wider than
the test surface: agent reasoning text varies, but no assertion
inspects it.

## Hook telemetry gap — freshness-pre-edit.sh observables

`src/superclaude/hooks/scripts/freshness-pre-edit.sh` (revision as of
2026-05-20, lines 108-119) writes to
**`$HOME/.claude/logs/freshness-hook.jsonl`** (note the `-hook` suffix)
with the JSONL envelope:

```json
{"ts":"...","event":"PreToolUse","tool":"Edit","path":"...",
 "session_id":"...","tool_call_idx":N,"decision":"...","reason":"..."}
```

The OQ-2 D-0082 §4 body shape — which T05.10 lands verbatim — asserts
against `$HOME/.claude/logs/freshness.jsonl` (no `-hook` suffix) and
uses different field names: `type=pre_edit` (script uses `event=PreToolUse`)
and `matcher=Edit` (script uses `tool=Edit`).

**Two divergences** between the script's current emit and the OQ-2
contract:

1. **Path**: `logs/freshness-hook.jsonl` vs. `logs/freshness.jsonl`.
2. **Field names**: `event` / `tool` vs. `type` / `matcher`.

The OQ-2 resolution (D-0082 §4) freezes the eval body to assert
against the **hook contract** — not the **current hook implementation**.
The same pattern was applied to E3 / D-0087 §8.1 for the parallel
`session-init.sh` gap, E4 / D-0088 §8.1 for `freshness-session-start.sh`,
and E5 / D-0089 §8.1 for `freshness-user-prompt.sh`.

### Discovery and mitigation

1. **Grep + Read confirms the gap:**
   ```
   $ grep -n "freshness" src/superclaude/hooks/scripts/freshness-pre-edit.sh
     Lines 108-119: appendln to $HOME/.claude/logs/freshness-hook.jsonl
     Field schema: {ts, event:"PreToolUse", tool:<tool_name>, path,
                    session_id, tool_call_idx, decision, reason}
   ```
   The asserted ledger path is not written by any script in
   `src/superclaude/hooks/` on the normal PreToolUse path at T05.10
   authoring time.

2. **Not in scope for T05.10.** T05.10's acceptance criteria require
   "E6 entry whose body matches the OQ-2 resolution" — they do **not**
   require modifying `freshness-pre-edit.sh`. The hook script update
   is a downstream task (sibling-shape to the pending updates for
   `session-init.sh` / `freshness-session-start.sh` /
   `freshness-user-prompt.sh`).

3. **Risk acknowledged in spec §8.1.** Today's `eval run --eval E6`
   would fail every JSONL substring assertion deterministically (the
   file may exist from the SessionStart hook chain, but neither
   `pre_edit` nor `Edit` substrings appear because the actual emit
   uses `event=PreToolUse` and `tool=Edit` in a different file). This
   is **not introduced** by T05.10; it is a transitive dependency on
   the hook-script update task.

4. **Verification path that works today:**
   - `eval describe --suite real --eval E6` round-trips the manifest
     body — proves it loads and resolves through `Expect.from_mapping`.
   - `eval list --json` enumerates E6 alongside E1..E15 — proves
     schema acceptance and FR-SCH2 id validity.
   - Manual `Expect.from_mapping` invocation over each `expects[]` row
     — proves the declarative DSL accepts the body.
   These three artifacts are the T05.10 acceptance evidence in
   `evidence/T05.10/`.

5. **Follow-up task scope (out of T05.10).** A future task (to be
   added to the phase-5 followups under a new T05.XX id, or grouped
   with the E3 / E4 / E5 hook-script updates) wires
   `freshness-pre-edit.sh` to:
   - append `{"ts":...,"session_id":...,"turn":...,"type":"pre_edit",
     "matcher":<tool_name>,...}\n` to
     `$HOME/.claude/logs/freshness.jsonl` (no `-hook` suffix) on every
     PreToolUse fire — idempotent per tool invocation.

   Once that follow-up lands AND the runner NameError is fixed, E6's
   per-task AC ("`uv run superclaude eval run --suite real --eval E6`
   exits 0 deterministically across 3 runs") becomes satisfiable
   without further body changes.

## Schema validation walkthrough

The new body must satisfy `suite.schema.json`:

| Field | Schema rule | This body |
|---|---|---|
| `id` | `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` | `E6` ✅ |
| `title` | string ≥1 char | `"PreToolUse Edit matcher fires"` ✅ |
| `category` | string | `"hook-lifecycle"` ✅ |
| `timeout_sec` | integer ≥ 1 | `60` ✅ |
| `isolation.home_strategy` | enum [ephemeral, seeded, shared] | `"ephemeral"` ✅ |
| `inputs` | array of object | 3-element `[{prompt: ...}, {prompt: ...}, {prompt: "/quit"}]` ✅ |
| `expects` | array of object | 5 single-key mappings ✅ |
| `no_pty` | enum [skip] | `"skip"` ✅ |

No `additionalProperties: false` violations; no schema-version bump
required.

## Coverage gate (FR-COV1) impact

E6 issues no MCP tool calls in the assertion surface and carries no
`expect_tool_call` field. The agent's Write and Edit tool calls are
**built-in** Claude Code tools, not MCP tools — they do not appear in
`_iter_eval_tool_calls`'s output for any matcher prefix in
`_DEFAULT_MCP_TOOL_PREFIXES` (`coverage.py:99-107`). The matcher-
coverage triad (`mcp__auggie__.*` / `mcp__auggie-mcp__.*` /
`mcp__airis-mcp-gateway__auggie_.*`) remains covered exclusively by
E1 + E2.1-3 — E6 contributes nothing to that gate, which is the
correct outcome (E6 covers a hook-event *surface*, not an MCP-matcher
prefix).

The hook-event coverage axis (D-0082 §3) is the gate E6 advances: it
adds **PreToolUse (matcher=Edit)** to the covered set. E7 / E8 will
complete the PreToolUse matcher-group coverage when they land.

## Why the comment block in real.yaml is verbose (~65 lines)

Matches the verbosity of the E1 / E2.1-3 / E3 / E4 / E5 comment blocks.
Reviewers of `real.yaml` should be able to understand each eval's
contract (and the matcher-discrimination two-substring shape, the
telemetry-gap acknowledgment, the per-input count deferral, the
three-input rationale for matcher discrimination) without
context-switching to the deliverable artifacts. The verbosity is paid
once at authoring time and amortized across every future review /
debug session.

## Differences from E3 / E4 / E5 siblings

| Aspect | E3 (D-0087) | E4 (D-0088) | E5 (D-0089) | E6 (D-0090) |
|---|---|---|---|---|
| Hook covered | SessionStart pos-0 | SessionStart pos-1 matcher=* | UserPromptSubmit no-matcher | PreToolUse matcher=Edit |
| Script | `session-init.sh` | `freshness-session-start.sh` | `freshness-user-prompt.sh` | `freshness-pre-edit.sh` |
| `hooks.json` timeout | 10s | 5s | 3s | **5s** |
| Asserted log file | `state/session-init.log` | (none) | (none) | (none) |
| Asserted JSONL file | `logs/session-events.jsonl` | `logs/freshness.jsonl` | `logs/freshness.jsonl` | `logs/freshness.jsonl` |
| Asserted JSONL `type` substring | `"type":"session_init"` | `"type":"session_start"` | `"type":"user_prompt"` | `"type":"pre_edit"` |
| Asserted matcher-discrimination substring | (none) | (none) | (none) | **`"matcher":"Edit"`** |
| Asserted file existence (beyond logs) | session-init.log | (none) | (none) | **edited.txt** |
| OQ-2 §4 extra deferred predicate | (none) | `event_count == 1` | `event_count >= 1 per injected prompt` | `event_count == 1` |
| Inputs | `[{prompt: "/quit"}]` | `[{prompt: "/quit"}]` | `[{prompt: "echo test"}, {prompt: "/quit"}]` | `[{prompt: Write seed}, {prompt: Edit fire}, {prompt: "/quit"}]` |
| Why extra input(s) | n/a — SessionStart fires before any prompt | n/a — SessionStart fires before any prompt | content prompt required to fire UserPromptSubmit | Edit requires both a target (Write seed) and an Edit invocation prompt |
| Capability tags | — | — | — | — |
| `timeout_sec` | 60 | 60 | 60 | 60 |
| Telemetry gap (script doesn't emit asserted JSONL) | ✅ D-0087 §8.1 | ✅ D-0088 §8.1 | ✅ D-0089 §8.1 | ✅ D-0090 §8.1 |

The shared posture across all four siblings: same isolation strategy,
same exit-code assertion, same telemetry-gap acknowledgment posture,
same `event_count`-style deferral pattern. E6 extends the pattern with
(a) a matcher-discrimination substring (the second `"matcher":"Edit"`
assertion) and (b) a side-effect file-existence assertion (the
`edited.txt` row) — both new for the PreToolUse-tool-fires class of
evals.

## Three-substring shape is unique to PreToolUse matcher-group siblings

E6 / E7 / E8 will share the JSONL ledger but assert *different* matcher
substrings (`"matcher":"Edit"`, `"matcher":"Write"`,
`"matcher":"mcp__serena__..."`) against the same hook script's output.
This is the first place in the manifest where three coverage evals
share a hook script and discriminate by matcher value. The
three-substring shape (`exists`, `type`, `matcher`) is the structural
fingerprint of the PreToolUse matcher-group coverage strategy.

The E2.1-3 matcher-coverage triad (D-0086) uses the same pattern but
in the MCP-tool-call dimension (`mcp__auggie__.*` /
`mcp__auggie-mcp__.*` / `mcp__airis-mcp-gateway__auggie_.*`); E6-E8
extends the pattern to the PreToolUse-hook-matcher dimension. Both
triads use two-substring discrimination (event + matcher/tool) — the
file-existence assertion is unique to E6 because it has a filesystem
side-effect to verify.
