# Brainstorm brief — reflect-wrapper AUTO-FIX evolution (decisions 1–7)

> Supersedes `reflect-cli-wrapper-brainstorm-brief.md` (audit-only v1). This brief
> evolves the SHIPPED audit-only wrapper into a **wrapper-orchestrated
> audit → auto-fix → verify → promote** engine that serves TWO gate sites
> (O1 whole-tasklist + O2 per-phase). The 7 decisions below are **MADE** (a
> `/sc:reflect --mode pre` flagged them load-bearing). Do NOT re-litigate —
> consolidate into `merged-requirements.md`, `--handoff none`.

## Canonical base (NOT the dial)

- **Adopt:** the audit-only reflect CLI in worktree `…/wrapper-onto-master`
  (`src/superclaude/cli/reflect/{commands,config,runner,contract,models}.py` +
  `main.py` registration + `tests/cli/reflect/`). It is the F3-de-ranged,
  CLI-registered, fail-closed POST gate on current `origin/master`.
- **Abandon:** the `--reflect <none|0|1|2|auto>` dial (this branch's commits
  `ecadfe47`, `879bb64f`; PR #157 closed). The 8-value oracle / TB-Add-9 /
  V1–V16 / 304-line test are OUT OF SCOPE and must not be carried forward.

## What the base already does (do not re-spec)

`superclaude reflect run <tasklist>` → resolves base/head/depth/spec/executor →
launches `/sc:reflect --mode post --no-promote --diff <BASE> --tasklist … --depth …`
as a **top-level `claude --print` subprocess** (so Tier-2 heterogeneous fan-out
works — the whole reason the wrapper exists; memory
`reference_subagent_cannot_nest_skill_fanout`) → parses `return-contract.yaml` →
derives a fail-closed 4-state verdict (`blocked→degraded→halted→pass`,
first-match-wins; only PASS exits 0) → atomic race-safe `reflect_post:`
frontmatter write-back + `wrapper-result.yaml` sidecar. `--diff <BASE>` is a
SINGLE ref vs working tree (F3 de-range, #153). Reflect stays read-only SoT;
the wrapper never duplicates wave/tier/taxonomy logic.

## Grounded facts the design MUST respect

- **Reflect never auto-executes remediation.** `--remediate` only *authors* a
  Tier-3 corrective MDTM file via `rf-task-builder` (BUILD_REQUEST in
  `refs/remediation-handoff.md`); "Will Not: Auto-execute a Tier 3 remediation
  task — task-builder produces a file, the user runs `/task <path>`"
  (`sc-reflect-protocol/SKILL.md` §Will-Not). → the WRAPPER owns the fix layer.
- **Contract v1.3.0 fields** (`SKILL.md` §9.1): `status`, `tier_reached`,
  `deviation_count_by_class{authorized,necessary,drift,regression}`,
  `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`
  (true iff `grounding-gaps.yaml` non-empty → `status: partial`),
  `user_decision_required`, `remediation_offered`, `remediation_accepted`,
  `grounding_gaps_path`, `deviation_register_path`, `report_path`.
  **GAP:** there is NO `remediation_task_path` — the wrapper cannot locate the
  authored file to auto-run it. Closing this gap is a contract-field addition
  (reflect emits the absolute path of the file `rf-task-builder` wrote).
- **Promotion adapters = exactly two** (`refs/promotion-adapters.md`):
  `task` (`.dev/tasks/to-do/TASK-*` → `done/`) and `sprint-release`
  (`.dev/releases/current/` → `complete/`). **No per-phase adapter.**
- `needs_human_decision is True` → already `HALTED` in `contract.py` (so the
  grounding-gaps carve-out is partly free). `regression`, `drift>0`,
  `unauthorized_deviation`, `user_decision_required` → already `HALTED`.

## The 7 decisions (MADE — resolutions to encode)

**D1 — Wrapper-orchestrated auto-fix loop around audit-only reflect.**
New `--fix/--no-fix` (default `--fix` for the gate). Loop body:
(a) run reflect audit with `--remediate`; (b) derive verdict; (c) PASS → done;
(d) verdict is a HUMAN-REQUIRED class (D4) → terminal HALT; (e) verdict is an
AUTO-FIXABLE class AND `remediation_task_path` present → `claude --print
"/task <remediation_task_path>"` as a top-level subprocess (marker set, D2) →
loop to (a) to RE-VERIFY. Reflect stays read-only; the wrapper executes the fix.

**D2 — Recursion-breaker (CONTRACT POINT).** Marker env
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`. The wrapper exports it for the entire
auto-fix subtree (its reflect child + every auto-run `/task`). **Primary breaker
lives in the wrapper itself:** `superclaude reflect run` checks the marker at
startup — if `=1`, it immediately no-ops `exit 0` ("nested gate suppressed").
The remediation tasklist (built by task-builder, which per O1 carries its own
terminal gate) therefore self-suppresses when the wrapper auto-runs it. The
outer wrapper owns the real re-verification. Generators MUST NOT clear the
marker and SHOULD also skip gate *emission* when it is set (belt-and-suspenders).

**D3 — Bounded fix-loop.** `--max-fix-iterations N` (default **2**). After N
apply→verify cycles without convergence to PASS → terminal HALT (exit 10),
do NOT promote, surface the last report + sidecar to the operator.

**D4 — Auto-fix safe-class carve-out** (reconciles "auto-fix by default" with
`feedback_human_decision_items_must_halt`). Auto-run remediation ONLY for
mechanically-unambiguous deviations:
- AUTO-FIXABLE: HALTED caused solely by `drift>0` and/or `necessary` doc-class
  items, with NO regression, NO `needs_human_decision`, NO `user_decision_required`,
  empty grounding-gaps.
- HUMAN-REQUIRED (terminal HALT, never auto-promoted): `regression_present`,
  `needs_human_decision`, `user_decision_required`, non-empty grounding-gaps,
  any `degraded`/`blocked` verdict.
The wrapper reads these straight off the contract — no new classification logic.

**D5 — Promote default flip + scope.** `--promote/--no-promote` default flips to
`--promote`. BUT there is no per-phase adapter, so:
- **O1 (whole tasklist):** promote-by-default; the `task` adapter applies
  (`.dev/tasks/to-do/TASK-*`).
- **O2 (per-phase):** the wrapper FORCES `--no-promote` (no adapter exists;
  adding one would thicken the wrapper). Per-phase gates auto-fix-and-verify but
  do NOT promote. Promotion happens once at tasklist/release level.
Do NOT add a per-phase promotion adapter (keeps the wrapper thin; reflect SoT).

**D6 — Per-phase base (O2).** Add `--base <ref>` to the wrapper (highest
precedence). Resolution chain: explicit `--base` > frontmatter per-phase
`start_commit` > `git merge-base HEAD master`. A phase-N gate passes
`--base <phase-N-start-sha>` so it audits ONLY phase-N work. Keep the F3
de-range (single ref vs working tree; start_commit-preferred).

**D7 — Depth.** Keep `--depth standard|deep`; callers pass `--depth deep`
(forces Tier 2). Cost band to confirm in the contract: deep ≈ 35–70k tokens /
8–15 min PER gate; O1+O2 ⇒ this runs per phase AND per tasklist. Operator chose
deep-everywhere deliberately.

## Thinness guardrails (carry from v1)

No imports from `cli.sprint`/`cli.roadmap`; zero `async`; the only launch path
is `ClaudeProcess` (never an Agent/Task surface); reflect logic (waves, tiers,
taxonomy, promotion mechanics) stays in the skill. New wrapper surface is ONLY:
the fix-loop orchestration, the marker check, `--base`, the promote-default flip,
and reading `remediation_task_path`.

## Desired output

`merged-requirements.md` — unified spec: problem, FRs/NFRs, the
audit→fix→verify→promote state machine, the safe-class verdict→action table,
the recursion-breaker contract, O1 vs O2 invocation + promotion scope, the
`remediation_task_path` contract-field gap, thinness boundaries. Stop at merged
requirements (`--handoff none`).
