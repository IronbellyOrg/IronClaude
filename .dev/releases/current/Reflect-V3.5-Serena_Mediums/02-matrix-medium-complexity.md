# sc:reflect V3 — Serena Feature Adoption Matrix #2

**Scope:** Medium implementation cost / complexity items with **High** value to the sc:reflect protocol's objectives (UC-1 coverage audit, UC-2 deviation classification, tiered review ensemble, adversarial merge, evidence-validator gate, per-project deviation memory).

**Posture:** sc:reflect is read-only **with respect to project source code** — it does not mutate code. It DOES write logs, audit trails, reflection cards, reviewer briefs, reports, and may run tests/linters/build commands as verification activity. This boundary is the filter applied to every row — and is the reason `execute_shell_command` qualifies for inclusion rather than being out-of-scope.

**Source ranking:** Implementation cost is rated relative to wiring effort inside `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `refs/*.md`. Medium-cost items typically involve a new conditional code path, a flag gate, a safety envelope, or schema additions to the reflection card / return contract.

---

## Matrix

| # | Name | Description | Implementation Cost / Complexity | Value to sc:reflect |
|---|---|---|---|---|
| 1 | **`type_hierarchy`** | Transitive supertypes/subtypes for a type. JetBrains-strong; LSP partial coverage. | **Medium.** Conditional wiring: detect JetBrains availability via `get_current_config`; degrade gracefully on pure LSP. Schema change in `reflection-card` to carry hierarchy slice. New `--with-hierarchy` flag for opt-in on non-OO codebases. | **High for UC-1 / Medium for UC-2.** Spec compliance often turns on "did we wire all subclasses of `BaseAgent` into the registry?" — a question only a hierarchy query answers. sc:reflect currently degenerates to grep heuristics here. Major lift in object-oriented codebases (Python class hierarchies, Java interface trees, TypeScript abstract bases). |
| 2 | **`onboarding`** | First-run automated routine that analyzes project structure / build system / testing setup and writes memory files. | **Medium.** Add as optional Wave 0 step gated on `list_memories` returning empty for the project slug. Risk: significant context consumption — must be opt-in or one-shot. Need a `--onboard` flag and an `onboarding_ran: bool` audit field. | **High at cold-start / Low at warm-start.** Massive value the first time `sc:reflect` runs on a new project (richer Wave 0 hydrate, better deviation calibration baseline). Near-zero value on every subsequent run. Best wired as a one-time bootstrap behind a `--onboard` flag, not default behavior. |
| 3 | **`prepare_for_new_conversation`** | Saves current session state into a Serena memory blob keyed for next-conversation hydration. | **Medium.** Hook into Wave 5 alongside existing `write_memory` for `reflect/last-pass-*`. Defines a new memory schema for in-flight Tier 3 handoffs (rubric scores, deviation set, evidence packet, reviewer verdicts). | **High for Tier 3 chain / Low otherwise.** When `--remediate` escalates to MDTM task-builder, the next conversation currently starts cold and must re-derive context. This tool is the canonical bridge — recovers the rubric scores, deviation set, and evidence packet without re-running Waves 1–4. Significant token savings on the remediation chain (estimated 30–60% reduction in handoff context). |
| 4 | **`execute_shell_command`** | Run shell commands (tests, linters, build, type-checkers) inside Serena's project context with output capture. | **Medium.** Sits within sc:reflect's existing audit posture — sc:reflect already writes `audit.log`, `serena-checkpoints.log`, reviewer briefs, and the final report. Wiring needs: per-call timeout, output-size cap, allowlist of safe verbs (`pytest`, `ruff`, `mypy`, `make test`, `uv run`, etc.), exit-code capture into the rubric, and explicit *non-mutating* gate (no `git commit`, no file writes outside `<output>/`). The complexity is in the safety envelope, not the integration. | **High (both UC-1 and UC-2).** One of the largest single-feature lifts available to the protocol:<br>• **UC-2 deviation audit** moves from "tasklist *claims* tests pass" to **"orchestrator *verified* tests pass on the affected files"** — directly eliminates the most common false-PASS path in the **Regression** deviation class.<br>• **UC-1 best-practice compliance** gains a real signal — `ruff` / `mypy` results on spec-referenced modules feed `S_dev_density` instead of being self-reported.<br>• Removes the current implicit dependency on the user to run tests between sc:reflect and any downstream remediation.<br>• Pairs naturally with `get_diagnostics_for_file` (LSP issues) and `summarize_changes` (what changed) to form a three-signal verification triangle.<br>**Recommend wiring as default behavior in UC-2 with `--no-verify` opt-out**, rather than opt-in. The cost is one test-suite run; the value is closing the audit loop. |

---

## Wiring notes (shared across all items)

- **Safety envelope (item 4):** `execute_shell_command` MUST enforce — (a) verb allowlist, (b) per-call timeout (default 120s, max 600s), (c) output cap (default 50KB tail-truncated), (d) no mutation outside `<output>/`, (e) audit-log entry per invocation with exit code, (f) optional `--no-verify` to disable globally.
- **Tier-gating:** items 1 and 3 are most valuable in Tier 2+ contexts (multiple reviewers, remediation handoff). Item 2 is one-shot per project. Item 4 should default-on in Tier 1 UC-2 as well, since it is the cheapest correctness signal available.
- **Fail-open:** §6.5 posture inherits — missing → `degraded: ["serena"]`, continue.
- **Schema:** all four require additions to the reflection card / return contract (`refs/return-contract.yaml` if present, or inline in SKILL.md §16).

---

## Research expansion section

> The detailed best-practice, documentation, and sample-use-case research for each row above is appended by the parallel research agent. The header below is the boundary; everything below it is research-agent output.

<!-- BEGIN: research-agent appended content -->

### 1. `type_hierarchy`

**Canonical documentation:**
- [Serena v1.0+ Extended Symbol Information news entry (oraios/serena/news/20260111.html)](https://github.com/oraios/serena/blob/main/news/20260111.html) — "A new type hierarchy tool has been introduced exclusively for JetBrains mode."
- [Serena Codex evaluation on Tianshou (docs/04-evaluation/030_results/010_cc_on_tianshou.md)](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/010_cc_on_tianshou.md) — "Serena's `type_hierarchy` function efficiently retrieves the full transitive type hierarchy (both superclasses and subclasses) in a single call, providing file locations for each type."
- [Serena Codex JetBrains-plugin evaluation (docs/04-evaluation/030_results/020_codex_on_jbplugin.md)](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/020_codex_on_jbplugin.md) — surfaces the verbatim call signature.
- [Serena README "Programming Language Support" capability matrix](https://github.com/oraios/serena) — confirms `type hierarchy` is supported on BOTH LSP and JetBrains backends per the capability table ("yes / yes").
- context7: `/oraios/serena` retrieval surfaced the Codex evaluation snippets and the JetBrains-mode news entry verbatim.

**Tool signature:**
```
type_hierarchy(relative_path=<file>, name_path=<symbol-name-path>, hierarchy_type=<both|supertypes|subtypes>, depth=<int>)
```
- Parameters:
  - `relative_path: str` — file containing the symbol ([Codex eval call form](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/020_codex_on_jbplugin.md))
  - `name_path: str` — symbol name path (e.g., `PostRequestHandler`); follows the same name-path semantics as `find_symbol` (per CHANGELOG v1.0 entry on overloaded-symbol indexing)
  - `hierarchy_type: enum {both, supertypes, subtypes}` — direction ([Codex eval](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/020_codex_on_jbplugin.md))
  - `depth: int` — recursion bound. `depth=0` means transitive traversal in the Codex eval call; unknown / not surfaced for what `depth=N>0` truncates.
- Returns: a hierarchy slice "providing file locations for each type" — exact JSON shape unknown / not surfaced beyond "type name + file location per node" ([Tianshou eval](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/010_cc_on_tianshou.md)).
- Errors / known exceptions: not surfaced in any source; tool inherits Serena's standard "language-server unavailable → fall back" envelope per [§6.5 of SKILL.md](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md). The README capability table shows LSP "yes" but the news entry says "exclusively for JetBrains mode," so LSP coverage is likely partial and language-server-dependent.

**Best-practice usage patterns:**
- Pattern 1 — *Single-call hierarchy retrieval over grep iteration*: Serena's evaluation explicitly contrasts `type_hierarchy` with built-in `Grep`: "Built-in tools require multiple iterative `Grep` searches to piece together even a partial hierarchy, making them significantly less efficient" ([Tianshou eval](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/010_cc_on_tianshou.md)). For OO codebases, replace the orchestrator's "find all subclasses of `BaseAgent`" grep heuristic with one `type_hierarchy(hierarchy_type=subtypes)` call.
- Pattern 2 — *Bounded traversal via `depth`*: Use `depth=1` to verify direct supertype/subtype edges only when interaction effects across a single inheritance hop are sufficient; use `depth=0` (transitive) for full registry-completeness verification.
- Pattern 3 — *Backend-aware invocation*: Probe backend via `get_current_config` at Wave 0; route to `type_hierarchy` only when the JetBrains backend is active OR when the LSP language is in the README capability matrix's confirmed list. Otherwise fall back to a `find_symbol` + `find_referencing_symbols` chain on the base class.

**Failure modes / gotchas:**
- The [news entry](https://github.com/oraios/serena/blob/main/news/20260111.html) flags the tool as "exclusive to JetBrains mode," but the [README capability matrix](https://github.com/oraios/serena) shows LSP support too. The discrepancy suggests LSP coverage is language-server-dependent — Java/Kotlin/TypeScript likely work; experimental languages (Erlang, GDScript per CHANGELOG v1.5.0) likely do not.
- The Codex Tianshou eval was run on a Python codebase, suggesting LSP support exists at least for Python's `pylsp`/`pyright`, contradicting the "JetBrains only" framing.
- Performance unknown for large hierarchies; the JetBrains-plugin eval uses `depth=0` (transitive) on a single class without comment on cost, but no benchmarking surfaced.

**Version / language-server dependencies:**
- Introduced in: v1.0.0 (initial JetBrains plugin release per [CHANGELOG v1.0.0](https://github.com/oraios/serena/blob/main/CHANGELOG.md), JetBrains backend was added then). The [news entry](https://github.com/oraios/serena/blob/main/news/20260111.html) dates the JetBrains-side tool to 2026-01-11.
- Languages supported: JetBrains backend covers all IntelliJ-supported languages (Java, Kotlin, Python, TypeScript, etc., but not Rider/CLion-only languages). LSP backend: language-server-dependent; Java's `eclipse.jdt.ls` and TypeScript's `typescript-language-server` are documented as supporting type hierarchy via LSP `textDocument/typeHierarchy`.

**sc:reflect wiring (sample use case):**
- Wave: 1B.3 (cross-task interaction-effects scan) + Wave 1A (mandatory evidence chain extension).
- Insertion point: [SKILL.md §4.1 Step 1B.3](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — the symbol-overlap scan currently uses `find_symbol` + `find_referencing_symbols`. Add a third pass: for every base class or interface symbol in the diff, query `type_hierarchy(hierarchy_type=subtypes, depth=0)` to verify registry-completeness invariants. Also extend [§6.1 Mandatory evidence-gathering chain](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) step 4.5 (inserted between `find_referencing_symbols` and `get_diagnostics_for_file`).
- Concrete invocation (paste-ready):
  ```
  # Wave 1A step 4.5 (new), only when backend supports it
  if backend_supports_type_hierarchy(serena_config):
      for base_symbol in spec_referenced_base_classes:
          hierarchy = mcp__serena__type_hierarchy(
              relative_path=base_symbol.file,
              name_path=base_symbol.name_path,
              hierarchy_type="subtypes",
              depth=0,
          )
          # Compare hierarchy node set against tasklist-claimed subclass registrations
          unregistered = set(hierarchy.subtypes) - set(tasklist.registered_subclasses)
          if unregistered:
              emit_finding(category="coverage_gap", subtypes=unregistered)
  ```
- Rubric inputs affected: `S_dev_density` increases when hierarchy gaps surface (an unmapped subtype is exactly an unmapped artifact); `coverage_pct` for UC-1 gains a new denominator term (hierarchy-derived requirements).
- Audit-log field(s) emitted: `hierarchy_scan_ran: bool`, `hierarchy_backend: jetbrains|lsp|none`, `hierarchy_nodes_examined: int`, `hierarchy_gaps_found: int`.
- Return-contract addition(s): `hierarchy_slice_path: <abs path>` (location of materialized hierarchy artifact at `<output>/artifacts/hierarchy-slice.yaml`); contract minor-version bump per [§9.4 evolution policy](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md).
- Fail-open behavior: when backend probe at Wave 0 reports neither JetBrains nor a hierarchy-capable LSP, emit `hierarchy_backend: none`, skip step 4.5 in §6.1, and mark `degraded_components: ["type-hierarchy"]` per [§6.5 fail-open posture](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md). The skill must never abort because hierarchy is unavailable.

**Interaction with adjacent sc:reflect mechanics:**
- Composes naturally with the existing §6.1 chain — `get_symbols_overview` finds the base class, `find_symbol` retrieves its body, `find_referencing_symbols` shows downstream consumers, and `type_hierarchy` extends the evidence with *upstream* (supertypes) and *peer* (siblings via shared supertypes) edges. This closes a structural gap the current chain misses: a class's *family* is not derivable from referencing call sites alone.
- Pairs with [Wave 1B.3](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — when the cross-task scan identifies a shared base-class symbol as a top-30 hotspot, `type_hierarchy` becomes the verification tool for "is this genuinely shared or just transiently named the same."

---

### 2. `onboarding`

**Canonical documentation:**
- [Serena Memories & Onboarding (oraios.github.io)](https://oraios.github.io/serena/02-usage/045_memories.html) — primary reference for onboarding behavior, the `memory_maintenance` seed, the gating ("triggered when no project memories exist"), and the recommended post-onboarding workflow.
- [Serena Project Workflow (docs/02-usage/040_workflow.md)](https://github.com/oraios/serena/blob/main/docs/02-usage/040_workflow.md) — confirms onboarding is the default on first project encounter.
- [Serena Tools reference (oraios.github.io/serena/01-about/035_tools.html)](https://oraios.github.io/serena/01-about/035_tools.html) — onboarding is listed under `workflow_tools`: "Performs onboarding (identifying the project structure and essential tasks, e.g. for testing or building)."
- [CHANGELOG v1.5.0 — `check_onboarding_performed` removal](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — "Delete `check_onboarding_performed` tool (instead extend project activation message)." So as of v1.5.0, the check-flag tool is gone; activation message carries onboarding state.
- [serena/src/serena/resources/config/modes/onboarding.yml](https://github.com/oraios/serena/blob/main/src/serena/resources/config/modes/onboarding.yml) — the onboarding mode definition.
- context7: `/oraios/serena` retrieval surfaced the workflow_tools description and Memories & Onboarding section verbatim.

**Tool signature:**
```
onboarding()    # no parameters surfaced in any source
```
- Parameters: none surfaced. The tool is invoked without arguments and the agent itself drives the read/analyze/write loop using its other tools (`read_file`, `list_dir`, `write_memory`).
- Returns: triggers an interactive workflow whose final state is a populated `.serena/memories/` directory; exact tool-return JSON unknown / not surfaced.
- Errors / known exceptions: per the docs, "If an LLM fails to complete the onboarding and does not actually write the respective memories to disk, you may need to ask it to do so explicitly" ([Memories & Onboarding "Tips for Onboarding"](https://oraios.github.io/serena/02-usage/045_memories.html)). Silent-incomplete is the dominant failure mode.

**Best-practice usage patterns:**
- Pattern 1 — *Gate on memory absence*: per [the docs](https://oraios.github.io/serena/02-usage/045_memories.html), "Serena will check whether onboarding was already performed by looking for existing project memories and will skip the onboarding process if memories are found." Trigger onboarding only when `list_memories` returns empty for the project slug.
- Pattern 2 — *Switch conversations after completion*: "Context usage: The onboarding process will read a lot of content from the project, filling up the context window. It is therefore advisable to switch to a new conversation once the onboarding is complete" ([docs](https://oraios.github.io/serena/02-usage/045_memories.html)). In sc:reflect, this means onboarding should be its own pre-pass, not interleaved with the reflection waves.
- Pattern 3 — *Honor `memory_maintenance` precedence*: as of [CHANGELOG v1.5.0](https://github.com/oraios/serena/blob/main/CHANGELOG.md), onboarding seeds a `memory_maintenance` memory; "A `global/memory_maintenance` memory takes precedence over the per-project seed." sc:reflect should not overwrite a `global/memory_maintenance` if present.
- Pattern 4 — *Disable cleanly when not wanted*: `no-onboarding` mode in `base_modes` disables only onboarding; `no-memories` disables the whole memory subsystem ([Configuration](https://oraios.github.io/serena/02-usage/050_configuration.html)).

**Failure modes / gotchas:**
- Onboarding is excluded by default in the `ide-assistant` and `claude-code` contexts (per [issue #494 trace](https://github.com/oraios/serena/issues/494) showing the active-tool list). sc:reflect runs under whichever context the operator chose — onboarding tool may not even be exposed. Probe before assuming availability.
- Auto-onboarding creates a `.serena/` directory anywhere the user activates a project — this surprised users in [discussion #1513](https://github.com/oraios/serena/discussions/1513). sc:reflect must NOT trigger onboarding implicitly; it must be opt-in via an explicit flag.
- The exact set of memories onboarding produces is implementation-dependent and not enumerated in any single source. Known seeded files: `memory_maintenance`. Likely produced (inferred from docs): `project_structure`, `suggested_commands`, `style_conventions`, `testing_setup`. unknown / not surfaced as a definitive list.
- LLM silent-fail mode: onboarding completes "successfully" but doesn't actually write memories. sc:reflect's wiring must verify memory existence post-onboarding before declaring the bootstrap succeeded.

**Version / language-server dependencies:**
- Introduced in: pre-v1.0; onboarding was part of the initial public release (2025-04-01 per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md)). The `memory_maintenance` seeding behavior was added in [v1.5.0](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: language-agnostic — onboarding reads project files generically. No LSP dependency.

**sc:reflect wiring (sample use case):**
- Wave: 0 (project activation & session bootstrap), conditionally.
- Insertion point: [SKILL.md §4 Wave 0 step 0.7 "Activate Serena project + memory hydrate"](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md). Add a new sub-step `0.7b Onboarding bootstrap (conditional, --onboard flag)`.
- Concrete invocation (paste-ready):
  ```
  # Wave 0 step 0.7b (new), only when --onboard flag set
  if args.onboard:
      memories = mcp__serena__list_memories()
      if not memories.get(f"reflect/{project_slug}/", []):
          # Note: tool likely excluded in ide-assistant context — probe first
          if "onboarding" in active_tools:
              mcp__serena__onboarding()  # interactive; consumes significant context
              # Verify post-onboarding state (silent-fail guard)
              memories_after = mcp__serena__list_memories()
              if len(memories_after) <= len(memories):
                  emit_warn("onboarding completed but no new memories written")
                  emit_audit(onboarding_ran=True, onboarding_succeeded=False)
              else:
                  emit_audit(onboarding_ran=True, onboarding_succeeded=True)
          else:
              emit_warn("onboarding tool not available in current context")
              emit_audit(onboarding_ran=False, onboarding_skipped_reason="context-excluded")
  ```
- Rubric inputs affected: `S_dev_density` may decrease on subsequent reflect runs because deviation-pattern memory hydrate (§6.3) now has richer baseline content; no direct first-run rubric effect.
- Audit-log field(s) emitted: `onboarding_ran: bool`, `onboarding_succeeded: bool`, `onboarding_memories_written: list[str]`, `onboarding_skipped_reason: str|null`.
- Return-contract addition(s): `onboarding_ran: bool` (top-level), `onboarding_memories_count: int` (telemetry block); contract minor-version bump per [§9.4 evolution policy](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md).
- Fail-open behavior: per [§6.5](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md), if onboarding tool is unavailable in the active context, skip with audit row; never block the skill. If `--onboard` was explicitly requested but the tool is excluded, surface a clear WARN telling the user to switch context, not a hard STOP.

**Interaction with adjacent sc:reflect mechanics:**
- Onboarding feeds the [§6.3 per-project memory pattern](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — the `reflect/last-pass-{slug}` and `reflect/deviation-patterns-{slug}` blobs are *new* additions on top of Serena's own onboarding memories (`project_structure`, `suggested_commands`, etc.). Onboarding establishes the "calibration baseline" the matrix description points to. The two memory namespaces must coexist without collision; sc:reflect's `reflect/` prefix already provides isolation.
- Pairs with [Wave 0 alias routing (§4.0 step 0.5)](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — onboarding writes memories the per-reviewer brief packages in [§4.3 step 3B.0](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) can reference via `mem:` links, reducing per-reviewer token spend by linking to richer hydrate content.

---

### 3. `prepare_for_new_conversation`

**Canonical documentation:**
- [Serena Tools reference (oraios.github.io/serena/01-about/035_tools.html)](https://oraios.github.io/serena/01-about/035_tools.html) — listed under `workflow_tools`.
- [Serena Additional Usage / "Running Out of Context" (docs/02-usage/999_additional-usage.md)](https://github.com/oraios/serena/blob/main/docs/02-usage/999_additional-usage.md) — "When dealing with long or complex tasks that consume a lot of context tokens, it's advisable to start a new conversation. Serena provides a tool to summarize the current progress and essential information, which can be saved to a memory. In a new conversation, Serena can read this memory to resume the task effectively."
- [Issue #637 — "why is `prepare_for_new_conversation` excluded in ide-assistant context?"](https://github.com/oraios/serena/issues/637) — confirms the tool's purpose: "create a summary of the current state of the progress and all relevant info for continuing it" and that it is excluded by default in `ide-assistant` context.
- [Issue #609 — "rename memory tools to handoff and handoff-retrieve"](https://github.com/oraios/serena/issues/609) — community framing: "SERENA's memory tools are more indicated to accommodate session pause and restart between context refresh."
- context7: `/oraios/serena` retrieval surfaced the "Running Out of Context" section verbatim.

**Tool signature:**
```
prepare_for_new_conversation()    # signature not surfaced in any source
```
- Parameters: unknown / not surfaced — no source documents the exact parameter shape. Based on the docs description ("summarize the current progress and essential information, which can be saved to a memory"), the tool likely accepts an optional `memory_name` to control where the summary is written, but this is not confirmed.
- Returns: unknown / not surfaced; likely a memory-name handle or success indicator.
- Errors / known exceptions: unknown / not surfaced. Inherits the standard Serena memory-write failure modes (disk full, permission denied, serena down) per [§14 Error Handling Matrix row "Serena `write_memory` fails at Wave 5"](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md).

**Best-practice usage patterns:**
- Pattern 1 — *Pre-context-exhaustion handoff*: per [docs](https://github.com/oraios/serena/blob/main/docs/02-usage/999_additional-usage.md), invoke when context is filling up and you intend to resume the task in a new conversation. Save to a named memory, then in the next conversation call `read_memory` with that name.
- Pattern 2 — *Override the ide-assistant exclusion*: per [issue #637](https://github.com/oraios/serena/issues/637), the tool is excluded by default in `ide-assistant` context. Operators using Serena under Claude Code must explicitly include it via context customization to use it.
- Pattern 3 — *Pair with task-builder/MDTM handoffs*: the sc:reflect Tier 3 escalation route hands off to `task-builder` ([SKILL.md §7](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md)). `prepare_for_new_conversation` is the canonical Serena mechanism for the handoff blob.

**Failure modes / gotchas:**
- Excluded by default in `ide-assistant` context — the default Serena context for Claude Code workflows. Operators must explicitly include it. Per [issue #494 active-tool trace](https://github.com/oraios/serena/issues/494): "Context ide-assistant excluded 5 tools: create_text_file, read_file, execute_shell_command, prepare_for_new_conversation, replace_regex."
- Tool signature is the largest research gap of any of the four features in this matrix. Implementation MUST verify the actual signature against the live MCP surface before relying on parameters.
- LLM silent-incomplete failure mode applies as with `onboarding` — the tool may report success without having materially summarized progress.
- The `mem:` reference convention (v1.5.0+) means a handoff memory can reference other project memories — but stale references will fail integrity checks per [Memories docs](https://oraios.github.io/serena/02-usage/045_memories.html).

**Version / language-server dependencies:**
- Introduced in: pre-v1.0; present in the initial public release per [Issue #494 active-tools list (loaded tools 36)](https://github.com/oraios/serena/issues/494). No specific introduction CHANGELOG entry — likely v0.1.x.
- Languages supported: language-agnostic; no LSP dependency.

**sc:reflect wiring (sample use case):**
- Wave: 5 (Synthesis + persist) and Wave 6 (Tier 3 remediation handoff).
- Insertion point: [SKILL.md §6.3 Memory pattern](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) extends with a new `reflect/handoff-{slug}-{timestamp}` namespace; [SKILL.md Wave 6](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) calls the tool just before invoking `task-builder`.
- Concrete invocation (paste-ready):
  ```
  # Wave 6 step before task-builder handoff (when --remediate accepted)
  handoff_key = f"reflect/handoff-{project_slug}-{run_timestamp}"
  # ACTUAL parameter shape unknown; this is the assumed surface
  mcp__serena__prepare_for_new_conversation(
      memory_name=handoff_key,   # assumed parameter — verify against live tool surface
      # likely an implicit "summarize current state" content build
  )
  # Then invoke task-builder with a pointer to the handoff memory
  Skill task_builder with --handoff-memory-key=$handoff_key \
                          --rubric-scores=$rubric_yaml \
                          --deviation-register=$deviation_yaml
  ```
- Rubric inputs affected: none directly (Tier 3 is post-rubric).
- Audit-log field(s) emitted: `handoff_memory_written: bool`, `handoff_memory_key: str`, `handoff_payload_size_bytes: int`.
- Return-contract addition(s): `handoff_memory_key: <serena-memory-name>` under the Tier 3 section of [§9.1](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md); minor-version bump.
- Fail-open behavior: if the tool is excluded by context (the most likely failure path), fall back to `mcp__serena__write_memory` with an inline-built summary blob. Per [§14 row "Serena `write_memory` fails at Wave 5"](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md), continue: report still ships, emit `memory_persist_failed: true` (extend the existing handler to also cover `prepare_for_new_conversation` failures with `handoff_persist_failed: true`).

**Interaction with adjacent sc:reflect mechanics:**
- Composes with the existing [§6.3 memory pattern](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — `reflect/last-pass-{slug}` is the "what happened" record; `reflect/deviation-patterns-{slug}` is the "what to look for next time" record; the new `reflect/handoff-{slug}-{timestamp}` is the "what's in-flight right now" record that bridges to Wave 6.
- Extends the [Tier 3 task-builder handoff (§7)](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — the matrix description claims 30-60% token savings on the remediation chain; this is plausible because the handoff memory replaces re-derivation of Waves 1-4 context (rubric scores, deviation set, evidence packet) that would otherwise need to be reconstructed by `task-builder`'s parallel research pass.

---

### 4. `execute_shell_command` *(highest-value item — deepest treatment)*

**Canonical documentation:**
- [Serena llms.txt / Tools reference](https://oraios.github.io/serena/01-about/035_tools.html) and [context7 `/oraios/serena` retrieval](https://context7.com/oraios/serena/llms.txt) — "The `execute_shell_command` tool runs shell commands in the project's root directory or a specified subdirectory. It's useful for builds, tests, and linters, returning stdout, stderr, and the return code."
- [Serena on ChatGPT special guide (docs/03-special-guides/serena_on_chatgpt.md)](https://github.com/oraios/serena/blob/main/docs/03-special-guides/serena_on_chatgpt.md) — documents the security-relevant `excluded_tools` and `read_only: true` project-config gates: `excluded_tools: [execute_shell_command, ...]` and `read_only: true`.
- [Serena project.yml template (referenced in issue #92)](https://github.com/oraios/serena/issues/92) — confirms the `read_only` project-config flag added 2025-04-18: "whether the project is in read-only mode. If set to true, all editing tools will be disabled and attempts to use them will result in an error."
- [Serena Security Audit Discussion #380](https://github.com/oraios/serena/discussions/380) — discloses the tool's implementation: `src/serena/tools/cmd_tools.py:14-43`, `src/serena/util/shell.py:15-42`, uses `subprocess.Popen(command, shell=True)`, no command whitelisting or sandboxing.
- [Issue #581 — `execute_shell_command` parameter trace](https://github.com/oraios/serena/issues/581) — verbatim default-parameter values: `command=<str>, cwd=None, capture_stderr=True, max_answer_chars=200000`.
- [CHANGELOG v0.1.3 — "Fix `ExecuteShellCommandTool` and `GetCurrentConfigTool` hanging on Windows"](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- [Configuration > Global Configuration (docs/02-usage/050_configuration.md)](https://github.com/oraios/serena/blob/main/docs/02-usage/050_configuration.md) — "tool execution parameters like timeouts" are configurable globally.
- context7: `/oraios/serena` retrieval surfaced two canonical invocation examples and the read_only project-config snippet verbatim.

**Tool signature:**
```
execute_shell_command(command: str, cwd: str | None = None, capture_stderr: bool = True, max_answer_chars: int = 200000)
```
- Parameters (confirmed from [issue #581 trace](https://github.com/oraios/serena/issues/581) and [context7 retrieval](https://context7.com/oraios/serena/llms.txt)):
  - `command: str` — shell command to run; executed via `subprocess.Popen(command, shell=True)` ([Security Audit #380](https://github.com/oraios/serena/discussions/380))
  - `cwd: str | None` — working directory; `None` defaults to project root ([context7](https://context7.com/oraios/serena/llms.txt))
  - `capture_stderr: bool` — default `True` ([issue #581 trace](https://github.com/oraios/serena/issues/581))
  - `max_answer_chars: int` — default `200000` ([issue #581 trace](https://github.com/oraios/serena/issues/581))
- Returns: stdout, stderr (when captured), and return code per [Tools reference](https://oraios.github.io/serena/01-about/035_tools.html). Exact JSON shape unknown / not surfaced beyond these three fields.
- Errors / known exceptions:
  - Subprocess invocation errors (e.g., Windows `creationflags` collision in [issue #581](https://github.com/oraios/serena/issues/581)).
  - Hang on Windows in pre-v0.1.3 ([CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md)).
  - Tool is excluded entirely when `read_only: true` is set in `project.yml` ([issue #92 project.yml template](https://github.com/oraios/serena/issues/92), [Serena on ChatGPT](https://github.com/oraios/serena/blob/main/docs/03-special-guides/serena_on_chatgpt.md)).
  - Tool is excluded by default in the `ide-assistant` and `claude-code` contexts ([issue #494 active-tool list](https://github.com/oraios/serena/issues/494)).
  - Per-call timeout: the global-config `tool execution parameters like timeouts` setting exists ([config docs](https://github.com/oraios/serena/blob/main/docs/02-usage/050_configuration.md)) but the exact default value is unknown / not surfaced in any source.

**Best-practice usage patterns:**
- Pattern 1 — *Test/lint/build verification*: per the [context7 retrieval examples](https://context7.com/oraios/serena/llms.txt), the canonical use is `pytest test/serena -v -m python` and `npm run build`. This is precisely the verification class sc:reflect needs.
- Pattern 2 — *Safety envelope at the consumer side, not the tool*: the tool itself has no allowlist. Per the [Security Audit #380](https://github.com/oraios/serena/discussions/380), "No command whitelisting or sandboxing mechanisms." The consumer (sc:reflect) MUST impose the safety envelope.
- Pattern 3 — *Honor the project's `read_only` config*: when `read_only: true`, the tool is unavailable. sc:reflect must probe project config at Wave 0 and degrade gracefully — exactly the pattern in the [matrix description's "verb allowlist, timeout, output cap"](.).
- Pattern 4 — *Use `cwd` to scope to affected files*: per [context7 example #2 (`cwd: "frontend"`)](https://context7.com/oraios/serena/llms.txt), `cwd` restricts execution scope, which limits blast radius when running scoped lint or test commands on only the modified subtree.

**Failure modes / gotchas:**
- Excluded by default in `ide-assistant` and `claude-code` contexts ([issue #494](https://github.com/oraios/serena/issues/494)). Operators must explicitly include it, which is a deliberate friction step. sc:reflect must NOT silently degrade — it must surface the unavailability loudly so the operator knows the verification triangle isn't firing.
- `read_only: true` blocks the tool entirely ([Serena on ChatGPT](https://github.com/oraios/serena/blob/main/docs/03-special-guides/serena_on_chatgpt.md), [issue #92](https://github.com/oraios/serena/issues/92)). This is the most operationally-relevant gate for sc:reflect's posture — Serena's `read_only` is broader than sc:reflect's read-only-against-project-source posture, so they don't trivially align.
- Per the [Security Audit #380](https://github.com/oraios/serena/discussions/380): `shell=True` enables command injection if the command string is built from untrusted input. sc:reflect builds the command from spec/tasklist content — untrusted by definition.
- No default timeout surfaced. The [global-config docs](https://github.com/oraios/serena/blob/main/docs/02-usage/050_configuration.md) mention "tool execution parameters like timeouts" exist but don't quote the default. Per the matrix description, sc:reflect's safety envelope sets `default 120s, max 600s` — this must be enforced consumer-side (e.g., a wrapper that wraps the command in `timeout 120 <cmd>` rather than relying on Serena's tool-level timeout).
- Output cap (`max_answer_chars=200000`) is high; the matrix description's `default 50KB tail-truncated` cap is more aggressive and must be imposed at the consumer side.

**Version / language-server dependencies:**
- Introduced in: pre-v1.0; present in 2025-04-01 initial public release per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md). Hang fix in v0.1.3.
- Languages supported: language-agnostic; no LSP dependency.

**sc:reflect wiring (sample use case):**
- Wave: 1A (mandatory evidence chain extension) for the verification triangle; Wave 1B for UC-2 tasklist-claim verification; Wave 5 pre-synthesis for re-verification.
- Insertion point: [SKILL.md §6.1 Mandatory evidence-gathering chain](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — add step 5.5 between `get_diagnostics_for_file` and re-Read; [SKILL.md Wave 1B](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — add verification suite that runs scoped tests against affected files. Critically, this also tightens the §6.4 audit-checkpoint pattern: rather than `think_about_*` nudges being the only "Did the work actually pass?" signal, real test exit codes feed the audit.
- Concrete invocation (paste-ready):
  ```
  # Wave 1A step 5.5 (new) — verification triangle
  # Probe availability at Wave 0
  if not serena_capabilities.execute_shell_command_available:
      emit_audit(verify_skipped=True, verify_skip_reason="tool-unavailable")
      degraded_components.append("execute_shell_command")
      # FAIL-OPEN per §6.5: continue without this signal
  else:
      # Consumer-side safety envelope (matrix description §wiring notes)
      VERB_ALLOWLIST = {"pytest", "ruff", "mypy", "make", "uv", "npm", "tsc", "cargo"}
      cmd_tokens = command.split()
      first_verb = cmd_tokens[0] if cmd_tokens else ""
      if first_verb not in VERB_ALLOWLIST:
          emit_audit(verify_blocked=True, verify_blocked_reason=f"verb '{first_verb}' not in allowlist")
          continue  # skip; do not invoke

      # Wrap with a hard timeout — Serena's tool-level timeout is unverified
      wrapped = f"timeout 120 {command}"
      result = mcp__serena__execute_shell_command(
          command=wrapped,
          cwd=affected_subtree_path,   # scope to changed files
          capture_stderr=True,
          max_answer_chars=51200,       # 50 KB cap, tighter than 200 KB default
      )
      # Tail-truncate just in case (defensive)
      stdout_tail = result.stdout[-51200:]
      stderr_tail = result.stderr[-51200:] if result.stderr else ""

      emit_audit(
          verify_cmd=command,
          verify_exit_code=result.return_code,
          verify_stdout_path=write_to_output(stdout_tail),
          verify_stderr_path=write_to_output(stderr_tail),
          verify_duration_ms=elapsed,
      )

      # UC-2 deviation classification: feed result into §10.4 Regression detection
      if result.return_code != 0 and command_targets_regression_candidate:
          mark_deviation_class("regression", evidence_anchor=verify_stdout_path)
  ```
- Rubric inputs affected:
  - `S_dev_density` (UC-1 & UC-2): real `ruff`/`mypy` results on spec-referenced modules now feed this directly rather than being self-reported.
  - `coverage_pct` (UC-2): tasklist items claiming "tests added" can now be verified by running the test file and checking it both exists and passes.
  - New `regression_present` flag in [§9.1 stable contract](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md): true when any verification command exited non-zero on a tasklist-claimed-passing file.
- Audit-log field(s) emitted (per matrix description "safety envelope" requirements):
  - `verify_invocations: list[{cmd: str, exit_code: int, duration_ms: int, stdout_path: str, stderr_path: str, blocked_reason: str|null}]`
  - `verify_skipped: bool` + `verify_skip_reason: str|null`
  - `verify_timeout_default: int` (e.g. `120`) for forensic provenance.
- Return-contract addition(s): under [§9.1 stable contract](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md):
  ```yaml
  verification_ran: bool
  verification_invocations: int          # count of verify_invocations
  verification_failures: int             # exit_code != 0 count
  verification_regressions_detected: int # exit_code != 0 on tasklist-claimed-passing files
  verification_skip_reason: tool-unavailable | read-only-project | --no-verify | null
  ```
  Contract minor-version bump; consumers in [§9.3 Consumer Field Map](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) (sprint executor.py, sc-task-protocol end-of-task hook, sc:tasklist) can opt in to consume `verification_regressions_detected > 0` as a strong rollback signal.
- Fail-open behavior: per [§6.5 fail-open posture](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — when `execute_shell_command` is unavailable (context-excluded, `read_only` project, or `--no-verify` set), emit `verification_ran: false` with the appropriate `verification_skip_reason`, fall back to the pre-existing `get_diagnostics_for_file` LSP-issue signal as the only correctness check, and degrade the **Regression** class's [§10.4 detection signals](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) from "tests verified failing" to "task log claims tests passed" with a Grounding Gap entry. This preserves the audit posture without breaking the skill.

**Interaction with adjacent sc:reflect mechanics:**
- *Forms the verification triangle* (per matrix description): `get_diagnostics_for_file` (LSP issues) + `summarize_changes` (what changed) + `execute_shell_command` (does it pass). The triangle is the single largest correctness-signal expansion in V3.
- *Tightens [§6.4 audit-checkpoint pattern](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md)*: the `think_about_*` checkpoints currently produce 200-token nudges that bias `S_dev_density` upward when they surface gaps. With `execute_shell_command`, the pattern can be reinforced — a `think_about_collected_information` nudge that says "we should run the tests" can now be *acted on* by the orchestrator, not just logged. The `think_about_*` outputs stay non-load-bearing for ship-gating per the existing posture; what changes is that the orchestrator has a real mechanism to honor them.
- *Aligns with the posture clarification in `03-conversation-context.md` §3*: reflect "may execute non-mutating verification commands — `pytest`, `ruff`, `mypy`, `make test`, `uv run`, build steps — and consume their exit codes / output as audit signal." This is the precise integration point. The wiring above (VERB_ALLOWLIST, scoped `cwd`, 120s timeout, 50KB cap, no mutation guard) operationalizes that clarification.
- *Plugs into the [§14.5.2 promotion gate's condition 4](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) (`deviation_count_by_class.regression == 0`)*: `verification_regressions_detected > 0` deterministically promotes a hunk to Regression class, blocking Wave 7 promotion. This closes the largest single false-PASS path in the existing protocol.
- *Compatible with the [Wave 0 read_only project-config probe](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md)*: extend Wave 0 step 0.7 `Activate Serena project` to also call `get_current_config` and inspect for `read_only: true`. When that flag is set, sc:reflect SHOULD respect it as a stricter superset of its own posture (Serena `read_only` blocks ALL editing tools, including symbolic editing routed to Tier 3 — but it also blocks `execute_shell_command`, which sc:reflect wants enabled). The resolution: when `read_only: true`, sc:reflect emits a clear WARN ("verification triangle disabled by Serena `read_only: true`; verdict will degrade to LSP-only signals") and proceeds.

---

## Cross-feature observations

**Adoption ordering recommendation.**

1. **`execute_shell_command` FIRST.** Highest single-feature ROI (closes the largest false-PASS path in UC-2 Regression detection), independent of the other three, fail-open profile is well-understood (Wave 0 probe + degraded telemetry), and the safety envelope work is already specified in [the matrix wiring notes](.). It also has the cleanest contract-evolution story — a single minor-version bump adds the four `verification_*` fields without touching any existing field. Ship this as a standalone PR; do not bundle.

2. **`onboarding` SECOND.** Independent of the other three, one-shot per project (no per-run regression risk), and the wiring is a single Wave 0 sub-step gated behind `--onboard`. It strengthens the calibration baseline for the existing [§6.3 memory pattern](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) which paid §3 of [Reviewer-V3 conversation context](.) has already validated. Schema additions are forward-compatible. The main risk is operator surprise from `.serena/` directory creation — mitigated by making the flag explicit and never auto-triggering.

3. **`prepare_for_new_conversation` THIRD.** Conditional on Tier 3 / Wave 6 being a frequently-exercised path. The 30-60% token-saving claim only realizes when the remediation chain actually runs, so adoption value scales with how often `--remediate` is accepted. The largest research gap (tool signature unknown) means implementation MUST verify the live tool surface before relying on parameters; treat this as a Wave 6 enhancement, not a Wave 0/1 dependency.

4. **`type_hierarchy` LAST.** Highest backend-dependency risk (JetBrains-exclusive per [news entry](https://github.com/oraios/serena/blob/main/news/20260111.html) but partial LSP per [README](https://github.com/oraios/serena)), useful only on OO codebases, and the `--with-hierarchy` opt-in flag means non-OO codebases see no degradation when this is unshipped. Schema additions are small (one path field). Ship as the v1.1 enhancement after the first three are stable in production.

**Overlap analysis.**

- *Ship together in ONE PR:* `execute_shell_command` + the existing `get_diagnostics_for_file` extension (Wave 1A step 5.5). These two form the verification triangle the matrix description names explicitly. Co-designing the audit-log shape (`verify_*` fields) and the §6.1 chain insertion point avoids two consecutive contract minor bumps.
- *Ship in SEPARATE PRs (different waves, different gating):* `onboarding` (Wave 0 conditional) and `prepare_for_new_conversation` (Wave 5/6 conditional). They share the Serena memory namespace, but their lifecycle and consumer surfaces are disjoint. Bundling them into one PR would conflate "first-run bootstrap" with "Tier 3 handoff" concerns and obscure the gating logic.
- *Co-design SCHEMA additions for the memory features*: `onboarding`'s memory baseline, `prepare_for_new_conversation`'s handoff blob, and the existing [§6.3 `reflect/last-pass-*` and `reflect/deviation-patterns-*` keys](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) should share a single naming convention (`reflect/<category>-<slug>[-<timestamp>]`) and a single TTL/retention policy (90-day expire, 20-entry cap per key) decided once and applied across all three features.
- *Keep `type_hierarchy` orthogonal*: no overlap with the memory or verification features; isolated to the §6.1 chain. A separate PR with its own backend-probe machinery.

**Outstanding research gaps.**

- **`prepare_for_new_conversation` tool signature** — no source surfaces the parameter shape. Implementation MUST verify against the live MCP surface (`Skill('serena', '--list-tools')` or equivalent) before parameter-dependent wiring.
- **`execute_shell_command` default timeout** — the global-config docs reference the setting's existence but not its default value. Mitigated by the consumer-side `timeout <N> <cmd>` wrap.
- **`onboarding` produced-memory list** — no canonical enumeration of which memory files onboarding writes. Mitigated by post-onboarding `list_memories` count diff as the success signal.
- **`type_hierarchy` LSP-vs-JetBrains coverage matrix** — the news-entry/README discrepancy on whether LSP backends support the tool needs empirical resolution per-language (run `type_hierarchy` against a Python/Java/TypeScript test project and record success/failure). Until empirically confirmed, the `--with-hierarchy` flag should default-off on LSP backends.

**One-sentence ordering recommendation:** Ship `execute_shell_command` first as the highest-ROI standalone PR closing the verification-triangle gap, then `onboarding` and `prepare_for_new_conversation` in separate PRs sharing a co-designed memory-naming convention, and reserve `type_hierarchy` for a v1.1 enhancement gated on a backend-probe.

<!-- END: research-agent appended content -->
