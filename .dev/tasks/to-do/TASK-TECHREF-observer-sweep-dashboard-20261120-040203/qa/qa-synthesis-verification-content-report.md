# QA Report - Gate 2 Synthesis Fix Verification (content, qualitative)

**Topic:** Observer / sweep / dashboard technical reference, synthesis files after Gate 2 fix cycle 1
**Date:** 2026-11-20
**Phase:** fix-cycle (tech-ref-qualitative lens, report-only; fix_authorization: false)
**Fix cycle:** 1 (verification review 2 of max 3)
**Status:** Complete

---

## Scope and method

Inputs read in full: consolidated findings (`qa-synthesis-consolidated-findings.md`), fix log (`qa-synthesis-fix-log-c1.md`), and all seven synthesis files (`synth-01` to `synth-07`, current state, `wc -l` = 104 / 136 / 250 / 243 / 211 / 234 / 322 = 1,500). Pre-fix copies in `/tmp/*.before-gs5` were used only to see what the cuts removed. Code facts re-checked against the read-only snapshot `/home/coder/.cache/ic-snap-20261120/master` and, for origin-only files, `git show origin/master:`. Fix authorization: false; no synthesis file was changed. No Inherited Structural Verdict block was in the spawn prompt, so this review ran standalone.

## Part 1. Resolution of the seven blocking findings

| ID | Result | Evidence read (current text and source) |
|---|---|---|
| GS-1 (Draft7Validator in `test_export.py`) | RESOLVED | synth-03 line 119 now names `test_commands.py` and `test_snapshot_schema.py` with "shared validator set up in `conftest.py:17, 32`". Grep of `tests/observe` for `Draft7`: `conftest.py:17` import, `:32` `check_schema`, `test_commands.py:17,44`, `test_snapshot_schema.py:10,25,60`; no hit in `test_export.py`. Claim is exact. |
| GS-2 (UNVERIFIED items missing from 14.4 B; #590 tagging) | RESOLVED | synth-07 14.4 B now holds: error-code names `consumer_fenced` / `no_active_terminal` (line 215, U-02 row), `orchestrator-poll` `*/5 * * * *`, `IronbellyOrg/IronOrchestrator`, `waker.py` triggers (line 219), and a new row for "three Orca wrappers not stated" plus the #590 recorded result (line 221). #590 figures are tagged consistently: synth-01:88 `[UNVERIFIED]`, synth-06:180 and :206 "recorded, not re-run [UNVERIFIED]", synth-07:136 and :221. The three cited code lines of the new row are right (`adapter.py:224` `production_runner`, `probes.py:214` `orca_binary`, `orca_term.py:17-21` bare `orca`). Two small leftovers are in Part 4 (minor). |
| GS-3 (false "two places" claim) | RESOLVED | synth-07 line 71 now says `classify_all` tests `idle` and `person_active` once at `classify.py:958`. Read `classify.py:958` = `if cls.rule in ("idle", "person_active"):`, `:960` = `if forced:`. Exact. |
| GS-4 (`report-entry` "callers") | RESOLVED | synth-07 14.5 closing paragraph: verb "named in `check.py:77` (docstring) and `common.py:136` (comment) and called only by `settle.sh:1037-1042`". Grep of `src`: `check.py:77` docstring, `common.py:136` comment, `settle.sh:1037` probe, `:1042` call. The touch-point row that carried the same wording was deleted under GS-5, so no second copy remains. synth-05:94/:123 and synth-06:85 say the same (settle.sh is the consumer). |
| GS-5 (line budget) | QUALITATIVE PART RESOLVED; NUMERIC TARGET NOT MET | See Part 3. |
| GS-6 (C8 carry lines in synth-01) | RESOLVED | synth-01 line 103 now gives per-item lines: stalled and fenced 493, 636, 841, 877; `agent_wait_since` 493, 494, 649, 1003; `Safe to close` 794; `Removable` 795. Read `docs/designs/orchestrator-mode.md` in the snapshot: 636 "Stalled and fenced are not observed in Phase 1", 841 (D7), 877 (SP-24), 493 (Rule 5 / `agent_wait`), 494 (waiting timestamp / unknown age), 649 (unknown-age ordering), 1003 (item 6 `agentWait`), 794 (FR-012 `safe_to_close`), 795 (FR-013 `removable`). Matches synth-07 C8-1..C8-5 and synth-04 lines 84-88. |
| GS-7 (R1 glossary) | RESOLVED | synth-07 line 298 now: "R1 live worker-list ledger, `--once` and snapshot (it records the redacted golden samples)". `release-gates.md` (origin/master) row R1 is "Live worker-list ... the JSON snapshot export" and the R0 row says the redacted sample is recorded by R1. Agrees with synth-01:70 and synth-03:204. |

## Part 2. Cross-file consistency of values touched by the fixes

| # | Value | Result | Evidence |
|---|---|---|---|
| X1 | Counts (31 row keys read, 20 exported, 11 dropped; 9 rules, 8 classes; 12 report sections; 10 Orca templates and 7 verbs; 3 observer argv shapes and 13 forbidden prefixes; 19 observer fixtures; 16 AWR scripts, 15 steps; 360 exports / 180 per batch) | Consistent | Same numbers in synth-01 2.5, synth-02 3, synth-03 5.1, synth-04 5.3/5.4, synth-06 8.1/11, synth-07 12-14. Observer line total 6,011 re-added from the per-file counts in synth-01/03 (512+835+361+142+274+524+1300+1461+235+192+126+48+1 init) = 6,011. |
| X2 | Caps and budgets (5 calls, 10 s, 8 MiB, 15 s, 45 s STALE, 1,000 retained, 100 window; sweep 50 / 90 s / 10 s, 256 KiB, 1 MiB) | Consistent | synth-01 2.5, synth-03 5.1 limits table, synth-04 budgets, synth-06 11.2, synth-07 12.2 and 14.1 agree. |
| X3 | Verbs, class names, labels (`stalled (proved)`, `fenced`, `working`, ..., `could not determine`; KNOWN LIMIT / DEFECT-CANDIDATE) | Consistent | `models.CLASSES` list in synth-01, synth-04 and synth-07 12.2 match. Labels: C8-1..C8-7 KNOWN LIMIT, C8-8 and C8-9 DEFECT-CANDIDATE in synth-01:103-104, synth-03:223, synth-05:99/190, synth-07 14.1 and 14.5. |
| X4 | Paths and line cites touched by fixes (`orchestrator-mode.md` carry lines; `classify.py:958`; `settle.sh:1037-1042`; `conftest.py:17, 32`; `main.py:590-592`, `581-583`) | Consistent and correct | Re-read in source (Part 1). synth-04 cites a subset of the carry lines (fenced 493/841; `agent_wait_since` omits 649), which is a subset, not a conflict. |

## Part 3. GS-5 (line budget): harm and protected parts

Numbers. Total 1,644 to 1,500 lines (`wc -l` re-run: 104, 136, 250, 243, 211, 234, 322). The about-1,300 target is missed by 200 lines. The Standard ceiling of 1,200 named in the original finding is missed by 300. The fix log says this plainly and lists what a further cut would remove (all unique rows, about 125 lines named, none applied).

Protected parts, all intact in the current text:
- Section 2.5 comparison matrix: synth-01 lines 83-99 (four subject rows, overlap table, C8 pointers).
- 8.1 Orca verb inventory: synth-06 lines 36-73 (per-tool table and verb-family table, counts line).
- 14.4 contradictions list: synth-07 lines 181-222 (A grouped by subject, B UNVERIFIED, C open gaps), with SD/CC rows unchanged.
- Five 13.1 scenarios A to E: synth-07 lines 71-75, plus skeletons.
- DEFECT-CANDIDATE rows: C8-8 and C8-9 at synth-07 lines 257-258, both ending "Remediation task not created (read-only brief); flagged for the owner". The same words are on C8-1, C8-2, C8-3, C8-6 (KNOWN LIMIT), and in synth-01:101, synth-03:223, synth-04:84-88, synth-05:99/190. No DEFECT-CANDIDATE was relabelled as a plain known gap; no plain gap was promoted.

Harm check on the cuts. I compared the cut text in the `/tmp/*.before-gs5` copies with where the facts now sit. Replacement pointers resolve (synth-02 4.1 (c)/(d) point to 5.5/5.6, which hold the diagrams; synth-05's issue-409 contradictions pointer goes to 14.4 A SD-21 to SD-29 and 14.3; 13.1 intro points to 2.5, 8.1, 8.2; 15.2 step 2 points to the Section 5 Public Interface blocks). A grep for the removed headings ("Entry points", "Replacement wording", "Superseded labels", "Source conflicts and corrections", "Public wording (GF-2)", "Overlap facts (GF-3)", "Consumers of `.dev/sweeps`") finds no surviving reference to any of them. One unique fact was lost although the fix log says duplicates only: the removed 13.1 WC-16 touch-point row said the orchestrator design states everything else in the contract is unchanged (DESIGN:135). No other section carries that sentence (`DESIGN:135` now appears only in 14.4 A SD-30 to SD-35 as a stale WC-9 cite). It is peripheral to the facts-only brief, so I grade it minor. I found no other loss and no change of meaning.

GS-5 call. The cuts did not harm meaning and the protected parts are intact, so the qualitative part is resolved. The numeric target is not met and no further duplicate-only cuts remain per the fix log. Whether to accept 1,500 lines or to cut unique rows is a scope call for the executor or the owner; I do not count it as a blocking content defect (no false claim, no missing deliverable, no wrong behaviour), and I report it as an open numeric item, not as passed.

## Part 4. New defects scan (adversarial)

| # | Check | Result | Evidence |
|---|---|---|---|
| N1 | New contradiction introduced by the fixes | None found | Counts, caps, verbs and cites cross-checked above; GS-3, GS-4, GS-6, GS-7 edits agree with every other file that mentions the same fact. |
| N2 | Designed-only item described as built | None found | Orchestrator, `report-entry`, `/sc:orchestrator`, PR B stay "designed / absent" in synth-01:20, synth-02:110-113, synth-05:88-97, synth-06:58, synth-07 glossary and 14.1. Phase 2 `/sc:close` appears only as a named later phase (synth-07:134, :171). Observer R2/R3 are described as built, matching `commands.py:67, 70`. |
| N3 | Mislabelled C8 candidate or lost remediation wording | None introduced | Pre-fix C8-4, C8-5, C8-7 rows already ended only "Flagged for the owner" (`/tmp/synth-07.before-gs5` lines 272, 273, 275); unchanged. 14.1 rows for D-1 and C8-8 are word-for-word as before. See minor note m3. |
| N4 | Unification recommendation | None | Grep for recommend/should-unify/better-to/consolidate phrasing finds only the "no unification" disclaimers (header lines of synth-01..07, glossary, appendix) and the title "Unification touch points (facts only; no recommendation)". C8-9 holds one owner question, labelled "fact, not a recommendation". |
| N5 | Dangling references created by the cuts | None blocking | Pointer targets all exist (Part 3). The `DC-01` / `DC-02` ids in synth-02:120 and synth-06:3, :184 have no printed mapping to C8-8 / C8-9, but the removed "Superseded labels" line never carried that mapping either (`/tmp/synth-07.before-gs5:279`), so this is not new (minor m4). |

Open blocking findings: 0 content defects. Open numeric item: GS-5 line total, 1,500 against about 1,300 (and against the 1,200 ceiling).

### Minor findings (notes only; not rechecked)

- m1. synth-07 line 221 (14.4 B new row) cites "synth-01 Section 2.5" for "reason for three Orca wrappers not stated"; the tagged sentence is in synth-01 Section 2.3 (line 69).
- m2. The error-code names `consumer_fenced` / `no_active_terminal` are tagged UNVERIFIED in 14.4 B and synth-06:166, but appear untagged in synth-02:119, synth-03:84 and synth-07:104.
- m3. synth-07 14.5 rows C8-4, C8-5 and C8-7 print only "Flagged for the owner." while R-C8 rule 4 (line 244) and synth-04:87-88 use the full words for Safe to close and Removable. Present before the fix.
- m4. `DC-01` / `DC-02`, C8-8 / C8-9 and D-1 are three handles for two DEFECT-CANDIDATEs with no crosswalk; synth-06:3 omits `Safe to close` / `Removable` from its KNOWN LIMIT list.
- m5. synth-07:259 says the `report-entry` call "ends `ENTRY escalated why=surface_absent`"; in `settle.sh:1038` the line printed on probe failure is `ENTRY escalated key=%s why=surface_absent` (synth-05:94 has the key).
- m6. synth-01 line 7 says "Four subjects" then lists five items (three live, two designed); the lost DESIGN:135 sentence (Part 3).

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. The spawn prompt carried no `## Inherited Structural Verdict`; I ran standalone and re-checked structure-adjacent facts (line counts, pointers, headings) myself.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- GS-1 claim re-derived from source: grep `Draft7` in `tests/observe` (conftest.py:17, 32; test_commands.py:17, 44; test_snapshot_schema.py:10, 25, 60; none in test_export.py).
- GS-3 claim re-derived: Read `classify.py:950-965` (`:958` one tuple test, `:960` `if forced:`).
- GS-4 claim re-derived: grep of `src` for `report-entry` / `surface_absent` (check.py:77, common.py:136, run.py:688, settle.sh:1037, 1038, 1042).
- GS-6 and GS-7 re-derived: `sed` of nine lines of `orchestrator-mode.md` in the snapshot and `git show origin/master:` of `release-gates.md` R0-R4 rows.
- New 14.4 B row cites re-read: `adapter.py:222-226`, `probes.py:212-217`, `orca_term.py:14-22`.
- GS-5 harm check: diffed removed text in `/tmp/synth-07.before-gs5` against current sections (found the DESIGN:135 loss; found C8-4/5/7 wording unchanged since before the fix).
- Facts a reader would accept without these checks: the fix log's statements that the C8 wording was kept and that cuts were duplicates only; the second was not fully true (one unique sentence lost).

## Confidence Gate

- Checklist items: 7 findings (GS-1..GS-7) + 4 cross-file value checks (X1..X4) + 5 new-defect checks (N1..N5) = 16.
- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (GS-5 verified as to harm and protected parts; its numeric target is verified as NOT met and is reported as open).
- **Tool engagement:** Read: 13 | Grep: 18 | Glob: 2 | Bash: 4 (this exceeds 16, so the minimum is met).
- Limits: nothing was run; code claims are checked by reading the snapshot; claims I did not re-derive (for example the 1,978-line test counts and research-file cites) were checked only for cross-file agreement.

## Summary
- Checks passed: 16 / 16 (GS-5 passes on harm and protected parts; its numeric target is open)
- Checks failed: 0
- Critical issues: 0
- Open blocking findings: 0 (content). Open numeric item: GS-5, 1,500 vs about 1,300 lines.
- Minor notes: 6 (m1 to m6)

## Overall Verdict: PASS (with notes; GS-5 numeric target not met)

## Recommendations
- Proceed to Gate 3 with the six minor notes carried as notes.
- Executor or owner decision on GS-5: accept 1,500 lines, or order a further cut of unique rows (fix log names about 125 lines of candidates; each loses a fact held in one place only).

## QA Complete
