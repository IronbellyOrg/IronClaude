## T1 card excerpt
```text
# Tier 1 pre-execution reflection card

## Coverage
Two tasks; zero regex requirement IDs, 21 quote-pinned inferred rows. Deterministic containment matches 13/21 (coverage_pct=null; coverage_pct_union=0.6190; S_dev_density=0.380952). Unmatched rows: INF-001, INF-011, INF-016, INF-017, INF-018, INF-019, INF-020, INF-021. See artifacts/coverage-matrix.json for exact words, ratios and matches, and artifacts/coverage-analysis.md for the separate semantic analysis. Global constraints and plan shape are intentionally not folded into either task for matching; this lowers lexical coverage without proving eight substantive omissions. The parsed-sparse pre-filter independently requires Tier 2. The analyst found no blocking omission and six wording/context notes, pending ensemble adjudication. In particular, the explicit New Terminal prohibition warrants adversarial checking against Task 1's global-selection rule and AC.

## Grounding
The proposed installer change addresses an existing early-return and missing propagation, not Orca shell causation. In `src/superclaude/cli/install_user_setup.py:230-243`, the helper has only home/deadline parameters and returns immediately when all three skills exist. In `src/superclaude/cli/install_user_setup.py:434-444`, the enclosing setup receives force but calls the Orca helper with deadline only. The captured process result is checked for return code and file presence without relaying stdout/stderr at `src/superclaude/cli/install_user_setup.py:245-263`.

Existing tests in `tests/cli/test_install_user_setup.py:247-308` cover absent Orca, wrong executable, initial installation, repeat skip, and timeout, but do not exercise a force argument. These are baseline source observations, not observed test passes or newly run red tests.

## Risks and boundaries
The existing helper's return value is a nonfatal boolean plus message; changing that contract or treating guide presence as a successful refresh would violate the proposed safe-refresh boundary. Preserve both positional home/deadline callers, the three-skill list and timeouts. The plan already requires these checks. New guidance must not replace supervised worker-start authority or internal Agent-tool subagents. Static document tests cannot prove UI launch success. Read-only Orca discovery in artifacts/orca-discovery.md supports the agent-launch versus shell distinction and safe installer semantics; no launch or install was run. No new abstraction or standalone component is proposed, so implementor and neighbour-search checks have no applicable new component. Auggie codebase-retrieval is not available in this session; native Read/Grep and a fresh codegraph index supplied grounding. Executor identity and actual gateway vendor diversity remain unresolved; report those limitations rather than claim complete model independence.

## Provisional findings
Grounding confirms the plan targets existing instruction-delivery and safe-refresh gaps. No implementation has been performed and no current defect is classified as a post-execution Regression. Final plan verdict remains pending the requirements extraction and independent reviewers. The planned changes span code, documentation and tests (three domains), so Tier 2 is required by rubric rule 4 independent of confidence. No depth or tier override was supplied to reflect; the plan's own quick depth does not pin this review.

## Recommendations
Keep the original two-task plan unchanged during this advisory run. Resolve any confirmed blocking coverage defect before execution, with verification against the byte-exact source and the affected acceptance criterion. Do not treat baseline lint or static instruction checks as runtime incident reproduction. Preserve the source's no-overwrite and no-external-force boundaries; read artifacts/orca-discovery.md for the actual normal-install safety statement rather than speculate that normal Orca installation overwrites edited guides. Execution is outside this review's authorization, regardless of the source's future-execution sentence.
```


## Grounding hunks
codegraph run state: index_state=fresh checked_at=2026-11-06T21:59:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/fix-claude-cli-session-launch projectPath=/home/coder/workspaces/worktrees/IronClaude/fix-claude-cli-session-launch

Persona: analyzer. UC-1 proposed plan review only, not a completed-work audit. No shell, git, writes, execution or remediation. Return findings to parent for persistence. Assume errors; report PASS or FAIL, blocking versus minor, plus Self-Audit if no blocking findings. Do not treat a speculative execution mistake as an actual plan contradiction.

### .dev/tasks/to-do/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md:1-52
```text
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-fixIssue412SVeri-20261106-215543
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Correct Claude CLI session launch guidance

Source: ./source.md
Goal: New ccsession-backed Claude sessions are explicitly directed to Orca's Claude (CLI) agent route, and forced IronClaude setup requests a safe refresh of existing Orca guides.

## Constraints

- Fix only issue #412. Its existing issue body already references verified IronClaude refresh-introducing PR #245 and intentional Orca CLI-label PR #29074. Do not create another issue or claim that the label PR changed shell startup. Runtime incident causation remains UNDETERMINED; diagnostic closure remains advisory.
- No commit, push, PR, global install or other-repository mutation. Orca source/history stays read-only. No new dependency or launch wrapper.
- Canonical edits are under src/superclaude and tests. Run make sync-dev and make verify-sync after changes. Never stage generated .claude mirrors. Always stage .dev/tasks packages and artifacts.
- Supervised workers keep the dispatch preamble and worker-start authority. Internal Agent-tool subagents remain internal. Ordinary agent launch is not a substitute for supervised worker dispatch.
- IronClaude force means request Orca's normal safe installation. Never pass Orca --force, replace edited guides, change Claude executable settings or make plain shell terminals start an agent.
- Installed Orca help defines update behavior; existing owned unmodified copies may update, edited or foreign copies may be skipped. Meaningful installer output must remain visible. Do not treat a safe skip as proof that the guide refreshed.

## Phase 1: Explicit session selection

## Task 1: Add canonical launch instructions and a regression check

Inputs: the explicit launch requirement in source.md, src/superclaude/core/CLAUDE.md, src/superclaude/skills/ccsession-tag/README.md, and the current installed orca-cli guide. Add a concise global selection rule and matching launcher README passage. Add tests/core/test_orca_session_launch_guidance.py using existing pytest static-document conventions. Test the absence before editing the two instruction files, then apply the instructions. Preserve Settings > Agents > Claude > Command configuration of ccsession-orca and distinguish a Claude CLI agent from an ordinary shell.

Outputs: the two canonical instruction files and runnable guidance checks; save observed failing/passing output under ./artifacts/t1-tests.log. No runtime Orca change is authorized.

Acceptance criteria:
- Both instruction surfaces explicitly distinguish Claude (CLI) for ccsession-backed Claude sessions from New Terminal and terminal create for shells, and identify agent launch and worktree create --agent as programmatic agent creation routes after loading the version-matched Orca guide. Explicit terminal surface is named only when a CLI session is required.
- Both surfaces preserve supervised worker-start/preamble authority and internal Agent-tool subagents. README retains the ccsession-orca executable configuration prerequisite rather than claiming every agent launch automatically uses ccsession.
- The new guidance tests are observed failing against the original instruction files and passing after the bounded edit. They check the shell/CLI distinction and supervised/internal-agent boundaries, not UI runtime success. Evidence records that scope honestly.

## Phase 2: Safe guide refresh

## Task 2: Propagate forced setup refresh with regression checks

Depends on: Task 1

Inputs: source.md's safe-refresh requirement, src/superclaude/cli/install_user_setup.py helper and caller, tests/cli/test_install_user_setup.py, and installed orca-ide skills install --help. Add a backward-compatible force argument to install_orca_skills and pass the enclosing install_user_setup force intent. Existing files may short-circuit only when force is false. A forced request uses the normal safe Orca install command, without external --force. Preserve the current executable identification, deadline, absent/failed-Orca nonfatal behavior and three-skill list. Relay meaningful Orca stdout/stderr so edited/foreign guide skips cannot be hidden by an unconditional success summary; reuse existing result fields without a new parser. Add minimal tests for helper refresh, top-level propagation, safe default skip, surfaced skip/failure output and nonfatal absence/failure with existing guides.

Outputs: the canonical helper/caller and matching tests; observed red/green and wider regression output under ./artifacts/t2-tests.log. Run synchronization and record its output in ./artifacts/sync.log as part of delivering the changed skill README, without staging mirrors.

Acceptance criteria:
- A forced user-setup request reaches normal Orca guide installation even with all three files present, and top-level force propagation is covered. Nonforce repeated setup still skips existing guides with no Orca calls. The external command never gains --force and existing edited-guide contents are not rewritten by IronClaude.
- Absent Orca, timeout, nonzero installation result or incomplete installation remains nonfatal and accurately reported. Meaningful skipped/warning output from Orca is surfaced, including when files already exist; tests cover those cases without network or global writes.
- New refresh regression checks fail before the implementation and pass afterwards. The related installer tests, tests/unit/test_cli_install.py, guidance tests and tests/core/test_claude_md_routing_block.py pass. Ruff on changed Python files and make sync-dev plus make verify-sync succeed. Logs distinguish mocked installer checks from actual Orca dry-run evidence; no live guide refresh or UI reproduction is claimed.
```
### src/superclaude/cli/install_user_setup.py:230-263
```text
def install_orca_skills(
    home: Path | None = None, deadline: float | None = None
) -> Tuple[bool, str]:
    """Ask Orca to install its skills for Claude Code; never fails the install."""
    home = Path.home() if home is None else Path(home)
    skills_dir = home / ".claude" / "skills"
    if all((skills_dir / name / "SKILL.md").exists() for name in _ORCA_SKILLS):
        return True, "✅ Orca skills: already installed"
    orca = _find_orca()
    if orca is None:
        return True, "⏭️  Orca skills: Orca CLI not found; skipped"
    command = [orca, "skills", "install", "--agent", "claude-code"]
    for name in _ORCA_SKILLS:
        command += ["--skill", name]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=_orca_timeout(deadline),
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return (
            True,
            f"⚠️  Orca skills: not installed ({exc}); rerun `{orca} skills install`",
        )
    installed = [n for n in _ORCA_SKILLS if (skills_dir / n / "SKILL.md").exists()]
    if result.returncode != 0 or len(installed) != len(_ORCA_SKILLS):
        return True, (
            f"⚠️  Orca skills: installed {len(installed)}/{len(_ORCA_SKILLS)}; "
            f"rerun `{orca} skills install`"
        )
    return True, f"✅ Orca skills: {', '.join(installed)}"
```
### src/superclaude/cli/install_user_setup.py:434-444
```text
def install_user_setup(force: bool = False) -> Tuple[bool, str]:
    """Run every user-setup step; returns combined success and messages."""
    deadline = time.monotonic() + _NETWORK_BUDGET
    results = [
        install_rules(force=force),
        install_output_styles(force=force),
        apply_settings_defaults(),
        install_orca_skills(deadline=deadline),
        install_plugins(deadline=deadline),
    ]
    return all(ok for ok, _ in results), "\n".join(msg for _, msg in results)
```
Read-only Orca discovery (artifacts/orca-discovery.md): version-matched guide names agent launch/worktree create --agent as agent routes and terminal create as shells/commands; explicit surface selects chat or terminal. Installed installer help states only Orca-owned unmodified copies update; edited/foreign copies are skipped and reported unless external --force is used. No actual installation was invoked.


## Coverage slice
| Requirement | Verbatim source quote | Deterministic match | Ratio |
|---|---|---|---|
| INF-001 | Fix issue #412's verified instruction-delivery gaps, not Orca shell behavior. | none | 0.272727 |
| INF-002 | Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance | Task 1 | 0.875 |
| INF-003 | new ccsession-backed Claude sessions use Claude (CLI), never New Terminal | Task 1 | 0.777778 |
| INF-004 | programmatic creation uses the version-matched Orca agent launch or worktree create --agent | Task 1 | 1.0 |
| INF-005 | explicit terminal surface when CLI required | Task 1 | 1.0 |
| INF-006 | Reserve terminal create for shells. | Task 1 | 0.75 |
| INF-007 | Preserve supervised worker-start/dispatch-preamble rules and internal Agent-tool subagents. | Task 1 | 0.818182 |

13/21 lexical matches overall. Zero parsed IDs, 21 inferred rows; parsed-sparse. Shared constraints are outside the task-only matcher. Lexical misses are not by themselves proven missing requirements. Inspect original source and constraints before grading a gap.

