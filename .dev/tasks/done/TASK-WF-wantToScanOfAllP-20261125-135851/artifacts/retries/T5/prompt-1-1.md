140027902029382256a70866314b63a2d10cd54a
Review one task for spec compliance.

Task brief: ## Task 5: Re-run render.py and check that only the intended lines changed

Depends on: Task 1, Task 2, Task 3, Task 4

Run `uv run python agent1/tools/render.py` from the planning folder. It overwrites only `agent1/issue-drafts/` (89 files). Expected change: the "Before step 1" paragraph in 73 story drafts, the `- Owner goal:` bullet in `EPIC-12-STORY-01-coordinator-needs-as-decisions.md`, the `Related: #726` bullet in 9 drafts, the EPIC-01-STORY-03 done item, and the added done item in `EPIC-12-STORY-05-you-are-needed-notice.md`. If `git diff` shows any other hunk, a draft was edited by hand after the last render: stop, report the file and hunk, and restore it with `git checkout -- <file>` only after the owner decides.

Acceptance criteria:
- `ls agent1/issue-drafts | wc -l` prints 89 and no draft file was added or removed (`git status --short -- agent1/issue-drafts` shows only `M` lines).
- `grep -rlE "not meant to replace|does not replace|NOT meant to replace" agent1/issue-drafts` prints nothing.
- `grep -rl "open decision is whether the read-only rule may be relaxed" agent1/issue-drafts` prints nothing.
- Every changed hunk is one of the five kinds above (check with `git diff -U0 -- agent1/issue-drafts | grep '^[-+][^-+]'` and read each distinct line pair).
- The 15 epic drafts and `agent1/issue-drafts/README.md` are unchanged: `git diff --stat -- agent1/issue-drafts/README.md agent1/issue-drafts/EPIC-0[1-9]-release*.md agent1/issue-drafts/EPIC-1[0-5]-release*.md` prints nothing.

AC ids:
T5.AC1: `ls agent1/issue-drafts | wc -l` prints 89 and no draft file was added or removed (`git status --short -- agent1/issue-drafts` shows only `M` lines).
T5.AC2: `grep -rlE "not meant to replace|does not replace|NOT meant to replace" agent1/issue-drafts` prints nothing.
T5.AC3: `grep -rl "open decision is whether the read-only rule may be relaxed" agent1/issue-drafts` prints nothing.
T5.AC4: Every changed hunk is one of the five kinds above (check with `git diff -U0 -- agent1/issue-drafts | grep '^[-+][^-+]'` and read each distinct line pair).
T5.AC5: The 15 epic drafts and `agent1/issue-drafts/README.md` are unchanged: `git diff --stat -- agent1/issue-drafts/README.md agent1/issue-drafts/EPIC-0[1-9]-release*.md agent1/issue-drafts/EPIC-1[0-5]-release*.md` prints nothing.
Global constraints: ## Constraints

- Scan result and blast-radius reasoning for this plan: ./artifacts/scan-and-blast-radius.md (every place, its count, why the rest were left alone). Grounding note: ./artifacts/codegraph-grounding.md.
- Every path below is relative to `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` (the planning folder), which is tracked on branch `ironbelly/orch-ledger-20261122` of the main checkout and is absent from master and from the Coordinator branch. Run `/sc:implement` from the checkout that has that branch checked out.
- Corrected wording of the sentence (same meaning as the corrected issue 727): the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
- Corrected wording of the 726 text: the owner answered in chat on 2026-11-22, recorded as a comment on issue 726, that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote still waits for the architecture and storage evaluation in issue 727.
- Do not edit the 89 files under `agent1/issue-drafts/` by hand; they are output of `agent1/tools/render.py`. Do not edit the owner's verbatim text (`OWNER-INSTRUCTIONS.md`, the quote in issue 727 and in `.dev/issues/727/issue-body.md`). Do not file, edit or close any GitHub issue. Commit and push nothing.
- `PIPELINE-RECORD.md` is append-only and has an uncommitted change in that checkout: add one row at the end and keep every existing line and the uncommitted change.
Start sha: 140027902029382256a70866314b63a2d10cd54a
Diff against the start snapshot: Compact diff of Task 5 (render.py output). The full diff is: git -C /home/coder/workspaces/IronClaude diff 140027902029382256a70866314b63a2d10cd54a -- .dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/issue-drafts   (run it yourself if you want every hunk; paths below are relative to .dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/)

git diff --stat summary line:
 76 files changed, 85 insertions(+), 84 deletions(-)

Task 5 acceptance commands as run, with output:
$ ls agent1/issue-drafts | wc -l
89
$ git status --short -- agent1/issue-drafts | cut -c1-2 | sort | uniq -c
     76  M
$ grep -rlE "not meant to replace|does not replace|NOT meant to replace" agent1/issue-drafts
(no output above = none)
$ grep -rl "open decision is whether the read-only rule may be relaxed" agent1/issue-drafts
(no output above = none)
$ git diff --stat -- agent1/issue-drafts/README.md agent1/issue-drafts/EPIC-0[1-9]-release*.md agent1/issue-drafts/EPIC-1[0-5]-release*.md
 .../agent1/issue-drafts/EPIC-01-release-2-prep.md                       | 2 +-
 .../agent1/issue-drafts/EPIC-12-release-1-8-first-write-and-respond.md  | 2 +-
 .../issue-drafts/EPIC-15-release-2-0-feedback-and-more-write-respond.md | 2 +-
 3 files changed, 3 insertions(+), 3 deletions(-)

Modified draft files that are epics (not stories):
 M agent1/issue-drafts/EPIC-01-release-2-prep.md
 M agent1/issue-drafts/EPIC-12-release-1-8-first-write-and-respond.md
 M agent1/issue-drafts/EPIC-15-release-2-0-feedback-and-more-write-respond.md

Changed-line kinds (count of files; one example before/after each):
KIND A: 'Before step 1' paragraph: removed in 73 files, added in 73 files. Example:
-Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
+Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

KIND B: 'Related: #726' bullet, 9 files; example:
-- Related: #726 (a vote on each question, kept as a local record; its open decision is whether the read-only rule may be relaxed)
+- Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)
files:

KIND C: Owner goal bullet in EPIC-12-STORY-01:
-- Owner goal: owner goal: the dashboard does not replace talking to the coordinator sessions; it is where decisions are made, with coordinator questions reduced to binary or multiple choice where possible
+- Owner goal: owner goal: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail)

KIND D: EPIC-01-STORY-03 done item:
-- The decision to relax the read-only rule is recorded by the owner in a dated record (house pattern: `.dev/issues/409/owner-decisions-<date>.md`); issue #726 is told.
+- The owner's 2026-11-22 decision (read-only rule relaxed, dashboard two-way) is copied into the owner-decisions record in the house pattern `.dev/issues/409/owner-decisions-<date>.md`, with the exact write paths this PRD allows still to be decided by the owner.

KIND E: EPIC-12-STORY-05 added done item:
+- The owner's open question from issue #727 (2026-11-25) is answered or deferred in the record: should longer conversations with a coordinator move into the dashboard too, and in which release.

Hunk headers per file are all single-line hunks; any hunk of a kind not listed above:
(no output above = none)

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
