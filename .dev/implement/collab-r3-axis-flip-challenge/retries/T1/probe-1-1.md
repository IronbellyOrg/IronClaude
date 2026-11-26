7dabb5fbd744c8030ba69f59cd84a173825b5fde
## family spike-s2-luna-kill
defect: S2 kill check never shows text before the kill for luna
search: grep -n -F killed_text_events .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh
before: lines 34, 39, 40 (computed and reported, not in pass)
coupled: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md S2 rows; spikes/s2/*/result.json
## family spike-record-verdict
defect: pass expression omits a design pass condition
search: grep -n -F 'pass:(' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/run.sh
before: spike-s2.sh:44 pass without kill condition; g0-h3/run.sh pass includes all four design conditions
coupled: spikes/s2/*/result.json pass fields
## family report-accuracy
defect: a number in the report does not match its record
search: grep -n -E '10.5-14.2|5.5-6.6|20 \+ 20|20 sampled matches' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-surf/NOTES.md
before: IMPLEMENTATION.md:89 (ranges), IMPLEMENTATION.md:91 (20 + 20), NOTES.md:6 (20 sampled matches)
coupled: IMPLEMENTATION.md section 1 G0-SURF row
## family guard-test-coverage
defect: guard test omits required refused paths
search: grep -n -F r1-move-radar .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_guards.py
before: test_guards.py:23
coupled: none
## family ac14-evidence
defect: AC-14 manifests not bracketing and not on file
search: grep -n -F 'AC-14' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md
before: IMPLEMENTATION.md:109
coupled: IMPLEMENTATION.md section 6 manifest row
## family sandbox-parity
defect: snapshot drops tracked-at-base files that the sandbox .gitignore matches
search: grep -n -F 'git add -A' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/conftest.py
before: build-sandbox.sh:45; conftest.py mini_sandbox (no ignored tracked files; unaffected)
coupled: cleanup-sessions.sh git clean -fdX (correct once the snapshot holds the files)

after (r2-1 tree fb1f545c69b4f581e28c7d43178c4df151e30270):
spike-s2-luna-kill: 37 
spike-record-verdict: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/run.sh:22:        pass:($brc==0 and ($rows|all(.status!="same_as_impl")) and $leak=="" and $refl=="absent
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/run.sh:24:jq '{spike:"G0-H3",rows:.,pass:(map(.pass)|all)}' <<<"$OUT" | tee "$R3/spikes/g0-h3/result.json
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh:41:    resume_pass:($rrc==0 and $sid==$rsid and $sid!="" and $mok2 and ($ts==true)),
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh:42:    pass:($rrc==0 and $sid==$rsid and $sid!="" and $mok2 and ($ts==true) and ($m!="gpt-6-luna" or (
report-accuracy: none
guard-test-coverage: 23:    others = ("r1-move-radar", "r2-idle-shift-sweeper", "r4-flag-and-adjudicate", "r5-coverage-deflection")
ac14-evidence: 112:AC-14: the sha256 manifests of `REPO/src` and `EVAL` (13,243 files) are iden
sandbox-parity: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/conftest.py:109:    subprocess.run("git init -q && git add -A && git -c 
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh:46:  ( cd "$T" && git init -q && git add -A -f && git -c 
