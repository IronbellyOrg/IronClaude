start=b6de60bca78d4bd884af1b3721cebe4d62c50bb9 tree=c8ed6ba9649ebddee1fd7055d18388f3d071ccb5
## Acceptance criteria

T6.AC1: **unmet** (F1.1). Kill switch, NOFALLBACK, exit codes, preflight and steps 2-8 are met: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh:36-42, :52-54, :99-109, :126-139, :144-147.
T6.AC2: **met**. T-10 gate order .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_launch.py:122-136; F-4 :221-225; F-5 :173-181; F-10 :184-196; F-11 :199-204; F-12 :207-218. 11 passed.

F1.1 sev=blocking trigger=B1 ac=T6.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh:36 anchor="default 1, any other value refused exit 2" chk=y,n,n,n family=killswitch-empty fix=read the variable with ${PANEL_COLLAB-1} (unset-only default) so a set-but-empty value reaches the 0/1 case and is refused; the same for NOFALLBACK at line 41 first=A1 origin=new covers="default 1, any other value refused exit 2": COLLAB=${PANEL_COLLAB:-1} treats a set-but-empty PANEL_COLLAB= as the default 1, so the kill switch silently stays on instead of refusing with exit 2; NOFALLBACK= is likewise accepted at line 41.
F1.2 sev=note trigger=none ac=T6.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh:75 anchor=DESIGN.md:316 chk=n,n,n,n family=resume-skip-rule first=A1 origin=new fix=skip only a package whose status is ok and re-run the others: the reviewer's yes (ac-outcome-missing, anchor "a package with score.json reached is skipped") failed the Read-back because those words are not in the AC text; the skip test is [ -f "$d/status" ], so invalid, quarantined and judge_failed packages are also skipped on resume.
F1.1 resolved
