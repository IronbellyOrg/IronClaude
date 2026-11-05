# Launcher follow-up: export the three alias variables in ccsession tier mode (issue #384)

This is the exact spec of the separate launcher pull request for issue #384 (owner decision of 2026-11-05, option A).
**The edit must not start before the #315 pull request is merged.** The coordinator tells the worker when it has merged; until then nothing under `src/superclaude/skills/ccsession-tag/` may change.
All line numbers below are at this branch's base commit `38eb3c58afe6988b51060ae14117172869ea4c1e` and must be re-verified after #315 merges.

## File to edit

`src/superclaude/skills/ccsession-tag/ccsession` (the shell launcher). No other file under `src/superclaude/skills/ccsession-tag/` changes. `ccsession-orca` stays untouched.

## Anchor (re-verify after #315 merges)

The tier-mode block, lines 776-785. Line 777 also tests that `CCSESSION_EXT_PROFILE` is not 1:

```bash
TIER_MODE=0
if [ "$CCSESSION_EXT_PROFILE" != 1 ] && python3 "$CCSESSION_MODELS" tier-mode 2>/dev/null; then
  TIER_MODE=1
fi
if [ "$TIER_MODE" = 1 ]; then
  if [ -n "$PROFILE" ]; then
    echo "ccsession: --profile is not used in this workspace; choose --tier <tier> or --model <name> (see ccsession --help)" >&2
    exit 2
  fi
  USE_SHIM=1
```

The custom-option exports, lines 1099-1103 (shown for contrast: `PROFILE_MODEL` is a shell variable, not an export, so nothing here exports the model):

```bash
  if [ "$PROFILE_CUSTOM_OPTION" = 1 ]; then
    export ANTHROPIC_CUSTOM_MODEL_OPTION="$PROFILE_MODEL"
    export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="$PROFILE_MODEL"
    export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="$PROFILE context profile"
  fi
```

## The edit

Add exactly these three lines inside the `if [ "$TIER_MODE" = 1 ]; then` branch, right after `USE_SHIM=1` (line 785 at the base commit), with the same indentation as that line:

```bash
  export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
  export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
  export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
```

They run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched (the `elif` branches below the block do not export them).

Tier-mode detection rule, from `src/superclaude/skills/ccsession-tag/models.py` (`tier_mode`, lines 469-479 at the base commit): tier mode is on when a `T<N>_WINDOW` variable exists in the tier environment and `CCSESSION_TIERS` is not `0`; the launcher adds its own check that `CCSESSION_EXT_PROFILE` is not 1 (line 777).

## Before the pull request is opened

- Probe `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` the way `.dev/issues/384/analysis/probe-alias-remap.md` probed the other two variables (throwaway HOME and config directory under /tmp, removed afterwards). The #384 probe covered only the opus and haiku variables.
- Re-verify the line numbers above and the tier-mode rule against the merged #315 code.
- After the edit, change the status paragraph of `docs/reference/model-aliases.md` ("Status on 2026-11-05 ...") and the "once the launcher sets" wording of the pages that point to it, so they say the launcher now sets the variables.

## Harness addition for `tests/unit/test_ccsession_tiers.py`

The fake claude of `_launch_env` records a fixed set of keys (lines 330-341 at the base commit). Add these three lines to its `json.dump` call, after the `"auth_token"` line:

```python
    "opus_model": os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", ""),
    "sonnet_model": os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL", ""),
    "haiku_model": os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", ""),
```

The tests below remove the three variables from the launch environment first, because the harness copies `os.environ` (line 359) and the workspace exports them.

## Failing-first test

Append to `tests/unit/test_ccsession_tiers.py` (it uses only `_launch`, `pytest` and `Path`; the autouse fixture `_isolated` already removes tier variables):

```python
ALIAS_VARIABLES = (
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
)


def test_tier_launch_exports_the_alias_variables(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The harness copies os.environ and the workspace exports these three
    # variables, so remove them first: only the launcher may set them here.
    for name in ALIAS_VARIABLES:
        monkeypatch.delenv(name, raising=False)
    rc, out, err, seen = _launch(tmp_path, "work")
    assert rc == 0, err
    assert (seen["opus_model"], seen["sonnet_model"], seen["haiku_model"]) == (
        "claude-gw-tier1a",
        "claude-gw-tier1b",
        "claude-gw-tier2",
    )


def test_non_tier_launch_leaves_the_alias_variables_unset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ALIAS_VARIABLES:
        monkeypatch.delenv(name, raising=False)
    rc, out, err, seen = _launch(tmp_path, "work", defaults=None)
    assert rc == 0, err
    assert (seen["opus_model"], seen["sonnet_model"], seen["haiku_model"]) == ("", "", "")
```

Helper names used in the test code block, checked by grep in `tests/unit/test_ccsession_tiers.py` on 2026-11-05:

```text
_launch: 301:def _launch(
_launch_env: 322:def _launch_env(
_defaults: 128:def _defaults(tmp_path: Path, text: str = TIER_BLOCK) -> Path:
_isolated: 102:def _isolated(monkeypatch, tmp_path_factory):
TIER_BLOCK: 36:TIER_BLOCK = """\
SKILL_DIR: 31:SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "ccsession-tag"
26:from pathlib import Path
28:import pytest
```

## Result of running it against the unchanged launcher

A scratch copy of the harness with the addition above, in `.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t9-scratch/test_alias_exports_scratch.py`, was run with `uv run pytest`; the output is `.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t9-red.log`.
`test_tier_launch_exports_the_alias_variables` fails with an AssertionError (the three values are `''`, `''`, `''` instead of the tier ids), and `test_non_tier_launch_leaves_the_alias_variables_unset` passes.
After the edit above, both must pass.
