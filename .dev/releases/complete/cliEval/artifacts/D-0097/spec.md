# D-0097 — E13 Hook Stderr Error Fails Open Eval (Body)

**Deliverable ID:** D-0097
**Task ID:** T05.19 (Phase 5)
**Roadmap items:** R-096 (E13 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E13 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E13 — the tenth post-OQ-2
hook-surface coverage entry (R-086 … R-098), pinning the harness's
**hook stderr error-path discipline** (design-spec §11 / OQ-2 D-0082
§4 row E13). E13 exercises the documented fail-open contract:

> A hook script that returns a non-zero exit code with content on
> stderr MUST NOT cause an apparent tool failure. The harness must
> (a) complete the matched tool call successfully, (b) capture the
> hook's stderr to the eval transcript so a human reader can see what
> went wrong, and (c) emit a structured `{type:"hook_error",
> disposition:"fail_open"}` row to `logs/hook-errors.jsonl` so the
> failure is auditable post-run.

The regression class motivating E13 is: a misbehaving hook script
surfaces its own stderr as if the matched TOOL had failed — the
agent sees the hook's error message instead of the tool's result.
This is the "hook stderr causes apparent tool failure" bug noted in
the OQ-2 D-0082 §4 row E13.

E13 is structurally distinct from E3-E12 along two axes:

1. **Cross-cutting surface (the harness, not a single hook).** E3-E11
   each exercise one hook event entry from `hooks.json`; E12 covers
   the install_hooks adapter; E13 covers the **harness's error-
   handling path** — the code that runs when ANY hook returns
   non-zero. The eval is hook-event-agnostic by design (a failing
   PostToolUse Read hook happens to be the concrete fixture, but
   the assertion shape would apply equally to a failing PreToolUse
   Edit hook or a failing SessionStart hook).
2. **Requires a hooks.json variant deployment.** Unlike E3-E12, which
   all run against the production `src/superclaude/hooks/hooks.json`
   shipped via `hook_adapter.deploy_hooks_to`, E13 requires a
   **test-only** hooks.json variant that registers the failing
   fixture (`tests/fixtures/hooks/failing-post-read.sh`) as the
   PostToolUse Read handler — otherwise the matched tool call would
   fire the production `freshness-post-read.sh` (which exits cleanly)
   and no hook error would surface. See §3 "Scaffolding gap" for
   the deferral.

The body must:

- run on a fresh per-eval HOME isolated by FR-ISO2 — the harness's
  error-logging path writes to `<home>/.claude/logs/hook-errors.jsonl`
  which must not exist prior to the run;
- assert the harness's three-part fail-open contract (tool call
  succeeds, stderr captured, structured error row emitted) — mapped
  to the available declarative DSL primitives (mapping documented
  in §3 and §8.1 below);
- exit cleanly so `exit_code.equals(0)` can pin the PTY teardown
  contract — sibling to E3-E12;
- carry no capability tag (`requires: []`) — the failing fixture is
  a pure shell script; no MCP, no network.

The "hooks.json variant deployment" + the "structured `{type,
disposition}` event-count predicate" cannot be expressed in the
current declarative DSL. The strict declarative form is deferred to
follow-up tasks per the established T05.07..T05.17 precedent: land
the OQ-2 body verbatim with the best-effort declarative proxies,
document the gap in §8.1, and gate the strict form on the YAML
callback escape hatch / a future schema extension.

## 2. Hook error-path contract (from design-spec §11 + OQ-2 D-0082 §4)

The harness's hook-execution loop (commands.py / runner.py hook-exec
path) wraps each hook script invocation and is responsible for the
fail-open discipline:

```
For each hook in hooks.json matching the current event:
  1. Spawn hook script with timeout from `timeout:` field.
  2. Capture stdout (envelope-parsed), stderr (line-captured), and
     exit code.
  3. If exit code != 0:
     a. The tool call MUST continue (fail-open) — the hook does NOT
        block the matched tool's result from reaching the agent.
     b. The hook's stderr MUST be propagated to the eval transcript
        (so the human reader sees what went wrong).
     c. A structured `{type:"hook_error", disposition:"fail_open",
        hook:<script-name>, exit_code:<n>, stderr:<truncated>, ...}`
        row MUST be appended to `<home>/.claude/logs/hook-errors.jsonl`.
  4. If exit code == 0:
     normal-path telemetry only (no hook-errors.jsonl row).
```

The fixture script (per OQ-2 D-0082 §4 row E13) is
`tests/fixtures/hooks/failing-post-read.sh` — a deterministic-exit
shell script that prints a known message to stderr and exits with
a non-zero code. The eval registers it as the PostToolUse Read
handler in a test-only hooks.json variant; the inputs trigger a
Read; the harness fires the failing hook; the harness logs the
error and fails open; the assertions pin all three observable
guarantees.

| Observable | Purpose |
|---|---|
| `logs/hook-errors.jsonl` exists post-run | proves the harness opened the error ledger at all |
| `logs/hook-errors.jsonl` contains `"type":"hook_error"` substring | proves the harness emitted a hook_error-typed row |
| `logs/hook-errors.jsonl` contains `"disposition":"fail_open"` substring | proves the disposition was fail-open (vs. fail-closed) |
| `stderr` contains `"failing-post-read.sh"` | proves the hook's stderr was captured + surfaced to the eval transcript |
| Process exits cleanly (exit_code == 0) | proves the failing hook did NOT propagate up to the eval-process exit code (the fail-open contract decouples hook exit from process exit) |

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E13 entry that
previously carried only a stale placeholder (`title: "doctor surfaces
stale ~/.claude/settings.json schema"`, `category: doctor` — left
over from the pre-OQ-2 numbering when E13 was a doctor-surface eval).
T05.19 replaces the scaffolding with the frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"Hook stderr error fails open"` (matches D-0082 §4 OQ-2 row E13) |
| **category** | `hook-lifecycle` (sibling to E3-E12; was `doctor` in stale stub — the eval surface is the harness's hook error-handling path, which is part of the hook lifecycle, not the doctor diagnostics surface) |
| **requires** | `[]` — no capability tags; the failing fixture is a pure shell script, no MCP, no network |
| **timeout_sec** | `60` (matches E3-E12 sibling parity; in practice the eval is bounded by 1 Write + 1 Read + /quit through the PTY, typically <10s — 60s is generous headroom) |
| **inputs[0].prompt** | seed `fixture.txt` via Write so the subsequent Read has a target (mirrors E9's fixture-seeding pattern) |
| **inputs[1].prompt** | trigger a Read of `fixture.txt`; this is the call whose PostToolUse hook (the failing fixture) returns non-zero — the surface this eval asserts; carries `expect_tool_call: Read` to pin the matched tool |
| **inputs[2].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract |
| **expects[0]** | `file: { path: logs/hook-errors.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/hook-errors.jsonl, exists: true, contains: '"type":"hook_error"' }` |
| **expects[2]** | `file: { path: logs/hook-errors.jsonl, exists: true, contains: '"disposition":"fail_open"' }` |
| **expects[3]** | `stderr: { contains: "failing-post-read.sh" }` |
| **expects[4]** | `exit_code: { equals: 0 }` |

PTY-exclusion tag: `no_pty: skip` (carried forward from the
scaffolding entry — every eval in the `real` suite is PTY-driven
per DOC-OQ3 / R-077).

No additions to `optional_capabilities` — the failing fixture is a
pure shell script; no MCP server is required.

### Schema-expressibility constraint — the `contains_event(type=..., disposition=...)` proxy

The OQ-2 D-0082 §4 row E13 expect shape names a conjunctive
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
  must be present for the eval to pass. The proxy is **necessary
  but not sufficient** for the strict semantic: it does not prove
  the two substrings appeared on the SAME JSONL row (a hypothetical
  pathological emit pattern that wrote `{type:hook_error,
  disposition:fail_closed}` on one row and `{type:other_thing,
  disposition:fail_open}` on a second row would satisfy the
  proxies but violate the strict semantic). In practice the
  harness's error-logging path emits all four fields on a single
  row by design (per design-spec §11), so the proxy converges with
  the strict semantic; an emit-pattern regression that split them
  across rows would itself be a bug worth surfacing.
- **Event-count proxy:** none — the OQ-2 shape doesn't require
  `event_count == 1`, only `contains_event` (at-least-once), so
  the substring presence proxy is a complete coverage of the
  at-least-once aspect.

This proxy posture mirrors the two-substring `{type, matcher}`
pattern used by E6 / E7 / E8 (PreToolUse matcher coverage):
matching primitives, matching mechanism (Expect.file with JSONL
substring), matching deferral footprint (declarative DSL
expressibility limitation). The conjunctive `{type, matcher}`
shape converges with the strict semantic for the same reason
described above (the harness emits all matcher-pin fields on a
single row by design).

### Scaffolding gap — the failing fixture + hooks.json variant deferral

The OQ-2 input shape requires a **test-only hooks.json variant**
that registers `tests/fixtures/hooks/failing-post-read.sh` as the
PostToolUse Read handler. Three preconditions are needed:

1. **The fixture script `tests/fixtures/hooks/failing-post-read.sh`
   must exist on disk.** Today it does not (per the codebase grep:
   `tests/fixtures/hooks/` directory does not exist; no
   `failing-post-read*` file anywhere in the repo). A follow-up
   task is responsible for landing the fixture as a deterministic-
   exit shell script (e.g., `printf "simulated hook failure\n" >&2;
   exit 17`).
2. **A hooks.json-variant deployment path must exist.** The per-eval
   setup wrapper (NFR-ISO2 / T02.13) deploys the production
   `src/superclaude/hooks/hooks.json` verbatim via
   `hook_adapter.deploy_hooks_to(home_path)`. There is no
   `isolation.hooks_variant:` field on `evalEntry` and no
   `inputs[].setup:` callback that could swap in a test-only
   hooks.json with the failing fixture registered. Two options
   for landing this:
   - (a) the YAML `callback:` escape hatch (D-4) — a callback that
     writes a test-only hooks.json to `<home>/.claude/hooks.json`
     and `<home>/.claude/settings.json` before the PTY session
     opens;
   - (b) a new `isolation.hooks_variant: <path>` schema field that
     points to a test-only hooks.json fixture, with the setup
     wrapper preferring the variant over the production hooks.json
     when present.
3. **The harness's structured hook-error ledger must be wired.** The
   harness currently propagates hook stderr opaquely (commands.py
   hook-exec path captures it but does not emit a structured
   `{type:"hook_error", disposition:"fail_open"}` row to
   `logs/hook-errors.jsonl`). A follow-up task is responsible for
   wiring the structured-error-ledger emission on the
   non-zero-exit hook path.

Until all three land, E13's full end-to-end execution path
(`eval run --suite real --eval E13`) will surface predictable
failures: the harness deploys the production hooks.json (no
failing fixture is registered), no PostToolUse hook fails, no
`logs/hook-errors.jsonl` is written, and the eval ERRORs with
"file not found at logs/hook-errors.jsonl". This is the correct
failure mode — surfacing each missing precondition incrementally.

§8.1 documents the deferral with the same "telemetry gap" framing
established by T05.07..T05.17. Acceptance criteria for T05.19 are
met by the describe / list / round-trip evidence (the manifest body
is FR-SCH2-valid, OQ-2-shaped, and resolves through
`Expect.from_mapping`); the per-task AC requiring full end-to-end
`eval run --eval E13` execution depends transitively on (i) the
runner NameError fix at `commands.py:1418`, (ii) the failing
fixture script existing, (iii) the hooks.json-variant deployment
path landing, and (iv) the harness's structured hook-error ledger
being wired.

### Why `expect_tool_call: Read` (not just a free-form prompt)

The OQ-2 input shape names "inject prompt triggering a Read". The
declarative `inputs[].expect_tool_call: Read` field (recognized by
the PTY input dispatch per `commands.py` input loop) pins the
matched tool to `Read`, ensuring the PTY harness waits for the
specific tool call to fire before treating the input as resolved
(rather than accepting any in-session output as completion). This
mirrors E8's `expect_tool_call: mcp__serena__replace_content` and
E9's `expect_tool_call: Read` patterns.

### Why a seed Write before the Read

`Read` requires a target file. The seed Write creates `fixture.txt`
under the per-eval HOME's cwd, then the subsequent Read targets it.
This mirrors E9's two-step (Write fixture, Read fixture) pattern.
The seed Write also fires the PreToolUse hook on the Write matcher
branch (covered independently by E7) — that co-fire is harmless
because E13's assertions pin error-path events keyed by
`type:"hook_error"` on `logs/hook-errors.jsonl`, not pre_edit
telemetry on `logs/freshness.jsonl`.

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E13` is
trivially accepted — `eval describe --suite real --eval E13` returns
the full body and `eval list --json` continues to enumerate 17
evals under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The failing fixture (once landed per §3 scaffolding gap) is a
  deterministic-exit shell script — same exit code + same stderr
  message on every invocation, with no time-of-day or network
  dependencies.
- The harness's error-logging path (once wired) is a pure-append to
  `logs/hook-errors.jsonl` — no shared-state dependencies, no
  ordering ambiguity (the failing hook fires once per matched Read,
  the eval triggers exactly one Read, so the ledger contains exactly
  one error row).
- The asserted substrings (`"type":"hook_error"`,
  `"disposition":"fail_open"`, `"failing-post-read.sh"`) are
  invariant across runs (the `ts`, `session_id`, `tool_call_idx`,
  `stderr` (truncated copy) fields on the JSONL row, once emitted,
  are not asserted against).
- The `/quit` input causes an immediate clean exit (exit code 0)
  after PTY harness EOF.
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored.

Three consecutive `eval run --suite real --eval E13` invocations on
a clean HOME must therefore yield identical EvalOutcome statuses,
which is the per-task acceptance criterion. (The determinism
contract is independent of the scaffolding gap — once the gap
closes, the body is determined by construction.)

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` and `inputs[].expect_tool_call: string`
  (additionalProperties: true under `evalEntry.inputs.items` per
  `suite.schema.json`).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved
  at load-time by `Expect.from_mapping` (`expect.py:640-669`). All
  primitives used (3×`file`, 1×`stderr`, 1×`exit_code`) are in
  `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported
  by `Expect.file._build` (`expect.py:187-268`).
- `stderr` primitive kwarg `contains` is supported by
  `Expect.stderr._build` (`expect.py:556-569`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `requires: []` (empty / omitted) is accepted by the schema.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E13 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E13` (no flags) | RUNS (subject to §3 scaffolding gap) | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E13 --no-mcp` | RUNS (subject to §3) | `requires: []` — no MCP capability to skip; failing fixture is pure shell |
| `eval run --suite real --eval E13 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077); `--no-pty` short-circuits before any eval body executes |
| `eval run --suite real --eval E13 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture matches siblings E3-E7 / E9-E12 (which also carry
`requires: []`) and differs from E1 / E2.1-3 / E8 (which carry MCP
capability tags and soft-skip under `--no-mcp`).

## 8. Verification

Per phase-5-tasklist.md T05.19, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E13
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03..T05.17 evidence blocks all block any direct
`eval run` invocation. That blocker is the responsibility of the
runner-completion task (Phase-5 dependency of the CP-P05-T13-T17
checkpoint at T05.18). T05.19 authors the manifest body; observable
verification is therefore via:

- (a) `eval describe --suite real --eval E13` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.19/describe-E13.txt`);
- (b) `eval list --json` continuing to enumerate suite `real`
  with 17 evals (proves schema acceptance; see
  `evidence/T05.19/list-with-E13.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.19/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls into
the runner-completion task downstream of T05.19, AND the
scaffolding-gap closure tasks described in §8.1.

### 8.1 Deferred branches — scaffolding gap + contains_event predicate

OQ-2 D-0082 §4 row E13 specifies a four-part contract:

1. **Tool call completes successfully (fail-open).** Landed verbatim
   via `exit_code.equals(0)` — the PTY-teardown exit code being 0
   is the necessary downstream observable for "the failing hook
   did not propagate up to the eval-process exit code". (Strict
   form would also assert the Read tool's specific result reached
   the agent; deferred to a future per-tool-result primitive.)
2. **Stderr captured.** Landed verbatim via
   `stderr.contains("failing-post-read.sh")` — the OQ-2-named
   `stderr.contains(failing_hook_script_name)` assertion, with
   the script name literalized from the OQ-2-named fixture path.
3. **Hook-error ledger row present with `{type:hook_error,
   disposition:fail_open}` fields.** Landed with the declarative
   proxy: three `Expect.file` rows on `logs/hook-errors.jsonl`
   (one for existence, one for each of the two substring pins).
   Strict `Expect.jsonl.contains_event(type=hook_error,
   disposition=fail_open)` requires a Python callable filter
   (expect.py:269-369), not expressible in declarative YAML.
4. **The harness wires all of the above.** **Deferred** — the
   harness today does not (a) deploy a hooks.json variant with the
   failing fixture, (b) emit a structured hook-error ledger on
   non-zero hook exit, or (c) include a fixture script at
   `tests/fixtures/hooks/failing-post-read.sh`. See §3 "Scaffolding
   gap" for the three sub-deferrals.

Following the same precedent as T05.07..T05.17 (telemetry gaps in
freshness scripts, event_count predicates not expressible
declaratively, "twice + digest" deferrals), T05.19 lands the OQ-2
body shape with the best-effort declarative proxies for branches
(1)-(3) and defers branch (4) to follow-up tasks gated on:

- (a) the failing fixture script landing at
  `tests/fixtures/hooks/failing-post-read.sh`;
- (b) the YAML `callback:` escape hatch (D-4) OR a new
  `isolation.hooks_variant:` schema field, plus the per-eval
  setup wrapper honoring the variant deployment;
- (c) the harness's structured hook-error ledger being wired into
  the hook-exec path (commands.py / runner.py) to emit
  `{type:"hook_error", disposition:"fail_open", hook:..., exit_code:...,
  stderr:..., ts:..., session_id:..., tool_call_idx:...}` rows to
  `<home>/.claude/logs/hook-errors.jsonl` on non-zero hook exit;
- (d) a future schema bump adding declarative
  `jsonl.contains_event:` primitive shorthand (optional — the
  two-substring proxy is operationally meaningful as documented
  in §3 above).

(d) is optional because the two-substring proxy converges with the
strict semantic in the absence of pathological emit patterns; (a)-(c)
are required for ANY end-to-end execution of E13 to pass at all.

The proxy retains operational meaning: once (a)-(c) land, the body
catches every regression in the harness's fail-open discipline —
missing ledger file, wrong type field, wrong disposition field,
swallowed stderr, propagated hook exit code. The strict
`contains_event` form (d) only adds discrimination against
pathological emit-patterns that split the two pinned fields across
multiple JSONL rows, which is itself an emit-pattern bug worth
surfacing through other channels.

This gap is **not introduced** by T05.19; it predates the
deliverable and is structural to the declarative DSL's
expressibility envelope PLUS the harness's current error-handling
maturity. Acceptance criteria for T05.19 (manifest body landed,
FR-SCH2-valid id, OQ-2 body shape recorded, spec/notes/evidence
written) are met by the describe / list / roundtrip evidence above;
the per-task AC that requires `eval run --eval E13` to exit 0
deterministically depends transitively on (i) the runner NameError
fix and (ii)-(iv) the four scaffolding-gap closures listed in §3.

### 8.2 Failure-mode taxonomy

| Failure mode | Surface | Discriminator |
|---|---|---|
| Runner NameError unblocked, fixture missing | eval ERROR | "hook script not found at tests/fixtures/hooks/failing-post-read.sh" (or hooks.json validation error) |
| Fixture exists, hooks.json variant deployment missing | eval FAIL on expects[0..2] | "file not found at logs/hook-errors.jsonl" — production hooks.json deployed, no hook fails, no ledger row emitted |
| Variant deployment wired, ledger emission missing | eval FAIL on expects[0..2] | "file not found at logs/hook-errors.jsonl" — failing hook fires but harness doesn't emit structured error row |
| Ledger emission wired, wrong type | eval FAIL on expects[1] | "file does not contain '\"type\":\"hook_error\"'" — type field mislabeled |
| Ledger emission wired, fail-closed regression | eval FAIL on expects[2] | "file does not contain '\"disposition\":\"fail_open\"'" — disposition field wrong (suggests fail-closed regression that would also fail expects[4] via non-zero exit) |
| Ledger emission wired, stderr swallowed | eval FAIL on expects[3] | "stderr does not contain 'failing-post-read.sh'" — hook's stderr captured but not propagated to eval transcript |
| Ledger emission wired, hook exit propagated | eval FAIL on expects[4] | "exit_code != 0" — failing hook's exit code propagated up to eval process (fail-open contract violation, the dominant regression class) |

The expects[] ordering is deliberate: expects[0..2] surface the
strongest scaffolding gap (missing ledger) first; expects[3..4]
discriminate the subtler regressions (swallowed stderr vs.
propagated exit code).

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E13` |
| Depends on | T04.01 / T04.02 (Expect.file impl) | satisfied by current `expect.py:187-268` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Depends on | T04.??  (Expect.stderr impl) | satisfied by current `expect.py:556-569` |
| Sibling | T05.07..T05.17 (E3..E12 bodies) | E13 is the tenth post-OQ-2 hook-coverage body; shares `category: hook-lifecycle`, `requires: []`, `timeout_sec: 60`, `/quit` exit pattern |
| Differs from | T05.07..T05.17 (E3..E12 bodies) | E13's surface is the harness's error-handling path (cross-cutting), not a single hook script or the install_hooks adapter; reads `logs/hook-errors.jsonl`, not `logs/freshness.jsonl` or `settings.json`; requires a hooks.json variant + a failing fixture (deferred — see §8.1) |
| Unblocks | T05.20 (E14 author) | downstream peer authoring continues |
| Unblocks | follow-up "failing fixture + hooks.json variant + structured ledger" tasks | gated on the four sub-deferrals in §3 / §8.1 |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
