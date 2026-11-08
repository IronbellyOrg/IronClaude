# Cross-Validation Report, round 3 (final): gap-fill file 06 against files 01-05, design and spec

**Analysis type:** completeness-verification, lens: cross-validation (FINAL re-check, round 2 of the gap-fill; third and last review)
**Date:** 2026-11-07
**Scope:** `research/06-gap-fill-decisions.md` (314 lines now) against `research/01..05`, `research-notes.md`, `docs/designs/issue-watcher.md` (D), `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (S)
**Prior reports:** `qa/analyst-cross-validation-report.md` (X-1..X-15), `qa/analyst-cross-validation-report-r2.md` (I-1, I-2, R2-M1..M11)
**Status:** Complete. VERDICT: FAIL (0 CRITICAL, 4 IMPORTANT, 10 MINOR). r2 blockers I-1 and I-2: both RESOLVED.

---

Method: read file 06 in full (314 lines); re-read the r2 report; re-read the design (D) and spec (S) ranges that the new rows DF-41 to DF-59 cite; read research 05 lines 244-258, 340-361, 431-451 and `research-notes.md` 20-54; read the task-builder template (`~/.claude/templates/workflow/02_mdtm_template_complex_task.md`) and `SKILL.md` lines that DF-08 cites; ran read-only checks against the repo. No research file was modified. No web research.

## 1. Internal consistency of file 06 (DF against DF, tables, phases)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Reason arithmetic: 52 spec names + new reasons = 57 | CONSISTENT | I counted S 332-358 row by row: 6+1+5+5+2+2+1+3+3+2+1+2+2+2+1+1+1+2+1+1+1+2+2+1+2 = 52. New names: `marker_unreadable`, `edits_unreadable` (DF-02), `operator_reset` (DF-03), `dry_run_shadow_reset` (DF-22), `reset_refused` (DF-57) = 5, so 57. "57" appears in DF-02 (with the 2+1+1+1 breakdown), DF-22, DF-31, DF-41 (names the same five), P2. No place still says 52, 55 or 56. |
| 2 | DF-41 kind and exit for each new reason against the rows that create them | CONSISTENT | `marker_unreadable`/`edits_unreadable` skip 0 (DF-02); `operator_reset` skip/warning 0 (DF-03); `dry_run_shadow_reset` warning 0 (DF-22); `reset_refused` warning 2 (DF-04, DF-57). Exit-6 reasons and `lock_held` 75 match S 336 and S 340. Representation of the two-kind `operator_reset` is open: R3-M9. |
| 3 | DEVIATION count: DF-40 says 24 | COUNT CORRECT, MARKING INCOMPLETE | Rows marked yes in 1.1, 1.7 and 1.8: 01, 02, 03, 04, 05, 06, 07, 09, 10, 12, 13, 17, 18, 20, 22, 24, 25, 27, 28, 29, 43, 50, 55, 57 = 24, equal to DF-40's list and the R2-AC B-4 row of the change log. But rows DF-15, 42, 44, 48 and the X10 runbook location resolve a D-vs-D or S-vs-D conflict the same way as DF-24/DF-25 (marked yes) and are marked no or have no row: finding R3-N1. |
| 4 | Gate counts against the gate map | CONSISTENT ARITHMETIC | DF-08: 4 x 6 + 7 + 2 = 33. Table 1.6: A 6, B 6, C 6, D 6, Final 7, M4 2 = 33. Section 2: P3 Gate A, P5 B, P7 C, P8 D, P9 Final then M4; P1, P2, P4, P6, P10 none; "covered by Gate X" notes in P2, P4, P6 match the "Covers" column. The Final = 3 rf-qa + 3 rf-qa-qualitative + 1 domain (rf-qa) matches I22 line 807 ("7 = 3 structural + 3 content + 1 domain"). The agent-count rules against the template text are a different matter: R3-N2. |
| 5 | Stub list against the PATH design and the sleep/matched fields | CONSISTENT | DF-10, Table 1.4 "Stub files", "Guard" row and the e2e description all name `gh`, `orca`, `orca-ide`, `git`. PATH = `stubbin:linkbin`, no `/usr/bin`; the shebang uses the absolute `/usr/bin/env`. `sleep` (Scenario row), `matched` (Log header row and teardown rule) and `IW_STUB_STATE_DIR` (State snapshot row) are the same three things DF-55 (a), (b) cite. The orca probe row matches `install_user_setup.py:216-219` (`.get("topics", [])`, `any(t.get("name") == "orca-cli" ...)`, verified). |
| 6 | conftest phase assignment against module build order (DF-56) | ONE CONFLICT | `FakeRunner`/`FakeClock` at P2 (import nothing later), `tmp_state`/`CrashingStore` at P4 (needs `record`), `FakeLauncher` at P5, deps factory at P6, stub fixture at P8: build order is right. Conflict: P2 lists `test_runner.py` "incl. DF-55 sleeping-stub timeout", and DF-55 (a)+(c) define that stub as the Table 1.4 scenario stub whose fixture only arrives at P8: R3-N3. |
| 7 | Commit item (DF-07, P10) against staged paths | CONSISTENT | Six prefixes in the `git add` (`src/superclaude/cli/issue_watch`, `src/superclaude/cli/main.py`, `tests/issue_watch`, the design, the runbook, `.dev/tasks`) equal the six in the allowlist sentence. `git diff --cached --name-only` today: 83 paths, 0 outside `.dev/tasks/` (verified), matching "83 files already staged". `docs/designs/issue-watcher.md`, `.dev/brainstorms/...` and `.dev/issues/331/` are untracked (verified); only the first enters the commit. HEAD = merge-base = `e8db2fe6...`, origin/master = `0b8a5801...` (verified). Trailer text equals the attribution reminder. The branch is `ironbelly/issue-331-github-issue-watcher` (not master); the item never checks that: R3-M7. |
| 8 | DF-01 (`cwd`) against DF-10 stub log and DF-24/DF-48 | CONSISTENT | `Runner.run(..., *, cwd=None)`; `FakeRunner` records `(tuple(argv), cwd)`; the stub log header records `os.getcwd()`; only `OrcaLauncher.launch` passes cwd; `check_origin` passes none because of `git -C` (D 317/329/843). |
| 9 | DF-57 against DF-03, DF-04, D 399, D 718-722 | CONSISTENT, one wording gap | Order lock, load, entry check; success per DF-03; exit 2/6/75 lines per D 399; `stderr_fallback` uses match D 722 ("exit 2 before state_dir is known, exit 6 state_dir_unwritable"); exit-75 append without rotation matches D 720. The sentence "The AC-17 test asserts audit.jsonl for each exit" cannot hold for the three stderr-only exit classes: R3-M8. |
| 10 | DF-05 (no local full suite) against G-2 and CI | CONSISTENT | `test.yml:47` is `pytest ... -n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py`; comment `:44-45`; serial step `:137` (all verified). |
| 11 | DF-29 against D 760, DF-06 and P7 | CONSISTENT | `main.py:547` (swarm) and `:559-561` (reflect) use the eager `# noqa: E402,I001  # intentional: ...` pattern (verified); `:564-565` is the `__main__` guard. |
| 12 | Phase checkpoints against gate commands | MINOR GAPS | G-1 exit 5 at P1 stated in G-1, P1, DF-56 (consistent). G-5 "at P3-P8" (DF-09) vs P2 using it and P8 omitting it; G-10 "P9" in Table 1.2 vs "P9 and P10" in DF-59; G-11 vs 0-byte `__init__.py`: R3-M1, R3-M2, R3-N4. |
| 13 | Test file list against D 761-763 | CONSISTENT | All 8 per-module tests and all 11 cross-cutting tests of D 762-763 appear in P2-P8 (19 files). |
| 14 | DF-43 against D 476-490 | CONSISTENT | D 478 T-1 (none) to `failed`, D 480 T-3 `attempts` reaches 3 inside `record.fail`; no T-row for `failed` to `failed`; DF-43 adds it and marks the deviation. |
| 15 | DF-15 / Table 1.3 against D 507-533 | CONSISTENT | C1-C5 durable states match D 527-531; `os.replace` in `write_prepared_bytes` at `atomic.py:32`, `except Exception` at `:33` (verified), so a `SystemExit` leaves the orphan tmp file as D 528 says. |

## 2. The two r2 blockers

### I-1 (register completeness): RESOLVED

Every item r2 listed now has a DF row, and each row's decision matches the research 05 text it adopts.

| Source item (r2 section 2.2) | DF row | Matches 05/02 text |
|---|---|---|
| 05 G-06 reason mapping | DF-41 | 05 line 436 (companion mapping; `re-approved` in `REASONS`, note only) |
| 05 G-07 `last_reason` vs import rule | DF-42 | 05 line 437 and X15 (type-only check, membership in tests) |
| 05 G-09 `failed` to `failed` | DF-43 | 05 line 439; D 478-480 read |
| 05 G-10 `sweep`/`day_cap_count` | DF-44 (and DF-25 for `slo_numbers`) | 05 line 440 and X12 |
| 05 G-11 `Deps`, `CycleResult` | DF-45 | 05 line 441; D 302 |
| 05 G-12 marker-contract path | DF-46 | 05 line 442; both `src/superclaude/skills/sc-issue-protocol/` files exist, marker at `templates/claim-comment.md:23` and `refs/claim.md:29` |
| 05 G-13 account rename | DF-47 | 05 line 443; S 213 |
| 05 G-14 `FakeRunner` value type | DF-48 | 05 line 444 |
| 05 G-15 fixture names | DF-49 | 05 lines 246-258 exist |
| 05 G-16 / 02 G9, X1-X5 | DF-50 | 05 lines 347-351 (X1-X5, S 161, 163-164, 196, 267); D 866 Q1-Q4 |
| 05 G-17 `Retry-After: 120` on G1 | DF-51 | 05 line 447, X3 |
| 05 G-18 mountinfo reader | DF-52 (parser DF-23) | 05 line 448 |
| 05 G-21 `init-state` network-FS | DF-53 | 05 line 451 |
| 02 G7 `which` keyword | DF-54 | D 222 `find_orca(runner, which)`, D 299 |

I also checked the remaining 05 ids: G-01 to G-05, G-08, G-19, G-20 and X6 to X15 map to DF-01, 10, 03, 33, 28, 04, 11, 54, 01, 15, 29, 44, 42 as listed in the "Source" column; the only 05 item with no DF row is X10 (runbook location), which feeds R3-N1. The 06 header ban on citing G-ids no longer strands any decision. One residue: DF-41 to DF-54 say "adopt research/05 as written", so a builder must still open 05 for the details of DF-45, 49 and 50; that is acceptable because the header says 06 supersedes 05 only where they conflict.

### I-2 (rename-event / null-label handling): RESOLVED

- DF-18 now reads per event kind: every item needs non-null `id`, `event`, `created_at`; only `labeled` and `unlabeled` additionally need `label`, `actor_id`, `actor_login`, `actor_type`; "`renamed` and every other kind need only `id`, `event`, `created_at`". It names the test case (a `renamed` event with `label: null` and null actor fields parses and does not make the history unreadable) and P3 lists it. The deviation from D 572 is marked yes and listed in DF-40.
- Against the design's events projection: `EVENTS_JQ` (D 545) projects `label: .label.name`, so a `renamed` item always has `label` null or absent in the projection. The only predicate that reads rename events is T4 `predicates.unchanged_since(approval, edits, events)` (D 660; S 94 "no `renamed` event follows it"), which needs the event name and `created_at`, plus `id` for the (`created_at`, `id`) order of S 92. All three are required for every kind by DF-18. The design never asks for rename actor or label data. So the new rule is consistent with the projection and with the one consumer.
- Residual, non-blocking: DF-18 still requires `label` and the three actor fields for every `labeled`/`unlabeled` event, including events about unrelated labels and, for the actor fields, `unlabeled` events that the predicates do not read for actor data (S 89 (e) needs only label and time). That is stricter than DF-18's own principle ("fail closed only on fields a predicate reads") but fails in the safe direction: R3-M5.

## 3. Repo and source spot-checks of facts file 06 asserts (target 12; 32 done)

Tags: VERIFIED = matches; CONTRADICTED = differs; QUALIFIED = true in part. All checks read-only.

| # | Claim in 06 | Checked at | Result |
|---|---|---|---|
| 1 | D is 935 lines, S is 515; D and the brainstorm folder untracked (header, DF-07, DF-31) | `wc -l`, `git status --short` | VERIFIED (935, 515; `??` for `docs/designs/issue-watcher.md`, `.dev/brainstorms/20261107-064825-github-issue-watcher/`, `.dev/issues/331/`) |
| 2 | HEAD = merge-base = `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b`; origin/master = `0b8a5801d75f159bcbca7087b99507c2a50d8dba` (DF-07) | `git rev-parse`, `git merge-base` | VERIFIED, all three byte-equal |
| 3 | 83 files already staged, all under `.dev/tasks/` (DF-07) | `git diff --cached --name-only` (count 83; 0 outside `.dev/tasks/`) | VERIFIED |
| 4 | `test.yml:47` `-n auto ... --ignore=tests/cli/test_verify_sync_hooks.py`; comment `:44-45`; serial step `:137` (DF-05) | Read | VERIFIED |
| 5 | Hook lines: trailing-whitespace `:9` excluding `.md`, end-of-file-fixer `:11`, check-json `:15`, check-added-large-files `:17`, check-merge-conflict `:19`, mixed-line-ending `:21`, detect-secrets `:26-41`, detect-private-key `:47`, secret regex `:54-63`, markdownlint `:74-88`, shellcheck `:98-103` (DF-32, DF-58) | Read of `.pre-commit-config.yaml` | VERIFIED |
| 6 | "CI applies the hygiene hooks ... CI would fail the PR otherwise" (DF-58 Issue and Rationale) | `grep -rn 'pre-commit\|markdownlint' .github`, `Makefile` | CONTRADICTED / UNSUPPORTED: no workflow or make target runs pre-commit; the hooks run only from a developer's installed git hook (an external service is not visible here). The file-hygiene rules are still sensible; only the stated reason is unsupported: R3-M3 |
| 7 | `uvx --offline ruff@0.15.20 --version` = 0.15.20; `ruff==0.15.20` in `pyproject.toml` (`:50-54` comment and pin); ruff-pre-commit `v0.15.20` (`.pre-commit-config.yaml:110`); local Python 3.11.15 (DF-09, G-5) | ran, Read | VERIFIED |
| 8 | xdist resolves offline (G-3 note: 3.8.0) | `uv run --offline --no-sync --with "pytest-xdist>=3.5,<4" python -c "import xdist"` | VERIFIED (3.8.0) |
| 9 | Makefile `test:13-15`, `lint:48-50` (`lint: lint-architecture`, then `uv run ruff check .`), `sync-dev:109`, `verify-sync:166`, `verify-deps:356-358` (Section 3) | `sed -n` | VERIFIED |
| 10 | `main.py:547` swarm import, `:559-561` reflect import and `add_command`, `:564-565` `__main__` guard (DF-29, DF-34) | Read | VERIFIED |
| 11 | `swarm/atomic.py:14` `write_prepared_bytes`; `:32` `os.replace(tmp_name, str(path))`; `:33` `except Exception` unlinks the tmp file; no directory fsync (DF-15, DF-30, Table 1.3) | Read | VERIFIED (so C2's `dst.endswith("dispatch.json")` closure patch and the `dispatch.json.*.tmp` orphan are right) |
| 12 | `install_user_setup.py:35` `_ORCA_CLIS = ("orca-ide", "orca")`; `:216-219` `.get("topics", [])` and `any(t.get("name") == "orca-cli" ...)` (DF-10, DF-36, Table 1.4 Orca probe) | Grep | VERIFIED |
| 13 | `tests/pr_submit/__init__.py` and `tests/cli_portify/__init__.py` exist (DF-27); the six G-2 test files exist | `ls`, `wc -c` | VERIFIED. Note: `tests/pr_submit/__init__.py` is 0 bytes (R3-N4) |
| 14 | `FULL_ID` at `test_model_alias_policy.py:50`, test at `:137` (DF-11) | Grep | VERIFIED |
| 15 | `pyproject.toml:110` `python_classes = ["Test*"]`, `:135` property_based marker text (DF-12) | `sed -n` | VERIFIED |
| 16 | S 332-358 holds 52 names; exit-6 reasons are kind `cycle` at S 336; `lock_held` 75 at S 340; warning reasons only `discovery_count`, `clock_skew` at S 358 (DF-02, 22, 41, 57) | Read, hand count | VERIFIED |
| 17 | D 399 "every exit of `once` and `reset`"; D 718 `REASONS` frozenset and `ValueError`; D 720 exit-75 no rotation; D 722 stderr fallback uses; D 711 `issue` optional on warning lines (DF-03, 04, 57) | Read | VERIFIED |
| 18 | D 118-121 reset rows and usage rule; D 221 `sweep(store, now)`, `day_cap_count(store, now)`; D 437 `last_reason` "reason from the closed enum"; D 439 validation "types as above" (DF-03, 06, 42, 44) | Read | VERIFIED as quoted; they feed R3-N1 |
| 19 | D 137 "Absolute after expansion"; D 131-132 label rules; D 69 deny list nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p; D 344 mountinfo check; D 351 warning at >= 80; D 449 `dry-run.json` warning (DF-13, 20, 22, 23) | Read, Grep | VERIFIED |
| 20 | D 545-548 projections equal the Table 1.5 GraphQL drafts and `EVENTS_JQ`/`MARKER_JQ` (DF-14, 18, 21) | Read | VERIFIED (field names and `first:100`, `pageInfo` match; repository literal at D 555) |
| 21 | D 476-490 T-1..T-13; D 525-531 C1-C5; D 776-780 seam table; D 785 `multiprocessing`; D 892 AC-19; D 866 Q1-Q4; D 761-766 file list (DF-15, 24, 43, 50, 55) | Read | VERIFIED |
| 22 | D 295-302 `FakeRunner` value `CommandResult \| Callable`, `RecordingLauncher`, `FakeClock(start, step)`, `Deps` fields (DF-24, 45, 48) | Read | VERIFIED; D 776 says `Reply`, so D 295 vs D 776 is a D-vs-D conflict (R3-N1) |
| 23 | Template I15 `:636`, I22 `:797` (standard row `:807`: intermediate 3, final 7, M4 2), M2 `:1056`, `:1100` (every step an explicit item), `:1110` (M4 Step 2) (DF-08) | Read | VERIFIED as locations; content of `:1110` and the F2 line: next two rows |
| 24 | "M4 is split by document ... because together they exceed the 1,000-line partition threshold (template line 1110)" (DF-08) | Read `:788`, `:1110`, `:1117` | QUALIFIED / CONTRADICTED: the rule at `:788` and `:1110` is "minimum 2; if source docs exceed 1000 lines total, partition across 3-4 agents"; D + S = 1,450 lines, so the cited rule calls for 3-4, not 2. `:1117` Step 3 adds one cross-source contradiction agent when several source documents exist. Neither is in the 33: R3-N2 |
| 25 | "F2 (line 428) is noted" (DF-08) | Read `:422-429` | QUALIFIED: `:428` says phase-gate QA "after completing all items in Phase 2+; proceeding to the next phase without a passing QA gate is prohibited". The map has no gate after P2, P4 or P6 and does not list F2 in Open Questions: R3-N2 |
| 26 | task-builder `SKILL.md` `:1149-1152` (M4 minimum 2), `:1186-1187` (intermediate under 5 rejected), `:2140` (any gate under 6 FAIL), `:2223` (`--diff {BASE}..HEAD`), `:2363` (standard final 7, intermediate 5) (DF-07, DF-08) | Read | VERIFIED |
| 27 | `research-notes.md:26` edited (DF-07); `:49` `qa_intensity standard` (DF-08) | Read | VERIFIED. Lines 20 (stubs), 24 (collision premise) and 53 (`AMBIGUITIES_FOR_USER: None`) still carry superseded text: R3-M6 |
| 28 | 05 lines 347-351 (X1-X5) and 431-451 (G-06..G-21 defaults); fixture names at 246-258 (DF-49, DF-50) | Read, Grep | VERIFIED |
| 29 | `refs/claim.md:29` and `:88`; `templates/claim-comment.md:23` (DF-16, DF-21, DF-46) | Read, Grep | VERIFIED |
| 30 | `adversarial/base-selection.md` and top-level `spec-panel-review.md` exist (DF-26) | Glob | VERIFIED |
| 31 | The design file committed unchanged is clean for the hygiene hooks (DF-07, DF-58) | `tail -c2`, `grep -c` CR and trailing space | VERIFIED (ends in one `\n`, 0 CR, 0 trailing-space lines) |
| 32 | Both `__init__.py` files "empty" (P1) pass G-11 (`tail -c1 \| od -An -c` prints `\n`) | `tail -c1 tests/pr_submit/__init__.py \| od` (prints nothing; file is 0 bytes) | CONTRADICTED for a 0-byte file: R3-N4 |

Result: 28 verified, 2 qualified (rows 24, 25), 2 contradicted (rows 6, 32); none changes a research fact, all four feed findings below.

## 4. New blocking findings in detail

Each is small and mechanical to fix. They are blocking because each makes a literal reading of 06 fail or mislead a downstream gate, and because round 2 treated the same class (DEVIATION labels, unpassable gates, phase-order conflicts) as blocking (R2-AC B-1, B-4).

### R3-N1 (IMPORTANT). The DEVIATION list is incomplete and inconsistent with its own definition

The header defines DEVIATION = yes as departing from literal D or S text "even when the departure fixes a design-internal error". DF-24 (D 297-298 names) and DF-25 (D 224 vs D 745) follow that and are marked yes. Five other resolutions of the same kind are marked no or have no row:

| Row | What it departs from | Mark in 06 |
|---|---|---|
| DF-44 | D 221 `sweep(store, now)`, `day_cap_count(store, now)` (D 737 says `doc`); 05 X12 | "no (DF-25 records the D 224 text deviation)", but DF-25 covers only `slo_numbers` at D 224, not D 221 |
| DF-48 | D 776 `FakeRunner(script: dict[tuple[str, ...], Reply])` (D 295 says `CommandResult \| Callable`); 05 G-14 | no |
| DF-42 | D 437 "`last_reason`: reason from the closed enum", checked by D 439 "types as above"; `record.validate` is reduced to str-or-null; 05 X15 | no |
| DF-15 | D 296 "`CrashingStore` raises at the k-th write" (D 779 uses `crash_at="C1".."C5"`); D 784 "rerun" against 5 reruns | "no for the seam" |
| X10 (no row) | S 384 puts the operator runbook inside the design doc; D 766 and P9 create `docs/designs/issue-watcher-setup.md`; DF-31 forbids editing the design | none |

Effect: DF-40 promises that the M4 prompts carry the full deviation list "so that a listed departure is not reported as drift". The two M4 agents compare the package with D (935 lines) and S (515 lines); an unlisted departure (the runbook file, `sweep(doc, now)`, the `FakeRunner` value type, the `last_reason` check) is reportable as drift and would cost a fix cycle. The Open Questions section would also omit them.

Fix (edit to 06): mark DF-44 (D 221), DF-48 (D 776) and DF-42 (D 437, 439) as yes; mark DF-15 yes for D 296 and D 784; add a row (for example DF-60) for X10: "runbook written to `docs/designs/issue-watcher-setup.md` as D 766 says, not inside the design doc as S 384 says; DEVIATION yes (S 384)". Update the count in DF-40 and in the R2-AC B-4 change-log row (24 becomes 24 plus the rows added; with all five that is 29). Alternatively state a single rule ("a D-vs-D conflict resolved by choosing one D line is not a deviation") and then change DF-24 and DF-25 to match.

### R3-N2 (IMPORTANT). The QA gate map misstates the template rules it cites and omits required M4 and F2 elements

Evidence (template `02_mdtm_template_complex_task.md`):
- `:788` and `:1110`: "Minimum 2 fidelity agents. If source docs exceed 1000 lines total, partition across 3-4 agents". The M4 sources are D (935) and S (515): 1,450 lines. DF-08 says M4 is "split by document, one agent on D and one on S, because together they exceed the 1,000-line partition threshold (template line 1110)". The cited rule gives 3-4 agents, so the stated reason points away from the chosen count of 2. (SKILL.md `:1151` and I22 `:807` do allow 2 at `standard`, which DF-08 also cites; the two sources conflict and 06 resolves it silently.)
- `:1117` (M4 Step 3): "If multiple source documents exist, spawn ONE additional rf-qa agent that reads ALL source documents and checks for contradictions". D and S are two source documents (and 05 X1-X5 show they do contradict). The gate map and the 33 have no such agent.
- `:428` (F2): phase-gate QA is required "after completing all items in Phase 2+; proceeding to the next phase without a passing QA gate is prohibited". DF-08 writes "F2 (line 428) is noted" and runs gates only after P3, P5, P7, P8, so P2, P4 and P6 proceed without a gate. DF-40's Open Questions list names only the SKILL.md 2140 vs I19 tension, not F2 or the M4 rules.

Fix (edit to 06): in DF-08 either (a) make M4 three agents partitioned as D lines 1-468, D 469-935 and S, plus the Step 3 contradiction agent (total 33 becomes 35), or (b) keep 2 and replace the "because ... 1,000-line threshold" clause by an explicit statement that this departs from template `:788`/`:1110`/`:1117`; and in either case add the F2 and M4 tensions to the DF-40 Open Questions list with the reason (task-builder `SKILL.md` `:1151` and I22 allow the smaller map).

### R3-N3 (IMPORTANT). P2 asks for a test whose fixture arrives at P8

DF-55 (a) and (c) define the AC-19 timeout test as "`SubprocessRunner` runs a sleeping stub with `timeout=0.5`" where "Table 1.4 stubs accept an optional `sleep`". DF-56 puts the stub-on-PATH fixture and scenario helper in P8 and forbids a module-level import of a later phase's module. P2 lists `test_runner.py (incl. DF-55 sleeping-stub timeout)` and requires G-1 to pass at P2. Read literally, the P2 test depends on a P8 fixture.

Fix: add one clause to DF-55 (c) and to the P2 row: "`test_runner.py` writes its own one-line sleeping script into `tmp_path` and does not use the P8 stub fixture", or move that case to P8.

### R3-N4 (IMPORTANT). G-11 cannot pass for the two empty `__init__.py` files

P1 creates `src/superclaude/cli/issue_watch/__init__.py` "empty" (D 751 "exports nothing") and `tests/issue_watch/__init__.py`; the repo convention is 0 bytes (`tests/pr_submit/__init__.py` is 0 bytes, verified). G-11 requires, "for each new file", that `tail -c1 <file> | od -An -c` prints `\n`; for a 0-byte file it prints nothing, so the row fails. Table 1.2 says "no row allows SKIP" and P9 requires every row to pass.

Fix: G-11 pass text: "every non-empty new file ends with exactly one newline; a 0-byte file is allowed". (The `end-of-file-fixer` hook accepts empty files.)

## 5. Gap list

### CRITICAL
None.

### IMPORTANT (blocking)

| ID | Gap | Where | Fix |
|---|---|---|---|
| R3-N1 | DEVIATION marks inconsistent with the header definition: DF-44 (D 221), DF-48 (D 776), DF-42 (D 437/439), DF-15 (D 296, D 784) marked no; X10 (S 384 runbook location) has no row; the count in DF-40 and the change log (24) is therefore short by up to 5 | 06 DF-15, 42, 44, 48; DF-40; change log R2-AC B-4; 05 X10 | Flip the four marks, add an X10 row, recount (section 4) |
| R3-N2 | QA gate map: DF-08 cites template `:1110` as the reason for a 2-agent M4 while that rule (`:788`, `:1110`) requires 3-4 agents above 1,000 source lines (D + S = 1,450); M4 Step 3 cross-source agent (`:1117`) missing from the 33; F2 `:428` "noted" but not resolved or listed in Open Questions | 06 DF-08, Table 1.6, DF-40 | Choose 3 + 1 agents (total 35) or state the departure and list it in Open Questions (section 4) |
| R3-N3 | P2 `test_runner.py` sleeping-stub case depends on the stub fixture that DF-56 assigns to P8 | 06 DF-55 (a), (c); DF-56; P2 row | Say test_runner builds its own sleeper, or move the case to P8 |
| R3-N4 | G-11 requires a trailing `\n` on every new file; the two 0-byte `__init__.py` files from P1 cannot satisfy it and no row allows SKIP | 06 Table 1.2 G-11; P1 | Exempt 0-byte files in G-11 |

### MINOR (non-blocking)

| ID | Gap | Where |
|---|---|---|
| R3-M1 | DF-09 says G-5 runs on changed files at "P3-P8", but P2 already runs it and the P8 command list (G-1, G-3, G-8) omits G-5 (P9 runs the full-tree check, so nothing escapes) | 06 DF-09, Section 2 P2, P8 |
| R3-M2 | G-10: Table 1.2 notes say "P9"; DF-59, P9 and P10 say P9 and P10. Also `git diff --exit-code pyproject.toml Makefile` does not see a staged change; add `--cached` | 06 Table 1.2 G-10, DF-59 |
| R3-M3 | DF-58 rationale "CI would fail the PR otherwise" and DF-32 "CI or the commit hook runs them" are not supported: nothing under `.github/` or the Makefile runs pre-commit. Keep the rules, soften the reason | 06 DF-58, DF-32 |
| R3-M4 | DF-58 says "every new or changed file", but G-11 scans only `.py` and `.json` under the two new directories; the runbook `.md`, `main.py` and `docs/designs/issue-watcher.md` are outside it (end-of-file-fixer and mixed-line-ending also apply to `.md`). The design file itself is clean (verified) | 06 DF-58, G-11 |
| R3-M5 | DF-18 requires `label` and the three actor fields on every `labeled`/`unlabeled` event, including unrelated labels and `unlabeled` actors that no predicate reads; stricter than its own principle, safe direction | 06 DF-18 |
| R3-M6 | `research-notes.md` lines 20 (`stubs/gh`, `stubs/orca`), 24 (collision premise) and 53 (`AMBIGUITIES_FOR_USER: None`) still carry superseded text while line 26 was edited; the header supersession covers it, but an edit like line 26 would remove the trap | `research-notes.md` |
| R3-M7 | P10 never checks that the current branch is not master or main before the commit (project rule 4); it is a feature branch today | 06 DF-07 |
| R3-M8 | DF-57: "the AC-17 test asserts `audit.jsonl` for each exit" is impossible for the stderr-only exits (usage error before `state_dir`, config invalid, `state_dir_unwritable`); say "for each exit that has a `state_dir`" and name the D 399 shortfall in the DEVIATION cell | 06 DF-57 |
| R3-M9 | DF-41 stores `(kind, exit)` as `tuple[str, int]`, but `operator_reset` has two kinds (skip and warning); fix the string used (for example the first kind, with the second line use recorded in a comment or a second field) | 06 DF-03, DF-41 |
| R3-M10 | DF-34's e2e subprocess uses `sys.executable -m superclaude.cli.main`; the UV-only rule bans `python -m` as an operator command, not test internals. Say so in the item so an executor does not "correct" it | 06 DF-34 |

## 6. What holds up

- I-1 and I-2 from round 2 are both resolved; no r2 blocker is open.
- The reason arithmetic (52 + 5 = 57), the stub list against the PATH design, the DEVIATION count of 24 against the marked rows, the 33-agent sum against the gate map, the commit allowlist against the staged paths, and the crash-injection recipes against D 525-531 all agree with each other and with the repo.
- 28 of 32 spot-checked facts match exactly; the four exceptions are the ones listed above.
- Every DF-41 to DF-59 row cites lines that exist and say what the row says (D 399, 437-439, 476-490, 718-722, 776-780, S 336, 340, 358, test.yml, pre-commit lines).

## 7. Limits of this check

- I read 06 and the cited D, S, template, SKILL.md and 05 ranges directly; for 01-04 I relied on the r2 reading plus targeted greps, and did not re-read their 240 KB.
- I did not run `pytest`, `make` targets, `uv run ruff`, `gh` or `orca`. The xdist and ruff facts rest on the `--version` and import checks listed in section 3.
- GitHub API shapes (rename events, stderr text, GraphQL variables) stay UNVERIFIED, as 06 itself marks them. The I-2 verdict rests on the design's projection and its single consumer (D 545, 660; S 94), not on a live reply.
- R3-N2 turns on the template text; the skill (`SKILL.md` `:1151`) alone would accept a 2-agent M4, so the fix may be a recorded departure instead of a larger gate.

VERDICT: FAIL

Both r2 blockers (I-1, I-2) are RESOLVED. The gate fails on four NEW IMPORTANT findings (R3-N1 to R3-N4), all fixable with short edits to `research/06-gap-fill-decisions.md` (flip four marks and add one row, restate the M4/F2 sentence in DF-08, add one clause to DF-55 and one to G-11); no CRITICAL gap exists. After those edits only R3-N1 to R3-N4 need re-checking.

Report path: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/analyst-cross-validation-report-r3.md`
