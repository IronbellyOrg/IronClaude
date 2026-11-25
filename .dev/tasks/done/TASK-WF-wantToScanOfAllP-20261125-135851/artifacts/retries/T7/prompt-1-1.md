17bc096b9a27294b3d1be06ee3edb2a70501cc7a
Review one task for spec compliance.

Task brief: ## Task 7: Refresh the local copy of the issue 727 body

Unlike Tasks 1 to 6 and 8, this task's path is relative to the repository root of that checkout, not to the planning folder: run its commands from the repository root. Replace the content of `.dev/issues/727/issue-body.md` (tracked) with the live body of issue 727: run `gh issue view 727 --repo IronbellyOrg/IronClaude --json body -q .body` and write its output to that file. `OWNER-INSTRUCTIONS.md` tells planning agents to read this file first, so it must match the corrected issue. The command is read-only on GitHub.

Acceptance criteria:
- `diff <(gh issue view 727 --repo IronbellyOrg/IronClaude --json body -q .body) .dev/issues/727/issue-body.md` prints nothing.
- The file contains "Correction (owner, 2026-11-25)" and still contains the owner's quote "The ultimate goal is NOT to replace interacting with the coordinator sessions" unchanged below that correction.
- `git status --short -- .dev/issues/727/issue-body.md` shows the file as modified and no other `.dev/issues/` path changed.

AC ids:
T7.AC1: `diff <(gh issue view 727 --repo IronbellyOrg/IronClaude --json body -q .body) .dev/issues/727/issue-body.md` prints nothing.
T7.AC2: The file contains "Correction (owner, 2026-11-25)" and still contains the owner's quote "The ultimate goal is NOT to replace interacting with the coordinator sessions" unchanged below that correction.
T7.AC3: `git status --short -- .dev/issues/727/issue-body.md` shows the file as modified and no other `.dev/issues/` path changed.
Global constraints: ## Constraints

- Scan result and blast-radius reasoning for this plan: ./artifacts/scan-and-blast-radius.md (every place, its count, why the rest were left alone). Grounding note: ./artifacts/codegraph-grounding.md.
- Every path below is relative to `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` (the planning folder), which is tracked on branch `ironbelly/orch-ledger-20261122` of the main checkout and is absent from master and from the Coordinator branch. Run `/sc:implement` from the checkout that has that branch checked out.
- Corrected wording of the sentence (same meaning as the corrected issue 727): the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
- Corrected wording of the 726 text: the owner answered in chat on 2026-11-22, recorded as a comment on issue 726, that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote still waits for the architecture and storage evaluation in issue 727.
- Do not edit the 89 files under `agent1/issue-drafts/` by hand; they are output of `agent1/tools/render.py`. Do not edit the owner's verbatim text (`OWNER-INSTRUCTIONS.md`, the quote in issue 727 and in `.dev/issues/727/issue-body.md`). Do not file, edit or close any GitHub issue. Commit and push nothing.
- `PIPELINE-RECORD.md` is append-only and has an uncommitted change in that checkout: add one row at the end and keep every existing line and the uncommitted change.
Start sha: 17bc096b9a27294b3d1be06ee3edb2a70501cc7a
Diff against the start snapshot: diff --git a/.dev/issues/727/issue-body.md b/.dev/issues/727/issue-body.md
index 9b8373533..60dfeafb6 100644
--- a/.dev/issues/727/issue-body.md
+++ b/.dev/issues/727/issue-body.md
@@ -5,11 +5,13 @@ Nothing has been built for this yet. Filed from the owner's note of 2026-11-22.
 State read on 2026-11-22 (so the next person starts from facts):
 - The observer dashboard (`superclaude observe`) is read-only by design. Its user guide (`docs/user-guide/observer.md` on master) says it "never approves, retries, terminates, dispatches, merges or messages". It shows the coordinator's questions (questions screen and Decision Desk) but has no way to answer them; the person answers in the coordinator's own terminal.
 - It keeps no database. Questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder.
-- The first small step toward this roadmap is already filed: issue 726 (a vote on each question, kept as a local record). Its open decision is whether the read-only rule may be relaxed. This note is the owner's direction on that rule: the dashboard is meant to become two-way.
+- The first small step toward this roadmap is already filed: issue 726 (a vote on each question, kept as a local record). Its question of whether the read-only rule may be relaxed was answered by the owner in chat on 2026-11-22 (recorded as a comment on #726): yes, the dashboard is meant to become two-way. The vote itself still waits for the architecture and storage evaluation in this issue.
+
+Update, 2026-11-25 (from the session logs and the planning folder `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/`): no dashboard code has been written. The planning pipeline for this roadmap (issue #731) produced 15 epic drafts and 73 feature drafts, one per release item below, all on disk and none filed as issues; they wait for the owner to schedule each release. The `/sc:brainstorm --depth deep` on dashboard storage and the Postgres database has not been run (the only brainstorm in that folder is about who writes the spec at the hand-off from BMAD, the planning method, to IronClaude, so it does not count).
 
 ## Relevant files and links
 
-- Related issues: #409 (TUI dashboard, open), #706 (observer follow-up, open), #604 (observer remote fleet, open), #606 (visual parity, closed; holds the Zellij go or no-go), #718 (dashboard items from the 655 split), #716 (coordinator next release), #726 (vote on interventions).
+- Related issues: #409 (TUI dashboard, open), #706 (observer follow-up, open), #604 (observer remote fleet, open), #606 (visual parity, closed; holds the Zellij go or no-go), #718 (dashboard items from the 655 split), #716 (coordinator next release), #726 (vote on interventions), #731 (reusable release-planning pipeline that holds the unfiled drafts for this roadmap).
 - Code today: `src/superclaude/cli/observe/` (`view.py`, `questions.py`, `commands.py`, `export.py`), tests in `tests/observe/`, guide `docs/user-guide/observer.md`.
 - The design mockups and "Clay's html dashboards" mentioned in the note: location Not known yet (the 20 synthetic designs are in the design package on branch `docs/409-orca-dashboard-designs`).
 
@@ -26,9 +28,13 @@ Each release in the list then gets its own issue when the owner schedules it; th
 
 Do not build anything from this issue before the owner says go. The owner's order: the architecture and preliminary evaluation come first and take precedence over the release list; the priority is checking what is needed to support the two-way dashboard and building or changing it, including a Postgres database per project. Dashboard, watcher and coordinator work are meant to be developed together as needed.
 
-The goal stated by the owner is NOT to replace talking to the coordinator sessions. It is that the dashboard is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions for the person, and, when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
+The goal is that the dashboard replaces talking to the coordinator sessions directly. It is the one place where the person reads and answers everything the coordinators need (the 1.8 release in the list below is where the first write and respond features arrive: responses and answers go through the dashboard and are relayed to the coordinator). Decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions for the person, and, when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
+
+Open for the owner: the 1.8 line also lists "notifications that the user is needed in the coordinator session for a q&a or longer conversation". Until the dashboard can carry such conversations itself, that notice is the only case where the person still talks to a coordinator directly. Should longer conversations move into the dashboard too, and in which release? (If yes, the 1.8 and 2.0 items need a line for it.)
+
+Reading notes (UNVERIFIED, mine): "Zelij" is read as Zellij; "1\n5 release" is read as 1.5; the version numbers such as 1.105 are kept as the owner wrote them. The planning drafts read the list as: 1.105, 1.505, 1.705 and 1.905 are test-and-CI releases between the numbered ones, and the Zellij review fills the 1.3 slot because the list jumps from 1.2 to 1.4.
 
-Reading notes (UNVERIFIED, mine): "Zelij" is read as Zellij; "1\n5 release" is read as 1.5; the version numbers such as 1.105 are kept as the owner wrote them.
+**Correction (owner, 2026-11-25):** the sentence "The ultimate goal is NOT to replace interacting with the coordinator sessions" in the verbatim text below is wrong. The goal is for the dashboard to replace direct communication with the coordinators; the 1.8 line below (first write and respond features: the person's responses and answers go through the dashboard to the coordinator) is the intent. The same wrong sentence was copied from this issue into the planning folder's release plan and into every epic and feature draft (see the Update above), so those need the same correction before anything is filed. Where this note and the quote conflict, this correction wins. The quote is left unchanged as the record of the original note.
 
 Owner's text, verbatim (2026-11-22):
 
@@ -59,3 +65,5 @@ Owner's text, verbatim (2026-11-22):
 > - Human testing, feedback/feature requests, validation, bug filing and fixing for 1.9 release
 > - 1.905: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests
 > - Implement feedback from 1.9 and additional write/respond features for 2.0 release
+
+

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
