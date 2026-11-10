# Round 1: Advocate Statements (verbatim summaries of each advocate's returned statement)

Plan = `TASK-WF-spec-20261108-181547.md`, src.md = `source.md` (both in `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/`).

## Variant 1 Advocate (analyzer card, calibrated C 0.76)

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

## Variant 2 Advocate (qa card, calibrated C 0.75)

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

## Variant 3 Advocate (refactorer card, calibrated C 0.81)

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

## Round 1 tally (orchestrator)

- Unanimous: C-001 blocking keep; C-002 minor; C-003 minor; C-004 minor; C-006 minor; C-007 minor (classification split); C-009 minor; C-011 drop; X-001, X-002, X-004 (C-003 = drift).
- Majority: C-005 blocking (V1, V3 vs V2); C-010 minor (V1, V3 vs V2); C-008 drop-as-defect, record as authorized expansion (V2, V3 vs V1 keep-minor-note); X-003 blocking (2/3); X-005 authorized expansion (all three agree on the class; V1 keeps a minor labelling note).
- Contested for Round 2: C-005 severity, C-010 severity, C-008 keep/drop, classification label for spec-inherited defects (C-001, C-007, C-010: "drift (spec-inherited)" vs "spec-inherited / necessary deviation required").
