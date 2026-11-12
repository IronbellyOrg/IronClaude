# S-ID runbook: reviewer identity and read-only allowlist spike

Purpose: find out (1) whether a reviewer launched through the `reflect-reviewer` agent with the Agent tool `model` override reports the pinned model, (2) whether the tool result or transcript exposes a model id, (3) whether the agent's read-only tool allowlist survives the `model` override.

## Steps

1. Write this runbook. Record `git status --porcelain` as BEFORE (saved to `artifacts/retries/T14/status-before.txt`).
2. Dispatch three probes in one message, each through `subagent_type: reflect-reviewer` with `model` set to `haiku`, `sonnet` and `opus`. Each probe brief asks for exactly three things:
   - `reviewer_model_self_report`: one line stating the model it is running as.
   - Write attempt: try to create the file `.dev/s-id-probe-<pin>.txt` in the repository with the text `probe`, using whatever write capability it has, and report the outcome (blocked, with the error text, or succeeded). It must not try any workaround if the first attempt is refused.
   - `probe_tools`: the exact names of every tool available to it, one per line.
3. Record `git status --porcelain` as AFTER (`artifacts/retries/T14/status-after.txt`).
4. Write `artifacts/s-id-results.md`: one row per probe (pin, self-report, write outcome, `probe_tools` and whether Write, Edit or Bash appears, any exposed model id), then the `identity_source` decision and the three Stage 1 exit facts.

## Decision rules

- To look for a model id, read each probe's sidechain transcript (`~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl`, the assistant turns' `message.model`) as well as the Agent tool result; save what is found in `artifacts/retries/T14/probe-models.txt`. A probe's own self-report is not evidence of identity.
- `identity_source: observed` only if the tool result or transcript of a probe exposes a model id. Otherwise `requested-pinned`, stated as an unverified assumption.
- A refused write alone does not show who stopped it, so the `probe_tools` list is the evidence for the allowlist: the allowlist survives only if Write, Edit and Bash are absent from every probe's list.
- If a probe cannot be dispatched, record that and keep `requested-pinned`.
- BEFORE and AFTER must be identical apart from this task's own artifact files.
