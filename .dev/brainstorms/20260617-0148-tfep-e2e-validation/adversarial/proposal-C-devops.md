# Proposal C — DevOps / Orchestration Lens

**Distinctive emphasis:** operability, audit trail, cross-run aggregation. The 4 tests are the same behavioural dimensions; this proposal makes them **machine-run, evidence-emitting, roll-up-ready**.

---

## 1. Orchestration Plan

### 1.1 Directory layout

All artifacts land under a single evidence root:

```
.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/
  ├─ TEST-01-residual/
  │   ├─ run-1/verdict.yaml
  │   ├─ run-1/findings.md
  │   ├─ run-2/verdict.yaml
  │   ├─ run-2/findings.md
  │   ├─ run-3/verdict.yaml
  │   └─ run-3/findings.md
  ├─ TEST-02-contract/
  │   └─ run-{1,2,3}/  (same shape)
  ├─ TEST-03-chain/
  │   └─ run-{1,2,3}/  (same shape)
  └─ TEST-04-safety/
      └─ run-{1,2,3}/  (same shape)
  └─ roll-up.yaml              ← aggregator output
  └─ dashboard.md              ← human-readable 4×3 matrix
```

Each `run-N/` directory contains exactly two files:
- **`verdict.yaml`** — machine-readable (strict schema, §4 below).
- **`findings.md`** — human-readable narrative with embedded command output.

### 1.2 Spawn discipline (12 subagents)

The orchestrator spawns 4 batches of 3 subagents each (one batch per test). All 3 runs in a batch are spawned in a **single parallel message** so they start simultaneously and share no state. Between batches, the orchestrator waits for completion before spawning the next batch (sequential batches, parallel runs).

Rationale for batch-sequential: limits concurrent context-window contention and makes the aggregator's "wait for all 12" a simple 4-wait loop.

Pseudocode for the orchestrator:

```
for test in [TEST-01, TEST-02, TEST-03, TEST-04]:
    spawn 3 subagents in parallel (run indices 1,2,3)
    wait for all 3 to complete
# After 4 batches: all 12 runs done → spawn aggregator
spawn aggregator subagent
```

Each subagent receives:
1. The test ID, scope, and probe steps (embedded below).
2. Its run index (1, 2, or 3) and the evidence output directory.
3. An instruction to write exactly `verdict.yaml` + `findings.md` to its assigned `run-N/` directory.
4. **No read access** to other runs' artifacts (enforced by the prompt, not file permissions — they land after the spawn anyway).

### 1.3 Aggregator subagent

After all 12 runs complete, a single aggregator subagent:
1. Reads all 12 `verdict.yaml` files.
2. Groups by test ID; checks that all 3 runs agree per test.
3. Computes per-test verdict: PASS iff all 3 runs PASS; FAIL otherwise.
4. Computes global gate: GREEN iff all 4 tests PASS; RED otherwise.
5. Writes `roll-up.yaml` (machine-readable) and `dashboard.md` (human-readable 4×3 matrix).

### 1.4 Idempotency & non-mutation

- **Read-only probes only**: `rg`, `grep`, `make verify-sync`, `git status`, `Read` — no file writes to the 5 migrated files, no `git add`, no `git commit`.
- **Evidence is append-only**: each `run-N/` is created fresh; re-running the whole suite creates a new evidence root with a timestamp suffix, never overwrites.
- **Committable trail**: the entire `evidence/` tree is plain text (YAML + Markdown), suitable for a PR commit or a `.dev/` artifact directory.

### 1.5 Reproducibility & cost guardrails

- **Deterministic probes first**: each test begins with shell-grounded checks (`rg -c`, `make verify-sync`, `git status`) that produce identical output across runs. LLM protocol-trace portions are anchored to the probe output, not left to free-form judgment.
- **Token budget per run**: ~2K tokens (mostly Read + Grep/Rg calls). Total 12-run budget: ~24K tokens + aggregator ~3K = ~27K.
- **Fail-fast within a run**: if a binary acceptance criterion fails, the run records FAIL and skips remaining optional checks — the evidence file still captures the first-failure context.
- **Timeout per subagent**: 5 minutes wall-clock; if a run exceeds this, it emits `verdict: FAIL, verdict_reason: "timeout"` with whatever probes completed.

---

## 2. Test Definitions

### TEST-01: Residual Cleanup & Sync Parity

**Outcome dimension:** Backend swap is complete and clean.

**Scope:** The 5 migrated files + `src/` tree.

#### Delegable Subagent Prompt

```
You are a read-only validation subagent. Execute TEST-01 "Residual Cleanup & Sync Parity".
You are run number RUN_N (1, 2, or 3) of 3 independent runs.
Do NOT modify any files. Write results to the evidence directory given.

WORKTREE ROOT: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend

PROBE STEPS (execute in order):

1. Residual sweep in the 2 task-protocol files:
   Run: rg -n "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" \
     src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md
   ACCEPT: 0 hits. Record the count and any lines if >0.

2. Global src/ sweep for /sc:forensic:
   Run: rg -rn "/sc:forensic" src/
   ACCEPT: 0 hits. Record count and lines if >0.

3. Out-of-scope noise check (confirm you are NOT false-flagging generic "forensic"):
   Run: rg -rn "\bforensic\b" src/superclaude/skills/sc-task-protocol/SKILL.md \
     src/superclaude/commands/task.md src/superclaude/commands/troubleshoot.md \
     src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md \
     src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
   Record: 0 hits expected in the 5 migrated files. (If hits appear, check whether they are
   the backend reference "/sc:forensic" vs generic vocabulary — only the former is a failure.)

4. Sync parity:
   Run: make verify-sync
   ACCEPT: EXIT 0, stdout contains "All components in sync", no DIFFERS or MISSING lines.

5. No .claude/ staged:
   Run: git status --porcelain
   ACCEPT: no lines matching "^\?\? \.claude/" or "^[AMD] \.claude/" (excluding .claude/settings.json).

NEGATIVE CHECK: After probes 1-2 pass, ALSO run:
   rg -rn "/sc:troubleshoot" src/superclaude/skills/sc-task-protocol/SKILL.md
   Confirm at least 1 hit exists (the replacement backend IS present). If 0 hits, the
   sweep in probe 1 is vacuously passing because the files are empty or missing — record FAIL.

EVIDENCE: Write verdict.yaml and findings.md to EVIDENCE_DIR/run-RUN_N/.
```

#### Binary Acceptance Criteria

| # | Criterion | PASS when |
|---|-----------|-----------|
| 1 | No forensic residue in task-protocol files | `rg` probe returns 0 hits |
| 2 | No `/sc:forensic` anywhere in `src/` | `rg -rn "/sc:forensic" src/` returns 0 hits |
| 3 | No false-positive on generic vocabulary | Hits in probe 3 are 0, or if >0, none match `/sc:forensic` |
| 4 | `make verify-sync` exits 0 with "All components in sync" | Exit code 0, no DIFFERS/MISSING |
| 5 | No `.claude/` paths staged (except settings.json) | `git status --porcelain` shows none |
| 6 | Negative: troubleshoot backend IS present | `rg -rn "/sc:troubleshoot"` in task-protocol files >= 1 hit |

**PASS iff all 6 criteria hold.**

---

### TEST-02: Adapter Contract Integrity (Producer ↔ Consumer)

**Outcome dimension:** The 7-field wire set is byte-identical across consumer (§4.5), producer (Output Contract), and report template (`## TFEP Consumer`).

**Scope:** `src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5, `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Output Contract + adapter rows, `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` `## TFEP Consumer` section.

#### Delegable Subagent Prompt

```
You are a read-only validation subagent. Execute TEST-02 "Adapter Contract Integrity".
You are run number RUN_N (1, 2, or 3) of 3 independent runs.
Do NOT modify any files. Write results to the evidence directory given.

WORKTREE ROOT: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend

The 7 TFEP adapter field names to verify across all three surfaces:
  status, test_is_wrong, recommended_escalation, tasklist_insertion_path,
  remediation_target, root_cause_summary, solution_summary

PROBE STEPS (execute in order):

1. Consumer presence (§4.5 in sc-task-protocol SKILL.md):
   For each of the 7 field names, run:
     rg -c "<field_name>" src/superclaude/skills/sc-task-protocol/SKILL.md
   ACCEPT: each returns >= 1. Record per-field counts.

2. Producer presence (Output Contract in sc-troubleshoot-protocol SKILL.md):
   For each of the 7 field names, run:
     rg -c "<field_name>" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
   ACCEPT: each returns >= 1. Record per-field counts.

3. Report-template presence (## TFEP Consumer section in report-template.md):
   For each of the 7 field names, run:
     rg -c "<field_name>" src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
   ACCEPT: each returns >= 1. Record per-field counts.

4. Enum byte-match — recommended_escalation:
   The enum values "none|retry|escalate_depth|halt" must appear in all three files.
   For each file, run:
     rg -c "none\|retry\|escalate_depth\|halt" <file>
   ACCEPT: >= 1 in each. Record exact matched lines for each file.

5. Enum byte-match — remediation_target:
   The enum values "test|code|docs|none" must appear in all three files.
   For each file, run:
     rg -c "test\|code\|docs\|none" <file>  (scope to remediation_target context)
   More precisely: read the lines around "remediation_target" in each file and confirm
   the enum token set {test, code, docs, none} is present in the defining context.

6. Contract version bump:
   Run: rg -n "1\.1\.0" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
   ACCEPT: at least 1 hit where "1.1.0" is the contract_version default. Record the line.

7. Adapter row count (producer-side):
   Run: rg -c "TFEP adapter field \(contract v1.1.0" \
     src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
   ACCEPT: count == 5 (recommended_escalation, tasklist_insertion_path, remediation_target,
   root_cause_summary, solution_summary). Record count.

8. Backend declaration:
   Run: rg -n "Diagnostic backend.*troubleshoot" \
     src/superclaude/skills/sc-task-protocol/SKILL.md
   ACCEPT: exactly 1 hit with "troubleshoot" (not "forensic"). Record the line.

NEGATIVE CHECK: Read the actual enum definitions in each file (Read the lines around
"recommended_escalation" and "remediation_target" in all 3 files). Confirm there are no
additional enum values beyond the specified sets. Extra values = FAIL.

EVIDENCE: Write verdict.yaml and findings.md to EVIDENCE_DIR/run-RUN_N/.
```

#### Binary Acceptance Criteria

| # | Criterion | PASS when |
|---|-----------|-----------|
| 1 | All 7 fields present in consumer (§4.5) | All 7 `rg -c` counts >= 1 |
| 2 | All 7 fields present in producer (Output Contract) | All 7 `rg -c` counts >= 1 |
| 3 | All 7 fields present in report template (## TFEP Consumer) | All 7 `rg -c` counts >= 1 |
| 4 | recommended_escalation enum {none, retry, escalate_depth, halt} present in all 3 files | Each file has >= 1 match |
| 5 | remediation_target enum {test, code, docs, none} present in all 3 files | Each file has >= 1 match in context |
| 6 | contract_version default is 1.1.0 | "1.1.0" appears in SKILL.md Output Contract |
| 7 | Producer adapter row count == 5 | rg count of "TFEP adapter field (contract v1.1.0" == 5 |
| 8 | Backend declaration is "troubleshoot" | Exactly 1 hit with "troubleshoot", 0 with "forensic" |
| 9 | No extra enum values | Read of enum definitions shows no additional tokens |

**PASS iff all 9 criteria hold.**

---

### TEST-03: End-to-End Protocol Chain Trace

**Outcome dimension:** The trigger → freeze → context → dispatch → wave ingestion → return-contract → consume → branch → compose → resume chain is coherent and depth-mapping is consistent.

**Scope:** Protocol text trace across the 5 migrated files (no live invocation; this is a deterministic protocol-path simulation via reading + structural verification).

#### Delegable Subagent Prompt

```
You are a read-only validation subagent. Execute TEST-03 "End-to-End Protocol Chain Trace".
You are run number RUN_N (1, 2, or 3) of 3 independent runs.
Do NOT modify any files. Write results to the evidence directory given.

WORKTREE ROOT: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend

PROBE STEPS (execute in order):

1. Step 1 freeze block existence:
   Read lines around "Step 1: Halt and freeze" in
   src/superclaude/skills/sc-task-protocol/SKILL.md
   ACCEPT: Section exists with "STOP testing immediately" and "FREEZE implementation".
   Record the exact freeze block text.

2. Step 2 context.yaml binding:
   Read lines around "context.yaml" and "{context_path}" in the same file.
   ACCEPT: The text writes failure context to a YAML file and passes it as {context_path}
   to Step 3. Record the relevant lines.

3. Step 3 dispatch string:
   Run: rg -n "sc:troubleshoot --caller task-unified" \
     src/superclaude/skills/sc-task-protocol/SKILL.md
   ACCEPT: exactly 1 hit matching the pattern:
     /sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}
   or its inline form. Record the line(s).

4. No --fix in dispatch:
   Read the Step 3 dispatch context and the Escalation Budget section.
   ACCEPT: "--fix" does NOT appear in any TFEP dispatch string. Record the search result.

5. Wave 0 caller/context ingestion (troubleshoot side):
   Read Wave 0 step 6 in sc-troubleshoot-protocol SKILL.md.
   ACCEPT: The text records --caller in audit header and reads --context; mentions
   "caller=task-unified" marks Wave 5 to emit return-contract.yaml. Record the relevant lines.

6. Wave 5 step 4.5 return-contract emission:
   Read Wave 5 step 4.5 in sc-troubleshoot-protocol SKILL.md.
   ACCEPT: The text writes return-contract.yaml when caller=task-unified, mapping the
   7 adapter fields. Record the field list it emits.

7. Step 4 branch ladder (consumer side):
   Read Step 4 in sc-task-protocol SKILL.md (§4.5).
   ACCEPT: The branch ladder checks (in precedence order):
     a) test_is_wrong == true → present to user
     b) remediation_target == "docs" → present to user
     c) status == "success" → proceed
     d) recommended_escalation == "none" → proceed
     e) recommended_escalation == "retry" → re-enter Step 3
     f) recommended_escalation == "escalate_depth" → re-enter at deep
     g) recommended_escalation == "halt" OR status == "failed" → FULL STOP
   Record the branch lines found. Confirm first-match-wins ordering note is present.

8. Depth mapping consistency:
   Read the "Escalation Budget" section in sc-task-protocol SKILL.md.
   ACCEPT: Maps are:
     1st trigger → standard
     2nd trigger / systemic / >=3 new → deep
     3rd trigger → FULL STOP
   Record the budget block text.

9. Loop termination proof:
   Read Step 4 and Step 6 together.
   ACCEPT: escalation_count increments on re-entry; max 3 triggers; halt/failed = immediate
   FULL STOP; escalate-from-deep = FULL STOP. This is a terminating decision procedure.
   Record the termination evidence.

NEGATIVE CHECK: Search for ANY reference to "--tier" or "--intent" flags (the old forensic
backend's flags) in the 5 migrated files. If found, record FAIL — these should have been
stripped by the migration.

EVIDENCE: Write verdict.yaml and findings.md to EVIDENCE_DIR/run-RUN_N/.
```

#### Binary Acceptance Criteria

| # | Criterion | PASS when |
|---|-----------|-----------|
| 1 | Step 1 freeze block exists | "STOP testing" + "FREEZE implementation" present |
| 2 | Step 2 writes context.yaml and binds {context_path} | Text confirms YAML write + path binding |
| 3 | Step 3 dispatch uses /sc:troubleshoot --caller task-unified | Exactly 1 dispatch hit with correct flag shape |
| 4 | No --fix in TFEP dispatch | "--fix" absent from all TFEP dispatch strings |
| 5 | Wave 0 ingests --caller/--context | Wave 0 step 6 references caller + context |
| 6 | Wave 5 step 4.5 emits return-contract.yaml for caller=task-unified | Text confirms 7-field emission |
| 7 | Step 4 branch ladder has all 7 branches in precedence order | All branches present, first-match-wins noted |
| 8 | Depth mapping is consistent (1st→standard, 2nd→deep, 3rd→STOP) | Escalation Budget matches |
| 9 | Loop is a terminating decision procedure | escalation_count + max 3 + halt=STOP confirmed |
| 10 | No --tier or --intent flags in migrated files | rg for "--tier" and "--intent" returns 0 in the 5 files |

**PASS iff all 10 criteria hold.**

---

### TEST-04: Safety Invariants Preserved

**Outcome dimension:** Freeze block is byte-identical to pre-migration baseline, no --fix leaks into §4.5, asymmetric-cost gates present with "do not auto-apply" discipline, backend-neutral prose enables future swap.

**Scope:** 5 migrated files + the freeze-block baseline artifact.

#### Delegable Subagent Prompt

```
You are a read-only validation subagent. Execute TEST-04 "Safety Invariants Preserved".
You are run number RUN_N (1, 2, or 3) of 3 independent runs.
Do NOT modify any files. Write results to the evidence directory given.

WORKTREE ROOT: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend

PROBE STEPS (execute in order):

1. Freeze block byte-identical to pre-migration baseline:
   Read the current freeze block from Step 1 in
   src/superclaude/skills/sc-task-protocol/SKILL.md (the text under "Step 1: Halt and freeze",
   including "STOP testing immediately" and "FREEZE implementation — no further code changes permitted").
   Read the baseline from:
   .dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md
   ACCEPT: the two texts are byte-identical (or structurally identical allowing whitespace).
   Record both texts and the comparison result.

2. No --fix in §4.5 dispatch:
   Read the entire §4.5 section in sc-task-protocol SKILL.md.
   ACCEPT: "--fix" does not appear in any TFEP invocation string (Step 3 dispatch,
   Escalation Budget, or retry/escalation re-invocations). Record the search scope and result.

3. Asymmetric-cost gate — test_is_wrong:
   Read Step 4 in sc-task-protocol SKILL.md.
   ACCEPT: The "test_is_wrong == true" branch says "Present to user for review.
   Do NOT auto-fix tests." Record the exact line.

4. Asymmetric-cost gate — remediation_target == "docs":
   Read Step 4 in sc-task-protocol SKILL.md.
   ACCEPT: The branch says "present to user for spec/stakeholder review.
   Do NOT auto-insert a code remediation." Record the exact line.

5. Backend-neutral declaration:
   Read the "Diagnostic backend:" declaration line in sc-task-protocol SKILL.md §4.5.
   ACCEPT: The line reads "Diagnostic backend: troubleshoot" and the adjacent comment
   states "The TFEP references below are backend-neutral — swapping the backend changes
   only this declaration and the invocation string." Record the declaration and comment.

6. Invocation strings are parameterized (not hardcoded to troubleshoot internals):
   Read the Escalation Budget section in sc-task-protocol SKILL.md.
   ACCEPT: The invocation uses "/sc:troubleshoot --caller task-unified --depth {standard|deep}"
   without troubleshoot-internal flags. Record the escalation budget text.

7. Report template TFEP Consumer section is conditional:
   Read the "## TFEP Consumer" section header in report-template.md.
   ACCEPT: The preamble says "Emitted ONLY when caller=task-unified" and "Omit this section
   entirely for non-TFEP callers." Record the conditional text.

NEGATIVE CHECK: Search for ANY "auto-fix", "auto-apply", or "auto-insert" language in the
TFEP section that would contradict the asymmetric-cost gates. If found, record the line and
mark FAIL (unless it is in a "Do NOT auto-*" prohibition context, which is acceptable).

EVIDENCE: Write verdict.yaml and findings.md to EVIDENCE_DIR/run-RUN_N/.
```

#### Binary Acceptance Criteria

| # | Criterion | PASS when |
|---|-----------|-----------|
| 1 | Freeze block byte-identical to baseline | Current and baseline texts match |
| 2 | No --fix in §4.5 dispatch | "--fix" absent from all TFEP dispatch/escalation strings |
| 3 | test_is_wrong gate → present to user, no auto-fix | Exact "Do NOT auto-fix tests" text present |
| 4 | remediation_target=="docs" gate → present to user, no auto-insert | Exact prohibition text present |
| 5 | Backend-neutral declaration present | "Diagnostic backend: troubleshoot" + swap comment |
| 6 | Invocation strings are parameterized | Escalation Budget uses generic flag shape, no internal flags |
| 7 | Report template TFEP section is conditional | "ONLY when caller=task-unified" + "omit for non-TFEP" |
| 8 | No contradictory auto-fix language | No "auto-fix" / "auto-apply" outside "Do NOT" prohibition context |

**PASS iff all 8 criteria hold.**

---

## 3. Evidence-Artifact Schema

### 3.1 Machine-readable verdict.yaml

Every run writes a `verdict.yaml` conforming to this strict schema:

```yaml
---
# TFEP E2E Validation — per-run verdict artifact
schema_version: 1.0.0
test_id: "TEST-01"              # One of TEST-01, TEST-02, TEST-03, TEST-04
test_name: "Residual Cleanup & Sync Parity"
run_index: 1                     # 1, 2, or 3
timestamp: "2026-06-17T02:15:00Z"
worktree: "/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend"
verdict: "PASS"                  # PASS | FAIL
verdict_reason: null             # null when PASS; first-failure description when FAIL
criteria:
  - id: 1
    description: "No forensic residue in task-protocol files"
    result: "PASS"               # PASS | FAIL | SKIPPED
    evidence: "rg returned 0 hits"
    command: "rg -n '/sc:forensic|...' src/superclaude/skills/sc-task-protocol/SKILL.md ..."
  - id: 2
    description: "No /sc:forensic anywhere in src/"
    result: "PASS"
    evidence: "rg -rn '/sc:forensic' src/ returned 0 hits"
    command: "rg -rn '/sc:forensic' src/"
  # ... one entry per criterion for the test
probes_completed: 5              # Number of probe steps that ran
probes_total: 5                  # Total probe steps defined for this test
fail_fast: false                 # true if the run aborted early on first failure
```

Schema invariants:
- `verdict` MUST be "PASS" only when every `criteria[*].result` is "PASS" (or "SKIPPED" if the test definition allows skips — none of the 4 tests do).
- `verdict` MUST be "FAIL" if any `criteria[*].result` is "FAIL".
- `verdict_reason` is `null` when PASS; otherwise the description of the first failed criterion.
- `probes_completed` == `probes_total` unless `fail_fast: true`.

### 3.2 Human-readable findings.md

Each run writes a `findings.md` with this structure:

```markdown
# TEST-01 Run 1 — Residual Cleanup & Sync Parity

**Verdict**: PASS
**Timestamp**: 2026-06-17T02:15:00Z
**Run index**: 1/3

## Probe 1: Residual sweep in task-protocol files

Command:
```
rg -n "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" \
  src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md
```

Output:
```
(no output — 0 hits)
```

Result: PASS — 0 forensic tokens found.

## Probe 2: Global src/ sweep

...

## Summary

All 5 probes completed. Verdict: PASS.
```

---

## 4. Aggregator & Roll-Up

### 4.1 roll-up.yaml

The aggregator reads all 12 `verdict.yaml` files and writes:

```yaml
---
schema_version: 1.0.0
generated_at: "2026-06-17T02:45:00Z"
worktree: "/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend"
per_test:
  - test_id: "TEST-01"
    test_name: "Residual Cleanup & Sync Parity"
    runs:
      - run_index: 1, verdict: "PASS", timestamp: "2026-06-17T02:15:00Z"
      - run_index: 2, verdict: "PASS", timestamp: "2026-06-17T02:15:03Z"
      - run_index: 3, verdict: "PASS", timestamp: "2026-06-17T02:15:06Z"
    cross_run_agreement: true      # true iff all 3 verdicts are identical
    test_verdict: "PASS"           # PASS iff all 3 runs PASS
  - test_id: "TEST-02"
    ...
  - test_id: "TEST-03"
    ...
  - test_id: "TEST-04"
    ...
global_gate: "GREEN"               # GREEN iff all 4 test_verdicts are PASS; RED otherwise
total_runs: 12
passed: 12
failed: 0
gate_rule: "All 4 tests must PASS in all 3 runs (12/12). Any single FAIL flips the gate to RED."
```

### 4.2 Gate rule

```
global_gate = GREEN  iff  forall test_id in {01,02,03,04}:
                            forall run in {1,2,3}:
                              verdict(test_id, run) == "PASS"

Otherwise: RED
```

This is a strict 12/12 gate. No majority tolerance — the migration touches only 5 files and the probes are deterministic (shell-based with read-anchored traces). If one run out of 3 disagrees, it indicates either a probe bug or a real inconsistency; the human reviewer inspects the divergent `findings.md` before signing off.

### 4.3 Dashboard (dashboard.md)

```markdown
# TFEP E2E Validation Dashboard

## Migration: forensic → troubleshoot backend
## Date: 2026-06-17
## Worktree: tfep-troubleshoot-backend

| Test | Run 1 | Run 2 | Run 3 | Cross-Run | Verdict |
|------|-------|-------|-------|-----------|---------|
| TEST-01: Residual Cleanup & Sync Parity | PASS | PASS | PASS | agree | PASS |
| TEST-02: Adapter Contract Integrity | PASS | PASS | PASS | agree | PASS |
| TEST-03: E2E Protocol Chain Trace | PASS | PASS | PASS | agree | PASS |
| TEST-04: Safety Invariants Preserved | PASS | PASS | PASS | agree | PASS |

## Gate: GREEN (12/12 PASS)

Gate rule: All 4 tests must PASS in all 3 runs. Any FAIL flips to RED.
```

---

## 5. Distinctive Summary

This proposal treats the validation suite as a **mini CI pipeline**: 4 tests x 3 runs = 12 subagents spawned in 4 parallel batches with strict isolation (no artifact cross-pollination between runs), each emitting a machine-readable `verdict.yaml` plus a human-readable `findings.md` to a deterministic per-test/per-run directory. An aggregator subagent reads all 12 verdicts and computes a strict 12/12 GREEN/RED gate, rendered as both a machine-parsable `roll-up.yaml` and a one-glance 4x3 markdown dashboard the human reviewer can sign off on without re-deriving anything.
