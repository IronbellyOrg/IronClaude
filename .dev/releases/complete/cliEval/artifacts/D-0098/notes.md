# D-0098 — Notes / Design Rationale

## Why E14's surface is multi-session concurrency, not a single hook

E3-E11 each pin one row of `src/superclaude/hooks/hooks.json` — the
eval drives Claude Code through the PTY, fires the matched hook, and
reads the freshness ledger to prove the hook script emitted its
event. E12 pins the **deployer** (`hook_adapter.deploy_hooks_to`).
E13 pins the **harness's hook-execution error-handling path**. E14
is structurally distinct from all of them: its surface is the
**SessionStart hook chain at the multi-session boundary** — the
shared-mutable-state regression class that arises when N concurrent
sessions fire SessionStart hooks within a small time window.

The body is intentionally hook-event-agnostic on the strict form:
the OQ-2 contract (D-0082 §4 row E14) names per-session
`state/auggie-first-pending/<sid>.txt` (sticky), per-session
`logs/session-events.jsonl` (session_init), and per-session
`event_count == 1`. The regression class motivating E14 is **any
hook script or harness path that writes to a fixed location (no
`<sid>` in the path)**: such a path would have N=3 sessions race on
the same file, surfacing only the last writer's sticky and
corrupting per-session telemetry.

The natural strict body shape is: spawn N=3 PTY sessions in rapid
succession (~200ms inter-arrival), wait for all 3 to reach
prompt-ready, then assert four observable guarantees of the
no-shared-mutable-state contract:

1. Each session's per-eval HOME contains its own
   `state/auggie-first-pending/<sid>.txt` (no cross-contamination).
2. Each session's per-eval HOME contains exactly one session_init
   event in its `logs/session-events.jsonl` ledger.
3. The `<sid>` values are pairwise distinct (no SESSION_ID reuse).
4. Each PTY teardown exits cleanly (no inter-process corruption).

That's the OQ-2 contract verbatim. The body assertions ATTEMPTED to
pin all four guarantees with the best-effort declarative proxies,
but the multi-session orchestration itself is unexpressible in the
current declarative DSL — it requires a Python callable that
threads spawn fan-out + per-session HOME collection. D-4's YAML
`callback:` escape hatch is the named vehicle, deferred to follow-up
tasks gated on schema + loader + runner extensions.

## Why the declarative DSL can't express N=3 multi-session

The DSL is single-input, single-PTY-spawn, single-HOME by design:

- `inputs[]` enumerates a SEQUENCE of prompts driven through ONE
  PTY in order (per `EvalRunner._execute_eval` driving
  `claude_process.send_input` per-input).
- `EvalContext.home_path` is a SINGLE per-eval HOME directory
  created by the setup wrapper (NFR-ISO2 / T02.13) — not a list of
  N HOMEs.
- `Expect.file(path=..., exists=..., contains=...)` resolves `path`
  against `EvalContext.home_path` per `expect.py:187-268` — no
  multi-HOME assertion semantics.

To express N=3 multi-session concurrency, the runner must:

1. Detect an alternative invocation mode (callback vs. PTY-driven).
2. Hand control to a Python callable instead of driving inputs.
3. Provide the callable with primitives to spawn isolated PTY
   sessions in parallel (N distinct HOMEs).
4. Collect per-session observables (sticky files, JSONL rows, exit
   codes) and return them in a shape the reporter consumes.

None of those orchestration primitives exist today. The current
runner is single-PTY-per-eval, structurally. The OQ-2 D-0082 §4
row E14 explicitly names the v1 implementation mechanism as the
**YAML `callback:` field**, which (a) needs to land in the schema,
(b) needs loader-side string→callable resolution, (c) needs
runner-side callback invocation, (d) needs the named callable to
exist, and (e) needs multi-HOME orchestration in the setup wrapper.
None of (a)-(e) exist today; T05.20 lands the body that names the
contract and depends on them.

## Why the proxy posture is "degenerate N=1" (single PTY session)

Given the five preconditions above are not met, T05.20's options
were:

- **Option A: Land an OQ-2-shaped body with N=3 multi-session
  orchestration via the callback escape hatch.** Rejected — the
  callback field isn't schema-valid, the loader doesn't resolve it,
  the runner doesn't invoke it, and the named callable doesn't
  exist. Landing this body would produce a schema validation error
  in `SuiteLoader.load`, blocking the entire suite from
  enumerating.
- **Option B: Land a degenerate N=1 body with single-PTY-session
  observables (sticky-pending directory + session_init ledger event
  + clean PTY exit).** Selected — the body satisfies FR-SCH2 (id
  matches regex), the schema accepts the entry (no `callback:`
  field), `Expect.from_mapping` resolves all 3 expects cleanly, and
  the suite continues to enumerate. The body's assertions are
  necessary-but-not-sufficient for the OQ-2 contract: they catch
  single-session SessionStart regressions but cannot catch
  multi-session shared-state regressions.
- **Option C: Skip the eval entirely (no body) until the callback
  escape hatch lands.** Rejected — the OQ-2 resolution explicitly
  scheduled E14 for T05.20 authoring; skipping would violate the
  per-task acceptance criteria ("File `suites/real.yaml` contains
  entry `id: E14` matching the OQ-2 resolution").

Option B mirrors the deferral posture established by T05.07..T05.19
(land OQ-2-named observables with declarative proxies; document
scaffolding gaps without introducing them).

## Why `state/auggie-first-pending` (directory, not per-`<sid>` file)

`freshness-session-start.sh:91` creates the directory
`$STATE_DIR/auggie-first-pending` unconditionally on every
SessionStart, then `:108` writes
`$STATE_DIR/auggie-first-pending/$SESSION_ID.txt` to mark the
session as auggie-first-pending. The OQ-2 contract names the
per-`<sid>` file as the asserted observable.

`Expect.file(path=..., exists=true)` (`expect.py:187-268`) does:

- string `path` resolution against `EvalContext.home_path`;
- single-file existence check via `Path.exists()`;
- no glob support, no template substitution, no `<sid>` placeholder
  resolution (the eval doesn't know the session_id ahead of time —
  it's generated by the PTY harness at spawn).

The two options for asserting the per-`<sid>` file:

- **(a) Glob-based `Expect.file_glob` primitive** — would let the
  body say `file_glob(state/auggie-first-pending/*.txt,
  exists: true)`. Doesn't exist today; would need a new primitive
  in `expect.py` + schema entry.
- **(b) Callback-collected per-session observable** — the
  E14_concurrent_session_start callback would collect each
  session's actual sticky file path and assert directly. Doesn't
  exist today (gaps #1-#5).

T05.20 falls back to **directory existence**: the directory IS
created by `freshness-session-start.sh:91` on every SessionStart,
so presence of the directory proves the sticky-pending mechanism
initialised. This is **necessary-but-not-sufficient** for the
per-`<sid>` form: a hypothetical regression where
`freshness-session-start.sh` creates the directory but fails to
write any `<sid>.txt` file would satisfy the proxy and violate the
strict semantic. In practice the two lines (`:91 mkdir` + `:108 :>
sid.txt`) are co-located in the script, so the proxy converges with
the strict semantic.

## Why `logs/session-events.jsonl` substring (not 3× row count)

The OQ-2 contract names "3 distinct session_init events in 3
separate JSONL files". The N=1 proxy collapses this to "1
session_init event in 1 JSONL file":
`file(logs/session-events.jsonl, contains '"type":"session_init"')`.
The proxy:

- proves the SessionStart hook chain emitted a session_init row to
  the per-eval HOME's ledger;
- does NOT prove the event_count==1 invariant (declarative
  `jsonl.event_count` needs a Python callable, deferred to the
  callback);
- does NOT prove the 3-across-3-HOMEs no-cross-contamination
  invariant (multi-HOME assertion isn't expressible without
  callbacks).

This proxy is shared with E3 / T05.07 — both inherit the
**hook-script emission gap** (`session-init.sh` doesn't yet append
`{"type":"session_init", ...}` rows to `logs/session-events.jsonl`).
Once that gap closes (shared follow-up with E3), the proxy catches
the single-session emission regression for E14; the multi-session
discrimination remains gated on the callback.

## Why `exit_code: equals 0` (not multi-session exit code matrix)

The OQ-2 contract says each of N=3 PTY teardowns must exit cleanly.
The N=1 proxy asserts ONE PTY exit code. Sibling parity with
E3-E13 / E15 (all assert `exit_code.equals(0)` against the single
PTY teardown).

The multi-session exit-code matrix (3 exit codes, all == 0) is
implicit in the callback's per-session observable collection: the
callback would return a per-session list of exit codes, and the
reporter would assert all match 0. Deferred to the callback.

## Why `category: hook-lifecycle` (sibling parity)

The stale E14 placeholder carried `category: doctor` (a leftover
from the pre-OQ-2 numbering when E14 was "doctor reports MCP
gateway reachability"). The OQ-2 resolution reassigned E14 to the
SessionStart multi-session boundary, which is part of the hook
lifecycle. The category options:

- `harness` or `concurrency` — technically accurate (the surface IS
  the harness's multi-session orchestration boundary), but no other
  eval in the suite uses these categories; creating singleton
  categories creates noise in `eval list` filtering.
- `doctor` — wrong (E14 doesn't exercise any doctor surface).
- `hook-lifecycle` — the sibling category for E3-E13. E14 covers
  the multi-session boundary of the SessionStart hook chain
  (sticky-pending + session_init telemetry); E3 / E4 cover the
  single-session boundary. The category groups them together for
  filtering and reporting purposes.

T05.20 picks `hook-lifecycle` for sibling parity, matching the
T05.07 / E3 + T05.19 / E13 precedent.

## Why `requires: []` (not `[mcp_server.*]`)

The callback (once landed) spawns local PTY sessions only — no
network, no MCP servers, no external binaries beyond the standard
`claude` CLI binary that the PTY harness already drives. The
degenerate N=1 proxy is even simpler: a single `/quit` through one
PTY. Per D-0082 §6 capability-tag rollup, E14's row lists no
capability tag.

The practical implication: E14 runs under `--no-mcp` (the
matcher-coverage gate counts it as a non-MCP eval), and the only
way E14 skips is via `--no-pty` (per-eval `no_pty: skip` tag).
Matches siblings E3-E7 / E9-E12 / E13 / E15.

## What this body does NOT assert (and why)

The OQ-2 D-0082 §4 row E14 frames four explicit observable
contracts:

1. **N=3 sessions spawned in rapid succession** — NOT asserted in
   the proxy (single PTY session). Deferred to callback.
2. **Each session writes its own `<sid>.txt` sticky (no
   cross-contamination)** — partially asserted via directory
   existence; per-`<sid>` form deferred to callback.
3. **3 distinct session_init events in 3 separate JSONL files** —
   partially asserted via single-substring presence; multi-HOME
   form deferred to callback.
4. **`event_count == 1` per session** — implicit in N=1; per-session
   form deferred to callback.

Plus one inherited gap from E3 / T05.07:

5. **`session-init.sh` doesn't append to `logs/session-events.jsonl`
   today** — the OQ-2 body names this ledger path; the current
   hook script writes `state/session-init.log` but does not emit
   the `{"type":"session_init"}` JSONL row. Once the shared
   follow-up hook-script task lands the emission (responsibility
   shared with E3), the proxy at expects[1] becomes operational.

The strict no-shared-mutable-state form (contracts 1-4) is gated
on the YAML `callback:` escape hatch (D-4) — schema bump + loader
extension + runner callback-invocation path + the
`real_callbacks.E14_concurrent_session_start` module +
multi-HOME isolation orchestration.

## Scaffolding-gap inheritance (DEEPER than T05.17 and T05.19)

| Task | Scaffolding gaps inherited |
|---|---|
| T05.17 (E12) | **0** — install_hooks adapter + setup wrapper materialize post-first-deploy shape today |
| T05.19 (E13) | **3** — failing fixture script doesn't exist, hooks.json-variant deployment path doesn't exist, harness structured-error-ledger emission not wired |
| **T05.20 (E14, this)** | **5** — `callback:` schema field, loader callback resolution, runner callback invocation, `real_callbacks` module, multi-HOME isolation orchestration; PLUS one inherited gap (session-init.sh emission, shared with E3) |

T05.20 inherits the deepest scaffolding-gap stack of any post-OQ-2
eval body landed so far. The deferred form depends on a
**schema extension**, not just on hook-script wiring or hooks.json
variants. The five preconditions (per spec §3) are each independent
follow-up tasks; they could land in any order. The proxy body that
T05.20 lands TODAY is FR-SCH2-valid and resolves through
`Expect.from_mapping` — meeting the per-task acceptance criteria
for the body-authoring deliverable.

## Failure-mode discrimination (what an ERROR vs. FAIL means under E14)

Once gap #6 (session-init.sh emission) closes, the proxy's failure
modes are discriminable:

- **Hook chain doesn't create sticky-pending directory** →
  `Expect.file(state/auggie-first-pending, exists: true)` FAILs →
  eval FAIL → signals a regression in
  `freshness-session-start.sh:91` (the `mkdir -p` line).
- **session-init.sh emits to ledger but no `"type":"session_init"`
  substring** → `Expect.file(logs/session-events.jsonl,
  contains: '"type":"session_init"')` FAILs → eval FAIL → signals
  a schema regression in the JSONL emission (the type field renamed
  or omitted).
- **Hook chain crashes mid-spawn** → `Expect.exit_code(equals: 0)`
  FAILs → eval FAIL → signals a PTY teardown regression.
- **Ledger doesn't exist at all** → `Expect.file(logs/session-events.jsonl,
  exists: true)` FAILs (the `exists: true` check is evaluated
  before the `contains:` check) → eval FAIL → signals
  `session-init.sh` didn't emit anything OR the file path moved.
- **All proxies pass but multi-session races on shared state** →
  (proxy can't detect) — the strict per-`<sid>` form (deferred to
  callback) would catch this; the degenerate N=1 proxy cannot
  differentiate single from multi.

The last failure mode is the **structural blind spot** of the
proxy: a multi-session shared-state regression is undetectable by
the N=1 proxy. The mitigation is the deferred callback escape
hatch, which IS the OQ-2-named v1 mechanism.

## Inheritance from sibling deferral pattern

The deferral posture in §8.1 follows the same template established
by T05.07..T05.19:

| Task | Deferred construct | Reason |
|---|---|---|
| T05.07..T05.14 | freshness-ledger emit (script telemetry gap) | scripts write to bare integer counters, not OQ-2-contract JSONL |
| T05.15 | `jsonl.event_count(...) >= 1` | needs Python callable filter |
| T05.16 | `event_count(start) == event_count(stop)` symmetry | needs Python callable filter |
| T05.17 | `install_hooks` second invocation + digest unchanged | needs YAML callback escape hatch + digest primitive |
| T05.19 | `jsonl.contains_event(type=…, disposition=…)` same-row conjunction + hooks.json-variant deployment + harness structured-error-ledger wiring | needs YAML callback escape hatch + new declarative primitive (or callback) + harness implementation |
| **T05.20 (this)** | YAML `callback:` field + multi-session spawn orchestration + multi-HOME isolation + per-`<sid>` glob assertion + per-session event_count==1 | needs schema bump + loader extension + runner callback-invocation path + `real_callbacks` module + setup-wrapper multi-HOME mode |

Each deferral lands the OQ-2 body verbatim with the best-effort
declarative proxy, documents the gap explicitly, and gates the
strict form on a future schema/feature/implementation landing.
T05.20 inherits this pattern with the deepest scaffolding-gap
stack and the only schema-extension-gated deferral — but the
manifest body itself is FR-SCH2-valid and resolves correctly
through `Expect.from_mapping`, satisfying the per-task acceptance
criteria for the body-authoring task.
