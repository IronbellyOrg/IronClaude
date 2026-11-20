037a20427733cd81a9a0cc2989110c4500579e1c
Review of Task 13 (repair re-review, scope: F2.1 plus every design-doc sentence on tamper tokens, gh classes or message precedence)

Earlier blocking findings
F2.1 resolved
  Evidence: docs/designs/sc-issue-launch-level-hook.md:174 now lists the tokens `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git` or `.config/superclaude`, and states the accepted over-match (any governed command whose text names that path is refused, reads included). The guard has the same token list at src/superclaude/hooks/scripts/launch-level-guard.sh:777 and the over-match comment at :779-781. The same line 174 also names the Bash-only coordinator verbs `complete`, `release-worker`, `adopt-*`, `record-*` and the `issue_pipeline` modules, which matches the guard case at launch-level-guard.sh:455 (comment :448-454 on best effort and the accepted `issue_pipeline/complete.py` over-match). Bash-only, `install_hooks` and the edit-tools `/../` clause are unchanged and agree with the guard (:444, :793).

Earlier finding F1.1 (carried from the previous review) stays resolved: docs/designs/sc-issue-launch-level-hook.md:172 H3 order (`project item-list`/`field-list` NONE, then issue/label/project ISSUE, then `pr create|edit|comment|ready` SUBMIT, then UNKNOWN in command position) equals launch-level-guard.sh:664, :665, :666, :667.

Other design-doc sentences checked against the guard
- docs/designs/sc-issue-launch-level-hook.md:96 (ISSUE blocked at all four levels) matches launch-level-guard.sh:815.
- :98 (message precedence BIG, TAMPER, MERGE, GHWRITE, ISSUE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL) is identical to the loop at launch-level-guard.sh:802.
- :110 (row 20a: ISSUE class, ISSUE at W, WA, F, FS; reads stay NONE) matches :664-665 and :815; the column layout matches rows 5 and 22 (:108-109 region).
- :244 (LL-ISSUE blocked/why/you-can) matches launch-level-guard.sh:74-77; :245 (LL-SUBMIT without "or issue") matches :70-73.
- :251 (LL-TAMPER message) matches launch-level-guard.sh:98-101 (message text was not changed by the task and does not list the new tokens, and neither does the guard's own message, so they agree).
- :85 ("any Bash ... call that names the store, Claude Code settings or hooks, a git config file, or a reinstall is TAMPER") is a summary, not a token list. It is incomplete next to :174 but not false; noted as F3.1 with no blocking answers.
- :121 (TAMPER examples) is an example list, not exhaustive; nothing in it contradicts the guard.
- :516 "version: 1" is the pre-push hook stamp, a different stamp from guard line 10 ("launch-level-guard-version: 2"), so it is not stale.
- Lines 17, 34, 313, 319 and 522 name no tamper token, gh class or precedence and need no change.

Per-AC marks (scope limited to the repair; test files and test runs not in scope for this re-review)
- scope (design doc agrees with guard on tamper tokens, gh H3 classes, message precedence): met. Citations: docs/designs/sc-issue-launch-level-hook.md:172, :174, :98 against launch-level-guard.sh:664-667, :455, :777, :802.
- T13.AC1: not re-assessed here. Guard side: T13.AC1@src/superclaude/hooks/scripts/launch-level-guard.sh:664-665 (reads allowed, issue/label/project give ISSUE), :815 (ISSUE refused at W, WA, F, FS), :802 (class in the for list).
- T13.AC2: not re-assessed here. Guard side: T13.AC2@src/superclaude/hooks/scripts/launch-level-guard.sh:10 (stamp 2), :74-77 (three-part message), :777 (`.config/superclaude` token).
- T13.AC3: not re-assessed here. Guard side: T13.AC3@src/superclaude/hooks/scripts/launch-level-guard.sh:455 (anchored `complete` forms, `.complete`, `/complete.py`, import and `complete.run` alternatives).
- T13.AC4: not re-assessed here (read-only review; suites, make verify-sync and staging not run).

Findings
F3.1 ac=scope at=docs/designs/sc-issue-launch-level-hook.md:85 anchor=src/superclaude/hooks/scripts/launch-level-guard.sh:777 chk=n,n,n,n family=design-doc-summary-incomplete fix=optional: add "the watcher config under .config/superclaude" to the :85 list : The summary sentence at :85 omits the new `.config/superclaude` token that :174 and the guard (:777) now carry; the sentence stays true, so it is not a contradiction.
