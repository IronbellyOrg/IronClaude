# Reviewer 1 brief (persona: analyzer: audit the plan for wrong assumptions about the repo, behaviour changes the plan does not state, and defects in task logic)

## T1 card excerpt

(verbatim slice of .dev/reflect/pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821/t1-card.md)

#### Deviation and risk findings (plan vs repo)

- R-1 (grounded, Medium) Task 5 (plan lines 78-86) renames the retry-ladder variables to the names the workspace exports. `/etc/aidev02/aienv.d/defaults.sh` exports T3Model01, T2Model01, T2Model02, T1Model01 and T1Model02, so after the rename the primary ladder in `src/superclaude/skills/sc-implement-protocol/refs/retry.md` (line 162: "active only when the four rung variables are all set") becomes active in Coder workspaces for the first time. That is a behaviour change of /sc:implement escalation (adviser models, family rule). The task acceptance criteria check names and archive tests only; nothing records or tests the activation.
- R-2 (grounded, Low) Task 6 (plan lines 90-98) says sprint alternate-model suggestions "return nothing for tier-valued slots". In `src/superclaude/cli/sprint/aienv.py` (lines 111-153) the suggestion still works when the failed model is given as the alias (`opus` finds alias `opus`); it returns None only when the failed model is a real model id from a cooldown body (for example `claude-opus-5-5`) while the slot value is a tier id. The sentence in the reference page and the Task 8 test (plan lines 112-119) should say that precisely.
- R-3 (grounded, Low) Ordering: Task 2 (line 48) and Task 3 (line 58) write text that links to `docs/reference/model-aliases.md`, which Task 6 (line 90) creates. The end state is consistent; during Tasks 2-5 the link target does not exist yet.
- R-4 (grounded, Low) Task 1 (plan lines 28-44) lists a residual allow-list dict for AST hits; a repo scan of `src/superclaude/cli/**/*.py` string constants (non-docstring) finds exactly one hit, `src/superclaude/cli/reflect/commands.py:31`, so the residual dict will be empty and could be dropped to keep the test minimal.
- R-5 (grounded, Info) The plan does not touch `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:109`, which still says Coder workspaces no longer set the ANTHROPIC_DEFAULT_* variables; this workspace exports them. Out of the stated scope, candidate follow-up.


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

### src/superclaude/skills/sc-implement-protocol/refs/retry.md:162-164

```markdown
**Ladders.** Rungs are numbered weakest to strongest. The primary ladder (environment variables) is rung 0 `T3_Model01`, rung 1 `T2_Model02`, rung 2 `T1_Model02`, rung 3 `T1_Model01`, the top rung. `T2_Model01` is on par with `T2_Model02`: it is recognized as rung 1 only when matching the executor's own model id and is never used as an adviser. The primary ladder is active only when the four rung variables are all set and non-empty (`T2_Model01` is optional); otherwise the whole fallback ladder is active: rung 0 `haiku`, rung 1 `sonnet`, rung 2 `opus`, the top rung. The two ladders are never mixed.

**Executor tier.** A primary rung's model id is the variable's value with any trailing `[...]` suffix stripped (rung 1 also matches the value of `T2_Model01`, when set); a fallback rung's id is `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` when that variable is set, else the Claude model for that alias. The executor's tier is the rung of the active ladder whose id equals the executor's own model id as its system prompt states it, both compared with any trailing `[...]` suffix stripped. No exact match → tier unknown. The tier is recorded as `tier=` (the canonical name of the executor's rung: `T2_Model02` for an executor on either T2 model, otherwise the variable name or fallback alias; or `unknown`).
```

### /etc/aidev02/aienv.d/defaults.sh:22-31

```bash
export T1a_WINDOW=850000
export T1aModel01=claude-opus-5-5
export T1aModel01_WINDOW=850000
export T1aModel02=claude-sonnet-5-5
export T1aModel02_WINDOW=850000
export T1b_WINDOW=850000
export T1bModel01=claude-sonnet-5-5
export T1bModel01_WINDOW=850000
export T1bModel02=gpt-6.1-sol
export T1bModel02_WINDOW=850000
```

### /etc/aidev02/aienv.d/defaults.sh:66-71

```bash
export T1_WINDOW=850000
export T1Model01=claude-opus-5-5
export T1Model01_WINDOW=850000
export T1Model02=gpt-6.1-sol
export T1Model02_WINDOW=850000
export T1Model03=claude-sonnet-5-5
```

### src/superclaude/cli/sprint/aienv.py:111-153

```python
    items = list(_load_aliases(env).items())
    failed = _base_id(failed_model_or_alias)

    failed_idx: int | None = None
    for idx, (alias, resolved) in enumerate(items):
        if failed in (alias, _base_id(resolved)):
            failed_idx = idx
            break
    if failed_idx is None:
        # An unset Anthropic slot resolves inside Claude Code, so the cooldown
        # body carries the real id (``claude-opus-5-5``); match it by family.
        lowered = failed.lower()
        for idx, (alias, resolved) in enumerate(items):
            if resolved == alias and alias in lowered and lowered.startswith("claude"):
                failed_idx = idx
                break
    if failed_idx is None:
        return None

    failed_alias, failed_resolved = items[failed_idx]
    exhausted = {failed, _base_id(failed_resolved)}
    for alias, resolved in items[failed_idx + 1 :]:
        if resolved == alias and any(
            e.lower().startswith("claude") and alias in e.lower() for e in exhausted
        ):
            # An unset built-in (``haiku``) resolves inside Claude Code to its
            # family's model; skip it when that family is the exhausted one.
            continue
        candidate = _base_id(resolved).lower()
        if (
            failed_resolved == failed_alias
            and candidate.startswith("claude")
            and failed_alias in candidate
        ):
            # The exhausted model is an unset built-in (``opus``), resolved by
            # Claude Code to its family's model; a slot pinned to that family's
            # id is the same model.
            continue
        if alias != failed_alias and _base_id(resolved) not in exhausted:
            # ``claude --model`` understands opus/sonnet/haiku but not a slot
            # NAME such as ``T2Model02``; for proxy slots hand back the model id.
            return resolved if alias.startswith(T2_MODEL_ENV_PREFIX) else alias
    return None
```

### src/superclaude/cli/reflect/commands.py:26-31

```python
# Top-level orchestrator model for the headless ``claude --print`` run. The
# spec Section 9 option set is exact (no ``--model`` flag), so the model is
# sourced from the ``ANTHROPIC_MODEL`` env var with a default fallback; the
# Tier-2 reviewer diversity comes from the ``ANTHROPIC_DEFAULT_*`` aliases, not
# this value. (Flagged decision -- see Task Log.)
_DEFAULT_MODEL = "claude-opus-4-8"
```

### src/superclaude/cli/reflect/commands.py:359-359

```python
    model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:28-44

```markdown
## Task 1: Add the alias-only policy tests

Create tests/skills/test_model_alias_policy.py (ROOT = Path(__file__).resolve().parents[2], like tests/skills/test_issue_worker_agents.py, which also shows how agent frontmatter is parsed). Define ALIASES = opus, sonnet, haiku, inherit and an allow-list written as named constants with a one-line reason each: the three issue-worker agents (value must equal their pinned claude-gw-tier3 / claude-gw-tier2 / claude-gw-tier1a; reason: they stop with E-TIER-UNAVAILABLE outside a ccsession tier workspace, see src/superclaude/skills/sc-issue-protocol/refs/tiers.md) and the paths allowed to contain the text claude-gw-tier (those three agent files, everything under src/superclaude/skills/sc-issue-protocol/, src/superclaude/commands/issue.md, and src/superclaude/skills/ccsession-tag/ which is read-only here). Tests, each with a docstring naming the rule:

- Frontmatter `model:` of every file in src/superclaude/agents/*.md and src/superclaude/skills/*/SKILL.md is in ALIASES, except the allow-listed issue workers.
- The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in allow-listed paths.
- No non-docstring string constant in any src/superclaude/cli/**/*.py module (parsed with ast; comments and docstrings are skipped) matches `^claude-(opus|sonnet|haiku|fable)-\d`; a residual allow-list dict (path to reason) exists for any legitimate hit found when the test first runs.
- superclaude.cli.reflect.commands._DEFAULT_MODEL is in ALIASES.
- The brainstorm steps in src/superclaude/skills/sc-issue-protocol/refs/chains.md contain no `--models` flag.
- src/superclaude/agents/audit-scanner.md pins `model: sonnet`, and neither src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md nor src/superclaude/commands/cleanup-audit.md contains the word Haiku.
- Neither src/superclaude/skills/sc-implement-protocol/refs/retry.md nor refs/ledger.md, nor their copies under plugins/superclaude/skills/sc-implement-protocol/refs/, contains a name matching `T[0-4]_Model`, and retry.md names the primary-ladder variables T3Model01, T2Model02, T1Model02 and T1Model01.
- docs/reference/model-aliases.md exists and states the three exports with the exact ids ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2; and tier1a, tier1b and tier2 are keys of "tiers" in src/superclaude/skills/ccsession-tag/ccsession-models.json (read only).

Acceptance criteria:
- tests/skills/test_model_alias_policy.py exists and `uv run pytest tests/skills/test_model_alias_policy.py` run on the unchanged tree fails exactly these tests: the Python constants test, the reflect default test, the chains test, the cleanup-audit test, the retry names test and the mapping document test; the remaining tests pass. The pytest output is saved to ./artifacts/t1-red.log.
- Every failing test fails for the stated reason (for example the Python constants test reports src/superclaude/cli/reflect/commands.py and claude-opus-4-8), not an import or collection error.
- `uv run ruff check tests/skills/test_model_alias_policy.py` and `uv run ruff format --check tests/skills/test_model_alias_policy.py` pass.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:78-86

```markdown
## Task 5: Rename the implement retry-ladder variables to the names the workspace exports

Depends on: Task 1

The workspace exports T3Model01, T2Model01, T2Model02, T1Model01 and T1Model02 (no underscore); src/superclaude/skills/sc-implement-protocol/refs/retry.md (lines 162-172) names T3_Model01, T2_Model02, T1_Model02, T1_Model01 and T2_Model01, so the primary ladder never activates. In retry.md replace each underscore name with the exported name (T3_Model01 to T3Model01, T2_Model01 to T2Model01, T2_Model02 to T2Model02, T1_Model01 to T1Model01, T1_Model02 to T1Model02) including the tier-token wording at line 164 and the example at line 172, and add one sentence in the Ladders paragraph saying these are the tier slot variables exported by the workspace environment and that the fallback ladder (haiku, sonnet, opus) applies when they are not all set. In src/superclaude/skills/sc-implement-protocol/refs/ledger.md change the example `tier=T2_Model02` (line 200) to `tier=T2Model02`. Copy both edited files over plugins/superclaude/skills/sc-implement-protocol/refs/retry.md and plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md. In tests/skills/test_workflow_archive.py change the RUNGS entries (lines 774-777) and the tier value in _rt (line 786) to the new names, and in tests/skills/test_task_workspace_lifecycle.py change the assertion at line 597 (`T2_Model01` is on par) to the new name. src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py already accepts `[A-Za-z0-9_]+` for the tier token and needs no change.

Acceptance criteria:
- `grep -rnE "T[0-4]_Model0" src plugins tests docs` returns nothing, and `cmp` shows the two mirrored files identical to their src counterparts.
- The retry names test of tests/skills/test_model_alias_policy.py passes; `uv run pytest tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_adviser_family.py` passes; evidence saved to ./artifacts/t5-test.log.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:90-98

```markdown
## Task 6: Write the model-alias reference page

Depends on: Task 1

Create docs/reference/model-aliases.md and add a line for it to the index in docs/reference/README.md. Sections: what a primitive may name (plain aliases only; the issue-worker allow-list and why; the test tests/skills/test_model_alias_policy.py enforces it); the mapping table (opus to claude-gw-tier1a via ANTHROPIC_DEFAULT_OPUS_MODEL, sonnet to claude-gw-tier1b via ANTHROPIC_DEFAULT_SONNET_MODEL, haiku to claude-gw-tier2 via ANTHROPIC_DEFAULT_HAIKU_MODEL inside a ccsession tier workspace; outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning), stating the mapping is owner-decided on 2026-11-05 and is applied by the ccsession launcher in a follow-up change; why aliases and not picker ids (frontmatter model takes an alias, a full model id or inherit with no environment lookup; the Agent-call model parameter takes only sonnet, opus, haiku and fable; source https://code.claude.com/docs/en/sub-agents read 2026-11-05) and the verified behaviour (with ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a and ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2, a subagent with model: opus ran on claude-gw-tier1a and one with model: haiku on claude-gw-tier2 while the main session kept its own model; Claude Code logs an unrecognized_model notice but serves the request); and a Known consequences section: reflect reviewer diversity counts the three variable values (tier1a and tier1b both list Claude Sonnet 5.5 in src/superclaude/skills/ccsession-tag/MODEL-TIERS.md), sprint alternate-model suggestions return nothing for tier-valued slots (src/superclaude/cli/sprint/aienv.py), roadmap step ids such as generate-opus-architect and recommend best_model values stay unchanged because the aliases stay, and today the workspace defaults file exports real model ids for the three variables until the launcher change lands.

Acceptance criteria:
- docs/reference/model-aliases.md exists with the sections above and the three exports spelled exactly as in the mapping table; docs/reference/README.md links to it.
- The mapping document test of tests/skills/test_model_alias_policy.py passes; the markdown contains no secrets or tokens; evidence saved to ./artifacts/t6-test.log.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:112-119

```markdown
## Task 8: Add characterization tests for tier-valued alias variables

Depends on: Task 6

Add tests that pin today's behaviour when the three variables hold tier ids, so the launcher change cannot silently alter it: in tests/sprint/test_aienv.py (existing tests there show the `env=` seam of suggest_alternate_model) assert that with ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b and ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2 the function _load_aliases returns those ids unchanged under the keys opus, sonnet and haiku, and that suggest_alternate_model("claude-opus-5-5", env=that env) returns None (never a fabricated alias). In the existing test module for superclaude.cli.reflect.runner.count_model_aliases (search tests/ for count_model_aliases) assert that the same env gives a count of 3. Each test docstring says it records current behaviour and points to the Known consequences section of docs/reference/model-aliases.md.

Acceptance criteria:
- The three new tests pass on unchanged production code, and `uv run pytest tests/sprint/test_aienv.py` and the reflect test module that holds the count test pass; evidence saved to ./artifacts/t8-test.log.
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
