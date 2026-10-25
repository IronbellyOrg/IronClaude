reviewer_id: 2
persona: qa
model_class: haiku
findings:
  - id: R2-1
    kind: unworkable_check
    severity: medium
    tasks: [Task 5]
    claim: "The backslash-before-backtick acceptance check is a broken Markdown code span, so an executor cannot tell which grep must be 0. A wrong render can pass, which breaks the quality rule that every acceptance bullet fails on a wrong edit."
    evidence: ["TASK-WF-spec-20261022-211556.md:94", "source.md:24", "source.md:38", "coverage-matrix.yaml:233-241"]
    card_ref: C2
    recommendation: "Rewrite the Task 5 bullet as a fenced command that searches render-after for a backslash immediately before a backtick and requires a count of 0, and state that any nonzero count fails the task."
    confidence: 0.93
  - id: R2-2
    kind: unworkable_check
    severity: medium
    tasks: [Task 6]
    claim: "The stub run says to replace git push and gh with PATH stubs, but the step also runs git config, git add, git diff --cached, and git commit. A git binary that only logs arguments fails a correct script; the task never says non-push git commands must call real git."
    evidence: ["TASK-WF-spec-20261022-211556.md:114", "pull-sync-framework.yml:89-109", "source.md:10"]
    card_ref: C3
    recommendation: "In Task 6, require the git stub to log arguments and exec real git for every subcommand other than push, and require the gh stub only to log arguments and print the scripted pr-list count."
    confidence: 0.9
  - id: R2-3
    kind: ambiguity
    severity: medium
    tasks: [Task 9]
    claim: "Replacing only scripts/README.md lines 7-12 leaves line 3 and the Required Secrets, Release steps, line 39, and Upload Failures text describing a publish workflow that the new paragraph says was removed. The spec forbids editing those lines, and the plan records them as leftovers only after the contradictory edit."
    evidence: ["source.md:35", "scripts/README.md:3", "scripts/README.md:7-14", "scripts/README.md:16-28", "scripts/README.md:39", "scripts/README.md:49-53", "TASK-WF-spec-20261022-211556.md:26", "TASK-WF-spec-20261022-211556.md:146-160"]
    card_ref: C1
    recommendation: "Before Task 9, add a user question asking whether those neighbor lines may be updated. If the user says no, keep the leftover list and state in the task that the README will stay inconsistent on purpose."
    confidence: 0.88
  - id: R2-4
    kind: unworkable_check
    severity: medium
    tasks: [Task 8]
    claim: "Task 8's acceptance checks pass a wrong README. The boundary and sync paragraphs only need the words advisory, sync/framework, and pull request, and the badge check never requires test.yml. A paragraph that still says the job blocks merges, or a badge that points at another IronbellyOrg workflow, still passes."
    evidence: ["TASK-WF-spec-20261022-211556.md:134-144", ".github/workflows/README.md:30", ".github/workflows/README.md:35", ".github/workflows/README.md:43", ".github/workflows/README.md:124", "source.md:34", "source.md:38"]
    card_ref: null
    recommendation: "Tighten Task 8 acceptance so the boundary paragraph contains cannot block and does not contain gates or branch protection must require; the sync paragraph contains does not push to master; both badge URLs contain actions/workflows/test.yml."
    confidence: 0.86
  - id: R2-5
    kind: ordering
    severity: low
    tasks: [Task 2, Task 3, Task 4, Task 6, Task 7]
    claim: "Every Depends on names one task, but several links do not reflect real order. Codecov research does not gate the GitHub API check or the throwaway diff proof, and the sync edit does not gate the boundary edit. Task 7 needs Task 2, not Task 6."
    evidence: ["source.md:40", "TASK-WF-spec-20261022-211556.md:43", "TASK-WF-spec-20261022-211556.md:53", "TASK-WF-spec-20261022-211556.md:65", "TASK-WF-spec-20261022-211556.md:101", "TASK-WF-spec-20261022-211556.md:119"]
    card_ref: C6
    recommendation: "Keep Task 2, Task 5, and Task 9 after their real predecessors. Point Task 3 and Task 4 at Task 1, Task 6 at Task 1, and Task 7 at Task 2. One Depends on line cannot name two tasks, so sequence Task 8 after Task 7 and state in Task 8 that Tasks 5 and 6 are already ancestors."
    confidence: 0.84
  - id: R2-6
    kind: unworkable_check
    severity: low
    tasks: [Task 5]
    claim: "The header check is pinned to sed lines 19-20, and summary item 3 is pinned to the next two lines. A reword that moves gates or branch protection must require onto the following line passes, and a correct wrap onto a third line can fail."
    evidence: ["TASK-WF-spec-20261022-211556.md:88", "TASK-WF-spec-20261022-211556.md:91", "boundary-guard.yml:19-20", "boundary-guard.yml:66-67", "source.md:19", "source.md:38"]
    card_ref: C4
    recommendation: "Match the header by the gating sentence text, not by line numbers 19-20. Match summary item 3 from the PR-review discipline line through the next item or the blank line, and fail if that block still contains branch protection must require."
    confidence: 0.85
  - id: R2-7
    kind: ambiguity
    severity: low
    tasks: [Task 5, Task 6, Task 7, Task 8, Task 9]
    claim: "Acceptance criteria tell the executor to run git show <t1-head>:... and to use <decided file input>, but no task says to substitute ./artifacts/t1-head.txt and the Task 2 Decision line. A literal command fails a correct edit."
    evidence: ["TASK-WF-spec-20261022-211556.md:39", "TASK-WF-spec-20261022-211556.md:87", "TASK-WF-spec-20261022-211556.md:112", "TASK-WF-spec-20261022-211556.md:124", "TASK-WF-spec-20261022-211556.md:144", "TASK-WF-spec-20261022-211556.md:156"]
    card_ref: C5
    recommendation: "In Task 1, define t1-head as the exact text of ./artifacts/t1-head.txt. In Task 2, define the Decision file-input token. Tell later tasks to substitute those values and to fail if the angle-bracket placeholders are still present in the commands they run."
    confidence: 0.8
  - id: R2-8
    kind: coverage_gap
    severity: low
    tasks: []
    claim: "The plan correctly adds no task for the 300-versus-3000 path-filter note, but it also never verifies current GitHub docs or records the question. An executor who follows only the tasklist will drop that obligation."
    evidence: ["source.md:47", "TASK-WF-spec-20261022-211556.md:17-28", "TASK-WF-spec-20261022-211556.md:146-160", "coverage-matrix.yaml:427-434"]
    card_ref: null
    recommendation: "Add a constraint, not a task, that the session report must quote current GitHub path-filter docs and ask the user about the contract3 header's 3000-file figure versus the bot's 300-file claim."
    confidence: 0.77
  - id: R2-9
    kind: other
    severity: low
    tasks: [Task 4, Task 5, Task 8, Task 9]
    claim: "Three mapped rows point at the wrong task. The three-dot proof is Task 4, not Task 9. The advisory README entry is Task 8, not Task 5. Change nothing else in scripts/README.md is Task 9, not Task 6. The plan still covers each one."
    evidence: ["coverage-matrix.yaml:251-259", "coverage-matrix.yaml:323-331", "coverage-matrix.yaml:350-358", "TASK-WF-spec-20261022-211556.md:63-71", "TASK-WF-spec-20261022-211556.md:134-137", "TASK-WF-spec-20261022-211556.md:154-156"]
    card_ref: null
    recommendation: "No tasklist edit. Correct the matrix best_item values to Task 4 for INF-025, Task 8 for INF-033, and Task 9 for INF-036 so later reviewers do not treat the lexical match as the covering task."
    confidence: 0.91
  - id: R2-10
    kind: other
    severity: low
    tasks: [Task 1, Task 9]
    claim: "The matrix skips requirement-bearing sentences that the plan does implement. Missing quotes are the YAML-parse warning, the ban on unscoped git diff --stat and master...HEAD, the end-of-plan path allowlist, and the uv run rule."
    evidence: ["source.md:38", "source.md:39", "source.md:40", "TASK-WF-spec-20261022-211556.md:21-22", "TASK-WF-spec-20261022-211556.md:157-159", "coverage-matrix.yaml:359-408"]
    card_ref: null
    recommendation: "No tasklist edit. Add inferred matrix rows for those four clauses so union coverage is not understated."
    confidence: 0.83
unmapped_row_verdicts:
  - {row: INF-001, verdict: covered, where: "Task 6"}
  - {row: INF-003, verdict: covered, where: "CON-2"}
  - {row: INF-037, verdict: partial, where: "Task 5"}
  - {row: INF-040, verdict: covered, where: "Task 9"}
  - {row: INF-041, verdict: partial, where: "Task 3"}
  - {row: INF-042, verdict: covered, where: "tasklist"}
  - {row: INF-045, verdict: partial, where: null}
overall_verdict: not_ready
self_confidence: 0.82
self_audit: "Read source.md, all 9 tasks and 10 constraints, the full 45-row matrix, t1-card claims C1-C9, boundary-guard.yml, pull-sync-framework.yml, test.yml Codecov step, both READMEs, ci.py name match, and the boundary-guard pytest path assertions. Confirmed Fix 1-4 bodies are tasked; rejected no card claim. Unmapped rows judged above. Matrix false task ids and skipped sentences are R2-9 and R2-10."