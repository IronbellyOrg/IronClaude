Please carry out this task from my Orca coordinator by following the brief I pasted below. 

<pasted_content id="a412">
You are working inside Orca, a multi-agent IDE. You are a dispatched worker.
Your coordinator's terminal handle is: term_8fb192ce-19ad-49b3-b7df-39451da0697c
Your task ID is: task_0ffe03bb1425

The coordinator cannot see this terminal, so reach it with the `orca orchestration`
commands below; a question or result left only in this terminal never gets to it.
Don't post to Slack, GitHub, or other channels during the run; report through these commands.

=== CLI COMMANDS ===

```sh
  # Report the task outcome (required, exactly once).
  #
  # --body must be a 3-sentence executive summary (what you did,
  # what you found, what's left). Never send an empty body; the coordinator
  # reads the body first and only opens artifacts if it needs more detail.
  # Append --files-modified only when files changed, and append --report-path
  # only when you produced a durable report. Always pass real values; do not
  # send the example placeholders literally.
  #
  # Send worker_done exactly once. Use --outcome succeeded when the
  # requested work is done, or replace it with --outcome failed when it is not.
  # Never encode failure only in prose and never silently exit.
  # Include BOTH taskId and dispatchId in the payload so a late completion
  # from a failed retry cannot complete the current dispatch.
  orca orchestration send --from term_b1776e00-e90d-4403-8c1c-9a1fa0ec030c --type worker_done --subject "<short status>" --body "<3-sentence summary: what you did, what you found, what's left>" --task-id task_0ffe03bb1425 --dispatch-id ctx_cafa62af9b4a --outcome succeeded

  # Send a heartbeat every 5 minutes
  # while actively working on the task. The coordinator uses this to
  # distinguish "still thinking" from "hung / crashed." Skip heartbeats only
  # while blocked inside `check --wait` or `ask` — those calls are
  # themselves liveness signals. If a background loop sends them, restart
  # it if it expires mid-task, and stop it before you send worker_done.
  #
  # Include BOTH taskId and dispatchId in the payload: the coordinator
  # attributes the heartbeat to the specific dispatch context, not just
  # the task, so a straggler heartbeat from a previously-failed dispatch
  # cannot mask a hung retry.
  orca orchestration send --from term_b1776e00-e90d-4403-8c1c-9a1fa0ec030c --type heartbeat --subject "alive" --task-id task_0ffe03bb1425 --dispatch-id ctx_cafa62af9b4a --phase "<short: investigating|implementing|reviewing|waiting>"

  # Ask the coordinator a question and block until it answers.
  #
  # Use this instead of AskUserQuestion: that opens a local prompt the
  # coordinator cannot see or answer, so the task would stall until someone
  # happened to look at this terminal. Send every question through `ask`.
  #
  # The `ask` verb durably records a question in this Dispatch's Run and
  # blocks until the coordinator replies, then prints the reply body. If the
  # call times out or disconnects, resume with the returned message ID instead
  # of creating a duplicate question.
  orca orchestration ask --from term_b1776e00-e90d-4403-8c1c-9a1fa0ec030c --question "<your question>" --options "<optional,comma,separated>" --timeout-ms 600000

  # Escalate a blocker or failure (pre-completion, when you need the
  # coordinator to do something before you can continue):
  orca orchestration send --from term_b1776e00-e90d-4403-8c1c-9a1fa0ec030c --type escalation --subject "Blocked: <reason>" --body "<details>" --task-id task_0ffe03bb1425 --dispatch-id ctx_cafa62af9b4a

  # Read coordinator follow-ups. Nothing interrupts you: a durable message only
  # arrives when you look, so run this at each natural checkpoint — before you
  # start a new file and after a test run — and once more immediately before
  # you send worker_done, so a redirect lands before the task settles.
  orca orchestration check --terminal term_b1776e00-e90d-4403-8c1c-9a1fa0ec030c --json

  # After processing every message, ack the returned deliveryId; this also reads
  # the next batch. Repeat until count is 0, then resume. Unacked batches replay
  # and hide newer mail.
  orca orchestration check --terminal term_b1776e00-e90d-4403-8c1c-9a1fa0ec030c --ack <delivery_id> --json
```

=== AFTER YOU SEND worker_done ===

worker_done ends your turn for this task. Your dispatched work is complete:
stop, return to an idle prompt, and take no further actions — do NOT start
new or unrelated work, do NOT run a sleep/poll loop, and do NOT keep calling
`orca orchestration check`. The coordinator has already recorded your
completion and expects no further output.

A direct instruction from the user takes precedence over this idle rule.
Treat it as new user-owned work: follow it without coordinator approval or a
fresh Dispatch, and do not send lifecycle messages using the settled task or
Dispatch IDs. Never refuse a direct user request because you were a worker.

Do not exit the shell. Your terminal stays available, and if the
coordinator has more for you it will re-engage this terminal with a fresh
preamble + TASK block, which arrives as new input. Treat that as supervised
work under the new Dispatch; ignore stale follow-ups from the settled task.

=== TASK ===
Resume the issue 478 BMAD first-use research in this existing bmad-ponytail-global worktree (IronbellyOrg/Coder). Prior dispatch ctx_45c984b66310 settled failed only because it asked the coordinator about a review-limit exception and the answer arrived after it had stopped; this is new work, so do not reuse that dispatch. The USER HAS EXPLICITLY DECIDED (2026-11-07) for the exception it asked about: apply the one-sentence fix to the Gate 4 web-source table of .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md (task-file lines about 421 and 423, with the web-access-unavailable wording at lines about 279 and 283): allow one row "none | reason" and call that table complete when web access is unavailable. Do NOT run a fourth review of the task file, leave the 5 minor wording gaps alone, and record in the final report that the user explicitly accepted this one exception to the 3-review limit and which lines you changed. Then run the research by executing that task file using the tech-research skill (invoke its backing skill, resume rather than rebuild; same depth as built), read the actual report, and answer the three open questions the prior worker listed: (a) can BMAD create its needed directories on first use without a global BMAD install and without breaking the per-project rule, given bmad 6.9.0 declares a user-home skills path for Claude Code that nothing in the installer reads (UNVERIFIED, test it from code), (b) does a user-level stub skill count as user level under the 2026-09-25 OD-1 wording (surface this as a user decision, do not decide it), (c) what counts as first use (CLI command, BMAD skill invocation or opening a session) with options and your recommendation. Context to keep: the user decided BMAD SHOULD create directories on first use (supersedes OD-1 for first-use directory creation only); global BMAD install is NOT requested; the Ponytail gap is out of scope until evidence E-1 to E-3 exists (see .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md). Then write .dev/issues/478/spec.md covering only the BMAD first-use ask, citing the user decision, listing the pinned tests and docs that must change (test-57-catalogue-configure.sh, test-startup-boot.sh, README, manifest), and run /sc:workflow .dev/issues/478/spec.md --depth standard --handoff none (invoke its backing skill), reading the printed plan and advisory check. If the research shows the ask needs a global install or another repo (IronClaude, IronOrca), STOP, touch no other repo, and report the re-scope. If you need a user decision mid-run, use the live preamble ask and WAIT for the reply; do not stop early. Keep the model this session started with (no /model). LIMITS: research, spec and plan outputs plus the one approved task-file sentence only. No product-code edits, no /sc:implement, no commit, push, PR, GitHub comment or merge. Stage .dev/tasks; never stage root artifacts/ or env captures. No cd (use git -C and absolute paths); UV only; validation belongs to existing GitHub Actions, no one-off scripts. Mark unverified items UNVERIFIED. Send worker_done once with report path, spec path, plan path, advisory result and unresolved user decisions.
</pasted_content id="a412">
