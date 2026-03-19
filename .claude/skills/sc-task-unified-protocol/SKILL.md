---
name: sc:task-unified-protocol
description: Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation. Merges orchestration capabilities with MCP compliance into a single coherent interface.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task
---

> **NOTE**: Classification has already been performed by the `/sc:task` command before this skill was invoked. The classification header has already been emitted. Do NOT emit it again. This skill handles **execution only** for STANDARD and STRICT tier tasks.
>
> If for any reason no classification header was emitted before this skill was invoked, emit one now using ONLY the tier values STRICT, STANDARD, LIGHT, or EXEMPT (no other values are valid).

# /sc:task-unified - Unified Task Execution with Compliance

## Purpose

Unified command that merges orchestration capabilities with MCP compliance enforcement. Automatically classifies tasks into compliance tiers and enforces appropriate verification.

**Key Benefits**:
- Single command replaces confusion between `sc:task` and `sc:task-mcp`
- Automatic tier classification with confidence scoring
- Appropriate verification for each task type
- Prevents over-engineering for trivial changes
- Ensures safety for critical changes

## Triggers

Use `/sc:task` when:
- Task involves code modifications with downstream impacts
- Complexity score >0.6 with code modifications
- Multi-file scope (>2 estimated affected files)
- Security domain paths detected (auth/, security/, crypto/)
- Refactoring or system-wide changes requested

**Auto-Suggest Keywords**:
- High confidence: "implement feature", "refactor system", "fix security", "add authentication", "update database schema"
- Moderate confidence: "add new", "create component", "update service", "modify API"

## Usage

```bash
/sc:task [description]                           # Auto-detect all dimensions
/sc:task [description] --compliance strict       # Force STRICT tier
/sc:task [description] --compliance light        # Force LIGHT tier
/sc:task [description] --skip-compliance         # Bypass compliance (escape hatch)
/sc:task [description] --verify auto             # Auto-select verification
```

## Behavioral Flow

### 0. Classification (Already Performed)

Classification was handled by the `/sc:task` command before this skill was invoked. The tier has been determined and the classification header has been emitted. Proceed directly to execution based on the classified tier.

**Reference** — the tier keyword tables (for context only, do not re-classify):
- **STRICT**: security, authentication, database, migration, refactor, breaking change, encrypt, token, session, oauth
- **EXEMPT**: explain, search, commit, push, plan, discuss, brainstorm
- **LIGHT**: typo, comment, whitespace, lint, docstring, formatting, minor
- **STANDARD**: implement, add, create, update, fix, build, modify, change (default)

### 2. Confidence Display (Human-Readable)

After the mandatory classification header, show a human-readable summary:

```
**Tier: STANDARD** [████████░░] 80%

Classified as STANDARD:
- Keywords matched: add, implement
- Confidence score: 0.78
- Considered alternatives: STRICT (0.35)
```

If confidence <70%, add prompt: "⚠️ Low confidence. Override with: `--compliance [strict|standard|light|exempt]`"

**Note**: The machine-readable header (Section 0) is for telemetry/A/B testing. This human-readable display is for user understanding.

### 3. Execution Phase

Execute task according to tier requirements:

**STRICT Execution**:
1. Activate project (mcp__serena__activate_project)
2. Verify git working directory clean (git status)
3. Load codebase context (codebase-retrieval)
4. Check relevant memories (list_memories -> read_memory)
5. Identify all affected files and test files
6. Make changes with full checklist
7. Identify all files that import changed code
8. Update all affected files
9. Spawn verification agent (quality-engineer)
10. Run comprehensive tests: `pytest [path] -v`
11. Answer adversarial questions

**STANDARD Execution**:
1. Load context via codebase-retrieval
2. Search downstream impacts (find_referencing_symbols OR grep)
3. Make changes
4. Run affected tests OR document manual verification
5. Verify basic functionality

**LIGHT Execution**:
1. Quick scope check (files/lines within bounds)
2. Make changes
3. Quick sanity check (syntax valid, no obvious errors)
4. Proceed with judgment

**EXEMPT Execution**:
1. Execute immediately
2. No verification overhead

### 4. Verification Phase

Route to appropriate verification based on tier and paths:

| Compliance Tier | Verification Method | Token Cost | Timeout |
|-----------------|---------------------|------------|---------|
| STRICT | Sub-agent (quality-engineer) | 3-5K | 60s |
| STANDARD | Direct test execution | 300-500 | 30s |
| LIGHT | Skip verification | 0 | 0s |
| EXEMPT | Skip verification | 0 | 0s |

**Critical Path Override**: Paths matching `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always trigger CRITICAL verification regardless of compliance tier.

**Trivial Path Override**: Paths matching `*.md`, `docs/`, `*test*.py` may skip verification.

### 4.5 Test Failure Escalation Protocol (TFEP)

**CRITICAL**: When tests fail during the Verification Phase (Section 4), agents MUST follow this protocol. Ad-hoc fixes are PROHIBITED.

#### TFEP Prohibition Rules (VIOLATION-level)

These rules apply to ALL compliance tiers that run tests (STRICT, STANDARD):

1. **VIOLATION**: Agents MUST NOT fix any code in response to test failures without completing the TFEP workflow.
2. **VIOLATION**: Agents MUST NOT modify test expectations to make failing tests pass without adversarial validation.
3. **VIOLATION**: Ad-hoc patches derived from test output are PROHIBITED. The agent must not read a traceback and immediately edit code to resolve it.

**Permitted Exceptions** (MAY fix directly without TFEP):
- Single `ImportError`/`NameError` in test scaffolding the agent just wrote, affecting <=2 tests, where the error is in the test file itself (not in implementation code).
- Lint/formatting failures (trivially fixable, unambiguous root cause).
- Deprecation warnings (not failures).

**Valid Adversarial Outcome**: "Test expectations are wrong" is a legitimate conclusion from adversarial debate. When the debate concludes that test expectations are outdated rather than the code being wrong, this is NOT grounds for the agent to directly edit the tests — it must be presented to the user for review.

#### Test Baseline Snapshot (Pre-Implementation)

Before implementation begins, the agent MUST record a test baseline:

1. Capture the list of all existing test files and test function names at task start (e.g., via `uv run pytest --collect-only -q` or directory listing).
2. Store this baseline in memory for the duration of the task.
3. On any test failure, classify each failing test as:
   - **Pre-existing**: Test name appears in the baseline (existed before this task).
   - **New**: Test name does NOT appear in the baseline (written by the agent during this task).
4. This classification drives the MUST-escalate vs MAY-fix-directly decision below.

#### Escalation Trigger Detection

**MUST escalate (trigger TFEP):**
- Any **pre-existing test** fails (tests in the baseline that were not modified by the agent). This is the primary trigger — regressions in existing tests indicate the implementation broke something.
- **3 or more new tests** fail simultaneously (indicates a systemic issue, not a simple typo).
- **Runtime exceptions in implementation code** (TypeError, AttributeError, KeyError, etc. in the code being tested, not in the test scaffolding itself).

**Escalation gradient (within-TFEP, for future forensic integration):**
- Repeated failure (same test cluster fails after fix attempt) → escalate from light to standard
- Multi-file blast radius from recent changes → escalate
- Low-confidence root cause from adversarial debate → escalate
- Unresolved adversarial outcome (no winner/tie) → escalate
- Second failed retest → escalate
- Cross-domain or non-obvious regression → escalate

#### TFEP Execution Flow

When TFEP triggers, execute the following steps:

**Step 1: Halt and freeze**
1. **STOP** testing immediately.
2. **FREEZE** implementation — no further code changes permitted.

**Step 2: Construct failure context**
3. Build a `failure_context` YAML package containing:
   - `test_names`: list of failing test function names
   - `test_files`: list of test files containing failures
   - `error_output`: full traceback/error output
   - `expected_behavior`: what was expected
   - `actual_behavior`: what actually happened
   - `changes_made`: files changed during this task with descriptions
   - `task_description`: current task description
   - `test_baseline`: the pre-implementation test baseline
   - `escalation_count`: which TFEP trigger this is (1, 2, or 3)
4. Write context to `{output_dir}/context.yaml`.

**Step 3: Invoke forensic**
5. Determine the forensic tier based on escalation count:
   - 1st trigger → `--tier light --intent triage`
   - 2nd trigger → `--tier standard`
   - 3rd trigger → **FULL STOP**. Report to user. Do not attempt further fixes.
6. Invoke: `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick`
7. The forensic pipeline runs autonomously through all its phases and returns a structured return contract.

**Step 4: Consume forensic results**
8. Read the forensic return contract from `{output_dir}/return-contract.yaml`.
9. Handle based on status:
   - If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
   - If `status == "success"`: Proceed to Step 5 (tasklist insertion).
   - If `status == "partial"` or `recommended_escalation != "none"`: Increment `escalation_count` and return to Step 3.
   - If `status == "failed"`: Report to user, halt execution.

**Step 5: Tasklist insertion**
10. Read `tasklist_insertion_path` from the return contract.
11. Insert the remediation block into the current tasklist:
    - Add `## Failure Remediation Plan (Adjudicated)` heading.
    - Insert remediation tasks BEFORE existing test/verification tasks.
    - Preserve original tasklist structure — append, don't replace.

**Step 6: Resume**
12. Resume execution with `--compliance strict` starting from the inserted remediation tasks.
13. After remediation tasks complete, re-run the original test suite.
14. If tests pass: TFEP resolved successfully. Produce incident report and continue.
15. If tests fail again: Increment `escalation_count`, return to Step 2.

#### TFEP Incident Reporting

After each TFEP resolution (success or escalation), produce `tfep-incident-report.md`:

```markdown
# TFEP Incident Report

- **Trigger**: {which threshold rule fired}
- **Escalation count**: {1, 2, or 3}
- **Failing tests**: {test names and classification}
- **Root cause**: {summary from rca-verdict.md}
- **Solution**: {summary from solution-verdict.md}
- **Outcome**: {success / escalated / failed}
- **Forensic artifacts**: {path to output_dir}
```

This report is committed to git alongside other forensic artifacts.

#### Escalation Budget

```
1st TFEP trigger  → /sc:forensic --tier light --intent triage    (~5-8K tokens)
2nd TFEP trigger  → /sc:forensic --tier standard                 (~15-20K tokens)
3rd TFEP trigger  → FULL STOP. Report to user. Do not attempt further fixes.
```

### 5. Feedback Collection

After completion, collect implicit feedback:
- Track if user overrode tier (implicit classification feedback)
- Note smooth completion vs errors (quality signal)
- Store for calibration learning

## MCP Integration

**Required Servers by Tier**:
- STRICT: Sequential, Serena (fallback not allowed)
- STANDARD: Sequential, Context7 (fallback allowed)
- LIGHT: None required (fallback allowed)
- EXEMPT: None required

**Circuit Breaker Behavior**:
- If required servers unavailable for STRICT tier, block task execution
- For other tiers, use fallbacks with noted limitations

## Tool Coordination

**Planning Phase**:
1. TodoWrite: Create task breakdown
2. codebase-retrieval: Load context
3. list_memories / read_memory: Check project state

**Execution Phase**:
1. Edit/MultiEdit/Write: Make changes
2. Grep/Glob: Find references
3. find_referencing_symbols: Trace dependencies

**Verification Phase**:
1. Task (quality-engineer): Spawn verification agent (STRICT only)
2. Bash: Run tests directly (STANDARD)
3. think_about_task_adherence: Reflect on completeness

**Completion Phase**:
1. write_memory: Save session state
2. think_about_whether_you_are_done: Final check

## Examples

### STRICT Task
```
/sc:task "implement user authentication with JWT"

-> Classified as STRICT (security domain, authentication keyword)
-> Full 6-category checklist enforced
-> Verification agent spawned
-> Adversarial questions answered
```

### STANDARD Task
```
/sc:task "add pagination to user list"

-> Classified as STANDARD (add keyword, typical feature)
-> Context loaded before editing
-> Downstream impacts checked
-> Direct test execution
```

### LIGHT Task
```
/sc:task "fix typo in README"

-> Classified as LIGHT (trivial keyword, documentation path)
-> Quick sanity check only
-> No verification delay
```

### EXEMPT Task
```
/sc:task "explain how the auth flow works"

-> Classified as EXEMPT (explain pattern detected)
-> Immediate execution
-> No compliance overhead
```

### Override Example
```
/sc:task "update config file" --compliance strict

-> User override to STRICT regardless of classification
-> Full verification enforced
```

## Boundaries

**Will:**
- Classify tasks into appropriate compliance tiers
- Enforce tier-appropriate verification requirements
- Provide confidence scoring with rationale
- Track feedback for continuous calibration
- Support user overrides with justification

**Will Not:**
- Skip safety-critical verification for STRICT tasks
- Apply STRICT overhead to genuinely trivial changes
- Override user's explicit compliance choice
- Proceed with <70% confidence without user confirmation

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tier classification accuracy | >=80% | User feedback on appropriateness |
| User confusion rate | <10% | "Which command?" questions eliminated |
| Skip rate (--skip-compliance) | <12% | Override tracking |
| Regression prevention | >=85% | Post-verification bug detection |
| STRICT tier overhead | <25% | Execution telemetry |

## Configuration References

- Keywords: `config/tier-keywords.yaml`
- Verification routing: `config/verification-routing.yaml`
- Acceptance criteria: `config/tier-acceptance-criteria.yaml`
- Circuit breakers: See MCP.md
- Routing logic: See ORCHESTRATOR.md
