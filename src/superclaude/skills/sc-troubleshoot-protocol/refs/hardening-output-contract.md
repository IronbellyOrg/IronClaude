# Hardening Output Contract

This ref defines the additive, versioned output contract for the Pipeline Hardening Closure mode: the result-field schema, the deterministic verdict-aggregation truth table, the HC5 decision-to-status mapping, the backtest-status-vs-verdict mapping, and the one-way waiver / no-re-greening latch with its downstream propagation rule.

`pipeline_hardening_verdict` is the **five-token** enum `pass | blocked | advisory | not_applicable | blocked-on-authorization`. `advisory` is a first-class outcome and MUST NOT be removed: the §5.4 truth table emits `advisory` in rows 5 and 6 (the anti-theatre design distinguishes `blocked` = hard fail from `advisory` = rationalized-N/A or accepted-substitute proof). Any artifact that drops `advisory` or uses a three-token enum is a defect. `blocked-on-authorization` is valid only when an emitter row exists in the diagnosability tasklist AND `re-run permitted: no` (explicit refuse). Closed table for `re-run permitted`: `yes` = authorized same-shell/remote-command already granted this run; `no` = issue/flags/prior artifact explicitly refuse a re-run; otherwise `unknown`. `unknown` maps to pending rows and never sets `blocked-on-authorization`. Never AskUserQuestion. It is set by the Wave 1.6 S1.6.4 status-precedence rule, takes precedence over the §5.4 aggregation, carries report `status: blocked` (never `partial`), and the tasklist file is still written. `capability-verdict: blocked` is a tasklist HEADER value, not a contract enum value. Any other string (e.g. `blocked_pending_retry_run`) fails validator A4.

## Output contract field schema (§5.5)

All fields are **additive** under `contract_version`; existing consumers that read only prior result fields are unaffected (NFR-6 backward-compat).

| Field | Type | Required | Default | Nullability | Producer | Consumer Behavior If Missing |
|-------|------|----------|---------|-------------|----------|------------------------------|
| `contract_version` | semver string | yes | `1.2.0` | non-null | FR-13 | Treat missing as legacy contract; do not infer hardening pass |
| `pipeline_hardening_applicable` | bool | yes | `false` | non-null | HC0 | Missing ⇒ legacy/unknown; report must not claim closure |
| `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable\|blocked-on-authorization` | yes when applicability known OR S1.6.4 authorization block set | `not_applicable` | non-null | S1.6.4 authorization precedence; otherwise HC aggregation | Missing with applicable=true ⇒ `blocked`; an authorization result must be emitted even before HC0 |
| `waiver_status` | enum `none\|latched` | yes | `none` | non-null | HC1-HC5 / FR-12 | Missing with any waiver marker ⇒ `blocked` |
| `backtest_status` | enum `not_run\|partial\|complete` | yes | `not_run` | non-null | NFR-1 replay suite | Missing ⇒ treat production-facing signoff as `advisory` |
| `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | yes | `not_required` | non-null | HC5 | Missing when HC5 required ⇒ `blocked` |
| `runtime_entrypoint_card_path` | absolute path string | required when HC1 runs | `null` | nullable before HC1 | HC1 | Missing when HC1 required ⇒ `blocked` |
| `contract_ledger_path` | absolute path string | required when HC2 runs | `null` | nullable before HC2 | HC2 | Missing when HC2 required ⇒ `blocked` |
| `unmask_sweep_path` | absolute path string | required when HC3 runs | `null` | nullable before HC3 | HC3 | Missing when HC3 required ⇒ `blocked` |
| `effective_input_card_path` | absolute path string | required when HC4 runs | `null` | nullable before HC4 | HC4 | Missing when HC4 required ⇒ `blocked` |
| `known_escapes_caught` | list of objects `{escape_id, wave, card_path, status}` | yes | `[]` | non-null list | HC0/closure | Missing/empty ⇒ no coverage claim |

`contract_version` is the **contract semver** (default `1.2.0`; `1.1.0` added the TFEP adapter fields, `1.2.0` adds `status: blocked` and `pipeline_hardening_verdict: blocked-on-authorization`); `execution_locus_card_path` lives on the skill Output Contract, not this schema. It is monotonic and additive-only within a major version. It is **distinct from** `target_release` (the release version this work ships in), which is a separate decision and is NOT stamped by this contract.

## Verdict aggregation truth table (§5.4)

The aggregation function is deterministic and evaluated after HC0–HC5. `FAIL` is sticky and outranks advisory waiver handling. `waiver_status=latched` is a one-way latch and is checked before any downstream success signal. Rows are evaluated in priority order; the first matching row wins.

| Condition Priority | Input Condition | Output Verdict | Report Language | Downstream Override Allowed? |
|--------------------|-----------------|----------------|-----------------|------------------------------|
| 1 | `pipeline_hardening_applicable=false` AND HC0 has reason + boundary scan | `not_applicable` | `Pipeline hardening not applicable: <reason>` | No |
| 2 | Any HC1-HC5 status is `FAIL` | `blocked` | `NOT PROVEN — failed hardening wave: <wave>` | No |
| 3 | `waiver_status=latched` AND any mandatory probe absent/waived without accepted substitute | `blocked` | `NOT PROVEN — mandatory runtime proof waived or absent` | No |
| 4 | Any HC1-HC5 status is `N/A` without rationale | `blocked` | `NOT PROVEN — unrationalized N/A: <wave>` | No |
| 5 | `waiver_status=latched` AND all mandatory probes have accepted substitutes + rationale AND no HC-status is `FAIL` | `advisory` | `ADVISORY — closure relies on waived/substituted proof` | No |
| 6 | Any HC1-HC5 status is `N/A` with valid rationale and no failures/latch | `advisory` | `ADVISORY — scoped closure with rationalized N/A` | No |
| 7 | HC0 applicable, all required HC1-HC5 statuses `PASS`, and `waiver_status=none` | `pass` | `Pipeline hardening closure proven` | No |

When any required proof is absent, the rendered report uses **`NOT PROVEN`** blockers (stronger than ordinary confidence language), per FR-13.

## HC5 decision-to-status mapping (§5.4)

| HC5 Decision | HC5 Status | Waiver Status Effect | Notes |
|-------------|-----------|----------------------|-------|
| `performed` | `PASS` | `none` | Required off-path review completed and consumed the effective-input proof. |
| `not_required` | `PASS` | `none` | Pass-equivalent only when the boundary-risk scan proves no HC5 trigger applies; no required proof is missing. |
| `required` | `FAIL` | `none` | Off-path review was required but not performed or validly waived. |
| `waived_with_rationale` | `N/A` with rationale | `latched` | Valid waiver downgrades the final verdict through the truth table; an invalid waiver maps to `FAIL`. |

## Downstream no-override rule

Downstream `task-builder`, `sc:reflect`, `sc:adversarial`, and report-rendering stages may append findings, but they may **not** convert `blocked`/`advisory` into `pass`/`success`. If a downstream stage has its own success enum, the rendered result is `success_with_hardening_blocker` or `success_with_hardening_advisory`, never plain `success`, whenever this table returns `blocked` or `advisory`.

The same downstream consumers MUST preserve `blocked-on-authorization` plus its explicit authorization blocker independently of applicability or aggregation. Where a separate success enum must be rendered, use `success_with_hardening_blocker` with the original fifth verdict and refusal reason, never plain `pass`/`success`; the diagnostic status remains blocked or higher-precedence failed. An early authorization exit may precede HC0: default `pipeline_hardening_applicable=false` is not a boundary-scan decision. Render `HC0 not run — applicability unassessed`, retain the tasklist/refusal evidence, and do not fabricate HC cards or a justified not-applicable reason. This pre-aggregation rule does not alter the seven truth-table rows or the waiver latch.

## Backtest status vs run-level verdict (§5.4)

`pipeline_hardening_verdict` is the run-level HC0–HC5 closure verdict. `backtest_status` is the separate coverage-validation state for NFR-1 (whether the E1–E5 replay suite has validated the gates). REPORT.md renders both so consumers do not confuse a clean HC0–HC5 run with validated E1–E5 catch-rate coverage.

| Backtest Status | Meaning | Production-Facing Pipeline-Health Signoff |
|-----------------|---------|-------------------------------------------|
| `not_run` | No E1-E5 replay suite has run against the built hardening gates | `advisory` even if `pipeline_hardening_verdict=pass` |
| `partial` | Some, but not all, E1-E5 replay scenarios have passed | `advisory` with missing escape IDs listed |
| `complete` | E1-E5 replay scenarios all pass against the built gates | May mirror `pipeline_hardening_verdict` |

## Waiver / no-re-greening latch and anti-inflation (FR-12)

- **One-way latch (`waiver_status`).** A waived or absent mandatory runtime probe sets `waiver_status` from `none` to `latched`. The transition is one-way: `latched` never resets to `none`. Once `latched`, `pipeline_hardening_verdict ∈ {blocked, advisory}` and no later `task-builder`, `sc:reflect`, or `sc:adversarial` stage may upgrade it to `pass`/`success`.
- **Set-once applicability.** `pipeline_hardening_applicable` is set exactly once by HC0; if `true`, HC1–HC5 must run or be waived.
- **Production-facing signoff.** Production-facing pipeline-health signoff FAILs when a mandatory runtime probe is absent or `N/A` without rationale.
- **Anti-inflation.** An escape ID may appear in `known_escapes_caught` only if a passing wave/card is cited that would catch it (`status=PASS`). An un-earned membership that inflates coverage is a defect.
