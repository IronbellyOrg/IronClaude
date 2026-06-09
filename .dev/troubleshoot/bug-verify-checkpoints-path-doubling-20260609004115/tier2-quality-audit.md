# Tier 2 Quality / Edge-Case Audit — verify-checkpoints path-doubling

**Mode:** Tier 2 quality/edge-case skeptic, depth=deep. **READ-ONLY** — no source edited.
**Defect site:** `src/superclaude/cli/sprint/checkpoints.py:86-94` (`extract_checkpoint_paths`).
**On-disk confirmation:** `.dev/e2e-reflect/tl-1/bundle/manifest.json` entry P02 →
`.../bundle/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md` (segment `.dev/e2e-reflect/tl-1/bundle` doubled).
Declared path in `phase-2-tasklist.md:134` = `` `.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md` `` (release-prefixed-relative).
`release_dir` = `.../ReflectInTaskLists/.dev/e2e-reflect/tl-1/bundle` (the bundle root; confirmed from manifest P01 `expected_path`).

---

## Fix definitions under test

Both fixes replace the `candidate.exists()`-selected join (current lines 86-94) with a **lexical
longest-overlap idempotent join**:

```
parts        = candidate parts (release-relative, after TASKLIST_ROOT strip)
rel_parts    = release_dir parts
k_max        = min(len(rel_parts), len(parts))
strip largest k in [k_max..1] s.t. rel_parts[-k:] == parts[:k]
resolved     = (release_dir / Path(*parts[k:])).resolve()   # k=0 ⇒ no overlap, plain join
```

- **Fix A** — keeps the `candidate.exists()` fast-path *before* the overlap logic
  (i.e. `is_absolute` → passthrough; `elif candidate.exists()` → `candidate.resolve()`;
  `else` → overlap-strip join).
- **Fix B** — removes the `candidate.exists()` branch entirely; `is_absolute` → passthrough;
  everything else → overlap-strip join (no cwd probe).

> [INFERENTIAL] Exact code is not yet written; this audit reasons from the two candidate shapes as
> described in the mandate. Where a regression verdict depends on an implementation detail of the
> strip, it is flagged.

---

## 1. INPUT-SHAPE MATRIX

`R` = `release_dir` = `/w/.dev/e2e/bundle` (4 trailing parts after root: `w`,`.dev`,`e2e`,`bundle`) unless noted.

| # | Shape | Example `raw_path` | Expected resolved | Overlap-strip output | OK? |
|---|-------|--------------------|-------------------|----------------------|-----|
| S1 | Absolute | `/abs/checkpoints/CP.md` | `/abs/checkpoints/CP.md` (verbatim, **unresolved**) | `is_absolute` branch → verbatim | ✅ (both fixes keep passthrough) |
| S2 | `TASKLIST_ROOT/...` | `TASKLIST_ROOT/checkpoints/CP.md` | `R/checkpoints/CP.md` | prefix stripped → `checkpoints/CP.md`; no overlap (k=0) → `R/checkpoints/CP.md` | ✅ |
| S3 | Bare `TASKLIST_ROOT` | `TASKLIST_ROOT` | `R` (`.` rel) | rewritten to `.`; `Path(".")` parts=`()` → k=0 → `R/.` = `R` | ✅ [INFERENTIAL: `Path(".").parts == ()`; join of empty → `R.resolve()`] |
| S4 | Bare release-relative | `checkpoints/CP.md` | `R/checkpoints/CP.md` | parts=`(checkpoints,CP.md)`; `bundle`≠`checkpoints` → k=0 → `R/checkpoints/CP.md` | ✅ (existing-test contract) |
| S5 | **Release-prefixed relative (THE BUG)** | `.dev/e2e/bundle/checkpoints/CP.md` | `R/checkpoints/CP.md` | parts head `.dev,e2e,bundle` == `R` tail `.dev,e2e,bundle` → k=3 strip → `R/checkpoints/CP.md` | ✅ FIXED |
| S6 | Path with `..` | `../bundle/checkpoints/CP.md` | ambiguous; literal intent `R/../bundle/checkpoints/CP.md` → resolves to `R/checkpoints/CP.md` (since `R` ends `bundle`)… | parts=`(..,bundle,checkpoints,CP.md)`; `R` tail `..bundle..` ≠ — `..`≠`bundle`, no suffix==prefix match → k=0 → `(R/../bundle/checkpoints/CP.md).resolve()` = `/w/.dev/e2e/bundle/checkpoints/CP.md` | ✅ resolve() collapses `..`; lands correct **by coincidence** [INFERENTIAL] |
| S7 | Partial/coincidental single-seg overlap | `R=/w/x/bundle`, `bundle/checkpoints/CP.md` | **AMBIGUOUS** — see §2 | k=1 (`bundle`==`bundle`) strip → `R/checkpoints/CP.md` | ⚠️ correct IFF `bundle/` was a release-prefix echo, WRONG IFF `bundle` is a real subdir of `R` |
| S8 | Candidate head matches only PART of a longer release tail | `R=/w/a/b/c`, `b/c/checkpoints/CP.md` | `R/checkpoints/CP.md` (prefix `b/c` echoes release tail `b/c`) | longest k: try k=2 → `rel[-2:]`=`(b,c)` == `parts[:2]`=`(b,c)` → strip 2 → `R/checkpoints/CP.md` | ✅ (suffix==prefix anchored at both ends) |
| S9 | Candidate head matches release tail but **misaligned** (one seg of a longer tail) | `R=/w/a/b/c`, `c/checkpoints/CP.md` | likely `R/checkpoints/CP.md` (single-seg echo) **or** real `c/` subdir | k=1 (`c`==`c`) → `R/checkpoints/CP.md` | ⚠️ same ambiguity class as S7 — single-segment overlaps are the residual risk |
| S10 | No overlap at all | `results/foo.md`, `R=/w/.dev/e2e/bundle` | `R/results/foo.md` | k=0 → `R/results/foo.md` | ✅ |
| S11 | Full candidate == release tail, no remainder | `.dev/e2e/bundle`, `R=/w/.dev/e2e/bundle` | `R` | k=3 strip → `R/` (empty remainder) = `R` | ✅ [INFERENTIAL: empty remainder join] |

**Key finding:** the bug case (S5) and all multi-segment echoes (S8) are fixed correctly by longest-overlap.
The *only* hazardous shapes are **single-segment overlaps (S7, S9)** where `candidate`'s first part
coincidentally equals `release_dir`'s last part but is actually an intended real subdirectory.

---

## 2. OVER-STRIP / FALSE-POSITIVE RISK

**The danger shape (S7):** `release_dir = /w/x/bundle`, declared `bundle/checkpoints/CP.md`.

- If `bundle/` is a **release-prefix echo** (agent re-emitted the bundle dir name as a relative anchor) →
  strip is **correct** → `R/checkpoints/CP.md`.
- If `bundle/` is a **genuine subdirectory** `R/bundle/checkpoints/CP.md` (a real nested `bundle` dir
  inside the release) → strip is **WRONG**: it deletes a real path segment, producing
  `R/checkpoints/CP.md` instead of `R/bundle/checkpoints/CP.md`.

Longest-suffix==longest-prefix matching **does NOT distinguish these** — both are lexically identical.
The anchoring the mandate proposes ("overlap starts at candidate part 0 AND aligns to release_dir final
part") is *already inherent* in suffix==prefix and does not resolve the single-segment ambiguity; it only
prevents floating mid-string matches (which a suffix/prefix algorithm already can't produce).

**Residual-risk assessment:**

- **Multi-segment overlaps (k≥2): negligible false-positive risk.** A coincidental 2+ segment
  suffix==prefix collision (e.g. `R` ending `e2e/bundle` AND a real subdir also named `e2e/bundle`)
  is astronomically unlikely in practice. [INFERENTIAL]
- **Single-segment overlaps (k=1): real but low risk.** Requires `release_dir.name` to equal the
  first path-segment of an intended *real* subdir. For sprint bundles `release_dir.name` is typically
  `bundle`/`<release-id>`; a phase tasklist declaring `bundle/...` as a real intended subdir of the
  bundle is not an observed pattern. **Not observed in any of the 11 callers/tests.** [INFERENTIAL]

**Recommended guard (defense-in-depth, applies to BOTH fixes):**
Restrict the strip to **k ≥ 2** OR retain a single-segment strip *only when* the resulting joined path
does NOT exist while the un-stripped path DOES (existence as tiebreaker for k=1 only). Simpler and
sufficient: **prefer the largest k, but if `k == 1`, additionally require that `(release_dir/candidate)`
(the un-stripped join) does not exist on disk** before stripping. This preserves a real `R/bundle/...`
subdir when it exists, and still de-doubles the prefix-echo case (where `R/bundle/...` does not exist
because the file truly lives at `R/...`).

> Note: this k=1 existence tiebreaker re-introduces a disk probe — but a *scoped* one (only the
> ambiguous single-segment case), not the broad cwd-relative probe that caused the original found/missing
> asymmetry. The S5 multi-segment bug is fixed without any probe.

---

## 3. EXISTING-TEST REGRESSION CHECK

All tests pass `tmp_path` as `release_dir`; cwd = repo root ≠ tmp_path, so `candidate.exists()` is
**False** in every existing test (grounding.md:42, confirmed). None declares a release-prefixed path,
so **none triggers a k≥1 overlap** (tmp_path's final segment is a random pytest dir name, never a
prefix of `checkpoints/...`). Therefore overlap-strip yields k=0 for every existing relative case →
identical to the current `else` join.

| Test (line) | Asserted value | Fix A | Fix B |
|-------------|----------------|-------|-------|
| `test_single_checkpoint_backticks` (53) | `path == (tmp_path/"checkpoints"/"CP-P01-END.md").resolve()` | ✅ PASS — k=0 join | ✅ PASS |
| `test_two_checkpoints_mixed_formats` (65) | names `["Mid Phase 3","End of Phase 3"]` (paths not asserted) | ✅ PASS | ✅ PASS |
| `test_absolute_path_preserved` (79) | `[("Abs", Path("/abs/checkpoints/CP.md"))]` (**unresolved**, verbatim) | ✅ PASS — `is_absolute` passthrough untouched | ✅ PASS |
| `test_name_falls_back_to_basename` (87) | `result[0][0] == "CP-P01-END.md"` (name only) | ✅ PASS | ✅ PASS |
| `test_missing_phase_file_returns_empty` (94) | `== []` (read fails before resolve) | ✅ PASS | ✅ PASS |
| `test_wave4_numbered_checkpoint_task_form` (97) | `path == (tmp_path/"checkpoints"/"CP-P01-END.md").resolve()` | ✅ PASS — k=0 join | ✅ PASS |
| `test_zero_checkpoints` (48) | `== []` | ✅ PASS | ✅ PASS |
| `test_wave4_mid_and_end_mixed_with_legacy` (111) | names only | ✅ PASS | ✅ PASS |

**build_manifest / downstream sample:**

| Test (line) | Asserted | Fix A | Fix B |
|-------------|----------|-------|-------|
| `TestBuildManifest.test_single_phase_with_one_checkpoint` (329) | `exists is False`; `recovered False` | ✅ — resolved path is `tmp_path/checkpoints/CP-P01-END.md` (k=0), file absent → `exists False` | ✅ |
| `test_multi_phase_with_mixed_counts` (344) | `exists == [True,False,False]` (P01 seeded) | ✅ — k=0 join, P01 file present | ✅ |
| `TestWriteManifest.test_writes_valid_json_with_summary` (359) | `summary total=3 found=1 missing=2`; `entries[0].expected_path.endswith("CP-P01-END.md")` | ✅ | ✅ |
| `TestRecoverMissingCheckpoints.*` (407-800) | recovery writes at `expected_path` | ✅ — `expected_path` unchanged for bare-relative declares | ✅ |
| `TestVerifyCheckpointsCLI.test_table_output_reports_counts` (809) | `3 declared / 1 found / 2 missing`; `manifest.json` exists | ✅ — CliRunner sets cwd to an isolated dir, but declares are bare-relative → k=0 either way | ✅ |
| `test_recover_flag_regenerates_missing_reports` (832) | `CP-P03-END.md` & `CP-P03-MID.md` exist after recover | ✅ | ✅ |

**Conclusion §3:** Both Fix A and Fix B are **green against the entire existing suite.** No existing
test asserts a resolved value that depends on the `candidate.exists()` branch *being taken*, because
no existing relative test ever satisfies `candidate.exists()` (cwd≠tmp_path) — they all flow through
the `else` join today, which overlap-strip reproduces at k=0. **This means the `candidate.exists()`
branch is currently dead under test** [INFERENTIAL — verified by grounding.md:42 + cwd reasoning],
which is a strong argument for Fix B (see §6).

---

## 4. CALLER SAFETY

| Caller | `release_dir` arg | Is it the bundle root? | Fix-correct? |
|--------|-------------------|------------------------|--------------|
| `commands.py:694` `build_manifest(index_path, output_dir)` | `output_dir` = the verify-checkpoints OUTPUT_DIR positional (`click.Path(exists=True, file_okay=False)`, commands.py:650) | ✅ YES — docstring (676-681) states OUTPUT_DIR is the release dir containing `tasklist-index.md` + `checkpoints/`. In the e2e bug, OUTPUT_DIR == bundle. | ✅ overlap-strip correct |
| `executor.py:2201` `build_manifest(config.index_path, config.release_dir)` | `config.release_dir` = `_resolve_release_dir(index_path)` (config.py:351) → bundle root (or grandparent in tasklist-subdir layout, config.py:262-276) | ✅ YES — release dir by construction | ✅ |
| `executor.py:2457` `extract_checkpoint_paths(phase.file, config.release_dir)` | same `config.release_dir` | ✅ YES | ✅ |
| `checkpoints.py:161` `extract_checkpoint_paths(phase.file, release_dir)` (inside `build_manifest`) | forwarded from the two `build_manifest` callers above | ✅ inherits | ✅ |

**Edge note on `_resolve_release_dir` (config.py:242-278):** when the index lives in a
`tasklist/` subdir AND the grandparent has a spec/state file, `release_dir` = **grandparent**, while
phase files (and any `TASKLIST_ROOT/`-anchored or release-prefixed declares the agent wrote) are
authored relative to that same grandparent release root. So the overlap anchor still matches the
release root — **no caller passes a `release_dir` that is NOT the intended anchor for the declared
paths.** [INFERENTIAL — based on config.py docstring + the manifest evidence; no caller passes e.g.
`index.parent` while declares are grandparent-relative.]

**No unsafe caller found.** All four call paths pass the bundle/release root. The fix is correct for
every real caller.

---

## 5. AUTHORITATIVE REGRESSION TESTS (copy-pasteable, matches file style)

Add to `tests/sprint/test_checkpoints.py` inside `class TestExtractCheckpointPaths`. These encode the
fix contract: (a) prefixed+absent → no doubling, (b) prefixed+present → still correct, (c) no-over-strip
guard for a real single-segment subdir, (d) `..` and bare-relative idempotence.

```python
    def test_release_prefixed_relative_absent_no_doubling(self, tmp_path: Path):
        """THE BUG: a release-PREFIXED relative `Checkpoint Report Path:` whose
        target file is ABSENT must resolve to release_dir/<remainder>, NOT
        release_dir/release_dir/<remainder>. release_dir's trailing parts equal
        the declared path's leading parts, so a naive join doubles them.
        """
        # release_dir's tail segments are echoed as the declared path's head.
        release_dir = tmp_path / "proj" / "bundle"
        release_dir.mkdir(parents=True)
        phase_file = release_dir / "phase-2-tasklist.md"
        rel_prefix = f"{tmp_path.name}/proj/bundle"  # echoes release_dir tail
        phase_file.write_text(
            "### Checkpoint: End of Phase 2\n"
            f"**Checkpoint Report Path:** `{rel_prefix}/checkpoints/CP-P02-END.md`\n"
        )
        result = extract_checkpoint_paths(phase_file, release_dir)
        assert len(result) == 1
        _name, path = result[0]
        expected = (release_dir / "checkpoints" / "CP-P02-END.md").resolve()
        assert path == expected, f"path doubled: {path}"
        # Hard guard: the release-dir tail must appear exactly once in the result.
        assert str(path).count("/proj/bundle/") == 1

    def test_release_prefixed_relative_present_still_correct(self, tmp_path: Path):
        """Prefixed declare whose target file EXISTS must resolve to the same
        single (non-doubled) path — the found/missing asymmetry that produced the
        original bug (present→correct, absent→doubled) must be gone."""
        release_dir = tmp_path / "proj" / "bundle"
        (release_dir / "checkpoints").mkdir(parents=True)
        target = release_dir / "checkpoints" / "CP-P01-END.md"
        target.write_text("ok")
        phase_file = release_dir / "phase-1-tasklist.md"
        rel_prefix = f"{tmp_path.name}/proj/bundle"
        phase_file.write_text(
            "### Checkpoint: End of Phase 1\n"
            f"**Checkpoint Report Path:** `{rel_prefix}/checkpoints/CP-P01-END.md`\n"
        )
        result = extract_checkpoint_paths(phase_file, release_dir)
        assert result[0][1] == target.resolve()
        assert str(result[0][1]).count("/proj/bundle/") == 1

    def test_no_over_strip_real_single_segment_subdir(self, tmp_path: Path):
        """GUARD: a single-segment head that coincidentally equals release_dir's
        final part but is a REAL intended subdirectory on disk must NOT be
        stripped. release_dir ends with `bundle`; the declared path
        `bundle/checkpoints/CP.md` points at a real nested `bundle/` subdir whose
        target file exists — the resolver must keep it, not collapse it.
        """
        release_dir = tmp_path / "bundle"
        nested = release_dir / "bundle" / "checkpoints"
        nested.mkdir(parents=True)
        target = nested / "CP.md"
        target.write_text("ok")  # real file lives at release_dir/bundle/checkpoints/CP.md
        phase_file = release_dir / "phase.md"
        phase_file.write_text(
            "### Checkpoint: Nested\n"
            "**Checkpoint Report Path:** `bundle/checkpoints/CP.md`\n"
        )
        result = extract_checkpoint_paths(phase_file, release_dir)
        # The real nested file must be the resolved target, not the de-doubled one.
        assert result[0][1] == target.resolve()

    def test_bare_relative_join_unchanged_idempotent(self, tmp_path: Path):
        """Contract lock: a bare release-relative path (no echo) is unaffected by
        the overlap logic (k=0) — release_dir/checkpoints/CP.md, exactly as before.
        """
        phase_file = tmp_path / "phase.md"
        phase_file.write_text(
            "### Checkpoint: Bare\n"
            "Checkpoint Report Path: checkpoints/CP-P01-END.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert result[0][1] == (tmp_path / "checkpoints" / "CP-P01-END.md").resolve()
```

> **`test_no_over_strip_real_single_segment_subdir` is the discriminating test:**
> a plain longest-overlap (k=1) implementation **FAILS** it (collapses the real subdir); only a fix
> carrying the §2 k=1 existence-tiebreaker guard PASSES it. If the team chooses NOT to add the guard
> (accepting the single-segment risk as theoretical), this test should be written as the documented
> known-limitation (xfail) rather than dropped — so the risk is recorded, not silent.

---

## 6. VERDICT — Fix B (lower risk), with the §2 k=1 guard

**Recommend Fix B (remove the `candidate.exists()` fast-path), augmented with the k=1 existence
tiebreaker from §2.**

Reasoning grounded in the test contract + callers:

1. **The `candidate.exists()` branch is the root cause, not a safety net.** The found/missing
   asymmetry (grounding.md:23-27) exists *only because* the selector at line 89 is a cwd-relative
   probe: present file → line 92 (correct), absent file → line 94 (doubled). Fix A keeps that probe,
   so it keeps a cwd-dependent, non-deterministic selector whose behavior changes with the process's
   working directory. That is a latent defect even after de-doubling — any future caller invoked from
   a different cwd re-opens the same class of bug.

2. **The branch is dead under the current test suite** (§3): every existing relative test runs with
   cwd ≠ tmp_path → `candidate.exists()` is always False → the suite never validates the True arm.
   Keeping an untested, cwd-sensitive branch (Fix A) is strictly more surface for no proven benefit.

3. **All four callers pass the bundle/release root** (§4), so the lexical overlap-strip is sufficient
   on its own — no caller needs the existence probe to disambiguate a non-root `release_dir`. Fix B
   loses nothing the callers rely on.

4. **Determinism + idempotence:** Fix B makes resolution a pure function of `(raw_path, release_dir)`
   for every relative shape (S2,S4,S5,S8,S10,S11 all correct without disk access). The single residual
   ambiguity (S7/S9, single-segment overlap) is the *only* place a disk check earns its keep, and the
   §2 guard scopes that check to exactly k=1 — far narrower than Fix A's blanket cwd probe on every
   relative path.

**Net:** Fix B + k=1-guard removes the cwd-dependence that caused the bug, passes the entire existing
suite (§3), satisfies all callers (§4), and the discriminating over-strip test (§5) gates the guard.
Fix A is *acceptable* (also de-doubles, also passes existing tests) but is **strictly higher-risk**:
it preserves the cwd-sensitive selector that is both the original root cause and untested.

**One caveat on Fix B:** removing `candidate.exists()` means a declared path that is *genuinely*
intended as cwd-relative-and-already-correct (e.g. an agent that wrote the file at a cwd-relative
location and declared it the same way) would now be re-anchored under `release_dir`. No caller or test
exhibits this pattern (§3, §4), and the module docstring (checkpoints.py:49-51) states relative paths
*are* resolved against `release_dir` by design — so this is a contract alignment, not a regression.
Confirm no agent prompt instructs writing checkpoints cwd-relative-to-process before merging. [INFERENTIAL]

---

## Evidence index (file:line / test:asserted-value)

- Defect site: `checkpoints.py:86-94`; doubling site line 94.
- TASKLIST_ROOT strip: `checkpoints.py:77-80`.
- On-disk doubled path: `.dev/e2e-reflect/tl-1/bundle/manifest.json` P02 `expected_path` (segment `.dev/e2e-reflect/tl-1/bundle` ×2).
- Declared prefixed path: `phase-2-tasklist.md:134`.
- release_dir = bundle root: manifest P01 `expected_path` (single, correct) confirms anchor.
- Callers: `commands.py:694`, `executor.py:2201`, `executor.py:2457`, `checkpoints.py:161`.
- release_dir provenance: `config.py:242-278` (`_resolve_release_dir`), `config.py:351`.
- Existing-test cwd≠tmp_path → exists()=False: grounding.md:42 + CliRunner isolation reasoning.
- Absolute verbatim contract: `test_absolute_path_preserved` (line 79) asserts `Path("/abs/checkpoints/CP.md")` unresolved.
- Bare-relative resolve contract: `test_single_checkpoint_backticks` (line 63) asserts `(tmp_path/"checkpoints"/"CP-P01-END.md").resolve()`.
