# Merged Tier-2 Verdict — UC-1 pre-execution coverage audit

<!-- Provenance: produced by /sc:adversarial (Mode A), base Variant 1 (analyzer/sonnet); merged 2026-11-13T00:20Z -->
<!-- Contributions: V2 (qa) verification posture + attribution/inclusion distinction; V3 (refactorer) list-style, test-naming, plugin advisory; Round 2.5 probe INV-002/003/006 corrections -->

## Mode

Plain UC-1 plan-fidelity findings. No UC-2 deviation classes (Authorized/Necessary/Drift/Regression) apply: this is a pre-execution audit of a plan against its spec; no executor work exists to deviate. (Unanimous, Round 1; V2 withdrew its own Drift 2 counts; a false Drift label could trigger headless AUTO-FIX remediation per the reflect skill's remediation routing.)

## Coverage

Union requirement set (parsed 0, inferred 3): **3/3 covered** → coverage_pct_union 1.0, unmapped union [].
- INF-002 ten-file list: verified against issue-summary.md:24 **outside the grounding root** (main checkout /home/coder/workspaces/IronClaude/.dev/issues/504/issue-summary.md; absent from this worktree); the tasklist enumerates all ten files inline and the enumeration matches exactly.
- Every INF row maps to concrete tasklist tasks (Tasks 1-11) with line-grounded citations.

## Findings

**MF-1 (MEDIUM) — False wording attribution in Constraints (plan:19).**
The tasklist's Constraints assert the mandated rule text "is the wording of the rule in" reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md. Direct reads of all four show every one gates codegraph use on `index_state: fresh` + `projectPath` only; none mentions `checked_at`, `worktree_root`, "callees and impact", or "say so in your reply" (troubleshoot-analyst.md:27; reflect-reviewer.md:64; reuse-auditor.md:50; auggie-reviewer.md:79). The composed text is a NEW, stricter rule — consistent with the spec's own parenthetical (source.md:1) but falsely attributed to precedent. The error is the attribution, not the inclusion of the extra fields (V2). The four references also carry an explicit returns-nothing fallback in 3 of 4 files (reflect-reviewer.md:64, troubleshoot-analyst.md:27, auggie-reviewer.md:79; reuse-auditor.md:50 gates without naming empty results), which the composed sentence omits; 14 agent files now carry two freshness-gate families under one "shared" label (probe correction INV-002/003). Severity rationale: false provenance in the exact sentence executors paste into ten files, plus incoherence between claim and sources — NOT demonstrated behavioral loss (probe INV-006: the rule's own reference target, ~/.claude/CODEGRAPH.md:32,70,76, preserves the effective native-floor fallback on empty results).
Citations: TASK-WF-addTheSharedCode-20261111-193909.md:19 (plan); source.md:1 (spec); the four agent files (source).

**MF-2 (LOW) — Acceptance criteria cannot enforce the rule they gate (plan:31,38,45,52,59,66,73,80,87,94).**
Tasks 1-10 ACs check grep counts plus diff shape and absence of a tools line, but contain no exact-text assertion: text materially different from Constraints, or missing `checked_at`/`worktree_root`/the fallback sentence, still passes. (Probe correction INV-001: "only grep counts" overstates — the diff-shape and tools-line constraints do real work; the surviving gap is the missing exact-text check.) Task 11's `make verify-sync` compares src to .claude mirrors, not against the Constraints sentence. Also folds V3 F4: Task 11 says "find the agent-file tests with grep" instead of naming them, so the pass condition depends on which tests the executor picks (plan:102,105).

**MF-3 (LOW) — Spec self-contradiction resolved silently (source.md:1; plan:19).**
The spec simultaneously says "following the wording in [four agents]" and requires `checked_at`/`worktree_root`, which those agents lack. The tasklist adopts the stricter reading without recording the choice; the false attribution (MF-1) is the symptom, this is the cause. Remediation is a one-line recorded choice, not a text patch.

**MF-4 (LOW) — Placement instruction looser than the files (plan:28; system-architect.md:30-35).**
Tasks 1-8,10 say "one bullet at the end of the `## Key Actions` list", but every target list is numbered with bold labels; the executor had to invent the number and the "**Use Codegraph Safely**" label. The AC cannot distinguish a correct item from a stray bullet. Tasks 9 and 10 (self-review's own list style; technical-writer's code-fact-only variant) are correctly specified.

## Advisory (non-finding)

**ADV-1 — Plugin mirror divergence (pre-existing, out of scope).** plugins/superclaude/agents/ holds 22 tracked files including copies of all ten targets; zero contain `index_state`; no make target syncs them; `make build-plugin` ships that folder verbatim into dist (scripts/build_superclaude_plugin.py:76-77). The spec never names plugins/; the four reference agents are absent from the mirror entirely, so the gap predates this plan. Action: decide whether plugins/superclaude/agents must mirror src/superclaude/agents; if yes, a separate task adds the rule there.

## Verdict

The tasklist covers 100% of the spec's requirement-bearing content with accurate file targeting and sound structural constraints. It is executable as written. The four findings are plan-fidelity defects (one medium, three low) whose fixes are documentation edits to the tasklist itself, not blockers to execution. Recommended before execution: correct the attribution sentence (MF-1), add an exact-text check (`grep -F` of the Constraints sentence, or `grep -c checked_at`/`worktree_root` floor) to Tasks 1-10 ACs (MF-2), record the wording choice (MF-3); fix the list-style wording while editing (MF-4). No --remediate is required for these to be actionable; they are stated here as the merged Tier-2 verdict.
