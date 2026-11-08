# QA Report - Cross-Source Contradictions (M4 fidelity gate, agent 3 of 3)

**Topic:** issue-watch design vs spec
**Date:** 2026-11-08
**Phase:** report-validation (lens: cross-source-contradictions), report only (fix_authorization: false)
**Fix cycle:** 1 (first review)

## Overall Verdict: PASS (with minor notes). Blocking NEW contradictions: 0

Scope read in full this session: design `docs/designs/issue-watcher.md` (935 lines, D), spec `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (515 lines, S), decision register `research/06-gap-fill-decisions.md` (DF-01 to DF-60, Tables 1.2 to 1.6, phase plan). To classify a contradiction as resolved I also read the Open Questions section of the task file (OQ-1 to OQ-51) and `phase-outputs/reports/deviation-register.md` (Table 2 item 1). I did not read any implementation file. One source file, `src/superclaude/skills/sc-issue-protocol/refs/claim.md` lines 20-60, was read only to check a citation (D C7 and S R18 both cite claim.md:26; both are true, because line 26 holds the `gh issue view` text read and the `gh api user` call, so no contradiction).

Classification keys: DF-nn = register decision; Q-n = owner question (D 866); X-n = spec-versus-design choice (DF-50: X1 S1 reading, X2 full-argv retry, X3 3600 s clamp, X4 `last_completed_cycle_at`, X5 `status` exit 1); OQ-n = Open Questions entry of the task file (section D proposal values); DREG-T2-1 = deviation-register Table 2 item 1; NEW = no decision found.

## Part A. Contradictions already covered by a decision (all minor notes)

| id | design lines | spec lines | the contradiction | classification | severity |
|---|---|---|---|---|---|
| C-01 | 177, 759 ("6 verbs") | 190 (FR-026) | D says six verbs; the six usage rows (D 112-119) are five command names | COVERED-BY-DF-06 (in the 29) | minor |
| C-02 | 218, 264-265 | 309 | S: free function `run_command(argv, timeout)`; D: `Runner` Protocol, `SubprocessRunner`; D has no `cwd` though D 625 needs it | COVERED-BY-DF-01 (in the 29) | minor |
| C-03 | 222, 604 | 154, 309 | S: `find_orca(runner)`; D: `find_orca(runner, which)` | COVERED-BY-DF-54 | minor |
| C-04 | 100 (C19), 613 | 154 | S: "same acceptance rule as `_find_orca`"; D rejects a non-dict topic that the original raises on; the original also raises on `null`, int, str and dict topics | COVERED-BY-DF-36 | minor |
| C-05 | 101 (C20), 741 | 160-161 (FR-015 GWT) | retry text: S `<orca> agent launch --retry-launch op-1 --json`; D the full original 12-element argv plus the flag | COVERED-BY-Q-2 / X-2 (DF-50, in the 29) | minor |
| C-06 | 104 (S1), 388 | 163-164 (FR-016) | S GWT "examines k and launches 1" vs S text "a second eligible candidate is never reached" | COVERED-BY-Q-1 / X-1 (DF-50) | minor |
| C-07 | 103 (C22), 602 | 196-197 (FR-028) | S: `Retry-After: 120` gives now+120; D: only G1 carries headers, so every per-issue limit clamps to 3600 s with `rate_limit_clamped` | COVERED-BY-Q-3 / X-3 (DF-50), DF-51 | minor |
| C-08 | 410, 360 | 267 | D adds store key `last_completed_cycle_at`; S schema lacks it | COVERED-BY-X-4 (DF-50) | minor |
| C-09 | 115, 121 | 187, 315-326 | `status` exit 1 (unhealthy) exists only in D; the S exit table has no code for it | COVERED-BY-X-5 (DF-50) | minor |
| C-10 | 30, 766 | 32, 384 | runbook: S inside the design doc; D a separate `issue-watcher-setup.md` | COVERED-BY-DF-60 (in the 29) | minor |
| C-11 | 570-572, 118-119, 449, 718 | 136, 330-358 | D needs reasons the closed S table lacks (marker/edits unreadable, reset audit lines, dry-run shadow reset) while `audit.line` raises on an unlisted reason | COVERED-BY-DF-02, DF-03, DF-22, DF-57 | minor |
| C-12 | 118 | 190, 297 | `reset N` with no entry is undefined | COVERED-BY-DF-04 (in the 29) | minor |
| C-13 | 399 ("every exit of `once` and `reset`") | 330-358 | only the reset success paths had a line | COVERED-BY-DF-57 | minor |
| C-14 | 892 (AC-19) | 219 (NFR-008) | "sleeping stub ends with `gh_timeout`" cannot run in subprocess mode at 20 s | COVERED-BY-DF-55 (in the 29) | minor |
| C-15 | 896, 798 | 366 | gate `make test` vs the affected subset locally | COVERED-BY-DF-05 (in the 29) | minor |
| C-16 | 800 | none | `uv run ruff format --check` vs pinned `uvx --offline ruff@0.15.20` | COVERED-BY-DF-09 | minor |
| C-17 | 765, 780 | 361 | committed `stubs/gh`, `stubs/orca` vs stubs written at test time | COVERED-BY-DF-10 | minor |
| C-18 | 93 (C12), 693 | 213 | `property_based` marker on a test that does not use hypothesis | COVERED-BY-DF-12 | minor |
| C-19 | 441 vs 362 | 181 (FR-019) | "migrated store saved under the lock before any other step" vs dry-run never writes `dispatch.json` | COVERED-BY-DF-17 | minor |
| C-20 | 572 | none | "item missing a field" vs `--jq` that always emits every key (null) | COVERED-BY-DF-18 | minor |
| C-21 | 131-132 | 82 | `gh issue list --label` splits on comma; the D label rule allowed one | COVERED-BY-DF-20 | minor |
| C-22 | 110, 137 | 193 | default config path contains `~` but must be "absolute after expansion" | COVERED-BY-DF-13 | minor |
| C-23 | 296 vs 779 | 213 | "raises at the k-th write" vs `crash_at="C1".."C5"`; S asks 5 reruns | COVERED-BY-DF-15 | minor |
| C-24 | 297-298 vs 777-778 | none | `RecordingLauncher` and `FakeClock(start, step)` vs `FakeLauncher` and `FakeClock(now, mono)` | COVERED-BY-DF-24 | minor |
| C-25 | 224 vs 745 | none | `slo_numbers(lines, store, now)` vs `(lines, doc: StoreDoc, now)` | COVERED-BY-DF-25 | minor |
| C-26 | 221, 350 vs 492, 737 | none | `sweep(store, now)` and `day_cap_count(store, now)` vs functions on `StoreDoc` | COVERED-BY-DF-44 | minor |
| C-27 | 95 (C14) vs 761 | none | premise "name collision with `tests/cli_portify/test_cli.py`" is false | COVERED-BY-DF-27 | minor |
| C-28 | 102 (C21) vs 554 | none | "every G2 to G7 argv" has `--method GET` vs the precise rule (G2 is `gh issue list`, G5 and G6 are GraphQL) | COVERED-BY-DF-28 | minor |
| C-29 | 244 vs 173, 760 | 309 | "imports the package lazily" vs the eager `reflect` pattern | COVERED-BY-DF-29 | minor |
| C-30 | 437 vs 237-239 | none | `record` validates `last_reason` membership but may not import `audit` | COVERED-BY-DF-42 | minor |
| C-31 | 476-492 | 285-288 | no T-row for `failed` to `failed` (attempts + 1) while "any other pair raises" | COVERED-BY-DF-43 | minor |
| C-32 | 295 vs 776 | none | `FakeRunner` script value `CommandResult \| Callable` vs `Reply` | COVERED-BY-DF-48 | minor |
| C-33 | 774-790 (test list) | 213 (NFR-005) | S requires an account-rename test; the D test list has none | COVERED-BY-DF-47 | minor |
| C-34 | 220 vs 545 | 142 | marker literal appears twice (`CLAIM_MARKER`, `MARKER_JQ`) | COVERED-BY-DF-21 | minor |
| C-35 | 791 | 142 (FR-009) | "dual surface" read of `claim.md` is not available in CI | COVERED-BY-DF-46 | minor |
| C-36 | 709 (cycle line has `reason`, enum = S table) | 184, 330-358 | no S reason exists for a normal exit-0 cycle or a crash line | COVERED-BY-DREG-T2-1 (`cycle_complete`, `cycle_crashed`; the table now has 59 names) | minor |
| C-37 | 354 (step 11, marker read first for every state) | 103 vs 296 | S-internal: a `failed` entry in backoff gets only the marker read (S 103) but T-12 needs the current approval time | COVERED-BY-OQ-36 | minor |
| C-38 | 614 vs 277-279 | none | probe cache "in the `OrcaLauncher` instance" vs a `Launcher` Protocol with one method | COVERED-BY-OQ-41a | minor |
| C-39 | 362 (`probe: skipped`, `would_launch`) vs 701-716 (closed audit key list) | 181-182 | dry-run would-launch line has no reason and no key in the closed schema | COVERED-BY-OQ-39 | minor |
| C-40 | 633 vs 634 | 157-158 | rows overlap: exit 0 plus an operation id (launched) vs `agent_session_operation_unknown` anywhere (unknown) | COVERED-BY-OQ-40 | minor |
| C-41 | 689 (an id failing `^[A-Za-z0-9._:-]{1,128}$` is stored null and the outcome is `unknown`), 633 | 157 (exit 0 plus a non-empty operation ID is `launched`) | D adds a pattern check that turns a non-empty id into `unknown`; D 633 itself says a non-empty `str` gives `launched` | COVERED-BY-OQ-47 for the pattern; the launched-path override is D 689's own explicit choice and is safe-direction (at-most-once is kept) | minor |

## Part B. Contradictions with no decision of their own (NEW)

None of these changes a launch outcome, a safety property, an exit code or a deliverable in a single-failure case; each is graded minor with the reason given. They stay notes and are not rechecked.

| id | design lines | spec lines | the contradiction | classification | severity |
|---|---|---|---|---|---|
| N-01 | 166 ("the combinations that can occur are 7 with 5 and 7 with 3": a `failed` entry, then a later read is rate limited or times out), 386 (after any launch-step outcome later candidates are neither read nor stamped) | 197 (FR-028 GWT "given a `failed` entry written earlier in the same cycle, it stands"), 163-164 | A pre-pending `failed` entry is written in step 12, the last step that makes any call (D 355-358: steps 13 to 15 make none) and under the S1 stop rule no candidate is read afterwards. The 7-with-5 and 7-with-3 combinations and the FR-028 GWT scenario are unreachable as worded. The stop rule itself is decided (Q-1/X-1); the leftover wording is not. | NEW residual of X-1 | minor: production behaviour is decided by Q-1; only a design sentence and one test description are unreachable (`resolve_exit` is a pure function over a condition set and is testable either way). Owner to confirm that a pre-pending `failed` ends the cycle. |
| N-02 | 322 (diagram: events, comments, edits, items), 545-548 (G3 events before G4 marker), versus 354 and 384 (step 11 and r = 4: marker first, then events, edits, items) | 102-105 (Eligible: approved, then not claimed, then unchanged, then Project; "the first failure is the skip reason") | D contradicts itself on the read order and 354/384 contradict the S order. A marker first cannot decide `claimed` for a no-entry or `failed` entry anyway, because T-11 and T-12 need the current approval time (S 295-296; D 488-489), so the marker read must be evaluated after the events read. The observable contract (first failing check, in the S order, is the reason) is S's. | NEW | minor: read order only changes the reason when two checks fail at once; the result (no launch) is the same, and the literal D order cannot be implemented for T-11/T-12 |
| N-03 | 460-461 (diagram arrow "own marker newer than pending_at"), 502, 7.4 T-10 (at or after `pending_at` - 300 s) | 100 (300 s tolerance), 143 (FR-009 GWT "only a marker older than T: stays `launched`"), 294 (transition "newer than `pending_at`") | S-internal: the GWT and transition row say "older/newer than T", Section 3 allows a 300 s skew tolerance, so a marker up to 300 s older than T already counts. D follows Section 3 in 502 and T-10 but keeps the shorter wording in its diagram. | NEW | minor: Section 3 is the specific rule; a test for "older than T" must use more than 300 s |
| N-04 | 546-548 (G4 path `/comments`, G5 requests `comments{nodes{...}}`) | 122 (FR-003 GWT "no recorded argv requests `title`, `body` or `comments` as a field"), 207 (NFR-002 allows the `repos/.../comments` read and the edit-timestamp projections) | The FR-003 GWT read literally forbids argv that NFR-002 and Section 3 require (marker and edit-time reads). The intent is "no text field", as D 556 says. | NEW | minor: a scan must target requested fields (`title`, `body`, comment `body`), not the word `comments` |
| N-05 | 369, 22 (RC2 row: `is_intended_owner` re-checks the discovery result) | 98 (`unassigned` and `assigned_other` "arise only in unit tests and in the FR-011 re-read"), 121 and 139 (FR-003 and FR-008: non-owned issues are dropped before any per-issue call) | `gh issue list --assignee <login>` also returns an issue assigned to {own, other}; S 121 and 139 filter it at discovery, S 98 says it can only be seen at the re-read. D follows FR-003/FR-008. | NEW | minor: S-internal; D follows the two requirement rows, which also spend fewer calls |
| N-06 | 369-372 (flow table: local checks drop `already_dispatched` before the GitHub checks) | 103 (an entry in `launched`, `unknown`, `abandoned` or `failed` still gets the marker read) | D 6.3 table disagrees with D 354 ("marker for every entry state that can reach `claimed`") and with S 103 | NEW | minor: the 6.3 table is a rough flow; 354 and S 103 agree |
| N-07 | 640 ("every runner call gets `min(configured, remaining())`") vs 647 (Orca launch "never shortened") | 199 (FR-029: the lesser-of rule is for `gh` and probe calls; a started launch is never cut short) | D 640 over-states its own rule; the table and S agree | NEW | minor: wording |
| N-08 | 823 (5 MiB x 4 files, "about 60 days of cycle lines per file at about 300 bytes a line") | 184 ("at least 25 MiB, about 40 days at 10 candidates per cycle") | Two different retention figures for one setting (per file at cycle lines only vs the whole set at 10 decision lines per cycle). Neither is a requirement. | NEW | minor: rationale text only |
| N-09 | 855 (FU-3: fine-grained token scope when the owner moves off the CLI login), 862 (FU-10: after 7 days live) | 402 (FU-3: confirm `read:project` and the `projectItems` read), 409 (FU-10: two weeks of real logs) | Follow-up items carry different content and timing; D 58 and 133 also use FU-3 for "Project access" | NEW | minor: follow-ups are not built |
| N-10 | 129, 139 (required `schema_version`, unknown keys rejected exit 2, `labels.approval` must differ from `labels.trigger`, 50-character limit) | 193 (FR-027 field list has none of these) | D adds required config validation that S does not state, so a config built from the S field list alone fails `check-config` | NEW | minor: elaboration, not a conflict; the setup runbook (built from D) must show `schema_version` |
| N-11 | 110 (`--config` on every verb), 117 (`init-state` exits 6 when a store exists) | 190 (flags per verb: only `once` gets `--config` in S 312), 324 (exit 6 means record unreadable or unwritable, or store or lock missing) | D adds `--config` to the other verbs because they need `state_dir`, and picks exit 6 for "store already exists"; S is silent on both | NEW | minor: gaps in S filled by D |
| N-12 | 350 (sweep makes no call and moves every `launched` past its lease to `abandoned`) | 293 (`launched` to `abandoned` on lease end "with no marker") | The sweep cannot know there is no marker without a read; the later marker read moves the entry to `claimed` (S 294, A-009 at S 514) | NEW | minor: wording; A-009 makes the order harmless |
| N-13 | 86 and 564 (`poll-augment-review.sh:48-77` for `fetch_rest`) | 92 and 470 (`:46-77`) | citation ranges differ by two lines (the function starts at line 48, the comment block at 46) | NEW | minor: citation |

## Summary

- Contradictions or inconsistencies found: 54 (41 covered by a decision, 13 with no decision of their own).
- NEW and blocking: 0. NEW and minor: 13. Covered (minor notes): 41.
- Checks that the numbers of the two sources agree (verified by reading both): 12-element launch argv (D 618-623, S 154); 35 calls with 3 reserved and 37 per worst cycle, 444 an hour, 8.88 percent, 24 an hour idle, 0.48 percent (D 380-381, S 221, 381); 5-page cap (D 575, S 92); 100-item pages (D 566-568, S 92); day cap 6 in a 24 h half-open window (D 500, 505, S 169, 269); 60-minute lease; 10-minute backoff; 3 attempts; 240 s deadline, 5 s floor, 120 s launch cutoff (D 644-649, S 199); 500-byte stderr cap; 5 MiB rotation with 4 files; 0600 and 0700 modes; 17 entry fields (D 419-437 and S 267 list the same 17); 52 spec reason names (counted from S 332-358; the register's 57 and the deviation register's 59 are decided additions); exit-code set 0, 2, 3, 4, 5, 6, 7, 75 and the precedence 2, 6, 7, 5, 3, 4 (D 155-166, S 315-328); 13 transitions (S 283-297 against D T-1 to T-13); nine revisit conditions (D 60, S 63); the Coder#477 statement (D 49, S 414: identical text); FU-1 to FU-12 present in both. No disagreement found in any of these.
- The "at least 15 contradictions" assumption held in count (54) but not in severity: every contradiction that changes behaviour is already decided by DF, Q, X, OQ or the deviation register.

## Minor notes carried forward (not rechecked)

1. N-01 deserves one owner confirmation line: a pre-pending `failed` entry ends the cycle (no later candidate is read), so the FR-028 GWT "a `failed` entry written earlier in the same cycle stands" can only be shown by a store that already holds such an entry, or by a condition other than `failed`. If the owner prefers that the cycle continues after a `failed` entry, Q-1 must be amended; the code would then need to change.
2. N-02: if anyone later reorders the per-issue reads, the S order (approval events, then marker, then edit timestamps, then Project items) is the contract; D 354 and 384 are the outliers.
3. C-41 and OQ-47: D 689 turns an id that fails the pattern into `unknown`. This is the safe direction. If the owner wants S 157 followed literally (any non-empty string is `launched`), the status retry line must then be suppressed for such an id instead.
4. N-10: `docs/designs/issue-watcher-setup.md` should show `schema_version: 1` in its config example.

## Items Reviewed (lens checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Design read in full (935 lines) | PASS | Read of D lines 1-480 and 481-935 |
| 2 | Spec read in full (515 lines) | PASS | Read of S lines 1-340 and 341-515 |
| 3 | Every contradiction classified against DF-01 to DF-60, Q1 to Q4, X1 to X5 | PASS | register read in full for DF-01 to DF-60 (lines 1-234), Tables 1.2 to 1.6 and the phase plan; OQ-1 to OQ-51 read at task file lines 901-975; deviation register Table 2 |
| 4 | Residual items checked for a hidden decision | PASS | Grep for `would_launch`, operation-id regex, "7 with 5", "after any launch-step", "first eligible" in research/ and the task file; research/05 line 164 (trap T-D) confirms the stop rule is part of X-1 |
| 5 | Numeric and name cross-check of counts, windows, codes | PASS | list in the Summary, each re-read in both sources |
| 6 | Citation cross-check | PASS | `claim.md:20-60` read; `poll-augment-review.sh:44-80` sampled |
| 7 | No implementation file read; only this report written | PASS | no Write or Edit outside this path |

Confidence: Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Limits: the 29 authorized departures were taken as listed in the invoking prompt and DF-40; I did not re-derive their text from the implementation, which this lens forbids.

Tool engagement: Read: 10 | Grep: 8 | Glob: 0 | Bash: 8. No web research was done (no Tavily or fallback calls).

## Actions Taken

None (report only; `fix_authorization: false`). No file other than this report was created or changed (the folder `qa/m4/` already held `qa-source-fidelity-report-1.md` from the sibling agent; I did not touch it).

## QA Complete
