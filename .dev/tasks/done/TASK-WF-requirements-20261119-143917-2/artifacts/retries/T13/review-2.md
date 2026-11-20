037a20427733cd81a9a0cc2989110c4500579e1c
Review of Task 13 (re-review, scope: F1.1 plus any other design-doc sentence that contradicts the guard)

Earlier blocking findings
F1.1 resolved
  Evidence: docs/designs/sc-issue-launch-level-hook.md:172 now reads "`project item-list` and `project field-list` NONE; group `issue`, `label` or `project` ISSUE anywhere ... `pr create|edit|comment|ready` SUBMIT anywhere". The guard H3 rows are src/superclaude/hooks/scripts/launch-level-guard.sh:664 (project item-list/field-list allowed), :665 (issue/label/project give ISSUE), :666 (pr create|edit|comment|ready give SUBMIT). The order and the verbs match. The rest of the sentence still matches the guard (:658 api, :660 merge, :661 alias/extension, :662 and :663 NONE rows, :667 UNKNOWN in command position).

Other design-doc sentences checked against the guard
- docs/designs/sc-issue-launch-level-hook.md:96 (ISSUE blocked at all four levels) matches launch-level-guard.sh:815.
- :98 (message precedence, ISSUE after GHWRITE) matches the loop at launch-level-guard.sh:802.
- :110 (pattern row 20a) matches the H3 rows above.
- :244 (LL-ISSUE text) matches launch-level-guard.sh:74-77.
- :245 (LL-SUBMIT no longer says "or issue") matches launch-level-guard.sh:70-73.
- :108 and :109 (SUBMIT rows) are unaffected.
- docs/designs/sc-issue-launch-level-hook.md:516 "version: 1" is the pre-push hook stamp, a different stamp, so it is not stale.

Per-AC marks (only what the re-review scope lets me check; test files not re-read)
- scope (design doc agrees with guard H3): met for :172, :96, :98, :110, :244, :245 (see above); unmet for :174 (F2.1).
- T13.AC1: not re-assessed in this re-review (test files out of scope). Guard side verified: ISSUE:W|WA|F|FS ll_deny LL-ISSUE at launch-level-guard.sh:815, for-list at :802, read rows at :664, message at :74-77.
- T13.AC2: not re-assessed. Guard side: version stamp 2 per the diff for line 10, tamper token at launch-level-guard.sh:777.
- T13.AC3: not re-assessed. Guard side: coordinator-only pattern at launch-level-guard.sh:455.
- T13.AC4: not re-assessed (test suite and sync checks not run, read-only review).

Findings
F2.1 ac=scope at=docs/designs/sc-issue-launch-level-hook.md:174 anchor=src/superclaude/hooks/scripts/launch-level-guard.sh:777 chk=n,y,n,n family=design-doc-h3-stale fix=add `.config/superclaude` to the tamper-token list in the Tamper paragraph (and note the accepted over-match: any governed command whose text mentions that path is refused, reads included) : The Tamper paragraph lists the tokens T contains as `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config` or `.config/git`. The guard also refuses `*.config/superclaude*` (the guard's tamper case, line 777, added by Task 13). The design doc is the guard's stated design (guard line 3), so its list is now false against the live guard.
