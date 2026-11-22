# QA Report - Synthesis Coherence (Partition A)

**Topic:** Observer, sweep and dashboard family technical reference
**Phase:** doc-qualitative (synthesis-coherence lens), partition A (synth-01..synth-04)
**Fix cycle:** N/A (review 1)
**Status:** Complete
**Date:** 2026-11-20
**Reviewer:** rf-qa-qualitative (fix authorization: false; no synthesis file modified)
**Assigned files (partition A):** synth-01-overview-architecture.md, synth-02-directory-dataflow.md, synth-03-subsystem-observer.md, synth-04-subsystem-sweep.md (all in `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/synthesis/`). Read for cross-checks only: synth-05, synth-06, synth-07, research/gapfill-c1-GF1-c8-reconciliation.md, gaps-and-questions.md.
**Code basis for spot checks:** `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6) and the checkout design package.
**Inherited structural verdict:** none supplied in the prompt; standalone behaviour applied.
**Drift axis:** not applicable (this is a synthesis-coherence review, not task-qualitative).

---

## Checks (one table per check)

### Check 1 - Cross-file consistency of repeated facts

| Fact | Locations compared | Result |
|---|---|---|
| Line counts, observer (6,011 + 158), sweep (3,759), AWR (5,777 + 194), orchestrator.md (1,412), design renderer (1,011) | synth-01 s1 table and s2.2; synth-05 s5.5 and s5.6 | Match each other and `wc -l` on the snapshot (observe 6011; sweep 3759; AWR scripts 5777, SKILL.md 194; orchestrator.md 1412; render 130 + fixtures 122 + canvas 122 + layouts 637 = 1011) |
| Test counts (observer 26 files / 565 defs; sweep 7 files / 323 defs; test_sweep_command 28; AWR 142; tests/observe 36 entries) | synth-01 s1, synth-04 s5.4, synth-06 s11.1 | Match Grep counts on the snapshot (565 / 323 / 28 / 142; `ls tests/observe` = 36) |
| Caps and intervals (5 calls, 10 s, 8 MiB, 2 KiB, 15 s, 60 s backoff, STALE 45 s, 1,000 / 100 questions; sweep 50 / 90 s / 10 s) | synth-01 s2.3, synth-02 s4, synth-03 s5.1, synth-04 s5.4 | Identical everywhere |
| 13 forbidden prefixes, 3 observer argv shapes, 10 sweep templates (6 called, 4 pinned), 7 verbs, 4 git shapes | synth-01, 02, 03, 04 | Identical; the 13 names in synth-03 count to 13 |
| Gate constants `commands.py:67, 70`; registration `main.py:581-583`, `590-592`; `.gitignore:255-256`; `JOIN_PATH`, `CHECKED_ORCA_VERSION`, `JSON_SCHEMA_VERSION` | synth-01..04 | All verified by Grep on the snapshot |
| WC-16 `WORKER-CONTRACT.md:287-289`, never-as-worker `:23`, "Nothing starts it automatically" `sweep.md:22` | synth-01, 02, 04 | Identical; WC-16 header and never-as-worker line read on the snapshot |
| C8 carry lines in the design for the five sweep limits | synth-01 line 115 versus synth-04 lines 84-88 and GF-1 | **MISMATCH, see finding F-1** |
| "9 of 9 fixture names" (synth-01 line 100) versus "all 9 variant names plus base" (synth-05) and "all ten" (synth-06, synth-07) | synth-01, 05, 06, 07 | Denominator differs (9 versus 10), see minor note N-2 |
| Sanitizer line range for the sweep (`report.py:569-599` synth-01; `569-605` synth-02) | synth-01, synth-02 | Same function, different end line (function versus function plus `cell`); minor note N-6 |
| Observer release stage R1 | synth-01 line 75 and synth-03 (R1 = live worker ledger) versus synth-07 glossary line 318 (R1 = golden worker-list samples); `release-gates.md` row R1 on origin/master reads "Live worker-list" | **MISMATCH, see finding F-2 (location is in synth-07, outside partition A)** |

Verdict for check 1: FAIL (F-1, F-2).

### Check 2 - "Family at a glance" matrix and overlaps table versus subsystem detail

| Matrix or overlap cell | Compared with | Result |
|---|---|---|
| Observer row: sources (3 argv shapes, 5 + 1 calls), outputs (20 of 31 attributes, 0600, 15 s replace, no question text), consumers (tests only), live status (R0-R3, D-1) | synth-03 s5.1 and s5.2; synth-02 s4.1(a), s4.3 | Agree. 31 - 11 dropped = 20 is internally consistent (7 `resource.*` + 2 `workspace.*` + 2 `stage.*`) |
| Sweep row: 6 templates called, git, disk, 12 sections, JSON 12 keys, exit 0/1/2, C8 items | synth-04 s5.3, s5.4; synth-06 s8, s10 | Agree. The "6 of 8 classes can print on live data" wording is looser than synth-04 (idle and person session need `person_started True`, never seen live): note N-4 |
| AWR row: 16 scripts, 15 steps, gate 7 checks plus sha256 chain, writer designed only, `orchestrator_repo` fails on master | synth-05 s5.5; synth-02 s4.1(c) | Agree |
| Dashboard row: 180 exports per batch, 19 scenarios x 10 x 3, QA.md FAIL, 3 of 20 designs | synth-05 s5.6; synth-02 s4.1(d) | Agree |
| Overlap rows: status vocabularies (8 / 6 / FR-9 8 / S0-S11), "waits on a person" (3 meanings), joins, sanitizers (4), Orca binary, verbs (4 of about 30 match the sweep, none match the observer) | synth-03, synth-04, synth-05, synth-07 s12.2 and s13.1 | Agree. The join description matches `classify.py:667-682` read in the snapshot (path A `session_join == sid`; path B keys from tab-map file name and terminal handle) |

Verdict for check 2: PASS.

### Check 3 - Architecture and data-flow diagrams versus subsystem sections

| Diagram element | Result |
|---|---|
| synth-01 s2.1 observer chain (adapter, parse, collector, view, render / export) versus synth-02 s4.1(a) and synth-03 | Same components, same [live] label |
| Sweep chain (probes, classify, report, one write) versus synth-02 s4.1(b), synth-04 | Same. The synth-01 diagram source box omits `run-current` (listed in the matrix, synth-02 and synth-04); omission, not contradiction (note N-5) |
| AWR chain and "entry files: reader built, no writer on master" versus synth-02 s4.1(c), synth-05 | Same |
| ORCHESTRATOR [DESIGNED] box, "bound by WC-16? [UNVERIFIED]" versus synth-02 s4.1(e), synth-04 overlap facts | Same |
| Design package [prototype] box versus synth-02 s4.1(d), synth-05 | Same |

Verdict for check 3: PASS.

### Check 4 - Live versus designed accuracy

| Item | Evidence | Result |
|---|---|---|
| Observer R2 and R3 live | `commands.py:67, 70` both True (Grep); synth-03 PR table (#577, #592) | Correctly described as built |
| Fixture replay of the question ledger | `commands.py:183-188` returns exit 2 for `--questions` with `--fixture`; `collector.py:129` returns FAILED `no-question-fixture` (Grep) | Correctly described as refused (D-1) |
| Sweep `stalled (proved)`, `fenced`, `agent_wait_since` | Grep over `src/superclaude`: `worker_done_seen`, `fenced_evidence`, `agent_wait_since` appear only as defaults, readers and comments; no producer | Correctly described as unable to fire on live rows |
| Sweep `working` | Reported as produced since 2026-11-16 in synth-01, 04, 07; stale CHANGELOG line flagged | Consistent |
| Living-report writer, orchestrator, `superclaude orchestrator report-entry` | Labelled designed-only in synth-01, 02, 05 | Consistent; no designed item described as built |
| Package | "not a production integration"; no code reuse | Consistent |
| Opening paragraph count | synth-01 line 7 says "Four subjects" but then "Three are live" plus "Two are designed only" (five), and the s1 table has five rows | Wording only; note N-1 |

Verdict for check 4: PASS.

### Check 5 - Neutrality

Grep of synth-01..04 for recommend / should / better / unif / consolidat / absorb / prefer / ideal / best returned only disclaimers ("no unification recommended", "recommends nothing" as a description of the sweep report, "duplicate Dispatch ids"). Overlap and unification-touch-point text is stated as facts and undecided proposals (live issue 409 alignment item 1). No value judgment about which tool should absorb which was found.

Verdict for check 5: PASS.

### Check 6 - C8 treatment

Authority read: `research/gapfill-c1-GF1-c8-reconciliation.md` (rule R-C8, items 3.1-3.8) and synth-07 s14.5 (table C8-1 to C8-9).

| Candidate | Label in synth-01 / 02 / 03 / 04 | Label in GF-1 and synth-07 | Result |
|---|---|---|---|
| `stalled (proved)` (C8-1) | KNOWN LIMIT (cited), SPEC:231-232 (synth-01 s2.5, s2.5 pointers; synth-02 s4.1(b); synth-04 s5.3 table) | KNOWN LIMIT (cited) | Same label, same SPEC lines |
| `fenced` (C8-2) | KNOWN LIMIT (cited), SPEC:251 | KNOWN LIMIT (cited) | Same |
| `agent_wait_since` (C8-3) | KNOWN LIMIT (cited), SPEC:238 | KNOWN LIMIT (cited); DESIGN:493, 494, 649, 1003 | Label same; design carry lines wrong in synth-01 (F-1) |
| `Safe to close` (C8-4), `Removable` (C8-5) | KNOWN LIMIT, SPEC:106, 274, 338 | KNOWN LIMIT (cited); DESIGN:794 and 795 | Label same; design carry lines wrong in synth-01 (F-1) |
| Living-report writer (C8-6) | KNOWN LIMIT sequenced to PR B (synth-01 matrix and pointers; synth-02 s4.1(c)) | KNOWN LIMIT (cited), sequenced to PR B | Same. synth-01 cites ORCH lines `3, 510, 791, 1020, 1041`; synth-02 omits 1021 and 1041 (subset lists, minor N-3) |
| `orchestrator_repo` (C8-7) | KNOWN LIMIT sequenced to PR A (synth-01 pointers; synth-02 line 54); synth-01 matrix shows it only as CC-02 fact | KNOWN LIMIT (cited), sequenced to PR A | Same |
| `prefs.py answer ... <session url>` (C8-8 = DC-01) | DEFECT-CANDIDATE (synth-01 pointers); no ID | DEFECT-CANDIDATE | Same label |
| D-1 fixture replay (C8-9 = DC-02) | DEFECT-CANDIDATE with no cited scope decision (synth-01, synth-02 s4.1(a) as "D-1 / C8-9", synth-03 s5.2 "D-1") | DEFECT-CANDIDATE | Same label and same reason (only text found records an absence, `acceptance-tests.md:25`) |

No candidate is relabelled a plain "known gap" without a citation: every KNOWN LIMIT in synth-01..04 prints SPEC or design line numbers. The pointer to "Section 14" is present in synth-01 (line 113, "details in Section 14; GF-1 is the authority") but absent from synth-03 and synth-04, which cite GF-1 or inline text only (note N-3). The same two DEFECT-CANDIDATEs carry three different ids across the synthesis (D-1 in synth-01..05, C8-9 in synth-02 and synth-07 s14.5, DC-02 in synth-02 line 139 and synth-06) with no crosswalk printed in any synth file (note N-3); the register `gaps-and-questions.md` lines 100-101 and 262 do define DC-01 = C8-8 and DC-02 = C8-9.

Verdict for check 6: FAIL only because of F-1 (wrong design carry lines attached to three C8 labels). Labels themselves agree everywhere.

### Check 7 - Single source of truth (no drift in repeated information)

| Repeated information | Where repeated | Drift found |
|---|---|---|
| Observer argv templates, caps and error codes | synth-01 s2.3, synth-02 s4.3, synth-03 s5.1, synth-06 s10.1 | None |
| Sweep allowlist, budgets, exit codes, JSON keys, 12 sections | synth-01 s2.3, s2.5, synth-02, synth-04, synth-06 | None |
| WC-16 text and "no code enforces it" | synth-01 s2.1, synth-02 s4.1(b), synth-04 s5.4, synth-07 s13.1 | None |
| Design package pipeline and counts | synth-01, synth-02 s4.1(d), synth-05 s5.6 | None apart from the 9 versus 10 name denominator (N-2) |
| C8 design carry lines | synth-01 line 115 versus synth-04 table | Drift: F-1 |
| Observer stage definitions R0-R3 | synth-01, synth-03 versus synth-07 glossary | Drift: F-2 |
| Overlap facts (4 of about 30 verb forms) | synth-01, 04, 05, 06, 07 | None |

Verdict for check 7: FAIL (F-1, F-2).

### Check 8 - Key numbers stated once in Section 1 and agreeing wherever repeated

Every number in the synth-01 s1 table was re-counted against the snapshot or the checkout (see check 1 and the evidence list below): 13 observer `.py` files (wc lists 13 including `__init__.py`), 6,011 + 158 lines, 20 fixture entries / 19 JSON, 26 test files / 565 defs, sweep 6 `.py` / 3,759 lines / 7 test files / 323 defs / 28 drift guards, AWR 16 scripts / 7 templates / 5,777 + 194 lines / 142 defs, package 412 files of which 6 `.pyc` (406 tracked), 130 + 122 + 122 + 637 = 1,011 renderer lines, orchestrator.md 1,412 lines. All agree with the repeated values in synth-02 to synth-06. One presentation point: the design-package merge-record cell says "(545 files)" for PR #503, which is the whole PR, not the package (note N-7).

Verdict for check 8: PASS.

### Check 9 - Reads as one document for the owner

The owner's list is covered: data sources (s2.5 matrix, s4.2), output formats (s2.5, s4.1, s4.3, synth-03/04), what is live (matrix "Live vs designed", s5 built-versus-designed tables), who consumes the output (matrix, s5.1 to s5.5 Consumers tables), overlaps in purpose (s2.5 overlaps table), relation to WC-16 (s2.1, s5.4 WC-16 table, s4.1(b) and (e)). Cross-section pointers resolve (s2.2 rows 5.1 to 5.6 map to synth-03, 04, 05; "pointer in 2.5" for D-1 exists; "Section 13" and "Section 14" exist in synth-07). Presentation problems that the assembler must handle, all minor: synth-02 to synth-04 start with provenance preambles and use research-internal handles ("R01 s12", "GF1 section 4", "GF4 5.3", "file 04's 1478", "M-4") that an owner cannot resolve from the final document (the Appendix maps research files by "Research 01" and "GF-1", not by "R01" or "file 04"); synth-04 line 3 says "no source was re-read except wc -l counts" (a process note, not reference content). See note N-8.

Verdict for check 9: PASS with notes.

---

## Issues Found

| # | Severity | Blocking? | Location | Issue | Required Fix |
|---|---|---|---|---|---|
| F-1 | IMPORTANT | Yes | synth-01 line 115 (s2.5 "C8 pointers", first bullet) versus synth-04 lines 84-88, GF-1 sections 3.3-3.5, synth-07 s14.5 rows C8-3 to C8-5 | The bullet says `stalled`, `fenced`, `agent_wait_since`, `Safe to close` and `Removable` are "each carried to `docs/designs/orchestrator-mode.md:493, 636, 841, 877`". I read those lines in `/home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator-mode.md`: 636 is the footnote "Stalled and fenced are not observed", 841 is row D7 ("The footnote covers stalled and fenced only"), 877 is row SP-24 "Applied as D7", 493 is Rule 5. None of 636, 841 or 877 mentions `agent_wait_since`, `Safe to close` or `Removable`. The design carries them elsewhere: `agent_wait_since` at 493, 494, 649, 1003; `Safe to close` at 794 (FR-012 row); `Removable` at 795 (FR-013 row). The KNOWN LIMIT labels rest on these citations, so a reader who follows the stated lines for three of the five items finds no scope text. | Replace "each carried to ..." with per-item lines: stalled and fenced: DESIGN:493, 636, 841, 877; `agent_wait_since`: DESIGN:493, 494, 649, 1003; `Safe to close`: DESIGN:794; `Removable`: DESIGN:795 (as synth-04 lines 84-88 and GF-1 already state). |
| F-2 | IMPORTANT | Yes (cross-file; location is outside partition A) | synth-07 line 318 (s16 Glossary row "R0, R1, R2, R3") versus synth-01 line 75, synth-03 release-stage table, `release-gates.md` row R1 (origin/master: "R1 Live worker-list: COUNTS strip, freshness strip, worker ledger ... JSON snapshot export") | The glossary defines "R1 golden worker-list samples". synth-01 and synth-03 define R1 as the live worker ledger, `--once` and snapshot (PR #503). The gate document says R1 is the live worker-list stage and that R1 is the stage that records the golden samples; the glossary turns a duty of R1 into its definition. Two files give different meanings to the same stage name. | In synth-07 line 318 change to: "R1 live worker-list ledger, `--once` and snapshot (it records the redacted golden samples)". Owner of partition B to apply. |

### Notes (minor; never fail the gate)

| # | Location | Note |
|---|---|---|
| N-1 | synth-01 line 7 | "Four subjects" followed by "Three are live" and "Two are designed only" counts five items; the s1 table has five rows. Say "four subjects (three live, one designed-only package) plus the designed orchestrator writer". |
| N-2 | synth-01 line 100 | "9 of 9 fixture names ... 0 of 10 fixture contents": synth-05, synth-06 and synth-07 use 10 (base plus 9 variants). Use 10 of 10 names. |
| N-3 | synth-02 lines 104, 115, 139; synth-03 s5.2; synth-04 s5.3; synth-06 | The same two DEFECT-CANDIDATEs appear as D-1 / C8-9 / DC-02 and as C8-8 / DC-01 (no id in synth-01 to synth-05). Print one crosswalk line (D-1 = C8-9 = DC-02; prefs answer = C8-8 = DC-01) and add the "Section 14" pointer to the C8 text of synth-03 and synth-04; also note ORCH:1021 and 1041 are missing from some writer citation lists (synth-02 line 115). |
| N-4 | synth-01 line 98 | "6 of 8 classes can print on live data" is looser than synth-04 (idle and person session need `person_started True`, no live row found; waiting (a) needs a non-null `agentWait`, never captured). Add "(idle and person session never seen live)". |
| N-5 | synth-01 s2.1 diagram | Sweep source box omits `run-current`; the matrix and synth-04 list it. |
| N-6 | synth-01 line 109 versus synth-02 line 169 | Sweep sanitizer cited as `report.py:569-599` and `569-605`. Pick one range. |
| N-7 | synth-01 line 19 | "on master via #503 (545 files)" can be read as 545 package files; the package is 406 files, 545 is the PR total. |
| N-8 | synth-02 to synth-04 preambles and inline handles | Strip or define research-internal handles (R01, GF1, GF4, file 04, M-n) before assembly; keep register ids (U-, SD-, CC-, G-) only if the register ships with the document. |

---

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was supplied in the prompt, so nothing was skipped on reliance; structural facts (line counts, file counts, paths) were re-counted independently as listed below.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- C8 carry-line citations: read `docs/designs/orchestrator-mode.md` lines 493, 494, 636, 649, 794, 795, 841, 877, 1003 on the snapshot (Bash `sed -n`), compared with synth-01 line 115 and synth-04 lines 84-88: found F-1.
- Observer stage definition: ran `git show origin/master:.dev/issues/409/bmad/spec-orca-observer/release-gates.md | grep` for rows R0 to R4 and compared with synth-01, synth-03 and synth-07: found F-2.
- Live versus designed: Grep of `QUESTION_GATE_PASSED|QUESTION_LINK_PASSED`, `_question_refusal`, `no-question-fixture`, `worker_done_seen|fenced_evidence|agent_wait_since` over the snapshot: confirms built R2/R3, refused fixture replay and producer-less sweep inputs as the synthesis states.
- Join description: read `classify.py` 600-690 to confirm the overlaps-table sentence about path A / path B.
- Numbers: `wc -l`, `ls`, and `^def test_` Grep counts on the snapshot and the checkout package (values in check 1 and check 8).

**Factual claims independently verified:** about 60 (counts, line citations, constants, labels). **Files read:** synth-01 to synth-07, GF-1, gaps-and-questions.md (rows 98-102, 260-262), `classify.py`, `orchestrator-mode.md` (9 lines), `WORKER-CONTRACT.md` (lines 23, 287-289), `release-gates.md` (via git show), research/06 (Grep). **Why trust a finding count of 2 blocking:** the synthesis files agree with the code on every count and constant I re-checked, so the defects are citation and definition errors, found by reading the cited lines rather than the claims about them. **Web research:** none performed (Tavily not needed); Tool-engagement summary: no external lookup.

## Confidence gate

- TOTAL checklist items: 9. VERIFIED (tool evidence cited): 9. UNVERIFIABLE: 0. UNCHECKED: 0.
- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 (the 7 synth files, GF-1, gaps-and-questions x3, classify.py, report) | Grep: 14 | Glob: 2 | Bash: 5. Read + Grep + Glob (29) is at least the 9 checks.
- The confidence figure measures how many checks were evidenced, not that the synthesis is free of defects; the verdict below is FAIL.

## Actions Taken

None (fix authorization false). No synthesis, source or design file was modified; only this report was written.

## Recommendations

1. Fix F-1 in synth-01 line 115 (per-item design citations).
2. Fix F-2 in synth-07 line 318 (R1 definition), then re-run the gate for the two files.
3. Apply notes N-1 to N-8 when assembling; none blocks.

## Overall Verdict: FAIL

Blocking findings: 2 (F-1 in partition A, F-2 in synth-07 found by cross-check). Minor notes: 8.

## QA Complete
