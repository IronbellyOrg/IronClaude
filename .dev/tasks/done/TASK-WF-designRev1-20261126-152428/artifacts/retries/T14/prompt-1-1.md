876adbab68139695fa6f9a7843d7aa391691ecd8
Review one task for spec compliance.

Task brief: ## Task 14: Draft the pull request body .dev/issues/837/pr-body.md

Depends on: Task 4, Task 11, Task 12, Task 13

Write `.dev/issues/837/pr-body.md` from the template of section 3.7 of `./source.md`. Sections: Summary; "Decided for this work (iteration 3)", copied word for word from the matching block at the end of `.dev/issues/837/issue-summary.md` including the line that records Clay's answer (copy the block with a command, never retype it); What this change adds (the files of Tasks 1 to 4); Audit and gate results (one row per repository, summarising its ledger rows from `.dev/issues/837/gates.md`: applied, skipped with the first failing gate, or handed to Ryan, and that nothing is applied yet); The restated done condition per repo (read locally from the section "Done condition for this pull request" of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md`: the issue's literal condition is met by none of the six repos under this design, and issue 837 stays open until Ryan reports); What is left (the three Ryan repos, and the clearances that unlock the apply); Tests run (paste the real output summary lines of `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `uv run ruff check tests/docs/test_branch_protection_rulesets.py` and `make lint`); and as its last line `Refs #837`. The body carries no private detail (see the constraints) and says where the handoff comment on issue 837 is.

Acceptance criteria:
- `.dev/issues/837/pr-body.md` contains the "Decided for this work (iteration 3)" block and a diff of that block against the one in `.dev/issues/837/issue-summary.md` shows no difference.
- The file ends with the line `Refs #837` and contains neither `Fixes #837` nor `Closes #837`.
- The per-repo table has one row for each of the six repos and matches the decisions in `.dev/issues/837/gates.md`.
- The Tests run section shows output copied from commands run in this task, including `make lint`, not typed from memory; a `make lint` failure on files this change does not touch is named as pre-existing.
- `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/pr-body.md` prints 0.
Global constraints: ## Constraints

- This plan only writes files in this worktree and runs read-only `gh api` GET calls. No task may send POST, PUT or DELETE to any GitHub ruleset, create a branch or ruleset in another repository, comment on an issue or edit a pull request. Applying rulesets is "Phase 3" of `./source.md` section 4 and is carried out from the runbook that Task 13 produces, after the pull request monitor has settled, never by `/sc:implement`.
- Never write to IronHands-CLI, irondots, ironops-marketplace, the archived IronHands repo, or any repository outside IronbellyOrg. Every `gh` call names its repository in full (`repos/IronbellyOrg/<repo>/...`, or `--repo IronbellyOrg/IronClaude`) except `gh api user`; never rely on the fork-parent default and never touch `SuperClaude-Org/SuperClaude_Framework`.
- Where `./source.md` section 2 names the four state files, this plan writes them there and nowhere else: `.dev/issues/837/audit/<repo>.md`, `.dev/issues/837/gates.md`, `.dev/issues/837/handoff-ryan.md` and `.dev/issues/837/apply-runbook.md`. They are never staged. The drafted pull request body goes to `.dev/issues/837/pr-body.md`. The package `./artifacts/` folder holds only the codegraph grounding note. The results of the later apply are recorded in the audit file and the ledger, as section 3.6 of `./source.md` says; there is no separate apply-results file.
- IronClaude is public and `IronbellyOrg/Coder` is private (Revision 1 of `./source.md`). Nothing that describes the internals of the private repository's release tooling (its file name, folder, function names, lines or line numbers) may be written to any file under `.dev/tasks/`, to any log or QA output captured there, to the pull request body or to an issue comment. The only neutral sentence allowed in such places is: "release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca". Task 5 reads the tooling without printing or saving its lines and keeps the evidence only in `.dev/issues/837/private/`, which is never staged. Those names are not written in this plan: E-2 of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md` lists them.
- Do not create `.github/rulesets/other-repos/protect-aidev02.json`: it needs Clay's written yes for `aidev02`, which is not recorded in `.dev/issues/837/issue-summary.md`.
- IronClaude's three existing files `.github/rulesets/protect-master.json`, `protect-integration.json` and `protect-release-tags.json` and the live IronClaude rulesets stay unchanged. Every existing assertion in `tests/docs/test_branch_protection_rulesets.py` stays.
- Facts that nobody verified stay labelled UNVERIFIED in every file this plan writes: whether the Sync fork button is refused under a `pull_request` rule, whether `clayphi`'s token can create rulesets, whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, and whether `time_period=quarter` is 90 days (it is not used).
- A check that cannot run (for example `gh api --paginate orgs/IronbellyOrg/installations`, which needs the `admin:org` scope) is written down as "could not run" with the real error text and blocks the repo it covers; it is never recorded as clean.
- Clay's recorded answer is in `.dev/issues/837/issue-summary.md` under "Decided for this work (iteration 3)". It is quoted word for word wherever a task says to quote it, never paraphrased. The lead's note in it, that the release-tag ruleset has its `update` rule on integration (pull request 844 merged), was verified before this plan: `.dev/issues/837/accuracy-check.md` line 13 records commit 206abea1c and the live ruleset 28081842 with `update`.
- This plan does not commit or push. Those are later story steps.
Start sha: 876adbab68139695fa6f9a7843d7aa391691ecd8
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/pr-body.md


diff --git a/.dev/issues/837/pr-body.md b/.dev/issues/837/pr-body.md
new file mode 100644
index 000000000..45a195f6d
--- /dev/null
+++ b/.dev/issues/837/pr-body.md
@@ -0,0 +1,83 @@
+## Summary
+
+Issue 837 asks for the branch protection rulesets of issue 702 on the other public IronbellyOrg repos. All six default to `main`, so IronClaude's `master` and `integration` files would protect nothing there. This change adds rulesets by branch role (a full role and a mirror role for forks), the guide section, the pinning test, and the local audit, gate and handoff records. It applies nothing: every repo gets its rulesets only after its own 90-day check of direct pushes, and the gates below keep all three Clay repos skipped for now. Nothing is written to any repo other than IronClaude.
+
+## Decided for this work (iteration 3)
+
+- **Question:** Which repos get the rulesets? **Decided:** The six repos listed in the issue are the candidates; each one gets the rulesets only after the issue owner's go for that repo and its own 90-day check of direct pushes; Ryan applies the three only his login can change. This part needs Clay's answer at the start of the story: ask, then record the answer here and in the pull request.
+- **Scope:** first step: the issue owner (Clay) gives the go per repo, as its pick-up note asks; needs admin on each repo: Clay has it on three, Ryan applies the three only his login can change (IronHands-CLI, ironops-marketplace, irondots); run the 90-day check of direct pushes per repo first.
+- **Between people:** #837 (Clay) needs Ryan for the three repos only his login can change: IronHands-CLI, ironops-marketplace, irondots.
+- **Between people:** #702 (Leandro) still has an update rule for the release-tag ruleset open, and #837 and #838 (Clay) copy the rulesets in `.github/rulesets/` to other repos: settle the release-tag rule in #702 first, or copy only the branch rulesets until it is settled.
+- **Answer (Clay's answer for this story, typed in by the lead on 26 Nov 2026):** go on the three public IronbellyOrg repos Clay has admin on: CPA-Manager-Plus, IronOrca, coder_orca. IronHands-CLI, irondots and ironops-marketplace need Ryan (Clay's login has only read there): do not write to them; prepare what Ryan must apply and ask the lead to hand it to Ryan. Each repo still gets the rulesets only after its own 90-day check of direct pushes. The lead's note: the release-tag ruleset now has its update rule on integration (pull request 844 merged), so verify that and copy the release-tag ruleset too; if you find it is not settled, copy only the branch rulesets.
+
+## What this change adds
+
+- `.github/rulesets/other-repos/protect-main.json`: the full role (`deletion`, `non_fast_forward`, `pull_request` with 0 approvals) on `refs/heads/main`, derived from `protect-master.json` by changing only `name` and the branch.
+- `.github/rulesets/other-repos/protect-main-mirror.json`: the mirror role (`deletion`, `non_fast_forward`; no `pull_request` rule) for a fork's `main`, which receives fast-forwards from its parent.
+- `docs/developer-guide/branch-protection.md`: a new section "Other IronbellyOrg repos" (targets, variables, the role of a fork's `main`, before applying, apply, check, self-test, roll back and break glass) and one edited sentence in "Tests".
+- `tests/docs/test_branch_protection_rulesets.py`: four new tests (full role derived, mirror derived, files match the target table, guide section), a target table for the six repos, and the "no `~DEFAULT_BRANCH`" scan made recursive.
+- `protect-aidev02.json` is not created: it needs Clay's written yes for `aidev02`, which is not recorded.
+- The release-tag ruleset is copied as it is (`.github/rulesets/protect-release-tags.json`); its `update` rule on integration was verified (commit 206abea1c, pull request 844 merged; live ruleset 28081842 returns `deletion`, `non_fast_forward`, `update`).
+
+## Audit and gate results
+
+Six read-only audit records were written locally (not part of this change). Nothing is applied yet. The decision of each ruleset is the first gate that fails (G3 is the organisation installations read, which `clayphi`'s token cannot run because it lacks the `admin:org` scope; no written acceptance of that gap is recorded).
+
+| Repo | Role and audit finding | Ruleset decisions |
+|---|---|---|
+| CPA-Manager-Plus | fork of seakee/CPA-Manager-Plus, `ahead_by` 0 (mirror candidate); 0 direct pushes in 90 days; 72 `v*` tags equal the parent's; tag producer search clear | branch ruleset skipped (G3); tag ruleset skipped (G3) |
+| IronOrca | fork of stablyai/orca, `ahead_by` 0 (mirror candidate); 3 parent syncs on `main`, no direct push; tag producer search clear | branch ruleset skipped (G3); tag ruleset skipped (G3); `aidev02` skipped (G5: no written yes, file not created) |
+| coder_orca | not a fork, full role; 1 branch creation, no direct push; 16 `v*` tags | `protect-main` skipped (G3); tag ruleset skipped (G6): release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca |
+| IronHands-CLI | fork of OpenHands/OpenHands-CLI, `ahead_by` 13 (full role); 0 events in 90 days; no `v*` tag | handed to Ryan |
+| irondots | not a fork; 3 events by a person (1 branch creation, 2 pull request merges); no tag; its gated-release workflow only creates tags | handed to Ryan |
+| ironops-marketplace | not a fork; no event in 90 days, no tag, no workflow | handed to Ryan |
+
+The handoff text for Ryan (commands, audit results and what to report back) and the draft ledger are posted as a comment on issue 837 right after the push and before this pull request is opened; its links are pinned to the pushed commit.
+
+## The restated done condition per repo
+
+The issue's literal condition (three rulesets per repo, with check commands printing three rule types) is met by none of the six repos under this design: no target repo has an `integration` branch, the forks get a mirror whose branch check prints two rule types, coder_orca gets one ruleset, and the three Ryan repos get nothing applied by this change. So it is restated per repo:
+
+| Repo | End state this change delivers | Rulesets this change can leave active |
+|---|---|---|
+| CPA-Manager-Plus | `main` mirror once the gates pass; tag ruleset only if its producer search clears it; otherwise skipped with the reason | at most 2 |
+| IronOrca | `main` mirror once the gates pass; tag ruleset only if its producer search clears it; `aidev02` only on Clay's written yes | at most 3 |
+| coder_orca | `main` full role once the gates pass; tag ruleset skipped | 1 |
+| IronHands-CLI, irondots, ironops-marketplace | handed to Ryan: `main` full role, plus the tag ruleset if the read-only workflow search clears it; nothing is written to these repos by this change | 0 |
+
+Clay's written acceptance of this restated condition is not recorded yet. Issue 837 stays open: this pull request says `Refs #837` and does not close it.
+
+## What is left
+
+- Ryan applies the three repos only his login can change (IronHands-CLI, irondots, ironops-marketplace), from the handoff comment, and reports the ids and read-back output on issue 837.
+- Clearances that unlock the apply on the three Clay repos, each a written statement quoted in the issue summary: Clay accepts the installations check as not runnable with his token (or an organisation owner posts its output); Clay accepts the mirror rule set on the two forks; Clay says yes or no to protecting `aidev02`; `ironbelly` confirms admin on the three Clay repos; Clay accepts the restated done condition.
+- The apply for the Clay repos follows the runbook after this pull request's monitor has settled, only for rulesets whose gates all pass.
+- Unverified and unanswerable by design: whether the Sync fork button is refused under a `pull_request` rule, whether `clayphi`'s token can create rulesets, whether a duplicate ruleset name is accepted, and whether the mirror's bypass actor is accepted without a `pull_request` rule (the scratch self-test answers the last one before any real create).
+
+## Tests run
+
+Output copied from the commands run for this change:
+
+```text
+tests/docs/test_branch_protection_rulesets.py::test_branch_rulesets[protect-master-refs/heads/master] PASSED [ 11%]
+tests/docs/test_branch_protection_rulesets.py::test_branch_rulesets[protect-integration-refs/heads/integration] PASSED [ 22%]
+tests/docs/test_branch_protection_rulesets.py::test_tag_ruleset PASSED   [ 33%]
+tests/docs/test_branch_protection_rulesets.py::test_no_default_branch_token_anywhere PASSED [ 44%]
+tests/docs/test_branch_protection_rulesets.py::test_guide_has_apply_and_check_commands PASSED [ 55%]
+tests/docs/test_branch_protection_rulesets.py::test_other_repos_full_role_derived PASSED [ 66%]
+tests/docs/test_branch_protection_rulesets.py::test_other_repos_mirror_derived PASSED [ 77%]
+tests/docs/test_branch_protection_rulesets.py::test_other_repos_files_match_targets PASSED [ 88%]
+tests/docs/test_branch_protection_rulesets.py::test_guide_has_other_repos_section PASSED [100%]
+============================== 9 passed in 0.12s ===============================
+============================== 57 passed in 0.65s ==============================
+All checks passed!
+make lint exit code 0
+  Errors:   0
+  Warnings: 4
+  ✅ PASS — architecture policy compliant (4 warning(s))
+All checks passed!
+```
+
+Commands: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `uv run ruff check tests/docs/test_branch_protection_rulesets.py` and `make lint`. No `make lint` failure occurred.
+
+Refs #837


Codegraph context: index_state: fresh; checked_at: 2026-11-26T15:31:43Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files of this task are JSON and Markdown (not indexed) unless a Python file is named; dependents were checked with Grep.
Note on files the diff cannot show: paths under `.dev/issues/837/private/` are git-ignored, so they are absent from the diff; read them directly with Read when a task names them. Never print private content in your answer.
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
