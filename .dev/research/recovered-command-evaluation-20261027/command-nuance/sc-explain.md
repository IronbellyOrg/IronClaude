# /sc:explain: scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: `/home/coder/.claude/commands/sc/explain.md` (104 lines, cited as CMD), `/home/coder/.claude/HOW-WE-WORK.md` (cited as HWW). Backing protocol skill: none (see section 1).

## 1. Status and role
- Does: "Provide clear explanations of code, concepts, and system behavior with educational clarity" (CMD:3). Guide level 1, "Ask a question": "An answer. No files change." (HWW:15). Routing row `ask`, `changes_files` = `no` (HWW:303).
- Phase: none in the build pipeline. It is a side tool usable at any point; HWW lists it under "Investigate how something works" (HWW:145). Not retired. Standalone-invokable, and the guide names it directly (HWW:15, 303).
- **No backing protocol skill exists**: `/home/coder/.claude/skills/sc-explain-protocol/` is absent (checked with `ls`). The guide says commands with no skill "run from their own file, so no skill load is expected", naming `/sc:explain` (HWW:232). Overlaps: a plain-English question to Claude (same level, HWW:15), `/sc:analyze`, `/tech-research`, `/sc:document`. It does not refer to `/sc:task` or `/sc:tasklist` anywhere in CMD.
- **Checker rule up front**: guide level 1, changes no files. A checker should never expect it and never penalize it, unless a file says otherwise (none found). Details in sections 5 and 6.

## 2. Flags
Usage line: `/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]` (CMD:22). The command file defines no defaults for any flag. No flag in the file changes whether files are written.

| Flag / argument | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `[target]` | a file, concept or system name; examples: `authentication.js`, `react-hooks`, `microservices-system`, `jwt-authentication` (CMD:64, 72, 80, 87) | none stated | What gets analysed (Behavioral Flow step 1, CMD:27) | Always; without it the command has nothing to explain (inference, J) | n/a |
| `--level` | `basic`, `intermediate`, `advanced` (CMD:22) | not stated (UNVERIFIED) | Audience level and explanation depth (CMD:28, 54 "Progressive Learning"; examples CMD:64-66, 72-74, 80-81) | Onboarding someone new to a module (`basic`); a design walkthrough for a senior (`advanced`). Both J | Never harmful; picking the wrong level only changes wording |
| `--format` | `text`, `examples`, `interactive` (CMD:22) | not stated (UNVERIFIED) | Presentation shape: "Static content → examples → interactive exploration" (CMD:57). Only `interactive` appears in an example (CMD:80) | `examples` for a usage walkthrough (J) | `interactive`: the file never says what it does or whether it writes anything (UNVERIFIED), so do not rely on it producing a file |
| `--context` | `domain`, free word; the file shows `react` and `security` (CMD:72, 87) | not stated (UNVERIFIED) | `react` routes through Context7 for official docs (CMD:73, 42-43); `security` brings the Security persona (CMD:88, 44) | A framework or security question where official patterns matter | A question about this repo's own code; Context7 only serves library docs (CMD:42, J) |

Does not exist (absent from CMD and no protocol skill to define them; people may assume them):

| Flag | Where people might expect it |
|---|---|
| `--depth` (any value) | exists on `/sc:workflow`, `/sc:troubleshoot`, `/sc:research`; not on `/sc:explain`. Depth here is `--level`. |
| `--output` / `--save` / any output path | the file defines no output location at all |
| `--spec`, `--fix`, `--no-promote`, `--monitor`, `--handoff` | belong to other commands |

Frontmatter note: `complexity: standard` (CMD:5) is a label on the command file, not task-builder's TCS score and not a flag. Do not use it as a complexity signal for a task. There is no `allowed-tools` key (CMD:1-8), so "changes no files" is stated in the guide (HWW:15) and implied by the tool list (CMD:48-50: Read/Grep/Glob, TodoWrite, Task), not enforced by a tool allowlist.

## 3. Scope x complexity matrix
**It does not vary by scope or complexity.** Its triggers (CMD:12-17) are about understanding something, not about the size of the job, and the guide places it at level 1, outside the scope ladder (HWW:15). No file gives a complexity threshold for it, and the only complexity-like input is the audience `--level` (CMD:28), which is about the reader, not the task. So every cell is the same. Nothing here is REQUIRED or WORTH IT in any cell, and no cell makes absence a miss.

Complexity bands (one line each, all J since no file defines them for this command):
- LOW: one file or one concept; a plain question to Claude does the same job.
- MEDIUM: several files, named up front; the engineer wants a walkthrough before editing.
- HIGH: unfamiliar subsystem, no named files, shared interfaces; orientation is more valuable but `/tech-research` is the better tool if the answer must be kept or acted on (see section 4).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| B bug fix | OPTIONAL (J), orientation before `/sc:troubleshoot` | OPTIONAL (J) | OPTIONAL (J) |
| S single story | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| F multi-story feature | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| R multi-feature release | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| N new product | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |

Flag set in every cell: none needed. `--level` / `--context` only tune the wording (section 2).
R under the new definition: no change in substance. The command has no release role in any file; the existing R cell was SKIP, and the only change proposed is the same SKIP to OPTIONAL as for S/F/N (section 7).

## 4. Choose this or the neighbour
None of these is a pipeline step that `/sc:explain` stands in for. The rules below are about picking the right side tool, not about a pipeline choice.

| Neighbour | Use `/sc:explain` (or a plain question) when | Use the neighbour when | Cited |
|---|---|---|---|
| Plain-English question to Claude | You name a file or concept and want it explained. Equivalent at level 1 | n/a: the guide gives both as the same level-1 route ("Ask Claude in plain English. For an explanation of specific code, `/sc:explain ...`") | HWW:15, 303 |
| `/sc:analyze <path> --focus ...` | You want to understand what code does | You want a health verdict on a module (security, quality, performance, architecture). Reports only | HWW:144-145 |
| `/tech-research "<question, why, code>"` | The answer is for you now, nothing needs saving, and you can name the code | The system is not understood yet, files are unknown, the idea needs feasibility or options, or the answer must be kept: it writes `RESEARCH-REPORT-<topic>.md` and feeds `/task-builder` (level 5, the better fit at HIGH complexity) | HWW:19, 142, 308 |
| `/sc:research "<q>" --depth deep` | The subject is code in this repo | The subject is outside the repo: a library, standard, best practice (searches the web) | HWW:143, 247, 312 |
| `/sc:document <path> --type api` | You only need to read an explanation | You need reference text written into the repo; it changes files | HWW:184, 246, 320 |
| `/tech-reference` | Same as above | You need a reviewed architecture document for a built feature | HWW:181, 246 |
| `bmad-document-project` (BMad) | Not comparable: existence only; its behaviour was not read here (UNVERIFIED) | | command-value-by-phase.md:38 |

Complexity rule, one line: LOW or MEDIUM and files already named, ask or `/sc:explain`; HIGH or files not named or an answer that must persist, `/tech-research` (J, built from the level 1 and level 5 rows at HWW:15, 19).

## 5. What a scheduled checker can see
**On disk: none.** No path, frontmatter key or ledger line is defined anywhere in CMD: it names no output file, no folder, no report and no state file (CMD:1-104, read in full). The guide says no files change (HWW:15) and lists `changes_files: no` (HWW:303). `TodoWrite` (CMD:49) is session-internal progress tracking; the file does not say it persists anything to the repo (UNVERIFIED).

**Transcript only.** The only trace is the slash command line or its tool calls in the session log. Session logs exist under `/home/coder/.claude/projects/<project>/` (directory observed while searching; contents not read for this analysis). Whether the scheduled checker can read them is UNVERIFIED.

Consequence: a checker that looks only at the repo cannot tell whether `/sc:explain` ran. That is fine, because it is never an expected step (section 6).

## 6. Expected-step rule
- **Never expected, at any scope or complexity (T, B, S, F, R, N; LOW, MEDIUM, HIGH).** Its absence is never a skipped step. Its presence is never a deviation either: it changes no files (HWW:15), so running it cannot break the pipeline, and a checker must not penalize it or any engineer who uses it.
- **Never count it as a stand-in for a pipeline check.** Its own "Validate" step (CMD:31) checks the accuracy of the explanation, not the work product, so it does not satisfy review, validation, spec-panel, `/sc:reflect`, `/code-review` or `/sc:analyze` for any scope.

## 7. Proposed changes to command-value-by-phase.md
Proposals only; `command-value-by-phase.md` was not edited.

**P1. Row `/sc:explain` (line 178, section 2.6).**
- Current: `| /sc:explain | Provide clear explanations ... | OPTIONAL | OPTIONAL | SKIP | SKIP | SKIP | SKIP | Guide level 1: understanding, no files change |`
- Proposed: `| /sc:explain | Provide clear explanations ... | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | Guide level 1: understanding, no files change (HOW-WE-WORK:15, 303). Not tied to a phase or scope; no backing protocol skill. Never expected by a checker and never penalized: no on-disk footprint. Flags: --level, --format, --context only; no --depth |`
- Why: a SKIP reads as "do not use", but no file says that; the guide puts level 1 outside the scope ladder, and CMD:12-17 triggers do not depend on scope. SKIP also gives a checker a reason to treat use as odd. The T/B OPTIONAL cells stay as they are.
- R re-rating: R was SKIP. Under the multi-feature release definition nothing changes in substance (no release role in any file); it moves to OPTIONAL only by the consistency argument above.

**P2. Section 2 "Rating rules" (after line 51).** Add one line: "Commands that change no files and have no on-disk footprint (for example `/sc:explain`) are never expected steps for a checker; absence is never a miss and use is never a deviation, at any scope or complexity."

**P3. Section 2.6 phase placement.** The row sits under "Bug fix / Troubleshoot" only because it needs a home. Add to the row Notes or section intro: "side tool, usable in any phase (HWW:145)".

## 8. Unverified items
1. Defaults of `--level`, `--format`, `--context`: CMD gives none; no protocol skill exists to define them.
2. Allowed values of `--context`: CMD says `domain` and shows only `react` and `security` (CMD:22, 72, 87).
3. What `--format interactive` does and whether it ever writes anything: CMD says only "interactive exploration" (CMD:57, 80).
4. Whether any run of the command writes a file: no instruction in CMD says so, but there is no `allowed-tools` key (CMD:1-8) and `Task` delegation is listed (CMD:50). "No files change" rests on the guide (HWW:15), not on enforcement.
5. Whether `TodoWrite` output persists outside the session (CMD:49).
6. Whether persona auto-activation (educator, architect, security; CMD:7, 44, 97) is defined in any file; persona definitions were not read.
7. The "established explanation validation or educational quality requirements" in CMD:104 are not defined in any file read.
8. Whether the scheduled checker can read session logs under `/home/coder/.claude/projects/` (section 5).
9. Whether other engineers' `~/.claude/commands/sc/explain.md` and `HOW-WE-WORK.md` match the copies read here.
10. `bmad-document-project` behaviour (section 4 row) was not read.
