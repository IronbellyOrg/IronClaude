# Round 1 statement: Variant 1 advocate (haiku:analyzer)

Persisted verbatim by the debate-orchestrator from the advocate's returned text.

Position summary

Variant 1 is stronger at finding contradictions between the plan, executable source and snapshot contract; Variant 2 is stronger at checking required test coverage. I defend R1's main findings, but concede that its empty-state severity is too low and that QA's missing-criterion findings need separating from actual missing behaviour.

Citation key — all paths are absolute:
P = /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md
S = /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md
D = /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/install_user_setup.py
N = /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/architecture-options.md
O = /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md

Steelman of Variant 2

QA correctly treats acceptance tests as deliverables, not optional reassurance. Its strongest finding is QA-01: S:215 requires four sample kinds, "each pinned in a contract test," and says otherwise "the gate stays closed." P:63–64 establishes fixture existence and redaction, while P:86 names only the success file for parsing. Creating the remaining samples does not demonstrate their contracts.

QA also strengthens the shared deadline finding: S:369 explicitly requires that "the cycle ends within the 15 s cycle budget." P:106 checks only that "DEFAULT_TIMEOUT_S is less than 15."

Strengths claimed

1. R1-02 exposes a real side-call contradiction. P:23 says "The only live Orca call is worker-list"; D:209–213 instead executes `subprocess.run([path, "skills", "list", "--json"], … timeout=10)`. P:105 excludes subprocess access outside the injected default runner. Discovery needs an explicit boundary; the fake worker-list runner alone cannot cover it.

2. R1-03 catches misleading exported state. P:173 writes snapshots "after each successful cycle," but N:79 requires an "Envelope (one per cycle)" and N:88 defines "OK, STALE … ERROR or UNKNOWN." A success-only file cannot publish subsequent failures or STALE transitions.

3. R1-04 identifies incompatible privacy promises. P:25 prohibits any "absolute path, token or credential" being printed; P:45 removes control sequences and character classes, not printable secrets. P:157 exports `stage.detail` and `stage.activity` with "All strings … sanitized." Sanitization is not credential redaction.

4. R1-01 distinguishes detection from enforcement. P:112 reports a cycle that "overruns its 15 s budget"; P:97 permits five calls with a measured per-call timeout. Reporting an overrun after it happens does not enforce the total deadline.

Weaknesses identified in Variant 2

1. QA-04 overstates snapshot-retention absence. P:118 already requires: "A failed cycle keeps the previous snapshot readable and marks it with the failure." The remaining gap is a specific end-to-end shape-error assertion, not missing retention behaviour.

2. QA-08 includes an already-pinned item. P:182 explicitly asserts "worker-list NOT AVAILABLE (orca binary not found)." Other listed behaviours are already instructions at P:126, including "not reobserved," the selection placeholder and filter text. Additional assertions are useful, but their absence alone is minor.

3. QA-11 incorrectly says no task builds STALE/FAILED presentation. P:126 expressly lists "STALE 52s" and "FAILED (exit 2) 1m." Its narrower concern holds: S:154 requires last-known values qualified "as of HH:MM:SS," whereas the plan explicitly names only the header's "as of <HH:MM>."

4. QA-12 overlooks recorded scope context. P:20 cites owner-decisions items 1 and 5; O:17 confirms "Python + Rich with snapshot export." P:33 explicitly says a failed spike must "stop this task as blocked." The criterion's pass-or-fail artifact wording is weak, but it does not authorize continuing after failure.

Concessions

X-001: I upgrade R1-06 to blocking, agreeing with QA-02. S:172 says the empty variant "must render" the coverage warning; P:75 merely creates empty data, and P:126 does not assign the empty-state output. This is a missing required rendering deliverable, not cosmetic wording.

X-002: Missing a dedicated criterion is not automatically blocking. P:97 already instructs the paging outcomes and failure mapping, so QA-03 and the surviving part of QA-04 are minor test-specificity gaps. A contradictory implementation instruction, missing deliverable or explicit unmet gate remains blocking.

R1-04 establishes an unenforced privacy promise—not evidence that real credentials have already leaked. R1-05 establishes an incomplete dependency declaration—not proof that execution necessarily runs tasks concurrently.

Shared assumptions

A-001 QUALIFY — P:20–21 limits work to R0 foundations plus R1 and excludes question/B/C features; test scope must follow those features, not merely absence from an exclusion list.

A-002 QUALIFY — P:22 cites authorization for live calls and registration but says the formal selection record "remains a reviewer-checked item"; O:9 leaves full gate satisfaction to the owner.

A-003 QUALIFY — P:157 promises "every ledger row," but P:126 hides historical rows and applies filtering; S:189 says historical rows are "never deleted from the snapshot," requiring an explicit all-rows export invariant.

A-004 REJECT — P:80 declares only "Depends on: Task 3," while P:88 consumes Task 4's variant; numeric headings do not repair the dependency declaration.

Per-finding table

id | holds? | severity | reason
R1-01 | confirmed | blocking | Per-call limits do not enforce the cycle deadline.
R1-02 | confirmed | blocking | Discovery bypasses the declared runner boundary.
R1-03 | confirmed | blocking | Success-only publication omits required failure states.
R1-04 | narrowed | blocking | Printable sensitive text defeats the absolute privacy promise.
R1-05 | confirmed | minor | Fixture prerequisite is absent from dependencies.
R1-06 | confirmed | blocking | Required empty-state output lacks assigned implementation.
R1-07 | confirmed | minor | Partial disclosure needs explicit implementation and assertions.
QA-01 | confirmed | blocking | Four-kind contract-test gate is not satisfied.
QA-02 | confirmed | blocking | Required empty-state rendering is omitted.
QA-03 | narrowed | minor | Paging behaviours exist in instructions, not dedicated assertions.
QA-04 | narrowed | minor | Retention exists; shape-path integration assertion remains unpinned.
QA-05 | confirmed | blocking | Total collection time lacks enforced bounds.
QA-06 | confirmed | minor | Required partial disclosure is insufficiently explicit.
QA-07 | confirmed | minor | Cost behaviour is instructed but not specifically asserted.
QA-08 | narrowed | minor | Most behaviours are instructed; NOT AVAILABLE is asserted.
QA-09 | confirmed | blocking | Required per-process inspector disclosure is missing.
QA-10 | narrowed | minor | B-view rotation text should not automatically become R1 scope.
QA-11 | narrowed | minor | State cells exist; per-value stale qualification lacks explicit verification.
QA-12 | narrowed | minor | Failure-record criterion is weak, but blocking instructions prevent continuation.

Anything both cards missed

No additional confirmed finding beyond the export-completeness ambiguity identified under A-003.

Read-only review completed; no files changed, tests run, git commands executed or network accessed. Runtime behaviour remains unverified.
