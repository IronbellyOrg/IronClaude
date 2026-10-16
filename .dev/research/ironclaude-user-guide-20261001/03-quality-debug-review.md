# Research: IronClaude Quality, Debug, Review, Test, and PR Skills (Quick-Reference Source)
**Scope:** /Users/cmerritt/GFxAI/IronClaude/src/superclaude/skills (troubleshoot, reflect, adversarial, bare-review, auggie-review, confidence-check, brainstorm, crash-recovery, recommend, cleanup-audit, release-split, pr-submit, swarm-wizard) and src/superclaude/commands (troubleshoot, reflect, adversarial, spec-panel, business-panel, auggie-review, analyze, test, git, improve, cleanup, research, brainstorm, select-tool)
**Status:** Complete
**Date:** 2026-10-01
**Citation base:** `M:` = /Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/ (current master worktree of the same repo; see Section 0 for why)
---

## 0. Source Version Note (READ FIRST)

The requested checkout `/Users/cmerritt/GFxAI/IronClaude` is on branch `feature/task-builder-merge` at commit `58bdef20` (2026-06-08). It is about four months behind `origin/master`. The current master is checked out in the sibling git worktree `/Users/cmerritt/GFxAI/IronClaude-tier-tools` (branch `feat/tier-tools-update`, commit `50a8c7f4`, 2026-09-30, "Merge pull request #250"), verified via `git worktree list` and `git branch -a --contains` (both show the same repository).

| Evidence | Result |
|---|---|
| `sc-pr-submit-protocol`, `sc-swarm-wizard-protocol`, `commands/pr-submit.md`, `commands/swarm-wizard.md` | ABSENT in the June checkout; PRESENT on master worktree |
| `~/.claude/skills/sc-pr-submit-protocol`, `~/.claude/skills/sc-swarm-wizard-protocol` | ABSENT (user-level skill dir does not hold them); a project-level copy exists at `/Users/cmerritt/GFxAI/IC-Harness/.claude/skills/sc-pr-submit-protocol` |
| SKILL.md byte comparison June vs master | 10 of 11 requested skills DIFFER (only `confidence-check` identical); e.g. troubleshoot 548 vs 675 lines, reflect 1797 vs 2015, bare-review 221 vs 80 |
| Command byte comparison June vs master | 10 of 14 commands DIFFER (`business-panel`, `analyze`, `test`, `git` identical) |

**Decision for this guide:** a human quick-reference must describe what the user actually runs today, so all citations below use the master worktree. Citation prefix `M:` means `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/`. This is logged as a deviation from the literal source path in Section 4.

---

## 1. Skill Reference Table

### 1.1 Debugging

| Skill | Problem it solves | Trigger situation | Tiers/flags that matter | Cost | Exact invocation | Evidence |
|---|---|---|---|---|---|---|
| `/sc:troubleshoot` (skill `sc:troubleshoot-protocol`) | Diagnoses a concrete symptom (bug, build, performance, deployment, security, test) with every claim grounded in a real file:line; small bugs stay cheap, hard ones fan out | Broken build, runtime error, stack trace, failing or flaky test, "this used to work" | **Tier 1** always: one `root-cause-analyst` hypothesis plus `confidence-calibrator` re-grade. **Tier 2** auto on confidence below 0.85, multi-domain, intermittent, security below 0.95, or `--depth deep`: 2-4 parallel specialist agents, then `sc:adversarial-protocol` debate if 2 or more strong fixes. **Tier 3** only with `--fix` AND user accepts: `task-builder` builds an MDTM task. Other flags: `--type`, `--depth quick/standard/deep`, `--scope`, `--no-escalate` (cap at Tier 1), `--no-doc-discovery`, `--no-mcp`. Diagnose-only by default: no code change without `--fix` plus confirmation | Tier 1 about 3-6k tokens, 1-3 min; Tier 2 adds 15-60k tokens, 4-15 min; Tier 3 adds 20-40k tokens, 5-10 min | `/sc:troubleshoot "<symptom>" [--type test] [--depth deep] [--scope <path>] [--fix]` | M:commands/troubleshoot.md:8, :37-44, :48-60, :73-77, :187-195; M:skills/sc-troubleshoot-protocol/SKILL.md:18-24, :98-110 |

Troubleshoot notes for the guide:
- Output lands in `.dev/troubleshoot/<slug>-<timestamp>/` (REPORT.md, hypothesis cards, audit.log) (M:commands/troubleshoot.md:56).
- Return flags `test_is_wrong` and `behavior_is_documented` tell you when the fix belongs in the test or the docs, not the code (M:skills/sc-troubleshoot-protocol/SKILL.md:49-51, :82-94).
- Tier 1 always runs first, even with `--depth deep`; Tier 3 task file is never auto-executed; you run `/task` yourself and then `/sc:reflect --type task --validate` as the pre-commit gate (M:commands/troubleshoot.md:177-183, :191-193).

### 1.2 Reflection (plan check and work audit)

| Skill | Problem it solves | Trigger situation | Tiers/flags that matter | Cost | Exact invocation | Evidence |
|---|---|---|---|---|---|---|
| `/sc:reflect` (skill `sc:reflect-protocol`) | Independent, citation-grounded audit that a plan covers its spec (UC-1) or that finished work matches its plan (UC-2), avoiding single-agent self-review bias | **UC-1 pre**: you have a spec plus a tasklist and have not started. **UC-2 post**: work is done and you have a diff or task log | **UC-1** `--mode pre --spec <path>` (spec required; tasklist recommended); ships at Tier 1 if confidence at least 0.85 AND `coverage_pct` at least `--coverage-floor` (default 0.90). **UC-2** `--mode post --diff <ref>` or `--task-log`; classifies every divergence as Authorized / Necessary / Drift / Regression; runs scoped tests/linters by default (`--no-verify` disables). **Tier 1** single card; **Tier 2** 2-3 heterogeneous reviewers (different model classes) merged via `sc:adversarial-protocol` (forced by `--depth deep` or `--tier 2`); **Tier 3** `--remediate` plus user accept hands off to `task-builder`. Legacy `--type task --analyze` = pre, `--type task --validate` = post | Tier 1 about 3-6k tokens, 1-3 min (UC-1 example quoted as 200-500 tokens to save 5-50k); Tier 2 adds 15-60k, 4-15 min; Tier 3 adds 20-40k, 5-10 min | `/sc:reflect --mode pre --spec docs/spec.md --tasklist <tasklist>` and `/sc:reflect --mode post --diff HEAD~1..HEAD --tasklist <tasklist> [--depth deep] [--remediate]` | M:commands/reflect.md:10, :25-35, :39-62, :77-107, :133-137, :174-207, :269-277; M:skills/sc-reflect-protocol/SKILL.md:3 (skill description) |

Reflect gotchas for the guide:
- **UC-2 moves files by default.** Wave 7 promotion moves the validated work-unit folder to its done destination when the strict gate passes. Use `--no-promote` for review-only or `--promote-dry-run` to preview (M:commands/reflect.md:103-106, :221-236, :248).
- Output goes to `.dev/reflect/<mode>-<slug>-<ts>/`; it refuses to write under `.claude/skills|agents|commands/` (M:commands/reflect.md:35, :92).
- Mixing legacy and new grammar (for example `--type task --analyze --mode post`) is a STOP condition (M:commands/reflect.md:118).
- PR detection-contract readiness is NOT a reflect audit; use the CLI `superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <n>` (M:commands/reflect.md:64-73).

### 1.3 Multi-agent panels and debate (several perspectives)

| Skill | Problem it solves | Trigger situation | Tiers/flags that matter | Cost | Exact invocation | Evidence |
|---|---|---|---|---|---|---|
| `/sc:adversarial` (skill `sc:adversarial-protocol`) | Picks or merges the best of 2-10 competing artifacts through structured debate, scoring, and a provenance-annotated merge | You have two or more drafts/plans/designs, or want several models/personas to each draft one and then merge | **Mode A** `--compare a.md,b.md` (2-10 files). **Mode B** `--source <file> --generate <type> --agents model[:persona[:"instruction"]],...`. **Pipeline** `--pipeline "<dag>"` or `@file.yaml` (with `--pipeline-resume`). `--depth quick/standard/deep` = 1/2/3 debate rounds; `--convergence` (default 0.80); `--blind` strips model names; `--interactive`; `--focus` | No token figure in the command file; scales with depth (rounds) and variant count. UNVERIFIED numeric cost | `/sc:adversarial --compare draft-a.md,draft-b.md --depth standard` | M:commands/adversarial.md:13-17, :21-33, :55-71, :75; M:skills/sc-adversarial-protocol/SKILL.md:334, :1082-1083 |
| `/sc:spec-panel` | Expert-panel critique of a specification (Wiegers, Adzic, Cockburn, Fowler, Nygard, Newman, Hohpe, Crispin, Gregory, plus Whittaker adversarial attacks) producing prioritized fixes and an improved spec | A spec, PRD, or TDD exists and needs a quality review before it drives work | `--mode discussion/critique/socratic`; `--focus requirements,architecture,testing,compliance,correctness` (correctness adds a State Variable Registry and a Guard Condition Boundary Table that hard-blocks synthesis if incomplete); `--experts`; `--iterations N`; `--format standard/structured/detailed`. Does NOT create a spec from raw instructions | No figure stated. UNVERIFIED | `/sc:spec-panel @spec.md --mode critique --focus requirements,architecture` | M:commands/spec-panel.md:22-24, :41-83, :187-190, :210, :274, :318, :398-424 |
| `/sc:business-panel` | Business-strategy panel (Christensen, Porter, Drucker, Godin, Kim and Mauborgne, Collins, Taleb, Meadows, Doumont) analyzing a document through competing frameworks | Strategy, market, product-positioning, or risk questions (not code) | `--mode discussion` (default) / `debate` / `socratic` / `adaptive`; `--experts "a,b,c"`; `--focus <domain>` | No figure stated. UNVERIFIED | `/sc:business-panel @doc.md --mode debate` | M:commands/business-panel.md:20-40, :56-72 |
| `sc-bare-review` (skill only, NO slash command) | Gets 2-4 "bare" unscaffolded reviews from different EXTERNAL (non-Anthropic) models to catch edge cases structured reviewers miss; every output tagged `suspect: true` | Called by other commands (troubleshoot, reflect, auggie-review, adversarial); not user-invoked | `--reviewers 2-4` (default 3); `--transport openai_compat` needs env `T2ProxyUrl`, `T2ProxyKey`, `T2Model0N`; `--transport stub` is a dry run. Fewer than 2 successes = `failed` | External proxy calls; Claude side is a thin caller (model: sonnet). No token figure | `superclaude swarm run --lens bare-review --target <file> --output <dir> --transport openai_compat` (what the skill runs) | M:skills/sc-bare-review/SKILL.md:3, :5, :14-25, :29-39, :50-55, :62-66 |

Panel notes for the guide:
- Adversarial will not validate domain correctness, will not execute the merge, and needs at least 2 variants (M:commands/adversarial.md:165-172).
- Spec-panel lists integration with adversarial: run adversarial after the panel to stress-test (M:commands/adversarial.md:178; M:commands/spec-panel.md:386).
- Bare-review hands off via `recommended_next_command: "/sc:adversarial --compare <existing>,<bare...> --suspect-source <bare...>"`, but no `--suspect-source` flag was found in M:commands/adversarial.md or M:skills/sc-adversarial-protocol/SKILL.md (grep, zero hits). See Section 4.

### 1.4 Code review, multi-model swarm, and PR submission

| Skill | Problem it solves | Trigger situation | Tiers/flags that matter | Cost | Exact invocation | Evidence |
|---|---|---|---|---|---|---|
| `/sc:auggie-review` (skill `sc:auggie-review-protocol`) | Code review of a PR, local diff, or file snapshot using the `auggie` CLI's indexed retrieval for bugs, architecture risks, and anti-patterns; findings validated against real files | Before or after opening a PR; reviewing a branch diff; auditing a subtree. EXPLICIT ONLY, never auto-activates | Target: PR number/URL, `--diff <base>...HEAD`, or `--snapshot <path>`. `--depth quick` (auggie single pass, about 2 min) / `standard` (plus Claude synthesis, about 5 min) / `deep` (per-persona passes, about 10-15 min). `--focus security,architecture,quality,performance,anti-patterns,tests,docs,all`. **`--post-pr` is ON by default for PR targets and posts with NO confirmation**; use `--no-post-pr` to keep it local. `--remediation-offer` default on | Time figures above; token cost reduced by offloading to auggie (no number given) | `/sc:auggie-review --diff origin/master...HEAD --no-post-pr` or `/sc:auggie-review 62 --depth deep` | M:commands/auggie-review.md:8, :15-21, :25-31, :35-55, :78 |
| `/sc:pr-submit` (skill `sc:pr-submit-protocol`) | Opens a PR on your fork and (optionally) arms an in-session monitor that waits for the Augment Code bot review, re-grades and verifies each finding, sends verified ones to `/sc:troubleshoot`, and at higher levels fixes, pushes, replies, and resolves | Ready to open a PR and want the bot review handled | `--monitor` ordinal is a capability ceiling: **0** open PR only; **1** arm + poll + propose (no edits); **2 (DEFAULT)** also fixes locally and HALTS before push; **3** full loop fix, push, reply, resolve. `--max-rounds` (default 2, hard cap 5); `--poll-interval` (min 30s); `--timeout` 600; `--silence-timeout` 300; `--resume <run-log.jsonl>`. Will not push to default/protected branch or upstream parent | Not stated. UNVERIFIED | `/sc:pr-submit --monitor 1 --head feature/x --title "..." --body "..."` | M:commands/pr-submit.md:3, :8, :15-19, :23-32, :35-41, :45-56, :74-80; M:skills/sc-pr-submit-protocol/SKILL.md (186 lines) |
| `/sc:swarm-wizard` (skill `sc:swarm-wizard-protocol`) | Plain-language guided front door to the `superclaude swarm` multi-model review CLI: interviews you, picks lens and flags, always runs a safe stub dry run first, then offers a real run, monitors, and summarizes | You want a multi-model review but do not know swarm lenses or flags | `--goal`, `--target` (at least 50 non-whitespace bytes), `--real` (needs `T2ProxyUrl`/`T2ProxyKey`/`T2Model01`), `--detached` (tmux), `--advanced`, `--yes`. Lenses: `bare-review` (only stable), `refactor-find`, `edge-case-hunt`, `spec-completeness`, `feasibility-probe`, `troubleshoot-hypothesis`, `doc-completeness` (experimental) | External proxy models; not stated. UNVERIFIED | `/sc:swarm-wizard --goal "find bugs in my code" --target src/auth.py` | M:commands/swarm-wizard.md:8, :28-32, :37-41, :47-55, :82-89; M:skills/sc-swarm-wizard-protocol/refs/cli-contract.md:22-23, :43-51 |

Review notes for the guide:
- Swarm lens to downstream skill mapping: bare-review and edge-case-hunt go to `/sc:adversarial`; spec-completeness to `/sc:reflect`; feasibility-probe to `/sc:research`; troubleshoot-hypothesis to `/sc:troubleshoot`; refactor-find to `/sc:code-review --apply`; doc-completeness to `/sc:document` (M:skills/sc-swarm-wizard-protocol/refs/cli-contract.md:43-49).
- Swarm `--transport` help text wrongly claims `openai_compat` is the default; the lens path default is `stub` (M:skills/sc-swarm-wizard-protocol/refs/cli-contract.md:22).
- After `gh pr create`, the `offer-pr-review.sh` hook offers both `/sc:auggie-review` and `/sc:pr-submit --monitor`; it never arms a monitor itself (M:commands/pr-submit.md:17; M:commands/auggie-review.md:18).
- Conflict with this user's git policy: `--monitor 3` pushes autonomously. Recommend `--monitor 1` or `2` (2 halts before push) unless the user explicitly wants autonomous push (M:commands/pr-submit.md:30-31).

### 1.5 Readiness, exploration, recovery, and routing

| Skill | Problem it solves | Trigger situation | Tiers/flags that matter | Cost | Exact invocation | Evidence |
|---|---|---|---|---|---|---|
| `confidence-check` (skill only; no `/sc:` command file found) | Stops wrong-direction work: scores readiness before implementing | Before writing code or before giving the user any command, flag, path, or step-by-step instruction | 5 weighted checks: no duplicate (25%), architecture compliance (25%), official docs verified (20%), working OSS reference (15%), root cause identified (15%). At least 0.90 proceed; 0.70-0.89 present alternatives and ask; below 0.70 STOP. Lightweight form: verify a single token via `--help`, grep, or file read | Small; the skill cites only the 8-case trigger test (precision/recall 1.000), not a token cost | `Skill confidence-check` (or ask "run a confidence check before implementing X") | M:skills/confidence-check/SKILL.md:3, :12-20, :27-50, :58-104, :119-121 |
| `/sc:brainstorm` (skill `sc-brainstorm-protocol`) | Turns an ambiguous idea into a merged spec via Socratic dialogue, 2-7 parallel proposals, and an adversarial merge, saved as reproducible artifacts | Ambiguous feature idea, unclear requirements, need multiple design options | `--proposals` (default 3; quick caps at 2; deep allows 7); `--depth quick/standard/deep` (passed to adversarial); `--strategy systematic/agile/enterprise/auto` (enterprise implies deep); `--no-codebase`, `--no-research`; `--blind`; `--convergence` 0.75; `--handoff none/design/tasklist/task` (`task` needs task-builder); `--dry-run`; `--resume-from` | Not stated; quick depth cap is labelled a "cost guardrail". UNVERIFIED numeric | `/sc:brainstorm "<topic>" --depth standard [--handoff task]` | M:commands/brainstorm.md:3, :14-19, :34-41, :45-71, :134 |
| `sc-crash-recovery` (skill only; no command file) | Read-only forensic report of every in-flight initiative and concrete resume commands after a crash, reboot, or lost session | "Where was I", reboot, interrupted `/sc:task`, `superclaude sprint`, or roadmap run | `<project-path>` (default cwd); `--since <duration>` (default 72h); `--all` fleet sweep of `~/workspace/`. Read-only by `allowed-tools` (no Edit/Write); fans parallel investigators | Parallel subagents; no number given. Warns before `--all` over 6 projects | "the session crashed, where was I?" or `Skill sc-crash-recovery` with `--since 24h` | M:skills/sc-crash-recovery/SKILL.md:3-4, :10-12, :18-34, :38-58 |
| `/sc:recommend` (skill `sc-recommend`) | Produces one paste-ready prompt routing your goal to the right local skill/command/agent, or tells you plain native tools are enough | You do not know which command fits, or a goal could map to several skills | Default local mode; `--plugin` searches plugin marketplaces and community repos; `--minstar N` (plugin mode, default 500); `--eval <mode>` | Not stated | `/sc:recommend "<goal>"` | M:commands/recommend.md:3, :8, :18-38; M:skills/sc-recommend/SKILL.md:22-32, :118 |
| `/sc:cleanup-audit` (skill `sc-cleanup-audit-protocol`) | Read-only, evidence-gated repo audit recommending DELETE/CONSOLIDATE/MOVE/FLAG/KEEP; never deletes without grep proof of zero references | Before a cleanup, after a large change, before a release | `--pass surface` (Haiku, Pass 1) / `structural` (Sonnet 8-field profiles) / `cross-cutting` (duplication matrix) / `all`; `--batch-size`; `--focus infrastructure/frontend/backend/all`. Reports to `.claude-audit/`; checkpoint resume | Not stated; Haiku for the cheap pass | `/sc:cleanup-audit --pass all --focus all` | M:commands/cleanup-audit.md:3, :31-43, :53, :74-77, :91-99 |
| `/sc:release-split` (skill `sc-release-split-protocol`) | Neutral analysis of whether a release should be split into two, with adversarial validation and fidelity check between original and split specs | A release spec feels too big or has natural seams | `--depth deep`, `--interactive`, `--agents model:persona[:"instr"]`, `--resume-from`, `--no-split`, `--output` | Not stated | `/sc:release-split path/to/release-spec.md [--depth deep]` | M:commands/release-split.md:3, :19-45 |

### 1.6 Lightweight utility commands (single-pass, no tier system)

These are thin command files without a protocol skill, tiers, evidence-validator gate, or task-builder handoff. Cost is not stated in any of them (UNVERIFIED).

| Command | Problem it solves | Trigger situation | Flags that matter | Exact invocation | Evidence |
|---|---|---|---|---|---|
| `/sc:analyze` | Read-only quality/security/performance/architecture analysis report | No specific symptom yet; want a health read of a module | `--focus quality/security/performance/architecture`, `--depth quick/deep`, `--format text/json/report`. Will not modify code | `/sc:analyze src/auth --focus security --depth deep` | M:commands/analyze.md:3, :22, :68, :97-101 |
| `/sc:test` | Runs tests with coverage and a quality report | After a change; checking coverage | `--type unit/integration/e2e/all` (e2e uses Playwright MCP), `--coverage`, `--watch`, `--fix`. Will not generate new test cases | `/sc:test src/components --type unit --coverage` | M:commands/test.md:3, :22, :43, :74-89, :102-106 |
| `/sc:git` | Git operations with generated commit messages | Committing or merging | `--smart-commit`, `--interactive`. Will not do destructive ops without confirmation | `/sc:git commit --smart-commit` | M:commands/git.md:3, :22, :67, :87-91 |
| `/sc:improve` | Applies quality/performance/maintainability/style improvements | Known code smell, after review findings | `--type quality/performance/maintainability/style`, `--safe`, `--interactive`, `--preview`; has an "AUTO-FIX VS APPROVAL-REQUIRED" section | `/sc:improve src/ --type quality --safe` | M:commands/improve.md:3, :22, :65-89, :102-108 |
| `/sc:cleanup` | Removes dead code and unused imports, tidies structure (this one CHANGES files, unlike cleanup-audit) | After cleanup-audit findings, or targeted dead-code removal | `--type code/imports/files/all`, `--safe` or `--aggressive`, `--interactive`, `--preview` | `/sc:cleanup --type imports --preview` then `/sc:cleanup src/ --type code --safe` | M:commands/cleanup.md:3, :22, :65-89, :102-108 |
| `/sc:research` | Deep web research with adaptive planning | External knowledge gap (library behavior, best practice) | `--depth quick/standard/deep/exhaustive`, `--strategy planning/intent/unified` | `/sc:research "<query>" --depth deep` | M:commands/research.md:3, :25, :112-114 |
| `/sc:select-tool` | MCP tool selection advice by complexity scoring | (historical) | `--analyze`, `--explain` | `/sc:select-tool "<operation>" --analyze` | **REMOVED on master** by commit `3ae238b1` "chore: drop unused commands and sequential/magic/chrome-devtools MCPs"; exists only in the June checkout at /Users/cmerritt/GFxAI/IronClaude/src/superclaude/commands/select-tool.md:3, :22. Use `/sc:recommend` instead |

### 1.7 Built-in Claude Code complements (not IronClaude)

These come from Claude Code itself (listed in this session's available skills, not in the IronClaude repo).

| Built-in | What it does | When to use alongside IronClaude | Evidence |
|---|---|---|---|
| `/code-review` | Reviews the current diff or a PR/branch/path for correctness bugs at an effort level (low to max); `--comment` posts inline PR comments, `--fix` applies findings | Fast local bug review before commit; cheaper than `/sc:auggie-review --depth deep` | Session skill listing (Claude Code built-in description); not in IronClaude source |
| `/simplify` | Reviews changed code for reuse, simplification, efficiency and applies fixes; explicitly does NOT hunt bugs | After implementation passes tests, before commit | Session skill listing |
| `/security-review` | Security review of pending changes on the current branch | Any change touching auth, input handling, secrets, or file paths; before PR | Session skill listing |

Note: the swarm lens table references `/sc:code-review --apply` (M:skills/sc-swarm-wizard-protocol/refs/cli-contract.md:44) and bare-review lists `/sc:code-review` as a caller (M:skills/sc-bare-review/SKILL.md:21), but no `commands/code-review.md` exists on master (directory listing grep for "code-review" returned nothing). Whether `/sc:code-review` is a distinct IronClaude command or means the built-in `/code-review` is UNVERIFIED.

---

## 2. Recommended Sequences

Each sequence is assembled from the documented hand-offs and "Related Commands" sections cited. Where the order is this researcher's recommendation rather than a documented chain, it is marked [RECOMMENDED, not documented].

### (a) Bug or failing test

| Step | Command | Why | Evidence |
|---|---|---|---|
| 1 | `/sc:troubleshoot "<error or test name>" --type test` | Tier 1 grounded diagnosis in 1-3 min; auto-escalates to Tier 2 if flaky/intermittent or confidence below 0.85 | M:commands/troubleshoot.md:51, :73-77, :119-128 |
| 2 | Read REPORT.md; check `test_is_wrong` / `behavior_is_documented` | Tells you whether to fix the code, the test, or the docs | M:skills/sc-troubleshoot-protocol/SKILL.md:49-51 |
| 3a (small fix) | Apply the fix yourself, then `/sc:test <target> --coverage` | Confirm the fix [RECOMMENDED, not documented] | M:commands/test.md:22, :74 |
| 3b (multi-file fix) | Re-run with `--fix`, accept the offer | Tier 3: task-builder builds an MDTM task, `/sc:reflect --type task --analyze` reviews it | M:skills/sc-troubleshoot-protocol/SKILL.md:552-558 |
| 4 | `/task <path>` (you run it) | Skill never auto-executes | M:skills/sc-troubleshoot-protocol/SKILL.md:559 |
| 5 | `/sc:reflect --type task --validate` | Pre-commit gate | M:skills/sc-troubleshoot-protocol/SKILL.md:560; M:commands/troubleshoot.md:193 |

Shortcut: `--no-escalate` for a fast second opinion; `--depth deep` when you already know it is hard (M:commands/troubleshoot.md:43, :51-53).

### (b) Hard, ambiguous problem needing several perspectives

| Step | Command | Why | Evidence |
|---|---|---|---|
| 1 | `/sc:brainstorm "<problem>" --depth deep --strategy systematic` | Socratic scoping plus up to 7 parallel proposals merged by adversarial debate; documented example "deployment broke staging at 3am" | M:commands/brainstorm.md:45-70, :86 |
| 2 (if it is a defect) | `/sc:troubleshoot "<symptom>" --depth deep` | Forces Tier 2: 2-4 specialist hypotheses plus adversarial fix debate | M:commands/troubleshoot.md:51, :76; troubleshoot lists brainstorm as upstream for ambiguous symptoms at :203 |
| 3 (competing drafts exist) | `/sc:adversarial --compare a.md,b.md --depth deep --blind` | Scored, documented merge | M:commands/adversarial.md:21-33, :62-71 |
| 4 (spec-shaped output) | `/sc:spec-panel @merged.md --mode critique --focus correctness` | Expert critique plus Whittaker attacks | M:commands/spec-panel.md:22-24, :173-190 |
| Alt | `/sc:swarm-wizard --goal "<goal>" --target <file>` | Different external model families (bare reviews), then adversarial | M:commands/swarm-wizard.md:37-41 |
| Alt (business question) | `/sc:business-panel @doc.md --mode debate` | Strategy rather than code | M:commands/business-panel.md:56-67 |

### (c) Before starting implementation

| Step | Command | Why | Evidence |
|---|---|---|---|
| 1 | `/sc:recommend "<goal>"` (if unsure which workflow) | Picks the smallest delegation that wins | M:skills/sc-recommend/SKILL.md:22 |
| 2 | `/sc:brainstorm "<idea>" --handoff task` (if requirements are fuzzy) | Merged spec, then hands to task-builder | M:commands/brainstorm.md:60, :71; M:skills/sc-brainstorm-protocol/SKILL.md:329 |
| 3 | `/sc:spec-panel @spec.md --mode critique` | Fix spec gaps before they become code | M:commands/spec-panel.md:22, :398 |
| 4 | `/sc:release-split <spec>` (only if the release looks too large) | Neutral split analysis | M:commands/release-split.md:19-26 |
| 5 | `/sc:reflect --mode pre --spec <spec> --tasklist <tasklist>` | UC-1 coverage audit; documented ROI "200-500 tokens to potentially save 5-50k" | M:commands/reflect.md:41, :174-182 |
| 6 | `confidence-check` | Must score at least 0.90 to proceed | M:skills/confidence-check/SKILL.md:12, :119-121 |

### (d) After implementation, before commit

| Step | Command | Why | Evidence |
|---|---|---|---|
| 1 | `/sc:test --coverage` | Run the suite | M:commands/test.md:22 |
| 2 | `/sc:reflect --mode post --diff HEAD --tasklist <tasklist> --no-promote` | UC-2 deviation audit (Drift/Regression) with scoped verification; `--no-promote` avoids the default folder move. NOTE `--diff` accepts "Git ref or path"; whether uncommitted changes are covered is UNVERIFIED | M:commands/reflect.md:44, :85, :97, :103 |
| 3 | `/simplify` then `/code-review` (built-ins) | Cleanup pass, then bug pass [RECOMMENDED, not documented] | Session skill listing |
| 4 | `/security-review` (if security-relevant) | Built-in [RECOMMENDED] | Session skill listing |
| 5 | `/sc:git commit --smart-commit` | Generated commit message | M:commands/git.md:67 |

### (e) Before push and opening a PR

| Step | Command | Why | Evidence |
|---|---|---|---|
| 1 | `/sc:auggie-review --diff origin/master...HEAD --no-post-pr` | Local branch review, nothing posted | M:commands/auggie-review.md:29, :39, :53 |
| 2 | `/sc:cleanup-audit --pass surface` (optional, larger branches) | Read-only stray-file check [RECOMMENDED] | M:commands/cleanup-audit.md:31-53 |
| 3 | Push (only with user approval per this repo's git policy) | IC-Harness CLAUDE.md Git Policy | /Users/cmerritt/GFxAI/IC-Harness/CLAUDE.md "Git Policy" |
| 4 | `/sc:pr-submit --monitor 1 --head <branch> --title "..." --body "..."` | Opens PR and watches the Augment bot review, proposes fixes without edits. Use `--monitor 2` to fix locally and halt before push; avoid `3` unless autonomous push is wanted | M:commands/pr-submit.md:28-32, :38 |
| 5 | `/sc:auggie-review <PR#>` (optional) | Posts review to the PR by default | M:commands/auggie-review.md:28, :51 |

Note: pr-submit's own Wave 2 routes verified findings to troubleshoot: Medium to `--fix`, High/Critical to `--depth deep --fix`, Low/Nit report-only (M:skills/sc-pr-submit-protocol/SKILL.md:132).

### (f) After a crash or lost session

| Step | Command | Why | Evidence |
|---|---|---|---|
| 1 | Say "the session crashed, where was I?" (activates `sc-crash-recovery`), optionally `--since 24h` | Read-only inventory of ALL in-flight initiatives with resume commands | M:skills/sc-crash-recovery/SKILL.md:3, :10-12, :18-30 |
| 2 | For an interrupted `/task`: re-run `/task <task-file>` | Task file checkboxes are the source of truth (task skill resumes) | Session skill listing for `task` ("resume an in-progress task") |
| 3 | For an interrupted adversarial pipeline: `/sc:adversarial --pipeline ... --pipeline-resume` | Manifest checkpoint resume | M:commands/adversarial.md:64 |
| 4 | For an interrupted PR monitor: `/sc:pr-submit --resume <run-log.jsonl>` | Write-ahead run-log reconstruct | M:commands/pr-submit.md:39, :56 |
| 5 | For an interrupted cleanup audit: re-run; checkpoint resume is built in | M:commands/cleanup-audit.md:43 |
| 6 | For brainstorm: `/sc:brainstorm --resume-from <seed-brief>` | Skips Socratic dialogue | M:commands/brainstorm.md:62 |

---

## 3. Hand-offs into task-builder (Tier 3 remediation chains)

| Source skill | Gate flag | Chain | Auto-executes? | Evidence |
|---|---|---|---|---|
| `/sc:troubleshoot` | `--fix` AND REPORT status `success` AND user accepts | Phase A `task-builder` BUILD_REQUEST (template 01, or 02 if more than 3 files or 2 hours) -> Phase B `/sc:reflect --type task --analyze` -> Phase C user runs `/task <path>` -> Phase D `/sc:reflect --type task --validate` before commit | No; never runs `/task`, never commits | M:skills/sc-troubleshoot-protocol/SKILL.md:550-563; M:commands/troubleshoot.md:54, :77, :187-195 |
| `/sc:troubleshoot` (diagnosability) | `--diagnosability-handoff` | Packages the diagnosability (instrumentation) tasklist via task-builder | No | M:skills/sc-troubleshoot-protocol/SKILL.md:606 |
| `/sc:reflect` | `--remediate` AND accept | Warm-start handoff file written, then `task-builder` authors corrective MDTM -> operator runs `/task` -> `/sc:reflect --mode post` re-runs as post-commit gate. Headless (`claude --print`) auto-accepts only for Drift/Necessary; any Regression yields `remediation_task_path: null` | No; authors but never runs `/task` | M:commands/reflect.md:101, :137, :269-277; M:skills/sc-reflect-protocol/SKILL.md:362-364 |
| `/sc:auggie-review` | `--remediation-offer` (default ON) AND user accepts | `/sc:design` -> `task-builder` -> `/sc:reflect --type task --analyze` -> execute -> `/sc:reflect --type task --validate` | Waits for explicit acceptance | M:commands/auggie-review.md:52; M:skills/sc-auggie-review-protocol/SKILL.md:327-328, :345 |
| `/sc:brainstorm` | `--handoff task` | `Skill task-builder --source <output>/merged-requirements.md --template <detected>`; STOPs if task-builder missing | Builds task file only | M:commands/brainstorm.md:60, :71; M:skills/sc-brainstorm-protocol/SKILL.md:106, :329 |
| `/sc:pr-submit` | (indirect) `--monitor >= 1` | Dispatches verified findings to `sc:troubleshoot-protocol` with `--fix` / `--depth deep --fix`; any task-builder use is via troubleshoot. No direct task-builder reference found (grep zero hits) | L2 fixes locally; L3 pushes | M:skills/sc-pr-submit-protocol/SKILL.md:22, :122, :132 |

No direct task-builder handoff found (grep zero hits) in: `sc-adversarial-protocol`, `sc-cleanup-audit-protocol`, `sc-release-split-protocol`, `sc-swarm-wizard-protocol`. `sc-crash-recovery` only references task-builder output folders (`.dev/tasks/to-do/TASK-PRD-*/`) as something to inspect (M:skills/sc-crash-recovery/SKILL.md:113); `sc-recommend` only may recommend it (M:skills/sc-recommend/SKILL.md:34).

---

## 4. UNVERIFIED Items and Gaps

| # | Item | Status | Detail |
|---|---|---|---|
| G1 | Source path deviation | DEVIATION | Cited the master worktree (`IronClaude-tier-tools`, 50a8c7f4, 2026-09-30) instead of the requested `IronClaude` checkout (stale branch `feature/task-builder-merge`, 58bdef20, 2026-06-08). 10 of 11 skills and 10 of 14 commands differ; pr-submit and swarm-wizard exist only on master. If the guide must describe the June branch, every line number needs re-cutting. |
| G2 | Which version the user actually runs | UNVERIFIED | `IC-Harness/.claude/skills/sc-troubleshoot-protocol/SKILL.md` (602 lines) and `sc-reflect-protocol/SKILL.md` (1875 lines) match NEITHER June nor master; `sc-bare-review` and `sc-recommend` copies match master. The installed project copies are a third, intermediate version. `~/.claude/skills` holds none of these skills. |
| G3 | `--suspect-source` flag | UNVERIFIED / likely missing | Bare-review's contract tells you to run `/sc:adversarial ... --suspect-source`, but grep finds no such flag in master adversarial command or skill. |
| G4 | `/sc:code-review` | UNVERIFIED | Referenced by swarm lens table and bare-review callers; no `commands/code-review.md` or `skills/*code-review*` on master. May mean built-in `/code-review`. |
| G5 | `/sc:select-tool` | REMOVED on master | Dropped by commit 3ae238b1. Do not put it in the guide except as "replaced by `/sc:recommend`". |
| G6 | `confidence-check` and `sc-crash-recovery` have no `/sc:` command file | VERIFIED absent | Invoked via the Skill tool or natural-language triggers only; exact user-typed invocation is therefore by description, not a slash command. |
| G7 | Crash-recovery `--all` sweeps `~/workspace/` | GAP for this user | `~/workspace` does not exist on this machine (`ls` failed); the user's repos live in `~/GFxAI/`. `--all` would STOP per the skill's own rule (M:skills/sc-crash-recovery/SKILL.md:30-31). Its `allowed-tools` also hardcode `~/workspace/IronClaude/...` script paths (:4). Single-project mode (cwd) is unaffected. |
| G8 | Token/time costs | PARTIAL | Only troubleshoot, reflect (tiers) and auggie-review (time) state figures. adversarial, spec-panel, business-panel, brainstorm, pr-submit, swarm, cleanup-audit, release-split, and the utility commands state none. |
| G9 | `/sc:reflect --mode post` on uncommitted work | UNVERIFIED | `--diff` takes "Git ref or path to a diff file"; whether a working-tree diff is accepted without first saving it to a file was not traced in the skill. |
| G10 | Default side effects worth warning about | VERIFIED | (1) reflect UC-2 moves the work-unit folder by default (Wave 7 promotion); (2) auggie-review posts to the PR with no confirmation by default on PR targets; (3) pr-submit defaults to `--monitor 2` (local edits); `--monitor 3` pushes. |
| G11 | Skill-internal tier rubric thresholds beyond the command summary | NOT READ | `refs/escalation-rubric.md` (troubleshoot) and `refs/reflection-rubric.md` (reflect) were not opened; the 0.85 / 0.95 thresholds come from the command files. |
| G12 | pr-submit and swarm skill bodies | PARTIAL | Read command files fully; skills only via targeted grep (pr-submit :22, :38, :66, :122, :132; swarm cli-contract table). Full FSM and interview details not documented here. |
| G13 | Built-in `/code-review`, `/simplify`, `/security-review` | Not in IronClaude source | Described from this session's skill listing only; not code-verified. |

---

## 5. Summary

- 13 IronClaude skills plus 14 requested commands documented; 3 built-in complements noted.
- The tiered, evidence-gated skills are troubleshoot, reflect, auggie-review, and pr-submit (ordinal levels). Panels and debate are adversarial, spec-panel, business-panel, brainstorm, and swarm/bare-review.
- task-builder hand-offs exist in troubleshoot (`--fix`), reflect (`--remediate`), auggie-review (remediation offer), and brainstorm (`--handoff task`); pr-submit reaches it only through troubleshoot. None of them ever runs `/task` or commits on their own.
- Biggest guide risks: stale source branch (G1/G2), the missing `--suspect-source` and `/sc:code-review` targets (G3/G4), and three default side effects (G10).
