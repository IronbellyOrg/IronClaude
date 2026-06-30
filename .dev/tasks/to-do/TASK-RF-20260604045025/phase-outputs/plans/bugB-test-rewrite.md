# Bug B Test Rewrite Record — Step 2.3

**Timestamp:** 2026-06-04 05:17
**File modified:** `tests/cli_portify/test_brainstorm_gaps.py` (TEST ONLY)

## What was replaced

The broken `test_skill_not_available_returns_false` (formerly lines 83-89) which patched the module attribute `superclaude.cli.cli_portify.steps.brainstorm_gaps.check_brainstorm_skill_available` but then called the LOCAL import binding of the same name — so the patch was a no-op and the real `$HOME`-coupled function ran (passing/failing based on whether `~/.claude/skills/sc-brainstorm-protocol` happened to exist).

## What it was replaced with (HOME-redirected pair, calls the REAL function)

```python
class TestSkillAvailability:
    def test_skill_not_available_returns_false(self, tmp_path, monkeypatch):
        """No skill dirs under ~/.claude/skills -> False."""
        monkeypatch.setenv("HOME", str(tmp_path))
        assert not check_brainstorm_skill_available()

    def test_skill_available_returns_true(self, tmp_path, monkeypatch):
        """sc-brainstorm-protocol present under ~/.claude/skills -> True."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude" / "skills" / "sc-brainstorm-protocol").mkdir(parents=True)
        assert check_brainstorm_skill_available()
```

- `test_skill_not_available_returns_false`: redirects `HOME` to an empty `tmp_path` so no `~/.claude/skills/*` exists → real function returns False.
- `test_skill_available_returns_true` (NEW): redirects `HOME` to `tmp_path`, creates `tmp_path/.claude/skills/sc-brainstorm-protocol`, → real function returns True. Matches production lookup at `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py:52-62` (`Path(os.path.expanduser("~/.claude/skills")) / "sc-brainstorm-protocol"`).
- Neither test patches `check_brainstorm_skill_available` — both exercise the REAL function against a controlled tmp HOME (hermetic, no longer coupled to the dev machine's actual `$HOME`).

## What was left untouched (verified)

- **Production code** `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py`: NOT modified.
- **`test_fallback_activates_with_warning`** (now at lines ~94-104): COMPLETELY unchanged — it still legitimately patches the module attribute, which works because production code looks the symbol up via the module global (the correct patch site).
- **`from unittest.mock import patch`** import (line 15): RETAINED — still used by `test_fallback_activates_with_warning`.

## Outcome

Test-only hermetic rewrite. No production logic changed. The not-available test now passes deterministically regardless of the dev machine's `$HOME`, and a positive-case test was added.
