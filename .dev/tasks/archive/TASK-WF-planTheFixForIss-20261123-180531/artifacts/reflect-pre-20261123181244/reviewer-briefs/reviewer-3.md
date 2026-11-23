# Reviewer 3, refactorer, pre-execution

## T1 card excerpt
Task3 owns the high-blast-radius shared builder and explicitly restricts default behavior to refactor-find, protects caller substitutions/templates, statuses, sibling lens mappings and resume. It requires real stub output plus partial-worker and path/override cases. Task2 intentionally does not claim full repair after a template-only change. Task4 updates current matching documentation, not historical records. A real repaired CLI artifact is required before fix acceptance. These are plan obligations, not observed passing runs.

## Grounding hunks
codegraph run state: index_state=fresh checked_at=2026-11-23T18:12:44Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s projectPath=/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s

### docs/swarm/README.md:67
```text
| `refactor-find` | 3 | `findings_table_v1` | experimental | no | `/sc:code-review` |
```
### docs/swarm/lens-catalog.md:25
```text
| [`refactor-find`](#refactor-find) | 3 | `findings_table_v1` | experimental | T2-code | — | `/sc:code-review --apply {compare_files}` |
```
### docs/swarm/lens-catalog.md:47-49
```text
The smallest cleanups that improve correctness, readability, or efficiency. Recipe
`findings_table_v1` → `| ID | Locator | Finding | Detail | Action |`. Hands off to
`/sc:code-review`.
```
### docs/swarm/user-guide.md:200
```text
| Code, for the smallest worthwhile cleanups | `refactor-find` | findings table | `/sc:code-review` |
```
Full plan .dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-180531/TASK-WF-planTheFixForIss-20261123-180531.md, source at sibling source.md. Read both. Root is current user worktree, reviewer_isolation=disabled. Scope: proposed plan only; no product fix expected in this audit. Check two-source-file boundary, practical task dependencies, minimal reuse and matching docs. No new component/framework is requested. No out-of-scope improvements. Inspect concrete errors that change a named decision/required behavior/check, missing requested deliverables or safety. Return full card with binary PASS/FAIL, Blocking Decision/Missing/Safety or minor Medium/Note and label HIGH/MEDIUM/LOW. No invented findings. State checked scope/reason if zero. No commands, writes, skills, agents or external model runs; parent persists your returned card. All future test/repair evidence remains future, not a missing current deliverable.

## Coverage slice
Own INF004 matching documentation and cross-task change sizing/dependencies. Machine INF004->Task4 ratio0.6667. Four phases/tasks, Task1 failing regression, Task2 lens template, Task3 argument list/preservation plus acceptance evidence, Task4 docs. Raw eight quotes and machine matrix in parent of brief folder. Analyst note about docs/swarm/wizard-guide.md:216 was nonblocking: broad lens-agnostic list, not a fifth verified refactor-specific occurrence. Judge from live source, not that note. Do not penalize lexical matching misses as semantic omissions; no stemming matcher has union0.5.
