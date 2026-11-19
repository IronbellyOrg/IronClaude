ce29bcda4f5cb5efdd7b720f7e78c81cd1f36e63

REVIEW RE-RUN (r4-2) after the A2 fix pass. Task brief, constraints and start sha unchanged; the fix-pass delta is saved at artifacts/retries/T4/delta-4-2.txt (read it). Earlier blocking findings of this start:
Review one task for spec compliance.

Task brief: Task 4 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 90-120). Deliverables: session-a.sh and session-a2.sh; prompt files in .dev/issues/442/scripts/prompts/ copied byte for byte from the runbook's text blocks; session A items in runbook order (item 1 line 234, item 3 line 253, item 4 lines 268-281 incl. the literal /sc:implement x then Esc, item 2 line 286, item 5 lines 304/308/312 through wait-notice, item 6 line 330, item 9 line 349, item 8 line 366, LL-NOBIND line 385, OB-CTX part 1 lines 401/405/409/413/417, plus /hooks at runbook line 168, the item-7 first prompt at line 445, /exit --resume /clear and --continue --fork-session restarts at line 428, say ok in each, own-shell MAIN read at line 225 and human tree/push at lines 424-425); session A2 starts per section 2.1b (claude --settings /tmp/ob/settings-a2.json, runbook line 452), checks the h1m log is non-empty (line 455), sends the MCP prompt at line 458, ends with /exit; each script saves the screen after every prompt and stops at the first NEEDS_INPUT or timeout recording PENDING with the screen file. Session start uses the create-with-cd form (no directory flag exists on orca terminal create; F05 fix in the plan): --command "cd $OB/repo-a && HOME=... claude". AC ids: T4.AC1 = "A self-test case extracts every `text` block in runbook lines 228-472 and diffs it against the prompt files: no missing prompt and no changed byte."; T4.AC2 = "With the stub driver, the self-test shows session A sending the prompts in runbook order, and stopping with `PENDING` at a scripted `NEEDS_INPUT`."; T4.AC3 = "No prompt file starts with `[sc-launch:v1:`. The only file holding the marker is the LL-NOBIND prompt file (a self-test grep)."

Global constraints: plan lines 17-27 (read them). Key: every script set -u -o pipefail, umask 077, external calls timeout-bounded; scratch under /tmp/ob (OB overridable); no change to src/ or tests/; marker only at the LL-NOBIND step; settings/hook/git-config/launch-store changes never from prompts (own shell only).

Start sha: ce29bcda4f5cb5efdd7b720f7e78c81cd1f36e63

Diff against the start snapshot: new files under .dev/issues/442/scripts/ — read session-a.sh, session-a2.sh, session-a-selftest.sh in full, the changed selftest.sh (STUB_NOTICE stages the notice pair), and the 17 prompt files under .dev/issues/442/scripts/prompts/ (spot-check at least p01, p04, p10, p17 against runbook lines 235, 305, 386, 458). The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t4-selftest.txt (read it). Runbook grounding: .dev/issues/442/observation-runbook.md lines 228-472.

Delta diff from the previous reviewed tree (empty on the first review):

Earlier blocking findings of this start (empty on the first review):

Saved-probe re-check hit locations (may be empty):

F4.1 sev=blocking trigger=B1 family=selftest-order-partial: order assertion covered only the first four sends.
F4.2 sev=blocking trigger=B4 family=timeout-no-stop: plain TURN_END timeout was not a stop; notice-PENDING lacked the screen file.
F4.3 sev=blocking trigger=B4 family=a2-exit-not-sent: session A2 ended by terminal close, /exit never sent.
Saved-probe re-check hit locations: probe-4-1.md after-lines cover the full-order loop, the TURN_END timeout arms with screen files, and the /exit send with a 5s bound.
Do not trust the implementer's report.
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
