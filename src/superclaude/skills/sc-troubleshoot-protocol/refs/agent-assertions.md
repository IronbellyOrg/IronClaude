# Agent structural assertions (calibrator C1-C8, validator A1-A10)

Used in Wave 1.7, Wave 3, and Wave 5.

One list, three consumers: `confidence-calibrator` step 5b, `evidence-validator` responsibility 2b, and the orchestrator's inline fallbacks (SKILL Wave 1.7 step 2 / Wave 5 step 3). All three MUST produce the same flag set on the same inputs; inline/agent parity is required (<!-- evidence-absence: tests/troubleshoot/test_inline_fallback_parity.py not landed until Phase 7 -->). No Bash anywhere: every input an assertion needs is passed in by the orchestrator (see each agent's Inputs). A rule whose input is absent is *skipped* and listed in Notes, never silently passed.

Calibrator C-rules (C1-C8, with C3b after C3) are evaluated by confidence-calibrator after step 5a and before the escalation decision. Validator A-rules (A1-A10) are evaluated by evidence-validator after citation verification (responsibility 2b). Table order is A then C (reconcile X-3).

## Validator

| id | trigger | flag | severity |
|---|---|---|---|
| A1 | definite enum token in Summary/Diagnosis and (max calibrated < 0.50 or token in Grounding Gaps with unobserved/deduced/pending or token absent from captured failing-run output with run/arm provenance in observation_paths; generated reports, cards, producer tables and definitions never count as observations) | `deduced_headline` | partial |
| A2 | diff touches a collector or invocation site and the report omits its linked measurement row, preregistered outcomes or pending reason, or omits the required Next Steps form `The report stays \`partial\` until <row>=<value>`; enabling tasks require linked row IDs and operational verification, not invented causal values; optional rows require informational publication but never a status prerequisite | `instrumentation_without_falsifier` | partial |
| A3 | Timestamp/Date/pushed_at later than artifact mtime + 5 min or equal to T00:00:00Z | `timestamp_invalid` | drop that line |
| A4 | pipeline_hardening_verdict not in {pass, blocked, advisory, not_applicable, blocked-on-authorization} | `verdict_not_in_contract` | partial |
| A5 | candidate-fixes.md says consensus and adversarial_invoked is false and a card with evidence_class in {source_static, doc_static, none} makes a dynamic claim; or the calibration file states the evidence class is none/static | `consensus_on_unobserved` | partial |
| A6 | Reference-context value is not one literal: first exempt exact `n/a` only when that probe has `first_instrumented_run=true`; otherwise accept one numeric/boolean/null literal or one quoted string, and reject conditional prose, unquoted alternatives/lists, blank values and later-run `n/a`. Slashes/commas inside a quoted literal (e.g. a path) are data, not alternatives | `reference_value_not_literal` | FAIL |
| A7 | RUN-SITE is pending-producers at finalize while producers.md has at least one producer row | `run_site_unresolved` | FAIL |
| A8 | OBSERVE-VIA is artifact-file and the captured job log is missing, AND the locus identifies the failing arm as a CI job whose harness result marker is absent at finalize | `ci_verdict_unobserved` | status blocked; Diagnosis begins UNDETERMINED — CI verdict unobserved |
| A9 | A literal Reference-context value differs from an actually captured reference-arm observation, including on the first run; failing-arm output is not a reference observation. Skip comparison for evidenced first-run n/a or an unobserved reference cell; neither proves a control | `probe_suspect` | probe row suspect; Grounding Gap; outcome table skipped (no status change) |
| A10 | capability-verdict is blocked without an Emitter search block establishing usable-capture-routes: 0 with searched channels, truthful raw emitters-found/already-read-files counts and candidate exclusions; a viable permitted-site route must capture the actual datum, not merely name a sink or annotate expected data. Refused/unknown permission is separate from capability | `capability_block_unproven` | partial |

## Calibrator

| id | trigger | flag | severity |
|---|---|---|---|
| C1 | headline enum token and calibrated < 0.50 | `headline_definite_low_confidence` | verdict forced ESCALATE |
| C2 | card excludes an enum without a file:line for that enum's exit statement | `unproven_exclusion:<token>` | Runtime check := 0.0 |
| C3 | control arm cited without `CONTROL-PROOF: yes: <file:line>` | `control_unproven` | Symptom coverage ≤ 0.5 |
| C3b | runs-in is unknown | `locus_unknown` | Runtime check ≤ 0.5 |
| C4 | measurement row missing either preregistered true/false prediction or its outcome mapping (equal predictions and explicitly justified unknown are valid, not proof); enabling task missing its linked measurement IDs or operational verification/rollback | `no_prereg_falsifier` | Fix directness ≤ 0.5 |
| C5 | Timestamp later than card_mtime + 5 min or equal to T00:00:00Z | `timestamp_invalid` | drop that line; timestamp not load-bearing |
| C6 | numeric threshold or bracket asserted in the headline without a bracket= line in bracket.md | `bracket_unproven` | calibrated ≤ 0.3 (cap, applied after the formula) |
| C7 | card names an environment property without citing a 2x2 row | `uncited` | calibrated ≤ 0.5 (cap) |
| C8 | behaviour-definition: row N missing or the row's Status is empty | `behaviour-cite: missing` | calibrated ≤ 0.5 (cap); audit.log line behaviour-cite: missing |

Caps apply after the formula at `refs/escalation-rubric.md:20` (unchanged); record every fired rule in the Stage-2 `structural_flags` row.

## Output shape (both agents, same table)

`## Structural assertions` — `| id | fired | flag | consequence applied | evidence (file:line or "input absent") |`, one row per rule, in the order above. Skipped rules show `fired: skipped`.

## Loading discipline

Passed to agents as `assertions_path`; read by the orchestrator only inside the two inline-fallback branches. Not pre-loaded.
