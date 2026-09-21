# Preserve-baseline sentences (item 0.8)

These strings MUST survive byte-identical through every later Edit. Cited from the worktree at HEAD `5d35643e`.

## RUB:20 formula

`refs/escalation-rubric.md:20`

```
**Confidence** = `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`.
```

## RUB:35 (allow-listed H-token line)

`refs/escalation-rubric.md:35`

```
Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 0.95-REFUTE case); a wrong AFFIRM is caught by CI. Source-only REFUTEs of runtime claims are the precise failure mode under repair and must not clear the 0.85 STOP gate. The 0.84 AFFIRM cap means source-only AFFIRMs of runtime claims still ESCALATE to Tier 2 (below the 0.85 STOP).
```

## CAL:127-134 Will-Not block

`src/superclaude/agents/confidence-calibrator.md:127-134`

```
**Will Not:**

- Trust the card's self-reported confidence as a starting point
- Re-write the card
- Propose new evidence or fixes
- Inherit the card's narrative framing — score what's there, not what's implied
- Apply social judgement — only the rubric anchors and the cited evidence
- Decide the escalation verdict from intuition — the rubric's rules in order determine the verdict
```

## HOC:68 latch literal

`refs/hardening-output-contract.md:68`

```
Once `latched`, `pipeline_hardening_verdict ∈ {blocked, advisory}` and no later `task-builder`, `sc:reflect`, or `sc:adversarial` stage may upgrade it to `pass`/`success`.
```

## NOT PROVEN / ADVISORY strings (truth table + report template)

`refs/hardening-output-contract.md:34-38` and `refs/report-template.md:248-252`

- `NOT PROVEN — failed hardening wave: <wave>`
- `NOT PROVEN — mandatory runtime proof waived or absent`
- `NOT PROVEN — unrationalized N/A: <wave>`
- `ADVISORY — closure relies on waived/substituted proof`
- `ADVISORY — scoped closure with rationalized N/A`

## 4 HC5-mapping rows (`refs/hardening-output-contract.md:47-50`)

| H5 Decision | H5 Status | Waiver Status Effect |
| `performed` | `PASS` | `none` |
| `not_required` | `PASS` | `none` |
| `required` | `FAIL` | `none` |
| `waived_with_rationale` | `N/A` with rationale | `latched` |

## calibrator-eval-cases.md:49,54 (allow-listed H-token lines)

`:49` `Replays actual H2 card from T4. **Self-reported confidence on the original card: 0.85** (REFUTE; also passed through unguarded). \`claim_class: runtime_behavior\`, \`evidence_class: source_static\` (WebFetch GitHub URLs), \`verdict_direction: REFUTE\`.`

`:54` `Replays actual H1 card from T4 (0.82 self-reported CONFIRM with mixed source + log evidence). \`claim_class: runtime_behavior\`, \`evidence_class: log_evidence\`, \`verdict_direction: AFFIRM\`.`

## SKILL:530

```
- Emit an instrumentation tasklist at `<output-dir>/diagnosability-tasklist.md` instead of hypothesis work when the hard-stop fires — no hypothesis work happens in the same turn as an instrumentation patch; the user re-runs after instrumenting.
```

## Output-Contract field NAMES (`tests/troubleshoot/test_hardening_output_contract.py:21-56`)

Legacy (19): `status`, `tier_reached`, `report_path`, `audit_log_path`, `confidence`, `escalation_reason`, `test_is_wrong`, `test_file_path`, `behavior_is_documented`, `doc_context_card_path`, `hypothesis_cards`, `adversarial_artifacts_dir`, `task_file_path`, `remediation_offered`, `remediation_accepted`, `diagnosability_verdict`, `diagnosability_context_card_path`, `diagnosability_tasklist_path`, `diagnosability_hard_stop`

Hardening (11): `contract_version`, `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `waiver_status`, `backtest_status`, `off_path_review_decision`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path`, `known_escapes_caught`

## Five tavily strings (`tests/skills/test_tier2_tavily_consistency.py`)

- `mcp__tavily__tavily_search`
- `≤2 queries` / `at most 2`
- `fail-open` / `degrad`
- `search_depth: advanced`
