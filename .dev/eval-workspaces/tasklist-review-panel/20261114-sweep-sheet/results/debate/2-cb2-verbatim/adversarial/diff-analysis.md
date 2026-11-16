# Diff Analysis: CB-2 reword decision (DD-7 / 15.1 row 3), three position papers

Orchestrator: the main Sonnet session (no Opus). Variants: V1 = `variant-1-haiku-defender.md`, V2 = `variant-2-sonnet-prosecutor.md`, V3 = `variant-3-sonnet-architect.md`.
Paths: SW, RL, MR as defined in `work/evidence-pack.md`.

## Metadata
- Generated: 2026-11-15
- Variants compared: 3
- Categories: structural (1), content (9), contradictions (3), unique (4), shared assumptions (5)
- Taxonomy level in the last column of each table: L1 surface (wording, format), L2 structural (what changes where), L3 state mechanics (guards, rules, what the measure can and cannot see)

## Corrections to the evidence pack (found by the orchestrator while reading the position papers; every advocate gets them in Round 1)
- CORR-1. `SW/config/freeze.json` does not exist: `ls SW/config` shows `packages.json`, `panels.json`, `values.json`. The freeze (`bin/freeze.sh`, plan step 14) has not been run, so no brief hash is frozen yet and no run exists. Before the freeze a reword needs no re-run.
- CORR-2. The pack (F8) said Z0 and K are "one shared control" with RL. RL `DESIGN.md` DR-12 (line 87) says each build runs its OWN same-block Z0 and K, that the copied brief parts make the Z0 and K briefs byte-identical in both builds, and that a combined schedule "can therefore pool the control arms later" (owner choice: one combined schedule saves 132 panel runs, 458 against 326, or two separate ones). RL line 184: `briefs/` is Tier A, "Copy byte for byte with `cp`. Never edit the copy." So the control is shared in TEXT, run twice, with pooling still open.
- CORR-3. `ledger_headings` is called only by `render_report` (`SW/analysis/analyze.py` lines 1294, 1010; grep of `analysis/` and `bin/`): no gate D1 to D7 or G0 reads it.
- CORR-4. DESIGN 14.2 (line 774): the timing spike already runs 5 luna runs with the Z0 brief on one document (plus 5 SS runs). Those are real-model Z0 reports that carry the CB-2 clause and exist before any decision run.

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Paper form | evidence list, no options table | evidence list plus a replacement text | options table a to e plus the recommendation | Low | L1 |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Is the default (verbatim plus the heading count) blocking? | NO | YES, but "if the verdict rule needs proof of a biased result, my answer is NO" | NO; if the panel reads "owner decision above 0, no action named" as an unregistered consequence, option (d) is the smallest fix | High | L2 |
| C-002 | Does the heading count need a registered rule and consequence to be a complete measure? | No: disclosed uncertainty | Yes (BD-1): the count has no link to any action, the same defect type as the act-band debate | Yes in text (option d), but not required for PASS | High | L3 |
| C-003 | Change `briefs/cb2.txt` now? | No | No (contingent reword only if a pilot shows a heading) | No | Medium | L2 |
| C-004 | A real-model look before the freeze | none | new 5 Z0 + 5 K panel runs on HO-6 | read the Z0 reports of the existing timing spike (5 luna runs, CORR-4) for the word "ledger" | Medium | L2 |
| C-005 | What the measure counts | exact `## Ledger` line (conceded narrow) | "any ledger-like heading or table" in the pilot | heading starting "ledger" or "defect ledger", any level and case, or a `ledger-v1` block; plus the exact upper bound | Medium | L3 |
| C-006 | Size of the harm | small, qualitative, UNVERIFIED | probability that the clause moves a gate: guess under 10%; asymmetry: nobody could tell | 0.001 to 0.003 on K's mean found fraction at 2% to 5% affected reports, assuming a 0.05 loss per affected report (guess) | Medium | L2 |
| C-007 | Direction of any bias | either direction | UNVERIFIED | favours SS (a damaged control flatters the treatment) | Medium | L2 |
| C-008 | Cost of rewording | test exception, freeze, `copy-briefs.py`, RL coordination | REQ-05 waiver, new SS-only part, 4+ tests, RL must follow | table: (b) breaks REQ-05 and needs an RL copy; (c) breaks REQ-05 for Z0 and K and RL's "starts with the Z0 brief" prefix | Medium | L2 |
| C-009 | The sentence the report may print about the count | none new | "Z0 and K briefs carried a clause naming a ledger; n of N reports wrote one." | n = 0 is "none seen in N reports (upper bound x%)", never "harmless"; n >= 3 of 60 adds a line to D2 and D7 | Low | L1 |

## Contradictions
| # | Point of conflict | Position A | Position B | Impact | Level |
|---|---|---|---|---|---|
| X-001 | Is CB-2's hash frozen and a reword a re-run of both arms? | V2 evidence 4: hash "already pinned in `config/freeze.json` and in every `run.json`"; a reword "means re-running both arms" (V3 section 6 also names `config/freeze.json`) | CORR-1: the file does not exist, no run exists, the freeze has not run | High (V2's cost argument for its rule rests on it; before the freeze there is no re-run cost) | L3 |
| X-002 | "One shared control" with RL | pack F8 and V2 section 3: a reword here "splits the control" | RL DR-12 (CORR-2): two builds, two Z0 and K blocks, byte-identical briefs, pooling optional | Medium (the cost of an SW-only reword is the loss of byte identity and of the pooling option, not a split run set) | L2 |
| X-003 | MR 5.3 says K has "no ledger"; K's brief carries a clause that names ledger rows | V2 evidence 7 | V1 evidence 3: K = Z0 plus a paragraph, and Z0 holds CB-2 by MR 201 and 209; "no ledger" describes machinery, not a word | Low | L2 |

## Unique Contributions
| # | Variant | Contribution | Value | Level |
|---|---|---|---|---|
| U-001 | V2 | Contingent reword text (clause dropped from CB-2, PROBLEM-row duty moved to a new SS-only part `briefs/ledger-link.txt` after the ledger rule) with sha256 values | Medium | L2 |
| U-002 | V3 | Report rule: n of N with an exact one-sided 95% upper bound; never "harmless"; n >= 1: found fraction and finding count with and without a heading as numbers without a test | High | L3 |
| U-003 | V3 | A free real-model look: the Z0 reports of the timing spike (CORR-4) | High | L2 |
| U-004 | V1, V2 | `results/copy-briefs.py` would overwrite a reworded `cb2.txt` if re-run (lines 29-36, 66-68) | Low | L2 |

## Shared Assumptions
| # | Assumption | Source agreement | Classification | Promoted | Level |
|---|---|---|---|---|---|
| A-001 | Reviewers read the clause as inert or conditional in Z0 and K | all three (V1 states it; none has real-model evidence, pack F7) | UNSTATED | yes | L3 |
| A-002 | A report-only consequence is enough because no gate reads the count (CORR-3) | all three | STATED | no | L3 |
| A-003 | The owner's verdict rule counts a missing consequence rule as "misleading" or "unmeasurable" (the debate-1 standard) | V2 and V3 | UNSTATED | yes | L3 |
| A-004 | The `## Ledger` heading is the visible symptom of the harm; harm without a heading (padding, an invented checklist, fewer findings) is not seen by any option | V1 and V3 | STATED | no | L3 |
| A-005 | The clause is the only instruction that every PROBLEM row gets a findings line, so dropping it changes SS | all three (pack F3, `DESIGN.md` 511-519) | STATED | no | L2 |

## Summary
- Structural 1, content 9, contradictions 3, unique 4, shared assumptions 5 (UNSTATED 2, both promoted: A-001, A-003; STATED 3: A-002, A-004, A-005; CONTRADICTED 0).
- Debate points for convergence: S-001, C-001 to C-009, X-001 to X-003, A-001 to A-005 = 18.
- Highest severity: C-001, C-002, X-001.
- Level coverage: L1 = S-001, C-009; L2 = C-001, C-003, C-004, C-006, C-007, C-008, X-002, X-003, A-005; L3 = C-002, C-005, X-001, A-001 to A-004. All three levels are covered.
