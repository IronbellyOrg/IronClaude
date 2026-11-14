# Refactoring Plan: Merge into Base (Variant V1)

Template: `~/.claude/skills/sc-adversarial-protocol/refs/artifact-templates.md` Section 4, with three added sections required by the Step 4 brief: "Index tables" (inside Overview), "Merge-executor instructions" and "Acceptance checks for the merge". Drafter: Step 4 refactoring planner for the debate-orchestrator; argues for no variant. Read-only except this file. Written 2026-11-13.

## Overview

- Base: Variant V1 (`variant-1-opus-architect.md`, opus:architect, 751 lines), selected in `base-selection.md` (score 0.915987; tiebreaker level 1, debate wins 9 of 44).
- Incorporating strengths from: V2 (`variant-2-opus-analyzer.md`, opus:analyzer) and V3 (`variant-3-haiku-backend.md`, haiku:backend).
- Planned changes: 66 (16 invariant Changes, 44 debate-point Changes, 6 document-level Changes).
- Changes NOT being made: 32 rows.
- New owner questions: Q25 to Q33 (nine). Q1 and Q14 are widened, not renumbered.
- Risk level: **Medium-High** overall. Most Changes are additive. Three groups are structural and carry most of the risk: the edge-table rebuild (Change 19), the PR actor and grant model (Changes 1, 13, 14, 44) and the JOIN move (Changes 7, 35).

### Inputs read for this plan

All read in this step: `base-selection.md` (whole), `convergence.md` (whole), `debate-transcript.md` Scoring Matrix (lines 973-1038), `diff-analysis.md` (whole), `invariant-probe.md` (whole), `round3-invariants-V1.md`, `-V2.md`, `-V3.md` (whole), section 6 of `round2-rebuttal-V1.md`, `-V2.md`, `-V3.md`, `variant-1-opus-architect.md` (whole), V2 sections 0, 1, 3 and 4 plus every register id and title, V3 sections 1, 2 (SW, CO, XC parts cited), 3, 4 (node table), 5 and 6, `seed-brief.md` Success Criteria and Open Questions, `scoring-pass1.md` IC rows. Checks re-run in this step (read-only, 2026-11-13, ROOT = `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`):

| Check | Result | Used by |
|---|---|---|
| `ls -d .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115 .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239` | both exist | Change 34 (X-001) |
| `sed -n` on `src/superclaude/core/WORKER-CONTRACT.md` lines 23, 41, 42, 62, 243, 244, 288 | `/sc:pr-submit` and `/sc:sweep` on the never-as-worker list (23); WC-9: no PR or push from a worker (41), a local commit only with a word-for-word quoted instruction (42); WC-13 (62); "PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session ... never as a worker" (243); unseen worker commits shown to the person before a push (244); re-arm on expiry, sweep at most once every 5 minutes (288) | Changes 1, 6, 10, 15 |
| `sed -n` on `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` lines 19, 47, 70, 241 | attended in-session poll loop (19); "MUST run in the main orchestrating session" (47); posts an "augment review" re-trigger (70); `--merge-guard {draft,off}`, default `draft` (241) | Changes 1, 5, 14 |
| `sed -n 23,24p src/superclaude/skills/sc-sweep-protocol/SKILL.md` | the `uv run` fallback runs "Only when step 1 fails with 'command not found'" | Change 6 |
| `ls .dev/sweeps/` | four reports, `20261112-031151` to `20261112-034511` | Change 16 |
| `git worktree list` (first lines) | main checkout `/home/coder/workspaces/IronClaude` at `495eb96d1 [docs/409-orca-dashboard-designs]` | Change 2 |
| ADJ lines 771, 781, 784, 794, 442, 710 | Q1, Q11, Q14, Q24 wording; cross-issue order "(1) owner answers ... (2) #450; (3) Coder#477; (4) #409 pass ...; (5) one #339 comment; (6) #423"; #423 research "may be done ahead of the rest" | Changes 3, 4, 7, 32, 38, 41, 42 |

Not re-checked here (taken from the cited debate files, which ran them): `filter.<driver>.process` behaviour (git documentation only, never run; R25-INV-004), live Orca state (the probe found the app not reachable; R25-INV-009), live PR and issue state (probe R25-INV-026, as of 2026-11-13).

### Naming conventions the merged spec must use

1. **Two invariant id spaces.** V1 already uses bare `INV-nnn` for the adjudicated document's ids (ADJ Part 5; V1 7.1). This debate's Round 2.5 probe (`invariant-probe.md`) reuses `INV-001` to `INV-028` for different findings. The merged spec writes this debate's probe ids as **`R25-INV-nnn`** everywhere and keeps bare `INV-nnn` for ADJ's. Example: ADJ `INV-008` (git config) is this probe's `R25-INV-018`. This plan uses the same convention from here on; "INV-001..016" in the Step 4 brief means `R25-INV-001` to `R25-INV-016`.
2. **Owner questions.** `Q1` to `Q24` are ADJ Part 7's. `Q25` to `Q33` are new from this debate. `Q-1`, `Q-2`, `Q-3` (with a hyphen) stay Orca gate tests (ADJ line 67). The Round 3 labels `N5` to `N10` (V1 advocate) and V2's `N1` to `N4` are not carried as ids; each is mapped in Change 63.
3. **Work-item ids.** V1's 46 ids are kept unchanged and never reused. Four new ids are added: `SW-14`, `V2-05`, `XC-10`, `XC-11` (50 items). V2 and V3 ids appear only in the old-to-new map (Change 61).
4. **New graph node kinds.** `GRANT(<item>,<action>)` (replaces V3's single `M-APPROVAL`), `ORCA-AVAILABLE`, `SWEEP-RUNNABLE`, `TB-GIT-ROW` (a ledger eligibility row, a procedural guard, not a code control), plus boundary nodes `TB-REMOTE`, `TB-RELAY`, `TB-EDIT`, `TB-WRITE`. Each is defined once, in section 4.1 of the merged spec.
5. **Provenance tags** are HTML comments, defined in "Merge-executor instructions", step 2.

### Index tables

**Base defects named in the Step 4 brief, and the Change that fixes each.**

| # | Defect in V1 | Where in V1 | Fixed by |
|---|---|---|---|
| D1 | False claim that the two task packages were "not found in this checkout" | V1:57 (0.4 item 5) | Change 34 (X-001) |
| D2 | JOIN (XC-04) may run the unfixed sweep before the INV-008 ruling holds in the code actually run | V1:322, V1:508 (W1 lane L-live) | Changes 7 and 35 (R25-INV-007, X-002); Change 16 (TB-GIT-ROW) |
| D3 | Default ledger path inside the #539 checkout | V1:319 against V1:332 (IC-V1-1) | Changes 2 and 45 (R25-INV-002, X-012) |
| D4 | Workers run `/sc:pr-submit --monitor 3`; a worktree created with `--agent` and then given a `worker-start` worker | V1:575 (6.3 Worker row); V1:327 (3); V1:567 (6.2) | Change 1 (R25-INV-001) |
| D5 | Blanket "never post, reply or merge without approval" against a mandated tool that pushes, replies and resolves without asking | V1:573, V1:633 against V1:584 rule 2 | Changes 44, 50, 13, 14 (X-011, A-002, R25-INV-013, R25-INV-014) |
| D6 | Register, graph and wave inconsistencies; the hard order stalls under Q3's default | IC-V1-1 (V1:319 vs 332), IC-V1-2 (V1:346 vs 436) | Changes 48, 61 and 3 (X-015, id map and validation, R25-INV-003) |

**Imports named in the Step 4 brief, item 4, and the Change that carries each.**

| Import | Source | Change |
|---|---|---|
| Evidence-tagged dependency edges with kinds | V2 4.2 | 19, 56 |
| Security regression acceptance (measured two-key test, widened) | V2 0.1, SW-02; R25-INV-004 | 23, 4 |
| Early dedicated #423 research item | V2 V2-04 | 28, 41 |
| CAP separated from JOIN | V1 XC-03; R25-INV-022 | 36, 7 |
| Capture recorded versus `working` class shipped | V2 Weak point W5, SW-13 | 42 |
| Observation methods ("Observe:", OBS-NOW) | V2 0.2, 0.3, section 2 | 22, 33 |
| Contract-completion rule | V3 section 1 | 24 |
| Read-capture versus seed-test operator roles | V3 role contract, concurrency rule 8 | 30 |
| Decision scope and lifetime; withheld-slot semantics | V3 section 3; R25-INV-003 | 60, 3 |
| Interruption and recovery rules | V3 sections 5 and 6 | 20, 30 |
| Two-scope acceptance gate | V3 XC-08 | 59 |
| ORCA-AVAILABLE prerequisite | R25-INV-009 | 9 |
| Runtime capability gate for the coordinator CLI | R25-INV-006 | 6 |
| Cadence record (WC-16 against the owner's recurring order) | R25-INV-010 | 10 |

## Planned Changes

### Part 1: one Change per invariant finding (R25-INV-001 to R25-INV-016)

Each Change states the rule the merged spec adopts, how the three Round 3 rules were reconciled, and what changes. "R3-Vn" = `round3-invariants-Vn.md`. Round 3 verdicts (V1 / V2 / V3) are from those files.

### Change 1: PR actor model; no worker runs `/sc:pr-submit` (R25-INV-001, HIGH; fixes D4)
- **Source**: Round 3 rules R3-V1 (split each PR item: supervised worker, then a coordinator-launched top-level PR session after `worker_done`), R3-V2 (each PR item is a top-level agent created with `worktree create --agent`, no worker), R3-V3 (hand back to an owner-designated ordinary top-level PR session). Verdicts VALID / VALID / VALID.
- **Target**: Base 6.3 Roles (Worker row, new PR session row), 6.2, 6.4 rule 2, XC-09 (3), every PR item's "runs in" cell (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07), 7.2 Interaction rows (replace + insert).
- **Rule adopted**: (1) `/sc:pr-submit --monitor 3` runs only in an ordinary top-level **PR session**, never in a `worker-start` worker and never in the coordinator itself (`WORKER-CONTRACT.md:23`, `:41`, `:243`; `sc-pr-submit-protocol/SKILL.md:47`). (2) A worktree gets its agent either from `worker-start` or from `worktree create --agent`, never both; delete V1's "creates worktrees ... with `--agent` ... and dispatches only through supervised `worker-start`" (XC-09 (3)) and replace it with that rule. (3) A worker makes and tests the change and stops at `worker_done`; it has no PR, push or post. (4) Only after the coordinator admits `worker_done` and the worker's session has ended does the owner-designated PR session open or attach the PR in that worktree, so one worktree never holds two live agents. (5) The coordinator never runs the attended poll loop, so its WC-16 watch is never blocked; it tracks each PR by `gh pr view <N> --repo IronbellyOrg/IronClaude` at wakes. (6) The PR session's writes are bounded by the GRANT row of Change 13 and the write list of Change 14.
- **Reconciliation**: all three agree on (1), (2) and (5). They differ on who starts the PR session. Picked V3's framing (owner designates) with V1's mechanics as the recommended answer, because V1's split keeps the code change under worker supervision and WC-13, while V2's route drops `worker_done` and WC-13 binding (probe R25-INV-001: an unsupervised `--agent` session "is not a worker, sends no `worker_done`, is not bound by WC-13"). V2's route stays an owner option in Q25.
- **New owner question**: **Q25** "Who runs `/sc:pr-submit --monitor 3` for each program PR?" Recommended: an owner-designated top-level PR session per PR, launched by the coordinator with `orca agent launch` in the item's worktree after the worker's `worker_done` is admitted and its session has ended, closed when the PR merges (that Orca permits a second, sequential agent launch in a `worker-start` worktree is UNVERIFIED; the owner confirms). Alternative: V2's top-level agent per PR item. Default if unanswered: no PR is opened; the change stays uncommitted in its worktree; the lane is held.
- **Graph**: every PR item gains a DEC edge from Q25 and a GATE edge from `GRANT(<item>,pr-submit)`.
- **Rationale**: probe R25-INV-001 HIGH UNADDRESSED; X-011/A-002 (NEITHER, 93.0) covered scope only, not the actor.
- **Risk**: High. It touches every PR item and three sections; a missed "runs in" cell leaves a worker with a PR duty.

### Change 2: Coordinator home and the ledger's branch (R25-INV-002, HIGH; fixes D3 with Change 45)
- **Source**: R3-V1 PARTLY (owner creates a program worktree with `--agent` whose agent is the coordinator), R3-V2 VALID (main checkout, per project CLAUDE.md "Session A: Open the main checkout (current branch); it is the orchestrator"; owner gives it a program branch), R3-V3 PARTLY (owner-selected existing checkout, main allowed, plus the branch authorized to hold the ledger; no implied branch switch).
- **Target**: Base XC-01 "Location", XC-09 "runs in", 5.4 and 6.2 worktree map, 6.1 "Decision ledger" row, 6.4 rule 3 (replace).
- **Rule adopted**: (1) The coordinator never runs in the #539 checkout and no program artifact (ledger, records, debate files, research packages) is created there. (2) No session creates a worktree for its own use (project CLAUDE.md). (3) Before W0 exits, the owner names the coordinator's home and the branch that stages the always-staged ledger package `.dev/tasks/<program-package>/` (project rule: `.dev/tasks/` is always staged; staging is not committing). (4) The ledger is committed only when the owner asks. (5) The coordinator never switches a checkout's branch on its own.
- **Reconciliation**: V1 and V3 are right that a human may create a worktree that gets an agent, so the probe's "only the main checkout" is too strong (PARTLY). V2 and V3 both allow the main checkout, which the project rule names as the orchestrator's place; V1's route depends on an `--agent`-launched agent counting as "person-opened", which no source confirms. Recommended answer follows V2 and V3; V1's route stays an option.
- **New owner question**: **Q26** "Where does the coordinator run, and on which branch is the ledger package staged?" Recommended: the main checkout (`/home/coder/workspaces/IronClaude`, today on `docs/409-orca-dashboard-designs`), on a dedicated program branch from `origin/master` that the owner switches to only after the current work there is safe. Alternative: an owner-created Orca worktree with `--agent` whose agent is the coordinator. Default if unanswered: XC-09 does not start; the owner keeps the ledger by hand; no program file is written on any branch; SW-01's ruling is recorded as the owner's reply on the Codex thread only (the ruling never waits for the ledger: R2-V3 fix 2).
- **Graph**: Q26 -> XC-09 (DEC); XC-10 exit checks Q26 answered or defaulted.
- **Rationale**: R25-INV-002 HIGH; X-012 MERGE 86.7; A-005 MERGE 86.0.
- **Risk**: Medium. If the owner answers "main checkout, current branch", the ledger is staged on an unrelated docs branch; the spec must say that is the owner's accepted cost.

### Change 3: Skip rule for the hard publication order, with withheld-slot semantics (R25-INV-003, HIGH; fixes IC-V1-2)
- **Source**: R3-V1 and R3-V2 (mechanical skip rule, no owner question), R3-V3 (ordered publication slots; withheld is not completed and does not satisfy content or decision dependencies; reopening needs a fresh authorized edit pass; asks owner approval).
- **Target**: Base XC-02 (append criterion 6), 3 "Default if unanswered" cells of Q2, Q3, Q20 (amend), 4.2 PROC edges WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01, 6.5 row "A gated Q is unanswered" (amend), WA-02 (append).
- **Rule adopted**: The order #450 -> Coder#477 -> #409 pass -> #339 comment -> #423 (ADJ line 442) stays hard (PROC) between links that are posted. A link whose owner answer is defaulted to "not posted" (or declined) is recorded in the ledger as `skipped (default Qn, date)` and the next link becomes eligible. Skipped is not completed: it satisfies the order edge only, never a DEC or content edge (for example V2-01's "if #477 is kept" clause still needs Q3). A later link never cites text from a skipped link. A skipped link posted later goes through XC-02 with a fresh `updatedAt` read, and any cross-link it needs in an already-posted issue is added by a new ordered edit. Inside the single #450 edit set (WA-02), an edit whose own Q defaulted (edit 1 under Q2, edit 4 under Q20) is omitted and recorded; the set still posts once.
- **Reconciliation**: V1 and V2 agree; V3 adds the "withheld is not completed" and content-dependency clauses, which are adopted. V3's request for a separate owner approval is not adopted (see "not made" row 24): the rule is derived from ADJ line 442 ("the order is mainly for cross-links") and changes no owner default.
- **New owner question**: none.
- **Rationale**: R25-INV-003 HIGH; scoring IC-V1-2; X-005 V1 92.3 keeps the order hard.
- **Risk**: Low.

### Change 4: Widen the INV-008 requirement to effective executable paths (R25-INV-004, HIGH)
- **Source**: R3-V1, R3-V2, R3-V3 (all VALID); git 2.47.3 `gitattributes(5)` on `filter.<driver>.process` (documentation only, not run).
- **Target**: Base 0.1 (append), SW-01 (append (4)), SW-02 F1/F2 criterion (1) (replace), 4.1 TB-GIT row (replace), 7.2 Guard row, 7.3 first row (replace), Q1 row in section 3 (widen).
- **Rule adopted**: The requirement is stated by outcome: no command that repository configuration or the inherited environment defines runs during any `git status` the sweep runs. SW-02's regression test fails, for F1, if a `core.fsmonitor` hook, a `filter.<d>.clean` command or a `filter.<d>.process` command runs (each set once in shared config and selected by `.gitattributes`); for F2, if a worktree defining any of them is scanned rather than reported `unscanned`. The ruling states whether `include.path`/`includeIf` config and inherited `GIT_*`/`GIT_CONFIG_*` variables are in scope. TB-GIT counts as satisfied only when the landed test covers every channel the ruling puts in scope; a two-key test alone never declares JOIN safe. **No code fix is specified.** INV-008 (ADJ) stays first and UNRESOLVED-EXTERNAL with the owner (this probe's R25-INV-018).
- **Reconciliation**: all three agree. Adopted V2's outcome wording and test list, V3's "effective invocation" framing, V1's "TB-GIT satisfied only when the test covers the ruled set".
- **New owner question**: none new; **Q1 is widened** with part (b): "Does your INV-008 ruling cover `filter.<driver>.process`, config pulled in by `include.path`/`includeIf`, and inherited `GIT_*`/`GIT_CONFIG_*` variables?" Recommended: yes to all, and the ruling names any channel it leaves out. Default: as Q1 (#539 stays open, no caveat added).
- **Rationale**: R25-INV-004 HIGH; C-001 V2 88.0.
- **Risk**: Low (requirement text only).

### Change 5: No monitored PR tool on #539 before the ruling is applied (R25-INV-005, HIGH)
- **Source**: R3-V1 (no `--monitor 2/3` until SW-02 lands and the Codex thread is resolved under the ruling), R3-V2 (`--monitor 1` before; afterwards `--monitor 3` with the Codex thread excluded), R3-V3 (hold monitor-3 until Q1 applied, checked and remediation scope authorized; do not assume a thread-exclusion capability; do not silently lower the mandated level).
- **Target**: Base SW-02, SW-03, SW-05 "runs in" and criteria (append), 6.3 "#539 author" row (replace), 6.5 (new row), 6.9 (append).
- **Rule adopted**: `/sc:pr-submit` is not attached to PR #539 at `--monitor 2` or `3` until SW-02 has landed the owner's Q1 ruling and the Codex security thread at `probes.py:1211` is closed by the owner's ruling reply (SW-01). Until then the #539 author pushes by hand, staging named paths only, and no tool designs or pushes an INV-008 fix. `--monitor 1` (propose only) is allowed only if the #539 GRANT row says so explicitly. After the ruling is applied, `--monitor 3` runs only under a GRANT row that lists every write (Change 14). A new finding that needs an owner ruling stops the run before any fix, reply or resolve.
- **Reconciliation**: all agree no level 2 or 3 before the ruling. V2's "Codex thread excluded from the tool even afterwards" is not adopted, because no exclusion switch was found in the skill (V3; probe marks the Codex selection rule UNVERIFIED); closing the thread by the owner's reply removes the need.
- **New owner question**: **Q28** (shared with Change 14) "What may `/sc:pr-submit` do on PR #539?" Recommended: nothing before SW-02 lands the ruling; after it, `--monitor 3` once the Codex thread is closed by your reply, with `--merge-guard off` (no draft toggle on a large, long-open PR). Default if unanswered: no `/sc:pr-submit` on #539 at any level; the author pushes by hand.
- **Rationale**: R25-INV-005 HIGH; X-011, A-002 NEITHER 93.0.
- **Risk**: Medium (adds a manual push path for #539).

### Change 6: Runtime capability gate SWEEP-RUNNABLE (R25-INV-006, MEDIUM)
- **Source**: R3-V1, R3-V2, R3-V3 (all VALID); `superclaude sweep --help` prints "No such command 'sweep'" in the installed uv-tool CLI (probe; R3-V2); `sc-sweep-protocol/SKILL.md:23-24` fallback runs only on "command not found" (re-checked in this step).
- **Target**: Base 7.3 row 2 (replace), 6.6 bullet 2 (replace), 4.1 (new node), 6.5 (new row), XC-04 blocked-by (append).
- **Rule adopted**: New node **SWEEP-RUNNABLE**: satisfied when, after SW-05 and after the owner's distribution route has run, `superclaude sweep --help` exits 0 in the coordinator's own environment and `/sc:sweep` produces one report; the result and date go in the ledger. Until then the WC-16 `/sc:sweep` duty is recorded as "not runnable", the coordinator runs only "The sweep." under Liveness supervision, and sweep-dependent work (XC-04) is held. No in-place reinstall on the authority of this spec or of memory (V3). The skill's narrow fallback condition is logged as a #534 row (SW-06), not edited inside #539 (A-004).
- **New owner question**: **Q29** "After #539 merges, how does this host's `superclaude` CLI get the sweep command: the Coder template update or an owner-approved uv-tool reinstall?" Recommended: the Coder template (owner memory `ironclaude-updates-only-via-coder.md`, lowest source tier, so asked). Default: duty "not runnable"; XC-04 held.
- **Rationale**: R25-INV-006 MEDIUM; A-001 V1 94.3 (the availability caveat is V1's, the install claim is wrong).
- **Risk**: Low.

### Change 7: JOIN after the merge, from a named runner, root and destination (R25-INV-007, MEDIUM; fixes D2 with Change 35)
- **Source**: R3-V1 and R3-V2 (JOIN after SW-05 plus the capability gate, Q24 runner, master-based checkout; both reverse their Round 2 timing), R3-V3 (record actor, revision, root and report destination; allows a pre-merge run by the authorized #539 owner).
- **Target**: Base XC-04 (replace criterion (4), blocked-by, runs in), 5.1 W1 lane L-live and W1 exit (remove XC-04), W3 lane L-note (insert XC-04 before XC-07), 5.4 row for this checkout (remove "the sweep run in XC-04 if done before merge").
- **Rule adopted**: XC-04 runs after SW-05, SWEEP-RUNNABLE and a TB-GIT-ROW entry (Change 16), by the Q24 runner, with the sweep run as `superclaude sweep run --run <id>` on master code. Its record names the actor, the executable revision, `--root`, and the report destination (the sweep writes `<root>/.dev/sweeps/`; probe cites `sweep/commands.py:220-240`), plus the observer's `dispatchId` list from the same Run in the same sitting. CAP (XC-03) is unchanged and stays in W1 (Change 36).
- **Reconciliation**: V1 and V2 agree; V3's record fields adopted; V3's pre-merge option not adopted ("not made" row 9), because the only consumers of JOIN's result (XC-07, and the soft "join key" words in OB-08) already wait for SW-05 or use "candidate join basis", so waiting costs no schedule.
- **New owner question**: none (Q24 names the runner).
- **Rationale**: R25-INV-007 MEDIUM; X-002 V2 94.3.
- **Risk**: Medium (moves an item across waves; W1 and W3 exit checks change).

### Change 8: OB-04 names its target Run and actor (R25-INV-008, MEDIUM)
- **Source**: R3-V1 (a non-critical coordinator Run the owner names), R3-V2 (a throwaway coordinator Run opened for the test, no real workers, written acceptance), R3-V3 (a disposable representative Run with a `--wait`/ack workload, never the alignment Run; usability stays a separate requirement).
- **Target**: Base OB-04 (replace criteria and "runs in"), 6.3 Live reader row (amend: OB-04 is not run "from a terminal that holds no Run"), 4.2 (Q30 -> OB-04 DEC; `GRANT(OB-04,live-read)` GATE).
- **Rule adopted**: OB-04 runs only after OB-03 passes (GATE, C-003), in the holder terminal of an owner-approved coordinator Run that is never the alignment coordinator's own and carries no work whose questions matter; the Run is disposable and representative (a live `--wait` listener and an ack cycle). The record names the Run id, the terminal, whether any question disappeared, and whether the panel was usable. If no such Run exists, OB-04 is held and OB-06 waits.
- **New owner question**: **Q30** "Which coordinator Run may OB-04 read, and do you accept in writing that its questions may be consumed?" Recommended: a disposable representative Run you open for the test, never the program's own. Default: OB-04 held; OB-06 not opened.
- **Rationale**: R25-INV-008 MEDIUM; ADJ INV-024 (Q-1 FAIL: only the holder terminal reads).
- **Risk**: Low.

### Change 9: ORCA-AVAILABLE prerequisite and stop trigger (R25-INV-009, MEDIUM)
- **Source**: R3-V1, R3-V2 (stop trigger, retry once per WC-16 interval, ask owner once), R3-V3 (ORCA-AVAILABLE as an intake and resume prerequisite; no tight failure and re-arm loop; only a successful readback reopens the gate).
- **Target**: Base 4.1 (new node ORCA-AVAILABLE beside LIVE), 4.2 (ORCA-AVAILABLE -> XC-03, XC-04, OB-03, OB-04, WA-04 and every worker dispatch), 6.5 (new row), XC-10 (Change 51) exit check, 5.5 interruption rule (Change 20).
- **Rule adopted**: "Orca app not reachable" holds every live lane (CAP, JOIN, OB-03, OB-04, FU-1, any dispatch or wait), writes one ledger row with the time, retries at most once per WC-16 interval (5 minutes), and asks the owner once to start Orca. Non-live lanes (issue drafts, note draft, GitHub-only items) continue. A failed re-arm is never counted as work settled. The gate reopens only on a successful read. The spec does not claim the probe's outage is still current.
- **New owner question**: none (starting Orca is a request, not a decision).
- **Rationale**: R25-INV-009 MEDIUM; base-selection RISK-4 residual.
- **Risk**: Low.

### Change 10: Cadence record replaces "no extra scheduler" (R25-INV-010, MEDIUM; owner confirms)
- **Source**: R3-V1, R3-V2, R3-V3 (all VALID; all withdraw their Round 2 categorical "no scheduler"); `WORKER-CONTRACT.md:288` ("Phase 1 adds this duty, not a scheduler" concerns the `/sc:sweep` duty); owner memory `coordinator-never-stop-polling.md` (2026-11-05 order; lowest source tier).
- **Target**: Base 6.6 (restructure into a cadence table), V1 6.6 bullet 4 "GitHub state ... not on a timer" (replace), base-selection preserved strength 9 (amend).
- **Rule adopted**: 6.6 becomes a cadence record with rows: WC-16 re-arm on every expiry and `/sc:sweep` at most once per 5 minutes once SWEEP-RUNNABLE holds; observer 15 s (one instance for the coordinator); watcher cron 5 minutes after FU-2; PM 30 minutes; GitHub state read at wave gates and before each edit; and a row "owner's recurring read-only check (about 10 minutes, off the hour and half-hour: Orca Run, ListAgents, open PRs on `IronbellyOrg/IronClaude` and `IronbellyOrg/Coder`, idle subscriptions)" whose status is Q31's answer. That check never runs `/sc:sweep` more often than WC-16 allows and never writes.
- **New owner question**: **Q31** "Does your 2026-11-05 recurring-check order apply to this program's coordinator?" Recommended: yes, read-only. Default: WC-16 only, and Q31 is shown open at the top of the ledger (the spec does not pick an answer from memory either way).
- **Rationale**: R25-INV-010 MEDIUM; X-014 V1 84.0 is kept only for the coordinator's own work clock (V3's housekeeping tick stays rejected).
- **Risk**: Low.

### Change 11: F3 caveat inventory by grep, not four texts (R25-INV-011, MEDIUM)
- **Source**: R3-V1, R3-V2 (grep pattern), R3-V3 (reviewed inventory, mirrors equal).
- **Target**: Base 0.1 ("F3 accept and caveat four texts": replace), SW-02 F3 branch (replace), 7.1 INV-010 row (replace "four caveats"), 3 Q1 row and "What the first four answers do" (replace "four caveats").
- **Rule adopted**: Under F3, every statement in #539's files that calls the sweep read-only or says it changes nothing else, found by `git grep -n -i -E 'read-only|changes nothing'` over #539's file list at ruling time, carries the caveat or is listed in the PR body with the reason it is not about the sweep. At least the 16 locations the probe names; the plugin mirror `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` stays byte-equal to the source.
- **New owner question**: none (Q1 = F3 already decides the caveat).
- **Rationale**: R25-INV-011 MEDIUM.
- **Risk**: Low.

### Change 12: Where SW-02's own plan package lives (R25-INV-012, MEDIUM)
- **Source**: R3-V1 PARTLY (may be staged in #539), R3-V2 PARTLY (only if the owner allows; recommended yes), R3-V3 PARTLY (decide explicitly; reuse an adequate existing plan; keep alignment artifacts out).
- **Target**: Base 6.4 rule 5 and 6.9 bullet 8 (replace "No JSON key, file or sidecar" with A-004's exact scope), SW-02 (append), SW-05 (4) (keep: "no added sweep JSON key or sidecar").
- **Rule adopted**: A-004 forbids, inside #539, a new program, collector, JSON key, sidecar or report file, and every program artifact of this alignment work. SW-02's own plan package (the CLAUDE.md hard limit requires a written plan for a change across several source files) is a separate question: first check whether an adequate existing plan covers SW-02 (V3); if a new one is needed, it enters #539 only under Q27.
- **New owner question**: **Q27** "May SW-02's own `/sc:workflow` plan package be committed inside PR #539?" Recommended: yes (it is not a program, collector, key or sidecar; probe R25-INV-012 counts 921 `.dev/tasks/to-do/*` files already in #539). Default: the package is written in the coordinator home (Q26) and referenced by absolute path; #539 commits stage named code and test paths only.
- **Rationale**: R25-INV-012 MEDIUM (PARTLY in all three).
- **Risk**: Low.

### Change 13: GRANT records replace a single approval node (R25-INV-013, MEDIUM; part of D5)
- **Source**: R3-V1 (rows keyed by PR or issue and action, with lifetime), R3-V2 (fields: item, PR or issue, action, monitor level, excluded threads, allowed writes, date, lifetime; `APPROVAL(<item>,<action>)` nodes), R3-V3 (grant records keyed by repository, PR/issue/test, actor, action, scope, validity and revocation).
- **Target**: Base 6.8 ledger format (append a second table), XC-01 (append criterion), 4.1 (new node kind), 4.2 (every outward edge), 6.3 Owner row (replace "approves every outward post").
- **Rule adopted**: XC-01 holds a **grant table**: `grant id | repository | item | PR, issue or test | actor | action | scope and allowed writes | monitor level | owner wording | date | lifetime and revocation`. Actions: `pr-submit`, `merge`, `issue-write`, `thread-reply`, `live-read`, `seeded-write`, `live-test`, `commit`, `draft-toggle`. The graph uses `GRANT(<item>,<action>)`; an edge is satisfied only by a matching row. A push grant satisfies neither merge, issue write nor live test. A row is void when a Q it depends on changes (decision lifetime, Change 60).
- **New owner question**: none (each row is itself an owner approval).
- **Rationale**: R25-INV-013 MEDIUM; S-005 MERGE 81.3 imported `M-APPROVAL`, which this replaces.
- **Risk**: Medium (every outward edge in the graph changes).

### Change 14: The pr-submit grant lists every write the tool makes (R25-INV-014, MEDIUM; part of D5)
- **Source**: R3-V1, R3-V2, R3-V3 (all VALID); `SKILL.md:70` (re-trigger comment), `:241` (`--merge-guard` default `draft`), probe cites `:234` (create or attach) and `:306` (troubleshoot artifacts).
- **Target**: grant table of Change 13 (field "allowed writes"), 6.4 rule 2 (append), every PR item (append a criterion "run under GRANT(<item>,pr-submit)").
- **Rule adopted**: A `pr-submit` grant row lists: PR create or attach; local fix commits and `sc:troubleshoot` artifacts in the worktree; push; thread replies and resolves; the "augment review" / Codex re-trigger comments; the draft and ready toggle under `--merge-guard draft`, or `--merge-guard off` when the owner does not approve the toggle; resume effects. An unlisted write needs a new row; without consent the run is held, and no exclusion switch is invented. Before the PR session pushes worker changes the person has not seen, the coordinator shows them to the person (`WORKER-CONTRACT.md:244`). Merge is never in this row.
- **New owner question**: none new; the #539 draft toggle is part of **Q28** (Change 5). Recommended for new small PRs: approve `--merge-guard draft`.
- **Rationale**: R25-INV-014 MEDIUM.
- **Risk**: Low.

### Change 15: Who commits a worker's change (R25-INV-015, MEDIUM)
- **Source**: R3-V1 (ask the owner for per-Task commit wording; recommended yes), R3-V2 (top-level agents commit their own work; workers commit only with a quoted grant), R3-V3 (default no worker commits; an ordinary PR or coordinator actor commits; never manufacture a quote from generic PR consent).
- **Target**: Base 6.3 Worker row, 6.4 (new rule), worker brief requirements (6.10 from Change 30).
- **Rule adopted**: By default a supervised worker leaves its changes uncommitted and unstaged outside WC-9's grant; the PR session (Change 1) stages and commits named paths with exclusive use of the worktree, after the coordinator has shown the person any change they have not seen. A worker commit happens only when its brief quotes, word for word, an owner instruction naming a local commit for that Task, recorded as `GRANT(<item>,commit)` (`WORKER-CONTRACT.md:42`).
- **Reconciliation**: two of three (V2, V3) keep commits away from workers by default; V1's per-Task wording is kept as the owner's option.
- **New owner question**: **Q32** "May supervised workers make one end-of-Task local commit? If yes, give the sentence to quote." Recommended: no; the PR session commits. Default: same as recommended. Asked only when the first code-changing worker is dispatched.
- **Rationale**: R25-INV-015 MEDIUM.
- **Risk**: Low.

### Change 16: TB-GIT as a ledger eligibility row before every sweep run (R25-INV-016, LOW)
- **Source**: R3-V1, R3-V2, R3-V3 (all VALID); `ls .dev/sweeps/` (four reports, 2026-11-12; re-checked here).
- **Target**: Base 4.1 (new node TB-GIT-ROW), XC-04 (append), 6.4 rule 1 (append), 7.4 (new edge case).
- **Rule adopted**: Before any sweep run by any program session, a ledger row records the ruling status, the code revision run, and the runner's authority. The four existing `.dev/sweeps/` reports (`20261112-031151` to `20261112-034511`) are marked "pre-INV-008, not JOIN evidence". With Change 7, the program runs no sweep before SW-05. The spec calls this a procedural guard, not a mechanical block (V3).
- **New owner question**: none.
- **Rationale**: R25-INV-016 LOW.
- **Risk**: Low.

### Part 2: one Change per debate point (44 points)

Winner and confidence are from the `debate-transcript.md` Scoring Matrix (Round 2 FINAL tables). "Keep" Changes record a V1 point the merge must not lose.

### Change 17: Skeleton: V1 sections plus V2 weak points and V3 interface blocks (S-001, MERGE 68.3, unanimous)
- **Source**: V1 sections 0-7 (with 0.6 and 7.5); V2 Weak point blocks; V3 per-system interface, failure and runbook blocks.
- **Target**: Base, all H2 sections kept in order; per-system sections 2.1-2.6 gain two sub-blocks after "Risks": "Weak points" (Change 57) and "Interface contracts" (Change 58) (insert).
- **Rationale**: S-001 Round 2: "V1 seed-ordered skeleton; add V2 weak points, V3 interface blocks".
- **Risk**: Low (additive).

### Change 18: Keep V1's register and ids; add four ids (S-002, V1 67.5)
- **Source**: V1 4.1 register (46 items).
- **Target**: Base 4.1 "Work items" count (46 -> 50) and section 2 tables (append rows SW-14, V2-05, XC-10, XC-11).
- **Integration**: keep every V1 id with its meaning; add only the four new ids; record every V2 and V3 id in the map of Change 61.
- **Rationale**: S-002 Round 2: V1 has the fewest reversals; V2 would collapse WA-02/03/04 and drop CO-01.
- **Risk**: Medium (any re-keyed content risks a wrong target id; Change 61 validates).

### Change 19: Replace the text graph with an evidence-tagged edge table (S-003, V2 86.3, unanimous)
- **Source**: V2 4.2 (70 numbered edges, kinds FILE, PIN, GATE, DEC, PROC, SOFT, each with evidence), V2 4.4.
- **Target**: Base section 4: 4.1 Node legend (extend), 4.2 becomes the numbered edge table `# | From | To | Kind | Evidence | Provenance` (restructure), 4.3 text graph regenerated from the table as a summary view (replace), 4.4 graph checks (V1 4.3 extended by Change 61's validation), 4.5 "Where this graph differs from ADJ Part 4.1" (V2 4.4, updated per Changes 38, 40, 35: drop the "Demoted to SOFT" row; add "TB-GIT, SWEEP-RUNNABLE -> XC-04", "no XC-05 -> OB-06").
- **Integration**: seed the table by re-keying V2's 70 edges through Change 61's map; then add every V1 edge V2 lacks, with its V1 evidence; then apply the debate changes: V2 edge 19 SOFT -> GATE (C-003), edges 47 and 50 SOFT -> PROC (X-005), V2's three #450 write items collapsed into WA-02 (X-006), edge 61 replaced (JOIN after SW-05, SWEEP-RUNNABLE, TB-GIT-ROW; Change 7), GRANT and Q25-Q33 edges added (Changes 1-15). SOFT edges never block a wave.
- **Rationale**: S-003, U-004: only V2 gives kind and evidence per edge.
- **Risk**: High (largest rewrite; the table is authoritative and the text graph must be regenerated from it, never hand-edited).

### Change 20: Waves: V1 schedule, V2 lists, V3 interruption and concurrency rules (S-004, MERGE 74.3, unanimous)
- **Source**: V1 5.1-5.4; V2 section 5 lists "can run today", "waits for #539", "never waits for #539"; V3 "Lockstep and concurrency rules" 1, 3, 4, 8 and "Wave interruption rule".
- **Target**: Base 5.1 (amend rows per Changes 7, 9, 28, 51, 59), 5.2 (extend into the three lists, recomputed from the edge table), new 5.5 "Concurrency rules" (V3 rules 1, 3, 4, 8, deduplicated against 5.3), new 5.6 "Wave interruption rule" (V3: re-read authoritative state before any write at resume; "An expired polling wait is not an exit gate"; a completed predecessor is reused only while its evidence still applies).
- **Rationale**: S-004 Round 2: "V1 waves and serial table; V3 interruption rule; V2 lists"; all three Round 2 fix lists ask for the interruption rule (M-09).
- **Risk**: Medium (wave rows must be re-checked against the edge table: Change 48).

### Change 21: Boundary and contract node set (S-005, MERGE 81.3, unanimous)
- **Source**: V1 TB and K names; V2 TB-3 (route from outside a workspace that can start a session) and TB-6 (strings relayed between programs or agents); V3 B-EDIT, B-WRITE, M-APPROVAL.
- **Target**: Base 4.1 TB table (append TB-REMOTE from V2 TB-3 and V3 B-IDENTITY, TB-RELAY from V2 TB-6, TB-EDIT from V3 B-EDIT, TB-WRITE from V3 B-WRITE), plus gate nodes ORCA-AVAILABLE, SWEEP-RUNNABLE, TB-GIT-ROW and the GRANT family (Change 13). M-APPROVAL is not added as a node.
- **Integration**: add edges TB-REMOTE -> CO-03, CO-04; TB-RELAY -> V2-04, OB-09; TB-EDIT -> every issue write (WA-02, CO-01, OB-08, SW-09, V2-01, SW-06, SW-01 thread reply); TB-WRITE -> SW-12, WA-07, OB-09.
- **Rationale**: S-005 Round 2: "V1 TB names, V2 TB-3, V3 M-APPROVAL and B-EDIT"; R25-INV-013 replaces M-APPROVAL.
- **Risk**: Low.

### Change 22: Table conventions: named worktrees, "Observe:", wave column, decision lifetime (S-006, MERGE 76.0, unanimous)
- **Source**: V1 named worktrees and "Wave needed by"; V2 "Observe:" clause; V3 decision lifetime.
- **Target**: Base 0.5 (append the "Observe:" rule), every acceptance cell in section 2 (append "Observe: <command, file or record>"), section 3 (Change 60).
- **Integration**: take V2's "Observe:" text verbatim where V2 has the same item (via Change 61's map); write one for the others from the criterion itself. V3's role letters are not used.
- **Rationale**: S-006 Round 2.
- **Risk**: Low (wording only; many cells).

### Change 23: INV-008 requirement and regression test detail (C-001, V2 88.0, 2 of 3)
- **Source**: V2 0.1 requirement sentence (two branches: no hook or filter runs, or owner accepts with caveats in the same PR); V2 SW-02 test detail (`core.fsmonitor` hook, `filter.probe.clean`, `* filter=probe` in `.gitattributes`; F1 fails if either runs; F2 fails if scanned rather than `unscanned`); V3 "ruling separate from apply; ruling must not await ledger creation".
- **Target**: Base 0.1 (insert the requirement sentence), SW-02 criterion (1) (replace with V2's test, widened by Change 4), SW-01 (amend: ruling recorded on the Codex thread first, ledger row when the ledger exists).
- **Integration**: requirement-only stays; no code fix named; SW-01 and SW-02 stay separate items.
- **Rationale**: C-001 Round 2: "measured regression, scope separation, refusal falsifier"; ADJ line 206 "Keep the probe experiment as the regression test" (R2-V1 fix 11).
- **Risk**: Low.

### Change 24: Chain to target: root cause column and contract completion rule (C-002, MERGE 77.3, unanimous)
- **Source**: V2 section 1 "Root cause of the gap" column and the sentence "After this first release the chain is still broken at L1 and L3"; V3 "Contract completion rule" (producer, consumer, identity, version, authority, retry, interruption, receipt, rollback; "No item may be accepted merely because an upstream item completed").
- **Target**: Base 1.1 table (insert column after "Evidence"), 1.2 (append the sentence), new 1.5 "Contract completion rule" (insert).
- **Integration**: V1's "What the near-term waves deliver instead" column stays. L1 row: nearest design cites the existing research package (Change 34).
- **Rationale**: C-002 Round 2: "V1 interim deliverables, V2 root cause, V3 completion rule".
- **Risk**: Low.

### Change 25: Keep the seed-before-live guard flip sequence (C-003, V1 84.3, unanimous; keep)
- **Source**: V1 OB-03 -> OB-04 (hard) -> OB-05 -> OB-06.
- **Target**: Base OB-03 to OB-06 kept; the edge OB-03 -> OB-04 is GATE in the edge table.
- **Integration**: OB-04's content changes by Change 8 only; OB-06's XC-05 edge goes by Change 40.
- **Rationale**: C-003: live-layout read on a real Run before the seeded test risks consumption (X-016); V2 conceded.
- **Risk**: Low.

### Change 26: Keep seven watcher items and one #450 edit set; add watcher contracts (C-004, V1 81.0, unanimous; keep)
- **Source**: V1 WA-01 to WA-07; V3 launch interface contract and interruption runbook (V3:167, :171).
- **Target**: Base 2.3 (keep); interface block inserted by Change 58.
- **Rationale**: C-004: one #450 edit set (A-011); V2 conceded.
- **Risk**: Low.

### Change 27: One Coder#477 reply carrying the Q4 line; audit reconciliation (C-005, MERGE 73.3, unanimous)
- **Source**: V1 CO-01 (2) (one reply states Q4's answer in one line); V3:198 ("CO-02 must reconcile the source's no-write status criterion with its read-audit requirement").
- **Target**: Base CO-01 (keep), CO-03 (append criterion: "a status read may append a read-audit event but changes no other observable state; the no-write criterion is reconciled with the read-audit requirement in the design").
- **Rationale**: C-005 Round 2: "V1 one reply with Q4 line; V3 audit reconciliation". V2's separate owner one-liner is not imported ("not made" row 14).
- **Risk**: Low.

### Change 28: #423 decomposition: gated brainstorm, ungated research (C-006, V2 90.3, unanimous)
- **Source**: V2 V2-03 (brainstorm, gated) and V2-04 (research, "runs any time"); ADJ line 710.
- **Target**: Base V2-03 (remove criterion (2); keep brainstorm and design; blocked-by V2-02 and XC-05 unchanged), new **V2-05** "Dedicated `/tech-research` on multi-agent memory and context" (insert after V2-04).
- **V2-05 content**: acceptance: report saved in its own master-based worktree (PLAN INFERENCE name `issue-423-research`, created by the coordinator through Orca with `--agent`), its path recorded in the ledger, linked on #423 only under `GRANT(V2-05,issue-write)` through XC-02. Blocked-by: none (V2-01 SOFT). Blocks: V2-03 (SOFT), V2-04 (GATE: "do not begin implementation before both are complete", ADJ Part 6.4). Wave: W1 or any later wave. Q: none. Undo: yes.
- **Rationale**: C-006 Round 2: ADJ line 710 research "may be done ahead of the rest".
- **Risk**: Low.

### Change 29: Contract note: early draft, test after merge, full content list (C-007, MERGE 78.0, unanimous)
- **Source**: V1 XC-05/XC-06/XC-07; V3 "Contract-note content" list (V3:250-267) and the 9-row word mapping table (V3:269-281).
- **Target**: Base XC-05 acceptance (append: "contains every item of the content list and the 9-row word mapping table in 2.6"), section 2.6 (insert both lists after the XC table).
- **Integration**: V1 timing kept (draft in W1, test and link after SW-05); XC-05 is never committed in the #539 checkout (INV-031).
- **Rationale**: C-007 Round 2: "draft early, test after merge (SC-28); V3 content list and mapping".
- **Risk**: Low.

### Change 30: Orchestrator session: verified map, V3 roles, evidence handoff and resume (C-008, MERGE 80.7, unanimous)
- **Source**: V1 6.4 guardrails and 6.5 stops; V2 6.2 worktree map verified by `git worktree list` (with `issue-394-launch-level-hook` "do not touch" and the main checkout row); V3 role contract (read-capture operator, seed-test operator, independent reviewer), concurrency rule 8, "Evidence handoff and resume" (V3:547-551).
- **Target**: Base 5.4 and 6.2 (replace with V2's verified rows plus V1's proposed rows, updated by Change 2), 6.3 (add rows Read-capture operator, Seed-test operator, PR session (Change 1); the Live reader row splits into the two operators), new 6.10 "Evidence handoff and resume" (insert).
- **Integration**: shared capture (read-only) and seeded test (writes, then consumes) get separate grants: `GRANT(XC-03,live-read)` and `GRANT(OB-03,seeded-write)`. A launch receipt or a self-reported done is not acceptance.
- **Rationale**: C-008 Round 2: "V1 guardrails and stops; V2 map; V3 roles, resume".
- **Risk**: Low.

### Change 31: Invariants section: severity map, check column, load gap, gate (C-009, MERGE 78.0, unanimous)
- **Source**: V1 7.1 severity map; V2 7.1 "how a reviewer checks it" column and V2 7.4 gap row (no item measures simultaneous load, INV-032); V3 XC-08 gate.
- **Target**: Base 7.2 (add a "Check" column, V2 commands where the invariant matches), 7.1 (append row "INV-032: explicit gap, no item measures simultaneous load; guardrail one observer instance"), 7.1 header (state that R25-INV rows live in the appendix of Change 62).
- **Rationale**: C-009 Round 2.
- **Risk**: Low.

### Change 32: Keep V1's owner-decision gate mapping (C-010, V1 75.0, unanimous; keep)
- **Source**: V1 section 3 Gates column (Q11 gates nothing; Q21 gates SW-10; #409 pass gated by Q8, Q16, not Q2).
- **Target**: Base section 3 kept; V2's and V3's wider gate sets are not imported.
- **Rationale**: C-010: ADJ lines 781, 787; Q11 and Q17 do not gate the note.
- **Risk**: Low.

### Change 33: Evidence basis: OBS-NOW convention (C-011, V2 81.0, 2 of 3)
- **Source**: V2 0.2-0.3 OBS-NOW (each read-only check names its command).
- **Target**: Base 0.2 markers (add OBS-NOW), 0.3 table (add an "Evidence" entry per row where a check was run in this debate: SC-01 to SC-42 of `diff-analysis.md`, the probe checks, this plan's checks, each with date 2026-11-13).
- **Rationale**: C-011: V2's checks confirmed by SC-02, 23, 24, 27, 28; V1's Glob was wrong (SC-01).
- **Risk**: Low.

### Change 34: Both task packages exist (X-001, V2 98.3, unanimous; fixes D1)
- **Source**: V2 L1 row and 6.1; V3 section 6 inputs; SC-01, SC-02; `ls -d` re-run in this step.
- **Target**: Base 0.4 item 5 (replace: both `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115` and `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239` exist in this checkout; contents not read), 6.1 inputs (append both), SW-12, SW-13, WA-07 (append "read the existing package first", V3 rule 10).
- **Rationale**: X-001: V1 factual error; V1 conceded.
- **Risk**: Low.

### Change 35: JOIN never runs the unfixed sweep (X-002, V2 94.3, unanimous; fixes D2)
- **Source**: V2 TB-1 -> XC-05 edge and R-XC4.
- **Target**: Base XC-04 blocked-by (append TB-GIT, TB-GIT-ROW, SW-05, SWEEP-RUNNABLE, ORCA-AVAILABLE, `GRANT(XC-04,live-read)`), 4.2 edge table, 5.1 (move to W3, Change 7).
- **Rationale**: X-002: V1 lets JOIN run the unfixed `git status` across every listed worktree on a permission-free host; timing revised by R25-INV-007 to after the merge.
- **Risk**: Medium (wave move).

### Change 36: CAP stays early and separate from JOIN (X-003, MERGE 91.5, 2 of 3)
- **Source**: V1 XC-03 and V2 XC-06 (no #539 predecessor); ADJ graph `CAP -> {...}` with no `P539m` (SC-35); R25-INV-022 (CAP runs no git and no sweep).
- **Target**: Base XC-03 kept in W1; blocked-by gains ORCA-AVAILABLE and `GRANT(XC-03,live-read)`; no TB-GIT edge.
- **Rationale**: X-003 Round 2: "read-only CAP has no sweep-merge prerequisite". V3's merge gate is not imported.
- **Risk**: Low.

### Change 37: #534 table written now; source edits after merge (X-004, MERGE 81.3, unanimous)
- **Source**: V1 SW-06 (W0, "logged there now"); V2 Weak point W1 (ADJ A-004 "log items in #534" against A-005 "#539 merged", SC-36).
- **Target**: Base SW-06 (append: posted by the single editor under XC-02's pin rule and `GRANT(SW-06,issue-write)`; outside the five-link cross-issue order), 2.1 Weak points (insert W1 with the ADJ tension flagged), SW-07/SW-08 unchanged (post-merge).
- **Rationale**: X-004 Round 2: ADJ lines 211-212 "now"; keep V2's W1 flag.
- **Risk**: Low.

### Change 38: Keep the hard cross-issue order (X-005, V1 92.3, unanimous; keep)
- **Source**: V1 XC-02 (3) and the chain WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01; ADJ line 442 (re-read here).
- **Target**: Base kept; edges typed PROC in the edge table (U-004); skip rule from Change 3.
- **Rationale**: X-005: all-advocate adjudicated order; V2 conceded W7, W8.
- **Risk**: Low.

### Change 39: Keep one #450 edit set (X-006, V1 91.3, unanimous; keep)
- **Source**: V1 WA-02.
- **Target**: Base WA-02 kept (one write, one `updatedAt` re-read); defaulted edits omitted per Change 3.
- **Rationale**: X-006: A-011 one edit set per issue; INV-030 no etag, so fewer writes mean fewer race windows (R25-INV-025 residual accepted).
- **Risk**: Low.

### Change 40: The guard flip does not wait for the note draft (X-007, V2 86.0, unanimous)
- **Source**: V2 Weak point W2 and OB-05 blocked-by.
- **Target**: Base OB-06 blocked-by (remove "XC-05 (for (e))"), 4.2 (remove `XC-05 -> OB-06`), OB-06 (e) kept disjunctive ("in the note draft or, if the note is not merged, in the observer spec"), 2.2 Weak points (insert W2), W2 gate cell in 5.1 (remove "XC-05 draft").
- **Rationale**: X-007: ADJ line 192 lists no note predecessor; V1 conceded.
- **Risk**: Low.

### Change 41: #423 research may start early (X-008, V2 90.7, unanimous)
- **Source**: V2 V2-04; ADJ line 710.
- **Target**: implemented by Change 28 (new V2-05); 5.1 W1 gains lane "L-research (new `issue-423-research`): V2-05"; 1.1 L3 row "near-term" cell mentions V2-05.
- **Rationale**: X-008: V1 ambiguous (item gated, criterion says early), V3 conceded.
- **Risk**: Low.

### Change 42: Q14's gate: capture recorded versus `working` class restored (X-009, V2 81.0, unanimous)
- **Source**: V2 Weak point W5, V2 SW-13 (conditional), V2 N3.
- **Target**: Base Q14 row (widen: "and does the gate mean the capture is recorded, or the sweep's `working` class is restored in code?"; recommended per ADJ: #539 merged plus the #534 capture; default PLAN INFERENCE: ADJ's gate read as "capture recorded", labelled default), V2-02 (replace (3): passes only if every part of the owner's Q14 answer is met), new **SW-14** "Restore the sweep's `working` class from the shared capture (conditional)", 2.5 Weak points (insert W5).
- **SW-14 content**: needed only if Q14 means "restored". Acceptance: the class is derived from the values XC-03 recorded; a test pins it; the #534 row is closed; PR under Q25 and `GRANT(SW-14,pr-submit)`. Blocked-by: XC-03, SW-05, SW-06, Q14. Blocks: V2-02 (conditional GATE). Runs in: `sweep-534-followups` (PLAN INFERENCE). Wave W4. Undo: revert.
- **Rationale**: X-009: W5 separates a record from a shipped class; the owner's Q14 wording decides.
- **Risk**: Low.

### Change 43: Keep the "Phase 2" contradiction marker (X-010, V1 91.3, unanimous; keep)
- **Source**: V1 1.4.
- **Target**: Base 1.4 kept; SW-12 and SW-13 stay separate; the L1 row's gate names "SW-13 (#444 design)" and "SW-12 (research-report Phases 2-5)" separately; nothing imported from V2's L1 gate wording ("SW-12 (Phase 2 of #339)").
- **Rationale**: X-010: V2 conceded the conflation.
- **Risk**: Low.

### Change 44: Outward writes: per-PR, per-action grants replace the blanket rule (X-011, NEITHER 93.0, unanimous; fixes D5)
- **Source**: debate consensus (no variant correct); `WORKER-CONTRACT.md:243`; project CLAUDE.md (`/sc:pr-submit --monitor 3` "pushes the fixes without asking, and replies to and resolves the review comments it fixed").
- **Target**: Base 6.3 Owner row, 6.4 rule 2, 6.9 bullet 1, XC-02 (4) (replace).
- **New wording**: "The owner grants each outward action separately in the ledger (Change 13). A `pr-submit` grant on one PR covers only the writes it lists (Change 14), on that PR. Merges, issue posts, the #539 Codex-thread INV-008 reply and live tests each need their own grant. The coordinator never merges and never posts without a matching grant."
- **Rationale**: X-011: all three variants forbid what their own mandated tool does.
- **Risk**: Medium (central authority rule).

### Change 45: Ledger and program files never in the #539 checkout (X-012, MERGE 86.7, unanimous; fixes D3)
- **Source**: V3 "no extra sidecar is placed in #539"; V1 XC risk (V1:332); Change 2.
- **Target**: Base XC-01 "Location" (replace the PLAN INFERENCE path under the #539 checkout with "the home and branch named in Q26"), 6.1 Decision ledger row.
- **Rationale**: X-012: V1's default path contradicted its own risk note (IC-V1-1).
- **Risk**: Low.

### Change 46: Who merges #541 (X-013, MERGE 77.0, unanimous)
- **Source**: V1 SW-04 "owner merges"; V3 "authorized maintainer".
- **Target**: Base SW-04 blocked-by (replace "none (owner merges)" with "`GRANT(SW-04,merge)`: the owner merges, or records approval for a named merger"), 4.1 OWNER-MERGE note.
- **Rationale**: X-013: ADJ line 208 is silent; V2's "not owner-gated by any source" is not imported.
- **Risk**: Low.

### Change 47: No new coordinator work clock; cadence per Change 10 (X-014, V1 84.0, 2 of 3)
- **Source**: V1 6.6; `WORKER-CONTRACT.md:288`.
- **Target**: Base 6.6 per Change 10; V3's 5-minute ledger reconciliation tick is not imported.
- **Rationale**: X-014 Round 2 (V3 withdrew its tick, R2-V3:16); Round 3 R25-INV-010 turned the scheduler question into Q31.
- **Risk**: Low.

### Change 48: Reconcile register, graph and waves (X-015, NEITHER 86.3, unanimous; fixes D6)
- **Source**: debate consensus; IC-V1-1, IC-V1-2.
- **Target**: Base sections 2, 4 and 5 jointly.
- **Integration**: after Changes 1-47 are applied, re-check every wave row against the edge table: every item in a wave has all its hard predecessors in an earlier wave or earlier in the same wave's serial column; every wave exit check names only items scheduled in that wave or earlier; every "may run today" item has no unmet hard edge. Known fixes: XC-04 leaves W1 (Change 7); OB-06's XC-05 dependency leaves W2's gate (Change 40); V2-05 enters W1; XC-10 enters W0; SW-14 enters W4; XC-11 enters at W3 exit and W5. V2's and V3's own mismatches (V2 XC-05 "never waits for #539" against wave 3; V3 "XC-03 draft in K" with no draft item) are not imported.
- **Rationale**: X-015: every variant has register and schedule mismatches.
- **Risk**: Medium.

### Change 49: `/sc:sweep` availability caveat, corrected (A-001, V1 94.3, unanimous; keep and fix)
- **Source**: V1 6.6 and 7.3 (no `/sc:sweep` on master before SW-05; SC-06).
- **Target**: Base 6.6 and 7.3 per Change 6 (SWEEP-RUNNABLE replaces "install or `make sync-dev`").
- **Rationale**: A-001; R25-INV-006 showed the install claim is insufficient.
- **Risk**: Low.

### Change 50: The mandated PR tool and owner approval (A-002, NEITHER 93.0, unanimous; part of D5)
- **Source**: same root as X-011.
- **Target**: section 3 "Authority not granted" list (Change 60): append "A `pr-submit` grant on one PR does not authorize a merge, an issue write, the INV-008 ruling reply, or the tool on any other PR".
- **Rationale**: A-002: per-PR scoped authorization.
- **Risk**: Low.

### Change 51: W0 intake item XC-10 confirms the live reader (A-003, MERGE 82.3, unanimous)
- **Source**: debate consensus; V3 W0 exit ("real ownership/worktree map and permissions known").
- **Target**: new **XC-10** "W0 intake" (insert in 2.6 after XC-09); 5.1 W0 lane L-coord and W0 exit (append).
- **XC-10 content**: acceptance, each recorded in the ledger (or held with a reason): (1) the Q24 runner is confirmed live (exists, reachable, can run Orca read verbs from a terminal that holds no Run), else Q24's default is recorded; (2) the #539 author session is named (Q33, Change 52); (3) the coordinator home and ledger branch (Q26); (4) ORCA-AVAILABLE read back; (5) ADJ live facts re-read (Change 55); (6) both task packages listed (Change 34); (7) Q25 and Q31 asked. Blocked-by: none (owner and coordinator). Blocks: XC-09 (for (3)), SW-02, SW-03, SW-05 (for (2)), XC-03, OB-03 (for (1), (4)). Runs in: ledger only. Q: Q24, Q25, Q26, Q31, Q33. Undo: n/a.
- **Rationale**: A-003: ADJ's Q24 default names "the 409 session", whose liveness no source shows.
- **Risk**: Low.

### Change 52: The owner names the #539 author session (A-004, MERGE 82.3, unanimous)
- **Source**: debate consensus; V1 6.3 "#539 author (UNVERIFIED which)".
- **Target**: Base 6.3 #539 author row (replace "UNVERIFIED which" with "named by the owner at W0 (Q33); a top-level session, not a worker, because it pushes"), SW-02, SW-03, SW-05 blocked-by (append Q33).
- **New owner question**: **Q33** "Which session is the #539 author that applies SW-02 and SW-03 and pushes?" Recommended: the session that owns this checkout's agent, named by you. Default: SW-02, SW-03 and SW-05 pushes are held.
- **Rationale**: A-004: the critical path Q1 -> ruling -> fix -> merge had no named actor; V2's "the worker" withdrawn.
- **Risk**: Low.

### Change 53: Program files out of #539; named-file staging (A-005, MERGE 86.0, unanimous)
- **Source**: debate consensus; SC-42 (this debate's folder is not ignored in the #539 checkout); R25-INV-027 (`/sc:pr-submit` stages only changed paths).
- **Target**: Base 6.4 (new rule): any commit in the #539 checkout stages named files only (`git add -- <paths>`, `git commit --only -- <paths>`); the only `.dev/tasks/` package allowed there is SW-02's own under Q27; no program artifact is created there; existing untracked files there (this debate's folder, the review files) are neither deleted nor moved to satisfy isolation (R2-V3 fix 4).
- **Rationale**: A-005.
- **Risk**: Low.

### Change 54: Owner latency is the critical path; per-wave question batches (A-006, MERGE 74.0, unanimous)
- **Source**: V1 "Wave needed by" column; V2 Q1 "longest-lead item"; V3 "Decision runbook".
- **Target**: Base section 3 intro (append): "Owner latency is the real schedule. Ask one question at a time: Q1 first; then the W0 intake questions Q33, Q26, Q2, Q3, Q4, Q25, Q31; then each wave's questions when that wave opens (column 'Wave needed by'). Q27, Q28, Q29, Q30, Q32 are asked when their item is next." Add the "Wave needed by" cell for Q25-Q33.
- **Rationale**: A-006.
- **Risk**: Low.

### Change 55: ADJ live facts are historical; re-read at W0 and each gate (A-007, V3 85.0, unanimous)
- **Source**: V3 (ADJ facts treated as historical; "Fresh correct-fork PR evidence"; V3:466).
- **Target**: Base 0.3 header and every per-system "Current state" heading (append "as of ADJ, 2026-11-13"), 6.1 Live state row (append "re-read at W0 by XC-10 and at each gate"), 2.1 PR #539 facts (append the probe's re-read: #539 OPEN, head `873599d59`, 1003 files, mergeStateStatus UNSTABLE; #541 OPEN, head `779e58b17`, CLEAN; R25-INV-026, as of 2026-11-13).
- **Rationale**: A-007.
- **Risk**: Low.

### Change 56: Edge kinds with evidence; PROC for the publication order (U-004, V2 88.0, unanimous)
- **Source**: V2 0.3 kind definitions; V2 4.2.
- **Target**: Base 4 intro (replace V1's `->`/`~>` legend with V2's six kinds; `~>` becomes SOFT); applied in Change 19.
- **Rationale**: U-004: "apply PROC to cross-issue order".
- **Risk**: Low.

### Change 57: Weak points W1 to W6 (U-005, V2 80.7, unanimous)
- **Source**: V2 Weak points W1 (#534 timing), W2 (where the `reclaimable` row lives), W3 (no #539 -> flip edge), W4 (the note's test waits for the merge), W5 (Q14 meaning), W6 (#450 edits before FU-1). W7 and W8 withdrawn.
- **Target**: "Weak points" sub-block of each per-system section (Change 17): W1 in 2.1, W2 and W3 in 2.2, W6 in 2.3, W5 in 2.5, W4 in 2.6; each re-keyed through Change 61 and each naming the evidence that would settle it.
- **Rationale**: U-005: keep W1 to W6, drop W7 and W8 (X-005).
- **Risk**: Low.

### Change 58: Interface, failure, retry and idempotency contracts (U-010, V3 85.0, unanimous)
- **Source**: V3 sweep (V3:116-118, 124), snapshot (:142), question read (:146), launch and interruption runbook (:167, :171), remote read and failure (:194-200), catalogue, operational and communication contracts (:218-226), issue edit (:283), PR merge (:285).
- **Target**: "Interface contracts" sub-block of 2.1 (sweep), 2.2 (snapshot, question read), 2.3 (launch, store, interruption), 2.4 (remote read), 2.5 (catalogue), 2.6 (issue edit, PR merge) (insert), re-keyed through Change 61. The PR-merge contract's writer becomes "the owner or a named merger under `GRANT(<item>,merge)`".
- **Rationale**: U-010: failure, retry and idempotency per interface prevents duplicate writes.
- **Risk**: Low.

### Change 59: XC-11 independent invariant and coverage gate, two scopes (U-011, V3 87.7, unanimous)
- **Source**: V3 XC-08 and V3:248.
- **Target**: new **XC-11** (insert in 2.6 after XC-10); 5.1 W3 exit (first-release scope) and W5 (end-to-end scope).
- **XC-11 content**: a fresh reader who did not produce the work checks the 12 seed criteria, every item and decision edge, safe defaults, evidence and honest built/unbuilt status, and records PASS or FAIL with exact open blockers. INV-008 unresolved means FAIL; never voted away. Two scopes: **first-release alignment** (later items checked as deferred with gates and owners) and **end-to-end chain** (only after real behaviour evidence). A first-release PASS is never relabelled end-to-end PASS; CO-03 not selected under Q3 = close is recorded as such. Blocked-by (first-release): SW-05, OB-06, WA-04, XC-07, OB-08, SW-09, V2-01 or their recorded holds. Blocked-by (end-to-end): also SW-12, SW-13, WA-07, OB-09, V2-04. Runs in: an independent read-only context. Undo: n/a.
- **Rationale**: U-011.
- **Risk**: Low.

### Change 60: Decision runbook, lifetime and authority not granted (U-012, V3 87.7, unanimous)
- **Source**: V3:319-323.
- **Target**: Base section 3 (insert after the table): "Decision runbook", "Decision lifetime" (a changed answer voids unsent drafts, unmerged plans and dependent GRANT rows; applied effects need a separate authorized revert), "Authority not granted by these questions" (V3's five entries, plus: Q25 does not authorize a merge; Q28 does not authorize an INV-008 fix by the tool; Q30 does not authorize `run-use` or any Run other than the named one; Q31 does not authorize `/sc:sweep` above WC-16's cap or any write; Change 50's entry).
- **Rationale**: U-012.
- **Risk**: Low.

### Part 3: document-level Changes

### Change 61: Appendix: old-to-new id map, and its validation (X-015, S-002, R25-INV-021)
- **Source**: this plan (built from the V2 and V3 register ids and titles, read in this step).
- **Target**: new "Appendix: old-to-new id map" after section 7 (append).
- **Content the executor writes** (merged id = V1 id unless marked new):

| V2 id | Merged | V3 id | Merged |
|---|---|---|---|
| SW-01 | SW-01 | SW-01 | SW-01 (author impacts into SW-02 (3)) |
| SW-02 | SW-02 | SW-02 (#541) | SW-04 |
| SW-03 | SW-03 | SW-03 (threads and merge) | SW-02, SW-03, SW-05 |
| SW-04 (#539 free of keys) | SW-02 (4), SW-05 (4) | SW-04 (follow-ups) | SW-07, SW-08 |
| SW-05 (refresh merge ref) | SW-05 (1) | SW-05 (capture and compare) | XC-03, XC-04 |
| SW-06 (merge #539) | SW-05 | SW-06 (handoff contract) | SW-13 |
| SW-07 (#534 table) | SW-06 | SW-07 (management phase) | SW-12 |
| SW-08 (wording fixes) | SW-07 | OB-01 | OB-01 |
| SW-09 (small probe items) | SW-08 | OB-02 (seeded and live gate) | OB-03, OB-04 |
| SW-10 (#339 comment) | SW-09 | OB-03 (ship guarded read) | OB-05, OB-06 |
| SW-11 | SW-11 | OB-04 (#409 body) | OB-08 |
| SW-12 | SW-12 | OB-05 (routing) | OB-07 |
| SW-13 (`working` class) | **SW-14 (new)** | OB-06 (Decision Desk) | OB-09 |
| OB-01, OB-02, OB-03, OB-04 | same | WA-01, WA-02, WA-03, WA-04 | same |
| OB-05 (flip PR) | OB-06 (build pin part: OB-05) | WA-05 (handoff delivery) | WA-07 |
| OB-06 (routing) | OB-07 | (no FU-2 item; rule 7) | WA-05 |
| OB-07 (#409 pass) | OB-08 | CO-01 | CO-01 |
| OB-08 (build in golden capture) | OB-05 (3) | CO-02 (remote status design) | CO-03 (design criteria) |
| OB-09 | OB-09 | CO-03 (delivery) | CO-03 |
| OB-10 (reviewer asks, sweep panel) | OB-09 (2); SW-11 and Q17 | V2-01 | V2-01 |
| WA-01 | WA-01 | V2-02 (brainstorm and research) | V2-03 and **V2-05 (new)** |
| WA-02, WA-04 (#450 edits) | WA-02 | V2-03 (catalogue contract) | V2-03 (3), V2-04 |
| WA-03 (runbook; #450 edit 4) | WA-03 (+ WA-02 edit 4) | V2-04 | V2-04 |
| WA-05 (FU-1) | WA-04 | XC-01, XC-02 | same |
| WA-06 (FU-2) | WA-05 | XC-03 (publish note) | XC-05, XC-07 |
| WA-07 (label row) | SW-10 (1), SW-06 row | XC-04 (pin test) | XC-06 |
| WA-08 | WA-06 | XC-05 (vocabulary) | XC-08 |
| WA-09 | WA-07 | XC-06 (#339 comment) | SW-09 |
| CO-01 (owner one-liner) | CO-01 (2) | XC-07 (#534 table) | SW-06 |
| CO-02 (post text) | CO-01 | XC-08 (gate) | **XC-11 (new)** |
| CO-03 | CO-03 | M-APPROVAL | GRANT family |
| V2-01, V2-02, V2-03 | same | B-GIT | TB-GIT |
| V2-04 (research) | **V2-05 (new)** | B-READ, B-QUESTION | TB-CONSUME (+ LIVE, ORCA-AVAILABLE) |
| V2-05 (design content) | V2-03 (3) | B-LAUNCH | TB-PERM, TB-UNTRUSTED |
| V2-06 | V2-04 | B-EDIT | TB-EDIT (new) |
| XC-01, XC-02 | same | B-IDENTITY | TB-REMOTE (new) |
| XC-03 (#541) | SW-04 | B-DATA | TB-UNTRUSTED, TB-RELAY |
| XC-04 (note draft) | XC-05 | B-WRITE | TB-WRITE (new) |
| XC-05 (JOIN) | XC-04 | C-SNAPSHOT | K-SNAP |
| XC-06 (CAP) | XC-03 | C-SWEEP | K-SWJSON, K-NFR001 |
| XC-07 (land note and test) | XC-06, XC-07 | C-WATCH | K-WATCH |
| XC-08 | XC-08 | C-REMOTE, C-FACT | not nodes; deliverables of CO-03 and V2-03 |
| XC-09 (build-string rule) | 6.4 guardrail (new rule 13) | | |
| TB-1, TB-2, TB-4, TB-5, TB-7 | TB-GIT, TB-PERM, TB-CONSUME, TB-WC13, TB-UPSTREAM | | |
| TB-3, TB-6 | TB-REMOTE, TB-RELAY (new) | | |
| K-1 to K-7 | K-SNAP, K-SWJSON, K-NFR001, K-ALLOW, K-WC, K-ROUTE, K-NOTE | | |
| K-8 (WC-12 channel) | K-WC | | |

- **XC-10 (new)** has no V2 or V3 source id (debate consensus on A-003, A-004, A-007 plus R25-INV-002, R25-INV-009).
- **Validation (the executor runs it after the map is applied)**: (a) every `(SW|OB|WA|CO|V2|XC)-nn` used anywhere is defined in a section 2 table (set difference used minus defined is empty); (b) no V1 id changed meaning; (c) every V2 or V3 id in a provenance comment resolves through this map; (d) the 50 defined ids are exactly V1's 46 plus SW-14, V2-05, XC-10, XC-11.
- **Risk**: Medium (a wrong row mis-keys an edge; check (c) catches it).

### Change 62: Appendix: invariant coverage table R25-INV-001 to R25-INV-028
- **Source**: `invariant-probe.md` and Changes 1-16.
- **Target**: new "Appendix: invariant coverage" (append); 7.1 points to it.
- **Content**: one row per R25-INV id: id | severity | status after merge | rule | section and items that carry it. Rows 001-016 point to Changes 1-16. Rows 017-028 (ADDRESSED in the probe) record where the merged spec keeps them: 017 rebase actor = PR session (Change 1), 5.3 one-at-a-time merges; 018 = ADJ INV-008: 0.1, SW-01, SW-02, Q1, **UNRESOLVED-EXTERNAL with the owner**; 019 #539 file independence: 4.4 shared-files check, 5.3; 020 counts: Change 61 (d); 021 ids defined: Change 61 (a); 022 CAP needs no TB-GIT: XC-03 (Change 36); 023 cadence caps: 6.6 (Change 10); 024 seeded test necessary not sufficient: OB-03 (6), OB-04, 7.3; 025 one #450 set leaves a read-write gap: XC-02, accepted residual (single owner, before-body kept); 026 live PR state: 0.3 and 6.1 (Change 55); 027 pr-submit stages changed paths only: 6.4 (Change 53); 028 Orca CLI resolution: 6.1 orchestration-guide row.
- **Risk**: Low.

### Change 63: Appendix: owner questions Q1 to Q24 and Q25 to Q33
- **Target**: new "Appendix: owner questions" (append). Section 3 stays the single full table (Q1-Q33 with recommended answer, default, gates, wave); the appendix is an index only: id | one-line title | origin (ADJ Part 7, or this debate with the R25-INV id or debate point) | section 3 row. No answer, default or recommendation is restated there (single source of truth).
- **Label mapping**: V2 N1 (where the ruling is recorded) -> SW-01 criterion (Change 23); V2 N2 (`reclaimable` row before the note) -> OB-06 (e) disjunctive, no question (Change 40); V2 N3 -> Q14 widened (Change 42); V2 N4 -> WA-06, WA-07; V1 advocate N5 -> Q25, N6 -> Q26, N7 -> Q29, N8 -> Q30, N9 -> Q31, N10 -> Q32; V2 R3 unnamed questions -> Q27 (plan package), Q28 (#539 scope); A-004 -> Q33; R25-INV-004 -> Q1 part (b).
- **Risk**: Low.

### Change 64: Appendix: provenance and deviations
- **Target**: new "Appendix: provenance and deviations" (append).
- **Content**: (1) three proposals were debated, not five, because of a token pre-flight (as stated in the debate-orchestrator's Step 4 brief; not verified by this plan); (2) the V3 advocate could not write files, so the orchestrating session saved its messages (`round3-invariants-V3.md` header says so); (3) Round 3 (invariant resolution) ran in parallel across the three advocates, so no advocate saw another's Round 3 rules; (4) debate status: Round 2 converged 44 of 44 points on agreement (`convergence.md`); the Round 2.5 probe found 16 UNADDRESSED findings, each resolved by a rule in Changes 1-16; INV-008 (ADJ) is UNRESOLVED-EXTERNAL with the owner; (5) base selection was decided by tiebreaker with a 0.000877 score margin (`base-selection.md`); (6) no live GitHub or Orca action was taken by the debate beyond the read-only probe checks.
- **Risk**: Low.

### Change 65: Frontmatter, provenance header, Part A label, INV-008 first
- **Target**: Base lines 1-17.
- **Integration**: keep V1's frontmatter fields; set `variant:` to `merged`, keep `status: BLOCKED_BY_INVARIANTS (INV-008 UNRESOLVED-EXTERNAL; owner decision Q1; carried, not waived)`, add `base: variant-1-opus-architect.md`, `merged_from: [variant-2-opus-analyzer.md, variant-3-haiku-backend.md]`, `plan: refactor-plan.md`. After the H1 add the Section 6 provenance header comments and the line `**Part A: Unified alignment spec** (sections 0 to 7); appendices follow section 7.` 0.1 stays the first subsection, keeps "This spec does **not** specify the code fix", states the requirement and options F1, F2, F3 (Changes 4, 11, 23), and adds: "R25-INV-018 in this debate's probe is the same finding; it stays UNRESOLVED-EXTERNAL with the owner."
- **Risk**: Low.

### Change 66: Project rules and honest-limit statements in one place
- **Target**: Base 0.4 (append items) and 6.4 (consolidate).
- **Integration**: 6.4 states, once each: PRs only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`, every `gh` call names the fork (or `IronbellyOrg/Coder` for #477), no interaction of any kind with `SuperClaude-Org/SuperClaude_Framework`, the returned PR URL checked; never stage `.claude/` mirrors (only `.claude/settings.json` is tracked; edit `src/superclaude/` and run `make sync-dev`); `.dev/tasks/` always staged, staging is not committing; worktrees only through Orca at its default location with `--agent`, never `EnterWorktree`, raw `git worktree add`, `.claude/worktrees/` or `.dev/worktrees/`; WC-13 (no worker creates worktrees or dispatches workers); the Orca build string recorded at every live record's exit (from V2 XC-09). 0.4 keeps "It changes nothing ... posts nothing" and adds: "No section claims that the watcher-to-orchestrator link (L1) or the orchestrator-manages-work link (L2) exists."
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| # | Diff point or finding | Rejected approach (source) | Rationale (debate evidence) |
|---|---|---|---|
| 1 | X-005, U-005 | V2's soft publication order: "Demoted to SOFT" (V2 4.4), Weak points W7 and W8, edges 47 and 50 SOFT, #339 comment posted before the #409 pass | X-005 V1 92.3 unanimous; ADJ line 442 all-advocate order; V2 conceded and withdrew W7, W8 |
| 2 | X-006, C-004 | V2's three separate writes to #450 (V2 WA-02, WA-03 edit 4, WA-04) | X-006 V1 91.3; one edit set per issue (A-011); each extra write adds a race window (INV-030) |
| 3 | X-014 | V3's 5-minute decision-ledger reconciliation clock (V3 polling table) | X-014 V1 84.0; V3 withdrew it (R2-V3:16); WC-16 adds a duty, not a clock |
| 4 | R25-INV-010 | Any categorical "no extra scheduler" or "GitHub not on a timer" (V1 6.6; R2-V2, R2-V3) | All three Round 3 rules: WC-16's sentence is about the sweep duty; the owner's order is asked (Q31), not decided |
| 5 | X-003 | V3's CAP gated on the #539 merge (V3 SW-05 blocked by SW-03) | X-003 MERGE 91.5; ADJ graph has no `P539m` predecessor for CAP (SC-35); CAP runs no git (R25-INV-022) |
| 6 | X-008, C-006 | V3's research gated on #539 merge and capture; V1's single gated V2-03 holding research | X-008 V2 90.7; ADJ line 710 "may be done ahead of the rest" |
| 7 | X-007 | V1's hard edge XC-05 -> OB-06 | X-007 V2 86.0; ADJ line 192 lists no note predecessor; V1 conceded |
| 8 | C-003 | V2's SOFT edge OB-03 -> OB-04 and V3's merged single item | C-003 V1 84.3 unanimous; a live-layout read before the seeded test risks consumption (X-016) |
| 9 | X-002, R25-INV-007 | V1's JOIN in W1 before the ruling; V2's Round 2 "JOIN in Wave 2 after TB-1"; V3's pre-merge JOIN by the #539 owner | X-002 V2 94.3; V2 withdrew its timing in Round 3; V3's option not adopted because waiting costs no schedule (JOIN's consumers already wait for SW-05) and it avoids the worktree-ownership and CLI problems (R25-INV-006, -007) |
| 10 | X-012, R25-INV-002 | V1's ledger path under the #539 checkout; V2's Round 2 "neither the #539 nor the main checkout" | X-012 MERGE 86.7; V2 withdrew its rule in Round 3 (main checkout is the project's orchestrator home) |
| 11 | R25-INV-001 | Workers run `/sc:pr-submit` (V1:575; V2:563, :610) | `WORKER-CONTRACT.md:23`, `:41`, `:243`; `SKILL.md:47`; all three Round 3 rules |
| 12 | R25-INV-001 | V2 Round 3's top-level agent per PR item as the recommended model | Drops `worker_done` supervision and WC-13 binding (probe); kept only as the owner's alternative in Q25 |
| 13 | R25-INV-001 | V1's "create the worktree with `--agent`, then `worker-start` into it" (V1 XC-09 (3), 6.2) | Two agents per worktree (probe R25-INV-001); all three Round 3 rules |
| 14 | C-005 | V2's separate owner one-line comment on Coder#477 before the reply | C-005 MERGE 73.3: one reply carries the Q4 line |
| 15 | X-010 | V2's use of "Phase 2" in both senses (L1 gate "SW-12 (Phase 2 of #339)") | X-010 V1 91.3; V2 conceded |
| 16 | X-013 | V2's "the merge itself is not owner-gated by any source" for #541 | X-013 MERGE 77.0: owner merges or approves a named merger |
| 17 | X-001 | V1's "not found in this checkout ... UNVERIFIED" for the task packages | X-001 V2 98.3; SC-01 WRONG; re-checked in this step |
| 18 | S-002 | V2 (50 items) or V3 (33 items) as the id base | S-002 V1 67.5; fewest reversals; V2 and V3 ids collide with V1 meanings (XC-03, XC-04, SW-05, SW-13) |
| 19 | S-006 | V3's role letters (S, O, W, K, F, C, L, R) in place of worktree names | S-006 MERGE 76.0 keeps V1 named worktrees |
| 20 | C-010 | V3's wide gates (Q11 gating SW-04, XC-03, XC-07; Q21 gating five items); V2's Q2 gate on the #409 pass | C-010 V1 75.0 unanimous; ADJ lines 781, 787; V2 conceded |
| 21 | X-015 | V2's and V3's own schedule mismatches (V2 XC-05 "never waits for #539" in wave 3; V3 "XC-03 draft in K" with no draft item; V3 SW-05 called a follow-up holder) | X-015 NEITHER 86.3 |
| 22 | R25-INV-011 | "Four texts" as the full F3 caveat set (V1, V2, V3) | At least 16 locations (probe); all three Round 3 rules |
| 23 | A-001, R25-INV-006 | "`superclaude install` or `make sync-dev` makes `/sc:sweep` available" (V1 7.3) | The installed uv-tool CLI has no `sweep` command; neither step upgrades it (probe; R3-V2 check) |
| 24 | R25-INV-003 | V3's separate owner approval for withheld-slot semantics | The skip rule changes no owner default and follows ADJ line 442; V1 and V2 need no question; V3's substance (withheld is not completed) is adopted |
| 25 | R25-INV-005 | V2's "Codex thread excluded from the tool even after the ruling" | No exclusion switch was found in the skill (V3; Codex selection UNVERIFIED in the probe); closing the thread by the owner's reply makes it unnecessary |
| 26 | R25-INV-013 | V3's single `M-APPROVAL` node | One boolean cannot carry PR scope, action or lifetime (probe; all three Round 3 rules) |
| 27 | S-005 | New contract nodes `K-REMOTE`, `K-FACT` from V3 `C-REMOTE`, `C-FACT` | Proposed contracts not yet defined; they remain deliverables of CO-03 and V2-03; no debate point asked for nodes |
| 28 | U-009 (not promoted) | V2 XC-09 build-string rule as its own work item | Not promoted to debate; folded into a 6.4 guardrail (Change 66) |
| 29 | S-004 | V3's seven waves (separate W5 designs and W6 releases) | S-004 MERGE keeps V1's W0-W5 |
| 30 | invented ids | Carrying Round 3 labels N1-N10 as ids, or naming new worktrees without the PLAN INFERENCE label | Change 63 maps them to Q25-Q33; V1 0.5 rule: proposed worktree names are PLAN INFERENCE |
| 31 | R25-INV-002 | V1 Round 3's owner-created `--agent` worktree as the recommended coordinator home | Relies on an `--agent`-launched agent counting as person-opened (unverified); project rule names the main checkout; kept as the owner's alternative in Q26 |
| 32 | X-011, A-002 | V3's blanket "explicit authorization for every outward write" kept beside a mandated autonomous tool | X-011 NEITHER 93.0: replaced by per-PR, per-action grants |

## Risk Summary

Every Change not listed here is Low risk: additive text, rollback by removing the inserted block.

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 19 (edge table) | High | Dangling or mis-keyed edges; waves no longer follow the graph | Restore V1 4.2 text graph; re-apply edge changes one at a time |
| 1 (PR actor) | High | A PR item left with a worker PR duty breaks WC-9 and WC :243 | Revert 6.3, 6.4 rule 2 and the PR items' "runs in" cells to base, then re-apply |
| 13, 14, 44 (grants) | Medium | An outward edge with no matching GRANT; owner approval scope unclear | Restore base 6.3/6.9 wording; keep the grant table as an appendix only |
| 7, 35 (JOIN move) | Medium | W1/W3 exit checks still cite XC-04 in W1 | Re-run Change 48's wave check |
| 18, 61 (ids, map) | Medium | A V2/V3 id resolved to the wrong merged item | Fix the map row; re-run validation (a)-(d) |
| 20, 48 (waves) | Medium | A wave row schedules an item before a hard predecessor | Re-run Change 48's check; move the item |
| 2 (home) | Medium | Ledger staged on an unrelated branch if the owner keeps the main checkout's current branch | Owner decision; recorded in Q26 |
| 5 (#539 manual pushes) | Medium | A manual push path skips the monitored workflow | Grant row for #539 records the limit; revert to "held" |

## Merge-executor instructions

Ordered steps. Work stub-first and incrementally: copy the base, then apply one step at a time, writing to disk after each. Do not rewrite the file from memory.

1. **Copy the base.** Copy `variant-1-opus-architect.md` to the merged output path the debate-orchestrator names. Keep the base's H1 and its eight H2 sections, in this order and with these names: `0. Status, how to read, and honest limits`; `1. Chain to target`; `2. Per-system sections`; `3. Owner decisions`; `4. Cross-system dependency graph`; `5. Ordered lockstep schedule of waves`; `6. What an orchestrator session needs`; `7. Invariants and edge cases`. Never renumber an existing H3; new H3s take the next free number in their section (1.5, 5.5, 5.6, 6.10, 4.5).
2. **Provenance convention (HTML comments).** At the top, after the frontmatter: `<!-- Provenance: This document was produced by /sc:adversarial -->`, `<!-- Base: Variant V1 (opus:architect) -->`, `<!-- Merge date: <ISO-8601> -->`, `<!-- Plan: refactor-plan.md, Changes 1-66 -->`. Before each changed or inserted block: `<!-- Source: <Base (V1) | Variant V2 (opus:analyzer) | Variant V3 (haiku:backend) | Debate consensus | Round 3 rule>, <section or id> — merged per Change N -->`. Tables cannot hold comments inside rows: put one comment line directly above the table listing the changed rows, e.g. `<!-- Changed rows: SW-02 (Change 4, 23), SW-14 new (Change 42) -->`. Unchanged base sections get one `<!-- Source: Base (original) -->` at the section start.
3. **Section 0** (Changes 65, 4, 11, 23, 33, 34, 55, 66): frontmatter and Part A label; 0.1 requirement sentence, widened channels, F3 inventory rule, INV-008 UNRESOLVED-EXTERNAL; 0.2 markers (add OBS-NOW, `R25-INV-nnn`, edge kinds, GRANT, Q25-Q33); 0.3 "as of ADJ" plus re-read facts; 0.4 item 5 replaced, "no link claimed" sentence added; 0.5 "Observe:" rule.
4. **Section 1** (Changes 24, 41, 43, 34): root-cause column, first-release sentence, 1.5 contract completion rule, L1 and L2 gates named separately.
5. **Section 2** (per system, in order 2.1-2.6): apply every item-level Change: SW (4, 5, 11, 12, 16, 23, 37, 42 SW-14, 46, 52, 53); OB (8, 25, 40); WA (3, 26, 39); CO (27); V2 (28 V2-05, 42); XC (2, 7, 9, 13, 29, 35, 36, 45, 51 XC-10, 59 XC-11). Then add "Observe:" to every acceptance cell (22), the "Weak points" sub-blocks (57) and the "Interface contracts" sub-blocks (58). Every PR item gets the PR-session and GRANT text (1, 14).
6. **Section 3** (Changes 4, 42, 54, 60, and the new rows): widen Q1 and Q14; append Q25-Q33 rows with every column (decision in plain words, recommended answer, default if unanswered, gates, wave needed by), worded as in Changes 1, 2, 5, 6, 8, 10, 12, 15, 52; add the ask order, the decision runbook, the decision lifetime and the authority-not-granted list.
7. **Section 4** (Changes 19, 21, 56, 61): extend 4.1 nodes; build the 4.2 edge table by re-keying V2's 70 edges through the map, adding V1 edges V2 lacks, applying the debate changes, and adding GRANT, Q25-Q33, ORCA-AVAILABLE, SWEEP-RUNNABLE and TB-GIT-ROW edges; regenerate the 4.3 text graph from the table; 4.4 graph checks; 4.5 differences from ADJ.
8. **Section 5** (Changes 7, 20, 28, 41, 48, 51, 59): W0 gains XC-10 and the intake questions; W1 loses XC-04 and gains V2-05 and the OB-04 Q30 gate; W2's OB-06 gate loses XC-05; W3 gains SWEEP-RUNNABLE then XC-04 before XC-07, and the XC-11 first-release run at its exit; W4 gains SW-14 (conditional); W5 notes XC-11 end-to-end. Recompute 5.2 into the three lists; add 5.5 concurrency rules and 5.6 interruption rule; update 5.4.
9. **Section 6** (Changes 1, 2, 5, 9, 10, 13, 15, 30, 44, 53, 66): roles (PR session, read-capture and seed-test operators, owner-named #539 author), guardrails, new stop rows (Orca not reachable, sweep not runnable, ruling-required finding during a PR run, wrong-fork URL), 6.6 cadence record, 6.8 ledger plus grant table, 6.9 never-do list, 6.10 evidence handoff and resume.
10. **Section 7** (Changes 31, 6, 4, 16, 62): check column, INV-032 gap row, corrected 7.3 rows, new 7.4 edge cases (Orca down; sweep command missing; a Q answer changes after drafts exist; a skipped link posted later; the four old sweep reports offered as evidence).
11. **Appendices**, after section 7, as H2 in this order: `Appendix: old-to-new id map` (Change 61); `Appendix: owner questions Q1-Q24 (from the adjudicated doc) and Q25-Q33 (new from this debate)` (Change 63); `Appendix: invariant coverage R25-INV-001 to R25-INV-028` (Change 62); `Appendix: provenance and deviations` (Change 64).
12. **Validate**, then write `merge-log.md` from template Section 5 with one entry per Change (Applied, Failed or Skipped, with the reason). Run every check in the next section; a failed check is a failed merge, not a note.

## Acceptance checks for the merge

Each check is PASS or FAIL; the method says how it is observed.

| # | Check | Method |
|---|---|---|
| A1 | Every R25-INV-001 to R25-INV-016 has a rule and a location | Each id appears in the coverage appendix with a section reference, and that section contains the rule of the matching Change |
| A2 | No work-item id is used but undefined | grep every `(SW|OB|WA|CO|V2|XC)-[0-9]{2}`; the set used minus the set defined in section 2 tables is empty |
| A3 | Every blocked-by and blocks endpoint exists | Every From and To in the 4.2 table is a defined item, Q1-Q33, a K-node, a TB-node, LIVE, ORCA-AVAILABLE, SWEEP-RUNNABLE, TB-GIT-ROW, OWNER-MERGE or a GRANT(<defined item>,<listed action>) |
| A4 | The graph covers every work item | Each of the 50 items appears at least once in the 4.2 table as From or To |
| A5 | The waves respect the edges | For each hard edge (not SOFT) A -> B, A's wave is earlier than B's, or both are in one wave with A before B in its serial column; no cycle; no wave gate names an item that is not scheduled |
| A6 | INV-008 stays first and unresolved | 0.1 is the first subsection, says UNRESOLVED-EXTERNAL and owner decision Q1, and says the spec does not specify the code fix; no section states a fix design |
| A7 | No claim that L1 or L2 exists | grep for the L1 and L2 rows and every "watcher hands", "manages work" sentence; each says not built |
| A8 | No fact without a source or UNVERIFIED label | Spot-check 20 facts across sections; each cites ADJ, SEED, ENR, an OBS-NOW check, a debate file, or carries UNVERIFIED or PLAN INFERENCE |
| A9 | Project rules stated | 6.4 contains: fork-only PRs with `/sc:pr-submit --monitor 3` and `--repo IronbellyOrg/IronClaude`; no upstream interaction; never stage `.claude/`; `.dev/tasks/` always staged; Orca-only worktrees with `--agent`; WC-13 |
| A10 | Read-only constraint stated | 0.4 says the spec changes, posts and stages nothing |
| A11 | No worker runs `/sc:pr-submit` | grep `pr-submit`: every hit names the PR session, the grant, or a rule forbidding it for workers |
| A12 | Id spaces kept apart | No bare `INV-0nn` is used for a Round 2.5 finding; every such reference is `R25-INV-nnn` |
| A13 | Every Q has a default | Q1-Q33 each have a "Default if unanswered" cell that takes no outward or irreversible step |
| A14 | Map validation | Change 61 checks (a)-(d) pass |
| A15 | Heading structure | The eight base H2s appear in order, then the four appendices; no H2 removed |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-13 (plan written; the merge executor records the exact time in `merge-log.md`)
