# D-0003 — Evidence: `sc-roadmap-protocol/SKILL.md` CLI Step Crosswalk + Wave Mapping

| Field | Value |
|---|---|
| Task | T02.01 |
| Roadmap Item | R-003 |
| Drift Item | B-3 |
| Deliverable | D-0003 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` |
| CLI Reference | `_get_all_step_ids` (`src/superclaude/cli/roadmap/executor.py:2281-2300`) |
| Decision Posture | Hybrid based on Option 1 — preserve Wave pedagogy, add CLI step crosswalk as first-class (see `design-decision.md` B-3 row) |

## Linkage

- **B-3 → D-0003.** `verification.md:76-88` (VERIFIED) confirmed the skill used Wave 0–4 + Post-Wave taxonomy and made no mention of `anti-instinct`, `spec-fidelity`, `wiring-verification`, `deviation-analysis`, `remediate`, or `certify` — the six CLI step IDs the CLI emits via `_get_all_step_ids`. `release-scope.md` "B-3" entry called for the 14-step crosswalk and threshold reconciliation. `design-decision.md` row B-3 selected the hybrid path (Option 1-based): keep Waves as orchestration, add CLI step crosswalk + Wave mapping, mark non-CLI thresholds as inference-only, and document the cosmetic gate auto-remediation lane.
- **D-0003** is the resulting source-file edit at `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` plus this evidence record.

## Source-file parity check

CLI canonical step list from `cli/roadmap/executor.py:2281-2300` (`_get_all_step_ids`):

```
extract, generate-{agent_a.id}, generate-{agent_b.id}, diff, debate, score,
merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification,
deviation-analysis, remediate, certify
```

Total: 14 step IDs (two `generate-*` IDs templated on agent identity).

Post-edit `SKILL.md` (Section 4 → "### CLI Step Crosswalk", lines 107–138) lists all 14 step IDs in the same pipeline order and adds a Wave → CLI step mapping table:

| Acceptance criterion | Location in `SKILL.md` | Status |
|---|---|---|
| All 14 CLI roadmap step IDs named | Crosswalk list lines 117–126 (`extract` through `certify`, including `generate-{agent_a.id}` / `generate-{agent_b.id}`) | ✅ |
| Wave orchestration preserved | Waves 0, 1A, 1B, 2, 3, 4, Post-Wave headings unchanged (lines 156+) | ✅ |
| Each Wave mapped to CLI steps | Wave ↔ CLI step mapping table at lines 130–138 | ✅ |
| Six previously-missing step names mentioned (`anti-instinct`, `spec-fidelity`, `wiring-verification`, `deviation-analysis`, `remediate`, `certify`) | Lines 120, 122–126 (numbered list) and lines 136–137 (mapping rows) | ✅ |
| Thresholds reframed as inference-only | "### Inference-Only Thresholds" subsection lines 140–146 explicitly demotes convergence routing (`>=0.6 PASS / >=0.5 PARTIAL / <0.5 FAIL`), validation aggregate (`>=85 PASS / 70-84 REVISE / <70 REJECT`), and `2-10 agents` count range to inference heuristics. CLI gate criteria (`validate_gates.py`) named as canonical. | ✅ |
| Cosmetic gate auto-remediation lane documented | "### Cosmetic-Gate Auto-Remediation Lane" subsection lines 148–156 names `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` / `--strict-no-remediation`, cites `cli/roadmap/commands.py:153-170` and `cli/roadmap/cosmetic_remediator.py`, references the `is_pure_cosmetic` classification, and the HALT remediated-step surfacing at `executor.py:2254-2266`. | ✅ |

## CLI behavior anchors cited in the edit

- `cli/roadmap/executor.py:2281-2300` — `_get_all_step_ids` canonical pipeline order.
- `cli/roadmap/validate_gates.py` — `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, `SPEC_FIDELITY_GATE`, `WIRING_GATE`, `DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE` cited as canonical pass/fail mechanism.
- `cli/roadmap/prompts.py` — `build_extract_prompt`, `build_extract_prompt_tdd`, `build_debate_prompt`, `_DEPTH_INSTRUCTIONS` named where the Wave ↔ step rows reference them (consistency with B-7 / B-8 verification evidence).
- `cli/roadmap/commands.py:153-170` — cosmetic-remediation flag triplet (`--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` / `--strict-no-remediation`).
- `cli/roadmap/cosmetic_remediator.py` — `apply_cosmetic_remediations`, `Classification.is_pure_cosmetic` named for the auto-remediation lane classification.
- `cli/roadmap/executor.py:2254-2266` — HALT report surfacing of `remediated` step results and applied cosmetic transforms.

## Reframed vs. preserved skill content

- **Preserved** (Wave pedagogy untouched): Wave 0 prerequisites, Wave 1A multi-spec invocation, Wave 1B extraction + scoring, Wave 2 milestone/template logic, Wave 3 generation sequencing, Wave 4 dispatch language, Post-Wave completion. The hybrid decision explicitly retained these as orchestration units.
- **Reframed as inference-only** (now documentation-only, CLI gates canonical):
  - `convergence_score >= 0.6 / >= 0.5 / < 0.5` routing (was at lines 143-144 / 198-200; still present inside Wave 1A and Wave 2 bodies but now annotated as inference-only via the new "Inference-Only Thresholds" subsection).
  - `PASS >= 85% / REVISE 70-84% / REJECT < 70%` aggregate (referenced by Wave 4 via `refs/validation.md`).
  - `Range: 2-10 agents` (Section 5 "Agent Count Rules") demoted to inference recommendation.
- **Added** (new canonical content for B-3): CLI step crosswalk list + Wave ↔ CLI step mapping table + cosmetic-gate auto-remediation lane subsection.

## Acceptance criteria check (`phase-2-tasklist.md:46-49`)

- ✅ `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` lists all 14 CLI roadmap step IDs named in the source documents.
- ✅ `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` preserves Wave orchestration while mapping each Wave to CLI steps.
- ✅ `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` marks threshold language as inference-only rather than CLI gate behavior.
- ✅ Evidence at this path links B-3 to `D-0003` and names the cosmetic gate auto-remediation lane (`--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` / `--strict-no-remediation`).

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`. A subsequent `make sync-dev` is required (and tracked under B-12 / Phase 5) before `.claude/skills/sc-roadmap-protocol/SKILL.md` and `/config/.claude/skills/sc-roadmap-protocol/SKILL.md` reflect the change. Per repo rules, `.claude/` mirrors are not staged or committed.
