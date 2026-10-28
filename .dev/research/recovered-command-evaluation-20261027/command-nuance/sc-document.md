# Command nuance: /sc:document

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: when one-pass reference text is enough versus `/tech-reference`, `/operational-guide` or `/readme`, by complexity and scope.

Sources read: `~/.claude/commands/sc/document.md` (101 lines, in full; cited CMD). Backing protocol skill `~/.claude/skills/sc-document-protocol/` DOES NOT EXIST (`ls` exit 2); the command runs from its own file (`HOW-WE-WORK.md:232`; `sc-cli-eval-protocol/refs/integration-map.md:9-10` says "no `sc:document` skill"). Neighbours were read in part, not in full: `tech-reference/SKILL.md` lines 1-420 and 536-545 (cited TR), `operational-guide/SKILL.md` lines 1-200 plus greps (cited OG), `readme/SKILL.md` lines 1-200 plus greps (cited RM), all under `~/.claude/skills/`. `HOW-WE-WORK.md` cited HWW.

## 1. Status and role
- One sentence from its own file: "Generate focused documentation for components, functions, APIs, and features" (CMD:3). Single pass: Analyze, Identify, Generate, Format, Integrate (CMD:27-31). Frontmatter `complexity: basic` (CMD:5) is the command's own weight class, not a task-complexity signal.
- Phase: Document (post-implement / post-merge). Standalone-invokable; NOT retired; CMD never mentions `/sc:task` or `/sc:tasklist`. No backing skill, no task folder, no ledger.
- Overlaps: `/tech-reference`, `/operational-guide`, `/readme` (HWW:175-184, 246, 320), `/sc:post-release` at release level (its description covers user and technical docs; it does not name the doc skills, grep found no reference), `bmad-agent-tech-writer` / `bmad-document-project` in the BMad lane (value file:92,193).

## 2. Flags
The command has one positional argument and two flags (CMD:22). No defaults are stated for any of them (UNVERIFIED default behaviour).

| Flag / arg | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[target]` | file, directory, module or component name (CMD:59, 67, 75, 83) | none stated | Scope of the code analysis (CMD:27) | Always give a named path; "Will Not" generate docs "without proper code analysis and context understanding" (CMD:98) | Vague names or the whole repo: one pass cannot verify a large target (J) |
| `--type inline` | inline | not stated | JSDoc/docstring generation plus inline comments, "Adds comprehensive inline documentation for functions and classes" (CMD:49, 60-62). Edits source files. | A new or changed public function with no docstring. The only documentation path that touches source; no neighbour writes docstrings (TR:148, OG:153, RM:155 all write one document file) | Files where a docstring-only diff would mix with a feature diff in review (J) |
| `--type api` | api | not stated | Interface extraction, reference material, usage examples (CMD:50); "endpoints and schemas" (CMD:68). HWW's one example (HWW:184, 320 note) | A bounded interface: one route file, one module's public surface | Targets spanning several subsystems (use `/tech-reference`) |
| `--type guide` | guide | not stated | Feature analysis, tutorial content, implementation guidance (CMD:51); "user-focused documentation with practical examples" (CMD:76-77). Used by `/sc:cli-eval` to update an inventory table (integration-map.md:46-55) | Small edits to an existing guide; a brief how-to for a LOW target | Operator procedures (install, deploy, rollback): use `/operational-guide` (HWW:182) |
| `--type external` | external | not stated | Component overview, detailed specifications, integration instructions as external doc files (CMD:52, 83-85) | A component library folder needing a doc file | A README for a new module (use `/readme`) |
| `--style brief` | brief | not stated | Focuses on "implementation patterns and common use cases" (CMD:77-78 example) | LOW targets; edits to existing docs | HIGH targets |
| `--style detailed` | detailed | not stated | "comprehensive API documentation with endpoints and schemas", usage examples, integration guidelines (CMD:68-69 example) | MEDIUM interface docs | Using it as a substitute for a reviewed reference (no review step exists, CMD:25-31) |

Does NOT exist in CMD: `--depth` (the `--depth quick` flag belongs to `/sc:workflow`, validation-oneoff file), `--output` / `--path` (no output path convention at all), `--audience`, `--spec`, `--dry-run`, `--tier`, `--format`, `--no-write`. Output location is whatever the target and `--type` imply; CMD:44 only says "Write: Documentation file creation with proper formatting".

Neighbour "pseudo-flags" (natural-language only, no CLI flags in TR, OG or RM): the inputs WHAT / WHY / WHERE / OUTPUT (TR:38-47; OG:56-65; RM:55-68). Words "thorough", "comprehensive", "detailed" force Heavyweight (TR:93; OG:116; RM:122); "quick", "fast", "light QA", "basic" force `qa_intensity: lite` (TR:105; OG:128; RM:132). Default output paths: `docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md` (TR:47), `docs/docs-product/ops/[name]-operational-guide.md` (OG:61, a folder this repo does not have; this repo has `docs/operations/`), `[module-dir]/README.md` (RM:61). Pass the output path explicitly (HWW:41, 181-183 do).

## 3. Scope x complexity matrix
Does the command vary by complexity? Not in its own file: it is one fixed pass (CMD:25-31) with `--style` as the only dial, and `--style` is not tied to any signal. The variation below comes from the neighbours' own tier tables, which are the only on-disk file-count thresholds for documentation. Applying them to `/sc:document` is JUDGMENT.

Bands (signals: files in the target, subsystems, procedure vs reference, risk):
- LOW: target named up front; fewer than 5 relevant files; one subsystem; no new deploy or operator steps. Borrowed boundary: TR:83, 85 (Lightweight "<5 relevant files"), RM:110, OG:108.
- MEDIUM: 5-20 files or several subsystems, but the reader needs reference for one bounded interface. Borrowed: TR:88 (Standard "5-20 files, multiple subsystems"), OG:109 (5-15 config files).
- HIGH: 20+ files, cross-cutting, several integration points, multi-machine or multi-environment, or content touching secrets, permissions, paths, infrastructure. Borrowed: TR:89, 95; OG:110, 118. CMD:100 also bars docs that expose "sensitive implementation details", and the user NFR12 rule bars secrets in docs: one unreviewed pass is the wrong tool here.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J). A docstring is part of the edit itself; `--type inline` OPTIONAL only when a new public function has none | SKIP (J) | SKIP (J) |
| B bug fix | SKIP (J) | SKIP (J) | SKIP (J) |
| S single story | OPTIONAL (J) `--type inline --style brief` or `--type api --style brief` | OPTIONAL (J) `--type api --style detailed` on the changed interface | OPTIONAL (J) `--type api --style detailed`; escalate to `/tech-reference` at 20+ files (TR:89) |
| F multi-story feature | WORTH IT (J) `--type api --style detailed`; cheaper than the `/tech-reference` minimum | OPTIONAL (J) `--type inline` only; `/tech-reference` covers the rest | OPTIONAL (J) `--type inline` only; the reference is `/tech-reference` |
| R multi-feature release | OPTIONAL (J) `--type api` per feature | OPTIONAL (J) `--type inline` | OPTIONAL (J) `--type inline` only; release docs are `/tech-reference` per feature, `/operational-guide`, `/sc:post-release` |
| N new product | OPTIONAL (J) `--type guide --style brief` | OPTIONAL (J) `--type inline` | OPTIONAL (J) `--type inline` only; the module README is `/readme` (RM:61) |

Exception in any cell: if a `/sc:troubleshoot` REPORT.md says the fix belongs "in the documentation" (HWW:128), the doc edit IS the fix; a plain edit or `/sc:document <file> --type guide --style brief` both fit (J).
No cell is REQUIRED: no file requires this command at any scope.

## 4. Choose this or the neighbour
Cost anchor: the three doc skills are NOT one-pass. Each runs Stage A scope discovery, writes a BUILD-REQUEST, calls `/task-builder`, then `/task` over 7 phases with analyst, QA and fidelity gates (TR:159-183; OG:164-188; RM:170-194). Even the Lightweight tier (TR:85: 2-3 codebase agents, 400-600 lines) goes through that pipeline; only "trivial updates to an existing tech reference" use the simple Template 01 (TR:368). Neither `/task-builder` nor `/task` is retired. So the question is "does this documentation justify a research-and-QA pipeline", not "which template".

| Neighbour | Pick the NEIGHBOUR when (signals) | Pick `/sc:document` when | Cited |
|---|---|---|---|
| `/tech-reference` | A whole feature or subsystem, not a named file; 5+ relevant files or more than one subsystem; the reader needs architecture, how it works, how to extend; claims must be code-verified (the skill tags CODE-VERIFIED / CODE-CONTRADICTED, TR:792); the document will be relied on later by maintainers | A named file, route file or small module (under 5 files); reference text, not architecture; or `--type inline` docstrings (no neighbour does that) | HWW:181, 246; TR:85-95, 792 |
| `/operational-guide` | The reader EXECUTES steps: install, deploy, operate, roll back; multi-service or 5+ config files; multi-machine or multi-environment; infrastructure or secrets handling | LOW only: single-service, under 5 config files, linear procedure, no secret handling, and `--type guide --style brief` is enough (J) | HWW:182; OG:106-118 |
| `/readme` | A new package or module needs a navigational entry file at the module root; README must follow `readme_template.md`; 500-line ceiling | Editing an existing README or one table in it (the `/sc:cli-eval` create flow does this with `--type guide`) | HWW:183; RM:55-61, 116; integration-map.md:46-55 |
| `/sc:post-release` | Multi-feature release already tagged; the whole external surface (user docs, technical docs, install scripts, e2e guides) must be synchronised | Per-target docstrings or API text written during the release, before the tag | `commands/sc/post-release.md:3` |
| `/sc:explain` | Reader only needs an answer, no file (HWW:15) | You need the text on disk | HWW:15 |
| BMad `bmad-agent-tech-writer`, `bmad-document-project` | Work is in the BMad lane; pick the lane at the Spec step and stay in it | Task-file lane | value file:92, 193, 223 |

Cross-pick rule: never run `/sc:document` and `/tech-reference` for the same target and the same output type (value file:50 `‡`, 237). The one safe pairing is `/tech-reference` for the document plus `/sc:document --type inline` for docstrings (J).

## 5. What a scheduled checker can see
| Command | Footprint | Source |
|---|---|---|
| `/sc:document` | None of its own: no task folder, ledger, frontmatter or fixed output path (CMD has no output section; whole file read). Transcript only. Indirect: a commit whose diff has docstring/comment-only hunks (`--type inline`) or new/changed `*.md` files (other types). UNVERIFIED, never observed | CMD:44, 49-52 |
| `/tech-reference` | `.dev/tasks/to-do/TASK-TECHREF-<subject>-YYYYMMDD-HHMMSS/` holding the task file, `research-notes.md`, `research/`, `synthesis/`, `qa/`, `reviews/`; task frontmatter `status: "🟢 Done"` and `completion_date`; final `docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md` | TR:113-148, 541 |
| `/operational-guide` | `TASK-OPSGUIDE-<subject>-...` folder, same subfolders; final `docs/docs-product/ops/[name]-operational-guide.md` unless the engineer passed a path. OG:48 says the folder moves to `.dev/tasks/completed/` at Done; this repo uses `done/` | OG:37, 48, 140-153 |
| `/readme` | `TASK-README-<subject>-...` folder; final `[module-dir]/README.md`; 11 lens QA reports in `qa/` | RM:36, 144-156 |

Repo check on 2026-10-27: `.dev/tasks/to-do` (20), `done` (33), `archive` (1) contain 0 `TASK-TECHREF-*`, `TASK-OPSGUIDE-*`, `TASK-README-*` folders. The only technical-reference file, `_bmad-output/planning-artifacts/aidev02-v1.0-as-built-technical-reference.md` (54 lines), says it was "Produced by the `bmad-retrospective` milestone-exit reconciliation gate" (line 13), so it is not evidence of `/tech-reference` use. `docs/operations/aidev02-operator.md` is 3467 lines, above the 1,000-line ceiling in OG:112, so it was not (or is no longer) an `/operational-guide` output (inference). Existing docs here are hand-maintained; updating them is an edit, which leaves no doc-skill folder.

Under the repo rule that `.dev/tasks/` is always staged (project `CLAUDE.md`), any doc-skill folder would show up in git. A task file `type:` of "📝 Documentation" is possible (task-builder template comment, `task-builder/SKILL.md:2160`) but the doc skills' BUILD_REQUEST sets no `type` (TR:376-419): UNVERIFIED.

## 6. Expected-step rule
- `/sc:document` is never an expected step at any scope x complexity. The only routing-table row that names it is `document-built`, an either-or among four commands with `mandatory_flags` "-" (HWW:320). Absence is always fine; presence is always fine.
- What a checker MAY expect is "some documentation action" for F, R and N at MEDIUM or HIGH complexity (HWW:87, step 11 of the full-spec flow; value file:255-257 lists the doc skills as additions, not minimums), satisfied by any of `/tech-reference`, `/operational-guide`, `/readme`, `/sc:document`, a plain docs edit, a BMad tech-writer step, or doc items inside the task file (J). For T and B expect nothing. Do not flag a missing `TASK-TECHREF-*` folder when docs were edited by hand.

## 7. Proposed changes to command-value-by-phase.md
Proposals only; the main file was not edited. Line numbers refer to that file.

**R re-rating (multi-feature release).** Rating letters do not change for the four doc commands; the reading changes. The old R column fits "one release's docs"; under the new definition the doc sweep is per feature plus release level, and `/sc:post-release` (line 186, R: WORTH IT) is the release-level vehicle. Proposal: add to the R reading "per feature, scaled by complexity band" and the cells below.

| Line | Current | Proposed |
|---|---|---|
| 192 `/sc:document` | `SKIP SKIP OPTIONAL OPTIONAL OPTIONAL OPTIONAL` / "One-pass reference text (`--type api`). ‡ with `/tech-reference`" | Ratings unchanged. Notes: "One pass, no task folder, no backing skill, no ledger: transcript only. `--type inline` is the only path that writes docstrings; no neighbour covers it. Use for a named target of under 5 files; at 5+ files or several subsystems use `/tech-reference`. Never required. R (multi-feature): OPTIONAL at LOW and MEDIUM, `--type inline` only at HIGH (J)." |
| 189 `/tech-reference` Notes | "Repo already carries `aidev02-v1.0-as-built-technical-reference.md`. ‡ with `/sc:document`" | Remove the repo-evidence sentence: that file says it was produced by `bmad-retrospective` (its line 13), and `.dev/tasks` holds 0 `TASK-TECHREF-*` folders. Replace with: "Full pipeline even at Lightweight tier (`/task-builder` + `/task`, 7 phases). Footprint `TASK-TECHREF-*`. S: OPTIONAL at HIGH only (J). R: per feature, WORTH IT at MEDIUM and HIGH, OPTIONAL at LOW (J)." |
| 190 `/operational-guide` Notes | "Repo has `docs/operations/*`. Needed when deploy or operator steps changed" | Keep the trigger, make it the rule: "Rated by trigger, not scope: WORTH IT in ANY scope when deploy or operator steps changed (J), otherwise SKIP. Default output `docs/docs-product/ops/` does not exist here: pass the path. Existing `docs/operations/aidev02-operator.md` is 3467 lines, above the skill's 1,000-line ceiling, so edit it by hand." |
| 191 `/readme` Notes | "Only for a new package or module" | Add: "Footprint `TASK-README-*`; 500-line ceiling; output at the module root. Updating one table in an existing README is a plain edit or `/sc:document <file> --type guide`." |
| 237 O11 "Why" | "Researches a whole feature and is reviewed; `/sc:document` is one-pass reference for specific code" | Append the decision rule: "`/tech-reference` when 5+ relevant files or several subsystems; `/operational-guide` when the reader executes steps; `/readme` for a new module; `/sc:document` for a named target under 5 files, or `--type inline` at any size." |
| After 269-276 (footprint table) | No rows for the four doc commands (line 276 lists commands with no footprint but not these) | Add four rows from section 5 of this file. `/sc:document`: "none, transcript only". |
| 260 (skippable list) / 256 (R path) | R path lists `/operational-guide`, `/tech-reference` as WORTH IT additions | Keep; add `/sc:post-release` as the release-level docs step after the tag (already at line 256) and note that a checker must not require the doc skills by name. |

Also add a one-line cross-reference to the scope x complexity matrix of this file in the doc rows, so the main file shows `/sc:document` as OPTIONAL only (J) and never REQUIRED.

## 8. Unverified items
| # | Item | Why |
|---|---|---|
| 1 | Defaults for `--type` and `--style` | CMD:22 lists values only; no default stated anywhere |
| 2 | Where `/sc:document` writes `api|guide|external` output | CMD:44 says only "Documentation file creation"; no path convention |
| 3 | Whether `--type inline` edits source in place or prints | CMD:62 says "Adds"; no protocol file to confirm |
| 4 | No backing protocol skill | `sc-document-protocol` absent (`ls` exit 2); behaviour is only what CMD:25-31 states |
| 5 | Any observed output of any doc command | Nothing run; 0 `TASK-TECHREF/OPSGUIDE/README` folders in this repo's `.dev/tasks` |
| 6 | Neighbour skills read in part only | TR lines 1-420 and 536-545; OG 1-200 and greps; RM 1-200 and greps. Agent prompts and QA details unread |
| 7 | Contradiction inside `tech-reference/SKILL.md` | TR:88 puts "multiple subsystems" in Standard; TR:95 says multiple subsystems is "always Heavyweight". The MEDIUM/HIGH boundary for subsystems is therefore unclear |
| 8 | Where a finished doc-skill folder ends up | OG:48 says `.dev/tasks/completed/`; TR and RM do not say; HWW:83 says leave folders in `to-do/`; this repo uses `done/` |
| 9 | Whether `/sc:post-release` calls the doc skills | grep for their names in the command and protocol found nothing; how it writes docs is unread |
| 10 | Whether doc-skill task files carry `type: "📝 Documentation"` | Template comment only (`task-builder/SKILL.md:2160`); BUILD_REQUEST sets none |
| 11 | All LOW / MEDIUM / HIGH thresholds applied to `/sc:document`, and every `(J)` cell | Borrowed from neighbours' tier tables; no file states them for this command |
| 12 | Whether `docs/operations/aidev02-operator.md` was ever generated by a doc skill | Inferred from its length (3467 vs the 1,000-line ceiling); git history not checked |
