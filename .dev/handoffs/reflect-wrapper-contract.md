# Reflect-Wrapper ⇄ Generators — Interface Contract

> **Authoritative.** This file is the SINGLE source the generator worktree
> (`ReflectInTaskLists`, branch `reflect/f3-hygiene-stage105-e2e`) reads to wire
> the terminal/per-phase reflect gates. **Do NOT re-derive any of this.** The
> wrapper worktree (`reflectWrapper`) OWNS this file + the wrapper engine; the
> generator worktree OWNS gate emission and MUST conform to the shapes below.
>
> - Contract version: **1.0** (wrapper engine target: `superclaude reflect run`
>   auto-fix evolution; reflect skill contract target: `return-contract.yaml`
>   `contract_version 1.4.0`).
> - Design source: `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md`
> - Canonical wrapper base: worktree `wrapper-onto-master`,
>   `src/superclaude/cli/reflect/*` (audit-only) + `main.py` registration.
> - **The `--reflect` dial is ABANDONED** (PR #157 closed). Generators MUST NOT
>   emit any `--reflect <none|0|1|2|auto>` flag.

---

## 1. The two gate sites

| Obj | Site | Who emits | What it audits |
|-----|------|-----------|----------------|
| **O1** | terminal task at the END of every task-builder tasklist | `task-builder` | the whole tasklist's work |
| **O2** | gate at the END of every `sc:tasklist` PHASE | `sc:tasklist` | only that phase's work |

Both shell out to the SAME engine: `superclaude reflect run`. The wrapper must be
merged + `pipx install --force`-ed **before** either gate goes live, else every
generated tasklist breaks at `superclaude: no such command`.

---

## 2. Exact invocation shapes

### O1 — whole tasklist (task-builder terminal gate)

```bash
superclaude reflect run <ABS_TASKLIST_PATH> --depth deep --fix --promote
```

- `--base` is **omitted** → the wrapper resolves the base from frontmatter
  `start_commit` (the whole-task base).
- `--fix` (auto-fix loop ON), `--promote` (default; `task` adapter promotes the
  tasklist dir `.dev/tasks/to-do/TASK-* → .dev/tasks/done/TASK-*`).
- `--depth deep` forces Tier-2 heterogeneous fan-out.

### O2 — per-phase (sc:tasklist end-of-phase gate)

```bash
superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>
```

- `--base <PHASE_N_START_SHA>` pins the audit to phase-N work ONLY (single ref vs
  working tree — NOT a `<base>..HEAD` range).
- `--no-promote` is **required** for O2 (see §5 — there is no per-phase promotion
  adapter).

### Flags the generators MUST NOT emit

`--reflect …` (abandoned dial), `--max-turns` (no such flag), any
`<base>..HEAD` range form for `--base`. `--depth` accepts only `standard|deep`.

### Exit-code consumption (unchanged from v1, fail-closed)

| Exit | Verdict | Gate meaning |
|------|---------|--------------|
| 0 | pass | clean OR auto-fixed-and-verified (and promoted if O1) → gate PASSES |
| 10 | halted | deviations a human must resolve, or fix loop did not converge → gate FAILS, surface |
| 11 | degraded | audit untrustworthy (lost chain-critical capability) → gate FAILS |
| 2 | blocked | child crash / timeout / missing-or-bad contract → gate FAILS |

Only exit 0 may let the tasklist/phase complete.

---

## 3. Recursion breaker (CONTRACT POINT — load-bearing)

**Marker:** environment variable `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.

**Why it exists.** When the wrapper auto-fixes (O1 `--fix`), it auto-runs the
remediation MDTM file that reflect authored via `task-builder`. That remediation
tasklist ALSO carries an O1 terminal gate → without a breaker, the gate re-invokes
the wrapper → reflect → new remediation → … forever.

**Semantics (both parties):**

1. **Wrapper (primary breaker):** `superclaude reflect run` reads the marker at
   startup. If it equals `"1"`, the wrapper **immediately exits 0** ("nested gate
   suppressed") before any audit. The wrapper EXPORTS `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`
   into the environment of every child it spawns inside the fix subtree (the
   reflect audit subprocess AND every auto-run `/task`). This alone terminates
   the recursion; the outer wrapper owns the real re-verification.

2. **Generators (obligations):**
   - MUST NOT clear, unset, or overwrite `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
   - Exception: executors MAY remove `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` only from
     ordinary verification/build/test subprocess environments that cannot emit or
     execute reflect gates; they MUST preserve it for reflect audits, reflect gate
     commands, and auto-run `/task` execution so nested-gate suppression remains
     intact.
   - SHOULD additionally **skip emitting / skip executing** the gate when the
     marker is already `"1"` at gate time (belt-and-suspenders). A safe emission
     shape:
     ```bash
     if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then
       echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0
     fi
     superclaude reflect run <FILE> --depth deep --fix [--promote|--no-promote --base <SHA>]
     ```
   - MUST NOT introduce a SECOND marker or rename this one.

Truthy value is exactly the string `"1"`. Absent/empty/any-other-value ⇒ not
suppressed (normal run).

---

## 4. Auto-fix / HALT contract (decisions D1, D3, D4)

The wrapper, when `--fix` is set, runs a bounded **audit → apply → re-verify**
loop. It auto-applies ONLY mechanically-unambiguous deviations; everything a
human must decide HALTs.

**AUTO-FIXABLE** (wrapper auto-runs the authored `/task`, then re-audits) ⇔ the
audit HALTED *solely* because of `drift>0` and/or `necessary`-class items, AND
**none** of: `regression_present`, `needs_human_decision` (= grounding-gaps
non-empty), `user_decision_required`, `unauthorized_deviation_present`.

**HUMAN-REQUIRED — terminal HALT (exit 10), never auto-fixed, never promoted** ⇔
any of: `regression_present`, `needs_human_decision`, `user_decision_required`,
`unauthorized_deviation_present`, non-empty grounding-gaps, OR a `degraded`/`blocked`
verdict.

**Bound (D3):** `--max-fix-iterations N` (wrapper default **2**). After N
apply→verify cycles without reaching `pass`, terminal HALT (exit 10). The
`wrapper-result.yaml` sidecar records `fix_iterations` and `fix_converged: bool`.

**Enabling field the generators do NOT touch but should know exists:** reflect's
`return-contract.yaml` (`1.4.0`) emits `remediation_task_path: <abs>|null` — the
file the wrapper auto-runs. Generators never read it; it is wrapper↔reflect only.

This honors `feedback_human_decision_items_must_halt`: a `needs_human_decision`
item NEVER gets an auto-applied default that ships a change.

---

## 5. Promotion scope (decision D5)

`--promote` is the wrapper's **default**. But reflect has exactly two promotion
adapters — `task` (`.dev/tasks/to-do/TASK-* → done/`) and `sprint-release`
(`.dev/releases/current/ → complete/`). **There is NO per-phase adapter.**

| Site | Promote flag the generator emits | Effect |
|------|----------------------------------|--------|
| **O1** (whole tasklist) | `--promote` (or omit — it's default) | `task` adapter moves the tasklist dir to `done/` on a clean/auto-fixed PASS |
| **O2** (per-phase) | **`--no-promote` (REQUIRED)** | phase gate auto-fixes + verifies but does NOT promote; promotion happens once at tasklist/release level |

Generators MUST NOT attempt to make O2 promote. No per-phase adapter will be
added (keeps the wrapper thin; reflect remains promotion SoT).

---

## 6. Frontmatter the generators MUST persist

The wrapper reads these from the audited file's frontmatter. Generators are
responsible for writing them at build/emit time.

| Key | Required for | Shape | Consumed as |
|-----|--------------|-------|-------------|
| `start_commit` | **O1** | git SHA string | whole-task `--diff` base (when `--base` omitted) |
| per-phase `start_commit` | **O2** | git SHA string, one per phase | surfaced to that phase's gate as `--base <SHA>` |
| `executor_model_class` | O1 + O2 | model-class alias string (e.g. `sonnet`) | reflect `--executor-model` (anti-self-confirmation: reviewers must differ from the executor) |

Notes:
- For O2, the generator records each phase's start SHA and passes it on that
  phase's gate line as `--base <PHASE_N_START_SHA>`. Equivalent alternative: write
  a per-phase `start_commit` the wrapper can resolve — but the **explicit `--base`
  on the gate line is the canonical path** (precedence: `--base` > frontmatter
  `start_commit` > `git merge-base HEAD master`).
- `reflect_post:` is written BACK by the wrapper — generators must leave room for
  it (do not hand-author or lock it).

---

## 7. Cost band (decision D7 — informational)

`--depth deep` forces Tier 2: ≈ **35–70k tokens / 8–15 min per audit**. The O1
auto-fix loop runs `(iterations+1)` audits + `iterations` `/task` applies
(iterations ≤ 2 default). O1+O2 means this runs **per phase AND per tasklist** —
the operator chose deep-everywhere deliberately. Generators do not need to budget;
the wrapper enforces `--max-fix-iterations` and the NFR-5 subprocess timeout
(default 3600s).

---

## 8. Conformance checklist for the generator worktree

- [ ] O1 gate emits `superclaude reflect run <abs> --depth deep --fix --promote`.
- [ ] O2 gate emits `superclaude reflect run <abs> --depth deep --fix --no-promote --base <phase-start-sha>`.
- [ ] No `--reflect …` dial flag anywhere.
- [ ] Gate is wrapped with the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard (§3.2).
- [ ] `start_commit` (O1) and per-phase start SHA (O2) are persisted/passed.
- [ ] `executor_model_class` persisted in frontmatter.
- [ ] Gates do not run before the wrapper is `pipx install --force`-ed (§1).
- [ ] Consumes exit codes 0/10/11/2 per §2 (only 0 completes the gate).
