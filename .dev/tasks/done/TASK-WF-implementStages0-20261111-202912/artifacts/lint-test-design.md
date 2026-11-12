# Panel contract lint: test design (Task 6, implemented by Task 15)

Source: `merged-requirements.md`, "Contract compatibility gate", item 3 (contract lint test) and item 5 (bump rule
check), and the plan's Task 15 text. Task 15 creates `src/superclaude/cli/reflect/panel_lint.py` and
`tests/cli/reflect/test_panel_contract_lint.py` from this design.

## Checker shape

`lint_panel_contract(out_dir, legacy_contract) -> list[str]`

- `out_dir`: the panel run's output directory. The contract is `out_dir/return-contract.yaml`.
- `legacy_contract`: the parsed contract of the matched legacy fixture (a mapping), used only by L7.
- Returns the failure lines in the order L0 to L7, then B. An empty list is a pass. Values inside messages are
  Python `repr()` of the parsed YAML value (`None` for an absent key), so each message is exact.
- If L0 fails, the checker returns that single line and runs nothing else.

## Pinned constants (Task 15)

- `STABLE_FIELDS_1_8_0`: the 110 top-level keys of the YAML block in `SKILL.md` section 9.1
  (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`, the fenced block after the "### 9.1 Stable contract
  (contract_version: 1.8.0)" heading). Extraction rule: every line of that block that matches `^([a-z_0-9]+):`
  (no indent). The block does not parse as YAML (it holds `a | b` value forms), so the rule is line-based.
- `TELEMETRY_FIELDS`: the 26 top-level keys of the YAML block in section 9.2, same rule.
  `citations_dropped_extrapolated` is in both lists.
- Drift test: a test re-extracts both lists from `SKILL.md` with the rule above and fails when either differs
  from the constant (message names the keys added and removed).
- `LOAD_BEARING_BOOLS`: imported from `contract.py` `_LOAD_BEARING_BOOL_FIELDS` (lines 47-57): `regression_present`,
  `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `adversarial_unavailable`,
  `input_drift_detected`, `verification_ran`.
- `PARITY_FIELDS`: `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity` (the diversity
  trio, section 9.1), `calibrator_diversity`, `reviewer_cards`.

"Wave 4 ran" below means `tier_reached` is not the integer `1` (EV-1 applies only when Wave 4 runs; the plan's
panel and shadow runs are T2).

## Assertions and exact failure messages

| ID | Gate item | Assertion | Exact failure message |
|---|---|---|---|
| L0 | precondition | `return-contract.yaml` exists, parses as YAML and is a mapping | `L0 contract: return-contract.yaml is missing, unparseable or not a mapping` |
| L1 | 3 | `contract_version == "1.8.0"` (string equality) | `L1 contract_version: expected '1.8.0', got {value!r}` |
| L2 | 3, 5 | every top-level key is in `STABLE_FIELDS_1_8_0`, in `TELEMETRY_FIELDS`, or is `telemetry`; one line per offending key, keys sorted | `L2 stable keys: top-level key {key!r} is not in the 1.8.0 stable field list or the telemetry block` |
| L2t | 3 | when `telemetry` is present it is a mapping (panel telemetry lives inside it) | `L2 stable keys: 'telemetry' must be a mapping, got {type_name}` |
| L3 | 3, 5 (EV-2) | Wave 4 ran: `merge_method` in `{adversarial, single-reviewer-fallback}`; T1: `merge_method` is null, absent or one of those two | `L3 merge_method: {value!r} is not a legal 1.8.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')` |
| L4 | 3 | `adversarial_convergence_score` is a finite Python `float` (not `bool`, not `int`) or null/absent | `L4 adversarial_convergence_score: expected a float or null, got {value!r}` |
| L5 | 3 | each of `LOAD_BEARING_BOOLS`, in sorted order: a present non-null value is a real `bool`; and when Wave 4 ran, `adversarial_unavailable` and `regression_present` are present and not null | `L5 {field}: expected a real boolean, got {value!r}` |
| L6m | 3 (EV-1) | Wave 4 ran and `out_dir/panel/manifest.json` exists: it is a JSON object, and if it has `reviewers_resolved` that value is an `int` (not `bool`) of at least 1; when this fails, L6a takes R from `len(reviewer_cards)` | `L6 EV-1: panel/manifest.json is not a JSON object with a positive integer reviewers_resolved` |
| L6a | 3 (EV-1) | Wave 4 ran and `out_dir/adversarial/merged-verdict.yaml` parses to a mapping whose `merge_method` is `adversarial`: the number of distinct `<n>` among regular files in `out_dir/reviewer-cards/` named `reviewer-<n>-card.yaml`, `.yml` or `.md` is at least `required = max(2, R)`, where R is `reviewers_resolved` from `panel/manifest.json` when that key is present, else `len(reviewer_cards)` (0 when not a list) | `L6 EV-1: reviewer-cards/ holds {cards} card(s), fewer than the required {required} ({source})` with `{source}` one of `reviewers_resolved from panel/manifest.json`, `len(reviewer_cards)`, `minimum 2` (the last when R < 2) |
| L6b | 3 (EV-1) | Wave 4 ran and L6a's merged verdict is not there: the loud fallback holds, that is `adversarial_unavailable is True`, `merge_method == 'single-reviewer-fallback'` and `out_dir/audit.log` has a line matching `\bF[23]\b` | `L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: {mv_state}; fallback missing: {missing})` with `{mv_state}` one of `absent`, `unparseable`, `merge_method {value!r}` and `{missing}` the comma-joined subset, in this order, of `adversarial_unavailable: true`, `merge_method: single-reviewer-fallback`, `audit.log F2/F3 row` |
| L7 | 3 (and item 2) | for each of `PARITY_FIELDS` in the order above: the panel value equals the legacy value; `reviewer_cards` compares the sorted list of path basenames of each side (recorded paths are absolute and differ by run directory and machine) | `L7 parity {field}: panel {panel_value!r} differs from matched legacy {legacy_value!r}` (for `reviewer_cards` both values are the sorted basename lists) |
| B | 5 | bump rule: added as the last line whenever an L2 key line (not L2t) or L3 failed; `{n}` counts the L2 key lines, `{m}` is 1 when L3 failed, else 0 | `B bump rule: the contract leaves 1.8.0 ({n} stable-key violation(s), {m} EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make` |

Notes on the choices:

- L2 accepts section 9.2 names at the top level because `derive_verdict` reads `degraded_components` at the top
  level (`contract.py:197`) and recorded contracts carry it there (for example
  `.dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203517/return-contract.yaml`). Panel keys
  that are in neither list (for example `cluster_agreement`) must sit under `telemetry:`. Of the 36 recorded
  1.8.0 T2 pre contracts, 16 pass L2; the others carry run-specific keys such as `plan_verdict`. The lint is
  meant for panel-run contracts and the matched fixture, not as a retro-check of every recorded run.
- L5 tolerates absent or null for the five other booleans, as `derive_verdict` does (`contract.py:210-222`):
  `verification_ran` is a UC-2 field and most recorded pre contracts write `null`.
- L4 rejects an `int`: the gate text says float, and every recorded 1.8.0 pre contract writes a float or null.
- L6 checks the interactive layout `out_dir/adversarial/` that the recorded pre runs and the Stage 2 shadow mode
  use. The `--unattended` layout (`nested/adversarial-<n>/`, `SKILL.md` section 8) is not covered; on such a run
  L6 reports `merged-verdict: absent`. Task 15 states this limit in the module docstring.
- L6b follows the plan's Task 15 text, which requires `merge_method: single-reviewer-fallback` for the fallback
  (SKILL.md EV-1 requires it only on the F2 path; on F3 a T2 contract still needs a legal L3 value).

## Fixtures

Recorded source: `.dev/reflect/pre-design-20261104164711/` (contract 1.8.0, `mode: pre`, `tier_reached: 2`,
`merge_method: adversarial`, `adversarial_convergence_score: 0.852`, all seven booleans real, no top-level key
outside the stable list, `telemetry` a mapping, `adversarial/merged-verdict.yaml` with `merge_method:
adversarial`, three cards `reviewer-{1,2,3}-card.yaml`, three `reviewer_cards` entries; parity values
`full`, `multi`, `full`, `degraded`). Copy `return-contract.yaml`, `adversarial/merged-verdict.yaml` and
`reviewer-cards/` with the directory structure to `tests/cli/reflect/fixtures/` (Task 15 picks the folder name).
No `audit.log` and no `panel/` exist in the source.

| Fixture | Built from | Purpose |
|---|---|---|
| FX-LEGACY | the copy above, unchanged | matched legacy fixture: the run under test and `legacy_contract` |
| FX-PANEL-DIR | FX-LEGACY plus `panel/manifest.json` = `{"reviewers_resolved": 3}` and one more file under `panel/` | a `panel/` directory does not change the result |
| FX-EXTRA-KEY | FX-LEGACY plus the top-level line `cluster_agreement: 1.0` | an extra stable key fails |
| FX-MERGE-PANEL | FX-LEGACY with `merge_method: panel` | an illegal EV-2 value fails |

Variants built in the test from FX-LEGACY in `tmp_path` (no committed file): listed with the cases below.

## Pass cases (expected result: empty list)

| Case | Input | Legacy |
|---|---|---|
| P1 | FX-LEGACY | FX-LEGACY |
| P2 | FX-PANEL-DIR (manifest `reviewers_resolved: 3`, 3 cards) | FX-LEGACY |
| P3 | FX-LEGACY without `panel/` (R from `len(reviewer_cards)` = 3) | FX-LEGACY |
| P4 | FX-LEGACY plus panel keys under `telemetry:` (`telemetry.panel_engine: shadow`) | FX-LEGACY |
| P5 | FX-LEGACY plus top-level `degraded_components: []` (a section 9.2 name) | FX-LEGACY |
| P6 | FX-LEGACY with `verification_ran: null` | FX-LEGACY |
| P7 | FX-LEGACY with `adversarial_convergence_score: null` | FX-LEGACY |
| P8 | loud fallback: `adversarial/` removed, `adversarial_unavailable: true`, `merge_method: single-reviewer-fallback`, `audit.log` holding `{"wave":5,"step":"5.0","outcome":"F2"}` | the same variant |
| P9 | T1: `tier_reached: 1`, `merge_method: null`, `adversarial/` removed | the same variant |
| P10 | FX-LEGACY with each `reviewer_cards` entry moved to another directory (same basenames) | FX-LEGACY |

## Fail cases (expected result: exactly these lines)

| Case | Input (legacy is FX-LEGACY unless stated) | Expected lines |
|---|---|---|
| F1 | FX-EXTRA-KEY | `L2 stable keys: top-level key 'cluster_agreement' is not in the 1.8.0 stable field list or the telemetry block`; `B bump rule: the contract leaves 1.8.0 (1 stable-key violation(s), 0 EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make` |
| F2 | FX-MERGE-PANEL | `L3 merge_method: 'panel' is not a legal 1.8.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')`; `B bump rule: the contract leaves 1.8.0 (0 stable-key violation(s), 1 EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make` |
| F3 | `contract_version: "1.9.0"` | `L1 contract_version: expected '1.8.0', got '1.9.0'` |
| F4 | `contract_version` removed | `L1 contract_version: expected '1.8.0', got None`; no L2 line (a missing stable key is not an extra key) |
| F5 | `return-contract.yaml` holds `- a list` | `L0 contract: return-contract.yaml is missing, unparseable or not a mapping` (only line) |
| F6 | `telemetry: [1]` | `L2 stable keys: 'telemetry' must be a mapping, got list` |
| F7 | `adversarial_convergence_score: "0.852"` | `L4 adversarial_convergence_score: expected a float or null, got '0.852'` |
| F8 | `adversarial_convergence_score: 1` | `L4 adversarial_convergence_score: expected a float or null, got 1` |
| F9 | `regression_present: "false"` | `L5 regression_present: expected a real boolean, got 'false'` |
| F10 | `adversarial_unavailable` removed | `L5 adversarial_unavailable: expected a real boolean, got None` |
| F11 | `verification_ran: 1` | `L5 verification_ran: expected a real boolean, got 1` |
| F12 | FX-PANEL-DIR with `reviewers_resolved: 4` | `L6 EV-1: reviewer-cards/ holds 3 card(s), fewer than the required 4 (reviewers_resolved from panel/manifest.json)` |
| F13 | FX-LEGACY with `reviewer-3-card.yaml` deleted (no manifest) | `L6 EV-1: reviewer-cards/ holds 2 card(s), fewer than the required 3 (len(reviewer_cards))` |
| F14 | FX-LEGACY with `reviewer_cards: []` and only `reviewer-1-card.yaml` left | `L6 EV-1: reviewer-cards/ holds 1 card(s), fewer than the required 2 (minimum 2)`; `L7 parity reviewer_cards: panel [] differs from matched legacy ['reviewer-1-card.yaml', 'reviewer-2-card.yaml', 'reviewer-3-card.yaml']` |
| F15 | FX-PANEL-DIR with `panel/manifest.json` = `{"reviewers_resolved": "3"}` | `L6 EV-1: panel/manifest.json is not a JSON object with a positive integer reviewers_resolved` |
| F16 | FX-LEGACY with `adversarial/` removed (no fallback fields) | `L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row)` |
| F17 | P8 without `audit.log` (legacy: P8's variant) | `L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: audit.log F2/F3 row)` |
| F18 | FX-LEGACY with `merge_method: single-reviewer-fallback` written into `adversarial/merged-verdict.yaml` | `L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: merge_method 'single-reviewer-fallback'; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row)` |
| F19 | `t2_vendor_diversity: single` | `L7 parity t2_vendor_diversity: panel 'single' differs from matched legacy 'multi'` |
| F20 | `calibrator_diversity: full` | `L7 parity calibrator_diversity: panel 'full' differs from matched legacy 'degraded'` |

Task 15's acceptance criteria map to P1, P2 (lint passes on the legacy fixture and on the `panel/` copy), F1 and
F2 (fails naming the offending key or value), P2 with F12 (EV-1 with `reviewers_resolved`) and P3 with F13 (EV-1
without a manifest).

Check of this design: every pass and fail case above (P3 is P1 without a manifest, so it ran as P1) was run once
against a throwaway prototype of the checker on copies of the recorded source run; each produced exactly the
lines listed. The prototype is not committed; Task 15 writes the real module.
