# Research: Verified fix evidence (from /sc:troubleshoot Tier 1 diagnosis)

**Topic type:** File Inventory + Patterns & Conventions (consolidated)
**Scope:** The 8 files in the fix; all claims reproduced during the troubleshoot run.
**Status:** Complete
**Date:** 2026-06-04

---

## Bug A — CanonicalFixtureParity (tests CORRECT; 6 fixtures untracked)

### Root cause (reproduced)
- `git check-ignore -v .dev/releases/complete/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log` → `.gitignore:79:*.log  <path>`. The blanket `*.log` rule (`.gitignore:79`) ignores all 6 fixtures.
- `git ls-files "*.log" | grep .dev/ | wc -l` → `0`. No `.dev` logs are tracked.
- All 6 fixtures exist on disk (`exists=Y tracked=N`).
- `uv run pytest <4 audit files> -k Canonical` → **27 passed** locally (fixtures present), proving the test logic is correct and only fixture availability differs in clean CI.

### The 6 fixtures (full paths)
```
.dev/releases/complete/task-builder-merge/artifacts/D-0056/fixture-F-5-5-5-halt-cycle-2.log
.dev/releases/complete/task-builder-merge/artifacts/D-0057/fixture-pass1-fail2-shrinking.log
.dev/releases/complete/task-builder-merge/artifacts/D-0057/fixture-pass1-fail2-non-shrinking.log
.dev/releases/complete/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log
.dev/releases/complete/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log
.dev/releases/complete/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log
```

### Test consumption sites (file:line)
- `tests/audit/test_slow_shrink_continues.py:66-75` (CANONICAL_LOG), `:171-172` (`canonical_log_text` bare read_text — FileNotFoundError if missing), `:364` (TestCanonicalFixtureParity), `:371-375` (test_canonical_log_present → `assert CANONICAL_LOG.is_file()`).
- `tests/audit/test_monotonicity_halt_F_5_5_5.py:64-71`, `:304`.
- `tests/audit/test_synthetic_dnsp_dedup_not_regression.py:87-89`, `:98-100`, `:446`.
- `tests/audit/test_regression_halt_pass1_fail2.py:79-81`, `:90-92`, `:417`.

### Verified fix — .gitignore negation
Append AFTER the `*.log` block (line 79):
```gitignore
# Canonical evidence-pack fixtures asserted by tests/audit/*CanonicalFixtureParity*.
# The blanket *.log rule above otherwise leaves them untracked -> clean CI checkouts fail.
!.dev/releases/**/artifacts/**/fixture-*.log
```
VERIFIED (transient append + `git check-ignore` + revert): the 6 fixtures become UN-IGNORED; `twine.log` and `.dev/releases/**/results/phase-*-output.txt` stay ignored. Negation does not leak other `.log` files.

Then `git add` the 6 fixtures + `.gitignore` (no `-f` needed once un-ignored). These are `.dev/` artifacts — staging is policy-aligned; NO `.claude/` path is involved.

## Bug B — test_skill_not_available_returns_false (test is WRONG)

### Root cause (reproduced)
- `uv run pytest tests/cli_portify/test_brainstorm_gaps.py -k skill -v` → `test_skill_not_available_returns_false FAILED — assert not True` on this dev machine (where `~/.claude/skills/sc-brainstorm-protocol` exists).
- `tests/cli_portify/test_brainstorm_gaps.py:24-30` imports `check_brainstorm_skill_available` into the test module (local binding bound to the original function at import time).
- `tests/cli_portify/test_brainstorm_gaps.py:83-89`: patches `superclaude.cli.cli_portify.steps.brainstorm_gaps.check_brainstorm_skill_available` (module attribute) but `assert not check_brainstorm_skill_available()` calls the LOCAL name → patch never applies → real function runs → result depends on `$HOME`/`~/.claude/skills`.
- `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py:52-62`:
  ```python
  skills_base = Path(os.path.expanduser("~/.claude/skills"))
  brainstorm_skill = skills_base / "sc-brainstorm"
  brainstorm_protocol = skills_base / "sc-brainstorm-protocol"
  return brainstorm_skill.is_dir() or brainstorm_protocol.is_dir()
  ```
- `test_fallback_activates_with_warning` (`:91-101`) passes because production code looks the symbol up via the module global — that patch site is correct. Only the direct-call test is broken. DO NOT touch the fallback test.

### Verified fix — hermetic rewrite (test-only)
Replace `test_skill_not_available_returns_false` (`:83-89`) with a `$HOME`-redirected pair that calls the REAL function:
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
Keep `test_fallback_activates_with_warning` unchanged. The `patch` import (`from unittest.mock import patch`) is still used by other tests in the file (e.g. `:85`, `:94`) — confirm before removing any import (it IS still needed — `test_fallback_activates_with_warning` uses `patch`).

## Validation commands
- `uv run pytest tests/audit/test_slow_shrink_continues.py tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_synthetic_dnsp_dedup_not_regression.py tests/audit/test_regression_halt_pass1_fail2.py -k Canonical` → expect 27 passed.
- `uv run pytest tests/cli_portify/test_brainstorm_gaps.py -k skill -v` → expect all green (incl. on this dev machine where sc-brainstorm-protocol is installed).
- `uv run ruff check` and `uv run ruff format --check src/ tests/` → no new errors.
- `git status --porcelain | grep '^[AM] .claude/'` → MUST be empty (no `.claude/` staged).

## Summary
Two independent, small, reproduced fixes. Bug A = data/gitignore (commit fixtures); Bug B = test rewrite (hermetic). No production code logic changes. 8 files total, 6 of which are `git add` of pre-existing fixtures.
