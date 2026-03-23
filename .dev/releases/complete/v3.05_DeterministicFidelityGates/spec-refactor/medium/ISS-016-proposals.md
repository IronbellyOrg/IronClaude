# ISS-016 Refactoring Proposals

**Issue**: FR-7/FR-8 circular interface not designed. FR-7 (Convergence Gate) triggers FR-8 (Regression Detection) when structural HIGHs increase. FR-8 produces findings that feed back into FR-7's registry and budget tracking. This circular dependency requires an explicit interface contract, including clear specification that the regression validation flow counts as one "run" toward the budget of 3.

**Source**: Compatibility Report Section 7g (FR-7/FR-8 Circular Interface)

**Type**: Omission (interface contract between FR-7 and FR-8 never specified)

**Pre-existing resolutions checked**: No CRITICAL or HIGH proposals address this issue. ISS-001 rewrites FR-7's description/baseline but does not address the FR-7/FR-8 interface. The existing spec text acknowledges the budget accounting rule (FR-8 AC item: "This entire flow counts as one 'run' toward the budget of 3") but does not specify the calling contract, return type, or how FR-8's results re-enter FR-7's evaluation loop.

---

## Proposal #1: Add FR-7/FR-8 Interface Contract Subsection (RECOMMENDED)

**Rationale**: The spec already states _what_ should happen (FR-8 counts as one run, results update registry) but never specifies _how_ FR-7 calls FR-8 or what FR-8 returns. This proposal adds a concrete interface contract as a new subsection within FR-7, making the circular dependency explicit and implementable without ambiguity.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Insert after** FR-7 Acceptance Criteria (after line 366, before the `**Dependencies**` line) and before the `---` separator preceding FR-8:

**New text to add**:

```markdown
#### FR-7.1: FR-7/FR-8 Interface Contract

FR-7 and FR-8 have a circular dependency: FR-7 detects regression and
delegates to FR-8; FR-8 validates findings and writes results back to
the registry that FR-7 evaluates. This subsection specifies the
interface contract.

**Calling convention**:
```python
def handle_regression(
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
    run_number: int,
) -> RegressionResult
```

**Return contract**:
```python
@dataclass
class RegressionResult:
    validated_findings: list[Finding]     # After debate verdicts applied
    debates_run: int                       # Number of adversarial debates executed
    consolidated_report_path: Path         # Path to fidelity-regression-validation.md
    registry_updated: bool                 # True if registry.save() was called
```

**Lifecycle within the convergence loop**:
1. `execute_fidelity_with_convergence()` calls `_check_regression(registry)` after each run
2. If regression detected: call `handle_regression(registry, ...)` — this is FR-8's entry point
3. `handle_regression()` spawns 3 parallel agents, merges findings, runs adversarial debates, and calls `registry.merge_findings()` + `registry.save()` internally
4. `handle_regression()` returns `RegressionResult` — it does NOT increment the run counter
5. The calling convergence loop increments the run counter ONCE for the entire regression flow
6. After `handle_regression()` returns, FR-7 evaluates `registry.get_active_high_count()` as normal
7. If budget (3 runs) is exhausted after the regression-containing run, halt

**Budget accounting rule**: The regression validation flow (spawn + merge + debate) counts as part of the run that triggered it, not as a separate run. Example:
- Run 1: 5 structural HIGHs → remediate → Run 2: 7 structural HIGHs (regression!)
- FR-8 activates within Run 2's scope → validates → updates registry
- Run 2 is now complete (with FR-8's validated results). Budget: 2/3 used.
- Run 3 proceeds if needed. Budget: 3/3 used. Final.

**Ownership boundary**:
- FR-7 owns: run counter, budget enforcement, pass/fail decision, `execute_fidelity_with_convergence()`
- FR-8 owns: parallel agent spawning, finding merge/dedup, adversarial debate invocation, `handle_regression()`
- Shared (FR-6): DeviationRegistry — FR-8 writes to it, FR-7 reads from it

**Acceptance Criteria** (FR-7.1):
- [ ] `handle_regression()` signature matches the contract above
- [ ] `RegressionResult` dataclass is defined in models.py or convergence.py
- [ ] `handle_regression()` calls `registry.save()` before returning
- [ ] The convergence loop increments run_number exactly once per iteration, regardless of whether FR-8 was invoked
- [ ] After `handle_regression()` returns, the convergence loop evaluates the registry (not the raw RegressionResult)
- [ ] Budget check occurs after FR-8 completes, not before
```

**Also amend** FR-7's Dependencies line (currently line 367):

**Before**:
```
**Dependencies**: FR-6 (registry), FR-8 (regression handling)
```

**After**:
```
**Dependencies**: FR-6 (registry), FR-8 (regression handling — see FR-7.1 for interface contract)
```

**Also amend** FR-8's Dependencies line (currently line 407):

**Before**:
```
**Dependencies**: FR-1 (checkers), FR-4 (adversarial), FR-6 (registry), FR-7 (budget)
```

**After**:
```
**Dependencies**: FR-1 (checkers), FR-4 (adversarial), FR-6 (registry), FR-7 (budget — see FR-7.1 for interface contract)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (new FR-7.1 subsection + two dependency line amendments)

### Risk: **LOW**
Purely additive subsection. No existing acceptance criteria change. The function signature and dataclass are new spec text that directly constrain future implementation. The two dependency line amendments are cosmetic cross-references.

### Requires Code Changes: **No**
Spec-only. The `handle_regression()` function and `RegressionResult` dataclass do not yet exist (identified as new code in Compatibility Report Section 4). This proposal specifies their contract before implementation begins.

---

## Proposal #2: Inline Budget Accounting Clarification into FR-7 and FR-8

**Rationale**: Rather than adding a new subsection (FR-7.1), this proposal modifies the existing FR-7 and FR-8 text to make the circular dependency explicit inline. Smaller edit surface than Proposal #1, but distributes the interface contract across two FR sections rather than centralizing it.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Change 1** — FR-7 Description (lines 341-342). Add after "trigger parallel validation (see FR-8)":

**Before** (line 342):
```
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)
```

**After**:
```
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, call `handle_regression()` (FR-8). The entire regression flow executes within the scope of run N+1 and does NOT consume an additional run from the budget. After `handle_regression()` returns, the convergence loop evaluates `registry.get_active_high_count()` with the updated findings.
```

**Change 2** — FR-7 Acceptance Criteria. Add two new items after line 361 ("Run 3 is final"):

**Insert**:
```
- [ ] Regression validation (FR-8) executes within the triggering run's scope — no additional run counter increment
- [ ] After `handle_regression()` returns, gate evaluates the updated registry, not FR-8's raw output
```

**Change 3** — FR-8 Description (lines 373-377). Append ownership clarification:

**Before** (line 377):
```
Their findings are collected, merged by stable ID, deduplicated, sorted by
severity, and written to a consolidated report. After consolidation, an
adversarial debate validates the severity of each HIGH.
```

**After**:
```
Their findings are collected, merged by stable ID, deduplicated, sorted by
severity, and written to a consolidated report. After consolidation, an
adversarial debate validates the severity of each HIGH. `handle_regression()`
writes validated findings to the DeviationRegistry and returns a
`RegressionResult` to the calling convergence loop (FR-7). FR-8 does NOT
manage the run counter or budget — that responsibility belongs to FR-7.
```

**Change 4** — FR-8 Acceptance Criteria item (line 403). Clarify existing item:

**Before**:
```
- [ ] This entire flow counts as one "run" toward the budget of 3
```

**After**:
```
- [ ] This entire flow executes within the calling run's scope and does NOT increment the run counter (FR-7 owns the counter; FR-8 is a subroutine)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (4 inline edits across FR-7 and FR-8)

### Risk: **LOW**
Small inline changes. No structural reorganization. The existing FR-8 AC item about budget accounting is clarified rather than replaced with new semantics.

### Requires Code Changes: **No**
Spec-only.

---

## Proposal #3: Sequence Diagram + Contract in New Appendix

**Rationale**: The FR-7/FR-8 interaction is the most complex control flow in the spec. Rather than embedding the interface contract inline (where it competes for attention with other FR-7/FR-8 concerns), add an Appendix that documents the full sequence with a text-based diagram. This is the most complete treatment but the largest addition.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Insert** as new appendix after Appendix C (after line 653):

```markdown
## Appendix D: FR-7/FR-8 Interface Sequence

### Control Flow

```
execute_fidelity_with_convergence()           [FR-7 — owns budget]
│
├── Run 1: structural_checkers() + semantic_layer()
│   ├── merge_findings() → registry
│   ├── _check_regression() → false (no prior run)
│   ├── remediate() if HIGHs > 0
│   └── run_count = 1
│
├── Run 2: structural_checkers() + semantic_layer()
│   ├── merge_findings() → registry
│   ├── _check_regression() → true? (structural HIGHs increased)
│   │   └── YES → handle_regression()            [FR-8 — subroutine]
│   │       ├── _create_validation_dirs(3)
│   │       ├── parallel: agent_1, agent_2, agent_3
│   │       ├── merge by stable_id → consolidated
│   │       ├── adversarial debate per HIGH
│   │       ├── registry.merge_findings()
│   │       ├── registry.save()
│   │       └── return RegressionResult
│   ├── evaluate registry.get_active_high_count()
│   ├── remediate() if HIGHs > 0
│   └── run_count = 2  ← (FR-8 did NOT increment this)
│
├── Run 3: (final — pass or halt)
│   └── ... same as Run 2 ...
│   └── run_count = 3
│
└── Budget exhausted → halt with diagnostic report
```

### Interface Contract

| Aspect | FR-7 (Caller) | FR-8 (Callee) |
|--------|---------------|---------------|
| Entry point | `execute_fidelity_with_convergence()` | `handle_regression()` |
| Trigger | `_check_regression()` returns `True` | Called by FR-7 only |
| Run counter | Increments once per loop iteration | Does NOT touch run counter |
| Registry writes | Reads after FR-8 returns | Writes during execution |
| Budget enforcement | Checks `run_count <= 3` | Unaware of budget |
| Pass/fail decision | `registry.get_active_high_count() == 0` | Returns `RegressionResult` |
| Cleanup | Delegates to FR-8 | `_cleanup_validation_dirs()` in finally block |

### `handle_regression()` Signature

```python
def handle_regression(
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
    run_number: int,
) -> RegressionResult

@dataclass
class RegressionResult:
    validated_findings: list[Finding]
    debates_run: int
    consolidated_report_path: Path
    registry_updated: bool
```

### Budget Accounting Example

| Event | Run Counter | Structural HIGHs | Notes |
|-------|------------|-------------------|-------|
| Run 1 completes | 1 | 5 | Baseline |
| Run 2 starts, checkers run | — | 7 | Regression detected |
| FR-8: handle_regression() | — | — | 3 agents validate, debate |
| FR-8: registry updated | — | 4 | Two HIGHs downgraded by debate |
| Run 2 completes | 2 | 4 | Budget: 2/3 |
| Run 3 starts, checkers run | — | 0 | All fixed |
| Run 3 completes | 3 | 0 | PASS |
```

**Also add** cross-references in FR-7 and FR-8:

**FR-7 Description** (line 342), append:
```
(see FR-8; full sequence in Appendix D)
```

**FR-8 Description** (after line 377), append:
```
See Appendix D for the full FR-7/FR-8 interaction sequence and interface contract.
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (new Appendix D + two cross-reference additions)

### Risk: **LOW-MEDIUM**
Large additive content but no existing text changes beyond two cross-reference insertions. Risk: the sequence diagram could become stale if FR-7 or FR-8 acceptance criteria change. Mitigation: the diagram is illustrative, not normative — the AC items remain the source of truth.

### Requires Code Changes: **No**
Spec-only. The function signature and dataclass serve as implementation guidance.

---

## Ranking Summary

| Rank | Proposal | Disruption | Correctness | Completeness | Recommendation |
|------|----------|-----------|-------------|--------------|----------------|
| 1 | #1 (FR-7.1 interface contract subsection) | Low | High | High | Best balance of specificity and locality — contract lives next to FR-7 where the call originates |
| 2 | #2 (Inline clarifications) | Very Low | High | Medium | Sufficient if interface contract is considered obvious from context; does not specify function signature or return type |
| 3 | #3 (Appendix with sequence diagram) | Medium | Highest | Highest | Best for implementation clarity; risk of staleness if FR-7/FR-8 evolve |

**Recommended approach**: **Proposal #1** as the primary fix. It centralizes the interface contract in one place (FR-7.1), specifies the function signature and return type, clarifies budget accounting with a concrete example, and establishes ownership boundaries. If additional visual clarity is desired, Proposal #3's sequence diagram could be adopted as a supplement.

**Combination option**: #1 + #3's sequence diagram as Appendix D. This gives both the normative contract (FR-7.1) and the illustrative sequence (Appendix D) without redundancy — FR-7.1 would reference Appendix D for the visual flow.
