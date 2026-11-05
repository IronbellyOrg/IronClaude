# Hypothesis: apply_settings_defaults fills `enabledPlugins.ponytail@ironclaude` with the default `true` and ignores an existing `"ponytail@ponytail": false`, so a renamed plugin loses the user's opt-out

**Agent**: root-cause-analyst (lens), run by troubleshoot-analyst
**Tier**: 1
**Timestamp**: 2026-11-04T15:37:04Z (parent receipt time; the worker's own value was model-generated and replaced)
**Cause class**: Logic regression (a plugin rename in 1de47e82 broke the opt-out because defaults are merged one key at a time)
**Claim class**: `runtime_behavior`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts (the fix carries out the doc card's restrictions; installation.md:458 and CHANGELOG.md:11 say nothing about the old key, so both need one added sentence)

## Claim

`apply_settings_defaults` merges `enabledPlugins` one key at a time. Its only guard is "this key is missing", and it fills a missing key with the shipped default. The rename to `ponytail@ironclaude` created a key that no existing user has, so a user whose settings hold `"ponytail@ponytail": false` gets `"ponytail@ironclaude": true` written at producer P1. `install_plugins` then selects every default plugin whose value is `True` and installs the pinned Ponytail the user had turned off.

## Evidence

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | `source_citation` | `src/superclaude/cli/install_user_setup.py:175-178` (producer **P1**; menu says :174, real statement at :177) | `for name, entry in value.items():` / `if name not in current:` / `current[name] = entry` / `added.append(...)`. The guard checks only the key's own name. |
| E2 | `source_citation` | `src/superclaude/cli/user_settings_defaults.json:36` | `"ponytail@ironclaude": true` is the value P1 copies in; `ponytail@ponytail` is not in the defaults (`tests/cli/test_install_user_setup.py:139`). |
| E3 | `source_citation` | `src/superclaude/cli/install_user_setup.py:297` | `wanted = [p for p in defaults.get("enabledPlugins", {}) if enabled.get(p) is True]`; the install commands at :341-345 then include it. |
| E4 | `executed_reproducer` | `tier1-observation.md` (parent-captured, failing arm, `timeout 120 uv run python /tmp/t14c-repro/repro.py`, settings `{"enabledPlugins": {"ponytail@ponytail": false}}`) | `ponytail entries after defaults: {'ponytail@ponytail': False, 'ponytail@ironclaude': True}` / `install_plugins would want ponytail@ironclaude: True` |

Producer citation: P1 (`surviving=yes`) is the only producer of the value. No exclusion claimed.

## Proposed Fix

Add a module constant mapping the new id to the old one, `_RENAMED_PLUGINS = {"ponytail@ironclaude": "ponytail@ponytail"}`. In the nested-fill branch, when `key == "enabledPlugins"`, the new name is missing and `current.get(_RENAMED_PLUGINS.get(name)) is False`, write `False` instead of the default. Only the new key is written; the old key is read, never edited or deleted. A new key the user already set is untouched (existing `if name not in current` guard). Only a literal `False` carries over: an old `true` keeps the documented "both enabled" migration (installation.md:393-398).

```python
if name not in current:
    if key == "enabledPlugins" and current.get(_RENAMED_PLUGINS.get(name)) is False:
        entry = False  # a user's opt-out under the plugin's old id carries over
    current[name] = entry
```

Files:
- `src/superclaude/cli/install_user_setup.py`: constant near `_NESTED_KEYS` (:41); two-line condition in the loop at :175-178.
- `tests/cli/test_install_user_setup.py`: new test below.
- `docs/getting-started/installation.md:458` and `CHANGELOG.md:11`: one sentence each that an existing `"ponytail@ponytail": false` carries over as `"ponytail@ironclaude": false`.

Test: new `test_settings_defaults_carry_old_ponytail_opt_out`: (1) `{"ponytail@ponytail": false}` → `ponytail@ironclaude is False`, old key unchanged, second run "already present"; (2) `{"ponytail@ponytail": false, "ponytail@ironclaude": true}` keeps `True`; (3) `{"ponytail@ponytail": true}` → `True`. Existing tests :145, :180, :73 must still pass.

## Confidence

Self-reported confidence: 0.92 (grounding 1.0, runtime check 1.0, symptom coverage 1.0, reproducibility 1.0, fix directness 1.0, domain coherence 0.5: the rename map is Ponytail-specific).

## Risks

- A workspace that already ran this unmerged branch has `ponytail@ironclaude: true` saved; the fix cannot tell it from a user's choice. Branch unmerged (PR #360), master users not exposed.
- The `added` message still lists `enabledPlugins.ponytail@ironclaude` without saying it was added as `false` (cosmetic).
- A future rename not added to `_RENAMED_PLUGINS` repeats the bug.

## If I'm wrong, it's probably because...

Another writer, or Claude Code itself, re-enables the plugin after `apply_settings_defaults`. E3 and E4 make that unlikely.

## Falsification standard

Wrong if, after the fix, `uv run pytest tests/cli/test_install_user_setup.py -k carry_old_ponytail -v` (seed `{"enabledPlugins": {"ponytail@ponytail": false}}`) fails to show `ponytail@ironclaude is False` with the :297 `wanted` expression excluding it.

## Evidence classification

- Claim class: `runtime_behavior`; Evidence class: `runtime_repro` (parent-captured, tier1-observation.md); runtime check performed by the parent (E4); verdict AFFIRM.

## Alternatives considered

- Skip in `install_plugins` when the old key is false: rejected, settings would still say `true`.
- Delete or rewrite `ponytail@ponytail`: rejected by the doc card (installation.md:398, CHANGELOG.md:14).

## Grounding gaps

- Fix and test not executed by the worker (no shell); the parent runs the falsification command.
- No behaviour-definition row needed (no third-party behaviour asserted).
