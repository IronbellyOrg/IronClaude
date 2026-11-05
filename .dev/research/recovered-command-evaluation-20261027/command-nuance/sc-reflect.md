# /sc:reflect: scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: `/home/coder/.claude/commands/sc/reflect.md` (311 lines, cited as CMD), `/home/coder/.claude/skills/sc-reflect-protocol/SKILL.md` (2045 lines, cited as SKILL), and refs under `/home/coder/.claude/skills/sc-reflect-protocol/refs/` (cited as refs/<name>).

## 1. Status and role
- **What it is** (CMD:3): "Tiered reflection protocol: UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate". Phase: Review/Revise/Validate. `--mode pre` checks a plan against a spec; `--mode post` checks built work against a plan. Backing skill EXISTS (`sc-reflect-protocol/SKILL.md`, 2045 lines, plus 12 refs; all read).
- **Standalone and automatic**: NOT retired, invokable by hand (CMD:19). Also called with no engineer action by `/sc:workflow` Wave 4 (WP:56), `/task-builder` A.10.7 PRE gate and its generated POST item (TB:1662, TB:2215), and `/sc:troubleshoot --fix` Wave 6 (CMD:305). `/sc:implement` does NOT call it and forbids it as a per-task gate (IM:130, IS:11, IS:171).
- **Neighbours / retired names**: overlaps `bmad-check-implementation-readiness` (CV:231), `/sc:analyze` (CMD:310), `/sc:implement` FINAL reviewer. The reflect files still name retired `/sc:task` (end-of-task hook, CMD:309, SKILL:54) and `/sc:tasklist` (consumer row, SKILL:1008). Neither is ever an engineer step; ignore those mentions.

## 2. Flags
Citation key: CMD = command file, SKILL = backing skill, refs/x = file under `sc-reflect-protocol/refs/`, TB = `~/.claude/skills/task-builder/SKILL.md`, HW = `~/.claude/HOW-WE-WORK.md`, WP = `~/.claude/skills/sc-workflow-protocol/SKILL.md`, TK = `~/.claude/skills/task/SKILL.md`, IM/IS = `/sc:implement` command file and skill, CV = `command-value-by-phase.md`.

### 2a. Flags in the command file's option table (CMD:86-116)

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--mode` | `pre` or `post` | auto-detect, 6 rules, first match wins (SKILL:103-112) | `pre` = UC-1 coverage/gap audit of a plan; `post` = UC-2 deviation audit of built work (CMD:88). A bare call with neither resolves to STOP (SKILL:112) | Always pass it (CMD:88, SKILL:77) | Mixing with legacy `--type/--analyze/--validate` is a STOP (CMD:127) |
| `--type` / `--analyze` / `--validate` | `task` / flag / flag | legacy | `--type task --analyze` = `--mode pre`; `--validate` = `--mode post` (CMD:118-125). Kept for `/sc:troubleshoot` MDTM route only (CMD:305) | Never in new use | - |
| `--spec` | path | none | `pre`: REQUIRED, no spec = STOP (CMD:32). `post`: recommended (CMD:92). Also feeds the reachability gate (SKILL:552-558) | Whenever a spec, PRD or TDD exists | - |
| `--tasklist` | path | none | The plan under audit. Strongly recommended for `post` (CMD:93) | Always when a task file or plan exists. Without it every hunk is "unmapped" so Drift cannot be assigned (J, from S_dev_density definition, SKILL:430) | - |
| `--diff` | git ref, `A..B`, or diff file | none | `post`: required unless `--task-log` (CMD:94). A SINGLE ref is diffed against the working tree, so uncommitted tracked edits are audited; `A..B` sees committed work only (refs/remediation-handoff.md:103, HW:83) | After `/task`: one commit before the work started (HW:83, HW:322) | `..HEAD` range right after `/task`: `/task` does not commit, so it misses the phase (HW:81) |
| `--commit-range` | range | none | Alternative to `--diff` (CMD:95) | - | - |
| `--scope` | path | none | Narrows scope; may flip auto-detect to `post` (CMD:96, SKILL:109) | Only with auto-detect | - |
| `--task-log` | path | none | Alternative `post` input (CMD:97). Plan-route Phase D passes the sibling `progress.md` so files created but untracked are seen (refs/remediation-handoff.md:100-103) | After `/sc:implement` of a remediation plan | - |
| `--depth` | `quick`, `standard`, `deep` | `standard` | `quick` = Tier 1 only; `deep` = force Tier 2 (CMD:98). Both are hard overrides applied BEFORE the rubric (SKILL:410-415). `deep` on under-specified input (1-line spec, empty tasklist) = STOP (CMD:34). With `--remediate`, depth also picks the route (CMD:110) | Pick by TCS band (TB:2429-2433): `quick` only at `pre` | `quick` at `post`: task-builder forbids it, because it disables regression escalation (TB:2440, SKILL:414) |
| `--tier` | `1`, `2`, `auto` | `auto` | Explicit pin that overrides the rubric (CMD:99, SKILL:412-413). `--tier 2` needs at least 2 distinct model classes (SKILL:242-244) | `--tier 1` for a cheap second opinion (CMD:53-54) | Combining with a contradicting `--depth`: precedence not stated (UNVERIFIED) |
| `--reviewers` | 2 or 3 | 3 | Tier 2 reviewer count, clamped by depth and alias count (CMD:100, SKILL:242-244) | Leave default | - |
| `--output` | dir | `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/` | Report location (CMD:101, SKILL:87). STOP if under `.claude/skills`, `agents`, `commands` (CMD:35). STOP `output_input_overlap` if it equals or contains an input (SKILL:209) | A fresh dedicated dir when a previous report is an input | Reusing an earlier report's folder |
| `--coverage-floor` | float | `0.90` | `pre` only. Used in Tier-1 STOP row 1 (SKILL:438, SKILL:448). Does not touch the `S_dev_density > 0.20` escalation (refs/coverage-mapping.md:204-208) | `0.95` for high-safety work (CMD:102) | Expecting it to change `/task-builder`'s pass line: task-builder does not pass it (TB:1671-1676) |
| `--no-mcp` | bool | false | Native tools only, quality degrades (CMD:103) | Debug | Normal runs |
| `--no-evidence-validator` | bool | false | Skips the final citation gate; forces `status: partial` (CMD:104, SKILL:1246) | Debug only | Normal runs |
| `--no-doc-discovery` | bool | false | Skips Wave 1.5 documentation grounding, logged as a gap (CMD:105) | Debug | Normal runs |
| `--no-verify` | bool | false (post) | Turns off the test/lint/type-check "verification triangle"; regression detection falls back to the task-log claim plus a Grounding Gap (CMD:106, SKILL:1109) | Only when tests cannot run in this environment | When tests can run |
| `--rerun-tests` | alias | - | Deprecated alias for verification on (the default) (CMD:106) | Never | - |
| `--no-reachability` | bool | false (post) | Switches off the contracted-sink reachability gate; telemetry only, no Grounding Gap, no `status: partial` (CMD:107, SKILL:552) | Operator rollback only | - |
| `--onboard` | bool | false | One-shot Serena `onboarding` bootstrap when project memory is empty (CMD:108) | Never routinely | - |
| `--with-hierarchy` | bool | false | Opt-in type-hierarchy retrieval; backend-gated (CMD:109) | OO codebases on a capable backend | Others |
| `--remediate` | bool | false | After the audit, offers the Tier 3 chain. Plan route (default): `sc:workflow` builds `.dev/tasks/to-do/<slug>/<slug>.md`, you run `/sc:implement`, then re-run `--mode post`. `--depth deep` adds MDTM route: `task-builder`, you run `/task`. `--depth deep` alone never remediates (CMD:110, refs/remediation-handoff.md:11-19). Reflect never runs the executor (CMD:282, CMD:297). +20-40k Claude tokens, +5-10 min (SKILL:1725) | After a `post` audit with Drift or Regression you want fixed as a plan | `confirm-built` routing row does not use it (HW:322) |
| `--budget-remaining` | int | none | Caller budget hint; `N < 5` STOP, may force Tier 1 (CMD:111, SKILL:320-324) | Sprint callers only | Humans |
| `--no-promote` | bool | false (post) | Suppresses Wave 7, which otherwise MOVES a passing work folder to its done location (CMD:112, SKILL:1538-1563) | ALWAYS when you want a report only. HW:322 lists it as the mandatory flag of `confirm-built` | - |
| `--promote-anyway` | bool | false | Overrides the `status: partial` gate condition only; no effect on `failed` (CMD:113) | Never routinely | Defeats the gate |
| `--promote-dry-run` | bool | false | Prints the `mv` command and 9-condition gate result, no mutation (CMD:114) | To debug why a folder did or did not move | - |
| `--promote-mode` | `auto`, `task`, `sprint-release`, `none` | `auto` | Forces a promotion adapter (CMD:115, refs/promotion-adapters.md:9-12) | Rare | - |
| `--promote-resume` | checkpoint path | none | Resumes an interrupted cross-filesystem move; exclusive with the other promote flags (CMD:116, refs/promotion-adapters.md:33) | After a crash | - |

### 2b. Flags found in the skill or refs but NOT in the command file's option table

| Flag | Where | What it is | Status |
|---|---|---|---|
| `--no-escalate` | SKILL:416 | Stop at Tier 1 with a warning if confidence < 0.85 | Not in CMD:10 argument-hint. Whether the slash command accepts it: UNVERIFIED |
| `--strategy enterprise` | SKILL:445, SKILL:674 | "set on caller": forces escalation (rubric row 7) and an `opus` reviewer | Same |
| `--executor-model <class>` | SKILL:666, refs/reviewer-spec.md:88 | Removes the executor's model class from the reviewer pool. Used by task-builder CLI mode (TB:2246) | Same |
| `--isolate-reviewers` | SKILL:283 | Wrapper-level snapshot grounding; default OFF | Wrapper CLI; source not read |
| `--fuzzy-ids` | refs/coverage-mapping.md:93 | Optional fuzzy requirement-ID matching | Mentioned only there |
| `--remediate-docs` | SKILL:1085, refs/remediation-handoff.md:265 | Offers a spec-update task for Necessary deviations | Mentioned only there |
| `--recursive`, `--resume-from` | SKILL:1887, SKILL:1497 | Named in prose, never defined | Treat as not existing |
| `superclaude reflect run <task> --depth deep --fix --promote [--base]` | CMD:66-70, TB:2237 | Headless wrapper used by `/task-builder --cli`; exit 0 = pass, 10/11/2 = fail (TB:2237) | Wrapper source not read: UNVERIFIED |
| `superclaude reflect contract-status [--validate] --repo --pr` | CMD:73-82 | Detection-contract readiness; not a reflect audit; writes nothing by default | Out of SDLC scope here |

### 2c. Does not exist (people may assume)

- `--fix` on `/sc:reflect` itself: only the wrapper CLI has it (CMD:66-70, TB:2237). The slash command uses `--remediate` (CMD:110). `/sc:troubleshoot` is the one that has `--fix`.
- A `--coverage-floor` for `post`: it is `pre` only (SKILL:448).
- `--rollback-last` and `--auto-rollback-on-verify-fail`: deferred to v1.1, not built (SKILL:2027, refs/promotion-adapters.md:128). Rollback is a manual inverse `mv` printed in `promotion-log.yaml` (SKILL:1648).
- Operator-registered promotion adapters: v1.1 only; two adapters are hard-coded (refs/promotion-adapters.md:21).
- `--jury`: eval-runner flag, not a command flag (SKILL:1426).
- `--handoff` / `--output` on workflow: reflect passes `--handoff none` to `sc:workflow` and never `--output` (refs/remediation-handoff.md:74).

## 3. Scope x complexity matrix
**The command varies by complexity in exactly one way the files define: the depth/tier it runs at.** Whether to run it at all is driven by scope and by whether a spec or a tasklist exists. Two different measures share the words LOW/MEDIUM/HIGH, so a checker must not mix them:

- **Before the run (static, on disk):** the Tasklist Complexity Score (TCS) that `/task-builder` computes and writes to `reflect_pre.tcs` (TB:2410-2441): LOW = TCS 12 or less (`quick`), MEDIUM = 13-34 (`standard`), HIGH = 35 or more (`deep`, Tier 2 forced).
- **During the run (measured by reflect in Wave 1, not available beforehand):** Tier-1 STOP only if `C >= 0.90`, `S_scope <= 5 files`, one domain, `S_dev_density <= 0.05` (SKILL:438); otherwise escalate on `S_domains >= 3`, `S_dev_density > 0.20`, `C < 0.85`, or any Regression candidate (SKILL:440-446).

Band definitions used below (one line each):

- **LOW**: TCS 12 or less (TB:2431); files can be named up front; one subsystem; no driving spec or a short one; no human-decision items; not a refactor.
- **MEDIUM**: TCS 13-34 (TB:2432); up to about 10 files and 2 domains (SKILL:439); a driving spec exists; stories share no interface (J on the last clause).
- **HIGH**: TCS 35 or more (TB:2433), OR a refactor/remediation `type:` (forces `deep`, O2, TB:2438), OR 3 or more domains (SKILL:442), OR spec-declared required capabilities or durable sinks (SKILL:552-558), OR "must not drift" with a spec to trace. Human-decision items floor depth at `standard` (O1, TB:2437).

Only the TCS thresholds, the SKILL rubric thresholds and the O1-O4 overrides are file facts. Every REQUIRED/WORTH IT/OPTIONAL/SKIP rating below is `(J)` unless a file is cited in the same cell.

### 3a. `--mode pre` (plan against spec)

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | N/A: no tasklist, and `--mode pre` STOPs without `--spec` (CMD:32) | N/A | N/A |
| **B** bug fix | SKIP (J) | SKIP (J). A task file built from a troubleshoot report normally records `reflect_pre: skipped` (HW:192) | OPTIONAL (J): only if a real spec exists; `--spec <spec>` or `@<spec>` in the goal makes `/task-builder` run it (TB:41) |
| **S** single story | SKIP: `/sc:workflow` already ran it in Wave 4 (WP:56). Do not rerun (J) | OPTIONAL: manual only if a separate spec exists beyond the request (HW:191): `--mode pre --spec <spec> --tasklist <plan>` | REQUIRED, but automatic: `/task-builder --spec <path>` runs it, depth from TCS (TB:1666-1675). Do not rerun if `reflect_pre.verdict` is `pass` or `fail` (HW:190) |
| **F** multi-story feature | WORTH IT (J), automatic via `--spec`, `--depth quick` | REQUIRED, automatic via `--spec`, `--depth standard` (HW:307 lists `--spec` as the mandatory flag) | REQUIRED, automatic, `--depth deep`, Tier 2 forced; `--coverage-floor 0.95` optional (J) |
| **R** multi-feature release | WORTH IT (J): each phase task file | REQUIRED (J): every phase task file built with `--spec <TDD>` (HW:77) | REQUIRED (J), `deep`; plus run by hand on any hand-written release plan that has a spec |
| **N** new product | WORTH IT (J) | REQUIRED (J), same as R | REQUIRED, `deep`. `/roadmap` composes `/task-builder`, so the gate is automatic when `--spec` is passed (CV:112, HW:77) |

If no spec exists the only legal state is `reflect_pre.verdict: skipped` with `skip_reason: no-spec` (TB:1666). That is a pass for a checker, not a miss.

### 3b. `--mode post` (built work against plan)

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP (J): no tasklist to audit against; proposed one-off minimum is a plain edit plus the related test (validation-oneoff file, still PROPOSED) | SKIP (J) | SKIP (J) |
| **B** bug fix | SKIP (J) | SKIP (J) | WORTH IT (J), and automatic when the fix went through `/task-builder` (in-task POST item, TB:2215). Manual re-confirm OPTIONAL |
| **S** single story | OPTIONAL. Workflow + `/sc:implement` lane: implement has its own per-task reviewer and FINAL review and does not call reflect (IS:11, IS:171). If run: `--mode post --tasklist <pkg>/<id>.md --diff <commit> --no-promote` (J) | WORTH IT (J): `--no-promote`, `--depth standard` | WORTH IT (J): task-file lane, POST item ran automatically, but it audits a committed range and `/task` does not commit, so re-confirm with one commit and `--no-promote` (HW:81-83, HW:322) |
| **F** multi-story feature | OPTIONAL (J): POST item already ran in each task file | WORTH IT per phase: `--no-promote` (CV:255) | REQUIRED (J) per phase, `--depth deep --no-promote`. Cross-task interaction scan only fires with 3 or more completed tasks (SKILL:338) |
| **R** multi-feature release | WORTH IT (J) | REQUIRED (J): every phase of every feature, `--no-promote` | REQUIRED (J): every phase PLUS one final run over the whole release range with the release plan as `--tasklist`, `--depth deep`. Large diffs switch to per-file classification above 100 hunks and to sampled citation checks above 20 (SKILL:1055, SKILL:1283) |
| **N** new product | REQUIRED: "always run the re-confirm audit" after each phase (HW:81-83); routing note repeats it (HW:309). Band only changes depth | REQUIRED | REQUIRED, `--depth deep` |

POST depth is never `quick` (O4, TB:2440). In `--cli` mode the generated POST item is fixed at `--depth deep` (TB:2441); in skill mode it is the TCS depth floored at `standard` (TB:1081).

### 3c. `--promote` / `--no-promote` by band

Does not vary by complexity. For hand-run audits the team routing mandates `--no-promote` at every size (HW:322); the default (promote on) moves a passing folder to `.dev/tasks/done/` only when all 9 gate conditions hold, including `tasklist_completion_pct == 1.0`, zero Drift and Regression, zero dropped citations, zero Grounding Gaps, and tasklist `status: done` (SKILL:1545-1563). A higher band makes promotion less likely (more Grounding Gaps and human-decision flags), not more (J). The `/task-builder --cli` POST item passes `--promote` on purpose (TB:2237); the skill-mode item does not pass `--no-promote`, but HW:252 says the folder stays in `to-do/` because the audit runs before the task is marked Done.

## 4. Choose this or the neighbour
### 4a. When it runs by itself, and when a person should run it

| Caller | What it runs | Flags it passes | Person should add a manual run when |
|---|---|---|---|
| `/sc:workflow` Wave 4 (WP:56-58) | `--mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, always, advisory, never edits the plan, never changes workflow status | Defaults only: `--depth standard`, no `--remediate`. Workflow's own `--depth quick` is NOT passed through, so complexity does not scale this call | A separate spec/PRD/TDD exists beyond the request (HW:191). Result lives in `return-contract.yaml` as `reflect_status`, `reflect_report_path` |
| `/task-builder` A.10.7 (TB:1662-1703) | `--mode pre` on the built file. Mandatory when a spec resolves; `skipped` is legal ONLY with no spec (TB:1666, TB:1701). Never auto-loops | `--mode pre --remediate [--spec] --tasklist <file> --depth <TCS depth> --output ${TASK_DIR}reflect/pre/`; no `--executor-model` (TB:1671-1678) | `reflect_pre.verdict` is `skipped`, or the plan is hand-written, AND a spec exists (HW:192-194). Not when verdict is `pass` or `fail` (HW:190) |
| Generated POST item inside every task file (TB:2215-2240, TB:1077) | `--mode post` as the penultimate item, before "Update status to Done". Skill mode: a dedicated subagent runs `Skill(sc-reflect-protocol, "--mode post --remediate --diff {BASE}..HEAD --tasklist {TASK_FILE} [--spec] --depth {DEPTH} --output {OUTPUT_DIR}")` (TB:2223). CLI mode (`/task-builder --cli`, default OFF): `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` (TB:2237) | `{BASE}..HEAD` is a range, so uncommitted phase work is NOT audited (HW:81) | After every `/task` phase of a roadmap or multi-phase feature: single commit, `--no-promote` (HW:83, HW:322). Skill mode is "NOT yet session-validated"; the `--cli` path is the validated one (TB:2371) |
| `/sc:troubleshoot --fix` Wave 6 (CMD:305, troubleshoot.md:54) | Plan route: workflow's own pre, then `--mode post` as the pre-commit gate. `--fix --depth deep`: legacy `--type task --analyze/--validate` | - | After `/sc:implement <tasklist>` completes, run `--mode post` yourself (troubleshoot.md:202) |
| `/sc:implement` (IM:130, IS:11, IS:171) | Does NOT call reflect and refuses it as a per-task gate | - | Post-audit of an implement run is always manual |
| `/roadmap` (CV:112) | Composes `/task-builder`, so PRE/POST items appear in every phase task file | As above | The phase re-confirm in HW:83 |

### 4b. Choose this or the neighbour

| Neighbour | Decision rule by signal | Cites |
|---|---|---|
| In-task POST item (`reflect_post`) versus manual `--mode post` | Rely on the in-task item when the work is committed and `reflect_post` holds a verdict. Run manually when work is uncommitted at POST time (HW:81), when `reflect_post` is empty or failed, or when the lane is workflow + `/sc:implement` (no automatic post) | HW:81-83, HW:322, IM:130 |
| Workflow Wave 4 pre versus manual `--mode pre` | One signal decides: does a spec exist that is separate from the request? Yes: run manual pre against it. No: nothing to check against; read the plan yourself | HW:191-194 |
| Task-builder PRE versus manual `--mode pre` | `reflect_pre.verdict` is `pass` or `fail`: do not rerun, fix Open Questions instead. `skipped` plus spec on hand: run manual pre, then add missed requirements as new unchecked `- [ ]` items | HW:190-194 |
| `/sc:implement` FINAL review versus `--mode post` | Implement's reviewer is one fresh reviewer against the plan (validation-feature file E1/E2). Reflect post adds a heterogeneous reviewer ensemble and a Drift/Regression taxonomy. At LOW complexity implement's own review is enough (J). At MEDIUM or HIGH with a driving spec, add a manual post (J) | IS:11, SKILL:1051-1210 |
| `bmad-check-implementation-readiness` | Same job (O5), different inputs (plan versus spec, versus PRD+UX+architecture+epics). One per lane: task-file lane uses `--mode pre`; BMad lane uses the BMad skill | CV:231 |
| `/sc:analyze` | No spec and no diff to compare to: use analyze. Reflect needs a spec (pre) or a diff or task log (post) | CMD:310 |
| `/sc:brainstorm` | The spec or tasklist itself is ambiguous: scope it first | CMD:311 |
| `bmad-retrospective`, `bmad-code-review` | Not overlaps: retrospective is lessons after an epic; reflect post is a deviation audit against a plan | CV:243 |
| `/code-review` (built-in) | Relation to reflect is stated in no file read: UNVERIFIED. HW:323 lists it as a separate step after the commit | HW:323 |
| `/sc:adversarial` | Reflect calls it internally in Tier 2 Wave 4; never run it for this purpose | CMD:306, SKILL:699 |
| `/sc:task`, `/sc:tasklist` | RETIRED. Reflect text mentions them (CMD:309, SKILL:54, SKILL:1006-1008). Do not follow | brief ruling 3 |

### 4c. Choosing `--depth` / `--tier` from complexity signals

| Signal (on disk) | Choose | Basis |
|---|---|---|
| `reflect_pre.tcs` 12 or less, no refactor type | pre `quick` (Tier 1); post `standard` | TB:2431, TB:2440 |
| TCS 13-34, or any human-decision item, or more than 40 checklist items (50 single-track) | `standard` (reflect may escalate) | TB:2432, TB:2437, TB:2439 |
| TCS 35 or more, or `type:` Refactor/Remediation/Code Remediation | `deep`, Tier 2 forced | TB:2433, TB:2438 |
| Diff touches 3 or more domains (code, infra, docs, tests, config), or more than 20 percent of hunks unmapped, or any Regression candidate | Reflect escalates to Tier 2 on its own under `standard` | SKILL:440-444 |
| Cost matters | Tier 1 about 3-8k Claude tokens, 1-3 min; Tier 2 about 35-70k, 8-15 min. These are targets, not measurements | SKILL:1721-1727 |

## 5. What a scheduled checker can see
Footprint exists on disk for every path except a bare manual run that is never committed. Items marked "observed" were seen in this repo with read-only listing; the rest are from the files cited.

| Footprint | Where | Key fields | Source / status |
|---|---|---|---|
| Task-file frontmatter `reflect_pre` | top of the task file | `verdict` (`pass`, `fail`, `skipped`), `skip_reason` (`no-spec` only when skipped), `coverage_pct`, `depth`, `tcs`, `tier_reached`, `run_id`, `report`, `reviewed_at` | TB:1686-1699. Observed (count of files in `.dev/tasks/to-do/*/TASK-*.md` where `reflect_pre:` is followed directly by a `verdict:` line): 8 `pass`, 3 `skipped`, 2 `fail` |
| Task-file frontmatter `reflect_post` | same | `{verdict, run_id, report}`; `reflect_post_mode: skill` or `cli` always present; CLI mode adds `start_commit`, `executor_model_class` | TB:2168-2171, TB:2231, TB:2392 |
| Real files are looser than the spec | same | Observed: `reflect_pre: "historical evidence only; ..."` as a plain string, `reflect_post: ""` empty, `verdict: "pass"` quoted, extra keys (`best_practice_grade`, `advisory_gaps`) | `.dev/tasks/to-do/TASK-RF-aidev02-profile-route-20260913-210529/*.md:14-15`; `.dev/tasks/to-do/TASK-FU-STARTUP-WIRING-20260706-050839/*.md:19-29`. A checker must parse tolerantly |
| Pre report inside a task folder | `<task-dir>/reflect/pre/REPORT.md` | report header YAML, `return-contract.yaml`, `audit.log`, `artifacts/tier_decision.yaml` | TB:1675, SKILL:734, SKILL:456. Observed: `.dev/tasks/to-do/TASK-RF-t51-leak-scan-20260919-181004/reflect/pre/REPORT.md` |
| Case mismatch | `report.md` versus `REPORT.md` | task-builder's hard check names lowercase `report.md` (TB:1697, TB:1701); reflect writes `REPORT.md` (SKILL:734, CMD:138, refs/report-template.md) | Observed on disk: uppercase. A checker should accept both |
| CLI-mode post report | `<task-dir>/reflect/post/<short-sha>/` with `adversarial/merged-verdict.yaml`, `reviewer-cards/`, `audit.log` | `merge_method` must be `adversarial` or `single-reviewer-fallback` | TB:2239, SKILL:850 |
| Skill-mode post report | `{OUTPUT_DIR}` chosen by the builder; value not defined in the lines read | same files for Tier 2 | TB:2223, TB:2232. UNVERIFIED path |
| Hand-run report | `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/REPORT.md`, `return-contract.yaml` | `contract_version` 1.8.0, `mode`, `status`, `tier_reached`, `confidence_calibrated`, `deviation_count_by_class`, `promotion_action` | CMD:101, SKILL:739-741. Observed: `.dev/reflect/post-pr43-remediation-20260529/REPORT.md`. Resolves CV:272 and CV:297 U13 for reflect |
| Workflow plan record | `<pkg>/return-contract.yaml` | `reflect_status`, `reflect_report_path`; no coverage number | WP:56, validation-feature file E4 |
| Promotion | folder moved `.dev/tasks/to-do/TASK-*` to `.dev/tasks/done/TASK-*`; `promotion-log.yaml` with `gate_evaluation` | only when 9 conditions pass and `--no-promote` absent | SKILL:1538-1563, SKILL:1654-1689. Appears as renames in git |
| Per-machine metrics | `<output>/metrics.json`; `.dev/reflect/runs.jsonl` | append-only, "gitignored by convention" | SKILL:1828-1834 |
| Transcript only | a manual run whose output dir is never committed | - | see ignore rule below |

**Ignore rule (observed, matters for a scheduled job).** `.gitignore:32` is `reflect/`, with no leading slash, so it matches a folder named `reflect` at any depth. `git check-ignore -v` reports the pattern for both `.dev/reflect/...` and `.dev/tasks/to-do/<task>/reflect/pre/report.md`. Existing report folders are tracked anyway (`git ls-files .dev/reflect` and `.dev/tasks/**/reflect/**` list files), so they were committed before the rule or with force. Consequence: a plain `git add .dev/tasks` does NOT stage a NEW `reflect/` subfolder, though the repo `CLAUDE.md` says `.dev/tasks/` is always staged. The durable record in git for new work is the frontmatter `reflect_pre` and `reflect_post`; the report folders may exist only on the engineer's disk. Whether engineers force-add them: UNVERIFIED.

## 6. Expected-step rule
- **Count as expected (flag if missing):** (1) any task-builder file built with a spec: `reflect_pre.verdict` of `pass` or `fail` with a real `run_id` and a report on disk, at the depth the TCS dictates (TB:1701); (2) any task-builder file whose `status` is Done: non-empty `reflect_post` (TB:2231; observed files with `reflect_post: ""` exist, so check status first); (3) N (new product): a hand-run `--mode post --no-promote` after each `/task` phase (HW:81-83); (4) R and HIGH F (J): the same per phase, plus a final whole-release run for R.
- **Absence is fine:** T at any band; B at LOW and MEDIUM; `reflect_pre.verdict: skipped` with `skip_reason: no-spec` (TB:1666); the workflow + `/sc:implement` lane has no post-audit requirement (IS:11, IS:171) and its pre-check is automatic and advisory (WP:56-58); manual pre when `reflect_pre` already says `pass` or `fail` (HW:190); LOW and MEDIUM F or S where the in-task POST item already recorded a verdict and nothing is uncommitted (J).

## 7. Proposed changes to command-value-by-phase.md
CV line numbers refer to `command-value-by-phase.md`. Proposals only; nothing was edited there. Items overlapping `validation-feature-task-builder-vs-sc-workflow.md` row 14 are marked.

| # | CV line | Current text | Proposed text | Evidence |
|---|---|---|---|---|
| 1 | CV:124 | One row: `/sc:reflect` : SKIP SKIP OPTIONAL WORTH IT REQUIRED REQUIRED | Split into two rows. **`/sc:reflect --mode pre`**: T N/A, B SKIP, S OPTIONAL, F REQUIRED (automatic inside `/task-builder --spec`), R REQUIRED, N REQUIRED. **`/sc:reflect --mode post`**: T SKIP, B SKIP, S OPTIONAL, F WORTH IT (REQUIRED at HIGH), R REQUIRED, N REQUIRED. Only F-pre changes a rating (WORTH IT to REQUIRED, and only when a spec exists); the split makes the two modes' different triggers visible | HW:307 (`--spec` mandatory flag), TB:1664-1666, HW:81-83. F-pre REQUIRED is (J) |
| 2 | CV:124, R column, and CV:256 Release row | R = REQUIRED, Release steps list only `--mode post --diff <commit> --no-promote` on each phase | Keep REQUIRED, but re-state it for the multi-feature meaning: (a) `--mode pre` on the release plan and on every phase task file against its spec, (b) `--mode post --no-promote` per phase of EVERY feature in the release, (c) one final `--mode post --depth deep --no-promote` over the whole release range with the release plan as `--tasklist`. Old reading looks like the shipping step of one feature, which the new ruling puts inside S or F | Brief ruling 2; SKILL:338-349 (interaction scan needs 3 or more tasks), SKILL:1055 and SKILL:1283 (large-diff behaviour). (b)-(c) are (J) |
| 3 | CV:124 Notes | "`--mode pre` only when `reflect_pre` verdict is `skipped` or the plan is hand-written. S: `/sc:workflow` already self-checked" | "`--mode pre` by hand only when `reflect_pre` is `skipped` or the plan is hand-written AND a spec exists (without `--spec` it STOPs, CMD:32). S: `/sc:workflow` already ran an advisory pre against its own source at default depth (WP:56-58); rerun only against a separate spec (HW:191). Automatic callers: workflow Wave 4, task-builder A.10.7 and its POST item. Depth follows the task file's TCS, never below `standard` at post (TB:2440). Default `--mode post` MOVES a passing folder to `done/`; HW:322 mandates `--no-promote`" | Same as validation-feature row 14 (qualifies "self-checked") |
| 4 | CV:231, O5 row | "`/sc:reflect --mode pre` in the task-file lane" | Add: "run automatically by `/task-builder --spec` and by `/sc:workflow`; do not rerun when `reflect_pre.verdict` is `pass` or `fail`" | HW:190, TB:1701, WP:56 |
| 5 | CV:255 Multi-story row, "WORTH IT additions" | `/sc:reflect --mode post --no-promote` per phase | Keep. Add that it is REQUIRED (J) at HIGH complexity (TCS 35 or more, or refactor type), with `--depth deep` | TB:2433, TB:2438 |
| 6 | CV:272, footprint row for `--mode pre` | "`.dev/reflect/pre-<name>-<timestamp>/` (post-mode path not stated in the guide: UNVERIFIED)" | Replace with the table in Section 5 of this file: hand-run default `.dev/reflect/<mode>-<slug>-<ts>/` for both modes; inside task-builder `<task-dir>/reflect/pre/`; CLI post `<task-dir>/reflect/post/<short-sha>/`; frontmatter `reflect_pre` and `reflect_post`; add the `.gitignore:32` caveat and the `report.md` versus `REPORT.md` mismatch | CMD:101, TB:1675, TB:2239; `.gitignore:32` |
| 7 | CV:267-268, `/task-builder` and `/task` footprint rows | `reflect_pre` block; `reflect_post` entry | Add the observed shapes: values may be a plain string or empty (`reflect_post: ""` before completion), keys may be quoted, extra keys exist | Observed in `.dev/tasks/to-do` files, see Section 5 |
| 8 | CV:281 | "For `/sc:reflect` ... I read only the usage and flag lines (grep)" | Update: `/sc:reflect` command file, `sc-reflect-protocol/SKILL.md` and its refs have now been read in full (this file) | This file's header |
| 9 | CV:297, U13 | "Post-mode output folder of `/sc:reflect` ... Guide gives only the pre-mode path" | Resolve the reflect half: same default folder pattern for both modes. The `/sc:pr-submit` log half stays open | CMD:101, SKILL:87 |
| 10 | CV Section 5 table | none for reflect depth | Add one line: depth is the only complexity dial; TCS 12 or less quick, 13-34 standard, 35 or more deep; post never quick | TB:2429-2440 |

## 8. Unverified items
| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| 1 | Wrapper CLI `superclaude reflect run` flags and exit codes (`--fix`, `--promote`, `--base`, `--max-fix-iterations`, `--isolate-reviewers`) | Named in CMD:66-70, SKILL:283, TB:2237; wrapper source (`cli/reflect/*.py`) not read; not run | Read the wrapper source |
| 2 | Whether the slash command accepts `--no-escalate`, `--strategy`, `--executor-model`, `--fuzzy-ids`, `--remediate-docs` | In SKILL or refs only; absent from CMD:10 and CMD:86-116 | Run `/sc:reflect` with each, or read the command parser |
| 3 | Precedence when `--depth deep` and `--tier 1` conflict (or `--depth quick` with `--tier 2`) | SKILL:410-416 lists both as hard overrides without ordering | Read the runner code, or a test case |
| 4 | What `--remediate` does at `--mode pre` (task-builder passes it at PRE, TB:1671, and carries "the Tier-3 offer into A.11", TB:1683) | Wave 6 text and the delegation table frame remediation as UC-2 (SKILL:654, refs/remediation-handoff.md:3) | Read a task-builder PRE run that failed coverage |
| 5 | Which `{OUTPUT_DIR}` the skill-mode POST item uses | TB:2223 uses the placeholder; its value is not defined in the lines read | Look at a built task file's POST item |
| 6 | Whether task-builder's Mandatory-run check is case-insensitive about `report.md` versus `REPORT.md` | TB:1701 vs SKILL:734; on-disk reports are uppercase | Inspect a passing build's QA output, or ask the maintainers |
| 7 | How task-builder routes a spec with no labelled IDs: it reads `coverage_pct` (TB:1680), which is parsed-only and may be null (SKILL:751-754), while reflect's own gates use `coverage_pct_union` | Neither file says which field decides `pass` or `fail` in that case | Run `/task-builder --spec` on a prose-only spec |
| 8 | Whether `POST_REFLECT_GATE: ENABLED` is on for every user-invoked build or can be disabled | Only the BUILD_REQUEST template at TB:1077 sets it; no off switch found | Search for a disable path, or inspect several built files |
| 9 | Whether engineers force-add `reflect/` folders despite `.gitignore:32` | Tracked files exist; how they were staged is not recorded | `git log --diff-filter=A -- .dev/reflect` and task-folder history |
| 10 | Skill version drift across engineers' homes: CMD:8 says 2.0.0, SKILL frontmatter says 1.0.0 with contract 1.8.0; CMD:153 points at `src/superclaude/skills/...`, which is the IronClaude source tree, not `~/.claude` | Per-user install (CV:23) | Compare installs |
| 11 | Cost and time | SKILL:1721-1727 are "targets, not caps"; no measurement found | Count spawn logs in a few `reflect/` folders |
| 12 | Promotion on `/task` files: adapter needs tasklist `status: done` (SKILL:1553) but the status vocabulary `/task` writes was not re-checked here | TK frontmatter text not re-read for this | Read TK status values |
| 13 | A claim of mine: that `--mode post` without `--tasklist` cannot assign Drift | Inferred from the S_dev_density definition (SKILL:430) and taxonomy (SKILL:1093); no file states it | Run once on a diff with no tasklist |
| 14 | `/code-review` versus reflect | `/code-review` is a built-in with no file to read | Built-in docs |

Not read: wrapper source, `reflect-reviewer`, `confidence-calibrator`, `evidence-validator` agent files; `refs/grader-extensions.md` past line 80 (eval-only, not behavioural). Nothing was run.
