# QA Report: Task Qualitative Review (operational-correctness lens), Phases 8 to 14

**Topic:** TASK-RF-sweep-phase1-20261108-072653
**Date:** 2026-11-08
**Phase:** task-qualitative
**Lens:** operational-correctness
**Assigned phases:** 8 to 14
**Fix cycle:** N/A
**fix_authorization:** false (report only)

---

## Overall Verdict: FAIL

Two blocking findings (OPS-01, OPS-02), both in Phase 14. Phases 8 to 13 have no blocking finding; their anchors, signatures and test sequencing check out against the repository at `5dc29d23`.

## Drift baseline (BUILD-REQUEST.GOAL, verbatim opening)

"Build the MDTM task file for issue #339 Phase 1 (orchestrator mode). The task, when run by `/task`, first closes five required design items on `docs/designs/orchestrator-mode.md`, then implements, exactly as that design specifies: [...] the tests in `tests/sweep/` and `tests/commands/test_sweep_command.py`. The design's section 15 maps REPORT steps 1.0a to 1.29." The POST_REFLECT_GATE DIFF clause adds: "append `git diff --no-index /dev/null <file>` for each new untracked file the task created". AX-1 is active.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-1 | FAIL | Phase 8 to 13 commands checked (see Command dry-run notes). 14.8 Branch A puts pipx build, install and help inside `timeout 30` (OPS-02). The 14.43 diff command picks up untracked files that existed before the task (OPS-01). |
| 2 | Project convention compliance | none | PASS | Every edit targets `src/superclaude/`, `tests/`, `docs/`, `CHANGELOG.md`, `.gitignore` or the plugin refs copy. `.claude/` is only produced by `make sync-dev` (14.1) and checked unstaged. `.dev/tasks` is staged only in 14.45. No commit or push. `plugins/superclaude/core/` holds no WORKER-CONTRACT or HOW-WE-WORK mirror (ls), so no second copy is missed. |
| 3 | Intra-phase execution order | none | PASS | 8.6 `.gitignore` comes before the 8.9 real-git test; 8.8 fakes before 8.9; `raising=False` removed in 8.11 after 8.10 defines `_orca`; 11.2 directly after 11.1 (`test_routing_refresh.py:648` `shipped - _POST_REFRESH_ADDITIONS == active`); 12.1 and 12.2 before 12.3 with no test run between; 13.2 and 13.3 adjacent, with the membership test (`test_how_we_work_routing_table.py:297` `members == _OTHER_COMMANDS`) run only in 13.3; R3 copy in 13.4 before the parity test. |
| 4 | Function signature verification | none | PASS | Names in 8.2 to 8.12 and 9.1 match DESIGN 7.1 lines 357-445 and 7.3 lines 518-543 (Budget defaults, OrcaResult kinds, `check_*_args`, `_git(cwd, *args, timeout)`, `_publish(text, output_dir, now)`, `to_json(result, ctx, report_path)`, 8 ALLOWED_ORCA templates, FORBIDDEN_TOKENS). The `recommend/__init__.py:12-20` pattern is confirmed. |
| 5 | Module context analysis | AX-2 | PASS (note) | `superclaude/cli/__init__.py:13` imports `.main`, so after 9.2 any `import superclaude.cli...` loads `sweep.commands`. 10.6 deletes both sweep modules from `sys.modules` before re-import, so the lazy test still holds. 8.5 says probes holds "only `import subprocess`", but `_git` needs an `os.environ` copy (M-03). |
| 6 | Downstream consumer analysis | none | PASS | Consumers of a new command file traced: `test_routing_refresh.py:648` (R5, 11.2), `test_how_we_work_routing_table.py:297` (R1 plus R4), `test_routing_plugin_parity.py:38` (R3), `test_worker_contract.py:837` unattended equality (no section, holds), `:765` never-as-worker term line, `:1081` removal test, write-verb audit `:1940-2012` (12.3 grep), `make lint-architecture` Checks 1, 2, 6, 8 and 9 (Makefile:369-450; `sc:sweep-protocol` ends in `-protocol`, Activation present). |
| 7 | Test validity | AX-4 | PASS (notes) | Tests exercise real modules with seam fakes. The real-git test copies the real `.gitignore` (`parents[2]` is the repo root). Notes: the 10.3 FR-021 check semantics are unstated (M-02); the 8.9 per-worktree test proves little until 10.4 re-points it (the item accepts this). |
| 8 | Test coverage of primary use case | none | PASS | 10.4 runs `superclaude sweep run` end to end through `CliRunner` with both seams patched and snapshots the filesystem; 9.3 runs the built CLI live against a named Run. |
| 9 | Error path coverage | none | PASS | 9.1 lists all six `[sweep publish]` messages (DESIGN 3.2 lines 106-128); 10.7 tests each exit code and every publication failure; 10.3 covers allowlist negatives before any subprocess. |
| 10 | Runtime failure path trace | AX-3 | PASS (note) | Trace below. One gap: the 10.1 `sweep_root` creates no `.git`, but SPEC FR-004 requires an explicit `--root` to hold `.git` (M-01). |
| 11 | Completion scope honesty | AX-1 | FAIL | 14.9 tags, and 14.43 diffs, pre-existing untracked docs as task output (OPS-01). The POST audit and the TCS file-count evidence therefore overstate what the task created. |
| 12 | Ambient dependency completeness | none | PASS | main.py registration (9.2, after `:565`, verified), `tests/sweep/__init__.py` (8.7), the registered `integration` marker (`pyproject.toml:114,119`), routing rows R1 to R8, `.gitignore`, CHANGELOG and developer guide :991 all have owning items. |
| 13 | Kwarg sequencing red flags | none | PASS | `patch_orca` uses `raising=False` until `_orca` exists (8.8) and is reverted in 8.11; 10.4 re-points the 8.9 test only after `collect` exists (8.10). No argument is supplied before its parameter exists. |
| 14 | Function existence claims | none | PASS | Grep-verified: `main.py:563,565,568`; `test_worker_contract.py:25,86,156,165,173,382,438,755,765,813,912,1322,1556,1954,2016`; `HOW-WE-WORK.md:318,333,337,396,403,404`; `commands.md:105,115,116`; `CHANGELOG.md:5,7`; developer guide :991; `WORKER-CONTRACT.md:23,271,273,275`; `.gitignore:254`; `recovery.py:433` `os.link`; `atomic.py:31` `os.fsync`; `test_conflict_scripts.py:46,48-64`; graph.md :9 and :41; issue.md :12, :23, :27 and :34; full-tree `src/superclaude` count 168. |
| 15 | Template cross-references | none | PASS | DESIGN sections 3.2, 5, 7.1 to 7.6, 8, 9, 10 and 11 read; every section the items cite exists and holds what the item claims. Reflect skill `SKILL.md:80` (a diff-file path is accepted) and `:204` (`output_input_overlap`) confirmed in `~/.claude/skills/sc-reflect-protocol/SKILL.md`. |

## Summary

- Checks passed: 13 / 15
- Checks failed: 2 (checks 1 and 11, both from OPS-01 and OPS-02)
- Critical issues: 0
- Important (blocking) issues: 2
- Minor issues: 8
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Axis | Location | Issue | Required Fix |
|---|----------|------|----------|-------|-------------|
| OPS-01 | IMPORTANT | AX-1 | Items 14.9 (line 2495) and 14.43 (line 2733) | Both items treat every file from `git ls-files --others --exclude-standard -- src tests docs plugins` as something this task created. At the start base, four files under `docs/` are already untracked: `docs/designs/orchestrator-mode.md` (the DESIGN itself) and `docs/designs/orchestrator-mode-review-1.md`, `-review-2.md` and `-review-3.md` (verified now with that same command; the DESIGN has no `git log` history). Because no item stages or commits DESIGN, the result is: (1) `phase1.diff` carries the three review documents, which are not this task's work, as new files, so the POST reflect audits unrelated content and can report it as drift; (2) DESIGN appears as one whole new file, so the R3-B1, R3-B2, R3-B3 and R4 edits from Phases 2 to 6 cannot be seen as changes, either by reflect or by the final gate's `git diff <base> -- <file>` (item 14.10 Context); (3) `final-inventory.md` tags all four as `new`, and the TCS "more than 25 distinct files" evidence (14.43 Verification, 14.44 Context) is inflated by four files. The BUILD-REQUEST DIFF clause says "for each new untracked file the task created", so the commands do not match their own requirement. | In 14.9 and 14.43, drop every path that is listed as `?? <path>` in `artifacts/baseline-git-status.txt` (item 1.3 already records it). For example, build the untracked list, then remove the baseline `??` paths with `grep -vxF -f` on a path list cut from the baseline. In item 1.3, also copy `docs/designs/orchestrator-mode.md` to `artifacts/design-base.md`. In 14.43, append `git diff --no-index -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/design-base.md docs/designs/orchestrator-mode.md`, so the design edits show as a real diff, and note in OQ-12 that the DESIGN hunk compares against a snapshot, not a commit. In 14.10, read the DESIGN changes from that snapshot diff. |
| OPS-02 | IMPORTANT | AX-1 | Item 14.8 Branch (A) (line 2488); also item 14.6 option (A) text (line 2474) | REPORT:1300's pass rule is "Run `superclaude sweep --help` once [...] time limit 30 s". Branch (A) wraps the whole `pipx run --spec "$WT" superclaude sweep --help` in `timeout 30`. On a cold pipx cache that one command builds a wheel from the worktree with hatchling (`pyproject.toml:2-3`), creates a venv and installs eight runtime dependencies (`pyproject.toml` `dependencies`: pytest, click, rich, pyyaml, jsonschema, jinja2, pexpect, httpx), and only then runs the help. The 30 s limit set for the help run is applied to install plus help, so `exit=124` is a likely outcome. That outcome HALTs the task at its last manual step (14.8 Verification) for a reason that has nothing to do with the code. | Make Branch (A) two calls: first an untimed warm-up `pipx run --spec "$WT" superclaude --version` from `/tmp` (it only fills pipx's own cache, which option (A) already accepts as leaving the installed tool unchanged), then the timed `timeout 30 pipx run --spec "$WT" superclaude sweep --help`, which reuses the cached venv. Update the option (A) wording in 14.6 to match before the owner decides. |
| M-01 | MINOR | AX-3 | Item 10.1 (line 1778) | SPEC FR-004 (merged-requirements.md:98): "An explicit `--root` must resolve to an existing directory that holds `.git`". The `sweep_root` builder lists packages, transcripts and `orca-tabs/`, but no `.git`, so the 10.4 and 10.7 CLI tests exit 2 until the executor adds it. This is recoverable inside the item's fix loop. | Add "and an empty `.git` directory (or a `.git` file) at the root" to the 10.1 Action. |
| M-02 | MINOR | AX-4 | Item 10.3 (line 1792) | The FR-021 static test is described only as "the FR-021 forbidden verb list written as a literal". SPEC FR-021 says the test checks that `probes.ALLOWED_ORCA` holds no verb from the list. A substring check fails on `--dispatch` and `<dispatch>` in the worker-show template, because `dispatch` is on the list. That invites the executor to weaken the test. | State that the test compares whole tokens of every `ALLOWED_ORCA` template against the list, and add the SPEC `worker-read` negative. |
| M-03 | MINOR | AX-2 | Item 8.5 (line 1446) | "holding only, for now, `import subprocess`, ..." conflicts with the same item's `_git` env copy, which needs `os`, and with the `Path` annotation. Ruff would flag the missing import. | Say "imports `os`, `subprocess` and `pathlib.Path`". |
| M-04 | MINOR | AX-3 | Item 9.1 Context (line 1624) | The run orchestration in DESIGN section 5 (lines 229-281) is not cited: `now` is read once, `Budget()`, `bind_run` only without `--run`, and with `--run` or after a binding, unavailable continues on disk. The gate inputs (9.5 to 9.12, "DESIGN sections 3, 5 and 7.1") and the 10.7 tests cover it, so the gap is caught later. | Add "DESIGN section 5 sequence and notes (lines 223-288)" to the 9.1 Context. |
| M-05 | MINOR | AX-3 | Items 11.5 and 12.5 | Phase 11 creates a new skill and command, but neither phase runs `make lint-architecture` (Makefile:362-450, Checks 1, 2, 6, 8 and 9 apply to the pair). Phase 11 also does not run `tests/skills` (write-verb audit at `test_worker_contract.py:1981`). These run first at 12.5 and 14.2, after the cmd-skill gate has passed. | Add `make lint-architecture` to the 11.5 commands. |
| M-06 | MINOR | AX-4 | Item 10.4 (line 1799) | The snapshot records `st_mtime_ns`. If directories are included, `.dev/` changes mtime when `sweeps/` is created, and the "exactly one added file" assertion fails. | Say the snapshot records regular files only and compares directory sets by path. |
| M-07 | MINOR | AX-4 | Item 9.1 Verification (line 1627) | `grep -c 'sys.exit'` cannot show the calls sit "only inside `run`". | Use `grep -n` and check each hit's line lies inside the `run` function body. |
| M-08 | MINOR | none | Item 8.6 | Inserting directly after `.gitignore:254` splits the sprint-state comment block (lines 252-257: `.dev/sprint-state/`, then the `e2e-reflect` sprint-state lines). DESIGN 10 asks for exactly this spot, so this is cosmetic. | Optional: insert after line 257. |

Known open item N-01 (item 5.12) is owned by A.10 and is not re-reported.

## Runtime path trace: `superclaude sweep run` to the published report

1. `superclaude` entry, then `superclaude/cli/__init__.py:13` imports `main`. `main.py` after line 565 runs `from superclaude.cli.sweep import sweep_group` (item 9.2), which goes through the lazy `__getattr__` (8.2) into `commands.sweep_group` (9.1). Holds.
2. `commands.run`: `_parse_window`, `_find_root` or explicit `--root` (FR-004 needs `.git`), `_check_output`, `_check_run_ids` (regex from the 1.0a facts, 7.17); any failure exits 2 and writes nothing (DESIGN 5 lines 229-230). Holds, with the M-04 note.
3. `Budget()` and `bind_run` when `--run` is absent, via `_orca` `run-current` (template 1). `check_orca_argv` runs before `subprocess.run` (8.10). Holds.
4. `collect(ctx, runs, root, budget)`: Orca reads (templates 2 to 6), `_git` per worktree with `--no-optional-locks -C` and `GIT_OPTIONAL_LOCKS=0` (8.5), disk readers that never raise past `collect` (8.10). Holds.
5. `classify_all` (8.4) returns `SweepResult` with `ClassifiedRow(row, classification, policy_of(row), safe_to_close(...))`, which matches the 8.3 `ClassifiedRow` fields. `report.render` (8.12) prints dimension 9 from `ClassifiedRow.policy`. The field producer and consumer agree.
6. `_publish(text, output_dir, now)` (9.1): makedirs, re-resolve, `O_EXCL` temp, fsync, `os.link` loop to `-99`, unlink. Then `to_json(result, ctx, report_path)` on stdout. The report lands under `<root>/.dev/sweeps/`, which 8.6 ignores. Holds; 10.4 and 10.7 test it.
7. Skill (11.3): PATH `superclaude sweep run`, with the `uv run --frozen --no-sync` fallback only on "command not found", then Read `report_path`. Holds.

No break in the code path. The breaks are in Phase 14 evidence handling (OPS-01) and the manual pipx step (OPS-02).

## Command dry-run notes (Phases 8 to 13)

- 8.1 `grep -h 'gate: PASS'`: every gate-decision writer (lines 412, 579, 753, 969, 1129, 1405) writes `<Name> gate: PASS...`, and HALT lines do not contain `gate: PASS`, so the count of 6 is sound.
- 8.6 and 13.7 `git check-ignore`: today both `.dev/sweeps/x.md` and `.dev/tasks/to-do/x.md` exit 1, so 8.6 is needed, and after it the expected 0 and 1 hold.
- 8.8 guard `getattr(request.function, "pytestmark", [])`: decorator marks live there; the plugin's `/integration/` auto-mark (`pytest_plugin.py:219-221`) uses `add_marker`, not `pytestmark`, so it is ignored as required.
- 9.4 `uv run pytest tests/sweep tests/unit`: `tests/unit/` exists.
- 11.2: anchor `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` is at `test_routing_refresh.py:33` and the assertion at `:648`; there is 1 insertion and 1 deletion.
- 12.3: the five anchors exist at the cited lines. `"WC-14": (` is at :156 and stays the only one; ident `WC-16` and phrase `WC-16. Coordinator loop` share the heading line, which `_check_rule` (:760-762) requires.
- 13.1 to 13.6: line predictions hold (R2 at new line 404 before R1 lands; R1 at 334; user-guide row at 116; CHANGELOG heading at 7). Plugin refs copy is byte-identical today (`cmp` exit 0), so 13.4 expects exactly 2 insertions.
- 14.5: the full-tree count is 168 today, which matches.
- 14.43: `git diff --no-index -- /dev/null <p>` exits 1 inside the `while` loop with no `set -e`, so the loop continues. `.dev` is excluded and `.claude/` (ignored except settings.json) does not appear. The reflect output root `reflect/post/audit/` does not contain `phase1.diff`, so `SKILL.md:204` overlap does not trigger. The fault is the input list (OPS-01), not the mechanics.

## Cross-phase limits

- Phases 2 to 7 were not reviewed. This review assumes their outputs exist as named: the revised DESIGN text, `1.0a-facts.md` (7.17), `tests/sweep/fixtures/captured-*` (7.18), the OQ records and `pr422-409-check.md` (7.19).
- OPS-01's DESIGN-snapshot fix touches item 1.3 in Phase 1, which is outside my phases. Any Phase 2 to 6 item that runs `git diff` on DESIGN has the same untracked-file problem; I did not check those items.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for V-01 (14.8 Branch B path).
- Relied on rf-qa PASS for V-02 (impl-cli gate floor, 8 agents).
- Relied on rf-qa PASS for the Phase 9 renumbering and cross-references.
- Relied on rf-qa PASS for gate counts against full-intensity floors.
- Relied on rf-qa PASS for the POST reflect runner prompt (byte-identical to the template).
- Relied on rf-qa PASS for phase order and the absence of commit or push items.
- Relied on rf-qa PASS for I-3 (8.3 and 8.4 field names).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- The POST diff inputs, where the runner-prompt PASS was not enough: the template match says nothing about what `phase1.diff` contains. I ran `git ls-files --others --exclude-standard -- src tests docs plugins`, which lists the DESIGN and three review documents as untracked before any task work (OPS-01).
- The 14.8 timing rule, where the V-01 path PASS was not enough: I read REPORT:1300 ("Run `superclaude sweep --help` once [...] time limit 30 s") and `pyproject.toml:2-3` and the dependency list, and found the limit applied to install plus help (OPS-02).
- The routing and test sequencing, where the phase-order PASS was not enough: I read `test_how_we_work_routing_table.py:27-40,291-311`, `test_routing_refresh.py:30-36,645-650` and `test_worker_contract.py:755-839,889-913,1940-2012` to confirm that no test runs between dependent edits.
- Signature conformance: I read DESIGN 7.1 to 7.4 (lines 351-590) against items 8.2 to 9.1.
- Anchors: I verified every cited line in main.py, HOW-WE-WORK.md, commands.md, CHANGELOG.md, the developer guide, WORKER-CONTRACT.md, `.gitignore`, recovery.py, atomic.py, test_conflict_scripts.py, graph.md, issue.md and sc-graph-protocol SKILL.md with sed and grep.
- The SPEC FR-004 and FR-021 rows (merged-requirements.md:98,115) against items 10.1 and 10.3 (M-01, M-02).
- Makefile `lint-architecture` Checks 1 to 11 against the new command and skill pair (M-05).

**Answers:**
1. Factual claims independently verified against source: about 75 (line anchors, signatures, test assertions, make targets, git state).
2. Files read: the task file (Phases 1, 8 to 14 and the Execution Context), BUILD-REQUEST.md, DESIGN sections 3, 5, 7, 8, 9, 10 and 11, research/09 Gap 6, SPEC FR-004 and FR-021, REPORT:1300, main.py, `cli/__init__.py`, recommend `__init__.py`, test_worker_contract.py, test_how_we_work_routing_table.py, test_routing_refresh.py, test_routing_plugin_parity.py, test_help_command.py, test_graph_command.py, test_conflict_scripts.py, pyproject.toml, Makefile, arch_lint.py, `.gitignore`, HOW-WE-WORK.md and its plugin copy, commands.md, CHANGELOG.md, the developer guide, WORKER-CONTRACT.md, recovery.py, atomic.py, graph.md, issue.md, sc-graph-protocol SKILL.md, sc-reflect-protocol SKILL.md and APPROVED.md.
3. Not applicable: 10 findings, 2 blocking.
4. No web research was done; Tavily was not needed.

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 19 | Grep: 7 | Glob: 0 | Bash: 18

VERDICT: FAIL
