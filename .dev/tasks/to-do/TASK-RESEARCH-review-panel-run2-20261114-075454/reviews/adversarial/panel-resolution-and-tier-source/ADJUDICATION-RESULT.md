# Adjudication Result: slot C-09 (panel-resolution-and-tier-source)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage`, Mode A, two advocates, Round 1 parallel, Round 2 sequential (A then B), Round 2.5 independent invariant probe, hybrid scoring with two position-bias passes and a re-evaluation, plan reviewed by an analytical agent, merge by the merge-executor. Return contract: status `partial`, convergence score 0.96 (24 of 25 diff points, threshold 0.80, CONVERGED).

## Winner

A named hybrid that the debate itself produced: the hybrid both advocates converged on in their Round 2 section 6 texts, merged onto Variant B (Proposal B) as the base.

Base selection, as the debate concluded it (`adversarial/base-selection.md`): **Variant B (Proposal B) is the selected base.**
- Quantitative (mean of the two scoring passes): A 0.9605, B 0.9533.
- Qualitative after the position-bias re-evaluation (6 of 60 criterion-variant pairs disagreed): A 25/30 = 0.8333, B 24/30 = 0.8000. Both pass the edge-case floor (5/5 each).
- Combined: A 0.8969, B 0.8767; margin 0.0202, below the 5% threshold, so the tiebreaker applied. Level 1 (debate performance): Variant B 6 pure wins (C-002, C-003, C-006, C-009, X-006, X-007), Variant A 2 (C-010, X-005), 9 hybrid, 8 neither or qualify, 1 contested (C-007); 24% against 8%, so level 2 was not reached. Even if C-007 is credited to A, B keeps the lead 6 to 3.

Contents of the hybrid (from the section 6 texts of both Round 2 files, as carried in the merged document):
1. Ownership wording: the Coder env slots that `ccsession-models.json` names, described by `MODEL-TIERS.md`, decide which models a tier holds and in what order; the packaged `review-tiers.default.json` is "the reviewed copy `panel resolve` reads, held in step with those by the guard"; it alone holds `classes`, `names`, `available`, `stand_ins` and `launch`. No env overlay, no `vendors` map, no env marker list.
2. Guard: one test replaces `_assert_tiers_match_ccsession_slots`: the ordered ids of `aliases.<tier>.models` for tier1a to tier4 equal column 3 of the `MODEL-TIERS.md` section 1 table, and the counts equal `len(models_env)`; parser rules and mutation tests; every listed id has a `names` and a `classes` entry; the env is not a test leg.
3. Distinctness: soft stays the default in the library and the CLI; `--strict-distinct` stays the opt-in flag; no `--allow-repeat`, no per-profile field, no stderr line, no resolve-time exit rule beyond fixed-anchor exhaustion.
4. Order: scarcest tier first as the CLI's slot order for soft and strict, `panel.resolve` keeping today's order behind a keyword, `reviewers` in emission order, `template_sha256` unchanged. The sort key is NOT decided (see Unresolved).
5. Record: the CLI always writes `requested_slots` and `distinct_models`; the library output is unchanged.
6. The spec loop prompt is not edited. 7. Class and vendor: one parity test, no vocabulary merge. 8. Ember: the union edit list (Coder slot first; `ccsession-models.json` `T4Model04`; `aliases.tier4.models`; `names` and `classes` in the same change; the `MODEL-TIERS.md` tier 4 row; `test_ccsession_tiers.py:222` and `test_review_panel_live7.py:94-96`; golden regenerated once; `make sync-dev` and `make verify-sync`). 9. INV-L accounting sentence: any packaged-file edit changes `tiers_sha256`, after which `recompute_parity` reports earlier runs as not proven.

## Rationale

Both advocates conceded most of their own over-claims before Round 2 ended. Variant A's advocate withdrew the strict default and `--allow-repeat`, the `vendors` map, the env marker list, the stderr line, the resolve-time exit rule, the loop-prompt edit and the "single source" wording; Variant B's advocate withdrew the per-profile `distinctness` field and the env overlay, and conceded that its keys left the soft consumer's repeat invisible and that its ember steps omitted the packaged-list edit. What survived from each side: from B, the ordered derive-and-compare guard (C-002, 90%), soft as the default (C-003, 83%), the class and vendor treatment (C-006, 80%), the unedited loop prompt (C-009, 88%); from A, the scarcest-first slot order, measured on 1000 run ids (345 and 693 of 1000 gateway panels repeat a model in template order, 0 with scarcest-first, panel size 4 and 7), and the always-written record placed in the CLI layer (0 pins at the CLI against 17 in the library). Variant B was selected as base because the raw score margin was inside the 5% band and the debate performance tiebreaker went to B, 6 pure wins to 2.

## Conditions under which the winner holds

Each condition is one the debate itself stated or the invariant probe recorded:
- The CLI-layer placement holds only while the keys and the order are applied in the CLI and the library default stays today's order; written in the library the keys would move 17 pins (16 byte-identity parameters plus the packaged-tier golden). The "0 pins at the CLI" figure is an in-process simulation by both advocates (661 and 681 tests), a prediction until the code exists (probe INV-024).
- The gateway benefit (no repeated model, full panels of 4 and 7 in 1000 of 1000 runs) holds for the packaged gateway lists, `distinct_across_slots: true`, no hard exclusion, the gateway environment and no override tier file (probe INV-023; the probe's INV-019 shows two excluded classes on `live7` fall below the optimum in 27 of 1840 resolutions).
- In anthropic-only, strict gives 2 reviewers in 1000 of 1000 runs, which is a count and not diversity (shared assumption A-004 answered QUALIFY by both); the minimum panel per consumer stays with C-03, C-10 and C-11.
- The soft default stands until Variant A's M1 (soft versus strict versus a hand-chosen repeat at equal reviewer count on ground-truth packages) is run; Variant B's section 5 item 4 test needs the served-model record of C-08.
- The guard compares the package with `MODEL-TIERS.md` and the slot counts, not with the workspace env, because the documented order is Coder env first; a read-only `panel check` is only to be built if drift is observed (A's M3).
- The ember change is one change over several files and needs the Coder slot first; the slot index (02 or 04) is the owner's (GQ-046).

## Unresolved diff point and open items

- C-007, the sort key of the scarcest-first order: Variant A's `len(aliases[tier].models)` ("A, repaired", 70%) against Variant B's servable-candidate count (75%). Variant B's measurement M2 (A's key changes anthropic-only strict resolutions of `default` and `live7` in 1000 of 1000 runs while 681 tests still pass) was not answered inside the debate (A had no turn after B's Round 2) and the Round 2.5 probe reproduced it (INV-012). The merged document shows it as open.
- Also open and unanswered by A: B's `slot_order` key, B's library helper functions (inside C-004), and B's Round 2 section 4 (g) additions.
- Deferred by both Round 2 hybrids: the env leg of the guard, the E2 ladder as a function of (tier, model), the strictness default as a measured question, the minimum acceptable panel per consumer, the profile declaration (when a second strict consumer exists), external tooling that re-resolves a first review by run id [UNVERIFIED], the shim's failover behaviour [UNVERIFIED].

## Invariants the debate left unaddressed (from `invariant-probe.md`: 26 findings, 13 ADDRESSED, 13 UNADDRESSED)

Return contract `unaddressed_invariants` (HIGH only): empty. No HIGH UNADDRESSED finding, so the invariant probe gate did not block convergence.

MEDIUM (8, UNADDRESSED):
- INV-001 (state_variables): environment is detected once from the process env alone (`$T3Model01`), which may differ from the workspace view ccsession uses.
- INV-005 (guard_conditions): "the packaged file is the file `panel resolve` reads" fails when an override tier file (`--tiers`, `$SUPERCLAUDE_REVIEW_TIERS`, project or home file) replaces it; the guard reads only the packaged file.
- INV-009 (guard_conditions): "Coder slot first, then the repo edits" has no gate; merging the `T4Model04` line before every workspace env carries it breaks tier mode there.
- INV-010 (count_divergence): `requested_slots` follows `apply_to`, not the kind name; no test takes the branch where `apply_to` holds both kinds.
- INV-012 (count_divergence): the ascending-count sort key; the agreed tests cannot tell the two candidate keys apart (this is C-007).
- INV-019 (interaction_effects): scarcest-first with two excluded classes on `live7` falls below the optimum in 27 of 1840 resolutions and below template order in 3.
- INV-021 (interaction_effects): the spec loop does not hand the resolution to merge, so `requested_slots` does not reach the denominator of C-03 INV-007 there.
- INV-026 (sufficiency_challenge): "the loop gains distinct gateway panels" is true of requested ids only; the gateway has no dispatch mapping and served identity belongs to C-08.

LOW (5, UNADDRESSED): INV-003 (library and CLI orders differ without a trace in the artifact), INV-004 (statistics cover `fixed` and `random` slots only; a `round_robin` slot depends on the date), INV-011 (a fixed anchor with count above 1 can resolve two reviewers to one model), INV-017 (ember insertion index changes `fallback_depth` of Haiku), INV-018 (the ember edit list omits the `profiles` and `picker` entries that `MODEL-TIERS.md:189-192` names).

## Adversarial artifacts

Folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/panel-resolution-and-tier-source/`
- Merged output: `merged-panel-resolution-and-tier-source.md`
- `adversarial/variant-1-original.md`, `adversarial/variant-2-original.md` (normalized copies of Proposal A and B)
- `adversarial/diff-analysis.md` (Step 1: 3 structural, 10 content, 7 contradictions, 6 unique, 6 shared assumptions)
- `adversarial/round1-advocate-A.md`, `adversarial/round1-advocate-B.md`, `adversarial/round2-advocate-A.md`, `adversarial/round2-advocate-B.md`
- `adversarial/debate-transcript.md` (Step 2: transcript, scoring matrix, convergence)
- `adversarial/invariant-probe.md` (Round 2.5)
- `adversarial/scorer-pass1.md`, `adversarial/scorer-pass2.md`, `adversarial/scorer-reeval.md`, `adversarial/base-selection.md` (Step 3)
- `adversarial/refactor-plan.md`, `adversarial/plan-review.md` (Step 4)
- `adversarial/merge-log.md` (Step 5: 14 of 14 changes applied, post-merge validation PASS)
- `adversarial/return-contract.yaml`
