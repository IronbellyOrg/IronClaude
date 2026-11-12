# QA Report: Task Qualitative Review (operational-correctness lens), Phases 1 to 7

**Topic:** TASK-RF-sweep-phase1-20261108-072653
**Date:** 2026-11-08
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**fix_authorization:** false (report only)
**Assigned:** Phases 1 to 7

---

## Overall Verdict: FAIL

Blocking: Q-01, Q-02, Q-03, Q-04, Q-05, Q-06, Q-07 (all IMPORTANT). No CRITICAL finding. Inherited N-01 is not re-reported.

## Drift baseline (BUILD-REQUEST GOAL, verbatim first sentence)

"Build the MDTM task file for issue #339 Phase 1 (orchestrator mode). The task, when run by `/task`, first closes five required design items on `docs/designs/orchestrator-mode.md`, then implements, exactly as that design specifies: ..." The full GOAL is at BUILD-REQUEST.md lines 9-23 and is copied verbatim at task lines 120-134. Drift axis is active.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-4 | FAIL | Ran every Phase 1 anchor read (18 anchors all CONFIRMED at 5dc29d23, `wc -l` 1013/327/3195/569, `cmp` exit 0). Ran the Phase 2-6 greps on DESIGN as it is now. Item 6.4 check `grep -n '^| R5 |'` already hits DESIGN:698 (routing row R5), so "the R5 row exists once" can never pass after 6.3 adds the Fix cycle 3 row (Q-06). Item 2.1 verification greps only field names and cannot see a duplicated or table-breaking row (Q-01). |
| 2 | Project convention compliance | none | PASS | Phases 2-6 edit only `docs/designs/orchestrator-mode.md`; no `.claude/` path; no commit, push, fetch or rebase; 7.19 `gh` carries `--repo IronbellyOrg/IronClaude`; 7.18 uses `uv run python`; reads in 150-line chunks; 7.13 reads APPROVED.md (90 lines, checked) in one chunk. |
| 3 | Intra-phase execution order | AX-3 | FAIL | Item 2.2 writes research/04 edit 4 text, which ends "Several matching rows follow the R3-B2 rule below." and drops the old clause "and that transcript is None with the same note" (DESIGN:494). The R3-B2 rule only arrives in item 3.1. The r3-b1 gate (2.8-2.25) audits that intermediate state and no lens prompt says R3-B2 is pending (Q-02). |
| 4 | Value/signature verification | AX-1 | FAIL | DESIGN:455 already reads "plus `dispatch: str`, `run: str`, `session_join: str \| None` (design: ...)". research/04:87 edit 1 says to replace "the parenthesis at the end of the row" with text that again begins "plus `dispatch: str`, `run: str`, `session_join: str | None`", with unescaped pipes. Item 2.1 says to copy it "exactly as worded" (Q-01). |
| 5 | Module (document) context | AX-2 | FAIL | DESIGN:665 says the WC text is "The SPEC section 10 text (lines 404-408), unchanged, with one sentence appended", and D6 (DESIGN:812) says "The same text with one sentence appended". Items 5.1 and 5.4 change the heading id and the cadence sentence. SPEC:415 and OQ-7 (SPEC:583) say "Phase 1 sets no cadence". Items 5.8 and 5.12 lock `Total: 9 deviations.` (Q-04). |
| 6 | Downstream consumer analysis | AX-2 | FAIL | Item 5.4 removes "It sweeps on every wake" from WC-16 because it reads against contract :110 (research/07:134). Item 5.2 only renumbers routing row R2 (DESIGN:695), which keeps "**The coordinator sweeps on every wake.**". The Phase 12/13 item at task:2258 then copies that into the installed HOW-WE-WORK.md (Q-05). |
| 7 | Test (verification) validity | AX-4 | FAIL | Item 5.10's grep `WORKER-CONTRACT.md:\|test_worker_contract.py:\|HOW-WE-WORK.md:\|commands.md:\|CHANGELOG.md:\|main.py:` returns 0 hits on DESIGN (`grep -c` = 0). DESIGN cites lines as "line N", so the catch-all re-anchor step always passes (Q-07). Minor always-pass sub-checks are in 3.1 and 5.8 (M-02). |
| 8 | Coverage of required edits | AX-3 | FAIL | research/04:95 edit 9 also says "Also fix the cycle 2 row's 'the transcript's earliest timestamp' to 'the earliest `timestamp` in the transcript tail' (m2)". The phrase exists at DESIGN:1011. Item 2.6 omits it, item 2.11's completeness lens treats a PARTIAL edit as BLOCKING, and item 4.5 says "Leave the cycle 2 R2-B1 row unchanged" (Q-03). |
| 9 | Error path coverage | none | PASS | Every owner gate has a non-default-answer HALT: 6.3(a), 7.2, 7.4(b), 7.6, 7.8 (72h recorded), 7.10(b), 7.12(b). 7.16 HALTs on a before/after difference (matches DESIGN:875). 7.17 HALTs on a field-name mismatch and on missing open item 2. 7.19 HALTs on #422 or ancestry drift. Notes M-06 and M-08. |
| 10 | Runtime failure path trace | none | PASS | Walked Phase 1 -> 2 -> ... -> 7 with the halt order regression -> monotonicity -> cap (2.21, 2.25). SKIPPED paths close consistently (2.18 marks 2.18-2.24; 2.25 reads the fix-log SKIPPED). 7.20 expectations hold: 8 OQ files, the OQ-6 sentence contains "does NOT authorize adoption", OQ-8 has none. Notes M-05 and M-08. |
| 11 | Completion scope honesty | none | PASS | R5 is never resolved by the task (6.1 PENDING, 6.2 HALT, recommendation "does NOT authorize adoption"). GQ-63 has the no-recommendation sentence. 7.19 facts hold now: `git merge-base --is-ancestor 2327fbd3 HEAD` exit 0; `495eb96d origin/master` exit 1. |
| 12 | Ambient dependency completeness | none | PASS | The Fix cycle 3 table grows R3-B1 -> R3-B2 -> R3-B3 -> R4 -> R5 in order (2.6, 3.4, 4.5, 5.11, 6.3). Every gate has its own folder (the 1.2 mkdir list matches the 14 gate names). Open Questions additions are named (6.1, 6.3). Note M-10. |
| 13 | Dependent-edit sequencing | AX-3 | FAIL | Same root as row 3: an R3-B1 edit depends on R3-B2 text that is written one phase later (Q-02). |
| 14 | Existence claims | none | PASS | Verified by tool: main.py:565 and 517-569; WORKER-CONTRACT :23/:110/:273/:275; test_worker_contract :25/:89/:155/:165-173/:382-391/:765/:837/:912/:1081-1082/:1318/:1322; HOW-WE-WORK :318/:333/:337/:396/:403/:404; commands.md :105/:115; CHANGELOG :5; .gitignore :254; graph.md :9/:41; dev guide :991; routing tests :27/:33/:38/:648; APPROVED.md lines 10-90 (13 rows); pragmatic.md :22/:53; sc-crash-recovery :26; GAPS :33/:34/:58/:84/:86; orca-ide symlink; commits 2327fbd3, 495eb96d, e8db2fe6. |
| 15 | Cross-references to research/template sections | none | PASS | research/04 edits 1-9 at :87-95, fixtures :99-117 and :154-164, R3-B3 :186-200, gates :221-224; research/07 :98, :100, :134, :142-158; research/08 :119. All are where the items say. Notes M-04, M-09 and M-11. |

## Summary
- Checks passed: 8 / 15
- Checks failed: 7
- Critical issues: 0
- Important (blocking) issues: 7
- Minor notes: 11
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Axis | Location | Issue | Required Fix |
|---|----------|------|----------|-------|-------------|
| Q-01 | IMPORTANT | AX-1 | Task 2.1 (line 244); research/04:87-88; DESIGN:455, :457 | Edit 1's replacement text starts with "plus `dispatch: str`, `run: str`, `session_join: ...`", which DESIGN:455 already holds before the parenthesis. Replacing only "the parenthesis at the end of the row", as 2.1 says, duplicates those three fields. Edits 1 and 2 also carry unescaped `datetime | None` / `str | None` inside table rows, while DESIGN escapes them (`str \| None`, DESIGN:455/457). Copying "exactly as worded" splits the table cells. The 2.1 verification only greps the field names, so it passes a broken row. | In 2.1, say: replace the whole tail of the row from "plus `dispatch: str`" to the end of its parenthesis; escape every `|` inside table cells as `\|`. Add to the verification: the `OrcaObservation` and `TranscriptTail` rows have the same `|`-separator count as the header (same rule 2.5 already uses), and `grep -c 'plus `dispatch: str`'` on the row is 1. |
| Q-02 | IMPORTANT | AX-3 | Task 2.2 (line 251) vs 3.1 (line 425); r3-b1 lens prompts 2.12 and 2.14 | Edit 4's second replacement deletes "and that transcript is None with the same note" and ends "Several matching rows follow the R3-B2 rule below." During the whole r3-b1 gate there is no R3-B2 rule, and 7.2 states no transcript outcome for a failed path-B match. Meanwhile the new section 11 fixture `test_path_b_terminal_row_without_end_has_no_window` asserts "S None with the same note". The crossref lens ("every ... cited in the new text must exist") and the actionability lens ("a row with no end time ... no start time") are built to flag this. The result is predictable BLOCKING findings. The fix agent has no research/04 section 3 input, so it may write its own transcript rule, which item 3.1 then contradicts. This also eats one of only two fix cycles and raises the monotonicity-HALT risk. | Do one of these: (a) add to every r3-b1 lens prompt (2.8-2.16) and the fix-agent input: "The R3-B2 several-rows rule (research/04 section 3.3, item 3.1) lands in Phase 3; the forward reference 'the R3-B2 rule below' and the transcript outcome for a failed path-B match are closed there and are not R3-B1 findings"; or (b) have 2.2 keep a temporary transcript clause ("and that transcript is None with the same note") that 3.1 replaces. |
| Q-03 | IMPORTANT | AX-3 | Task 2.6 (line 279), 4.5 (line 620); research/04:95; DESIGN:1011 | research/04 edit 9 is two edits: the cycle 3 R3-B1 row, plus "Also fix the cycle 2 row's 'the transcript's earliest timestamp' to 'the earliest `timestamp` in the transcript tail' (m2)". Item 2.6 does only the first. Lens 2.11 counts edit 9 PARTIAL, which it calls BLOCKING. Item 4.5 then says "Leave the cycle 2 R2-B1 row unchanged", which contradicts edit 9. | Add the m2 replacement to 2.6 (anchor "the transcript's earliest timestamp", DESIGN:1011) with a `grep -c "the transcript's earliest timestamp"` = 0 check. Reword 4.5 to "Leave the rest of the cycle 2 R2-B1 row unchanged (2.6 already applied the m2 wording)". |
| Q-04 | IMPORTANT | AX-2 | Tasks 5.1, 5.4 (line 787), 5.8 (line 815), 5.12 (line 843); DESIGN:665, :812; SPEC:405, :415, :583 | After R4, DESIGN:665 still says the WC text is the SPEC section 10 text "unchanged, with one sentence appended". D6 still says "The same text with one sentence appended". But 5.1 changes the heading id to WC-16 and 5.4 adds a cadence ("at most once every 5 minutes") that SPEC:415 and OQ-7 (SPEC:583: "Phase 1 sets no cadence") rule out. That makes a false claim and an unrecorded SPEC deviation. The task also blocks the natural fix: 5.8 says "Do not add a new deviation" and 5.12 and later mechanical checks require `Total: 9 deviations.`. A gate fix agent that records the deviation would then fail every later totals check. | In 5.4, also reword DESIGN:665 and the D6 row to say the text is the SPEC section 10 text with the D6 sentence, renumbered to WC-16 and with the master cadence clause (R4). Either record that as deviation D10 and change every later `Total: 9 deviations.` expectation to 10, or record it in D6 and keep 9. State which in OQ text so the Phase 14 fidelity gate does not flag it. |
| Q-05 | IMPORTANT | AX-2 | Task 5.2 (line 773); DESIGN:695; task line 2258 | Routing row R2's bullet "**The coordinator sweeps on every wake.**" is only renumbered by 5.2. R4 removed the same claim from WC-16 because it reads against contract :110 "at most once every 5 minutes" (research/07:134). The later item at task:2258 writes R2 into the installed `HOW-WE-WORK.md` "or the revised DESIGN wording, if design fix R4 aligned it", and no R4 item aligns it. The prior alignment report graded this M-8 MINOR. It is upgraded here because the result is a shipped routing-guide sentence that contradicts WC-16 and the master contract (Critical Rule 6: contradictions are never minor). | Add to 5.2 (or 5.4): reword the R2 bullet to "**The coordinator sweeps on every wake, at most once every 5 minutes.** WC-16 in `~/.claude/WORKER-CONTRACT.md` ...", and add the check `grep -c 'sweeps on every wake\.\*\*' DESIGN` = 0. Update task:2258's quoted bullet and its verification grep (task:2260) to match. |
| Q-06 | IMPORTANT | AX-4 | Task 6.4 (line 1003); DESIGN:698 | `grep -n '^| R5 |' docs/designs/orchestrator-mode.md` already prints DESIGN:698 (routing row R5, `tests/recommend/test_routing_refresh.py`). After 6.3 appends the Fix cycle 3 R5 row there are two hits, so the pass rule "the R5 row exists once" can never pass. The FAIL path ("fix the edit in item 6.3 and re-run") then loops, or invites deleting or renaming a correct row. This is the same name clash the Key Constraints "Naming" bullet warns about. | Scope the check to section 18: count `^| R5 |` hits after the `^### Fix cycle 3` line (for example `awk '/^### Fix cycle 3/{f=1} f && /^\| R5 \|/' DESIGN | wc -l` = 1), or match the row text `'^| R5 | Master'`. Also review 5.11's R4 row against routing row R4 (DESIGN:697) for the same trap. |
| Q-07 | IMPORTANT | AX-4 | Task 5.10 (line 829) | The R4 catch-all "re-anchor every cited line" check greps only `file:line` forms. DESIGN cites changed files as "line N" (for example DESIGN:663, :677-680, :686, :694-701, :712), so the grep returns 0 hits today (`grep -c` = 0). The step's verification ("every grep hit has a status row") therefore always passes and cannot detect a stale citation. I checked every bare citation outside section 8 and main.py and found them current at 5dc29d23 today, so nothing is stale now. But the step that BUILD-REQUEST R4 requires ("Re-anchor every cited line") does not actually test anything. | Replace the pattern with one that finds the bare form near each changed file name, for example `grep -n 'line[s]\? [0-9]' DESIGN` filtered to rows naming WORKER-CONTRACT, test_worker_contract, HOW-WE-WORK, commands.md, CHANGELOG, main.py, the routing tests, graph.md and the developer guide. Require at least one hit per section 8/9/10 citation, so a zero-hit run is a FAIL. |

### Minor notes (never fail the review)

| # | Location | Note |
|---|----------|------|
| M-01 | 2.1 edit 3 (research/04:89) | The inserted sentence cites "(unknown row schema rule, line 504)". After edit 3 inserts its own paragraph before DESIGN:468, that rule moves to about line 506. Item 3.1 handles hard line numbers for its own text; 2.1 does not. Use a section reference. |
| M-02 | 3.1 verification; 5.8 verification | `grep -c 'pane moved to a later session'` >= 1 in 7.2 is already true at DESIGN:494 before the edit. The 7.6 "no `## Unattended mode`" text already exists at DESIGN:648. Both sub-checks always pass. Each item has another sub-check that does discriminate. |
| M-03 | 4.6 | After 4.5 the R3-B3 row quotes "changed three to four incomplete cases", so `grep -c 'four incomplete cases'` is nonzero. The pass rule says "absent from section 11", so the executor must map the hit lines to sections, not read the count. Say so. |
| M-04 | 4.2 | "beside the `sources` entry" in 7.4: that entry is DESIGN:566, inside the JSON code fence (558-588). Say "after the fence". |
| M-05 | 2.19/2.20 and every verifier item | Verifiers must re-check "every check id in the earlier cycle's PASS set", but their inputs list only the consolidated file, the ledger and DESIGN, not the lens reports that define each `C<n>`. Add the gate's `qa-*-report.md` glob to the verifier inputs so the regression halt runs on real checks. |
| M-06 | 7.16 | DESIGN:875 requires before/after equality apart from timestamps. research/09 asks for a live worker in the named Run. A live worker's `worker-show` `stage`, `liveness` or `agentWait` can change between the reads, so a false-positive HALT is likely. Tell the owner up front, or name the fields that may change. The forbidden-token grep expects "only the forbidden-list sentence", but no item writes such a sentence into readonly-probe.md. |
| M-07 | 7.18 | `grep -rn '/home/coder\|coder' tests/sweep/fixtures/` also scans SOURCES.md, which must state the sanitize rules. A rule written "replace /home/coder with /home/user" fails it. Say the rule must be written without the original value. |
| M-08 | 6.2, 7.2-7.15 | No item says who writes the owner's words into `Chosen:` / `Decided by:` / `Decision source:` on resume. Without it, Branch 2 is reachable only by a hand edit. The record/HALT pairs also run one at a time, so the owner faces up to 8 separate HALT-resume round trips (OQ-1 to OQ-8). Writing all OQ-2 to OQ-8 files first, then halting once, would avoid that. 7.15 Branch 2 checks only `Run id:`. |
| M-09 | Phase 2 intro, Phase 3 intro, gate inputs | research/04 section 2 is lines 77-132 (cited 75-140) and section 3 is 134-176 (cited 120-176). These are harmless extra lines. |
| M-10 | 5.12 vs 5.11 | The R4 row's "already has WC-14 and WC-15" is a new WC-14 hit after the 5.1-5.3 hit list was built. 5.12 does not say to add it as `worker rule (keep)`. |
| M-11 | 2.7, 3.5, 4.6, 5.12 heading map | `grep -n '^## \|^### '` also matches the fenced report-layout lines DESIGN:609-624 (`## Source coverage` etc.), which are not DESIGN sections. Ignore hits inside fences when mapping lines to sections. |

## Actions Taken
None. fix_authorization is false; the task file and DESIGN were not edited.

## Recommendations
- Fix Q-01 to Q-07 in the task file (all are small text edits to items 2.1, 2.2/2.8-2.16, 2.6/4.5, 5.2/5.4/5.8/5.12, 6.4, 5.10 and task:2258), then re-run this lens on Phases 2, 5 and 6.
- Optionally fix M-05 and M-08, which make every gate and every owner gate more reliable.

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 3 | Glob: 1 | Bash: 9 (four batched inspection scripts plus single greps)
- Cross-phase limit: Q-05's downstream consumer (task:2258, Phase 13) and Q-04's effect on the Phase 14 fidelity gate are outside Phases 1-7. They were read only to confirm the defect reaches them. [PARTITION NOTE: cross-phase trace limited to assigned subset.]

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for I-1 (WC-14 rename coverage: every DESIGN WC-14 line has an owning item).
- Relied on rf-qa PASS for I-2 (2.7 per-section rule is satisfiable).
- Relied on rf-qa PASS for I-4 (5.7 four points match 7.19 and research/09).
- Relied on rf-qa PASS for Phase 9 renumbering, gate counts, TBD/TODO, bare `artifacts/` paths, phase order, the no-commit check and the POST runner prompt (outside or structural).

**(b) Independent semantic checks (INV-019):**
- I-1 PASS was not enough: it proves every WC-14 line is renamed, not that the renamed text is true. Reading DESIGN:665 and :812 against items 5.1/5.4 and SPEC:415/:583 found the false "unchanged" claim and the locked deviation total (Q-04). Reading DESIGN:695 against 5.4 found the R2 cadence contradiction (Q-05).
- I-2 PASS was not enough: it proves the 2.7 matrix can be met, not that the edits that meet it are well formed. Reading DESIGN:455/:457 against research/04:87-88 found the duplicated fields and unescaped pipes (Q-01).
- Read research/04:90 against DESIGN:494 and task 3.1 to find the Phase 2 forward reference and the missing transcript outcome (Q-02). Read research/04:95 against DESIGN:1011 and task 2.6/4.5 (Q-03).
- Ran `grep -n '^| R[0-9] |'` on DESIGN (Q-06) and `grep -c` with the 5.10 pattern = 0 (Q-07). Then read every bare citation (HOW-WE-WORK :318/:337/:396, routing tests :27/:33/:38/:648, dev guide :991, graph.md :9/:41, commands.md :105) to grade Q-07's current impact.
- Re-ran the 7.19 ancestry checks (exit 0 and exit 1), checked the 13 APPROVED rows, and checked the 18 Phase 1 anchors.

I did no web research. If I reported 0 issues, the evidence above would contradict me: seven blocking defects, each with a `file:line`.

VERDICT: FAIL
