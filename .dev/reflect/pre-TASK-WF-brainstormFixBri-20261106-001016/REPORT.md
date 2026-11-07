```yaml
contract_version: 1.8.0
status: partial   # one citation dropped by the validator, and the debate's invariant gate is blocked (INV-020)
mode: pre
tier_reached: 2
confidence_calibrated: 0.84   # blind score of the Tier 1 card; the merged card was not re-scored (reviewer cards scored 0.85, 0.82, 0.82)
citations_total: 45           # distinct file:line tokens; 38 were in the draft the validator checked, 7 supporting lines were added afterwards at its request
citations_revalidated: 38     # the validator re-read all 38 (it also read the 7 added lines while naming them, but they got no second pass)
citations_dropped: 1          # spec:286 under F-7; see "Dropped by validation"
citations_dropped_extrapolated: 1
citations_inferred: 2
citation_budget_policy: sampled
coverage_degraded: null
```

# Pre-execution reflection: brainstorm nested-analyze wording fix

Spec (brief): `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/source.md`
Tasklist: `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md` (7 tasks, 4 phases)
Paths below are relative to the repository root. `plan:N` means line N of the tasklist above and `source.md:N` means line N of the brief. The full merged result is `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/adversarial/merged-verdict.yaml`.

## Verdict

The plan covers all five items of the brief and its constraints, but it is not ready for `/sc:implement` as written. Three fixes come first:

1. Task 6's live-check sentence decides whether the nested folder must exist by the recorded tier, and that is wrong.
2. Task 7's third acceptance bullet cannot pass on today's tree.
3. Two parts of the owner's rule (that no nested contract is listed, and that the nested folder exists only when `/sc:analyze` ran) are pinned by no planned test.

Fourteen smaller wording and coverage fixes follow, and one open conflict (research enrichment from phase P2) is outside this plan and needs the owner.

## How the review ran

- Tier 1 scored 0.84 in a blind re-grade, below the 0.85 floor, so the tier rule escalated to Tier 2 (rule 6).
- Three reviewers (sonnet, the haiku slot which resolves to glm-5.3, and opus) audited the plan. Their cards scored 0.85, 0.82 and 0.82 in blind re-grades run on opus. Every available model class was already used by a reviewer, so calibrator diversity is degraded. The model that wrote the plan could not be identified, so the guard against a reviewer reviewing its own work is weakened.
- A three-advocate debate over 24 differing points reached full agreement (23 unanimous, 1 by majority). Variant 2 was the base card (score 0.815, against 0.783 and 0.725).
- The invariant probe found one HIGH unaddressed item (INV-020). The skill's gate treats that as blocking, so the debate result is partial even though the points agree.

## Coverage matrix

| Brief item | Plan task(s) | Result |
|---|---|---|
| 1. Say the fallback tier writes no nested folder, in skill, command file and routing ref (`source.md:6`) | Tasks 1, 2, 3 | matched, wording needs the fixes below |
| 2. Pin the wording in tests (`source.md:7`) | Tasks 4, 5 | matched, pins are weaker than they look (F-3, F-4, F-5) |
| 3. Sync dev copies, check the plugin mirror (`source.md:8`) | Task 7, plan constraints | matched |
| 4. Record the corrected live-check wording (`source.md:9`) | Task 6 | matched, wording is wrong (F-1) |
| 5. Run affected tests and lint (`source.md:10`) | Task 7 | matched, test set incomplete (F-6) |

Parsed requirement rows: 5, matched 5 (`coverage_pct: 1.0`). Inferred rows: 5, all matched (`coverage_pct_union: 1.0`). Matched means a task or constraint addresses the row, not that its wording is right.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "no commit, push or PR" | source.md:12 | matched: plan Constraints (plan:24) |
| INF-002 | "UV only" | source.md:12 | matched: plan Constraints, every Python command in Tasks 1 to 7 |
| INF-003 | "edits only in the files the plan names" | source.md:12 | matched: plan Constraints (plan:20) |
| INF-004 | "the archived P1 packages under .dev/tasks/done/ stay untouched" | source.md:12 | matched: plan Constraints and Task 7 third bullet |
| INF-005 | "the skill must say that the auggie tier and the fallback_1 tier (codegraph/Grep) write no nested folder" | source.md:3 | matched: Tasks 1, 2, 3 |

## Findings

The merge step re-read the evidence lines of each finding; the git counts were taken from the saved diagnostics, not re-run. Priorities are the debate's final ones.

| ID | Priority | Finding | Evidence |
|---|---|---|---|
| F-1 | P1 | Task 6 says a `primary` or `fallback_1` scan has no nested folder. A clean `/sc:analyze` run is also `primary` (it is one of the two first-choice actions), and `source` and `quality_tier` are separate fields in `enrichment_used`, neither of which names the tool. A checker following this wording fails a correct analyze run. | plan:81, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:187`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:198`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:372` |
| F-2 | P1 | Task 7's third bullet requires only the six named files plus this package among tracked paths, and nothing changed under `.dev/tasks/done/`. Today's tree already has 950 `A` and 3 `R` entries for the archived P1 package, so the "tracked paths" clause fails before any edit; whether the `done/` clause fails depends on how "modified" is read. | plan:98, `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/artifacts/diagnostics.txt:3-4` |
| F-3 | P1 | The owner's rule has two halves: the fallback writes no nested folder, and it lists no nested contract. No planned pin covers the contract half, and "exists only when `/sc:analyze` ran" is pinned only in the spec. | source.md:6, plan:33, plan:60, plan:74, plan:84 |
| F-4 | P2 | Task 4's `fallback_1` check over the whole Wave 2A section already passes on the old text. | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:199`, plan:65, `tests/skills/test_brainstorm_protocol.py:24-29` |
| F-5 | P2 | The routing-ref checks count matches file-wide, so two copies in one tier, or in the research tiers, would pass. | plan:42, plan:60 |
| F-6 | P2 | Task 7 omits `tests/skills/test_codegraph_adoption.py` and `tests/skills/test_tier2_tavily_consistency.py`, which read the edited files. Read, not run: the planned text breaks neither. | plan:93, `tests/skills/test_codegraph_adoption.py:75-82`, `tests/skills/test_tier2_tavily_consistency.py:19` |
| F-7 | P2 | Task 6 puts a brainstorm-specific instruction in the general section 2.1 bullet and never records that it weighed the brief's placement rule (a search of the spec found no per-command extras list in sections 7.2 or 7.3). | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62` |
| F-8 | P2 | Task 5's "more cases than before" check records no baseline (17 today, a value that moves with the tree). | plan:75, `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/artifacts/diagnostics.txt:11` |
| F-9 | P2 | Task 2 says each tier list ends with its `quality_tier` line. The Tier 2 list ends with the Activation bullet. | plan:39, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:30-33` |
| F-10 | P2 | Stale line numbers: Task 4 says line 37 (it is 39); Task 5 says 286 (that is the brainstorm entry; its phrase list opens at 288). Line 711 needs no change. | plan:60, plan:71, `tests/skills/test_brainstorm_protocol.py:39`, `tests/skills/test_worker_contract.py:286-292`, `tests/skills/test_worker_contract.py:704-729` |
| F-11 | P2 | Task 6 calls spec line 142 a section 6 row. It is in section 3.1. | plan:81, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:142` |
| F-12 | P2 | "write" (skill) and "writes" (routing, command) are pinned separately. A shared phrase fixes it (covered by F-3). | plan:30, plan:39 |
| F-13 | P2 | Task 7 says "Do not edit any file" but writes three logs under `./artifacts/`. | plan:93 |
| F-14 | P2 | [INFERRED] Task 1's "listed only for a nested command that ran" could unlist a failed call's contract. | plan:30, `src/superclaude/commands/brainstorm.md:157` |
| F-15 | P2 | [INFERRED] After Task 2 the routing ref never names `/sc:analyze`, so a reader would conclude codebase enrichment never nests. | `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:9-33` |
| F-16 | P2 | The plan forbids commits, and live-check worktrees are built from committed branches, so the fix reaches the next live plan only after the edits are committed to a branch the live-check worktree is built from. | plan:24, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:282` |
| F-17 | P2 | Plan line 21 leaves the plugin copy alone but does not say it resolves spec open item 8 for this file. | plan:21, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:443` |
| F-18 | OPEN | Research enrichment from P2 also passes a nested report directory, and research-deep `fallback_1` is itself a nested command. The corrected wording covers only the codebase wave. Outside this plan's brief; not resolved. | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:142`, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:222`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:69` |

Claims the debate withdrew: the Tier 1 card's "ready after one fix", reviewer 3's fix that decides by the `source` field (it cannot tell analyze from auggie), reviewer 1's "say an auggie scan (tier primary)" fix (it leaves the `fallback_1` half false), and reviewer 2's "fails twice" and fixed post-edit count of 18.

The exact replacement text for the Task 6 sentence and for the Tasks 1 to 3 wording is in `adversarial/merged-verdict.yaml`, key `replacement_wording`. It has residual false-PASS risks (listed there); it has no known false FAIL on a correct run. The tool names `Skill`, `Agent` and `Task` in that sentence are inferred from the session-file format and not confirmed against a real run.

## Dropped by validation

One citation was dropped: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:286` (F-7). That line is the 7.2 step 4 contract check; it does not by itself show that the spec has no per-command extras. F-7 now stands on the search result stated in its row instead. This drop makes the report status partial.

## Open conflict for the owner

F-18 (INV-020) stays open. It does not block this plan's own fixes, but the next live plan can still fail falsely for the research wave from P2. Either record it as an accepted risk, or have the P2 live-plan author add research-wave wording.

## Inferred-claim audit

- `citations_inferred: 2` (F-14, F-15)
- Inferred-fraction: 2 over the citation total in the header.

## Recommendations

### Recommendation R-001: Fix the three P1 findings before running /sc:implement

- **File:** `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md` (Tasks 1 to 7, lines 28 to 98)
- **Change:** apply F-1 (Task 6 wording), F-2 (Task 7 third bullet compares a status snapshot taken before Task 1 with one taken after) and F-3 (pin both halves of the owner rule with the shared phrases in `replacement_wording`). The plan file is not edited by this review; regenerate it, or apply the changes by hand.
- **Verifier:** the revised plan no longer contains "a `primary` or `fallback_1` scan is recorded as the tier used" and no longer contains "among tracked paths"; Tasks 4 and 5 name the two shared pins.
- **Linked deviation(s):** none (proactive; findings F-1, F-2, F-3)
- **Priority:** P0

### Recommendation R-002: Apply the fourteen P2 fixes in the same pass

- **File:** `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md` and `adversarial/merged-verdict.yaml` (findings F-4 to F-17, each with its own file, change and verifier)
- **Change:** work through F-4 to F-17 from the merged verdict; among the larger are the per-tier routing pins (F-5), the two added test files (F-6) and the Task 6 placement (F-7).
- **Verifier:** each finding's verifier in `merged-verdict.yaml` passes; `uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py tests/skills/test_tier2_tavily_consistency.py -q -p no:cacheprovider` passes after the edits.
- **Linked deviation(s):** none (proactive)
- **Priority:** P1

### Recommendation R-003: Decide what to do about the research-wave conflict

- **File:** n/a (owner decision; later `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` for the P2 live-plan author)
- **Change:** record whether INV-020 is an accepted risk or must be fixed in the P2 live plan.
- **Verifier:** the owner's decision is recorded where the P2 live-plan author will read it.
- **Linked deviation(s):** none (finding F-18)
- **Priority:** P2
