# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (OURS, `variant-1-original.md`)
- Incorporating strengths from: Variant 2 (CLAY, `variant-2-original.md`) and from the debate transcript (advocate proposals verified by the orchestrator)
- Planned changes: 6
- Risk level: Low to Medium (overall Low; Change 5 is Medium)

## Planned Changes

### Change 1: Add the hand-back loop bounds, old-worker-final rule and idempotent re-plan (from Variant 2)
- **Source**: Variant 2, Mechanism bullets 3-4 and Cited facts 6-8 (D:612-614, D:1076-1080)
- **Target**: Base, new section "Loop bounds under any start rule", inserted after "Mechanism" (insert)
- **Rationale**: C-006, Variant 2 wins at 86% (both advocates); U-005 and U-006 unique contributions; the bounds hold whether or not a person re-approves each round (V2 advocate hybrid item 1-3). The base has only `HANDBACK_MAX` and no loop mechanics (rubric R3 NOT MET for V1).
- **Integration point**: Four bullets: (a) `handback` decides in order `no_remaining`, `cap` (`HANDBACK_MAX` = 3, at most 4 rounds, "this design's value, not measured"), `no_progress` (same remaining list as last round); (b) round n+1 starts only when the old worker's `worker_done` is received for the active Task and Dispatch (D:614); (c) the re-plan writes marker `<!-- sc:issue:replan round=<n> -->` so a rerun writes nothing twice, and `--remaining` replaces only `## Fix approach` and `## Test plan` (D:1078-1080); (d) restart: every step read-then-write, a restart resumes at the recorded step (D:620). Mark `--remaining` done-item fidelity UNVERIFIED (U60, D:1081).
- **Risk**: Low, additive; the facts were verified against D:612-614 by both advocates.

### Change 2: Keep `quick` as the default but add the per-repo `plan_depth` override (from Variant 2, goal G6)
- **Source**: Variant 2, Claim 1 and Mechanism bullet 1 (D:60, D:722-724)
- **Target**: Base, Claim 1 and "What it costs" (replace one sentence, append one)
- **Rationale**: C-005 Hybrid at 60%; U-004; V1 advocate and V2 advocate both state the key lets a repo opt in to `standard` or `deep` while the default stays `quick`, which keeps Clay's lever without the unverified `plan_tier` table (C-002, 72%).
- **Integration point**: Claim 1 becomes: default `quick`; a per-repo `plan_depth` of `standard` or `deep` is allowed; a plain key passed straight to `--depth`, no tier table. Costs gains: a `deep` repo setting multiplies up to 4 times per issue because the wave-2 re-plan passes the same depth (D:618); no cost baseline exists (D12).
- **Risk**: Low; configuration only.

### Change 3: Add the start re-check requirement (from Variant 2's own finding)
- **Source**: Variant 2, Cited fact 9 (D01 MR-1; `orchestrator.md:488`)
- **Target**: Base, Mechanism bullet 3 (append)
- **Rationale**: U-007; the check at the moment of start must repeat the approval, not only `hold:backlog` and `plan_check` (D01 item 3). It makes OD-2 option (a) testable.
- **Integration point**: One sentence plus a test statement: removing the approval between wake and start refuses the start.
- **Risk**: Low.

### Change 4: Correct the base's wrong or loose citations (base weakness)
- **Source**: Orchestrator spot-check recorded in `base-selection.md` (Correctness, V1) and the reviewer note in `diff-analysis.md`
- **Target**: Base, Cited facts 2 and 4
- **Rationale**: Rubric K1 NOT MET for V1. `predicates.py` in snapshot `pr-a` has 219 lines, so the lines 249-259 must be cited as master's `src/superclaude/cli/issue_watch/predicates.py:249-259` (`unchanged_since`, body edit after approval returns `edited_after_approval`; verified in master, 312 lines). D12 item 6 defers a higher tier floor at create; it is not a source for the `--plan` default.
- **Integration point**: Fact 4 path changed to master; fact 2 re-labelled "related cost-baseline deferral at create time, not a direct source for OD-1"; the direct source for OD-1 stays D15 G-2.
- **Risk**: Low.

### Change 5: Say how a waiting hand-back leaves the in-flight count, with its limits (from the debate)
- **Source**: Debate transcript, both advocates' proposal (status `escalated`, step `handback_awaiting_approval(body_sha)`), checked against `route.py:393-399`, D:605 and D:608
- **Target**: Base, Claim 3 and Mechanism bullet 4 (replace and extend)
- **Rationale**: C-004 Variant 1 at 76%, X-002 at 55%; the base says "exclude the waiting step" but not how; both advocates converge on the same carrier. D:605 already states that `escalated` means the issue leaves the places in flight.
- **Integration point**: Text: `route.in_flight` skips any readable file whose status is not `in_progress` (`route.py:399`), so a waiting step written as status `escalated` with step `handback_awaiting_approval` is not counted and returns to counting when set back to `in_progress`. Open points (UNVERIFIED): D:616 says "Nothing is escalated for a hand-back", so the use of `escalated` is an extension that needs its row-9, `stalled` and `--take` side effects checked (D:608, D:617); the flip back can overshoot `max_in_flight` if new work took the place (allow one-slot overshoot or require a free place); which component runs the wake path (C-INV-2) is not decided; whether restored WC-17 can serve as the round-2 gate is UNVERIFIED.
- **Risk**: Medium; it touches state semantics and the claim rests on a reading of the design, not on built code.

### Change 6: Record the shared assumptions and the Clay concessions that the debate surfaced
- **Source**: Diff analysis A-001 to A-004; debate transcript concessions
- **Target**: Base, "What it risks" (append)
- **Rationale**: A-001 to A-004 all QUALIFY favoring V1, so the base should state them: no measurement of plan quality or cost per depth (A-001); hand-backs assumed rare (A-002); login-based approval is weak against an agent on the same login (A-003, accepted risk L-1); the counting code lives in PR 686 whose adaptation is open (A-004).
- **Integration point**: Four short risk lines with an impact each (this also lifts rubric R1 and R2 weaknesses of V1: each risk gets a stated impact and one mitigation).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001, X-001 | `plan_tier` default `tier1b`, implying `deep` | Rests on a table not on master (UNVERIFIED) and on no cost baseline; both advocates side with `quick` (66%); the V2 advocate does not defend `deep` |
| C-002 | `plan_tier` mapped to `--depth` by a table in `refs/intake.md` (PR P) | D:726 passes a tier name where `--depth` takes quick/standard/deep; a plain `plan_depth` key needs no table (72%) |
| C-003, X-003 | Round 2 starts with no new approval (wave 2 re-plan, same waves) | A re-plan voids the approval (`predicates.py:249-259`); Clay's text has no round-2 gate and the V2 advocate concedes it (78%, 79%); option (b) stays only as the owner's cheaper alternative |
| C-004, X-002 | Hand-back stays `in_progress` and counted; no waiting step | Fine for live workers; with a person step it holds a place while nobody works (C-INV-1); Clay's own `escalated` already frees a place (D:605) (76%, 55%) |
| C-007 | No wake path needed | True only without a person step; `cycle.py:993-994` shows the poll never wakes an acknowledged entry (80%) |
| S-001, S-002 | (no difference worth merging) | Identical headings; evidence type differs but both sets were verified |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | A mis-stated bound would mislead the spec | Remove the inserted section |
| 2 | Low | Reader thinks `deep` is the default | Revert Claim 1 sentence |
| 3 | Low | Duplicate of D01 item 3 | Remove the sentence |
| 4 | Low | Citation stays wrong | Revert to the original text |
| 5 | Medium | Spec adopts a state carrier with side effects nobody checked | Replace with "carrier undecided; exclude waiting step from the count" |
| 6 | Low | Overstates the unknowns | Remove appended lines |

## Review Status
- [x] Auto-approved (default; unattended mode)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-20 (UTC)
