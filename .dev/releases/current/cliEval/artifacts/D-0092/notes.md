# D-0092 — Notes / Design Rationale

## Why a Write seed precedes the serena call

`mcp__serena__replace_content` requires a pre-existing file with the
`old_string` substring; without a seed file the serena call would
either error or never fire. E6 (D-0090) faced the same constraint
for the Edit branch and resolved it with a Write→Edit chain. E8
follows the same pattern: Write `modified.txt` with `'before'`,
then serena `replace_content('before' → 'after')`.

The seed Write fires the PreToolUse hook on the Write matcher
branch — emitting a row with `"matcher":"Write"`. The serena call
fires the PreToolUse hook a second time on the `mcp__serena__*`
matcher branch — emitting a row with
`"matcher":"mcp__serena__replace_content"`. Both rows coexist in
`logs/freshness.jsonl`; the E8 assertion uses `Expect.file.contains`
which only requires the serena substring to appear, so the Write
co-fire is harmless.

E7 already pins the Write branch independently (D-0091), so no
coverage is gained by isolating E8's input to a serena-only call.

## Why `replace_content` (not `replace_regex` / `insert_*`)

Per D-0082 §4 row E8: "or other `mcp__serena__*` variant in the
matcher". `replace_content` is the closest semantic sibling to
E6's Edit operation (both modify an existing file's contents in
place), which keeps the matcher-coverage trio symmetric:

- **E6 Edit branch** → Edit replaces a substring in an existing file.
- **E7 Write branch** → Write creates a new file.
- **E8 serena branch** → `replace_content` replaces a substring in
  an existing file.

A reviewer comparing the trio sees the same operation surface
across all three branches, with the matcher pin being the only
discriminator. `replace_regex` would also work but introduces
regex syntax into the prompt and the asserted substring; the
plain string form is simpler.

## Why `requires: [mcp_server.serena]` (not a YAML callback)

The OQ-2 freeze (D-0082 §4 row E8 + §6 capability-tag rollup)
explicitly names `mcp_server.serena` as the capability tag and
specifies "soft-skip under `--no-mcp` or if serena unreachable".
This is exactly what FR-CAP1's `requires:` clause provides — no
callback escape hatch is needed.

Adding `mcp_server.serena` to the manifest's `optional_capabilities`
block enables the declarative skip path. The capability is not yet
in the static `_DEFAULT_CAPABILITY_SPECS` roster
(`capabilities.py:184-214`); with the default
`PermissiveCapabilityResolver` the `requires` clause resolves
trivially. A stricter resolver upgrade is a future capabilities
task — it does not block T05.13.

## Telemetry gap inheritance

The `freshness-pre-edit.sh` script telemetry gap discovered during
T05.10 (E6) and T05.11 (E7) applies identically to E8: the script
emits to `freshness-hook.jsonl` with `event`/`tool` field names,
not to `freshness.jsonl` with `type`/`matcher` field names. The
OQ-2-frozen body lands verbatim — the script update is a
single-script change that unblocks all three siblings at once.

This is the established T05.07..T05.11 posture: land the OQ-2
body verbatim; let the hook-script update task close the gap
across all evals that share the script.

## Sibling-trio symmetry

The three PreToolUse matcher-coverage evals share:

- Hook script: `freshness-pre-edit.sh`.
- Asserted ledger: `logs/freshness.jsonl`.
- First substring: `"type":"pre_edit"`.
- Last assertion: `exit_code.equals(0)`.
- Per-eval HOME isolation: `ephemeral`.
- PTY exclusion: `no_pty: skip`.

Differences:

| Field | E6 (Edit) | E7 (Write) | E8 (serena) |
|---|---|---|---|
| `requires` | `[]` | `[]` | `[mcp_server.serena]` |
| Matcher substring | `"matcher":"Edit"` | `"matcher":"Write"` | `"matcher":"mcp__serena__replace_content"` |
| Scratch file | `edited.txt` | `written.txt` | `modified.txt` |
| Inputs | Write seed → Edit → /quit | Write → /quit | Write seed → serena → /quit |

The matrix is intentional — it gives a future reviewer a clean
comparison to spot regressions in matcher routing or capability
gating.
