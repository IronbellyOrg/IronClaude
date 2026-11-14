start=18e8eb6d54a0d71c1c5225866b836a06a0a4f681 tree=f6149eae112d2e67dad3802aee13730cab3ec002
## AC marks

- T3.AC1: UNMET (F1.1, F1.2). The parts that match the design:
  - msg-validate.sh follows the 2.2 rules and reasons: R1/tools/msg-validate.sh:15 (`too_long`), :19 (`bad_key`), :28 (`bad_field`), :29 (`bad_move`), :33 (`leak`).
  - radar-hook.sh follows steps 3-10 of 2.4. Failed seal: R1/tools/radar-hook.sh:36. Finish: :39-43. Checkpoint and K: :47. Guard: :51. Seal and fail-closed: :58-62. Item choice: :72-77. Task hint: :87. Validation: :100. Output: :107.
  - The 2.5 order is in R1/tools/launch.sh:5-12.
  - settings-gen.sh is in R1/tools/settings-gen.sh:10-14.
  - The deviations are the classifier's M2 rule (R1/tools/radar-classify.jq:38 against DESIGN.md 2.3, R1/DESIGN.md:147) and the corrupt-line guarantee of 2.4 step 4 (R1/DESIGN.md:162; R1/tools/radar-classify.jq:6 and :27, reached from R1/tools/radar-hook.sh:77).
- T3.AC2: MET. The suite passes with 60 tests, and each listed test checks what 6.1/6.2 lists for it:
  - T-3: R1/tests/test_classify.py:53-73
  - T-4: R1/tests/test_order.py:12, :20
  - T-5: R1/tests/test_hook_schedule.py:21-74
  - T-6: R1/tests/test_hook_finish.py:6
  - T-7: R1/tests/test_hook_seal.py:8, :21
  - T-8: R1/tests/test_hook_errors.py:8, :14, :25
  - T-9: R1/tests/test_validate.py:18-55
  - T-10, settings part: R1/tests/test_settings_and_cmd.py:8
  - F-6: R1/tests/test_faults.py:9
  - F-7: R1/tests/test_faults.py:16
  - F-14: R1/tests/test_faults.py:26

F1.1 sev=blocking trigger=B1 ac=T3.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:6 anchor="the four tools implement the behaviour of DESIGN.md sections 2.2, 2.3, 2.4 and 2.5" chk=y,n,n,n family=corrupt-line-breaks-hook fix=make `rec` drop non-objects, e.g. `def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");`, and add a T-8/F-7 case with a JSON-parsable non-object peer line (`[1]`) as the last tele line first=A1 origin=new covers="2.4 step 4: readers skip unparsable lines with `fromjson? // empty`, so a torn or corrupt line never breaks a hook, R-22": `rec` only skips lines that do not parse. A corrupt line that parses as a non-object (`[1]`, `42`, `"x"`) reaches `$r.sub` at radar-classify.jq:27, and jq exits 5 when that line is the last input. In the hook, `covered=$(cat "$BOARD"/tele/*.jsonl | classify | sort -u)` (radar-hook.sh:77) runs under `set -e -o pipefail`, so the searcher's checkpoint becomes `hook_error` and nothing is injected. Reproduced: a peer tele file ending in `[1]` cut the searcher from 2 injections (calls 6 and 10) to 1, with `hook_error` 1. The same applies to the own-tele classify at :72. The current F-7 and T-8 garbage lines (`\x00garbage{` and `{"n":1,"tool":"Bash","inp`) do not parse, so they never reach this path.
F1.2 sev=blocking trigger=B1 ac=T3.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:38 anchor="the four tools implement the behaviour of DESIGN.md sections 2.2, 2.3, 2.4 and 2.5" chk=y,n,n,n family=classifier-m2-overmatch fix=test the l/c/L flag cluster only on option tokens of the grep segment itself (reuse `segs` with the token split, as M1 and M7 do), not with a regex over the whole command after the word grep; add T-3 negatives `grep -rn x src/ | head -c 500` and `grep -n x f; ls -la` first=A1 origin=new covers="DESIGN.md 2.3 M2: Bash `cmd` contains `grep -l`, `grep -c`, `grep -L`, combined short flags containing `l` or `c` after `grep -`, `find `, or a pipe into `wc -l`": The M2 regex `\bgrep\s+(\S+\s+)*-[A-Za-z]*[lcL][A-Za-z]*(\s|$)` lets `(\S+\s+)*` run over `|`, `;` and `&&`. Any later token of another command that contains l, c or L therefore fires M2 (`| head -c 500`, `; ls -la`, `&& sort -c`); all three were reproduced. In the hook this marks M2 as covered by the panel when no grep listing or count ran, so the searcher's M2 is skipped silently (2.5 (b)). The post-hoc `move_executed` and `moves_covered` counters built on the same classifier are inflated too.
