# Orchestrator mode design, review 2

Reviewer: independent of the design author and of review 1. Inputs: `docs/designs/orchestrator-mode.md` (DESIGN, after fix cycle 1), `docs/designs/orchestrator-mode-review-1.md` (REVIEW1), `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (SPEC), and the ccsession source under `src/superclaude/skills/ccsession-tag/`. Line numbers are DESIGN lines unless another file is named.

## Verdict

**FAIL.** Three blocking findings.

- R2-B1: under join path B, a scoped worker whose pane later runs another session (a `/clear`, a resume, or a person running the command again in the tab) loses its tab-map entry. Its real transcript can then be `person_started` True, and the newer session is joined to the Dispatch row instead. No guard case catches this.
- R2-B2: a worker of an unscoped Run that has no tab-map entry can be shown as `person_started` True with no note at all (7.2 line 490, D9 line 809). The fix narrows SP-29 but leaves no visible marker on the rows it can no longer protect.
- R2-B3: the new unreadable-transcript rule (line 503) fires only on `OSError` on open, but the pinned `test_classify.py` fixture (line 733) expects a truncated-JSONL transcript to give `unscanned: transcript not readable`. A truncated file opens without error, so the rule and its test disagree.

B1 of REVIEW1 is fixed correctly. B3 of REVIEW1 has all its items, apart from the rule-versus-fixture gap in R2-B3.

## B1 check

Result: fixed. No blocking finding.

What the fix says, and where it appears:

- 3.2 step 7 and the error table (lines 105, 121-123): if `os.unlink(tmp)` fails after the `os.link` commit point, the run prints `[sweep publish] could not remove temp file <path>` on stderr, prints no success JSON, exits 1, and the complete report stays.
- 3.3 crash row (line 133) covers a kill between the commit and the unlink.
- 3.4 rule (line 147): "A run that exits 1 before the commit point (the successful `os.link`) leaves no file at any report name". The exit-1-after-commit sentence names both causes, the failed print and the failed unlink, and says the second leaves the temp file as well. "A run that exits 0 has removed its temp file, so it leaves exactly one report and nothing else."
- Sequence diagram (lines 266-274) has the branch "unlink fails: report stays, no JSON -> EXIT 1".
- Section 1 (line 7) and the rollback sentence (line 940, m5 applied) say a successful run leaves one report plus its directory when new, and that the temp file exists only during publication.
- Section 12 NFR-001 (line 775) and G-1 (line 790) rows are updated.
- Rollback row (line 951) keeps leftover dot-prefixed temp files as owner-decided local files.

Unconditional "exit 1 leaves no file" lines: none found. Every statement that exit 1 leaves no file at a report name carries "before the commit point" or "before commit". The data-flow footer (line 326) says "exit 1 before commit, exit 2". It leaves out the third state, exit 1 after commit (one report, no JSON); see minor note m2.

Tested:

- `test_cli_contract.py` (line 736): `os.unlink` patched to raise after a successful `os.link` gives exit 1, no success JSON, exactly one complete report ending in `Report complete`, and the stderr line naming the temp path. The print-failure-after-commit case is also there.
- `test_readonly.py` (line 731): "no temp file and no second name for the report remain after exit 0".

"Joint reading of FR-017 and NFR-001, not a deviation" (line 817): defensible. FR-017 (SPEC line 111) requires exit 1 without success JSON on failed publication. NFR-001 (SPEC line 130) allows exactly one added file on success. SPEC 5.3 (lines 160-181) states no exit-1 disk rule, and G-1 (SPEC lines 637-645) hands that rule to the design. Treating a failed unlink as failed publication breaks no SPEC sentence, so no section 13 entry is needed. The closing clause "it adds no rule the SPEC lacks" is not accurate, though: it adds exactly the exit-1 disk rule that G-1 asked the design to supply. See minor note m1.

## B2 check, with ccsession evidence

### What the ccsession source shows

The installed copies under `~/.claude/skills/ccsession-tag/` are byte-identical to the source (`cmp` exit 0 for `ccsession` and `hooks/session-name.sh`).

| Claim | Evidence |
|---|---|
| One file per pane, three lines: session id, launch folder, terminal handle | `src/superclaude/skills/ccsession-tag/ccsession:558-564` (comment, `ORCA_TABS_DIR`), `:590` (`want="$session"$'\n'"$folder"$'\n'"$ORCA_TERMINAL_HANDLE"`), `:601-602` (atomic replace of this pane's file) |
| Needs a valid pane key and terminal handle | `ccsession:566-572` (`orca_tab_file`), `:584-587` |
| Written only for the Claude Code a `ccsession` launch started | `ccsession:1889-1890` (`CCSESSION_LAUNCH_ID` exported only by a launch); `hooks/session-name.sh:144-163` (owner check against the launch pid); `:176-181` (`ORCA_TAB=1` only when `OWNER=1`, `CCSESSION_LAUNCH_ID` and `ORCA_PANE_KEY` are set, and the event is `SessionStart` or `UserPromptSubmit`); `:205-207` (the `--orca-tab-session` call) |
| A `ccsession` run inside Claude Code writes none | `ccsession:1879-1883` (unsets `ORCA_PANE_KEY` and `ORCA_TERMINAL_HANDLE` under `CLAUDECODE`) |
| Each pane keeps only its latest session, and `/clear` and resume move it | `ccsession:574-579` (comment: "/clear and /resume inside Claude Code move it along"), `:594-600` (removes other files holding the same session or a session no longer saved), `:601-602` |
| A person running the command again in the same tab is a designed case | `ccsession:607-613` (comment: "The same terminal means a person ran the command again in the tab") |
| No worker mark, no Run id, no Dispatch id | Nothing in `ccsession` or `session-name.sh` writes any such value; the file holds only the three lines above |

The fixer's summary in section 1 (line 26) matches the source and cites it accurately.

### The new rule

- 7.2 line 488: a worker is a transcript joined to a Dispatch row of a scoped Run by path A or path B; a tab-map entry counts only through that join. Correct reading of the source.
- Line 489: an entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs`. Safe.
- Line 490: no entry and no scoped join may be True when the guard holds. This is where R2-B1 and R2-B2 sit.
- Line 491: the three guard cases. Case 3 catches a path-B scoped row whose `session_join` matches no entry. It does not catch a row whose `session_join` matches an entry that now holds a later session of the same pane (R2-B1).
- Line 492: the SPEC False path `worker of Run <id>, outside scope` cannot occur because the file holds no Run id. Correct.

### D9, sign-off, fixtures, capture item 13, open item 22

- D9 (line 809) states the narrowing and its reason. The reason is accurate against the source: the file cannot tell a worker pane from a person pane, holds no Run id, has no entry for plain `claude` launches or earlier sessions of a reused pane, and no allowlisted verb lists rows of unscoped Runs (section 7.3, lines 515-524).
- Owner sign-off: step 1.0b (line 901) names "sign-off on the D9 narrowing of SP-29". Open item 22 (line 984) blocks the classify step until the owner signs off D9 or names a stricter rule.
- Four D9 fixtures in `test_classify.py` (line 733): path-B joined transcript is False and shown as `orca:<dispatch>`; unjoined entry gives None with the note; no entry and no join is True when the guard holds; path-B scoped row matching no entry makes every unjoined transcript None with the SP-16 literal. All four agree with 7.2.
- Capture item 13 (line 888) and open item 22 (line 984) exist, agree with each other and with 7.2, and feed the D9 fixtures.
- Section 14 SP-29 row (line 847) and section 12 FR-010 row (line 758) agree with 7.2.

### FR-010 and SP-29: a worker of another Run in the same tree

SPEC FR-010 and SP-29 (SPEC line 104) say a transcript whose session id appears in any Orca row of any Run is never True. The design cannot see unscoped Runs, so it cannot meet that literally, and D9 says so. The brief's minimum is weaker: such a worker must not be shown as person-started without a note. The design fails that minimum. Line 490 says outright "A worker of an unscoped Run can therefore reach True this way", and no note is attached to the True value. A reader of the report sees a True row, with idle or Historical consequences, that carries no sign that it may be another Run's worker. See R2-B2.

The SPEC's own SP-29 fixture (R1 with 2 workers, R2 with 3, tab map listing all 5) still passes. Every R2 transcript has an entry and joins no scoped row, so it gets None (line 489), and line 733 pins "none of the R2 transcripts True or Historical". The gap is only for workers with no entry, which section 1 says is the normal case for plain `claude` launches and for earlier sessions of a reused pane.

## B3 check

Result: every REVIEW1 B3 item is present. One rule does not match its own fixture (R2-B3).

Observation rules in 7.2 (lines 494-506), plus the SP-16 literal in line 491: all 12 items REVIEW1 listed are there. WC-13 note and Retained problems (496); list and show disagree (497); unknown row schema (498); duplicate Dispatch (499); input changed between reads (500); path escapes its source (501); worktree removed mid-sweep (502); unreadable transcript or contract (503); rule 6 wording and SP-07 (504); `FINAL:` reading (505); remote hosts (506); SP-16 literal (491).

Section 11 fixtures:

- `test_probes_allowlist.py` (line 732): nine byte-limit boundaries, 440, 443, 446, 450, 451, 452. Present.
- `test_classify.py` (line 733): SP-07, `FINAL:`, 442, WC-13, late heartbeat (444). Present.
- `test_report.py` (line 734): rule 6 wording, 454, WC-13 under Retained problems (380), SP-16 literal (236). Present.

Section 12 rows: the six changed rows FR-006 (754), FR-010 (758), FR-013 (761), FR-014 (762), FR-020 (768) and NFR-007 (781), and the two new rows for the SPEC section 11 failure modes (792) and the section 7 cross-cutting notes (793). All present.

Missing items: none.

Rule-versus-fixture gap: line 503 says "an `OSError` on open sets `transcript_readable` False". The 442 fixture at line 733 is "a truncated-JSONL transcript ... give[s] could not determine with [its] `unscanned:` note". A truncated JSONL opens without `OSError`, so under the rule as written it stays readable and the test fails, or the implementer invents a rule. Open item 16 (line 978) says "A transcript without `timestamp` or `sessionId` is unreadable for FR-010", which is a third, different trigger. SPEC line 442 mixes the same two (detection "OSError on open", fixture "Truncated-JSONL"), so the design inherited the gap rather than resolving it. See R2-B3.

REVIEW1 line 328 asked for "the SP-16 literal as the coverage note when `session_join` is None". The design uses `tab map join not observable` for that case and prints the SP-16 literal only in cases 2 and 3. SPEC line 236 requires the literal only when Orca returned worker rows and nothing joined, so the design's choice meets the SPEC. See minor note m4 for how cases 1 and 2 interact.

## Regression scan

- Sections 3, 5, 7, 11, 12, 13 and 17 agree on publication: one report on exit 0, no file at a report name on exit 1 before the commit point, one complete report on exit 1 after it. The only gap is the data-flow footer (m2).
- Sections 7.2, 11, 12, 13, 14, 15 and 17 agree on the D9 rule, apart from the two blocking gaps that every one of them inherits from 7.2.
- `ALLOWED_ORCA` (lines 515-524) still has exactly eight templates over seven verbs: `run-current`; `worker-list`; `worker-show`; `task-list --ready`; `task-list`; `worktree ps`; `worktree list`; `worktree current`. Capture rules (line 867) and the `test_probes_allowlist.py` exact-set pin (line 732) match. The forbidden tokens `--include-remote` and `--agent-wait` stay forbidden.
- Deviation count: D1 to D9, "Total: 9 deviations." (line 811). Matches the revision log (one new deviation, D9).
- Open-item count: items 1 to 22, "Total: 22 open items." (line 986). Matches the revision log (item 22 added).
- The revision log (lines 994-996) names sections 11, 13, 14 and 15 for B2. Each has a D9 change: 733, 809, 847, and 888 and 901.
- Grep for an em dash, `TODO`, `TBD`, `FIXME` and `XXX` in DESIGN: no matches.

## Blocking findings, each with an exact fix

### R2-B1. Path B misjoins a scoped worker whose pane has moved on to a later session

Defect. The tab map keeps only the latest session of each pane (`ccsession:574-579`, `:594-602`). `/clear` and resume move it, and a person running the command again in the same tab is a designed case (`ccsession:607-613`). Under path B, a scoped Dispatch row's `session_join` (a pane key or terminal handle) then matches the pane's file, but that file now holds a later session:

1. The later session's transcript joins the Dispatch row. It is shown as the worker, `person_started` False, as `orca:<dispatch>` (line 488), even if a person started it.
2. The worker's real transcript has no entry and joins nothing. When the guard holds it is True (line 490), so it can be idle or Historical. That is the outcome FR-010 forbids for a scoped worker.

Guard case 3 (line 491) fires only when `session_join` "matches no tab-map entry". Here it matches one, so no case fires. Line 490 even names "an earlier session of a reused pane" as a no-entry example, but treats it only as the unscoped-Run case.

Exact fix:

- 7.2 line 491: change "in three cases" to "in four cases" and add: "Fourth, under path B, at least one scoped Dispatch row joined through a tab-map entry. The entry holds only the pane's latest session, so an earlier session of the same pane, which may be that worker's own transcript, has no entry. Every unjoined transcript with no tab-map entry is None with note `earlier pane session not joinable (tab map keeps only the latest session)`."
- 7.2 line 488: add "Under path B the join names the pane's latest session only. The joined row carries note `joined by pane: latest session of the pane`."
- 7.2 line 490: begin with "Under path A only, ...", so the no-entry True path never applies under path B.
- D9 (line 809), the FR-010 row (line 758) and the SP-29 row (line 847): say "four join-incomplete cases" and name the path-B earlier-session case.
- Section 11 `test_classify.py` (line 733): add the fixture "path B, a scoped worker pane whose tab-map file now holds a later session: the worker's earlier transcript is None with the earlier-pane note, never True or Historical, and the joined row carries the latest-session note". Change "the three incomplete cases" to "the four incomplete cases".

### R2-B2. A worker of an unscoped Run can be True with no note

Defect. Line 490 and D9 (line 809) let a transcript with no tab-map entry and no scoped join be `person_started` True when the guard holds, and they say "a worker of an unscoped Run that has no entry can be True". No note is attached. SPEC FR-010 and SP-29 (SPEC line 104) say such a transcript is never True. The design cannot meet that literally, and owner sign-off at 1.0b covers the narrowing. But the report then shows a possible worker of another Run as a person's session with nothing to tell the reader. The brief's minimum, "not shown as person-started without a note", is not met. The D9 fixture at line 733 pins that bare True.

Exact fix:

- 7.2 line 490: append "Every True reached this way carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and in the JSON `notes`."
- D9 (line 809): append the same sentence after "can be True".
- Section 11 `test_classify.py` (line 733): change the third D9 fixture to "a transcript with no tab-map entry and no join is True when the guard holds and carries the `origin not proved` note (the declared D9 limit)".
- Section 11 `test_report.py` (line 734): add "a True row with the `origin not proved` note prints the note in its row".
- Open item 22 (line 984): add the note to the behaviour until closed.

If the owner prefers the stricter reading at 1.0b (None in place of True for every no-entry transcript while any scoped Run has workers), open item 22 already allows a stricter rule. The note is the minimum either way.

### R2-B3. The unreadable-transcript rule does not cover its own truncated-JSONL fixture

Defect. Line 503 marks a transcript unreadable only on "an `OSError` on open". The 442 fixture at line 733 expects "a truncated-JSONL transcript" to give `unscanned: transcript not readable`. A truncated file opens normally, so the test fails against the rule, or the implementer guesses a parse rule. Open item 16 (line 978) gives a third trigger (no `timestamp` or `sessionId`). This is a contradiction in the B3 fix, and an implementer reaches it at step 1.9.

Exact fix:

- 7.2 line 503: replace "an `OSError` on open sets `transcript_readable` False" with "an `OSError` on open, or a tail read (the 256 KiB limit) that holds no complete JSON record with both `timestamp` and `sessionId` (a truncated or malformed JSONL), sets `transcript_readable` False".
- Open item 16 (line 978): point to the same rule ("unreadable as defined in 7.2, observation rule for SPEC line 442").
- Section 11 line 733: make the fixture explicit, "a truncated-JSONL transcript (last record cut mid-object, no complete record with `timestamp` and `sessionId`) and an unreadable contract (open raises `OSError`) each give could not determine with their `unscanned:` note (442)". Optionally add a transcript cut only in its last line that still has an earlier complete record and stays readable.

## Minor notes

- m1. Line 817, "it adds no rule the SPEC lacks": it adds the exit-1 disk-state rule that G-1 (SPEC lines 637-645) delegates to the design. Reword to "it supplies the exit-1 rule G-1 asks the design to make and contradicts no SPEC sentence".
- m2. Data-flow footer (lines 325-326) lists exit 0 and "exit 1 before commit, exit 2", but not exit 1 after commit (one complete report, no JSON, possibly one temp file). Add a third line.
- m3. 3.4 (line 147) lists "killed" among exit-1 outcomes ("only when it was killed or its own unlink failed"). A killed run has no exit 1. Line 149 says "a killed run leaves no file that looks complete", but a kill between `os.link` and `os.unlink` leaves a complete report (3.3 line 133). Say "a run killed before the commit point leaves no file that looks complete; one killed after it leaves a complete report, which is correct".
- m4. Guard cases 1 and 2 (line 491) can hold together: `session_join` None on every row means nothing joined while worker rows exist. Say which note each transcript carries then (both, or the SP-16 literal first), so `test_report.py` can pin it.
- m5. REVIEW1 line 328 asked for the SP-16 literal when `session_join` is None. The design uses `tab map join not observable` for that case, which SPEC line 236 allows. Record the choice in the revision log so the next reviewer does not reopen it.

Minor count: 5.

## Self-audit

What was checked, and how:

- B1: read 3.2 to 3.4 (lines 105-149), the sequence diagram (266-274), the data flow (320-327), section 1 (line 7), rollback (940, 951), the NFR-001 and G-1 rows (775, 790), section 13 (809-817), and the `test_cli_contract.py` and `test_readonly.py` rows (731, 736). Compared them with SPEC FR-017 (111), NFR-001 (130), 5.2 and 5.3 (160-181) and G-1 (637-645). Looked for any exit-1 statement without the commit-point condition.
- B2: read `ccsession:556-615` and `:1876-1891`, and all of `hooks/session-name.sh`. Confirmed the installed copies are byte-identical with `cmp`. Read 7.2 joins (484-492), D9 (809), 1.0b (901), capture item 13 (888), open item 22 (984), the FR-010 and SP-29 rows (758, 847) and the D9 fixtures (733). Compared them with SPEC FR-010 and SP-29 (104) and SP-16 (236). Traced three pane histories against the rule: one session per pane, a reused pane under path B, and a worker of an unscoped Run with no entry.
- B3: compared each REVIEW1 B3 item (REVIEW1 lines 142, 302, 316, 328, 351 and the surrounding list) with 7.2 (494-506), section 11 (731-734) and section 12 (754-793). Checked each new rule against its fixture.
- Regression: allowlist (515-524) against the capture rules (867) and the pin (732); deviation and open-item totals (811, 986) against the revision log (994-996); grep for em dashes and TODO, TBD, FIXME and XXX markers.

Not checked: sections 4, 6, 8, 9 and 10 beyond what the fixes touch, and SPEC requirements that fix cycle 1 did not change. The Orca `worker-show` field names stay unverified until capture step 1.0a, as the design says.
