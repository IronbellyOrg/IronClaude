# Tier 1 observation
- Source read (orchestrator): finish-merge.sh:208 regex `^(<{7}|[|]{7}|={7}|>{7})( |$)` counts only 7-wide markers; step 4 (:214-233) compares staged-blob vs stage-1-blob counts with this function.
- Source read: finish-merge.sh:246-249 compares `git rev-parse :0:<path>` with `git rev-parse <MT_OID>:<path>` (blob ids only; modes not compared).
- Codex reported a reproduction of C2 (unrelated run.sh staged 100755->100644 committed). Not re-run here: no repro command in the issue; a hermetic repro is planned as a regression test in tests/pr_submit/test_conflict_scripts.py.
- Verification (pr-submit Wave 3, evidence-validator): A1 verified (git honours the conflict-marker-size gitattribute; no override at refs/conflict-mechanical.md:76), C2 verified.

## Probe (run 2026-11-04T22:05:48Z, same-shell, scratch repo under /tmp, unfixed script; command: bash probe-finish.sh <finish-merge.sh>; full output in probe-finish.out)
    == A1: conflict-marker-size=9, markers left in f.txt and staged
    marker line written by git: <<<<<<<<< HE
    {"merge_sha":"1b0d4e56bf4f68ef987b6e07e3bceffb395cf96f","parents":["d286323c17dfa26fadf8d9c9a04222a74720a606","5bfc8497b25bd0695436aec80ef86946df69086f"]}
    exit=0
    == C2: resolve f.txt, stage an unrelated mode change on run.sh
    diff --cached --name-only vs merge tree: f.txt run.sh 
    {"merge_sha":"4289c3aa730b69bad5a985c3830f086938d5e84d","parents":["58777b2547cb4e23319056243a9e799c0e3be6d6","5ca141abc79ef9be48b2e3b803d846656d3f2f2a"]}
    exit=0
    committed run.sh mode: 100644

## Behaviour definitions
- (a) observed: git wrote a 9-character marker line ('<<<<<<<<< HE...') under 'f.txt conflict-marker-size=9' (probe-finish.out:2); the gate passed (exit=0, :3-4).
- (b) observed: run.sh staged 100755->100644 with identical content was committed with mode 100644 while step 5 passed (probe-finish.out:6-9).
- (c) observed: 'git diff --cached --name-only --no-renames <merge-tree>' listed the mode-only path run.sh (probe-finish.out:6).
