# Completeness Re-check, Round 1 (gap-fill) - breadth lens

**Analysis type:** completeness-verification (gap-fill re-check, round 1)
**Date:** 2026-11-07
**Scope:** `research/06-gap-fill-decisions.md` (new, read in full, 219 lines) against the four failing QA reports (`qa-research-depth-report.md` RD, `qa-research-gap-report.md` RG, `qa-research-evidence-report.md` RE, `analyst-cross-validation-report.md` XV) and the MINOR items of `analyst-completeness-report.md` (AC); also `research-notes.md`.
**Track goal:** MDTM task file implementing the GitHub issue watcher exactly as in `docs/designs/issue-watcher.md`.
**Status:** Complete (see verdict at the end)

Method: read file 06 completely; read the four failing reports, the earlier completeness report and `research-notes.md`; re-read the design (`docs/designs/issue-watcher.md` lines 60-175, 262-265, 336-364, 436-452, 498-575, 706-723, 740-919) and spec-final lines 328-384; read the task-builder `SKILL.md` (lines 1000-1050, 1140-1190) and MDTM template 02 (I15, I16, I19, I21, I22, M2, M3, M4, F2, I17); read research 02 section G and 05 sections 3, 5.1, 6, Gaps. Spot checks run: SHAs of DF-07 (origin/master `0b8a580...`, merge-base = HEAD = `e8db2fe6...`: match), the five test files in G-2 (all exist), the spec reason table (hand count: 52 names, so 52 + 2 + 1 + 1 = 56 holds), `docs/designs/issue-watcher.md` untracked (confirmed), xdist pin at `test.yml:29`. No research file was modified. No web research.

---

## Part 1. Structural checks requested

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File begins with the supersede sentence | PASS | Line 1 of `06-gap-fill-decisions.md`: "This file supersedes research files 01 to 05 wherever they conflict. Every item below is a DECISION the task file must follow; items marked DEVIATION differ from the design and must be recorded as Open Questions / deviations in the task." It is the first line, before the H1. |
| 2 | Every DEVIATION = yes row is listed for the task | PASS as to the "yes" column; FAIL as to completeness of the labelling | The "yes" rows are DF-01, 02, 03, 04, 05, 07, 10, 12, 17, 20, 22 (11 rows). DF-40 (line 161) lists exactly those 11. But other rows depart from literal design text and are labelled "no"; see gap B-4. |
| 3 | Phase plan covers every file in design section 11 | PASS | Section 11 has 17 rows (D 751-768). `__init__.py` P1; `runner.py`, `predicates.py`, `audit.py` P2; `github.py` P3; `record.py` P4; `launch.py` P5; `cycle.py` P6; `cli.py` and `main.py` P7; `tests/issue_watch/__init__.py` P1; `conftest.py` P2 (but see B-1); 8 per-module tests P2/P3/P4/P5/P6/P7; 11 cross-cutting tests (`origin_parity`, `marker_contract`, `find_orca_parity` P5; `slo_helper` P6; `cli_e2e`, `security_invariants`, `crash_injection`, `concurrency`, `no_shell`, `no_text`, `module_boundaries` P8); `fixtures/_assumed_shape/*.json` P3; `stubs/gh`, `stubs/orca` replaced by test-time stubs (DF-10, recorded DEVIATION); runbook P9. The "Not changed" list (D 768) has no gate row (gap M-h). |
| 4 | Phase plan covers every test in design section 12 | PASS with one defect | `test_crash_injection` P8 (Table 1.3), `test_concurrency` P8, `test_cycle::test_fifty_cycles` and `::test_acceptance_property` P6, `test_no_shell` P8, `test_no_text` P8, `test_module_boundaries` P8, `test_marker_contract` P5. Seams: `FakeRunner` P2, `FakeClock` P2, `FakeLauncher` P2 (wrong phase, B-1), `CrashingStore` (no phase assigned, B-1), PATH stubs P8 (Table 1.4; incomplete, B-2). Section 17 AC-1 to AC-25: P9 has an AC trace table and the Final gate has an AC-coverage lens; AC-19 cannot be met by Table 1.4 as written (B-2). |
| 5 | Gate map meets the skill's agent-count rules | PASS on counts; FAIL on order | Final gate 7 (standard intensity: 3 structural + 3 content + 1 domain, template I22 line 807/831; SKILL.md 1186-1187 floor is 6). Intermediate gates 6 each (floor 5, SKILL.md 1186-1187 and I15 line 638; SKILL.md 2140 CRITICAL below 6). M4 fidelity gate present with 2 agents (standard intensity, template line 832; M4 floor 2, SKILL.md 1151-1152). Arithmetic 4 x 6 + 2 + 7 = 33 is right for lens/review agents only. Order defect: B-5. |
| 6 | Nothing contradicts the design or spec except where marked DEVIATION | FAIL (labelling) | Seven or more rows depart from literal design text but say "no": B-4. |

---

## Part 2. Finding-by-finding resolution

"Sev" is the severity the earlier reporter gave. R = RESOLVED (file 06 holds a concrete decision, DF id cited). NR = NOT RESOLVED. PR = partly.

### 2.1 Cross-validation report (XV): 6 IMPORTANT, 9 MINOR

| Finding | Sev | DF id | Status | Note |
|---|---|---|---|---|
| X-1 six verbs vs five commands | IMP | DF-06 | R | Five Click commands, "six usage forms", `--help` asserts five names; G-9 checks exactly five. |
| X-2 `ORCA_AGENT` literal | IMP | DF-11 | R | `"claude"`, source `seed-brief.md:64`, pinned as a literal; "no model name" rule dropped (no source existed). |
| X-3 stubs do not isolate `orca-ide` / `git` | IMP | DF-10, Table 1.4 | R (but see B-2) | Stubs `gh`, `orca`, `orca-ide`, `git`; PATH = stubbin + linkbin only; `which(name, path=PATH)` guard per stub. |
| X-4 no consolidated register | IMP | DF-40 and rows below | PR | 02-only items resolved: G3 DF-02, G4 DF-16, G8 DF-17, G12 DF-18, G13 DF-19, G14 DF-20, G15 DF-21. 05-only items resolved: G-04 DF-03, G-05 DF-33, G-18 DF-23, G-19 DF-04. NOT carried: G-06, G-07, G-09, G-10, G-11, G-12, G-13, G-14, G-17, G-21, 02 G7, plus the Q1-Q4 citation (G-16). See B-3. |
| X-7 ruff skew | IMP | DF-09 (G-5, G-4) | R | `uvx --offline ruff@0.15.20`, explicit files; checked this session by the author. See M-g for a wording nit. |
| X-8 `make test` / `-n auto` | IMP | DF-05, DF-09 (G-1, G-2, G-3) | R | Affected subset locally, full suite CI only, xdist via `uv run --with`, SKIP allowed. Recorded DEVIATION. All five G-2 test files exist (verified). |
| X-5 gate size | MIN | DF-08 | R | |
| X-6 C14 false premise | MIN | DF-27 | R | Real reason stated (package convention). |
| X-9 stub materialisation / e2e invocation / lock test | MIN | DF-10, DF-34 | R | Runtime-written stubs, subprocess e2e, `multiprocessing` lock test. |
| X-10 `property_based` | MIN | DF-12 | R | Seeded loop, no marker; recorded DEVIATION. |
| X-11 "9 source files" prose | MIN | DF-38 | R | |
| X-12 `cwd` not propagated | MIN | DF-01 | R | Signature stated once with the files that use it. |
| X-13 `fromisoformat` grep | MIN | DF-35, G-7 | R | |
| X-14 `find_orca` parity scope | MIN | DF-36 | R | |
| X-15 gap-id collisions | MIN | header, "Ids in this file are DF-nn only" | R | |

### 2.2 Gap report (RG): 5 IMPORTANT, 5 MINOR

| Finding | Sev | DF id | Status | Note |
|---|---|---|---|---|
| I1(a) reason for failed marker / edit read | IMP | DF-02 | R (see M-a) | `marker_unreadable`, `edits_unreadable`; recorded DEVIATION. |
| I1(b) `reset` audit reason | IMP | DF-03 | R (see M-j) | `operator_reset`. |
| I1(c) `reset N` with no entry | IMP | DF-04 | R | Exit 2, no write, no audit. |
| I1(d) `make test` sizing | IMP | DF-05 | R | |
| I2 verb count | IMP | DF-06 | R | |
| I3 POST reflect `{BASE}` | IMP | DF-07 | R (see M-e) | BASE captured at P1, explicit-path commit at P10, literal `--diff <BASE SHA>..HEAD`. SHAs verified this session. |
| I4 `~` expansion in `--config` | IMP | DF-13 | R | `expanduser` on default and passed value; HOME-monkeypatch test. |
| I5 gate commands | IMP | DF-09, Table 1.2 | R | |
| M1 pre-commit-only hooks | MIN | DF-10, DF-32 | R | No committed shell files; fixtures parsed with `json.loads`. |
| M2 repo-wide scans (model alias, retired docs) | MIN | DF-11, P9 row, G-2 | R | |
| M3 `AuditLog` constructor/path | MIN | DF-33 | R | |
| M4 missing test cases | MIN | DF-22, DF-23 | R | Dry-run shadow, clock skew 61/60, discovery 79/80, mountinfo parsing. |
| M5 untracked design / brainstorm | MIN | DF-31 | R | |

### 2.3 Evidence report (RE): 2 IMPORTANT, 10 + 6 MINOR

| Finding | Sev | DF id | Status |
|---|---|---|---|
| B.1 stubs omit `orca-ide`, PATH exposes real binaries | IMP | DF-10, Table 1.4 | R |
| B.2 `ORCA_AGENT` contradiction and unsourced rule | IMP | DF-11 | R |
| M-1 to M-9 locator errors | MIN | DF-26 | R |
| M-10 "16 vs 15 TASK-RF files" | MIN | none | not carried; harmless (no task item cites it) |
| B.3.1 gate size | MIN | DF-08 | R |
| B.3.2 `property_based` | MIN | DF-12 | R |
| B.3.3 `make test` | MIN | DF-05 | R |
| B.3.4 `RecordingLauncher`/`FakeLauncher`, `slo_numbers` | MIN | DF-24, DF-25 | R |

### 2.4 Depth report (RD): 6 IMPORTANT, 6 MINOR

| Finding | Sev | DF id | Status | Note |
|---|---|---|---|---|
| 1 POST reflect empty diff | IMP | DF-07 | R | |
| 2 gate sizes under the skill floor | IMP | DF-08, Table 1.6 | R on counts | Order defect B-5. |
| 3 gate commands | IMP | DF-09, DF-05 | R | |
| 4 six verbs | IMP | DF-06 | R | |
| 5 crash-point recipes C1-C5 | IMP | DF-15, Table 1.3 | R (see M-b) | |
| 6 no merged register (G3, G4, G8, G12, G13, G14, G-01, id collision) | IMP | DF-02, 16, 17, 18, 19, 20, 01, header | R for the items RD named | The wider X-4 residue is B-3. |
| M1 no step-to-function table for `run_cycle` | MIN | Section 3 lookup (D 304-388) | R | |
| M2 GraphQL texts | MIN | DF-14, Table 1.5 | R | Drafts match D 547-548 field for field (checked). |
| M3 stub protocol / git decision | MIN | DF-10, Table 1.4 | PR | Incomplete, B-2. |
| M4 52 reasons | MIN | DF-02, DF-31 | R | 56-name literal pin; arithmetic checked. |
| M5 P7/P8 overloaded | MIN | Section 2 (10 phases) | R | No phase above 7 deliverables. |
| M6 `RecordingLauncher`/`FakeClock` names | MIN | DF-24 | R | |

### 2.5 Earlier completeness report (AC): MINOR items the builder must act on

| Item | DF id | Status |
|---|---|---|
| MIN-1 `AMBIGUITIES_FOR_USER: None` | DF-40, header of 1.1 | R (file 06 says it replaces that statement; the 11 DEVIATION rows go to Open Questions) |
| MIN-2 02 findings missing from 05 (G3, G4, G12, G13, G14, G15, gh exit 4) | DF-02, 16, 18, 19, 20, 21, 37 | R |
| MIN-3 contradictions K1-K6 | K1 DF-06; K2, K3 DF-12; K4 DF-11; K5 DF-10; K6 DF-05 | R |
| K7 reruns | DF-15 | R |
| K8 template-rule conflicts (a)-(e) | (a) DF-08; (b) DF-08 (2 agents); (c) to (e) left to 04 Part D, which 06 does not contradict | R by reference (see M-c for the M4 partition note) |
| MIN-4 tag vocabulary | none needed | n/a |
| MIN-5 unread precedents / unverified environment | DF-05, DF-09, DF-29, DF-32; G-3 UNTESTED | R as notes |
| MIN-6 `{BASE}` and BUILD_REQUEST values | DF-07 | R |

Totals: the four failing reports hold 19 blocking findings (XV 6, RG 5, RE 2, RD 6). All 19 have a DF decision. One (XV X-4) is only partly resolved (B-3). Two decisions have a defect that stops them being usable as written: the stub protocol behind XV X-3 (B-2) and the gate order behind RD 2 (B-5). Among the MINOR items, only RE M-10 is not carried (harmless).

---

## Part 3. New gaps in file 06 (blocking)

### B-1 (IMPORTANT). P2 puts `conftest.py` fixtures in a phase before the modules they import exist

- File 06 P2 (line 170) lists "`conftest.py` with `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` (DF-24)" and says G-1 must pass at the end of P2.
- Research 05 section 3 (lines 238-244) gives the dependency order that 06 does not carry: `FakeRunner` needs `runner.py` (P2, fine); `tmp_state` calls `record.init_state` and returns `FileStore` (needs `record.py`, P4); `FakeLauncher` needs `LaunchOutcome` from `launch.py` (P5); `CrashingStore` needs `record.py` (P4); the `deps(...)` factory needs `cycle.Deps` (P6).
- Effect: a P2 `conftest.py` that imports `launch` or `record` at module level fails collection at the P2 checkpoint (ImportError). `CrashingStore` (DF-15, Table 1.3), the `deps` factory and the Table 1.4 stub fixtures appear in no phase deliverable list at all (P8 lists test files only).
- Fix: add to Section 2 a conftest split: `FakeClock`, `FakeRunner` in P2; `tmp_state`, `CrashingStore` in P4; `FakeLauncher` in P5; `deps` factory in P6; stub fixtures (Table 1.4) in P8.

### B-2 (IMPORTANT). Table 1.4 (PATH stub protocol) cannot support AC-19 or the FR-010 e2e case

- Table 1.4 "Scenario" row defines each rule as `{"argv_prefix", "exit", "stdout", "stderr"}`. There is no sleep field and no way for the `orca` stub to capture `dispatch.json` at launch time.
- Design AC-19 (D 892): "A sleeping stub ends with `gh_timeout`; no launch starts after 120 s". Research 05 line 208 (`test_cli_e2e`: "sleeping `gh` stub gives `gh_timeout` exit 3", "stub `orca` reads `dispatch.json` when invoked and sees `pending` with `launches` 1") and line 260 (scenario carries "sleep seconds"; stub `orca` copies `dispatch.json` into the log) both need it; 03 lines 115 and 189 say the same. The production gh timeout is 20 s and is a module constant (D 819, D 139), so the test must shrink it by `monkeypatch` (05 T-R, line 416); 06 does not say so.
- Because 06 declares its tables exact and 05 only yields "where they conflict", an item author following Table 1.4 literally writes a stub that cannot sleep; AC-19 and the FR-010 GWT lose their e2e coverage.
- Fix: add to Table 1.4 a `sleep_s` field per rule, an `orca` rule option `capture: dispatch.json` (copy the file into the log on a launch argv), and the sentence "the gh timeout is a module constant that the test shrinks with `monkeypatch`".

### B-3 (IMPORTANT). X-4 is only partly closed: 05-only decisions are not in the register, but 06 says it is the only decision source

- DF-40 (line 161): "This file is the only decision source; the task cites DF ids." Line 11 forbids citing 05's `G-01`..`G-21`. Yet these 05 items have no DF row (05 lines 436-451 and 358, 361 give each a default):
  - G-06: companion mapping for kind/exit per reason (a `frozenset` cannot carry it, D 718) and whether `re-approved` is in `REASONS`. (06 uses "reason-table kind" in DF-02/03 without saying where the mapping lives.)
  - G-07: closed `last_reason` enum vs `record` not importing `audit` (type-only validation in `record`, membership in tests).
  - G-09: `failed` to `failed` (attempts + 1) is not a T-row; changes the transition table tested in `test_record.py`.
  - G-10: `sweep(doc, now)`, `day_cap_count(doc, now)` take `StoreDoc` (DF-25 covers `slo_numbers` only).
  - G-11: `Deps` and `CycleResult` live in `cycle.py`.
  - G-12: `test_marker_contract.py` must read the `src/superclaude/skills/sc-issue-protocol/...` path because CI has neither `~/.claude` nor `.claude/`; DF-21 only says "via the dual surface (D 791)", which fails or skips in CI.
  - G-13: NFR-005 "account rename" test is missing from the design; 06's P6 test list does not add it.
  - G-14: `FakeRunner` script value type (`CommandResult | Callable`).
  - G-16: owner questions Q1 to Q4 (D 866) and the disclosed spec deviations (S1, C20, C22, `last_completed_cycle_at`, `status` exit 1) must be cited in the task's Open Questions.
  - G-17: the 120 s Retry-After case is only reachable on G1.
  - G-21: `init-state` shares network-FS validation.
  - 02 G7: `which` as keyword argument with default `shutil.which` for `find_orca`.
- Effect: item authors cannot cite 05's ids and have no DF id to cite, so each default is either dropped or restated without traceability. G-09, G-12 and G-13 change tests that exist in the acceptance criteria.
- Fix: add DF-41.. rows (or one row "carry-over defaults") restating each 05 default with its where-applied column.

### B-4 (IMPORTANT). DEVIATION labelling omits rows that depart from literal design text

The header (line 1) says DEVIATION rows "differ from the design". These rows differ from stated design text and say "no":

| Row | Design text departed from | Register label |
|---|---|---|
| DF-29 | D 244 "`cli.py` imports the package lazily from `main.py`" (06 registers eagerly and drops the sentence) | no (prose error) |
| DF-28 | D 102 (C21) "`--method GET` ... on every G2 to G7 argv" | no (typo) |
| DF-06 | D 177 and D 759 "six verbs" | no (wording) |
| DF-27 | D 95 (C14) collision premise | no (reason changed) |
| DF-24 | D 297-298 `RecordingLauncher`, `FakeClock(start, step)` | no (design-internal) |
| DF-25 | D 224 `slo_numbers(lines, store, now)` | no (design-internal) |
| DF-09 / G-5 | D 800 `uv run ruff format --check src/ tests/` (06 uses pinned `uvx` on an explicit file list) | no |
| DF-13 | D 137 "Absolute after expansion" (06 reads this as default-expansion only; a `~` in a JSON value fails) | no |

DF-40 (line 161) lists only the 11 "yes" rows for the Open Questions. The M4 design-fidelity agents will read D 244, 102, 177 and 759 and report them as drift unless their prompts carry this list; a fix agent could then revert correct decisions.
Fix: relabel these as "yes (design text corrected)" or add a second list in DF-40 named "design text corrected", and require both lists in the Open Questions and in the M4 prompts. DF-13 should also be recorded as an interpretation.

### B-5 (IMPORTANT). Gate order puts the M4 fidelity gate before the final M3 gate

- File 06 P9 (line 177): "**M4 fidelity** (2), then **Final** (7)"; Table 1.6 lists M4 before Final.
- Template 02 line 1103: M4 "runs AFTER M3 (lens-based QA)". SKILL.md 1149-1150: "After M3 completes, spawn fidelity agents". I21 (SKILL.md 1181-1183): the fidelity gate is "AFTER the M3 lens-based QA sequence". Template line 685: the post-completion lens QA "verifies the FINAL state of all outputs".
- Related: P10 (commit) comes after both gates, and DF-07 says "If a pre-commit hook fails, fix the files". Such a fix edits files after the Final gate, which is the late-phase fix case line 685 wants the final QA to catch.
- Fix: order Final (7) first, then M4 (2); state that any P10 hook fix is followed by G-1 and G-5 on the touched files, or encode the Final gate in Post-Completion Actions after P10.

---

## Part 4. MINOR gaps (not blocking; the builder can absorb them)

| Id | Gap | Where | Suggested action |
|---|---|---|---|
| M-a | `marker_unreadable` and `edits_unreadable` trigger lists omit two design conditions: a repeated `id` on a later REST page (D 571 "incomplete") and a repeated or empty GraphQL cursor with `hasNextPage` true (D 575) | DF-02, DF-19 | Add both to the trigger lists, plus the same for `events_incomplete` and `project_unreadable` handling. |
| M-b | C3 recipe says `CrashingStore` "raises when the launcher is next reached"; a Store wrapper never sees the launcher call | Table 1.3 row C3 | State the mechanism: a `before_spawn` hook on the store, or a `FakeLauncher` that raises `SystemExit` before recording. |
| M-c | "33 spawns" counts lens/review agents only (each gate also has one fix agent and at least 2 verification agents, template I15 items 4-5); agent types are not assigned to the lenses (I19 wants rf-qa and rf-qa-qualitative split, 3 + 3 + 1 domain for the Final); M4 source documents total about 1,450 lines (D 935 + S 515), above the 1,000-line partition threshold in M4 step 2 (template line 1110) | Table 1.6, DF-08 | Add a one-line note per point; say the M4 pair is split by document (design, spec). |
| M-d | P1 checkpoint "collects 0 tests without error" while G-1 says pass is "exit 0"; pytest exits 5 when nothing is collected | P1 row, Table 1.2 G-1 | Write "exit 5 (no tests collected) is the expected P1 result". |
| M-e | DF-07 says "owner-authorized for this task only" for a commit that BUILD_REQUEST excludes and project rules reserve for an explicit request; no citation of where the owner said so (no BUILD_REQUEST for this task dir was found) | DF-07 | Cite the source of the authorization in the Open Questions entry. |
| M-f | Design section 14 defaults (D 807-827) appear only in the runbook row of Section 3, not in the `cycle.py` / `cli.py` rows where constants are coded | Section 3 | Add D 807-827 to the `cycle.py`, `github.py` and `launch.py` rows. |
| M-g | G-5 rationale "explicit file list avoids the 12 pre-existing Markdown hits" applies to ruff 0.17.3; with the pinned 0.15.20, `src/ tests/` is clean (XV X-7, 03 section 6). CI runs `src/ tests/`. | Table 1.2 G-5 | Also run `uvx --offline ruff@0.15.20 format --check src/ tests/` once at P9 so the CI command is reproduced. |
| M-h | The "Not changed" list (D 768: `pyproject.toml`, `Makefile`, CI, `.claude/`) and AC-23 "no new dependency" have no gate row; 05's final gate 7 had `git diff --exit-code pyproject.toml Makefile` | Table 1.2 | Add a row G-10 with that command plus a check that nothing under `.claude/` is staged. |
| M-i | RE M-10 (15 vs 16 `TASK-RF-*` files) not corrected | DF-26 | Ignore; no item cites it. |
| M-j | `operator_reset` is "kind skip" in DF-03 but is also used on a `warning` line; the reason table has one kind per reason | DF-03 | State the kind for the warning use, or use a distinct name. |
| M-k | `make lint` (includes `lint-architecture`, the `ID_PATTERNS` literal rule) runs first at P9 | Section 2 | Run G-4 at each intermediate gate (P3, P5, P7) to catch a late arch-lint hit. |
| M-l | Gates sit after P3, P5, P7, P8, P9 only. P2, P4 and P6 outputs go to the next phase with only G-1 and G-5. Template F2 (line 428) says "proceeding to the next phase without a passing QA gate is prohibited" for Phase 2+, while I15 (line 636) and M2 (line 1056) only require a gate between the primary execution phase and dependent phases | DF-08 | Add one sentence to DF-08 giving the I15/M2 basis and saying each gate covers two phases, so the task-integrity validator can see the choice was deliberate. RD recommended this shape (RD issue 2), so it is not treated as blocking. |

---

## Part 5. What holds up

- All 19 blocking findings from the four failing reports have a concrete decision with a DF id; none was answered with "decide later".
- The 56-name arithmetic, the BASE SHAs, the GraphQL drafts (field for field against D 547-548), the Table 1.2 file names, the 11-row DEVIATION list and the gate counts (6/6/6/6, 2, 7) check out against the repo, the design, the spec and the skill text.
- The phase plan covers all 17 rows of design section 11 and all 8 section 12 tests; ordering of the source modules (runner, predicates, audit, github, record, launch, cycle, cli) respects the import rules of D 229-244.
- The decision register and the lookup table use DF ids only, which removes the G/C/T id collisions XV X-15 raised.

---

## Verdict

Gap list:

- CRITICAL: none.
- IMPORTANT (blocking): B-1 (conftest fixtures placed before the modules they import), B-2 (stub protocol cannot cover AC-19 or the FR-010 e2e case), B-3 (05-only decisions not carried into the "only decision source"), B-4 (design-text departures not labelled DEVIATION, so M4 will see drift), B-5 (M4 fidelity gate ordered before the final M3 gate).
- MINOR (not blocking): M-a to M-l above.

All five blocking items are text edits to file 06 (a conftest split in Section 2, three added fields in Table 1.4, a few added register rows, a relabel, and a swap of two gate names). No new code investigation is needed.

VERDICT: FAIL

Report path: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/analyst-completeness-report-r2.md`

