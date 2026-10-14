# Research: Planning and Execution Depth Ladder (IronClaude + IC-Harness)
**Scope:** IronClaude src/superclaude/skills (task-builder, task, tech-research, prd, tdd, tech-reference, sc-roadmap-protocol, sc-tasklist-protocol, sc-validate-roadmap-protocol, sc-task-protocol), src/superclaude/commands (workflow, implement, spec-panel, brainstorm, design), src/superclaude/cli (sprint, roadmap), docs/sprint-cli-deep-dive.md; IC-Harness .claude/skills (task-builder, task, roadmap), .claude/templates/workflow 01/02
**Status:** Complete
**Date:** 2026-10-01
**Authority:** IronClaude master = `/Users/cmerritt/GFxAI/IronClaude-tier-tools` (HEAD `50a8c7f4`, 2026-09-30). Sections A-E were first read from the June branch (`/Users/cmerritt/GFxAI/IronClaude`, `58bdef20`, 2026-06-08) and are kept for the June-vs-master comparison; Section G records every master difference and the installed state; PART 2 is the master-authoritative synthesis.

**Summary:** Three independent task-builder dials (research tier, template 01/02, QA intensity + gate placement). The genuinely "simple task file" in master is NOT MDTM Template 01: it is the new Template 00 `plan.md` written by `/sc:workflow` and executed by `/sc:implement` with one reviewer per task and a resumable ledger, and it is not present in IC-Harness. Template 01 via task-builder is lighter than 02 but still keeps research, validation, reflect, and `/task` 6-agent phase gates. Nothing IronClaude is installed user-wide, and the pipx CLI (4.2.0, March snapshot) lacks `reflect`, `prd`, and newer sprint/roadmap flags.
**Purpose:** Feed a human quick-reference guide on WHEN to use which planning/execution depth.
---

Path shorthand used below: `IC/` = `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/`; `ICH/` = `/Users/cmerritt/GFxAI/IC-Harness/.claude/`.

## A. Source findings: IronClaude task-builder (the three independent dials)

The single most important finding for a user: the IronClaude task-builder has THREE separate depth dials, not one. Users conflate them.

| Dial | Values | What it controls | Who sets it | Evidence |
|---|---|---|---|---|
| Research tier | Quick / Standard / Deep | How many researcher agents (3 / 4-5 / 6-8) and web agents (0 / 0-1 / 1-2) run BEFORE the task file is written | Orchestrator, from scope size and user words | `IC/skills/task-builder/SKILL.md:127-143` [CODE-VERIFIED] |
| Template | 01 Generic / 02 Complex | Shape of the generated task file (02 adds Section L handoff patterns: discovery, build-from-discovery, test, review, conditional, aggregation) | Orchestrator triage at A.6; BUILD_REQUEST `TEMPLATE:` field | `IC/skills/task-builder/SKILL.md:475-493`, `:992-994`; `IC/templates/workflow/02_mdtm_template_complex_task.md:77-80, 902-1002` [CODE-VERIFIED] |
| QA intensity + gate placement | `QA_INTENSITY`: lite / standard / full; `QA_GATE_REQUIREMENTS`: NONE / FINAL_ONLY / PER_PHASE | How many QA agents each gate in the generated task file spawns, and where the gates go | BUILD_REQUEST fields; "calling skill's tier mapping or user override" | `IC/skills/task-builder/SKILL.md:996-1050`; `IC/templates/workflow/01_mdtm_template_generic_task.md:776-823` (I22) [CODE-VERIFIED] |

### A.1 Tier table (verbatim facts)

- Quick: "Small scope, <5 relevant files, single concern", 3 researchers, 0 web agents (`SKILL.md:133`).
- Standard: "Most requests, 5-20 files", 4-5 researchers, 0-1 web (`:134`). This is the DEFAULT: "Default to Standard unless the scope is clearly small (<5 files) or clearly large" (`:129`).
- Deep: "20+ files, multiple subsystems, multi-track", 6-8 researchers, 1-2 web (`:135`).
- Trigger words: "thorough", "comprehensive", "deep dive" force Deep (`:140`). Multi-track defaults to Deep (`:143`). "Only use Quick for genuinely small tasks (<5 files, single concern, no discovery needed)" (`:141`).
- There is NO `--tier` or `--quick` flag in the task-builder Input section (`:29-41`); the only flag documented is `--spec <path>` (`:41`). Tier is chosen from wording and scope. [CODE-VERIFIED by reading Input section; grep for `--tier` returned nothing]

### A.2 Template triage (verbatim facts)

- Template 02 when work involves discovery, parallel subagents, multiple phases with different activities, conditional flows, or "Quality gates or verification steps" (`SKILL.md:479-485`).
- Template 01 when "Simple, sequential file creation", "Straightforward execution with no discovery", "Single-pass operations with known inputs and outputs" (`:487-491`).
- "For most task-builder requests, the answer is Template 02 ... Only use Template 01 for trivial tasks with known inputs and outputs." (`:493`).
- Builder loads the matching file: `02 -> .claude/templates/workflow/02_mdtm_template_complex_task.md`, `01 -> .../01_mdtm_template_generic_task.md` (`:1222-1223`).
- Note: tier and template are decided separately (A.6 is its own step, `:199`); Quick tier does NOT automatically mean Template 01. [CODE-VERIFIED: no coupling rule exists in the tier section `:127-143` or A.6 `:475-493`]

### A.3 QA dials (verbatim facts)

- `QA_GATE_REQUIREMENTS` default: "FINAL_ONLY for Template 01, PER_PHASE for Template 02. NONE = no QA gates in generated task file. FINAL_ONLY = include a final QA validation phase before task completion. PER_PHASE = include QA gates after each major phase." (`SKILL.md:997-1000`).
- `QA_INTENSITY` "determined by calling skill's tier mapping or user override" (`:996`). The rf-task-builder agent: "If QA_INTENSITY is absent, default to full" (`IC/agents/rf-task-builder.md:362`).
- I22 default mapping: Quick/Lightweight -> lite, Standard -> standard, Deep/Heavyweight -> full (`IC/templates/workflow/01_mdtm_template_generic_task.md:789-792`).
- I22 user-override phrasing: "quick with full QA" -> Quick research + full QA; "deep but lite QA" -> Deep research + lite QA (`01_...:794-797`). lite is also triggered when "user says 'quick' or 'light'"; full when "user says 'thorough'" (`01_...:785-787`).
- I22 agent counts per gate (`01_...:783-787`):

| Level | Intermediate gate | Final gate (M3) | Fidelity gate (M4) | Fix cycles | Verifiers |
|---|---|---|---|---|---|
| lite | 2 (1 rf-qa + 1 rf-qa-qualitative) | 3 (1 structural + 1 content + 1 domain) | 1 combined | 1 max, then Open Questions | 1 |
| standard | 3 (analyst + qa + qualitative) | 7 (3 + 3 + 1 domain) | 2 | 2 max | 2 |
| full | per I19 (5+ intermediate, 6-12+ final) | per I19 + all domain lenses | per I21 (2-8) | per I16 (2-3) | 2 |

- Never bypassed: "Serialized fix protocol (I20) applies at ALL intensity levels ... never bypassed." (`01_...:821-823`). Fidelity gate "runs at ALL intensity levels" (`IC/templates/workflow/02_mdtm_template_complex_task.md:1102`).
- "Double QA: DISABLED" at lite and standard: "only the skill-specific QA runs" (`01_...:806, 815`). See Open Questions: IronClaude `/task` does not read qa_intensity.

### A.4 Gates the task-builder itself always runs (build-time, not in the generated file)

- Research gate: "2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative ... (5 agents minimum)" with gap-fill up to 3 rounds (`SKILL.md:201`); intensity-scaled to 2/3/5 at lite/standard/full (`:687-689`).
- Task-file structural (2 rf-qa, A.10), research-alignment (1 rf-analyst, A.10.25), qualitative (2 rf-qa-qualitative, A.10.5) (`:204-206`).
- PRE reflect gate A.10.7 (`:1650-1687`): runs `/sc:reflect --mode pre --remediate [--spec <path>] --tasklist <TASK_FILE> --depth <pre_depth> --output ${TASK_DIR}reflect/pre/` (`:1658-1664`). Advisory-blocking: pass needs `coverage_pct >= 0.90` (`:1670`); fail appends unmapped requirements to Open Questions, "The build still completes; the tasklist is flagged not-signed-off" (`:1671`); no spec -> `verdict: skipped` (`:1654, 1672`); "max 0 auto-loops" (`:1687`). Depth `quick` permitted at PRE (`:1654`).
- POST reflect gate is always baked into the generated file: `POST_REFLECT_GATE: ENABLED`, `DEPTH: <max(tcs-derived depth, standard)> # POST floor per O4, never quick` (`:1073-1076`); must be the penultimate self-run item or the file is MALFORMED (`:2312`).
- Skill-delegated short path: `Source: skill-delegated` + `SKIP_RESEARCHERS: true` (default for delegated) skips A.2-A.8.5 and goes straight to the builder (`:47-58, 219-221`). Users can also set `SKIP_RESEARCHERS: false` (`:56, 223-225`).
- Direct user invocation stops after building: "the user reviews the task file and executes it with `/task [path]` when ready" (`:12, 190`).

## B. Source findings: IronClaude /task executor

- Input: a task file path, or weak phrasing ("continue the task") which searches `.dev/tasks/to-do/` for status "Doing", then "To Do" (`IC/skills/task/SKILL.md:31-56`).
- Executes the F1 loop: first unchecked `- [ ]`, execute, mark `- [x]`, repeat (`:10`, `:85`).
- Resume: re-read file, find first unchecked item, never re-execute `- [x]` (`:282-296`); mid-batch failure respawns only unchecked items (`:151`). Resume command: `/task .dev/tasks/to-do/TASK-[ID]/TASK-[ID].md` (`:399`).
- Executor-added QA, independent of what the task file encodes:
  - Phase-gate rf-qa after every Phase 2+, `fix_authorization: true`, max 3 fix cycles then HALT for user (`:192-214`). "No exceptions: QA gates are not optional. Every task file processed by this skill gets phase-gate verification on Phase 2+." (`:222`).
  - Post-completion: rf-qa structural (`report-validation`) then rf-qa-qualitative (`task-qualitative`) before Done (`:224-262`).
- Prohibitions include "Skipping phase-gate QA" and "Delegating across phase boundaries" (`:121-123`).
- Consequence for users: even a "simple" Template 01 task file with lite QA still gets executor phase gates on Phase 2+ and the two post-completion validators. The lightest achievable /task run is a task file with ONE execution phase after setup (only post-completion validation then applies). [CODE-VERIFIED from `:194, 222, 228`; inference about single-phase files is derived, not stated]

## C. Source findings: interactive /sc: commands (no task file)

### C.1 /sc:task (compliance tiers, NOT the same as /task)

- Syntax: `/sc:task [operation] --strategy [systematic|agile|enterprise] --compliance [strict|standard|light|exempt]` (`IC/commands/task.md:19`). Other flags: `--verify`, `--skip-compliance`, `--force-strict`, `--parallel`, `--delegate`, `--no-escalation` (`:44`).
- Classification header is the mandatory first output; tiers checked in priority order STRICT > EXEMPT > LIGHT > STANDARD (`:50-93`). Security words always win: "'quick security' -> still STRICT" (`:77`). Confidence <0.70 asks the user to override (`:93`).
- Execution: EXEMPT and LIGHT execute directly with no Skill call; STANDARD/STRICT invoke `Skill sc:task-protocol` (`:97-102`).
- Verification cost table: STRICT = quality-engineer sub-agent, 3-5K tokens; STANDARD = direct test run, 300-500 tokens; LIGHT/EXEMPT = skip (`IC/skills/sc-task-protocol/SKILL.md:122-127`). Critical paths (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) force CRITICAL verification regardless of tier (`:129`).
- STRICT steps include serena activation, clean git check, quality-engineer spawn, `pytest -v`, adversarial questions (`:84-96`). STANDARD: context load, downstream impact search, change, run affected tests (`:98-104`).
- TFEP: test-failure escalation to `/sc:forensic --tier light` then `--tier standard` (`:206-212, 258-259`); `--no-escalation` disables it with a warning (`IC/commands/task.md:48`).
- Max 15 changes per batch (`IC/commands/task.md:184`). No on-disk checklist, no resume. [CODE-VERIFIED: no task-file artifacts described in `commands/task.md` or `sc-task-protocol/SKILL.md`]

### C.2 /sc:implement, /sc:design, /sc:workflow

| Command | Syntax | Produces | Documented next step | Evidence |
|---|---|---|---|---|
| `/sc:implement` | `/sc:implement [feature-description] [--type component\|api\|service\|feature] [--framework react\|vue\|express] [--safe] [--with-tests]` | Code edits in-session; uses TodoWrite for tracking | "use `/sc:test` to run tests, then `/sc:git` to commit" | `IC/commands/implement.md:24, 57, 127` |
| `/sc:design` | `/sc:design [target] [--type architecture\|api\|component\|database] [--format diagram\|spec\|code]` | Design docs/specs; will NOT write implementation code | "After design is approved, use `/sc:implement`" | `IC/commands/design.md:22, 98, 109` |
| `/sc:workflow` | `/sc:workflow [prd-file\|feature-description] [--strategy systematic\|agile\|enterprise] [--depth shallow\|normal\|deep] [--parallel]` | "IMPLEMENTATION PLAN ONLY - no code execution" | "use `/sc:implement` to execute the plan step by step" | `IC/commands/workflow.md:21, 112-116, 133` |

None of these three produce an MDTM task file, a resumable checklist, or rf-qa gates. [CODE-VERIFIED by reading each command body; none references task-builder or rf-qa]

### C.3 /sc:brainstorm and /sc:spec-panel (upstream requirement shaping)

- `/sc:brainstorm "<topic>" [--proposals N] [--depth quick|standard|deep] ... [--handoff none|design|tasklist|task] ...` (`IC/commands/brainstorm.md:35-40`). `--depth quick` caps proposals at 2 "(cost guardrail)"; `--strategy enterprise` implies deep (`:67-70`). Produces `merged-requirements.md`, `seed-brief.md`, `adversarial/`, `enrichment/` under `.dev/brainstorms/<ts>-<slug>/` (`:61, 189-195`). `--handoff task` invokes the task-builder skill; `--handoff tasklist` invokes sc-tasklist-protocol; `--handoff design` prints a recommendation only (`:71, 173-175`). Documented next steps: `/sc:design`, `/sc:tasklist`, `/sc:implement` (`:197-201`).
- `/sc:spec-panel [spec|@file] [--mode discussion|critique|socratic] [--experts ...] [--focus requirements,architecture,testing,compliance,correctness] [--iterations N] [--format standard|structured|detailed]` (`IC/commands/spec-panel.md:22-25`). Reviews; does not create specs from raw instructions (`:274`). With a TDD or PRD input and `--downstream roadmap`, emits a scoped release spec in `release-spec-template.md` format with roadmap frontmatter (`:36, 272, 280`). Next step: "/sc:design for architecture or /sc:implement for coding" (`:462`).
- `spec-panel.md:416-417` references `/sc:code-to-spec`, which does not exist in `IC/commands/` (0 matches). [CODE-CONTRADICTED: stale cross-reference]

## D. Source findings: IronClaude document skills (Stage A build, Stage B execute)

| Skill | Tier names and default | Tier sizes (agents / output lines) | How Stage A builds the task file | How Stage B executes | Evidence |
|---|---|---|---|---|---|
| `/tech-research` | Quick / Standard / Deep; "Default to Deep"; "If in doubt, pick Deep" | Quick 1-2 codebase + 0-1 web; Standard 3-5 + 1-2; Deep 5-10+ + 2-4 | Spawns `rf-task-builder` agent directly (`subagent_type: "rf-task-builder"`) | Runs the F1 loop INLINE in the skill (its own Stage B), not via `/task` | `IC/skills/tech-research/SKILL.md:92-108, 326, 458, 476-500` |
| `/prd` | Lightweight / Standard / Heavyweight; vague requests default Heavyweight | 2-3 / 4-6 / 6-10+ agents; 400-800 / 800-1500 / 1500-2500 lines | Spawns `rf-task-builder` agent directly | `Skill task` with the task file path | `IC/skills/prd/SKILL.md:79-94, 252, 395, 420` |
| `/tdd` | Lightweight / Standard / Heavyweight; default Standard | 2-3 / 4-6 / 6-10+; 300-600 / 800-1400 / 1400-2200 lines | Spawns `rf-task-builder` agent directly | `Skill task` | `IC/skills/tdd/SKILL.md:65-80, 224, 369, 394` |
| `/tech-reference` | Lightweight / Standard / Heavyweight; default Standard, may upgrade, never downgrade without approval | 2-3 / 4-6 / 6-10+; 400-600 / 800-1200 / 1200-1800 lines | Spawns `rf-task-builder` agent directly | `Skill task` | `IC/skills/tech-reference/SKILL.md:82-97, 502, 531, 1257` |

- All four resume by skipping Stage A when a task file with unchecked items exists (`tech-research:156, 168`; `prd:168, 180`; `tdd:149, 161`; `tech-reference:165, 177`).
- `/tdd` accepts a PRD as input: "The PRD feeds the TDD the same way tech-research feeds a tech-reference" (`IC/skills/tdd/SKILL.md:44`). This is the code-documented prd -> tdd link.
- None of the four skills sets `QA_INTENSITY` in IronClaude (grep for `QA_INTENSITY|qa_intensity` across `IC/skills/{prd,tdd,tech-reference,tech-research}/` and their `refs/` returned 0 hits), so the rf-task-builder default "If QA_INTENSITY is absent, default to full" (`IC/agents/rf-task-builder.md:362`) applies. A Lightweight PRD still gets full-intensity gates unless the user asks. [CODE-VERIFIED by grep; behavioral consequence is inference]
- [CODE-CONTRADICTED] task-builder claims these skills call it via `Skill(skill: "task-builder", args: "<BUILD-REQUEST-file-path>")` with `Source: skill-delegated` (`IC/skills/task-builder/SKILL.md:45, 123`). In the IronClaude skill bodies they spawn the `rf-task-builder` AGENT instead (lines above), so the task-builder skill's build-time gates (A.8 research gate, A.10/A.10.25/A.10.5, A.10.7 PRE reflect) are not invoked from these skills. Each skill runs its own Stage A verification instead (e.g. "If the task file is malformed ... re-run the builder", `prd:410`, `tdd:384`, `tech-reference:521`, `tech-research:472`).

## E. Source findings: roadmap -> tasklist -> sprint (release pipeline)

### E.1 Commands and CLI

| Step | Invocation | Produces | Evidence |
|---|---|---|---|
| Roadmap (slash) | `/sc:roadmap [OPTIONS] INPUT_FILES...` (1-3 of spec, TDD, PRD) | Roadmap pipeline artifacts in `--output` or the first input's parent dir | `IC/commands/roadmap.md:13-20, 77-79` |
| Roadmap (CLI) | `superclaude roadmap run [OPTIONS] INPUT_FILES...`; also `roadmap validate`, `roadmap accept-spec-change` | Same artifacts; deterministic 14-step pipeline | `IC/cli/roadmap/commands.py:14-60, 404, 430`; `IC/skills/sc-roadmap-protocol/SKILL.md:109-111` |
| Roadmap depth | `--depth quick\|standard\|deep` = debate rounds 1/2/3, default standard | n/a | `IC/commands/roadmap.md:28`; `IC/cli/roadmap/commands.py:50-55` |
| Roadmap resume | `--resume` "Skip steps whose outputs already pass their gates" | n/a | `IC/commands/roadmap.md:29, 67` |
| Validate roadmap | `/sc:validate-roadmap <OUTPUT_DIR> [--agents ...]`; single agent default, N>=2 adds adversarial merge; always exits 0 | `<OUTPUT_DIR>/validate/validation-report.md` | `IC/commands/validate-roadmap.md:11-45` |
| Validate verdict | 0 CRITICAL + 0 HIGH + weighted >= 95% = "GO -- ready for tasklist generation" | GO/NO-GO | `IC/skills/sc-validate-roadmap-protocol/SKILL.md:688` |
| Tasklist | `/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]` | `tasklist-index.md` + `phase-N-tasklist.md`, every task tier-classified STRICT/STANDARD/LIGHT/EXEMPT; validates and patches drift | `IC/commands/tasklist.md:22-35`; `IC/skills/sc-tasklist-protocol/SKILL.md:14-16, 40-41, 80-81` |
| Tasklist CLI | `superclaude tasklist validate <output_dir>` is VALIDATION ONLY; generation is the slash-command skill | Fidelity report | `IC/cli/tasklist/commands.py:15-40`; `IC/skills/sc-tasklist-protocol/SKILL.md:132` |
| Sprint | `superclaude sprint run path/to/tasklist-index.md [--start N --end M] [--dry-run] [--resume <task-id>] [--task-parallelism N] [--fresh]`; plus `attach`, `status`, `logs`, `kill`, `verify-checkpoints`, `rerun-tasks` | Each phase executed as a fresh Claude Code session | `IC/cli/sprint/commands.py:16-33, 72-232, 580-745` |

- Sprint runs each phase as `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` (`IC/cli/sprint/process.py:219-220`). So the sprint lane executes through /sc:task STRICT, not through `/task`.
- Sprint blocks when `.roadmap-state.json` has `fidelity_status: fail`; override with `--force-fidelity-fail '<justification>'` (`IC/cli/sprint/commands.py:36-69, 159-175`).
- Phase execution modes `claude` (default), `python`, `skip` via the index's Execution Mode column (`docs/sprint-cli-deep-dive.md:173-183, 353-363`). [doc claim; config.py location cited in doc, not re-read]
- `/sc:tasklist` will NOT run `superclaude sprint run` (separate step) (`IC/commands/tasklist.md:118`). `/sc:roadmap` will NOT generate tasklists or trigger downstream commands automatically (`IC/commands/roadmap.md:98`).
- `superclaude prd run "<request>" --tier lightweight|standard|heavyweight` is a separate 15-step PRD CLI pipeline with `prd resume` (`IC/cli/prd/commands.py:1-28`).

### E.2 Staleness in this lane

- `docs/sprint-cli-deep-dive.md:62-70` says `sprint_group` "defines 5 subcommands" and `run` has "16 CLI options". Code has 7 subcommands (adds `verify-checkpoints`, `rerun-tasks`, `commands.py:647, 705`) and 23 option names on `run` (`commands.py:72-232`). [CODE-CONTRADICTED: doc is stale]
- `docs/sprint-cli-deep-dive.md:49` cites `main.py:356`; registration is at `IC/cli/main.py:402`. [CODE-CONTRADICTED: line drift]
- `IC/skills/sc-roadmap-protocol/SKILL.md:36` still says "future tasklist command -> sc:task"; `/sc:tasklist` now exists and targets `superclaude sprint run`. [CODE-CONTRADICTED]

## F. Source findings: IC-Harness live versions (comparison)

| Area | IronClaude | IC-Harness | Evidence |
|---|---|---|---|
| task-builder tier table | Quick/Standard/Deep, same numbers | Identical text (diffed) | `IC/skills/task-builder/SKILL.md:124-143` vs `ICH/skills/task-builder/SKILL.md:127-146` |
| Template triage (A.6) | Same | Identical text (diffed) | `IC/...:475-493` vs `ICH/...:479-497` |
| `QA_INTENSITY` / `QA_GATE_REQUIREMENTS` fields | Present | Present, same defaults | `IC/...:996-1000` vs `ICH/...:1000-1004` |
| Extra task-builder flag | only `--spec` | `--spec` plus `--cli` (POST reflect becomes `superclaude reflect run ... --depth deep --fix --promote` shell-out; default OFF; frontmatter `reflect_post_mode: cli\|skill`) | `ICH/skills/task-builder/SKILL.md:41, 43, 286, 2371` |
| PRE reflect gate wording | "advisory-blocking"; `skipped` when no spec | Same mechanism, but explicitly MANDATORY to run to completion when a spec resolves; skipping for cost/runtime is a "PROTOCOL VIOLATION"; `tcs` must be a real computed integer | `IC/...:1652-1654` vs `ICH/...:1664-1666` |
| POST reflect item form | Executor "spawn a subagent that runs `/sc:reflect --mode post`" | Dedicated-subagent runner with a verbatim runner prompt and hard completion contract (skill mode), or wrapper shell-out (cli mode) | `IC/...:2312` vs `ICH/...:2223, 2371` |
| Template 01 | Byte-identical file | Byte-identical (cmp) | `IC/templates/workflow/01_mdtm_template_generic_task.md`, `ICH/templates/workflow/01_mdtm_template_generic_task.md` |
| Template 02 | G1 and `:624`, `:1302` point at `.gfdoc/rules/core/...` (no `.gfdoc` dir exists in IronClaude) | Points at `.claude/rules/core/...` | diff at lines 474, 624, 1302 [CODE-VERIFIED; `ls IronClaude/.gfdoc` = not found] |
| Extra Template 01 variant | none | `01_mdtm_template_generic_task__gfdoc.md` (900 lines, 0 `I22` mentions); not referenced by task-builder or rf-task-builder | `ICH/templates/workflow/`; grep `__gfdoc` in `ICH/skills/task-builder/SKILL.md`, `ICH/agents/rf-task-builder.md` = 0 hits |
| /task phase-gate QA | ONE rf-qa per Phase 2+ with `fix_authorization: true`, max 3 fix cycles | Lens-based: minimum 6 agents (3 rf-qa + 3 rf-qa-qualitative, scaling 6/8/10/12 by output size), report-only, consolidate, single fix agent, 2-agent verification; "Gates that spawn fewer than 6 agents are a protocol violation" | `IC/skills/task/SKILL.md:192-222` vs `ICH/skills/task/SKILL.md:186-275` |
| Doc skills -> builder | prd/tdd/tech-reference/tech-research spawn the `rf-task-builder` AGENT; tech-research executes inline | All four call `Skill(skill: "task-builder", args: "${TASK_DIR}BUILD-REQUEST.md")` then `Skill task` | IC lines in section D vs `ICH/skills/prd/SKILL.md:642, 657`, `tdd:616, 631`, `tech-reference:563, 578`, `tech-research:594, 609` |
| Doc skills tier -> QA intensity mapping | Not present (defaults to full) | Present: Quick/Lightweight -> lite, Standard -> standard, Deep/Heavyweight -> full, override allowed | `ICH/skills/prd/SKILL.md:94-100`, `tdd:97-103`, `tech-reference:97-103`, `tech-research:111-117` |
| RF roadmap skill | Does not exist (only `sc-roadmap-protocol` + CLI) | `/roadmap` exists: Quick = roadmap doc only; Standard = roadmap + BUILD_REQUESTs; Deep = roadmap + BUILD_REQUESTs + one task file per phase via `/task-builder`; default Deep; Quick->lite, Standard->standard, Deep->full; "quick", "fast", "light QA", "basic" -> lite | `ICH/skills/roadmap/SKILL.md:8-12, 100-126`; `ls IC/skills` has no `roadmap` |
| `/roadmap` QA load | n/a | 44-48 evaluating agents minimum at full for 6 phases | `ICH/skills/roadmap/SKILL.md:27, 430` |
| `/roadmap` dry run | n/a | `--dry-run`, "dry run", or "plan only" -> phase plan summary only | `ICH/skills/roadmap/SKILL.md:247` |
| sc commands | `IC/commands/*.md` | Same set mirrored under `ICH/commands/sc/` (plus `cli-eval`, `pr-submit`, `swarm-wizard`) | `ls ICH/commands/sc` |

## G. CORRECTION: IronClaude master is authoritative (coordinator correction, 2026-10-01)

Sections A-E above were read from `/Users/cmerritt/GFxAI/IronClaude` = branch `feature/task-builder-merge`, last commit `58bdef20` 2026-06-08 (the "June branch"). The current master copy is `/Users/cmerritt/GFxAI/IronClaude-tier-tools`, branch `feat/tier-tools-update`, HEAD `50a8c7f4` 2026-09-30 "Merge pull request #250 from IronbellyOrg/Workflow_v3". Path shorthand: `MS/` = `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/`. Everything below supersedes A-E where they conflict.

### G.1 File-level comparison (cmp + wc -l)

| File | June -> master | Notes |
|---|---|---|
| `skills/task-builder/SKILL.md` | DIFF 2517 -> 2604 | Tier table, template triage, QA fields unchanged in substance; adds `--cli` flag (`MS/skills/task-builder/SKILL.md:43`) like IC-Harness |
| `skills/task/SKILL.md` | DIFF 402 -> 639 | Now lens-based 6-agent phase gates like IC-Harness (`MS/skills/task/SKILL.md:194, 282`) |
| `templates/workflow/01_...generic_task.md` | SAME | I22 lite/standard/full unchanged |
| `templates/workflow/00_mdtm_template_simple_task.md` | NEW in master (47 lines) | THE simple plan template, see G.2 |
| `commands/workflow.md` | DIFF 133 -> 82 | Rewritten: now drives `sc:workflow-protocol` and writes `plan.md` from Template 00 |
| `commands/implement.md` | DIFF 127 -> 139 | Rewritten: "Middleweight spec executor" via `sc:implement-protocol` |
| `skills/sc-workflow-protocol/`, `skills/sc-implement-protocol/` | NEW in master | Absent in June and in IC-Harness |
| `skills/roadmap/SKILL.md` (RF `/roadmap`) | ABSENT in June -> present in master | Byte-identical to IC-Harness (cmp) |
| `skills/tech-research`, `tech-reference` | DIFF | Now call `Skill(skill: "task-builder", ...)` then `Skill task` (`MS/skills/tech-research/SKILL.md:594, 609`; `MS/skills/tech-reference/SKILL.md:564, 579`) and carry the tier -> QA intensity mapping (`tech-research:111`, `tech-reference:97`) |
| `skills/prd`, `skills/tdd` | prd SAME, tdd DIFF | STILL spawn the `rf-task-builder` agent directly (`MS/skills/prd/SKILL.md:395`, `MS/skills/tdd/SKILL.md:386`) and have no QA intensity mapping. So in master, prd/tdd bypass task-builder's build-time gates; tech-research/tech-reference do not. [CODE-VERIFIED] |
| `commands/task.md`, `sc-task-protocol` | DIFF (minor) | Tiers and flags unchanged; TFEP escalation now goes to `/sc:troubleshoot` with `--depth standard` then `--depth deep`, 3rd trigger FULL STOP (`MS/skills/sc-task-protocol/SKILL.md:139, 212-215`) instead of `/sc:forensic` |
| `commands/tasklist.md` | DIFF (mcp list only) | Same syntax incl. `--no-reflect` |
| `commands/roadmap.md`, `cli/roadmap/commands.py`, `cli/tasklist/commands.py`, `commands/design.md` | SAME | |
| `cli/sprint/commands.py` | DIFF 941 -> 993 | Adds `--max-session-resets`, `--ignore-run-lock`, `--reevaluate-stale`; still 7 subcommands (`MS/cli/sprint/commands.py:72, 617, 629, 641, 666, 684, 757`) |
| `cli/sprint/process.py` | DIFF | Still `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` (`MS/cli/sprint/process.py:220-221`), plus a Bash inspection policy block |
| `cli/main.py` | DIFF | Registers `reflect` CLI (`MS/cli/main.py:495`) and `swarm` (`:483`) in addition to sprint/roadmap/tasklist/prd/eval |
| `commands/` set | DIFF | master drops `estimate.md`, `select-tool.md`, `sc.md`; adds `post-release.md`, `cli-eval.md`, `pr-submit.md`, `swarm-wizard.md` |

### G.2 The "simple task file" in master: Template 00 + /sc:workflow + /sc:implement

This is a NEW middleweight lane that did not exist in the June branch, and it answers "the simpler task file" directly.

- Template: `MS/templates/workflow/00_mdtm_template_simple_task.md` (47 lines). Frontmatter only `version`, `priority`, `created_date` (`:1-5`). Body: `# title`, `Source:`, `Goal:`, optional `## Constraints`, `## Phase N:` group headings, `## Task N:` items each with `Acceptance criteria:` bullets and optional `Depends on: Task K` (`:25-47`). Its own rules: "Use plain bullets, not checkboxes or numbered steps: /sc:implement treats those as separate tasks" and "This is not an MDTM /task checklist; /sc:implement handles per-task review and the progress ledger." (`:10, 20`). Added in commits `5619aef1` and `bb4f0212` (both 2026-09-30).
- Only consumer: `sc-workflow-protocol` (grep for `00_mdtm_template_simple_task` in `MS/` hits only `skills/sc-workflow-protocol/SKILL.md` and its `refs/quality-gates.md`). task-builder does NOT know about Template 00 (0 hits in `MS/skills/task-builder/SKILL.md`).
- How to ask for it: `/sc:workflow <path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--output DIR] [--handoff none|design|implement|tasklist]` (`MS/commands/workflow.md:26-32`). Output `.dev/workflow/<slug>/plan.md` + `return-contract.yaml` (`:41, 67`). Banned legacy flags `--parallel`, `--validate`, `--depth shallow|normal` (`:44`). Next step: "`/sc:implement @plan.md`" (`:82`), or `--handoff implement` to invoke `Skill sc:implement-protocol` automatically (`MS/skills/sc-workflow-protocol/refs/overlap-routing.md:5`).
- Workflow depth: quick 2-4 phases, standard 4-8, deep 6-12 (`MS/skills/sc-workflow-protocol/SKILL.md:38`). Gate: quick = "schema-min", standard/deep = "full"; fail -> STOP `E-GATE` (`:48-52`; `refs/quality-gates.md:18-34`). No subagents: "Will Not: ... Task fan-out" (`SKILL.md:64`).
- Executor: `/sc:implement <path>|<prompt> [--resume] [--ledger <path>] [--skip-final-review]` (`MS/commands/implement.md:38-47`). Aliases `--spec/--prd/--tasklist`. Removed flags `--type/--framework/--safe/--with-tests` now STOP `E-LEGACY` (`MS/skills/sc-implement-protocol/SKILL.md:30, 38`). Ledger `.dev/implement/<slug>/progress.md`; resume from first non-complete task (`MS/commands/implement.md:57-58`).
- QA it KEEPS: per task, ONE reviewer (inline when N<=3 tasks and source <=400 lines and not compacted, else one Task subagent) checks the git diff against that task's acceptance criteria with mandatory `path:line` citations; closed verdict `compliant|missing|extra|misunderstood|cannot-verify`; exactly one fix pass then HALT `E-HALT-QA` unless the operator writes a `Ruling:` line (`MS/skills/sc-implement-protocol/SKILL.md:89-121`; `refs/qa.md:11, 35-69, 77-81`). Optional advisory whole-list review when N>1 (`SKILL.md:142-144`). Lint/typecheck/tests run as recorded extras, "never the gate" (`SKILL.md:126-140`).
- QA it DROPS: "Will Not: Invoke `/task` or `/sc:task`; Import MDTM F1, 6-agent phase gates, or `/sc:reflect` as the per-task gate; Auto-commit" (`MS/commands/implement.md:120-127`). No PRE/POST reflect, no rf-qa lens panels, no research gate, no task-builder build-time validation. "Never 2+ reviewer agents per task" (`refs/qa.md:11`).

### G.3 Installed state for this user (what actually runs)

- `/Users/cmerritt/.claude/skills/` contains ONLY `ccsession-tag`, `computer-use`, `orca-cli`, `orchestration`, `skill-creator` (ls). None of task-builder, task, roadmap, tech-research, prd, tdd, sc-*-protocol are installed user-wide.
- `/Users/cmerritt/.claude/commands/sc` does NOT exist; `/Users/cmerritt/.claude/commands/` is empty (ls). So no `/sc:*` command is installed user-wide.
- Consequence: the RF and `/sc:` surfaces resolve per PROJECT from that repo's `.claude/`. In IC-Harness the live copies are `ICH/skills/*` and `ICH/commands/sc/*`. IC-Harness `commands/sc/workflow.md`, `implement.md`, `tasklist.md`, `spec-panel.md`, `validate-roadmap.md` are byte-identical to the JUNE branch, not master (cmp); `task.md` and `brainstorm.md` match neither; `roadmap.md` and `design.md` match both. IC-Harness has no `sc-workflow-protocol` or `sc-implement-protocol` skill and no Template 00 (ls `ICH/skills`, `ICH/templates/workflow`). So in IC-Harness today `/sc:workflow` and `/sc:implement` are the OLD June behavior (plan in prose, no ledger, no per-task QA). [CODE-VERIFIED by cmp]
- Installed CLI: `superclaude` 4.2.0 from pipx, `direct_url.json` = `file:///Users/cmerritt/GFxAI/IronClaude`, NON-editable copy, files dated 2026-03-24. `superclaude --help` lists only `cleanup-audit, cli-portify, doctor, install, install-skill, mcp, roadmap, sprint, tasklist, update, version`. There is NO `reflect`, `prd`, `eval`, `swarm`, `recommend`, `init-lite` subcommand; `superclaude reflect --help` fails. Installed `sprint` has 5 subcommands (`run, attach, status, logs, kill`) and `run` options `--start --end --max-turns --model --dry-run --no-tmux --permission-flag --tmux-session-name --debug --stall-timeout --stall-action --shadow-gates --force-fidelity-fail --force-fidelity` (no `--resume <task-id>`, `--task-parallelism`, `--fresh`, `rerun-tasks`, `verify-checkpoints`). Installed `roadmap run` options: `--agents --allow-regeneration --debug --depth --dry-run --max-turns --model --no-validate --output --resume --retrospective` (no `--prd-file`, `--tdd-file`, `--input-type`, `--no-convergence`, compression or cosmetic-remediation flags). [CODE-VERIFIED by reading the installed site-packages]
- Consequence: task-builder `--cli` (which emits `superclaude reflect run ...`) will fail at the POST gate with the installed CLI; `superclaude prd run` is unavailable; `/sc:roadmap` docs (which mirror the master CLI flags) list flags the installed CLI rejects. The June-branch sprint doc's "5 subcommands" claim (E.2) matches the INSTALLED CLI, not master.
- Staleness that persists in master: `docs/sprint-cli-deep-dive.md:60, 70` (5 subcommands / 16 options), `MS/skills/sc-roadmap-protocol/SKILL.md:36` ("future tasklist command"), `MS/commands/spec-panel.md:416-417` (`/sc:code-to-spec`), and task-builder's claim that prd/tdd call it via `Skill(skill: "task-builder")` (`MS/skills/task-builder/SKILL.md:47, 126`) while master prd/tdd spawn the agent. [CODE-CONTRADICTED, all re-checked in master]

---

# PART 2: SYNTHESIS FOR THE QUICK-REFERENCE GUIDE (master-authoritative)

## 1. The depth ladder (lightest to heaviest)

Cost column is an AGENT-COUNT proxy taken from the code. The only token figures in code are the `/sc:task` verification costs (`sc-task-protocol/SKILL.md:122-127`). Wall-clock and token totals per rung are UNVERIFIED.

| # | Rung | Invocation (exact) | Produces | Rough cost (from code) | Use when | Evidence |
|---|---|---|---|---|---|---|
| 0 | Direct interactive edit | Just ask Claude; no command | Edits only | 0 extra agents | One file, obvious change. IC-Harness project rule: any work over 5 edits or multiple files MUST go through a task file | `IC-Harness/CLAUDE.md` Custom Project Rule 6 |
| 1 | `/sc:task` LIGHT or EXEMPT | `/sc:task "<op>"` (auto) or `--compliance light` / `exempt` | Edits or an answer; no ledger | Verification skipped (0 tokens) | Typo, comment, lint, docstring; read-only questions | `MS/commands/task.md:71-100`; `sc-task-protocol:126-127` |
| 2 | `/sc:task` STANDARD | `/sc:task "<op>"` or `--compliance standard` | Edits + affected tests run | Direct tests, 300-500 tokens verification | Ordinary add/fix/update, few files | `sc-task-protocol:98-104, 125` |
| 3 | `/sc:task` STRICT | `--compliance strict` (auto for security, auth, DB, migration, refactor) | Edits + quality-engineer sub-agent + `pytest -v` + adversarial questions | 1 verifier sub-agent, 3-5K tokens | Safety-critical; security words always win | `sc-task-protocol:84-96, 124, 129`; `commands/task.md:73-77` |
| 4 | Simple plan + middleweight executor (master only) | `/sc:workflow <prd-or-prompt> --depth quick\|standard\|deep [--handoff implement]` then `/sc:implement @.dev/workflow/<slug>/plan.md` | `plan.md` (Template 00) + per-task ledger `.dev/implement/<slug>/progress.md` | 0 subagents to plan; 1 reviewer per task (inline if <=3 tasks), 1 fix pass | Multi-step change with known scope you want acceptance-criteria-checked task by task, resumable, without MDTM ceremony | Section G.2 |
| 5 | MDTM "simple" task file: task-builder Quick + Template 01 + lite QA | `/task-builder <goal>` with "quick"/"light" wording, or a BUILD_REQUEST with `TEMPLATE: 01`, `QA_INTENSITY: lite`, `QA_GATE_REQUIREMENTS: FINAL_ONLY`; then `/task <path>` | MDTM task file + research + QA reports in `.dev/tasks/to-do/TASK-RF-*/` | Build: 3 researchers, research gate 2 agents at lite, 5 task-file validators, PRE reflect if spec. Run: /task 6+ agent lens gate per Phase 2+, post-completion 2 validators, POST reflect | Small known-scope work that must be resumable across sessions and audited | Sections A, B; `MS/skills/task/SKILL.md:194, 282` |
| 6 | Standard task file: Standard tier + Template 02 + standard QA | `/task-builder <goal>` (default) then `/task <path>` | Same, with discovery/build/test/review handoff patterns (Section L) and per-phase gates | 4-5 researchers, 0-1 web; 7-agent final gates at standard | Most multi-file features, 5-20 files | `MS/skills/task-builder/SKILL.md:137, 1001-1004`; I22 |
| 7 | Deep task file: Deep tier + Template 02 + full QA | Say "thorough", "comprehensive", "deep dive", or multi-subsystem scope | Same, multi-track possible | 6-8 researchers, 1-2 web; full I19 gates (6-12+ agents) | 20+ files, multiple subsystems | `MS/skills/task-builder/SKILL.md:138, 143-146` |
| 8 | Research first | `/tech-research <question>` (Quick/Standard/Deep, default Deep) then feed the report to `/task-builder` | Research report with Implementation Plan section | Deep: 5-10+ codebase + 2-4 web agents; final gate 11+ agents | You do not yet know what to build or where | `MS/skills/tech-research/SKILL.md:97-117`; IC-Harness `tech-research:27` |
| 9 | Requirements and design documents | `/sc:brainstorm "<topic>"`, `/prd <product>`, `/tdd <component> [PRD path]`, review with `/sc:spec-panel @file` | PRD / TDD (template-conformant) or merged requirements | prd/tdd 2-10+ agents by tier, 300-2500 line budgets | New product or component; need a spec before planning | Section D; `commands/brainstorm.md:35-40`; `commands/spec-panel.md:22` |
| 10a | Release pipeline (sprint lane) | `/sc:roadmap spec.md [tdd.md prd.md]` (or `superclaude roadmap run`) -> `/sc:validate-roadmap <dir>` -> `/sc:tasklist <roadmap.md> [--spec ...]` -> `superclaude sprint run <tasklist-index.md>` | roadmap.md, validation report, `tasklist-index.md` + `phase-N-tasklist.md`, sprint execution | Roadmap debate 1-3 rounds; every sprint phase is a fresh Claude session running `/sc:task ... --compliance strict` | Multi-phase release, unattended or long-running execution | Section E; `MS/cli/sprint/process.py:220-221` |
| 10b | Release pipeline (RF lane) | `/roadmap <PRD/TDD/prompt>` then `/task <phase task file>` per phase | Roadmap doc + BUILD_REQUESTs (+ one MDTM task file per phase at Deep) | Deep/full: 44-48 evaluating agents for 6 phases | Phased plan that stays inside the MDTM /task world | `MS/skills/roadmap/SKILL.md:8, 27, 100-126` (= IC-Harness) |

Planning-only side rungs (no executor, no checklist): `/sc:design` (architecture/API spec, then `/sc:implement`, `MS/commands/design.md:22, 109`). In June/IC-Harness, `/sc:workflow` is also plan-only prose with "Next Step ... `/sc:implement`" (`IC/commands/workflow.md:112-133`).

## 2. The "simple task file": what it is, how to ask, what QA it keeps or drops

There are TWO things a user may mean. Name them explicitly in the guide.

### 2a. Template 00 plan (master only): the genuinely simple one

- What: a 47-line markdown plan, Tasks with Acceptance criteria, no checkboxes, no MDTM frontmatter (`MS/templates/workflow/00_mdtm_template_simple_task.md`).
- How to ask: `/sc:workflow "<feature or @prd.md>" --depth quick` then `/sc:implement @.dev/workflow/<slug>/plan.md` (or add `--handoff implement`). Resume: `/sc:implement @plan.md --resume`.
- Keeps: per-task diff-vs-acceptance-criteria review with citations, one fix pass, HALT on non-compliance until an operator Ruling, resumable ledger, optional whole-list review, lint/tests as recorded extras.
- Drops: task-builder research and its gates, rf-qa/rf-qa-qualitative lens panels, PRE and POST `/sc:reflect`, MDTM F1 loop, `/task` entirely. Not available in IC-Harness today (G.3).

### 2b. MDTM Template 01 task file (all versions): "simpler" but still heavy

- What: the generic MDTM template; the generated file is sequential with no Section L handoff patterns; `QA_GATE_REQUIREMENTS` defaults to FINAL_ONLY (one final QA phase) instead of PER_PHASE (`MS/skills/task-builder/SKILL.md:1001-1004`).
- How to ask: there is NO flag. Options, in order of reliability:
  1. Write a BUILD_REQUEST file and run `/task-builder path/to/BUILD-REQUEST.md` with `TEMPLATE: 01`, `QA_INTENSITY: lite`, `QA_GATE_REQUIREMENTS: FINAL_ONLY` (fields at `MS/skills/task-builder/SKILL.md:996-1004`; BUILD_REQUEST may carry a TEMPLATE preference, `:39`).
  2. Phrase the prompt with the I22 trigger words: "quick", "light", or "quick with full QA" / "deep but lite QA" for mixed dials (`01_mdtm_template_generic_task.md:785, 794-797`), and name the <5 files so the Quick tier rule applies (`MS/skills/task-builder/SKILL.md:144`).
  - Caveat: Template 01 is chosen only for "trivial tasks with known inputs and outputs"; "For most task-builder requests, the answer is Template 02" (`MS/skills/task-builder/SKILL.md:497`). Quick tier does not force Template 01.
- Keeps (always): research gate (2 agents at lite), task-file structural + research-alignment + qualitative validation, PRE reflect when a spec resolves, POST reflect item (skill mode: depth = max(TCS-derived, standard), O4 floor; `--cli` mode: fixed `--depth deep`; `MS/skills/task-builder/SKILL.md:1076-1085`), serialized fix protocol and fidelity gate at all intensities (I22 `:821-823`; Template 02 `:1102`), and /task executor gates.
- Drops or reduces: researchers 3 instead of 4-8, 0 web agents, in-file QA gate agents 3 instead of 7 or 6-12+, 1 fix cycle with leftovers logged as Open Questions (I22 `:799-806`), per-phase gates collapsed to a final gate.
- `QA_GATE_REQUIREMENTS: NONE` exists (`MS/skills/task-builder/SKILL.md:1002`) but turning gates off needs explicit user authorization under IC-Harness Custom Project Rule 1, and /task still adds its own executor gates.

## 3. Canonical chains documented in the code

| Chain | What the code actually says | Status | Evidence |
|---|---|---|---|
| Any doc skill: Stage A (task-builder) -> Stage B (`/task`) | tech-research, tech-reference: `Skill(skill: "task-builder", args: "${TASK_DIR}BUILD-REQUEST.md")` then `Skill task`. prd, tdd (master): spawn the `rf-task-builder` agent, then `Skill task` | Documented, but split implementation in master | `MS/skills/tech-research/SKILL.md:594, 609`; `MS/skills/prd/SKILL.md:395, 420`; `MS/skills/tdd/SKILL.md:386, 411` |
| `/task-builder` -> user runs `/task` | Direct invocation stops after building; user executes with `/task [path]` | Documented | `MS/skills/task-builder/SKILL.md:12` |
| tech-research -> task-builder -> task (as an INTER-skill handoff: research report becomes the input of a new implementation task) | Not stated as a handoff anywhere. tech-research only promises an actionable Implementation Plan (`tech-research` rule "Implementation plans must be actionable") | INFERRED, not documented. Present as a recommended practice, not a coded chain | IronClaude June `tech-research/SKILL.md:1333`; grep for a handoff in task-builder/tech-research returned none |
| prd -> tdd | "The PRD feeds the TDD the same way tech-research feeds a tech-reference" | Documented | `MS/skills/tdd/SKILL.md` (June `:44`, same text) |
| prd/tdd -> /roadmap -> /task (RF lane) | "/roadmap fills the gap between upstream document skills (/prd, /tdd) and downstream execution (/task)"; Deep tier produces one task file per phase via `/task-builder` | Documented | `MS/skills/roadmap/SKILL.md:8-12, 106-108` |
| spec/TDD/PRD -> sc:roadmap -> validate-roadmap -> sc:tasklist -> sprint run (sprint lane) | `/sc:roadmap` "See Also: /sc:validate-roadmap, /sc:tasklist"; validate-roadmap GO = "ready for tasklist generation"; tasklist output is "compatible with `superclaude sprint run`" but does not run it | Documented across files (no single file shows the whole chain) | `MS/commands/roadmap.md` See Also; `MS/skills/sc-validate-roadmap-protocol/SKILL.md` GO row (June `:688`); `MS/commands/tasklist.md:118`; `MS/skills/sc-tasklist-protocol/SKILL.md` (June `:14-16, 40`) |
| PRD/TDD -> spec-panel -> roadmap | `/sc:spec-panel @tdd.md --downstream roadmap` emits a scoped release spec with roadmap frontmatter | Documented | `MS/commands/spec-panel.md:36, 272, 280` |
| brainstorm -> design / tasklist / task-builder / implement | `--handoff design` (text), `--handoff tasklist` (invokes sc-tasklist-protocol), `--handoff task` (invokes task-builder); next steps `/sc:design`, `/sc:tasklist`, `/sc:implement` | Documented | June `IC/commands/brainstorm.md:60, 71, 173-175, 197-201` (master brainstorm.md DIFF, same line count; not re-read) |
| workflow -> implement (master) | `/sc:workflow` writes plan.md; "Next: `/sc:implement @plan.md` or `/sc:tasklist` on a roadmap"; `--handoff implement` invokes it | Documented | `MS/commands/workflow.md:42, 82`; `MS/skills/sc-workflow-protocol/refs/overlap-routing.md:5` |
| design -> implement -> test -> git | `/sc:design` next `/sc:implement`; `/sc:implement` suggests `/sc:test` and `/sc:git` as optional | Documented | `MS/commands/design.md:109`; `MS/commands/implement.md:135, 139` |
| sc:roadmap-protocol pipeline position | "spec(s) -> sc:roadmap -> roadmap artifacts -> future tasklist command -> sc:task" | STALE text (tasklist exists, sprint not mentioned) | `MS/skills/sc-roadmap-protocol/SKILL.md:36` |

## 4. Differences a user will trip on

1. **`/task` vs `/sc:task` are different tools.** `/task` executes an MDTM task file with lens QA gates; `/sc:task` is a one-shot compliance-tiered executor with no file. The POST reflect gate mandates "/task (never /sc:task) for any re-execution" (`MS/skills/task-builder/SKILL.md` Rule 20). Sprint uses `/sc:task --compliance strict` per phase (`MS/cli/sprint/process.py:220-221`).
2. **`/roadmap` vs `/sc:roadmap`.** `/roadmap` (RF skill) produces BUILD_REQUESTs and MDTM task files for `/task`; `/sc:roadmap` produces roadmap pipeline artifacts for `/sc:tasklist` + `superclaude sprint run`. `/roadmap` does not exist in the June branch.
3. **`/sc:workflow` and `/sc:implement` changed meaning.** Master: Template 00 plan + ledgered per-task QA executor; old flags `--type/--framework/--safe/--with-tests` and `--depth shallow|normal`, `--parallel` now STOP. June and IC-Harness live copies: old prose behavior and old flags (G.3).
4. **Tier does not pick the template or QA intensity in task-builder.** Three independent dials (Section A). Doc skills in IC-Harness and master tech-research/tech-reference map tier to QA intensity; master prd/tdd and the June branch do not, so the rf-task-builder default `full` applies.
5. **Lite QA in the task file does not make `/task` light.** Master and IC-Harness `/task` run a minimum 6-agent lens gate after every Phase 2+ and say fewer than 6 is "a protocol violation" (`MS/skills/task/SKILL.md:194, 282`), while I22 lite says 3 and "Double QA: DISABLED" (`01_mdtm_template_generic_task.md:785, 806`). The June `/task` instead ran a single rf-qa per phase. See Open Questions.
6. **Tier names differ by skill.** task-builder, tech-research, `/roadmap`: Quick/Standard/Deep. prd, tdd, tech-reference: Lightweight/Standard/Heavyweight. `superclaude prd run --tier lightweight|standard|heavyweight` (`IC/cli/prd/commands.py:20-26`). Depth flags (`--depth quick|standard|deep`) on `/sc:roadmap`, `/sc:brainstorm`, `/sc:workflow` mean debate rounds or phase counts, not research tiers.
7. **Defaults differ.** task-builder, prd, tdd, tech-reference default Standard; tech-research and `/roadmap` default Deep; `/sc:task` defaults STANDARD; `/sc:workflow` defaults standard.
8. **`/roadmap` Quick and Standard do NOT create task files.** Quick = roadmap doc only; Standard = roadmap + BUILD_REQUESTs; only Deep runs `/task-builder` per phase (`MS/skills/roadmap/SKILL.md:106-108`).
9. **Installed CLI lags the source.** pipx `superclaude` 4.2.0 is a 2026-03-24 snapshot of the June repo path: no `reflect`, `prd`, `eval` subcommands; sprint lacks `--resume <task-id>`, `--task-parallelism`, `rerun-tasks`; roadmap lacks `--prd-file`, `--tdd-file`, `--input-type`. task-builder `--cli` and `superclaude prd run` will fail until reinstalled from master (G.3).
10. **Nothing IronClaude is installed user-wide.** `~/.claude/skills` has none of these skills and `~/.claude/commands/` is empty; availability depends on the project's own `.claude/`.
11. **`--cli` is the validated POST path in master.** Master task-builder discloses that the default skill-mode POST path "is NOT yet session-validated" and says "prefer `--cli` for mission-critical builds" (`MS/skills/task-builder/SKILL.md:43, 2393`), but `--cli` needs the `superclaude reflect` CLI that the installed build lacks.
12. **PRE reflect only runs with a spec.** No `--spec` (or `@file`, or SPEC/PRD/TDD field) means `verdict: skipped`. In IC-Harness and master, when a spec resolves the PRE run is mandatory (`ICH/skills/task-builder/SKILL.md:1664-1666`; `MS/skills/task-builder/SKILL.md:1662-1666`).
13. **`/sc:tasklist` has `--no-reflect`** to skip both reflect gates (`MS/commands/tasklist.md:39`); task-builder has no equivalent switch (POST_REFLECT_GATE is hard-coded ENABLED in the builder prompt, `MS/skills/task-builder/SKILL.md:1076`).

## 5. Open questions / UNVERIFIED items

1. **I22 lite vs /task 6-agent floor (conflict).** Template I22 allows 3-agent lite gates and disables "Double QA"; master/IC-Harness `/task` mandates 6+ agents per phase gate and does not read `qa_intensity`. Which wins at runtime is not specified. UNVERIFIED; needs a run or an owner ruling.
2. **Does task-builder honor a user-supplied `TEMPLATE: 01` in a user BUILD_REQUEST** when A.6 triage would pick 02? The Input section says the file may carry a "TEMPLATE preference" (`:39`) but A.6 has no precedence rule. UNVERIFIED.
3. **Do task-builder's A.10/A.10.25/A.10.5 validators scale with QA_INTENSITY?** No intensity wording found in those sections (June `:1305-1615` scan); the research gate does scale (`:687-689`, master `:691`). Treat as fixed 5 agents. Partially verified.
4. **Template 00 naming.** File is named `00_mdtm_template_simple_task.md` but states it "is not an MDTM /task checklist" and is consumed only by `/sc:workflow`. Whether `/task` or task-builder will ever accept it is undecided in code.
5. **Token and wall-clock cost per rung** are not in code except `/sc:task` verification estimates. All cost columns are agent-count proxies.
6. **Master prd/tdd vs tech-research/tech-reference delegation split** (agent vs Skill). Unclear whether intentional; task-builder text still claims all call the skill. CODE-CONTRADICTED doc text.
7. **Master `brainstorm.md` and `spec-panel.md` were not re-read line by line** (DIFF with same line counts); their cited June lines may have shifted wording. Flag lines cited with `IC/` for re-check.
8. **IC-Harness `/sc:task` and `/sc:brainstorm` command files** match neither branch (cmp). Their exact divergence was not diffed.
9. **Sprint doc** (`docs/sprint-cli-deep-dive.md`) phase-mode and discovery claims were taken from the doc, not re-verified in `config.py`.
10. **Whether the user intends IC-Harness to adopt master's `/sc:workflow` + `/sc:implement` + Template 00.** Not present in IC-Harness today; the guide must say which environment each rung applies to.
11. **Reinstall path for the CLI** (`pipx install --force /Users/cmerritt/GFxAI/IronClaude-tier-tools` or similar) is not documented in the sources read. UNVERIFIED.
