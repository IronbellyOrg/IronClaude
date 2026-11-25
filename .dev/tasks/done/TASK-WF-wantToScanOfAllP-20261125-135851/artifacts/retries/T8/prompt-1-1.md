63715d250a1f5e520be3ffec6c8630e6235c0666
Review one task for spec compliance.

Task brief: ## Task 8: Append the correction row to PIPELINE-RECORD.md

Depends on: Task 5, Task 6, Task 7

Append one row at the end of the table in `PIPELINE-RECORD.md` (after row 24), numbered 25: date 2026-11-25; phase Correction; entry: the owner corrected the goal sentence of issue 727 (the dashboard replaces direct communication with the coordinators; the 1.8 release is where responses and answers start going through it), naming the old rows it changes (row 1, the roadmap input, and row 4, the 88 drafts written with the wrong sentence) and listing what was fixed (render.py, plan_common.py, plan_e01.py, plan_unique.py, RELEASE-PLAN.md, `.dev/issues/727/issue-body.md`, 89 drafts regenerated, nothing filed) and the open owner question about longer conversations; decided by: owner in chat; evidence: issue 727 body, `agent1/RELEASE-PLAN.md`; status: changed. Use the table's existing column order and `|` format.

Acceptance criteria:
- `git diff -U0 PIPELINE-RECORD.md` shows the added row 25 and no removed line of the existing rows; the uncommitted change that was already in the file is still there.
- The row has the same number of `|` separators as row 24.
- Rows 1 and 4 are not edited (append-only rule).

AC ids:
T8.AC1: `git diff -U0 PIPELINE-RECORD.md` shows the added row 25 and no removed line of the existing rows; the uncommitted change that was already in the file is still there.
T8.AC2: The row has the same number of `|` separators as row 24.
T8.AC3: Rows 1 and 4 are not edited (append-only rule).
Global constraints: ## Constraints

- Scan result and blast-radius reasoning for this plan: ./artifacts/scan-and-blast-radius.md (every place, its count, why the rest were left alone). Grounding note: ./artifacts/codegraph-grounding.md.
- Every path below is relative to `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` (the planning folder), which is tracked on branch `ironbelly/orch-ledger-20261122` of the main checkout and is absent from master and from the Coordinator branch. Run `/sc:implement` from the checkout that has that branch checked out.
- Corrected wording of the sentence (same meaning as the corrected issue 727): the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
- Corrected wording of the 726 text: the owner answered in chat on 2026-11-22, recorded as a comment on issue 726, that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote still waits for the architecture and storage evaluation in issue 727.
- Do not edit the 89 files under `agent1/issue-drafts/` by hand; they are output of `agent1/tools/render.py`. Do not edit the owner's verbatim text (`OWNER-INSTRUCTIONS.md`, the quote in issue 727 and in `.dev/issues/727/issue-body.md`). Do not file, edit or close any GitHub issue. Commit and push nothing.
- `PIPELINE-RECORD.md` is append-only and has an uncommitted change in that checkout: add one row at the end and keep every existing line and the uncommitted change.
Start sha: 63715d250a1f5e520be3ffec6c8630e6235c0666
Diff against the start snapshot: diff --git a/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/PIPELINE-RECORD.md b/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/PIPELINE-RECORD.md
index 1db80c614..cb716e3a8 100644
--- a/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/PIPELINE-RECORD.md
+++ b/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/PIPELINE-RECORD.md
@@ -28,3 +28,4 @@ Purpose (owner, 2026-11-23): keep a record of old decisions and completed phases
 | 22 | 2026-11-23 | Owner decisions | Branching decisions 4, 5, 7, 8 answered. 4: merge commit (--no-ff) for story into line. 5: integration branch is not currently in use (sync PR and early-warning checks against integration come out of the text). 7: a test-only multi-story release uses a release line. 8: precedent verified (PR 658 squash, single parent, reverted by 662, redone as 664 with a merge commit); proceed with sentence plus two-parent closeout check. 6: owner asked a clarifying question (planning files or implementation?); answered, decision pending. | owner in chat | UNIFIED-BRANCHING-PROPOSAL.md section 10; gh pr view 658 662 664 | approved (4, 5, 7, 8) |
 | 23 | 2026-11-23 | Owner decision | Branching decision 6 answered: (a) yes, manual CI (dispatch) runs on the pushed release line; (b) "Review all pull requests", read by the coordinator as: every story gets a review-only story pull request (bots review it, never merged by the PR button, the coordinator merges the story locally with a merge commit); the proposal's size threshold (15 files or 1,000 added lines) is dropped and the optional layer is on for all stories; trial T6 must pass before the first one is relied on; reading to be confirmed by the owner; (c) no: no test.yml change for release 1. | owner in chat | UNIFIED-BRANCHING-PROPOSAL.md section 10, Q2 | approved, reading of (b) to confirm |
 | 24 | 2026-11-23 | Owner decision | Decision 6(b) reading confirmed ("yes that is the correct reading"): every story gets a review-only story pull request (bots, never the merge button), default on, size threshold dropped; trial T6 before first reliance. All eight branching decisions are now answered. | owner in chat | UNIFIED-BRANCHING-PROPOSAL.md | approved |
+| 25 | 2026-11-25 | Correction | Owner corrected the goal sentence of issue 727: the dashboard replaces direct communication with the coordinators, and release 1.8 is where responses and answers start going through it. This corrects row 1 (the roadmap input carried the sentence "not to replace interacting with the coordinator sessions") and row 4 (the 88 drafts were written with that sentence). Fixed: agent1/tools/render.py, plan_common.py, plan_e01.py and plan_unique.py; agent1/RELEASE-PLAN.md; .dev/issues/727/issue-body.md (refreshed from the live issue); the 89 drafts regenerated, 76 changed (73 stories carried the sentence; 3 epic drafts changed only by the corrected 726 bullet); nothing filed. Also stale and fixed: the text calling issue 726's read-only question open (the owner ruled yes on 2026-11-22). Open owner question: should longer conversations with a coordinator move into the dashboard too, and in which release. | owner in chat | issue 727 body; agent1/RELEASE-PLAN.md | changed |

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
