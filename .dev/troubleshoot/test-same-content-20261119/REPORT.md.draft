# Troubleshoot report: test_same_content_is_true_only_for_identical_readable_files

**Target**: `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files`, scope `src/superclaude/cli/install_keep.py`
**Type**: test | **Tier reached**: 1 (`--no-escalate`) | **Calibrated confidence**: 1.00 (independent `confidence-calibrator`, verdict STOP) | **Status**: partial (the evidence validator dropped one git-history citation it could not read; the claim is restated from captured command output, see Diagnosis; no other citation was dropped and no structural assertion fired)
**Escalation reason**: none (suppressed by `--no-escalate`; without it the "intermittent" rule would have escalated)
**Waves run**: 0, 1, 1.5 (documentation grounding), 1.6 (diagnosability audit), 1.7 (hypothesis + calibration), 2, 5. Not run: Wave 3 and 4 (Tier 2, suppressed), 4.5 (no pipeline boundary), 6 (`--fix` not set).

## Summary

The test fails because `same_content` answers from a cache. `filecmp.cmp(a, b, shallow=False)` (`src/superclaude/cli/install_keep.py:21`) remembers its result under the file path, size and modification time. The test rewrites `b` with a same-size value inside the same filesystem timestamp tick, so the key is unchanged and the old "identical" answer comes back. This was observed inside the real failing test. The failure is flaky, not caused by issue 606, and the same flaw is a small real bug in the product function and in a second copy in `install_core.py`.

## Documentation Context

No release document covers this behaviour. Five architecture docs were consulted and all are current by git date; none describes `same_content` or its caching (one design doc only mentions `filecmp.cmp` in a test). The binding contract is the docstring at `install_keep.py:19`, "True only when both files are readable and byte-identical", which is exactly what the test asserts, so the test is correct. Card: `doc-context.md`. Separate finding: `docs/getting-started/upgrading.md` says an upgrade "keeps no backup" of edited files, but `install_keep.py` (#480, 2026-11-09) now saves a differing file as `<name>.bak.<stamp>` before a forced overwrite; that doc may be out of date and is not part of this fix.

## Diagnosability Context

Verdict: sufficient. Complexity: trivial. No logging exists on the comparison path (the only handler is a silent `except OSError: return False` at `install_keep.py:22-23`), but the cause was observed directly with read-only probes, so no instrumentation tasklist was needed. Card: `diagnosability-context.md`.

## Diagnosis

`same_content` returns a stale cached True when the second file is rewritten with the same size inside the same timestamp tick.

Mechanism, from the stdlib source (behaviour-definition row 1): `filecmp.cmp` computes a signature `(file type, size, mtime)` for each file, looks up `_cache.get((f1, f2, s1, s2))`, and only compares bytes on a miss. The test calls `same_content(a, b)` with both files "x" (cached True), rewrites `b` as "y" (still 1 byte), and calls it again. If `b`'s mtime did not change, the key matches and the cached True is returned.

Observed (three independent measurements, all in this session):
1. Inside the real failing test (six runs with a throwaway pytest plugin): `b`'s `st_mtime_ns` was identical on the first and second call, the second call had `cache_hit=True`, and the test failed in all six runs.
2. Replaying the test sequence 200 times in a script: both writes landed in the same tick 188 times, and in every one of those 188 the answer was a wrong True; in the 12 runs where the mtime changed the answer was False.
3. Forcing the colliding signature with `os.utime`: True (wrong); after `filecmp.clear_cache()`: False.

Scope of the flaw:
- `src/superclaude/cli/install_core.py:121-125` has a private `_same_content` with the same `filecmp.cmp(a, b, shallow=False)` call, so the same latent flaw.
- Callers that trust the answer: `src/superclaude/cli/install_user_setup.py:90`, `src/superclaude/cli/install_commands.py:61` (stale-file report) and `backup_if_differs` at `install_keep.py:42` (the pre-overwrite backup). A false "identical" would hide a stale kept file and skip the backup. How often this bites a real install is not measured: it needs a same-size rewrite within one timestamp tick, and on this machine the test sequence hit that tick in 188 of 200 runs.
- Not caused by issue 606: the git output in `tier1-observation.md` ("git history of the two files") shows one change to `install_keep.py` and its test in the history, the #480 install change (2026-11-09), and `git log --oneline origin/master..HEAD` over `install_keep.py`, the test and `install_core.py` is empty, so this branch did not change them. (The validator could not read git, so this claim rests on the captured command output, not on a file citation.)

`test_is_wrong`: false (the test states the documented contract). `behavior_is_documented`: false.

## Evidence

- `src/superclaude/cli/install_keep.py:21` — `return filecmp.cmp(a, b, shallow=False)`; the only producer of the value (producers.md P1).
- `src/superclaude/cli/install_keep.py:19` — `"""True only when both files are readable and byte-identical."""`
- `tests/cli/test_install_keep.py:41` — `assert same_content(a, b)`; line 42 rewrites `b` with `"y"`; line 43 — `assert not same_content(a, b)` (the failing line).
- `src/superclaude/cli/install_core.py:121-125` — `def _same_content(a: Path, b: Path) -> bool:` / `return filecmp.cmp(a, b, shallow=False)`.
- Command: `uv run pytest tests/cli/test_install_keep.py -q -k same_content` → `1 failed` at line 43 (five of six runs; observation file `tier1-observation.md`).
- Command: `PYTHONPATH=/tmp uv run pytest tests/cli/test_install_keep.py -q -k same_content -p probe_plugin` → in each of six runs `PROBE b mtime_ns=<same value> size=1 cache_hit=False result=True` then `PROBE b mtime_ns=<same value> size=1 cache_hit=True result=True`, `1 failed` (tier1-observation.md, "Parent probe 3").
- Command: `uv run python /tmp/probe_same_content.py` → `runs=200 same_mtime_tick=188 wrong_true_answers=188`; `forced same signature: same_content -> True (expected False)`; `after clear_cache -> False`; `proposed fix, forced same signature -> False` (tier1-observation.md, "Parent probe 2").
- behaviour-definition: row 1 (`behaviour-definitions.md`) — stdlib `filecmp.cmp` source: `outcome = _cache.get((f1, f2, s1, s2))` before `_do_cmp`; `_sig` returns `(stat.S_IFMT(st.st_mode), st.st_size, st.st_mtime)`.

## Proposed Fix

Not applied (`--fix` not set). Smallest change at the producer, `src/superclaude/cli/install_keep.py`, first line inside `same_content`:

```python
def same_content(a: Path, b: Path) -> bool:
    """True only when both files are readable and byte-identical."""
    filecmp.clear_cache()  # the stdlib cache is keyed on size and mtime, so a same-size rewrite in one tick would be answered from it
    try:
        return filecmp.cmp(a, b, shallow=False)
    except OSError:
        return False
```

Apply the same one-liner to `install_core.py:_same_content`, or better have it call `same_content` from `install_keep`. Alternative: `a.read_bytes() == b.read_bytes()` (no global state, but reads both files whole and changes behaviour for non-regular files).

Test that would prove it (add to `tests/cli/test_install_keep.py`, needs `import os`): write "x" to both files, assert `same_content`, remember `b.stat()`, rewrite `b` as "y", restore its mtime with `os.utime(b, ns=(st.st_atime_ns, st.st_mtime_ns))`, assert `not same_content(a, b)`. On the current code this fails on every run; with the fix it passes. The existing test then passes on every repeat.

## Alternative Fixes Considered

- `a.read_bytes() == b.read_bytes()`: correct and self-contained; rejected as the default only because it reads whole files and treats non-regular files differently.
- Sleep or `os.utime` in the existing test only: hides the product flaw; rejected.

## Risk + Rollback

`filecmp.clear_cache()` empties a process-wide cache that is only a speed-up; the cost is one byte comparison per call, which is small for installer-sized files. Callers can only change from a wrong "identical" to a correct "differs". Rollback: remove the line. After applying, run `uv run pytest tests/cli/test_install_keep.py tests/cli -k "install" -q` and the new test above.

## Next Steps

- Decide where the fix goes (see the chat message): it is unrelated to issue 606, so a separate small issue or branch keeps the 606 diff clean.
- If fixing, use `/sc:troubleshoot ... --fix` or make the one-line change by hand, add the deterministic test, and apply the same change to `install_core.py:_same_content`.
- Separately check `docs/getting-started/upgrading.md` against the #480 backup behaviour.

## Grounding Gaps

- Tier 2 (Waves 3 and 4) was not run (`--no-escalate`); calibrated confidence is 1.00, so no competing hypothesis was needed.
- The calibrator ran before the in-process measurement (probe 3) existed; it recorded that gap as the only residual one, and probe 3 closes it. Its structural rows C4, C6 and C7 were skipped because no diagnosability tasklist exists (verdict sufficient).
- Wave 4.5 (pipeline hardening) did not apply: no runtime, generated-artifact or review boundary is involved.
- The worker for documentation branch B had its output flagged by the harness for an instruction-like pattern ("settings-json", from plain text about `settings.json.bak.<timestamp>`); the tags were neutralized and nothing in it was followed.
- The deterministic new test and the fix were exercised only on a local copy in a scratch script, not on the repo.
