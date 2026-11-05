# Command nuance: /sc:design

**Generated**: 2026-10-27 by the sc-design nuance agent (read-only analysis; only this file written)
**Brief**: `command-nuance/_brief.md` (rulings 1-5 apply; R means a multi-feature release)
**Focus**: when a single-pass design is enough versus `/tdd` or `bmad-architecture`, by complexity
**Citation keys**: DS = `~/.claude/commands/sc/design.md`; HW = `~/.claude/HOW-WE-WORK.md`; CV = `command-value-by-phase.md`; TDDC = `~/.claude/commands/sc/tdd.md`; TDDS = `~/.claude/skills/tdd/SKILL.md`; BA = `<repo>/.claude/skills/bmad-architecture/SKILL.md`; TB = `~/.claude/skills/task-builder/SKILL.md`; RS = `~/.claude/skills/sc-release-split-protocol/SKILL.md`; RSC = `~/.claude/commands/sc/release-split.md`; RH = `~/.claude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`; AR = `~/.claude/commands/sc/auggie-review.md`; HR = `~/.claude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`; OR = `~/.claude/skills/sc-workflow-protocol/refs/overlap-routing.md`; SC = `scenarios.md`

<!-- SECTION 1 -->
## 1. Status and role
- **What it does** (DS:3): "Design system architecture, APIs, and component interfaces with comprehensive specifications". One 110-line command file, `complexity: basic`, no personas, no MCP servers (DS:5-7). Five-step flow Analyze, Plan, Design, Validate, Document (DS:27-31). No waves, no gates, no sub-agents, no research step named.
- **Phase**: Spec (CV:65). **Not retired, standalone-invokable.** **No backing protocol skill**: `~/.claude/skills/sc-design-protocol/` does not exist (`ls` exit 2; glob `~/.claude/skills/sc-design*` empty, checked 2026-10-27). Per HW:232, a command whose file names no skill runs from its own file, so no skill-load line appears in a transcript.
- **Overlaps**: `/tdd` = `/sc:tdd` (HW:244; TDDC:183), `bmad-architecture` (CV:88, CV:229), `/sc:spec-panel` (critique, not a rival), `/sc:workflow` (downstream; workflow.md:76 lists `/sc:design` as "Architecture spec"). Called programmatically by `/sc:auggie-review` remediation Phase A (RH:63-78; AR:137). Named by `/sc:release-split` Part 3 as the default command for release specs (RS:270-275; RSC:134). Text-only suggestion from `/sc:brainstorm --handoff design` (HR:170-181).

<!-- SECTION 2 -->
## 2. Flags
Usage line (DS:22): `/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]`. That is the whole flag surface. No protocol skill exists to add more.

| Flag / argument | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `[target]` | A name (DS:59, 67, 75, 83) or, per callers, `@<file>` (HR:164, 175; OR:10; RH:68). Whether design.md handles `@file`: UNVERIFIED (U4) | none stated | Subject of the design; Analyze step "examine target requirements and existing system context" (DS:27) | Name one interface, component or schema; or pass the requirements/plan file a caller prints | Target is a whole product or several subsystems (use `/tdd` or `bmad-architecture`, section 4) |
| `--type` | `architecture`, `api`, `component`, `database` (DS:22) | not stated (U2) | Selects the pattern: system structure, RESTful/GraphQL interface, functional interface, schema (DS:49-52) | `api` or `component` for one new interface inside a spec file (HW:98 uses `--type api`) | `architecture` on a narrow job. RH:76 calls it the broadest type and uses it only because reviews span many concerns |
| `--format` | `diagram`, `spec`, `code` (DS:22) | not stated (U2) | Output shape: diagrams, specification text, interface code (DS:37, DS:102-107) | `spec` when the output goes into a spec file that `/task-builder --spec` or `/sc:workflow` will read (HW:98; RH:77 "text that sc:workflow / the task-builder can consume") | `code`: DS:75-77 shows interface code with "implementation guidance" but DS:98 says it will not generate implementation code, and the boundary is undefined (U6). `diagram` when a downstream tool must read the result as text |

**Do not exist in DS (people might assume):** `--depth`, `--tier`, `--handoff`, `--resume`, `--focus`, `--from-prd`, `--spec`, `--strategy`. Those belong to other commands: `--depth` and `--handoff` to `/sc:workflow` (workflow.md:7, 30-31); `--tier`, `--from-prd`, `--focus`, `--resume` to `/tdd` (TDDC:43-51). **`--output` is not defined in DS either, but `/sc:auggie-review` passes it** (`--output <output_dir>/remediation-spec.md`, RH:68-72), while AR:137 and AR:149 show the same call without it. Whether it is honoured: UNVERIFIED (U3).

Consequence: there is no `--depth` or `--tier`, so `/sc:design` cannot be made lighter or heavier. The complexity choice is made by picking a different command (sections 3 and 4).

<!-- SECTION 3 -->
## 3. Scope x complexity matrix
**Does the command vary by complexity? No.** It is one pass with no depth or tier control (section 2). What varies is whether one pass is enough, so the bands below describe the work, and the cells say whether `/sc:design` is the right tool or a heavier design command takes over. All band boundaries are JUDGMENT built from numbers that other files give for `/tdd` tiers and for task-builder's subsystem counting rule. No file sets a threshold for `/sc:design` itself.

| Band | Signals (all (J) as a combination) | File numbers borrowed |
|---|---|---|
| LOW | One interface, component or schema; author can name the files up front; under 5 relevant files; one subsystem; no driving spec; nobody else builds against it | `/tdd` lightweight "single service or component, narrow scope, <5 relevant files" (TDDS:71) |
| MEDIUM | Two or more interfaces, or one interface shared by two or more stories; 5-20 files; two subsystems; a short spec exists | `/tdd` standard "5-20 files, moderate complexity" (TDDS:72); subsystem = first 2 path segments (TB:2411) |
| HIGH | 20+ files, or several services, layers or integration boundaries; other people or teams build against the design; units built independently could choose incompatible shapes; "must not drift" | `/tdd` heavyweight "20+ files", "always Heavyweight" for multi-service/layer scope (TDDS:73, 80); HW:18, HW:244; BA:11 (the "could two units choose incompatibly" test) |

Cell = rating of `/sc:design` itself. Text after the dash says what carries the design step. Every cell is JUDGMENT `(J)` unless it cites a file for the cell's own claim.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP. Levels 1-2 contain no design step (HW:15-16); a plain edit plus its test (proposed one-off minimum, not yet confirmed by Ryan) | N/A (J). Needing a design for a new interface breaks the level-2 limit "more than 5 edits or more than one source file" (HW:22); the work is no longer T | N/A (J). Same reason |
| **B** bug fix | SKIP. Diagnosis is `/sc:troubleshoot` and `REPORT.md` (HW:123-128) | SKIP. A few files with clear scope go to `/sc:workflow --depth quick` from the REPORT (HW:132) | SKIP (J). Larger or riskier fix goes to `/task-builder` built from the REPORT (HW:133). A redesign discovered here is a new F, not a B step |
| **S** single story | SKIP. Levels 2-3 have no design step (HW:16-17); scenario S4 lists design as skippable (SC:29) | OPTIONAL (J). `--type api` or `--type component`, `--format spec` only if the story adds an interface that the story file does not already define; output goes into the story/spec file, not straight to the executor (RH:14) | SKIP /sc:design (J). If others build against the interface, the design step is WORTH IT (J) via `/tdd --tier lightweight`, or a `bmad-architecture` slice in the BMad lane (BA:15 "the one slice a feature touches") |
| **F** multi-story feature | SKIP (J). HW:98 asks for a short agreed spec file; design is named only "if it includes a new interface or API" | OPTIONAL. `/sc:design <name> --type api --format spec`, paste into the spec file, then `/task-builder --spec` (HW:98; HW:307 notes column). This is the one file-stated use | SKIP /sc:design as the design step (J). Stories that share an interface and must not drift (HW:18; `validation-feature-task-builder-vs-sc-workflow.md:155` items 2 and 5, itself marked JUDGMENT there) need `/tdd --tier standard\|heavyweight` or `bmad-architecture`. `/sc:design` may still draft one interface section inside that document (HW:98, HW:244) |
| **R** multi-feature release (re-rated, see section 7) | SKIP (J). Small features with named files already have per-feature specs | OPTIONAL (J). One shared cross-feature interface drafted as a spec section | WORTH IT (J) only when `/sc:release-split` approves a split: Part 3 says "Default to /sc:design for producing release specs" and writes `release-1-spec.md`, `release-2-spec.md` (RS:270-275, 306-310). Usually runs inside release-split, so the engineer may never type it. Without a split, the design step is per-feature `/tdd` or one `bmad-architecture` run (J) |
| **N** new product | OPTIONAL (J). Helper for one interface. The design step in the file-routed path is `/prd` then `/tdd` (HW:20, HW:309); `/tdd --tier lightweight` fits under 5 files | OPTIONAL (J). Helper only. Design step is `/tdd --tier standard` or `bmad-architecture` (REQUIRED at N per CV:88, csv required=true) | SKIP as the design step (J). A single pass cannot cover 20+ files or several services (TDDS:73, 80). `/tdd --tier heavyweight` or `bmad-architecture` carries it; `/sc:design` only for a single interface section |

<!-- SECTION 4 -->
## 4. Choose this or the neighbour
### 4.1 `/sc:design` versus `/tdd` (= `/sc:tdd`)

HW:244 gives the base rule: `/sc:design` drafts one design (an API, a component, a schema) in a single pass; `/tdd` writes a full technical design document from the template, with research and independent reviewers; use `/tdd` when other people will build against the design.

| Signal | Pick `/sc:design` | Pick `/tdd` (tier) |
|---|---|---|
| What is being designed | One interface, component or schema (HW:244; DS:49-52) | A component, service or system (TDDS:12, 39) |
| Relevant files | Under 5 and nameable up front (LOW) (J) | Lightweight under 5 files; standard 5-20; heavyweight 20+ or several services/layers (TDDS:71-73, 80) |
| Who builds against it | The author, or one agent in one session | Other people or teams (HW:244) |
| Claims must be code-verified | No research step is named in DS:27-31 and DS:42-45 | Yes: "every claim through codebase verification", analyst and QA gates, template conformance (TDDS:16, 24-29; TDDC:65) |
| A PRD drives it | No `--from-prd` flag | `/tdd --from-prd <path>` (TDDC:26, 51) |
| Footprint and cost | No output path, no folder (section 5) | `.dev/tasks/to-do/TASK-TDD-<timestamp>/` with `research/`, `synthesis/`, `qa/` and a final `docs/<domain>/TDD_<NAME>.md` (TDDS:86-111); runs through `rf-task-builder` then `/task` (TDDS:10, 353-386) |
| Tier default | n/a | "Default to Standard"; "If in doubt, pick Standard" (TDDS:67, 77) |

Rule (J): LOW goes to `/sc:design`; LOW with a wish for verified claims goes to `/tdd --tier lightweight`; MEDIUM goes to `/tdd --tier standard` unless the only new thing is one interface section (then `/sc:design`, OPTIONAL); HIGH goes to `/tdd --tier heavyweight`. They are not exclusive: TDDC:183 lists `/sc:design` as "complementary" for "architecture diagrams and API specs", so both can appear in one feature (the TDD for the whole, `/sc:design` for one interface section).

### 4.2 `/sc:design` versus `bmad-architecture`

| Signal | Pick `/sc:design` | Pick `bmad-architecture` |
|---|---|---|
| Lane | Task-file lane: next step is `/task-builder --spec` or `/sc:workflow` (HW:98, HW:307) | BMad lane: next step is `bmad-create-epics-and-stories`, or at epic altitude `bmad-create-story` (BA:76). CV:223: pick the lane at the Spec step and stay in it |
| What it produces | Diagrams, API specs, schemas, interface definitions (DS:102-107) | A lean "architecture spine" of invariants: paradigm, boundaries, state mutation, shared-data ownership. Stack, tree and full data shape are "seed", owned by code once it exists (BA:9) |
| Decision test | None stated | "If two units one level down built this independently, could they choose incompatibly?" Fix it only if yes, non-obvious and a real trade-off (BA:11). This is the HIGH signal (shared interfaces, drift) |
| Size handling | None | "A few decisions for a small thing, comprehensive for a platform; the whole system or the one slice a feature touches" (BA:15); altitude initiative, feature, epic (BA:29, 31, 60) |
| Cost | One pass | Coaching path is the default, with a mandatory purpose-and-audience question and a memlog, then a reviewer gate of parallel subagents (BA:21, 35-41, 58, 62-64). Fast path drafts with `[ASSUMPTION]` tags (BA:21); headless mode exists (BA:55) |
| Output home | Unspecified | `{planning_artifacts}/architecture/architecture-{project_name}-{date}/ARCHITECTURE-SPINE.md` per `customize.toml:54-55` (this repo's `_bmad-output/planning-artifacts/architecture/` exists) |

Rule (J): BMad lane at LOW or MEDIUM: neither is needed at S (CV:88 SKIP at S; story file is the handoff); at F-MEDIUM an interface section is optional via `/sc:design` only if the team is not using BMad epics. BMad lane at F-HIGH or N: `bmad-architecture` at the matching altitude, not `/sc:design`. `/sc:design` and `bmad-architecture` are not substitutes for interface text: the spine defers detail it cannot justify fixing (BA:9, BA:11).

### 4.3 Neighbours that are order, not alternatives

| Neighbour | Relation | Rule |
|---|---|---|
| `/sc:spec-panel` | Critique of a spec; spec-panel.md:462 says to incorporate feedback, then use `/sc:design` | Not a rival. No ordering requirement for a checker (HW:309 puts spec-panel after `/tdd`) |
| `/sc:adversarial --compare a.md,b.md` | Picks or merges competing designs (adversarial.md:179; CV:230) | Only when two real candidate designs exist: a HIGH signal. Otherwise SKIP |
| `/sc:workflow`, `/sc:implement` (downstream) | DS:109 says "Next Step: /sc:implement". RH:14 says a design spec is prose and "would collapse to one task", so the plan route puts `/sc:workflow` between spec and implement. HW:98 pastes the output into a spec file for `/task-builder --spec` | LOW, one task: straight to `/sc:implement` is acceptable (J). MEDIUM: `/sc:workflow --depth quick` on the spec (S) or `/task-builder --spec` (F). HIGH: `/task-builder --spec` |
| `/sc:brainstorm --handoff design`, `/sc:workflow --handoff design` | Print a recommendation only; "design is interactive, user-initiated, not auto-invoked" (HR:177; OR:10; brainstorm.md:159) | A printed `/sc:design ...` line in a transcript is a suggestion, not a run |
| `/sc:release-split` Part 3 | Default command for release specs after an approved split (RS:270-275) | Runs inside the release-split run; see R row of section 3 |
| `/sc:auggie-review` remediation | Phase A of an opt-in five-phase chain, gated on explicit user acceptance (RH:27-61, 63-84; AR:54) | Part of a review-remediation chain, not a Spec step. Count it as that chain, not as a design step |

<!-- SECTION 5 -->
## 5. What a scheduled checker can see
**Standalone run: none defined, transcript only.** DS names no output path, no frontmatter key, no ledger and no return contract; the "Output" block lists contents only (DS:102-107). There is no protocol skill that could add one (section 1). Observed 2026-10-27 in this repo: no `.dev/design*` folder, and a search of `.dev/tasks/to-do` for the string `sc:design` returned nothing. The only trace is the `/sc:design ...` text in a session transcript, and per HW:232 no skill-load line accompanies it.

| Context | Footprint a checker could look for | Source | Status |
|---|---|---|---|
| Feature route (F-MEDIUM) | A spec file containing a pasted interface section, e.g. `docs/specs/invoice-csv-export.md`. Indistinguishable from a hand-written spec | HW:98 | UNVERIFIED (example path only) |
| `/sc:auggie-review` remediation Phase A | `<output_dir>/remediation-spec.md` beside `REVIEW.md` | RH:68-72, 78 | UNVERIFIED (depends on `--output` being honoured, U3) |
| `/sc:release-split` Part 3 (split approved) | `<output>/release-1-spec.md`, `release-2-spec.md`, `boundary-rationale.md`; no split: `<output>/release-spec-validated.md` | RS:306-314 | UNVERIFIED whether `/sc:design` is actually invoked or the protocol writes them inline (RS:280 says "select the appropriate command") |
| Downstream trace | If the next step is `/task-builder --spec <that spec>`: the task file's `spec_path:` and `reflect_pre` block | `validation-feature-task-builder-vs-sc-workflow.md:91, 230` | Indirect proof that a spec existed, not that `/sc:design` made it |

A checker should therefore test for **a design or spec artifact on disk before the tasklist**, not for the command name (section 6).

<!-- SECTION 6 -->
## 6. Expected-step rule
- **`/sc:design` is never an expected step at any scope or complexity** (no cell is REQUIRED, section 3). A checker must not flag its absence, and must not flag its presence as a wrong step. Its absence is fine at T, B, S-LOW, F-LOW, R-LOW, and wherever a heavier design command is used instead.
- **What to expect instead (J):** at F-HIGH, R-HIGH and N-MEDIUM/HIGH, expect *a design artifact before the tasklist*: any of a `/tdd` output (`TASK-TDD-*` folder or `TDD_*.md`), a `bmad-architecture` spine (`ARCHITECTURE-SPINE.md`), a release-split spec, or a spec file with a design/interface section (scenario S5 "spec before tasklist", SC:36). Accept `/sc:design` as one valid producer only for a single interface section.
- **Short paths that are legitimate:** (a) `/sc:design` output going straight to `/sc:implement` when the work is one task (DS:109; RH:14 explains the per-task QA is lost for prose input); (b) a printed `/sc:design` suggestion from brainstorm or workflow that was never run (HR:177; OR:10); (c) `/sc:design` appearing inside the opt-in auggie remediation chain or inside release-split, which a user did not type as a Spec step (RH:63; RS:270-275).
- The "design" allowed-skip at S4 (SC:29) and "brainstorm or design" at S5 (SC:34) already agree with this: design is a one-of choice, not a fixed step.

<!-- SECTION 7 -->
## 7. Proposed changes to command-value-by-phase.md
Proposals only; `command-value-by-phase.md` is not edited.

| # | Location (CV line) | Current text | Proposed text | Why |
|---|---|---|---|---|
| 1 | CV:65, `/sc:design` row, ratings | `SKIP \| SKIP \| SKIP \| OPTIONAL \| SKIP \| OPTIONAL` (T, B, S, F, R, N) | `SKIP \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL (J) \| OPTIONAL`. **Only R changes: SKIP to OPTIONAL.** Section 3 adds that R-HIGH is WORTH IT (J) when a split is approved | R re-rated under the multi-feature-release definition: `/sc:release-split` Part 3 says "Default to /sc:design for producing release specs" (RS:270-275; RSC:134). The old SKIP fits a "release ships work already built" reading (the reading CV:139 states for the Implement phase). F and N keep OPTIONAL |
| 2 | CV:65, `/sc:design` row, Notes | "Single-pass draft of one API/component (guide section 5). Use for a new interface inside a spec file. ‡ with `/tdd`" | "Single-pass draft of one interface, API, component or schema (HW:244). No `--depth` or `--tier`, no protocol skill, no file footprint. Use `--type api\|component --format spec` for a new interface inside a spec file (HW:98). Never REQUIRED. By complexity: LOW one interface, `/sc:design`; MEDIUM `/tdd --tier standard`; HIGH (20+ files, several services, shared interfaces) `/tdd --tier heavyweight` or `bmad-architecture`. Also called by `/sc:auggie-review` remediation Phase A and `/sc:release-split` Part 3. ‡ with `/tdd`" | Adds the complexity layer and the callers |
| 3 | CV:229, O3 "Technical design", Why | "`/sc:design` is a single-pass draft of one interface; not a substitute for either" | Append: "Pick by size: one interface = `/sc:design`; component or service needing verified claims = `/tdd` (lightweight under 5 files, standard 5-20, heavyweight 20+ or several services, TDDS:71-73); BMad lane and shared-interface drift risk = `bmad-architecture`. Lane rule: stay in the lane chosen at the Spec step (CV:223)" | Gives O3 a complexity rule |
| 4 | CV:276, footprint row for commands with no stated footprint | "`/code-review`, `/security-review`, `/sc:test`, `/sc:implement` (beyond `progress.md`), `/sc:git`" | Add `/sc:design` to the list, and add a note: "only caller-supplied paths exist: `<output_dir>/remediation-spec.md` (auggie remediation), `<output>/release-1-spec.md` (release-split); verify with a spec/design artifact check, not the command name" | Section 5 of this file |
| 5 | CV:281, "What I read in full" | "For `/sc:troubleshoot`, `/sc:pr-submit`, `/sc:brainstorm`, `/sc:design`, `/sc:test`, ... I read only the usage and flag lines (grep)" | Remove `/sc:design` from that list; add "`/sc:design` read in full (110 lines, 2026-10-27); it has no backing protocol skill" | Corrects the read-depth statement |
| 6 | CV:7 / CV:48, definition of R | "release (R)" | Out of scope for this file: a global change. Every R cell in the whole file needs the same re-rating pass under the new definition | Brief ruling 2 |

No change proposed to CV:254-257 (minimum paths): `/sc:design` appears in none of them and is OPTIONAL at most, so a checker's minimum paths stay valid.

<!-- SECTION 8 -->
## 8. Unverified items
| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | What `/sc:design` actually reads and writes at run time, and where | Only DS (command file) exists; no backing protocol skill; read-only rule forbids running it | Read an existing run's transcript, or run it once in a scratch dir |
| U2 | Defaults for `--type` and `--format` when omitted | Not stated in DS:22 or anywhere read | Same |
| U3 | Whether `--output` is honoured | Not defined in DS:22; passed by RH:68-72 but absent from AR:137 and AR:149 | Run once with `--output`; or fix DS to document it |
| U4 | Whether `[target]` accepts `@<file>` | DS uses names (DS:59-83); callers pass `@file` (HR:164, 175; OR:10; RH:68) | Same |
| U5 | The claim "design is interactive / dialogue-heavy" | Made by brainstorm (HR:177; brainstorm.md:159); DS contains no interaction or question step (searched DS for "interactive" and "dialogue": no match) | Run once; or correct the brainstorm text |
| U6 | Meaning of `--format code` against "Will Not: generate actual implementation code" | DS:75-77 vs DS:98 conflict | Maintainer ruling |
| U7 | Whether `/sc:release-split` Part 3 invokes `/sc:design` or writes the release specs inline | RS:280 says "select the appropriate command"; no invocation line read | Read the rest of RS Part 3 and `refs/phase-templates.md` (not read) |
| U8 | Lightweight tier definition differs between files | TDDC:59 "Bug fixes, config changes, small features (<1 sprint), <5 relevant files" vs TDDS:71 "Single service or component, narrow scope, <5 relevant files". TDDC:150-154 says the skill holds the tier logic, so I used TDDS. TDDC:171-172 also names `/sc:prd`, which is not in `~/.claude/commands/sc/` | Maintainer ruling on TDDC text |
| U9 | All band boundaries and every `(J)` cell in section 3 | No file sets a complexity threshold for `/sc:design`; numbers are borrowed from `/tdd` tiers (TDDS:71-73) and task-builder's subsystem counting rule (TB:2411). TCS (TB:2402-2441) sets *reflect depth for a finished tasklist*, not a design choice, so I did not use it as a gate | Team agreement |
| U10 | `bmad-architecture` details beyond SKILL.md and `customize.toml:43-55` | `references/reviewer-gate.md`, `references/headless.md` and `assets/spine-template.md` not read in full | Read them |
| U11 | Whether this command is identical on other engineers' machines | `~/.claude/commands/sc/design.md` is home-directory only (file mtime Oct 22); same caveat as CV U17 | Compare `~/.claude` across engineers |
| U12 | Whether any real `/sc:design` run ever happened in this repo | Only a string search of `.dev/tasks/to-do` and a look for `.dev/design*`; session transcripts not searched | Search LiteLLM logs or transcripts for `/sc:design` |
