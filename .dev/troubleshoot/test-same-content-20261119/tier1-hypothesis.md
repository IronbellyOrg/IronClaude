# Hypothesis: `filecmp.cmp` returns a cached "identical" result because the same-size rewrite of `b` leaves its (type, size, mtime) signature unchanged

**Agent**: root-cause-analyst (troubleshoot-analyst worker)
**Tier**: 1
**Timestamp**: 2026-11-19T01:26:20Z (parent-supplied)
**Cause class**: Stale state / cache (also fits Substituted primitive: the stdlib call, not our code, decides the answer)
**Claim class**: `runtime_behavior`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned

## Claim

`same_content` (`src/superclaude/cli/install_keep.py:21`) calls `filecmp.cmp(a, b, shallow=False)`. That function keeps a process-wide cache keyed on `(f1, f2, sig1, sig2)`, where `sig` is (file type, size, mtime). In the test, `a` and `b` are both "x" and the first call caches True. `b.write_text("y")` then keeps the same size, 1 byte. When the rewrite lands in the same filesystem timestamp tick as the first write, mtime is unchanged and the cache key matches. The second call returns the stale True, so `assert not same_content(a, b)` fails (`tests/cli/test_install_keep.py:43`). The intermittence comes from that timing.

## Evidence

- `src/superclaude/cli/install_keep.py:21` is `return filecmp.cmp(a, b, shallow=False)`. It is the only producer (producers.md P1, `surviving=yes`; exit statement is the return at :21). The `except OSError` at :22-23 is not taken because both files exist.
- `tests/cli/test_install_keep.py:39-43` writes "x" to `a` and `b`, asserts `same_content(a, b)`, rewrites `b` with "y" (same length), then asserts `not same_content(a, b)`.
- behaviour-definition: row 1. The verbatim stdlib `filecmp.cmp` body does `outcome = _cache.get((f1, f2, s1, s2))` before `_do_cmp`, and `_sig` is `(S_IFMT(st_mode), st_size, st_mtime)`.
- Probe from tier1-observation.md, captured by the parent in the same shell. After a rewrite the signatures were equal: `(32768, 1, 1795050557.418777)` before and after. The second call returned True. After `filecmp.clear_cache()` the result was `False`.
- Failing output, six local runs: one pass, then five failures at line 43 (tier1-observation.md). The same test also failed in two full `make test` runs.

## Proposed Fix

Clear the stdlib compare cache at the start of `same_content`, so every call compares bytes against the current files. The docstring promises "byte-identical", and a cache keyed on mtime cannot guarantee that.

- `src/superclaude/cli/install_keep.py` — add `filecmp.clear_cache()` as the first line inside `same_content`, before the `try`.

Test that would prove it (inert text, not run by the worker):

- Existing: `uv run pytest tests/cli/test_install_keep.py -k same_content` should pass on every repeat.
- New, in `tests/cli/test_install_keep.py`: a deterministic test that forces the colliding signature.
  ```python
  def test_same_content_sees_a_same_size_same_mtime_rewrite(tmp_path):
      a, b = tmp_path / "a", tmp_path / "b"
      a.write_text("x"); b.write_text("x")
      assert same_content(a, b)
      st = b.stat()
      b.write_text("y")
      os.utime(b, ns=(st.st_atime_ns, st.st_mtime_ns))  # restore the old mtime
      assert not same_content(a, b)
  ```
  It needs `import os`. It should fail on the current code on every run and pass with the fix.

An alternative is `a.read_bytes() == b.read_bytes()`. It is more self-contained but loads whole files into memory and changes behaviour for non-regular files.

## Confidence

Self-reported confidence: 0.85

Per-dimension self-assessment:
- Evidence grounding: 1.0. Source lines are read, and the stdlib source is cited as behaviour-definition row 1.
- Runtime check: 0.5. The parent-captured probe is an executed reproducer showing equal signatures and the flip after `clear_cache()`. It did not replay the exact pytest ordering, so it shows the mechanism is possible and sufficient, not that it fired in the failing runs.
- Symptom coverage: 1.0. It explains the failure at line 43, the intermittence, and the same failure under `make test`.
- Reproducibility fit: 0.5. The 5-of-6 rate fits the mtime-tick race, but no run recorded the mtimes of `a` and `b` in the failing pytest process.
- Fix directness: 1.0. One line at the single producer.
- Domain coherence: 1.0. The docstring contract matches the test, and the cache is the stdlib's documented behaviour.

## Risks

- `filecmp.clear_cache()` empties a global cache, so any other code using `filecmp` in the same process loses its entries; the loss is a performance cost only. `install_core.py:121` has its own `_same_content`, which was not read and may have the same flaw.
- Callers `src/superclaude/cli/install_user_setup.py:90` and `src/superclaude/cli/install_commands.py:61`, and `backup_if_differs` at `install_keep.py:42`, depend on an accurate "differs" answer. The fix only turns a wrongly cached True into a correct False; it cannot turn a correct answer wrong.
- doc-context.md cites the callers at `install_user_setup.py:77` and `install_commands.py:65`; those are a docstring and a comment line; the call sites are at :90 and :61.
- The real-world stale hit is rare, since it needs a same-size rewrite within one timestamp tick.

## If I'm wrong, it's probably because...

The failing runs hit something other than the cache, such as a different write ordering or pytest-level state; the probe would then show a possible mechanism that is not the one that fired.

## Falsification standard

Run the failing test with one extra line before the line-43 assertion: `print(os.stat(a).st_mtime_ns, os.stat(b).st_mtime_ns, filecmp._cache)`. If a failing run shows `b`'s mtime changed since the first call, or `filecmp._cache` has no entry for `(a, b, ...)`, this hypothesis is false.

## Evidence classification

- **Claim class**: `runtime_behavior` — depends on library cache dispatch and filesystem timestamp granularity.
- **Evidence class**: `runtime_repro` — the probe output was captured by the parent in the same shell.
- **Runtime check performed?**: yes (parent-captured probe). The probe did not replay the exact pytest ordering; the claim is "sufficient and observed in a probe", not "observed firing inside the failing pytest process".
- **If REFUTE verdict, coverage statement**: not applicable (AFFIRM).

## Alternatives considered

- Test-order or fixture leakage: rejected for now; each run uses a fresh `tmp_path`.
- Bug in `_do_cmp`: rejected, because the probe's flip after `clear_cache()` shows the byte compare is correct.

## Grounding gaps

- Not observed: the mtimes of `a` and `b` inside a failing pytest run (the parent runs this measurement next, see tier1-observation.md).
- `install_core.py:121` (`_same_content`) was not read by the worker.
- Codegraph was not used; Grep located the callers and each cited line was Read.

## Parent-added evidence (after receipt, from tier1-observation.md "Parent probe 2")

- Command: `uv run python /tmp/probe_same_content.py` -> `runs=200 same_mtime_tick=188 wrong_true_answers=188 (wrong answers iff mtime unchanged: verified per run)`. This replays the exact test sequence 200 times; the wrong True appears in every run where the mtime did not change and never otherwise.
- Same probe, forced colliding signature (the proposed new test): `same_content -> True` (wrong); after `filecmp.clear_cache()` -> `False`; the proposed fix applied to a local copy -> `False`.
- `src/superclaude/cli/install_core.py:121-125`: the private `_same_content` calls `filecmp.cmp(a, b, shallow=False)` the same way (same latent flaw; read by the parent).
