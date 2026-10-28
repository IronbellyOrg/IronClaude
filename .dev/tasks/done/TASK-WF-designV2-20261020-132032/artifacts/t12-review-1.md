# Task 12 independent spec-compliance review

Governing template: `/config/.claude/skills/sc-implement-protocol/refs/qa.md`, Reviewer contract, Compare the diff, Citations, Verdict, Isolation.

Transport limitation: the independent reviewer was prohibited by its developer instructions from writing report files. The orchestrator preserves the reviewer's returned text here. The reviewer did not create a stub-first report; this file was stubbed before the orchestrator populated its sections. No independent on-disk authoring is claimed.

## Acceptance criteria

| Criterion | Result | Evidence |
|---|---|---|
| T12.AC1 | Met for specified execution: independently observed 67 passed. Parent requirement violations remain. | tests/skills/test_auggie_claim_gate_oracle.py:202 and :225 |
| T12.AC2 | Met: 67 default items, 78 acceptance items; 11 held-back items present only in acceptance collection. | tests/skills/test_auggie_claim_gate_oracle.py:439 |
| T12.AC3 | Met for specified acceptance execution: existing evidence records 78 passed. Reviewer did not re-evaluate held-back outcomes. | tests/skills/test_auggie_claim_gate_oracle.py:440 |
| T12.AC4 | Unmet: family counts, single-field differences and digest pass, but required family and retention meanings are missing. | tests/skills/test_auggie_claim_gate_oracle.py:242; findings 2-4 |
| T12.AC5 | Met: existing heading allowed; untracked and staged added-source synthetic-token rejection checks execute. | tests/skills/test_auggie_claim_gate_oracle.py:395 and :415 |
| T12.AC6 | Met: scratch extracted disposition mutation fails equality. | tests/skills/test_auggie_claim_gate_oracle.py:185 |

## Findings

### 1. IMPORTANT: Unverified refutations override missing evidence

Oracle rows A1/A2 at tests/skills/test_auggie_claim_gate_oracle.py:81-82 choose guard/producer rejection without verification flags. Independent development-record probes observed `guard_blocks=True, guards_verified=False => rejected,A1` and `producer_refuses=True, producer_verified=False => rejected,A2`. Canonical rows require verified guards/producer; missing required verification belongs to A6, unproven (src/superclaude/skills/sc-auggie-review-protocol/refs/claim-gate.md:66-71). Full table-text equality passes while actual admission disagrees.

### 2. IMPORTANT: Known versus unknown provenance family missing

Requirement .dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:610 contrasts a present valid author with missing author/unknown identity. Implemented pair changes `policy_verified` (tests/skills/fixtures/auggie_claim_gate/corpus/development.json:1259,1270) while retaining the supported consequence about a valid known author (:1312). This tests policy documentation, not provenance.

### 3. IMPORTANT: Missing-abstraction structural negative absent

Requirement .dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:607 explicitly requires a missing-abstraction claim with no convention source. The second negative (tests/skills/fixtures/auggie_claim_gate/corpus/development.json:842) sets `convention_verified=false` (:863) but retains the import-cycle claim (:892). Counts and disposition do not supply the specified claim.

### 4. IMPORTANT: Frozen base retention has no default-path security sink

Requirement .dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:652 requires a Critical-tier security sink on a default path. The sole base security-retention item named `base-default-security` (tests/skills/fixtures/auggie_claim_gate/corpus/held-back.json:563) explicitly has `default_path=false` (:600). The label check passes without the property. This is a deficient frozen fixture, not an oracle outcome to tune away. Do not silently modify or re-pin it after acceptance.

### Verification and chronology (reviewer)

Independently re-derived frozen symbols from all eight titles/eighteen reasons using exact word boundaries and baseline whole-word subtraction. Raw matches, subtraction, and symbols were empty; case ids/source SHA matched. Creation times support tokens first, held-back plus hash next, development corpus next, oracle last. Held-back modification time equals creation time, predates oracle; digest matches pin. Reviewed full table conditions/order/dispositions, class text, purity, bundled consequences, harm grading, qualification/confidence/locality, fixture/source boundaries and mutations. Independently ran `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_auggie_claim_gate_oracle.py -q -p no:cacheprovider`: 67 passed. Additional probes used development records only. No full suite, product/ledger/pin edits or held-back outcome probing. Initial hyphenated fixture lookup failed; correct underscore directory then inspected. New-file graph coverage incomplete; source/fixture contents used.

## Extra scope

None found. Snapshot diff appeared to delete pre-existing tests because they are untracked; independent byte comparison against snapshot blobs found ACTUAL_CHANGED_PREEXISTING_TEST_FILES=[] .

## Misunderstood

Provenance contrast implemented as policy verification; missing-abstraction negative implemented as another import-cycle claim; default-path security retention has the right label but default_path=false. Citations in findings 2-4.

## Verdict

Binary: FAIL. Protocol: missing. Keep Task12 incomplete. Resolve development-side defects through the one allowed fix pass; escalate the deficient frozen fixture for explicit resolution rather than modifying/re-pinning it after acceptance.

## Self-Audit

Passing tests were not treated as compliance. Checked actual predicates against table requirements, family meanings against original requirements, retention facts rather than labels, and freeze chronology independently. Those checks exposed four findings. No additional findings were added during delivery.
