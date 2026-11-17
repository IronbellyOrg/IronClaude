# Round 1 advocate 2 (variant 2)

## Position summary

Variant 2 is the only card that finds defects which would produce a wrong implementation on the release-critical paths: the resume path cannot run release, the cycle id has no shared-source contract, the fold test omits rows, and the Wave 3 test can be passed by an unconditional engage sentence. Its weaknesses are attributing spec-origin gaps to the plan, rating some verifiable text defects too low, and missing the low-level checkable mismatches that V3 found.

## Steelman

**V1 (analyzer).** V1 is the only card that finds the release-path risk where a failed engage leaves the PR in RELEASE_PENDING with an undefined HOLD consequence (plan 70; spec 138, 199). It also finds that the Task 11 criterion (plan 169) is satisfied by empty stub tests, which is the most serious verification gap in the plan. It catches two owner-decided items that no other card covers: the PR body and the opening run's `--merge-guard off` (spec 326), and the failed-release return path (spec 201).

**V3 (refactorer).** V3 checks the plan's mechanical text against its own rules: the prefix-only byte-identity check against O4 (plan 154; spec 342), Depends-on completeness under spec 363, the Phase value contract (plan 56 vs plan 90), the plan-invented "non-goals" label (plan 25), and `git status` never listing ignored mirrors (plan 200). Each of these would cause rework during implementation. V3 verified every one of them against the file.

## Strengths claimed

1. **Resume path cannot execute row 4.** `release_decision` needs `target_sha` and `applied_edits` (spec 107-109). `resume_decision` takes neither (spec 109, 166; plan 70), and the folded state holds no `target_sha` (spec 189-191). Only V2 shows this. Part of the root cause is spec-origin, see Concessions.
2. **Wave 3 test is passable by a wrong implementation.** Plan 153 says an unconditional engage sentence must fail, but the test checks only that the trigger phrase and "once per cycle" are present. Only V2 identifies this.
3. **Fold coverage is overstated.** Plan 60 claims "every row" of spec 4.2, but omits `settled(ready, failed)`, `settled(any, skipped, user_override)`, and both `changed` variants. V2 is the only card to verify this.
4. **Cycle id is an unresolved contract.** Spec 251 requires one id shared by guard, push triad and `rereview_requested`. Plan 37 accepts "no id minted today", and plan 127 asks only that the mint point be named. No criterion checks equality or off-mode invariance.
5. **autoMergeRequest conversion is unspecified.** Plan 111 checks only the key, while spec 230 shows a boolean. V2 correctly labels the gh shape as unverified offline.

## Weaknesses identified in others

1. **V1: severity without gate.** All seven V1 findings are non-blocking (`"blocking":false` throughout), yet F2 and F5 describe the plan as unimplementable or unverifiable. Its severity labels and gate outcome do not match.
2. **V1 F4 overstates the direct path.** It says edits may proceed unguarded after a failed engage. Spec §3 ("Engage fails") halts before any edit. The gap V1 is pointing at exists only on the resume path (row 8), and it is stated too broadly.
3. **V3: "covered with no gap" is wrong.** V3 marks the `not_applied` fold in both directions as covered. Plan 60 tests only the HELD outcome for a ready request. The RELEASE_PENDING return in spec 201 is untested, as V1 notes.
4. **V3: misses the state-mechanics cluster.** It does not raise the FR-16 retry (plan 124, 169), the cycle id (spec 251) or the resume inputs (spec 109). Its C-016 finding is correctly labelled as rework, but the cluster it omits would produce wrong behaviour.
5. **V1 and V3 both miss the Wave 3 test defect** (plan 153), which only V2 finds.

## Concessions

1. **F1 and F2 are largely spec-origin.** Spec 109 and 166 define the resume inputs without `target_sha`. Spec 315 names the retry only in a test name. The defect belongs in the spec, and V2 should not have rated it as a plan MAJOR.
2. **C-001 is underrated.** V1's MAJOR is right: plan 137-140 cannot pass a correct bullet, and V2's MINOR undersells it.
3. **C-006 is underrated.** A prefix check cannot satisfy O4's pinned-text requirement (spec 342). V3's MAJOR is right.
4. **C-020 and X-005 are overstated.** Plan 73 and 172 already prove that engage is a no-op at ordinal 2 and with `off`. Only the flag-parse inertness is missing.
5. **Coverage gap.** V2 misses C-011 to C-018, including the PR-body task (C-017) and the failed-release return (C-018).
6. **Grounding caveat.** The tree already contains the feature, so V2's "symbols exist" check says nothing about the pre-build claims in O1.

## Shared assumptions

- **A-001: QUALIFY.** The diff marks this UNSTATED, but spec §10 line 366 states it: fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules each need a criterion "a wrong implementation would fail". It is spec-stated for those four rule families only. Extending it to every criterion, as V2 does for Task 10 and Task 11, is an inference and should be labelled as one.
- **A-002: QUALIFY.** The spec contradicts itself at line 241: the Wave 0 bullet must "contain no L3 or draft condition", yet it must print the "at L3" off line. Plan faults should be measured against the spec only where the spec is unambiguous. Where the spec is inconsistent (241, 138, 199, 109), the finding should be tagged spec-origin and routed to the spec. V2's F1 and F2 need that tagging.

## Per-point table

| Point | Level | Superior | Reason |
|---|---|---|---|
| S-001 | L1 | V2 | Blocking set tracks implementability; still over-attributes spec gaps |
| S-002 | L1 | Tie | Counts measure volume, not verdict quality |
| S-003 | L1 | Tie | Layout only |
| C-001 | L1 | V1 | MAJOR correct: plan 137-140 cannot pass a correct bullet |
| C-002 | L3 | Tie | Both MAJOR; V2 adds the non-output value point |
| C-003 | L2 | V2 | Adds the off-mode invariance spec 251 implies |
| C-004 | L3 | V1 | Names the undefined HOLD consequence on resume |
| C-005 | L2 | V1 | Stub-passing criterion (plan 169) outweighs case omissions |
| C-006 | L1 | V3 | Prefix-only check against O4 is MAJOR |
| C-007 | L2 | V3 | Lists Tasks 9, 10, 12, 13 as missing dependencies |
| C-008 | L3 | V2 | Only card on autoMergeRequest conversion (plan 111, spec 230) |
| C-009 | L2 | V2 | Only card showing plan 153 accepts an unconditional sentence |
| C-010 | L3 | V2 | Resume inputs missing; partly spec-origin |
| C-011 | L1 | V3 | Spec has no non-goals section; plan 25 misattributes |
| C-012 | L1 | V3 | `git status --short` never lists ignored mirrors (plan 200) |
| C-013 | L2 | V3 | Phase values undefined in Task 3 (plan 56) vs lowercase (plan 90) |
| C-014 | L1 | V3 | `file:NNN` ban (plan 124) has no check |
| C-015 | L1 | V3 | Wave 8 test checks phrase only; Wave 6 checks order |
| C-016 | L2 | V3 | Plan 124 omits git write verbs that plan 22 and spec 255 require |
| C-017 | L2 | V1 | PR body and opening-run flag have no producing task |
| C-018 | L3 | V1 | RELEASE_PENDING return (spec 201) untested |
| C-019 | L3 | V2 | Plan 60 says "every row" and lists fewer |
| C-020 | L2 | V1 | Plan 73 and 172 already cover inertness behaviour |
| X-001 | L1 | V1 | Same as C-001 |
| X-002 | L1 | V3 | MAJOR correct under O4 |
| X-003 | L3 | V1 | Resume HOLD (row 8) has no defined SKILL action; V2 is right only on the direct halt |
| X-004 | L2 | V1 | Stub pass is the real unpassable criterion |
| X-005 | L2 | V1 | Largely covered by plan 73 and 172 |

DONE: Read all six files. Checked V2's F1, F4, F11 and C-010 against plan and spec lines.
NEXT: Adjudicator should tag V2's F1 and F2 as spec-origin and route them to the spec, not the plan.

Not checked: gh's `autoMergeRequest` JSON shape (offline). Risk: the line citations come from this session's reads of the files.
