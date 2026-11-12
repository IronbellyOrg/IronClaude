# Pairs P31 to P40 (detail version)

For each pair, read complaint A and complaint B. They come from two different reviewers of the same plan.
Question: would ONE edit to the plan (or spec) fix both complaints? If yes, they are the same problem.
Write yes or no after the colon on the line that starts with ANSWER. Do not change anything else.
If one complaint lists several problems, answer yes when one of those problems is the other's problem.

## P31

A (reviewer-1-card, finding R1-1): Task 5's "exited 0" assertion can pass with the old contradicting sentence still in place ("The run is succeeded when the audit finished, and failed otherwise" at init-lite.md:92; "`succeeded` when the audit finished, else `failed`" at SKILL.md:61). No existing pin catches this (test_worker_contr...
   points at: source test_worker_contract.py:777-797 ; source init-lite.md:92-92 ; source SKILL.md:61-61 ; source TASK-WF-workerContractFo-20261106-214402.md:76-76

B (reviewer-3-card, finding R3-5): return-contract.md (installed skill ref) never mentions WORKER-CONTRACT.md, so a bare "WC-4" pointer in its YAML comment cannot be followed; no criterion forbids a src/superclaude/ path in the pointer text.
   points at: source return-contract.md:43-54 ; source TASK-WF-workerContractFo-20261106-214402.md:43-43

ANSWER P31:

## P32

A (reviewer-1-card, finding R1-07): At P0 no `--unattended` exists, so the /sc:workflow worker runs `git add .dev/tasks` in its disposable worktree. Step 6 compares paths only. Plan line 22 also overclaims that the only git-state changes are worktree create and remove.
   points at: source SKILL.md:28-28 ; source WORKER-CONTRACT.md:42-42 ; plan TASK-WF-writeTheP0LivePl-20261103-215902.md:22-22

B (reviewer-3-card, finding R3-08): plan:29 defines a skip only for a failed worktree setup. Two other failures are left open. A worker-start failure still owns a terminal that must be released. A Step 3 stall, or a decision question left unanswered, leaves an unsettled worker, and release needs an accepted settlement first. The co...
   points at: plan TASK-WF-writeTheP0LivePl-20261103-215902.md:29-29 ; source orca-capabilities.md:112-112 ; source orca-capabilities.md:108-108 ; source WORKER-CONTRACT.md:73-73

ANSWER P32:

## P33

A (reviewer-1-card, finding R1-5): The C-install-surface recipe symlinks /usr/local/bin/node, which does not exist on this host; under env -i the uv cache moves into the throwaway HOME; claude credentials unverified.
   points at: source C-install-surface.md:130-134 ; source TASK-WF-closeIronbellyOr-20261104-084334.md:98-98

B (reviewer-3-card, finding R3-5): Nothing forbids copying credentials from /home/coder/.claude into the throwaway to make M1c's session part work.
   points at: source TASK-WF-closeIronbellyOr-20261104-084334.md:22-22 ; source TASK-WF-closeIronbellyOr-20261104-084334.md:100-100

ANSWER P33:

## P34

A (reviewer-1-card, finding A-11): No invented functional requirement; additions beyond the spec are verification-only checks.
   points at: source TASK-WF-design-20261104-164423.md:176-176 ; source TASK-WF-design-20261104-164423.md:245-245 ; source TASK-WF-design-20261104-164423.md:270-270 ; source TASK-WF-design-20261104-164423.md:285-285 ; spec source.md:1324-1324

B (reviewer-2-card, finding Q-7): Task 20 omits step 14's staging instruction, so its 'no staged .claude/ path' check is vacuously true and .dev/tasks staging is left to memory.
   points at: source TASK-WF-design-20261104-164423.md:302-302 ; source TASK-WF-design-20261104-164423.md:307-307 ; spec source.md:1429-1429

ANSWER P34:

## P35

A (reviewer-1-card, finding A-9): Dropping 'make test' is the documented orchestrator constraint (Authorized); residual: line 19 'source wins' does not state the exception and nothing records VG-2 was not run; the tests/cli/reflect blast radius is smaller than claimed because every tests/pr_submit test already imports the package.
   points at: source TASK-WF-design-20261104-164423.md:19-19 ; source TASK-WF-design-20261104-164423.md:28-28 ; spec source.md:1408-1408 ; spec source.md:1429-1429 ; source TASK-WF-design-20261104-164423.md:169-178 ; source commands.py:99-99

B (reviewer-2-card, finding Q-5): TL:29 drops the section 12 preamble's fixed author and committer, and Task 19 lacks the merge-tree capability skip; git commit under GIT_CONFIG_GLOBAL=/dev/null fails without an identity, breaking F9, F10, X1, X3.
   points at: source TASK-WF-design-20261104-164423.md:29-29 ; source TASK-WF-design-20261104-164423.md:291-291 ; spec source.md:1316-1316 ; source TASK-WF-design-20261104-164423.md:186-186

ANSWER P35:

## P36

A (reviewer-1-card, finding R1-F11): Consistent: tasks 1-66 map to all items and gaps 1-70; ground facts (pyproject.toml:7, counts, transcript ranges, DECISIONS B1-B5, severity test path, RELEASE-READINESS 6.3, D10 fixture) verified.
   points at: source pyproject.toml:7-7 ; source CONSOLIDATED-PLAN.md:237-237 ; source CONSOLIDATED-PLAN.md:675-675 ; source c-e2e-transcript.txt:416-416 ; source c-e2e-transcript.txt:724-775 ; source DECISIONS.md:12-19 ; source RELEASE-READINESS.md:186-200

B (reviewer-2-card, finding R2-F6): Report/manifest exclusion and 'no issue filing' not restated in Constraints; executor reads CONSOLIDATED-PLAN whose section 6 (line 636) instructs filing O1-O22 issues.
   points at: spec source.md:36-36 ; spec source.md:38-38 ; source CONSOLIDATED-PLAN.md:636-636

ANSWER P36:

## P37

A (reviewer-1-card, finding R1-F6): Plan omits the Tier A/B/C grouping and template header fields (Capability, Audience, Source of truth, Est. time; Gate for sysop) required by the Test guide plan.
   points at: source CONSOLIDATED-PLAN.md:587-587 ; source user-test-guide.md:7-12

B (reviewer-2-card, finding R2-F4): B-W12 item 6 four-note links: Task 37 does not name them and runs before Tasks 43-46.
   points at: source CONSOLIDATED-PLAN.md:481-481

ANSWER P37:

## P38

A (reviewer-1-card, finding R1-F8): Dependency declarations do not enforce ordering for Tasks 37, 47, 66 and Task 1's upgrading.md link; fine only under sequential execution.
   points at: source CONSOLIDATED-PLAN.md:481-481

B (reviewer-3-card, finding R3-F4): Task 37 omits B-W12 #6 (link four new notes) and runs before Tasks 43-46 with no dependency; AC checks in-file anchors only.
   points at: source CONSOLIDATED-PLAN.md:481-481

ANSWER P38:

## P39

A (reviewer-1-card, finding R1-F4): Backslash-newline continuation and wrapper options (nice -n, sudo -u, env -u) unspecified; false positive on 'uv run \<newline> python', false negatives for option-taking wrappers
   points at: (no citation)

B (reviewer-3-card, finding R3-F7): Never-exit-1 and fail-open not guaranteed against jq or set -u errors
   points at: (no citation)

ANSWER P39:

## P40

A (reviewer-1-card, finding F1): Task 4's acceptance criterion cannot pass at the point Task 4 runs. Task 4 depends only on Task 2, and Task 2 depends on Task 1. Task 1 creates src/superclaude/core/WORKER-CONTRACT.md. Task 3 is the task that adds that name to KNOWN_CORE_FILES. Task 4's AC-0.2 command runs tests/cli/test_how_we_w...
   points at: source test_how_we_work_install.py:43-44 ; source install_core.py:13-27 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:56-60 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:70-72 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:77-77 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:106-108 ; source source.md:298-298

B (reviewer-2-card, finding R2-1): 7.2 step 5 requires each phase report to name at least one checked run that lasted longer than the heartbeat cadence, otherwise the WC-10 heartbeat-spacing check passes vacuously (source.md:291). Task 8 is the only task that runs 7.2 in P0 and neither its instructions (TL:122) nor its acceptance ...
   points at: unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:291 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:301 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:15 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:124 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml:1410

ANSWER P40:

