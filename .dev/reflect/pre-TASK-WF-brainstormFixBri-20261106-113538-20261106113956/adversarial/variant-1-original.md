# Reviewer 1 card (analyzer lens, sonnet slot = claude-gw-tier1b), persisted verbatim by the orchestrator from the reviewer's reply.
# Orchestrator note: some citations below use line numbers of the reviewer's brief file, not of the cited file
# (lc10-result.md:396/401, orchestra spec :375/:379, test_codegraph_adoption.py:532-540, plan:114/115).
# They are re-mapped at the Wave 5 evidence gate; the claims are unchanged here.
card:
  reviewer: reviewer-1
  lens: analyzer (root cause and correctness)
  mode: pre (UC-1)
  line_numbers: "plan:N is the line in TASK-WF-brainstormFixBri-20261106-113538.md. The grounding hunk starts at plan line 1, so plan:N is the brief-file line minus 88. Other files are cited under their own names."

findings:
  - id: R1-F1
    priority: P2
    claim: >
      Task 6's acceptance criteria do not pin the decision clauses of the amended live-check sentence. The only
      content pins on the 7.2 step 4 line are `lc10`, `a source: codebase entry`, `neither quality_tier nor source
      records` and `invokes sc:analyze`, plus the absence of the old "a Skill, Agent or Task tool call". A
      paraphrase would pass every criterion. For example, one that drops the `skipped` carve-out, drops the
      "did not refuse" clause, or drops "not a Task or Agent call whose prompt only names /sc:analyze" would still
      pass. Dropping the `skipped` carve-out brings back a false FAIL on a timed-out run. Dropping the Task or
      Agent exclusion brings back the lc10-class false FAIL on a Task prompt followed by an auggie or fallback_1
      scan. The task body says "copied character for character", but nothing checks it.
    evidence: >
      plan:142-145 (the three Task 6 criteria); plan:128 (the fenced sentence);
      source.md:109 (F-7's pin list, which the plan follows);
      routing ref handoff-routing.md:77 (a timeout records `skipped`, the premise of the carve-out).
    exact_change: >
      Add a criterion to Task 6 that each of these fragments occurs exactly once in the spec file
      (`grep -cF` prints 1 for each): "(not a `Task` or `Agent` call whose prompt only names `/sc:analyze`)";
      "the `codebase` entry is not `skipped`"; "did not refuse that directory"; and
      "this last clause is recorded `not verifiable`, never PASS". Alternatively, require
      `grep -cF` of the whole fenced sentence from plan:128 to print 1.
      This is an addition to the F-7 pin list, so record it next to the negative check (card finding F-1 / R-1).
    verifier: "Task 6 lists the four fragment checks (or the whole-sentence check) and each prints 1 after the edit."

  - id: R1-F2
    priority: P3
    claim: >
      The live-check sentence says when the folder is NOT required ("is required ... only when ...") but never
      says it is required when every condition holds. "Only when" gives a necessary condition, not a sufficient
      one. A literal checker can never reach a FAIL, because every no-folder case can be read as "not required".
      The intended reading is "required exactly when", and the brief's "a run that failed included" rule needs
      that reading. The text is the owner's amended wording, so it must stay byte for byte. This is an owner note,
      not a plan defect.
    evidence: "plan:128; source.md:219"
    exact_change: >
      Owner decision only. If the owner agrees, change "only when" to "exactly when" in source.md:219 and in
      plan:128 together. Otherwise record the ambiguity in the residual-risk list at plan:133-138.
    verifier: "plan:128 equals source.md:219 and the residual-risk list or the sentence names the intended reading."

  - id: R1-F3
    priority: P3
    claim: >
      Two clauses of the sentence cannot be tested the way they are written, and one of them can give a false
      FAIL. (a) "returns no tool error" says almost nothing about a Skill call to a slash command. The call
      returns once the command is loaded, so a failed or abandoned /sc:analyze still shows no tool error.
      That is harmless for a failed run, because analyze writes its contract on every outcome. It also means a
      Skill call that loads analyze and is then abandoned makes the folder required. (b) "/sc:analyze did not
      refuse that directory" has no recorded form. The refusal is "printed in chat only" (analyze.md:97), so the
      checker must read assistant text with no defined marker. A refused call (no directory written) that the
      checker misses as refused makes the folder required and absent, which is a false FAIL on a correct run.
      This contradicts plan:133 ("no known false FAIL"). Separately, the match on
      `--report-dir <report directory>/nested/analyze-<n>/` is literal. A call that omits the trailing slash or
      uses a relative path is not matched, which gives a false PASS.
    evidence: >
      analyze.md:97 (refusal printed in chat only), analyze.md:98 (contract written on every outcome);
      plan:128; plan:133; plan:135 (residual risk 2 covers the encoding but not the refusal marker).
    exact_change: >
      Add one residual-risk line to Task 6 after plan:138: the refusal clause is read from the worker's chat text
      because analyze records no marker, and a missed refusal gives a false FAIL, so the checker records
      `not verifiable` for that call. Do not change the sentence itself.
    verifier: "Task 6's residual-risk list names the refusal-marker case and the literal --report-dir match."

  - id: R1-F4
    priority: P3
    claim: >
      Task 7's third criterion and Task 6's `git diff --stat` criteria compare against HEAD and the starting
      status. They hold only if the six files are clean at the start. Task 1's first criterion checks that
      status-before.txt exists and nothing about the six files. If one of them were already dirty, the
      "one line changed" or "two lines changed" criteria would fail for a reason unrelated to the edit.
      The working tree is not shown in full here: the git status in the context is truncated.
    evidence: "[INFERRED] plan:46 (Task 1 criterion 1), plan:46-47, plan:145, plan:158, plan:115 (Constraints list the dirty files)"
    exact_change: >
      Add to Task 1's first criterion: none of the six Constraints files appears in ./artifacts/status-before.txt
      (grep of the six paths prints nothing), and stop and report if one does.
    verifier: "Task 1 states the six-path check and its outcome is in status-before.txt."

  - id: R1-F5
    priority: P3
    claim: >
      Task 7's lint criterion needs `make lint` to exit 0, and `make lint` runs ruff over the whole repository
      (Makefile:48-50). The tree already holds uncommitted edits to src/superclaude/cli/install_core.py and
      tests/cli/test_how_we_work_install.py that are not part of this work. A ruff finding there would fail the
      criterion for a reason this plan cannot fix, or it could be skipped without a record. Task 7 also forbids
      editing source files.
    evidence: "Makefile:48-50; plan:115; plan:157 (Task 7 criterion 2)"
    exact_change: >
      Reword the criterion: `make lint` exits 0, or every reported finding is listed in t7-lint.log and none is in
      the six edited files. Say what to do for a pre-existing finding (report it, do not fix it).
    verifier: "Task 7's lint criterion has a rule for findings outside the six files."

  - id: R1-F6
    priority: P3
    claim: >
      Owner note for the P2 live-plan author. The amended sentence says the analyze Skill call may sit in a
      subagent file, which is right. The routing ref sends all enrichment sources through `Task` agents
      (handoff-routing.md:77), so a correct codebase wave will usually have its /sc:analyze Skill call there.
      Spec 7.2 step 5 condition 2 requires "the Skill or command call is a top-level message, not a subagent
      message". The lc10 note extended it to the nested calls (lc10-result.md:401). Read that way, a correct
      run could be failed by condition 2 for the nested analyze call, even though step 4's extra accepts it.
      The plan does not edit condition 2 and says nothing about this interaction.
    evidence: >
      orca-worker-contract-spec.md:375 (condition 2 speaks of "the command"); lc10-result.md:401;
      handoff-routing.md:77; plan:128.
    exact_change: >
      Add one clause to Constraints beside the open P2 conflict at plan:114, or to Task 6's residual risks:
      condition 2 applies to the command under test, not to nested calls made through `Task` agents. Do not edit
      the spec beyond the two planned lines.
    verifier: "The plan names the condition 2 interaction as an owner item."

  - id: R1-F7
    priority: P3
    claim: >
      The appended extra sits on the step 4 line, whose Pass rule is "both commands exit 0". The extra reads the
      session file (step 5 material) and has no verdict of its own. lc10 recorded it as a separate "Extra:" line.
      Residual risk 4 says "the spec then blocks a PASS". That is true only for a missing, ambiguous or unreadable
      session file (spec:379, which fails step 5). It is not true when the file is readable and the Skill call is
      simply not recognised, which is residual risk 2 and gives a false PASS.
    evidence: "orca-worker-contract-spec.md:379; lc10-result.md:396; plan:136; plan:138"
    exact_change: >
      Narrow the wording of risk 4 at plan:136 to say the block follows from spec 7.2's not-verifiable
      paragraph only when the session file is missing, ambiguous or unreadable.
    verifier: "plan:136 states the condition under which the spec blocks a PASS."

self_reported_confidence: 0.7

checked_clean:
  - "Anchors: SKILL.md:195 (Wave 2A paragraph, `**Under `--unattended`**` lead-in, the only one inside Wave 2A; the others are at :93 and :286, outside it), handoff-routing.md:16/22/24/31/33, brainstorm.md:157, spec :62 and :286 all match the plan's descriptions."
  - "Task 4 slicing: the first `**Tier 1 (primary)**` in the routing ref is line 16 (the research tiers are at 42 and 63). The Tier 2 anchor is unique, and the Quality-tier boundary check is sound because the next blank line follows SKILL.md:195."
  - "Task 5: `_removals` adds one parametrized case per phrase (test_worker_contract.py:519-527, 559-568), so the +2 count is right. `_check_unattended_section` only bars `src/superclaude/` and Orca command names (:515-516). None of the planned text names either."
  - "Phrase forms: 'write no nested directory...' (skill) and 'writes no nested directory...' (ref and command) are not substrings of each other. The plan keeps them separate in Task 4 and Task 5, so the HEAD grep counts of 0 are valid."
  - "Task 2: the new Tier 2 bullet stays inside the span test_brainstorm_tier2_names_codegraph_files_and_search reads (test_codegraph_adoption.py:532-540), and the 'Glob for files matching topic keywords' check is untouched."
  - "Wrong-reason pass of the tier pins: separate exactly-once pins per tier slice cannot be satisfied by two bullets in one tier. The grep -c 2 in Task 2 is correctly marked as a smoke check."
  - "Amended sentence against the lc10 case: a Task prompt followed by an auggie or fallback_1 scan has no Skill call to sc:analyze, so no folder is required and the lc10 false FAIL does not recur."
  - "Amended sentence against the other cases: a clean analyze run passes with its folder present; a failed analyze run still requires the folder, which exists because analyze writes its contract on every outcome (analyze.md:98); a timed-out (`skipped`) call is exempt, consistent with handoff-routing.md:77; an Unknown-skill tool error is exempt."
  - "Plan content equals source.md:219/223/231-235 for the sentences and applied texts I compared. Task 6's fenced sentence equals source.md:219. The Task 1 text equals source.md:231. The Task 2 bullet equals source.md:232. The Task 3 text equals source.md:233."
  - "`./artifacts/` resolves to the package folder per sc-implement-protocol managed-workspace.md:33, so Task 1 and Task 7 write inside the package, not the project-root artifacts/."
  - "sync-dev and verify-sync output goes under the gitignored .claude/ and the Makefile does not write to plugins/, so the status comparison in Task 7 is not tripped by them. .ruff_cache, .venv and uv.lock are gitignored (.gitignore:56,169,177,222)."
  - "No plugin copy of the brainstorm skill or ref exists (only plugins/superclaude/commands/brainstorm.md), so leaving plugins/ untouched has no parity test against it."

unverified:
  - "I could not run git, so the cleanliness of the six files at the start (R1-F4) and a real `make lint` run are inferred, not observed."
  - "How a Skill call to a slash command is recorded in the session file (name, args, tool_result) is not observed; it matches the plan's own residual risk 2."
