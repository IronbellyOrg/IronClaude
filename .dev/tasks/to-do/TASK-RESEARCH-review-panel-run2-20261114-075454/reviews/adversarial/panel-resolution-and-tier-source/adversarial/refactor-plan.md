# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (Proposal B, `variant-2-original.md`), selected by the tiebreaker (debate performance: B 6 pure wins, A 2); raw scores A 0.8969, B 0.8767, margin 0.0202 (`base-selection.md`).
- Incorporating strengths from: Variant A (Proposal A, `variant-1-original.md`), and the agreed hybrid texts of both advocates (`round2-advocate-A.md` and `round2-advocate-B.md`, section 6 each). Convergence: 24 of 25 diff points (96%) converged; the sort key of the slot order (C-007) is open; B's `slot_order` key and library helper functions (inside C-004) and B's section 4 (g) additions are unanswered by A (A had no turn after B's Round 2).
- Source rule for every change: the debate must already contain the text or the conclusion; the merge adds no new design decision. Each change cites its debate source. Where the debate left a point open (C-007 sort key; B's `slot_order` and library helpers; B's (g) additions; the 13 UNADDRESSED findings of the invariant probe), the merged document states the point as open, with both sides' evidence, and does not resolve it. Text that only one advocate wrote and the other did not answer is tagged "B addition, unanswered by A" (or the reverse).
- Planned changes: 14 (9 integrations from A or from the agreed hybrid: Changes 1, 2, 4, 5, 6, 7, 8, 11, 13; 4 corrections or removals of base claims the debate refuted, the author conceded or both sides dropped: Changes 3, 9, 10, 14; 1 structural edit from the scorer evidence: Change 12).
- Merged output file: `merged-panel-resolution-and-tier-source.md` in the output directory (one level above `adversarial/`).
- Risk level: High overall (Change 4: the open sort key). Changes 1, 3, 5, 8, 9, 10, 12 and 14 modify or remove base text; Changes 2, 6, 7, 11 and 13 are additive.
- Order of application on shared sentences: Change 3 and Change 5 first, then Change 10 (it rewrites sentences those two also touch: section 5 item 2, section 7 point 1), then Change 12 (move and renumber), then Change 13.

### Merge conventions (label and reference integrity; from the plan review)
- Evidence labels of the base (E1-E10) stay; the base's evidence item "E2" is written "evidence item E2" and the experiment is always written "the E2 experiment" or "the E2 harness", never bare "E2" in a sentence that could mean either.
- Measurements are cited with the author: "A's M1 to M3" (Variant A section 5.1) and "B R2 M1 to M9" (B's Round 2 evidence).
- The probe findings are written "FF-INV-001" to "FF-INV-026" in the merged text, to avoid the clash with "C-02 INV-001" and "C-03 INV-007" (adjudicated slots) and with the synth-06 INV-A to INV-N. Diff-point ids (C-001 to C-010, X-, S-, A-) are not used in the merged text except in the "Open items" section, where the open sort key is named "the sort key of the slot order (diff point C-007)".
- Do not copy A's two mis-pointed internal references ("see 3.4" in A 2.3 item 4; "5.1 above lists why" in A 5.2). After Change 12, a reference scan must show every "section N" and "E-n" reference resolves.

## Planned Changes

### Change 1: Ownership statement as a "today versus proposed" table with the merged wording (from Variant A and both Round 2 hybrids)
- **Source**: Variant A, section 2.1 (the 7-row table: tier order and membership, class, vendor, launch, slot lists of ccsession, model id behind a slot, E2 ladder); `round2-advocate-A.md` section 6 item 1 and `round2-advocate-B.md` section 6 item 1 (merged wording).
- **Target**: Base, section 2 item 1 (replace) and section 1 (paragraph, edit "snapshot" wording).
- **Rationale**: C-001 hybrid 75% and S-002 hybrid 68% in the scoring matrix. Both advocates accepted: "Which models a tier holds, and in what order, is decided in the Coder env slots that `ccsession-models.json` names and that `MODEL-TIERS.md` describes. The packaged `review-tiers.default.json` is the reviewed copy `panel resolve` reads, held in step with those by the guard; it alone holds `classes`, `names`, `available`, `stand_ins` and `launch`." plus B's clause that the guard does not read the workspace env (documented order is Coder env first, `MODEL-TIERS.md:189-193`). "Snapshot" is replaced by "reviewed copy, checked by test" (A R2 section 4(b), B R2 section 4(b) AGREE). A's "single source" and "the one file" wording is NOT carried over (A conceded, X-006, 80% B).
- **Integration point**: replace the base's six-statement ownership list (2.1) by the A table adapted to the merged wording (columns Today / Under the merged position), keep B's repo-only layer note; remove the sentence "Nothing in the packaged file is called the single source of membership" in favour of the merged wording. Row rewrites of A's seven rows: tier order and membership -> the merged wording (not "the file is the owner"); class -> the tier file stays the only class owner (unchanged); vendor -> the existing substring table stays, plus the parity test of Change 7 (the `vendors` map row is dropped); launch -> unchanged (C-07's decision); slot lists of ccsession -> checked by the guard of Change 2; model id behind a slot -> "stays in the Coder env; the env leg is deferred (a read-only `panel check` only if drift is observed)"; E2 fallback ladder -> row dropped (deferred item in the open-items section). Add a one-line pointer after the merged wording: "the guard covers only the packaged copy; an override tier file (`--tiers`, `$SUPERCLAUDE_REVIEW_TIERS`, project or home `.superclaude/review-tiers.json`) replaces it silently: FF-INV-005, left open".
- **Risk**: Low. Wording and presentation; both advocates agreed on the text.

### Change 2: Drift guard as one test with parser rules, mutation tests and the names/classes assertion (from the agreed hybrid)
- **Source**: `round2-advocate-A.md` section 6 item 2 (parser rules: find the table by its header cell, map `**Tier 2b**` to `tier2b`, read only column 3, a missing header, row or empty cell raises; mutation tests: swap two ids, substitute an id, drop a row, rename the column header) and `round2-advocate-B.md` section 6 item 2 (adds: every id in every packaged tier list has a `names` and a `classes` entry, extending `test_review_panel_live7.py:83`; keep the retained mutation case `:101-106` and the pins `test_ccsession_tiers.py:221-222`).
- **Target**: Base, section 2 item 2 and section 5 item 1 (extend).
- **Rationale**: C-002 Variant B 90%; A adopted B's guard in Round 2; the fault-finder reproduced that the parse is green today for all six tiers (INV-006, ADDRESSED).
- **Integration point**: keep B's text; append the parser rules and mutation list; state that the env is not a leg of any test (A R2 section 4(b)); keep the optional read-only `panel check` as deferred.
- **Risk**: Low. Additive.

### Change 3: Distinctness: remove the per-profile `distinctness` field and the "profiles" mechanism from the base (correction of a base element)
- **Source**: `round2-advocate-B.md` section 1 W-2 (CONCEDE: "I withdraw hybrid item 3's profile field") and section 4 (a2) AGREE; `round2-advocate-A.md` section 4 (a2); code evidence `panel.py:174-176` (closed `_PANEL_KEYS`) and that no profile object exists (diff V-5).
- **Target**: Base, section 2 item 4 (rewrite), section 2 "Named modules" bullets (Tasklist, PR review, rf-qa), section 5 item 2 new-test list (drop "the spec profile resolves soft and records neither key"), section 6 bullets, plus the stale base sentences that presuppose the field: section 1 paragraph ("a module profile ... opts into strict"), section 4 INV-A ("optional keys only when a profile asks"; its "[UNVERIFIED]" on extra resolution keys is now supported by `recompute_parity` reading only `reviewers` and `tiers_sha256`, `reflect_shadow_exit.py:125-137`, both advocates A-006), section 8 ("B's per-profile `distinctness` follows that same split").
- **Rationale**: C-003 Variant B 83% (soft stays the default) and (a2) both advocates AGREE: reflect already declares strictness by passing `--strict-distinct` (`SKILL.md:340`, `test_shadow_skill_contract.py:243-246`, `test_shadow_exit_script.py:27`); the loop is soft by omission; build nothing now, revisit when a second strict consumer exists. The soft-default text of the base stays.
- **Integration point**: section 2 item 4 becomes: resolver and CLI keep today's soft default; `--strict-distinct` stays the opt-in flag; no `--allow-repeat`; no profile field or table; a consumer that wants strictness passes the flag. Remove "Reflect profiles are `strict`" as a new mechanism and "each declares its own `distinctness`" in the named-module bullets and replace by "passes the flag as reflect does".
- **Risk**: Medium. Several sections reference the removed field (2 item 4, named modules, section 5 item 2, section 6 PR and rf-qa bullets); all references must be updated together.

### Change 4: Scarcest-tier-first order as the CLI's slot order, with the sort key shown as OPEN (from Variant A, repaired)
- **Source**: Variant A, section 3.3 third bullet and section 2.3 item 4; `round2-advocate-A.md` section 6 item 4 (keyword `scarcest_first`, library default False, CLI passes True for soft and strict, fixed slots first, `reviewers` emitted in emission order `fixed + rest` in template order, `template_sha256` stays the hash of the real template; tests listed there); `round2-advocate-B.md` section 6 item 4 (same placement; key CONTESTED: ascending number of candidates the selected environment can serve, ties by template order). B additions, unanswered by A: the `skipped_slots` re-sort to emission order (B R2 section 2 weakness 3), and tests (vii) placeholder tier fails closed through the CLI, (viii) `skipped_slots` in emission order under a hard exclusion that skips two slots, (ix) many-seed property test replacing the one-seed assertion at `test_review_panel_live7.py:109-125`. Test (i) (CLI parity for the eight packaged templates in anthropic-only) is the test that fails on A's raw key (B R2 M2, FF-INV-012); it is shown only inside the open-key paragraph as "the test that tells the two keys apart", not in the required-test list.
- **Target**: Base, new item 4a in section 2 (insert after the distinctness item); section 3 (add the measured evidence); section 5 (add tests).
- **Rationale**: X-002 hybrid 90%; both advocates AGREE (c0) on placement: 345 and 693 of 1000 gateway panels repeat a model in template order, 0 with scarcest-first, panel size 4 and 7 in 1000 of 1000; soft+scarcest-first equals strict+scarcest-first in the gateway in 1000 of 1000 runs. C-007 is NOT agreed on the key: A (`len(aliases[tier].models)`, "A, repaired" 70%) against B (servable-candidate count, 75%); B's M2 (A's key changes anthropic-only strict resolutions of `default` and `live7` in 1000 of 1000 runs while 681 tests still pass) is unrebutted in the debate and reproduced by the fault-finder (INV-012, MEDIUM, UNADDRESSED).
- **Integration point**: state the agreed part as the position; state the key as an open decision with both options, B R2 M2 and the FF-INV-012 finding, and the test that tells the keys apart (B's CLI parity test, not among the agreed items). Carry A's `shortcut:` note with A's own wording ("ascending model count; upgrade to models-per-demanded-slot when a custom template is skipped under it", A Round 2 section 6 item 4) and B's upgrade condition as B wrote it (B R2 section 6 item 4). State FF-INV-019 (MEDIUM, open: scarcest-first with two excluded classes on `live7` falls below the optimum in 27 of 1840 resolutions and below today's template order in 3).
- **Risk**: High. This is the one point the debate left open, and the item touches the pinned reviewer order for reflect personas (`reflect_shadow_exit.py:133-153`). The merge must not choose a key.

### Change 5: Record keys written by the CLI, always; B's two small additions marked contested (modifies base section 2 item 5)
- **Source**: `round2-advocate-A.md` section 6 item 5 and `round2-advocate-B.md` section 6 item 5: the CLI adds `requested_slots` (template count when the kind is in `apply_to`, else 1, the one fixed slot `validate_panel` requires, `panel.py:245-246`) and `distinct_models` to every resolution; the library output is unchanged (0 pins in the CLI against 17 in the library: 16 byte-identity parameters plus the packaged-tier golden; the 17 counts are by reading, the 0 at the CLI is simulated in-process by both advocates, A with 661 tests and B with 681, FF-INV-024 calls it a prediction until code exists); no stderr line (A counted 5 CLI tests that parse `res.output` and fail; B verified the mechanism, not the count), no `shortfall`, no `distinctness`, no resolve-time exit rule beyond the existing anchor exhaustion.
- **Target**: Base, section 2 item 5 (rewrite: "written only when a profile or flag asks" becomes "always written, by the CLI") and the denominator discussion in section 8 and section 7.
- **Rationale**: C-004 hybrid 78%, X-001 hybrid 83% (B conceded that the base text left the soft consumer's repeat invisible). Contested and kept as such: B's `slot_order` key and the library helper functions (B R2 section 4 (d2); A had no turn after it).
- **Integration point**: rewrite item 5; also update the stale base sentences that tie the keys to a profile: section 4 INV-A, section 5 item 2 (replace the removed "records neither key" test by the agreed tests: the CLI output carries both keys for every packaged template and kind; the library output carries neither, the 16 byte-identity parameters and the packaged-tier golden stay as they are; `requested_slots == len(reviewers)` in an unconstrained gateway run for every packaged template and kind), and section 8 (the denominator sentences, applied after the section is moved by Change 12). Add a one-sentence note that `requested_slots` is a source for `requested` in C-02 INV-001 and C-03 INV-007 and that what merge does with it stays C-03's; list the two B additions under "Open items" (tagged "B addition, unanswered by A"). Add the fault-finder warnings FF-INV-010 (the formula follows `apply_to`, not the kind name; partly resolved here because the base already states the `apply_to` branch, the test over an `apply_to` holding both kinds is still missing) and FF-INV-021 (the spec loop does not pass the resolution to merge) next to it.
- **Risk**: Medium. The CLI/library placement changes which tests see the keys.

### Change 6: Spec loop prompt not edited, with the pinned and mirrored evidence (from Variant A, N3)
- **Source**: `round2-advocate-A.md` section 3 N3 and section 6 item 6; `round2-advocate-B.md` section 1 (N3 verified, `cmp` byte-identical mirror); (f) AGREE.
- **Target**: Base, section 2 "Named modules" first bullet (extend) and section 4 (INV-C, INV-D).
- **Rationale**: C-009 Variant B 88%, X-007 Variant B 90%. The prompt line is pinned (`test_review_rules_text.py:21, 31`) and mirrored under `plugins/`; the loop gains distinct gateway panels from the order (Change 4) and a visible record (Change 5).
- **Integration point**: add the evidence; keep the base's "unchanged; soft". Qualify the outcome sentence "the loop gains distinct gateway panels" with "(distinct requested ids; served identity is the subject of slot C-08; FF-INV-026, which also needs FF-INV-001 environment detection and FF-INV-005 no override tier file)".
- **Risk**: Low.

### Change 7: Class and vendor: parity test, no `vendors` map (keep base; add verified facts)
- **Source**: `round2-advocate-A.md` section 1 B-W6 and section 6 item 7; `round2-advocate-B.md` M8 (`_vendor_from_model_id` maps all 13 packaged ids and `muse-ember-1.0`, which gives `meta`).
- **Target**: Base, section 2 item 6 (extend).
- **Rationale**: C-006 Variant B 80%; A withdrew the `vendors` map and the environment marker list. FX-14 (detection by `T3Model01` alone) stays open under both; the fault-finder adds INV-001 (MEDIUM) on the two-source view of the environment.
- **Integration point**: keep B's test; add the verified facts; state FX-14 as open.
- **Risk**: Low.

### Change 8: Ember: union edit list (from both advocates)
- **Source**: `round2-advocate-A.md` section 6 item 8 and `round2-advocate-B.md` section 6 item 8.
- **Target**: Base, section 2 "muse-ember-1.0" bullet (replace) and section 4 (cross-repo ordering).
- **Rationale**: C-005 hybrid 75%, X-004 hybrid 70%, X-005 Variant A 78% (B's list omitted the packaged-list edit). Order: Coder `defaults.sh` slot (outside this repo); in this repo `ccsession-models.json` `T4Model04`; `aliases.tier4.models` at the index the Coder env gives; `names` and `classes` in the same change (`validate_reflect_profile` rejects a tier4 model with no `classes` entry in all six reflect templates, `panel.py:112-125`); the `MODEL-TIERS.md` tier 4 row; `test_ccsession_tiers.py:222` and `test_review_panel_live7.py:94-96` updated; `panel-golden-packaged-tiers.json` regenerated once; `make sync-dev` then `make verify-sync`. No Python source change. Slot index 02 against 04 stays the owner's (GQ-046). Add the tier-size coupling clause (B R2 M4: adding ember changed a non-tier4 reviewer in `live7` gateway resolutions in about 20 to 27 percent of run ids under a count-based order).
- **Integration point**: replace; carry the fault-finder warnings INV-009, INV-017 and INV-018 (UNADDRESSED, MEDIUM/LOW) under open items.
- **Risk**: Low.

### Change 9: INV-L accounting sentence and goldens (replaces base's "INV-L preserved" claim)
- **Source**: `round2-advocate-A.md` section 4 (e) and `round2-advocate-B.md` section 4 (e), AGREE.
- **Target**: Base, section 4 (INV-L bullet and "Frozen goldens" bullet) (replace).
- **Rationale**: C-008 hybrid 73%. The base's claim holds only until the first packaged-file edit. Sentence: "INV-L holds until the first edit of the packaged file; any such edit changes `tiers_sha256`, after which `recompute_parity` reports an earlier run as not proven (`reflect_shadow_exit.py:128-132`), by design of that script; the CLI-layer keys change neither `tiers_sha256` nor `template_sha256`." `panel-golden-packaged-tiers.json` regenerated once, for ember; the frozen-copy golden untouched.
- **Integration point**: replace both bullets with the sentence and the golden statement.
- **Risk**: Medium. The base's "Preserved" list loses INV-L as unconditional.

### Change 10: Correct the base claims the debate refuted or the author conceded
- **Source**: `round1-advocate-B.md` section 5 concessions 1-3 and `round2-advocate-B.md` section 1 W-1, W-3; diff-analysis X-001, X-002, X-003, X-005; A-001 (1000 run ids).
- **Target**: Base, section 7 answer point 1 ("The repeat is not silent under B"), section 7 point 2 ("unresolvable"), section 3 E4 (counts), section 5 item 2 ("pins must pass unmodified"), section 2 "muse-ember-1.0".
- **Rationale**: the base text contains statements the debate showed wrong. Edits: section 7 (1): the repeat is visible through the always-written `distinct_models` (Change 5), not "not silent" by profile; section 7 (2): strict in anthropic-only resolves 2 reviewers with no exception (1000 of 1000 runs) and a floor of `min(2, requested)` never fires there, so "makes the default panel unresolvable" is deleted; E4: report the 1000-run figures (345 and 693 of 1000, not 18 and 30 of 40) and say that the gateway shrinkage is an artifact of template order (0 with scarcest-first), the anthropic-only 2 is inherent; "pins unmodified" is restated for the merged design (CLI-layer keys: 0 pins, simulated; the strict-default flip, now dropped, would have moved 3 to 4): the packaged-tier golden `test_review_panel_reflect_profile.py:74-88` is removed from the "must pass unmodified" list because ember regenerates it once, and the only pin edits are the three ember ones (`panel-golden-packaged-tiers.json` regenerated, `test_ccsession_tiers.py:222`, `test_review_panel_live7.py:94-96`). Add A's candour sentence (A section 4.2: "I do not call that 'pins unmodified'", and section 0: the merged design does not claim C-01 condition 3 "all existing pins pass unmodified" for these three).
- **Integration point**: in-place rewrites of the cited sentences; applied after Changes 3 and 5 (shared sentences).
- **Risk**: Medium. These sentences carry B's objection answer; the rewrite must keep the answer's structure.

### Change 11: Measurements and concessions from Variant A (M1-M3, 7.4) added to base section 5 and section 7
- **Source**: Variant A section 5.1 (M1 soft versus strict versus declared repeat on ground-truth packages, with the metric of record; M2 shortfall rate over `run1..run1000`; M3 drift between sources), section 7.4 (the single-source claim and the strictness default can be judged apart), section 7.5 (open owner question GQ-050/Q-5).
- **Target**: Base, section 5 (append as items 6-8) and section 7 (append a closing "what the debate left unmeasured").
- **Rationale**: U-003 High unique contribution; both Round 2 deferred lists put "the strictness default as a measured question (M1)" and "the env leg of the guard (only if M3 shows drift)" under Deferred.
- **Integration point**: append; relabel A's M-numbers as "A's M1 to M3" to avoid the clash with B R2's evidence labels. Restate the superseded parts as the debate corrected them: A's M2 uses the 1000-run figures (345 and 693 of 1000 gateway panels repeat a model in template order, 0 with scarcest-first) instead of "30 of 40 and 0 of 40" (shared assumption A-001, QUALIFY); A's 7.4 is reworded "the ownership wording and the strictness default can be judged apart" (the "single-source" wording was conceded, X-006, and the per-profile mechanism was withdrawn, Change 3); M1's third arm is described as "a repeat chosen by hand (the E2 style)" because `--allow-repeat` was dropped.
- **Risk**: Low. Additive.

### Change 12: Dependence section moved before the design (scorer-driven structure edit) and a debate-outcome block
- **Source**: scorer evidence S1 in `scorer-pass1.md` and `scorer-pass2.md` (B NOT MET: the dependence on C-01..C-03 is section 8 although section 2 items 4-5 rely on it). This is a scorer-driven structure edit; the debate itself scored S-001 (placement of the consistency material) "Neither (tie) 65%". The "Debate outcome" block is drawn from `debate-transcript.md` (convergence assessment) and `base-selection.md`, not from a variant.
- **Target**: Base section 8 (move to a new section 0; keep the text, then apply Changes 3 and 5 to it, since those edit sentences inside it). Add a short "Debate outcome" block at the top: winner (hybrid on Variant B as base), convergence (24 of 25 points, 96%), unresolved point (the sort key of the slot order).
- **Rationale**: structure only; no content decision.
- **Integration point**: the moved text becomes a new section 0 (sections 1 to 7 keep their numbers); the Open items of Change 13 becomes section 8 only after every remaining reference to the old "section 8" is rewritten to "section 0"; otherwise it is section 9. Update the references ("section 3, E9", "section 8").
- **Risk**: Medium. Renumbering and a reused number can break internal references (scorer DC metric); validation re-scan required.

### Change 13: Open items left by the debate (new final section)
- **Source**: `invariant-probe.md` (13 UNADDRESSED: INV-001, 003, 004, 005, 009, 010, 011, 012, 017, 018, 019, 021, 026; MEDIUM: 001, 005, 009, 010, 012, 019, 021, 026; LOW: 003, 004, 011, 017, 018) and the unresolved diff point C-007.
- **Target**: Base, new final section "Open items left by the debate".
- **Rationale**: the adjudication must report the invariants the debate left unaddressed; the merged document must not present the open points as settled.
- **Integration point**: table with ID (written FF-INV-nnn, see the merge conventions), category, assumption, severity, copied from the probe (assumption text may be shortened to one sentence; evidence not required) plus the contested items (the sort key of the slot order, diff point C-007; B's `slot_order`; B's library helpers; B's section 4 (g) additions), each tagged with its owner and "unanswered by A" where applicable. A second table carries the Deferred list of both Round 2 hybrids (item 9 of each) verbatim: the env leg of the guard (a read-only `panel check`, only if drift is observed), the E2 ladder as a function of (tier, model), the strictness default as a measured question (A's M1), the minimum acceptable panel per consumer (shared assumption A-004; C-03, C-10, C-11), the profile declaration (when a second strict consumer exists), any tooling outside this repo that re-resolves a first review by run id [UNVERIFIED], and the shim's failover behaviour (shared assumption A-005, [UNVERIFIED]); plus the "what I did not verify" lists of both Round 2 files (wheel carries `ccsession-models.json`, which gate keeps the `plugins/` loop-prompt mirror identical, the `SKILL.md:1248` class set, whether a test asserts the `SKILL.md:340` text).
- **Risk**: Low. Additive.

### Change 14: Remove the env overlay (layer 2) from the base text (a base element dropped by both advocates)
- **Source**: `round1-advocate-B.md` concession 4 and `round2-advocate-B.md` section 1 (overlay dropped); `round2-advocate-A.md` section 1 ("AGREE; both Round 1 hybrids drop it"); scoring matrix C-010 Variant A (no overlay) 85%.
- **Target**: Base, section 2 item 3 (second sentence, the overlay), section 3 E9 (keep only as a note under "considered and dropped"), section 4 "Reproducibility of a resolution" bullet, section 5 item 5 (overlay check), section 6 PR-review bullet ("once the overlay exists", and the same phrase in the Tasklist, PR review and rf-qa named-module bullet), section 7 answer (4) (the "optional overlay" clause), section 1 paragraph.
- **Rationale**: no planned change removed the overlay from the base in the first draft; without this the merged text would still describe a mechanism both sides dropped (reason: a per-workspace `tiers_sha256` that `recompute_parity` reports as not proven, A's strength 6; B's E9 calls it the weakest layer).
- **Integration point**: delete or reword each listed sentence; keep one sentence "an env overlay was considered and dropped: it would give a per-workspace `tiers_sha256`".
- **Risk**: Medium. Several sections reference it; all must change together (re-grep for "overlay" after the merge).

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-003 | Variant A: `panel resolve` default becomes strict, `--allow-repeat`, `distinctness: soft` recorded | A withdrew it in Round 2 (3 to 4 CLI pins, a 3-file prompt change with a lag window, no consuming beneficiary; gateway soft+scarcest-first equals strict+scarcest-first in 1000 of 1000 runs). Base soft default kept (83%). |
| C-004 | Variant A: `expected`, `shortfall`, stderr line, resolve-time exit rule | Withdrawn: derivable as `requested_slots - len(reviewers)`; stderr breaks 5 CLI tests parsing `res.output`; the rule never fires in anthropic-only (2 is not below `min(2, requested)`). |
| C-006 | Variant A: new top-level `vendors` map and an environment marker-variable list | Withdrawn by A: `_vendor_from_model_id` classifies all 13 ids and ember; the marker list needs a validator edit (`panel.py:371-373`); base keeps one parity test. |
| C-001 | Variant A: "the one file" / "single source" ownership claim | Conceded as an overclaim (X-006, 80% B); replaced by the merged wording (Change 1). |
| C-010 | Base element dropped: B's layer 2 env overlay (not an A approach) | Dropped by both advocates (weakest layer, per-workspace `tiers_sha256` reads as "not proven"); the removal itself is Change 14; recorded as considered and dropped. |
| C-009 | Variant A: loop prompt declares its distinctness | Not edited (pinned by `test_review_rules_text.py:21, 31`, mirrored under `plugins/`; 88% B). |
| C-002 | Variant A: count-and-first-model check extended to six tiers | Superseded by the ordered derive-and-compare (90% B). |
| U-002 | Variant A: E2 fallback ladder as a function of (tier, model) | Deferred by both Round 2 hybrids (concerns the harness, not `panel resolve`); kept as a deferred item, not a planned change. |
| C-007 (part) | Either sort key | Not chosen: the debate did not conclude; shown as open (Change 4). |
| Env test leg | An env-equality pytest | Not adopted: the documented order is Coder env first, repo second (`MODEL-TIERS.md:189-193`), so such a test would turn Coder workspaces red between releases; only a read-only `panel check` if drift is observed (deferred). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Ownership wording inconsistent between sections 1 and 2 | Restore base text of sections 1 and 2 item 1 |
| 2 | Low | Guard description incomplete | Remove the appended parser rules |
| 3 | Medium | A dangling reference to the removed `distinctness` field remains in another section | Re-grep for `distinctness` after merge; restore the base item 4 |
| 4 | High | The open sort key is silently decided, or reflect persona order is misdescribed | Remove item 4a; keep both options only in "Open items" |
| 5 | Medium | The CLI/library placement is misstated, so the 0-versus-17 pin claim is wrong | Restore base item 5 and keep Change 5 text only in open items |
| 6 | Low | Additive evidence | Remove the added sentences |
| 7 | Low | Additive evidence | Remove the added sentences |
| 8 | Low | Ember list incomplete or wrongly ordered | Restore base ember bullet |
| 9 | Medium | INV-L stated as preserved without its condition | Restore base INV-L bullet and keep the new sentence in open items |
| 10 | Medium | The objection answer loses coherence after in-place edits | Restore the base sections 7 and 3 E4 |
| 11 | Low | Additive; M-label clash | Remove the appended items |
| 12 | Medium | Broken internal references after renumbering | Re-run the reference scan; revert to the base numbering |
| 13 | Low | Additive | Remove the final section |
| 14 | Medium | A sentence still describes the dropped overlay | Re-grep for "overlay" and "tiers_source"; restore the base text of the affected sentence |

## Review Status
- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (--interactive)
- Analytical review: `plan-review.md` (22 checks, 14 FINDINGs, 0 HIGH); all 14 were applied to this plan (source attributions, merge conventions, Change 14, ordering of shared sentences, restated figures).
- Approved by: auto
- Approval timestamp: 2026-11-14T17:09:00Z
