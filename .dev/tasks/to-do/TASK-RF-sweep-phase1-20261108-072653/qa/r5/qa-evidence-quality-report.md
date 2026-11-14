# QA Report: R5 evidence-quality lens (item 6.3 edit, master contract and INV-005 condition 1)

**Topic:** R5, `worktree ps --agent-wait` allowed by the owner decision of 2026-11-08
**Date:** 2026-11-09
**Phase:** fix-cycle / evidence review (fix_authorization: false, report only)
**Reviewer lens:** evidence quality. Every claim the R5 edit makes about master's contract (`src/superclaude/core/WORKER-CONTRACT.md:110`) and about INV-005 condition 1 is checked against the file on disk.

## Method

Files read: `src/superclaude/core/WORKER-CONTRACT.md` 95-134; SPEC `merged-requirements.md` 479-523, lines 132, 143, 301-312, 323 (read-only `sed`); `OQ-1-agent-wait-decision.md` (all 41 lines); `r5-mechanical.md` (all 91 lines); research/07 grep of the sweep paragraph (lines 117, 121, 127, 172); DESIGN lines 66, 157-222 (heading positions), 215-224, 505-575, 805-845, 890-897, 1035-1047, plus whole-file greps for `agent-wait`, `eight`, `seven`, `forbid`, `1.4.245`, `R5`. `git status` shows `WORKER-CONTRACT.md` unmodified and DESIGN untracked, so no diff exists for DESIGN. No `orca` command and no network call was made.

## Claims checked and what the source says

| # | Claim in the R5 edit | Source on disk | Supported? |
|---|---|---|---|
| a | Master's sweep runs "one prompt-wait listing (`worktree ps --agent-wait`)" (OQ-1 line 10; Fix cycle 3 R5 row, DESIGN 1047) | WORKER-CONTRACT.md:110 reads "one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11)"; research/07 :117 and :127 quote the same | Yes |
| b | The master sweep runs at most once every 5 minutes (D6, DESIGN 833; line 679) | WORKER-CONTRACT.md:110 "at most once every 5 minutes" | Yes |
| c | `WORKER-CONTRACT.md:110` needs no edit because master's text already allows the listing (OQ-1 line 41) | Line 110 prescribes the listing; `git status` shows the file unmodified | Yes |
| d | INV-005 condition 1 said `worktree ps` never carries `--agent-wait` (OQ-1 line 10; D10, DESIGN 837) | SPEC 500 "`worktree ps` (never with `--agent-wait`)"; 504, 310, 323, 510, 562, 619, 132 and 143 repeat it | Yes, for every line D10 lists |
| e | D10 lists the SPEC lines that say it (310, 323, 500, 504, 510, 562, 619, plus NFR-003 line 132 and NFR-014 line 143) | All nine lines checked; each carries the ban | Yes, but incomplete (see F2) |
| f | The sign-off allowlist had eight templates and the design now has ten with the same seven verbs (D10, 7.3 line 537, OQ-1 line 28) | SPEC 301 "eight templates", NFR-014 "eight pinned templates"; DESIGN 526-536 lists 10 tuples over 7 verbs | Yes |
| g | R5 shows a conflict between master's sweep and INV-005 condition 1 (Fix cycle 3 R5 row "Master's sweep runs ...; INV-005 condition 1 forbade it") | SPEC 495 "The sweep calls only these seven Orca read verbs": "the sweep" is `/sc:sweep`, the command this SPEC specifies. Condition 1 does not bind the coordinator's sweep in master's contract. DESIGN 679 and D6 keep the two sweeps separate | Partly (see F1) |
| h | "since R5 ... ten templates (NFR-014)" (DESIGN 555) | NFR-014 on disk (SPEC 143) pins eight templates and forbids `--agent-wait` on `worktree ps`; the ten-template pin comes from D10 only | No (see F3) |
| i | Owner decision "Allow it, no conditions needed." (OQ-1 line 22; DESIGN 1047) | Present only as a relay: OQ-1 line 22 cites `msg_d95a87e312e1` and `msg_6ee5998d0874`, whose text is not on disk; the task file and QA reports repeat the same quote | Relay only (see F4) |
| j | Live probe: 24 calls, 0 `index.lock` sightings, one idle worktree, Orca 1.4.245 (OQ-1 lines 34-37) | Coordinator report; no raw output on disk. SPEC 510 says `--agent-wait` "turns on terminal wait-state reads, which is why it is forbidden" and gives no static trace of those reads | Relay only; DESIGN does not rely on it (see F5) |
| k | The report lock line stays "unlikely (checked for Orca 1.4.245)" (OQ-1 line 29; DESIGN 611, 1047) | Phase 1 never calls `--agent-wait` (DESIGN 535-536 comments, 679, 895), so the lock claim covers only the called verbs | Yes |
| l | `FORBIDDEN_TOKENS` holds only `--include-remote` (DESIGN 539, 66) | OQ-1 line 30 keeps `--include-remote` forbidden; line 539 matches | Yes |
| m | Section 4 extension-point rule at line 221 names "a recorded owner decision (R5, 2026-11-08)" | Line 221 read; section 4 spans 157-222 (headings at 157 and 223) | Yes |
| n | Mechanical report: 12 of 12 checks PASS | Commands 1-10 re-checked: em-dash count 0, no `TODO`/`TBD` (exit 1), one `Total: 10 deviations.`, `ALLOWED_ORCA (10)` and `10 read templates` in the diagram, no `eight` outside D10, no `9 deviations`. Checks 11 and 12 have no command block in r5-mechanical.md, and Command 4 shows "(no output expected; ...)" instead of the observed result | Results true; recording incomplete (see F6) |

## Findings

### F1. MINOR. The R5 row frames a conflict between master's sweep and condition 1 that the sources do not show
- **Evidence:** DESIGN `docs/designs/orchestrator-mode.md:1047` ("Master's sweep runs `worktree ps --agent-wait`; INV-005 condition 1 forbade it"); OQ-1 line 10; SPEC `merged-requirements.md:495` ("The sweep calls only these seven Orca read verbs"); DESIGN 679 and 833 (D6) keep `/sc:sweep` apart from master's sweep and say it does not run the listing.
- **What is wrong:** Condition 1 binds `/sc:sweep`'s own allowlist. It never mentioned master's coordinator sweep. The two clauses are each true, but the row reads as if master's contract broke the sign-off. Master's contract and condition 1 never collided; the owner widened the allowlist of a command that does not call the flag.
- **Smallest fix:** In the R5 row, write "Master's coordinator sweep runs `worktree ps --agent-wait`; INV-005 condition 1 forbade the flag in `/sc:sweep`'s allowlist".

### F2. MINOR. D10 leaves out two SPEC statements that D10's own "ten, not eight" contradicts
- **Evidence:** SPEC `merged-requirements.md:301` ("so there are eight templates"); the "eight pinned templates of section 8" wording inside NFR-014 (line 143, already cited by D10); DESIGN 837.
- **What is wrong:** Line 301 is a SPEC statement the design now contradicts and D10 does not list it.
- **Smallest fix:** Add "301" to the SPEC line list in D10.

### F3. MINOR. DESIGN 555 cites NFR-014 for a ten-template pin that NFR-014 does not make
- **Evidence:** DESIGN 555 ("names exactly these seven verbs and, since R5 (owner 2026-11-08), ten templates (NFR-014)"); SPEC 143 pins eight templates and forbids `--agent-wait`.
- **What is wrong:** The ten-template pin comes from D10, not from NFR-014 or the sign-off text. The parenthetical points the reader to the wrong authority.
- **Smallest fix:** Replace "(NFR-014)" with "(D10)".

### F4. MINOR. The owner quote is a relay with no primary text on disk
- **Evidence:** OQ-1 lines 19-22; `msg_d95a87e312e1` and `msg_6ee5998d0874` are named in the task file, QA reports and `.dev/implement` prompts only, never as message text.
- **What is wrong:** Every on-disk copy of "Allow it, no conditions needed." traces to one coordinator relay. The SPEC was not updated and still shows the old sign-off (D10 records the difference, so the design is honest about it).
- **Smallest fix:** None required for the gate. If the owner wants a durable record, quote the two message bodies in OQ-1.

### F5. MINOR. The only lock evidence for `--agent-wait` is a relayed probe the design does not carry
- **Evidence:** OQ-1 lines 34-37; SPEC 510 ("turns on terminal wait-state reads, which is why it is forbidden", no static trace).
- **What is wrong:** Nothing in DESIGN claims `--agent-wait` is lock-safe, and Phase 1 never runs it, so no unsupported claim is made. Open item 11 and M4 (DESIGN 879, 1001) cover only `worker-show` and `task-list`.
- **Smallest fix:** None. A future change that calls `--agent-wait` must first add a capture or a lock claim.

### F6. MINOR. r5-mechanical.md records checks 11 and 12 and the Command 4 result without command output
- **Evidence:** `r5-mechanical.md:31-35` ("no output expected; grep exit status 1" is a prediction), `:87-88` (checks 11 and 12 have no command block), `:90` ("12 of 12").
- **What is wrong:** The recorded evidence is thinner than the verdict. I re-ran the equivalent greps and all pass, so the result stands.
- **Smallest fix:** Add the two missing command blocks and the observed exit status.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | WORKER-CONTRACT.md:110 names `worktree ps --agent-wait` as the prompt-wait listing in the sweep | PASS |
| C2 | The 5-minute cadence and "at most once" wording in D6 and line 679 match line 110 | PASS |
| C3 | OQ-1's claim that line 110 needs no edit holds (file unmodified, text already prescribes the listing) | PASS |
| C4 | Every SPEC line D10 cites (132, 143, 310, 323, 500, 504, 510, 562, 619) carries the `--agent-wait` ban | PASS |
| C5 | INV-005 condition 1 scope: whether it binds master's sweep | FAIL (F1, MINOR) |
| C6 | D10 lists every SPEC statement the ten-template change contradicts | FAIL (F2, MINOR) |
| C7 | The 7.3 constants (10 templates, 7 verbs, `FORBIDDEN_TOKENS` = `--include-remote`) match OQ-1 "What stays in force" | PASS |
| C8 | Attribution of the ten-template pin (DESIGN 555) | FAIL (F3, MINOR) |
| C9 | Section 4 line 221, section 11 (759), section 12 NFR-014 row (815), 15.1 (895) and GQ-109 row (66) say `--agent-wait` is allowed and not called in Phase 1, with no stale "never" or "eight" text left | PASS |
| C10 | Fix cycle 3 R5 row facts (what was added, removed and kept) match 7.3, D10 and OQ-1 | PASS |
| C11 | Provenance of the owner decision on disk | PASS with note (F4) |
| C12 | Lock evidence for `--agent-wait`: DESIGN claims nothing beyond what the sources support | PASS with note (F5) |
| C13 | The version-scoped report lock line (DESIGN 611) is still true given the allowlist change | PASS |
| C14 | r5-mechanical.md results reproduce | PASS (recording gap F6, MINOR) |
| C15 | Section 4 spans lines 157-222, `### Fix cycle 3` at 1037, deviation total 10 | PASS |

## Summary

- Checks passed: 12 of 15 (C5, C6, C8 failed on MINOR findings only).
- BLOCKING findings: 0. MAJOR findings: 0. MINOR findings: 6 (F1 to F6), recorded as notes.
- No claim about master's contract (`WORKER-CONTRACT.md:110`) is unsupported. The unsupported or loosely supported claims are all about INV-005 condition 1 and NFR-014 attribution (F1, F3) and a missing SPEC line in D10 (F2).

Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 9 | Grep: 8 | Glob: 0 | Bash: 6

Verdict: PASS
Blocking count: 0
