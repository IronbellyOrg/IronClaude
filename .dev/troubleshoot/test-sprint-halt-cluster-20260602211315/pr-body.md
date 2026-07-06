## Summary

Fixes the **41-failure sprint-suite cluster** (halt / timeout / integration / signal / lifecycle) on `master`.

**Root cause:** `ProcessManager.start()` (`src/superclaude/cli/pipeline/process.py:141`, introduced in `47997190` for deadlock-safe stdin prompt delivery) reads `self._process.stdin`. A real `subprocess.Popen` always has `.stdin`, but the sprint suite's hand-rolled fake Popen doubles never modeled it — so every test patching `subprocess.Popen` raised:

```
AttributeError: '<FakePopen variant>' object has no attribute 'stdin'  @ process.py:141
```

This is fake-Popen interface drift behind the stdin change, not a production bug.

## Fix

Adds `self.stdin = None` (or class-level `stdin = None`) to **30 fake Popen/Process doubles across 12 files**, mirroring the already-established `_FakePopenSuccess` convention (`tests/sprint/test_e2e_success.py:49`, `test_backward_compat_regression.py:93`, `test_rerun_tasks_e2e.py:137`, `test_watchdog.py:300`). Production code is unchanged.

## Verification (`uv run pytest tests/sprint/`)

| Metric | Before | After |
|--------|--------|-------|
| Failed | 54 | **18** |
| Passed | 1012 | **1048** |
| Real `.stdin` failures | ~36 (+ masking layer) | **0** |

- **36 fail→pass, 0 pass→fail** — no regressions; edits confined to `tests/sprint/`.
- The **18 remaining failures are the separate summarizer narrative-leak cluster** (`IndexError` at the test factory + missing context-manager protocol), addressed by #118 — **out of scope** for this PR.

## Complementarity with #118

This PR (all `.stdin` doubles) and #118 (summarizer leak + 13 `.stdin` doubles) are complementary → green suite combined. **Merge note:** the ~13 doubles #118 also patches overlap this change; expect trivially-resolvable conflicts on those identical `self.stdin = None` additions.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
