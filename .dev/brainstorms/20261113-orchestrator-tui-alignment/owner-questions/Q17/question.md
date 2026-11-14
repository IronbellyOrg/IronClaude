# Q17: should the observer ever show sweep facts on the Orca-ledger screen?

## The question (verbatim from the spec row)

"Should the observer ever show sweep facts on the Orca-ledger screen?"
Source: merged-requirements.md section 3, row Q17 (line 544). ADJ Part 7 row Q17 (line 787) words it in full: "Should the observer ever show the sweep's facts (frozen plans, safe-to-close, contract questions, git state) on the same screen as the Orca ledger?"

## The spec's recommended answer

"No, not now; if yes later, Q9 becomes a real requirement." Q9 is the owner question about whether the sweep's JSON is ever stored as a file or captured by the caller. Source: merged-requirements.md line 544; ADJ line 787.

## Default if unanswered

"ADJ recommendation applies", that is, no sweep-facts panel now. Source: merged-requirements.md line 544.

## What it gates (work items, in words)

- OB-09 (deferred: observer release 3, the "Decision Desk" screen, and the first of a design reviewer's four asks). Its condition (3) says the release declares which contract it reads: "snapshot v1 only, or sweep facts, which then needs Q17 = yes and SW-11". merged-requirements.md line 257; graph rows 60 and 61 (lines 707, 708).
- SW-11 (deferred: the decision on storing the sweep's JSON, owned by Q9). Its blocks column lists "OB-09 (only if Q17 = yes)". merged-requirements.md line 200; graph row 31 (line 678).
- Wave: W5 (the last wave). Line 544.

## Facts the question depends on

1. The observer (`superclaude observe`, issue #409) is a read-only terminal dashboard of Orca workers, built and merged in two releases (PR #503, PR #514). It shows Orca ledger facts in Orca's own words. ADJ glossary line 77; ADJ line 239.
2. The observer reads none of the sweep's facts today: git state, contracts, transcripts, `safe_to_close`, frozen plans and Task specs are owned by the sweep only. ADJ line 240 (units table).
3. The sweep (`superclaude sweep run`, Orchestrator mode Phase 1, issue #339) is in PR #539, which is still open. ADJ glossary line 78.
4. The sweep writes one dated report under `<root>/.dev/sweeps/` (ADJ line 244). Its "sweep report JSON v1" is printed to stdout only and is not stored (ADJ line 131, fact E-05). The rule "a sweep adds exactly one report file" is NFR-001, pinned by two tests (ADJ glossary line 83).
5. The two JSON formats differ: the observer snapshot uses camelCase and `"UNKNOWN"` strings keyed by `dispatchId`; the sweep JSON uses snake_case and `null` keyed by `row_id` = `orca:<dispatch>`. ADJ line 131.
6. Shared words mean different things in the two programs (for example "stale" and "historical"). The mapping rule: "if a panel ever shows sweep rows it prints the sweep's words verbatim and labels the report age". ADJ line 253.
7. The debate judged at 78 percent that the sweep JSON v1 is a candidate carrier only for Orchestrator v2 and for a Coder#477 status record, "not for the observer"; it tied this to Q17 "no observer panel for sweep facts now". ADJ line 361 (row A-001).
8. The disagreement in the source debate (D-6): reviews 01 and 04 wanted the observer to read sweep facts eventually; review 05 said "optional, later, only if wanted". The settling fact is "the owner only". round2-rebuttal-V5.md line 69.
9. If the owner says yes, the first possible exchange is caller-captured sweep stdout in the coordinator's sweep pass, a Phase 2 item that needs the Q9 decision. round2-rebuttal-V5.md line 108.
10. Q9's recommended answer: "Not now. Phase 2: caller-side stdout capture first; relax NFR-001 only if a stored file is needed." ADJ line 779.
