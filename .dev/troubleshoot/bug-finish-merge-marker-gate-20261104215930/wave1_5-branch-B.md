# Wave 1.5 Branch B (architectural docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

- doc_path: .dev/tasks/done/TASK-WF-design-20261104-164423/source.md
  currency_verdict: unknown
  reason: no header markers. Section 7.2 (:795-824) is the finish-gate spec; commit step 4 (:817) pins the marker regex to exactly `^(<{7}|\|{7}|={7}|>{7})( |$)` (the design itself counts only 7-wide markers); commit step 5 (:818) compares `git rev-parse :<path>` with `git rev-parse <merge-tree-oid>:<path>` and never mentions modes. No F-case covers other marker widths or a mode-only difference (F-cases :1380-1382).
- doc_path: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
  currency_verdict: unknown
  reason: no header markers. Step 9 (:103-120) defines the finish-merge.sh call and the FINISH_FAIL token table; it does not spell out marker width or blob-vs-mode semantics.
- doc_path: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
  currency_verdict: unknown
  reason: no header markers. :60 "Remove every conflict marker. Then stage the finished file at once"; does not define gate width or mode semantics.
