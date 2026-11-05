# /sc:tdd (= /tdd): scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: command file `/home/coder/.claude/commands/sc/tdd.md` (cited CMD), backing skill `/home/coder/.claude/skills/tdd/SKILL.md` (cited SK) and its five refs in `/home/coder/.claude/skills/tdd/refs/`: `build-request-template.md` (BR), `operational-guidance.md` (OG), `synthesis-mapping.md` (SM), `validation-checklists.md` (VC), `agent-prompts.md` (AP). Neighbours read in full: `/home/coder/.claude/commands/sc/design.md` (DES), `.claude/skills/bmad-architecture/SKILL.md` in the repo (BA, its `references/` not read), `/home/coder/.claude/HOW-WE-WORK.md` (HW). Also read: `command-value-by-phase.md` (CV) and `validation-feature-task-builder-vs-sc-workflow.md` (VAL). Repo evidence is cited by repo-relative path.

## 1. Status and role
- **What it does (CMD:3):** "Create or populate a Technical Design Document (TDD) for a component, service, or system": researches the code with parallel agents, then assembles the 28-section template with independent QA gates (SK:8-12; SM:36-117). It is the Technical Design Document, NOT test-driven development (CMD:11, CMD:156; HW:283).
- **Phase and status:** Spec phase (design step). Standalone-invokable, NOT retired. `/sc:tdd` and `/tdd` are the same skill (CMD:148-156 "invoke: Skill tdd"; HW:283). The command file, SK and all five refs name neither `/sc:task` nor `/sc:tasklist` (none seen in the full read); Stage B hands the built task file to `/task` (SK:411).
- **Overlaps:** `/sc:design` (one-pass draft of one design), `bmad-architecture` (invariants spine), partly `/tech-research` (research first) and the spec-file route of HW 3.2 (HW:98).

## 2. Flags
All flags are defined ONLY in the command file (CMD:43-51). A grep of SK and the five refs for `--tier`, `--resume`, `--from-prd`, `--prd`, `--focus`, `--output`, `--depth` returned nothing: the skill describes the same four inputs in prose (SK:37-48) and picks the tier itself (SK:226, SK:75-80). Whether the flags are honoured as written is therefore UNVERIFIED (U1).

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `<component>` (positional, required) | free text: component, service or system plus why | none | Becomes GOAL/WHY of the request (SK:39, SK:172-178). Topic-only input "will work but produces broader, less focused results"; no input at all gives agents "no context" (CMD:136-146). If it is too vague to search, the skill asks; otherwise it proceeds without quizzing (SK:50-61 vs SK:190) | Always: name the component and why a design is needed | A bare topic such as `"wizard"` |
| `--from-prd` / `--prd` (alias) | path to a PRD | none | Adds `research/00-prd-extraction.md` (SK:104; OG:101), traces every FR to a PRD epic (AP:189; VC:30 FR-trace check), inherits scope and sets `parent_doc` (OG:99-105). Without it PRD_CONTEXT is "N/A", a feature description is the requirements source (SK:44, SK:268) and FR rows are marked `[NO PRD TRACE]` (AP:189) | A PRD exists, from `/prd` or `bmad-prd`. Repo evidence: `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` has `parent_doc` pointing at a BMad PRD | The "PRD" is a stub with no epics or acceptance criteria (every FR will carry `[NO PRD TRACE]`) |
| `--tier` / `-t` | `lightweight`, `standard`, `heavyweight` | `standard` (CMD:46) | Codebase agents 2-3 / 4-6 / 6-10+, web agents 0-1 / 1-2 / 2-4, target lines 300-600 / 800-1,400 / 1,400-2,200 (CMD:57-61; SK:69-73); QA checks the line budget (VC:97) and requires SLO/SLI tables for Standard and Heavyweight only (AP:378). The BUILD_REQUEST encodes all seven phases and both QA gates whatever the tier (BR:98-160), so the tier changes size, not the gate structure (whether the builder trims Lightweight: U3) | Heavyweight when the design spans several services, layers or integration boundaries (SK:80) or the request says "detailed", "comprehensive", "thorough" (SK:78). Lightweight only when "genuinely narrow": single service, under 5 relevant files (SK:79) | Lightweight "to save time": the same phases run (BR:98-160). Also: CMD:59 lists "Bug fixes, config changes" under Lightweight, but SK:71 does not and HW routes bugs to `/sc:troubleshoot` (HW:311) |
| `--resume` / `-r` | path to the MDTM task file | none | Per CMD:28-29 resumes an interrupted session. The skill does this on its own: A.1 looks in `.dev/tasks/to-do/` for `TASK-TDD-*` with unchecked `- [ ]` items and skips to Stage B (SK:157-167); `/task` then continues from the first unchecked item (SK:149; OG:126) | After a crash or lost session; give the folder's task file | Starting over (the skill finds the prior folder anyway, SK:116) |
| `--output` / `-o` | path for the final TDD | auto: stub location if a stub exists, else `docs/[domain]/TDD_[COMPONENT-NAME].md` (SK:48, SK:111) | Where the assembler writes the TDD (BR:148; path rule SK:111) | The downstream reader expects another path. Observed TDDs sit at `.dev/releases/current/v2-m3/TDD_V2_M3.md`, `.dev/releases/complete/v1.3-2026Upgrade/TDD_VSCODE_AIDEV02.md`, `_bmad-output/planning-artifacts/tdd.md`, not under `docs/` | Never harmful; omit to take the default |
| `--focus` / `-f` | comma-separated directories or files | all | Bounds scope discovery and the research assignments (SK:46, SK:194-199); "saves significant time" (SK:46) | Whenever the directories can be named (the author "can name the files up front", a LOW-complexity signal) | Scenario B, where broad discovery is the point (SK:186-188, SK:198) |
| Keywords in the request (not flags) | "detailed", "comprehensive", "thorough"; multi-service, multi-layer scope | n/a | Force Heavyweight (SK:78, SK:80) | When you want the deepest run | When the scope is narrow: the keyword overrides it |
| BUILD_REQUEST `TEMPLATE: 01\|02` (set by the skill, not the user) | 01 simple, 02 complex | 02 ("almost always", SK:349) | Selects the MDTM template the builder uses (BR:17-19; SK:331-349) | n/a | n/a |

Short forms in CMD:43-51: `-t`, `-r`, `-o`, `-f`; `--prd` is an alias for `--from-prd`.

**Flags and behaviours that do NOT exist:**

- No `--depth`. The tier is the only depth control (`--depth` belongs to `/sc:workflow`, `/sc:troubleshoot`, `/sc:reflect`). No `--spec`, `--handoff`, `--type`, `--format` (those are other commands).
- No flag to skip, shorten or turn off QA gates, research or web research. CMD:175 lists "Skip investigation phases to produce faster but shallower output" under Will Not; web research is driven by gaps, not a flag (OG:17).
- `/sc:prd` is named at CMD:172 and CMD:182, but `/home/coder/.claude/commands/sc/` holds no `prd.md` (only `design.md` and `tdd.md` matched `prd|tdd|design`). The PRD step is `/prd` or `bmad-prd` (U5).
- No automatic hand-off flag. Phase 7 only asks the user whether to build implementation tasks (BR:158).

## 3. Scope x complexity matrix
**Does the command vary by complexity?** Yes, but only in size, not in structure. The one internal switch is the tier, chosen by relevant-file count and service/layer breadth (SK:69-80). The same seven phases and QA gates are encoded at every tier (BR:98-160). `/task-builder`'s TCS formula (task-builder SKILL lines 2410-2441) does NOT apply to `/tdd`: the TDD skill has no TCS and no `reflect` call (grep of SK for `TCS|reflect` found nothing). TCS applies later, to the task file built FROM the TDD.

**Bands for this command** (file counts and breadth are the only thresholds on disk, SK:71-73, SK:80; everything else is JUDGMENT):

| Band | Signals | Tier it maps to |
|---|---|---|
| LOW | under 5 relevant files, one service or component, author can name the files, no one else builds against it (SK:71; CMD:59) | `lightweight` |
| MEDIUM | 5-20 files, one subsystem, moderate complexity (SK:72) | `standard` |
| HIGH | 20+ files, or several services, layers or integration boundaries, or platform-scale (SK:73, SK:80); also "others will build against it" and "must not drift" (HW:20, HW:18) (J) | `heavyweight` |

**Cost note (my sum from BR, not a file statement):** every run spawns at least 7 fixed agents beyond research (Phase 3 analyst + QA: BR:121; Phase 5 analyst + QA: BR:142; Phase 6 assembler, structural QA, qualitative QA: BR:148-151), plus 2-3 or more codebase agents (CMD:59-61), at least one synthesis agent (SM:149-163), an optional PRD extraction item (BR:111) and a reuse-audit pass (SK:212). `/task` adds its own phase-gate QA on top (SK:414; VAL E2 gives "at least 6 agents" per phase after the first, TK:188-199, not re-read here). So even Lightweight is a heavy run; that is why LOW is mostly SKIP.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP | SKIP | SKIP (J: a HIGH one-off is not a one-off, reclassify; HW:22) |
| **B** bug fix | SKIP (HW:311 has no design step; CMD:59 names bug fixes under Lightweight, which conflicts) | SKIP | SKIP (J: a design-sized fix is an F; use `/sc:troubleshoot --fix`, HW:125-126) |
| **S** single story | SKIP (J: `/sc:design` for one interface, HW:98) | SKIP (J) | OPTIONAL (J) `--tier standard --from-prd <spec>` only if other engineers build against the story; a HIGH single story usually means it is really an F |
| **F** multi-story feature | SKIP (J: a short agreed spec file, HW:91-98) | OPTIONAL (J) `--tier standard --from-prd <spec> --focus <dirs>`: when stories share an interface and several people build, or no spec exists | WORTH IT (J) `--tier heavyweight --from-prd <prd> --focus <dirs>`: HW:20 "major feature that other people will build against", multiple services or layers (SK:80) |
| **R** multi-feature release | OPTIONAL (J) | WORTH IT (J) `--tier standard`: one release-level TDD for cross-feature interfaces plus sections 19, 24, 25 (rollout, release criteria, operational readiness: SM:90, SM:105, SM:108) | WORTH IT (J) `--tier heavyweight`; per-feature TDDs follow the F HIGH row. Input for `/sc:release-split` (HW:72, HW:309) |
| **N** new product | REQUIRED (HW:20, HW:309; band sets tier: `--tier lightweight` allowed for a tiny product, J) | REQUIRED `--tier standard --from-prd <prd>` | REQUIRED `--tier heavyweight --from-prd <prd>` (CMD:61 "New systems") |

Notes on the cells:

- N is REQUIRED because HW's `full-spec` route lists `/tdd` unconditionally (only steps 1 and 6 are marked optional, HW:309) and CV:68 already rates N REQUIRED. In the BMad lane the same step is `bmad-architecture` (CV:88), and the repo shows both were used together (section 4).
- N is greenfield, but the skill's discovery is codebase-first (SK:194-199) and CMD:173 forbids "architectural decisions without codebase evidence". How it behaves with no code to scan: U15.
- **R re-rating.** CV:68 rates R as SKIP. Under Ryan's definition (a multi-feature release includes the plan, the build and the push), design work for shared interfaces and rollout happens inside R, so SKIP is too low: proposed OPTIONAL at LOW, WORTH IT at MEDIUM and HIGH. All three are (J): no file rates `/tdd` for a release. CV:139 states the "release ships already built work" reading only for the Implement table; whether the /tdd row used it is unknown.

## 4. Choose this or the neighbour
**4a. `/tdd` vs `/sc:design`**

| Signal | Pick `/sc:design` | Pick `/tdd` |
|---|---|---|
| What is being designed | One interface (API, component, schema), `--type api\|component\|database\|architecture` (DES:22) | A whole component, service or subsystem (SK:72-73) |
| Who builds against it | The same engineer or one story; the output is pasted into a spec file (HW:98) | Other people (HW:244, HW:20) |
| Requirements to trace | None, or the prompt itself | A PRD with epics and acceptance criteria to trace requirement by requirement (SK:44; AP:189) |
| Evidence standard | Single pass; reads existing system context (DES:27) but describes no parallel research, verification tags or QA gates | Every claim code-verified with file:line, doc-only claims excluded, independent reviewers (OG:13-19, VC:117-118) |
| Downstream | `/sc:implement` per DES:109 (stale for F and above, see 4e) | `/roadmap`, `/task-builder --spec <TDD>` (roadmap SKILL:12, task-builder SKILL:41) |
| Size | Under 5 files and one interface (J) | 5 or more files (SK:72) |

Rule (J built from those rows): if you can name one interface and one reader, use `/sc:design` and put the result in a spec file; a Lightweight TDD still runs the full pipeline (section 3 cost note), so it rarely beats `/sc:design` plus a short spec. They stack rather than compete: CMD:183 calls `/sc:design` "complementary", and the TDD already contains diagrams (VC:101).

**4b. `/tdd` vs `bmad-architecture`**

| Signal | Pick `bmad-architecture` | Pick `/tdd` |
|---|---|---|
| Artifact | A lean spine of invariants: paradigm, boundaries, state ownership; "record decisions, not rationale" (BA:9, BA:17) | A full 28-section engineering spec: requirements, data models, API, testing, rollout; detailed enough to "begin implementation from the TDD alone" (OG:35; SM:36-117) |
| How decisions are made | Coaching by default: it elicits the invariants from the user (BA:21) | Autonomous research pipeline; "do NOT interrogate the user" (SK:190) |
| Brownfield | Reads real code to ratify existing conventions (BA:25) | Verifies every claim against code (OG:13-19) |
| Altitude | Scales: a few decisions for a small thing, comprehensive for a platform; initiative, feature or epic (BA:15, BA:29) | Scales by tier only (SK:69-73) |
| Lane | BMad lane; next step `bmad-create-epics-and-stories` (BA:76; CV:88, CV:116) | Task-file lane; next step `/roadmap` or `/task-builder --spec` (HW:309) |

Rule: when the invariants are still undecided, run `bmad-architecture` first. When they are decided and a detailed spec is needed (HIGH F, R, N), `/tdd` fills the detail. Repo evidence says they stack: `_bmad-output/planning-artifacts/tdd.md:4,14-18` describes itself as an "Engineering bridge document" with `parent_doc` `prd.md` and `depends_on` `architecture.md`, and `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` has a BMad PRD as parent. At LOW and MEDIUM pick ONE; at HIGH F, R and N both are legitimate. This contradicts CV:223 ("pick the lane at the Spec step and stay in it") for the design step.

**4c. `/tdd` vs the PRD step (`/prd`, `bmad-prd`) and the spec-file route.** The TDD takes a PRD as input (SK:44), so it is downstream, not an alternative. When requirements are already clear and the feature extends an existing system, HW 3.2 needs no PRD and no TDD: a short agreed spec file plus `/task-builder --spec` (HW:91-98, HW:307). That is the F LOW and often F MEDIUM answer.

**4d. `/tdd` vs `/tech-research`.** If you do not yet know how the current system works or whether the idea is feasible, research first (HW:19). The TDD researches the code too, but only to document a design, bounded by `--focus`. Feasibility question with no design wanted: `/tech-research`. Design wanted and the system is understood: `/tdd`.

**4e. What comes after a TDD (stale hints in CMD).** CMD:184 names `/sc:workflow` for "post-TDD implementation planning" and CMD:171 names `/sc:implement` for implementation. A TDD only appears at HIGH F, R or N, and VAL confirms `/task-builder` + `/task` is the minimum for a multi-story feature while `/sc:workflow` + `/sc:implement` is not eligible (VAL Verdict 1). So downstream of a TDD, a checker should expect `/roadmap` or `/task-builder --spec <TDD path>`, not `/sc:workflow`. BR:158 (Phase 7) offers to build implementation tasks "using the `/task` skill"; `/task` only executes files (HW:242), so the builder step is `/task-builder` (U6). Neither retired command (`/sc:task`, `/sc:tasklist`) is referenced by this command.

## 5. What a scheduled checker can see
Stated paths come from the skill files; "observed" means seen on disk in this repo today (read-only listing).

| Footprint | Where stated | Observed |
|---|---|---|
| Task folder `.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/` with the task file `TASK-TDD-*.md`, `research-notes.md`, `research/` (`00-prd-extraction.md`, `NN-<topic>.md`, `web-NN-*.md`, `reuse-audit.yaml`), `synthesis/`, `qa/`, `reviews/`, `gaps-and-questions.md` | SK:86-110, SK:212 | One folder: `.dev/tasks/done/TASK-TDD-20260429-203031/` holding `research-notes.md`, `research/00-05-*.md`, `qa/qa-combined-report.md`. No task file, no `synthesis/`, no `reuse-audit.yaml` inside it. Why it is in `done/` and what was removed: U9 |
| `research-notes.md` header lines `**Scenario:** A\|B` and `**Tier:** Lightweight\|Standard\|Heavyweight` | SK:252-258 template | Yes, in the observed folder (lines 3-5: Scenario A, Tier Heavyweight) |
| The TDD file: frontmatter `id: <X>-TDD`, `type: "📐 Technical Design Document"`, `status`, `parent_doc`, `depends_on`; body line `**Tier:**` | VC:44; SM:13-24; template `docs/templates/tdd_template.md:1-24` | Three TDDs: `.dev/releases/current/v2-m3/TDD_V2_M3.md` (1,405 lines, tier stated in body line 66), `.dev/releases/complete/v1.3-2026Upgrade/TDD_VSCODE_AIDEV02.md` (2,034 lines, `tier: Heavyweight` frontmatter line 10), `_bmad-output/planning-artifacts/tdd.md` (2,209 lines, no tier line found by grep). The `tier` key is not uniform |
| Default output path `docs/[domain]/TDD_[COMPONENT-NAME].md` | SK:111 | None of the three observed TDDs is there. The 2026-04-29 run's notes name `docs/docs-product/tech/vscode-aidev02/TDD_VSCODE_AIDEV02.md`, which was not found within five directory levels of the repo root |
| QA reports under `qa/` | SK:109-110 (`analyst-report-[gate].md`, `qa-report-[gate].md`); OG:86-88 (`analyst-[gate]-report.md`, `qa-[gate]-report.md`); BR:121, BR:142 (`qa-*-gate-report.md`), BR:149 (`qa-report-validation.md`) | Observed `qa/qa-combined-report.md` matches none. Three naming schemes disagree, so do not key on QA file names |
| Independent review file | none stated | `.dev/releases/current/v2-m3/TDD_V2_M3-review.md` (hand-run review against `docs/templates/tdd_template.md`) |
| Link to the next step: a downstream task file whose frontmatter `spec_path:` ends in `TDD_*.md` (or a `TDD:` field in a BUILD_REQUEST) | task-builder SKILL:41, 285 | UNVERIFIED (no task file observed) |
| `reflect_pre` / TCS / `.dev/reflect/` output | none: SK has no `reflect` or TCS text | not applicable to the TDD itself |
| Which `--tier` or flags were typed | none on disk | Transcript only |

What a checker can and cannot conclude:

- A TDD file proves a TDD exists, not that `/tdd` wrote it. Only one `TASK-TDD-*` folder exists against three TDD files, and `TDD_V2_M3.md` has a hand-run review next to it. The strong signal for "the command ran" is a `TASK-TDD-*` folder with `research-notes.md` showing `**Tier:**`; the weak signal is the document alone.
- Key on the folder prefix plus `research-notes.md`, not on QA report names or the TDD's location.
- The word "tdd" also appears in test file names (CMD:156 names `tests/cli/test_tdd_extract_prompt.py`). A transcript grep for "tdd" will produce false hits for test-driven development.

## 6. Expected-step rule
- **Count `/tdd` (or `bmad-architecture` in the BMad lane) as expected only at N, any band** (HW:309; CV:68). At HIGH F and at R MEDIUM/HIGH treat it as a soft expectation (J): do not flag its absence when a spec file, an existing architecture spine, or a PRD plus architecture pair covers the same scope (HW:98; section 4b), and never flag it as a skipped step at T, B, S, or F LOW/MEDIUM.
- **Its presence at T, B or S is over-process, not a violation**; a checker should note it, not fail it. If a TDD exists, the next expected step is `/roadmap` or `/task-builder --spec <TDD>`, not `/sc:workflow` (section 4e). Treat `/tdd` and `/sc:tdd` as one command, and ignore "tdd" hits that mean test-driven development.

## 7. Proposed changes to command-value-by-phase.md
Line numbers are in `command-value-by-phase.md` (CV). Proposals only; that file was not edited. Rows marked (J) are my judgment.

| # | CV line | Current text | Proposed text | Why |
|---|---|---|---|---|
| 1 | 68, `/tdd` row, columns T B S F R N | `SKIP \| SKIP \| SKIP \| OPTIONAL \| SKIP \| REQUIRED` | `SKIP \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| REQUIRED` (R changed, J) | R re-rated under Ryan's definition (planning is inside a multi-feature release). Section 3 gives the bands: R OPTIONAL at LOW, WORTH IT at MEDIUM and HIGH |
| 2 | 68, Notes | "Guide level 6. Not test-driven development. Use when others build against the design. ‡ with `bmad-architecture`" | "Guide level 6. Not test-driven development. Use when others build against the design. F: SKIP at LOW, OPTIONAL at MEDIUM, WORTH IT at HIGH (J). R: OPTIONAL / WORTH IT / WORTH IT (J). N: REQUIRED at every band, tier by band (`--tier`). Stacks with `bmad-architecture` (spine = invariants, TDD = full spec); at LOW and MEDIUM pick one. Even `--tier lightweight` runs the full 7-phase pipeline" | Sections 3 and 4b; SK:69-80; BR:98-160 |
| 3 | 88, `bmad-architecture` Notes | "... ‡ with `/tdd`" | Replace the double-dagger with "partly overlaps `/tdd`; repo evidence shows the TDD built after the spine (`_bmad-output/planning-artifacts/tdd.md:14-18`)" | Section 4b |
| 4 | 65, `/sc:design` Notes | "... ‡ with `/tdd`" | Replace with "overlaps `/tdd` for one interface only; stacks with it (CMD:183)" | Section 4a |
| 5 | 223 and 229 (O3 "Technical design", Section 3 intro) | "pick the lane at the Spec step and stay in it" / "`bmad-architecture` after `bmad-prd`, `/tdd` after `/prd`" | Add: "Not exclusive at the design step. `/tdd` consumed a BMad PRD in `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` and was written after `bmad-architecture` in `_bmad-output/planning-artifacts/tdd.md:14-18`. Both may appear at N and HIGH F; a checker must not flag `/tdd` after `bmad-prd`" | Section 4b |
| 6 | 240 (O14) | "`/tdd` and `/sc:tdd` ... Pick `/tdd`" | Add: "A checker treats them as one command and must not match 'tdd' in test-driven-development contexts" | CMD:156; section 5 |
| 7 | 254-257 minimum paths, N row task-file lane step 3 | "3. `/tdd`" | "3. `/tdd --from-prd <prd> --tier heavyweight` (BMad lane: `bmad-architecture`)" | Section 2, 3 |
| 8 | 256 (Release row, WORTH IT additions) | no `/tdd` | Add "`/tdd` (MEDIUM and HIGH: one release-level TDD or per-feature TDDs; input to `/sc:release-split`)" (J) | R re-rating; HW:72 |
| 9 | 255 (Multi-story feature row, WORTH IT additions) | no `/tdd` | Add "`/tdd` at HIGH complexity (20+ files, several services or layers, others build against it) (J)" | SK:73, SK:80; HW:20 |
| 10 | 263-276 footprint table | no `/tdd` row | Add: "`/tdd`: folder `.dev/tasks/to-do/TASK-TDD-*/` (`research-notes.md` with `**Tier:**`, `research/`, `qa/`) plus the TDD file with frontmatter `type: \"📐 Technical Design Document\"` and `parent_doc`. Observed: 1 `TASK-TDD` folder (in `done/`, no task file) against 3 TDD files; location and QA file names vary, so the document alone does not prove the command ran" | Section 5 |
| 11 | 110 (`/sc:workflow` row Notes; the hint comes from CMD:184) | no mention of TDD | Add to the note: "CMD:184 recommends `/sc:workflow` after a TDD; for a TDD-sized feature use `/task-builder --spec <TDD>` (VAL)" | Section 4e |
| 12 | 281 (Section 5 intro) | Lists the files read in full and those read only by grep; `/tdd` is in neither list (only its frontmatter was read) | Add: "`/sc:tdd` command file, the `tdd` skill and its five refs were read in full (nuance file `sc-tdd.md`); its flags are defined only in the command file (U1)" | This file |

R re-rating summary for `/tdd`: SKIP becomes OPTIONAL in the table cell, with WORTH IT at MEDIUM and HIGH inside the Notes. Everything else in the row is unchanged.

## 8. Unverified items
| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | Whether the skill honours `--tier`, `--from-prd`, `--prd`, `--resume`, `--output`, `--focus` | Defined only in CMD:43-51; SK and refs never name them (grep empty). The model reads them from the command text | A dry run, or add the flags to SK:35-61 |
| U2 | Tier wording conflict | CMD:59 puts "Bug fixes, config changes, small features (<1 sprint)" under Lightweight; SK:71 says "Single service or component, narrow scope". CMD:60 and SK:72 also word Standard differently | Maintainer decision on which text wins |
| U3 | Whether the builder trims any phase or gate at Lightweight | BR:98-160 encodes all phases for every tier; the `rf-task-builder` agent file was not read | Read `/home/coder/.claude/agents/rf-task-builder.md` or a Lightweight task file |
| U4 | Which TDD template is used on an engineer machine | SK:12 and SK:112 name `src/superclaude/examples/tdd_template.md`; it was not found under `~/.claude` or this repo (find, depth 6). Two other copies exist and differ: `docs/templates/tdd_template.md` (1,240 lines) and `/home/coder/.claude/templates/documents/tdd_template.md` (1,310 lines). The V2-M3 review used the repo copy (`.dev/releases/current/v2-m3/TDD_V2_M3-review.md:6`) | Check for the source file in an IronClaude checkout; diff the two copies |
| U5 | `/sc:prd` | Named at CMD:172 and CMD:182; no `~/.claude/commands/sc/prd.md` exists. The `prd` skill (`/prd`) does exist | Fix the two lines in CMD, or add the command |
| U6 | What Phase 7 does when the user says yes to "create implementation tasks using the `/task` skill" (BR:158) | `/task` runs files (HW:242); the builder is `/task-builder`. Not run | A dry run, or reword BR:158 |
| U7 | `/task` phase-gate agent counts ("at least 6") | Taken from VAL E2 (TK:188-199); `/task` SKILL not re-read for this file | Read `/home/coder/.claude/skills/task/SKILL.md` |
| U8 | Which QA file names are real | Three schemes in SK:109-110, OG:86-88, BR:121-149; observed `qa-combined-report.md` matches none | Inspect a fresh run's `qa/` |
| U9 | Why `.dev/tasks/done/TASK-TDD-20260429-203031/` has no task file or `synthesis/`, and what moved it | Only the folder listing was seen; no git history checked | `git log` on that path |
| U10 | Which command produced `_bmad-output/planning-artifacts/tdd.md` (2,209 lines) and `TDD_V2_M3.md` | No `TASK-TDD` folder accompanies either; `TDD_V2_M3.md` has a hand-run review next to it | File headers, git log, ask the authors |
| U11 | `bmad-architecture` default output path and its reviewer gate | BA:60 uses `{workflow.spine_output_path}`; `customize.toml` and `references/` not read | Read them |
| U12 | Whether `rf-task-builder` adds `reflect_pre` or `reflect_post` blocks to a `TASK-TDD` task file | SK has no `reflect` text; agent file not read | Read the agent file or a built task file |
| U13 | `/sc:design` output path and whether it writes a file | DES:44 lists Write as a tool; no path is stated | Run once, or ask the maintainers |
| U14 | Cost and duration of a TDD run | No file states them; the section 3 count is my sum from BR | Count spawns in an existing `TASK-TDD` folder |
| U15 | Behaviour at N when there is no code to scan | SK:194-199 and CMD:173 assume codebase evidence; a greenfield product has none | A run on a greenfield request, or maintainer statement |
| U16 | Whether every engineer has the same `~/.claude/skills/tdd` | Per-user directory (CV:23); this check reflects this machine only | Compare installs |
| U17 | All (J) cells in section 3 (S HIGH, F, R, N tier-by-band) and the proposed R re-rating | No file gives a threshold or rating for them | Team agreement |
