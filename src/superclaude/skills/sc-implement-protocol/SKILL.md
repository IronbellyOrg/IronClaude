---
name: sc:implement-protocol
description: "Middleweight spec executor; spec/PRD/tasklist, informal notes, or inline prompt; per-task spec-compliance QA; one-file ledger"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, Skill
---

# /sc:implement protocol

Middleweight executor. Source is a spec/PRD/tasklist path, an informal notes file, or an inline prompt. Walk enumerable tasks (informal/prompt → one task). After each task, spec-compliance QA against **that task's** AC + parent spec + instructions. Lint/tests are extras, never the verdict. One markdown ledger.

Load `refs/qa.md` for Q3–Q5. Load `refs/ledger.md` for ledger I/O and resume. Do not load reflect-protocol. Do not invoke `/task`, `/sc:task`, or `sc:task-protocol`.

## Required input (STOP if missing)

A source: one file path (aliases `--spec`, `--prd`, `--tasklist`) **or** leftover `$ARGUMENTS` as an inline prompt. At most one file. Empty invocation (no path, no prompt) → `E-NO-SOURCE`.

```
Usage: /sc:implement <path-to-spec|prd|tasklist|notes> | /sc:implement <prompt>
STOP: need a source (file or prompt). Will not invent scope beyond that source.
```

## STOP table

| Code | Trigger | Product writes? | Ledger? |
|------|---------|-----------------|---------|
| `E-NO-SOURCE` | Empty invocation; two file paths; path under `.claude/skills\|agents\|commands` | No | No |
| `E-SOURCE-MISSING` | Path given but not found, or path is a directory | No | No |
| `E-NO-TASKS` | File exists but is empty/whitespace only | No | No |
| `E-NO-AC` | Ti has no AC after QUALIFY (including whole-body fallback) | No writes for Ti | Header/prior tasks may exist; no start line for Ti |
| `E-LEGACY` | Pitch invocation and/or removed flags `--type` / `--framework` / `--safe` / `--with-tests` | No | No |
| `E-HALT-QA` | Non-compliant after one fix pass; no operator Ruling | No T{i+1} | Non-compliant verdict line written |
| `E-NO-RULING` | Continue after non-compliant without operator Ruling; `--force` | No T{i+1} | Unchanged except existing blocked line |
| `E-LEDGER-CORRUPT` | Last ledger line truncated/unparseable | No further | Unchanged |
| `E-LEDGER-PATH` | `--ledger` not under `.dev/implement/` | No | No |

No other `E-*` codes. Unreadable/binary with no text → `E-NO-TASKS`. Directory → `E-SOURCE-MISSING`. Informal prose is a valid 1-task source, not `E-NO-TASKS`.

E-LEGACY copy: `Removed flags: --type/--framework/--safe/--with-tests. Pass a spec path.`

## Wave 0 — parse and intake

1. If `$ARGUMENTS` contains `--type`, `--framework`, `--safe`, or `--with-tests` → STOP `E-LEGACY`.
2. If `$ARGUMENTS` contains `--force` → STOP `E-NO-RULING`.
3. Resolve source:
   - Two file flags/paths → STOP `E-NO-SOURCE` (`pass one file`).
   - One path under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` → STOP `E-NO-SOURCE`.
   - One path that is a directory or missing → STOP `E-SOURCE-MISSING` citing the path.
   - One existing file → use it.
   - No path, leftover non-flag text → **inline prompt**. Persist it to `.dev/implement/<slug>/source.md` **before** any product edit (slug from first 40 slug-chars of the prompt, or `prompt`). That file is the source path for the ledger header. Do not invent extra tasks or extra scope.
   - No path and no leftover text → STOP `E-NO-SOURCE`.
4. Read the source file. Enumerate tasks (below). If zero enumerable items and the file has non-whitespace text → **T1 = the whole document** (informal spec / prompt). If the file is empty/whitespace → STOP `E-NO-TASKS`.
5. Resolve ledger path (default `.dev/implement/<slug>/progress.md`; slug = basename without extension, lowercased, non-`[a-z0-9_-]` → `-`, max 64). `--ledger` override MUST be under `.dev/implement/` else `E-LEDGER-PATH`.
6. Open or create ledger (header first, before any product edit). Resume per `refs/ledger.md`. Truncated last line → `E-LEDGER-CORRUPT`.
7. If N≥20 print **once**: `N tasks; compaction likely; ledger is the source of resume.` Do not STOP. Do not split.
8. Optional auggie before significant edits; unavailability is a warning, not a STOP.

### Enumerable tasks

A file is enumerable if **at least one** of these matches. Mix in document order → `T1..TN`. If the source already labels `T001` / `Task 3` uniquely, keep that label. Ids MUST NOT change on resume.

1. Markdown task items: `- [ ]` or `- [x]` or `* [ ]`.
2. Numbered items `1.` / `1)` under a heading, or `R-NNN` / `T-NNN` identifiers.
3. Headings `## Task N` / `### T1` / `## Phase N` with body text.

Do not invent extra tasks from prose paragraphs. Mixed prose + N≥1 items → those N items only. Zero items + non-empty prose → T1 = whole document (do not split paragraphs).

Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`. Phase-N tasklists are accepted as markdown. MDTM-shaped files still use **this** protocol. Do not auto-handoff.

### AC QUALIFY (before any edit for Ti)

First match:

1. An `AC:` / `Acceptance:` / `Acceptance criteria` / `Done when` block on that item.
2. Nested checkbox children of the item.
3. Sentences containing `MUST` / `SHALL` / `must` / `Then` / `done when`.
4. Else the item's own title **if** it contains a verb and an object (e.g. `Add login form`, `Fix resume parser`). That title **counts as AC**.
5. Else the item's full body / the informal source / the persisted prompt, if it has at least one sentence of observable intent. That body **is** `Ti.AC1`. QA is against this text; do not grow scope past it.

Else STOP `E-NO-AC` **before** any edit for that task. Single-word or empty-intent titles (`auth`, `make it better`, whitespace) are not AC. AC ids are `Ti.ACk` in source order.

Global constraints for `extra`: `## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable`.

### Parallel

Default sequential in source order. Parallel only when the source marks a set independent (literal `independent`, `parallel-ok`, or heading `Independent`) **and** set size ≤ 3. Unmarked = sequential. If overlap is obvious (`same file`), stay sequential. After a parallel batch, each task still gets its own verdict and ledger line before the next batch.

### Reviewer mode (no flag)

Inline, same session, when **all** are true: N≤3, source file ≤400 lines, session not compacted. Else one Task subagent (prompt from `refs/qa.md`). Same verdict schema. If compacted mid-run, remaining QA uses the subagent.

## Loop (Q0–Q8)

Re-read the ledger from disk at the start of each iteration. Do not trust session memory for "what's next".

```
Q0 START   If AC QUALIFY fails → E-NO-AC (do not reach Q1).
           Write start line with `git rev-parse HEAD` (40-hex) or `nogit`.
           Read Ti text + AC ids + global constraints.
Q1 EXEC    Implement only that task. Touched files = Write/Edit paths for this task.
           Drive-by files not implied by the AC are `extra`.
Q2 DIFF    `git diff start_sha..WORKTREE` (HEAD plus unstaged), scoped to Ti files when possible.
Q3 REVIEW  Load refs/qa.md. Reviewer (not the implementer voice) fills:
             - For each Ti.ACk: met | unmet + citation
             - extra_scope: hunks not mapped to any AC / instruction
             - misunderstood: ACs whose implementation contradicts the AC text
           Do not trust the implementer's report.
Q4 VERDICT Apply refs/qa.md order. Closed enum only.
Q5 FIX     If Q4 is not compliant: exactly one fix pass, re-run Q2–Q4 once.
Q6 EXTRAS  Detect and run lint/typecheck/tests if present. Record extras. Never overwrite Q4.
Q7 GATE    Apply halt table in refs/qa.md. Write ledger line(s). Flush before the next task.
Q8 NEXT    Only if complete (compliant, or non-compliant plus operator Ruling). Else STOP.
```

A 1-task source still runs Q0–Q8 once (inline). Skip the end-of-list second pass.

### Extras (after verdict, never the gate)

Detect in repo root, run what exists, skip the rest. Do not install tools. No extras flag.

| Extra | Detect | Record |
|-------|--------|--------|
| lint | `package.json` lint script, `ruff`, `eslint`, `make lint` | `lint=pass\|fail\|skip` |
| typecheck | `tsc --noEmit`, `mypy`, `pyright`, `package.json` typecheck | `typecheck=pass\|fail\|skip` |
| tests | `package.json` test script, `make test`, `uv run pytest` | `test=pass\|fail\|unrelated-red\|skip` |

Prefer the cheapest command scoped to this task's files when the tool allows.

Extra `fail` does not change the spec verdict. A task MUST NOT be marked `compliant` because extras are green when citations are missing.

`unrelated-red` when failing test files ∩ task-touched files = ∅. Red tests whose traceback includes this task's files → `test=fail` (still not the spec verdict; if the AC required those tests, that is `missing`).

### Whole-list review

After the last task is `complete`, when N>1 and not `--skip-final-review`: one reviewer pass vs the full spec + full ledger. Append `FINAL: pass|issues evidence=...`. Advisory. Do not rewrite per-task verdicts. Do not reopen completed tasks unless the operator says so. N=1: skip (the per-task review is that pass).

## Done

Every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus operator Ruling). Print the ledger path. Suggest `/sc:test` and `/sc:git` only as optional next steps, not gates.

If all tasks already `complete` on invoke: STOP `already complete: <ledger path>`.

## Out of scope

- Empty `/sc:implement` with no path and no prompt
- Growing scope past the given prompt / informal notes
- Generating the spec (`/sc:brainstorm`, `/sc:workflow`, `/sc:tasklist`)
- `/task` MDTM execution, `/sc:task` compliance tiers, `/sc:tdd`
- `/sc:test`, `/sc:git`, `/sc:reflect` as required steps
- Dual-mode pitch UX, `--reviewer`, `--force`, `--fresh`, `--no-extras`
- Python CLI, JSON/YAML ledger, 6-agent phase gates, TDD as pass/fail
