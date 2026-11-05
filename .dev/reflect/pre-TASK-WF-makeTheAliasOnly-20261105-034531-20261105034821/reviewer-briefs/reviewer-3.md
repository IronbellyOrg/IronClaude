# Reviewer 3 brief (persona: refactorer: audit task ordering, dependencies, duplication and scope creep; check every helper, file and line the tasks name actually exists)

## T1 card excerpt

(verbatim slice of .dev/reflect/pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821/t1-card.md)

#### Recommendations

- A-1 Add to Task 5's acceptance criteria a note artifact `./artifacts/t5-notes.md` stating that the primary ladder now activates when all four variables are set, with the one-line effect on adviser selection, so the PR description can carry it.
- A-2 Reword the sprint-suggestion sentence in Task 6 and the matching Task 8 assertion as in R-2.
- A-3 No change needed for R-3, R-4, R-5 (record as notes).


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

### tests/unit/test_ccsession_tiers.py:301-330

```python
def _launch(
    tmp_path: Path, *args: str, defaults: str | None = TIER_BLOCK, **extra: str
):
    """Run ccsession with a fake claude and a fake running shim; return (rc, out, err, seen)."""
    env = _launch_env(tmp_path, defaults, **extra)
    proc = subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    seen = (
        json.loads((tmp_path / "seen.json").read_text())
        if (tmp_path / "seen.json").exists()
        else None
    )
    return proc.returncode, proc.stdout, proc.stderr, seen


def _launch_env(
    tmp_path: Path, defaults: str | None = TIER_BLOCK, **extra: str
) -> dict[str, str]:
    """The environment of _launch: a fake claude that writes seen.json and a fake running shim."""
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    fake_claude = tmp_path / "claude"
    fake_claude.write_text(
        """#!/usr/bin/env python3
```

### tests/unit/test_ccsession_tiers.py:386-410

```python
def _compact(seen: dict, model: str) -> int:
    """The auto-compact window ccsession passed for one model (--settings)."""
    settings = json.loads(seen["settings"])
    return settings["modelSettings"][model]["autoCompactWindow"]


def _model_arg(seen: dict) -> str:
    argv = seen["argv"]
    return argv[argv.index("--model") + 1]


def test_default_tier_sets_model_and_tier_window(tmp_path: Path) -> None:
    rc, out, err, seen = _launch(tmp_path, "work")
    assert rc == 0, err
    assert _model_arg(seen) == "claude-gw-tier2[1m]"
    assert seen["context"] == "500000"
    # One window per tier and model, so a /model switch takes the new
    # tier's window; no env value pins one window for the whole session.
    assert seen["compact"] == ""
    assert _compact(seen, "claude-gw-tier2") == 500000
    assert _compact(seen, "claude-gw-tier1a") == 850000
    assert seen["custom"] == ""  # tiers are already in the picker
    assert seen["base_url"] == "http://127.0.0.1:4555"  # shim is always on
    assert "tier2" in out and "muse-spark-1.3" in out

```

### tests/skills/test_workflow_archive.py:771-790

```python
# --- retry / halt ledger records -------------------------------------------------
CK = "a" * 40
RUNGS = [
    "T3_Model01",
    "T2_Model02",
    "T1_Model02",
    "T1_Model01",
    "haiku",
    "sonnet",
    "opus",
]
BRIEF3 = "./artifacts/retries/T1_brief-3.md"


def _rt(n=3, **kw):
    f = {"checkpoint": CK, "tier": "T2_Model02", "brief": BRIEF3, "supersedes": "none"}
    f.update(kw)
    return {
        "open": f"T1: retry n={n} step=open checkpoint={f['checkpoint']} tier={f['tier']}",
        "revert": f"T1: retry n={n} step=revert brief={f['brief']} supersedes={f['supersedes']}",
```

### src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py:55-62

```python
_RETRY = re.compile(
    rf"^T({TASK_ID}): retry n=([345]) "
    r"(?:step=open checkpoint=([0-9a-f]{40}) tier=([A-Za-z0-9_]+)"
    r"|step=revert brief=(\S+) supersedes=(T[0-9A-Za-z.-]+_brief-[34]\.md|none)"
    r"|step=review)$"
)
_HALT = re.compile(rf"^T({TASK_ID}): halt review=([2-5]) reason=([a-z][a-z-]*)$")
_LEGACY_BRIEF = re.compile(
```

### docs/reference/README.md:1-25

```markdown
# Reference Documentation

This folder holds reference material: troubleshooting guides, diagnostic procedures, and format contracts. It does not tell you which command to use for a job; for that, read [How We Work](../user-guide/how-we-work.md), or run `/sc:recommend "<what you want to do>"`. For the syntax of each command, see the [Commands Reference](../user-guide/commands.md).

## Troubleshooting

| Document | Use it when |
|---|---|
| [common-issues.md](./common-issues.md) | You hit a frequent problem and want the quick fix |
| [troubleshooting.md](./troubleshooting.md) | The quick fixes did not work and you need a step-by-step diagnosis |
| [diagnostic-reference.md](./diagnostic-reference.md) | You need to check installed context files and configuration by hand |
| [mcp-server-guide.md](./mcp-server-guide.md) | An MCP server will not start, connect, or respond |

## Contracts and design notes

| Document | What it defines |
|---|---|
| [deviation-report-format.md](./deviation-report-format.md) | The deviation report schema that pipeline gates and CLI commands read |
| [nfr-conv-2-prose-determinism.md](./nfr-conv-2-prose-determinism.md) | Where task-builder output must be deterministic and where prose may vary |
| [pm-agent-autonomous-reflection.md](./pm-agent-autonomous-reflection.md) | How the PM agent reflects on its own work and saves tokens |
| [claude-code-history-management.md](./claude-code-history-management.md) | How Claude Code stores conversation history and how to rotate it |
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

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:58-66

```markdown
## Task 3: Drop the haiku workaround from the issue chains

Depends on: Task 1

In src/superclaude/skills/sc-issue-protocol/refs/chains.md remove ` --models opus,sonnet` from the three brainstorm steps in the table rows for Feature simple, Feature medium and Feature complex (lines 11-13), and replace the note at line 21 (the bullet that begins with /sc:brainstorm --models defaults) with a bullet that says: the brainstorm rows use the default models opus,sonnet,haiku; inside a ccsession tier workspace these resolve to claude-gw-tier1a, claude-gw-tier1b and claude-gw-tier2, outside one to Claude Code's own models; see docs/reference/model-aliases.md. In tests/skills/test_issue_protocol.py rename test_brainstorm_steps_have_no_handoff_and_pin_models (lines 268-282) to test_brainstorm_steps_have_no_handoff_and_use_default_models and replace `assert "--models opus,sonnet" in step` with an assertion that `--models` is not in the step. In docs/designs/sc-issue-command.md add a note "Superseded by #384: the chains use the default models; see docs/reference/model-aliases.md" to the D25 row (about line 442) and to the bullet at about line 237 that explains the workaround; leave the rest of that design record unchanged.

Acceptance criteria:
- `grep -n "models opus,sonnet" src/superclaude/skills/sc-issue-protocol/refs/chains.md` returns nothing and the six chain rows still parse (the existing chain tests in tests/skills/test_issue_protocol.py pass).
- The chains test of tests/skills/test_model_alias_policy.py passes; `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py` passes; evidence saved to ./artifacts/t3-test.log.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:100-108

```markdown
## Task 7: Point the existing model pages at the reference page

Depends on: Task 6

Edit src/superclaude/skills/sc-issue-protocol/refs/tiers.md: in item 4 of the list under "Why the pin lives in frontmatter" (line 26) replace the claim that haiku resolves to glm-5.3 on this workspace with the statement that the haiku alias follows ANTHROPIC_DEFAULT_HAIKU_MODEL and, inside a ccsession tier workspace, resolves to claude-gw-tier2 once the launcher sets it, and add one sentence under "E-TIER-UNAVAILABLE" (after line 40) that the issue workers are the only primitives pinned to picker ids and all other primitives use aliases (docs/reference/model-aliases.md). In docs/user-guide/brainstorm.md extend the `--models` row (line 52) with: inside a ccsession tier workspace opus, sonnet and haiku resolve to claude-gw-tier1a, claude-gw-tier1b and claude-gw-tier2; see docs/reference/model-aliases.md. In docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md add a short note, in the section that describes agent frontmatter if one exists (find the heading that mentions frontmatter or the `model` field), that agent `model:` must be an alias unless it is an allow-listed issue worker, with a link to docs/reference/model-aliases.md; if the guide has no such section, record that in ./artifacts/t7-notes.md and skip this file.

Acceptance criteria:
- src/superclaude/skills/sc-issue-protocol/refs/tiers.md no longer says the haiku alias resolves to glm-5.3 as a fixed fact, and still passes `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py`.
- docs/user-guide/brainstorm.md and the developer guide (or ./artifacts/t7-notes.md explaining the skip) carry the pointer; every added link target exists in the repository.
```

### .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/TASK-WF-makeTheAliasOnly-20261105-034531.md:121-129

```markdown
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
| INF-007 | the haiku workaround --models opus,sonnet in skills/sc-issue-protocol/ | containment 0.875 | Task 3 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-008 | the audit-scanner Haiku-versus-sonnet contradiction (skills/sc-cleanup | containment 0.8235 | Task 4 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-009 | the T1_Model01-style env names in skills/sc-implement-protocol/refs/re | containment 0.75 | Task 5 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-010 | plus the plugins/superclaude mirror copies of any edited file | containment 0.6667 | Task 1 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-011 | update any existing test that pins an edited string | none 0.5 | Task 1 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:1 |
| INF-012 | Do NOT edit the ccsession launcher in this change. | containment 0.75 | Task 6 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:5 |
| INF-013 | This change must deliver, for that follow-up, the exact edit as a writ | containment 0.6667 | Task 9 | .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-034531/source.md:5 |
