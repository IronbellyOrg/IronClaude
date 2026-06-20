# Eval and Validation Targets Research

Status: Complete

## Scope

Reviewed eval and validation artifacts under `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/` for remediation tasklist targets:

- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/evals/evals.json`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/grader.py`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/qualitative-comparison-summary.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.json`

## Current eval inventory and assertion gaps

- `evals.json` is still marked `iteration: 2` with scope `expanded-12-cases-depth-mixed`, and contains 12 cases covering code, incident, product, architecture, process, and research domains plus quick/standard/deep depths and handoffs (`evals/evals.json:1-5`, `evals/evals.json:6-13`, `evals/evals.json:40-61`, `evals/evals.json:84-138`).
- Cases 13-15 and edge flows are explicitly deferred: v1-compat regression cases, trivial edge case, `--resume-from`, `--dry-run`, adversarial FAIL routing, and token-budget hard-kill (`evals/evals.json:140-143`). The remediation tasklist should either keep these deferred explicitly or add them as new eval cases with expected assertions.
- The top-level `assertions_v2` list is under-specified relative to actual live failures. It currently lists broad assertions such as seed brief existence/domain/strategy, acceptance/open questions, convergence, model diversity, enrichment/handoff presence, no silent adversarial pass, budget checks, and contract version (`evals/evals.json:144-159`). It does **not** name several failure-producing checks seen in live comparison: depth, proposal_count, interactive_mode, blind_mode, merged frontmatter spec_type/adversarial_status/proposal_count/blind_mode, Provenance section, return-contract status/domain/proposal_count/handoff_action/agent_spec, and blind-label assertions.

### Exact eval assertion updates to capture in tasklist

Add or make explicit in `evals/evals.json` / generated metadata:

1. `seed_brief_frontmatter_has_depth` for quick/standard/deep expected depth. Evidence: live case 4 failed expected quick vs actual standard (`live-runs/comparison-against-iteration-2.json:92-96`).
2. `seed_brief_frontmatter_has_proposal_count` for expected 2/3/5 proposal counts. Evidence: cases 4, 6, 7, 10, and 11 failed missing proposal_count (`live-runs/comparison-against-iteration-2.json:98-102`, `live-runs/comparison-against-iteration-2.json:571-575`, `live-runs/comparison-against-iteration-2.json:811-815`, `live-runs/comparison-against-iteration-2.json:1414-1418`, `live-runs/comparison-against-iteration-2.json:1670-1674`).
3. `seed_brief_frontmatter_has_interactive_mode_when_expected`. Evidence: incident case 10 failed simulated interactive tagging (`live-runs/comparison-against-iteration-2.json:1420-1424`).
4. `seed_brief_frontmatter_has_blind_mode_when_expected`. Evidence: blind case 11 failed seed `blind_mode: true` (`live-runs/comparison-against-iteration-2.json:1676-1680`).
5. `merged_requirements_frontmatter_has_spec_type`, `merged_requirements_frontmatter_has_adversarial_status`, and `merged_requirements_frontmatter_has_proposal_count`. Evidence: case 4 failed all three (`live-runs/comparison-against-iteration-2.json:104-120`); case 10 failed adversarial_status and proposal_count (`live-runs/comparison-against-iteration-2.json:1468-1478`); case 11 had `adversarial_status='success'` where assertion expected `pass` (`live-runs/comparison-against-iteration-2.json:1718-1722`).
6. `merged_requirements_frontmatter_has_blind_mode_when_expected`. Evidence: blind case 11 failed merged `blind_mode: true` (`live-runs/comparison-against-iteration-2.json:1724-1728`).
7. `merged_requirements_has_provenance_section`. Evidence: missing Provenance is a repeated live structural failure in cases 4, 7, 8, 10, and 11 (`live-runs/comparison-against-iteration-2.json:152-156`, `live-runs/comparison-against-iteration-2.json:847-851`, `live-runs/comparison-against-iteration-2.json:1068-1072`, `live-runs/comparison-against-iteration-2.json:1462-1466`, `live-runs/comparison-against-iteration-2.json:1712-1716`).
8. `merged_requirements_risks_section_counts_tables_or_lists`. Evidence: risk checks failed as zero items in cases 7, 8, and 9 despite qualitative notes calling some of these table-vs-list parser mismatches (`live-runs/comparison-against-iteration-2.json:835-839`, `live-runs/comparison-against-iteration-2.json:1056-1060`, `live-runs/comparison-against-iteration-2.json:1250-1254`; `live-runs/qualitative-comparison-summary.md:100-105`, `live-runs/qualitative-comparison-summary.md:114-120`, `live-runs/qualitative-comparison-summary.md:127-130`).
9. `return_contract_has_status_success`, `return_contract_has_domain`, `return_contract_has_proposal_count`, and `return_contract_has_agent_spec_personas_and_model_aliases`. Evidence: case 4 failed return proposal_count and agent_spec persona/model alias checks (`live-runs/comparison-against-iteration-2.json:182-204`); case 6 failed agent_spec persona/model alias checks (`live-runs/comparison-against-iteration-2.json:667-677`); case 8 failed architect/refactorer and model alias checks (`live-runs/comparison-against-iteration-2.json:1116-1126`); case 11 failed return proposal_count (`live-runs/comparison-against-iteration-2.json:1754-1758`).
10. `blind_mode_anonymized_agent_spec_labels` and `blind_mode_anonymized_debate_labels`. Evidence: case 11 failed Agent A-E/blind/anonymized labels in agent_spec and debate transcript (`live-runs/comparison-against-iteration-2.json:1766-1782`).
11. `live_timing_token_telemetry_present` and `strict_quality_grading_present_for_compared_cases`. Evidence: comparison reports live timing/token unavailable and quality unavailable for every compared case (`live-runs/comparison-against-iteration-2.md:12-13`, `live-runs/comparison-against-iteration-2.md:19-26`), and JSON reasons state missing `timing.json/token telemetry` plus strict quality coverage only for cases 1-3 (`live-runs/comparison-against-iteration-2.json:237-244`).

## Grader extension needs

- `grader.py` parses frontmatter with a simple `key: value` reader and no nested/list support (`grader.py:31-45`). That is sufficient for flat scalar checks but fragile for richer frontmatter and status vocabularies.
- `parse_yaml_simple` skips indented lines and only captures flat top-level `key: value` strings (`grader.py:48-61`). This explains why multiline `agent_spec` or richer return-contract fields are likely to fail substring checks even when semantically present.
- `count_enumerated_items` only counts bullet, plus/star, or numbered items (`grader.py:88-96`). Add table-row counting or a new assertion type for sections that can be either enumerated lists or markdown tables, especially Risks.
- Current assertion types include `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, and `dir_count`; unknown types hard-fail (`grader.py:99-192`). Add new assertion types rather than overloading `yaml_substring` for all richer checks:
  - `section_items_or_table_rows` for Risks/Acceptance/Questions sections.
  - `frontmatter_field_in` or `yaml_field_in` for normalized vocabularies such as `adversarial_status` if `pass` and `success` are both intended to be valid. If only `pass` is canonical, keep assertion strict and fix output instead.
  - `yaml_contains_any_recursive` or real YAML parsing for multiline/nested return-contract checks.
  - `text_contains_any` / `text_not_contains_any` for blind-label transcript assertions; the current live comparison appears to apply a YAML-substring style check to `adversarial/debate-transcript.md`, which is text, not YAML (`live-runs/comparison-against-iteration-2.json:1778-1782`).
- The grader writes `grading.json` for `with_skill` and `old_skill` under each eval directory and returns aggregate stats (`grader.py:195-244`), so validation changes should remain backwards-compatible with existing grading schema: `{expectations, summary}` (`grader.py:11-12`).

## Comparison and quality validation paths

- Structural comparison path is `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.md`. It currently reports 8 cases compared, all 8 live artifact cases present, all 8 complete, baseline structural pass rate 100%, live structural pass rate 81.69%, no strict quality scores, and no live timing/token telemetry (`live-runs/comparison-against-iteration-2.md:5-13`).
- Per-case structural pass deltas: case 4 is 16/26 live (-38.46%), case 5 is 27/27, case 6 is 21/25, case 7 is 20/23, case 8 is 21/25, case 9 is 11/12, case 10 is 21/28, and case 11 is 19/27 (`live-runs/comparison-against-iteration-2.md:17-26`).
- `compare_live_runs.py` intentionally compares only `CASE_IDS = set(range(4, 12))`, i.e. cases 4-11 (`compare_live_runs.py:10-14`), and writes `comparison-against-iteration-2.json` plus `.md` under `live-runs/` (`compare_live_runs.py:277-295`). Case 12 exists in `evals.json` (`evals/evals.json:129-138`) but is excluded from the current comparison script. Remediation tasklist should decide whether case 12 must be included, especially because live-run files show an attempted GraphQL case with an error artifact (observed by file listing; exact error content not reviewed in scope).
- `compare_live_runs.py` pulls quality only from `iterations/iteration-2/quality-grading.json` and returns unavailable with reason `strict quality grading currently covers cases 1-3 only` when no matching output exists (`compare_live_runs.py:37-55`). Extend quality grading or comparison ingestion so cases 4-12 have strict-quality coverage.
- `compare_live_runs.py` only recognizes live runtime/token telemetry when a `timing.json` exists somewhere under a live eval directory (`compare_live_runs.py:134-148`). Current live runs do not include it, so telemetry validation cannot pass until protocol output writes timing/token data or compare script reads an alternate telemetry location.
- `artifact_completeness` requires `seed-brief.md`, `merged-requirements.md`, `return-contract.yaml`, and `adversarial`, plus `handoff` for tasklist/task/design cases (`compare_live_runs.py:100-124`). Structural completeness is therefore necessary but not sufficient; current comparison shows all artifacts complete even while quality regressed (`live-runs/comparison-against-iteration-2.md:7-13`).
- Qualitative validation path is `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/qualitative-comparison-summary.md`. It reports 8 cases, baseline wins 7, live wins 1, baseline average 54.0/60, live average 42.88/60, and average live delta -11.12 (`live-runs/qualitative-comparison-summary.md:5-13`).
- Qualitative dimensions show largest regressions in provenance (-3.88), concreteness (-2.25), actionability (-1.62), and adversarial synthesis (-1.50) (`live-runs/qualitative-comparison-summary.md:28-38`). Cross-case findings identify lost baseline-specific context, missing provenance/source mapping, and generic broadening (`live-runs/qualitative-comparison-summary.md:39-47`).

## Recommended validation command sequence

Run from project root `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2` and use UV for Python:

1. `uv run python /config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/grader.py /config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2`
   - Rebuilds baseline `grading.json` files for iteration-2 using updated assertions. The grader usage is currently `python grader.py <iteration-dir>` (`grader.py:14-16`); project rule requires wrapping with `uv run python`.
2. `uv run python /config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py`
   - Regenerates structural comparison JSON/MD at `live-runs/comparison-against-iteration-2.{json,md}` (`compare_live_runs.py:290-295`).
3. Inspect `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.md` and require: live structural pass rate improves from current 81.69%, quality scores available > 0, live timing/token telemetry available > 0 if telemetry is in scope, and case 12 inclusion if remediation adds it (`live-runs/comparison-against-iteration-2.md:7-13`).
4. Inspect `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/qualitative-comparison-summary.md` and require improvement in provenance/concreteness/actionability regressions before declaring qualitative remediation complete (`live-runs/qualitative-comparison-summary.md:28-47`).
5. If source-of-truth skill/protocol files are edited by the remediation, run `make sync-dev` and `make verify-sync` after src-side edits per project rules. This is outside the eval workspace itself but required for component sync discipline.

## Summary

The remediation tasklist should target three validation layers: (1) make `evals.json` / generated metadata assertions explicit for depth, proposal count, mode flags, merged frontmatter, provenance, risk-section shape, return-contract agent_spec, blind labels, telemetry, and quality coverage; (2) extend `grader.py` to parse real YAML/multiline fields and count table-shaped sections, with text-specific assertions for debate transcripts; and (3) extend `compare_live_runs.py`/quality artifacts so comparison covers intended cases beyond 4-11 (at least decide on case 12), strict quality is available for compared live cases, and timing/token telemetry can be validated.
