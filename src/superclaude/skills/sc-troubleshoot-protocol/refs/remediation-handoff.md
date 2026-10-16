# Tier 3 Remediation Handoff (Wave 6)

Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report. Drives the offer + remediation chain (plan route by default, MDTM route with `--depth deep`). This `success AND --fix` load precondition is reconciled with the Pipeline Hardening Closure verdict below: within this load path, a `blocked`/`advisory` hardening verdict prevents a plain-`success` handoff (see **Pipeline hardening verdict gating**).

## Route selection

The route is keyed on the `--depth` the user **requested**, never on the tier reached (an auto-escalation to Tier 2 does not change the route). `--depth quick` with `--fix` is a Wave 0 STOP, so only two routes exist:

| Flags | Route | Builder | User-run executor |
|-------|-------|---------|-------------------|
| `--fix` (depth `standard`, the default) | **Plan route** | `sc:workflow-protocol` → `plan.md` | `/sc:implement <plan.md>` |
| `--fix --depth deep` | **MDTM route** | `task-builder` → MDTM task file | `/task <task-file>` |

Without `--fix`, neither route runs.

## Pipeline hardening verdict gating

When the Pipeline Hardening Closure mode ran (`pipeline_hardening_applicable=true`), this handoff carries its verdict and reconciles success-gating with the §5.4 downstream no-override rule (governed by `refs/hardening-output-contract.md`):

- **Load precondition unchanged.** The handoff still loads only when `--fix` is set AND Wave 5 produced a `success` (not `partial`) report. The hardening verdict does not relax that precondition; it constrains how a loaded handoff renders.
- **`blocked`/`advisory` prevents a plain-`success` handoff.** Within the `success AND --fix` load path, a `pipeline_hardening_verdict` of `blocked` or `advisory` renders the downstream result as `success_with_hardening_blocker` or `success_with_hardening_advisory` respectively — never plain `success`.
- **One-way latch carried downstream.** `waiver_status=latched` forces `pipeline_hardening_verdict ∈ {blocked, advisory}` and is carried into the `BUILD_REQUEST` (MDTM route Phase A) or the `## Pipeline Hardening` block of the workflow source (plan route Phase A). A downstream `task-builder` / `sc:workflow` / `sc:implement` / `sc:reflect` / `sc:adversarial` / report-rendering stage may append findings but may **not** convert `blocked`/`advisory` into `pass`/`success` (spec §5.4 L411). The four-token verdict (`pass | blocked | advisory | not_applicable`) is preserved end-to-end; `advisory` is never dropped.

## The user offer

After Wave 5, before invoking the route's builder, the skill surfaces this prompt verbatim (substituting bracketed fields and keeping only the step list for the selected route). The user answers yes/no.

```text
Tier 3 remediation chain is available for this fix.   Route: <plan | mdtm>

Plan route (--fix) — the chain will:
  1. Build a phased plan.md from the report via /sc:workflow (no code edits yet)
  2. Run `/sc:reflect --mode pre --spec <REPORT.md> --tasklist <plan.md>` against the plan
  3. Stop and surface the literal `/sc:implement <plan.md>` command for you to run
  4. After you run /sc:implement and report back, run `/sc:reflect --mode post`
     as the final gate before you commit

MDTM route (--fix --depth deep) — the chain will:
  1. Build an MDTM task file from the report (no code edits yet)
  2. Run `/sc:reflect --type task --analyze` against the task file
  3. Stop and surface the literal `/task <path>` command for you to run
  4. After you run /task and report back, run `/sc:reflect --type task --validate`
     as the final gate before you commit

Fix to be applied:
  <one-paragraph summary from REPORT.md "Proposed Fix" section>

Files that will change:
  <bullet list of files from REPORT.md>

Expected task complexity (MDTM route only): <generic | complex>

Pipeline hardening verdict: <pass | blocked | advisory | not_applicable>   (waiver_status: <none | latched>)
  When blocked/advisory: closure is NOT clean — this hands off as success_with_hardening_<blocker|advisory>;
  a downstream stage may append findings but may NOT upgrade it to success.

Proceed with <sc:workflow | task-builder>?  [yes / no]
```

## Decision matrix

| User response | Action |
|---------------|--------|
| `yes` (or affirmative variant: "y", "go", "proceed") | Invoke the route's builder (Plan route Phase A, or MDTM route Phase A) |
| `no` (or any non-affirmative) | Record `remediation_accepted=false`; the report is the final deliverable; emit "Tier 3 declined — report at <path>" |
| Anything ambiguous | Treat as "no" — do not infer consent |

---

## Plan route (`--fix`) — Phases A–D

### Phase A — Build the plan

1. Write `<output-dir>/remediation-source.md` (the `sc:workflow` source), built from the report:

   ```text
   # Remediation: <REPORT.md title>

   Goal: Apply the fix described in <abs-path-to-REPORT.md>

   ## Summary
   <copy the REPORT.md "Summary" section, flattened — see the flatten rule below>

   ## Files
   <list of files from REPORT.md "Proposed Fix" section, as plain `- ` bullets>

   ## Acceptance
   - <test to verify from REPORT.md, restated as a plain bullet — no checkboxes, no numbered lines>
   - The change is limited to the files listed under Files
   - No new lint or type errors introduced

   ## References
   - REPORT.md: <abs-path>
   - Audit log: <abs-path>
   - Hypothesis card (chosen): <abs-path>

   ## Pipeline Hardening
   pipeline_hardening_verdict: <pass | blocked | advisory | not_applicable>
   waiver_status: <none | latched>
   (Downstream stages must not re-green a blocked/advisory closure — spec §5.4 L411.)
   ```

   **Flatten rule.** Anything copied from REPORT.md (the Summary, file lists, test names) must first be flattened: rewrite every numbered line (`1.`, `1)`) and every checkbox line (`- [ ]`, `- [x]`, `* [ ]`) as a plain `- ` bullet or a prose sentence. A single leftover list line makes the `sc:workflow` gate fail with `E-GATE` (or makes `sc:implement` enumerate it as a task).

2. Invoke `Skill sc:workflow-protocol` with `<output-dir>/remediation-source.md --depth standard --handoff none`. **Never** pass `--handoff implement` — that auto-invokes `sc:implement`, which edits product code, and the execution gate (Phase C) is always user-initiated. Do not pass `--output` (it must stay under `.dev/workflow/`; the default is correct).
3. Read the workflow `return-contract.yaml`. `status: success` → record `plan_path` in the audit log. Any other status → surface it, record `plan_path=null`, do not retry automatically.
4. Verify `plan.md` still carries the `pipeline_hardening_verdict` / `waiver_status` lines from the source. If either is missing, append the `## Pipeline Hardening` block to `plan.md` verbatim. (`sc:workflow` has no hardening field of its own, so troubleshoot owns this carry.)

### Phase B — Pre-execution review

`sc:workflow` runs only a mechanical schema gate — no semantic review — so this phase is the only check that the plan covers the diagnosis.

Invoke `/sc:reflect --mode pre --spec <REPORT.md> --tasklist <plan.md>` via `Skill` (if `sc:reflect` is available — otherwise fall back to spawning the `self-review` agent on `plan.md`).

Outcomes are handled exactly as in the MDTM route Phase B (OK / recommends refactor / blocker). On `refactor`, append the recommendation to `remediation-source.md` and re-run Phase A.

### Phase C — Execution gate (always user-initiated)

The skill **never** auto-executes the plan. It surfaces the path and the literal command:

```text
Plan ready: <abs-path>

To execute, run:
  /sc:implement <abs-path>

The skill stops here. After /sc:implement completes, optionally re-invoke /sc:troubleshoot
or /sc:reflect --mode post --spec <REPORT.md> --tasklist <abs-path> --diff <ref-or-patch> for the post-execution gate.
```

This is non-negotiable. `/sc:implement` edits product code; running it on the user's behalf bypasses their final review of what is about to change.

### Phase D — Post-execution validation (optional, user-triggered)

Only fires if the user comes back and explicitly invokes the validation step. The skill itself does not poll and does not auto-resume after `/sc:implement`.

```text
/sc:reflect --mode post --spec <REPORT.md> --tasklist <plan.md> --diff <ref-or-patch>
```

`OK` → emit "Validation passed — safe to commit." Issues → surface them; do not auto-fix. The user decides whether to revert, patch, or accept.

---

## MDTM route (`--fix --depth deep`) — Phases A–D

### Phase A — Build the task file

Invoke the `task-builder` skill via `Skill`. The `BUILD_REQUEST` is constructed from the report:

```text
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
  PIPELINE_HARDENING:
    pipeline_hardening_verdict: <pass | blocked | advisory | not_applicable>
    waiver_status: <none | latched>
    # Carried so the downstream task-builder/reflect/adversarial stage receives the latched
    # verdict and MUST NOT re-green a blocked/advisory closure to pass/success (spec §5.4 L411).
```

**Template selection**:

- Use `complex` (template 02) if any of:
  - More than 3 files in WHERE
  - REPORT.md "Risk + Rollback" rates likelihood-of-regression as `high`
  - The fix involves a schema change, a migration, or a public API change
- Otherwise use `generic` (template 01).

`task-builder` returns a task file path. Record it in the audit log as `task_file_path`.

### Phase B — Pre-execution review

Invoke `/sc:reflect --type task --analyze <task-file>` via `Skill` (if `sc:reflect` is available — otherwise fall back to spawning the `self-review` agent on the task file).

Reflect can return:

- **OK** — proceed to Phase C.
- **Recommends refactor** — surface the recommendation; ask the user "refactor the task before running, or proceed as-is? [refactor / proceed]". On `refactor`, re-invoke `task-builder` with the recommendation; on `proceed`, continue.
- **Blocker** — STOP. Surface the blocker. Do not advance to Phase C until the user resolves it.

### Phase C — Execution gate (always user-initiated)

The skill **never** auto-executes the task. It surfaces the path and the literal command:

```text
Task file ready: <abs-path>

To execute, run:
  /task <abs-path>

The skill stops here. After /task completes, optionally re-invoke /sc:troubleshoot
or /sc:reflect --type task --validate <abs-path> for the post-execution gate.
```

This is non-negotiable. The reason is the F1 execution loop in `/task` is the user's responsibility — running it on the user's behalf bypasses their final review of what's about to change.

### Phase D — Post-execution validation (optional, user-triggered)

Only fires if the user comes back and explicitly invokes the validation step. The skill itself does not poll, does not auto-resume after `/task`.

The user runs (or the skill is re-invoked with a flag like `--validate-task <path>`):

```text
/sc:reflect --type task --validate <task-file>
```

If `--validate` returns OK: emit "Validation passed — safe to commit. Suggested message: `<from task file's commit_message section>`".

If `--validate` returns issues: surface the issues; do not auto-fix. The user decides whether to revert, patch, or accept.

---

## Why this is the only safe handoff

- **No silent application of code changes.** Every step has a user-visible gate.
- **The plan or task file is reviewable as a diff target before any code moves.** That is the entire point of the intermediate artifact.
- **`/sc:reflect` pre-mode catches "this plan/task is wrong" before execution.** Post-mode catches "this ran but did the wrong thing" before commit.
- **The user runs `/sc:implement` or `/task`**, not the skill. This preserves the contract that all destructive operations are user-initiated.

## Failure modes

| Failure | Behaviour |
|---------|-----------|
| `task-builder` returns an error (MDTM route) | Surface the error; record `remediation_accepted=true` but `task_file_path=null`; do not retry automatically |
| `sc:workflow-protocol` returns non-`success` or STOPs (plan route) | Surface the code (e.g. `E-GATE`); record `remediation_accepted=true`, `plan_path=null`; do not retry automatically |
| `sc:workflow-protocol` unavailable (plan route) | Surface the fix proposal path; recommend manual planning or re-running with `--depth deep`; don't fail the whole skill |
| Builder returns a file but `/sc:reflect` pre-mode flags a blocker | Stop at Phase B; surface blocker; offer to re-build with the blocker addressed |
| User responds `yes` then `no` on the Phase B "refactor or proceed" prompt | Treat as decline of the refactor path → proceed to Phase C as-is |
| User does not respond within a reasonable time | Treat as decline; emit a soft note that Tier 3 can be re-invoked later by re-running `/sc:troubleshoot --fix` |
