# sc-brainstorm Live-vs-Baseline Remediation Plan

## Decision

Do not roll forward the current live `/sc:brainstorm` behavior as the default quality path.

Keep iteration-2 baseline as the quality bar, freeze or roll back live as the default, then selectively reintroduce live's useful improvements behind stricter provenance, context-retention, and fit-to-intent gates.

This is not a full discard. Live has useful ideas, but its current synthesis behavior is too lossy.

## Evidence Summary

Source artifacts:

- `.dev/eval-workspaces/sc-brainstorm/live-runs/qualitative-comparison-summary.md`
- `.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.md`

Qualitative comparison results:

- Cases compared: 8, eval cases 4-11
- Baseline wins: 7
- Live wins: 1
- Baseline average total: 54.00/60
- Live average total: 42.88/60
- Average live delta: -11.12 points
- `/sc:adversarial --depth quick` warranted: no cases

Dimension regressions:

| Dimension | Baseline avg | Live avg | Live delta |
|---|---:|---:|---:|
| provenance | 9.50 | 5.62 | -3.88 |
| concreteness | 9.12 | 6.88 | -2.25 |
| actionability | 9.00 | 7.38 | -1.62 |
| adversarial synthesis | 8.62 | 7.12 | -1.50 |
| fit to eval intent | 9.00 | 7.88 | -1.12 |
| coverage | 8.75 | 8.00 | -0.75 |

Structural comparison results:

- Baseline structural pass rate: 100.00%
- Live structural pass rate: 81.69%
- Live artifact completeness: 8/8 cases complete
- Live runtime/token telemetry: unavailable
- Strict quality scores for cases 4-11: unavailable

## Root Cause Pattern

The live version produces complete artifacts, but optimizes for generalized completeness over case-specific fidelity.

Recurring failure mode:

1. The final artifact broadens the problem into a generic framework.
2. Concrete anchors from the seed/eval prompt are dropped or diluted.
3. Requirement-level provenance collapses into broad source comments or frontmatter only.
4. The output remains plausible but loses the exact decision context the eval asked for.
5. Section names and metadata drift enough to break structural checks.

## Preserve These Live Improvements

The remediation should preserve useful live additions:

1. Broader governance framing
   - Security and isolation in caching
   - Policy-first auth consolidation
   - Rollout and rollback controls
   - Lifecycle-state taxonomies
   - Proof gates for runtime adoption

2. Better scope-boundary behavior
   - Requirements-discovery boundaries in incident work
   - Separation of discovery from implementation commitments where current facts are unknown

3. Repository-specific safeguards
   - Source-of-truth discipline for `src/superclaude/`
   - Avoiding generated `.claude` mirrors
   - UV-only workflow awareness

4. More explicit operational controls
   - Purge, disablement, validation, rollback rehearsal, compatibility adapters, and inventory requirements

Target state:

> Baseline specificity + baseline provenance + live governance/safety additions.

## Remediation Objectives

### Objective 1: Extract and preserve context anchors

Add a mandatory anchor-extraction step before proposal generation.

Anchor categories:

- named systems, services, products, and teams
- dates, deadlines, and time windows
- counts, scale numbers, and cost figures
- paths, files, modules, and commands
- thresholds, SLOs, SLAs, and recovery objectives
- named dependencies, vendors, tools, and observability stacks
- out-of-scope constraints
- stakeholder or organizational context
- rollback, revert, and recovery bounds
- compliance, security, and audit requirements

Acceptance criteria:

- `seed-brief.md` contains a `Context Anchors` section.
- Every proposal must preserve anchors or explicitly challenge them.
- `merged-requirements.md` contains a `Context Anchors Preserved` table.
- Dropped anchors require explicit rationale.

### Objective 2: Restore mandatory requirement-level provenance

Every final `merged-requirements.md` must include a dedicated `## Provenance` section.

Minimum provenance table:

| Requirement / Decision | Source | Variant(s) | Debate outcome | Preserved anchors |
|---|---|---|---|---|

Rules:

- Inline HTML comments are insufficient.
- Frontmatter alone is insufficient.
- Broad variant-level attribution is insufficient.
- Major FRs, NFRs, acceptance criteria, risks, and open questions require traceability.

Acceptance criteria:

- All merged artifacts include `## Provenance`.
- Provenance average across cases 4-11 recovers from 5.62 to at least 8.50.

### Objective 3: Enforce concrete-over-generic merge discipline

Add a merge rule:

> When one variant contains concrete eval-specific context and another contains a broader taxonomy, the final merge must keep the concrete context as the primary requirement and attach the taxonomy as supporting structure, not replace the concrete context.

Acceptance criteria:

- Generic taxonomies may augment concrete requirements but may not replace seed-specific constraints.
- The final artifact must still read as a response to the exact user/eval prompt, not as a reusable generic framework.

### Objective 4: Preserve thresholds and bounded commitments

Add a threshold-preservation rule:

> Any threshold, count, duration, cost, retention period, SLO/SLA, latency gate, rollout interval, or recovery objective present in the seed or winning variant must survive into the final artifact unless explicitly rejected with rationale.

Acceptance criteria:

- Numeric commitments in seed/proposals are present in the final artifact or listed as rejected.
- Rejected thresholds include reason and replacement decision path.

### Objective 5: Stabilize canonical output shape

Require canonical merged-requirements sections:

- `## Functional Requirements`
- `## Non-Functional Requirements`
- `## Acceptance Criteria`
- `## Risks`
- `## Open Questions`
- `## Provenance`

Tables are allowed inside sections, but canonical section names must remain stable.

Acceptance criteria:

- Structural graders detect all required sections.
- Risk content appears under `## Risks`, even if a table is used.

### Objective 6: Fix metadata and return-contract drift

Define one canonical return-contract schema and one canonical merged-requirements frontmatter schema.

Minimum merged-requirements frontmatter:

```yaml
---
spec_type: merged_requirements
adversarial_status: success
proposal_count: <n>
domain: <domain>
depth: <quick|standard|deep>
agent_spec: <spec>
provenance: required
---
```

For blind evals:

```yaml
blind_mode: true
anonymized_labels: true
```

Acceptance criteria:

- `proposal_count` matches the invoked proposal count.
- `agent_spec` and model/persona aliases are present.
- Status vocabulary is normalized.
- Blind-mode metadata survives through the final artifact and return contract.

### Objective 7: Add final fit-to-intent check

Before finalizing `merged-requirements.md`, the protocol must verify:

1. What exact decision/problem did the user ask for?
2. What concrete context did the user provide?
3. Did the final artifact preserve that context?
4. Did any requirement become generic enough to apply to a different organization or problem?
5. If yes, revise before returning success.

Acceptance criteria:

- Final artifacts include or internally satisfy a fit-to-intent checklist.
- Fit-to-eval-intent average across cases 4-11 remains at or above 8.50.

## Case-Specific Remediation Targets

### `code-migrate-pytest-vitest`

Restore:

- frontend-slice grounding
- pytest-shell-playwright bridge
- Storybook fixture details
- LCOV merge constraints
- batch order and bridge deletion sequence

Preserve from live:

- runtime-eligibility guard
- semantic preservation inventory
- dependency governance

### `architecture-worker-pool-errors`

Restore:

- 12 worker fleets
- Q1 incidents
- $40k retry cost
- Q3 cost target
- 100µs/5% latency gate
- 13M messages/hour floor
- 2-week canary soak

Preserve from live:

- mixed-result semantics
- terminal-state taxonomy
- compatibility adapters

### `process-contributor-onboarding`

Restore:

- hard onboarding metrics
- SLA thresholds
- concrete artifact names
- owner and budget decisions

Preserve from live:

- IronClaude source-of-truth rules
- UV-only workflow
- docs-only contributor path
- first-PR evidence package

### `research-bun-vs-node`

Restore:

- Q2 2026 decision frame
- planned WebSocket gateway
- 40-service Node 20 fleet
- named native dependencies
- observability stack
- one-sprint revert bound

Preserve from live:

- runtime-adoption taxonomy
- production proof gates
- assumption and benchmark separation

### `code-api-caching-tasklist`

Restore:

- cache key format
- TTL defaults
- concrete framework/module choices
- metrics names
- test quantities
- requirement-level provenance

Preserve from live:

- tenant/auth/session isolation
- purge, rollback, and policy-version controls
- regulated endpoint classification

### `code-feature-flag-task`

Use live as partial model, but fix:

- add dedicated Provenance section
- close override storage and precedence decisions
- map requirements to proposals and debate outcomes

Preserve from live:

- CLI command fit
- source-of-truth safeguards
- malformed override fail-closed behavior
- machine-readable output guidance

### `incident-payment-webhook-q1`

Restore:

- explicit Risks section
- incident thresholds
- retention values
- rollout order
- rollback triggers
- artifact-level provenance

Preserve from live:

- requirements-discovery boundaries
- lifecycle-state taxonomy
- clearer proximate-trigger framing

### `code-duplicate-auth-blind`

Restore:

- blind-mode metadata
- 5-proposal traceability
- Q3 compliance forcing function
- audit overlap
- 7-year retention
- pentest gates
- dashboards-before-build
- decommission gates

Preserve from live:

- policy-and-contract-first framing
- drift inventory classes
- AuthRequest/AuthResult/PolicyDecision/AuditEvent vocabulary

## Reflection Validation Notes

`/sc:reflect --type task --analyze` found the plan directionally sound but not yet executable enough for task-builder consumption without adding implementation targets and validation checkpoints.

Required refinements added before tasklist generation:

- name source-of-truth files to edit, not generated `.claude` mirrors
- separate protocol changes from adversarial merge-template changes
- define eval assertion and validation artifacts
- add measurable verification commands and quality gates
- preserve useful live behavior explicitly so remediation does not become a blanket rollback

## Likely Source-of-Truth Files

Implementation should inspect and update these files first:

- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md`
- `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md`
- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`
- `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md`
- `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md`
- `.dev/eval-workspaces/sc-brainstorm/evals/evals.json`
- `.dev/eval-workspaces/sc-brainstorm/grader.py`
- `.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py`

Do not edit or stage generated `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates` mirrors. If local Claude Code skill mirrors are needed for execution testing, edit `src/superclaude/` first and then run `make sync-dev`.

## Validation Commands

Use UV for Python operations.

Minimum validation after implementation:

```bash
uv run python - <<'PY'
import py_compile
for path in [
    '.dev/eval-workspaces/sc-brainstorm/grader.py',
    '.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py',
]:
    py_compile.compile(path, doraise=True)
print('syntax ok')
PY
```

```bash
uv run python .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py
```

If package checks are relevant to changed source files:

```bash
make verify-sync
```

If the implementation changes Python package code or testable helpers:

```bash
uv run pytest tests/ -q
```

Eval acceptance after rerunning cases 4-11:

- structural pass rate: at least 95%, target 100%
- qualitative baseline wins: no more than 2/8
- live average: at least 52/60
- provenance average: at least 8.50
- concreteness average: at least 8.50
- no missing dedicated Provenance sections
- no critical seed anchors dropped without rationale

## Implementation Phases

### Phase 0: Safety hold

If the current live implementation is user-facing, roll it back or gate it until remediation passes the eval quality gates.

### Phase 1: Protocol contract fixes

Update `/sc:brainstorm` protocol to require:

1. must-preserve anchor extraction
2. mandatory Provenance section
3. canonical section names
4. canonical frontmatter and return-contract schema
5. final fit-to-intent check

### Phase 2: Merge-rule fixes

Update adversarial merge instructions to enforce:

1. concrete beats generic
2. thresholds survive
3. dropped anchors require explicit rationale
4. live governance additions augment, not replace, baseline specificity

### Phase 3: Eval hardening

Add or update assertions for:

1. Provenance section presence
2. anchor preservation
3. threshold preservation
4. fit-to-intent language
5. canonical section names
6. frontmatter schema

### Phase 4: Rerun cases 4-11

Success criteria:

- structural pass rate: at least 95%, target 100%
- qualitative baseline wins: no more than 2/8
- live average: at least 52/60
- provenance average: at least 8.50
- concreteness average: at least 8.50
- no missing dedicated Provenance sections
- no critical seed anchors dropped without rationale

## Rollback Recommendation

If the current live implementation is already affecting normal `/sc:brainstorm` users:

- temporarily roll it back or gate it
- preserve live outputs and eval artifacts as regression evidence
- reintroduce live improvements only after contract, provenance, and context-retention fixes land

If it is not yet user-facing:

- do not promote it
- keep it on the evaluation branch
- treat this as a failed quality gate with useful learnings

## Proposed Execution Prompt

```text
/sc:task "Implement targeted sc-brainstorm remediation from the live-vs-baseline regression analysis: add must-preserve anchor extraction, mandatory Provenance section, canonical merged-requirements/frontmatter schema, concrete-over-generic merge rule, threshold preservation, and final fit-to-intent check. Preserve live improvements around governance, safety gates, lifecycle taxonomies, and repository-specific safeguards. Update eval assertions for cases 4-11 accordingly and rerun the sc-brainstorm eval comparison. Do not stage .claude generated mirrors."
```
