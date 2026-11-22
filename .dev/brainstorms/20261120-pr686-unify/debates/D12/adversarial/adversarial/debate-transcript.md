# Adversarial Debate Transcript: D12

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe; Round 3 skipped (depth=standard); no forced taxonomy round needed (all levels covered)
- Convergence achieved: 88 percent (22 of 25 diff points), BLOCKED_BY_INVARIANTS (5 HIGH UNADDRESSED probe findings)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, Variant 2 = CLAY; both ran as separate Agent-tool subagents on the session default model, `general-purpose`, read-only)
- Diff-point taxonomy tags (AD-5): L1 = S-001, S-002, S-003, C-009; L3 = C-008 (refusal guard), C-013 (stage transitions), A-002 (claim state and idempotency); every other point L2.

<!-- ROUND-1 -->

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position summary.** Keep brainstorm and design at claim, because the owner's own spec (issue 302) assumes the body is stale and checks it before planning. Keep PR 661 as merged and adapt PR 690 (plain `--plan` only). Reject issue 689's move of heavy planning into create and its refusal of plan-less claims. Clay found a real gap, and one claim-side rule closes it more cheaply than 689's chain move.

**Steelman of CLAY.** Planning once at filing, on a strong model, lets cheaper models and an unattended poll only execute (issue 651). After PR 661, create writes a plan that claim never reads (no "Fix approach" in `refs/claim.md`), so the same plan is made twice. Nothing fills the plan sections of pre-661 or hand-filed issues, and `--plan` does that. `plan_body.py` makes the write deterministic and keeps the owner's one-write boundary. The design's `plan_check` hold needs `--plan` first. Clay marked 689's open decisions "Decision for Clay" and built nothing.

**Strengths claimed.**
1. The claim-time chain is the owner's stated design: issue 302 ("assumes context in issue body is out of date"); design record B2, B4, B14.
2. 689 has no actor that can run the work at create: workers have `Read, Grep, Glob, Write, Bash` (`agents/issue-worker-t1.md:5`); `/sc:issue` is on the never-as-worker list (`core/WORKER-CONTRACT.md:23`); `refs/chains.md:7` says the command never runs these commands.
3. A design stored in the body goes stale and the accuracy check would validate a design.
4. Claim is idempotent and re-runnable (`refs/claim.md:43`; SKILL.md:86 Wave 2 stops on closed or other-assigned issues); a plan-section refusal would be a new third stop class.
5. R23 and R25 (Status picks command, Pipeline picks level; unpushed) would leave the Spec stage nothing to do.
6. The `worktree` level stops at a plan a human approves (`templates/launch-prompt.md:21-23`).

**Weaknesses identified in CLAY.**
1. 689 builds nothing and has six open "Decision for Clay" items and no baseline ("Not measured yet").
2. The refusal guard blocks every pre-2026-11-19 and hand-filed issue; `--plan` is its prerequisite and is still open.
3. The rename of `## Fix approach` touches PR 661 tests and the design's `fix_approach` token, plus chain tests (`tests/skills/test_issue_protocol.py:723-770`).
4. `--remaining` serves a `handback` verb in unbuilt PR B; interface merged ahead of its consumer.
5. Create-time cost is paid for filings that may never be claimed.

**Concessions.** Claim ignoring the plan sections is a real gap. Hand-filed and older issues have no planning path today. `plan_body.py` and the `already_planned` no-write result (`refs/plan.md:47`) are better engineering than anything on the owner's side. The owner's line leaves the unattended watcher with no plan-before-start check (another debate). The issue 302 quotation and the filing dates of 339, 409, 423, 431, 444, 450 are not re-read (UNVERIFIED).

**Per-point verdicts.**

| ID | Winner | Conf. | Evidence |
|---|---|---|---|
| S-001, S-003 | HYBRID | 55 | Formatting only |
| S-002 | OURS | 70 | Closing disposition list is actionable |
| C-001 | OURS | 80 | Issue 302; B2, B4, B14 |
| C-002 | HYBRID | 95 | Both keep PR 661 |
| C-003 | OURS | 65 | Plain `--plan` built; `--remaining` has no consumer |
| C-004 | OURS | 80 | 689 unbuilt, six open decisions |
| C-005 | HYBRID | 65 | Both see the gap; ours is smaller |
| C-006 | OURS | 85 | `issue-worker-t1.md:5`; `WORKER-CONTRACT.md:23` |
| C-007 | OURS | 75 | Staleness real; no mitigation named |
| C-008 | OURS | 80 | Guard blocks older and hand-filed issues; a warning instead |
| C-009 | OURS | 70 | Rename gains nothing, touches pinned tests |
| C-010 | CLAY | 55 | `--mode other` harmless, out of scope |
| C-011 | HYBRID | 55 | Strong tier plausible, but at claim per B14 |
| C-012 | OURS | 60 | Create-time cost unmeasured and paid per filing |
| C-013 | OURS | 70 | R23 and R25 undercut (unpushed, UNVERIFIED as binding) |
| C-014 | OURS | 75 | Issue 302 is the owner's own spec |
| X-001 | OURS | 75 | Issue 302 line 10 |
| X-002 | OURS | 85 | Tool lists and never-as-worker rule |
| X-003 | OURS | 60 | B2 and B4 are owner decisions |
| U-001 | OURS | 65 | R23 and R25 |
| U-002 | OURS | 60 | `launch-prompt.md:21-23` |
| U-003 | OURS | 70 | Cheap, closes the gap |
| U-004 | OURS | 80 | Never-as-worker list |
| U-005 | CLAY | 90 | `plan_body.py` |
| U-006 | CLAY | 85 | `--plan` fills the gap |
| U-007 | CLAY | 60 | Hold depends on `--plan`; design partly unpushed |
| U-008 | CLAY | 55 | Minor |
| U-009 | CLAY | 65 | Sandbox run, three reviews |

**L3 notes.** C-008: re-claim is idempotent (`claim.md:43`), a plan-section refusal adds an unexpected stop; claim should warn "plan sections missing, run `--plan`". C-013: a claim-time chain keeps Status the single selector. A-002: claim is re-runnable by design, `--plan` is idempotent on `already_planned` (`plan.md:47`), so create-time cost is not guaranteed to be amortised.

**Shared assumptions.** A-001 QUALIFY (a light plan is enough to start a short chain; not shown enough to execute from; test it). A-002 QUALIFY (claim re-runnable; create cost paid for never-claimed issues; no baseline). A-003 QUALIFY (watcher planned not built; wait for the watcher debate). A-004 ACCEPT (snapshot equality UNVERIFIED, low risk). A-005 QUALIFY (shared login; the merge is a fact, who merged is not).

### Variant 2 Advocate (CLAY)

**Position summary.** Plan once at filing time, on a strong model, so claim and the orchestrator only execute. PR 661 (merged) and PR 690 (built, with `--remaining`) are the working core; issue 689 is the unbuilt step that removes double planning. OURS wins on who can run brainstorm at create (C-006) and on staleness (C-007); CLAY wins on capability (U-005, U-006, U-007) and on the double-planning fix (C-005).

**Steelman of OURS.** The claim chain was a deliberate, tested design: issue 302 line 10 and B2/B4/B14. Planning belongs after the accuracy check so the design is built from today's code and a human approves it at `worktree` level. 689 is unbuilt with open decisions, would refuse every pre-661 and hand-filed issue, and names no actor that can run brainstorm at create. OURS also concedes the double-planning gap and its fix is cheap.

**Strengths claimed.**
1. Front-loaded planning lets execution run on cheaper models: the goal of issue 651 and the reason PR 661 exists; master `refs/create.md:59-67` fills the sections at every depth.
2. OURS's own fix keeps claim's heavy chain and quotes the light plan into `next-steps.md`: two planners with a patch between them; `refs/chains.md:12-13` still starts with brainstorm and design after create already planned.
3. `--plan` is built and deterministic (`plan_body.py` `check`, `splice`, `verify`; `E-PLAN-RACE`; `E-PLAN-WRITE-FAILED`; one body edit), and OURS keeps it (common ground).
4. `--remaining` is a re-plan with a round marker and `replaced_sha` guard (pr-p `refs/plan.md:34-35`); written, tested, reviewed; holding it back reopens a reviewed PR.
5. The design's `hold:plan` and `plan_check` depend on `--plan` (design 4.11, 8.3, ruling 31).
6. 689 is honest about its state and asks `plan_check` to accept both headings during migration.

**Weaknesses identified in OURS.**
1. The stale-design argument is overstated: OURS's light plan at create also describes moving code. It argues for a freshness check at claim, not against plan-at-create.
2. Claim-time cost is not shown lower; create tiers are cheaper at quick and standard; no baseline on either side.
3. OURS leans on R23/R25, unpushed requirements, weaker than master code.
4. "Plain `--plan` only" leaves the orchestrator's re-plan path without a tool; `--remaining` is a flag, not a dependency on `handback` (UNVERIFIED for PR code beyond refs).

**Concessions.** C-006 is a real hole in 689; refusing plan-less claims must not be adopted as written (conditional and pointing to `--plan`); heavy create costs more per filing with no baseline; `--remaining` serves a loop that does not exist yet; "plan once" is weakened by `--remaining` itself (strongest form: plan once at create, re-plan only on explicit hand-back); PR 690's drafting worker sees issue text as fenced data, hardening tracked on issue 665.

**Per-point verdicts.**

| ID | Winner | Conf | Evidence |
|---|---|---|---|
| S-001/S-003 | tie | 50 | cosmetic |
| S-002 | OURS | 65 | disposition list |
| C-001 | CLAY | 62 | 651's goal; claim re-plans a plan create just made |
| C-002 | HYBRID | 90 | both keep PR 661 |
| C-003 | CLAY | 66 | `--remaining` built and reviewed; no unbuilt verb needed (UNVERIFIED beyond refs) |
| C-004 | HYBRID | 58 | adopt sections and `--plan` flow; defer `## Design` and the rename |
| C-005 | CLAY | 68 | OURS patches and keeps two planners |
| C-006 | OURS | 80 | tool lists; never-as-worker |
| C-007 | OURS | 62 | accuracy check exists for this |
| C-008 | HYBRID | 60 | refuse only on the unattended or orchestrator path; a manual claim warns and proceeds |
| C-009 | OURS | 60 | rename churn |
| C-010 | CLAY | 55 | `refs/labels.md:26`; 3 forms have 0 plan matches |
| C-011 | HYBRID | 55 | raise the floor for medium and complex only |
| C-012 | HYBRID | 55 | both unmeasured |
| C-013 | OURS | 63 | a design at create leaves the Spec stage nothing; R23 unpushed so cheap to rewrite |
| C-014 | OURS | 60 | 302 and B2/B4/B14 are the owner's merged design |
| X-001 | HYBRID | 55 | both goals stated |
| X-002 | OURS | 78 | tool lists |
| X-003 | HYBRID | 55 | "opposite" overstated; layered |
| U-001 | OURS | 58 | R23/R25 |
| U-002 | OURS | 60 | human gate |
| U-003 | HYBRID | 60 | good; stands in for, not replaces, a plan read at claim |
| U-004 | OURS | 65 | `WORKER-CONTRACT.md:23` |
| U-005 | CLAY | 80 | deterministic |
| U-006 | CLAY | 82 | capability gap real |
| U-007 | CLAY | 66 | design 4.11, PR P before PR B |
| U-008 | CLAY | 55 | low severity |
| U-009 | CLAY | 62 | sandbox run, 3 reviews |

**Shared assumptions.** A-001 QUALIFY (one `/sc:analyze` pass suffices for simple and medium only; a complex feature needs the design step). A-002 QUALIFY (claim count not once; `--remaining` re-plans; advantage only if create plans are reused; claim re-runs UNVERIFIED). A-003 QUALIFY (orchestrator and watcher designed not built). A-004 ACCEPT. A-005 QUALIFY (shared login is weak evidence; who clicked merge UNVERIFIED).

## Round 2: Rebuttals

Orchestrator facts verified between rounds (given to both advocates): (a) `refs/claim.md:43` "re-claim is allowed and idempotent" and `already_launched` blocks a second agent launch (claim.md lines 125 and 146), so the chain runs once per launch; (b) `grep -i handback` finds nothing in the pr-p issue skill, command or refs, so `--remaining` is not coupled in code to the unbuilt `handback` verb (its consumer is the orchestrator, per PR 690's body); (c) pr-p snapshot equals PR 690's live head `f3bc7798197558d57090ef01c1363a7dafca579a`: UNVERIFIED.

### Variant 1 Advocate (OURS) rebuttal

**Response to criticisms.**
1. Stale design (Clay W1): partly conceded. A light plan at create also describes code that later moves; that argues for a freshness check at claim, not against plan-at-create. What survives: the larger the design in the body, the more a stale one costs; `create.md:63` tells the worker to state assumptions so claim has something to check.
2. Cost (W2): conceded. Fact (a) removes the A-002 argument; nobody has a baseline. Left over: claim-time cost lands only on issues actually worked, create-time cost on every filing; unmeasured, so a tie.
3. R23 and R25 (W3): conceded as a reason (unpushed, cheap to rewrite); UNVERIFIED as binding.
4. `--remaining` (W4): conceded. Per fact (b) it is self-contained (`pr-p .../refs/plan.md:89-94`: round marker, `replaced_sha` guard, `E-REMAINING-NEEDS-PLAN` when plain `--plan` has not run). Holding it back reopens a reviewed PR for little gain; the head check (c) stays UNVERIFIED.
5. One rule leaves two planners: conceded in part. If every plan that passes the check goes to the short chain, a light plan is assumed enough for a complex feature (A-001). Corrected rule: simple and medium, when the plan passes the check, claim runs the short chain; complex, claim still runs brainstorm and design, seeded with the filed plan and checking it against current code.

**Updated assessment.** Clay's central claim carries weight: merged `refs/create.md:61` says an issue "arrives with its plan already written and whoever picks it up only executes", and claim's chain contradicts that line in the owner's own merged code, so X-001 is not OURS to win outright. `plan_body.py` and `--plan` are better engineering. The split refusal guard (refuse only on the unattended path, warn on a manual claim) beats a flat rejection. Three points still held: no actor at create can run brainstorm or design (`agents/issue-worker-t1.md:5`); `/sc:issue` is on the never-as-worker list (`WORKER-CONTRACT.md:23`); 689 is unbuilt with open decisions.

**New evidence.** `create.md:61` and `:63` (master); `refs/claim.md:43` and `scripts/orca_worktree.py:1715` (`already_launched`); `pr-p refs/plan.md:94`.

**Revised adopt/reject list.** Adopt as is: PR 661; `plan_body.py` and plain `--plan`; `--remaining` (orchestrator-only, conditional on the live-head check). Adopt with changes: claim reads and quotes the plan sections (short chain for simple and medium; brainstorm and design seeded with the filed plan for complex); refusal guard on the unattended or orchestrator path only, a manual claim warns and points to `--plan`; `--mode other` as a separate small change; a higher tier floor at create only for medium and complex, if at all. Reject: moving brainstorm and design into create (no actor can run them there); the `## Design` section in the body; a blanket refusal of plan-less claims; the `Fix approach` to `Approach` rename now (defer).

**Changes (ID: old to new).** C-001 OURS 80 to HYBRID 60; C-003 OURS 65 to CLAY 55; C-005 HYBRID 65 to HYBRID 70; C-007 OURS 75 to OURS 62; C-008 OURS 80 to HYBRID 65; C-009 OURS 70 to OURS 62; C-012 OURS 60 to HYBRID 50; C-013 OURS 70 to HYBRID 52; C-014 OURS 75 to OURS 65; X-001 OURS 75 to HYBRID 55; U-001 OURS 65 to OURS 50; U-003 OURS 70 to HYBRID 60. Unchanged: C-006, X-002, U-004, C-004, S-002.

### Variant 2 Advocate (CLAY) rebuttal

**Response to OURS' remaining points.**
1. "No actor at create can run brainstorm or design": partly conceded, partly rebutted. Conceded: 689 does not say who runs them; it says "The create worker calls `/sc:recommend`", and its Dependencies line says the commands "behave as documented when called from create (not re-verified here)"; the create workers have `Read, Grep, Glob, Write, Bash` (`agents/issue-worker-t1.md:5`). Rebutted: "no actor can" is too strong. The calling session already invokes skills (claim Wave 5 invokes `Skill sc-recommend`, `refs/claim.md:79`) and `/sc:brainstorm` has a worker mode (`commands/brainstorm.md:148`). The real barrier is B2 (`refs/chains.md:7`: `/sc:issue` never runs chain commands); 689 moves the rows into create without saying B2 is lifted. `WORKER-CONTRACT.md:23` bars dispatching `/sc:issue` as an Orca worker, not a person-run create session, so OURS credits it too much.
2. 689 unbuilt with open decisions: conceded. 689 also decides nothing for the unattended path; its decision 9 would make PR 690 read create's rule, reopening a reviewed PR.
3. `## Design` in the body: conceded for now (stale-design risk; no stated writer). 4. Rename: defer, conceded. 5. Split refusal guard: agreed; 689 itself marks "refuse and point" as an assumption for Clay to confirm.
One point OURS did not test: 689 quotes a "ruling of 2026-11-20" that brainstorm and design belong to create, text found only in the issue (UNVERIFIED). It is Clay's ruling, not the owner's; it does not by itself outweigh B2/B4/B14.

**Assessment of OURS' revised rule.** Acceptable for simple and medium features, and it removes the `create.md:61` contradiction for them. Missing: (i) "passes the check" must mean more than three headings present (UNVERIFIED what `plan_check` tests beyond headings); (ii) bugs are not covered (bug rows start with `/sc:troubleshoot`); (iii) complex features still plan twice, only seeded, while the create-time Fix approach (`create.md:66`) names workflow, implement, pr-submit and claim overrides it; (iv) the rule must say whether the filed plan overrides the `/sc:recommend` pick (B4); (v) complex still runs on tier 1b at claim, so "strong model at filing" is only partly met. "The right stage-one step; 689's chain move needs a decided actor and a B2 repeal first."

**Who runs brainstorm and design at create.** `docs/designs/orchestrator.md` has no `/sc:brainstorm` call at plan time: the plan call is `Skill sc:issue-protocol --plan` in the orchestrator's own checkout with no `worker-start` (lines 726 and 1083), one `/sc:analyze` pass. Candidate actors (calling session or orchestrator session with `/sc:brainstorm --unattended`) are named by neither 689 nor the design. 689 leaves this open (conceded).

**Final adopt/reject list.** Adopt: PR 661; PR 690 incl. `plan_body.py`, plain `--plan`, `--remaining` (orchestrator-only, subject to the live-head check); OURS' claim rule for simple and medium; complex seeded with the filed plan; split refusal guard; `--mode other` as a separate change; tier floor only for medium and complex. Reject for now: moving brainstorm and design into create; `## Design` in the body; refusing plan-less claims everywhere; the rename. Defer: a one-plan design for complex until the actor and the B2 repeal are decided. HYBRID is honest for C-001, C-005, C-008, C-011, C-012, X-001.

**Changes (ID: old to new).** C-006 OURS 80 to OURS 68; X-002 OURS 78 to OURS 65; U-004 OURS 65 to OURS 55; C-001 CLAY 62 to HYBRID 55; C-005 CLAY 68 to HYBRID 60; C-004 HYBRID 58 to HYBRID 60; C-003 CLAY 66 to HYBRID 58 (not following OURS' move to CLAY 55: the consumer `handback` is unbuilt, head equality UNVERIFIED); C-013 stays OURS 60 (not following OURS' move to HYBRID 52: 689 would leave the Spec stage nothing, and OURS' own revised rule keeps that stage for complex); C-007 OURS 62 and C-009 OURS 60 unchanged.

## Round 2.5: Invariant Probe

Run by one independent fault-finder (see `invariant-probe.md`). 12 findings: 5 HIGH and 6 MEDIUM UNADDRESSED, 1 LOW ADDRESSED. Round 3 is not run at depth standard.
Round 3: skipped (depth=standard).

## Scoring Matrix

Final winner per diff point after Round 2 (a point both advocates name the same winner for is agreed; for the three split points the orchestrator decided, with the reason).

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | tie | 55% | Same section order; cosmetic |
| S-002 | Variant 1 | 68% | OURS ends in a disposition list; CLAY none (both advocates) |
| S-003 | tie | 55% | Both H2 only |
| C-001 | HYBRID | 58% | Both advocates moved to HYBRID: `create.md:61` says "whoever picks it up only executes", claim chain still plans |
| C-002 | HYBRID (both keep PR 661) | 92% | Agreed |
| C-003 | HYBRID (CLAY-leaning) | 56% | OURS advocate: CLAY 55; CLAY advocate: HYBRID 58. `--remaining` has no code coupling to `handback` but its consumer is unbuilt; head equality UNVERIFIED. Resolved by orchestrator as HYBRID |
| C-004 | Variant 1 | 70% | 689 unbuilt, open decisions, actor for brainstorm at create undecided and B2 not lifted; CLAY final list also "reject for now" |
| C-005 | HYBRID | 65% | Both: claim must read the plan; OURS' rule is the stage-one step; complex still plans twice |
| C-006 | Variant 1 | 68% | Gap is real but "no actor can" overstated: the calling session invokes skills (`claim.md:79`); B2 not lifted (`chains.md:7`) |
| C-007 | Variant 1 | 62% | Both agree; staleness is real, larger the stored design the worse |
| C-008 | HYBRID | 62% | Both: split guard, refuse only on the unattended path, warn on manual claim (but see INV-003) |
| C-009 | Variant 1 | 61% | Rename churn against PR 661 tests and `fix_approach` token; defer |
| C-010 | Variant 2 | 55% | Both: `--mode other` as separate small change |
| C-011 | HYBRID | 55% | Floor only for medium and complex |
| C-012 | HYBRID | 52% | Cost unmeasured on both sides; re-claim does not repeat the chain (`already_launched`) |
| C-013 | Variant 1 | 56% | Split: OURS advocate HYBRID 52, CLAY advocate OURS 60. Decided by orchestrator: recorded owner requirements R23/R25 (2026-11-18) weigh for OURS on a tie; still UNVERIFIED as binding (unpushed) |
| C-014 | Variant 1 | 62% | Issue 302 and B2/B4/B14 are the owner's recorded design; CLAY's counter, a "ruling of 2026-11-20" quoted in 689, is Clay's own and UNVERIFIED |
| X-001 | HYBRID | 55% | Both goals real; layered |
| X-002 | Variant 1 | 66% | Workers lack the Skill tool; actor open (both) |
| X-003 | HYBRID | 55% | "Opposite" overstated (both); layered |

## Convergence Assessment

- Points counted: 25 (S 3, C 14, X 3, A 5; U-NNN points are not counted)
- Points resolved (both advocates name the same winner or the same answer): 22 of 25; unresolved before orchestrator decision: C-003, C-013, X-003
- Alignment: 88 percent; threshold 80 percent
- Taxonomy coverage: L1 (S-001 to S-003, C-009) covered; L2 covered; L3 (C-008, C-013, A-002) covered by both advocates
- Shared assumptions: A-001 QUALIFY, A-002 QUALIFY, A-003 QUALIFY, A-004 ACCEPT, A-005 QUALIFY, both advocates, no omissions
- Invariant gate: 5 HIGH UNADDRESSED (INV-001, INV-002, INV-004, INV-005, INV-006), 6 MEDIUM
- Status: BLOCKED_BY_INVARIANTS
- Sycophancy check: OURS' Round 2 conceded five points. The orchestrator checked them: cost (A-002) was conceded on a verified fact (`already_launched`); `--remaining` coupling on a verified grep; R23/R25 was conceded as "cheap to rewrite", which is not a fact about the sources and was not followed on C-013; CLAY's Round 2 declined to follow OURS' concession on C-013 and C-003 and tightened C-006, so the concessions are not mirrored agreement.

