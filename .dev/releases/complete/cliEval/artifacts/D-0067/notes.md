# D-0067 — Implementation notes

## Why this task was test-only

T04.01 (D-0064) shipped the full `Expect.settings_json` body alongside
the package skeleton. The primitive already supported:

* `path` resolution against `ctx.home_path` (T02.11).
* Dot-separated `key_path` traversal with non-mapping short-circuit.
* `exists` and sentinel-aware `equals` arguments.
* Failure payloads with `expected`/`actual` (DM-005).
* Malformed-JSON branch with a `JSONDecodeError` traceback.

T04.04's deliverable is the **per-primitive acceptance harness** that
touches every named argument and the path-resolution invariant. No body
changes were required to `src/superclaude/cli/eval/expect.py`.

## Decisions

1. **Sentinel-aware `equals` default is the right call.** The temptation
   to default `equals=None` makes `Expect.settings_json(path=..., key_path="x")`
   ambiguous: is "no argument" or "value should equal JSON null" intended?
   The module-level `_SENTINEL` cleanly separates the two cases, and
   `test_equals_distinguishes_null_from_unset` pins it.
2. **Non-mapping intermediate yields `found=False`, not an exception.**
   Manifests can drift from real settings shapes (e.g. a refactor turns
   a sub-dict into a string). The primitive treats this as "key path
   does not resolve" rather than raising `TypeError`, which lets
   `exists=False` assertions stay green. `test_key_path_into_non_mapping_value`
   pins it.
3. **No path traversal sanitization.** The primitive trusts
   `HomeIsolation` (NFR-ISO1) to keep `home_path` rooted under the
   allowlist (T01.19). The hard-guard against real `~/.claude` lives
   one layer up; the primitive intentionally does not double-check.
4. **JSON parse errors carry the traceback.** Most Reporter consumers
   will only render `failure.message`, but the traceback survives in
   the eval JSONL log (T03.05) for triage. The
   `test_invalid_json_payload_fails` test asserts the traceback contains
   `JSONDecodeError` so we catch any future change that swallows it.

## Path resolution check (HomeIsolation isolation)

`test_resolution_isolated_from_real_home` confirms that a relative
`settings.json` path resolves under `home.home_path`, not the host's
real `~/.claude`. The body asserts:

* `result.passed` against a scratch-only marker (`scratch_only_marker`)
  that no real `~/.claude` would contain.
* `result.details["path"].startswith(str(home.home_path))` — the
  resolved absolute path is rooted under the scratch HOME.

This is the NFR-ISO1 contract translated to an `Expect.*` invariant: the
primitive cannot accidentally peek at the real host configuration.

## Things explicitly not covered here

* `key_path` containing literal dots in a key name — the dot is always
  a separator. Manifest authors who need keys with dots must use a
  different traversal helper; that has not been required by any eval in
  the M5 inventory.
* Empty `key_path` — passes the empty-string split through `split(".")`
  which yields `[""]`, so traversal short-circuits on the first segment.
  Not exercised here; not a real manifest pattern.
* `equals` against complex objects (sets, tuples, custom classes) — JSON
  decoding only ever produces dict/list/str/int/float/bool/None, so the
  argument space is closed.

## Follow-ups

None. Two adjacent tasks consume this primitive:

* T04.14 (FR-G5 coverage gate CLI) — uses `Expect.settings_json` shape
  knowledge internally, but invokes `settings_json` reading directly via
  `json.load`. No coupling required.
* T05.10 (E9 matcher-coverage eval) — wires `Expect.settings_json`
  directly into the manifest's `expects:` block.

Both pass without any further changes to `Expect.settings_json`.
