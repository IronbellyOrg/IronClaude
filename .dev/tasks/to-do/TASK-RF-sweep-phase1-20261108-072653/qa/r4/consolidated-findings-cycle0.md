# R4 gate, cycle 0: consolidated findings

Inputs: the 9 reports found by Glob `qa-*-report.md` in this folder (item 5.22). Design file: `docs/designs/orchestrator-mode.md` (1041 lines at consolidation time).

Report short names: TC = qa-template-conformance (item 5.13), IC = qa-internal-consistency (5.14), EQ = qa-evidence-quality (5.15), CO = qa-completeness (5.16), AC = qa-actionability (5.17), NM = qa-numbers-metrics (5.18), CR = qa-crossref-chain (5.19), DA = qa-domain-accuracy (5.20), MC = qa-master-contract-fidelity (5.21).

Report verdicts (blocking counts): TC PASS 0, IC FAIL 1, EQ PASS 0, CO PASS 0, AC PASS 0, NM FAIL 1, CR FAIL 2, DA FAIL 2, MC FAIL 1. Raw total 7 BLOCKING or MAJOR findings; after dedup 6 (1 BLOCKING, 5 MAJOR).

Raw to kept map: IC F1 to R4-F1; NM N-1 to R4-F1; MC F1 to R4-F2; CR F1 to R4-F3; CR F2 to R4-F4; DA F1 to R4-F5; DA F3 to R4-F6.

Severity note: the MC lens prompt says "Each predicted break is BLOCKING", but its report grades its one predicted break (MC F1) MAJOR. Under the lens rule it is BLOCKING, so it is kept here as BLOCKING (R4-F2). The verdicts and the blocking counts are the same either way.

## BLOCKING and MAJOR findings

### R4-F1 (MAJOR): the section 16 rollback row names four of the five test-file pin edits
- Sources: IC F1 (MAJOR, kept). Merged duplicates: NM N-1 (MAJOR), AC F3 (MINOR), CR F3 (MINOR).
- Evidence: `docs/designs/orchestrator-mode.md:682-688` says "Pins (five edits)", the fifth being the `RULE_PHRASES["never-as-worker"]` phrase at test line 89. The rollback row at `:970` lists WC-16, the line 23 entry, the `RULE_PHRASES` entry, the `NEVER_AS_WORKER` entry, the `UNATTENDED_COMMANDS` assertion and the test rename, and not the phrase edit. `:1041` says "added the fifth pin".
- Effect: following the row reverts contract line 23 but leaves the line 89 phrase carrying `/sc:sweep`, so `test_contract_states_rule[never-as-worker]` (`tests/skills/test_worker_contract.py:907-909`) fails on the reverted tree.
- Smallest fix: in `:970` replace "the `RULE_PHRASES` entry" with "the `RULE_PHRASES["WC-16"]` entry, the `RULE_PHRASES["never-as-worker"]` phrase at test line 89".

### R4-F2 (BLOCKING by the MC lens rule): step 1.18 turns `test_contract_states_rule[never-as-worker]` red and the fix sits in step 1.19
- Sources: MC F1 (graded MAJOR by its report; BLOCKING under the lens prompt, kept as BLOCKING). Merged duplicates: AC F2 (MINOR), IC F8 (MINOR).
- Evidence: `docs/designs/orchestrator-mode.md:944` (step 1.18 edits only contract line 23, gate 1.17) and `:945` (step 1.19 carries the pins); the phrase edit is pin 5 at `:688`. The pin is at `tests/skills/test_worker_contract.py:86-92` (phrase at :89-90) and `_check_rule` (:755-758) asserts it is a substring of the contract. After step 1.18 the old substring is gone.
- Effect: a per-step run of the contract tests after 1.18 is red until 1.19; 1.19 gates on a red 1.18. The end state is green.
- Smallest fix: move the `RULE_PHRASES["never-as-worker"]` phrase edit into the step 1.18 row, or state in the 1.18 and 1.19 rows that the two steps land in one commit (as R1 to R3 do at `:722`).

### R4-F3 (MAJOR): R2 and R8 name WC-16 as existing, but steps 1.21 and 1.24b do not wait for step 1.17 or 1.18
- Sources: CR F1 (MAJOR, kept). Merged duplicate: IC F9 (MINOR).
- Evidence: `:712` (R2) and `:718` (R8) cite WC-16; `:711` (R1) says "never a worker", which holds only after step 1.18 writes the line 23 entry. `:947` step 1.21 (R1 and R2) is gated on "1.14"; `:952` step 1.24b (R8) on "1.16"; `:951` step 1.24a (R7) is correctly gated on "1.18". `:668` and `:1005` (open item 20) hold only steps 1.17 to 1.19 while GQ-11 is open.
- Effect: while GQ-11 is open, R1, R2 and R8 could publish a rule that is not in the contract and may never be approved as written.
- Smallest fix: gate 1.21 on "1.14, 1.18" and 1.24b on "1.16, 1.17" in section 15.2, and add to open item 20's "Behaviour until closed": "R1, R2 and R8 (steps 1.21 and 1.24b) wait for 1.17 and 1.18 as well".

### R4-F4 (MAJOR): R1's own check fails until R4 lands, and R4 is ordered after R1 and left out of the one-commit rule
- Sources: CR F2 (MAJOR, kept).
- Evidence: `:711` (R1) is checked by `tests/core/test_how_we_work_routing_table.py`, which asserts `members == _OTHER_COMMANDS` (`:296-297`, in `test_other_commands_membership_and_live_references`, `:291`); `_OTHER_COMMANDS` (`:27`) is what R4 (`:714`) edits. `:722` says "R1, R2 and R3 land in one commit" and does not name R4; `:947` is step 1.21 (R1, R2) and `:948` is step 1.22 (R4, gate 1.21).
- Effect: after step 1.21 the table has a `/sc:sweep` row and `_OTHER_COMMANDS` does not, so the membership test is red.
- Smallest fix: `:722` becomes "R1 to R4 land in one commit" and steps 1.21 and 1.22 are merged (or 1.22 lists gate "1.21, same commit").

### R4-F5 (MAJOR): WC-16 never says how `/sc:sweep` relates to master's sweep (contract line 110)
- Sources: DA F1 (MAJOR, kept). Merged duplicates: CO F-4 (MINOR), AC F5 part (MINOR), IC F4 part (MINOR, no shared 5-minute budget stated).
- Evidence: master `src/superclaude/core/WORKER-CONTRACT.md:110` ("The sweep." after every wake or timeout, at most once every 5 minutes, with `worktree ps --agent-wait` and a contract `stat` per worker), state table `:116-129`, ladder `:148-155`. DESIGN `:677` ties WC-16 to that sweep by cadence only and reuses the bare term "the sweep" for the command ("The sweep's classes follow WC-10", "The sweep report", "The sweep recommends nothing"). `:672` says only that line 110 is not reworded. `/sc:sweep` cannot be master's sweep: `FORBIDDEN_TOKENS` has `--agent-wait` (`:537`), its eight Orca templates (`:526-535`) have no `check` or `inbox`, and it is read-only.
- Effect: the text fits replacing, running both, or running beside; R2's bold lead (`:712`) copies line 110's wording. A coordinator that treats `/sc:sweep` as "the sweep" skips the `agent-wait` listing and the heartbeat bookkeeping. "The sweep recommends nothing" is false for master's sweep read in the same contract.
- Smallest fix: make `/sc:sweep` explicitly additive in `:677` (the coordinator runs "The sweep." unchanged and, in the same pass, runs `/sc:sweep` and reads its report; it is an added read, not a replacement and not a second pass; it does not update heartbeat records or list `agentWait`), stop reusing "the sweep" for the command, and update R2's bold lead (`:712`) and D6 (`:829`) to match. The four pinned phrases survive that rewording.

### R4-F6 (MAJOR): `/sc:sweep` on every wake breaks master's trigger-gated probe rule (contract lines 110 and 151)
- Sources: DA F3 (MAJOR, kept).
- Evidence: master `:110` ("Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep") and `:151` (L1 probe: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat`; when a trigger fired; at most 2 costly probes per triggered worker per sweep). DESIGN `:303` (`worker-show` for `min(D, 50)` rows on every run), `:292` and `:514` (the tail of every scanned transcript and every contract record) are the same probes for all workers. `:672` says WC-16 does not reword line 151, which neither resolves nor acknowledges the conflict.
- Effect: a strict reader of master must skip `/sc:sweep` when no trigger fired (contradicting "on every wake") or break the cap.
- Smallest fix: add one sentence to WC-16 saying `/sc:sweep`'s own reads are not L1 probes and do not count against the L1 cap, while the coordinator's own L1 probes stay limited to triggered workers. DA notes this needs owner approval together with GQ-11; the pinned `liveness-*` phrases are not touched.

## MINOR findings (never fail the gate; left as notes)

| Id | Defect (sources) | Evidence |
|---|---|---|
| R4-F7 | Pin 5 quotes the old string with a leading quote that is not on disk; used literally as an edit anchor it finds no match (MC F2, CR F5, CO F-3) | `:688`; `tests/skills/test_worker_contract.py:89` |
| R4-F8 | The R4 revision-log row says draft names were marked "in 13 and 14"; section 14 has no WC text (TC m3, CO F-1, IC F3, CR F8) | `:1041`; `:854-880` |
| R4-F9 | R2's anchors (HOW-WE-WORK lines 396 and 403) are pre-R1 values; R1 inserts a row above them in the same step (CR F6, IC F7 part) | `:712`; research/08:111 |
| R4-F10 | "R4" names both the fix-cycle row and routing row R4 (TC m2, IC F7 part) | `:672`, `:714`, `:1041` |
| R4-F11 | The `.gitignore` comment cites WC-16, but the rollback keeps the comment while reverting WC-16 (CR F4) | `:732`, `:970`, `:973` |
| R4-F12 | The FR-001 traceability row cites 7.1 and 7.6 for the `main.py` registration; neither describes it (CR F7) | `:772` |
| R4-F13 | Trigger set differs: master says "wake or timeout", WC-16 and R2 say "wake" (DA F2, CR F9) | `:677`, `:712`; contract `:110` |
| R4-F14 | "It keeps a periodic sweep scheduled" has no 5-minute bound (IC F4) | `:677` |
| R4-F15 | The `/sc:sweep` classes are not mapped to master's S0-S11 and no tie-break is given; rule 2 covers only the Orca exit proof (DA F4) | `:472`, `:479`, `:491`; contract `:116-129`, `:157` |
| R4-F16 | `/sc:sweep` is listed before `/sc:swarm-wizard`, which breaks the alphabetical order of line 23 (DA F5 part, MC F3) | `:701`; contract `:23` |
| R4-F17 | Applying pin 1 twice would silently keep a duplicate `"WC-16"` key in the dict literal (DA F5 part) | `:684` |
| R4-F18 | "whatever #422 does" is stale next to "PR #422 is merged"; open item 21 sits under "unverified or undecided" (IC F2) | `:668`, `:982`, `:1006` |
| R4-F19 | Section 1 describes R3-B1 to R3-B3 as open defects that sections 7.2, 11 and 18 say are fixed (IC F5) | `:7-11` |
| R4-F20 | D6's source column and section 13's "Not counted" list omit the re-anchor and the record-only step 1.16a (IC F6) | `:829`, `:836-840` |
| R4-F21 | No step owns a `WRITE_VERB_CLASSIFICATION` row if the sweep text later gains a write verb (MC F4) | `:694`, `:945` |
| R4-F22 | The new `RULE_PHRASES` entry is one 141-character line that `ruff format` will wrap (MC F5) | `:684` |
| R4-F23 | The `"sweep"` assertion is placed in a test named for `load` (MC F6) | `:687`; test `:1318-1322` |
| R4-F24 | Step 1.7 gives no import path, group name or lint comment for the `main.py` pair (AC F1) | `:932` |
| R4-F25 | The pin list line numbers are pre-edit and the DESIGN does not say so (AC F4) | `:684-688` |
| R4-F26 | Step 1.16a states expected results and no action if they differ (AC F6) | `:942` |
| R4-F27 | `r4-reanchor.md` and `r4-wc14-hits.md` give section 8 as lines 666-695 and 666-693; it runs to 703 (AC F7, EQ F2) | `phase-outputs/discovery/r4-reanchor.md`, `r4-wc14-hits.md` |
| R4-F28 | `r4-reanchor.md` has no row for DESIGN 829 (contract line 110) or 970 (line 23) (EQ F1) | `phase-outputs/discovery/r4-reanchor.md` |
| R4-F29 | `r4-mechanical.md` Check 4 counts the WC-16 block twice (TC m5, EQ F3, NM N-2) | `phase-outputs/test-results/r4-mechanical.md:147` |
| R4-F30 | `r4-wc14-hits.md` records the open-items total at line 1000; it is now at 1010 (NM N-3) | `phase-outputs/discovery/r4-wc14-hits.md:109` |
| R4-F31 | DESIGN says the unattended-sections check globs `src/superclaude/commands/*.md`; the code globs `_THIS.COMMANDS_DIR` (NM N-4) | `:693`; test `:834` |
| R4-F32 | The GQ-107 row has a bare `\|` inside a code span, giving 5 cells under a 4-cell header; it exists in the design base, so R4 did not cause it (TC m1) | `:64` |
| R4-F33 | Section 7.6 repeats the "no `## Unattended mode` section" sentence (TC m4) | `:655` |
| R4-F34 | Section 8's constraint list omits `_check_repo_setup_gated` (CO F-2) | `:690-697` |
| R4-F35 | research/01, 02, 03 and 05 still carry the old WC-14 and "after 561" text with no stale marker; research/07 and 08 supersede them (CO F-5) | `research/01`, `02`, `03`, `05` |
| R4-F36 | WC-16 wording a reader must interpret: "Phase 1" can be read as the contract's own P1 phase, and "a ready Task it did not create, needing ownership review" has two readings (AC F5 part) | `:677` |

Not findings: the reviewers' notes about the lens reports themselves (CR report's Summary counts, TC report's C14 citation, MC report's C16 cell format and severity label, EQ and CR host-fact limits) are recorded in the T89, T95 and T97 notes files and need no DESIGN change.

## F_0 and the cycle-0 PASS set

F_0 = {R4-F1, R4-F2, R4-F3, R4-F4, R4-F5, R4-F6}

|F_0| = 6 (1 BLOCKING, 5 MAJOR)

Cycle-0 PASS set (every check id a report's `## Checks` table marks PASS), 144 ids; 27 other check ids are FAIL:

qa-actionability-report:C1 (item 5.17); qa-actionability-report:C2 (item 5.17); qa-actionability-report:C3 (item 5.17); qa-actionability-report:C4 (item 5.17); qa-actionability-report:C5 (item 5.17); qa-actionability-report:C6 (item 5.17); qa-actionability-report:C7 (item 5.17); qa-actionability-report:C8 (item 5.17); qa-actionability-report:C14 (item 5.17); qa-actionability-report:C15 (item 5.17); qa-completeness-report:C1 (item 5.16); qa-completeness-report:C2 (item 5.16); qa-completeness-report:C3 (item 5.16); qa-completeness-report:C4 (item 5.16); qa-completeness-report:C5 (item 5.16); qa-completeness-report:C6 (item 5.16); qa-completeness-report:C7 (item 5.16); qa-completeness-report:C8 (item 5.16); qa-completeness-report:C9 (item 5.16); qa-completeness-report:C10 (item 5.16); qa-completeness-report:C11 (item 5.16); qa-completeness-report:C12 (item 5.16); qa-completeness-report:C13 (item 5.16); qa-completeness-report:C14 (item 5.16); qa-completeness-report:C15 (item 5.16); qa-completeness-report:C16 (item 5.16); qa-completeness-report:C17 (item 5.16); qa-completeness-report:C18 (item 5.16); qa-completeness-report:C19 (item 5.16); qa-completeness-report:C20 (item 5.16); qa-completeness-report:C21 (item 5.16); qa-completeness-report:C22 (item 5.16); qa-crossref-chain-report:C1 (item 5.19); qa-crossref-chain-report:C2 (item 5.19); qa-crossref-chain-report:C3 (item 5.19); qa-crossref-chain-report:C4 (item 5.19); qa-crossref-chain-report:C5 (item 5.19); qa-crossref-chain-report:C6 (item 5.19); qa-crossref-chain-report:C7 (item 5.19); qa-crossref-chain-report:C8 (item 5.19); qa-crossref-chain-report:C9 (item 5.19); qa-crossref-chain-report:C10 (item 5.19); qa-crossref-chain-report:C11 (item 5.19); qa-crossref-chain-report:C18 (item 5.19); qa-crossref-chain-report:C19 (item 5.19); qa-crossref-chain-report:C23 (item 5.19); qa-crossref-chain-report:C24 (item 5.19); qa-domain-accuracy-report:C1 (item 5.20); qa-domain-accuracy-report:C6 (item 5.20); qa-domain-accuracy-report:C8 (item 5.20); qa-domain-accuracy-report:C9 (item 5.20); qa-domain-accuracy-report:C10 (item 5.20); qa-domain-accuracy-report:C11 (item 5.20); qa-domain-accuracy-report:C12 (item 5.20); qa-domain-accuracy-report:C14 (item 5.20); qa-domain-accuracy-report:C15 (item 5.20); qa-domain-accuracy-report:C16 (item 5.20); qa-evidence-quality-report:C1 (item 5.15); qa-evidence-quality-report:C2 (item 5.15); qa-evidence-quality-report:C3 (item 5.15); qa-evidence-quality-report:C4 (item 5.15); qa-evidence-quality-report:C5 (item 5.15); qa-evidence-quality-report:C6 (item 5.15); qa-evidence-quality-report:C7 (item 5.15); qa-evidence-quality-report:C8 (item 5.15); qa-evidence-quality-report:C9 (item 5.15); qa-evidence-quality-report:C10 (item 5.15); qa-evidence-quality-report:C11 (item 5.15); qa-evidence-quality-report:C12 (item 5.15); qa-evidence-quality-report:C13 (item 5.15); qa-evidence-quality-report:C14 (item 5.15); qa-evidence-quality-report:C15 (item 5.15); qa-evidence-quality-report:C16 (item 5.15); qa-evidence-quality-report:C18 (item 5.15); qa-evidence-quality-report:C19 (item 5.15); qa-evidence-quality-report:C20 (item 5.15); qa-evidence-quality-report:C21 (item 5.15); qa-internal-consistency-report:C1 (item 5.14); qa-internal-consistency-report:C2 (item 5.14); qa-internal-consistency-report:C3 (item 5.14); qa-internal-consistency-report:C4 (item 5.14); qa-internal-consistency-report:C5 (item 5.14); qa-internal-consistency-report:C6 (item 5.14); qa-internal-consistency-report:C7 (item 5.14); qa-internal-consistency-report:C8 (item 5.14); qa-internal-consistency-report:C9 (item 5.14); qa-internal-consistency-report:C11 (item 5.14); qa-internal-consistency-report:C12 (item 5.14); qa-internal-consistency-report:C13 (item 5.14); qa-internal-consistency-report:C14 (item 5.14); qa-internal-consistency-report:C15 (item 5.14); qa-internal-consistency-report:C16 (item 5.14); qa-internal-consistency-report:C17 (item 5.14); qa-internal-consistency-report:C18 (item 5.14); qa-internal-consistency-report:C19 (item 5.14); qa-master-contract-fidelity-report:C1 (item 5.21); qa-master-contract-fidelity-report:C2 (item 5.21); qa-master-contract-fidelity-report:C3 (item 5.21); qa-master-contract-fidelity-report:C4 (item 5.21); qa-master-contract-fidelity-report:C6 (item 5.21); qa-master-contract-fidelity-report:C7 (item 5.21); qa-master-contract-fidelity-report:C8 (item 5.21); qa-master-contract-fidelity-report:C9 (item 5.21); qa-master-contract-fidelity-report:C10 (item 5.21); qa-master-contract-fidelity-report:C11 (item 5.21); qa-master-contract-fidelity-report:C12 (item 5.21); qa-master-contract-fidelity-report:C13 (item 5.21); qa-master-contract-fidelity-report:C14 (item 5.21); qa-master-contract-fidelity-report:C15 (item 5.21); qa-master-contract-fidelity-report:C16 (item 5.21); qa-numbers-metrics-report:C1 (item 5.18); qa-numbers-metrics-report:C2 (item 5.18); qa-numbers-metrics-report:C3 (item 5.18); qa-numbers-metrics-report:C4 (item 5.18); qa-numbers-metrics-report:C5 (item 5.18); qa-numbers-metrics-report:C7 (item 5.18); qa-numbers-metrics-report:C8 (item 5.18); qa-numbers-metrics-report:C9 (item 5.18); qa-numbers-metrics-report:C10 (item 5.18); qa-numbers-metrics-report:C11 (item 5.18); qa-numbers-metrics-report:C12 (item 5.18); qa-numbers-metrics-report:C13 (item 5.18); qa-numbers-metrics-report:C14 (item 5.18); qa-numbers-metrics-report:C15 (item 5.18); qa-numbers-metrics-report:C16 (item 5.18); qa-numbers-metrics-report:C17 (item 5.18); qa-numbers-metrics-report:C18 (item 5.18); qa-template-conformance-report:C1 (item 5.13); qa-template-conformance-report:C2 (item 5.13); qa-template-conformance-report:C3 (item 5.13); qa-template-conformance-report:C4 (item 5.13); qa-template-conformance-report:C5 (item 5.13); qa-template-conformance-report:C6 (item 5.13); qa-template-conformance-report:C7 (item 5.13); qa-template-conformance-report:C8 (item 5.13); qa-template-conformance-report:C9 (item 5.13); qa-template-conformance-report:C10 (item 5.13); qa-template-conformance-report:C12 (item 5.13); qa-template-conformance-report:C13 (item 5.13); qa-template-conformance-report:C14 (item 5.13); qa-template-conformance-report:C15 (item 5.13); qa-template-conformance-report:C16 (item 5.13); qa-template-conformance-report:C17 (item 5.13); qa-template-conformance-report:C20 (item 5.13)
