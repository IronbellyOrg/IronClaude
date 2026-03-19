# Diff Analysis: Resume Pipeline Fix Comparison

## Metadata
- Generated: 2026-03-18T00:00:00Z
- Variants compared: 3
- Total differences found: 30
- Categories: structural (5), content (9), contradictions (5), unique (6), shared assumptions (5)

---

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Document organization | Bug-centric (Bug 1-4 as top-level sections) | Phase-centric (Problem, Root Cause, Fix Design, Interaction, Test, Migration) | Philosophy-centric (Problem, Philosophy, Fixes, Depth, Defense Layers, Click, Tests) | Medium |
| S-002 | Heading depth | Max H3 (3 levels) | Max H4 (4 levels: Fix 3 → 3.1, 3.2) | Max H3 (3 levels) | Low |
| S-003 | Code block density | ~8 code blocks (heavy implementation detail) | ~6 code blocks (moderate, more pseudocode) | ~6 code blocks (moderate, mixes guard logic with narrative) | Low |
| S-004 | Test plan placement | Per-bug inline tests (Tests 1-6 immediately after each fix) | Separate section (§6: Test Plan with Unit/Integration/Edge subsections) | Separate section (§8: table-only, no code) | Medium |
| S-005 | Risk/Compatibility section | Dedicated Risk Assessment table + Backward Compatibility section | Dedicated §7: Migration / Backward Compatibility (3 subsections) | No dedicated section; compatibility notes scattered inline | Medium |

---

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|--------------------|--------------------|--------------------|----------|
| C-001 | Click default detection mechanism | `ctx.get_parameter_source("agents")` — detects COMMANDLINE vs DEFAULT at Click API level | Change Click defaults to `None`, resolve later — eliminates the default entirely | Guard comparison: compares config agents against hardcoded Click default list | High |
| C-002 | Agent restoration strategy | Silent restore from state file with logging | Silent restore from state file with warning on missing state | Guard/abort: refuses to proceed on mismatch, requires user to pass `--agents` explicitly | High |
| C-003 | Resume cascade fix (Bug 3) | Dependency-aware: `dirty_outputs` set tracks regenerated files; per-step gate checking with input-overlap detection | Dependency-aware: `_step_needs_rerun()` helper with `dirty_outputs` set; identical algorithm, different factoring | Keeps `found_failure` cascade; argues cascade is architecturally correct for linear pipeline; adds logging only | High |
| C-004 | State file protection (Bug 4) | Defense-in-depth: if no generate steps passed, preserve existing agents from state | Defense-in-depth: "merge, don't replace" — preserve agents/depth if partial run | Conditional writes: refuses to write state if (a) no steps passed OR (b) agent mismatch with existing state | Medium |
| C-005 | `--depth` restoration | Not addressed | Explicitly addressed: same `None`-default pattern as `--agents`; audit table of all CLI options | Explicitly addressed: auto-restore with WARNING; argues depth is safe to auto-restore unlike agents | Medium |
| C-006 | `_apply_resume` refactor scope | Full rewrite: new function body with `regenerated_outputs` set | Full rewrite: new function body with `dirty_outputs` set + `_step_needs_rerun()` extraction | Minimal change: keeps `found_failure`, adds `_gate_check_step()` helper for state-driven paths, adds cascade logging | Medium |
| C-007 | `_save_state` protection granularity | Checks `generate_ran` boolean to decide whether to preserve existing agents | Notes Fix 1 makes this moot; provides defense-in-depth with resolved agents | Two guards: (1) no-progress → no write, (2) agent-mismatch → no write; refuses write entirely | Medium |
| C-008 | Test plan specificity | 6 tests with full pytest code blocks | 8 unit tests + 4 integration tests + 5 edge cases as tables | 9 test descriptions in table form, no code | Medium |
| C-009 | Implementation order rationale | Bug 1 → Bug 4 → Bug 3 → Bug 2; orders by root cause → defense → efficiency → diagnostics | Fix 1 → Fix 4 → Fix 3 → Fix 2; same order with interaction analysis (§5) showing why order matters | 3.1 → 3.4 → 3.2 → 4.2 → 3.3; agent guard → conditional writes → state paths → depth → logging | Low |

---

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|----|
| X-001 | Should agents be silently restored or should the system abort? | Silent restore: `_restore_agents_from_state()` transparently replaces `config.agents` | Silent restore: state file values override `None` config fields transparently | **Abort with error**: user must explicitly pass `--agents` on resume; silent restore hides intent | High |
| X-002 | Should `found_failure` cascade be eliminated? | Yes — replace with dependency-tracking `regenerated_outputs` set | Yes — replace with `_step_needs_rerun()` + `dirty_outputs` | **No** — cascade is architecturally correct for linear pipelines; just add logging | High |
| X-003 | Should `_save_state` ever be skipped entirely? | No — always writes, but preserves existing agents when no generate ran | No — always writes with defense-in-depth on agents/depth | **Yes** — refuses to write state if no steps passed or agent mismatch detected | Medium |
| X-004 | Should `--depth` be treated identically to `--agents`? | Not addressed (implicit: depth is not special) | Yes — same `None`-default pattern, same restore logic | **No** — depth can be safely auto-restored (single-step impact), unlike agents (structural impact) | Medium |
| X-005 | Is `ctx.get_parameter_source()` sufficient or should defaults be changed to `None`? | Sufficient — use `get_parameter_source("agents")` to detect DEFAULT vs COMMANDLINE | **Neither sufficient** — change Click defaults to `None` to make omission detectable at value level | Notes `get_parameter_source()` is more robust than hardcoded comparison, but uses guard approach instead | Medium |

---

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|------------------|
| U-001 | B | **Full CLI option audit table** (§4): Systematically reviews all `--` options (`--output`, `--model`, `--max-turns`, `--retrospective`) for the same default-substitution bug class, with risk ratings | High |
| U-002 | B | **Fix interaction matrix** (§5): Explicitly analyzes what happens when each fix is applied in isolation, showing partial-state risks | High |
| U-003 | B | **Schema version / migration analysis** (§7): Explicitly confirms no schema_version bump needed and explains why | Medium |
| U-004 | C | **"Guards over restores" design philosophy** (§2): Articulates a principled distinction between silently fixing state vs. refusing to proceed with inconsistent state | High |
| U-005 | C | **State-driven path resolution** (§3.2): Uses `state_paths[step_id]` lookup for gate checks, making resume independent of current `config.agents` entirely | High |
| U-006 | C | **Layered defense summary** (§5): Explicit 5-layer defense-in-depth diagram showing how each fix provides a failsafe for the others | Medium |

---

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|------------|----------------|----------|
| A-001 | All variants: `_build_steps` must run after agents are resolved | The pipeline's step list is built exactly once per `execute_roadmap()` invocation and is never rebuilt after state restoration | UNSTATED | Yes |
| A-002 | All variants: `Step.inputs` used for dependency tracking | Each `Step` object has an `inputs` field containing `Path` objects that are correct and complete for dependency analysis | UNSTATED | Yes |
| A-003 | All variants assume `read_state()` returns well-formed data or `None` | `read_state()` never returns partial/corrupt data — it either returns a valid dict or `None`; there is no partial-parse failure mode | UNSTATED | Yes |
| A-004 | All variants: state file is single-writer | No two concurrent `superclaude roadmap run` processes write to the same `.roadmap-state.json` simultaneously | STATED (Variant A mentions race condition as out-of-scope risk) | No |
| A-005 | All variants: `AgentSpec.__eq__` works correctly | Dataclass equality comparison between `AgentSpec` objects is reliable for detecting agent changes | STATED (Variant A notes "works via dataclass default") | No |

**Promoted to [SHARED-ASSUMPTION] diff points:**

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-001 | `_build_steps` is called exactly once and never rebuilt | If `_build_steps` is called before state restoration (current bug) or if a future refactor calls it again after, the pipeline uses stale step definitions | ACTIVE |
| A-002 | `Step.inputs` is always a correct, complete list of `Path` objects | If `Step.inputs` is `None` or incomplete, dependency tracking in Variants A and B silently skips the check, allowing stale outputs to persist | ACTIVE |
| A-003 | `read_state()` is atomic: valid dict or `None` | If `read_state()` returns a dict with missing keys (e.g., `"agents"` key absent in old state files), all three variants have different fallback behavior, but none handle a dict with structurally invalid values (e.g., `"agents": "not a list"`) | ACTIVE |

---

## Summary
- Total structural differences: 5
- Total content differences: 9
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: X-001, X-002, C-001, C-002, C-003
