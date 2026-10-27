# D-0096 — Notes / Design Rationale

## Why E12's surface is the adapter, not a hook

E3-E11 each pin one row of `src/superclaude/hooks/hooks.json` —
the eval drives Claude Code through the PTY, fires the matched
hook, and reads the freshness ledger to prove the hook script
emitted its event. E12 is structurally different: its surface is
the **deployer** (`hook_adapter.deploy_hooks_to`), which is the
machinery that puts those hooks on disk in the first place. The
regression class motivating E12 (per D-0082 §4 notes, PR #49) is:
"matcher exists but a second deploy duplicates it" — a bug in the
install_hooks merge pipeline, not in any individual hook script.

The natural body shape for this surface is: invoke the adapter
twice, snapshot the resulting settings.json after each invocation,
and assert the two snapshots are byte-identical. That's the OQ-2
contract verbatim.

Two of those three operations are not expressible declaratively:

- "invoke the adapter" requires a Python callback hook the schema
  does not define;
- "snapshot two states and diff" requires either a `digest_unchanged`
  predicate or a callback that stages both calls.

What IS expressible declaratively is the **post-first-deploy
shape**: after the harness's setup wrapper runs the adapter once
(per NFR-ISO2 / T02.13), the per-eval HOME's settings.json should
carry registrations for every hook event in hooks.json. That's the
"first deploy" half of the OQ-2 contract, landed via six
`Expect.settings_json` exists checks (one per hook event key).

The "second deploy + digest unchanged" half is deferred per the
same posture taken in T05.07..T05.16 — land the OQ-2 body
verbatim with the declarative proxies, document the gap in §8.1,
defer the strict form to a follow-up task gated on the YAML
callback escape hatch / a future schema extension.

## Why settings.json key-path enumeration (not a single deep check)

`Expect.settings_json` (`expect.py:373-480`) traverses dot-separated
key segments through `Mapping` values only — it short-circuits at
the first array boundary (`expect.py:423-429`). The merged
settings.json has the shape:

```jsonc
{
  "hooks": {
    "SessionStart": [{ "hooks": [...] }, ...],     // array of entries
    "PreToolUse": [{ "matcher": "...", "hooks": [...] }, ...],
    ...
  }
}
```

`hooks.SessionStart` resolves to the array of entries (Mapping →
key → list); `hooks.SessionStart.0` would require array indexing
the primitive doesn't support. The deepest expressible check is
**top-level event presence**: `hooks.<event>` exists.

Six independent checks (one per hook event) collectively prove:

- the merged settings.json was written at all (FR-ISO2 / setup
  wrapper correctness);
- every hook event from the source `hooks.json` was merged in (no
  event silently dropped);
- the top-level `hooks` key is present and structured as a Mapping.

This is sufficient discrimination for the "first deploy is
correct" regression class. Finer granularity (per-matcher pin,
per-script command pin, per-timeout pin) requires array traversal
or a callback predicate — both deferred.

## Why `inputs: [{prompt: "/quit"}]` (not an empty inputs[])

E12 has no in-session work to do — the install_hooks invocation
that produces the asserted shape is performed by the setup wrapper
before the PTY session opens. Strictly speaking, the eval could
omit `inputs` entirely (the schema allows it) and let the PTY
harness sit idle.

In practice the PTY harness needs a clean exit path to satisfy
`exit_code.equals(0)`. Sibling E3-E11 all use `/quit` as the final
input for this reason; an empty inputs[] would cause the harness
to timeout-kill the session and yield a non-zero exit code. T05.17
inherits this pattern: a single-element `inputs: [{prompt: "/quit"}]`
gives the PTY a clean shutdown trigger without doing any
in-session work.

The `/quit` also serves a secondary purpose: it advertises to the
reader that "this eval intentionally doesn't drive Claude through
any tool calls" — the body's only behavioral contract is on the
post-setup settings.json shape. A reader skimming `inputs[]`
sees `/quit` immediately and understands the eval is a
post-setup assertion suite, not a hook-firing scenario.

## Why `category: hook-lifecycle` (not `installer` or `doctor`)

The stale E12 placeholder carried `category: doctor` (a leftover
from the pre-OQ-2 numbering when E12 was "doctor surfaces missing
claude binary"). The OQ-2 resolution reassigned E12 to the
`install_hooks` adapter, which prompts a category re-think:

- `installer` would be a reasonable choice (the surface is the
  installer), but no other eval in the suite uses this category
  and creating a singleton category creates noise in `eval list`
  filtering.
- `doctor` is wrong — E12 doesn't exercise any doctor surface.
- `hook-lifecycle` is the sibling category for E3-E11. E12 covers
  the deployer half of the hook lifecycle (how hooks get on disk);
  E3-E11 cover the firing half (how hooks emit events). The
  category groups them cleanly under one heading for filtering
  and reporting purposes.

T05.17 picks `hook-lifecycle` for sibling parity and to avoid a
singleton `installer` category. A future "installer" suite (if
one is created — TBD per roadmap) would re-shard these.

## Why `requires: []` (not `[mcp_server.*]`)

`install_hooks` is pure Python stdlib + filesystem ops (json,
shutil, os, pathlib). It does no network I/O, calls no MCP
servers, and depends on no external binaries beyond Python itself.
Per D-0082 §6 capability-tag rollup, E12's row lists no capability
tag.

The practical implication: E12 runs under `--no-mcp` (the
matcher-coverage gate counts it as a non-MCP eval), and the only
way E12 skips is via `--no-pty` (per-eval `no_pty: skip` tag).
Matches siblings E3-E7 / E9-E11.

## What this body does NOT assert (and why)

The OQ-2 body row E12 frames three explicit contracts:

1. **Registration presence (first deploy)** — landed verbatim via
   six `settings_json.exists` checks.
2. **Registration presence (second deploy)** — deferred (no
   callback to invoke the adapter twice).
3. **Digest unchanged (idempotency proof)** — deferred (no
   `digest_unchanged` predicate; no callback to stage two
   snapshots).

The PR #49 regression class is on contract (3) specifically — a
malformed merge that duplicates an existing matcher entry. The
landed body catches contracts (1) but NOT (3). If the user
demands strict PR #49 coverage before the deferred form lands, the
follow-up task should:

(a) prioritize the YAML callback escape hatch (D-4) for the
    schema; OR
(b) add a declarative `Expect.file.digest_unchanged_after:` /
    similar primitive backed by a Python implementation that can
    invoke the adapter (or any callable) between snapshots; AND
(c) update E12 to use the new escape hatch and add a third
    expects row pinning the digest.

The defer-to-follow-up posture is consistent with T05.07..T05.16
(which defer event_count predicates / per-prompt count
discrimination for similar reasons). The deferred branches are
documented in §8.1 of the spec; the proxy assertions in the
landed body are necessary-but-not-sufficient coverage of the OQ-2
contract.

## Setup-wrapper dependency note

E12 implicitly tests the setup wrapper's correctness. If the
wrapper fails to invoke `deploy_hooks_to`, the per-eval HOME has
no settings.json, all six `settings_json.exists` checks would
ERROR with "settings.json not found at <path>", and the eval
would surface a clear failure mode.

This is the correct behavior: an E12 ERROR under "settings.json
not found" surfaces a regression in the wrapper, which is
precisely what E12 verifies as part of the broader
install_hooks-adapter-correctness contract. Sibling E3-E11 evals
depend on the same wrapper but do not specifically pin its
correctness — E12 does.

The distinguishable failure modes:

- **wrapper bug** → "settings.json not found at <path>" → eval ERROR
- **install_hooks bug (event dropped)** → "key_path 'hooks.X' exists=False, expected True" → eval FAIL
- **install_hooks bug (PR #49 duplication)** → not detected by current proxies → see §8.1 deferral

## Inheritance from sibling deferral pattern

The deferral posture in §8.1 follows the same template established
by T05.07 (D-0087 §8.1), T05.08 (D-0088 §8.1), T05.09 (D-0089
§8.1), T05.10/T05.11/T05.13 (D-0090/D-0091/D-0092 §8.1), T05.14
(D-0093 §8.1), T05.15 (D-0094 §3 footnote), and T05.16 (D-0095
embedded in real.yaml E11 comment block):

| Task | Deferred construct | Reason |
|---|---|---|
| T05.07..T05.14 | freshness-ledger emit (script telemetry gap) | scripts write to bare integer counters, not OQ-2-contract JSONL |
| T05.15 | `jsonl.event_count(...) >= 1` | needs Python callable filter |
| T05.16 | `event_count(start) == event_count(stop)` symmetry | needs Python callable filter |
| **T05.17 (this)** | `install_hooks` second invocation + digest unchanged | needs YAML callback escape hatch + digest primitive |

Each deferral lands the OQ-2 body verbatim with the best-effort
declarative proxy, documents the gap explicitly, and gates the
strict form on a future schema/feature landing. T05.17 inherits
this pattern with the additional twist that the deferred branch
is the **dominant** regression class (PR #49 duplication is what
motivates E12 in the first place) — but the operational coverage
of the proxy (six registration-presence checks) is still
load-bearing for the wrapper-correctness + first-deploy
correctness contracts, and matches the precedent of landing the
body verbatim rather than blocking on a schema extension.
