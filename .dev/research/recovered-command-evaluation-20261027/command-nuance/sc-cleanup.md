# Command nuance: /sc:cleanup

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: flags by risk and size; relationship to `/sc:cleanup-audit`; destructive-action guard rails.
Paths: `~/.claude/commands/sc/cleanup.md` is cited as `cleanup.md:N`; `~/.claude/commands/sc/cleanup-audit.md` as `audit-cmd:N`; `~/.claude/skills/sc-cleanup-audit-protocol/SKILL.md` as `audit-skill:N`; `~/.claude/HOW-WE-WORK.md` as `HWW:N`; the main table as `value:N` (`command-value-by-phase.md`). Other names are relative to `~/.claude/`: `improve.md` = `commands/sc/improve.md`, `analyze.md` = `commands/sc/analyze.md`, `verification-protocol.md` and `dynamic-use-checklist.md` = `skills/sc-cleanup-audit-protocol/rules/`, `templates/final-report.md` and `repo-inventory.sh` = under `skills/sc-cleanup-audit-protocol/` (`templates/`, `scripts/`), `delegation-vs-native-heuristics.md` = `skills/sc-recommend/refs/`, `task-builder/SKILL.md` = `skills/task-builder/SKILL.md`, repo `CLAUDE.md` = `IB-CPlus-01/CLAUDE.md`.
## 1. Status and role

- Does: "Systematically clean up code, remove dead code, and optimize project structure" (`cleanup.md:3`). It EDITS files (`cleanup.md:49`, Edit/MultiEdit). Phase: Implement (value:154). Standalone-invokable; not retired. It is not `/sc:task` or `/sc:tasklist`.
- Backing skill `~/.claude/skills/sc-cleanup-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"). The command file names no skill to load (no Activation block, unlike `audit-cmd:79-84`), so it runs from its own 128 lines (consistent with HWW:232). Nothing beyond `cleanup.md` specifies its behaviour.
- Overlaps: `/sc:cleanup-audit` (its report-only pair, `audit-cmd:119`), `/sc:improve` (same guard-rail pattern, `improve.md:108-129`), built-in `/simplify` (value:156), plain edit.

## 2. Flags

Usage line: `/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--interactive]` (`cleanup.md:22`). No backing skill, so these are the only definitions. No flag has a stated default (`cleanup.md` has no defaults section): every default below is UNVERIFIED.

| Flag | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `[target]` | path (file or folder); omitted is shown in an example (`cleanup.md:73`, `:81`) | not stated (UNVERIFIED whether omitted means whole repo) | Limits scope of analysis and edits ("across target scope", `cleanup.md:27`). Risk driver number one: the guide says run it "on a folder" (HWW:22, HWW:164). | Always pass an explicit folder (J). | Omitting it, or `.`, in this repo: no exclusion list exists in `cleanup.md`, so `.dev/`, `_bmad-output/`, `.github/` are not protected (J; contrast `audit-skill:54-62`). |
| `--type` | `code`, `imports`, `files`, `all` | not stated | `code` = dead code removal; `imports` = unused import removal; `files` = file organization and structure; `all` = every domain with all three personas (`cleanup.md:55-58`, `:81-83`). Examples only show `code`, `imports`, `all`. | `code` is the only value the guide's routing row names (HWW:318, mandatory step 3: `--type code --safe --interactive`). `imports` for a language-specific import sweep. | `files` and `all`: `files` moves and removes files, and whole-file removal is in NEITHER the auto-fix list nor the approval list (`cleanup.md:109-121`). `all` also "activates all personas" (`cleanup.md:83`) over the widest target. Treat both as HIGH risk (J). |
| `--safe` | flag | not stated (one of the pair `--safe\|--aggressive`) | "Conservative cleanup with automatic safety validation" (`cleanup.md:66`). | Every run (the guide's row carries it, HWW:318). | n/a |
| `--aggressive` | flag | not stated | "Thorough cleanup with Context7 framework patterns" (`cleanup.md:90`). No definition of what extra it removes. | Never as a first pass (J). Only after a clean commit, on a named folder, with the diff read afterwards. | Anywhere the target holds shared interfaces, exports, config values or fixtures; those are approval-class (`cleanup.md:118-121`) and "aggressive" has no stated rule that keeps the prompt. Not in the guide's routing row (HWW:318), so using it is outside the documented path. |
| `--interactive` | flag | not stated | "User guidance for complex decisions" (`cleanup.md:82`). Does NOT stop auto-fixes: the guide says unused imports, zero-reference code, empty blocks and redundant type annotations are still applied automatically (HWW:166, matching `cleanup.md:111-114`). | Every run (HWW:318). It is the only prompt path for approval-class items. | Do not read it as "nothing changes without asking". |
| `--preview` | flag | n/a | Appears ONLY in one example: "shows unused import cleanup without execution" (`cleanup.md:73-74`). It is NOT in the Usage line (`cleanup.md:22`) and is defined nowhere. The same pattern exists in `improve.md:81`. | Try it as a dry run on a first pass over a new folder, but do not rely on it: UNVERIFIED that it is honoured. | Never treat `--preview` as a guard rail in a policy or checker. |

**Does not exist** (people may assume): `--dry-run`, `--backup`, `--rollback` (the file promises "backup and rollback capabilities", `cleanup.md:38`, `:98`, but defines no flag or mechanism; git is the only undo, HWW:163 "commit first so every change can be undone"), `--force` (only in `improve.md:125`), `--exclude`, `--from-audit` / any report-path input, `--depth`, `--pass`, `--focus` (those belong to `/sc:cleanup-audit`, `audit-cmd:31`), `--batch-size`. There is no per-project exclusion file: `.claude-audit/SCOPE.md` is read by `repo-inventory.sh` (`repo-inventory.sh:13`) for the audit only; `cleanup.md` never mentions it.

**Risk order, lowest to highest (J, built from the cited lists):** `--type imports --safe --interactive` on one file < `--type code --safe --interactive` on one folder (documented path, HWW:318) < the same with `--aggressive` < `--type files` < `--type all` < any of these with no explicit target.

**In-file guard rails** (`cleanup.md:107-127`): auto-fix = unused imports, dead code with zero references, empty blocks, redundant type annotations. Prompt first = indirect references, exports possibly used externally, test fixtures/utilities, configuration values. Safety threshold = any usage path, any public API effect, or any doubt means prompt. Gap: "zero references" has no stated method (no grep requirement, no dynamic-use check), while the audit requires a cited grep, a CI/Docker/package/build search, and five dynamic-loading patterns before it will even propose DELETE (`verification-protocol.md:20-25`, `dynamic-use-checklist.md:5-9`, `:120-130`). So `/sc:cleanup`'s auto-delete bar is lower than the audit's recommendation bar.

## 3. Scope x complexity matrix

**Bands for this command.** The command does vary by complexity, because the damage a cleanup can do scales with what it can reach. No file gives a cleanup threshold; the only on-disk numbers are the guide's 5-edit / one-source-file limit with its cleanup-on-a-folder exception (HWW:22) and task-builder's TCS, where a refactor-class file forces `--depth deep` (`task-builder/SKILL.md:2415`, `:2438`). Everything else is JUDGMENT (J).

| Band | Signals (all J except where cited) |
|---|---|
| LOW | One named folder or file; author can name the files up front; only auto-fix class items (unused imports, zero-reference code, `cleanup.md:111-114`); no exports, fixtures, config, CI or infra paths touched. |
| MEDIUM | One subsystem, several files; some items fall in the approval class (indirect references, exports, fixtures, config, `cleanup.md:118-121`); the author cannot list every file but can name the folder. |
| HIGH | More than one subsystem or whole repo; any `--type files` or `--type all`; target includes CI, infra, secrets or `.dev/` paths (repo `CLAUDE.md:8` makes `.dev/tasks` always-staged); public API or shared interfaces between stories; or the work reads as a structural refactor (HWW:168 sends that through `/task-builder ... --spec`, where a refactor `type:` scores TCS S6=1 and forces `--depth deep`). |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL (J): a plain edit does it; `--type imports\|code --safe --interactive` on one folder after a commit | WORTH IT (J): this is the guide's own standalone "tidy a folder" row (HWW:318, `changes_files` yes); `--type code --safe --interactive`, commit first | SKIP as a direct run (J): run `/sc:cleanup-audit <path> --pass all` first, then `/sc:cleanup` only on the audit's "Immediate" paths; a structural job is a feature (HWW:168) |
| B bug fix | SKIP (J) | SKIP (J) | SKIP (J). A bug fix should not carry unrelated deletions (diff widens, review gets harder); clean up in a separate commit or task after the fix merges. |
| S single story | OPTIONAL (J): dead code or imports the story created, `--type code --safe --interactive` on the story's files, before the commit | OPTIONAL (J): same flags; commit first | SKIP (J): too big to ride inside a story; split it out as its own story or task |
| F multi-story feature | OPTIONAL (J) | WORTH IT (J): after the last story, audit then cleanup of the feature's folder, `--type code --safe --interactive`, as its own commit | SKIP direct run (J): audit first; execute via a task package (`/task-builder`) so each deletion is a checklist item with review |
| R multi-feature release | OPTIONAL (J) | WORTH IT (J): `audit-skill:19` lists "pre-release cleanup to reduce attack surface and deployment weight" as a trigger; audit `--pass all`, then cleanup of "Immediate" items; do it early enough to merge and re-test before the release is sealed | SKIP direct run (J): audit report feeds a task package; never an unattended `--type all` at release time |
| N new product | SKIP (J): greenfield, nothing to clean | SKIP (J) | OPTIONAL (J), late only: one audit plus guarded cleanup before first release; never early |

Cells with no `(J)` marker: none. This matrix is judgment built on cited guard rails; the only file-stated cell content is the flag set in the T/MEDIUM cell, which copies HWW:318.

## 4. Choose this or the neighbour

**`/sc:cleanup-audit` then `/sc:cleanup` (the pair).** The audit is read-only (`audit-cmd:103-110`) and its own "Next Step" says to use `/sc:cleanup` to execute safe recommendations, then `/sc:test`, then `/sc:git` (`audit-cmd:119`, `audit-skill:171`). The guide's cleanup row orders it: audit (`--pass all`), commit, cleanup, improve, review `git diff` (HWW:318, HWW:159-166).

| Signal | Rule (J unless cited) |
|---|---|
| You can name the folder and it is LOW | Skip the audit. Commit, then `/sc:cleanup <folder> --type code --safe --interactive`. The audit costs a Haiku/Sonnet fan-out in waves of 7-8 agents plus a 10% spot-check (`audit-skill:68-69`), and `sc-recommend` warns a large protocol dwarfs a small task (`delegation-vs-native-heuristics.md:50`). |
| You cannot name the files, or scope is repo-wide, or HIGH | Audit first (`delegation-vs-native-heuristics.md:29`, `:40` rate the audit YES for scope above a few files or whole repo). Pass an explicit path and `--pass all`; without `--pass all` it runs only the quick first pass (HWW:161). |
| You want to delete or move WHOLE FILES | Audit first, always (J). Only the audit holds a written evidence bar for DELETE (grep count, CI/Docker/package search, five dynamic-load patterns, successor or transient; `verification-protocol.md:20-25`). `/sc:cleanup` has no equivalent and no rule for whole-file removal (`cleanup.md:109-121`). |
| The audit's report exists | Hand `/sc:cleanup` only the paths in the report's "Immediate (safe, no dependencies)" section (`templates/final-report.md:23-26`) as the `[target]`. There is no input flag for a report (see section 2), so the handoff is manual. Items under "Requires Decision" or "Requires Code Changes" (`final-report.md:28-36`) are not for `/sc:cleanup`: decide or plan them. |

Coverage gap to remember: the audit never sees hidden paths (`.github/`, `.dev/`, `.claude/`) or `_bmad/`, `_bmad-output/`, `_planning-input/` (`audit-skill:54-62`, `repo-inventory.sh:20`). In this repo that is the CI workflows, the task packages and the BMad artifacts. So the audit cannot clear a deletion there, and `/sc:cleanup` has no exclusion list. Do not point `/sc:cleanup` at those paths (J).

**`/sc:improve`.** Same sibling pattern: both are the guide's only exception to the 5-edit limit (HWW:22), both need a commit first and a read of `git diff` (HWW:163-166). Rule: removal of dead code, unused imports, empty blocks, redundant annotations = `/sc:cleanup`; formatting, naming, unused variables, import ordering, simple annotations, performance, maintainability = `/sc:improve` (`improve.md:110-115`, `:22`). They overlap on unused imports (`cleanup.md:111` vs `improve.md:113-114`); run cleanup first (HWW:318 steps 3 then 4) and do not run both on the same files in LOW work (J).

**`/simplify` (built-in).** Diff-scoped: reviews changed code for reuse and simplification and applies fixes; "run before the commit, not after review" (value:156; no file, description from the session skill list). Rule (J): tidying code you just wrote in this branch = `/simplify`; removing dead code that already existed in a folder = `/sc:cleanup`.

**`/sc:analyze`.** Reports only (value:177); its Next Step names `/sc:improve` or `/sc:cleanup` (`analyze.md:111`). Use it when you want a health read on a module before deciding; it is lighter than the audit but gives no deletion evidence.

**Plain edit.** At LOW with named lines (one file, 5 edits or fewer) a plain edit plus the related test is enough (HWW:16, HWW:304). `/sc:cleanup` earns its use only on a folder (HWW:22).

**`/task-builder` + `/task`.** Large or structural refactors are treated as a feature: spec plus `/task-builder ... --spec` (HWW:168; routing row note at HWW:318). Any HIGH cell above goes here, not to a raw `/sc:cleanup`.

## 5. What a scheduled checker can see

| Item | Footprint | Source |
|---|---|---|
| `/sc:cleanup` run | None of its own. `cleanup.md` names no output file, ledger or frontmatter; step 5 "Report" is a "cleanup summary" with no path (`cleanup.md:31`). Transcript only, plus the working tree: deleted or edited tracked files (`git diff`, `git status`) and, if the engineer committed, a commit. | `cleanup.md:25-31`; UNVERIFIED by observation (command not run, per brief) |
| Pre-cleanup commit | Guide asks "commit first" (HWW:163). A checker could look for a commit immediately before the cleanup diff. Weak signal (J). | HWW:163 |
| `/sc:cleanup-audit` run | `.claude-audit/` with per-batch reports, `pass1-summary.md`, `pass2-summary.md`, `pass3-summary.md`, a final report, and `progress.json` (`audit-skill:164-169`, `templates/final-report.md:118-122`). The final report's exact filename is not stated in the files read: UNVERIFIED. | `audit-skill:164-169` |
| Is `.claude-audit/` visible in git? | Not present in this worktree now (`ls` failed), 0 tracked files under it, and no `.gitignore` line mentions it. So an audit run leaves an UNTRACKED directory in this repo unless the engineer ignores it. Repo `CLAUDE.md:8` requires only `.dev/tasks` to be staged; it says nothing about `.claude-audit/`. | observed this session |
| Task-package link | If cleanup ran inside a `/task` package, the footprint is the package under `.dev/tasks/<pkg>/` (checklist items, `artifacts/`), not anything from `/sc:cleanup`. | repo `CLAUDE.md:8` |

Gap to flag to the brainstorm: the audit leaves evidence; the destructive step leaves none. A checker can prove an audit ran but can only infer, from the diff, that a cleanup followed it (J).

## 6. Expected-step rule

- `/sc:cleanup` is never an expected step at any scope x complexity: the matrix has no REQUIRED cell, and WORTH IT appears only at T/MEDIUM, F/MEDIUM and R/MEDIUM (J). A checker must not flag its absence anywhere. Only the repo's own pipeline steps (spec, tasklist, implement, commit, push) are expected; cleanup is an extra.
- A checker should instead flag unguarded presence (J): a diff that deletes or moves whole tracked files, or touches `.dev/`, `_bmad-output/` or `.github/`, with no commit before it and no `.claude-audit/` report or task-package item behind it, at HIGH or with `--type files|all`. The audit is expected before whole-file deletions at HIGH, not before LOW code-and-import tidying.

## 7. Proposed changes to command-value-by-phase.md

Proposals only (file not edited).

| Where | Current | Proposed |
|---|---|---|
| value:154 `/sc:cleanup`, T cell | SKIP | OPTIONAL (J). A standalone "tidy a folder / dead code / unused imports" job is the guide's own one-off row (HWW:318) and the one allowed exception to the 5-edit limit (HWW:22). |
| value:154, B / S / F / N cells | SKIP / OPTIONAL / OPTIONAL / SKIP | No change to the single letters. Add the complexity layer from section 3: S and F are OPTIONAL at LOW, F is WORTH IT at MEDIUM, HIGH is not a direct run. |
| value:154, R cell (re-rated under the multi-feature release definition) | OPTIONAL | OPTIONAL at LOW, WORTH IT at MEDIUM, SKIP direct run at HIGH (J). Letter-level cell stays OPTIONAL; the change is the MEDIUM nuance, backed by `audit-skill:19` ("pre-release cleanup"). N stays SKIP (OPTIONAL only late at HIGH). |
| value:139 (reading of the R column in Implement) | "a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result" | Reading no longer matches the redefined R (a multi-feature release includes planning, implementation and push). It does not change this row's cell, but the merge step should reword it. |
| value:154 Notes | "Same guard rails as `/sc:improve`" | "Backing skill `sc-cleanup-protocol` does not exist; runs from its own file. NOT the same guard rails as `/sc:improve`: it has no `--force` and no stated rule for whole-file removal. Auto-applies unused imports, zero-reference code, empty blocks, redundant annotations even with `--interactive`. Commit first; always `--type code --safe --interactive`; give an explicit folder; never point it at `.dev/`, `_bmad-output/`, `.github/`. No output file: checker sees the git diff only." |
| value:155 `/sc:cleanup-audit` Notes | "Report only (`--pass all`); run before `/sc:cleanup`" | Add: "Excludes hidden paths and `_bmad*` directories (so not `.github/`, `.dev/`, `_bmad-output/`). Output `.claude-audit/` is untracked in this repo. `/sc:cleanup` has no input flag for the report: hand it the 'Immediate' paths by hand. Run first for whole-file deletions or HIGH work." Its R cell (OPTIONAL) deserves a re-rate to WORTH IT at MEDIUM and HIGH (J): `audit-skill:19`; the audit command's own nuance file should confirm. |
| value:243 | "Not overlaps despite similar names: ... `/sc:cleanup-audit` (report) versus `/sc:cleanup` (edits)." | Keep, but add that they are a sequenced pair, not alternatives (`audit-cmd:119`, HWW:318). |

## 8. Unverified items

1. Backing skill `sc-cleanup-protocol` is absent; whether one was intended is unknown. Behaviour beyond `cleanup.md` is unspecified.
2. Defaults for `[target]` (omitted), `--type`, and `--safe` vs `--aggressive` are not stated anywhere.
3. `--preview` is used in an example (`cleanup.md:73`) but not in the Usage line or any definition; whether it works is unknown.
4. "Backup and rollback capabilities" (`cleanup.md:38`, `:98`) have no described mechanism; git is assumed to be the only undo.
5. How "zero references" is decided (grep, Serena, other) is not stated; no dynamic-loading check is required of `/sc:cleanup`.
6. Whether whole-file deletion or move (`--type files`) is auto-fixed or prompted: absent from both lists (`cleanup.md:109-121`).
7. Whether `--aggressive` bypasses the approval-required list: not stated.
8. Whether `/sc:cleanup` reads `.claude-audit/` reports or `SCOPE.md`: no mention in `cleanup.md`; not observed.
9. Final-report filename under `.claude-audit/`: not named in the files read.
10. The premise "the repo requires approval before deleting" was NOT found in a repo or home rule file: grep of repo `CLAUDE.md` and `~/.claude/CLAUDE.md` for delet/destruct/approval found nothing; `HWW:229` covers pushing only. The only on-disk approval gate for deletions is the in-command list (`cleanup.md:116-126`). No hook or `settings.json` deny rule was found by grep for deny/`rm -`/cleanup, but `settings.json` (45 KB) was not read in full.
11. How `/sc:cleanup` treats tracked `.dev/tasks` files (repo `CLAUDE.md:8` says always staged): not specified; not observed.
12. `/simplify` has no file; its description comes from the session skill list and value:156.
13. No run of any command was made (brief rule), so every footprint claim in section 5 is by reading, not observation, except the `.claude-audit/` absence check.
14. The T row relies on the PROPOSED (not yet confirmed by Ryan) one-off minimum of a plain edit plus the related test.
