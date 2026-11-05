# Command nuance: /sc:improve

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: `--safe`, `--interactive` and related flags by risk and size; the allowed exception to the small-change limit in the routing guide.

Citation key (all under `/home/coder/.claude/` unless noted; line numbers from full reads this session):

| Tag | File |
|---|---|
| IMP | `commands/sc/improve.md` (130 lines, read fully) |
| HWW | `HOW-WE-WORK.md` (327 lines, read fully) |
| CLN | `commands/sc/cleanup.md` (read fully) |
| ANA | `commands/sc/analyze.md` (grep only: line 111) |
| SRC | `skills/sc-recommend/SKILL.md:155,157` and `skills/sc-recommend/refs/delegation-vs-native-heuristics.md:38` (grep only) |
| ADV | `commands/sc/adversarial.md:181` (grep only) |
| TB | `skills/task-builder/SKILL.md:2405-2446` (TCS section only) |
| CV | `command-value-by-phase.md` (same parent folder as this directory, read fully) |
| V1 | `validation-oneoff-sc-task-vs-sc-implement.md` (read fully) |
| V2 | `validation-feature-task-builder-vs-sc-workflow.md` (read fully) |

## 1. Status and role

- Does: "Apply systematic improvements to code quality, performance, and maintainability" (IMP:3). Phase: Implement, as an off-pipeline hygiene step (CV:153); routing row `cleanup`, step 4 (HWW:318). Standalone-invokable, not retired. Not in any of the brief's five pipelines.
- Backing protocol skill `~/.claude/skills/sc-improve-protocol/` DOES NOT EXIST (`ls` exit 2; no skill folder with "improve" in its name under `~/.claude/skills/`). The command file names no skill (IMP:1-8), so it runs from its own file (HWW:232). Everything below comes from IMP plus the guide.
- Overlaps: `/sc:cleanup` (same guard rails, CV:154), `/simplify` (built-in, CV:156), `/sc:analyze` (reports; its own "Next Step" points here, ANA:111), and the level 3 / level 4 plan routes for anything beyond a small folder tidy (HWW:22, 168).

## 2. Flags

Usage line, the only place IMP lists flags: `/sc:improve [target] [--type quality|performance|maintainability|style] [--safe] [--interactive]` (IMP:22). No `argument-hint` frontmatter (IMP:1-8). Flags 5-7 below appear only in examples or boundaries, not in the Usage line.

| # | Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|---|
| 1 | `[target]` | a path or a name. Examples: `src/`, `api-endpoints`, `legacy-modules`, `auth-service` (IMP:65,73,81,89). The guide passes a folder: `src/billing/` (HWW:165) | not stated | Scope of analysis and edits (IMP:27). A FOLDER target is what the guide's exception to the 5-edit limit covers (HWW:22) | Always give one explicit folder so the whole `git diff` stays reviewable (J) | No target or the repo root: default not stated (UNVERIFIED). A single file expected to need more than 5 edits: the exception text says "on a folder", so it is not covered (HWW:22; reading, not a stated rule) |
| 2 | `--type` | `quality`, `performance`, `maintainability`, `style` (IMP:22) | not stated | Picks the pattern and persona: quality = debt then refactor; performance = profile then optimise; maintainability = structure then complexity then docs (IMP:55-57). Personas architect, performance, quality, security (IMP:7,44) | `quality` is the only value the guide uses (HWW:165, 318). `style` for format-and-naming only (J) | `performance` without a measured bottleneck: IMP:56 puts profiling first and names no tool (J). `security`: used in an example (IMP:89) but not in the enum (IMP:22), so unconfirmed |
| 3 | `--safe` | switch | off (not stated) | Named in Usage and examples (IMP:22,65-68 "safe refactoring application"). NO file read defines what it does. The guide makes it mandatory with `--type quality` in the `cleanup` row, step 4 (HWW:318 `mandatory_flags`) | Always when running under the guide (HWW:165, 318) | Treating it as a guarantee: undefined. The guide still says commit first "so every change can be undone" (HWW:163) |
| 4 | `--interactive` | switch | off (not stated) | Named in Usage and the `api-endpoints` example (IMP:22,73-76). Indirect definition only: the Approval Required list (IMP:117-123) and the guide: it "asks before complex changes, but some changes are applied automatically even then" - formatting, naming, unused variables, import order, simple type annotations (HWW:166; matches IMP:110-115) | Always; mandatory in `cleanup` step 4 (HWW:318). It is the main brake at MEDIUM | Reading it as a substitute for `git diff` review: the guide requires the review anyway (HWW:166, 318 step 5) |
| 5 | `--preview` | switch (example only) | n/a | Example: "Preview mode shows changes before application for review" (IMP:81-84). Not in Usage, not in the guide | MEDIUM band first pass, if the command really parses it (J) | Relying on it: UNVERIFIED that it is a parsed flag |
| 6 | `--validate` | switch (example only) | n/a | Example with `--type security`: "Comprehensive validation ensures security improvements are effective" (IMP:89-92). Not in Usage, not in the guide | none established | Relying on it: UNVERIFIED |
| 7 | `--force` | switch (named in a boundary only) | off | IMP:125-129: "Explicitly Will NOT (without `--force` flag)": make architectural decisions, refactor structure without confirmation, remove functionality. So `--force` lifts the guard rails | never under the guide's exception | Always avoid. If the change needs `--force`, it is HIGH band: use a task file (HWW:168) |

Does not exist in the command file (checked by reading all 130 lines): `--depth`, `--spec`, `--dry-run`, `--aggressive` (cleanup only, CLN:22), `--type code|imports|files|all` (cleanup only, CLN:22), `--handoff`, `--resume`, `--ledger`, `--output`, `--coverage`, `--no-promote`. Also: `/sc:implement` bans `--safe` (V1:79), so do not carry improve's flags over to it.

## 3. Scope x complexity matrix

The command DOES vary by complexity, because the guide draws a size line around it: it is the one allowed exception to the hard limit (more than 5 edits or more than one source file must go through a written plan), "run on a folder ... commit first and review `git diff` afterwards" (HWW:22). The exception is for "small, contained cleanups" (HWW:163). "Large refactors (many files or a structural change): treat it as a feature" with `/task-builder ... --spec` (HWW:168). No file gives a number for "small" or "large": the band edges below are JUDGMENT unless a cell cites a file.

Band definitions (one line each):

- LOW: only the auto-fix classes (formatting, naming, unused variables, import order, simple type annotations; IMP:110-115); one folder; no signature or public API change; the whole `git diff` can be read in one pass (J).
- MEDIUM: also needs an Approval Required class (logic refactor, signature change, change spanning several files; IMP:119-123), but stays inside one subsystem (counted the TCS way: first two path segments, TB:2411) and must not change behaviour; files can be named up front (HWW:22 "clear scope"). The MEDIUM/HIGH edge is J.
- HIGH: any of: structural or architectural change (IMP:119; IMP:105 says it will not without understanding system impact); two or more subsystems (TB:2411); removing code used by public APIs (IMP:122); risk areas (secrets, permissions, user input, paths, infrastructure); a driving spec or "must not drift" (HWW:18); performance work needing profiling (IMP:56); files that cannot be named up front. At HIGH the guide sends it to a task file (HWW:168).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL (J): folder-wide mechanical tidy, `--type quality --safe --interactive`. SKIP if it is one file and 5 edits or fewer: use a plain edit | OPTIONAL (J): `--type quality|maintainability --safe --interactive`, commit first, review diff | SKIP: not a one-off (HWW:168) |
| B bug fix | SKIP (J): a bug goes to `/sc:troubleshoot` (HWW:3.4, CV:175) | SKIP (J) | SKIP (J) |
| S single story | OPTIONAL: tidy the folder the story touched, before the commit; `--type quality --safe --interactive` | OPTIONAL (J): separate commit after the story's tests pass, never mixed into the story's own commit | SKIP: put the refactor in the plan: `/sc:workflow ... --depth quick` + `/sc:implement` if few files (HWW:17), else `/task-builder` + `/task` |
| F multi-story feature | OPTIONAL | OPTIONAL (J): one separate cleanup commit after the feature is built, never inside a `/task` phase | SKIP: `/task-builder --spec` + `/task` (HWW:168). A refactor-type task file scores S6=1 and is forced to `--depth deep` (TB:2415, 2438) |
| R multi-feature release | OPTIONAL (J), was SKIP | OPTIONAL (J), was SKIP | SKIP |
| N new product | SKIP (J) | SKIP (J) | SKIP (J) |

Notes on the matrix:

- No cell is REQUIRED or WORTH IT: no file makes it a step in any pipeline; it is never credited as an implement step.
- R: under ruling 2 a release includes plan, implementation and push, so the CV:139 reading ("a release only assembles work already built, build commands SKIP") no longer holds. For this command R now matches F's LOW/MEDIUM ratings (J); the HIGH cell stays SKIP because structural work belongs in a task file.
- N: nothing legacy exists yet to improve; a hygiene pass over built phases uses the F/R cells.

## 4. Choose this or the neighbour

| Neighbour | Decision rule | Cite |
|---|---|---|
| `/sc:cleanup` | Dead code, unused imports, empty blocks, redundant annotations: `/sc:cleanup <folder> --type code --safe --interactive`. Quality, naming, formatting, structure: `/sc:improve`. Order in the guide: `/sc:cleanup-audit`, commit, `/sc:cleanup`, `/sc:improve`, review `git diff`. Both auto-apply unused-import handling, so a second pass right after cleanup adds little for LOW (J) | HWW:318; CLN:109-115; IMP:110-115 |
| `/sc:analyze` | Target or type unknown, or you want a report first: `/sc:analyze <path> --focus quality|performance|...` (reports only), then improve. Target and type already known: skip analyze | ANA:111; HWW:144 |
| `/simplify` (built-in) | Code you just changed on this branch: `/simplify` works on the changed code and edits it before the commit. A folder you did not change: `/sc:improve` (J split; `/simplify` has no file, CV:156) | CV:156 |
| `/sc:workflow --depth quick` + `/sc:implement` | The improvement is a defined change in a few named files with testable acceptance criteria, or exceeds the folder-tidy sense of the exception: plan route. Do not hand `/sc:implement` improve's flags (`--safe` is banned there) | HWW:17, 22; V1:79 |
| `/task-builder --spec` + `/task` | HIGH band: structural, several subsystems, public API removal, risk areas, must not drift, or files not nameable up front. Refactor-type file gets TCS S6=1 and `--depth deep` | HWW:168; TB:2415, 2438; V2 "Complexity signals" |
| `/sc:troubleshoot --type performance` | A slow path already observed as a defect: diagnose first (file:line evidence), then fix by the size rules. `/sc:improve --type performance` is for undiagnosed general tuning, and its own pattern wants profiling first | CV:175; HWW:125; IMP:56 |
| `/sc:adversarial` | Only when two competing refactor plans exist; its file lists `/sc:improve` as "Compare improvement approaches" | ADV:181 |

After a run, the guide's normal exits apply: read `git diff` (HWW:166), commit, and `/code-review` before pushing (HWW:199). The command's own "Validate" step says it ensures functionality is preserved (IMP:30) but names no test run, so run the related tests yourself (J; `CLAUDE.md` says validation goes through `.github` Actions).

## 5. What a scheduled checker can see

Short answer: none, transcript plus git diff only.

| Where | Finding | Cite |
|---|---|---|
| Output file or folder | None defined. Flow step 5 says "Generate improvement summary and recommendations" with no path | IMP:31 |
| Ledger, frontmatter, return contract | None. Contrast `/sc:implement`, which writes `.dev/implement/<slug>/progress.md` | IMP (whole file); V1:106 |
| `.dev/` in this worktree | Observed 2026-10-27: folders `architectural brainstorms implement manual-qa plans pr-monitor reflect releases research reviews tasks troubleshoot`; no `improve` folder | `ls .dev` |
| Git history | `git log -i --grep="sc:improve"` returned no commits in this worktree (observed; absence is not proof the command was never run) | observed |
| Inferred pattern | A commit just before the run (guide: "commit first", HWW:163, 318 step 2), then a dirty tree with mechanical edits across several files in ONE folder, then a review and commit. UNVERIFIED: no run observed | HWW:163, 166 |
| Transcript | The invocation line and its flags. The routing table expects `--type quality --safe --interactive` for step 4 (HWW:318); the TodoWrite and Task delegation in IMP:50-51 are session-only | HWW:297, 318 |

## 6. Expected-step rule

- Never count `/sc:improve` as an expected step: no scope x band cell is REQUIRED or WORTH IT (section 3), and it is in none of the five pipelines. Its absence is fine at every scope and complexity. Do not credit it as the implement step for S or F (no spec trace, no ledger), nor as the test step.
- If it appears, treat it as a hygiene extra, not a pipeline step. Optional quality notes (not "skipped step" flags, all J): HIGH-band work done through it with no task file; no commit before the run (HWW:163); a run that used `--force` (IMP:125) or lacked `--safe --interactive` where the routing row wants them (HWW:318, transcript only).

## 7. Proposed changes to command-value-by-phase.md

Proposals only; CV line numbers as of 2026-10-27.

| # | CV line | Current text | Proposed text |
|---|---|---|---|
| 1 | 153, `/sc:improve` row, T/B/S/F/R/N cells | `SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| SKIP \| SKIP` | `OPTIONAL (J) \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL (J) \| SKIP`. T changes only because a folder-wide tidy is itself a one-off and is the case the guide's exception exists for (HWW:22): Ryan to confirm that reading. R changes under ruling 2 (R was SKIP under the "assembles built work" reading, CV:139) |
| 2 | 153, Notes | "Guide 3.7: commit first, `--safe --interactive`, review `git diff`. The one allowed exception to the five-edit limit" | "Off-pipeline hygiene step; never REQUIRED, never credited as the implement step. Guide 3.7 and routing row `cleanup` (HWW:318): after `/sc:cleanup`, run `--type quality --safe --interactive`, commit first, review `git diff`. The exception to the five-edit limit covers small, contained FOLDER cleanups only (HWW:22, 163); structural refactors go `/task-builder --spec` + `/task` (HWW:168). No file footprint. Backing protocol skill does not exist; `--safe`, `--interactive`, `--preview`, `--validate`, `--force` are not defined in any file read." |
| 3 | 139, R reading under 2.4 | "a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result" | Replace under ruling 2: R is a multi-feature release including plan, implementation and push, so implement-phase commands inside R follow the F ratings unless a row says otherwise. This affects every 2.4 row, not only `/sc:improve`: merge step to re-rate |
| 4 | after 241 (Section 3, O15) | none | Add O16 "Tidy or improve existing code": `/sc:cleanup-audit`, `/sc:cleanup`, `/sc:improve`, `/simplify`, `/sc:analyze`. Pick: folder tidy = audit, commit, cleanup, improve, review diff (HWW:318); code you just changed = `/simplify`; structural = task file (HWW:168). Reason: `/sc:cleanup` and `/sc:improve` share guard rails and auto-fix lists (CLN:109-115, IMP:110-115) |
| 5 | 259, "Skippable at every size" | list without hygiene commands | Add a line: "Never counted as a missing step: `/sc:improve`, `/sc:cleanup`, `/sc:cleanup-audit`, `/simplify`, `/sc:analyze`" (J; none is REQUIRED at any size) |
| 6 | 276, no-footprint row | lists `/code-review`, `/security-review`, `/sc:test`, `/sc:implement`, `/sc:git` | Add `/sc:improve`: "no output path defined (IMP:31); only the git diff and transcript; no `improve` folder under `.dev/` (observed 2026-10-27)" |
| 7 | Section 5 (add rows) | none | Add the unverified items 1-8 below (flags undefined, approval/exception conflict, missing protocol skill) |

## 8. Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| 1 | What `--safe` does, and its default | Listed in IMP:22 and examples (IMP:65-68), defined in no file read; no protocol skill exists | Run once on a throwaway folder, or find the repo source (`src/superclaude/...`) |
| 2 | What `--interactive` adds beyond the Approval Required list | IMP:108-123 reads as always in force; HWW:166 says auto-fix classes apply "even then". Whether the flag changes anything else is undefined | Same |
| 3 | Whether `--preview`, `--validate`, `--force` are parsed | Appear only in examples (IMP:81, 89) or a boundary line (IMP:125), not in Usage (IMP:22) | Same |
| 4 | `--type` default, and whether `--type security` is valid | Not stated; example at IMP:89 is outside the enum at IMP:22 | Same |
| 5 | "Rollback capabilities" and "backup" claims | IMP:38 and IMP:100 name them; no mechanism is described. The guide relies on commit-first (HWW:163) | Same |
| 6 | How a folder run behaves given "Changes affecting multiple files" needs approval (IMP:123) while the guide's exception is a folder run (HWW:22) | Both read; behaviour not observed. Likely means a prompt on every cross-file change | Same |
| 7 | Whether a single-file `/sc:improve` with more than 5 edits is inside the exception | HWW:22 says "run on a folder"; team practice unknown | Ryan's ruling |
| 8 | Band edges (what counts as "small, contained"; MEDIUM vs HIGH) | No file gives a number; all edges are J (section 3) | Ryan's ruling |
| 9 | Whether a run leaves any footprint | No run observed; `git log --grep` and `.dev/` listing found nothing (absence is weak evidence) | Run once, or inspect another engineer's repo |
| 10 | `/simplify` behaviour and the J split with `/sc:improve` | Built-in, no file (CV:156, CV U3) | Claude Code docs |
| 11 | `/sc:troubleshoot --type performance` flag list | Read only through CV:175 and HWW:125, not the command file | Read `commands/sc/troubleshoot.md` |
| 12 | Whether Context7 is required or the command degrades without it, and how personas activate | IMP:6-7,40-44 list them; no behaviour stated | Run without Context7, or read the repo source |
| 13 | Whether the routing-table tests check `/sc:improve`'s mandatory flags | HWW:297 says "checked by tests"; tests not found (same as CV U18) | Locate the tests in the IronClaude source |
| 14 | Whether other engineers' `~/.claude` copy of IMP matches this one | Home-directory files are per engineer (CV U17); installed copy only, repo source not read | Compare installs |
