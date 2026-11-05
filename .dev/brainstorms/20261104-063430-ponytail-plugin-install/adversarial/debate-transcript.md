# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A then B then C), plus Round 2.5 invariant probe
- Convergence achieved: 94% of diff points (58 of 62)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (A = opus:architect, B = sonnet:refactorer, C = haiku:qa)
- Source of every statement: the round files below. Each statement is authored once, in its round file; this transcript indexes them and records the scoring.
- Round 3: skipped (depth=standard)
- Incident: the Step 1 diff agent dropped on an API connection error and was resumed with its context; no round was affected.

## Round 1: Advocate Statements

| Advocate | File |
|---|---|
| Variant A (opus:architect) | `debate/round1-variant-A.md` |
| Variant B (sonnet:refactorer) | `debate/round1-variant-B.md` |
| Variant C (haiku:qa) | `debate/round1-variant-C.md` |

Each file contains Position Summary, Steelman of the other two, Strengths, Weaknesses of others, Concessions, positions on diff points, and ACCEPT/REJECT/QUALIFY on A-001..A-009. No `[OMISSION]` flags: every advocate answered all nine shared assumptions in Round 1 and again in Round 2.

## Round 2: Rebuttals

| Advocate | File | Positions changed |
|---|---|---|
| Variant A | `debate/round2-variant-A.md` | Label-fix shape moved from C's `(label, argv)` pairs to B's 4-line shape; A-007 REJECT to QUALIFY (the second logged run was offline, not starved). Conceded the false failure row (X-003), the false budget rationale (X-005), "zero Python" (X-002) and the order test. |
| Variant B | `debate/round2-variant-B.md` | Split manual check into M1a (install mechanics) and M1b (env); specified the M1b fail outcome. Conceded the UserPromptSubmit claim (X-008) with upstream evidence, the budget wording, and two missing rejected alternatives. |
| Variant C | `debate/round2-variant-C.md` | Gave up "Ponytail first" (X-001); gave up `(label, argv)` pairs; A-004 ACCEPT to QUALIFY. Conceded X-004, X-015, X-016, X-017 and S-010. Added the untested claude-absent branch (N1) and the A-003 masking mechanism (N4). |

Merge recommendation, identical in all three Round 2 files: B's code, tests and docs as base; A's structure, decision record, gate wording, extension rule and per-subagent count; C's claude-absent leg, both-path `--scope` assertions, docs grep and Coder question.

## Round 2.5: Invariant Probe

File: `invariant-probe.md`. 31 findings: 11 ADDRESSED, 20 UNADDRESSED (HIGH 4, MEDIUM 6, LOW 10).

HIGH and UNADDRESSED: INV-001 (mode `off` is not dormant: the band module runs in every mode), INV-027 (existing workspaces need a package upgrade; Coder template unconfirmed), INV-028 (Orca can consume the whole 30 s budget on every run), INV-029 (no positive check that Ponytail works in a session).

## Scoring Matrix

Winner column: the approach the advocates agreed on in Round 2 (majority rule, 2 of 3 or more). "merge" names the parts taken from each.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | not debated | 50% | Cosmetic header difference; no advocate took a position. Unresolved. |
| S-002 | L1 | A | 75% | A's decision table plus rejected-alternatives record adopted by B and C in Round 2. |
| S-003 | L1 | not debated | 50% | Requirement numbering layout; no position. Unresolved. |
| S-004 | L2 | B | 85% | B's JSON + illustrative Python + rejected list is the executable base (all R2). |
| S-005 | L2 | A | 80% | A's four-column interaction table preferred (B R2 steelman, C R2). |
| S-006 | L2 | A (corrected) | 70% | A's table with evidence column, rows corrected per X-003. |
| S-007 | L2 | merge B+A | 85% | B's M1a/M1b IDs with A's pass/fail wording (all R2). |
| S-008 | L2 | B | 85% | B's T-table with "Proves" column; C's legs folded in. |
| S-009 | L1 | B | 75% | IDed risks; C conceded unIDed rows (C R2 #3). |
| S-010 | L1 | B | 85% | File's `###`/`####` style; C conceded. |
| S-011 | L1 | merge B+C | 80% | B's three questions plus C's fork-version question. |
| S-012 | L1 | not debated | 50% | Out-of-scope list length; no position. Unresolved. |
| S-013 | L1 | B | 75% | Real repo log evidence preferred. |
| C-001 | L2 | B | 95% | Defaults plus label fix; A conceded (A R2 R-2). |
| C-002 | L3 | B | 95% | Append last as convention, no budget rationale, no order test; C conceded (C R2 #1). |
| C-003 | L3 | all (same) | 95% | `env.PONYTAIL_DEFAULT_MODE="off"`; pending coordinator confirmation of the mode value. |
| C-004 | L1 | all (same) | 100% | No change to update paths. |
| C-005 | L3 | B | 100% | Fix the label; A conceded. |
| C-006 | L2 | B | 95% | 4-line shape; A and C moved to it in R2. |
| C-007 | L2 | B with A's rule | 90% | 5-line cap; A's replacement rule as NFR wording. |
| C-008 | L1 | B + C grep | 90% | Count-free sentence plus `grep -rn "six plugins" docs/`. |
| C-009 | L1 | merge | 85% | B's paragraph plus "do not delete", ledger, "user settings" (B R2 #6). |
| C-010 | L1 | B | 90% | Added + Fixed + migration sentence. |
| C-011 | L2 | merge | 90% | B's T1..T5 + C's claude-absent leg; Ponytail-keyed legs dropped. |
| C-012 | L3 | merge | 90% | Non-blocking M1a/M1b with A's pass/fail wording. |
| C-013 | L3 | C | 90% | Documented `config.json` user step + follow-up; no installer write. |
| C-014 | L1 | merge | 80% | `false` in user settings; do not delete; mode via env. |
| C-015 | L1 | all (same) | 100% | No `install --list` / `doctor` change. |
| C-016 | L1 | merge B+C | 90% | Handoff questions. |
| C-017 | L3 | probe | 85% | Ledger and band run in every mode (INV-001); certainty settled by the probe. |
| C-018 | L3 | A | 85% | `node` already required by `pragmatic-subagent.js`; C conceded X-017. |
| C-019 | L3 | none (corrected) | 85% | All three budget rationales corrected; Orca starvation is a follow-up. |
| C-020 | L3 | A | 90% | Tracker re-injects only for Qoder; B conceded with upstream lines. |
| C-021 | L3 | B | 90% | Migration sentence plus `/ponytail default` warning. |
| C-022 | L3 | all (same) | 85% | No pin; single named source. |
| C-023 | L2 | B | 85% | Diff-scope AC. |
| X-001 | L3 | B | 95% | See C-002. |
| X-002 | L2 | B | 95% | See C-001. |
| X-003 | L3 | B/C | 100% | A conceded; real log at `P2-layer2.md:624`. |
| X-004 | L3 | B | 100% | C conceded. |
| X-005 | L3 | none (corrected) | 95% | Adds precede installs; all three corrected text. |
| X-006 | L3 | none (corrected) | 95% | C conceded. |
| X-007 | L3 | C | 90% | See C-013. |
| X-008 | L3 | A | 90% | See C-020. |
| X-009 | L3 | merge | 90% | Non-blocking given `env-propagation-evidence.md`. |
| X-010 | L1 | B | 90% | See C-008. |
| X-011 | L1 | merge | 85% | Handoff as questions plus a handoff section. |
| X-012 | L3 | none (corrected) | 75% | Clone-size claims dropped in favour of the corrected queue order. |
| X-013 | L3 | probe | 85% | Ledger writes are certain when enabled (INV-001). |
| X-014 | L1 | not debated | 50% | Whether to name `claude plugin uninstall`; no advocate resolved it. Unresolved. |
| X-015 | L1 | B | 90% | C conceded ID hygiene. |
| X-016 | L1 | B | 90% | C conceded. |
| X-017 | L3 | A | 90% | C conceded. |
| A-001 | L3 | all REJECT | 95% | False as stated; docs state "upgrade the package, then update". |
| A-002 | L3 | all QUALIFY | 80% | Enabled-but-not-installed is an existing state; session outcome UNVERIFIED. |
| A-003 | L3 | all QUALIFY | 85% | Checked in M1a with the exact second-run message (C R2 N4). |
| A-004 | L3 | all QUALIFY | 80% | No required fields; closed-stdin prompting checked in M1a. |
| A-005 | L3 | all ACCEPT | 95% | Skills do not read the mode (`assumption-evidence.md`). |
| A-006 | L3 | all QUALIFY | 85% | No phrase switches the mode on; per-prompt `node` cost remains. |
| A-007 | L3 | all QUALIFY | 90% | Converges only while some run leaves budget; Orca mechanism observed twice. |
| A-008 | L3 | ACCEPT (B, C); QUALIFY (A) | 70% | Majority ACCEPT. |
| A-009 | L3 | all QUALIFY | 80% | Hook failure display and latency UNVERIFIED. |

## Convergence Assessment

- Points resolved: 58 of 62 (S 10/13, C 23/23, X 16/17, A 9/9). Unresolved: S-001, S-003, S-012 (cosmetic, never debated), X-014 (naming an uninstall command).
- Alignment: 94% (58/62)
- Threshold: 75%
- Taxonomy coverage: L1 covered (e.g. C-008, X-010), L2 covered (e.g. C-001, C-006), L3 covered (e.g. C-002, C-012, A-001..A-009). Gate passed.
- Invariant gate: initially BLOCKED_BY_INVARIANTS (INV-001, INV-027, INV-028, INV-029 HIGH and UNADDRESSED). Depth is standard, so no Round 3 runs. The orchestrator resolved each in the refactoring plan: INV-001 and INV-029 by spec changes (real `off` footprint documented; positive check M1c added); INV-027 and INV-028 accepted as documented risks (package-upgrade step in docs plus Coder handoff section; Orca budget starvation stated as a known limitation and listed as a follow-up). MEDIUM items INV-002, INV-006, INV-009, INV-024 are folded into wording and risks.
- Status: CONVERGED after invariant resolution (diff points 94%, all taxonomy levels covered, every HIGH invariant either addressed in the plan or accepted as a documented risk).
- Open decision outside the debate: the default mode value (`off` recommended) and whether the ledger defaults off are with the coordinator (question `msg_d37768933f42`, correction `msg_3493f6c1db7d`).
