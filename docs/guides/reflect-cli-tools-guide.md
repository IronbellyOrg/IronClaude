# Reflect CLI Tools — Auto-Fix Engine Guide

This guide covers the `superclaude reflect run` CLI auto-fix engine introduced by
PR #159. It explains:

- what the command does,
- when to use it,
- how to run it,
- the full flag surface and defaults,
- the auto-fixable vs human-required carve-out,
- exit codes and fail-closed semantics,
- and how it fits into the **task / per-phase gate → audit → auto-fix → verify → promote** workflow.

---

## 1) Release Summary (What was finalized)

### From audit-only (v1) to a validate→review→auto-fix→verify→promote engine

The shipped v1 of `superclaude reflect run` was **audit-only**: it launched a
single `/sc:reflect --mode post` pass, parsed `return-contract.yaml`, derived a
fail-closed 4-state verdict, and wrote a `reflect_post:` block back into the
tasklist frontmatter. It never repaired anything — a HALTED audit was terminal.

PR #159 evolves that command into a **bounded auto-fix engine** while keeping the
v1 fail-closed contract intact. The new engine runs a state machine:

```text
audit → derive 4-state verdict → classify (auto-fixable vs human-required)
      → [auto-run corrective /task → re-verify] (bounded) → promote (gated)
```

The new wrapper surface is intentionally narrow (the heavy reflect logic — waves,
tiers, the 4-category deviation taxonomy, promotion mechanics — stays inside the
`sc-reflect-protocol` skill). What PR #159 adds is **only**:

- the bounded **auto-fix loop** (`--fix/--no-fix`, `--max-fix-iterations`),
- the **`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion breaker**,
- the **`--base`** per-phase audit-scope override,
- the **`--promote` default flip** (promotion is now on by default),
- and consumption of the new `remediation_task_path` contract field.

The wrapper consumes `return-contract.yaml`; it never re-derives a verdict from
raw diffs. Implementation lives in `src/superclaude/cli/reflect/` (`commands.py`,
`config.py`, `runner.py`, `contract.py`, `models.py`).

### The state machine (the heart of the engine)

1. **Recursion-breaker check.** If `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`, exit
   `0` immediately ("nested gate suppressed") before any audit runs.
2. **Audit (A).** Launch `/sc:reflect --mode post --diff <BASE> --tasklist <file>
   --depth <d>` (plus `--remediate` when `--fix` is set) as a top-level
   `claude --print` subprocess.
3. **Derive verdict.** Parse `return-contract.yaml` into one of four states:
   `pass` / `halted` / `degraded` / `blocked` (first-match-wins ordering:
   `blocked → degraded → halted → pass`).
4. **Classify + act.**
   - `PASS` → converged. Promote if eligible.
   - `HALTED` **auto-fixable** (drift/necessary only) → auto-run the corrective
     `/task <remediation_task_path>` (B), then re-verify (back to A).
   - `HALTED` **human-required** (regression / human-decision / gaps) → terminal
     HALT, no auto-fix, no promote.
   - `DEGRADED` / `BLOCKED` → audit untrusted, never auto-fixed.
5. **Bound.** The loop runs at most `--max-fix-iterations` apply→verify cycles
   (default 2). Non-convergence after the bound → terminal HALT.

Convergence = the loop reaches `PASS`. Only a clean (or successfully auto-fixed)
`PASS` exits `0`.

---

## 2) Command Reference — When and How to Use

## `superclaude reflect run`

### What it does

Runs the post-execution reflect gate for a single MDTM task file. For Tier 2
(`--depth standard|deep`), it routes through the local ensemble driver, which
uses the swarm dispatch surface to fan out across heterogeneous reviewers and
writes the pinned `return-contract.yaml`. The Tier-1 grounded path remains the
single `/sc:reflect --mode post` top-level `claude --print` subprocess path. The
wrapper parses `return-contract.yaml`, derives a fail-closed 4-state verdict,
and — under `--fix` — runs a bounded auto-fix loop before writing a
`reflect_post:` block back into the tasklist frontmatter. Only a clean, full,
non-degraded Tier-2 pass exits `0`.

### Use when

- You are gating a completed MDTM task (O1) or an end-of-phase tasklist (O2) and
  want an independent, anti-bias adherence audit before promotion.
- You want drift / necessary-class divergences auto-repaired and re-verified with
  zero human intervention on the common path.
- You want a fail-closed gate: regression, human-decision items, degraded audits,
  and crashes must HALT rather than silently pass.

### Syntax

```bash
superclaude reflect run <tasklist_path> [options]
```

`<tasklist_path>` is the absolute (or resolvable) path to the MDTM task file whose
`reflect_post:` frontmatter block this command writes back. The process exit code
**is** the fail-closed verdict code.

### Key options

The exact option set and defaults below are read from
`src/superclaude/cli/reflect/commands.py`.

- `--fix` / `--no-fix` — run the bounded audit→apply→re-verify auto-fix loop.
  **Default: `--no-fix`** (audit-only). O1/O2 gate callers pass `--fix`.
- `--max-fix-iterations N` — max apply→verify cycles before terminal HALT.
  **Default: `2`.**
- `--base <ref>` — explicit audit base ref (a single ref vs the working tree).
  **Highest precedence** over frontmatter `start_commit` and the
  `git merge-base HEAD master` fallback. Stored verbatim as a single ref (never a
  `<ref>..HEAD` range).
- `--promote` / `--no-promote` — allow reflect's gated Wave-7 promotion.
  **Default: `--promote`.** O2 (per-phase) callers pass `--no-promote`.
- `--reachability` / `--no-reachability` — enable the §6.1 step-5.6 contracted-sink
  reachability & oracle-admissibility gate (UC-2). **Default: `--reachability`.** Pass
  `--no-reachability` for a telemetry-only skip.
- `--depth standard|deep` — reflect depth passthrough (POST never runs quick).
  **Default: `standard`.** Callers force Tier 2 with `--depth deep`.
- `--transport openai_compat|stub` — Tier-2 reviewer transport.
  **Default: `openai_compat`.** Use `stub` for deterministic, credit-free CI.
- `--reviewers N` — Tier-2 reviewer slots. **Default: `3`.** Values 2-4 are
  clamped to the supported range; `1` is preserved for the negative witness path.
- `--isolate-reviewers` / `--no-isolate-reviewers` — opt in to L2 reviewer
  isolation: ground the Wave-3 reviewers (Tier-1 audit child + adversarial scorer)
  in an isolated `git worktree` snapshot of the committed audit ref, never the live
  shared worktree, so a reviewer can never read another session's mid-commit state
  or mutate the repository it is auditing. **Default: `--no-isolate-reviewers`** —
  OFF preserves today's dirty-tree-audit behavior (#153) byte-for-byte. When ON, a
  non-committable (dirty / uncommitted / unresolvable-base / HEAD-moved) audit
  target STOPs with `status: stopped-precondition` → **BLOCKED** (exit 2).
- `--tmux` — run inside a detached tmux window so you can watch the run live.
- `--resume` — skip the launch when the prior `reflect_post` is a `pass` on the
  current HEAD (clean-HEAD short-circuit).
- `--dry-run` — derive + preflight + construct the command, but do **not** launch
  the subprocess or edit the task file.
- `--print-command` — print the composed `claude` argv + prompt and exit without
  launching.
- `--output <dir>` — pinned output directory.
  **Default: `<task-dir>/reflect/post/<short-sha>/`** (the short SHA is `HEAD[:12]`,
  the 12-char prefix of the resolved HEAD). It must **not** resolve under
  `.claude/{skills,agents,commands}` (a reflect STOP → exit 2).
- `--allow-single-vendor` — do not flag **DEGRADED** (exit 11) on single-vendor
  Tier-2 reviewer diversity (suppresses the single-vendor degradation trigger;
  single-vendor is a DEGRADED signal, not a HALTED one).
- `--timeout <seconds>` — subprocess timeout. **Default: `3600`.** A child
  timeout (rc `124`) routes to `blocked` (exit 2).

> **On the executor model.** The `run` command does **not** expose an
> `--executor-model` flag. The anti-self-confirmation executor class is resolved
> internally (`config.py`): first from the `EXECUTOR_MODEL_CLASS` environment
> variable, then from the tasklist frontmatter key `executor_model_class`, and is
> passed through to reflect as `--executor-model` only when present. Persist
> `executor_model_class` in the tasklist frontmatter so reviewers differ from the
> executor.

### Examples

```bash
# Audit-only (v1 behavior): one reflect pass, no auto-fix, no promote
superclaude reflect run path/to/TASK.md --no-fix --no-promote

# O1 — whole-tasklist gate: deep Tier-2 audit, bounded auto-fix, promote by default
superclaude reflect run .dev/tasks/to-do/TASK-RF-XXXX/TASK.md --depth deep --fix --promote

# O2 — per-phase gate: scope the audit to phase-N work, verify but do NOT promote
superclaude reflect run path/to/phase-3-tasklist.md \
  --depth deep --fix --no-promote --base <phase-3-start-sha>

# Watch a run live in a detached tmux window
superclaude reflect run path/to/TASK.md --tmux

# Preview the composed claude argv + prompt without launching anything
superclaude reflect run path/to/TASK.md --depth deep --print-command

# Cap the fix loop at a single apply→verify cycle
superclaude reflect run path/to/TASK.md --fix --max-fix-iterations 1

# Skip the launch when the prior verdict is a clean pass on the current HEAD
superclaude reflect run path/to/TASK.md --resume
```

---

## 3) The Auto-Fixable vs Human-Required Carve-Out

The engine never auto-applies a change a human must review. After a HALTED audit,
the wrapper classifies the result using **only existing contract fields** (no new
logic) via `classify_fix` in `contract.py`. It returns one of `auto-fixable`,
`human-required`, or `none`.

### HUMAN-REQUIRED → terminal HALT (no auto-fix, no promote)

The verdict is classified `human-required` (and the loop stops, exit `10`) on
**any** of these hard signals:

- `regression_present: true`
- `needs_human_decision: true` — the contract guarantees this is true **iff**
  `grounding-gaps.yaml` is non-empty, so a grounding-gaps-only audit lands here.
- `user_decision_required: true`
- `unauthorized_deviation_present: true`
- `deviation_count_by_class.regression > 0`

### AUTO-FIXABLE → auto-run the corrective `/task`, then re-verify

The verdict is classified `auto-fixable` **only when no hard signal above is
present** and the deviation register is solely drift and/or necessary-class:

- `deviation_count_by_class.drift > 0`, **or**
- `deviation_count_by_class.necessary > 0`

On `auto-fixable` with a present `remediation_task_path`, the wrapper auto-runs
`/task <remediation_task_path>` as its own top-level subprocess, then re-audits
against the same base. If `remediation_task_path` is **absent** on an
auto-fixable verdict, the wrapper **cannot repair** → terminal HALT (exit 10).

### `none` → clean

No drift, no necessary, no hard signal — nothing to fix.

> **The classifier is consulted only on a trustworthy HALTED result.** DEGRADED
> and BLOCKED verdicts are terminal upstream in `derive_verdict` and re-guarded in
> the runner loop, so they are never auto-fixed even if their deviation dict
> coincidentally carries `drift > 0`.

### Verdict → action summary

| Contract signal (post-audit)                            | Verdict   | `--fix` action                                | Promote?         |
|---------------------------------------------------------|-----------|-----------------------------------------------|------------------|
| `status: success` AND tier reached as expected          | PASS      | none (converged)                              | O1: yes / O2: no |
| `drift>0` and/or `necessary` only; no reg/human/gaps    | HALTED    | auto-run `remediation_task_path`, re-verify   | only after PASS  |
| `regression_present: true` or `deviations.regression>0` | HALTED    | **none — terminal HALT**                      | never            |
| `needs_human_decision: true` (grounding-gaps non-empty) | HALTED    | **none — terminal HALT**                      | never            |
| `user_decision_required: true`                          | HALTED    | **none — terminal HALT**                      | never            |
| `unauthorized_deviation_present: true`                  | HALTED    | **none — terminal HALT**                      | never            |
| any degraded trigger                                    | DEGRADED  | **none — exit 11**                            | never            |
| child crash / timeout / contract-missing / bad-version  | BLOCKED   | **none — exit 2**                             | never            |

---

## 4) Exit Codes (the fail-closed contract)

The process exit code **is** the verdict code. Only `PASS` exits `0`. The mapping
is defined once on `Verdict.exit_code` in `models.py` and is never hardcoded a
second time.

| Verdict   | Exit code | Meaning                                                                    |
|-----------|-----------|----------------------------------------------------------------------------|
| `pass`    | **0**     | Clean (or successfully auto-fixed) full, non-degraded Tier-2 pass. The **only** exit-0 path. |
| `halted`  | **10**    | A trustworthy audit found deviations/partial work; human-required or non-convergent after the fix bound. |
| `degraded`| **11**    | Chain-critical reviewer/tooling loss made the audit untrustworthy — never auto-fixed. |
| `blocked` | **2**     | Child crash, timeout (rc 124), missing/unparseable contract, bad contract version, or a config/preflight STOP. |

A config or preflight STOP (for example, an `--output` resolving under
`.claude/{skills,agents,commands}`) routes to `blocked` (exit 2) before the
runner launches anything.

---

## 5) The Dual Termination Guarantee

The engine cannot loop forever. Two independent mechanisms jointly guarantee
termination.

### 5.1 The recursion breaker — `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`

When the wrapper spawns a child subprocess inside the fix subtree — both the
reflect audit AND every auto-run `/task` — it exports
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into that child's environment.

If a child's own terminal reflect gate then fires `superclaude reflect run` again,
the group callback in `commands.py` reads the marker at parse time and **exits `0`
immediately** ("nested gate suppressed") **before any audit runs** — and before
Click validates the tasklist path argument, so a nested gate on a since-moved file
still exits cleanly.

The truthy value is **exactly the string `"1"`**. Absent, empty, `"0"`, `"2"`, or
any other value does **not** suppress — those run normally. This prevents an
infinite wrapper ↔ remediation-tasklist recursion: the corrective tasklist
self-suppresses its own gate, and the **outer** wrapper owns the real
re-verification.

### 5.2 The iteration bound — `--max-fix-iterations`

Even with the recursion breaker, a non-converging fix loop is bounded by
`--max-fix-iterations` (default `2`). After N apply→verify cycles without reaching
`PASS`, the wrapper performs a terminal HALT (exit `10`), does **not** promote,
and surfaces the last `report_path` plus the `wrapper-result.yaml` sidecar. The
sidecar records `fix_iterations` (completed cycles) and `fix_converged` (a bool).

The marker kills *nested* gates; `--max-fix-iterations` kills a non-converging
*outer* loop. Together they guarantee the engine always terminates.

---

## 6) O1 vs O2 — The Two Gate Sites

The engine serves two gate sites with different invocation shapes. The wrapper has
no O2-detection surface, so the **caller** (generator) selects the shape.

### O1 — whole tasklist (task-builder terminal gate)

```bash
superclaude reflect run <tasklist.md> --depth deep --fix --promote
```

- `--base` is omitted → the base resolves from the frontmatter `start_commit`
  (the whole-task base).
- Promote-by-default: the `task` adapter promotes
  `.dev/tasks/to-do/TASK-* → done/` once the verdict is a clean (or auto-fixed)
  PASS.

### O2 — per-phase (sc:tasklist end-of-phase gate)

```bash
superclaude reflect run <phase-N-file.md> --depth deep --fix --no-promote --base <phase-N-start-sha>
```

- `--base <phase-N-start-sha>` pins the audit to phase-N work only (a single ref
  vs the working tree), so a phase-N gate does not audit whole-task scope.
- The **generator passes `--no-promote` explicitly** — there is no per-phase
  promotion adapter. Per-phase gates auto-fix-and-verify; promotion lands once at
  the tasklist/release level.

> **Why `--no-promote` is the generator's job, not the wrapper's.** Since the
> `--promote` default flipped to on, an absent flag would default to promote-on.
> The wrapper does **not** force `--no-promote` for O2 (that would require
> thickening it with O2 detection). If the generator omits `--no-promote`,
> reflect's Wave-7 finds no per-phase adapter and safely skips
> (`adapter-unresolved`) — a defaulted O2 promote is a harmless no-op, never a
> mis-promote. The `--tmux` inner reinvocation forwards `--no-promote` explicitly
> for exactly this reason.

---

## 7) Fail-Closed Semantics (Important)

The engine is fail-closed by construction. The following invariants always hold.

- **DEGRADED and BLOCKED are never auto-fixed.** Only a *trustworthy* HALTED
  result is classified for repair. A degraded audit (chain-critical reviewer or
  tooling loss) or a blocked audit (crash, timeout, missing/bad contract) is
  terminal — even if its deviation dict carries `drift > 0`.
- **A failed `/task` apply HALTs — never PASSes.** If the auto-run corrective
  `/task` returns a non-zero exit code, the loop does **not** re-audit (a partial
  state would score garbage and risk a misleading verdict). The verdict is left at
  its HALTED state, the sidecar `reason` records `fix-apply-failed (rc=...)`, and
  the loop breaks **before** incrementing — so there is no audit on a failed apply.
- **Only PASS exits 0.** `halted → 10`, `degraded → 11`, `blocked → 2`.
- **An unwritable or stale frontmatter fails closed.** If the atomic, race-safe
  `reflect_post:` write-back cannot complete (the file changed since it was read,
  or the frontmatter is missing), a would-be PASS is downgraded to BLOCKED
  (exit 2). The `wrapper-result.yaml` sidecar is **always** written regardless, so
  the verdict signal survives even when the frontmatter write fails.
- **The `--tmux` sentinel inverts the sprint fail-open posture.** A missing or
  garbage `.reflect-exitcode` sentinel is treated as `blocked` (exit 2), never
  success.
- **No-launch paths leave no artifacts.** `--dry-run` and `--print-command`
  construct the command and exit without launching the subprocess, editing the
  task file, or writing the exit sentinel.

---

## 8) Quick Command Cheat Sheet

```bash
# Audit-only (v1 behavior): single reflect pass, no repair, no promote
superclaude reflect run <task.md> --no-fix --no-promote

# O1 whole-tasklist gate: deep audit, bounded auto-fix, promote by default
superclaude reflect run <task.md> --depth deep --fix --promote

# O2 per-phase gate: scope to phase-N, verify but do not promote
superclaude reflect run <phase-N.md> --depth deep --fix --no-promote --base <phase-N-start-sha>

# Cap the fix loop at one apply→verify cycle
superclaude reflect run <task.md> --fix --max-fix-iterations 1

# Watch a run live in a detached tmux window
superclaude reflect run <task.md> --tmux

# Preview the composed claude argv + prompt without launching
superclaude reflect run <task.md> --print-command

# Derive + preflight only, no launch, no file edit
superclaude reflect run <task.md> --dry-run

# Skip the launch if the prior verdict is a clean pass on the current HEAD
superclaude reflect run <task.md> --resume

# Allow a single-vendor Tier-2 reviewer set without HALTing
superclaude reflect run <task.md> --allow-single-vendor
```

---

## 9) Notes for Gate-Site Owners

- **Persist the right frontmatter.** O1 needs `start_commit` (whole-task base);
  O2 needs a per-phase `start_commit` surfaced to the gate as `--base <sha>`. Both
  benefit from `executor_model_class` so reviewers differ from the executor.
- **Generators must not clear the marker.** Never unset
  `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`; generators should additionally skip gate
  *emission* when it is already `=1` (belt-and-suspenders alongside the wrapper's
  own self-suppress).
- **Budget for `(N+1)` audits.** A deep Tier-2 audit is the dominant cost; the fix
  loop multiplies it by `(iterations + 1)` audits plus N `/task` runs. With the
  default `--max-fix-iterations 2`, that is at most three audits.
- **Treat exit 11 and exit 2 as "do not promote, surface for a human."** Only an
  exit-0 PASS is promotable.
