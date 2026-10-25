# Remediation Handoff

After the review report is posted, the skill offers the user a deterministic remediation chain. This file pins the exact phrasing, ordering, and command shapes used in that handoff so the chain is reproducible across invocations and the user always sees the same five-phase flow.

## Remediation chain

Every review `--depth`, including `deep`, uses the same chain: `sc:workflow-protocol` on the remediation spec produces the managed package `.dev/tasks/to-do/<id>/<id>.md` (its Wave 4 runs `/sc:reflect --mode pre` itself), and the user then runs `/sc:implement <pkg>/<id>.md`.

`sc:implement` only gets per-task QA when its source has enumerable tasks; a design spec is prose and would collapse to one task, so `sc:workflow` sits between the spec and `sc:implement`.

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
  Phase B — /sc:workflow on the spec
            (produces a phased tasklist package with per-task acceptance criteria)
  Phase C — review the pre-review /sc:workflow already ran (/sc:reflect --mode pre)
            (sanity-checks the plan/tasklist before execution; flags
            scope drift, weak verification criteria, missing rollback)
  Phase D — User-driven execution
            (the skill does NOT auto-execute; you run
            /sc:implement <pkg>/<id>.md)
  Phase E — /sc:reflect --mode post
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
- `--format spec`: not `code` (we're not implementing yet) and not `diagram` (we want text that `sc:workflow` can consume).
- `--output <output_dir>/remediation-spec.md`: keeps the artifact next to the review for traceability.

On `/sc:design` completion:

- Capture the spec path.
- Surface the spec path to the user with a one-line summary.
- Proceed to Phase B unless the user says stop.

## Phase B — `sc:workflow`

First build the workflow source `<output_dir>/remediation-workflow-source.md` (rewritten from scratch on every pass): a copy of `<output_dir>/remediation-spec.md`, plus a `## References` section pointing at `REVIEW.md` and the cited Critical/High files, plus — only when `<output_dir>/remediation-review-notes.md` exists — a `## Review Feedback` section with its contents. Flatten list syntax in the copy: rewrite every checkbox (`- [ ]`) or numbered-list line as a plain `- ` bullet or prose sentence, **keeping its full text — never delete a line** (a deleted task would also escape the workflow's coverage check, which only sees the snapshot). The workflow gate rejects list lines in the generated tasklist. Then invoke `Skill sc:workflow-protocol` on `<output_dir>/remediation-workflow-source.md` (not on the bare spec) with `--depth standard --handoff none` (never `--handoff implement`; execution is user-initiated). Never pass `--output` (retired). Read `.dev/tasks/to-do/<id>/return-contract.yaml`: `status: success` → resolve the absolute tasklist path (package dir + package-relative `plan_path`) and record it as `plan_path`, and keep `reflect_status` / `reflect_report_path`; otherwise surface the STOP code and do not retry automatically. Surface the tasklist path with a one-line summary, and proceed to Phase C unless the user says stop.

## Phase C — pre-execution review

`sc:workflow` Wave 4 already ran `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (advisory, read-only). Surface `reflect_status` and `reflect_report_path` from its return contract and handle the outcomes below. Never call `/sc:reflect --mode pre` a second time. `reflect_status: skipped|failed` → say so and fall back to the `self-review` agent on the tasklist. On a refactor request, append the concerns to `<output_dir>/remediation-review-notes.md` (append-only; Phase B rebuilds `remediation-workflow-source.md` from the spec plus these notes, so they are never lost) and re-run Phase B — this creates a **new** package (workflow never edits or reuses one; the tasklist is never edited from findings); same 2-cycle cap.

The pre-execution review is a **sanity check**: is the plan well-formed enough to execute? The skill expects it to address:

- Are the acceptance criteria of each plan task strong enough to detect failure?
- Are there obvious scope-drift risks (tasks that have grown beyond what the review findings warrant)?
- Is there a rollback / abort path documented?
- Are dependencies between tasks explicit?

On pre-execution review completion:

- If it reports **no significant concerns**: surface that, then ask the user "Proceed to Phase D (execute) or refactor the tasklist first?"
- If it reports **concerns**: surface them, and ask "Refactor the tasklist to address these, or override and proceed?"
- If the user chooses to refactor: record the concerns and re-run Phase B as described above, then re-run Phase C. Cap at 2 refactor cycles to avoid infinite loops.

## Phase D — Execution (user-driven)

The skill **does not auto-execute** the tasklist. It surfaces the tasklist path and the recommended execution command:

```text
Plan/tasklist validated. Ready to execute.

  Run: /sc:implement <pkg>/<id>.md

The skill will wait. When execution completes, reply 'done' or
'execution complete' and I'll run the final validation gate.
```

Rationale: execution can be long and may want to be split across sessions; forcing the user to confirm gives them control. Also, the user may want to spot-check the tasklist before running it.

After the user signals execution is complete, proceed to Phase E. If the user closes the session here, the skill returns the structured output contract with `remediation_status: in_progress`.

## Phase E — post-execution validation

The skill invokes `/sc:reflect --mode post --spec <output_dir>/remediation-spec.md --tasklist <pkg-now>/<id>.md --task-log <pkg-now>/progress.md --diff <baseline_ref>` (record `baseline_ref = git rev-parse HEAD` at Phase D; `<pkg-now>` is `.dev/tasks/to-do/<id>` or, once `/sc:implement` archived the package after its final review, `.dev/tasks/done/<id>`; resolve by id).

This is the **final gate before commit**.

The post-execution review checks:

- Were all tasklist tasks completed?
- Do the completed artifacts satisfy each task's acceptance criteria?
- Are there any new defects introduced during execution?
- Is the change minimal (no scope creep beyond what the original review findings required)?

On post-execution review completion:

- If it **passes**: surface that, and recommend the user commit. Do not auto-commit. The recommended commit message format is `fix(<scope>): remediate findings from <review-id>` with a reference to the review URL in the body.
- If it **fails**: surface the issues and ask the user how to proceed (re-run Phase D? Open a new review? Bail?). Do not recommend commit until it passes.

## Resumability

If the user closes the session mid-chain, the skill writes the chain's state to `<output_dir>/remediation-state.json`:

```json
{
  "phase": "<A|B|C|D|E>",
  "last_completed": "<phase>",
  "artifacts": {
    "review_path": "...",
    "spec_path": "...",
    "plan_path": "... (absolute .dev/tasks/to-do/<id>/<id>.md)",
    "reflect_pre_result": "...",
    "reflect_post_result": "..."
  },
  "started_at": "<iso>",
  "last_updated_at": "<iso>"
}
```

When the user re-invokes the skill with `--resume <output_dir>`, the chain picks up at the recorded phase. A state file written with the older key names ignores `task_file_path` and `task_reflect_*` and keeps `plan_path`. If the recorded phase's input is absent from the state, re-run the phase that produces it: `plan_path` (needed by Phases C, D and E) comes from Phase B, and `spec_path` (needed by Phase B) comes from Phase A, so a state with neither restarts at Phase A. If an older state has no `plan_path` and was recorded at Phase D or E, tell the user before resuming that anything already executed from its retired task file is not tracked by this chain.

## Anti-patterns to avoid

- **Don't auto-execute Phase D**. The most common failure mode of agentic remediation chains is silent execution of half-baked plans. The pause-for-user-confirmation pattern is intentional friction.
- **Don't skip Phase C even if findings are "obviously small"**. The pre-execution review is cheap and catches scope-drift early.
- **Don't proceed to commit if Phase E fails**. The whole point of having a final post-execution gate is to refuse to commit broken work.
- **Don't bundle the offer into an AskUserQuestion**. The user might want to start at Phase B with an existing spec, skip Phase C, etc. A free-form text offer preserves that flexibility.
- **Don't badger the user**. If they say no, that's the final answer for this review.
