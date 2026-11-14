# Step 3 Qualitative Layer, Pass 1 (forward order V1, V2, V3, V4, V5)

Rubric: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` section A.2 (30 binary criteria, 6 dimensions x 5, Claim-Evidence-Verdict). No partial credit; no evidence means NOT MET.

Variants (paths relative to the adversarial folder):

| Id | File | Subject reviewed |
|---|---|---|
| V1 | variant-1-original.md | Issue #409 (TUI observer) vs Orchestrator mode (#339 / PR #539) |
| V2 | variant-2-original.md | Issue #450 (issue watcher rollout) vs #339 and #409 |
| V3 | variant-3-original.md | Coder#477 (workspace listener, monitor registration) vs #339 and #409 |
| V4 | variant-4-original.md | Issue #423 (orchestrator v2) vs #339 and #409 |
| V5 | variant-5-original.md | The built `superclaude observe` vs Orchestrator mode (#339) |

Source requirements used for "what it was meant to do": (R-a) validate findings against sources, (R-b) best course of action per point, (R-c) identify dependencies, (R-d) cover the issue and its PRs/work, (R-e) judge alignment.

Correctness uses what the debate established (diff-analysis.md SC-1..SC-20 and X-001..X-020; round2-rebuttal concessions). Items conceded or disproved count against Correctness. Invariant probe rows (INV-xxx) are consensus-level, not per-variant; they are used only as context.

Evaluation order: V1, V2, V3, V4, V5, within each dimension. No other evaluator's output was read.

## Dimension 1: Completeness

Criteria: C1 covers all explicit requirements; C2 edge cases and failure scenarios; C3 dependencies and prerequisites; C4 success/completion criteria; C5 explicit out of scope.

### V1

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | V1 covers R-a to R-e for #409 and PR #539 | "Result: 39 claims checked"; "Smallest change" column per finding; "Missing for integration"; Verdict "NOT YET INTEGRABLE as written, but compatible in direction" | MET |
| C2 | Edge and failure cases covered | "Exit 1 and 2 leave no JSON and no report. The observer must show: no report found, newest report unreadable or truncated ... `orca_available: false`" (Missing item 5) | MET |
| C3 | Dependencies named | "Missing for integration ... Nothing below exists in #409 or in the Phase 1 design today"; C-08 "#539 needs a rebase after #541 merges" | MET |
| C4 | Completion criteria defined | Table "Acceptance criteria of #409" A-01..A-15 with verdicts; Missing item 1 "A written data contract ... schema version policy" | MET |
| C5 | Out of scope stated | "Not done: no live `superclaude sweep run` ... Not read: the 14.6k-character #339 accuracy-check comment" | MET |

Subtotal V1: 5/5.

### V2

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | V2 covers R-a to R-e for #450 | R-b, R-c, R-d, R-e present (W-01..W-16, "Proposed edits to #450"). R-a is not done systematically: no claim-check table of #450's body; claims are checked only ad hoc (W-12 test counts, W-13..W-15). Searched sections: Scope read, "How a watcher-launched session appears", Alignment findings | NOT MET |
| C2 | Edge and failure cases covered | W-09 "stalling at the ccsession Session Name prompt"; W-15 "A refused or failed launch (`W-ENFORCEMENT-ABSENT`) therefore still reads as claimed" | MET |
| C3 | Dependencies named | "Waits for Orchestrator mode Phase 2 (or #534) ... Waits for Coder#477 ... Does not need to wait: items 1, 2, 4 above" | MET |
| C4 | Completion criteria defined | "Add 'Done when 0: decide the claim level the watcher passes'"; Verdict "Partly aligned; not ready to run FU-1 live as written" | MET |
| C5 | Out of scope stated | "Not read: the #409 design package on the git ref ... PR diffs of #447/#448/#485"; "Do not build the observer's watcher reader ... until FU-1 is recorded" | MET |

Subtotal V2: 4/5.

### V3

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | V3 covers R-a to R-e for Coder#477 | Claim-check table of 8 paths plus related-issue claims; F1..F17; Edits 1..12; "What IronClaude must supply or wait for" | MET |
| C2 | Edge and failure cases covered | F6 "#477 has no criterion for a stopped, restarting or deleted workspace, for a stale registration, or for deregistration" | MET |
| C3 | Dependencies named | Edit 12 "Depends on: the owner's decision on IronClaude `docs/designs/issue-watcher.md` section 2.3 ...; the trust-grant format (IronbellyOrg/IronClaude#339)" | MET |
| C4 | Completion criteria defined | Edits 4..9 are testable acceptance criteria, e.g. "- [ ] Reading status and sending a prompt are separate permissions with separate credentials. A credential that can read status is rejected by the prompt route; a test shows this." | MET |
| C5 | Out of scope stated | Edit 10 "Out of Scope: ... Choosing or building the trust-grant format ... Reusing the central heartbeat collector ... Sending a prompt to a running session through Claude Code cross-session messaging" | MET |

Subtotal V3: 5/5.

### V4

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | V4 covers R-a to R-e for #423 | "Claim check of #423" C1..C11; F1..F22; "Results of the four proposals"; Proposed edits for #423, #339, #409 | MET |
| C2 | Edge and failure cases covered | F8 "Cheaper agents 'searching sessions or diffing logs' read transcripts that may contain untrusted web or PR content"; F7 no channel to ordinary sessions | MET |
| C3 | Dependencies named | Edit 2 "This starts only after #339 Phase 1 is merged (PR #539) and the #534 live capture that restores the `working` class is done" | MET |
| C4 | Completion criteria defined | "Acceptance Criteria, add: - [ ] The design names the exact catalogue fields, where each comes from in the sweep's JSON ..." | MET |
| C5 | Out of scope stated | "Out of Scope, add: A second scanner of Orca, git or transcripts. Sending prompts or commands to person-started sessions ..." | MET |

Subtotal V4: 5/5.

### V5

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | V5 covers R-a to R-e for the built observer | S1..S10 inventory with file:line; O-01..O-16 overlap; 23 corrections to the #409 body (validation against source); D1..D9 decisions; verdict "keep both programs; write one contract (D1)" | MET |
| C2 | Edge and failure cases covered | Section 4 flags `STALE`, `PARTIAL`, `identity unknown`, `order unknown`, `conflict (time went back)`; S8 Q-1 FAIL, `consumer_fenced`, `no_active_terminal` | MET |
| C3 | Dependencies named | "Dependencies for integrating Orchestrator mode with `observe`" table (PR #539, #541, #534, owner records, Orca facts) | MET |
| C4 | Completion criteria defined | D1 "Contract content: names ...; join key (`dispatchId` ... `row_id` minus `orca:`); who owns which fact; one word list ..."; each D has a "Smallest reversible first step" | MET |
| C5 | Out of scope stated | "Unverified and not claimed: a live Orca run of either program ..."; "Not read: keys.py, terminal.py, sanitize.py"; "Write-back stays out of scope until the boundary is changed explicitly" | MET |

Subtotal V5: 5/5.

Completeness subtotals: V1 5, V2 4, V3 5, V4 5, V5 5.

## Dimension 2: Correctness

Criteria: K1 no factual errors or hallucinated claims; K2 approaches feasible with stated constraints; K3 terminology consistent and accurate; K4 no internal contradictions; K5 claims supported by evidence or rationale in the document. Debate-established facts: X-012/X-013 (observer exists and does not read the sweep JSON), X-008, X-009, X-004, X-001, X-002, X-007, X-019, X-020; SC-1..SC-20.

### V1

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | V1 has no disproved factual claims | C-03 "No observer code exists ... Verified" and C-02 "The observer does not exist": disproved by X-012/SC-13 (PR #503 and #514 merged, `main.py:572-574`); R2-V1 "Concede in full". Also C-25/F-01 "(1) Observer reads the sweep JSON" disproved by X-013 | NOT MET |
| K2 | Proposed approach is feasible | F-03/Q1 "persist `<stem>.json` ... same atomic link publish" so the observer reads it; the built observer reads Orca only (SC-15/16), and persisting breaks the pinned "exactly one report file" rule (R2-V5 D-2, R2-V1 D-1). R2-V1 withdraws F-03's observer option and Q1 | NOT MET |
| K3 | Terminology used consistently | Fixed verdict vocabulary "aligned / gap / contradiction / unknown" used in every table; "UNVERIFIED" defined in Conventions | MET |
| K4 | No internal contradictions | Verdict "Both are read-only and share the same dimension names" vs C-02 "Overstated" and F-02 "Gap and contradiction in vocabulary" (X-008); header tally "2 WRONG ... 2 UNVERIFIED" miscounted (X-009) | NOT MET |
| K5 | Claims supported by cited evidence | Every row has file:line, e.g. "GraphQL reviewThreads: 6 threads. 4 resolved ... 2 unresolved" (confirmed SC-2); C-25 "`policy` is a JSON row key (report.py:650)" (SC-1) | MET |

Subtotal V1: 2/5.

### V2

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | V2 has no disproved factual claims | W-01 default `worktree` level confirmed (SC-3: `issue.md:43,88`, `launch.py:33`); W-06 confirmed (SC-5); orchestrator absence confirmed (SC-6). R2-V2 concessions are scope and stale `/tmp` cites only: "a scope choice, not a defence" | MET |
| K2 | Proposed approach is feasible | W-01 "change the fixed prompt to `/sc:issue --claim <N> --pipeline none` ... Edit `launch.PROMPT_PATTERN`, `build_claim_prompt`, the 12-element argv pin and the NFR-001 property test; the variable part stays an integer" (INV-012 treats it as addressed) | MET |
| K3 | Terminology consistent | Separates "Orca orchestration Worker" from `agent launch` session; "Run-less", "top-level session" used the same way throughout | MET |
| K4 | No internal contradictions | W-13/W-14 "aligned" sit beside W-01/W-06 "contradiction" on different points; verdict repeats the same two contradictions | MET |
| K5 | Claims supported | Each row cites file:line plus live commands, e.g. "`orca-ide agent launch --help`"; "`launch.py:42-45`" | MET |

Subtotal V2: 5/5.

### V3

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | V3 has no disproved factual claims | Claim-check table (5 of 8 paths omit `image/`) confirmed SC-4; F1 confirmed SC-5. Disproved items are proposals, not stated facts (see K2). Residual: stale `/tmp` line cites conceded in R2-V3 item 3 (citation drift, not a wrong fact) | MET |
| K2 | Proposed approach is feasible | Edit 5 "The reply is produced without any write and runs only the sweep's read-only commands" is unachievable: each `sweep run` publishes a report (`commands.py:186`, X-004); Edit 8 restates the launch without the claim's second agent (X-001). R2-V3 "I withdraw: Edit 5 as written, the restated launch in Edit 8" | NOT MET |
| K3 | Terminology consistent | F3 flags "the monitor" as undefined rather than using it loosely; Edit 3 asks the owner to define it; "listener", "registration" used consistently | MET |
| K4 | No internal contradictions | Q1 "keep option A ... rescope #477" matches F1 and Edit 1; Edits 4..9 stated as conditional ("written for the case that #477 stays open") | MET |
| K5 | Claims supported | F8 quotes the Claude Code docs ("Commands don't run: a command in the message's text ... arrives as plain text") with URL and fetch date; F4 cites `report.py:619-695` | MET |

Subtotal V3: 4/5.

### V4

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | V4 has no disproved factual claims | F17 "confines every path under the root ..." is INCOMPLETE for git-status targets (X-007, SC-9); C7/F11 "starts one ordinary top-level agent session" omits the second agent (X-001, SC-3); C8 "TRUE ... Matches the new #409 body" rests on a sentence that occurs only in decision 8 itself (X-002, SC-7) | NOT MET |
| K2 | Proposed approach is feasible | Proposed edits are text changes with owner questions: "The catalogue reads the facts that `superclaude sweep run` already produces ... Any field ... that JSON schema v1 lacks ... is requested through the one schema decision in #339" | MET |
| K3 | Terminology consistent | F1 names the two meanings of "v2"; F22 and Edit 6 fix "Orchestrator" as "coordinator session, WC-16 loop" and use it that way | MET |
| K4 | No internal contradictions | Proposal (b) "HOLDS, with one unresolved decision" and F13 (two diverging schema requests) are consistent; tally "22 findings: 3 contradictions ... 14 gaps, 2 unknowns, 3 aligned" adds up | MET |
| K5 | Claims supported | Claim-check table has an Evidence column per row; unread items labelled "UNVERIFIED" (C9, C11) | MET |

Subtotal V4: 4/5.

### V5

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | V5 has no disproved factual claims | Core facts confirmed (SC-13..SC-18: PRs #503/#514 merged, guard False on master, no cross-reference between programs). Disproved or overstated: Verdict "All four earlier reviews ... were wrong about one fact" (X-019), "Drop W-3 from the #409 body" (X-020, SC-19); O-05 reword withdrawn ("Whether `check --all --types question` consumes on a live Run is not established", R2-V5 section 5); R2-V5 "I concede nine in full or in part" | NOT MET |
| K2 | Proposed approach is feasible | D1(a) "keep them separate and write one contract"; first step "one short relationship note, linked from `docs/designs/orchestrator-mode.md` section 1"; D5 option (ii) needs only one owner sentence | MET |
| K3 | Terminology consistent | Names the two schemas "observe snapshot v1" and "sweep report JSON v1" and keeps them apart throughout; "live read off" defined in section 8 | MET |
| K4 | No internal contradictions | D4 "Non-owner non-consumption is UNVERIFIED, so nothing here widens a read" agrees with O-05 and the verdict's Unverified list | MET |
| K5 | Claims supported | Evidence column with file:line and `gh` results on every row (e.g. "`adapter.py:29-32`, `:153-188`"); unreproduced items labelled ("693 passed, 1 failed in my copy for a harness reason") | MET |

Subtotal V5: 4/5.

Correctness subtotals: V1 2, V2 5, V3 4, V4 4, V5 4.

## Dimension 3: Structure

Criteria: S1 logical section ordering; S2 consistent hierarchy depth; S3 separation of concerns; S4 navigation aids (TOC, cross-references, index); S5 follows conventions of the artifact type (a read-only alignment review: scope read, findings, edits, owner questions, verdict).

### V1

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Prerequisites precede dependents | Order: "Scope read" > "Claim check of the new #409 body" > "Alignment findings" > "Missing for integration" > "Questions only the owner can answer" > "Verdict" | MET |
| S2 | Hierarchy depth consistent | H2 sections; H3 only under Alignment findings ("Alignment points", "Acceptance criteria of #409", "Proposed wording") | MET |
| S3 | Concerns separated | Claim check, findings, acceptance criteria, wording, missing items, owner questions each have their own section or table | MET |
| S4 | Navigation aids present | Cross-references by id: "Fix wording is under Alignment findings (F-07 for C-07 and C-18, F-02 for C-25, F-16 for C-34)"; wording ids W-1..W-7 referenced from findings | MET |
| S5 | Follows review conventions | Scope read with exact sources, claim check, findings, owner questions, verdict, UNVERIFIED list | MET |

Subtotal V1: 5/5.

### V2

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Prerequisites precede dependents | "How a watcher-launched session appears to the sweep" (facts, items 1-7) comes before "Alignment findings" that cite those facts | MET |
| S2 | Hierarchy depth consistent | H2 sections only, no orphaned subsections | MET |
| S3 | Concerns separated | Facts, findings, "Proposed edits to #450", owner questions, verdict in separate sections | MET |
| S4 | Navigation aids present | W-01..W-16 ids cited from edits ("(W-01, W-02)", "(W-03, W-04, W-08, W-09)") | MET |
| S5 | Follows review conventions | Scope read, findings, proposed edits, "Questions only the owner can answer", Verdict | MET |

Subtotal V2: 5/5.

### V3

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Prerequisites precede dependents | Claim check precedes findings; findings precede "What IronClaude must supply" and Edits that cite "F1", "F8" | MET |
| S2 | Hierarchy depth consistent | H3 "What IronClaude must supply or wait for" sits under "Alignment findings" as its one subsection (not orphaned: it belongs to the findings) | MET |
| S3 | Concerns separated | Claim-check table, findings, "Proposed edits to Coder#477" (12 numbered edits), owner questions Q1..Q7, verdict | MET |
| S4 | Navigation aids present | Findings cite edits ("Edit 8, owner question Q1"); edits cite findings | MET |
| S5 | Follows review conventions | Scope read with not-read list, claim check, findings table, edits, questions, verdict | MET |

Subtotal V3: 5/5.

### V4

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Prerequisites precede dependents | "Claim check of #423" then "Alignment findings" (with "Results of the four proposals" summarising F2..F6 by id) then "Proposed edits" | MET |
| S2 | Hierarchy depth consistent | H3 "Results of the four proposals" and "Findings table" under findings; H3 "#423", "#339", "#409" under "Proposed edits" | MET |
| S3 | Concerns separated | Claim check, findings, edits per issue, owner questions, verdict | MET |
| S4 | Navigation aids present | F-ids cited in the proposal table ("F2 to F6", "F8, F9", "F12") and in edits | MET |
| S5 | Follows review conventions | Scope table, claim check, findings, edits, "Questions only the owner can answer", Verdict | MET |

Subtotal V4: 5/5.

### V5

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Prerequisites precede dependents | "What `superclaude observe` is today" (S1..S10) > "Overlap and conflict with the sweep" > "Re-test of review 01" > "Corrections to the #409 body" > "Integration decisions" > "Questions" > "Verdict" | MET |
| S2 | Hierarchy depth consistent | H2 sections with numbered H3 parts (1..10) and D1..D9; extra H3 "Facts each program owns", "Could `observe` read the sweep" under Overlap | MET |
| S3 | Concerns separated | Inventory, overlap, re-test of the earlier review, body corrections, decisions are separate sections | MET |
| S4 | Navigation aids present | Ids O-01..O-16, F-01..F-18 (re-test), D1..D9 cross-referenced ("(D1)", "O-07") | MET |
| S5 | Follows review conventions | Scope read with sha and conventions line, findings, corrections with exact replacement text, owner questions, Verdict | MET |

Subtotal V5: 5/5.

Structure subtotals: V1 5, V2 5, V3 5, V4 5, V5 5. (None has a table of contents; each qualifies through id cross-references, which the rubric accepts.)

## Dimension 4: Clarity

Criteria: L1 unambiguous language (no "should consider", "might", "as appropriate"); L2 concrete rather than abstract; L3 each section has a clear purpose; L4 acronyms and domain terms defined on first use; L5 actionable next steps or decision points. A grep of the five variants for might / should consider / as appropriate / as needed / probably / possibly / perhaps / likely found: V1 none; V2 "very likely" (line 26); V3 "might" (line 59); V4 "possibly" (line 79); V5 "probably" (line 263).

### V1

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Language is unambiguous | No hedge word found by grep; unknowns are labelled "UNVERIFIED" ("UNVERIFIED means I could not confirm it from a source I opened") | MET |
| L2 | Concrete | Exact replacement text: W-1 "JSON v1 carries class, rule, evidence, notes, policy, person-started and safe-to-close per row ..."; file:line on every finding | MET |
| L3 | Sections have a clear purpose | "Missing for integration: Nothing below exists in #409 or in the Phase 1 design today" | MET |
| L4 | Terms defined on first use | Defines "Body" and "UNVERIFIED" only. `WC-16`, `FIN-F7`, `D-05`, `SP-22`, `FR-012`, `Attention Ledger` are used without definition. Searched: Conventions line, tables C-10, C-24, F-05 | NOT MET |
| L5 | Actionable next steps | "Questions only the owner can answer" 1..9 each with "Recommended: ..." | MET |

Subtotal V1: 4/5.

### V2

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Language is unambiguous | Fact 4: "so a registered watcher worktree is very likely scanned" is a hedge on the premise that W-05 builds on, with no UNVERIFIED label at that point | NOT MET |
| L2 | Concrete | W-01 names the exact edit targets "`launch.PROMPT_PATTERN`, `build_claim_prompt`, the 12-element argv pin" | MET |
| L3 | Sections have a clear purpose | Section "How a watcher-launched session appears to the sweep" ends "Summary: to the sweep, a watcher session is an unowned, Run-less transcript ..." | MET |
| L4 | Terms defined on first use | `OB-H1`, `OB-H2`, `OB-H3`, `FU-1`..`FU-6`, `D2`, `W-ENFORCEMENT-ABSENT` used without definition (FU-1 and WC-13 get a short gloss; the OB-H gate does not). Searched: W-02, W-08, Proposed edits | NOT MET |
| L5 | Actionable next steps | "Proposed edits to #450" 1..5 and "Questions only the owner can answer" Q1..Q4 with recommendations | MET |

Subtotal V2: 3/5.

### V3

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Language is unambiguous | The single "might" (F9: "a reason a separate channel might be needed") sits inside a row marked "unknown" and "UNVERIFIED"; findings use fixed verdict words | MET |
| L2 | Concrete | Edit 2 lists the corrected paths, e.g. "`templates/VSCode-AIDev02/image/catalogue/orca/module.tf`" | MET |
| L3 | Sections have a clear purpose | "Proposed edits to Coder#477: Nothing below has been posted. Edits 1, 2, 10, 11 and 12 hold whatever the owner answers to Q1" | MET |
| L4 | Terms defined on first use | `AC1`..`AC5`, `NFR22`, `D1 option A`, `FU-1`, `heartbeat collector` used without definition; F3 explicitly says "the monitor" is undefined in the source | NOT MET |
| L5 | Actionable next steps | Q1..Q7 with recommendations; "Recommended action: the owner answers Q1 and Q2, then #477 is edited per Edits 1 to 12" | MET |

Subtotal V3: 4/5.

### V4

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Language is unambiguous | The single "possibly #431" (F12) carries "UNVERIFIED"; findings use fixed verdict words | MET |
| L2 | Concrete | Edit 7 gives replacement bullets with issue numbers; Edit 1 gives the exact sentence "In this issue 'v2' means the knowledge layer described here" | MET |
| L3 | Sections have a clear purpose | "Results of the four proposals" table: "(a) ... HOLDS FOR CLASSIFICATION, FAILS AS STATED" | MET |
| L4 | Terms defined on first use | `WC-3`, `WC-9`..`WC-16`, `GQ-109`, `INV-005`, `NFR`-style tags used without definition (F22 discusses the word "Orchestrator" but not these). Searched: scope table, F5, F7, F16 | NOT MET |
| L5 | Actionable next steps | "Questions only the owner can answer" 1..9; paste-ready edits per issue | MET |

Subtotal V4: 4/5.

### V5

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Language is unambiguous | D9 "so it probably means it (UNVERIFIED: only the owner knows)" is labelled and converted into a direct owner question (D9 first step) | MET |
| L2 | Concrete | Corrections table gives exact current text and exact replacement for 23 body lines | MET |
| L3 | Sections have a clear purpose | "What 'live read off' means, and the rule for switching it on" states the rule and its source (`commands.py:63-66`) | MET |
| L4 | Terms defined on first use | Many defined inline (Q-1, "live read off", AC-S), but `TUIBBS`, `NFR-014`, `INV-017`, `QUESTION-LINK` in section 6 only in passing, `D1`..`D9` heads are fine; no glossary. Searched: S1..S10, O-03, O-04, Dependencies table | NOT MET |
| L5 | Actionable next steps | Each D has options, recommendation and "Smallest reversible first step"; owner questions 1..10 with recommendations | MET |

Subtotal V5: 4/5.

Clarity subtotals: V1 4, V2 3, V3 4, V4 4, V5 4.

## Dimension 5: Risk Coverage

Criteria: R1 at least 3 risks with probability and impact; R2 mitigation for each risk; R3 failure modes and recovery procedures; R4 external dependencies and their failure scenarios; R5 monitoring or validation mechanism for risk detection. R1 is applied literally (probability and impact both stated); the variants rate findings with verdict labels (gap, contradiction) and UNVERIFIED flags, not with likelihood and impact ratings.

### V1

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | 3+ risks with probability and impact | No evidence found: findings carry verdict labels only (F-07 "Wrong claim in #409 (C-07); real open security item"); no likelihood or impact rating. Searched: Alignment findings, Missing item 10, Verdict | NOT MET |
| R2 | Mitigation per risk | "Smallest change" column per finding; F-07 "Owner: fix before merge (limit paths to the selected repository and disable executable git config) or record as accepted in design section 13" | MET |
| R3 | Failure modes and recovery | Missing item 5: "Exit 1 and 2 leave no JSON and no report ... Last-known data stays qualified with its age; source loss never turns into `finished` or 'all clear'" | MET |
| R4 | External dependencies and failure | F-04 "50 `worker-show` calls and 90 s ... rows past 50 are `could not determine`"; "`orca_available: false`"; "Orca inputs partly UNVERIFIED" | MET |
| R5 | Monitoring or validation mechanism | Missing item 4: "a visible 'last report N minutes old' in the header" and item 1 "the golden test that pins it" | MET |

Subtotal V1: 4/5.

### V2

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | 3+ risks with probability and impact | No evidence found: W-01 and W-02 are labelled "contradiction" and "gap" with no likelihood or impact rating. Searched: Alignment findings, Verdict | NOT MET |
| R2 | Mitigation per risk | W-01 "change the fixed prompt to `/sc:issue --claim <N> --pipeline none`"; W-02 "add to #450 a precondition 'OB-H1 item 1, OB-H2, OB-H3 recorded as passed (#394)'" | MET |
| R3 | Failure modes and recovery | Failure modes are named (W-09 stall at the name prompt, W-15 failed launch reads as claimed) but no recovery or rollback procedure is given; W-15 is "aligned ... None". Searched: W-03, W-09, W-15, Proposed edits | NOT MET |
| R4 | External dependencies and failure | "UNVERIFIED: that Orca writes no Run record at all for `agent launch`"; W-09 "depends on the Orca Claude command being `ccsession-orca`" | MET |
| R5 | Monitoring or validation mechanism | "Add to FU-1: before and after the test launch, run read-only `orca orchestration run-list` and `worker-list`, and write down that no Run or Dispatch appeared" | MET |

Subtotal V2: 3/5.

### V3

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | 3+ risks with probability and impact | No evidence found: F14 "gap (risk)" and F8 "contradiction" have no likelihood or impact rating. Searched: findings F1..F17, Verdict | NOT MET |
| R2 | Mitigation per risk | Edits 4..10 map to findings; F14 "Edit 10 (out of scope line)" for the anonymous heartbeat endpoint | MET |
| R3 | Failure modes and recovery | Edit 9 "A request for a stopped or stale workspace is refused with a stated reason; it is never queued silently ... A deleted workspace's registration is removed" | MET |
| R4 | External dependencies and failure | F9 "A session inside a container and a session on the host can't reach each other"; "If they use a gateway, Claude Code cannot carry a message between two workspaces" | MET |
| R5 | Monitoring or validation mechanism | Edit 7 "Every audit line holds the time, sender, workspace id, request type ... can be joined to the watcher's `audit.jsonl`"; Edit 8 live test "records that the prompt ran as a slash command and the permission mode" | MET |

Subtotal V3: 4/5.

### V4

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | 3+ risks with probability and impact | No evidence found: F8, F9, F14 are labelled "gap" with no likelihood or impact rating. Searched: findings F1..F22, Verdict | NOT MET |
| R2 | Mitigation per risk | F8 "Add AC and out-of-scope: relayed knowledge is data, never an instruction; fixed typed fields; summaries are marked LLM-derived"; F14 "LLM-derived entries are marked as inferred ... never change a sweep class" | MET |
| R3 | Failure modes and recovery | No evidence found of a recovery procedure; the nearest is the fallback "relays to the person only" (Edit 4 AC 5) if the trust design is not ready, which is a scope fallback, not recovery. Searched: F4, F7, F8, Proposed edits | NOT MET |
| R4 | External dependencies and failure | F8 untrusted transcripts and PR content feeding other agents; F3 "depends on Coder#477 ... is not built"; F5 GitHub reads not in the allowlist | MET |
| R5 | Monitoring or validation mechanism | No evidence found: the added acceptance criteria are design-time statements ("The design names ...") with no runtime or test mechanism to detect the risks. Searched: AC list, F14, Proposed edits | NOT MET |

Subtotal V4: 2/5.

### V5

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | 3+ risks with probability and impact | No evidence found: items are rated by verdict word and UNVERIFIED flag (O-05 "contradiction", O-13 "unknown"), not likelihood and impact. Searched: O-01..O-16, D1..D9, Verdict | NOT MET |
| R2 | Mitigation per risk | Every O row has "Proposed change"; D1..D9 each give "Smallest reversible first step" | MET |
| R3 | Failure modes and recovery | S4: "STALE after 45 s without a good read", last good rows kept, "backoff doubling to 60 s"; S8 `--questions` "prints `question read not enabled ...`, exits 1, and makes no Orca call" | MET |
| R4 | External dependencies and failure | S8 "Q-1 (an unbound terminal reading another terminal's Run) FAILED"; "`NOT AVAILABLE (no Orca CLI validated)`"; dependency table lists UNVERIFIED Orca facts | MET |
| R5 | Monitoring or validation mechanism | D1 "have the owner run `superclaude observe --once --run <run>` ... and compare its dispatch ids with a sweep's `rows[].row_id` for the same Run, to confirm the join key" | MET |

Subtotal V5: 4/5.

Risk Coverage subtotals: V1 4, V2 3, V3 4, V4 2, V5 4.

## Dimension 6: Invariant and Edge Case Coverage

Criteria: I1 boundary conditions for collections (empty, single, maximum); I2 state interactions across component boundaries; I3 guard condition gaps (missing validation, unguarded assumptions); I4 count divergence (off-by-one, inclusive/exclusive, miscounts); I5 interaction effects when features or components combine. Edge Case Floor: a variant under 1/5 is ineligible as base.

### V1

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Collection boundaries addressed | F-04 "50 `worker-show` calls and 90 s in total (probes.py:115-116) ... rows past 50 are `could not determine` (`bound_reached`), and a 100-row `worker-list` page sets `truncated` with no paging" | MET |
| I2 | State across component boundaries | F-03 "JSON is printed to stdout only ... the only file on disk is the Markdown report"; F-12 "Orca-backed sources carry `age_seconds: null`" | MET |
| I3 | Guard gaps | F-07 "`_git` runs `git status` with `{**os.environ}`" (confirmed SC-9); F-13 "JSON strings are Markdown-escaped, not raw" | MET |
| I4 | Count divergence | C-07 "6 threads. 4 resolved ... 2 unresolved" against the body's "Five review findings"; C-36 "407 zip entries incl. PACKAGE-SHA256.json" against "406 package files" | MET |
| I5 | Interaction effects | C-18/F-07 "read-only" claim vs the repo-config execution path; F-05 `safe_to_close` observation vs design rule 5 | MET |

Subtotal V1: 5/5. Floor: eligible.

### V2

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Collection boundaries addressed | W-07 "All watcher sessions (up to 6 a day, left open) start in one configured worktree"; W-04 "write down that no Run or Dispatch appeared (or that one did)" (empty case) | MET |
| I2 | State across component boundaries | W-03 "The watcher record cannot be joined to either" (transcript `sessionId` or tab-map pane key); only `operation_id` is kept | MET |
| I3 | Guard gaps | W-11 "`healthy` is false during the shadow run, the kill switch and `enabled: false`; an observer or alert reading it would show a planned stop as a fault"; W-05 mislabel as person-started | MET |
| I4 | Count divergence | W-12 "says 2655 tests where the PR bodies say 2637 and 2653" | MET |
| I5 | Interaction effects | W-01/W-02 "The claim can start a second agent" combined with the OB-H gate; W-07 "each claim creates `issue-<N>`" in addition to the shared watcher worktree | MET |

Subtotal V2: 5/5. Floor: eligible.

### V3

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Collection boundaries addressed | F6 "A Minimal workspace has no Orca and no IronClaude, so no orchestrator can receive a routed prompt"; stopped, restarting, deleted workspaces | MET |
| I2 | State across component boundaries | F4 "All workspaces run the same image with `HOME=/home/coder` ... so a path such as `/home/coder/workspaces/...` is not unique across workspaces"; F13 two unconnected audit records | MET |
| I3 | Guard gaps | F14 "`POST /aidev/heartbeat` — anonymous (no auth)" would break AC4; F8 held-message rule for bypass sessions | MET |
| I4 | Count divergence | "five of the eight paths are wrong"; "`module.tf:49-55` holds for the pair app (50-56, off by one)"; "`main.tf:103-108` covers the hash locals, not the image resource (110)" | MET |
| I5 | Interaction effects | F8 "A prompt sent to a running session would also arrive as plain text (no slash command) and be held in bypass mode"; F12 trust criteria vs #339 grant design | MET |

Subtotal V3: 5/5. Floor: eligible.

### V4

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Collection boundaries addressed | No evidence found for empty, single or maximum cases: F3 addresses scope (one Run, one host) but states no size or empty-case boundary. Searched: F2..F6, F12, F17, F18 | NOT MET |
| I2 | State across component boundaries | F4 "No durable catalogue storage and no history ... The sweep never reads its own earlier reports"; F13 two diverging schema requests | MET |
| I3 | Guard gaps | F17 "Who may read whose sessions ... a path that escapes is not read" (read-permission model missing for cross-workspace data); F14 "LLM output flows into the same catalogue" breaks the observer's rule | MET |
| I4 | Count divergence | No evidence found of an off-by-one or miscount finding; the report's own tally "22 findings: 3 contradictions ... 14 gaps, 2 unknowns, 3 aligned" is internally consistent but is not a divergence finding. Searched: claim check C1..C11, F1..F22 | NOT MET |
| I5 | Interaction effects | F18 "collision and duplicate-work detection already exist in narrow form in v1 and in the #409 designs ... v2's reviews would be a third detector"; F16 three cadences | MET |

Subtotal V4: 3/5. Floor: eligible (3 is at least 1).

### V5

| Crit | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Collection boundaries addressed | S3 "at most 5 calls per read (4 `worker-list` pages plus 1 message call when questions are on)"; S8 "at most 100 rows per read, applied after the type filter"; fixtures for "empty, cap-100" | MET |
| I2 | State across component boundaries | O-08 two "v1" JSON schemas, "A join key exists: `dispatchId` = the part after `orca:`"; S5 snapshot rewritten every live cycle | MET |
| I3 | Guard gaps | O-09/D5 "the guard is a single boolean and does not check the Run id (`commands.py:173-187`)" vs "orchestrator mode creates a new Run per coordinator" | MET |
| I4 | Count divergence | S7 "PR #503: 486 passed; PR #514: 691 passed; my copy: 693 passed, 1 harness failure"; S3 "5 calls" vs "4 `worker-list` pages plus 1" | MET |
| I5 | Interaction effects | O-04 "Allow-lists ... contradiction in policy on one verb" (`check`); O-10 "several observers multiply the load" beside the sweep | MET |

Subtotal V5: 5/5. Floor: eligible.

Invariant subtotals: V1 5, V2 5, V3 5, V4 3, V5 5.

## Summary

### Dimension subtotals (each out of 5)

| Dimension | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| Completeness | 5 | 4 | 5 | 5 | 5 |
| Correctness | 2 | 5 | 4 | 4 | 4 |
| Structure | 5 | 5 | 5 | 5 | 5 |
| Clarity | 4 | 3 | 4 | 4 | 4 |
| Risk Coverage | 4 | 3 | 4 | 2 | 4 |
| Invariant and Edge Case | 5 | 5 | 5 | 3 | 5 |
| **Total /30** | **25** | **25** | **27** | **23** | **27** |
| qual_score (total/30) | 0.833 | 0.833 | 0.900 | 0.767 | 0.900 |

### Invariant and edge-case floor check (needs at least 1/5)

| Variant | Invariant score | Eligible as base |
|---|---|---|
| V1 | 5/5 | yes |
| V2 | 5/5 | yes |
| V3 | 5/5 | yes |
| V4 | 3/5 | yes |
| V5 | 5/5 | yes |

No variant is below the floor, so the floor is not triggered and no warning suspension is needed.

### Notes for the reconciliation step (Pass 1 only; not a ranking)

- Correctness is the dimension where the debate changed the picture: V1 loses 3 criteria (observer exists, persist-JSON approach built on a wrong premise, verdict line contradicts its own tables). V3 and V4 each lose 1 to 2 (V3: Edit 5 and the Edit 8 restatement; V4: F17, C7 and C8). V5 loses K1 only for overgeneralisation and a mislabel, not for its central finding.
- Criteria where the verdict rests on a judgement call and may differ in the reverse pass: C1 for V2 (no systematic claim check), L1 for V2 ("very likely scanned"), L1 for V3/V4/V5 (a single labelled hedge each, judged MET), K1 for V3 (proposals, not facts, were disproved), K5 for V4 (circular C8 judged as one claim), L4 for V5, I1 for V2 (only "up to 6 a day" and the empty-Run case).
- R1 is NOT MET for all five variants under a literal reading (no probability and impact ratings); this does not separate them.
- S4 is MET for all five through id cross-references; none has a table of contents.
