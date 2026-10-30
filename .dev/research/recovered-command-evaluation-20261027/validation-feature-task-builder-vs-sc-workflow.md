# Validation: /task-builder as the MINIMUM tasklist step for a multi-story feature (vs /sc:workflow)

**Date:** 2026-10-27
**Method:** read-only; every claim below is taken from a file read in this session. Paths under `~/.claude` = `/home/coder/.claude`.
**Status:** COMPLETE (all sections populated; no placeholders remain)

---

## Verdict

1. CONFIRMED, with one correction: `/task-builder` + `/task` is the right minimum for a multi-story feature. `/sc:workflow` + `/sc:implement` is not eligible as that minimum because the pair is sized for a one-or-two-session plan (HW:17, PT:13), mandates no codebase research and a structure-only gate (WP:72, QG:24-39, TPL:14), reviews one task at a time with one reviewer (QA:11), has no `--spec` flag and freezes after task 1 (WF:35-40, MW:42), and writes a plan that `/task` cannot run (QG:22, QG:29, HW:216).
2. Correction: multi-session resume is NOT the differentiator (both resume: TK:525-540, LG:89-106), and no file read defines "story" or gives a numeric story or file threshold. The on-disk switch is "many files, more than one session, or must not drift" (HW:18); levels 3 and 4 overlap at two sessions (HW:17 vs HW:18) and only "choose the heavier one" (HW:9) breaks the tie.
3. Table fixes needed in command-value-by-phase.md: the double-dagger on both rows (CV:110-111) says "same job", but at F size they are not; `/sc:implement` F=OPTIONAL (CV:143) is likely SKIP (JUDGMENT). Details in the "What to change" section.

## Evidence

**Citation key** (all paths absolute; line numbers are from the Read output in this session; "read fully" = every line read).

| Tag | File |
|---|---|
| TB | `/home/coder/.claude/skills/task-builder/SKILL.md` (2605 lines, read fully) |
| TK | `/home/coder/.claude/skills/task/SKILL.md` (640 lines, read fully) |
| WF | `/home/coder/.claude/commands/sc/workflow.md` (read fully) |
| WP | `/home/coder/.claude/skills/sc-workflow-protocol/SKILL.md` (read fully) |
| IN, PT, QG, TPL, RC, OR | `/home/coder/.claude/skills/sc-workflow-protocol/refs/` `input-parse.md`, `phase-templates.md`, `quality-gates.md`, `00_mdtm_template_simple_task.md`, `return-contract.md`, `overlap-routing.md` (each read fully) |
| IM | `/home/coder/.claude/commands/sc/implement.md` (read fully) |
| IS | `/home/coder/.claude/skills/sc-implement-protocol/SKILL.md` (read fully) |
| QA, LG, MW | `/home/coder/.claude/skills/sc-implement-protocol/refs/` `qa.md`, `ledger.md`, `managed-workspace.md` (each read fully) |
| HW | `/home/coder/.claude/HOW-WE-WORK.md` (327 lines, read fully) |
| RF | `/home/coder/.claude/commands/sc/reflect.md` (read fully; the backing `sc-reflect-protocol` skill was NOT read) |
| CV | `.../brainstorm-clay-feedback-decisions-2026-10-26/command-value-by-phase.md` (read fully) |

### E1. What each produces, and why the executors are not interchangeable

- `/task-builder` produces a **task folder** `.dev/tasks/to-do/TASK-RF-<subject>-YYYYMMDD-HHMMSS/` holding the MDTM task file `<TASK_ID>.md`, `research-notes.md`, `research/NN-<topic>.md`, `research/web-NN-*.md`, and `qa/*.md` reports (TB:152-181). User-invoked, it STOPS after the file is built; the user then runs `/task` (TB:12, TB:193). It "does NOT produce synthesis files, reviews, or final documents" (TB:166).
- The task file is a checklist: YAML frontmatter, then `## Phase N` with `- [ ] **N.M - title**` items each carrying Context, Action, Output, Verification, Completion gate (TB:2155-2209), plus a `## Task Log / Notes` section (TB:2262-2271). Granularity rule: one item per file or component, no batch items (TB:1122-1128, TB:2321).
- `/sc:workflow` produces a **package** `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` with `<id>.md` (schema `workflow-plan/1.2`), `source.md` (snapshot) and `return-contract.yaml` 1.1 (WF:12, WF:65; IN:35-40). `progress.md` and `artifacts/` are created later by `/sc:implement`, not by workflow (IN:40). It "does not implement code" (WF:12).
- The plan body is `## Phase N:` / `## Task N:` headings with `Acceptance criteria:` bullets, written from `00_mdtm_template_simple_task.md` (WP:42-44; QG:18). Checkboxes and numbered lines are forbidden anywhere in the plan "because /sc:implement enumerates them as tasks" (QG:29; TPL:12). No status field or verification task: "Final verification belongs to the executor" (QG:22; TPL:17). The template itself says "This is not an MDTM /task checklist" (TPL:22).
- **Size / session limits found.** Workflow: phase count capped by depth, quick 2-4, standard 4-8, deep 6-12, and the deep note reads "(split layers, still one session)" (WP:38; PT:13). No cap on task count found in WP, QG, PT, IN, TPL. Task-builder: tiers by file count (Quick <5 files, Standard 5-20, Deep 20+ files or multiple subsystems or multi-track, TB:134-146), max 5 tracks (TB:324), no cap on checklist items found. HW level 3 "fits in one or two sessions" (HW:17); level 4 "more than one session" (HW:18).
- **Why the pairings are fixed (by rule; not run, because this task is read-only).**
  1. `/task` validates its input: frontmatter with `id`, `title`, `status`, `created_date`; checklist items `- [ ]`/`- [x]`; a `## Task Log / Notes` section; otherwise it refuses to execute (TK:65-73). A workflow plan has none of `id`/`title`/`status` (its keys are schema, source, strategy, depth, slug, version, priority, created_date, QG:5-14), has no checkboxes (QG:29) and no status (QG:22). Docs also say it outright: "TASK-WF-* ... run them with /sc:implement, never with /task" (HW:216); "a TASK-WF-* package is an implement package, not an MDTM task file" (OR:11); "Next: /sc:implement ... (not MDTM /task)" (WF:80).
  2. `/sc:implement` will parse a task-builder file only as a flat list of `- [ ]` items ("Ignore MDTM fields ... MDTM-shaped files still use this protocol", IS:70-78), so it would treat each QA-gate and reflect item as a product task, and it explicitly refuses what makes the file MDTM: "Invoke /task", "Import MDTM F1, 6-agent phase gates, or /sc:reflect as the per-task gate" (IM:129-130; IS:170, IS:173; QA:11). Its progress is a separate ledger, not the file's checkboxes (LG:3-14), so the task file's own resume state would not be updated.
  3. The state stores differ: `/task` keeps state in checkboxes, frontmatter and the Task Log, re-read from disk every item (TK:87-99, TK:586-587); `/sc:implement` keeps state in `progress.md` plus git refs `refs/superclaude/implement/<slug>/T<id>` (IS:109-114; LG:89-106).
  4. The review models differ (see E2): panel of at least 6 agents per phase (TK:190-199) versus exactly one reviewer per task, "Never 2+ reviewer agents per task ... No 6-agent panel" (QA:11).

### E2. Research depth, quality gates, parallel agents, reviewer panels

**What `/task-builder` runs that `/sc:workflow` does not.**

- Scope discovery with Glob, Grep and codebase retrieval before anything is written (TB:337-339), a 7-category `research-notes.md` (TB:410-452), and a mandatory sufficiency gate with at most 2 gap-fill rounds (TB:454-477).
- Parallel researcher agents, all spawned in one message: at least 3 per track (File Inventory + Patterns & Conventions + Template & Examples, TB:370), scaled to 3-8 by complexity (TB:371), from 8 topic types (TB:357-366). Every claim must cite file path and line number, and doc-sourced claims are tagged CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED (TB:559-564, TB:618-636).
- Research gate before building: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative (TB:691); passes only if ALL pass (TB:865); up to 3 gap-fill rounds (TB:872); 10 agents when more than 6 research files (TB:863). **Internal inconsistency in TB:** the same section says the count scales with `qa_intensity` "lite: 2, standard: 3, full: 5" (TB:691, TB:693), while TB:204 and Critical Rule 7 say "minimum 5" (TB:2345). Which intensity a user-invoked build gets is UNVERIFIED (TB:1000 says it is "determined by calling skill's tier mapping or user override"). Optional web research: Standard 0-1 agents, Deep 1-2 (TB:138, TB:919-926).
- A separate builder agent (`rf-task-builder`) that reads all research files (TB:975-1249); retries: RESEARCH_NEEDED up to 2, MALFORMED up to 2, counted independently (TB:1258, TB:1264, TB:1269); retry-monotonicity halt guards (TB:1273-1313).
- Task-integrity gate on the built file: 2 rf-qa (A.10, TB:1319-1413) + 1 rf-analyst research-alignment (A.10.25, TB:1424-1473) + 2 rf-qa-qualitative (A.10.5, TB:1477-1625) = 5 agents, with serialized single-fix-agent protocol. A.10.5 also rejects a generated task file whose own QA gates have fewer than 6 agents (TB:2140, TB:2299).
- Then the PRE reflect gate (A.10.7, TB:1662-1703, see E4).
- Arithmetic from the file numbers (my sum, not stated in any file): researchers (3 at Quick, 4-5 Standard, 6-8 Deep) + research gate (2 to 5, see the inconsistency above) + 1 builder + 5 task-integrity (fixed, TB:1473). That is 11-14 agents at Quick, 12-16 at Standard, 14-19 at Deep. Excludes fix and verification agents, web agents, and reflect's own ensemble.
- Execution side, `/task`: phase-gate QA after every phase except Phase 1, at least 6 agents (3 rf-qa + 3 rf-qa-qualitative), scaling to 8/10/12 with output size (TK:188-199); intermediate gates at least 5 (TK:201-213); single fix agent then verification round, max 3 cycles then HALT (TK:249-254, TK:349-370); Post-Completion Validation with pre-checks, structural lenses, content lenses, fix protocol, and a source-fidelity gate with at least 2 agents (TK:284-347, TK:374-416); plus the templated POST reflect item (TB:2215-2240). Fewer than 6 agents at a gate "is a protocol violation" (TK:118, TK:199).

**What `/sc:workflow` does instead.**

- Six waves: Parse, Structure, Synthesize, Gate, Reflect, Contract (WP:20-66). Wave 1 starts from a "readable source" and a strategy skeleton (WP:34; PT:5-9). There is no research wave. "Will Not: ... new agents, Task fan-out" (WP:72).
- Discovery is pushed onto the author: "DO NOT invent requirements, paths, or APIs not found in the Source or the repo" (TPL:14); "name every file and source section it needs" (TPL:15); cite "relevant existing files when known" (TPL:35); "For multi-item work, list every item explicitly in the plan; do not leave discovery to the executor" (TPL:20). The protocol's allowed tools include Read, Glob, Grep (WP:4), so repo reading is permitted but no step mandates it. Whether it greps in practice: UNVERIFIED.
- The gate is structural: schema keys, headings, contiguous task numbers, phase count within cap, and (only at standard/deep) "every source requirement is covered by at least one task" (QG:24-39). `--depth quick` runs only schema-min (WP:52; QG:24-29), which does NOT include the requirement-coverage line (QG:39). HW tells level 3 users to use `--depth quick` (HW:17, HW:113, HW:305).
- The only independent reviewer on the plan is the Wave 4 reflect (E4), advisory.

**What `/sc:implement` does that `/task` has no equivalent for (reverse direction).**

- Per-task git snapshot pinned as a ref (`refs/superclaude/implement/<slug>/T<id>`) and a reviewer that diffs the task's increment against that task's AC, with `path:line` citations; a verdict with zero citations is invalid (IS:107-125; QA:9-33).
- Closed verdict set `compliant | missing | extra | misunderstood | cannot-verify`, one fix pass, then `E-HALT-QA`; completing a non-compliant task needs an operator-written Ruling line (QA:35-69).
- Extras: lint, typecheck, tests detected and recorded per task, never the verdict (IS:135-149).
- Plan tamper detection: `PLAN:` hash pin and `E-PLAN-CHANGED` after the first task starts (MW:42; LG:144).
- A fresh FINAL reviewer on every archive attempt and a no-replace archive helper (MW:44-62, MW:74-76).
- `/task` reviews phase outputs against "ensuring..." clauses and lens checklists (TK:217-244); I found no per-task diff snapshot or `extra`-scope detection in TK. Neither side is a strict superset: task-builder + `/task` buys upfront evidence, spec tracing and phase panels; workflow + `/sc:implement` buys per-task diff conformance. Research and spec tracing are the part that matters when stories touch many files or modules.

### E3. Resumability and multi-session behavior

| Aspect | `/task-builder` + `/task` | `/sc:workflow` + `/sc:implement` |
|---|---|---|
| Resume while BUILDING the plan | Yes. Resume point is chosen from which files exist in the task folder (no task folder, research-notes In Progress or Complete, research without qa, qa without task file, task file without validation reports, and so on to A.11) (TB:213-220, TB:263-275, TB:2503-2517). Existence-only; the orchestrator re-reads verdicts (TB:2517). | No. Generation is one run. A re-run creates a NEW package; it "never overwrites or reuses an existing package" (WF:65; WP:70; IN:16-21). A failed generation leaves a `failed` contract and no valid plan (QG:41; RC:29). |
| Resume while EXECUTING | Re-read the task file, first unchecked `- [ ]`, never re-execute `- [x]`, read prior outputs for context (TK:525-540, TK:620-640). Session end rules: all outputs on disk, update `updated_date`, tell the user the resume command (TK:631-636). | Ledger `progress.md`; first task whose latest status is not `complete`; `--resume` is implicit when a ledger exists (LG:89-106; IM:57). N>=20 prints "compaction likely; ledger is the source of resume" and does not stop or split (IS:65). Git pins survive `git gc` (IS:109-114). |
| Mid-feature amendment by the operator | Allowed: add a missing requirement as a new unchecked item in the right phase, then re-run `/task`; write answers under open questions (HW:102, HW:190). | Not after task 1 starts: "Do not edit the plan after the first step starts; the tool stops with E-PLAN-CHANGED" (HW:117; MW:42). Add missing requirements "before its first step starts" (HW:194). |
| Where the executor may halt | Only: all remaining items blocked, a phase gate failing 3 fix cycles, or an item invalidating the rest (TK:120, TK:616). No pausing for scope or cost (TK:120). | `E-HALT-QA` after one failed fix pass; operator Ruling needed to continue (QA:61-69). |
| Closing | Folder stays in `to-do/` after `/task` (HW:83). | Moves to `.dev/tasks/done/` after a fresh FINAL, Linux only; elsewhere "archive-blocked" by design (HW:17, HW:256; MW:44-62, MW:76). |

Conclusion for (3): execution-time resume exists on BOTH sides, so it cannot be the reason workflow is ineligible. What differs is (a) build-time resume exists only for task-builder, (b) the task file accepts operator amendments mid-feature while a managed plan freezes after task 1, and (c) the review that guards each resumed session (phase panels versus one reviewer per task).

### E4. Spec checking: `--spec` and `reflect_pre` versus `/sc:workflow`'s automatic check

**`/task-builder`**

- `--spec <path>` is resolved in order: explicit flag, `@file` in the goal, `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST, else none; stored as `spec_path:` in the task frontmatter (TB:41, TB:285).
- Gate A.10.7 runs after the 5-agent task-integrity gate: `--mode pre --remediate [--spec] --tasklist <file> --depth <TCS-derived> --output ${TASK_DIR}reflect/pre/` (TB:1662-1676). Default coverage floor 0.90 (TB:1682; RF:102). `coverage_pct >= floor` and status not failed gives `verdict: pass`; otherwise `fail`, and the `unmapped_requirements` are APPENDED to `### Open Questions` without touching existing items (TB:1682-1683). No auto-loop back to the builder (TB:1703). HW restates it: "If the check fails (less than 90% of requirements covered), the missed requirements are added to the task file's Open Questions. Without --spec this check is skipped" (HW:102).
- The sign-off is a frontmatter block `reflect_pre` with `verdict`, `skip_reason`, `coverage_pct`, `depth`, `tcs`, `tier_reached`, `run_id`, `report`, `reviewed_at` (TB:1688-1698).
- It is mandatory, and enforced on disk: when a spec resolves, `verdict: skipped` is forbidden and the check requires `${TASK_DIR}reflect/pre/report.md` to exist and `run_id` to be a real run id; a `tcs` of 0 or a depth or tier below what the TCS band mandates makes the run MALFORMED and A.11 must not be presented (TB:1664, TB:1666, TB:1701). Substituting another gate's result is "explicitly NOT permitted" (TB:1701). `skipped` is legal only with `skip_reason: no-spec` (TB:1666, TB:1684).
- Depth is computed, not guessed: TCS = 3*S1 + 4*S2 + 2*S3 + 2*S4 + 5*S5 + 4*S6 (files, subsystems, FR/NFR in spec, dependencies, open-question items, refactor class); <=12 quick, 13-34 standard, >=35 deep (Tier 2 forced); overrides O1-O4 (TB:2410-2441).
- Other spec-adjacent checks inside the build: A.10.25 research-alignment (every research finding has an item, no item is unsupported, TB:1451-1461) and the drift axis in A.10.5, anchored on the BUILD_REQUEST GOAL verbatim (TB:1559-1562).
- Execution side: the POST reflect item audits the executed work (skill mode: dedicated subagent with `--spec` threaded; cli mode: `superclaude reflect run ... --depth deep --fix --promote`, audit base from `start_commit`) and writes `reflect_post` (TB:2215-2240, TB:2385-2393). `/task` must open the reflect return contract and fail the gate on non-pass verdicts, drift or regression counts (TK:576).

**`/sc:workflow`**

- There is no `--spec` flag. Flags are `--strategy`, `--depth`, `--handoff` (WF:35-40). The "spec" is the source argument (file or inline prompt), snapshotted to `source.md` (WP:24).
- Gate (Wave 3) is structure plus, at standard/deep only, requirement coverage against that source (QG:31-39). At quick it is schema-min (WP:52; QG:24-29).
- Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` with "defaults for every other flag, no --remediate" (WP:56). Reflect's own defaults: `--depth standard` (Tier 1, escalate by rubric), coverage floor 0.90 (RF:98, RF:102). Result handling: only `reflect_status` and `reflect_report_path` are recorded in `return-contract.yaml` (RC:16-17); the fields are "additive and advisory: they never change status" (RC:21; WP:58). If reflect is unavailable or failed, the run records `skipped|failed` and still proceeds (WP:58). The contract has no `coverage_pct`, `verdict` or `tier_reached` field (RC:5-19). Whether the report file itself shows coverage: UNVERIFIED (sc-reflect-protocol not read; RF:138 says the command surfaces `coverage_pct` for UC-1).
- When the source is an inline prompt, the check is "plan covers the prompt", not an independent spec: HW says so, "it was checked against your request when it was written ... If a separate spec, PRD, or TDD exists beyond your request, run the check below against that spec" (HW:191), and the manual route is `/sc:reflect --mode pre --spec <spec> --tasklist <plan>` (HW:193).
- No enforcement step equivalent to the Mandatory-run check was found: nothing blocks `/sc:implement` when reflect was skipped or low-coverage (WP:56-58, RC:21).

**Net:** `/task-builder` makes spec coverage a recorded, floor-gated, disk-verified sign-off with a computed depth; `/sc:workflow` makes it an advisory printout against whatever source it was handed. For a multi-story feature with a driving spec, only the first can claim "every requirement has a task, verified".

## Side-by-side table

Every cell is from a file cited in the Evidence section; "none found" means absent from the files read, not proven absent elsewhere.

| Dimension | `/sc:workflow` + `/sc:implement` | `/task-builder` + `/task` | Source |
|---|---|---|---|
| Level in the guide | 3, "simple checked plan": a few files, clear requirements, one or two sessions | 4, "build and run a task file": many files, more than one session, or must not drift | HW:17, HW:18 |
| Input | Exactly one of: file path or inline prompt | GOAL (mandatory), WHY, WHERE, BUILD_REQUEST path, `--spec`, `--cli` | WF:18-22; TB:31-43 |
| Output folder | `.dev/tasks/to-do/TASK-WF-<camelSubject max 16>-<UTC YYYYMMDD-HHMMSS>[-2..-9]/` | `.dev/tasks/to-do/TASK-RF-<kebab subject>-<YYYYMMDD-HHMMSS>/` (multi-track: `TASK-RF-track-T-...`) | IN:16-21; TB:152-164, TB:183 |
| Plan file shape | `<id>.md`, schema `workflow-plan/1.2`; headings `## Phase N:` / `## Task N:` + `Acceptance criteria:`; no checkboxes, no status | MDTM task file: frontmatter + `- [ ]` items (Context, Action, Output, Verification, Completion gate) + Task Log | QG:5-29; TB:2155-2271 |
| Size limits found | Phases: quick 2-4, standard 4-8, deep 6-12, "still one session"; no task cap found | Tiers Quick <5 files, Standard 5-20, Deep 20+ or multi-subsystem or multi-track; max 5 tracks; no item cap found | PT:13; TB:134-146, TB:324 |
| Codebase research | None mandated; tools permitted, use UNVERIFIED | 3-8 parallel researchers per track, evidence with file:line, CODE-VERIFIED tags | WP:72, WP:4; TB:370-371, TB:559-564 |
| Agents the planner itself spawns | None ("no new agents, Task fan-out"); only Wave 4 reflect, which spawns its own | About 11-19 depending on tier (my arithmetic, E2): researchers + research gate (2-5) + builder + 5 task-integrity, plus fix/verify, web, reflect | WP:72; TB:691, TB:693, TB:1473 |
| Plan gate | quick = schema-min; standard/deep = structure + requirement coverage vs source | Research gate (2-5 agents by intensity) + task-integrity gate (5) + PRE reflect with floor 0.90 | WP:52; QG:24-39; TB:691, TB:693, TB:1473, TB:1682 |
| Spec input | Source argument only; no `--spec` | `--spec <path>`, recorded as `spec_path:` | WF:35-40; TB:41 |
| Spec-check record | `reflect_status`, `reflect_report_path` in `return-contract.yaml`; advisory; never changes status | `reflect_pre{verdict, coverage_pct, depth, tcs, tier_reached, run_id, report}` in task frontmatter; mandatory; disk-verified | RC:16-21; TB:1688-1701 |
| Executor | `/sc:implement <pkg>/<id>.md` | `/task <task file>` | WF:80; TB:1755 |
| Per-unit review | One reviewer per task vs that task's diff since a git snapshot; closed verdict set; one fix pass | Per item: evidence + "ensuring" clause; per phase (2+): panel of at least 6 agents, single fix agent, up to 3 cycles | QA:9-69; TK:188-254 |
| Whole-run review | One fresh FINAL reviewer + archive helper (Linux) | Post-completion: structural + content lenses + source-fidelity gate + POST reflect (`reflect_post`) | MW:44-62; TK:284-347, TK:374-416; TB:2215-2240 |
| State store | `progress.md` ledger + git pin refs | Checkboxes + frontmatter + Task Log in the task file | LG:89-106; IS:109-114; TK:87-99 |
| Resume: build | No (new package each run) | Yes, by artifact state | IN:16-21; TB:2503-2517 |
| Resume: execution | Yes, first non-complete task | Yes, first unchecked item | LG:89-106; TK:525-540 |
| Plan changes during the run | Frozen after first task start (`E-PLAN-CHANGED`) | Operator may add unchecked items | MW:42; HW:117, HW:102 |
| Commits | Never (`/sc:implement` does not commit) | `/task` does not commit | IM:131; HW:81 |
| Docs' stated use | Few files, clear scope, 1-2 sessions | "Many files, multi-session work, or anything that must not drift" | HW:243, HW:305-306 |
| Measured cost or time | Not in any file read: UNVERIFIED | Not in any file read: UNVERIFIED | - |

## Complexity signals where the choice flips

**What the files actually give.** No file defines "story" or "multi-story". No file gives a number of stories, files or modules at which to switch commands. The only text that decides the switch is HW, and it uses unquantified words ("a few", "many"). Everything numeric below is either (a) a number the files DO state, labelled with its source, or (b) my suggestion, labelled JUDGMENT.

| Signal | What the files say | Where the choice flips | Basis |
|---|---|---|---|
| Size of change | Any work with more than 5 edits or more than one source file (its test file excluded) "must go through a written plan"; "level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier" | "A few" to "many" is undefined. The only countable thing in the files is the "more than one source file" line, and that decides plan versus no plan, not level 3 versus 4 | HW:22 |
| Sessions | Level 3 "one or two sessions"; level 4 "more than one session" | Two sessions fits both rows. Tie-break: "If you are unsure between two rows, choose the heavier one" | HW:17, HW:18, HW:9 |
| Phase count | Workflow plans are capped at 12 phases (deep) and described as "still one session" | A plan that needs more than 8 phases (standard cap) forces `--depth deep`; more than 12 cannot be expressed. The "more than 8 means switch" rule is JUDGMENT; the caps are from the files | PT:13; WP:38 |
| Cross-cutting or structural change | "Large refactors (many files or a structural change): treat it as a feature ... build a task file with /task-builder ... --spec"; bug fixes "larger or riskier" go to task-builder | Cross-cutting = flips to task-builder. Phrase is doc text; no count | HW:168, HW:133 |
| Need for research | Level 5: when you do not know how the system works, research first, then `/task-builder` | If the author cannot name the files and modules, workflow has no discovery step (TPL:20 pushes discovery to the author), task-builder has researchers (TB:357-371). Flip = JUDGMENT, built from those two facts | HW:19; TPL:20; TB:294-296 |
| Driving spec, PRD or TDD to trace | Feature-existing route: `/task-builder ... --spec <spec file>` | If a spec must be traced requirement by requirement, only task-builder takes it as `--spec` and records coverage | HW:102, HW:307; TB:41 |
| Must not drift from what was agreed | Level 4 trigger; mix-up table says the same | Flip to task-builder. No metric given | HW:18, HW:243 |
| Risk | "larger, longer, or riskier" goes to level 4. Workflow's `--strategy enterprise` adds a risk/ops column and a rollout phase, forces depth deep | Enterprise changes the plan text, not the review: the executor still uses one reviewer per task (QA:11). So enterprise does not substitute for task-builder. Inference from PT:9, WP:28, QA:11 | HW:22; PT:9 |
| Independence of stories | Task-builder splits into up to 5 tracks only if each track has its own goal, different source files, different outputs and no dependency; default is single track | Independent stories can become parallel task files in one run. Whether to prefer that over N separate workflow runs: JUDGMENT (the only feature-level spec trace is the task-builder one, and N workflow runs leave N unrelated packages) | TB:311-324; IN:16-21 |
| Plan likely to be amended mid-run | Task files accept new unchecked items; managed plans do not after task 1 | If open questions are expected to surface during the feature, flip to task-builder. JUDGMENT | HW:102, HW:117; MW:42 |

**Rule as written on disk (no invention):** use `/sc:workflow` only when ALL of: few files, clear scope, fits one or two sessions, and nothing in it "must not drift" (HW:17, HW:22). Anything larger, longer or riskier is level 4 (HW:22). Unsure: pick the heavier (HW:9).

**Rule I suggest for a multi-story feature (JUDGMENT):** a feature of two or more stories goes to `/task-builder` when any of: (1) the stories touch two or more subsystems, using the TCS counting rule "first 2 path segments" as a way to count (TB:2411); (2) a driving spec exists; (3) more than two sessions are expected; (4) the files cannot be named up front; (5) the stories share an interface and need one consistent plan. A feature that is really one story, or several fully independent single-subsystem stories, each within one or two sessions and with no driving spec, may run as separate `/sc:workflow` plans, but then no feature-level coverage check exists (each package checks only its own source).

**Note on cost.** Task-builder has no lightweight mode: even its Quick tier (<5 files, single concern) still runs a research gate, the 5-agent task-integrity gate and the PRE reflect (TB:136, TB:691, TB:1473; arithmetic in E2), and `/task` then adds phase-gate panels of at least 6 agents (TK:188-199). That is the cost side of choosing it for a small story, and a plausible reason the guide keeps workflow for level 3 (the guide does not state this reason: JUDGMENT).

### Is `/task-builder` ever justified on a SINGLE story?

Yes, on the files' own terms, when the story itself trips a level-4 trigger. Conditions from the files:

1. The story will take more than one session (HW:18). At exactly two sessions it also fits level 3 (HW:17); the tie goes to the heavier row (HW:9). CV:254 already lists "if the story is multi-session".
2. The story must not drift from what was agreed, and an agreed spec exists to trace with `--spec` (HW:18, HW:102).
3. The story is "larger or riskier" than a few files with clear scope (HW:22, HW:133, HW:168).
4. The story needs codebase discovery the author cannot do up front (HW:19 research-first, then `/task-builder`; workflow has no research step, TPL:20).

Not justified: a story that is a few files, clear scope, at most two sessions, and has no spec to trace (the level-3 row, HW:17). Cost counter: see "Note on cost" above. Which of conditions 1-4 counts as "high risk" is not defined in any file: JUDGMENT.

## Flags that matter

Each flag below was found on disk. "Changes outcome" is stated from the cited line, not from running the command.

### `/task-builder` (a skill; its frontmatter has only `name` and `description`, no `argument-hint`, TB:1-4; the flags are documented in its Input section)

| Flag or input | Default | What it changes | Source |
|---|---|---|---|
| GOAL (positional text) | required | Scope of the task file. If missing the skill asks and does not proceed | TB:33, TB:100-111 |
| WHY, WHERE (source directories) | optional | Narrow and shape research; WHERE "saves significant research time" | TB:35-37 |
| BUILD_REQUEST file path | none | Structured request; `Source: skill-delegated` skips scope discovery and researchers (`SKIP_RESEARCHERS` defaults true then) | TB:39, TB:47-61 |
| `--spec <path>` | none (resolved: flag, `@file` in goal, `SPEC:`/`PRD:`/`TDD:` in BUILD_REQUEST, else none) | Turns on the mandatory PRE reflect coverage gate and `spec_path:`; without it `reflect_pre.verdict` is `skipped` (reason `no-spec`); in skill mode also feeds the POST item | TB:41, TB:1666, TB:1684; HW:102 |
| `--cli` | OFF | POST gate becomes a flat `superclaude reflect run ... --depth deep --fix --promote` shell-out; adds `start_commit` and `executor_model_class` to frontmatter; fixed depth deep; only this path is "session-validated end-to-end" | TB:43, TB:2168-2170, TB:2385-2398 |
| BUILD_REQUEST `CLI_MODE: true` | false | Same as `--cli` | TB:59, TB:286 |
| BUILD_REQUEST `SKIP_RESEARCHERS` | true when delegated, false when user-invoked | Skips researcher layer | TB:58 |
| Words "thorough", "comprehensive", "deep dive" in the request (not a flag) | none | Force the Deep tier | TB:143 |
| Request shape (not a flag) | single track | Independent work streams may split into up to 5 tracks | TB:311-324 |
| `qa_intensity`, `QA_GATE_REQUIREMENTS`, `VALIDATION_REQUIREMENTS`, `TESTING_REQUIREMENTS`, `POST_REFLECT_GATE` (BUILD_REQUEST fields set by the orchestrator, not typed by the user) | see TB:1000-1088 | QA agent counts in the generated file; whether tests and validation items are encoded; whether the POST reflect item exists | TB:1000-1088 |

No `--depth`, `--quick` or tier flag exists; tier is chosen by the skill (TB:140-146).

### `/task`

No flags. Input is a task-file path or an identifier; with none it searches `.dev/tasks/to-do/` for status "Doing" (TK:29-52). Behaviour switches come from the task file (e.g. `reflect_post_mode`), not from the command.

### `/sc:workflow`

| Flag | Default | What it changes | Source |
|---|---|---|---|
| `<path>` or `<prompt>` | exactly one required | Source snapshotted to `source.md`; bare invocation stops with `E-NO-SOURCE` | WF:18-22; IN:5 |
| `--strategy systematic\|agile\|enterprise` | systematic | Phase skeleton; enterprise adds a risk/ops column and a rollout phase and, if depth was omitted, sets depth deep | WF:38; PT:5-9; WP:28 |
| `--depth quick\|standard\|deep` | standard | Phase cap (2-4 / 4-8 / 6-12) and gate strictness: quick = schema-min, others = full incl. requirement coverage | WF:39; WP:38, WP:52; QG:24-39 |
| `--handoff none\|design\|implement\|tasklist` | none | `implement` invokes the implement skill after the contract is written; others only print text | WF:40; WP:60-66; OR:7-12 |
| Banned: `--parallel`, `--validate`, `--depth shallow\|normal`, `--output` | - | Stop `E-LEGACY`, no package created | WF:42; IN:9-12 |

### `/sc:implement`

| Flag | Default | What it changes | Source |
|---|---|---|---|
| `<path>` / `--spec` / `--prd` / `--tasklist` (aliases for one file) or `<prompt>` | one required | Source; an inline prompt is persisted to `.dev/implement/<slug>/source.md` | IM:51-56; IS:60 |
| `--resume` | implicit if a matching ledger exists | Continue from first non-complete task | IM:57 |
| `--ledger <path>` | `.dev/implement/<slug>/progress.md` | Must be under `.dev/implement/`; managed packages always use sibling `progress.md`, any other value stops | IM:58 |
| `--skip-final-review` | off | Skips the whole-list pass; on a managed package it blocks archiving | IM:59; MW:51 |
| Banned: `--type`, `--framework`, `--safe`, `--with-tests`; `--force` | - | `E-LEGACY`; `--force` gives `E-NO-RULING` | IM:61; IS:49 |

### `/sc:reflect` (called by both, with different flags)

Workflow calls it with `--mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, defaults otherwise, no `--remediate` (WP:56). Task-builder calls it with `--mode pre --remediate [--spec] --tasklist --depth <TCS-derived> --output ${TASK_DIR}reflect/pre/` (TB:1670-1676). Relevant defaults: `--depth standard`, `--tier auto`, `--coverage-floor 0.90`, `--remediate` false, `--no-promote` false (RF:98-99, RF:102, RF:110, RF:112). Full flag list: RF:86-116.

## Footprint a checker could see

All items come from the stated output paths and frontmatter keys in the files cited; none was observed by running a command. Both leave files under `.dev/tasks/`, which the repo `CLAUDE.md` says must always be staged.

### `/task-builder` leaves

| Footprint | Where it is stated |
|---|---|
| Folder `.dev/tasks/to-do/TASK-RF-<subject>-YYYYMMDD-HHMMSS/` (multi-track: `TASK-RF-track-T-...`) | TB:152-164, TB:183 |
| `<TASK_ID>.md` task file; `research-notes.md` (status Complete); `research/NN-*.md` (3-8 files per track, each ending `Status: Complete`); optional `research/web-NN-*.md` and `NN-gap-fill.md` | TB:168-173, TB:2484-2486 |
| `qa/analyst-completeness-report.md`, `analyst-cross-validation-report.md`, `qa-research-evidence-report.md`, `qa-research-gap-report.md`, `qa-research-depth-report.md` (research gate); `qa-task-validation-b2-report.md`, `qa-task-validation-structure-report.md`, `qa-task-validation-consolidated.md`, `qa-task-research-alignment-report.md`, `qa-qualitative-operational-report.md`, `qa-qualitative-sufficiency-report.md`, `qa-qualitative-consolidated.md` (task gate). Each carries a line-anchored `VERDICT: PASS|FAIL` | TB:174-181, TB:1420 |
| Task frontmatter: `id: TASK-RF-...`, `status`, `reflect_post_mode: skill\|cli` (ALWAYS emitted, so a stable fingerprint of a task-builder output), `spec_path:`, `reflect_pre{verdict, skip_reason, coverage_pct, depth, tcs, tier_reached, run_id, report, reviewed_at}`; CLI mode adds `start_commit`, `executor_model_class` | TB:2155-2178, TB:1688-1698 |
| `reflect/pre/report.md` under the task folder when a spec resolved; hard-checked on disk, so absence with a non-skipped verdict means a MALFORMED build | TB:1675, TB:1697, TB:1701 |
| Open Questions section: unmapped requirements appended when PRE reflect fails | TB:1683 |
| After `/task`: checked boxes, `status` and `completion_date`, Task Log entries, `reflect_post{verdict, run_id, report}` in frontmatter, `qa/qa-structural-*`, `qa-content-*`, `qa-final-*` reports; skill-mode POST artifacts under the runner's `{OUTPUT_DIR}`; CLI-mode POST artifacts under `<task-dir>/reflect/post/<short-sha>/` (`adversarial/merged-verdict.yaml`, `reviewer-cards/`, `audit.log`) | TK:166-171, TK:234, TK:312, TB:2231-2239 |

Checker caveats: (a) the `TASK-RF-` prefix is not universal. A skill-delegated build uses the caller's pre-created directory and "does NOT create TASK-RF-*" (TB:55); other prefixes seen in the files are `TASK-ROADMAP-`, `TASK-RESEARCH-`, `TASK-TECHREF-` (HW:19, HW:76; TB:71). A checker should key on task-file frontmatter (`reflect_post_mode`, `reflect_pre`) rather than the directory glob. (b) `reflect_pre.verdict: skipped` with `skip_reason: no-spec` means the build had no `--spec` (HW:192). (c) `.dev/tasks/done` entries exist in the repo (CV:27), but `/task` itself leaves the folder in `to-do/` (HW:83), and promotion belongs to reflect `--promote` (TB:2237; RF:112); I did not verify which path moved those 33 entries.

### `/sc:workflow` (+ `/sc:implement`) leaves

| Footprint | Where it is stated |
|---|---|
| Folder `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>[-2..-9]/` containing `<id>.md` (frontmatter `schema: workflow-plan/1.2`, `slug: <id>`), `source.md`, `return-contract.yaml` | IN:16-21, IN:35-40; QG:5-14 |
| `return-contract.yaml`: `contract_version: "1.1"`, `status`, `slug`, `handoff_action`, `reflect_status`, `reflect_report_path`, `unresolved` | RC:5-19 |
| After `/sc:implement`: `progress.md` (header, `PLAN: sha256=... source_sha256=...`, `T<id>: start sha=...`, `T<id>: complete verdict=... ac=... evidence=... extras=... files=...`, `FINAL: pass\|issues ... state=...`, `ARCHIVE: start id=... token=...`) and `artifacts/` | LG:134-157; IN:40 |
| Git refs `refs/superclaude/implement/<slug>/T<id>` while a task is in flight (deleted on `complete`) | IS:109-114 |
| Package moved to `.dev/tasks/done/<id>/` after a FINAL pass (Linux only; elsewhere stays in `to-do/` as archive-blocked) | MW:44-62, MW:76; HW:17 |
| Legacy (non-managed) sources: ledger at `.dev/implement/<slug>/progress.md`, `source.md` there for inline prompts | LG:5-13; IS:60 |
| Reflect output for the Wave 4 pre-check: default `.dev/reflect/pre-<name>-<timestamp>/` (path printed with the plan) | RF:101; WP:56 |

Checker caveat: the ledger header says "Do not `git add` the ledger" (LG:3), which sits against the repo `CLAUDE.md` rule that `.dev/tasks/` is always staged (managed `progress.md` lives under `.dev/tasks/`). I did not resolve how the two interact: UNVERIFIED.

### Distinguishing the two lanes in one scan

`TASK-WF-*` folder with `source.md` + `return-contract.yaml` = workflow lane. Task file with `reflect_post_mode` in frontmatter, with `research/` and `qa/` siblings = task-builder lane. A feature built in the task-builder lane should show `reflect_pre.verdict` of `pass` or `fail` with a real `run_id` (a `skipped` means no spec was passed); a feature built in the workflow lane has no equivalent coverage number in its contract (RC:5-19).

## What to change in command-value-by-phase.md

Line numbers are in `command-value-by-phase.md` (CV). Nothing was edited there; these are proposals for the lead. Items marked JUDGMENT are my recommendation, not a fact on disk.

| # | CV line | Current | Proposed change | Why (evidence) |
|---|---|---|---|---|
| 1 | CV:110, `/sc:workflow` row, F column | `OPTIONAL` | `SKIP` as the feature-level tasklist step (JUDGMENT). If the lead prefers to keep `OPTIONAL`, the Notes cell must say "per story only, never the feature minimum" | Not eligible as the F minimum: no research wave (WP:72, TPL:14, TPL:20); gate is structural and at `--depth quick` skips requirement coverage (QG:24-39); no `--spec` (WF:35-40); frozen after task 1 (MW:42); sized for 1-2 sessions (HW:17, PT:13) |
| 2 | CV:110, Notes | "plan is auto-checked against the request ... ‡ with `/task-builder`" | Replace "auto-checked" with "checked by an advisory `/sc:reflect --mode pre` against its own source only; recorded as `reflect_status` in `return-contract.yaml`, never blocks". Replace the double-dagger with "overlaps `/task-builder` at S size only" | WP:56-58; RC:16-21; HW:191 |
| 3 | CV:111, `/task-builder` row, Notes | "... ‡ with `/sc:workflow`" | Replace the double-dagger with "overlaps `/sc:workflow` at S size only". Add: "F minimum because it alone runs codebase research (3-8 researchers), a 5-agent task-integrity gate, and a mandatory `--spec` coverage sign-off (`reflect_pre`); `/task` then reviews every phase after the first with at least 6 agents" | TB:357-371, TB:1473, TB:1664-1701; TK:188-199 |
| 4 | CV:111, S column `WORTH IT` | no condition given | Add condition list: story spans more than one session; a spec must be traced; story is larger or riskier; files cannot be named up front. At exactly two sessions both rows fit and the guide says pick the heavier | HW:9, HW:17, HW:18, HW:22, HW:102 |
| 5 | CV:143, `/sc:implement` row, F column | `OPTIONAL` | `SKIP` (JUDGMENT), Notes: "walks `TASK-WF-*` plans only; do not use on a task-builder file" | HW:216; OR:11; IM:129-130; IS:170, IS:173 |
| 6 | CV:144, `/task` row, Notes | "... ‡ with `/sc:implement`" | Add: "runs only task-builder-shaped files (frontmatter id/title/status, `- [ ]` items, Task Log); cannot run a `TASK-WF-*` plan, which has none of them"; replace the double-dagger with "S size only" | TK:65-73; QG:22, QG:29; HW:216 |
| 7 | CV:50, double-dagger legend | "two commands do the same job and the team does one of them" | Add: "a pair marked double-dagger can differ in depth at larger sizes; the Notes column names the size at which they actually overlap" | Rows 110/111/143/144 are the cases |
| 8 | CV:232, O6 "Turn spec into steps" | "By size: `/sc:workflow` (S), `/task-builder` (F, R) ..." Why: "Guide section 5 table" | Add the three reasons: research (task-builder only), spec trace (`--spec` only), phase panels versus one reviewer per task. Add the tie rule from HW:9 | E2, E4 in this file |
| 9 | CV:233, O7 "Execute the steps" | executor matches the input file | Add "task-builder file: never `/sc:implement`; `TASK-WF-*`: never `/task`" with the two source lines | HW:216; IM:129-130 |
| 10 | CV:254, Single story row, "WORTH IT additions" | "`/task-builder` + `/task` instead of steps 1-3 if the story is multi-session" | Extend to the four conditions in row 4 above | HW:18, HW:102, HW:133 |
| 11 | CV:255, Multi-story feature row, task-file lane | steps 1-4 listed | Add to step 1: "the spec file is what lets step 2's `--spec` produce a coverage number; without it `reflect_pre.verdict` is `skipped` and nothing was coverage-checked (run `/sc:reflect --mode pre` by hand)". Add to step 3: "`reflect_pre.verdict`, `coverage_pct`, `run_id`" | HW:102, HW:192; TB:1688-1698 |
| 12 | CV:266, `/sc:workflow` footprint row | `.dev/tasks/to-do/TASK-WF-*/<id>.md`, `progress.md`, `return-contract.yaml` | Add `source.md`; contract fields `reflect_status`, `reflect_report_path`; ledger lines `PLAN:`, `T<id>:`, `FINAL:`, `ARCHIVE:`; git refs `refs/superclaude/implement/*`. Say: no coverage number in the contract | RC:5-19; LG:134-157; IS:109-114 |
| 13 | CV:267, `/task-builder` footprint row | "task file under `.dev/tasks/to-do/` with a `reflect_pre` block" | Add: `TASK-RF-*` folder with `research/` and `qa/` (file names in TB:174-181), frontmatter `reflect_post_mode` (always), `spec_path:`, `reflect_pre` fields; caveat that delegated builds use the caller's prefix | TB:152-181, TB:2168, TB:55 |
| 14 | CV:124, `/sc:reflect` row, Notes, "S: `/sc:workflow` already self-checked" | - | Qualify: "advisory, against its own source" | RC:21; HW:191 |
| 15 | CV:281, Section 5 intro | "For ... `/sc:implement`, `/sc:workflow` ... I read only the usage and flag lines" | Update: both command files, their protocol skills and all their refs have now been read in full (this file); `/sc:reflect`'s backing skill still not read | This file's citation key |
| 16 | CV Section 5 (add rows) | - | Add the unverified items listed below: workflow repo-grep in practice, `qa_intensity` for user-invoked builds, two-session overlap | Unverified section below |

Rows 1 and 5 change a rating; the rest change wording. If the lead keeps `OPTIONAL` in rows 1 and 5, the Notes must still carry the reasons in rows 2, 3 and 6, otherwise a checker reading the table cannot tell the feature-minimum from the story-minimum.

## Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| V1 | Whether `/sc:workflow` reads the repo (Grep/Glob) while writing a plan | WP lists Read, Glob, Grep as allowed tools (WP:4) but no wave mandates repo research; no run observed (read-only task) | Inspect a few existing `TASK-WF-*` plans for file:line grounding, or run once |
| V2 | What `/sc:implement` and `/task` actually do when given the other's file | By-rule reading only (E1); nothing was run | A dry run on a throwaway copy |
| V3 | Which `qa_intensity` (lite 2, standard 3, full 5 research-gate agents) a user-invoked `/task-builder` gets | TB contradicts itself: TB:691/693 scale by intensity, TB:204 and TB:2345 say minimum 5; TB:1000 says the intensity comes from a caller's tier mapping or user override | Read `rf-task-builder` agent file or a built task file's BUILD_REQUEST; ask the maintainers |
| V4 | Agent counts and costs | My sums from the file numbers (E2); excludes fix, verify, web and reflect agents; no cost or duration is stated in any file read | Count spawn logs in an existing `TASK-RF-*/qa/` folder |
| V5 | Contents of the reflect report for a workflow plan (does it show `coverage_pct`?) and reflect's default tier behaviour | Only `commands/sc/reflect.md` was read; `sc-reflect-protocol/SKILL.md` was not | Read that skill, or open a `.dev/reflect/pre-*` report |
| V6 | Whether a hook or CI check enforces the HW routing (HW:22 "Hard limit") | The text is guidance; no detector was read. The freshness hook that blocked one of my edits is unrelated | Search `~/.claude/hooks/` and `.github/` |
| V7 | Directory contents of `~/.claude/skills/task-builder/` and `~/.claude/skills/task/` beyond `SKILL.md` | I did not enumerate directories (no commands allowed). TB's text points to MDTM templates at `.claude/templates/workflow/01_...` and `02_...` and to `rf-qa.md` (TB:655-661, TB:1616) which I did not open; templates may add rules | List and read those files |
| V8 | Where "story" is defined | Not defined in any file read; "multi-story" is the lead's term. HW uses files, sessions and drift. The BMad lane uses `_bmad-output/implementation-artifacts/` story files (CV:26) | Lead's definition |
| V9 | The two-session overlap: whether the team intends level 3 or level 4 | HW:17 and HW:18 both fit; only the generic tie-break (HW:9) applies | Lead's ruling, then edit the HW wording |
| V10 | Archive helper behaviour and the Linux-only claim | Stated in MW:76 and HW:17; `archive_workspace.py` not read | Read the script and `tests/skills/test_workflow_archive.py` |
| V11 | Which command moved the 33 entries in `.dev/tasks/done` | `/task` leaves folders in `to-do/` (HW:83); reflect `--promote` moves them (RF:112, TB:2237); not checked | `git log` on `.dev/tasks/done` |
| V12 | Interaction of "Do not `git add` the ledger" (LG:3) with repo rule "`.dev/tasks/` is always staged" for a managed `progress.md` | Both read; behaviour not observed | Run a managed plan once, or ask the maintainers |
| V13 | Whether home-directory skills here match other engineers' (the checker may run elsewhere) | `~/.claude/` is per-user (CV:23, CV Section 5 U17); this validation reflects this machine only | Compare installs |
| V14 | The suggested thresholds in the Signals section (more than 8 phases, two or more subsystems, more than two sessions) | They are marked JUDGMENT; none comes from a file | Lead's decision |

**Coverage statement.** Fully read: TB (2605 lines in 5 chunks), TK (640), WF, WP, IN, PT, QG, TPL, RC, OR, IM, IS, QA, LG, MW, HW (327), RF, CV. Not read: `sc-reflect-protocol`, `rf-task-builder`/`rf-qa` agent files, MDTM templates 01/02, `archive_workspace.py`, any hook or CI file. No command was run.
