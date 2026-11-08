3a39908e75dd9490d059f2ecb764d9d64d90b478
Review one task for spec compliance.

Task brief: ## Task 21: Record the L2 pre-push disposition

Depends on: Task 1

Create ./artifacts/l2-disposition.md from the L2 verdict in ./artifacts/b-ctx-verdict.md. If that verdict is L2: BLOCKED, the file states that this plan builds no pre-push file, no L2 installer and no L2 test beyond the IR-7 detection, lists the exact missing launcher or harness integration copied from the verdict, and gives the follow-up scope as design sections 19.2 to 19.5 (one owned shared hooks/pre-push, no config change, no forwarding, refuse field-3 updates to refs/heads/main and refs/heads/master for a positively selected governed process, human pushes in the same worktree unrestricted, tests on a temporary bare remote) with the open items U28 and OB-H3 L2 observation. If the verdict is L2: GO, the file states that a follow-up plan for sections 19.2 to 19.5 is still required because the install place (U28) and the OB-H3 L2 observation are unverified, and this plan builds no L2 code either way.

Acceptance criteria:
- ./artifacts/l2-disposition.md exists and quotes the L2 line of ./artifacts/b-ctx-verdict.md.
- The file states that no pre-push or installer code was written by this plan, and a search of the diff for a file named pre-push finds none.
- The follow-up scope paragraph names design sections 19.2, 19.3, 19.4 and 19.5.

AC ids (source order):
T21.AC1: ./artifacts/l2-disposition.md exists and quotes the L2 line of ./artifacts/b-ctx-verdict.md.
T21.AC2: The file states that no pre-push or installer code was written by this plan, and a search of the diff for a file named pre-push finds none.
T21.AC3: The follow-up scope paragraph names design sections 19.2, 19.3, 19.4 and 19.5.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: 3a39908e75dd9490d059f2ecb764d9d64d90b478
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/l2-disposition.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/l2-disposition.md
new file mode 100644
index 00000000..4ea49c7f
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/l2-disposition.md
@@ -0,0 +1,61 @@
+# L2 pre-push disposition (issue #394, Task 21)
+
+## The verdict this follows
+
+`./artifacts/b-ctx-verdict.md`, section "L2 verdict", says:
+
+> L2: BLOCKED
+
+and names the missing launcher or harness integration exactly:
+
+> Missing launcher or harness integration, named exactly: (1) a live observation of subagent, nested-subagent, background-Bash-to-Git and Monitor-to-Git process trees with the same-worktree human terminal at the same time; (2) a live observation of resume in a new Claude process, `/clear`, fork and auto mode (E:19); (3) the claim launcher provisioning the governed level record for the actual logical session and checking the adapter runtime before it advertises protection (E:19, D:565); (4) a verified install place for the shared `hooks/pre-push` file (U28, D:377,457). Until these exist, L2 cannot be built or claimed.
+
+## What this plan builds, and what it does not
+
+This plan wrote no pre-push file, no L2 installer and no L2 test. The only L2
+code is the detection in the claim script (IR-7): `l2_status()` reports
+`absent` when the worktree has no executable file at git's `hooks/pre-push`
+path, and the claim then adds the warning `W-L2-ABSENT` and lets the launch
+continue (see `./artifacts/ir7-consequence.md`). It reads the file's presence
+and mode only. It never creates, edits or adopts a hook, and it never claims
+that an existing hook is the owned one. A search of this plan's changed files
+for a file named `pre-push` finds none.
+
+Of the four missing items, this plan closed part of item (3): the claim now
+checks the adapter runtime and the guard's registrations before it launches
+(IR-4), but it does not provision the level record for the actual logical
+session (the guard binds it on the session's first prompt) and it does not
+check the L2 layer beyond presence.
+
+## Follow-up scope
+
+A separate plan is required. It covers design sections 19.2, 19.3, 19.4 and
+19.5:
+
+- 19.2 (placement and coexistence): one owned, shared `hooks/pre-push` file,
+  installed only when no foreign pre-push exists and the default hooks lookup
+  is in effect; no change to the user's git configuration (no `core.hooksPath`
+  migration) and no forwarding of other hooks; ownership is the exact owned
+  version and content, never a header alone.
+- 19.3 (update stream and limits): for a positively selected governed process,
+  refuse the entire push when field 3 of any record is exactly
+  `refs/heads/main` or `refs/heads/master`; the known bypasses stay with the
+  L1 text layer.
+- 19.4 (release and removal): human pushes in the same worktree stay
+  unrestricted, and a retained worktree marker must not restrict them after
+  release; the shared hook may stay installed and inert.
+- 19.5 (tests): real git on a temporary bare remote, a clone and linked
+  worktrees, asserting the remote refs before and after, not only the exit
+  status.
+
+Open items for that plan: U28 (the verified install place for the shared
+`hooks/pre-push` file) and the OB-H3 L2 observation (real governed process
+trees and a same-worktree human terminal at the same time). The design files
+that 19.2 to 19.4 cite as evidence are absent from this tree (listed in
+`./artifacts/b-ctx-verdict.md`, section F7), so the decisions in those sections
+are unverified until that plan re-derives them.
+
+## When the L2 plan ships
+
+Turn the `W-L2-ABSENT` warning into a refusal in `cmd_launch`; the one-line
+change is in `./artifacts/ir7-consequence.md`.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
