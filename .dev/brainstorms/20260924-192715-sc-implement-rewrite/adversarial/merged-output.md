---
status: merged
base: variant-2-sonnet-refactorer
convergence: 0.80
date: 2026-09-24
topic: sc-implement-rewrite
soT_command: src/superclaude/commands/implement.md
soT_skill: src/superclaude/skills/sc-implement-protocol/SKILL.md
---

# Merged requirements — rewrite `/sc:implement`

This is a requirements specification. It is not the rewrite. After this file, `/sc:improve` (or equivalent) implements against it.

Binding sources: seed brief `seed-brief.md`; variant 2 (base); variant 1 (one-fix-then-HALT, start-SHA, extras-after already in V2, warn at N≥20); variant 3 (halt table, citation obligation, E-NO-AC with verb+object QUALIFY, slim E-* codes, ledger regex). V2 delete-table copied verbatim.

<!-- provenance: section=header; base=variant-2-sonnet-refactorer; steal=variant-1-opus-architect,variant-3-haiku-qa; decision=binding-merge -->

## 1. Problem / goals

<!-- provenance: section=1-problem-goals; base=variant-2-sonnet-refactorer; steal=variant-1-opus-architect §1 -->

### Problem

`src/superclaude/commands/implement.md` is a persona/MCP behavioral mode. Invocation is a free-form feature pitch plus `--type` / `--framework`. Done means "compiles, basic functionality, ready for `/sc:test`". That is the wrong job.

The file has no `## Activation` and no skill. It is the product. Modern `/sc:*` commands (reflect, brainstorm, auggie-review) are thin dispatchers that MUST invoke `Skill sc:<name>-protocol`.

### Goals

1. `/sc:implement` becomes a **middleweight executor**: given a spec, PRD, or tasklist (never a pitch), walk the tasks, and after each task verify **that task** against its AC + spec + instructions.
2. Primary QA is Superpowers SDD Part 1 spec-compliance (Missing / Extra / Misunderstood). Lint / typecheck / tests are extras, never the verdict.
3. Ledger is one markdown file, parseable lines, resumable. Not `/task` F1, not 6-agent gates, not MDTM.
4. Hard cutover. No "legacy free-form still works". No `--type` / `--framework` / `--safe` / `--with-tests`.

### Non-goals (this rewrite)

Do not import `/task` phase-gate QA, MDTM templates, reflect pre/post, executing-plans TDD gates, Matt end-of-batch suite+review as the only gate, or feature-dev 7-phase. Do not add a Python CLI, a third intake ref, or a `--reviewer` / `--force` flag.

### Design principles (binding)

1. **Spec is authority.** Deviations are operator-authored ledger rulings, never silent, never executor-authored.
2. **One reviewer vs the brief**, not an ensemble.
3. **Thin command, fat skill.** Protocol lives in `sc-implement-protocol`. Command file must not be executable on its own.
4. **Intake lives in SKILL.md.** Rubrics that will be cited go in `refs/qa.md` and `refs/ledger.md` only.
5. **Grepable ledger.** Closed-enum verdicts. No JSON, no YAML state machine, no Python runner.
6. **Do not route into `/task` or `/sc:task`.** MDTM-shaped files still execute this protocol (ceremony ignored). Mention `/task` only in Will-Not.

## 2. Functional requirements

<!-- provenance: section=2-functional; base=variant-2-sonnet-refactorer §2; steal=variant-1 R-032/R-040 start-SHA one-fix; steal=variant-3 R-007/R-008/E-* -->

Each requirement is falsifiable: a static grep, a fixture invocation, or a protocol self-check can fail it. Reviewer evidence for the rewrite MUST cite `file:line` of the command/skill **or** an AC id below.

### R-001. Required source path

`/sc:implement` with no resolvable path to an existing spec, PRD, or tasklist file **STOP**s. It does not write product code and does not create a ledger.

- **AC-001.1** Given argv with no path, when invoked, then STOP `E-NO-SOURCE`, zero product writes, no ledger file created.
- **AC-001.2** Given a path that does not exist, or a directory, when invoked, then STOP `E-SOURCE-MISSING` citing the path attempted. The protocol MUST NOT invent a spec from leftover argument text.
- **AC-001.3** Given two source paths (positional plus `--spec`/`--prd`/`--tasklist`, or two of those flags), then STOP `E-NO-SOURCE` with message `pass one file`.
- **AC-001.4** Given a path under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`, then STOP `E-NO-SOURCE` (not an input; not an output).
- **AC-001.5** `--spec`, `--prd`, `--tasklist` are aliases for the same single file. Positional `<path>` is equivalent.

Falsify: invoke with `"user profile component"` and observe a write.

### R-002. Enumerable tasks required

A path that exists but contains no enumerable tasks (see §6) **STOP**s. The command does not invent a tasklist from prose.

- **AC-002.1** Given a pitch-only file (prose, no checklist, no numbered items, no `R-NNN`/`T-NNN`, no Task headings), then STOP `E-NO-TASKS`. Message MUST include `no enumerable tasks` and MUST state the file is a pitch. Zero product writes. No ledger.
- **AC-002.2** Given mixed prose + N≥1 enumerable items, then N tasks are assigned ids `T1..TN` in source order. Parse MUST NOT invent tasks from prose paragraphs.
- **AC-002.3** SuperClaude phase-N tasklist markdown IS accepted if it still has enumerable items. MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) are ignored except `independent` (R-003).
- **AC-002.4** A 1-task file is valid.

### R-003. Sequential by default; parallel only when marked, max 3

Tasks execute in source order. Parallel only when the source marks a set independent (literal `independent` on the item, `parallel-ok`, or a heading `Independent`) **and** the set size is ≤ 3. Unmarked = sequential.

- **AC-003.1** Two unmarked tasks MUST NOT run concurrently.
- **AC-003.2** Consecutive tasks each tagged `independent` may run at most 3 concurrently. The fourth waits.
- **AC-003.3** After a parallel batch, each task still gets its own spec-compliance verdict and its own ledger line before the next batch.
- **AC-003.4** If overlap is obvious from the task text (`same file`), stay sequential. Do not build a dep graph.

### R-004. Per-task spec-compliance verdict

After each task, before the next task starts, the protocol produces a spec-compliance verdict of exactly one of: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`. The verdict is against **that task's** AC + parent spec/PRD + task instructions.

- **AC-004.1** No other verdict strings. Not `pass`/`fail`/`issues`. Not `spec-compliant`.
- **AC-004.2** A task marked `complete` with no verdict field in the ledger fails this requirement.
- **AC-004.3** Order is fixed: implement → spec-compliance QA → extras. Skipping a step is a protocol fail.
- **AC-004.4** A 1-task spec still runs this QA. No 1-task fast-path that skips the reviewer.

### R-005. Reviewer evidence; do not trust the implementer

The reviewer does not treat the implementer's prose report as evidence. Evidence is the diff (or file reads) versus the brief.

- **AC-005.1** Reviewer instructions include the sentence: `Do not trust the implementer's report.`
- **AC-005.2** For each AC of Ti the reviewer MUST cite either `path:line` in the produced diff **or** `Ti.ACk` (optionally `Ti.ACk@path:line`).
- **AC-005.3** A verdict with zero citations is invalid and MUST be treated as `cannot-verify`.
- **AC-005.4** Invalid evidence: `the component works`, `tests pass`, `as implemented above`, line-less paths, citations into files not in this task's touched set unless the AC required reading them (then cite the source spec `path:line`).
- **AC-005.5** Falsify: ledger `complete` after "implemented X" with no file change.

### R-006. One fix then HALT; operator Ruling only

Verdict `missing`, `extra`, or `misunderstood` (and `cannot-verify` after the same loop) blocks the next task.

- **AC-006.1** On first non-compliant verdict: attempt **exactly one** fix pass, then re-QA. Do not start the next task.
- **AC-006.2** If the second QA is `compliant`, mark `complete` and continue.
- **AC-006.3** If the second QA is still not `compliant`: HALT `E-HALT-QA`. Do not loop. Do not start T{i+1}.
- **AC-006.4** `complete` on a non-compliant verdict is legal **only if** an operator-supplied ledger line exists: `T<id>: Ruling: <what> — <why> — <cost-if-wrong>`. All three fields required. Missing any field → ruling invalid → stay HALT.
- **AC-006.5** The executor MUST NOT author that Ruling line. If the operator attempts to continue without it, STOP `E-NO-RULING`.
- **AC-006.6** No `--force` flag. A `--force` token in `$ARGUMENTS` is `E-NO-RULING`.
- **AC-006.7** A ruling does not change the verdict enum. Ledger then has: non-compliant verdict line, then the operator Ruling line, then a `complete` line may be written.

### R-007. `cannot-verify` is not a pass

- **AC-007.1** Verdict `cannot-verify` is not `complete`. Next action is more evidence (read the files, show the diff, make the AC observable) via the one-fix pass, or an operator Ruling.
- **AC-007.2** Empty diff after "done" → `cannot-verify`.
- **AC-007.3** AC not observable from the diff (UX copy, runtime only) and no check/log/test added → `cannot-verify`.
- **AC-007.4** `nogit` and no written-path list from the tool trace → `cannot-verify`.

### R-008. Extras after verdict, never the gate

Lint, typecheck, and the project test command, when the repo has them, run **after** the spec-compliance verdict and are recorded on the same ledger line as extras. They never flip `compliant` → fail, and they never make a missing/extra/misunderstood task `complete`.

- **AC-008.1** Detect in repo root, run what exists, skip the rest. No extras flag.
- **AC-008.2** Record `lint=pass|fail|skip`, `typecheck=pass|fail|skip`, `test=pass|fail|skip|unrelated-red`.
- **AC-008.3** Extra `fail` does not change the spec verdict.
- **AC-008.4** A task MUST NOT be marked `compliant` because extras are green when R-005 citations are missing.
- **AC-008.5** Missing toolchain → `skip`. Do not install tools.

Detection (run what exists):

| Extra | Detect | Record |
|---|---|---|
| lint | `package.json` lint script, `ruff`, `eslint`, `make lint` | `lint=pass\|fail\|skip` |
| typecheck | `tsc --noEmit`, `mypy`, `pyright`, `package.json` typecheck | `typecheck=pass\|fail\|skip` |
| tests | `package.json` test script, `make test`, `uv run pytest` (this repo) | `test=pass\|fail\|unrelated-red\|skip` |

Prefer the cheapest detected command scoped to this task's files when the tool allows (`package.json` test in the nearest package, else repo root).

### R-009. Unrelated red is not a fail

A red test suite whose failing files are disjoint from the files this task touched is recorded `test=unrelated-red` and is **not** a fail and is **not** a spec HALT.

- **AC-009.1** `unrelated-red` when failing test files ∩ task-touched files = ∅.
- **AC-009.2** Red tests whose traceback includes this task's files → `test=fail`. Still not the spec verdict. If the AC required those tests to pass, spec-compliance captures it as `missing`.

### R-010. One markdown ledger

One markdown ledger file is created/appended per run. Format is the grammar in §8. No second schema. No YAML sidecar. No execution-log table.

- **AC-010.1** Default path: `.dev/implement/<slug>/progress.md`.
- **AC-010.2** `<slug>` = basename of the source path without extension, lowercased, non-`[a-z0-9_-]` → `-`, trimmed, max 64 chars.
- **AC-010.3** Create the directory if missing. Not next to the spec. Not `.claude/`. Not `docs/generated/`.
- **AC-010.4** `--ledger <path>` overrides. If the override is not under `.dev/implement/`, STOP `E-LEDGER-PATH`. Still one file.
- **AC-010.5** Re-invoke on the same source reuses the same ledger path. No second directory unless `--ledger`.
- **AC-010.6** After each task's terminal state, the file is flushed (Write) before starting the next task.
- **AC-010.7** The protocol MUST NOT `git add` the ledger.

### R-011. Resume from first non-complete

On `/sc:implement <same-path>` (or `--resume`), the protocol reads the ledger, finds the first task whose **latest** status is not `complete`, and starts there. Compacted sessions trust ledger + `git log`, not chat memory.

- **AC-011.1** If the ledger is missing, start at T1 and create the file with the header **before** the first edit.
- **AC-011.2** If all enumerable tasks have `complete`, STOP with `already complete: <ledger path>`. Do not re-implement unless the user passes a new path.
- **AC-011.3** Truncated or unparseable last line → STOP `E-LEDGER-CORRUPT`. Do not guess. Operator may delete the bad line.
- **AC-011.4** `--resume` is implicit when a matching ledger exists. No `--fresh` flag in this rewrite.

### R-012. Whole-list review

After the last task is `complete`, the protocol runs **one** whole-list spec-compliance pass against the parent spec when N>1. Default **ON** for N>1. Skip if N=1 (the per-task review is that pass). Operator may skip with `--skip-final-review`.

- **AC-012.1** N=1: do not run a second pass.
- **AC-012.2** N>1: one reviewer pass vs the full spec + full ledger. Default on.
- **AC-012.3** `--skip-final-review` skips the pass even for N>1.
- **AC-012.4** Not a 6-agent panel. Not `/sc:reflect`. Not `/task` phase-gate QA. Findings append a `FINAL:` line. They do not rewrite per-task verdicts.
- **AC-012.5** Whole-list review is advisory. It MUST NOT reopen completed tasks unless the operator says so.

### R-013. Activation

The command file contains `## Activation` that invokes `Skill sc:implement-protocol` before any protocol step.

- **AC-013.1** Body includes the exact invoke line `Skill sc:implement-protocol` (blockquote form `> Skill sc:implement-protocol` is required to match sibling commands).
- **AC-013.2** Command MUST state: do not execute protocol steps from the command file alone.
- **AC-013.3** Falsify: `make lint-architecture` Check 1 / Check 6.

### R-014. Protocol skill package

Skill directory `src/superclaude/skills/sc-implement-protocol/` exists with `SKILL.md` frontmatter `name:`, `description:`, `allowed-tools:`, and `name` ending in `-protocol`.

- **AC-014.1** Files that exist after rewrite:
  - `src/superclaude/commands/implement.md`
  - `src/superclaude/skills/sc-implement-protocol/SKILL.md`
  - `src/superclaude/skills/sc-implement-protocol/refs/qa.md`
  - `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`
- **AC-014.2** No `refs/intake.md`. Intake rules live in `SKILL.md`.
- **AC-014.3** No other new packages, Python modules, CLI subcommands, or agent files.
- **AC-014.4** Falsify: lint-architecture Checks 2, 8, 9.

Skill frontmatter MUST include:

```yaml
name: sc:implement-protocol
description: "Middleweight spec executor; require a spec/PRD/tasklist path; per-task spec-compliance QA; one-file ledger"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, Skill
```

### R-015. Hard cutover; legacy grammar STOP

Free-form pitch UX is gone. Command examples are path-based only. Flags `--type`, `--framework`, `--safe`, `--with-tests` do not appear in `implement.md` or the skill.

- **AC-015.1** Given `/sc:implement user profile component --type component`, STOP `E-LEGACY`. No product writes. No flag mapping.
- **AC-015.2** Given any of `--type`, `--framework`, `--safe`, `--with-tests` present, STOP `E-LEGACY` even if a path is also present.
- **AC-015.3** Grep of the two SoT files for `--type`, `--framework`, `--safe`, `--with-tests` returns 0 (except inside a "removed / E-LEGACY" sentence that names the banned tokens as banned).
- **AC-015.4** Grep of `implement.md` for `user profile component` returns 0.
- **AC-015.5** Frontmatter `argument-hint` requires a path and MUST NOT list those four flags.
- **AC-015.6** The command is explicit-invocation only. Triggers MUST NOT list "feature development requests" or free-form pitches as activation. Conversational "please implement X" does not auto-activate.

### R-016. Done is ledger-complete, not compile-ready

Completion is **not** "compiles / ready for `/sc:test`". Done = every enumerable task has a `complete` ledger line with verdict `compliant` (or a non-compliant verdict plus an operator Ruling).

- **AC-016.1** Remaining "ready for `/sc:test`" or "compiles" as completion criteria in SoT files fails this requirement.
- **AC-016.2** Suggest `/sc:test` and `/sc:git` as optional next steps only, not as gates.

### R-017. No `/task` routing; MDTM still uses this protocol

`/sc:implement` does not route into `/task` or `/sc:task`. If the source is an MDTM task file, implement still uses this protocol (enumerate + spec-compliance + tiny ledger). Ignore MDTM ceremony.

- **AC-017.1** Protocol MUST NOT invoke `/task`, `/sc:task`, or `sc:task-protocol` as the executor.
- **AC-017.2** Skill text MUST NOT say "hand off to `/task`".
- **AC-017.3** `/task` appears only in command Boundaries **Will Not**.

### R-018. Spec is binding

A deviation that ships must be an operator ledger `Ruling:` line: what, why, cost if wrong. Silent extras in the diff that the brief did not ask for are `extra` (R-004/R-006), not "nice to have".

### R-019. Source of truth is `src/superclaude/`

After edit, `make sync-dev`. `.claude/skills` and `.claude/commands` are not staged. Plugin copy `plugins/superclaude/commands/implement.md` follows the existing plugin sync; it is not a second SoT.

- **AC-019.1** `make verify-sync` passes after `make sync-dev`.
- **AC-019.2** No `.claude/skills` or `.claude/commands` staged.

### R-020. One rewrite, no dual grammar

Hard cutover in one rewrite. No dual grammar, no "legacy: feature-description still accepted", no mapping of `--type component` onto the new loop.

### R-021. AC required; verb+object title QUALIFY

Every task must have AC text before any edit for that task.

- **AC-021.1** AC extraction, first match:
  1. An `AC:` / `Acceptance:` / `Acceptance criteria` / `Done when` block on that item.
  2. Nested checkbox children of the item.
  3. Sentences containing `MUST` / `SHALL` / `must` / `Then` / `done when`.
  4. Else the item's own title **if** it contains a verb and an object (e.g. `Add login form`, `Fix resume parser`). That title **counts as AC**.
- **AC-021.2** Else STOP `E-NO-AC` **before** any edit for that task. Do not implement-then-guess. T{i-1} may already be complete; T{i+1} is not started.
- **AC-021.3** A single-word or vague title with no verb+object (`auth`, `make it better`) is **not** AC → `E-NO-AC`.
- **AC-021.4** AC ids used later are `Ti.ACk` in source order (k=1..m).

### R-022. Start-SHA before first edit

- **AC-022.1** Before the first edit of Ti, ledger gets a start line with `git rev-parse HEAD` (40-hex) or `nogit` if not a repo.
- **AC-022.2** Reviewer diff is `start_sha..WORKTREE` (HEAD plus unstaged), scoped to Ti files when possible.
- **AC-022.3** Header exists before the first start line.

### R-023. Reviewer mode (no flag)

- **AC-023.1** Inline, same session, when **all** are true: N≤3, source file ≤400 lines, session not compacted.
- **AC-023.2** Else one `Task` subagent. Prompt = SDD Part 1 only (diff vs brief; Missing/Extra/Misunderstood; verdict + citations). No Part 2 code-quality ensemble. No second subagent.
- **AC-023.3** Same verdict schema either way. No `--reviewer` flag. Tests assert the ledger line, not the executor identity.
- **AC-023.4** One mode for the whole run (recompute after compaction: if compacted mid-run, remaining QA uses the subagent).

### R-024. Slim STOP codes

STOP messages MUST contain exactly one of the codes in §5. No other `E-*` codes.

### R-025. Warn once at N≥20; no hard cap

- **AC-025.1** There is no 20-task hard cap. A 21-task source runs.
- **AC-025.2** When N≥20, print **once**: `N tasks; compaction likely; ledger is the source of resume.` Do not auto-split into multiple ledgers.

## 3. NFRs

<!-- provenance: section=3-nfrs; base=variant-2-sonnet-refactorer §3; override=two refs qa.md+ledger.md per binding decision 2 -->

| ID | Requirement |
|---|---|
| N-001 | Command file ≤ 150 lines (lint warns at 200, hard-fails at 500). Target the thin-dispatcher band used by `auggie-review.md`. |
| N-002 | `SKILL.md` ≤ 500 lines. Loop + STOP + intake live in SKILL.md. Exactly two `refs/` files: `qa.md` (Missing/Extra/Misunderstood + halt table + citation rules), `ledger.md` (exact grammar + regex). No `refs/intake.md`. No `cost-profile.yaml`, no templates dir, no Python package. |
| N-003 | No new runtime dependency. No new MCP server required. Optional Context7 only when a task implements against a third-party library API; not listed as the command's purpose. Optional auggie before significant edits; unavailability is a warning, not a STOP. |
| N-004 | No new CLI entry point (`superclaude implement` is out). Slash command + skill only. |
| N-005 | Personas are not the product. Command frontmatter `personas` is empty or omitted. No "activate frontend/backend/security" flow. |
| N-006 | Skill `allowed-tools` is the minimum: Read, Grep, Glob, Edit, Write, Bash, Task, Skill. Not TodoWrite-as-ledger (disk ledger is the ledger). |
| N-007 | Protocol is restart-safe after compaction: resume rule (R-011) does not require the previous session transcript. Resume ≤1 ledger Read + 1 git log. |
| N-008 | One reviewer vs the brief. Never 2+ reviewer agents per task. |
| N-009 | STOP messages contain one slim `E-*` code from §5. |
| N-010 | Explicit invocation only. Triggers section does not list "feature development requests" as auto-activate. |
| N-011 | Ledger path prefix `.dev/implement/`. Output not under `.claude/skills\|commands\|agents`. |
| N-012 | Trust-boundary refusals (criminal assistance, secret-committing, `.claude/` staging) still apply. Spec-compliance is not a license to violate them. |

## 4. Architecture

<!-- provenance: section=4-architecture; base=variant-2-sonnet-refactorer §4; override=refs/qa.md + refs/ledger.md; steal=variant-1 Activation copy; steal=variant-3 test seams -->

### What to build (four files)

```
src/superclaude/commands/implement.md          # rewrite in place; thin dispatcher
src/superclaude/skills/sc-implement-protocol/
  SKILL.md                                     # STOP, enumerate/intake, loop, extras, HALT
  refs/qa.md                                   # rubric, citations, halt table
  refs/ledger.md                               # exact line grammar + regex
```

Then `make sync-dev`.

Mirror: `src/superclaude/commands/auggie-review.md` (Required Input + STOP + Activation + short Options). Do not mirror `reflect.md` (legacy grammar, tiers, ensembles).

### Command file (dispatcher only)

Responsibilities:

1. Parse `$ARGUMENTS`: a filesystem path (positional, or `--spec|--prd|--tasklist` as aliases for the same thing — one path).
2. Optional `--resume`, optional `--ledger <path>` override, optional `--skip-final-review`.
3. STOP copy (usage) if path missing; `E-LEGACY` if banned flags present.
4. `## Activation` → `Skill sc:implement-protocol`.
5. Boundaries: will execute a spec/PRD/tasklist; will not invent a feature from a pitch; will not call `/task`.
6. Three path-based examples. Zero pitch examples.

Command frontmatter (target):

```yaml
name: implement
description: "Middleweight spec executor — walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger"
category: workflow
complexity: standard
personas: []
argument-hint: "<path-to-spec-or-prd-or-tasklist> [--resume] [--ledger <path>] [--skip-final-review]"
```

Empty `personas:` is intentional. Do not restore the five-persona cocktail. Do not list `mcp-servers` as identity. Optional auggie/context7 are protocol notes, not command identity.

Activation block (copy this):

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:implement-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill at
`src/superclaude/skills/sc-implement-protocol/SKILL.md`.
```

Command sections in order: YAML frontmatter; title + one-paragraph purpose; `## Triggers` (explicit only); `## Required Input` (STOP + usage); `## Usage` + `## Options` (closed flag table); `## Behavioral Flow` (parse → validate path → invoke skill → surface ledger path — MUST NOT contain the per-task loop, QA rubric, or ledger grammar); `## Activation`; `## Examples` (exactly three: STOP, 1-task `--spec`, tasklist resume); `## Boundaries` Will / Will Not; `## Related Commands`; `## Completion` — run is done when every enumerable task has a `complete` ledger line.

### Skill (the loop)

```
STOP if no path / not a file / not enumerable / legacy flags
  codes: E-NO-SOURCE | E-SOURCE-MISSING | E-NO-TASKS | E-LEGACY | E-LEDGER-PATH
open or create ledger (header first)
resume = first task whose latest status is not complete
  if last line truncated → E-LEDGER-CORRUPT
if N≥20: warn once
for each remaining task:
    if no AC (verb+object QUALIFY fails) → E-NO-AC before any edit for this task
    write start line with sha
    implement that task only
    spec-compliance review vs that task's AC + spec + instructions (citations required)
    if not compliant: exactly one fix pass + re-QA
    if still not compliant: HALT E-HALT-QA (operator Ruling is the only override)
    run extras if present; record; do not gate
    append one ledger line; flush
optional one whole-list pass if N>1 and not --skip-final-review
print ledger path
```

### Makefile / sync

| Check | Expectation after rewrite |
|---|---|
| lint-architecture Check 1 | `implement.md` has `## Activation` → dir `src/superclaude/skills/sc-implement-protocol/` |
| Check 2 | that skill dir has matching `commands/implement.md` |
| Check 3 | command ≤200 lines (warn); rewrite target ≤150 (N-001) |
| Check 4 | command ≤500 lines (error) |
| Check 6 | Activation heading present |
| Check 8 | SKILL.md has `name:`, `description:`, `allowed-tools:` |
| Check 9 | `name:` ends with `-protocol` |
| `make sync-dev` | mirrors into `.claude/` |
| `make verify-sync` | src and `.claude/` match |

Checks 5 and 7 are currently `NEEDS DESIGN` in the Makefile; this rewrite MUST NOT wait on them.

### What NOT to build

- Dual-mode / legacy free-form / `--type` compatibility shims
- `--reviewer`, `--force`, `--fresh`, `--no-extras`
- Python executor, pytest plugin, `selfcheck.py` package, or `superclaude implement` CLI
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
- Third intake ref (`refs/intake.md`)

### Delete from current `implement.md`

<!-- provenance: section=4-delete-table; base=variant-2-sonnet-refactorer §4 delete-table; copied=verbatim -->

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

## 5. Input contract + STOP table

<!-- provenance: section=5-input-stop; base=variant-2-sonnet-refactorer §5-6; steal=variant-3 §5/§11 slim E-* and E-NO-AC QUALIFY; override=MDTM executes this protocol -->

### Invocation

```
/sc:implement <path>
/sc:implement --spec <path>
/sc:implement --prd <path>
/sc:implement --tasklist <path>
/sc:implement <path> --resume
/sc:implement <path> --ledger <ledger-path>
/sc:implement <path> --skip-final-review
```

`--spec`, `--prd`, `--tasklist` are **aliases**. One file. No "spec plus tasklist required together". If two paths are passed, STOP `E-NO-SOURCE`: `pass one file`.

Closed flag set: `<path>` / `--spec` / `--prd` / `--tasklist`; `--resume`; `--ledger`; `--skip-final-review`. No other flags.

### STOP table (no work, print usage + code)

| Code | Trigger | Product writes? | Ledger? |
|---|---|---|---|
| `E-NO-SOURCE` | No path; two sources; path under `.claude/skills\|agents\|commands` | No | No |
| `E-SOURCE-MISSING` | Path not found, or path is a directory | No | No |
| `E-NO-TASKS` | Pitch-only file; zero enumerable tasks | No | No |
| `E-NO-AC` | Ti has no AC after verb+object QUALIFY | No writes for Ti | Header/prior tasks may exist; no start line for Ti |
| `E-LEGACY` | Pitch invocation and/or `--type/--framework/--safe/--with-tests` | No | No |
| `E-HALT-QA` | Non-compliant after one fix pass; no operator Ruling | No T{i+1} | Non-compliant verdict line written |
| `E-NO-RULING` | Attempt to `complete`/continue after non-compliant without operator Ruling; `--force` | No T{i+1} | Unchanged except existing blocked/verdict line |
| `E-LEDGER-CORRUPT` | Last ledger line truncated/unparseable | No further | Unchanged |
| `E-LEDGER-PATH` | `--ledger` not under `.dev/implement/` | No | No |

No other `E-*` codes. Do not add `E-TOO-MANY`, `E-EMPTY`, `E-SOURCE-UNREADABLE`, `E-WRONG-TOOL`. Fold: unreadable/empty/binary with no enumerable tasks → `E-NO-TASKS`; directory → `E-SOURCE-MISSING`.

### Not STOP

- Spec/PRD whose numbered requirements are the tasks (no separate tasklist file).
- SuperClaude phase-N tasklist markdown, if it still has enumerable items. Accepted as markdown, not as MDTM.
- MDTM-shaped files: execute this protocol; ignore ceremony; do not auto-handoff.
- A 1-task file.
- N≥20 (warn once; do not STOP).

### Usage text (exact shape)

```
Usage: /sc:implement <path-to-spec|prd|tasklist>
STOP: need a file of enumerable tasks with acceptance criteria.
Will not implement from a feature pitch.
```

Missing-path STOP also includes `E-NO-SOURCE`. Legacy STOP includes `E-LEGACY` and: `Removed flags: --type/--framework/--safe/--with-tests. Pass a spec path.`

### Enumerable tasks

A file is enumerable if **at least one** of these matches:

1. Markdown task items: `- [ ]` or `- [x]` or `* [ ]`.
2. Numbered items `1.` / `1)` under a heading, or `R-NNN` / `T-NNN` identifiers.
3. Headings `## Task N` / `### T1` / `## Phase N` with body text.

Extractors may mix in document order: every matching item becomes a task `T1..TN` in source order. If the source already labels `T001` / `Task 3` uniquely, keep that label; otherwise assign `T1..TN`. Ids MUST NOT change on resume.

Do not require MDTM fields. If present, ignore them except `independent` (R-003).

If the file is prose with zero lists, zero `R-NNN`, zero task headings: STOP `E-NO-TASKS` (R-002). Do not call `/sc:brainstorm` or `/sc:workflow` automatically.

### AC QUALIFY (normative)

See R-021. Verb+object title counts as AC. Else `E-NO-AC` before any edit for that task.

Global constraints the reviewer uses for `extra`: any `## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable` in the source.

## 6. Per-task loop + halt table

<!-- provenance: section=6-loop-halt; base=variant-2-sonnet-refactorer §7; steal=variant-1 one-fix-then-HALT + start-SHA; steal=variant-3 halt table + citations + Q0-Q7 order with extras after verdict -->

### Order (fixed)

```
Q0 START   Write start line. Record sha. Read Ti text + AC ids + global constraints.
           If AC QUALIFY fails → E-NO-AC (do not reach Q1).
Q1 EXEC    Implementer edits. Touched files = union of Write/Edit paths for this task.
Q2 DIFF    Collect git diff start_sha..WORKTREE (or tool-trace paths if nogit).
Q3 REVIEW  Reviewer (not the implementer voice) fills:
             - For each Ti.ACk: met | unmet + citation
             - extra_scope: diff hunks not mapped to any AC / instruction
             - misunderstood: ACs whose implementation contradicts the AC text
Q4 VERDICT Apply:
             if zero citations → cannot-verify
             if diff empty and no ruling → cannot-verify
             elif any unmet → missing
             elif any misunderstood → misunderstood
             elif extra_scope nonempty → extra
             else → compliant
Q5 FIX     If Q4 is not compliant: exactly one fix pass, re-run Q2–Q4 once.
Q6 EXTRAS  Detect and run lint/typecheck/tests if present. Record extras. Never overwrite Q4.
Q7 GATE    Apply halt table. Write ledger line(s). Flush.
Q8 NEXT    Only if complete (compliant, or non-compliant plus operator Ruling). Else STOP.
```

Do not re-run the full test suite as the review. Do not trust "I implemented X". Load `refs/qa.md` for Q3–Q5. Do not load reflect-protocol.

### Rubric (reviewer vs the brief)

Compare the **diff** (files this task changed) to:

- that task's AC
- the parent spec/PRD constraints that apply to this task
- explicit instructions on the task ("do not X", "file Y only")

| Label | Meaning |
|---|---|
| Missing | AC/instruction not in the diff |
| Extra | behavior/files/API the brief did not ask for |
| Misunderstood | work present but solves the wrong thing |
| (none) | spec compliant |

Verdict:

- `compliant` — no Missing/Extra/Misunderstood; every AC cited
- `missing` / `extra` / `misunderstood` — at least one of those labels
- `cannot-verify` — diff insufficient to judge, or zero citations (empty diff, generated binaries only, AC refers to runtime the reviewer cannot see)

If both missing and extra: verdict `missing` (unmet AC is the gate). Record extra findings on the same ledger line after the verdict. If misunderstood is present, it dominates extra.

### Halt table

| Verdict after Q4 (or after Q5 re-QA) | Action | May proceed to T{i+1}? |
|---|---|---|
| `compliant` (first QA) | Extras, append `complete` line | Yes |
| `missing` / `extra` / `misunderstood` / `cannot-verify` on first QA | Exactly one fix pass + re-QA | No |
| `compliant` after that one fix | Extras, append `complete` line | Yes |
| still non-compliant after one fix | HALT `E-HALT-QA`. Print ledger path, Ti, verdict, missing citations. Next operator action: fix in a later invocation, or supply a Ruling line. | No, unless operator Ruling line written |
| operator Ruling with all three fields | Append Ruling line; then `complete` with **unchanged** non-compliant verdict | Yes |
| `--force` or executor-authored Ruling | STOP `E-NO-RULING` | No |

HALT means: stop the loop, print ledger path, print the blocking task id + verdict + findings, print the exact next user action (`fix`, `ruling`, or `resume`). Do not start the next task.

### `cannot-verify` next actions (during the one fix pass)

| Cause | Next action |
|---|---|
| Empty diff | Implement, or operator marks skipped via Ruling |
| AC not observable from diff | Add a check/log/test that makes it observable, or operator Ruling |
| Files claimed edited are not in the diff | Re-run reviewer on actual diff |
| Compaction lost the diff | `git diff` from task start SHA |

### Reviewer isolation (fail the rewrite if violated)

- Reviewer prompt/instructions include: `Do not trust the implementer's report.`
- Reviewer input includes the task brief and the diff, not "the tests passed".
- Reviewer does not call `/sc:reflect` or a 6-agent panel.

### 1-task source

Still run Q0–Q8 once (inline). Skip the end-of-list second pass (R-012).

## 7. Ledger schema (exact)

<!-- provenance: section=7-ledger; base=variant-2-sonnet-refactorer §8; steal=variant-1 start-SHA; steal=variant-3 regex + header + ruling; override=extras pass/fail/skip/unrelated-red; override=Ruling shape from binding decision 7 -->

### Location

Default: `.dev/implement/<slug>/progress.md`

- `<slug>` = basename of the source path without extension, lowercased, non-`[a-z0-9_-]` → `-`, trimmed, max 64 chars.
- Create the directory if missing.
- `--ledger <path>` overrides. Still one file. Must live under `.dev/implement/` or `E-LEDGER-PATH`.

Not next to the spec. Not `.claude/`. Not `docs/generated/`. Encoding: UTF-8, `\n` endings, no wrapping of record lines.

### Header (line 1 only)

```
# implement ledger — source: <abs-or-repo-relative-path> — created: <ISO-8601>
```

`<ISO-8601>` is `YYYY-MM-DDTHH:MM:SSZ`. Header is required so resume can find the source path after compaction.

Regex:

```
^# implement ledger — source: \S+ — created: [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$
```

### Start line (once per task, before edits)

```
T<id>: start sha=<40-hex|nogit>
```

Regex:

```
^T([0-9A-Za-z.-]+): start sha=([0-9a-f]{40}|nogit)$
```

### Verdict line (once per completed review)

```
T<id>: <status> verdict=<verdict> ac=<ac-list> evidence=<ev-list> extras=lint:<lx>,typecheck:<tx>,test:<sx> files=<file-list>
```

- `<status>` ∈ `complete` | `blocked`
- `<verdict>` ∈ `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`
- `<ac-list>` = comma-separated `T{i}.AC{k}` (no spaces)
- `<ev-list>` = comma-separated evidence tokens (no spaces): `rel/path:line`, `rel/path:start-end`, `T{i}.AC{k}`, `T{i}.AC{k}@rel/path:line`
- `<lx>`,`<tx>` ∈ `pass` | `fail` | `skip`
- `<sx>` ∈ `pass` | `fail` | `skip` | `unrelated-red`
- `<file-list>` = comma-separated repo-relative paths (no spaces)

Regex:

```
^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=([^ ]+) extras=lint:(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|unrelated-red) files=([^ ]+)$
```

`complete` is allowed on the verdict line **only if** `verdict=compliant`. Otherwise status MUST be `blocked` until an operator Ruling + a follow-up complete line.

### Ruling line (operator-supplied only)

```
T<id>: Ruling: <what> — <why> — <cost-if-wrong>
```

Em dashes as shown (` — `). Three non-empty fields required (`what`, `why`, `cost-if-wrong`). Executor MUST NOT write this line.

Regex:

```
^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$
```

### Post-ruling complete line

After a valid operator Ruling, write:

```
T<id>: complete verdict=<unchanged-non-compliant-verdict> ac=... evidence=... extras=... files=...
```

Here `complete` + non-compliant verdict is legal **only** when a matching `T<id>: Ruling:` line exists above it.

### Final review line (optional)

```
FINAL: <pass|issues> evidence=<ev-list>
```

### Rules

- Append-only; do not rewrite earlier `complete` lines.
- One start line per task. One or more verdict lines (first QA, optional re-QA).
- No columns, no HTML, no JSON, no YAML frontmatter on the ledger.
- Negative example that MUST fail the verdict regex: `Task 1: done`

### Resume algorithm (normative)

```
if last line does not match header|start|verdict|ruling|FINAL regex → E-LEDGER-CORRUPT
parse lines in order
for each id in T1..TN (source order):
  if no line for id → resume here
  if latest status for id is not complete → resume here
  if latest status is complete → skip
first such id wins
if all complete → run FINAL unless --skip-final-review or FINAL already present or N=1
```

`complete` in a line is the substring after `T<id>: ` beginning with `complete`. Trust ledger + git history after compaction. Do not ask the user to paste prior chat.

`refs/ledger.md` MUST include 4 example lines (start, compliant complete, blocked missing, ruling) plus the negative `Task 1: done`.

## 8. Out of scope

<!-- provenance: section=8-oos; base=variant-2-sonnet-refactorer §9; steal=variant-1 §11 table items that do not contradict binding -->

- Implementing from a sentence with no file
- Generating the spec/PRD/tasklist (`/sc:brainstorm`, `/sc:workflow`, `/sc:tasklist`)
- `/task` MDTM execution, `/sc:task` compliance tiers
- `/sc:tdd` (builds an MDTM task and hands to `/task`)
- `/sc:test`, `/sc:git`, `/sc:reflect` as required steps
- Auto-commit, PR open, CI watch
- Dual-mode legacy; mapping `--type/--framework/--safe/--with-tests`
- `--reviewer`, `--force`, `--fresh`, `--no-extras`
- New MCP servers, Magic UI generation as the implementer
- Performance/security/accessibility review ensembles
- Python CLI, eval workspace, cost profile, `selfcheck.py` as a new package
- Per-task code-quality Part 2
- Silent routing to `/task` or `/sc:task`
- 20-task hard cap
- Third intake ref
- Changing other commands' text except a one-line pointer if they currently say `/sc:implement` is a free-form feature writer (docs follow-up; not a blocker for the two SoT files)

Related-commands (command file MUST state):

| Command | Relationship |
|---|---|
| `/task` | Heavy MDTM executor. Out of scope. No silent routing. Will-Not only. |
| `/sc:task` | Compliance-tiered execution. Out of scope. No silent routing. |
| `/sc:tdd` | Builds MDTM then `/task`. Out of scope. |
| `/sc:workflow` | Generates workflows from PRDs; does not execute. Upstream producer of specs. |
| `/sc:reflect` | Post-hoc audit. Not invoked by implement. |
| `/sc:test`, `/sc:git` | Optional after a successful run. |
| `/sc:brainstorm`, `/sc:design`, `/sc:tasklist` | Producers of the spec/tasklist implement consumes. |

## 9. Open questions — RESOLVED

<!-- provenance: section=9-resolved; base=variant-2-sonnet-refactorer §10; steal=variant-1/3 positions where they match binding decisions -->

| Question | Position | Why |
|---|---|---|
| Tasklist format: simple markdown vs SuperClaude phase-N | **Any markdown with enumerable tasks + AC.** Phase-N accepted as markdown; MDTM fields ignored except `independent`. Verb+object title QUALIFY as AC; else `E-NO-AC`. | Zero parser. Zero schema. One enumerate function in prose. |
| Reviewer: inline vs fresh subagent | **Inline when N≤3 AND source ≤400 lines AND not compacted. Else one Task subagent.** Never ensemble. No `--reviewer` flag. | Isolation when context is actually fat. Ledger schema is the test, not process shape. |
| Ledger location | **`.dev/implement/<slug>/progress.md`.** `--ledger` override under that prefix. | One known directory; does not dirty the spec; matches `.dev/` as generated-artifact root. |
| 1-task spec: per-task reviewer or skip | **Inline spec-compliance once. No second whole-list pass. No subagent.** | The gate is the product; the extra pass is not. |
| Relationship to `/sc:task` and `/task` | **Implement is the middleweight path. Those stay the heavy path. No silent routing.** MDTM-shaped files execute this protocol; `/task` named only in Will-Not. | Avoids a compatibility maze. User who wants MDTM types `/task` themselves. |
| 20-task cap | **No hard cap. Warn once at N≥20.** | Binding decision 12. Operator splits if they want; protocol does not refuse. |
| `--force` | **Forbidden.** Continue after non-compliant only via operator Ruling. `E-NO-RULING`. | Binding decision 7. |
| Intake ref | **Intake lives in SKILL.md.** Only `refs/qa.md` and `refs/ledger.md`. | Binding decision 2. |
| Extras vs QA order | **Implement → spec-compliance QA → extras.** | Binding decision 5; already V2. |
| Halt after fail | **Exactly one fix pass, then HALT.** | Binding decision 7; V1. |

## 10. Risks / edge cases

<!-- provenance: section=10-risks; base=variant-2-sonnet-refactorer §11; steal=variant-1 §13 20-task warn; steal=variant-3 §11 named cases minus dropped E-* -->

| Risk / case | Handling |
|---|---|
| User pastes a pitch out of habit | STOP `E-LEGACY` or `E-NO-SOURCE`. No "did you mean to brainstorm". One usage line. |
| Spec is 2k lines of design with 40 implicit tasks | Enumerate only explicit list/R-NNN/task headings. If none, `E-NO-TASKS`. Do not "helpfully" slice chapters into tasks. |
| Task has no AC block but verb+object title | Title is the AC (R-021). |
| Task title is a single word (`auth`) | `E-NO-AC` before any edit for that task. |
| Missing AC on T2 of 5 | T1 may complete; STOP `E-NO-AC` before T2 edits. |
| Independent tasks share a file | Parallel bound still 3; if overlap is obvious from the task text (`same file`), stay sequential. Do not build a dep graph. |
| Extras command not found | `skip`. Do not install tools. |
| `make test` is the whole SuperClaude suite on a docs-only task | Touched files disjoint → `unrelated-red`. Prefer the cheapest detected command. |
| Lint fail, spec citations complete | `verdict=compliant` `extras=lint:fail` `status=complete` |
| Spec missing, lint green | `verdict=missing` `extras=lint:pass` `status=blocked` then one fix; then `E-HALT-QA` if still missing |
| Tests red, traceback in other package, Ti files clean | `test=unrelated-red`; spec verdict unchanged; no spec HALT |
| Tests red in Ti file | `test=fail`; spec verdict unchanged unless AC required that test |
| Empty diff after "done" | `cannot-verify` → one fix → still empty → `E-HALT-QA` |
| Extra file in diff vs Ti brief | `verdict=extra` → one fix (revert or justify) → else HALT |
| Implemented opposite of AC | `verdict=misunderstood` → one fix → else HALT |
| Ruling missing cost-if-wrong, or executor-authored | invalid; stay `blocked`; `E-NO-RULING` if they try to continue |
| Ruling used to skip all QA | Allowed by grammar **only** as operator-authored line; cost-if-wrong is mandatory. Do not add a second approval ritual. |
| Two `/sc:implement` runs on the same path | Same ledger. Resume. No second directory unless `--ledger`. |
| Compaction mid-task | Resume starts that task again. Partial edits stay in the working tree; reviewer judges the eventual diff. No crash-recovery format. |
| Compaction with truncated last line | `E-LEDGER-CORRUPT` |
| Plugin copy drift | Edit `src/` only; `make sync-dev`; plugin sync is the existing pipeline. Spec does not add a third copy. |
| Docs (`docs/user-guide/commands.md`) still describe persona-mode implement | Follow-up in the same rewrite PR if the file names the old UX; not a new subsystem. |
| Check 3 warn if command >200 lines | Fail the rewrite if the dispatcher exceeds 150 (N-001). |
| N=20 or N=21 | Warn once; sequential unless marked independent; no STOP. |
| Git unavailable | `sha=nogit`; extras/git diff fall back to files written this task. If that list is missing → `cannot-verify`. |
| Auggie unavailable | Warn, continue. |
| Path is a directory | `E-SOURCE-MISSING` |
| `--ledger` outside `.dev/implement/` | `E-LEDGER-PATH` |
| `/sc:implement @spec.md --type api` | `E-LEGACY` |

## 11. Success criteria for the rewrite

<!-- provenance: section=11-success; base=variant-2-sonnet-refactorer §12; steal=variant-3 S1–S11 static checks without Python package; steal=variant-1 Activation/lint -->

The rewrite (later `/sc:improve`) is done when all of the following are true:

1. `src/superclaude/commands/implement.md` is a thin dispatcher (≤150 lines) with Required Input, STOP usage, path-only examples, `## Activation` → `Skill sc:implement-protocol`, and **none** of: `--type`, `--framework`, `--safe`, `--with-tests` as supported flags, "ready for `/sc:test`", persona activation as the method.
2. `src/superclaude/skills/sc-implement-protocol/SKILL.md` exists; loop = enumerate → implement → spec-compliance → one-fix-or-HALT → extras → ledger line → next; SKILL.md ≤ 500 lines; refs are exactly `qa.md` and `ledger.md`.
3. `make lint-architecture` Check 1, 2, 6, 8, 9 pass for `implement` / `sc-implement-protocol`.
4. `make verify-sync` passes after `make sync-dev`. No `.claude/skills` or `.claude/commands` staged.
5. Grep of the two SoT files finds zero pitch examples and zero "compiles" / "ready for testing" completion criteria.
6. A fixture file with no enumerable tasks produces STOP `E-NO-TASKS` and zero file writes.
7. A fixture with two checkbox tasks (verb+object titles) produces two ledger `complete` lines, each with a `verdict=` and an `extras=` field (values may be `skip`), plus a `start sha=` line per task.
8. Resume on that ledger starts at the first task whose latest status is not `complete`.
9. A planted Extra in the diff yields `verdict=extra`, one fix pass, then `E-HALT-QA` if still extra, and no next-task work until operator Ruling.
10. No new Python module, no dual-mode flag, no `/task` handoff, no reviewer ensemble, no `--reviewer`, no `--force`.
11. Skill contains the five verdict strings, the halt table, and the nine `E-*` codes. Ledger regex in `refs/ledger.md` matches §7. Negative example `Task 1: done` fails the verdict regex.
12. A fixture task titled `auth` (no verb+object, no AC block) STOP `E-NO-AC` before any edit for that task.
13. N=21 headings does **not** STOP. Warn-once text is in the skill.
14. MDTM-shaped fixture is executed by this protocol (ceremony ignored); skill does not invoke `/task`.

### Static checks to leave behind

Grep tests (existing pytest in this repo is enough; no new Python package, no grader.py, no evals.json):

| Check | Assertion |
|---|---|
| S1 | `## Activation` and `Skill sc:implement-protocol` in `commands/implement.md` |
| S2 | `src/superclaude/skills/sc-implement-protocol/SKILL.md` exists |
| S3 | command ≤150 lines, SKILL.md ≤500 |
| S4 | `argument-hint` contains a path token; does not contain `--type` as a flag |
| S5 | Grep command file: 0 hits for `user profile component` as an example |
| S6 | Triggers do not list free-form "Feature development requests" as activation |
| S7 | Skill contains the five verdict strings and the halt table |
| S8 | `refs/ledger.md` regex matches §7; four positive examples + one negative |
| S9 | Grep skill: no invocation of `/task`, `sc:task-protocol`, `/sc:reflect` as a step (allow "do not" / Will-Not) |
| S10 | `make lint-architecture` Check 1 includes `implement → sc-implement-protocol` |
| S11 | `make verify-sync` exit 0 after `make sync-dev` |
| S12 | Banned flags are not in Options as supported usage |
| S13 | Nine slim `E-*` codes present; `E-TOO-MANY` / `E-WRONG-TOOL` absent as STOP codes |

### Transformation path (binding)

Ship the thin dispatcher + skill with the loop in **one** cut.

Do not leave the old Analyze→Plan→Generate flow behind a flag. Do not accept `[feature-description]` as a valid invocation. Do not document "for simple features, the old command still works".

Skipped: dual-mode, MDTM parser, Part 2 quality review, Python CLI, 20-task cap, intake ref, `--reviewer`. Add those only if this loop fails in real use.

A reviewer can fail the rewrite by pointing at a missing STOP, a missing skill dir, extras used as the gate, F1/MDTM imported, executor-authored rulings, or a hard 20-task cap.

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-24T19:48:06.866Z","contentHash":"719bf27c","sections":[{"heading":null,"hash":"47a5a156"},{"heading":"Merged requirements — rewrite `/sc:implement`","hash":"3137fde7"},{"heading":"1. Problem / goals","hash":"8ae668eb"},{"heading":"Problem","hash":"62fb910e"},{"heading":"Goals","hash":"31558113"},{"heading":"Non-goals (this rewrite)","hash":"9d04860f"},{"heading":"Design principles (binding)","hash":"d39c83e2"},{"heading":"2. Functional requirements","hash":"847b513e"},{"heading":"R-001. Required source path","hash":"977caf74"},{"heading":"R-002. Enumerable tasks required","hash":"4feef8c4"},{"heading":"R-003. Sequential by default; parallel only when marked, max 3","hash":"24d2e7b3"},{"heading":"R-004. Per-task spec-compliance verdict","hash":"25e9012f"},{"heading":"R-005. Reviewer evidence; do not trust the implementer","hash":"50cad425"},{"heading":"R-006. One fix then HALT; operator Ruling only","hash":"20b70594"},{"heading":"R-007. `cannot-verify` is not a pass","hash":"e6269422"},{"heading":"R-008. Extras after verdict, never the gate","hash":"2a0b826b"},{"heading":"R-009. Unrelated red is not a fail","hash":"2cc41eb8"},{"heading":"R-010. One markdown ledger","hash":"de1ddf8a"},{"heading":"R-011. Resume from first non-complete","hash":"acd5426c"},{"heading":"R-012. Whole-list review","hash":"caaceada"},{"heading":"R-013. Activation","hash":"4b1fa245"},{"heading":"R-014. Protocol skill package","hash":"0367e24d"},{"heading":"R-015. Hard cutover; legacy grammar STOP","hash":"922c3339"},{"heading":"R-016. Done is ledger-complete, not compile-ready","hash":"88138d07"},{"heading":"R-017. No `/task` routing; MDTM still uses this protocol","hash":"f32edba6"},{"heading":"R-018. Spec is binding","hash":"a8f3b0a4"},{"heading":"R-019. Source of truth is `src/superclaude/`","hash":"43b067fa"},{"heading":"R-020. One rewrite, no dual grammar","hash":"dd1a894f"},{"heading":"R-021. AC required; verb+object title QUALIFY","hash":"0c8d73b4"},{"heading":"R-022. Start-SHA before first edit","hash":"56647c2e"},{"heading":"R-023. Reviewer mode (no flag)","hash":"83a3db7a"},{"heading":"R-024. Slim STOP codes","hash":"09cb5373"},{"heading":"R-025. Warn once at N≥20; no hard cap","hash":"276bda23"},{"heading":"3. NFRs","hash":"ddc9660d"},{"heading":"4. Architecture","hash":"6c863bac"},{"heading":"What to build (four files)","hash":"6d39530f"},{"heading":"Command file (dispatcher only)","hash":"918d1780"},{"heading":"Activation","hash":"12e60b91"},{"heading":"Skill (the loop)","hash":"4f5ab4ae"},{"heading":"Makefile / sync","hash":"4a34cc8c"},{"heading":"What NOT to build","hash":"7592f13f"},{"heading":"Delete from current `implement.md`","hash":"9020b8ce"},{"heading":"5. Input contract + STOP table","hash":"2b8dcfa3"},{"heading":"Invocation","hash":"ba9f2312"},{"heading":"STOP table (no work, print usage + code)","hash":"0fa19d15"},{"heading":"Not STOP","hash":"82e48337"},{"heading":"Usage text (exact shape)","hash":"8d42dbf7"},{"heading":"Enumerable tasks","hash":"84584d28"},{"heading":"AC QUALIFY (normative)","hash":"be1fc5bf"},{"heading":"6. Per-task loop + halt table","hash":"f9442775"},{"heading":"Order (fixed)","hash":"99676bee"},{"heading":"Rubric (reviewer vs the brief)","hash":"88f74a25"},{"heading":"Halt table","hash":"9d4df3e7"},{"heading":"`cannot-verify` next actions (during the one fix pass)","hash":"8eb6570c"},{"heading":"Reviewer isolation (fail the rewrite if violated)","hash":"d9e25978"},{"heading":"1-task source","hash":"ff96038b"},{"heading":"7. Ledger schema (exact)","hash":"2cf9e16b"},{"heading":"Location","hash":"55c9a99d"},{"heading":"Header (line 1 only)","hash":"bb891e87"},{"heading":"implement ledger — source: <abs-or-repo-relative-path> — created: <ISO-8601>","hash":"de354e42"},{"heading":"Start line (once per task, before edits)","hash":"0a49ddee"},{"heading":"Verdict line (once per completed review)","hash":"430e3710"},{"heading":"Ruling line (operator-supplied only)","hash":"f3691f3d"},{"heading":"Post-ruling complete line","hash":"01be2263"},{"heading":"Final review line (optional)","hash":"83b9ac58"},{"heading":"Rules","hash":"a811ace2"},{"heading":"Resume algorithm (normative)","hash":"c9908ce7"},{"heading":"8. Out of scope","hash":"0459a899"},{"heading":"9. Open questions — RESOLVED","hash":"960b490c"},{"heading":"10. Risks / edge cases","hash":"ac6875aa"},{"heading":"11. Success criteria for the rewrite","hash":"97f6dd53"},{"heading":"Static checks to leave behind","hash":"b93043a0"},{"heading":"Transformation path (binding)","hash":"485694cc"}]}-->
<!--mc:threads:end-->
