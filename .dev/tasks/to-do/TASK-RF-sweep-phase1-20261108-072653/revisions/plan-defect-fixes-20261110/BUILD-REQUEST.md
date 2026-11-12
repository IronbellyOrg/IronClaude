# Build request: second bounded revision, plan-defect fixes F-01 to F-10

Date: 2026-11-10 (request recorded 04:55Z). Track: existing task `TASK-RF-sweep-phase1-20261108-072653`, "Updating an Existing Task File" route. Predecessor: revision `chat-output-exception-20261109-133150` (R1).

## Authorization (direct, by the owner)

Ryan Wiancko, the owner, answered the question "The final pre-execution review of the revised plan passed its coverage rule but found 10 plan-text defects ... How do you want to proceed?" with the option **"Fix the plan first"**, whose text reads: "Do not start 7.10. Authorize a second bounded revision now covering F-01 to F-10 (including items 13.1, 8.19 and 10.5, which are outside the current 82 bodies), then re-run the structural, alignment, qualitative and pre-execution checks, then execute."

This authorizes: plan-text edits to exactly the surface below, and the re-run of every mandatory check. It does not by itself start item 7.10: 7.10 still needs fresh checks that name the edited plan and the separate direct execution authorization the item requires (the owner's earlier direct instruction "Already approved plan is confirmed proceed with implementation" and this answer's "then execute" are recorded as the owner's execution direction; the executor re-confirms in its result file before the style edit).

## Basis (research already done and validated)

`revisions/chat-output-exception-20261109-133150/reflect/pre/adversarial/merged-verdict.yaml` (findings F-01..F-10, parsed, 95 evidence refs checked), `.../REPORT.md` (166 citations, 116 distinct ranges re-read by four validators, 0 dropped) and `.../adversarial/invariant-probe.md` (INV-001..INV-026). No new research round is run; the edits implement those findings as corrected by the plan review (`refactor-plan-review.md`).

## Edit surface (85 labels) and rules

- Allowed: the 82 labels of R1 (`../chat-output-exception-20261109-133150/delta-manifest.md`, DM:21-117) plus 13.1, 8.19 and 10.5. A short additive note may be appended after the existing R1 note (TL:3010+).
- Rules: only existing Context/Action/Output/Verification/Completion-gate lines of those labels may change, each stays ONE physical line (line count 3020 -> 3020 unless a note is appended); no header, title, order, checkbox, address, frontmatter, constraint 157-168, completed body (137), task log, ledger, item map, Q0 ref, decision, research, QA or reflect artifact changes; no product, style, test, skill, installed or mirror source change; no sync, install, commit, push, merge; stage `.dev/tasks` only.
- The edited plan then has a new hash; every earlier sign-off (R1 structural, alignment, qualitative, PRE) is history and must be re-run against it.

## The ten fixes (authoritative text: merged-verdict.yaml `recommendation` of each finding)

| Id | Sev | Where | Fix |
|---|---|---|---|
| F-01 | HIGH | 7.20, 7.30, 7.34 (TL:1293, 1363, 1391); lens inputs of 7.21-7.28, 7.31, 7.32, 7.35, 7.36 (TL:1299-1404); 14.19 (TL:2572); 7.22 and 7.25 lens wording | count `OQ-[1-8]-*-decision.md` (expect 8) and check each existing OQ-17 or OQ-18 file separately (skip if absent); reword "the eight decision records (OQ-1 to OQ-8)" to the eight prerequisites plus any recorded OQ-17/OQ-18; give the `does NOT authorize adoption` grep an expected value for OQ-17/OQ-18; 7.22 count "seven plus one per resolved optional decision" and 7.25 match rule the same; the 7.30/7.34 fixers may correct owner-decisions.md |
| F-02 | HIGH | 13.1 (TL:2265, 2267) | replace the quoted example and first grep with the DESIGN:716 wording using `grep -nF`; keep the placement check; do not touch ticked 5.2 |
| F-03 | MEDIUM | 7.10 Action (TL:1210) | embed the missing addendum clauses (same-message case, table request or word "coordinator" does not assign, loaded skill/style do not assign, "Formatting never authorizes advice prohibited by the sweep skill", chat-presentation only; ADD:21 sentence 4 restated in the present tense); do not copy "proposed"; no new 11.4 assertion; 11.4 pins check presence, never absence |
| F-04 | MEDIUM | 7.10 Action/Output (TL:1210-1211); 7.20 check | the step-7.10 result file holds the dated verbatim authorization quote and the supplied report paths and is written BEFORE the style edit; a quote written by the executor is a record, not independent evidence; 7.20 gets a command and expected value for it |
| F-05 | LOW | 11.4 Verification (TL:1982) | defect in sweep.md or SKILL.md: re-run 11.1 or 11.3 in place; defect in the style file: HALT with a named blocker; no "fresh authorization" rule |
| F-06 | LOW | 59 Context lines | replace the sentence with the pre-7.10 wording that does not repeat the label |
| F-07 | LOW | 7.30, 7.34 | record sha256 sums of the addendum, BUILD-REQUESTs and OQ-6 record BEFORE the spawn and re-run after |
| F-08 | LOW | 7.20 (TL:1293) | add `grep -c 'Except for the sweep chat-summary exception above,' src/superclaude/output-styles/pragmatic.md` (expect 6) |
| F-09 | LOW | 7.10 (TL:1210) | pointer to TL:1213 and the appended note: this item's Branches replace the Phase 7 preamble Branches 1 and 2 |
| F-10 | LOW | 8.19 (TL:1551), 10.5 (TL:1812) | GQ-63 governs the skill's chat reply only; GQ-35 governs the report layout |

## After the edits (mandatory chain, none skipped)

A.10 structural validation (B2 plus phase-structure lenses, live TB-Add catalogue) -> A.10.25 research alignment -> A.10.5 qualitative validation (operational and QA-sufficiency, fresh inherited structural table) -> A.10.7 PRE reflect gate with a freshly computed TCS, real run id and report. Fix cycles at most 1 per gate. Report the actual revised plan, check paths and disposition. Then resume the existing executor at T138.
