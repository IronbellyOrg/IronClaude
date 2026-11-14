# Merge Execution Log

## Metadata
- Base: Variant B (Proposal B, `variant-2-original.md`)
- Executor: merge-executor agent (slot C-09, panel-resolution-and-tier-source)
- Changes applied: 14 of 14
- Status: success
- Timestamp: 2026-11-14T17:20:50Z
- Plan: `refactor-plan.md` (14 planned changes, auto-approved 2026-11-14T17:09:00Z), applied in the plan's order: Changes 3 and 5, then 10, then 12, then 13, with the remaining changes in numeric order around them
- Merged output: `../merged-panel-resolution-and-tier-source.md` (52 provenance tags; header comments present; last line `Status: Complete`)

## Changes Applied

Section references in "Target" and "After" are to the merged document unless "Base" is named. Plan order of application: 3, 5, 10, 12, 13 first where they share sentences, then the others; the entries below are in numeric order.

### Change 1: Ownership statement as a "today versus proposed" table with the merged wording
- **Status**: Applied
- **Source**: Variant A section 2.1 (7-row table); `round2-advocate-A.md` and `round2-advocate-B.md` section 6 item 1 (merged wording)
- **Target**: Base section 2 item 1 (replaced) and section 1 paragraph ("snapshot" wording)
- **Before**: Six-statement ownership list ending "Nothing in the packaged file is called the single source of membership"; section 1 called the packaged lists "a snapshot".
- **After**: Section 2 item 1 is a 6-row Today / Under-the-merged-position table (tier order and membership, class, vendor, launch, slot lists of ccsession, model id behind a slot) plus the merged wording in a block quote with B's clause (the guard does not read the workspace env; `MODEL-TIERS.md:189-193`), a note that "snapshot" and "single source" are not used, a repo-only note, and the pointer to FF-INV-005 (override tier file, left open). A's seventh row (E2 fallback ladder) is not carried (deferred, section 8.3). Section 1 now says "reviewed copy ... held in step by a test".
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 2.1 table — merged per Change 1; wording from Round 2 section 6 item 1 ... -->`; section 1: `<!-- Source: Base (original, modified) ... per Changes 1, 3, 5 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK (no surviving "snapshot" or "single source" outside the sentence that says they are not used, section 7's quoted objection, and provenance comments)

### Change 2: Drift guard as one test with parser rules, mutation tests and the names/classes assertion
- **Status**: Applied
- **Source**: `round2-advocate-A.md` section 6 item 2 (parser rules, four mutation tests); `round2-advocate-B.md` section 6 item 2 (names and classes assertion); invariant probe FF-INV-006 (parse green today)
- **Target**: Base section 2 item 2 (extended) and section 5 item 1 (extended)
- **Before**: B's derive-and-compare check with one mutation case and no parser rules.
- **After**: Item 2 lists the parser rules (find table by header cell, map `**Tier 2b**` to `tier2b`, read only column 3, raise on a missing header, row or empty cell), the four mutation tests (swap, substitute, drop a row, rename the header), the retained case `:101-106` and the pins `test_ccsession_tiers.py:221-222`, the env-is-not-a-leg statement, what each leg covers, and the FF-INV-006 parse result. The names and classes assertion is tagged "B addition, unanswered by A" (A had no turn after it; it also appears in B's section 4 (g) list). Section 5 item 1 restates the red/green conditions.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 item 2, extended per Change 2 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 3: Remove the per-profile `distinctness` field and the "profiles" mechanism
- **Status**: Applied (applied first, with Change 5)
- **Source**: `round2-advocate-B.md` section 1 W-2 (CONCEDE) and section 4 (a2); `round2-advocate-A.md` section 4 (a2); `panel.py:174-176`
- **Target**: Base section 2 item 4, the three named-module bullets, section 5 item 2, section 6 bullets, section 1 paragraph, section 4 INV-A, section 8 (now section 0) last C-03 sentence
- **Before**: Item 4 gave the profile a `distinctness: soft|strict` field ("Reflect profiles are `strict`"); the named modules each "declare their own `distinctness`"; section 5 item 2 had "the spec profile resolves soft and records neither key"; section 8 said "B's per-profile `distinctness` follows that same split".
- **After**: Item 4: soft default unchanged, `--strict-distinct` stays the opt-in (SKILL.md:340; `test_shadow_skill_contract.py:243-246`; `test_shadow_exit_script.py:27`), no `--allow-repeat`, no profile field or table, reasons from both advocates, revisit when a second strict consumer exists; named modules say "passes the flag as reflect does"; section 5 item 2 drops the two profile-based tests; section 6 bullets say the consumer passes the flag or leaves it off; INV-A no longer ties keys to a profile; section 0 says the per-profile field was withdrawn in Round 2.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 item 4 rewritten per Change 3 ... -->` and the matching tags on each edited block
- **Validation**: Structural integrity OK | References OK (re-grep: `distinctness` survives only in the sentence that withdraws the field, in the "no `distinctness` key" list, a quoted test of the old design, E12's simulated-change row and "Requested-id distinctness" / "soft distinctness" as plain concepts; "profile" survives only as "reflect profile" (existing code), C-03's `degrade` profiles, and statements that no profile field exists) | Contradictions OK

### Change 4: Scarcest-tier-first order as the CLI's slot order, sort key shown as OPEN
- **Status**: Applied (key left open as planned; nothing decided)
- **Source**: Variant A section 3.3 and 2.3 item 4; `round2-advocate-A.md` and `round2-advocate-B.md` section 6 item 4; B R2 M2, M3, M5, M6, M7; FF-INV-003, 012, 019
- **Target**: Base new item 4a in section 2; section 3 (E4, E11); section 5 (new item 5, slot-order tests)
- **Before**: No slot-order item; E4 compared strict and soft in template order only.
- **After**: Item 4a states the agreed part as the position (`scarcest_first` keyword defaulting to today's order, CLI passes `True` for soft and strict, fixed slots first, emission-order output, `template_sha256` of the real template, seeds unchanged) with E4's 345 and 693 of 1000 against 0; tags the `skipped_slots` re-sort "B addition, unanswered by A"; presents the sort key as OPEN with Option A (`len(aliases[tier].models)`, A's `shortcut:` wording from A R2 section 6 item 4) and Option B (servable-candidate count, B's `shortcut:` wording from B R2 section 6 item 4) and each side's evidence (B R2 M2 unrebutted and reproduced by FF-INV-012); names B's CLI parity test as "the test that tells the two keys apart", inside the open-key paragraph only; states FF-INV-019 (27 of 1840 and 3) and FF-INV-003 as open. Section 5 item 5 lists the agreed tests and B's tests (vii) to (ix) as "B addition, unanswered by A". E11 carries B R2 M2, M3, M5, M6, M7.
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 3.3 third bullet and Section 2.3 item 4, repaired in Round 2 section 6 item 4 of both advocates — merged per Change 4 as new item 4a; the sort key is carried as OPEN -->`; E11: `<!-- Source: Debate round ref — Round 2 section 3 M2, M3, M5, M6, M7 of Variant B, merged per Change 4 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK. One edit beyond the plan's target list, a consistency edit and not a decision: section 1 gained one sentence stating the agreed CLI order (key open) so the position summary matches section 2.

### Change 5: Record keys written by the CLI, always; B's two small additions marked contested
- **Status**: Applied (applied first, with Change 3)
- **Source**: `round2-advocate-A.md` and `round2-advocate-B.md` section 6 item 5; A R2 N2; B R2 W-1, M1; FF-INV-010, 011, 021, 024
- **Target**: Base section 2 item 5 (rewritten), section 4 INV-A, section 5 item 2, section 8 (now section 0) denominator sentences, new E12
- **Before**: Keys "written only when a profile or flag asks"; "pins must pass unmodified" for the profile design.
- **After**: Item 5: the CLI adds `requested_slots` (template count when the kind is in `apply_to`, else 1) and `distinct_models` to every resolution; library output unchanged; 0 pins at the CLI against 17 in the library (counted by reading; the 0 simulated by both advocates, 661 and 681 tests; FF-INV-024 calls it a prediction); no stderr line, `shortfall`, `distinctness` or resolve-time exit rule; FF-INV-010, 011 and 021 warnings next to it; the two B additions (`slot_order`, library helper functions) are pointed to section 8.2 where they are tagged "B addition, unanswered by A". Section 0 now says `requested_slots` is a source for `requested` in C-02 INV-001 and C-03 INV-007, is read from the resolution file, and what merge does with it stays C-03's; this replaces the base sentence that the key "does not depend on `--resolution` being passed", which FF-INV-021 shows is not true for the spec loop.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 item 5 rewritten per Change 5 ... -->`; E12: `<!-- Source: Debate round ref — Round 2 section 3 N2 of Variant A and M1 of Variant B, merged per Change 5 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 6: Spec loop prompt not edited, with the pinned and mirrored evidence
- **Status**: Applied
- **Source**: `round2-advocate-A.md` section 3 N3 and section 6 item 6; `round2-advocate-B.md` section 1 (N3 verified, `cmp` byte-identical mirror)
- **Target**: Base section 2 Named modules first bullet; section 4 (INV-C, INV-D)
- **Before**: "unchanged; soft profile".
- **After**: The bullet says unchanged and soft by omission, adds `E_FIRST` and `TEXT.count(E_FIRST) == 1` (`test_review_rules_text.py:21, 31`), the `plugins/` mirror (byte-identical by `cmp`; which gate keeps it identical is [UNVERIFIED]), the three-file-edit cost, and the outcome sentence qualified as "distinct requested ids; served identity is the subject of slot C-08; FF-INV-026, which also needs FF-INV-001 and FF-INV-005". Section 4 splits INV-C and INV-D out of the "untouched" list with the same evidence.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 first bullet extended per Change 6 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 7: Class and vendor: parity test, no `vendors` map
- **Status**: Applied
- **Source**: `round2-advocate-A.md` section 1 B-W6 and section 6 item 7; `round2-advocate-B.md` M8
- **Target**: Base section 2 item 6 (extended)
- **Before**: B's parity test and extras list, no verified facts, no FX-14 statement.
- **After**: B's test kept; added: `_vendor_from_model_id` maps all 13 packaged ids and `muse-ember-1.0` (gives `meta`) [OBSERVED-RUNTIME, B R2 M8]; A withdrew the `vendors` map and the marker list (validator edit `panel.py:371-373`, changes `tiers_sha256`); FX-14 stays open under both positions; the `SKILL.md:1248` line was not re-read by either advocate [UNVERIFIED].
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 item 6, extended per Change 7 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 8: Ember: union edit list
- **Status**: Applied
- **Source**: `round2-advocate-A.md` section 6 item 8 and `round2-advocate-B.md` section 6 item 8; B R2 M4, M8; FF-INV-009, 017, 018
- **Target**: Base section 2 `muse-ember-1.0` bullet (replaced); section 4 cross-repo ordering (extended); section 3 E6 (extended)
- **Before**: A data edit "by a `ccsession-models.json` slot edit" then a `classes` and `names` entry and a regenerated golden.
- **After**: Eight ordered steps (Coder `defaults.sh` slot; `ccsession-models.json` `T4Model04`; `aliases.tier4.models` at the index the Coder env gives; `names` and `classes` in the same change; the `MODEL-TIERS.md` tier 4 row; `test_ccsession_tiers.py:222` and `test_review_panel_live7.py:94-96`; `panel-golden-packaged-tiers.json` regenerated once; `make sync-dev` then `make verify-sync`), "no Python source change", slot index 02 against 04 left to the owner (GQ-046), the tier-size coupling clause (B R2 M4: about 20 to 27 percent of run ids) and pointers to FF-INV-009, 017, 018. Clauses that only B wrote (same-change clause, `make sync-dev` / `make verify-sync`, coupling clause) are tagged "B addition, unanswered by A". E6 carries the M4 table and A R2 N8 (pool effect).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 muse-ember-1.0 bullet replaced per Change 8 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 9: INV-L accounting sentence and goldens
- **Status**: Applied
- **Source**: `round2-advocate-A.md` section 4 (e) and `round2-advocate-B.md` section 4 (e)
- **Target**: Base section 4 INV-L bullet and "Frozen goldens" bullet (replaced)
- **Before**: "INV-L ... preserved" and "layer 1 does not edit the packaged tier file, so `tiers_sha256` stays".
- **After**: The agreed sentence verbatim ("INV-L holds until the first edit of the packaged file; ... the CLI-layer keys change neither `tiers_sha256` nor `template_sha256`") and the golden statement: the frozen-copy golden and `panel-golden-default-live7.json` untouched, `panel-golden-packaged-tiers.json` regenerated once for ember (it pins only anthropic-only resolutions, so only `tiers_sha256` changes).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 4 INV-L bullet and "Frozen goldens" bullet replaced per Change 9 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 10: Correct the base claims the debate refuted or the author conceded
- **Status**: Applied (after Changes 3 and 5)
- **Source**: `round1-advocate-B.md` section 5 concessions 1 to 3; `round2-advocate-B.md` section 1 W-1, W-3; A R2 N1; shared assumption A-001
- **Target**: Base section 7 answer points 1 and 2, section 7 objection figures, section 3 E4, section 5 item 2, section 2 ember bullet
- **Before**: "The repeat is not silent under B"; "makes the default panel unresolvable"; E4 with 18 and 30 of 40; "pins must pass unmodified" including the packaged-tier golden.
- **After**: Point 1: the repeat is visible through the always-written `distinct_models` and, in the gateway, removed by the CLI's order. Point 2: strict in anthropic-only resolves 2 reviewers in 1000 of 1000 runs; a floor of `min(2, requested)` never fires; "unresolvable" deleted. Point 4: overlay clause rewritten (dropped by both advocates). Objection and E4 restated with 1000-run figures (345 and 693 of 1000, 0 with scarcest-first; anthropic-only 2 is inherent); section 5 item 2 restates "unmodified" for the merged design (CLI keys 0 pins; flip would have moved 3 to 4; packaged-tier golden removed from the list; only the three ember pin edits) with A's candour sentences (section 4.2 and section 0 of Variant A). Answer's four-point structure kept.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 7 answer, points (1), (2) and (4) corrected per Change 10 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 11: Measurements and concessions from Variant A (M1 to M3, 7.4) added
- **Status**: Applied
- **Source**: Variant A sections 5.1, 7.4, 7.5; `round2-advocate-A.md` section 4 (a) and N6
- **Target**: Base section 5 (appended as items 6 to 8) and section 7 (closing "What the debate left unmeasured")
- **Before**: Section 5 had items 1 to 5 (item 5 was the overlay check, removed by Change 14); section 7 ended with answer point (4).
- **After**: Section 5 items 6 to 8 are A's M1, M2, M3 relabelled "A's M1 / M2 / M3". M1's third arm is "a repeat chosen by hand (the E2 style)" because `--allow-repeat` was dropped; M2 uses the 1000-run figures; M3 says "reviewed-copy wording" instead of "single-source claim" and uses the slot-filtered env correction (A R2 N6). Section 7 closes with "What the debate left unmeasured": the ownership wording and the strictness default can be judged apart (7.4 reworded), and the open owner question GQ-050 / Q-5 (7.5).
- **Provenance tag**: `<!-- Source: Variant A (Proposal A), Section 5.1 M1 / M2 / M3, merged per Change 11 ... -->`; `<!-- Source: Variant A (Proposal A), Section 7.4 and 7.5, merged per Change 11 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK. Note: base item 4 (value of distinctness) and A's M1 ask the same question; each cross-references the other and neither is removed.

### Change 12: Dependence section moved before the design, and a debate-outcome block
- **Status**: Applied
- **Source**: scorer evidence S1 (`scorer-pass1.md`, `scorer-pass2.md`); `debate-transcript.md` Convergence Assessment; `base-selection.md`
- **Target**: Base section 8 (moved to new section 0, after Changes 3 and 5 were applied inside it); new "Debate outcome" block at the top of section 0
- **Before**: Dependence on C-01, C-02 and C-03 was section 8, after section 2 items 4 and 5 already relied on it.
- **After**: New section 0 holds the Debate outcome block (winner: the hybrid on Variant B as base; convergence 24 of 25 points, 96%; unresolved: the sort key; probe totals) and the dependence text. Sections 1 to 7 keep their numbers. The Open items section is section 8 only after all references to the old "section 8" were rewritten: the base text contains no internal "section 8" reference (the only "section 8" mentions were `r04 section 8`, an external research-file reference, kept as such), and the base's "(section 3, E9)" pointer is kept and resolves.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 8 moved here per Change 12 ... -->`; `<!-- Source: debate-transcript.md Convergence Assessment and base-selection.md — Debate outcome block merged per Change 12 -->`
- **Validation**: Structural integrity OK | References OK (scan below) | Contradictions OK. Edits inside the moved text beyond the plan: "I read the ADJUDICATION-RESULT.md" rephrased in the third person (it was Variant B's statement), and a sentence from Variant A section 0 about C-01 condition 3 added to the C-01 bullet (Change 10's candour sentence).

### Change 13: Open items left by the debate (new final section)
- **Status**: Applied
- **Source**: `invariant-probe.md` (13 UNADDRESSED: FF-INV-001, 003, 004, 005, 009, 010, 011, 012, 017, 018, 019, 021, 026; MEDIUM 8, LOW 5); diff point C-007; Round 2 item 9 of both advocates; the "did not verify" lists of both Round 2 files
- **Target**: Base, new final section 8
- **Before**: Section did not exist.
- **After**: 8.1 table of the 13 findings (ID, category, one-sentence assumption, severity, where used); 8.2 table of contested and unanswered items (the sort key with both options and the state of the evidence; B's `slot_order`; B's library helper functions; B's section 4 (g) additions and the other B-only clauses, each tagged "B addition, unanswered by A"); 8.3 the deferred list of both hybrids (seven items); 8.4 the "did not verify" lists of A, B and the fault-finder. The 13 ADDRESSED findings are not tabled; the section says so and names the three cited elsewhere.
- **Provenance tag**: `<!-- Source: invariant-probe.md (13 UNADDRESSED findings) and debate-transcript.md, merged per Change 13; nothing in this section is decided by the merge -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK. Severity totals recomputed: MEDIUM = FF-INV-001, 005, 009, 010, 012, 019, 021, 026 (8); LOW = 003, 004, 011, 017, 018 (5).

### Change 14: Remove the env overlay (layer 2) from the base text
- **Status**: Applied
- **Source**: `round1-advocate-B.md` concession 4; `round2-advocate-B.md` section 1; `round2-advocate-A.md` section 1; scoring row C-010
- **Target**: Base section 2 item 3, section 3 E9, section 4 reproducibility bullet, section 5 item 5, section 6 PR-review bullet, the Tasklist/PR review/rf-qa named-module bullet, section 7 answer (4), section 1 paragraph
- **Before**: Item 3 described the overlay and `tiers_source`; E9 listed its weaknesses; the reproducibility bullet said "with the overlay"; section 5 item 5 was an overlay check; section 6 said "once the overlay exists"; section 7 (4) called it "optional".
- **After**: Item 3 keeps `select_env` unchanged and one sentence: "An env overlay ... was considered and dropped by both advocates: it would give a per-workspace `tiers_sha256`, which `recompute_parity` reports as not proven". E9 is reduced to "Considered and dropped" with the three reasons. The reproducibility bullet is rewritten around the two default orders. Section 5 item 5 became the slot-order tests (the overlay check is removed, so A's M1 to M3 stay items 6 to 8). The section 6 and named-module phrases are removed; section 7 (4) says the overlay was dropped. Section 1 had no overlay sentence (nothing to remove there).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant B section 2 item 3; overlay sentence removed per Change 14 (dropped by both advocates) -->` and the matching tags on each edited block
- **Validation**: Structural integrity OK | References OK | Contradictions OK. Re-grep for "overlay" and "tiers_source" gives hits only in provenance comments and in the sentences that say the overlay was dropped (item 3, E9, section 4 reproducibility bullet, section 7 answer (4)); no sentence describes it as part of the design.

## Post-Merge Validation

Checks run on `merged-panel-resolution-and-tier-source.md` with read-only grep and one read-only shell scan.

### Structural Integrity
- Heading hierarchy: PASS. One H1; H2 sections 0 to 8 in order; H3 only under section 0 (Debate outcome, Dependence on the adjudicated slots), section 2 (Shared core, Named modules) and section 8 (8.1 to 8.4); no H4 or deeper, no level gap, no orphan H3.
- Section ordering: PASS. The dependence on C-01 to C-03 (section 0) now precedes the design (section 2) that relies on it; evidence (3) precedes invariants (4), tests (5), effect (6), objection (7), open items (8). Sections 1 to 7 keep the base numbering.
- Document flow: PASS. B's shape is kept (Position, Design consequence, Evidence, Invariants, Test or measurement, Effect on PR review and rf-qa, Strongest objection and answer) plus section 0 and section 8. Provenance: header comments (`Provenance`, `Base: Variant B (Proposal B)`, `Merge date`) present; 52 `<!-- Source: ... -->` tags, one before every section or significant block; no unresolved `RF_PLACEHOLDER`; last line `Status: Complete`.

### Internal References
- Total references: 128 machine-counted (78 "section N" references to sections 0 to 8, counted without the ones attributed to another document, plus 50 evidence-item references E1 to E12) and about 38 standalone "item N" references checked by reading.
- Resolved: all, after three corrections made during validation.
- Broken: 0 remaining. Found and fixed: (1) "agreed item 6 below" in section 2 item 5 pointed at the class and vendor item instead of the spec loop; reworded to "the spec loop bullet of the named modules below"; (2) "(item 4)" in section 7 qualified as "section 2 item 4"; (3) "item 4a" in section 5 item 7 qualified as "item 4a of section 2". No reference to a section above 8 or an evidence item above E12 exists (scan: none).
- References to other documents were excluded from the count and left as written: Variant A sections 0, 3.3, 4.2, 5.1, 7.4, 7.5; `r04` sections 2, 3.2, 3.4, 4.3, 7, 8; "Round 2 section N item M", "A R2" and "B R2" labels. Neither of A's two mis-pointed internal references ("see 3.4", "5.1 above lists why") was copied.
- Label conventions: "evidence item E2" versus "the E2 experiment" and "the E2 harness" are separated (four bare uses of "the E2 ..." were reworded during validation); "A's M1 to M3" versus "B R2 M1 to M9" and "A R2 N1 to N8"; the probe ids are written FF-INV-nnn (16 distinct ids used, none clashing with C-02 INV-001, C-03 INV-007 or INV-A to INV-N); diff-point ids appear only in section 8.2 (and the one "diff point C-007" mention).
- Stale-sentence greps (all on the merged file): "overlay" and "tiers_source": only provenance comments and sentences that say the overlay was dropped (section 2 item 3, E9, section 4, section 7 answer (4)); "distinctness": only the sentence that withdraws the field, the "no `distinctness` key" list, one quoted old test, E12's simulated-change row, and plain uses ("soft distinctness", "requested-id distinctness"); "snapshot" and "single source": only the sentence that says they are not used, the quoted section 7 objection and provenance comments; "profile": only "reflect profile" (existing code), C-03's `degrade` profiles, and statements that no profile field exists; "records neither key", "once the overlay exists": only a quoted dropped test and a provenance comment.

### Contradiction Re-Scan
- New contradictions introduced: 0.
- Details: the three intra-base contradictions recorded in `base-selection.md` for Variant B are removed by the merge: X-001 ("the repeat is not silent" versus keys written only on request: keys are now always written by the CLI and section 7 point (1) says so), X-003 ("unresolvable" versus "always 2": the word is deleted), X-005 (snapshot versus an ember path that omits the packaged-list edit: the union list has the `aliases.tier4.models` and `MODEL-TIERS.md` steps). Two sentences were corrected during the scan before they became contradictions: a carried-over claim of "four distinct Anthropic ids for seven slots" was replaced by A R2 N8's correction (three Anthropic models reachable; strict gives one Sonnet plus one Haiku), and the base's claim that `requested_slots` "does not depend on `--resolution` being passed" was reconciled with FF-INV-021 (section 0). Open points are shown as open and are not stated as settled anywhere else: the sort key appears as OPEN in section 0, item 4a, E11 and section 8.2, and no other section chooses one.
- Plan-fidelity notes (not contradictions): (a) section 1 gained one sentence describing the agreed CLI order (key open), a consistency edit; (b) section 5 item 5 was reused for the slot-order tests so A's M1 to M3 are items 6 to 8 as planned; (c) E11 and E12 are new evidence items that carry the Round 2 measurements the plan cites for Changes 4 and 5; (d) section 8 subsections are numbered 8.1 to 8.4; (e) no claim, figure or decision was added that is not in the debate files; the arithmetic-free figures are quoted from A R2 N1 to N8, B R2 M1 to M9 and the probe.

## Summary

- Total changes planned: 14
- Successfully applied: 14
- Failed: 0
- Skipped: 0 (no change needed a decision the debate left open; where a point is open, Changes 4, 5, 8 and 13 present it as open and carry both sides' evidence)
- Post-merge validation: PASS (heading hierarchy, section ordering, 128 of 128 machine-counted references resolved after 3 corrections, 0 new contradictions)
- Left open on purpose, for the orchestrator: the sort key of the slot order (merged document item 4a and section 8.2); B's `slot_order` key and library helper functions; B's Round 2 section 4 (g) additions; the 13 UNADDRESSED probe findings (section 8.1). A had no turn after B's Round 2, so every text tagged "B addition, unanswered by A" is carried as written and not settled.
- Outputs: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/panel-resolution-and-tier-source/merged-panel-resolution-and-tier-source.md` and this file.
