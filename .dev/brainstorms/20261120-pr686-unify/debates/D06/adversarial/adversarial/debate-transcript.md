# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe)
- Convergence achieved: 100% on diff points; gate status BLOCKED_BY_INVARIANTS
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant A OURS, Variant B CLAY; general-purpose agents, read-only)
- Note: the weighting rule was given to both advocates; see the process note under Round 2.5

## Round 1: Advocate Statements

### Variant A Advocate (OURS, general-purpose agent)

**Position**: Variant A should win on C-001, C-003, C-005 and C-006. The merge into an unprotected default branch, who may run `/sc:pr-submit`, and who may grant authority all stay with the person. Two parts of Variant B can be separated from those rules and adopted as a HYBRID: the merge-time reviewer check (C-004) and the head-pinned, fail-closed form of `gh pr merge`.

**Steelman of Variant B**:
An orchestrator that owns an issue from handoff to merge is useless if a person must answer at every step. B turns "the person's go" into something testable: a closed gate of 13 reasons, a `gh pr merge --match-head-commit` call with no `--auto`, `--admin` or `--delete-branch`, and a hard hold on merge-safety files (orchestrator.md D:118, D:586-593). It also finds a real gap. The PR loop treats a late reviewer as absent for the rest of the run (SKILL.md:29-32 (master)), and the owner's own memory records a Codex security review landing after a "clean" result. B states its costs honestly (unbuilt machinery, unprotected master, an answer source it cannot verify).

**Key strengths claimed**:
1. The line is the owner's. WORKER-CONTRACT.md:241 requires the user's instruction to name each outward action. :245 says "no earlier pre-authorization waives this". :244 and :23 keep `/sc:pr-submit` off workers. APPROVED.md:10-13 records D3, D4 and D5, with "Nothing here is reopened" at :3.
2. B's own ADD1 (D:135) says the autonomous merge in ruling R10 "contradict[s] all of this". B reverses owner decisions on Clay's authority alone, and FULL-REPORT.md section 4 says no `ironbelly` approval of PR 681 exists (the advocate did not re-check that file).
3. A is not "never automate". R25 and R9/R17 already allow a script-started coordinator and an automated Full Submit that "never merges"; they need an authorization the owner records in chat.
4. Nothing on GitHub stops a bad merge. B's DQ8 and K12 agree master is unprotected. The person's go is the only brake.
5. B's `answer-check` is not a stronger guard than chat approval. D:694 calls the "typed by a person" check "FR-17's accepted v1 guard", and the design's wake path types into the same terminal.

**Weaknesses identified in Variant B**:
1. The merge gate, `answer-check` and `grants` do not exist in master, PR 686 or `issue-655-pr-p` (B's own admission), so C-001 would run on prose first and machinery later.
2. The contract text leaves a route open (:23 "If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard"). ADD1 states no brief-guard route; it adds a new contract section. D3's own preconditions (AC-4.3 live check, D4 (a)) were never run.
3. B says a worker can open PRs through `/sc:pr-submit`, yet ADD1 itself says the skill "has no unattended mode" (D:135). Unresolved contradiction in B.
4. A repo-level standing `grants` list (C-007) is broader than a per-issue go and conflicts with :245.
5. B's reviewer lists are marked UNVERIFIED as the permanent set (D:138).

**Concessions**:
- A has no merge-time check for a late reviewer.
- The merge-and-typed-go rules are prose with no hook behind them (tech reference :318).
- A person is a bottleneck when absent.
- R25 sits in a local, unpushed plan, so it is not a rule in force.
- A's reading of D5 as a depth rule is partly beaten: that reason covers `worker-start` starts only.
- WORKER-CONTRACT.md:23 weakens "never a worker" from absolute to "while D3 says so".

**Shared assumptions**:
- A-001 QUALIFY: the loop layer and the merge layer are separable. Skip in the loop, check the final head at merge. `merge_wait` already tracks `absent` and `incomplete` separately (reviewers.py:395-424).
- A-002 ACCEPT: both depend on a person who answers. An unanswered question waits.
- A-003 REJECT: a typed go cannot yet be told apart from text typed by an agent. Neither side has a mechanical guard.
- A-004 ACCEPT: master is unprotected and the choice is made without a GitHub-side control. A repo admin enabling branch protection or required review would be a separate hybrid (feasibility UNVERIFIED).
- A-005 QUALIFY: reviewer sets are observed on few PRs; the list should be a per-repo setting the owner sets, not detected.

**Point positions**: C-001 A (separable hybrid: head-pinned merge flags and fail-closed file list offered as the check run at the person's go). C-003 A. C-004 B's merge-time check is a clear benefit, separable: HYBRID. C-005 A for now; answer-check worth adopting only if it can tell person from script, which B concedes it cannot. C-006 A; B's nine-row list adoptable only after the owner records it in chat. X-001 QUALIFY. X-004 A. X-005 R25 not yet in force.

### Variant B Advocate (CLAY, general-purpose agent)

**Position**: On authority, OURS should win. The person's go for a merge and for pushing a PR stays the rule. Four parts of CLAY are clear and separable and should be adopted as a hybrid: the mechanical merge gate, the merge-time reviewer hold, `answer-check` as a validator, and the script start of a depth-0 coordinator.

**Steelman of Variant A**:
The default branch is unprotected and the acting user holds `maintain` (DQ8, orchestrator.md:118; K12 at :1234). So the person's go is the only brake on a merge. The owner decided D3, D4, D5 and GIT on 2026-11-02, and ADD1 itself says R10's autonomous merge "contradict[s] all of this" (:135). Master WORKER-CONTRACT still says PRs go "never as a worker" (:244) and pushes need "the person's go; no earlier pre-authorization waives this" (:245). OURS is not "never automate": R9, R17 and R25 already allow a script-started coordinator and a per-issue Full Submit go. D3's AC-4.3 live check was never run, and pr-submit has no unattended mode (:135).

**Key strengths claimed**:
1. The gate turns prose into a test: 13 closed reasons, head-pinned `gh pr merge --match-head-commit` with no `--auto`, `--admin`, `--delete-branch`, re-run within 2 minutes of the merge (D:582, :588; DQ8 :118). A restart reads the PR state first, so there is never a second merge (:591). The file list fails closed (:597). OURS has nothing equivalent; its own costs admit "nothing mechanical binds the coordinator."
2. The reviewer hold fixes a real gap in the skip rule. `/sc:pr-submit` marks an absent reviewer "sticky ... ignored for the rest of the run" (SKILL.md:29-32). `merge_wait` also calls a reviewer absent on a clock alone (reviewers.py:390-391); with one done and one absent the outcome is "clean" (:417-419). Only a per-repo `reviewers` list at merge time catches a late Codex review. The hold sits at the merge decision, not in the fix loop.
3. `answer-check` binds an answer to one question key and one head SHA and requires it to be newer than the notice (:694). An approval of one head cannot stand for another.
4. The `merge_safety` hold and the `changes_requested` hard refusal (:583, :593) are stricter than OURS, which has neither.
5. The script start is compatible with D5. D5's precondition is "a root session ... never one started with `worker-start`" (D5 rec:9, :47). A terminal plus `ccsession` is depth 0 (:112), and OURS's own R17 allows a script start.

**Weaknesses identified in Variant A**:
1. Its mechanism is prose only; a "go" can be relayed or stale with no key or head binding.
2. It has no merge-time reviewer check (conceded).
3. R25 sits in an unpushed local plan and sits awkwardly with :245; A's R17 standing authorization is the same kind of pre-authorization A criticizes in CLAY's `grants`.
4. A reads D5 "person opened" wider than D5's own text, which is about `worker-start` depth.

**Concessions**:
- None of the gate, `answer-check` or `grants` is built (no `merge-gate` or `answer-check` in master, PR 686 or `issue-655-pr-p`).
- `answer-check --source` is self-declared (D:694 "accepted v1 guard"); the wake path types into the same terminal (:112), so the verb cannot tell a person from a script.
- CLAY reverses D3, D4, D5 (ADD1 :135); Clay alone approved it; K12 is an accepted risk, not a mitigation. ("Clay approved only" and "no ironbelly approval" are UNVERIFIED for this advocate.)
- Under the weighting rule the authority-transfer parts (orchestrator merges on its own, a worker runs pr-submit) do not clear the bar.

**Shared assumptions**:
- A-001 ACCEPT: the fix loop and the merge decision are separate layers; that separation lets the hold be adopted without changing the loop.
- A-002 QUALIFY: a person is reachable only sometimes; "an unanswered question waits, no default" (:692) and A's go both stall when nobody answers.
- A-003 QUALIFY: neither side can tell a typed go from script-typed text; answer-check narrows the gap but cannot close it.
- A-004 ACCEPT: DQ8 shows no branch protection, and only a repo admin can add it. Strongest argument for keeping the person's go.
- A-005 QUALIFY: reviewer sets come from three repos and are UNVERIFIED (:138); stable enough for an owner-set list, not for auto-detection.

**Point positions**: C-001 A on who decides to merge; the gate is separable and adopted as a precondition the person's go consults. C-003 A (AC-4.3 never run; pr-submit has no unattended mode). C-004 CLAY on the merge-time hold, separable: hybrid. C-005 CLAY's answer-check is the better mechanism as a validator of a person's chat go. C-006 A on reaching the person at each outward action; the nine-row list is useful as an inventory of reasons, authority part not adopted. X-001 CLAY (D5's text limits the reason to `worker-start` depth). X-004 both (checkable on key, entry, freshness; unreliable on source). X-005 against OURS (R25 unpushed; :245 bars pre-authorization).

## Round 2: Rebuttals

### Variant A Rebuttal (OURS)

**Response to criticisms**
- (a) Prose only, no key or head binding: CONCEDE for stale answers. Counter: binding to a question key and head sha does not stop a relayed answer, because B's own verb cannot tell person from script (D:694, "FR-17's accepted v1 guard"). It is a stale-answer guard, nothing more.
- (b) No merge-time reviewer check: CONCEDE; B's clock reading is correct. `codex_wait_outcome` returns absent when `other_settled` or elapsed >= min(silence_timeout, timeout) (reviewers.py:390-391); `merge_wait` then uses only the done reviewer (:414-419), so one done plus one absent gives clean or findings. SKILL.md:31-32 makes absence sticky and rebuilt on `--resume`. The fix belongs at merge, not in the loop.
- (c) R25 and R17 are pre-authorization: CONCEDE in part. R25 says "Rule change to state in the contract" and calls the label "the person's go" (requirements.md R25), so it amends :245 rather than complying with it. Difference from `grants`: per issue, owner-recorded, a feature-branch push and PR only, "never merges". R17 is the same kind of standing authorization as `grants`, limited to issue-pipeline duties, no merge.
- (d) D5 over-read: CONCEDE. D5 rec:9 is about `worker-start` depth. "Person opened" (WORKER-CONTRACT.md:70) is a separate authority rule. A ccsession-started coordinator is depth 0 and acceptable if its launch prompt states the owner's recorded authorization (R17 caveat).

**Updated assessment**
1. Mechanical merge gate: ACCEPT WITH A CHANGE. It runs as a read-only check whose output is shown to the person before the go. Pinned flags and the fail-closed file list accepted. The merge call stays behind the person's go; any path where a passing gate triggers the merge is rejected.
2. Merge-time reviewer hold: ACCEPT. Owner-set per-repo `reviewers` list (`none` allowed); the check re-polls the final head and does not read the loop's sticky absent state; 60 minutes is a default (UNVERIFIED as the right number).
3. answer-check: ACCEPT WITH A CHANGE, as a validator for stale or mismatched chat answers only, never as proof of a person.
4. Script-started depth-0 coordinator: ACCEPT WITH A CHANGE; the launch prompt states the owner's recorded authorization and lists only duties the owner wrote down.
The person's go at merge contains: repo, PR number, full 40-character head sha, merge method, the word "merge", and a reference to the gate output shown (within the gate's 2-minute window); typed in live chat, newer than the gate output; void if the head moves. R25 and R17 need an owner chat approval and a one-sentence amendment of :245 before they count: "A push of a feature branch for an issue the owner set to Full Submit and approved with the approval label counts as the person's go for that issue's push and pull request only, and never covers a merge, a force push, a branch deletion or any other push."

**New evidence**: WORKER-CONTRACT.md:241 ends "unless that instruction is in its live conversation" (a live-chat go needs no second confirmation). reviewers.py:379-382 documents absent as a clock or settled-peer outcome, not a finding that the reviewer is not installed (best evidence for the merge-time hold).

### Variant B Rebuttal (CLAY)

**Response to criticisms**
- Unbuilt gate, answer-check, grants: conceded (a design, not code; build tasks, not a reason to reject the checks).
- WORKER-CONTRACT.md:23 door: conceded. ADD1 (D:135) states no brief-guard route; D3's preconditions (AC-4.3, D4 (a)) never ran.
- grants vs :245: partly answered. DQ6 scopes each use to a listed repo and one issue assigned to the user and routed to this orchestrator (D:116). Still a standing grant; needs the owner's chat amendment like A's R25 and R17. Conceded.
- Reviewer lists UNVERIFIED (D:138): agreed; ADD4 already has the owner set the list, `none` included.
- answer-check cannot tell a person from a script (D:694): conceded; a validator only.

**Remaining dispute** (judged under "OURS unless a clear, evidenced benefit")
1. Autonomous merge for a narrow class of PRs: no clear evidenced benefit (only throughput while nobody is present; no measured figure; master unprotected D:118; AU4a is an audit after the fact D:812). OURS.
2. Worker runs pr-submit: no evidenced benefit over R25's launch route. OURS.
3. Repo-level `grants` including `pr.merge` and `issue.close`: not shown. OURS.
4. One separable part of grants worth keeping: `E-NO-GRANT` (D:696), the verb refusal of any GitHub write not on the list; the only mechanical bind either side has. Hybrid: keep the refusal; the list holds only duties the owner recorded in chat, with no `pr.merge`.
5. Nine-row table (D:672-696): modest and separable; adopt as the list of reasons for non-outward decisions only. Benefit UNVERIFIED (no use shown).
6. `changes_requested` as a hard refusal that no OK overrides (D:583): a real difference; in A's hybrid the person's go could merge over it. The spec must say which and the gate output must print it.

**Hybrid gaps**
- Go window: the 2-minute window covers check and review state; the head is pinned by `--match-head-commit` (D:118). Require the gate to run again immediately before the merge (D:588); any new reason voids the go.
- Absent person: "waits, no default" (D:692) is right, but A's go has no expiry; add a limit after which the go is void and the gate output is shown again.
- Spoofed typing: "live chat newer than the gate output" cannot be told from `orca terminal send` into the same terminal (D:112); a script knows the full sha. Whether the harness marks sent text differently from typed text is UNVERIFIED. State it as a residual risk.
- Method: the go names the method and the gate checks it against `merge_method` or `release_merge_method` (the squash merge of release 6.1.0 (#658) was reverted by #662, D:118).
- Restart: read the PR state first (D:591), so a go cannot cause a second merge.
- Keep the AU4a and AU7 audit after merge even when a person gave the go (D:812, D:601).

**New evidence**: D:597: `gh pr diff --name-only` does not print `previous_filename`, so a rename out of `.github/workflows/` is invisible to a person reading that diff; the gate sees it, so the gate output belongs in front of the go. Net: CLAY's clear, separable benefits are the gate, the merge-time reviewer hold, answer-check as a validator, `E-NO-GRANT` and the script start of a depth-0 coordinator. Merge authority is not among them.

## Round 2.5: Invariant Probe (summary)

An independent fault-finder agent probed the emerging consensus in six categories. Full table: `invariant-probe.md` (13 findings: 7 HIGH UNADDRESSED, 5 MEDIUM, 1 ADDRESSED as a named residual risk). Headline findings: the pinned head sha does not cover state that changes without a new commit (INV-001, INV-013); a go has no expiry or recorded entry (INV-002); nothing verifies that a person typed the go (INV-003); the go's reach over the 13 gate reasons is undefined (INV-004); the merge-time hold depends on a re-trigger the loop never performs (INV-009, INV-012); a launch-prompt authorization is self-attested (INV-010); `E-NO-GRANT` only sees writes made through the orchestrator's own verbs (INV-011).

Gate result: CONVERGENCE BLOCKED by 7 HIGH-severity UNADDRESSED invariants (INV-001, INV-004, INV-009, INV-010, INV-011, INV-012, INV-013). Depth is `standard`, so no Round 3 runs. Per the protocol the pipeline force-selects by score, documents the non-convergence, and carries every blocked item into the refactor plan as a required spec closure.

Process note: both advocates were given the owner's weighting rule in their prompts, and both ended close to the same hybrid in Round 1. Agreement on diff points is therefore partly a product of the shared rule, not only of the evidence; the invariant probe is the check on that.

## Scoring Matrix

"A" = Variant 1 (OURS), "B" = Variant 2 (CLAY). "Hybrid" means one side wins the rule and the other side's separable part is adopted.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Tie | 90% | Same layout; both advocates agree it decides nothing |
| S-002 | A | 75% | Owner decision records outweigh design-doc rulings under the weighting rule (both advocates) |
| S-003 | Tie | 80% | Both candid; both advocates agree |
| C-001 | A (Hybrid) | 88% | Person's go stays; B's head-pinned, fail-closed gate adopted as a read-only precondition (A Round 2, B Round 2) |
| C-002 | Hybrid | 85% | Script start allowed at depth 0 with owner-recorded authorization (both conceded; INV-010 open) |
| C-003 | A | 92% | D3 stands; AC-4.3 never run; ADD1 states no brief-guard route (both) |
| C-004 | B (Hybrid) | 85% | Merge-time reviewer hold adopted; loop keeps its skip rule (both; INV-009 open) |
| C-005 | Hybrid | 75% | Chat go stays; `answer-check` as a stale-answer validator only (both) |
| C-006 | A | 85% | Person reached at each outward action; nine-row table only as reasons list (both) |
| C-007 | A (Hybrid) | 85% | No repo-level `pr.merge` or `issue.close` grants; `E-NO-GRANT` refusal kept (B Round 2) |
| C-008 | A | 90% | Unprotected master and unguarded workers: B concedes K12 is accepted risk, not mitigation |
| C-009 | Tie | 70% | Both unenforced: A prose, B unbuilt; both conceded |
| C-010 | A | 85% | B concedes authority-transfer parts do not clear the weighting bar |
| X-001 | B | 85% | D5's text is about `worker-start` depth; terminal plus ccsession is depth 0 (A conceded) |
| X-002 | A | 88% | ADD1 reverses D3, D4, D5 (B conceded) |
| X-003 | B | 85% | Skip is sticky and clock-based (reviewers.py:390-391); late reviews are lost (A conceded) |
| X-004 | Hybrid | 80% | Checkable on key, entry, freshness; not on source (both) |
| X-005 | B | 85% | R25 amends :245 and is in an unpushed plan; needs owner chat approval and an amendment (A conceded) |
| A-001 | Agreed: separable | 88% | Loop and merge layers separable (both; INV-009 shows a shared re-trigger step) |
| A-002 | Agreed | 85% | Both depend on a person who answers; unanswered waits |
| A-003 | Agreed: no guard | 90% | Neither side can tell a typed go from script-typed text (INV-003 residual risk) |
| A-004 | Agreed | 90% | Unprotected master is why the go matters; admin-side protection is a separate option |
| A-005 | Agreed | 85% | Reviewer list is an owner-set per-repo setting, not detected |

## Convergence Assessment
- Points resolved: 23 of 23 (every diff point has an agreed winner, a tie or an agreed hybrid)
- Alignment: 100% on diff points (20 resolved to a named side, an agreed hybrid or an agreed assumption; 3 ties counted as agreed)
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (S-002, S-003, C-002, C-003, C-006, C-007, C-009, C-010, X-002, A-001, A-002, A-005), L3 (C-001, C-004, C-005, C-008, X-001, X-003, X-004, X-005, A-003, A-004): all covered
- Status: BLOCKED_BY_INVARIANTS (7 HIGH-severity UNADDRESSED invariants: INV-001, INV-004, INV-009, INV-010, INV-011, INV-012, INV-013)
- Unresolved points: none among S/C/X/A; open sub-points inside C-001: whether the person's go may override `changes_requested` (B Round 2, item 6), the go expiry, the second gate run
- Final status handling: no Round 3 at depth standard; force-select by score; non-convergence documented; closures carried into `refactor-plan.md`
