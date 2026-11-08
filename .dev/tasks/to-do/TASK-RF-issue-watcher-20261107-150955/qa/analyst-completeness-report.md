# Research Completeness Verification (completeness lens)

**Topic:** implement `superclaude issue-watch` exactly as designed in `docs/designs/issue-watcher.md`
**Date:** 2026-11-07
**Analysis type:** completeness-verification (breadth, not depth)
**Files analyzed:** 5 research files plus `research-notes.md` (01-cli-package-conventions, 02-integration-points-and-citation-check, 03-test-and-verification, 04-template-and-examples, 05-work-breakdown)
**Compared against:** design sections 11 (files), 12 (tests), 13 (gates), 17 (acceptance criteria), read directly from `docs/designs/issue-watcher.md`
**Depth tier:** Standard

---

## Verdict: see end of file (appended last)

## Part 1. Nine-point coverage checklist

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Source files identified with paths and exports | PASS | 01 F8 table lists all 9 package modules plus `main.py` with exports, allowed imports, repo precedent and test file. 05 sections 1.0 to 1.9 give a public API per module (stated vs derived). Reused helpers (`write_prepared_bytes`, `_ORCA_CLIS`, `_find_orca`, `parse_origin_url`) have exact signatures and import-or-copy rulings in 02 section E. |
| 2 | Output paths and formats clear or inferable | PASS | New-file paths come from design section 11 and are repeated in 01 F8, 05 section 1 and section 3. The test output convention (raw `.txt` plus summary `.md` under `phase-outputs/test-results/`) is in 04 C.3 and A.9. The task file id and folder are inferable from 04 B.1. `_assumed_shape` fixture names are not in the design; 05 section 3 proposes them (flagged as G-15). |
| 3 | Logical breakdown of phases and steps | PASS | 05 section 1 gives a dependency-ordered build (orders 0 to 10). 05 section 6 gives a 10-phase plan with a checkpoint per phase and 8 final gates. 04 Part D gives the QA-gate placement. |
| 4 | Patterns and conventions with examples | PASS | 01 F1 to F6 give registration text, Click group style, exit-code idioms, `from __future__` counts, Protocol style, and ruff and arch_lint rules. 03 section 3 quotes the PATH-stub pattern. 03 section 7 gives recipes for each cross-cutting test, each with a repo precedent. |
| 5 | MDTM template notes with rule references | PASS | 04 Part A cites T02 line numbers (A3, B2 to B5, C, D3, E, F, I11 to I22, J, K, L1 to L7, M2 to M4). Part B cites the builder-side rules (TB-Add-1, 3 to 8, `reflect_post_mode: skill`, the POST item, anti-orphaning, TCS) with SKILL and RFQA line numbers. Part E is a validator pitfall list. |
| 6 | Granularity for one checklist item per module and per test file | PASS | 9 modules plus the `main.py` edit are each a distinct row in 01 F8 and 05 sections 1.0 to 1.9. All 19 design test files have their own row in 05 sections 2.1 and 2.2, each with assertions and fakes. conftest is split into 6 increments (05 section 3). Stubs, fixtures and the setup runbook (15-section outline, 05 section 4) are separate rows. |
| 7 | Doc-sourced claims tagged | PASS with minor format deviation | 01 and 02 tag with `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]` and `[UNVERIFIED]`. 02 covers all 23 section-3 rows (C1 to C22, S1), plus 14 citations outside section 3 (X1 to X14), plus the section-15 table. 02 section H tallies 45 / 3 / 8. 03 section 9 uses HOLDS and PARTLY instead of the tags (same information, other vocabulary). 05 derives from the design and tags with "stated", "derived" and "UNVERIFIED", not the three tags. No `[CODE-CONTRADICTED]` claim is reported as current fact. |
| 8 | Design and solution choices evaluated | PASS | The design is binding, so research evaluates the gaps instead: 02 section G (G1 to G15) and 05 section 5.1 (X1 to X15) and Gaps (G-01 to G-21) give a treatment for each. 04 Part E lists five template-rule conflicts for the builder to adjudicate. |
| 9 | Unresolved ambiguities documented | PASS with caveats | Documented in 02 G, 03 Gaps, 04 Gaps and 05 Gaps. Caveat: `research-notes.md` still says `AMBIGUITIES_FOR_USER: None`, although the research found high-severity decisions (see IMP-1, MIN-1). |

## Part 2. Coverage against design sections 11, 12, 13, 17

### Section 11 (files to create or change): 17 of 17 rows covered

| Design row | Covered in |
|---|---|
| `issue_watch/__init__.py` | 01 F8 #1; 05 1.0 |
| `runner.py` | 01 F8 #2; 05 1.1 |
| `github.py` | 01 F8 #5; 05 1.4 |
| `predicates.py` | 01 F8 #3; 05 1.2 |
| `record.py` | 01 F8 #6; 05 1.5 |
| `launch.py` | 01 F8 #7; 05 1.6; 02 section E |
| `audit.py` | 01 F8 #4; 05 1.3 |
| `cycle.py` | 01 F8 #8; 05 1.7 |
| `cli.py` | 01 F8 #9; 05 1.8; 01 F2 |
| `main.py` two lines | 01 F1 (exact text and line numbers); 02 X3; 05 1.9 |
| `tests/issue_watch/__init__.py`, `conftest.py` | 01 F4; 02 C14; 03 sections 2.1 and 4; 05 1.0 and section 3 |
| 8 per-module test files | 05 2.1 (one row each) |
| 11 cross-cutting test files | 05 2.2 (one row each); 03 section 7 gives recipes |
| `fixtures/_assumed_shape/*.json` | 05 section 3 (proposed names); 02 section D |
| `stubs/gh`, `stubs/orca` | 03 section 3; 02 G5; 05 3.8 and T-J |
| `docs/designs/issue-watcher-setup.md` | 05 section 4 |
| "Not changed" list (`pyproject.toml`, Makefile, CI, `.claude/`) | 04 C.2 (no-change verify item); 05 final gate 7 |

### Section 12 (tests): 8 of 8 named tests covered, 5 of 5 seams covered

`test_crash_injection` (03 section 7.4; 05 2.2), `test_concurrency` (03 7.3), `test_cycle::test_fifty_cycles` and `::test_acceptance_property` (05 2.1), `test_no_shell` (03 7.2), `test_no_text` (03 7.7), `test_module_boundaries` (03 7.1), `test_marker_contract` (02 section F, 03 7.8). Seams: `FakeRunner`, `FakeClock`, `FakeLauncher`, `CrashingStore` and the PATH stubs all appear in 05 section 3 steps 3.2 to 3.9.

### Section 13 (gates): 7 of 7 covered

`uv run pytest tests/issue_watch/ -v`, `make test`, `make lint`, `uv run ruff format --check src/ tests/`, `make verify-deps`, `make verify-sync` and `make sync-dev` are all in 03 section 6 (with measured behavior and caveats) and 05 section 6 (final gate list). Python 3.10 floor: 03 section 5, 02 section A, 05 T-A.

### Section 17 (acceptance criteria): 25 of 25 covered

AC-1 to AC-25 each map to a test file in 03 section 8 and to FR and NFR ids in 05 section 5. AC-23 (no new dependency, gates pass) is gate-only in both files, which agrees with the design. No criterion lacks a home.

**Files, tests, gates or criteria with no research coverage: none.**

## Part 3. Contradictions and integration seams between the research files

These are surfaced, not resolved. Each has a documented source on both sides, so the builder can adjudicate without more research.

| # | Topic | File A says | File B says | Needed |
|---|---|---|---|---|
| K1 | Number of verbs | 01 F2: the design's "six verbs" are five Click commands (`reset` is one command with two forms) | 05 1.8 (`test_cli`: "help lists six verbs") and 05 P8 checkpoint (`--help` lists six verbs). The design itself says "six verbs" at section 11 line 759 | Builder writes "five commands" in any `--help` check; a "lists six verbs" check cannot pass |
| K2 | `property_based` marker | 05 2.2: `test_prompt_regex_property` "tagged `property_based`" | 03 7.6: do not tag (marker text names hypothesis). Design C12 only says it "may" tag | Builder picks; 03's reasoning is the stronger one |
| K3 | Other markers | 05 2.2 `test_concurrency`: "consider `thread_safety` marker" | 03 section 1: tests should use no custom marker | Builder picks; no marker is the safer choice under `--strict-markers` |
| K4 | `ORCA_AGENT` literal | 02 G10: state the value (`claude`, from `seed-brief.md:64`) in the task file; the pin test holds a literal | 05 T-F and G-20: do not repeat the literal; refer to "the seed-brief agent token"; no value given | Builder must supply the value somewhere an implementer can read it |
| K5 | PATH stubs | Design 11/12: committed `stubs/gh`, `stubs/orca`. 05 G-03 adds `stubs/git` | 03 2.1 and 01 F6: no executable file is tracked under `tests/`; recommend copy-then-chmod into `tmp_path`. 02 G5: stubs must also shadow `orca-ide` because `_ORCA_CLIS` tries it first; 05 3.8 lists no `orca-ide` stub | Builder fixes the stub set (gh, git or a real tmp repo, orca, orca-ide) and committed vs written-at-runtime |
| K6 | `make test` gate | 05 section 6 final gate 4 lists `make test` as is | 03 section 6: the whole serial suite includes `tests/cli/test_verify_sync_hooks.py`, which rewrites real files under `src/superclaude/hooks/`; runtime unrecorded; xdist absent locally. 03 proposes a named subset | Builder states how design gate 2 and AC-23 are met (CI full run, or the 03 subset locally) |
| K7 | Crash-injection reruns | Design 12 line 784: one rerun | Spec NFR-005 (via 02 G6 and 05 X8): five reruns | Already resolved in both files: use 5 |
| K8 | Template rule conflicts | 04 Gaps (a) to (e): intermediate-gate size (3 vs 5), M4 agent count (2 vs 3 or 4), single paragraph vs bulleted item layout, `src/` paths in Execution Context vs the RFQA spot check, fix-cycle cap (2 vs 3) | Same file gives a recommended encoding for each | Builder follows 04 Part D |

## Part 4. Gap list

No CRITICAL and no IMPORTANT gap found. Every file, test, gate and acceptance criterion of design sections 11, 12, 13 and 17 has research coverage.

### CRITICAL
None.

### IMPORTANT
None.

### MINOR (not blocking)

| Id | Gap | Where | Suggested action |
|---|---|---|---|
| MIN-1 | `research-notes.md` still reads `AMBIGUITIES_FOR_USER: None`, but the research found decisions an implementer cannot make silently: 02 G1 (`Runner.run` has no `cwd`), 02 G3 (no closed-enum reason for a failed or incomplete marker read or edit-timestamp read; 02 says "flag as an owner question"), 02 G5 (stubs must shadow `orca-ide`), 05 G-04 (reason for the `reset` audit line), G-06, G-19. | research-notes.md vs 02 G, 05 Gaps | Builder lists these in the task file's `### Open Questions` with the chosen resolution (TB-Add-3 requires blocked items to cite an OQ index). G3 has two options and no recommendation in 02; the builder must choose. |
| MIN-2 | 05 (the file a builder will use as the per-module breakdown) does not carry several 02 findings into its module traps: 02 G3 (reason gap), G4 (`marker_time` undefined), G12 (null event fields), G13 (page longer than 100), G14 (label names with commas), G15 (single marker constant for `MARKER_JQ`), and the `gh` exit-code-4 signal. A grep of 05 for these returns nothing. They are covered in 02, not lost. | 05 sections 1.2, 1.4 | Builder copies them into the `predicates.py` and `github.py` item text. |
| MIN-3 | Contradictions K1 to K6 above are not reconciled inside the research files. | See Part 3 | Builder resolves each in the item text. |
| MIN-4 | Tag vocabulary differs: 03 section 9 uses HOLDS and PARTLY; 05 uses stated, derived and UNVERIFIED. The information is present. | 03 section 9, 05 | None needed. |
| MIN-5 | Unread or unverified precedents the research itself names: `sprint/logging_.py` and `swarm/logging_.py` (JSONL analogues for `audit.py`), `swarm/state.py` read only by line count, `pipeline/gates.py`-style predicates; runtime import order of `issue_watch.cli` to `swarm.atomic`; `detect-secrets` and `shellcheck` on fixtures and stubs (pre-commit only); full-suite runtime; Python 3.10 behavior (only 3.11 locally); `-n auto` stability of a `multiprocessing` test. | 01 Gaps, 02 Gaps, 03 Gaps | Builder keeps these as UNVERIFIED notes; none blocks item writing. |
| MIN-6 | `BUILD_REQUEST` was not present when 04 was written, so POST_REFLECT_GATE, QA_INTENSITY and TESTING_REQUIREMENTS come from `research-notes.md` lines 47 to 49. The skill-mode `{BASE}` for `--diff {BASE}..HEAD` is unspecified in SKILL.md. | 04 Gaps | Builder confirms the values against the BUILD_REQUEST and picks a literal base ref. |

## Part 5. Method and limits

- Read all 5 research files completely (05 in two pages, lines 1 to 455) and `research-notes.md`.
- Read design sections 11 to 18 directly (lines 740 to 919) and grepped the design for the verb count, `property_based`, PF-034, `orca-ide` and the marker-read reason text. Section 18 lines after 919 were not read; 05 states D18 covers all 29 FR and 14 NFR.
- This is a breadth check. I did not re-run the code-level checks behind 02's `[CODE-VERIFIED]` tags. No invented claim turned up where I compared a research statement with the design text.
- Research files were not modified.

## Verdict: PASS

All 9 checklist items pass (items 7 and 9 with the minor caveats above). 17 of 17 design file rows, 8 of 8 named tests, 7 of 7 gates and 25 of 25 acceptance criteria are covered. Gap list: 0 CRITICAL, 0 IMPORTANT, 6 MINOR.

VERDICT: PASS

