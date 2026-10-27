---
type: "🧭 Design Decision"
release: "roadmap-cli-skill-converge"
date: "2026-05-25"
status: "recorded"
source_artifacts:
  - release-scope.md
  - solutions.md
  - verification.md
---

# Design Decision — Roadmap CLI ↔ Skill / Command Convergence

## Decision posture

Use a mixed posture: make lightweight command/reference surfaces CLI-faithful where the release already verified concrete drift, preserve the high-value deep-validation protocol as an explicitly inference-only surface, and defer structure-only refactors until they are needed.

This satisfies the release's up-front requirement to record a design decision before edits land (`release-scope.md:32-39`, `release-scope.md:202`) while avoiding a destructive rewrite of the rich validation skill.

## Current-update sweep incorporated

- B-1's CLI-only flag list must include the newer cosmetic-remediation flags: `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` and `--strict-no-remediation`.
- B-3 and B-6 should mention the CLI's cosmetic gate auto-remediation lane when describing current CLI behavior.
- B-9 should describe CLI validation as 7 baseline dimensions, expanding to 9 input-aware dimensions when original source inputs resolve.
- B-12's historical md5 evidence may be stale, but the parity/sync conclusion remains the governing requirement.

## Per-item decisions

| Item | Decision | Rationale | Implementation note |
|---|---|---|---|
| B-1 — `commands/roadmap.md` flag-set drift | Option 1 | `solutions.md:48` recommends a 1:1 command rewrite, and the drift is concrete user-facing CLI surface mismatch verified in `verification.md:37-48`. | Mirror current `superclaude roadmap run` help, including `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` and `--strict-no-remediation`; remove or explicitly deprecate inference-only flags. |
| B-2 — `commands/validate-roadmap.md` frontmatter + flag drift | Option 1 | `solutions.md:83` recommends the full rewrite, and the command currently mixes a cosmetic naming issue with substantive flag/output-dir/NFR-006 drift (`verification.md:54-72`). | Fix `name: sc:validate-roadmap`, mirror CLI validate flags, document `<OUTPUT_DIR>/validate/`, and state exit 0 per NFR-006. |
| B-3 — `sc-roadmap-protocol/SKILL.md` taxonomy mismatch | Hybrid, based on Option 1 | `solutions.md:118` recommends keeping Wave pedagogy while making CLI step IDs first-class, which best fits the release purpose without deleting useful skill structure. | Keep Waves as orchestration, add an exact CLI step crosswalk for the 14-step pipeline, include cosmetic gate auto-remediation, and reframe non-CLI thresholds as inference heuristics only. |
| B-4 — `refs/scoring.md` stale CLI cross-reference | Option 1 | `solutions.md:153` recommends re-deriving scoring from CLI source; verification shows the ref omits the PRD detection algorithm even though it claims CLI parity (`verification.md:92-106`). | Add PRD-first detection and cite the current CLI detection function rather than preserving the stale prose. |
| B-5 — `refs/templates.md` 4-tier discovery vs single-template CLI | Option 1 | `solutions.md:188` recommends collapsing to current CLI behavior, and verification confirms the 4-tier model does not match the implemented CLI (`verification.md:110-119`). | Replace the 4-tier discovery model with the single-template resolver behavior, or move future-looking material out of the canonical ref. |
| B-6 — `refs/validation.md` sub-agent pattern absent from CLI | Option 1 | `solutions.md:223` recommends replacing the sub-agent/REVISE loop with CLI gate criteria, and verification confirms the CLI uses gate criteria rather than sub-agent dispatch (`verification.md:123-134`). | Rewrite around CLI gate criteria and include the cosmetic gate auto-remediation lane; only keep sub-agent validation if clearly marked as non-canonical. |
| B-7 — `refs/extraction-pipeline.md` 8-step extraction vs single CLI prompt | Option 1 | `solutions.md:258` recommends collapsing to a single-pass reference; verification confirms the CLI executes one extraction step via a prompt builder (`verification.md:138-147`). | Convert the 8 steps into checklist/rationale inside a single-pass extraction description. |
| B-8 — `refs/adversarial-integration.md` protocol delegation | Option 1 | `solutions.md:293` recommends removing `sc:adversarial-protocol` delegation to match the CLI's single debate step; verification confirms the delegation is skill-only (`verification.md:151-161`). | Replace direct protocol delegation with the CLI debate prompt flow; mention richer `sc:adversarial` usage only as out-of-band/inference-only if needed. |
| B-9 — `sc-validate-roadmap-protocol/SKILL.md` deep validation pipeline | Option 2 | `solutions.md:328` recommends preserving the rich deep-validation protocol with an explicit disclaimer because a full rewrite would destroy likely useful inference content. | Add a top-of-file Relationship to CLI header and crosswalk; describe CLI validation as 7 baseline dimensions and 9 input-aware dimensions when source inputs resolve. |
| B-10 — `sc-validate-roadmap-protocol` packaging shape | Option 2 / defer | `solutions.md:363` recommends deferring structure-only factoring until B-9 is settled; B-9 preserves the deep skill but this release should stay minimal. | Leave single-file packaging as-is for this release; revisit refs factoring only if load/token cost becomes a measured problem. |
| B-12 — synced copies refresh | Mechanical, same under both options | `solutions.md:398` recommends the existing sync workflow; verification confirms source and synced copies were in parity and only need refresh after edits (`verification.md:211-220`). | After source edits, run `make sync-dev`, verify with `make verify-sync`, and refresh global `/config/.claude/` copies according to project release practice. |

## Explicit exclusions

- B-11 is excluded from this decision because `verification.md:193-207` refuted the global-install gap.
- Release-guide rewrites remain out of scope for this release, as stated in `release-scope.md:14` and `release-scope.md:220-225`.
- No new automation is authorized by this decision; generated flag-table tooling and CI sync checks remain deferred because `solutions.md:39-46` and `solutions.md:389-396` describe heavier machinery than this release needs.

## Sequencing

1. Land B-1 and B-2 command-surface changes first.
2. Land B-3, B-4, B-5, B-6, B-7, and B-8 as the roadmap skill/reference convergence batch, keeping the CLI crosswalk internally consistent.
3. Land B-9's Relationship to CLI header and crosswalk without rewriting the deep-validation protocol.
4. Leave B-10 unchanged unless B-9 follow-up review finds measured load/token pain.
5. Run B-12 sync and verification after all `src/` edits land.
