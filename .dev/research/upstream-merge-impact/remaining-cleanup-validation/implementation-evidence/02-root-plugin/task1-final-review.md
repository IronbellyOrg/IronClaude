# Research: Root-plugin compatibility contract gate

- **Topic type:** Independent spec-compliance review
- **Scope:** Revised Task 1
- **Status:** FAIL
- **Closed verdict:** `missing`
- **Persistence:** Independent reviewer return persisted by parent before consumption.
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

## Findings

FAIL. Closed verdict: missing. Task 1 has one unrecorded required-resource compatibility gap; product preservation and loader mapping pass independently.

- Task1.AC1: compliant. Contract pins 26 command edit paths and lookup rules at `plugin-contract.json:2846-2874` and original/corrected manifest hashes at `:2880-2884`. Independent read-only recomputation verified all 2,260 protected hashes (excluding the explicitly revised manifest), all 22 fixture candidates byte-identical to their named sources, and the exact authorized manifest deletion.
- Task1.AC2: missing (IMPORTANT). The contract maps both audit tiers to confidence-calibrator and declares STATIC_TRACE_COMPLETE with blockers=[] at `plugin-contract.json:2830-2845`, while `closure-research.md:15,56-58` treats the calibration edge as supplied without recording its incompatible input/scoring contract. Actual candidate `src/superclaude/agents/confidence-calibrator.md:48,61-70` requires escalation-rubric.md, six named troubleshooting dimensions, a Runtime-check cross-tab, a gated-minimum formula, and verdict-direction caps. Actual supplied `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:9-13` defines five different reflection dimensions and their arithmetic mean. Passing that path does not resolve the explicit conflicting agent instructions. The closure needs to record this required calibration compatibility blocker and a scoped resolution; this is a source-level mismatch, not a demand for Task 4 runtime proof or an assertion that all runtime attempts fail.
- Task1.AC3: compliant. `loader-candidates-session.stdout.txt:1,4` contains the actual external-cwd native inventory, qualified command/skill/agent names, empty MCP list and successful terminal result. Candidate and external probe records show isolated HOME/config and strict empty MCP; the fixture has no user framework settings/resources. Built-ins were present but supplied no missing audit dependency because this was inventory-only.
- Task1.AC4: compliant. Actual git diff from 2f98141c36d9599c40d719b63aca7d70af8ac3d5 is exactly the empty-homepage-line deletion; `preservation-revised.json:2-15` agrees with independent hashes. No Task 2 command edits or Task 3 product additions occurred.
- extra_scope=[]; misunderstood=[].

Reviewer paths in this persisted return are repository-relative for source files and evidence-directory-relative for evidence files; findings are otherwise preserved from the independent reviewer.

## Gaps

One open gap: required calibration resource compatibility is not resolved or recorded as blocking. Task 3 delivery and Task 4 audit runs remain deliberately unbuilt/unverified and are not additional Task 1 findings. The two user-approved revisions were applied as written scope, not treated as waivers.

## Key Takeaways

Keep Task 1 blocked until the calibration mismatch is explicitly resolved within authorized adaptation scope, or recorded for a revised written scope. Do not silently replace independent calibration with inline scoring. No files written, no retry/troubleshoot directories read, no suite or native runtime rerun.

| Status | Result |
|---|---|
| DONE | Independent Task 1 review and preservation recomputation completed. |
| NEXT | Persist this finding before consumption and resolve the calibration contract gap. |
