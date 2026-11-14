# Q11: which static report goes in the coordinator's chat

## Question (verbatim from the spec row)

merged-requirements.md section 3, row Q11: "Is #339's \"static report in chat every 3 to 5 minutes\" the sweep summary, `observe --once`, or both?"

ADJ Part 7 wording (alignment-findings-adjudicated.md:781): "Is the \"static report in chat every 3 to 5 minutes\" that #339 asks for the sweep's summary, the `observe --once` text, or both?"

## Spec's recommended answer

"The sweep summary only until the contract note exists" (merged-requirements.md:538; ADJ:781; origin V5 D2, variant-5-original.md:219-223 and Q7 at :294).

## Default if unanswered

"PLAN INFERENCE: sweep summary only" (merged-requirements.md:538). PLAN INFERENCE means the spec derived this itself; no debate file states it.

## What it gates

- No work item is scheduled on it. The row says "none scheduled; recorded in XC-01; informs section 6.7" (merged-requirements.md:538). XC-01 is the decision ledger (one row per owner decision); section 6.7 is the coordinator's status output rule.
- Graph edge 101: "Q11, Q31, Q32 -> XC-01, DEC, Recorded only; they gate no item" (merged-requirements.md:748).
- Section 6.7 already applies the recommended answer: "Q11's recommended answer applies to any in-chat report: the sweep summary only, until the note exists" (merged-requirements.md:1040).
- Wave needed by: "any".

## Facts the question depends on

1. #339 asks for a static report every 3 to 5 minutes "taking inspiration" from #409 (variant-5-original.md:221 citing the #339 body; variant-1-original.md:61, check C-33 "Verified"). The issue summary says the report would replace the usual end-of-message table (.dev/issues/339/issue-summary.md, "What the issue asks for").
2. The sweep's chat reply today is counts and report path only, and it is the one reply allowed to drop the DONE / NEXT table, under five conditions (src/superclaude/skills/sc-sweep-protocol/SKILL.md:31-43; src/superclaude/output-styles/pragmatic.md:22-23 on this branch).
3. The sweep runs at most once every 5 minutes; WC-16 (the worker-contract coordinator loop rule) is a cap, not a schedule (WORKER-CONTRACT.md:109 "at most once every 5 minutes"; ADJ glossary line 81; debate-transcript.md:625 "Phase 1 adds this duty, not a scheduler").
4. Every sweep run writes one report file (NFR-001, ADJ glossary line 83; X-004 at debate-transcript.md:904: "the only no-write static status is `observe --once`").
5. `superclaude observe --once [--width 80] [--ascii]` already prints a static plain-text record with no file write unless `--snapshot` is passed (ADJ E-17 at line 143; variant-5-original.md:126, O-16). The observer is built and merged (PRs #503, #514; ADJ glossary line 77); `src/superclaude/cli/observe/` exists in this checkout.
6. V5's D2 recommendation: "keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet. First step: none in code; the owner states the choice on #339" (variant-5-original.md:222-223). D1 is the contract note between observer and sweep (XC-05, unbuilt).
7. The observer's gate test Q-1 failed: an unbound terminal cannot read another terminal's Run (ADJ glossary line 87). Whether `observe --once` in the coordinator's own terminal shows that coordinator's Run is UNVERIFIED here.
8. Load: several observers plus the sweep plus the watcher were never measured together (INV-032; merged-requirements.md:502, :1032 "At most one `superclaude observe` instance for the coordinator's own view").
9. Section 6.7: automated status shows only outstanding owner decisions and held items (merged-requirements.md:1040, quoting SEED Batch 2 item 8).
10. The coordinator loop that would print a recurring report is unbuilt; no orchestrator that manages work exists yet.
