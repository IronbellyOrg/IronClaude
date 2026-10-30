# Validation: one-off task minimum, /sc:task vs /sc:implement

Date: 2026-10-27. Read-only research. Sources are files on disk under /home/coder/.claude/ (paths below). Nothing was executed.

## Verdict

1. `/sc:implement --depth quick` is not valid: `/sc:implement` has no `--depth` flag (E1); `--depth quick` belongs to `/sc:workflow`, which is the guide's level 3, not a one-off.
2. The true minimum for a one-off is a plain edit plus the related test (guide level 2 says "or a plain edit", HWW:16, 304). Of the two commands, `/sc:implement "<prompt naming file, change, test>"` is the better optional add-on: it takes a plain prompt, reviews against the prompt with `path:line` citations, and leaves a ledger. `/sc:task` should not stay WORTH IT (E3.10, E3.11, E3.14).
3. Retiring `/sc:task` standalone is safe: its only programmatic caller is `/sc:tasklist` Stage 9 (E5.1); deleting the skill would break that.

## Evidence

Path prefix `~/.claude/` = `/home/coder/.claude/`. `impl-cmd` = `commands/sc/implement.md`, `impl-skill` = `skills/sc-implement-protocol/SKILL.md`, `task-cmd` = `commands/sc/task.md`, `task-skill` = `skills/sc-task-protocol/SKILL.md`, `HWW` = `HOW-WE-WORK.md`.

### E1. Does `/sc:implement` accept `--depth`? No.

- E1.1 The option table lists only `<path>`/`--spec`/`--prd`/`--tasklist`, `<prompt>`, `--resume`, `--ledger`, `--skip-final-review` (impl-cmd:53-59). The argument-hint says the same: `<path-or-prompt> [--resume] [--ledger <path>] [--skip-final-review]` (impl-cmd:6).
- E1.2 The protocol's known-option list is `--spec`, `--prd`, `--tasklist`, `--resume`, `--ledger`, `--skip-final-review` (impl-skill:49). Banned tokens are `--type`, `--framework`, `--safe`, `--with-tests`, plus `--force` (impl-skill:49, 32-34). `--depth` is in neither list.
- E1.3 What happens if `--depth quick` is typed anyway is not specified. Reading impl-skill:50-51 literally, `--depth` starts as an option token, only `--spec`/`--ledger` take values, so `quick` would be the first non-option token and would start an inline prompt. That is an inference from the tokenizer text, not a documented behavior: UNVERIFIED. Do not rely on it.
- E1.4 Where `--depth quick|standard|deep` really exists: `/sc:workflow` (`commands/sc/workflow.md:7,39`), `/sc:brainstorm` (`commands/sc/brainstorm.md:49`), `/sc:troubleshoot` (`commands/sc/troubleshoot.md:51`), `/sc:analyze` (`commands/sc/analyze.md:22`, only `quick|deep`), `/sc:adversarial`, `/sc:roadmap`, `/sc:auggie-review`, `/sc:research`. A grep of `commands/sc/` for `--depth` found no hit in `implement.md` or `task.md`.
- E1.5 The only `--depth quick` in the guide for small plans is on `/sc:workflow`, then `/sc:implement <plan path>` (HWW:17, HWW:113-115, HWW:305). On `/sc:workflow`, quick means 2-4 phases and the schema-minimum gate (`skills/sc-workflow-protocol/SKILL.md:38,52`; `refs/phase-templates.md:13`). That is the nearest real equivalent, and it is level 3 of the guide, not a one-off.
- E1.6 Tiers inside `/sc:implement`: there are none. It has one path (Q0-Q8, impl-skill:102-131). The only variation is reviewer mode (inline vs one subagent, impl-skill:98-100) and a skipped whole-list pass when N=1 (impl-skill:133,153).

### E2. What input does `/sc:implement` need? A plain prompt is enough.

- E2.1 The mandatory input is "a source": an existing file, or inline prompt text in `$ARGUMENTS` (impl-cmd:24-29). Only a bare `/sc:implement` stops (`E-NO-SOURCE`, impl-skill:17,28). The example `/sc:implement Add logout to the header and wire it to /logout` is in impl-cmd:43,94-99.
- E2.2 The prompt is saved to `.dev/implement/<slug>/source.md` before any product edit; `<slug>` = first 24 slug-chars of the prompt + 8 hex chars of SHA-256 of the full prompt (impl-skill:60; impl-cmd:56).
- E2.3 A prompt becomes one task whose acceptance criterion (AC) is the prompt text (impl-cmd:29; impl-skill:87-88 rule 5, 62). A one-word or empty-intent prompt stops with `E-NO-AC` before any edit (impl-skill:90).
- E2.4 No plan file is produced or needed, so it is not "too heavy" on input. Nothing has to run first.
- E2.5 Consequence for a one-off: the prompt itself must name the file, the exact change, and the test (for example "and update tests/test_runner.py"). The reviewer judges only against that text, "do not grow scope past it" (impl-skill:88), and an AC not observable from the diff with no check or test added is `cannot-verify`, which is not a pass (`refs/qa.md:52`).

### E3. What checks each command actually runs

`/sc:implement` (one-task run, from impl-skill:102-131 and `refs/qa.md`):

- E3.1 Q0 snapshots the git tree and pins it as `refs/superclaude/implement/<slug>/T<id>` (impl-skill:107-114). Q1 implements only that task. Q2 takes `git diff "$start"`, including full contents of untracked new files (impl-skill:118-120).
- E3.2 Q3-Q4: a reviewer "not the implementer voice" checks each AC against the diff, with a `path:line` citation per AC. Closed verdict: `compliant | missing | extra | misunderstood | cannot-verify`. Zero citations means `cannot-verify` (`refs/qa.md:25-52`).
- E3.3 The reviewer is inline in the same session when N<=3, source <=400 lines and the session is not compacted (impl-skill:100; `refs/qa.md:83`). So for a one-off the review is not a separate agent. It follows a written rubric but is not independent in the strong sense.
- E3.4 Q5: exactly one fix pass if not compliant. Still non-compliant gives `E-HALT-QA` and stops (impl-skill:127,33; `refs/qa.md:54-63`).
- E3.5 Q6 extras: lint, typecheck and tests are detected and run only if they already exist, "Do not install tools", cheapest command scoped to the task's files (impl-skill:135-145). They are recorded but never the pass/fail (impl-skill:11,147; impl-cmd:128).
- E3.6 For N=1 the whole-list FINAL review is skipped (impl-skill:133,153).
- E3.7 No LIGHT or EXEMPT tier exists in `/sc:implement`. A tiny task gets the same Q0-Q8.

`/sc:task` (from task-cmd and task-skill):

- E3.8 First output must be a classification header with TIER in `STRICT|STANDARD|LIGHT|EXEMPT`, as text, before any tool call (task-cmd:50-69). First match in priority order: STRICT, EXEMPT, LIGHT, STANDARD (task-cmd:71-91).
- E3.9 STRICT keywords include `refactor`, `database`, `migration`, `token`, `session`, `security`, `authentication`; "security always wins" and ">2 estimated files" adds weight (task-cmd:73-77). A single-file `refactor` or `token` change is therefore STRICT. A "rename a field and update its test" prompt is most likely STANDARD (keywords `update`/`change`); that is my reading of the keyword tables, not a tested result.
- E3.10 LIGHT and EXEMPT: "Execute immediately", "No Skill invocation needed" (task-cmd:99-100). Verification is "Skip" for both (task-skill:127-129). This is what the guide itself warns about (HWW:16, HWW:304).
- E3.11 STANDARD: invoke `sc:task-protocol`: load context, search downstream impacts, make changes, "Run affected tests OR document manual verification", verify basic functionality (task-skill:100-106). Tests are one of two acceptable options. No acceptance criteria, no diff review, no verdict, no citations.
- E3.12 STRICT: serena project activation, clean git status, spawn a `quality-engineer` verification agent, run `pytest`, answer adversarial questions (task-skill:86-98, 126). The only "reviewer" in the whole command exists here.
- E3.13 Test Failure Escalation Protocol (TFEP): if a pre-existing test fails (or 3+ new fail), freeze, write `context.yaml`, call `/sc:troubleshoot --caller task-unified --depth standard|deep`, and at the 3rd trigger FULL STOP (task-skill:135-273). This applies to STANDARD and STRICT, not LIGHT/EXEMPT (task-skill:143). It needs a pre-implementation test baseline via pytest-style collection (task-skill:157-166; the example command is `uv run pytest --collect-only -q`, which assumes Python).
- E3.14 The command's own stated triggers are complexity >0.6, more than 2 files, security paths, refactoring (task-cmd:31-36; task-skill:29-35). A one-file, five-edit change meets none of them. The guide's level-2 use of `/sc:task` (HWW:16) is not what the command file says it is for.

### E4. Footprint on disk: see the dedicated section below (evidence is in the footprint table).

### E5. Is `/sc:task` invoked inside other skills or commands?

Grep of `~/.claude/commands`, `skills`, `agents`, `HOW-WE-WORK.md`, `CLAUDE.md` for `sc:task`, `sc-task-protocol`, `/sc:task`, excluding the two `sc:task` files themselves:

- E5.1 A real caller: `skills/sc-tasklist-protocol/SKILL.md` Stage 9 "Patch Execution (Delegate to `sc:task`)": "Invoke `sc:task` via the `Skill` tool" with `--compliance strict`, against `PatchChecklist.md` (lines 1535-1557); the loop-back at :1557 and :1607; stage table :1693; task text :1728, :1756, :1776. Also :16 and :592 reuse its classification algorithm. This is the only programmatic invocation found.
- E5.2 Forbidden by `/sc:implement`: "Do not invoke `/task`, `/sc:task`, or `sc:task-protocol`" (impl-skill:11) and "Invoke `/task` or `/sc:task`" under Will Not (impl-cmd:129).
- E5.3 Not callers (they only mention it): `commands/sc/reflect.md:21,309` and `skills/sc-reflect-protocol/SKILL.md:54,1006` describe `sc:task-protocol` calling reflect as an "end-of-task hook when configured", marked "deferred" (reflect.md:309). `commands/sc/validate-tests.md:133-134` and `skills/sc-validate-tests-protocol/SKILL.md:32,426` test the tier rules (contributor tooling, HWW:285).
- E5.4 Stale-looking operator text: `skills/sc-crash-recovery/refs/pipelines.md:25,39,173` tell the user to run `/sc:task <MDTM file path>` for recovery of old `TASK-PRD`/MDTM tasks, while the same file at :179 says `/sc:workflow` packages route to `/sc:implement`, "never to MDTM `/task` or `/sc:task`". Whether `/sc:task <file path>` even works is UNVERIFIED (task-cmd takes a description, not a file).
- E5.5 Guide references: HWW:16 (level 2), HWW:119, HWW:242 ("`/sc:task` does one job directly, with no file"), HWW:285, HWW:304 (routing row `small-change`: "`/sc:task "<change>"` or a plain edit").
- E5.6 Net for retirement: dropping standalone use is consistent with the files (the one real caller, tasklist Stage 9, uses the Skill route, not a user command). Deleting the command or skill would break `/sc:tasklist` Stage 9, which is part of the separate roadmap pipeline the existing analysis already rates SKIP (command-value-by-phase.md:113-114).

## Flag table (as found on disk)

### `/sc:implement` (impl-cmd:6, 36-61; impl-skill:49)

| Flag | Values | Default | Notes |
|---|---|---|---|
| `<path>` / `--spec` / `--prd` / `--tasklist` | one existing file | one of path or prompt | aliases for one file |
| `<prompt>` (leftover text) | free text | one of path or prompt | saved to `.dev/implement/<slug>/source.md`; becomes one task |
| `--resume` | switch | implicit if a matching ledger exists | continues from first non-complete task |
| `--ledger <path>` | path under `.dev/implement/` | `.dev/implement/<slug>/progress.md` | other paths stop `E-LEDGER-PATH` |
| `--skip-final-review` | switch | off | skips the N>1 whole-list pass; blocks archiving of managed packages |
| `--depth` | NONE | not applicable | not in the option table or the protocol's known-option list; behavior if typed is UNVERIFIED (E1.3) |
| `--type`, `--framework`, `--safe`, `--with-tests`, `--force` | banned | - | `E-LEGACY` / `E-NO-RULING` |

### `/sc:task` (task-cmd:18-48; task-skill:44-50)

| Flag | Values | Default | Notes |
|---|---|---|---|
| `--compliance` | `strict`, `standard`, `light`, `exempt`, `auto` | auto-classified | override of the tier; low confidence (<0.70) prompts the user (task-cmd:93) |
| `--strategy` | `systematic`, `agile`, `enterprise`, `auto` | auto | how to coordinate work |
| `--verify` | `auto` shown in the skill's usage (task-skill:49) | - | full value list not stated in the files read: UNVERIFIED |
| `--skip-compliance` | switch | off | escape hatch |
| `--force-strict`, `--parallel`, `--delegate` | switches | off | named in task-cmd:44; "see protocol skill for full flag reference", but the skill file does not define them: UNVERIFIED |
| `--no-escalation` | switch | `false` | bypasses TFEP (task-cmd:46-48) |
| `--depth` | NONE | not applicable | `/sc:task` has `--compliance`, not `--depth` |

### Nearest real equivalents of "quick"

| Wanted | Real flag | Where |
|---|---|---|
| a smaller plan before implementing | `/sc:workflow ... --depth quick` (2-4 phases, schema-minimum gate), then `/sc:implement <plan path>` | workflow.md:39; HWW:17, HWW:305 |
| a lighter execution tier | `/sc:task ... --compliance light` (no verification at all) | task-cmd:84-87; task-skill:108-113, 127 |
| a lighter `/sc:implement` run | none. A prompt source is already one task, inline review, no FINAL | impl-skill:100, 133 |

## Footprint a checker could see

| Where | `/sc:implement "<prompt>"` | `/sc:task "<change>"` |
|---|---|---|
| Product files | the edited files (and the test, if the prompt asked for it) | the edited files |
| Ledger / progress file | `.dev/implement/<slug>/progress.md`: line 1 header, then `T1: start sha=<40-hex>`, then `T1: complete verdict=compliant ac=T1.AC1 evidence=<path:line,...> extras=lint:..,typecheck:..,test:.. files=<paths>` (`refs/ledger.md:15-59`) | none defined in either file |
| Prompt copy | `.dev/implement/<slug>/source.md`, written before any edit (impl-skill:60) | none |
| Git refs | `refs/superclaude/implement/<slug>/T1` pinned at start, deleted when the task completes (impl-skill:112-114). After a clean run, absent. If left behind, the task did not complete | none |
| Session-visible text | ledger path printed at the end (impl-cmd:73) | `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header with TIER and CONFIDENCE (task-cmd:62-68), plus a human-readable `Tier:` line (task-skill:65-78). Visible only in the session transcript |
| Written only on failure | `E-HALT-QA` leaves a `blocked` verdict line in the ledger (`refs/qa.md:61`) | TFEP only: `{output_dir}/context.yaml`, `return-contract.yaml` from troubleshoot, `tfep-incident-report.md` (task-skill:207, 221, 249-265) |
| Memory / telemetry | none stated | "write_memory: Save session state" (task-skill:319) and "Store for calibration learning" (task-skill:275-281). No path is given for either: UNVERIFIED where or whether anything lands in the repo |

Facts about the repo that matter to a checker (checked on disk, 2026-10-27):

- F1 `.dev/implement/` already exists in this worktree with 4 ledgers (`design-round4-feebe4a4`, `tasks-01ce7210`, `workflow_aidev02-comme-89b93115`, `workflow_orca-agents-def-aadd7099`), each a `progress.md`. The one I read in full (`design-round4-feebe4a4/progress.md`, 3 lines) matches the grammar in `refs/ledger.md`: header, `T1: start sha=...`, `T1: complete verdict=compliant ... files=...`. All four were file-source runs; no `source.md` exists anywhere under `.dev/implement/`, so no prompt-source run has ever been recorded here and the prompt-run layout is UNVERIFIED by observation (it is documented, not seen).
- F2 These 4 ledgers are tracked by git (`git ls-files .dev/implement`), added by bulk commits `92d244ec` (2026-09-27, "preserve untracked session artifacts") and `722c4c9b` (2026-10-19, "preserve uncommitted development records"), not by `/sc:implement`. The ledger rules say "Do not `git add` the ledger" (`refs/ledger.md:3`).
- F3 `.dev/implement/` is not gitignored (`git check-ignore` returned no match; repo `.gitignore` has no `implement` entry). A new run therefore shows as untracked in `git status`. The project `CLAUDE.md` rule "`.dev/tasks/` is always staged" covers `.dev/tasks/` only; it says nothing about `.dev/implement/`, so a one-off ledger is neither required to be staged nor ignored. That is a decision for the team lead, not something the files settle.
- F4 `refs/superclaude/` currently has no refs (`git for-each-ref refs/superclaude` was empty), consistent with F1 (all runs completed and unpinned).
- F5 Managed packages (`.dev/tasks/to-do/TASK-WF-*`, sibling `progress.md`, archive to `done/`) apply only to `/sc:workflow` plans (impl-cmd:63-65). A prompt-source `/sc:implement` is not managed, so none of that footprint (FINAL line, `ARCHIVE:` lines, `done/` move) applies to a one-off.
- F6 Net for a scheduled checker: `/sc:implement` is detectable by file (`.dev/implement/*/progress.md`, last-line regex in `refs/ledger.md:56`). `/sc:task` and a plain edit leave nothing but the git diff; they can only be inferred from the transcript or commit contents.

## What to change in command-value-by-phase.md

File: `/home/coder/workspaces/worktrees/Coder/IB-CPlus-01/_bmad-output/brainstorming/brainstorm-clay-feedback-decisions-2026-10-26/command-value-by-phase.md`. Columns are T (one-off), B, S, F, R, N (line 48). Line numbers are as of 2026-10-27 15:2x. These are recommendations for the lead to apply; I edited nothing there.

| Line | Row | Now | Change to |
|---|---|---|---|
| 145 | 2.4 `/sc:task` | T = WORTH IT, B = OPTIONAL, rest SKIP; note "Guide level 2 ... A plain edit also satisfies level 2" | T = SKIP, B = SKIP. Replace the note with: "Retired as a standalone command (lead's decision). Its only programmatic caller is `/sc:tasklist` Stage 9 (`sc-tasklist-protocol/SKILL.md:1535-1557`), a separate pipeline. Command file's own triggers are >2 files, security paths, refactors (`task-cmd:31-36`), not small changes. The guide still names it at HOW-WE-WORK.md:16, 304; the guide is shipped by `superclaude update` and is not ours to edit." |
| 143 | 2.4 `/sc:implement` | T = SKIP | T = OPTIONAL. Append to the note: "Also accepts a plain prompt (`/sc:implement "<change, file, test>"`), no plan file; one task, inline spec-compliance review, ledger at `.dev/implement/<slug>/progress.md`. There is no `--depth` flag (`--depth quick` belongs to `/sc:workflow`)." Keep REQUIRED for S. |
| 233 | O7 pick | "...no file, tiny change -> `/sc:task` or a plain edit" | "...no file, tiny change -> a plain edit + the related test; `/sc:implement "<prompt>"` when a ledger record is wanted" |
| 238 | O12 pick and reason | pick "Plain edit + related test, or `/sc:task`"; reason "Guide level 2. `bmad-quick-dev` ..." | pick "Plain edit + related test. Optional: `/sc:implement "<prompt>"` for a checkable record". Reason: "Guide level 2 says 'or a plain edit' (HWW:304). `/sc:task` is retired standalone. `bmad-quick-dev` produces a spec file first, which is overkill at T size." In column 3 (alternatives) keep `/sc:task` listed but mark "(retired)". |
| 252 | Section 4, One-off task | step 1 "edit (plain, or `/sc:task`)"; additions "`/sc:task` (T: WORTH IT), `/sc:test`" | step 1 "plain edit that includes the related test"; additions "`/sc:implement "<prompt>"` if a checker-visible record is wanted (T: OPTIONAL), `/sc:test`". Remove `/sc:task` from the additions |
| 147 | `bmad-quick-dev` note | "BMad-lane substitute for `/sc:task` on small work. ‡ with `/sc:task`" | Replace both `/sc:task` mentions with "a plain edit + test" |
| 252, 276 area | Section 4b footprint | line 276 says `/sc:implement (beyond progress.md)` has no stated footprint | Add one line: "`/sc:implement "<prompt>"`: `.dev/implement/<slug>/source.md` and `progress.md` (`refs/ledger.md`); `/sc:task`: none defined (UNVERIFIED for memory/telemetry)." |

Also fix in Section 5 (unverified items) if kept: replace any claim that `/sc:task` is WORTH IT for T with a pointer to this file.

A caution on the one thing the earlier file got right: "plain edit + test" is the true minimum and the guide says so (HWW:16, HWW:304 "or a plain edit"; hard limit at HWW:22). The earlier file's WORTH IT rating for `/sc:task` is not supported by the command's own text (E3.10, E3.11, E3.14).

## Unverified items

- U1 What `/sc:implement ... --depth quick` does when typed. Not documented; my tokenizer reading (E1.3) says `quick` would join the prompt. Needs a run to confirm, which I was told not to do.
- U2 Whether a prompt-source `/sc:implement` run behaves as documented (layout of `source.md` and `progress.md`). No prompt-run exists in this repo to inspect (F1). Only file-source runs were observed.
- U3 Which tier `/sc:task` would actually assign to a given one-file prompt. Classification is model-performed from the keyword tables (task-cmd:52-93); I did not run it. My STANDARD guess in E3.9 is a reading, not a result.
- U4 Where `/sc:task`'s "Save session state" memory and "calibration learning" feedback go, and whether anything is written inside the repo (task-skill:275-281, 317-320).
- U5 Full value list for `/sc:task --verify`, and definitions of `--force-strict`, `--parallel`, `--delegate` (task-cmd:44 points to the skill, the skill does not define them).
- U6 Whether `/sc:task <path to MDTM file>` works as `skills/sc-crash-recovery/refs/pipelines.md:25,173` implies.
- U7 Whether the inline reviewer in `/sc:implement` is meaningfully independent in practice (it is "not the implementer voice" by rubric, same session by design; impl-skill:100, `refs/qa.md:83`). Rubric strength is documented, observed quality is not.
- U8 Cost and time of a one-task `/sc:implement` versus a plain edit. Neither file states a token or time figure for `/sc:implement`. Only `/sc:task` states rough token costs per tier (task-skill:124-129).
- U9 Whether the installed copies in `~/.claude/` match the repo source (`src/superclaude/...`, referenced at impl-cmd:83 and task-cmd:161). I read the installed copies only; the repo source was not in this workspace.
- U10 The 2026-09 `.dev/implement/` ledgers are from a different checkout path (`/config/workspace/Coder/...`, header of `design-round4-feebe4a4/progress.md`); I treated their format as representative of the current protocol because they match `refs/ledger.md`.
