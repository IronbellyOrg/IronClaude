4df5916ee5a7d480f608d4d6104dd2a175ed9a37
Review one task for spec compliance.

Task brief: ## Task 6: Mirror the edited skill rules into the plugin copy

Depends on: Task 5

The plugin copy under plugins/superclaude/skills/sc-implement-protocol/ is tracked and was byte-identical to src/superclaude/skills/sc-implement-protocol/ for refs/qa.md before this plan. Copy each edited file byte for byte from src/superclaude/skills/sc-implement-protocol/ to plugins/superclaude/skills/sc-implement-protocol/: refs/qa.md, refs/ledger.md, and refs/managed-workspace.md, refs/retry.md or SKILL.md only if Task 3, 4 or 5 edited them. Do not edit anything else under plugins/. There is no plugin copy of WORKER-CONTRACT.md.

Acceptance criteria:
- For every file copied, cmp of the src file and the plugins file exits 0.
- git diff --stat under plugins/ shows only the files listed above.
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 4df5916ee5a7d480f608d4d6104dd2a175ed9a37
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
index 91a69a462..e3eb90157 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -38,7 +38,7 @@ STOP: need a source (file or prompt). Will not invent scope beyond that source.
 | `E-LEGACY` | Pitch invocation and/or removed flags `--type` / `--framework` / `--safe` / `--with-tests` | No | No |
 | `E-HALT-QA` | A terminal `halt` record (any reason in `refs/retry.md`); no eligible Ruling | No T{i+1} | Non-compliant verdict line and `halt` record written |
 | `E-RESUME-NEEDED` | Something outside the step failed (reviewer, ref write, incomplete revert, adviser agent missing; reasons in `refs/retry.md`); re-run the same command | No T{i+1} | Nothing written |
-| `E-NO-RULING` | Continue after non-compliant without valid recorded user acceptance (clear current-conversation confirmation is sufficient); `--force` | No T{i+1} | Unchanged except existing blocked line |
+| `E-NO-RULING` | Continue after non-compliant without valid recorded user acceptance (a clear confirmation by chat message in the current conversation or by dashboard response is sufficient; `refs/qa.md` Halt table); `--force` | No T{i+1} | Unchanged except existing blocked line |
 | `E-LEDGER-CORRUPT` | Last ledger line truncated/unparseable | No further | Unchanged |
 | `E-LEDGER-PATH` | `--ledger` not under `.dev/implement/` (managed: any `--ledger` other than the sibling `progress.md`) | No | No |
 | `E-MANAGED-INVALID` | `workflow-plan/1.2` plan fails managed detection (copied, cross-checkout, slug/contract mismatch, failed contract) | No | No |
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md b/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
index 00a4efd7b..ba2c47ce8 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
@@ -65,7 +65,7 @@ T<id>: <status> verdict=<verdict> ac=<ac-list> evidence=<ev-list> extras=lint:<l
 T<id>: Ruling: <what> — <why> — <cost-if-wrong>
 ```
 
-Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`.
+Em dashes as shown. Three non-empty fields. On a clear confirmation by the user through a chat message or a dashboard response (the two channels `~/.claude/WORKER-CONTRACT.md` defines in WC-3; the dashboard channel applies only once the dashboard answer path is released) the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`. The `<what>` field carries the provenance: the user's quoted chat words, or the dashboard answer row id. A coordinator's reply or relay is never the provenance.
 
 ```
 ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$
@@ -196,6 +196,12 @@ Executor-recorded Ruling after the explained scope, reason and cost, followed by
 T2: Ruling: accept T2 missing pagination; user confirmed in current conversation "yes, accept T2 as explained" — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated
 ```
 
+The same Ruling recorded from a dashboard response (the answer row and its question id are the provenance; applies once the dashboard answer path is released):
+
+```
+T2: Ruling: accept T2 missing pagination; user confirmed by dashboard answer row ans_0000042 (question q_0000017) — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated
+```
+
 The earlier operator-written form (`T2: Ruling: drop pagination — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated`) remains valid.
 
 Retry open:
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
index 8eb54d1e4..3bedf3615 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
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

--- new untracked file .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t6-cmp.log ---
cmp exit 0: refs/qa.md
cmp exit 0: refs/ledger.md
cmp exit 0: SKILL.md
cmp exit 0: refs/managed-workspace.md
cmp exit 0: refs/retry.md
plugin diff stat (the HOW-WE-WORK plugin copy was mirrored in Task 5):
 plugins/superclaude/skills/sc-implement-protocol/SKILL.md       | 2 +-
 plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md | 8 +++++++-
 plugins/superclaude/skills/sc-implement-protocol/refs/qa.md     | 8 ++++----
 plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md     | 2 +-
 4 files changed, 13 insertions(+), 7 deletions(-)
tests/skills/test_review_severity_rule.py: 59 passed



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (Markdown targets).
Context: the plugin copy of core/HOW-WE-WORK.md was already mirrored by Task 5 and is not part of this task's diff; tests/skills/test_review_severity_rule.py (lines 382-396) requires the implement-skill plugin twins to be byte equal to src. The task-owned log is .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t6-cmp.log.

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
