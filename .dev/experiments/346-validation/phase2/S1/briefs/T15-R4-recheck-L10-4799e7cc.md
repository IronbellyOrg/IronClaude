Please carry out this task from my Orca coordinator by following the brief I pasted below. 

<pasted_content id="d3ef">
You are working inside Orca, a multi-agent IDE. You are a dispatched worker.
Your coordinator's terminal handle is: term_cddf23a9-82f5-45ee-a9b8-1fdd61d80197
Your task ID is: task_dcf1a60db1bb

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
  orca orchestration send --from term_b4734a3d-568d-42b9-ac49-6183737dbb97 --type worker_done --subject "<short status>" --body "<3-sentence summary: what you did, what you found, what's left>" --task-id task_dcf1a60db1bb --dispatch-id ctx_325fac87b297 --outcome succeeded

  # Send a heartbeat every 5 minutes
  # while actively working on the task. The coordinator uses this to
  # distinguish "still thinking" from "hung / crashed." Skip heartbeats only
  # while blocked inside `check --wait` or `ask` — those calls are
  # themselves liveness signals.
  #
  # Include BOTH taskId and dispatchId in the payload: the coordinator
  # attributes the heartbeat to the specific dispatch context, not just
  # the task, so a straggler heartbeat from a previously-failed dispatch
  # cannot mask a hung retry.
  orca orchestration send --from term_b4734a3d-568d-42b9-ac49-6183737dbb97 --type heartbeat --subject "alive" --task-id task_dcf1a60db1bb --dispatch-id ctx_325fac87b297 --phase "<short: investigating|implementing|reviewing|waiting>"

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
  orca orchestration ask --from term_b4734a3d-568d-42b9-ac49-6183737dbb97 --question "<your question>" --options "<optional,comma,separated>" --timeout-ms 600000

  # Escalate a blocker or failure (pre-completion, when you need the
  # coordinator to do something before you can continue):
  orca orchestration send --from term_b4734a3d-568d-42b9-ac49-6183737dbb97 --type escalation --subject "Blocked: <reason>" --body "<details>" --task-id task_dcf1a60db1bb --dispatch-id ctx_325fac87b297

  # Read coordinator follow-ups. Nothing interrupts you: a durable message only
  # arrives when you look, so run this at each natural checkpoint — before you
  # start a new file and after a test run — and once more immediately before
  # you send worker_done, so a redirect lands before the task settles.
  orca orchestration check --terminal term_b4734a3d-568d-42b9-ac49-6183737dbb97 --json
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
Task 15, recheck after fix pass 1. You did not write the spec or the fixes. Inputs: current spec, frozen baseline specs/history/spec-v5-after-round4.md, review/round4-review.md, APPROVED.md 'Round-4 review fixes', the 'Fix pass 1' section of review/disposition-round4.md. Scope (binding): (1) diff baseline and current spec; (2) confirm from the spec text that B1 and B2 are fixed as APPROVED.md states; (3) check ONLY the changed lines for new blocking defects, including contradictions with the unchanged lines they touch and citations on them; (4) flag any change beyond B1, B2 and their consequential edits. Do not recheck minor findings, do not run /sc:spec-panel, do not review unchanged text. Grade findings blocking or minor as in round4-review.md. Output: append a section 'Recheck after fix pass 1' to .dev/orca-command-refactor/review/round4-review.md with a B1/B2 resolution table, any findings, and a binary verdict: PASS if no blocking finding, otherwise FAIL. On PASS include a Self-Audit naming what you checked. Ownership: edit ONLY round4-review.md (append only). Report path: review/round4-review.md. Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. First read .dev/orca-command-refactor/README.md (shared rules; binding) and .dev/orca-command-refactor/decisions/APPROVED.md (owner-approved inputs, including the new 'Round-4 review fixes' table; binding, not open for debate). Planning only: no edits to src/, tests/, docs/, .claude/, ~/.claude or Orca settings; never run superclaude install; no git commits, pushes, PRs or GitHub posts; never interact with SuperClaude upstream. Cite path:line for claims, mark unverified items UNVERIFIED, stub any new output file first. Review rule (merged PR #343): only blocking findings fail a review; minor findings are notes and trigger no fix. Finish with worker_done --report-path <your report file>.
</pasted_content id="d3ef">
