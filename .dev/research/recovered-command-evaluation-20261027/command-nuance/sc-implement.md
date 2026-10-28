# Command nuance: /sc:implement

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: plain-prompt versus plan-file input, `--resume`, `--ledger`, `--skip-final-review` by complexity band, and the rule that it never runs a task-builder file. There is no `--depth` flag (see `validation-oneoff-sc-task-vs-sc-implement.md` E1).

Citation key (installed copies under `/home/coder/.claude/`): IM = `commands/sc/implement.md`; IS = `skills/sc-implement-protocol/SKILL.md`; LG = `.../refs/ledger.md`; QA = `.../refs/qa.md`; MW = `.../refs/managed-workspace.md`; AW = `.../scripts/archive_workspace.py`; HW = `HOW-WE-WORK.md`; TB = `skills/task-builder/SKILL.md`; CV = `command-value-by-phase.md` (this folder's parent); VO = `validation-oneoff-sc-task-vs-sc-implement.md`; VF = `validation-feature-task-builder-vs-sc-workflow.md`. "Observed" = seen on disk in this worktree on 2026-10-27.

## 1. Status and role

- Does: "Middleweight spec executor: walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger" (IM:3). Phase: Implement (executor for `/sc:workflow` plans, hand-written plans, notes, or one inline prompt). Standalone-invokable, explicit only, never auto-activated (IM:15-20). Backing skill exists: `skills/sc-implement-protocol/` (SKILL.md, 3 refs, 1 script). Not retired.
- Overlaps: plain edit + test (T/B, proposed minimum per VO), `/sc:task` (retired standalone; `/sc:implement` is forbidden to call it, IM:129, IS:11), `/task` (MDTM executor; "operator types it themselves", IM:139), `bmad-dev-story` / `bmad-quick-dev` (BMad lane, CV:146-147).
- One path only: Q0-Q8 (IS:102-131). Complexity changes only reviewer mode (inline vs one subagent, IS:100), the N=1 FINAL skip (IS:133,153), the N>=20 notice (IS:65), and managed-vs-legacy rules (IS:13). There is no tier, no `--depth` (VO E1.6).

## 2. Flags

### 2a. Options (every one in IM:51-59 and IS:49; both files agree, no flag is defined in one and missing from the other)

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `<path>` (aliases `--spec`, `--prd`, `--tasklist`) | one existing file | one of path or prompt (IM:55) | Source file. Aliases are cosmetic: "aliases for one file" (IM:49). Two files = `E-NO-SOURCE`; directory or missing = `E-SOURCE-MISSING`; path under `.claude/skills\|agents\|commands` = `E-NO-SOURCE` (IS:56-58). Ledger slug = `{basename<=24}-{sha256(absolute path)[:8]}` (IS:63) | Any enumerable plan: workflow plan, hand-written plan, spec, informal notes (HW:194 names "a plan you wrote yourself") | A task-builder (MDTM) file (see 2c) |
| `<prompt>` (leftover text) | free text | one of path or prompt (IM:56) | Persisted to `.dev/implement/<slug>/source.md` before any edit; `<slug>` = first 24 slug-chars + sha256(full prompt)[:8] (IS:60). Becomes ONE task, the prompt text is its AC (IM:29; IS:62,88). No parallel, no end-of-list pass (IS:133) | One deliverable, files and test nameable in the prompt, one session (see 2b) | Anything with several independent deliverables or any need to trace requirements one by one |
| `--resume` | switch | implicit when a matching ledger exists (IM:57; LG:104) | Nothing observable. No Wave 0 step reads it beyond the known-option list (IS:49; grep of IS for "resume" shows no flag handling). Resume = re-invoke on the same source; first task whose latest ledger status is not `complete` (LG:89-100) | Optional, as documentation to the reader | Do not rely on it to change behaviour. Resume does NOT happen if the source key changed: reworded prompt = new slug (IS:60); copied or moved file = new absolute-path hash (IS:63) |
| `--ledger <path>` | path under `.dev/implement/` | `.dev/implement/<slug>/progress.md` (IM:58) | Relocates the ledger inside `.dev/implement/`. Outside it = `E-LEDGER-PATH` (IS:36). Managed package: only its sibling `progress.md` is accepted, anything else `E-LEDGER-PATH` (IM:58; MW:31) | Almost never. Only to give a legacy run a human-readable folder (J) | Managed plans (pointless, rejected). Also avoid when a checker globs `.dev/implement/*/progress.md`: a different file name or depth would be missed (J) |
| `--skip-final-review` | switch | off | Legacy source: skips the whole-list review when N>1 (IS:153). N=1: already skipped, so a no-op (IS:133,153). Managed package: no FINAL and no archive, `E-ARCHIVE-BLOCKED` (MW:51; IS:41). Also suppresses the "run FINAL on resume" step (LG:99,104) | By band, see 2d. HW:227 says "Never turn off a quality check... skip a reviewer step to save time" | Managed packages (always). Any HIGH-band run (J) |

Banned, stop with `E-LEGACY`: `--type`, `--framework`, `--safe`, `--with-tests` (IM:61; IS:32,49-51). `--force` as an option token stops with `E-NO-RULING` (IS:34,49). After the first non-option token these four banned words are plain prompt text (IS:51).

### Does not exist (people may assume)

| Assumed flag | Fact |
|---|---|
| `--depth quick\|standard\|deep` | Not in the option table (IM:53-59), not in the known-option list (IS:49). Belongs to `/sc:workflow` (VO E1.4). Behaviour if typed: UNVERIFIED (VO E1.3; reading of IS:50-51 says `quick` would start an inline prompt) |
| `--reviewer`, `--fresh`, `--no-extras`, dual-mode pitch | Listed as out of scope (IS:172). No Wave 0 handling, so not valid options |
| `--commit`, `--pr`, `--release` | Will Not auto-commit, open PRs or release (IM:131) |
| `--fix` | No such flag on `/sc:implement`. `--fix` belongs to `/sc:troubleshoot` and `/sc:reflect`, which build a plan the operator then runs with `/sc:implement <pkg>/<id>.md` (`commands/sc/troubleshoot.md:54,201`; `skills/sc-troubleshoot-protocol/refs/remediation-handoff.md:11,138`) |
| per-tier review flags | None. Reviewer mode has no flag: inline when N<=3 and source <=400 lines and session not compacted, else one Task subagent (IS:98-100) |

### 2b. Input form: plain prompt versus plan file

| Input form | Tasks it yields | Review | Ledger and footprint | Fits | Cited |
|---|---|---|---|---|---|
| Inline prompt | exactly 1 (T1); AC = the prompt text; "do not invent extra tasks or extra scope" | Inline same-session reviewer by rule (N=1, short); one fix pass; no FINAL | `.dev/implement/<slug>/source.md` + `progress.md`; never seen on disk here | LOW only: single deliverable. Prompt must name file, change and test, because the reviewer judges only against the text and an AC not observable from the diff with no check added is `cannot-verify`, not a pass (VO E2.5; QA:52) | IS:60,62,88; QA:52 |
| Informal notes file / prose spec | 1 (T1 = whole document) when zero enumerable items (IS:62,76) | same as prompt | `.dev/implement/<slug>/progress.md` | LOW | IS:62,76 |
| Spec/PRD/tasklist with enumerable items (`- [ ]`, numbered, `R-NNN`, `## Task N`) | N, in source order; mixed prose + items = items only (IS:68-76) | Per-task review; FINAL for N>1 (advisory) | `.dev/implement/<slug>/progress.md` | MEDIUM and above | IS:68-78,153 |
| `/sc:workflow` plan (`schema: workflow-plan/1.2`, `TASK-WF-*`) = managed package | N from its `## Task N` headings | Per-task review + mandatory fresh FINAL subagent + archive helper | `<pkg>/progress.md`, `<pkg>/artifacts/`, `PLAN:` pin, `FINAL:`, `ARCHIVE:` lines; package moves `to-do/` to `done/` (Linux only) | S and B-MEDIUM, per HW:17,132 | IM:63-65; MW:1-62 |
| Task-builder / MDTM file | See 2c | | | NOT intended | IS:78 |

Prompt nuance (reading of IS:82-88, not seen in a run: UNVERIFIED): a multi-clause prose prompt stays ONE task, since prose paragraphs are never split (IS:76). If its sentences contain `MUST`/`SHALL`/`Done when`, AC QUALIFY rules 1 and 3 may split T1 into several ACs; otherwise the whole text is the single `T1.AC1` (IS:82-88). So a prompt written with explicit "Done when" lines gets per-AC citations, a vague one gets one blanket AC. For several separate deliverables, give a checkbox or numbered list in a file instead.

### 2c. The "never runs a task-builder file" rule: what the files actually say

- Hard refusal: NONE found. The protocol says the opposite of a refusal: "Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`. Phase-N tasklists are accepted as markdown. MDTM-shaped files still use **this** protocol. Do not auto-handoff." (IS:78). `E-NO-SOURCE` only blocks paths under `.claude/skills|agents|commands` (IS:57).
- What it does refuse to do: invoke `/task`, `/sc:task`, `sc:task-protocol` (IS:11; IM:129) and import "MDTM F1, 6-agent phase gates, or `/sc:reflect` as the per-task gate" (IM:130; IS:173; QA:11).
- Consequence (by rule, not run; VF E1 point 2): every `- [ ]` item of a task-builder file, including its QA-gate and reflect items, would be walked as a product task; the file's own checkboxes, frontmatter and Task Log are not updated; the phase panels and `reflect_pre/post` sign-offs never run.
- The team rule is a pairing convention: "TASK-WF folders run with `/sc:implement`, never with `/task`" (HW:216); first pair vs second pair (HW:243, 305-306); "executor that matches the input file" (CV:233). The reverse direction (task-builder file to `/sc:implement`) is implied by those pairings and by IM:129-130, not stated as a prohibition in any file read. Treat as a CONVENTION a checker may flag (J), not as a tool-enforced stop.

### 2d. `--skip-final-review` by complexity band

Band thresholds below are the file's own reviewer-mode switch (N<=3, source <=400 lines, IS:100) and the N=1 FINAL skip (IS:133); the band names are mine (J).

| Band (signals) | Legacy source | Managed package |
|---|---|---|
| LOW: N=1 (a prompt, notes file, or one-task spec) | No-op: FINAL is already skipped at N=1 (IS:153). Never type it | FINAL is mandatory even at N=1 (IS:155; MW:46-48); the flag blocks archiving. Never type it |
| MEDIUM: N=2-3, source <=400 lines, one session (inline review) | Allowed: FINAL is "advisory" and does not rewrite verdicts or reopen tasks (IS:153). Skipping loses the only whole-list check, and HW:227 forbids skipping a reviewer step to save time. Acceptable only with a stated reason (J) | Do not use |
| HIGH: N>=4, or source >400 lines, or multi-session / compacted (subagent review; N>=20 prints a compaction notice, IS:65,100) | Do not use (J). Per-task QA diffs only the increment since that task's Q0 snapshot (IS:118-119), so cross-task drift is caught only by FINAL. Likely also outside the plan-lane (see 3) | Do not use. The package would stay in `to-do/` forever (MW:51,60) |

## 3. Scope x complexity matrix

Scope letters per the brief: T one-off, B bug fix, S single story, F multi-story feature, R multi-feature release (Ruling 2: full release plan, implementation and push), N new product. The command does not vary by complexity itself (one path, section 1); the bands decide whether it is the right executor at all.

Bands for this command (signals from files; thresholds marked J are mine):

| Band | Signals |
|---|---|
| LOW | One deliverable; files and test nameable in one sentence; one session; no driving spec; no risk trigger (secrets, permissions, user input, file paths, infrastructure). Fits HW level 2 shape (HW:16) or a 1-task level 3 plan (HW:17). N=1. TCS-equivalent <=12 (J; TCS is defined only for task-builder bodies, TB:2410-2433; 2 files in one subsystem = 10, 3 files = 13) |
| MEDIUM | A few files, clear scope, 1-2 sessions, 2-3 tasks, a short or no spec, nothing that "must not drift" (HW:17). Review still inline (N<=3, <=400 lines, IS:100). TCS-equivalent 13-34 (J) |
| HIGH | Many files or several subsystems, more than one session, must not drift, a spec to trace requirement by requirement, files not nameable up front, stories sharing an interface, or a risk trigger (HW:18,19,22; VF "Complexity signals" table; TB:2410-2415 for the counting rules). Subagent review, N>=4 or >400 lines (IS:100). TCS-equivalent >=35 or refactor-class `type:` (TB:2438, J) |

Cells: rating, then the flag set. "(lane)" = rating holds when the tasklist step chose the `/sc:workflow` lane; in the task-builder lane the cell is SKIP.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T | OPTIONAL (J, built on the PROPOSED T minimum "plain edit + related test", VO verdict 2): `/sc:implement "<file, change, test>"`, no flags | REQUIRED (J, lane): HW:22 hard limit (>5 edits or >1 source file) forces a written plan; level 3 = `/sc:implement <plan path>`, no flags | SKIP (J): level 4, `/task-builder` + `/task` (HW:18,22). A "one-off" this big is mis-scoped |
| B | OPTIONAL (J): HW bug route 3a is test-first fix + `/sc:test`, no implement (HW:131; routing row bug 3a, HW:311). Prompt form allowed, no flags | REQUIRED (lane): route 3b/4, `/sc:workflow --depth quick` then `/sc:implement <plan>` (HW:132; HW:311). Operator-run, never auto (`commands/sc/troubleshoot.md:190`) | SKIP: route 3c, `/task-builder` + `/task` (HW:133) |
| S | REQUIRED (lane): `/sc:workflow --depth quick` then `/sc:implement <plan>`, no flags (HW:17,305; CV:143) | REQUIRED (lane), but move to task-builder when any HIGH signal appears; at exactly 2 sessions both rows fit and the heavier wins (HW:9, VF verdict 2) | SKIP: `/task-builder` + `/task`; conditions in VF "Is /task-builder ever justified on a SINGLE story" (more than one session, spec to trace, larger or riskier, files not nameable) |
| F | OPTIONAL (J), per story only: several independent single-subsystem stories, each 1-2 sessions, no driving spec, may run as separate workflow plans, but no feature-level coverage check exists (VF "Rule I suggest", J) | SKIP (J): not eligible as the feature minimum (VF verdict 1: no research wave, no `--spec`, plan frozen after task 1, sized for 1-2 sessions) | SKIP: `/task-builder --spec` + `/task` is the feature minimum (VF verdict 1; HW:306-307) |
| R | OPTIONAL (J): only as executor of a constituent S-size item inside the release. Never the release-level step. Re-rated, see section 7 | OPTIONAL (J): same | SKIP (J): constituent features at F-size use `/task` |
| N | N/A: a new product is not LOW; if it is, it is S | SKIP: `/roadmap` emits task files for `/task` (HW:76,309; CV:112,144) | SKIP: same |

Flag set in every cell above: none. `--resume` is implicit (IM:57). `--skip-final-review`: never in LOW (no-op), reason-only in MEDIUM, never in HIGH or managed (2d). `--ledger`: default.

## 4. Choose this or the neighbour

| Neighbour | Pick `/sc:implement` when | Pick the neighbour when | Cited |
|---|---|---|---|
| Plain edit + related test (T/B) | You want a checkable record: ledger with `path:line` citations per AC, an independent-by-rubric review, git pin. The prompt names file, change and test | One source file plus its test, <=5 edits, exact change known (HW:16, 22). The edit alone is the T minimum (PROPOSED, VO verdict 2). Do not use the prompt form to get around the HW:22 written-plan limit: a prompt is one task with one blanket AC, not a plan (J) | HW:16,22,304; VO verdict 2; IS:62,88 |
| `/sc:task` | Never as an alternative: retired standalone (Ruling 3). `/sc:implement` itself may not call it | Never | IM:129; IS:11; VO E5.1 (only caller is `/sc:tasklist` Stage 9) |
| `/sc:workflow` first, then `/sc:implement <plan>` (versus prompt form or a hand-written list) | Prompt form is not enough when: more than one source file or >5 edits (HW:22); 2-3 separable deliverables each needing its own acceptance check; files not obvious; reviewer should read AC written by someone other than the implementer | Prompt form or a hand-written checkbox list is enough when it is one deliverable (prompt) or you can write N clear items yourself (HW:194 accepts "a plan you wrote yourself"). `/sc:workflow` adds a structure gate and an advisory `/sc:reflect --mode pre` against its own source only (VF E4) | HW:17,22,194; IS:68-78; VF E4 |
| `/task-builder` + `/task` | S/B with a plan-lane fit: few files, clear scope, 1-2 sessions, nothing "must not drift" (HW:17) | Any of: more than one session; a spec to trace (`--spec`, `reflect_pre`); larger or riskier than a few files; files cannot be named up front; stories share an interface; plan likely to be amended mid-run (managed plan freezes after task 1: `E-PLAN-CHANGED`, MW:42). Tie at 2 sessions: heavier row (HW:9). Never feed the task-builder file to `/sc:implement` (2c) | VF verdict 1-2, "Complexity signals" table; HW:9,18,19,22 |
| `bmad-dev-story` / `bmad-quick-dev` | Task-file lane work (`TASK-WF-*` or hand plan) | BMad lane: a story file exists from `bmad-create-story` (dev-story); BMad small change (quick-dev). "Pick the lane at the Spec step and stay in it" (CV:223) | CV:146-147,223 |
| `/sc:troubleshoot --fix` | Executing the plan that Tier 3 built: troubleshoot surfaces the literal `/sc:implement <pkg>/<id>.md` and stops; the operator runs it | Diagnosis only (default) | `commands/sc/troubleshoot.md:54,190,201`; `skills/sc-reflect-protocol/refs/remediation-handoff.md:21,96` |
| `/sc:reflect --mode post` | Not a substitute. `/sc:implement` does not run reflect as the per-task gate and does not need it (IM:130; QA:11) | Optional audit afterwards against spec; troubleshoot and reflect remediation chains surface it as the post-execution gate | IM:130,140; `skills/sc-troubleshoot-protocol/SKILL.md:564` |
| `/sc:test`, `/sc:git` | Not gates; "Suggest ... only as optional next steps" (IS:159). Lint, typecheck, tests run inside Q6 as extras if they already exist; they never decide the verdict (IS:135-147) | Run `/sc:test` yourself when no test existed to detect | IS:135-159 |

## 5. What a scheduled checker can see

Yes, a file footprint exists. Documented in LG and MW; "Observed" marks what is on disk in this worktree.

| Run type | Where | Content a checker can test | Observed |
|---|---|---|---|
| Inline prompt | `.dev/implement/<slug>/source.md` (written before any edit, IS:60) and `.dev/implement/<slug>/progress.md` | `progress.md` line 1 header, `T1: start sha=`, `T1: complete verdict=compliant ac=T1.AC1 evidence=<path:line> extras=... files=...` (LG:15-59) | Not observed: no `source.md` exists under `.dev/implement/` (only 3 under `.dev/tasks/`, those belong to workflow packages) |
| File source (legacy) | `.dev/implement/<slug>/progress.md`; slug has a hash of the engineer's absolute path (IS:63), so a checker cannot recompute it; read the header `source:` instead (LG:18) | Same lines; `FINAL: pass\|issues evidence=...` after the last task when N>1 and not skipped (LG:83-86; IS:153) | 4 ledgers. Header sources are absolute paths from another checkout (`/config/workspace/Coder/...`) or `claudedocs/workflow_*.md` / `.dev/plans/*/tasks.md`; match on basename, not repo-relative path |
| Managed package (`TASK-WF-*`) | `.dev/tasks/to-do/<id>/` then `.dev/tasks/done/<id>/`: `<id>.md`, `source.md`, `return-contract.yaml`, `progress.md`, `artifacts/` (MW:29-36) | `PLAN:` pin on line 2; per-task lines; `FINAL: pass ... state=<64hex>`; `ARCHIVE: start id=<id> token=<hex>` as last line after a successful move (LG:134-157) | 2 in `done/` (`TASK-WF-designSpec-20261022-132541`, `TASK-WF-takeThePlanConfi-20261023-173430`); both end `FINAL: pass` then `ARCHIVE: start` |
| Git refs | `refs/superclaude/implement/<slug>/T<id>`, pinned at Q0, deleted when the task completes (IS:111-114) | A ref that survives = a task started and not completed | None present now (`git for-each-ref refs/superclaude` empty); consistent with all runs finished |
| Product files | The edited files, listed in each line's `files=` field | `files=` paths vs `git diff` | n/a |
| Not written | Commits, PRs, releases: never (IM:131). The start `sha=` is a tree object from `git write-tree` (IS:110), not a commit; `nogit` when no git | Do not `git show` it as a commit; the object may be absent in another clone | Of 4 start shas sampled, 2 resolve here as `tree` (`git cat-file -t`), 2 are not in this clone. One ledger has `sha=nogit` (`tasks-01ce7210`) |

Signals by state:

| State | Footprint |
|---|---|
| Started, in progress | Header + `T<n>: start` with no `complete`/`blocked` line for that id; live pin ref |
| Halted | `T<n>: blocked verdict=...` last line; `E-HALT-QA` is printed, not written (QA:61); operator `Ruling:` line needed to continue (LG:61-71). Rulings are operator-written only |
| Finished, legacy, N>1 | every id `complete` + a `FINAL:` line. No `FINAL:` and all complete = FINAL skipped, or run interrupted before it (LG:99,104) |
| Finished, managed | package in `done/`, `progress.md` ending `FINAL: pass` then `ARCHIVE: start`. All tasks complete but folder still in `to-do/` = archive-blocked (IS:163; MW:46) |
| Wrong lane | Ledger header `source:` pointing at a task-builder output (`TASK-RF-*`, `TASK-ROADMAP-*`, frontmatter `reflect_post_mode`, VF "Distinguishing the two lanes"), or `/task` run on a `TASK-WF-*` folder (HW:216). No such ledger exists here (UNVERIFIED as a pattern) |

Cautions for the checker:

1. Do not validate whole lines against the installed grammar regex (LG:56). Observed real managed ledgers contain record kinds that the installed `refs/ledger.md` and `SKILL.md` never define: `T12: halt review=2 reason=operator-review`, `T14: retry n=3 step=open checkpoint=<sha> tier=unknown`, `retry n=3 step=revert brief=...` (in `.dev/tasks/done/TASK-WF-designSpec-20261022-132541/progress.md` and `.../TASK-WF-takeThePlanConfi-20261023-173430/progress.md`). A grep of the installed skill and command for `retry n=` and `halt review=` returned nothing. Match per-line prefixes (`T<id>: start|complete|blocked|Ruling:`, `FINAL:`, `ARCHIVE:`, `PLAN:`) and ignore unknown lines. Which version writes the extra lines: UNVERIFIED.
2. A ledger may show `T<n>: blocked` several times for one id (retries within one fix budget) and finish with an operator `Ruling` plus a `complete` line whose verdict is still non-compliant (`complete verdict=missing`, observed). "complete" does not mean "compliant" (LG:59-81).
3. Task ids are not always `T1..TN`: `T-0` observed (`tasks-01ce7210`), allowed by the id regex (LG:38).
4. Ledgers are not gitignored (`git check-ignore` returned no match on 2026-10-27) and "Do not `git add` the ledger" (LG:3), so a fresh legacy ledger shows as untracked. The 4 observed legacy ledgers are tracked only because of bulk commits (VO F2). Read the working tree, not git history. For managed ledgers under `.dev/tasks/`, the project rule "`.dev/tasks/` is always staged" applies (project `CLAUDE.md`); how that interacts with LG:3 is UNVERIFIED (VF V12).
5. Plain edit and "no `/sc:implement`" leave nothing: the checker can only infer from commits or transcript.
6. The ledger is local to the engineer's checkout. A different engineer's `~/.claude` may carry a different protocol version (VF V13).

## 6. Expected-step rule

- Count `/sc:implement` as EXPECTED when the work's tasklist step produced a `/sc:workflow` plan or a hand-written plan as its executor input: S (LOW, MEDIUM) and B-MEDIUM, and T-MEDIUM (J). Evidence of the miss: a `TASK-WF-*` package whose `files=`-listed product paths changed but has no `progress.md`, or whose tasks are all `complete` with no `FINAL:` (legacy N>1) or no `ARCHIVE: start` / still in `to-do/` (managed). Do not flag a plan that exists with no ledger and no related commits yet: not started (J).
- Its ABSENCE is fine for: T and B at LOW (plain edit + test; PROPOSED minimum), every task-builder lane (S/B HIGH, F, N via `/task`), the BMad lane (`bmad-dev-story`, `bmad-quick-dev`), and the release-level step of R. At F and R, a `/sc:implement` ledger is allowed only for a constituent S-size item (J).
- Flag as WRONG (not as a skipped step): ledger `source:` is a task-builder output, or a `TASK-WF-*` folder was run with `/task` (HW:216); `/sc:task` used standalone (retired).
- `--skip-final-review` has no direct footprint except the missing `FINAL:`/archive. Do not flag a missing `FINAL:` at N=1 (IS:153). At N>1 legacy, a missing `FINAL:` is a soft finding (the pass is advisory, IS:153); on a managed package it is a hard one (no archive possible, MW:51).

## 7. Proposed changes to command-value-by-phase.md

Proposals only; `command-value-by-phase.md` (CV) not edited. Changes already proposed in VO (T cell, notes on `--depth`, row 143) and VF (F cell, rows 5, 9) are not repeated in full; this list adds to them or resolves overlap.

| # | CV location | Current | Proposed | Why |
|---|---|---|---|---|
| 1 | CV:143, `/sc:implement` row, T..N cells | `SKIP \| OPTIONAL \| REQUIRED \| OPTIONAL \| SKIP \| SKIP` | `OPTIONAL \| OPTIONAL \| REQUIRED \| SKIP \| OPTIONAL \| SKIP`. Changes: T SKIP to OPTIONAL (VO row 129; rests on the PROPOSED T minimum); F OPTIONAL to SKIP (VF row 5, J); **R SKIP to OPTIONAL (J, Ruling 2)**. B stays OPTIONAL, S stays REQUIRED | Matrix in section 3. R: under Ruling 2 a release includes implementation, so the "R assembles work already built" reading no longer holds; `/sc:implement` shows up only as executor of S-size items inside it |
| 2 | CV:143, Notes cell | "Runs `/sc:workflow` plans (`TASK-WF-*`). Resumes from first unfinished step. Stops with `E-HALT-QA` after two failed step checks. ‡ with `/task`" | "Executor for `/sc:workflow` plans (`TASK-WF-*`), hand-written plans, notes files, or one inline prompt (one task, ledger in `.dev/implement/<slug>/`). No `--depth`. Options: `--resume` (implicit), `--ledger`, `--skip-final-review` (never on a managed plan: blocks archiving). Never run it on a task-builder file. Resumes from first unfinished step; stops with `E-HALT-QA` after one failed fix pass. Rating holds in the `/sc:workflow` lane only; at S-HIGH and F use `/task-builder` + `/task`. ‡ overlaps `/task` at S size only" | Sections 2, 3; IM:53-59; IS:100,153 |
| 3 | CV:139, intro to Section 2.4 | "Reading of the R column in this phase: a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result." | "R = multi-feature release including its implementation (Ruling 2). Build-the-code commands rate R by the items inside the release: `/task` for F-size features, `/sc:implement` and `bmad-dev-story` only for S-size items. Release-level steps are review, push and docs." Note: the R cells of `/task` (CV:144, SKIP), `bmad-dev-story` (CV:146, SKIP) and `bmad-quick-dev` (CV:147, SKIP) rest on the old reading and need the same re-rating; other agents own those rows | Ruling 2; CV:139 |
| 4 | CV:276, last row of the footprint table | "`/code-review`, `/security-review`, `/sc:test`, `/sc:implement` (beyond `progress.md`), `/sc:git` \| No file footprint stated anywhere I read..." | Remove `/sc:implement` from that row. Add its own row: "`/sc:implement` \| prompt run: `.dev/implement/<slug>/source.md` + `progress.md`; file run: `.dev/implement/<slug>/progress.md` (header `source:` has the path); managed plan: `<pkg>/progress.md` with `PLAN:`, `FINAL:`, `ARCHIVE:` lines, package moves to `.dev/tasks/done/`; git ref `refs/superclaude/implement/<slug>/T<id>` only while a task is in flight. Real ledgers carry extra `retry`/`halt` lines the installed grammar does not define: match by line prefix, not whole-line regex" | Section 5 |
| 5 | CV:50, double-dagger legend, row 144 note for `/task` | "‡ ... two commands do the same job" | Add to the `/sc:implement` / `/task` pair: "never swap inputs: task-builder file to `/task`, `TASK-WF-*` to `/sc:implement`". The task-builder-to-implement direction is a convention (IS:78 does not refuse it); the `TASK-WF`-to-`/task` direction is stated at HW:216 | Section 2c |
| 6 | CV:254 and CV:252 | Single-story and one-off rows list `/sc:implement <plan path>` in step 3 and `/sc:task` in step 1 | S step 3: append "(creates `progress.md` beside the plan; on Linux the package moves to `done/` after a fresh FINAL; do not pass `--skip-final-review`)". T step 1 per VO row 132 | IM:63-65; MW:44-62; HW:17 |
| 7 | CV Section 5 (unverified), add rows | - | Add: the extra ledger record kinds (U3 below), the `.dev/tasks/archive/` folder (U4 below), and that `--resume` is a no-op | Section 8 |

## 8. Unverified items

Nothing was run (read-only task). Everything below is a reading of files, or an observation of files, not a result of executing `/sc:implement`.

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | What `/sc:implement ... --depth quick` does when typed | Not documented; tokenizer reading says `quick` would join the prompt (VO E1.3) | One run on a throwaway prompt |
| U2 | Prompt-source layout (`source.md`, `progress.md`) and whether a prompt with `MUST`/`Done when` sentences splits into several ACs | No prompt run exists in this repo (no `source.md` under `.dev/implement/`); AC split is my reading of IS:82-88 | One run; inspect the ledger `ac=` field |
| U3 | Which version writes `halt review=` / `retry n=` ledger lines seen in two real managed ledgers | Not defined in installed `SKILL.md`, `refs/ledger.md`, `refs/managed-workspace.md` (grep empty); the IronClaude source tree cited in ledgers (`/config/workspace/IronClaude`) is not on this machine | Compare installed copy with the repo source; ask maintainers |
| U4 | `.dev/tasks/archive/TASK-WF-closeTheRealTest-20261023-140622/` (has plan, `source.md`, `return-contract.yaml`, no `progress.md`) | Installed MW describes only `to-do/` to `done/`; no file read explains `archive/` | `git log` on that path; read the producing command |
| U5 | What `/sc:implement` does with a task-builder file | By-rule reading only (IS:78, IM:129-130, VF E1; VF V2). No file states the prohibition in this direction; it is a pairing convention | Dry run on a throwaway copy |
| U6 | `--resume` beyond "implicit": invoked with no matching ledger, or on a changed source | No handling found outside the known-option list; LG:104 says a missing ledger gets a header written. Source change mid-run on a legacy source: no hash pin found (the `PLAN:` pin is managed-only, LG:144) | One run each |
| U7 | A path followed by trailing text (`/sc:implement spec.md also do X`) | IM:49 says "A non-path remainder is an inline prompt"; the mixed case is not specified | One run |
| U8 | Whether the inline reviewer (N<=3, <=400 lines) is meaningfully independent | By rubric "not the implementer voice", same session by design (IS:100; QA:83; VO U7) | Compare inline and subagent verdicts on seeded defects |
| U9 | The TCS-equivalent bands in section 3 | TCS is defined only for task-builder bodies (TB:2410-2433); applying it to a workflow plan is JUDGMENT; HW's "a few files" is looser than TCS <=12 | Lead decision; or compute TCS on a few existing `TASK-WF-*` plans |
| U10 | The T-minimum cells (T-LOW, B-LOW) | The one-off minimum "plain edit + test, `/sc:implement "<prompt>"` optional" is PROPOSED in VO, not confirmed by Ryan | Ryan's ruling |
| U11 | Cost and time of a one-task run versus a plain edit, and of FINAL | No token or time figure in any file read | Measure |
| U12 | Whether installed copies match other engineers' or the repo source | `~/.claude` is per engineer (brief ruling 1); IM:83 cites `src/superclaude/skills/...`, not present here (VO U9) | Compare installs |
| U13 | The statement that a checker "cannot recompute" the legacy slug | Based on IS:63 hashing the engineer's absolute path; observed headers carry absolute paths from `/config/workspace/Coder` | Check on a second engineer's machine |
