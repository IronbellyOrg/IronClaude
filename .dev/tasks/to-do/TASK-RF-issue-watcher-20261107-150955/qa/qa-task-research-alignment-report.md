# QA Report: Task Integrity, Lens task-research-alignment

**Topic:** GitHub issue watcher (issue 331), TASK-RF-issue-watcher-20261107-150955
**Date:** 2026-11-07
**Task file:** TASK-RF-issue-watcher-20261107-150955.md (925 lines, 176 items)
**Research:** research/01..06 (06 authoritative); design docs/designs/issue-watcher.md (935 lines)
**Stance:** adversarial; assume the builder dropped or misrepresented findings.

Status: COMPLETE. Verdict: FAIL (3 IMPORTANT blocking, 13 MINOR). Verdict line at the end of the file.

---

## 0. Method

Read in full: the task file (all 925 lines; grep counts 176 `- [ ]` items and 176 `**Step` headers), research 06 (all 327 lines), research 05 (sections 1, 2, 3, 4, 5, 7 and the gap list), research 01 (F1 to F8), research 02 (E, F, G), research 03 (sections 4 to 9), research 04 (Parts B to E), BUILD-REQUEST.md, design sections 4, 6, 7.5-7.6, 8.4-8.5, 10, 11 to 18 and the C-rows, and spec lines 96-108 and 326-361. DF coverage was computed by script (`/tmp/qa-align/df.py`, maps every `DF-nn` mention to the `- [ ]` item that carries it); spot checks were done by grep against the task file. Nothing in the task, design, spec or research was modified.

Result in one line: the task applies all 60 decisions and all 29 DEVIATION rows, but 3 items carry a wrong or missing treatment (Section 9: I-1 to I-3) and a set of smaller gaps is listed as MINOR. Verdict at the end of the file.

---

## 1. Decision register DF-01 to DF-60: item numbers that apply each

Item numbers are task "Step" ids (core items only; QA-gate prompt items 3.G5, 9.M1 etc. that repeat a DF for the reviewer are not listed). "Applied" means the item text states the decision's treatment, not merely cites the id.

| DF | Dev. | Applied by items | Check |
|---|---|---|---|
| 01 | yes | 2.1, 2.5, 5.1, 5.4, 5.5, 9.18 | Applied: keyword-only `cwd`, `FakeRunner` records `(argv, cwd)`, only `OrcaLauncher.launch` passes cwd, `check_origin` passes none |
| 02 | yes | 2.3, 2.8, 3.1, 3.7, 6.2, 6.7, 9.18 | Applied (57 names). See I-1 for the paging reason inside 3.1 |
| 03 | yes | 2.3, 2.8, 4.1, 4.5, 7.2, 7.5, 9.18 | Applied (decision line, warning line, no cycle line, fresh cycle_id) |
| 04 | yes | 4.1, 4.5, 7.2, 7.5, 9.18 | Applied (exit 2, one `reset_refused` warning line, store bytes identical) |
| 05 | yes | 7.7, 9.5, 9.18, 9.19 | Applied (G-2 subset, "full suite: CI only") |
| 06 | yes | 7.1, 7.2, 7.4, 7.6, 9.14, 9.18 | Applied (five names, six usage forms) |
| 07 | yes | 1.3, 10.2, 10.3, 10.4, 10.8, 9.18 | Applied (BASE immediately before the commit, six-prefix allowlist, HALT, branch check, final `git add .dev/tasks`). Baseline goes to a file, not the Task Log (MINOR m-2) |
| 08 | no | structure: Gates A to D, 9.F1-9.F13, 9.M1-9.M8; Overview; OQ-34 | Applied: 6/6/6/6/7/3 = 34 lens agents, Final before M4, lens names match Table 1.6 exactly |
| 09 | yes | 1.4, 2.11, 3.10, 4.7, 5.11, 6.11, 7.9, 8.12, 9.8, 9.12 | Applied (pinned `uvx --offline ruff@0.15.20`, G-7 grep identical to Table 1.2) |
| 10 | yes | 8.1, 8.2, 9.18 | Applied (stubs generated at test time, 4 names, no `stubs/` dir) |
| 11 | no | 5.1, 5.5 | Applied (`ORCA_AGENT = "claude"`, test holds literal, no `.dev/` read) |
| 12 | yes | 8.3, 9.18 | Applied (`random.Random(331)`, 2,000 draws, no marker). Item says the seed and count are fixed by D 693 (correct per r3 M3) |
| 13 | yes | 6.1, 6.5, 7.1, 7.4, 9.18 | Applied (expanduser only for default and `--config`; HOME test) |
| 14 | no | 3.1, 3.4, 3.6 | Applied (Table 1.5 text, nullable `$after`) |
| 15 | yes | 4.1, 4.2, 4.3, 8.4, 9.18 | Applied (CrashingStore points, C2 `os.replace` one-shot patch, 5 reruns, lock released in `finally`) |
| 16 | no | 2.2, 2.7 | Applied (`max(created_at, updated_at)`, edited-old-comment test) |
| 17 | yes | 4.1, 4.3, 6.2, 6.7, 9.18 | Applied (migrate in memory, dry-run never saves) |
| 18 | yes | 3.1, 3.3, 3.7, 9.18 | Applied (null only for fields a predicate reads; renamed-with-null-label fixture and test). G5 null `author` rule not stated (m-9) |
| 19 | no | 3.1, 3.7 | PARTLY WRONG: 3.1 sends an over-100 REST page to `events_incomplete`; DF-19 says `events_unreadable`. See I-1 |
| 20 | yes | 6.1, 6.5, 9.18 | Applied (comma and double quote rejected, test) |
| 21 | no | 2.2, 3.1, 3.6, 5.8 | Applied (`MARKER_JQ` built from `CLAIM_MARKER`) |
| 22 | yes | 2.3, 2.8, 6.2, 6.6, 6.7, 9.18 | Applied (`dry_run_shadow_reset`, skew 60/61, discovery 79/80) |
| 23 | no | 6.1, 6.5 | Applied (`fs_type_of` pure, escape decoding, longest prefix) |
| 24 | yes | 2.4, 5.3, 9.18 | Applied (`FakeLauncher(outcomes)`, `FakeClock(now, mono)`) |
| 25 | yes | 6.3, 9.18 | Applied (`slo_numbers(lines, doc, now)`) |
| 26 | no | implicit in 1.5, 1.4, 7.1, 7.4 | Applied without citing the id (`reflect/commands.py:222`, lines 4-5, `test_cli_smoke.py:7,17,21,46`, `test.yml:22`) |
| 27 | yes | 1.7, 9.18 | Applied (reason is the repository convention, no collision claim) |
| 28 | yes | 3.1, 3.6, 8.3, 9.18 | Applied (`--method GET` on every `gh api` argv except G1 and graphql) |
| 29 | yes | 7.3, 8.8, 9.18 | Applied (eager import after line 561, exact text, `ast.walk`) |
| 30 | no | 2.3, 4.1 | Applied (private `_fsync_dir` in both) |
| 31 | no | 2.8, 5.5, 8.4, 9.1, 10.3 | Applied (literals in tests, design committed unchanged) |
| 32 | no | 3.2, 3.4, 3.6, 9.1, 9.3, 9.19 | Applied (fixtures parse with `json.loads`, placeholder ids, runbook read against markdownlint) |
| 33 | no | 2.3 | Applied (`AuditLog(state_dir)`, `.1`-`.4`, 5 MiB) |
| 34 | no | 8.1, 8.2, 8.5 | Applied (`CliRunner` in test_cli, subprocess in e2e, multiprocessing spawn) |
| 35 | no | 2.2, 2.7, 3.1, 3.6 | Applied (`strptime`, `timezone.utc`, header parsing, G-7 includes `fromisoformat`) |
| 36 | no | 5.1, 5.4, 5.6 | Applied (non-dict shapes rejected without raising; parity only for the two safe shapes) |
| 37 | no | 3.1, 3.5, 3.6 | Applied (no exit-code rule) |
| 38 | no | Task Overview text ("eight modules plus an empty `__init__.py`") | Applied |
| 39 | no | 2.4, 6.4, 6.5, 7.4, 8.1, 8.5 | Applied |
| 40 | no | Open Questions (OQ-1 to OQ-46), 9.18, M4 prompts 9.M1 to 9.M3 and 9.M7 | Applied (29 rows, Q1-Q4, X1-X5, gate-sizing tension) |
| 41 | no | 2.3, 2.8, 6.1, 6.5 | PARTLY APPLIED: table created and pinned; the sentence "`cycle.resolve_exit` reads the exit from the table" and the kind check are not carried into cycle items. See I-2 |
| 42 | yes | 4.1, 4.4, 9.18 | Applied (`last_reason` str or null; membership test in test_record) |
| 43 | yes | 4.1, 4.4, 6.2, 6.7, 9.18 | Applied (`fail` from `failed`, attempts to 3) |
| 44 | yes | 4.1, 4.5, 9.18 | Applied (`sweep` and `day_cap_count` take `StoreDoc`) |
| 45 | no | 6.1, 7.1 | Applied (`Deps`, `CycleResult` in `cycle.py`) |
| 46 | no | 5.8 | Applied (tracked `src/...` copies required, others when present) |
| 47 | no | 6.2, 6.7 | Applied (account-rename case) |
| 48 | yes | 2.4, 6.4, 9.18 | Applied (`CommandResult | Callable`) |
| 49 | no | 3.2, 3.3, 3.4, 3.5, 5.2 | Applied: all 13 fixture file names equal research 05 section 3 |
| 50 | yes | 6.2, 6.3, 6.7, 7.4, 9.18 | Applied (S1 two cases, full-argv retry, 3600 s clamp, `last_completed_cycle_at`, status exit 1) |
| 51 | no | 6.2, 6.6 | Applied (`Retry-After: 120` on G1; per-issue clamps) |
| 52 | no | 6.1, 6.5, 7.4 | Applied (`_read_mountinfo` monkeypatch point) |
| 53 | no | 6.1, 6.5, 7.1, 7.5 | Applied (shared check, tested once for `init-state`) |
| 54 | no | 5.1, 5.4 | Applied (`which` keyword, signature inspected) |
| 55 | yes | 2.1, 2.5, 6.6, 8.1, 8.2, 9.17, 9.18 | Applied (a: `sleep`/`matched`; b: state snapshot; c: inline sleeper at P2; d: in-process) |
| 56 | no | 1.8, 2.4, 4.2, 5.3, 6.4, 8.1 | Applied (conftest in five parts, P1 exit 5) |
| 57 | yes | 2.3, 2.8, 6.6, 7.2, 7.5, 9.18 | Applied except two untested branches (m-4) |
| 58 | no | 9.16, 9.19, phase 2 header | Applied |
| 59 | no | 9.15, 10.3 | Applied |
| 60 | yes | 9.1, 9.18 | Applied (separate runbook, design not edited) |

NOT APPLIED: none. PARTLY WRONG or PARTLY APPLIED: DF-19 (I-1), DF-41 (I-2).

## 2. Design section 11 files and section 12 tests: creating item and phase

Phase assigned by research/06 Section 2; "item" is the item that creates the file (later parts append to it).

| Design file (section 11) | 06 phase | Creating item | Task phase | OK |
|---|---|---|---|---|
| `issue_watch/__init__.py` | P1 | 1.6 (zero bytes) | P1 | yes |
| `runner.py` | P2 | 2.1 | P2 | yes |
| `predicates.py` | P2 | 2.2 | P2 | yes |
| `audit.py` | P2 | 2.3 | P2 | yes |
| `github.py` | P3 | 3.1 | P3 | yes |
| `record.py` | P4 | 4.1 | P4 | yes |
| `launch.py` | P5 | 5.1 | P5 | yes |
| `cycle.py` | P6 | 6.1 (creates), 6.2 and 6.3 append | P6 | yes (three items, one file; declared in the phase header) |
| `cli.py` | P7 | 7.1 (creates), 7.2 appends | P7 | yes |
| `main.py` (two lines) | P7 | 7.3 | P7 | yes, text identical to DF-29 and research 01 F1 |
| `tests/issue_watch/__init__.py` | P1 (06 P1 row; r3 gap M-7) | 1.7 | P1 | yes |
| `conftest.py` | P2, P4, P5, P6, P8 | 2.4, 4.2, 5.3, 6.4, 8.1 | same | yes (DF-56 split exact) |
| `test_runner.py` | P2 | 2.5 | P2 | yes |
| `test_predicates.py` | P2 | 2.6, 2.7 | P2 | yes |
| `test_audit.py` | P2 | 2.8 | P2 | yes |
| `test_github.py` | P3 | 3.6, 3.7 | P3 | yes |
| `test_record.py` | P4 | 4.3, 4.4, 4.5 | P4 | yes |
| `test_launch.py` | P5 | 5.4, 5.5 | P5 | yes |
| `test_find_orca_parity.py` | P5 | 5.6 | P5 | yes |
| `test_origin_parity.py` | P5 | 5.7 | P5 | yes |
| `test_marker_contract.py` | P5 | 5.8 | P5 | yes |
| `test_cycle.py` | P6 | 6.5, 6.6, 6.7, 6.8 | P6 | yes |
| `test_slo_helper.py` | P6 | 6.9 | P6 | yes |
| `test_cli.py` | P7 | 7.4, 7.5 | P7 | yes |
| `test_cli_e2e.py` | P8 | 8.2 | P8 | yes |
| `test_security_invariants.py` | P8 | 8.3 | P8 | yes |
| `test_crash_injection.py` | P8 | 8.4 | P8 | yes |
| `test_concurrency.py` | P8 | 8.5 | P8 | yes |
| `test_no_shell.py` | P8 | 8.6 | P8 | yes |
| `test_no_text.py` | P8 | 8.7 | P8 | yes |
| `test_module_boundaries.py` | P8 | 8.8 | P8 | yes |
| `fixtures/_assumed_shape/*.json` (13) | P3 (06 P3 row names the folder) | 3.2 to 3.5 (11 files), 5.2 (2 Orca files) | P3 and P5 | 11 yes; the 2 Orca files sit one phase later than the 06 row (m-3) |
| `stubs/gh`, `stubs/orca` | replaced by DF-10 | none by design (written in `tmp_path` by 8.1) | P8 | yes (deviation DF-10 recorded as OQ-9) |
| `docs/designs/issue-watcher-setup.md` | P9 | 9.1, 9.2 | P9 | yes |

Count check: 8 per-module + 11 cross-cutting test files = 19 (task 10.1 lists the same 19 names), 13 fixtures (2+2+2+5+2), 9 source files, 1 registry edit, 1 runbook. Matches Overview and 10.1.

Design section 12 tests: `test_crash_injection` (8.4), `test_concurrency` (8.5), `test_cycle::test_fifty_cycles` and `::test_acceptance_property` (6.8, N in {1,2,6,7,50,99}), `test_no_shell` (8.6), `test_no_text` (8.7), `test_module_boundaries` (8.8), `test_marker_contract` (5.8). All present. Section 12 seams: `FakeRunner` (2.4), `FakeClock` (2.4), `FakeLauncher` (5.3), `CrashingStore` (4.2), PATH stubs (8.1): all present with the DF-48, DF-24, DF-10 corrections.

## 3. AC-1 to AC-25 and FR/NFR traceability

Method: for each criterion (design 872-898) I looked for the item whose test text asserts what the criterion says. "Id cited" = the string `AC-n` occurs in the task body (grep count).

| AC | Proving items | Id cited | Gap |
|---|---|---|---|
| 1 | 6.6 (idle = 2 gh calls, order), 8.2 | yes (6) | none |
| 2 | 3.6 (FR-003 literal incl. `-L 100`), 3.7 and 6.6 (99/100/101, repeated number, exit 4) | no | none in content |
| 3 | 2.6, 6.7 (events_incomplete, edited_after_approval) | no | none in content |
| 4 | 2.7, 6.7 | no | none in content |
| 5 | 6.7 (own marker gives claimed, launched+marker, no entry+marker) | yes | none |
| 6 | 6.7 (FR-010 `on_call` reads `dispatch.json`, FR-011 re-read), 8.2 snapshot | no | none |
| 7 | 8.3 | yes | none |
| 8 | 5.4, 5.5, 6.7 (FR-014 outcomes) | no | none |
| 9 | 7.4 (stale and retry with full argv), 6.7, 6.8 | yes | "no automatic retry" half has no dedicated case (m-5) |
| 10 | 4.5 (consumed_log through reset), 6.8 | yes | none |
| 11 | 8.5, 4.3, 7.5 | no | foreign-owner lock only at record level (m-13) |
| 12 | 6.6 | no | none |
| 13 | 6.7 (dry-run byte-identical, `dry-run.json`) | no | none |
| 14 | 6.6, 7.5, 2.8 | yes | none |
| 15 | 6.5 (precedence over every pair), 6.6 (matrix) | no | none |
| 16 | 5.4, 5.7, 6.6 | yes | none |
| 17 | 7.4, 7.5 | yes | reset with invalid config untested (m-4) |
| 18 | 6.6, 4.5, 7.5 | no | none |
| 19 | 2.5 (inline sleeper), 6.6 (in-process 236 s and 121 s), 8.1/8.2 (snapshot) | yes (7) | split exactly as DF-55 |
| 20 | 8.3 | yes | none |
| 21 | 8.6 | no | none |
| 22 | 8.4, 6.8 | no | none |
| 23 | gates G-4, G-6, G-10 (9.7, 9.9-9.11, 9.15) | yes (4) | none (OQ-5 records the `make test` departure) |
| 24 | 6.9 | yes | none |
| 25 | 8.8, 5.6, 5.7 | yes (7) | none |

Content coverage of all 25 criteria is present. What is missing is the binding between a criterion and a test the executor can search for: 12 of 25 ids (AC-2, 3, 4, 6, 8, 11, 12, 13, 15, 18, 21, 22) are never written next to the test that proves them, no test item tells the executor to carry the id in a test name or docstring, and item 9.17 must "use Grep to find the test functions that prove each criterion". The FR and NFR side is worse: grep finds no mention of FR-005, FR-008, FR-013, FR-017, FR-018, FR-019, FR-024, FR-025, FR-026, FR-027, NFR-004, NFR-005, NFR-006, NFR-008, NFR-011, NFR-012, NFR-013 in any item; the only P9 artefact (ac-trace.md, 9.17) has no FR/NFR column; the FR/NFR check exists only inside the prompt of 9.F8 ("every FR and NFR cited in the criterion table ... maps to some test") and the M4 spec agent (9.M2). Research 05 section 5 already holds the FR/NFR to test map with the AC id per row and was not carried. See I-3.

## 4. Research files: key findings and the item that acts on each

| Research file | Key finding | Acting item | Result |
|---|---|---|---|
| 01 F1 | `main.py` pair text, position after 561, eager import, `noqa` suffix | 7.3, 1.5 | acted, text identical |
| 01 F2/F3 | five commands; hyphenated names explicit; `sys.exit` idiom; no `exists=True` on `--config` | 7.1, 7.2 | acted |
| 01 F4 | `cli.py` name kept; package marker | 1.6, 7.1 | acted |
| 01 F5 | `from __future__`, frozen dataclasses, plain `Protocol` | Phase 2 header, 2.1 | acted |
| 01 F6 | arch_lint Check 11 (no `THRESHOLDS`, no id-pattern literal), N-rules lowercase argv builders, relative-import rule | 2.2, 2.3, 3.1, 6.1, 3.9 | acted |
| 01 F6 | pre-commit hooks (check-json, detect-secrets, shellcheck, markdownlint) | 3.2-3.4, 3.6, 9.3 | acted (DF-32) |
| 01 F7 | no registry edit; do not add to `EXPECTED_TOP_LEVEL_COMMANDS` | none (correctly absent) | acted by omission |
| 02 E | import vs copy: `write_prepared_bytes`, `_ORCA_CLIS` imported; `_find_orca`, `parse_origin_url` mirrored | 4.1, 5.1, 5.6, 5.7 | acted |
| 02 F | three marker copies, src required | 5.8 | acted |
| 02 G1 to G15 | cwd, `--method GET` scope, 2 missing reasons, `marker_time`, real `orca-ide` shadowing, 5 reruns, `which` kw, dry-run migration, retry argv, `ORCA_AGENT`, lazy-import claim, null fields, page > 100, comma labels, one marker constant | via DF-01, 28, 02, 16, 10, 15, 54, 17, 50, 11, 29, 18, 19, 20, 21 | all acted; DF-19 mis-stated inside 3.1 (I-1) |
| 03 sec 4 | autouse fixtures, `_pollution_snapshot`, scrub `REFLEXION_OUTPUT_DIR` | 2.4, 8.1 (env holds only HOME, XDG, `IW_STUB_*`, PATH) | acted |
| 03 sec 5 | xdist rules, 3.10 floor, grep self-check | 8.10, 9.6, 9.12, Phase 2 header | acted |
| 03 sec 6 | gate commands, ruff 0.17.3 vs pin, `make test` unsafe locally, `.claude/skills` absent until sync | 7.7, 9.5, 9.8, 9.10, 9.11 | acted (DF-05, DF-09) |
| 03 sec 7 | AST tests with mutation guard, spawn context with bounded joins, SystemExit crash, seeded random, no marker, hostile text, marker dual surface | 8.5, 8.6, 8.8, 8.4, 8.3, 8.7, 5.8 | acted |
| 03 gaps | flat `"$*"` stub logs unfit for exact argv | 8.1 (one record per argv element) | acted |
| 04 B | skill-mode frontmatter, no `start_commit`/`executor_model_class`, `created/template/tracks`, POST item verbatim and penultimate, Done last, anti-orphaning, evidence-absence comments, TCS depth | frontmatter, 10.6, 10.7, items, "Reflect Depth Derivation" | acted |
| 04 B.5 | rule 16 gate floor conflict | OQ-34 | acted |
| 04 B TB-Add-7 | Execution Context must not hold `src/` or `path:NN` | Source Areas clean; GOAL line 108 still has `src/superclaude/...` | partly (m-7) |
| 04 D/E | one item per file, scoped ruff incl. `format --check`, duplicate-operation reasons stated | per-phase G-5 items, 8.11, 9.13 | acted |
| 05 sec 1 | module APIs and traps (T-A to T-S) | 2.1 to 7.2 | acted; T-F and T-J superseded by DF-11 and DF-10 |
| 05 sec 2.3 | account rename, 5 reruns, `test_second_once_launches_nothing`, NFR-012 gate-only | 6.7, 8.4, 6.8, 9.17 | acted |
| 05 sec 3 | 13 fixture names, stub scenario format | 3.2-3.5, 5.2, 8.1 | acted |
| 05 sec 4 | 15-section runbook outline | 9.1, 9.2 | acted, all 16 sections 0-15 |
| 05 sec 5 | FR/NFR to test map | not carried (see I-3) | dropped |
| 05 X1-X5 | spec-vs-design choices | 6.2, 6.7, 7.4, OQ-26 | acted |
| 06 | all 60 decisions, Tables 1.2 to 1.6, phase plan | whole task | see Sections 1 to 3 |

## 5. Research edge cases present in the verification criteria

| Edge case | Where | Verdict |
|---|---|---|
| Crash points C1 to C5, five reruns, six runs, launcher calls <= 1, `launches` never 0 after a call | 8.4 (and Objective 3, Gate D prompts 8.G3, 8.G5, 8.G7) | present; durable-state assertions per point match Table 1.3 incl. "unchanged" for C1 and "orphan tmp always exists" for C2 (r3 depth N-3, N-4 folded) |
| `FileStore.lock` releases in `finally` so the lock is free after `SystemExit` | 4.1, 4.3, 8.4 | present |
| C2 injected by a one-shot `os.replace` patch, not by the Store seam | 4.2 docstring rule, 8.4 | present |
| AC-19 split a, b, c, d | 8.1 (sleep, matched), 8.2 (snapshot), 2.5 (inline sleeper, `timeout=0.5`, not the P8 fixture), 6.6 (exit 3, 236 s, 121 s) | present |
| Stub protocol: scenario file, log header with `matched`, one record per argv, `IW_STUB_STATE_DIR` snapshot, interpreter symlink, PATH without `/usr/bin`, `shutil.which` guard for four names, teardown failure on `matched` false | 8.1, 8.2 (4) | present, line by line |
| Rename events ignored by label predicates, `renamed` after approval is a change | 3.3 fixture, 3.7, 2.6 | present |
| Reset audit exits (success x2, no entry, not abandoned/unknown, 75, 6 x4 reasons, unwritable dir) with fresh `cycle_id`, `dry_run` false, never a cycle line | 7.2, 7.5 | present except reset with invalid config and Click parse error (m-4) |
| Reason list of 57 names as a literal in the test, plus kind and exit per name | 2.3, 2.8 | present; counts verified: 7+5+5+2+2+1+3 = 25 cycle names, 17 skip, 9 entry, 1 note, 3+1+1 warning = 57 |
| `ORCA_AGENT = "claude"` as a literal in the test, never read from `.dev/` | 5.1, 5.5 | present |
| xdist form `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/`, zero skips | 8.10, 9.6 | present |
| Pinned ruff forms, `check` and `format --check`, full tree at P9 | every G-5 item, 9.8 | present |
| Exact `main.py` insertion text and blank-line layout | 7.3 | present, identical to DF-29 |
| G-1 exit 5 at P1 only | 1.8 | present |
| S1 two cases with k = min(10, floor(32/r)) = 8 | 6.7 | present |
| `Retry-After: 120` only observable on G1 | 6.6 | present |
| Network-FS check shared by `once`, `check-config`, `init-state`; injectable `_read_mountinfo` | 6.1, 6.5, 7.5 | present |
| Account rename (NFR-005) | 6.7 | present |
| Second `once` launches nothing (NFR-010) | 6.8 | present |
| P1 baseline, branch not master/main, allowlist HALT, no `--no-verify`, no `git add -A` | 1.3, 10.2, 10.3, 10.4 | present |

## 6. Dependencies between components versus phase order

Checked build order runner, predicates, audit, github, record, launch, cycle, cli, main.py (research 05 sec 1 and 06 Section 2) against the item order:

- `test_predicates` 2.7 reads `audit.REASONS`: audit is 2.3, earlier. OK.
- `github.py` 3.1 uses `predicates.parse_utc`, `valid_issue_number`, `CLAIM_MARKER`: P2. OK.
- `test_record` 4.4 asserts `last_reason` membership in `audit.REASONS`: P2. OK (DF-42).
- `conftest` part 2 (4.2) imports `record`, part 3 (5.3) imports `launch`, part 4 (6.4) imports `cycle`, part 5 (8.1) needs nothing later: no module-level import of a module a later phase creates (DF-56). OK.
- `test_marker_contract` 5.8 uses `github.MARKER_JQ` (P3). OK.
- `launch.py` 5.1 needs `runner` and `install_user_setup._ORCA_CLIS`; the two Orca fixtures (5.2) need `OPERATION_ID_PATHS` from 5.1, which is why they sit in P5. OK, but this departs from the 06 P3 row (m-3).
- `cycle.py` 6.1 to 6.3 need `github`, `record`, `launch`, `audit`: all earlier. `status_report` 6.3 uses `launch.retry_argv` and `_ORCA_CLIS`: 5.1. OK.
- `cli.py` 7.1 needs `cycle`: P6. `main.py` 7.3 after `cli.py` (7.1, 7.2). G-9 (7.6) after 7.3. OK.
- Gate order: Gate A (P2, P3), B (P4, P5), C (P6, P7), D (P8), then runbook (9.1, 9.2) and full gate run before Final M3 (9.F), then M4 (9.M), then P10. Each phase header requires the previous gate verdict PASS file. OK.
- G-2 first runs at 7.7 and again at 9.5 (runbook now exists and is scanned by the model-alias and retired-docs tests). Reason stated. OK.

No ordering defect found.

## 7. Deviations and open questions section

- 29 DEVIATION rows: OQ-1 to OQ-29 correspond one to one, in DF order, with the D/S lines from register column 6 (verified id by id: 01, 02, 03, 04, 05, 06, 07, 09, 10, 12, 13, 15, 17, 18, 20, 22, 24, 25, 27, 28, 29, 42, 43, 44, 48, 50, 55, 57, 60). The count in DF-40, the Overview ("Twenty-nine"), 9.18, and the three M4 prompts (9.M1, 9.M2, 9.M3, 9.M7) are consistent.
- Q1 to Q4: OQ-30 to OQ-33. X1 to X5: all five named inside OQ-26, not as separate entries (acceptable, DF-50 treats them as one row; see m-11).
- DF-08 gate-size tension: OQ-34. Commit authority (DF-07): OQ-7 and OQ-35. Remaining gaps: OQ-42 to OQ-46. Staleness corrections: section F.
- Builder-originated readings that are not in the register: OQ-36 (an in-backoff `failed` entry also gets the events read; contradicts the sentence of spec line 103, consistent with design step 11 and T-12), OQ-37 to OQ-40, OQ-41, OQ-41a (probe cache held by the cycle instead of the `OrcaLauncher` instance of D 614). They are listed under section D, and the M4 prompts exempt "the other proposal values listed in the Open Questions section". OQ-41a and OQ-36 are real departures from literal source text and would be cleaner as register rows (m-11).

## 8. Fabrication check

I looked for items that cite a file, symbol, pattern or requirement present in neither the research nor the design/spec.

- Every `DF-nn` in the task is in 01..60 (script check: no id above 60). No research 05 `G-nn`/`X-nn` or research 02 `G1..G15` id is used as a task id (collision rule of 06 line 11 respected). Gate rows `G-1..G-11` are the only hyphenated G ids.
- Every repository path cited in items exists (checked with ls: the 6 G-2 test files, `poll-augment-review.sh`, `tests/skills/test_issue_repo_resolution.py`, `tests/pr_submit/test_conflict_scripts.py`, `tests/docs/test_retired_docs_absent.py`).
- Names the task coins that no source fixes (`github.Read`, `github.Reply`, `timeout_for`, `PendingContext`, `SloNumbers`, `OPERATION_ID_PATHS` value, `FileStore.migrated`, `CycleResult` fields, `rate_limit_wait`, `argv_*` builder names) are all disclosed in OQ-41. Not fabricated.
- Two items state rules with no source: the SLO (c) denominator ("launched lines whose lease has ended or that reached `claimed`", 6.3) goes beyond D 745 and S 229 and is not disclosed (m-8); the skip condition in 8.2 (temporary directory on a deny-listed filesystem) comes from research 05 T-C but is not in any DF row (m-12).
- No requirement, file, or pattern was invented. No TBD/TODO/FIXME token exists.

## 9. Issues

### Blocking (IMPORTANT)

**I-1 (IMPORTANT, blocking): Step 3.1 and Step 3.7 contradict DF-19 and DF-02 for an over-long REST page.**
Evidence: item 3.1 (line 230 of the task) says "more than 5 pages, a repeated `id` on a later page, or a page longer than 100 gives `events_incomplete` for events and `marker_unreadable` for the marker read". DF-19 (06 line 146) says a REST page longer than 100 is "unreadable: `events_unreadable` (G3), `marker_unreadable` (G4)". DF-02 gives `events_incomplete` only for the two D 571 conditions (more than 5 pages, repeated id). Item 3.7 (line 248) then tests "101 items (unreadable)" without naming the reason, so the item pair is internally inconsistent and the executor will write code and tests for the wrong G3 reason (the audit `reason` differs; the skip is still exit 0).
Fix, item 3.1: replace the clause with "more than 5 pages or a repeated `id` on a later page gives `events_incomplete` for events and `marker_unreadable` for the marker read; a page longer than 100 items gives `events_unreadable` for events and `marker_unreadable` for the marker read (DF-19)".
Fix, item 3.7: replace "101 items (unreadable)" with "101 items (`events_unreadable` for the events read, `marker_unreadable` for the comments read)" and add "a sixth page and a repeated id give `events_incomplete`" so both reasons are asserted.

**I-2 (IMPORTANT, blocking): DF-41 is only half applied; no cycle item makes the exit code and line kind come from `audit.REASON_TABLE`.**
Evidence: `REASON_TABLE` occurs in the task only in 2.3 (creation) and 9.2 (runbook). DF-41 (06 line 175) decides "One table feeds the pin test, the exit mapping and the kind check ... `cycle.resolve_exit` reads the exit from the table". Item 6.1 defines `resolve_exit(conditions: frozenset[int])` and 6.2 raises exit conditions at call sites with literal reasons; 6.6 only checks that "each of the exits ... appends exactly one cycle line whose `exit` matches". Nothing ties a reason the cycle emits to its table row, so a typo such as exit 3 for `gh_non_json` or a `skip` reason written on a `cycle` line passes every test, and the pinned table could drift from behaviour.
Fix, item 6.1: add "and a helper `exit_for(reason) -> int` returning `audit.REASON_TABLE[reason][1]`; every exit condition `run_cycle` raises is `exit_for(<reason>)`, never a literal other than 0 (DF-41)".
Fix, item 6.6: add "a table-driven test over every reason of kind `cycle` that a scenario of this part can produce: the cycle line `exit` equals `REASON_TABLE[reason][1]`; and for decision and warning lines written in parts C and D the line `kind` is allowed by `REASON_TABLE[reason][0]` (DF-41 kind check)".

**I-3 (IMPORTANT, blocking): AC, FR and NFR ids are not bound to the tests that prove them, and item 9.17 has no FR/NFR trace.**
Evidence: Section 3 above. 12 of 25 AC ids and 17 FR/NFR ids appear nowhere in the item text; no test-creating item tells the executor to carry the id in a test name or docstring; 9.17 builds the trace by grepping for "the test functions that prove each criterion" and its table has no FR/NFR column; the only FR/NFR check is inside the 9.F8 prompt and 9.M2. Research 05 section 5 already contains the FR/NFR to test map (with the AC id per row) and was not carried, so the executor has nothing to grep for and a GAP found at 9.17 would trigger late test additions.
Fix, Phase 2 header paragraph (inherited by every test item; repeat one clause in the Phase 8 header): "Every test function name or the first line of its docstring names the ids it proves, for example `test_ac3_outsider_relabel__fr005_fr006`, taken from the Ids column of design lines 872-898 and from research/05 section 5."
Fix, item 9.17: add "the table has the columns AC, Ids (the FR/NFR ids of the design's Ids column), test file and function, result; a second table lists every FR-001 to FR-029 and NFR-001 to NFR-014 of design section 18 (lines 902-934) with its test, NFR-012 marked gate-only (G-4, G-6, G-10)".

### Non-blocking (MINOR)

- m-1: Item 1.6 says "Read design lines 751 and 11"; line 11 of the design is not the files table (section 11 is meant). Write "design line 751 (section 11)".
- m-2: DF-07 item (1) says the origin/master SHA and merge-base are written to the Task Log; item 1.3 writes `phase-outputs/discovery/git-baseline.md` only. Add one line to the Phase 1 Findings section, or accept the file.
- m-3: The two Orca fixtures are created in 5.2 (P5); the 06 P3 row assigns `fixtures/_assumed_shape/*.json` to P3. The reason is sound (`OPERATION_ID_PATHS` exists only after 5.1). Record it in OQ section D.
- m-4: DF-57 branches not tested in 7.5: `reset` with an invalid config (stderr fallback `config_invalid`, exit 2) and "Click parse errors write nothing". Add both to 7.5.
- m-5: AC-9 first half and design NG-5 ("no automatic Orca retry"), and research 05's FR-015 row ("no orca argv for `unknown`"), have no dedicated case. Add to 6.7: an `unknown` entry in two later cycles produces no launcher call and stays `unknown`.
- m-6: Item 2.3 makes `clock_skew_s` optional on the cycle line; design 10.1 marks it present on every cycle line. Either keep and record, or state "present on every cycle line, null when the `Date` header was unparseable".
- m-7: The GOAL line (task line 108, verbatim from BUILD-REQUEST) contains `src/superclaude/...`; the consumer-side TB-Add-7 spot check `grep -cE "src/|/.*:[0-9]+"` on the Execution Context block returns 1 (checked on lines 104-151). The Source Areas sub-block is clean. The check is optional and the GOAL must be verbatim; note the known hit in the Task Log so it is not read as a regression.
- m-8: The SLO (c) denominator in 6.3 ("launched lines whose lease has ended or that reached `claimed`") is a builder rule not in D 745 or S 229. Add to OQ-41 or use the literal "launched lines" denominator.
- m-9: r3 minors not folded: evidence M6 (a G5 comment with `author: null` means "not own login", fixture exists in 3.4 but 3.1 and 3.7 state no rule), cross-validation R3-M10 (8.2 should say `-m superclaude.cli.main` is test internals, not an operator command, so an executor does not "correct" it under the UV rule), R3-M2 (G-10 `git diff --exit-code` does not see staged changes; add `--cached` in 10.3).
- m-10: Research 05 names `test_shared_failure_matrix` for NFR-007; 6.6 has the matrix unnamed. Name it so 9.17 can find it.
- m-11: OQ-36 (events read for an in-backoff `failed` entry, contradicts spec line 103) and OQ-41a (probe cache in the cycle, contradicts D 614) are departures from source text outside the 29; X1 to X5 are not individually enumerated in OQ-26. Promote OQ-36 and OQ-41a to "owner to confirm" or add them to the M4 exemption list explicitly (the 29-id list in 9.M1 to 9.M3 does not name them; the generic sentence about "other proposal values" covers them only by interpretation).
- m-12: Item 8.2 contains the only conditional skip in the suite while G-1/G-3 require zero skips. State "a skip at a gate run is a FAIL unless the log shows the deny-listed filesystem".
- m-13: AC-11 "foreign lock exits 6": the foreign-owner case is tested at record level (4.3), the cycle-level exit 6 only for symlink, directory and missing lock (8.5). Add the foreign-owner case (monkeypatched `os.geteuid`) to 8.5.

## 10. Counts

Items checked: 176. Decisions DF-01 to DF-60: 60 applied (58 fully, DF-19 and DF-41 partly). DEVIATION rows listed: 29 of 29. Design section 11 rows in the Section 2 table: 34 of 34 have a creating item in the right phase (the fixtures row: 11 of 13 files in the 06 phase, 2 one phase later). Design section 12 tests: 8 of 8. AC content coverage: 25 of 25; AC id traceability: 13 of 25 ids cited. Edge cases from the lens list: 19 of 19 present (reset audit exits with 2 untested branches). Blocking issues: 3 IMPORTANT, 0 CRITICAL. MINOR: 13.

VERDICT: FAIL

Reason: three blocking alignment defects (I-1, I-2, I-3), each fixable with the one-paragraph edits given above; no CRITICAL defect, no DF fully missing, and the phase order, the 29 deviations, the file list and the edge-case criteria are sound. After the three edits (items 3.1, 3.7, 6.1, 6.6, 9.17, plus the Phase 2 and Phase 8 header clause) the task should pass this lens.

