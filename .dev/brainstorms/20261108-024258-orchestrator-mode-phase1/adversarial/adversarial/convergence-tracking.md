# Convergence Tracking: Orchestrator Mode Phase 1 (#339) debate

- Role: convergence tally clerk (no advocacy)
- Date: 2026-11-08 (from session context)
- Inputs read: `diff-analysis.md` (235 lines), `debate/round1-advocate-v1.md` (217), `debate/round1-advocate-v2.md` (229), `debate/round1-advocate-v3.md` (161), `debate/round2-rebuttal-v1.md` (139), `debate/round2-rebuttal-v2.md` (110), `debate/round2-rebuttal-v3.md` (73). Each was read in chunks of 150 lines or fewer. No variant file, `qa/` file, code or live tool was read or run.
- Counted points: 100 (S 13, C 43, X 19, A 25). The 33 U-NNN points are not counted.

## 1. Method

### 1.1 How positions were read

- Round 1 positions come from each advocate's per-point table (V1R1 sections 6 and 7, V2R1 sections 8 and 9, V3R1 "Per-point positions" and "Shared assumptions").
- Round 2 positions start from Round 1 and apply only the rows each rebuttal lists as changed (V1R2 sections 3 and 4, V2R2 sections 3 and 4, V3R2 "Updated per-point positions"). Every row not listed keeps its Round 1 value. Confidence-only changes (V1R2 lists six) do not change a position and are not counted as changes.
- Prose that argues for something without changing the table row is not counted as a position change. Where this matters it is noted (C-012, C-022).

### 1.2 Normalisation rules

1. A row is the variant label the advocate gave, after these steps.
2. V2's tag "V2 (= V1)" means V2 says its approach on that point is the same as V1's. It is written `V1=V2` and matches a V1 or a V2 choice. Likewise "V2 (= V3)" is `V2=V3`, and "V1 / V3" is `V1=V3`.
3. Where `diff-analysis.md` records two variants' approaches on a point as the same ("Same" in its table), a choice of either variant is the same position. This applies to C-015, C-033, C-042, X-001, X-016 (V1 and V2 identical), X-009 (V1 and V3 both `orca-ide`) and X-014 (V2 and V3 both include the Shift Brief).
4. V2's X-002 entry "V1 (V3 wording)" is written `M V1+V3`, because it takes V1's predicate and V3's text.
5. A merge equals a single-variant choice only when the merge's extra part is already in that variant's approach as `diff-analysis.md` describes it. Used for S-011, C-004, C-011, C-016, C-021 (Round 2), C-025, C-035 and C-037; each is noted in its row. Where the extra part is not already there, the merge is a different position (C-014, C-017, C-022, C-034, and X-006 in Round 1).
6. A-NNN: ACCEPT and QUALIFY both mean the assumption stands. REJECT means it does not. The A winner is "stands" or "rejected".
7. Agreement: 3 of 3 or 2 of 3 on the same normalised position gives Agreed = Y, and the majority position is the winner. Otherwise Agreed = N.
8. Convergence = agreed points / 100.

### 1.3 The A-101 and A-103 mapping

- `diff-analysis.md` does not number the shared assumptions A-001 to A-025. It numbers them A-001 to A-017 (agreement points, lines 179-195) plus A-101 to A-108 (the eight promoted [SHARED-ASSUMPTION] points, lines 201-208; line 175 says "promoted below to a synthetic diff point (A-101 onward)"). That is 25 points.
- All three Round 1 files use the same A-101 to A-108 labels, so V2's labels match the source. The premise that A runs only A-001 to A-025 does not match the file.
- V2R1 line 207, "A-101 REJECT", says the assumption "is UNVERIFIED and, if false, defeats the first safety item" and refers to Orca's own git. That is diff-analysis A-101: Orca read verbs (`worktree ps`, `worker-show`) do not run a plain `git status` in worker worktrees. In a sequential 1 to 25 count it is the 18th A point (A-018).
- V2R1 line 209, "A-103 REJECT", says "No allowlisted read is named as the source of `worker_done`". That is diff-analysis A-103: some allowlisted read shows whether `worker_done` was sent. Sequentially it is the 20th A point (A-020).
- V2R2 lines 107-108 move both to QUALIFY.
- This file keeps the diff-analysis labels. Sequential equivalents: A-101 = A-018, A-102 = A-019, A-103 = A-020, A-104 = A-021, A-105 = A-022, A-106 = A-023, A-107 = A-024, A-108 = A-025.

### 1.4 Table key

- `M` = merge, for example `M V1+V3`. `(chg)` marks a Round 2 cell that the rebuttal changed.
- Agreed column: `R1/R2`, each Y or N.
- Winner column: the Round 2 winner. If the Round 1 winner differs, the Note says so.
- A rows: A = ACCEPT, Q = QUALIFY, R = REJECT.

## 2. Per-point table

| Point | Level | R1 v1 | R1 v2 | R1 v3 | R2 v1 | R2 v2 | R2 v3 | Agreed | Winner | Note |
|---|---|---|---|---|---|---|---|---|---|---|
| S-001 | L1 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous |
| S-002 | L2 | M V1+V3 | V2 | M V1+V3 | M V1+V3 | V2 | M V1+V3 | Y/Y | M V1+V3 | V1 and V3 merges match: V1 sections plus V3's CLI and re-run section |
| S-003 | L1 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous |
| S-004 | L1 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous; merge must renumber |
| S-005 | L2 | V1 | M V1+V2 | V1 | V1 | M V1+V2 | V1 | Y/Y | V1 | V2 adds data flow and rejected placements |
| S-006 | L2 | V1 | M V1+V2 | V1 | V1 | M V1+V2 | V1 | Y/Y | V1 | V2 wants V1 types inside its 7.1/7.2/7.3 split |
| S-007 | L2 | V2 | V2 | M V1+V2 | V2 | V2 | M V1+V2 | Y/Y | V2 | V1 and V3 both note V1's Exit column can be added |
| S-008 | L1 | V2 | V2 | V2 | V2 | V2 | V2 | Y/Y | V2 | Unanimous |
| S-009 | L1 | V2 | V2 | V2 | V2 | V2 | V2 | Y/Y | V2 | Unanimous |
| S-010 | L1 | V2 | V2 | V2 | V2 | V2 | V2 | Y/Y | V2 | Unanimous |
| S-011 | L2 | M V1+V3 | V3 | V3 | M V1+V3 | V3 | V3 | Y/Y | V3 | V3 already has per-requirement ACs plus the checklist, so V1's merge equals V3 in substance |
| S-012 | L2 | V2 | V2 | V2 | V2 | V2 | V2 | Y/Y | V2 | Unanimous |
| S-013 | L1 | V2 | V2 | V2 | V2 | V2 | V2 | Y/Y | V2 | Unanimous |
| C-001 | L3 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous: idle rule 7, explicit fallback rule 8 |
| C-002 | L3 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous |
| C-003 | L3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V2+V3 (chg) | M V1+V2+V3 (chg) | M V1+V2+V3 (chg) | Y/Y | M V1+V2+V3 | FLIP: R1 winner M V1+V3. R2 adds V2's note "Orca: exited; fenced evidence not readable" and a fixture-only label on rule 2 |
| C-004 | L3 | M V1+V3 | V3 | V3 | M V1+V3 | V3 | V3 | Y/Y | V3 | V1's partial note is already V3's "usable not yet judged" |
| C-005 | L1 | M V1+V3 | V3 | V3 | M V1+V3 | V3 | V3 | Y/Y | V3 | Majority V3 ("ownership review", never "foreign") |
| C-006 | L3 | M V1+V2 | M V1+V2 | V1 | M V1+V2 | M V1+V2 | M V1+V2 (chg) | Y/Y | M V1+V2 | V1 and V2 merges match: V1's six states incl. `unknown` plus archive-blocked blocks removal. R2 unanimous |
| C-007 | L3 | V1 | V1=V2 | V1 | V1 | V1=V2 | V1 | Y/Y | V1 | Unanimous in substance; V3 dropped its base-tree comparison |
| C-008 | L3 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous: includes non-ready `task-list --run` |
| C-009 | L3 | M V1+V2 | V2 | V1 | M V1+V2 | M V1+V2 (chg) | M V1+V2 (chg) | N/Y | M V1+V2 | R1 split three ways (status only plus walk; status, log, --version; status plus rev-parse). R2 unanimous: status only, root by path walk |
| C-010 | L3 | V1 | V2 | V1 | V1 | V1 (chg) | V1 | Y/Y | V1 | V2 conceded the version gate. R2 unanimous |
| C-011 | L3 | M V1+V2 | M V1+V2 | V2 | M V1+V2 | M V1+V2 | V2 | Y/Y | M V1+V2 | V2's NFR-002 already pairs argv test and control experiment, so V3's V2 equals the merge in substance |
| C-012 | L2 | V2 | V2 | V1 | V2 | V2 | M V1+V2 (chg) | Y/Y | V2 | Path walk. V1R2 and V2R2 prose add the `.git` file-or-folder AC without changing their rows; V3's merge label covers the same content |
| C-013 | L3 | V1 | V2 | V1 | V1 | V1 (chg) | V1 | Y/Y | V1 | V2 conceded `git log`. R2 unanimous |
| C-014 | L3 | M V1+V3 | M V2+V3 | V3 | M V1+V3 | M V2+V3 | V3 | N/N | none | UNRESOLVED. All keep V3's dedupe and partial coverage; V1 adds a capture-gated cursor template, V2 adds a fixed 101-row two-call AC |
| C-015 | L3 | V1 | V1=V2 | V2 | V1 | V1=V2 | V2 | Y/Y | V1=V2 | V1 and V2 identical (disk-only exit 0); unanimous in substance. Owner sign-off against Seed:63 still needed |
| C-016 | L2 | M V1+V3 | V3 | V3 | M V1+V3 | V3 | V3 | Y/Y | V3 | V3 = same 0/1/2 plus "exit 0 means published" |
| C-017 | L2 | M V1+V2+V3 | M V1+V2 | M V1+V3 | M V1+V2+V3 | M V1+V2 | M V1+V3 | N/N | none | UNRESOLVED. All keep V1's `class` key and additive-only schema; they differ on adding V2's per-row `evidence`/`notes` and V3's ID-only `waiting`, zero counts and JSON-after-publication |
| C-018 | L2 | V3 | M V2+V3 | M V2+V3 | V3 | M V2+V3 | M V2+V3 | Y/Y | M V2+V3 | V2 order (could not determine before working rows) plus V3 coverage, Shift Brief, footer |
| C-019 | L3 | V3 | V3 | V3 | V3 | V3 | V3 | Y/Y | V3 | Unanimous: collision suffix, exclusive reservation |
| C-020 | L3 | V3 | V3 | V3 | V3 | V3 | V3 | Y/Y | V3 | Unanimous: re-run contract |
| C-021 | L3 | V1 | V2 | V3 | V1 | M V1+V3 (chg) | V3 | N/Y | V1 | R1 three-way. R2: V2's merge text is V1's rule ("byte-identical report and JSON" with injected `now`), so V1 2 of 3; V3's rule is the same in substance |
| C-022 | L3 | M V2+V3 | V2 | V3 | M V2+V3 | V2 | V3 | N/N | none | UNRESOLVED. V1 and V3 include V3's "admission or rejection recorded"; V2 keeps "admitted" only; V1 alone adds V2's "Run's own task list" clause. V1R2 prose says "take V3's" but the row was not changed |
| C-023 | L3 | V3 | V1 | V3 | V3 | V3 (chg) | V3 | Y/Y | V3 | Periodic coordinator duty, no scheduler, no fixed cadence. Owner memory source UNVERIFIED |
| C-024 | L2 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | Y/Y | M V1+V3 | Unanimous: recommends nothing, V3's verb list, V1's pins |
| C-025 | L1 | M V1+V2+V3 | M V2+V3 | V3 | M V1+V2+V3 | M V2+V3 | V3 | Y/Y | M V2+V3 | V1 has no extra sentences on this point, so V1's three-way merge equals V2+V3 (lock-free sentence plus heartbeat sentence). See A-101 R2 condition on scoping |
| C-026 | L1 | V1 | V1=V2 | V1 | V1 | V1=V2 | V1 | Y/Y | V1 | Unanimous: three pins, count-free test rename |
| C-027 | L2 | M V1+V2+V3 | M V1+V2+V3 | M V1+V2+V3 | M V1+V2+V3 | M V1+V2+V3 | M V1+V2+V3 | Y/Y | M V1+V2+V3 | Unanimous union of failure modes |
| C-028 | L3 | M V1+V2 | M V1+V2 | M V2+V3 | M V1+V2 | M V1+V2 | M V2+V3 | Y/Y | M V1+V2 | V3 adds publication-failure checks |
| C-029 | L3 | M V1+V3 | M V1+V3 | V3 | M V1+V3 | M V1+V3 | V3 | Y/Y | M V1+V3 | Injected Budget plus per-call remaining time and byte limits |
| C-030 | L3 | M V1+V3 | M V1+V3 | V3 | M V1+V3 | M V1+V3 | V3 | Y/Y | M V1+V3 | Fold LF to space plus HTML neutralizing |
| C-031 | L2 | M V1+V3 | V1 | M V1+V3 | M V1+V3 | V1 | M V1+V3 | Y/Y | M V1+V3 | Keep ignore line; never remove `.dev/tasks/` |
| C-032 | L2 | V1 | V2 | V1 | V1 | V2 | V1 | Y/Y | V1 | Capture before step 1.2 |
| C-033 | L1 | V1 | V1=V2 | V2 | V1 | V1=V2 | V2 | Y/Y | V1=V2 | Diff-analysis records V1 and V2 as the same; unanimous in substance |
| C-034 | L2 | M V1+V3 | V2 | V3 | M V1+V3 | V2 | V3 | N/N | none | UNRESOLVED. V1: new files first plus V3's overlap check; V2: after #422 else a follow-up PR; V3: verify overlap, do not omit WC-14 |
| C-035 | L3 | M V1+V3 | V3 | V3 | M V1+V3 | V3 | V3 | Y/Y | V3 | V1's join rule is shared by all variants, so V3's version contains it |
| C-036 | L2 | V1 | V1 | M V1+V3 | V1 | V1 | M V1+V3 | Y/Y | V1 | Ten dimensions, default `unknown` |
| C-037 | L2 | M V1+V2 | V2 | M V2+V3 | M V1+V2 | V2 | M V2+V3 | Y/Y | V2 | V2 already has `rule` plus `evidence`, so V1's merge equals V2. V3 adds observation time and reason |
| C-038 | L2 | V3 | M V2+V3 | V3 | V3 | M V2+V3 | V3 | Y/Y | V3 | "Next inspection" in Sessions; V2 also wants its ledger column |
| C-039 | L3 | M V1+V2 | M V1+V2 | M V1+V3 | M V1+V2 | M V1+V2 | M V1+V3 | Y/Y | M V1+V2 | Static forbidden list plus negative `worker-read` test |
| C-040 | L3 | V3 | V3 | V3 | V3 | V3 | V3 | Y/Y | V3 | Unanimous: symlink-safe `--output`, no overlap |
| C-041 | L3 | M V2+V3 | M V2+V3 | M V2+V3 | M V2+V3 | M V2+V3 | M V2+V3 | Y/Y | M V2+V3 | Unanimous |
| C-042 | L1 | V1 | V1=V2 | V2 | V1 | V1=V2 | V2 | Y/Y | V1=V2 | Diff-analysis records V1 and V2 as the same; unanimous in substance |
| C-043 | L2 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous |
| X-001 | L3 | V1 | V1=V2 | V2 | V1 | V1=V2 | V2 | Y/Y | V1=V2 | Orca unavailable: disk-only exit 0; confirmed missing binding exit 2. Owner sign-off against Seed:63 still needed |
| X-002 | L3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | Y/Y | M V1+V3 | Unanimous. No rebuttal changed this row, although C-003 moved to M V1+V2+V3; the merge should carry the C-003 note here too |
| X-003 | L2 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | M V1+V3 | Y/Y | M V1+V3 | Unanimous: sweep recommends nothing |
| X-004 | L3 | M V1+V2 | V2 | V1 | M V1+V2 | M V1+V2 (chg) | M V1+V2 (chg) | N/Y | M V1+V2 | R1 three-way. R2 unanimous: one status template only, no `log`, `rev-parse`, `branch` or `--version` |
| X-005 | L3 | V1 | V1=V2 | V1 | V1 | V1=V2 | V1 | Y/Y | V1 | Unanimous: one status call answers GQ-101 |
| X-006 | L3 | M V1+V2 | V2 | V1 | M V1+V2 | V2 | M V1+V2 (chg) | N/Y | M V1+V2 | R1: V1's merge and V2 both block removal on archive-blocked, but V1's merge also carries V1's state set, which V2's bare V2 lacks, so counted as different. R2: V1 and V3 on M V1+V2 |
| X-007 | L3 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous |
| X-008 | L3 | V3 | V1 | V3 | V3 | V3 (chg) | V3 | Y/Y | V3 | R2 unanimous; owner memory source UNVERIFIED |
| X-009 | L2 | V1 | V1=V3 | M V1+V3 | V1 | V1=V3 | M V1+V3 | Y/Y | V1=V3 | All choose `orca-ide`; correct binary name UNVERIFIED |
| X-010 | L2 | V2 | V2 | V2 | V2 | V2 | V2 | Y/Y | V2 | Unanimous, as one isolated real-git test; V2R2 narrowed its session-wide allowance |
| X-011 | L3 | V1 | V1=V2 | V1 | V1 | V1=V2 | V1 | Y/Y | V1 | Unanimous |
| X-012 | L1 | V1 | V1 | V1 | V1 | V1 | V1 | Y/Y | V1 | Unanimous: key `class` |
| X-013 | L2 | M V1+V3 | V1 | M V1+V3 | M V1+V3 | V1 | M V1+V3 | Y/Y | M V1+V3 | Keep ignore line until reports are dealt with |
| X-014 | L2 | V3 | V2=V3 | M V2+V3 | V3 | V2=V3 | M V2+V3 | Y/Y | V2=V3 | All include the Shift Brief |
| X-015 | L2 | V3 | M V2+V3 | V3 | V3 | M V2+V3 | V3 | Y/Y | V3 | "Next inspection" per session |
| X-016 | L2 | V1 | V1=V2 | M V1+V2 | V1 | V1=V2 | M V1+V2 | Y/Y | V1=V2 | No live check in this work; unanimous in substance |
| X-017 | L1 | V1 | V1=V2 | V1 | V1 | V1=V2 | V1 | Y/Y | V1 | Unanimous: "it is never posted" pin |
| X-018 | L3 | V1 | V3 | V1 | V1 | V1 (chg) | V1 | Y/Y | V1 | V2R1 wrote "V3 (with V1)", counted as V3; V2R2 moves to V1. Guard-refused body is finished |
| X-019 | L3 | V3 | V3 | V3 | V3 | V3 | V3 | Y/Y | V3 | Unanimous |
| A-001 | L2 | A | A | A | A | A | A | Y/Y | stands | |
| A-002 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Conditions: covers only direct `_git`; A-101 open |
| A-003 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Conditions: `run-current` form and child visibility (A-102) UNVERIFIED |
| A-004 | L3 | A | Q | Q | Q (chg) | Q | Q | Y/Y | stands | R2 condition: live exited rows are could not determine with Orca's verdict in the note; stalled (proved) fixture-only |
| A-005 | L3 | A | A | A | A | A | A | Y/Y | stands | |
| A-006 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Rests on A-104 to A-106; failed join means unknown, never idle |
| A-007 | L3 | Q | A | Q | Q | A | Q | Y/Y | stands | Bounds are limits, not evidence a typical Run fits (see A-107) |
| A-008 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Condition: second-resolution uniqueness rejected; add collision suffix |
| A-009 | L2 | A | A | A | A | A | A | Y/Y | stands | Click exit 2 UNVERIFIED in V2R1 |
| A-010 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Viewer rendering (A-108) UNVERIFIED |
| A-011 | L3 | A | A | A | A | A | A | Y/Y | stands | |
| A-012 | L2 | A | A | A | A | A | A | Y/Y | stands | |
| A-013 | L1 | A | A | Q | A | A | Q | Y/Y | stands | V3: gap counts not independently verified |
| A-014 | L3 | A | A | A | A | A | A | Y/Y | stands | |
| A-015 | L3 | A | A | A | A | A | A | Y/Y | stands | |
| A-016 | L2 | A | A | Q | A | A | Q | Y/Y | stands | V3: contract rule is not enforcement |
| A-017 | L2 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Condition: one isolated real-git test allowed |
| A-101 | L3 | Q | R | Q | Q | Q (chg) | Q | Y/Y | stands | Sequential A-018. R2 condition (V2): any lock-free sentence scoped to direct `_git`; Orca indirect git a named UNVERIFIED risk |
| A-102 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Sequential A-019. If false, skill passes `--run` |
| A-103 | L3 | Q | R | Q | Q | Q (chg) | Q | Y/Y | stands | Sequential A-020. R2 condition (V2): live exited rows keep Orca's verdict in the note; stalled (proved) fixture-only until a source is captured |
| A-104 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Sequential A-021 |
| A-105 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Sequential A-022 |
| A-106 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Sequential A-023 |
| A-107 | L3 | R | Q | R | R | Q | R | Y/Y | rejected | Sequential A-024. 2 of 3 REJECT: do not assume Runs fit within 50 rows; report cap exhaustion |
| A-108 | L3 | Q | Q | Q | Q | Q | Q | Y/Y | stands | Sequential A-025 |

## 3. Summary

### 3.1 Agreed counts and convergence

| Round | S (13) | C (43) | X (19) | A (25) | Agreed | Convergence |
|---|---|---|---|---|---|---|
| After Round 1 | 13 | 37 | 17 | 25 | 92 | 0.92 |
| After Round 2 | 13 | 41 | 19 | 25 | 96 | 0.96 |

### 3.2 Agreed per level (coverage gate)

| Level | Points | Agreed after R1 | Agreed after R2 | Gate (at least 1) |
|---|---|---|---|---|
| L1 | 15 | 15 | 15 | Pass |
| L2 | 31 | 29 | 29 | Pass |
| L3 | 54 | 48 | 52 | Pass |

The coverage gate passes in both rounds.

### 3.3 Unresolved after Round 2 (4 points)

- **C-014 (L3):** three different positions. V1 wants a capture-gated cursor template; V2 wants a fixed 101-row, two-call acceptance criterion; V3 keeps its own text. No two match in substance.
- **C-017 (L2):** all three keep V1's `class` key and the additive JSON shape, but the merges differ in substance: V2 adds evidence and note fields, V3 adds ID-only waiting, zero counts and JSON written only after publication.
- **C-022 (L3):** V2 keeps "admitted" only; V1 and V3 both add "rejection recorded", but V1 alone adds a Run task-list clause, so V1 and V3 differ in substance. V1R2 prose (item 9) endorses V3's end condition, but V1 did not list C-022 as a changed row, so its R1 value stands for the count.
- **C-034 (L2):** V1 wants an ordering and overlap check; V2 wants this work after #422, otherwise a follow-up PR; V3 wants overlap verified and WC-14 kept. Three different conditions.

### 3.4 Resolved only in Round 2

C-009, C-021, X-004, X-006 (no point lost agreement between rounds).

### 3.5 Winner flips

- **C-003:** winner changed from M V1+V3 (R1) to M V1+V2+V3 (R2), after all three advocates added V2's note "Orca: exited; fenced evidence not readable" and the fixture-only label on rule 2.

Position moves that did not change the winner: C-006 (V3), C-010, C-013, C-023, X-008, X-018 (V2), C-012 (V3, now M V1+V2), A-004 (V1, ACCEPT to QUALIFY), A-101 and A-103 (V2, REJECT to QUALIFY).

### 3.6 Limits of this tally

- Agreement among advocates is not evidence. Points the advocates themselves mark UNVERIFIED stay UNVERIFIED: the Orca binary name (X-009), the owner cron order (X-008, C-023), old-git behaviour on `--no-optional-locks` (C-010), Orca indirect git and message consumption (A-101), the Run-scoped task-list form (A-102), and the live source of completion and fencing evidence (A-103).
- Owner gates sit outside the vote: WC-14 wording and the disk-only outage exception against Seed:63 (X-001, C-015).
- Equivalence calls (Method 1.2) are the clerk's reading; where a call was close, the row note says why.

## 4. Emerging consensus (for the independent fault-finder)

These are agreed winners only, L3 first, most behaviour-bearing at the top. They record what the advocates agreed, not that it is correct.

### L3

- **Classifier (C-001, X-007: V1):** one total rule table, first match wins, idle as rule 7 before the final fallback as rule 8, order pinned by rule name, with a fixture that must classify as idle.
- **Stalled and fencing (X-002, C-003; A-004, A-103 QUALIFY):** stalled (proved) needs fencing known absent; unknown fencing gives could not determine with the note "Orca: exited; fenced evidence not readable". Stalled is reachable only in synthetic fixtures in Phase 1.
- **Unknown policy (C-002):** an unreadable gate policy gives could not determine, never a guess.
- **Git seam (C-009, X-004, C-010, C-012, C-013):** the only git call is `git --no-optional-locks -C <path> status --porcelain --branch` per worktree, plus the environment variable. No `rev-parse`, `log`, `branch` or `--version`. Root by a plain path walk that accepts a `.git` file or folder. Ancestry into the feature branch stays not observed. No version gate; a failed call gives a stable reason code and unknown git evidence, never a retry without the flag.
- **GQ-101 (C-007, X-005: V1):** answered from the one status call; no base-tree comparison.
- **Orca allowlist (C-008, X-011: V1):** includes the non-ready `task-list --run` read; exact syntax UNVERIFIED.
- **Orca outage (C-015, X-001):** Orca unavailable gives a disk-only report and exit 0; a confirmed missing binding gives exit 2. Needs owner sign-off against Seed:63.
- **Package states (C-006, X-006: M V1+V2):** V1's six states including unknown and interrupted archive; archive-blocked is a named removal blocker, not "unfinished".
- **Re-run and publication (C-019, C-020, X-019: V3):** exclusive path reservation with a collision suffix; no overwrite.
- **Periodic duty (C-023, X-008: V3):** a coordinator duty in contract text only; no scheduler, no fixed cadence. Source memory UNVERIFIED.
- **Guard-refused body (X-018: V1):** an observed `guard refused:` body is finished; an unreadable contract is could not determine.
- **Tests (C-011; with X-010 and A-017, both L2):** argv structural tests, with exactly one marked, isolated real-git control test; every other test blocks subprocess calls.
- **Determinism (C-021: M V1+V3):** byte-identical report and JSON with an injected clock.
- **Other agreed L3 rows:** C-028, C-029, C-030, C-035, C-039, C-040, C-041 (see table).
- **Assumptions:** A-107 rejected (do not assume a Run fits the row cap; report exhaustion). A-101 stands only with lock-free claims scoped to the sweep's own `_git` and Orca's indirect git effects named as an UNVERIFIED risk.

### L2

- **Sweep recommends nothing (X-003, C-024: M V1+V3).**
- **Next inspection per session (C-038, X-015: V3).**
- **Report sections (C-018):** V2's order plus V3's coverage section, Shift Brief and "Report complete" footer (X-014: V2=V3).
- **No live check in this work (X-016: V1=V2).**
- **Binary name `orca-ide` (X-009: V1=V3);** correct name UNVERIFIED.
- **Module table (S-005).**

### Flag for the fault-finder

Four points have no agreed winner and need a decision: C-014, C-017, C-022, C-034 (reasons in 3.3).

## Post-Round-3 Final Convergence

- Author: debate orchestrator (no advocacy). Date: 2026-11-08.
- Inputs read for this section: `debate/round3-final-v1.md` (V1R3), `debate/round3-final-v2.md` (V2R3), `debate/round3-final-v3.md` (V3R3), `invariant-probe.md`, sections 1 to 4 above, and the protocol (SKILL = `~/.claude/skills/sc-adversarial-protocol/SKILL.md`). Every file was read in chunks of 150 lines or fewer.
- Method: the rules in section 1.2 apply unchanged. A Round 3 position replaces a Round 2 position only where a Round 3 file states it. Order of writing: V1R3 first, then V2R3 (which read V1R3), then V3R3 (which read both). Where V1R3 describes another advocate's position, the later file's own statement governs.

### P3.1 Recount over the 100 points

| Round | S (13) | C (43) | X (19) | A (25) | Agreed | Convergence |
|---|---|---|---|---|---|---|
| After Round 2 | 13 | 41 | 19 | 25 | 96 | 0.96 |
| After Round 3 | 13 | 43 | 19 | 25 | 100 | 1.00 |

| Level | Points | Agreed after R2 | Agreed after R3 | Gate (at least 1) |
|---|---|---|---|---|
| L1 | 15 | 15 | 15 | Pass |
| L2 | 31 | 29 | 31 | Pass |
| L3 | 54 | 52 | 54 | Pass |
| Overall | 100 | 96 | 100 | Pass |

No point that was agreed after Round 2 lost agreement in Round 3. Two agreed points were checked for loss and keep 2 of 3:

- X-009: V1R3:48 and V2R3:49 both now hold "`ORCA_CLI_COMMAND` if set, else `orca-ide`"; V3R3 is silent, so V3's Round 2 value (`orca-ide`) stands. The override is not in V3's text, so by rule 1.2.5 this is a 2 of 3 majority for V1's amended form, not unanimity.
- C-009 and X-004: V2R3:45 proposes `--untracked-files=normal` as a candidate, conditional on owner or design choice; V1R3:43 and V3R3:54 keep the fixed template. V2 did not change its row, so the R2 winner (M V1+V2, one fixed status template) stands.

### P3.2 Winner changes made by Round 3 that no advocate listed as a changed row

The brief named only C-014, C-017, C-022 and C-034. Round 3 also changes or amends these agreed points, and the final matrix must carry them:

- **X-001 and C-015 (L3), winner changes from V1=V2 to V3.** V1R3:22 adopts V3's original rule (V3:165-166): with no `--run`, an unavailable lookup exits 2. V2R3:24 accepts it ("V1's text at V1R3:22, unchanged, plus one added sentence"). V3R3:31 accepts it and withdraws its own Round 2 exception ("My V3R2:16 exception is withdrawn"). Unanimous. The owner sign-off against Seed:63 that section 3.6 listed is no longer needed, because the agreed rule now follows Seed:63 literally. V1R3:54 still describes V2 and V3 as holding exit 0; that description is out of date, because both later files moved.
- **C-003 and X-002 (L3), winner unchanged, text amended.** Rule 2 declines (no match) and attaches the note, instead of returning could not determine (V1R3:42, V2R3:44, V3R3:53; INV-007).
- **A-006 (L3), stands, condition amended.** `person_started` becomes `True`, `False` or `None` (V1R3:24, V2R3:26, V3R3:33; INV-003).
- **X-009 (L2), winner amended.** See P3.1.

### P3.3 The four points open after Round 2

| Point | Level | Agreed | Winner | Final text (one line) |
|---|---|---|---|---|
| C-014 | L3 | yes (3 of 3) | M V1+V2+V3 | V3's dedupe and keep-and-mark-partial rows; V1's cursor template admitted only after the step 1.0a capture; V2's 101-row AC (2 list calls) enabled only once that template exists; until then one list call per Run, and a full 100-row page sets `truncated` and prints `Orca rows: 100 shown; total is a lower bound (paging not yet captured)` (V1R3:31, V2R3:33, V3R3:42). |
| C-017 | L2 | yes (3 of 3) | M V1+V2+V3 | V1's `class` key, schema version 1 additive-only and golden key-set test; V2's per-row `rule`, `evidence`, `notes` and `safe_to_close` (never `yes` in Phase 1); V3's zero counts, ID-only `waiting` lists and success JSON printed only after publication; a failed write exits 1 with no success JSON (V1R3:32, V2R3:34, V3R3:43). |
| C-022 | L3 | yes (3 of 3) | V3 | "until every Task it created is settled and every result has been inspected and its admission or rejection recorded" (V3:324-325), plus "It never stops watching on its own." (V1R3:33, V2R3:35, V3R3:44). |
| C-034 | L2 | yes (3 of 3) | M V1+V3 | New package, command, skill and docs first; check the overlap with PR #422 before the contract edit; rebase onto #422 if it merges first; WC-14 and its pins land in this PR and are never left out of done (V1R3:34, V2R3:36, V3R3:45). |

### P3.4 HIGH invariant dispositions

| INV | Final disposition | Final merged text and its sources |
|---|---|---|
| INV-001 | RESOLVED | Merged text is V3R3:31, quoted: "Without `--run`, call `run-current`. An unavailable lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>`; a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`. Neither case writes a report or success JSON. With an explicit Run, or a binding already established by a successful lookup, a later unavailable result stops further Orca reads, retains already collected evidence, marks remaining Orca sources unscanned, adds the `Orca unavailable` banner and `orca_available: false`, and permits disk-only continuation. Exit 0 requires successful report publication; write failure exits 1 without success JSON." Parts: the two exit-2 cases, both messages and ACs (1) and (2) come from V1R3:22; the "binding already established" case and AC (3) come from V2R3:24; "retains already collected evidence" and the write-failure exit 1 come from V3R3:31. Where V1R3:22 says "every Orca source `unscanned: orca unavailable`", V3R3:31 governs for a failure after the first call. |
| INV-002 | RESOLVED | Merged text is V3R3:32, quoted in part: "Classify each `_orca` result once as `ok`, `no_binding`, `unavailable` or `call_failed`. ... Also treat nonzero exit or invalid response on the first Orca call as unavailable. Stop further Orca calls after unavailable. A later nonzero exit or invalid response without those unavailable signals is `call_failed` ... `no_binding` applies only to zero-exit `run-current` with the captured explicit no-binding shape, never to an empty body, arbitrary null or a missing field guessed to mean no binding. Those shapes remain UNVERIFIED until step 1.0a. `ok` requires the captured success shape." Parts: the unavailable causes, the stop after the first unavailable (V3:293) and the five-cause parametrized AC come from V1R3:23; the `call_failed` class, the first-call rule and the 3-row `worker-show` AC come from V2R3:25; the invalid-response definition, the shape checks and the reason `orca call failed (invalid response)` come from V3R3:32. V1R3:23 holds three classes; V2R3 and V3R3 hold four, so four classes is the 2 of 3 position. Dependency: because `ok` requires a captured shape, the step 1.0a capture is a precondition for the parser. |
| INV-003 | RESOLVED | Merged text is V3R3:33, quoted in part: "Represent `person_started` as True, False or None. A positive transcript-to-worker join makes it False. Only when every scoped Run's worker list is complete, no relevant list or join is unscanned or truncated, and the tab map is read and the join completed may an unjoined transcript be True. Otherwise it is None. None never becomes idle or Historical". Parts: the tri-state field, the rule 7 condition and the outage AC come from V1R3:24; "complete" in place of "scanned" and the truncated-page AC come from V2R3:26; the reason "worker list call failed" and the `call_failed` AC come from V3R3:33. |
| INV-005 | ACCEPTED-RISK-OWNER-SIGNOFF | Risk statement, quoted from V3R3:34: "Whether Orca read verbs take optional git locks inside worker worktrees is UNVERIFIED. If they do, the sweep can disturb a live worker despite its direct `_git` safeguards. All lock-free claims are scoped to the sweep's own `_git` calls. The report states `Orca read verbs' git effects on worker worktrees: UNVERIFIED`." Parts: the risk, the scoping of lock-free claims and the coverage line come from V1R3:25; the withdrawal of V2's unscoped sentences at V2:228 and V2:245 comes from V2R3:27 (also V1R3:57); "absent sign-off, the risk remains a blocker" comes from V3R3:34. V2R3:27 also asks that `_orca` pass `GIT_OPTIONAL_LOCKS=0` with an AC. V3R3:34 rejects that requirement and V1R3:25 does not propose it, so it is a candidate mitigation only, not part of the merged text. No owner sign-off is recorded in any file. |

Literal gate reading. The gate filters "Status == UNADDRESSED AND Severity == HIGH" (SKILL:1466). An accepted risk is not ADDRESSED: the probe defines no accepted-risk status, and no rule converts an acknowledgement into ADDRESSED. INV-005 therefore stays in `unaddressed_invariants`.

- `unaddressed_invariants` (HIGH): INV-005.
- count(HIGH + UNADDRESSED) = 1.

### P3.5 Status decision

**Status: BLOCKED_BY_INVARIANTS.**

The protocol lines this rests on:

- SKILL:1419: "convergence requires: (all_levels_covered == true) AND (score >= threshold) AND (no_high_unaddressed_invariants == true)"
- SKILL:1467-1468: "If count(HIGH + UNADDRESSED) > 0: a. Block convergence regardless of diff-point agreement score"
- SKILL:1473: "convergence requires: count(HIGH + UNADDRESSED invariants) == 0"
- SKILL:1478: "Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk."
- SKILL:1498: CONVERGED is "Agreement ≥ threshold AND all taxonomy levels covered AND no HIGH unaddressed invariants"
- SKILL:1501: BLOCKED_BY_INVARIANTS is "Agreement ≥ threshold AND taxonomy covered BUT HIGH-severity UNADDRESSED invariants exist"
- SKILL:1380-1382: post_round_3 "convergence_check: Final convergence measurement" and "if_not_converged: Proceed with non-convergence → force-select by score (per FR-006)"

Reasoning:

1. Agreement is 1.00, at or above the 0.75 threshold, and all three levels are covered, so the first two terms of SKILL:1419 hold.
2. One HIGH invariant is UNADDRESSED (INV-005), so the third term fails.
3. SKILL:1478 names acknowledgement as an action the flagged item may receive, but neither the gate (SKILL:1466, 1473) nor the CONVERGED definition (SKILL:1498) lets an acknowledged item count as addressed. The protocol therefore does not allow convergence on acknowledgement.
4. Even if it did, the acknowledgement would have to be the owner's (V1R3:25, V2R3:27, V3R3:34). Advocate agreement is not owner sign-off, and no file records one.
5. Round 3 was the last round at `--depth deep`, so no further debate round can address INV-005. Per SKILL:1382, the pipeline proceeds without convergence and the base is force-selected by score (FR-006). INV-005 is carried forward as an unresolved conflict for the return contract.

Process note: SKILL:1365 runs Round 3 only when "convergence < configured_threshold after Round 2", and SKILL:1368 skips it when "convergence ≥ threshold". Round 2 scored 0.96, so a literal reading skips Round 3. It was run to address the invariant block, which SKILL:1478 supports ("Address the flagged items in a subsequent debate round"). This is recorded as a deviation from the round_3_conditional rule.

### P3.6 MEDIUM warnings (do not block, SKILL:1470-1471)

The probe listed nine MEDIUM items as UNADDRESSED. Round 3 gives agreed text for six of them: INV-004 (lower-bound coverage line, V1R3:40, V2R3:42, V3R3:51), INV-006 (`worker_done_seen` is None on live rows, never stalled, V1R3:41, V2R3:43, V3R3:52), INV-007 (rule 2 declines, V1R3:42, V2R3:44, V3R3:53), INV-009 (lower-bound note plus the INV-003 guard, V3R3:55), INV-012 (C-022) and INV-013 (C-034). Three remain warnings:

```
WARNING: 3 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-008, INV-011, INV-017
These items do not block convergence but should be reviewed.
```

- **INV-008:** the gap is disclosed, not closed. V1R3:43 and V3R3:54 keep the fixed status template and name `status.showUntrackedFiles=no` as a report limitation; V2R3:45's `--untracked-files=normal` is UNVERIFIED and not agreed.
- **INV-011:** all three add the pin phrase "it never stops watching on its own" (V1R3:45, V2R3:47, V3R3:56). The probe's other half, a coordinator that sweeps rarely, is not answered, because no cadence is required. V3R3:56 states it did not check the owner-memory file.
- **INV-017:** V1R3:48 and V2R3:49 agree on `ORCA_CLI_COMMAND` if set, else `orca-ide`. V3R3 takes no position. Whether the sweep's environment carries `ORCA_CLI_COMMAND` is UNVERIFIED (V1R3:48). Inside an Orca-managed terminal the orca-cli skill selects bare `orca` (SKILL.md:27), so a missing `orca-ide` there makes every sweep take the outage path; the failure is now visible (`binary not found: orca-ide`, V2R3:49) but not prevented.

LOW items: no action (SKILL:1472). INV-010 and INV-015 are answered by V1R3:49-50 and V2R3:50-51; INV-014 by C-017; INV-016 is named as an owner cost at V2R3:24.

### P3.7 Errors found in the advocates' Round 3 files

1. Seed path: V1R3:6, V2R3:6 and V3R3:27 cite the seed as `../../seed-brief.md`. From `debate/` that resolves to `adversarial/seed-brief.md`, which does not exist; the correct path from `debate/` is `../../../seed-brief.md`. Line citations into the seed are unaffected.
2. Orca binary: V1R3:48 cites orca-cli SKILL.md:21-26 for "never bare `orca`". SKILL.md:27 selects bare `orca` inside Orca-managed terminals. V2R3:49 corrects this and calls V1's rule a deliberate safety deviation.
3. INV-007 test: V1R3:42's AC uses "an exited row with a `blocked` contract". A blocked contract is matched by rule 1 (V1:147), which runs before rule 2, so the test passes whether rule 2 declines or returns. A rule 4 or rule 6 case (for example an exited row with a `guard refused:` body that must classify as finished) would test the decline.
4. INV-001 reasoning: V1R3:22 argues from INV-004, which applies with `--run` as well (V2R3:24). The requirement text is unaffected.
5. Stale description: V1R3:54 says V2 and V3R2 hold exit 0; both later files moved to exit 2 (V2R3:24, V3R3:31).
6. Unlisted winner changes: no advocate lists X-001 or C-015 as changed, but Round 3 reverses both (P3.2).
7. Omissions: V3R3 states no position on INV-017, INV-010 or INV-015.

### P3.8 Final score

- Diff-point convergence: 100 of 100 = 1.00 (threshold 0.75).
- Taxonomy: L1 15/15, L2 31/31, L3 54/54.
- Invariant gate: 1 HIGH UNADDRESSED (INV-005, accepted risk awaiting owner sign-off); 3 MEDIUM warnings.
- Status: BLOCKED_BY_INVARIANTS; proceed to force-select by score (SKILL:1382, FR-006).

