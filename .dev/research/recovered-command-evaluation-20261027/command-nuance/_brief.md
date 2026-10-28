# Shared brief for the per-command nuance agents

Written 2026-10-27 from Ryan's instructions. Every agent reads this first. Single source of truth: do not copy it into your output.

## Why this exists

`command-value-by-phase.md` (same parent folder) rates each command per phase and per scope (T one-off, B bug fix, S single story, F multi-story feature, R release, N new product). Ryan's verdict: it is missing a layer of nuance for the COMPLEXITY of the task, layered on top of scope. Example: when to use `/task-builder` on a single story versus `/sc:workflow`. The output feeds a brainstorm about a scheduled job that checks whether engineers followed the right pipeline steps. That job must not flag a legitimate short path as a skipped step, so it needs to know, per command, when the command is expected and when skipping is fine.

## Rulings from Ryan (treat as fixed)

1. Location: BMad commands are in the repo; `sc:*`, `/task-builder`, `/task`, `/prd`, `/tdd`, `/roadmap` and the rest live in each engineer's home directory (`~/.claude`).
2. "Release" (the R scope) means a MULTI-FEATURE release: a full release plan, implementation and push. It is one step below greenfield new-product development (N). A single feature's release is just a phase inside S or F, not R. The existing R column in `command-value-by-phase.md` may have been rated under a different reading: re-rate R under this definition and say where it changed.
3. `/sc:task` and `/sc:tasklist` are RETIRED. They must not be invoked on their own, only possibly inside other skills (the one programmatic caller found is `/sc:tasklist` Stage 9 calling `/sc:task`). Never recommend either as a step an engineer runs. If your command refers to them, say so.
4. Validated already (read these, do not redo them):
   - `validation-feature-task-builder-vs-sc-workflow.md`: `/task-builder` + `/task` is the minimum tasklist step for a multi-story feature; `/sc:workflow` + `/sc:implement` is not eligible as that minimum. Differentiators: research, spec trace (`--spec`, `reflect_pre`), review depth. Not multi-session resume (both resume).
   - `validation-oneoff-sc-task-vs-sc-implement.md`: `/sc:implement` has NO `--depth` flag (`--depth quick` belongs to `/sc:workflow`). Proposed one-off minimum: a plain edit plus the related test, with `/sc:implement "<prompt>"` as an optional step that leaves a ledger. This one-off minimum is PROPOSED and not yet confirmed by Ryan: say "proposed" wherever you rely on it.
5. Pipelines (Ryan): spec (brainstorm, design, spec-panel or BMad equivalents); tasklist (`/sc:workflow` or `/task-builder`) then review/revise, validate; implement (`/sc:implement` or `/task`); commit regularly and push with `/sc:pr-submit`; bugs and issues via `/sc:troubleshoot`. Not every command runs every time.

## The two axes

- SCOPE: T, B, S, F, R (as redefined above), N.
- COMPLEXITY (new layer): how hard the work is inside a given scope. Use only signals that appear in files on disk, and cite them: number of files or subsystems touched, expected sessions, whether the author can name the files up front, whether a driving spec exists, risk (secrets, permissions, user input, paths, infrastructure), drift sensitivity ("must not drift"), need for research, shared interfaces between stories. The only on-disk formula is task-builder's TCS (`~/.claude/skills/task-builder/SKILL.md` around lines 2410-2441; quick <=12, standard 13-34, deep >=35). `~/.claude/HOW-WE-WORK.md` levels 1-6 and its routing table (lines 9-22, 168, 191-194, 243, 304-307) give the rest. Where no file gives a threshold, you may propose one but label it JUDGMENT. Do not invent numbers and call them facts.
- Use three complexity bands per scope: LOW, MEDIUM, HIGH. Define each band with the signals above in one line per band for your command. If the command does not vary by complexity, say so plainly instead of inventing variation.

## What each agent produces (one file per command)

Your output file: `/home/coder/workspaces/worktrees/Coder/IB-CPlus-01/_bmad-output/brainstorming/brainstorm-clay-feedback-decisions-2026-10-26/command-nuance/<slug>.md` where `<slug>` is given in your prompt.

Create a header stub first, then append section by section. Do not write the file in one go from memory. Sections:

1. **Status and role** (3 lines max): what the command does in one sentence taken from its own file, which phase(s) it serves, whether it is retired or standalone-invokable, which neighbouring commands overlap it.
2. **Flags**: a table of EVERY optional flag and argument found in the command file and its backing protocol skill (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/sc-<name>-protocol/`). Columns: flag, values, default, what it changes (cited), when worth using, when to avoid. Flags banned or absent that people might assume exist (for example `--depth` on `/sc:implement`) go in a short "does not exist" list.
3. **Scope x complexity matrix**: rows T, B, S, F, R, N; columns LOW, MEDIUM, HIGH. Each cell is one of REQUIRED / WORTH IT / OPTIONAL / SKIP / N/A plus, where it matters, the flag set to use (for example `--depth quick`). Mark any cell that is your judgment, not a file's statement, with `(J)`.
4. **Choose this or the neighbour**: for each overlapping command, a short decision rule by complexity signals (for example `/sc:workflow` vs `/task-builder` on a single story). Cite files.
5. **What a scheduled checker can see**: the footprint on disk (paths, frontmatter keys, ledger lines) or "none, transcript only". Cite files; mark UNVERIFIED if unobserved.
6. **Expected-step rule**: one or two lines saying when a checker should count this command as expected, and when its absence is fine, by scope x complexity.
7. **Proposed changes to command-value-by-phase.md**: specific rows or cells (give the current text and the proposed text), including any R re-rating under the new definition. Proposals only; do not edit that file.
8. **Unverified items**.

## Rules for every agent

- Read-only analysis. Do not run the command you are describing or any other sc: command. Only read files.
- Read the command file and its backing protocol skill and refs in full before writing. Cite `path:line` for every factual claim. Anything not confirmed from a file is UNVERIFIED. If a flag is mentioned in one file but not defined in another, say so.
- Do not edit `command-value-by-phase.md`, the two validation files, `epics-micro-first.md`, or any file other than your own output file. A separate merge step will fold your file into the main file.
- Do not design epics or stories. Do not write secrets. Do not read or print environment variable values.
- Keep each section tight. Tables over prose. No filler.
- When finished, reply with only your output file path and a one-line status (include the number of unverified items).
