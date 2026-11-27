71634ad3a5afaadb3ff865d69c51db7ee3df2eb6
Review one task for spec compliance.

Task brief: ## Task 11: Write the gate ledger .dev/issues/837/gates.md

Depends on: Task 5, Task 6, Task 7, Task 8, Task 9, Task 10

Write `.dev/issues/837/gates.md` as defined in section 3.5 of `./source.md`. Start with a header that names the gates G1 to G9 in one line each and quotes where Clay's recorded answer is (`.dev/issues/837/issue-summary.md`, "Decided for this work (iteration 3)"), cites `.dev/issues/837/accuracy-check.md` line 13 as the verification of the release-tag ruleset's `update` rule that the lead asked for and states the rule that follows (if that rule is not settled, every tag row is `SKIP(not settled)` and only the branch rulesets are copied), and records the two statements that are not gates (Clay's written acceptance of the restated done condition, and `ironbelly`'s written confirmation of admin on each Clay repo) as "not recorded". Then one row per (repo, ruleset): CPA-Manager-Plus (branch role and tag ruleset), IronOrca (branch role, tag ruleset and `aidev02`), coder_orca (`protect-main`, tag ruleset), and for each Ryan repo (`protect-main`, tag ruleset). Columns: repo, ruleset file, decision, first failing gate, evidence path under `.dev/issues/837/audit/`. The only decisions are `APPLY`, `SKIP(<first failing gate>)` and `HANDOFF`. In this Phase 1 draft: `HANDOFF` for the three Ryan repos; `SKIP(Gn)` where a gate fails now (G3 while the installations read could not run, G4 for a mirror without Clay's quoted acceptance, G5 for `aidev02`, G6 for coder_orca's tag ruleset and for any tag ruleset whose producer search is not `CLEAR`); `SKIP(G8)` for a row whose G1 to G7 pass now, because G8 (pushed SHA) and G9 (scratch self-test) can only be evaluated later. Put no private detail in the file (see the constraints). End with the expected end state of this run from section 8 of `./source.md` and the list of clearances that unlock the apply, each with its "yes means" and "no or silence means".

Acceptance criteria:
- `.dev/issues/837/gates.md` has one row for every (repo, ruleset) named above, each with exactly one decision of `HANDOFF`, `SKIP(Gn)` or `APPLY` and a link to the audit file that supports it.
- No row says `APPLY` and no row says `PENDING`.
- Every `SKIP` row names its first failing gate and the audit block that shows it; the three Ryan repos are all `HANDOFF`.
- The header cites `accuracy-check.md` line 13 and states the "not settled" rule.
- The file lists the five clearances of section 8 with what each unlocks.
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
Start sha: 71634ad3a5afaadb3ff865d69c51db7ee3df2eb6
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/gates.md


diff --git a/.dev/issues/837/gates.md b/.dev/issues/837/gates.md
new file mode 100644
index 000000000..cbc3de758
--- /dev/null
+++ b/.dev/issues/837/gates.md
@@ -0,0 +1,64 @@
+# Gate ledger for issue 837 (draft written in Phase 1, read-only)
+
+One row per (repo, ruleset), one decision per row: `APPLY`, `SKIP(<first failing gate>)` or `HANDOFF`. A ruleset is applied only when every gate G1 to G9 passes for it. The decision names the FIRST gate that fails, counting G1 to G9 in order; gates that also fail are listed in the column "Also fails" and are not part of the decision. This file is local, never staged, and holds no private detail.
+
+## Gates
+
+- G1 Authority: the repo is CPA-Manager-Plus, IronOrca or coder_orca and Clay's recorded answer is present; the three Ryan repos are always `HANDOFF` (no write of any kind).
+- G2 Preflight: login is `clayphi`, `admin` is `true`, default branch is `main`, the repo is not archived and is public.
+- G3 Audit: the audit record's result is `CLEAR` for the target ref (no automation pushes straight to it, every event classified, every check that could not run cleared by an organisation owner's output or by Clay's written acceptance quoted in `issue-summary.md`).
+- G4 Role: a non-fork gets `protect-main`; a fork gets `protect-main-mirror` when `ahead_by` is 0 and Clay's written acceptance of the mirror's direct-push exposure is quoted in `issue-summary.md`, and `protect-main` when `ahead_by` is above 0.
+- G5 `aidev02`: Clay's written yes is quoted in `issue-summary.md` and `protect-aidev02.json` exists.
+- G6 Tag producers: the audit's producer search is `CLEAR` and the repo is not coder_orca.
+- G7 Existing rulesets: the list is empty at the moment of the snapshot.
+- G8 Source: the files to apply are at a commit SHA that is pushed to `origin` and equals the branch head, with no uncommitted change (cannot be evaluated before the push).
+- G9 Self-test: the scratch self-test of the runbook (R1) passed for the role about to be applied (cannot be evaluated before apply day).
+
+Clay's recorded answer is in `.dev/issues/837/issue-summary.md`, section "Decided for this work (iteration 3)", the bullet "Answer (Clay's answer for this story, typed in by the lead on 26 Nov 2026)": a go on CPA-Manager-Plus, IronOrca and coder_orca; IronHands-CLI, irondots and ironops-marketplace need Ryan.
+
+## The release-tag rule (the lead's note)
+
+The lead asked to verify that the release-tag ruleset has its `update` rule on integration (pull request 844 merged). `.dev/issues/837/accuracy-check.md` line 13 records the verification: commit 206abea1c (pull request 844) added `update` to `.github/rulesets/protect-release-tags.json`, and the live IronClaude ruleset 28081842 returns `deletion`, `non_fast_forward` and `update`. The rule is settled, so the release-tag ruleset is copied (the rows below treat it as an ordinary candidate). If it were not settled, every tag row would be skipped and only the branch rulesets copied; that case does not apply.
+
+## Statements that are not gates
+
+- Clay's written acceptance of the restated done condition (section "Done condition for this pull request" of the merged requirements): not recorded.
+- `ironbelly`'s written confirmation of admin on each Clay repo (the revert owner): not recorded; until then Clay is the revert owner.
+
+## Rows
+
+State on 2026-11-26 (audit `END` times are in each audit file). G1 and G2 pass for the three Clay repos (preflight in each audit file). G3 fails for all three Clay repos for the same reason: the organisation installations read could not run (needs the `admin:org` scope, which `clayphi`'s token lacks) and no written acceptance of that gap is recorded.
+
+| Repo | Ruleset file | Decision | First failing gate | Also fails or notes | Evidence |
+|---|---|---|---|---|---|
+| CPA-Manager-Plus | branch role: `protect-main-mirror.json` (fork of seakee/CPA-Manager-Plus, `ahead_by` 0 on 2026-11-26) | `SKIP(G3)` | G3 | G4: no written acceptance of the mirror is recorded | `.dev/issues/837/audit/CPA-Manager-Plus.md` (Blocks, line 100; Result, line 108) |
+| CPA-Manager-Plus | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 passes: producer search `CLEAR` | `.dev/issues/837/audit/CPA-Manager-Plus.md` (Producer search, line 79; Blocks, line 100) |
+| IronOrca | branch role: `protect-main-mirror.json` (fork of stablyai/orca, `ahead_by` 0 on 2026-11-26) | `SKIP(G3)` | G3 | G4: no written acceptance of the mirror is recorded | `.dev/issues/837/audit/IronOrca.md` (Blocks, line 179; Result, line 188) |
+| IronOrca | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 passes: producer search `CLEAR` | `.dev/issues/837/audit/IronOrca.md` (Producer search, line 93; Blocks, line 179) |
+| IronOrca | `protect-aidev02.json` (not created) | `SKIP(G3)` | G3 | G5: no written yes for `aidev02`, so the file does not exist | `.dev/issues/837/audit/IronOrca.md` (Blocks, line 179) |
+| coder_orca | `protect-main.json` (not a fork, full role) | `SKIP(G3)` | G3 | G4 passes | `.dev/issues/837/audit/coder_orca.md` (Blocks, line 77; Result, line 84) |
+| coder_orca | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 also fails: release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca | `.dev/issues/837/audit/coder_orca.md` (Producer search, line 65; Blocks, line 77) |
+| IronHands-CLI | `protect-main.json` (a fork of OpenHands/OpenHands-CLI, `ahead_by` 13, so the full role) | `HANDOFF` | G1 | Ryan applies; Clay writes nothing | `.dev/issues/837/audit/IronHands-CLI.md` (Fork test, line 33; Result, line 106) |
+| IronHands-CLI | `.github/rulesets/protect-release-tags.json` | `HANDOFF` | G1 | no tag exists and no tag-moving workflow found; Ryan decides | `.dev/issues/837/audit/IronHands-CLI.md` (Producer search, line 76; Blocks, line 96) |
+| irondots | `protect-main.json` (not a fork) | `HANDOFF` | G1 | Ryan applies | `.dev/issues/837/audit/irondots.md` (Fork test, line 33; Result, line 122) |
+| irondots | `.github/rulesets/protect-release-tags.json` | `HANDOFF` | G1 | its gated-release workflow only creates tags, which the ruleset allows | `.dev/issues/837/audit/irondots.md` (Producer search, line 92; Blocks, line 112) |
+| ironops-marketplace | `protect-main.json` (not a fork) | `HANDOFF` | G1 | Ryan applies | `.dev/issues/837/audit/ironops-marketplace.md` (Fork test, line 33; Result, line 97) |
+| ironops-marketplace | `.github/rulesets/protect-release-tags.json` | `HANDOFF` | G1 | no tag and no workflow exist | `.dev/issues/837/audit/ironops-marketplace.md` (Producer search, line 75; Blocks, line 86) |
+
+No row says `APPLY`. G8 and G9 cannot be evaluated until the files are pushed and the scratch self-test has run; the runbook (`.dev/issues/837/apply-runbook.md`) re-evaluates G2 to G9 inside the hour before the first write.
+
+## Expected end state of this run
+
+The files, test and guide changed and pushed; six audit records; this ledger; the handoff posted for Ryan; the runbook ready; the pull request open with `Refs #837`; no ruleset applied; `outcome: partial`. Nothing is written to any repository other than IronClaude. This is the safe default, not a failure.
+
+## Clearances that unlock the apply
+
+Each is a written statement quoted in `.dev/issues/837/issue-summary.md`.
+
+| Clearance | Yes means | No or silence means |
+|---|---|---|
+| Clay accepts the installations check as not runnable with his token (or an organisation owner posts the output of `gh api --paginate orgs/IronbellyOrg/installations`) | G3 can pass on the three Clay repos; the rulesets that pass the other gates are applied. | Every ruleset on the three Clay repos stays `SKIP(G3)`. |
+| Clay accepts the mirror rule set (no pull-request rule; direct pushes still allowed) on the fork `main` of IronOrca and CPA-Manager-Plus | G4 passes for the forks and the mirror is applied when `ahead_by` is 0. | The forks' branch rulesets stay skipped and reported; the tag rulesets are decided separately. |
+| Clay says yes to protecting `aidev02` in IronOrca | `protect-aidev02.json` is created and may be applied. | The file does not exist. |
+| `ironbelly` confirms admin on the three Clay repos | `ironbelly` is a named revert owner. | Clay is the only revert owner and must be reachable. |
+| Clay accepts the restated done condition | The issue can be closed by hand once Ryan reports. | The issue stays open with the table as its status. |


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
