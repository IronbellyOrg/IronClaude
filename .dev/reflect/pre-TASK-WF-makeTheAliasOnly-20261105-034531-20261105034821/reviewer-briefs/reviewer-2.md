# Reviewer 2 brief (persona: qa: audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding; audit acceptance criteria for verifiability)

## T1 card excerpt

(verbatim slice of .dev/reflect/pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821/t1-card.md)

#### T1 reflection card (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md` (9 lines; 1 request paragraph at line 1, owner/evidence context at lines 3-9)
- Tasklist: `.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md` (9 tasks, 4 phases)
- Coverage (deterministic, `artifacts/coverage-matrix.json`): parsed requirement IDs 0; inferred rows 13 (INF-001..INF-013); `coverage_pct_union` 0.9231; unmapped: INF-011; `coverage_degraded: parsed-sparse` (inferred > parsed), so Tier 1 stop is forbidden and the run routes to Tier 2.
- Structural signals: `S_scope` 9 tasks; `S_domains` 4 (code, tests, docs, config/spec docs under .dev); `S_dev_density` 0.0769.

#### Coverage findings

- C-1 (grounded) 12 of 13 inferred requirements map to a task by containment (ratios 0.6667 to 0.9167 in `artifacts/coverage-matrix.json`). The matcher is word-overlap only, so three matches are loose: INF-002 (do not edit ccsession-tag) matched Task 9 although the guard is enforced by the Constraints block at plan lines 17-24 and by Task 9's final acceptance bullet; INF-010 (plugin mirrors) matched Task 1 although mirror copying is written in Task 5 (plan lines 78-86) and the Constraints; INF-012 (do not edit the launcher) matched Task 6 although it is a Constraints item.
- C-2 (grounded) INF-011 ("update any existing test that pins an edited string") scored 0.5 and is reported unmapped, but it is covered by Task 3 (plan lines 58-66, edits tests/skills/test_issue_protocol.py) and Task 5 (plan lines 78-86, edits tests/skills/test_workflow_archive.py and tests/skills/test_task_workspace_lifecycle.py). Treat as a matcher false negative, not a plan gap.
- C-3 (grounded) Every Task has an `Acceptance criteria:` block with at least two bullets (plan lines 28-125).

#### Self-assessment

Grounding is by direct reads of the plan, the repo files named above and the workspace defaults file. Matcher results are deterministic; the three loose matches are disclosed in C-1.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T03:50:45Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-384-ccsession-model-aliases projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-384-ccsession-model-aliases

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1-9

```markdown
Make the alias-only model selection for #384 explicit and tested. Owner decision (final, 2026-11-05, option A): agents, commands, skills and the Python package keep the plain aliases opus, sonnet, haiku; in a ccsession tier workspace the launcher (a separate later PR, NOT in this plan) exports ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2; outside a ccsession workspace nothing is set so the plain names apply. Do NOT edit src/superclaude/skills/ccsession-tag/ or ccsession-orca (read-only, issue #315). This plan covers: (1) aliases-only tests with an allow-list that scan src/superclaude agents, commands, skills and Python for literal picker ids (claude-gw-tier*), dated or full model ids used as selections (e.g. claude-opus-4-8), and agent frontmatter model values other than opus/sonnet/haiku/inherit, failing before the fixes; the existing issue-worker agents (claude-gw-tier1a/2/3) are documented allow-list exceptions; (2) docs of the mapping and the outside-workspace fallback (the sc-issue-protocol refs/tiers.md, the user-guide and developer-guide pages that describe model selection, and the Claude Code subagent resolution facts: frontmatter model takes alias/full id/inherit, Agent-call model param takes aliases only, ANTHROPIC_DEFAULT_* values may be tier ids, verified); (3) fixes of the sites that bypass aliases: src/superclaude/cli/reflect/commands.py _DEFAULT_MODEL claude-opus-4-8 (and its use at the model argument), the haiku workaround --models opus,sonnet in skills/sc-issue-protocol/refs/chains.md and templates (brainstorm defaults to opus,sonnet,haiku stay), the audit-scanner Haiku-versus-sonnet contradiction (skills/sc-cleanup-audit-protocol/SKILL.md and commands/cleanup-audit.md say Haiku while agents/audit-scanner.md pins sonnet), and the T1_Model01-style env names in skills/sc-implement-protocol/refs/retry.md that do not match the T1Model01/T1aModel01 names the workspace exports; plus the plugins/superclaude mirror copies of any edited file; (4) update any existing test that pins an edited string. Files and evidence: @.dev/issues/384/issue-summary.md @.dev/issues/384/analysis/analyze-superclaude.md @.dev/issues/384/accuracy-check.md

Additional context supplied with the request (owner answers relayed by the coordinator on 2026-11-05, and the evidence behind option A):

- Do NOT edit the ccsession launcher in this change. The launcher edit is a separate small pull request, done only after the #315 pull request is merged. This change must deliver, for that follow-up, the exact edit as a written spec (file, anchor, the three exports and where they go) plus a test that fails before the edit.
- Evidence (checked 2026-11-05 in a throwaway HOME): Claude Code accepts a tier id as the VALUE of ANTHROPIC_DEFAULT_OPUS_MODEL. With OPUS=claude-gw-tier1a, `claude -p --model opus` ran on claude-gw-tier1a. With OPUS=claude-gw-tier1a and HAIKU=claude-gw-tier2, a subagent with `model: opus` ran on claude-gw-tier1a and one with `model: haiku` ran on claude-gw-tier2 while the main session stayed on its own model.
- Docs (code.claude.com/docs/en/sub-agents): frontmatter model takes sonnet/opus/haiku/fable, a full model id, or inherit; no environment interpolation. The Agent-call model parameter takes only the four aliases.
- The workspace exports T3Model01, T2Model01, T2Model02, T1Model01, T1Model02 (legacy Tier 1 slots kept for readers such as swarm and reflect) and T1aModel01, T1aModel02, T1bModel01-03; none of the underscore names T3_Model01, T2_Model02, T1_Model01, T1_Model02 exist.
- /sc:issue claim of #384 wrote the cheatsheet, the accuracy check and the deep analysis; the issue's first acceptance criterion was reworded in a comment on #384.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:17-24

```markdown
## Constraints

- Do not edit anything under src/superclaude/skills/ccsession-tag/ or any ccsession-orca file (issue #315 owns them); read them only. Do not edit the ccsession launcher in this change.
- Agent, command and skill text keeps the plain aliases opus, sonnet and haiku. The three issue-worker agents (src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md) keep their pinned claude-gw-tier ids as documented allow-list exceptions.
- Edit under src/ only; the .claude/ copies are gitignored sync output regenerated by make sync-dev. Where an edited src/superclaude file has a byte-identical copy under plugins/superclaude/, copy the edited file over that mirror so both stay identical.
- Do not change `model:` values in any agent file, and do not add agent files.
- Python commands run through uv (uv run pytest ...). Run only the tests named in a task plus the tests that read the files it edits; never the whole suite and never tests/cli/eval/ as a directory.
- Task-owned evidence is written under ./artifacts/ in this package.
```

### src/superclaude/skills/sc-issue-protocol/refs/chains.md:11-13

```markdown
| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:brainstorm "<topic> @<S>" --depth quick --models opus,sonnet` (no `--handoff`)<br>2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`<br>3. `/sc:implement <plan path printed by step 2>` |
| Feature, medium | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --blind --models opus,sonnet`<br>2. `/sc:design <brainstorm dir>/merged-requirements.md --type <architecture\|api\|component\|database> --format spec`<br>3. `/sc:workflow <design doc> --depth standard --handoff none`<br>4. `/sc:implement <plan path>` |
| Feature, complex | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind --models opus,sonnet`<br>2. `/sc:design <merged-requirements.md> --type <...> --format spec`<br>3. `/sc:workflow <design doc> --depth deep --handoff none`<br>4. `/sc:implement <plan path>` |
```

### src/superclaude/skills/sc-issue-protocol/refs/chains.md:21-21

```markdown
- `/sc:brainstorm --models` defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only. Every brainstorm row passes `--models opus,sonnet` so no proposal runs on the `haiku` alias, which on this workspace resolves to `glm-5.3` (`refs/tiers.md`), below T2 (B14). Aliases cannot name a picker ID, so this is the closest the chain can get to B14 inside a brainstorm; the session tier itself is pinned by the `/model` line (default D25).
```

### tests/skills/test_issue_protocol.py:268-282

```python
def test_brainstorm_steps_have_no_handoff_and_pin_models():
    rows = chain_rows(_text(REFS / "chains.md"))
    assert len(rows) == 6
    steps = [
        s
        for row in rows
        for s in _COMMAND_SPAN.findall(row)
        if s.startswith("/sc:brainstorm")
    ]
    assert len(steps) == 3
    for step in steps:
        assert "--handoff tasklist" not in step and "--handoff design" not in step
        assert "--models opus,sonnet" in step
    text = _text(REFS / "chains.md")
    assert "--handoff tasklist" not in text and "--handoff design" not in text
```

### src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:68-74

```markdown
3. **Orchestrate**: Spawn parallel subagents via Task tool in waves of 7-8 concurrent agents. Pass 1 uses `audit-scanner` (Haiku), Pass 2 uses `audit-analyzer` (Sonnet), Pass 3 uses `audit-comparator` (Sonnet). Each agent writes batch reports incrementally to disk. Track progress via TodoWrite.
4. **Validate**: Spawn `audit-validator` for 10% spot-check sampling (5 findings per 50 files). Verify grep claims match actual results. Enforce quality gates: all batch reports must have required sections and mandatory per-file profiles. Failed reports trigger regeneration.
5. **Report**: Spawn `audit-consolidator` to merge batch reports into pass summaries. For `--pass all`, produce final report with executive summary, prioritized action items, cross-cutting findings, and discovered issues registry. Apply ultrathink synthesis for cross-pass pattern extraction.

Key behaviors:

- **Haiku-first cost optimization**: Pass 1 uses Haiku agents for 50-70% cost reduction; Sonnet reserved for deep analysis in Passes 2-3
```

### src/superclaude/agents/audit-scanner.md:1-8

```markdown
---
name: audit-scanner
description: "Fast read-only surface scanner for repository audit Pass 1. Classifies files as DELETE/REVIEW/KEEP with grep evidence."
tools: Read, Grep, Glob
model: sonnet
maxTurns: 60
permissionMode: plan
---
```

### tests/swarm/test_coder_tier_env_2026_10.py:1-30

```python
"""Coder tier env change (2026-10): pools, window lines, vendor diversity.

The Coder workspace env now carries context windows next to each tier model
(``T2Model01_WINDOW``) and per tier (``T2_WINDOW``). Every reader builds exact
slot names, so these must never be taken as models; the pools themselves
change to the new tier contents.
"""

from __future__ import annotations

import pytest

from superclaude.cli.reflect._diversity import (
    _vendor_from_model_id,
    compute_vendor_diversity,
)
from superclaude.cli.reflect.fallback import evaluate_quorum
from superclaude.cli.reflect.runner import count_model_aliases
from superclaude.cli.swarm.config import SwarmConfig
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.transports.openai_compat import read_env_for_pool

CODER_ENV = {
    "T2ProxyUrl": "https://gateway.invalid/cli/v1",
    "T2ProxyKey": "test-key",
    "T1ProxyUrl": "https://gateway.invalid/cli/v1",
    "T1ProxyKey": "test-key",
    "T1_WINDOW": "850000",
    "T1Model01": "claude-opus-5-5",
    "T1Model01_WINDOW": "1000000",
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:26-26

```markdown
## Phase 1: Pin the policy with tests that fail first
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:46-76

```markdown
## Phase 2: Fix the sites that bypass the aliases

## Task 2: Make the reflect default model an alias

Depends on: Task 1

In src/superclaude/cli/reflect/commands.py change `_DEFAULT_MODEL = "claude-opus-4-8"` (line 31) to `"opus"` and update the comment above it (lines 26-30) to say the default is the plain alias opus, that ANTHROPIC_MODEL still takes precedence at the use in the reflect run command (`model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL`, about line 359), and that the alias resolves to claude-gw-tier1a only inside a ccsession tier workspace (see docs/reference/model-aliases.md). Find the tests that import superclaude.cli.reflect.commands or reference _DEFAULT_MODEL (search tests/ for them) and run them.

Acceptance criteria:
- `grep -n claude-opus-4-8 src/superclaude/cli/reflect/commands.py` returns nothing and `_DEFAULT_MODEL == "opus"`.
- The Python constants test and the reflect default test of tests/skills/test_model_alias_policy.py pass; the reflect tests found by the search pass; evidence saved to ./artifacts/t2-test.log.

## Task 3: Drop the haiku workaround from the issue chains

Depends on: Task 1

In src/superclaude/skills/sc-issue-protocol/refs/chains.md remove ` --models opus,sonnet` from the three brainstorm steps in the table rows for Feature simple, Feature medium and Feature complex (lines 11-13), and replace the note at line 21 (the bullet that begins with /sc:brainstorm --models defaults) with a bullet that says: the brainstorm rows use the default models opus,sonnet,haiku; inside a ccsession tier workspace these resolve to claude-gw-tier1a, claude-gw-tier1b and claude-gw-tier2, outside one to Claude Code's own models; see docs/reference/model-aliases.md. In tests/skills/test_issue_protocol.py rename test_brainstorm_steps_have_no_handoff_and_pin_models (lines 268-282) to test_brainstorm_steps_have_no_handoff_and_use_default_models and replace `assert "--models opus,sonnet" in step` with an assertion that `--models` is not in the step. In docs/designs/sc-issue-command.md add a note "Superseded by #384: the chains use the default models; see docs/reference/model-aliases.md" to the D25 row (about line 442) and to the bullet at about line 237 that explains the workaround; leave the rest of that design record unchanged.

Acceptance criteria:
- `grep -n "models opus,sonnet" src/superclaude/skills/sc-issue-protocol/refs/chains.md` returns nothing and the six chain rows still parse (the existing chain tests in tests/skills/test_issue_protocol.py pass).
- The chains test of tests/skills/test_model_alias_policy.py passes; `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py` passes; evidence saved to ./artifacts/t3-test.log.

## Task 4: Align the cleanup-audit docs with the audit-scanner pin

Depends on: Task 1

src/superclaude/agents/audit-scanner.md pins `model: sonnet` (a deliberate change from haiku made in commit 70ef6486, which replaced haiku defaults with sonnet); the docs still say Haiku. Leave the agent file unchanged and edit the docs to state Sonnet: in src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md lines 68 (`audit-scanner` (Haiku)), 74 (Haiku-first cost optimization), 95 (audit-scanner (Haiku, Pass 1)), 99 (Haiku-First Escalation) and 114 (Uses Haiku agents), and in src/superclaude/commands/cleanup-audit.md lines 43 and 53. Replace each Haiku mention with Sonnet or neutral wording (for example "Surface-first escalation: all files get a surface scan, then the flagged subset gets deep analysis"), and remove the 50-70% cost-reduction claim, which was specific to Haiku. Then search src/superclaude and docs/ for any other text that says audit-scanner runs on Haiku and fix it the same way; the Haiku strings in tests/cli_portify/test_discover_components.py are parser fixtures and stay.

Acceptance criteria:
- `grep -rn "Haiku" src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md src/superclaude/commands/cleanup-audit.md` returns nothing and src/superclaude/agents/audit-scanner.md is unchanged.
- The cleanup-audit test of tests/skills/test_model_alias_policy.py passes, and the existing tests that read these two files (search tests/ for cleanup-audit and sc-cleanup-audit-protocol) pass; evidence saved to ./artifacts/t4-test.log.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:88-129

```markdown
## Phase 3: Document the mapping

## Task 6: Write the model-alias reference page

Depends on: Task 1

Create docs/reference/model-aliases.md and add a line for it to the index in docs/reference/README.md. Sections: what a primitive may name (plain aliases only; the issue-worker allow-list and why; the test tests/skills/test_model_alias_policy.py enforces it); the mapping table (opus to claude-gw-tier1a via ANTHROPIC_DEFAULT_OPUS_MODEL, sonnet to claude-gw-tier1b via ANTHROPIC_DEFAULT_SONNET_MODEL, haiku to claude-gw-tier2 via ANTHROPIC_DEFAULT_HAIKU_MODEL inside a ccsession tier workspace; outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning), stating the mapping is owner-decided on 2026-11-05 and is applied by the ccsession launcher in a follow-up change; why aliases and not picker ids (frontmatter model takes an alias, a full model id or inherit with no environment lookup; the Agent-call model parameter takes only sonnet, opus, haiku and fable; source https://code.claude.com/docs/en/sub-agents read 2026-11-05) and the verified behaviour (with ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a and ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2, a subagent with model: opus ran on claude-gw-tier1a and one with model: haiku on claude-gw-tier2 while the main session kept its own model; Claude Code logs an unrecognized_model notice but serves the request); and a Known consequences section: reflect reviewer diversity counts the three variable values (tier1a and tier1b both list Claude Sonnet 5.5 in src/superclaude/skills/ccsession-tag/MODEL-TIERS.md), sprint alternate-model suggestions return nothing for tier-valued slots (src/superclaude/cli/sprint/aienv.py), roadmap step ids such as generate-opus-architect and recommend best_model values stay unchanged because the aliases stay, and today the workspace defaults file exports real model ids for the three variables until the launcher change lands.

Acceptance criteria:
- docs/reference/model-aliases.md exists with the sections above and the three exports spelled exactly as in the mapping table; docs/reference/README.md links to it.
- The mapping document test of tests/skills/test_model_alias_policy.py passes; the markdown contains no secrets or tokens; evidence saved to ./artifacts/t6-test.log.

## Task 7: Point the existing model pages at the reference page

Depends on: Task 6

Edit src/superclaude/skills/sc-issue-protocol/refs/tiers.md: in item 4 of the list under "Why the pin lives in frontmatter" (line 26) replace the claim that haiku resolves to glm-5.3 on this workspace with the statement that the haiku alias follows ANTHROPIC_DEFAULT_HAIKU_MODEL and, inside a ccsession tier workspace, resolves to claude-gw-tier2 once the launcher sets it, and add one sentence under "E-TIER-UNAVAILABLE" (after line 40) that the issue workers are the only primitives pinned to picker ids and all other primitives use aliases (docs/reference/model-aliases.md). In docs/user-guide/brainstorm.md extend the `--models` row (line 52) with: inside a ccsession tier workspace opus, sonnet and haiku resolve to claude-gw-tier1a, claude-gw-tier1b and claude-gw-tier2; see docs/reference/model-aliases.md. In docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md add a short note, in the section that describes agent frontmatter if one exists (find the heading that mentions frontmatter or the `model` field), that agent `model:` must be an alias unless it is an allow-listed issue worker, with a link to docs/reference/model-aliases.md; if the guide has no such section, record that in ./artifacts/t7-notes.md and skip this file.

Acceptance criteria:
- src/superclaude/skills/sc-issue-protocol/refs/tiers.md no longer says the haiku alias resolves to glm-5.3 as a fixed fact, and still passes `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py`.
- docs/user-guide/brainstorm.md and the developer guide (or ./artifacts/t7-notes.md explaining the skip) carry the pointer; every added link target exists in the repository.

## Phase 4: Guard the launcher follow-up

## Task 8: Add characterization tests for tier-valued alias variables

Depends on: Task 6

Add tests that pin today's behaviour when the three variables hold tier ids, so the launcher change cannot silently alter it: in tests/sprint/test_aienv.py (existing tests there show the `env=` seam of suggest_alternate_model) assert that with ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b and ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2 the function _load_aliases returns those ids unchanged under the keys opus, sonnet and haiku, and that suggest_alternate_model("claude-opus-5-5", env=that env) returns None (never a fabricated alias). In the existing test module for superclaude.cli.reflect.runner.count_model_aliases (search tests/ for count_model_aliases) assert that the same env gives a count of 3. Each test docstring says it records current behaviour and points to the Known consequences section of docs/reference/model-aliases.md.

Acceptance criteria:
- The three new tests pass on unchanged production code, and `uv run pytest tests/sprint/test_aienv.py` and the reflect test module that holds the count test pass; evidence saved to ./artifacts/t8-test.log.

## Task 9: Write the launcher follow-up spec with its failing test

Depends on: Task 6

Create .dev/issues/384/launcher-followup.md, the exact spec of the separate launcher pull request that may start only after the #315 pull request is merged. Read, without editing, src/superclaude/skills/ccsession-tag/ccsession (the shell launcher), src/superclaude/skills/ccsession-tag/models.py and tests/unit/test_ccsession_tiers.py. The spec states: the file to edit (src/superclaude/skills/ccsession-tag/ccsession) with the anchor (the function or block that handles tier mode and exports PROFILE_MODEL / ANTHROPIC_CUSTOM_MODEL_OPTION, quoted from the file with its line numbers at this branch's base commit and marked "re-verify after #315 merges"); the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2) and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched; the tier-mode detection rule from models.py (a T<N>_WINDOW variable exists and CCSESSION_TIERS is not 0); and a failing-first pytest, as a code block, in the style of the tier-launch tests of tests/unit/test_ccsession_tiers.py using only helpers that exist there (state which helper captures the launched environment, and if the harness cannot capture those three variables say exactly what small harness addition is needed). The test asserts the three values in a default tier launch and that a non-tier launch does not set them.

Acceptance criteria:
- .dev/issues/384/launcher-followup.md exists and contains the file path, the quoted anchor with line numbers, the three exact export lines, the placement and tier-mode rule, the test code block, and the sentence that the edit must not start before the #315 pull request is merged.
- Every helper name used in the test code block exists in tests/unit/test_ccsession_tiers.py (checked by grep and listed in the file), and no file under src/superclaude/skills/ccsession-tag/ was modified (`git diff --stat -- src/superclaude/skills/ccsession-tag` is empty).
```

## Coverage slice

| Requirement | Quote (70 chars) | Match | Task | Spec citation |
|---|---|---|---|---|
| INF-001 | agents, commands, skills and the Python package keep the plain aliases | containment 0.7273 | Task 1 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-002 | Do NOT edit src/superclaude/skills/ccsession-tag/ or ccsession-orca (r | containment 0.8 | Task 9 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-003 | aliases-only tests with an allow-list that scan src/superclaude agents | containment 0.6667 | Task 1 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-004 | the existing issue-worker agents (claude-gw-tier1a/2/3) are documented | containment 0.8182 | Task 7 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-005 | docs of the mapping and the outside-workspace fallback (the sc-issue-p | containment 0.7222 | Task 7 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-006 | src/superclaude/cli/reflect/commands.py _DEFAULT_MODEL claude-opus-4-8 | containment 0.9167 | Task 2 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-007 | the haiku workaround --models opus,sonnet in skills/sc-issue-protocol/ | containment 0.875 | Task 3 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-008 | the audit-scanner Haiku-versus-sonnet contradiction (skills/sc-cleanup | containment 0.8235 | Task 4 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-009 | the T1_Model01-style env names in skills/sc-implement-protocol/refs/re | containment 0.75 | Task 5 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-010 | plus the plugins/superclaude mirror copies of any edited file | containment 0.6667 | Task 1 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-011 | update any existing test that pins an edited string | none 0.5 | Task 1 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-012 | Do NOT edit the ccsession launcher in this change. | containment 0.75 | Task 6 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:5 |
| INF-013 | This change must deliver, for that follow-up, the exact edit as a writ | containment 0.6667 | Task 9 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:5 |
