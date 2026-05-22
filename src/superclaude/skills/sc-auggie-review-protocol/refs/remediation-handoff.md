# Remediation Handoff

After the review report is posted, the skill offers the user a deterministic remediation chain. This file pins the exact phrasing, ordering, and command shapes used in that handoff so the chain is reproducible across invocations and the user always sees the same five-phase flow.

## When the offer fires

The remediation offer is presented only if **all** the following hold:

1. The review completed successfully (`status: success` or `status: partial`).
2. `--remediation-offer` is true (the default).
3. `findings_count.critical + findings_count.high >= 1` — no point offering remediation for a nit-only review.
4. The user has not already declined a remediation offer in this session (avoid badgering).

If the conditions are not met, the skill returns the structured output contract and stops.

## The offer prompt (exact text)

The skill emits this message verbatim to the user (substituting only the bracketed values):

```text
Review complete: [N critical, N high, N medium, N low, N nits] in [report_path]
[Posted to PR #N: <url>]

Would you like to run the full remediation chain on these findings?

  Phase A — /sc:design <report_path> --type architecture --format spec
            (produces a remediation specification document)
  Phase B — task-builder skill on the spec
            (produces an MDTM task file with evidence-backed steps)
  Phase C — /sc:reflect --type task --analyze
            (sanity-checks the tasklist before execution; flags
            scope drift, weak verification criteria, missing rollback)
  Phase D — User-driven execution of the task file
            (the skill does NOT auto-execute; you run /task <path>)
  Phase E — /sc:reflect --type task --validate
            (final gate before commit; blocks if validation fails)

Reply 'yes' to proceed with Phase A, 'no' to stop here, or name a
specific phase if you want to skip ahead (e.g., 'start at Phase B
using existing spec at <path>').
```

The offer must be a single message, not a yes/no AskUserQuestion form — the user might want to skip phases or reroute, and a binary form forecloses that.

## Phase A — `/sc:design`

If the user accepts, the skill invokes:

```
/sc:design <REVIEW.md path>
  --type architecture
  --format spec
  --output <output_dir>/remediation-spec.md
```

Rationale for the flag choices:

- `--type architecture`: even for narrow-bug findings, `/sc:design` treats the input as a structured input and produces a spec; `architecture` is the broadest type, which is correct because reviews typically span multiple concerns. If the user prefers a tighter type, they can override.
- `--format spec`: not `code` (we're not implementing yet) and not `diagram` (we want text that the task-builder can consume).
- `--output <output_dir>/remediation-spec.md`: keeps the artifact next to the review for traceability.

On `/sc:design` completion:

- Capture the spec path.
- Surface the spec path to the user with a one-line summary.
- Proceed to Phase B unless the user says stop.

## Phase B — `task-builder` skill

The `task-builder` skill is invoked via natural language, not a slash command, because it's a skill (not a command). The skill triggers on phrases like "build a task file from..." per its description.

The skill invokes the task-builder by emitting:

```
> Skill task-builder
```

with a BUILD_REQUEST that points at the remediation spec:

```text
GOAL: Build a task file to remediate the findings in <output_dir>/REVIEW.md,
      following the remediation specification at <output_dir>/remediation-spec.md.

WHY: Code review of <PR/diff/snapshot identifier> surfaced <N critical, N high>
     findings that must be addressed before merge. The remediation spec defines
     the structural changes; this task file should translate those into
     evidence-backed, executable steps.

WHERE: <list of files cited in the review's Critical and High sections>

BUILD_REQUEST file: <output_dir>/BUILD-REQUEST-REMEDIATION.md
```

Before invoking, the skill writes the BUILD-REQUEST file with GOAL, WHY, OUTPUTS, CONTEXT, and a TEMPLATE preference (defaults to the project's standard MDTM template).

On task-builder completion:

- Capture the task file path from the skill's output.
- Surface it with a one-line summary.
- Proceed to Phase C unless the user says stop.

## Phase C — `/sc:reflect --type task --analyze`

The skill invokes:

```
/sc:reflect --type task --analyze
```

with the new task file as the implicit current task context (or pass the task file path explicitly if the user is in a session where multiple tasks are open).

`/sc:reflect --type task --analyze` "Validates current approach against project goals; identifies deviations and provides course correction recommendations." Per its `## Behavioral Flow`, it uses Serena's `think_about_task_adherence` and `think_about_collected_information` tools.

For our purposes, the analyze pass is a **pre-execution sanity check**. We're not asking "is this task done?" — we're asking "is this task plan well-formed enough to execute?". Specifically, the skill expects the reflect output to address:

- Are the verification criteria for each task item strong enough to detect failure?
- Are there obvious scope-drift risks (task items that have grown beyond what the review findings warrant)?
- Is there a rollback / abort path documented?
- Are dependencies between task items explicit?

On reflect-analyze completion:

- If reflect-analyze reports **no significant concerns**: surface that, then ask the user "Proceed to Phase D (execute) or refactor the tasklist first?"
- If reflect-analyze reports **concerns**: surface them, and ask "Refactor the tasklist to address these, or override and proceed?"
- If the user chooses to refactor: invoke `task-builder` again with the reflect-analyze concerns appended to the BUILD-REQUEST, then re-run Phase C. Cap at 2 refactor cycles to avoid infinite loops.

## Phase D — Execution (user-driven)

The skill **does not auto-execute** the task file. It surfaces the task file path and the recommended execution command:

```text
Tasklist validated. Ready to execute.

  Run: /task <task-file-path>

The skill will wait. When execution completes, reply 'done' or
'execution complete' and I'll run the final validation gate.
```

Rationale: execution can be long and may want to be split across sessions; forcing the user to confirm gives them control. Also, the user may want to spot-check the task file before running it.

After the user signals execution is complete, proceed to Phase E. If the user closes the session here, the skill returns the structured output contract with `remediation_status: in_progress`.

## Phase E — `/sc:reflect --type task --validate`

The skill invokes:

```
/sc:reflect --type task --validate
```

This is the **final gate before commit**. Per `/sc:reflect`'s `## Behavioral Flow`, `--validate` "Comprehensive analysis of session work and information gathering; quality assessment and gap identification."

The validate pass checks:

- Were all task items completed?
- Do the completed artifacts satisfy the verification criteria each task item declared?
- Are there any new defects introduced during execution?
- Is the change minimal (no scope creep beyond what the original review findings required)?

On validate completion:

- If validate **passes**: surface that, and recommend the user commit. Do not auto-commit. The recommended commit message format is `fix(<scope>): remediate findings from <review-id>` with a reference to the review URL in the body.
- If validate **fails**: surface the issues and ask the user how to proceed (re-run Phase D? Open a new review? Bail?). Do not recommend commit until validate passes.

## Resumability

If the user closes the session mid-chain, the skill writes the chain's state to `<output_dir>/remediation-state.json`:

```json
{
  "phase": "<A|B|C|D|E>",
  "last_completed": "<phase>",
  "artifacts": {
    "review_path": "...",
    "spec_path": "...",
    "task_file_path": "...",
    "task_reflect_analyze_result": "...",
    "task_reflect_validate_result": "..."
  },
  "started_at": "<iso>",
  "last_updated_at": "<iso>"
}
```

When the user re-invokes the skill with `--resume <output_dir>`, the chain picks up at the recorded phase.

## Anti-patterns to avoid

- **Don't auto-execute Phase D**. The most common failure mode of agentic remediation chains is silent execution of half-baked plans. The pause-for-user-confirmation pattern is intentional friction.
- **Don't skip Phase C even if findings are "obviously small"**. The reflect-analyze pass is cheap and catches scope-drift early.
- **Don't proceed to commit if Phase E fails**. The whole point of having a final validate gate is to refuse to commit broken work.
- **Don't bundle the offer into an AskUserQuestion**. The user might want to start at Phase B with an existing spec, skip Phase C, etc. A free-form text offer preserves that flexibility.
- **Don't badger the user**. If they say no, that's the final answer for this review.
