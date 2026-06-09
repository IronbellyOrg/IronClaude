# Grounding — verify-checkpoints path-doubling

## Defect
`extract_checkpoint_paths` in `src/superclaude/cli/sprint/checkpoints.py` (lines 40-98) doubles a
checkpoint path when a phase tasklist declares a **release-prefixed relative** `Checkpoint Report Path:`.

On-disk evidence: `.dev/e2e-reflect/tl-1/bundle/manifest.json` records
`.../ReflectInTaskLists/.dev/e2e-reflect/tl-1/bundle/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md`
— the segment `.dev/e2e-reflect/tl-1/bundle/` appears twice. tl-1/tl-2 e2e runs errored ~6ms; `live-tl` (correct paths) succeeded.

## The function (current HEAD, checkpoints.py:86-96)
```python
candidate = Path(raw_path)
if candidate.is_absolute():
    resolved = candidate
elif candidate.exists():                 # line 89 — cwd-relative existence probe
    resolved = candidate.resolve()       # line 92
else:
    resolved = (release_dir / candidate).resolve()   # line 94 — DOUBLING SITE
```
Preceding (lines 77-80): `TASKLIST_ROOT/` prefix is stripped to release-relative; `TASKLIST_ROOT` alone → `.`.

## Why the found/missing asymmetry
The branch selector at line 89 is `candidate.exists()` (cwd-relative). For a release-prefixed declared path
like `.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P0X-END.md` run from the worktree root:
- CP-P01 (file present on disk) → `exists()`→True → line 92 → correct (no doubling).
- CP-P02 (file absent) → `exists()`→False → line 94 → `release_dir / candidate` → DOUBLED (release_dir already ends with `.dev/e2e-reflect/tl-1/bundle`).

## release_dir provenance / callers
- `commands.py:694` `build_manifest(index_path, output_dir)` → release_dir = the verify-checkpoints OUTPUT_DIR positional.
- `commands.py:161` `extract_checkpoint_paths(phase.file, release_dir)` inside build_manifest.
- `executor.py:2457` `extract_checkpoint_paths(phase.file, config.release_dir)` (in-executor scan).
- `executor.py:2201` `build_manifest(config.index_path, config.release_dir)`.
In the e2e case OUTPUT_DIR == bundle == `.dev/e2e-reflect/tl-1/bundle`, and the phase tasklist's declared
checkpoint path is `.dev/e2e-reflect/tl-1/bundle/checkpoints/...` (same anchor) → overlap.

## Existing test contract (tests/sprint/test_checkpoints.py, TestExtractCheckpointPaths 47-125)
All existing tests pass `tmp_path` as `release_dir` and use either:
- bare release-relative `checkpoints/CP-*.md` → assert resolved == `(tmp_path / "checkpoints" / "CP-*.md").resolve()`
- absolute `/abs/checkpoints/CP.md` → asserted preserved verbatim
None use a release-PREFIXED relative path. So no existing test exercises the bug case.
These tests run with cwd = repo root (≠ tmp_path) so `candidate.exists()` is False → they currently hit line 94.

## Fix goal
Make resolution idempotent against an already-release-prefixed relative path; stop depending on
cwd-relative `candidate.exists()` as the selector. Preserve: absolute passthrough, `TASKLIST_ROOT/`
stripping, and bare release-relative join (the existing-test contract). Add a regression test:
release-prefixed `Checkpoint Report Path:` + absent target file → resolved path has NO duplicated release_dir segment.
UV-only tests: `uv run pytest tests/sprint/ -q`.
