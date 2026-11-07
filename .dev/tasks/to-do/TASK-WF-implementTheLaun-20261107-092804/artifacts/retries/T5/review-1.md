10d7c8f8dac0d54b499bdfabb570e335c2c3eb2f d65b74d56ecc4420a52037cc4a35b4f43b8b1ea4
T5.AC1 met tests/hooks/test_launch_level_guard.py:767-810
T5.AC2 met tests/hooks/test_launch_level_guard.py:1105
T5.AC3 met tests/hooks/test_launch_level_guard.py:1072
T5.AC4 met tests/hooks/test_launch_level_guard.py:1091
F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:222 anchor="for _ in {1..64}; do" chk=n,n,n,y family=raw-id-cap fix=drop the 64 cap so every session_id value is tried covers="remove the fixed-64 raw-id early-allow loop of MR" first=A1 origin=new: the failure-path scan still tries only 64 session_id values, so 70 forged ids before the real bound id allow the call.
F1.2 sev=note trigger=none ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:222 anchor=src/superclaude/hooks/scripts/launch-level-guard.sh:222 chk=n,n,n,n family=raw-id-forged fix=declared limit in the Task 14 record and the final report first=A1 origin=new: on a failure path a bound id anywhere in broken JSON counts, so an ordinary session sending broken JSON with a nested bound id is blocked; Task 5 AC4 and MR T-FC-5 require the raw read, and design section 3 says no raw match counts as proof; the conflict is in the sources.
F1.3 sev=note trigger=none ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:209 anchor=src/superclaude/hooks/scripts/launch-level-guard.sh:209 chk=n,n,n,n family=comment-drift fix=reword the comment first=A1 origin=new: comment said never infer a binding while the code reads a raw bound id.
