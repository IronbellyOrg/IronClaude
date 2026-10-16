# Research: In-session routing surfaces (/sc:help, /sc:recommend, mirrors)
**Scope:** /tmp/ic-master/src/superclaude/commands/{help,recommend,README}.md, src/superclaude/skills/sc-recommend/, .claude/cache/sc-recommend-lookup.yaml, routing hooks, commands/sc-*.md and plugins/ mirrors
**Status:** Complete
**Date:** 2026-10-12
**Source snapshot:** /tmp/ic-master (IronClaude origin/master), per `/tmp/ic-master/SNAPSHOT.txt`: "snapshot of origin/master ee1c1787 (2026-10-11)". The snapshot is not a git checkout (no `.git`), so file history could not be checked.
**Reference guide:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md` (242 lines; cited below as GUIDE:line)

All paths below are relative to `/tmp/ic-master/` unless stated otherwise.
---

## Bottom line (read this first)

| Question | Short answer |
|---|---|
| How does `/sc:help` answer? | A hand-written static table of 22 commands plus a flags reference. No live discovery. It omits 21 of 43 commands and all 36 skills, including every skill the guide's main workflows depend on (`/prd`, `/tdd`, `/roadmap`, `/task-builder`, `/task`, `/tech-research`). It even says it "is manually generated and may become outdated" (help.md:149). |
| How does `/sc:recommend` decide? | A hot-path cache lookup (Haiku classifier into a closed 10-key list, then a CLI dispatch), falling through to a cold path: Glob of `src/superclaude/{commands,skills,agents,templates}`, one auggie ranking query, a Read-verify of up to 3 candidates, then a native-first "net value" rubric. It never reads any "how we work" or workflow document. |
| Can it route the guide's workflows? | Partly. It can name a single correct entry point for bug diagnosis and codebase research. It cannot emit an ordered multi-step workflow, it is biased toward `/sc:*` commands and native tools in exactly the places the guide says otherwise, and two of its four cached rows (and two classifier keys) point at the wrong tool per the guide. In a normal user project (not the IronClaude repo itself) its Glob finds nothing, because it only looks under `src/superclaude/`. |
| Is the cache stale? | Yes. The stored `surface_hash` no longer matches the current surface, so the cache loader discards every row on load (the cache is dead weight today). 3 of 4 rows also have stale `source_hash` values. |
| Where must edits go? | `src/superclaude/` only. `.claude/` copies are gitignored `make sync-dev` output and a pre-commit hook blocks committing them. `plugins/superclaude/commands/{help,recommend}.md` is a second tracked copy that the plugin build and a source-checkout install fallback read, so it must be kept in step (or retired). Root `commands/sc-*.md` is a stale copy of the upstream SuperClaude framework written by `scripts/sync_from_framework.py` (run by a cron CI workflow); nothing installs or reads it. |
| One source of truth? | Make the guide (relocated into the IronClaude repo, inside `src/superclaude/`) the single routing document. `/sc:help` prints a short generated inventory plus "for which-to-use-when, see the guide". `/sc:recommend` reads the guide as a mandatory ref in Phase 0 and treats its workflow table as the priority source for ordering and safe defaults, while keeping live enumeration for existence and flag checks. |

---

## 1. How `/sc:help` builds its answer today

### 1.1 Mechanism [CODE-VERIFIED]

- `src/superclaude/commands/help.md` (149 lines) has no `## Activation` section and no backing skill. It is a self-contained prompt.
- Behavioral Flow is "Display: Present complete command list with descriptions" then "Complete" (help.md:18-21). "Information display only" (help.md:25).
- The list is a literal Markdown table at help.md:30-53 (22 rows). There is no Glob, no file read, no tool use. Boundaries forbid execution and file creation (help.md:141-145).
- help.md:55-129 is a long "Framework Flags" reference (mode, MCP, depth, execution, output flags). This duplicates `src/superclaude/core/FLAGS.md` in spirit and is not about which tool to use when.
- help.md:149 admits: "This list is manually generated and may become outdated."
- Frontmatter description (help.md:3): "List all available /sc commands and their functionality". It is scoped to `/sc:*` commands by design, so skills such as `/prd` are out of its contract today.

### 1.2 Full command inventory vs help.md [CODE-VERIFIED]

`src/superclaude/commands/` holds 43 command files plus `README.md` and `__init__.py`. "Listed" means the exact `` `/sc:<name>` `` string appears in help.md. 22 listed, 21 omitted.

| Command | In help.md? | Current frontmatter description (truncated) | Guide uses it? |
|---|---|---|---|
| `/sc:adversarial` | OMITTED | Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts | Yes (GUIDE:147) |
| `/sc:agent` | OMITTED | SC Agent, session controller that orchestrates investigation, implementation, and review | No |
| `/sc:analyze` | listed | Comprehensive code analysis ... | Yes (GUIDE:139) |
| `/sc:auggie-review` | OMITTED | Auggie-powered code review for PRs, local diffs, or file snapshots | Yes (GUIDE:195, 240) |
| `/sc:brainstorm` | listed (stale description) | Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge | Yes (GUIDE:48, 146) |
| `/sc:build` | listed | Build, compile, and package projects ... | No |
| `/sc:business-panel` | listed | (no description line in frontmatter) | Yes (GUIDE:150) |
| `/sc:cleanup-audit` | OMITTED | Multi-pass read-only repository audit ... | Yes (GUIDE:155, 235) |
| `/sc:cleanup` | listed | Systematically clean up code ... | Yes (GUIDE:159) |
| `/sc:cli-eval` | OMITTED | Manage the cliEval pipeline lifecycle ... | No |
| `/sc:cli-portify` | OMITTED | Port inference-based SuperClaude workflows into programmatic CLI pipelines | No |
| `/sc:design` | listed | Design system architecture, APIs, and component interfaces ... | Yes (GUIDE:94, 231) |
| `/sc:document` | listed | Generate focused documentation ... | Yes (GUIDE:179, 233) |
| `/sc:explain` | listed | Provide clear explanations of code ... | Yes (GUIDE:13, 140) |
| `/sc:git` | listed | Git operations with intelligent commit messages ... | No |
| `/sc:help` | listed | List all available /sc commands ... | No |
| `/sc:implement` | listed (stale description) | Middleweight spec executor: walk a spec/PRD/tasklist, per-task spec-compliance QA ... | Yes (GUIDE:15, 111) |
| `/sc:improve` | listed | Apply systematic improvements ... | Yes (GUIDE:160) |
| `/sc:index-repo` | OMITTED | Repository Indexing, 94% token reduction | No |
| `/sc:index` | listed | Generate comprehensive project documentation ... | No |
| `/sc:init-lite` | OMITTED | Safely audit project-local SuperClaude context surfaces ... | No |
| `/sc:load` | listed | Session lifecycle management with Serena MCP ... | No |
| `/sc:pm` | OMITTED | Project Manager Agent, default orchestration agent ... | No |
| `/sc:post-release` | OMITTED | Post-release follow-through ... | No |
| `/sc:pr-submit` | OMITTED | Open a PR on the fork and arm an in-session PR-review auto-remediation monitor ... | Yes (GUIDE:198, 241) |
| `/sc:recommend` | OMITTED | Build a refined, paste-ready prompt that delegates the user's goal ... | Yes (GUIDE:223) |
| `/sc:reflect` | listed (stale description) | Tiered reflection protocol, UC-1 pre / UC-2 post ... | Yes (GUIDE:79, 187, 239) |
| `/sc:release-split` | OMITTED | Neutral two-phase release split analysis ... | Yes (GUIDE:67) |
| `/sc:research` | OMITTED | Deep web research with adaptive planning ... | Yes (GUIDE:138, 234) |
| `/sc:review-translation` | OMITTED | Systematic localization review ... | No |
| `/sc:roadmap` | OMITTED | Generate roadmap pipeline artifacts from 1-3 specification, TDD, and PRD inputs | Yes, as a "do not use unless your lead says" contrast (GUIDE:232) |
| `/sc:save` | listed | Session lifecycle management ... | No |
| `/sc:spawn` | listed | Meta-system task orchestration ... | No |
| `/sc:spec-panel` | listed | Multi-expert specification review ... | Yes (GUIDE:56, 148) |
| `/sc:swarm-wizard` | OMITTED | Plain-language interactive guide to the superclaude swarm CLI ... | Yes (GUIDE:149) |
| `/sc:task` | listed (stale description) | Unified task execution with intelligent workflow management, MCP compliance ... | Yes (GUIDE:14, 229) |
| `/sc:tasklist` | OMITTED | Generate deterministic, Sprint CLI-compatible tasklist bundles from roadmaps | Contrast only (GUIDE:232) |
| `/sc:tdd` | OMITTED | Create or populate a Technical Design Document (TDD); activates the `tdd` skill (tdd.md:151) | Guide uses `/tdd` (GUIDE:60) |
| `/sc:test` | listed | Execute tests with coverage analysis ... | Yes (GUIDE:127, 167) |
| `/sc:troubleshoot` | listed (stale description) | Tiered debugging ... | Yes (GUIDE:120) |
| `/sc:validate-roadmap` | OMITTED | Validate roadmap pipeline outputs ... | No |
| `/sc:validate-tests` | OMITTED | Validate tier classification behavior against YAML test specifications | No |
| `/sc:workflow` | listed (stale description) | Generate a phased implementation plan from a PRD, spec, or feature prompt | Yes (GUIDE:15, 109) |

"Stale description" means help.md's one-liner describes the old behavior (for example help.md:42 says `/sc:implement` is "Feature and code implementation with intelligent persona activation and MCP integration", while implement.md frontmatter now says it is a "Middleweight spec executor" with per-task QA; help.md:46 says `/sc:reflect` is "Task reflection and validation using Serena MCP" while reflect.md is now a tiered UC-1/UC-2 audit; help.md:53 says `/sc:workflow` generates workflows "from PRDs" while it now writes a checked plan consumed by `/sc:implement`).

**Guide-relevant commands help.md omits (12):** `/sc:adversarial`, `/sc:auggie-review`, `/sc:cleanup-audit`, `/sc:pr-submit`, `/sc:recommend`, `/sc:release-split`, `/sc:research`, `/sc:swarm-wizard`, `/sc:roadmap` and `/sc:tasklist` (as contrasts), `/sc:tdd`. Note that help.md omits `/sc:recommend` even though the guide's rule 8 sends unsure users to it (GUIDE:223).

### 1.3 Full skill inventory vs help.md [CODE-VERIFIED]

`src/superclaude/skills/` has 36 skill directories with a `SKILL.md`. help.md lists **none** of them. Mapping to commands was taken from each command's `## Activation > Skill <name>` line (grep of `src/superclaude/commands/*.md`).

| Skill | Reached by | Guide uses it? |
|---|---|---|
| `prd` | Skill only (`/prd`), no command | Yes, core of 3.1 (GUIDE:52) |
| `tdd` | `/tdd` skill, and `/sc:tdd` (tdd.md:151) | Yes (GUIDE:60) |
| `roadmap` | Skill only (`/roadmap`) | Yes (GUIDE:71) |
| `task-builder` | Skill only (`/task-builder`) | Yes, level 4 (GUIDE:16) |
| `task` | Skill only (`/task`) | Yes (GUIDE:16, 76, 205) |
| `tech-research` | Skill only (`/tech-research`) | Yes, level 5 (GUIDE:17) |
| `tech-reference` | Skill only | Yes (GUIDE:176) |
| `operational-guide` | Skill only | Yes (GUIDE:177) |
| `readme` | Skill only | Yes (GUIDE:178) |
| `sc-crash-recovery` | Skill only (no command) | Yes (GUIDE:210) |
| `confidence-check` | Skill only | No |
| `ccsession-tag` | Skill only | No |
| `sc-bare-review` | Delegate-only infrastructure skill (no slash command) | No |
| `sc-recommend` | `/sc:recommend` (recommend.md:56) | Yes |
| `sc-adversarial-protocol` | `/sc:adversarial` | via command |
| `sc-auggie-review-protocol` | `/sc:auggie-review` | via command |
| `sc-brainstorm-protocol` | `/sc:brainstorm` | via command |
| `sc-cleanup-audit-protocol` | `/sc:cleanup-audit` | via command |
| `sc-cli-eval-protocol` | `/sc:cli-eval` | No |
| `sc-cli-portify-protocol` | `/sc:cli-portify` | No |
| `sc-implement-protocol` | `/sc:implement` | via command |
| `sc-init-lite-protocol` | `/sc:init-lite` | No |
| `sc-pm-protocol` | `/sc:pm` | No |
| `sc-post-release-protocol` | `/sc:post-release` | No |
| `sc-pr-submit-protocol` | `/sc:pr-submit` | via command |
| `sc-reflect-protocol` | `/sc:reflect` | via command |
| `sc-release-split-protocol` | `/sc:release-split` | via command |
| `sc-review-translation-protocol` | `/sc:review-translation` | No |
| `sc-roadmap-protocol` | `/sc:roadmap` | contrast |
| `sc-swarm-wizard-protocol` | `/sc:swarm-wizard` | via command |
| `sc-task-protocol` | `/sc:task` | via command |
| `sc-tasklist-protocol` | `/sc:tasklist` | contrast |
| `sc-troubleshoot-protocol` | `/sc:troubleshoot` | via command |
| `sc-validate-roadmap-protocol` | `/sc:validate-roadmap` | No |
| `sc-validate-tests-protocol` | `/sc:validate-tests` | No |
| `sc-workflow-protocol` | `/sc:workflow` | via command |

**Twelve skills have no `/sc:` command in front of them** (prd, roadmap, task-builder, task, tech-research, tech-reference, operational-guide, readme, sc-crash-recovery, confidence-check, ccsession-tag, sc-bare-review). Ten of those (all except confidence-check, ccsession-tag) appear in the guide, and nine of them carry the guide's levels 4-6. help.md cannot surface any of them because its contract is "/sc commands" only.

Also not in help.md: Claude Code built-ins the guide relies on, `/code-review` and `/security-review` (GUIDE:193-194). These are not IronClaude files, so live enumeration will never find them either.

### 1.4 Other observations

- `src/superclaude/core/CLAUDE.md:100` tells every session "use `/sc:help` to list all available", so help.md is the advertised discovery entry point despite covering about half the commands.
- `docs/reference/suggested-commands.md:143`, `docs/user-guide/commands.md`, `docs/reference/commands-list.md`, `docs/user-guide/modes.md` also reference `/sc:help`; these are human-doc routing surfaces outside my scope but are inbound references (section 5).
- Size constraint: `make lint-architecture` (run in CI at `.github/workflows/quick-check.yml:57`) warns at 200 lines and fails at 500 lines per command file (Makefile Check 3/4). help.md is 149 lines today; a full 79-row inventory plus flags would cross 200. This argues for help printing a compact inventory and pointing to the guide rather than inlining everything.

---

## 2. How `/sc:recommend` decides today

### 2.1 Layers [CODE-VERIFIED]

| Layer | File | What it does |
|---|---|---|
| Command | `src/superclaude/commands/recommend.md` (134 lines) | Thin dispatcher. "MANDATORY: Before executing any protocol steps, invoke: Skill sc-recommend" (recommend.md:54-58). Flags: `--plugin`, `--eval`, `--minstar` only (recommend.md:32-38). |
| Skill | `src/superclaude/skills/sc-recommend/SKILL.md` (306 lines) | Hot path (SKILL.md:38-57), cold path Phases 0-3 (SKILL.md:59-210), cache write-back (SKILL.md:212-239), rules R1-R4 (SKILL.md:241-264). |
| Refs | `refs/surface-enumeration.md` (107), `refs/delegation-vs-native-heuristics.md` (97), `refs/plugin-ecosystem-sources.md` (140) | Glob set and auggie query; net-value rubric; `--plugin` sources. |
| CLI | `src/superclaude/cli/recommend/` (12 modules, 1697 lines) | `dispatch.py` (hot-path decision), `cache.py` (surface hash, atomic writer), `prompts.py` (Haiku classifier and cold-path runbook), eval and telemetry modules. |
| Cache | `.claude/cache/sc-recommend-lookup.yaml` (91 lines, 4 rows) | Tracked by a `.gitignore` exception (`.gitignore:123-125`). |
| Hook | `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` | PreToolUse(Skill) reminder; fail-open (section 2.6). |

### 2.2 Hot path (tried first) [CODE-VERIFIED]

1. One Haiku subagent classifies the verbatim request using `prompts.py::CLASSIFIER_PROMPT` (SKILL.md:44). It may only emit one of a **closed list of 10 keys** (`prompts.py:28-39`): `spec-generation`, `codebase-research`, `tasklist-generation`, `parallel-agent-fanout`, `roadmap-generation`, `adversarial-review`, `cleanup-audit`, `troubleshoot-debug`, `web-research`, `cli-portify`. Keys 5-10 are flagged in the source as "surface-derived DESIGN PROPOSALS that currently LACK iteration-1 eval coverage" (`prompts.py:22-27`).
2. `uv run superclaude recommend dispatch` runs `dispatch.py::dispatch` (`dispatch.py:74-137`): native short-circuit, unknown key to miss, top-2 delta below threshold to miss, table lookup, `source_hash` check, budget gate, then hit.
3. On a hit, the row's `prompt_envelope_template` is emitted verbatim (SKILL.md:53).

Note: this closed key list is itself a static keyword-to-category mapping, which the skill and the hook both say is the root cause of the previous version's failure (SKILL.md:63, 293; sc-recommend-phase0.sh:58-60). The classifier key descriptions are routing judgments (for example `spec-generation` = "build/generate a spec, TDD, or PRD from inputs", `prompts.py:55`).

### 2.3 Cold path (Phases 0-3) [CODE-VERIFIED]

- **Phase 0 Step A, live Glob.** Patterns are `src/superclaude/commands/*.md`, `src/superclaude/skills/*/SKILL.md`, `src/superclaude/agents/*.md`, `.claude/agents/*.md`, `src/superclaude/templates/**/*.md`, `examples/*-template.md` (SKILL.md:69-72; refs/surface-enumeration.md:15-24). All relative to cwd (refs/surface-enumeration.md:30).
- **Phase 0 Step B, one auggie query** ranks the enumerated names against the request (SKILL.md:80-86; refs/surface-enumeration.md:36-51). Degrades to Glob plus Read with a fixed notice when auggie is missing (SKILL.md:101-106).
- **Phase 0 Step C, Read-verify** each candidate's source file; unresolved candidates are dropped silently (SKILL.md:88-97). Hard cap of 3 candidates (refs/surface-enumeration.md:96-99).
- **Phase 1, net-value rubric.** Default is native Read/Edit (refs/delegation-vs-native-heuristics.md:5-16). Five axes (capability, scope, output structure, token budget, discipline) at lines 18-54. Tier preference: "Command (`/sc:<name>`) ... Almost always the right thing to recommend", "Skill directly ... recommend only when there is no command in front of the skill (rare in this project, most skills have a command)" (lines 58-62). Tie-break: fewer protocol phases first, command-level surface preferred (lines 89-97).
- **Phase 2, hand-off envelope** with one "Recommended delegation" and one paste-ready prompt (SKILL.md:126-156). Multiple blocks only for genuinely different alternatives (SKILL.md:34).
- **Phase 3, `--plugin`** ecosystem search (SKILL.md:158-210), not relevant to in-session routing.
- **Write-back**: a second Haiku subagent runs the condensed `COLD_PATH_RUNBOOK` (`prompts.py:109-202`) and returns a `cache_update`; the parent commits it with `superclaude recommend cache put` (SKILL.md:214-222).

### 2.4 Does it ever consult a "how we work" or workflow document? [CODE-VERIFIED: No]

- A search of `src/superclaude/skills/sc-recommend/`, `src/superclaude/commands/help.md`, `src/superclaude/commands/recommend.md`, and `src/superclaude/cli/recommend/` for `how-we-work`, `USER-GUIDE`, `user guide`, `user-guide` returned no matches.
- The Glob set (refs/surface-enumeration.md:15-24) contains no `docs/` path. Templates are enumerated, but templates describe document shape, not routing.
- The only routing knowledge is (a) whatever auggie infers from the codebase at query time, (b) the rubric in `refs/delegation-vs-native-heuristics.md`, (c) the 10-key classifier and the 4 cache rows. None encodes the guide's levels, workflow order, or safe defaults.

### 2.5 Can it route the guide's workflows correctly?

Assessment is from code and rubric reading. No live `/sc:recommend` run was made (read-only task), so per-workflow outcomes are **UNVERIFIED by execution**; they are what the documented algorithm and cached rows imply.

| Guide workflow | What the guide prescribes | What recommend would likely do | Verdict |
|---|---|---|---|
| 3.1 Full feature (PRD, critique, TDD, critique, release-split, roadmap, task per phase, PR) | 8-11 ordered steps across `/sc:brainstorm`, `/prd`, `/sc:spec-panel`, `/tdd`, `/sc:release-split`, `/roadmap`, `/task` (GUIDE:47-83) | Classifier picks `spec-generation`. The cached row for that key sends the user to `/sc:spec-panel` (lookup.yaml:6-29), which only critiques (GUIDE:57). Cold path returns at most one primary delegation (cap 3, alternatives not sequences). If the request says "roadmap", key `roadmap-generation` and the tier rule "prefer `/sc:<x>`" lean to `/sc:roadmap`, which the guide says not to use (GUIDE:232). | Wrong or incomplete. Cannot emit the sequence. |
| 3.2 Add a feature (spec file, `/task-builder --spec`, `/task`) | GUIDE:91-102 | Likely `tasklist-generation`. The cached row recommends `/sc:tasklist` "(or task-builder)" with `--spec` (lookup.yaml:50-70); the guide sends people to `/task-builder ... --spec` then `/task`. Rubric line 27 also names `/sc:tasklist` as the roadmap-to-tasklist tool. | Wrong primary tool. |
| Levels 2-3, small change | One file and 5 edits or fewer: native or `/sc:task`; a few files: `/sc:workflow --depth quick` then `/sc:implement` (GUIDE:14-15, 20, 106-113) | Rubric says "Scope 3 files or fewer, single-domain: native almost always wins" (heuristics:38). The guide's hard limit says more than one source file or more than 5 edits must go through a plan (GUIDE:20). A 2-3 file change would get "use Read then Edit" from recommend. | Contradicts the guide's hard limit for 2-3 file changes. Correct for the 1-file case. |
| 3.4 Bug fix | `/sc:troubleshoot --type bug`, then test-first fix plus `/sc:test`, or `/task-builder` from the report (GUIDE:119-131) | Key `troubleshoot-debug` (no cached row; cold path) would find `/sc:troubleshoot`. Follow-on steps are not produced. | Correct first step only. |
| 3.11 PR flow | `/code-review`, `/security-review`, `/sc:auggie-review --diff ... --no-post-pr`, then `/sc:pr-submit --monitor 1` (GUIDE:192-199) | `/code-review` and `/security-review` are Claude Code built-ins, not in the Glob surface, so R2 forbids recommending them (SKILL.md:249-251). `/sc:pr-submit` can be found, but R1 only checks that a flag exists, not that it is the safe choice; nothing forces `--monitor 1` (guide default warning GUIDE:241) or `--no-post-pr` (GUIDE:240). No classifier key covers PR work, so it is always a cold miss. | Partially wrong; unsafe defaults possible. |
| 3.12 Resume | Re-run `/task <path>`, re-run doc skills, `/sc:implement --resume`, `/sc:brainstorm --resume-from`, `/sc:pr-submit --resume`, or the `sc-crash-recovery` skill (GUIDE:203-210) | Cold path may find `sc-crash-recovery` via `src/superclaude/skills/*/SKILL.md`. Per-tool resume recipes (re-run same `/task`) live only in the guide. Rubric tier rule says skills without commands are "rare", which pushes away from it. | Partial. |
| 3.5 Investigate | `/tech-research` for our code, `/sc:research` for the web (GUIDE:137-138) | `codebase-research` row points at tech-research (lookup.yaml:30-49) but its template says "tech-research skill (or deep-research agent)", and the deep-research agent is a web researcher. `web-research` key exists. | Mostly correct; the "or deep-research agent" fallback blurs the guide's mix-up rule (GUIDE:234). |

**Consumer-project blind spot [CODE-VERIFIED from paths; runtime effect UNVERIFIED].** Every Glob pattern and the CLI's `compute_surface_hash` default base are `src/superclaude/...` relative to cwd (`cache.py:33-34`, `dispatch.py:80`, refs/surface-enumeration.md:15-24). A user working in their own project after `superclaude install` has commands in `~/.claude/commands/sc/` (`install_commands.py:25`) and skills in `~/.claude/skills/`, neither of which is enumerated. In that case Step A returns only `.claude/agents/*.md` if present, every command and skill candidate fails Step C, and R2 drops them. The guide's audience is exactly these users. Also `uv run superclaude recommend ...` (SKILL.md:48) assumes a `uv` project containing the `superclaude` package; in a consumer repo that command likely fails (UNVERIFIED).

### 2.6 Hook involvement [CODE-VERIFIED]

- `src/superclaude/hooks/scripts/sc-recommend-phase0.sh:1-67`: PreToolUse on the Skill tool. If the skill name is `sc-recommend`, `sc:recommend`, or the legacy `sc-recommend-protocol`, it prints a reminder block repeating the Phase 0 Glob set and auggie rule, then exits 0. It never blocks and never routes or offers commands itself.
- Registered in the tracked `.claude/settings.json:15-25` (matcher `Skill`), as a project hook only. `src/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/hooks.json` do not mention recommend (grep returned no match). `install_hooks.py:69-78` lists the script as a project-local script so `superclaude install` copies it, and `tests/cli/test_install_hooks.py:96` asserts that.
- The hook repeats the Glob set verbatim (lines 43-46). Any change to the enumeration (for example adding the guide as a mandatory read, or adding `~/.claude/skills`) must also change this hook, or the hook will contradict the skill.
- No other hook under `src/superclaude/hooks/scripts/` (freshness-*, auggie-flag-clear, reject-workspace-writes, pragmatic-subagent.js) routes or offers commands (file names checked; contents of freshness hooks not read in full, so "none offer commands" is UNVERIFIED for their bodies beyond the grep for `recommend|help|offer|suggest` in settings and hooks.json).

### 2.7 Is the cache stale? [CODE-VERIFIED: yes, and currently inert]

| Check | Stored | Current (computed on the snapshot) | Result |
|---|---|---|---|
| `surface_hash` (sha256 of sorted `src/superclaude/{commands/*.md,skills/*/SKILL.md,agents/*.md}`, `cache.py:51-63`) | `6f96875e...e2f3` (lookup.yaml:2) | `7aa6e590...64c6` | Mismatch. `LookupCache.load_or_create` discards all rows when the hash differs (`cache.py:87-109`), so every dispatch is a miss today. |
| `spec-generation` source_hash (`commands/spec-panel.md`) | `655dd700...` | `e7b1a2c6...` | Stale |
| `codebase-research` source_hash (`skills/tech-research/SKILL.md`) | `72a853d0...` | `b6ec931f...` | Stale |
| `tasklist-generation` source_hash (`commands/tasklist.md`) | `f3cd47a9...` | `a4ca4273...` | Stale |
| `parallel-agent-fanout` source_hash (`refs/delegation-vs-native-heuristics.md`) | `889c5d5d...` | `889c5d5d...` | Matches |
| `generated` | 2026-06-03 (lookup.yaml:3) | snapshot 2026-10-11 | About 4 months old |

Practical effect: the cache never hits, so it costs a Haiku classify plus a CLI call on every invocation and then runs the full cold path anyway. The danger is the write-back: the next cold run will recreate rows, and two of the four existing row designs (`spec-generation` to `/sc:spec-panel`, `tasklist-generation` to `/sc:tasklist`) conflict with the guide. If those rows come back, the hot path will serve guide-contradicting answers with high confidence.

---

## 3. Gaps to close, and how to have one source of truth

### 3.1 Gaps in `/sc:help`

| # | Gap | Evidence |
|---|---|---|
| H1 | Static list; 21 of 43 commands missing | help.md:30-53, section 1.2 |
| H2 | No skills at all; 12 commandless skills (including all of guide levels 4-6) unreachable from help | help.md:3 contract is "/sc commands"; section 1.3 |
| H3 | Six listed descriptions describe old behavior (`implement`, `reflect`, `task`, `workflow`, `brainstorm`, `troubleshoot`) | help.md:33, 42, 46, 50, 52, 53 vs current frontmatter |
| H4 | No "which to use when" guidance, no levels, no mix-up table; nothing points at the guide or `/sc:recommend` | whole file |
| H5 | 75 lines of flag reference (help.md:55-129) that is not routing and partly disagrees with the plugin copy (plugins copy says `--think` "enables Sequential", src copy does not) | diff of the two files, lines 84-85 |
| H6 | Self-admitted manual maintenance (help.md:149) with no generator or test | no test references help.md (grep of `tests/`) |
| H7 | Built-in `/code-review` and `/security-review` used by the guide's PR flow are absent | GUIDE:193-194 |

### 3.2 Gaps in `/sc:recommend`

| # | Gap | Evidence |
|---|---|---|
| R-1 | Never reads a workflow document; routing order and safe defaults exist nowhere in its inputs | section 2.4 |
| R-2 | Output is one delegation (cap 3 alternatives), not an ordered workflow | SKILL.md:34, 137-154; surface-enumeration.md:96-99 |
| R-3 | Tier rule prefers `/sc:*` and calls commandless skills "rare", which steers away from `/prd`, `/task-builder`, `/task`, `/roadmap`, `/tech-research` | heuristics:58-62, 95 |
| R-4 | Native-first scope rule ("3 files or fewer, native almost always wins") conflicts with the guide's hard limit (more than 1 source file or more than 5 edits needs a plan) | heuristics:38 vs GUIDE:20 |
| R-5 | Rubric names `/sc:tasklist` as the roadmap-to-tasklist tool | heuristics:27 vs GUIDE:232 |
| R-6 | Classifier key `spec-generation` covers "spec, TDD, or PRD" and its cached row routes to `/sc:spec-panel` (critique only) | prompts.py:55; lookup.yaml:6-29 |
| R-7 | Classifier has no key for PR/review flow, small change, feature build, resume, or documentation; it is a static mapping despite the skill's anti-static stance | prompts.py:28-39 |
| R-8 | Cache is stale and inert; stale row designs would be repopulated | section 2.7 |
| R-9 | Surface Glob is IronClaude-repo-only (`src/superclaude/...`); consumer projects with a global install see nothing | section 2.5 |
| R-10 | R2 forbids recommending tools not in the enumerated surface, so Claude Code built-ins used by the guide (`/code-review`, `/security-review`) can never be recommended; R4 exempts only Read/Grep/Glob/Edit/Write/Bash/TodoWrite/WebFetch/WebSearch | SKILL.md:249-264 |
| R-11 | R1 checks flag existence, not safe defaults (`/sc:pr-submit --monitor 1`, `/sc:auggie-review --no-post-pr`, `/sc:reflect --no-promote`) | SKILL.md:245-247; GUIDE:237-242 |
| R-12 | The Phase-0 hook hardcodes the same Glob list; any enumeration change must be mirrored there and in `prompts.py::COLD_PATH_RUNBOOK` (three copies of one rule) | sc-recommend-phase0.sh:42-46; prompts.py:122-125; SKILL.md:69-72 |

### 3.3 Recommended single-source design

Principle: the guide owns "which tool, in which order, with which safe flags". Live enumeration owns "does it exist and what are its exact flags". Neither help nor recommend restates the guide's workflows.

1. **Put the guide inside IronClaude source.** Proposed path: `src/superclaude/core/HOW-WE-WORK.md` (or under `docs/user-guide/` with a copy rule). `src/superclaude/core/` is already installed for every user: `install_core.py:19, 30, 39` copies every `src/superclaude/core/*.md` to `~/.claude/` [CODE-VERIFIED], so the guide would land at `~/.claude/HOW-WE-WORK.md`, a stable path both commands can Read in any project. Caveat: anything in `core/` may also be pulled into session context by the core loader, which would cost tokens every session (UNVERIFIED; check how `~/.claude/CLAUDE.md` imports core files before choosing this path). Putting it under `src/` means it ships with `superclaude install` and is readable in consumer projects; a `docs/` path would not be installed (UNVERIFIED for pip packaging, but `MANIFEST.in` includes `docs *.md` only for the sdist).
2. **Make the guide machine-readable at one point.** Add one fenced table or YAML block (for example "routing table": level or intent, ordered steps, mandatory safe flags, mix-up pairs) inside the guide. Both consumers read that block; the prose stays for humans. This avoids a second data file that could drift.
3. **`/sc:help` becomes: compact inventory + pointer.** Replace the static 22-row table with an instruction to Glob the installed surface at run time (`~/.claude/commands/sc/*.md`, `~/.claude/skills/*/SKILL.md`, and, when present, `src/superclaude/...`), print name plus frontmatter `description` grouped as "Commands" and "Skills", then print the guide's level table (section 1 of the guide) by reading it, and end with "For which-to-use-when see <guide path>; unsure? run `/sc:recommend`". Drop or move the 75-line flags block to a pointer at `FLAGS.md`. This keeps help.md well under the 200-line lint warning and removes H1, H2, H3, H6 permanently. A static fallback list could be generated by a Makefile target instead, if a no-tool help is preferred (design choice for the user).
4. **`/sc:recommend` reads the guide as a ref.** Add the guide to Phase 0 as a mandatory Read before auggie (and to the hook text and `COLD_PATH_RUNBOOK`). Change Phase 1 so the guide's level table and hard limit take priority over the native-first scope rule, and change Phase 2 so it can emit an ordered workflow (numbered paste-ready steps) when the guide maps the request to a multi-step workflow. Keep R1/R2 verification against live files for every step, and add an R4-style exemption for named Claude Code built-ins listed in the guide. Add an R1 extension: when the guide names a safe-default flag for a command, the prompt must include it.
5. **Fix enumeration roots.** Enumerate the installed locations (`~/.claude/commands/sc/`, `~/.claude/skills/`, project `.claude/`) in addition to `src/superclaude/`, in SKILL.md, refs/surface-enumeration.md, the hook, `prompts.py`, and `cache.py::_SURFACE_GLOBS` / `dispatch.py` default base.
6. **Cache.** Either retire the hot path for now (delete the 4 rows; the loader already treats them as dead) or rebase the classifier keys on the guide's levels and workflows and include the guide's hash in `surface_hash` so a guide edit invalidates the cache. Removal of the cache rows is a proposed removal for the user to adjudicate (see section 6).
7. **Rubric edits.** In `refs/delegation-vs-native-heuristics.md`, remove the "skills without a command are rare" claim (line 61), replace `/sc:tasklist` at line 27 with `/roadmap` plus `/task-builder`, and replace line 38's scope rule with a pointer to the guide's hard limit.

---

## 4. Mirror and duplicate copies

| Copy | Tracked? | What generates it | What reads it | Same as src? | Verdict |
|---|---|---|---|---|---|
| `src/superclaude/commands/*.md`, `src/superclaude/skills/sc-recommend/**` | Yes | Hand-edited | Everything below | n/a | **Source of truth.** `CONTRIBUTING.md:42` calls `src/superclaude/` "source of truth for skills/agents/commands"; `CLAUDE.md:18` says `.claude/` is gitignored sync-dev output. |
| `.claude/commands/sc/*.md`, `.claude/skills/**`, `.claude/hooks/*.sh` | No (gitignored; `.gitignore:120-121` keeps only `settings.json`) | `make sync-dev` (Makefile:109-162) copies src to `.claude/`; skips `README.md` and `__init__.py` for commands (Makefile:132-135) | Claude Code during IronClaude development; `make verify-sync` (Makefile:166-351) checks drift in CI (`quick-check.yml:53`) | Not present in snapshot | Generated. Never edit. `scripts/precommit_block_claude_mirrors.sh` rejects staged `.claude/{skills,agents,commands,hooks,templates}` paths. |
| `plugins/superclaude/commands/*.md` (27 files) and `plugins/superclaude/skills/` (3 skills) | Yes | No generator found that writes into `plugins/` from `src/`. `scripts/build_superclaude_plugin.py:16-17, 75-76` reads **from** `plugins/superclaude` into `dist/plugins/superclaude`; `make sync-plugin-repo` (Makefile:73-87) rsyncs `dist/` to `../SuperClaude_Plugin`. | (1) plugin build; (2) `install_commands.py::_get_commands_source` (lines 92-122) uses `plugins/superclaude/commands` only as a fallback when the package `commands/` dir is missing, which in a source checkout means never because `src/superclaude/commands` exists; (3) `MANIFEST.in` includes `plugins/superclaude` in the sdist | `recommend.md` identical to src. `help.md` differs at lines 84-85 only (flag text). 17 src commands are missing from it (adversarial, auggie-review, cleanup-audit, cli-eval, cli-portify, init-lite, post-release, pr-submit, release-split, review-translation, roadmap, swarm-wizard, tasklist, tdd, validate-roadmap, validate-tests, README). | **Hand-maintained, partially stale plugin packaging.** It is not auto-synced. If help/recommend change in src, either copy them here by hand or decide to retire this tree (the plugin manifest `.claude-plugin/plugin.json` is name `sc`, version 4.3.0). |
| Root `commands/sc-*.md` (28 files), root `agents/sc-*.md`, root `skills/` | Yes | `scripts/sync_from_framework.py` (pulls the upstream SuperClaude_Framework repo and applies `sc-` filename prefixes, lines 1-18, 174-250, 444-445; generates plugin.json from `commands/sc-*.md` at lines 334-342). Not in the Makefile, but **run by CI**: `.github/workflows/pull-sync-framework.yml:3-6, 60` runs it on a 6-hourly cron and on manual dispatch, when the upstream framework head has moved (line 35). Whether that workflow is enabled on the IronClaude fork and whether it commits its output is UNVERIFIED (later steps of the workflow not read). | Only `sync_from_framework.py` itself. No install, test, or build code reads `commands/sc-*.md` (grep of `*.py *.sh *.toml *.yml *.yaml *.json Makefile` outside `.dev/` found only the script's own generator line). | No. `commands/sc-recommend.md` is the 1011-line pre-rewrite recommender ("Ultra-intelligent command recommendation engine", Turkish examples, `/sc:sc:recommend` double prefix). `commands/sc-help.md` has `/sc:sc:sc:help` header text and the old list. `commands/sc-README.md` claims `plugins/` is the edit source. | **Stale upstream-sync artifact, mirroring the upstream SuperClaude_Framework, not IronClaude's `src/`.** Any hand edit here could be overwritten by the sync workflow. An earlier reflect run already flagged the orphan `commands/sc-reflect.md` for a human disposition decision (`.dev/brainstorms/20260604-041249-pr133-reflect-remediation/reflect-pre/return-contract.yaml:27`). Candidate for removal (section 6). |
| `.claude/cache/sc-recommend-lookup.yaml` | Yes (gitignore exception `.gitignore:123-125`) | `superclaude recommend cache put` via `LookupCache.save()` (atomic write, `cache.py`) | `dispatch.py` hot path; `tests/recommend/conftest.py` uses a tmp copy, not this file | n/a | Runtime state committed to git. Stale (section 2.7). |

**Edit rule:** make every change in `src/superclaude/` only, then `make sync-dev` locally. Additionally decide, per change, whether `plugins/superclaude/commands/{help,recommend}.md` must be hand-copied (it is not generated, and `make verify-sync` does not check it). Do not edit root `commands/sc-*.md`.

**Install quirk found [CODE-VERIFIED]:** `install_commands.py:37` globs `*.md` in the command source with no README exclusion, so `superclaude install` copies `src/superclaude/commands/README.md` into `~/.claude/commands/sc/README.md`, where Claude Code exposes it as a `/sc:README` command. This session's own skill list shows `sc:README: SuperClaude Commands`, consistent with that. `list_available_commands` (line 139) and `list_installed_commands` (line 159) do exclude README, so the installer reports one fewer than it installs. The README's content is also stale: it lists 4 commands and says to edit `plugins/` first (README.md:7-20), the reverse of `CONTRIBUTING.md:42`. Any help redesign should either exclude README from install or rewrite it.

---

## 5. Inbound references (whole snapshot)

Searched with grep over `/tmp/ic-master` excluding `.git`. `.dev/` hits are historical artifacts; counted, not listed.

| Scoped file | Code, test, install references | Doc and prompt references | `.dev/` hits |
|---|---|---|---|
| `src/superclaude/commands/help.md` (`/sc:help`) | None in code or tests. Installed by `install_commands.py` (all `*.md`). Linted by `make lint-architecture` size checks. | `src/superclaude/core/CLAUDE.md:100` (installed to every user, points sessions at `/sc:help`); `docs/user-guide/commands.md`; `docs/user-guide/modes.md`; `docs/reference/suggested-commands.md:143`; `docs/reference/commands-list.md`; mirrors `plugins/superclaude/commands/help.md`, `commands/sc-help.md`, `commands/sc-recommend.md` | 430 files mention `sc:help`; 9 mention `commands/help.md` |
| `src/superclaude/commands/recommend.md` (`/sc:recommend`) | `tests/unit/test_cli_doctor.py:33-46, 78` (doctor checks recommend command needs `sc-recommend` skill); `tests/unit/test_cli_install.py:221-232` (install payload includes `sc-recommend` skill) | `docs/user-guide/commands.md:97`; `docs/reference/commands-list.md:54` (calls it `/recommend`); `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md:62, 93, 110, 268` and `visual-architecture-summary.md:316, 328, 461, 468` (both name a non-existent `sc:recommend-protocol` skill, stale); `PROJECT_INDEX.md:57, 210` (also `sc-recommend-protocol`, stale); the guide (GUIDE:223) | 47 |
| `src/superclaude/commands/README.md` | `install_commands.py:37` installs it (quirk above). `tests/cli/test_init_lite.py:123` expects a `.claude/commands/README.md` surface in a synthetic fixture project (a fixture, not this file). | `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`; mirror `commands/sc-README.md` | 16 |
| `src/superclaude/skills/sc-recommend/**` | `src/superclaude/cli/recommend/prompts.py` (runbook names `refs/*.md`); `tests/agents/test_tavily_tool_parity.py:5, 14` (parses SKILL.md `allowed-tools`); `tests/unit/test_cli_install.py:224-232`; `tests/unit/test_cli_doctor.py`; `make lint-architecture` Check 1/2 (command to skill pairing, utility skill without `-protocol` suffix allowed); the cache row `source_path` (lookup.yaml:87) | `.claude/settings.json:17` (hook description cites SKILL.md Phase 0) | 53 |
| `.claude/cache/sc-recommend-lookup.yaml` | `src/superclaude/cli/recommend/commands.py:26` (`_DEFAULT_CACHE`), `models.py:32`; `tests/recommend/conftest.py:18` (tmp path of same name); `.gitignore:125` | none | 34 |
| `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` | `src/superclaude/cli/install_hooks.py:69-78`; `tests/cli/test_install_hooks.py:96`; `.claude/settings.json:21` | `src/superclaude/commands/recommend.md:60`; `plugins/superclaude/commands/recommend.md:60` | 43 |
| `plugins/superclaude/commands/{help,recommend}.md` | `scripts/build_superclaude_plugin.py:16, 75-76`; `install_commands.py:116-120` (fallback); `MANIFEST.in` | none found | not counted |
| `commands/sc-help.md`, `commands/sc-recommend.md`, `commands/sc-README.md` | `scripts/sync_from_framework.py:336-342`, run by `.github/workflows/pull-sync-framework.yml:60` (cron) | none found outside `.dev/` | 1 reflect record flags the sibling `commands/sc-reflect.md` as orphaned |

Tests that would break or need updating if help/recommend change: `tests/unit/test_cli_doctor.py` and `tests/unit/test_cli_install.py` (only if the skill name `sc-recommend` changes), `tests/agents/test_tavily_tool_parity.py` (only if `allowed-tools` changes), `tests/cli/test_install_hooks.py` (only if the hook script is renamed or removed), `tests/recommend/*` (if cache schema or dispatch logic changes). No test asserts help.md content.

---

## 6. Proposed removals (each for the user to adjudicate)

- **Remove:** help.md:55-129 flag reference block. **Why:** not routing content, duplicates `FLAGS.md`, already drifted from the plugin copy, and pushes help toward the 200-line lint warning. Replace with a one-line pointer.
- **Remove:** help.md:30-53 static command table. **Why:** 21 of 43 commands missing and 6 stale descriptions; replace with run-time enumeration or a generated list.
- **Remove:** the 4 rows in `.claude/cache/sc-recommend-lookup.yaml`. **Why:** already discarded at load because the surface hash changed; two rows encode routing that contradicts the guide.
- **Remove or rewrite:** `refs/delegation-vs-native-heuristics.md` lines 27, 38, 61. **Why:** they contradict the guide (sections 3.2 R-3 to R-5).
- **Remove (or exclude from install):** `src/superclaude/commands/README.md` as an installed `/sc:README` command. **Why:** it is installed as a fake command and its content is stale and contradicts `CONTRIBUTING.md:42`.
- **Remove (decision needed, outside routing scope):** root `commands/sc-*.md`. **Why:** stale upstream copies with broken `/sc:sc:` prefixes, unread by any install or test code; but a CI sync workflow writes them, so removal also means disabling or rescoping `pull-sync-framework.yml`.

## 7. Open questions and unverified items

1. UNVERIFIED: live behavior of `/sc:recommend` on the guide's workflows; section 2.5 is derived from code and rubric, not a run.
2. UNVERIFIED: whether `uv run superclaude recommend dispatch` works from a consumer project cwd.
3. UNVERIFIED: whether files placed in `src/superclaude/core/` are auto-imported into every session (token cost) or only copied to `~/.claude/`.
4. UNVERIFIED: whether `pull-sync-framework.yml` is active on the IronClaude fork and commits to `commands/`.
5. Decision for the user: should `/sc:help` stay tool-free (static list kept current by a generator plus a test) or become a run-time Glob of the installed surface? Both remove the drift; the run-time version needs no generator but costs a few tool calls.
6. Decision for the user: keep or retire `plugins/superclaude/` (hand-maintained, 17 commands behind, not checked by `verify-sync`).
7. Content fix noted in passing: `src/superclaude/commands/brainstorm.md:175` names a `/sc:task-builder` command that does not exist (the skill is `/task-builder`).

## Summary

`/sc:help` is a stale static list that covers half the commands and none of the skills the guide relies on. `/sc:recommend` has sound anti-fabrication machinery (live Glob, Read-verify, flag checks) but no workflow knowledge: it never reads a routing document, emits single delegations rather than ordered workflows, prefers `/sc:*` commands and native edits in exactly the places the guide says otherwise, only enumerates the IronClaude repo's own `src/` tree, and carries a dead, guide-contradicting cache. The cleanest consolidation is to move the guide into `src/superclaude/` with one machine-readable routing block, have `/sc:help` print a live inventory plus the guide's level table and a pointer, and have `/sc:recommend` read the guide as a mandatory Phase 0 ref that governs order and safe flags while live files govern existence and flags. All edits go in `src/superclaude/` (plus `.claude/settings.json` if the hook changes), with a deliberate decision on the hand-maintained `plugins/` copy.
