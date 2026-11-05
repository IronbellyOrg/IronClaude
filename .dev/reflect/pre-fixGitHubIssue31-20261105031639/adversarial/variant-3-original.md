# Reviewer 3 card (persona: refactorer; model class: opus). Persisted by the orchestrator from the reviewer's returned text, condensed; claims and evidence refs are unchanged.
reviewer: 3
persona: refactorer
findings:
  - id: F1
    claim: Task 1 puts --auto-name in the --ask dispatch (ccsession:1515-1546), which runs after the main argument loop (ccsession:648-723); that loop takes --shim, --name=*, --profile=*, --tier=*, --model=* and --claude-args out of the arguments and exits 2 on a bare --model/--tier/--profile/--name with no value, so a prompt such as "--model" or "--tier=x" is eaten or aborts the launch, breaking Task 1's own hostile-text requirement.
    tag: grounded
    evidence: ccsession:648-723, ccsession:1543-1546, ccsession:597-628; TASK-WF plan:31
    severity: minor
    deviation_class: drift
    recommendation: Place --auto-name in the early dispatch at ccsession:597-628 before the argument loop; add acceptance tests for `ccsession --auto-name --model` and `ccsession --auto-name "--tier=x"` printing a valid label and exiting 0.
  - id: F2
    claim: Task 5 says to keep "the relaunch reopen tests asserting untagged or reopened behaviour as they are", but test_orca_a_new_tab_or_a_rerun_is_still_asked and test_orca_relaunch_whose_conversation_is_gone_is_asked press Enter and assert an untagged start; under Task 4 Enter gets an auto-name, so they must change. Task 5 contradicts itself.
    tag: grounded
    evidence: tests/unit/test_ccsession_tag.py:1801-1804, tests/unit/test_ccsession_tag.py:1859-1863; plan:84, plan:69
    severity: minor
    deviation_class: drift
    recommendation: In Task 5, keep unchanged only reopen tests that do not press Enter; name the two tests above as tests to update to the auto-named result; verify with `uv run pytest tests/unit/test_ccsession_tag.py -k orca`.
  - id: F3
    claim: Task 7 has the final test run write ./artifacts/launch-paths.md into the package, a test writing outside tmp_path, against the plan's own Constraint; the source does not ask for it.
    tag: grounded
    evidence: plan:25, plan:108; source.md:1
    severity: minor
    deviation_class: drift
    recommendation: Change Task 7's criterion so the executor writes launch-paths.md from the pytest -v output, not from test code; verify no test opens a path outside tmp_path.
  - id: F4
    claim: Task 3 lifts Claude --name/-n into ccsession's --name, adding two behaviours the source does not ask for: a value equal to a saved label now resumes that old conversation, and a value validate_label rejects now stops at ccsession exit 2 with no Claude start.
    tag: grounded
    evidence: ccsession:1649-1650, ccsession:1681-1693, ccsession:275-301; ccsession-orca:113-117; plan:23, plan:57
    severity: minor
    deviation_class: authorized
    recommendation: Keep as a reported plan-author decision, add acceptance cases for a Claude --name equal to a saved label and for an invalid Claude --name value (Claude still starts, e.g. fall back to an auto-name); ask the owner which is intended.
  - id: F5
    claim: Task 2 changes the default hint and the 30-second limit for every caller of ask_session_name; the new default hint "Enter = auto-named, Ctrl+C = cancel" misdescribes the out-of-scope Coder New Terminal hook caller until Coder changes.
    tag: grounded
    evidence: ccsession:1418-1421; plan:19, plan:43
    severity: minor
    deviation_class: authorized
    recommendation: Keep the timer for every caller; keep the old default hint and let ccsession-orca pass the auto-name hint, or list the hint change in the Task 11 Coder handoff.
  - id: F6
    claim: Task 4's rule for which launches get an auto-name mixes "or" and "and" and can be read two ways; the classification is split between Task 3 and Task 4, hiding a coupling.
    tag: grounded
    evidence: plan:57, plan:69
    severity: minor
    deviation_class: none
    recommendation: Rewrite the Task 4 rule as one ordered decision list (resume-like, AUTOSTART=0 or print mode -> untagged; name -> that name; asked -> its outcome; otherwise -> auto-name from the task text); Task 3 computes every class the list uses.
  - id: F7
    claim: Tasks 1-4 change behaviour that existing tests pin and those tests are updated only in Task 5, so Tasks 3 and 4 cannot be checked one at a time against a passing test file.
    tag: inferred
    evidence: null
    severity: minor
    deviation_class: none
    recommendation: Fold each task's updates to old tests into Task 3 and Task 4, or state that `-k orca` is expected to fail until Task 5 and give Tasks 3 and 4 narrow -k selectors.
  - id: F8
    claim: Task 1 checks uniqueness only against existing topic files; the file is written later by the SessionStart hook, so two launches in the same folder in the same minute with the same or no task text can get the same label.
    tag: grounded
    evidence: ccsession:1668-1669, ccsession:336-337; plan:31
    severity: minor
    deviation_class: none
    recommendation: Add a random or process-id part to the stamp, or create the topic file atomically; test two auto-name calls in the same minute expecting different labels.
scope_additions:
  - Claude --name/-n lifted into ccsession --name (Constraints, Task 3): ask-owner.
  - Print mode (-p/--print) stays untagged: keep.
  - CCSESSION_AUTOSTART=0 means plain untagged start: keep.
  - --from-pr added as resume-like: keep.
  - Auto-name format (folder name, 4 words, stamp, 80-char cap): keep, report to the owner; the 80-character cap plus a -2 suffix can exceed 80 and there is no protection against concurrent launches.
  - 245-byte limit measured as the saved file name: keep.
  - Default hint text changed for every ask_session_name caller (Task 2): ask-owner or record in the Coder handoff.
  - launch-paths.md written by test code (Task 7): remove from test code; have the executor write it.
  - Coder handoff artifact (Task 11): keep.
verdict: ready-with-notes
self_confidence: 0.75
calibration:
  calibrator_model_class: sonnet
  calibrated_confidence: 0.74
  note: blind calibration; F1,F2,F4,F5,F6 evidence verified, F3 and F8 partly overstated
