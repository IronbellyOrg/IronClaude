# Research Notes: implement the GitHub issue watcher (`superclaude issue-watch`) from docs/designs/issue-watcher.md

**Date:** 2026-11-07
**Scenario:** A (explicit request: the design document names every file, test, gate and acceptance criterion)
**Depth Tier:** Standard
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

- `docs/designs/issue-watcher.md` (about 12.5K words, sections 1 to 18): the design. Section 11 lists files to create; section 12 tests; section 13 gates; section 17 acceptance criteria; section 18 FR/NFR traceability. Driving spec: `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (FR/NFR ids), refactor log `.../spec-refactor-log.md`.
- `src/superclaude/cli/main.py` (565 lines): Click root; the design says two lines after line 561 register the new group, same pattern as `reflect_group` (lines 559 and 561).
- Existing CLI packages under `src/superclaude/cli/`: `swarm/`, `reflect/`, `pipeline/`, `sprint/`, `roadmap/`, `tasklist/`, `eval/`, `audit/` (style references). `swarm/atomic.py:14` `write_prepared_bytes` is cited by the design.
- `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` (`parse_origin_url`, `read_origin`) and `refs/claim.md` (claim marker, lines 26, 41-42, 47) and `templates/claim-comment.md`.
- `src/superclaude/cli/install_user_setup.py:198-221` (private `_find_orca`).
- Tests: `tests/pr_submit/test_conflict_e2e.py` (PATH-stub pattern for `gh`), `tests/conftest.py`, `tests/cli/`.
- Build gates: `Makefile` (lint, lint-architecture, test, verify-deps, verify-sync, sync-dev), `pyproject.toml` (ruff 0.15.20, select E,F,I,N,W,TID, line length 88, py310, `--strict-markers`), `.github/workflows/test.yml` (pytest `-n auto`, `ruff format --check src/ tests/`).
- To create (design section 11): `src/superclaude/cli/issue_watch/{__init__,runner,github,predicates,record,launch,audit,cycle,cli}.py`; `tests/issue_watch/` (`__init__.py`, `conftest.py`, per-module tests, cross-cutting tests, `fixtures/_assumed_shape/*.json`, `stubs/gh`, `stubs/orca`); `docs/designs/issue-watcher-setup.md`; two lines in `main.py`.

## PATTERNS_AND_CONVENTIONS

- UV only; Python 3.10 floor; `from __future__ import annotations` style to be checked in neighbours; click groups registered in `main.py`; no new dependency or pytest marker; tests safe under xdist (`-n auto`), a `tests/issue_watch/__init__.py` is required (two `test_cli.py` files would collide otherwise).
- Injectable seams (Runner, Clock, Launcher, Store) with fakes in `conftest.py`; no real `gh`, `orca`, `git` or network in any test; PATH stubs for the end-to-end test.
- `.claude/` is never staged; `.dev/tasks/` is always staged; no push and no PR step inside the task file; exactly one local checkpoint commit item before the POST reflect gate (research/06 DF-07).

## GAPS_AND_QUESTIONS

- Whether each design citation (file:line) still holds in this checkout (design section 3 lists 23 corrections; section 15 lists UNVERIFIED shapes). Researchers must re-verify before the builder writes items.
- Exact list and size of existing similar Click packages, their test layout, and how `tests/` import the CLI.
- Whether `make test` can run in reasonable time or the affected subset must be named.
- UNVERIFIED gh and Orca reply shapes: the task must record them only as `_assumed_shape` fixtures (design section 15).

## RECOMMENDED_OUTPUTS

Research files under `research/`: 01 CLI package conventions and registration; 02 integration points and design-citation cross-validation; 03 test and verification infrastructure; 04 MDTM template and task examples; 05 work breakdown (module dependency order, FR/NFR to file map, suggested phases).

## SUGGESTED_PHASES

1. File Inventory + Patterns & Conventions: existing `src/superclaude/cli/*` packages, `main.py` registration, Click group style, `__init__` conventions, error and exit-code idioms, lint rules (ruff, arch_lint).
2. Integration Points + Doc Cross-Validator: verify every code citation of the design (sections 3, 8, 15) against the repo: `origin_repo.py`, `_find_orca`, `swarm/atomic.py`, `claim.md` marker and template; tag CODE-VERIFIED, CODE-CONTRADICTED or UNVERIFIED.
3. Test & Verification: pytest config, markers, xdist, conftest fixtures, PATH-stub pattern, Makefile and CI gates, ruff pin.
4. Template & Examples: MDTM template 02 rules and a recent finished implementation task under `.dev/tasks/done/` as a model.
5. Data Flow Tracer / work breakdown: read the design and spec-final completely; propose the module build order, per-file items, per-FR/NFR mapping, test ordering, and the final gates.

## TEMPLATE_NOTES

Template 02 (complex task): discovery, build, test, QA gates, completion. Tier Standard, qa_intensity standard. Tests are required (UNIT, plus the PATH-stub end-to-end test); VALIDATION_REQUIREMENTS: lint, `ruff format --check`, `make verify-deps`, `make sync-dev` then `make verify-sync`. POST reflect gate ENABLED in default skill mode (`reflect_post_mode: skill`), `--spec docs/designs/issue-watcher.md`. Template path: `/home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md` (the project copy `.claude/templates/workflow/` does not exist).

## AMBIGUITIES_FOR_USER

None. Intent is clear from the design; owner questions Q1 to Q4 in design section 16 are resolved by following the design's stated choice.
