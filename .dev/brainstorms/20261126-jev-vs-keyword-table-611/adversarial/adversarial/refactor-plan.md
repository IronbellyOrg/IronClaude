# Refactoring Plan

## Overview

- Base variant: A (`blind/variant-A.md`, original `variant-1-*.md`), combined score 0.9833
- Incorporated from: B (`blind/variant-B.md`) and C (`blind/variant-C.md`)
- Planned changes: 27 (18 from debate winners and merges, 9 from the invariant probe)
- Overall risk: Medium. Changes are additive requirements; the merged spec grows from about 1,800 to about 4,000 words.
- Status of inputs: the decision rule (sign test, 2 s median, 5 s slowest) is PROPOSED by another session, not AGREED. The merged spec carries it as a proposed rule-file content and keeps the gate closed. No number for the margin or latency is set by the spec itself.

## Planned Changes

Each entry: source, target in the base, rationale (debate or probe id), integration, risk.

**From the debate**

1. Folder name. Source: B C-009. Target: section 5. Replace `.dev/experiments/611-jev-vs-keyword-table/` with `.dev/research/jev-vs-keyword-table-611/`. Rationale: C-009 B, `.dev/README.md` lines 23 and 38. Replace. Low.
2. Retry policy. Source: B FR-016, C FR-006. Target: FR-016 and NFR-005. Replace "no retries in the scored run" with a pre-written policy: one rerun per failed prompt, never a rerun of the whole run; every attempt logged and counted against the cap; the failed attempt stays visible. Rationale: X-001 B, C-006 MERGE. Replace. Medium.
3. No-default rule file. Source: B FR-011, FR-012, NFR-007. Target: FR-014, FR-018. Add a frozen `decision-rule.md` holding Noul band operators, error and rerun treatment, latency limits, margin test, validity conditions; the scorer reads them and has no built-in default. A's conservative text (an unresolved error is not right and stays in the denominator) becomes the content. Rationale: C-005, X-002 MERGE. Restructure. Medium.
4. Proposed rule as content. Source: issue-summary.md "Decision rule as it stands". Target: section 4. Record the proposed rule as rule-file content marked PROPOSED: exact one-sided sign test on the prompts where only one arm is right, in integer arithmetic (pass when 20 times the tail count is below 2 to the power b+c); right means same type for a typed label and unset for an ambiguous or none-fit label, for both arms; median 2 s or less over each prompt's final answered attempt; slowest 5 s or less over all attempts, a timeout counting at its value; 10 s timeout; 90th percentile reported; Jev must pass both. The spec states it is a proposal and names no value as decided. Rationale: C-003, C-010. Insert. Medium.
5. Latency basis. Source: A FR-019 with rule. Target: FR-019. Keep A's two bases, align to the rule, add the 90th percentile and local-versus-remote labels (U-009). Open item recorded: median treatment of a prompt that fails twice. Merge. Low.
6. Two gates, comparison-scope. Source: C run gate, B gate order. Target: section 4. Replace the single gate with Gate 1 (before the table is applied or any Jev call: rule AGREED, labels and corpus frozen and hashed, owner words verbatim beside the interpretation, unclear unit or tie sent back) and Gate 2 (before the first live call: table answers stored and hashed, scorer and runner pinned with passing tests, spend bound verified, response contract check, the lead's go). Rationale: C-004 MERGE, INV-015. Restructure. Medium.
7. Persisted gate result and event log. Source: C FR-003, FR-009. Target: section 4, section 5. Add an append-only `events.jsonl` (owner input received, freeze, rule freeze, gate results, first request, run end, scoring, verdict), each linked to evidence; first request references the manifest. Rationale: U-008. Insert. Low.
8. Table answers before Jev, after Gate 1. Source: B FR-009, gate step 4; C. Target: new FR. Rationale: U-005. Insert. Low.
9. Corpus check in the scorer. Source: B FR-002, FR-003, T-01. Target: FR-002, tests. Scorer fails on a missing type, no ambiguous entry, no none-fit entry, duplicate id, missing provenance. Rationale: U-006. Merge. Low.
10. Append-only run ids and offline rescoring. Source: B NFR-008, FR-018, T-12. Target: NFR-005, new FR. A rescore under another rule file is labelled non-decisional and never replaces the original verdict. Rationale: U-007, C's critique. Insert. Low.
11. Per-request spend bound. Source: C cost cap, A NFR-001. Target: NFR-001. Before each request, including a rerun, a verified upper bound of that request's cost plus spend so far must fit the cap; if no bound can be shown, stop before sending. Keep the whole-run estimate as a second check. No concurrent-request machinery (calls run one at a time). Rationale: C-007. Merge. Medium.
12. Key secrecy layers. Source: A refuse-to-write, B redaction and folder scan, C minimisation. Target: NFR-003. Rationale: C-008 MERGE. Merge. Low.
13. Tests linked to requirements. Source: B T-01 to T-13. Target: section 6. Each test cites the FR it checks. Add tests listed in change 24. Rationale: S-003 B. Restructure. Low.
14. Section layout. Source: B. Target: sections 2 and 3. NFRs grouped under Cost, Privacy and key secrecy, Reproducibility, Maintainability; risks as a table. Rationale: S-001, S-002 B. Restructure. Low.
15. Verdict states. Source: C-002 MERGE. Target: FR-023. Three states: `JEV_BEATS_TABLE`, `NOT_CLEARLY` (valid run, rule not met), `RUN_INVALID` with a reason field. Keep A's invalid reasons. Merge. Low.
16. Owner words and interpretation. Source: C run gate, A item 6. Target: gate. Verbatim words kept beside the machine reading; a unit, denominator or tie that is unclear blocks the gate and goes back to the owner. Rationale: C-010. Merge. Low.
17. Corpus availability and shortfall. Source: C FR-001, A-001 QUALIFY. Target: FR-001, FR-002. Before the freeze, list the public sources and the achieved counts per label; a shortfall in ambiguous or none-fit cases is reported to the lead and is never padded. Insert. Low.
18. Issue updates recorded. Source: C FR-010. Target: FR-024. This work posts nothing to GitHub; the decision record carries the exact text and target issues (611, 609, 612) for the coordinator, and the coordinator's posted text and links are added afterwards. Insert. Low.

**From the invariant probe (HIGH items first)**

19. INV-001. Who may set AGREED. Target: gate. The rule file records who accepted, the verbatim words and the date; the scorer refuses any status other than AGREED; and before the first live call the lead types an explicit go in the terminal, quoted in the event log, naming the rule's hash. A relayed proposal is not the owner's words and must be recorded as such. Insert. Medium.
20. INV-002. Table answers frozen. Target: manifest, RUN_INVALID. `table-answers.jsonl` is hashed at storage and checked before scoring; a change after the first Jev result is RUN_INVALID. Insert. Low.
21. INV-003. Scorer pinned and tested. Target: NFR-004, Gate 2. Hash of the scorer and the runner recorded in the manifest with the git commit (the folder must be committed before the run); the test command `uv run pytest <path> -v` and its passing result recorded before Gate 2, because tests under `.dev/` are not collected by the repository's normal run. Insert. Medium.
22. INV-013. Labeller and table applier. Target: FR-011. The table applier is given the prompts only, never the labels, and is a different person or session from the labeller; if an AI session applies the table it is told to follow the prose as written, and the cue record is kept. Insert. Medium.
23. INV-014. Ambiguous and none-fit labels. Target: FR-003. The basis for an ambiguous or none-fit label is written before any arm runs and is not taken from the table's own two-row rule; the report gives accuracy separately for typed and for ambiguous or none-fit prompts, and flags a pass that rests only on the second group. Insert. Medium.
24. INV-017. Systemic failure. Target: verdict. RUN_INVALID, with no build or close decision on issue 612, when the key is rejected, a returned model id differs from the pin, or unresolved failures exceed a count the rule file must state before AGREED (no number is set here). Insert. Medium.
25. INV-004, INV-005. One cumulative spend ledger for the whole experiment that carries across run ids; "rerun" defined as one per prompt, and a whole new run needs a reason written before it starts. Insert. Low.
26. INV-008, INV-009, INV-010, INV-011. Duplicate text check (same text under two ids); Noul band operators at 0.3 and 0.7 stated in the rule file before AGREED; one median population and definition (even-count median and the 90th-percentile method stated); the achieved prompt count recorded, and a prompt swapped after table answers exist forces a new freeze. Insert. Low.
27. INV-012, INV-016, INV-018; open questions. Seen-by-table prompts reported both ways (kept from A); each Gate 2 input shown to pass or listed as not yet passed; the open-question list updated: remove the folder name and retry questions; add median treatment of a prompt that fails twice, the unresolved-failure count, Noul boundary operators, table method and applier, who labels. Merge. Low.

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base or a merge was kept |
|---|---|---|
| C-007 | C's reservation of "outstanding liability" for concurrent requests | Calls run one at a time; B and C advocates both accepted a per-request bound without concurrency machinery |
| C-003 | Imputing the 10 s timeout into the median for a prompt that fails twice | C's advocate noted this is a new proposal not yet agreed; recorded as an open item, not written as a rule |
| X-001 | A's "no retries in the scored run" | Dropped by A's own advocate once the rerun rule arrived |
| U-007 | B's open-ended rescoring | Kept only as non-decisional, so rule shopping cannot change the verdict |
| S-001 | C's unnumbered layout | Replaced by numbered, grouped sections |
| C-009 | `.dev/experiments/...` (base) and open name (C) | `.dev/README.md` lists `research/` and not `experiments/` |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 2, 3, 6, 19 | Medium | Policy wording moves from the spec to a rule file; a gap between the two could reopen X-002 | Revert to the base wording in the same section |
| 4 | Medium | Records a proposal that is not yet agreed; must not read as decided | Delete the PROPOSED block; the gate stays closed anyway |
| 11, 21, 22, 23, 24 | Medium | New requirements add implementation work to the plan | Each is a separate requirement and can be dropped alone |
| Others | Low | Additive | Remove the added requirement |

## Review Status

Auto-approved (non-interactive run). Timestamp: 2026-11-26T14:40:00+00:00.
