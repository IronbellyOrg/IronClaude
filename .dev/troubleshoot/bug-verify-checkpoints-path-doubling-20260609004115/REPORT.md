---
status: partial
tier_reached: 2
confidence: 0.9
---

# Troubleshoot REPORT — verify-checkpoints path-doubling

**Target:** `extract_checkpoint_paths` in `src/superclaude/cli/sprint/checkpoints.py`
**Mode:** `--depth deep --fix` · Tier 2 (3 parallel hypothesis agents + orchestrator adjudication)
**Status:** `partial` — fix applied + unit-verified, BUT a parallel session switched the working
directory to the wrong branch mid-run, so full-suite regression certification is deferred (see Caveat).

## Summary

`extract_checkpoint_paths` doubled a checkpoint path when a phase tasklist declared a **release-prefixed
relative** `Checkpoint Report Path:` (e.g. `.dev/<release>/bundle/checkpoints/CP.md`) and the target file
was absent. Root cause: the `else` branch joined `release_dir / candidate` even though `candidate` already
carried `release_dir`'s trailing segments, and the branch selector `candidate.exists()` was cwd-relative —
so a present checkpoint resolved correctly while an absent one doubled (the "found 1 / missing 1" asymmetry).

## Diagnosis (chosen hypothesis — Fix B, adjudicated)

Three independent agents (root-cause-analyst, refactoring-expert, quality-engineer) converged on the same
mechanism (lexical longest-overlap idempotent join). The quality-engineer (skeptic) adjudicated for **Fix B**
(remove the cwd-dependent `exists()` selector) over Fix A (keep it): the `exists()` True-arm is dead under
test, contradicts the function docstring ("resolved against release_dir"), and is the source of the
cwd-sensitivity. The theoretical over-strip hazard (a checkpoint path whose leading segment coincidentally
equals `release_dir.name`) is unreachable — no checkpoint generator emits that shape.

## Evidence (grounded)

- Doubling site: `checkpoints/checkpoints.py:94` (pre-fix) `resolved = (release_dir / candidate).resolve()`.
- Asymmetry selector: `checkpoints.py:89` (pre-fix) `elif candidate.exists():`.
- On-disk proof: `.dev/e2e-reflect/tl-1/bundle/manifest.json` records the doubled
  `.../bundle/.dev/e2e-reflect/tl-1/bundle/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md`.
- Callers verified safe (all pass the bundle/release root): `commands.py:694`, `executor.py:2201`, `executor.py:2457`, `checkpoints.py:161`.
- Existing-test contract preserved: all bare-relative + absolute tests unchanged.

## Fix applied

`checkpoints.py`: added `_resolve_checkpoint_path(release_dir, raw_path)` — a purely lexical, cwd-independent
resolver that (1) passes absolutes through, (2) strips the longest leading run of `candidate` matching
`release_dir`'s trailing parts (idempotent — release-prefixed paths no longer double), (3) joins the
remainder onto `release_dir`. Replaced the old `is_absolute / exists / else` block with a call to it.
3 regression tests added to `tests/sprint/test_checkpoints.py::TestExtractCheckpointPaths`.

Saved as recoverable patch: `path-doubling-fix.patch` (this dir).

## Verification

- `TestExtractCheckpointPaths`: **11 passed** (8 existing + 3 new), 0.25s.
- e2e attribution: `tests/sprint/e2e_real/` group **18 passed**; checkpoint tests + `test_e2e_resume` together **44 passed**; `test_e2e_resume` in isolation **passed**.
- One full-suite run showed `test_e2e_resume` failing, but it passes in isolation, in its group, and adjacent
  to the checkpoint tests → an **ordering-dependent flake from an unrelated earlier test**, not this fix.

## Caveat (why status=partial)

A **parallel session** sharing this single working directory ran `git checkout` at 00:47:19, switching from
`fix/sprint-recovery-...` @ 563464f2 (correct base, has FIX-2) to `fix/prd-local-file-no-session-token` @
ac80f176 (lacks FIX-2). My uncommitted fix is now sitting on the wrong branch/base, and full-suite runs were
on a shifting base. The fix is unit-verified and correct, but **regression certification on the correct base
(563464f2) and the commit are deferred** pending resolution of the shared-directory conflict (recommend a
git worktree per the project's parallel-session rule). My rebased branch 563464f2 is intact; nothing lost.

## Next steps

1. Resolve the shared-working-dir conflict (worktree, or pause the other session).
2. Re-home the fix onto `fix/sprint-recovery-...` @ 563464f2 (the sprint-recovery line where it belongs) via
   `path-doubling-fix.patch` or `git checkout` carry.
3. Re-run `uv run pytest tests/sprint/ -q` on that base to certify 0 regressions, then commit.
