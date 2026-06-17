# QA Report — Phase Gate 4 (WS-B Parity Gate): Deletion-Survivability Lens

**Topic:** Does the rebuilt CLI-vs-frozen-golden parity gate survive WS-C's deletion of `t2_normalize.py`?
**Date:** 2026-06-16
**Phase:** report-validation (structural, deletion-survivability lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE (report-only)
**Target:** `tests/swarm/test_bare_review_parity.py`

---

## Overall Verdict: PASS

The rebuilt gate has **zero executable runtime references** to the legacy `t2_normalize.py` script or any `scripts/t2_*` path. Every `t2_`-family match in the file is benign docstring/comment prose documenting the byte-faithful-port lineage. The gate was empirically proven to keep asserting (16 passed, 0 skipped) with the legacy script physically removed.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No `pytestmark` whole-module skipif guard keyed on `LEGACY_SCRIPT.exists()` | PASS | `grep -nE 'pytestmark\|skipif\|\.skip\|mark\.skip'` on the file returns EXIT:1 (zero matches). There is no module-level `pytestmark` at all, and no `skipif`/`skip` anywhere in the file. |
| 2 | No `importlib` load of `t2_normalize.py` (`_load_legacy`, `spec_from_file_location`, `module_from_spec`) | PASS | `grep -nE 'importlib\|spec_from_file_location\|_load_legacy\|module_from_spec'` returns EXIT:1 (zero matches). The import block (lines 49-63) imports only `pathlib`, `typing`, `pytest`, `yaml`, `click.testing.CliRunner`, and 6 `superclaude.cli.swarm.*` symbols — none load the legacy script. |
| 3 | No runtime dependency on `scripts/t2_*` or a `LEGACY_SCRIPT` constant in executable code | PASS | `grep` for `LEGACY_SCRIPT` = zero matches. `grep -nE 'scripts/'` returns one match (line 46) which is inside the module docstring. No constant named `LEGACY_SCRIPT` is defined or used. The only path constants are `FIXTURES_DIR`/`GOLDEN_DIR`/`TARGET_FIXTURE` (lines 70-72), all pointing at the committed frozen golden tree, not the legacy script. |
| 4 | Classify every `t2_` / `LEGACY_SCRIPT` / `skipif` / `importlib` match as (a) benign prose or (b) executable runtime ref | PASS | 4 `t2_` matches found, all (a) benign prose (see classification table below). 0 matches for the other three patterns. |
| 5 | Gate keeps asserting after WS-C deletes `t2_normalize.py` | PASS | Hard empirical proof: temporarily renamed both `src/.../scripts/t2_normalize.py` and `.claude/.../scripts/t2_normalize.py` out of the way, re-ran the gate → **16 passed, 0 skipped** (`-rs` showed no skip reasons), then restored both files. Also: the live CLI path the gate drives (`bare_review_v1.py` recipe + `commands.py`) references the legacy script only in comments, never via `importlib`/file-read. |

## Grep Evidence — the 4 `t2_` matches (all benign docstring prose)

All four matches fall within the module docstring (lines 1-47). Each is classified **(a) benign comment/prose** — NOT executable:

| Line | Matching text | Classification |
|------|---------------|----------------|
| 13 | `` ``t2_normalize.py`` aggregator at run time and self-skipped once that script was `` | (a) benign — docstring describing the OLD gate's behavior the rebuild removed |
| 15 | `` script at run time**, so it survives WS-C's deletion of ``t2_normalize.py``. The `` | (a) benign — docstring stating the survivability claim being verified |
| 19 | `` port of legacy ``t2_normalize``, the frozen golden equals what the live CLI `` | (a) benign — docstring describing port lineage |
| 46 | `` tokens. No reference to ``t2_normalize.py`` or any ``scripts/t2_*`` path. `` | (a) benign — docstring asserting absence of legacy coupling |

`importlib`: 0 matches. `LEGACY_SCRIPT`: 0 matches. `skipif`/`pytestmark`/`skip`: 0 matches.

## Transitive (live-CLI-path) check

The gate drives the real CLI, which exercises `superclaude.cli.swarm.recipes.bare_review_v1` and `superclaude.cli.swarm.commands`. Both contain `t2_normalize` strings — verified to be comment/docstring-only lineage notes, NOT runtime script loads:

- `recipes/bare_review_v1.py`: lines 4, 89, 105, 217 — all comments/docstrings ("mirror t2_normalize.py verbatim (byte-identity parity)", module-path reference in a docstring). No `importlib`, no `spec_from_file`, no `scripts/` file read.
- `commands.py:1847`: comment `# ... Mirrors legacy t2_normalize.py:293-295: compare =` — a provenance comment, not executable.

The recipe is a self-contained byte-faithful port; the legacy script is not on the import or execution path.

## Note on legacy-script location

The prompt referenced `scripts/t2_normalize.py`; the script actually lives at `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py` (with a sync-dev mirror at `.claude/.../scripts/t2_normalize.py`). It is NOT under a top-level `scripts/` dir (that dir has no `t2_*` files). This does not affect the verdict — the simplified `scripts/t2_*` phrasing in the file's docstring is itself benign prose, and the deletion-survivability proof renamed the real source + dev-mirror paths.

## Empirical deletion-survivability proof (definitive)

```
# moved out:  src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py
# moved out:  .claude/skills/sc-bare-review/scripts/t2_normalize.py
$ uv run pytest tests/swarm/test_bare_review_parity.py -q -rs
collected 16 items
................                                                  [100%]
16 passed in 0.35s
# both files restored, confirmed present again
```

No skip, no collection error, no silent death. The adversarial hypothesis — "this gate still silently dies when t2_normalize.py is deleted" — is **disproven**.

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None.

## Confidence
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 (run via Bash) | Glob: 0 | Bash: 6
- Note: greps executed via Bash (`grep -nE`) for line-numbered evidence + an empirical deletion+rerun proof; Bash count (6) exceeds the 5 checklist items, satisfying the tool-engagement minimum. Each Bash call mapped to a specific check (grep classification, import enumeration, legacy-script locate, baseline run, transitive-dep grep, delete-and-rerun proof).

## Recommendations
None blocking. The gate is deletion-survivable and ready for WS-C to remove `t2_normalize.py`. Optional cosmetic-only follow-up (NOT a defect): the docstring's `scripts/t2_*` phrasing (line 46) refers to the script by a simplified path; the real path is `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`. Harmless since it is prose asserting absence-of-coupling.

## QA Complete
