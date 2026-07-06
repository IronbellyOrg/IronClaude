---
status: success
tier_reached: 1
confidence: 0.96
type: test
test_is_wrong: mixed  # Bug B test is wrong; Bug A test is correct (fixture availability is the defect)
---

# Troubleshoot Report — CanonicalFixtureParity + brainstorm skill test fail in clean CI

## Summary

Two unrelated CI failures, both caused by **non-hermetic test dependencies on state that does not
exist in a clean checkout**.

- **Bug A (CanonicalFixtureParity, 4 audit files):** the canonical evidence-pack `.log` fixtures the
  tests assert against are matched by `.gitignore:79` (`*.log`) and were never committed. They exist
  in the dev working tree but are absent in a clean CI checkout → `test_canonical_log_present` fails
  and the `canonical_log_text` fixture raises `FileNotFoundError` for the rest. **The tests are
  correct; the fixtures need to be tracked.**
- **Bug B (`test_skill_not_available_returns_false`):** the test patches the module attribute
  `…brainstorm_gaps.check_brainstorm_skill_available` but then calls a **local import binding** of the
  same name, so the patch is a no-op and the *real* environment-sensitive function runs. Its result
  depends on whether `~/.claude/skills/sc-brainstorm{,-protocol}` happens to exist. **The test is
  wrong** (broken mock target + environment coupling).

Tier 1 was sufficient: both root causes are mechanically certain and single-domain (CI test
hermeticity). No escalation.

## Diagnosis

### Bug A — gitignored canonical fixtures

The four `TestCanonicalFixtureParity` classes load a canonical D-00xx synthetic log and assert the
runtime emission matches it byte/line-for-line. Path construction (example):

- `tests/audit/test_slow_shrink_continues.py:66-75` →
  `REPO_ROOT/.dev/releases/complete/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log`
- `tests/audit/test_slow_shrink_continues.py:171-172` — `canonical_log_text` fixture is a bare
  `CANONICAL_LOG.read_text(...)` with **no skip guard**, so a missing file raises `FileNotFoundError`.
- `tests/audit/test_slow_shrink_continues.py:371-375` — `test_canonical_log_present` asserts
  `CANONICAL_LOG.is_file()`.

All six fixtures consumed by the four files:

| Test file | Fixture(s) |
|---|---|
| `test_slow_shrink_continues.py` | `D-0060/fixture-slow-shrink-F-5-4.log` |
| `test_monotonicity_halt_F_5_5_5.py` | `D-0056/fixture-F-5-5-5-halt-cycle-2.log` |
| `test_synthetic_dnsp_dedup_not_regression.py` | `D-0059/fixture-cross-cycle-dedup-shrinking.log`, `D-0059/fixture-cross-cycle-dedup-non-shrink.log` |
| `test_regression_halt_pass1_fail2.py` | `D-0057/fixture-pass1-fail2-shrinking.log`, `D-0057/fixture-pass1-fail2-non-shrinking.log` |

All six live under `.dev/releases/complete/task-builder-merge/artifacts/D-00xx/` and are caught by the
blanket `*.log` ignore. `.gitignore` itself documents that "in-tree archive/release artifacts under
`.dev/releases/` remain tracked" (line ~231) — so these fixtures are *meant* to be tracked; the
blanket `*.log` rule catches them as unintended collateral.

### Bug B — broken mock target + environment coupling

`tests/cli_portify/test_brainstorm_gaps.py:24-30` imports the symbol into the test module:

```python
from superclaude.cli.cli_portify.steps.brainstorm_gaps import (
    ..., check_brainstorm_skill_available, ...
)
```

`tests/cli_portify/test_brainstorm_gaps.py:83-89`:

```python
def test_skill_not_available_returns_false(self, tmp_path):
    with patch(
        "superclaude.cli.cli_portify.steps.brainstorm_gaps.check_brainstorm_skill_available",
        return_value=False,
    ):
        assert not check_brainstorm_skill_available()   # ← calls the LOCAL binding, not the patched attr
```

`patch(...)` replaces the attribute on the `brainstorm_gaps` module, but the test calls its own
module-level name `check_brainstorm_skill_available`, bound to the original function object at import
time. The patch never takes effect → the real function executes:

`src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py:52-62`:

```python
skills_base = Path(os.path.expanduser("~/.claude/skills"))
return (skills_base / "sc-brainstorm").is_dir() or (skills_base / "sc-brainstorm-protocol").is_dir()
```

Result is environment-dependent: **True** where the skill is installed (this dev machine has
`~/.claude/skills/sc-brainstorm-protocol`), **False** in a clean checkout. Two independent defects:
the patch tests nothing, and even if removed the assertion couples to `$HOME`.
(`test_fallback_activates_with_warning` at line 91-101 passes because the *production* code looks the
symbol up via the module global — that patch site is correct. Only the direct-call test is broken.)

## Evidence (commands run)

- `git check-ignore -v .../D-0060/fixture-slow-shrink-F-5-4.log` →
  `.gitignore:79:*.log <path>` (proves the blanket ignore catches it).
- `git ls-files "*.log" | grep .dev/ | wc -l` → `0` (no `.dev` logs tracked).
- All six fixtures present on disk (`exists=Y tracked=N` for each).
- `uv run pytest …/test_brainstorm_gaps.py -k skill -v` →
  `test_skill_not_available_returns_false FAILED — assert not True` on this machine
  (skill installed); `ls ~/.claude/skills` confirms `sc-brainstorm-protocol` present, `sc-brainstorm` absent.
- `uv run pytest <4 audit files> -k Canonical -q` → **27 passed** locally (fixtures present),
  proving logic is correct and only fixture availability differs in CI.
- Transient `.gitignore` negation `!.dev/releases/**/artifacts/**/fixture-*.log` →
  all six fixtures report `UN-IGNORED` via `git check-ignore`; `twine.log` and
  `.dev/releases/**/results/phase-*-output.txt` stay ignored (negation is tightly scoped).
  `.gitignore` restored after the probe.

## Proposed Fix

### Fix A — track the canonical fixtures (test files unchanged)

1. Append to `.gitignore` (after the `*.log` block):

   ```gitignore
   # Canonical evidence-pack fixtures asserted by tests/audit/*CanonicalFixtureParity*.
   # The blanket *.log rule above otherwise leaves them untracked → clean CI checkouts fail.
   !.dev/releases/**/artifacts/**/fixture-*.log
   ```

2. Stage and commit the six fixtures (no `-f` needed once un-ignored; these are `.dev/` release
   artifacts, not `.claude/` — committing aligns with the documented `.dev/releases/` tracking policy):

   ```bash
   git add .dev/releases/complete/task-builder-merge/artifacts/D-0056/fixture-F-5-5-5-halt-cycle-2.log .dev/releases/complete/task-builder-merge/artifacts/D-0057/fixture-pass1-fail2-shrinking.log .dev/releases/complete/task-builder-merge/artifacts/D-0057/fixture-pass1-fail2-non-shrinking.log .dev/releases/complete/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log .dev/releases/complete/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log .dev/releases/complete/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log .gitignore
   ```

   *(Optional hardening, not required: give `canonical_log_text` a `pytest.skip` guard so a future
   missing fixture skips rather than errors. Not recommended here — a hard failure is the correct
   signal that the evidence pack regressed.)*

### Fix B — make the brainstorm test hermetic (test-only; `test_is_wrong=true`)

Replace the broken patch with `$HOME` redirection so the **real** function inspects a controlled
directory. Covers both the absent and present cases and tests the actual logic:

```python
class TestSkillAvailability:
    def test_skill_not_available_returns_false(self, tmp_path, monkeypatch):
        """No skill dirs under ~/.claude/skills → False."""
        monkeypatch.setenv("HOME", str(tmp_path))
        assert not check_brainstorm_skill_available()

    def test_skill_available_returns_true(self, tmp_path, monkeypatch):
        """sc-brainstorm-protocol present under ~/.claude/skills → True."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude" / "skills" / "sc-brainstorm-protocol").mkdir(parents=True)
        assert check_brainstorm_skill_available()
```

*(More robust alternative — dependency injection: change the signature to
`check_brainstorm_skill_available(skills_base: Path | None = None)` defaulting to the expanduser path,
then pass `tmp_path` in tests. This touches production code but removes the `$HOME` dependency
entirely. Either is acceptable; the `$HOME` monkeypatch is the minimal test-only fix.)*

## Risk + Rollback

- **Fix A:** committing six small text fixtures (~4.5 KB each). Negation is anchored to
  `.dev/releases/**/artifacts/**/fixture-*.log` — verified not to leak other `.log` files. Rollback:
  revert the `.gitignore` line + `git rm --cached` the six files.
- **Fix B:** test-only (option 1). `monkeypatch.setenv("HOME", ...)` is auto-undone by pytest after
  each test; no cross-test leakage. On non-POSIX runners `expanduser` consults `USERPROFILE`, but CI
  here is Linux — `HOME` is authoritative.

## Next Steps

This was a diagnose-only run (no `--fix`). To apply: re-run with `--fix` to open the Tier 3
task-builder chain, or have me apply Fix A + Fix B directly on a feature branch and run the suite.
