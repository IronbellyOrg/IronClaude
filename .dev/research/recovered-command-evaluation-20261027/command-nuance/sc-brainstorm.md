# /sc:brainstorm: scope x complexity nuance

**Generated**: 2026-10-27 by the sc-brainstorm nuance agent (read-only analysis; only this file written)
**Brief**: `command-nuance/_brief.md` (rulings 1-5 apply; the one-off minimum is PROPOSED, not confirmed)
**Read in full**: `~/.claude/commands/sc/brainstorm.md` (201 lines, cited `cmd:N`), `~/.claude/skills/sc-brainstorm-protocol/SKILL.md` (424, `SKILL:N`), and its refs `agent-spec-builder.md` (`asb:N`), `handoff-routing.md` (`hr:N`), `socratic-templates.md` (`st:N`). Also read in full: `~/.claude/HOW-WE-WORK.md` (`HWW:N`), the BMad skill `.agents/skills/bmad-brainstorming/` SKILL.md, `customize.toml`, `references/finalize.md`, `references/headless.md` (`bmad:`). Only grepped, not read in full: `sc-adversarial-protocol/SKILL.md` (`adv:N`, pass-through flags and depth rounds only), `task-builder/SKILL.md` (flags and TCS section), `sc-release-split-protocol/SKILL.md`. Observed on disk: 11 run folders under `/home/coder/workspaces/Coder/.dev/brainstorms/` and 2 under `_bmad-output/brainstorming/`.
**Rule**: nothing here was run. Anything not confirmed from a file is marked UNVERIFIED. `(J)` = my judgment, no file states it.

## 1. Status and role

- **Does**: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge" (`cmd:3`). It produces a requirements spec (`merged-requirements.md`) and stops; it writes no code and never auto-runs `/sc:design` (`cmd:179-187`, `SKILL:413-418`). Phase: Spec, idea shaping.
- **Status**: NOT retired. Standalone-invokable by the engineer (`cmd:25-29`); its protocol skill is never run directly (`SKILL:23-30`). It is also called programmatically by `/sc:release-split` Part 1 (`sc-release-split-protocol/SKILL.md:103,149,161`).
- **Overlaps**: `bmad-brainstorming` (the lane twin), `/tech-research` (when the unknown is facts about our code), `/sc:adversarial` (when drafts already exist), `/sc:design`, `/prd`. Retired `/sc:tasklist` is still named in its `--handoff tasklist` and in its "Next:" text (`cmd:174,199`, `SKILL:315-318`): never use it.

## 2. Flags

Source: option table `cmd:45-64`, interactions `cmd:66-71`. The protocol's `argument-hint` lists only `--proposals --depth --strategy --handoff --output` (`SKILL:5`); the other flags exist in the command file only, and all arguments are passed through to the protocol (`SKILL:27-28`). Short forms `-p -d -s -i -o` appear only in `cmd:46-61`.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `<topic>` | free text or `@file` | required; empty STOPs (`cmd:29`, `SKILL:70`) | Becomes the seed brief's `topic`, and drives domain and strategy auto-detection (`st:5-32`) | Always. Give who it is for, the outcome, the main constraint (`HWW:30,310`) | A one-word topic: auto-detection then guesses the domain |
| `--proposals N` (`-p`) | 2-7 | 3 | Number of parallel variants. Clamped silently: quick max 2, standard max 5, deep max 7 (`SKILL:96-100`; the command file states only the quick and deep caps, `cmd:68-70`). At exactly 2, per-persona instructions are dropped (`asb:101`) | 3 (default) for most work. 4-5 at deep when approaches truly differ | 7 at deep: by the formula in `asb:146-152` with the code-domain personas the estimate is about 276K tokens, over the 250K trigger, so it auto-downgrades to 3 (derived arithmetic, not observed). 1 is invalid (below the 2 floor) |
| `--depth` (`-d`) | `quick`, `standard`, `deep` | `standard` | Socratic question count 3-5 / 6-10 / 10-20 (`SKILL:131-133`); proposal cap (above); token estimate per proposal 8K / 15K / 35K (`SKILL:237`); passed to adversarial where `--depth` sets debate rounds 1 / 2 / 3 (`adv:334`): quick skips Round 2 and 2.5 (`adv:1083,1112`), Round 3 runs only at deep and only below the convergence threshold (`adv:1361`). At deep the first two personas run on opus (`asb:63`) | `standard` is the guide's default and "need not be passed" (`HWW:309-310`). `quick` for a narrow question. `deep` for cross-component or risky topics | `deep` for routine ideas: 35K per proposal against 15K at standard |
| `--strategy` (`-s`) | `systematic`, `agile`, `enterprise`, `auto` | `auto` | `auto` picks by keywords: compliance / audit / regulation / enterprise / SOC2 / SOX / HIPAA / large customers means enterprise; MVP / prototype / quick / experiment / iterate / ship fast / validate means agile; else systematic (`st:26-32`). `enterprise` forces `--depth deep` unless `--depth` is given (`cmd:67`, `SKILL:110`) and sets personas architect, analyzer, devops, scribe, qa (`asb:19`) | Set it explicitly when the topic is compliance-driven | Leaving `auto` on a topic that merely contains "audit", "quick" or "validate": the keyword rules can flip strategy. Whether an auto-detected enterprise also forces deep is unclear: Wave 0 applies the rule (`SKILL:110`) before Wave 1 detects the strategy (`SKILL:123`) (UNVERIFIED) |
| `--codebase` / `--no-codebase` | flags | auto: on for domains code, architecture, incident (`SKILL:183`) | Runs a quick codebase scan (Auggie, then Serena, then Glob/Grep) into `enrichment/codebase-context.md` (`hr:9-40`); total enrichment summary capped near 3000 tokens (`SKILL:198`) | `--codebase` for a product or process topic that touches existing code | `--no-codebase` is right for a greenfield N topic. The scan is shallow: not a substitute for `/tech-research` |
| `--research` / `--no-research` | `light`, `deep`, `none` / flag | auto | `light` routes to `/sc:research --depth quick`, `deep` routes to the `tech-research` skill (`SKILL:185-186`, `hr:42-80`). Auto-light when the topic names a framework not in the project; auto-deep only for enterprise + novel technology (`SKILL:185-186`) | `light` when the topic depends on an outside library or standard | `deep` below HIGH: `tech-research` is itself a heavy run (`HWW:255`). Note: the skill directory `sc-research-protocol` does not exist under `~/.claude/skills/`; the table allows `/sc:research` standalone and `hr:55-59` falls back to WebSearch (UNVERIFIED which path runs) |
| `--personas p1,p2` | comma list | auto by domain (`asb:9-17`) | Overrides persona choice. `security` is never auto-selected, only when named here (`asb:29-35`, `SKILL:216`). Empty value STOPs (`SKILL:101`) | HIGH topics with a risk class (secrets, permissions, user input, paths, infrastructure): name `security` explicitly | Naming personas for LOW work: adds cost for no gain (J) |
| `--models a,b,c` | aliases | `opus,sonnet,haiku` | Round-robin model per persona (`asb:53-73`). Unset env aliases are not an error (`SKILL:109`) | Leave default | Changing it without a reason |
| `--blind` | flag | false | Pass-through: strips model names before adversarial scoring (`cmd:57`, `adv:343`) | HIGH, deep, when model bias would matter | Everything else |
| `--convergence FLOAT` | 0.50-0.99 (`adv:335`) | 0.75 here; adversarial's own default is 0.80 (`adv:335`) | Pass-through threshold; the adversarial table describes it as the threshold "for deep mode" (`adv:335`). Brainstorm's own PASS / PARTIAL / FAIL cutoffs are fixed at 0.65 and 0.50 whatever you pass (`SKILL:290-292`) | Leave default | Raising it to force agreement: it does not move the 0.65 pass line |
| `--interactive` (`-i`) | flag | false | Pauses for the user at Socratic and adversarial decision points (`cmd:59`). Without it the Socratic batches "auto-proceed using best-available context" (`SKILL:134`): no real answers are collected | Any MEDIUM+ topic whose answers are not in files or the topic text | Unattended runs. Do not expect a dialogue if you leave it off |
| `--handoff` | `none`, `design`, `tasklist`, `task` | `none` | Runs in Wave 4, only after PASS or PARTIAL (`SKILL:290-292`). `none`: prints the artifact table and next steps (`SKILL:311`). `design`: prints a hint only (`SKILL:313`). `tasklist`: calls `sc-tasklist-protocol --source merged-requirements.md` after a 3-requirement check (`SKILL:315-318`): RETIRED, never use. `task`: calls `Skill task-builder --source ... --template <feature/bugfix/migration/documentation/decision-record>-template` (`SKILL:320-330`, `hr:206-225`) | `none`, then build the task file yourself with `--spec` (J, see section 4) | `tasklist` (retired). `task`: `task-builder` documents only a goal, `--spec`, `--cli` and a BUILD_REQUEST path (`task-builder/SKILL.md:33-43`), has no `--source`, `--template` or the five `*-template` names (grep: no hits), and the handoff passes no `--spec` (`hr:217-223`); so it may leave `reflect_pre` as `skipped` (UNVERIFIED, derived from `task-builder/SKILL.md:41`). `design` adds nothing a person cannot type |
| `--output` (`-o`) | dir | `.dev/brainstorms/<ts>-<slug>/` | Run folder; on collision a `-N` suffix, STOP at 100 (`SKILL:108`) | Leave default so a checker can find it (J) | Custom paths hide the footprint (J) |
| `--dry-run` | flag | false | Runs Waves 0-2B, prints the agent spec and token estimate, skips Waves 3-4; contract `status: dry-run` (`SKILL:249-254`) | Before `--depth deep` or `--strategy enterprise`, to see cost | It is not a deliverable: no `merged-requirements.md` |
| `--resume-from PATH` | seed-brief path | none | Skips the Socratic dialogue and reuses a saved seed brief; needs frontmatter `topic, domain, strategy, depth` (`SKILL:124-128`). Also the retry route after a hard abort (`SKILL:400`); an interrupted dialogue saves `seed-brief-partial.md` (`SKILL:393`) | Continue an interrupted run | Starting over a finished run |
| `--force-stale` | flag | false | Lets `--resume-from` proceed when domain re-classification differs (`cmd:64`, `SKILL:127`) | Only with `--resume-from` | Otherwise |

**Does not exist** (people may assume it): `--spec` (a spec can only arrive as `@file` in the topic); `--handoff implement` or `roadmap` (the `implement` value belongs to `/sc:workflow`, `workflow.md:7,40`); `--proposals 1` (floor is 2, `SKILL:96`, although a 1-proposal run exists on disk, see section 5); `--focus` and `--pipeline` (adversarial flags, not passed through, `adv:334-345`); `--tier` or `--compliance`.

## 3. Scope x complexity matrix

**How this command varies with complexity.** It does vary, through one knob: `--depth` (plus `--proposals` and `--interactive`). Its own files tie depth only to cost and rounds, never to scope or to a score. Examples in the command file: `standard` for a feature discovery, `deep` for an incident post-mortem, a cross-domain redesign and a blind comparison (`cmd:78,86,102,112`); no `quick` example. The task-builder TCS (`task-builder/SKILL.md:2402-2441`) cannot be used as an input: it is computed from a finished task file (S1 reads the "MDTM body", S3 needs a `--spec`), which does not exist yet when a brainstorm runs. So the bands below are JUDGMENT, built from signals the files do name:

| Band | Signals (all (J) as a grouping; each signal is cited) |
|---|---|
| LOW | The author can state the outcome and name the files; one subsystem; a driving spec, PRD or story already exists, or the request already answers what / why / where (`HWW:30`); no risk class touched |
| MEDIUM | Intent is clear but alternatives are open; two or three components (the file's own rule: three or more components or "across" means `architecture`, one component means `code`, `st:20`); no driving spec yet; the author names some files, not all; low-to-moderate risk |
| HIGH | Three or more components or "across" (`st:20`); competing approaches; interfaces shared between stories; novel outside technology (`hr:67-69`); compliance wording (`st:30`); a security-review class: login, permissions, secrets, user input, file paths (`HWW:200`); costly to reverse (deep probe questions, `st:55-62`) |

No file rates this command REQUIRED anywhere: the guide runs it "only if the idea is vague" (`HWW:309`) and the BMad twin is `required=false` (`bmad-help.csv:3`). So REQUIRED never appears below.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP | SKIP | SKIP (J). A one-off means the exact change is already known (`HWW:16`); if it is not known, it is not a T: re-scope |
| B bug fix | SKIP | SKIP | OPTIONAL (J), `--depth quick --no-research`. `/sc:troubleshoot` comes first; brainstorm is "upstream ... when the symptom is genuinely ambiguous" (`troubleshoot.md:213`). It yields requirements, not a diagnosis (`cmd:186`) |
| S single story | SKIP (`scenarios.md:29` lists brainstorm as skippable for a story) | OPTIONAL (J), `--depth quick` | OPTIONAL (J), `--depth standard --interactive`. A single story that needs a deep brainstorm is probably an F: re-scope |
| F multi-story feature | SKIP. Clear requirements go straight to a short spec file and `/task-builder --spec`; the guide route has no brainstorm step (`HWW:93,306-307`) | WORTH IT, `--depth standard --handoff none` | WORTH IT, `--depth deep --interactive`; add `--personas ...,security` if a risk class applies (J) |
| R multi-feature release (re-rated, see section 7) | SKIP (J) | OPTIONAL (J), `--depth standard`. Skip it if `/sc:release-split` will run: that command runs a brainstorm itself as Part 1 (`release-split SKILL:103,149-161`) | WORTH IT (J), `--depth deep --interactive`, only when the release scope itself is unsettled; not when each feature already has a spec |
| N new product | OPTIONAL (J), `--depth quick`. Full-spec step 1 is "only if the idea is vague" (`HWW:309`) | WORTH IT, `--depth standard` (guide default, `HWW:309`) | WORTH IT, `--depth deep --interactive`; `--strategy enterprise` only if compliance wording is real; `--no-codebase` if greenfield (J) |

Flag set by band in one line: LOW and MEDIUM use `--handoff none` and default or `quick` depth; HIGH uses `deep` with `--interactive`; `--handoff` is `none` at every band (J), because the two useful values are worse than doing the next step by hand (section 4).

## 4. Choose this or the neighbour

### 4.1 `/sc:brainstorm` vs `bmad-brainstorming`

What each is (files): `bmad-brainstorming` is a creative coach with three stances (Facilitator, Creative Partner, Ideate for me, `bmad:SKILL.md:12`); it says "aim past 100 ideas; resist concluding" and one prompt per message (`bmad:SKILL.md:33,35`); output is a `.memlog.md` under `_bmad-output/brainstorming/brainstorm-{topic_slug}-{date}/` (`bmad:customize.toml:67-68`) plus opt-in `brainstorm.html` / `brainstorm-intent.md` (`bmad:references/finalize.md:20-22`); it has no adversarial merge and no enumerated-requirements output. `/sc:brainstorm` is convergent: it ends in `merged-requirements.md` with a convergence score (`SKILL:289-292`). BMad catalog: phase 1-analysis `required=false` and "anytime" (`_bmad/_config/bmad-help.csv:3,33`). Running both on one idea is waste (value file line 50, O1).

| Signal | Pick |
|---|---|
| Next step is `bmad-product-brief`, `bmad-prd` or `bmad-spec` (BMad lane) | `bmad-brainstorming`: its own wrap-up points to those (`bmad:references/finalize.md:21,26`) |
| Next step is `/prd`, `/task-builder --spec`, `/sc:workflow` or `/roadmap` (task-file lane) | `/sc:brainstorm`: the output is a requirements file you can pass as the spec |
| Need many ideas, the human wants to generate them, no decision needed yet | `bmad-brainstorming` (divergent) |
| Topic is ambiguous with competing approaches that need a decision and a spec | `/sc:brainstorm` (parallel proposals plus debate) |
| HIGH: three or more components, shared interfaces, risk class | `/sc:brainstorm --depth deep` (J): only it has an adversarial debate |
| LOW or MEDIUM and a person wants to think aloud | `bmad-brainstorming` (J) |
| Must run unattended | `/sc:brainstorm` without `--interactive`. `bmad-brainstorming` goes headless only on a machine signal; a present human always means interactive (`bmad:references/headless.md:7-11`) |

### 4.2 Other neighbours

| Neighbour | Rule (cited) |
|---|---|
| `/tech-research` | The unknown is facts about our code or feasibility, or you cannot name the files: `/tech-research` first (`HWW:19,142`). Brainstorm's codebase scan is capped near 3000 tokens (`SKILL:198`). Brainstorm only if "what to build" is still open afterwards (J) |
| `/sc:adversarial` | You already have two or more drafts: `/sc:adversarial --compare` (`HWW:152`). Brainstorm generates its own variants (adversarial Mode B, `SKILL:266-281`); do not run it to compare drafts you wrote |
| `/sc:design` | Brainstorm never invokes it (`cmd:158`, `SKILL:313`). One new interface: `/sc:design` afterwards (`HWW:98`). Something others build against: `/tdd` |
| `/prd`, `bmad-prd` | Requirements already clear: skip brainstorm, write the PRD or short spec (`HWW:93`). Vague: brainstorm, then `/prd "Start from <merged-requirements.md>"` (`HWW:56`) |
| `/sc:workflow` vs `/task-builder` after brainstorm | Not decided by this command. Use the validated rule: multi-story feature needs `/task-builder` + `/task` with `--spec` (`validation-feature-task-builder-vs-sc-workflow.md`); a single story may use `/sc:workflow --depth quick` (`HWW:17`). Pass the `merged-requirements.md` path as `--spec` (J) |
| `/sc:tasklist` | RETIRED. Do not use `--handoff tasklist`. The "Next:" text of `--handoff none` still suggests `/sc:tasklist` and `/sc:implement @merged-requirements.md` (`SKILL:311`, `hr:164-166`): a checker must not treat that printed suggestion as the pipeline, and `/sc:implement` straight from requirements skips the tasklist step that is the validated minimum for F |
| `/sc:release-split` | It calls brainstorm itself (`release-split SKILL:149,161`). A brainstorm folder created inside a release-split run belongs to release-split; a standalone one before it is redundant at R-MEDIUM (J) |
| `bmad-forge-idea`, `bmad-party-mode`, `openspec-explore` | Idea-stage aids outside Ryan's pipelines (value file rows 80, 90, 100). Not a substitute for either brainstorm in the checker's eyes |

## 5. What a scheduled checker can see

A footprint exists on disk. Observed in 11 run folders under `/home/coder/workspaces/Coder/.dev/brainstorms/` (names `YYYYMMDDTHHMMSSZ-<slug>`), counted 2026-10-27.

| Artifact | Path / keys | Source | Seen in 11 observed folders |
|---|---|---|---|
| Run folder | `.dev/brainstorms/<ts>-<slug>/` (`-N` suffix on collision) | `cmd:61`, `SKILL:108` | 11 |
| Seed brief | `seed-brief.md`; frontmatter `topic, domain, strategy, depth, proposals_target, handoff_target, created` | `SKILL:138-147` | 7 |
| Merged requirements | `merged-requirements.md`; frontmatter `adversarial_status: partial` when PARTIAL | `SKILL:290-291` | 9 |
| Return contract | `return-contract.yaml`; stable keys `contract_version, status (success/partial/failed/dry-run), convergence_score, domain, proposal_count, handoff_action, unresolved_conflicts`; telemetry block is "non-stable" | `SKILL:336-378` | 7 |
| Adversarial artifacts | `adversarial/` (6 files) | `SKILL:59` | 5 |
| Enrichment | `enrichment/` | `SKILL:57-58` | 5 |
| Failure marks | `brainstorm-failed.md`; `seed-brief-partial.md` | `SKILL:297,393` | 0 (not observed) |
| In git | `git ls-files .dev/brainstorms` lists 111 files in this worktree, so committed runs show up in the repo and in PR diffs; an uncommitted run is visible only inside that engineer's workspace (J) | command run on this worktree | n/a |
| BMad twin | `_bmad-output/brainstorming/brainstorm-<slug>-<date>/.memlog.md`; frontmatter `topic, goal, mode (facilitator/partner/autonomous), status (set to complete at wrap-up), updated`; 74 tracked files under `_bmad-output/brainstorming/` | `bmad:customize.toml:67-68`, `bmad:references/finalize.md:12` | 2 folders (one `status: complete`, one still in progress without `status`) |
| Skill load / flags typed | transcript only; `Skill sc:brainstorm-protocol` is the activation line (`cmd:140-141`) | | none on disk |

What the 11 folders show about legitimate short forms (so the checker does not flag them):
- Flags used where the seed brief records them: `depth: standard` in 5, `depth: quick` in 1, `deep` in 0; `handoff_target: none` in all 6 seed briefs that record it. No observed run used any `--handoff` value other than `none`.
- Reduced forms exist: `20261008T201500Z-tailscale-device-cleanup` has a return contract noting a "lightweight two-critic debate, not sc-adversarial-protocol" (`convergence_score: null`, `proposal_count: 1`); `20261003T004656Z-orca-reader-var-expansion-r2` notes "reduced re-ground, not a new debate"; `20261009T135100Z-orca-agents-defaults` is `quick`, `proposals_target: 1`, `status: partial`. How these were produced is UNVERIFIED (a 1-proposal run is below the protocol's floor of 2, `SKILL:96`).
- Four folders have no `return-contract.yaml`, four have no `seed-brief.md`, two have no `merged-requirements.md` (`20260930T171955Z-orca-gh-auth`, `20261008T201500Z-tailscale-device-cleanup`). The only file common to the completed ones is `merged-requirements.md`.
- Dry run leaves a seed brief and a contract with `status: dry-run` and no merged file (`SKILL:254`).

## 6. Expected-step rule

- **Count the idea-shaping step as expected** (either `/sc:brainstorm` or `bmad-brainstorming` satisfies it) only when all three hold (J, built on `HWW:309` "only if the idea is vague"): scope is F or N (R only at HIGH); complexity is MEDIUM or HIGH; and no spec, PRD, requirements file or story file existed before the tasklist step was created. Even then it is WORTH IT, never REQUIRED: no file marks it required (`bmad-help.csv:3`, `HWW:309`).
- **Absence is fine** for T and B at any complexity; S at any complexity; F-LOW; any scope when a spec / PRD / story / epic predates the tasklist; R when each feature already has a spec or `/sc:release-split` ran (it runs a brainstorm itself). Do not judge the flags chosen (`--depth`, `--proposals`, `--handoff none`) or short and hand-run forms (3 of the 11 observed folders). The one thing a checker may flag is `--handoff tasklist` (retired `/sc:tasklist`).
- Note for the checker design: `scenarios.md:34-35` lists "brainstorm or design" in S5 and says "Allowed to skip: nothing in the chain", which conflicts with the guide's "only if vague". Align S5 with this rule.

## 7. Proposed changes to command-value-by-phase.md

Line numbers refer to `command-value-by-phase.md` as read on 2026-10-27.

| # | Where | Current text | Proposed text |
|---|---|---|---|
| 1 | Line 64, `/sc:brainstorm` row, columns T/B/S/F/R/N | `SKIP \| SKIP \| OPTIONAL \| WORTH IT \| OPTIONAL \| WORTH IT` | Keep the six cells. **R cell: keep `OPTIONAL`, but under the new definition (multi-feature release, one step below N) it reads "OPTIONAL; WORTH IT only when the release scope is unsettled (HIGH); SKIP when each feature already has a spec or `/sc:release-split` runs".** The old R cell was probably rated on a single-feature reading, where it was OPTIONAL for a different reason (a feature's release is a phase inside S or F). If the merged file gains complexity sub-columns, use the section 3 matrix |
| 2 | Line 64, Notes | `Guide: "only if the idea is still vague". \`--handoff task\` goes straight to a task file. ‡ with \`bmad-brainstorming\`` | `Never REQUIRED: guide runs it "only if the idea is vague" (HOW-WE-WORK.md:309). Skip when a spec, PRD or story already exists. --depth quick/standard/deep by complexity. Use --handoff none, then /task-builder --spec <merged-requirements.md>: --handoff task passes no --spec, and --handoff tasklist calls the retired /sc:tasklist. Footprint .dev/brainstorms/<ts>-<slug>/. ‡ with bmad-brainstorming` |
| 3 | Line 79, `bmad-brainstorming` Notes | `bmad-help.csv: phase 1-analysis, required=false. ‡ with /sc:brainstorm` | Append: `Divergent idea generation with a coach (Facilitator / Creative Partner / Ideate for me); no adversarial merge, no requirements spec. Pick when the next step is bmad-product-brief / bmad-prd or when ideas, not a decision, are needed. Footprint _bmad-output/brainstorming/brainstorm-<slug>-<date>/.memlog.md (status: complete at wrap-up)`. R cell: same note as row 1 |
| 4 | Line 227, O1 "Why" | `Has --handoff none\|design\|tasklist\|task, so its output feeds either lane. Use bmad-brainstorming only when the next step is bmad-prd` | `Its merged-requirements.md feeds either lane (as a file, not through --handoff: tasklist calls the retired /sc:tasklist and task passes no --spec). Use bmad-brainstorming when the next step is bmad-product-brief / bmad-prd, or when the need is ideas rather than a decision` |
| 5 | Line 255 (F row, WORTH IT additions) | list has no `/sc:brainstorm` | Add `/sc:brainstorm --depth standard` (only when no spec or requirements file exists) |
| 6 | Line 256 (R row, WORTH IT additions) | no `/sc:brainstorm` | Add `/sc:brainstorm --depth deep` (only when release scope is unsettled and `/sc:release-split` is not planned) |
| 7 | Line 265 (footprint table) | `.dev/brainstorms/<timestamp>-<name>/merged-requirements.md` / `guide 3.1` | `.dev/brainstorms/<YYYYMMDDTHHMMSSZ>-<slug>/`: `merged-requirements.md` (9 of 11 observed), `seed-brief.md` (7), `return-contract.yaml` (7); tracked in git when committed. BMad twin: `_bmad-output/brainstorming/brainstorm-<slug>-<date>/.memlog.md`. Source: protocol `SKILL.md:136-147,334-378` and observed folders |
| 8 | Line 281 (what was read) | says `/sc:brainstorm` was read for usage and flag lines only | Note that command file, protocol skill and its three refs were later read in full (this file) |
| 9 | New unverified items for section 5 (line 283 onward) | n/a | Add U-items from section 8 below that concern `--handoff task`, the missing `sc-research-protocol` skill, and the 1-proposal runs on disk |

## 8. Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | The LOW / MEDIUM / HIGH bands and every `(J)` cell in section 3 | No file ties brainstorm depth to scope or to a complexity score; TCS needs a finished task file | Team agreement (Ryan) |
| U2 | `--handoff task` works as written | It passes `--source` and `--template <x>-template` to `task-builder`, whose SKILL.md defines neither flag nor the five template names (`task-builder/SKILL.md:33-43`, grep no hits). Not run | Run it once on a disposable topic, or read `task-builder` Branch handling for those arguments |
| U3 | A task file made by `--handoff task` records `reflect_pre: skipped` | Derived: no `--spec` is passed (`hr:217-223`) and spec resolution needs `--spec`, an `@file` in the goal or a `SPEC:` field (`task-builder/SKILL.md:41`). Not observed | Inspect a task file produced that way |
| U4 | Which research route runs for `--research light` | `sc-research-protocol` is absent from `~/.claude/skills/`; `SKILL:185` allows `/sc:research`, `hr:55-59` falls back to WebSearch | Observe a run's `enrichment/research-light.md` and `quality_tier` |
| U5 | Wave 0 prerequisite path | It reads `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` (`SKILL:103`), a source-tree path, while installed skills live in `~/.claude/skills/`. Runs complete on disk, so it evidently resolves; how is unobserved. The spec it cites, `.dev/eval-workspaces/sc-brainstorm/SPEC.md` (`cmd:9`), was not found on this machine and was not read | Read a run transcript; find the spec in the IronClaude repo |
| U6 | Whether auto-detected `enterprise` forces `--depth deep` | Wave 0 applies the rule (`SKILL:110`) before Wave 1 detects strategy (`SKILL:123`) | Run `--dry-run` with a topic containing "audit" |
| U7 | How the 1-proposal and "lightweight two-critic" runs on disk were produced | Below the protocol's floor of 2 (`SKILL:96`); the contract comments say so but not how | Ask the authors; read their transcripts |
| U8 | Real token cost per depth | Only the formula in `asb:136-157`; the 276K figure for deep + 7 proposals is my arithmetic on the code-domain persona list, not a measurement | Read `token_usage` in a deep run's `return-contract.yaml` |
| U9 | Persona agent files | `asb:27` says each persona needs `src/superclaude/agents/<persona>.md` "or known persona alias"; none of architect / refactorer / qa / backend / frontend / analyzer / devops / scribe was found in `~/.claude/agents/`; behaviour on a miss is a substitute-with-INFO rule only | Observe an `agent_spec` in a contract and its run log |
| U10 | Cost and time of `bmad-brainstorming` | Not stated in its files | Observe a session |
| U11 | Whether committed `.dev/brainstorms/` folders reach a checker's view | `git ls-files` shows 111 tracked files in this worktree; whether every engineer commits them is unknown | Count across engineers' branches or merged PRs |
| U12 | Whether the other engineers' `~/.claude` copies match the one read | Brief ruling 1: these files live in each home directory | Compare versions (`version: 2.0.0` in `cmd:8`) across machines |
