# Re-review 2 (of TASK-WF-implementDocsDes-20261120-020554), reflect-reviewer opus, verdict not-ready

Prior blockers B1 to B12: 11 resolved, B2 partly open (Medium N1: the rewritten confinement test must also allow section 17.6, where the grader row at reflect SKILL.md:1918 sits).
New blocking finding: N2 (Safety), Wave 5 replaces the whole contract file, so `review_verdict: FAIL`, `supersedes`, `finding_counts` written by `place` and `mark` could be lost and /sc:implement would accept a plan with open blockers. Repaired in cycle 2.
Medium and Note findings left unrepaired (follow-up candidates):
- N1 allowed-section list misses 17.6; N12 the "Contract version is v1.8.0" sentence is in 9.1 (SKILL.md:877), not 9.4.
- N3 `mark` is not the only writer of `superseded_by` and `fix_cycles`; appended lines can duplicate keys.
- N4 appending to `unresolved` fails when it is `[]` or not the last key (second cycle, `--revise`).
- N5 the "already has a SUPERSEDED line" match must be case-insensitive; three of the seven contracts use lowercase.
- N6 test text still says `place` picks a suffixed id; `reserve` does now.
- N7 `reserve` leaves an empty package folder if a later step fails; `restore` only undoes `archive`.
- N8 `mark` runs before the re-review in the listed order; it must follow the last re-review.
- N9 the regenerate route has no stated use of `place`.
- N10 the Agent tool name (`Task` in other skills); N11 the mirror test only collects `*.md`.
