# /sc:validate-roadmap: complexity nuance

**Written**: 2026-10-27 by nuance agent for `/sc:validate-roadmap` (read-only analysis; only this file written)
**Brief**: `command-nuance/_brief.md`
**Sources read in full**: `~/.claude/commands/sc/validate-roadmap.md` (105 lines), `~/.claude/skills/sc-validate-roadmap-protocol/SKILL.md` (1156 lines), `~/.claude/HOW-WE-WORK.md` (cited lines), `command-value-by-phase.md`.

**Citation legend** (all paths under `/home/coder/.claude/` unless noted): VR = `commands/sc/validate-roadmap.md`; VP = `skills/sc-validate-roadmap-protocol/SKILL.md`; RM = `commands/sc/roadmap.md`; SRP = `skills/sc-roadmap-protocol/SKILL.md`; RS = `skills/roadmap/SKILL.md`; TL = `skills/sc-tasklist-protocol/SKILL.md`; TB = `skills/task-builder/SKILL.md`; HW = `HOW-WE-WORK.md`; CV = `command-value-by-phase.md` (in the parent folder); REPO = `/home/coder/workspaces/worktrees/Coder/IB-CPlus-01`.

## 1. Status and role

- Does: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, extraction.md) produced by `superclaude roadmap run`" (VR:3). Phase: Review/Validate, but only inside the separate `/sc:roadmap` release pipeline (HW:245, HW:284).
- Standalone-invokable, NOT on the retired list in the brief. Its documented next step is `/sc:tasklist` (VR:103, VP:76, VP:969), which is retired: nothing in the supported pipelines consumes its output. It never calls `/sc:task` or `/sc:tasklist` itself (VR:97; VP:1138). The one programmatic `/sc:task` caller is `/sc:tasklist` Stage 9 (TL:1535-1540), outside this command.
- Overlaps: `/sc:reflect --mode pre` (CV:231), `/roadmap` built-in QA (RS:27-34), `/sc:roadmap` built-in validation (RM:34, RM:80), `/sc:tasklist` stages 7-10 (retired). **The command file and its protocol skill describe two different interfaces** (section 2).

## 2. Flags

Two flag sets exist, one per file. VR:76 says to pass all arguments "verbatim" to the skill, but the skill defines a different set (see the CONTRADICTION list below the tables). Which set is live in a real run: UNVERIFIED.

**A. Command-file surface (VR:23-34), mirrors the CLI `superclaude roadmap validate`**

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `OUTPUT_DIR` (positional, required) | dir holding `roadmap.md`, `test-strategy.md`, `extraction.md` | none | Input location; results go to `<OUTPUT_DIR>/validate/` (VR:21, VR:25) | Always (required) | Pointing it at a `/roadmap` or `/sc:workflow` output: those do not produce `test-strategy.md` / `extraction.md` (grep of RS found neither name) |
| `--agents` | `model[:persona]`, comma list | `opus:architect` (VR:31) | N=1: one reflection writes `validation-report.md`; N>=2: N parallel reflections then adversarial merge (VR:38-39) | N>=2 on a MEDIUM/HIGH roadmap, e.g. `opus:architect,haiku:qa` (VR:31, VR:52) (J) | N>=2 on a LOW roadmap: cost with little extra signal (J) |
| `--model` | model name | `""` = each agent's own model (VR:32) | Overrides the model for every validation step | HIGH only, when one strong model should do all steps (VR:55-59 example) (J) | Default runs |
| `--max-turns` | integer | `100` (VR:33) | Turn cap per claude subprocess | Raise (example uses 150, VR:58) if a large roadmap run stops early (J) | Default runs |
| `--debug` | bool | `false` (VR:34) | Debug logging | Only when a run misbehaves | Routine runs |

**B. Protocol-skill surface (VP:3-5, VP:80-109)**

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `<roadmap-path>` (required) | roadmap file path | none | Document under test (VP:92) | Always on this surface | n/a |
| `--specs` / `-s` (required) | 1-10 spec paths, comma list | none | Source of truth the roadmap is checked against (VP:93, VP:1085 R4) | Always on this surface; pass every driving spec/TDD/PRD | Omitting it: the skill refuses without specs (VP:82) |
| `--output` / `-o` | dir | `{roadmap-dir}/validation/` (VP:94) | Where `00-` to `05-` artifacts go | Keep default so a checker finds it | Pointing at a tracked path by accident |
| `--depth` / `-d` | `quick` / `standard` / `deep` | `standard` (VP:96) | quick: explicit requirements only, max 6 agents, abbreviated adversarial, no file-path or freshness check; standard: 7-category extraction, max 12 agents, full adversarial; deep: adds one-hop references, max 20 agents, silent-assumption audit, symbol lookups (VP:105-109, VP:318-322, VP:620) | quick for LOW, standard for MEDIUM, deep for HIGH (J: no file ties depth to size) | deep on LOW: pure cost |
| `--max-agents` | 4-20 | `20` (VP:97) | Cap on parallel agents; domain clusters capped at `max-agents - 4` (VP:312) | Lower it to bound cost on LOW/MEDIUM (J) | Below 4 (out of stated range) |
| `--exclude` / `-x` | comma list of domains | none | Table entry only (VP:95); no step in the body uses it. Effect: UNVERIFIED | Not recommended until its behaviour is confirmed | Relying on it to scope a run |
| `--skip-adversarial` | bool | `false` (VP:98) | Skips Phase 4 (VP:744) | LOW roadmaps, when a cheap pass is enough (J) | HIGH: Phase 4 is the check on false COVERED claims (VP:752-760) |
| `--skip-remediation` | bool | `false` (VP:99) | Skips Phase 5 remediation plan (VP:850) | When only a verdict is wanted | When the verdict is not GO and someone must fix the roadmap |
| `--report` / `-r` | path | none | Also writes the summary there (VP:100, VP:974) | When a human wants the summary outside the output dir | Writing into a tracked path without reading it |
| `--prior-taxonomy` | path to a prior `00-domain-taxonomy.md` | none | Seeds domain clustering for repeat runs (VP:101, VP:304) | Re-validating the same roadmap after fixes (J) | First run |

**CONTRADICTION list** (both versions recorded; neither silently picked)

| # | VR says | VP says |
|---|---|---|
| C1 | Invoke as `<OUTPUT_DIR>` (VR:18) | Invoke as `<roadmap-path> --specs <spec...>`, specs required (VP:84, VP:93) |
| C2 | Writes `<OUTPUT_DIR>/validate/reflect-<agent-id>.md` + `validation-report.md` (VR:62-69) | Writes `{roadmap-dir}/validation/00-...05-validation-summary.md` (VP:94, VP:953-966) |
| C3 | "Will Not ... Spawn additional sub-agents beyond the `--agents` list" (VR:98) | Dispatches domain + 4 cross-cutting agents, all `sonnet`, up to 20 (VP:97, VP:365, VP:496) |
| C4 | "Mirrors the CLI `roadmap validate` surface" (VR:3, VR:81) | "NOT a behavioural mirror" of the CLI (VP:20) |
| C5 | Exit 0 always; findings as blocking/warning/info counts (VR:43) | Verdict GO / CONDITIONAL_GO / NO_GO from a fixed matrix (VP:686-693) |
| C6 | Flags `--agents`, `--model`, `--max-turns`, `--debug` (VR:31-34) | None of the four appear anywhere in VP (grep: zero hits) |
| C7 | n/a | Depth table promises a freshness-check column and abbreviated adversarial at `quick` (VP:105-109); Step 3.5 has no depth gate (VP:582-590) and Phase 4 is skipped only by `--skip-adversarial` (VP:744) |

**Does not exist** (flags people may assume): `--depth`, `--specs`, `--output` on the command-file surface (they live only in the skill); `--no-validate`, `--resume`, `--dry-run`, `--input-type` (these belong to `/sc:roadmap`, RM:29-38); `--fix` / auto-remediation (the skill only plans remediation and never edits the roadmap, VP:1134-1140, VR:93-96); `--no-reflect` (that is `/sc:tasklist`, `commands/sc/tasklist.md:23,39`).

## 3. Scope x complexity matrix

**Does the command vary by complexity?** Yes, but only in how heavy the run is (agent count on the command-file surface, `--depth` on the skill surface), not in whether it applies. It does not vary by scope in any file: the command exists only for `/sc:roadmap` output (VR:3, VR:21), and that exists only at release or new-product size. No file ties complexity to a depth or agent count, so every band below is JUDGMENT; the only file-stated numbers are the skill's size cut-offs: under 10 requirements is "very small", over 500 is "very large" (VP:1114-1115), and domain clusters split above 20 requirements (VP:310). TCS (TB:2410-2441) scores task files for reflect depth and is not defined for roadmaps.

| Band | Signals (file-sourced where cited; band edges are J) |
|---|---|
| LOW | One source doc, under 10 extractable requirements (VP:1115) or a single milestone; no irreversible or infrastructure gates (VP:385). Run: command `--agents opus:architect` (default) / skill `--depth quick`. |
| MEDIUM | 10 to 500 requirements; two or more milestones; spec plus TDD or PRD, so the 9 input-aware dimensions apply (VR:41, VP:38-39). The one observed run (about 146 input entities, 5 milestones, about 151 roadmap rows; `REPO/_bmad-output/planning-artifacts/validate/validation-report.md`, Proportionality finding) sits here by count. Run: `--agents opus:architect,haiku:qa` (VR:52) / `--depth standard`. |
| HIGH | Over 500 requirements (VP:1114), or the roadmap sequences irreversible or infrastructure steps (VP:385), or several sources that may conflict (VP:1086). Run: three agents, `--model opus`, `--max-turns 150` (VR:55-59) / `--depth deep` with every driving doc in `--specs`. |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | N/A (no roadmap exists) | N/A | N/A |
| B bug fix | N/A (bug route is `/sc:troubleshoot`, HW:311) | N/A | N/A |
| S single story | SKIP (J) | SKIP (J) | SKIP (J) |
| F multi-story feature | SKIP (J) | SKIP (J) | SKIP (J) |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | WORTH IT (J) |
| N new product | N/A (J) | OPTIONAL (J) | WORTH IT (J) |

Rules that apply to every cell:
- Cells assume a `/sc:roadmap` (or `superclaude roadmap run`) output directory exists. If the roadmap came from `/roadmap` or from `bmad-create-epics-and-stories`, the command has no valid input and the cell is N/A for the command and SKIP for a checker.
- S and F are SKIP because their tasklist step is `/sc:workflow` or `/task-builder` (brief, ruling 5), and the spec check there is `--spec` / `reflect_pre` (validation-feature file, E4) or `/sc:reflect --mode pre` (HW:190-194), not this command.
- R and N use `/roadmap` as the default roadmap tool (HW:245; CV:112), and `/roadmap` runs its own 4-stage QA with coverage validation (RS:27-34). The R and N cells above apply only to the rarer `/sc:roadmap` lane.
- **R re-rating** (brief, ruling 2): CV:125 rates R flat OPTIONAL. Under "multi-feature release" a roadmap-level plan is the central artifact, so a coverage gap is paid for once per feature. Proposed: R splits into SKIP / OPTIONAL / WORTH IT by band (J). The base (MEDIUM) stays OPTIONAL, because `/sc:roadmap` already validates by default (RM:34, RM:80) and the next documented step, `/sc:tasklist`, is retired. N also splits the same way (CV:125 had flat OPTIONAL).

## 4. Choose this or the neighbour

The deciding signal is the kind of artifact being checked, then its size. This command accepts one artifact type: a `/sc:roadmap` output directory (VR:21).

| Neighbour | Rule | Cited |
|---|---|---|
| `/sc:reflect --mode pre` | Checking a task file or a `/sc:workflow` plan against a spec: use reflect (`reflect_pre` already runs inside `/task-builder --spec`; run reflect by hand only when it says `skipped` or the plan is hand-written). Checking a `/sc:roadmap` directory: this command. The skill says a tasklist-shaped roadmap is still validated (VP:1117), but the command file's three-file input rule (VR:25) would reject it: do not use this command for plans. | HW:190-194; VR:25; VP:1117; validation-feature file E4 |
| `/roadmap` built-in QA | If the roadmap came from `/roadmap`, do not run this command: it has no `test-strategy.md` / `extraction.md` (grep of RS: no hit) and `/roadmap` already runs 4 QA stages (document, coverage, BUILD_REQUEST, cross-task). | RS:27-34; HW:245 |
| `/sc:roadmap` own validation | `/sc:roadmap` validates after generation unless `--no-validate` (RM:34, RM:80). Run this command after it only when (a) `--no-validate` was used, (b) the roadmap was hand-edited after a failed report, or (c) the roadmap is in the HIGH band and the deeper multi-phase protocol (coverage matrix, gap registry, adversarial pass; VP:20-25) is wanted. Otherwise the pipeline's own `validate/validation-report.md` is the check. | RM:34; RM:80; VP:20-25 |
| `/sc:tasklist` (retired) | Do not follow the "next step" text. VP:969-971 says "Proceed to tasklist generation with `/sc:tasklist`"; VR:103 lists it under See Also. Ignore both. `/sc:tasklist` stages 7-10 validate a tasklist against a roadmap, the opposite direction (TL:3, TL:16). | VP:969-971; VR:103; TL:3 |
| `bmad-check-implementation-readiness` | BMad-lane analogue for PRD, UX, architecture, epics. No overlap in inputs: BMad lane never creates a `/sc:roadmap` directory. | CV:126 |
| `/sc:spec-panel` | Critiques the spec, not the roadmap. Run it before the roadmap exists; this command assumes the spec is the source of truth (VP:1085). | CV:66; VP:1085 |
| `/sc:adversarial` | Embedded: with N>=2 agents the command does an adversarial merge itself (VR:39). Do not stack `/sc:adversarial` on top. | VR:39 |

## 5. What a scheduled checker can see

| Surface | Footprint | Status |
|---|---|---|
| Command-file layout | `<OUTPUT_DIR>/validate/validation-report.md`; plus `validate/reflect-<agent-id>.md` when N>=2 agents (VR:62-69). Frontmatter keys `blocking_issues_count`, `warnings_count`, `tasklist_ready`. | OBSERVED once: `REPO/_bmad-output/planning-artifacts/validate/{validation-report.md, reflect-opus-architect.md, reflect-sonnet-architect.md}`; frontmatter lines 1-4 of each. Added to git in commit `4f42d1b2` ("commit v1 planning + roadmap pipeline artifacts"). |
| Pipeline state | `.roadmap-state.json` top-level key `validation` = `{status, timestamp}` next to the roadmap files. | OBSERVED: `REPO/_bmad-output/planning-artifacts/.roadmap-state.json` has `validation.status: "fail"` (2026-05-17T17:22:57Z) while the report beside it shows `blocking_issues_count: 0`. Reason for the mismatch: UNVERIFIED. |
| Skill layout | `{roadmap-dir}/validation/00-requirement-universe.md` ... `02-consolidated-report.md` (frontmatter `verdict: GO\|CONDITIONAL_GO\|NO_GO`), `03-adversarial-review.md`, `04-remediation-plan.md`, `05-validation-summary.md` (VP:94, VP:667, VP:953-966). | NOT observed: a find for `02-consolidated-report.md`, `00-requirement-universe.md`, `05-validation-summary.md` under REPO returned nothing. |
| Serena memory | Keys `validation-ledger-{slug}`, `terminology-map-{slug}`, `pattern-log-{slug}`, `adversarial-patterns-{slug}` (VP:1005-1072). | Not in the repo; Serena storage location UNVERIFIED. A checker should not rely on it. |
| Invocation with no output | Transcript only. A run that fails before writing leaves no file. | UNVERIFIED (not run). |

The `tasklist_ready` key and the "Parseability ... sc:tasklist's splitter" dimension (VP:37) are tied to the retired `/sc:tasklist`. Treat `tasklist_ready` as a quality flag only, never as a gate to a next step.

The v1.3 release folder `REPO/.dev/releases/complete/v1.3-2026Upgrade/validation/` holds `ValidationReport.md`, `PatchChecklist.md` and `reflect-phase-N-merged.md`. By name and location these are `/sc:tasklist` artifacts (`commands/sc/tasklist.md:112` says it writes `TASKLIST_ROOT/validation/`; TL:1535 names `validation/PatchChecklist.md`); file contents were not read, so UNVERIFIED. They are not this command's output. A checker must not count them as a roadmap validation.

## 6. Expected-step rule

- **Never expected** at T, B, S, F, or at R and N when the roadmap came from `/roadmap` or the BMad lane. Its absence is fine, and its presence there is also fine (do not flag either way).
- **Soft-expected** only at R or N when a `/sc:roadmap` output directory (`roadmap.md`, `test-strategy.md`, `extraction.md`, `.roadmap-state.json`) is in the branch AND no `validate/validation-report.md` sits beside it AND the work proceeds to implementation (J). If `validate/validation-report.md` exists, the step is satisfied, whether `/sc:roadmap` produced it or this command did. Never require a following `/sc:tasklist`: it is retired.

## 7. Proposed changes to command-value-by-phase.md

Proposals only; that file was not edited. Line numbers are CV lines.

| # | Where | Current text | Proposed text |
|---|---|---|---|
| 1 | CV:125, `/sc:validate-roadmap` row, R and N cells | `OPTIONAL` / `OPTIONAL` (flat) | R: `OPTIONAL` base, banded: LOW SKIP, MEDIUM OPTIONAL, HIGH WORTH IT (J). N: banded: LOW N/A, MEDIUM OPTIONAL, HIGH WORTH IT (J). **R changed**: yes, from flat to banded, because under "multi-feature release" a roadmap coverage gap repeats per feature. Base stays OPTIONAL. All of it applies only to the `/sc:roadmap` lane. |
| 2 | CV:125, Notes | `Only in the separate /sc:roadmap pipeline. /roadmap runs its own QA` | `Only for a /sc:roadmap output directory (roadmap.md, test-strategy.md, extraction.md); /roadmap output is not valid input. /sc:roadmap already validates by default (--no-validate skips it), so this is a re-run or deeper pass. Its documented next step /sc:tasklist is retired. Command file and skill disagree on flags and output layout (command-nuance/sc-validate-roadmap.md section 2).` |
| 3 | CV:231, O5 row, "Overlapping commands" and "Why" | lists `/sc:validate-roadmap`, `/sc:tasklist` integrated validation | Add: `/sc:validate-roadmap` applies only to `/sc:roadmap` outputs; `/sc:tasklist` is retired and drops out of the comparison. |
| 4 | CV:259, "Skippable at every size" | `/sc:roadmap + /sc:tasklist + /sc:validate-roadmap (separate pipeline)` | `/sc:tasklist` (retired). `/sc:roadmap` + `/sc:validate-roadmap` stay skippable at S and F; optional at R and N, as a pair, and a `/sc:roadmap` output has no documented continuation now (see unverified item 5). |
| 5 | CV:263-276, "What a checker could observe" | no `/sc:validate-roadmap` row | Add row: `/sc:validate-roadmap` / `/sc:roadmap` validation: `<out>/validate/validation-report.md` (frontmatter `blocking_issues_count`, `warnings_count`, `tasklist_ready`) and `reflect-<agent>.md`; `.roadmap-state.json` `validation.{status,timestamp}`. Source: observed in `_bmad-output/planning-artifacts/`. |
| 6 | CV:290, U6 "Whether the team runs `superclaude sprint run`" | `Existence of the binary does not prove use`; resolve by "look for `.dev/releases/` runs" | Add evidence: `/sc:roadmap` was run once (`_bmad-output/planning-artifacts/.roadmap-state.json`, `last_run` 2026-05-17, depth deep) and `.dev/releases/complete/v1.3-2026Upgrade/` holds `phase-1..8-tasklist.md`, `tasklist-index.md`, `execution-log.jsonl`, `manifest.json`. Both pipelines were used in the past; current use is still UNVERIFIED. |
| 7 | CV:113-114, `/sc:roadmap` and `/sc:tasklist` rows | R and N `OPTIONAL` for both | Out of scope for this file; cross-reference only: `/sc:tasklist` should read retired (SKIP everywhere) per brief ruling 3. |

## 8. Unverified items

**Focus answer (assigned focus):** it depends on `/sc:roadmap` outputs and nothing else: input is a directory with `roadmap.md`, `test-strategy.md`, `extraction.md` (VR:21), and the skill's pipeline position is `spec -> sc:roadmap -> roadmap.md -> sc:validate-roadmap -> ... -> sc:tasklist` (VP:76). With `/sc:tasklist` retired, the chain ends here: the "GO: proceed to `/sc:tasklist`" text (VP:969) points at a retired command, and nothing on disk consumes the report. It stays useful only as a quality gate on a `/sc:roadmap` roadmap before a human acts on it; it is no longer a step toward implementation. `/sc:roadmap` is rated OPTIONAL at R and N, with `/roadmap` the default (CV:112-113), so this command applies to a minority of R and N work.

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| 1 | Which flag set is live: command-file (`--agents`, ...) or skill (`--specs`, `--depth`, ...) | Contradiction C1-C7 in section 2; I did not run the command | Run once in a scratch dir, or read the CLI source `src/superclaude/cli/roadmap/validate_prompts.py` (cited by VP:23, not opened) |
| 2 | `--exclude` effect | In the flag table (VP:95) but no step in the body uses it | Read the CLI source or run with it |
| 3 | Whether `/sc:roadmap` output is still in use for current work | Only observed run: `.roadmap-state.json` `last_run` 2026-05-17 (`_bmad-output/planning-artifacts/`); `.dev/releases/current/` holds `v2-m2`, `v2-m3` with no `roadmap.md` or `validate/` found (find, depth 4) | Ask the team; list `.dev/releases/` after the next release |
| 4 | Why `.roadmap-state.json` says `validation.status: fail` while `validate/validation-report.md` shows `blocking_issues_count: 0` | Report and state file may come from different runs; state file's other steps not all read | Read `src/superclaude/cli/roadmap/` executor, or compare timestamps (state: 17:22:57Z) |
| 5 | Replacement continuation for a `/sc:roadmap` output now that `/sc:tasklist` is retired | No file names one; HW:245 still says `/sc:roadmap` then `/sc:tasklist` then `superclaude sprint run` | Ryan's ruling on whether the whole `/sc:roadmap` pipeline is retired too |
| 6 | Whether `/sc:validate-roadmap` is shipped to every engineer's `~/.claude` | HW:3 says plugin installs ship only some commands; shipping list not read | Compare `~/.claude/commands/sc/` across engineers |
| 7 | Band edges in section 3 and all `(J)` cells | No file maps complexity to depth or agent count for this command | Team agreement |
| 8 | Serena memory location and whether the ledger hooks fire | Fail-open and not observable from files (VP:136) | Run once with Serena enabled |
| 9 | Exact content of the v1.3 `validation/` folder | Names only listed; files not opened | Open `ValidationReport.md` header |
| 10 | CLI behaviour `superclaude roadmap validate` | `--help` printed the first 5 lines only; the CLI was not run for a real validation | Read the full `--help`; compare against VR:27-34 |
