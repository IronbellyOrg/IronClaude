### Variant A Rebuttal (opus:analyzer), Round 2

## Response to criticisms
Steelman: B's case is fair; A-F10 is wrong, A's first C-001 remedy would ship a forbidden path, A missed the heartbeat, and "cannot" overreached; on precision per finding B is better.

| Criticism | Response |
|---|---|
| A-F10 wrong | Conceded in full (source.md:163: duplicates ruled by a blinded analyst; plan :93 follows the spec). Drop A-F10. |
| A-F1 first remedy breaks the no-`src/superclaude` rule | Conceded in full; only the second remedy (matching B-F1) survives, and it is a content decision for the owner (new evidence 3). |
| A-F8 unverified/overstated | Partly conceded: the four S1 briefs checked are single-line files, so the line-pair clause of plan :177 holds for any edit; the content clause needs a mechanical method (reverse-substitute and `cmp`). Keep minor. |
| A-F4 "cannot" overstated | Conceded on the word; the defect is task ordering. Task 2's E-CAP on a fourth `begin` and Task 3's E-TERMINAL after a terminal decision target the same state (Task 3 :76: review 3 always terminal); order unspecified. |
| Missed heartbeat (C-007) | Conceded; B superior. `heartbeat` appears nowhere in the plan; source.md:144 requires it; plan :125/:172 condition only on spawning; :200 defines no smoke check covering it. |
| Missed Task 6 sweep conflict | Conceded. Plan :125 (sweep after any terminal close) vs :44 (review-1 PASS needs no sweep); neither matches source.md:28; B's single predicate is the right fix. |

## Updated assessment of Variant B
- B-F1: content and fix correct; class should be `necessary` (inherited from source.md:83 vs :124-125).
- B-F2: correct; cross-task addition A missed; class drift.
- B-F3: correct; strongest unique point.
- B-F4: a spec-internal contradiction (source.md:72 vs :157); the plan followed :157; minor, class `necessary` with an owner note.
- Coverage map: only positive coverage evidence, but its "points at the section" standard accepted INF-005/058/104 though plan :53 lets a `subprocess` git call through.
- Overall: precise but narrow; misses C-004, C-005, C-006.

## New evidence
1. `grep -n heartbeat` on the plan finds nothing (source.md:144 requires it).
2. S1 briefs T05, T06, T07, T09 are one line each (`wc -l` = 1).
3. `src/superclaude/templates/documents/release-spec-template.md` exists and installs to `~/.claude/templates/` (install_templates.py:4, :45) but differs from the `examples/` copy (`cmp` differs at byte 401, line 8): rewriting line 220 changes which template the agent reads, an owner content decision.
4. The spec's premise for C-004 is false: source.md:124 says "(that test scans all of `src/`)", but `_tracked_text()` (test_review_severity_rule.py:36-52) scans only `git ls-files`; the plan inherited the false claim.
5. E-CAP and E-TERMINAL collide on a fourth `begin` (plan :61, :68 vs :76); Task 2's E-CAP test passes only if E-CAP is checked first.
6. test_routing_refresh.py:33 and :647-648 re-confirmed; plan :155/:159 omit it.

## Updated per-point positions
| point | superior | reason |
|---|---|---|
| S-001 | B (qualified) | only positive coverage evidence; standard too loose |
| S-002 | A | three unique high-severity items remain after dropping A-F10 |
| S-003 | Equal | style |
| C-001 | Merge: A class, B remedy | `necessary`; keep the whole-file pin; rewrite line 220 under an owner decision |
| C-002 | B content, A class | single predicate fixes :44 and :125; k=1 tail minor; drift |
| C-003 | A | no AC; :53 accepts subprocess |
| C-004 | A (strengthened) | spec premise false |
| C-005 | A | routing test breaks |
| C-006 | A (ordering) | Task 2 needs Task 3; E-CAP/E-TERMINAL order unspecified |
| C-007 | B (strengthened) | heartbeat absent from plan |
| C-008 | B (weak; `necessary`) | spec-internal contradiction |
| C-009 | A | source.md:60; tied to C-006 order |
| C-010 | A (weak, verified) | one-line briefs |
| C-011 | A | untracked brainstorm files trip :207 |
| C-012 | B (by absence) | A-F10 refuted |
| C-013 | A | minor, accurate |
| C-014 | A | calibration |
| X-001 | A | covered means a check fails on violation |
| X-002 | A | `necessary` |
| X-003 | A | drift |
| (new) Task 6/Task 1 sweep conflict | B | only B found :125 vs :44 |

## Shared assumptions
- A-001: QUALIFY. Starts in the spec but blocks the plan (plan :132 and :144-145 vs :127); resolve by a recorded owner decision because the installed template differs; class `necessary`.
- A-002: QUALIFY. Static reading suffices for C-004/C-005 (re-read this round), not for C-007 runtime heartbeat survival.
- A-003: ACCEPT. Two AC that cannot both pass (:44 vs :125; E-CAP vs E-TERMINAL) fail mechanically; an executor picking a winner would be drift.

Checked: plan :40-90, :120-208; source.md:24-62, :118-126, :134-165; spec-panel.md:216-222; test_review_severity_rule.py:36-56; test_routing_refresh.py:30-35, :644-650; S1 brief line counts; both template copies. Wrote nothing; ran no tests.
