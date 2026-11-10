## Card reviewer-3
model_class: opus
persona: refactorer
verdict: FAIL
self_confidence: 0.85

### Findings

- id: R3-F1
  grade: blocking
  class: contradiction
  claim: Task 5 adds spec-panel-minfix.md to src/superclaude/commands/; an existing repo test the plan never runs will then fail, and the plan gives no permission to edit it.
  evidence: tests/recommend/test_routing_refresh.py:33 `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}`; lines 647-648 `shipped = {p.stem for p in _COMMANDS.glob("*.md") if p.name != "README.md"}` / `assert shipped - _POST_REFRESH_ADDITIONS == active`; frozen package .dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/SPEC-sc-recommend-refresh.md exists; comment lines 29-32 show every later command is added to that set. Plan line 124 omits this file; source.md:90 names only four tests.
  tag: Grounded
  fix: Task 5 adds "spec-panel-minfix" to _POST_REFRESH_ADDITIONS (with comment), adds the file to the regression run, and flags it to the owner as an edit source.md does not list; optionally a full `uv run pytest tests/ -q` as the last check.

- id: R3-F2
  grade: minor
  class: unverifiable-AC
  claim: The pin "the `~/.claude/` path precedes the `.claude/` path" is ambiguous: whole-file it fails (bullet 5 names the project .claude/ path first and must stay byte-identical); as plain substring it can never fail. Task 4 has the same substring problem.
  evidence: plan line 122; src/superclaude/commands/spec-panel.md:262; tests/skills/test_spec_panel_review_loop.py:136-138; plan line 103.
  tag: Grounded
  fix: Scope the check to the ## Fix Budget section and use a lookbehind `(?<!~/)\.claude/skills/sc-fixcheck/`.

- id: R3-F3
  grade: minor
  class: unverifiable-AC
  claim: importlib loading of fixcheck.py may leave scripts/__pycache__/*.pyc with the absolute src/superclaude path, tripping Task 4's recursive grep and being copied by the install block's cp -rn.
  evidence: plan lines 50 and 104; source.md:172.
  tag: [INFERRED]
  fix: grep -rnI --exclude-dir=__pycache__; set sys.dont_write_bytecode in the test; exclude __pycache__ from the install copy.

- id: R3-F4
  grade: minor
  class: gap
  claim: INSTALL.md's pre-run probe needs one valid and one invalid fixture on disk, but no task creates them.
  evidence: plan line 163; Task 8 file list line 158; source.md:180.
  tag: Grounded
  fix: Task 8 adds .dev/brainstorms/346-minfix/probe/{valid,invalid}/ fixtures with exit-0/exit-1 ACs, or INSTALL.md states the coordinator writes them.

- id: R3-F5
  grade: minor
  class: gap
  claim: test_worker_contract.py's write-verb audit scans every file under src/superclaude/{skills,commands,agents}; the plan does not warn that new text must avoid git add/commit/push/merge/stash, gh pr and gh api tokens.
  evidence: tests/skills/test_worker_contract.py:1940-1950 (AUDIT_ROOTS, WRITE_VERB_RE) and 3129-3130 test_every_write_verb_hit_is_classified; plan line 20.
  tag: Grounded
  fix: Add that rule to Constraints.

### Self-Audit (reviewer)
Task order 1-6, 5->7, 6+7->8 holds. Removing the Unattended section keeps _check_no_unattended_sections passing. Bullet 6 pins can pass; the 427 bullet 6 in .dev/tasks/done/TASK-WF-specPanelReviewL-20261107-090418/source.md:64 matches the current one, so Task 7's byte-identity AC is consistent. test_routing_plugin_parity.py, test_how_we_work_routing_table.py, test_cli_install.py, test_model_alias_policy.py and test_graph_command.py are not tripped. sync-dev/verify-sync cover scripts/ and skip __pycache__. Task 8's sed/cmp ACs are sound. Not checked: 95f2c6e4 contents, /tmp sources (no shell).

### Blind calibration (confidence-calibrator, opus, card only)
scores: {citation_grounding: 0.90, coverage_completeness: 0.75, deviation_classification_clarity: 0.75, risk_surface_coverage: 0.75, recommendation_actionability: 0.85}
confidence_calibrated: 0.80   # self-reported 0.85
finding_checks:
  R3-F1: holds (blocking correct)
  R3-F2: partly holds (whole-file order pin really fails because of line 262; the "can never fail as substring" half is wrong)
  R3-F3: holds, grade too low (importlib writes __pycache__/*.pyc by default containing the absolute src/superclaude path; Task 4's grep -rn could then never pass -> blocking)
  R3-F4: holds (minor defensible)
  R3-F5: holds, low impact (test_worker_contract.py already in the plan's regression run)
risks_missed: other tests that enumerate shipped skills; /tmp brief sources
