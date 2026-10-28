# /sc:analyze: scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: `/home/coder/.claude/commands/sc/analyze.md` (111 lines, cited as CMD). Backing protocol skill `/home/coder/.claude/skills/sc-analyze-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"; no skill dir in `~/.claude/skills/` matches `analy`). So CMD is the only definition. Neighbour and caller files cited by path.
Marker `(J)` = judgment, not a file statement.

## 1. Status and role
- What it does: "Comprehensive code analysis across quality, security, performance, and architecture domains" (CMD:3, 10). Static only, reports only, changes nothing (CMD:99-100; HOW-WE-WORK.md:144). Frontmatter `category: utility`, `complexity: basic` (CMD:4-5); it names no skill and no agents (CMD:6-7, 40-46), so it runs from its own file (HOW-WE-WORK.md:232).
- Phase: standalone health check of existing code, no symptom, no spec, no diff (troubleshoot.md:209; reflect.md:310). Standalone-invokable, NOT retired (HOW-WE-WORK.md:144, 313). CMD does not mention `/sc:task` or `/sc:tasklist`.
- Overlaps: `/sc:troubleshoot` (has a symptom), `/sc:reflect` (has a spec or diff), `/tech-research`, `/sc:explain`, `/sc:cleanup-audit`, `/code-review`, `/security-review`. Also called by other protocols: `/sc:brainstorm` Wave 2A (sc-brainstorm-protocol/SKILL.md:183) and `/sc:release-split` Part 4 (release-split.md:137; sc-release-split-protocol/SKILL.md:106, 324).

## 2. Flags
Usage line, the only flag definition anywhere: `/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]` (CMD:22). No protocol skill, so nothing else defines semantics. Every default and every depth meaning below is example-implied only.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[target]` | path (file or directory) | Whole project: bare `/sc:analyze` = "multi-domain analysis of entire project" (CMD:60-63). Default is inferred from the example, never stated | Narrows the file discovery step (CMD:27). Path syntax (glob, several paths) not defined: UNVERIFIED | Always. Name the subsystem. HOW-WE-WORK routing row takes `<path>` (HOW-WE-WORK.md:313) | Bare whole-project run: one context, no agent fan-out in CMD:40-46, so coverage of a large repo is unmeasured (J) |
| `--focus` | `quality`, `security`, `performance`, `architecture`: one value per usage line | Omitted = all four domains (inferred from CMD:60-62; not stated) | Selects the domain-specific technique (CMD:50, 66-68, 84). Combining values (`a,b`) is not defined: UNVERIFIED | Always pass one. The team guide makes it a mandatory flag for the module-health row: `1: --focus <area>` (HOW-WE-WORK.md:313) even though CMD marks it optional | Omitting it on a target of more than one subsystem: a diluted pass across four domains |
| `--depth` | `quick`, `deep` ONLY | Not stated | Only by example: `quick` = "rapid assessment ... code smells and maintainability issues" (CMD:84-86); `deep` = "vulnerability assessment with detailed remediation guidance" (CMD:68-71). What work each does is not defined: UNVERIFIED. Callers use `quick`: `--focus quality --depth quick` (sc-brainstorm-protocol/SKILL.md:183). Observed `deep` use: `--focus architecture --depth deep` (.dev/reviews/orca-catalogue-bundle-20260924/01-template-analyze.md:3) | `quick` for one subsystem or a context scan; `deep` for risk areas (auth, secrets, infra) or cross-subsystem architecture | `deep` on a whole-project, all-domain run (cost unknown; J) |
| `--format` | `text`, `json`, `report` | Not stated | Output shape only. `report` is described as "Generates HTML report" (CMD:76-78) while the Output list says "Analysis report" (CMD:103-109): the two do not say the same thing. Where a file is written is not stated, although Write is listed (CMD:46) | `text` for chat reading. `report`/`json` only when someone will keep or parse the file: no consumer found on disk (grep of `~/.claude/commands`, `~/.claude/skills`) | `json` with no parser; a checker cannot rely on any of the three producing a file at a fixed path |

Does NOT exist in CMD (people may assume them):
- `--depth standard` (that value exists on `/sc:troubleshoot`, HOW-WE-WORK.md:125, and `/sc:workflow`; analyze takes only `quick|deep`, CMD:22).
- `--fix`, `--apply`, `--safe`, `--interactive` (analyze must not modify code, CMD:100; `--safe --interactive` belong to `/sc:cleanup` and `/sc:improve`, HOW-WE-WORK.md:164-165).
- `--spec`, `--diff`, `--tasklist`, `--mode` (reflect flags, HOW-WE-WORK.md:309-322; analyze has no spec or diff concept).
- `--type`, `--output`, `--handoff`, `--monitor`, `--no-post-pr`, `--coverage`.
- Comma-listed `--focus`, a `--depth` default, and an output-path flag: not defined.

## 3. Scope x complexity matrix
Does it vary by complexity? Only in HOW MUCH to point it at, not WHETHER it is a pipeline step. No file makes it required anywhere: HOW-WE-WORK lists it once as an answer to "general health of a module" (HOW-WE-WORK.md:144) and once as a routing row with `changes_files: no` (HOW-WE-WORK.md:313); the callers treat it as optional enrichment (sc-brainstorm-protocol/SKILL.md:183 gives `OR mcp__auggie__codebase-retrieval`; sc-release-split-protocol/SKILL.md:324 gives `or inline verification`).

Band definitions, all (J). The band describes the TARGET being analyzed, not the story. No file gives a threshold for `/sc:analyze`. TCS (task-builder/SKILL.md:2410-2433) sizes a task file for `/sc:reflect --depth` and does NOT apply to analyze; only its counting rule is borrowed here: S1 = distinct files, S2 = distinct subsystems = first 2 path segments (task-builder/SKILL.md:2410-2411). Risk classes: login, permissions, secrets, user input, file paths (HOW-WE-WORK.md:200); this repo adds env/secret paths (CLAUDE.md "Secrets discipline").

| Band | Signals (J) | Flag set (J) |
|---|---|---|
| LOW | Target is 1 subsystem key (S2 = 1), author can name the path up front, no risk class | `<path> --focus <one> --depth quick` |
| MEDIUM | Target spans 2-3 subsystem keys, OR author cannot name the files up front, OR exactly 1 risk class | `<path> --focus <one> --depth quick` first; `--depth deep` only on the subsystem the quick pass flags; one run per `--focus` |
| HIGH | 4+ subsystem keys, OR shared interfaces between stories or features, OR 2+ risk classes, OR infrastructure | `--depth deep`, one run per `--focus` domain per subsystem group. Never one bare whole-project run |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J). Level 2: one file plus test, change already known (HOW-WE-WORK.md:16, 22); nothing to assess | SKIP (J) | SKIP (J). A risky one-off wants `/security-review` on the diff (HOW-WE-WORK.md:200), not a module health pass |
| B bug fix | SKIP (J). A symptom exists, so `/sc:troubleshoot` (HOW-WE-WORK.md:123-125; troubleshoot.md:209) | SKIP (J) | OPTIONAL (J), after the fix: `<cited path> --focus <domain REPORT.md names> --depth quick`, only if REPORT.md says the cause is a module-wide pattern. Not a bug finder |
| S single story | SKIP (J) | SKIP (J). The context question is `/tech-research` (HOW-WE-WORK.md:95-96, 142) | OPTIONAL (J): `<path> --focus <risk domain> --depth quick` before the story when it touches a risk class in code nobody on the story knows |
| F multi-story feature | SKIP (J) | OPTIONAL (J): `<path> --focus architecture --depth quick` before the spec | WORTH IT (J): `--focus architecture --depth deep` per shared subsystem before `/task-builder --spec`, when `/tech-research` was not run. Observed: `/sc:analyze templates/VSCode-AIDev02 --focus architecture --depth deep` for a feature spec (.dev/reviews/orca-catalogue-bundle-20260924/01-template-analyze.md:3) |
| R multi-feature release (re-rated) | OPTIONAL (J): `--focus architecture --depth quick` on the shared code before release planning | WORTH IT (J): one `--focus architecture` run and one `--focus security` run, `--depth quick`, before the release plan | WORTH IT (J): `--depth deep`; `architecture` per shared subsystem before the plan, `security` on every risk-class subsystem before push. Never REQUIRED: output feeds no downstream step |
| N new product | N/A (J). Greenfield: no code to analyze | SKIP (J). Spec exists, so drift is `/sc:reflect`'s job (reflect.md:310) | OPTIONAL (J): at a milestone, once code exists, `--focus security|performance --depth quick` (domains with no spec); or at the start when the product is built on an existing codebase being ported or replaced |

Where it is useful in R and N (J): R is the first scope with several features sharing subsystems, so a per-domain health read of the shared code before planning and of risk subsystems before push is the cheapest use. N is mostly SKIP because the first useful moment is after code exists, and then a spec exists too.

## 4. Choose this or the neighbour
| Neighbour | Rule | Source |
|---|---|---|
| `/sc:troubleshoot` | Have a symptom, error or failing test: troubleshoot. No symptom yet: analyze | troubleshoot.md:209; HOW-WE-WORK.md:123-125, 144 |
| `/sc:reflect` | Have a spec, tasklist or diff to compare against: reflect. None of those: analyze | reflect.md:310 |
| `/tech-research` | Question is "how does it work, is it feasible, what must change" and the answer should be options plus a plan: tech-research. Question is "how healthy is this module" with severity-rated findings: analyze. Tech-research runs at its deepest setting by default (HOW-WE-WORK.md:255); analyze's cost is UNVERIFIED | HOW-WE-WORK.md:95-96, 142, 144, 308 |
| `/sc:explain` | Understand what specific code does: explain. Assess its health: analyze | HOW-WE-WORK.md:145 |
| `/sc:cleanup-audit` | Looking for dead code, duplication, files to delete or merge: cleanup-audit (evidence-backed passes). CONFLICT: CMD:111 names `/sc:improve` or `/sc:cleanup` as the next step, while the cleanup routing row starts with `/sc:cleanup-audit` (HOW-WE-WORK.md:318). Follow the routing row | CMD:111; HOW-WE-WORK.md:160-161, 318 |
| `/code-review`, `/security-review`, `/sc:auggie-review` | Review of a pending diff or branch: those. Analyze takes a path, not a diff (CMD:22); it does not review changes | HOW-WE-WORK.md:199-201, 322-323 |
| `/sc:improve`, `/sc:cleanup` | Apply fixes: those. Analyze never modifies code without explicit consent (CMD:100). Commit first, review `git diff` after (HOW-WE-WORK.md:22) | CMD:111 |
| `/sc:brainstorm` (caller) | Wave 2A auto-runs `/sc:analyze <paths> --focus quality --depth quick` when domain is code, architecture or incident and `--no-codebase` is absent, OR auggie retrieval. Not an engineer step | sc-brainstorm-protocol/SKILL.md:183 |
| `/sc:release-split` (caller) | Part 4 "fidelity verification" delegates to `sc:analyze` OR inline verification. MISMATCH: CMD defines no comparison of an output against a source artifact (CMD:93-95), only code analysis in four domains. Do not read this caller as proof analyze checks fidelity | release-split.md:137; sc-release-split-protocol/SKILL.md:106, 324 |
| `/sc:task`, `/sc:tasklist` (retired) | Not referenced by CMD, nor required by it | CMD (whole file) |

## 5. What a scheduled checker can see
Footprint defined by the command: NONE. CMD lists Write for "report generation" (CMD:46) but gives no path, no frontmatter keys, no ledger and no return contract. The routing row only says a report may land under `.dev/`, `claudedocs/` or the tool's own output folder (HOW-WE-WORK.md:297). No `.dev/analyze*` directory exists in this repo (checked `.dev/analysis`, `.dev/analyze`).

Footprints seen in this repo (engineer-placed, not command-defined; all show a past run, none is a rule):
- `.dev/reviews/orca-catalogue-bundle-20260924/01-template-analyze.md`: report whose line 3 quotes the full command line with flags. A checker can grep a doc for the literal `/sc:analyze ... --focus ... --depth ...` string.
- `.dev/tasks/done/TASK-RF-20260521-033055/TASK-RF-20260521-033055.md:63, 96, 113` and `phase-outputs/discovery/advanced-deletion-rationale.md`: a decision transcribed from "a `/sc:analyze` 3-agent fan-out".
- `.dev/reviews/pr177-t51-leak-scan-20260919/context.md:35`: "All five agents invoked sc:analyze". Prose only.
- Via brainstorm: `enrichment/codebase-context.md` inside the brainstorm folder (sc-brainstorm-protocol/SKILL.md:183; folder `.dev/brainstorms/<timestamp>-<name>/`, HOW-WE-WORK.md:53). It may instead come from `mcp__auggie__codebase-retrieval`, so its presence does not prove analyze ran.

Verdict: transcript only (the `sc:analyze` skill call in the session log: UNVERIFIED, not observed). Any report file is optional and at an unpredictable path.

## 6. Expected-step rule
- A checker must NEVER count `/sc:analyze` as an expected step in any scope x complexity cell, including R and N: no file requires it and nothing downstream consumes its output. Its absence is always fine.
- If it does appear (F HIGH, R MEDIUM/HIGH are the likeliest), treat it as an extra. Do NOT let it satisfy a review step (`/code-review`, `/sc:auggie-review`), a validate step, or a spec-trace step (`/sc:reflect`): it reviews no diff and compares nothing to a spec (CMD:22, 93-101).

## 7. Proposed changes to command-value-by-phase.md
Proposals only; `command-value-by-phase.md` not edited.

1. Section 2.6 row `/sc:analyze` (line 177), ratings T B S F R N.
   - Current: `SKIP | OPTIONAL | SKIP | OPTIONAL | OPTIONAL | SKIP`
   - Proposed: `SKIP | OPTIONAL | SKIP | OPTIONAL | WORTH IT | SKIP`. Only R changes (re-rated under the multi-feature release definition, ruling 2): OPTIONAL becomes WORTH IT (J) at MEDIUM and HIGH complexity, OPTIONAL at LOW. Reason: R is the first scope with several features sharing subsystems. Still never REQUIRED.
   - Other columns keep their label, with conditions: B only at HIGH after a fix (J); S SKIP, OPTIONAL only at HIGH (J); F WORTH IT only at HIGH when no `/tech-research` ran (J); N SKIP, OPTIONAL at HIGH once code exists (J).
2. Same row, Notes cell.
   - Current: `Reports only, changes nothing. Module health check, not a bug finder. Next step per its file: /sc:improve or /sc:cleanup`
   - Proposed: `Reports only, changes nothing. Module health check, not a bug finder: use it when there is no symptom (troubleshoot.md:209), no spec and no diff (reflect.md:310). Flags: [target] --focus quality|security|performance|architecture (one value; the guide's routing row makes it mandatory) --depth quick|deep ONLY (no standard) --format text|json|report. No protocol skill exists; defaults and depth meaning are not defined. Output path undefined, so a checker sees transcript only. Never an expected step. Next step per its file is /sc:improve or /sc:cleanup, but the guide's cleanup route starts with /sc:cleanup-audit.`
3. Section 2.x row O9 (line 235).
   - Current: `/sc:troubleshoot, bmad-investigate, /sc:analyze` ... `/sc:analyze is health, not bugs`
   - Proposed: drop `/sc:analyze` from the O9 "Diagnose a bug" command list; it has no symptom input. Keep the health-not-bugs note on the 2.6 row only. (Low priority.)
4. Method line 4 (`/sc:analyze skill invoked and followed ... It ran normally`): no change; but note no `sc-analyze-protocol` skill backs it, so "followed" means CMD only.
5. Cross-file note for the merge step: the `/sc:release-split` row should say its Part 4 "deep fidelity verification via /sc:analyze" is not backed by CMD (CMD defines no source-versus-output comparison) and that `inline verification` is the file's own alternative (sc-release-split-protocol/SKILL.md:324).

## 8. Unverified items
1. Default `--depth`: not stated in CMD or any file read.
2. Default `--format`, and whether `report` writes HTML (CMD:76-78) or something else (CMD:103-109 says "Analysis report"). Where any file is written: not stated.
3. What `quick` versus `deep` actually change in work done, cost, or time: only example text (CMD:68-71, 84-86). No measurement.
4. Whether `--focus` accepts several values, and whether `[target]` accepts globs or several paths.
5. Whether omitting `--focus` runs all four domains (inferred from CMD:60-62 only).
6. Whether a bare whole-project run on a large repo degrades coverage (no agent fan-out in CMD:40-46; coverage never measured). Observed fan-outs of 3 and 5 agents were set up by the engineer, not by CMD (TASK-RF-20260521-033055.md:63; pr177 context.md:35).
7. Tension inside CMD: Bash is listed for "external analysis tool execution" (CMD:45) while dynamic analysis requiring compilation or runtime is excluded (CMD:99). Which external tools may run is not stated.
8. Whether a session transcript records the `sc:analyze` Skill call in a form a scheduled job can read: not observed.
9. The band thresholds in section 3 (S2 = 1, 2-3, 4+, risk-class counts) are my judgment; no file gives any for this command. TCS (task-builder/SKILL.md:2410-2433) governs `/sc:reflect --depth`, not analyze.
10. Cost of analyze versus `/tech-research`: not stated in either file read.
11. Whether the T, B, S, N cells that are SKIP/N/A should be left unrated by a checker rather than SKIP: left to the merge step.
