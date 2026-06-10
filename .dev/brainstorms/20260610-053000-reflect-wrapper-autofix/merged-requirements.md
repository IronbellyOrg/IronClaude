---
title: "reflect-wrapper AUTO-FIX evolution — merged requirements"
source_brief: .dev/handoffs/reflect-wrapper-autofix-brainstorm-brief.md
canonical_base: "worktree wrapper-onto-master: src/superclaude/cli/reflect/*"
contract_artifact: .dev/handoffs/reflect-wrapper-contract.md
adversarial_status: skipped-by-design
created: 2026-06-10T05:30:00+00:00
---

# reflect-wrapper AUTO-FIX evolution — merged requirements

## 0. Scope & non-goals

**In scope.** Evolve the shipped audit-only `superclaude reflect run` into a
wrapper-orchestrated **validate → review → auto-fix → verify → promote** engine
serving two gate sites (O1 whole-tasklist, O2 per-phase). New wrapper surface is
ONLY: the fix-loop orchestration, the recursion-breaker marker, `--base`, the
promote-default flip, and consuming a new `remediation_task_path` contract field.

**Out of scope / abandoned.** The `--reflect <none|0|1|2|auto>` dial (this
branch's `ecadfe47`, `879bb64f`; PR #157 closed), the 8-value oracle, TB-Add-9,
V1–V16, the 304-line dial test. Not carried forward. The **canonical base** is the
audit-only reflect CLI in worktree `wrapper-onto-master`.

**Hard thinness boundary (NFR-1).** No reflect-logic duplication — waves, tiers,
the 4-category taxonomy, and promotion mechanics stay in `sc-reflect-protocol`.
The wrapper consumes `return-contract.yaml`; it never re-derives a verdict from
raw diffs. No imports from `cli.sprint`/`cli.roadmap`; zero `async`; the only
subprocess-launch path is `ClaudeProcess`.

## 1. The state machine (the heart of the evolution)

```
                ┌─────────────────────────────────────────────┐
                │  superclaude reflect run <file> [--base R]   │
                │  [--depth deep] [--fix] [--promote]          │
                └─────────────────────────────────────────────┘
                                   │
              SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1 ?  ──yes──▶ exit 0  (D2 breaker)
                                   │ no
                                   ▼
                 iteration ← 1 ;  max ← --max-fix-iterations (default 2)
                                   │
   ┌───────────────────────────────▼───────────────────────────────┐
   │ (A) AUDIT: launch /sc:reflect --mode post --diff <BASE>        │
   │     --tasklist <file> --depth <d> [--remediate if --fix]      │
   │     [--no-promote]  as top-level claude --print subprocess     │
   └───────────────────────────────┬───────────────────────────────┘
                                   ▼
                 parse return-contract.yaml → derive 4-state verdict
                                   │
        ┌──────────────┬──────────┴───────────┬──────────────────────┐
        ▼              ▼                       ▼                      ▼
     PASS          HUMAN-REQUIRED         AUTO-FIXABLE            BLOCKED/DEGRADED
   (clean)         HALT class             HALT class             (audit untrusted)
        │              │                       │                      │
        │              ▼                       │                      ▼
        │        exit 10, no promote,          │                exit 11 / exit 2,
        │        surface report                │                no promote, surface
        │                                       │
        │                         --fix set AND iteration ≤ max
        │                         AND remediation_task_path present?
        │                              │ yes              │ no
        │                              ▼                  ▼
        │              (B) APPLY: export marker;     exit 10, surface
        │              claude --print "/task          (cannot repair)
        │              <remediation_task_path>"
        │              as top-level subprocess
        │                              │
        │              iteration += 1 ; ──▶ back to (A)  (RE-VERIFY)
        │
        ▼
   --promote set AND O1-level (task adapter applies)?
        │ yes                         │ no (O2 / --no-promote)
        ▼                             ▼
   reflect Wave-7 promote        exit 0 (verified, not promoted)
        │
        ▼
   exit 0 (promoted)
```

Convergence = the loop reaches PASS. Non-convergence after `max` iterations →
terminal HALT (exit 10), no promote, last report + sidecar surfaced.

## 2. Functional requirements

### FR-1 — Auto-fix loop (D1)
The wrapper gains `--fix/--no-fix` (gate default `--fix`). When `--fix`, the
audit runs with `--remediate` so reflect *authors* (never runs) a Tier-3
corrective MDTM file. On an AUTO-FIXABLE verdict (§3) with a present
`remediation_task_path`, the wrapper auto-executes `/task <path>` as its own
top-level `claude --print` subprocess, then re-runs the audit to verify. Reflect
stays read-only; the wrapper is the sole mutator-orchestrator.

### FR-2 — Recursion breaker (D2, CONTRACT POINT)
Marker env var `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
- The wrapper **exports `=1`** into the environment of every child it spawns
  inside the fix subtree (the reflect audit subprocess AND every auto-run `/task`).
- **Primary breaker (in the wrapper):** at startup, `superclaude reflect run`
  reads the marker; if `=1`, it immediately no-ops **`exit 0`** ("nested gate
  suppressed") before any audit. The remediation tasklist (built by task-builder,
  which per O1 carries its own terminal gate) therefore self-suppresses when the
  wrapper auto-runs it. The OUTER wrapper owns the real re-verification.
- **Generator obligation:** generators MUST NOT clear/unset the marker, and
  SHOULD also skip gate *emission* when it is already `=1` (belt-and-suspenders).

### FR-3 — Bounded fix-loop (D3)
`--max-fix-iterations N` (default **2**). After N apply→verify cycles without
convergence to PASS, terminal HALT (exit 10); do NOT promote; surface the last
`report_path` + `wrapper-result.yaml`. The sidecar records `fix_iterations` and
`fix_converged: bool`.

### FR-4 — Safe-class carve-out (D4)
The wrapper classifies the HALTED verdict using ONLY existing contract fields
(no new logic):
- **AUTO-FIXABLE** ⇔ HALTED caused solely by `drift>0` and/or `necessary`-class
  items AND `regression_present` is not true AND `needs_human_decision` is not
  true AND `user_decision_required` is not true AND grounding-gaps empty.
- **HUMAN-REQUIRED** (terminal HALT, never auto-promoted) ⇔ any of
  `regression_present`, `needs_human_decision`, `user_decision_required`,
  non-empty grounding-gaps, OR a `degraded`/`blocked` verdict.
Auto-fix applies to the AUTO-FIXABLE path only; "promote by default" applies to
the clean OR successfully auto-fixed path only.

### FR-5 — Promote default flip + scope (D5)
`--promote/--no-promote` default flips to **`--promote`**.
- **O1 (whole tasklist):** promote-by-default; the `task` adapter applies
  (`.dev/tasks/to-do/TASK-*`).
- **O2 (per-phase):** the wrapper **forces `--no-promote`** — no per-phase
  adapter exists and adding one would thicken the wrapper. Per-phase gates
  auto-fix-and-verify but do NOT promote. Promotion is tasklist/release-level only.
No per-phase promotion adapter is added (reflect stays SoT for promotion).

### FR-6 — Per-phase base (D6)
Add `--base <ref>` (highest precedence). Resolution chain in `config.py`:
**explicit `--base` > frontmatter per-phase `start_commit` > `git merge-base
HEAD master`**. A phase-N gate passes `--base <phase-N-start-sha>` to audit ONLY
phase-N work. Preserve the F3 de-range: `--diff <BASE>` is a SINGLE ref vs the
working tree (start_commit-preferred), never a `<BASE>..HEAD` commit range.

### FR-7 — Depth passthrough (D7)
Keep `--depth standard|deep` (POST never runs quick → floored to standard).
Callers pass `--depth deep` (forces Tier 2). No `--max-turns` flag (Section-9
option set stays exact; `_DEFAULT_MAX_TURNS=250` covers a deep T2 run).

### FR-8 — Remediation-task-path contract field (enabling gap for FR-1)
Reflect's Wave 6 MUST emit `remediation_task_path: <abs path>|null` into
`return-contract.yaml` — the absolute path of the MDTM file `rf-task-builder`
wrote (null when no remediation authored). The wrapper reads this to auto-execute;
it never guesses "newest `TASK-RF-*` dir" (fragile under parallel sessions). This
is a small skill contract-field addition (a `1.3.0 → 1.4.0` minor bump), NOT
reflect-logic duplication.

### FR-9 — Headless `--remediate` auto-authoring
In wrapper (`claude --print`) mode there is no human to "accept" a Tier-3 offer.
`--remediate` under `--print` MUST author the corrective file non-interactively
(no accept prompt) and set `remediation_task_path`. When the deviation set is
HUMAN-REQUIRED, reflect still authors nothing auto-runnable (BUILD_REQUEST with
`needs_human_decision: true` prompts for human resolution) — the wrapper HALTs.

### FR-10 — Preserve all v1 fail-closed semantics
The 4-state verdict map (`blocked→degraded→halted→pass`, first-match-wins, only
PASS exits 0), atomic race-safe `reflect_post:` write-back (FR-6 v1),
always-write `wrapper-result.yaml` sidecar (FR-7 v1), `--tmux` fail-closed
sentinel inversion, `--dry-run`/`--print-command` no-launch path, `--resume`
clean-HEAD short-circuit, and the `.claude/{skills,agents,commands}` `--output`
STOP all remain unchanged.

## 3. Verdict → action table (the carve-out, mechanically)

| Contract signal (post-audit)                              | Verdict   | `--fix` action                          | Promote? |
|-----------------------------------------------------------|-----------|------------------------------------------|----------|
| `status: success` AND `tier_reached == expected`          | PASS      | none (converged)                         | O1: yes / O2: no |
| `drift>0` and/or `necessary` only; no reg/human/gaps      | HALTED    | auto-run `remediation_task_path`, re-verify | only after PASS |
| `regression_present: true` or `deviations.regression>0`   | HALTED    | **none — terminal HALT**                 | never |
| `needs_human_decision: true` (grounding-gaps non-empty)   | HALTED    | **none — terminal HALT**                 | never |
| `user_decision_required: true`                            | HALTED    | **none — terminal HALT**                 | never |
| `unauthorized_deviation_present: true`                    | HALTED    | **none — terminal HALT**                 | never |
| any degraded trigger (FR-11 v1)                           | DEGRADED  | **none — exit 11**                       | never |
| child crash / timeout / contract-missing / bad-version    | BLOCKED   | **none — exit 2**                        | never |

`remediation_task_path` absent on an AUTO-FIXABLE verdict ⇒ cannot repair ⇒
terminal HALT (exit 10). Exit codes unchanged from v1: pass 0 / halted 10 /
degraded 11 / blocked 2.

## 4. O1 vs O2 invocation (consumed by the generator worktree)

**O1 — whole tasklist (task-builder terminal gate):**
```
superclaude reflect run <tasklist.md> --depth deep --fix --promote
```
- `--base` omitted → resolves from frontmatter `start_commit` (whole-task base).
- promote-by-default; `task` adapter promotes `.dev/tasks/to-do/TASK-* → done/`.

**O2 — per-phase (sc:tasklist end-of-phase gate):**
```
superclaude reflect run <phase-N-file.md> --depth deep --fix --no-promote --base <phase-N-start-sha>
```
- `--base` pins phase-N scope (single ref vs working tree).
- `--no-promote` forced (no per-phase adapter).

Both inherit `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` honoring (FR-2): if a gate is
reached while the marker is `=1`, the wrapper self-suppresses (exit 0).

## 5. Required frontmatter the generators MUST persist

| Key                     | Site | Purpose |
|-------------------------|------|---------|
| `start_commit`          | O1   | whole-task base for `--diff` (existing key) |
| per-phase `start_commit`| O2   | phase-scoped base; surfaced to the gate as `--base <sha>` |
| `executor_model_class`  | both | anti-self-confirmation: reflect's `--executor-model` so reviewers differ from the executor (existing `config.py` consumption) |
| `reflect_post:`         | both | written back by the wrapper (existing) |

## 6. Non-functional requirements

- **NFR-1 Thinness** — see §0. Enforced by tests: no `cli.sprint`/`cli.roadmap`
  import, no `async`, only `ClaudeProcess` launch.
- **NFR-2 Bounded cost (D7)** — deep ≈ 35–70k tokens / 8–15 min PER audit; the
  fix loop multiplies by (iterations+1) audits + iterations `/task` runs. Bound:
  `(N+1)` audits, N≤2 default. Document the band in the contract.
- **NFR-3 Termination** — FR-2 + FR-3 jointly guarantee termination: the marker
  kills nested gates; `max-fix-iterations` kills a non-converging outer loop.
- **NFR-4 Idempotent re-verify** — re-running the audit after a `/task` apply
  uses the SAME `--base` (working-tree diff), so repaired work is re-scored
  against the same scope.
- **NFR-5 Land-before-generators** — the wrapper command must be registered in
  `main.py` and `pipx install --force`-able before the companion worktree's gate
  emission goes live, else generated tasklists break at "no such command".

## 7. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Infinite wrapper↔remediation recursion | FR-2 marker self-suppress (primary) + generator emission-skip (belt) |
| Auto-applying a human-decision change | FR-4 carve-out: regression/needs_human/user_decision/gaps → terminal HALT |
| Non-converging fix loop burns tokens forever | FR-3 `--max-fix-iterations` (default 2) → HALT |
| Wrapper can't find authored remediation file | FR-8 `remediation_task_path` contract field (no dir-guessing) |
| O2 promotes with no adapter → silent skip or wrong dir | FR-5 O2 forces `--no-promote` |
| Phase-N gate audits whole-task scope | FR-6 `--base <phase-N-start-sha>` |
| Generators re-derive the contract and drift | single authoritative `.dev/handoffs/reflect-wrapper-contract.md` |

## 8. Acceptance criteria

1. `superclaude reflect run` self-suppresses (exit 0) when
   `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`.
2. AUTO-FIXABLE (drift-only) verdict with a present `remediation_task_path`
   triggers an auto-run `/task` and a re-audit; convergence → exit 0.
3. `regression_present`/`needs_human_decision`/`user_decision_required`/non-empty
   grounding-gaps → terminal HALT (exit 10), no `/task`, no promote.
4. Non-convergence after `--max-fix-iterations` → exit 10, `fix_converged: false`
   in sidecar.
5. O1 `--promote` promotes via the `task` adapter; O2 with `--no-promote` exits 0
   verified-not-promoted.
6. `--base <ref>` overrides frontmatter `start_commit`; `--diff` stays a single
   ref vs working tree.
7. Reflect emits `remediation_task_path` (contract `1.4.0`); wrapper reads it.
8. No `cli.sprint`/`cli.roadmap` import; no `async`; only `ClaudeProcess` launch
   (thinness tests green). `pipx install --force` exposes `superclaude reflect run`.
9. All v1 fail-closed tests remain green (FR-10).

## 9. Implementation surface (for the tasklist)

- `cli/reflect/commands.py` — add `--fix/--no-fix`, `--max-fix-iterations`,
  `--base`; flip `--promote` default to True; add the FR-2 marker self-suppress
  guard at command entry; thread new flags to `resolve_config`.
- `cli/reflect/config.py` — `_resolve_base` precedence `--base > start_commit >
  merge-base`; add `fix`, `max_fix_iterations`, `base_override` to `ReflectConfig`.
- `cli/reflect/runner.py` — the fix-loop orchestration (audit → classify →
  apply `/task` → re-verify), export marker into child env, read
  `remediation_task_path`, record `fix_iterations`/`fix_converged` in sidecar.
- `cli/reflect/contract.py` — surface `remediation_task_path`; add the
  AUTO-FIXABLE vs HUMAN-REQUIRED classifier (pure, off existing fields).
- `cli/reflect/models.py` — `ReflectConfig`/`ReflectResult` new fields.
- `sc-reflect-protocol` — FR-8/FR-9: emit `remediation_task_path`, headless
  `--remediate` auto-authoring; contract `1.3.0 → 1.4.0`.
- `tests/cli/reflect/` — marker suppression, carve-out routing, bounded loop,
  O1/O2 promote scope, `--base` precedence, thinness guards.
