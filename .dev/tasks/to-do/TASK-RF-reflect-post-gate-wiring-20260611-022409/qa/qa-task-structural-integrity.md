# QA Report — Task Structural Integrity

**Topic:** Reflect post-gate wiring structural integrity
**Date:** 2026-06-11
**Phase:** final QA gate / structural-integrity lens
**Fix authorization:** false — report only

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All four `# Phase N` line-1 assertions amended for optional frontmatter | PASS | `SKILL.md:100` says optional leading YAML frontmatter immediately followed by `# Phase N -- <Name>` and only requires first-line heading when no frontmatter exists. `SKILL.md:857-867` seeds `executor_model_class`/`start_commit` frontmatter before `# Phase N -- <Phase Name>` and states parsers tolerate the leading block. `SKILL.md:1137` structural check #5 allows optional leading `---` frontmatter. `phase-template.md:9-23` mirrors the frontmatter block and parser-tolerance wording. Grep found no surviving unqualified mandate that `# Phase N` must be literal line 1 without frontmatter allowance in the four requested locations. |
| 2 | Reflection task heading prefix preserved and #18/#19/#20 consistency checked | PASS with related finding | The fixed terminal reflection heading appears as `### T<PP>.<final> -- Post-Execution Reflection: superclaude reflect run (wrapper shell-out)` in `SKILL.md:1045` and `phase-template.md:138`; the required `-- Post-Execution Reflection:` prefix including colon is intact. `SKILL.md:1178-1180` keeps #18 scanner-visible reflection task, #19 reflection as sole task after end checkpoint with highest `<NN>`, and #20 reflection exempt from checkpoint path because it uses `**Reflect Report Path:**`. Related structural issue found in the standalone template checkpoint examples; see Finding 1. |
| 3 | Phase-file frontmatter seeding present and parser-safe | PASS | `SKILL.md:860-864` and `phase-template.md:12-16` seed only `executor_model_class`, optional `start_commit`, closing `---`, then `# Phase N -- <Phase Name>`. `SKILL.md:867` and `phase-template.md:20` explicitly say do not seed `reflect_post:` or a `# reflect_post` comment line. Grep for `^# reflect_post`, `^\s*# reflect_post`, and `reflect_post:` found no seeded lines; only prose warnings at `SKILL.md:867`, `SKILL.md:1137`, and `phase-template.md:20`. |
| 4 | PRE gate and `--no-reflect` toggle unchanged vs `origin/master` | PASS | `SKILL.md:1455-1476` still contains Stage 10.5 `/sc:reflect --mode pre --remediate` and disabled skip wording. `rg -- '--no-reflect' SKILL.md` reports four occurrences: `SKILL.md:9`, `SKILL.md:725`, `SKILL.md:1042`, `SKILL.md:1474`. `git diff --unified=0 origin/master -- SKILL.md | rg -- '--mode pre|Stage 10\.5|Skip when disabled'` produced no output. Diff grep for `--no-reflect` only showed unchanged-context occurrences inside modified POST-reflection paragraphs, not toggle semantics. |
| 5 | Parser smoke test with seeded frontmatter | PASS | Ran `uv run python -c ...` against `count_tasks_in_file`, `parse_tasklist`, and `_extract_phase_name`. Actual output: `{'count': 2, 'task_ids': ['T02.01', 'T02.02'], 'frontmatter_name': '- Wiring', 'plain_name': '- Wiring', 'names_equal': True}`. Assertions passed: count is 2, parsed IDs are `[T02.01,T02.02]`, and phase-name extraction matches the frontmatter-less version. |
| 6 | Additional structural scan of edited template examples against struct check #18 | FAIL | `phase-template.md:109-110` still documents range checkpoints as `### Checkpoint: Phase <P> / Tasks <start>-<end>` and `phase-template.md:127-129` still documents end-of-phase checkpoint as `### Checkpoint: End of Phase <N>`. This contradicts `SKILL.md:1178`, which requires every checkpoint block to be emitted as `### T<PP>.<NN> -- Checkpoint:` and never as a sibling `### Checkpoint:` heading. |

## Candidate Issues Examined

1. Candidate: surviving strict line-1 `# Phase N` rule. Rejected for requested four locations because each now allows optional frontmatter (`SKILL.md:100`, `SKILL.md:857-867`, `SKILL.md:1137`, `phase-template.md:9-23`).
2. Candidate: frontmatter includes `# reflect_post` comment. Rejected; grep found only prose warnings, no seeded comment line.
3. Candidate: reflection heading lost `-- Post-Execution Reflection:` colon. Rejected; exact prefix present at `SKILL.md:1045` and `phase-template.md:138`.
4. Candidate: Stage 10.5 PRE gate modified. Rejected; diff grep for `--mode pre`, `Stage 10.5`, and `Skip when disabled` produced no output.
5. Candidate: parser frontmatter breaks task count or parse. Rejected by smoke test output above.
6. Candidate: template checkpoint examples still use non-task headings. Confirmed; promoted to Finding 1.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md:109-110`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md:127-129` | The human-review phase template still shows checkpoint headings as sibling `### Checkpoint:` blocks. This conflicts with structural check #18 in `SKILL.md:1178`, which says every checkpoint must be a scanner-visible `### T<PP>.<NN> -- Checkpoint:` task heading and never a sibling `### Checkpoint:` heading. If a human copies the template, Sprint task scanning can miss checkpoints despite the SKILL self-check asserting the opposite. | Update the template checkpoint examples to the scanner-visible task-heading form, e.g. `### T<PP>.<NN> -- Checkpoint: Phase <P> / Tasks <start>-<end>` and `### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>`, keeping the reflection task as the sole allowed task after the end checkpoint. |

## Parser Smoke-Test Output

```text
warning: `VIRTUAL_ENV=/lsiopy` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
{'count': 2, 'task_ids': ['T02.01', 'T02.02'], 'frontmatter_name': '- Wiring', 'plain_name': '- Wiring', 'names_equal': True}
```

Note: the `- Wiring` value is not introduced by frontmatter; it is identical with and without frontmatter. The smoke-test requirement was transparency across frontmatter, and that assertion passed.

## Actions Taken

- No source edits made (`fix_authorization: false`).
- Created this QA report only.

## Confidence

- Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 7 | Grep/Bash: 10 | Glob: 0 | Bash: 10 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

VERDICT: FAIL

## Numbered Findings

1. IMPORTANT — `phase-template.md` checkpoint examples still use `### Checkpoint:` sibling headings, contradicting `SKILL.md` structural check #18's scanner-visible `### T<PP>.<NN> -- Checkpoint:` requirement.
