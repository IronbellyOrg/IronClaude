# Pairs P21 to P30 (detail version)

For each pair, read complaint A and complaint B. They come from two different reviewers of the same plan.
Question: would ONE edit to the plan (or spec) fix both complaints? If yes, they are the same problem.
Write yes or no after the colon on the line that starts with ANSWER. Do not change anything else.
If one complaint lists several problems, answer yes when one of those problems is the other's problem.

## P21

A (reviewer-1-card, finding R1-5): Task 3's new wording 'no ... link' is ambiguous against the existing upstream issue link in CLAUDE.md
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

B (reviewer-3-card, finding R3-F6): CLAUDE.md keeps a link to an upstream issue that Task 3's wording may forbid
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

ANSWER P21:

## P22

A (reviewer-2-card, finding R2-F1): Task 3's new 'no link that resolves to upstream' rule is contradicted by the untouched #419 upstream issue link elsewhere in CLAUDE.md
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

B (reviewer-3-card, finding R3-F6): CLAUDE.md keeps a link to an upstream issue that Task 3's wording may forbid
   points at: source CLAUDE.md:251-251 ; source CLAUDE.md:251-251

ANSWER P22:

## P23

A (reviewer-2-card, finding R2-F4): chains.md:14 token <REPORT.md is safe only because '<' is not stripped; no probe case pins it
   points at: source chains.md:14-14

B (reviewer-3-card, finding R3-F7): refs/chains.md:14 has `<REPORT.md path printed by step 1>`; token <REPORT.md is safe only because '<' is not stripped
   points at: source chains.md:14-14

ANSWER P23:

## P24

A (reviewer-1-card, finding R1-F1): Spec's closing verification (smoke -k "doc or primitive or how_we_work or severity" then full make test) is absent; only Task 6's narrow -k; Task 26 edits an installed primitive with only make verify-sync.
   points at: spec source.md:47-50

B (reviewer-2-card, finding R2-F1): Spec verification constraint dropped: no 'make test' in the tasklist (grep 0 hits); only Task 6's narrower -k. T1 C3 mitigation contradicted: implement.md:11 says 'Lint and tests are extras, never the pass/fail'; FINAL is a spec-compliance review, not a test run.
   points at: spec source.md:47-50 ; source implement.md:11-11

ANSWER P24:

## P25

A (reviewer-1-card, finding R1-F1): Spec's closing verification (smoke -k "doc or primitive or how_we_work or severity" then full make test) is absent; only Task 6's narrow -k; Task 26 edits an installed primitive with only make verify-sync.
   points at: spec source.md:47-50

B (reviewer-3-card, finding R3-F1): Spec-mandated verification is missing: source.md:47-50 requires the pytest smoke (-k "doc or primitive or how_we_work or severity") then a full make test at the end; no task runs make test; the only pytest is Task 6's narrower -k (tasklist:89); Task 26 edits an installed primitive with no test ru...
   points at: spec source.md:47-50

ANSWER P25:

## P26

A (reviewer-1-card, finding R1-4): The owner's core rule (the nested analyze directory exists only when /sc:analyze ran; the fallback lists no nested contract) is pinned by no test in the primitives. A later edit could drop that clause and every planned test stays green. Add a second exact phrase to Task 3, UNATTENDED_EXPECT and t...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:30-30 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:47-47 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:60-60 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:71-71 ; spec source.md:6-6 ; spec source.md:8-8 ; source test_worker_contract.py:508-509

B (reviewer-2-card, finding R2-4): Brief item 4's placement procedure is not evaluated. Per-command live-check extras are defined in the spec's section 7 acceptance rows (AC-1.5/1.6/1.7 replace 7.2 steps 3-4 per command), yet Task 6 writes to the section 2.1 bullet. Mitigating: spec line 376 maps the 2.1 rule to AC-2.1 (a P2 crite...
   points at: source orca-worker-contract-spec.md:318-322 ; source orca-worker-contract-spec.md:376-376 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:81-81

ANSWER P26:

## P27

A (reviewer-1-card, finding R1-6): Task 5's 'more cases than before' check has no recorded baseline; the edit adds exactly one id (`brainstorm:phrase:writes no nested directory`). Tell the implementer to save the before-count first.
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:75-75 ; source test_worker_contract.py:519-527 ; source test_worker_contract.py:559-568

B (reviewer-2-card, finding R2-1): Task 7's third acceptance criterion is unsatisfiable at baseline: it requires git status to list only the six files plus this package among tracked paths and nothing under .dev/tasks/done/ modified, but 950 staged additions and 3 renames of the prior package already exist. Both the first clause a...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:98-98 ; source diagnostics.txt:3-4

ANSWER P27:

## P28

A (reviewer-2-card, finding R2-1): Task 7's third acceptance criterion is unsatisfiable at baseline: it requires git status to list only the six files plus this package among tracked paths and nothing under .dev/tasks/done/ modified, but 950 staged additions and 3 renames of the prior package already exist. Both the first clause a...
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:98-98 ; source diagnostics.txt:3-4

B (reviewer-3-card, finding R3-6): Phrase variants are pinned correctly but fragile: 'write no nested directory' is not a substring of 'writes no nested directory', so each file is held to its own verb form. A shared phrase such as 'no nested directory' would pin the same rule with less risk.
   points at: plan TASK-WF-brainstormFixBri-20261106-001016.md:30-30 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:39-39 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:47-47 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:60-60 ; plan TASK-WF-brainstormFixBri-20261106-001016.md:71-71 ; source test_worker_contract.py:508-509 ; source test_worker_contract.py:531-531

ANSWER P28:

## P29

A (reviewer-2-card, finding 4): Assigned skill edits omit the SKILL.md frontmatter description (says 'then stops') and claim step 6 (Wave 5 summary would omit prompt rendering and the plan boundary). No acceptance criterion detects either.
   points at: spec source.md:303-303 ; source SKILL.md:3-3 ; source SKILL.md:87-87 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:86-86

B (reviewer-3-card, finding 8): Design section 16 puts design-doc B2 and B16 in Phase 1; the plan moves every design-doc edit to Task 8 (Phase 3) without stating why. Both phases ship in one PR.
   points at: spec source.md:405-405 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:139-149

ANSWER P29:

## P30

A (reviewer-2-card, finding 5): Plan lacks P1's blanket prohibition on code, warnings, options or text added only for non-Orca projects. Confirms T1 F-4.
   points at: spec source.md:39-39 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:19-26 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:17-17

B (reviewer-3-card, finding 7): Design step 5 hand_command note ('an agent started by hand is not governed by the hook; re-running the claim is preferred'), timeout 'check Orca' detail, and step 6 'the pending record stays' are absent from Task 6; LA-3 does not assert them.
   points at: spec source.md:211-212 ; plan TASK-WF-scIssueClaimPipe-20261107-063237.md:116-116

ANSWER P30:

