b0a7f9d6eaf45660bfe9511bd5cafecce21dafed
family impl-md-accuracy (second entry, after review r2-1)
defect form: IMPLEMENTATION.md says one thing in one section and a different or unevidenced thing in another (a figure dropped in one place and kept in another; "passes" against "only partly")
command: grep -nE "9-81|re-checked the concurrency|frozen/pins.sha256|offline measurement|left no trace|1,577|measured offline" .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate/IMPLEMENTATION.md
before-output:
(from the reviewed tree r2-1: lines 111, 192 held frozen/pins.sha256; line 214 held "The offline measurement was 9-81 ms"; line 216 held "S0 re-checked the concurrency pattern (passes)")
after-output:
30:| `frozen/pins.sha256` | 14 | sha256 of every frozen file, `lib/values.py`, `lib/results.py`, `lib/arm_summary.py`, `REQ`, `judge-one.sh`, `findings.py`, `ledger.py` |
137:| Hook time per call | probe hook at most 27 ms (`hook_ms_max` per model in `s0-summary.json`). For `r4-hook` itself, the board metrics of `smoke-f7-el2-3` give 9 to 143 ms over 35 calls; the earl
coupled sites: section 5 S0 table rows (hook time, concurrency pattern, sandbox hooks), section 7.2 rows, section 4 test_pins row
