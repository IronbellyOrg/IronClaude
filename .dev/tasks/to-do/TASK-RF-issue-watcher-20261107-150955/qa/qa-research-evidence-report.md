# QA Report - Research Gate (lens: evidence-quality)

**Topic:** GitHub issue watcher MDTM task build (docs/designs/issue-watcher.md)
**Date:** 2026-11-07
**Phase:** research-gate
**Fix cycle:** N/A (fix_authorization: false, report only)
**Assigned files:** research/01 .. research/05

---

## Progress log (appended incrementally)

- Header written. Read all five research files in full. Spot-checks in progress.
- Spot-checks complete (see Section A and B). Adversarial stance held; cross-file contradiction pass done.

---

## Section A. Spot-check ledger (what I re-read against the real repo, with tool evidence)

Scale: roughly 60 distinct cited paths checked for existence (target was 20 percent of about 150; reached about 40 percent) and about 190 cited line numbers or quoted snippets (target 15).

### A.1 The files you told me to focus on: all HOLD

| Cite (research file) | Result | Evidence |
|---|---|---|
| `main.py:559` reflect import with `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` (01 F1, 02 X3) | HOLDS, text byte-matches | Read main.py 515-565: 559 import, 561 `main.add_command(reflect_group, name="reflect")`, 562-563 blank, 564-565 entry guard; file is 565 lines (`wc -l`). Registration pairs at 519/521 ... 555/557 all as listed in 01 F1. |
| arch_lint rules at 164-186 / 188-209 / 211-228, `_ALLOW_MARKER` 58 and 107, docstring exemption 141-159, 304 lines (01 F6, 02 C9) | HOLDS | Read arch_lint.py 50-230; `wc -l` 304. Rule 1 uses flat `ast.walk` and `ast.Assign/AnnAssign` with `ast.Name` target (172), so any scope. |
| `contracts/__init__.py` `ID_PATTERNS` 64-77 and `__all__` 302-313, ten names (01, 02) | HOLDS | Read lines 60-80 and 298-313. Pattern bodies at 71-76 match the six quoted. |
| `_find_orca` `install_user_setup.py:198-221`, timeout 213, excepts 217, `orca-cli` check 219, `_ORCA_CLIS` 35, import of `install_hooks` at 31 (01, 02 C2, C19, X5) | HOLDS | Read lines 20-39 and 195-224. C19 reasoning also correct: line 219 sits outside the `try` (208-218). |
| `swarm/atomic.py:14` signature, 22-26 mkstemp, 28-31 fsync, 32 replace, 33-38 except, 39 return, 7-11 imports, no dir fsync (02 C4, X4) | HOLDS | Read the whole 39-line file. Only callers are `swarm/normalize.py:81` and `swarm/reduce.py:108` (grep), matching 02 E. |
| `origin_repo.py:86-99`, `_NAME` 65, patterns 66-69, `_GITHUB_URL` 70-73 with IGNORECASE, `check_claim` 102, case-insensitive compare 135, `read_origin` 156-174 with no cwd/timeout (02 C3, E) | HOLDS | Read lines 60-180. `scripts/` holds only `clickup_claim.py` and `origin_repo.py` (`ls`), no `__init__.py`. |
| `claim.md:26` (both commands), 29 marker, 41-42 assignee rules, 47 `--add-assignee @me`, 88 marker (02 C6, C7, E, G4) | HOLDS | Read lines 22-91. `templates/claim-comment.md:23` is `<!-- sc:issue:claim -->` (grep), file is 23 lines. |
| Makefile 13-15, 48-50, 53-55, 109, 166, 356-359, 362-493, Check 11 at 467-476 (01, 02, 03) | HOLDS | Read lines 10-57 and 460-495, plus grep. |
| `pyproject.toml:54` `ruff==0.15.20`, 16, 71, 76, 78-83, 107-116, 114, 135, 173-206 select/ignore/banned-api, 208-216 mypy, deps 34-43, dev extra 46-56 (01, 02, 03) | HOLDS (one comment-range nit, M-3 below) | Read lines 12-216. `uv.lock` ruff 0.15.20 at 1563-1564 and click 8.5.1 at 108-109 (sed). `.pre-commit-config.yaml` rev v0.15.20 at 110 (sed 98-113). |
| `test.yml` 22 (python 3.10), 26-29 xdist ad hoc, 32-38 sync-dev, 47 `-n auto`, 102/106 ruff, 123 verify-deps, 127/131 sync and verify-sync, 135 lint-architecture, 137-142 serial hook tests (01, 02, 03) | HOLDS (job-name nit, M-6) | Read test.yml 1-145. |

### A.2 Other cites that HOLD (sample)

- Design: 102, 104, 110, 112-120, 173, 176, 218-225, 233-242, 244, 246, 264-302, 387-388, 621, 625 (the `cwd=worktree` sentence is on 625), 636, 666, 671, 693, 722, 737, 741, 751-766, 777-791, 793-805, 829-840, 866, 870, 900, 935. Design is 935 lines; spec-final is 515 lines.
- Spec: 112, 136, 161, 163-164, 196, 213, 267, 309, 317, 332-358, 361, 366, 384, 395. The reason table (spec 334-358, first column) holds exactly 52 names (I counted by hand from the printed rows), so the "52" in 05 is right.
- 01 F3 exit-code table: counts for `sys.exit(` per package (reflect 4, tasklist 1, cli_portify 7, prd 4, eval 22, recommend 7, roadmap 1+2=3, cleanup_audit 1+1=2, swarm 0) and `click.exceptions.Exit` for swarm (1+70=71) all re-counted and match.
- 01 F4 file sizes (`wc -l` on 27 files), 266 of 292 modules with `from __future__ import annotations` (I recomputed 292/266), 27 files with `@dataclass(frozen=True)`, zero `from ..` imports, no `cli.py` anywhere, no `issue_watch` dir, `tests/cli` without `__init__.py`: all match.
- 01 F7 / 03: `tests/cli/test_cli_registration.py` 24, 26, 31-49 (15 names), 102-106; swarm and cleanup-audit membership tests; the two slash-command-count tests; no `mix_stderr`; 70 CliRunner files; no `multiprocessing` use; `tests/conftest.py` 12-15, 29, 83; `pytest_plugin.py` 20, 148, 172, 206; test dir `__init__.py` map (21 with, 5 without) exactly as listed.
- 02/03 PATH-stub precedent: `test_conflict_scripts.py` 46-64, 165-179, 1510-1517, 1555-1571, 1691-1719; `test_conflict_e2e.py` 61-71, 75-78, 118-146, 472-475, 508-513, 698. Other precedents (swarm TUI subprocess 130-143, ccsession flock holder 4496-4518, eval exit codes 70-80, eval lifecycle 642-650, AST tests, imm6 spies) all present.
- 02 live help claims (`gh` 2.103.3, Orca 1.4.245-aidev02, `--retry-launch` Notes text verbatim, `orca skills list` topics array, `gh help exit-codes` exit 4, `gh issue list` flags and `projectItems` field, `gh label create` flags, `git -C ... remote get-url origin` output): re-ran the help commands; all match.
- 04: template (1519 lines) I15/I16/I18-I22/M-section/PART 2 cites; SKILL.md 1070-1077, 1233, 1662-1701, 2154-2233, 2296-2312, 2361-2371, 2388, 2419-2440; rf-qa.md 312-375; both example tasks (628 and 686 lines, 94 and 86 checkboxes, line cites for items and gates); `src` and installed copies of SKILL.md and template identical (`diff -q`); `.claude/templates` absent. All hold.
- Design status claims: `docs/designs/issue-watcher.md` and the brainstorm dir are untracked (`git status`: `??`), so "no test may read `.dev/`" is correct.

### A.3 Mismatches found (every one; true claim, wrong or imprecise locator unless stated)

| # | Where | Research says | Real repo shows |
|---|---|---|---|
| M-1 | 01 F2 | `@reflect_group.command()` for `run` at `reflect/commands.py:221` | line 222 (grep: `222:@reflect_group.command()`) |
| M-2 | 01 F2 | module docstring "Heavy imports ... lazy" at lines 5-6 | lines 4-5 |
| M-3 | 01 F6 | `pyproject.toml:48-53` comment explains the exact pin | comment is lines 50-53; 48-49 are `pytest-benchmark` and `scipy` |
| M-4 | 01 F1 | `superclaude/cli/__init__.py:12` is `from .main import main` | line 13 |
| M-5 | 01 F5, 03 s2.1/s2.2 | `tests/cli/reflect/test_cli_smoke.py` `from __future__` at 8, `reflect_group` import at 15, `.conftest` import at 19, `invoke(reflect_group, ["--help"])` at 49 | 7, 17, 21, 46 |
| M-6 | 02 s A | `test.yml:22` is the job name "Test on Python 3.10" | line 22 is `python-version: "3.10"`; job name is line 12 |
| M-7 | 04 B (template note) | detection-contract `template_schema_doc` (line 69) is an absolute `src/superclaude/templates/...` path that "resolves" | the value is `/config/workspace/IronClaude/src/superclaude/templates/...`; `/config/workspace/IronClaude` does not exist on this host, so it does not resolve here |
| M-8 | 02 E and G10 | `spec-panel-review.md:179-180` and `adversarial/base-selection.md:157` | both exist and say what is claimed, but only under `.dev/brainstorms/20261107-064825-github-issue-watcher/` (the repo has 189 files named `base-selection.md`); the bare basename is not a usable locator |
| M-9 | 01 F7 | `plugins/superclaude/` holds `agents, commands, core, examples, hooks, mcp, modes, scripts, skills` | also `__init__.py` and `templates`; conclusion (no `cli/` mirror) still right |
| M-10 | 04 s C | "Surveyed 16 `TASK-RF-*` files" | Glob finds 15 `TASK-RF-*/TASK-RF-*.md` files (20 `TASK-RF-*` dirs); cannot reproduce the 16 |

None of M-1 to M-10 changes a conclusion. Grade: MINOR (moved or imprecise line numbers on true claims; M-7 and M-8 are minor locator or "resolves" errors).

---

## Section B. Substantive findings (cross-file contradictions and unsupported assertions)

### B.1 IMPORTANT: 05's stub plan omits the `orca-ide` stub that 02 rates HIGH, and 05's own mitigation does not work on this host

- 02 G5 (line 135, severity H): `_ORCA_CLIS = ("orca-ide", "orca")` (`install_user_setup.py:35`, loop at `:204-205`), so `find_orca` tries `orca-ide` first; a stub named only `orca` is never reached and the probe plus `agent launch` would hit the real Orca. 02 requires stubs named `orca-ide` AND `orca` with guards on `which("orca-ide")`, `which("orca")`, `which("gh")` (and `git` if stubbed), or a PATH of stub dir plus symlinks only (precedent `test_conflict_scripts.py:1555-1571`, which I confirmed).
- 05 does not carry this through: s3 step 3.8 (line 243) and the P8 row (line 378) list only `stubs/gh`, `stubs/orca` (+ `stubs/git`); the `test_cli_e2e.py` row (line 208) names `stubs/gh`, `stubs/orca`; the guard is only `shutil.which("gh")`. 03 s3 caveat 2 also guards only `gh` and its `which gh orca` omits `orca-ide`.
- 05 T-J (line 408) proposes "e2e PATH = stub dir + `/usr/bin:/bin`" with the guard `which("orca-ide") is None or stub`. Evidence from this host (`which -a`): `/usr/bin/orca-ide` and `/bin/orca-ide` exist, as do `/usr/bin/gh`, `/bin/gh`, `/usr/bin/git`. So that PATH still exposes the real `orca-ide`, `gh` and `git`, and the `is None` guard would fail on any host like this one unless an `orca-ide` stub exists.
- Why it blocks: the task builder synthesizes the file list from 05 (the work breakdown). Following 05 literally yields e2e tests that call the real Orca on this host, violating the design's "No test runs a real gh, orca, git" (design s12) and NFR-001 safety intent.
- Required fix: amend 05 (s2.2 `test_cli_e2e` row, s3.8, P8, T-J, G-03) to the 02 G5 form: stubs `orca-ide` and `orca` (both log argv), a `git` decision (stub or tmp repo), guards for all four names, and a PATH of the stub dir only (plus symlinks to needed tools such as `bash`, `jq`), not `/usr/bin:/bin`.

### B.2 IMPORTANT: contradictory instructions on printing the `ORCA_AGENT` literal, and the governing "no model name" rule is asserted without a source

- 02 G10 (line 140): "State the value in the task file (the PF-034 ban was on the spec/design text, not on code)"; the value is `claude` (confirmed at `seed-brief.md:64`).
- 05 T-F (line 404): "Task items and docs refer to 'the seed-brief agent token'; the constant's literal appears only in `launch.py` and its one pin test; no tier or model names anywhere", justified as "Project/user constraint". 05 line 8 also promises never to repeat the literal.
- The rule behind T-F is not cited. The only trace I found is `spec-refactor-log.md:47` and `:81` ("PF-034 vs the no-model-name rule: the rule wins"). `grep` for "model name" in `research-notes.md`, `seed-brief.md` and `spec-final.md` finds nothing, so its source and scope (every file, or only spec text) are not established, and it carries no [UNVERIFIED] tag. PF-034 itself (confirmed at `spec-refactor-log.md:47`, `spec-final.md:47`, `design:66`) only decided not to print the literal in the spec and design.
- Why it blocks: the builder must write the `ORCA_AGENT` item and the pin-test item; the two files give opposite directions, and the builder cannot tell which is authoritative. An implementer also needs a readable source for the value (the only local one is the untracked `seed-brief.md:64`).
- Required fix: tag the "no model name" constraint [UNVERIFIED] or cite its source; reconcile 02 G10 with 05 T-F/T-G/G-20 into one instruction (for example: the item cites `seed-brief.md:64` by path and line for the value, and the pin test holds the literal).

### B.3 MINOR notes (recorded, not blocking)

1. Gate-size precedent (04 Gap (a), `SKILL.md:2363` and `:2299`). 04 recommends 3-agent intermediate gates and cites the t2 validator PASS as "resolution evidence". SKILL.md:2363 says any intermediate gate with fewer than 5 agents is MALFORMED (it names research-gate and synthesis-gate in a parenthesis) and `:2299` says QA gates have minimum 6 agents. That rule text already existed when t2 was built (`git show ac80f176:...SKILL.md | grep -c 'fewer than 5 agents'` = 2; commit date 2026-06-08, t2 dated 2026-07-06). But the t2 report (`qa-qualitative-sufficiency-report.md:13-23`) evaluates only the final-document "fewer than 6" rule and never mentions the intermediate rule, so it shows "not flagged", not "considered and accepted". 04 does disclose the conflict as Gap (a); the builder should record the choice explicitly.
2. `property_based` tag. 03 s7 item 6 recommends not tagging; 05 s2.2 says `test_prompt_regex_property` is "tagged `property_based`"; design line 93 says the marker "may tag" the test. The disagreement between 03 and 05 is not flagged.
3. `make test` gate. 03 s6 says the whole suite is too large to run without an owner decision and recommends an affected subset; 05 s6 lists `make test` as gate 4 and defers sizing to 03; design s13 / spec line 366 / AC-23 name `make test` as a gate. Nobody turns this into an explicit open decision. Note `make test` includes `tests/cli/test_verify_sync_hooks.py`, which rewrites real files in place (its docstring, lines 7-15, which I confirmed).
4. Design-internal naming not in 05's gap list: `RecordingLauncher` (design 297) versus `FakeLauncher` (design 761, 778); `slo_numbers(lines, store, now)` at design 224 versus the `doc` parameter 01 and 05 write (I could not read design line 745, which is omitted as a long line).
5. Items correctly flagged [UNVERIFIED] or as gaps in the research and not over-claimed: `gh api user --include` layout, REST events fields, GraphQL edit/project fields, auth and rate-limit stderr text, `agent_session_operation_unknown`, operation-id JSON path, `--label` comma splitting, `multiprocessing` stability under `-n auto`, `make test` run time, Python 3.10 behaviour, ruff-format wrapping of the registration line. No untagged documentation-derived claim found in 02's tables; the three [CODE-CONTRADICTED] items (C14 premise, C21 scope, X13 guard) are real (C14 and the C21 reasoning re-derived; X13 confirmed: no `shutil.which("gh")` guard exists in the precedent).
6. Claims I could not reproduce at reasonable cost and did not downgrade: `uv run pytest --collect-only` = 17,096 tests in 17.56 s, and `import xdist/hypothesis/pytest_timeout` failures (03 s1, s6). Both are environment measurements, tagged as measurements; xdist absence is consistent with `test.yml:26-29`.

---

## Items Reviewed (research-gate checklist, evidence-quality lens)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory (Status: Complete, Summary) | PASS | All five files read: "Status: Complete" and a Summary/Gaps section present in each (01 lines 5, 159-173; 02 lines 5, 161-175; 03 lines 5, 219-236; 04 lines 5, 200-213; 05 lines 6, 421-453). |
| 2 | Evidence density | PASS (Dense, above 90 percent of factual claims carry path plus line or function) | About 190 cites re-checked; 10 imprecise locators (M-1 to M-10), none wrong in substance. |
| 3 | Scope coverage (research-notes EXISTING_FILES) | PASS (partial read) | Read `research-notes.md` lines 17-50: install_user_setup, tests, Makefile, pyproject, workflows, to-create list are all discussed in 01-05. I did not read lines 1-16. |
| 4 | Doc cross-validation tags | PASS | 02 tags every design row [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]; I re-read about 40 of the [CODE-VERIFIED] rows, all hold. |
| 5 | Contradiction resolution | FAIL | B.1 (05 versus 02 on stubs and PATH) and B.2 (02 versus 05 on the agent literal); minor items B.3.2 and B.3.3. |
| 6 | Gap severity | PASS with notes | Gap sections list real unknowns; none hides a fact the builder needs except those in B.1 and B.2. |
| 7 | Depth appropriateness | PASS | 05 traces the design end to end (build order, import graph, test map, FR/NFR map). |
| 8 | Integration point coverage | PASS | 02 sections A-F cover every reused helper with signature, import path and import-versus-copy decision. |
| 9 | Pattern documentation | PASS | 01 F2-F6 give group style, exit idioms, naming, typing, lint and arch_lint rules with evidence. |
| 10 | Incremental writing compliance | UNVERIFIABLE | No write history available; only mtimes 15:17-15:21 and the "(appended incrementally)" heading in 01. |

## Summary

- Checks passed: 8 / 10 (PASS or PASS with notes). Failed: 1 (item 5). Unverifiable: 1 (item 10).
- Critical issues: 0. Important issues: 2 (B.1, B.2). Minor: 10 locator mismatches (M-1 to M-10) plus 6 notes (B.3).
- Fixes applied: 0 (report only; fix_authorization: false).

**Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% of checkable items (9/9). The verdict is still FAIL because two blocking contradictions are open.

**Tool engagement:** Read: 22 | Grep: 11 | Glob: 3 | Bash: 10 (each Bash call was a batched read-only chunk, e.g. 15-30 `sed -n`/`wc`/`grep` probes). No Tavily or web tools used (no external-web claim needed checking; `gh`/`orca` claims were checked with local `--help`).

**UNCHECKED items:** none. **UNVERIFIABLE items:** item 10 (incremental writing), blocker: no per-write history exists for the research files.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | 05 s2.2 `test_cli_e2e` row, s3.8 (line 243), P8 (line 378), T-J (line 408), G-03; 03 s3 caveat 2 | Stub plan lists `stubs/gh`, `stubs/orca` (+git) but not `orca-ide`, which `find_orca` resolves first (02 G5, HIGH; `install_user_setup.py:35,204-205`). T-J's `PATH = stub dir + /usr/bin:/bin` still exposes real `orca-ide`, `gh`, `git` on this host (`which -a`: `/usr/bin/orca-ide`, `/usr/bin/gh`, `/usr/bin/git`), so its guard would fail and a literal follow of 05 could run the real Orca. | Align 05 and 03 to 02 G5: stubs `orca-ide` and `orca`, `git` decision, guards on all four names, PATH of stub dir plus symlinks only. |
| 2 | IMPORTANT | 02 G10 (line 140) vs 05 T-F (line 404), T-G, G-20, line 8 | 02 says state the `ORCA_AGENT` value in the task file; 05 says task items must not repeat it and cites a "Project/user constraint: no model name in any file" with no source (only `spec-refactor-log.md:81` mentions it; absent from research-notes, seed-brief, spec-final). No [UNVERIFIED] tag. Builder gets opposite instructions. | Cite the rule's source and scope or tag it [UNVERIFIED]; give one reconciled instruction (cite `seed-brief.md:64` for the value; literal only in `launch.py` and the pin test, or state it in the task if the rule is spec-only). |
| 3 | MINOR | 01 F1/F2/F5/F6, 02 s A, 03 s2, 04 B, 02 E | M-1 to M-10 locator errors (see A.3). | Optional: correct line numbers; give full path for `spec-panel-review.md` and `base-selection.md`. |
| 4 | MINOR | 04 Gap (a), `SKILL.md:2363`, `:2299` | Gate-size precedent shows "not flagged", not "accepted"; rule text predates t2. | Builder records the intermediate-gate choice explicitly. |
| 5 | MINOR | 03 s7.6 vs 05 s2.2 vs design 93 | `property_based` tag disagreement unflagged. | Pick one in the task file. |
| 6 | MINOR | 03 s6 vs 05 s6 vs spec 366 / AC-23 | `make test` versus subset not turned into an explicit decision. | Add as an explicit builder decision or Open Question. |
| 7 | MINOR | design 297 vs 761/778; design 224 | `RecordingLauncher` vs `FakeLauncher`; `store` vs `doc` for `slo_numbers`, not in 05's gaps. | Add to 05's gap list. |

## Recommendations

- Before building: fix the two IMPORTANT items by editing 05 (and 03 caveat 2) for B.1, and adding one reconciled ORCA_AGENT instruction (and a sourced or [UNVERIFIED] "no model name" rule) for B.2. Both are text edits to research files; no new code investigation is needed.
- Minor items need no re-review (review severity rule); the builder can absorb them while writing the task file.
- The research is otherwise strongly evidence-based: every cite you asked me to focus on (main.py 559/561, arch_lint constraints, `_find_orca`, `atomic.py:14`, `origin_repo.py:86-99,156-174`, `claim.md:26,41-42,47`, Makefile cites, `pyproject.toml:54`, `test.yml` cites) matches the repo.

VERDICT: FAIL

## QA Complete
