# Q19: which of the reviewer's four asks comes first, in which program?

## The question (verbatim from the spec row)

"Which of the reviewer's four asks comes first, in which program?"
Source: merged-requirements.md section 3, row Q19 (line 546). ADJ Part 7 row Q19 (line 789) words it in full: "Which of the reviewer's four asks (Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse, summary and links) comes first, and in which program?"

## The spec's recommended answer

"Fleet Quilt or Decision Desk first, in the observer, after the note and the shared capture." "The note" is the contract note between the observer and the sweep (XC-05 draft, XC-07 linked and final); "the shared capture" is one read-only recorded session against live Orca (XC-03). Source: merged-requirements.md line 546; ADJ line 789.

## Default if unanswered

"PLAN INFERENCE: OB-09 does not start." Source: merged-requirements.md line 546.

## What it gates (work items, in words)

- OB-09 (deferred: observer release 3, the Decision Desk screen, and the first of the reviewer's four asks). Its conditions: (1) QUESTION-LINK (the gate for release 3: an authoritative mapping from a coordinator message to a worker's dispatch or worktree id) is established and recorded; (2) Q19 names the first ask and its program; (3) the release declares which contract it reads and that a human answer travels only through the coordinator; (4) every answer path is audited in the vocabulary of XC-08 (the trust vocabulary decision, Q16). Blocked by OB-06 (the PR that switches on the observer's coordinator-questions read), OB-02 (the owner's dated direction-selection record, AC-S), XC-05, Q19, Q17. merged-requirements.md line 257; graph rows 59 and 60 (lines 706, 707).
- Wave: W5 (the last wave). Line 546.

## Facts the question depends on

1. The four asks, from a reviewer's comment on issue #409 dated 2026-11-11T14:47Z (the comment author is not named in the sources read; UNVERIFIED): (1) Fleet Quilt, (2) Decision Desk, (3) Loop Detector or Mission Pulse (named steps with green, yellow, red), (4) a plain-English summary with issue and PR links. variant-5-original.md section 6 (lines 60 to 75); ADJ line 789. Review 01 also lists "click a session to open it" as a related ask (variant-1-original.md line 87, F-11).
2. Fleet Quilt, Loop Detector, Mission Pulse and Decision Desk are names of designs among the twenty synthetic design images of the #409 package. The built observer implements only Signal Bridge's worker ledger and the Attention Ledger's question panel. ADJ glossary line 93; ADJ line 187.
3. Status of each ask: Decision Desk is release 3, not built, behind QUESTION-LINK ("Not established"). Fleet Quilt is not built and in no release row. Loop Detector and Mission Pulse are not built and in no release row. The summary and issue or PR links are not built; the closest field is Orca's worker-reported `stage.activity` and `.detail`, shown only in the observer's inspector. variant-5-original.md lines 62 to 72; merged-requirements.md line 72.
4. What data each ask needs is not recorded for Fleet Quilt (UNVERIFIED; the sources read describe it only as a design name). For the summary, named steps and links, review 01 found: no field in the sweep JSON or report today; a deterministic summary option exists (the first line of the Orca Task brief, already read by the sweep, plus its `Command:` lines); named steps could come from the workers' handoff files with `worker_status` words; issue and PR links need a GitHub read the sweep does not make (a new allow-list and owner note) or an observer read of `gh pr list --head`. variant-1-original.md lines 84 to 87 (F-08 to F-11).
5. Review 05's recommendation (D7): settle D1 (whether the observer ever reads sweep data, the Q17 subject) and D3 first, then add one row per ask to the observer's `release-gates.md` with its data gate, "in the order the reviewer values (Fleet Quilt and Decision Desk first). First step: the owner picks the first ask." variant-5-original.md lines 250 to 254.
6. Release 3 also needs the questions read switched on (OB-06) and the owner's AC-S record (OB-02). merged-requirements.md graph row 59 (line 706).
7. The sweep (Orchestrator mode Phase 1, issue #339, PR #539 open) is read-only and "recommends nothing" (WC-16, ADJ glossary line 81). Phase 1 makes no GitHub read (variant-1-original.md line 85).
