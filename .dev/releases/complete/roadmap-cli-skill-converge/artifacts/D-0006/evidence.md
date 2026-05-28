# D-0006 — Evidence: `sc-roadmap-protocol/refs/validation.md` CLI Gate Criteria

| Field | Value |
|---|---|
| Task | T02.04 |
| Roadmap Item | R-006 |
| Drift Item | B-6 |
| Deliverable | D-0006 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` |
| CLI Reference | `REFLECT_GATE` + `ADVERSARIAL_MERGE_GATE` (`src/superclaude/cli/roadmap/validate_gates.py:30-69`); `_build_single_agent_steps` / `_build_multi_agent_steps` (`src/superclaude/cli/roadmap/validate_executor.py:247-338`); cosmetic lane (`src/superclaude/cli/roadmap/cosmetic_remediator.py`, `src/superclaude/cli/roadmap/commands.py:153-170`). |
| Decision Posture | Option 1 (replace sub-agent dispatch with CLI gate criteria) — see `design-decision.md` row B-6 |
| Source Claim Status | VERIFIED (`verification.md:123-134`) — `quality-engineer` / `self-review` sub-agent dispatch and the REVISE loop are documented in the skill ref; CLI has no `Task(`, no sub-agent spawn, no `REVISE` string, and instead uses `REFLECT_GATE` + `ADVERSARIAL_MERGE_GATE` for validate-subcommand steps. |

## Linkage

- **B-6 → D-0006.** `release-scope.md` and `verification.md:123-134` capture the claim: `refs/validation.md:8` ("Dispatch this prompt to a quality-engineer sub-agent."), `:76` ("Dispatch this prompt to a self-review sub-agent."), and `:171-196` (`## REVISE Loop` with `"Hard limit: 2 iterations"` at `:192`) document sub-agent + REVISE behavior that the CLI does not implement. CLI grep confirms zero `Task(`, `sub_agent`, `quality-engineer`, `self-review`, or `REVISE` substrings in `cli/roadmap/executor.py` (the lone `agents_spawned` match at `:2626` is metadata for the remediate step, not sub-agent spawning). `cli/roadmap/validate_executor.py:122-134` shows the only out-of-process invocation is a `ClaudeProcess` subprocess (not `Task`). `cli/roadmap/validate_gates.py:30-69` defines `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` as `GateCriteria` (frontmatter + `min_lines` + semantic checks), which are pure-data validators, not sub-agent dispatches.
- `design-decision.md` row B-6 selected **Option 1**: rewrite around CLI gate criteria and include the cosmetic gate auto-remediation lane; only keep sub-agent validation if clearly marked as non-canonical. `solutions.md:192-223` recommends Solution 1 — "fixes the drift without losing the validation guidance; sub-agent enhancement can be reintroduced later if measured to add value."
- **D-0006** is the resulting source-file edit at `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` plus this evidence record.

## Source-file parity check

### CLI canonical gate criteria cited in the edit

`src/superclaude/cli/roadmap/validate_gates.py:30-45` (`REFLECT_GATE`):

```
required_frontmatter_fields = ["blocking_issues_count", "warnings_count", "tasklist_ready"]
min_lines = 20
enforcement_tier = "STRICT"
semantic_checks = [SemanticCheck("frontmatter_values_non_empty", _frontmatter_values_non_empty, ...)]
```

`src/superclaude/cli/roadmap/validate_gates.py:47-69` (`ADVERSARIAL_MERGE_GATE`):

```
required_frontmatter_fields = [
    "blocking_issues_count", "warnings_count", "tasklist_ready",
    "validation_mode", "validation_agents",
]
min_lines = 30
enforcement_tier = "STRICT"
semantic_checks = [
    SemanticCheck("frontmatter_values_non_empty", _frontmatter_values_non_empty, ...),
    SemanticCheck("agreement_table_present", _has_agreement_table, ...),
]
```

`_has_agreement_table` (`validate_gates.py:15-27`) requires a markdown header row containing `agree`/`agreement`, a separator row, and at least one data row.

### CLI step routing cited in the edit

`cli/roadmap/validate_executor.py:247-274` (`_build_single_agent_steps`): single `Step(id="reflect", gate=REFLECT_GATE, retry_limit=1, ...)` writes `validation-report.md`.

`cli/roadmap/validate_executor.py:277-338` (`_build_multi_agent_steps`): N parallel `Step(id=f"reflect-{agent.id}", gate=REFLECT_GATE, ...)` writing `reflect-{agent.id}.md` per agent, followed by sequential `Step(id="adversarial-merge", gate=ADVERSARIAL_MERGE_GATE, inputs=reflect_outputs, ...)` writing `validation-report.md`.

### Cosmetic-gate auto-remediation lane cited in the edit

`cli/roadmap/commands.py:153-170`: `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` (default enabled) and `--strict-no-remediation` (explicit alias to disable).

`cli/roadmap/cosmetic_remediator.py:27-38` documents the C1-C11 transform catalogue (heading aliases, dash variants, whitespace, smart-quote folding, table padding, frontmatter trim, resource-requirements aliases). `executor.py:3086-3091` wires `apply_cosmetic_remediations` into the generic pipeline executor when `config.allow_cosmetic_remediation` is on. `executor.py:2254-2266` surfaces applied transforms in the HALT report.

### Post-edit `refs/validation.md` structure (in file order)

| Section | Anchor | Status |
|---|---|---|
| Header lead paragraph | `validation.md:3` | ✅ Reframed from "agent prompt + 4-question + aggregation + thresholds" to "CLI gate-criteria validation + cosmetic lane + non-canonical inference-only sub-agent prompts" |
| CLI Canonical Behavior (B-6, VERIFIED) | `validation.md:7-80` | ✅ New canonical section — names `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, `frontmatter_values_non_empty`, `agreement_table_present`, `_has_agreement_table`; cites `validate_gates.py:30-69`, `validate_executor.py:247-338`; documents single-agent vs multi-agent routing and lists per-roadmap-step gates (`SPEC_FIDELITY_GATE`, `WIRING_GATE`, `DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE`, `CERTIFY_GATE`, `ANTI_INSTINCT_GATE`, `TEST_STRATEGY_GATE`) for B-3 cross-link |
| Cosmetic-Gate Auto-Remediation Lane | `validation.md:84-128` | ✅ New canonical section — names `--allow-cosmetic-remediation`, `--no-allow-cosmetic-remediation`, `--strict-no-remediation`, `classify_gate_failure`, `apply_cosmetic_remediations`; enumerates C1-C11; cites `commands.py:153-170`, `cosmetic_remediator.py`, `executor.py:2254-2266` and `executor.py:3086-3091`; describes how the lane sits in front of every gate |
| Non-Canonical Inference-Only Material | `validation.md:132-258` | ✅ Demoted material — preserves verbatim the `quality-engineer` agent prompt, `self-review` 4-question protocol, aggregation formula, decision thresholds, adversarial-mode additional checks, REVISE loop (Iteration 1, Iteration 2, Maximum iterations), and `--no-validate` behavior. All wrapped under an out-of-scope marker that explicitly cites the CLI grep evidence (no `Task(`, no `REVISE`) and refers back to the SKILL.md crosswalk's "inference-only and non-canonical" flag |
| CLI parity baseline (B-6) | `validation.md:262-273` | ✅ New comparison table — CLI canonical vs inference-only side-by-side across mechanism, gates, failure model, re-run, multi-agent path, cosmetic auto-fix, and `--no-validate` |
| Footer | `validation.md:end` | ✅ Updated to record CLI parity baseline citations (`validate_gates.py:30-69`, `validate_executor.py:247-338`, `cosmetic_remediator.py`, `commands.py:153-170`) |

## Acceptance criteria check (`phase-2-tasklist.md:207-212`)

- ✅ `refs/validation.md` describes CLI gate criteria instead of sub-agent dispatch — see "CLI Canonical Behavior (B-6, VERIFIED)" section (`validation.md:7-80`). The canonical section is at the top of the file, before any sub-agent material, and explicitly states that the CLI does not dispatch `quality-engineer` or `self-review` sub-agents.
- ✅ `refs/validation.md` names `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, frontmatter checks, semantic checks, and cosmetic gate auto-remediation — all present in the canonical CLI section. `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` are each documented with their required_frontmatter_fields, min_lines, enforcement_tier, and semantic_checks. The cosmetic lane section enumerates `--allow-cosmetic-remediation`, `--no-allow-cosmetic-remediation`, `--strict-no-remediation`, and the C1-C11 transform catalogue.
- ✅ `refs/validation.md` marks any retained quality-engineer, self-review, or REVISE-loop sub-agent language as non-canonical or removes it from canonical scope — the "Non-Canonical Inference-Only Material" section (`validation.md:132-258`) wraps all sub-agent prompts, the aggregation formula, the decision thresholds, and the entire REVISE loop. Every retained piece is explicitly marked "(inference-only)" inline and bracketed by the section-level out-of-scope marker. The REVISE Loop subsection has an additional "CLI parity reminder" block restating that the CLI does not execute the loop.
- ✅ Evidence at this path links B-6 → D-0006 and records the removed REVISE-loop behavior — see the "Source Claim Status" row of the header table, the "Linkage" section above, and the explicit "removed REVISE-loop behavior" treatment captured in both the "Reframed vs. preserved skill content" section below and the inline "CLI parity reminder" in the demoted REVISE Loop subsection.

## Reframed vs. preserved skill content

- **Preserved verbatim** (text identical, semantics demoted to inference-only):
  - Quality-engineer agent prompt and the 4-dimension scoring (completeness 0.35, consistency 0.30, traceability 0.20, test_strategy 0.15).
  - Self-review agent prompt and the 4-question protocol (faithfulness 0.30, achievability 0.25, risk_quality 0.25, test_actionability 0.20).
  - Aggregation formula `final_score = (qe * 0.55) + (sr * 0.45)`.
  - Decision Thresholds table (`>= 85% PASS / 70-84% REVISE / < 70% REJECT`).
  - Adversarial mode additional checks (missing adversarial/ dir → REJECT; missing convergence_score → REVISE).
  - REVISE Loop iterations 1 and 2, the 2-iteration hard cap, and `PASS_WITH_WARNINGS` fallthrough.
  - `--no-validate` behavior — preserved as the one item that is canonical on both surfaces (CLI: no validate pipeline built; skill-mode: no sub-agents dispatched).
- **Removed from canonical scope** (folded under the "Non-Canonical Inference-Only Material" section with an out-of-scope marker):
  - The REVISE loop is no longer presented as something the roadmap protocol executes; its CLI-parity disclaimer is restated inline immediately above the iteration descriptions.
  - Aggregate weighted score and PASS/REVISE/REJECT bands are no longer presented as CLI behavior — the "CLI parity baseline (B-6)" table makes this explicit.
- **Added** (new canonical content for B-6):
  - "CLI Canonical Behavior (B-6, VERIFIED)" section covering the four-field `GateCriteria` shape, `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, single-vs-multi-agent routing, and the post-merge per-roadmap-step gate catalogue.
  - "Cosmetic-Gate Auto-Remediation Lane" section covering the three CLI flags, the C1-C11 transform catalogue, and the orchestrator equivalent guidance.
  - "CLI parity baseline (B-6)" comparison table.
  - Footer parity-baseline note flagging the CLI source citations.

## Cross-edit linkage

This edit aligns with three companion items:

- `SKILL.md:137` already flags Wave 4's sub-agent dispatch as "inference-only and non-canonical for CLI parity" and points to B-6. No SKILL.md edit was needed here — the crosswalk row is consistent with the new `refs/validation.md` layout.
- `SKILL.md:145` Inference-Only Thresholds bullet already states that the CLI does not compute an aggregate validation score and does not run a REVISE loop. The new "CLI parity baseline (B-6)" table in `refs/validation.md` is the canonical reference for the bullet.
- `SKILL.md:296-302` (Wave 4 behavioral instructions) still references the quality-engineer / self-review prompts in `refs/validation.md`. That is consistent with the demoted-but-preserved treatment in this edit; SKILL.md prose changes are out of scope for T02.04.

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md`. A subsequent `make sync-dev` is required (tracked under B-12 / Phase 5) before `.claude/skills/sc-roadmap-protocol/refs/validation.md` and `/config/.claude/skills/sc-roadmap-protocol/refs/validation.md` reflect the change. Per repo rules, `.claude/` mirrors are not staged or committed.

## CLI behavior anchors cited in the edit

- `cli/roadmap/validate_gates.py:15-27` — `_has_agreement_table` semantic check.
- `cli/roadmap/validate_gates.py:30-45` — `REFLECT_GATE` definition.
- `cli/roadmap/validate_gates.py:47-69` — `ADVERSARIAL_MERGE_GATE` definition.
- `cli/roadmap/validate_executor.py:247-274` — `_build_single_agent_steps`.
- `cli/roadmap/validate_executor.py:277-338` — `_build_multi_agent_steps` (N parallel reflections + adversarial merge).
- `cli/roadmap/gates.py:131-139` — `_frontmatter_values_non_empty` semantic check used by both gates.
- `cli/roadmap/commands.py:153-170` — cosmetic remediation CLI flag surface.
- `cli/roadmap/cosmetic_remediator.py:27-38` — C1-C11 transform catalogue documentation block.
- `cli/roadmap/executor.py:2254-2266` — cosmetic-remediation surfacing in HALT report.
- `cli/roadmap/executor.py:3086-3091` — wiring of `apply_cosmetic_remediations` into the generic pipeline executor.

## REVISE-loop removal record

Per `phase-2-tasklist.md:212` the evidence must record the removed REVISE-loop behavior. Summary:

- **Behavior removed from canonical scope.** The 2-iteration REVISE loop (collect `improvement_recommendations`, re-run Wave 3 → Wave 4, max 2 iterations, fall through to `PASS_WITH_WARNINGS`) no longer represents roadmap-protocol behavior. It is preserved verbatim under "Non-Canonical Inference-Only Material" with the CLI-parity reminder block immediately above the iteration descriptions.
- **Why removed.** CLI grep confirms zero `REVISE` substrings in `cli/roadmap/executor.py` and `cli/roadmap/validate_executor.py`; the CLI's only retry mechanism is the per-step `retry_limit=1` knob on `Step(...)` (`validate_executor.py:271, 319`), which is a single mechanical retry on transport errors, not a regenerate-on-low-score loop.
- **What the CLI does instead.** Each step either passes its `GateCriteria` (frontmatter fields present and non-empty, `min_lines` floor met, all `semantic_checks` return True) or halts the pipeline (STRICT) / records the failure (STANDARD). Cosmetic-only failures may be auto-rewritten by the cosmetic-remediation lane and the step continues; semantic failures are terminal.
- **Reintroduction path.** If a future CLI release wires a REVISE-style loop into `validate_executor.py`, the demoted material can be promoted back to canonical and the CLI parity baseline table updated accordingly. The B-6 row in `release-scope.md` is the tracking point.
