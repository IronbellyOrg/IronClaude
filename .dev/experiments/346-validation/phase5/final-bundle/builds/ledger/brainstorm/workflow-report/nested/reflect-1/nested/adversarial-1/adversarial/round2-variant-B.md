### Variant B Rebuttal (opus:qa), Round 2

## Response to criticisms
Steelman: the criticisms are fair; B trusted the spec's claims about the repo and accepted "points at the section" as coverage, so it missed C-004, C-005, C-006, and inflated class and confidence.

| Criticism | Response |
|---|---|
| B-F1/B-F2 misclassified as regression | Conceded. B-F1 `necessary` (source.md:83 vs :124; spec-panel.md:220 outside every changed block). B-F2 `drift` (plan :44 drops "with the document unchanged", source.md:28). Both stay blocking. |
| Overconfident (0.92 vs 0.72) | Conceded; 0.72 is right. |
| Missed C-004, C-005, C-006 | Conceded in full; re-checked all three. B took source.md:124 "(that test scans all of `src/`)" on trust. |
| X-001 too loose | Conceded. Covered only when an AC would fail on violation; plan :53 checks imports only. INF-005/058/104 become true gaps (minor). Relabel B's map "referenced" vs "checked". |
| B-F4 thin | Conceded mostly: spec-internal gap (source.md:72/:227 vs :157); plan :93 followed :157; minor owner note, not drift and not strictly `necessary`. |

## Updated assessment of Variant A
- A-F2 (C-004): strengthened; Task 7 (plan :140-145) drops two assertions source.md:124 requires; `drift`.
- A-F3 (C-005): accept; `necessary`, owner decides.
- A-F4 (C-006): accept as ordering; without `verify` the loop ends at review 2 either way; plus the E-CAP/E-TERMINAL collision.
- A-F1: accept class `necessary` and only the second remedy.
- A-F5, A-F7: accept. A-F6, A-F9, A-F11: accept as minor. A-F8: low value, verified. A-F10: withdrawn, agreed.
- Citation precision: "review 3 always terminal" is plan :79 and source.md:27 (A cited Task 3 :76 and source.md:79, which are a blank line and "All additive"); claims right, lines off.

## Check of A's new evidence
| # | Claim | Verdict | Check |
|---|---|---|---|
| 1 | heartbeat absent from plan | Accept | `grep -ni heartbeat` empty; plan :172/:200 never define the smoke check |
| 2 | S1 briefs one line each | Accept | `wc -l` = 1 for T05, T06, T07, T09 |
| 3 | installed template differs | Accept | templates copy 8944 bytes vs examples 8997; `cmp` differs byte 401 line 8; install_templates.py:4, :45; spec-panel.md:284, :292 name the template by bare filename |
| 4 | spec premise false | Accept | test_review_severity_rule.py:36-52 `git ls-files`; Constraints :28 never stages src/ |
| 5 | E-CAP/E-TERMINAL collide | Accept (narrower) | plan :61, :68, :79; pin the order or let the test accept E-TERMINAL |
| 6 | routing test breaks | Accept | :33; :646-648 (active size 43); plan :155/:159 omit it |

## Updated per-point positions
| point | superior | reason |
|---|---|---|
| S-001 | B (qualified) | only positive coverage evidence; relabel referenced vs checked |
| C-001 | Merge: A class, B remedy | keep whole-file pin; rewrite line 220 under an owner decision naming the template; exclude and declare it |
| C-002 | B content, A class | one skip predicate fixes :44 and :125 |
| C-003 / X-001 | A | covered means a check fails on violation |
| C-004 | A (strengthened) | spec premise false; drift |
| C-006 | A (ordering) | plus E-CAP/E-TERMINAL |
| C-007 | B (strengthened) | heartbeat absent; smoke check undefined |
| C-008 | B (weak; owner note) | spec-internal gap |
| C-010 | A (weak; verified) | reverse-substitute and cmp |
| C-012 | B (by absence) | A-F10 refuted |
| C-014 | A | calibration |
| X-002, X-003 | A | conceded |
| Task 6/Task 1 sweep conflict | B | only B found it |
| Spec factual premises (new) | A | spec claims about the repo must be re-checked |

## Shared assumptions
- A-001: QUALIFY. Blocks the plan (plan :132/:144 vs :127/:145; Constraints :25 too); needs an owner decision because the templates differ; `necessary`.
- A-002: QUALIFY. Enough for the two deterministic cases; not for C-007 runtime or the E-CAP/E-TERMINAL order in unwritten code.
- A-003: ACCEPT. Three AC pairs cannot both pass (:44 vs :125; E-CAP vs E-TERMINAL; :132 vs :145); the executor must report, not pick.
- New unstated shared assumption: the plan may cite the spec's claims about repo behaviour without checking them; disproved by item 4.

Not checked: T07/T09 content, T08/T10 line counts, runtime behaviour. Ran no tests; wrote nothing.
