# /sc:git: scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: `/home/coder/.claude/commands/sc/git.md` (91 lines, cited as CMD). Backing protocol skill `/home/coder/.claude/skills/sc-git-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"; also no other skill named `*git*` under `~/.claude/skills`). So CMD is the whole definition.
Context read: `~/.claude/HOW-WE-WORK.md` (cited HWW), `command-value-by-phase.md` (cited CVP), `/home/coder/workspaces/worktrees/Coder/IB-CPlus-01/CLAUDE.md` (cited REPO-CLAUDE).

## 1. Status and role
- Does: "Git operations with intelligent commit messages and workflow optimization" (CMD:3). Serves the Commit phase only (CVP section 2.5). Standalone-invokable, not retired; CMD never mentions `/sc:task` or `/sc:tasklist`.
- Overlaps: plain `git` (HWW:272 "Commit with a generated message"), `/sc:pr-submit` (push and PR, not commit; its L2 ceiling leaves edits uncommitted, `skills/sc-pr-submit-protocol/SKILL.md:194`). Callers elsewhere only suggest it as optional: `/sc:implement` ("not gates", `commands/sc/implement.md:140`, `skills/sc-implement-protocol/SKILL.md:171`) and `/sc:cleanup-audit` (`commands/sc/cleanup-audit.md:119`).
- Frontmatter says `complexity: basic`, `mcp-servers: []`, `personas: []` (CMD:5-7). That label describes the command itself, not a task-complexity band.

## 2. Flags
Usage line: `/sc:git [operation] [args] [--smart-commit] [--interactive]` (CMD:22). No default is stated for any of them. No protocol skill exists, so nothing else defines them.

| Flag / argument | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `[operation]` | `status`, `add`, `commit`, `push`, `pull`, `branch` (CMD:14); `merge <branch>` appears only in an example (CMD:75) | none stated | Selects the git command to run (CMD:29) | `status` for a state summary and next steps (CMD:59-61) | `push`: HWW:229 says never push without approval; CMD does not list push as needing confirmation (CMD:89 covers "destructive operations" only). UNVERIFIED how it behaves |
| `[args]` | free text, e.g. a branch name (CMD:75) | none | Passed to the operation | n/a | n/a |
| `--smart-commit` | boolean | off | "Generates conventional commit message from change analysis" (CMD:66-69, 49) | Many changed files or mixed concerns, want a conventional message | When `.dev/tasks` staging must be exact: CMD says nothing about which files get staged (section 8, U1) |
| `--interactive` | boolean | off | "Guided merge with conflict resolution assistance" (CMD:75-76); only shown with `merge` | Merges with conflicts | Complex merges: CMD:91 says it will not handle merges needing manual intervention |

Does not exist in CMD (people might assume): `--depth`, `--dry-run`, `--amend`, `--no-verify`, `--all` or any path-selection flag, `--push`, `--approve`, any flag that sets staging scope. CMD only promises not to "modify repository configuration without explicit authorization" (CMD:89).

## 3. Scope x complexity matrix
The command does not vary by complexity: CMD has no complexity input, depth flag, or branching on task size. What varies is HOW OFTEN the commit step happens, and that is Ryan's pipeline rule ("commit regularly", brief ruling 5), not a file-defined threshold. So two matrices.

Matrix A: the command `/sc:git` itself. OPTIONAL everywhere, because plain `git` does the same (HWW:272; CVP line 163).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL | OPTIONAL | OPTIONAL |
| B bug fix | OPTIONAL | OPTIONAL | OPTIONAL |
| S single story | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J: more files, more message value) |
| F multi-story feature | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J) |
| R multi-feature release | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J) |
| N new product | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J) |

Matrix B: the COMMIT STEP (by any means) and its expected cadence. Floor is "at least one commit before push" in every scope that changes files (CVP lines 252-253 list "commit" as a step; HWW:198 "Commit locally"). Everything above the floor is JUDGMENT unless cited.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T | REQUIRED, 1 commit | REQUIRED, 1 commit | n/a (T is by definition small; HWW:22 sends >5 edits or >1 source file to a written plan) |
| B | REQUIRED, 1 commit | REQUIRED, 1 commit; separate commit for the failing test (J) | REQUIRED, commit before risky edits (J), then per fix |
| S | REQUIRED, 1 commit | REQUIRED, 1 commit per ledger milestone (J) | REQUIRED, per phase of the task file (HWW:83 "Commit each phase once it passes") |
| F | REQUIRED, per phase (HWW:83; CVP line 255 "commit per phase") | same | same, plus commit before any `/sc:cleanup` or `/sc:improve` (HWW:163, 22) |
| R | REQUIRED, per phase of each feature (J extension of HWW:83 and CVP line 255) | same | same |
| N | REQUIRED, per phase (CVP line 257 "commit per phase") | same | same |

Band definitions for the commit step (signals from the brief):
- LOW: files nameable up front, 1 session, 1 subsystem, no driving spec, no secrets/permissions/paths. One commit is enough.
- MEDIUM: 2 to 5 files or 2 subsystems, or 1 to 2 sessions, spec exists. Commit at each natural checkpoint (J).
- HIGH: many files or subsystems, 3 or more sessions (so a `/task-builder` task file with phases, which is the HIGH signal in the brief), shared interfaces, risk areas, or drift sensitivity. Commit per phase, because `/task` does not commit (HWW:81) and the phase audit needs a commit reference (HWW:83).

## 4. Choose this or the neighbour
| Neighbour | Decision rule | Cite |
|---|---|---|
| Plain `git add` / `git commit` | Default for LOW. Use plain `git` whenever the staging set must be exact, in particular when `.dev/tasks` must be staged (REPO-CLAUDE "Development Practices"), because CMD does not define staging. | CMD:14, 49; REPO-CLAUDE |
| `/sc:git commit --smart-commit` | Use when the diff is large or mixed and you want a conventional message. Still stage by hand first (J). | CMD:35, 66-69 |
| `/sc:pr-submit` | Different phase: it opens the PR and runs the review monitor after you have committed and been approved to push. It does not replace the commit step. At L2 it leaves edits in the working tree with no commit. | `skills/sc-pr-submit-protocol/SKILL.md:194`; HWW:198-205 |
| `/sc:implement`, `/task` | Neither commits. `/sc:implement` lists "Auto-commit" under Will Not (`commands/sc/implement.md:131`); `/task` does not commit (HWW:81). So the commit after them is always a separate step the engineer (or `/sc:git`) takes. | as cited |

No complexity-based choice between `/sc:git` and plain `git` is stated anywhere on disk. Any rule beyond the table is JUDGMENT.

## 5. What a scheduled checker can see
Footprint of the command itself: none. CMD names no file it writes, no ledger, no frontmatter key (CMD:40-45 lists tools only; its Write use is for "commit message generation and documentation" with no path given). Transcript only. UNVERIFIED by observation.

What IS visible in git, whichever tool made the commit (so the checker should look at these, not at the command):

| Signal | Where | Notes |
|---|---|---|
| Commit count on the branch vs `origin/main` | `git log origin/main..HEAD` | Floor of 1 for any scope that changed files. Cadence checks (per phase) compare this count to the number of phases in the task file (J). |
| Conventional message style | commit subject | CMD:35 says it generates conventional messages. Recent commits in this repo already use `docs(planning):`, `feat(orca):`, `fix(orca):` (git log at session start), so style cannot tell `/sc:git` from plain `git` or from a human. |
| `Co-Authored-By` trailer | commit body | Comes from the session's attribution instruction, not from CMD. Does not prove `/sc:git` was used. |
| `.dev/tasks/**` in the commit tree | `git ls-tree`, `git diff --name-only` | REPO-CLAUDE says `.dev/tasks` is always staged and never left untracked. A checker can test "no untracked `.dev/tasks` path at push time" (`git status --porcelain`). |
| Commit between phases | `reflect_post` entry names a commit; HWW:83 tells the engineer to give "that one commit" and to commit each phase after it passes | A phase audit run with `--diff <sha>` implies a commit existed. |
| Package moved to `done/` | `.dev/tasks/done/<id>/` | `/sc:implement` moves the package at the end and implies no commit (`commands/sc/implement.md:65`); a later commit should contain the rename (J). |

Cadence evidence is timestamps and file groupings in commits. One commit holding every phase's files, for a multi-phase task file, is a signal of an uncommitted-until-the-end path (J), not proof of a skipped step.

## 6. Expected-step rule
- Never expect the command `/sc:git`; always expect the commit. Count a commit (any tool) as the expected step; absence of `/sc:git` is fine in every cell.
- Expected commits: T and B at least 1; S at least 1 (more if the task file has phases or the work spanned sessions, J); F, R, N at least 1 per task-file phase (HWW:83; CVP lines 255, 257). A single commit for a multi-phase F, R or N branch is a reportable deviation (J). No commit at all before `/sc:pr-submit` on a branch with code changes is a deviation in every scope.

## 7. Proposed changes to command-value-by-phase.md
**Resolution of the earlier open question (U12 in CVP line 296, and the note in line 163).** CMD is 91 lines and read in full. It contains no mention of `.dev/tasks`, no staging policy, no path rules, and no instruction to read `CLAUDE.md`. `--smart-commit` is defined only as "Analyze changes → generate conventional commit message" (CMD:49) and "Generates conventional commit message from change analysis" (CMD:68). So the command does NOT respect the rule by design; it is silent. The rule can only be followed if the agent applies the project `CLAUDE.md` that is already in its session context. Whether it does is UNVERIFIED (not observed). Also CMD's `add` operation (CMD:14) says nothing about `git add -A` versus named paths.

1. CVP line 163 (`/sc:git` row, Notes column)
   - Current: `Committing regularly is mandatory (Ryan, pipeline step 4); plain `git` does the same. Guide: "never push without approval". How `--smart-commit` treats `.dev/tasks` (which `CLAUDE.md` says must always be staged) is UNVERIFIED`
   - Proposed: `Committing regularly is mandatory (Ryan, pipeline step 4); the command is optional, plain `git` does the same. Cadence by scope: T/B/S-LOW one commit; S-MEDIUM and above and all of F/R/N one per task-file phase (/task does not commit). Resolved from the command file: it says nothing about `.dev/tasks` or staging, so it does not enforce the repo rule; stage `.dev/tasks` yourself (plain `git add .dev/tasks`) before committing. Guide: "never push without approval"; the command file does not say it asks before push`
2. CVP line 241 (O15 row)
   - Current: `Judgment. How `/sc:git` handles `.dev/tasks` staging is UNVERIFIED`
   - Proposed: `Judgment. `/sc:git` does not define staging (command file silent), so use plain `git` when staging must be exact`
3. CVP line 276 (footprint row listing `/sc:git`)
   - Current: `No file footprint stated anywhere I read. Only visible in a session transcript or PR comments: UNVERIFIED`
   - Proposed: split `/sc:git` out: `No file footprint (command file names none). The commit itself is visible in `git log`; the checker should count commits per phase, not the command. Conventional message style and the `Co-Authored-By` trailer do not identify `/sc:git``
4. CVP line 296 (U12)
   - Current: `Whether `/sc:git --smart-commit` respects the "always stage `.dev/tasks`" rule ... command body not read`
   - Proposed: mark RESOLVED: command file read in full; silent on staging; behaviour at run time still UNVERIFIED (see U1 here).
5. CVP line 256 (Release scenario row, "Fewest" column)
   - Current: `1. `/sc:reflect --mode post --diff <commit> --no-promote` on every phase of the release 2. `/code-review` on the full branch 3. `/sc:pr-submit --monitor 1``
   - Proposed: add the commit step, matching the other rows: `... 1. commit per phase 2. `/sc:reflect --mode post ...` on every phase 3. `/code-review` 4. `/sc:pr-submit --monitor 1``. The `/sc:git` column cell for R stays OPTIONAL; this is a cadence fix, not a re-rating of the command. Under the new multi-feature R definition the commit count is higher (per phase of each feature) (J).
6. CVP line 163 columns T..N: all six stay OPTIONAL (no change); the command does not vary by scope or complexity.

## 8. Unverified items
| # | Item | Why unverified | How to close |
|---|---|---|---|
| U1 | Whether a real `/sc:git commit --smart-commit` run stages `.dev/tasks` (or runs `git add -A`, or `git commit -a`, which skips untracked files) | CMD is silent; I did not run the command (brief rule) | Observe one run in a throwaway worktree with an untracked file under `.dev/tasks/`, then check `git status` |
| U2 | Whether `/sc:git push` asks for confirmation | CMD:89 guards only "destructive operations"; push is not labelled either way. HWW:229 says never push without approval | Same observation, or tighten CMD |
| U3 | Whether commit cadence thresholds beyond "per phase" hold (S-MEDIUM, B-HIGH) | Only Ryan's "commit regularly" and HWW:83 exist; the rest is marked (J) | Ryan to confirm |
| U4 | Where the `Co-Authored-By` trailer comes from for other engineers | It comes from this session's attribution instruction, not from CMD; other engineers' setups not read | Check a teammate's commits |
| U5 | Whether a `/sc:reflect --mode post` run leaves a path a checker can match to a commit | Only the `pre-` report path was seen in HWW; `post-` path not read | Read `reflect.md` or the nuance file for `/sc:reflect` |
| U6 | No protocol skill `sc-git-protocol` exists; whether one is planned | `ls` found none | Ask Ryan |
