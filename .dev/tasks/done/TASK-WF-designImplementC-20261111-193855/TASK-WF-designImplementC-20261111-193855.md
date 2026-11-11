---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-designImplementC-20261111-193855
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Use codegraph in /sc:implement

Source: ./source.md
Goal: /sc:implement runs one codegraph readiness check per run and uses codegraph for per-task context loading and dependent checks only when the index is fresh, with the Grep/Read floor and a recorded note otherwise, and every sub-agent brief carries the run state.

## Constraints

- Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking, minor, note, the four checklist answers, the verdict order), retry ladder and managed-package rule of /sc:implement. Add no new `E-*` code.
- The reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` stays closed with exactly seven slots (task_brief, global_constraints, diff, start_sha, prior_findings, delta_diff, recheck_list); codegraph context reaches the reviewer only through the content of the existing `{diff}` slot.
- Graph notes never go into the ledger notes file (it would add a `notes@` token and change the inline-review rule); they go to one run file named `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`).
- Installed primitives never tell an agent to read a `src/superclaude/...` path; the usage guide is named only as `~/.claude/CODEGRAPH.md`.
- The tool allowlist names exact `mcp__codegraph__codegraph_<tool>` entries, never a wildcard. Never call `codegraph_explore`, `codegraph init`, `codegraph index`, `codegraph sync`, or CLI `codegraph status` while an init or index runs.
- Edit only `src/superclaude/commands/implement.md` and files under `src/superclaude/skills/sc-implement-protocol/`; do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, and do not stage `.claude/`.

## Phase 1: Command file states the codegraph contract

## Task 1: Add the codegraph section to the implement command file

Edit `src/superclaude/commands/implement.md`. In the frontmatter add the line `mcp-servers: [codegraph]` after `complexity: standard`. Add a short `## Codegraph` section before `## Boundaries`. It states: the protocol runs exactly one codegraph readiness check per run (Wave 0 of the protocol skill, rules in `~/.claude/CODEGRAPH.md`); codegraph is used only when `index_state` is `fresh`, for pre-edit context (definitions, callers, impact of the symbols a task touches) and for the per-task check that the change reached every dependent; otherwise the run continues on Grep/Read and records a `graph:*` note in `codegraph.md`; codegraph never causes a STOP. Under `**Will Not:**` in Boundaries add a bullet: run `codegraph init`, `codegraph index` or `codegraph sync`. Do not change any flag, option row, STOP behaviour or the Activation block.

Acceptance criteria:
- `src/superclaude/commands/implement.md` frontmatter contains `mcp-servers: [codegraph]` and still parses as YAML with the original `name`, `description`, `category`, `complexity` and `argument-hint` values unchanged.
- The `## Codegraph` section names one readiness check per run, the fresh-only rule, the Grep/Read floor with a recorded `graph:*` note, and that it never STOPs; it points to `~/.claude/CODEGRAPH.md` and contains no `src/superclaude` path.
- The Boundaries `Will Not` list names `codegraph init`, `index` and `sync`; the Options table, Usage block and Activation block are byte-identical to before.

## Phase 2: Protocol skill runs the check and uses the graph per task

## Task 2: Add frontmatter, pointer and the one readiness check to the protocol skill

Edit `src/superclaude/skills/sc-implement-protocol/SKILL.md`. Extend the `allowed-tools` line (currently `Read, Grep, Glob, Edit, Write, Bash, Task, Skill`) by appending the exact entries `mcp__codegraph__codegraph_status`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_callees`, `mcp__codegraph__codegraph_impact` (the set `src/superclaude/skills/sc-reflect-protocol/SKILL.md` allows for codegraph). After the frontmatter add an HTML comment block headed `Extended metadata (for documentation, not parsed):` with `mcp-servers: [codegraph]`, as the reflect and troubleshoot protocol skills do. After the intro paragraph add one line: codegraph usage rules are in `~/.claude/CODEGRAPH.md`, read once per run. In Wave 0 add a step 9 after the existing step 8 (optional auggie) that runs the `~/.claude/CODEGRAPH.md` section 2 readiness check exactly once per run, before the first Q0, and keeps the result as the run state: `index_state`, `access`, `checked_at`, `worktree_root`, `projectPath`. The step also states: a resume is a new run with its own single check; there is no second check after the first product write, the state stays as recorded at `checked_at`, and graph rows about files this run changed are leads confirmed by Grep/Read; a later codegraph call that reports not indexed, foreign index or an error adds the matching token and keeps the rest of the run on the floor without a re-check; an `index_state` other than `fresh`, or `access: none`, means no codegraph call this run and the matching closed-list `graph:*` token; print one line `codegraph: index_state=<state> access=<access> checked_at=<ts>` (plus the token when degraded); write the state and every token to `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`), appending one line per later token; the check never halts the run and adds no STOP code. State that the existing `sc:impact-protocol` delegations at Q1 and Q6 are unchanged and run their own readiness inside that skill, which this protocol does not count as a second check of its own.

Acceptance criteria:
- The `allowed-tools` line of `src/superclaude/skills/sc-implement-protocol/SKILL.md` still lists `Read, Grep, Glob, Edit, Write, Bash, Task, Skill` and adds exactly the six `mcp__codegraph__codegraph_*` names above, with no wildcard; the file's frontmatter still parses.
- The extended-metadata comment lists `mcp-servers: [codegraph]` and the file points to `~/.claude/CODEGRAPH.md` without a `src/superclaude` read path.
- Wave 0 step 9 states one readiness check per run, the five run-state fields, the no-re-check-after-write rule, the not-fresh behaviour with a `graph:*` token, the `codegraph.md` record location for legacy and managed runs, and that it never halts; the STOP table has no new row.

## Task 3: Add the pre-edit context step and the dependents step to the Q loop

Depends on: Task 2

In `src/superclaude/skills/sc-implement-protocol/SKILL.md` add two steps to the Q0-Q8 loop block, keeping the existing step numbering and text of Q0 to Q8 otherwise intact, and add a short tool-to-step table. Q1a (before the Q1 edits): when the run state is `index_state: fresh` and `access: mcp`, for up to 5 symbols the task names or touches, locate with `codegraph_search`, read the definition with `codegraph_node {symbol, file, includeCode:true}` (file outline with `codegraph_node {file, symbolsOnly:true}`), and find who depends on it with `codegraph_callers` and `codegraph_impact` at depth 1; every call passes the run state's `projectPath`. The Grep for the definition, Read of the range, word-boundary Grep for references and Read of each call site stay as the floor and run whenever the run state is not fresh; Read before every Edit regardless; the Q1 rename/delete/signature `sc:impact-protocol` step stays as it is. Q2b (after the Q2 diff, before Q3): for up to 5 symbols whose definition, signature or behaviour the diff changed, query `codegraph_callers`, `codegraph_impact` at depth 1 and, when the change moved a call, `codegraph_callees`, and list the dependents whose file is not in the task's touched set; floor is Grep `\b<symbol>\b` plus Read of the hits. Rules for both steps: each row is confirmed by Grep plus Read of the call site before it is cited or drives an edit (the CS1 to CS5 procedure of `~/.claude/CODEGRAPH.md` section 5); at most 5 rows per symbol and 20 per run; an empty graph answer is never read as "no dependents"; a truncated list is re-queried once, then `graph:truncated` is recorded; rows about files this run changed are leads. The Q2b list is context for the reviewer, placed in the `{diff}` slot content (Task 4); it becomes a finding only through the existing four-question checklist, never edits files and never widens the touched set. The Q5 fix pass and any retry attempt run Q1a and Q2b again for the symbols they touch.

Acceptance criteria:
- `src/superclaude/skills/sc-implement-protocol/SKILL.md` contains a `Q1a` step before `Q1` and a `Q2b` step between `Q2` and `Q3`, naming `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_impact` and (for Q2b) `codegraph_callees`, each tied to its step, with the Grep/Read floor stated for each; the original text of Q0 to Q8 is otherwise unchanged.
- Both steps say codegraph runs only when the run state is `index_state: fresh`; otherwise Grep/Read runs and a `graph:*` line is appended to `codegraph.md`; neither step can halt the run or change a verdict.
- The 5-symbol, 5-rows-per-symbol and 20-rows-per-run caps, the confirm-by-Grep-and-Read rule and the "empty is not absence" rule appear in the skill text.

## Phase 3: Sub-agent briefs carry the run state

## Task 4: Carry the run state in the reviewer and final-review prompts

Edit `src/superclaude/skills/sc-implement-protocol/refs/qa.md`. Do not edit the closed reviewer template fenced block or its seven slots. In the "Slot sources" list change the `{diff}` entry so the slot content is the Q3 diff followed, when Q2b produced rows or the run state is not fresh, by a `Codegraph context` block. The block starts with the four run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath`, then the standing line `call codegraph only when index_state: fresh, never to widen scope`, then the Q2b dependents not in the diff (or the note that Q2b ran on the Grep/Read floor). State that the block is context only: a dependent becomes a finding only through the existing checklist, with its own anchor, and an unreached dependent that no AC or quoted constraint requires is not blocking. In the "Managed FINAL review (archive gate)" paragraph add that the FINAL prompt carries the same four run-state fields. State once that saved prompts keep line 1 as the start sha, that the block sits inside the `{diff}` slot content, and that the saved-prompt comparison with the template is therefore unchanged.

Acceptance criteria:
- The fenced reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` is byte-identical to before and `tests/skills/test_implement_severity_static.py::test_ac02_one_closed_reviewer_template_with_seven_slots` passes.
- The `{diff}` slot-source text names the `Codegraph context` block with `index_state`, `checked_at`, `worktree_root` and `projectPath`, the standing codegraph-only-when-fresh line, and the Q2b dependents list; it says the block is context only and adds no new blocking trigger.
- The managed FINAL paragraph states the FINAL prompt carries the four run-state fields, and the saved-prompt rule text states the comparison is unchanged because the block sits inside a slot.

## Task 5: Carry the run state in the retry adviser prompts

Edit `src/superclaude/skills/sc-implement-protocol/refs/retry.md`. Wherever it writes the prompt for an `implement-retry-adviser` (the adviser spawns of escalations 1 to 3 and any adviser re-spawn), require the prompt to carry the four run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath` from the run's single readiness check. State that the adviser definition lists only Read, Grep and Glob and so has no codegraph tools: its prompt tells it to use Grep and Read and to treat the run state as context only. Add one sentence that the executor's own retry attempts run Q1a and Q2b of `SKILL.md` again, and that no ladder step, halt reason, ledger record or brief file format changes.

Acceptance criteria:
- `src/superclaude/skills/sc-implement-protocol/refs/retry.md` states that every adviser prompt carries `index_state`, `checked_at`, `worktree_root` and `projectPath`, and that the adviser has no codegraph tools and stays on Grep/Read.
- The halt table, the `retry` record format, the brief file layout and every `E-*` code in `refs/retry.md` are unchanged.
- Running `uv run pytest tests/skills/test_implement_retry_revert.py tests/skills/test_implement_retry_citation.py tests/skills/test_implement_saved_prompt_rule.py tests/skills/test_implement_adviser_family.py tests/skills/test_implement_severity_static.py tests/skills/test_review_severity_rule.py tests/commands/test_impact_command.py tests/commands/test_workflow_command.py` passes.
