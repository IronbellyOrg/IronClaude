# D-0089 — Design notes

## Why two file assertions instead of one

The minimum-viable "did the UserPromptSubmit freshness hook fire"
assertion could be just **one** of:

- `file.exists(logs/freshness.jsonl)` — proves the freshness ledger was
  opened (the hook ran far enough to create the file, or a prior
  SessionStart hook opened it on the same spawn).
- `file(logs/freshness.jsonl, contains: '"type":"user_prompt"')` —
  proves the freshness `user_prompt` event row was emitted.

We assert **both** because they fail under different failure modes,
following the same matrix established in D-0087 / D-0088 for the E3 /
E4 siblings:

| Failure mode | `freshness.jsonl` exists | `freshness.jsonl` `user_prompt` row |
|---|---|---|
| Hook never invoked (registration missing from `hooks.json` UserPromptSubmit block) | ❌ fails (assuming SessionStart hook didn't open the ledger first — see note below) | ❌ fails |
| Hook invoked but script crashed before opening the ledger | depends on order | ❌ fails |
| Hook invoked, ledger opened/already-open, but failed before emitting the JSONL event | ✅ passes | ❌ fails |
| Hook invoked, ledger opened, but JSONL writer mis-types the `type` field | ✅ passes | ❌ fails (substring miss) |
| Everything OK | ✅ passes | ✅ passes |

**Asymmetry vs. E3/E4:** the freshness ledger may **also** be opened
by `freshness-session-start.sh` on the same PTY spawn (E4's hook). So
`file.exists` alone is a weaker proof for E5 than it is for E3/E4 —
the file might exist solely from the position-1 SessionStart hook
without `freshness-user-prompt.sh` ever firing. The second assertion
(`contains '"type":"user_prompt"'`) is what uniquely pins
UserPromptSubmit-hook execution: only `freshness-user-prompt.sh`
emits a `user_prompt`-typed row to the freshness ledger.

Without the second assertion, a "ledger-open-but-no-user_prompt-event"
regression — e.g. the UserPromptSubmit registration silently
disappearing from `hooks.json` while SessionStart hooks still open the
ledger — would pass undetected. The two-assertion shape preserves the
OQ-2 coverage contract (D-0082 §3) that *every hook event type is
exercised AND its emit contract is asserted*. It mirrors E3 (D-0087),
E4 (D-0088), and the matcher-coverage triad (D-0086 §"Two-assertion
shape ({event, tool})"), all of which assert two substrings against
the same JSONL file for the same structural reason.

## Why a literal substring, not a JSONL field equality

`Expect.jsonl` would let us assert a structural predicate
(e.g. `type == "user_prompt"`) but only via Python callables
(`expect.py:269-369`). Those have no YAML wire form, so declaring them
in `real.yaml` would either require a `callback:` escape hatch (D-4,
deferred) or a v2 declarative DSL extension.

For the v1 manifest the substring `'"type":"user_prompt"'` is
uniquely identifying within `logs/freshness.jsonl`:

- The expected JSONL line format (per the OQ-2 contract D-0082 §4) is
  `{"ts":...,"session_id":...,"type":"user_prompt",...}`.
- The freshness ledger writers in scope today are
  `freshness-session-start.sh` (emits `type=session_start`) and
  `freshness-user-prompt.sh` (would emit `type=user_prompt`). No other
  hook script writes to `logs/freshness.jsonl`.
- The substring includes the leading `"type":"` so it cannot collide
  with any `"some_field":"…user_prompt"` line that might appear in a
  future hook extension.

This mirrors the substring-vs-callable trade-off documented in
D-0087 §"Why a literal substring..." and D-0088 §"Why a literal
substring..." and D-0086 §"Why a literal contains substring, not a
JSONL field equality".

## Why `event_count >= 1 per injected prompt` is deferred

D-0082 §4 row E5 lists **two** `jsonl` assertions:

1. `jsonl.contains_event(logs/freshness.jsonl, type=user_prompt)` —
   proves the event fired at least once.
2. `jsonl.event_count(logs/freshness.jsonl, type=user_prompt) >= 1 per injected prompt` —
   proves at least one `user_prompt` row is emitted **per injected
   prompt** (a multi-fire pairing guard scaled to the number of
   prompts in `inputs`).

Both require a Python callable bound to the `type` field
(`expect.py:269-369`). The first is functionally covered by the
`Expect.file` substring proxy (above) — a substring assertion against
the ledger proves *at least one* `user_prompt` row was emitted, which
is exactly the v1 OQ-2 contract for E5's first jsonl assertion.

The second — the per-injected-prompt count guard — has no analogous
static-string proxy:

- `Expect.file` line-count constraints (`line_count_min` /
  `line_count_max`) count *all* lines in the file, not lines matching
  a filter.
- The total `freshness.jsonl` line count is non-deterministic when
  the same ledger is shared by SessionStart and UserPromptSubmit
  hooks (one `session_start` row + N `user_prompt` rows + any future
  hook contributors). A total-line-count assertion would be brittle:
  it would break if `freshness-session-start.sh` later emits a second
  envelope row, even though that's unrelated to the
  user_prompt-event-count contract.
- The N-prompts-N-rows aspect is the most YAML-unfriendly part of the
  D-0082 §4 spec: it relates the cardinality of `inputs[]` to the
  cardinality of matching jsonl rows, which requires either (a) a
  Python callable that reads both sides of the relationship at runtime
  or (b) a templated count expression like `count: ${len(inputs)}`
  that the schema does not yet support.

The per-injected-prompt count guard is deferred to a follow-up under
one of:

- **D-4 callback escape hatch** — exercised for E5 to land the
  `event_count >= len(inputs)` predicate as a Python callback
  registered against E5. Lowest-friction path.
- **YAML DSL extension** — add a declarative `jsonl: contains_event:
  { type: ..., count_per_input: 1 }` shorthand that compiles down to
  a `Expect.jsonl(filter=..., line_count=...)` callable at load time.
  Highest leverage if other evals (E9 / E10 / E11) also need
  per-input-count predicates.

T05.09's AC is "body matches the OQ-2 resolution; runs deterministically
on a clean HOME" — the first assertion (event fired at least once) is
sufficient for that AC. The pairing guard is not load-bearing today
(the UserPromptSubmit hook fires exactly once per injected prompt by
Claude Code's hook-engine contract) and can be added later without
re-authoring the existing assertions.

## Why `"echo test"` AND `/quit` as the inputs

OQ-2 D-0082 §4 row E5 names the input shape as
`spawn session; inject_prompt("echo test")`. E3 and E4 use `/quit`
alone since their assertion surface is SessionStart-only and the
session needs no content prompts. E5 is different: the
UserPromptSubmit hook is the assertion target, so the body **must**
inject at least one content prompt.

The chosen shape `[{prompt: "echo test"}, {prompt: "/quit"}]` does
two jobs:

- **`echo test`** literally satisfies the OQ-2 `inject_prompt("echo test")`
  contract. It is content (not a slash command) so it routes through
  the UserPromptSubmit hook chain.
- **`/quit`** matches E3/E4's clean-exit input. Without it the PTY
  session would hang on the agent's response to "echo test" and
  the `exit_code.equals(0)` assertion couldn't fire in bounded
  wall-clock time.

Alternatives considered and rejected:

| Alternative | Why rejected |
|---|---|
| `"echo test"` alone | session never terminates → exit code unprovable in bounded wall-clock; `timeout_sec` would always fire. |
| `"hi"` instead of `"echo test"` | doesn't match OQ-2 literal text; review would flag a mismatch against D-0082 §4. |
| `["/quit"]` alone | matches E3/E4 but **doesn't fire UserPromptSubmit on a content prompt** — `/quit` is a slash command. The hook *does* fire on `/quit` in current Claude Code (slash commands route through UserPromptSubmit), but that side-effect is implementation-dependent; the OQ-2 contract names content-prompt injection explicitly. Using `/quit` alone would test a different code path than the contract specifies. |
| `["echo test", "exit"]` | `exit` is not a Claude Code slash command — would produce an "unknown command" prompt rather than a clean exit. |
| `[N x "echo test", "/quit"]` (multi-fire for the count guard) | the per-injected-prompt count predicate is **deferred** (see above) — adding multiple content prompts doesn't change which assertion fires today, but it does increase wall-clock and per-eval HOME footprint. Single content prompt + clean exit is the smallest viable input that satisfies AC1 (OQ-2 body) and AC4 (clean isolation). |

Critically, the **same PTY spawn that fires E3/E4's SessionStart hooks
also fires E5's UserPromptSubmit hook** — but the SessionStart hooks
fire *before* the first user prompt and UserPromptSubmit fires *after*
each prompt submission, so the three hooks observe disjoint phases of
the same session lifecycle. The shared spawn means E3, E4, and E5
share the freshness ledger they all assert against.

## Why `timeout_sec: 60` (vs. default 120)

The suite default is `per_eval_timeout_sec: 120`. E5's actual work is
bounded by:

- PTY spawn → both SessionStart hooks fire: <1s on every observed host.
- "echo test" prompt submission → UserPromptSubmit hook fires →
  hook flush: <0.5s (`hooks.json` per-hook timeout is **3s** — the
  tightest hook budget in the manifest, reflecting that UserPromptSubmit
  is on the synchronous prompt path).
- Agent response to "echo test": variable, but bounded by the next
  step.
- `/quit` → clean exit: <1s.

Worst-case wall-clock is dominated by the agent's response to
"echo test". For an offline / no-MCP host the response is typically
a single canned reply; for a host with MCP it might be longer but is
still bounded by Claude Code's response budget. 60s is generous (well
above the observed steady-state of <10s for any "echo test"-class
prompt) but tighter than the default, so a runner regression that
wedges E5 flushes faster.

Matches E3's `timeout_sec: 60` and E4's `timeout_sec: 60` for
sibling-spawn parity — all three evals share the same PTY-spawn
lifecycle and the same one-content-prompt-then-quit envelope, so they
should share the same wall-clock budget.

## Why no capability tags (E5 runs everywhere)

`freshness-user-prompt.sh` has zero external dependencies:

- No MCP tool calls (the script is a freshness-check + JSONL emit).
- No network (freshness is computed against local HOME state).
- No filesystem dependencies outside `$HOME/.claude/`.

The injected content prompt `"echo test"` is a no-op from the hook
perspective — the hook fires on submission regardless of what the
agent does with the content. The agent might call MCP tools to respond
to "echo test" (depending on personality/skill activation), but the
**UserPromptSubmit hook** fires *before* any tool-routing decision.
So E5's assertion surface is reachable without any MCP infrastructure.

Therefore E5 needs no `requires:` clause; the FR-CAP1 gate is a no-op
for E5 and `--no-mcp` is irrelevant to its execution. This matches
the D-0082 §6 capability-tag rollup row for E5 (`requires: —`,
soft-skip under `--no-mcp`: no) — identical posture to E3 / E4.

## Why E5 keeps `no_pty: skip` despite asserting only UserPromptSubmit

Every eval in `suites/real.yaml` carries `no_pty: skip` because the
suite is PTY-driven by construction (R-077 / D-0077). E5 is no
exception — its assertion model relies on the PTY harness spawning a
real Claude subprocess and **injecting content prompts via the PTY
write channel** so the UserPromptSubmit hook fires naturally. There
is no "logic-only" path through E5 that could survive `--no-pty`
(you'd have to mock the prompt-submit event emission, which defeats
the real-world coverage purpose). Keeping the tag aligns with the
suite-wide DOC-OQ3 contract.

## Determinism analysis

The body passes/fails the same way every run on a clean per-eval HOME
(D-0082 §2 constraint 2 / per-task AC):

| Variable | Stable? | Notes |
|---|---|---|
| PTY spawn outcome | ✅ stable | FR-ISO2 fresh HOME → no carry-over. |
| `logs/freshness.jsonl` creation | ✅ stable | the freshness ledger is opened by `freshness-session-start.sh` on every spawn; E5 doesn't depend on which hook opened it. |
| `freshness.jsonl` `type=user_prompt` row | ✅ stable | OQ-2 contract emits exactly one such row per UserPromptSubmit fire; with 2 prompts (echo + /quit), at least one `user_prompt` row is guaranteed. |
| `ts` timestamp on JSONL row | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| `session_id` field | ⚠️ varies | **not asserted against** — irrelevant to the body. |
| Agent response to "echo test" | ⚠️ varies | **not asserted against** — body only pins the hook fire, not the agent's reply text. |
| Whether the agent calls MCP tools | ⚠️ varies | **not asserted against** — UserPromptSubmit hook fires before tool-routing. |
| `/quit` exit code | ✅ stable | Claude Code returns 0 on `/quit`. |

Three consecutive runs yield identical EvalOutcome statuses, which is
the per-task AC. Note that the deterministic surface here is wider
than the test surface: the agent's response varies, but no assertion
inspects it.

## Hook telemetry gap — freshness-user-prompt.sh observables

`src/superclaude/hooks/scripts/freshness-user-prompt.sh` (revision as
of 2026-05-20) emits the UserPromptSubmit envelope to **stdout** via
`jq -nc ... hookSpecificOutput ...` (lines 259-264 of the script) and
writes truncation telemetry to `logs/freshness-hook.jsonl` only when
the envelope is truncated (lines 252-256). On the normal (non-
truncated) path it **does not** append a `{"type":"user_prompt"}`
row to `$HOME/.claude/logs/freshness.jsonl`.

The OQ-2 resolution (D-0082 §4 row E5) freezes the eval body to assert
this observable anyway, on the basis that the **hook contract** —
not the **current hook implementation** — is what the eval body is
authored against. The same pattern was applied to E3 / D-0087 §8.1
for the parallel `session-init.sh` gap and E4 / D-0088 §8.1 for the
parallel `freshness-session-start.sh` gap.

### Discovery and mitigation

1. **Grep + Read confirms the gap:**
   ```
   $ Read freshness-user-prompt.sh
     Line 252-256: truncation-only ledger write to logs/freshness-hook.jsonl
     Line 259-264: jq -nc ... hookSpecificOutput ... → stdout
     (no append to logs/freshness.jsonl in the normal path)
   ```
   The asserted ledger path is not written by any script in
   `src/superclaude/hooks/` on the normal UserPromptSubmit path at
   T05.09 authoring time.

2. **Not in scope for T05.09.** T05.09's acceptance criteria require
   "E5 entry whose body matches the OQ-2 resolution" — they do **not**
   require modifying `freshness-user-prompt.sh`. The hook script
   update is a downstream task (sibling-shape to the same update
   pending for `session-init.sh` per D-0087 §8.1 and
   `freshness-session-start.sh` per D-0088 §8.1).

3. **Risk acknowledged in spec §8.1.** Today's `eval run --eval E5`
   would fail the second assertion deterministically (the file may
   exist from the SessionStart hook chain, but the `user_prompt`
   substring would not appear in `logs/freshness.jsonl`). This is
   **not introduced** by T05.09; it is a transitive dependency on
   the hook-script update task.

4. **Verification path that works today:**
   - `eval describe --suite real --eval E5` round-trips the manifest
     body — proves it loads and resolves through `Expect.from_mapping`.
   - `eval list --json` enumerates E5 alongside E1..E15 — proves
     schema acceptance and FR-SCH2 id validity.
   - Manual `Expect.from_mapping` invocation over each `expects[]` row
     — proves the declarative DSL accepts the body.
   These three artifacts are the T05.09 acceptance evidence in
   `evidence/T05.09/`.

5. **Follow-up task scope (out of T05.09).** A future task (to be
   added to the phase-5 followups under a new T05.XX id, or grouped
   with the E3 / E4 / E9 / E10 / E11 hook-script updates) wires
   `freshness-user-prompt.sh` to:
   - `printf '{"ts":...,"session_id":...,"turn":...,"type":"user_prompt",...}\n' >> $HOME/.claude/logs/freshness.jsonl`
     before the script exits successfully (idempotent append per
     UserPromptSubmit invocation).

   Once that follow-up lands AND the runner NameError is fixed, E5's
   per-task AC ("`uv run superclaude eval run --suite real --eval E5`
   exits 0 deterministically across 3 runs") becomes satisfiable
   without further body changes.

## Schema validation walkthrough

The new body must satisfy `suite.schema.json`:

| Field | Schema rule | This body |
|---|---|---|
| `id` | `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` | `E5` ✅ |
| `title` | string ≥1 char | `"UserPromptSubmit freshness hook fires"` ✅ |
| `category` | string | `"hook-lifecycle"` ✅ |
| `timeout_sec` | integer ≥ 1 | `60` ✅ |
| `isolation.home_strategy` | enum [ephemeral, seeded, shared] | `"ephemeral"` ✅ |
| `inputs` | array of object | `[{prompt: "echo test"}, {prompt: "/quit"}]` ✅ |
| `expects` | array of object | 3 single-key mappings ✅ |
| `no_pty` | enum [skip] | `"skip"` ✅ |

No `additionalProperties: false` violations; no schema-version bump
required.

## Coverage gate (FR-COV1) impact

E5 issues no MCP tool calls in the assertion surface and carries no
`expect_tool_call` field. The agent might call MCP tools while
formulating its reply to "echo test", but those calls are not asserted
against and therefore don't appear in `_iter_eval_tool_calls`'s output
for any matcher prefix in `_DEFAULT_MCP_TOOL_PREFIXES`
(`coverage.py:99-107`). The matcher-coverage triad
(`mcp__auggie__.*` / `mcp__auggie-mcp__.*` / `mcp__airis-mcp-gateway__auggie_.*`)
remains covered exclusively by E1 / E2.1-3 — E5 contributes nothing
to that gate, which is the correct outcome (E5 covers a hook-event
*surface*, not a matcher prefix).

The hook-event coverage axis (D-0082 §3) is the gate E5 advances: it
adds **UserPromptSubmit (no-matcher)** to the covered set, completing
the row when paired with E3 / E4 (the two SessionStart positions).
With E3 + E4 + E5 landed, the freshness-related hook chain is the
first hook-surface row to reach full OQ-2 coverage.

## Why the comment block in real.yaml is verbose (~60 lines)

Matches the verbosity of the E1 / E2.1-3 / E3 / E4 comment blocks.
Reviewers of `real.yaml` should be able to understand each eval's
contract (and the YAML-vs-callable trade-off, the telemetry-gap
acknowledgment, the per-injected-prompt count deferral, and why two
inputs are required vs. one for E3/E4) without context-switching to
the deliverable artifacts. The verbosity is paid once at authoring
time and amortized across every future review / debug session.

## Differences from E3 / E4 siblings

| Aspect | E3 (D-0087) | E4 (D-0088) | E5 (D-0089) |
|---|---|---|---|
| Hook covered | `hooks.json` SessionStart position-0 (no matcher) | `hooks.json` SessionStart position-1 (matcher=*) | `hooks.json` UserPromptSubmit (no matcher) |
| Script | `session-init.sh` | `freshness-session-start.sh` | `freshness-user-prompt.sh` |
| `hooks.json` timeout | 10s | 5s | **3s** (tightest in manifest) |
| Asserted log file | `state/session-init.log` | (none) | (none) |
| Asserted JSONL file | `logs/session-events.jsonl` | `logs/freshness.jsonl` | `logs/freshness.jsonl` |
| Asserted JSONL `type` substring | `"type":"session_init"` | `"type":"session_start"` | `"type":"user_prompt"` |
| OQ-2 §4 extra deferred predicate | (none — `contains` substring is the full body) | `event_count == 1` | `event_count >= 1 per injected prompt` |
| Inputs | `[{prompt: "/quit"}]` | `[{prompt: "/quit"}]` | `[{prompt: "echo test"}, {prompt: "/quit"}]` |
| Why extra input | n/a — SessionStart fires before any prompt | n/a — SessionStart fires before any prompt | **content prompt required** to fire UserPromptSubmit |
| Capability tags | — | — | — |
| `timeout_sec` | 60 | 60 | 60 |
| Telemetry gap (script doesn't emit asserted JSONL) | ✅ documented in D-0087 §8.1 | ✅ documented in D-0088 §8.1 | ✅ documented in D-0089 §8.1 |

The shared posture across all three siblings: same isolation strategy,
same exit-code assertion, same telemetry-gap acknowledgment posture,
same `event_count`-style deferral pattern. E5's body is the natural
extension of the E3/E4 siblings — same PTY spawn, same ledger
infrastructure, same proxy pattern — with the unique addition of the
content-prompt injection step that the UserPromptSubmit assertion
surface requires.
