# Refactor Plan Review (D3)

Reviewer: analytical reviewer for Step 4 of `/sc:adversarial` (D3). Target: `refactor-plan.md` (14 changes). All sources were re-read on 2026-11-02 in this worktree. Line numbers for the Orca guides come from `orca-ide skills get orca-cli | cat -n` (`[CLI]`), `orca-ide skills get orchestration | cat -n` (`[G]`) and `orca-ide orchestration worker-start --help | cat -n` (`WSH`). `PRS` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`; `PRC` = `src/superclaude/commands/pr-submit.md`; `SM` = `refs/state-machine.md` of that skill; `HWW` = `src/superclaude/core/HOW-WE-WORK.md`; `SPEC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `CAPS` = `.dev/orca-command-refactor/inventory/orca-capabilities.md`; `GO-RP` / `GO-BS` = `decisions/git-ownership/debate/adversarial/refactor-plan.md` / `base-selection.md`.

## Verdict

**FAIL.** 1 CRITICAL, 8 IMPORTANT, 8 MINOR findings. All four HIGH invariants (INV-006, INV-012, INV-017, INV-023) have a planned change, but INV-012's change (Change 5) does not fully stop a second monitor, and INV-023 is closed only implicitly. Change 2 conflicts with the git-ownership plan, and the plan does not say so. Change 10's main conclusion holds at `--monitor 2/3`, but it is overstated at `--monitor 1`.

## Findings

| ID | Change # | Severity | What is wrong | Evidence path:line | Exact fix |
|---|---|---|---|---|---|
| F-01 | 2 (also 4) | CRITICAL | Change 2 takes the coordinator's own session off pr-submit and makes a person-owned tab in the child worktree the carrier. That tab opens the PR and pushes fix commits. This contradicts the converged git-ownership merge, which makes the coordinator the owner of every outward action, "PR through `/sc:pr-submit --monitor 3`", "in its main chat". It also contradicts that merge's Change 3, which says that "under D3 (a) the coordinator itself must stand in the PR-head checkout". The D3 plan never names this conflict. Change 4 then uses the same git-ownership convergence to make the coordinator the git owner, so the plan relies on that decision in one place and overrides it in another without saying so. | `GO-BS:172`; `GO-RP:35-36`; `refactor-plan.md:23-25,38` | Add to Change 2 a "Cross-decision conflict" bullet: "This overrides git-ownership row 1 (`GO-BS:172`) and its Change 3 rationale (`GO-RP:35`). The PR and its fix pushes are made by the pr-submit session in the PR's child worktree, which runs on the person's named instruction (Change 3). The consolidated revision must change git-ownership row 1's PR owner to match, or this change is rolled back." Add the same item to the Risk Summary row for Change 2. |
| F-02 | 2 | IMPORTANT | The plan calls Change 2 "a constraint-driven change, not a debate outcome", but K4 and K5 do not exclude the coordinator. They require a PR-head checkout with no other writer, and a coordinator session could in principle stand in that checkout (`GO-RP:35` assumes it does). The exclusion rests on an unsourced claim about a tool: "Claude Code's Bash tool keeps a `cd` only inside the session's working directories". No source is cited, and the plan does not consider adding the child worktree as a working directory (for example `/add-dir`). Only the conclusion is marked UNVERIFIED, not the claim about the tool. | `refactor-plan.md:23`; `CR-01:19` (T3 is defined for a worker dispatched with `worker-start`, `CR-01:16`) | Reword the claim: "Claude Code's Bash tool does not keep a `cd` outside the session's working directories (UNVERIFIED here; not checked whether `/add-dir` makes a sibling worktree usable for every pr-submit script call)." Replace "This is a constraint-driven change, not a debate outcome" with "This is a judgment drawn from K4, K5 and the UNVERIFIED tool behaviour above; it overrides the debate's 'coordinator or person' default (R2-V1 #16, A-006)." |
| F-03 | 1 vs 2 | IMPORTANT | Change 1 takes its text from V1:17 and drops only the withdrawn "rarely needed" clause. V1:17's first sentence is "One PR at a time from the coordinator's session; the person sees the review loop where they already talk to the coordinator". Change 2 removes exactly that. A merge executor following Change 1's Source would bring the coordinator-session wording back. | `variant-1-original.md:17`; `refactor-plan.md:14,23` | In Change 1's Source, write "V1:17, without its 'from the coordinator's session ... where they already talk to the coordinator' clause (removed by Change 2) and without its withdrawn 'rarely needed' clause". |
| F-04 | 1 vs 10 | IMPORTANT | Change 1's lead rule is "pr-submit is never an Orca worker". Change 10 and the common Round 2 position say (b) is "deferred, not rejected". "Never" states a rejection. | `refactor-plan.md:17,75,79`; `debate-transcript.md:665` | Change Change 1's first sentence to "Under this decision pr-submit does not run as an Orca worker and gains no `--unattended` mode and no Phase 4 edits; (b) stays deferred under the conditions in Change 10." |
| F-05 | 5 | IMPORTANT | INV-012 (HIGH) is closed by the rule "the coordinator launches once per PR per instruction". A second instruction from the person (a re-ask), or a person-typed run in a PR that already has a tab, still starts a second live monitor in the same child worktree. That is the failure INV-012 names. The guard is applied per instruction, not per PR, and no pre-launch check exists. | `invariant-probe.md:33`; `refactor-plan.md:45`; `PRS:306` (no lock, by design) | Replace the second clause with: "Before any launch for a PR, the coordinator checks the PR's child worktree for a run-log under `.dev/pr-monitor/pr-<N>-*/` with no terminal status and for a live agent tab there. If either exists it launches nothing and tells the person to continue that run, or to `--resume` it after the tab is gone. A person who types the command checks the same thing. (Whether a live tab can be detected reliably is UNVERIFIED.)" |
| F-06 | 5 vs 13/14 | IMPORTANT | Change 5 lets the git owner remove the child worktree "only after the run reached a terminal status". Changes 13 and 14 remove every way for the coordinator to learn that status: no completion tracking, run-log reading dropped (X-004), and the coordinator "does not watch the tabs". The plan gives no way to establish the cleanup precondition. | `refactor-plan.md:45,99,105`; `[G]` line 39 | Add to Change 5: "The terminal status is established at cleanup time only, by the person's report or by one read of the run-log's final event when the person asks for cleanup. This is a one-time precondition check, not monitoring." |
| F-07 | 4 (with 2) | IMPORTANT | Change 2 makes the PR head the child's own branch, but Change 4 does not say which branch is rebased and pushed, or in which worktree. A branch checked out in the child cannot be rebased from the parent by checking it out there. If the feature branch is rebased after the child is created, the child is stale. The order "rebase, create child, push" is missing. | `refactor-plan.md:24,38`; `PRS:267-268`; `CLAUDE.md:65` | Rewrite Change 4's steps in order: (1) commits are on the feature branch in the parent; (2) the git owner rebases the feature branch onto `origin/<base>` in the parent; (3) the git owner creates the PR's child worktree from it (Change 2); (4) the git owner pushes the child's branch by name (`git push origin <child-branch>`) with the person's approval (`HWW:215`); (5) only then is the run started. No commit lands on the feature branch between steps 3 and 5. |
| F-08 | 6 | IMPORTANT | The smoke test runs in "child of a scratch branch" with `--pr <scratch PR>`. pr-submit's head binding requires the local branch name to equal the PR's `headRefName` exactly. A child created from a scratch base branch gets its own branch, so the test would HALT `pr_head_mismatch` whether or not the route works. The pass condition "poll events from at least two poll iterations" may also be unreachable on an existing PR whose reviews and CI have already finished (UNVERIFIED). | `src/superclaude/pr_submit/fsm.py:548`; `PRS:268`; `refactor-plan.md:24,52` | Change the target to: "a scratch PR whose head branch is the child worktree's own branch (pushed by the person beforehand)". Change the pass condition to: "a run-log with at least one Wave 1 or Wave 8 poll event and no HALT". Mark "two iterations on an already-reviewed PR" as UNVERIFIED, or use a PR the review App has not yet reviewed. |
| F-09 | 8 | IMPORTANT | Change 8 says the default `--max-rounds 2` "keeps every run at the 2-cycle cap". pr-submit's decline fallback allows `push_count <= max_rounds + 1` for the whole run, so a run can make a third fix push. That bears directly on fixed constraint K3. | `PRS:275`; `refactor-plan.md:65-66` | Add: "Exception: after an Augment decline, the single-shot fallback can add one more fix push (`push_count <= max_rounds + 1`, `PRS:275`). Whether this counts as a third fix cycle under #343 is UNVERIFIED; until it is settled, report it to the person as a K3 deviation, not as a pass." |
| F-10 | 13 | IMPORTANT | The corrected V3:11 text, "every HALT ends the run with `terminal_halted`", is itself wrong. The round cap (HALT_MAX_ROUNDS) ends `terminal_max_rounds`, and the L2 halt before push ends `halt_before_push`. C-003 says *operator* HALTs. The change meant to repair factual errors adds a new one. | `PRS:236,273,276`; `debate-transcript.md:587` | Replace it with: "every operator HALT (`pr_head_mismatch`, `push_range_mismatch`, `fix_commit_failed`, a `needs_human_decision` finding) ends the run with `terminal_halted`, and its recovery steps stay in that tab for the person (`PRS:268,274,316-318,325`); the round cap ends with `terminal_max_rounds` (`PRS:276`)." |
| F-11 | 10 | MINOR | "Nothing requires a person to watch" holds at L2 and L3. At L1, Wave 4 ends on a "fix these? y/n" proposal to the person (`PRS:272`), which is why the spec refuses `--monitor 1` under `--unattended` (`SPEC:56`). This matters because Change 6's smoke test runs at L1. | `PRS:272`; `SPEC:56`; `refactor-plan.md:78` | Change it to "At `--monitor 2` or `3`, nothing requires a person to watch; at `--monitor 1` the run ends on a y/n proposal to the person (`PRS:272`)." |
| F-12 | 10 | MINOR | `CAPS:47` is cited for "a terminal Orca worker is a top-level Claude session". `CAPS:47` covers readiness and the argv prompt path. It shows that a Claude worker is started with its task on the command line, not that the worker is top-level. `CAPS:161` alone supports the claim. | `CAPS:47`, `CAPS:161` | Cite `CAPS:161` (and `WSH` line 38) for top-level. Keep `CAPS:47` only for the argv prompt path. |
| F-13 | 4 | MINOR | "the coordinator under the git-ownership convergence, `CR-01:34`": CR-01:34 says only "one owner for push, PR and comments" and does not name the coordinator. The coordinator is named at `GO-BS:172`. | `CR-01:23,34`; `GO-BS:172` | Cite `GO-BS:172` for "the coordinator", and resolve it together with F-01. |
| F-14 | 11 | MINOR | The plan says the old SPEC:340 citations `189,196` and `41-64` "now point at poll-attribution text". That is true for 189 and 196 (S5 attribution). It is not true for 41-64, which still covers the framing, the top-level rule and the start of the poll loop. The other stale-looking citations in the SPEC:137 row (`46-64,66-68,141,170,189-197,237-246`) and in WC-10 at SPEC:74 (`46-64`, the loop is now at 51-80) were not re-checked. | `PRS:41-64,141,170,185-198`; `SPEC:74,137,340` | Say "`189,196` now point at S5 attribution text; `41-64` only partly covers the loop (51-80)". Add item (4): re-check every pr-submit citation in SPEC:74 and SPEC:137 against the current file. |
| F-15 | 2, 7 | MINOR | Change 2 says the child worktree is "created by Orca ... with `--base-branch`" (`CR-01:16,22`), but CR-01:16 is the `worker-start --worktree new-child` path. Under (a)/(c) no `worker-start` runs. The verb for a non-worker child, and how its setup is gated (Change 7), are not named. | `CR-01:16,24`; `orca-ide worktree create --help` lines 3, 23, 32-33, 53 | Name the verb: `orca worktree create --name <name> --parent-worktree <feature worktree> --base-branch <feature branch> --setup run --json`, without `--agent`. Then `agent launch` (or the person's tab) only after setup has succeeded. |
| F-16 | all | MINOR | The plan has no citation key. It uses `SPEC`, `HWW`, `CAPS`, `CR-01`, `V1:N`, `[CLI]`, `[G]` and a bare `SKILL.md`, which is ambiguous next to the adversarial and implement SKILL.md files. K5 cites `~/.claude/skills/...` while the review sources are the `src/` copies. | `refactor-plan.md:6,23,35` | Add a citation-key line under Overview defining each prefix, with `SKILL.md` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (installed copy identical when synced). |
| F-17 | INV-023 | MINOR | INV-023 (HIGH) is closed only piecemeal: Change 4 names G2-G4 and Change 7 names G7. G1 (Change 3), G6 (Change 2), G8 (Change 6), G9 (Change 5) and G10 (accepted, INV-003) are not mapped. The gate at `debate-transcript.md:655` asks for one explicit change or accepted-risk entry per HIGH item. | `invariant-probe.md:44`; `debate-transcript.md:655` | Add an "INV-023 closure" row: G1→3, G2-G4→4, G5 passes, G6→2, G7→7, G8→6, G9→5 (as fixed by F-05), G10 accepted risk (INV-003, no completion tracking by design). |

## Citations checked

| Citation (as used in the plan) | Result |
|---|---|
| `base-selection.md` "Combined Scoring" (level-1 tiebreaker, V3 selected) | OK |
| `debate-transcript.md:655` (status, plan must carry each HIGH item) | OK |
| `debate-transcript.md:661-665` (three recommendations; common position) | OK |
| `debate-transcript.md:662` (R2-V2 SPEC:137 fix) | OK |
| Scoring matrix: S-003 93%, C-002 97%, A-004 95%, X-005 92% (sole V1); X-001 V2 95%; X-004 V1=V2 97%; S-004/C-009 V1=V3 95-96%; C-008 90% with caveat | OK (`debate-transcript.md:581-605`) |
| `CR-01:41` (K1 Orca default paths) | OK |
| `CR-01:45` (K2 upstream; Orca project id) | OK |
| `CR-01:19` (K4, T3) | OK, but T3 is a worker-dispatch trigger (`CR-01:16`); the use for non-worker runs rests on K4 as given |
| `CR-01:15` (coordinator in parent worktree) | OK |
| `CR-01:16,22` (`--base-branch`) | OVERSTATED for non-worker children (F-15) |
| `CR-01:23` (cleanup by git owner) | OK |
| `CR-01:24` (setup before use) | OK |
| `CR-01:34` (git owner = coordinator) | OVERSTATED (F-13) |
| `SKILL.md:268,274,318` (K5) | OK |
| `SKILL.md:43-45` (attended, in-session; durability from run-log) | OK |
| `SKILL.md:82-84` (no side effect to background shell, detached loop, subagent) | OK |
| `SKILL.md:267` (Wave 0 origin, rebase if behind, no head push) | OK |
| `SKILL.md:268` (head binding; force-push never done) | OK |
| `SKILL.md:270` (Medium+ fixed, Low/Nit report-only) | OK |
| `SKILL.md:272` (L1 applies no edits) | OK (also shows the L1 y/n proposal, F-11) |
| `SKILL.md:274` (one fix commit, push) | OK |
| `SKILL.md:276` (HALT at round cap) | OK |
| `SKILL.md:304` (never upstream parent) | OK |
| `SKILL.md:306` (no lock file, Will Not) | OK |
| `SKILL.md:324` (rate-limit backoff) | OK |
| `SKILL.md:47-49` (top-level rule, Change 11) | OK |
| SPEC:340's `189,196` / `41-64` "now poll-attribution text" | OVERSTATED for 41-64 (F-14) |
| `refs/state-machine.md:170-172` (no interactive confirmation before push; monitor 3 + push_decision = authorization) | OK |
| `commands/pr-submit.md:8` (no worktree argument) | OK |
| `commands/pr-submit.md:28-30` (STOPs: head mismatch, CI preflight) | OK |
| `commands/pr-submit.md:47` (`--max-rounds` 2, cap 5) | OK |
| `commands/pr-submit.md:50` (Augment poke L3-only) | OK |
| `commands/pr-submit.md:55` (default output dir in worktree) | OK |
| `HWW:215` ("Push only with approval") | OK |
| `HWW:221` ("Requested and authorized full loop") | OK |
| `HWW:223` (prerequisites; "Recommending any branch performs no Git/GitHub action"; withhold on policy conflict) | OK |
| `CLAUDE.md:65` (rebase onto `origin/master` before push) | OK |
| `SPEC:67` (WC-3) | OK |
| `SPEC:71` (WC-7 cites `37-39`) | OK (stale cite confirmed) |
| `SPEC:137` (row says "`ask` or `escalation`", cites `37-39`) | OK |
| `SPEC:156` (`/sc:git`: coordinator runs git only when the user asked) | OK |
| `SPEC:195-197` (35, or 36 with pr-submit) | OK |
| `SPEC:276` (AC-4.3) | OK |
| `SPEC:340` (D3 text and its citations) | OK |
| `SPEC:343` (parallel need left to the person) | OK |
| `decisions/D4/option-c.md:3` (local commits only, never push) | OK |
| `decisions/D4/debate/adversarial/debate-transcript.md:720-722` ((c′) converged) | OK |
| `invariant-probe.md:22,23,27,28,29,30,33,35,38,39` (INV-001, 002, 006, 007, 008, 009, 012, 014, 017, 018) | OK, all at the cited lines |
| `CAPS:47` (top-level worker) | OVERSTATED (F-12); OK for the argv prompt path |
| `CAPS:161` (Orca worker is a top-level Claude session) | OK |
| `CAPS:52` (dropped by Change 13 as overstated) | OK to drop: the line covers a person's launch tab readiness, not HALT behaviour |
| `[CLI]` line 27 (full handoff; "the original agent stops") | OK |
| `[CLI]` line 29 (`prompt.outcome` `journaled` / `handed-to-terminal`) | OK |
| `[CLI]` line 47 (`outcome.kind` structured or terminal) | OK |
| `[CLI]` line 63 (Chat UI setting; `--surface`) | OK |
| `[CLI]` line 65 (`--retry-launch <operationId>`) | OK |
| `[G]` line 37 (coordinator role) | OK |
| `[G]` line 39 (handoff owner; "do not monitor completion") | OK |
| `worker-start --help` lines 42-44 (follows person's tab setting; not every worker has a terminal) | OK |
| V1:3, V1:10, V1:17, V1:21; V2:9, V2:17, V2:24; V3:8, V3:11-13, V3:17 | OK (content as described; V1:17 carries the coordinator-session clause, F-03) |
| Commit `80f934de` "did not edit pr-submit" | OK (`git show --stat 80f934de`: no `sc-pr-submit-protocol` or `pr-submit.md` path) |
| Not cited by plan, opened to test it: `src/superclaude/pr_submit/fsm.py:528-579` (exact branch-name equality) | Supports F-08 |
| Not cited by plan, opened to test it: `PRS:275` (`push_count <= max_rounds + 1`) | Supports F-09 |
| Not cited by plan, opened to test it: `GO-BS:172`, `GO-RP:35-36` (coordinator owns PR via pr-submit in main chat) | Supports F-01 |
| Not cited by plan, opened to test it: `orca-ide worktree create --help` (`--parent-worktree`, `--base-branch`, `--setup`) | Supports F-15 |

## Self-Audit

- **Scope read.** I read the whole plan and these files in full or at the cited ranges: base-selection.md (all, including "Combined Scoring" and "Selected Base"), the three variant files, debate-transcript.md:555-666, invariant-probe.md, PRS 30-89 and 185-328, SM 155-184, PRC 1-91, HWW 205-229, CLAUDE.md 46-67, SPEC 50-77, 134-158, 192-199, 272-277 and 336-349, CR-01 (all), D4 option-c (all), D4 transcript 710-723, and CAPS 44-53, 108-118 and 155-163. I ran the three read-only Orca help commands and `git show --stat 80f934de`. To test claims the plan makes, I also opened `fsm.py` `pr_head_ok` / `pr_branch_ok`, `orca-ide worktree create --help`, and the git-ownership base-selection and refactor-plan.
- **Check 1 (citations).** Every path:line in the plan was opened. Four are OVERSTATED (CR-01:16/22, CR-01:34, CAPS:47, SPEC:340's 41-64). None is outright wrong. Every invariant-probe line number matches.
- **Check 2 (follows from evidence; no silent overturn).** Changes 1, 3, 5-14 follow from the debate, the probe or K1-K5. Change 2 discloses that it overturns the debate's "coordinator or person" default (Changes NOT Made, row C-005/A-006). But it calls itself constraint-driven when it rests on an unsourced tool claim (F-02), and it silently overturns the converged git-ownership merge (F-01). I rated F-01 CRITICAL because the consolidated revision would otherwise carry two contradictory PR owners, and the plan cites the same git-ownership convergence for the opposite purpose in Change 4.
- **Change 10 (special attention).** I re-read PRS:43-45, PRS:82-84, SM:170-172, PRC:85 and SPEC:56. "Attended, in-session" is defined against detachment ("closing the session loses it ... never from detachment"), and push authorization is the monitor-3 arming plus the `push_decision` record, with no confirmation step. HALTs end the run, and the recovery text is read afterwards, so nobody needs to watch a live L3 run. The plan's conclusion holds at `--monitor 2/3` and agrees with the unanimous X-001 and C-001 results. It does not hold at `--monitor 1`, where Wave 4 ends on a y/n proposal (F-11). The chat-surface question is correctly marked UNVERIFIED.
- **Change 2 (special attention).** PRC:8 (no worktree flag) and PRS:268 (cwd-bound `git branch --show-current` / `git rev-parse HEAD`) are accurate, and K4 with the one-worktree-per-branch rule does force the PR head into the child. What the cited sources do not establish is that the coordinator *cannot* carry the run; that depends on Claude Code's working-directory behaviour, which the plan does not source. GO-RP:35-37 makes the opposite assumption and marks it UNVERIFIED. So the change is a defensible judgment, but it is labelled as a constraint and it conflicts with another decision.
- **Check 3 (HIGH invariants).** INV-006 → Change 3 (closed). INV-017 → Change 4 (closed; ordering gap F-07). INV-012 → Change 5 (partly: per-instruction guard, F-05). INV-023 → spread over Changes 2-7 without an explicit closure row (F-17). All seven MEDIUM items (INV-001, 002, 007, 008, 014, 015, 018) and all five LOW items (INV-004, 005, 009, 011, 013) have a change or a Changes-NOT-Made entry.
- **Check 4 (contradictions).** Found 1 vs 2 (F-03), 1 vs 10 (F-04), 5 vs 13/14 (F-06), 2 vs 4 ordering (F-07), and 2/4 vs git-ownership (F-01). The Changes NOT Being Made table agrees with the changes; its INV-004 accepted-risk entry is marked UNVERIFIED correctly.
- **Check 5 (unsourced assertions).** The Bash `cd` behaviour (F-02) and the "2-cycle cap" claim (F-09, contradicted by PRS:275) are asserted without marking. "git allows a branch in one worktree at a time" is sourced through INV-001 (`invariant-probe.md:22`) and is acceptable.
- **Not findings.** K1-K5 were treated as given, as instructed. "Review Status: TODO" (`refactor-plan.md:142-143`) is the slot for this review and is not flagged. Change 8's UNVERIFIED mapping of #343's "blocking" grade to Medium-and-above is correctly marked.

## Cycle 2

**Verdict: PASS.** No blocking finding remains. All 17 cycle-1 findings are fixed. This cycle found 5 new MINOR issues; under PR #343's rule they are notes, not blockers.

I re-read the revised `refactor-plan.md` (lines 1-159) and opened every new citation: `src/superclaude/pr_submit/fsm.py:548`, `orca-ide worktree create --help` lines 3/23/32-33, `SKILL.md:272,275,276,316-318,325`, `GO-BS:172`, `GO-RP:35-37`, and `worker-start --help` line 38. I also checked the claim "byte-identical installed copy" with `diff -q` (IDENTICAL).

| F-ID | Status | Evidence (revised plan) |
|---|---|---|
| F-01 | FIXED | Change 2 now has a "Cross-decision conflict" bullet naming `GO-BS:172` and the two ways the consolidated revision can resolve it (`refactor-plan.md:26`). The Risk Summary row for Change 2 names the conflict (`:137`). |
| F-02 | FIXED | The tool behaviour is marked UNVERIFIED, and the change is labelled "a judgment ... not a fixed constraint" (`:24`). The coordinator is kept as the first carrier, gated on that check (`:25` item 3). The Changes NOT Made row C-005/A-006 matches (`:125`). |
| F-03 | FIXED | Change 1's Source drops V1:17's coordinator-session clause (`:15`). |
| F-04 | FIXED | Change 1's integration point now says "does not run as an Orca worker ... (b) stays deferred" (`:18`). See note N-02 on the heading. |
| F-05 | FIXED | There is now a per-PR pre-launch check (run-log not at a terminal status, or a live tab), and a person-typed run checks the same thing. Tab detection is marked UNVERIFIED (`:47`). |
| F-06 | FIXED | The terminal status is established once, at cleanup time, from the person's report or one read of the run-log, framed as a precondition and not monitoring (`:47`). |
| F-07 | FIXED | The ordered steps are commit, rebase the feature branch in the parent, create the child, push the child branch by name with approval, then run, with no feature-branch commit between steps 3 and 5 (`:40`). |
| F-08 | FIXED | The scratch PR's head is the child's own branch, citing `fsm.py:548` (verified: `if local_branch != head_ref_name: return False`). The pass condition is now one Wave 1 or Wave 8 poll event and no HALT. Multi-iteration behaviour is UNVERIFIED (`:54`). |
| F-09 | FIXED | Change 8 now states the `push_count <= max_rounds + 1` exception (`SKILL.md:275`, verified) and reports it as a K3 deviation (`:68`). |
| F-10 | FIXED | The text now limits the claim to operator HALTs (`pr_head_mismatch`, `push_range_mismatch`, `fix_commit_failed`, `needs_human_decision`) ending in `terminal_halted`, and the round cap to `terminal_max_rounds`. `SKILL.md:316,317,318,325,276` were verified (`:101`). |
| F-11 | FIXED | The claim is now limited to monitor 2/3, with the L1 y/n proposal named (`SKILL.md:272`) and `SPEC:56` cited (`:80`). |
| F-12 | FIXED | Top-level now rests on `CAPS:161` and `worker-start --help` line 38 (verified: `--agent` takes `claude`). `CAPS:47` is used only for the argv prompt path (`:80`). |
| F-13 | FIXED | The coordinator as git owner is now cited to `GO-BS:172`, and the owner role to `CR-01:34` (`:40`). |
| F-14 | FIXED | `189,196` are described as S5 attribution text and `41-64` as partial loop coverage (51-80). An item (4) re-check of SPEC:74 and SPEC:137 was added (`:87`). |
| F-15 | FIXED | The verb is now `orca worktree create --name <name> --parent-worktree <feature worktree> --base-branch <feature branch> --setup run --json`, without `--agent` (verified at `worktree create --help` lines 3, 23, 32-33) (`:25`). |
| F-16 | FIXED | A citation key was added. The byte-identical claim was verified (`diff -q`: IDENTICAL) (`:10`). |
| F-17 | FIXED | The new Change 15 maps G1-G10 to Changes 3, 4, 2, 7, 6 and 5. G5 passes, and G10 is an accepted risk (INV-003) (`:110-115`). |

### New findings (all MINOR; notes only)

| ID | Change # | Severity | What is wrong | Evidence | Fix |
|---|---|---|---|---|---|
| N-01 | 2 vs Changes NOT Made | MINOR | The INV-005/INV-013 row still says "under Change 2 the coordinator never holds the loop". Revised Change 2 keeps the coordinator as the first carrier once its check passes, and then INV-005 and INV-013 apply again. | `refactor-plan.md:25,129` | "Not needed while the fallback carrier is used; if the Change 2 coordinator check passes, INV-005 and INV-013 reopen as accepted LOW risks." |
| N-02 | 1 | MINOR | The Change 1 heading still reads 'Lead with "never an Orca worker"', which contradicts its own fixed integration point. | `refactor-plan.md:14,18` | Rename the heading: "Lead with 'not an Orca worker under this decision; (b) deferred'". |
| N-03 | 2, C-005 row | MINOR | `GO-RP:35-36` is cited for the git-ownership merge marking the coordinator's move UNVERIFIED. The UNVERIFIED text is at `GO-RP:37` (Risk line); lines 35-36 hold the rationale and conditions only. | `GO-RP:35-37`; `refactor-plan.md:24,125` | Cite `GO-RP:35-37`. |
| N-04 | 2 | MINOR | "A check shows it can stand in the child for the whole loop" names no procedure or pass condition, so the first carrier can never be enabled as written. The plan is safe, because the fallback applies, but the gate cannot be completed as written. | `refactor-plan.md:25` | Add one line: "Check: in a coordinator session, run Change 6's L1 smoke test with the session standing in the child; pass = the same conditions as Change 6." |
| N-05 | 6 | MINOR | "The run ends on L1's 'fix these? y/n' proposal" holds only when at least one finding is verified; with none, the run reaches Wave 8 or a terminal status without a proposal. | `SKILL.md:271-272`; `refactor-plan.md:54` | "If any finding is verified, the run ends on L1's 'fix these? y/n' proposal ..., which the person answers 'n'." |

### Cycle 2 self-audit

I checked only what was asked: whether each fix is in place as written, and whether the revisions introduced new errors. Every new citation was opened, and none is wrong. One is off by a line (N-03). Each new issue is either a wording leftover (N-01, N-02, N-05) or a gate that stays closed, which is safe (N-04). None reopens a HIGH invariant or creates a conflict that would carry into the merged text as a factual error, so none is graded blocking.
