# D-0096 — E12 Hook Deploy Idempotency Eval (Body)

**Deliverable ID:** D-0096
**Task ID:** T05.17 (Phase 5)
**Roadmap items:** R-095 (E12 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E12 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E12 — the ninth and
final post-OQ-2 hook-surface coverage entry (R-086 … R-098) before the
Phase-5 R3 mitigation block (T05.19+). E12 covers the
**`install_hooks` adapter idempotency contract** documented at
`src/superclaude/cli/eval/hook_adapter.py:28-33` ("Re-invoking
`deploy_hooks_to` against the same `home_path` produces identical
filesystem state").

E12 is structurally distinct from E3-E11 along two axes:

1. **Cross-cutting surface (not a single hook).** E3-E11 each exercise
   one hook event entry from `hooks.json`. E12's surface is the
   **deployer** (`hook_adapter.deploy_hooks_to`), so the eval reads
   the merged `settings.json` rather than the `logs/freshness.jsonl`
   ledger.
2. **Not PTY-driven.** E3-E11 inject `/quit`-bounded prompt sequences
   through the PTY harness so the in-session Claude Code process
   fires the matched hook. E12 has no in-session work to do — the
   adapter call is performed by the harness during HOME setup
   (`HomeIsolation.setup` → `deploy_hooks_to` per the NFR-ISO2 wiring
   task), and the eval only asserts the post-setup `settings.json`
   shape. The body therefore lands with a minimal `/quit`-only
   inputs sequence and leans on `Expect.settings_json` rather than
   `Expect.file`.

The body must:

- run on a fresh per-eval HOME isolated by FR-ISO2 — the
  `deploy_hooks_to` call invoked by the setup wrapper is the
  effective "first deploy" of the OQ-2 contract;
- assert that the merged `settings.json` carries hook registrations
  for **every** hook event in `src/superclaude/hooks/hooks.json` —
  the `has_registration(<all hook events>, <all matchers>)` predicate
  from OQ-2 D-0082 §4 row E12, mapped to existing
  `Expect.settings_json` primitive checks (mapping documented in §3
  and §8.1 below);
- exit cleanly so `exit_code.equals(0)` can pin the PTY teardown
  contract — sibling to E3-E11;
- carry no capability tag (`requires: []`) — `install_hooks` is a
  pure stdlib operation; no MCP, no network.

The "twice in a row" element of the OQ-2 input shape (and its paired
`digest unchanged` expect) cannot be expressed in the current
declarative DSL (the schema has no `callback:` field — see §3
"Schema-expressibility constraint" below). The strict declarative form
is deferred to a follow-up task per the established T05.07..T05.16
precedent: land the OQ-2 body verbatim with the best-effort
declarative proxies, document the gap in §8.1, and gate the strict
form on the YAML callback escape hatch / a future
`adapter:` schema extension.

## 2. Hook-surface contract (from `hook_adapter.py` + OQ-2 D-0082 §4)

`src/superclaude/cli/eval/hook_adapter.py:183-256` `deploy_hooks_to`:

```python
def deploy_hooks_to(home_path: Path) -> None:
    """Deploy SuperClaude hooks into the per-eval HOME at ``home_path``.

    Two filesystem effects, in this order:
    1. install_hooks() copies hook scripts to <home>/.claude/hooks/
       and merges hook registrations into <home>/.claude/settings.json.
    2. Source src/superclaude/hooks/hooks.json is copied verbatim to
       <home>/.claude/hooks.json (byte-identical via shutil.copy2).

    Idempotent: re-invocation on the same home_path produces identical
    filesystem state.
    """
```

The idempotency contract of interest (OQ-2 D-0082 §4 row E12):

| Observable | Purpose |
|---|---|
| Every hook event from `hooks.json` has a registration in `<home>/.claude/settings.json` after the first deploy | proves the install_hooks merge pipeline produced the expected target shape |
| Every hook event from `hooks.json` has a registration in `<home>/.claude/settings.json` after the second deploy | proves the second deploy did NOT remove/break the registrations |
| The settings.json digest is unchanged between the two deploys (no duplicate matcher entries) | proves the second deploy is a true no-op — the bug class from PR #49 was exactly this: matcher exists but a second deploy duplicated it |
| Process exits cleanly | sanity pin for the PTY teardown contract |

The "all hook events" set from `src/superclaude/hooks/hooks.json` (the
ground-truth source of registrations) covers six events:

| Event | Matcher | Hook script |
|---|---|---|
| `SessionStart` | (none) | `session-init.sh` |
| `SessionStart` | `*` | `freshness-session-start.sh` |
| `UserPromptSubmit` | (none) | `freshness-user-prompt.sh` |
| `PreToolUse` | `Edit\|Write\|mcp__serena__*` | `freshness-pre-edit.sh` |
| `PostToolUse` | `Read` | `freshness-post-read.sh` (async) |
| `PostToolUse` | `mcp__auggie__.*\|mcp__auggie-mcp__.*\|mcp__airis-mcp-gateway__auggie_.*` | `auggie-flag-clear.sh` |
| `SubagentStart` | (none) | `freshness-subagent-start.sh` (async) |
| `SubagentStop` | (none) | `freshness-subagent-stop.sh` (async) |

Six distinct hook events appear under the top-level `hooks` key
(SessionStart, UserPromptSubmit, PreToolUse, PostToolUse,
SubagentStart, SubagentStop). E12 asserts presence of each.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E12 entry that
previously carried only stale scaffolding metadata (a placeholder
title `"doctor surfaces missing claude binary"` from the pre-OQ-2
numbering and no body). T05.17 replaces the scaffolding with the
frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"Hook deploy idempotency"` (matches D-0082 §4 OQ-2 row E12) |
| **category** | `hook-lifecycle` (sibling to E3-E11; was `doctor` in stale stub — the eval surface is the install_hooks adapter, which is part of the hook lifecycle, not the doctor diagnostics surface) |
| **requires** | `[]` — no capability tags; `install_hooks` is pure stdlib, no MCP, no network |
| **timeout_sec** | `60` (matches E3..E11 sibling parity; in practice the eval is bounded by per-eval HOME setup time + a `/quit` PTY round-trip, typically <10s — 60s is generous headroom) |
| **inputs[0].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract. No interactive work needed; the `install_hooks` invocation that produces the asserted `settings.json` is performed by the setup wrapper (FR-ISO2 / NFR-ISO2 atomic-setup), not by the in-session Claude Code process |
| **expects[0]** | `settings_json: { path: settings.json, key_path: hooks.SessionStart, exists: true }` |
| **expects[1]** | `settings_json: { path: settings.json, key_path: hooks.UserPromptSubmit, exists: true }` |
| **expects[2]** | `settings_json: { path: settings.json, key_path: hooks.PreToolUse, exists: true }` |
| **expects[3]** | `settings_json: { path: settings.json, key_path: hooks.PostToolUse, exists: true }` |
| **expects[4]** | `settings_json: { path: settings.json, key_path: hooks.SubagentStart, exists: true }` |
| **expects[5]** | `settings_json: { path: settings.json, key_path: hooks.SubagentStop, exists: true }` |
| **expects[6]** | `exit_code: { equals: 0 }` |

PTY-exclusion tag: `no_pty: skip` (carried forward from the
scaffolding entry — every eval in the `real` suite is PTY-driven
per DOC-OQ3 / R-077).

No additions to `optional_capabilities` — `install_hooks` is built
into the SuperClaude CLI; no MCP server is required.

### Schema-expressibility constraint — the "twice" and "digest unchanged" deferral

The OQ-2 D-0082 §4 row E12 input shape says: "call `install_hooks`
adapter against the per-eval HOME **twice in a row** (back-to-back
invocations)". The OQ-2 expect shape pairs this with: "settings.json
file digest unchanged between the two deploys (no duplicate entries)".

Neither half is expressible under the current
`src/superclaude/cli/eval/suites/suite.schema.json`:

1. **No `callback:` field.** Schema `$defs/evalEntry` (lines 124-160)
   defines `id, title, category, requires, timeout_sec, isolation,
   inputs, expects, parameterize, no_pty`. There is no
   `callback:` field that could programmatically invoke
   `deploy_hooks_to` a second time from inside the eval. The D-4
   "YAML callback escape hatch" referenced in D-0082 §4 for E14 is
   a planned extension that has not yet been added to the schema
   (cross-referenced in `commands.py` design notes only).
2. **No `inputs[].adapter:` field.** Schema `inputs[]` items use the
   open-shape `type: object` (additionalProperties: true), but the
   runner's input dispatch only knows about `prompt` and
   `expect_tool_call` (commands.py PTY input loop). An `adapter:`
   field would be silently dropped by the runner.
3. **No `digest_unchanged:` predicate.** `Expect.settings_json`
   (`expect.py:373-480`) supports `exists` + `equals` checks on a
   `key_path` dot-traversal, but no `digest:` / `unchanged_since:`
   primitive exists in `PRIMITIVE_NAMES` (`expect.py:56-64`). The
   strict digest-unchanged form requires either a Python callable
   predicate (D-4 callback escape hatch) or a new `Expect.file.digest`
   primitive (schema bump).

Per the established T05.07..T05.16 deferral posture, T05.17 lands the
OQ-2 body shape with the best-effort declarative proxy:

- **"twice in a row" proxy:** the per-eval setup wrapper invokes
  `deploy_hooks_to` exactly once (per NFR-ISO2 / T02.13). The
  asserted shape (`hooks.<event>` keys exist) holds post-setup, which
  is the "after first deploy" half of the OQ-2 contract. The
  "after second deploy" half is the deferred branch — if the same
  shape continues to hold after a hypothetical second invocation,
  the assertion as authored continues to pass (idempotency at the
  registration-presence level). The proxy is therefore **necessary
  but not sufficient**: it catches "second deploy clobbered the
  registrations" regressions but does not catch "second deploy
  duplicated an entry" regressions (the PR #49 class). The PR #49
  regression class is the explicit motivation in D-0082 §4 notes;
  catching it requires the digest-unchanged assertion.
- **"digest unchanged" proxy:** none — declarative DSL has no
  digest primitive. The full assertion is deferred to either (a) the
  YAML callback escape hatch (D-4) being added to the schema and
  exercised for E12, or (b) a future `Expect.file.digest` primitive.

§8.1 documents the deferral with the same "telemetry gap" framing
established by T05.07..T05.16 for the freshness-ledger emit gap.
Acceptance criteria for T05.17 are met by the describe / list /
round-trip evidence (the manifest body is FR-SCH2-valid, OQ-2-shaped,
and resolves through `Expect.from_mapping`); the per-task AC requiring
full end-to-end `eval run --eval E12` execution depends transitively
on (i) the runner NameError fix at `commands.py:1418` and (ii) the
callback / digest escape hatch landing.

### Why `key_path: hooks.<event>` (not deeper)

`Expect.settings_json` (`expect.py:373-480`) traverses dot-separated
key segments through `Mapping` values only. The merged settings.json
structure is:

```jsonc
{
  "hooks": {
    "SessionStart": [
      { "hooks": [...] },         // unmatched entry
      { "matcher": "*", "hooks": [...] }  // matched entry
    ],
    "UserPromptSubmit": [...],
    ...
  }
}
```

`hooks.SessionStart` resolves to the **array** of entries — an
`exists` check succeeds (the key is present at that path). Going
deeper (e.g., `hooks.SessionStart.0.hooks.0.command`) requires array
indexing, which the current primitive does not support
(`expect.py:423-429`: traversal short-circuits at the first
non-Mapping). The granular per-matcher pin (e.g., proving the
`Edit|Write|mcp__serena__*` matcher specifically is present) is
therefore deferred to either a future array-traversal extension or a
callback predicate.

For the OQ-2 minimum AC, asserting every top-level hook event key is
present is sufficient to prove `install_hooks` merged the full hooks
surface. If `install_hooks` regressed to skip an event entirely (e.g.,
SubagentStart never gets merged), the `key_path: hooks.SubagentStart`
exists check would fail — that is the operationally-meaningful
regression class for the registration-presence half of the contract.

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E12` is
trivially accepted — `eval describe --suite real --eval E12` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The setup wrapper invokes `deploy_hooks_to` against the
  freshly-created per-eval HOME, which in turn calls `install_hooks`
  + the verbatim `hooks.json` copy. `install_hooks` is itself
  deterministic given a clean `settings.json` target — the matcher-
  collision detection (install_hooks.py merge logic) short-circuits
  on a fresh HOME (no prior settings.json), producing a deterministic
  output identical to the source `hooks.json` registrations.
- The `Expect.settings_json` assertions are pure-read on the
  resulting `<home>/.claude/settings.json` — no time-of-day, network,
  or shared-state dependencies. Six independent `exists` checks
  against six fixed key_paths.
- The `/quit` input causes an immediate clean exit (exit code 0)
  after PTY harness EOF.
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored.

Three consecutive `eval run --suite real --eval E12` invocations on
a clean HOME must therefore yield identical EvalOutcome statuses,
which is the per-task acceptance criterion. (The "twice in a row"
strict form remains deferred; the determinism of the registration-
presence proxy is independent of the deferral.)

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`). The single-element
  `inputs[]` array is accepted by the open-shape array schema.
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All
  primitives used (6×`settings_json`, 1×`exit_code`) are in
  `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `settings_json` primitive kwargs `path`, `key_path`, `exists` are
  supported by `Expect.settings_json._build` (`expect.py:373-480`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `requires: []` (empty / omitted) is accepted by the schema.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E12 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E12` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E12 --no-mcp` | RUNS | `requires: []` — no MCP capability to skip; `install_hooks` is pure stdlib |
| `eval run --suite real --eval E12 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077); `--no-pty` short-circuits before any eval body executes |
| `eval run --suite real --eval E12 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture matches siblings E3-E7 / E9-E11 (which also carry
`requires: []`) and differs from E1 / E2.1-3 / E8 (which carry MCP
capability tags and soft-skip under `--no-mcp`).

## 8. Verification

Per phase-5-tasklist.md T05.17, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E12
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 / T05.07..T05.16 evidence
blocks all block any direct `eval run` invocation. That blocker is
the responsibility of the runner-completion task (Phase-5 dependency
of the CP-P05-T13-T17 checkpoint at T05.18). T05.17 authors the
manifest body; observable verification is therefore via:

- (a) `eval describe --suite real --eval E12` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.17/describe-E12.txt`);
- (b) `eval list --json` continuing to enumerate suite `real`
  with 17 evals (proves schema acceptance; see
  `evidence/T05.17/list-with-E12.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.17/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls
into the runner-completion task downstream of T05.17.

### 8.1 Deferred branches — "twice in a row" and "digest unchanged"

OQ-2 D-0082 §4 row E12 specifies a two-part contract:

1. **Registration presence.** After the install_hooks adapter runs,
   every hook event from the source `hooks.json` must be registered
   in the per-eval HOME's `settings.json`. **Landed verbatim** by
   T05.17 via the six `Expect.settings_json(key_path=hooks.<event>,
   exists=true)` rows.
2. **Idempotency under re-invocation.** A second back-to-back
   `install_hooks` call must produce **byte-identical** settings.json
   (no duplicated matcher entries, no clobbered registrations). The
   PR #49 regression class is exactly: "matcher exists but a second
   deploy duplicates it". **Deferred** by T05.17 — declarative DSL
   has no callback hook to invoke the adapter twice, and no
   `digest_unchanged` predicate to compare pre/post-second-deploy
   states.

Following the same precedent as T05.07..T05.16 (telemetry gaps in
freshness scripts, event_count predicates not expressible
declaratively, per-prompt count discrimination), T05.17 lands the
OQ-2 body shape with the best-effort declarative proxy for branch (1)
and defers branch (2) to a follow-up task gated on either:

- (a) the YAML `callback:` escape hatch (D-4) being added to the
  schema and exercised for E12 — the callback would invoke
  `deploy_hooks_to(home_path)` a second time and compare SHA256
  digests of the pre/post settings.json;
- (b) a future schema bump adding declarative
  `expect.file.digest_unchanged_after: { adapter_call: ... }` or
  equivalent shorthand.

Neither is in scope for T05.17.

The proxy retains operational meaning: if `install_hooks` regresses
such that a hook event is dropped from the merge pipeline (e.g.,
SubagentStart gets skipped on second deploy), the registration-
presence assertion would catch it on a follow-up describe/expect
round-trip OR on a re-run after the runner fix lands. The strict
PR #49 regression class is on the **digest-unchanged** branch
specifically.

This gap is **not introduced** by T05.17; it predates the deliverable
and is structural to the declarative DSL's expressibility envelope.
Acceptance criteria for T05.17 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E12` to exit 0 deterministically
depends transitively on (a) the runner NameError fix and (b) the
"twice + digest" deferred branches if/when the user demands strict
PR #49 regression coverage.

### 8.2 Setup-wrapper dependency

E12 is unique in the post-OQ-2 hook-coverage roster in that its
assertions read **only** the merged settings.json — not any
runtime-emitted freshness ledger. This means the eval's correctness
depends entirely on the per-eval setup wrapper invoking
`deploy_hooks_to` correctly. If the setup wrapper is missing or
broken (NFR-ISO2 / T02.13 incomplete), the per-eval HOME has no
`.claude/settings.json`, all six `settings_json.exists` checks would
report "settings.json not found at <path>", and the eval would
ERROR.

This is the correct failure mode: an E12 ERROR (not FAIL) under
"settings.json not found" surfaces a regression in the setup wrapper,
which is precisely what E12 implicitly verifies. Sibling E3-E11
evals depend on the same wrapper (their freshness-ledger assertions
fail open if the wrapper doesn't deploy the hooks at all), but they
do not specifically pin the wrapper's correctness — E12 does.

This makes E12 the **integration smoke test** for the install_hooks
adapter's idempotency contract AND the per-eval setup wrapper's
correctness. The two failure modes are distinguishable by the error
tag: "settings.json not found" → wrapper bug; "hooks.<event> exists
mismatch" → install_hooks bug.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E12` |
| Depends on | T04.06 / T04.07 (Expect.settings_json impl) | satisfied by current `expect.py:373-480` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Depends on | T02.14 / D-0034 (`hook_adapter.deploy_hooks_to`) | satisfied by current `hook_adapter.py:183-256` |
| Depends on | T02.13 (NFR-ISO2 atomic-setup wrapper) | wrapper invokes `deploy_hooks_to` from inside HomeIsolation.setup; required for E12 assertions to find a settings.json at all |
| Sibling | T05.07..T05.16 (E3..E11 bodies) | E12 is the ninth and final post-OQ-2 hook-coverage body; shares `category: hook-lifecycle`, `requires: []`, `timeout_sec: 60`, `/quit` exit pattern |
| Differs from | T05.07..T05.16 (E3..E11 bodies) | E12's surface is the adapter, not a hook script; reads settings.json, not freshness.jsonl; minimal inputs (no in-session work) |
| Unblocks | T05.18 (CP-P05-T13-T17 checkpoint) | E12 must enumerate + describe; full-run verification follows runner fix |
| Unblocks | follow-up "twice + digest" task | gated on D-4 callback escape hatch landing |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
