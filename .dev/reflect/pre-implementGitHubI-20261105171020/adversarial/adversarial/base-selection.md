# Base Selection Report

- Variants: A = `variant-1-original.md` (reviewer 1, analyzer, sonnet class); B = `variant-2-original.md` (reviewer 2, qa, haiku class)
- Artifact type: sc:reflect UC-1 reviewer card (YAML) for the plan `TASK-WF-implementGitHubI-20261105-170815.md` (PLAN)
- Inputs: both variants, `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`; protocol `sc-adversarial-protocol/refs/scoring-protocol.md`

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (reviewer 1, sonnet) | Variant B (reviewer 2, haiku) |
|--------|--------|-------------------|-------------------|
| requirement_coverage (RC) | 0.30 | 0.5000 (5 of 10 review surfaces) | 0.6000 (6 of 10 review surfaces) |
| internal_consistency (IC) | 0.25 | 0.9545 (1 contradiction / 22 scorable claims) | 0.9355 (2 contradictions / 31 scorable claims) |
| specificity_ratio (SR) | 0.15 | 0.8696 (40 concrete / 46 substantive sentences) | 0.9487 (37 concrete / 39 substantive sentences) |
| dependency_completeness (DC) | 0.15 | 1.0000 (0 internal references; vacuous) | 1.0000 (0 internal references; vacuous) |
| section_coverage (SC) | 0.15 | 1.0000 (5 top-level keys / 5) | 1.0000 (5 top-level keys / 5) |
| **quant_score** | | **0.8191** | **0.8562** |

Formula: `quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC`.
A: 0.1500 + 0.2386 + 0.1304 + 0.1500 + 0.1500 = 0.8191. B: 0.1800 + 0.2339 + 0.1423 + 0.1500 + 0.1500 = 0.8562.

### RC detail: review surfaces of the plan (Constraints plus Tasks 1 to 9)

The plan has no requirement IDs, so the surfaces are the source requirements. A variant covers a surface when one of its findings is anchored to it (`plan_ref`) or clearly addresses its text.

| Surface | Variant A | Variant B |
|---|---|---|
| Constraints | covered: A-F2 recommends "State in Constraints that the check runs on every invocation" (addresses PLAN:22) | covered: B-F3 `plan_ref: Constraints` (PLAN:22); B-F7 also anchored there |
| Task 1 | not covered (A-F3 mentions Task 1 only as a comparison: "Task 1 guards against this in its own file") | covered: B-F2 `plan_ref: Task 1` (PLAN:36, 39) |
| Task 2 | not covered | not covered |
| Task 3 | covered: A-F3 | covered: B-F5, B-F6 |
| Task 4 | covered: A-F2 `plan_ref: Task 4` | covered: B-F3 "Task 4 replaces the assignment at ccsession:124, which is top-level and executes before the argument dispatch" |
| Task 5 | covered: A-F1 | covered: B-F1 |
| Task 6 | not covered | not covered (B-F4 cites the README row PLAN:111 only as a place the claim is repeated; it asserts no defect in Task 6 and asks for no Task 6 change) |
| Task 7 | not covered | not covered (same reasoning; PLAN:121 is not cited for a defect) |
| Task 8 | covered: A-F4 | not covered |
| Task 9 | not covered | covered: B-F4 `plan_ref: Task 9` (PLAN:148) |
| **Total** | **5 / 10** | **6 / 10** |

### IC detail

Scorable claims were counted as the distinct falsifiable statements in each finding's `claim` (A: F1 7, F2 7, F3 5, F4 3 = 22; B: F1 7, F2 4, F3 5, F4 3, F5 4, F6 5, F7 3 = 31). A contradiction is a claim and its own label or remedy asserting opposite things about the same subject.

- A, 1: A-F2 says "The plan does not say whether that is intended" yet labels the finding "Necessary deviation", which by `sc-reflect-protocol/SKILL.md:987` asserts a documented, forced rationale.
- B, 2: B-F7 is labelled Drift (a departure the plan made) while its own remedy says "No plan change needed"; B-F2 is labelled Drift, which `SKILL.md:1009` defines as NOT contradicting an acceptance criterion, while its claim is that the plan's own criterion (PLAN:39) cannot be met.
- Not counted as internal contradictions (they are external factual errors, scored under Correctness): A's "sourced (line 846)" and A-F3's aside about Task 1.

### SR detail

Computed by a script over each card's `claim`, `recommended_change` and `not_checked` text (evidence lists, keys and the calibration block excluded; sentences of 4 or more words). A sentence is concrete when it holds a number, a code token, a flag, an ALL_CAPS variable name, a file name, `Task N` or `PLAN:`. Non-concrete sentences: A 6 (for example "The user-visible messages are misleading, though."; "Optionally note the orca message wording as a known cosmetic effect."); B 2 (for example "A user with a typo'd exported value breaks tab-title cleanup and name listing, behavior unrelated to permission flags.").

### DC and SC detail

- DC: neither card has an internal cross-reference (finding to finding or section to section). Every reference is to an external file (`ccsession:1652`, `PLAN:39`) or an external artifact ("Tier 1 risk R1"), which the protocol excludes. With 0 internal references there is nothing unresolved, so both score 1.0; the metric does not separate the variants here.
- SC: the cards are YAML with no H2 headings, so the top-level keys stand in for sections: `verdict`, `self_confidence`, `findings`, `not_checked`, `calibration` (the calibration block was attached by the orchestrator to both). 5 / 5 each.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Reading of the rubric for this artifact type: the "source input" of a reviewer card is its brief (`reviewer-briefs/reviewer-1.md:20-24` for A, `reviewer-briefs/reviewer-2.md:23-29` for B) and the plan it reviews. Each verdict follows Claim / Evidence / Verdict; a MET verdict without a quoted or cited piece of the variant defaults to NOT MET. Pass 1 evaluated A then B. Pass 2 (next section) evaluated B then A from the variant text again, without consulting the pass 1 verdicts.

### Pass 1 (order A, B)

#### Completeness

| Criterion | A | A: Claim / Evidence | B | B: Claim / Evidence |
|---|---|---|---|---|
| 1. Covers all explicit requirements of the source input | NOT MET | C: A's brief asks for "a task that cannot achieve its acceptance criteria as worded" and "a hidden launch path that still adds the bypass" (`reviewer-1.md:20`). E: A has no finding on Task 1's criterion (U-004, conceded A R2 crit 1), and no finding and no not_checked line on caller-passed bypass flags (probe INV-016: Orca's default `--dangerously-skip-permissions` reaches Claude through `"$@"`, `ccsession-orca:14-17, 247, 249`). | MET | C: B's brief lists five defect families plus a matrix audit (`reviewer-2.md:23, 25`). E: unobservable or wrong-reason criterion and old-launcher pass: F2 ("the CC_CLAUDE_FLAGS=--verbose + CCSESSION_PERMISSIONS=default test ... PASSES on old code"); unbacked doc claim: F4; missing case and isolation: F3 ("The plan's only bad-value test uses `ccsession demo`"), F5, F6; matrix audit: F7 ("No requirement-bearing span of source.md is absent from the matrix"). |
| 2. Addresses edge cases and failure scenarios | MET | E: A-F1 "(a) If Task 5 rewrites that line ... `--help` dumps the whole launcher. (b) If the new paragraph stays at or below the old sentinel position ... the Task 5 criterion fails." | MET | E: B-F1 gives the same two outcomes; B-F3 "CCSESSION_PERMISSIONS=typo makes every subcommand exit 2". |
| 3. Includes dependencies and prerequisites | MET | E: A-F2 "It also reaches `ccsession-orca`, which calls `ccsession --check-name`, `--ask` and `--auto-name`." | MET | E: B-F4 ties Task 9's acceptance to Tasks 1-3 ("every behavior in the bullet matching the tests of Tasks 1 to 3"); B-F6 ties Task 3 to Task 1's isolation criterion. |
| 4. Defines success / completion criteria | MET | E: verdict `FAIL`; A-F1 "Add a test that `--help` contains `CCSESSION_PERMISSIONS=default` and does not contain `set -e` or `CLAUDE_BIN=`." | MET | E: verdict `FAIL`; B-F2 supplies the replacement criterion text ("every test that asserts the new default-flag behavior or the bad-value error fails; ..."). |
| 5. Specifies what is out of scope | MET | E: `not_checked` lists 6 items, e.g. "The `.claude/` and `plugins/` mirrors of the ccsession files (the glob skipped them)." | MET | E: `not_checked` lists 5 items, e.g. "IronbellyOrg/Coder#458 (other repository) was not checked". |
| **Subtotal** | **4/5** | | **5/5** | |

#### Correctness

| Criterion | A | A: Claim / Evidence | B | B: Claim / Evidence |
|---|---|---|---|---|
| 1. No factual errors or hallucinated claims | NOT MET | E: A-F2 "before the `.env` file is sourced (line 846)"; `ccsession:846` only assigns `CCSESSION_ENV_FILE`, sourcing is `:847-849` (orchestrator re-read; A's calibrator and A R1 concession agree). A-F3 "it removes `CC_CLAUDE_FLAGS` and adds it to the excluded names" is loose: the tuple already holds it (diff-analysis C-004, A R1 concession). | MET | E: every B evidence line resolves to the stated content (diff-analysis marks C-001, C-003, C-004, C-005, U-004, U-005, U-008 VERIFIED). The two PARTIAL items are of degree, not fact: F5's risk is low but its facts hold (`test_ccsession_tiers.py:445, 500` do pass the flag); F3's "breaks tab-title cleanup" is a silent loss of function, which A R2 N4 showed is reachable. |
| 2. Technical approaches feasible with stated constraints | MET | E: A-F1 remedy "Add the `CCSESSION_PERMISSIONS=default ccsession <topic>` usage entry in the usage block before line 109 ... Either keep the line starting `# The wrapper always runs` as the awk sentinel, or change the sentinel ... together"; both advocates confirm it is the remedy that satisfies PLAN:100 (C-001, R2). | NOT MET | E: B-F1's primary remedy "update the awk stop-marker in show_help() (ccsession:1652) to match the rewritten sentence" leaves the new paragraph below the stop line, so PLAN:100's positive assertion still fails; B conceded (B R2 #8). |
| 3. Terminology used consistently and accurately | NOT MET | E: A-F2 `class: Necessary deviation` for a scope the plan never justifies; fails `SKILL.md:987`; conceded (A R2 crit 3). | NOT MET | E: B-F2 and B-F7 `class: Drift` misfit (`SKILL.md:1009`; F7 "No plan change needed"); conceded (B R2 #2, #3). |
| 4. No internal contradictions | NOT MET | E: IC count 1 (A-F2 claim vs label). | NOT MET | E: IC count 2 (B-F2, B-F7 claim vs label). |
| 5. Claims supported by evidence | MET | E: every finding carries an `evidence` list of file:line citations (F1 5, F2 5, F3 2, F4 2). | MET | E: every finding carries an `evidence` list (36 citations, including `PLAN:` lines). |
| **Subtotal** | **2/5** | | **2/5** | |

#### Structure

| Criterion | A | A: Claim / Evidence | B | B: Claim / Evidence |
|---|---|---|---|---|
| 1. Logical ordering | MET | E: blocking F1 first, then three `minor` findings. | MET | E: blocking F1 and F2 first, then five `minor`. |
| 2. Consistent hierarchy depth | MET | E: every finding has the same seven keys at the same depth. | MET | E: same seven keys on all seven findings. |
| 3. Clear separation of concerns | MET | E: one defect per finding (help sentinel; check scope; fixture leak; D08 clause). | MET | E: one concern per finding; F5 (control ambiguity) and F6 (env leak) split two Task 3 issues; F7 is the matrix audit the brief asked to report "as a finding" (`reviewer-2.md:23`) and is self-labelled "No plan change needed". |
| 4. Navigation aids | MET | E: finding ids F1-F4 and `plan_ref: Task N` cross-reference the plan. | MET | E: ids F1-F7, `plan_ref`, and `PLAN:<line>` citations. |
| 5. Follows artifact-type conventions | MET | E: `verdict`, `self_confidence`, `findings[id, claim, evidence, class, severity, plan_ref, recommended_change]`, `not_checked` as required by `reviewer-1.md:24`. | MET | E: same schema as required by `reviewer-2.md:29`. |
| **Subtotal** | **5/5** | | **5/5** | |

#### Clarity

| Criterion | A | A: Claim / Evidence | B | B: Claim / Evidence |
|---|---|---|---|---|
| 1. Unambiguous language | MET | E: none of the rubric's hedges ("should consider", "might", "as appropriate") occurs; one "Optionally" marks an explicitly optional add-on. | MET | E: no hedge term occurs (SR script found 0 vague terms). |
| 2. Concrete rather than abstract | MET | E: SR 0.87; e.g. "next to the line-96 entry". | MET | E: SR 0.95; e.g. "Name the exact control invocation in Task 3 (for example _launch(tmp_path, "work", "--tier", "tier0"))". |
| 3. Each section has a clear purpose | MET | E: each claim opens with a one-sentence thesis, e.g. "Task 5 cannot meet its acceptance criteria and, as worded, would break `ccsession --help`." | MET | E: e.g. "Task 1's red-log acceptance criterion is unsatisfiable as written". |
| 4. Acronyms and domain terms defined on first use | NOT MET | E: "(this is Tier 1 risk R1)" in A-F2 is never defined. | NOT MET | E: B-F7 uses "INF-004", "INF-007" and "unmapped_requirements_union" without defining them. |
| 5. Actionable next steps | MET | E: every finding has a `recommended_change`. | MET | E: every finding has a `recommended_change` (F7's is a coverage-slice action). |
| **Subtotal** | **4/5** | | **4/5** | |

#### Risk Coverage

| Criterion | A | A: Claim / Evidence | B | B: Claim / Evidence |
|---|---|---|---|---|
| 1. At least 3 risks with probability AND impact | NOT MET | E: `severity` gives impact on all four findings; no finding states a probability (searched all claims and not_checked). | NOT MET | E: impact on all seven; one probability statement only ("the F6 exposure is latent, not observed", not_checked), fewer than 3. |
| 2. Mitigation for each risk | MET | E: 4 of 4 findings carry `recommended_change`. | MET | E: 7 of 7. |
| 3. Failure modes and recovery | MET | E: A-F1 failure modes (a) and (b), recovery "keep the line ... or change the sentinel ... together". | MET | E: B-F1 failure modes plus recovery "update the awk stop-marker ... or move the permissions documentation above the marker" (feasibility scored separately under Correctness 2). |
| 4. External dependencies and their failure scenarios | MET | E: A-F3 "A developer or CI shell with `CC_CLAUDE_FLAGS` set therefore fails the control assertion." | MET | E: B-F6 "true only when the developer's shell does not export CC_CLAUDE_FLAGS"; B-F3 hook-run subcommands. |
| 5. Monitoring / validation mechanism | MET | E: A-F1 guard test; A-F2 "add one test that a bad value makes `ccsession --help` exit 2". | MET | E: B-F1 guard assertion; B-F3 "add one test (bad value + `ccsession --list` exits 2)"; B-F4 env-file test. |
| **Subtotal** | **4/5** | | **4/5** | |

#### Invariant and Edge Case Coverage

| Criterion | A | A: Claim / Evidence | B | B: Claim / Evidence |
|---|---|---|---|---|
| 1. Boundary conditions (empty, single, maximum) | MET | E: A-F3 "pass `CC_CLAUDE_FLAGS=""` explicitly (an empty value takes the default)"; not_checked "The correctness of the `case`/`:-` expansion itself ... I saw no defect in it". | MET | E: B-F2 analyses the empty-`CC_CLAUDE_FLAGS` + `default` and empty + unset tests against `ccsession:124`. |
| 2. State variables across component boundaries | MET | E: A-F2 exit status crossing into `ccsession-orca` ("a valid CCSESSION_NAME is dropped"); A-F3 environment copied by `_launch_env`. | MET | E: B-F6 `os.environ.copy()` at `tiers:362`; B-F3 hook-run subcommands. |
| 3. Guard condition gaps | MET | E: A-F1 "The existing help tests use `in` checks, so they would still pass and hide the breakage." | MET | E: B-F1 "No automated test catches the broken-marker variant: every help test is substring-based". |
| 4. Count divergence / inclusive-exclusive ranges | MET | E: A-F1 "Only the usage block above the sentinel (lines 2-108 ...) reaches `--help` output" (awk prints from line 2 and stops before the sentinel line). | MET | E: B-F1 "'always' occurs only on line 109 of that paragraph"; "appending the new paragraph after line 114 means the paragraph is after the stop-marker". |
| 5. Interaction effects when features combine | MET | E: A-F3 `CC_CLAUDE_FLAGS` from the shell combined with the new variable in the Task 3 control run. | MET | E: B-F2 `CC_CLAUDE_FLAGS=--verbose` combined with `CCSESSION_PERMISSIONS=default` on the old launcher. |
| **Subtotal** | **5/5** | | **5/5** | |

### Pass 2 (order B, A; independent re-read, stricter reading of borderline criteria)

| Dimension / criterion | B pass 2 | B note | A pass 2 | A note |
|---|---|---|---|---|
| Completeness 1 | MET | Each brief family has a finding (F2, F4, F3/F5/F6, F7) | NOT MET | No Task 1 criterion finding; no hidden-bypass-path finding |
| Completeness 2 | MET | F1 outcomes; F3 typo | MET | F1 (a)/(b) |
| Completeness 3 | MET | F4 Task 9 to Tasks 1-3 | MET | F2 orca callers |
| Completeness 4 | MET | F2 replacement criterion | MET | F1 guard test spec |
| Completeness 5 | MET | 5 not_checked items | MET | 6 not_checked items |
| Correctness 1 | NOT MET | Stricter reading: F3's "breaks tab-title cleanup and name listing" was judged overstated in diff-analysis X-001 | NOT MET | "sourced (line 846)" |
| Correctness 2 | NOT MET | F1 primary remedy leaves PLAN:100 failing | MET | F1 remedy satisfies PLAN:100 |
| Correctness 3 | NOT MET | F2, F7 labels | NOT MET | F2 label |
| Correctness 4 | NOT MET | IC 2 | NOT MET | IC 1 |
| Correctness 5 | MET | 36 citations | MET | 14 citations |
| Structure 1 | MET | blocking first | MET | blocking first |
| Structure 2 | MET | uniform keys | MET | uniform keys |
| Structure 3 | NOT MET | Stricter reading: F7 is a coverage-matrix concern filed in the plan-defect list with `plan_ref: Constraints` | MET | one defect per finding |
| Structure 4 | MET | ids, plan_ref, PLAN lines | MET | ids, plan_ref |
| Structure 5 | MET | brief schema | MET | brief schema |
| Clarity 1 | MET | no hedges | NOT MET | Stricter reading: "Optionally note the orca message wording" and "Or run the check only where a launch is about to happen" leave the fix open |
| Clarity 2 | MET | SR 0.95 | MET | SR 0.87 |
| Clarity 3 | MET | thesis sentences | MET | thesis sentences |
| Clarity 4 | NOT MET | INF-004 etc. undefined | NOT MET | "Tier 1 risk R1" undefined |
| Clarity 5 | MET | recommended_change on all | MET | recommended_change on all |
| Risk 1 | NOT MET | 1 probability statement | NOT MET | none |
| Risk 2 | MET | 7/7 | MET | 4/4 |
| Risk 3 | MET | F1 | MET | F1 |
| Risk 4 | MET | F6 shell, F3 hooks | MET | F3 shell |
| Risk 5 | MET | guard, tests | MET | guard, tests |
| Edge 1 | MET | F2 empty-flag analysis | NOT MET | Stricter reading: A never analyses an empty-value defect; the `""` value appears only inside a remedy |
| Edge 2 | MET | F6, F3 | MET | F2, F3 |
| Edge 3 | MET | F1 substring tests | MET | F1 `in` checks |
| Edge 4 | MET | "always" only on line 109 | MET | lines 2-108 |
| Edge 5 | MET | F2 verbose + default | MET | F3 shell flags + variable |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (re-evaluation) |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 1 | B | MET | NOT MET | DISAGREE | MET. Pass 2 relied on the diff-analysis label "overstated", which predates A R2 N4. With a bad exported value, `hooks/session-name.sh:196-212` runs `--sync-name` and the tab calls in any session with the hook, and they exit 2 silently, so tab-title cleanup does not happen; `--list` exits 2. "breaks" is imprecise about visibility (corrected in Step 4) but is not a false fact. |
| Structure 3 | B | MET | NOT MET | DISAGREE | MET. `reviewer-2.md:23` instructs B to report the matrix audit "as a finding"; F7 is a separate finding and states "No plan change needed", so the concern is separated, not mixed. Its placement in a merged plan-defect card is handled in Step 4. |
| Clarity 1 | A | MET | NOT MET | DISAGREE | MET. The criterion names "should consider", "might", "as appropriate"; none occurs. "Optionally" and "Or" offer explicit alternatives, each concrete. |
| Edge 1 | A | MET | NOT MET | DISAGREE | MET. A's not_checked line "The correctness of the `case`/`:-` expansion itself ... I saw no defect in it" shows A examined the empty / unset expansion boundary and reported a result, and A-F3 states the empty-value rule correctly. |

Disagreements re-evaluated: 4. Final verdicts changed from pass 1: 0. The other 56 criterion-variant pairs agreed across passes.

## Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 2/5 | 2/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant and Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **24/30 = 0.8000** | **25/30 = 0.8333** |

## Edge-Case Floor Check

| Variant | Invariant and Edge Case score | Floor (>= 1/5) | Eligible as base |
|---|---|---|---|
| A | 5/5 | met | yes |
| B | 5/5 | met | yes |

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (reviewer 1, analyzer, sonnet) | 0.4095 | 0.4000 | **0.8095** | won 2 of 16 S/C/X points (12.5%) |
| B (reviewer 2, qa, haiku) | 0.4281 | 0.4167 | **0.8448** | won 8 of 16 S/C/X points (50.0%) |

**Margin**: 0.0353 absolute (4.2% relative to B), below the 0.05 threshold.
**Tiebreaker applied**: Yes, step 1 (debate performance). Diff-point wins from the Scoring Matrix of `debate-transcript.md`: A won C-001 and C-002; B won S-001, S-002, S-004, S-006, S-007, X-002, C-004 and C-005; ties on S-003, S-005, S-008, X-001, C-003 and C-006. A-points have no winner (shared assumptions) and are excluded. Counting the agreed U-points as well gives A 5 (adds U-001, U-002, U-003) and B 11 (adds U-004, U-005, U-008); B leads either way. Step 2 was not needed.

## Selected Base: Variant B (reviewer 2, qa persona, haiku class)

### Selection Rationale

B has the higher combined score (0.8448 vs 0.8095) and, because the margin is under 0.05, also wins the tiebreaker on debate performance (8 to 2 diff-point wins). The decisive evidence is coverage: B is the only card with the executor-blocking Task 1 criterion defect (U-004, PLAN:36 vs PLAN:39 vs `ccsession:124`, conceded by A in both rounds) and the untested env-file clause behind Task 9's acceptance (U-005, PLAN:148), and it covers 6 of 10 plan surfaces to A's 5. B's citations into plan lines (`PLAN:<line>`) give the merged card the anchors a plan editor needs. B's weaknesses are specific and fixable from A: the infeasible primary remedy for Task 5 (Correctness 2), two misapplied class labels, the guard-test token, and the overstated impact wording in F3. Both cards lose Correctness 3 and 4 on labels, so the base choice does not buy classification quality; Step 4 corrects labels on both sides.

The A advocate's position that A is the better base is recorded (A R1 recommendation, A R2 unresolved item 5). It rests on per-finding precision (C-001, C-002, U-002, U-003), which Step 4 carries into the base in full; it does not offset A's missing Task 1 and Task 9 coverage.

### Strengths to Preserve from Base (B)

1. B-F2: the Task 1 red-log criterion defect with its replacement wording (blocking).
2. B-F4: the env-file clause that PLAN:148 requires to be test-backed, with the cheap test (`_label_launch` already sets `CCSESSION_ENV_FILE`, `test_ccsession_tag.py:1182`).
3. B-F1's evidence base: "always" only on line 109 of the paragraph, and the full inventory of substring-only help tests (`test_ccsession_tag.py:157-169, 2315-2323`; `test_ccsession_tiers.py:576-582`; `test_install_ccsession.py:224-238`).
4. B-F3's wider subcommand reach (`--rm`, the hook-run subcommands) and B-F6's link to PLAN:40.
5. `PLAN:<line>` anchoring on every finding, and the method disclosure in not_checked ("No command was run").

### Strengths to Incorporate from Non-Base Variant (A)

1. A-F1 remedy (C-001, R2 both A): the usage entry next to `ccsession:96-97` above the sentinel; keep the `# The wrapper always runs` prefix or change `ccsession:1652` in the same edit; rewrite the PLAN:100 wording (U-003).
2. A-F1 guard tokens (C-002, R2 both A): `--help` contains `CCSESSION_PERMISSIONS=default` and contains neither `set -e` nor `CLAUDE_BIN=`.
3. A-F2's `ccsession-orca` trace (U-001): valid `CCSESSION_NAME` dropped with "not a valid session name; ignoring it" (`ccsession-orca:132-137`), "the session-name question failed (status 2)" (`:204-212`), no bypass leak (`:247, 249`).
4. A-F4 (U-002): D08 line 23's "Claude Code then runs tools without asking" becomes false for an opted-in launch.
5. A-F3 (C-004): the alternative fix of passing `CC_CLAUDE_FLAGS=""` explicitly, merged into B-F6.
