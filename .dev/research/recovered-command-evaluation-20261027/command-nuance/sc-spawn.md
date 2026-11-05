# /sc:spawn: scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: `/home/coder/.claude/commands/sc/spawn.md` (210 lines, cited as CMD). Backing protocol skill `/home/coder/.claude/skills/sc-spawn-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"). Other files cited: `/home/coder/.claude/HOW-WE-WORK.md` (HW), `/home/coder/.claude/skills/task-builder/SKILL.md` (TB), `.dev/plans/top9-issues-20261001/` (TOP9, repo-relative).

## 1. Status and role
- Role (CMD:3, CMD:192-194): "Meta-system task orchestration with intelligent breakdown and delegation", but it STOPS after producing a task hierarchy (Epic, Story, Task, Subtask) and delegates execution to other `/sc:*` commands; it writes no code. Phase served: Tasklist (decompose only). Standalone-invokable: yes; no file marks it retired or deprecated. No backing skill, so it runs from its own file (HW:232).
- Routing: HW lists it only under "Other commands ... no workflow above routes to them" (HW:262, HW:282: "For work that changes code, prefer `/task-builder`"); it is absent from the six levels, workflows 3.1-3.12 and the routing table (HW:301-325; grep for `spawn` in HW returns line 282 only).
- Overlaps: `/task-builder`, `/sc:workflow`, `/roadmap`, `bmad-create-epics-and-stories`. Answer to the focus question: no complexity band is justified by any file (section 3); it is effectively retired from the pipeline (JUDGMENT), though not formally retired by a file. It names the retired `/sc:task` once (CMD:124, section 2).

## 2. Flags
Only one usage line defines flags (CMD:22): `/sc:spawn [complex-task] [--strategy sequential|parallel|adaptive] [--depth normal|deep]`. Frontmatter has no `argument-hint` (CMD:1-8). There is no backing skill, so no second source.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[complex-task]` (positional) | free text | none stated; a bare call is not addressed in the file | The operation to decompose (CMD:22, CMD:27) | Only for the narrow case in section 3 (R/HIGH batch) | Any code-changing job with files nameable up front: use `/task-builder` (HW:282) |
| `--strategy` | `sequential`, `parallel`, `adaptive` | NOT STATED | Names the coordination strategy recorded in the output ("Coordination strategy", CMD:208). Key Patterns defines them as "Sequential (dependency-ordered) -> Parallel (independent) -> Adaptive (dynamic)" (CMD:146). Whether it changes anything beyond a label is UNVERIFIED, because the command also says it does not execute (CMD:192-201) | `adaptive` (JUDGMENT) when a batch mixes dependent and independent items, as in TOP9 spawn-runbook.md section 5 lanes | When all items are one dependency chain: the choice is moot |
| `--depth` | `normal`, `deep` | NOT STATED | Nothing in the file says what it changes. Only evidence is the example `... --strategy adaptive --depth deep` described as "Enterprise-scale operation with sophisticated orchestration" (CMD:163-165). Effect UNVERIFIED | `deep` is only evidenced for "migrate legacy monolith"-class jobs (CMD:163) | Do not confuse with `/sc:workflow --depth quick\|standard\|deep` (workflow.md line 7): value sets differ |

**Does not exist** (people may assume): `--depth quick` or `--depth standard` (value set is `normal|deep` only, CMD:22); `--handoff` (exists on `/sc:workflow`, workflow.md line 7); `--spec` (task-builder only, HW:18); any output-path flag (output path never specified, CMD:203-208); `--resume` or any ledger/progress file; `--dry-run`; any flag that makes it execute tasks. Frontmatter `complexity: high` (CMD:5) is metadata, not a flag.

**Internal contradiction in CMD (affects what a user gets):** Behavioral Flow step 4 says "Orchestrate: Execute tasks using optimal coordination strategy" and step 5 "Monitor: Track progress" (CMD:30-31), and Will says it will "Execute meta-system operations" (CMD:182). The closing section says "STOP AFTER TASK DECOMPOSITION ... Explicitly Will NOT: Execute implementation tasks directly" (CMD:192-201). I treat the closing section as binding (JUDGMENT; later and capitalised, and Will Not at CMD:186-188 does not contradict it). Untested.

**Retired-command reference:** CMD:124 lists, as a case where Rule 2.5 is NOT triggered, "any `/sc:task` invocation without an adversarial-debate stage". That is the only mention of `/sc:task` (grep over CMD for `sc:task\|sc:tasklist`). Its delegation list (CMD:210) names `/sc:implement`, `/sc:design`, `/sc:test`: not retired commands. It never names `/task`, `/task-builder` or `/sc:workflow`.

**Rule 2.5 is inert in this repo:** it fires only for a single Python function in a failing-test cohort of 4 or more (CMD:78-83) and is "NOT triggered" for non-Python targets (CMD:124). `docs/generated/PROJECT_INDEX.md` (Structure) shows a Terraform/shell/workflow repo. Rules 1-3 (absolute paths, tiered evidence standard, count injection; CMD:45-128) are prompt-writing practices, not flags.

## 3. Scope x complexity matrix
**Does it vary by complexity?** Barely. CMD's triggers are all "complex", "multi-domain", "large-scale" (CMD:14-17) and Will Not says it does not "Replace domain-specific commands for simple operations" (CMD:186). So only the HIGH band is even in its stated domain. CMD names no file counts, no session counts, no thresholds, and no spec input. The only on-disk numeric formula, task-builder's TCS (TB:2402-2433: quick <=12, standard 13-34, deep >=35), scores a finished task file, so it cannot be computed on a spawn input; I use it only as the band vocabulary.

Band definitions for this command (signals from the brief; edges are JUDGMENT, no numbers invented):
- LOW: author can name the files up front, one subsystem, fits one or two sessions (HW:17 level 3 profile; TB:2431 TCS <=12 profile).
- MEDIUM: several files or subsystems, one domain, more than one session, a driving spec exists or is easy to write (HW:18 level 4 profile).
- HIGH: several independent work items or domains, shared files between them that force ordering ("lanes" in TOP9 spawn-runbook.md section 5: PIN, ENV, TEST-57), or risk items (secrets, infrastructure) in some of them.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP | SKIP | N/A (J): a one-off that is HIGH is not a one-off; HW:22 hard limit sends it to a written plan |
| B bug fix | SKIP | SKIP | SKIP (bug route 3c is `/task-builder` + `/task`, HW routing row `bug`, HW:311) |
| S single story | SKIP | SKIP | SKIP (levels 3 and 4, HW:17-18) |
| F multi-story feature | SKIP | SKIP | SKIP (`/task-builder` + `/task` is the validated minimum; `validation-feature-task-builder-vs-sc-workflow.md` line 11) |
| R multi-feature release | SKIP | SKIP | OPTIONAL (J), no flag set evidenced; `--strategy adaptive` if used. Sole candidate band, see below |
| N new product | N/A (J): never LOW | SKIP (J): `/roadmap` is REQUIRED here in `command-value-by-phase.md` and produces the same decomposition plus task files | SKIP (J): same reason |

**Why R/HIGH is the only non-SKIP cell, and how weak the evidence is.**
- For: TOP9 is a batch of nine open issues described as a `/sc:spawn` decomposition (Epic, then Story per issue, then Task per chain stage), "stopped before delegation" (`spawn-runbook.md:5`), with cross-issue file lanes (`spawn-runbook.md` section 5) and a per-issue pipeline. Nothing file-backed in the pipeline decomposes a batch of independent items with cross-item ordering: `/task-builder` and `/sc:workflow` take one job, `/roadmap` takes a spec (HW:75). The adversarial review scored that runbook 0.977 against 0.867 for the BMad alternative (`adversarial/top9-recommendation.md:14`).
- Against: (1) it is a batch of issues, not strictly a release as Ryan defines R; (2) the runbook header says "Nothing in this runbook has been executed" (`spawn-runbook.md:7`) and no file shows `/sc:spawn` was actually invoked to make it (section 8, U1); (3) the recommended final chain (`top9-recommendation.md:47-64`) contains no `/sc:spawn` step: it uses `/sc:design`, `/sc:reflect`, `/sc:implement`, `/bmad-code-review`, `/sc:pr-submit`; (4) only the shape and the Prompt Construction Rules were reused (`spawn-runbook.md:53`).
- Conclusion: OPTIONAL at most, and only in R/HIGH. Every other cell is SKIP or N/A. A checker never expects it (section 6).

## 4. Choose this or the neighbour
Common fact for every row: nothing consumes `/sc:spawn` output. `grep -c "sc:spawn"` returns 0 in `task-builder/SKILL.md`, `task/SKILL.md`, `sc-workflow-protocol/SKILL.md` and `sc-implement-protocol/SKILL.md`; the only `~/.claude` files naming it are CMD and HW:282.

| Neighbour | Decision rule by complexity signal | Cited basis |
|---|---|---|
| `/task-builder` (+ `/task`) | Work changes code and the files can be named, or a spec exists, or it spans more than one session, or must not drift: `/task-builder`. It researches the code, gates quality, writes a checklist file `/task` runs, and traces `--spec` (`reflect_pre`). `/sc:spawn` does none of those: it emits a hierarchy and stops. Choose `/sc:spawn` over it only for a batch of independent items (R/HIGH), and then each item still gets its own `/task-builder` run | HW:18, HW:282, HW:243; CMD:192-208; `validation-feature-task-builder-vs-sc-workflow.md` line 11 |
| `/sc:workflow` (+ `/sc:implement`) | LOW to MEDIUM, a few files, clear scope, one or two sessions: `/sc:workflow --depth quick`. It writes an executable `TASK-WF-*` package that `/sc:implement` resumes; spawn writes no package, no progress file, no resume | HW:17, HW:305; workflow.md lines 7-12 |
| `/roadmap` | New product or major feature from a PRD/TDD: `/roadmap` gives phases plus task files. Spawn's Epic/Story/Task shape (CMD:36) duplicates the phase plan without the task files | HW:20, HW:74-77 |
| `bmad-create-epics-and-stories` (BMad lane) | In the BMad lane never use spawn; the epics step is REQUIRED there and produces the tracked artifact | `command-value-by-phase.md` section 2.2 row |
| `/sc:task`, `/sc:tasklist` (RETIRED, Ryan ruling 3) | Not a choice. Spawn does not call them; it only mentions `/sc:task` in an exclusion clause (CMD:124). Never recommend either as the step spawn delegates to | CMD:124, CMD:210 |

## 5. What a scheduled checker can see
**None defined: transcript only.** CMD names the output content (Epic decomposition, task hierarchy with dependencies, delegation assignments, coordination strategy; CMD:203-208) but no path, no frontmatter keys, no ledger, no progress or resume file. HW lists no output path for it (HW:282). TodoWrite is named for tracking (CMD:138); whether that persists to disk is UNVERIFIED.

| Possible trace | Where | Strength |
|---|---|---|
| A plan file whose header says `/sc:spawn` | `.dev/plans/top9-issues-20261001/spawn-runbook.md:5` | Weak: a label in a hand-placed file, not proof of invocation (section 8, U1). A checker could grep `.dev/plans/**` for the literal `/sc:spawn`, but a hit proves nothing about the command having run |
| Command line in the session | transcript or `~/.claude/history.jsonl` | Per machine only. On this machine 0 of 70 history lines mention `sc:spawn` |

Absence of any trace is expected and normal.

## 6. Expected-step rule
- **Never count `/sc:spawn` as an expected step, at any scope or complexity.** No file routes to it, no file consumes its output, and it leaves no footprint. Its absence is always fine, including T/B/S/F/R/N at LOW, MEDIUM and HIGH.
- **Its presence is allowed but earns nothing.** Do not flag its use (R/HIGH is OPTIONAL (J); elsewhere it is merely redundant). Do not count it as the tasklist step: it stops after decomposition (CMD:192-201) and writes no executable tasklist, so a feature (F) that went spawn, then implement with no `/task-builder` or `/sc:workflow` plan is still missing its tasklist step.

## 7. Proposed changes to command-value-by-phase.md
Proposals only; `command-value-by-phase.md` was not edited. Line numbers are that file's.

| # | Where | Current text | Proposed text |
|---|---|---|---|
| 1 | Section 2.2, line 115, `/sc:spawn` row, R column (R RE-RATING under "multi-feature release") | `SKIP` | `OPTIONAL (J)`. Changed because the old R reading ("a release assembles and ships work already built", line 139) made a planning tool irrelevant, while under Ryan's definition (full release plan) the batch-decomposition case (TOP9) belongs to R/HIGH. T, B, S, F, N stay `SKIP` |
| 2 | Same row, Notes | `Guide "Other commands": for work that changes code, prefer /task-builder` | `Guide "Other commands" only (HW:262, HW:282); not in any workflow or the routing table. Stops after a task hierarchy (CMD:192-208), writes no executable tasklist, no output path, no backing skill, and no other skill consumes its output, so it never satisfies the Tasklist step. Flags: --strategy sequential\|parallel\|adaptive, --depth normal\|deep (defaults and effect not stated). R/HIGH only (a batch of independent items with cross-item ordering): OPTIONAL (J), single precedent .dev/plans/top9-issues-20261001/spawn-runbook.md, invocation UNVERIFIED. Rule 2.5 mentions retired /sc:task (CMD:124)` |
| 3 | Section 3, line 232 (O6), Why cell | `... /sc:spawn is superseded by /task-builder` | `... /sc:spawn is superseded by /task-builder for code-changing work; for a batch of independent items it is OPTIONAL (J) at R/HIGH` |
| 4 | Section 4, line 259 "Skippable at every size" | `... /sc:spawn, ...` | No change needed (OPTIONAL is skippable). Optional wording: add "(OPTIONAL (J) only for R/HIGH batches)" |
| 5 | "What a checker could observe" table, after line 276 | no row | Add: `/sc:spawn` \| none defined; transcript only (no output path in CMD:203-208) \| sc-spawn.md section 5 |
| 6 | Section 1 inventory line 19 or section 5 unverified list | no mention that spawn has no backing skill | Add: "`/sc:spawn` has no backing protocol skill (`~/.claude/skills/sc-spawn-protocol/` missing); it runs from its command file" |
| 7 | Section 4 "Minimum viable path", Release row, WORTH IT additions | lists `/task-builder` / `/roadmap` for release steps | No change: spawn is not a minimum or WORTH IT item at any size |

## 8. Unverified items
| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | Whether `/sc:spawn` was actually invoked to produce `spawn-runbook.md` | The runbook header only says "`/sc:spawn` decomposition" (`spawn-runbook.md:5`) and "Nothing in this runbook has been executed" (line 7); `spawn-runbook-prompt.md` shows no invocation; `~/.claude/history.jsonl` on this machine has 0 matches | Ask the author, or search the originating session transcript |
| U2 | What `--strategy` and `--depth normal\|deep` change, and their defaults | CMD defines only the usage line (CMD:22) and one example (CMD:163-165); no protocol skill | Run it once (not allowed in this task), or add a flags section to CMD |
| U3 | Whether it ever executes tasks, given the contradiction between CMD:30-31, CMD:182 and CMD:192-201 | Not run; I treat the closing "STOP AFTER TASK DECOMPOSITION" as binding (JUDGMENT) | Run it once |
| U4 | Whether TodoWrite entries (CMD:138) persist to disk | No file says | Run it once and check |
| U5 | The path cited in CMD:76 (`.dev/releases/current/test_obligation_scanner_meta_context-fixes/PHASE0-MITIGATION-DEBATE.md`) | Belongs to another repository (IronClaude); not checked | Open it in that repo |
| U6 | Whether other engineers' `~/.claude/commands/sc/spawn.md` matches this copy (mtime Oct 22 here) or has a backing skill | Home-directory file, not shared; history count covers this machine only | Compare across engineers |
| U7 | Why Rule 2.5 and the troubleshoot/adversarial pipeline wording remain in a command that has no troubleshoot step | Only an inference (JUDGMENT): leftover from an earlier IronClaude-internal use | Check IronClaude git history |

Total unverified items: 7.
