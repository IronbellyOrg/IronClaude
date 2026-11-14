# Merge Execution Log

Slot X-14 `eval-acceptance-and-harness-owner`. Template: `~/.claude/skills/sc-adversarial-protocol/refs/artifact-templates.md` Section 5. Plan: `adversarial/refactor-plan.md` (13 changes). Merged file: `../merged-output.md` (`<slot folder>/merged-output.md`). Line numbers "A:n" are lines of `adversarial/variant-1-original.md`; line numbers "M:n" are lines of the merged file as written.

## Metadata
- Base: Variant A (Proposal A, default model, default persona; `adversarial/variant-1-original.md`)
- Executor: merge-executor agent
- Changes applied: 13 of 13 (see "Adjusted items" below for the entries marked Applied (adjusted))
- Status: success
- Timestamp: 2026-11-14T18:07:42Z

## Changes Applied

Order. The plan's application order is C1, C2, C3, C7, C8, C6, C4, C5, C9, C10, C11, C13, C12. The merged file was composed from the base section by section with that order applied wherever two changes edit the same text. In the shared paragraph A:11, the order was owner sentence (C1, with C4's restated owners), metric sentence (C7), accepted and lead sentences (C8), Tier Q ordering sentence (C6). A:11 was one paragraph; for readability the merged text splits it into three paragraphs (M:22 acceptance, tiers and Tier Q ordering; M:26 metric of record; M:29 ownership), each with its own provenance comment. Re-read after the last change: the three paragraphs agree with each other and with Sections 3, 6, 7, 8 and 9.

### Change 1: Remove the kernel `verify-run` command; the verifier becomes a script
- **Status**: Applied (adjusted)
- **Source**: Variant B Section 1, Section 2 ("Shared core: no change for this slot"), E9, E10; Round 2 of Advocate A (`round2-advocate-A.md` section 0 and 3(d)); Advocate B Round 2 section 2.4 (i) and F-5.
- **Target**: Base A:11 owner sentence; A:27-31 (shared core items 1 to 4); A:33 (script set, extended, not replaced); local edits at A:19, A:20, A:21 (table rows), A:83 (P-2), A:99 (INV-F), A:109 (INV-N), A:113 (M-1), A:121 (M-5), A:127-129 (Section 7 bullets), A:139 and A:141 (Section 8 bullets). A:37 is handled in Change 5. A:38 and A:147 were checked and contain no `verify-run` text, so they needed no edit.
- **Before**: Kernel subcommand `verify_run_cmd.py` registered in `cli/review/__init__.py`, two ledger-entry additions, the verifier importing `findings._check_finding`, a script set that "calls the kernel through the `superclaude` CLI", and `verify-run` named in about 15 places.
- **After**: M:54 "Shared core: none for this slot; kernel files are read, never written, no contract key, ledger key or verdict added". M:62 script set keeps every base item (judge wrapper with completion record and the `wrong_blockers` equation, anonymiser, ground-truth registry, seeded-plan manifest with a clean twin, table builder with exact-key lookup, statistics with minimum detectable effect and comparison count, the three-valued state, "unaudited") and adds the verifier script. M:65-70 describe the verifier (input, `flags.tsv` columns, one severity policy file, three check families, exact keys, `reason` carries no document text, imports public helpers only, precedent `scripts/reflect_shadow_exit.py:50-52`, test file under `tests/`). M:73 holds the "Conditions that would reopen a kernel command" sentence with E-7, E-12 and E-13 kept as evidence. M:191 is the replacement M-5. Local edits: table rows M:43-45, P-2 M:146, INV-F M:173, INV-N M:176, M-1 M:181, Section 7 M:218 and M:220, Section 8 M:238 and M:240.
- **Adjustment**: the base sentence "The scripts call the kernel through the `superclaude` CLI" (end of A:33) would contradict the plan's statement that the verifier imports `superclaude.cli.review` modules. It was reworded at M:62 to "Where a script needs kernel behaviour other than reading its modules, it calls the `superclaude` CLI". The base's conservation text ("the full parse-error list and raw, kept and rejected counts per reviewer") was rewritten to the re-parse form that Change 2 requires (M:68).
- **Provenance tag**: `<!-- Source: Variant 2 (Proposal B), Section 2 ("Shared core: no change for this slot") — merged per Change #1; replaces base items 1 to 4 -->` and the base-modified and Debate tags at M:60-72.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (residual `verify-run` / "kernel command" scan below)

### Change 2: Drop the two ledger-entry additions; compute conservation after the fact
- **Status**: Applied
- **Source**: A Round 2 W1 and N-6; B Round 2 F-7 and section 1.2 (priors never become members); B E9 (`ledger.py:141-149`, `:131-134`).
- **Target**: A:30 (shared core item 3); A:19 (C-01 row DEPENDS clause); A:106-107 (INV-D, INV-C).
- **Before**: "Two ledger-entry additions, both additive" with the claim that `parse_block` "already returns" the counts; INV-D and INV-C as endangered; INV-D question about readers rejecting unknown entry keys left open.
- **After**: M:58 states the one kernel touch the hybrid keeps (the raw text of a rejected line sits behind the private `_blocks_after`, `findings.py:38`; a script imports a private name or the kernel exposes one small public helper; open C-01 and C-06 interaction, probe INV-003 and probe INV-019) and that the law is defined per engine (v1 returns `ok/findings/priors/errors`; v2 returns a `state`, `findings_v2.py:215`; mapping to v2 not settled, shared assumption A-013). M:68 gives conservation as a re-parse compared with the ledger `members`, with the corrected identity `kept = len(findings)` (priors never become members; members filtered by round). M:70 states that the first parse error is folded into a returned warning (`ledger.py:131-134`, returned at `:296`) and that the entry holds five fields. M:43 keeps the bracketed law `raw == kept + rejected-with-reason [+ repaired]`, now computed by re-parse. M:165-166 rewrite INV-C and INV-D: no additive key remains.
- **Provenance tag**: `<!-- Source: Base (original, modified) — item 3 replaced per Change #2 (no ledger-entry additions; conservation computed after the fact) -->` with a Debate tag naming `round2-advocate-A.md` W1 and N-6 and `round2-advocate-B.md` 1.2 and F-7.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: Correct statements of A that the debate found false or inconsistent
- **Status**: Applied
- **Source**: `diff-analysis.md` Summary ("Claims found false or inaccurate"); A Round 1 concessions; A Round 2 sections 1 and 3.
- **Target**: A:65 (E-10, two replacements); A:45 (E-1, the sentence after the quoted rule); A:73 (E-14).
- **Before**: "a silent swap passes `model_ok`"; "the product kernel has no served-model field: no match for ..."; E-1 omitted the control result; E-14 left open whether the `eval_*.py` files have tests.
- **After**: M:123 (E-10): the `:75` log line, `meta.json` holds `observed_model`, `:58` writes `expected_model` from the overwritten `$MODEL`, so `model_ok` passes against the swapped expectation, and the `meta.json` fields A's advocate read hold none that keeps the originally requested model; the served-model field is declared and read (`telemetry.py:49`, `:364`, `:378`; `SKILL.md:341`) with no writer, so the accurate claim is "no populated, reliable record". M:94 (E-1): control wrong blockers were 0, 0, 0, so the control clause does not change the outcome. M:133 (E-14): only `eval_runner.py` and `eval_workflow_vs_task_builder.py` have a test file; the tested precedents are the five `reflect_*.py` and those two.
- **Provenance tag**: `<!-- Source: Base (original, modified) — E-10 corrected per Change #3 (two local replacements) -->`, `... E-14 test-file statement added per Change #3 -->`, E-1 tag combined with Change #7.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: the E-10 tag "[CODE-VERIFIED by A's advocate in Round 1, A-S5]" is copied as the plan specifies. The Round 1 file is not among this run's inputs; `round2-advocate-A.md` W2 re-confirms the `:58` read.

### Change 7: Metric of record, per-item reporting, secondary columns, unmatched blocking rows, minimum detectable effect, double-scored sample
- **Status**: Applied
- **Source**: A Round 2 N-4 and section 3(d) item 2; B Round 2 sections 2.3, 3(a) F-1 to F-4, 3(c); B E4, E5, E6.
- **Target**: A:11 metric sentence; A:45 (E-1), A:49 (E-3), A:51 (E-4).
- **Before**: metric of record with "wrong blockers"; any-severity count "stays in the report as a secondary number and gates nothing"; E-3 with 65 against 38 only; E-4 with the 131 of 147 concentration only.
- **After**: M:26 (per item; unmatched blocking rows until a blind adjudication exists, with `PILOT-REPORT.md:79`; any-severity count and control ceiling as secondary columns that gate nothing at pilot n; minimum detectable effect and comparison count up front, "no evidence" valid; double-scored judge sample, R16:134; the rule is committed after C-02 lands). M:94 adds GT7 (`blocking_in_implement: false`) and the `PILOT-REPORT.md:61` quote. M:101 adds 89 against 38 (51 outside blocking rows is B's arithmetic), the `COMBO-REPORT.md:291` reversal, the typing dependence on C-02, and 81 of the 89 on two items. M:105 adds the ground-truth flags (5 + 3 + 0 of 10 + 4 + 2), GT7 at 34 percent, and per-item reporting.
- **Provenance tag**: `<!-- Source: Base (original, modified) — metric sentence extended per Change #7 -->`, `<!-- Source: Variant 2 (Proposal B), E4 and E6; Debate (round2-advocate-A.md section 3(d) N-4) — merged per Change #7 -->`, `... E-4 extended with the ground-truth flags per Change #7 -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: probe INV-012 (part of the 89 against 38 gap may be rejected blocking lines, not typing) is carried at M:101 as an open question and at M:314.

### Change 8: Status wording for "accepted"
- **Status**: Applied (adjusted)
- **Source**: A Round 2 section 1 W4 and section 4 C-001; B Round 2 section 2.4 (iii) and section 2.4 closing; diff points C-008 and X-004 (UNRESOLVED by label).
- **Target**: A:11 first sentence and the "lead" sentence; A:126 (Section 7 status); A section 9 (owner definition).
- **Before**: "accepted for a use case only on three tiers of evidence ... Anything weaker than S, Q and G for that use case is a lead, as E1's own `PLAN.md:184` says"; Section 7 "status lead".
- **After**: M:22 "A use case is accepted only with Tier S, a pre-registered Tier Q and Tier G. A use case with Tier S and Tier Q only is 'not worse on what is pinned, lead only'. Building and shadow runs are not held up by the status", then the open statement that Tier S includes the identity check, which may stay `unrecorded` for good if C-08's M1 fails (probe INV-026), so "accepted" is unreachable while it does (the debate did not decide what then happens). M:217 keeps the status "lead" for PR review and rf-qa until a seeded set with a clean twin exists and states building and shadow runs are not held up. M:259 records that the wording is an owner definition with no code falsifier, that Tier G is unbuilt and not unbuildable (`PILOT-REPORT.md:83`; R16:157), and that who writes and pays for it is open (R16 Q2, Q3, Q7).
- **Adjustment**: the plan replaces the base "lead" sentence, which carried the citation "`PLAN.md:184`". Advocate A's Round 2 N-3 found that quote accurate but not a Tier G definition (it is E1's rule for separating combinations at n=3). The citation was kept in that narrowed form (M:22, last sentence) instead of being dropped; no design content is added.
- **Provenance tag**: `<!-- Source: Base (original, modified) — acceptance sentence and "lead" wording replaced per Change #8; Tier Q commit timing per Change #6 -->` plus `<!-- Source: Debate (round2-advocate-A.md), section 3(c) N-3 — merged per Change #8 (scope of the "lead" quotation) -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: B's offline metric-discrimination test and the ordering test
- **Status**: Applied (adjusted)
- **Source**: B Section 5 M2 and M3; B Round 2 section 3(a) F-3 and section 3(b) (mix H3).
- **Target**: A:11 Tier Q sentence (timing); new M-7 in Section 6.
- **Before**: Tier Q "committed in a commit that precedes the first run commit"; no offline discrimination test.
- **After**: M:22 one timing (M-7 offline first, re-run after C-02 lands; rule, analysis script and values file committed after C-02 lands and before the first run commit; rule commit sha recorded in the run record, marked as a Round 2 addition by A's advocate and contested: diff point C-007, probe INV-002). M:197 M-7 with four metrics, B's prediction left as a prediction, the re-run after C-02. M:199-211 quote B's F-3 proxy table with B's own tag.
- **Adjustments**: (1) The plan's Risk Summary row 6 says "Keep the proxy tagged [UNVERIFIED]", while the Overview rule and Change 6's integration point say to copy the source's tag. B tagged F-3 `[CODE-VERIFIED arithmetic on PF:2-8; a proxy, not the metric of record]`. I followed the Overview rule and Change 6 and kept the "a proxy, not the metric of record" wording. The orchestrator may want to resolve that row of the Risk Summary. (2) B's M2 says the comparison is fixed "with a rule written down before it is run", while the plan commits the acceptance rule after C-02 lands. To keep one timing, M-7 says the comparison (four metrics, separation against run-to-run spread, permutation test) is fixed in writing before M-7 is run, and the acceptance rule is committed afterwards.
- **Provenance tag**: `<!-- Source: Variant 2 (Proposal B), Section 5 M2 and M3; Debate (round2-advocate-B.md section 3(a) F-3 and section 3(b)) — merged per Change #6 -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: Tasklist review in the named modules; import of the E2 harness
- **Status**: Applied
- **Source**: B Section 2 (tasklist review bullet) and E8; Scoring Matrix S-005; shared assumption A-008.
- **Target**: A Section 3 "Named modules" (new bullet after the spec-review loop); A:11 two-owners statement; A:39 (`.dev/` bullet).
- **Before**: no tasklist-review entry; "the two harness layers have two named owners"; "`.dev/` keeps run outputs and per-run data only".
- **After**: M:79 new bullet (0 tracked files; study tip not an ancestor of HEAD; `.gitignore:13`; generic code moves to `scripts/` with tests; study data, ground truth, values files and run outputs stay under `.dev/eval-workspaces/tasklist-review-panel/`; owner and `.gitignore` exception are owner decisions, not made; one sentence to `.dev/README.md` line 5; departs from the letter, not the purpose). M:29 restates the owners (kernel is not an owner; script set owns generic code; `.dev/` owns run data, ground truth and values files). M:86 `.dev/` bullet adds ground truth and values files.
- **Provenance tag**: `<!-- Source: Variant 2 (Proposal B), Section 2 (Named modules, tasklist review) and E8 — merged per Change #4 -->`, `<!-- Source: Base (original, modified) — ground truth and values files added per Change #4 -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: The two reflect-gate repairs and the gate-bite test
- **Status**: Applied
- **Source**: B Section 2 (Reflect Tier 2 bullet) and M4; Scoring Matrix C-010; A Round 2 section 3(d) item 7; B Round 2 section 2.2.
- **Target**: A:37 (reflect bullet scope sentence); new M-6.
- **Before**: the two defects "are defects in that gate, outside this slot".
- **After**: M:82 brings the two repairs and the gate-bite test into scope with the critical-path reason (C-08's identity gate is added to the same script, ADJ-C08). M:194 M-6 (empty legacy baseline read as "no baseline"; where required runs are missing it still reports a failing or insufficient state; Right if / Wrong if wording kept; contract bytes untouched; open: `legacy_runs` skips pre-runs with a panel manifest, 15 tracked runs below `REQUIRED_RUNS` 20, so the repaired gate may reach INSUFFICIENT-RUNS and never PASS, probe INV-017; "not worded as 'must still FAIL'"). The 15 figure is attributed to the fault-finder; B's M4 count (14, 13 published) is listed as unreconciled at M:345.
- **Provenance tag**: `<!-- Source: Variant 2 (Proposal B), Section 2 (Reflect Tier 2 bullet) and M4; Debate (round2-advocate-B.md section 2.2) — merged per Change #5 -->`, `<!-- Source: Variant 2 (Proposal B), Section 5 M4; Debate (invariant-probe.md, probe INV-017) — merged per Change #5 -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Identity check design aligned with the adjudicated C-08
- **Status**: Applied
- **Source**: B Round 2 F-5; A Round 2 N-1 and separability item 2; ADJ-C08 (as cited by B).
- **Target**: A Section 3 script set (identity check, in the verifier description); A Section 2 paragraph "Where this proposal adds something these slots do not say" (A:23) and one new sentence after A:15.
- **Before**: "Nothing below disagrees with a recorded outcome", written against three slots; identity as a Tier S check reporting `unrecorded` when the record is absent.
- **After**: M:36-38 one sentence that C-06 and C-08 have been adjudicated since and bear on this slot (probe INV-019 for C-06, ADJ-C08 for C-08), pointing to Section 10. M:49 identity paragraph: no code writes `model.observed` (`telemetry.py:49,364,378`; transport `openai_compat.py:385`, `:468-469`); C-08's identity gate lives in `scripts/reflect_shadow_exit.py` reading `panel/events.jsonl` read-only, ships only after M1, 13 HIGH invariants unaddressed including C-08 INV-013; the verifier's `unrecorded` and C-08's `requested-pinned` differ (probe INV-021); the dispatch-time expected-cells manifest is owed to the dispatch slot and is in no adjudicated merged output (probe INV-005). M:66 identity family `unrecorded` until a writer exists. Table rows were not rewritten beyond Changes 1 and 2. The Section 2 heading keeps the base wording "three adjudicated slots" because the table still covers C-01 to C-03.
- **Provenance tag**: `<!-- Source: Base (original, modified) — identity paragraph replaced per Change #9 -->` with Debate tags for `round2-advocate-A.md` N-1, `round2-advocate-B.md` F-5 and F-6, and the probe.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: Rewrite A Section 5 Invariants
- **Status**: Applied (adjusted)
- **Source**: A Round 2 N-2; B Round 2 sections 1.1 (B-W8), 1.2; diff points S-003, C-016.
- **Target**: A Section 5 "Preserved" and "Endangered" lists.
- **Before**: INV-F preserved by placement; INV-H, INV-D MEDIUM, INV-C LOW, INV-K LOW, INV-N endangered.
- **After**: M:163-170 Preserved: INV-A, INV-B, INV-C, INV-D, INV-E, INV-I, INV-L, repository rules. M:173-176 "Conditional or endangered": INV-F (neutral today, stays HIGH as the trigger of the reopen condition; "preserved by placement" withdrawn), INV-H MEDIUM (reader exists wherever the verifier lives; the `reason` test is needed in `scripts/`), INV-K LOW (lint-architecture [UNVERIFIED]; `.gitignore:13` and CI collecting `tests/` added with probe INV-022 and probe INV-023), INV-N (only if skill prose names the verifier). Each entry names the Round 2 fact that moved it.
- **Adjustment**: the plan says "INV-D, INV-C: no additive key remains" without naming the list. I placed INV-C and INV-D under Preserved because the reason that endangered them (additive entry keys) no longer exists. INV-F left Preserved for the conditional list because the plan withdraws "preserved by placement". INV-N stays a conditional entry.
- **Provenance tag**: `<!-- Source: Base (original, modified) — lists rewritten per Change #10 -->` plus a Debate tag.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Strongest-objection section, concessions and the flip condition
- **Status**: Applied
- **Source**: B Section 7 answer 5; A Round 2 section 0; B Round 2 sections 0 and 2.3.
- **Target**: A Section 8, after "Answer".
- **Before**: an answer with no concessions and no condition under which the other position is better.
- **After**: M:230-234 "Concessions and the flip condition": four concessions (kernel command withdrawn with its ledger additions; served-model check stays `unrecorded`; blocking recall 0 of 8 so "no evidence" at pilot n; `scripts/` tests couple CI to `findings.py`), the flip condition both advocates named, and the verification status (present half verified, tagged with B's E10 tag; future half not).
- **Provenance tag**: `<!-- Source: Variant 2 (Proposal B), Section 7 answer 5; Debate (...) — merged per Change #11 -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: the "no caller found in `src/`, `plugins/`, `Makefile`, `.github/`, `.claude/settings.json`" claim was spot-checked by the merge executor with a read-only grep for `reflect_shadow_exit`, `reflect_verdict_replay`, `verify-run` and `verify_run` over those paths: no matches. The tag in the text is still the source's.

### Change 13: Section 9 and the header
- **Status**: Applied
- **Source**: B Section 8; B reading note (B:15); A Section 9.
- **Target**: A Section 9; A header paragraph.
- **Before**: five non-claims; header with status line and code-state line.
- **After**: M:5-16 header keeps "Status: Complete", the code-state line (HEAD `50d4d2b9d`) and the study-tip pin, and adds the merge note (base, inputs, hybrid), the tag convention, citation forms and the id legend. M:251-259 add B's open facts (12-row blind re-judge; j1 audit gap), the import statement (`scripts/reflect_shadow_exit.py:50-52`, `tests/cli/reflect/test_shadow_exit_script.py:18-21`; untested under `.dev/`), "the kernel command is deferred, not rejected", and B's reading note on the control ceiling. The thresholds T-1..T-10, stop rule S-0..S-5 and ground-truth authorship items were not duplicated.
- **Provenance tag**: `<!-- Source: Variant 2 (Proposal B), Section 8 (open facts) and reading note (B:15) — merged per Change #13 -->` and `<!-- Source: Variant 2 (Proposal B), Section 2 and Debate (...) — merged per Change #13 -->`.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: New Section 10, "Debate status and conditions left open"
- **Status**: Applied (adjusted)
- **Source**: `invariant-probe.md` (29 findings); Convergence Assessment and Scoring Matrix of `debate-transcript.md`; `base-selection.md`.
- **Target**: new Section 10 after A Section 9 (M:261-355).
- **Before**: section did not exist.
- **After**: 10.1 debate status (Mode A, standard; Round 1 28 of 44 = 63.6%; Round 2 40 of 44 = 90.9%, 83.3% on the 24 points with a named winner; threshold 80%; BLOCKED_BY_INVARIANTS; tiebreaker at 0.97%, A 0.9157, B 0.9060; qualitative 25/30 each; points won A 11, B 9; correctness A 3, B 2; force-select by score; flagged for review). 10.2 the four UNRESOLVED points (C-005, C-007, C-008, X-004) with each advocate's final call. 10.3 id legend. 10.4 the 12 HIGH items (probe INV-001, 002, 003, 005, 006, 007, 013, 019, 021, 025, 026, 027), one sentence each. 10.5 the 13 MEDIUM items (probe INV-004, 008, 011, 012, 015, 016, 017, 018, 020, 022, 023, 028, 029). 10.6 the 4 ADDRESSED items (probe INV-009, 010, 014, 024). 10.7 open facts (probe "Open items" plus the advocates' [UNVERIFIED] items). 10.8 no decisive point rests on a [POST-BASELINE] fact.
- **Adjustment**: the probe item probe INV-015 cites an id of the dispatch slot ("dispatch INV-011"). It is not one of the five prefixes in the plan's legend, so I added `dispatch INV-nnn` to the legend (M:16) and wrote it prefixed at M:315. The id legend appears at the top of the file (as the plan's Overview requires) and again at M:284 (10.3).
- **Provenance tag**: `<!-- Source: Debate (invariant-probe.md), findings probe INV-001 to probe INV-027 (HIGH, UNADDRESSED) — merged per Change #12 -->` and the sibling tags at M:263, M:308, M:327, M:337, M:352.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ One H1 (M:5), H2 sections 1 to 10 in A's numbering, H3 4.1 to 4.3 under Section 4 and 10.1 to 10.8 under Section 10. No level gaps, no orphan H3. Sections 3, 5 to 9 use bold labels and lists as the base does.
- Section ordering: ✅ 1 position, 2 consistency with the adjudicated slots, 3 design consequence, 4 evidence, 5 invariants, 6 measurements, 7 PR review and rf-qa, 8 strongest objection, 9 non-claims, 10 debate status. Prerequisites come before dependents; Section 10 is last, as Change 12 requires.
- Document flow: ✅ Header and id legend, then the position; the evidence in Section 4 sits under the claims it supports; M-5 to M-7 follow M-1 to M-4; the concessions follow the Answer; Section 10 closes with "Status: Complete" as the base does.
- Provenance: ✅ Header comments (Provenance, Base, Merge date) at M:1-3; a `<!-- Source: ... -->` comment before every section and every modified or incorporated block; debate-derived content tagged `Debate (<file>), <ref> — merged per Change #N`. Annotations are HTML comments only. No "Change N" wording appears in the document body outside provenance comments (grep over body lines: the only other hit is "refactoring plan" in the merge note, which names an input file).

### Internal References
- Total references: 84 (body lines only, counted after the check): 37 "Section n" references, 26 E-n references (excluding the 15 definitions), 16 M-n references (excluding the 7 definitions), 3 P-n references (excluding the 5 definitions), 2 sub-section references ("(10.4)", "10.4 to 10.6").
- Resolved: 84
- Broken: 0
- Spot checks: "Section 4, E-1" (M:45) resolves to E-1 at M:94; "M-6 (Section 6)" (M:82) to M-6 at M:194; "M-7 (Section 6)" (M:22) to M-7 at M:197; "Section 10, probe INV-003" (M:58, M:70) to the row at M:295; "E-12 and E-13 (Section 4)" (M:73) to M:128 and M:130; "(Section 5, INV-H)" (M:330) to M:174.
- Id-prefix check: ✅ Every `INV-nnn` in the file carries a prefix: `probe INV-nnn`, `C-01 INV-nnn`, `C-02 INV-nnn`, `C-03 INV-nnn`, `C-06 INV-nnn`, `C-08 INV-nnn`, and once `dispatch INV-nnn` (M:315). A regex scan for an `INV-` plus three digits not preceded by one of those prefixes prints nothing. The letters INV-A to INV-N appear only as in A Section 5 (INV-A to INV-E, INV-F, INV-H, INV-I, INV-K, INV-L, INV-N). The first scan found one bare id (the dispatch slot's INV-011 at M:315); it was fixed by adding the `dispatch` prefix and noting it in the legend at M:16.
- Probe counts against `invariant-probe.md` (29 findings: 4 ADDRESSED, 25 UNADDRESSED, 12 HIGH, 13 MEDIUM): ✅ Section 10 holds 12 HIGH rows (probe INV-001, 002, 003, 005, 006, 007, 013, 019, 021, 025, 026, 027), 13 MEDIUM rows (004, 008, 011, 012, 015, 016, 017, 018, 020, 022, 023, 028, 029) and 4 ADDRESSED rows (009, 010, 014, 024); a row count over M:288-334 gives 29 distinct `probe INV-nnn` ids.
- Evidence tags: ✅ None upgraded or removed. Counts of `[CODE-VERIFIED` 35, `[UNVERIFIED` 27, `[CODE-CONTRADICTED` 1, `[POST-BASELINE` 11. Every A tag at its original place is unchanged; tags added by the merge are copied from the source (Advocate A, Advocate B, the diff analysis or the probe). No fact from commit `c44c98a77` is the only evidence for any decisive point (M:353). The one item where two parts of the plan disagree on a tag (M-7 proxy) is described under Change 6.

### Residual check for Change 1 (`verify-run`, `verify_run_cmd`, "kernel command")
A grep over the merged file for `verify-run`, `verify_run[a-z_]*` and `kernel command` gives the hits below. `verify_run_cmd` itself appears nowhere.

| M line | Section | Occurrence | Why it is allowed |
|---|---|---|---|
| M:10 | header merge note | "no kernel `verify-run` command" | describes the hybrid by naming the position that was withdrawn |
| M:73 | 3 | "Conditions that would reopen a kernel command"; "no `verify-run` exists at HEAD" | the reopen sentence, and its reference to E-7 |
| M:115 | 4.2 | E-7 title and its `git grep -n -E "verify-run|verify_run"` | E-7 (kept as the evidence that no `verify-run` exists at HEAD) |
| M:232 | 8 | "the kernel `verify-run` command that the base proposal argued for is withdrawn" | concession required by Change 11; quotes the withdrawn position |
| M:233 | 8 | "a kernel command is the better design if ..." | the flip condition required by Change 11 (names the same condition as the reopen sentence) |
| M:240 | 8 | "no kernel `verify-run`" and "the absence of a kernel command" | quoted statement of Proposal B's position, and what this document takes from it |
| M:257 | 9 | "The kernel command is deferred, not rejected" | statement required by Change 13 |
| M:271 | 10.1 | "withdrew the kernel `verify-run` command" and "no kernel command" | Section 10 |

Hits at M:232, M:233, M:240 and M:257 are outside the plan's list of allowed places (reopen sentence, E-7, E-12, E-13, M-5 pin sentence, section 10) but are required by Changes 11 and 13 or quote the withdrawn position. No residual hit describes `verify-run` as part of the design. E-12 and E-13 (M:128, M:130) do not contain the strings; they keep the `verify-citations` precedent and the INV-F argument, as Change 1 asks. M-5 (M:191) says "the later kernel move" and has no matching string. An earlier draft of M:218 (Section 7) had a "kernel command" hit; it was reworded to "a `superclaude` CLI subcommand".

Base script-set items still present (M:62, M:65-67): ✅ judge wrapper with completion record (judge model, prompt hash, script hash, input hashes, `score.json` hash, exit status) and the `wrong_blockers = ledger_rows_blocking - blocking_rows_gt_matched` check; anonymiser; ground-truth registry (hashes, mechanical quote checks, `dropped`-with-reason list); seeded-plan manifest with a clean twin; table builder with exact-key lookup (and the refusal of a run directory with no verifier record); statistics with a stated minimum detectable effect and comparison count; the three-valued state `pass / flag / unrecorded`; "unaudited" as a reported state (a run not in the manifest).

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details:
  - Two contradictions in the base are gone because of the plan: A's additive ledger keys against "Nothing below disagrees with a recorded outcome" (Change 2), and "never importing a v1 or v2 engine internal" against `findings._check_finding` (Change 1).
  - Tension that is stated, not hidden: Section 3 says the shared core has "none for this slot" (M:54) and also names one open kernel touch (M:58: a script imports a private name or the kernel exposes one small public helper). The plan prescribes both; the second is marked open and tied to probe INV-003 and probe INV-019.
  - The word "lead": Section 1 uses "not worse on what is pinned, lead only" for a use case with Tier S and Tier Q, and Section 7 keeps the plain status "lead" for PR review and rf-qa, which have no ground truth. The usage is consistent (neither is "accepted").
  - Left unchanged because the plan did not change it: P-1 (M:143) still says what is missing is one shared verifier. Advocate A's Round 2 W9 conceded P-1 as non-decisive; P-1 is tagged [POST-BASELINE] and M-4 is its own falsifier, so it is not a contradiction.
  - Observation, not a contradiction: M:317 (probe INV-017) and M:194 (M-6) both carry the open question about the empty-baseline verdict, and the 15 against 14 (13 published) manifest count is listed as unreconciled (M:345).

## Summary
- Total changes planned: 13
- Successfully applied: 13 (8 as written: Changes 2, 3, 4, 5, 7, 9, 11, 13; 5 as Applied (adjusted): Changes 1, 6, 8, 10, 12)
- Failed: 0
- Skipped: 0
- Adjusted items for the orchestrator: (1) Change 1, the base sentence "The scripts call the kernel through the `superclaude` CLI" reworded because the verifier imports kernel modules; (2) Change 6, plan Risk Summary row 6 says tag the proxy [UNVERIFIED] but Change 6 and the Overview say copy the source's tag, so B's `[CODE-VERIFIED arithmetic on PF:2-8; a proxy, not the metric of record]` was kept; the plan row should be reconciled; (3) Change 8, the narrowed `PLAN.md:184` quotation kept from Advocate A's Round 2 N-3; (4) Change 10, INV-C and INV-D placed under Preserved, INV-F under the conditional list; (5) Change 12, `dispatch INV-nnn` added to the id legend for one probe-sourced id.
- Facts the sources could not settle, carried as open: see Section 10.7 of the merged file. The E-10 Round 1 tag "A-S5" is copied from the plan; the Round 1 file was not in this run's inputs.
- Post-merge validation: PASS

