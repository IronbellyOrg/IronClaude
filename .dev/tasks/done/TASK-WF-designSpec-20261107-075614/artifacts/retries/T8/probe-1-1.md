68b9da66f0b14bac92cd6226f8ac1429a65c8d99
family resume-row2-precedence
defect form: the ref says a resume below ordinal 3 or with the flag off also reconciles an unsettled request, but resume row 2 answers REPORT_HELD before row 3 can reconcile.
command: grep -n -i -e "reconcil" -- src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md
before:
  156:run must be reported (and an unsettled request reconciled) before any edit, release or re-trigger.
  176:| 3 | `RECONCILE` | An unsettled request exists. Reason `resume_reconciled`: the live state matches the request and the transition count is the 
  184:Unsettled requests are always reconciled first, so no edit, release or re-trigger runs on an unknown
coupled sites: the Resume intro paragraph, the row 2 and row 3 table rows and the closing paragraph of the Resume section.

family guard-status-halt-unavailable
defect form: the Exit report maps merge_guard to guard_status only, but an engage halt before any request leaves no guard record, so guard_status returns released.
command: grep -n -e "unavailable" -- src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md
before:
  73:| `HOLD` | Ownership is unproven: do not mutate, keep going and report `unavailable`. |
  79:`timeline_unreadable`), halt with `terminal_halted` reason `draft_guard_unavailable` before any edit.
  140:| `unavailable` | The guard could not act or prove ownership (engage failure, ownership unproven). |
coupled sites: the Engage failure paragraph and the Exit report value table.

family keyword-only-signatures
defect form: the ref writes the three decision calls with positional arguments, but the functions take keyword arguments only.
command: grep -n -E -e "(engage|release|resume)_decision\(" -- src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md
before:
  64:**Steps.** Read, then decide with `engage_decision(mode, ordinal, cycle_id, guard, read)` where `guard`
  101:`release_decision(mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)`.
  159:`resume_decision(mode, ordinal, guard, read, pending, dangling_branch, published)`:
coupled sites: the three call sites above; the protocol test names the functions without parentheses.
