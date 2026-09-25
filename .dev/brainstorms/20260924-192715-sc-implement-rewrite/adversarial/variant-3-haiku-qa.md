---
variant: 3
persona: qa
model: haiku
generated: 2026-09-24
topic: sc-implement-rewrite
bias: acceptance-criteria-and-failure-modes
---

# Variant 3 — `/sc:implement` rewrite spec (QA / haiku)

Binding authority for this variant: **testable acceptance criteria, halt rules, evidence contract**. If a later merge drops an AC, the corresponding requirement is untestable and MUST be rewritten or deleted — not left as prose.

## 1. Problem / goals

### Problem

`/sc:implement` is a persona/MCP behavioral mode. Invocation is free-form (`/sc:implement user profile component --type component`). Done-when is "compiles + basic functionality + ready for `/sc:test`". That ships invented features and treats lint/compile as the gate.

### Goals (falsifiable)

| ID | Goal | Fail if |
|----|------|---------|
| G-1 | Executor, not inventor | Any run that writes product code without a resolved source path |
| G-2 | Per-task spec QA is the gate | A task is marked complete because lint/tests passed while AC evidence is missing |
| G-3 | Cheap extras never sole-gate | A task is marked fail solely because lint/typecheck/`npm test` is red |
| G-4 | Middleweight ledger | Protocol imports `/task` F1, 6-agent phase gates, MDTM, or reflect pre/post as the per-task gate |
| G-5 | Thin dispatcher | `implement.md` contains protocol steps instead of `Skill sc:implement-protocol` |
| G-6 | No silent legacy | `/sc:implement user profile component --type component` writes code or maps flags |

## 2. Functional requirements

Each requirement has one or more ACs. Reviewer evidence MUST cite `file:line` of the command/skill **or** the AC id below. "Looks right" is not evidence.

### R-001 — Required source path

The command accepts a source that is a spec, PRD, or tasklist path. It does not accept a blank feature pitch.

**AC-001.1** Given argv with no path and no `@file`, when `/sc:implement` is invoked, then the run STOPs with usage (exit-class `E-NO-SOURCE`), writes no product files, and creates no ledger.

**AC-001.2** Given a path that does not exist, when invoked, then STOP `E-SOURCE-MISSING`. Cite the path in the STOP message.

**AC-001.3** Given a path that exists but is not markdown/text (binary, empty 0-byte, or directory without an index file), then STOP `E-SOURCE-UNREADABLE`.

**AC-001.4** Given `@path/to/spec.md` or a bare existing `.md` path as the first positional, then intake proceeds to R-002.

### R-002 — Enumerable tasks required

Intake MUST extract an ordered task list from the source. A pitch with no tasks is not a source.

**AC-002.1** Given a file whose only content is a feature pitch (prose, no numbered items, no checklist, no `### T` headings, no `## Tasks` list), then STOP `E-NO-TASKS`. Message MUST include "spec that is only a pitch".

**AC-002.2** Given a file with a task heading/checklist but **zero** items after parse, then STOP `E-EMPTY`. Distinct from `E-NO-TASKS`.

**AC-002.3** Given mixed prose + N≥1 enumerable items, then N tasks are assigned ids `T1..TN` in source order. Parse MUST NOT invent tasks from prose paragraphs.

**AC-002.4** SuperClaude `phase-N-tasklist.md` files ARE accepted if they contain enumerable task headings. MDTM templates are NOT required. MDTM-only ceremony fields (persona gates, F1 checkboxes) are ignored, not executed.

### R-003 — Every task must have AC text before execute

**AC-003.1** Given task Ti with no acceptance-criteria block, no `Then`/`MUST`/`Done when` sentence, and no checkbox AC under the task, then STOP `E-NO-AC` **before** editing for Ti. Do not implement-then-guess.

**AC-003.2** Given Ti with ≥1 AC sentence, then execute may start. The AC ids used later are `Ti.ACk` in source order (k=1..m).

**AC-003.3** Given a 1-task spec that has AC, then the per-task reviewer still runs (no 1-task fast-path that skips R-007).

**AC-003.4** Given a 20-task spec that has AC on all tasks, then tasks run sequentially T1→T20 unless R-006 parallel applies. Hard cap for one invocation: 20 tasks. Task 21+ → STOP `E-TOO-MANY` with count cited. Operator splits the source.

### R-004 — Legacy grammar is a hard STOP

**AC-004.1** Given exactly `/sc:implement user profile component --type component`, then STOP `E-LEGACY`. No product writes. No flag mapping to a new mode. No "I'll just implement it".

**AC-004.2** Given any of `--type`, `--framework`, `--safe`, `--with-tests` present, then STOP `E-LEGACY` even if a path is also present. Unknown/legacy flags are not ignored.

**AC-004.3** Command examples in `implement.md` MUST NOT contain the old pitch invocations. A grep of `src/superclaude/commands/implement.md` for `--type component` returns 0. A grep for `user profile component` returns 0.

**AC-004.4** Frontmatter `argument-hint` MUST require a path and MUST NOT list `--type|--framework|--safe|--with-tests`.

**AC-004.5** `disable-model-invocation` equivalent: the command is user-invoked only. Protocol MUST state that conversational "please implement X" does not auto-activate `/sc:implement`. Fail if the Triggers section lists free-form feature requests as activation.

### R-005 — Sequential walk; resume after compaction

**AC-005.1** Given ledger with T1..Tk `complete` and Tk+1 absent, when the command is re-invoked on the same source, then execution starts at Tk+1. No re-implementation of complete tasks.

**AC-005.2** Given session compaction (context lost) and an on-disk ledger, then resume rule is **first task id whose latest status line is not `complete`**. Trust ledger + git log. Do not trust the implementer's chat recap.

**AC-005.3** Given no ledger file, then start at T1 and create the ledger before the first edit.

**AC-005.4** Given a ledger whose last line is truncated/unparseable, then STOP `E-LEDGER-CORRUPT`. Do not guess. Operator may delete the bad line.

### R-006 — Parallel only when source says independent, and bounded

**AC-006.1** Default is sequential. Parallel MUST NOT be inferred from "these look independent".

**AC-006.2** Given consecutive tasks marked in-source as independent (explicit `independent` / `parallel-ok` tag on each), then at most 3 may run concurrently. Fourth waits.

**AC-006.3** After a parallel batch, each task still gets its own R-007 verdict and its own ledger line before the next batch.

### R-007 — Per-task spec-compliance verdict (primary gate)

After implementer claims Ti done, a reviewer compares **the diff for Ti** against **Ti's AC + the global spec constraints + Ti's instructions**. The implementer's report is not evidence.

**AC-007.1** Verdict MUST be exactly one of:

| Enum | Meaning |
|------|---------|
| `compliant` | Every AC for Ti is evidenced. No extra scope vs Ti brief + global constraints. No misunderstood AC. |
| `missing` | ≥1 AC or instruction for Ti is unimplemented. |
| `extra` | Diff contains work not asked by Ti brief + global constraints. |
| `misunderstood` | Work exists but implements a different meaning than the AC/spec text. |
| `cannot-verify` | Reviewer cannot cite evidence (no diff, AC is unobservable, files not in the diff). |

No other strings. Not `pass`/`fail`/`issues`. Not `spec compliant`.

**AC-007.2** Reviewer MUST cite, for each AC of Ti, either `path:line` in the produced diff **or** `Ti.ACk` plus `path:line` of the AC in the source. A verdict with zero citations is invalid → treat as `cannot-verify`.

**AC-007.3** `compliant` requires: all Ti ACs cited AND extra-scope empty AND misunderstood empty.

**AC-007.4** Do not re-run the full test suite as the review. Tests are extras (R-009).

**AC-007.5** Same verdict schema whether reviewer is inline or subagent. Tests assert the ledger line, not the executor identity.

### R-008 — Halt vs continue-with-ruling vs cannot-verify

Decision table (mandatory):

| Verdict | Default action | May proceed to T{i+1}? |
|---------|----------------|------------------------|
| `compliant` | Append complete line | Yes |
| `missing` | HALT. Fix or ruling. | No, unless ruling line written |
| `extra` | HALT. Revert extra or ruling. | No, unless ruling line written |
| `misunderstood` | HALT. Fix or ruling. | No, unless ruling line written |
| `cannot-verify` | HALT. Produce evidence or ruling. | No, unless ruling line written |

**AC-008.1** HALT means: no T{i+1} edits, no `complete` status, STOP message names verdict + Ti + missing citations.

**AC-008.2** Continue-with-ruling requires a **second ledger line** matching R-010 ruling schema: `what — why — cost-if-wrong`. Missing any of the three fields → ruling is invalid → stay HALT.

**AC-008.3** A ruling does not change the verdict enum. The status becomes `complete` only after the ruling line exists. Ledger then has: verdict line (`missing`/`extra`/`misunderstood`/`cannot-verify`) then ruling line then the complete line may be written.

**AC-008.4** Operator-supplied `--force` without a ruling line is invalid. STOP `E-NO-RULING`. Silent skip of QA is forbidden.

**AC-008.5** `cannot-verify` is not a pass. Common causes and required next action:

| Cause | Next action |
|-------|-------------|
| Empty diff | Implement or mark task skipped via ruling (cost-if-wrong required) |
| AC not observable from diff (UX copy, runtime only) | Add a check/log/test that makes it observable, or ruling |
| Files claimed edited are not in the diff | Re-run reviewer on actual diff |
| Compaction lost the diff | `git diff` from task start SHA (recorded on start line) |

### R-009 — Lint / typecheck / tests are extras

**AC-009.1** When a detector finds a repo command (`ruff`/`eslint`, `tsc`/`mypy`, `npm test`/`pytest`/`uv run pytest`), run it after Ti. Record on the extras field. When absent, record `skip`.

**AC-009.2** Extra `fail` does **not** by itself change the spec verdict to `missing`/`misunderstood`.

**AC-009.3** Given `npm test`/`pytest` red, and the failing test files are **not** in Ti's touched-file set and were red before Ti (or fail without Ti files in the traceback), then extras=`tests:unrelated-red`. Verdict stays spec-based. Do not HALT for spec.

**AC-009.4** Given extras fail **and** the failing file is in Ti's touched-file set, then extras=`tests:fail` (or lint/typecheck fail). Still not the spec verdict. Optional: operator may treat as HALT only if Ti's own AC required that test to pass — that is an AC, not an extra.

**AC-009.5** A task MUST NOT be marked `compliant` because extras are green when R-007 citations are missing.

### R-010 — Ledger is one markdown file, one parseable line family

See §8 for exact schema. Requirements:

**AC-010.1** Ledger path is `.dev/implement/<slug>/progress.md` where `<slug>` is the source basename without extension, lowercased, non-alnum → `-`, max 60 chars. Not next to the spec. Not under `.claude/`.

**AC-010.2** File starts with exactly one header line (schema §8). Then 0..N record lines.

**AC-010.3** Re-invoke on same source reuses the same ledger path. Do not create a second file.

**AC-010.4** After each task's terminal state, the file is flushed (Write) before starting the next task. Compaction-safe.

### R-011 — Optional whole-list review at end, not per-task ensemble

**AC-011.1** After T_last `complete`, one optional whole-list review MAY run. Default: run it. `--skip-final-review` skips it.

**AC-011.2** Whole-list review MUST NOT spawn a 6-agent panel, `/task` QA, or `/sc:reflect` as a required gate. One reviewer pass vs the full spec + full ledger.

**AC-011.3** Final review findings append `FINAL:` lines. They do not rewrite per-task verdicts.

### R-012 — No silent routing to `/task` or `/sc:task`

**AC-012.1** Protocol MUST NOT invoke `/task`, `/sc:task`, or `sc:task-protocol` as the executor.

**AC-012.2** If the source is an MDTM task file, still execute via this protocol or STOP `E-WRONG-TOOL` recommending `/task` — do not auto-handoff.

### R-013 — Thin command + protocol skill

**AC-013.1** `src/superclaude/commands/implement.md` contains `## Activation` with the exact line `> Skill sc:implement-protocol`.

**AC-013.2** Directory `src/superclaude/skills/sc-implement-protocol/` exists with `SKILL.md`. `make lint-architecture` Check 1 prints `implement → sc-implement-protocol`.

**AC-013.3** Command file ≤150 lines. Skill `SKILL.md` ≤500 lines. Extra detail in `refs/` loaded on demand (`refs/qa.md`, `refs/ledger.md`, `refs/intake.md`).

**AC-013.4** Edit `src/` then `make sync-dev`. `.claude/` mirrors are not SoT. `make verify-sync` exits 0.

**AC-013.5** Command `allowed-tools` includes `Skill`.

### R-014 — Start SHA recorded per task

**AC-014.1** Before first edit of Ti, ledger gets a `start` line with `git rev-parse HEAD` (or `nogit` if not a repo). Reviewer diff is `start_sha..HEAD` plus unstaged, scoped to Ti files when possible.

**AC-014.2** If `nogit` and no file mtimes snapshot, verdict defaults to `cannot-verify` unless the reviewer can still list written paths from the tool trace. Cost of no-git is explicit.

## 3. NFRs

| ID | Requirement | Test |
|----|-------------|------|
| NFR-1 | Protocol is middleweight: no 6-agent QA, no MDTM, no reflect ensemble | Grep skill tree for `sc:task-protocol`, `phase-gate`, `/sc:reflect`, `MDTM` as invoked tools — 0 invocation hits (mentions in "do not" lists allowed) |
| NFR-2 | Deterministic STOP codes | STOP message contains one of the `E-*` codes in §11 |
| NFR-3 | Compaction resume ≤1 ledger Read + 1 git log | Documented in protocol; eval case E-RESUME |
| NFR-4 | SKILL.md load budget | `wc -l` SKILL.md ≤500 |
| NFR-5 | No new Python runtime dependency | `make verify-deps` unchanged |
| NFR-6 | Explicit invocation only | Triggers section does not list "feature development requests" as auto-activate |
| NFR-7 | Output not under `.claude/skills\|commands\|agents` | Ledger path prefix `.dev/implement/` |
| NFR-8 | 20-task run stays sequential by default | No Task-tool fanout unless independent tags present |

## 4. Architecture sketch (testability only)

```
/sc:implement @source.md [--skip-final-review] [--ledger <path>]
        │
        ▼
implement.md          # flags, STOP codes, examples, ## Activation
        │ Skill sc:implement-protocol
        ▼
SKILL.md              # intake → loop → extras → final
  refs/intake.md      # parse tasks + AC, E-NO-TASKS / E-EMPTY / E-NO-AC
  refs/qa.md          # verdict enum, evidence rules, halt table
  refs/ledger.md      # exact line regex
        │
        ▼
.dev/implement/<slug>/progress.md
```

**Test seams (no extra abstractions):**

1. Intake function-in-prose: given fixture markdown → expected task ids + AC ids or STOP code. A tiny Python self-check may regex-parse fixtures; it MUST NOT import sprint/task QA modules.
2. Ledger regex: every written line matches §8.
3. Halt table: given a verdict, next tool call is not Edit/Write on T{i+1} files.

Reviewer implementation: **inline when N≤3 and context is not compacted; otherwise one fresh subagent with the task brief + diff + global constraints**. Same output schema. Do not test "was it a subagent".

## 5. Input contract

```
/sc:implement <source> [--skip-final-review] [--ledger <path>]
```

| Token | Required | Rule |
|-------|----------|------|
| `<source>` | yes | Existing file path or `@path`. Markdown/text. |
| `--skip-final-review` | no | Skip R-011 |
| `--ledger` | no | Override path; still MUST live under `.dev/implement/` or STOP `E-LEDGER-PATH` |

**Rejected (STOP `E-LEGACY`):** `--type`, `--framework`, `--safe`, `--with-tests`, free-form description with no path.

**Rejected (STOP `E-NO-SOURCE`):** empty argv; conversational pitch.

**Accepted source shapes (intake):**

| Shape | How tasks are found |
|-------|---------------------|
| Numbered list `1. ...` | Each top-level number is a task |
| Checklist `- [ ] ...` | Each item is a task |
| Headings `### T1` / `### T<PP>.<TT>` | Each heading is a task |
| `## Tasks` section of a PRD/spec | List items under it |

AC extraction per task, first match wins:

1. Subsection `Acceptance Criteria` / `AC:`
2. Gherkin `Then` lines
3. Sentences starting `MUST` / `Done when`
4. Nested checkboxes under the task

If none: `E-NO-AC`.

Global constraints: any `## Constraints` / `## Out of scope` / `## Non-goals` in the source. Reviewer uses them for `extra`.

## 6. Per-task QA protocol (testable)

Order is fixed. Skipping a step is a protocol fail.

```
Q0 START  Write start line. Record start_sha. Read Ti text + AC ids + global constraints.
Q1 EXEC   Implementer edits. Touched files = union of Write/Edit paths for this task.
Q2 DIFF   Collect git diff start_sha..WORKTREE (or tool-trace paths if nogit).
Q3 REVIEW Reviewer (not the implementer voice) fills:
            - For each Ti.ACk: status in {met, unmet, n/a-global} + citation
            - extra_scope: list of diff hunks not mapped to any AC / instruction
            - misunderstood: list of ACs whose implementation contradicts the AC text
Q4 VERDICT  Apply:
            if diff empty and no ruling → cannot-verify
            elif any unmet → missing
            elif any misunderstood → misunderstood
            elif extra_scope nonempty → extra
            elif any AC lacks citation → cannot-verify
            else → compliant
Q5 EXTRAS   Detect and run lint/typecheck/tests if present. Record extras. Never overwrite Q4.
Q6 GATE     Apply R-008 table. Write ledger line(s). Flush.
Q7 NEXT     Only if complete (compliant or ruled). Else STOP.
```

**Q3 isolation checks (fail the rewrite if violated):**

- Reviewer prompt/instructions include: "Do not trust the implementer's report."
- Reviewer input includes the task brief and the diff, not "the tests passed".
- Reviewer does not call `/sc:reflect` or a 6-agent panel.

**1-task spec:** Q0–Q7 still run, then optional FINAL review.

**20-task spec:** Q0–Q7 × 20. No batching of reviews. After each Q6 flush.

**Missing AC:** never reach Q1; STOP at intake.

**Lint fail vs spec fail:** Q5 fail ≠ Q4 `missing`. Ledger shows both fields.

**Tests red, unrelated files:** extras=`tests:unrelated-red`; Q4 unchanged; Q6 does not HALT for extras.

## 7. (continued) Reviewer citation rules

Valid evidence tokens (must appear in the verdict line `evidence=` field):

| Token | Form | Example |
|-------|------|---------|
| File line | `rel/path:line` | `src/foo.py:42` |
| Range | `rel/path:start-end` | `src/foo.py:42-58` |
| AC id | `T{i}.AC{k}` | `T3.AC1` |
| Pair | `T{i}.AC{k}@rel/path:line` | `T3.AC1@src/foo.py:42` |

**Invalid:** `the component works`, `tests pass`, `as implemented above`, line-less paths, citations into files not in Q1 touched set unless the AC required reading them (then cite source spec `path:line` instead).

**cannot-verify if:** reviewer would need a running UI and no check was added.

## 8. Ledger format (exact)

File: `.dev/implement/<slug>/progress.md`

Encoding: UTF-8, `\n` endings, no wrapping of record lines.

### Header (line 1 only)

```
# implement ledger — source: <source-path> — created: <ISO-8601>
```

`<source-path>` is the resolved path as invoked. `<ISO-8601>` is `YYYY-MM-DDTHH:MM:SSZ`.

### Start line (once per task, before edits)

```
T<id>: start sha=<40-hex|nogit>
```

Regex:

```
^T([0-9]+): start sha=([0-9a-f]{40}|nogit)$
```

### Verdict line (once per completed review)

```
T<id>: <status> verdict=<verdict> ac=<ac-list> evidence=<ev-list> extras=lint:<lx>,typecheck:<tx>,tests:<sx> files=<file-list>
```

- `<status>` ∈ `complete` | `blocked`
- `<verdict>` ∈ `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`
- `<ac-list>` = comma-separated `T{i}.AC{k}` (no spaces)
- `<ev-list>` = comma-separated evidence tokens from §7 (no spaces)
- `<lx>`,`<tx>` ∈ `ok` | `fail` | `skip`
- `<sx>` ∈ `ok` | `fail` | `skip` | `unrelated-red`
- `<file-list>` = comma-separated repo-relative paths (no spaces)

Regex:

```
^T([0-9]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=([^ ]+) extras=lint:(ok|fail|skip),typecheck:(ok|fail|skip),tests:(ok|fail|skip|unrelated-red) files=([^ ]+)$
```

`complete` is allowed on the verdict line **only if** `verdict=compliant`. Otherwise status MUST be `blocked` until a ruling + a follow-up complete line.

### Ruling line

```
T<id>: Ruling: <what> — <why> — cost-if-wrong: <cost>
```

Em dashes as shown (` — `). Three fields required.

Regex:

```
^T([0-9]+): Ruling: .+ — .+ — cost-if-wrong: .+$
```

### Post-ruling complete line

After a valid ruling, write:

```
T<id>: complete verdict=<unchanged-non-compliant-verdict> ac=... evidence=... extras=... files=...
```

Here `complete` + non-compliant verdict is legal **only** when a matching `T<id>: Ruling:` line exists above it.

### Final review line (optional)

```
FINAL: <pass|issues> evidence=<ev-list>
```

### Resume algorithm (normative)

```
parse lines in order
for each id in T1..TN:
  if no line for id → resume here
  if latest status for id is blocked and no subsequent complete → resume here (re-review or fix)
  if latest status is complete → skip
first such id wins
if all complete → run FINAL unless --skip-final-review or FINAL already present
```

`complete` in a line is the substring after `T<id>: ` beginning with `complete`.

## 9. Out of scope

- `/task` F1 loop, 6-agent phase-gate QA, MDTM templates, reflect pre/post as the per-task gate
- TDD-watched-fail / `Expected:` test-runner as the completion contract
- Inventing a spec from a pitch
- Mapping legacy `--type/--framework/--safe/--with-tests` to new behavior
- Auto-routing into `/sc:task` or `/task`
- Per-task code-quality ensemble (SDD Part 2) — optional FINAL only
- Committing, PR, `/sc:test`, `/sc:git` as required next steps
- New CLI Python package or pytest plugin
- Full eval harness / grader.py / evals.json suite as a rewrite deliverable (see §12 tiny self-check instead)
- Writing product features inside this brainstorm

## 10. Open-question positions (testability first)

| # | Question | Position | Why testable |
|---|----------|----------|--------------|
| Q1 | Tasklist format | Any markdown with enumerable tasks + AC. Phase-N headings accepted. MDTM not required. | Fixture files: checklist, numbered, phase-N, pitch. Assert parse or STOP code. |
| Q2 | Inline vs subagent reviewer | Same schema always. Inline if N≤3 and not compacted; else one subagent. | Tests assert ledger lines, not process shape. |
| Q3 | Ledger location | `.dev/implement/<slug>/progress.md` | Path prefix grep. No writes beside spec. |
| Q4 | 1-task reviewer | Always run Q0–Q7 | One fixture, assert verdict line exists. |
| Q5 | Relation to `/task` | No silent routing. `E-WRONG-TOOL` only if operator points at an MDTM file and we refuse ceremony — actually: execute as markdown tasks if AC exist; do not invoke `/task`. | Grep for `/task` invocation. |
| Q6 | Cap | 20 tasks per invocation | Fixture with 21 headings → `E-TOO-MANY`. |
| Q7 | Independent parallel | Explicit tag only, max 3 | Untagged 20-task stays sequential. |
| Q8 | `--force` | Forbidden without ruling | `E-NO-RULING`. |

## 11. Failure-mode catalog

| Code | Trigger | Product writes? | Ledger? |
|------|---------|-----------------|---------|
| `E-NO-SOURCE` | No path | No | No |
| `E-SOURCE-MISSING` | Path not found | No | No |
| `E-SOURCE-UNREADABLE` | Unreadable/non-text | No | No |
| `E-NO-TASKS` | Pitch, no enumerable tasks | No | No |
| `E-EMPTY` | Task section exists, 0 items | No | No |
| `E-NO-AC` | Ti has no AC | No writes for Ti | Start line optional; no complete |
| `E-TOO-MANY` | ≥21 tasks | No | No |
| `E-LEGACY` | Pitch and/or `--type/--framework/--safe/--with-tests` | No | No |
| `E-LEDGER-PATH` | `--ledger` outside `.dev/implement/` | No | No |
| `E-LEDGER-CORRUPT` | Unparseable last record | No further | Unchanged |
| `E-NO-RULING` | Attempt to continue after non-compliant without ruling | No T{i+1} | blocked line only |
| `E-HALT-QA` | `missing`/`extra`/`misunderstood`/`cannot-verify` and no ruling | No T{i+1} | blocked line |
| `E-WRONG-TOOL` | Reserved; not used for auto-handoff (R-012) | — | — |

**Named edge cases → expected code:**

| Case | Expected |
|------|----------|
| Missing AC on T2 of 5 | T1 may complete; STOP `E-NO-AC` before T2 edits |
| 1-task spec with AC | One Q0–Q7 cycle + FINAL |
| 20-task spec | 20 sequential cycles; task 21 absent |
| 21-task spec | `E-TOO-MANY` at intake, nothing runs |
| Compaction mid-run after T3 complete | Resume T4 via ledger |
| Compaction with truncated last line | `E-LEDGER-CORRUPT` |
| Lint fail, spec citations complete | `verdict=compliant` `extras=lint:fail` `status=complete` |
| Spec missing, lint green | `verdict=missing` `extras=lint:ok` `status=blocked` |
| Tests red, traceback in other package, Ti files clean | `tests:unrelated-red`, spec verdict unchanged |
| Tests red in Ti file | `tests:fail`, spec verdict unchanged unless AC required that test |
| Empty tasklist file (`## Tasks` then EOF) | `E-EMPTY` |
| Pitch-only spec | `E-NO-TASKS` |
| `/sc:implement user profile component --type component` | `E-LEGACY` |
| `@spec.md --type api` | `E-LEGACY` |
| Empty diff after "done" | `cannot-verify` → `E-HALT-QA` |
| Extra file in diff vs Ti brief | `verdict=extra` → HALT |
| Implemented opposite of AC | `verdict=misunderstood` → HALT |
| Ruling missing `cost-if-wrong` | ruling invalid, stay `blocked` |

## 12. Success criteria / eval cases for the rewrite

The rewrite is done when **all** of the following pass. This is the verification of the rewrite itself — not `/task` QA, not a full skill-eval workspace unless someone later adds one.

### 12.1 Static self-check (must ship with the rewrite)

A single file `src/superclaude/skills/sc-implement-protocol/scripts/selfcheck.py` (or `tests/commands/test_implement_contract.py`) that uses **stdlib + pytest already in the repo**. No grader.py, no evals.json, no reflect fixtures.

Checks:

| Check | Assertion |
|-------|-----------|
| S1 | `## Activation` and `> Skill sc:implement-protocol` in `commands/implement.md` |
| S2 | `src/superclaude/skills/sc-implement-protocol/SKILL.md` exists |
| S3 | `wc -l` command ≤150, SKILL.md ≤500 |
| S4 | `argument-hint` contains a path token; does not contain `--type` |
| S5 | Grep command file: 0 hits for `user profile component`, `--type component`, `--with-tests`, `--framework` |
| S6 | Triggers do not list free-form "Feature development requests" as activation |
| S7 | Skill contains the five verdict strings and the halt table |
| S8 | Skill ledger regex matches §8 (the regex is copied into the test, fixtures round-trip) |
| S9 | Grep skill: no invocation of `/task`, `sc:task-protocol`, `/sc:reflect` as a step (allow "do not") |
| S10 | `make lint-architecture` Check 1 includes `implement → sc-implement-protocol` |
| S11 | `make verify-sync` exit 0 after `make sync-dev` |

### 12.2 Ledger regex fixtures (must ship)

`src/superclaude/skills/sc-implement-protocol/refs/ledger.md` includes 4 example lines (start, compliant complete, blocked missing, ruling). Self-check parses them with the §8 regex: all match. One negative example (`Task 1: done`) MUST fail the regex.

### 12.3 Eval cases (prompt-level; run later as skill evals if desired — not a rewrite blocker except where marked MUST)

| ID | Kind | Input | Expect | MUST now? |
|----|------|-------|--------|-----------|
| E-LEGACY-1 | regression | `/sc:implement user profile component --type component` | STOP `E-LEGACY`; no Write to product paths | MUST — assert via command text + protocol "legacy → E-LEGACY" |
| E-PITCH | intake | fixture `pitch-only.md` | `E-NO-TASKS` | MUST — fixture + intake rules in refs |
| E-EMPTY | intake | fixture `empty-tasks.md` | `E-EMPTY` | MUST — fixture in `refs/fixtures/` |
| E-NO-AC | intake | fixture `task-without-ac.md` | `E-NO-AC` | MUST |
| E-ONE | happy | fixture `one-task.md` | start + verdict line; reviewer not skipped | MUST — stated in SKILL |
| E-TWENTY | scale | fixture `twenty-tasks.md` | sequential T1..T20; no parallel | stated |
| E-TWENTYONE | cap | 21 headings | `E-TOO-MANY` | MUST — fixture |
| E-RESUME | compaction | ledger with T1 complete, T2 absent | resume T2 | stated + resume algo |
| E-LINT-NOT-GATE | extras | compliant citations + lint fail | `verdict=compliant extras=lint:fail` | stated |
| E-UNRELATED-RED | extras | red tests outside Ti files | `tests:unrelated-red`; not HALT | stated |
| E-MISSING-HALT | gate | unmet AC | `blocked verdict=missing`; no T{i+1} | stated |
| E-RULING | gate | missing + valid ruling | complete after ruling line | stated |
| E-BAD-RULING | gate | ruling without cost-if-wrong | stay blocked | stated |
| E-CANNOT-VERIFY | gate | empty diff | `cannot-verify` HALT | stated |
| E-NO-SILENT-TASK | boundary | protocol steps | no `/task` call | S9 |

Fixtures live in `src/superclaude/skills/sc-implement-protocol/refs/fixtures/` (tiny markdown files). They are for the static self-check and future evals. They are not an eval-workspace under `.dev/eval-workspaces/` unless a later change requests `make eval-skill SKILL=sc-implement-protocol`.

### 12.4 Rewrite acceptance (human)

- `/sc:implement` without a path STOPs with usage.
- Legacy example in current `implement.md` is gone and would STOP.
- One real run against a 2-task fixture produces a parseable ledger with two verdicts.
- `make lint-architecture` and `make verify-sync` pass.

## Traceability

| Goal | Requirements |
|------|----------------|
| G-1 | R-001, R-002, R-003, R-004 |
| G-2 | R-007, R-008, R-014 |
| G-3 | R-009 |
| G-4 | R-010, R-011, R-012, NFR-1 |
| G-5 | R-013 |
| G-6 | R-004, E-LEGACY-1 |

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-24T19:37:41.989Z","contentHash":"d9a5ef5a","sections":[{"heading":null,"hash":"38593774"},{"heading":"Variant 3 — `/sc:implement` rewrite spec (QA / haiku)","hash":"622480d9"},{"heading":"1. Problem / goals","hash":"19412f08"},{"heading":"Problem","hash":"bcf52e8d"},{"heading":"Goals (falsifiable)","hash":"ff753ec2"},{"heading":"2. Functional requirements","hash":"e402e790"},{"heading":"R-001 — Required source path","hash":"21b63683"},{"heading":"R-002 — Enumerable tasks required","hash":"2e44c86b"},{"heading":"R-003 — Every task must have AC text before execute","hash":"c8bb148d"},{"heading":"R-004 — Legacy grammar is a hard STOP","hash":"874ea420"},{"heading":"R-005 — Sequential walk; resume after compaction","hash":"f10189d6"},{"heading":"R-006 — Parallel only when source says independent, and bounded","hash":"4af7fe88"},{"heading":"R-007 — Per-task spec-compliance verdict (primary gate)","hash":"9b9106da"},{"heading":"R-008 — Halt vs continue-with-ruling vs cannot-verify","hash":"4668d950"},{"heading":"R-009 — Lint / typecheck / tests are extras","hash":"817d6f6e"},{"heading":"R-010 — Ledger is one markdown file, one parseable line family","hash":"7aea78ff"},{"heading":"R-011 — Optional whole-list review at end, not per-task ensemble","hash":"97597727"},{"heading":"R-012 — No silent routing to `/task` or `/sc:task`","hash":"84b6ec83"},{"heading":"R-013 — Thin command + protocol skill","hash":"d9443eb5"},{"heading":"R-014 — Start SHA recorded per task","hash":"ea46d0fd"},{"heading":"3. NFRs","hash":"325b5bae"},{"heading":"4. Architecture sketch (testability only)","hash":"df0479ba"},{"heading":"5. Input contract","hash":"571df34a"},{"heading":"6. Per-task QA protocol (testable)","hash":"ac321ed7"},{"heading":"7. (continued) Reviewer citation rules","hash":"c57cddf8"},{"heading":"8. Ledger format (exact)","hash":"ef83bfb2"},{"heading":"Header (line 1 only)","hash":"bb891e87"},{"heading":"implement ledger — source: <source-path> — created: <ISO-8601>","hash":"172e5417"},{"heading":"Start line (once per task, before edits)","hash":"9c953c3f"},{"heading":"Verdict line (once per completed review)","hash":"a9120501"},{"heading":"Ruling line","hash":"fe66cd3d"},{"heading":"Post-ruling complete line","hash":"ebe39397"},{"heading":"Final review line (optional)","hash":"83b9ac58"},{"heading":"Resume algorithm (normative)","hash":"39699989"},{"heading":"9. Out of scope","hash":"060da1f6"},{"heading":"10. Open-question positions (testability first)","hash":"e98c0cf4"},{"heading":"11. Failure-mode catalog","hash":"5c4a4353"},{"heading":"12. Success criteria / eval cases for the rewrite","hash":"610c3b46"},{"heading":"12.1 Static self-check (must ship with the rewrite)","hash":"53153995"},{"heading":"12.2 Ledger regex fixtures (must ship)","hash":"b8bcc997"},{"heading":"12.3 Eval cases (prompt-level; run later as skill evals if desired — not a rewrite blocker except where marked MUST)","hash":"1040b9f6"},{"heading":"12.4 Rewrite acceptance (human)","hash":"60a2791a"},{"heading":"Traceability","hash":"3059e209"}]}-->
<!--mc:threads:end-->
