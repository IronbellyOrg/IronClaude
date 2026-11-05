# Merge Execution Log

## Metadata
- Base: Variant 3 (option c, unsupervised orca-cli handoff to a person-owned tab), `variant-3-original.md`
- Executor: merge-executor agent
- Changes applied: 15 of 15
- Status: success
- Timestamp: 2026-11-02T18:19:27Z
- Plan: `refactor-plan.md` (approved after review cycle 2, `refactor-plan-review.md` section "Cycle 2"). Output: `merged-output.md`.
- Interpretation of the requested section list: "Position" is the base's "Position:" paragraph under the H1, not a separate H2 section (the base has no H2 Position section, and a second one would repeat the paragraph). Every other requested section is an H2, in the requested order.
- Plan change numbers do not exist in the merged text, so every "Change N" pointer the plan writes inside merged wording (Change 1 position, Change 15 gate list, Change 2 item 3) is rendered as a pointer to the merged section or bullet that holds that change. No pointer changes meaning.

## Changes Applied

### Change 1: Lead with "never an Orca worker"; one run per PR by default
- **Status**: Applied
- **Source**: Variant 1, Position (V1:3) and "How a person works day to day" (V1:17), without V1:17's coordinator-session clause and its withdrawn "rarely needed" clause
- **Target**: Base, Position (restructure); also the first bullet of "How a person works day to day"
- **Before**: V3:3 opened with the parallel route ("When the person wants several PRs monitored at once, the coordinator ... launches each pr-submit run") and called pr-submit "never a supervised worker".
- **After**: Position opens with the rule (not an Orca worker under this decision, no `--unattended`, no Phase 4 edits, `SPEC:341`; (b) deferred, not rejected), then the default (one ordinary top-level session per PR after the workers finish), then several tabs only when the person names several PRs. The base's launch command and `[CLI]` lines 49-52 / 27-31 citations are kept (base strengths 1-2, `base-selection.md:164-165`). The heading wording "never" (N-02) is not carried into the merged text; the merged text follows the integration point. The day-to-day section gains "One PR, one session: the default" (INV-016).
- **Provenance tag**: `<!-- Source: Variant 1, Position (V1:3) and "How a person works day to day" (V1:17), merged per Change #1; Base (original, modified) V3:3, ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:341`, `[CLI]` 49-52, 27-31 re-opened) | Contradictions ✅

### Change 2: The run's session must stand in the PR's own child worktree
- **Status**: Applied
- **Source**: CR-01 T3 (`CR-01:19`), K4, K5 (`SKILL.md:268`), INV-001 and INV-014 (`invariant-probe.md:22,35`), `GO-BS:172`, `GO-RP:35-36`
- **Target**: Base, Position (child worktree named) and new H2 "Where the run happens" after the Position
- **Before**: [Section did not exist]; V3:3 said the agent runs "in that change's worktree".
- **After**: New section: binding facts (`commands/pr-submit.md:8`, `SKILL.md:268`, `fsm.py:548`, `CR-01:15,19`), the UNVERIFIED session-move question, the "judgment, not a fixed constraint" label, items 1-4 (child per PR via `orca worktree create ... --setup run --json` without `--agent`, Orca default path `CR-01:41`; session stands in the child; carrier order with the coordinator gated and UNVERIFIED; open CR-01 gap), and the cross-decision conflict with git-ownership row 1 (`GO-BS:172`). The Position now says "that PR's child worktree".
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #2 (fixed constraints K1, K4, K5; closes INV-001 and INV-014, ...); new section -->`
- **Validation**: Structural integrity ✅ | References ✅ (all re-opened; `GO-RP:35-36` carried as written, known off by one line per N-03, not corrected) | Contradictions ✅

### Change 3: Start only on the person's named instruction
- **Status**: Applied
- **Source**: INV-006 (`invariant-probe.md:27`); `HWW:215`, `HWW:221`, `HWW:223`, `SPEC:156`; base V3:13
- **Target**: Base, Safety (replace V3:13)
- **Before**: "The launch itself starts an outward loop, so the coordinator does it only when the person's instruction names it (D4)."
- **After**: "Start guard" bullet: a run is started, by the person or the coordinator's launch, only when the person's own instruction names opening or attaching to the PR for that branch at `--monitor 3`; authority anchored on `HWW:215` / `HWW:221` (and `SPEC:156`), not D4; without it the coordinator reports branch, child worktree and command line and starts nothing (`HWW:223`); the instruction text is recorded beside each launch.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #3 (closes INV-006, ...; INV-019 ADDRESSED); replaces the base's V3:13 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: Pre-PR steps and their owner
- **Status**: Applied
- **Source**: INV-017 (`invariant-probe.md:38`), INV-007 (`:28`); `SKILL.md:267,268,274`; `CLAUDE.md:65`; `decisions/D4/option-c.md:3`; `decisions/D4/debate/adversarial/debate-transcript.md:720-722`; `GO-BS:172`; `CR-01:34`
- **Target**: Base, new H2 "Before the run" after "Where the run happens"
- **Before**: [Section did not exist]
- **After**: Why pr-submit needs the steps (no commit or head push; create-path rebase; `pr_head_mismatch` after a rebased pushed branch; fork master often ahead), then the five ordered steps (commit, rebase in the parent, create the child, push the child branch by name with approval, then start), "no commit between steps 3 and 5", the git owner (coordinator under `GO-BS:172`, role at `CR-01:34`), and the D4 coupling. One citation was added for an uncited plan claim: `SPEC:347` for D4 (b) "Workers make no outward changes" (re-opened; it states exactly that).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #4 (closes INV-017 and INV-007, ...); new section -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: One live monitor per PR; keep the worktree until the run is over
- **Status**: Applied
- **Source**: INV-012 (`invariant-probe.md:33`), INV-002 (`:23`); `SKILL.md:306`; `commands/pr-submit.md:55`; `[CLI]` line 65; `CR-01:23`
- **Target**: Base, Reliability (append)
- **Before**: Reliability had no exclusivity or worktree-lifetime rule.
- **After**: Three bullets: "One live monitor per PR" (no PR lock by design; pre-launch run-log and live-tab check; a person-typed run checks the same; tab detection UNVERIFIED); "Lost launches and resumes" (`operationId`, `--retry-launch`, `--resume` in the same child); "Keep the worktree until the run is over" (removal only after a terminal status and a merged or closed PR; status read once at cleanup as a precondition, not monitoring).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #5 (closes INV-012, ...; addresses INV-002, ...) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (the one cleanup-time read is framed as a precondition, consistent with the X-004 removal in Change 13)

### Change 6: A defined smoke test for the coordinator-launched route
- **Status**: Applied
- **Source**: Variant 2, Reliability (V2:17) and Implementation cost (V2:24) as the model for a pass condition; INV-008 (`invariant-probe.md:29`); INV-022; `[CLI]` lines 29, 63; `SKILL.md:272`; `commands/pr-submit.md:50`; `fsm.py:548`
- **Target**: Base, Reliability (replace the UNVERIFIED sentence of V3:17) and Implementation cost
- **Before**: "Whether a slash command passed as `--prompt` runs as a slash command is UNVERIFIED; the spec's own workers depend on the same argv prompt mechanism for Claude (`CAPS:47`)."
- **After**: "Launch check" bullet: the question stays UNVERIFIED until the check passes, and only the person-typed route is used until then; the exact `agent launch ... --monitor 1 --pr <scratch PR> --max-rounds 2` command on the person's actual surface; scratch PR on the fork with the child's own branch as head; why L1 is safe; the four pass conditions; the UNVERIFIED multi-iteration note; the closing y/n answered "n" (wording as planned; N-05 not applied). Implementation cost gains "costs one scratch PR on the fork".
- **Provenance tag**: `<!-- Source: Variant 2, Reliability (V2:17) and Implementation cost (V2:24) ..., merged per Change #6 ...; replaces the UNVERIFIED sentence of V3:17 -->` and `<!-- Source: Variant 2, Implementation cost (V2:24), merged per Change #6 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (the Position points to this check as the gate for launched tabs)

### Change 7: Readiness before the run
- **Status**: Applied
- **Source**: INV-009 (`invariant-probe.md:30`); `commands/pr-submit.md:28-30`; `HWW:223`; `CR-01:24`
- **Target**: Base, "Before the run" (append)
- **Before**: [No readiness rule]
- **After**: "Readiness" bullet: child setup succeeded, `gh` authenticated, review App installed on the fork before a run starts; otherwise pr-submit STOPs at preflight.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #7 (INV-023 gate G7; INV-009, ...) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (see the inherited wording note under "Contradiction Re-Scan")

### Change 8: Two fix cycles, then the person decides
- **Status**: Applied
- **Source**: K3 (commit `80f934de`, PR #343); `commands/pr-submit.md:47`; `SKILL.md:270,275,276`
- **Target**: Base, Safety (append)
- **Before**: [No round-cap rule]
- **After**: Bullet: default `--max-rounds 2`, never higher (pr-submit still accepts up to 5); at the cap `terminal_max_rounds` and the person decides; Low and Nit reported, never fixed; the decline-fallback extra push (`push_count <= max_rounds + 1`) reported as a deviation, its #343 status UNVERIFIED; the "blocking" to Medium-and-above mapping UNVERIFIED.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #8 (fixed constraint K3, commit 80f934de, PR #343) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (the launch check's `--max-rounds 2` matches)

### Change 9: Fork only; no Orca PR or issue linking
- **Status**: Applied
- **Source**: K2 (`CR-01:45`); `SKILL.md:267`, `SKILL.md:304`
- **Target**: Base, Safety (append)
- **Before**: [No fork rule]
- **After**: Bullet: the PR is opened only by pr-submit on origin (`IronbellyOrg/IronClaude`); launches pass no Orca `--pr` / `--issue` linking because Orca records the project as `github:superclaude-org/superclaude_framework`.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #9 (fixed constraint K2, CR-01:45) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: "Attended" means in-session; (b) is deferred, not rejected
- **Status**: Applied
- **Source**: Variant 2, Strongest case (V2:9); X-001; `SKILL.md:43-45`, `SKILL.md:82-84`, `SKILL.md:272`; `refs/state-machine.md:170-172`; `SPEC:56`; `CAPS:161`, `CAPS:47`; `worker-start --help` lines 38, 42; `[CLI]` lines 47, 63; `HWW:223`; `SPEC:276`
- **Target**: Base, "Why a third option" (replace V3:8; heading renamed "Why not a worker now, and why a third route" per the requested section list) and Implementation cost (append reopening conditions)
- **Before**: V3:8: "(b) gives parallelism but makes an attended, top-level, 'Will Not: run headless' command ... into an unattended worker."
- **After**: Four bullets with the corrected meaning (in-session, not watched; no confirmation before a push; monitor 2/3 versus the monitor-1 y/n proposal and `SPEC:56`; a terminal worker is top-level; the chat-surface question UNVERIFIED for workers and launched tabs alike; so (b) is not ruled out). The non-conflated part of V3:8 is kept as "Why a third route" ((a) one PR per session; (c) several PRs with the command unchanged), so the section keeps the base's purpose. Implementation cost gains the four reopening conditions, with the base's "Cost to switch to (b) later is unchanged" kept.
- **Provenance tag**: `<!-- Source: Variant 2, Strongest case (V2:9), merged per Change #10 ...; replaces the base's V3:8 claim ... -->`, `<!-- Source: Base (original, modified), V3:8: the non-conflated clause kept ... -->`, `<!-- Source: Variant 2, Strongest case (V2:9), reopening conditions merged per Change #10; ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (no "headless" or "unattended worker" claim remains; Changes NOT Being Made rows C-001/X-001 and C-006/S-006 respected)

### Change 11: Spec corrections that hold whatever D3 decides
- **Status**: Applied
- **Source**: Variant 2, Round 2 rebuttal (`debate-transcript.md:662`); INV-010, INV-011; `SPEC:67`, `SPEC:71`, `SPEC:74`, `SPEC:137`, `SPEC:340`
- **Target**: Base, Implementation cost (replace "One sentence in section 4 / D3 of the spec")
- **Before**: "One sentence in section 4 / D3 of the spec".
- **After**: Numbered list of four spec corrections: drop "(the worker may use `ask` or `escalation`)" from the `SPEC:137` row; WC-7 and the `SPEC:137` row cite `SKILL.md:47-49`, not `37-39`; `SPEC:340` re-cited to `SKILL.md:267,274` and `43-45,51-84`; re-check the other pr-submit citations in `SPEC:74` and `SPEC:137`. Each spec line was re-opened and holds the quoted text.
- **Provenance tag**: `<!-- Source: Variant 2, Round 2 rebuttal (debate-transcript.md:662), merged per Change #11 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: Zero build cost and the command count
- **Status**: Applied
- **Source**: Variant 1, Implementation cost (V1:21); `SPEC:195-197`
- **Target**: Base, Implementation cost (append)
- **Before**: V3:23 "no pr-submit edits, no AC-4.3".
- **After**: "35, not 36, commands accept `--unattended` (`SPEC:195`; `SPEC:197`); no pr-submit edits; no AC-4.3 (`SPEC:276`)." The base clause it repeats was folded into this bullet rather than kept twice.
- **Provenance tag**: `<!-- Source: Variant 1, Implementation cost (V1:21), merged per Change #12 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 13: Repair the base's factual errors
- **Status**: Applied
- **Source**: Correctness 1, 4, 5 NOT MET for V3 (`base-selection.md`); X-004; X-003 and C-003; better variant V1:10; `SKILL.md:268,274,276,316-318,325`; `[G]` line 39
- **Target**: Base, Safety V3:11-12 and Reliability V3:17 (replace)
- **Before**: V3:11 "A HALT waits in a visible tab, and a person's tab has no readiness limit (`CAPS:52`, ...)"; V3:12 quoted `[G]` line 39 without "and do not monitor completion"; V3:17 "The person reads each tab, or the coordinator reads the run-log file later."
- **After**: V3:11: every operator HALT (`pr_head_mismatch`, `push_range_mismatch`, `fix_commit_failed`, `needs_human_decision`) ends the run with `terminal_halted`, recovery steps stay in the session or tab for the person; the round cap ends with `terminal_max_rounds`; the `CAPS:52` claim dropped. V3:12 quotes `[G]` line 39 in full. V3:17: the coordinator gets no completion signal and does not track completion; the person reads each tab.
- **Provenance tag**: `<!-- Source: Base (original, modified), V3:11, adjusted per Change #13 ... -->`, `<!-- Source: Base (original, modified), V3:12, adjusted per Change #13 ... -->`, `<!-- Source: Base (original, modified), V3:17, adjusted per Change #13 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (Changes NOT Being Made row X-004 respected)

### Change 14: Order of the coordinator's two roles
- **Status**: Applied
- **Source**: INV-018 (`invariant-probe.md:39`); `[G]` lines 37, 39; `[CLI]` lines 27, 29
- **Target**: Base, "How a person works day to day" (append)
- **Before**: [No ordering of the supervised Run and the handoff]
- **After**: Bullet: settle the supervised Run (read contracts, admit or reject, release workers), then the pre-PR steps, then launch the tabs and report worktree id, handle and the person's instruction, then do not watch the tabs; "stops" means not monitoring, not ending unrelated work.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #14 (INV-018, ...) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 15: One gate list that closes INV-023
- **Status**: Applied
- **Source**: INV-023 (`invariant-probe.md:44`); `debate-transcript.md:655`
- **Target**: Base, end of "Before the run" (append a checklist)
- **Before**: [No gate list]
- **After**: Ten-item checklist G1-G10 in order, each pointing at the merged section or bullet that owns it (the plan's "Change N" owners rendered as section names); G5 passes unchanged (`SKILL.md:267`); G10 is the accepted risk (INV-003, `[G]` line 39).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change #15 (closes INV-023, ...; gate requirement debate-transcript.md:655) -->`
- **Validation**: Structural integrity ✅ | References ✅ (every G-item pointer resolves to an existing section or bullet) | Contradictions ✅

### Additional item (not a numbered plan change): V1:9 safety point
- **Status**: Applied, on the orchestrator's instruction (its section list names "V1:9 point" under Safety); not counted in the 15 planned changes
- **Source**: Variant 1, Safety (V1:9); strength 2 in `base-selection.md:173` (C-002)
- **Target**: Base, Safety (one bullet)
- **Before**: [Not in base]
- **After**: "At its default `--monitor 3` pr-submit commits, pushes the fixes without asking, and replies to and resolves the review comments it fixed (`CLAUDE.md:50`; `HWW:221`). So the safety difference between routes is visibility and who authorized the start, not a per-push approval."
- **Provenance tag**: `<!-- Source: Variant 1, Safety (V1:9), strength 2 in base-selection.md:173 (C-002); placed in Safety per the orchestrator's section list, not a numbered plan change -->`
- **Validation**: Structural integrity ✅ | References ✅ (`CLAUDE.md:50`, `HWW:221` re-opened; V1:9's `HWW:307` and `commands/pr-submit.md:83` not carried) | Contradictions ✅ (no row of "Changes NOT Being Made" covers it)

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ One H1 (merged position title), then seven H2 sections; no H3 or deeper, no skipped levels (checked with `grep -nE '^#{1,6} '`).
- Section ordering: ✅ Position paragraph, citation key, then "Where the run happens", "Before the run", "Why not a worker now, and why a third route", "Safety", "Reliability", "How a person works day to day", "Implementation cost", matching the requested order and the plan's insert points (Change 2 after Position, Change 4 after "Where the run happens").
- Document flow: ✅ The base's position-file shape is kept (H1, "Position:" paragraph, citation-key line, H2 sections). 25 `<!-- Source: ... -->` tags; every section and significant block carries one; the provenance header names Base = Variant 3 (option c). No `TODO` left; no em or en dashes (checked with `grep -nP '\x{2014}|\x{2013}'`).

### Internal References
- Total references: 22 (15 quoted section names, 1 "from the Position", 2 item pointers in "Where the run happens", 3 step pointers in "Before the run", 1 "readiness bullet above")
- Resolved: 22
- Broken: 0
- External path:line citations: every one carried into the merged text was re-opened in this run (`SKILL.md`, `refs/state-machine.md`, `commands/pr-submit.md`, `fsm.py`, `HWW`, `SPEC`, `CAPS`, `CR-01`, `GO-BS`, `GO-RP`, `invariant-probe.md`, both debate transcripts, `decisions/D4/option-c.md`, `CLAUDE.md`, and the four Orca help texts). All resolve. One is imprecise as already recorded by the plan review: `GO-RP:35-36` holds the rationale, while the UNVERIFIED wording is at `GO-RP:37` (note N-03, carried unchanged because minor notes trigger no fix pass).

### Contradiction Re-Scan
- New contradictions introduced: 0
- Against "Changes NOT Being Made": C-006/S-006 (no worker route; only deferral conditions) ✅; C-001/X-001 (no "headless" claim) ✅; X-002 ("rarely needed" absent) ✅; C-008 (no "Depends on D4 (a) or (c) for any push"; the true pre-PR coupling stated instead) ✅; C-005/A-006 (coordinator kept as first carrier, gated and UNVERIFIED) ✅; X-004 ("coordinator reads the run-log file later" removed; the single cleanup-time read is a precondition, as Change 5 frames it) ✅; INV-015 (no tab limit set) ✅; INV-004 (instruction recorded in the coordinator's launch report; launch prompt carries only the slash command) ✅; INV-005/INV-013 (not mentioned) ✅; C-012 (no worker reports; the person reads each tab) ✅.
- Against the plan's own text: Position (tabs launched on instruction) agrees with "Launch check" (person-typed route only until the check passes) through an explicit pointer; Safety's 2-round cap agrees with the launch check's `--max-rounds 2`; the start guard's `--monitor 3` and the launch check's `--monitor 1` cover different runs (real PR versus scratch PR), as the plan writes them.
- Inherited wording, not new and not fixed (the plan is applied as written): Change 7 says that without the review App "pr-submit STOPs at preflight", but the cited STOPs (`commands/pr-submit.md:28-30`) cover head mismatch and the CI-wait preflight only; per INV-009 a missing App ends `terminal_augment_no_response` (`invariant-probe.md:30`). The review did not flag this; it is recorded here for the consolidated revision.

## Summary
- Total changes planned: 15
- Successfully applied: 15
- Failed: 0
- Skipped: 0
- Additional item applied on the orchestrator's instruction: 1 (V1:9 safety point, `base-selection.md:173`), not counted above
- Post-merge validation: PASS (0 broken references, 0 new contradictions; one imprecise citation, N-03, and one inherited Change 7 wording issue disclosed above)

## Known minor notes
From `refactor-plan-review.md`, section "Cycle 2", "New findings (all MINOR; notes only)". None was applied: under the PR #343 rule, minor findings are notes and trigger no fix pass.

- N-01 (Change 2 vs Changes NOT Made), not applied: The INV-005/INV-013 row still says "under Change 2 the coordinator never holds the loop". Revised Change 2 keeps the coordinator as the first carrier once its check passes, and then INV-005 and INV-013 apply again.
- N-02 (Change 1), not applied: The Change 1 heading still reads 'Lead with "never an Orca worker"', which contradicts its own fixed integration point.
- N-03 (Change 2, C-005 row), not applied: `GO-RP:35-36` is cited for the git-ownership merge marking the coordinator's move UNVERIFIED. The UNVERIFIED text is at `GO-RP:37` (Risk line); lines 35-36 hold the rationale and conditions only.
- N-04 (Change 2), not applied: "A check shows it can stand in the child for the whole loop" names no procedure or pass condition, so the first carrier can never be enabled as written. The plan is safe, because the fallback applies, but the gate cannot be completed as written.
- N-05 (Change 6), not applied: "The run ends on L1's 'fix these? y/n' proposal" holds only when at least one finding is verified; with none, the run reaches Wave 8 or a terminal status without a proposal.
