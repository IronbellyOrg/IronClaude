# Variant 3: /sc:task QA Architecture (SuperClaude Tier-Classified Executor)

## 1. Architectural Identity

`/sc:task` is a **task-time** QA architecture with **risk-routed verification cost**. It validates individual coding tasks by matching verification depth to a compliance-tier classification, and responds to test failures via a structurally-enforced escalation protocol (TFEP) that prohibits ad-hoc fixes.

## 2. Tier-Classified Verification Routing

### Compliance Tiers

| Tier | Verification Method | Token Cost | Timeout |
|---|---|---|---|
| STRICT | Sub-agent (quality-engineer persona) | 3-5K | 60s |
| STANDARD | Direct test execution | 300-500 | 30s |
| LIGHT | Skip verification | 0 | 0s |
| EXEMPT | Skip verification | 0 | 0s |

### Tier Selection Algorithm

- Priority order: `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)`
- Compound phrase overrides ("quick fix" → LIGHT; "fix security" → STRICT) checked first
- Keyword scoring across 4 buckets (security/data/scope/exploration/trivial/development)
- Context boosters: >2 files → +0.3 STRICT; auth|security|crypto path → +0.4 STRICT; docs|*.md → +0.5 EXEMPT; tests → +0.2 STANDARD
- **Critical Path Override**: paths matching `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always trigger CRITICAL verification REGARDLESS of computed tier
- **Trivial Path Override**: paths matching `*.md`, `docs/`, `*test*.py` MAY skip verification

### Confidence Threshold

- Below 0.70: flag `Requires Confirmation: Yes` (operator must explicitly confirm tier)

## 3. Test Failure Escalation Protocol (TFEP)

### VIOLATION-Level Prohibitions (architectural, not policy)

1. **VIOLATION**: agents MUST NOT fix any code in response to test failures without completing TFEP workflow
2. **VIOLATION**: agents MUST NOT modify test expectations to make failing tests pass without adversarial validation
3. **VIOLATION**: ad-hoc patches derived from test output are PROHIBITED — agent must not read traceback and immediately edit code to resolve

### Permitted Exceptions (MAY fix directly without TFEP)

- Single `ImportError`/`NameError` in test scaffolding agent just wrote, affecting ≤2 tests, error is in test file itself
- Lint/formatting failures (trivially fixable, unambiguous root cause)
- Deprecation warnings (not failures)

### Test Baseline Snapshot (pre-implementation)

- Captures list of existing test files + function names at task start
- On any test failure, classifies each as:
  - **Pre-existing**: name in baseline → regression in EXISTING test → MUST escalate
  - **New**: name NOT in baseline → agent-written → may MAY fix per exceptions
- Classification drives MUST-escalate vs MAY-fix-directly decision

### MUST-Escalate Triggers

- Any **pre-existing test** fails (regression signal — primary trigger)
- **≥3 new tests** fail simultaneously (systemic issue signal)
- **Runtime exceptions in implementation code** (TypeError/AttributeError/KeyError in code under test, not test scaffolding)

### TFEP Execution Flow

1. **Halt + Freeze**: STOP testing; FREEZE implementation; no further code changes
2. **Failure Context**: build `failure_context.yaml` with test names, files, full traceback, expected vs actual, changes made, task description, baseline, escalation count
3. **Forensic Invocation**: 1st trigger → `/sc:forensic --tier light --intent triage` (~5-8K); 2nd → `--tier standard` (~15-20K); 3rd → **FULL STOP**, report to user
4. **Consume Forensic Return Contract**:
   - `test_is_wrong: true` → present to USER for review; do NOT auto-edit tests
   - `status: success` → tasklist insertion (Step 5)
   - `status: partial` OR `recommended_escalation != "none"` → increment escalation_count, return to Step 3
   - `status: failed` → report to user, halt
5. **Tasklist Insertion**: read `tasklist_insertion_path`; insert `## Failure Remediation Plan (Adjudicated)` BEFORE existing test/verification tasks; preserve original structure (append, don't replace)
6. **Resume**: `--compliance strict` from inserted remediation tasks; re-run original test suite; pass → produce incident report; fail → increment, return to Step 2

### Escalation Budget

- 1st TFEP trigger → ~5-8K tokens
- 2nd TFEP trigger → ~15-20K tokens
- 3rd TFEP trigger → 0 tokens (FULL STOP)

### Incident Reporting

After each TFEP resolution (success or escalation), `tfep-incident-report.md` is committed to git alongside forensic artifacts.

## 4. Architectural Invariants

- **Verification cost matched to risk**: tier classification is the routing axis; LIGHT/EXEMPT skip is intentional
- **No ad-hoc fixes**: structurally enforced via VIOLATION-level prohibitions; the architecture refuses to allow the unsafe shortcut
- **Regression detection is automatic**: baseline snapshot distinguishes regressions from new-test failures without operator input
- **Tests-are-wrong requires user adjudication**: never auto-edit tests, even when forensic concludes tests are outdated

## 5. Operational Characteristics

- Token cost: ~3-5K STRICT, ~300-500 STANDARD, ~0 LIGHT — distribution-weighted total is the lowest of the three variants
- Wall-clock impact: bounded by tier timeout (60s STRICT, 30s STANDARD); LIGHT/EXEMPT instant
- Applicable to: individual coding tasks; tier classification works across code/docs/config but Critical Path Override is path-string-keyword-specific
- Failure modes: tier misclassification (mitigated by confidence threshold + Critical Path Override); forensic agent crash (not explicitly addressed)

## 6. Theory of Defects

Defects in coding tasks are NOT uniformly distributed across tasks — security/data/migration tasks contain ~80% of catastrophic risk in <20% of tasks. Spending the same verification budget on every task is wasteful. Tier classification routes budget to where it matters. The TFEP prohibition reflects an empirical pattern: AI agents systematically gravitate toward test-modification when given freedom (Goodhart's law). Architectural prohibition is more reliable than instructional restraint.

## 7. Documented Limitations

- Tier classification is keyword/path heuristic — semantically blind to domain-specific criticality (e.g., a "models" path-keyword catches ORM models but might miss domain-significant types living outside `models/`)
- LIGHT/EXEMPT skip means a doc-only change that structurally breaks a downstream consumer gets zero detection
- No formal protection against QA-agent hallucination (a quality-engineer false-positive flows through with no rebuttal mechanism)
- TFEP forensic-ladder relies on `/sc:forensic` being available; no fallback
- No plan-time validation — defects in the task specification itself are not caught until execution
- No cross-task interaction-effect detection (each task validated in isolation)
- Critical Path Override is keyword/path-string only — semantic over- and under-catch both possible
