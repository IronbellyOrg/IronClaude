# Reviewer 1 brief (persona: analyzer; model slot: sonnet)

Mode: UC-1 (pre-execution plan review). You review a PROPOSED plan against its driving brief and the spec it cites. Read-only: never edit, write or run anything; return findings only. Grounding root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 (all relative paths below are under it).

Inputs:
- Plan under review: `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md` (read it whole).
- Driving brief: `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md`.
- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (section 2.1 terms incl. the nested propagation rule, section 2.2 WC-2/WC-4/WC-9/WC-10/WC-11, section 3.1 rows reflect, release-split, tdd, troubleshoot, workflow, brainstorm; section 3.2 rows auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist; section 5 SA-1..SA-6; section 6 row P2; section 7.3 AC-2.1).

Persona focus (analyzer): for each of the 15 P2 command tasks and the workflow/brainstorm tasks, check that every gate the spec row names is resolved the way the row says (default, caller flag, or blocked), that nothing in the plan adds an outward capability or changes standalone behaviour (SA-1, SA-3), that every nested call obeys the nested propagation rule, and that each plan decision D-P2-1..D-P2-17 is either required by the spec's silence or is a deviation the owner must approve. Verify any claim about a command or skill file by reading that file. Flag wrong file paths, wrong line anchors, gates the plan missed, and decisions that contradict the spec.

Output: a YAML card with `findings:` (each: id R1-Fn, severity P1 (plan would produce wrong behaviour or violate a spec rule) | P2 (a task is incomplete or an AC cannot catch the defect it targets) | P3 (wording, minor), claim, evidence as file:line list you actually read, deviation_class drift|regression|necessary|authorized|none, suggested_fix), plus `self_confidence` (0-1) and a `self_audit` paragraph naming what you checked. Every claim must cite file:line you read; tag anything else [INFERRED].

## T1 card excerpt

```yaml
  - id: T1-F4
    severity: P3
    claim: "Task 16 moves tasklist Stage 10.5 reflect outputs under --unattended from TASKLIST_ROOT/validation/reflect-pre/phase-<P>/ to <report-dir>/nested/reflect-<n>/ (D-P2-13). Any consumer that reads the old folder (the superclaude tasklist CLI, tests/tasklist) is only checked by running tests/tasklist, with no grep for readers of 'reflect-pre'."
  - id: T1-F5
    severity: P3
    claim: "Task 20's P2_GATES table repeats phrases already in UNATTENDED_EXPECT; it satisfies AC-2.1 'one assertion per gate' only if each gate of each section 3 row has its own phrase, which Tasks 2-16 do not enumerate gate by gate for every command."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T01:31:09Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189-195

```markdown
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | Otherwise | Skip enrichment | — |

   Research depth/params are owned by `/sc:research` and `tech-research` — see RESEARCH_CONFIG.md; brainstorm selects the route only.

   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). ...
```

### src/superclaude/commands/workflow.md:75

```markdown
- **Nested invocations.** The reflect step runs as today, without `--unattended` and without `--remediate`; in that form it has no gate.
```

### src/superclaude/cli/reflect/commands.py:317

The `--isolate-reviewers/--no-isolate-reviewers` option is a click option of the `superclaude reflect run` CLI (basis of plan D-P2-2). Read the file to confirm.

### src/superclaude/core/WORKER-CONTRACT.md:199-202

```markdown
| `/sc:reflect` | no `--remediate`; `--no-promote` when the coordinator owns folder moves |
| `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive` |
| `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>` |
| `/sc:troubleshoot` | no `--fix` (and no `--depth deep` until P2) |
```

## Coverage slice

| Requirement | Plan location | Status |
|---|---|---|
| INF-008 each default-on gate resolves per its section 3 row (source.md:10) | Tasks 2-16 | covered (verify per row) |
| INF-011 workflow nested reflect (source.md:10) | Task 17 | covered |
| INF-012 brainstorm research nested (source.md:10) | Task 18 | covered |
| INF-013 outward defaults only turned off (source.md:10) | Tasks 10, 12 | covered |
| INF-014 no safety rule touched, no outward capability added (source.md:10) | plan:23 | covered (verify) |
| INF-016 research-deep conflict decided (source.md:12) | D-P2-1, Task 18 | covered |
