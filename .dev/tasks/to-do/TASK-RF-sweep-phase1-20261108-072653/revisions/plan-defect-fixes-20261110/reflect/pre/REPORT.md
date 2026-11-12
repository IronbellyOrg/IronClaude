# Reflection report: sc:reflect UC-1 pre-execution, run 4, second bounded revision (plan-defect fixes F-01 to F-10)

```yaml
run_id: reflect-pre-20261110T0540Z-TASK-RF-sweep-phase1-run4-plan-defect-fixes
mode: pre
tier_reached: 2
depth: deep
tcs: 1860
status: partial   # adversarial convergence_status BLOCKED_BY_INVARIANTS; see Findings M-01 and M-02
plan_sha256: eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99
spec_sha256: e4a06d0cf1c2e81df1c61138587a511c5ccd065cd896a42bb6f04ab329afacf3
citations_total: 132
citations_distinct_ranges: 81
citations_mechanical_failures: 0
citations_revalidated: 132
citations_dropped: 0
coverage_pct: 1.0
coverage_pct_union: 0.99
```

## 1. Verdict

The default path of the edited plan is sound and 7.10 may start once its own conditions hold (fresh structural, alignment, qualitative and PRE checks naming the plan, and the separate execution authorization). Before execution reaches 7.17, the owner should decide on M-01 (a new bounded authorization naming 7.17, including the approval follow-up of INV-R4-003) and accept M-02 by name, or accept both as a known conditional gap that needs a later plan revision if the OQ-17/OQ-18 branch fires. M-03 (MEDIUM) and the LOW findings M-04 to M-08 are inside the 85 labels and can be fixed in one line-stable pass; M-02, M-06, M-08 and the 14.x part of M-03 need owner acceptance by name. Any edit requires re-running the structural, alignment, qualitative and PRE checks.

Findings: HIGH 2, MEDIUM 1, LOW 6 (total 9). Authorization split: {'inside_85': 7, 'outside_needs_new_bounded_authorization': 2}.

Convergence: primary reading 29 of 31 diff points agreed (S 7, C 7, X 6, A 9; stated prose positions counted) = 0.935; strict reading (POINT lines only, silence = no position) 24 of 31 = 0.774; cross-check over the 34 S/C/X/U points 32 of 34 = 0.941. Threshold 0.80 met on the primary reading, not on the strict one. Unagreed: X-005 (winner name tied, disposition agreed) and A-006 (one stated position). Status: BLOCKED_BY_INVARIANTS.

## 2. Findings

| Id | Severity | Scope | Location | Claim |
|---|---|---|---|---|
| M-01 | HIGH | outside: needs new bounded authorization | TL:1274 (7.17 Verification) against TL:1272 (step 3 resume) and TL:1275 (Completion gate); TL:1270 (Action step 1, no skip when the decision file already exists) | When the owner allowlist branch fires, item 7.17 halts unticked, and the task skill resumes at the first unchecked item, so the 7.17 Verification is read after step 3 has set the decision record RESOL... |
| M-02 | HIGH | inside the 85 allowed labels (owner acceptance by name advised: 7.24 is not one of F-01 to F-10) | TL:1321 (7.24 Action, read-only safety lens prompt); TL:1271 (7.17 step 2 follow-up list, which omits 7.24); halt chain TL:1363, TL:1384, TL:1412, TL:1415 | The 7.24 safety lens prompt requires, with no condition, that every command in readonly-probe.md is one of templates 1 to 8, that run-current --json was never run and that ALLOWED_ORCA holds ten templ... |
| M-03 | MEDIUM | inside the 85 allowed labels (7.30 DM:32, 7.34 DM:35; the 14.x parity part is outside F-07, owner acceptance by name) | TL:1363 (7.30 Action), TL:1391 (7.34 Action); same pattern, pre-existing, at TL:2614, 2642, 2705, 2733 (14.25, 14.29, 14.38, 14.42) | Items 7.30 and 7.34 record the pre-spawn sha256 sums of the four authority files in fix-log-cycle1.md and fix-log-cycle2.md, the same path the fix agent is told to write its fix log to. An instructed ... |
| M-04 | LOW | inside the 85 allowed labels | TL:1363 (7.30 Action re-run list), TL:1391 (7.34 Action re-run list) against TL:1293 (7.20 authorization check) | The 7.30 and 7.34 fixers may edit the step-7.10 result file that holds the execution authorization section, but their post-fix re-run lists repeat the other 7.20 checks and leave out the 7.20 authoriz... |
| M-05 | LOW | inside the 85 allowed labels (DM:21) | TL:1210 (7.10 Action, Branch 2), TL:1211 (7.10 Output); checked by TL:1293 | Item 7.10 Branch 2 says to write the authorization section first and then edit the style file, but it names no rule for a resume or a retry after a failed bounded check: whether to skip an existing se... |
| M-06 | LOW | inside the 85 allowed labels (DM:21); the two omitted clauses are outside the F-03 list of BR:27, so owner acceptance by name is advised | TL:1210 (7.10 Action) against ADD:17, ADD:19 and BR:27 | The 7.10 Action embeds most addendum clauses but leaves out the ADD:17 clause do not reconstruct role from files or history and the ADD:19 clause never print a fabricated successful summary or hide an... |
| M-07 | LOW | inside the 85 allowed labels for 7.20 (DM:23); the root ambiguity in BR:9 is outside the plan | TL:1293 (7.20 authorization check); root cause BR:9 (outside the plan) | The 7.20 authorization check matches a quote the executor itself writes against the authorization section of the second revision request, whose own text points both ways: it says it does not by itself... |
| M-08 | LOW | inside the 85 allowed labels (DM:73, DM:76; owner acceptance by name advised: not one of F-01 to F-10) | TL:2384 (13.18 Action), TL:2412 (13.22 Action) | The docs-gate fix agents in 13.18 and 13.22 may edit the docs, and DESIGN lives under docs/; DESIGN immutability there rests on one prose sentence with no sha256 check before and after the spawn, unli... |
| M-09 | LOW | outside: needs new bounded authorization | TL:1267 (7.17 Context), TL:2991 (OQ-17 entry), TL:2992 (OQ-18 entry) against DESIGN:557, DESIGN:559, DESIGN:993, DESIGN:995 | The 7.17 Context and the OQ-17 and OQ-18 open-question entries cite DESIGN lines 550, 552, 971 and 973 for sentences that now sit at DESIGN:557, 559, 993 and 995. The quoted text is intact and findabl... |

### M-01 (HIGH): unsound-check

Condition: conditional on the 7.17 owner allowlist branch firing (outcome (a) a cursor field captured, or (b) run-current needing --json), for an owner approval and a refusal alike; no effect on the default path

Tag: Grounded (the text of TL:1270-1275, TL:195 and SK:535); [INFERRED] consequence, conditional on the branch firing, whose likelihood is unknown (DESIGN:995 gives the behaviour when no cursor template exists). Location: TL:1274 (7.17 Verification) against TL:1272 (step 3 resume) and TL:1275 (Completion gate); TL:1270 (Action step 1, no skip when the decision file already exists). Authorization: outside: needs new bounded authorization.

Claim: When the owner allowlist branch fires, item 7.17 halts unticked, and the task skill resumes at the first unchecked item, so the 7.17 Verification is read after step 3 has set the decision record RESOLVED, filled Chosen:, Decided by: and Decision source:, and cleared the halt. The Verification then demands status: PENDING, the empty owner lines and a halted task, while the Completion gate demands no open HALT, so the two cannot both hold, for an approval and a refusal alike. On the resume the literal Action step 1 would also write a PENDING decision file again over the RESOLVED one (O-001, folded). Every exit is a failure under the caller scale: a silent reinterpretation of the Verification, the task skill generic rule that ticks a blocked item with its check unmet (a required check lost), or a stop that names no blocker.

Evidence:

- `TL:1274`: "When the owner allowlist branch fires, confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines"
- `TL:1274`: "and that the task is halted (frontmatter `status` and `blocker_reason` set by the HALT rule) before any step 1.2 item runs"
- `TL:1272`: "it sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to "🟠 Doing", and clears `blocker_reason`"
- `TL:1275`: "The facts file is written with no open HALT."
- `TL:1270`: "1. The branch first writes a decision file `phase-outputs/plans/OQ-<n>-<topic>-decision.md` under the task folder"
- `TL:1270`: "step 1 appends no second row."
- `TL:195`: "STOP, and do not tick the item."
- `TL:1266`: "- [ ] **7.17 — Record the 1.0a facts the code needs (L1)**"
- `SK:535`: "Scan for the first `- [ ]` item. This is where execution resumes."
- `SK:183`: "mark the item `- [x]` with a note in Task Log explaining what was blocked and why, then continue to next item."
- `TL:1271`: "2. An owner approval triggers this follow-up work: a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate"
- `TL:1271`: "and a re-run of the R5 review gate (6.5 to 6.22) over the new edit."
- `TL:1011`: "- [x] **6.5 — QA r5, agent 1 of 9: rf-qa, template-conformance lens (report-only)**"
- `TL:1130`: "- [x] **6.22 — QA r5: gate decision (L5, proceed or HALT)**"
- `SK:537`: "Do NOT re-execute any `- [x]` items"
- `TL:3016`: "no new checkbox/task heading/numbered task"
- `TL:3016`: "This note is not an executable checklist."
- `BR:17`: "Allowed: the 82 labels of R1 (`../chat-output-exception-20261109-133150/delta-manifest.md`, DM:21-117) plus 13.1, 8.19 and 10.5."
- `BASE:1274`: "When the owner allowlist branch fires, confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING`"

Fix: Needs a new owner authorization that names item 7.17, because 7.17 is not one of the 85 allowed labels. Inside that extension: (1) split the 7.17 Verification into a first-halt record and a completion check: the first-halt proof becomes history (the one Execution Log row counted by the existing grep, which must still return exactly 1 per decision file), and at completion each written decision file must be status: RESOLVED with Chosen:, Decided by: and Decision source: filled, the refusal recorded in 1.0a-facts.md or the approval follow-up done, and no open HALT; a record still PENDING must block completion, since both outcomes can fire. (2) In Action step 1, skip writing the decision file when it already exists and reuse it with its owner fields intact, so a resume adds no second HALT (PENDING) row. (3) Keep the Verification on one physical line. (4) The same extension must also cover the approval follow-up of TL:1271: the DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate does not exist in the plan, and the R5 re-run of ticked items 6.5 to 6.22 cannot re-execute ticked items, so the owner either authorizes how those are created or accepts that an approval needs a later plan revision. An appended note alone is not a fix (TL:3016).

Verifier: Walk three cases against the edited 7.17 text: no optional outcome; an outcome fired and refused; an outcome fired and approved with the follow-up in place. Each completed case satisfies the Verification and the Completion gate together; a case with one record still PENDING cannot complete; after a resume the 7.17 HALT (PENDING) row grep still returns exactly 1 per decision file.

Notes:
- Severity votes in Round 2: H / H / H (unanimous). Origin pre-existing: TL:1266-1275 are byte-identical to BASE (line hashes compared in this step), and no 7.17 row exists in DM.
- INV-R4-003 (HIGH, UNADDRESSED in the probe) is carried here as fix part (4). It was raised in Round 2 by two advocates (R2v1:45, R2v3:15) and checked: grep -n DESIGN edit item on TL prints only lines 1268 and 1271.
- Does not block starting 7.10 (TL:1208 comes before 7.16 and 7.17). The Tier 1 card did not raise it; its verified_ok claim that the branch is coherent end to end did not test TL:1274 (diff-analysis X-001).
- The task skill line SK:538 (If an item output file exists, that work is done) softens the Action re-run but not the Verification of an unticked item (diff-analysis A-003).

### M-02 (HIGH): unsound-check

Condition: conditional on (i) step 1.0a showing outcome (a) or (b), (ii) the owner approving (a refusal keeps ten templates), (iii) the approval follow-up landing before the 7.21-7.28 panel, and (iv) the lens agent obeying Each breach is BLOCKING; unconditionally MEDIUM; no effect on the default or refusal path

Tag: Grounded (TL:1321, TL:1271, DESIGN:557, DESIGN:559); [INFERRED] the approved re-capture lands in readonly-probe.md (from TL:1263 and TL:1271). Location: TL:1321 (7.24 Action, read-only safety lens prompt); TL:1271 (7.17 step 2 follow-up list, which omits 7.24); halt chain TL:1363, TL:1384, TL:1412, TL:1415. Authorization: inside the 85 allowed labels (owner acceptance by name advised: 7.24 is not one of F-01 to F-10).

Claim: The 7.24 safety lens prompt requires, with no condition, that every command in readonly-probe.md is one of templates 1 to 8, that run-current --json was never run and that ALLOWED_ORCA holds ten templates, and it makes each breach BLOCKING. After an owner-approved OQ-17 or OQ-18 change, the approved re-capture and the eleventh or changed template breach up to three of those checks, although the 7.24 Context (changed by the second revision) now hands the lens the OQ-17/OQ-18 record. The 7.30 and 7.34 fixers must leave a finding that needs the owner or a new capture OPEN, so the decisions gate ends on a monotonicity HALT or the hard cap and cannot record Decisions gate: PASS without a plan edit. Item 7.24 is not on the 7.17 step 2 follow-up list.

Evidence:

- `TL:1321`: "Prove or disprove that every command in readonly-probe.md is one of templates 1 to 8 of DESIGN 7.3 or a file read, that no forbidden token (worker-read, gate-list, check, inbox, --include-remote, git stash, run-current --json) was run"
- `TL:1321`: "that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10"
- `TL:1321`: "Each breach is BLOCKING."
- `TL:1320`: "plus any OQ-17 or OQ-18 decision record in that folder that item 7.17 wrote"
- `TL:1271`: "the 8.10 and 10.3 count source changed from the literal 10 to the approved count recorded in the 1.0a facts file; the 7.16 forbidden list and its grep (item 7.16 Context and Verification) updated to allow the approved argv and a re-capture of it"
- `DESIGN:559`: "it is added only after step 1.0a captures the cursor field, as one extra template"
- `DESIGN:557`: "that is a template change and needs the same owner note as any other allowlist change"
- `TL:1363`: "it may never change a decision's `Chosen:` line or re-run a live Orca command. A finding that needs the owner or a new capture is left OPEN with that reason."
- `TL:1384`: "(b) Monotonicity: if `|F_1| >= |F_0|`, write `[HALT-MONOTONICITY] |F|=<n>`"
- `TL:1412`: "and escalate the open BLOCKING and MAJOR findings to the user"
- `TL:1415`: "`Decisions gate: PASS` (at any cycle) is recorded."
- `TL:1272`: "8.10 then keeps `ALLOWED_ORCA` at exactly 10"
- `TL:1363`: "`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`, the fixtures under `tests/sweep/fixtures/`"
- `TL:1041`: "that step 1.0a runs only templates 1 to 8"
- `DM:27`: "| 7.24 | Read-only safety lens | Add scoped inputs; distinguish build-time Markdown edit from runtime writes/probes. |"
- `BR:7`: "Authorize a second bounded revision now covering F-01 to F-10"
- `BASE:1321`: "that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10"

Fix: Inside the 85 labels (DM:27), but 7.24 is not one of F-01 to F-10 (BR:7), so list this edit for owner acceptance by name. Replace the unconditional checks in the 7.24 lens prompt with one conditional clause that names all three: when the 7.17 owner allowlist branch was approved, check the readonly-probe.md commands against templates 1 to 8 plus the approved re-capture, the forbidden tokens minus the approved argv, and ALLOWED_ORCA against the approved count; read the approval from the RESOLVED OQ-17 or OQ-18 record (Chosen: and Decision source: quoting the owner), which the fixer may not change, and require 1.0a-facts.md to match that record; with no approval or with a refusal, keep the ten templates and the original forbidden list. Keep the line one physical line and keep every halt at TL:1384 and TL:1412 as written. Adding 7.24 to the 7.17 step 2 follow-up list rides with the 7.17 extension of M-01, because 7.17 is outside the 85. Do not edit the ticked R5 review items 6.5 to 6.22.

Verifier: Walk five cases through the edited 7.24 prompt: default path; refusal; approved cursor template (outcome a); approved run-current --json (outcome b); both approved. With the RESOLVED record and a matching 1.0a-facts.md the lens PASSES each case. The same argv or count change FAILS when the OQ record is absent, PENDING or refused, or when 1.0a-facts.md differs from the record.

Notes:
- Severity votes in Round 2: H / M / H. The V2 advocate gave MEDIUM (owner handling is a named category of OPEN work, R2v2:19); CONS 4.1 kept HIGH because a correct approved run cannot record Decisions gate: PASS without a plan edit, and a plan revision is a workaround for every defect.
- INV-R4-011 (HIGH, PARTIAL in the probe) is closed in this fix text: the one-clause restatement proposed in the diff analysis replaced only the ten-template and run-current rules and left the templates 1 to 8 probe check, which an approved re-capture also breaches.
- INV-R4-009 (MEDIUM): the 7.30 fixer may edit 1.0a-facts.md (TL:1363) but never a Chosen: line, so the approval is anchored in the RESOLVED OQ record.
- INV-R4-012 (MEDIUM): the base card sub-fix Apply the same qualification to the reused R5 review inputs is dropped; ticked 6.9 (TL:1041) keeps that step 1.0a runs only templates 1 to 8 as history.
- Origin pre-existing: TL:1321 is byte-identical to BASE; the second revision changed only the Context line TL:1320. Does not block starting 7.10.

### M-03 (MEDIUM): guard-evidence-placement

Tag: Grounded (TL:1363, TL:1391); [INFERRED] the loss needs an instructed write that replaces the file, or a resume. Location: TL:1363 (7.30 Action), TL:1391 (7.34 Action); same pattern, pre-existing, at TL:2614, 2642, 2705, 2733 (14.25, 14.29, 14.38, 14.42). Authorization: inside the 85 allowed labels (7.30 DM:32, 7.34 DM:35; the 14.x parity part is outside F-07, owner acceptance by name).

Claim: Items 7.30 and 7.34 record the pre-spawn sha256 sums of the four authority files in fix-log-cycle1.md and fix-log-cycle2.md, the same path the fix agent is told to write its fix log to. An instructed write of that file can remove the only durable baseline, and a resumed session cannot rely on chat memory, so the PASS line for all four sums unchanged has nothing to compare against. An honest executor without a baseline cannot append PASS, so the failure is fail-closed and a correct uninterrupted run does not fail. The sentence also puts the after-return re-check before Then spawn, and no action is named for a changed sum.

Evidence:

- `TL:1363`: "record the output of `sha256sum .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md"
- `TL:1363`: "in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md` (hash only the OQ-6 record"
- `TL:1363`: "Write a fix log listing each finding id, the change, and the `file:line` after the change."
- `TL:1363`: "and the output path `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md`"
- `TL:1363`: "after the agent returns, re-run that command first and append a PASS line only when all four sums are unchanged. Then spawn ONE `rf-qa` agent"
- `TL:1391`: "in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle2.md` (hash only the OQ-6 record"
- `TL:1391`: "and the output path `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle2.md`"
- `TL:1365`: "every appended re-check line is PASS. If the fix agent fails to return twice, log the blocker in `### Phase 7 Findings` and stop."
- `TL:1210`: "because a resumed session does not remember the chat"
- `TL:2614`: "record the output of `sha256sum docs/designs/orchestrator-mode.md"
- `DM:32`: "| 7.30 | Serialized fix cycle1 |"
- `DM:35`: "| 7.34 | Serialized fix cycle2 |"
- `DM:100`: "| 14.25 | Serialized final fix cycle1 |"
- `BR:31`: "| F-07 | LOW | 7.30, 7.34 |"

Fix: In 7.30 and 7.34, write the pre-spawn sums to a separate orchestrator-owned file (for example qa/decisions/sha256-before-cycle1.txt and sha256-before-cycle2.txt) that is not passed to the fix agent; if that file already exists on a resume, do not re-record, compare against it; put Then spawn before the after-return re-check; on a changed sum write a FAIL line, log it in Phase 7 Findings and stop. Keep the PASS or FAIL lines in the fix log (TL:1365). The same weakness at 14.25, 14.29, 14.38 and 14.42 is inside the 85 (DM:100, 103, 110, 113) but outside F-07 (BR:31), so a parity edit needs owner acceptance by name; it may also add the second revision request to the 14.x sum lists (Tier 1 L5).

Verifier: After 7.30 runs, test -s qa/decisions/sha256-before-cycle1.txt exits 0, and the file is byte-identical after the fix agent writes fix-log-cycle1.md; a simulated resume between the spawn and the re-check leaves the sums file unchanged; grep -c sha256-before on TL prints 2 (TL:1363 and TL:1391; 0 today).

Notes:
- Severity votes in Round 2: L / M / M. The V1 advocate withdrew its premise that an ordinary Write replaces the file as unproven (R2v1:96); CONS 4.3 kept MEDIUM: real impact with a workaround (the orchestrator still holds the sums in an unresumed session).
- Origin: introduced by the second revision at 7.30 and 7.34, copying the 14.x house pattern; BASE has sha256sum only on lines 2614, 2642, 2705 and 2733.
- INV-R4-015 (MEDIUM): without the do-not-re-record rule a resumed 7.30 would re-take the sums after the fixer ran and the compare would pass trivially.

### M-04 (LOW): missing-check

Tag: Grounded. Location: TL:1363 (7.30 Action re-run list), TL:1391 (7.34 Action re-run list) against TL:1293 (7.20 authorization check). Authorization: inside the 85 allowed labels.

Claim: The 7.30 and 7.34 fixers may edit the step-7.10 result file that holds the execution authorization section, but their post-fix re-run lists repeat the other 7.20 checks and leave out the 7.20 authorization-section check, so a fixer edit that removes, duplicates or alters that record is not re-checked in the fix cycle.

Evidence:

- `TL:1363`: "For the bounded exception only, also permit `src/superclaude/output-styles/pragmatic.md` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-7.10-style-exception.md`"
- `TL:1363`: "`grep -c 'Except for the sweep chat-summary exception above,' src/superclaude/output-styles/pragmatic.md` (expect 6), and the sha256 sums recorded before the spawn (all unchanged)"
- `TL:1391`: "For the bounded exception only, also permit `src/superclaude/output-styles/pragmatic.md` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-7.10-style-exception.md`"
- `TL:1293`: "run `grep -c '^## Execution authorization (verbatim)' .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-7.10-style-exception.md`, expect 1, then read that section"

Fix: Add to the 7.30 and 7.34 re-run lists the full 7.20 authorization check: the heading grep (expect 1) and the read-and-match step against the same authority as TL:1293. A heading count alone is not enough, because the count stays 1 when the quote is changed in place, and a sha256 of the section would need an extraction command the plan does not define.

Verifier: grep -c "Execution authorization (verbatim)" on TL prints 5 after the fix (lines 1210, 1211, 1293, 1363, 1391; 3 today); in a simulated fix cycle that edits the quote, the re-run writes FAIL.

Notes:
- Severity votes in Round 2: L / L / L. Introduced with the second revision re-run list (F-07, F-08).
- INV-R4-020 (LOW): V1 suggested a sha256 of the section; replaced by the read-and-match step.
- V1 claim without detection was called too categorical by its calibrator (later verifiers re-check earlier PASS checks); the gap is in the fix cycle itself.

### M-05 (LOW): missing-rule

Tag: Grounded for the text; [INFERRED] for the duplicate (a possible reading, not a required one). Location: TL:1210 (7.10 Action, Branch 2), TL:1211 (7.10 Output); checked by TL:1293. Authorization: inside the 85 allowed labels (DM:21).

Claim: Item 7.10 Branch 2 says to write the authorization section first and then edit the style file, but it names no rule for a resume or a retry after a failed bounded check: whether to skip an existing section, to verify rather than re-apply an existing style edit, and where the before excerpts come from. The Action already tells a resumed session to look for the section and the Output says later content is appended, so a duplicate section is a possible reading, not a required one.

Evidence:

- `TL:1210`: "look first for the `## Execution authorization (verbatim)` section in the result file named in Output, because a resumed session does not remember the chat"
- `TL:1210`: "and only after first writing the dated verbatim text of the owner's separate execution authorization"
- `TL:1210`: "On failure log negative evidence in Phase 7 Findings and remain incomplete."
- `TL:1211`: "with the `## Execution authorization (verbatim)` section written first (later content is appended below it, never overwriting it)"
- `TL:1293`: "`grep -c 'Except for the sweep chat-summary exception above,' src/superclaude/output-styles/pragmatic.md`, expect 6, one per separate later restatement line"
- `TL:3020`: "Keep T138's original start `a09f6a12b0dce12e63b5b781a10a7be5446be367`"
- `DM:21`: "| 7.10 | Owner HALT with legacy title/AC1 |"

Fix: In the 7.10 Branch 2 text add: on a resume, if the section exists, do not write it again (append a dated re-confirmation line below it if one is needed); if the style file already holds the exception, verify it against the diff instead of re-applying it, and apply the qualifier at each of the six sites only where it is absent; take the before excerpts from the original start a09f6a12b0dce12e63b5b781a10a7be5446be367, not from HEAD. Do not change the 7.20 count instead: grep -c counts lines, so a doubled prefix on one line would still count 6, and changing the 7.20 command is not allowed (invariant G5).

Verifier: Run 7.10 twice with a simulated failed check between the runs: grep -c "^## Execution authorization (verbatim)" on the result file prints 1, and grep -o "Except for the sweep chat-summary exception above," on STYLE piped to wc -l prints 6.

Notes:
- Severity votes in Round 2: L / L / L. The V1 card rated it MEDIUM; all three advocates accept LOW (CONS 4.4).
- INV-R4-022 (LOW): a commit that lands before the retry would make HEAD hold the edited text; the plan fixed anchor is the original start (TL:3020).

### M-06 (LOW): partial

Tag: Grounded for the omission and the rewording; [INFERRED] for any test consequence (no current check greps these words). Location: TL:1210 (7.10 Action) against ADD:17, ADD:19 and BR:27. Authorization: inside the 85 allowed labels (DM:21); the two omitted clauses are outside the F-03 list of BR:27, so owner acceptance by name is advised.

Claim: The 7.10 Action embeds most addendum clauses but leaves out the ADD:17 clause do not reconstruct role from files or history and the ADD:19 clause never print a fabricated successful summary or hide an error to fit the success format, and it quotes the ADD:19 sentence in reworded form although the second revision request names the exact words. No current check greps these words, and 11.3 and the 11.4 pins already carry the no-fabricated-success rule, so a test consequence is not shown.

Evidence:

- `ADD:17`: "do not reconstruct role from files or history"
- `ADD:19`: "never print a fabricated successful summary or hide an error to fit the success format"
- `ADD:19`: "Formatting never authorizes advice prohibited by the sweep skill."
- `TL:1210`: "the rule says "Formatting never authorizes advice the sweep skill prohibits""
- `TL:1210`: "Preserve visible exit1/2 stderr and accurate other errors with ordinary formatting"
- `BR:27`: "loaded skill/style do not assign, "Formatting never authorizes advice prohibited by the sweep skill", chat-presentation only"
- `MV3:180`: "that formatting never authorizes advice the sweep skill prohibits (ADD:19 sentence 4)"
- `TL:1980`: "use ordinary formatting without fabricated success or prohibited advice"
- `ADD:21`: "All other applicable style, truthfulness, safety, and error-reporting rules remain in force."

Fix: In the 7.10 Action add never print a fabricated successful summary or hide an error to fit the success format, and do not reconstruct role from files or history, and quote the sentence as ADD:19 and BR:27 word it: "Formatting never authorizes advice prohibited by the sweep skill". Optional, from the Tier 1 card only (not debated): also embed ADD:21 sentence 3. Add no 11.4 assertion (BR:27).

Verifier: grep -c "fabricated successful summary", grep -c "reconstruct role" and grep -c "advice prohibited by the sweep skill" on TL each print 1 after the fix (0 today, each hit on line 1210).

Notes:
- Severity votes in Round 2: L / L / L.
- INV-R4-025 settled in this step: the authoritative wording is ADD:19 (the normative source), which BR:27 repeats; the run 3 merged verdict paraphrased it in its F-03 claim (MV3:180), and TL:1210 copied that paraphrase.
- The coverage matrix note on row INF-A08 quotes the reworded TL:1210 literal and still marks the row covered (CM:258); the row stays covered because the meaning is the same.

### M-07 (LOW): weak-check

Tag: Grounded (TL:1293, BR:9, TL:3020); [INFERRED] the resume loop of INV-R4-026. Location: TL:1293 (7.20 authorization check); root cause BR:9 (outside the plan). Authorization: inside the 85 allowed labels for 7.20 (DM:23); the root ambiguity in BR:9 is outside the plan.

Claim: The 7.20 authorization check matches a quote the executor itself writes against the authorization section of the second revision request, whose own text points both ways: it says it does not by itself start 7.10, yet records the owner earlier instruction and then execute as the execution direction. The later-dated-message branch has no on-disk comparator. 7.20 is a record check; the gate that matters is 7.10 Branch 1, which refuses to start without separate authorization and fresh checks, and the 7.23 lens traces execution claims to their evidence.

Evidence:

- `TL:1293`: "it must hold a dated verbatim quote of the owner's separate execution authorization and the paths of the fresh structural, alignment, qualitative and PRE reports as supplied with it"
- `TL:1293`: "or, when the separate execution authorization is a later dated owner message, that message as supplied with the fresh reports"
- `TL:1293`: "a quote written by the executor is a record of that authorization, not independent evidence, so a mismatch or an empty section is a FAIL"
- `BR:9`: "It does not by itself start item 7.10"
- `BR:9`: "the owner's earlier direct instruction "Already approved plan is confirmed proceed with implementation" and this answer's "then execute" are recorded as the owner's execution direction"
- `TL:3020`: "Separate execution authorization remains required after fresh revision checks/PRE."
- `TL:1210`: "keep Blocked, log the exact missing evidence in `### Phase 7 Findings`, STOP without ticking or changing the decision"
- `TL:1314`: "revision-check/execution claims to their actual evidence; old PRE/waivers do not approve this delta"
- `TL:1295`: "On a FAIL, return to the owning item and re-run this item"
- `SK:537`: "Do NOT re-execute any `- [x]` items"
- `DM:23`: "| 7.20 | Existing decision/capture mechanical checks |"

Fix: Keep the deliberate match target (second revision row B2-1); do not adopt the variant-1 fix that has the owner save the message to a named file, which is an owner action the plan does not create. Two optional clarifications: (a) outside the plan, the owner states which of the BR:9 instructions is the separate execution authorization for 7.10, which removes the two-way reading at its root; (b) in 7.20, for a later dated owner message after a resume, require the owner to re-supply that message with the fresh reports, and state that a FAIL of this check after 7.10 is ticked is logged as a blocker for the owner, not a re-run of ticked 7.10.

Verifier: For (b): a walk of the case later dated message plus resume plus mismatch ends in a named blocker, not in a return to ticked 7.10; grep -c "re-supply" on TL prints 1 after the fix (0 today).

Notes:
- Severity votes in Round 2: L / L / L. V1 conceded that its verifier claim Today 7.20 returns PASS was overstated (R1v1:58); all three rejected it (CONS X-005).
- INV-R4-026 (MEDIUM, conditional on a later-message authorization and a resume before 7.20, UNADDRESSED in the debate): a resumed session holds that message only in the 7.10 record under test, so the check self-compares or fails, and a FAIL routes to ticked 7.10 (TL:1295, SK:537). Carried as optional fix (b).

### M-08 (LOW): missing-guard

Tag: [INFERRED] (the risk rests on the behaviour of a spawned fix agent); the text is Grounded. Location: TL:2384 (13.18 Action), TL:2412 (13.22 Action). Authorization: inside the 85 allowed labels (DM:73, DM:76; owner acceptance by name advised: not one of F-01 to F-10).

Claim: The docs-gate fix agents in 13.18 and 13.22 may edit the docs, and DESIGN lives under docs/; DESIGN immutability there rests on one prose sentence with no sha256 check before and after the spawn, unlike 7.30, 7.34 and the 14.x fixers, and the 14.x hashes are taken only when those items start, so a DESIGN change made in Phase 13 would not be caught.

Evidence:

- `TL:2384`: "The fix agent edits only `src/superclaude/` and `tests/` sources, the docs and `CHANGELOG.md`, never a `.claude/` or installed HOME path"
- `TL:2384`: "DESIGN with its append, SPEC, revision authority and severity-test modules are immutable, with any required authority change left OPEN for escalation."
- `TL:2412`: "The fix agent edits only `src/superclaude/` and `tests/` sources, the docs and `CHANGELOG.md`, never a `.claude/` or installed HOME path"
- `TL:2614`: "record the output of `sha256sum docs/designs/orchestrator-mode.md"
- `DM:73`: "| 13.18 | Serialized fix cycle1 |"
- `DM:76`: "| 13.22 | Serialized fix cycle2 |"
- `BASE:2384`: "DESIGN with its append, SPEC, revision authority and severity-test modules are immutable, with any required authority change left OPEN for escalation."

Fix: In 13.18 and 13.22, record the four-file sha256sum (DESIGN, SPEC, design addendum, first revision request) before the spawn into a separate orchestrator-owned file, not the fix log, so the M-03 collision is not copied, and re-check it after the agent returns, as 14.25 does. Inside the 85 (DM:73, DM:76) but outside F-01 to F-10, so owner acceptance by name is advised.

Verifier: grep -c sha256sum on TL lines 2384 and 2412 prints 1 each after the fix (0 today; the TL hits today are lines 1363, 1391, 2614, 2642, 2705, 2733).

Notes:
- Severity votes in Round 2: L / L / L. Origin pre-existing: TL:2384 and TL:2412 are byte-identical to BASE (line hashes compared in this step).
- The V3 second option (compare DESIGN with the frozen hash e4a06d0c at the start of 14.25) was withdrawn and is not carried.

### M-09 (LOW): stale-reference

Tag: Grounded. Location: TL:1267 (7.17 Context), TL:2991 (OQ-17 entry), TL:2992 (OQ-18 entry) against DESIGN:557, DESIGN:559, DESIGN:993, DESIGN:995. Authorization: outside: needs new bounded authorization.

Claim: The 7.17 Context and the OQ-17 and OQ-18 open-question entries cite DESIGN lines 550, 552, 971 and 973 for sentences that now sit at DESIGN:557, 559, 993 and 995. The quoted text is intact and findable, so this is a navigation defect only.

Evidence:

- `TL:1267`: "DESIGN line 552: "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320).""
- `DESIGN:559`: "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320)."
- `TL:1267`: "DESIGN line 550: a `run-current --json` need "is a template change and needs the same owner note as any other allowlist change""
- `DESIGN:557`: "that is a template change and needs the same owner note as any other allowlist change"
- `TL:1267`: "DESIGN line 971 (open item 3): "a `--json` need goes to the owner as an allowlist change""
- `DESIGN:993`: "a `--json` need goes to the owner as an allowlist change"
- `TL:1267`: "DESIGN line 973 (open item 5): "A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template""
- `DESIGN:995`: "A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template"
- `TL:2991`: "(DESIGN line 552, SPEC line 320)"
- `TL:2992`: "(DESIGN line 550, DESIGN 17 open item 3 at line 971)"

Fix: With the 7.17 owner extension of M-01: cite these DESIGN sentences by quoted text or by section (section 7.3; section 17 open items 3 and 5) instead of line numbers, because an approved follow-up edit of DESIGN 7.3 would move them again. TL:2991 and TL:2992 are in the Open Questions section, outside the 85 labels.

Verifier: grep -c "DESIGN line 55[02]" on TL prints 0 after the fix (3 today: lines 1267, 2991, 2992).

Notes:
- No card raised it; the diff analysis found it and all three advocates agreed it is real and LOW.
- Merge-executor observation, not a separate finding: TL:1272, TL:2991 and TL:2992 also use the shorthand DESIGN 973 and DESIGN 971 for the same moved rows.

## 3. Closure of the ten defects of run 3 (F-01 to F-10)

fixed 8 (F-02, F-03, F-04, F-05, F-06, F-08, F-09, F-10); partial 2 (F-01 open on the optional branch through M-01 and M-02; F-07 residual M-03)

| Id | Status | Scope status |
|---|---|---|
| F-01 | partial | fixed as scoped (variant-1, variant-3, Tier 1); open end to end on the optional branch (variant-2) |
| F-02 | fixed |  |
| F-03 | fixed |  |
| F-04 | fixed |  |
| F-05 | fixed |  |
| F-06 | fixed |  |
| F-07 | partial |  |
| F-08 | fixed |  |
| F-09 | fixed |  |
| F-10 | fixed |  |

- F-01 `TL:1293`: "this glob counts only the eight prerequisite records, because the optional OQ-17 and OQ-18 records that item 7.17 may write have two-digit numbers and do not match it"
- F-02 `TL:2267`: "(fixed-string search, because the bullet holds backticks and inner double quotes) prints one line, line 404"
- F-03 `TL:1210`: "a direct operative assignment for specified work plus a separate sweep request in the same message is eligible only if the assignment is applicable before execution and every other condition holds"
- F-04 `TL:1211`: "section written first (later content is appended below it, never overwriting it)"
- F-05 `TL:1982`: "A failure caused by `sweep.md` or `SKILL.md` is fixed by returning to the owning item (11.1 or 11.3), correcting the source in place and then re-run this item"
- F-06 `TL:1292`: "Pre-7.10 source anchor for the style scope: `src/superclaude/output-styles/pragmatic.md:22` held the unqualified table mandate; after item 7.10 it holds the scoped sweep exception."
- F-07 `TL:1363`: "after the agent returns, re-run that command first and append a PASS line only when all four sums are unchanged"
- F-08 `TL:1293`: "expect 6, one per separate later restatement line; the primary rule line is not counted"
- F-08 `STYLE:22`: "EVERY response includes a DONE / NEXT table. No exceptions."
- F-09 `TL:1210`: "This item's Branch 1 and Branch 2 replace the Phase 7 preamble Branches 1 and 2 for this item only"
- F-10 `TL:1551`: "the report layout follows the recorded GQ-35 decision (the recorded GQ-63 decision governs only the sweep skill's chat reply, not the report file layout)"
- F-10 `TL:1812`: "The report layout follows the OQ-4 (GQ-35) record; the OQ-6 (GQ-63) record governs only the sweep skill's chat reply, not the report file layout."
- F-10 `OQ6:12`: "this decision affects only the sweep skill's chat reply, not the report file's layout."

## 4. Coverage (Wave 1)

Parsed requirements covered: 127 of 127. Union coverage: 0.99. Unmapped (union): ['INF-017', 'INF-A29']. The matrix (`coverage-matrix.yaml`) was rebuilt mechanically on the edited plan; INF-A06 and INF-A08 moved to covered after the second revision.

- INF-A06: covered -> now covered: the second revision embedded the same-message case in 7.10 (F-03); was partial in run 3 and carried there as part of F-03
- INF-A08: covered -> now covered: 7.10 states the rule and keeps placement; the quoted literal is reworded, which M-06 carries
- INF-017: partial -> not carried
- INF-A29: missing -> not carried

## 5. Reviewers, calibration and merge

| Card | Persona | Recorded model | Findings | Self C | Calibrated C | Calibrator |
|---|---|---|---|---|---|---|
| Tier 1 | requirements-analyst | claude-sonnet-5-5 | 0 HIGH, 0 MEDIUM, 9 LOW | 0.84 | 0.83 | haiku class (gpt-6.1-sol) |
| Reviewer 1 | analyzer | claude-sonnet-5-5 | 0 HIGH, 4 MEDIUM, 1 LOW | 0.72 | 0.68 | haiku class (gpt-6.1-sol) |
| Reviewer 2 | qa | gpt-6.1-sol | 2 HIGH | 0.89 | 0.86 | sonnet (claude-sonnet-5-5) |
| Reviewer 3 | refactorer | claude-opus-5-5 (outside the Tier1b slots) | 3 LOW | 0.80 | 0.86 | sonnet (claude-sonnet-5-5) |

Base variant: variant-2 (reviewer 2, qa; recorded model gpt-6.1-sol in the haiku-class slot; calibrated C 0.86). Best-practice grade: 4 (The ten run 3 defects are fixed as scoped (F-01 and F-07 with residuals), scope and line-stability hold, and no QA lens, fixer, counter or halt was weakened; a point is withheld because two pre-existing checks on the optional OQ-17/OQ-18 branch reject a correct owner-answered run (M-01, M-02) and the new sha256 guard keeps its baseline where the fix agent writes (M-03).). Calibrated confidence: 0.8 (mean of the three reviewer-card blind calibrations 0.68 (variant-1), 0.86 (variant-2), 0.86 (variant-3) = 0.80).

## 6. Invariant probe and what stays open

Unaddressed HIGH: [{"id": "INV-R4-003", "probe_status": "UNADDRESSED", "carried_in": "M-01", "covered_by": "M-01 fix part (4): the owner extension that names 7.17 must also cover the approval follow-up of TL:1271 (the DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate does not exist in the plan; the R5 re-run targets ticked items 6.5 to 6.22), or the owner accepts that an approval needs a later plan revision. Out of the 85 labels; needs the owner."}, {"id": "INV-R4-011", "probe_status": "PARTIAL (counted as UNADDRESSED by the gate)", "carried_in": "M-02", "covered_by": "M-02 fix names all three breaching checks of TL:1321 (probe commands limited to templates 1 to 8, forbidden run-current --json, ten ALLOWED_ORCA templates), anchored in the RESOLVED OQ-17/OQ-18 record. This is the clearing condition the probe states; the gate stays BLOCKED until a remediation brief adopts this wording or th

Consequence: Applying any of M-01 to M-09 is an edit of the task file and gives the plan a new hash, so it invalidates every earlier sign-off of the edited plan: re-run the structural, alignment, qualitative and PRE checks against it before 7.10 starts (BR:19). Each edit must stay on its single physical line with the line count unchanged unless a note is appended (BR:18). M-01 and M-09 need a new bounded owner authorization naming 7.17 (and the follow-up items of INV-R4-003); M-02, M-06 (two clauses), M-08 and the 14.x parity of M-03 are inside the 85 labels but outside the owner wording covering F-01 to F-10, so list them for owner acceptance by name rather than treat the label surface as consent. An owner authorization or amendment itself changes the compared surface.

Residual notes:
- Default-run SKIP lines against a gate that says every check PASSes. The 7.20 Action says SKIP for an absent optional file is not a failure, which settles it for a careful executor; a literal executor could stall. Optional wording: write PASS (absent, optional). Not a finding (not raised by any card).
- 11.4 names routes for sweep.md, SKILL.md and style defects; a defect in the test module or an environment failure falls to the closing stop with no named step. The test-module case is fixable inside 11.4, so this is a wording gap. Not a finding.
- Two routes for one style hazard: 7.20 says return to the owning item, 11.4 says a style failure is not sent back to ticked 7.10. The 7.20 route works for a careful executor (it does not require the destructive original-start retry). Not a finding.
- The appended end note names only the first revision as bounded authority; the second revision request is named only inside 7.20, 7.30 and 7.34. BR:17 allows a short additive note after the existing note. Not a finding.
- No merged finding makes a default-path run fail, and none blocks starting 7.10: 7.10 comes before 7.16 and 7.17, and both HIGH findings bite only from 7.17 onward if the optional branch fires.

## 7. Limits and disclosures

- Reviewer 3 ran on claude-opus-5-5, outside the allowed Tier1b model slots; the other reflect stages ran on claude-sonnet-5-5 or gpt-6.1-sol.
- Reviewers had no shell: they judged shell commands by reading; the operational QA agent simulated the F-01 commands in /tmp.
- Reviewer briefs were slimmer than run 3's (a common file plus one lens file each, pointing at the live files and the diff against the baseline plan).
- Reviewers and the Tier 1 analyst were launched in parallel; the deep override does not depend on the Tier 1 card.
- The adversarial rubric passes were made by one merge-executor session (forward and reverse), not two independent judges.
- Calibrator diversity is degraded (every available class is also a reviewer class). Vendor diversity is single.
- The tracked file docs/memory/reflect/deviation-patterns-IronClaude.md was not written (avoids an unrelated tracked change).
- Nothing was executed from the plan; model behaviour and installed activation are unverified.

## 8. Citations (mechanical check)

132 cited quotes in `artifacts/citations.json`; 0 mechanical failures: [].
