# Hardening Output Contract

This ref defines the additive, versioned output contract for the Pipeline Hardening Closure mode: the result-field schema, the deterministic verdict-aggregation truth table, the H5 decision-to-status mapping, the backtest-status-vs-verdict mapping, and the one-way waiver / no-re-greening latch with its downstream propagation rule.

`pipeline_hardening_verdict` is the **four-token** enum `pass | blocked | advisory | not_applicable`. `advisory` is a first-class outcome and MUST NOT be removed: the §5.4 truth table emits `advisory` in rows 5 and 6 (the anti-theatre design distinguishes `blocked` = hard fail from `advisory` = rationalized-N/A or accepted-substitute proof). Any artifact that drops `advisory` or uses a three-token enum is a defect.

## Output contract field schema (§5.5)

All fields are **additive** under `contract_version`; existing consumers that read only prior result fields are unaffected (NFR-6 backward-compat).

| Field | Type | Required | Default | Nullability | Producer | Consumer Behavior If Missing |
|-------|------|----------|---------|-------------|----------|------------------------------|
| `contract_version` | semver string | yes | `1.0.0` | non-null | FR-13 | Treat missing as legacy contract; do not infer hardening pass |
| `pipeline_hardening_applicable` | bool | yes | `false` | non-null | H0 | Missing ⇒ legacy/unknown; report must not claim closure |
| `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | yes when applicable known | `not_applicable` | non-null | aggregation | Missing with applicable=true ⇒ `blocked` |
| `waiver_status` | enum `none\|latched` | yes | `none` | non-null | H1-H5 / FR-12 | Missing with any waiver marker ⇒ `blocked` |
| `backtest_status` | enum `not_run\|partial\|complete` | yes | `not_run` | non-null | NFR-1 replay suite | Missing ⇒ treat production-facing signoff as `advisory` |
| `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | yes | `not_required` | non-null | H5 | Missing when H5 required ⇒ `blocked` |
| `runtime_entrypoint_card_path` | absolute path string | required when H1 runs | `null` | nullable before H1 | H1 | Missing when H1 required ⇒ `blocked` |
| `contract_ledger_path` | absolute path string | required when H2 runs | `null` | nullable before H2 | H2 | Missing when H2 required ⇒ `blocked` |
| `unmask_sweep_path` | absolute path string | required when H3 runs | `null` | nullable before H3 | H3 | Missing when H3 required ⇒ `blocked` |
| `effective_input_card_path` | absolute path string | required when H4 runs | `null` | nullable before H4 | H4 | Missing when H4 required ⇒ `blocked` |
| `known_escapes_caught` | list of objects `{escape_id, wave, card_path, status}` | yes | `[]` | non-null list | H0/closure | Missing/empty ⇒ no coverage claim |

`contract_version` is the **contract semver** (default `1.0.0`); it is monotonic and additive-only within a major version. It is **distinct from** `target_release` (the release version this work ships in), which is a separate decision and is NOT stamped by this contract.

## Verdict aggregation truth table (§5.4)

The aggregation function is deterministic and evaluated after H0–H5. `FAIL` is sticky and outranks advisory waiver handling. `waiver_status=latched` is a one-way latch and is checked before any downstream success signal. Rows are evaluated in priority order; the first matching row wins.

| Condition Priority | Input Condition | Output Verdict | Report Language | Downstream Override Allowed? |
|--------------------|-----------------|----------------|-----------------|------------------------------|
| 1 | `pipeline_hardening_applicable=false` AND H0 has reason + boundary scan | `not_applicable` | `Pipeline hardening not applicable: <reason>` | No |
| 2 | Any H1-H5 status is `FAIL` | `blocked` | `NOT PROVEN — failed hardening wave: <wave>` | No |
| 3 | `waiver_status=latched` AND any mandatory probe absent/waived without accepted substitute | `blocked` | `NOT PROVEN — mandatory runtime proof waived or absent` | No |
| 4 | Any H1-H5 status is `N/A` without rationale | `blocked` | `NOT PROVEN — unrationalized N/A: <wave>` | No |
| 5 | `waiver_status=latched` AND all mandatory probes have accepted substitutes + rationale AND no H-status is `FAIL` | `advisory` | `ADVISORY — closure relies on waived/substituted proof` | No |
| 6 | Any H1-H5 status is `N/A` with valid rationale and no failures/latch | `advisory` | `ADVISORY — scoped closure with rationalized N/A` | No |
| 7 | H0 applicable, all required H1-H5 statuses `PASS`, and `waiver_status=none` | `pass` | `Pipeline hardening closure proven` | No |

When any required proof is absent, the rendered report uses **`NOT PROVEN`** blockers (stronger than ordinary confidence language), per FR-13.

## H5 decision-to-status mapping (§5.4)

| H5 Decision | H5 Status | Waiver Status Effect | Notes |
|-------------|-----------|----------------------|-------|
| `performed` | `PASS` | `none` | Required off-path review completed and consumed the effective-input proof. |
| `not_required` | `PASS` | `none` | Pass-equivalent only when the boundary-risk scan proves no H5 trigger applies; no required proof is missing. |
| `required` | `FAIL` | `none` | Off-path review was required but not performed or validly waived. |
| `waived_with_rationale` | `N/A` with rationale | `latched` | Valid waiver downgrades the final verdict through the truth table; an invalid waiver maps to `FAIL`. |

## Downstream no-override rule

Downstream `task-builder`, `sc:reflect`, `sc:adversarial`, and report-rendering stages may append findings, but they may **not** convert `blocked`/`advisory` into `pass`/`success`. If a downstream stage has its own success enum, the rendered result is `success_with_hardening_blocker` or `success_with_hardening_advisory`, never plain `success`, whenever this table returns `blocked` or `advisory`.

## Backtest status vs run-level verdict (§5.4)

`pipeline_hardening_verdict` is the run-level H0–H5 closure verdict. `backtest_status` is the separate coverage-validation state for NFR-1 (whether the E1–E5 replay suite has validated the gates). REPORT.md renders both so consumers do not confuse a clean H0–H5 run with validated E1–E5 catch-rate coverage.

| Backtest Status | Meaning | Production-Facing Pipeline-Health Signoff |
|-----------------|---------|-------------------------------------------|
| `not_run` | No E1-E5 replay suite has run against the built hardening gates | `advisory` even if `pipeline_hardening_verdict=pass` |
| `partial` | Some, but not all, E1-E5 replay scenarios have passed | `advisory` with missing escape IDs listed |
| `complete` | E1-E5 replay scenarios all pass against the built gates | May mirror `pipeline_hardening_verdict` |

## Waiver / no-re-greening latch and anti-inflation (FR-12)

- **One-way latch (`waiver_status`).** A waived or absent mandatory runtime probe sets `waiver_status` from `none` to `latched`. The transition is one-way: `latched` never resets to `none`. Once `latched`, `pipeline_hardening_verdict ∈ {blocked, advisory}` and no later `task-builder`, `sc:reflect`, or `sc:adversarial` stage may upgrade it to `pass`/`success`.
- **Set-once applicability.** `pipeline_hardening_applicable` is set exactly once by H0; if `true`, H1–H5 must run or be waived.
- **Production-facing signoff.** Production-facing pipeline-health signoff FAILs when a mandatory runtime probe is absent or `N/A` without rationale.
- **Anti-inflation.** An escape ID may appear in `known_escapes_caught` only if a passing wave/card is cited that would catch it (`status=PASS`). An un-earned membership that inflates coverage is a defect.
