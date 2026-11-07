# Diff Analysis: Decision-Option Comparison (D-P2-25)

## Metadata
- Generated: 2026-11-07
- Variants compared: 2 (Variant A = option A "inline", Variant B = option B "pass the flag to the Part 3 callees")
- Total differences found: 15
- Categories: structural (4), content (6), contradictions (2), unique (3), shared assumptions (3)
- Evidence read in the working tree (uncommitted P2 edits): `src/superclaude/skills/sc-release-split-protocol/SKILL.md`, `src/superclaude/commands/release-split.md`, `src/superclaude/commands/{design,workflow,tasklist}.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, `tests/skills/test_worker_contract.py`.
- Not read (UNVERIFIED, not used to decide): the D-P2-24 and D-P2-13 option files that Variant B says it interacts with.

## Ground facts both variants rest on (verified)
- The working tree already carries Variant A's text: `SKILL.md:281` ("Under `--unattended`, Part 3 produces the specs inline with the Write tool (the fallback of the Error Handling table) and makes no nested command call.") and `release-split.md:119` ("Part 3 writes the specs inline and Part 4 uses inline verification, so neither makes a nested call."). The Error Handling row is `SKILL.md:439`.
- Part 3's required deliverables are three fixed paths: `<output>/release-1-spec.md`, `<output>/release-2-spec.md`, `<output>/boundary-rationale.md` (or `<output>/release-spec-validated.md` for no split) (`SKILL.md:312-320`). Steps 3-6 of the Split Approved instructions (`SKILL.md:287-303`) already say what content each file must carry, with traceability.
- Pinned tests assert Variant A's nesting: `EXPECTED_NESTING["release-split"] == ["brainstorm", "adversarial"]` at `tests/skills/test_worker_contract.py:1391` and again, hard-coded as "the spec nesting", at `:1466`; `UNATTENDED_EXPECT["release-split"]["nested"]` at `:482`.
- All three Part 3 callees have an `## Unattended mode` section: design (`design.md:91-100`), workflow (`workflow.md:66-76`), tasklist (`tasklist.md:105-115`).

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Where Part 3's specs are authored under `--unattended` | Inline in the release-split worker with the Write tool; no callee | Delegated to `/sc:design`, `/sc:workflow` or `/sc:tasklist` workers, each in `<report-dir>/nested/<command>-<n>/` | High |
| S-002 | Membership of release-split's nested list | Unchanged: brainstorm, adversarial (2 commands) | Grows to brainstorm, adversarial, design, workflow, tasklist (5 commands) | Medium |
| S-003 | Files touched by the decision | Zero further edits: the SKILL and command sentences and both test pins already match | Spec row, `EXPECTED_NESTING` (two places), `UNATTENDED_EXPECT`, the command section, the skill, plus new nested-call tests | High |
| S-004 | Naming of the mechanism | "the fallback of the Error Handling table" for a callee that is available but not called | "nested-result rule" reused for three more callees | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Structure and checks of the authored specs | Authored directly from the Part 3 instructions (`SKILL.md:283-303`); claims quality may be lower | Keeps each callee's structure and checks (design's no-architecture-change rule, workflow's reflect step, tasklist's validation report) | Medium |
| C-002 | Fit of each callee to the required deliverable | The three fixed output files do not depend on any callee | `/sc:design` writes one file passed to its own `--output`; `/sc:workflow` writes a plan package under `.dev/tasks/to-do/<id>/`, not a spec; `/sc:tasklist` needs a roadmap input and writes a tasklist bundle. Neither of the last two produces `release-N-spec.md` | High |
| C-003 | Report-directory flag for the nested call | Not needed | `/sc:design` and `/sc:workflow` take `--report-dir` only (`design.md:96`, `workflow.md:71`); release-split's existing nested idiom is `--unattended --output <dir>`, so the new calls need a different idiom | Medium |
| C-004 | Reading of spec section 2.1 | The nested propagation rule applies to a command that does invoke another command; it does not oblige a command to invoke every accepting command | "Follows 2.1 literally": the flag must be passed to callees that accept it | Medium |
| C-005 | Depth and spread of nesting under one worker | Depth stays at the current two levels (brainstorm, adversarial) | Adds release-split -> workflow -> reflect (-> adversarial, workflow) and release-split -> tasklist -> {reflect, task} (-> impact, troubleshoot -> ...); `/sc:task` may execute work | High |
| C-006 | Staging and package writes (WC-9) | Writes only the three spec files and the report; nothing under `.dev/tasks` | `/sc:workflow` creates `.dev/tasks/to-do/<id>/` and defers staging to the coordinator (`workflow.md:76`); the package path lies outside `nested/workflow-<n>/` and has to be listed in `artifacts` | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Does section 2.1 require the nested call? | 2.1 says "a command that invokes another command ... passes `--unattended` when the invoked command accepts it" (`WORKER-CONTRACT.md:24`); not invoking is not a breach | "Follows spec section 2.1 literally" implies the call must be made | Medium |
| X-002 | What a nested `blocked` does to release-split | No Part 3 nested contract exists, so no Part 3 `blocked` path is added | Nested `blocked` stops release-split as `blocked` (`WORKER-CONTRACT.md:25`); `/sc:tasklist` has two HALT-as-blocked gates (`tasklist.md:113`) that would surface as release-split blocked at Part 3, after Parts 1-2 are paid for | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Reuses an existing, tested fallback row (`SKILL.md:439`); deterministic: no choice among three commands at run time | High |
| U-002 | B | Per-callee nested contracts give the coordinator a separate status and report for each spec | Medium |
| U-003 | B | Keeps `/sc:design`'s guardrail that an unattended run "changes no existing architecture" and writes no implementation code (`design.md:98`) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | Part 3's deliverable under `--unattended` is exactly the three spec files plus the report (STATED in `SKILL.md:312-316`; not promoted) | Both options leave the Outputs list unchanged | Low | STATED |
| A-002 | Choosing among design, workflow and tasklist is a mechanical choice a worker can make without a person (UNSTATED: `SKILL.md:286` says "Select the appropriate command based on the proposal's recommended next step", a judgment step; the table at `SKILL.md:272-277` is keyed by verdicts the worker cannot always read off) | Both options speak of "Part 3 callees" as a settled set | Medium | UNSTATED, promoted |
| A-003 | A command's quality checks are what protect Part 3 output, and `/sc:design` under `--unattended` has a validation rule that the inline path lacks (UNSTATED: the design section lists "no gate" and a no-architecture-change guard, but no spec-quality validation rule; the inline path is bound by Part 3's traceability rule at `SKILL.md:303` and Part 4 fidelity verification) | Both options treat "structure and checks" as the quality variable | Medium | UNSTATED, promoted |

## Summary
- Total structural differences: 4
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-001, S-003, C-002, C-005, X-002
- Variants-too-similar check: not triggered (differences far above 10%).

## Taxonomy tags (AD-5)

| Point | Level | Signal |
|-------|-------|--------|
| S-004 | L1 surface | naming, wording |
| S-001, S-002, S-003, C-001, C-002, C-003, C-004, C-005, X-001 | L2 structural | component, interface, dependency, organization |
| C-006, X-002, A-002, A-003 | L3 state mechanics | guard, state transition, validation rule |
