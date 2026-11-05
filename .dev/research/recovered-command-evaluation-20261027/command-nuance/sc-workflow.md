# Command nuance: /sc:workflow

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus (Ryan's own example): when to use `/task-builder` on a single story versus `/sc:workflow`, by complexity band, with `--depth`, `--strategy`, `--handoff` by band; and when two or more single-story workflow plans are acceptable instead of one task-builder run for a feature.

**Citation key.** Home dir = `/home/coder/.claude`. WF = `commands/sc/workflow.md`. WP = `skills/sc-workflow-protocol/SKILL.md`. IN, PT, QG, TPL, RC, OR = `skills/sc-workflow-protocol/refs/` `input-parse.md`, `phase-templates.md`, `quality-gates.md`, `00_mdtm_template_simple_task.md`, `return-contract.md`, `overlap-routing.md`. HW = `HOW-WE-WORK.md`. TB = `skills/task-builder/SKILL.md`. IM = `commands/sc/implement.md`. IS = `skills/sc-implement-protocol/SKILL.md`; QA, MW, LG = its `refs/qa.md`, `refs/managed-workspace.md`, `refs/ledger.md`. RFC = `commands/sc/reflect.md`. TSC = `commands/sc/troubleshoot.md`. TSK = `skills/sc-troubleshoot-protocol/SKILL.md`. RH = `skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`. CV = `command-value-by-phase.md`. VAL = `validation-feature-task-builder-vs-sc-workflow.md` (same folder as CV). OBS = observed on disk in `.dev/tasks/done/` of this checkout (read-only `ls`, `sed`, `grep`).

## 1. Status and role

- Does: "Generate a phased implementation plan from a PRD, spec, or feature prompt" (WF:3); writes a new package `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` and no product code (WF:12, WF:65). Phase: Tasklist; with `--handoff implement` it also starts Implement (WP:64). Standalone-invokable, NOT retired. Backing skill exists: `skills/sc-workflow-protocol/` (SKILL.md plus 6 refs, all read).
- Also called by other skills with fixed flags `--depth standard --handoff none`: `/sc:troubleshoot --fix` plan route (TSK:561; RH:109) and `/sc:reflect --remediate` plan route (RFC:307). An engineer did not necessarily choose such a package.
- Overlaps: `/task-builder` (plan for the same work, heavier), `/sc:implement` (its executor, not an overlap), `bmad-create-story` (BMad lane, CV:118). Retired neighbour: `/sc:tasklist` is named in WF:74, WF:80 and printed by `--handoff tasklist` (OR:8): never follow it (ruling 3).

## 2. Flags

Defined in WF:35-42 and WP:5 (frontmatter `argument-hint`); enums at IN:54. The command file and the protocol agree on every flag.

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `<path>` or `<prompt>` | exactly one: existing file (`@path` unwraps) or leftover text | required (`E-NO-SOURCE`, WF:22; IN:46) | Source is snapshotted byte-exact to `<pkg>/source.md`; the ID subject comes from the file basename or the prompt (IN:5, IN:18-20, IN:37) | File path when a spec, PRD or story file exists: it is the only way to give workflow a spec (no `--spec`, WF:35-40). Prompt when the change is a few named files (TPL:15) | Prompt standing in for a driving spec: the Wave 4 check then only confirms the plan covers the prompt (HW:191) |
| `--strategy` | `systematic` \| `agile` \| `enterprise` | `systematic` (WF:38) | Phase skeleton only (PT:5-9). `enterprise` adds a risk/ops column on every phase plus a rollout phase and, when `--depth` is omitted, sets depth `deep` (WP:28; PT:9) | `systematic` always as default. `agile` (slice 0 spike, then thin increments, PT:7) when the first slice should prove the approach (J). `enterprise` when a rollout phase is wanted (infra, deploy) (J) | `enterprise` as a way to get more review: the review is unchanged, one reviewer per task (QA:11) and Wave 4 gets default reflect flags (WP:56) |
| `--depth` | `quick` \| `standard` \| `deep` | `standard` (WF:39) | Phase cap quick 2-4, standard 4-8, deep 6-12 (WP:38; PT:13). Gate: quick = schema-min, standard/deep = full, which adds "every source requirement is covered by at least one task" (WP:52; QG:24-39). Does NOT change: research (none exists, WP:72), reviewer count (QA:11), or the Wave 4 reflect depth (defaults, WP:56) | `quick` for LOW prompt-sourced work (HW:17, HW:113, HW:305). `standard` when the source is a spec file or the work needs 5-8 phases. `deep` only when more than 8 phases are needed or `enterprise` forces it | `quick` on a spec-file source with several requirements (the coverage line is not in schema-min, QG:26-29 vs QG:39). `deep` as a substitute for task-builder: PT:13 says deep is "split layers, still one session", it adds phases, not research or panels |
| `--handoff` | `none` \| `design` \| `implement` \| `tasklist` | `none` (WF:40) | `none`: prints next-step strings incl. `/sc:implement <pkg>/<id>.md` (OR:13). `design`: prints `/sc:design @<pkg>/<id>.md` (OR:10). `tasklist`: prints `/sc:tasklist --source <roadmap>` (OR:8). `implement`: invokes `sc:implement-protocol` on the plan after the contract is written; a failed handoff makes the contract `partial` (WP:64; OR:7; RC:28) | `none`: the guide's route is read the plan, then run `/sc:implement` (HW:17, HW:114, HW:228). `implement` only when the plan was already approved or the source is trivial (J) | `tasklist`: never, it points at a retired command (ruling 3). `design`: no guide row uses it (HW has no `--handoff` with workflow; its three hits are brainstorm, HW:53, 151, 310). `implement`: skips the human read of the plan, and callers forbid it (TSK:613; RH:109) |
| Banned | `--output`, `--parallel`, `--validate`, `--depth shallow\|normal` | - | `E-LEGACY`, no package, no yaml (WF:42; IN:9-12, IN:49) | - | - |
| Unknown enum value | any value outside the enums above | - | `E-BAD-FLAG`, no package (IN:48) | - | - |

**Does not exist on `/sc:workflow`** (absent from WF:35-40 and WP:5): `--spec` (the source argument is the spec); `--output` (retired, WF:42); `--resume`, `--ledger`, `--skip-final-review` (these belong to `/sc:implement`, IM:57-59); any flag to turn off the Wave 4 reflect (WP:56-58); `--tier`, `--coverage-floor`, `--remediate` (reflect or troubleshoot flags; Wave 4 passes defaults, WP:56); `--fix`, `--type`.

**Three different "quick"s** a checker may meet: workflow `--depth quick` (phase cap and gate, WP:38, WP:52); task-builder's Quick tier (3 researchers, under 5 files, TB:134-136); and TCS-quick (reflect depth, TCS <= 12, TB:2429-2431). They are unrelated settings.

## 3. Scope x complexity matrix

`/sc:workflow` DOES vary by complexity, but only in plan size and gate strictness (`--depth`), not in rigor: it never gains research, a reviewer panel, or `--spec`. That ceiling is why HIGH belongs to task-builder.

### 3.1 Bands for this command

No file defines bands for workflow. The on-disk anchors are HW:17 (level 3), HW:18-19 (levels 4-5), HW:22 (hard limit), HW:9 (tie rule) and the TCS signals S1 and S2 (TB:2410-2411). Band edges below are (J) unless a cite is shown.

| Band | One-line definition (all must hold) |
|---|---|
| LOW | Files can be named up front and are few (HW:17 "a few files"), one subsystem, requirement stated in a paragraph or one short story, at most 1-2 sessions (HW:17), no driving spec to trace, no risk class, no shared interface. Counting proxy (J): S1 <= 5 and S2 = 1, using the TCS counting rules (TB:2410-2411); the 5 is borrowed from HW:22's edit limit, which counts edits, not files |
| MEDIUM | Files still nameable, 2 subsystems or about 6-10 files (J), a short spec or story file exists but nothing must be traced requirement by requirement, 2 sessions (tie row, HW:17 vs HW:18, HW:9), stable requirements, no risk class |
| HIGH | ANY of: more than 2 sessions (HW:18); must not drift or a spec must be traced (HW:18, HW:102); files cannot be named or the system is not understood (HW:19; workflow has no discovery, TPL:20, WP:72); risk class: secrets, permissions, user input, file paths, infrastructure (J, built from the security-review trigger list HW:200 and the repo `CLAUDE.md` secrets section); shared interface with sibling stories (J); mid-run amendments expected (HW:102 vs MW:42, HW:117) |

### 3.2 Matrix

Legend: "REQUIRED (plan)" = HW:22 makes a written plan mandatory above 5 edits or more than one source file, and either plan command satisfies it; the cell names the lighter command that suits the band. Flag sets are in 3.3.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (HW:16, HW:22: plain edit plus related test) | N/A (J): more than 5 edits or more than one source file is not a one-off (HW:22); rate on the S row | N/A (J): not a one-off; rate on S or F |
| B bug fix | SKIP (J): failing test, fix, `/sc:test` (HW:131) | WORTH IT: `--depth quick`, then `/sc:implement` (HW:132; HW:311 route 3b). A plan (either command) is REQUIRED here by HW:22 | SKIP: `/task-builder` (HW:133; HW:311 route 3c; `/sc:troubleshoot --fix --depth deep` also routes to task-builder, TSC:54) |
| S single story | REQUIRED (plan): `--depth quick` | OPTIONAL, either-or with `/task-builder`; HW:9 says pick the heavier when unsure: `--depth standard` | SKIP: `/task-builder` + `/task` (HW:18) |
| F multi-story feature | OPTIONAL (J), only under the 4.2 exception: one plan per story, `--depth quick`. NOT the F minimum (ruling 4; VAL verdict 1) | SKIP (VAL verdict 1) | SKIP |
| R multi-feature release | OPTIONAL (J), same as F-LOW: per-story plans inside a feature that meets 4.2; never the release plan | SKIP (J) | SKIP (J) |
| N new product | SKIP (J): a product small enough for LOW is S-LOW; rate it there | SKIP (HW:20; `/roadmap` makes the tasks, CV:112) | SKIP |

R re-rating: CV:110 rates workflow R = OPTIONAL. Under Ryan's definition (a multi-feature release with its own plan, implementation and push) the release plan is made of F-scope features, so workflow at release level becomes SKIP; the only surviving use is per-story plans inside a feature (R-LOW, J). The old reading behind the R column is stated at CV:139 ("a release assembles and ships work already built").

### 3.3 Flag set by band (applies to S, B-MEDIUM, F-LOW exception)

| Band | `--depth` | `--strategy` | `--handoff` | Why |
|---|---|---|---|---|
| LOW | `quick` (HW:17, HW:113, HW:305). Use `standard` instead when the source is a spec file with several requirements (J), because only standard/deep check requirement coverage (QG:39) | `systematic` | `none` | 2-4 phases is enough for a few files (PT:13); schema-min gate is cheap; Wave 4 reflect still runs at default depth whatever you pick (WP:56) |
| MEDIUM | `standard` | `systematic`; `agile` (J) if the first slice should prove the approach | `none` | 4-8 phases; full gate including "every source requirement covered" (QG:31-39) |
| HIGH | Not this command. If forced (a caller-built remediation plan, or the operator overrides): `deep` | `enterprise` only if a rollout phase is wanted | `none`, never `implement` | `deep` gives 6-12 phases but the same single reviewer per task (QA:11) and no research or `--spec`; it is not a substitute for task-builder |

### 3.4 TCS as a switch? No (cross-check)

TCS (`3*S1 + 4*S2 + 2*S3 + 2*S4 + 5*S5 + 4*S6`, TB:2422) picks reflect's depth for task-builder (TB:2402), not workflow-versus-task-builder. Arithmetic from the formula: TCS <= 12 allows at most 2 files in one subsystem (3 files in one subsystem is already 13); 13-34 spans about 3-10 files in one subsystem (TB:2429-2433). HW's "a few files" is therefore already TCS-standard, so TCS cannot be the line between level 3 and level 4. Use S1 and S2 only as a counting aid (JUDGMENT).

### 3.5 What this repo actually shows (OBS)

Two real workflow packages sit in `.dev/tasks/done/`; none in `to-do/` (`ls`, 2026-10-27). Counts are from `grep` over the plan body outside fenced code, not a run of the TCS rules, and they include paths named in prose, so treat as approximate.

| Package | Tasks / phases / `Depends on` | Distinct paths S1 / subsystems S2 (approx) | `depth` / `strategy` / `handoff_action` | `source_origin`, `reflect_status` |
|---|---|---|---|---|
| `TASK-WF-designSpec-20261022-132541` | 15 / 7 / 13 | about 44 / about 17 | standard / systematic / none | a 68 KB design spec file; `partial` (contract says the plan was amended three times after reflect runs, to v4) |
| `TASK-WF-takeThePlanConfi-20261023-173430` | 8 / 5 / 6 | about 51 / about 21 | standard / systematic / none | `inline`; `skipped` (contract: reflect was interrupted, plan not independently reviewed) |

Reading: the team already uses `/sc:workflow` at sizes the guide assigns to task-builder (HW:18), always at default depth. A checker that applied the LOW/MEDIUM/HIGH edges above to these two would call both HIGH. The first one shows the operator hand-running the spec trace that task-builder automates (two reflect rounds, three FINAL `issues` before `pass`, OBS `progress.md`). Do not flag workflow use on size alone (see 6).

## 4. Choose this or the neighbour

### 4.1 `/sc:workflow` or `/task-builder` for ONE story (Ryan's example)

Ordered tests, first hit wins. Cites are the on-disk basis; (J) marks my reading. Differentiators already validated (VAL verdict 1): research, spec trace, review depth; not multi-session resume (both resume, VAL E3).

| # | Test | Result | Basis |
|---|---|---|---|
| 0 | One source file plus its test, 5 edits or fewer, exact change known | Neither: plain edit plus related test, optionally `/sc:implement "<prompt>"` (the one-off minimum is PROPOSED, not confirmed by Ryan) | HW:16, HW:22 |
| 1 | An agreed spec, PRD, TDD or story file must be traced requirement by requirement | `/task-builder --spec <path>`. Workflow has no `--spec`; its Wave 4 check only covers its own source (inline prompt: "checked against your request", HW:191) | HW:18, HW:102; WF:35-40; WP:56; TB:41 |
| 2 | Files cannot be named up front, or how the system works is unknown | `/tech-research` first, then `/task-builder` (level 5). Workflow pushes discovery onto the author and has no research wave | HW:19; TPL:15, TPL:20; WP:72 |
| 3 | More than 2 sessions expected, or "must not drift from what was agreed" | `/task-builder` + `/task` | HW:18, HW:243 |
| 4 | Risk class touched: secrets, permissions, user input, paths, infrastructure | `/task-builder` (J): HW:22 sends "riskier" work to level 4; the risk list is my reading of HW:200 and the repo `CLAUDE.md` secrets section | HW:22 |
| 5 | The plan is likely to be amended mid-run (open questions expected) | `/task-builder`: task files accept new unchecked items; a managed workflow plan freezes at the first task start (`E-PLAN-CHANGED`) | HW:102; HW:117; MW:42 |
| 6 | Story shares an interface with sibling stories | `/task-builder`, one run for the feature (J) | VAL signals table |
| 7 | Exactly 2 sessions, or 2 subsystems, none of tests 1-6 hit | Either command is legal; HW:9 says choose the heavier (`/task-builder`). A checker should accept either (J) | HW:9, HW:17, HW:18 |
| 8 | Few files, clear scope, 1-2 sessions, no spec to trace | `/sc:workflow`: `--depth quick` (LOW) or `standard` (MEDIUM) | HW:17, HW:113 |

Cost side: task-builder has no lightweight mode; even its Quick tier spawns 3 researchers (TB:136) and adds its gates (VAL E2; agent counts there are the VAL author's arithmetic and were not re-derived here). That is the plausible reason the guide keeps level 3 for workflow (the guide does not state it: J).

### 4.2 Two or more single-story workflow plans instead of ONE task-builder run for a feature

Status: this is a JUDGMENT exception. Ruling 4 says workflow + implement is not eligible as the multi-story F minimum, and VAL line 155 offers the same exception as a suggestion. It needs Ryan's confirmation (U1). It does not make workflow the F minimum; it only says a checker need not flag it.

Acceptable only when ALL hold:

| # | Condition | Basis |
|---|---|---|
| 1 | Every story is individually LOW or MEDIUM and trips none of tests 1-6 in 4.1 | HW:18 |
| 2 | Stories are independent: own goal, different source files, different outputs, no dependency between them. This is task-builder's own test for splitting into tracks | TB:304-309 |
| 3 | No feature-level spec to trace. Each package checks only its own source and a new package is made per run, so no feature-level coverage number exists | WP:56; IN:16; VAL E4 |
| 4 | Each story fits 1-2 sessions and is built and committed on its own | HW:17 (commit-per-story is Ryan's pipeline, brief item 5) |
| 5 | No shared interface: no shared files and no `Depends on` across packages | VAL signals table (J) |
| 6 | Count of plans: no file gives a number. Soft ceiling 5 (J), borrowed from task-builder's maximum of 5 tracks | TB:324 |

If any condition fails: ONE `/task-builder` run for the feature (single track, or up to 5 independent tracks, TB:311-324) with `--spec` when a spec exists.

### 4.3 Other neighbours

| Neighbour | Decision rule | Basis |
|---|---|---|
| `/sc:implement` without a workflow plan | A prompt, spec, tasklist or informal notes are all valid sources; informal prose becomes one task whose acceptance criteria are the text (IM:24-29; IS:62, IS:88). Use direct for the T-level optional step. Above HW:22's limit, write a plan first. What workflow adds: per-task acceptance criteria, coverage gate at standard/deep, advisory pre-reflect, and the managed package with a mandatory fresh FINAL review plus archive (MW:44-62) instead of the advisory whole-list pass on legacy sources (IS:153) | HW:22 |
| `bmad-create-story` (BMad lane, CV:118 marks it "‡ with `/sc:workflow` for the single-story case") | Pick the lane at the Spec step and stay in it until the PR (CV:223). In the BMad lane the story file replaces the plan; do not also run workflow on it. Its stated goal: a story file giving the dev agent everything needed (`.claude/skills/bmad-create-story/SKILL.md:8`) | CV:223 |
| `/sc:tasklist` (RETIRED) | Never recommend or run. WF:74, WF:80 and OR:8 (`--handoff tasklist`) still name it; treat those lines as stale | ruling 3 |
| `/sc:design` via `--handoff design` | Prints `/sc:design @<pkg>/<id>.md` only (OR:10). No guide row routes plan-to-design; design comes before the plan in every guide workflow (HW:98) | HW:98 |
| Callers (`/sc:troubleshoot --fix`, `/sc:reflect --remediate`) | They build the plan for the engineer with `--depth standard --handoff none` and stop; the engineer then runs `/sc:implement`. For HIGH bug fixes `--fix --depth deep` routes to task-builder instead (TSC:54, TSC:191) | TSK:561, TSK:613; RFC:307 |

## 5. What a scheduled checker can see

Stated in files AND observed in this checkout (two packages in `.dev/tasks/done/`, none in `to-do/`; OBS). Nothing was run.

| Footprint | Where stated | Observed |
|---|---|---|
| Folder `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>[-2..-9]/` holding `<id>.md`, `source.md`, `return-contract.yaml`; later `progress.md` and `artifacts/` from `/sc:implement` | IN:35-40 | Yes, all five items in both packages, folder in `done/` |
| Plan frontmatter: `schema: workflow-plan/1.2`, `source`, `strategy`, `depth`, `slug`, `version`, `priority`, `created_date`. The `schema` line is the fingerprint of the workflow lane | QG:5-14 | Yes (`strategy: systematic`, `depth: standard` in both) |
| `return-contract.yaml`: `status`, `handoff_action`, `depth`, `strategy`, `source_origin` (original path or `inline`), `reflect_status`, `reflect_report_path`, `unresolved`. No `coverage_pct` or verdict field | RC:5-19 | Yes; `reflect_status` seen as `partial` and `skipped`; `unresolved` carried free-text amendment history |
| Ledger `progress.md`: `PLAN: sha256=...`, `T<id>: start sha=...`, `T<id>: complete verdict=... evidence=...`, optional `T<id>: Ruling:`, `FINAL: pass\|issues`, `ARCHIVE: start ...` | MW:36-42, MW:56-62; `T<id>: Ruling:` form at HW:117; `ARCHIVE: Ruling:` at MW:66-70 | Yes; plan 1 shows `Ruling:` lines on T12-T15 and FINAL `issues` x3 then `pass` |
| Git refs `refs/superclaude/implement/<slug>/T<id>` while a task is in flight, deleted on complete | IS:112, IS:114 | Not checked (transient) |
| Move to `.dev/tasks/done/<id>/` after a FINAL pass; Linux only, otherwise "archive-blocked" and the folder stays in `to-do/` | MW:60, MW:76; HW:17 | Seen in `done/` here |
| Wave 4 reflect output (advisory), default `.dev/reflect/pre-<name>-<timestamp>/`, path in the contract | WP:56; RFC:101 | Path recorded in plan 1's contract; its folder not opened |
| Pre-creation STOPs (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`) leave nothing on disk | IN:9-12, IN:42-50 | Not applicable |

What the footprint tells a checker: chosen `depth`, `strategy`, `handoff_action`, and `source_origin` (a spec path versus `inline`). It does NOT tell whether the engineer or a caller chose them: callers use `--depth standard --handoff none` and a source named `remediation-source.md` or `diagnosability-plan-source.md` (RH:75, RH:109; `skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:247-248`). Not visible: the typed command, the HW:22 edit count, session count (transcript only). Distinguishing lanes in one scan: `TASK-WF-*` with `source.md` + `return-contract.yaml` = workflow lane; a task file with `reflect_post_mode` and `research/` + `qa/` siblings = task-builder lane (VAL "Distinguishing the two lanes").

Caveat (UNVERIFIED, VAL V12): the ledger header says "Do not `git add` the ledger" (LG:3) while the repo `CLAUDE.md` says `.dev/tasks/` is always staged; managed `progress.md` lives under `.dev/tasks/`. A staged-files check should not treat `progress.md` as a defect either way.

## 6. Expected-step rule

**Count `/sc:workflow` as expected** only when the change crosses HW:22 (more than 5 edits or more than one source file) AND is S-LOW, S-MEDIUM or B-MEDIUM AND no task-builder file covers the same change AND the work is in the task-file lane. A `TASK-WF-*` package OR a task-builder task file satisfies the same "written plan" expectation (HW:22); workflow is never the only acceptable plan.

**Its absence is fine** at T and B-LOW (HW:16, HW:22); at S-HIGH, F, R and N (a task-builder file or `/roadmap` output is the expected plan instead); when a BMad story file exists (CV:223); and when the plan came from a caller. Two further rules: (1) do not flag a `TASK-WF-*` package as the WRONG tool on size alone, because this repo's own packages run well past the LOW/MEDIUM edges (3.5); flag only when a driving spec file exists for the work and the package's `source_origin` is `inline` or is not that spec (spec trace missing, HW:102, HW:191). (2) At F, two or more `TASK-WF-*` packages with disjoint files, `source_origin` pointing at different story sources, and no `Depends on` across them meet the 4.2 exception (J, pending Ryan) and are not a skipped step.

## 7. Proposed changes to command-value-by-phase.md

Proposals only; nothing in CV was edited. Rows 1 and 12 of VAL already propose F = SKIP and the footprint additions; the items below extend them with the complexity layer and the R re-rating.

| # | CV line | Current | Proposed |
|---|---|---|---|
| 1 | CV:110 `/sc:workflow`, T..N cells | `SKIP \| OPTIONAL \| REQUIRED \| OPTIONAL \| OPTIONAL \| SKIP` | Per scope with bands (LOW / MEDIUM / HIGH): T `SKIP / N/A / N/A`; B `SKIP / WORTH IT / SKIP`; S `REQUIRED (plan) / OPTIONAL either-or / SKIP`; F `OPTIONAL (J, 4.2 exception only) / SKIP / SKIP`; R `OPTIONAL (J, per-story only) / SKIP / SKIP`; N `SKIP`. One-cell summary if bands are not adopted: T SKIP, B WORTH IT (MEDIUM only), S REQUIRED (LOW), F SKIP, R SKIP, N SKIP |
| 2 | CV:110 R cell (R re-rating) | `OPTIONAL` (rated under CV:139: a release "assembles and ships work already built") | `SKIP` at release level. Under Ryan's definition (multi-feature plan, implementation, push) a release is several F-scope features, each planned by `/task-builder` or `/roadmap`. Only per-story workflow plans inside a feature meeting 4.2 survive (R-LOW, J) |
| 3 | CV:110 B cell | `OPTIONAL` ("B: only when the fix spans a few files") | `WORTH IT` for B-MEDIUM: it is the guide's route 3b (HW:132; HW:311), `--depth quick`. Keep `SKIP` for B-LOW and B-HIGH |
| 4 | CV:110 Notes | "Guide level 3: `--depth quick`; plan is auto-checked against the request ..." | Append: "`--depth quick` for LOW, `standard` for MEDIUM or a spec-file source (only standard/deep check requirement coverage, QG:39). `--depth` never adds research or reviewers. Use `--handoff none`; `--handoff tasklist` prints a retired command; callers use `--depth standard --handoff none`." Keep VAL row 2's wording on the advisory check |
| 5 | CV:254 Single story, step 1 | "`/sc:workflow "<..>" --depth quick`" | "`/sc:workflow "<..>" --depth quick` (LOW) or `--depth standard` (MEDIUM, or source is a spec file); HIGH goes to `/task-builder` + `/task`" |
| 6 | CV:254 WORTH IT additions | "`/task-builder` + `/task` instead of steps 1-3 if the story is multi-session" | "... instead of steps 1-3 if any HW:18 trigger applies: more than 2 sessions, must not drift or a spec must be traced, files cannot be named, risk class touched, amendments expected (4.1 tests 1-6)" (extends VAL row 10) |
| 7 | CV:255 Multi-story feature | Task-file lane: steps 1-4 start with a spec file and `/task-builder` | Add one line: "Exception (J, needs Ryan): two or more independent LOW/MEDIUM stories with no feature spec may use one `/sc:workflow` plan each (4.2); this is tolerated, not the minimum" |
| 8 | CV:232 O6 Turn spec into steps | "By size: `/sc:workflow` (S), `/task-builder` (F, R), `/roadmap` (N) ..." | "By size and band: `/sc:workflow` (S-LOW, S-MEDIUM, B-MEDIUM), `/task-builder` (S-HIGH, F, R), `/roadmap` (N). Tie at two sessions: heavier (HW:9)" |
| 9 | CV:259 Skippable at every size | lists `/sc:roadmap` + `/sc:tasklist` + `/sc:validate-roadmap` | Add "the `--handoff tasklist` option of `/sc:workflow`" (prints the retired `/sc:tasklist`, OR:8) |
| 10 | CV:266 `/sc:workflow` footprint row | `.dev/tasks/to-do/TASK-WF-*/<id>.md` and `progress.md`; `return-contract.yaml` with `reflect_status`; ... | Add what is observed: `done/` already holds 2 packages; frontmatter `schema: workflow-plan/1.2`; contract fields `depth`, `strategy`, `handoff_action`, `source_origin`; ledger lines `PLAN:`, `T<id>:`, `Ruling:`, `FINAL:`, `ARCHIVE:`; caller-built packages carry `remediation-source.md` or `diagnosability-plan-source.md` as source (section 5) |
| 11 | CV Section 5 intro (CV:281) | "For ... `/sc:implement`, `/sc:workflow` ... I read only the usage and flag lines" | Command file, protocol skill and all six refs of `/sc:workflow` have now been read in full (this file and VAL) |
| 12 | CV:256 Release row (cross-command, not mine to rate) | Minimum path starts at `/sc:reflect --mode post`; planning appears only under "WORTH IT additions" | Under the multi-feature definition planning is not optional; the release minimum should start from the per-feature plans. Left to the agents rating `/task-builder` and `/roadmap` |

## 8. Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | The 4.2 exception (several single-story workflow plans instead of one task-builder run) against ruling 4 ("not eligible as that minimum") | The ruling and VAL line 155 point in different directions; the exception is my reading of VAL, labelled J | Ryan's decision |
| U2 | Every band edge: S1 <= 5 and S2 = 1 for LOW, about 6-10 files for MEDIUM, soft ceiling of 5 plans, the risk-class list | No file gives a threshold for workflow; 5 is borrowed from HW:22 (edits) and TB:324 (tracks) | Ryan's decision, or a measured sample of past plans |
| U3 | Whether Wave 1-2 reads the repo (Grep/Glob) while writing a plan | Allowed tools include them (WP:4), no wave mandates it (VAL V1). OBS: plan 1 has 19 `path:line` citations, plan 2 has 2, which does not show who or what read the code | Run once, or read several more `TASK-WF-*` plans |
| U4 | Whether `--strategy enterprise` with an explicit `--depth quick` keeps the rollout phase under the 2-4 phase cap | PT:9 and PT:13 do not say; WP:28 covers only the omitted-depth case | Run once |
| U5 | Meaning of PT:13 "deep 6-12 (split layers, still one session)": can a deep plan span sessions? | One parenthetical; HW:18 puts multi-session work at level 4 | Maintainers |
| U6 | Whether the Wave 4 reflect report for a workflow plan shows a coverage number | `sc-reflect-protocol` not read; the contract has no such field (RC:5-19) (VAL V5) | Open a `.dev/reflect/pre-*` report; read that skill |
| U7 | The S1 / S2 figures in 3.5 | My `grep` count, not the TCS extraction rules; includes prose paths; TCS is defined for MDTM task bodies, not workflow plans (TB:2410-2411) | Apply the rules by hand to the two plans |
| U8 | How many sessions the two observed packages took | The ledger records one header timestamp only (OBS); `git log` not checked | `git log` on the plan folders and delivery files |
| U9 | Who chose the flags on the two observed packages (engineer or caller) | `source_origin` is a design-spec path in one and `inline` in the other, which suggests an engineer, not proof | Ask the authors |
| U10 | Task-builder gate agent counts and the `qa_intensity` ambiguity used in 4.1's cost note | Taken from VAL E2 / V3, not re-read (only TB:134-146, TB:288-324, TB:2402-2445 were read for this file) | Read TB:691-693, TB:1473 |
| U11 | `bmad-create-story` output and validate action | Only the first 60 lines read; the rest comes from CV:118 and CV:26 | Read the full skill |
| U12 | `--handoff implement` end to end, and the relocation rule after archive (WP:66) | No command run (read-only task) | A dry run on a throwaway checkout |
| U13 | Interaction of "Do not `git add` the ledger" (LG:3) with the `CLAUDE.md` rule that `.dev/tasks/` is always staged | Both read; behaviour not observed (VAL V12) | Run a managed plan once, or ask the maintainers |
| U14 | Whether other engineers' `~/.claude` match this one | Home-directory install is per user (CV U17). WF:54 names `src/superclaude/skills/...`, a source-repo path; the installed copy at `~/.claude/skills/sc-workflow-protocol/` was the one read | Compare installs |
| U15 | Stale references to the retired `/sc:tasklist` inside workflow's own files (WF:74, WF:80, OR:8, plus IM:138 on the implement side) | Seen, not changed (read-only). Whether the maintainers intend `--handoff tasklist` to stay is unknown | Maintainers; a checker should ignore these mentions |

Doc tension noted, resolved from files: HW:17 says `/sc:workflow ... --depth quick` "checks the plan against your request automatically". The check is the advisory Wave 4 reflect (WP:56-58), not the gate; at `--depth quick` the gate does not include requirement coverage (QG:26-29 vs QG:39), and a skipped or failed reflect does not stop the run (WP:58; OBS plan 2 `reflect_status: skipped`).
