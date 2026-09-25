---
variant: 1
persona: architect
model: opus
generated: 2026-09-24
topic: sc-implement-rewrite
domain: code
status: draft-spec
soT_command: src/superclaude/commands/implement.md
soT_skill: src/superclaude/skills/sc-implement-protocol/SKILL.md
---

# Variant 1 — `/sc:implement` rewrite requirements (architect / opus)

This is a requirements specification for rewriting `/sc:implement`. It is not the rewrite. After merge, `/sc:improve` (or equivalent) implements against this spec.

Binding sources: seed brief `seed-brief.md`; `enrichment/codebase-context.md`; `enrichment/research-light.md`; current command `src/superclaude/commands/implement.md`.

---

## 1. Problem / goals

### 1.1 Problem

`/sc:implement` is a persona/MCP behavioral mode. Invocation is a free-form feature pitch. Completion is "compiles + basic functionality + ready for `/sc:test`". That job is wrong:

- It invents scope instead of executing a spec.
- It treats compile/smoke as the gate. Spec compliance is optional.
- It has no Activation, no protocol skill, no on-disk progress. Compaction loses the run.
- It overlaps `/task` (MDTM F1 + 6-agent gates) without being a lighter alternative.

### 1.2 Goal

Turn `/sc:implement` into a **middleweight spec executor**:

1. Require a path to a spec, PRD, or simple markdown tasklist. STOP otherwise.
2. Enumerate tasks from that document (simple markdown, not MDTM).
3. For each task: implement only that task, then run **spec-compliance QA** against that task's AC + spec + instructions.
4. Record one ledger line per task in one markdown file. Resume from the first incomplete line.
5. Run lint / typecheck / `npm test` (or repo equivalent) as **recorded extras**, never as pass/fail.
6. Optionally run one whole-list review at the end. Not a 6-agent `/task` phase gate.

### 1.3 Non-goals (summary)

See §11. Do not import `/task` F1, MDTM, reflect pre/post, TDD-as-primary-gate, or free-form "write this feature".

### 1.4 Design principles (binding)

1. **Spec is authority.** Deviations are ledgered rulings, never silent.
2. **One reviewer vs the brief**, not an ensemble.
3. **Thin command, fat skill.** Protocol lives in `sc-implement-protocol`. Command file must not be executable on its own.
4. **Fewest files that still split by change-rate.** Loop stays in `SKILL.md`. Rubrics that will be cited or reused go in `refs/`.
5. **Grepable ledger.** One line per task, closed-enum verdicts. No JSON, no YAML state machine, no Python runner.
6. **Do not route into `/task` or `/sc:task`.** Middleweight path stays middleweight.

---

## 2. Functional requirements

Each requirement is falsifiable: a reviewer can pass/fail it from the rewritten command + skill + a fixture run.

### 2.1 Invocation and input

**R-001.** `/sc:implement` with no resolvable path to an existing file STOP-fails before any implementation. The error MUST contain the usage string:

```text
/sc:implement requires a path to a spec, PRD, or tasklist.
Usage: /sc:implement <path> [--reviewer auto|inline|subagent] [--no-extras] [--no-whole-list-review] [--resume]
```

**R-002.** A path that does not exist on disk STOP-fails with the absolute path attempted. The protocol MUST NOT invent a spec from the leftover argument text.

**R-003.** A path that exists but yields **zero enumerable tasks** (see R-010) STOP-fails with: `"No enumerable tasks in <path>. Add a numbered list, markdown checklist, or Task headings with acceptance criteria."`

**R-004.** Invocation with only a free-form feature description (no path, or a path that is not a file) is invalid. The current examples (`/sc:implement user profile component --type component`) MUST be removed from the command file and MUST NOT remain as supported usage.

**R-005.** The command is **explicit-invocation only**. It MUST NOT auto-activate from conversational keywords ("implement", "build this", "add a feature"). Triggers section MUST list: (1) user types `/sc:implement ...`; (2) another `/sc:*` command invokes `Skill sc:implement-protocol` with a path.

**R-006.** Flags `--type`, `--framework`, `--safe`, `--with-tests` are **removed**. If present in `$ARGUMENTS`, STOP with: `"Removed flags: --type/--framework/--safe/--with-tests. Pass a spec path. Tests belong in that task's AC, not a flag."`

**R-007.** Accepted path flags are equivalent: positional `<path>`, `--spec <path>`, `--prd <path>`, `--tasklist <path>`. At most one source path. Two sources STOP.

**R-008.** `--output` (if ever added) MUST NOT resolve under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. Default ledger path is fixed (R-040); no `--output` is required in v1.

### 2.2 Architecture split

**R-009.** After rewrite, these paths exist and are the source of truth:

| Path | Role | Size gate |
|------|------|-----------|
| `src/superclaude/commands/implement.md` | Thin dispatcher | ≤150 lines target; Makefile warn >200; hard fail >500 |
| `src/superclaude/skills/sc-implement-protocol/SKILL.md` | Protocol | ≤500 lines; overflow in `refs/` |
| `src/superclaude/skills/sc-implement-protocol/refs/task-enumeration.md` | Task parse rules | loaded Wave 0 |
| `src/superclaude/skills/sc-implement-protocol/refs/spec-compliance.md` | QA rubric | loaded per-task QA |
| `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` | Ledger grammar + resume | loaded Wave 0 and on resume |

No other new packages, Python modules, CLI subcommands, or agent files are required for v1.

**R-010.** `implement.md` MUST contain a `## Activation` section whose body includes the exact invoke line:

```text
Skill sc:implement-protocol
```

and the sentence: do not execute protocol steps from the command file alone.

**R-011.** Skill frontmatter MUST include:

```yaml
name: sc:implement-protocol
description: "<one line: middleweight spec executor; require spec/PRD/tasklist path>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, TodoWrite, Task, Skill
```

`name:` MUST end with `-protocol` (Makefile Check 9). Description MUST mention the required path so the skill does not look like a free-form implementer.

**R-012.** `make lint-architecture` MUST pass after the rewrite (Check 1 command→`sc-implement-protocol`, Check 2 skill→command, Check 6 Activation present, Check 8 frontmatter, Check 9 name suffix).

**R-013.** Edit SoT under `src/superclaude/` only. After edits, `make sync-dev` then `make verify-sync`. `.claude/skills/sc-implement-protocol/` and `.claude/commands/sc/implement.md` (or equivalent sync targets) are generated mirrors and MUST NOT be staged.

**R-014.** Command `## Behavioral Flow` (or equivalent) MAY list parse → validate path → invoke skill → surface ledger path. It MUST NOT contain the per-task loop, QA rubric, or ledger grammar.

### 2.3 Task enumeration (simple markdown, not MDTM)

**R-015.** Load `refs/task-enumeration.md` once in Wave 0. Enumerable tasks are discovered in this order, first match wins for the whole document (do not mix extractors):

1. Markdown checklists: lines matching `^- \[[ xX]\] `.
2. Numbered lists of work items: `^[0-9]+\.\s+` at heading-or-body scope where the item has a verb (implement/add/fix/write/create/update/remove) **or** an explicit AC subsection.
3. Headings matching `^#{2,4}\s+(Task|T|Item)[\s:-]*([0-9A-Za-z.-]+)` (e.g. `## Task 3`, `### T001`).

If none match, zero tasks → R-003.

**R-016.** MDTM task files (frontmatter with `id:` + `## Task Log` / B2 self-contained checklist under `.dev/tasks/`) are **not** implement input. If the file matches MDTM shape, STOP with: `"This looks like an MDTM task file. Run /task <path>, not /sc:implement."` Do not silently re-route.

**R-017.** SuperClaude phase-N tasklists (markdown with phase headings and numbered/checklist items) **are** accepted. Enumerate the work items. Ignore MDTM-only fields (agent prompts, spawn directives, compliance tiers). Do not execute F1.

**R-018.** Each enumerated task MUST be assigned a stable id `TNNN` (T001, T002, …) in document order. If the source already labels `T001` / `Task 3`, keep that label when unique; otherwise assign sequentially. Ids MUST NOT change on resume.

**R-019.** Each task record has exactly these fields (in-memory + ledger title column):

| Field | Required | Source |
|-------|----------|--------|
| `id` | yes | R-018 |
| `title` | yes | first line / heading text, stripped of checkbox markup |
| `instructions` | yes | body under the item until the next item |
| `ac[]` | yes | see R-020 |
| `files[]` | no | paths the source names; else filled after implement from the task's diff |
| `independent` | no | true only if the source marks it independent (R-022) |

**R-020.** Acceptance criteria extraction, in order:

1. A subsection titled `Acceptance criteria` / `AC` / `Done when` under the item.
2. Checkbox children of the item.
3. Sentences in the item body containing `MUST` / `SHALL` / `must` / `done when`.
4. Fallback: the entire item body is the single AC.

If after (4) the body is empty or a single vague phrase with no observable outcome (e.g. "make it better"), keep the task but the QA verdict on that task MUST be `cannot-verify` unless the user supplies AC before implement starts. The protocol MUST print the missing-AC warning **before** writing code for that task and wait one turn if the session is interactive. Non-interactive: ledger `blocked` + HALT (R-036).

**R-021.** Default execution order is **sequential** in document order.

**R-022.** Parallel execution is allowed only when the source **explicitly** marks a set independent (`independent: true`, a heading `Independent`, or a bullet `parallel-ok`). Max **3** concurrent implementers. QA still runs per task before the next wave. If the source is silent, sequential.

**R-023.** A 1-task document is valid. It still gets implement + spec-compliance QA + extras (R-050). Whole-list review is skipped (R-060). Reviewer is inline (R-033).

### 2.4 Per-task loop

**R-024.** After Wave 0 (parse, ledger create/resume), the protocol loops:

```text
IDENTIFY next incomplete task from ledger
  → IMPLEMENT only that task
  → EXTRAS (optional, recorded)
  → SPEC-COMPLIANCE QA vs that task's AC + parent spec + instructions
  → APPEND/UPDATE ledger line
  → HALT or CONTINUE
```

Re-read the ledger from disk at the start of each iteration (compaction-safe). Do not trust session memory for "what's next".

**R-025.** IMPLEMENT for task N MAY edit only files required for that task's AC. Drive-by refactors, extras, and "while I'm here" files that are not implied by the AC are `extra` (R-029).

**R-026.** Before significant edits, call `mcp__auggie__codebase-retrieval` once per task (or skip with a ledger note if auggie is unavailable). Unavailability is a warning, not a STOP.

**R-027.** Domain personas (frontend/backend/security/…) MUST NOT all activate at start. Activate at most one persona per task, and only when the task's files/domain clearly warrant it. Default: no persona cocktail.

**R-028.** After IMPLEMENT, run spec-compliance QA. The reviewer MUST NOT trust the implementer's summary. Compare the **diff for this task** (files touched since the previous ledger `complete` line, or `git diff` against the task-start ref recorded on the `in-progress` line) to:

- that task's `ac[]`
- that task's `instructions`
- parent spec constraints that apply globally (named "Constraints", "Out of scope", "Non-negotiable", or equivalent)

Load `refs/spec-compliance.md` for this step. Do not load reflect-protocol.

**R-029.** Closed-enum findings (Part 1 only — spec compliance):

| Finding | Meaning |
|---------|---------|
| `missing` | An AC or required instruction is not satisfied by the diff |
| `extra` | The diff adds behavior/files not asked for and not required to satisfy AC |
| `misunderstood` | The diff addresses the task but implements a different interpretation than the written AC |
| none | no findings |

**R-030.** Closed-enum verdicts (exactly one per task per QA pass):

| Verdict | When |
|---------|------|
| `spec-compliant` | no findings |
| `missing` | ≥1 missing, no misunderstood required |
| `extra` | only extra findings |
| `misunderstood` | ≥1 misunderstood (dominates extra) |
| `cannot-verify` | diff or AC insufficient to judge (empty diff, generated binaries, AC still vague after R-020) |

If both missing and extra: verdict `missing` (unmet AC is the gate). Record extra findings on the same ledger line after the verdict.

**R-031.** `spec-compliant` → mark task `complete`, proceed to next task.

**R-032.** `missing` | `extra` | `misunderstood` → do **not** proceed to the next task. Protocol MUST:

1. Write the findings into the ledger (status `in-progress` or `blocked`, verdict set).
2. Attempt **exactly one** fix pass (implement the findings, re-QA).
3. If the second QA is `spec-compliant`, mark `complete` and continue.
4. If the second QA still fails, HALT (R-036). Do not loop.

**R-033.** Reviewer mode (`--reviewer`, default `auto`):

| Mode | When |
|------|------|
| `inline` | same session; default when task count ≤ 3 and estimated context is not fat |
| `subagent` | `Task` tool, fresh reviewer, no implementer memory; default when task count > 3 **or** the implementer just compacted **or** the user passed `--reviewer subagent` |
| `auto` | apply the table above per run (not per task): one mode for the whole run |

A 1-task spec uses `inline`. Subagent reviewer prompt MUST include the task record, the parent constraints, and the diff; MUST exclude the implementer's self-assessment. Part 2 (code quality) is **out of scope** for the per-task gate (optional whole-list review may comment on quality).

**R-034.** `cannot-verify`: mark `blocked`, HALT, ask the user for AC or a ruling. Do not treat as pass. Do not skip.

**R-035.** User ruling: a message that authorizes deviation. Append a ledger line:

```text
T00N | Ruling: <what> — <why> — cost-if-wrong: <cost>
```

After a ruling, the task may be marked `complete` (accepted deviation) or `skipped`. Without a ruling line, a failed QA MUST NOT be marked `complete`.

**R-036.** HALT means: stop the loop, print ledger path, print the blocking task id + verdict + findings, print the exact next user action (`fix`, `ruling`, or `resume`). Do not start the next task.

### 2.5 Ledger

**R-040.** Ledger path is:

```text
.dev/implement/<slug>/progress.md
```

`<slug>` = source file basename without extension, lowercased, `[^-a-z0-9]+` → `-`, trimmed, max 64 chars. If that directory already has a `progress.md` whose `source:` frontmatter path equals this source, reuse it (resume). If it exists for a **different** source path, append `-2`, `-3`, … to the slug.

**R-041.** Ledger lives under `.dev/implement/`, not next to the spec. Specs are often committed; progress is run state. `.dev/implement/` SHOULD be gitignored if not already; the protocol MUST NOT `git add` the ledger.

**R-042.** File shape (exact grammar in `refs/ledger.md`):

```markdown
---
source: <absolute path>
slug: <slug>
started: <ISO-8601>
reviewer: inline|subagent
---

# Implement ledger — source: <path>

T001 | complete | spec-compliant | extras: ruff=recorded pytest=recorded | files: src/foo.py
T002 | in-progress | — | start-ref: <git sha or 'unborn'> | files:
T002 | missing | missing: AC-2 not in diff; extra: src/util.py | extras: ruff=recorded
T002 | Ruling: keep src/util.py — shared helper required by AC-2 — cost-if-wrong: unused if AC-2 drops
T003 | pending | — | <title>
```

**R-043.** One data line per event. Status vocabulary is closed: `pending` | `in-progress` | `complete` | `blocked` | `skipped`. Verdict vocabulary is R-030 plus `—` for not-yet-run.

**R-044.** Resume algorithm: re-read `progress.md`; next task = first `TNNN` whose latest status is not `complete` and not `skipped`, in id order. Trust ledger + `git log` / `start-ref`, not chat memory. After compaction, the first action is Read ledger + Read source, then continue.

**R-045.** `--resume` is the default when a matching ledger exists. Starting over requires `--fresh` (deletes or archives `progress.md` to `progress-<ts>.md` then creates a new file). Without `--fresh`, do not re-implement `complete` tasks.

**R-046.** On first create, write all tasks as `pending` in one pass, then set T001 (or the first incomplete) to `in-progress` with `start-ref`.

### 2.6 Cheap extras (never the gate)

**R-050.** After implement and **before** spec-compliance QA, if `--no-extras` is not set, detect and run **at most one** of each class when the repo has it:

| Class | Detection | Command |
|-------|-----------|---------|
| lint | `ruff` / `eslint` / `biome` config or script | existing project command; SuperClaude repo: `make lint` is **not** required (it runs lint-architecture). Prefer `uv run ruff check` on **this task's files** |
| typecheck | `mypy` / `tsc` / `pyright` config | scoped to this task's files when the tool allows |
| tests | `package.json` scripts.test / `pytest` / `uv run pytest` | run the repo's default unit command |

Record stdout/stderr **existence and command** on the ledger line as `extras: <tool>=recorded`. Do **not** record pass/fail as the task verdict. Do not parse TAP/JUnit into the gate.

**R-051.** A red test suite whose failures are **outside this task's files** (files not in the task diff and not named in the task record) is **not** a fail of this task. Note `extras: pytest=recorded (failures outside task files)` and continue to spec-compliance.

**R-052.** A red test that **does** touch this task's files is still not the spec-compliance verdict. Note it on the extras field. If the AC required those tests to pass, spec-compliance captures it as `missing`. If the AC did not mention tests, extras stay informational.

**R-053.** Missing toolchain: skip that class, record `extras: tsc=absent`. Not a STOP.

**R-054.** TDD (red-green-refactor, watch-the-fail) is not the per-task protocol. Tests are written when the task AC says so.

### 2.7 Whole-list review (optional, end only)

**R-060.** After every task is `complete` or `skipped`, if task count ≥ 2 and `--no-whole-list-review` is not set, run **one** whole-list review: diff of the full run vs the parent spec. Output: `.dev/implement/<slug>/whole-list-review.md`. This is advisory. It MUST NOT reopen completed tasks unless the user says so.

**R-061.** 1-task runs skip whole-list review (the per-task QA already compared the only task to the spec).

**R-062.** Whole-list review is one reviewer (inline if `--reviewer inline`, else one subagent). Not 6 agents. Not `/sc:reflect`. Not `/task` phase-gate QA.

**R-063.** `--no-whole-list-review` skips R-060 even for long lists.

### 2.8 Surfaces, related commands, completion of a run

**R-070.** On success (all tasks `complete` or `skipped`): print ledger path, counts (`complete/skipped/blocked`), extras-ran boolean, whole-list review path or `skipped`. Suggest `/sc:test` and `/sc:git` as optional next steps, not as gates.

**R-071.** Related-commands section MUST state:

| Command | Relationship |
|---------|--------------|
| `/task` | Heavy MDTM executor. Out of scope. No silent routing. |
| `/sc:task` | Compliance-tiered execution. Out of scope. No silent routing. |
| `/sc:tdd` | Builds MDTM then `/task`. Out of scope. |
| `/sc:workflow` | Generates workflows from PRDs; does not execute. Upstream producer of specs. |
| `/sc:reflect` | Post-hoc audit. Not invoked by implement v1. |
| `/sc:test`, `/sc:git` | Optional after a successful run. |
| `/sc:brainstorm`, `/sc:design`, `/sc:tasklist` | Producers of the spec/tasklist implement consumes. |

**R-072.** Plugin mirror `plugins/superclaude/commands/implement.md` is produced by `make build-plugin` / `make sync-dev` as applicable. Do not hand-edit plugin copies.

---

## 3. Non-functional requirements

**NFR-001. Token budget.** SKILL.md + currently loaded ref ≤ ~8k tokens of protocol text at any moment. Load refs per phase; never preload all refs.

**NFR-002. Compaction survivability.** After a compact, Read `progress.md` + source path from frontmatter is sufficient to resume. No dependency on TodoWrite or chat.

**NFR-003. Command file size.** `implement.md` ≤150 lines. If examples would blow the cap, keep 3 examples max (STOP, 1-task, tasklist).

**NFR-004. Skill file size.** `SKILL.md` ≤500 lines. Rubrics in `refs/`.

**NFR-005. No new runtime dependencies.** No new Python package, no new MCP server required. Optional: auggie (R-026), context7 when the spec names a library.

**NFR-006. MCP defaults.** `mcp-servers` on the command: `[auggie, context7]`. Sequential/Magic/Playwright are not default. Playwright only if a task AC requires browser evidence.

**NFR-007. Latency.** Per-task QA inline target ≤ 2 minutes of reviewer work for a small diff. Subagent reviewer allowed to cost more when R-033 selects it.

**NFR-008. Parsability.** Ledger lines MUST remain grepable with `^\s*T[0-9A-Za-z.-]+ \|`. Future tools may parse this; do not break the pipe-separated shape in v1.

**NFR-009. Security / trust boundaries.** The protocol implements what the spec says. It MUST still refuse criminal assistance, secret-committing, and `.claude/` staging per repo CLAUDE.md. Spec-compliance is not a license to violate those.

**NFR-010. Accessibility / validation.** Not applicable beyond: trust-boundary input is the spec path (R-001). No extra config schema.

**NFR-011. Extension seams (v1 only these):**

- Verdict enum in `refs/spec-compliance.md` (add a value later without rewriting the loop).
- Ledger path prefix `.dev/implement/` (do not hardcode a second location).
- Reviewer mode flag (inline vs subagent) so a later version can default differently without a protocol rewrite.

Do not add a plugin API, webhook, or "executor interface" in v1.

---

## 4. Architecture

### 4.1 Target shape

```text
User → /sc:implement <path>
         │
         ▼
src/superclaude/commands/implement.md     # flags, STOP copy, Activation only
         │  Skill sc:implement-protocol
         ▼
src/superclaude/skills/sc-implement-protocol/SKILL.md
         │
         ├─ Wave 0  Read refs/task-enumeration.md, refs/ledger.md
         │            parse path → tasks → open/resume progress.md
         │
         ├─ Loop    implement task N
         │            extras (lint/typecheck/tests) recorded
         │            Read refs/spec-compliance.md
         │            QA → ledger line → next or HALT
         │
         └─ End     optional whole-list-review.md
```

### 4.2 Activation pattern (copy this)

Command file, after Usage/Options/Boundaries:

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:implement-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill at
`src/superclaude/skills/sc-implement-protocol/SKILL.md`.
```

This matches `reflect.md`, `brainstorm.md`, `auggie-review.md`.

### 4.3 Makefile / sync

| Check | Expectation after rewrite |
|-------|---------------------------|
| lint-architecture Check 1 | `implement.md` has `## Activation` → dir `src/superclaude/skills/sc-implement-protocol/` |
| Check 2 | that skill dir has matching `commands/implement.md` |
| Check 3 | command ≤200 lines (warn) |
| Check 4 | command ≤500 lines (error) |
| Check 6 | Activation heading present |
| Check 8 | SKILL.md has `name:`, `description:`, `allowed-tools:` |
| Check 9 | `name:` ends with `-protocol` |
| `make sync-dev` | mirrors into `.claude/` |
| `make verify-sync` | src and `.claude/` match |

Checks 5 and 7 are currently `NEEDS DESIGN` in the Makefile; this rewrite MUST NOT wait on them. Check 7 (activation references the correct skill) is satisfied in practice by R-010 even if the Makefile skips it.

### 4.4 What lives where

| Concern | File | Why |
|---------|------|-----|
| Usage, flags, STOP one-liners, Will/Will-not, related commands | `commands/implement.md` | loaded on slash; keep small |
| Wave 0, loop, HALT, extras detection, whole-list trigger | `skills/sc-implement-protocol/SKILL.md` | change with the loop |
| Extractors, AC fallback | `refs/task-enumeration.md` | tweak without retouching the loop |
| Finding/verdict definitions, dominance rules | `refs/spec-compliance.md` | cited by subagent reviewer; reusable later |
| Line grammar, resume, slug rules | `refs/ledger.md` | must stay exact; reviewers grep it |

### 4.5 Deliberately not built

- No `sc-implement` utility skill (non-`-protocol` alt). Check 1 would pass, but every modern `/sc:*` executor uses `-protocol`.
- No Python `superclaude implement` CLI.
- No new agent markdown under `src/superclaude/agents/`.
- No copy of F1, execution-log tables, TurnLedger, or reflect `per_task_verdicts`.

---

## 5. Input contract

### 5.1 STOP unless a spec/PRD/tasklist path is given

Valid:

```text
/sc:implement docs/prd/foo.md
/sc:implement --spec .dev/brainstorms/<id>/merged-requirements.md
/sc:implement --tasklist .dev/tasklists/foo.md
/sc:implement --prd docs/prd.md --resume
```

Invalid (STOP):

```text
/sc:implement
/sc:implement user profile component
/sc:implement --type api --with-tests
/sc:implement .dev/tasks/to-do/TASK-FOO/TASK-FOO.md    # MDTM → point at /task
```

### 5.2 Task enumeration rules (normative summary)

Full algorithm: `refs/task-enumeration.md` (R-015–R-023). Short version:

- Simple markdown only: checklists, numbered work items, Task headings.
- Not MDTM. Not a JSON schema. Not a required SuperClaude template.
- AC required in spirit; fallback to body; vague body → `cannot-verify` / block, not invention.
- Independent parallel only when marked.

### 5.3 Command frontmatter (target)

```yaml
name: implement
description: "Middleweight spec executor — walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger"
category: workflow
complexity: standard
mcp-servers: [auggie, context7]
personas: []
argument-hint: "<path-to-spec-or-prd-or-tasklist> [--reviewer auto|inline|subagent] [--no-extras] [--no-whole-list-review] [--resume|--fresh]"
```

Empty `personas:` is intentional (R-027). Do not restore the five-persona cocktail.

---

## 6. Per-task loop (normative)

See R-024–R-036. Sequence for task N:

1. Ledger: set `in-progress`, record `start-ref` (HEAD sha, or `unborn` if no git).
2. Read task instructions + AC + global constraints.
3. Auggie retrieve (best-effort).
4. Implement the smallest diff that can satisfy AC.
5. Extras (R-050–R-054).
6. Spec-compliance QA (inline or subagent per R-033).
7. Verdict:
   - `spec-compliant` → `complete` → next.
   - fail → one fix → re-QA → `complete` or HALT.
   - `cannot-verify` → `blocked` → HALT.
8. Never start N+1 while N is `in-progress` or `blocked` without a `Ruling:` or `skipped`.

### 6.1 When to halt (closed list)

| Condition | Action |
|-----------|--------|
| No path / missing file / two sources / removed flags | STOP before ledger |
| Zero enumerable tasks | STOP before loop |
| MDTM file | STOP, name `/task` |
| Vague AC on current task, interactive | wait one turn; then block |
| Vague AC, non-interactive | `blocked` + HALT |
| QA fail after one fix | HALT |
| `cannot-verify` | HALT |
| User interrupt | leave `in-progress`; `--resume` later |
| Compaction mid-task | resume as `in-progress`; do not double-append pending lines |

---

## 7. Simple ledger

One file, one line per event, resume from first incomplete: R-040–R-046.

Path: `/config/workspace/<repo>/.dev/implement/<slug>/progress.md` (repo-relative `.dev/implement/<slug>/progress.md`).

Resume = first `TNNN` whose latest status ∉ {`complete`, `skipped`}.

---

## 8. Cheap extras

R-050–R-054. Recorded, never the pass/fail. Red suite outside this task's files is not a fail.

---

## 9. Optional whole-list review

R-060–R-063. End of run, ≥2 tasks, one reviewer, advisory. Not a phase gate.

---

## 10. Flags (closed set)

| Flag | Default | Effect |
|------|---------|--------|
| `<path>` / `--spec` / `--prd` / `--tasklist` | required | source document |
| `--reviewer auto\|inline\|subagent` | `auto` | R-033 |
| `--no-extras` | off | skip R-050 |
| `--no-whole-list-review` | off | skip R-060 |
| `--resume` | implicit if ledger exists | R-045 |
| `--fresh` | off | archive ledger and start over |

No other flags in v1.

---

## 11. Explicit out of scope

| Item | Why |
|------|-----|
| `/task` F1 (`READ → IDENTIFY → EXECUTE → UPDATE → REPEAT` with MDTM item semantics) | Heavy ledger; different job |
| 6-agent phase-gate QA | User rejected ensemble cost |
| MDTM templates, B2 items, task-builder output as input | R-016 STOP |
| `/sc:reflect` pre/post inside the loop | Reflect is an audit; implement is an executor |
| Free-form "write this feature" | R-004 |
| TDD-as-primary-gate / `Expected:` test-runner match | User rejected; extras only |
| Mattpocock end-of-batch suite + one `/code-review` | No per-task spec QA |
| `feature-dev` 7-phase explore→design→implement | Too heavy; still one review at the end |
| Persona cocktail + Magic/Playwright defaults | Old command; restore only if a task AC needs them |
| Silent routing to `/sc:task` or `/task` | Middleweight path must stay callable without MDTM |
| Python CLI, JSON ledger, new agent files | YAGNI |
| Per-task code-quality Part 2 | Whole-list review may mention quality; not the gate |
| Auto-commit / auto-PR | User runs `/sc:git` if they want |

---

## 12. Open questions — positions

### Q1. Tasklist format: simple markdown vs SuperClaude phase-N?

**Position: accept any markdown with enumerable tasks + AC. Do not require MDTM. Phase-N tasklists are just markdown (R-017).**

Rationale: the seed's lean is correct. Requiring a SuperClaude template recreates `/sc:tasklist` lock-in and blocks PRDs from `/sc:brainstorm`. Phase-N files already contain checklists; enumerating them is cheaper than rejecting them. MDTM is the opposite shape (executor-embedded prompts) and would pull F1 in by accident — hence the hard STOP (R-016).

### Q2. Reviewer: inline vs fresh subagent?

**Position: `auto` — inline when ≤3 tasks and context is not fat; subagent when >3 tasks, after compaction, or on `--reviewer subagent` (R-033). One mode for the whole run.**

Rationale: Superpowers SDD isolation is real (implementers rubber-stamp themselves). Paying a subagent on a 1-task typo fix is ceremony. Switching mode *per task* makes the ledger and resume harder. Fat context is the actual failure mode, not task count alone — hence the compaction clause.

### Q3. Where does the ledger live?

**Position: `.dev/implement/<slug>/progress.md` (R-040). Not next to the spec.**

Rationale: SuperClaude already writes run artifacts under `.dev/` (`reviews/`, `reflect/`, `brainstorms/`). Spec-adjacent `progress.md` gets committed, bikeshedded, and collides when two runs share a spec. Slug-from-basename is enough; do not hash paths in v1.

### Q4. Does a 1-task spec still get the per-task reviewer?

**Position: yes — implement + spec-compliance QA + extras. Skip whole-list review. Force inline (R-023, R-061).**

Rationale: the primary gate is AC-vs-diff. Dropping it for "small" work reintroduces compile-as-done. Whole-list review would duplicate the same comparison.

### Q5. Relationship to `/sc:task` and `/task`?

**Position: implement is the middleweight path. Those remain the heavy path. No silent routing. MDTM file → STOP with `/task` pointer (R-016, R-071).**

Rationale: silent routing hides cost and ceremony. Users who wanted F1 already have `/task`. Users who wanted a spec walk should not inherit six agents.

---

## 13. Risks and edge cases

| Case | Required behavior |
|------|-------------------|
| Empty spec (file exists, no tasks) | R-003 STOP |
| 1-task spec | R-023: full per-task QA, no whole-list, inline |
| 20-task spec | Sequential (unless marked independent). `--reviewer subagent`. Warn once: "20 tasks; compaction likely; ledger is the source of resume." Do not auto-split into multiple ledgers. Optional whole-list at the end. |
| Compaction mid-run | R-044: Read ledger + source; continue first incomplete. If current task is `in-progress` without a complete diff, resume implement (do not reset to pending). |
| Missing AC | R-020: warn; interactive wait; else `cannot-verify` / `blocked` |
| Spec path is a directory | STOP (not a file) |
| Spec is binary / empty file | zero tasks → R-003 |
| Two checklists in one file | First matching extractor wins; document that in `task-enumeration.md` |
| Task files overlap | Allowed; extras scoped to this task's diff only |
| Independent mark on some but not all | Parallel only the marked clique; others sequential |
| Ledger exists for same source, some complete | Default resume; `--fresh` to restart |
| Ledger exists, source file changed | Resume anyway; Wave 0 re-enumerates; new tasks append as `pending`; removed tasks that were `pending` are dropped; `complete` tasks stay complete even if removed from source (note in ledger header `source-drift: true`) |
| Git unavailable | `start-ref: unborn`; extras/git diff fall back to "files written this task" list the implementer recorded — weaker QA, still run |
| Auggie unavailable | Warn, continue |
| User pastes AC in chat after HALT | Treat as ruling+AC update: append to ledger, set task `in-progress`, continue. Do not require editing the spec (spec remains authority; chat AC is a dated ruling) |
| Implementer "fixes" extras failures in unrelated files | `extra` finding |
| All tasks skipped via rulings | Success path with counts; skip whole-list |

### 13.1 Risks

| Risk | Mitigation |
|------|------------|
| Command file keeps old examples; users keep pitching features | R-004 deletes them; Triggers become explicit-only |
| SKILL.md grows into a second `/task` | Size cap + 3 refs + out-of-scope table |
| Reviewer rubber-stamps | Subagent when >3; reviewer prompt forbids trusting the implementer report |
| Extras become the gate in practice | Ledger grammar has no place for extras pass/fail as verdict |
| `.dev/implement/` committed | R-041; add gitignore pattern if missing as part of the rewrite |
| Check 1 fails because skill dir named `implement` | Directory MUST be `sc-implement-protocol` |
| Plugin copies drift | `make sync-dev` / `build-plugin`; never hand-edit mirrors |

---

## 14. Success / completion criteria for the rewrite itself

The rewrite of `/sc:implement` is done when all of the following are true:

1. **SoT files exist** at `src/superclaude/commands/implement.md` and `src/superclaude/skills/sc-implement-protocol/{SKILL.md,refs/task-enumeration.md,refs/spec-compliance.md,refs/ledger.md}`.
2. **Activation** line is `Skill sc:implement-protocol`. Command has no per-task loop.
3. **`make lint-architecture`** exits 0. **`make sync-dev && make verify-sync`** exits 0.
4. **Removed** from command: `--type`, `--framework`, `--safe`, `--with-tests`, free-form feature examples, five-persona cocktail, Analyze→Plan→Generate→Validate→Integrate as the completion story, "ready for `/sc:test`" as the definition of done.
5. **STOP copy** for missing path is in both command (usage) and skill (Wave 0). A dry read of the skill shows Wave 0 returns before Write/Edit on application code when path is missing.
6. **Ledger grammar** matches R-042 (pipe-separated, closed enums). Resume documented as first non-complete/non-skipped id.
7. **QA rubric** lists Missing / Extra / Misunderstood / cannot-verify and the dominance rule (R-030).
8. **Out-of-scope** list appears in the command Boundaries **Will Not**.
9. **No** new Python modules, no MDTM, no reflect invoke, no F1 copy.
10. **Eval fixtures** (minimal, under `.dev/eval-workspaces/sc-implement/`):
    - `fx-stop-nopath` — protocol text requires STOP.
    - `fx-empty-spec` — file with no tasks → STOP.
    - `fx-one-task` — one AC item → loop runs QA, no whole-list.
    - `fx-mdtm-reject` — MDTM-shaped file → STOP pointing at `/task`.
    These are markdown fixtures + expected STOP/ledger lines, not a reflect-style grader. One `README.md` in that folder telling a human or `/sc:improve` how to walk them is enough.

11. **Related docs:** if `COMMANDS.md` or user-facing command index lists `/sc:implement` as "feature from description", update that sentence to "spec/PRD/tasklist executor". Do not write a new essay.

### 14.1 Done-when for a later `/sc:improve` pass (acceptance of *this spec*)

- Every R-00x and NFR-00x is either implemented or explicitly waived in the improve log with a ruling line.
- A reviewer can fail the rewrite by pointing at a missing STOP, a missing skill dir, extras used as the gate, or F1/MDTM imported.

---

## 15. Command file skeleton (normative outline, not implementation)

Sections in order:

1. YAML frontmatter (R-003 / §5.3)
2. Title + one-paragraph purpose (middleweight executor)
3. `## Triggers` (explicit only)
4. `## Required Input` (STOP + usage string)
5. `## Usage` + `## Options` (closed flag table)
6. `## Behavioral Flow` (four bullets: parse, validate, activate skill, surface ledger)
7. `## Activation` (R-010)
8. `## MCP Integration` (auggie, context7)
9. `## Examples` (exactly three: STOP, `--spec` 1-task, tasklist resume)
10. `## Boundaries` Will / Will Not (include §11)
11. `## Related Commands` (R-071)
12. `## Completion` — run is done when ledger has no `pending`/`in-progress`/`blocked`; extras and `/sc:test` are not the definition of done

---

## 16. Skill file skeleton (normative outline, not implementation)

`SKILL.md`:

1. Frontmatter (R-011)
2. Purpose (6-line cap)
3. Required input / STOP table
4. Wave 0: resolve path, load enumeration + ledger refs, open/resume ledger
5. Loop (R-024)
6. HALT table
7. Extras detection (short; details can stay here — not a fourth ref)
8. End: whole-list trigger
9. Return contract: `status` (`success` \| `halted` \| `stopped-precondition`), `ledger_path`, `blocked_task`, `counts`

`refs/spec-compliance.md` MUST be written so a subagent can be pointed at it with the task record + diff and return exactly one verdict enum value plus finding bullets.

---

End of variant 1 spec.

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-24T19:35:26.296Z","contentHash":"9151134b","sections":[{"heading":null,"hash":"cb65719c"},{"heading":"Variant 1 — `/sc:implement` rewrite requirements (architect / opus)","hash":"eed3fd21"},{"heading":"1. Problem / goals","hash":"19412f08"},{"heading":"1.1 Problem","hash":"70a1845c"},{"heading":"1.2 Goal","hash":"c9840a41"},{"heading":"1.3 Non-goals (summary)","hash":"c75b2a19"},{"heading":"1.4 Design principles (binding)","hash":"1a9290c4"},{"heading":"2. Functional requirements","hash":"235bd311"},{"heading":"2.1 Invocation and input","hash":"45ef00ee"},{"heading":"2.2 Architecture split","hash":"b9807757"},{"heading":"2.3 Task enumeration (simple markdown, not MDTM)","hash":"8e85ee9c"},{"heading":"2.4 Per-task loop","hash":"c32317c0"},{"heading":"2.5 Ledger","hash":"49d8c6eb"},{"heading":"Implement ledger — source: <path>","hash":"e4d7f96e"},{"heading":"2.6 Cheap extras (never the gate)","hash":"7943f708"},{"heading":"2.7 Whole-list review (optional, end only)","hash":"a568dcd7"},{"heading":"2.8 Surfaces, related commands, completion of a run","hash":"0bf4d836"},{"heading":"3. Non-functional requirements","hash":"54261ecc"},{"heading":"4. Architecture","hash":"a2245ef6"},{"heading":"4.1 Target shape","hash":"7a648f45"},{"heading":"4.2 Activation pattern (copy this)","hash":"f23bf0c9"},{"heading":"Activation","hash":"c9c73189"},{"heading":"4.3 Makefile / sync","hash":"17223604"},{"heading":"4.4 What lives where","hash":"ec9ef4f5"},{"heading":"4.5 Deliberately not built","hash":"f47c1437"},{"heading":"5. Input contract","hash":"ba673cb8"},{"heading":"5.1 STOP unless a spec/PRD/tasklist path is given","hash":"a69b2e0a"},{"heading":"5.2 Task enumeration rules (normative summary)","hash":"8b11cd1a"},{"heading":"5.3 Command frontmatter (target)","hash":"babe3936"},{"heading":"6. Per-task loop (normative)","hash":"01e60177"},{"heading":"6.1 When to halt (closed list)","hash":"b635f26f"},{"heading":"7. Simple ledger","hash":"2ea3c28a"},{"heading":"8. Cheap extras","hash":"5928078a"},{"heading":"9. Optional whole-list review","hash":"588eb3b7"},{"heading":"10. Flags (closed set)","hash":"119b5e01"},{"heading":"11. Explicit out of scope","hash":"4588d138"},{"heading":"12. Open questions — positions","hash":"f63cd559"},{"heading":"Q1. Tasklist format: simple markdown vs SuperClaude phase-N?","hash":"2f163063"},{"heading":"Q2. Reviewer: inline vs fresh subagent?","hash":"013cc5a8"},{"heading":"Q3. Where does the ledger live?","hash":"6b8348cf"},{"heading":"Q4. Does a 1-task spec still get the per-task reviewer?","hash":"31bf1fd6"},{"heading":"Q5. Relationship to `/sc:task` and `/task`?","hash":"b9b8f754"},{"heading":"13. Risks and edge cases","hash":"6f6c7b67"},{"heading":"13.1 Risks","hash":"222979ea"},{"heading":"14. Success / completion criteria for the rewrite itself","hash":"efd74b41"},{"heading":"14.1 Done-when for a later `/sc:improve` pass (acceptance of *this spec*)","hash":"2281f8cb"},{"heading":"15. Command file skeleton (normative outline, not implementation)","hash":"8edef76a"},{"heading":"16. Skill file skeleton (normative outline, not implementation)","hash":"1a280702"}]}-->
<!--mc:threads:end-->
