# Base Selection: Reflect Reviewer-Card Comparison

## Metadata

- Step: sc:adversarial Step 3 (Hybrid Scoring & Base Selection), Mode A
- Generated: 2026-11-04
- Variants: variant-1 = reviewer-1 (sonnet, analyzer); variant-2 = reviewer-2 (glm-5.3 in haiku slot, qa); variant-3 = reviewer-3 (opus, refactorer)
- Inputs: `variant-{1,2,3}-original.md`, `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `../artifacts/coverage-matrix.json` (17 INF rows), plan source `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/source.md`
- Ground truth used for correctness: plan line 80 says "bare `/ponytail` switches to `full`"; `/tmp/ponytail-src-t14b/mode-tracker.js:109-119` shows bare `/ponytail` reports and keeps the level when on, and switches to `getDefaultMode()` (lite) when off, with `full` only when the default is `off` (line 117). Re-read for this step. Variant 2's "no false claims found" and verdict `pass` are therefore judged factually wrong, whatever the card reports about itself.

## Quantitative Scoring (50% weight)

### Summary

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|--------|--------|-----------|-----------|-----------|
| Requirement Coverage (RC) | 0.30 | 0.765 (13/17) | 0.706 (12/17) | 0.765 (13/17) |
| Internal Consistency (IC) | 0.25 | 1.000 (0/13) | 0.900 (1/10) | 1.000 (0/21) |
| Specificity Ratio (SR) | 0.15 | 0.935 (29/31) | 0.938 (15/16) | 0.971 (34/35) |
| Dependency Completeness (DC) | 0.15 | 1.000 (1/1) | 0.000 (0/2) | 1.000 (1/1) |
| Section Coverage (SC) | 0.15 | 0.444 (4/9) | 0.444 (4/9) | 1.000 (9/9) |
| **quant_score** | | **0.836** | **0.644** | **0.925** |

Formula: `quant = RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15`.

- V1: 0.2294 + 0.2500 + 0.1403 + 0.1500 + 0.0667 = 0.8364
- V2: 0.2118 + 0.2250 + 0.1406 + 0.0000 + 0.0667 = 0.6441
- V3: 0.2294 + 0.2500 + 0.1457 + 0.1500 + 0.1500 = 0.9251

### Computation notes

**RC.** The source has no FR/NFR IDs, so the 17 inferred rows (INF-001..INF-017) are the requirement list. A variant covers a row when one of its findings, or its `confirmed_claims` / `coverage_check` / `scope_check` / `verified_adherent` block, names that row's subject specifically. A generic "16 units adherent" does not cover a row by itself.

| Row | Subject | V1 | V2 | V3 |
|-----|---------|----|----|----|
| INF-001 | implement merged-requirements.md | Y (R1-F1 cites merged-requirements.md:140,171) | Y (R2-F3/F4 cite merged-requirements.md:281,283-286) | Y (R3-2 cites merged-requirements.md:111; R3-5 :140) |
| INF-002 | env lite, filled only when unset | N | Y (R2-F1: Task 1 leg 2 + fill loop, install_user_setup.py:36,151-164) | Y (verified_adherent: fill semantics :36,150-164) |
| INF-003 | off rewritten to lite everywhere | Y (notes: F-2/INF-003 authorized; R1-F1 off-era text) | Y (R2-F1: lite in tests, docs, CHANGELOG, M1b) | Y (verified_adherent: Task 1 matches Design 3.1 with lite) |
| INF-004 | ledger on, `ledger` option off | Y (confirmed: plugin.json:15-20) | N | N |
| INF-005 | SessionStart flag + lite ruleset | Y (confirmed: runtime.js:51-66, instructions.js:11-41, skill.md:50) | Y (R2-F1: INF-005 owned by Task 3) | N |
| INF-006 | codebase map + SubagentStart injection | Y (confirmed: subagent.js:17-49) | N | N |
| INF-007 | one-time statusline nudge | Y (confirmed: activate.js:109-134,148-153) | Y (R2-F1: INF-007 owned by Task 3) | N |
| INF-008 | `/ponytail default` no effect while env set | Y (confirmed: config.js:80-105, mode-tracker.js:67-77) | N | Y (R3-5: PONYTAIL DEFAULT SET claim) |
| INF-009 | docs: change mode, opt out | Y (R1-F1: bare /ponytail behaviour) | N | Y (R3-5: bare /ponytail, project settings precedence) |
| INF-010 | defaults JSON, three entries | N | N | Y (R3-6: JSON entry shape) |
| INF-011 | FR-005 fix, at most 5 lines | Y (R1-F3) | Y (R2-F3; T5 fails on :292,303,305) | Y (R3-2; scope_check) |
| INF-012 | tests T1..T5c with lite | Y (confirmed: T1/T3/T4/T5) | Y (named_tests_fail_on_defect) | Y (verified_adherent: test ranges, T5c :258) |
| INF-013 | installation.md + CHANGELOG | Y (confirmed: installation.md, CHANGELOG refs) | Y (R2-F1; six-plugins grep by Task 3) | Y (R3-4, R3-7) |
| INF-014 | no change to main.py, update.sh, .claude/ ... | N | Y (R2-F1: INF-014 in Constraints) | Y (scope_check: forbidden_file_edits none, claude_dir_staging none) |
| INF-015 | checks list incl. tests reading edited files | Y (confirmed: 'six plugins' only at installation.md:354) | Y (every_spec_check_owned) | Y (R3-4: tests/docs unowned) |
| INF-016 | manual AC-M1 never touches ~/.claude | Y (R1-F2) | Y (R2-F4) | Y (R3-1, R3-8) |
| INF-017 | superseded package untouched | N | Y (R2-F1: INF-017 in Constraints) | Y (verified_adherent: superseded package untouched) |
| **Total** | | **13** | **12** | **13** |

**IC.** Scorable claims = each finding plus each specific assertion in the summary blocks and notes (V1: 4 findings + 6 confirmed assertions + 3 notes = 13; V2: 4 coverage_check assertions + 4 findings + 2 notes = 10; V3: 5 scope_check flags + 9 findings + 7 verified_adherent assertions = 21). Contradictions found: V1 none (verdict comment "1 blocking (plus 1 conditional), 2 minor" matches F1..F4). V2 one: `coverage_check.fully_adherent: 16` of 16 against its own R2-F3 `deviation_class: drift` (a unit cannot be fully adherent and drift at once). V3 none (verdict comment "1 blocking (R3-1), 8 minor" matches R3-1..R3-9). IC measures internal contradictions only; V2's external false claim is scored in the qualitative Correctness dimension.

**SR.** Counted over every line after the 6-line header block (metadata excluded). Concrete = file:line citations (regex `\.(py|js|md|json|yaml|tsx|sh):[0-9]+`) + numeric thresholds (`<= N`, `N s`, `N insertions/deletions/lines`) + named mechanisms (`CLAUDE_CONFIG_DIR`, `XDG_CONFIG_HOME`, `PONYTAIL_*`, `env -u`, `git diff --numstat`, `getDefaultMode()`, `markdownlint`). Vague = appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard, likely, could, may, possibly, probably.
- V1: 20 + 3 + 6 = 29 concrete, 2 vague ("could" x2) -> 29/31 = 0.935
- V2: 11 + 4 + 0 = 15 concrete, 1 vague ("likely") -> 15/16 = 0.938
- V3: 20 + 6 + 8 = 34 concrete, 1 vague ("may") -> 34/35 = 0.971

**DC.** Internal references = verdict annotations that count the card's own findings, cross-references between the card's own IDs, and counts that summarise an enumeration inside the card. References to plan lines, INF rows, other reviewers' IDs and files are external and excluded.
- V1: verdict "1 blocking finding (plus 1 blocking-conditional), 2 minor" resolves to F1/F2/F3+F4. 1/1. (Notes' "F-2" is the pre-flight finding ID, external.)
- V2: `spec_units_audited: 16 / fully_adherent: 16` names 16 units the card never lists (unresolved); R2-F1 "All eight containment-unmapped rows" lists only seven IDs (INF-002, 015, 014, 017, 005, 007, 003; INF-001 is missing) (unresolved). 0/2.
- V3: verdict "1 blocking (R3-1), 8 minor" resolves to R3-1 and R3-2..R3-9. 1/1.

**SC.** Per the instruction, each top-level finding is a section: V1 4, V2 4, V3 9; max 9.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

CEV rule: MET needs a specific citation from the card; with no citation the verdict is NOT MET. Final verdicts below are after position-bias resolution.

### Completeness (5 criteria)

| # | Criterion | Variant | Claim | Evidence | Verdict |
|---|-----------|---------|-------|----------|---------|
| 1 | Covers all explicit requirements | V1 | not met | RC table: INF-002, 010, 014, 017 not addressed | NOT MET |
| 1 | | V2 | not met | RC table: INF-004, 006, 008, 009, 010 not addressed; "16 of 16 adherent" is a bare count | NOT MET |
| 1 | | V3 | not met | RC table: INF-004, 005, 006, 007 not addressed | NOT MET |
| 2 | Edge cases and failure scenarios | V1 | met | R1-F1 on/off branches of bare /ponytail; R1-F2 CLAUDE_CONFIG_DIR bypass | MET |
| 2 | | V2 | met | R2-F3 "'At most 5 changed lines' can false-FAIL" | MET |
| 2 | | V3 | met | R3-1 two env bypass routes; R3-8 Orca step eating 25 of 30 s | MET |
| 3 | Dependencies and prerequisites | V1 | not met | Searched findings, confirmed_claims, notes: no task or test dependency analysis; only a grounding gap on env state | NOT MET |
| 3 | | V2 | met | every_spec_check_owned: Task 2 list "includes test_install_retired_mcp.py which patches install_user_setup at :522" | MET |
| 3 | | V3 | met | R3-3 "Task 2 independent of Task 1; Task 3 needs Task 1 only" | MET |
| 4 | Success/completion criteria | V1 | met | R1-F3 "git diff --numstat insertions <= 5"; R1-F2 "record that the real ~/.claude/settings.json and ~/.claude/plugins/ are unchanged" | MET |
| 4 | | V2 | met | R2-F3 "<= 4 insertions, <= 3 deletions" | MET |
| 4 | | V3 | met | R3-2 "numstat <= 5 insertions and <= 5 deletions, all inside install_plugins" | MET |
| 5 | Explicit out-of-scope | V1 | met | notes: "editing the brainstorm file is not needed"; "Not verified from fetched files: band/register.tsx, project settings precedence, commit 96608e07" | MET |
| 5 | | V2 | met | notes: "Upstream Ponytail facts taken as given (not in grounding root)" | MET |
| 5 | | V3 | met | scope_check: `new_mechanism: none, forbidden_file_edits: none, claude_dir_staging: none` | MET |

Subtotal: V1 3/5, V2 4/5, V3 4/5.

### Correctness (5 criteria)

| # | Criterion | Variant | Claim | Evidence | Verdict |
|---|-----------|---------|-------|----------|---------|
| 1 | No factual errors | V1 | met | R1-F1 matches mode-tracker.js:109-119; no claim withdrawn as false in debate (F2 severity and F3 class were calibration concessions, not false facts) | MET |
| 1 | | V2 | not met | notes "no false claims found" and verdict `pass` are false: plan:80 contradicts mode-tracker.js:109-119; `every_spec_check_owned` overclaimed (tests/docs unowned, X-002, conceded) | NOT MET |
| 1 | | V3 | not met | R3-5 "the reset clause was grounded only on the off path": withdrawn in debate, reset is grounded at hooks_ponytail-activate.js:193,55 | NOT MET |
| 2 | Approaches feasible | V1 | met | R1-F2 "env -u CLAUDE_CONFIG_DIR (or set it to <throwaway>/.claude)" | MET |
| 2 | | V2 | met | R2-F3 counting rule is executable; R2-F1/F2/F4 "no change" recommendations are executable | MET |
| 2 | | V3 | met | R3-1 "env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME HOME=$H"; R3-4 "uv run pytest tests/docs" | MET |
| 3 | Terminology consistent and accurate | V1 | not met | R1-F3 classes an AC ambiguity as `authorized` (expansion); conceded misclassified in Round 1 | NOT MET |
| 3 | | V2 | not met | R2-F3 classes an ambiguity as `drift`; R2-F4 is a finding with `deviation_class: none`; `fully_adherent: 16` beside a drift | NOT MET |
| 3 | | V3 | met | ambiguities as `grounding_gap` (R3-2, R3-3, R3-5..R3-9), plan omissions as `drift` (R3-1, R3-4); debate adopted V3's class for C-003 | MET |
| 4 | No internal contradictions | V1 | met | IC 1.000 | MET |
| 4 | | V2 | not met | IC 0.900: fully_adherent 16/16 vs R2-F3 drift | NOT MET |
| 4 | | V3 | met | IC 1.000 | MET |
| 5 | Claims supported by evidence | V1 | met | every finding carries file:line evidence (e.g., R1-F1 mode-tracker.js:109-119) | MET |
| 5 | | V2 | not met | headline claims (16/16 adherent, "no false claims") carry no per-unit evidence and are refuted by mode-tracker.js:109-119 | NOT MET |
| 5 | | V3 | met | every finding carries file:line evidence (e.g., R3-4 tests/docs/test_retired_docs_absent.py:39-44) | MET |

Subtotal: V1 4/5, V2 1/5, V3 4/5.

### Structure (5 criteria)

| # | Criterion | Variant | Claim | Evidence | Verdict |
|---|-----------|---------|-------|----------|---------|
| 1 | Logical ordering | V1 | met | blocking F1, F2 before minor F3, F4; summary blocks after | MET |
| 1 | | V2 | met | coverage_check before findings; findings before notes | MET |
| 1 | | V3 | met | scope_check, then R3-1 (blocking), then minor R3-2..R3-9, then verified_adherent | MET |
| 2 | Consistent hierarchy depth | V1 | met | one level: findings list with fixed keys | MET |
| 2 | | V2 | met | one level: coverage_check map, findings list | MET |
| 2 | | V3 | met | one level: scope_check map, findings list | MET |
| 3 | Separation of concerns | V1 | met | findings / confirmed_claims / notes | MET |
| 3 | | V2 | met | coverage_check / findings / notes | MET |
| 3 | | V3 | met | scope_check / findings / verified_adherent | MET |
| 4 | Navigation aids | V1 | met | IDs R1-F1..F4; verdict comment counts findings | MET |
| 4 | | V2 | met | IDs R2-F1..F4; INF cross-refs in R2-F1 | MET |
| 4 | | V3 | met | IDs R3-1..R3-9; verdict comment names R3-1 | MET |
| 5 | Follows reviewer-card conventions | V1 | met | every finding has id, claim, evidence, class or gap, severity, recommendation | MET |
| 5 | | V2 | not met | R2-F4 is listed as a finding with `deviation_class: none` and "conformant"; verdict `pass` while a drift finding exists | NOT MET |
| 5 | | V3 | met | every finding has id, claim, evidence, class or gap, severity, recommendation | MET |

Subtotal: V1 5/5, V2 4/5, V3 5/5.

### Clarity (5 criteria)

| # | Criterion | Variant | Claim | Evidence | Verdict |
|---|-----------|---------|-------|----------|---------|
| 1 | Unambiguous language | V1 | met | hedges are conditional: "could touch ... if set in the worker env" | MET |
| 1 | | V2 | not met | R2-F4 "M1b/M1c likely UNVERIFIED", an unconditioned hedge about its own audit | NOT MET |
| 1 | | V3 | met | hedge conditional: "the Orca step can eat 25 s ..., so M1a may time out" | MET |
| 2 | Concrete over abstract | V1 | met | R1-F1 exact replacement wording | MET |
| 2 | | V2 | met | R2-F3 exact counts; R2-F1 maps each row to a plan element | MET |
| 2 | | V3 | met | R3-6 "diff = three entries + three trailing commas" | MET |
| 3 | Each section summarizable | V1 | met | each claim is one sentence | MET |
| 3 | | V2 | met | each claim is one sentence | MET |
| 3 | | V3 | met | each claim is one sentence | MET |
| 4 | Terms defined on first use | V1 | not met | "F-2", "AC", "T1/T3/T4/T5" undefined | NOT MET |
| 4 | | V2 | not met | "AC-M1", "M1b/M1c", "T5c", "T6" undefined | NOT MET |
| 4 | | V3 | not met | "AC", "M1a", "T5c", "Design 3.1" undefined | NOT MET |
| 5 | Actionable next steps | V1 | met | each finding has a concrete recommendation | MET |
| 5 | | V2 | met | decision stated: "Accept coverage as complete"; R2-F3 counting rule | MET |
| 5 | | V3 | met | each finding has a recommendation (R3-1 env -u prefix, R3-4 commands) | MET |

Subtotal: V1 4/5, V2 3/5, V3 4/5.

### Risk Coverage (5 criteria)

| # | Criterion | Variant | Claim | Evidence | Verdict |
|---|-----------|---------|-------|----------|---------|
| 1 | >= 3 risks with probability and impact | V1 | not met | severities give impact; probability only on R1-F2 ("conditional") | NOT MET |
| 1 | | V2 | not met | severities only; no probability | NOT MET |
| 1 | | V3 | not met | severities only; probability only on R3-1 (orchestrator note, not the card) | NOT MET |
| 2 | Mitigation for each risk | V1 | met | every finding has a recommendation | MET |
| 2 | | V2 | met | every finding has a recommendation | MET |
| 2 | | V3 | met | every finding has a recommendation | MET |
| 3 | Failure modes and recovery | V1 | met | R1-F2: proof touching real ~/.claude, recovery by env -u and recording | MET |
| 3 | | V2 | met | R2-F3: false-FAIL on the line cap, recovery by counting rule | MET |
| 3 | | V3 | met | R3-8: time-limit FAIL told apart by recording Orca presence and time | MET |
| 4 | External dependencies and their failures | V1 | met | upstream source pinned to evidence; notes list unverified upstream items incl. commit 96608e07 | MET |
| 4 | | V2 | not met | notes: upstream facts "taken as given"; no failure scenario | NOT MET |
| 4 | | V3 | met | R3-8 Orca on PATH consuming the shared 30 s budget (install_user_setup.py:34-35) | MET |
| 5 | Monitoring/validation mechanism | V1 | met | R1-F2 "record that the real ~/.claude/settings.json and ~/.claude/plugins/ are unchanged" | MET |
| 5 | | V2 | met | named_tests_fail_on_defect: "T5 verified to fail on unfixed code" | MET |
| 5 | | V3 | met | R3-4 run tests/docs + markdownlint; R3-1 "log that neither variable is set inside" | MET |

Subtotal: V1 4/5, V2 3/5, V3 4/5.

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant | Claim | Evidence | Verdict |
|---|-----------|---------|-------|----------|---------|
| 1 | Collection boundaries | V1 | not met | searched all findings and notes: none | NOT MET |
| 1 | | V2 | not met | searched all findings and notes: none | NOT MET |
| 1 | | V3 | met | R3-6: appending to the marketplaces object edits the prior last entry's comma (last-element boundary) | MET |
| 2 | State variables across components | V1 | met | R1-F1: live mode (readMode) vs getDefaultMode() in mode-tracker | MET |
| 2 | | V2 | not met | no state variable discussed | NOT MET |
| 2 | | V3 | met | R3-1: CLAUDE_CONFIG_DIR / XDG_CONFIG_HOME read by claude CLI, install_mcp and Ponytail | MET |
| 3 | Guard condition gaps | V1 | met | R1-F1 guard `live && live !== 'off'` / default `off` -> full; R1-F2 HOME-only isolation | MET |
| 3 | | V2 | not met | none | NOT MET |
| 3 | | V3 | met | R3-1: isolation guards HOME only | MET |
| 4 | Count divergence | V1 | met | R1-F3 4 insertions + 3 deletions vs "5 changed lines" | MET |
| 4 | | V2 | met | R2-F3 same | MET |
| 4 | | V3 | met | R3-2 same | MET |
| 5 | Interaction effects | V1 | met | R1-F2: install_mcp, claude CLI and Ponytail config all honour CLAUDE_CONFIG_DIR | MET |
| 5 | | V2 | met | every_spec_check_owned: test_install_retired_mcp.py patches install_user_setup at :522 | MET |
| 5 | | V3 | met | R3-8: Orca step and the new clone share the 30 s budget; R3-4 markdownlint --fix on installation.md | MET |

Subtotal: V1 4/5, V2 2/5, V3 5/5.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 3 | 4 | 4 |
| Correctness | 4 | 1 | 4 |
| Structure | 5 | 4 | 5 |
| Clarity | 4 | 3 | 4 |
| Risk Coverage | 4 | 3 | 4 |
| Invariant & Edge Case | 4 | 2 | 5 |
| **Total** | **24/30** | **17/30** | **26/30** |
| **qual_score** | **0.800** | **0.567** | **0.867** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>= 1/5) | Eligible as base |
|---------|-----------------------------|----------------|------------------|
| V1 | 4/5 | pass | yes |
| V2 | 2/5 | pass | yes |
| V3 | 5/5 | pass | yes |

Floor not suspended.

## Position-Bias Mitigation

Pass 1 evaluated V1, V2, V3; Pass 2 evaluated V3, V2, V1, each against the full 30-criterion rubric. Limitation: both passes were run by this one orchestrator in one context, not by independent evaluators, so the mitigation reduces order effects but does not remove anchoring.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation |
|-----------|---------|--------|--------|-----------|-------|---------------|
| Correctness 1 | V3 | MET | NOT MET | disagree | NOT MET | Pass 2 read V3 first and checked R3-5 against the debate: V3 withdrew the "reset grounded only on the off path" example (activate.js:193,55). A withdrawn false claim is a factual error. |
| Completeness 3 | V2 | MET | NOT MET | disagree | MET | Pass 2 had just read V3's explicit R3-3. Re-evaluated: V2's ownership map names a test-to-module prerequisite (test_install_retired_mcp.py patches install_user_setup:522), which meets the criterion. |
| Clarity 1 | V2 | NOT MET | MET | disagree | NOT MET | "likely UNVERIFIED" has no stated condition, unlike V1's and V3's conditional hedges. |
| Edge 5 | V2 | MET | NOT MET | disagree | MET | Pass 2 compared it with V3's richer R3-8. Re-evaluated on presence, not richness: the edited function interacting with a second test file is an interaction effect. |
| all other 86 pairs | all | | | agree | as above | |

- disagreements_found: 4 of 90
- verdicts_changed from Pass 1: 1 (V3 Correctness 1, MET to NOT MET)
- Net effect on totals: V3 -1 versus Pass 1; V1 and V2 unchanged versus Pass 1.

## Combined Scoring

`combined = 0.50 * quant + 0.50 * qual`

| Variant | quant | qual | 0.5 x quant | 0.5 x qual | Combined | Rank |
|---------|-------|------|-------------|------------|----------|------|
| V3 (opus, refactorer) | 0.925 | 0.867 | 0.4626 | 0.4333 | **0.896** | 1 |
| V1 (sonnet, analyzer) | 0.836 | 0.800 | 0.4182 | 0.4000 | **0.818** | 2 |
| V2 (glm-5.3, qa) | 0.644 | 0.567 | 0.3220 | 0.2833 | **0.605** | 3 |

- Margin top two: 0.896 - 0.818 = 0.078 (7.8 points), above the 0.05 trigger.
- Tiebreaker applied: No. For reference, level 1 (debate points won) would also pick V3: 8 points against V1's 3 and V2's 3 (debate-transcript.md scoring matrix).
- Sensitivity: V3 stays first if its DC or SC lead is removed (SC = 0.444 for V3 gives quant 0.842, combined 0.854, still ahead of V1's 0.818).

## Selected Base: Variant 3 (opus, refactorer)

### Selection rationale

V3 has the highest quantitative score (0.925: widest finding set, no internal contradictions, highest specificity) and the highest qualitative score (26/30, the only card at 5/5 on Invariant & Edge Case coverage). It won 8 of 16 contested debate points (C-002, C-003, C-004, C-008, C-009, C-010, C-011, X-002), and its classification vocabulary and line-cap counting rule were adopted unanimously. Its one major gap is that it missed the false plan claim at plan:80 (C-001, X-001), which V1 supplies. That gap is incorporated below rather than tipping the base: V1's card is narrower (4 findings, RC gaps on INF-002, 010, 014 and 017) and V1 won 3 points.

### Strengths to preserve (from V3)

1. R3-4: `tests/docs/test_retired_docs_absent.py` and `markdownlint --fix` reach `installation.md` and are owned by no task; run `uv run pytest tests/docs` and markdownlint (X-002, unanimous).
2. R3-1 content: the throwaway-HOME proof must also neutralise `XDG_CONFIG_HOME`, not only `CLAUDE_CONFIG_DIR`. Severity recalibrated to minor (both variables verified unset at 12:48Z; debate C-002). Extend per INV-016: also unset `PONYTAIL_DEFAULT_MODE`, `PONYTAIL_MAP`, `PONYTAIL_SUBAGENT_MATCHER`.
3. R3-2 counting rule: `git diff --numstat` <= 5 insertions and <= 5 deletions, all inside `install_plugins` (C-003 consensus).
4. R3-6 (expanded JSON form; prior last line gains a comma) and R3-7 (link the file or the Step 3 anchor; add no heading).
5. scope_check and verified_adherent blocks (no forbidden files, no `.claude/` staging, superseded package untouched, fill semantics at install_user_setup.py:36,150-164).
6. R3-5 narrowed: Task 3's "every claim matches the lite facts" AC cannot check claims outside the facts block; project-settings precedence (plan:81) remains unsourced. Drop the withdrawn reset example.

### Base weaknesses to correct

- R3-8: drop the "move AC-M to its own task" recommendation (X-003 won by V2; conceded); keep only "record whether Orca was on PATH and the time used".
- R3-3: keep as informational, no action.
- Verdict: `revise` stands but its blocking item changes from R3-1 to the plan:80 false claim (below).

### Strengths to incorporate from non-base variants

From V1 (sonnet, analyzer):
1. **R1-F1 as the blocking finding (C-001, X-001, 100% confidence):** plan:80 "bare `/ponytail` switches to `full`" is false under lite (`mode-tracker.js:109-119`). The docs must say bare `/ponytail` reports the level when Ponytail is on and switches on at the default level (lite) when it is off. Add INV-002: it switches to `full` only when the default is `off`.
2. **INV-001 (HIGH, unaddressed) attached to the same docs line:** "switches every session in that repo until a new session starts there" is too narrow. Any new session, `/clear` or resume in that project directory resets the shared per-project mode to the default (`hooks_claude-codex-hooks.json:5`, `hooks_ponytail-activate.js:193,55`, `runtime.js:51-66,75-78`), and each worktree has its own mode. Applied at implementation time (A-002), not by editing the plan.
3. The upstream lite-fact verification list (confirmed_claims: runtime.js, instructions.js, skill.md:50, activate.js, subagent.js, config.js, mode-tracker.js:67-77, plugin.json:15-20). It is the only coverage of INF-004 (ledger option) and INF-006 (map and subagent injection).
4. R1-F2's validation step: record that the real `~/.claude/settings.json` and `~/.claude/plugins/` are unchanged after the proof.
5. Notes: mention "stop ponytail" / "normal mode" (INV-008), and the not-verified list (band/register.tsx, project-settings precedence, commit 96608e07), carried with A-001's qualifier that the docs are "checked against v5.3.3".

From V2 (glm-5.3, qa):
1. R2-F1: the containment-unmapped matrix rows are matcher artifacts, each owned by a plan element (C-005). Include INF-001, which V2's own list omits.
2. Coverage evidence: T5 verified to fail on unfixed code (install_user_setup.py:292,303,305, fixture :232-242); T3/T4, T5c and T6 are pins that pass today by design.
3. R2-F2: the goal span "on every workspace via the installer and update scripts" is missing from the matrix but covered by the plan (plan:15,39,82).
4. R2-F4 / X-003: AC-M1 placement in Task 4 is conformant.

Not incorporated from V2: verdict `pass`, "no false claims found", `fully_adherent: 16`, `every_spec_check_owned` (all refuted or conceded), and R2-F3's 4/3 rule (withdrawn).
