<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (option B document, skeleton only; chosen by score and the edge-case floor, not by the debate verdict) -->
<!-- Merge date: 2026-11-07 -->

# D-P2-25: how release-split Part 3 behaves under --unattended

<!-- Source: Base (original, modified) — title and scope reworded to a decision record per Change #1; the shared "How to judge" brief is dropped per Change #7 -->

## Decision

<!-- Source: Variant 1, first paragraph — merged per Change #1 (replaces the base mechanism paragraph; base coverage structure kept) -->
Winner: option A (inline)

Under `--unattended`, release-split Part 3 writes `release-1-spec.md`, `release-2-spec.md` and `boundary-rationale.md` itself with the Write tool (for no split, `release-spec-validated.md`). It makes no nested command call. The text for this is already in the working tree: `src/superclaude/skills/sc-release-split-protocol/SKILL.md:281` and `src/superclaude/commands/release-split.md:119`. The three fixed outputs are listed at `SKILL.md:312-320`. release-split's nested list stays brainstorm and adversarial (`tests/skills/test_worker_contract.py:1391`, `:1466`, `:482`). Part 4 also stays inline (`SKILL.md:331`).

Debate result: option A wins 9 of 14 points, option B wins 1 (C-001), and 4 are unresolved but lean A. Both advocates recommended A on their own (`debate-transcript.md`, Scoring Matrix).

## Why option A

<!-- Source: Variant 1, Claimed strengths (U-001, S-002, S-003) — merged per Change #2 -->
- The text is already true. No file needs a further edit (see "Edits required"). Debate S-003, 92%.
- The tests already match. The nested list is pinned at two entries (`test_worker_contract.py:1391`, `:1466`) and in `UNATTENDED_EXPECT` (`:482`). Debate S-002, 85%.
- The path is deterministic. Part 3 says "Select the appropriate command" (`SKILL.md:286`), which is a judgment step; inline writing needs no such choice. Debate A-002, 70%.
- It reuses an existing row: "Part 3 command unavailable: produce specs inline using Write tool" (`SKILL.md:439`).
- Section 2.1 does not oblige a call. It governs "a command that invokes another `/sc:` command" (`WORKER-CONTRACT.md:24`). Not invoking is not a breach. Debate C-004 and X-001 lean A, 55%.
- The step-by-step content rules (scope, validation, planning gate, traceability) are already in Part 3 itself (`SKILL.md:287-303`).

## Why not option B

<!-- Source: Debate transcript points C-002, C-003, C-005, C-006, X-002 (both advocates) — merged per Change #3 -->
- Wrong deliverable (C-002, 95%). `/sc:workflow` writes a plan package, not a spec (`workflow.md:80`). `/sc:tasklist` is a roadmap-to-tasklist generator (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:3`), and `SKILL.md:279` says not to use it unless the proposal says so. `/sc:design` writes one file per call; three outputs would need several calls.
- Different report-directory flag (C-003, 85%). design and workflow take `--report-dir` only (`design.md:96`, `workflow.md:71`); release-split's idiom is `--unattended --output` (`release-split.md:119`).
- Deeper nesting (C-005, 93%). workflow adds a reflect call (`workflow.md:75`). tasklist adds reflect and `sc:task` (`tasklist.md:114`), and `sc:task` can execute work.
- A late `blocked` (X-002, 92%). tasklist has two halt-as-blocked gates (`tasklist.md:113`). A nested `blocked` stops the caller as `blocked` (`WORKER-CONTRACT.md:25`), after Parts 1 and 2 are already paid for.
- <!-- Source: Base (original, modified) — staging sentence replaced per Change #4; the base and Variant 1 both said the callees "stage files", which Pass 2 finding R1 showed to be wrong -->
  Package location, not staging (C-006, 90%). `/sc:workflow` does not stage `.dev/tasks` and leaves that to the coordinator (`workflow.md:76`). `/sc:tasklist` stages nothing (`tasklist.md:115`). The real cost is that the workflow package is written outside `nested/workflow-<n>/`, so release-split would have to list it in `artifacts`.
- Size. Option B edits the spec row, `EXPECTED_NESTING` in two places, `UNATTENDED_EXPECT`, the command section and the skill, and needs new nested-call tests. Debate S-003.

A narrowed form of B (call `/sc:design` only) was considered and is not preferred. `/sc:design` is a generic architecture command and carries none of Part 3's release rules (`SKILL.md:287-303`), so the rules would still have to be handed to it. It still adds a nested entry, pin changes and spec edits, and needs at least three calls (`debate-transcript.md`, facilitator note).

## What option A gives up

<!-- Source: Variant 2, Claimed strengths (U-002, U-003) and Variant 1, Claimed weakness; debate point C-001 — merged per Change #5 -->
- Callee structure and checks (C-001, B wins, 70%). The specs are authored without a callee's own steps. Both advocates discount the gain (A-003, 65%).
- One contract per spec (U-002). With B the coordinator would get a separate nested contract for each spec. With A it gets one release-split contract.
- design's guard (U-003). `/sc:design` under `--unattended` changes no existing architecture (`design.md:98`). The inline path has no such rule.
- Output quality may be lower. This is claimed by Variant 1 and is unmeasured.
- What remains as protection: the traceability rule, "no orphan scope, no invented scope" (`SKILL.md:303`), and the inline fidelity verification in Part 4 (`SKILL.md:331`). Both options share these.

## Edits required

<!-- Source: Base (original, modified) — new section from rubric criteria L5, E1, E4 per Change #6; neither variant had it -->
None. With A winning, no change is needed in `SKILL.md`, `release-split.md`, `tests/skills/test_worker_contract.py` or the spec row.

Optional wording polish, not recommended under scope discipline:
- `SKILL.md:281` says "the specs", while Part 3 also writes `boundary-rationale.md` and, for no split, `release-spec-validated.md`. Outputs at `SKILL.md:312-320` already cover them, so the gap is wording only.
- `SKILL.md:281` calls the Error Handling row a "fallback", but that row is for "command unavailable" (`SKILL.md:439`) and here the callee is available. Debate S-004, wording only.

## Open points

<!-- Source: Debate transcript, Convergence Assessment; diff-analysis Metadata — merged per Change #7 -->
- Status: NOT_CONVERGED, 71.4% against the 80% threshold (10 of 14 points). Depth was quick, so only Round 1 ran.
- Unresolved, all leaning A: S-001 (55%), S-004 (50%), C-004 (55%), X-001 (55%). No advocate argued that B wins any of them.
- UNVERIFIED: how this interacts with D-P2-24 and D-P2-13. Their option files were not read.
- UNVERIFIED: the claim that inline output quality is lower. Nothing in the evidence measures it.
