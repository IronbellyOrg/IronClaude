Research the IronClaude PRD/TDD/Spec pipeline architecture and produce verified findings, corrections, and a precise implementation plan.

We have an analysis document at `.dev/analysis/spec-vs-prd-vs-tdd.md` that was produced through conversation rather than codebase investigation. Every claim in it needs to be verified against the actual source files. This research has two missions:

---

## Mission 1 — Accuracy audit of the analysis document

Verify every factual claim in `.dev/analysis/spec-vs-prd-vs-tdd.md` by reading the actual source files. Flag anything that is wrong, incomplete, or misleading. Specifically confirm or correct:

1. How the spec is actually created — manual template vs spec-panel — and whether spec-panel has any knowledge of `release-spec-template.md` or its frontmatter fields. Check `.claude/commands/sc/spec-panel.md` and confirm whether a protocol skill exists at `.claude/skills/sc-spec-panel*/`

2. Exactly which YAML frontmatter fields sc:roadmap reads from the spec and how it uses them — read `.claude/skills/sc-roadmap-protocol/SKILL.md`, `refs/extraction-pipeline.md`, `refs/scoring.md`, `refs/templates.md`

3. Exactly what sc:tasklist accepts as input and what it extracts — read `.claude/skills/sc-tasklist-protocol/SKILL.md` in full

4. Whether sc:roadmap's extraction pipeline would handle TDD-structured input (sections 7, 8, 9, 10, 14, 15, 19, 24, 25) — specifically whether the 8-step extraction would find and use TDD content or miss it

5. What the PRD and TDD skills actually do and what they output — read `.claude/skills/prd/SKILL.md` and `.claude/skills/tdd/SKILL.md` in full

6. What `src/superclaude/examples/release-spec-template.md` and `src/superclaude/examples/tdd_template.md` actually contain — read both in full

7. Whether IronClaude truly has no TDD or PRD system beyond the two recently-added skills — check `.claude/commands/sc/` for any spec/design/prd/tdd commands

---

## Mission 2 — Precise implementation plan for Option 3

Assuming Option 3 is confirmed correct (modify TDD template + upgrade pipeline tools), produce an exact, file-level implementation plan. For each change, specify the exact file to edit, what currently exists, and what needs to be added or changed:

1. **TDD template additions** — exactly which YAML frontmatter fields to add to `src/superclaude/examples/tdd_template.md`, with the exact field names, types, and values sc:roadmap expects. Reference `refs/scoring.md` and `refs/extraction-pipeline.md` to confirm field names match exactly.

2. **sc:roadmap extraction pipeline upgrades** — for each TDD section (data models §7, API specs §8, state management §9, component inventory §10, observability §14, testing strategy §15, migration plan §19, release criteria §24, operational readiness §25): determine whether the current 8-step extraction pipeline already captures this content or misses it, and specify exactly what new extraction logic is needed in `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`

3. **sc:roadmap scoring formula upgrades** — read `.claude/skills/sc-roadmap-protocol/refs/scoring.md` in full and specify exactly how to add `api_surface` and `data_model_complexity` factors while keeping weights summing to 1.0

4. **sc:spec-panel additions** — since no protocol skill exists, determine whether spec-panel needs a protocol skill created or whether the command file itself needs instructions added. Specify exactly what template-awareness and TDD-awareness instructions are needed and where they go in `.claude/commands/sc/spec-panel.md`

5. **sc:tasklist additions** — read the full tasklist protocol and determine exactly where and how to add TDD-aware task generation rules (component inventory → tasks, migration phases → phases, testing strategy → test tasks, observability → instrumentation tasks) in `.claude/skills/sc-tasklist-protocol/SKILL.md`

6. **PRD→TDD wiring in the tdd skill** — read `.claude/skills/tdd/SKILL.md` in full and identify exactly where synthesis agents should be instructed to consume PRD epics, ACs, and success metrics

---

## Scope

- `.claude/skills/`
- `.claude/commands/sc/`
- `src/superclaude/examples/`
- `.dev/analysis/spec-vs-prd-vs-tdd.md`

## Output

A research report that:
- Corrects the analysis document with verified facts
- Provides a precise, file-by-file implementation plan for Option 3 that a developer could execute without guessing

Update `.dev/analysis/spec-vs-prd-vs-tdd.md` directly with verified corrections when findings contradict what's currently written.

## Depth: Deep
