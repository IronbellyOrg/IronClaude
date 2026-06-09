# Tier 2 — Fix B (PRINCIPLED / cwd-independent)

**Bug:** verify-checkpoints path-doubling
**File:** `src/superclaude/cli/sprint/checkpoints.py` → `extract_checkpoint_paths` (lines 40–98)
**Stance:** Remove the cwd-relative `candidate.exists()` selector; resolve every relative path
deterministically against `release_dir` with an idempotent overlap-strip join.

---

## 1. ROOT CAUSE confirmation

The resolution selector at **`checkpoints.py:89`** (`elif candidate.exists():`) branches on the
**process cwd + on-disk presence**, not on the structure of the declared path. This produces a
found/missing asymmetry:

- **`checkpoints.py:89` → `:92`** (`resolved = candidate.resolve()`): taken when the
  release-prefixed relative path *happens to already exist relative to cwd* (e.g. CP-P01 present on
  disk, run from worktree root) → resolves correctly, **no doubling**.
- **`checkpoints.py:94`** (`resolved = (release_dir / candidate).resolve()`): taken when the same
  declared path is **absent** (CP-P02 not yet written) → `release_dir / candidate`. When
  `release_dir` already *ends with* the leading components of `candidate`
  (`release_dir = …/.dev/e2e-reflect/tl-1/bundle`, `candidate = .dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md`),
  the segment is **re-nested** → the doubled manifest path in `grounding.md:7-9`.

So `:94` is the doubling *site*, but the true root cause is that **`:89` lets two structurally
identical paths take two different branches purely because of disk state.** A path's resolution must
not depend on whether the target file exists yet — checkpoint verification runs precisely *before*
the file is guaranteed present.

---

## 2. EXACT proposed code (copy-pasteable)

Replace lines **86–94** (the `candidate = Path(raw_path)` block through the `else` join) with:

```python
        candidate = Path(raw_path)
        if candidate.is_absolute():
            resolved = candidate
        else:
            # Resolve every relative path deterministically against release_dir,
            # independent of process cwd and of whether the target exists yet.
            # Idempotent join: if the declared relative path is already prefixed
            # with release_dir's trailing components (a release-anchored path),
            # strip that overlap so the shared segment is not re-nested.
            base_parts = release_dir.parts
            rel_parts = candidate.parts
            overlap = 0
            for k in range(min(len(base_parts), len(rel_parts)), 0, -1):
                if base_parts[-k:] == rel_parts[:k]:
                    overlap = k
                    break
            remainder = rel_parts[overlap:]
            resolved = (
                release_dir.joinpath(*remainder).resolve()
                if remainder
                else release_dir.resolve()
            )
```

Unchanged above this block: the `TASKLIST_ROOT/` strip (`:77-80`) and the heading-name derivation
(`:82-84`). The absolute passthrough is preserved (now the single `if` arm). The `elif
candidate.exists()` arm and its cwd-relative `candidate.resolve()` are **deleted**.

**Why longest-overlap-first:** iterating `k` from `min(len(base),len(rel))` down to `1` and taking
the first match strips the *maximal* shared suffix/prefix. This is what makes the join idempotent
against a fully release-prefixed path while leaving a bare `checkpoints/CP.md` (no overlap with
`release_dir`'s tail) untouched.

---

## 3. Walkthrough (resolved paths under Fix B)

Verified by executing the exact algorithm (see §6 test; results reproduced below).

| Case | Input `raw_path` | `release_dir` | Resolved |
|---|---|---|---|
| (a) | `/abs/checkpoints/CP.md` | `tmp_path` | `/abs/checkpoints/CP.md` (absolute arm, verbatim) |
| (b) | `checkpoints/CP-P01-END.md` | `tmp_path` | `tmp_path/checkpoints/CP-P01-END.md` (no overlap → plain join) |
| (c) | `.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md` (file **absent**) | `/W/.dev/e2e-reflect/tl-1/bundle` | `/W/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md` — overlap=4 stripped, **no doubling** |
| (d) | `.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P01-END.md` (file **present**) | `/W/.dev/e2e-reflect/tl-1/bundle` | `/W/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P01-END.md` — identical to (c); existence is now irrelevant |
| (e) | `TASKLIST_ROOT/checkpoints/CP.md` | `tmp_path` | `tmp_path/checkpoints/CP.md` (`TASKLIST_ROOT/` stripped first → bare join) |

**Key result:** (c) and (d) resolve **identically** — the found/missing asymmetry is eliminated.
Under today's code (d) takes `:92` (correct by luck) and (c) takes `:94` (doubled). Under Fix B both
take the same deterministic path. This is the entire point of the fix.

---

## 4. No regression of existing tests (`test_checkpoints.py:53-125`)

These tests run with cwd = repo root (≠ `tmp_path`), so under today's code `candidate.exists()` is
False and they hit `:94` (`release_dir / candidate`). Fix B's no-overlap branch produces the **same
`(release_dir / candidate).resolve()`** for every bare-relative input, because `tmp_path`'s trailing
component (a pytest temp dir name) never overlaps a `checkpoints/…` prefix → `overlap == 0` →
`release_dir.joinpath(*rel_parts)`. Verdicts:

| Test (line) | Input shape | Assertion | Fix B |
|---|---|---|---|
| `test_zero_checkpoints` (48) | none | `== []` | **PASS** (no path code reached) |
| `test_single_checkpoint_backticks` (53) | `checkpoints/CP-P01-END.md` | `== tmp_path/checkpoints/CP-P01-END.md` | **PASS** (overlap=0) |
| `test_two_checkpoints_mixed_formats` (65) | two bare relatives | names list | **PASS** (names untouched; paths bare-join) |
| `test_absolute_path_preserved` (79) | `/abs/checkpoints/CP.md` | `== Path("/abs/checkpoints/CP.md")` | **PASS** (absolute arm verbatim) |
| `test_name_falls_back_to_basename` (87) | bare relative, no heading | name `== CP-P01-END.md` | **PASS** (name logic at `:82-84` unchanged) |
| `test_missing_phase_file_returns_empty` (94) | unreadable file | `== []` | **PASS** (early return at `:59`) |
| `test_wave4_numbered_checkpoint_task_form` (97) | bare relative | name + `== tmp_path/checkpoints/CP-P01-END.md` | **PASS** (overlap=0) |
| `test_wave4_mid_and_end_mixed_with_legacy` (111) | two bare relatives | names list | **PASS** |

Downstream contract tests that depend on this resolution also hold: `TestBuildManifest`
(`:323-355`), `TestWriteManifest`, `TestRecoverMissingCheckpoints`, `TestVerifyCheckpointsCLI`,
`TestVerifyCheckpointsGate` all seed bare-relative `checkpoints/CP-*.md` against `tmp_path` →
overlap=0 → byte-identical resolution to today. **No existing assertion changes.**

---

## 5. Honest trade-off — the ONE behavior-changing scenario

Removing `:89` changes behavior in **exactly one** scenario: a declared **relative** path that
**exists relative to the current process cwd** but where that cwd-relative location **differs from
`release_dir`-relative location**. Today `:89→:92` picks the cwd-relative file; Fix B always picks
the `release_dir`-relative location.

Concretely this is the "sprint agent invoked from inside the release dir, wrote `checkpoints/CP.md`
relative to cwd" pattern that the `:90-91` comment claims to support ("repo-root invocations,
matching how sprint agents write checkpoint files").

**Judgment — is it load-bearing?** No, and here is why I am not hedging:
- The function's own docstring (`:48-51`) states relative paths are resolved **against
  `release_dir`** — `:89` *contradicts* the documented contract. Fix B restores it.
- The only cases where cwd-relative and release-relative coincide (the common, working case —
  `live-tl` in `grounding.md:9`) are invocations where **cwd == release_dir**; for those Fix B's
  overlap-strip yields the *same* path, so nothing changes.
- The cases where they *diverge* are precisely the buggy ones (`grounding.md:23-28`): the e2e runs
  errored because divergence + absence produced doubling. The "feature" at `:89` is the bug's
  enabler, not a supported configuration.
- There is **no test** exercising the cwd-relative-resolves arm (confirmed: every test runs from
  repo root with `tmp_path` release_dir, so `:89` is always False — `grounding.md:42`). An
  undocumented, untested branch that contradicts the docstring is dead-weight, not load-bearing.

**One residual caveat (favoring honesty over advocacy):** the overlap-strip has a *theoretical*
collision — if `release_dir` legitimately ends with the same directory name that a bare relative
path legitimately begins with (e.g. `release_dir=/proj/checkpoints`, declared
`checkpoints/CP.md` meaning `/proj/checkpoints/checkpoints/CP.md`), the strip collapses it to
`/proj/checkpoints/CP.md`. I verified this collapses (see §6 `edge overlap` assertion). **In this
codebase that collision cannot occur**: `release_dir` is the sprint OUTPUT_DIR / bundle root
(`grounding.md:30-34`), and checkpoints live in a `checkpoints/` *subdir* of it — a release dir
literally named `checkpoints` nested under another `checkpoints/` is not a produced layout. If that
assumption is ever violated, **Fix A (conservative: gate the overlap-strip behind an
`is-already-release-prefixed` check rather than a blanket longest-overlap)** is the safer choice. I
judge the collision non-real for the supported configuration, so Fix B stands — but this is the
single point where Fix A would win.

---

## 6. Regression test (pytest)

Add to `TestExtractCheckpointPaths` in `tests/sprint/test_checkpoints.py`:

```python
    def test_release_prefixed_relative_path_not_doubled(self, tmp_path: Path):
        """Path-doubling regression: a phase tasklist that declares a
        release-PREFIXED relative `Checkpoint Report Path:` must resolve WITHOUT
        re-nesting release_dir's trailing segments — even when the target file is
        ABSENT (the missing-branch that previously hit `release_dir / candidate`
        and doubled). Resolution must not depend on process cwd or disk presence.
        """
        # release_dir ends with the exact prefix the declared path is anchored on.
        release_dir = tmp_path / ".dev" / "e2e-reflect" / "tl-1" / "bundle"
        release_dir.mkdir(parents=True)
        rel = ".dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md"  # file absent
        phase_file = release_dir / "phase-2-tasklist.md"
        phase_file.write_text(
            "### Checkpoint: End of Phase 2\n"
            f"Checkpoint Report Path: {rel}\n"
        )

        result = extract_checkpoint_paths(phase_file, release_dir)
        assert len(result) == 1
        _, path = result[0]
        expected = (release_dir / "checkpoints" / "CP-P02-END.md").resolve()
        assert path == expected, f"doubled: {path}"
        # No release segment appears twice.
        assert str(path).count("/.dev/e2e-reflect/tl-1/bundle/") == 1

    def test_release_prefixed_resolves_same_present_or_absent(self, tmp_path: Path):
        """The found/missing asymmetry is gone: a present checkpoint and an absent
        one declared with the same release-prefixed anchor resolve identically."""
        release_dir = tmp_path / ".dev" / "e2e-reflect" / "tl-1" / "bundle"
        (release_dir / "checkpoints").mkdir(parents=True)
        # CP-P01 present on disk, CP-P02 absent — same anchor.
        (release_dir / "checkpoints" / "CP-P01-END.md").write_text("ok")
        phase_file = release_dir / "phase-1-tasklist.md"
        phase_file.write_text(
            "### Checkpoint: P1\n"
            ".dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P01-END.md".join(
                ("Checkpoint Report Path: ", "\n")
            )
            + "### Checkpoint: P2\n"
            "Checkpoint Report Path: "
            ".dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md\n"
        )
        results = extract_checkpoint_paths(phase_file, release_dir)
        resolved = {p.name: p for _, p in results}
        assert resolved["CP-P01-END.md"] == (
            release_dir / "checkpoints" / "CP-P01-END.md"
        ).resolve()
        assert resolved["CP-P02-END.md"] == (
            release_dir / "checkpoints" / "CP-P02-END.md"
        ).resolve()
```

Run: `uv run pytest tests/sprint/test_checkpoints.py -q` (UV-only per project rules).

**Pre-fix:** `test_release_prefixed_relative_path_not_doubled` FAILS — from repo-root cwd the absent
path hits `:94` and doubles. **Post-fix:** PASS. I validated the resolution algorithm out-of-band
(executed the exact overlap-strip logic): cases (a)-(e) and both contract checks
(`bare single`, `abs`) returned the expected paths, and the `edge overlap` collapse was confirmed
(the §5 caveat).

---

## 7. RISKS + "if I'm wrong it's probably because…"

**Risks:**
- **R1 (the §5 collision).** A legitimately `checkpoints`-named release dir would get its
  bare-relative `checkpoints/…` over-stripped. Judged non-real for this codebase's produced layouts;
  if violated, switch to Fix A. **Severity: low, mitigation known.**
- **R2 — partial-overlap false positive.** Longest-overlap-first means a path sharing only its
  *first* component with release_dir's *last* component triggers a strip. Mitigated by requiring the
  contiguous run to match from `k` downward (a single accidental shared dir name = `k=1` strip only,
  and only when `base[-1]==rel[0]`). Real declared paths are either bare (`checkpoints/…`, no
  collision with a non-`checkpoints` release dir) or fully prefixed (clean `overlap==N`). **Low.**
- **R3 — callers passing a *non-canonical* release_dir** (e.g. with a trailing `.` or symlink) could
  shift `release_dir.parts`. Today's `:94` has the identical exposure (`release_dir / candidate`),
  so Fix B does not *add* risk here; both are equally subject to caller hygiene. **Neutral.**

**If I'm wrong it's probably because…**
- …the `:89` cwd-relative arm IS load-bearing for a real invocation mode I can't see in-repo — e.g.
  a sprint agent that genuinely runs from a cwd *different* from `release_dir` and writes checkpoints
  relative to *that* cwd, relying on `:92` to find them. The absence of any test or doc for this
  (and the docstring saying the opposite at `:48-51`) is my evidence it doesn't exist — but the
  branch comment at `:90-91` asserts it does. If that comment reflects a real production path, Fix A
  (keep `:89`, only de-double the `:94` join) is correct instead, and Fix B would regress those
  agents from "found via cwd" to "looked for under release_dir."
- …`release_dir` is sometimes passed *already* containing a trailing `checkpoints` segment by a
  caller I didn't trace (`commands.py:694`, `executor.py:2457/2201` per `grounding.md:30-34` all
  pass the bundle/OUTPUT_DIR root, which argues against this) — that would activate R1 in practice.
