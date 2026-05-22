# D-0098 — E14 Concurrent SessionStart Bursts Eval (Body)

**Deliverable ID:** D-0098
**Task ID:** T05.20 (Phase 5)
**Roadmap items:** R-097 (E14 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E14 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E14 — the eleventh
post-OQ-2 hook-surface coverage entry (R-086 … R-098), pinning the
harness's **SessionStart concurrency contract** (design-spec §11 /
OQ-2 D-0082 §4 row E14). E14 is the only entry in the v1 roster that
exercises a **multi-session** surface: N=3 sessions spawned in rapid
succession (within ~200ms of each other) MUST each write their own
per-session sticky `state/auggie-first-pending/<sid>.txt` (no
cross-contamination) and each MUST emit exactly one `session_init`
event in its own per-eval HOME's JSONL ledger.

The regression class motivating E14 is **shared-mutable-state at the
SessionStart boundary**: a hook script or harness path that writes
to a fixed location (no `<sid>` in the path) would have N=3 sessions
race on the same file, surfacing only the last writer's sticky and
corrupting per-session telemetry. E14 pins the no-shared-state
invariant.

E14 is structurally distinct from E3 / E4 (which pin SINGLE-session
SessionStart hook fire) along one axis: **N=3 multi-session
orchestration**. The OQ-2 contract (D-0082 §4 row E14 + D-4 decision
notes) names the v1 implementation mechanism as the **YAML
`callback:` escape hatch** — a programmatic spawn ordering that
cannot be expressed in the declarative input/expects DSL. The
callback (named `superclaude.cli.eval.suites.real_callbacks:
E14_concurrent_session_start` per D-0082 §4) is responsible for:

  (a) spawning N=3 sessions in threads with ~200ms inter-arrival;
  (b) waiting for all 3 PTY sessions to reach prompt-ready;
  (c) collecting the 3 per-session HOMEs' sticky files + JSONL
      ledgers;
  (d) asserting no-shared-mutable-state — 3 distinct sticky files,
      3 distinct session_init JSONL rows, one per session.

The body must:

- run on a fresh per-eval HOME isolated by FR-ISO2 (single-HOME
  proxy; the FULL N=3 multi-HOME variant lives behind the callback
  escape hatch);
- assert the SessionStart-boundary observable shape — sticky-pending
  directory created, session_init event row emitted, PTY teardown
  exit 0 — mapped to the available declarative DSL primitives
  (mapping documented in §3 and §8.1 below);
- exit cleanly so `exit_code.equals(0)` can pin the PTY teardown
  contract — sibling to E3-E13;
- carry no capability tag (`requires: []`) — pure PTY spawn; no
  MCP, no network. Matches OQ-2 D-0082 §6 row E14.

The "YAML `callback:` field" + the "multi-session orchestration"
cannot be expressed in the current declarative DSL **or** the
current schema (`evalEntry.additionalProperties: false` rejects the
`callback:` key). The strict form is deferred to follow-up tasks
per the established T05.07..T05.19 precedent: land the OQ-2 body
verbatim with the best-effort declarative N=1 proxy, document the
gap in §8.1, and gate the strict form on the schema-bump + loader-
extension + EvalRunner callback-invocation wiring described in
D-4 / D-0082 §4.

## 2. Concurrency contract (from design-spec §11 + OQ-2 D-0082 §4)

The harness's SessionStart hook chain (`session-init.sh` +
`freshness-session-start.sh` per `src/superclaude/hooks/hooks.json`)
must produce per-session output keyed by `$SESSION_ID`:

```
For each spawned session i in {1..N=3}:
  1. PTY spawn fires SessionStart hooks before prompt-ready.
  2. session-init.sh writes state/session-init.log under <home_i>.
  3. freshness-session-start.sh writes
     state/auggie-first-pending/<sid_i>.txt under <home_i>.
  4. session-init.sh (per OQ-2 contract) appends
     `{"type":"session_init", "sid":<sid_i>, ...}` to
     <home_i>/.claude/logs/session-events.jsonl.

Multi-session invariants:
  - Each home_i is a DISTINCT per-eval HOME (no cross-pollination).
  - The <sid_i> values are pairwise distinct.
  - Each logs/session-events.jsonl contains exactly ONE
    session_init row (event_count == 1 per session).
  - No state/auggie-first-pending/<sid_i>.txt appears under
    home_j for i != j.
```

The fixture spawn function (per OQ-2 D-0082 §4 row E14) is
`superclaude.cli.eval.suites.real_callbacks:E14_concurrent_session_start`
— a Python callable that uses threads + the PTY harness to drive
the 3 spawns and collects per-session observables for assertion.

| Observable | Purpose |
|---|---|
| `state/auggie-first-pending/<sid>.txt` (per session) | proves the sticky-pending mechanism is keyed by `<sid>` (no shared-mutable-state) |
| `logs/session-events.jsonl` (per session) contains `"type":"session_init"` | proves the session_init event row was emitted in EACH per-session ledger |
| `event_count == 1` per session ledger | proves no duplicate emission (the SessionStart hook chain fires exactly once per spawn) |
| `exit_code == 0` (per session) | proves clean PTY teardown for each spawn — the concurrent spawns don't corrupt each other's exit codepaths |

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E14 entry that
previously carried only a stale placeholder (`title: "doctor reports
MCP gateway reachability"`, `category: doctor` — left over from the
pre-OQ-2 numbering when E14 was a doctor-surface eval). T05.20
replaces the scaffolding with the frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"Concurrent SessionStart bursts"` (matches D-0082 §4 OQ-2 row E14) |
| **category** | `hook-lifecycle` (sibling to E3-E13; was `doctor` in stale stub — the eval surface is the SessionStart hook chain at the multi-session boundary, which is part of the hook lifecycle, not the doctor diagnostics surface) |
| **requires** | `[]` — no capability tags; the callback (once landed) spawns local PTY sessions only |
| **timeout_sec** | `60` (matches E3-E13 sibling parity; in practice the degenerate N=1 proxy is bounded by 1× `/quit` through the PTY, typically <10s — 60s is generous headroom for the N=1 form. The full N=3 multi-session form would need a larger budget; that's a follow-up concern gated on the callback escape hatch landing.) |
| **inputs[0].prompt** | `"/quit"` — fresh PTY session that fires the SessionStart hook chain; immediate clean exit. The N=3 concurrent-spawn aspect is fully deferred to the callback escape hatch (per §3 schema-expressibility constraint below). |
| **expects[0]** | `file: { path: state/auggie-first-pending, exists: true }` — the sticky-pending directory created by `freshness-session-start.sh:91` on every SessionStart; necessary-but-not-sufficient proxy for "each session writes its own `<sid>.txt`" |
| **expects[1]** | `file: { path: logs/session-events.jsonl, exists: true, contains: '"type":"session_init"' }` — single-session degenerate of "3 distinct session_init events"; sibling pattern to E3 |
| **expects[2]** | `exit_code: { equals: 0 }` — clean PTY teardown |

PTY-exclusion tag: `no_pty: skip` (carried forward from the
scaffolding entry — every eval in the `real` suite is PTY-driven
per DOC-OQ3 / R-077).

No additions to `optional_capabilities` — the callback (once
landed) is a pure Python thread-fan-out + PTY spawn; no MCP server
is required.

### Schema-expressibility constraint — the `callback:` field

The OQ-2 D-0082 §4 row E14 inputs shape names a **YAML `callback:`
field** that invokes
`superclaude.cli.eval.suites.real_callbacks:E14_concurrent_session_start`
per the D-4 escape hatch. The current `suites/suite.schema.json`
shape for `evalEntry`:

```json
"evalEntry": {
  "required": ["id", "title"],
  "additionalProperties": false,
  "properties": { "id": ..., "title": ..., "category": ...,
                  "requires": ..., "timeout_sec": ...,
                  "isolation": ..., "inputs": ..., "expects": ...,
                  "parameterize": ..., "no_pty": ... }
}
```

`additionalProperties: false` rejects any unrecognised field; the
D-4 `callback:` escape hatch is documented in `decisions.md` (D-4)
but **not yet wired** into the schema, the loader, OR the EvalRunner.
Adding the field end-to-end requires:

  (a) `suite.schema.json` extension — add `callback: string` (or
      `callback: { module: string, function: string }`) to
      `evalEntry.properties`;
  (b) loader update — `SuiteLoader` resolves the callable from the
      `callback:` string by `importlib.import_module + getattr`;
  (c) EvalRunner update — when an EvalSpec carries a `callback`, the
      runner invokes it (instead of driving inputs through the PTY)
      and consumes the callback's returned outcome shape;
  (d) the `superclaude.cli.eval.suites.real_callbacks` module +
      `E14_concurrent_session_start` function — actual multi-session
      orchestration implementation.

None of (a)-(d) exist today. Per the established T05.07..T05.19
deferral posture, T05.20 lands the OQ-2 body shape with the
best-effort declarative proxy:

- **N=3 → degenerate N=1.** A single PTY session (`inputs[0].prompt:
  "/quit"`) fires the SessionStart hook chain, creates the sticky-
  pending directory, and emits one session_init event — the same
  observable shape E3 / E4 pin for SINGLE-session SessionStart. The
  N=3 concurrency aspect (no-shared-mutable-state across parallel
  spawns) is fully deferred to the callback escape hatch.
- **per-`<sid>` sticky file → directory existence proxy.**
  `Expect.file` (expect.py:187-268) has no glob support and no
  `<sid>` template substitution — the per-session file
  `state/auggie-first-pending/<sid>.txt` cannot be asserted without
  knowing the session_id ahead of time. The directory
  `state/auggie-first-pending/` (created by
  `freshness-session-start.sh:91` on every SessionStart) is a
  necessary-but-not-sufficient proxy: directory presence proves the
  sticky-pending mechanism initialised; the actual per-session file
  presence (and the no-cross-contamination guarantee across N=3
  HOMEs) is deferred.
- **3 distinct session_init events → 1 substring assertion.**
  Inherits the same proxy posture as E3: `file(logs/session-events.jsonl,
  contains '"type":"session_init"')`. The 3-events-across-3-HOMEs
  aspect is deferred (multi-HOME assertion semantics not supported
  — Expect.file resolves against a single EvalContext.home_path per
  expect.py:187-268).
- **`jsonl.event_count == 1` per session → degenerate-N=1 implicit.**
  A single-session run produces exactly one session_init row by
  construction; the per-session count=1 invariant for the multi-
  session case is deferred to the callback escape hatch
  (declarative `jsonl.event_count` requires a Python callable per
  expect.py:269-369).

This proxy posture mirrors the deferral footprint established by
T05.07..T05.19: lands the OQ-2 named ledger paths verbatim with
single-session degenerate observables, defers the schema-bump-gated
strict form to follow-up tasks. T05.20 differs from prior bodies in
ONE structural respect: it depends on a schema EXTENSION (the
`callback:` field) rather than only on a hook-script wiring (E3-E5)
or a hooks.json variant + fixture (E13).

### Scaffolding gap — five preconditions

The OQ-2 input shape requires:

1. **The `callback:` field added to `suite.schema.json`** —
   today's schema (`evalEntry.additionalProperties: false`) rejects
   it.
2. **The loader resolving `callback:` strings to callables** — no
   import path resolution exists in `SuiteLoader`.
3. **The EvalRunner invoking the callback** — `runner.py` drives
   ONE PTY session per eval via `claude_process.py`; there is no
   alternative invocation path that hands control to a Python
   callable.
4. **The `superclaude.cli.eval.suites.real_callbacks` module
   existing** — the named callable `E14_concurrent_session_start`
   has no implementation; the module directory itself does not
   exist.
5. **Multi-HOME isolation orchestration** — the per-eval setup
   wrapper (NFR-ISO2 / T02.13) creates ONE HOME per eval; the
   callback needs to create N=3 distinct HOMEs (one per concurrent
   session) AND have Expect.file resolve assertions against ALL of
   them (or have the callback collect per-session observables and
   return them in a shape the reporter consumes).

In addition, T05.20 inherits two telemetry gaps from E3 / T05.07:

6. **`session-init.sh` doesn't append to `logs/session-events.jsonl`
   today** — the OQ-2 body names this ledger path; the current
   `src/superclaude/hooks/scripts/session-init.sh` writes its own
   `state/session-init.log` but does not emit the
   `{"type":"session_init"}` JSONL row. Follow-up hook-script task
   (shared with E3) is responsible for the emission.
7. **`<sid>` keying on the sticky file is in
   `freshness-session-start.sh:108`** — the script DOES write
   `state/auggie-first-pending/$SESSION_ID.txt`, so the per-`<sid>`
   keying is correct. But the proxy at expects[0] checks DIRECTORY
   existence, not per-session file existence. The strict per-`<sid>`
   assertion form is the deferral (gap #5 above).

Until gaps #1-#5 land, E14's full multi-session execution path is
not invocable. The degenerate N=1 proxy lands the OQ-2-named
observables (sticky-pending directory + session_init event +
clean exit) so the regression-detection envelope is partially
covered TODAY: a regression that breaks the SessionStart hook
chain entirely (no sticky directory, no JSONL ledger, non-zero
PTY exit) would surface via the proxy. The strict no-shared-
mutable-state assertion lives behind the callback escape hatch.

§8.1 documents the deferral with the same "schema-gap +
implementation-gap" framing.

### Why `inputs[0].prompt: "/quit"` (no `expect_tool_call`)

The N=1 proxy doesn't need to PIN a specific tool call (unlike E13
which pinned `expect_tool_call: Read`). The SessionStart hooks fire
BEFORE any tool call is issued — they fire as part of the PTY
spawn handshake, not in response to any specific tool. The `/quit`
input is sufficient to trigger the full SessionStart chain and
exit cleanly.

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E14` is
trivially accepted — `eval describe --suite real --eval E14` returns
the full body and `eval list --json` continues to enumerate 17
evals under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The SessionStart hook chain (session-init.sh +
  freshness-session-start.sh) fires the same way on every PTY
  spawn — same scripts, same matchers, same side-effects.
- The `state/auggie-first-pending/` directory is created
  unconditionally on every SessionStart (per
  freshness-session-start.sh:91) — no time-of-day or network
  dependencies.
- The asserted substring `"type":"session_init"` (once the gap-#6
  hook-script emission lands) is invariant across runs; the
  `ts` / `session_id` fields on the JSONL row, once emitted, are
  not asserted against.
- The `/quit` input causes an immediate clean exit (exit code 0)
  after PTY harness EOF.
- No shared-state dependencies — D-0082 §2 constraint 3 (no
  `CLAUDE_FAKE_TIME_OFFSET`) is honored.

Three consecutive `eval run --suite real --eval E14` invocations
on a clean HOME must therefore yield identical EvalOutcome
statuses, which is the per-task acceptance criterion. (The
determinism contract for the full N=3 multi-session form, once
the callback escape hatch lands, depends on the callback honoring
the same no-time-of-day, no-network, no-shared-state discipline —
the OQ-2 contract says "spawned in rapid succession (within
~200ms of each other) via threads" which is deterministic modulo
wall-clock skew. Same posture as standard thread-fan-out tests in
pytest.)

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved
  at load-time by `Expect.from_mapping` (`expect.py:640-669`). All
  primitives used (2×`file`, 1×`exit_code`) are in `PRIMITIVE_NAMES`
  (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported
  by `Expect.file._build` (`expect.py:187-268`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `requires: []` (empty array) is accepted by the schema.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required **for the proxy body**. The full
OQ-2 shape with the `callback:` field requires a schema bump (see
§3 / §8.1).

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E14 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E14` (no flags) | RUNS (subject to §3 / §8.1 scaffolding gaps for full N=3 shape; the degenerate N=1 proxy runs) | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E14 --no-mcp` | RUNS (subject to §3) | `requires: []` — no MCP capability to skip |
| `eval run --suite real --eval E14 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077); `--no-pty` short-circuits before any eval body executes |
| `eval run --suite real --eval E14 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture matches siblings E3-E7 / E9-E12 / E13 / E15 (which all
carry `requires: []`) and differs from E1 / E2.1-3 / E8 (which
carry MCP capability tags and soft-skip under `--no-mcp`).

## 8. Verification

Per phase-5-tasklist.md T05.20, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E14
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03..T05.19 evidence blocks all block any direct
`eval run` invocation. That blocker is the responsibility of the
runner-completion task (Phase-5 dependency of the CP-P05-T19-T23
checkpoint at T05.24). T05.20 authors the manifest body;
observable verification is therefore via:

- (a) `eval describe --suite real --eval E14` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.20/describe-E14.txt`);
- (b) `eval list --json` continuing to enumerate suite `real` with
  17 evals (proves schema acceptance; see
  `evidence/T05.20/list-with-E14.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.20/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls into
the runner-completion task downstream of T05.20, AND the
scaffolding-gap closure tasks described in §8.1.

### 8.1 Deferred branches — schema gap + multi-session orchestration

OQ-2 D-0082 §4 row E14 specifies a four-part contract:

1. **`callback:` invokes multi-session spawn function.** **Deferred** —
   the schema rejects the `callback:` key today; loader and runner
   have no callback resolution / invocation path; the named callable
   has no implementation. See §3 "Scaffolding gap" gaps #1-#4.
2. **Each session writes its own `state/auggie-first-pending/<sid>.txt`.**
   Landed with the degenerate-N=1 directory-existence proxy
   (`file.exists(state/auggie-first-pending)`). The per-`<sid>`
   file presence + no-cross-contamination invariant across N=3
   HOMEs is deferred to the callback escape hatch (Expect.file
   resolves against a single EvalContext.home_path).
3. **3 distinct session_init events in 3 separate JSONL files.**
   Landed with the degenerate-N=1 single-substring proxy
   (`file(logs/session-events.jsonl, contains '"type":"session_init"')`).
   The 3-events-across-3-HOMEs aspect is deferred to the callback
   escape hatch.
4. **`jsonl.event_count == 1` per session.** Implicit in the N=1
   proxy (one session produces exactly one row by construction);
   the per-session count=1 invariant for the multi-session case is
   deferred to the callback escape hatch (declarative
   `jsonl.event_count` requires a Python callable per
   expect.py:269-369).

Following the same precedent as T05.07..T05.19 (telemetry gaps in
hook scripts, event_count predicates not expressible declaratively,
"twice + digest" deferrals, hooks.json-variant deployment gaps,
structured ledger emission gaps), T05.20 lands the OQ-2 body shape
with the best-effort declarative proxies for branches (2)-(4) and
defers branch (1) to follow-up tasks gated on:

- (a) the `callback:` field added to `suites/suite.schema.json` —
  schema bump + loader extension;
- (b) the `superclaude.cli.eval.suites.real_callbacks` module
  landing with the `E14_concurrent_session_start` function;
- (c) the EvalRunner gaining an alternative invocation path that
  resolves a callable from an EvalSpec.callback and drives the
  multi-session orchestration;
- (d) the multi-HOME isolation orchestration in
  `home_isolation.py` / setup wrapper (N=3 distinct HOMEs per
  callback invocation, with per-session observables collected for
  assertion);
- (e) (shared with E3 / T05.07) `session-init.sh` updated to
  append `{"type":"session_init", ...}` rows to
  `<home>/.claude/logs/session-events.jsonl`.

The proxy retains operational meaning: once (e) lands, the body
catches every regression in the **single-session** SessionStart
hook chain — missing sticky-pending directory, missing
session_init event row, non-zero PTY teardown. The strict no-
shared-mutable-state form (1)-(4) only adds discrimination against
multi-session regressions (a hook writing to a fixed
`state/auggie-first-pending/global.txt` would race; the proxy
can't detect this).

This gap is **not introduced** by T05.20; it predates the
deliverable and is structural to the declarative DSL's
expressibility envelope PLUS the schema's current shape PLUS the
harness's single-session-per-eval execution mode. Acceptance
criteria for T05.20 (manifest body landed, FR-SCH2-valid id, OQ-2
body shape recorded, spec/notes/evidence written) are met by the
describe / list / roundtrip evidence above; the per-task AC that
requires `eval run --eval E14` to exit 0 deterministically depends
transitively on (i) the runner NameError fix and (ii)-(e) the
five scaffolding-gap closures listed in §3.

### 8.2 Failure-mode taxonomy

| Failure mode | Surface | Discriminator |
|---|---|---|
| Runner NameError unblocked, hook script doesn't emit session_init | eval FAIL on expects[1] | "file does not contain '\"type\":\"session_init\"'" — session-init.sh emission gap (#6 above) — shared with E3 / T05.07 |
| Hook chain doesn't create sticky-pending dir | eval FAIL on expects[0] | "file not found at state/auggie-first-pending" — freshness-session-start.sh:91 regression |
| Session_init emission wired, ledger ordering wrong | (proxy can't detect) | the strict per-`<sid>` form (deferred to callback) would catch this; proxy can't |
| Multi-session shared-state regression (fixed-path sticky) | (proxy can't detect) | the strict form (deferred to callback) would catch this; the degenerate N=1 proxy can't differentiate single from multi |
| PTY teardown breakage | eval FAIL on expects[2] | "exit_code != 0" — /quit didn't cleanly exit |

The expects[] ordering is deliberate: expects[0..1] surface the
SessionStart hook chain observables (directory + ledger event)
first; expects[2] discriminates the PTY teardown contract. The
multi-session-specific failure modes are NOT detectable by the
proxy — they are the scaffolding-gap-deferred surface.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E14` |
| Depends on | T04.01 / T04.02 (Expect.file impl) | satisfied by current `expect.py:187-268` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.07..T05.19 (E3..E13 bodies) | E14 is the eleventh post-OQ-2 hook-coverage body; shares `category: hook-lifecycle`, `requires: []`, `timeout_sec: 60`, `/quit` exit pattern |
| Differs from | T05.07..T05.19 (E3..E13 bodies) | E14 is the only entry that depends on a SCHEMA EXTENSION (the `callback:` field per D-4) rather than only on hook-script wiring or hooks.json variants; E14 is also the only entry exercising a MULTI-SESSION surface (others are single-session) |
| Unblocks | T05.21 (E15 author) | downstream peer authoring continues |
| Unblocks | follow-up "schema bump + callback wiring + real_callbacks module + multi-session orchestration" tasks | gated on the five sub-deferrals in §3 / §8.1 |
| Shares deferral with | T05.07 / D-0087 | the `logs/session-events.jsonl` + `"type":"session_init"` substring is the same proxy E3 uses; shared hook-script-emission gap (#6) |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
