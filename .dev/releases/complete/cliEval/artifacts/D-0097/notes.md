# D-0097 — Notes / Design Rationale

## Why E13's surface is the harness, not a hook

E3-E11 each pin one row of `src/superclaude/hooks/hooks.json` — the
eval drives Claude Code through the PTY, fires the matched hook, and
reads the freshness ledger to prove the hook script emitted its
event. E12 pins the **deployer** (`hook_adapter.deploy_hooks_to`)
via post-setup settings.json shape. E13 is structurally distinct
from all of them: its surface is the **harness's hook-execution
error-handling path** — the code that wraps every hook invocation,
captures stderr / exit code, and decides what to do when the hook
returns non-zero.

The body is hook-event-agnostic by design. A failing PostToolUse
Read hook happens to be the concrete fixture (per OQ-2 D-0082 §4
row E13), but the assertion shape would apply equally to a failing
PreToolUse Edit hook or a failing SessionStart hook. The harness
must fail-open uniformly regardless of which hook event fired.

The regression class motivating E13 (per design-spec §11 / OQ-2
D-0082 §4 notes) is: a hook script's stderr message surfaces to the
agent **as if the matched tool had failed**. The agent sees the
hook's error text instead of the tool's result. This is a
correctness/UX bug in the harness's error-propagation path — the
hook layer is supposed to be invisible to the agent's tool-call
contract.

The natural body shape for this surface is: register a known-failing
hook, fire the matched tool, and assert all three observable
guarantees of the fail-open contract:

1. The tool call completes (process exits cleanly).
2. The failing hook's stderr is captured to the eval transcript
   (a human reader can see what went wrong, even though the agent
   does not).
3. A structured `{type:"hook_error", disposition:"fail_open"}` row
   is appended to `logs/hook-errors.jsonl` (auditable post-run).

That's the OQ-2 contract verbatim. The body assertions pin all three
guarantees with the best-effort declarative proxies.

## Why two `Expect.file(contains=…)` substring proxies for `{type, disposition}`

The OQ-2 D-0082 §4 row E13 expects entry names a conjunctive
predicate over a single JSONL row:

```
jsonl.contains_event(logs/hook-errors.jsonl, type=hook_error,
                     disposition=fail_open)
```

`Expect.jsonl` (`expect.py:269-369`) supports `contains_event` via
Python callable filters — kwargs like `type="hook_error"` and
`disposition="fail_open"` become filter predicates applied row-by-row
to the JSONL ledger. The DSL signature requires Python callables /
keyword-argument dicts, neither of which is expressible under the
declarative YAML manifest schema (`suites/suite.schema.json` has no
`jsonl.contains_event:` primitive entry, only `jsonl:` with a
`path` + `min_count` shape — see expect.py docstring for the kwarg-
based call signature).

Per the established T05.07..T05.17 deferral posture, T05.19 lands
the OQ-2 body shape with the best-effort declarative proxy:

- **Conjunctive `{type, disposition}` proxy:** two independent
  `Expect.file(contains=…)` substring assertions on the SAME ledger
  file — one for `"type":"hook_error"`, one for
  `"disposition":"fail_open"`. The conjunction is implicit: BOTH
  must be present for the eval to pass.

The proxy is **necessary but not sufficient** for the strict
semantic: it does not prove the two substrings appeared on the SAME
JSONL row. A hypothetical pathological emit pattern that wrote
`{type:hook_error, disposition:fail_closed}` on one row and
`{type:other_thing, disposition:fail_open}` on a second row would
satisfy the proxies but violate the strict semantic. In practice
the harness's error-logging path emits all four fields on a single
row by design (per design-spec §11), so the proxy converges with
the strict semantic; an emit-pattern regression that split them
across rows would itself be a bug worth surfacing as a separate
ERROR.

This proxy posture mirrors the two-substring `{type, matcher}`
pattern used by E6 / E7 / E8 (PreToolUse matcher coverage):
matching primitives (`Expect.file` with JSONL substring), matching
mechanism (substring presence on the ledger file), matching
deferral footprint (declarative DSL expressibility limitation). The
conjunctive `{type, matcher}` shape converges with the strict
semantic for the same reason described above (the harness emits all
matcher-pin fields on a single row by design).

## Why a seed `Write` before the `Read`

`Read` requires a target file. The seed Write creates `fixture.txt`
under the per-eval HOME's cwd, then the subsequent Read targets it.
This mirrors E9's two-step (Write fixture, Read fixture) pattern.

The seed Write also fires the PreToolUse Write matcher hook
independently (covered by E7) — that co-fire is harmless because
E13's assertions pin error-path events keyed by `"type":"hook_error"`
on `logs/hook-errors.jsonl`, not pre_edit telemetry on
`logs/freshness.jsonl`. Co-firing of the production
`pre_edit_freshness.sh` does NOT emit anything to
`logs/hook-errors.jsonl` (it exits cleanly).

The PostToolUse Read hook is the one that's replaced by the failing
fixture in the test-only hooks.json variant. The Read input
(`inputs[1]`) is the surface this eval asserts. The Write input
(`inputs[0]`) is pure scaffolding.

## Why `expect_tool_call: Read` on the second input

The OQ-2 input shape names "inject prompt triggering a Read". The
declarative `inputs[].expect_tool_call: Read` field (recognized by
the PTY input dispatch per `commands.py` input loop) pins the
matched tool to `Read`, ensuring the PTY harness waits for the
specific tool call to fire before treating the input as resolved
(rather than accepting any in-session output as completion). This
mirrors E8's `expect_tool_call: mcp__serena__replace_content` and
E9's `expect_tool_call: Read` patterns.

The seed Write input (`inputs[0]`) intentionally omits
`expect_tool_call`. A reasonable agent might satisfy "create
fixture.txt with the line 'content'" via `Write` OR via `Bash
echo`. Pinning a specific tool would make the seed brittle. The
matching tool-call assertion is on the *second* input — the one
whose hook is the surface under test.

## Why `inputs: [Write, Read, /quit]` (not a single `/quit`)

E12 uses `inputs: [{prompt: "/quit"}]` because its assertions are on
post-setup state (no in-session tool calls required to materialize
the asserted shape). E13 is opposite: the assertions are on
**post-hook-execution** state (`logs/hook-errors.jsonl` exists
because a hook fired and failed during a tool call). The eval MUST
actually fire the failing hook in-session, which requires firing the
PostToolUse Read matcher, which requires actually invoking Read,
which requires a target file. Hence: Write seed → Read trigger →
/quit teardown.

The `/quit` is the same clean-shutdown trigger used by E3-E12 — it
lets the PTY harness reach EOF and the runner emit the eval-process
exit code without timing out.

## Why `category: hook-lifecycle` (not `harness` or `error-handling`)

The stale E13 placeholder carried `category: doctor` (a leftover
from the pre-OQ-2 numbering when E13 was "doctor surfaces stale
settings.json schema"). The OQ-2 resolution reassigned E13 to the
hook stderr error-path, which prompts a category re-think:

- `harness` or `error-handling` would be technically accurate (the
  surface IS the harness's error-handling path), but no other eval
  in the suite uses these categories and creating singleton
  categories creates noise in `eval list` filtering.
- `doctor` is wrong — E13 doesn't exercise any doctor surface.
- `hook-lifecycle` is the sibling category for E3-E12. E13 covers
  the error-path half of the hook lifecycle (what happens when a
  hook returns non-zero); E3-E11 cover the happy-path firing half
  (how hooks emit events on clean exit); E12 covers the deployer
  half (how hooks get on disk). The category groups all three under
  one heading for filtering and reporting purposes.

T05.19 picks `hook-lifecycle` for sibling parity, matching the
T05.17 / E12 precedent.

## Why `requires: []` (not `[mcp_server.*]`)

The failing fixture (`tests/fixtures/hooks/failing-post-read.sh`) is
a pure shell script. It does no network I/O, calls no MCP servers,
and depends on no external binaries beyond `printf` + `exit`. The
harness's hook-execution wrapper is also pure Python stdlib (no MCP
dependency). Per D-0082 §6 capability-tag rollup, E13's row lists
no capability tag.

The practical implication: E13 runs under `--no-mcp` (the
matcher-coverage gate counts it as a non-MCP eval), and the only way
E13 skips is via `--no-pty` (per-eval `no_pty: skip` tag). Matches
siblings E3-E7 / E9-E12.

## What this body does NOT assert (and why)

The OQ-2 body row E13 frames three explicit observable contracts +
two implicit derived contracts:

1. **Tool call completes** (exit_code == 0) — landed verbatim via
   `Expect.exit_code(equals=0)`.
2. **Hook stderr captured to transcript** — landed verbatim via
   `Expect.stderr(contains="failing-post-read.sh")`.
3. **Structured `{type:hook_error, disposition:fail_open}` row
   emitted** — landed via the two-substring proxy (see "Why two
   `Expect.file(contains=…)`" above) + a presence check for the
   ledger file itself.
4. **(Implicit) Same-row conjunction** — deferred (no
   `jsonl.contains_event` declarative primitive).
5. **(Implicit) Event count == 1** (the failing hook fires once per
   matched Read; the eval triggers exactly one Read; the ledger
   contains exactly one error row) — NOT asserted. The OQ-2 shape
   names `contains_event` (at-least-once), not `event_count == 1`,
   so the substring presence proxy is complete coverage of the
   at-least-once aspect. If a future regression caused the harness
   to emit the row N>1 times (e.g., a retry loop that doesn't
   short-circuit on fail-open), E13 would still pass — the
   regression would surface elsewhere (e.g., performance regression
   on hook latency).

The same-row conjunction (contract 4) is the weakest gap. The
follow-up path is the same as T05.17 / E12: a YAML callback escape
hatch (D-4) OR a future declarative `jsonl.contains_event:`
primitive backed by a Python implementation that can express
conjunctive predicates over JSONL rows.

The defer-to-follow-up posture is consistent with T05.07..T05.17
(which defer event_count predicates / per-prompt count
discrimination / digest-unchanged primitives for similar reasons).
The deferred branches are documented in §8.1 of the spec; the proxy
assertions in the landed body are necessary-but-not-sufficient
coverage of the OQ-2 contract.

## Scaffolding-gap inheritance (NEW dimension vs. T05.17)

T05.17 (E12) inherited zero scaffolding gaps — the install_hooks
adapter exists, the setup wrapper invokes it, and the
post-first-deploy shape is materialized today on every eval run.
T05.19 (E13) inherits **three scaffolding gaps** that, until closed,
will cause `eval run --eval E13` to ERROR rather than PASS:

1. **The fixture script does not exist.**
   `tests/fixtures/hooks/failing-post-read.sh` is not in the repo
   (the `tests/fixtures/hooks/` directory itself does not exist).
   Until it lands, no failing hook can be registered. A follow-up
   task is responsible for landing the script as a deterministic-
   exit shell script (e.g., `printf "simulated hook failure\n" >&2;
   exit 17`).
2. **No hooks.json-variant deployment path exists.** The per-eval
   setup wrapper (NFR-ISO2 / T02.13) deploys the production
   `src/superclaude/hooks/hooks.json` verbatim via
   `hook_adapter.deploy_hooks_to(home_path)`. There is no
   `isolation.hooks_variant:` schema field and no `inputs[].setup:`
   callback that could swap in a test-only hooks.json. Two options
   for closing this gap (documented in spec §3 / §8.1):
   (a) the YAML `callback:` escape hatch (D-4), or (b) a new
   `isolation.hooks_variant: <path>` schema field with setup-wrapper
   support.
3. **The harness's structured hook-error ledger is not wired.** The
   harness currently propagates hook stderr opaquely (commands.py
   hook-exec path captures it but does not emit a structured
   `{type:"hook_error", disposition:"fail_open"}` row to
   `<home>/.claude/logs/hook-errors.jsonl`). A follow-up task is
   responsible for wiring the structured-error-ledger emission on
   the non-zero-exit hook path.

The acceptance criteria for T05.19 are met by the describe / list /
round-trip evidence (the manifest body is FR-SCH2-valid, OQ-2-shaped,
and resolves through `Expect.from_mapping`); the AC requiring full
end-to-end `eval run --eval E13` execution depends transitively on
(i) the runner NameError fix at `commands.py:1418`, (ii) the failing
fixture script existing, (iii) the hooks.json-variant deployment
path landing, and (iv) the harness's structured hook-error ledger
being wired. Items (ii)-(iv) are the **NEW** dimension vs. T05.17 —
this is the deepest scaffolding-gap inheritance of any post-OQ-2
eval body landed so far.

## Failure-mode discrimination (what an ERROR vs. FAIL means under E13)

Once the scaffolding gaps close, E13's failure modes are
discriminable:

- **Harness error-path wired but disposition is fail-closed** →
  `Expect.file(logs/hook-errors.jsonl, contains: '"disposition":"fail_open"')`
  FAILs → eval status FAIL → signals the harness DID emit the error
  ledger but chose the wrong disposition (fail-closed). This is a
  correctness regression on the fail-open contract.
- **Harness error-path wired but stderr not surfaced** →
  `Expect.stderr(contains: "failing-post-read.sh")` FAILs → eval
  FAIL → signals the harness emitted the structured ledger row but
  did NOT propagate the hook's stderr to the eval transcript. This
  is a UX regression (the human reader can't see what went wrong).
- **Harness error-path wired but tool exit propagates** →
  `Expect.exit_code(equals: 0)` FAILs → eval FAIL → signals the
  harness did NOT decouple hook exit from process exit (fail-closed
  via process termination). This is the strongest form of the
  fail-open regression.
- **Harness error-path NOT wired** → `logs/hook-errors.jsonl` does
  not exist → all three file-substring expects ERROR (the file
  doesn't exist, so the `exists:true` check ERRORs before the
  `contains:` check runs) → eval status ERROR → signals the
  scaffolding gap (3) is still open.
- **hooks.json-variant not deployed** → production hooks.json fires
  the clean-exit `freshness-post-read.sh` instead of the failing
  fixture → no hook returns non-zero → no `logs/hook-errors.jsonl`
  is written → all three file-substring expects ERROR → eval status
  ERROR → indistinguishable from "harness error-path not wired"
  without inspecting the eval transcript. The inspection hint: the
  eval transcript for the variant-not-deployed case shows clean
  freshness emissions on `logs/freshness.jsonl`; for the
  harness-not-wired case shows a failing-fixture stderr line in the
  raw PTY transcript but no structured ledger row.

Sibling E3-E12 evals depend on the setup wrapper and the production
hooks.json firing correctly; E13 depends additionally on (ii) and
(iii) above. The scaffolding-gap framing in §8.1 of the spec
documents this explicitly to set expectations for the runner-
completion task downstream.

## Inheritance from sibling deferral pattern

The deferral posture in §8.1 follows the same template established
by T05.07 (D-0087 §8.1), T05.08 (D-0088 §8.1), T05.09 (D-0089
§8.1), T05.10/T05.11/T05.13 (D-0090/D-0091/D-0092 §8.1), T05.14
(D-0093 §8.1), T05.15 (D-0094 §3 footnote), T05.16 (D-0095 embedded
in real.yaml E11 comment block), and T05.17 (D-0096 §8.1):

| Task | Deferred construct | Reason |
|---|---|---|
| T05.07..T05.14 | freshness-ledger emit (script telemetry gap) | scripts write to bare integer counters, not OQ-2-contract JSONL |
| T05.15 | `jsonl.event_count(...) >= 1` | needs Python callable filter |
| T05.16 | `event_count(start) == event_count(stop)` symmetry | needs Python callable filter |
| T05.17 | `install_hooks` second invocation + digest unchanged | needs YAML callback escape hatch + digest primitive |
| **T05.19 (this)** | `jsonl.contains_event(type=…, disposition=…)` same-row conjunction + hooks.json-variant deployment + harness structured-error-ledger wiring | needs YAML callback escape hatch (or `isolation.hooks_variant:` schema field) + new declarative primitive (or callback) + harness implementation |

Each deferral lands the OQ-2 body verbatim with the best-effort
declarative proxy, documents the gap explicitly, and gates the
strict form on a future schema/feature/implementation landing.
T05.19 inherits this pattern with the deepest scaffolding-gap stack
(three preconditions, vs. T05.17's zero) — but the manifest body
itself is FR-SCH2-valid and resolves correctly through
`Expect.from_mapping`, satisfying the per-task acceptance criteria
for the body-authoring task.
