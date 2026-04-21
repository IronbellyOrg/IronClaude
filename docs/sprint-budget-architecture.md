# Sprint Budget Architecture (TurnLedger)

This document covers the full budgeting system in the sprint CLI: how the
TurnLedger works, every point where turns are debited and credited, how
exhaustion is detected, and the practical consequences of the current defaults.

---

## 1. The Ledger

The budget is tracked by a single `TurnLedger` dataclass (`models.py:547`),
created once at the start of `execute_sprint()`:

```python
ledger = TurnLedger(
    initial_budget = config.max_turns * len(config.active_phases),  # e.g. 100 * 6 = 600
    reimbursement_rate = 0.8,
)
```

### Core Formula

```
available = initial_budget - consumed + reimbursed
```

`consumed` only goes up. `reimbursed` only goes up. They are tracked
separately so the ledger never loses accounting history.

### Fields

| Field | Default | Purpose |
|-------|---------|--------|
| `initial_budget` | `max_turns * phases` | Total turn pool for the sprint |
| `consumed` | 0 | Cumulative turns debited (monotonically increasing) |
| `reimbursed` | 0 | Cumulative turns credited back (monotonically increasing) |
| `reimbursement_rate` | 0.8 | Multiplier for anti-instinct gate credits |
| `minimum_allocation` | 5 | Minimum turns needed to launch a task subprocess |
| `minimum_remediation_budget` | 3 | Minimum turns needed for remediation or wiring |
| `wiring_turns_used` | 0 | Cumulative turns consumed by wiring analysis |
| `wiring_turns_credited` | 0 | Cumulative turns credited back from wiring analysis |
| `wiring_budget_exhausted` | 0 (flag) | Set to 1 when wiring can no longer run |
| `wiring_analyses_count` | 0 | Count of wiring analyses executed |

---

## 2. Exhaustion Checks (Guards)

Three guard functions control whether work can proceed:

| Guard | Threshold | What it gates |
|-------|-----------|---------------|
| `can_launch()` | `available() >= 5` | Starting a new task subprocess |
| `can_remediate()` | `available() >= 3` | Running remediation after a gate failure |
| `can_run_wiring_gate()` | `wiring_budget_exhausted == 0 AND available() >= 3` | Running wiring analysis |

When `can_launch()` returns False, the per-task loop marks all remaining
tasks as SKIPPED and exits. This is the **only mechanism that stops the
per-task loop** (task failures alone do not stop it).

---

## 3. Complete Transaction Timeline for One Task

Here is every ledger operation that happens for a single task, in order:

```
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 STEP 0: GUARD CHECK                                                 u2502
u2502 can_launch() u2192 available >= 5?                                       u2502
u2502 If NO u2192 mark this + all remaining tasks SKIPPED, exit loop           u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
         u2502
         u25bc
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 STEP 1: PRE-ALLOCATION DEBIT                                         u2502
u2502 ledger.debit(minimum_allocation)          # debit 5 turns            u2502
u2502 consumed += 5                                                        u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
         u2502
         u25bc
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 STEP 2: SUBPROCESS EXECUTION                                         u2502
u2502 _run_task_subprocess(task, config, phase)                             u2502
u2502 Returns: (exit_code, turns_consumed, output_bytes)                    u2502
u2502                                                                      u2502
u2502 NOTE: turns_consumed is currently hardcoded to 0                      u2502
u2502 (see _run_task_subprocess line 1092)                                  u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
         u2502
         u25bc
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 STEP 3: RECONCILIATION                                               u2502
u2502 actual = max(turns_consumed, 0)                                      u2502
u2502 pre_allocated = 5                                                    u2502
u2502                                                                      u2502
u2502 if actual > 5:  debit(actual - 5)     # task used more than reserved u2502
u2502 if actual < 5:  credit(5 - actual)     # task used less than reservedu2502
u2502 if actual == 5: no-op                                                u2502
u2502                                                                      u2502
u2502 WITH CURRENT DEFAULTS: actual=0, so credit(5). Net cost = 0.         u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
         u2502
         u25bc
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 STEP 4: WIRING GATE HOOK                                             u2502
u2502 (only if wiring_gate_mode != "off")                                  u2502
u2502                                                                      u2502
u2502 4a. Guard: can_run_wiring_gate()?                                    u2502
u2502     If NO u2192 skip wiring entirely, return result unchanged             u2502
u2502                                                                      u2502
u2502 4b. Debit: debit_wiring(wiring_analysis_turns)  # debit 1 turn       u2502
u2502     consumed += 1, wiring_turns_used += 1, wiring_analyses_count += 1u2502
u2502     If available < 3 after debit: set wiring_budget_exhausted = 1     u2502
u2502                                                                      u2502
u2502 4c. Run wiring analysis                                              u2502
u2502                                                                      u2502
u2502 4d. Credit (see section 4 below for mode-specific behavior)           u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
         u2502
         u25bc
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 STEP 5: ANTI-INSTINCT GATE HOOK                                      u2502
u2502 (only if gate_rollout_mode is "soft" or "full")                      u2502
u2502                                                                      u2502
u2502 5a. Evaluate gate on task output artifact                             u2502
u2502                                                                      u2502
u2502 5b. If PASS:                                                         u2502
u2502     credit = floor(turns_consumed * 0.8)                              u2502
u2502     ledger.credit(credit)                                            u2502
u2502                                                                      u2502
u2502 5c. If FAIL + can_remediate():                                       u2502
u2502     (inline fail logic, no retry — deferred to v3.2)                 u2502
u2502     gate_outcome = FAIL                                              u2502
u2502     full mode: task status = FAIL                                    u2502
u2502                                                                      u2502
u2502 5d. If FAIL + !can_remediate():                                      u2502
u2502     gate_outcome = FAIL (BUDGET_EXHAUSTED logged)                    u2502
u2502     full mode: task status = FAIL                                    u2502
u2502                                                                      u2502
u2502 WITH CURRENT DEFAULTS: turns_consumed=0, so credit = floor(0*0.8)=0  u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
         u2502
         u25bc
       [NEXT TASK]
```

---

## 4. All Debit Points (Where Budget Is Consumed)

### 4a. Task pre-allocation

**Where:** `executor.py:976`
**When:** Before every task subprocess launch.
**Amount:** `minimum_allocation` (default **5**).

```python
ledger.debit(ledger.minimum_allocation)  # consumed += 5
```

This is a reservation. If the task uses fewer turns, the difference is
credited back in step 3 (reconciliation).

### 4b. Task actual consumption (reconciliation overshoot)

**Where:** `executor.py:1013`
**When:** After subprocess exits, if actual turns > pre-allocated.
**Amount:** `actual - minimum_allocation`.

```python
if actual > pre_allocated:
    ledger.debit(actual - pre_allocated)
```

With the current `turns_consumed=0` hardcode, this branch never fires.

### 4c. Wiring analysis debit

**Where:** `executor.py:490`
**When:** Before every wiring analysis run (if mode != off and budget allows).
**Amount:** `config.wiring_analysis_turns` (default **1**).

```python
ledger.debit_wiring(config.wiring_analysis_turns)
# consumed += 1
# wiring_turns_used += 1
# wiring_analyses_count += 1
# if available < 3: wiring_budget_exhausted = 1
```

### 4d. Wiring remediation debit

**Where:** `executor.py:573`
**When:** In `full` mode only, when blocking findings exist AND `can_remediate()` is true.
**Amount:** `config.remediation_cost` (default **2**).

```python
ledger.debit(config.remediation_cost)  # consumed += 2
```

This is the most expensive single debit. It fires only when wiring
analysis finds critical/major issues and has budget to attempt a fix.

---

## 5. All Credit Points (Where Budget Is Reimbursed)

### 5a. Task reconciliation (undershoot)

**Where:** `executor.py:1015`
**When:** After subprocess exits, if actual turns < pre-allocated.
**Amount:** `minimum_allocation - actual`.

```python
if actual < pre_allocated:
    ledger.credit(pre_allocated - actual)  # reimbursed += (5 - actual)
```

With `turns_consumed=0`, this always credits back the full 5. Net effect:
the pre-allocation debit is fully reversed.

### 5b. Wiring gate credit

**Where:** `executor.py:533, 549, 586, 608`
**When:** After wiring analysis completes without blocking the task.

| Wiring Mode | When Credited | Amount |
|-------------|---------------|--------|
| `shadow` | Always | `credit_wiring(wiring_analysis_turns)` |
| `soft` | Always | `credit_wiring(wiring_analysis_turns)` |
| `full` + no blocking findings | Always | `credit_wiring(wiring_analysis_turns)` |
| `full` + blocking + remediation **succeeds** | After recheck | `credit_wiring(wiring_analysis_turns)` |
| `full` + blocking + remediation **fails** | Never | u2014 |

**CRITICAL SUBTLETY:** `credit_wiring()` applies `floor(turns * rate)`.
With defaults (`turns=1, rate=0.8`), `floor(1 * 0.8) = 0`. The wiring
credit is **always zero** with default settings. This is documented as
intentional: "By design: `credit_wiring(1, 0.8)` returns 0 credits (R7)."

So with defaults, every wiring analysis costs exactly 1 turn permanently.
To get actual credits, either `wiring_analysis_turns` must be >= 2 or the
`reimbursement_rate` must be set to 1.0.

### 5c. Anti-instinct gate credit

**Where:** `executor.py:867-868`
**When:** In `soft` or `full` mode, when the gate **passes**.
**Amount:** `floor(turns_consumed * reimbursement_rate)`.

```python
credit_amount = int(task_result.turns_consumed * ledger.reimbursement_rate)
ledger.credit(credit_amount)
```

With `turns_consumed=0`, this always credits 0. When turn counting is
wired up, a task that consumed 10 turns and passed its gate would get
`floor(10 * 0.8) = 8` turns reimbursed.

---

## 6. Exhaustion Scenarios

### 6a. Task launch exhaustion

**Guard:** `can_launch()` u2014 `available >= minimum_allocation (5)`
**Where checked:** `executor.py:960`
**Consequence:** All remaining tasks in the phase are marked SKIPPED.
The phase continues to completion (no sprint halt).

```python
if ledger is not None and not ledger.can_launch():
    remaining = [t.task_id for t in tasks[i:]]
    for t in tasks[i:]:
        results.append(TaskResult(task=t, status=TaskStatus.SKIPPED, ...))
    break  # exits the per-task loop (NOT the per-phase loop)
```

### 6b. Wiring gate exhaustion

**Guard:** `can_run_wiring_gate()` u2014 `wiring_budget_exhausted == 0 AND available >= 3`
**Where checked:** `executor.py:481`
**Consequence:** Wiring analysis is silently skipped for this task.
The task result is returned unchanged. Logged as INFO.

```python
if ledger is not None and not ledger.can_run_wiring_gate():
    _wiring_logger.info("Wiring hook skipped for task %s: budget exhausted", ...)
    return task_result
```

The `wiring_budget_exhausted` flag is sticky: once set (in `debit_wiring`
when `available < 3`), it stays set permanently. All future wiring
analyses are skipped even if credits later bring the balance back above 3.

### 6c. Remediation exhaustion (wiring)

**Guard:** `can_remediate()` u2014 `available >= minimum_remediation_budget (3)`
**Where checked:** `executor.py:568` (wiring full mode)
**Consequence:** Remediation is skipped. The FAIL status persists.
Logged as WARNING ("BUDGET_EXHAUSTED").

### 6d. Remediation exhaustion (anti-instinct)

**Guard:** `can_remediate()` u2014 `available >= 3`
**Where checked:** `executor.py:885`
**Consequence:** gate_outcome set to FAIL. In `full` mode, task status
set to FAIL. Logged as WARNING.

### 6e. Whole-phase subprocess budget exhaustion

**Guard:** None in the ledger u2014 detected by output analysis.
**Where checked:** `executor.py:1842`
**Detection:** `detect_error_max_turns()` scans the NDJSON output for
`"subtype":"error_max_turns"`, which Claude CLI emits when a subprocess
hits its `--max-turns` limit.
**Consequence:** Phase status is reclassified from PASS to INCOMPLETE,
which triggers a sprint HALT.

This is separate from the TurnLedger. It's the Claude CLI's own
per-subprocess turn limit, not the sprint-wide budget.

---

## 7. Practical Budget Math With Current Defaults

Given the `turns_consumed=0` hardcode in `_run_task_subprocess()`, here
is what actually happens to the ledger during a sprint:

### Example: 6 phases, 100 max_turns, 5 tasks per phase, wiring=soft

```
initial_budget = 100 * 6 = 600

Per task:
  Step 1: debit(5)          u2192 consumed = 5
  Step 2: subprocess runs      (turns_consumed = 0)
  Step 3: credit(5 - 0 = 5) u2192 reimbursed = 5     u2190 fully reversed
  Step 4: debit_wiring(1)   u2192 consumed = 6
          credit_wiring(1)  u2192 floor(1*0.8) = 0   u2190 zero credit
  Step 5: anti-instinct     u2192 floor(0*0.8) = 0   u2190 zero credit

  Net cost per task: 1 turn (wiring only)

Per phase (5 tasks):
  Net cost: 5 turns

Full sprint (6 phases, 30 tasks):
  consumed = 30 * 6 = 180    (5 pre-alloc + 1 wiring per task)
  reimbursed = 30 * 5 = 150  (reconciliation credits)
  available = 600 - 180 + 150 = 570
```

The budget drains at 1 turn per task (wiring analysis cost). With 600
initial budget, the sprint can run 597 tasks before `can_launch()` fails
(available needs to stay >= 3 for wiring, then >= 5 for launch).

**Exhaustion is practically unreachable with current defaults.** The
budget system is infrastructure waiting for turn counting to be wired up.

### When turn counting IS wired up (hypothetical)

If each task consumed 20 turns:

```
Per task:
  Step 1: debit(5)          u2192 consumed = 5
  Step 3: debit(20 - 5 = 15)u2192 consumed = 20
  Step 4: debit_wiring(1)   u2192 consumed = 21,  credit_wiring = 0
  Step 5: credit(20*0.8=16) u2192 reimbursed = 16  (if gate passes)

  Net cost per task (gate pass): 21 - 16 = 5 turns
  Net cost per task (gate fail): 21 turns

Full sprint (30 tasks, all gates pass):
  consumed = 30 * 21 = 630
  reimbursed = 30 * 16 = 480
  available = 600 - 630 + 480 = 450

Full sprint (30 tasks, all gates fail):
  consumed = 30 * 21 = 630
  reimbursed = 0
  available = 600 - 630 + 0 = -30  u2190 exhausted around task 28
```

With turn counting active, the anti-instinct gate credit becomes the
major budget recovery mechanism: 80% of consumed turns flow back on
pass, making the effective cost per task only ~20% of actual consumption.
Consistent gate failures drain the budget fast.

---

## 8. Budget Flow Diagram

```
                    u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
                    u2502      TurnLedger           u2502
                    u2502                            u2502
                    u2502  initial: 600              u2502
                    u2502  consumed: 0  reimbursed: 0u2502
                    u2502  available() = 600          u2502
                    u2514u2500u2500u2500u2500u2500u2500u2500u252cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u252cu2500u2500u2500u2500u2500u2500u2500u2500u2518
                DEBIT u2502          u2502 CREDIT
          u250cu2500u2500u2500u2500u2500u2500u2500u2500u2534u2500u2500u2500u2510    u2502
          u2502              u2502    u2502
          u25bc              u2502    u25bc
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510 u2502  u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 Task pre-alloc u2502 u2502  u2502 Reconciliation     u2502
u2502 debit(5)       u2502 u2502  u2502 credit(5-actual)   u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518 u2502  u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510 u2502  u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 Task overshoot u2502 u2502  u2502 Wiring credit      u2502
u2502 debit(N-5)     u2502 u2502  u2502 credit_wiring(1)   u2502
u2502 (if N > 5)     u2502 u2502  u2502 = floor(1*0.8) = 0 u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518 u2502  u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510 u2502  u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
u2502 Wiring debit   u2502 u2502  u2502 Anti-instinct      u2502
u2502 debit_wiring(1)u2502 u2502  u2502 credit(N*0.8)      u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518 u2502  u2502 (soft/full + PASS) u2502
u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510 u2502  u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518
u2502 Remediation    u2502 u2502
u2502 debit(2)       u2502 u2502
u2502 (full+blocking)u2502 u2502
u2514u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2518 u2502
                    u2502
                    u25bc
          u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
          u2502   EXHAUSTION    u2502
          u2502   CHECKS        u2502
          u2514u2500u2500u2500u2500u2500u2500u252cu2500u2500u2500u2500u2500u2500u2500u2500u2518
                 u2502
     u250cu2500u2500u2500u2500u2500u2500u2500u2500u2500u253cu2500u2500u2500u2500u2500u2500u2500u2500u2500u2510
     u2502           u2502           u2502
     u25bc           u25bc           u25bc
 can_launch  can_run_    can_remediate
  avail>=5  wiring_gate   avail>=3
     u2502      avail>=3        u2502
     u2502      + !exhausted    u2502
     u25bc           u2502           u25bc
 SKIP all    skip wiring  skip remediation
 remaining   for task     log BUDGET_EXHAUSTED
 tasks
```

---

## 9. Design Gaps and Open Items

### 9a. Turn counting returns 0

`_run_task_subprocess()` at line 1092 returns `(exit_code, 0, output_bytes)`,
with a comment: "Turn counting is wired separately in T02.06." Until this
is implemented, the pre-allocation reconciliation always credits back the
full 5 turns, and the anti-instinct credit is always 0. The budget
effectively only drains from wiring analysis (1 turn per task).

### 9b. Wiring credit is always zero

`credit_wiring(1, rate=0.8)` computes `floor(1 * 0.8) = 0`. This is
documented as intentional ("R7"), but it means wiring analysis has a
permanent 1-turn cost that is never recovered. To enable actual credits,
either increase `wiring_analysis_turns` to >= 2, or set the rate to 1.0.

### 9c. Sticky wiring exhaustion flag

`wiring_budget_exhausted` is a one-way flag. Once `debit_wiring()` drops
`available` below 3, it's set to 1 and never cleared. Even if credits
later bring the balance above 3, `can_run_wiring_gate()` still returns
False. This is a deliberate conservative design but could be surprising.

### 9d. No cross-phase budget reset

The ledger is sprint-wide. There is no per-phase budget reset or
per-phase budget allocation. A phase with many tasks can consume budget
that was "intended" for later phases.

### 9e. Anti-instinct remediation is a stub

The anti-instinct FAIL path (executor.py:882) has a comment: "Spec says
this path should delegate to `attempt_remediation()` for retry-once
semantics. We use inline fail logic as an intentional v3.1
simplification. Deferred to v3.2." Currently it just sets FAIL status
without any retry.
