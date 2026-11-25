196fe544da9d6953b1dbf1f3dbafe7f07d0b90c0
Review one task for spec compliance.

Task brief: ## Task 6: Correct the goal paragraph in RELEASE-PLAN.md

Edit `agent1/RELEASE-PLAN.md` line 69, the paragraph "Goal text that every epic must keep (owner, issue 727): the dashboard is NOT meant to replace talking to the coordinator sessions; ...". Replace the wrong sentence with the corrected wording of the Constraints, and replace the tail "issue 726 (vote on each question) is the first small step and its open decision is whether the read-only rule may be relaxed" with the corrected 726 text. Keep the other facts of that paragraph (observer read-only today, no database, questions in process memory, export record and snapshot).

Acceptance criteria:
- `grep -n "NOT meant to replace\|open decision is whether" agent1/RELEASE-PLAN.md` prints nothing.
- `git diff -U0 agent1/RELEASE-PLAN.md` shows one changed line (69).
- The paragraph still says the observer is read-only by design today.

AC ids:
T6.AC1: `grep -n "NOT meant to replace\|open decision is whether" agent1/RELEASE-PLAN.md` prints nothing.
T6.AC2: `git diff -U0 agent1/RELEASE-PLAN.md` shows one changed line (69).
T6.AC3: The paragraph still says the observer is read-only by design today.
Global constraints: ## Constraints

- Scan result and blast-radius reasoning for this plan: ./artifacts/scan-and-blast-radius.md (every place, its count, why the rest were left alone). Grounding note: ./artifacts/codegraph-grounding.md.
- Every path below is relative to `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` (the planning folder), which is tracked on branch `ironbelly/orch-ledger-20261122` of the main checkout and is absent from master and from the Coordinator branch. Run `/sc:implement` from the checkout that has that branch checked out.
- Corrected wording of the sentence (same meaning as the corrected issue 727): the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
- Corrected wording of the 726 text: the owner answered in chat on 2026-11-22, recorded as a comment on issue 726, that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote still waits for the architecture and storage evaluation in issue 727.
- Do not edit the 89 files under `agent1/issue-drafts/` by hand; they are output of `agent1/tools/render.py`. Do not edit the owner's verbatim text (`OWNER-INSTRUCTIONS.md`, the quote in issue 727 and in `.dev/issues/727/issue-body.md`). Do not file, edit or close any GitHub issue. Commit and push nothing.
- `PIPELINE-RECORD.md` is append-only and has an uncommitted change in that checkout: add one row at the end and keep every existing line and the uncommitted change.
Start sha: 196fe544da9d6953b1dbf1f3dbafe7f07d0b90c0
Diff against the start snapshot: diff --git a/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md b/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md
index 680dae9a7..46eb79e63 100644
--- a/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md
+++ b/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md
@@ -66,7 +66,7 @@ Order rule from the owner: the architecture and preliminary evaluation (Release
 
 Not planned here (owner: "Release 2 and beyond"): user feedback systems that gather data to tune when and how the person is prompted. It is recorded as a closing note in EPIC-15, not as an epic.
 
-Goal text that every epic must keep (owner, issue 727): the dashboard is NOT meant to replace talking to the coordinator sessions; it becomes where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail). Dashboard, watcher and coordinator work are developed together as needed. Facts read in issue 727 for the starting point: the observer (`superclaude observe`) is read-only by design, keeps no database, questions live in process memory, stored files are an export record and a snapshot under the observer state folder; issue 726 (vote on each question) is the first small step and its open decision is whether the read-only rule may be relaxed.
+Goal text that every epic must keep (owner, issue 727): the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail). Dashboard, watcher and coordinator work are developed together as needed. Facts read in issue 727 for the starting point: the observer (`superclaude observe`) is read-only by design, keeps no database, questions live in process memory, stored files are an export record and a snapshot under the observer state folder; issue 726 (vote on each question) is the first small step; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way, and the vote waits for the architecture and storage evaluation in issue 727.
 ## S3. How epics, features and stories map (agent 1 position, to be debated)
 
 ### S3.1 Three layers, three owners

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
