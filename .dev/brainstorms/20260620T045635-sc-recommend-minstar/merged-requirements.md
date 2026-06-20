---
title: "sc:recommend --minstar — Merged Requirements"
topic: "Add --minstar popularity floor (default 500) to /sc:recommend --plugin"
domain: code
strategy: agile
status: ready-for-implementation
adversarial_status: converged-via-user-decision
convergence_basis: "Socratic Q1-Q4 user decisions D1-D4; single fully-grounded proposal"
created: 2026-06-20T04:56:00Z
source_files_verified:
  - src/superclaude/commands/recommend.md
  - src/superclaude/skills/sc-recommend/SKILL.md
  - src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
  - src/superclaude/cli/recommend/prompts.py
---

# Merged Requirements: `sc:recommend --minstar`

## 1. Summary

Add a `--minstar <N>` flag to `/sc:recommend`. In `--plugin` (ecosystem
search) mode it enforces a **minimum GitHub-star floor** on surfaced
candidates, **defaulting to 500 even when the flag is omitted** (D1).
Surviving GitHub candidates are **sorted by stars descending** (D4) in a
primary section; credible candidates with no own-repo star count are not
dropped but moved to a separate **"Bonus — unranked by stars"** section
(D2). In default (local) mode the flag **warns and is ignored** (D3),
because the local surface has no stars.

This is a **protocol-markdown change** (command + skill + ref). No Python
argparse change is required; `cli/recommend/*.py` does not parse
`--plugin`/`--eval`/`--minstar`.

## 2. Flag Contract

| Property | Value |
|---|---|
| Name | `--minstar <N>` |
| Type | non-negative integer |
| Default | `500` (applied in `--plugin` mode whether or not the flag is typed) |
| Disable | `--minstar 0` (no floor; bonus section still separates unranked) |
| Scope | `--plugin` mode only; in local mode → warn-and-ignore |
| Validation | negative or non-integer → STOP: `"--minstar requires a non-negative integer (e.g. --minstar 500). Use --minstar 0 to disable the floor."` |

`recommend.md` currently says **"`--plugin` and `--eval` are the only
flags"** (line ~36). That sentence MUST be rewritten to enumerate three
flags and state that `--minstar` is plugin-mode-only.

## 3. Behavioral Requirements

### R-1 — Plugin-mode floor (default-on)
In `--plugin` mode, resolve the floor: `N = value of --minstar if passed
else 500`. A candidate with a discoverable own-repo star count `< N` is
excluded from output entirely (it is neither primary nor bonus).

### R-2 — Primary section: filter + sort (D1, D4)
Candidates with a discoverable own-repo GitHub star count `>= N` form the
**primary** section, ordered by stars **descending**. Keep the existing
top-3 disambiguator discipline (`refs:61`). Each primary record gains a
`Stars` field (see §4).

### R-3 — Bonus section: unranked-but-credible (D2)
Candidates that are credible matches but have **no own-repo star count**
are listed in a separate, clearly-labeled **"Bonus — not ranked by GitHub
stars"** section. This covers three sub-cases, and each entry states which:
- `curated` — Anthropic-curated marketplace plugin (no GitHub stars by design)
- `non-github` — source is not a GitHub repo
- `nested` — skill/plugin lives inside a larger repo; the repo's stars are
  not attributable to this component
The bonus section is **never** filtered by the floor (the floor applies to
GitHub-star candidates only). Apply the same top-3 discipline (OQ1 → top 3).

### R-4 — Local-mode warn-and-ignore (D3)
If `--minstar` is present and `--plugin` is NOT, emit exactly one notice:
`"--minstar has no effect without --plugin (the local surface has no
stars); ignoring it."` Then run the normal local recommendation. Do not STOP.

### R-5 — Star capture in the delegated search
Because the skill delegates the search, the generated search prompt MUST
instruct the delegate to **capture each candidate's GitHub star count and
its source URL** (the repo page / API). The skill then enforces R-1..R-3
on the returned set. Stars are a claim → carry a citation (C4 / `refs:96`).

### R-6 — Empty-primary handling
If the floor removes every GitHub candidate but bonus candidates exist,
surface the bonus section and a one-line note:
`"No candidate met the >= N star floor; showing unranked credible matches
below. Lower the floor with --minstar <smaller>."` If nothing credible
survives at all, reuse the existing "found nothing credible" guidance
(`refs:63-66`).

### R-7 — Anti-fabrication (C1, R1-R4 unchanged)
`--minstar` is now a verified flag in the command flag table + skill
`argument-hint`, satisfying R1. No star count may be invented; an
undiscoverable count routes a candidate to bonus (R-3), never to a guessed
number.

## 4. Result-Format Change (`refs/plugin-ecosystem-sources.md`)

Add a `Stars` row to the per-candidate result table (§"Result format",
currently lines 50-59) and to the output template (lines 68-79):

```text
Plugin: <name>
Stars: <count> (<source URL>)        <-- NEW; "n/a — <curated|non-github|nested>" in bonus
Capability: <one-sentence summary>
Install: `<single-line bash command>`
Repo: <URL>
Version / activity: <last commit date or version pin>
Integration notes: <what to wire up>
Caveats: <any>
Source: <citation URL>
```

Add a new subsection documenting the **two-tier output** (primary sorted
by stars + bonus for unranked) and the floor-resolution rule.

## 5. File-Change Plan (source-of-truth first, then sync)

| # | File | Change | Required |
|---|---|---|---|
| 1 | `src/superclaude/commands/recommend.md` | Add `--minstar` to flag table; fix the "only flags" line; update `argument-hint`, Usage, and add a `--plugin --minstar` example | Yes |
| 2 | `src/superclaude/skills/sc-recommend/SKILL.md` | Update `argument-hint`; extend Phase 3 with floor-resolution, two-tier output, R-4 warn-and-ignore, R-5 delegated star capture; add `--minstar` to Boundaries | Yes |
| 3 | `src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md` | Add `Stars` field to result table + template; add two-tier-output subsection; add floor + sort rules | Yes |
| 4 | `make sync-dev` | Propagate 1-3 to `.claude/`; then `make verify-sync` | Yes |
| 5 | `src/superclaude/cli/recommend/prompts.py` (COLD_PATH_RUNBOOK Phase-3 text, ~line 160) | Mention the floor + two-tier output so the cold-path Haiku subagent honors it | Recommended |
| 6 | `plugins/superclaude/commands/recommend.md` (standalone plugin mirror, 32KB) | Mirror the flag-table change | Defer (OQ2) — note in PR |
| 7 | Tests | No Python unit (feature is protocol-markdown). Optional: a doc-presence assertion that `--minstar` appears in both command flag table and skill `argument-hint` (doc⇆protocol parity), mirroring the CLI-doc-parity practice | Optional |

**Do NOT** stage `.claude/` paths (gitignored sync-dev output); stage only
the `src/` side + `plugins/` if touched.

## 6. Edge Cases

- E1. `--minstar 0` → floor disabled; primary lists all GitHub candidates
  sorted by stars; bonus still separates unranked. (Useful escape hatch.)
- E2. `--minstar abc` / `--minstar -5` → STOP (validation, §2).
- E3. A candidate inside `anthropic/skills` (huge repo): its own component
  has no separate star count → **bonus / `nested`**, not the parent's stars.
- E4. Curated `claude-plugins-official` entry with no GitHub repo →
  **bonus / `curated`**.
- E5. Rate-limited / unreachable star lookup for an otherwise-GitHub repo →
  treat as undiscoverable → **bonus / `non-github`**-equivalent with note
  `"star count unavailable at lookup time"`; do not guess (R-7).
- E6. `--minstar` + `--eval` together in `--plugin` mode → floor applies to
  the discovery set BEFORE the eval adoption pipeline runs on survivors.

## 7. Acceptance Criteria

- AC1. `--minstar` present in command flag table AND skill `argument-hint`
  (R1 satisfied); the "only flags" sentence corrected.
- AC2. `--plugin` with no `--minstar` filters at 500 (D1) and sorts primary
  by stars desc (D4).
- AC3. Unranked-but-credible candidates appear in a labeled bonus section
  with sub-case reason, never silently dropped (D2).
- AC4. `--minstar` without `--plugin` warns-and-ignores (D3); local
  recommendation otherwise unchanged.
- AC5. Result format + output template show a `Stars` field with citation.
- AC6. `make verify-sync` green; no `.claude/` paths staged.

## 8. Out of Scope (scope discipline, C5)

- `--maxstar`, a generic `--sort` flag, fork-count / download-count metrics,
  time-windowed "trending" popularity, and any change to default (local)
  ranking. Only the plugin-mode star floor + sort + two-tier output.

## 9. Recommended Next Step

This is small and well-bounded — direct implementation, no further
brainstorming needed:

```text
/sc:implement Add a --minstar flag (default 500, plugin-mode-only, warn-and-ignore in local mode) to /sc:recommend per .dev/brainstorms/20260620T045635-sc-recommend-minstar/merged-requirements.md: edit src/superclaude/commands/recommend.md, src/superclaude/skills/sc-recommend/SKILL.md, and refs/plugin-ecosystem-sources.md (add Stars field + two-tier primary/bonus output), then run make sync-dev and make verify-sync. Do not stage .claude/ paths.
```
