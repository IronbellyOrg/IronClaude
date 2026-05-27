# Wave 6 Remediation Handoff — task-builder Chain

Loaded by Wave 6 only when `--remediate` is set AND Wave 5 produced a deviation register with at least one item whose class warrants an MDTM remediation task (see default-remediation table below). Reflect itself never fixes code; this ref documents the opt-in handoff to `task-builder`.

Source: `task-builder/SKILL.md` lines 785-985 (M1-frozen BUILD_REQUEST schema, plus the API-001-M2 `EXECUTION_CONTEXT_REQUIREMENTS` extension). Merged-requirements driver: §7 row "task-builder (skill, not agent) — Wave 6", §8 cross-skill table, §10.3 Drift, §10.4 Regression.

## BUILD_REQUEST template

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

Wave 6 presents this verbatim **before** invoking `task-builder` (no auto-execute — §17 Will Not). The user answers yes/no; ambiguous responses are treated as "no" (matches sc-troubleshoot remediation-handoff posture).

```text
Reflect identified <N> Regression-class and <M> Drift-class deviation(s)
eligible for Tier 3 remediation.

Regression items (will be primary objective):
  <bullet list from deviation-register.md, severity-sorted>

Drift items (authorize-or-revert per item):
  <bullet list from deviation-register.md>

Spawn task-builder to author a remediation MDTM task?  [yes / no]

If yes: an MDTM task file will be written under .dev/tasks/to-do/.
        Reflect will NOT execute /task — you run it yourself.
If no:  the report at <report_path> is the final deliverable.
```

## Default-remediation guidance per deviation class

Drives whether Wave 6 even reaches the opt-in prompt for a given register row.

| Deviation class | Default (no flag) | With `--remediate` | Notes |
|---|---|---|---|
| §10.1 Authorized | No remediation task | No remediation task | Document only; appears in report's "Authorized changes" section |
| §10.2 Necessary | No remediation task | `--remediate-docs` may propose a spec-update task (TEMPLATE: 01, docs-only) | Default still no-op; spec update is the only remediation venue |
| §10.3 Drift | Surface "Authorize-or-revert decision required" in report | Offer Tier 3 task with **backfill-or-revert prompt** in TEMPLATE 02 phase 1 | User picks per item: (a) backfill spec to authorize, or (b) revert the drift |
| §10.4 Regression | Surface as STOP-class finding in report | **Unconditionally** offer Tier 3 task; regression repair is the primary objective | Also unconditionally forces Wave 3A T2 escalation per §5.3 rule 3 (debated by ≥2 reviewers before report ships) |

If the register contains only §10.1 + §10.2 items, Wave 6 short-circuits: no opt-in prompt, no `task-builder` invocation, emit "No Tier 3 remediation warranted — register holds only Authorized / Necessary items."

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
| `QUALITY GATE RESULTS` | `evidence_validator.pass_rate` + status from §9.1 return contract |
| `OPEN QUESTIONS` | Copied verbatim from `report.md` "Open Questions" section |
| `REMAINING GAPS` | Copied verbatim from `grounding-gaps.md` |
