68b9da66f0b14bac92cd6226f8ac1429a65c8d99
family unreadable-at-engage-scope
defect form: the ref says an unreadable timeline at engage, including events missing from a complete read, halts, but engage_decision halts only on a failed or incomplete read (rows 3 and 8); events missing from a complete read fall through to ENGAGE.
command: grep -n -i -e "unreadable" -e "events are missing" -- src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md
before:
  79:**Engage failure.** An engage failure, and an unreadable timeline at engage (reason `read_failed` or
  80:`timeline_unreadable`), halt with `terminal_halted` reason `draft_guard_unavailable` before any edit.
  109:| `HOLD` | Keep the PR draft and report `held` with the reason (`head_mismatch`, `push_not_completed`, `read_failed` or `timeline_unreadable`) and the clear command; keep going. |
  119:## 5. Foreign toggle and unreadable timeline
  123:calls that failed or were never settled) and returns `ok`, `foreign` or `unreadable`.
  127:- **Unreadable** (the timeline call failed, the list is incomplete, or events are missing): at engage
  128:  this halts (section 2); at a later checkpoint do not release, report `held (timeline unreadable)`
  150:could not be confirmed, an unreadable timeline and a merged or closed PR. Exits with unpublished or
coupled sites: the Unreadable bullet of section 5 (lines 127-129) only; lines 79-80 already name the two halt reasons exactly, and lines 109 and 150 are about later checkpoints, where an unreadable result holds.
after:
  79:**Engage failure.** An engage failure, and an unreadable timeline at engage (reason `read_failed` or
  80:`timeline_unreadable`), halt with `terminal_halted` reason `draft_guard_unavailable` before any edit.
  109:| `HOLD` | Keep the PR draft and report `held` with the reason (`head_mismatch`, `push_not_completed`, `read_failed` or `timeline_unreadable`) and the clear command; keep going. |
  119:## 5. Foreign toggle and unreadable timeline
  123:calls that failed or were never settled) and returns `ok`, `foreign` or `unreadable`.
  127:- **Unreadable** (the timeline call failed, the list is incomplete, or events are missing from it): at
  128:  engage only a failed or incomplete read halts (reasons `read_failed` and `timeline_unreadable`,
  130:  engage. At a later checkpoint do not release, report `held (timeline unreadable)` with the clear
  152:could not be confirmed, an unreadable timeline and a merged or closed PR. Exits with unpublished or
