Please carry out this task from my Orca coordinator by following the brief I pasted below. 

<pasted_content id="825b">
You are working inside Orca, a multi-agent IDE. You are a dispatched worker.
Your coordinator's terminal handle is: term_feb70160-0a10-426d-810c-502bd6f00e63
Your task ID is: task_7d6a85904c3d

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
  orca orchestration send --from term_5453057a-ec2e-40be-a9bf-095e78122165 --type worker_done --subject "<short status>" --body "<3-sentence summary: what you did, what you found, what's left>" --task-id task_7d6a85904c3d --dispatch-id ctx_f77ae7eb2fd6 --outcome succeeded

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
  orca orchestration send --from term_5453057a-ec2e-40be-a9bf-095e78122165 --type heartbeat --subject "alive" --task-id task_7d6a85904c3d --dispatch-id ctx_f77ae7eb2fd6 --phase "<short: investigating|implementing|reviewing|waiting>"

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
  orca orchestration ask --from term_5453057a-ec2e-40be-a9bf-095e78122165 --question "<your question>" --options "<optional,comma,separated>" --timeout-ms 600000

  # Escalate a blocker or failure (pre-completion, when you need the
  # coordinator to do something before you can continue):
  orca orchestration send --from term_5453057a-ec2e-40be-a9bf-095e78122165 --type escalation --subject "Blocked: <reason>" --body "<details>" --task-id task_7d6a85904c3d --dispatch-id ctx_f77ae7eb2fd6

  # Read coordinator follow-ups. Nothing interrupts you: a durable message only
  # arrives when you look, so run this at each natural checkpoint — before you
  # start a new file and after a test run — and once more immediately before
  # you send worker_done, so a redirect lands before the task settles.
  orca orchestration check --terminal term_5453057a-ec2e-40be-a9bf-095e78122165 --json
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
Task 6, revise the spec. Inputs: .dev/orca-command-refactor/review/spec-panel.md and the spec. Change: verify each numbered finding against the evidence; apply confirmed findings to .dev/orca-command-refactor/specs/orca-worker-contract-spec.md; write .dev/orca-command-refactor/review/disposition.md with one row per finding: applied (where) or rejected (cited reason). Acceptance: every finding has a disposition row; the spec has no placeholder left. Report path: review/disposition.md. Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. First read .dev/orca-command-refactor/README.md (shared goal, evidence and rules; they are binding). Ownership: write ONLY your output file(s); planning only, no edits to src/, tests/, docs/, .claude/, ~/.claude or Orca settings, no git commits/pushes/PRs. Cite path:line for every claim, mark unverified items UNVERIFIED, stub the output file first and fill it section by section. Finish with worker_done --report-path <your output file>.
</pasted_content id="825b">
