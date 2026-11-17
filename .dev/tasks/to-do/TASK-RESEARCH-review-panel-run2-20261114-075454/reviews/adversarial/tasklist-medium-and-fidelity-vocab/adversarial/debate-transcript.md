# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A then B) plus Round 2.5 invariant probe; no Round 3 (standard depth)
- Convergence achieved: 86.5% (32 of 37 diff points agreed)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant A = Proposal A, `variant-1-original.md`; Variant B = Proposal B, `variant-2-original.md`; both default model, default persona)
- Denominator: 7 S + 14 C + 10 X + 6 promoted A (A-004..A-009, the UNSTATED shared assumptions) = 37. The four STATED assumptions (A-001, A-002, A-003, A-010) are documented in `diff-analysis.md` and not promoted.
- Full advocate texts (verbatim, written by the advocate agents): `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md` in this folder. This file records each round's content in condensed form and the orchestrator's per-point tracking.

## Round 1: Advocate Statements

### Variant A Advocate (default model, default persona) — `round1-advocate-A.md`

- Position: a tasklist Medium must not block, because every other written Medium in the repo is non-blocking (the `/sc:implement` model that S4 cites as its exemplar, `refs/qa.md:81`; `card_convert.py:71-83`; the CLI gate; `pragmatic.md:230`). A is the better position only with a written grading block and the omission rule.
- Steelman of B: the Medium-blocks text is explicit and pinned in four places (9 skill sites, 12 sweep rows, 2 worker-contract pins, `commands/tasklist.md:113`); B's change is smaller and loosens nothing; B has the only data (two archived ValidationReports); the CLI's non-gating Medium has a plain cause (no fixer).
- Strengths claimed: S4's exemplar maps medium to minor; the skill's rule is label-driven with no definition (S5 direction); the #343 history shows a bucket mapping, not a Medium decision; B's reading of the archive does not hold (2 omissions, 4 weaker-but-present of 6); B's blocking Medium widens the regression-halt channel (SK:1610); A is statically testable; both maps parse, A states the `reflect_category` hazard.
- Weaknesses identified in B: S4 premise holds only after B's own edit; B's Medium definition is a dilemma; two opposite readiness answers to one question; E6/E7 overstate the archive; B's new text is unpinned; `card_convert.py` caution supports A.
- Concessions: X-004 (A read no report; regrade is an assumption; do not adopt before M1); X-009 (union mitigation dropped, one grader per task slice); X-003 (the edit was deliberate); X-001/X-006 (S5 names no High/Medium/Low scale); X-005 (no module role table exists); X-008; X-010; A's edit list omits `commands/tasklist.md:113`; Form 2 withdrawn in substance; A loosens a gate.
- Shared-assumption responses: A-004 QUALIFY, A-005 QUALIFY, A-006 QUALIFY, A-007 ACCEPT, A-008 QUALIFY, A-009 ACCEPT. No omissions.

### Variant B Advocate (default model, default persona) — `round1-advocate-B.md`

- Position: keep Medium blocking and the fidelity prompt separate; after re-reading, rest this on S1's definition of blocking, not S4, and accept a tightening: Medium = "incomplete or weakened against a stated roadmap requirement", pure wording or ambiguity moves to Low (Hybrid H).
- Steelman of A: one review rule (S1-S5); the skill defines no label (S5 targets that); the only written definition is the CLI's; the CLI passes a Medium-only report; A adds a grading block, regrades omissions to High and states its costs.
- Strengths claimed: blocking Medium is shipped and pinned in four places; the sweep drew the line at Low on purpose; the archived Medium findings are mostly "incomplete against a stated roadmap requirement" (own read: 2 omissions, 2 acceptance gaps, 2 assumption/inconsistency); under B the grade boundary cannot decide the verdict while Stage 7 is re-sampled (SK:1608, SK:1410); no core change; the fidelity gate is a shared contract.
- Weaknesses identified in A: A's two promises about the Medium definition contradict (the CLI MEDIUM example "Acceptance criteria are weaker", PR:62); the union mitigation does not exist at Stage 7; A makes a re-sampled grade verdict-decisive; A's edit list is incomplete (`commands/tasklist.md:113`); Form 2 is new core code the adjudicated shape excludes; A reads S5 wider than written; the "one product" argument is internally inconsistent; A loosens the only hard gate.
- Concessions: X-002 (S4 premise conceded), X-003 partly, X-004 (E7 ignores the regrade), E6 overstated "mostly omission", X-005 true of today's code only, X-010 (line ranges wrong), A-007/INV-J interpretation, INV-016 exposure real under B.
- Shared-assumption responses: A-004 QUALIFY, A-005 QUALIFY, A-006 QUALIFY, A-007 ACCEPT, A-008 REJECT, A-009 QUALIFY. No omissions.
- Round 1 verdict by B: B survives as hybrid H; the decisive open measurement is M-X15-1 on a larger set of real Medium findings.

## Round 2: Rebuttals

### Variant A Rebuttal — `round2-advocate-A.md`

- Concedes W1 (the CLI Medium example and the omission regrade contradict), W2 (union), W3 in part ("B's best point": SK:1608 + SK:1410 make a High-only `F_k` a false-clean path under re-sampling), W4 (`commands/tasklist.md:113`; the pins read the command file via `_unattended_section`, `test_worker_contract.py:893-906`), W5 (Form 2 withdrawn), W6 (S5 literal reading), W7, and W8 (loosening is the real cost).
- Tests B's H on its merits: B's Medium does not collapse into CLI HIGH (it maps onto PR:62); the dispute narrows to one class, "weakened but still present". Counts against H: it blocks on the one class the CLI passes; its Low swallows CLI-MEDIUM "ambiguous language"; its parity test is hollow; the naming collision with `pragmatic.md:230`, `qa.md:81`, `:274`, `card_convert.py`.
- Proposes hybrid A+: grading block (High = omits, contradicts, fabricates, or a criterion dropped or weakened so a roadmap-stated check can no longer fail; Medium = warning, still checkable; Low = notes), grade higher when torn, dedup keeps highest severity, Stage 8-10 count High only, SK:1421-1422 regraded to High, PR:62 split, 12 rows + `commands/tasklist.md:113` + 2 pins rewritten, adoption gated on M-X15-1, M1 and M-X15-5 with fallback to H.
- Central answers: (a) Medium does not block under A+, conditional on measurement; (b) the fidelity prompt stays outside the core (moved to B's placement; parity test kept); (c) measurement is a precondition for the loosening only, not for the grading block, the parity test or the placement.
- Changed responses: A-008 QUALIFY to REJECT; A-009 ACCEPT to QUALIFY. Moved positions: S-004 to B, C-002 to Hybrid, C-003 to B, C-008 to Hybrid.

### Variant B Rebuttal — `round2-advocate-B.md`

- Concedes W1 (S4 premise), W2 in part, W3 narrowed to one class, W4 (archive overstated; own re-read: 2 omissions, 2 dropped acceptance criteria, 1 contradiction, 1 assumption-as-fact), W6 (new text unpinned), W7 as naming evidence.
- Assessment of A+: right on the consequence boundary as the blocking test; one blocking tier matches every other written model; dedup-highest and tie-break-up are real fixes (adopted). Wrong or risky: no buffer tier (a High typed Medium is a false-clean; the one observed failure is real reviewers typing two omissions Medium), "grade High when torn" enlarges High, the PR:62 split changes the exit-1 rate of `tasklist validate` (the prompt has one caller, `executor.py:173`; the phrase occurs once, `prompts.py:62`), the parity test is real only after PR:62 is edited. Blocking set is identical in A+ and H+ by construction; they differ in the label word, the buffer tier, churn (about thirty edit sites vs two) and the PR:62 edit.
- Tests its own H against A's four counts: count 1 true (declared divergence on one class), count 2 true for wording and false for outcome, count 3 true as written (partly fixable), count 4 true and measurable.
- Final position H+: B's H plus A's consequence boundary, dedup-highest, tie-break-up and a pinned containment test. Grading block: High = omits/contradicts/fabricates; Medium (blocking) = present but a criterion, checkpoint or validation step is dropped or softer so a roadmap-stated check can pass where the roadmap's would fail; Low (note) = detail, ambiguity, estimate, equivalent method, formatting, wording. One insertion after SK:1391 and one clause at SK:1410; no existing sentence edited; 12 rows, `commands/tasklist.md:113` and 2 pins untouched; CLI prompt unchanged; core gets nothing. Measurements F1 (M-X15-1), F2 (M1 under both blocks, FC/FB), F3 (M-X15-5, both boundaries); thresholds registered before any run; default H+ if not run or not met; A+ replaces H+ only if FC(A+) <= 1, FC(A+) <= FC(H+) and FB(H+) - FB(A+) >= 3 and the owner accepts the PR:62 edit.
- Changed responses: none to A-004..A-009 beyond Round 1 (A-008 REJECT, A-009 QUALIFY).

## Round 2.5: Invariant Probe

Run by an independent fault-finder agent (`x15-fault-finder-r25`), not an advocate. Output: `round2.5-fault-finder-raw.md`; assembled table: `invariant-probe.md`. 20 findings, 3 ADDRESSED, 17 UNADDRESSED; HIGH UNADDRESSED: INV-017 (H+ is not behaviour-preserving: its block lands unmeasured and moves "insufficient detail / ambiguity" to a non-blocking Low) and INV-018 (dedup-highest plus tie-break-up do not act on the across-run re-sampling of SK:1608).

## Scoring Matrix

Winner key: A, B, Hybrid (named), Neither, Unresolved (the two advocates' final positions differ on the point's own content). For A-NNN points the "winner" column holds the shared response both advocates gave. Confidence follows the protocol: unanimous 90-94 with a concession boost, unanimous with the point of low consequence 85, split 50-55.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|------------------|
| S-001 | L1 | A | 85% | Both advocates (R1, R2): an inputs-first dependency table lets a reader check C-01..C-03 reliance. |
| S-002 | L1 | A | 85% | Both: one checkable fact per row beats bundled prose cites; B conceded E1 bundled six cites. |
| S-003 | L1 | Neither | 85% | Both: heading depth does not affect correctness. |
| S-004 | L2 | B | 88% | A moved to B in R2: fidelity prompt stays outside the core with an adapter seam; no consumer or role table exists. |
| S-005 | L3 | Hybrid (A's static tests + B's pre-registered thresholds) | 85% | Both name the same hybrid. |
| S-006 | L1 | Neither | 85% | Both: scope statements are cosmetic. |
| S-007 | L2 | B | 85% | Both: a stop condition that a measurement can trigger is more useful. |
| C-001 | L3 | Unresolved (A+ vs H+) | 50% | A: Medium warns, adoption gated; B: the word Medium stays on the blocking sub-class until F2 overrules it. Blocking set identical by construction (B R2), the label word and the default differ. |
| C-002 | L2 | Hybrid (PM:225/PM:231 consequence test decides) | 85% | Both: neither S4 (X-002) nor S5 as literally written (X-006) is a basis; consequence test applied by analogy. |
| C-003 | L3 | B | 95% | A withdrew Form 2 (W5): `findings_v2.py:155-162` is not reusable; C-02 ruled out a core predicate. Form 1 only. |
| C-004 | L3 | Hybrid (A's grading block; label of SK:1421-1422 left to C-001) | 80% | Both adopt the grading block; both keep the two TDD checks blocking until measurement; the label differs (A+ High, H+ Medium). |
| C-005 | L2 | B | 90% | A: B's edit is smaller; A+ pays about ten sites, `commands/tasklist.md:113`, 12 rows and 2 pins (stated as cost). |
| C-006 | L3 | B | 90% | A concedes: B holds every pin; A+ rewrites them. |
| C-007 | L3 | Unresolved | 50% | Dedup-highest and tie-break-up are adopted by both; whether `F_k` counts Medium (A+ High-only, H+ as today) is the C-001 split, gated by F2/F3. |
| C-008 | L2 | Hybrid (B's placement outside the core, A's parity/containment test) | 85% | Both. |
| C-009 | L2 | B | 90% | Both: the shared six-field contract is a reason to leave the gate and prompt in place. |
| C-010 | L2 | B (with A's corrected reading of the archive) | 82% | A: "B has the only data"; B: its own reading was corrected by A's (2 omissions, 2 dropped acceptance criteria, 1 contradiction, 1 assumption). |
| C-011 | L3 | Hybrid (A's static tests, B's registered thresholds, M-X15-5) | 85% | Both; threshold numbers differ in detail, structure and default rule are shared. |
| C-012 | L3 | Unresolved | 50% | A: Neither (exposure under both, B's buffer claim unmeasured); B: H+ adds a buffer tier for High-typed-Medium. |
| C-013 | L2 | Unresolved | 55% | A: ambiguity stays Medium (CLI text), split PR:62; B: ambiguity goes to Low, Medium = PR:62 class only. Both non-blocking for ambiguity; labels and the PR:62 edit differ. |
| C-014 | L2 | Unresolved | 50% | A: A (Medium-as-warning matches rf-qa, `qa.md:81`); B: Neither (outcome matches rf-qa, the word collides with PM:230). |
| X-001 | L2 | Neither | 85% | Both: S4 and S5 are overread; PM:225/231 decide. |
| X-002 | L2 | A | 95% | B conceded: the skill states no model before B's own edit. |
| X-003 | L2 | B | 82% | Both: the fixture header (`:29`) records "open High/Medium findings HALT"; the dispute is only framing. |
| X-004 | L3 | Hybrid (settled by F1/M-X15-1, not argument) | 82% | Both. |
| X-005 | L3 | B | 90% | Both: no module-declared role table exists (`ROLES` closed, `findings_v2.py:35`). |
| X-006 | L2 | B | 90% | Both: `pragmatic.md:229/:231` name no High/Medium/Low scale. |
| X-007 | L2 | Neither | 85% | Both: "gap" and "no fixer" are inferences. |
| X-008 | L2 | B | 90% | A conceded: one product family, not one code path. |
| X-009 | L3 | B | 95% | A conceded fully: one grader per task slice (SK:1351-1368), no cluster for a union. |
| X-010 | L1 | A | 95% | B conceded its line ranges were wrong (`prompts.py:49-69`, `roadmap/gates.py:195-240`, test `:208-225`). |
| A-004 | L2 | QUALIFY (both) | 85% | A marker is not needed for the decision; survival through the ledger merge unverified. |
| A-005 | L2 | QUALIFY (both) | 85% | Stage 7 findings are prose today (SK:1384-1391); no consumer reads the map. |
| A-006 | L2 | QUALIFY (both) | 85% | Risk-level `Medium` (SK:565, 581, 964, 1699) and complexity `MEDIUM` (SK:735) must be left alone. |
| A-007 | L2 | ACCEPT (both) | 85% | The sweep header applies S1/S2 to 12 tasklist rows; P2 is 2 fix cycles, inside S3. |
| A-008 | L3 | REJECT (both) | 92% | SK:1608 re-runs with fresh agents; SK:1410 has no severity tie-break (A changed QUALIFY to REJECT). |
| A-009 | L3 | QUALIFY (both) | 85% | Static counts hold; no test was run by either advocate. |

Points won, for tiebreaker use: Variant A 4 (S-001, S-002, X-002, X-010); Variant B 12 (S-004, S-007, C-003, C-005, C-006, C-009, C-010, X-003, X-005, X-006, X-008, X-009); Hybrid 6 (S-005, C-002, C-004, C-008, C-011, X-004); Neither 4 (S-003, S-006, X-001, X-007); Unresolved 5 (C-001, C-007, C-012, C-013, C-014); shared A-NNN responses 6.

## Convergence Assessment

- Points resolved: 32 of 37 (S 7 of 7, C 9 of 14, X 10 of 10, A 6 of 6)
- Alignment: 86.5% (32 / 37 = 0.8649)
- Threshold: 80%
- Unresolved points: C-001, C-007, C-012, C-013, C-014
- Taxonomy coverage gate (AD-5): L1 covered (S-001, S-002, S-003, S-006, X-010), L2 covered (21 points), L3 covered (15 points, e.g. S-005, C-001, C-003, C-007, X-004, X-009, A-008). No forced round needed.
- Invariant probe gate: BLOCKED. 2 HIGH UNADDRESSED invariants (INV-017, INV-018); no Round 3 at standard depth, so they are not resolved. 12 MEDIUM UNADDRESSED are warnings.
- Status: BLOCKED_BY_INVARIANTS (agreement above threshold, taxonomy covered, HIGH UNADDRESSED invariants exist)

Note on denominator: only the 6 promoted (UNSTATED) A-NNN rows are counted, per the protocol's promotion rule; the 4 STATED rows drew no required response. Excluding all A-NNN rows gives 26 of 31 = 83.9%, still above the threshold with the same status.
