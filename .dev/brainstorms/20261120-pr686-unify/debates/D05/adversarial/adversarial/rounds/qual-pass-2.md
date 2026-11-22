# Qualitative scoring, pass 2 (reverse order: Variant 2 first, then Variant 1), debate D05

Evaluator: independent, CEV protocol, 30-criterion additive binary rubric. Variant 1 = OURS (`variant-1-original.md`), Variant 2 = CLAY (`variant-2-original.md`), both in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D05/adversarial/`. Papers judged on their own pre-debate text; the transcript was used only to check whether a claim was later shown wrong. `rounds/qual-pass-1.md` was not read.

Spot checks in the snapshot `/home/coder/.cache/ic-snap-20261120/master`: LD:23 and D:117 / D:1234 quotes match; `orca_worktree.py` has `publish_pending` at line 1488 and `cmd_pending` at line 1515 (V1 has them swapped); `issue-pipeline-guard-g2.md:9` contains "Before any other issue runs through the flow, the worker must be bound to the guard (G2)".

Section names used in evidence: V1 and V2 both have Claim, Mechanism (items 1-4), Cited facts (1-9), What it costs, What it risks, What it gets right.

## 1. Completeness

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Covers all explicit requirements of the brief | MET | Claim, Mechanism (4 items), Cited facts (9), What it costs, What it risks, What it gets right all present | MET | Same six sections present; 9 cited facts, 4 mechanism items |
| 2 | Edge cases and failure scenarios | MET | Costs: "Fail-closed for a bound worker: LL-BROKEN if `jq` is missing (LD:208-215)"; Risks: "A bare `claude "<prompt>"` runs a turn outside the limits"; pinned leaks | MET | Fact 4: "Identity loss is a declared fail-open (LD:81)"; Costs: "The audit reads pull requests, so a direct push to `master` with no pull request is outside its reach" |
| 3 | Dependencies and prerequisites | MET | Costs: "the claim preflight (jq present, hooks registered, W-ENFORCEMENT-ABSENT refusal; OB-H2 lines 471-472) must run before the first worker"; "A level has to be chosen" | MET | Mechanism 4 (live test records `ls ~/.claude/state/launch-level/sessions/` before and after); Fact 8: D:970 "settled before the first real issue"; Fact 6 (G2 facts 1 to 4, FU-1 precondition f) |
| 4 | Success or completion criteria | NOT MET | No evidence found, searched Claim, Mechanism, Costs, Gets right. Nothing says when "bound" is done or proven (R33 in Gets right is an existing gate, not this paper's criterion) | MET | Fact 7: "`refuse(argv)` has a failing case for every 'may never' pattern (D:1117)"; Mechanism 2: "a test fails if the skill launches through `orca_worktree.py launch` (K4, D:1226)" |
| 5 | Explicitly out of scope | NOT MET | No evidence found, searched Claim, Mechanism, Costs, Risks. Limits of the guard are stated (Risks: "not TH3 (deliberate evasion)") but no scope exclusion for the position | NOT MET | No evidence found, searched Claim, Costs, Risks, Gets right. "left for the owner" is a deferral, not an out-of-scope list |

## 2. Correctness

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | No factual errors or hallucinated claims | NOT MET | Mechanism 2 gives "`cmd_pending` and `publish_pending` ... `:1488` and `:1515`"; snapshot has `publish_pending` at 1488 and `cmd_pending` at 1515 (swapped); "one marker line" omits that the marker slot was deleted with `brief.py` (conceded in debate) | NOT MET | Fact 1: DQ7 "adds no new exposure that the owner's own text did not already describe" cites `issue-pipeline-guard-g2.md:9` but omits its clause "Before any other issue ... the worker must be bound" (snapshot line 9); Fact 2 counts OB-H1 item 8 (issue 678) against binding, later shown parked and not a gate |
| 2 | Technical approach feasible within stated constraints | MET | Mechanism 3: level `FS` allows commit, feature-branch push, `gh pr create --repo`, and the grid refuses PUSHFORM, PROTECTED, MERGE (LD:113-115); Risks states binding of a `worker-start` worker "has never been observed live" | MET | Mechanism 1-4: unbound worker bounded by handoff prompt, ADD1, merge gate `--match-head-commit`, `refuse(argv)`, audit; Costs states "A worker that ignores its prompt can push to `master`" |
| 3 | Terminology consistent and accurate | MET | Preface fixes "the guard", "L2", "D:nnn", "LD:nnn"; used consistently, "governed", "bound", "unbound" used the same way throughout | MET | Same short names defined in preface and used consistently; "guard-less", "unbound" consistent |
| 4 | No internal contradictions | NOT MET | Mechanism 2 "one marker line plus one `pending` call, not new code in the hook" against Risks 2 "never been observed live"; Costs 3 "neither mapping is written down yet" against Gets right 2 "with no new rule" (flagged as X-001 in diff-analysis) | MET | No evidence found of contradiction, searched Claim, Mechanism, Facts 1-9, Costs, Risks. Costs admit the limits of the substitute controls rather than contradicting the Claim |
| 5 | Claims supported by evidence or rationale | MET | Each of Cited facts 1-9 carries a file and line, e.g. Fact 1 "K12 (D:1234) ... `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false`" | MET | Each fact carries a file and line, e.g. Fact 3 "R33 (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` line 59 ...) sets `GOVERNED_LEVELS_ALLOWED = False`" |

## 3. Structure

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Logical section ordering | MET | Claim, Mechanism, Cited facts, costs, risks, gets right (the brief's order) | MET | Same order |
| 2 | Consistent hierarchy depth | MET | One H1, six H2 sections, flat numbered or bulleted lists beneath | MET | Same |
| 3 | Clear separation of concerns | MET | Costs (friction, level choice, fail-closed) kept apart from Risks (false assurance, unobserved binding, 442 open) | MET | Costs (push to `master`, prompt only, WC-9) kept apart from Risks (`refuse` list, scale, later guard extension) |
| 4 | Navigation aids (cross references, short-name index) | MET | Preface: "'the guard' is ... L1 ... 'L2' ... 'D:nnn' ... 'LD:nnn'"; line cites used throughout | MET | Preface defines the same short names; "(DQ7 and K12, decision OD1)" and D:/LD: cites throughout |
| 5 | Follows conventions of a position paper per the brief | MET | Claim first, then mechanism, 9 facts, costs, risks, gets right | MET | Same |

## 4. Clarity

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous language | MET | Claim: "must be bound to the launch-level guard before it runs, including a worker the orchestrator starts with `orca orchestration worker-start`" | NOT MET | Claim says the risk is "left for the owner (decision OD1)" while Fact 8 says OD1 is "Decided by ruling 3"; "owner" is used for the repository owner (LD:23, G2) and for Clay's ruling without distinction |
| 2 | Concrete rather than abstract | MET | Mechanism 3 names levels and rows (PUSHFORM LD:113, PROTECTED LD:114, MERGE LD:115); Fact 1 gives the exact `gh api` command | MET | Mechanism 3 quotes `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>`; Fact 5 names `reply-resolve-thread.sh:131`, `:141` |
| 3 | Each section has a clear purpose | MET | Section titles match content; Costs lists price, Risks lists what could go wrong | MET | Same |
| 4 | Acronyms and domain terms defined on first use | NOT MET | Preface defines guard, L2, D:, LD:; but DQ7, K12, OD1, G2, WC-9, FU-1, TH3, R33 (partly glossed) and OB-H1/OB-H2 are used without definition | NOT MET | Preface defines guard, L2, D:, LD:; but DQ7, K12, OD1, ADD1, R9, K4, K22, U42, AU1 to AU8, 5.9, 5.11, WC-9, FU-1, G2 are used without definition |
| 5 | Actionable next steps or decision points | MET | Costs: "the claim preflight ... must run before the first worker"; "A level has to be chosen for implementation workers ... `FS` fits OD1, `F` fits WC-9" | MET | Claim: "named, graded and left for the owner"; Fact 8: D:970 "settled before the first real issue"; Mechanism 4 live test |

## 5. Risk Coverage

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | NOT MET | Risks lists three risks (false assurance, unobserved binding, 442 open) with no likelihood or impact; only Clay's K12 "M / H" is cited in Fact 1 | NOT MET | Risks lists three items with no likelihood or impact; only K12 "graded M / H" in Fact 8 (one risk) |
| 2 | Mitigation for each identified risk | NOT MET | No evidence found, searched What it risks (3 bullets), Costs, Gets right. No bullet carries a mitigation | NOT MET | No evidence found, searched What it risks (3 bullets), Fact 7, Fact 8. Fact 8 says K12 "with its mitigations" but the three Risks bullets have none (U42 "is open") |
| 3 | Failure modes and recovery | NOT MET | Failure behaviours stated ("fails open ... allowed silently", "Fail-closed ... LL-BROKEN"), but no recovery path anywhere | MET | Fact 7: merge gate "refuses `threads_open`, `changes_requested`, a moved head and an unreadable state"; audit "escalates only the violations that can leave a merge broken or unreviewed (D:822-828)" |
| 4 | External dependencies and their failure | MET | Costs: "`jq`, hooks registered, W-ENFORCEMENT-ABSENT"; Risks 2: "first-prompt delivery by `worker-start` ... is the open question"; Risks 1: bare `claude` turn (issue 678) | MET | Costs: "`protected: false`, no rulesets, D:118"; Fact 6: G2 facts 1 to 4 UNVERIFIED about `worker-start` session id and `send`/`ask` |
| 5 | Monitoring or validation mechanism for risk detection | MET | Costs: claim preflight (jq present, hooks registered, W-ENFORCEMENT-ABSENT refusal) before the first worker; Fact 6 live observations as validation | MET | Mechanism 4: live test records `ls ~/.claude/state/launch-level/sessions/` before and after; Mechanism 3: audit AU checks after landing (D:801-828) |

## 6. Invariant and Edge Case Coverage

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Collection boundaries (empty, single, maximum) | NOT MET | No evidence found, searched Mechanism, Costs, Risks. No empty, single or maximum case for workers, sessions or pending records | MET | Risks 2: "the orchestrator runs up to three issues at once (D:698-718), each with a worker holding push rights on its own branch" (maximum) |
| 2 | State-variable interactions across component boundaries | MET | Mechanism 1: marker in first prompt plus "matching `pending/<nonce>` record in `~/.claude/state/launch-level/`"; Mechanism 2: helper `publish_pending` writes the record the hook reads | MET | Mechanism 1: guard binds only with `[sc-launch:v1:<32 hex>]` plus pending nonce; Costs: "`install_l2` runs only in the claim's launch step" |
| 3 | Guard-condition gaps | MET | Risks 1: "Pinned leaks stay allowed: `bash ./push.sh`, `G=gi; ${G}t push origin main` (LD:122)" | MET | Fact 4: "Identity loss is a declared fail-open (LD:81). Pinned leaks stay allowed"; Costs: audit cannot see a push with no pull request |
| 4 | Count-divergence (first versus second issue) | MET | Fact 2: "The owner's acceptance was for one issue ... 'Before any other issue runs through the flow, the worker must be bound to the guard (G2)'. DQ7 stretches a one-issue acceptance into the standing rule" | NOT MET | Fact 1 cites "the first test issue" but concludes DQ7 "adds no new exposure", missing the "before any other issue" clause; Risks 2 on up to three issues is scale, not a first-versus-second divergence |
| 5 | Interaction effects when components combine | MET | Costs 2: guard blocks compound pushes (LL-PUSH-FORM, LD:283) and inline `gh api` writes (GHWRITE, LD:116) against the PR workflow | MET | Fact 5: "The guard and the pull-request workflow rub against each other ... `/sc:pr-submit` ... `resolveReviewThread` ... GHWRITE, LD:116" |

## Subtotals

| Dimension | V1 | V2 |
|---|---|---|
| Completeness (5) | 3 | 4 |
| Correctness (5) | 3 | 4 |
| Structure (5) | 5 | 5 |
| Clarity (5) | 4 | 3 |
| Risk Coverage (5) | 2 | 3 |
| Invariant and Edge Case Coverage (5) | 4 | 4 |
| **Total (30)** | **21** | **23** |

## Edge-case floor check

Floor: a variant scoring below 1 of 5 on Invariant and Edge Case Coverage is ineligible as base.

- V1: 4 of 5. Eligible.
- V2: 4 of 5. Eligible.

## Notes on close calls

- Correctness 1: both fail. V1 on the swapped `cmd_pending` / `publish_pending` lines and the understated "one marker line"; V2 on the G2:9 reading that omits the "before any other issue" clause. Neither is fatal to the paper's thesis.
- Correctness 4: V1 fails on the internal tension named X-001 in diff-analysis (conceded by V1's advocate in Round 2). V2 passes because its Costs section discloses what its substitute controls cannot do instead of claiming they can.
- Edge case 4 splits the papers in V1's favour: only V1 uses the first-versus-second issue divergence. Edge case 1 splits it in V2's favour: only V2 states a maximum (three issues).
- Neither paper gives probability and impact for its own risks, nor a mitigation per risk, so Risk Coverage is low for both.

