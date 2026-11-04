# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 debate rounds (Round 1, Round 2), plus the Round 2.5 invariant probe and 1 extra invariant-resolution round (see the final metadata block)
- Convergence achieved: 85.2% (23 of 27 diff points)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3
- Mode: A (`--compare` of three sc:reflect Wave-3 reviewer cards); this run is sc:reflect Wave 4
- Variants: A = `variant-1-original.md` (reviewer 1, analyzer, sonnet); B = `variant-2-original.md` (reviewer 2, qa, glm-5.3 on the haiku alias); C = `variant-3-original.md` (reviewer 3, refactorer, opus)
- Calibrated confidence (`../artifacts/calibration-t2.yaml`): A 0.82, B 0.78, C 0.82. Context only; not a scoring input.
- Sources: `diff-analysis.md`, `round1-advocate-{A,B,C}.md`, `round2-advocate-{A,B,C}.md` (sequential A, B, C), `invariant-probe.md`, `round-inv-advocate-{A,B,C}.md`
- Citation key: P = plan `.dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md`; S = `source.md` in the same folder; IMPL = `~/.claude/skills/sc-implement-protocol/SKILL.md`
- Generated: 2026-11-04T18:48:52Z

## Round 1: Advocate Statements

Ran in parallel. Full text: `round1-advocate-{A,B,C}.md`.

### Variant A Advocate (analyzer card, A-1..A-11)
**Position**: Card A has the widest acceptance-criteria coverage (16 of 22 canonical findings). Its severities follow one rule: Medium when an AC or test runs an artifact outside the task's closure, Low when only prose or order is affected.

**Steelman of B and C**: C found the biggest miss on any card, Task 19 with no path to Task 13 (U-001), and gave the only full chain for the shared test file (F-4). B showed that the `.claude/` staging check is vacuous and tied the dropped identity to real breakage.

**Key strengths claimed**:
1. U-002 / CF-09: `git ls-files -s` prints nothing for an untracked file, so Task 10's mode AC cannot pass.
2. C-006 / CF-08: P:27 states the staging rule but no task stages anything (S:1429).

**Weaknesses identified in B and C**:
1. F-10 / X-004: Task 5 on Task 4 and Task 8 on Task 4 are spec-required, because spec step 3 = Tasks 3 + 4. Only Task 9 on Task 6 is stricter.
2. F-9 / X-003: the spec itself splits E5 and E12 (S:1416, S:1426), so "necessary" is the wrong label.

**Concessions**:
- A missed CF-17 and CF-22. A-10b (CF-07) withdrawn. A-7 (CF-10) made advisory. A-8d (CF-14) reclassified as a spec defect: P:53 inherits `:86-99` from S:731.
- Shared assumptions: A-001 ACCEPT, A-002 ACCEPT, A-006 QUALIFY.

### Variant B Advocate (qa card, Q-1..Q-8)
**Position**: Verdict unchanged (ready-with-fixes). B gives the best severity call on CF-11/CF-12 (Q-5): S:1316 requires a fixed author and committer and a capability skip, and P:29 and P:291 carry neither, which breaks F9, F10, X1 and X3.

**Steelman of A and C**: A owns AC observability (U-002, U-006). C owns structure (F-2, F-7, F-8, F-9), and U-001 is the highest-value finding.

**Key strengths claimed**:
1. Q-5 (CF-11, CF-12) at Medium with the named breakage.
2. Q-7 (U-014): without staging, the "no staged `.claude/`" check at P:307 is vacuously true.

**Weaknesses identified in A and C**:
1. A bundled CF-11 and CF-12 into low-severity A-8 (C-007).
2. A's "blast radius smaller" (X-002) covers import failure only, not the unexercised CLI path.

**Concessions**:
- Overconfident (self 0.87 vs calibrated 0.78, C-012). Q-1 cites S:1392; the make-test line is S:1408 (C-011). B shared the A-002 blind spot that missed CF-22. B adopts U-001 and U-002 to U-005.
- Shared assumptions: A-001, A-002 and A-006 ACCEPT.
- Recording note: B's R1 point table labels the CF-04, CF-05 and CF-06 rows "C-004", "C-005" and "C-006". By content they are diff points C-003, C-004 and C-005. This transcript scores them by content. B's position on C-006 (CF-08) comes from its prose: "A-6b's fix is stronger — adopt it".

### Variant C Advocate (refactorer card, F-1..F-11)
**Position**: Card C has the best graph structure: F-2 (Task 19 to Task 13), F-4 (one chain for the shared test file) and F-1 (split Task 4 along the resume boundary).

**Steelman of A and B**: Only A found the unobservable mode check (P:191) and the missing staging step (S:1429). Only B tied the identity and capability-skip gap to concrete breakage. A and B caught CF-13 and CF-14; C missed them.

**Key strengths claimed**:
1. F-2: spec step 13 depends on all of step 9 (S:1428), and Task 19's closure has no Task 13.
2. F-8: confirmed that `poll-ci-checks.sh:30` exits 2 when `--pr` is missing.

**Weaknesses identified in A and B**:
1. A and B miss CF-17 to CF-21.
2. Uneven severity scale for one defect type (X-005).

**Concessions**:
- F-2 over-reaches: X1's command list (S:1400) omits `expect_checks_after_push`, so only the Task 13 edge is required (U-001 Medium, not High).
- F-1 drops to Low drift. F-6 drops to Low, Task 20 only. F-9 relabelled drift. F-10 / X-004 conceded. C also missed CF-22.
- Shared assumptions: A-001, A-002, A-003 and A-004 ACCEPT; A-005 and A-006 QUALIFY.

## Round 2: Rebuttals

Ran sequentially in the order A, B, C. Each advocate saw all Round 1 files, and B and C also saw the Round 2 files before theirs.

### Variant A Rebuttal
A concedes the severity scale (X-005) with a sharper rule: Medium when an AC or test, run as written, fails, passes falsely or cannot be observed; Low when only prose or order is affected and a later gate fails loudly. Under that rule A concedes CF-03 and CF-04 to Medium (false green at the release gate) and CF-11 and CF-12 to Medium. A rejects B's "necessary, Medium" for CF-05/06 and adopts C's 4a/4b split, plus one new edge: 4b depends on Task 5, because P:93 and P:114 both append to `test_conflicts_core.py`. A holds CF-07 as advisory, CF-14 as a spec defect, and CF-15 and CF-18 at Low. On CF-17, only Task 13 is required. CF-21 is revised to "necessary", because Task 9's AC collects `test_ci_classify.py`.

### Variant B Rebuttal
B concedes CF-05/06 to Low drift, CF-15 and CF-18 to Low, CF-17 to Task 13 only, CF-14 to spec defect and CF-07 to advisory. B verifies and adopts A's 4b-on-5 edge, and adds one change: Task 8's Task 4 dependency (P:155) re-points to 4b, which holds the planners Task 8 calls (P:166). B holds CF-11/12 at Medium, and A has already conceded them. B's final table agrees fully with A's Round 2 table plus the Task 8 re-point.

### Variant C Rebuttal
C agrees with every row except CF-05. C verifies the 4b-on-5 hazard and warns that the A/B edge set is incomplete. P:106 still reads "Depends on: Task 4", which closes the cycle 4b → 5 → 4b if read as 4b. If read as 4a, Task 9 (P:171), which exports the 4b planners (S:741-744), cannot reach 4b. C proposes "Task 5 on 4b; 4b on 4a, 7; 8 on 4b". Its fallback, if the panel keeps the A/B ordering, adds "Task 5 on 4a" and "Task 9 on 4b". C concedes CF-04 (list Task 6 explicitly), CF-07 and CF-14.

## Round 2.5: Invariant Probe

Full table: `invariant-probe.md`. It reports 18 findings: 11 ADDRESSED and 7 UNADDRESSED. The UNADDRESSED findings are 3 HIGH (INV-001, INV-002, INV-005), 2 MEDIUM (INV-006, INV-007) and 2 LOW (INV-012, INV-014).
- INV-001: the A/B CF-05 set leaves P:106 unchanged, which gives either a cycle or a missing path.
- INV-002: under 4a → 5 → 4b, Task 9 imports `conflict_resume_plan` and `crash_resume_plan` (S:744) before 4b defines them, and every `tests/pr_submit` gate fails.
- INV-005: `/sc:implement` runs tasks sequentially in document order and ignores `depends-on`, and P has no `independent` or `parallel` marker. The CF-05 fix must therefore state 4b's document position.
- INV-006: under document order, every edge-only fix (CF-01, 02, 03, 04, 17, 22) is already satisfied, so their Medium ratings rest on the refuted assumption A-003.
- INV-007: Task 1 and Task 3 both edit `test_static_grep.py` with no ordering edge.

The probe recommends R-INV, which is C's Round 2 fallback plus 4b's document position.

```
CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002, INV-005
These invariant violations must be resolved before convergence can be declared.
WARNING: 2 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-006, INV-007
```

## Invariant-Resolution Round (extra round, triggered by the invariant gate)

Full text: `round-inv-advocate-{A,B,C}.md`. The R-INV elements:
- E1: the A/B set plus "Task 5 on 4a" and "Task 9 on 4b".
- E2: 4b sits between Task 7 and Task 8.
- E3: split the P:95-100 ACs, with logs `t4a` and `t4b`.
- E4: Task 3 depends on Task 1 and Task 2.
- E5: record INV-006 and lower CF-01, 02, 03, 04, 17 and 22 to Low.

| Element | A | B | C |
|---|---|---|---|
| E1 edge set | ACCEPT; adds the stale "from Task 4" at P:241 (R-INV omitted it) | ACCEPT, on condition that the Task 8 → 4b re-point (P:155) is named in the fix | ACCEPT; drops its own 5-on-4b set (conceded, INV-014) |
| E2 4b between 7 and 8 | ACCEPT; give 4b a body sentence saying why it sits there | ACCEPT | QUALIFY: heading `## Task 4b: ...` with body text (IMPL:71, :75); the heading should say it extends `conflicts.py` (cosmetic) |
| E3 AC split | QUALIFY: split the P:93 test bullet as well; `crash_resume_plan` (P:92) has no AC today; rename P:100 | ACCEPT; also closes INV-012 | QUALIFY: P:96-98 go to 4a; P:99's `prior_conflict_cycles` clause goes to 4a and the rest to 4b; split P:93; fix P:241 |
| E4 Task 3 on 1, 2 | ACCEPT | ACCEPT (closes INV-007) | ACCEPT (Low; latent under document order) |
| E5 INV-006 regrade | QUALIFY: Low for 01/02/04/17/22; CF-03's header-match grep stays; Low holds only while no `independent`/`parallel-ok` marker exists | QUALIFY (concedes): Low, scoped to document-order execution; a graph-order executor re-opens the cards | QUALIFY: Low only while no parallel marker exists; only the edge part of CF-03 is lowered |

Citation check by the orchestrator: A and C report that the probe's "IMPL:77" is actually IMPL:79. A direct read confirms that IMPL:79 is "Ignore MDTM fields (`depends-on`, ...) except `independent`" and IMPL:97 is "Default sequential in source order". A grep of P for `independent|parallel` returns no match.

## Round 3: Final Arguments

Round 3 skipped: depth=standard

## Scoring Matrix

Taxonomy levels are auto-tagged from each point's diff-analysis text. The priority is L3 > L2 > L1, and L2 is the fallback. Position notation: Round 1 and Round 2 positions are listed as A / B / C, giving each advocate's preferred card or stance. "Agreed" follows the protocol: unanimous, or at least 2 of 3. A point with no recorded position from any advocate is unresolved. A point lost by one card whose advocate conceded, with no advocate dissenting, is recorded as an uncontested concession.

| Diff Point | Level | R1 (A / B / C) | R2 (A / B / C) | Agreed | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 bundling granularity | L2 | split / split / split | split / split / split | Yes | Consensus (one defect per row; no card) | 80% | Every final table splits A-8, A-6, A-10, Q-5, Q-6, F-1 and F-5 into separately rated CF rows. B criticised A-8's bundling (R1) and A conceded the framing (R2). |
| S-002 severity distribution | L2 | A / C / C | C / C / C | Yes | C | 80% | A conceded the scale in R2 (X-005). No card or advocate argues for High. R-INV lowered the edge findings to Low under a qualifier, which keeps one scale. |
| S-003 class vocabulary | L2 | A / C / C | C / C / C | Yes | C | 75% | All three R2 tables keep `necessary` for CF-21. C's first use (F-9) and B's CF-05 use were withdrawn. |
| S-004 finding order | L1 | none / none / none | none / none / none | No | Unresolved (not debated) | 50% | No advocate argued it. Presentation only. |
| S-005 evidence paths, Verify clauses | L1 | none / none / none | none / none / none | No | Unresolved (not debated) | 50% | No advocate argued it. |
| S-006 provenance header | L1 | none / none / none | none / none / none | No | Unresolved (not debated) | 50% | Orchestrator-written header. No advocate argued it. |
| C-001 CF-01 Task 13 edge | L3 | C / C / C | C / C / C | Yes | C | 95% | Chain 11 → 12 → 13 rooted on Task 10 (P:207, P:215). A conceded "optional" was too soft. R-INV (E5): Low under the document-order qualifier. |
| C-002 CF-03 Task 16 edge | L2 | C / C / C | C / C / C | Yes | C (plus B's header grep) | 90% | Task 16 on 2, 6, 13 (S:1070 names both functions). A conceded Medium in R2. R-INV lowered the edge part only; the grep stays (A, C). |
| C-003 CF-04 Task 20 closure | L2 | A/B / A/B / C | A/B / A/B / A/B | Yes | A/B | 95% | C conceded "9 suffices" (R2). Final fix 20 on 6, 9, 18, 19. R-INV: Low under the qualifier, which matches the original A/B severity. |
| C-004 CF-05 resume tests | L3 | A / C / C | A/B set / A/B set / C set (dissent) | Yes (R2 majority; unanimous after R-INV) | C (F-1b split and placement), amended | 90% | R-INV: A/B set plus 5 → 4a and 9 → 4b; 4b sits between Task 7 and Task 8, as F-1 itself proposed. All three accept in `round-inv-*`. |
| C-005 CF-06 Task 4 split line | L2 | A / C / C | C / C / C | Yes | C | 95% | Split along the resume boundary. A adopted C's split in R2. |
| C-006 CF-08 staging omission | L2 | A / A / A | A / A / A | Yes | A | 95% | Explicit `git add` of exact paths plus `.dev/tasks`, with an AC on `git diff --cached --name-only`. B adds the vacuity note (U-014). |
| C-007 CF-11/12 skip and identity | L3 | A / B / B | B / B / B | Yes | B | 95% | S:1316 requires both. A conceded Medium (R2). |
| C-008 CF-13/14 clause and range | L1 | spec defect / drift / drift | spec defect / spec defect / spec defect | Yes | A | 90% | P:53 copies S:731's `:86-99`. B and C conceded the class in R2. The winner changed once (R1 drift majority to R2 spec defect); no oscillation. |
| C-009 CF-15 make-test residual | L2 | A / B / A | A / A / A | Yes | A (severity) with B's fix | 90% | Import failure already breaks every `tests/pr_submit` test; only the CLI path is unexercised. B conceded Low (R2). |
| C-010 CF-16 authorized additions | L2 | A/C / A/C / A/C | A/C / A/C / A/C | Yes | A/C | 90% | All R2 tables: "None". C's optional "net +15" was not carried. |
| C-011 citation grounding | L1 | none / concede / none | none / concede / none | Yes (uncontested concession) | A/C | 80% | B conceded the Q-1 mis-citation (S:1392, actually S:1408). |
| C-012 confidence calibration | L2 | none / concede / none | none / concede / none | Yes (uncontested concession) | C | 75% | B conceded overconfidence (0.87 vs 0.78). C's self-report equals its calibration (0.82). |
| C-013 summary caveats | L1 | none / none / B | none / none / none | No | Unresolved | 50% | Only C (R1, A-005 QUALIFY) says B's 21 unresolved unmapped-union INF rows remain open. A and B never addressed it. |
| X-001 class of CF-05 move | L3 | drift / necessary / drift | drift / drift / drift | Yes | A/C | 95% | S:1422 gives a spec-compliant placement. B conceded (R2). |
| X-002 make-test residual size | L2 | A / B / A | A / A / A | Yes | A | 85% | Same evidence as C-009. B conceded severity (R2). |
| X-003 E5/E12 split class | L2 | anchor gap drift / same / same | same | Yes | Consensus (C's finding, class drift) | 95% | The spec splits E5 and E12 itself (S:1416, S:1426). C conceded "necessary" (R1). |
| X-004 F-10 stricter edges | L2 | reject / reject / concede | same | Yes | Consensus (only 9 → 6 is stricter) | 95% | Spec step 3 = Tasks 3 + 4. C conceded (R1). CF-21 keeps 9 → 6 as necessary. |
| X-005 severity scale | L2 | A / qualify / C | C / C / C | Yes (from R2) | C | 85% | No majority in R1. A conceded the scale in R2. |
| A-001 Task 3 stands for step 3 | L2 | ACCEPT / ACCEPT / ACCEPT | ACCEPT / ACCEPT / ACCEPT | Yes | Consensus (calibrator finding CF-22) | 95% | P:184. R2 refines the edge to "Task 10 on 3, 4a". |
| A-002 name-match edge audit | L2 | ACCEPT / ACCEPT / ACCEPT | ACCEPT / ACCEPT / ACCEPT | Yes | Consensus | 95% | Method fix: expand spec case IDs and export lists into the functions they use, and compute closures from the plan graph. |
| A-006 spec column complete | L2 | QUALIFY / ACCEPT / QUALIFY | QUALIFY / QUALIFY / QUALIFY | Yes | Consensus (qualified) | 90% | The step 10 column is incomplete (S:1070 needs Task 6). The step 13 column is adequate (S:1400). |

Debate-performance tally (points won; a shared win counts for each card): A 8 (C-003, C-006, C-008, C-009, C-010, C-011, X-001, X-002); B 2 (C-003, C-007); C 11 (S-002, S-003, C-001, C-002, C-004, C-005, C-010, C-011, C-012, X-001, X-005). Six points went to a consensus position that no card held (S-001, X-003, X-004, A-001, A-002, A-006). Four points are unresolved.

### Unique contributions (informational; U-NNN are not in the convergence denominator)

| U | Card | Outcome |
|---|---|---|
| U-001 | C | Adopted as CF-17, reduced to the required Task 13 edge (C's own R1 concession) |
| U-002 | A | Adopted as CF-09, Medium |
| U-003 | C | Adopted as CF-18, Low |
| U-004 | C | Adopted as CF-20, relabelled drift |
| U-005 | C | Adopted as CF-19, Low |
| U-006 | A | Adopted as CF-10, Low drift |
| U-007 | A | Withdrawn by A; CF-07 kept as advisory |
| U-008 | A | Partly adopted: the "VG-2 not run" log line was carried; the P:19 reword was not |
| U-009 | C | Adopted (Task 16 on Task 6) |
| U-010 | B | Adopted (header-match grep in CF-03) |
| U-011 | B | Dropped (Task 9 import smoke and reflect test in Task 9; B conceded) |
| U-012 | C | Rejected (keep Task 9 → 6; CF-21 necessary) |
| U-013 | C | Not carried ("net +15" tightening) |
| U-014 | B | Adopted as the rationale in CF-08 |

### Unpromoted shared assumption refuted in the probe
A-003 ("the executor runs tasks in Depends-on order, possibly parallel") was STATED in F-4 and not promoted. INV-005 and INV-006 refute it for `/sc:implement` (IMPL:79, IMPL:97). All three advocates accepted the E5 regrade that follows from it.

## Taxonomy Coverage Gate

| Level | Points | Addressed in debate | Not addressed |
|---|---|---|---|
| L1 surface | 6 (S-004, S-005, S-006, C-008, C-011, C-013) | 3 (C-008, C-011, C-013) | S-004, S-005, S-006 |
| L2 structural | 17 | 17 | none |
| L3 state mechanics | 4 (C-001, C-004, C-007, X-001) | 4 | none |

All three levels have at least one addressed point after Round 1 and after Round 2. No forced round was triggered. Gate: PASS.

## Invariant Gate

| INV | Severity | Probe status | After the invariant-resolution round | Basis in `round-inv-*` |
|---|---|---|---|---|
| INV-001 | HIGH | UNADDRESSED | ADDRESSED by R-INV E1 | A, B and C all state "fully addressed": P:106 becomes "Task 4a", which removes the 4b → 5 → 4b cycle |
| INV-002 | HIGH | UNADDRESSED | ADDRESSED by R-INV E1 + E2 | A, B and C all state "fully addressed": 9 → 4b puts the planners in Task 9's closure (S:744), and 4b runs before Task 9 in document order |
| INV-005 | HIGH | UNADDRESSED | ADDRESSED by R-INV E2, conditionally | A, B and C all state "fully addressed". Condition (A, C): the 4b heading must physically move between Task 7 and Task 8, and must be `## Task 4b: ...` with body text |
| INV-006 | MEDIUM | UNADDRESSED | ADDRESSED by R-INV E5 (regrade with qualifier) | A, B and C QUALIFY: Low only while `/sc:implement` runs sequentially in document order with no parallel-marked set. CF-03's grep stays |
| INV-007 | MEDIUM | UNADDRESSED | ADDRESSED by R-INV E4 | A, B and C all ACCEPT "Task 3 depends on Task 1, Task 2" |
| INV-012 | LOW | UNADDRESSED | ADDRESSED by R-INV E3 | B: "also closes INV-012"; A and C QUALIFY with the P:93/P:99/P:100 split |
| INV-014 | LOW | UNADDRESSED | MOOT | C withdrew its 5-on-4b set, which was the only source of the stricter edge (B: "moot here") |

After the invariant-resolution round: HIGH UNADDRESSED = 0; MEDIUM UNADDRESSED = 0; LOW: INV-014 moot. Gate: PASS.

## Convergence Assessment
- Points resolved: 23 of 27
- Alignment: 85.2% (23 / 27 = 0.852)
- Denominator: S 6 + C 13 + X 5 + promoted A-NNN 3 = 27. U-NNN are excluded, as the formula specifies.
- Per round: Round 1 = 22 of 27 (81.5%; X-005 had no majority). Round 2 = 23 of 27 (85.2%). After the invariant-resolution round = 23 of 27 (85.2%; C-004 went from a majority to unanimous).
- Threshold: 80%
- Early termination: stable majority at or above the threshold for 2 consecutive rounds (Round 1 and Round 2), with all taxonomy levels covered. Convergence stayed blocked by the invariant gate until the invariant-resolution round.
- Status after Round 2.5: BLOCKED_BY_INVARIANTS (INV-001, INV-002, INV-005)
- Status after the invariant-resolution round: CONVERGED
- sc:reflect routing (0.75 or higher PASS, 0.60 or higher PARTIAL, below that FAIL): 0.852, so PASS
- Unresolved points: S-004, S-005, S-006, C-013

## Final Metadata

```yaml
depth: standard
convergence_threshold: 0.80
convergence_score: 0.852            # 23 / 27
status: CONVERGED
rounds:
  - {id: R1, type: advocate statements, execution: parallel, files: round1-advocate-{A,B,C}.md, convergence: 0.815}
  - {id: R2, type: rebuttals, execution: sequential A>B>C, files: round2-advocate-{A,B,C}.md, convergence: 0.852}
  - {id: R2.5, type: invariant probe, file: invariant-probe.md, result: "BLOCKED_BY_INVARIANTS (INV-001, INV-002, INV-005)"}
  - {id: R-INV, type: extra invariant-resolution round, trigger: "invariant gate block after R2.5", files: round-inv-advocate-{A,B,C}.md, result: "R-INV accepted or qualified by all three; INV-001, INV-002, INV-005 fully addressed; gate cleared", convergence: 0.852}
  - {id: R3, type: final arguments, executed: false, log: "Round 3 skipped: depth=standard"}
extra_rounds: 1                     # R-INV, outside the standard-depth schedule
taxonomy_gate: PASS                 # L1 6 / L2 17 / L3 4 points; every level addressed
invariant_gate: PASS                # after R-INV: 0 HIGH, 0 MEDIUM unaddressed; INV-014 moot
unresolved_points: [S-004, S-005, S-006, C-013]
recording_notes:
  - "B's R1 point table labels are offset by one for diff points C-003..C-005; scored by content."
  - "Probe cites IMPL:77; the cited text is at IMPL:79 (verified by direct read)."
```
