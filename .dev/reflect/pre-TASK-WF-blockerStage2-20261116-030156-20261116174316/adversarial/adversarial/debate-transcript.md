# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Advocates: A1 (variant 1, sonnet), A2 (variant 2, haiku), A3 (variant 3, sonnet). Judge/scorer class: opus (different from every debater class).
- Round 1 persisted condensed by the orchestrator: every point verdict, every concession and every cited objection is kept; prose is shortened.

## Round 1: Advocate Statements

### A1 (variant 1, analyzer)
Position: card 1 holds the most concrete runtime gap (R1-1) and the safety-to-partial gap (R1-2); union of all cards is the best register; R1-3 to R1-5 minor.
Steelman of card 2: R2-1 (run-scoped ids, spec:352 vs plan:138) and R2-2 (plan:126 "blind table only" vs plan:28 and spec:512-516) are strong. Steelman of card 3: R3-1 (plan:56 "prints what it returns", plan:88 write then safety), R3-2 (spec:737 "the label is information"), R3-3 (rf-analyst at SKILL.md:479-480, 507-508, 819 not among the five templates).
Verified: grep of sc-implement-protocol for follow-up finds only refs/ledger.md:60; SKILL.md:192 prints notes files; spec:484 pointer row not built; spec:438 vs plan:102 and WORKER-CONTRACT.md:36; SKILL.md:192 is one physical line; no "unattended" in tech-research/SKILL.md.
Objections: R2-3 is not a plan defect (card says so); R3-1 "by construction" is overstated (stage1 plan:196 says the route "tags the row"); R3-3 unproven if the run owner supplies the fields; R2-2 partly mitigated by plan:132 (UNSET/NA).
Concessions: Task 8's "mostly reports skips" (plan:138) does not say there is no ledger; card 1 missed tasks 6-8 depth, run-scoped ids, blind-only inputs, tag persistence, tier source; R1-4 minor.

### A2 (variant 2, qa)
Position: two blocking measurement defects (R2-1, R2-2); concedes cards 1 and 3 add genuine omissions.
Steelman: card 1 follows record-to-consumption path; card 3 checks actual report producers. Verified R2-1 (plan:138 "one row id per line" vs spec:352 "run-scoped"), R2-2 (plan:130 "the blind table only" vs spec:501; stage1 plan:159 supplies inputs).
Objections: card 3 overstates C-005 and C-006 as certain (stage1 plan:196 "tags the row", stage1 plan:62 mandates LABEL=Outcome mappings); card 1's printed-list producer (C-011) not independently blocking (plan:72 directs the executor to print).
Concessions: missed implement pointer row, safety-status mapping, analyst-template gap; C-007 blocking only when an analyst supplies non-blocking findings; R2-3 traceability only.

### A3 (variant 3, refactorer)
Position: card 3 finds real gaps in the producer-to-ledger path; ranks R1-1 above its own follow-up note; R2-1 real but cheap to fix; R2-2 over-reads plan:126.
Verified: R3-3 (SKILL.md:479-480, 507-508, 819; 952 and 1003 LEGACY), R3-2 (spec:737, 739, SKILL.md:549), R3-1 on the plan's flow (plan:88 then plan:56; spec:932 T17), R3-6, R3-5.
Objections: R1-1 disclosed in part at plan:138 yet still a defect; R2-1 is a missing `run_id:id` qualifier (spec:339 carries run_id), a one-line fix; R2-2's parenthetical at plan:126 excludes consensus, grade, label and scale map, not code inputs, plan:132 implies the agents saw inputs; card 2 never read spec:438.
Concessions: R3-1 depends on whether stage 1's route mutates the ledger (unconfirmed); R3-4 overstates "after edits" since plan:59 checks `classify` in Task 2; R3-8 weak; the /sc:implement ledger gap is blocking, not a follow-up.

### Per-point positions (superior variant, confidence) after Round 1
| Point | A1 | A2 | A3 | Agreed |
|---|---|---|---|---|
| C-001 | V1 85 | V1 94 | V1 75 | yes V1 |
| C-002 | V1 62 | V1 93 | V1 65 | yes V1 |
| C-003 | V2 75 | V2 99 | V2 55 | yes V2 (A3: fixable format gap) |
| C-004 | V2 68 | V2 96 | V2 40 | yes V2 (A3: wording vs substance) |
| C-005 | V3 58 | V2 qualified 80 | V3 60 | yes V3, qualified (tag persistence unspecified) |
| C-006 | V3 68 | V2 83 | V3 65 | majority V3 |
| C-007 | V3 55 | V3 narrowed 95 | V3 75 | yes V3 |
| C-008 | V3 80 | V3 96 | V3/V2 60 | yes V3 minor |
| C-009 | tie V1/V3 85 | tie 95 | tie 80 | yes tie, minor |
| C-010 | tie 90 | tie 90 | tie 75 | yes tie, minor |
| C-011 | V1 60 | V2 85 | V1 50 | majority V1, low confidence |
| C-012 | none 65 | V2 qualified 97 | V2 55 | traceability only |
| C-013 | V3 75 | V3 90 | V3 75 | yes V3 minor |
| C-014 | V3 45 | V3 82 | V3 40 | yes V3 minor/wording |
| X-001 | V1 62 | V1 93 | V1 60 | yes V1 |
| X-002 | V3 62 | V2 83 | V3 60 | majority V3 |
| X-003 | V3 78 | V3 96 | V3 60 | yes V3 minor |

### Shared assumptions
- A-001: A1 QUALIFY, A2 QUALIFY, A3 QUALIFY (tasks follow a dependency graph; late failure is true only for scale-map and registry files, not for `classify` which Task 2 checks).
- A-002: A1 QUALIFY, A2 QUALIFY, A3 QUALIFY (Task 2 reads the real modules and writes the wiring artifact; behavior such as whether the safety route saves the tag is the real exposure).

## Round 2: Rebuttals (sequential A1, A2, A3; condensed by the orchestrator, every verdict kept)

### A1 (analyzer)
- Concedes R1-1 is a disclosed shadow-stage limit: plan:138 says "shadow ledgers come only from tech-research runs"; Task 3 acceptance only checks text; verdict MINOR (the printed line stays unconditional, that is the residue). C-011 minor.
- C-003 BLOCKING 80: spec:339 run_id, spec:352 "run-scoped"; plan:138 `--confirmed-misses <file>` "one row id per line" over many run folders cannot be resolved; a one-run fixture passes, real data fails; fix is a `run_id:id` form.
- C-005 BLOCKING 60 unless Task 2's required read of safety_route.py shows it saves the tag (stage1 plan:196 "tags the row"; nothing in stage1 Tasks 7/13 or any acceptance line says the tag is stored or tested; stage 2 `safety` "prints what it returns", plan:56; Task 8 counts rows "that lack the tag").
- C-006 minor 65: real row `| # | Severity | Section | Finding | Proposed Fix |` with CRITICAL/IMPORTANT/MINOR (tech-research SKILL.md:1147-1149; blocking gates SKILL.md:892, 900); stage1 plan:62 requires LABEL=Outcome pairs; executor can choose and a test can pin it.
- C-004 minor 65: plan:28 vs plan:126/130 do not contradict literally; agents' M, C, E answers come from agents who never saw the inputs; pin "blind table plus the supplier's inputs for that row".
- X-001 BLOCKING 70: spec:438 GR12 -> partial; Task 5 (plan:102) maps only `incomplete`; no key carries the signal; impact zero today (no live emitter).
- X-002 minor 65: `write` parses rows whose columns the plan never pins; failure sets `capture_state: incomplete` (plan:56), a counted capture failure at the stage 3 entry (plan:29), safe and visible.

### A2 (qa)
- Withdraws R2-3 as a plan defect (traceability only).
- R2-1 BLOCKING (95): ids are run-scoped (spec:352); plan:138 confirmations are bare ids; two runs can share FU-000001; repair is run_id:id with a colliding-id test across two runs; "blocking because a required result is ambiguous, not because the fix is expensive".
- R2-2 BLOCKING (90): plan:126 "The agents see only the blind table" and plan:130 "given the blind table only" mean M, C and E answers are text-only; stage1 plan:159 supplier and plan:28 require inputs for those questions; counting inputs at plan:132 shows availability, not that the agents received them; the acceptance lines can be met while the evaluation measures the text-only judge; neither a permitted enriched packet nor an enriched table is specified. Concedes plan:126's parenthetical names forbidden labels only.
- Concedes X-001 BLOCKING (spec:438 not covered by plan:102/106).

### A3 (refactorer)
- Concedes R3-1 "by construction" overstated (stage1 plan:194 Task 13 depends on Task 7; plan:125 lets safety_route.py import follow_ups; stage1 plan:196 "tags the row"). New evidence: none of Task 13's acceptance checks (stage1 plan:198-202) tests that the ledger holds the tag; stage 2 `safety` has no `--write` switch; plan:88 runs `write` before `safety`, so a row exists as a plain follow-up first. Verdict R3-1 MINOR (55): meetable, add one acceptance line.
- Concedes R3-2: agents' report tables have a Severity column (rf-qa.md:448, rf-qa-qualitative.md:883 `| # | Severity | Location | Issue | Required Fix |`); tech-research treats IMPORTANT as blocking (SKILL.md:900); residue: `write` has no family selector (plan:56), spec:744 says card_convert maps important to non-blocking, parser must accept two column layouts. Verdict MINOR (65).
- C-007 CONFIRMED and wider, BLOCKING (65), narrowed to phases 3 and 5: SKILL.md:952 and :1003 are LEGACY ("Do NOT use ... for Phase 6 QA"), so two of the five edited templates are dead; active Research QA (:864) and Synthesis QA (:911) edited; the two rf-analyst agents per gate use the prompt at :819 (not edited) and the rf-qa-qualitative agent per gate (:483, :511) has no embedded template; three of five reviewers per gate never get `rests_on`/`why not blocking`; analyst format is bullets under "Compiled Gaps" (rf-analyst.md:195-202): if the parser reads only tables, analyst non-blocking items vanish; if it reads bullets, GR2 refuses them; either way phase 3 and 5 ledger volume (a stage 2 exit number) is undercounted; Task 4 and T9 check only five templates so they pass anyway. Lite depth runs no analysts (SKILL.md:400, 404).
- C-001: reverses her Round 1 concession: MINOR (60). plan:138 discloses the tech-research-only limit; but Task 3's printed line "recorded and not filed" is unconditional, so in a zero-ledger run a reader believes follow-ups were captured; the stated reason at plan:138 ("skips code deliverables") is not the main one (no input at all). Fix: make the line conditional.
