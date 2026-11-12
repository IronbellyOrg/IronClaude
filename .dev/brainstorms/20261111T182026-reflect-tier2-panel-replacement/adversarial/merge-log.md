# Merge Execution Log

## Metadata
- Base: Variant 1 (opus:architect)
- Executor: merge-executor agent
- Changes applied: 46 of 46 planned (0 skipped, 0 failed)
- Status: success
- Timestamp: 2026-11-11T20:30:00Z
- Method note (deviation, recorded for honesty): the base was copied with `cp`, then, because the plan replaces almost every section after Candidate C wholesale, the file was rebuilt section by section on disk (one Write for the first chunk, then four Edit appends at a marker), retyping unchanged base text (Candidates A, B, D, Q1 table rows, Finding-format table rows, Assumptions) from the base I had read. Small post-merge fixes used Edit. Plan draft text was used verbatim except that every "Change N" cross-reference was converted to the target section name (so the document is self-contained) and plan-internal labels (INV-, S-, C-, X-, A-) were kept as external labels explained in the conventions paragraph. Retyped base text was not diffed byte-for-byte against the base.

## Changes Applied

Format: status | before -> after | provenance. Validation for every change: structure OK, references OK, contradictions OK unless noted.

### Group A (incorporations)
- **1 Execution contract**: Applied | no failure model -> `### Execution contract (both adapters)` (manifest states, idempotency, resume, atomic publish) | Variant 3, "Adapter sketches" final block, Change #1.
- **2 Completion states and channel**: Applied | none -> `### Completion and channel`; Risk 5 mitigation now "one bounded re-ask" in the Risks table | Variant 3, Change #2.
- **3 Judge identity**: Applied | "pass K1 classes if accepted" -> Q3 "Judge identity" paragraph (collision telemetry, Fable/tier0 assertion) | Variant 3 Q3, Change #3.
- **4 Cost model**: Applied | one 49-96k / 35-68k lane table -> three separated bases, lane table 42-66k vs 37-56k (lane labels taken from Variant 3 rows), footnote for 49-96k | Variant 3 Cost model, Change #4. Intent note: the plan gave the totals and the arithmetic; the lane table rows come from Variant 3 lines 269-274.
- **5 Embedded calibration**: Applied | sidecars `calibration.json`/`validation.json` -> embedded `calibration:` block, join by finding id; "never mutated" removed; the withdrawn sidecars are named once as not part of the design | Variant 3 Q2, Change #5.
- **6 Debate kept**: Applied | debate removed in pre, `panel_agreement_score` -> debate kept, clustering is telemetry; Summary, C, E', Q3, matrix rows rewritten | Variants 2 and 3, Change #6.
- **7 Engine rule by `launch`**: Applied | tier alias as ccsession alias -> explicit `model` whitelist `{sonnet, opus, haiku}`, null `launch` refused for pre | Variants 2 and 3, Change #7.
- **8 Forbidden-model filter**: Applied | "never listed" -> `#### Forbidden models` with three validation rules | Variant 2 U-013, Change #8.
- **9 Reviewer cap and 15-point gate**: Applied | none -> hard cap 3, `N_eff`, raising gate, in Q7 | Variant 2 Q7, Change #9.
- **10 Real-card evidence**: Applied | none -> appended to reason 2 and `### What a recorded card looks like` | Variant 2, Change #10.
- **11 Ablation arm, per-source layout, `reflect_category`**: Applied | `category` extended -> unchanged enum plus `reflect_category` and mapping; arm D; H3 hunk layout | Variant 2 U-010/011/012, Change #11.
- **12 Q5 and Q7 in place**: Applied | forward pointers -> direct answers (Q5 condensed to one paragraph, Q7 bullets) | Variant 3, Change #12.
- **13 Conventions paragraph**: Applied | opening paragraph -> conventions (kept "(enrichment)", added "(plan-verified)") | Variant 2, Change #13.

### Group B (corrections)
- **14 Contract-version facts**: Applied | "legacy runs emit 2.0.0" -> producers 1.8.0 and `"1.0"`, wrapper blocks non-1 majors | Change #14.
- **15 Versioning plan and mapping**: Applied | 1.9.0/2.0.0 plan -> no version change, bump rule, mapping table, null-score rules, gate 9, `reflect_post`, consumers (each "no change"), deferred list | Variant 3 mapping, Change #15. Intent note: the plan said "keep V1's consumer bullets"; they were rewritten from the base bullets with the 2.0.0 annotations moved to the deferred list.
- **16 Gate 9 and EV-1 wording**: Applied | PROPOSED EV-1 on ledger -> EV-1 unchanged (in pre step 10); gate 9 paragraph in the mapping | Change #16.
- **17 Ledger role and `--cap 1`**: Applied | ledger written -> not used in Stages 0-4; `ESCALATE` fact; cites fixed to `ledger.py:187-190`, `:107-298` | Change #17.
- **18 Recorded convergence evidence**: Applied | "1.0 in 4 of 5" -> 21 of 35 equal 1.0, 14 below, 7 null; moved to the mapping section and referenced in reason 3 | Change #18.
- **19 Opus uses**: Applied | "only here" -> complete four-point list; calibrator-diversity claim limited to lite | Change #19.
- **20 IC fixes**: Applied | "34-66k"/"35-68k"/"1.9.0 additive" -> 37k-56k, matrix row "none (1.8.0)" | Change #20.
- **21 Risks table**: Applied | 8-item list -> 12-row table with probability, impact, mitigation | Change #21.
- **22 Assumptions inventory**: Applied | base UNVERIFIED list -> VERIFIED (a)-(g) plus kept UNVERIFIED; A-7 moved to VERIFIED, A-10 added | Change #22.
- **23 Template set**: Applied | sonnet/haiku/haiku template -> parity `@reflect-pre` plus `-x2`, `-enterprise`, `-lite`, post | Change #23.

### Group C (invariant resolutions)
- **24 INV-005 exclusion**: Applied | `hard_exclude raises` -> K1 hard exclusion contract (8 items) | Variants 1 and 3, Change #24.
- **25 INV-015 multi-file identity**: Applied | fingerprint v2 with ledger -> `cluster_v2`, no ledger, no concatenation | Change #25.
- **26 INV-022 gates**: Applied | none -> `#### Executor-exclusion gates` table, spike S-ID | Change #26.
- **27 INV-023 compatibility gate**: Applied | none -> `### Contract compatibility gate` (5 items); Stage rows reference it. Mechanical fix: the plan text said "Stages 3, 4 and 5" while the plan's own Stage 2 entry requires the gate; reworded to "Stages 2, 3, 4 and 5 (Stage 2 entry needs items 1-3, exit adds item 4)". | Change #27.
- **28 INV-024 first measurement**: Applied | K4-vs-debate, 20 pairs -> H-A/H-B/H-C, arms A-D, sample size, strata, Stage 0a | Variants 1-3, Change #28.
- **29 INV-001..003**: Applied | none -> state-variable paragraph in Execution contract | Change #29.
- **30 INV-006/007/009/011**: Applied | none -> `#### Guards and counts` | Change #30.
- **31 INV-012/013 pre-check**: Applied | drop-adding pre-check -> flag-only pre-check, headless gap as Stage 5 item, thresholds unchanged | Change #31.
- **32 INV-014/018/019/021**: Applied | `panel_agreement_score` -> `cluster_agreement` | Change #32.
- **33 INV-020 null score**: Applied | none -> pre step 10 and null-score rules | Change #33.

### Group D (unresolved points)
- **34 S-001, S-004, C-025**: Applied (no-op decisions) | order and naming kept; `panel_agreement_score` replaced elsewhere | Change #34.
- **35 C-007**: Applied | cluster map fed to post debate -> not fed (post step 7, O-3) | Change #35.
- **36 A-002**: Applied | none -> Stage 3 entry environment gate, A-10 | Change #36.
- **37 A-003**: Applied | quote required -> `quote` optional, conversion rule, 90% gate | Change #37.
- **38 Open items**: Applied | none -> `## Open items` O-1..O-11 placed before Assumptions | Change #38.

### Group E and F
- **39 Depth x tier**: Applied | scattered `--depth` text -> `## When the panel is called` (rules D1-D5, table, default-workflow paragraph), placed after Chosen architecture | Change #39. The old "debate only under `--depth deep`" claims are gone; the remaining 7 `depth deep` mentions are table rows, rule D3, the cap rejection and the stratum list.
- **40 Summary, candidates, matrix**: Applied | rewritten as specified; E replaced by E' | Change #40. Intent note: the "maintenance surface" row text is kept from the base; B/C/D cost cells follow the plan's numbers.
- **41 Reasons**: Applied | reasons 2, 3 edited, reason 6 added | Change #41.
- **42 Q1, Q2, Q3, Q5, Q6 sync**: Applied | rows and answers as specified | Change #42.
- **43 Staged migration**: Applied | table replaced (7 rows) | Change #43.
- **44 Adapter sketches**: Applied | pre 1-12 and post 1-10 replaced by plan text | Change #44.
- **45 PROPOSED names**: Applied | old inventory -> new, placed at the end of Assumptions | Change #45.
- **46 Required-content map and consistency pass**: Applied | `## Required-content map` added; grep pass (a)-(e) run, results below | Change #46.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: OK. One H1, H2 sections, H3 subsections, H4 only under Q4 (Template set, K1 hard exclusion contract, Opus uses, Forbidden models, Executor-exclusion gates, Guards and counts). No skipped levels, no orphan subsections.
- Section ordering: OK. Required sections (Summary, Candidates, Chosen architecture, depth x tier, Q1-Q7, Finding format, Adapter sketches, Staged migration, Return-contract mapping, Cost model, Risks, First measurement, Open items, Assumptions, Required-content map) are present.
- Document flow: OK.

### Internal References
- Scanned: "see ..." section names, "Q1-Q7", "Stage n", "D1-D5", "O-1..O-11", "K1 contract item n", "Post-execution adapter, step 7", table cross-references. All resolve to a heading or numbered item in the merged document. Plan-internal labels (INV-, S-, C-, X-, A-, U-) are external labels explained in the conventions paragraph; "Change #n" occurs only in HTML provenance comments and refers to refactor-plan.md (stated in the header comment). Broken: 0. One dangling label fixed: "A-7" in the VERIFIED list was rephrased because A-7 is no longer in the assumptions list.

### Contradiction Re-Scan
- Contract version: 1.8.0 in every stage; 2.0.0 appears only in candidate E', the comparison cell and the deferred list. OK.
- `merge_method`: always `{adversarial, single-reviewer-fallback}`; `panel` only as the deferred value. OK.
- N=2 floor: counts complete reviewers of distinct classes everywhere (Q4 gates, Guards, Completion, mapping table). OK.
- Calibrator tier: parity template keeps `degraded` (Opus uses, gate list); lite arm becomes `full`/two-class `degraded`. OK.
- Flag read stage: after the final tier (D1/D2, pre step 2, Stage 2 row). OK.
- Depth table vs adapters and staged migration: consistent (panel only at T2, `legacy` default until Stage 4). OK.
- Fixed mechanically: contract-gate stage list (see Change 27).
- Not resolved, inherited from the plan: the parity cost lane differs from legacy by 3k-6k in the parallel lane and 2k-4k in the primary lane (Variant 3's table), while plan Change 4 also says parity differs "only by +0.5k per card". The document keeps both statements because the plan requires them and labels the saving a hypothesis; the owner should resolve it with Stage 2 telemetry.
- Plan statement D5 (clamp by depth) remains UNVERIFIED as written.

### Required-content check (owner list)
- Candidates (>= 3, includes leave-as-is): present, "Candidate architectures" (A, B, C, D, E').
- Chosen architecture with reasons: present, "Chosen architecture and reasons" (6 reasons).
- Q1-Q7 answers: present, "Answers to Q1-Q7".
- Finding format: present, "Finding format".
- Pre and post adapter sketches: present, "Adapter sketches".
- Staged migration with pre behind an off-by-default flag first: present, "Staged migration" (Stage 2 `shadow`, Stage 3 `panel`, default `legacy`).
- Contract 1.8.0 mapping (`merge_method`, convergence score, null-score rules, gate 9, `reflect_post`, every consumer): present, "Return-contract 1.8.0 mapping".
- Cost model with the depth table: present, "Cost model" plus "When the panel is called (depth x tier path)".
- Risks: present, "Risks".
- First measurement: present, "First measurement".

### Constraint check
- `Fable` / `Tier 0` / `tier0`: appear only as forbidden (conventions-adjacent rules in Q3 judge, template set, "Forbidden models", Opus-uses sentence, Stage 1 row, Risk 8).
- `src/superclaude`: 3 hits, all in the conventions paragraph (path base, and the statement that it is never an instruction for an installed primitive). Classification: allowed. No primitive-read instruction uses it; package cites use `cli/...`, `skills/...`.
- UNVERIFIED markers: kept (D5 clamp rule, band 52-65 implementation, judge-exclusion input, Agent reply model id, fallback.py, telemetry schema, sprint executor, report-template.md, tools allowlist, `SKILL.md:837`, per-lane splits, and others listed under "UNVERIFIED (kept)").
- Other consistency greps: `panel_agreement_score`, `calibration.json`, `validation.json`, `review-doc.md` appear only in "not used / withdrawn" sentences; `hard_exclude raises` is gone (replaced by "kernel fails closed, adapter degrades").

## Summary
- Total changes planned: 46
- Successfully applied: 46
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (one inherited cost-statement tension listed above)

## Post-check fixes
Total document size 101963 -> 102676 bytes (+713). Byte figures per id are approximate net adds/deletes.
- B1: applied. Lines 60, 78, 93, 128, 279, 479-488, 493 (lane table, midpoint statement, Candidate C Cost, matrix, depth-table row, Q7, E' derivation). About +900 added, -620 deleted. E' re-derived as 33k-61k. Residual 37k-56k hits (lines 60, 93, 279, 488) are all labelled an unproven hypothesis. H-C wording (line 526) already says "a saving is reported, not required"; left as is.
- M1: applied. Line 47, Verdict reverted to "violates the calibration constraint" (B Changes and Keeps keep the evidence-validator). +20 / -34.
- M2: applied. Line 127 depth-table row now cites :84-85, default implied by --tier auto, UNVERIFIED as a stated default (SKILL.md:84-85 read and confirmed). +50 / -18.
- M3: applied. Line 34 now cites reflect_review.py:14 and cli/swarm/config.py:59 (both read and confirmed). +20 / -35.
- M4: applied. Line 416 "37 of 62" (disk: 62 contracts, 37 at 1.8.0, confirmed). +0 / -0.
- M5: applied. Line 435 reworded to the T2-reached breakdown. My quick grep showed 8 explicit nulls and 19 contracts without the key (report said 9 and 18) and reproduced 5 of the 7 T2-reached nulls by pattern; the rest differ in formatting, so the report's breakdown was used. +170 / -150.
- M6: applied. Lines 456, 461: fixtures 25 (disk: 27 files, 25 carry merge_method), reflect SKILL.md 25 (disk: three-term regex gives 25). +0 / -0.
- M7: superseded by B1 item 4 (applied there).
- M8: applied. Line 529 arm C defined as development-build --t2-engine panel or the shadow run with parity assertion; Stage 3 ships the same code. +230 / -0.
- M9: applied. Line 207 cites review-tiers.default.json:10,27 (read and confirmed). +50 / -45.
- M10: recorded, document not changed. Candidate D Verdict dropped "and two merges"; unplanned but consistent with the debate being kept.
- M11: applied. UNVERIFIED marker removed at lines 437 and 589 (SKILL.md:837 read and confirmed). +0 / -110.
