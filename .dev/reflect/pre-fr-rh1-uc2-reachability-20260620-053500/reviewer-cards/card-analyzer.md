# Tier-2 Reflect Reviewer Card — Analyzer

## Scope

- SPEC: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md`
- TASKLIST: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/TASK-RF-uc2-reachability-gate-20260620-043410.md`
- Lens: UC-1 PRE-EXECUTION coverage/gap audit, analyzer stance.

## Per-obligation coverage table

| R# | Covered? | Implement item line(s) | Verify item line(s) | Notes |
|---|---:|---|---|---|
| R1 — real-boot-only Regression | Yes | Tasklist lines 109-110 constrain real-boot-only proof and telemetry-only skips; lines 152, 156, 158, and 160 require protocol/taxonomy/template edits preserving real-boot-only Regression and static-signal-only `unproven`. | Lines 196 and 200 add consumer/eval assertions that proxy/oracle/static evidence cannot prove Regression; line 224 final semantic QA explicitly checks real-boot-only Regression. | Covered. Verification is strong for negative proof-bar safety. Positive real-boot-proven Regression eval is conditional at line 200 (`if implementable`), which is acceptable under the spec's own R6 allowance but leaves positive-path coverage weaker than the negative path. |
| R2 — telemetry-only `--no-reachability` | Yes | Lines 110, 152, 156, 160, and 174 define telemetry-only disablement with no Grounding Gap/status effect; lines 180-184 implement wrapper/docs disable plumbing. | Lines 194, 196, 198, 200, 202, and 226 verify skip fixtures, consumer tests, help/prompt/docs parity, producer eval skip, pytest execution, and wrapper actionability. | Covered with dedicated tests and eval coverage. |
| R3 — telemetry-only spec/tasklist absent | Yes | Lines 110, 152, 156, and 160 require spec/tasklist absence to be a telemetry-only skip with no gap/status effect. | Lines 194 and 196 require fixtures/tests for `spec-and-tasklist-absent`; line 200 adds `uc2-reachability-missing-inputs-skip`; line 224 final semantic QA checks telemetry-only skips. | Covered with both consumer and producer verification. |
| R4 — contract `1.6.0`; `1.5.0` D13-only | Yes | Line 111 states the stable contract rule; lines 142, 154, 160, 166, and 192 implement requirements/protocol/template/grader/fixture updates for `1.6.0` while preserving `1.5.0` as D13-only. | Lines 196 and 200 assert `1.6.0` in consumer/eval tests; line 220 final QA checks `contract_version: "1.6.0"`, exact R7 fields, and D13-only `1.5.0`. | Covered with dedicated schema/contract verification. |
| R5 — wrapper plumbing and docs parity | Yes | Lines 174-184 implement slash-command row, wrapper model/config/Click/tmux forwarding, `_build_prompt()` exact-once disabled forwarding, and docs. | Lines 198 and 202 add help/prompt/docs/tmux tests and pytest execution; lines 186 and 226 add phase/final QA for wrapper drift. | Covered strongly; includes both implementation surfaces and tests requested by spec. |
| R6 — producer-level eval fixture distinct from consumer fixtures | Yes | Lines 190 and 200 explicitly distinguish consumer tolerance from producer behavior and require active FR-RH1 eval cases exercising Step 5.6 output. | Lines 204 and 206 run producer eval validation and QA distinctness; line 222 final QA assumes tests are consumer-only unless producer behavior is proven. | Covered. Strong adversarial language prevents substituting consumer fixtures for producer evals. |
| R7 — exact seven reachability fields and consistency | Yes | Lines 154, 160, 166, and 192 require the exact stable fields `reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`, `reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, and `reachability_skip_reason`, plus consistency rules. | Lines 196 and 200 require tests/eval assertions over the fields; line 220 final QA checks exact R7 fields. | Covered with exact field names; no extra stable `oracle_*` schema is allowed at lines 192 and 196. |
| R8 — bounded cost, not zero | Yes, weak verification | Lines 164 and 142 require bounded estimates/caps and removal of zero-token/zero-turn claims; line 136 includes bounded cost in the requirements map. | Line 144 verifies stale zero-cost strings in the requirements artifact; line 224 final semantic QA checks bounded cost. | Covered, but verification is mostly prose/search/QA rather than a dedicated machine test. This is acceptable for a documentation/cost-contract obligation, but weaker than R2/R5/R7. |
| R9 — advisory-only semantic fallback; only explicit `durable_sink:`/`@sink` blocks | Yes | Lines 109, 152, 156, 158, 160, 166, and 174 require explicit annotated-sink eligibility and semantic fallback as advisory telemetry only. | Lines 194 and 196 add semantic-fallback-only fixtures/tests; line 200 requires no false Regression on semantic evidence; line 224 final semantic QA checks advisory-only semantic fallback. | Covered with dedicated semantic-fallback negative tests/eval/QA. |

## Coverage

- Covered obligations: 9 / 9
- coverage_pct: 1.00

## Gaps / weak spots / violations

| Severity | Type | Obligation | Finding |
|---|---|---|---|
| Low | Weak verification | R8 | Bounded-cost verification relies on requirements-string search and qualitative QA (tasklist lines 144 and 224), not a dedicated schema/test assertion over the cost profile. This is probably sufficient because R8 is largely documentation/cost-envelope work, but it is weaker than the other obligations. |
| Low | Weak verification | R1 | Positive real-boot Regression producer eval is conditional (`if implementable`) at line 200. The spec allows this as a follow-up if safe boot cannot run, and negative proof-bar verification is covered; still, the positive `unreachable` path may remain less directly tested. |

## Spec-violation scan

No task item was found that contradicts the spec. I found no item that lets a static signal set Regression, no item that lets `--no-reachability` or `spec-and-tasklist-absent` create a Grounding Gap/status effect, and no item that lets semantic fallback become a v1 blocking trigger. The tasklist repeatedly encodes the safe semantics at lines 109-111, 152-160, 174-184, 194-200, and 224-226.

## Best-practice grade

best_practice_grade: 4.5 / 5

Rationale: the tasklist is unusually comprehensive and maps every R1-R9 obligation to implementation and verification work, including producer-level evals and adversarial QA gates. The grade is not 5 only because bounded-cost verification is not a dedicated executable check and the positive real-boot Regression path is conditional.

SELF_CONFIDENCE: 0.93
