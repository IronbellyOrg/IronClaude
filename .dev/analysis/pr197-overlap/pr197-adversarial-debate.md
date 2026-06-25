# PR #197 vs ReflectHardening-3 Adversarial Debate

Generated: 2026-06-20

## Question

How much of PR #197 lives purely in the inference/protocol layer versus the CLI/programmatic layer, and how much of its inference-only work should be forked as an optional fallback if the user or situation does not want the CLI portion of `sc:reflect`?

## Verdict

PR #197 is mostly inference/protocol and RF skill workflow work, with a small but important CLI/programmatic touch. It should not be merged as a drop-in replacement for ReflectHardening-3. The strongest synthesis is:

1. Keep ReflectHardening-3's CLI/programmatic ensemble as canonical for headless/CI/post-task automation.
2. Fork a PR197-derived inference-only fallback mode for in-session skill execution when subprocess CLI is unavailable or intentionally undesired.
3. Port PR197's artifact-level EV hardening into both paths after resolving contract/version semantics.

## Layer Classification

| Layer | Approx share by changed-file intent | PR197 examples | Keep / fork guidance |
|---|---:|---|---|
| Pure CLI/programmatic | ~5-10% | `src/superclaude/cli/reflect/runner.py` prompt directive | Do not import as-is; local Tier-2 production path bypasses `_build_prompt()` and the directive contains banned `subagent` wording. |
| Mixed skill-to-CLI contract | ~10-15% | `task-builder/SKILL.md` `--cli` mode split; POST reflect generation contract | Needs human/product decision. Recommended: keep CLI canonical; make skill-only fallback explicit and non-default. |
| Reflect inference/protocol | ~15-20% | instance-level independence; no-formation-context briefs; EV-1/EV-2; reviewer-card naming; contract `1.5.1` | Port selectively. EV and no-formation-context are useful; contract shell and class-diversity semantics need decision. |
| RF/doc skill workflow | ~55-65% | `/task` lens QA; `tech-reference`, `tech-research`; new `operational-guide`, `readme`, `roadmap` skills | Mostly separate feature stream; depends on task-builder/task execution contract. |
| Tool-surface config | ~5% | RF Tavily tool id rename | Decide separately by validating target MCP tool names. |

Percentages are approximate because PR197 is heavily skewed by large Markdown skill additions; by line count, new/rewritten RF/doc skills dominate, while direct Python CLI code is tiny.

## Dedicated `sc:reflect` Work Analysis

This is the core overlap area. Treat PR197 as **three different `sc:reflect` contributions**, not one:

1. a runner-level prompt directive,
2. an inference/protocol semantic redesign,
3. an optional skill-only POST reflect mode.

### 1. Runner-level prompt directive

PR197 adds a directive to `_build_prompt()` telling the headless `claude --print` child to execute inline and avoid delegating to a worker subagent. The added text explicitly says the run must be top-level and that delegated/nested runs can degrade because reviewer callbacks route to the top-level coordinator (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:349`).

For this branch, that patch is not the right canonical `sc:reflect` fix. Current ReflectHardening-3 production Tier-2 uses a programmatic branch: when `expected_tier == 2` and `ClaudeProcess` is production, `runner.py` calls `run_tier2_ensemble(config)` and does **not** pass the `/sc:reflect` slash-command prompt into proxy workers (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:421`). The old prompt path remains for Tier-1 / non-production `ClaudeProcess` cases (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:427`).

Therefore:

- **Relevant to CLI/programmatic work?** Yes, but mostly as historical failure evidence, not as a patch to accept.
- **Inference-only fallback value?** Medium. The instruction captures the failure mode a skill-only fallback must avoid.
- **Merge recommendation:** Do not merge into `runner.py` as-is. Re-express as fallback-mode protocol language or tests, avoiding banned `subagent` source tokens.

### 2. `sc:reflect` anti-self-confirmation semantics

PR197 changes the protocol from executor-class exclusion to instance-level independence. It accepts `--executor-model` but records/ignores it; it says reflect does not class-exclude and emits no `executor_exclusion_degraded` signal (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:6887`). Its argument is that self-confirmation is about same instance plus same formation context, not about the same model class; therefore fresh reviewer subagents, no formation context, and blind calibration are sufficient (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:6896`). It also states class diversity is a preference that never drops slots or degrades a tier (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:6906`).

This is a genuine semantic alternative to the local protocol, not a small merge hunk. The overlap matrix marks it as M-056: PR197's instance-level independence conflicts with the local executor-class exclusion rule and needs a human decision, not mechanical merge (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197-overlap-matrix.md:36`).

Therefore:

- **Relevant to CLI/programmatic work?** Yes, because it changes how the programmatic ensemble should decide pass/degrade/fallback.
- **Inference-only fallback value?** High. This is the strongest PR197 idea for a skill-only or degraded-model environment.
- **Merge recommendation:** Implement, if desired, as an explicit mode/decision: `class_exclusion` vs `instance_independence`, with tests/evals/telemetry updated atomically.

### 3. `sc:reflect` EV-1 / EV-2 artifact hardening

PR197 adds EV-1: Wave 4 is not complete until the orchestrator verifies on disk that adversarial merge artifacts exist, or verifies a loud fallback path. It explicitly checks `merged-verdict.yaml`, reviewer cards, fallback audit rows, and bounded remediation (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:6932`). PR197 also adds EV-2: `merge_method` legal values are exactly `{adversarial, single-reviewer-fallback}` and synthetic inline merge values are malformed (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:6954`).

This is not tied to the CLI-versus-skill launch mechanism. It strengthens both. The matrix already classifies EV-1/EV-2 as M-057: a partial overlap that should be merged as a new shared item, with the current worktree owning the contract/version shell and PR197 owning the EV concept if ported (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197-overlap-matrix.md:37`).

Therefore:

- **Relevant to CLI/programmatic work?** Yes, directly; the programmatic ensemble should verify artifacts too.
- **Inference-only fallback value?** High; skill-only fallback needs artifact proof even more because it has less external process isolation.
- **Merge recommendation:** Port EV-1/EV-2 after contract version is settled. Do not import PR197's `1.5.1` contract shell wholesale.

### 4. `sc:reflect` contract/version collision

PR197 changes the stable contract heading from `1.5.0` to `1.5.1` and describes it as a patch with no stable-field changes (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:6940`). Local work has already moved the skill protocol to `1.6.0` with runtime-surface fields, and the matrix flags PR197 as a fourth claimant in the existing M-028/M-042 contract collision (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197-overlap-matrix.md:34`).

Therefore:

- **Relevant to CLI/programmatic work?** Yes, because consumers parse the return contract.
- **Inference-only fallback value?** Low as written; the version shell is stale relative to local `1.6.x` work.
- **Merge recommendation:** Do not take PR197's contract version text. Translate any accepted semantics into the chosen local `1.6.x` line.

### 5. `task-builder` POST `sc:reflect` mode split

PR197 introduces `--cli` as an optional flag and makes skill-only / in-session POST reflect the default; CLI mode emits the flat `superclaude reflect run` wrapper only when requested (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197.diff:7139`). In contrast, current local task-builder requires that when `POST_REFLECT_GATE: ENABLED`, the generated task includes a flat wrapper shell-out: `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`, and considers legacy self-run reflect-subagent or human-handoff forms malformed (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/task-builder/SKILL.md:2322`).

This is the clearest product decision:

- Current branch says: **CLI wrapper is canonical; skill-only is not the default.**
- PR197 says: **Skill-only is canonical; CLI wrapper is opt-in via `--cli`.**

The matrix marks this as M-060 and recommends resolving it first (`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/analysis/pr197-overlap/pr197-overlap-matrix.md:40`).

Recommended compromise:

- Keep current CLI wrapper as default for generated tasklists.
- Add PR197-style skill-only POST reflect as an explicit fallback, e.g. `reflect_post_mode: skill`, but do **not** make it default.
- Require clear degraded/fallback reporting when skill-only mode is used, because it lacks the same process boundary as the CLI wrapper.

### `sc:reflect`-specific decision matrix

| PR197 `sc:reflect` item | Canonical CLI path? | Optional inference fallback? | Recommendation |
|---|---:|---:|---|
| Runner inline prompt directive | No | Partial | Preserve the failure-mode rationale; do not merge into `runner.py` as-is. |
| Skill-only POST reflect mode | No, not default | Yes | Add as explicit fallback after M-060 decision. |
| Instance-level independence | Not until decided | Yes | Treat as explicit semantic mode or human decision. |
| No-formation-context reviewer briefs | Yes | Yes | Port, preserving local rich grounding hunks. |
| EV-1 on-disk adversarial verification | Yes | Yes | Port after contract/version decision. |
| EV-2 legal `merge_method` values | Yes | Yes | Port after contract/version decision. |
| PR197 `1.5.1` contract shell | No | No | Rewrite into local `1.6.x`; do not import wholesale. |
| Reviewer-card filename shape | Unknown | Unknown | Decide based on real producer artifacts before EV implementation. |

## Debate Positions

### Advocate A: ReflectHardening-3 CLI/programmatic approach

Strengths:

- More deterministic and testable: Tier-2 orchestration is in programmatic code (`run_tier2_ensemble`) rather than relying on a prompt directive to make the headless agent behave.
- Better for CI/headless operation: exit codes, contract parsing, wrapper write-back, and transport knobs are explicit.
- Maintains a hard no-nesting invariant: no `Task(`/`subagent` surface in reflect wrapper Python.
- Aligns with current task-builder contract: POST reflect gate is a flat `superclaude reflect run ... --depth deep --fix --promote` shell-out.

Weaknesses:

- Heavier implementation surface: transport, swarm lens, reducer, return-contract, and tests must stay aligned.
- Less flexible when subprocess CLI is not available or when the user wants everything in-session.
- Current executor-class exclusion rule may be too strict in constrained model environments.

### Advocate B: PR197 inference-layer approach

Strengths:

- Offers a viable skill-only fallback model: no subprocess wrapper required, useful when CLI/headless execution is undesirable.
- Strong conceptual frame for anti-self-confirmation: same instance/context is the real risk; fresh reviewer instances plus stripped formation context may be sufficient.
- EV-1/EV-2 artifact checks are valuable regardless of launch mechanism: they verify that adversarial merge artifacts actually exist and `merge_method` is legal.
- The broader RF/doc skill work makes task execution more rigorous through lens-based QA and source-fidelity gates.

Weaknesses:

- The runner prompt fix is stale in this branch because local production Tier-2 does not use that prompt path.
- It contains `subagent` wording that directly conflicts with this branch's no-nesting guard.
- It reverses the local task-builder POST reflect default: CLI becomes opt-in rather than canonical.
- Its `1.5.1` contract text conflicts with the local `1.6.0` runtime-surface contract and the existing unresolved M-028/M-042 collision.

## Complementary Merge Strategy

### Keep canonical in ReflectHardening-3

- CLI/programmatic Tier-2 ensemble route.
- Flat POST reflect wrapper as the default generated task gate.
- No-nesting guard over reflect wrapper Python.
- Local `1.6.x` contract shell and runtime-surface fields, pending M-028/M-042 resolution.

### Fork from PR197 as optional inference fallback

- A `reflect_post_mode: skill` or equivalent explicit fallback, not the default.
- Instance-level independence as an alternate semantic mode when model-class diversity is scarce.
- No-formation-context reviewer brief invariant, interpreted as “same three sections, rich grounding hunks preserved.”
- EV-1/EV-2 on-disk adversarial merge verification, ported into local `1.6.x` wording.
- Lens-based `/task` QA as opt-in/full-intensity execution, after task-builder defaults are resolved.

## Recommended Decision Order

1. Decide POST reflect default: keep CLI canonical and add skill-only fallback, or accept PR197's `--cli` split.
2. Resolve the contract/version collision: PR197 `1.5.1` vs local `1.6.0` plus M-028/M-042.
3. Decide anti-self-confirmation semantics: executor-class exclusion vs instance-level independence.
4. Port EV-1/EV-2 and no-formation-context brief invariant.
5. Split RF/doc skill expansion into a separate PR after task-builder/task semantics are stable.

## Bottom Line

PR197 is best treated as an inference-layer fallback and protocol-hardening source, not a replacement for the current CLI/programmatic ReflectHardening work. The CLI path is the stronger default for automation and verification. The PR197 path is valuable as a user-facing/in-session option when the CLI wrapper is too heavy, unavailable, or intentionally not desired.
