# Input reconciliation: PRD vs originals (issue 409)

Reviewer: input-reconciliation subagent, 2026-11-08. Read-only on all inputs.

Inputs checked:
- O = `IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md` (17 lines)
- H = `IronClaude/issue-409-mvp/.dev/issues/409/bmad/handoff-step1.md` (17 lines)
- I = issue 409 body (`gh issue view 409 --repo IronbellyOrg/IronClaude --json body --jq .body`, 102 lines; line numbers are of that output)
- PRD = `prd.md` (498 lines), ADD = `addendum.md` (52 lines)

Status: complete. 3 BLOCKING, 8 MINOR. `extract-originals.md` was not used as a source; every finding below was checked against O, H and I directly.

## BLOCKING

### B1. The confirmed stack is never stated, and the gate row reopens it
- Source: O:17 "Stack and release-1 scope CONFIRMED ... The owner chose 'Python + Rich with snapshot export' ... This supersedes item 2 (stack no longer open)." H:5 "Python + Rich `superclaude observe`-style subcommand, key-reader spike first, Textual only on failure".
- PRD: PRD:101 lists "stack confirmation" among the things the still-pending DIRECTION-SELECTED record must hold. That treats a closed owner decision as open.
- PRD: nowhere does it say the owner confirmed Python + Rich (the string "Python + Rich" appears only inside OI-11, PRD:445, as a numbering note). Section 4 (PRD:94) records the staged direction as binding but not the stack. FR-2 (PRD:129) mentions Rich only through the spike rule.
- The PRD never says that the issue's Go preference (I:27, "Preferred direction is Bubble Tea v2, Lip Gloss v2 and Bubbles v2") is overridden by the owner (H:17 "issue's Go preference overridden by owner decision 2", in fact by item 5). A reader holding the issue sees a conflict with no explanation.
- Fix: in section 4, add one binding line: "Stack CONFIRMED by the owner 2026-11-08 (owner-decisions item 5): standalone Python + Rich observer as a `superclaude observe`-style subcommand; key-reader spike first; Textual only if the spike fails; this overrides the issue's Bubble Tea preference (I:27)." Remove "stack confirmation" from PRD:101.

### B2. AC 2's "explains why they matter" has no requirement, but the table says it is covered
- Source: I:78 "The observer identifies human attention items and explains why they matter"; I:19 "shows attention items and reasons".
- PRD: PRD:320 (9.1 row 2) maps the criterion, including "why they matter", to T7, T10-T12, T46 and FR-17/FR-18, and marks it "fully met" at R3. None of those tests and neither FR-17 (PRD:240-247) nor FR-18 (PRD:251-255) requires a reason or "why" for an attention item. Unlike the other gaps it is not marked "no spec test", and P2 (PRD:374) leaves it out.
- Fix: add an FR-17 consequence ("each observed question shows why it needs a human, from source fields only, or `reason unknown`"), or mark row 2 "no spec test for reasons" and add it to P2 and OI-6.

### B3. AC 6's "unmapped worktrees" is claimed covered with no test or FR
- Source: I:82 "including uneven ownership, shared/unmapped worktrees ...".
- PRD: PRD:324 (row 6) lists T16, T17, T20, T21, T22, T39, T40, T13, T19 and FR-1/4/5/9. T20 (PRD:145) covers shared worktrees only. No FR-4 consequence covers a session with no worktree. PRD:37 mentions "some sessions are unmapped" only in the user description.
- Graded BLOCKING because part of an acceptance criterion is silently marked covered. Fix: add an FR-4 consequence (an unmapped row shows `worktree unknown (absent in source)` and is still counted), or flag "no spec test" in row 6 and in P2.

## MINOR

- M1. Wrong decision number on FR-2. PRD:129 cites "owner decision 2" for the stack rule; O:11 (item 2) says the stack was *not* confirmed, and O:17 (item 5) confirms it. OI-11 (PRD:445) notes the mismatch but FR-2 still cites item 2. Cite item 5.
- M2. Wrong decision number for the open items. PRD:451 "Owner positions still open (owner decision 4): the licence opinion (OQ-9) and TUIBBS as the staff platform (OQ-10)". O:17 numbers the licence opinion as decision 4 and the staff platform as decision 5 (summary.md numbering); in O, item 4 (O:15) is the TUIBBS background note. Cite O:17 and both numbers.
- M3. The issue's third-party code rule is narrowed to TUIBBS. I:38 "Use original compositions or properly licensed upstream library APIs, not an unreviewed transplant of third-party application code/assets." NFR-14 (PRD:276) covers only TUIBBS/AGPL and `canvas.py`. The visual-grammar references (I:36: otel-tui, Dolphie, bashtop, btop, oxker) are not covered. Widen NFR-14 to all third-party code and assets.
- M4. "IronClaude/Coder environment" becomes "IronClaude environment". I:7 vs PRD:29.
- M5. Problem statement narrowed and misattributed. PRD:27 attributes "loses human questions in recency-ordered chat, and 'read' gets treated as 'handled'" to "issue 409 Problem Statement". I:11 says "can miss important decisions, meaningful updates, and evidence in noisy chats"; recency and read-as-handled come from the merged requirements, not the issue. Quote I:11 as written, then the merged-requirements root cause separately.
- M6. AC 11 is carried as "Open" with no mention that the issue says delivery already happened. PRD:329 and OI-7 (PRD:439) call it open; I:5 and I:25 say the complete package ZIP is published (406 files plus checksum manifest, 14,438,526 bytes) and the image attachments are embedded (I:44-71). Record that the issue states delivery, still unverified by a check.
- M7. The write-back first stage presumes TUIBBS as its host. PRD:392 "Lives inside the later Go TUIBBS screen", but the licence opinion and TUIBBS as the staff platform are open (O:17; OQ-9, OQ-10). The section is labelled "nothing here is approved" (PRD:380), so this is wording only: add "if TUIBBS is chosen (OQ-10) and the licence opinion allows (OQ-9)".
- M8. The issue's design-package caveats are dropped. I:73 "there is no independent post-correction PASS. No performance, live integration, or user-comprehension claim is made." This is not carried into the PRD, which matters because R0 reviewers use those renders (PRD:52). Add one line to section 2.2 or 13.

## Checked and found consistent (no gap)
- Staged direction: PRD:94 and PRD:31 match O:6-8 (R1 = Signal Bridge worker ledger on `worker-list` with the "question source UNVERIFIED" notice; Attention Ledger after QUESTION-OBSERVATION; Decision Desk behind QUESTION-LINK). Whether this satisfies DIRECTION-SELECTED stays open (PRD:101, OQ-1), as O:9 requires.
- Snapshot: FR-16 (PRD:231-236) gives a versioned, additive-only JSON snapshot via `export(view)` with a schema test, in R1, for a later read-only Go screen (PRD:54), matching O:17. Key-reader spike first: FR-2 and PRD:100, matching O:17. Textual only if the spike fails: PRD:129, matching H:5.
- R1 read-only; write-back a future stage needing the issue 409 boundary change plus the TUIBBS FR-X-13 amendment: PRD:107, 281, 382-384 and OQ-11, matching O:13 and the brief. Licence opinion and staff platform are open (OQ-9, OQ-10), and TUIBBS is background only (PRD:89, NFR-14).
- Users: one human, 5-10 orchestrators, 50-100 sessions (PRD:27, 37 vs I:11). The user story is quoted verbatim (PRD:48 vs I:15).
- All 11 issue acceptance criteria (I:77-87) appear in 9.1 (PRD:319-329).
- Issue rules: dirty/stale/shared/admission rules (I:19) at PRD:200; schema PROPOSED and Orca/coordinator authority (I:21) at PRD:18-19 and NFR-14; the unverified-feed list (I:21) at PRD:489; non-goals (I:91) at PRD:281-287, including forks and "does not authorize production code changes or deployment".
- No invented Orca facts were found against these three inputs. Spec-sourced detail (T-ids, argv, write-back gates) was not traced to the spec; that is outside this input set.

