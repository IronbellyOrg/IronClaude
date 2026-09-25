---
variant: 2
persona: refactorer
model: sonnet
generated: 2026-09-24
topic: sc-implement-rewrite
bias: deletion-and-reuse
---

# Variant 2 — Rewrite `/sc:implement` by deletion

This variant is the cheapest transformation that still matches the seed brief. It rewrites the existing command file and adds one protocol skill. It does not add a subsystem, a Python runner, dual-mode compatibility, or an ensemble.

## 1. Problem / goals

### Problem

`src/superclaude/commands/implement.md` is a persona/MCP behavioral mode. Invocation is a free-form feature pitch plus `--type` / `--framework`. Done means "compiles, basic functionality, ready for `/sc:test`". That is the wrong job.

The file has no `## Activation` and no skill. It is the product. Modern `/sc:*` commands (reflect, brainstorm, auggie-review) are thin dispatchers that MUST invoke `Skill sc:<name>-protocol`.

### Goals

1. `/sc:implement` becomes a **middleweight executor**: given a spec, PRD, or tasklist (never a pitch), walk the tasks, and after each task verify **that task** against its AC + spec + instructions.
2. Primary QA is Superpowers SDD Part 1 spec-compliance (Missing / Extra / Misunderstood). Lint / typecheck / `npm test` are extras, never the verdict.
3. Ledger is one markdown file, one line per task, resumable. Not `/task` F1, not 6-agent gates, not MDTM.
4. Hard cutover. No "legacy free-form still works".

### Non-goals (this rewrite)

Do not import `/task` phase-gate QA, MDTM templates, reflect pre/post, executing-plans TDD gates, Matt end-of-batch suite+review as the only gate, or feature-dev 7-phase.

## 2. Functional requirements

Each requirement is falsifiable: a static grep, a fixture invocation, or a protocol self-check can fail it.

**R-001.** `/sc:implement` with no resolvable path to an existing spec, PRD, or tasklist file **STOP**s. It does not write code. The STOP message is usage plus the missing input (path absent, path not a file, or file empty of enumerable tasks). Falsify: invoke with `"user profile component"` and observe a write.

**R-002.** A path that exists but contains no enumerable tasks (see §6) **STOP**s with: "no enumerable tasks; produce a checklist or numbered AC list." The command does not invent a tasklist from prose.

**R-003.** Tasks execute in source order. Parallel only when the source marks a set independent (literal `independent` on the item or a heading `Independent`) **and** the set size is ≤ 3. Unmarked = sequential. Falsify: two unmarked tasks run concurrently.

**R-004.** After each task, before the next task starts, the protocol produces a spec-compliance verdict of exactly one of: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`. The verdict is against **that task's** AC + parent spec/PRD + task instructions. Falsify: a task marked complete with no verdict line in the ledger.

**R-005.** The reviewer does not treat the implementer's prose report as evidence. Evidence is the diff (or file reads) versus the brief. Falsify: ledger `complete` after "implemented X" with no file change.

**R-006.** Verdict `missing`, `extra`, or `misunderstood` blocks the next task until either (a) a fix + re-review yields `compliant`, or (b) a ledger **Ruling** line is written. No silent proceed.

**R-007.** Verdict `cannot-verify` is not `complete`. Next action is more evidence (read the files, show the diff) or a Ruling. It is not a pass.

**R-008.** Lint, typecheck, and `npm test` / project test command, when the repo has them, run after the spec-compliance verdict and are recorded on the same ledger line as extras. They never flip `compliant` → fail, and they never make a missing/extra/misunderstood task `complete`.

**R-009.** A red test suite whose failing files are disjoint from the files this task touched is recorded `extras: test=red-unrelated` and is **not** a fail.

**R-010.** One markdown ledger file is created/appended per run. Format is the four-line grammar in §8. No second schema. No YAML sidecar. No execution-log table.

**R-011.** Resume: on `/sc:implement <same-path>` (or `--resume`), the protocol reads the ledger, finds the first task whose line does not contain `complete`, and starts there. Compacted sessions trust ledger + `git log`, not chat memory.

**R-012.** After the last task is `complete`, the protocol may run **one** whole-list spec-compliance pass against the parent spec. It does not run a per-task ensemble, a second reviewer persona set, or `/sc:reflect`. For a 1-task source, the per-task review **is** that pass (do not run it twice).

**R-013.** The command file contains `## Activation` that invokes `Skill sc:implement-protocol` before any protocol step. Falsify: `make lint-architecture` Check 1 / Check 6.

**R-014.** Skill directory `src/superclaude/skills/sc-implement-protocol/` exists with `SKILL.md` frontmatter `name:`, `description:`, `allowed-tools:`, and `name` ending in `-protocol`. Falsify: lint-architecture Checks 2, 8, 9.

**R-015.** Free-form pitch UX is gone. Command examples are path-based only. Flags `--type`, `--framework`, `--safe`, `--with-tests` do not appear in `implement.md` or the skill. Falsify: grep those strings in the two SoT files.

**R-016.** Completion is **not** "compiles / ready for `/sc:test`". Done = every enumerable task has a `complete` ledger line with verdict `compliant` (or a Ruling). Falsify: remaining "ready for `/sc:test`" in SoT files.

**R-017.** `/sc:implement` does not route into `/task` or `/sc:task`. If the source is an MDTM task file, implement still uses this protocol (enumerate + spec-compliance + tiny ledger). Falsify: skill text that says "hand off to `/task`".

**R-018.** Spec is binding. A deviation that ships must be a ledger `Ruling:` line: what, why, cost if wrong. Silent extras in the diff that the brief did not ask for are `extra` (R-004/R-006), not "nice to have".

**R-019.** Source of truth is `src/superclaude/`. After edit, `make sync-dev`. `.claude/skills` and `.claude/commands` are not staged. Plugin copy `plugins/superclaude/commands/implement.md` follows the existing plugin sync; it is not a second SoT.

**R-020.** Hard cutover in one rewrite. No dual grammar, no "legacy: feature-description still accepted", no mapping of `--type component` onto the new loop.

## 3. NFRs

| ID | Requirement |
|---|---|
| N-001 | Command file ≤ 150 lines (lint warns at 200, hard-fails at 500). Target the thin-dispatcher band used by `auggie-review.md`. |
| N-002 | `SKILL.md` ≤ 500 lines. Loop + STOP + ledger grammar live in SKILL.md. At most **one** `refs/` file (`spec-compliance.md`) for the Missing/Extra/Misunderstood rubric. No `cost-profile.yaml`, no templates dir, no Python package. |
| N-003 | No new runtime dependency. No new MCP server required. Optional Context7 only when a task implements against a third-party library API; not listed as the command's purpose. |
| N-004 | No new CLI entry point (`superclaude implement` is out). Slash command + skill only. |
| N-005 | Personas are not the product. Command frontmatter `personas` is empty or omitted. No "activate frontend/backend/security" flow. |
| N-006 | Skill `allowed-tools` is the minimum: Read, Grep, Glob, Edit, Write, Bash, Task, Skill. Not TodoWrite-as-ledger (disk ledger is the ledger). |
| N-007 | Protocol is restart-safe after compaction: resume rule (R-011) does not require the previous session transcript. |
| N-008 | One reviewer vs the brief. Never 2+ reviewer agents per task. |

## 4. Architecture

### What to build (two files, optionally three)

```
src/superclaude/commands/implement.md          # rewrite in place; thin dispatcher
src/superclaude/skills/sc-implement-protocol/
  SKILL.md                                     # STOP, enumerate, loop, ledger, extras
  refs/spec-compliance.md                      # optional; only if SKILL.md would exceed ~350 lines
```

Then `make sync-dev`.

Mirror: `src/superclaude/commands/auggie-review.md` (Required Input + STOP + Activation + short Options). Do not mirror `reflect.md` (legacy grammar, tiers, ensembles).

### Command file (dispatcher only)

Responsibilities:

1. Parse `$ARGUMENTS`: a filesystem path (positional, or `--spec|--prd|--tasklist` as aliases for the same thing — one path).
2. Optional `--resume`, optional `--ledger <path>` override.
3. STOP copy (usage) if path missing.
4. `## Activation` → `Skill sc:implement-protocol`.
5. Boundaries: will execute a spec/PRD/tasklist; will not invent a feature from a pitch; will not call `/task`.
6. Three path-based examples. Zero pitch examples.

### Skill (the loop)

```
STOP if no path / not a file / not enumerable
open or create ledger
resume = first task without `complete`
for each remaining task:
    implement that task only
    spec-compliance review vs that task's AC + spec + instructions
    if not compliant: fix or Ruling; do not advance
    run extras if present; record; do not gate
    append one ledger line
optional one whole-list pass if N>1
print ledger path
```

Reviewer (lean):

- **N = 1, or N ≤ 3 and source file ≤ 400 lines:** inline, same session. One pass. Same rubric.
- **N > 3, or source file > 400 lines, or session already compacted:** one `Task` subagent, prompt = SDD Part 1 only (diff vs brief; Missing/Extra/Misunderstood; verdict). No Part 2 code-quality ensemble. No second subagent.

### What NOT to build

- Dual-mode / legacy free-form / `--type` compatibility shims
- Python executor, pytest plugin, or `superclaude implement` CLI
- F1 checklist, MDTM templates, 6-agent phase gates
- sc-tasklist `execution-log.md` schema, TurnLedger, reflect `per_task_verdicts`
- TDD red/green as the pass/fail
- Full-suite-once + one `/code-review` as the only QA (Matt shape)
- feature-dev 7-phase, ce-work `lfg`
- Persona activation matrix, Magic/Playwright as required MCP
- `--with-tests` as a substitute for spec-compliance
- Per-task code-quality Part 2, reviewer ensembles, `/sc:reflect` hook
- JSON/YAML ledger, SQLite, session store
- Auto-commit / `/sc:git` as a required next step
- Routing: "if this looks like MDTM, call `/task`"

### Delete from current `implement.md`

The current file is 128 lines of the wrong product. Rewrite; do not patch. Specifically **gone**:

| Delete | Why |
|---|---|
| Frontmatter `personas: [architect, frontend, backend, security, qa-specialist]` as identity | Personas-as-the-product |
| Frontmatter `mcp-servers: [context7, sequential, magic, playwright]` as identity | MCP-as-the-product |
| Triggers: "feature development requests", "framework-specific requirements" | Pitch activation |
| Context Trigger Pattern: `/sc:implement [feature-description] [--type ...] [--framework ...]` | Main UX to kill |
| Behavioral Flow Analyze → Plan → Generate → Validate → Integrate | Invent-then-write |
| MCP Integration section (Context7/Magic/Sequential/Playwright as the method) | Not the job |
| Tool Coordination: TodoWrite as progress; Task "for large-scale feature development" | Wrong ledger; silent `/task` |
| Key Patterns: context detection, multi-persona coordination | Personas-as-the-product |
| Examples: user profile component / auth API / payment system / Vue widget | Pitch examples |
| COMPLETION CRITERIA: compiles, basic functionality, files saved | Wrong done |
| Post-Implementation Checklist item 3: "Ready for `/sc:test`" | Test-readiness as done |
| Next Step: `/sc:test` then `/sc:git` as the success path | Extras, not the gate |
| Flags `--type`, `--framework`, `--safe`, `--with-tests` | Old UX |
| Boundaries "Will: intelligent persona activation" | Personas-as-the-product |

Keep the filename, slash name `/sc:implement`, and category `workflow`. Everything else is replaced.

## 5. Input contract — STOP without spec/PRD/tasklist

### Invocation

```
/sc:implement <path>
/sc:implement --spec <path>
/sc:implement --prd <path>
/sc:implement --tasklist <path>
/sc:implement <path> --resume
/sc:implement <path> --ledger <ledger-path>
```

`--spec`, `--prd`, `--tasklist` are **aliases**. One file. No "spec plus tasklist required together". If two paths are passed, STOP: "pass one file".

### STOP (no work, print usage)

1. No path in `$ARGUMENTS`.
2. Path is not an existing file (directories are not accepted).
3. File has no enumerable tasks (§6).
4. Path resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (not an input; not an output).

### Not STOP

- Spec/PRD whose numbered requirements are the tasks (no separate tasklist file).
- SuperClaude phase-N tasklist markdown, if it still has enumerable items. Accepted as markdown, not as MDTM.
- A 1-task file.

### Usage text (exact shape)

```
Usage: /sc:implement <path-to-spec|prd|tasklist>
STOP: need a file of enumerable tasks with acceptance criteria.
Will not implement from a feature pitch.
```

## 6. Enumerable tasks

A file is enumerable if **at least one** of these matches:

1. Markdown task items: `- [ ]` or `- [x]` or `* [ ]`.
2. Numbered items `1.` / `1)` under a heading, or `R-NNN` / `T-NNN` identifiers.
3. Headings `## Task N` / `### T1` / `## Phase N` with body text.

**Acceptance criteria** for a task, first match:

1. An `AC:` / `Acceptance:` / `Acceptance criteria` block on that item.
2. Else the item's own text (the requirement sentence is the AC).

Do not require MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`). If present, ignore them except `independent` (R-003).

If the file is prose with zero lists, zero `R-NNN`, zero task headings: STOP (R-002). Do not call `/sc:brainstorm` or `/sc:workflow` automatically.

## 7. Per-task spec-compliance QA

Steal Superpowers SDD **Part 1 only**. Do not steal Part 2 (code quality) as a gate. Do not steal executing-plans `Expected:` command match.

### Rubric (reviewer vs the brief)

Compare the **diff** (files this task changed) to:

- that task's AC
- the parent spec/PRD constraints that apply to this task
- explicit instructions on the task ("do not X", "file Y only")

Emit:

| Label | Meaning |
|---|---|
| Missing | AC/instruction not in the diff |
| Extra | behavior/files/API the brief did not ask for |
| Misunderstood | work present but solves the wrong thing |
| (none) | spec compliant |

Verdict:

- `compliant` — no Missing/Extra/Misunderstood
- `missing` / `extra` / `misunderstood` — at least one of those labels
- `cannot-verify` — diff insufficient to judge (empty diff, generated binaries only, AC refers to runtime the reviewer cannot see)

Do not re-run the full test suite as the review. Do not trust "I implemented X".

### Extras (after verdict, never instead)

Detect in repo root, run what exists, skip the rest. No flag.

| Extra | Detect | Record |
|---|---|---|
| lint | `package.json` lint script, `ruff`, `eslint`, `make lint` | `lint=pass\|fail\|skip` |
| typecheck | `tsc --noEmit`, `mypy`, `pyright`, `package.json` typecheck | `typecheck=pass\|fail\|skip` |
| tests | `package.json` test script, `make test`, `uv run pytest` (this repo) | `test=pass\|fail\|red-unrelated\|skip` |

`red-unrelated`: failing test files ∩ task-touched files = ∅.

Extras may be mentioned to the user. They do not block `complete` when verdict is `compliant`. They do not create `complete` when verdict is not `compliant`.

### 1-task source

Still run the rubric once (inline). Skip the end-of-list second pass (R-012).

## 8. One-file ledger + resume

### Location

Default: `.dev/implement/<slug>/progress.md`

- `<slug>` = basename of the source path without extension, `[a-zA-Z0-9_-]` only; other chars → `-`.
- Create the directory if missing.
- `--ledger <path>` overrides. Still one file.

Not next to the spec (avoids dirtying the source doc). Not `.claude/`. Not `docs/generated/`.

### Grammar (the whole schema)

```
# implement ledger — source: <abs-or-repo-relative-path>

Task <id>: complete | verdict=<compliant|missing|extra|misunderstood|cannot-verify> | extras: lint=<p|f|s> typecheck=<p|f|s> test=<p|f|s|red-unrelated>
Task <id>: Ruling: <what> — <why> — <cost if wrong>
```

Rules:

- One `Task <id>:` status line per task. Append-only; do not rewrite earlier `complete` lines.
- `complete` appears only with `verdict=compliant` or on the line **after** a `Ruling` for that id.
- `Ruling` is optional and only when shipping a deviation or overriding a non-compliant verdict.
- No columns, no HTML, no JSON.
- Header line is required so resume can find the source path after compaction.

### Resume

1. Open default ledger path for this source (or `--ledger`).
2. If missing, start at task 1 and create the file with the header.
3. Parse `Task <id>:` lines. Next task = first enumerable task whose id has no line containing `complete`.
4. If all enumerable tasks have `complete`, STOP with "already complete: <ledger path>". Do not re-implement unless the user passes a new path.

Trust ledger + git history after compaction. Do not ask the user to paste prior chat.

## 9. Out of scope

- Implementing from a sentence with no file
- Generating the spec/PRD/tasklist (`/sc:brainstorm`, `/sc:workflow`, `/sc:tasklist`)
- `/task` MDTM execution, `/sc:task` compliance tiers
- `/sc:tdd` (builds an MDTM task and hands to `/task`)
- `/sc:test`, `/sc:git`, `/sc:reflect` as required steps
- Auto-commit, PR open, CI watch
- Dual-mode legacy
- New MCP servers, Magic UI generation as the implementer
- Performance/security/accessibility review ensembles
- Python CLI, eval workspace, cost profile
- Changing other commands' text except a one-line pointer if they currently say `/sc:implement` is a free-form feature writer (docs follow-up; not a blocker for the two SoT files)

## 10. Positions on seed-brief open questions (lean cheapest)

| Question | Position | Why cheapest |
|---|---|---|
| Tasklist format: simple markdown vs SuperClaude phase-N | **Any markdown with enumerable tasks + AC.** Phase-N accepted as markdown; MDTM fields ignored except `independent`. | Zero parser. Zero schema. One enumerate function in prose. |
| Reviewer: inline vs fresh subagent | **Inline by default (N≤3 and source ≤400 lines). One subagent when N>3 or source >400 lines or session compacted.** Never ensemble. | Matches the brief's lean. Isolation only when context is actually fat. |
| Ledger location: `.dev/implement/<slug>/progress.md` vs next to spec | **`.dev/implement/<slug>/progress.md`.** `--ledger` override. | One known directory; does not dirty the spec; matches `.dev/` as generated-artifact root. |
| 1-task spec: per-task reviewer or skip | **Inline spec-compliance once. No second whole-list pass. No subagent.** | The gate is the product; the extra pass is not. |
| Relationship to `/sc:task` and `/task` | **Implement is the middleweight path. Those stay the heavy path. No silent routing.** | Avoids a compatibility maze. User who wants MDTM types `/task`. |

## 11. Risks / edge cases

| Risk | Handling |
|---|---|
| User pastes a pitch out of habit | STOP (R-001). No "did you mean to brainstorm". One usage line. |
| Spec is 2k lines of design with 40 implicit tasks | Enumerate only explicit list/R-NNN/task headings. If none, STOP. Do not "helpfully" slice chapters into tasks. |
| Task has no AC block | Item text is the AC. If the item is a single word with no verb ("auth"), still treat it as AC; reviewer will likely `cannot-verify` or `misunderstood` — that is correct, not a parser special case. |
| Independent tasks share a file | Parallel bound still 3; if overlap is obvious from the task text (`same file`), stay sequential. Do not build a dep graph. |
| Extras command not found | `skip`. Do not install tools. |
| `make test` is the whole SuperClaude suite on a docs-only task | Touched files disjoint → `red-unrelated` or skip if the operator sees the suite is unrelated. Prefer running the cheapest detected command (`package.json` test in the nearest package, else repo root). |
| Ruling used to skip all QA | Allowed by grammar; cost-if-wrong is mandatory on the line. Do not add a second approval ritual. |
| Two `/sc:implement` runs on the same path | Same ledger. Resume. No second directory unless `--ledger`. |
| Compaction mid-task | Resume starts that task again. Partial edits stay in the working tree; reviewer judges the eventual diff. No crash-recovery format. |
| Plugin copy drift | Edit `src/` only; `make sync-dev`; plugin sync is the existing pipeline. Spec does not add a third copy. |
| Docs (`docs/user-guide/commands.md`) still describe persona-mode implement | Follow-up in the same rewrite PR if the file names the old UX; not a new subsystem. |
| Check 3 warn if command >200 lines | Fail the rewrite if the dispatcher exceeds 150 (N-001). |

## 12. Success criteria for the rewrite

The rewrite (later `/sc:improve`) is done when all of the following are true:

1. `src/superclaude/commands/implement.md` is a thin dispatcher (≤150 lines) with Required Input, STOP usage, path-only examples, `## Activation` → `Skill sc:implement-protocol`, and **none** of: `--type`, `--framework`, `--safe`, `--with-tests`, "ready for `/sc:test`", persona activation as the method.
2. `src/superclaude/skills/sc-implement-protocol/SKILL.md` exists; loop = enumerate → implement → spec-compliance → extras → ledger line → next; SKILL.md ≤ 500 lines; at most one refs file.
3. `make lint-architecture` Check 1, 2, 6, 8, 9 pass for `implement` / `sc-implement-protocol`.
4. `make verify-sync` passes after `make sync-dev`. No `.claude/skills` or `.claude/commands` staged.
5. Grep of the two SoT files finds zero pitch examples and zero "compiles" / "ready for testing" completion criteria.
6. A fixture file with no enumerable tasks produces STOP and zero file writes.
7. A fixture with two checkbox tasks produces two ledger `complete` lines, each with a `verdict=` and an `extras:` field (values may be `skip`).
8. Resume on that ledger starts at the first task without `complete`.
9. A planted Extra in the diff yields `verdict=extra` and no next-task work until fix or Ruling.
10. No new Python module, no dual-mode flag, no `/task` handoff, no reviewer ensemble.

### Transformation path (binding)

Ship the thin dispatcher + skill with the loop in **one** cut.

Do not leave the old Analyze→Plan→Generate flow behind a flag. Do not accept `[feature-description]` as a valid invocation. Do not document "for simple features, the old command still works".

Smallest static check to leave behind: grep tests that (a) `## Activation` and `sc-implement-protocol` exist, (b) banned flags/strings are absent from the two SoT files. No protocol-simulator framework.

Skipped: dual-mode, MDTM parser, Part 2 quality review, Python CLI. Add those only if this loop fails in real use.

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-24T19:34:23.962Z","contentHash":"5524c228","sections":[{"heading":null,"hash":"fde0c02b"},{"heading":"Variant 2 — Rewrite `/sc:implement` by deletion","hash":"b7cac539"},{"heading":"1. Problem / goals","hash":"19412f08"},{"heading":"Problem","hash":"62fb910e"},{"heading":"Goals","hash":"7800eea8"},{"heading":"Non-goals (this rewrite)","hash":"96b28ae7"},{"heading":"2. Functional requirements","hash":"0a2ede0e"},{"heading":"3. NFRs","hash":"a84d0e84"},{"heading":"4. Architecture","hash":"a2245ef6"},{"heading":"What to build (two files, optionally three)","hash":"c3141d92"},{"heading":"Command file (dispatcher only)","hash":"8c9bf981"},{"heading":"Skill (the loop)","hash":"54bb7fc0"},{"heading":"What NOT to build","hash":"405829ee"},{"heading":"Delete from current `implement.md`","hash":"bc9372a7"},{"heading":"5. Input contract — STOP without spec/PRD/tasklist","hash":"3abe2e82"},{"heading":"Invocation","hash":"b9c4b391"},{"heading":"STOP (no work, print usage)","hash":"3d30d555"},{"heading":"Not STOP","hash":"485f8475"},{"heading":"Usage text (exact shape)","hash":"6dd0a2fd"},{"heading":"6. Enumerable tasks","hash":"ef5e4749"},{"heading":"7. Per-task spec-compliance QA","hash":"4060fd96"},{"heading":"Rubric (reviewer vs the brief)","hash":"c899f816"},{"heading":"Extras (after verdict, never instead)","hash":"40384880"},{"heading":"1-task source","hash":"29acd6a8"},{"heading":"8. One-file ledger + resume","hash":"00530a1b"},{"heading":"Location","hash":"29d23e30"},{"heading":"Grammar (the whole schema)","hash":"5c5ef6b3"},{"heading":"implement ledger — source: <abs-or-repo-relative-path>","hash":"4348ebb0"},{"heading":"Resume","hash":"559ea4c8"},{"heading":"9. Out of scope","hash":"52787aa8"},{"heading":"10. Positions on seed-brief open questions (lean cheapest)","hash":"e9ba5dee"},{"heading":"11. Risks / edge cases","hash":"34068d9e"},{"heading":"12. Success criteria for the rewrite","hash":"e7212746"},{"heading":"Transformation path (binding)","hash":"a92e4959"}]}-->
<!--mc:threads:end-->
