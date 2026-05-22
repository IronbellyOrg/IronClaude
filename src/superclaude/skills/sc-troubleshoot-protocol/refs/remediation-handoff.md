# Tier 3 Remediation Handoff (Wave 6)

Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report. Drives the offer + task-builder chain.

## The user offer

After Wave 5, before invoking `task-builder`, the skill surfaces this prompt verbatim (substituting bracketed fields). The user answers yes/no.

```
Tier 3 remediation chain is available for this fix.

The chain will:
  1. Build an MDTM task file from the report (no code edits yet)
  2. Run `/sc:reflect --type task --analyze` against the task file
  3. Stop and surface the literal `/task <path>` command for you to run
  4. After you run /task and report back, run `/sc:reflect --type task --validate`
     as the final gate before you commit

Fix to be applied:
  <one-paragraph summary from REPORT.md "Proposed Fix" section>

Files that will change:
  <bullet list of files from REPORT.md>

Expected task complexity: <generic | complex>

Proceed with task-builder?  [yes / no]
```

## Decision matrix

| User response | Action |
|---------------|--------|
| `yes` (or affirmative variant: "y", "go", "proceed") | Invoke `task-builder` (Phase A below) |
| `no` (or any non-affirmative) | Record `remediation_accepted=false`; the report is the final deliverable; emit "Tier 3 declined — report at <path>" |
| Anything ambiguous | Treat as "no" — do not infer consent |

## Phase A — Build the task file

Invoke the `task-builder` skill via `Skill`. The `BUILD_REQUEST` is constructed from the report:

```
BUILD_REQUEST:
  TEMPLATE: <generic | complex>
  GOAL: Apply the fix described in <abs-path-to-REPORT.md>
  WHY: <copy the REPORT.md "Summary" section verbatim>
  WHERE: <list of files from REPORT.md "Proposed Fix" section>
  ACCEPTANCE_CRITERIA:
    - <test to verify from REPORT.md, restated as a checkbox criterion>
    - The change is limited to the files listed in WHERE
    - No new lint or type errors introduced
  REFERENCES:
    - REPORT.md: <abs-path>
    - Audit log: <abs-path>
    - Hypothesis card (chosen): <abs-path>
```

**Template selection**:

- Use `complex` (template 02) if any of:
  - More than 3 files in WHERE
  - REPORT.md "Risk + Rollback" rates likelihood-of-regression as `high`
  - The fix involves a schema change, a migration, or a public API change
- Otherwise use `generic` (template 01).

`task-builder` returns a task file path. Record it in the audit log as `task_file_path`.

## Phase B — Pre-execution review

Invoke `/sc:reflect --type task --analyze <task-file>` via `Skill` (if `sc:reflect` is available — otherwise fall back to spawning the `self-review` agent on the task file).

Reflect can return:

- **OK** — proceed to Phase C.
- **Recommends refactor** — surface the recommendation; ask the user "refactor the task before running, or proceed as-is? [refactor / proceed]". On `refactor`, re-invoke `task-builder` with the recommendation; on `proceed`, continue.
- **Blocker** — STOP. Surface the blocker. Do not advance to Phase C until the user resolves it.

## Phase C — Execution gate (always user-initiated)

The skill **never** auto-executes the task. It surfaces the path and the literal command:

```
Task file ready: <abs-path>

To execute, run:
  /task <abs-path>

The skill stops here. After /task completes, optionally re-invoke /sc:troubleshoot
or /sc:reflect --type task --validate <abs-path> for the post-execution gate.
```

This is non-negotiable. The reason is the F1 execution loop in `/task` is the user's responsibility — running it on the user's behalf bypasses their final review of what's about to change.

## Phase D — Post-execution validation (optional, user-triggered)

Only fires if the user comes back and explicitly invokes the validation step. The skill itself does not poll, does not auto-resume after `/task`.

The user runs (or the skill is re-invoked with a flag like `--validate-task <path>`):

```
/sc:reflect --type task --validate <task-file>
```

If `--validate` returns OK: emit "Validation passed — safe to commit. Suggested message: `<from task file's commit_message section>`".

If `--validate` returns issues: surface the issues; do not auto-fix. The user decides whether to revert, patch, or accept.

## Why this is the only safe handoff

- **No silent application of code changes.** Every step has a user-visible gate.
- **The task file is reviewable as a diff target before any code moves.** That is the entire point of the MDTM intermediate.
- **`/sc:reflect --analyze` catches "this task is wrong" before execution.** `/sc:reflect --validate` catches "this task ran but did the wrong thing" before commit.
- **The user runs `/task`**, not the skill. This preserves the contract that all destructive operations are user-initiated.

## Failure modes

| Failure | Behaviour |
|---------|-----------|
| `task-builder` returns an error | Surface the error; record `remediation_accepted=true` but `task_file_path=null`; do not retry automatically |
| `task-builder` returns a task file but `/sc:reflect --analyze` flags a blocker | Stop at Phase B; surface blocker; offer to re-build with the blocker addressed |
| User responds `yes` then `no` on the Phase B "refactor or proceed" prompt | Treat as decline of the refactor path → proceed to Phase C as-is |
| User does not respond within a reasonable time | Treat as decline; emit a soft note that Tier 3 can be re-invoked later by re-running `/sc:troubleshoot --fix` |
