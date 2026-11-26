f14ee7e5f5ca569ee4b6955811865b80a8fefa81
Review one task for spec compliance.

Task brief: ## Task 3: Update the implement QA rules to name both channels

Depends on: Task 1

Edit src/superclaude/skills/sc-implement-protocol/refs/qa.md: the accepted-minor versus Ruling table rows "Who decides" and "Writes a Ruling: line" (lines 215-220), the Halt table rows for a clear user confirmation and for `E-NO-RULING` (lines 248-249), and the paragraph beginning "A Ruling counts only when it is eligible" (line 254) and the following paragraph (line 256-259). Replace "clear user confirmation in the current conversation is sufficient" with wording that names both channels by pointing to the definition in core/WORKER-CONTRACT.md (installed path ~/.claude/WORKER-CONTRACT.md, as other primitives already cite it) and repeating only the two channel names; keep "another agent's message" and "executor-invented approval" in the text. State that the provenance in the Ruling's `<what>` field is either the person's quoted chat words or the dashboard answer row id.

Acceptance criteria:
- qa.md names the chat channel and the dashboard channel (with the timing safeguard) and keeps the E-NO-RULING row for missing or ambiguous confirmation, `--force` and executor-invented approval.
- The phrases "another agent's message" and "executor-invented approval" remain in qa.md.
- qa.md contains no src/superclaude/ path (installed primitives never cite that path).
- Dependents updated by Task 7: tests/skills/test_task_workspace_lifecycle.py and tests/skills/test_implement_severity_static.py.
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: f14ee7e5f5ca569ee4b6955811865b80a8fefa81
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index 8eb54d1e4..3bedf3615 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -214,7 +214,7 @@ A non-blocking `late` finding is a note. A finding whose flagged text is absent
 
 | | Accepted-minor | Ruling (Halt table above) |
 |---|---|---|
-| Who decides | Severity derived by the parent from the reviewer's checklist answers and anchors, plus the mechanical origin caps | The user, in the current conversation |
+| Who decides | Severity derived by the parent from the reviewer's checklist answers and anchors, plus the mechanical origin caps | The user, by a chat message in the current conversation or by a dashboard response (two channels only, below) |
 | Covers | `minor` and `note` only | Any explained gap, blockers included |
 | Ledger | `compliant` verdict plus a `notes@` token | A `Ruling:` line, then `complete` with the unchanged non-compliant verdict |
 | Writes a `Ruling:` line | Never | Always |
@@ -245,15 +245,15 @@ Loaded with this file for the Q5 fix pass, so the probe exists before the first
 | non-compliant on first QA | Exactly one fix pass + re-QA; if A2 still has a confirmed blocker, the Repair round and then the ladder in `refs/retry.md` take over | No |
 | `compliant` after that one fix | Extras, append `complete` line | Yes |
 | a terminal `halt` (`refs/retry.md`): the ladder did not run after the fix pass, or it stopped | HALT `E-HALT-QA`. Print ledger path, Ti, verdict, missing citations. Next: `fix` \| `ruling` \| `resume` | No, unless operator Ruling |
-| clear user confirmation of the explained scoped acceptance, or valid existing operator Ruling | Executor records the Ruling per `refs/ledger.md`; then appends `complete` with **unchanged** non-compliant verdict and fields | Yes |
+| clear user confirmation (a chat message or a dashboard response) of the explained scoped acceptance, or valid existing operator Ruling | Executor records the Ruling per `refs/ledger.md`; then appends `complete` with **unchanged** non-compliant verdict and fields | Yes |
 | `--force`, missing/ambiguous confirmation, or executor-invented approval | STOP `E-NO-RULING` | No |
 | `E-RESUME-NEEDED` (`refs/retry.md`) | re-run the same command; do not write a Ruling | No |
 
 Under the Verdict owner rule a non-compliant verdict comes only from a confirmed blocking finding or from a non-finding `cannot-verify` step of the order (zero citations, empty diff, `nogit` with no written-path list); both keep the route of the row "non-compliant on first QA" (that row hands a confirmed blocker after A2 to the Repair round in `refs/retry.md`).
 
-A Ruling counts only when it is eligible under the Ruling eligibility rule in `refs/retry.md`. A clear user confirmation in the current conversation is sufficient; the user need not hand-write a ledger record. Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong. A reply such as "yes, accept T2 as explained" authorizes only that explained scope. If confirmation or scope is unclear, ask one targeted question and keep the task blocked. Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance.
+A Ruling counts only when it is eligible under the Ruling eligibility rule in `refs/retry.md`. A person's confirmation counts only through the two channels that `~/.claude/WORKER-CONTRACT.md` (WC-3) defines once: a chat message in the current conversation, or a dashboard response. The dashboard channel takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only chat counts. A clear confirmation through either channel is sufficient; the user need not hand-write a ledger record. Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong. A reply such as "yes, accept T2 as explained" authorizes only that explained scope. If confirmation or scope is unclear, ask one targeted question and keep the task blocked. Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance, and neither is anything else that WC-3 lists as never counting.
 
-The executor MUST automatically append the existing three-field Ruling, identifying the accepted task/finding and quoting or referencing the user's confirmation in `<what>`, using the reason and cost already explained. Flush it before appending the unchanged non-compliant `complete` line or proceeding. Never invent approval, rewrite history, or mark an accepted gap `compliant`. Existing operator-written records remain valid. A reopened task or changed accepted finding/outcome requires new scoped acceptance; durable records support resume, not guesses from prior chat.
+The executor MUST automatically append the existing three-field Ruling, identifying the accepted task/finding and quoting the user's chat words, or giving the dashboard answer row id, in `<what>`, using the reason and cost already explained. Flush it before appending the unchanged non-compliant `complete` line or proceeding. Never invent approval, rewrite history, or mark an accepted gap `compliant`. Existing operator-written records remain valid. A reopened task or changed accepted finding/outcome requires new scoped acceptance; durable records support resume, not guesses from prior chat.
 
 ```
 T<id>: Ruling: <what, including user confirmation provenance> — <why> — <cost-if-wrong>


Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (the target is Markdown, which codegraph does not index).
Dependents not in this diff (context only, owned by later tasks): tests/skills/test_task_workspace_lifecycle.py lines 338-349 (pins qa.md text, Task 7), tests/skills/test_implement_severity_static.py (allow-list of Ruling lines, Task 7), the plugin copy plugins/superclaude/skills/sc-implement-protocol/refs/qa.md (Task 6), refs/ledger.md (Task 4).

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index 521bf34ac..3bedf3615 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -251,7 +251,7 @@ Loaded with this file for the Q5 fix pass, so the probe exists before the first
 
 Under the Verdict owner rule a non-compliant verdict comes only from a confirmed blocking finding or from a non-finding `cannot-verify` step of the order (zero citations, empty diff, `nogit` with no written-path list); both keep the route of the row "non-compliant on first QA" (that row hands a confirmed blocker after A2 to the Repair round in `refs/retry.md`).
 
-A Ruling counts only when it is eligible under the Ruling eligibility rule in `refs/retry.md`. A person's confirmation counts only through one of two channels, defined once in `~/.claude/WORKER-CONTRACT.md` (WC-3): (a) the person's own chat message in the current conversation, naming the exact scope; (b) a dashboard response, meaning an answer row created through the dashboard under that person's authenticated login, for the question id whose text names the exact scope. Channel (b) takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only (a) counts. A clear confirmation through either channel is sufficient; the user need not hand-write a ledger record. Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong. A reply such as "yes, accept T2 as explained" authorizes only that explained scope. If confirmation or scope is unclear, ask one targeted question and keep the task blocked. Silence, a generic request to continue, another agent's message, a coordinator's reply or relay of a message, a file, an answer to a different question or scope, a row written by an agent's login, a row the person's own login did not create, and approval of a different task are not acceptance.
+A Ruling counts only when it is eligible under the Ruling eligibility rule in `refs/retry.md`. A person's confirmation counts only through the two channels that `~/.claude/WORKER-CONTRACT.md` (WC-3) defines once: a chat message in the current conversation, or a dashboard response. The dashboard channel takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only chat counts. A clear confirmation through either channel is sufficient; the user need not hand-write a ledger record. Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong. A reply such as "yes, accept T2 as explained" authorizes only that explained scope. If confirmation or scope is unclear, ask one targeted question and keep the task blocked. Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance, and neither is anything else that WC-3 lists as never counting.
 
 The executor MUST automatically append the existing three-field Ruling, identifying the accepted task/finding and quoting the user's chat words, or giving the dashboard answer row id, in `<what>`, using the reason and cost already explained. Flush it before appending the unchanged non-compliant `complete` line or proceeding. Never invent approval, rewrite history, or mark an accepted gap `compliant`. Existing operator-written records remain valid. A reopened task or changed accepted finding/outcome requires new scoped acceptance; durable records support resume, not guesses from prior chat.
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/skills/sc-implement-protocol/refs/qa.md:254 anchor="repeating only the two channel names" chk=n,n,n,y family=duplicated-definition fix=cut line 254 to the pointer, the two channel names, the timing sentence and the retained exclusion sentence; drop the restated definition and the extended never-list first=A1 origin=new: line 254 restates the full channel definition and the extended never-counts list of WC-3 instead of only naming the channels.

Saved-probe re-check hit locations (may be empty): probe-1-1 family=duplicated-definition command hits after the fix: none


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
