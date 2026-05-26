# D-0009 — Evidence: B-9 Relationship-to-CLI framing for `sc-validate-roadmap-protocol/SKILL.md`

**Task:** T03.01
**Roadmap Item:** R-009
**Decision recorded:** B-9 = Option 2 (preserve the deep-validation protocol; add a top-of-file Relationship-to-CLI header + crosswalk).
**Source of truth:** `.dev/releases/current/roadmap-cli-skill-converge/design-decision.md:39`,
`.dev/releases/current/roadmap-cli-skill-converge/solutions.md:297-328`.

## 1. Option 2 decision and usage distinction (B-9)

Per `solutions.md:310-328`, Solution 2 ("top-of-file disclaimer + crosswalk; preserve rich pipeline") is selected because:

- the rich deep-validation pipeline likely carries inference value the CLI's single-pass flow does not reproduce, and
- a full rewrite (Solution 1) is "hard to reverse" and risks destroying genuinely useful content.

**Usage distinction recorded in `SKILL.md` Relationship-to-CLI header:**

- **Skill** → thorough investigative validation for a human reviewer (multi-phase coverage matrix, gap registry, adversarial review, remediation plan, Auggie/Serena enrichment). Use when the goal is to *understand* roadmap quality.
- **CLI (`superclaude roadmap validate`)** → automated CI/CD gating via a simpler reflect + adversarial-merge flow. Use when a deterministic pass/fail signal is needed for pre-merge or pre-tasklist hooks.

The two surfaces are explicitly framed as **complementary, not equivalent**, and the SKILL.md states the CLI does not delegate into the skill and the skill does not wrap the CLI.

## 2. CLI validation dimensions — 7 baseline / 9 input-aware

Derived directly from the CLI prompt builder
`src/superclaude/cli/roadmap/validate_prompts.py:7,52,74-127` and reproduced in the SKILL.md crosswalk table.

Baseline (always present, no original input documents supplied) — 7 dimensions:

| # | Dimension | Severity |
|---|---|---|
| 1 | Schema | BLOCKING |
| 2 | Structure | BLOCKING |
| 3 | Traceability | BLOCKING |
| 4 | Cross-file consistency | BLOCKING |
| 5 | Parseability | BLOCKING |
| 6 | Interleave | WARNING |
| 7 | Decomposition | WARNING |

Input-aware (when spec / TDD / PRD input files resolve) — 9 dimensions: the same five BLOCKING structural dimensions plus two BLOCKING input-aware dimensions, followed by two WARNING heuristics:

| # | Dimension | Severity | Notes |
|---|---|---|---|
| 1 | Schema | BLOCKING | same as baseline |
| 2 | Structure | BLOCKING | same as baseline |
| 3 | Traceability | BLOCKING | same as baseline |
| 4 | Cross-file consistency | BLOCKING | same as baseline |
| 5 | Parseability | BLOCKING | same as baseline |
| 6 | **Coverage** | BLOCKING | added only when input docs supplied (`validate_prompts.py:89-97`) |
| 7 | **Proportionality** | BLOCKING | added only when input docs supplied (`validate_prompts.py:98-104`) |
| 8 | Interleave | WARNING | renumbered from baseline #6 |
| 9 | Decomposition | WARNING | renumbered from baseline #7 |

The conditional 7-or-9 selector is implemented at `validate_prompts.py:51-52` (`dim_count = 9 if has_inputs else 7`).

## 3. Reflect + adversarial-merge CLI flow

The SKILL.md Relationship-to-CLI header documents that `superclaude roadmap validate` runs a **reflect + adversarial-merge** flow rather than the skill's multi-phase pipeline. Source citations:

- `src/superclaude/cli/roadmap/validate_prompts.py:7` — module-level docstring naming the two prompt builders: `build_reflect_prompt` (single-agent reflection across N validation dimensions) and `build_merge_prompt` (adversarial merge with agreement categorization).
- `src/superclaude/cli/roadmap/validate_prompts.py:68` — `build_reflect_prompt` signature (the entry point for the reflection pass).
- `src/superclaude/cli/roadmap/validate_prompts.py:74-127` — body of `build_reflect_prompt` emitting the 7/9 dimensions verbatim.

## 4. Preservation of B-9's deep protocol

A manual inspection of `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` confirms that none of the deep-protocol content was removed: phases, CC1–CC4 agents, GO / CONDITIONAL_GO / NO_GO verdict matrix, Auggie/Serena enrichment, and remediation planning are still present below the inserted Relationship-to-CLI header. The header is additive only and explicitly states the deep protocol is "preserved intentionally."

## 5. Acceptance-criteria checklist

| Criterion (from `phase-3-tasklist.md:46-49`) | Result |
|---|---|
| `SKILL.md` contains a top-of-file Relationship to CLI section stating this skill is an inference-only deep-validation protocol | ✅ — section inserted between the metadata comment and `## Triggers` (header text: "This skill is an inference-only deep-validation protocol."). |
| `SKILL.md` states that `superclaude roadmap validate` runs a simpler reflect plus adversarial-merge flow against CLI validation dimensions | ✅ — explicit statement in the Relationship-to-CLI prose with citation to `validate_prompts.py:7,68`. |
| `SKILL.md` describes 7 baseline dimensions and 9 input-aware dimensions when original source inputs resolve, while preserving B-9's deep protocol | ✅ — full 9-row dimension table reproduced (showing baseline and input-aware numbering side by side); deep protocol content below the header is unchanged. |
| Evidence at `D-0009/evidence.md` records the Option 2 decision and the usage distinction (skill = investigative; CLI = CI/CD gating) | ✅ — this file, section 1. |
| Evidence at `D-0009/evidence.md` records the 7 baseline and 9 input-aware CLI validation dimensions | ✅ — this file, section 2. |

## 6. Files modified

- `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` — inserted Relationship-to-CLI section + crosswalk table immediately after the extended-metadata comment.
- `.claude/skills/sc-validate-roadmap-protocol/SKILL.md` — refreshed via `make sync-dev`; `make verify-sync` reports "All components in sync."

## 7. Source citations summary

| Claim | Source |
|---|---|
| B-9 selects Option 2 | `design-decision.md:39`; `solutions.md:328` |
| Deep protocol preserved with disclaimer + crosswalk | `solutions.md:310-317` |
| 7 baseline dimensions vs 9 input-aware dimensions | `validate_prompts.py:51-52, 74-127` |
| Coverage + Proportionality are the two input-aware BLOCKING additions | `validate_prompts.py:89-104` |
| Reflect + adversarial-merge flow names | `validate_prompts.py:6-9` |
| Usage distinction (investigative vs CI/CD gating) | `solutions.md:311` ("Use this skill for thorough investigative validation; use the CLI for automated CI/CD gating.") |
