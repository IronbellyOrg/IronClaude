# Code Review: PR #197 — feat(rf-harness): sync RF skills + agents + reflect enforcement (contract 1.5.1)

**Target**: [IronbellyOrg/IronClaude#197](https://github.com/IronbellyOrg/IronClaude/pull/197)
**Reviewer**: `/sc:auggie-review` (depth=deep, focus=all)
**Generated**: 2026-06-20 22:xx UTC
**Base ↔ Head**: `master` ↔ `feat/rf-harness-sync` (head `a3f3f0cb`)
**Scope reviewed**: code + enforcement surface only — **16 files / ~1,925 lines**. The 3 brand‑new skill docs (`operational-guide`, `readme`, `roadmap`; 6,495 lines) were **excluded** by reviewer choice (PR exceeds the deep‑review 5,000‑line threshold; the new docs are pure additive markdown with low defect density).
**Findings**: 0 critical · 2 high · 2 medium · 3 low · 2 nits · **9 dropped during grounding**

---

## Summary

**Recommendation: 🟠 Request changes.** Two issues should be fixed before merge.

1. **The headline change is backwards.** The 8 `rf-*` agents are renamed from `mcp__tavily__tavily-search` (hyphen) to `mcp__tavily__tavily_search` (underscore). The **hyphen form is the one that actually resolves** in this harness — it is the literal registered tool id, and every other Tavily consumer on this same branch (`deep-research`, `deep-research-agent`, `sc-recommend`, `sc-reflect-protocol`, `sc-troubleshoot-protocol`) keeps the hyphen. The PR's premise ("hyphen does not resolve") is inverted; the rename silently breaks the Tavily‑first protocol in all 8 agents and splits the `agents/` directory into two incompatible conventions.

2. **The default POST‑reflect gate ships unvalidated on an unproven assumption.** `task-builder/SKILL.md` asserts as *"confirmed"* that a subagent can invoke the Skill tool and have it spawn its own reviewer ensemble — but the PR body itself says that exact (default) path is *"NOT yet validated end‑to‑end"*, and project memory records nested skill fan‑out from an Agent‑tool subagent degrading to a hand‑rolled fixture. No in‑file disclosure of the risk exists.

**The reflect‑enforcement contract work (1.5.1) is solid.** Contract version, EV‑1/EV‑2 gates, telemetry‑field removal, and instance‑level anti‑self‑confirmation are internally consistent across `SKILL.md` and both refs (verified on the PR branch — see *Audit*). The agent‑rename **scope discipline** is also excellent (uniform across all 8, zero non‑tavily edits) — the mechanics are clean; only the direction is wrong.

> ⚠️ **Review‑environment note:** Auggie's CLI passes indexed the **working tree** (checked out to `feat/recommend-minstar`), not the PR branch, and consequently emitted 6 false "diff not applied / contract still 1.5.0 / EV‑1 missing" criticals. These were **dropped** after grounding every claim against the PR‑branch blobs (`git show origin/feat/rf-harness-sync:…`). See *Audit → Dropped*.

---

## Findings

### 🟠 High (should fix before merge)

#### H1. Tavily MCP tool‑id rename inverts the resolving form — breaks Tavily‑first in all 8 rf‑* agents
- **File**: `src/superclaude/agents/rf-analyst.md:13-14` — and identically in `rf-assembler.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-task-builder.md`, `rf-task-executor.md`, `rf-task-researcher.md`, `rf-team-lead.md` (frontmatter `tools:` **and** body prose)
- **Category**: correctness / api‑contract · **Source**: both (Auggie + independent Claude pass) · **Confidence**: high · **in_diff**: true
- **Evidence**:
  ```diff
  -  - mcp__tavily__tavily-search    # PRIMARY web search (rare use; see body)
  -  - mcp__tavily__tavily-extract   # PRIMARY web content extraction (rare use)
  +  - mcp__tavily__tavily_search    # PRIMARY web search (rare use; see body)
  +  - mcp__tavily__tavily_extract   # PRIMARY web content extraction (rare use)
  ```
- **Why this matters**: The registered tool ids in this harness are `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` (**hyphen** — the Tavily MCP server names its tools with hyphens). The underscore form `mcp__tavily__tavily_search` does not match any registered tool, so it is dropped at agent spawn and each agent silently falls back to `WebSearch`/`WebFetch` — defeating the Tavily‑first protocol those same files mandate. On the PR branch, **5 other Tavily consumers keep the hyphen** (`deep-research.md:6`, `deep-research-agent.md:6`, `sc-recommend/SKILL.md:4`, `sc-reflect-protocol/SKILL.md:5`, `sc-troubleshoot-protocol/SKILL.md:4`), so this PR creates an in‑repo split: 8 agents on the non‑resolving underscore, everything else on the resolving hyphen. The change is the **opposite of its stated intent** (the PR claims it *fixes* resolution). This caps at High rather than Critical only because agents still spawn and degrade gracefully to web fallback (no crash, no data loss) — but it is the #1 must‑fix.
- **Recommendation**: Revert all 8 `rf-*` agents to `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` (frontmatter + every body reference). If a real resolution failure was observed, debug the MCP server/gateway version — not the tool‑id spec. Consider a repo‑wide test asserting a single canonical tavily id form across `agents/` + `skills/`.

#### H2. Default skill‑mode POST gate ships unvalidated and asserts an unproven nested‑skill‑fanout capability, with no in‑file disclosure
- **File**: `src/superclaude/skills/task-builder/SKILL.md:2370` (Rule 20, skill arm); same assertion at `:2218` and `:1668`
- **Category**: correctness / anti‑pattern (unvalidated default) · **Source**: both · **Confidence**: medium‑high · **in_diff**: true
- **Evidence** (line 2370):
  > "Nested‑subagent and Skill‑tool‑in‑subagent capability are confirmed: a subagent CAN invoke the Skill tool to run `sc-reflect-protocol` verbatim, and that skill spawns its own reviewer ensemble from inside the subagent."
- **Why this matters**: The **default** mode (`reflect_post_mode: skill`, i.e. `--cli` absent) makes the POST‑reflect gate's entire executor‑independence guarantee depend on this asserted capability. Yet the PR body states *"only the wrapper path has been session‑validated end‑to‑end; the skill‑default path is not yet validated,"* and project memory `reference_subagent_cannot_nest_skill_fanout.md` records Agent‑tool subagents **falling back to fixtures** when asked to run a fan‑out skill. If the assertion is wrong in practice, the default gate silently produces a hand‑rolled "verdict" — the exact self‑confirmation the contract exists to prevent — while the `--cli` wrapper path (a real `claude --print` subprocess) is immune. The "confirmed" wording inside the skill directly contradicts the "not yet validated" caveat that lives only in the PR body and never travels with the shipped skill.
- **Recommendation**: Do one of: (a) cite the specific run/artifact that re‑confirmed nested Skill‑tool fan‑out from an Agent‑tool subagent; or (b) soften the assertion to provisional and add an in‑SKILL disclosure on the default arm (e.g. *"the skill‑default POST path is not yet session‑validated end‑to‑end; prefer `--cli` for mission‑critical builds"*); or (c) make `--cli` the recommended/default POST mechanism until skill‑mode nesting is re‑proven. The risk must be visible in the skill, not just the PR description.

### 🟡 Medium

#### M1. "Fix A" inline‑execution directive has no test coverage and relies on best‑effort prose
- **File**: `src/superclaude/cli/reflect/runner.py:367-380`
- **Category**: tests / correctness · **Source**: both · **Confidence**: high (test gap), medium (efficacy) · **in_diff**: true
- **Evidence**: `_build_prompt()` now ends with `return command + inline_directive`, where `inline_directive` is a ~70‑word natural‑language instruction telling the headless `claude --print` agent to run the reflect top‑level. `tests/cli/reflect/` is **unchanged by this PR**; `test_no_nesting_guard.py` guards only the *wrapper* branch, not this directive. No test asserts the directive is present, well‑formed, or appended exactly once.
- **Why this matters**: The directive is the entire mechanism of "Fix A," but its efficacy depends on the receiving agent obeying prose — there is no structural enforcement at this layer. If the agent ignores it, the run still degrades to single‑reviewer (the failure EV‑1 now has to catch). Idempotence and empty/None‑prompt safety are fine (verified: `_build_prompt()` is called fresh per audit; `parts` is never empty), so the residual risk is purely the unverified directive + soft enforcement.
- **Recommendation**: Add a unit test asserting the directive is appended once and contains the load‑bearing phrases ("INLINE", "Do NOT delegate", "Wave 3/4"). Document that **EV‑1 (the on‑disk merge gate added in this same PR) is the real enforcement** and the prose directive is best‑effort defense‑in‑depth. Optionally extract the directive to a module‑level constant for testability (see Nits).

#### M2. CLI vs skill‑mode POST bifurcation increases maintenance / spec‑drift surface
- **File**: `src/superclaude/skills/task-builder/SKILL.md` (Rule 20 two arms; `reflect_post_mode` frontmatter at `:157`; CLI‑only keys `start_commit`/`executor_model_class`)
- **Category**: architecture / maintainability · **Source**: auggie‑only · **Confidence**: medium · **in_diff**: true
- **Why this matters**: One shared `reflect_post_mode` key now drives two mutually‑exclusive POST implementations with different frontmatter schemas, different O4 depth floors (CLI=deep, skill=standard), and two validator clauses. A future change to one arm can silently miss the other. The Validator‑branching requirement mitigates the *validation* half well, but there is no single place that enumerates the divergences.
- **Recommendation**: Add a compact "Mode Bifurcation Table" (Field/Rule · CLI · Skill‑only · Justification) and a validation rule binding the keys to the mode (e.g. *"`reflect_post_mode: cli` ⇒ `start_commit` + `executor_model_class` MUST be present; `skill` ⇒ MUST be absent"*).

### 🟢 Low

#### L1. Dangling cross‑reference: "§4.2 clause 4" does not exist
- **File**: `src/superclaude/skills/task-builder/SKILL.md:2276`
- **Category**: docs · **Confidence**: high · **in_diff**: true
- **Why**: "...the forwarded `--executor-model` is accepted‑and‑ignored **per §4.2 clause 4**" — but there is no `§4.2` heading in the file. The clauses it means live in the **unnumbered** note at `:2246-2248` (clause `(4)` of "CLI mode anti‑self‑confirmation"). A reader/validator following the anchor lands nowhere.
- **Recommendation**: Number that note as `§4.2` (or rename it) or change the reference to name the note literally ("clause (4) of the CLI‑mode anti‑self‑confirmation note").

#### L2. `spec_path` threading statements are not consistently mode‑qualified *(advisory)*
- **File**: `src/superclaude/skills/task-builder/SKILL.md` (input‑description / threading prose; ~`:19`, `:38` in the diff)
- **Category**: docs/consistency · **Source**: auggie‑only · **Confidence**: medium · **in_diff**: true
- **Why**: Blanket statements that `spec_path` is "threaded into the POST item" read as unconditional, but in CLI mode the wrapper resolves the base from `start_commit` frontmatter and does not take `--spec`. Not contradictory enough to block, but worth a one‑clause qualifier ("in skill‑only mode …; in CLI mode …"). *(Single‑source; not corroborated by the independent pass — listed as advisory.)*
- **Recommendation**: Add the mode qualifier to the two threading statements.

#### L3. Pre‑existing stale absolute‑line citations in reflection‑rubric.md *(not introduced by this PR)*
- **File**: `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:126,142,163`
- **Category**: docs · **Confidence**: high · **in_diff**: false (pre‑existing)
- **Why**: Citations like "spec §11.3 line 886/888/900/904" no longer match (§11.3 begins at `SKILL.md:1071` on this branch). The PR's rubric diff only touched the partition section, so this is incidental drift, not a PR defect.
- **Recommendation**: Replace hardcoded line numbers with section anchors in a follow‑up. Out of scope to block this PR.

### 💬 Nits

- **runner.py:372** — Extract `inline_directive` to a module‑level constant (e.g. `_INLINE_EXECUTION_DIRECTIVE`) so it is greppable and unit‑testable independently of `_build_prompt()`.
- **task-builder/SKILL.md:159** — The frontmatter comment uses "does NOT class‑exclude"; prefer positive framing ("keeps the executor class in the reviewer pool") to avoid implying an exclusion mechanism still exists.

---

## Architectural / Cross‑Cutting Observations

- **Tavily convention split (H1).** After this PR the `agents/` directory contains two incompatible Tavily id conventions. Even setting aside which form resolves, having both is a latent footgun; a single canonical form should be enforced repo‑wide.
- **POST‑gate bifurcation (M2).** The `--cli` toggle is a reasonable design, but the unvalidated default arm (H2) + the doubled spec surface (M2) mean the *validated* path is the opt‑in one. Until skill‑mode nesting is proven, the safer default is the wrapper.
- **Contract 1.5.1 is the strong part of this PR.** EV‑1 (on‑disk adversarial‑merge gate), EV‑2 (merge_method enum guard), and the instance‑level anti‑self‑confirmation model are coherent and consistently expressed across `SKILL.md` + both refs. The telemetry‑field removal is genuinely non‑breaking (no `src/` or `tests/` consumers).

---

## Audit

- **Auggie chunks**: 4 (code, reflect, rfskills, agents) — succeeded: 4, retried: 0, skipped: 0. Durations 106–156s. Run concurrently with `--wait-for-indexing --max-turns 24`.
- **Independent Claude‑side pass**: `auggie-reviewer` agent (deep cross‑check) — corroborated H1, H2, M1, L1 independently via `git show origin/feat/rf-harness-sync:` (correct branch content).
- **Findings dropped during grounding: 9** —
  - **6× reflect‑chunk false criticals/highs** ("diff not applied", "contract still 1.5.0", "EV‑1 missing", "telemetry fields still present", "§7.1 retains class‑exclusion"): **wrong‑tree artifacts.** Auggie indexed the working tree (`feat/recommend-minstar`), not the PR branch. Verified false against PR‑branch blobs: `contract_version: "1.5.1"` consistent at `SKILL.md:669/672/813/1645/1776`; removed fields appear only in negative mentions; EV‑1 at `:661`; EV‑2 at `:756/1610`; instance‑level at `:594/600/1089`.
  - **1× rfskills "non‑existent contract 1.5.1"**: false — 1.5.1 present on branch.
  - **1× rfskills cross‑cutting "instance‑level claim needs cross‑skill alignment"**: resolved — sc‑reflect 1.5.1 implements it.
  - **1× code‑chunk "directive shows in --print‑command dry‑run"**: low‑value (the printed prompt legitimately includes the directive); dropped.
- **Grounding verification commands**: `git show origin/feat/rf-harness-sync:<path> | grep -n …` for every retained finding's file:line; live tool‑surface check for the Tavily id (registered functions are `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract`).
- **Verified CLEAN (credited)**: contract 1.5.1 consistency; telemetry‑field removal non‑breaking; EV‑1/EV‑2 internal consistency; instance‑level consistency across all 3 reflect files; §7.1 anchor resolves; agent‑rename scope discipline (uniform, zero non‑tavily edits); runner.py idempotence + empty/None‑prompt safety; existing runner tests survive the append.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 2 medium: 2 low: 3 nit: 2
dropped: 9
auggie_chunks: 4
-->
