# Merge Execution Log

## Metadata

- Base: Variant 2 (reviewer 2, qa, haiku slot), `variant-2-original.md`
- Executor: merge-executor agent (sc-adversarial-protocol Step 5, T05.03 to T05.05; template refs/artifact-templates.md Section 5)
- Plan: `refactor-plan.md` (30 changes plus "Fix cycle 1"); reviews `refactor-plan-review.md` (FAIL, fixed) and `refactor-plan-review-2.md` (PASS, minor N-01 to N-06)
- Output: `merged-verdict.yaml` (this directory), run 1 shape (`../../pre/adversarial/merged-verdict.yaml`, shape only)
- Changes applied: 30 of 30 planned
- Status: success
- Timestamp: 2026-11-08T15:10Z

### Shape decisions

- Top-level keys follow run 1: `schema`, `merge_method`, `base_variant`, `sources`, `convergence_score`, `convergence_status`, `path_aliases`, `unaddressed_invariants_high`, `severity_counts`, `findings`, `row_coverage`, `not_carried`, `best_practice_grade`, `calibrated_confidence`. Added, not replacing any run 1 key: `convergence_detail`, and `folded_into` on each `unaddressed_invariants_high` entry.
- Finding fields follow run 1 (`id`, `severity`, `gap_class`, `tag`, `affected_items`, `evidence`, `recommendation`, `provenance {cards, debate, change, invariants}`), plus `location` and `notes` as the caller asked. The remediation text sits in run 1's `recommendation` field. `evidence` holds `{ref, quote}` pairs instead of run 1's bare refs, because the caller asked for quotes with file:line.
- F-02 also carries a `check_command` field holding the exact grep pattern, so a reader can copy it without parsing prose.
- Provenance annotations (T05.04) are YAML comments: the document header (`# Provenance`, `# Base`, `# Merge date`) and one `# Source: ...` comment above every finding and every top-level block, naming the variant, the card id and the change number.
- `row_coverage` adds `merged_by_scope` (parsed and inferred rows) and two `_note` fields for the coverage percentages, from the plan's field plan.

## Changes Applied

Validation key: Structural = the entry loads and has every finding field; References = every cited file:line was re-read and its quote matched; Contradictions = no new conflict with another finding. Every change below passed all three unless noted.

### Change 1: 8.3 name-count check (F-01, HIGH, unsound-check)
- **Status**: Applied
- **Source**: Variant 2 R2-G1; probe INV-020 residual
- **Target**: Base, R2-G1 kept and modified
- **Before**: R2-G1 with the V2 remedy only.
- **After**: Same claim, evidence widened with TL 1433 and DESIGN 459; INV-020 residual (count constants by definition, `^class Classification` does not prefix-match `ClassifiedRow`) appended. The phrase "the only HIGH" is removed and recorded in `not_carried`.
- **Provenance tag**: `# Source: Change 1; Base (original, modified): V2 R2-G1 kept, INV-020 residual appended`
- **Validation**: Structural PASS | References PASS (5 of 5) | Contradictions PASS

### Change 2: item 6.2 Verification cannot be met (F-02, HIGH, unsound-check)
- **Status**: Applied
- **Source**: invariant probe INV-006 (no card, no debate point); caller ruling (a)
- **Target**: new finding after F-01
- **Before**: did not exist.
- **After**: claim, evidence TL 991, 993, 2802, 2804; recommendation copied verbatim from plan lines 40 to 42; the grep pattern also in `check_command`. Plan notes on plain grep and the orchestrator check carried. Review N-04 and N-06 recorded as notes; the plan text, including the N-06 clause "as the TL 2804 rule requires for every owner decision", was not changed.
- **Provenance tag**: `# Source: invariant probe INV-006 (new finding, no card) merged per Change 2; caller ruling (a)`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS. Exactness: a script confirmed the pattern `grep -c '^| [^|]* | 6\.2 | .*OQ-1 (R5) RESOLVED' <TL>` is byte-identical in the plan, in `recommendation` and in `check_command`. Re-run against the TL today it prints 0, as the plan's success test expects before 6.2 runs.

### Change 3: step 1.0a unrouted outcomes, remedy widened (F-03, MEDIUM, design-fix)
- **Status**: Applied
- **Source**: Variant 1 R1-G1 (claim); Variant 2 R2-G5 (cursor half and its TL 1482, TL 1793 evidence); probe INV-021; caller ruling (b)
- **Target**: restructure of two card findings into one
- **Before**: R1-G1 (gate-bypass, a third Branch with a PENDING note) and R2-G5 (HIGH, cursor half plus a run-current narrowing).
- **After**: one MEDIUM finding with the unrouted-outcome claim; `gate-bypass` dropped; V2's run-current narrowing dropped. Recommendation steps 1, 2 and 3 and the success test copied verbatim from plan lines 52 to 55 (script-checked: all four match). Review N-01, N-02 and N-03 recorded as notes. N-01 note states that the HALT rule at TL 194 already appends the halt line to `### Execution Log`, so the "exactly one PENDING row for item 7.17" check must count the HALT row too or drop step 1's own row; it also records the missing `blocker_reason` and the TL 1142 recommendation-line ending.
- **Provenance tag**: `# Source: Variant 1 R1-G1 (claim), Variant 2 R2-G5 (cursor half only), invariant probe INV-021 (remedy widened); restructured per Change 3; caller ruling (b)`
- **Validation**: Structural PASS | References PASS (10 of 10) | Contradictions PASS. The N-01 tension between the success test and TL 194 is inherited from the plan and recorded, not introduced.

### Change 4: DESIGN 80 builder rule not copied (F-04, MEDIUM, traceability)
- **Status**: Applied
- **Source**: Variant 2 R2-G2
- **Target**: Base, R2-G2 relabelled HIGH to MEDIUM
- **Before**: HIGH, gap_class `missing`.
- **After**: MEDIUM, `traceability`; worded as a missing Key Constraints bullet; rows GQ-111, GQ-112, GQ-113 (partial) and INF-001 (missing) noted.
- **Provenance tag**: `# Source: Change 4; Base (original, modified): V2 R2-G2, HIGH label replaced by calibrated MEDIUM`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 5: byte limits and open item 19 (F-05, MEDIUM, traceability)
- **Status**: Applied
- **Source**: Variant 2 R2-G3; probe INV-003 (LOW)
- **Target**: Base, R2-G3 relabelled and extended
- **Before**: HIGH, gap_class `partial`.
- **After**: MEDIUM; INV-003 note in the recommendation (keep 23 open items or update the four pins TL 269, 454, 784, 1005); rows SP-28 and INF-024 noted.
- **Provenance tag**: `# Source: Change 5; Base (original, modified): V2 R2-G3, HIGH replaced by MEDIUM, INV-003 note appended`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS

### Change 6: missing checks for probes.py boundary, B5 and renderer bans (F-06, MEDIUM, test-plan)
- **Status**: Applied
- **Source**: Variant 2 R2-G4
- **Target**: Base, relabelled
- **Before**: HIGH, `partial`.
- **After**: MEDIUM, `test-plan`; stated as missing checks; V2's note that an import-absence grep cannot prove B5 kept.
- **Provenance tag**: `# Source: Change 6; Base (original, modified): V2 R2-G4, HIGH replaced by MEDIUM`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS

### Change 7: set-union session-count wording (F-07, MEDIUM, traceability)
- **Status**: Applied
- **Source**: Variant 2 R2-G6
- **Target**: Base, kept
- **Before**: R2-G6.
- **After**: same, with "may still be delivered by delegation" added.
- **Provenance tag**: `# Source: Change 7; Base (original, modified): V2 R2-G6 with the delegation qualifier added`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 8: D10 row and R5 history line (F-08, MEDIUM, traceability)
- **Status**: Applied
- **Source**: Variant 3 R3-G1 with R3-G7 merged in
- **Target**: new finding
- **Before**: two V3 findings.
- **After**: one finding; evidence converted to a list; R3-G7's note-as-quote replaced by the TL 999 quote; section list includes 2.2, 12 and 4. R3-G7 text appears once.
- **Provenance tag**: `# Source: Variant 3 R3-G1 with R3-G7 merged in, Section findings; merged per Change 8`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS. The SPEC line numbers come from V3 and were not re-read (noted in the finding).

### Change 9: DESIGN 221 capture rule (F-09, MEDIUM, authorized-expansion)
- **Status**: Applied
- **Source**: Variant 3 R3-G5, first remedy only
- **Target**: new finding
- **Before**: R3-G5 with two remedies.
- **After**: first remedy only; severity shown as open (MEDIUM kept, LOW defensible); cross-reference F-12.
- **Provenance tag**: `# Source: Variant 3 R3-G5 (first remedy only); merged per Change 9`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 10: 6.4 needs a 15.1 allowing hit (F-10, MEDIUM, unsound-check)
- **Status**: Applied
- **Source**: Variant 3 R3-G6, 15.1 half only
- **Target**: new finding
- **Before**: R3-G6 with a D10 half and a 15.1 half.
- **After**: 15.1 half only, V3's "ambiguous; costs a fix loop via TL 1007" wording.
- **Provenance tag**: `# Source: Variant 3 R3-G6 (15.1 half only); merged per Change 10`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 11: TL 1142 points at item 6.2 (F-11, MEDIUM, design-fix)
- **Status**: Applied
- **Source**: Variant 1 R1-G2
- **Target**: new finding
- **Before**: R1-G2, `gate-bypass`.
- **After**: `design-fix`, impact note added, evidence filled with TL 1142, TL 989 and TL 1244 quotes.
- **Provenance tag**: `# Source: Variant 1 R1-G2; merged per Change 11`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS. The TL 989 quote keeps the tasklist's own em dash, because it is quoted verbatim; it is the only em dash in the file.

### Change 12: section 4 edits outside every review (F-12, MEDIUM, design-fix)
- **Status**: Applied
- **Source**: probe INV-018; caller ruling (c)
- **Target**: new finding
- **Before**: did not exist.
- **After**: recommendation and success test as planned; cross-references F-08, F-09, F-20.
- **Provenance tag**: `# Source: invariant probe INV-018 (new finding); merged per Change 12; caller ruling (c)`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS

### Change 13: resumed HALT names no follow-up (F-13, MEDIUM, design-fix)
- **Status**: Applied
- **Source**: probe INV-005; caller ruling (c)
- **Target**: new finding
- **Before**: did not exist.
- **After**: recommendation reuses F-03 step 2's wording (named DESIGN edit item with its gate, or re-planning before step 1.2).
- **Provenance tag**: `# Source: invariant probe INV-005 (new finding); merged per Change 13; caller ruling (c)`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS (agrees with F-03 step 2)

### Change 14: 7.16 forbidden-token grep fails an honest capture (F-14, MEDIUM, unsound-check)
- **Status**: Applied
- **Source**: probe INV-008; caller ruling (c)
- **Target**: new finding
- **Before**: did not exist.
- **After**: as planned; cross-references F-16 and F-03 step 2.
- **Provenance tag**: `# Source: invariant probe INV-008 (new finding); merged per Change 14; caller ruling (c)`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 15: zero Dispatch rows (F-15, MEDIUM, design-fix)
- **Status**: Applied
- **Source**: probe INV-015; caller ruling (c)
- **Target**: new finding
- **Before**: did not exist.
- **After**: as planned.
- **Provenance tag**: `# Source: invariant probe INV-015 (new finding); merged per Change 15; caller ruling (c)`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS

### Change 16: bare coder grep and unwritten sentence (F-16, LOW, unsound-check)
- **Status**: Applied
- **Source**: Variant 1 R1-G5
- **Target**: new finding
- **Before**: R1-G5 with no evidence and a SOURCES.md extension.
- **After**: SOURCES.md extension left out; evidence filled with TL 1276 and TL 1262; tag set to Grounded on those quotes.
- **Provenance tag**: `# Source: Variant 1 R1-G5 (SOURCES.md extension left out); merged per Change 16`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 17: echo and ls against the 7.16 Verification (F-17, LOW, unsound-check)
- **Status**: Applied
- **Source**: Variant 1 R1-G6, first sentence only
- **Target**: new finding
- **Before**: R1-G6 with two sentences and no evidence.
- **After**: first sentence only; evidence filled with TL 1260 and TL 1262.
- **Provenance tag**: `# Source: Variant 1 R1-G6 (first sentence only); merged per Change 17`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 18: name the 7.16 capture actor (F-18, LOW, design-fix)
- **Status**: Applied
- **Source**: Variant 2 R2-G8 framing; Variant 1 R1-G4
- **Target**: restructure of two findings into one
- **Before**: R2-G8 (traceability) and R1-G4 (gate-bypass).
- **After**: one finding, V2 wording, provenance cards [R2-G8, R1-G4]; R1-G4's 14.8 Branch B hand-off kept as an option.
- **Provenance tag**: `# Source: Variant 2 R2-G8 framing merged with Variant 1 R1-G4; restructured per Change 18`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 19: INF-017 cites F11 (F-19, LOW, traceability)
- **Status**: Applied
- **Source**: Variant 2 R2-G9
- **Target**: Base, kept as is
- **Before**: R2-G9 with absolute paths.
- **After**: same content; paths made repo-relative through `path_aliases`.
- **Provenance tag**: `# Source: Change 19; Base (original): V2 R2-G9 kept as is`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 20: DESIGN 181 and 196 keep 8 (F-20, LOW, unsound-check)
- **Status**: Applied
- **Source**: Variant 3 R3-G2
- **Target**: new finding
- **Before**: R3-G2 (`design-fix`).
- **After**: `unsound-check`; cross-reference F-12.
- **Provenance tag**: `# Source: Variant 3 R3-G2; merged per Change 20`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS

### Change 21: 5.11 hits are in section 13 (F-21, LOW, traceability)
- **Status**: Applied
- **Source**: Variant 3 R3-G4
- **Target**: new finding
- **After**: tagged single-source in `notes`.
- **Provenance tag**: `# Source: Variant 3 R3-G4; merged per Change 21`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 22: config.py:64-78 citation (F-22, LOW, traceability)
- **Status**: Applied
- **Source**: Variant 3 R3-G9, narrowed
- **Target**: new finding
- **After**: narrowed claim (only the citation is missing); "missing reuse" framing dropped.
- **Provenance tag**: `# Source: Variant 3 R3-G9, narrowed; merged per Change 22`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 23: "five helpers" (F-23, LOW, traceability)
- **Status**: Applied
- **Source**: Variant 3 R3-G10; INV-013
- **Target**: new finding
- **Provenance tag**: `# Source: Variant 3 R3-G10; merged per Change 23`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 24: OQ-16 wording (F-24, LOW, test-plan)
- **Status**: Applied
- **Source**: Variant 3 R3-G11
- **Target**: new finding, worded as a wording fix
- **Provenance tag**: `# Source: Variant 3 R3-G11; merged per Change 24`
- **Validation**: Structural PASS | References PASS (2 of 2) | Contradictions PASS

### Change 25: 7.16 timestamp fields (F-25, LOW, design-fix)
- **Status**: Applied
- **Source**: Variant 1 R1-G3; INV-009
- **Target**: new finding, clarification only
- **After**: does not say "no strip rule"; recommends naming the fields.
- **Provenance tag**: `# Source: Variant 1 R1-G3, clarification only; merged per Change 25`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 26: DESIGN 939 scope (F-26, LOW, traceability)
- **Status**: Applied
- **Source**: Variant 1 R1-G9; Variant 2 R2-G7
- **Target**: restructure of two findings into one note
- **After**: open reading only, "Open, LOW either way"; both mechanisms dropped and listed in `not_carried`.
- **Provenance tag**: `# Source: Variant 1 R1-G9 and Variant 2 R2-G7, merged into one note; restructured per Change 26`
- **Validation**: Structural PASS | References PASS (4 of 4) | Contradictions PASS

### Change 27: 6.3 re-run matches the D10 ban quote (F-27, LOW, unsound-check)
- **Status**: Applied
- **Source**: probe INV-007; caller ruling (c)
- **Target**: new finding; cross-reference F-10
- **Provenance tag**: `# Source: invariant probe INV-007 (new finding); merged per Change 27; caller ruling (c)`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 28: 6.3 tuple count can exceed 3 (F-28, LOW, unsound-check)
- **Status**: Applied
- **Source**: probe INV-010; caller ruling (c)
- **Target**: new finding
- **Provenance tag**: `# Source: invariant probe INV-010 (new finding); merged per Change 28; caller ruling (c)`
- **Validation**: Structural PASS | References PASS (3 of 3) | Contradictions PASS

### Change 29: row_coverage
- **Status**: Applied
- **Source**: the three cards' `row_coverage` lists; plan field plan
- **Target**: `row_coverage` block
- **After**: per_card_raw, empty overlaps, unique_rows 152, merged_by_scope, merged (109 / 30 / 10 / 3 / 0 of 152), coverage_pct 0.960, coverage_pct_union 0.914, 3 missing ids, 10 partial ids, no false-match ids, four caveats.
- **Provenance tag**: `# Source: Change 29. Union of the three disjoint card slices (S-001) ...`
- **Validation**: Structural PASS | References PASS | Contradictions PASS. Re-count by the merge executor from the card files: V1 65/10/1/0, V2 18/15/8/3, V3 26/6/0/0, matching `per_card_raw`. Union with INF-019 moved from covered-in-substance to partial gives 109/30/10/3, summing to 152. The partial and missing id lists match the ids the cards mark partial or missing, plus INF-019.

### Change 30: header, invariants block, not_carried, grade and confidence
- **Status**: Applied
- **Source**: plan field plan; `debate-transcript.md` gate results; `invariant-probe.md`; calibrated card confidences
- **Target**: top-level fields
- **After**: `merge_method: adversarial`; `base_variant` variant-2; `convergence_score 1.00`, `convergence_status BLOCKED_BY_INVARIANTS` with a comment that both blocking items are fixed here; `unaddressed_invariants_high` lists INV-006 (`folded_into: F-02`) and INV-021 (`folded_into: F-03`); `severity_counts` HIGH 2, MEDIUM 13, LOW 13; 21 `not_carried` entries, one per row of the plan table (21 of 21) (the INV-002 entry carries the N-05 note); grade 3 on the 0 to 5 scale; `calibrated_confidence` 0.77 (inputs 0.71, 0.81, 0.79, re-read from the card files at V1 line 255, V2 line 558, V3 line 404).
- **Provenance tag**: `# Source: Change 30`
- **Validation**: Structural PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural integrity
- YAML loads: PASS. `uv run python` with `yaml.safe_load` loads the file; top-level keys in run 1 order.
- Every planned finding present: PASS. Ids F-01 to F-28 in order, `provenance.change` 1 to 28 in order, and every finding has `severity`, `gap_class`, `location`, `claim`, `evidence`, `recommendation`, `provenance` and `notes`.
- Severity counts match the plan: PASS. Counted from the findings: HIGH 2, MEDIUM 13, LOW 13 (total 28), equal to `severity_counts` and the plan header.
- Unaddressed invariants: PASS. All nine (INV-003, 005, 006, 007, 008, 010, 015, 018, 021) appear in at least one finding's `provenance.invariants`.
- Exact-copy checks: PASS. The F-02 grep pattern is byte-identical to the plan; F-03 steps 1 to 3 and the success test match plan lines 52 to 55.
- Section ordering: PASS. HIGH first, then MEDIUM, then LOW, as in the plan table.

### Internal references
- Cited file:line references re-read: 93 evidence refs checked (all evidence entries in all 28 findings), plus 28 `location` refs.
- Resolved: 93 of 93 evidence quotes found at their cited lines; 28 of 28 locations exist.
- Broken: 0. Corrected: 0.
- Cross-references between findings (F-xx mentions): every one points at F-01 to F-28; none dangles.
- Spot checks beyond the quotes: the naive 6.2 grep hits TL 991, 993 and 2802 today (3 hits, as INV-006 states); DESIGN 438 to 442 holds four underscore helpers plus `_publish`; `config.py:64` is `def _git`; the tasklist has no "allowlist change" text and "cursor" only at TL 1267 and TL 1482, as INV-021 states.

### Contradiction re-scan
- New contradictions introduced: 0.
- Checked pairs: F-03 step 2 against F-13 (same follow-up wording); F-08 against F-12 (both add section 4); F-10 against F-27 (different steps of 6.3); F-14 against F-16 and F-17 (command-line-only grep is compatible with allowing echo and ls and with dropping the sentence expectation); F-03 MEDIUM against the `not_carried` row "Raising F-03 to HIGH" (consistent); "the only HIGH" appears only where it is recorded as removed.
- Pre-existing tensions carried from the plan and recorded as notes, not new: N-06 (F-02 step 1 clause against the `not_carried` INV-006 rationale) and N-01 (F-03 "exactly one PENDING row" against the TL 194 HALT row).

## Summary
- Total changes planned: 30
- Successfully applied: 30
- Failed: 0
- Skipped: 0
- Review minor findings N-01 to N-06: 6 of 6 recorded as notes (N-01, N-02, N-03 on F-03; N-04, N-06 on F-02; N-05 on the INV-002 `not_carried` entry). The plan content was not changed for any of them.
- Post-merge validation: PASS
