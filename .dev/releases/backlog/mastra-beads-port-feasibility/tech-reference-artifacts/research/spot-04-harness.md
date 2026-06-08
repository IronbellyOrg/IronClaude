# Spot-04: Harness-Corpus Counts & Source-of-Truth Verification

**Investigation type:** Integration Mapper
**Status:** Complete
**Date:** 2026-06-03
**HEAD:** 9e8648603636d6b9f8fab9e261e583d0de849f34

---

## Scope

Confirm research file 05's harness-corpus counts (42 commands, 39 agents, 24 skills),
the presence of `hooks.json`/`core/*`, and resolve the `src/superclaude/` vs
`plugins/superclaude/` source-of-truth conflict at HEAD.

## Claims extracted from research files

### From `05-skills-agents-harness-reuse.md`

- **Section 8 inventory totals** (lines 165-172):
  - Command markdown: **42 files** under `src/superclaude/commands/`
  - Agent markdown: **39 files** under `src/superclaude/agents/`
  - Skill packages: **24 `SKILL.md` files** under `src/superclaude/skills/`
  - Core instruction files: 12 markdown files under `src/superclaude/core/`
  - Workflow templates: 8 files; Document templates: 7 files
  - Hook assets: `hooks.json` + 9 scripts + README/example
  - MCP assets: 11 MCP docs + 11 JSON configs
- **Source-of-truth conflict** (Gaps #1, lines 188; Section 6 line 151):
  - `src/superclaude/core/CLAUDE.md:45-48` says edit `src/superclaude/` first
  - `commands/README.md`, `agents/README.md`, `hooks/README.md` say assets are
    copies from `plugins/superclaude/...` — both path families claimed to exist.

(findings appended below as verified)

---

## Verified Findings

### (a) Corpus counts at HEAD 9e864860 — CONFIRMED (no drift)

All three research-file counts reconcile exactly once you account for the
`README.md` in each directory (the research file itself flags these READMEs as
stale at its lines 197-198).

| Asset | Research claim | Verified at HEAD | Verdict |
|---|---:|---|---|
| Commands | **42 files** under `src/superclaude/commands/` | **42** `*.md` total = 41 command defs + 1 `README.md` (`git ls-files src/superclaude/commands/*.md` = 42) | CONFIRMED — no drift. The 42 counts README; functional command defs = 41. |
| Agents | **39 files** under `src/superclaude/agents/` | **39** `*.md` total = 38 agent defs + 1 `README.md` (`git ls-files src/superclaude/agents/*.md` = 39) | CONFIRMED — no drift. The 39 counts README; functional agent defs = 38. |
| Skills | **24 `SKILL.md`** under `src/superclaude/skills/` | **24** skill directories, each with exactly one `SKILL.md` (`find -mindepth 2 -maxdepth 2 -name SKILL.md` = 24; skill dirs = 24) | CONFIRMED — exact match, no drift. |

**Counting method (counts only, per task scope):**
- Commands: `ls src/superclaude/commands/*.md` → 42 (41 excluding README.md).
- Agents: `ls src/superclaude/agents/*.md` → 39 (38 excluding README.md).
- Skills: `find src/superclaude/skills -mindepth 2 -maxdepth 2 -name SKILL.md` → 24,
  and `find -mindepth 1 -maxdepth 1 -type d` → 24 (1:1 dir↔SKILL.md).

**Interpretation note:** Research file 05 phrased these as "42 files / 39 files",
i.e. a raw directory `*.md` file count that includes the directory README. That
raw count is exactly correct at HEAD. If a future consumer wants *functional
definitions only*, the numbers are 41 commands / 38 agents / 24 skills.

The 24 skills enumerated:
`confidence-check, prd, sc-adversarial-protocol, sc-auggie-review-protocol,
sc-brainstorm-protocol, sc-cleanup-audit-protocol, sc-cli-portify-protocol,
sc-crash-recovery, sc-pm-protocol, sc-recommend-protocol, sc-reflect-protocol,
sc-release-split-protocol, sc-review-translation-protocol, sc-roadmap-protocol,
sc-tasklist-protocol, sc-task-protocol, sc-troubleshoot-protocol,
sc-validate-roadmap-protocol, sc-validate-tests-protocol, task-builder, task,
tdd, tech-reference, tech-research`.

### (b) hooks.json + core/* presence — CONFIRMED

- `src/superclaude/hooks/hooks.json` — **PRESENT** (2110 bytes, regular file).
- `src/superclaude/core/` — **PRESENT**, **12 `.md` files** (matches research's
  "12 markdown files under core" claim): `BUSINESS_PANEL_EXAMPLES.md`,
  `BUSINESS_SYMBOLS.md`, `CLAUDE.md`, `COMMANDS.md`, `FLAGS.md`, `MCP.md`,
  `MODES.md`, `ORCHESTRATOR.md`, `PERSONAS.md`, `PRINCIPLES.md`,
  `RESEARCH_CONFIG.md`, `RULES.md` (plus an `__init__.py`).

### (c) Source-of-truth verdict: `src/superclaude/` vs `plugins/superclaude/`

**Verdict: BOTH path trees exist and are git-tracked at HEAD, but
`src/superclaude/` is the canonical source-of-truth and `plugins/superclaude/`
is a materially out-of-sync, smaller subset/mirror — NOT canonical.**

Evidence:

| Path tree | Commands (`*.md`, tracked) | Agents (`*.md`, tracked) | Skills (`SKILL.md`) | `hooks.json` | core `*.md` |
|---|---:|---:|---:|---|---:|
| `src/superclaude/` | **42** (41 + README) | **39** (38 + README) | **24** | present | 12 |
| `plugins/superclaude/` | 30 | 20 | **1** | present | 6 |

- `plugins/superclaude/` is **a strict, stale subset**: it is missing many
  commands that exist only in `src/` (`diff -qr` reports `Only in src`:
  `adversarial.md`, `auggie-review.md`, `cleanup-audit.md`, `cli-portify.md`,
  `release-split.md`, `review-translation.md`, `roadmap.md`, … plus README),
  and many shared files differ in content (`analyze.md`, `brainstorm.md`,
  `business-panel.md`, `cleanup.md`, `design.md`, `estimate.md`, `implement.md`,
  `improve.md`, `pm.md`, `recommend.md`, `reflect.md`, `research.md` all
  reported as differing). The plugins skills tree has only **1** SKILL.md vs
  24 in src.
- `src/superclaude/core/CLAUDE.md` (sync section) designates `src/superclaude/`
  as source-of-truth with `.claude/` as synced dev copies; project + user
  CLAUDE.md reinforce "edit `src/superclaude/` first, then `make sync-dev`".
- The conflict noted in research (the `commands/README.md`, `agents/README.md`,
  `hooks/README.md` "edit `plugins/superclaude/...` first" notes) is real but
  is a **transitional / stale-doc artifact**, not the operative policy. The
  plugins tree's drift (smaller, divergent) confirms it is not being treated as
  canonical on this branch.

**Resolution stated explicitly:** At HEAD `9e864860`, `src/superclaude/` is the
canonical instruction corpus (42/39/24). `plugins/superclaude/` exists but is a
divergent, incomplete v5-transition mirror and must NOT be used as primary
source. Any port should ingest `src/superclaude/`.

### External target-mapping claims

All Mastra / Backlog.md / Beads agent/skill→target mappings in research files 05
and 11 are **[DESIGN — UNBUILT]**, not verified. No Mastra/Backlog/Beads
integration exists in this repo; those mappings are target hypotheses only.

## Summary

- **Counts CONFIRMED, no drift** vs 42/39/24: src commands `*.md` = 42 (41 defs +
  README), agents `*.md` = 39 (38 defs + README), skills `SKILL.md` = 24 (exact).
  Research's "42/39 files" wording is a raw `*.md` count including each
  directory README — correct as written.
- **hooks.json PRESENT** (`src/superclaude/hooks/hooks.json`, 2110B); **core/**
  PRESENT with 12 `.md` files.
- **Source-of-truth: `src/superclaude/` is canonical**; `plugins/superclaude/`
  exists and is git-tracked but is a smaller, divergent, out-of-sync mirror
  (30 commands / 20 agents / 1 skill / 6 core) and is NOT canonical.
- External Mastra/Backlog/Beads mappings = [DESIGN — UNBUILT].

**Status: Complete**
