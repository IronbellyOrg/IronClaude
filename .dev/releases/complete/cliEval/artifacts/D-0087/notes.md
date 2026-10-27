# D-0087 — Design notes

## Why two file assertions instead of one

The minimum-viable "did the SessionStart unmatched hook fire" assertion
could be just **one** of:

- `file.exists(state/session-init.log)` — proves the script ran.
- `file(logs/session-events.jsonl, contains: '"type":"session_init"')`
  — proves the event was emitted.

We assert **both** because they fail under different failure modes:

| Failure mode | `session-init.log` assertion | `session_events.jsonl` assertion |
|---|---|---|
| Hook never invoked (registration missing from `hooks.json`) | ❌ fails | ❌ fails |
| Hook invoked but script crashed before `tee state/session-init.log` | ❌ fails | depends on order |
| Hook invoked but failed before emitting the JSONL event | ✅ passes | ❌ fails |
| Hook invoked, logged, but JSONL writer mis-types the `type` field | ✅ passes | ❌ fails (substring miss) |
| Everything OK | ✅ passes | ✅ passes |

Without the second assertion, a "logs but doesn't emit telemetry"
regression would silently pass — defeating the OQ-2 coverage contract
(D-0082 §3) that *every hook event type is exercised AND its emit
contract is asserted*. The two-assertion shape is consistent with the
matcher-coverage triad (D-0086 §"Two-assertion shape ({event, tool})"),
which also asserts two substrings against the same JSONL file for the
same reason.

## Why a literal substring, not a JSONL field equality

`Expect.jsonl` would let us assert a structural predicate
(e.g. `type == "session_init"`) but only via Python callables
(`expect.py:269-369`). Those have no YAML wire form, so declaring them
in `real.yaml` would either require a `callback:` escape hatch (D-4,
deferred to E14) or a v2 declarative DSL extension.

For the v1 manifest the substring `'"type":"session_init"'` is
uniquely identifying within `logs/session-events.jsonl`:

- The expected JSONL line format (per the OQ-2 contract) is
  `{"ts":...,"session_id":...,"type":"session_init",...}`.
- The `"type":"…"` key only appears in SessionStart event records.
- The substring includes the leading `"type":"` so it cannot collide
  with any `"some_field":"…session_init"` line that might appear in a
  future hook extension.

This mirrors the substring-vs-callable trade-off documented in D-0086
§"Why a literal contains substring, not a JSONL field equality".

## Why `/quit` as the input

E3's only "input" requirement per D-0082 §4 is "spawn a fresh claude
session via PtyDriver.spawn(home=isolated); wait for prompt-ready".
The session must then exit cleanly so the `exit_code.equals(0)`
assertion holds.

`/quit` is the canonical Claude Code exit command. It is:

- **Non-tool-call** — doesn't fire PreToolUse / PostToolUse hooks that
  would muddy the SessionStart-only assertion surface.
- **Synchronous** — Claude Code drains pending hook output and exits
  with code 0 (no race against async SubagentStop hooks etc.).
- **Stable across versions** — the `/quit` slash command has been the
  exit primitive across every Claude Code release in scope.

Alternative inputs considered and rejected:

| Input | Rejected because |
|---|---|
| Empty array `inputs: []` | Driver wouldn't know when to stop; would rely on session-init.sh exiting the session, which it doesn't. |
| `EOF` (Ctrl-D) | Less portable across PTY harness layers; `/quit` is the documented exit channel. |
| Long-running prompt | Adds noise; would trigger PreToolUse hooks; defeats the SessionStart-only assertion focus. |

## Why `timeout_sec: 60` (vs. default 120)

The suite default is `per_eval_timeout_sec: 120`. E3's actual work is
bounded by:

- PTY spawn → SessionStart hooks fire: <1s on every observed host.
- session-init.sh runtime: <0.5s (it shells out to `git status` and
  emits ~10 lines of text).
- `/quit` → clean exit: <1s.

Total expected wall-clock is <3s. 60s is generous (20× expected) but
tighter than the default, so a runner regression that wedges E3
flushes faster. Following the same proportional-timeout pattern used
by E1 / E2.1-3 (`timeout_sec: 90` each — slightly higher because they
make real MCP calls).

## Why no capability tags (E3 runs everywhere)

session-init.sh has zero external dependencies:

- No MCP tool calls (the entire script is `git status` + `echo`).
- No network (the `📊 Git:` banner is git-CLI-only).
- No filesystem dependencies outside `$HOME/.claude/`.

Therefore E3 needs no `requires:` clause; the FR-CAP1 gate is a no-op
for E3 and `--no-mcp` is irrelevant to its execution. This is the
exact rollup recorded in D-0082 §6 (E3 capability tags: `—`, soft-skip
under `--no-mcp`: no).

## Why E3 keeps `no_pty: skip` despite asserting only SessionStart

Every eval in `suites/real.yaml` carries `no_pty: skip` because the
suite is PTY-driven by construction (R-077 / D-0077). E3 is no
exception — its assertion model relies on the PTY harness spawning a
real Claude subprocess so the SessionStart hooks fire naturally. There
is no "logic-only" path through E3 that could survive `--no-pty`
(you'd have to mock the SessionStart event emission, which defeats the
real-world coverage purpose). Keeping the tag is therefore aligned
with the suite-wide DOC-OQ3 contract.

## Determinism analysis

The body passes/fails the same way every run on a clean per-eval HOME
(D-0082 §2 constraint 2 / per-task AC):

| Variable | Stable? | Notes |
|---|---|---|
| PTY spawn outcome | ✅ stable | FR-ISO2 fresh HOME → no carry-over. |
| `session-init.log` creation | ✅ stable | first-position SessionStart hook contract per D-0082 §4. |
| `session_events.jsonl` `type=session_init` line | ✅ stable | OQ-2 contract emits exactly one such line per SessionStart. |
| `ts` timestamp on JSONL line | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| `session_id` field | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| `/quit` exit code | ✅ stable | Claude Code returns 0 on `/quit`. |

Three consecutive runs yield identical EvalOutcome statuses, which is
the per-task AC.

## Hook telemetry gap — session-init.sh observables

`src/superclaude/scripts/session-init.sh` (revision as of 2026-05-20)
**does not** currently write to `$HOME/.claude/state/session-init.log`
or `$HOME/.claude/logs/session-events.jsonl`. It only echoes the
SessionStart banner to stdout (lines 9, 12, 19, 22-28 of the script).

The OQ-2 resolution (D-0082 §4 row E3) freezes the eval body to assert
both observables anyway, on the basis that the **hook contract** —
not the **current hook implementation** — is what the eval body is
authored against. The same pattern was applied to E14 / E15
(callback-based / timeout-based assertions for future runner behavior;
see D-0082 §4 rows E14 / E15).

### Discovery and mitigation

1. **Grep confirms the gap:**
   ```
   $ grep -rn "session-init\.log\|session-events\.jsonl\|session_init" src/
   (no matches)
   ```
   Neither the asserted log path nor the JSONL event ledger exists
   anywhere in the source tree at T05.07 authoring time.

2. **Not in scope for T05.07.** T05.07's acceptance criteria require
   "E3 entry whose body matches the OQ-2 resolution" — they do **not**
   require modifying session-init.sh. The hook script update is a
   downstream task (sibling-shape to the runner NameError fix that
   blocks E2.1-3 from running end-to-end today, per D-0086 §"Pre-
   existing runner bug").

3. **Risk acknowledged in spec §8.1.** Today's `eval run --eval E3`
   would fail the first two assertions deterministically (asserting
   files that the hook doesn't yet create). This is **not introduced**
   by T05.07; it is a transitive dependency on the hook-script update
   task.

4. **Verification path that works today:**
   - `eval describe --suite real --eval E3` round-trips the manifest
     body — proves it loads and resolves through `Expect.from_mapping`.
   - `eval list --json` enumerates E3 alongside E1 / E2.1-3 — proves
     schema acceptance and FR-SCH2 id validity.
   - Manual `Expect.from_mapping` invocation over each `expects[]` row
     — proves the declarative DSL accepts the body.
   These three artifacts are the T05.07 acceptance evidence in
   `evidence/T05.07/`.

5. **Follow-up task scope (out of T05.07).** A future task (to be
   added to the phase-5 followups under a new T05.XX id, or grouped
   with the E4 / E5 / E9 / E10 / E11 hook-script updates) wires
   session-init.sh to:
   - `tee $HOME/.claude/state/session-init.log` on stdout output, and
   - `printf '{"ts":...,"session_id":...,"type":"session_init"}\n' >> $HOME/.claude/logs/session-events.jsonl`
     before the script exits.

   Once that follow-up lands AND the runner NameError is fixed, E3's
   per-task AC ("`uv run superclaude eval run --suite real --eval E3`
   exits 0 deterministically across 3 runs") becomes satisfiable
   without further body changes.

## Schema validation walkthrough

The new body must satisfy `suite.schema.json`:

| Field | Schema rule | This body |
|---|---|---|
| `id` | `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` | `E3` ✅ |
| `title` | string ≥1 char | `"SessionStart unmatched (session-init) hook fires"` ✅ |
| `category` | string | `"hook-lifecycle"` ✅ |
| `timeout_sec` | integer ≥ 1 | `60` ✅ |
| `isolation.home_strategy` | enum [ephemeral, seeded, shared] | `"ephemeral"` ✅ |
| `inputs` | array of object | `[{prompt: "/quit"}]` ✅ |
| `expects` | array of object | 3 single-key mappings ✅ |
| `no_pty` | enum [skip] | `"skip"` ✅ |

No `additionalProperties: false` violations; no schema-version bump
required.

## Coverage gate (FR-COV1) impact

E3 issues no MCP tool calls and carries no `expect_tool_call` field.
It therefore does **not** appear in `_iter_eval_tool_calls`'s output
for any matcher prefix in `_DEFAULT_MCP_TOOL_PREFIXES`
(`coverage.py:99-107`). The matcher-coverage triad
(`mcp__auggie__.*` / `mcp__auggie-mcp__.*` / `mcp__airis-mcp-gateway__auggie_.*`)
remains covered exclusively by E1 / E2.1-3 — E3 contributes nothing
to that gate, which is the correct outcome (E3 covers a hook-event
*type*, not a matcher prefix).

The hook-event coverage gate (separately enumerated in D-0082 §3) is
the gate E3 advances: it adds first-position `SessionStart` to the
covered set, completing the SessionStart row when paired with E4.

## Why the comment block in real.yaml is verbose

The leading comment block on the E3 entry (~35 lines) mirrors the
verbosity of the E1 / E2.1-3 comment blocks. Reviewers of `real.yaml`
should be able to understand each eval's contract without context-
switching to the deliverable artifacts. The verbosity is paid once at
authoring time and amortized across every future review / debug
session.
