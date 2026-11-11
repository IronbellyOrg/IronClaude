# Round 2: Rebuttals (sequential: V1, then V2 with V1's rebuttal, then V3 with both)

## Variant 1 Rebuttal (analyzer, C 0.76)
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

## Variant 2 Rebuttal (qa, C 0.75)
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

## Variant 3 Rebuttal (refactorer, C 0.81)
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
