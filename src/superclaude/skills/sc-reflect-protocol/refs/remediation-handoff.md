# Wave 6 Remediation Handoff — Plan Route (default) and task-builder Route (`--depth deep`)

Loaded by Wave 6 only when `--remediate` is set AND Wave 5 produced a deviation register with at least one item whose class warrants a remediation (see default-remediation table below). Reflect itself never fixes code; this ref documents the opt-in handoff. The default chain builds a `plan.md` through `sc:workflow` for the user to run with `/sc:implement`; the `task-builder` → `/task` chain runs only with `--depth deep`.

Source for the MDTM route: `task-builder/SKILL.md` lines 785-985 (M1-frozen BUILD_REQUEST schema, plus the API-001-M2 `EXECUTION_CONTEXT_REQUIREMENTS` extension). Merged-requirements driver: §7 row "task-builder (skill, not agent) — Wave 6", §8 cross-skill table, §10.3 Drift, §10.4 Regression.

## Route selection

The route is keyed on the `--depth` the user **requested**, never on the tier reached (an auto-escalation to Tier 2 does not change the route). `--remediate` is the gate on reflect, the analogue of `--fix` on troubleshoot.

| Flags | Route | Builder | User-run executor |
|-------|-------|---------|-------------------|
| no `--remediate` (any depth, including `--depth deep` alone) | **None** | none | none |
| `--remediate` (depth `standard`, the default, or `quick`) | **Plan route** | `sc:workflow-protocol` → `plan.md` | `/sc:implement <plan.md>` |
| `--remediate --depth deep` | **MDTM route** | `task-builder` → MDTM task file | `/task <task-file>` |
| headless `claude --print` + `--remediate` (reflect wrapper, `superclaude reflect run --fix`), depth `standard`/`quick` | **Plan route** (same depth rule) | `sc:workflow-protocol` → `plan.md` | the wrapper auto-runs `/sc:implement <remediation_plan_path>` |
| headless `claude --print` + `--remediate --depth deep` | **MDTM route** | `task-builder` | the wrapper auto-runs `/task <remediation_task_path>` |

- `--depth deep` alone does **not** trigger remediation: Wave 6 still requires `--remediate`.
- `--depth quick` with `--remediate` takes the plan route; there is no new STOP for it.
- The skill never runs `/sc:implement` or `/task`, and never passes `--handoff implement` to `sc:workflow` (that would auto-run `sc:implement`). The route-specific phases below stop at a user-run execution gate.
- Headless runs follow the same depth-keyed rule; the only differences are auto-accept and no Phase B/C user gates. See "Headless auto-accept under `--print` (FR-9)".
- **Sanctioned nested call.** Plan-route Phase B invokes `/sc:reflect --mode pre` from inside Wave 6. This is the one sanctioned exception to the SKILL.md Will Not rule against reflecting on reflect's own intermediate output: it audits the authored `plan.md` against the report, runs as a fresh Skill call without `--remediate`, and writes to its own `--output`.

## Plan route (`--remediate`) — Phases A–D

`sc:workflow` and `sc:implement` have no `BUILD_REQUEST`-style field, so any reflect state that must survive (Regression items, Drift decisions, `needs_human_decision`, grounding gaps) travels as a plain section in the source file handed to `sc:workflow`. The `sc:workflow` gate forbids checkbox (`- [ ]`) and numbered-list lines anywhere in `plan.md` (`sc:implement` would enumerate them as tasks), so the source uses plain dash bullets and prose only.

### Phase A — Build the plan

1. Surface the opt-in prompt below (plan-route steps only). `yes` proceeds; anything else, including an ambiguous answer, is `no`.
2. Write `<output-dir>/remediation-source.md` (the `sc:workflow` source), built from the report and the deviation register:

   ```text
   # Remediation: <REPORT.md title>

   Goal: Remediate the Regression-class and Drift-class deviations in <abs-path-to-report.md>

   ## Summary
   <REPORT.md summary, verbatim>

   ## Deviations To Remediate
   - Regression <D-id>: <title> - <file:line> - <one-line required repair>
   - Drift <D-id>: <title> - <file:line> - decision: <backfill spec | revert>

   ## Files
   - <files from the deviation register>

   ## Acceptance
   - <previously failing test or check per Regression item, as a plain bullet>
   - The change is limited to the files listed under Files
   - No new lint or type errors introduced

   ## References
   - Report: <abs-path>
   - Deviation register: <abs-path>
   - Grounding gaps: <abs-path>

   ## Reflect Verdict State
   needs_human_decision: <true | false>
   regression_count: <n>
   drift_count: <n>
   grounding_gaps: <none | see References>
   (Downstream stages may append findings but must not downgrade a Regression item or clear needs_human_decision.)
   ```

   Drift items need a per-item backfill-or-revert decision; when undecided, say in prose that deciding it is the first change the plan must make (no numbered list).

   **Flatten list syntax.** Anything copied verbatim into this source (the REPORT.md summary, register rows, test names) must first be flattened: rewrite every numbered line (`1.`, `1)`) and every checkbox line (`- [ ]`, `- [x]`, `* [ ]`) as a plain `- ` bullet or a prose sentence. A single leftover list line makes the `sc:workflow` gate fail with `E-GATE` (or makes `sc:implement` enumerate it as a task).
3. Invoke `Skill sc:workflow-protocol` with `<output-dir>/remediation-source.md --depth standard --handoff none`. Never pass `--handoff implement`: that auto-invokes `sc:implement`, which edits product code, and the execution gate (Phase C) is always user-initiated. Do not pass `--output` (it must stay under `.dev/workflow/`; the default is correct).
4. Read the workflow `return-contract.yaml`. `status: success` → record `plan_path` in `audit.log` and emit it as the `remediation_plan_path` contract field (§9.1, 1.8.0). Any other status (for example `E-GATE`) → surface it, record `plan_path=null`, do not retry automatically.
5. Verify `plan.md` still carries the `## Reflect Verdict State` lines (`needs_human_decision`, `regression_count`). If missing, append the section to `plan.md` verbatim, keeping it free of checkbox and numbered-list lines. (`sc:workflow` has no such field of its own, so reflect owns this carry.)

### Phase B — Pre-execution review

`sc:workflow` runs only a mechanical schema gate — no semantic review and never `sc:reflect` — so this phase is the only semantic check that the plan covers the deviations.

Invoke `/sc:reflect --mode pre --spec <report.md> --tasklist <plan.md> --output <output-dir>/plan-review` via `Skill` (fall back to spawning the `self-review` agent on `plan.md` if `sc:reflect` is unavailable).

- Make this a fresh `Skill` call after the current run's Wave 5 report is final.
- The nested call must NOT carry `--remediate` (that would recurse into Wave 6) and uses its own `--output`.
- Coverage caveat: reflect reads the tasklist as a free-form file, but exact-ID matching (`R-`, `REQ-`, `SPEC-`, `T-` tokens) will not fire on `## Task N:` headings, so spec rows match through the Pass-2 containment rule only. Treat `coverage_undefined` as a surfaced warning, not a silent pass. Whether the Step 1B.1 zero-task guard counts `## Task N:` headings as tasks is unverified; if it STOPs `empty_input`, surface that and let the user proceed as-is or use the `self-review` agent.
- Outcomes: **OK** → proceed to Phase C. **Recommends refactor** → surface it and ask "refactor the plan before running, or proceed as-is? [refactor / proceed]"; on `refactor`, append the recommendation to `remediation-source.md` and re-run Phase A. **Blocker** → STOP, surface it, and do not advance to Phase C until the user resolves it.

### Phase C — Execution gate (always user-initiated)

Record `baseline_ref = git rev-parse HEAD` in `audit.log`, then surface the path and the literal commands:

```text
Plan ready: <abs-path>

To execute, run:
  /sc:implement <abs-path>

The skill stops here. After /sc:implement completes, run the post-execution gate:
  /sc:reflect --mode post --spec <report.md> --tasklist <abs-path> --diff <baseline_ref> --task-log .dev/implement/<slug>/progress.md
```

A single ref (not `A..B`) diffs against the working tree, so `--diff <baseline_ref>` captures uncommitted `/sc:implement` edits to tracked files; `git diff` omits untracked files, so `--task-log` (the `sc:implement` ledger) lets reflect see files the run created. This is non-negotiable: the skill never runs `/sc:implement` — running it on the user's behalf bypasses their final review of what is about to change.

### Phase D — Post-execution validation (optional, user-triggered)

Only fires if the user comes back and explicitly invokes the gate. The skill itself does not poll and does not auto-resume after `/sc:implement`. The surfaced command carries no `--remediate` (no loop).

`OK` → emit "Validation passed — safe to commit." Issues → surface them; do not auto-fix. The user decides whether to revert, patch, or accept.

---

## MDTM route (`--remediate --depth deep`) — BUILD_REQUEST template

Reflect constructs this prompt and spawns `rf-task-builder` via Skill invocation. Field names are taken verbatim from `task-builder/SKILL.md:785-985`.

```text
Agent:
  subagent_type: "rf-task-builder"
  mode: "bypassPermissions"
  prompt: |
    BUILD_REQUEST:
    ==============
    GOAL: Remediate <N> Regression-class and <M> Drift-class
      deviations surfaced by sc-reflect run <run_id> against
      tasklist <tasklist_path>.

    WHY: Wave 5 evidence-validated deviation register
      (<deviation_register_path>) classifies <N> Regression items
      (unconditional Tier 3 per §10.4) and <M> Drift items the user
      authorized for repair via --remediate. Grounding gaps from
      <grounding_gaps_path> are listed as known limitations.

    TASK_ID_PREFIX: TASK-RF

    TEMPLATE: 02
      # Reflect-driven remediation almost always lands on Template 02
      # (complex) because Regression repair requires discovery + build
      # + test + review phases. Template 01 is permitted ONLY when the
      # register holds a single Drift item with ≤1 file scope.

    QA_GATE_REQUIREMENTS: PER_PHASE
      # Regression repair MUST include rf-qa / rf-qa-qualitative gates
      # after the repair phase (matches §10.4 unconditional-Tier-3 +
      # rule-3-escalation posture). For Drift-only remediation, FINAL_ONLY
      # is acceptable.

    VALIDATION_REQUIREMENTS: |
      Standard project validation: lint, type-check, build, and
      previously-passing tests must pass. For each Regression item,
      verify the previously-failing test now passes AND no new test
      failures introduced.

    TESTING_REQUIREMENTS: UNIT
      # Default for Regression repair. Escalate to UNIT + INTEGRATION
      # when the deviation register tags an item as touching public API
      # surface or cross-module behavior.

    EXECUTION_CONTEXT_REQUIREMENTS: AUTO
      # Reflect leaves heuristic emission to task-builder. REQUIRED only
      # when the deviation register spans ≥3 distinct source areas.

    DOCUMENTATION STALENESS WARNINGS:
      None found — reflect's Wave 5 evidence-validator already
      re-Read every cited file:line. Inherited [CODE-VERIFIED] tags
      from the deviation register apply.

    RESEARCH DIR: <output>/reflect/<run_id>/
      # Reflect's own artifacts substitute for the standard
      # researcher dir. Read:
      # - report.md            (Wave 5 synthesized report)
      # - deviation-register.md (per-item classification)
      # - grounding-gaps.md    (known unverified claims)
      # - hypothesis-cards/    (root-cause-analyst cards)
      # - adversarial/merged.md (T2 only — reviewer verdict)

    HANDOFF_MEMORY_KEY: reflect/handoff-{slug}-{timestamp}
      # FR-3 warm-start bridge. When present, task-builder should
      # `read_memory` this key to recover reflect's in-flight rubric
      # scores + deviation set + evidence packet + reviewer verdicts
      # instead of re-deriving them. Omitted / null when no Tier 3
      # handoff was written (handoff_persist_failed or no --remediate).

    QUALITY GATE RESULTS:
      Evidence-validator gate (Wave 5) PASSED with
      <validator_pass_rate>% citation re-Read pass rate.
      No separate analyst-completeness-report.md or
      qa-research-gate-report.md exist for reflect runs.

    OPEN QUESTIONS:
      <copied verbatim from report.md "Open Questions" section, or
      "None" when empty>

    REMAINING GAPS:
      <copied verbatim from grounding-gaps.md, or "None">
```

## Opt-in prompt

Wave 6 presents this verbatim **before** invoking the route's builder (no auto-execute — §17 Will Not), substituting bracketed fields and keeping only the step list for the selected route. The user answers yes/no; ambiguous responses are treated as "no" (matches sc-troubleshoot remediation-handoff posture).

```text
Tier 3 remediation chain is available.   Route: <plan | mdtm>

Plan route (--remediate) — the chain will:
  1. Build a phased plan.md from this report via /sc:workflow (no code edits yet)
  2. Run `/sc:reflect --mode pre --spec <report.md> --tasklist <plan.md>` against the plan
  3. Stop and show the literal `/sc:implement <plan.md>` command for you to run
  4. After you run it and report back, run `/sc:reflect --mode post` as the final gate

MDTM route (--remediate --depth deep) — the chain will:
  1. Build an MDTM task file from the report (no code edits yet)
  2. Run `/sc:reflect --type task --analyze` against it
  3. Stop and show the literal `/task <path>` command for you to run
  4. After you run /task, run `/sc:reflect --type task --validate` as the final gate

Reflect identified <N> Regression-class and <M> Drift-class deviation(s) eligible for remediation.

Regression items (will be primary objective):
  <bullet list from deviation-register.md, severity-sorted>

Drift items (authorize-or-revert per item):
  <bullet list from deviation-register.md>

needs_human_decision: <true | false>

Proceed with <sc:workflow | task-builder>?  [yes / no]

If no: the report at <report_path> is the final deliverable.
```

**State carried per route.** Step 6.0 (handoff memory write) and the `remediation_task_path` emission are **MDTM-route only**: `task-builder` can `read_memory` a handoff key, `sc:workflow` cannot. On the plan route the state travels in the `## Reflect Verdict State` section of `remediation-source.md`, so `handoff_memory_key: null` and `remediation_task_path: null`; the plan route records `remediation_route: plan` in `audit.log` and emits the built plan as the `remediation_plan_path` contract field (§9.1, 1.8.0; `null` when no plan was built). The wrapper's auto-fix loop is the only consumer of either field.

## Headless auto-accept under `--print` (FR-9)

**Same route rule, no exception.** The headless path follows the depth-keyed route table: `superclaude reflect run --fix` (`src/superclaude/cli/reflect/runner.py`) passes `--depth <d> --remediate`. With depth `standard`/`quick` reflect authors a plan and emits `remediation_plan_path`; the wrapper's auto-fix loop runs `/sc:implement <remediation_plan_path>`. With `--depth deep` reflect authors the MDTM and emits `remediation_task_path`; the loop runs `/task <remediation_task_path>`. The loop reads whichever field is non-null (the MDTM pointer wins if both are set) and fails closed on a non-zero apply rc.

The opt-in prompt above is for **interactive** runs. When reflect runs **non-interactively**
(the reflect-wrapper launches it as `claude --print`, with **no TTY** — `--print` mode is the
headless signal; this is distinct from the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker,
which is the nested-gate suppressor, not the headless signal), `--remediate` MUST **auto-accept and
author** the corrective artifact **without presenting the yes/no prompt** — but ONLY for **AUTO-FIXABLE**
registers (solely §10.3 Drift and/or §10.2 Necessary). The authored path is then emitted as
`remediation_plan_path` (plan route) or `remediation_task_path` (MDTM route) (§9.1) for the wrapper to auto-run.

**Headless plan route skips Phases B and C.** There is no user to gate on, and the wrapper's own re-audit after the apply (same `--base`, bounded by `--max-fix-iterations`) is the verification. Phase A (build the plan) still runs in full, including the flatten rule and the `## Reflect Verdict State` carry.

For **HUMAN-REQUIRED** registers (any §10.4 Regression, or `needs_human_decision: true` from a
non-empty `grounding-gaps.yaml`), the headless branch authors **nothing auto-runnable**: the
BUILD_REQUEST (MDTM route) or the `## Reflect Verdict State` section (plan route) carries `needs_human_decision: true` (see `HANDOFF_MEMORY_KEY` mapping below and
SKILL.md §"Will Not") to prompt human resolution, and both `remediation_task_path: null` and `remediation_plan_path: null` are emitted — so
the wrapper terminal-HALTs and never auto-applies a human-decision change
(honoring `feedback_human_decision_items_must_halt`). The §"Will Not" invariant (reflect AUTHORS but
NEVER EXECUTES `/task` or `/sc:implement`) is preserved in BOTH branches — only the AUTHORING accept gate changes under
`--print`, never the execution gate. The Authorized/Necessary-only short-circuit (below) still yields
both pointers `null`.

## Default-remediation guidance per deviation class

Drives whether Wave 6 even reaches the opt-in prompt for a given register row.

| Deviation class | Default (no flag) | With `--remediate` | Notes |
|---|---|---|---|
| §10.1 Authorized | No remediation task | No remediation task | Document only; appears in report's "Authorized changes" section |
| §10.2 Necessary | No remediation task | `--remediate-docs` may propose a spec-update task (TEMPLATE: 01, docs-only) | Default still no-op; spec update is the only remediation venue |
| §10.3 Drift | Surface "Authorize-or-revert decision required" in report | Offer Tier 3 task with **backfill-or-revert prompt** in TEMPLATE 02 phase 1 | User picks per item: (a) backfill spec to authorize, or (b) revert the drift |
| §10.4 Regression | Surface as STOP-class finding in report | **Unconditionally** offer Tier 3 task; regression repair is the primary objective | Also unconditionally forces Wave 3A T2 escalation per §5.3 rule 3 (debated by ≥2 reviewers before report ships) |

If the register contains only §10.1 + §10.2 items, Wave 6 short-circuits: no opt-in prompt, no `sc:workflow` or `task-builder` invocation, emit "No Tier 3 remediation warranted — register holds only Authorized / Necessary items."

## Field-by-field mapping from reflect contract to BUILD_REQUEST

Maps each BUILD_REQUEST field to the reflect output-contract source (§9.1).

| BUILD_REQUEST field | Reflect source |
|---|---|
| `GOAL` | Derived from `deviation_register.regression_count` + `drift_count`; references `run_id` and `tasklist_path` from return contract |
| `WHY` | Citations from `report_path`, `deviation_register_path`, `grounding_gaps_path` |
| `TASK_ID_PREFIX` | Constant `TASK-RF` |
| `TEMPLATE` | 02 by default; 01 only when register = single Drift, scope ≤1 file |
| `QA_GATE_REQUIREMENTS` | PER_PHASE when ≥1 Regression present; else FINAL_ONLY |
| `VALIDATION_REQUIREMENTS` | Composed from project CLAUDE.md baseline + per-Regression "previously-passing test" repair verification |
| `TESTING_REQUIREMENTS` | UNIT default; UNIT + INTEGRATION when register tags item as API-surface or cross-module |
| `EXECUTION_CONTEXT_REQUIREMENTS` | AUTO default; REQUIRED when register spans ≥3 distinct source areas (matches DM-001.SourceAreas heuristic) |
| `DOCUMENTATION STALENESS WARNINGS` | "None found" — evidence-validator already re-Read every citation in Wave 5 |
| `RESEARCH DIR` | `<output>/reflect/<run_id>/` substitutes for standard researcher dir; lists reflect's own artifacts |
| `HANDOFF_MEMORY_KEY` | `handoff_memory_key` (§9.1 Tier-3 block) — `reflect/handoff-{slug}-{timestamp}`; null when no Tier 3 handoff was written (FR-3) |
| `QUALITY GATE RESULTS` | `evidence_validator.pass_rate` + status from §9.1 return contract |
| `OPEN QUESTIONS` | Copied verbatim from `report.md` "Open Questions" section |
| `REMAINING GAPS` | Copied verbatim from `grounding-gaps.md` |

## Failure modes

| Failure | Behaviour |
|---------|-----------|
| `task-builder` returns an error or is missing (MDTM route) | Surface the error; record `remediation_task_path=null`; do not retry automatically; do NOT silently downgrade to the plan route |
| `sc:workflow-protocol` returns non-`success` or STOPs, e.g. `E-GATE` (plan route) | Surface the code; record `plan_path=null` and emit `remediation_plan_path: null`; do not retry automatically (headless: the wrapper terminal-HALTs for lack of a pointer) |
| `sc:workflow-protocol` unavailable (plan route) | Surface the report path; recommend manual planning or re-running with `--depth deep`; do not fail the whole skill |
| Plan built but the Phase B pre review flags a blocker | Stop at Phase B; surface the blocker |
