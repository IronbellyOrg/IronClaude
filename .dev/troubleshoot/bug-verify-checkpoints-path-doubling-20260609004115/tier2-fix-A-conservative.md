# Tier 2 Fix Proposal — Fix A (CONSERVATIVE / minimal blast radius)

Bug: `extract_checkpoint_paths` doubles the release-dir segment for release-prefixed,
absent checkpoint paths.
Target file: `src/superclaude/cli/sprint/checkpoints.py`
Mode: READ-ONLY proposal (no source edited).

---

## 1. ROOT CAUSE confirmation — AGREE with grounding

**Confirmed at `checkpoints.py:86-94`.** The resolution ladder is:

- `checkpoints.py:87-88` — absolute → returned verbatim (note: NOT `.resolve()`; the
  test at `tests/sprint/test_checkpoints.py:85` asserts `Path("/abs/checkpoints/CP.md")`
  unresolved, so this branch must stay byte-identical).
- `checkpoints.py:89-92` — `candidate.exists()` is a **cwd-relative** probe. When the
  declared path is release-prefixed (`.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-*.md`)
  and the sprint is invoked from the worktree root, this probe is True **iff the file is
  already on disk**, in which case `candidate.resolve()` yields the correct path with no
  doubling.
- `checkpoints.py:94` — the `else` branch `(release_dir / candidate).resolve()` is the
  **doubling site**. When `release_dir` already ends with the same path components the
  candidate begins with (e.g. `release_dir=/W/.dev/e2e-reflect/tl-1/bundle` and
  `candidate=.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md`), the join produces
  `/W/.dev/e2e-reflect/tl-1/bundle/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md`.

**Found/missing asymmetry confirmed** exactly as the grounding states (`checkpoints.py:89`
vs `:94`): CP-P01 (present) → `exists()`→True → line 92 → correct; CP-P02 (absent) →
`exists()`→False → line 94 → DOUBLED. This precisely reproduces the on-disk manifest
evidence in `.dev/e2e-reflect/tl-1/bundle/manifest.json` cited in `grounding.md:7-9`.

I independently reproduced the doubling and the asymmetry by executing the live ladder
logic against the four mandate inputs (see §3).

---

## 2. EXACT proposed code

Add a module-level helper (place it directly **above** `extract_checkpoint_paths`, i.e.
before `checkpoints.py:40`), and replace ONLY the `else` body at `checkpoints.py:94`.
The absolute branch (87-88) and the `candidate.exists()` fast-path (89-92) are UNCHANGED.

### New helper (insert before `def extract_checkpoint_paths`)

```python
def _join_release_relative(release_dir: Path, candidate: Path) -> Path:
    """Join a release-relative ``candidate`` onto ``release_dir`` idempotently.

    A phase tasklist may declare a checkpoint path in *bare* release-relative
    form (``checkpoints/CP.md``) OR in *release-prefixed* form, where the path
    already carries the release_dir's own trailing components
    (``.dev/e2e-reflect/tl-1/bundle/checkpoints/CP.md`` when release_dir ends
    with ``.dev/e2e-reflect/tl-1/bundle``). A naive ``release_dir / candidate``
    doubles the shared segment for the prefixed form.

    Strategy: find the LONGEST k such that ``release_dir``'s last k path parts
    equal ``candidate``'s first k path parts, then join only the non-overlapping
    remainder. k=0 (bare form, no overlap) degrades to plain
    ``release_dir / candidate`` — preserving the existing test contract.
    Longest-match (not first-match) is used so a full multi-segment prefix wins
    over a coincidental single-segment tail collision.
    """
    r_parts = release_dir.parts
    c_parts = candidate.parts
    overlap = 0
    for k in range(min(len(r_parts), len(c_parts)), 0, -1):
        if r_parts[-k:] == c_parts[:k]:
            overlap = k
            break
    if overlap:
        remainder = c_parts[overlap:]
        return release_dir.joinpath(*remainder) if remainder else release_dir
    return release_dir / candidate
```

### Replacement for the `else` branch (`checkpoints.py:93-94`)

Before:

```python
        else:
            resolved = (release_dir / candidate).resolve()
```

After:

```python
        else:
            resolved = _join_release_relative(release_dir, candidate).resolve()
```

That is the **entire** functional change. Lines 86-92 untouched; `.resolve()` is still
applied at the same point, preserving normalization semantics for the existing tests.

---

## 3. Walkthrough — resolved path per mandate input

Verified by executing the helper/ladder logic (uv run python). `R()` = `Path.resolve()`.

| # | Input | Branch taken | Resolved path |
|---|-------|--------------|---------------|
| (a) | `/abs/checkpoints/CP.md` (absolute) | `is_absolute()` → `:88` (UNCHANGED) | `/abs/checkpoints/CP.md` (verbatim, unresolved) |
| (b) | bare `checkpoints/CP-P01-END.md`, release_dir=`tmp_path`, file absent | `else` → helper, overlap **k=0** | `R(tmp_path/checkpoints/CP-P01-END.md)` = `tmp_path/checkpoints/CP-P01-END.md` |
| (c) | release-prefixed `.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md`, release_dir=`/W/.dev/e2e-reflect/tl-1/bundle`, file ABSENT | `else` → helper, overlap **k=4** (`.dev`,`e2e-reflect`,`tl-1`,`bundle`) | `/W/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md` — **NO doubling** |
| (d) | `TASKLIST_ROOT/checkpoints/CP.md` → stripped at `:77-78` to `checkpoints/CP.md`, release_dir=`tmp_path` | `else` → helper, overlap **k=0** | `tmp_path/checkpoints/CP.md` |

(b) and (d) are byte-identical to current behavior — the existing-test contract at
`tests/sprint/test_checkpoints.py:63, :109` and the `TASKLIST_ROOT` stripping at
`checkpoints.py:77-80` are preserved. (c) is the bug-case, now idempotent.

For (c), if the file WERE present it would take the `:89-92` fast-path (unchanged) and
already resolve correctly — so the fix only alters the absent branch, exactly as mandated.

---

## 4. Regression TEST (pytest, TestExtractCheckpointPaths style)

Add to `class TestExtractCheckpointPaths` in `tests/sprint/test_checkpoints.py`.
The release_dir is constructed to end with the SAME components the declared path begins
with, and the target file is intentionally NOT created (absent → exercises `:94`).

```python
    def test_release_prefixed_absent_path_not_doubled(self, tmp_path: Path):
        """Defect regression: a release-PREFIXED relative `Checkpoint Report Path:`
        whose target file is ABSENT must resolve idempotently against release_dir —
        the shared release segment must appear exactly once, never doubled.

        Pre-fix: the `else` branch did `(release_dir / candidate).resolve()`, which
        doubled the overlapping segment (checkpoints.py:94)."""
        # release_dir ends with the same tail the declared path begins with.
        release_dir = tmp_path / ".dev" / "e2e-reflect" / "tl-1" / "bundle"
        release_dir.mkdir(parents=True)
        rel_prefix = ".dev/e2e-reflect/tl-1/bundle"

        phase_file = release_dir / "phase-2-tasklist.md"
        phase_file.write_text(
            "### Checkpoint: End of Phase 2\n"
            f"Checkpoint Report Path: {rel_prefix}/checkpoints/CP-P02-END.md\n"
        )
        # Target checkpoint file deliberately ABSENT → forces the join branch.

        result = extract_checkpoint_paths(phase_file, release_dir)
        assert len(result) == 1
        _, path = result[0]

        expected = (release_dir / "checkpoints" / "CP-P02-END.md").resolve()
        assert path == expected
        # No segment doubled: the release tail appears exactly once.
        assert str(path).count("/e2e-reflect/tl-1/bundle/") == 1
        assert ".dev/e2e-reflect/tl-1/bundle/.dev/" not in str(path)

    def test_bare_release_relative_still_joins(self, tmp_path: Path):
        """Contract lock: a BARE release-relative path (zero overlap) still joins
        onto release_dir unchanged — the fix must not over-strip the k=0 case."""
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text(
            "### Checkpoint: End of Phase 1\n"
            "Checkpoint Report Path: checkpoints/CP-P01-END.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert result[0][1] == (tmp_path / "checkpoints" / "CP-P01-END.md").resolve()
```

Run: `uv run pytest tests/sprint/test_checkpoints.py::TestExtractCheckpointPaths -q`

Note on `phase_file` placement: the existing tests put `phase_file` under `tmp_path`
and run with cwd=repo-root so `candidate.exists()` is False (`grounding.md:42`). This new
test places `phase_file` under `release_dir` for realism, but the candidate path is still
absent on disk, so the `else` branch is still the one exercised — the assertion holds
regardless of cwd because the declared path component `checkpoints/CP-P02-END.md` does not
exist relative to any plausible cwd.

---

## 5. RISKS

- **R1 (low):** `.resolve()` collapses `..`/symlinks; behavior here is identical to the
  current `:94` (resolve applied at the same point), so no new normalization surprise.
- **R2 (low):** The helper compares `Path.parts`, which is OS-path-separator aware and
  drops redundant separators — robust to `checkpoints//CP.md`-style noise.
- **R3 (very low):** Over-stripping a genuinely-nested path whose first segment
  coincides with a release tail segment (see §6) — mitigated by longest-match and by the
  fact the old code ALSO mishandled that case.
- **R4 (none for tests):** Existing tests at `:63, :85, :109` are untouched in outcome —
  absolute passthrough (k-loop never runs for absolute, handled at `:88`), bare-relative
  (k=0), and `TASKLIST_ROOT` stripping all preserved.

**If I'm wrong it's probably because** the real declared paths are not lexically prefixed
by the release tail but doubled via some other anchor (e.g. a symlinked or `..`-laden
`release_dir` whose `.parts` don't textually match the candidate's), in which case the
lexical overlap is k=0 and the doubling would persist — the fix would be a no-op for that
variant and the true anchor mismatch would lie upstream in how `release_dir` is derived
(`commands.py:694` / `executor.py:2457`, per `grounding.md:30-33`).

---

## 6. FALSE-POSITIVE analysis — can overlap-strip remove a legitimate nested dir?

**The risk:** a candidate like `bundle/checkpoints/CP.md` where `bundle` is a real
subdir of release_dir that *coincidentally* shares the name of release_dir's last
segment (`/W/.dev/e2e-reflect/tl-1/bundle`). Naive single-segment matching would strip
`bundle` and resolve to `/W/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP.md` instead of
the intended `/W/.dev/e2e-reflect/tl-1/bundle/bundle/checkpoints/CP.md`.

**Three reasons this fix is safe in practice:**

1. **Longest-match, not first-match.** The k-loop descends from
   `min(len(r),len(c))` and stops at the FIRST (largest) k that matches. A real
   multi-segment release prefix (k=4 in case (c)) always wins over a coincidental
   single-segment collision (k=1). The helper only strips the *maximal contiguous*
   shared run anchored at release_dir's tail / candidate's head — it never strips an
   interior coincidence.

2. **The collision case is ALREADY broken under the current code.** I verified that for
   `candidate=bundle/checkpoints/CP.md` with `release_dir=/W/.dev/e2e-reflect/tl-1/bundle`,
   the OLD `:94` produces `/W/.dev/e2e-reflect/tl-1/bundle/bundle/checkpoints/CP.md` — a
   `bundle/bundle` double. A real nested `bundle/` subdir holding checkpoints is not a
   pattern any tasklist emits: checkpoints are declared either bare (`checkpoints/...`) or
   fully release-prefixed. So the only inputs that hit k≥1 are the prefixed-form inputs the
   fix is *designed* to repair; the fix changes a wrong answer into the right one, it does
   not turn a right answer wrong.

3. **k=0 is the dominant real path and is untouched.** Bare `checkpoints/CP.md` (the
   overwhelmingly common form, and every existing test) has zero overlap → plain join →
   identical to today.

**Residual exposure:** a tasklist that *intentionally* declared
`bundle/checkpoints/CP.md` meaning a literal nested `bundle/` under the release whose name
equals the release tail. This is pathological, unattested in the corpus, and was already
mis-resolved (to `bundle/bundle/...`) before the fix — so the fix does not regress any
currently-working behavior. If defense-in-depth is later wanted, gate the strip on
`not (release_dir / candidate).exists()` — but per the mandate the `else` branch is the
absent-file path, so that guard would be a tautology here and is omitted to keep blast
radius minimal.
