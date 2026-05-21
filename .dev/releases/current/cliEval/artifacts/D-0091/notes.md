# D-0091 — Design notes

## Why two inputs instead of three (departure from E6)

E6 required **three** inputs (Write seed → Edit fire → /quit) because
the Edit operation requires a pre-existing target file. E7 requires
only **two**:

1. **Write fire** — `"Use the Write tool to create a file named
   written.txt under the current working directory with the single
   line 'hello'."` Creates the file and fires the PreToolUse hook on
   the Write matcher branch — the assertion target.
2. **Clean exit** — `"/quit"` Lets `exit_code.equals(0)` pin the PTY
   teardown contract (same pattern as E3 / E4 / E5 / E6).

Why no seed prompt for E7? `freshness-pre-edit.sh`'s `no_prior_read`
branch (lines 78-87 of the script) explicitly falls open on a
**not-yet-existing** path via the `create_allowed` route. A single
Write against a fresh path on a clean per-eval HOME is exactly the
intended `create_allowed` path:

- The Write target does not exist yet (clean HOME).
- The hook's `no_prior_read` predicate evaluates true (no prior Read
  of the path is on record).
- `create_allowed` permits the Write.
- The Write tool call fires PreToolUse on the **Write matcher branch**.
- The script emits its `pre_edit`-typed row with `matcher=Write` to
  the freshness ledger.
- `written.txt` exists post-Write.

This is the simplest possible PreToolUse fire on a fresh HOME — no
synchronization prompt is needed because Write *creates* its own
target, unlike Edit which *requires* one.

Alternatives considered and rejected:

| Alternative | Why rejected |
|---|---|
| `[{prompt: Write fire}, {prompt: /quit}]` (chosen) | Minimum viable: creates target and fires the hook in one tool call. |
| `[{prompt: "Read X first"}, {prompt: "Write X"}, {prompt: /quit}]` | Pre-Read of a nonexistent file is undefined / errors; adds zero coverage value vs. the one-prompt version. |
| `[{prompt: "Write A then Write B"}, {prompt: /quit}]` (multiple Writes) | Generates two `pre_edit` rows + two `matcher=Write` rows. Substring assertions still pass (they're presence-only, not count), but the body diverges from the OQ-2 §4 "single Write" shape and pollutes the determinism story. |
| `[{prompt: Write fire}]` (no /quit) | The session may not exit cleanly within `timeout_sec`; `exit_code.equals(0)` either fails or relies on PTY teardown semantics. /quit is the documented clean-exit path. |

The chosen `[Write, /quit]` shape is the minimum viable input that
simultaneously: (a) fires the PreToolUse hook **on the Write matcher
branch** specifically (the assertion target); (b) creates a file that
the `file.exists(written.txt)` assertion can verify; (c) terminates
cleanly so the exit-code assertion holds.

## Why two assertions for matcher discrimination (same as E6)

The minimum-viable "did the PreToolUse hook fire" assertion could be
just one of:

- `file.exists(logs/freshness.jsonl)` — proves the ledger was opened.
- `file(logs/freshness.jsonl, contains: '"type":"pre_edit"')` — proves
  a `pre_edit` event row was emitted.
- `file(logs/freshness.jsonl, contains: '"matcher":"Write"')` — proves
  the Write branch specifically fired.

We assert **all three** because they fail under different failure
modes, following the matrix established in D-0086 §"Two-assertion
shape" and extended for matcher-group discrimination by D-0090 §"Why
two assertions for matcher discrimination":

| Failure mode | `freshness.jsonl` exists | `"type":"pre_edit"` substring | `"matcher":"Write"` substring |
|---|---|---|---|
| Hook never invoked (matcher block missing from `hooks.json`) | ❌ (assuming SessionStart didn't open ledger) | ❌ | ❌ |
| Hook invoked but script crashed before ledger open | depends on order | ❌ | ❌ |
| Hook invoked, ledger opened, but failed before emitting event | ✅ | ❌ | ❌ |
| Hook invoked, event emitted, but with wrong `type` value | ✅ | ❌ | ❌ |
| Hook invoked, `type=pre_edit` emitted, but `matcher` field missing | ✅ | ✅ | ❌ |
| Hook invoked, `type=pre_edit` emitted, but matcher routed wrong branch (e.g. Edit instead of Write) | ✅ | ✅ | ❌ |
| Hook invoked, all fields correct (E7 success) | ✅ | ✅ | ✅ |

**The third assertion is the matcher-discrimination row.** Without it,
a regression that wires the PreToolUse hook only to Edit but not Write
(or vice versa) would pass the first two assertions but break the
matcher-coverage contract. Since E6 and E8 independently assert
`"matcher":"Edit"` and `"matcher":"mcp__serena__*"` respectively
against the *same hook script and same ledger file*, E7's `Write`-
specific assertion is what distinguishes the three coverage evals.

This mirrors the D-0086 §"Two-assertion shape ({event, tool})" pattern
used for the E2.1-3 matcher-coverage triad and is structurally
identical to E6 (D-0090) — only the matcher-pin substring value differs
(`"matcher":"Write"` here vs `"matcher":"Edit"` in E6).

## Why a literal substring, not a JSONL field equality

`Expect.jsonl` would let us assert structural predicates
(`type == "pre_edit"`, `matcher == "Write"`) but only via Python
callables (`expect.py:269-369`). Those have no YAML wire form, so
declaring them in `real.yaml` would either require a `callback:`
escape hatch (D-4, deferred) or a v2 declarative DSL extension.

For the v1 manifest the substrings `'"type":"pre_edit"'` and
`'"matcher":"Write"'` are uniquely identifying within
`logs/freshness.jsonl`:

- The expected JSONL line format (per the OQ-2 contract D-0082 §4) is
  `{"ts":...,"session_id":...,"type":"pre_edit","matcher":"Write",...}`.
- The freshness ledger writer in scope for the Write matcher branch is
  only `freshness-pre-edit.sh` — no other hook emits `pre_edit`-typed
  rows.
- The substrings include the leading `"type":"` and `"matcher":"` so
  they cannot collide with adjacent fields (e.g. a hypothetical
  `"some_other_field":"…Write"` line wouldn't match because the
  prefix `"matcher":"` would not match).

This mirrors the substring-vs-callable trade-off documented in
D-0086 / D-0087 / D-0088 / D-0089 / D-0090.

## Why `event_count == 1` is deferred

D-0082 §4 row E7 lists a secondary assertion
`event_count(type=pre_edit, matcher=Write) == 1` — exactly one
Write-branch PreToolUse fire per the single Write prompt.

This predicate requires a Python callable bound to two JSONL fields
(`type` + `matcher`), expressible only through
`Expect.jsonl(filter=..., line_count=...)`. Same YAML-expressibility
limit as the E3/E4/E5/E6 deferrals.

The substring assertions cover the "at least one matched row" semantic;
the precise per-input cardinality (`== len([p for p in inputs if p
matches Write])`) is deferred until either:

- **D-4 callback escape hatch** — exercised for E7 to land the
  `event_count == 1` predicate as a Python callback registered
  against E7. Lowest-friction path.
- **YAML DSL extension** — add a declarative `jsonl: contains_event:
  { type: ..., matcher: ..., count: 1 }` shorthand that compiles down
  to `Expect.jsonl(filter=..., line_count=...)` at load time. Highest
  leverage if E6 / E7 / E8 / E9-E11 also need count predicates.

T05.11's AC is "body matches the OQ-2 resolution; runs deterministically
on a clean HOME" — the substring assertion (event fired at least
once with the correct matcher) is sufficient for that AC. The exact
count guard is not load-bearing today (one Write prompt → one
PreToolUse fire by hook-engine contract) and can be added later
without re-authoring the existing assertions.

## Why `file.exists(written.txt)` is the fourth assertion

E3/E4/E5 used three assertions (file exists + type substring + exit
code). E6 added a **fourth**: `file.exists(edited.txt)`. E7 inherits
the same four-assertion shape with `written.txt` swapped in.

The fourth assertion proves the Write operation completed end-to-end.
Without it, a regression where the PreToolUse hook fires but the Write
itself is silently dropped (e.g. the hook returns a malformed
`hookSpecificOutput` envelope that Claude Code interprets as "skip the
tool call") would pass the first three assertions — the hook still
fired and emitted its row — but the user's intent (the file being
created) wouldn't be realized.

The assertion is **existence-only**, not content-equality, because:

- The Write's success is bounded by Claude Code's Write-tool semantics
  (create file with given content), which is itself implementation-
  dependent — the hook contract is what's under test, not the Write
  tool's correctness.
- Content equality would require asserting the file contains `'hello'`
  exactly. Whitespace / newline variation in the agent's actual
  payload (the agent might write `hello\n` vs `hello` vs add a leading
  blank line) makes content assertions brittle without further
  normalization.
- Existence is the minimum proof that "the agent did *something*" —
  the hook fired AND the action propagated to the filesystem. Combined
  with the JSONL row substrings, this is sufficient AC coverage.

`_resolve_path` (expect.py:79-91) resolves the relative path against
`ctx.home_path`, so `written.txt` evaluates to
`<per-eval-HOME>/written.txt`. The Write tool call creates it in the
agent's CWD, which is `ctx.home_path` (the per-eval scratch root).

## Why `timeout_sec: 60` (vs. default 120)

The suite default is `per_eval_timeout_sec: 120`. E7's actual work is
bounded by:

- PTY spawn → both SessionStart hooks fire: <1s.
- Write prompt submission → UserPromptSubmit fires → agent reasons →
  Write tool call → PreToolUse fires (matcher=Write) → Write succeeds:
  ~5-15s depending on agent reasoning.
- `/quit` → clean exit: <1s.

Worst-case wall-clock is dominated by agent reasoning between prompts.
For an offline / no-MCP host the agent uses canned reasoning; for a
host with MCP it might invoke tools to "decide" what to do, but the
core path remains bounded.

60s is generous (well above the observed steady-state of <20s for
this 2-prompt sequence — E7 is faster than E6 because it has one
fewer tool call) but tighter than the default, so a runner regression
that wedges E7 flushes faster.

Matches E3 / E4 / E5 / E6's `timeout_sec: 60` for sibling-spawn
parity — all five evals share the PTY-spawn lifecycle.

## Why no capability tags (E7 runs everywhere)

The Write tool is built into Claude Code itself — no MCP server
required. `freshness-pre-edit.sh` is a local-only script with zero
external dependencies:

- No MCP tool calls (the script is a freshness-check + JSONL emit).
- No network.
- No filesystem dependencies outside `$HOME/.claude/`.

Therefore E7 needs no `requires:` clause; the FR-CAP1 gate is a no-op
for E7 and `--no-mcp` is irrelevant to its execution. This matches
the D-0082 §6 capability-tag rollup row for E7 (`requires: —`,
soft-skip under `--no-mcp`: no) — identical posture to E3 / E4 / E5 /
E6, and distinct from sibling E8 which will require
`mcp_server.serena`.

## Why E7 keeps `no_pty: skip`

Every eval in `suites/real.yaml` carries `no_pty: skip` because the
suite is PTY-driven by construction (R-077 / D-0077). E7 is no
exception — its assertion model relies on the PTY harness spawning a
real Claude subprocess and **injecting tool-eliciting prompts via
the PTY write channel** so the PreToolUse hook fires naturally on
the agent's actual tool invocation. There is no "logic-only" path
through E7 that could survive `--no-pty` (you'd have to mock both
the tool-call event emission AND the file-system side-effect, which
defeats the real-world coverage purpose).

## Determinism analysis

The body passes/fails the same way every run on a clean per-eval HOME
(D-0082 §2 constraint 2 / per-task AC):

| Variable | Stable? | Notes |
|---|---|---|
| PTY spawn outcome | ✅ stable | FR-ISO2 fresh HOME → no carry-over. |
| `logs/freshness.jsonl` creation | ✅ stable | the freshness ledger is opened by `freshness-session-start.sh` on every spawn; E7 doesn't depend on which hook opened it. |
| Write tool call success | ✅ stable | per-eval HOME has empty CWD; `no_prior_read` `create_allowed` branch permits Write on fresh path; deterministic creation. |
| `freshness.jsonl` `type=pre_edit` row | ✅ stable | OQ-2 contract emits one such row per PreToolUse Write fire. |
| `freshness.jsonl` `matcher=Write` row | ✅ stable | Write branch of the matcher group fires on each Write tool invocation. |
| `written.txt` existence | ✅ stable | created by Write, persists. |
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

## Hook telemetry gap — freshness-pre-edit.sh observables (shared with E6)

`src/superclaude/hooks/scripts/freshness-pre-edit.sh` (revision as of
2026-05-20, lines 108-119) writes to
**`$HOME/.claude/logs/freshness-hook.jsonl`** (note the `-hook` suffix)
with the JSONL envelope:

```json
{"ts":"...","event":"PreToolUse","tool":"Write","path":"...",
 "session_id":"...","tool_call_idx":N,"decision":"...","reason":"..."}
```

The OQ-2 D-0082 §4 body shape — which T05.11 lands verbatim — asserts
against `$HOME/.claude/logs/freshness.jsonl` (no `-hook` suffix) and
uses different field names: `type=pre_edit` (script uses
`event=PreToolUse`) and `matcher=Write` (script uses `tool=Write`).

**Two divergences** between the script's current emit and the OQ-2
contract:

1. **Path**: `logs/freshness-hook.jsonl` vs. `logs/freshness.jsonl`.
2. **Field names**: `event` / `tool` vs. `type` / `matcher`.

The OQ-2 resolution (D-0082 §4) freezes the eval body to assert
against the **hook contract** — not the **current hook implementation**.
The same pattern was applied to E3 / D-0087 §8.1 for the parallel
`session-init.sh` gap, E4 / D-0088 §8.1 for `freshness-session-start.sh`,
E5 / D-0089 §8.1 for `freshness-user-prompt.sh`, and E6 / D-0090 §8.1
for **the same `freshness-pre-edit.sh` script**.

**Crucial observation:** E6 and E7 share the underlying hook script
(both branches of the `Edit|Write|mcp__serena__*` matcher group
dispatch to `freshness-pre-edit.sh`). The single hook-script update
that wires `logs/freshness.jsonl` with `type` / `matcher` field names
unblocks both E6 and E7 simultaneously (and E8 when it lands). The
follow-up hook-script update task is a single deliverable that pairs
all three sibling evals.

### Discovery and mitigation

1. **Grep + Read confirms the gap:**
   ```
   $ grep -n "freshness" src/superclaude/hooks/scripts/freshness-pre-edit.sh
     Lines 108-119: appendln to $HOME/.claude/logs/freshness-hook.jsonl
     Field schema: {ts, event:"PreToolUse", tool:<tool_name>, path,
                    session_id, tool_call_idx, decision, reason}
   ```
   The asserted ledger path is not written by any script in
   `src/superclaude/hooks/` on the normal PreToolUse path at T05.11
   authoring time.

2. **Not in scope for T05.11.** T05.11's acceptance criteria require
   "E7 entry whose body matches the OQ-2 resolution" — they do **not**
   require modifying `freshness-pre-edit.sh`. The hook script update
   is a downstream task (sibling-shape to the pending updates for
   `session-init.sh` / `freshness-session-start.sh` /
   `freshness-user-prompt.sh` — and shared with T05.10's parallel
   identification).

3. **Risk acknowledged in spec §8.1.** Today's `eval run --eval E7`
   would fail every JSONL substring assertion deterministically (the
   file may exist from the SessionStart hook chain, but neither
   `pre_edit` nor `Write` substrings appear because the actual emit
   uses `event=PreToolUse` and `tool=Write` in a different file). This
   is **not introduced** by T05.11; it is a transitive dependency on
   the hook-script update task.

4. **Verification path that works today:**
   - `eval describe --suite real --eval E7` round-trips the manifest
     body — proves it loads and resolves through `Expect.from_mapping`.
   - `eval list --json` enumerates E7 alongside E1..E15 — proves
     schema acceptance and FR-SCH2 id validity.
   - Manual `Expect.from_mapping` invocation over each `expects[]` row
     — proves the declarative DSL accepts the body.
   These three artifacts are the T05.11 acceptance evidence in
   `evidence/T05.11/`.

5. **Follow-up task scope (out of T05.11).** A future task (to be
   added to the phase-5 followups under a new T05.XX id, or grouped
   with the E3 / E4 / E5 / E6 hook-script updates) wires
   `freshness-pre-edit.sh` to:
   - append `{"ts":...,"session_id":...,"turn":...,"type":"pre_edit",
     "matcher":<tool_name>,...}\n` to
     `$HOME/.claude/logs/freshness.jsonl` (no `-hook` suffix) on every
     PreToolUse fire — idempotent per tool invocation.

   Once that follow-up lands AND the runner NameError is fixed, both
   E6's and E7's per-task AC ("`uv run superclaude eval run --suite
   real --eval E{6,7}` exits 0 deterministically across 3 runs")
   become satisfiable without further body changes.

## Schema validation walkthrough

The new body must satisfy `suite.schema.json`:

| Field | Schema rule | This body |
|---|---|---|
| `id` | `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` | `E7` ✅ |
| `title` | string ≥1 char | `"PreToolUse Write matcher fires"` ✅ |
| `category` | string | `"hook-lifecycle"` ✅ |
| `timeout_sec` | integer ≥ 1 | `60` ✅ |
| `isolation.home_strategy` | enum [ephemeral, seeded, shared] | `"ephemeral"` ✅ |
| `inputs` | array of object | 2-element `[{prompt: ...}, {prompt: "/quit"}]` ✅ |
| `expects` | array of object | 5 single-key mappings ✅ |
| `no_pty` | enum [skip] | `"skip"` ✅ |

No `additionalProperties: false` violations; no schema-version bump
required.

## Coverage gate (FR-COV1) impact

E7 issues no MCP tool calls in the assertion surface and carries no
`expect_tool_call` field. The agent's Write tool call is **built-in**
Claude Code tool, not an MCP tool — it does not appear in
`_iter_eval_tool_calls`'s output for any matcher prefix in
`_DEFAULT_MCP_TOOL_PREFIXES` (`coverage.py:99-107`). The matcher-
coverage triad (`mcp__auggie__.*` / `mcp__auggie-mcp__.*` /
`mcp__airis-mcp-gateway__auggie_.*`) remains covered exclusively by
E1 + E2.1-3 — E7 contributes nothing to that gate, which is the
correct outcome (E7 covers a hook-event *surface*, not an MCP-matcher
prefix).

The hook-event coverage axis (D-0082 §3) is the gate E7 advances: it
adds **PreToolUse (matcher=Write)** to the covered set. E6 already
contributed Edit (D-0090); E8 will complete the PreToolUse matcher-group
coverage when it lands.

## Why the comment block in real.yaml is verbose (~70 lines)

Matches the verbosity of the E1 / E2.1-3 / E3 / E4 / E5 / E6 comment
blocks. Reviewers of `real.yaml` should be able to understand each
eval's contract (and the matcher-discrimination two-substring shape,
the telemetry-gap acknowledgment, the per-input count deferral, the
single-input rationale vs E6's three-input shape) without context-
switching to the deliverable artifacts. The verbosity is paid once at
authoring time and amortized across every future review / debug
session.

## Differences from E6 sibling (closest neighbor)

| Aspect | E6 (D-0090) | E7 (D-0091, this) |
|---|---|---|
| Hook covered | PreToolUse matcher=Edit | PreToolUse matcher=**Write** |
| Script | freshness-pre-edit.sh | **freshness-pre-edit.sh (same)** |
| `hooks.json` matcher group | `Edit\|Write\|mcp__serena__*` (Edit branch) | `Edit\|Write\|mcp__serena__*` (**Write** branch) |
| Inputs | `[Write seed, Edit fire, /quit]` (3) | `[Write fire, /quit]` (**2**) |
| Why fewer inputs | n/a | Write creates target directly via `create_allowed` branch; no seed needed |
| Asserted JSONL file | `logs/freshness.jsonl` | `logs/freshness.jsonl` (same) |
| Asserted JSONL `type` substring | `"type":"pre_edit"` | `"type":"pre_edit"` (same — shared event type) |
| Asserted matcher-discrimination substring | `"matcher":"Edit"` | **`"matcher":"Write"`** |
| Asserted file existence (beyond logs) | `edited.txt` | **`written.txt`** |
| OQ-2 §4 deferred predicate | `event_count(type=pre_edit, matcher=Edit) == 1` | `event_count(type=pre_edit, matcher=Write) == 1` |
| Capability tags | — | — (same) |
| `timeout_sec` | 60 | 60 (same) |
| Telemetry gap | ✅ D-0090 §8.1 | ✅ D-0091 §8.1 (**same script, paired follow-up**) |

The shared posture across E6 and E7: same isolation strategy, same
exit-code assertion, same telemetry-gap acknowledgment posture, same
`event_count`-style deferral pattern, same hook script. E7 differs from
E6 only in: (a) the matcher-pin substring value (`Write` vs `Edit`);
(b) the asserted file name (`written.txt` vs `edited.txt`); (c) the
input count (2 vs 3 — no seed needed for Write).

## Three-substring shape unique to PreToolUse matcher-group siblings

E6 / E7 / E8 share the JSONL ledger but assert *different* matcher
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
file-existence assertion is unique to E6/E7 because they have
filesystem side-effects to verify.

## Sibling-comparison table across E3..E7

| Aspect | E3 | E4 | E5 | E6 | E7 (this) |
|---|---|---|---|---|---|
| Hook covered | SessionStart pos-0 | SessionStart pos-1 matcher=* | UserPromptSubmit | PreToolUse Edit | **PreToolUse Write** |
| Script | session-init.sh | freshness-session-start.sh | freshness-user-prompt.sh | freshness-pre-edit.sh | **freshness-pre-edit.sh** |
| Asserted JSONL `type` | `session_init` | `session_start` | `user_prompt` | `pre_edit` | **`pre_edit`** |
| Matcher-discrimination substring | (none) | (none) | (none) | `"matcher":"Edit"` | **`"matcher":"Write"`** |
| Asserted file (beyond logs) | session-init.log | (none) | (none) | edited.txt | **written.txt** |
| Inputs | `[/quit]` | `[/quit]` | `[echo test, /quit]` | `[Write, Edit, /quit]` | **`[Write, /quit]`** |
| Capability tags | — | — | — | — | — |
| `timeout_sec` | 60 | 60 | 60 | 60 | **60** |
| Telemetry gap | ✅ D-0087 §8.1 | ✅ D-0088 §8.1 | ✅ D-0089 §8.1 | ✅ D-0090 §8.1 | **✅ D-0091 §8.1** |
