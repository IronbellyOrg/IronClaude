# Base Selection Report

## Metadata

- Generated: 2026-11-04T07:43:14Z
- Pipeline step: 3 (hybrid scoring and base selection), sc-adversarial-protocol
- Variants: A = `variant-1-opus-architect.md` (opus:architect), B = `variant-2-sonnet-refactorer.md` (sonnet:refactorer), C = `variant-3-haiku-qa.md` (haiku:qa)
- Source requirements: `seed-brief.md` Success Criteria (5) and Open Questions (6), 11 in total
- Debate inputs: `debate/round1-variant-{A,B,C}.md`, `debate/round2-variant-{A,B,C}.md`; contradictions from `diff-analysis.md`; post-debate probe `invariant-probe.md`
- Line citations use `A:n`, `B:n`, `C:n` for the variant files.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (opus:architect) | Variant B (sonnet:refactorer) | Variant C (haiku:qa) |
|--------|--------|----------------------------|-------------------------------|----------------------|
| requirement_coverage (RC) | 0.30 | 1.000 (11/11) | 1.000 (11/11) | 1.000 (11/11) |
| internal_consistency (IC) | 0.25 | 0.975 (1 − 2/79) | 0.990 (1 − 1/100) | 0.937 (1 − 4/63) |
| specificity_ratio (SR) | 0.15 | 0.898 (79/88) | 0.877 (100/114) | 0.926 (63/68) |
| dependency_completeness (DC) | 0.15 | 1.000 (15/15) | 1.000 (22/22) | 0.889 (8/9) |
| section_coverage (SC) | 0.15 | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) |
| **quant_score** | | **0.9783** | **0.9791** | **0.9564** |

### Computation notes

All counts come from one deterministic script run over the three variant files (no judgment), except the two corrections marked "orchestrator rule".

- **Text units.** A "substantive line" is a non-blank line outside code fences that is not a heading and not a table separator. A: 88, B: 114, C: 68.
- **RC.** The source has no FR/NFR IDs, so section-level topic matching is used. Each of the 11 source items maps to a pattern set that must all match in the variant: SC1 `installed_plugins.json`; SC2 `false` opt-out; SC3 never-fatal (`never fatal|non-fatal|ok=True|ok is True`); SC4 `DietrichGebert/ponytail` + `test`; SC5 `CHANGELOG` + `installation.md`; OQ1 `user_settings_defaults.json`; OQ2 `PONYTAIL_DEFAULT_MODE`; OQ3 `Pragmatic` + `freshness` + `Orca|subagent`; OQ4 `30 s|budget`; OQ5 `doctor` + `install --list`; OQ6 `opt-out`. All three variants match all 11.
- **IC.** Scorable claims = substantive lines carrying a concrete indicator (a digit or a backticked name): A 79, B 100, C 63. Contradictions counted (orchestrator rule: the four CODE contradictions in `diff-analysis.md` X-003..X-006, plus the INTRA rows):
  - A: 2. X-003 (offline failure row `A:100` shows a line the code cannot print; `install_user_setup.py:303,305` append `--scope`) and X-005 ("placed last so it cannot starve the six", `A:14,71`; marketplace adds run before all installs, `install_user_setup.py:271-284`).
  - B: 1. X-005 (R4 "starves the last-listed plugin", `B:221`).
  - C: 4. X-004 (CODE + INTRA: "Behaviour today (verified)" row `C:55` against its own FR-006 `C:22`), X-006 ("first ... wins contention", `C:33,56`), X-015 (INTRA: "T7" is a unit test at `C:87` and the manual check at `C:97`), X-016 (INTRA: "CHANGELOG names the verified version" `C:98`, but `C:74` names none).
  - Not counted in IC (scored in Correctness criterion 1 instead): X-008 (B's UserPromptSubmit cell `B:108`, a CROSS row later refuted by upstream in B Round 2 #5) and X-017 (C's "`claude` is a Node app", unverifiable, not contradicted).
- **SR.** Concrete lines / substantive lines. A vague-indicator scan (`appropriate|as needed|properly|adequate|should consider|might|various|etc.|best practices|industry standard`) found 0 hits in every variant, so SR is limited only by lines without a number or named entity.
- **DC.** Internal references = occurrences of the variant's own IDs (`FR-`, `NFR-`, `R-n`/`Rn`, `T-n`/`Tn`, `AC-n`, `AC-Mn`, `V-n`) outside their defining line. All resolve textually (A 15/15, B 22/22, C 9/9). Orchestrator rule (semantic resolution): C's Risks reference "T7 manual throwaway-HOME check" (`C:97`) resolves to a unit test, not the item it names (X-015), so it counts as unresolved: C = 8/9.
- **SC.** H2 count: 12 in every variant; max 12.
- **Formula.** quant = RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15.
  - A: 0.300 + 0.2437 + 0.1347 + 0.150 + 0.150 = 0.9783
  - B: 0.300 + 0.2475 + 0.1316 + 0.150 + 0.150 = 0.9791
  - C: 0.300 + 0.2341 + 0.1390 + 0.1333 + 0.150 = 0.9564

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV protocol: each cell is a verdict with the evidence that supports it. NOT MET cells give the evidence of the failure or the sections searched.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | MET | Decision Summary answers all six open questions (`A:9-19`); success criteria mapped to FR-004, FR-006, T-1..T-4, docs (`A:30-33,141-144,121-133`); RC 11/11 | MET | Decision Summary (`B:9-19`); T1-T5 (`B:196-200`); RC 11/11 | MET | Decision Summary items 1-9 (`C:5-13`); T1-T7 (`C:81-87`); RC 11/11 |
| Addresses edge cases/failures | MET | Failure table, 6 rows incl. offline, no `claude`, budget, no `node` (`A:97-104`) | MET | Failure table, 6 rows incl. malformed settings (`B:124-131`) | MET | Failure table, 6 rows incl. non-dict `enabledPlugins` (`C:52-59`) |
| Includes dependencies/prerequisites | MET | `node` (`A:103`), `claude` CLI (`A:99`), env propagation gate V-1 (`A:91`) | MET | `claude` (`B:126`), `node` (`B:129`), env check AC-M1 (`B:210`) | MET | `claude` (`C:54`), `node` (`C:58`), real `claude` for the manual check (`C:89`) |
| Defines success/completion criteria | MET | AC-1..AC-5 (`A:149-153`) | MET | AC-1..AC-3, AC-M1..AC-M3 (`B:207-212`) | MET | "Done when: ... green; docs grep clean; CHANGELOG entry present" (`C:91`) (passes disagreed; see Position-Bias) |
| Specifies out-of-scope items | MET | 6 items (`A:167-174`) | MET | 7 items (`B:229-236`) | MET | 5 items (`C:104-110`) |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| No factual errors | NOT MET | X-003: offline row `A:100` prints a line the code cannot produce; X-005: "cannot starve the six" (`A:14,71`); A conceded both (A R1 Concessions 1-2) | NOT MET | X-008: "Re-injects the ruleset each prompt" (`B:108`), refuted by upstream `ponytail-mode-tracker.js:173-191` (B R2 #5); X-005 in R4 (`B:221`); X-012 "not an outlier" with no sizes (`B:133`) | NOT MET | X-004 (`C:55`), X-006 (`C:33,56`), X-017 unsupported "`claude` is a Node app" (`C:58`) |
| Technical approaches feasible | MET | Data-only change rides the verified call chain (`diff-analysis.md` code-check log `:89-101`) | MET | 4-line fix keeps existing assertions green (`B:92`; code-check log `:99`) | MET | Defaults edit plus label fix (`C:33-37`) |
| Terminology consistent | MET | One ID scheme (FR/NFR/T-/AC-/R-/V-1); 15/15 references resolve | MET | One ID scheme (T/AC-M/R); 22/22 references resolve | NOT MET | "T7" names two different things (`C:87` vs `C:97`, X-015) |
| No internal contradictions | MET | No INTRA row for A in `diff-analysis.md`; its contradictions are CODE (X-003, X-005) and are counted in IC | MET | No INTRA row for B | NOT MET | X-004 (INTRA with FR-006), X-015, X-016 |
| Claims supported by evidence | MET | `file:line` on every design bullet (`A:69-71`) and upstream lines in the interaction table (`A:81-84`) | MET | Real log for the defect `P2-layer2.md:358` (`B:73`); line cites throughout | MET | Line cites (`C:5-6,22,48`); some via enrichment notes (S-013), still cited |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Logical section ordering | MET | Decision → Requirements → Design → Interaction → Failure → Opt-out → Visibility → Docs → Tests → Risks → Out of Scope → Coder (12 H2) | MET | Same 12-section order | MET | Same 12-section order |
| Consistent hierarchy depth | MET | H1 + 12 H2, no orphan H3 | MET | H3 3.1-3.3 only under Design (`B:47,71,94`) | MET | H1 + 12 H2 |
| Clear separation of concerns | MET | V-1 sits in Interaction but is cross-referenced from AC-3 and R-1 (`A:151,159`) (passes disagreed; see Position-Bias) | MET | Rejected options in Design 3.3; tests in Tests; risks in Risks | MET | Design edits in Design (`C:31-39`); Failure table only flags "Change needed" |
| Navigation aids | MET | "see R-4" (`A:84`), "(R-2)" (`A:113`), "see Coder Handoff" (`A:19`) | MET | "Proves" column maps tests to FR/NFR (`B:194-201`); "See Risks R2" (`B:97`) | MET | "(FR-001)" (`C:56`), "FR-006" (`C:55,99`) |
| Follows artifact-type conventions | MET | FR/NFR IDs, AC IDs, risk IDs with probability and impact | MET | Same | NOT MET | Risks have no IDs (`C:95-102`, S-009); no AC IDs (S-008); CHANGELOG style differs from the file (S-010) |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Unambiguous language | MET | Vague-indicator scan: 0 hits | MET | 0 hits | MET | 0 hits |
| Concrete rather than abstract | MET | Exact JSON (`A:47-65`); 79/88 concrete lines | MET | Exact JSON and code shape (`B:49-63,77-90`); 100/114 | MET | Exact JSON (`C:35`); 63/68 |
| Each section has a clear purpose | MET | Every H2 summarizable in one sentence; Decision table states each position | MET | Same; Decision table plus "Why `off`" | MET | Same; numbered decisions |
| Terms defined on first use | NOT MET | "Orca", "Coder", "band" used without definition (`A:82,84,176`) | NOT MET | Defines the UNVERIFIED convention (`B:4`) but not "Orca", "Coder", "AC" (`B:21,240`) (passes disagreed; see Position-Bias) | NOT MET | "Orca", "Coder" undefined (`C:46,112`) |
| Actionable next steps | MET | V-1 pass and fail outcomes (`A:91`); Coder note (`A:178`) | MET | Three Coder questions (`B:242-246`); AC-M1..M3 | MET | "Done when" (`C:91`); Coder line (`C:114`) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| ≥3 risks with probability and impact | MET | R-1..R-7 (`A:157-165`) | MET | R1..R9 (`B:216-226`) | MET | 6 rows with Prob and Impact (`C:95-102`) |
| Mitigation for each risk | MET | Mitigation column filled for all 7 | MET | All 9 | MET | All 6 |
| Failure modes and recovery | MET | "reruns converge" (`A:102`); fallback (d) (`A:91`) | MET | "rerun resumes" (`B:128`) | MET | "rerun retries just the install" (`C:57`) |
| External dependencies | MET | Upstream change R-5, supply chain R-6 (`A:163-164`) | MET | R5 unpinned upstream, R9 mode value (`B:222,226`) | MET | Upstream drift row (`C:98`) |
| Monitoring/validation mechanism | MET | V-1 and AC-3 (`A:91,151`) | MET | AC-M1..M3 (`B:210-212`) | MET | Manual check (`C:89`); docs grep (`C:75`) |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Collection boundaries (empty, single, max) | NOT MET | No evidence found. Searched Failure Behaviour, Tests, Risks | NOT MET | T1 checks every key has `source.repo` (`B:196`), a per-element guard, not an empty/single/max case; malformed settings (`B:131`) is a parse failure (passes disagreed; see Position-Bias) | MET | Non-dict `enabledPlugins` coerced to `{}`, nothing installs, reported as "already installed" (`C:59`) |
| State interactions across components | MET | Env value beats `/ponytail default` (`A:113`); band and ledger not gated on mode (`A:84`) | MET | Env default overrides `config.json` (R1 `B:218`; Opt-out 4 `B:142`) | MET | Ledger not mode-gated (`C:48`); hook registration vs settings merge (`C:44`) |
| Guard condition gaps | MET | No `node` check (`A:103`); deleting the key is not an opt-out (`A:111`) | MET | Positional `args[3]` assumption (`B:73`) | MET | Same defect (`C:22`); non-dict coercion (`C:59`) |
| Count divergence | MET | Docs count six → seven (`A:121`); `<2 s` threshold (`A:101`) | MET | Count-free docs (`B:157`); `args[3]` index (`B:73`) | MET | `grep -rn "six plugins" docs/` (`C:75`); `args[3]` index (`C:22`) |
| Interaction effects when features combine | MET | Third SubagentStart block on every Orca worker (`A:82`, U-002) | MET | Orca workers and statusline nudge (`B:114`) | MET | Subagent tax for adversarial panels and Orca workers (`C:46`) |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 4/5 | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 | 5/5 |
| Invariant & Edge Case | 4/5 | 4/5 | 5/5 |
| **qual_score** | **27/30 = 0.900** | **27/30 = 0.900** | **26/30 = 0.867** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case | Floor (≥1/5) | Eligible as base |
|---------|-----------------------|--------------|------------------|
| A | 4/5 | Pass | Yes |
| B | 4/5 | Pass | Yes |
| C | 5/5 | Pass | Yes |

Floor not suspended.

## Position-Bias Mitigation

Pass 1 evaluated A, B, C in input order; Pass 2 evaluated C, B, A in reverse order. Of 90 criterion-variant pairs, 86 agreed. The four disagreements were re-evaluated with both passes' evidence side by side; the re-evaluation is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation reason |
|-----------|---------|--------|--------|-----------|-------|----------------------|
| Structure 3: separation of concerns | A | MET | NOT MET | DISAGREE | MET | Pass 2 (A read last, after B's separate Tests section) penalized V-1 sitting in Interaction (S-007). V-1 is still named and cross-referenced from AC-3 and R-1 (`A:151,159`); the section keeps one purpose. |
| Clarity 4: terms defined | B | MET | NOT MET | DISAGREE | NOT MET | Pass 1 credited the UNVERIFIED convention (`B:4`). The criterion needs domain terms defined; "Orca", "Coder" and "AC" are not (`B:21,240`). |
| Invariant 1: collection boundaries | B | MET | NOT MET | DISAGREE | NOT MET | Pass 1 read T1's all-keys check (`B:196`) as a boundary case. It guards each element, not empty, single or maximum collections. |
| Completeness 4: success criteria | C | NOT MET | MET | DISAGREE | MET | Pass 1 (C read after A's and B's ID'd ACs) penalized missing AC IDs. The criterion asks for defined completion criteria; `C:91` defines them. The missing IDs are scored under Structure 5. |

- Disagreements re-evaluated: 4
- Final verdict differs from Pass 1: 3 (B twice, C once). Final verdict differs from Pass 2: 1 (A Structure 3).
- Effect on the ranking: none. Under either pass alone A and B are level on qualitative points.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (Level 1) |
|---------|---------------|--------------|-----------------|-----------------------------|
| A (opus:architect) | 0.4892 | 0.4500 | **0.9392** | 0.5 of 9 points (5.6%) |
| B (sonnet:refactorer) | 0.4895 | 0.4500 | **0.9395** | 6 of 9 points (66.7%) |
| C (haiku:qa) | 0.4782 | 0.4333 | **0.9115** | 1.5 of 9 points (16.7%) |

**Margin**: B − A = 0.0004 (0.04 percentage points), below the 5% threshold. B − C = 0.0280.
**Tiebreaker applied**: Yes, Level 1 (debate performance). Level 1 is decisive (66.7% against 5.6%), so Levels 2 and 3 are not reached.

### Debate points (Level 1)

No consolidated `debate-transcript.md` scoring matrix exists for this run, so points come from the Round 2 "Final Positions" tables. A point counts only where all three advocates name the same preferred variant; a merged preference splits the point.

| Diff point | Round 2 consensus | A | B | C |
|------------|-------------------|---|---|---|
| C-002 / X-001 order | B: append last, no budget rationale, no order test | 0 | 1 | 0 |
| C-005 / X-002 / X-003 label fix | B's 4-line shape (+ C's test assertions) | 0 | 1 | 0 |
| X-005 budget ordering | none: correct the text in all three | — | — | — |
| C-012 / X-009 env check | B's AC-M1 split + A's pass/fail wording | 0.5 | 0.5 | 0 |
| C-013 / X-007 fallback | C: documented user step, no installer write | 0 | 0 | 1 |
| C-008 docs count | B (+ C's grep) | 0 | 1 | 0 |
| C-016 Coder handoff | B + C | 0 | 0.5 | 0.5 |
| C-021 migration note | B | 0 | 1 | 0 |
| U-006 existing-user test | B (as an extension of the existing test) | 0 | 1 | 0 |
| **Total (9 points, 8 decided)** | | **0.5** | **6** | **1.5** |

Sources: `round2-variant-A.md:45-55`, `round2-variant-B.md:45-55`, `round2-variant-C.md:43-53`.

## Selected Base: Variant B (sonnet:refactorer)

### Selection Rationale

- B has the highest combined score (0.9395) and the highest IC (0.990). Of the four CODE contradictions, only X-005 touches B, and B conceded and corrected it in Round 2 (#1).
- A and B tie on qualitative points (27/30) and differ by 0.0004 overall, so the protocol's Level 1 tiebreaker decides. B wins 6 of 9 debate points. In Round 2 all three advocates named B the base for every code-facing decision (`round2-variant-A.md:27`, `round2-variant-B.md:31`, `round2-variant-C.md:28`).
- B's design is the one the code supports. It alone found and proved the `--scope` label defect with a real log (`B:73`; `P2-layer2.md:358,624`), and A withdrew its own "zero Python" rule (X-002) in Round 2 (R-2).
- C scored highest on Invariant & Edge Case (5/5) but lost on Correctness (3/5) and Structure (4/5). In Round 2 it conceded its "first" order, its `(label, argv)` restructure and its Ponytail-keyed test legs (#1, #5, #6).

### Strengths to Preserve from Base

1. Defaults-file-only design with the 4-line label fix (FR-005, Design 3.2, `B:31,71-92`) and the real-log evidence for both failure paths (`B:73`; B R2 N1).
2. T1 invariant: every `enabledPlugins` marketplace has a `source.repo` (`B:196`).
3. T2 install assertions: `["plugin","marketplace","add","DietrichGebert/ponytail"]` in calls and `ponytail@ponytail` in installs (`B:197`).
4. Existing-user proof with an idempotent second run (T4, `B:199`).
5. Count-free docs wording (`B:157-163`).
6. CHANGELOG Added + Fixed + migration sentence (`B:178-188`).
7. Diff-scope AC-2 with a 5-line Python cap and an allowed-files list (`B:208`); AC-3 primitive-path grep (`B:209`).
8. Visibility reasoning: `update.sh:10` runs `doctor`, so a plugin check there would gate updates (`B:151`).
9. Coder confirmation questions (`B:242-244`) and the unknown-mode-falls-to-`full` risk R9 (`B:226`).

### Strengths to Incorporate from Non-Base Variants

1. From A, Round 2 R-2: the replacement rule "a default plugin is added by data only; code changes only for defects on the shared plugin path, each pinned by a test".
2. From A, Decision Summary (`A:21`): the lettered rejected-alternatives record (a)-(d).
3. From A, Interaction table (`A:82`, U-002): the per-subagent count (IronClaude already injects two SubagentStart blocks, `hooks.json:110-128`).
4. From A, V-1 (`A:91`): explicit pass and fail wording for the env check.
5. From A, docs paragraph (`A:111,123`) and Round 2 N7: deleting the key is not an opt-out; opt out in USER settings because project settings win.
6. From A, Failure Behaviour (`A:103-104`): `node` grounded in `install_hooks.py:66-68`; the enabled-but-not-installed row.
7. From A, Interaction (`A:83`): the correct UserPromptSubmit reading (re-injection is Qoder-only), confirmed by B R2 #5.
8. From C, Round 2 N1: the `claude`-absent test leg with the exact tuple.
9. From C, Round 2 #8 and N2: T5 asserts `--scope` absent on both failure paths, with a named fixture.
10. From C, Docs (`C:75`): `grep -rn "six plugins" docs/` returns nothing.
11. From C, Coder Handoff (`C:114`): confirm the template installs the fork's current version, not a pinned older one.
12. From C, Round 2 N4: the M1a second-run check asserts the exact "already installed" line, because a key mismatch hides behind a success line.
13. From C, Docs (`C:73`) and Round 2 #3: ledger caveat in the docs; CHANGELOG names the verified upstream version.
