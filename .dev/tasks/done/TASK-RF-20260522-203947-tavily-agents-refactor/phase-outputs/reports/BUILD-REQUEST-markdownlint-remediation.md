# BUILD_REQUEST: Markdownlint remediation across 9 RF agent files

**Purpose:** Build an MDTM task to fix every markdownlint violation across the 9 agent definition files currently modified by the in-flight `TASK-RF-20260522-203947-tavily-agents-refactor` task. Pre-commit `markdownlint --fix` cannot auto-resolve these (line-length, heading-style, ordered-list-prefix, fenced-code-language, duplicate-heading require manual rewrites that preserve content semantics). Until they're fixed, the parent task's Phase 5 commit is blocked.

**Parent task (paused, awaiting this remediation):** `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/TASK-RF-20260522-203947-tavily-agents-refactor.md` (status `🟠 Doing`, Phase 5 paused after pre-commit gate).

## Scope (9 files)

All under `src/superclaude/agents/`:

1. `deep-research.md`
2. `deep-research-agent.md`
3. `rf-task-researcher.md`
4. `rf-task-builder.md`
5. `rf-task-executor.md`
6. `rf-assembler.md`
7. `rf-analyst.md`
8. `rf-qa.md`
9. `rf-qa-qualitative.md`

`rf-team-lead.md` is explicitly **out of scope** (held back from the parent task's commit because of a separate SHA-256 line-pin conflict with `tests/audit/test_dnsp_all_agents_fail_bypass.py`).

## Total violations: 234 (across 5 markdownlint rules)

| Rule | Count | Description | Remediation approach |
|---|---|---|---|
| MD029/ol-prefix | 79 | Ordered list prefix uses sequential numbering (16, 17, 18…) instead of restarting at 1 or staying at 1 | Renumber ordered-list items to either `1./2./3.` style or `1./1./1.` style consistently per list |
| MD040/fenced-code-language | 54 | Fenced code blocks (` ``` `) without a language tag | Add language tag (`bash`, `python`, `markdown`, `yaml`, `text` as appropriate per code block content) |
| MD036/no-emphasis-as-heading | 39 | `**Bold paragraph**` used where a heading (`####`) belongs | Convert `**Foo**` standalone-line-paragraph to `#### Foo` heading where structural; leave as bold when intentionally inline-emphasis |
| MD024/no-duplicate-heading | 37 | Same heading text repeated (e.g. `### What You Verify` appears 3+ times under different parent sections) | Disambiguate via parent-context suffix (e.g. `### What You Verify (Research Gate)`, `### What You Verify (Synthesis Gate)`); or restructure to use `####` sub-headings under a single canonical `###` heading |
| MD013/line-length | 25 | Lines exceeding 500 chars (current `.markdownlint.json` line_length is 500 per user override; default upstream was 160) | Reflow long prose paragraphs at soft line breaks (sentence boundaries) without breaking semantic content. Keep code-block lines intact (code_blocks=false in config). |

## Per-file violation distribution

| File | MD029 | MD040 | MD036 | MD024 | MD013 | Total |
|---|---|---|---|---|---|---|
| `deep-research.md` | 0 | 1 | 0 | 0 | 0 | 1 |
| `deep-research-agent.md` | 0 | 0 | 15 | 0 | 0 | 15 |
| `rf-task-researcher.md` | 0 | 18 | 0 | 0 | 0 | 18 |
| `rf-task-builder.md` | 0 | 14 | 0 | 0 | 7 | 21 |
| `rf-task-executor.md` | 0 | 16 | 0 | 0 | 1 | 17 |
| `rf-assembler.md` | 0 | 2 | 0 | 0 | 0 | 2 |
| `rf-analyst.md` | 0 | 1 | 0 | 5 | 1 | 7 |
| `rf-qa.md` | 12 | 1 | 0 | 3 | 6 | 22 |
| `rf-qa-qualitative.md` | 67 | 1 | 24 | 29 | 10 | 131 |
| **Total** | **79** | **54** | **39** | **37** | **25** | **234** |

## Build requirements for the resulting task

The task that the task-builder produces MUST satisfy these constraints:

1. **One Phase 2 item per file** (9 items, all marked `parallelizable: yes`). Each item edits ONE `src/superclaude/agents/<name>.md` file in isolation. No cross-file dependencies.
2. **Per-item self-contained editing instructions:** each item must (a) enumerate the specific rule violations to fix in that file with line numbers (pulled from the raw lint output at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/markdownlint-raw-output.txt`), (b) describe the remediation strategy per rule type, (c) require Edit-tool-only mutations (no sed/awk/Python helper), (d) write a per-file review file at `.dev/tasks/to-do/<new-task-id>/phase-outputs/reviews/<file>-review.md` with a checklist confirming each rule's violations have been resolved.
3. **Per-item completion verification:** each item ends with running `uv run pre-commit run markdownlint --files <the_one_file>` to confirm zero markdownlint violations remain in that file. If violations remain, log them in Phase 2 Findings and continue (other parallel items shouldn't be blocked by one file's residual issues).
4. **Phase-Gate QA after Phase 2:** spawn `rf-qa` with adversarial stance to re-verify all 9 files independently against the full `uv run pre-commit run markdownlint --files <all 9 files>` pass.
5. **Phase 3: sync & verify:** `make sync-dev`, `make verify-sync`. Both must pass cleanly.
6. **Phase 4: smoke tests:** `uv run pytest` must return same 102 failed / 7263 passed baseline (zero NEW failures). Audit-test wrapper pins (`tests/audit/test_dnsp_all_agents_fail_bypass.py`, `test_dnsp_twice_exhaust.py`) must remain unchanged in failure count (14 baseline).
7. **Phase 5: stage and commit.** Stage ONLY the 9 `src/superclaude/agents/*.md` files (NOT `.claude/agents/`). Use conventional commit message: `style(agents): remediate 234 markdownlint violations across 9 agent files`. The pre-commit hook must PASS cleanly on this commit (this is the success criterion).
8. **Phase 6: completion aggregation.** Consolidated report.
9. **Post-Completion Actions:** task notes must explicitly link back to the parent task (`TASK-RF-20260522-203947-tavily-agents-refactor`) so the parent task's executor can resume Phase 5 (stage+commit the 9-agent Tavily-first refactor) immediately after this remediation task completes.

## Constraint: preserve content semantics

- **Do NOT** delete content to fit line-length limits. Reflow at sentence boundaries.
- **Do NOT** change ordered-list semantic meaning when renumbering. If the list was numbered 16-28 because it was a continuation of an earlier numbered list, that structural choice has meaning — preserve the relationship (e.g. via section reorganization rather than naïve renumbering).
- **Do NOT** edit `.claude/agents/` (sync output, gitignored).
- **Do NOT** modify the Tavily-first content that the parent task added (those edits stay verbatim; only the markdownlint compliance changes).

## Parallelism requirement (user-stated)

> "When executing the tasklist with /task do as much in parallel as possible"

The task-builder MUST mark every Phase 2 item with `parallelizable: yes` (they're independent file-edits with no cross-file dependencies). The `/task` executor will then spawn all 9 items in a single parallel batch per the F2a exception.

## Raw lint output reference

The full raw markdownlint output (240 lines, all 234 violations with file:line:col and rule code) is at:

`.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/phase-outputs/reports/markdownlint-raw-output.txt`

The task-builder MUST read this file end-to-end to extract per-file per-line violation details for each Phase 2 item's "Context" field.

## Validation gate (post-build, pre-execute)

After task-builder produces the task file, invoke `/sc:reflect --type task --analyze` against the new task file to validate: (a) all 9 files are in scope, (b) each Phase 2 item is parallelizable, (c) the link back to the parent task is documented, (d) Phase 5 commit message is correct, (e) no scope creep (e.g. accidentally fixing markdownlint in other agent files that aren't part of this remediation).

After `/sc:reflect` passes, invoke `/task <new-task-path>` to execute.
