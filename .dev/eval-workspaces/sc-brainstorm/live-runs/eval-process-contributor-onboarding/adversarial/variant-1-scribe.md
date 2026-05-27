---
variant: 1
agent: opus:scribe
focus: agile iterative docs improvements
created: 2026-05-27T00:00:00Z
---

# Variant 1 — Documentation-First Onboarding (Scribe / Opus)

## Premise

Most new-contributor drop-off happens at the "first 30 minutes" — clone, install, run tests, attempt one change. Documentation is the highest-leverage surface to fix in an agile sprint because it ships in hours, not weeks.

## Proposed Improvements

### 1. Add a `QUICKSTART.md` (top-level, ~150 lines)

- Linear "first PR in 30 minutes" path: clone → `make dev` → `uv run pytest -k smoke` → pick a `good-first-issue` → PR.
- Single decision tree: "Are you fixing a typo? Adding a skill? Touching `src/superclaude/`? Touching `.claude/`?" Each branch maps to 3-5 concrete steps.
- Linked from `README.md` above CONTRIBUTING.md.

### 2. Inline failure-mode appendix in CONTRIBUTING.md

- New section: "If pre-commit blocked you with X, do Y." Cover the top 5 hook failures: `verify-sync`, `markdownlint`, `freshness-pre-edit`, `ruff lint`, `ruff format`.
- Each entry is 3 lines: symptom, root cause one-liner, exact command to fix.

### 3. Worked-example skill PR

- Create `docs/contributor-guide/worked-example-skill-pr.md` walking through a real merged PR that added a small skill: every file touched, every command run, every hook output.
- Pin in `docs/` index so newcomers can mirror it.

### 4. "Three-doc rule" sticker on issues

- Add issue template field: "Before you start, skim these three docs: QUICKSTART, CONTRIBUTING §Y, and KNOWLEDGE §Z."
- Templates auto-populate links based on label (`good-first-issue` → skill docs; `bug` → debugging docs).

### 5. Glossary as a first-class doc

- `docs/contributor-guide/glossary.md`: skill, slash command, agent, hook, sync-dev, source-of-truth, MDTM, persona, MCP. Each entry: one-sentence definition + one-line example.
- Cross-linked from CONTRIBUTING.md and from every skill SKILL.md.

## Success Metrics

- Time-to-first-PR (median, from first commit on contributor's branch to merge) drops by 30%.
- Issue comments asking "how do I run the tests?" / "what is sync-dev?" drop to near-zero within 4 weeks.
- New contributors successfully resolve their own pre-commit failures (measured by absence of maintainer comments about hooks).

## Sprint Plan (one 2-week sprint)

- Week 1: QUICKSTART.md, failure-mode appendix, glossary.
- Week 2: worked-example skill PR, issue template updates, internal review + iteration.

## Risks

- Docs drift if not paired with a lightweight lint/check. Mitigation: add a `make docs-check` target verifying QUICKSTART commands still work (smoke-runs the documented sequence in CI).
- "Yet another doc" fatigue. Mitigation: keep QUICKSTART under 150 lines; everything else is an appendix or cross-link, not a new doc.

## Out-of-Scope Acknowledged

- No mentorship rotation, no chat-bot, no automated environment provisioning — pure documentation surface.
