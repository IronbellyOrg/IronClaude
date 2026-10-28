# Task 12 independent review after the single fix pass

Governing template: `/config/.claude/skills/sc-implement-protocol/refs/qa.md`, Reviewer contract, Compare the diff, Citations, Verdict, Isolation.

Transport limitation: the fresh independent reviewer's agent instructions prohibit writing report Markdown files. The orchestrator created this skeleton and will preserve the reviewer's returned sections. No independent on-disk authoring is claimed.

## Acceptance criteria

Reviewer: fresh adversarial review against Q0 tree `03b0db3359f806c5db39a3631b24c0d99908b957` and live Task12 brief, parent requirements, canonical admission reference and rubric. No delivery/product, ledger, pin, spec, global or held-back file modified.

- T12.AC1: Met for execution, not sufficient for full compliance. Independently ran default module: 74 passed. Outcome assertion/parametrization: tests/skills/test_auggie_claim_gate_oracle.py:208,231.
- T12.AC2: Met. Independently collected 74 default tests without held-back outcome tests. Acceptance collection records 85 items including 11 held-back tests. Guard: tests/skills/test_auggie_claim_gate_oracle.py:509. Post-fix collection evidence inspected; acceptance outcomes not rerun to probe predicates.
- T12.AC3: Met for recorded acceptance execution. ./artifacts/t12-fix-acceptance.log:85-97 records all 11 held-back outcomes and 85 passed after fixes. Does not establish missing retention property.
- T12.AC4: Mechanical family counts, eligible held-back pairs, retention labels and original digest match. Complete specified corpus unmet: default-path security retention missing (finding 1). Family/digest checks at tests/skills/test_auggie_claim_gate_oracle.py:248-282 validate labels but not missing property.
- T12.AC5: Met. Legal template heading/fixture-source scopes: tests/skills/test_auggie_claim_gate_oracle.py:440-473. Temporary token-file mutation exercises untracked source and staged single-plus lines at :485-500. Passed independently.
- T12.AC6: Met. Scratch extracted disposition mutation raises expected equality failure: tests/skills/test_auggie_claim_gate_oracle.py:191-198. Passed independently.

## Findings

### 1. IMPORTANT, Missing: required default-path Critical security retention absent

The base retention requirement includes a Critical security sink on a default path, not merely any exploitable example (.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:652). Task12 requires that set through its brief and parent requirement.

The sole base-list security case is named `base-default-security`, but its authoritative fixture says `default_path=false` (tests/skills/fixtures/auggie_claim_gate/corpus/held-back.json:563-600). Its base/security_sink labels are at :627-628. Other security examples do not supply a default-path base-list case; the retained default-path null dereference is correctness, not a security sink.

The coverage check only compares retention label sets (tests/skills/test_auggie_claim_gate_oracle.py:269-277). Passing label/acceptance checks cannot supply the missing property. This is a frozen-fixture coverage defect, not a reason to tune admission outcomes.

No change or re-pin was made. After the one permitted fix pass, this unresolved requirement forces FAIL. Escalate the frozen-fixture conflict for explicit operator resolution, not another unapproved repair or silent replacement.

## Extra scope

None found. The added second structural positive is the development comparison needed to test the separately required missing-abstraction negative without corrupting the cycle contrast. Managed execution evidence is not a product addition.

### Verification and resolved prior findings

Reviewer formed independent conclusions from live requirements, code, losslessly factored complete development fixtures, held-back data and targeted execution before consulting the old review.

- Actual guard/seam predicates require verification (tests/skills/test_auggie_claim_gate_oracle.py:85-88). Independent development probes: verified guards/producers yield A1/A2 rejection; missing guard/entrypoint/producer verification yields A6 unproven. Regression tests: :285-296.
- Provenance contrast changes actual author input under verified schema. Known input yields defect, missing author A2 rejection, unverified producer A6 unproven (:299-316). Independent development-only execution confirmed.
- Both cycle cases preserved; separate missing-abstraction contrast added. Existing cycle admitted, labeled pre-existing, tier-dropped; missing-abstraction negative lacks convention, is unproven (:319-344). Confirmed with development-only execution.
- Checked full table conditions/order/dispositions/fallback/class rules plus actual predicates, priority, policy challenge, prerequisite violation, current/as-submitted state, class evidence, mocked-only paths and incomplete refutations. No remaining predicate mismatch established.
- Literal-contract pair both admitted: positive admits incorrect success; negative excludes it with A6, grades Medium for narrow instruction failure. Structural/runtime and unsupported-loss bundles grade only supported harm. Checked harm floors, security/data-integrity/Critical exemptions, qualification cap, omitted confidence downgrade and locality.

### Frozen tokens, isolation and scope

Independently derived tokens from eight titles/eighteen reasons using exact word-boundary alternatives/backtick spans/baseline subtraction. Raw tokens/subtraction/symbols empty: permitted derivation, not evidence of meaningful symbol ban. All 26 case ids, PR numbers and source SHA matched (./artifacts/t12-frozen-tokens.log:163-167).

Checked fixture/source scopes, single-plus added lines excluding triple-plus headers, untracked source inclusion, legal template heading, synthetic-token rejection and PR forms. No held-back item sent to admit/grade by reviewer. Read held-back only for coverage/anti-overfit/freeze; existing acceptance logs supplied outcomes.

Creation times support tokens 2026-10-21 21:34:39 UTC, held-back/hash 21:35:19, oracle 21:38:24. Held-back birth/modification times equal; SHA256 `d54be745f4f9b8f9e0804f8f69ae6b5efc0f9f209123fb432c28015420fcef71` matches original pin and oracle constant. No re-pin/modification.

Compared snapshot bytes rather than treating untracked prior files as deleted: 153 apparent prior deletions byte-identical to Q0; only progress ledger differed among snapshot paths. Four new delivery files: oracle, token file, two corpus files. No Task11 re-review or unrelated repair.

Negative evidence/limits: overly broad snapshot inspection exceeded foreground timeout and stopped. Bounded archive-based comparison of 154 snapshot paths completed and supplied result above. Lint logs show ruff could not spawn; no lint pass claimed, not an acceptance criterion. Graph reported changed oracle metadata/partial rubric parse; direct source supplied evidence. No full suite, live model evaluation or external write.

## Misunderstood

Frozen security-retention case has required label but not default-path fact. Same shortfall as finding1, not an additional finding. Former provenance/policy and abstraction/cycle substitutions corrected.

## Verdict

Binary: FAIL. Protocol: missing.

One required retention property unresolved after the one allowed fix pass. No conditional pass. Keep Task12 incomplete; halt under post-fix QA rule. Obtain explicit operator resolution of the frozen-fixture conflict. Do not infer permission to modify pin, fixture, plan or specification.

## Self-Audit

Did not infer compliance from green tests or producer report. Checked actual predicates/verification gates, contrast input differences, retention properties, supported-harm grading, exact token derivation/scopes, snapshot bytes, definition-time collection guard and original freeze chronology. Independently observed 74 default tests pass; existing post-fix acceptance records 85 passed. Green results do not close absent default-path security fixture. Exactly one unresolved finding. No delivery, product, pin, ledger, spec, global or held-back file edited by reviewer.
