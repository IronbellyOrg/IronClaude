# QA Report: R4 cross-reference chain lens (rf-qa-qualitative, doc-qualitative)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` (1041 lines on disk), items 5.1 to 5.11
**Date:** 2026-11-09
**Phase:** doc-qualitative, cross-reference lens (research/09 Gap 5, 500-1500 line row)
**Fix cycle:** N/A (`fix_authorization: false`; this report is the only file written)
**Partition note:** one lens of 9 agents. Domain accuracy of WC-16 against master's liveness rules is another lens (`qa-domain-accuracy-report.md` exists; I did not rely on it).

## Scope and method

Chains followed:

- Chain A (WC-16): section 8 (`:666-703`) to routing rows R2 (`:712`) and R8 (`:718`), the `.gitignore` comment (`:732`), FR-023 (`:794`), step 1.17 (`:943`) and the rollback row (`:970`). I also followed it to sections 1, 11, 13, 15, 17 and 18.
- Chain B (565 anchor): line 28 to step 1.7 (`:932`) and the rollback row (`:968`).

Files read from disk (every Read at most 150 lines): the DESIGN in chunks (`:1-60`, `:60-84`, `:353-382`, `:434-449`, `:645-704`, `:660-740`, `:740-850`, `:849-960`, `:961-1041`); `src/superclaude/core/WORKER-CONTRACT.md` by line (`:12-23`, `:46`, `:95-112`, `:151`, `:270-276`) and by grep for `WC-*`; `tests/skills/test_worker_contract.py` (`:25`, `:84-98`, `:165-173`, `:209-238`, `:382-391`, `:755-771`, `:831-839`, `:905-930`, `:1081-1082`, `:1318-1322`, `:1556-1570`, `:1940-1955`, `:1966`, `:2016`); `src/superclaude/core/HOW-WE-WORK.md` (`:316-338`, `:394-406`); `.gitignore:252-256`; `CHANGELOG.md:1-14`; `docs/user-guide/commands.md:105-117`; the developer guide `:991`; `src/superclaude/cli/main.py:515-570`; `src/superclaude/cli/recommend/__init__.py:8-24`; the three routing tests; research/07 (all 173 lines); research/08 (all 125 lines); `r4-wc14-hits.md`, `r4-reanchor.md`, `r4-mechanical.md`. I ran no `orca` command and made no network call. Bash was used only for read-only `sed -n`, `grep`, `cmp`, `ls`, `wc`.

Fact base on disk: master has no `WC-16` anywhere (`grep -c` = 0 in `WORKER-CONTRACT.md`, `test_worker_contract.py`, `HOW-WE-WORK.md`, `CHANGELOG.md`, `.gitignore`). `WORKER-CONTRACT.md` has WC-14 (`:63`, "No turn ends between chain steps") and WC-15 (`:64`). The DESIGN file is untracked (`?? docs/designs/orchestrator-mode.md`).

## Findings

Two findings are MAJOR (they fail the gate). Seven are MINOR (notes). Every link not listed below was followed and held; see the Checks table.

### F1 - MAJOR - R2 and R8 name WC-16 as existing, but their step gates do not wait for step 1.17

Evidence:
- `docs/designs/orchestrator-mode.md:712` (R2): "WC-16 in `~/.claude/WORKER-CONTRACT.md` has the coordinator run `/sc:sweep` and read its report before it acts. The sweep is read-only and is itself never a worker." `:718` (R8) lists "WC-16" under `#### Added (sweep)`. `:711` (R1) says "never a worker", which only holds after step 1.18 writes the line 23 entry.
- `:947` step 1.21 (R1 and R2): gate "1.14". `:952` step 1.24b (R8): gate "1.16". Neither gate reaches 1.17 or 1.18. Compare `:951` step 1.24a (R7, which copies the line 23 list): gate "1.18". The design applied the right pattern to R7 and not to R2, R1 or R8.
- `:668` (section 8 gate) and `:1005` (open item 20, "Steps 1.17 to 1.19 do not start") hold only steps 1.17 to 1.19 until the owner answers GQ-11. `:5`: "Owner approval of the WC-16 text (section 8) is still required."
- On disk `WORKER-CONTRACT.md` has no WC-16 (`grep -c WC-16` = 0), so R2's sentence is false until 1.17 lands.

What is wrong: while GQ-11 is open, steps 1.20 to 1.24b may start, and R2 and R8 would publish a rule that is not in the contract and may never be approved as written. The gate on 1.17 protects the contract text but not the three documents that cite it.

Smallest fix: in section 15.2 set the gate of 1.21 to "1.14, 1.18" (1.18 implies 1.17), and of 1.24b to "1.16, 1.17". Add to open item 20's "Behaviour until closed": "R1, R2 and R8 (steps 1.21 and 1.24b) wait for 1.17 and 1.18 as well".

### F2 - MAJOR - R1's own check fails until R4 lands, but R4 is ordered after R1 and is outside the one-commit rule

Evidence:
- `:711` (R1) is "Checked by" `tests/core/test_how_we_work_routing_table.py`. On disk that file asserts `members == _OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py:296-297`, inside `test_other_commands_membership_and_live_references`, `:291`). `_OTHER_COMMANDS` is the set at `:27` that R4 (`:714`) edits.
- `:722`: "R1, R2 and R3 land in one commit." R4 is not named. `:947` step 1.21 does R1 and R2; `:948` step 1.22 does R4 with gate "1.21".
- So after step 1.21 the table has a `/sc:sweep` row and `_OTHER_COMMANDS` does not: `test_other_commands_membership_and_live_references` is red, and R1's declared check cannot pass at its own step. Applying R4 first fails the same assertion the other way round.

Smallest fix: `:722` becomes "R1 to R4 land in one commit" and steps 1.21 and 1.22 merge (or 1.22 lists gate "1.21, same commit"). Keep R3's "same commit as 1.21" line.

### F3 - MINOR - Rollback row for WC-16 omits the fifth pin

Evidence: `:688` (pin 5) changes `RULE_PHRASES["never-as-worker"]` at `test_worker_contract.py:89`. `:970` lists "WC-16 with the D6 sentence, the line 23 never-as-worker entry, the `RULE_PHRASES` entry, the `NEVER_AS_WORKER` entry, the `UNATTENDED_COMMANDS` assertion (design) and the test rename". That covers pins 1 to 4 and steps 1.17 and 1.18, not pin 5. If a reader reverts row by row, line 23 goes back to the old list while `test_worker_contract.py:89` still pins `/sc:sweep`, and `test_contract_states_rule[never-as-worker]` fails. The rollback check at `:978` runs that file, so it would show red.
Why MINOR: `:963` makes the mechanism one revert of the whole branch, so the row list is descriptive.
Fix: add "the `RULE_PHRASES["never-as-worker"]` phrase change (line 89)" to `:970`.

### F4 - MINOR - The `.gitignore` comment cites WC-16, but the rollback keeps the comment and reverts WC-16

Evidence: `:732` "(WC-16)" is in the comment that step 1.4a (`:928`) commits first, long before 1.17 writes WC-16. `:970` reverts WC-16; `:973` keeps the `.gitignore` lines "until existing reports are dealt with". After a rollback, or after the owner rejects the WC-16 text, the kept comment points at a rule that does not exist.
Fix: drop the rule number from the comment ("dated, operator-local, never posted. Never tracked.") or add to `:973`: "reword the comment when WC-16 is reverted".

### F5 - MINOR - Pin 5 quotes an old string that does not match line 89

Evidence: `:688` gives the old phrase as ``"`/sc:spawn` and `/sc:swarm-wizard`, "`` with a leading quote character. On disk `tests/skills/test_worker_contract.py:89` is `"`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "`: the quoted literal starts at `/sc:agent`, so no quote precedes `/sc:spawn`. Used literally as an Edit `old_string`, the text finds no match.
Fix: give the old text as `` `/sc:spawn` and `/sc:swarm-wizard`, `` without the leading quote, or name the whole of line 89.

### F6 - MINOR - R2's anchors are pre-R1 values and the row does not say so

Evidence: `:712` cites `## Orca coordination` "(line 396)" and the never-workers bullet "(line 403)". R1 adds one row above them in the same step 1.21, so they become 397 and 404 (`research/08-reanchor-routing.md:111`, and `:57` "R2 shifts to after 404 once R1 lands"). On disk today `HOW-WE-WORK.md:396` and `:403` are correct. An executor that applies R1 first will land R2 one bullet early.
Fix: add "(line numbers before R1 is applied)" or anchor R2 by its text ("the bullet that starts `**Some commands are never workers.**`").

### F7 - MINOR - FR-001 traceability cites sections that do not describe the `main.py` registration

Evidence: `:772`: "`main.py` registration (7.1, 7.6, step 1.7)". `grep` for `main.py` finds it only at `:28`, `:171`, `:772`, `:932`, `:968` and `:1041`. Section 7.1 declares `__getattr__` (`:360`) and `sweep_group` (`:438`) but not the `add_command` line; section 7.6 is the command and skill surface. The 565 chain (`:28` to `:932` to `:968`) is consistent, but the FR-001 row does not point at it.
Fix: cite "1 (line 28), 4, step 1.7" in `:772`, or add one sentence to 7.1.

### F8 - MINOR - Revision log R4 row claims a section 14 edit that is not there

Evidence: `:1041`: "marked the SPEC and REPORT draft names in 13 and 14". Section 14 (`:854-879`) has no WC-14 or WC-16 text; its SP-27 row (`:868`) reads "Applied as D6 | 8". Only section 13 carries the marks (`:829` D6, `:852` row 1.17). This matches `r4-wc14-hits.md:94-110`, which lists only 819 and 842 (now 829 and 852).
Fix: change "13 and 14" to "13".

### F9 - MINOR - WC-16 reuses master's cadence but changes the trigger from "wake or timeout" to "wake"

Evidence: `WORKER-CONTRACT.md:110`: "After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep". `:677` (WC-16): "On every coordinator wake, at most once every 5 minutes (the cadence of "The sweep." ...)". `:712` (R2) and `:829` (D6) repeat "every wake". The 5-minute cap matches; the trigger set does not, and the text does not say whether `/sc:sweep` is part of that sweep or runs beside it (`:672` says only that line 110 is not reworded). The pinned phrase "On every coordinator wake" is a substring of "On every coordinator wake or wait timeout", so a fix keeps the pin.
This is the cross-reference half only; whether the two sweeps conflict is for the domain lens.
Fix: "On every coordinator wake or wait timeout, at most once every 5 minutes" in `:677` and `:712`, plus one sentence saying `/sc:sweep` is an added read beside the contract's own sweep.

## Links that held (followed and confirmed)

Chain A (WC-16):
- Every WC-16 hit uses the same id: `:5`, `:13`, `:666`, `:668`, `:672`, `:675`, `:684`, `:697`, `:712`, `:718`, `:732`, `:794`, `:829`, `:852`, `:943`, `:970`, `:1005`, `:1006`, `:1041`. `grep WC-14` returns four lines: `:668` (master's worker rule), `:829` and `:852` (written "WC-14 (WC-16 in this design)", the SPEC and REPORT draft names), `:1041` (the R4 row naming master's WC-14). No coordinator-loop mention of WC-14 remains. This matches `r4-mechanical.md` check 1 and my own grep.
- The four pinned phrases (`:684`) each occur verbatim in `:675-677`: "WC-16. Coordinator loop" (heading), "On every coordinator wake", "it is never posted", "It never stops watching on its own". The heading carries the ident, so `_check_rule` (`test_worker_contract.py:755-762`) passes.
- The pin is a new key `"WC-16"`: master's `"WC-14"` entry (`RULE_PHRASES`, worker rule) is not overwritten, which is the collision research/07 `:142` found.
- R2 (`:712`) uses the same cadence as WC-16 (`:677`) and D6 (`:829`); R8 (`:718`) and the `.gitignore` comment (`:732`) use the same rule id. FR-023 (`:794`), section 11 (`:761`) and step 1.19 (`:945`) name the same file, `tests/skills/test_worker_contract.py`, and section 8's five pins.
- Gate chain: section 8 (`:668`), step 1.17 (`:943`, gates 1.0b and 1.16a), step 1.0b (`:924`, GQ-11), step 1.16a (`:942`, record-only, four points), open items 20 and 21 (`:1005-1006`) and section 1 (`:5`) all agree. The `495eb96d` pin named in `:942` is defined at `:601`.
- Line 23 text (`:701`) lists `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard` in that order; pin 5 (`:688`), R7 (`:717`, "same order as section 8") and the keep-the-phrase rule (`plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers`) all fit that text. `NEVER_AS_WORKER` has 8 entries on disk (`:382-391`), so 9 after the edit.
- Disk, section 8: `WORKER-CONTRACT.md:23`, `:110` ("The sweep." under `### Liveness supervision` at `:95`), `:151`, `:273`, `:275`; `test_worker_contract.py` `:25`, `:89`, `:165-173`, `:209-219`, `:228-237`, `:382-391`, `:755-762`, `:765`, `:831-839`, `:837`, `:912`, `:1081-1082`, `:1318`, `:1322`, `:1556` (with `assert len(expect) == 31` at `:1564`), `:1940-1944`, `:1953-1955`, `:1966`, `:2016`.
- Disk, sections 9 and 10: `HOW-WE-WORK.md:318`, `:333`, `:337`, `:396`, `:403`; `commands.md:105`, `:115`; developer guide `:991`; `CHANGELOG.md:5`; `.gitignore:254` (`.dev/sprint-state/`) and no existing `sweeps` entry; `test_how_we_work_routing_table.py:27`; `test_routing_refresh.py:33` and `:648`; `test_routing_plugin_parity.py:38`; the plugin copy of `HOW-WE-WORK.md` is byte-identical (`cmp`, exit 0).

Chain B (565 anchor):
- `main.py:519` is the sprint import, `:563` the `issue_watch_group` import, `:565` `main.add_command(issue_watch_group, name="issue-watch")`, `:568` `if __name__ == "__main__":`, 569 lines. DESIGN `:28` says exactly this. Step 1.7 (`:932`) and the rollback row (`:968`) both say "after line 565". `grep` for "after line 561" or "519-561" returns nothing. The other "565" in the file (`:76`, "SPEC line 565") is a line of a different file and does not collide.
- `src/superclaude/cli/recommend/__init__.py:12-20` is the lazy `__getattr__` pattern that `:29` cites.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | WC-16 id identical on every hit; no coordinator-loop WC-14 left | PASS |
| C2 | Four pinned phrases verbatim in the final text; heading carries the ident | PASS |
| C3 | Section 8 to R2: same rule, cadence and installed path | PASS |
| C4 | Section 8 to R8: WC-16 named | PASS |
| C5 | Section 8 to `.gitignore` comment: same rule id and "never posted" | PASS |
| C6 | Section 8 to FR-023, section 11 and step 1.19: same file and five pins | PASS |
| C7 | Section 8 gate to step 1.17, 1.0b, 1.16a, open items 20 and 21, section 1 | PASS |
| C8 | Line 23 text to step 1.18, pins 2 and 5, R7 and list order | PASS |
| C9 | Disk anchors cited in section 8 | PASS |
| C10 | Disk anchors cited in sections 9 and 10; plugin copy identical | PASS |
| C11 | R1 to R8 map to steps 1.20 to 1.24b, FR-024 and section 11 | PASS |
| C12 | R2, R1 and R8 step gates wait for the step that creates WC-16 | FAIL (F1) |
| C13 | R1 ordered with R4, whose edit R1's own check needs | FAIL (F2) |
| C14 | Rollback row names every section 8 deliverable | FAIL (F3, MINOR) |
| C15 | `.gitignore` comment survives the rollback it sits beside | FAIL (F4, MINOR) |
| C16 | Pin 5 old string matches `test_worker_contract.py:89` | FAIL (F5, MINOR) |
| C17 | R2 anchors stay true after R1 lands in the same step | FAIL (F6, MINOR) |
| C18 | 565 anchor: line 28 matches `main.py` on disk | PASS |
| C19 | 565 anchor: step 1.7 and rollback row say line 565 | PASS |
| C20 | FR-001 row points at text that describes the registration | FAIL (F7, MINOR) |
| C21 | Revision log R4 row matches the sections it says it changed | FAIL (F8, MINOR) |
| C22 | WC-16 cadence quote matches contract line 110 trigger set | FAIL (F9, MINOR) |
| C23 | research/07, research/08 and the r4 files agree with disk where the chains use them | PASS |
| C24 | The second "565" (`:76`) is a different file and breaks nothing | PASS |

## Summary

- Checks passed: 14 / 24
- Checks failed: 10 (2 MAJOR findings F1 and F2, 7 MINOR findings F3 to F9 across 8 checks)
- Blocking findings: 2 (MAJOR)

## Self-Audit

No `## Inherited Structural Verdict` section came with the prompt, so I used standalone behaviour and relied on no rf-qa PASS.

**(a) Reliance list:** none. I did not take any verdict from the sibling reports `qa-completeness-report.md` and `qa-domain-accuracy-report.md`; I looked at both only to avoid duplicating a lens, and every line in my findings was read by me.

**(b) Independent semantic checks (at least one required, INV-019):**
- R1 to R4 coupling: read `tests/core/test_how_we_work_routing_table.py:15-40` and `:291-300` and found `assert members == _OTHER_COMMANDS`; this is not in any producer report and is the basis of F2.
- Gate completeness for WC-16 citations: read the whole step table (`:921-957`) and compared each row that names WC-16 or the line 23 list against its gate; this found the R7 versus R2 and R8 mismatch (F1).
- Pin 5 old string: read `test_worker_contract.py:84-98` and compared the quoted old text with the literal; the leading quote does not exist on disk (F5).
- Contract wording: read `WORKER-CONTRACT.md:110` and compared with `:677`; "wake or timeout" versus "wake" (F9).
- Claim "13 and 14": grep over `:854-879` for WC ids returns nothing (F8).
- Producer-report claims re-run: `grep -c` for em-dash returns 0; WC-14 hit count 4; "after line 565" 2 hits; each equals `r4-mechanical.md`.

Factual claims independently checked against disk: about 70 line anchors and quoted strings (see "Links that held"). No web research was done, so Tavily was not needed and no fallback was used.

**Confidence:** Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 26 | Grep: 12 | Glob: 0 | Bash: 11 (read-only `sed -n`, `grep`, `cmp`, `ls`, `wc`)

## Recommendations

Before this gate passes:
1. Fix F1: add 1.17 and 1.18 to the gates of steps 1.21 and 1.24b (section 15.2) and to open item 20.
2. Fix F2: put R4 in the same commit as R1 (`:722`) and merge steps 1.21 and 1.22.

Notes for the same edit pass (not blocking): F3 to F9, each a one-line change.

## QA Complete

Verdict: FAIL
Blocking count: 2

