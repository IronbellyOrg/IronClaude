# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe; Round 3 skipped: depth=standard)
- Convergence achieved: 100% diff-point alignment; status BLOCKED_BY_INVARIANTS (INV-001, INV-003)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (Mode A, one advocate per card, current model; read-only general-purpose agents)
- Agent failures: none
- Per-round source files: debate/round1.md, debate/round2.md, debate/scoring.md (concatenated below)

## Round 1: Advocate Statements (verbatim summaries of each advocate's returned statement)

Plan = `TASK-WF-spec-20261108-181547.md`, src.md = `source.md` (both in `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/`).

### Variant 1 Advocate (analyzer card, calibrated C 0.76)

**Position**: V1 alone found the only defect that meets the strictest blocking test, two ACs that cannot both pass (C-001), and has the widest coverage (9 findings, 8 confirmed). Weak on classification (none given), under-graded FR-8 protection, missed C-010.

**Steelman V2**: fail-closed focus; src.md:183 makes exit 2 part of the interface; src.md:199 promises byte-identity on any failure; plan:87 puts readback and two metadata writes after `os.replace` with no rollback, a real hole nobody else saw; plan:61 does bring in the source test bullets by reference.
**Steelman V3**: line-23 finding cites the plan's own constraint "does not support --unattended" (plan:26) while spec-panel.md:23 keeps flags defined only at 455-459; FR-8 point strong because plan:55 caps the recorded label at "CRITICAL, MAJOR, MINOR or unknown", dropping the FR-8 tag that src.md:39, 218, 231 and :140 rely on.

**Strengths**: (1) C-001 verified: spec-panel.md:220 has `src/superclaude/...`; Task 7 differences (plan:134) do not touch 220; plan:147 demands both pins. (2) Unique cheap finds C-007, C-009. (3) C-004 grounded: plan:74 + :104 vs :115.

**Weaknesses in others**: V2 self 0.94 vs calibrated 0.75; misses C-001, C-002, C-004, C-005; QA-001 blocking overstated (FAIL already forced, plan:101, 114); QA-002 labelled drift though spec has same gap (src.md:44). V3: R3-F1 overstated, guard keys on the heading (WORKER-CONTRACT case 2 refuses), S1 briefs never pass the flag; a state.json flag is not strictly required (class column of fix-list.md, read by check, can carry protection); misses C-001.

**Concessions**: C-005 raised to blocking (narrow): explicit label set plus AC let an implementer parse `MAJOR (FR-8 GAP)` as non-blocking MAJOR, class minor-only, revertable. C-010 real. C-011 drop. R1-F9 split into C-006 and C-007. No classification given.

**Shared assumptions**: A-001 QUALIFY (Unattended ruling mechanically forced anyway; T10 ruling uncited in plan). A-002 ACCEPT. A-003 QUALIFY (inherited defect counts for severity when ACs are unsatisfiable; classify inherited / needs necessary deviation, never drift).

**Structure**: S-001 flat schema + V2 `category` + list evidence; S-002 combine `actively_checked` + `checked_sound`; S-003 one finding per root cause (~10).

| Point | Keep | Severity | Classification |
|---|---|---|---|
| C-001 | keep | blocking | necessary deviation required (spec-inherited, src.md:237 vs :239) |
| C-002 | keep (V3 fix) | minor | drift |
| C-003 | keep | minor | drift |
| C-004 | keep | minor | drift (internal inconsistency) |
| C-005 | keep | blocking (narrow) | drift |
| C-006 | keep | minor | drift |
| C-007 | keep | minor | drift |
| C-008 | keep (note) | minor | authorized expansion |
| C-009 | keep | minor | latent regression |
| C-010 | keep | minor | inherited spec gap |
| C-011 | drop | - | - |
| X-001 | minor | | X-002 minor; X-003 blocking (narrow); X-004 C-003 drift, C-010 inherited; X-005 minor authorized |

### Variant 2 Advocate (qa card, calibrated C 0.75)

**Position**: two real, confirmed findings; QA-002 (C-010) is the only apply-integrity finding and stays blocking; QA-001 conceded to minor; V2 missed C-001 and has thin coverage (0.65).

**Steelman V1**: widest coverage; alone found C-001 (src.md:237/239, plan:147 vs spec-panel.md:220, plan:134); calm severities; honest INFERRED tags.
**Steelman V3**: highest calibration; R3-F1 grounded (spec-panel.md:23 vs 455-459; Task 8 checks only the heading); R3-F2 correctly notices state.json records no FR-8/FR-9 marker (plan:55, 58).

**Strengths**: (1) C-010 concrete failure: S replaced, apply-log missing; re-run misses "already applied", re-runs check, K1 fails on S's changed sha256 (src.md:212), state.json records `skipped(check failed)` while S is modified; Task 7 ships command text promising "leaves the specification byte-identical" (src.md:199): wrong behaviour. (2) only card with a `category` field. (3) quoted-line evidence.

**Weaknesses in others**: R3-F2 overreaches: Task 2 applies the class rule by reference (plan:56), which makes any FR-8/FR-9 hunk blocking-involved (src.md:39); K6 allows revert only on minor-only hunks (plan:74, src.md:218); so only the AC test is missing (plan:64 vs src.md:231). R3-F1 overrated: guard case 2 refuses; T08a has no flag (plan:202). R1-F8 speculative.

**Concessions**: QA-001 minor; spec self-contradicts (src.md:183 vs 2.7 item 4 at src.md:133); FAIL still forced (plan:101, 116). Missed C-001, C-002, C-004, C-006. QA-002 INFERRED; trigger is I/O failure.

**Shared assumptions**: A-001 QUALIFY (msg_7b27 cited plan:26 and independently checkable; msg_2000 only in orchestrator notes). A-002 QUALIFY (body directives bind too; body-incorporated + AC-omitted = minor; neither = real gap). A-003 ACCEPT (tag spec-inherited; fix goes to both documents).

| Point | Keep | Severity | Classification |
|---|---|---|---|
| C-001 | keep | blocking | drift (spec-inherited) |
| C-002 | keep | minor | drift (incomplete necessary deviation) |
| C-003 | keep | minor | drift (spec self-inconsistent) |
| C-004 | keep | minor | drift |
| C-005 | keep | minor | drift (AC omission) |
| C-006 | keep | minor | drift |
| C-007 | keep | minor | drift |
| C-008 | drop as defect, record | - | authorized expansion |
| C-009 | keep | minor | drift (inferred) |
| C-010 | keep | blocking | drift (spec-inherited) |
| C-011 | drop | - | - |
| X-001 minor; X-002 minor; X-003 minor; X-004 C-003 drift (spec self-inconsistent), C-010 drift (spec-inherited); X-005 authorized expansion | | | |

### Variant 3 Advocate (refactorer card, calibrated C 0.81)

**Position**: highest calibrated C and widest line-checked coverage; defends C-005 as blocking; concedes it missed C-001 and that C-002 drops to minor.

**Steelman V1**: broadest card; found the one mechanical contradiction (plan:147 both pins vs spec-panel.md:220; plan:134 does not touch 220).
**Steelman V2**: strictest evidence format and only `category` field; C-010 real (src.md:199 vs plan:87).

**Strengths**: (1) C-005: plan never says "FR-8"/"FR-9" (grep: no hit); plan:55, 58 record only "severity label (CRITICAL, MAJOR, MINOR or unknown) and the blocking flag", so `MAJOR (FR-8 GAP), minor` collapses to a plain revertable minor id although src.md:39, 218 protect it; AC omits src.md:231 test. (2) C-002 recommendation more actionable. (3) C-006 tied to src.md:174 and Task 9 docs. (4) `actively_checked` names line ranges; clears T1 S2.

**Weaknesses in others**: V1 rates C-005 as test-only, missing the data-model gap at plan:55, 58; keeps unconfirmed C-011. V2: C-003 blocking overstated (plan:101); C-010 drift label wrong (spec has same omission); `actively_checked` passes C-005 by reference (plan:61) though AC plan:64 drops it.

**Concessions**: missed C-001 (blocking). C-002 minor (guard keys on section, WORKER-CONTRACT.md:17; no AC conflict; T08a never passes the flag). "K6 cannot refuse" too strong: K6 also checks the hunk class, and plan:56 brings in the class rule by reference including FR-8; the real defect is explicit lists omit the tag and no AC tests it. `--improve` exists in person mode (spec-panel.md:35); only `--unattended` and `--report-dir` are orphaned.

**Shared assumptions**: A-001 QUALIFY (only the Unattended ruling cited by id, plan:26; T10 uncited id, plan:193, 200). A-002 ACCEPT (severity then depends on likelihood and harm). A-003 QUALIFY (counts when ACs unsatisfiable; classify spec-inherited, not drift).

| Point | Keep | Severity | Classification |
|---|---|---|---|
| C-001 | keep | blocking | spec-inherited conflict; needs a deviation (owner call) |
| C-002 | keep (V3 fix) | minor | drift (authorized deviation only partly carried through) |
| C-003 | keep | minor | drift |
| C-004 | keep | minor | drift (inconsistency inside the plan) |
| C-005 | keep | blocking | drift |
| C-006 | keep | minor | drift |
| C-007 | keep | minor | spec-inherited |
| C-008 | drop as defect; record | none | authorized expansion |
| C-009 | keep | minor | regression risk |
| C-010 | keep | minor | spec-inherited gap |
| C-011 | drop | - | - |
| X-001 minor; X-002 minor; X-003 blocking (narrowed); X-004 C-003 drift, C-010 spec-inherited; X-005 authorized expansion | | | |

### Round 1 tally (orchestrator)

- Unanimous: C-001 blocking keep; C-002 minor; C-003 minor; C-004 minor; C-006 minor; C-007 minor (classification split); C-009 minor; C-011 drop; X-001, X-002, X-004 (C-003 = drift).
- Majority: C-005 blocking (V1, V3 vs V2); C-010 minor (V1, V3 vs V2); C-008 drop-as-defect, record as authorized expansion (V2, V3 vs V1 keep-minor-note); X-003 blocking (2/3); X-005 authorized expansion (all three agree on the class; V1 keeps a minor labelling note).
- Contested for Round 2: C-005 severity, C-010 severity, C-008 keep/drop, classification label for spec-inherited defects (C-001, C-007, C-010: "drift (spec-inherited)" vs "spec-inherited / necessary deviation required").

## Round 2: Rebuttals (sequential: V1, then V2 with V1's rebuttal, then V3 with both)

### Variant 1 Rebuttal (analyzer, C 0.76)
- V3's "test-only" criticism of C-005: conceded in Round 1; re-verified that the plan holds no "FR-8"/"FR-9" string (grep, no hit) and plan:55/58 record only "severity label (CRITICAL, MAJOR, MINOR or unknown) and the blocking flag". A state.json flag is one valid fix; the fix-list class column (plan:58, read by check at plan:74) is another.
- V2's "C-005 minor": REJECTED. plan:56 brings in the class rule by reference, but plan:55 narrows the input that rule needs: `MAJOR (FR-8 GAP), minor` is recorded MAJOR/non-blocking with no tag, prepare cannot tell it from an ordinary minor id, the hunk is minor-only and K6 (src.md:218) lets it revert. That reverts a fix on an id the spec says is "never closed" and breaks src.md:140. AC plan:64 lacks the src.md:231 test. Blocking (narrow).
- V2's "C-010 blocking": path real; NEW EVIDENCE: if `closed-minor.txt` is never written, `verdict` reads closed as empty (plan:101), a reverted R2-MAJOR non-blocking id is not held, and the owner count drops, against plan:21 ("nothing in the script lowers it"). Still minor: (a) only an I/O fault right after a successful write of S triggers it; (b) the plan follows the spec's own order (src.md:44), so both AC sets can pass; (c) a few-line fix. Top minor, fix required.
- C-008: drop as defect; record authorized expansion; the plan never cites msg_2000b167e322 (grep, no hit; T10 only at plan:199).
- Labels: "necessary deviation" where following the spec literally makes the plan fail; "drift (spec-inherited)" where the spec is silent and the plan carries the silence past its own stated intent. C-001 necessary deviation (spec-inherited); C-007 drift (spec-inherited); C-010 drift (spec-inherited).
- `--improve` is not orphaned (spec-panel.md:35, person-mode step 6).

| point | final severity | final classification |
|---|---|---|
| C-001 | blocking | necessary deviation (spec-inherited) |
| C-005 | blocking | drift |
| C-007 | minor | drift (spec-inherited) |
| C-008 | none (recorded) | authorized expansion |
| C-010 | minor | drift (spec-inherited) |

### Variant 2 Rebuttal (qa, C 0.75)
- QA-001 overstated: already conceded; C-003 minor (src.md:183 vs :133; FAIL forced at plan:101, :116).
- `actively_checked` wrongly passed C-005: CONCEDED. grep finds no FR-8/FR-9 in the plan; plan:55's list is the input the rule at plan:56 needs; "protection flows through the class" assumed prepare has the tag, and as written it does not.
- C-010 labelled drift although the spec shares the gap: CONCEDED; the plan follows src.md:44; the fix is a deviation the plan must add to honour src.md:199.
- V1 on C-010: ACCEPT minor; V1's owner-count strengthening stands; top minor, fix required (restore S from D/current-before-audit.md on any failure after the replace, or write the metadata before the replace).
- C-008: drop as defect, record authorized expansion; plan should cite msg_2000b167e322 at plan:193.
- Labels: a plan that copies a spec defect faithfully has not drifted; the remedy is a deviation it must add: C-001, C-007, C-010 = necessary deviation (spec-inherited). C-007: src.md:239 omits fix_audit.py, but the project CLAUDE.md rule covers every installed primitive and plan:182 installs it.
- NEW EVIDENCE: src.md:140, class A findings (0.5 critical+major per run, flg arm) are "protected by the FR-8 rule, so 0 reachable": the FR-8 case is on the measured S1 path, supporting C-005 blocking.

| point | final severity | final classification |
|---|---|---|
| C-001 | blocking | necessary deviation (spec-inherited) |
| C-002 | minor | drift |
| C-003 | minor | drift |
| C-004 | minor | drift |
| C-005 | blocking | drift |
| C-006 | minor | drift |
| C-007 | minor | necessary deviation (spec-inherited) |
| C-008 | none (recorded) | authorized expansion |
| C-009 | minor | drift |
| C-010 | minor (fix required) | necessary deviation (spec-inherited) |
| C-011 | dropped | - |

### Variant 3 Rebuttal (refactorer, C 0.81)
- V1 on C-005: ACCEPTED; drops the "must be a state.json flag" claim; either a protected flag or a fix-list class carrying the FR-8/FR-9 tag satisfies src.md:39, 218, provided a Task 2 AC tests the src.md:231 case.
- V2's src.md:140 strengthens C-005: wrong behaviour on the measured S1 path, not just a missing test.
- V1's C-010 evidence checks out: plan:101 reads closed as empty when closed-minor.txt is absent; K6 needs ids minor by blocking flag, not label, so `MAJOR, non-blocking` can revert; owner count drops against plan:21. I/O-failure only: minor, fix required.
- C-008: not a finding; record authorized expansion; cite msg_2000b167e322 at plan:193.
- Labels: sides with V2: "drift" means leaving the spec without authority; C-001, C-007, C-010 copy the spec faithfully, so necessary deviation (spec-inherited).
- NEW EVIDENCE (C-007): the plan's own rule at plan:29 covers "no installed primitive", and Task 11 installs fix_audit.py (plan:182); stays minor because plan:58 already requires a non-`src/superclaude` brief lookup.

| point | final severity | final classification |
|---|---|---|
| C-001 | blocking | necessary deviation (spec-inherited) |
| C-002 | minor | drift |
| C-003 | minor | drift |
| C-004 | minor | drift |
| C-005 | blocking | drift |
| C-006 | minor | drift |
| C-007 | minor | necessary deviation (spec-inherited) |
| C-008 | none (recorded) | authorized expansion |
| C-009 | minor | regression |
| C-010 | minor (fix required) | necessary deviation (spec-inherited) |
| C-011 | dropped | none |

## Round 2.5: Invariant Probe

See `invariant-probe.md`: 12 findings, 2 HIGH UNADDRESSED (INV-001, INV-003), which block convergence.

## Round 3

Skipped: depth=standard.

## Shared-assumption responses

| A-NNN | V1 | V2 | V3 | Outcome |
|---|---|---|---|---|
| A-001 owner rulings genuine and binding | QUALIFY (Unattended ruling mechanically forced anyway; T10 ruling uncited in plan) | QUALIFY (msg_7b27 cited plan:26 and checkable; msg_2000 only in orchestrator notes) | QUALIFY (only Unattended ruling cited by id) | Agreed QUALIFY: binding for classification; the plan should cite msg_2000b167e322 at plan:193 |
| A-002 severity judged against literal plan execution; AC is the guard | ACCEPT | QUALIFY (body directives bind too; AC-only omission of a body-incorporated rule is minor) | ACCEPT | Agreed (majority ACCEPT); V2 conceded in Round 2 that plan:55 narrows the incorporated rule, so C-005 falls on the "not delivered" side |
| A-003 inherited spec defects count against the plan | QUALIFY (counts for severity when ACs are unsatisfiable; classify inherited) | ACCEPT (tag spec-inherited; fix both documents) | QUALIFY (same as V1) | Agreed: counts for severity; classified necessary deviation (spec-inherited), never plain drift |

Omissions: none (every advocate answered A-001..A-003).

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | V1 = V3 (flat schema), plus V2 `category` and list evidence | 85% | All three proposed the same merged schema in Round 1 |
| S-002 | L1 | V3 `actively_checked` + V1 `checked_sound` | 80% | Unanimous combination |
| S-003 | L2 | V3 (one finding per cluster) | 85% | V1 conceded R1-F9 bundled two issues |
| C-001 | L3 | V1 | 95% | Unanimous blocking; spec-panel.md:220 vs plan:134, 147; all advocates conceded they missed it |
| C-002 | L2 | V3 fix, V1 severity (minor) | 85% | V3 conceded severity; guard keys on the heading (WORKER-CONTRACT case 2); `--improve` not orphaned (spec-panel.md:35) |
| C-003 | L3 | V1 = V3 (minor) | 90% | V2 conceded; FAIL still forced (plan:101, 114); spec self-inconsistent (src.md:133 vs 183) |
| C-004 | L3 | V1 = V3 (minor) | 75% | Unanimous minor; probe INV-008 argues the wrong-behaviour half is met on failed-audit paths (kept minor, noted) |
| C-005 | L3 | V3 | 85% | Unanimous blocking after Round 2 (V2 conceded); plan has no FR-8/FR-9 string; plan:55, 58 drop the tag; src.md:140, 218, 231 |
| C-006 | L2 | V3 | 85% | Fuller scope (docs/ and .dev/tasks, src.md:174) |
| C-007 | L2 | V1 | 85% | Unique to V1; plan:29 rule vs plan:147 list; plan:182 installs fix_audit.py |
| C-008 | L2 | V3 (recorded, not a finding) | 85% | V1 conceded in Round 2; authorized expansion; plan should cite msg_2000b167e322 |
| C-009 | L2 | V1 | 75% | Unique to V1; INFERRED; label regression (V1, V3) vs drift (V2) |
| C-010 | L3 | V2 (finding), V1/V3 (minor) | 80% | V2 conceded minor; V1's owner-count evidence (plan:101 vs plan:21) makes it top minor, fix required |
| C-011 | L3 | dropped | 90% | V1 conceded; calibrator not-confirmed |
| X-001 | L3 | V1 (minor) | 85% | Resolved with C-002 |
| X-002 | L3 | V1 = V3 (minor) | 90% | Resolved with C-003 |
| X-003 | L3 | V3 (blocking, narrowed) | 85% | Resolved with C-005 |
| X-004 | L3 | V2 = V3 (C-003 drift; C-010 necessary deviation, spec-inherited) | 70% | V1 held "drift (spec-inherited)" for C-010; 2/3 majority |
| X-005 | L3 | V3 (authorized expansion) | 85% | Resolved with C-008 |
| A-001 | L2 | all (QUALIFY) | 80% | Unanimous qualify |
| A-002 | L3 | V1 = V3 (ACCEPT) | 75% | Majority |
| A-003 | L3 | V1 = V3 (QUALIFY) | 75% | Majority; same practical outcome as V2 |

Classification outcomes with a 2/3 majority (dissent recorded): C-007 and C-010 necessary deviation (spec-inherited) (V1: drift (spec-inherited)); C-009 regression (V2: drift).

Taxonomy coverage: L1 2 points, L2 7, L3 13 debated; all levels covered; no forced round.

## Convergence Assessment
- Points resolved: 22 of 22 (unanimous 16, majority 6)
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: passed (L1, L2, L3 all covered)
- Invariant gate: BLOCKED (INV-001, INV-003 HIGH UNADDRESSED)
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement meets the threshold; convergence is not declared)
- Unresolved points: none among the 22 diff points; INV-001 and INV-003 remain open outside them
