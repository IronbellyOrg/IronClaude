---
topic: "Add a --minstar flag to sc:recommend that sets the minimum GitHub stars required before recommend will suggest a plugin/project. Default 500 stars."
domain: code
strategy: agile
depth: standard
proposals_target: 1
handoff_target: none
created: 2026-06-20T04:56:00Z
adversarial_note: "Heavyweight multi-model adversarial wave intentionally scoped out — change is tightly bounded, fully grounded in source, and all design ambiguity was resolved by direct user decisions (Socratic Q1-Q4). Convergence = user decisions."
---

# Seed Brief: sc:recommend --minstar

## Problem Statement

`/sc:recommend --plugin` searches the Claude Code plugin / community-skill
ecosystem and returns candidate plugins/skills. Today it applies **no
popularity floor** — a 3-star abandoned repo ranks alongside a 12k-star
maintained one. The user wants a `--minstar N` flag (default **500**) that
filters out low-popularity candidates before they are surfaced.

## Known Context (grounded in source, 2026-06-20)

- Stars are a **GitHub/marketplace repo metric**. The local surface
  (commands/skills/agents/templates) has no stars, so `--minstar` is
  meaningful **only in `--plugin` mode** (Phase 3 ecosystem search).
- `src/superclaude/commands/recommend.md:36` asserts **"`--plugin` and
  `--eval` are the only flags"** — this line is now false and must change.
- The `--plugin` result format
  (`refs/plugin-ecosystem-sources.md:46-59`) has **no Stars field**. You
  cannot filter/sort on a metric you do not surface; a visible `Stars`
  field must be added to the result record + output template first.
- The skill **delegates** the ecosystem search (to `tech-research` /
  `deep-research` / Tavily) and does not run it inline
  (`refs:27`, `SKILL.md:169`). So the filter has two possible homes:
  (a) embedded as an instruction inside the delegated search prompt, or
  (b) a post-filter the skill applies to returned candidates. The spec
  uses **both**: instruct the delegate to capture stars, and have the
  skill enforce the floor + two-tier split on the returned set.
- `--minstar` is a **protocol-markdown** feature. `cli/recommend/*.py`
  owns cache/dispatch/eval/telemetry; it does **not** parse `--plugin`
  or `--eval`. No argparse change is required. `prompts.py` carries the
  COLD_PATH_RUNBOOK Phase-3 description and is a secondary touch point.
- No occurrence of `minstar` exists anywhere in `src/` or `tests/` — clean slate.

## Constraints

- C1. Anti-fabrication rules R1-R4 hold: the new flag must appear in the
  verified command flag table / `argument-hint`, or it is itself a
  fabricated flag.
- C2. Source-of-truth discipline: edit `src/superclaude/**`, then
  `make sync-dev` → `.claude/`; never edit `.claude/` directly.
- C3. Single-line bash in any emitted command; no emojis (project convention).
- C4. Citation discipline already required for every `--plugin` candidate
  (`refs:96-98`) — star counts are claims and must carry their source URL.
- C5. Scope discipline: filter + sort only (user-approved); no
  `--maxstar`, no `--sort` flag, no time-window popularity.

## User Decisions (Socratic Wave 1)

- **D1 — Default scope: ALWAYS-ON at 500.** `--plugin` filters at a 500-star
  floor even when `--minstar` is omitted. This is a deliberate
  behavioral change (today's plugin mode is unfiltered). `--minstar 0`
  is the documented escape hatch to disable.
- **D2 — Unknown-star handling: TWO-TIER OUTPUT.** Do not silently drop
  candidates whose star count is undiscoverable (Anthropic-curated
  marketplace entries; skills nested inside a large parent repo where the
  repo's stars are not the skill's). Primary section = GitHub-star
  candidates at/above the floor, **sorted by stars descending**. A
  separate **"Bonus — unranked by stars" section** lists credible
  candidates with no own-repo star count (non-GitHub, curated, or
  nested-in-larger-project), each labeled with why it is unranked.
- **D3 — `--minstar` without `--plugin`: WARN AND IGNORE.** Emit a
  one-line notice that `--minstar` has no effect in local mode, then
  proceed with the normal local recommendation. Not a STOP.
- **D4 — Scope: FILTER + SORT.** Add the floor AND order surviving
  primary candidates by star count descending.

## Success Criteria

- S1. `/sc:recommend <goal> --plugin` returns only ≥500-star GitHub
  candidates in the primary section, sorted by stars desc, plus a bonus
  section for unranked-but-credible candidates.
- S2. `--minstar 1200` raises the floor; `--minstar 0` disables filtering;
  invalid values (negative / non-integer) STOP with a usage hint.
- S3. Every primary candidate shows a `Stars` field with its source URL.
- S4. `--minstar` in default mode warns-and-ignores (D3).
- S5. `make verify-sync` passes; the "only flags" assertion is corrected;
  no R1-R4 violation.

## Open Questions (deferred, non-blocking)

- OQ1. Should the bonus section be capped (e.g. top 3) like the primary
  list, or list all credible unranked candidates? (Spec proposes: same
  top-3 discipline as primary.)
- OQ2. Update the large standalone plugin mirror
  `plugins/superclaude/commands/recommend.md` in the same change, or defer
  to the plugin-packaging refresh? (Spec proposes: defer; note it.)
