# Reviewer 2, qa, pre-execution

## T1 card excerpt
The plan includes an actual failing-before check (Task1), separate template change (Task2), real accepted-file output/override tests plus repaired CLI capture (Task3), and current matching docs (Task4). No regression has been authored/executed in this planning run. Tier2 required by parse-density pre-filter and three domains, not a confidence-based optional stop.

## Grounding hunks
codegraph run state: index_state=fresh checked_at=2026-11-23T18:12:44Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s projectPath=/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s

### .dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-180531/source.md:1
```text
Plan the fix for issue 501: replace refactor-find's unavailable /sc:code-review --apply follow-up with /sc:adversarial --compare. Supply actual generated report filenames for refactor-find only, preserving other review modes and explicit caller overrides. Update the matching documentation. Include a regression test that fails before the fix and passes afterward, checking the complete suggested command and accepted report inputs. Carry forward the requirement to verify the repaired output; diagnosis alone is not fix acceptance. Do not implement, commit or push.
```
### src/superclaude/commands/adversarial.md:15
```text
- Mode A: `--compare file1,file2[,...,fileN]` (2-10 existing files)
```
### tests/swarm/test_commands_run.py:529-542
```python
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )
```
Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Full plan is .dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-180531/TASK-WF-planTheFixForIss-20261123-180531.md; Read directly. Review proposed work only. No repaired-state artifacts are expected yet. No current verification-results hunk because mode pre runs no tests. Read requirements.json and coverage-matrix.json in parent of brief folder. Four tasks; eight inferred rows, zero parsed IDs. Machine coverage0.5, no stemming; coverage misses are lexical, not proof of missing behavior. Binary PASS/FAIL, graded Blocking Decision/Missing/Safety versus minor Medium/Note, labels HIGH/MEDIUM/LOW. Find concrete broken requirements/acceptance behavior, not preference gaps or quotas. Report checked scope/reason if zero. Return complete card, parent owns persistence. No writes, commands, skills, agents or external model runs. Grounding root is live current user worktree, reviewer_isolation=disabled.

## Coverage slice
Own all8 source clauses, especially INF005 red/green regression, INF006 complete command and accepted inputs, INF007 repaired output proof, INF008 plan-only authority. Machine matches: INF001->Task2;002->Task3;003 none;004->Task4;005 none;006->Task3;007 none;008 none. Semantic leads: Task1 lines37-39 and Task3 line67 red/green; Task3 lines60,69 overrides; Constraints19 no implementation/commit/push; Constraints25 and Task3 line71 repaired real CLI proof. Do not replace deterministic numbers. Check all source clauses for substantive coverage and plan feasibility.
