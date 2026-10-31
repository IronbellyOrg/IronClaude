cef3ae370d5998139f825e94b666fe89ef88b4fd
family=mirror-root-copy
defect form: a primitive sentence changed in src/ and plugins/ but not in its tracked root commands/sc-*.md copy
command: grep -n -F -e "Code-graph readiness" -e "Codegraph one-hop view" -e "Session context documentation and checkpoint creation" -e "Delegation for comprehensive explanation workflows" -- commands/sc-load.md commands/sc-explain.md src/superclaude/commands/load.md src/superclaude/commands/explain.md plugins/superclaude/commands/load.md plugins/superclaude/commands/explain.md
before:
commands/sc-load.md:46:- **Write**: Session context documentation and checkpoint creation
commands/sc-explain.md:43:- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
src/superclaude/commands/load.md:52:- **Write**: Session context documentation and checkpoint creation
src/superclaude/commands/load.md:53:- **Code-graph readiness**: end the session summary with one line telling the user to type `/sc:graph st
src/superclaude/commands/explain.md:50:- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
src/superclaude/commands/explain.md:51:- **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (limit
plugins/superclaude/commands/load.md:52:- **Write**: Session context documentation and checkpoint creation
plugins/superclaude/commands/load.md:53:- **Code-graph readiness**: end the session summary with one line telling the user to type `/sc:grap
plugins/superclaude/commands/explain.md:50:- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
plugins/superclaude/commands/explain.md:51:- **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (l
coupled sites: root copies of the other Task 12 files: none exist (git ls-files commands/ shows no sc-implement, sc-task, sc-pr-submit, sc-troubleshoot, sc-auggie-review copies of edited sentences; HOW-WE-WORK has no root copy)
after:
commands/sc-load.md:46:- **Write**: Session context documentation and checkpoint creation
commands/sc-load.md:47:- **Code-graph readiness**: end the session summary with one line telling the user to type `/sc:graph status` to see 
commands/sc-explain.md:43:- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
commands/sc-explain.md:44:- **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (limit 10) to find 
src/superclaude/commands/load.md:52:- **Write**: Session context documentation and checkpoint creation
src/superclaude/commands/load.md:53:- **Code-graph readiness**: end the session summary with one line telling the user to type `/sc:graph st
src/superclaude/commands/explain.md:50:- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
src/superclaude/commands/explain.md:51:- **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (limit
plugins/superclaude/commands/load.md:52:- **Write**: Session context documentation and checkpoint creation
plugins/superclaude/commands/load.md:53:- **Code-graph readiness**: end the session summary with one line telling the user to type `/sc:grap
plugins/superclaude/commands/explain.md:50:- **Task**: Delegation for comprehensive explanation workflows requiring systematic breakdown
plugins/superclaude/commands/explain.md:51:- **Codegraph one-hop view** (code targets only, when codegraph is usable): `codegraph_search` (l

family=degraded-copy
defect form: an /sc:impact caller that does not read or does not copy the degraded tokens into its own list
command: grep -n -F -e "sc:impact-protocol" -e "degraded" -- src/superclaude/skills/sc-implement-protocol/SKILL.md src/superclaude/skills/sc-pr-submit-protocol/SKILL.md src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md src/superclaude/skills/sc-auggie-review-protocol/SKILL.md src/superclaude/skills/sc-task-protocol/SKILL.md
before:
src/superclaude/skills/sc-implement-protocol/SKILL.md:121:             > Skill sc:impact-protocol
src/superclaude/skills/sc-implement-protocol/SKILL.md:122:           with `<symbol> --depth 1 --limit 10 --output-dir <ledger dir>/impact/<t
src/superclaude/skills/sc-implement-protocol/SKILL.md:133:           Advisory test list (optional extra): invoke `> Skill sc:impact-protocol
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:193:- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent 
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:206:1. **VG-1** targeted tests (`uv run pytest <changed-area>`). Advisory only: before
src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:57:> Skill sc:impact-protocol
src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:60:and read only `status`, `degraded`, `symbols[].prod.total`, `s
src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:62:transitive count, with `report_path`) and copy `degraded` into
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:32:- **No unrestricted fallback:** if the profile is missing or invalid, do not sub
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:254:| Auggie unavailable for any branch | Fall back to `Grep`/`Glob` against the br
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:318:| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per `refs/diagnosabili
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:588:     - **Phase A — Build the plan**: first, impact warning: invoke `> Skill s
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:658:| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality 
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:660:| auggie unavailable in Wave 1.5 (others OK) | Fall back to `Grep`/`Glob` again
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:663:| root-cause-analyst agent fails in Tier 1 | Skill produces a degraded Tier 1 (
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:674:| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per refs/diagnosabilit
src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:141:   > Skill sc:impact-protocol
src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:142:   with `--diff <base> --depth 1 --output-dir <output-dir>/inputs/impact --cal
src/superclaude/skills/sc-task-protocol/SKILL.md:94:   > Skill sc:impact-protocol
src/superclaude/skills/sc-task-protocol/SKILL.md:95:   with `<changed symbols> --depth 2 --output-dir .dev/impact/task-<slug> --caller sc-ta
coupled sites: implement Q1 (notes), implement Q6, pr-submit Wave 3 read list, pr-submit VG-1, plugin twin of the implement skill (byte copy)
after:
src/superclaude/skills/sc-implement-protocol/SKILL.md:121:             > Skill sc:impact-protocol
src/superclaude/skills/sc-implement-protocol/SKILL.md:122:           with `<symbol> --depth 1 --limit 10 --output-dir <ledger dir>/impact/<t
src/superclaude/skills/sc-implement-protocol/SKILL.md:133:           Advisory test list (optional extra): invoke `> Skill sc:impact-protocol
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:193:- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent 
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:206:1. **VG-1** targeted tests (`uv run pytest <changed-area>`). Advisory only: before
src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:57:> Skill sc:impact-protocol
src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:60:and read only `status`, `degraded`, `symbols[].prod.total`, `s
src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:62:transitive count, with `report_path`) and copy `degraded` into
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:32:- **No unrestricted fallback:** if the profile is missing or invalid, do not sub
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:254:| Auggie unavailable for any branch | Fall back to `Grep`/`Glob` against the br
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:318:| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per `refs/diagnosabili
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:588:     - **Phase A — Build the plan**: first, impact warning: invoke `> Skill sc:
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:658:| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality 
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:660:| auggie unavailable in Wave 1.5 (others OK) | Fall back to `Grep`/`Glob` again
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:663:| root-cause-analyst agent fails in Tier 1 | Skill produces a degraded Tier 1 (
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:674:| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per refs/diagnosabilit
src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:141:   > Skill sc:impact-protocol
src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:142:   with `--diff <base> --depth 1 --output-dir <output-dir>/inputs/impact --cal
src/superclaude/skills/sc-task-protocol/SKILL.md:94:   > Skill sc:impact-protocol
src/superclaude/skills/sc-task-protocol/SKILL.md:95:   with `<changed symbols> --depth 2 --output-dir .dev/impact/task-<slug> --caller sc-ta

family=group-comment-rows
defect form: a group comment that omits decision-log rows of its group
command: grep -n -F -e "| T12 |" -- .dev/codegraph-migration/decisions/P3X-execution-log.md
before:
68:| 2026-10-31 | T12 | sc-task-protocol's `/sc:impact` call replaces the inline `codegraph_impact` text in STRICT step 6, not step 7 | step
69:| 2026-10-31 | T12 | `/sc:impact` output paths use each caller's own placeholder: `<ledger dir>` (the package folder, or `.dev/implement/
70:| 2026-10-31 | T12 | troubleshoot calls `/sc:impact` only in the plan route's Phase A; the MDTM route (`--fix --depth deep`) Phase A is u
71:| 2026-10-31 | T12 | `/sc:load` only tells the user to type `/sc:graph status`; it never runs `/sc:graph` | run status from load; name it
72:| 2026-10-31 | T12 | `/sc:explain` gets the one-hop view in both copies; the existing one-line difference between the two `explain.md` co
73:| 2026-10-31 | T12 | `ruff format` reformatted the whole `tests/commands/test_impact_command.py`, including Task 9 lines (layout only) | 
coupled sites: .dev/codegraph-migration/progress/P3-F.md "Decisions made on my own" list; the posted comment 6545142355 (edited in place)
after:
68:| 2026-10-31 | T12 | sc-task-protocol's `/sc:impact` call replaces the inline `codegraph_impact` text in STRICT step 6, not step 7 | step
69:| 2026-10-31 | T12 | `/sc:impact` output paths use each caller's own placeholder: `<ledger dir>` (the package folder, or `.dev/implement/
70:| 2026-10-31 | T12 | troubleshoot calls `/sc:impact` only in the plan route's Phase A; the MDTM route (`--fix --depth deep`) Phase A is u
71:| 2026-10-31 | T12 | `/sc:load` only tells the user to type `/sc:graph status`; it never runs `/sc:graph` | run status from load; name it
72:| 2026-10-31 | T12 | `/sc:explain` gets the one-hop view in both copies; the existing one-line difference between the two `explain.md` co
73:| 2026-10-31 | T12 | `ruff format` reformatted the whole `tests/commands/test_impact_command.py`, including Task 9 lines (layout only) | 
74:| 2026-10-31 | T12 | After review, the root copies `commands/sc-load.md` and `commands/sc-explain.md` get the same new bullet as their sr
75:| 2026-10-31 | T12 | After review, implement Q1 and Q6 copy `degraded` into the task's notes, and pr-submit Wave 3 and VG-1 read `degrade
76:| 2026-10-31 | T12 | implement Q1 writes `index_state` and `checked_at` to the task's notes, not to the ledger line | the ledger line as 
77:| 2026-10-31 | T12 | After review, the three `explain.md` copies list `codegraph` in `mcp-servers` | keep `[context7]`; add `codegraph` |
