# Command nuance: /sc:roadmap

**Generated**: 2026-10-27 by the nuance agent for `/sc:roadmap` (read-only; only this file written)
**Brief**: `command-nuance/_brief.md`. **Scopes**: T one-off, B bug fix, S single story, F multi-story feature, R multi-feature release (Ryan's 2026-10-27 definition), N new product.
**Path keys** (all under `/home/coder/.claude` unless stated):
- `CMD` = `commands/sc/roadmap.md` (105 lines, read in full)
- `PRO` = `skills/sc-roadmap-protocol/SKILL.md` (543 lines, read in full)
- `R-SC` = `skills/sc-roadmap-protocol/refs/scoring.md`; `R-VAL` = `.../refs/validation.md`; `R-TPL` = `.../refs/templates.md`; `R-ADV` = `.../refs/adversarial-integration.md`; `R-EXT` = `.../refs/extraction-pipeline.md` (all five read in full)
- `RM` = `skills/roadmap/SKILL.md` (the `/roadmap` task-file skill; 2678 lines; read lines 1-200 and 2610-2678 plus grep of the rest)
- `TLC` = `commands/sc/tasklist.md`; `TLP` = `skills/sc-tasklist-protocol/SKILL.md` (Stage 9 and 10 read; rest grepped)
- `HW` = `HOW-WE-WORK.md` (read in full); `TB` = `skills/task-builder/SKILL.md` (TCS lines 2406-2443 only)
- `CV` = `command-value-by-phase.md`; `VF` = `validation-feature-task-builder-vs-sc-workflow.md` (both read in full)
- Repo files are cited from `/home/coder/workspaces/worktrees/Coder/IB-CPlus-01` as `repo:<path>`.

<!-- SECTION 1 -->
## 1. Status and role

- **What it does**: "Generate roadmap pipeline artifacts from 1-3 specification, TDD, and PRD markdown inputs. Mirrors the CLI `superclaude roadmap run` surface" (CMD:3). Output is `roadmap.md`, `extraction.md`, `test-strategy.md` plus per-step files; it "will not" generate tasklists, execute implementation, or trigger downstream commands (CMD:98; PRO:38, PRO:458-466).
- **Phase and status**: Tasklist phase (planning artifact; CV row 113). STANDALONE-INVOKABLE and NOT retired under Ryan's rulings (only `/sc:task` and `/sc:tasklist` are retired). Its backing skill `sc:roadmap-protocol` is never run directly (PRO:21, PRO:28). Its designed next steps, `/sc:validate-roadmap` and `/sc:tasklist` (CMD:102-103), leave it with no sanctioned downstream in this team's pipeline (see section 4).
- **Overlaps**: `/roadmap` (a different thing with a similar name, section 4), `/task-builder`, `/sc:workflow`, `/sc:release-split` (runs before it), `/sc:validate-roadmap` (runs after it). Observed use in this repo: one full run on 2026-05-17 (section 5).

<!-- SECTION 2 -->
## 2. Flags

**The command file and the protocol skill disagree on the flag surface.** CMD is the CLI-mirroring list (CMD:7, CMD:92: "preserve CLI-faithful behavior"); PRO is an older design that still documents flags CMD lists as unsupported (CMD:46-48 vs PRO:67-82). The table follows CMD; every conflict is marked CONFLICT. The "worth using / avoid" columns are JUDGMENT (J) unless a file is cited.

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `INPUT_FILES...` | 1-3 markdown files; at most one spec, one TDD, one PRD, any order | required | Type auto-detected: PRD scorer first (>=5), then TDD (>=5), else spec (CMD:19, CMD:25; R-SC:9-15). PRD/TDD content enriches extraction (personas, metrics, scope, data models) but not the complexity score (R-EXT:289-307; R-SC:215-219) | Pass all of spec + TDD + PRD that exist: the full-spec route (HW:51-77) produces PRD and TDD, so both are available at N | Passing two files of one kind. A borderline detection score of 3 to 6 prints a warning (R-SC:15): then set `--input-type` |
| `--agents` | `model[:persona]`, comma list | `opus:architect,sonnet:architect` (CMD:27) | Two generator steps, then `diff -> debate -> score -> merge` (PRO:111-137; R-ADV:68-75) | Keep default (J) | A longer list: PRO says 2-10 agents with an orchestrator at 3+ (PRO:84, PRO:248) but CMD and the CLI default to 2. CONFLICT. Observed state file shows a third generator `haiku-architect` that FAILED (repo:`_bmad-output/planning-artifacts/.roadmap-state.json`) |
| `--output PATH` | directory | parent dir of the first input (CMD:19, CMD:27) | Where every artifact lands. CONFLICT: PRO:71 says `.dev/releases/current/<spec-name>/` | Always set it explicitly to a release folder (J), so the checker finds it | Relying on the default: the observed run wrote next to `tdd.md` in `_bmad-output/planning-artifacts/`, matching CMD (repo `.roadmap-state.json` `spec_file`), not PRO |
| `--depth` | `quick`, `standard`, `deep` | `standard` | Debate rounds 1 / 2 / 3, inside the single `debate` step (CMD:28; R-ADV:25-31) | `deep` when HIGH complexity and variants differ (the observed run used `deep`, repo `.roadmap-state.json`) | `deep` on small input: only the debate step gets longer (J) |
| `--resume` | boolean | false | Skip steps whose outputs already pass their gates; re-run from the first failing step (CMD:29). State is `.roadmap-state.json` (R-EXT:307). CONFLICT: PRO has `--resume-from <adversarial dir>` (PRO:81), a different mechanism (R-ADV:81) plus a Serena session-resume prompt (PRO:436-441) | After a halt on the same inputs | After editing the spec: whether the CLI checks the stored `spec_hash` is UNVERIFIED (PRO:439 checks it in skill mode only) |
| `--dry-run` | boolean | false | CMD: print step plan and gate criteria, exit, no subprocesses (CMD:30). PRO: run Waves 0-2 then print a preview (PRO:272). Not identical | First run on any new input (J): free | Never harmful |
| `--model TEXT` | model id | per-agent model (CMD:31) | Overrides the model for all steps | Cost control (J) | Mixed-model debate is the point of the default two agents (J) |
| `--max-turns` | integer | 100 (CMD:32) | Cap per Claude subprocess | Raise if a step times out (J) | - |
| `--debug` | boolean | false | Writes `output_dir/roadmap-debug.log` (CMD:33) | Diagnosing a halt | - |
| `--no-validate` | boolean | false | Skips post-pipeline validation (CMD:34). PRO also writes `validation_status: SKIPPED`, `validation_score: 0.0` (PRO:78, R-VAL:347-352) | Throwaway exploration (J) | R and N: it removes the only gate-checked review of the roadmap (J) |
| `--allow-regeneration` | boolean | false | Allows patches over the diff-size threshold (FR-9); "use with caution" (CMD:35). Threshold value is not stated in any file read | Rare | Default |
| `--no-convergence` | boolean | false | Turns off the spec-fidelity convergence engine; single-shot LLM check instead (CMD:36). PRO:137 says the convergence-aware gate is the fail-closed replacement for the old bypass | Never on R or N (J) | Always (J). Interaction with the gate: UNVERIFIED |
| `--retrospective PATH` | file | none | Prior release-cycle retrospective; a missing file is not an error (CMD:37) | When a prior release has one (J) | - |
| `--input-type` | `auto`, `tdd`, `spec` | `auto` | Forces the type for a single file; PRD stays auto-detected (CMD:38). TDD uses a different extract prompt with 6 extra sections (R-EXT:212-225) | Detection warning shown (R-SC:15) | Multi-file input |
| `--tdd-file PATH` | file | none | Supplementary TDD when the primary is a spec: data models, endpoints, components, test strategy (CMD:39) | Spec primary plus a TDD | Primary is already a TDD (ignored, CMD:39) |
| `--prd-file PATH` | file | none | Supplementary PRD: personas, metrics, compliance, scope; auto-wired from `.roadmap-state.json` on `--resume` (CMD:40) | Spec or TDD primary plus a PRD | - |
| `--no-compress` | boolean | false | Stops lossless markdown compression of the LLM-read inputs; deterministic steps already read originals (CMD:41). Observed run's `roadmap.md` cites `tdd.compressed.md` (repo) | Debugging a fidelity finding (J) | - |
| `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` | toggle | enabled | Auto-fix pure-cosmetic gate failures (11 deterministic transforms C1-C11); semantic failures always halt (CMD:42; R-VAL:104-146) | Default | `--no-...` on high-stakes runs (J) |
| `--strict-no-remediation` | boolean | false | Alias for `--no-allow-cosmetic-remediation` (CMD:43; R-VAL:113) | High-stakes runs | - |
| `--help` | - | - | CLI help (CMD:44) | - | - |

**Flags that do not exist (people may assume them):**

| Assumed flag | Evidence |
|---|---|
| `--specs`, `--template` / `-t`, `--multi-roadmap`, `--interactive` / `-i`, `--compliance` / `-c`, `--persona` / `-p` | CMD:46-48 says unsupported. CONFLICT: PRO:67-82 and PRO:5 (`argument-hint`) still document all of them. Behaviour of an engineer typing one: UNVERIFIED |
| `--validate` / `-v` | In PRO:77 only. Not in CMD's flag table or its unsupported list. Not defined in CMD |
| `--resume-from` | In PRO:81 only. Not in CMD. Not defined in CMD |
| `--spec`, `--tasklist`, any "emit tasklist" flag | None. CMD:98 "Will not: generate tasklists" |
| `--depth` meaning task-builder's TCS bands | `--depth` here is debate rounds only (R-ADV:25-31); TCS is task-builder's (TB:2406-2441) |

<!-- SECTION 3 -->
## 3. Scope x complexity matrix

**Does the command vary by complexity?** Its OUTPUT does: the pipeline scores the input and sets milestone count and test interleave from the score (R-SC:98-104). The DECISION TO RUN it barely does: no pipeline Ryan listed names it, and the team guide routes everyone to `/roadmap` "unless your lead says otherwise" (HW:245). So the matrix is nearly flat on purpose.

**Bands for this command** (the only on-disk formula is the command's own input score, computed by the run itself, so an engineer cannot read it before running; the pre-run proxies are JUDGMENT):

| Band | On-disk definition | Pre-run proxy (J) |
|---|---|---|
| LOW | `complexity_score` < 0.4: 3-4 milestones, validation 1 per 3 work milestones (R-SC:100-102) | One spec, one subsystem, under about one session of work per milestone |
| MEDIUM | 0.4 to 0.7: 5-7 milestones, 1 per 2 (R-SC:103) | Several domains or a TDD with data models and APIs; clear dependency order |
| HIGH | above 0.7: 8-12 milestones, 1 per 1 (R-SC:104) | Spec + TDD + PRD, many requirements, deep dependency chains, security or infrastructure risk. Observed: AIDev02 GA scored 0.85 HIGH (repo:`_bmad-output/planning-artifacts/roadmap.md` frontmatter) |

The score formula weights requirement count (/50), dependency depth (/8), domain spread (/5), risk, and spec line count (/1000) (R-SC:76-82). This is NOT task-builder's TCS (TB:2406-2441); TCS does not apply to this command.

| Scope | LOW | MEDIUM | HIGH | Flag set when run |
|---|---|---|---|---|
| T one-off | SKIP | SKIP | SKIP | - |
| B bug fix | SKIP | SKIP | SKIP | - |
| S single story | SKIP | SKIP | SKIP | - |
| F multi-story feature | SKIP | SKIP | SKIP (J) | A feature that scores HIGH is probably an R: re-scope before reaching for this (J) |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | OPTIONAL (J) | `--dry-run` first, then `--output <release dir> --depth standard` (MEDIUM) or `--depth deep` (HIGH); give every spec/TDD/PRD; keep validation on (J) |
| N new product | SKIP (J) | OPTIONAL (J) | OPTIONAL (J) | Same as R. N always has PRD and TDD in hand (HW:51-77), so enrichment inputs exist (J) |

Why OPTIONAL and not WORTH IT at R and N: the output stops at roadmap documents; `/sc:tasklist`, its designed consumer, is retired, so a human must carry the result to `/task-builder` or `/roadmap` (section 4). The deterministic gates, two-agent debate and fail-closed spec-fidelity convergence (PRO:137, PRO:157) are a real advantage over `/roadmap` for the roadmap document only (J).

**R re-rating under the multi-feature-release definition.** CV rated `/sc:roadmap` R = OPTIONAL (CV:113) under a reading where a release "assembles and ships work already built" (CV:139). Under Ryan's definition (full release plan, implementation, push) planning commands do matter at R. Result for this command: R stays OPTIONAL at MEDIUM/HIGH and becomes SKIP at LOW (J). Changed: the reason, not the rating.

<!-- SECTION 4 -->
## 4. Choose this or the neighbour

### 4.1 `/sc:roadmap` versus `/roadmap` (same word, different tools)

`/roadmap` is the task-file skill at `~/.claude/skills/roadmap/SKILL.md`; `/sc:roadmap` is the command at `~/.claude/commands/sc/roadmap.md`. They share a name and nothing else on disk.

| Dimension | `/sc:roadmap` | `/roadmap` | Source |
|---|---|---|---|
| What it is | Slash command that loads `sc:roadmap-protocol`; mirrors the Python CLI `superclaude roadmap run` (14 gated steps) | Skill that is "a pure orchestrator": composes `/task-builder` and `/task` | CMD:92; PRO:111-126; RM:8 |
| Input | 1-3 markdown files: spec, TDD, PRD | Anything: PRD, TDD, free-form prompt, any document | CMD:19; RM:60 |
| Output | `roadmap.md`, `extraction.md`, `test-strategy.md`, plus diff, debate, score, fidelity and remediation files | Roadmap document, one BUILD_REQUEST per phase, one executable MDTM task file per phase (Deep tier) under `.dev/tasks/to-do/TASK-ROADMAP-*/` | PRO:46-50, PRO:113-126; RM:8, RM:130-143 |
| Depth control | `--depth` = debate rounds 1/2/3 only | Quick = roadmap only; Standard = roadmap + BUILD_REQUESTs; Deep = + task files. Default Deep; "if in doubt, pick Deep" | CMD:28; RM:102-114 |
| Quality checks | Per-step deterministic gates, spec-fidelity convergence, optional two-agent debate | Lens-based QA across 4 stages, 44-48 evaluating agents at minimum | R-VAL:7-74; RM:27 |
| Dry run | Prints step plan and gate criteria | Phase plan summary, asks "Proceed? (y/n)" | CMD:30; RM:2614-2644 |
| Next step | `/sc:validate-roadmap`, then the RETIRED `/sc:tasklist` | `/task <phase task file>` per phase | CMD:102-103; RM:8 |
| State file | `.roadmap-state.json` with `spec_file`, `spec_hash`, `agents`, `depth`, `steps{}` (observed) | `.roadmap-state.json` with `input_hash`, `input_paths`, `roadmap_status`, `task_files_created` | repo `.roadmap-state.json`; RM:579 |
| Guide's rule | "Separate release pipeline... Use `/roadmap` unless your lead says otherwise" | The full-spec step 7 | HW:245; HW:74-77 |

**Decision rule by scope.**
- **N (new product)**: `/roadmap`. It is step 7 of the full-spec route and its output is the thing `/task` runs (HW:74-84, routing row `full-spec`, HW:309). `/sc:roadmap` is OPTIONAL and only "if the lead says otherwise" (HW:245).
- **R (multi-feature release)**: `/roadmap` when the release needs executable per-phase task files; `/task-builder` per feature when the features are already specified (J; `/task-builder` is the validated F minimum, VF). `/sc:roadmap` only if the lead asks for the CLI pipeline's adversarial roadmap and accepts a manual hand-off afterwards.
- **F and below**: neither. Use `/task-builder` + `/task` (F) or `/sc:workflow` + `/sc:implement` (S), per the validation files.
- **Trap**: do not run both on the same inputs; the double-dagger in CV:113 marks that as waste, but the two do NOT do the same job (only `/roadmap` ends in runnable files). A checker that sees both should not treat one as a substitute for the other.
- **Stale cross-reference**: `TB:1668` says "`/sc:roadmap` invokes `/task-builder`". Neither CMD nor PRO does; `/roadmap` is the one that does (RM:8, RM:660). Treat the TB line as a mix-up.

### 4.2 Neighbours in one line each

| Neighbour | Rule |
|---|---|
| `/sc:release-split` | Runs BEFORE any roadmap. If it recommends a split, give the Release 1 spec to the roadmap command, not the whole TDD (HW:70-72). "Do not split" is a normal answer. |
| `/sc:validate-roadmap` | Runs AFTER `/sc:roadmap`, same pipeline only (HW:284; CV:125). `/roadmap` runs its own QA, so never pair it with `/roadmap` output. |
| `/task-builder` (+ `/task`) | The sanctioned tasklist step at F, and per feature inside an R (VF verdict). Whether it accepts a `/sc:roadmap` `roadmap.md` as `--spec` or goal context is UNVERIFIED (spec resolution in VF E4: flag, `@file`, BUILD_REQUEST field). |
| `/sc:workflow` | S-size only. It does not read a roadmap. |

### 4.3 What the `/sc:tasklist` retirement means for this pipeline

Ruling (brief item 3): `/sc:task` and `/sc:tasklist` are retired and never recommended as an engineer step. No file on disk records this: TLC has no deprecation text (grep for "retire" and "deprecat" in TLC, TLP and the sc-task files found nothing relevant), and `/sc:roadmap` still points at it. The ruling is Ryan's, not a file's.

1. **The designed pipeline loses its terminal step.** PRO:36 says `spec(s) -> sc:roadmap -> roadmap artifacts -> (user triggers) -> future tasklist command -> (user triggers) -> sc:task`. CMD:103 lists `/sc:tasklist` under See Also. PRO:383-385 names the "future tasklist generator" as consumer of `roadmap.md` and `test-strategy.md`; `estimated_phases` is "a hint for future tasklist generator" (R-TPL:394); the validate gate requires a `tasklist_ready` field (R-VAL:32). Those are now dead ends.
2. **`/sc:roadmap` becomes a planning artifact generator only.** It already says so ("The roadmap is a planning artifact", PRO:38; final message "recommend user review", PRO:329). A human must carry its output into `/task-builder` or `/roadmap` input. No file describes that hand-off: UNVERIFIED (see section 8).
3. **The one programmatic `/sc:task` caller dies with it.** TLP Stage 9 invokes `sc:task --compliance strict` through the Skill tool to apply the patch checklist, and the P2 loop re-enters Stage 9 (TLP:1535-1557, TLP:1607). With `/sc:tasklist` retired, no remaining skill read here calls `/sc:task`.
4. **`superclaude sprint run` loses its input.** `/sc:tasklist` produced the Sprint-compatible bundle; "invocation is separate" (TLC:118; TLP:16). Another generator for that bundle: UNVERIFIED.
5. **History is legitimate, not a violation.** The team ran the whole chain once: `repo:.dev/releases/complete/v1.3-2026Upgrade/` holds `tasklist-index.md` (Generator Version "Roadmap->Tasklist Generator v4.0", 8 phases, 192 tasks), `phase-1..8-tasklist.md`, `execution-log.jsonl` with `sprint_start` on 2026-05-17, and was archived 2026-06-24 (commit 730ca38f). The later releases `repo:.dev/releases/current/v2-m2/tasks/T1-*.md` and `v2-m3/BUILD-REQUEST-V2-M3.md` show the BUILD_REQUEST / task-file lane instead. A checker must not flag old tasklist bundles, and must not expect new ones. This resolves CV unverified item U6 (see section 7).

<!-- SECTION 5 -->
## 5. What a scheduled checker can see

### 5.1 Observed in this repo (one run, 2026-05-17; read-only listing, nothing re-run)

Output folder `repo:_bmad-output/planning-artifacts/` (the parent of the input `tdd.md`, matching CMD:19):

| Footprint | Evidence |
|---|---|
| `.roadmap-state.json`: keys `schema_version`, `spec_file`, `tdd_file`, `prd_file`, `input_type` (`tdd`), `spec_hash`, `agents[]`, `depth` (`deep`), `last_run`, `steps{}` (each `status`, `attempt`, `output_file`, `started_at`, `completed_at`), `fidelity_status`, `validation{status,timestamp}` | observed |
| Step files named by step id: `extraction.md`, `roadmap-opus-architect.md`, `roadmap-sonnet-architect.md`, `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `roadmap.md`, `anti-instinct-audit.md`, `test-strategy.md`, `spec-fidelity.md`, `wiring-verification.md`, `spec-deviations.md`, `remediation-tasklist.md`/`.json`, `remediate-tdd.md`, `deviation-registry.json`, and a `validate/` folder (`validation-report.md`, `reflect-<agent>.md`) | observed |
| `roadmap.md` frontmatter: `spec_sources`, `complexity_score`, `complexity_class`, `primary_persona`, `adversarial`, `base_variant`, `variant_scores`, `convergence_score` | observed |

### 5.2 What the files say a current run leaves (not observed; version differences)

| Footprint | Source |
|---|---|
| `roadmap.md` frontmatter with `generator: sc:roadmap`, `complexity_score`, `complexity_class`, `milestone_count`, `validation_score`, `validation_status` (`PASS`/`REVISE`/`REJECT`/`PASS_WITH_WARNINGS`/`SKIPPED`) | R-TPL:359-403 |
| `extraction.md` with `generator: sc:roadmap`, `total_requirements`, `pipeline_diagnostics`; `test-strategy.md` with `validation_philosophy: continuous-parallel`, `interleave_ratio` | R-TPL:408-457 |
| `<release>/envelope.json` sidecar; terminal step `verify-implementation` (replaced `wiring-verification`) | R-TPL:330; PRO:126 |
| `roadmap-debug.log` only with `--debug` | CMD:33 |
| `.session-memory.md` in the output dir when Serena is unavailable; Serena key `sc-roadmap:<spec-name>:<timestamp>` | PRO:325-326 |

**Version drift matters to a checker.** The observed run has `wiring-verification.md`, no `envelope.json` (searched `_bmad-output` and `.dev/releases`, none found), and no `generator:` key: a grep for `generator: sc:roadmap` over the repo found no hit. Key the checker on `.roadmap-state.json` containing `steps` plus a sibling `extraction.md`, not on `generator:` or on a step file name.

**Name collision.** `/roadmap` also writes `.roadmap-state.json` (RM:143, RM:579) with a different schema (`input_hash`, `input_paths`, `roadmap_status`). Tell them apart: `/sc:roadmap` has `steps` and `spec_file`; `/roadmap` lives inside `TASK-ROADMAP-*/` next to `build-requests/` and `qa/` (RM:130-143).

### 5.3 Not on disk

The skill load (`sc:roadmap-protocol`) and the choice of flags: transcript only. The CLI can also be run directly from a shell, which leaves the identical footprint (CMD:92), so a footprint does not prove the slash command was used (UNVERIFIED which was used in May).

### 5.4 Footprint of the retired downstream (legacy only)

`tasklist-index.md`, `phase-N-tasklist.md`, `validation/ValidationReport.md`, `PatchChecklist.md`, `manifest.json`, `execution-log.jsonl` under a release folder: observed in `repo:.dev/releases/complete/v1.3-2026Upgrade/`. Do not expect new ones.

<!-- SECTION 6 -->
## 6. Expected-step rule

- **Count it as expected: never**, at any scope or complexity. No pipeline Ryan listed includes it, the guide routes R and N to `/roadmap` (HW:245, HW:309), and a work item that has a task file or `/roadmap` output instead has followed the pipeline. Its absence is always fine, including at R-HIGH and N-HIGH.
- **If it IS present** (a `.roadmap-state.json` with `steps`): do not flag it as wrong, and do not accept it as the tasklist step by itself. Expect (a) the run was not `--no-validate` at R/N (J), (b) the next step is a human hand-off into `/task-builder` or `/roadmap`, never `/sc:tasklist`, and (c) a task file or phase task files exist before implementation starts. Flag only a `/sc:tasklist` or `/sc:task` invocation as a step an engineer ran, and treat old `tasklist-index.md` bundles as legacy.

<!-- SECTION 7 -->
## 7. Proposed changes to command-value-by-phase.md

Line numbers are in `command-value-by-phase.md` (CV). Proposals only.

| # | CV location | Current text | Proposed text | Why |
|---|---|---|---|---|
| 1 | Row 113 `/sc:roadmap`, R and N columns | `OPTIONAL` / `OPTIONAL` | R: `OPTIONAL at HIGH complexity, else SKIP (J)`. N: `OPTIONAL at MEDIUM or HIGH, else SKIP (J)`. T, B, S, F stay `SKIP` | Section 3 matrix; R re-rated under the multi-feature-release definition |
| 2 | Row 113 Notes | "Guide section 5: belongs to a separate release pipeline (`/sc:tasklist`, then `superclaude sprint run`). Use `/roadmap` unless the lead says otherwise. ‡ with `/roadmap`" | "Mirrors CLI `superclaude roadmap run`. Its designed next step `/sc:tasklist` is RETIRED, so output stops at `roadmap.md` / `extraction.md` / `test-strategy.md` and a person must carry it to `/task-builder` or `/roadmap`. Use `/roadmap` unless the lead says otherwise (HW:245). Overlaps `/roadmap` for the roadmap document only: only `/roadmap` ends in runnable task files. Not expected by a checker at any size." Drop the ‡ (it says "same job") | Sections 4.1, 4.3 |
| 3 | Row 114 `/sc:tasklist`, R and N | `OPTIONAL` / `OPTIONAL` | `SKIP` / `SKIP`; Notes: "RETIRED (Ryan, 2026-10-27). Never invoke; only programmatic caller of `/sc:task` (Stage 9). Legacy output in `.dev/releases/complete/v1.3-2026Upgrade/`." Remove "whether the team runs `superclaude sprint run` is UNVERIFIED" | Section 4.3 items 3-5 |
| 4 | Row 125 `/sc:validate-roadmap` Notes | "Only in the separate `/sc:roadmap` pipeline." | Append: "that pipeline's terminal step is retired; run only if `/sc:roadmap` was run" | Section 4.3 |
| 5 | Row 112 `/roadmap` Notes | "Guide level 6 step 7. Ask for a "full roadmap" or it stops at build requests. Runs at deepest setting by default" | Append: "Not the same tool as `/sc:roadmap`; they share only the name. `task-builder` text at TB:1668 wrongly says `/sc:roadmap` invokes `/task-builder`: it is `/roadmap` that does (RM:8, RM:660)" | Section 4.1 |
| 6 | O6 (CV:232) Why | "`/sc:roadmap` + `/sc:tasklist` are a separate release pipeline" | "`/sc:roadmap` is a separate planning pipeline whose tasklist step (`/sc:tasklist`) is retired; `/roadmap` is the release/new-product pick" | Section 4.3 |
| 7 | Section 4 "Release" row (CV:256) | Minimum = `/sc:reflect --mode post` per phase, `/code-review`, `/sc:pr-submit --monitor 1` | The multi-feature-release definition includes plan + implement + push, so the minimum needs a tasklist step: `/roadmap` or `/task-builder` per feature, before step 1. `/sc:roadmap` is not that step | Section 3 R re-rating; `/sc:roadmap` is not a minimum step |
| 8 | Section 4 "Skippable at every size" (CV:259) | "`/sc:roadmap` + `/sc:tasklist` + `/sc:validate-roadmap` (separate pipeline)" | "`/sc:tasklist` (retired: never invoke). `/sc:roadmap` and `/sc:validate-roadmap` (skippable; optional at R/N HIGH)" | Retirement differs from "skippable" |
| 9 | Section 4 footprint table (CV:262-276) | no `/sc:roadmap` row | Add: "`/sc:roadmap`: `<output>/.roadmap-state.json` with `steps`, plus `extraction.md`, `roadmap.md`, `test-strategy.md`, `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`; key on the state file, not `generator:` (version drift). Name collision with `/roadmap`'s `.roadmap-state.json` (check for `steps` vs `input_hash`)" | Section 5 |
| 10 | Section 5 U6 (CV:290) | "Whether the team runs `superclaude sprint run`... Existence of the binary does not prove use" | Mark RESOLVED: run observed. `repo:.dev/releases/complete/v1.3-2026Upgrade/execution-log.jsonl` has `sprint_start` 2026-05-17, 8 phases, 192 tasks; archived 2026-06-24 (commit 730ca38f). Later releases use BUILD_REQUEST/task files | Section 4.3 item 5 |
| 11 | Section 5 (new row) | - | Add: "`/sc:roadmap` command file and protocol skill disagree on flags, default output dir, and resume flag; command file governs the CLI surface, skill governs the inference workflow (CMD:89, CMD:92). Which one an engineer actually hits: UNVERIFIED" | Section 2 conflicts |

<!-- SECTION 8 -->
## 8. Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | Which of CMD or PRO an engineer actually gets (flags, default `--output`, `--resume` vs `--resume-from`, `--agents` limits) | CMD:89 says the skill governs behaviour; CMD:92 says the command mirrors the CLI; they conflict (section 2). No run observed | Read the CLI source or run `superclaude roadmap run --help` (not done: read-only brief) |
| U2 | CLI behaviour behind every `executor.py` / `gates.py` / `prompts.py` line cited from PRO and the refs | The Python source was not opened; only skill text read | Open `src/superclaude/cli/roadmap/` in the IronClaude source |
| U3 | What takes `/sc:roadmap` output to tasks now that `/sc:tasklist` is retired (does `/task-builder --spec` or `/roadmap` accept `roadmap.md`?) | No file describes the hand-off | Ruling from Ryan, or read `task-builder` input handling |
| U4 | Retirement of `/sc:tasklist` and `/sc:task` is recorded in no file | TLC, TLP, sc-task files carry no retirement marker; `/sc:roadmap` still links to both (CMD:103; PRO:36) | Mark the files (the engineers' home directories are not in the repo) |
| U5 | Threshold value of `--allow-regeneration` ("diff-size threshold (FR-9)") | Not stated in any file read | CLI source |
| U6 | How `--no-convergence` interacts with the fail-closed `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` | PRO:137 and PRO:157 describe the gate; CMD:36 describes the flag; link not stated | CLI source |
| U7 | Whether CLI `--resume` checks `spec_hash` | State file stores it (observed); only the skill-mode resume checks it (PRO:439) | CLI source |
| U8 | Whether the May 2026 run was the slash command or the shell CLI | Footprint is identical (CMD:92) | Session logs, or the engineer |
| U9 | Whether the lead has said "otherwise" for this team (HW:245), i.e. whether `/sc:roadmap` is expected anywhere | HW is generic; no repo or lead statement read | Ask Ryan |
| U10 | The pre-run proxies for LOW / MEDIUM / HIGH in section 3 | JUDGMENT; the on-disk score exists only after a run (R-SC:98-104) | Ryan's decision |
| U11 | The OPTIONAL / SKIP ratings for R and N cells | JUDGMENT; no file rates this command by scope except HW:245 | Ryan's decision |
| U12 | Why the observed run recorded `validation.status: fail` and a failed third generator `generate-haiku-architect` | State file read; `validate/validation-report.md` not opened | Read that report |
| U13 | Repo `.dev/tasks/to-do` has no `TASK-ROADMAP-*` folder (listed both folders and filtered names for "roadmap": no hits in `to-do` or `done`) | Absence is not proof of non-use; folders may have been renamed or moved | `git log --all -- .dev/tasks` |
| U14 | `~/.claude` is per-engineer (CV U17), so the command may be missing or older on another machine | Home-directory files | Compare installs |
| U15 | `/roadmap` read only in part (lines 1-200, 2610-2678, grep of the rest) | 2678 lines; not needed for this file's claims, but the QA agent counts (RM:27) come from its prose, not a run | Read in full if the comparison is challenged |
