<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer-1, sonnet/analyzer) -->
<!-- Merge date: 2026-11-08T18:56:00Z -->

## Merged card
verdict: FAIL
merge_method: adversarial
blocking_count: 4

### Findings

<!-- Source: Variant 1 R1-F1 (base) + Variant 3 R3-F1 + Round 2.5 INV-001; fix replaced, merged per Change #1 -->
- id: M-F1
  grade: blocking
  class: gap
  claim: The plan's regression run omits tests/recommend/test_routing_refresh.py, which should fail once src/superclaude/commands/spec-panel-minfix.md exists. Task 5 either ships a command that breaks an existing test or stops blocked on a test it never runs, and plan:119 gives no permission to edit that test, so adding the command to the allowed set alone cannot pass: an executor following plan:119 must stop instead of editing the test.
  evidence: tests/recommend/test_routing_refresh.py:33 `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}`; lines 647-648 `shipped = {p.stem for p in _COMMANDS.glob("*.md") if p.name != "README.md"}` and `assert shipped - _POST_REFRESH_ADDITIONS == active`; comment lines 29-32 show every later command is added to that set. Plan line 119 "any other failure caused by the new command or skill stops this task as blocked"; plan line 124 list omits tests/recommend/. source.md:90 names only four tests. INV-001: "tests/recommend/test_routing_refresh.py:647-648 is exactly such a failure, so an executor following plan:119 must stop instead of editing the test".
  tag: Grounded (test code, plan:119); the failure is [INFERRED] (not run)
  fix: In Task 5 add "spec-panel-minfix" to _POST_REFRESH_ADDITIONS in tests/recommend/test_routing_refresh.py (with a comment naming issue #346); add that file to the plan:124 regression run and to the files Task 5 touches; rewrite plan:119 so this one listed test edit is allowed instead of "stops this task as blocked"; flag the edit to the owner as one source.md does not list.
  sources: R1-F1, R3-F1, INV-001; debate C-001, A-001

<!-- Source: Variant 2 R2-F1 + Round 2 V2 rebuttal (b), (d); merged per Change #2 -->
- id: M-F2
  grade: blocking
  class: gap
  claim: No task delivers the required correction and retry when the re-reviewer's own checker call exits 2. source.md:46 requires it, but the literal block the plan ships (source.md:120) handles only exits 3/4/5/70; the exit-2 retry exists only for the reviser at source.md:127, and plan:117 copies the block unchanged apart from one owner-decision sentence. The auditor's own coverage matrix credits this requirement to Task 8; that is an audit artifact error, not a plan claim.
  evidence: source.md:46 "An exit 2 from the reviewer's own call is corrected once and re-run." Plan line 117 "the literal text of the fenced `markdown` block in source.md section 3.2, plus this one owner-decision sentence". Calibration: "source.md:120 handles only exits 3/4/5/70; the exit-2 retry text exists only for the reviser at source.md:127". Round 2 V2 (b): "a grep of the plan for "exit 2" / "own call" finds no reviewer-side retry". artifacts/coverage-matrix.json:269-272 assigns the quoted requirement to "match": "Task 8".
  tag: Grounded
  fix: In Task 5 Region 4, append one owner-decision sentence inside the existing source.md:120 paragraph (the same channel plan:117 already uses) saying an exit 2 from the reviewer's own check call is corrected once and re-run; add a pin for that sentence in tests/skills/test_spec_panel_minfix.py. Task 7 inherits it through its byte-identity AC (plan:147).
  sources: R2-F1; Round 2 V2 (b), (d); debate C-002, A-002

<!-- Source: Round 2.5 INV-003 (HIGH); T1 card INF-032; merged per Change #3 -->
- id: M-F3
  grade: blocking
  class: gap
  claim: The source.md:46 step-3 requirement that the run at `review: 3` also lists each budget escalation with its need and each `GRADE-CONFLICT` has no plan task; Review Loop bullet 4 escalates only with the open blocking findings and the shipped block never mentions GRADE-CONFLICT.
  evidence: INV-003 (b): "review-3 escalation "also listing each budget escalation with its need and each GRADE-CONFLICT" absent — Review Loop bullet 4 (spec-panel.md:261) escalates only "with the open blocking findings" and the block never mentions GRADE-CONFLICT (INF-032)". INV-003: "Under A-003, (b) is the same kind of missing deliverable as (a)".
  tag: Grounded
  fix: Append one owner-decision sentence inside the same source.md:120 paragraph as M-F2 (Task 5 Region 4) stating the `review: 3` escalation also lists each budget escalation with its need and each `GRADE-CONFLICT`, and add a pin in tests/skills/test_spec_panel_minfix.py.
  sources: INV-003; INF-032

<!-- Source: Variant 3 R3-F3 (upgraded) + Round 2 V3 rebuttal (a) + Round 2.5 INV-005, INV-006; merged per Change #4 -->
- id: M-F4
  grade: blocking
  class: unverifiable-AC
  claim: importlib loading of fixcheck.py (plan:50) writes scripts/__pycache__/*.pyc carrying the absolute src/superclaude path, and Task 4's recursive grep (plan:104) then matches it, so the Task 4 AC cannot pass. Nothing in the repo suppresses bytecode, and a later `sys.dont_write_bytecode` leaves the .pyc written in Task 1.
  evidence: plan lines 50 and 104; source.md:172. Calibration: "importlib writes __pycache__/*.pyc by default containing the absolute src/superclaude path; Task 4's grep -rn could then never pass -> blocking". Round 2 V3 (a): "No `dont_write_bytecode` / `PYTHONDONTWRITEBYTECODE` in pyproject.toml, Makefile, CI workflows or tests/conftest.py; plan:104 grep then matches the .pyc." INV-005: "`__pycache__` is first written in Task 1 (plan:50) and persists through Tasks 2-3; `make clean` (Makefile:61) is in no task". INV-006: "install_skill.py:52 copytree and source.md:172 cp -rn copy the .pyc (harmless)".
  tag: Grounded (no suppression in repo config); the .pyc match is [INFERRED] (not run)
  fix: Use `grep -rnI --exclude-dir=__pycache__` in the Task 4 AC (works regardless of when the .pyc was written); optionally set `sys.dont_write_bytecode` in the test; note that the install copy (`cp -rn`, install_skill.py copytree) carries the harmless .pyc, or exclude `__pycache__` from it.
  sources: R3-F3; Round 2 V3 (a); INV-005, INV-006; debate C-009

<!-- Source: Variant 1 R1-F2 (base) + Round 2.5 INV-002; fix appended per Change #5 -->
- id: M-F5
  grade: minor
  class: unverifiable-AC
  claim: The repo variant lands at exactly 500 lines, the lint-architecture hard limit, and no AC checks it; the M-F2 and M-F3 sentences cannot add lines without breaking it.
  evidence: 486 - 12 (Unattended section lines 451-462) + 26 (Fix Budget block source.md:104-128 plus blank) = 500; Makefile lint-architecture errors at -gt 500; .github/workflows/test.yml:135 runs make lint-architecture. INV-002: "Makefile:403 fails above 500; CI runs make lint-architecture (.github/workflows/test.yml:133-135); Task 5 has no wc -l check; new sentences must be appended inside the existing source.md:120 paragraph, as plan:117 does".
  tag: Grounded
  fix: Add AC wc -l <= 500 plus make lint-architecture and make lint to Task 5. Append the M-F2 and M-F3 sentences inside existing paragraphs, never as new lines, since the variant already lands at exactly 500 lines.
  sources: R1-F2, INV-002; debate C-004

<!-- Source: Variant 1 R1-F3 (base), carried unchanged -->
- id: M-F6
  grade: minor
  class: gap
  claim: No task bullet says check verifies the baseline hash; only a Task 3 test exercises it.
  evidence: plan line 89; source.md:46 and :62 ("4 hash conflict").
  tag: [INFERRED]
  fix: Add a Task 2 bullet: check exits 4 when sha256(--baseline) differs from reviewed_sha256; move the test to Task 2.
  sources: R1-F3

<!-- Source: Variant 1 R1-F4 (base), carried unchanged -->
- id: M-F7
  grade: minor
  class: unverifiable-AC
  claim: gross, net and add-only are never defined and the delete exemption's cap is unstated.
  evidence: plan line 64 "`delete` entries are free of the gross cap"; source.md:60, :125.
  tag: [INFERRED]
  fix: Define the three counts in Task 2 and add a test for the delete exemption.
  sources: R1-F4

<!-- Source: Variant 1 R1-F5 (base), carried unchanged -->
- id: M-F8
  grade: minor
  class: unverifiable-AC
  claim: The exact post-edit text of Review Loop bullet 6 is not given; pins check only substrings and the owner sentence only via `carried-open:`.
  evidence: spec-panel.md:263; plan lines 116 and 122.
  tag: Grounded
  fix: Write the full resulting bullet 6 in Task 5 and pin the exact owner sentence; test bullet 6 has no `;;`.
  sources: R1-F5

<!-- Source: Variant 1 R1-F6 (base), narrowed to the 40-character half + Round 2 V1 rebuttal (b); merged per Change #7 -->
- id: M-F9
  grade: minor
  class: gap
  claim: The 40-character unique-substring quote match is dropped without being listed as a deviation; plan:63 has no minimum length or uniqueness rule, so a short quote attaches to any hunk.
  evidence: source.md:224 "normalisation, 40-character unique-substring quote match"; plan line 63. Round 2 V1 (b): "plan:63 has no minimum length or uniqueness rule, so a short quote such as "the" attaches to any hunk." Calibration: "40-char rule only a mitigation in source.md:224".
  tag: Grounded (source.md:224 text); [INFERRED] (whether the rule is a requirement or only a mitigation)
  fix: State the quote-match rule in Task 2 or list it as not implemented.
  sources: R1-F6 (40-character half only); Round 2 V1 (b); debate C-012

<!-- Source: Variant 1 R1-F7 (base) + Round 2 V1 rebuttal (c); evidence appended per Change #8 -->
- id: M-F10
  grade: minor
  class: unverifiable-AC
  claim: The Task 1 subprocess test does not prove no superclaude import is needed when superclaude is installed in the active environment; a lazy function-level import passes both checks.
  evidence: plan lines 50 and 52. Round 2 V1 (c): "plan:52 pattern `^(import|from) ` is column-0 anchored and misses function-level imports; plan:50 subprocess runs only `hash`; a lazy `from superclaude...` in `check` or `snapshot` passes both."
  tag: [INFERRED]
  fix: Run the subprocess with -I or a scrubbed environment and assert sys.modules has no superclaude entry.
  sources: R1-F7; Round 2 V1 (c); debate C-013

<!-- Source: Round 2.5 INV-004 (LOW); merged per Change #6 -->
- id: M-F11
  grade: minor
  class: gap
  claim: "Corrected once and re-run" does not say what a second exit 2 does, on either the reviser or the reviewer path; the M-F2 sentence would copy the gap.
  evidence: INV-004: "neither reviser path (source.md:43, :127) nor reviewer path (source.md:46) says what a second exit 2 does; the C-002 sentence copies the gap; one clause (second exit 2 handled like exit 3) closes it".
  tag: Grounded
  fix: In the M-F2 sentence, state that a second exit 2 is handled like exit 3 (stop and escalate).
  sources: INV-004

<!-- Source: Variant 2 R2-F2, reframed per Variant 3 (debate C-003, X-001) + Round 2 V2 rebuttal (c); merged per Change #9 -->
- id: M-F12
  grade: minor
  class: structural
  claim: The compatibility checks the source requires in the first implementation task run in Task 5 instead. The move is necessary, because before Task 5 the new command does not exist and there is nothing to trip, but the plan does not declare it as a deviation.
  evidence: source.md:90 "the first implementation task runs them"; plan line 119 "Run the 'check first' tests of source.md section 3.1" in Task 5, with the regression command at line 124. Calibration: "before Task 5 the new command does not exist, so an early run proves little". Round 2 V2 (c): "running the tests there is a necessary but undeclared deviation".
  tag: Grounded
  fix: State the move to Task 5 as a deviation in Constraints.
  sources: R2-F2 (reframed); Round 2 V2 (c); debate C-003, X-001

<!-- Source: Variant 3 R3-F2, narrowed (substring half dropped); merged per Change #10 -->
- id: M-F13
  grade: minor
  class: unverifiable-AC
  claim: The pin "the `~/.claude/` path precedes the `.claude/` path" is ambiguous: read over the whole file it fails, because bullet 5 names the project .claude/ path first and must stay byte-identical.
  evidence: plan line 122; src/superclaude/commands/spec-panel.md:262; tests/skills/test_spec_panel_review_loop.py:136-138; plan line 103. Calibration: "whole-file order pin really fails because of line 262; the "can never fail as substring" half is wrong".
  tag: Grounded
  fix: Scope the check to the `## Fix Budget` section and use a lookbehind `(?<!~/)\.claude/skills/sc-fixcheck/`; apply the same scoping to Task 4 (plan:103).
  sources: R3-F2 (path-order half only); debate C-008

<!-- Source: Variant 3 R3-F4; merged per Change #11 -->
- id: M-F14
  grade: minor
  class: gap
  claim: INSTALL.md's pre-run probe needs one valid and one invalid fixture on disk, but no task creates them.
  evidence: plan line 163; Task 8 file list line 158; source.md:180.
  tag: Grounded
  fix: Task 8 adds .dev/brainstorms/346-minfix/probe/{valid,invalid}/ fixtures with exit-0/exit-1 ACs, or INSTALL.md states the coordinator writes them.
  sources: R3-F4; debate C-010

<!-- Source: Variant 3 R3-F5 + Round 2 V3 rebuttal (c); merged per Change #11 -->
- id: M-F15
  grade: minor
  class: gap
  claim: test_worker_contract.py's write-verb audit scans every file under src/superclaude/{skills,commands,agents}; the plan does not warn that new text must avoid git add/commit/push/merge/stash, gh pr and gh api tokens, and Task 4 does not run that test, so a SKILL.md hit is found one task late.
  evidence: tests/skills/test_worker_contract.py:1940-1950 (AUDIT_ROOTS, WRITE_VERB_RE) and 3129-3130 test_every_write_verb_hit_is_classified; plan line 20. Round 2 V3 (c): "spec-panel.md has no git/gh write verbs; plan:124 catches new hits. Small gaps: Task 4 (plan:106) does not run the test, so a SKILL.md hit is found one task late".
  tag: Grounded
  fix: Add that rule to Constraints.
  sources: R3-F5; Round 2 V3 (c); debate C-011

### Self-Audit
<!-- Source: self-audits of Variants 1-3, calibration blocks, Round 2.5 INV-006 and INV-007; merged per Change #12 -->
Verified (by at least one reviewer or the fault-finder, read-only):
- Task order 1-6, 5->7, 6+7->8 holds (reviewer-3). Task 7's byte-identity AC holds if the M-F2/M-F3 sentences are written into the region-4 definition at plan:117 (INV-008).
- Tests that enumerate shipped commands or skills: test_routing_refresh.py:647 fails without M-F1; test_worker_contract.py:834 passes because the Unattended heading is removed (plan:115); test_worker_contract.py:1985 passes unless M-F15 tokens are added; test_model_alias_policy.py, test_how_we_work_routing_table.py, test_graph_command.py, test_cli_install.py and test_routing_plugin_parity.py are not tripped (INV-007; reviewer-3). test_model_alias_policy.py scans the new files but no assertion trips on them (Round 2 V1 (d)).
- Sync targets skip `__pycache__`: sync-dev (Makefile:117), verify-sync (Makefile:178), test_routing_plugin_parity.py:25 (INV-006; reviewer-3).
- The six brief sources exist and the substitution holds (T05/T07/T09 one hit each; T08/T10 none; T09 keeps "any finding of any severity is FAIL"); spec-panel.md has 486 lines and line 220 is its only src/superclaude hit (reviewer-1). Owner decisions reach tasks with checkable ACs (plan lines 21, 22, 23, 24, 67, 115).

Not verified:
- That bullets 1-7 at 95f2c6e4 equal the 486-line text's bullets (all three reviewers and the fault-finder).
- No tests were run; every "fails"/"passes" above is read from code.
- /tmp brief sources were not checked by reviewer-3 (no shell).

Calibration notes: confidence_calibrated reviewer-1 0.81 (self 0.75), reviewer-2 0.70 (self 0.96), reviewer-3 0.80 (self 0.85). risks_missed recorded by the calibrators: volatile /tmp brief sources (all three); sc-fixcheck folder exists without SKILL.md between Tasks 1 and 4 (reviewer-2); other tests that enumerate shipped skills (reviewer-3, answered by INV-007).

### Not merged
- X-002 — adding tests/skills/test_model_alias_policy.py to the regression run (originally part of R1-F1's fix). Excluded unanimously: the test scans the new files but no assertion trips on them (Round 2 V1 (d), withdrawn by its author).
- C-003 as originally framed by reviewer-2 — run the check-first tests at the start of Task 1. Excluded unanimously: before Task 5 nothing exists to trip them; kept only as the declared-deviation note M-F12.
