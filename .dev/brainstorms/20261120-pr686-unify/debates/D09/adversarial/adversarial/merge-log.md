# Merge Log

## Metadata
- Base: Variant 2 (CLAY paper), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/variant-2-original.md`
- Non-base source: Variant 1 (OURS paper), `variant-1-original.md`, plus `debate-transcript.md`, `invariant-probe.md`, `diff-analysis.md` (same folder)
- Plan: `refactor-plan.md` (9 planned changes, 4 rejected alternatives)
- Merge date: 2026-11-20
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/merged-output.md` (96 lines, under the 160 limit)
- Method: header stub first, then each section filled in plan order. The base was restructured to the required headings (the base had no "Who may write what" or "Rule text" sections).

## Changes Applied
### Change 1: Rewrite the claim as the agreed hybrid. Status: APPLIED
- Before (base): "The most visible and most reversible mark is one GitHub label, `hold:plan`, written by the poll and nothing else ... The write is narrow (add or remove one label, no comment, is tested)."
- After: "Adopt now: the read-only `plan_check(body)` and the `held_incomplete` skip. Allow later, as one named exception: the poll adds or removes one label ... behind the `issue.hold` grant ... NG-2 is amended ... Decision D2 is unchanged. Confidence: 92% on ... (C-001), 62% on ... (C-002)."
- Provenance: Base (original, modified) with Variant 1 Claim and Concession and Round 2 final positions. Location: `## Claim`.

### Change 2: Add the governing write rule, least privilege by actor. Status: APPLIED
- Before: no such section in the base.
- After: new `## Who may write what` with a five-row table (Worker, Poll, Per-repo init, Person, Coordinator or orchestrator) and the rule line citing WC-9, `claim.md:9`, R24.
- Provenance: Variant 1 Cited facts 4 and 6 merged per Change #2. The row for "Not adopted: coordinator writes the label" follows the "Changes NOT Being Made" table (C-002 OURS).

### Change 3: Correct the human-gate statement. Status: APPLIED
- Before (base fact 9): "The human approval that OURS leans on is not on master ... With no human gate on master, the plan check is the only thing between an empty issue and a launched worker."
- After (fact 11): master's poll still calls `predicates.approval_of` (`cycle.py:883`, `:998`, moderator verified); the PR 686 head has 0 references; the no-gate tree is the PR 686 head and design 681; the spec names a commit and a design.
- Provenance: Probe INV-002, debate C-007 and X-001. The PR 682 and issue 655 claims stay marked as Clay's paper, not re-read.

### Change 4: Fix the write count and the stateless wording. Status: APPLIED
- Before: "The write is narrow (add or remove one label)" beside a code description of three calls (create, add, remove); "Stateless-ish and idempotent"; the cost line said the poll gains write rights "and the `hold:plan` label must be created once per repo".
- After: two poll writes (add, remove); creation moves to the per-repo init (Claim, table, Mechanism 3, fact 2, rule 2); the cost line says the poll is not stateless because of the `holds` map; the gets-right line says "The poll still keeps a `holds` map, so it is not stateless".
- Provenance: Diff X-002 and C9 findings, Round 2 agreement that the poll must not create labels.

### Change 5: Add the cost side honestly. Status: APPLIED
- Before: two cost bullets (write rights and `test_hold.py`; `holds` map).
- After: five bullets adding `LabelWriter` about 87 lines, about 22 of 58 tests (rough), `hand_removed` state, live read, E1 to E4, eight audit reasons, store `state` 2 values and `plan_request` 5 values (corrected from "four states"), FU-3 token scope, and the unsized 4.11 rework.
- Provenance: Variant 1 Cited fact 8 (corrected) and the CLAY Round 2 cost list.

### Change 6: Add the unattended-wrong-write risk with a mitigation. Status: APPLIED
- Before: "A wrong write repeats each cycle until noticed (bounded by the retry-next-cycle rule and the call budget)."
- After: risk 1 with Likelihood Low, Impact Medium and mitigation (grant switch, dry-run, call budget, per-cycle failure memory); the idempotent-add part is credited to CLAY and the wrong-issue repeat stays. Risks 2 to 8 each carry likelihood, impact and mitigation.
- Provenance: Variant 1 Cited fact 7 and Risks, split per X-003. Note: the likelihood and impact ratings are the merge's reading of the debate, and the document says so in its source comment.

### Change 7: Add the spec lines from the probe's MEDIUM findings. Status: APPLIED
- Before: no rule section.
- After: `## Rule text` with 12 numbered one-line rules, each with a test hint where one exists: NG-2 amendment (1), no label creation and init creates both labels (2), `plan_check` before approval (3, INV-001), edit voids approval (4, R19, R36), document-level grant (5, INV-003), person-only `hold:backlog` (6), off state (7), placeholder sections empty (8, INV-004), body read limits (9, INV-007), one poll per repo (10, INV-008), failure counted once per cycle (11, INV-006), switch-on gate (12).
- Provenance: probe INV-001, INV-003 to INV-009. INV-005 (exact heading match) appears as a risk (risk 5), not as a rule, because the plan's rule list does not include a heading-match rule.

### Change 8: Record the single unresolved point. Status: APPLIED
- Before: base closed with "Weak point conceded" (lease and plan request depend on D07).
- After: `## Open point` records C-002 (dormant label-write code in PR 686 now or later), both sides' stated positions, 62% confidence, and the items that stay UNVERIFIED or deferred to D07.
- Provenance: Debate C-002. The base's "Weak point conceded" content moved into Mechanism item 5 and the table row for the coordinator.

### Change 9: Keep OURS' honest concession and fold the visibility finding in. Status: APPLIED
- Before: four gets-right bullets, the first calling the label "early, cheap, visible".
- After: six bullets; the check gap is credited as OURS' concession; visibility is stated as plausible, unmeasured and a tie that goes to OURS (75%); a hand-cleared label does not release the issue.
- Provenance: Variant 1 Concession and Round 2 rebuttals of both advocates.

## Post-Merge Validation
### Structural integrity
- Provenance comments are the first three lines; the nine required headings appear in the required order (grep result: lines 5, 7, 11, 25, 35, 50, 58, 70, 79, 94).
- Heading levels: one `#` title, nine `##` sections, no skipped levels.
- Every section carries one `<!-- Source: ... -->` comment (9 of 9). No `FILL:` marker is left. Zero em dashes (grep count 0).
- Length: 96 lines (limit 160). The "Who may write what" table has the required three columns, Actor, Allowed GitHub writes, Condition.

### Internal references
- Risk lines cite rules 7, 8, 9, 10, 11, 12 and facts 9 and 12; each resolves to the matching rule or fact (rule 7 off state, 8 placeholders, 9 body read, 10 one poll, 11 failure memory, 12 switch-on gate; fact 9 off state, fact 12 login and scope).
- The Claim's 92% and 62% match the debate scoring matrix. The Open point's 62% matches C-002.
- The `D:nnn` convention is defined at the top of Mechanism before first use. Facts cite `D:nnn` and plain file paths consistently with the base.

### Contradiction re-scan
- Base fact 4 said "a person always wins". Rewritten in fact 5 and the table: a hand removal does not release the issue (Round 2 concession). No remaining sentence claims otherwise.
- Base "stateless-ish" is gone; the costs and gets-right bullets both say the poll keeps a `holds` map.
- Base fact 9 ("no human gate on master") is replaced; no other sentence says master has no gate. Fact 11 and Mechanism item 1 agree that the check runs before the approval read.
- Base "bounded failure mode" is qualified in fact 8 and fact 9 (off state, no failure memory), and risk 1 and rule 11 point to the same fix. No remaining claim says the failure is fully bounded.
- Claim says the label write stays off until two tests pass; rule 12 and risk 4 say the same. The Open point does not contradict this: it asks only whether the dormant code ships in PR 686.
- Items kept UNVERIFIED: ruling 33 authority and the Jay comparison (fact 2), label write scope under cron (fact 12), who reads `hold:plan` (gets right, Open point), whether the init runs unattended (Open point), whether workspaces share a store (risk 7), the stranded label (fact 9, "inferred, not run"). Agent-reported probe items are labelled agent-reported.

### Notes
- Probe INV-010 (quadratic comment regex, LOW) is not in the plan and was not added. INV-009 appears in the table and rule 2.
- The base's CLAY facts about PR 651, PR 682 and issue 655 were not re-read by either advocate, and the document says so.

## Summary
| Measure | Count |
|---|---|
| Planned | 9 |
| Applied | 9 |
| Failed | 0 |
| Skipped | 0 |

"Changes NOT Being Made" respected: C-002 coordinator-writes-label (shown only as "Not adopted"), C-004 one-hour plan request and C-005 lease comment (moved out of scope into Mechanism item 5 and the table), and OURS fact 9 Jay comparison (kept only as an UNVERIFIED note on ruling 33, not used as evidence).
