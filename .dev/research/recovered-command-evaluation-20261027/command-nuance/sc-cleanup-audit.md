# Command nuance: /sc:cleanup-audit

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: `--pass` options and repository size; when it precedes `/sc:cleanup` and when it is overkill.

Citation keys. `CA:` = `~/.claude/commands/sc/cleanup-audit.md`. `SK:` = `~/.claude/skills/sc-cleanup-audit-protocol/SKILL.md`. `pass1:` / `pass2:` / `pass3:` = `rules/pass1-surface-scan.md`, `rules/pass2-structural-audit.md`, `rules/pass3-cross-cutting.md` in that skill folder. `INV:` = `scripts/repo-inventory.sh`. `CL:` = `~/.claude/commands/sc/cleanup.md`. `HWW:` = `~/.claude/HOW-WE-WORK.md`. `AG:` = `~/.claude/agents/`.

Read in full: all of the above, the other two `rules/` files, the 4 `templates/`, and `AG:audit-scanner.md`, `audit-validator.md`, `audit-consolidator.md`. Frontmatter only: `AG:audit-analyzer.md`, `audit-comparator.md`. `HWW:` read at lines 1-30, 150-175, 236-248, 296-327; `auggie-review.md` and `sc-recommend/refs/delegation-vs-native-heuristics.md` read only around their cleanup-audit mentions. Repo counts observed 2026-10-27 with `git ls-files` in this worktree. Nothing was run except read-only shell checks.

## 1. Status and role

- Does: "Multi-pass read-only repository audit producing evidence-backed cleanup recommendations" (`CA:3`). Standalone-invokable, not retired; backing skill exists (`~/.claude/skills/sc-cleanup-audit-protocol/`, plus five `AG:audit-*.md` agents). It names neither `/sc:task` nor `/sc:tasklist`.
- Phase: none of Ryan's five pipelines. It is a hygiene job: step 1 of guide 3.7 and routing row `cleanup` (`HWW:159-161`, `HWW:318`). Its only declared hand-off is "use `/sc:cleanup` to execute safe recommendations, then `/sc:test`, then `/sc:git`" (`CA:119`).
- Overlaps: `/sc:cleanup` (the editor that acts on it), `/sc:analyze` (module health), `/sc:auggie-review` (diff-scoped, "complementary", `auggie-review.md:185`), built-in `/simplify` (changed code only).

## 2. Flags

Syntax (`CA:31`, `SK:25`): `/sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]`. Four arguments; the command file and the protocol skill define them identically.

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `target-path` | a directory | `.` whole repo (`CA:36`) | Files enumerated with `git ls-files -- "$TARGET"` (`INV:63`), then the default scope floor is applied (below). Guide: "leave out the path only when you mean the whole repository" (`HWW:161`) | Always give a path for a folder cleanup | Omitting it on a large repo: cost scales with in-scope files |
| `--pass surface` | Pass 1 | The bare command runs Pass 1 only (`CA:53`; `HWW:161`). The Arguments list itself states no default | Quick scan: each file DELETE / REVIEW / KEEP, grep proof for every DELETE (`CA:43`, `pass1:80-86`). Output `.claude-audit/pass1-summary.md` (`CA:53`) | Question is "is there junk here?" Target is LOW or MEDIUM and you only want delete candidates | You need to know whether docs/config are still true, or whether files duplicate each other |
| `--pass structural` | Pass 2 | none | 8-field profile per file; finding types MISPLACED / STALE / STRUCTURAL ISSUE / BROKEN REFS / VERIFIED OK; only files Pass 1 marked KEEP or REVIEW (`pass2:30,51-62`). Highest-value finding: a doc "describes things that don't exist" (`pass2:89`). Command file says it "requires Pass 1 results as input context" (`CA:61`) | Docs, runbooks, configs may have drifted from code (this repo: `docs/operations/*`, `templates/*/README.md`, per `PROJECT_INDEX.md`) | No Pass 1 output exists yet (behaviour undefined, U6); target is a handful of files you can read yourself |
| `--pass cross-cutting` | Pass 3 | none | Compares files across directories; mandatory duplication matrix with overlap % when similar files exist (`pass3:76-87`); receives Pass 1-2 findings and does not re-flag them (`pass3:56`); directories of 50+ files are sampled at 10-15 files (`pass3:59`) | Sprawl: several compose / Dockerfile / deploy scripts / configs (`pass3:62-66`); example flag set `--pass cross-cutting --focus infrastructure` (`CA:66`) | Single small directory (nothing to compare against); Pass 1-2 output absent |
| `--pass all` | Passes 1, 2, 3 in order | none | Quality gate between passes, then a final report: executive summary, prioritized actions, cross-cutting findings, issues registry (`CA:77`, `SK:70`). This is the `mandatory_flags` entry for routing row `cleanup` (`HWW:318`) | MEDIUM or HIGH target, or a pre-release sweep (section 3) | LOW target: three passes, a validator and a consolidator for at most one Pass-1 batch of files (J) |
| `--batch-size N` | integer | 50 surface, 25 structural, 30 cross-cutting (`CA:38`) | Files per agent. Binary assets get grep-only audits at 50-100 per batch (`pass1:63-76`). Each agent has `maxTurns: 60` (`AG:audit-scanner.md:6`) | Lower it when files are long scripts or an agent reports "Remaining / Not Audited" (`batch-report.md:74-76`) | Raising it above defaults: more reads and greps per agent, more unreached files (J). `INV:12` takes a single size, so how one N maps onto three passes under `all` is not defined (U8) |
| `--focus` | `infrastructure`, `frontend`, `backend`, `all` | not stated | "Domain filter for targeted auditing" (`CA:39`). `INV:146-168` groups files into 8 domains (adds tests, documentation, config, assets, other) but the script takes no focus argument (`INV:3`) | Splitting a HIGH target into slices; Pass 3 on infrastructure (`CA:66`) | Expecting to audit only docs, config or tests: no value selects them. Mechanism is not defined (U4) |

Default scope floor, not a flag and not removable (`SK:54-65,103`; `INV:20`): hidden paths (any leading-dot segment), `_bmad/`, `_bmad-output/`, `_planning-input/`, `.claude-audit/`. A project may add regexes with `EXCLUDE: <regex>` lines in `.claude-audit/SCOPE.md`; it can tighten, never loosen.

Does not exist (a checker or engineer might assume them):

| Assumed flag | Fact |
|---|---|
| `--depth` | Absent from both files. Depth is chosen by `--pass` |
| `--resume` | Absent. Resume is described as automatic via `progress.json` (`SK:76,100`), but `sc-crash-recovery` says audits "are not designed for fine-grained resume": re-invoke the skill (`~/.claude/skills/sc-crash-recovery/refs/pipelines.md:203-205`) |
| `--fix` / `--apply` / `--dry-run` / `--preview` | Absent. The command is read-only by design (`CA:103-110`). `--type`, `--safe`, `--aggressive`, `--interactive` belong to `/sc:cleanup` (`CL:22`) |
| `--output` / `--out-dir` | Absent. Output location is fixed: `.claude-audit/` (`CA:112`) |
| `--exclude` / `--include-hidden` | Absent. Only `SCOPE.md` EXCLUDE lines; hidden and BMAD paths cannot be switched on (`SK:64,103`) |
| `--model` | Absent. Pass 1 "Haiku", Passes 2-3 "Sonnet" per prose (`SK:68`), but see U1 |

## 3. Scope x complexity matrix

This command does not vary with the complexity of a delivery task. It varies with the size and risk of the TARGET folder. No file rates it by scope (T/B/S/F/R/N), so every cell below is judgment, labelled `(J)`, derived from the triggers in `SK:16-20` and the cleanup route in `HWW:157-168,318`.

### Size facts (what "repository size" means for this command)

| Fact | Value | Source |
|---|---|---|
| Unit of work | one Pass-1 batch = 50 files; one agent wave = 7-8 batches, so about 350-400 files per wave | `CA:38`, `SK:68` |
| Size that matters | files left after the scope floor, not repo size. The command prints "Total tracked files" and "In-scope after default excludes" itself (`CA:15-16`), but both are repo-wide, not target-scoped | `CA:15-16` |
| Designed-for scale | Pass 3 depth plan budgets about 1,400 files (~200 deep, ~800 medium, ~400 light) | `pass3:70-74` |
| This repo (observed 2026-10-27) | 5,152 tracked files, 277 in scope (5.4%), 73 MB on disk excluding `.git` | `git ls-files`, `du` |
| Excluded here by the floor | `.dev` 3,936; `.claude` 263; `_bmad-output` 261; `.agents` 237; `.github` 128; `.opencode` 20; `_bmad` 17 | `git ls-files` + `INV:20` |
| In scope here by top folder | `templates` 168; `claudedocs` 31; `docs` 29; `ci-timing` 14; `scripts` 12; `orca-build` 9; `artifacts` 6; `openspec` 2; `install` 1; `SECURITY.md` 1 | `git ls-files` |
| Protocol load cost | `SKILL.md` 10,202 bytes + command file 5,126 bytes. `sc-recommend` says do not invoke a skill whose protocol is over ~2,000 tokens for a task under ~500 tokens of work, and names `/sc:cleanup-audit` as one of the large ones | `wc -c`; `delegation-vs-native-heuristics.md:50` |
| Derived agent count, this repo, `--pass all`, defaults | Pass 1: ceil(277/50) = 6 (one wave). Pass 2: at most ceil(277/25) = 12 (two waves; DELETEs drop out, `pass2:30`). Pass 3: at most ceil(277/30) = 10 (it samples, `pass3:58-59`). Upper bound about 28 batch agents plus validators and consolidators | arithmetic from the rows above (J) |
| Derived agent count, LOW target (50 files), `--pass all` | 1 + up to 2 + up to 2 batch agents, plus the same validator and consolidator steps per pass, so overhead is about the size of the work | arithmetic (J) |

Consequence: on this repo the pipeline's own CI (`.github/`, 128 files) and the task ledgers (`.dev/`, 3,936 files) are invisible to the audit by design (`SK:55-62`, `INV:20`). A "whole repo" audit here covers templates, docs and scripts only.

### Bands (edges are JUDGMENT, anchored on the batch and wave sizes above)

| Band | Definition for this command |
|---|---|
| LOW | 50 in-scope files or fewer in the target (one Pass-1 batch); one domain; you can name every referrer with a grep |
| MEDIUM | About 51-350 in-scope files (2 to ~7 Pass-1 batches, at most one wave); or 2+ domains; or suspected duplicates across directories. This repo as a whole (277) is MEDIUM |
| HIGH | More than ~350 in-scope files (more than one wave); or dynamic loading in play (env-var, string-built imports, plugin registries, glob discovery, config-driven: `dynamic-use-checklist.md:11-118`); or config/compose/deploy sprawl (`pass3:62-66`); or a pre-release sweep with unknown referrers |

### Matrix

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J) | SKIP (J) |
| B bug fix | SKIP (J) | SKIP (J) | SKIP (J) |
| S single story | SKIP (J) | OPTIONAL (J): `<path> --pass surface`, only if the story deletes or moves files and referrers are unknown | OPTIONAL (J): `<slice> --pass all`; a story that needs this is probably mis-sized |
| F multi-story feature | SKIP (J) | OPTIONAL (J): `<path> --pass surface` after merge, when the feature replaced or retired something (`SK:17` post-migration) | WORTH IT (J): `<path> --pass all` as research input to a cleanup or refactor feature spec; a large refactor is treated as a feature (`HWW:168`) |
| R multi-feature release | OPTIONAL (J): `<path> --pass surface` | WORTH IT (J): `--pass all` on the release paths or whole repo (`SK:19` pre-release cleanup) | WORTH IT (J): `--pass all` in slices by path or `--focus` (`verification-protocol.md:86` "cap files per agent... prevent audit the world") |
| N new product | SKIP (J) | SKIP (J) | SKIP (J): greenfield has nothing accumulated; a brownfield port is not N |

Reading rules:
- A job whose whole purpose is tidying (routing row `cleanup`, `HWW:318`) is its own route, outside T..N. Judge it by target band, not by scope.
- B stays SKIP at every band: the audit finds dead, duplicate and misplaced files, not defects. Use `/sc:troubleshoot` (`HWW:311`).
- T stays SKIP: removing unused imports in one file is level 2 (`HWW:16`) or `/sc:cleanup --type imports`.

## 4. Choose this or the neighbour

### Audit first, or straight to `/sc:cleanup`?

| Signal | Straight to `/sc:cleanup <path> --type imports\|code --safe --interactive` | Run `/sc:cleanup-audit` first |
|---|---|---|
| Target size | LOW: 50 in-scope files or fewer (J) | MEDIUM or HIGH (section 3) |
| What you want removed | Unused imports, code with zero references, empty blocks, redundant annotations: the things `/sc:cleanup` auto-fixes (`CL:109-114`) | Whole files: delete, move, merge duplicates (the audit's DELETE / MOVE / CONSOLIDATE actions, `verification-protocol.md:9-16`) |
| Who references it | You can name them, or one grep settles it | Unknown referrers; dynamic loading possible (`dynamic-use-checklist.md:9-13`) |
| Doc or config truth | Not in question | Docs or configs may describe things that no longer exist (`pass2:85-90`) |
| Duplication | None suspected | Several similar compose / deploy / config files (`pass3:62-66`) |
| In the scope floor? | Target is hidden or BMad (`.github/`, `.dev/`, `.claude/`, `_bmad*`): the audit cannot see it, so grep by hand | Target is outside the floor |
| Part of a larger refactor | Do not use either as the plan: a large or structural refactor is "a feature": spec plus `/task-builder --spec` (`HWW:168`, `HWW:318` notes). The audit may feed the spec as research | same |

`/sc:cleanup` safety behaviour to know: it prompts the user for anything with "ANY usage path", anything affecting a public API, or when unsure (`CL:123-127`). So skipping the audit does not make small cleanups unsafe; it removes the cross-file evidence.

Hand-off is manual. `/sc:cleanup` usage has no flag that reads an audit report (`CL:22`) and its own flow re-analyses the target (`CL:27-31`). Guide order: audit, commit, cleanup, improve, review `git diff` (`HWW:318`). The audit recommends file-level actions; the guide's step 3 passes `--type code`, while `/sc:cleanup` also offers `--type files|all` (`CL:22`). Which type executes the audit's file moves and deletes is not stated (U10).

### Other neighbours

| Neighbour | Pick the neighbour when | Pick `/sc:cleanup-audit` when | Cite |
|---|---|---|---|
| `/sc:analyze` | Question is module health: quality, security, performance, architecture (route `module-health`, `--focus <area>`) | Question is which files are dead, duplicate, misplaced, or documented wrongly | `HWW:313`, `HWW:318` (analyze file not read in full) |
| `/sc:auggie-review` | You want a review of the diff or PR before push (route `review-pr`) | You want the whole repo, not a diff. The two are "complementary", never substitutes | `auggie-review.md:185`, `HWW:323` |
| `/simplify` (built-in) | Your own changed code needs reuse and simplification cleanups before commit | Accumulated files you did not just change | session skill list; no file (U12) |
| `/tech-research` | You do not know how the system works or what must change (level 5) | You know the intent (remove dead stuff) and need evidence | `HWW:19` |
| Plain `git grep` then `git rm` | One to a few files; one grep settles referrers | More than that, or any dynamic-loading doubt | `pass1:80-86` sets the same grep-proof standard by hand |
| `/task-builder --spec` + `/task` | Acting on a large audit result (many files, more than one session, must not drift) | The audit itself, the evidence-gathering step | `HWW:18`, `HWW:168` |

## 5. What a scheduled checker can see

Footprint is a folder of reports in the working tree, not a ledger and not frontmatter. Nothing is written under `.dev/` (`CA:112-117`: "Audit reports written to `.claude-audit/` directory only").

| Path (repo root of the audited repo) | What it holds | Source |
|---|---|---|
| `.claude-audit/pass1-summary.md` | Pass 1 consolidated summary | `CA:53` |
| `.claude-audit/pass2-summary.md`, `pass3-summary.md` | Pass 2 and 3 summaries (appendix of the final report) | `final-report.md:120-122` |
| `.claude-audit/pass{N}/batch-NN.md` | One report per agent batch; header lines Status, Files audited, Date, Agent, Batch | `pass-summary.md:97-98`, `batch-report.md:3-7` |
| `.claude-audit/progress.json` | Checkpoint state; schema not defined in any file read | `CA:117`, `SK:169` |
| Final report | Header line `Passes Completed: {1, 2, 3 or subset}` tells a checker which `--pass` ran; file name not specified (U5) | `final-report.md:5` |
| `.claude-audit/SCOPE.md` | Optional input written by the engineer, not by the audit | `SK:64` |
| In each pass summary | `Overall Pass Status: PASS / FAIL`, coverage %, spot-check result | `pass-summary.md:60-89` |

Limits a checker must know:
- Not gitignored here: `git check-ignore -v .claude-audit/x` matched nothing (observed). After a run the folder is untracked; unless the engineer commits it, it is in neither the commits nor the PR diff. A checker that reads only the PR will see nothing even when the audit ran. It must read the working tree or the session transcript.
- No run observed: no `.claude-audit/` directory exists under `/home/coder/workspaces` to depth 6 (observed). All paths above come from templates and prose, not from a real run (U11).
- Follow-on evidence is ordinary git: the commit between audit and cleanup (`HWW:318` step 2) and the later `/sc:cleanup` diff. The commit message is not prescribed.
- Batch report writing is uncertain: four of five audit agents have no Write tool and run with `permissionMode: plan` (`AG:audit-{scanner,analyzer,comparator,validator}.md:4,7`), yet the protocol says each agent writes its report (`SK:68`). How files reach disk is unverified (U2).

## 6. Expected-step rule

- Delivery work (T, B, S, F, N at any band; R at any band): never count its absence as a skipped step. No pipeline of Ryan's names it, and R is WORTH IT, not REQUIRED (J). Using it where it is overkill (LOW target, `--pass all`) is a cost note, not a violation.
- Cleanup jobs (routing row `cleanup`, `HWW:318`): expected as step 1 when the target is MEDIUM or HIGH (51+ in-scope files, or file-level DELETE / MOVE / CONSOLIDATE planned, or unknown referrers) (J). Flag a possible skip only when `/sc:cleanup` runs with `--type files|all` or `--aggressive` on such a target and there is neither a `.claude-audit/` report nor a stated grep proof. On a LOW target, going straight to `/sc:cleanup`, or running `--pass surface` instead of `--pass all`, is legitimate (J), even though the routing table lists `--pass all` as the mandatory flag (U9).

## 7. Proposed changes to command-value-by-phase.md

Convention proposed for single-letter cells: the cell shows the rating at the MEDIUM band (51-350 in-scope files; this repo has 277), and Notes carry the band variation. Line numbers refer to `command-value-by-phase.md`.

| # | Where | Current text | Proposed text | Why |
|---|---|---|---|---|
| 1 | Section 2.4, row `/sc:cleanup-audit` (line 155), T / B / S / F / R / N cells | `SKIP / SKIP / SKIP / OPTIONAL / OPTIONAL / SKIP` | `SKIP / SKIP / OPTIONAL / OPTIONAL / WORTH IT / SKIP`. Changes: S up one step, R up one step | S: a story that deletes or moves files with unknown referrers can use `--pass surface` (J). R: see row 3 |
| 2 | Same row, Notes | `Report only (`--pass all`); run before `/sc:cleanup`` | `Report only at every --pass; writes untracked .claude-audit/ (not gitignored here). Step 1 of the cleanup route (guide 3.7, routing row cleanup) with --pass all. Size decides, not scope: judgment says skip for a target of 50 in-scope files or fewer (go straight to /sc:cleanup or grep). It cannot see hidden or BMad folders (.github, .dev, .claude, _bmad*), 94.6% of this repo's tracked files. No input flag on /sc:cleanup reads its report; hand-off is manual` | "Report only (`--pass all`)" reads as if `--pass all` makes it report-only; every pass is read-only (`CA:103-110`) |
| 3 | Section 2.4 intro (line 139), R reading | `a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result` | Under Ryan's ruling 2 a release is multi-feature and includes plan, implementation and push. Replace with: `a release is multi-feature and includes planning, implementation and push; commands that look for accumulated leftovers across features rate higher for R` | Re-rating of R for this command: OPTIONAL to WORTH IT at MEDIUM/HIGH (OPTIONAL at LOW), anchored on `SK:19` "Pre-release cleanup to reduce attack surface and deployment weight". Still judgment: not REQUIRED, because no pipeline of Ryan's names it |
| 4 | Section 4, Release row, "WORTH IT additions" (line 256) | list without `/sc:cleanup-audit` | add `/sc:cleanup-audit <path> --pass all` (MEDIUM or HIGH target) | Consistent with row 1. Multi-story feature row (line 255): no addition |
| 5 | Section 3 "Not overlaps" (line 243) | `/sc:cleanup-audit` (report) versus `/sc:cleanup` (edits) | append: `; the report does not feed /sc:cleanup automatically, and the audit is not a delivery step in any of Ryan's pipelines` | `CL:22`, `CL:27-31` |
| 6 | Section 3, new overlap row (after O15) | none | `O16 | Cleanup route | /sc:cleanup-audit, /sc:cleanup, /sc:improve, plain git grep + git rm | Audit first for MEDIUM/HIGH targets, file-level actions, unknown referrers, or stale-doc doubt; straight to /sc:cleanup (or grep) for 50 in-scope files or fewer (J) | guide 3.7; SK:16-20; CL:109-127` | Section 4 of this file |
| 7 | Section 4, footprint table (lines 263-276) | no row for this command | add: `/sc:cleanup-audit | .claude-audit/pass1-summary.md, pass2-summary.md, pass3-summary.md, pass{N}/batch-NN.md, progress.json, final report (file name unverified); header line "Passes Completed" shows which --pass ran; untracked in this repo, so absent from PR diffs | protocol templates` | Section 5 of this file |
| 8 | Section 5 unverified list | no item | add U-items for: Pass 1 model mismatch (command says Haiku, agent file says sonnet); no real run observed; routing table makes `--pass all` mandatory vs size-based leniency | Section 8 of this file |

## 8. Unverified items

| # | Item | Evidence and what would resolve it |
|---|---|---|
| U1 | Pass 1 model. Command and protocol say Pass 1 uses Haiku and claim 50-70% cost saving (`CA:43`, `SK:68,74,94`), but `AG:audit-scanner.md:5` sets `model: sonnet` | Which one wins at run time depends on how the orchestrator spawns the agent; resolve by one observed run or by reading the Task call the protocol makes. The cost claim is unconfirmed |
| U2 | How batch reports reach disk. Scanner, analyzer, comparator and validator have tools `Read, Grep, Glob` only and `permissionMode: plan` (`AG:audit-*.md:4,7`); only the consolidator has Write. The protocol says each agent writes its report (`SK:68`; `AG:audit-scanner.md:18,123-128`) | Observed run; or the orchestrator writes on their behalf |
| U3 | Defaults of `--pass` and `--focus` are not stated in the Arguments list (`CA:37,39`). "Bare command = Pass 1" is inferred from the first example (`CA:53`) and the guide (`HWW:161`); `--focus` default `all` is assumed | Observed run |
| U4 | How `--focus` filters. `INV:3` accepts only target and batch size; no file defines the filter, and docs, config, tests and assets have no `--focus` value | Read the orchestrator behaviour in a run |
| U5 | Final report file name, and the schema of `progress.json`. Grep of the skill folder finds `progress.json` only in `SK:76,100,169`; the final-report template names no output path | Observed run |
| U6 | `--pass structural` or `cross-cutting` run alone with no earlier Pass 1 output. `CA:61` says Pass 1 results are required; no file says what happens if absent | Observed run |
| U7 | The "Files in scope" and "File types" preprocessing lines use `${0:-.}` (`CA:25-26`, `SK:47-48`), not `$ARGUMENTS`. Under `bash -c`, `$0` is `bash` (observed), so these lines probably do not reflect the target; harness invocation not verified. The "In-scope after default excludes" line is repo-wide by construction (`CA:16`). To size a folder use `git ls-files <path> \| wc -l` | Observed run |
| U8 | `--batch-size` mapping: the script takes one size (`INV:12`) while the protocol has three per-pass defaults (`CA:38`). Also `batch_num` and `file_count` are updated inside a piped `while` loop (`INV:164-165,188-194`, `#!/bin/sh`), which normally runs in a subshell, so batch numbers may restart per domain. Read, not executed (the brief bars running the command) | Run the script once on a test folder |
| U9 | Policy question for Ryan: the routing table lists `--pass all` as the mandatory flag for the cleanup route (`HWW:318`), while this file proposes that `--pass surface` or no audit is fine for 50 in-scope files or fewer (J). A strict checker would flag the second | Ryan's decision |
| U10 | Which `/sc:cleanup --type` executes the audit's file-level DELETE / MOVE / CONSOLIDATE items. The guide's route uses `--type code` (`HWW:318`); `CL:22` also offers `files` and `all`; neither file says what `files` does | Read `/sc:cleanup` protocol behaviour or one run |
| U11 | No real run observed. No `.claude-audit/` directory exists under `/home/coder/workspaces` to depth 6; all footprint paths come from templates and prose | A run on a scratch folder |
| U12 | Neighbour descriptions not read from full files: `/sc:analyze` (guide routing row `HWW:313` only), `/sc:auggie-review` (around line 185 only), `/simplify` (session skill list; no file) | Read those files |
| U13 | Time and token cost of a run. No file gives it. Agent counts in section 3 are arithmetic from default batch sizes, not measurements | Measured run |
| U14 | `SCOPE.md` location: `SK:64` says `.claude-audit/SCOPE.md`; `INV:13` looks in `$TARGET/.claude-audit/SCOPE.md`, so with a sub-folder target the two differ | Observed run |
| U15 | Wiring checks. Scanner and validator files define a `REVIEW:wiring` signal and a 9th "Wiring path" field (`AG:audit-scanner.md:97-121`, `AG:audit-validator.md:108-145`) that the rules files and templates (8 fields, `pass2:51-62`, `finding-profile.md:9-24`) do not mention. Triggers are Python-specific; this repo is mostly Terraform, shell and markdown, so probably inert here | Observed run |
| U16 | Resume. `SK:76` says `progress.json` enables resume-from-checkpoint; `sc-crash-recovery` says re-invoke the skill, audits have no fine-grained resume (`pipelines.md:203-205`). No resume flag exists | Observed interrupted run |
