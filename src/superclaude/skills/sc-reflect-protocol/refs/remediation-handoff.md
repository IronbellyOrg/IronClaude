# Wave 6 Remediation Handoff — Plan Route

Loaded by Wave 6 only when `--remediate` is set AND Wave 5 produced a deviation register with at least one item whose class warrants a remediation (see default-remediation table below). Reflect itself never fixes code; this ref documents the opt-in handoff. The default chain builds a workflow tasklist (`.dev/tasks/to-do/<slug>/<slug>.md`, a managed `TASK-WF-*` package) through `sc:workflow` for the user to run with `/sc:implement`. There is one route: the older MDTM route for `--depth deep` was removed in 6.1.0.

Merged-requirements driver: §8 cross-skill table, §10.3 Drift, §10.4 Regression.

## Route selection

There is one route. `--depth` never changes it, and an auto-escalation to Tier 2 does not either. `--remediate` is the gate on reflect, the analogue of `--fix` on troubleshoot.

| Flags | Route | Builder | User-run executor |
|-------|-------|---------|-------------------|
| no `--remediate` (any depth, including `--depth deep` alone) | **None** | none | none |
| `--remediate` (any depth) | **Plan route** | `sc:workflow-protocol` → package tasklist `<pkg>/<slug>.md` (its built-in advisory `--mode pre` review is surfaced) | `/sc:implement <pkg>/<slug>.md` |
| headless `claude --print` + `--remediate` (reflect wrapper, `superclaude reflect run --fix`) | **Plan route** | `sc:workflow-protocol` → package tasklist `<pkg>/<slug>.md` | the wrapper auto-runs `/sc:implement <remediation_plan_path>` |

- `--depth deep` alone does **not** trigger remediation: Wave 6 still requires `--remediate`.
- `--depth quick` and `--depth deep` with `--remediate` take the plan route; there is no STOP for either.
- The skill never runs `/sc:implement`, and never passes `--handoff implement` to `sc:workflow` (that would auto-run `sc:implement`). The phases below stop at a user-run execution gate.
- Headless runs take the same route; the only differences are auto-accept and no Phase B/C user gates. See "Headless auto-accept under `--print` (FR-9)".
- **Sanctioned nested call.** Reflect's Wave 6 does not call reflect on the plan itself. The `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<slug>.md` call is made by `sc:workflow` in its own Wave 4 (advisory, no `--remediate`, its own output). This is the one sanctioned exception to the SKILL.md Will Not rule against reflecting on reflect's own intermediate output.
- A `TASK-WF-*` package is an `/sc:implement` package. `sc:workflow` no longer accepts `--output`; never pass it.

## Plan route (`--remediate`) — Phases A–D

`sc:workflow` and `sc:implement` have no handoff-file field, so any reflect state that must survive (Regression items, Drift decisions, `needs_human_decision`, grounding gaps) travels as a plain section in the source file handed to `sc:workflow`. The `sc:workflow` gate forbids checkbox (`- [ ]`) and numbered-list lines anywhere in the tasklist (`sc:implement` would enumerate them as tasks), so the source uses plain dash bullets and prose only. `sc:workflow` snapshots the source byte-exact as `<pkg>/source.md`, where `<pkg>` = `.dev/tasks/to-do/<slug>`.

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

   ## Review Feedback
   <contents of <output-dir>/remediation-review-notes.md, flattened; omit this whole section on the first pass>

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

   **Flatten list syntax.** Anything copied verbatim into this source (the REPORT.md summary, register rows, test names) must first be flattened: rewrite every numbered line (`1.`, `1)`) and every checkbox line (`- [ ]`, `- [x]`, `* [ ]`) as a plain `- ` bullet or a prose sentence, keeping its full text (never delete a line). A single leftover list line makes the `sc:workflow` gate fail with `E-GATE` (or makes `sc:implement` enumerate it as a task).
3. Invoke `Skill sc:workflow-protocol` with `<output-dir>/remediation-source.md --depth standard --handoff none`. Never pass `--handoff implement`: that auto-invokes `sc:implement`, which edits product code, and the execution gate (Phase C) is always user-initiated. Do not pass `--output` (retired in `sc:workflow`; it STOPs `E-LEGACY`). The package is always created at `.dev/tasks/to-do/<slug>/`.
   Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) pass `--unattended --report-dir <report-dir>/nested/workflow-<n>/ --handoff none` (`<n>` counts from 1 and is never reused), list the nested contract in `artifacts`, also when the call failed, and read the plan path from that nested worker contract's `report_path` in step 4 instead of `<pkg>/return-contract.yaml`.
4. Read `<pkg>/return-contract.yaml` (contract 1.1) of the package workflow reports as final. `status: success` → resolve the absolute tasklist path (`<pkg>` + `plan_path`, which is package-relative `./<slug>.md`). When the contract you read names a `superseded_by` package (workflow's Wave 4R replaced it), follow it: read that package's contract and use its `plan_path` instead, repeating until a contract names none. Never emit an archived plan (one under `.dev/tasks/archive/`) or a plan whose contract says `review_verdict: FAIL` as `remediation_plan_path`: record `plan_path=null`, emit `remediation_plan_path: null`, and surface the contract's `open_blockers`. Otherwise record the path as `plan_path` in `audit.log` and emit it as the `remediation_plan_path` contract field (§9.1, 1.8.0). Any other status (for example `E-GATE`) → surface it, record `plan_path=null`, do not retry automatically.
5. `<pkg>/source.md` is the byte-exact snapshot of `remediation-source.md`, so the `## Reflect Verdict State` section is already carried there. Verify the tasklist `<slug>.md` also carries the `needs_human_decision` / `regression_count` lines; if missing, append the section to the tasklist verbatim, keeping it free of checkbox and numbered-list lines. (`sc:workflow` has no such field of its own, so reflect owns this carry.)

### Phase B — Consume the built-in pre-review

`sc:workflow` already runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<slug>.md` as its Wave 4 (advisory, read-only). Reflect does **not** make a separate call on the plan; it consumes that result. Read `reflect_status` and `reflect_report_path` from `<pkg>/return-contract.yaml` and surface both with the tasklist path.

- Reflect itself never edits the tasklist. The routing of findings belongs to `sc:workflow`'s Wave 4R (`~/.claude/skills/sc-workflow-protocol/refs/remediation.md`; project `.claude/skills/sc-workflow-protocol/refs/remediation.md` second), so one rule applies: Wave 4R repairs blocking findings surgically on a copy and places the repaired plan as a new package that supersedes the old one, or regenerates the plan as a new package that supersedes the old one. A refactor you request below still re-runs Phase A and builds a new package; do not hand-edit a placed plan. To carry a recommendation into that new package, append it to `<output-dir>/remediation-review-notes.md` (append-only; Phase A step 2 rewrites `remediation-source.md` from scratch each pass and re-includes these notes as `## Review Feedback`, so they are never lost).
- The plan route archives the package it replaces: when Wave 4R or a re-run of Phase A supersedes a package, that package moves to `.dev/tasks/archive/` and its contract carries `superseded_by`. Read the final package through Phase A step 4, never the archived one. If Wave 4R leaves blockers open, the final contract says `review_verdict: FAIL`: treat it as a blocker here (surface `open_blockers`, no `remediation_plan_path`).
- `reflect_status: skipped|failed` (`reflect_report_path: null`) → say so and fall back to spawning the `self-review` agent on `<pkg>/<slug>.md`.
- Coverage caveat: the tasklist is read as a free-form file; exact-ID matching (`R-`, `REQ-`, `SPEC-`, `T-` tokens) will not fire on `## Task N:` headings, so spec rows match through the Pass-2 containment rule only. Treat `coverage_undefined` as a surfaced warning, not a silent pass.
- Interactive outcomes: no findings → proceed to Phase C. Findings or a blocker → surface them and ask "refactor the plan before running, or proceed as-is? [refactor / proceed]"; on `refactor`, re-run Phase A as above. A blocker → STOP and do not advance to Phase C until the user resolves it.
- Headless: the built-in advisory pre-review still runs inside `sc:workflow` (extra cost), but the wrapper does not gate on its findings.

### Phase C — Execution gate (always user-initiated)

Record `baseline_ref = git rev-parse HEAD` in `audit.log`, then surface the path and the literal commands:

```text
Plan ready: <abs-path to .dev/tasks/to-do/<slug>/<slug>.md>

To execute, run:
  /sc:implement <abs-path>

The skill stops here. After /sc:implement completes, resolve the package by id (it is archived to
.dev/tasks/done/<slug>/ after a fresh FINAL; use whichever of to-do/done exists) and run the post-execution gate:
  /sc:reflect --mode post --spec <report.md> --tasklist <resolved-pkg>/<slug>.md --diff <baseline_ref> --task-log <resolved-pkg>/progress.md
```

A single ref (not `A..B`) diffs against the working tree, so `--diff <baseline_ref>` captures uncommitted `/sc:implement` edits to tracked files; `git diff` omits untracked files, so `--task-log` (the package's sibling `progress.md` ledger) lets reflect see files the run created. This is non-negotiable: the skill never runs `/sc:implement` — running it on the user's behalf bypasses their final review of what is about to change.

### Phase D — Post-execution validation (optional, user-triggered)

Only fires if the user comes back and explicitly invokes the gate. The skill itself does not poll and does not auto-resume after `/sc:implement`. The surfaced command carries no `--remediate` (no loop).

`OK` → emit "Validation passed — safe to commit." Issues → surface them; do not auto-fix. The user decides whether to revert, patch, or accept.

---

## Opt-in prompt

Wave 6 presents this verbatim **before** invoking the builder (no auto-execute — §17 Will Not), substituting bracketed fields. The user answers yes/no; ambiguous responses are treated as "no" (matches sc-troubleshoot remediation-handoff posture).

```text
Tier 3 remediation chain is available.

The chain will:
  1. Build a phased tasklist package (.dev/tasks/to-do/<slug>/<slug>.md) from this report via /sc:workflow (no code edits yet)
  2. Show workflow's built-in pre-review result (reflect_status / reflect_report_path)
  3. Stop and show the literal `/sc:implement <pkg>/<slug>.md` command for you to run
  4. After you run it and report back, run `/sc:reflect --mode post` as the final gate

Reflect identified <N> Regression-class and <M> Drift-class deviation(s) eligible for remediation.

Regression items (will be primary objective):
  <bullet list from deviation-register.md, severity-sorted>

Drift items (authorize-or-revert per item):
  <bullet list from deviation-register.md>

needs_human_decision: <true | false>

Proceed with sc:workflow?  [yes / no]

If no: the report at <report_path> is the final deliverable.
```

**State carried.** `sc:workflow` cannot read a handoff file, so the state travels in the `## Reflect Verdict State` section of `remediation-source.md`. The contract fields `handoff_memory_key` and `remediation_task_path` stay in the schema so older reports still load; they are always `null` from 6.1.0. The route records `remediation_route: plan` in `audit.log` and emits the absolute path of the built tasklist `<pkg>/<slug>.md` as the `remediation_plan_path` contract field (§9.1, 1.8.0; `null` when no plan was built). The wrapper's auto-fix loop is the only consumer.

## Headless auto-accept under `--print` (FR-9)

**One route.** `superclaude reflect run --fix` (`src/superclaude/cli/reflect/runner.py`) passes `--depth <d> --remediate`. At every depth reflect authors a plan and emits `remediation_plan_path`; the wrapper's auto-fix loop runs `/sc:implement <remediation_plan_path>` on the final placed package (the one Phase A step 4 resolved after any `superseded_by` hop) and fails closed on a non-zero apply rc. `/sc:implement` refuses an archived plan and a plan with `review_verdict: FAIL`; that refusal is a non-zero apply, which the wrapper already handles fail-closed (no re-audit, terminal HALT), so no wrapper code change is needed.

The opt-in prompt above is for **interactive** runs. When reflect runs **non-interactively**
(the reflect-wrapper launches it as `claude --print`, with **no TTY** — `--print` mode is the
headless signal; this is distinct from the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker,
which is the nested-gate suppressor, not the headless signal), `--remediate` MUST **auto-accept and
author** the corrective artifact **without presenting the yes/no prompt** — but ONLY for **AUTO-FIXABLE**
registers (solely §10.3 Drift and/or §10.2 Necessary). The authored path is then emitted as
`remediation_plan_path` (§9.1) for the wrapper to auto-run.

Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) this headless rule is selected whatever the terminal state, so the yes/no prompt is never shown.

**Headless plan route skips Phases B and C.** There is no user to gate on, and the wrapper's own re-audit after the apply (same `--base`, bounded by `--max-fix-iterations`) is the verification. Phase A (build the plan) still runs in full, including the flatten rule and the `## Reflect Verdict State` carry. The built-in advisory pre-review still runs inside `sc:workflow` (extra cost) but the wrapper does not gate on its findings.

For **HUMAN-REQUIRED** registers (any §10.4 Regression, or `needs_human_decision: true` from a
non-empty `grounding-gaps.yaml`), the headless branch authors **nothing auto-runnable**: the
`## Reflect Verdict State` section carries `needs_human_decision: true` (see
SKILL.md §"Will Not") to prompt human resolution, and `remediation_plan_path: null` is emitted (`remediation_task_path` is always null) — so
the wrapper terminal-HALTs and never auto-applies a human-decision change
(honoring `feedback_human_decision_items_must_halt`). The §"Will Not" invariant (reflect AUTHORS but
NEVER EXECUTES `/sc:implement`) is preserved in BOTH branches — only the AUTHORING accept gate changes under
`--print`, never the execution gate. The Authorized/Necessary-only short-circuit (below) still yields
`remediation_plan_path: null`.

## Default-remediation guidance per deviation class

Drives whether Wave 6 even reaches the opt-in prompt for a given register row.

| Deviation class | Default (no flag) | With `--remediate` | Notes |
|---|---|---|---|
| §10.1 Authorized | No remediation task | No remediation task | Document only; appears in report's "Authorized changes" section |
| §10.2 Necessary | No remediation task | `--remediate-docs` may propose a spec-update task (docs-only) | Default still no-op; spec update is the only remediation venue |
| §10.3 Drift | Surface "Authorize-or-revert decision required" in report | Offer the Tier 3 plan with a **backfill-or-revert prompt** in its first phase | User picks per item: (a) backfill spec to authorize, or (b) revert the drift |
| §10.4 Regression | Surface as STOP-class finding in report | **Unconditionally** offer the Tier 3 plan; regression repair is the primary objective | Also unconditionally forces Wave 3A T2 escalation per §5.3 rule 3 (debated by ≥2 reviewers before report ships) |

If the register contains only §10.1 + §10.2 items, Wave 6 short-circuits: no opt-in prompt, no `sc:workflow` invocation, emit "No Tier 3 remediation warranted — register holds only Authorized / Necessary items."

## Failure modes

| Failure | Behaviour |
|---------|-----------|
| `sc:workflow-protocol` returns non-`success` or STOPs, e.g. `E-GATE` (plan route) | Surface the code; record `plan_path=null` and emit `remediation_plan_path: null`; do not retry automatically (headless: the wrapper terminal-HALTs for lack of a pointer) |
| `sc:workflow-protocol` unavailable (plan route) | Surface the report path; recommend manual planning; do not fail the whole skill |
| Plan built but workflow's built-in pre-review (`reflect_status`) flags a blocker | Stop at Phase B; surface the blocker (interactive only) |
