# QA Report - Fix Verification (task-integrity, A.10 cycle 1 verification)

**Topic:** Implement the GitHub issue watcher (`superclaude issue-watch`), task file TASK-RF-issue-watcher-20261107-150955
**Date:** 2026-11-08
**Phase:** fix-cycle (task-integrity, lens fix-verification)
**Fix cycle:** 1 (verification of the first fix pass; `fix_authorization: false`, no file other than this report was modified)
**Task file:** `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md` (1026 lines)
**Backup compared:** `/tmp/task-before-fixes.md` (925 lines), word-level diff written to `/tmp/rfqa-diff.txt` and `/tmp/rfqa-work/wd.py`

---

## Overall Verdict: PASS (with minor notes)

All 15 blocking findings (B-01 to B-15) are FIXED. No fix introduced a blocking defect and no previously passing check regressed. Five minor notes are recorded at the end; none triggers a fix pass.

## 1. Blocking findings, one by one

Each row was decided by reading the changed item text in the task file and, where the item makes a factual claim about code or the design, checking that claim against the source.

| id | Items | Decision | Evidence |
|---|---|---|---|
| B-01 | 5.1, 5.2, 5.5 | FIXED | 5.1 (line 363) defines `OPERATION_ID_PATHS` as holding the success path and the error path, and says that for every `unknown` outcome the id is looked up in the JSON object parsed from stdout, then from stderr; plain text never yields an id (`operation_id` None, no retry command). 5.2 (line 366) builds `orca_launch_unknown.json` with `stderr` holding JSON text and the id `op-test-0001` at the error path. 5.5 (line 375) asserts the fixture id read from stderr and the negative plain-text case (`op-test-0002`). OQ-47 exists in Open Questions section D and cites Steps 5.1, 5.2, 5.5. Design lines 627-636 and 687-689 confirm the design gives no text-scraping rule. |
| B-02 | 4.1a, 4.1c, 6.2 | FIXED | 4.1a (line 330) defines frozen `PendingContext` with exactly `approver_id, approval_event_id, approved_at, launch_cwd, launch_login, launch_account_id`; design lines 426-433 and T-4 (line 481) confirm those are the Entry fields written at the `pending` write. 4.1c (line 336) `mark_pending(doc, n, ctx, now)` copies the six fields and sets `consumed_at` and `pending_at` to `now`, `launches` 1 (matches T-4). 6.2 (line 460) builds `ctx` with the six fields and cites OQ-48; OQ-48 exists. |
| B-03 | 3.G12-G17, 5.G12-G17, 7.G12-G17, 8.G12-G17, 9.F13-F18, 9.M8-M13 | FIXED | All six decision items write `CYCLE2=run` plus `F_n=<n>` or `CYCLE2=not-needed` to `phase-outputs/plans/<gate>-cycle-decision.md`; five conditional items per gate follow with full prompts and `-cycle2` file names; the last item applies regression message, then `[HALT-MONOTONICITY] \|F\|=<n>`, then the 2-cycle hard cap ("never run a third fix cycle"). Verified by script for all six gates (section 4 below). No "perform Steps X again" text remains. |
| B-04 | 5.1, 5.6 | FIXED | `src/superclaude/cli/install_user_setup.py:216-217` read: `.get("topics", [])` sits inside the `try`, `AttributeError` is caught and the candidate skipped, so a top-level JSON list is skipped, not raised. Line 219 (outside the `try`) raises for `topics` null, int, str, dict and a non-dict element. 5.1 and 5.6 now state exactly this; 5.6 asserts equal results for the top-level list and only "rejects without raising" for the raising shapes. |
| B-05 | 2.2, 2.3, 3.1a-c, 4.1a-c, 5.1 | FIXED | Step ids `3.1a 3.1b 3.1c 4.1a 4.1b 4.1c` present, no duplicate ids. A token check (script `/tmp/rfqa-tok.sh`) confirmed that all 125 backticked tokens of old 3.1 and all 128 of old 4.1 reappear in the union of the three parts, so no part was dropped. Each part has its own evidence-absence comment and an import-check clause. TB-Add-5 single-item justification comments sit at lines 194 (2.2), 197 (2.3) and 363 (5.1). Largest split part is under 3,900 characters. Phase 3 and Phase 4 intros describe the split. |
| B-06 | 3.6, 3.1a | FIXED | 3.1a (line 230) and 3.6 (line 251) now say "no argv requests `title` or `body` as an output field", with the G4 `--jq` value (`MARKER_JQ`) as the only element allowed to contain `body`. Design line 556 states the same rule. The test text is satisfiable: no other argv, GraphQL constant or jq constant in design 8.1 contains `title` or `body`. |
| B-07 | 10.6, 10.7, deleted 10.8, Task Overview, Key Objective 6, Reflect Depth Derivation | FIXED | Step ids end at 10.7; no `Step 10.8` header exists. 10.7 (line 875) ends with the `git add .dev/tasks` staging action in both branches and never reverts Done. 10.6 is the penultimate `- [ ]`, 10.7 the last (Phase 10 has 7 items). Task Overview (line 72) says "POST reflect gate as the penultimate item followed only by the Done item, which also stages the task folder" and "209". The only remaining `Step 10.8` and `176` text is the historical sentence in Reflect Depth Derivation (line 1024), which is intended. |
| B-08 | 6.3 | FIXED | 6.3 (line 463) reaches the tuple as `launch._ORCA_CLIS`, marks `install_user_setup.py:35` as background only, and states that `cycle.py` never imports `install_user_setup` (design line 241 and the Step 8.8 boundary test). `launch_cwd` is named as the stored entry field. |
| B-09 | 9.5 | FIXED | `tests/skills/test_model_alias_policy.py`: `SRC` at line 23, `TIER_TEXT_DIRS` at line 48, all rglob/glob calls are under `SRC` (lines 75-86, 109, 140); no read of the runbook. `tests/docs/test_retired_docs_absent.py` walks `*.md` under repo roots (line 41) and checks link targets. 9.5 (line 693) states this correctly and points to the grep of Step 9.3 for the model-alias check. |
| B-10 | 5.8, 8.2, Phase 2 and Phase 8 headers | FIXED | 5.8 (line 384) is now one non-parametrized loop over the copies that exist, src copies required, no skip. 8.2 (line 587) replaces the conditional skip by a failing assertion with an explicit message. Phase 2 header (line 186) and Phase 8 header (line 579) forbid `pytest.skip`, `skipif`, `xfail`. A grep for `importorskip\|skipif\|pytest.skip\|xfail` finds only those prohibitions and gate-prompt mentions; no item still asks for a skip. The "zero skipped" statements of G-1/G-3 are now satisfiable. |
| B-11 | 9.17, 9.18, 9.19 | FIXED | 9.17 (line 729) and 9.18 (line 732) say that after any fix Steps 9.4 to 9.16 are re-run in order (9.3 first when the runbook changed) and the `p9-*` files overwritten. Steps 9.4 to 9.16 are exactly the gate steps G-1 to G-11 (verified by listing the headings and the `p9-g*` file each writes). 9.19 (line 735) copies only results that postdate the fixes. |
| B-12 | 2.2, 5.1, 6.2, 9.M1, 9.M2, 10.2, 10.3, 10.4, 10.7, OQ section D | FIXED | OQ refs verified present: 2.2 cites OQ-37 and OQ-38; 5.1 cites OQ-40 and OQ-47; 6.2 cites OQ-36, OQ-39 and OQ-48; 10.2, 10.3, 10.4 cite OQ-7 and OQ-35; 10.7 says when they block. 9.M1 and 9.M2 name OQ-36, OQ-41a, OQ-47 and OQ-48. Every OQ id cited in an item (OQ-7, 35, 36, 37, 38, 39, 40, 41, 41a, 47, 48) is defined in the Open Questions section (49 entries). Section D heading names the two departures. One edge-case ambiguity in 10.2/10.7 is recorded as minor note M-3. |
| B-13 | 3.1c, 3.7 | FIXED | 3.1c (line 236) gives `events_unreadable` / `marker_unreadable` for a page longer than 100 and `events_incomplete` only for the sixth page or a repeated id; research/06 DF-19 (line 146) confirms the unreadable rule. 3.7 (line 254) tests 99, 100, 101, repeated id and page cap with the matching reasons. |
| B-14 | 6.1, 6.2, 6.6 | FIXED | 6.1 (line 457) defines `exit_for(reason)` reading `audit.REASON_TABLE[reason][1]`; `REASON_TABLE` is defined in 2.3 (57 names, count re-derived by hand: 7 + 5 + 5 + 2 + 2 + 1 + 3 cycle names = 25, 17 skip, 9 entry, 1 note, 3 + 1 warning, 1 operator_reset = 57). 6.2 uses `exit_for(<reason>)` for every condition. 6.6 (line 472) adds `test_exit_and_kind_follow_reason_table`. |
| B-15 | Phase 2 and 8 headers, 9.17 | FIXED | Naming rule present in both headers with the example `test_ac3_outsider_relabel__fr005_fr006`; 9.17 reads the FR/NFR rows, adds the Ids column and a second table FR-001..FR-029 and NFR-001..NFR-014 with NFR-012 gate-only. Design lines 872-898 do have an Ids column (read). One off-by-one line range is recorded as minor note M-1. |

**Result: 15 of 15 FIXED. FIXED-BUT-INTRODUCED-DEFECT: none.**

## 2. Regression check against the backup

The diff against `/tmp/task-before-fixes.md` has 60 hunks. Every changed line was compared word by word (`/tmp/rfqa-work/wd.py`); all hunks map to a blocking finding, a listed minor fix (N-01, N-02, N-03, N-14 to N-19, N-24, N-26, N-36) or one of the "extra" edits (earlier gates read the `-cycle2` fix reports; Phase 8 and 9.M intros add a pre-check). Results:

| Regression probe | Result | Evidence |
|---|---|---|
| Stale `Step 3.1` / `Step 4.1` / `Step 10.8` references | none outside history | Script of all `Step(s) N.x` references minus all defined step ids returns only `10.8`, `3.1`, `4.1`, and all three occur only in the historical sentence of Reflect Depth Derivation (line 1024). |
| Old item count (176 / 175) | none stale | `176` appears only in line 1024 as "count at build time was 176; ... it is 209". `209` appears in line 72 and line 1024. |
| Renumbering slips | none | Step ids run 1.1-1.8, 2.1-2.11, 3.1a-c, 3.2-3.11, 3.G1-G17, 4.1a-c, 4.2-4.7, 5.1-5.11, 5.G1-G17, 6.1-6.11, 7.1-7.9, 7.G1-G17, 8.1-8.12, 8.G1-G17, 9.1-9.19, 9.F1-F18, 9.M1-M13, 10.1-10.7; no duplicate id; every `**Step` header is directly followed by its `- [ ]` item (209 of 209). |
| Split parts missing content | none | Token check for 3.1 (125 tokens) and 4.1 (128 tokens): zero missing in the union of parts. |
| Orphaned references to deleted steps | none | No reference to a deleted step id remains; Step 10.8 content lives at the end of 10.7. |
| Phase intro counts | match | Gate A/B/C/D intros say 17 items; counted 17 each. Final gate says 18; counted 18. M4 says 13; counted 13. Phase 3 and Phase 4 intros say three items each for `github.py` and `record.py`; there are three. Phase 6 intro says three items for `cycle.py`; 6.1-6.3 are three. |
| Cross-gate wording drift | none | After normalizing gate names, 5.G12/7.G12/8.G12 are byte-identical to 3.G12, and G13 and G16 are identical across gates 3, 5, 7, 8. G14, G15 and G17 differ only in file lists, the extra checks that mirror each gate's cycle-1 verifier, and the phase to release. Fix-agent file scopes in the cycle-2 fix items equal the cycle-1 scopes (checked for all six gates). |
| Previously passing structural facts | preserved | Frontmatter lines 1-64 identical (`diff` of the two files, lines 1-64). 8.2 citation of `main.py` guard is now positional and stays true. 6.6, 6.7 and 8.x gate prompts unchanged except where listed. |

No item that passed the b2 or structure checks now fails.

## 3. Integrity counts

| Metric | Expected | Found | Result |
|---|---|---|---|
| `- [ ]` items at column 0 | 209 | 209 (`grep -c '^- \[ \]'`); backup 176 | PASS |
| `**Step` headers | 209 | 209 | PASS |
| Inline `- [ ]` tokens | 209 (+1 for prose) | 210; the extra is the phrase "count the `- [ ]` items" in Step 10.1, present in the backup too (177 vs 176) | PASS (not a checkbox) |
| Nested or malformed checkboxes (`  - [ ]`, `- []`, `* [ ]`, `- [x]`) | 0 | 0 | PASS |
| `TBD`, `TODO`, `FIXME` | 0 | 0 | PASS |
| Trailing spaces, tabs, three blank lines in a row | 0 | 0 / 0 / 0 | PASS |
| Phase counts (1 to 10) | sum 209 | 8, 11, 13, Gate A 17, 9, 11, Gate B 17, 11, 9, Gate C 17, 12, Gate D 17, 19, Final 18, M4 13, 7 = 209 | PASS |
| Gate lens agents | A 6, B 6, C 6, D 6, Final 7, M4 3 = 34 | 6, 6, 6, 6, 7, 3 (count of "Spawn one `rf-qa` ..." items per gate range) = 34; Gate A to D are 3 `rf-qa` + 3 `rf-qa-qualitative` each, Final 3 + 3 + 1 domain lens, M4 3 `rf-qa` | PASS |
| POST reflect penultimate, Done last in Phase 10 | yes | 10.6 reflect, 10.7 Done are items 6 and 7 of 7; no `- [ ]` after 10.7 before `## Task Log` | PASS |
| Frontmatter lines 1-64 | unchanged | `diff` of lines 1-64: identical; line 32 `reflect_post_mode: skill`; no `start_commit` or `executor_model_class` key (grep over lines 1-64) | PASS |
| Items missing the closing "If unable to complete ... mark this item as complete" clause | same as backup | Only 1.1, 2.11 and 10.6 deviate (different wording or a multi-line item), identical to the backup | PASS (no regression) |

## 4. The 30 new cycle-2 conditional items

Gates covered: 3.G13-G17, 5.G13-G17, 7.G13-G17, 8.G13-G17, 9.F14-F18, 9.M9-M13. I read Gate A, Final and M4 in full and compared the other gates by script after normalizing gate names.

| Probe | Result | Evidence |
|---|---|---|
| Full prompt embedded in each spawning item | PASS | G14 (fix), G15 and G16 (verifiers) carry complete quoted prompts with absolute `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/<gate>/...-cycle2.md` paths; no "see above" or "as in cycle 1". |
| `-cycle2` file names | PASS | consolidation `qa-consolidated-findings-cycle2.md`, `qa-fix-report-cycle2.md`, `qa-verification-structural-report-cycle2.md`, `qa-verification-content-report-cycle2.md` (M4: `qa-fidelity-...-cycle2.md`); cycle-1 files are read by exact name and left untouched. |
| Guard order in the last item of each gate (3.G17, 5.G17, 7.G17, 8.G17, 9.F18, 9.M13) | PASS | (1) regression message `Regression detected on Item X.Y, previously PASS at cycle 1, now FAIL. Halt overrides monotonicity check.`, (2) `[HALT-MONOTONICITY] \|F\|=<n>` when `\|F_{n+1}\| >= \|F_n\|` with `F_n` read from the decision file, (3) hard cap: "never run a third fix cycle and never pass open blocking findings". Script count per gate: 1 regression message, 1 `HALT-MONOTONICITY`, 1 "never run a third fix cycle". This matches the rf-qa Retry Monotonicity Protocol order (regression, monotonicity, hard cap). |
| Cycle-1 decision item handles both outcomes | PASS | 3.G12, 5.G12, 7.G12, 8.G12, 9.F13, 9.M8 each: PASS writes verdict plus `CYCLE2=not-needed`; FAIL runs regression then monotonicity guards, then writes `CYCLE2=run` and `F_n=<n>`. After normalization 5.G12, 7.G12, 8.G12 equal 3.G12 exactly. |
| Decision-file protocol consistent | PASS | Each gate uses exactly one `phase-outputs/plans/<gate>-cycle-decision.md` (`gate-a`, `gate-b`, `gate-c`, `gate-d`, `final-gate`, `m4`), referenced twice in the cycle-1 decision item, once in the first cycle-2 item and once in the last. Values are only `CYCLE2=run` (plus `F_n=<n>`) and `CYCLE2=not-needed`. |
| Skip semantics when `CYCLE2=not-needed` | PASS | First item writes the "skipped: cycle 2 not selected" consolidation; G14 writes "skipped: cycle 2 not selected"; G15/G16 write "skipped: no cycle-2 fix applied"; last item confirms the cycle-1 verdict says PASS and appends "cycle 2: not run". |
| Item ordering and data flow (TB-Add-4) | PASS | cycle-1 decision item (writes decision file) precedes G13; G13 writes consolidation read by G14; G14 writes the fix report read by G15/G16; G17 reads all. The next phase reads the verdict file, which exists in both branches (written by the cycle-1 decision item on PASS, by the last cycle-2 item otherwise). |
| Post-fix re-run | PASS | The PASS branch of the last item re-runs `uv run pytest tests/issue_watch/ -v`, `make lint` and pinned ruff on changed files, records to `gate-<x>-postfix-cycle2.txt`. |
| M4 variant | PASS | 9.M8 and 9.M13 keep the NEEDS OWNER DECISION halt; 9.M10 tells the fix agent to record a design-or-spec-dependent finding as "needs owner decision"; 29 DEVIATION ids are listed in 9.M12. See minor note M-4 for one ordering ambiguity. |
| Gate item counts | PASS | 17 / 17 / 17 / 17 / 18 / 13 as the intros claim. |
| Review agents unchanged | PASS | No new lens agent; the totals are still 6 + 6 + 6 + 6 + 7 + 3 = 34. |

## 5. Spot-check of changed and new item text against the design and research (13 checks)

| # | Item | Claim checked | Source | Result |
|---|---|---|---|---|
| 1 | 3.1a | G1 to G7 argv, `PAGE_SIZE`/caps, `MARKER_JQ` built from the marker, GraphQL carries no `--method`, jq projections | design 8.1 table (lines 541-558) | matches |
| 2 | 3.1b | classify order and substrings, `HTTP 5` plus two digits, rate-limit time table (Retry-After, reset epoch, 3600 clamp, `rate_limit_clamped`) | design 8.2 table (lines 579-588), 8.3 (lines 596-600) | matches |
| 3 | 3.1c / 3.7 | page longer than 100 is unreadable, not incomplete | research/06 DF-19 (line 146) | matches |
| 4 | 4.1a | Entry has the 17 fields; `PendingContext` six fields are the `pending`-write fields | design lines 417-437 | matches (17 rows counted) |
| 5 | 4.1c | T-1 to T-13 effects: T-3 at attempts 3, T-4 sets `launches` 1 and times, T-5 lease 60 min, T-10 from three states, T-11 none, T-12 `failed`, T-13 removal and `consumed_log` | design 7.4 table (lines 476-490) | matches |
| 6 | 5.1 | `launch_argv` has exactly 12 elements; outcome mapping rows | design lines 625-636 | matches (12 counted) |
| 7 | 5.1 / 5.6 | original `_find_orca` catches `AttributeError` for a top-level list, raises for non-dict element | `src/superclaude/cli/install_user_setup.py:208-221` | matches |
| 8 | 5.1 | operation-id rule has no design text-scraping rule | design line 636 and 689 | matches; the task's stdout-then-stderr JSON rule is a recorded reading (OQ-47) |
| 9 | 2.3 / 6.1 / 6.6 | `REASON_TABLE` has 57 entries, kind and exit per reason; `exit_for` reads it | research/06 DF-41 (line 175); hand count of the names in 2.3 | matches (57) |
| 10 | 9.3 | `.markdownlint.json` is the rules file (`default: true`; MD013, MD029, MD033, MD036 off; MD024 siblings only); hook exclude list at `.pre-commit-config.yaml:74-88` | both files read | matches |
| 11 | 9.5 | `SRC` line 23, `TIER_TEXT_DIRS` line 48, retired-docs test globs `*.md` | `tests/skills/test_model_alias_policy.py`, `tests/docs/test_retired_docs_absent.py` | matches |
| 12 | 9.17 / headers | AC Ids column at design 872-898; FR/NFR rows at design 902-934 | design lines 872-935 | AC range matches; FR/NFR range is off by one (note M-1) |
| 13 | Gate prompts / 9.M12 | M4 has three agents; 29 DEVIATION ids | research/06 DF-08 (line 31) | matches |

## Items Reviewed

The live catalogue in `/home/coder/.claude/agents/rf-qa.md` ("Structural Gate Additions", lines 335-366) lists these structural checks: TB-Add-1, TB-Add-3, TB-Add-4, TB-Add-5, TB-Add-6, TB-Add-7, TB-Add-8 (there is no TB-Add-2 in the catalogue).

| Check | Result | Evidence |
|---|---|---|
| B2 self-containment, new and changed items (3.1a-c, 4.1a-c, 30 cycle-2 items, 10.7, edited items) | PASS | Each is one `- [ ]` paragraph with context, action, output paths, verification clause ("Ensuring ...") and the blocker clause; script found only 1.1, 2.11 and 10.6 without the standard closing clause, same as the backup. Cycle-2 spawn items embed full prompts. |
| B2 self-containment, unchanged items | PASS (reliance noted) | Byte-identical to the backup outside the 60 hunks (diff); prior b2 reports passed them. Not re-read word by word. |
| B2 atomicity (TB-Add-5 / check 10) | PASS | `github.py` and `record.py` split in three parts each; 2.2, 2.3, 5.1 carry single-item justification comments (lines 194, 197, 363); 6.2 (7,542 chars) and 6.7 remain single large items, already a recorded note (N-20) and justified by the Phase 6 intro for the file split. |
| Phase structure and order | PASS | Phases 1 to 10 in order, gates after Phases 3, 5, 7, 8 and 9; no gaps; each phase begins with the prior gate-verdict pre-check (Phase 4, 6, 8, 9 headers, and the M4 intro for the Final verdict). |
| Phase header and intro counts (check 18) | PASS | Counts 8, 11, 13, 17, 9, 11, 17, 11, 9, 17, 12, 17, 19, 18, 13, 7 = 209; intro claims of 17, 18, 13 and 209 match. |
| Prose counts (check 19) | PASS | Task Overview line 72: 34 lens agents, 209 items, five commands, 8 modules; consistent with the counts above. See minor note M-2 for the stale TCS sentence. |
| Intra-phase and item-level dependencies, no cycles (TB-Add-4, checks 11, 15, 16) | PASS | Split parts read only earlier parts; fixtures (5.2) read `OPERATION_ID_PATHS` from 5.1; the cycle-2 chain is strictly forward (decision item, then G13 to G17); no new forward reads of an uncreated file. |
| Duplicate operations (check 12) | PASS | New repeated commands occur only inside conditional cycle-2 items and after a fix, which justifies the re-run; 9.17/9.18 re-run list is justified by an intervening fix. |
| TB-Add-1 placeholder scan | PASS | `grep -E '\b(TBD\|TODO\|FIXME)\b'` returns no line; no title-only item (209 of 209 headers are followed by a full item). |
| TB-Add-3 clarification adjacency | PASS | Items that depend on an open question cite its index: 2.2 (OQ-37, 38), 5.1 (OQ-40, 47), 6.2 (OQ-36, 39, 48), 4.1a (OQ-48, 41), 10.2 to 10.4 and 10.7 (OQ-7, 35); every cited id is defined (49 entries). |
| TB-Add-4 circular dependency | PASS | See dependency row; no item references a later item as a prerequisite; mentions of later steps (for example Step 8.8 in 5.1 and 6.3) are verification pointers, not inputs. |
| TB-Add-5 granularity | PASS | See atomicity row; B-05 satisfied by split or comment for 2.2, 2.3, 3.1, 4.1, 5.1. |
| TB-Add-6 Verification format consistency | PASS (note) | New items use the same "Ensuring ..." closing form as the old ones; the task never used a `Verify:` prefix, which is the standing minor note N-13. |
| TB-Add-7 Execution Context source areas | PASS (unchanged) | The `### Source Areas` block (lines 113-120) and the items that name those areas are unchanged by the fixes; the consumer spot check `grep -cE "src/\|/.*:[0-9]+"` over lines 104-127 returns 1, the verbatim goal line already accepted as note N-23. |
| TB-Add-8 per-item Context evidence binding | PASS | 3.1a, 3.1b, 3.1c, 4.1a, 4.1b, 4.1c each carry an evidence-absence comment plus design line anchors; evidence-absence count rose from 53 to 57; the items without a file:line are gate-run and gate-agent items, the same set as before plus the new cycle-2 items (standing note N-21). |
| Research alignment, DF coverage | PASS | Items still cite 57 of 60 decision ids (DF-26, DF-38, DF-40 are prose or Open Questions decisions, uncited before and after); no id was dropped from the items; the 29 DEVIATION ids are intact in 9.M1/9.M2/9.M12; the three alignment findings are applied (DF-19 in B-13, DF-41 in B-14, naming rule in B-15). DF-36 is now exceeded by the parity test (it also compares the top-level-list case); this is stricter and verified against the code. |
| Open Questions section integrity | PASS | 49 entries OQ-1 to OQ-48 plus OQ-41a; OQ-47 and OQ-48 added in section D; the 29-departure count is unchanged and OQ-36 and OQ-41a are named as authorized readings. |
| POST reflect position | PASS | Step 10.6 is the penultimate item and Step 10.7 (Done) the last of Phase 10; `reflect_post_mode: skill` in the unchanged frontmatter; the reflect prompt uses `--depth deep` and the `<BASE SHA>` substitution from `base-sha.txt`; no item follows 10.7. |
| Gate agent totals | PASS | A 6, B 6, C 6, D 6, Final 7, M4 3 = 34 (script count of lens-agent spawn items per gate range). |
| Cycle-2 conditional items (3.G13-17, 5.G13-17, 7.G13-17, 8.G13-17, 9.F14-18, 9.M9-13) | PASS | Section 4. |
| No nested checkboxes, frontmatter unchanged | PASS | Section 3. |
| Execution Context / header scope, intro wording | PASS | Phase 2, 3, 4, 8 headers and gate intros read; wording consistent with the items. |

## Summary

- Blocking findings verified: 15 of 15 FIXED; FIXED-BUT-INTRODUCED-DEFECT: 0
- Checks passed: 22 of 22 rows of the Items Reviewed table (plus the 13 spot-checks and the 30-item cycle-2 section, all PASS)
- Checks failed: 0
- Critical issues: 0; IMPORTANT (blocking): 0; MINOR (notes): 5
- Regressions against the backup: none
- Issues fixed in place: 0 (verification only, `fix_authorization: false`)

## Issues Found

All five are minor: they are notes, never rechecked, and do not fail the gate.

| # | Severity | Location | Issue | Suggested fix (optional) |
|---|---|---|---|---|
| M-1 | MINOR | Phase 2 header (line 186), Phase 8 header (line 579), Step 9.17 (line 729) | The FR/NFR range "lines 902-934" of design section 18 stops one line short: the table runs 902-935 and line 935 is the `NFR-014` row. A true claim with a wrong line number (introduced by the B-15 fix). Step 9.17 also names NFR-014 explicitly, so an executor will still find it. | Replace `902-934` with `902-935` in all three places. |
| M-2 | MINOR | Reflect Depth Derivation (line 1024) | The S5 sentence "no item Context cites an OQ id, so the fallback counts the non-empty Open Questions entries = 47" is stale: items now cite OQ ids and the section has 49 entries. The band (`deep`) cannot change and the same paragraph says TCS was not recomputed, so no decision depends on it. | Reword S5 to "items cite OQ ids; S5 not recomputed (band unchanged)". |
| M-3 | MINOR | Steps 10.2 and 10.7 | If the owner withdraws the checkpoint commit, 10.2 says to skip Steps 10.2 to 10.4 and run 10.6 over a named base, but 10.7 still requires `commit-result.md` to show exit 0 and one commit, so Done would turn into Blocked. This is only the unlikely withdrawn branch, and 10.7 does say OQ-7/OQ-35 block in that case. | In 10.7 accept "Steps 10.2 to 10.4 skipped because the owner withdrew the commit, noted in the Phase 10 findings" in place of `commit-result.md`. |
| M-4 | MINOR | Steps 9.M8 and 9.M13 | The PASS branch ("zero blocking findings, or BOTH verification reports say PASS") is listed before the NEEDS OWNER DECISION halt. If a verifier writes verdict PASS while a row says NEEDS OWNER DECISION, the order is ambiguous. The fix agent and verifier prompts make a NEEDS OWNER DECISION row a blocking finding, so the case should not arise. | State that a NEEDS OWNER DECISION row prevents the PASS branch. |
| M-5 | MINOR | Step 4.1c | `sweep` is described twice in one item (as a transition function and again as "the helpers `day_cap_count` and `sweep` as pure functions"); present in the backup too. Harmless repetition. | Drop `sweep` from the second list. |

## Actions Taken

None. This was a read-only verification; the only file written is this report. Temporary helper scripts and diff output are under `/tmp` (`/tmp/rfqa-*`, `/tmp/rfqa-work/wd.py`).

## Recommendations

- Proceed to the next task-builder step. No blocking issue is open, so no second fix cycle is needed.
- The minor notes M-1 to M-5 and the 38 earlier notes (N-01 to N-38) may be left as notes. If the coordinator wants one cheap clean-up, M-1 (three one-token edits) is the only one that corrects a wrong citation.

## Confidence and tool engagement

- **Confidence:** Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The two b2 rows for unchanged items rest on a byte-identical diff plus the earlier passing reports (reliance, stated in the table); every changed or new item was read in full or compared word by word.
- **Tool engagement:** Read: 22 | Grep: 9 | Glob: 0 | Bash: about 28 (including two `uv run python -I` diff runs); the counts exceed the 22 checklist rows.
- No web research was performed (no Tavily or fallback calls).
- UNCHECKED items: none. UNVERIFIABLE items: none.

QA Complete

VERDICT: PASS

