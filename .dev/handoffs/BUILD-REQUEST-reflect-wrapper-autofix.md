# BUILD_REQUEST — reflect-wrapper AUTO-FIX evolution

GOAL: Evolve the shipped audit-only `superclaude reflect run` wrapper into a
wrapper-orchestrated **validate → review → auto-fix → verify → promote** engine
serving two gate sites (O1 whole-tasklist terminal gate; O2 sc:tasklist
per-phase gate), implementing decisions D1–D7 from
`.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md`.
The wrapper MUST stay THIN (reflect remains SoT for waves/tiers/taxonomy/
promotion mechanics) and MUST be mergeable + `pipx install --force`-able so it
lands BEFORE the companion worktree's gate emission goes live.

WHY: `/sc:reflect` spawned as an Agent/Task subagent silently loses Tier-2
heterogeneous-model fan-out (memory `reference_subagent_cannot_nest_skill_fanout`);
the wrapper launches reflect as a TOP-LEVEL `claude --print` subprocess so Tier-2
fans out. The audit-only v1 only HALTs on deviations; this evolution adds a
bounded, safe-class-gated auto-fix loop + promote-by-default so a clean or
mechanically-repairable tasklist completes with zero human intervention, while
anything a human must decide still HALTs (honoring
`feedback_human_decision_items_must_halt`). The companion worktree
(`ReflectInTaskLists`) CONSUMES the contract at
`.dev/handoffs/reflect-wrapper-contract.md` — this build must satisfy that
contract exactly.

CANONICAL BASE (critical): The work lands on the AUDIT-ONLY reflect CLI as it
exists in worktree `wrapper-onto-master` (built on current `origin/master`:
`src/superclaude/cli/reflect/{commands,config,runner,contract,models}.py` +
`src/superclaude/cli/main.py` reflect registration + `tests/cli/reflect/`).
The `--reflect <none|0|1|2|auto>` DIAL (this branch's commits ecadfe47/879bb64f;
PR #157) is ABANDONED — do NOT build on it, extend it, or reference it. Create a
fresh feature branch off `origin/master` (mirroring wrapper-onto-master), not off
this `reflectWrapper` dial branch.

WHERE:
- `src/superclaude/cli/reflect/commands.py` — add `--fix/--no-fix`,
  `--max-fix-iterations` (default 2), `--base`; flip `--promote` default to True;
  add the recursion-breaker `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` self-suppress
  guard at command entry; thread new flags to `resolve_config`.
- `src/superclaude/cli/reflect/config.py` — `_resolve_base` precedence
  `--base > frontmatter start_commit > git merge-base HEAD master`; new
  `ReflectConfig` fields.
- `src/superclaude/cli/reflect/runner.py` — the fix-loop orchestration
  (audit → classify → auto-run `/task <remediation_task_path>` as a top-level
  `ClaudeProcess` with the marker exported → re-verify), record
  `fix_iterations`/`fix_converged` in the sidecar.
- `src/superclaude/cli/reflect/contract.py` — surface `remediation_task_path`;
  add the pure AUTO-FIXABLE vs HUMAN-REQUIRED classifier off EXISTING contract
  fields (no new taxonomy logic).
- `src/superclaude/cli/reflect/models.py` — new `ReflectConfig`/`ReflectResult`
  fields.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (+ relevant refs) — emit
  `remediation_task_path: <abs>|null` in `return-contract.yaml`; headless
  `--remediate` under `--print` auto-authors the corrective file without an
  interactive accept; bump `contract_version 1.3.0 → 1.4.0`.
- `tests/cli/reflect/` — marker self-suppression; carve-out routing
  (drift-only→auto-fix vs regression/needs_human_decision/user_decision/
  grounding-gaps→terminal HALT); bounded loop non-convergence→exit10; O1 promote
  vs O2 `--no-promote` scope; `--base` precedence; thinness guards (no
  cli.sprint/cli.roadmap import, no async, only ClaudeProcess launch).

ACCEPTANCE CRITERIA: the nine criteria in merged-requirements §8 (verbatim).
Conformance to `.dev/handoffs/reflect-wrapper-contract.md` §§2–6 is mandatory.

NON-GOALS / THINNESS BOUNDARY: Do NOT duplicate reflect wave/tier/taxonomy/
promotion logic in Python. Do NOT add a per-phase promotion adapter. Do NOT
re-introduce the `--reflect` dial. No imports from `cli.sprint`/`cli.roadmap`;
zero `async`; only `ClaudeProcess` as the launch path.

SPEC: .dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md

TASK_ID_PREFIX: TASK-RF

TEMPLATE: 02
  # Complex: discovery (confirm canonical base + contract delta) → CLI/config/
  # runner/contract/models build → reflect-skill contract-field addition → tests
  # → verification. Multi-file, cross-package (CLI + skill).

QA_GATE_REQUIREMENTS: PER_PHASE
  # Fail-closed verdict logic + recursion termination + human-decision carve-out
  # are safety-critical; each build phase needs an rf-qa / rf-qa-qualitative gate.

BOOTSTRAP EXEMPTION (POST reflect gate): This tasklist BUILDS `superclaude
reflect run`; it MUST NOT end with a `superclaude reflect run` terminal gate
(the command does not exist until this tasklist completes — a "superclaude: no
such command" failure). Build with `--reflect 1` (inline same-session audit-only
`/sc:reflect --mode post`, CLI-independent) or `--reflect none`. After the
wrapper is merged + `pipx install --force`-ed, a full Tier-2
`superclaude reflect run` audit of the completed work can be run manually.
