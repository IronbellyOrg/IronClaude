# Agent 2 — Skills Eval Proposals

## Proposal 1 (one-off): `troubleshoot_escalation_contract`

- **Target skill(s):** `sc-troubleshoot-protocol`
- **Hypothesis:** Vague/deep and low-confidence cases halt or escalate deterministically; output includes required contract fields.
- **Cadence:** one-off baseline.
- **Inputs:** `/sc:troubleshoot --depth deep "flaky test sometimes fails across auth and deploy paths" --scope src/superclaude`
- **Assertions:** exit 0; transcript contains `tier_reached`, `confidence`, `escalation_reason`; contains `forced_by_depth_deep` or Tier 2 evidence; no invented uncited diagnosis.
- **Requires:** `claude`, `git`; optional `mcp_server.auggie`, `mcp_server.serena`.
- **Complexity:** medium.
- **Value:** Catches regressions in STOP/escalation behavior.
- **Evidence:** `.claude/skills/sc-troubleshoot-protocol/SKILL.md:26-35`, `:37-58`; `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:23-42`.

## Proposal 2 (one-off): `tasklist_deterministic_shape`

- **Target skill(s):** `sc-tasklist-protocol`
- **Hypothesis:** Same roadmap yields canonical Sprint-compatible tasklist shape: index + `phase-N-tasklist.md`, sequential phases, explicit artifact paths, objective acceptance criteria.
- **Cadence:** one-off baseline.
- **Inputs:** `/sc:tasklist` with a tiny roadmap containing Phase 1 and Phase 3 plus `.dev/releases/current/v1.2.3/`.
- **Assertions:** exit 0; files `tasklist-index.md`, `phase-1-tasklist.md`, `phase-2-tasklist.md`; phase filenames literal in index; phase files end with "Checkpoint: End of Phase".
- **Requires:** `claude`, `git`.
- **Complexity:** medium.
- **Value:** Catches drift breaking `superclaude sprint run` discovery and deterministic renumbering.
- **Evidence:** `.claude/skills/sc-tasklist-protocol/SKILL.md:31-43`, `:88-120`, `:215-219`; `.claude/skills/sc-tasklist-protocol/templates/phase-template.md:108-116`.

## Proposal 3 (recurring): `adversarial_task_quality_drift`

- **Target skill(s):** `sc-adversarial-protocol`, `sc-task-protocol`, `task-builder`
- **Hypothesis:** Protocols continue enforcing conservative quality gates: adversarial parsing rejects malformed specs, task execution freezes on pre-existing test failures, task-builder keeps research/QA gates.
- **Cadence:** recurring — scheduled nightly or on changes under `.claude/skills/**`. Protocol text is prompt-sensitive and easy to regress without unit tests. INFERENTIAL.
- **Inputs:** malformed `/sc:adversarial --source spec.md --generate roadmap --agents 'opus:architect:unquoted'`; `/sc:task` prompt with pre-existing failing test transcript; `task-builder` vague request.
- **Assertions:** adversarial transcript contains `Instruction must be quoted`; task flow contains `FREEZE`/no auto-fix; task-builder asks clarification or emits QA-gated plan.
- **Requires:** `claude`, `git`; no MCP.
- **Complexity:** complex.
- **Value:** Catches high-cost safety regressions.
- **Evidence:** `.claude/skills/sc-adversarial-protocol/refs/agent-specs.md:63-70`; `.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md:7-27`; `.claude/skills/sc-task-protocol/SKILL.md:133-151`, `:181-220`; `.claude/skills/task-builder/SKILL.md:18-24`, `:143-156`.
