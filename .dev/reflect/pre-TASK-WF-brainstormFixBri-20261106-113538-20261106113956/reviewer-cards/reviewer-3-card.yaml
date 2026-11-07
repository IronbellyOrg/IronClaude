# Reviewer 3 card (refactorer lens, opus slot = claude-gw-tier1a), persisted verbatim by the orchestrator from the reviewer's reply.
# Orchestrator check at 2026-11-06T11:50Z for R3-1: `git status --porcelain -- .dev/tasks` prints only `A`/`R` lines plus
# `?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/` (this package, which the AC exempts); no `AM` line.
reviewer: 3
lens: "refactorer (structure and maintainability); pre-execution plan audit, read-only"
plan: ".dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md"
brief: ".dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md"
findings:
  - id: R3-1
    priority: P2
    claim: >
      Task 7 bullet 3 exempts new status lines only when they name one of the six files or a path under
      this package's folder. /sc:implement's rule is `git add .dev/tasks`, which stages the whole tree, not
      just this package. Any other untracked path under .dev/tasks/ at Task 1 time would show up as new
      `A` lines in status-after.txt. That includes the two earlier brainstorm packages created today (001016
      and 021737), and a done-archive file that is staged and then modified (`AM`) would change too. Those
      lines are outside the exemption, so the AC could not pass. This is the same infeasible-AC class that
      F-2 fixed, and the brief's INV-001 reasoning covered only this package's `??` to `A` flip.
      [INFERRED] whether those paths are untracked today: the session git-status snapshot is truncated and
      I could not run git.
    evidence: "plan:158; plan:33; src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:36 ('`git add .dev/tasks`'); source.md:53 (exemption reasoned only for this package); .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/ and -021737/ exist (Glob)"
    exact_change: >
      In Task 7 bullet 3, replace "or a path under this package's folder" with "or a path under
      `.dev/tasks/to-do/`". Keep the `.dev/tasks/done/` clause unchanged. If the brief's exact F-2 text must
      stay byte for byte, add instead one sentence to Task 1: "If `status-before.txt` lists any `??` path
      under `.dev/tasks/` outside this package, run `git add .dev/tasks` before saving the snapshot."
    verifier: >
      Before running the plan, `git status --porcelain -- .dev/tasks` prints no `??` line and no `AM` line.
      If that holds, the finding is void. Otherwise Task 7 bullet 3 names `.dev/tasks/to-do/`.
  - id: R3-2
    priority: P2
    claim: >
      Tasks 1, 2, 3 and 6 say "copied character for character", but no acceptance check compares the full
      text. Each AC pins only short substrings. Task 6 is the weak spot: no test reads the spec, so the
      clauses that carry the owner amendment are not checked anywhere. Those clauses are "(not a `Task` or
      `Agent` call whose prompt only names `/sc:analyze`)", "returns no tool error", "the `codebase` entry is
      not `skipped`", "did not refuse that directory" and "recorded `not verifiable`, never PASS". An
      executor could paraphrase or drop any of them and every Task 6 AC would still pass.
    evidence: "plan:117 and plan:119/125 ('copied character for character'); plan:128 (full sentence); plan:143-145 (four positive pins, one negative pin, diff shape only); Grep of tests/ for 'orca-worker-contract-spec' finds no file"
    exact_change: >
      Add one AC to Task 6: "Each of the two fenced sentences in this task, saved verbatim to
      `./artifacts/t6-companion.txt` and `./artifacts/t6-livecheck.txt`, occurs exactly once in the spec
      (`grep -cxF` is not usable because the sentence is appended to a line, so use
      `grep -cF -f ./artifacts/t6-livecheck.txt <spec>` prints 1, and the same for the companion file)." Use
      the same pattern for Tasks 1 and 3 (one appended or replaced span each) and for Task 2
      (`grep -cxF` on the bullet prints 2). This adds no new pins, so it does not conflict with F-7's
      "exactly these pins". It is a byte check of text the brief already fixes.
    verifier: "Task 6 acceptance criteria include a whole-sentence fixed-string check for both spec sentences."
  - id: R3-3
    priority: P3
    claim: >
      Task 3 is the only wording task with no diff-shape AC. Tasks 1, 2 and 6 each pin one with
      `git diff --stat`. Task 3 says "Append this text to the end of that bullet", but a new physical line
      after the bullet still passes every Task 3 AC and Task 5's section-wide phrase check, because
      `_unattended_section` reads the whole section, not the bullet. The three primitives would then differ
      in structure.
    evidence: "plan:66; plan:74-77; plan:46; plan:61; plan:145; tests/skills/test_worker_contract.py:483-496 (_unattended_section spans the whole section)"
    exact_change: "Add to Task 3's acceptance criteria: \"`git diff --stat -- src/superclaude/commands/brainstorm.md` shows one line changed (one insertion, one deletion).\""
    verifier: "Task 3's AC list contains a git diff --stat bullet for src/superclaude/commands/brainstorm.md."
  - id: R3-4
    priority: P3
    claim: >
      The "fails on pre-change text" checks are inconsistent and claim more than they show. Task 4 guards
      its `git show HEAD:... | grep -c` checks with `git cat-file -e`. Task 5's identical check has no guard,
      so a wrong path makes `git show` fail, `grep -c` prints 0, and the check passes for nothing. Both
      tasks also test only the `write(s) no nested directory and no nested contract` phrase, while the text
      says "which shows the pins fail". The second shared pin, ``only by a `/sc:analyze` call``, and the
      paragraph `fallback_1` pin are not checked against HEAD.
    evidence: "plan:95 (cat-file guard present); plan:111 (no guard); plan:90 (claim that every pin fails on pre-change text)"
    exact_change: >
      In Task 5 bullet 4, append "and `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` exits 0".
      In both Task 4 and Task 5, add the ``only by a `/sc:analyze` call`` phrase to the HEAD grep, or change
      "which shows the pins fail" to "which shows the shared directory pin fails".
    verifier: "plan Task 5 bullet 4 contains `git cat-file -e`; the HEAD checks in Tasks 4 and 5 name both shared pins, or the wording is narrowed."
  - id: R3-5
    priority: P3
    claim: >
      Task 7 has no baseline for `make lint` or `make verify-sync`, and its logs record no exit codes.
      `make lint` runs `uv run ruff check .` over the whole repository. That includes the uncommitted,
      out-of-scope edits to install_core.py and test_how_we_work_install.py, so a finding there would halt
      Task 7 for a reason outside this plan. "No new ruff finding in the two edited test files" adds nothing
      once exit 0 is required. "Shows ... exiting 0" depends on the executor appending exit status, and the
      body does not ask for that. [INFERRED] whether the out-of-scope edits lint clean today.
    evidence: "plan:153; plan:156-157; Makefile:48-50; plan:27 (out-of-scope dirty files)"
    exact_change: >
      In Task 7's body, add "append `exit=<status>` after each command's output in its log". In Task 1, add
      "save `make lint` output and exit code to `./artifacts/lint-before.log`". Change Task 7 bullet 2 to:
      "`make lint` exits 0, or every finding in t7-lint.log is also in lint-before.log and none names one of
      the six files." This also covers the earlier review's carried note F-2 (ruff format).
    verifier: "Task 7 body mentions recording exit codes; Task 1 saves lint-before.log; Task 7 bullet 2 compares against it."
  - id: R3-6
    priority: P3
    claim: >
      The diff-shape ACs in Tasks 1, 2 and 6 assume that the edited files have no changes at the start. The
      only start-state guard is Task 1's status snapshot, and nothing checks it for the six files. If one of
      them was already modified, `git diff --stat` would mix old and new changes and the AC would fail or
      mislead. Task 7's before/after comparison would also hide it, because the line appears in both
      snapshots.
    evidence: "plan:44; plan:46; plan:61; plan:145; plan:27 (start state names only install_core.py and test_how_we_work_install.py)"
    exact_change: "Extend Task 1's first AC: \"... and no line of `./artifacts/status-before.txt` names one of the six files in Constraints.\""
    verifier: "Task 1's first AC states that status-before.txt names none of the six files."
  - id: R3-7
    priority: P3
    claim: >
      Task 7's body contradicts itself. It says "it writes only the logs under `./artifacts/`" (the F-13
      text), then names status-after.txt as "the one non-log file it writes there", then says make sync-dev
      rewrites the `.claude/` copies. A reader or QA gate that takes "only" literally could flag
      status-after.txt or the `.claude/` writes.
    evidence: "plan:153; source.md:169 (F-13 mandated sentence)"
    exact_change: >
      Keep the F-13 sentence verbatim and rewrite the next sentence: "Besides the logs, it writes the
      snapshot `./artifacts/status-after.txt`; `make sync-dev` also rewrites the gitignored copies under
      `.claude/` (output, not edits)."
    verifier: "Task 7 no longer pairs 'writes only the logs' with 'the one non-log file'."
  - id: R3-8
    priority: P3
    claim: >
      Owner note on wording carried from the brief. Residual risk 4 says that when the clause is
      `not verifiable`, "the spec then blocks a PASS until the owner accepts the gap in writing". The spec's
      owner-acceptance path (spec:300) is scoped to 7.2 step 5 conditions 1, 2, 4 and 5. The new clause sits
      in step 4, whose only stated pass condition is "both commands exit 0" (spec:286). The live-check
      sentence itself says "never PASS", but nothing in the spec routes a not-verifiable step-4 extra to the
      written owner acceptance. A later live-plan author could read step 4 as passed on the exit codes.
    evidence: "plan:137; plan:128; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:286; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:300; source.md:243"
    exact_change: >
      Owner decision. Either narrow residual risk 4 to "the sentence records the clause `not verifiable`,
      never PASS; the spec's written-acceptance path (7.2 step 5, Not verifiable) does not name step-4
      extras", or have the owner amend Part 4 so that the live-check sentence ends "..., never PASS, and
      the step is handled as in 7.2 step 5's Not verifiable rule".
    verifier: "Residual risk 4 no longer claims a spec mechanism the spec does not state for step 4, or the brief is amended."
self_reported_confidence: 0.74
checked_clean:
  - "Plan anchors match the files on disk: SKILL.md:195 is the paragraph, :196 is empty (no whitespace-only line in the file) and :197 is 'Quality-tier tracking'. handoff-routing.md:16/22/24/31/33/35 are as stated. brainstorm.md:157 is the Nested invocations bullet and ends 'so a nested directory is never reused.' spec:62 is the only 'Nested propagation rule' bullet (the other hit, :376, is a table row). spec:286 is step 4 and spec:142 is the brainstorm row."
  - "test anchors: test_brainstorm_protocol.py:39 (test def), :44 (assert), :47 (refs assert); test_worker_contract.py:286 (entry) and :288 (phrases list); the :704-724 mutation list rewrites a made-up section."
  - "_removals and _remove use text.replace(tok, '') on every occurrence (test_worker_contract.py:519-531). Adding a second `nested/analyze-` to the command section therefore does not break the existing removed-token case, and each new phrase adds exactly one case under -k brainstorm (ids at :562), so 'before-count plus 2' holds."
  - "_check_unattended_section and _check_nested_text (test_worker_contract.py:499-516, 864-869) accept the Task 3 text: it names no src/superclaude/ path and no Orca verb, and it keeps both nested names."
  - "Task 4 slicing is sound: `**Under `--unattended`**` occurs once in Wave 2A (the other bold hits at SKILL.md:286 and :352 are in other waves). The Tier 1 end anchor `**Tier 2 (fallback_1)**: codegraph` is distinct from the research Tier 2 at routing:48. The Tier 2 slice stays inside test_codegraph_adoption.py:75-82's span."
  - "No other test that reads the brainstorm skill, ref or command is broken by the planned text (test_codegraph_adoption mcp-servers and serena checks; test_primitive_dual_surface_lookup; test_tier2_tavily_consistency). lint-architecture's command size check counts lines, and Task 3 appends to an existing line."
  - "/sc:implement runs tasks one after another by default (sc-implement-protocol SKILL.md:97), so Task 1's status snapshot comes before Tasks 2 to 6 even though they have no 'Depends on: Task 1' line."
  - "Plan Task 1/2/3 texts and the Task 6 sentences match source.md:223, :219 and :231-233 as read side by side; the F-2, F-13, F-16 and F-17 sentences are present (plan:158, :153, :25, :22)."
