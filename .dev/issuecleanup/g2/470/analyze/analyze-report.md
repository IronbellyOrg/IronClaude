# Architecture analysis: src/superclaude (issue #470 area)

- Command: `/sc:analyze src/superclaude --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/470/analyze`
- Focus: architecture. Depth: quick. Scope narrowed to the five source surfaces issue #470 names.
- Codegraph: index_state=fresh, checked_at=2026-11-24T02:40:42Z; degraded: graph:truncated

The code graph does not index Markdown. It was used for the `src/superclaude` layout (328 indexed files, 306 Python; listing was truncated). Every issue #470 surface is Markdown, so the analysis used Glob/Grep and direct Reads instead of graph symbol/caller/impact queries for those surfaces. No broad audit of the package's unrelated Python code was performed.

## Findings

### 1. Medium: the research pipeline's producer skills are gone, but the contracts they served are still shipped

The three skills issue #470 asks to fix no longer exist:

- `src/superclaude/skills/tech-research/SKILL.md` removed by commit `430eaa87f`, pull request #650.
- `src/superclaude/skills/task/SKILL.md` and `src/superclaude/skills/task-builder/SKILL.md` removed by commit `a3edd84db`, pull request #656.
- All three are recorded as retired in `src/superclaude/cli/install_retired_data.py` at lines 83 (`task`), 86 (`task-builder`) and 100 (`tech-research`).

What remains, and still disagrees:

- `src/superclaude/agents/rf-qa.md:316` requires a task file's frontmatter to contain non-empty `created`, `template` and `tracks`.
- `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:12` uses `created_date`, and lines 1 to 40 contain no `created`, `template` or `tracks` field.

So a task written from the template still fails the reviewer's schema check. The check sits in the "Task Integrity Check" phase, whose own trigger line (`src/superclaude/agents/rf-qa.md:309`) is "after task file creation (A.8 in tech-research)", and that skill is removed. The test the issue names, `tests/skills/test_task_builder_merge.py`, is also gone.

### 2. Low: the reviewer agent is still used, but for other work

`rf-qa` is still spawned for structural review of code changes by the reflect command (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:620`, `src/superclaude/commands/reflect.md:171`) and is referenced by `src/superclaude/commands/spec-panel.md`. Whether those uses apply the frontmatter schema rule in finding 1 was not traced. UNVERIFIED.

All eight `rf-*` agent files (`rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-qa`, `rf-qa-qualitative`, `rf-team-lead`, `rf-analyst`, `rf-assembler`) remain. A text search found old pipeline references in that family; their complete contents and every caller were not audited. Open issue #572 is the evaluation of whether to keep, refactor or remove them.

## Metrics

| Item | Value |
|---|---|
| Indexed files under src/superclaude | 328 (306 Python) |
| Issue surfaces checked | 5 |
| Surfaces removed | 3 (tech-research, task, task-builder) |
| Surfaces still present and conflicting | 2 (rf-qa.md, complex task template) |
| Named test file still present | no |

## Security

Not assessed. This was an architecture pass at quick depth.

## Performance

Not assessed. This was an architecture pass at quick depth.

## Recommendations

1. Treat issue #470's pipeline fixes as superseded: the pipeline was removed in the 6.1.0 release and the research request it served (issue #463) is closed. The issue's own 2026-11-17 review said to close it as superseded if the task and task-builder skills went, and they have.
2. Recommend closing the removed pipeline's issue as superseded, not as fixed, while explicitly preserving the residual schema mismatch for issue #572's agent evaluation. A standalone task producer still exists: `src/superclaude/agents/rf-task-builder.md:61-84` mandates using the retained complex template. The removed skills must not be rebuilt just to fix their old resume path. No GitHub changes were made; closure and any transfer of the residual finding require the coordinator's owner-approved action.
3. Before relying on finding 2, confirm whether the reflect command's `rf-qa` pass applies the frontmatter schema rule. That was not verified here.
