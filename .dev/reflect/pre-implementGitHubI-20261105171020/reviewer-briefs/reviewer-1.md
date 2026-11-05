## T1 card excerpt

Persona: analyzer (root cause and deviation lens). Your model class: sonnet. You are reviewing a PLAN before anyone builds it (pre-execution). Audit only what this brief supplies plus what you can Read, Grep and Glob. Run no commands and edit nothing.

What is under review
- Spec (the user's decision, one line): .dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/source.md
- Plan (9 tasks, 4 phases): .dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/TASK-WF-implementGitHubI-20261105-170815.md
- Background summary: .dev/issues/390/issue-summary.md

Tier 1 grounding findings (verbatim from t1-card.md)
- G1 (grounded): the default flag string is assigned once at `src/superclaude/skills/ccsession-tag/ccsession:124`; the six launch lines (`:1799`, `:1801`, `:1859`, `:1861`, `:1866`, `:1868`) all expand `$CC_CLAUDE_FLAGS` unquoted, so one change at line 124 reaches all six. The plan's Task 4 edits only line 124.
- G2 (grounded): `~/.claude/ccsession.env` is sourced at `ccsession:846-849`, after line 124, so the variable cannot be set from that file; the plan states this (Constraints, Tasks 5, 6, 7).
- G3 (grounded): the test helpers the plan names exist: `_label_launch` (`tests/unit/test_ccsession_tag.py:1158`), `ORCA_FLAGS` (`:1313`), `_orca_no_tty` (`:1470`) with `_assert_through_shim` (`:1486`), `test_every_launch_restores_grep_and_glob`; `_launch` and `_launch_env` exist in `tests/unit/test_ccsession_tiers.py:301,322`.
- G4 (grounded): `ccsession-orca` unsets only `CCSESSION_NAME` and `CCSESSION_ASK_TIMEOUT` before `exec ccsession --shim --claude-args`, so `CCSESSION_PERMISSIONS` passes through.
- R1 (risk): Task 4 validates the variable at line 124, before any argument parsing, so `ccsession --help`, `--list` and other non-launch commands also exit 2 on a bad value. The plan does not say whether that is intended.
- R2 (risk): the plan fixes `--allowedTools=Grep` as the only flag in opt-in mode (flagged in Constraints as a user decision).
- R3 (risk): Tasks 1 to 3 require red-run logs against the unchanged launcher; Task 4 depends on Tasks 1 to 3.
- R4 (risk): Task 3 relies on an existing `--tier` launch in the neighbouring tier tests; not re-Read in full.

Your job: find defects in the PLAN as written. Look for: a task that cannot achieve its acceptance criteria as worded (wrong helper, wrong file, wrong line, wrong behaviour of bash `case`/`:-` expansion, wrong test mechanics); an ordering or dependency mistake; something the plan changes that breaks existing tests or existing behaviour for unset users; a hidden launch path that still adds the bypass; a missing file the change must reach. Assume mistakes exist.

Classify every divergence you report between the plan and the spec using: Authorized expansion, Necessary deviation, Drift, Regression (a plan step that contradicts the spec or an existing guarantee). Report only what you can ground with a `file:line`.

Return, as your final message, a YAML document with: `verdict` (PASS or FAIL for "plan is safe to approve as written"), `self_confidence` (0.0 to 1.0), and `findings`, a list of items each with `id`, `claim`, `evidence` (file:line list), `class`, `severity` (blocking or minor), `plan_ref` (Task N or Constraints), `recommended_change`. Add `not_checked` listing what you could not verify.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T17:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/ic-issue-390 projectPath=/home/coder/workspaces/worktrees/IronClaude/ic-issue-390

### src/superclaude/skills/ccsession-tag/ccsession:109-125

```bash
# The wrapper always runs claude with --dangerously-skip-permissions and
# --allowedTools=Grep. On macOS, Linux, and WSL, Claude Code leaves the Grep and
# Glob tools out by default. Naming either one in --allowedTools when the
# session starts brings both back; a settings-file allow rule does not. Keep the
# = form: a bare --allowedTools takes the next arguments as tool names.
# Override by setting CC_CLAUDE_FLAGS in your shell env.
#
# Env vars (proxy URL, auth tokens) can be set in ~/.claude/ccsession.env.
# See ccsession.env.example in this skill's directory for the template.
# Shim knobs: CC_SHIM_SCRIPT (default: local-gateway-alias-proxy.py in this
# skill's directory), CC_SHIM_PORT (default 4010).

set -e

CLAUDE_BIN="${CLAUDE_BIN:-claude}"
CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:---dangerously-skip-permissions --allowedTools=Grep}"
# Extra Claude Code arguments for this launch (tier mode: per-model settings).
CC_SETTINGS_ARGS=()
```

### src/superclaude/skills/ccsession-tag/ccsession:844-850

```bash
# Source per-user env (proxy base URL, auth tokens, etc.) before launching
# claude. Keep this file out of version control — it holds secrets.
CCSESSION_ENV_FILE="${CCSESSION_ENV_FILE:-$HOME/.claude/ccsession.env}"
if [ "$CCSESSION_SKIP_ENV_FILE" != 1 ] && [ -f "$CCSESSION_ENV_FILE" ]; then
  # shellcheck disable=SC1090
  . "$CCSESSION_ENV_FILE"
fi
```

### src/superclaude/skills/ccsession-tag/ccsession:1796-1802

```bash
  echo "[ccsession] Starting untagged session"
  orca_terminal_title
  if [ -n "${PROFILE_MODEL:-}" ]; then
    exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --model "$PROFILE_MODEL" "$@"
  else
    exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} "$@"
  fi
```

### src/superclaude/skills/ccsession-tag/ccsession:1858-1869

```bash
  if [ -n "${PROFILE_MODEL:-}" ]; then
    exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --model "$PROFILE_MODEL" --name "$TOPIC" --resume "$SESSION_ID" "$@"
  else
    exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --name "$TOPIC" --resume "$SESSION_ID" "$@"
  fi
else
  echo "[ccsession] Starting new session labeled '$TOPIC'"
  if [ -n "${PROFILE_MODEL:-}" ]; then
    exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --model "$PROFILE_MODEL" --name "$TOPIC" "$@"
  else
    exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --name "$TOPIC" "$@"
  fi
fi
```

### tests/unit/test_ccsession_tag.py:1251-1256

```python
    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
    stdout, _ = _label_launch(tmp_path, transcript=transcript, args=args)
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[:2] == ["--dangerously-skip-permissions", "--allowedTools=Grep"]
    assert ("--model" in launched) == ("--profile" in args)
    assert ("--resume" in launched) == transcript
```

### tests/unit/test_ccsession_tag.py:1470-1489

```python
def _orca_no_tty(tmp_path: Path, *args: str, **extra: str) -> tuple[str, dict]:
    result = subprocess.run(
        [str(ORCA), *args],
        env=_orca_env(tmp_path, **extra),
        cwd=tmp_path / "work",
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=60,
        check=True,
    )
    return result.stdout + result.stderr, json.loads(
        (tmp_path / "record.json").read_text()
    )


def _assert_through_shim(record: dict) -> None:
    assert record["base_url"] == "http://127.0.0.1:4555"
    # One credential reaches Claude Code, never both.
    assert record["set"] == {"ANTHROPIC_API_KEY": False, "ANTHROPIC_AUTH_TOKEN": True}
```

## Coverage slice

| Requirement (source.md:1) | Plan task | Status | Grounding |
|---|---|---|---|
| INF-001 new opt-in variable CCSESSION_PERMISSIONS=default | Task 4 (switch), Tasks 5 to 9 (docs) | covered | ccsession:124 |
| INF-002 no bypass flag on all six launch lines, shim and tier routing kept | Task 4, Tasks 1 to 3 | covered | ccsession:1799-1868 |
| INF-003 unset is unchanged | Tasks 1 to 3 control runs, Task 4 diff limit | covered | tests/unit/test_ccsession_tag.py:1251-1256 |
| INF-004 empty CC_CLAUDE_FLAGS handling unchanged | Constraints, Task 1, Task 4 | covered by judgment, matcher says none | ccsession:124 |
| INF-005 tests fail on old code | Tasks 1 to 3 red logs | covered | plan Task 1 to 3 acceptance |
| INF-006 documented where other variables are | Tasks 5 to 8 | covered | README table, ccsession header |
