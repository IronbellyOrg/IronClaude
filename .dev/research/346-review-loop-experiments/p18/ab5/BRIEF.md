# Task: build the ab5 harness (ab4 + the PN1 panel). Do NOT launch any run.

SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad ; build root = $SP/p18/ab5 (create files there). Python stdlib only (`python3`), no git, no repo clone, no network, no Jev.

## Goal
ab5 = the ab4 pipeline whose first-review stage is the PN1 panel.
- ab4 = $SP/p16/ab4 (read READY.md first): PN2 lint pre-pass, k=2 first reviews (R1b adds the acceptance-criteria sweep sentence), deterministic merge with cleaned finding blocks, CLEANED verifier VF, revise V, scoped re-reviews R2/R3 with lint, frozen AUD/AUD2, `reconcile_confirmed`, token matcher `scan_by_prompt`, advance.py state machine, tests/test_ab4.py (21 tests).
- PN1 = $SP/p13/ab1 (harness.py, advance.py, rules.json, analysis.py, c93.py): independent reviewer panel R1.t1b-1, R1.t2-1, R1.t3-1, R1.t3-2 on model tiers (slots from the MODEL-TIERS table; stand-in handling for Haiku stratum), deterministic merge M1, adjudication step ADJ, typed finding ledger, V/L steps, R2/R3.
Final flow to implement for each run: lint-1 -> panel R1 (the same 4 reviewers/tiers/briefs as PN1, each also given the lint value as ab4 does) -> merge (PN1's merge across the 4 reports, but with ab4's cleaned `finding_block`/`clean_body`) -> ADJ (PN1's, where PN1 uses it) -> VF1 (ab4's clean verifier over the merged list; VF2/VF3 as ab4) -> V1 -> R2 (scoped, lint-2) -> [V2 -> R3 (lint-3)] as the loop requires -> AUD, AUD2 (always Sonnet, frozen). Keep 3 reviews / 2 fix cycles. The acceptance-criteria sweep sentence of ab4 goes on exactly one panel member: the R1.t1b-1 reviewer (the Sonnet-tier one), as R1b has it in ab4; the other three get the plain brief. Record this choice in READY.md.
Preserve byte-for-byte from the sources: the frozen audit command/rules and hashes, the spec and its sha, all brief texts you do not have to change, ids parsing (ab4's improved `ids_from`), `reconcile_confirmed`, token accounting (output tokens, each message id once; prompt-text/path matching so pasted or short "Read <path>/PROMPT.md" launches both match). Reuse by import or copy; where you copy, say which file and why.

## Names / strata
Root $SP/p18/ab5; runs d5-r1..d5-r6 (Sonnet stratum only; Haiku stratum NOT built; keep the code path but `build --stratum haiku` may refuse with a clear message). AUD/AUD2 Sonnet. MAX_CONCURRENT per drive.sh stays what ab4 has (6 runs at a time); one run issues up to 4 parallel R1 launches. Every state record and launch-ledger line carries stratum and model, as in ab4.

## Deliverables
1. harness.py, advance.py, supporting modules, decision.json (decision constants as data; cost never stops a run: D6), frozen/ (copy what ab4/PN1 need, with hashes), a rules/prompts file coherent with a 4-reviewer panel + lint (state any wording change in READY.md and the minimal diff).
2. $SP/drive.sh must work for `p18/ab5` (check how it dispatches; extend minimally as ab4 did, do not break other dirs).
3. tests/test_ab5.py: cover at least: panel briefs (4 reviewers, tiers/models, lint value present, AC sweep only on t1b), merge over 4 reports with cleaned blocks and dedup, ADJ prep, VF contamination guard, confirmed-line authority, ids parsing on real fixtures from ab4 and PN1 runs, token matcher on pasted and short launches, names/strata, a full fake loop R1 -> AUD2 -> analyze on fixtures. Run them and report the pass count.
4. `python3 harness.py build --stratum sonnet` builds d5-r1..d5-r6; `python3 advance.py --dry-run` works and writes the first prompts (PROMPT-R1.* and lint-1.md) without marking anything launched. DO RUN the dry-run and show the first LAUNCH lines. Do NOT run ./drive.sh (it is live), do not launch agents.
5. $SP/p18/ab5/READY.md in the style of ab4's: files, design items, where D2/D3/D4/D6 are encoded, tests, dry-run output, open questions. List every deviation from the sources.
6. An `analyze` that writes RESULTS.md with loop-only tokens per run and per step (so panel / merge / ADJ / VF / revise / re-review costs are visible), and the audit BLK numbers as ab4 does. (The 44-defect ledger scoring is run separately by the coordinator; you need only keep the final spec path per run easy to find: runs/<run>/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md.)

Be careful and verify against the sources rather than guessing; if a PN1 mechanism is ambiguous, choose the reading that keeps PN1's panel behaviour intact and say so. Final reply: DONE, test pass count, the first LAUNCH lines, and the list of open questions (short).
