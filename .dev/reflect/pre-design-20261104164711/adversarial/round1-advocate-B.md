# Round 1 — Advocate B (qa card, variant-2-original.md)

Verdict unchanged: ready-with-fixes. Disputed citations re-verified.

## Steelman of the other cards

Card A is strongest on AC observability: U-002 (`git ls-files -s` cannot show 100755 for an unstaged new file) and U-006 (pinned-phrase ACs have no failing command until Task 18) make an AC that cannot fail a false green — my home turf, missed. Conceded. Card C owns structure: F-2, F-7, F-8, F-9 are real coverage gaps; U-001 is the highest-value finding here and I adopt it. Conceded weaknesses of mine: overconfident (0.87 vs 0.78, C-012); Q-1 cited S:1392 for the make-test line, actually S:1408 (C-011); and I shared the A-002 blind spot that missed CF-22.

## Where my card is right (re-verified)

- Q-5 is the best severity call on the table. S:1316 (read this turn) requires "a fixed author and committer" and "Each real-git module begins with a capability skip"; P:29 carries neither and Task 19's skip covers only absent `uv`. Card A bundled both into low-severity A-8 (C-007); the named breakage (F9, F10, X1, X3 do real commits) is the QA-correct framing.
- Q-6 verified: S:728 requires "plus the two conflict-cycle events `sync_started` and `sync_concluded`" in both docstrings, absent from P:51; the loop-guard list ends at line 103, not 99.
- Q-7: without staging, P:307's "no staged `.claude/`" check is vacuously true; A-6b's fix is stronger — adopt it.
- Q-4's grep (fenced usage line matches the script header) catches ref/script drift at Task 16, not Task 18.

## Shared assumptions — all three ACCEPTED, re-verified

- A-001: P:184 (Task 10 → Task 3 only); Tasks 11/18 (S:1388, S:1390, S:1345) call Task 4 functions with no path to Task 4. Root fix — Task 10 "Depends on: Task 4" (spec-faithful: step 9 depends on step 3 = Tasks 3+4) — subsumes CF-02.
- A-002: my audit matched function names in task text; Tasks 11/18 consume Task 4 only via spec case IDs. The method must add "expand spec case IDs to their asserted functions".
- A-006: step 10 depends on 9 only, yet ci-poll item 4 (S:1070) documents `expect_checks_after_push` (Task 6) and X1 replays step 11 (S:303). The spec column is incomplete; F-2/F-3's content edges are right.

## High/Medium points, U-001, X-001..X-005

| Point | Preferred card | Reason |
|---|---|---|
| S-002 | C | CF-09, CF-11, CF-12 are test-breaking, not cosmetic |
| C-001 | C | Sibling appends to one file is the execution hazard; chain 11→12→13 |
| C-002 | C | Task 16 needs 6 and 13 (S:1070); keep my header grep |
| C-004 | B/A | Fix "6, 9, 18, 19"; F's "9 suffices" is implicit, survives worse |
| C-005 | C | F-1b placement after the fold; my card was silent — conceded |
| C-006 | C | Split along the resume boundary, not router-vs-rest |
| C-007 | B | Medium with named breakage (Q-5) beats A's bundled low |
| C-009 | B/F | Medium stands, F's scope; A's "blast radius smaller" covers import failure only, not the unexercised CLI path |
| U-001 | C | Adopt verbatim: Task 19 → 5, 6, 8, 11, 12, 13, 14 |
| U-002..U-005 | A, C, C, C | All adopted; U-003, U-005 were my QA misses |

X-001 QUALIFY: documented in P:93, so "necessary deviation", M; fix = `rebuild_state()` state. X-002 side with B/F: import breakage is covered by tests/pr_submit, the CLI path is not; medium. X-003: split is spec-conformant; the real defect is the missing anchor (drift). X-004: F-10 partly false; only Task 9→6 is stricter. X-005 QUALIFY: edge-to-edit-target M (silent wrong-state edits) vs edge-to-gate L (fails loud); CF-04 upped to M.

## Canonical findings — severity / class / fix

- CF-01: M / drift / chain 11→12→13 rooted on Task 10.
- CF-02: M / drift / Task 15 → 4, 12; subsumed by A-001.
- CF-03: M / drift / Task 16 → 2, 6, 13 + Q-4 grep.
- CF-04: M / drift / Task 20 → 6, 9, 18, 19.
- CF-05: M / necessary deviation / `rebuild_state()` state or rows to Task 8.
- CF-06: M / necessary / split 4a/4b.
- CF-07: L / drift / per-family log sections.
- CF-08: M / drift / staging step + AC on `git diff --cached --name-only`.
- CF-09: M / drift / `test -x` in Tasks 10-12.
- CF-10: L / drift / per-task grep artifacts.
- CF-11: M / drift / capability-skip clause in Task 19.
- CF-12: M / drift / fixed author/committer in TL:29.
- CF-13: L / drift / quote the S:728 clause.
- CF-14: L / drift / cite loop-guard.md:86-103.
- CF-15: M / authorized / add tests/cli/reflect/test_contract_status_cli.py to Tasks 9, 20 + "VG-2 not run" log line.
- CF-16: L / authorized / no change; optionally "net +15".
- CF-17: M / drift / Task 19 → 5, 6, 8, 11, 12, 13, 14.
- CF-18: M / drift / force-push scan in Tasks 11, 12 (S:1424).
- CF-19: L / drift / C1-C4 without `--pr`; C4 asserts stderr names the SHA.
- CF-20: L / drift / F-9's anchors and final-substring AC.
- CF-21: L / drift / keep Task 5's edge; optionally drop Task 9→6.
- CF-22: M / drift / Task 10 "Depends on: Task 4".

Net: toward C on graph structure and A on AC observability; I hold CF-11/12 severity and CF-15's medium, and concede CF-05/06 and U-001/U-003/U-005 as misses.
