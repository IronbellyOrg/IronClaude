# Qualitative rubric, position-bias pass 1 (order: V1 OURS, then V2 CLAY), debate D05

Evaluator: independent, CEV protocol, 30 binary criteria. Papers judged on their own original text. Debate transcript used only to check whether a claim was later shown wrong. Snapshot spot checks: `/home/coder/.cache/ic-snap-20261120/master`.

Spot checks done in the snapshot: `orca_worktree.py` has `publish_pending` at line 1488 and `cmd_pending` at line 1515 (V1 has them the other way round). `docs/designs/issue-pipeline-guard-g2.md:9`, `docs/designs/orchestrator.md:1234` (K12) and `docs/designs/sc-issue-launch-level-hook.md:23` read as both papers quote them.

## 1. Completeness

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Covers all explicit requirements of the brief | MET | Sections Claim, Mechanism, Cited facts (9 items), What it costs, What it risks, What it gets right | MET | Same six sections, 9 cited facts |
| 2 | Edge cases and failure scenarios | MET | Costs: "Fail-closed for a bound worker: LL-BROKEN if `jq` is missing"; "compound pushes ... LL-PUSH-FORM"; Risks: "A bare `claude \"<prompt>\"` runs a turn outside the limits" | MET | Costs: "A worker that ignores its prompt can push to `master`"; "a direct push to `master` with no pull request is outside its reach"; Cited fact 4: "Identity loss is a declared fail-open" |
| 3 | Dependencies and prerequisites | MET | Costs: "the claim preflight (jq present, hooks registered, W-ENFORCEMENT-ABSENT refusal ...) must run before the first worker"; "A level has to be chosen" | MET | Cited fact 6: G2 facts 1 to 4 and "FU-1 precondition f (does `worker-start` deliver a bound first prompt)"; Mechanism 1: marker plus pending nonce needed to bind |
| 4 | Defines success or completion criteria | NOT MET | No evidence found, searched Claim, Mechanism, What it costs, What it gets right. The Claim says every worker "must be bound ... before it runs" but gives no pass test for done | NOT MET | No evidence found, searched Claim, Mechanism, What it gets right. Mechanism 4 names a probe (`ls .../sessions/` before and after) but no pass condition |
| 5 | Explicitly states what is out of scope | NOT MET | No evidence found, searched Claim, Mechanism, What it risks. "not TH3 (deliberate evasion)" describes the guard's limit, not an exclusion from the paper's own proposal | NOT MET | No evidence found, searched Claim, Mechanism, Cited facts. Same TH3 and "not a sandbox" text (fact 4) is a limit of the guard, offered as argument |

## 2. Correctness

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | No factual errors or hallucinated claims | NOT MET | Mechanism 2: "`cmd_pending` and `publish_pending` ... `orca_worktree.py:1488` and `:1515`" is swapped (snapshot: `publish_pending` 1488, `cmd_pending` 1515). Claim says issues 394, 442, PR 685 and R33 "all assume nothing the system starts runs ungoverned", which LD:23 and LD:349 contradict (X-003 in the debate, conceded). Mechanism 2 "one marker line ... not new code" was conceded as false for the whole job (marker slot deleted by PR 682, no `cmd_pending` preflight) | MET | No wrong cited fact found. Checked LD:23, D:1234, g2.md:9 against the snapshot. Overreach only: fact 6 lists G2 facts 1 and 4 as binding unknowns although level FS needs neither (conceded Round 2), and fact 2 counts OB-H1 item 8 although #678 is parked. These are weak relevance, not false statements |
| 2 | Technical approaches feasible with stated constraints | MET | Mechanism 1 to 3: marker in first prompt plus `pending/<nonce>`, level `FS` maps to OD1; Risks admit first-prompt delivery by `worker-start` is open | MET | Mechanism 3: handoff prompt, ADD1 contract section, `refuse(argv)`, head-pinned merge, audit; Mechanism 4 live probe |
| 3 | Terminology consistent and accurate | MET | Preface fixes "the guard", "L2", "D:nnn", "LD:nnn"; used consistently, "FS" defined at Mechanism 3 | MET | Same short names used consistently; "unguarded", "guard-less" and "unbound" used for one state |
| 4 | No internal contradictions | NOT MET | Mechanism 2 "Binding an orchestrator worker is therefore one marker line in the brief plus one `pending` call, not new code in the hook" against Risks "Binding of a `worker-start` worker has never been observed live. G2 facts 1 to 4 are UNVERIFIED" (X-001) | MET | No evidence of contradiction found, searched all six sections. Claim, fact 3 and fact 1 agree that the worker is unbound today |
| 5 | Claims supported by evidence or rationale in the document | MET | Nine numbered facts with file:line, e.g. fact 1 "`gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false`"; fact 2 quotes g2.md:9 | MET | Nine numbered facts with file:line, e.g. fact 1 LD:23 quote; fact 7 "`refuse(argv)` has a failing case for every 'may never' pattern (D:1117)" |

## 3. Structure

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Logical section ordering | MET | Preface, Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right | MET | Same order |
| 2 | Consistent hierarchy depth | MET | One H1, six H2, flat numbered or bulleted lists | MET | Same |
| 3 | Clear separation of concerns | MET | Costs hold effort and friction (marker line, compound pushes, level choice, LL-BROKEN); Risks hold false assurance and open evidence | NOT MET | "What it costs" bullets 1 and 2 ("A worker that ignores its prompt can push to `master`", "a direct push ... is outside its reach") are exposure statements, and "What it risks" then repeats the same exposure (K22). Borderline overlap between cost and risk |
| 4 | Navigation aids | MET | Preface defines short names "the guard", "L2", "D:nnn", "LD:nnn"; facts cross-reference each other (fact 3 to D:970, D:975) | MET | Preface defines the same short names; facts cite D and LD lines |
| 5 | Follows artifact-type conventions (position paper per the brief) | MET | Claim, mechanism, cited facts, cost, risk, "what it gets right" as the brief requires | MET | Same |

## 4. Clarity

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous language | MET | Claim: "must be bound to the launch-level guard before it runs, including a worker the orchestrator starts with `orca orchestration worker-start`" | MET | Claim: "do not need the launch-level guard or the L2 pre-push hook, and the design must not make them wait for it" (fact 3 "both lines run an unguarded worker" is mildly ambiguous, not enough to fail) |
| 2 | Concrete rather than abstract | MET | Fact 6 lists LL-COMMIT counts per session with observation-results line numbers | MET | Fact 5 names `reply-resolve-thread.sh:131`, `:141` |
| 3 | Each section has a clear purpose | MET | Section titles state purpose; each list serves it | MET | Same |
| 4 | Acronyms and domain terms defined on first use | NOT MET | Defined: guard, L2, D:, LD:, FS. Undefined on use: OD1, DQ7 (glossed only as "rule"), G2, TH3, OB-H1, OB-H2, OB-CTX, PUSHFORM, GHWRITE, WC-9 | NOT MET | Defined: guard, L2, D:, LD:. Undefined on use: FS (fact 2), OD1, K22, U42, TH3, IR-1, AU1 to AU8, GHWRITE, LL-PUSH-FORM |
| 5 | Actionable next steps or decision points | MET | Costs: "claim preflight ... must run before the first worker"; "neither mapping is written down yet" | MET | Claim: "left for the owner (DQ7 and K12, decision OD1)"; fact 8 "settled before the first real issue" |

## 5. Risk Coverage

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | NOT MET | Three risks listed (false assurance, binding unobserved, 442 still open) with no probability or impact. Only K12 "medium likelihood, high impact" (fact 1) is graded, and it is Clay's grade of one exposure | NOT MET | Three risks listed (K22, scale, guard extended later) with no grade. Only K12 "graded M / H" (fact 8) |
| 2 | Mitigation for each identified risk | NOT MET | Risks bullets carry no mitigation; "What it gets right" mentions R33 gate only | NOT MET | K12 has mitigations (Mechanism 3, fact 8); K22, scale and "guard later extended" have none (U42 left open) |
| 3 | Failure modes and recovery | MET | Costs: "LL-BROKEN if `jq` is missing"; "a blocked compound command was re-issued in split form" | MET | Fact 7: merge gate "refuses `threads_open`, `changes_requested`, a moved head and an unreadable state"; audit "escalates only the violations that can leave a merge broken or unreviewed" |
| 4 | External dependencies and their failure | MET | Costs: "jq present, hooks registered"; Risks: first-prompt delivery by `worker-start`; fact 1 `master` unprotected on GitHub | MET | Costs: "`protected: false`, no rulesets ... nothing on GitHub stops it"; fact 6 G2 facts about Orca `send` and `ask` unverified |
| 5 | Monitoring or validation mechanism for risk detection | MET | Costs: claim preflight with "W-ENFORCEMENT-ABSENT refusal" that refuses when enforcement is missing | MET | Mechanism 4: "records `ls ~/.claude/state/launch-level/sessions/` before and after the worker starts"; Mechanism 3 audit AU1 to AU8 after landing |

## 6. Invariant and Edge Case Coverage

| # | Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence |
|---|---|---|---|---|---|
| 1 | Boundary conditions for collections (empty, single, maximum) | NOT MET | No evidence found, searched Mechanism, Costs, Risks. No case for zero, one or many workers, pending records or sessions | MET | Risks: "the orchestrator runs up to three issues at once (D:698-718), each with a worker holding push rights on its own branch" (maximum case) |
| 2 | State-variable interactions across component boundaries | MET | Mechanism 1: marker plus "matching `pending/<nonce>` record in `~/.claude/state/launch-level/`", hook "binds the session id" (helper in `orca_worktree.py`, state read by the hook) | MET | Mechanism 1: binds "only a session whose first prompt carries `[sc-launch:v1:<32 hex>]` plus a pending nonce"; Mechanism 4 sessions directory before and after |
| 3 | Guard-condition gaps (missing validation, unguarded assumptions) | MET | Risks: "Pinned leaks stay allowed: `bash ./push.sh`, `G=gi; ${G}t push origin main` (LD:122)"; "unbound session is allowed silently" (Mechanism 4) | MET | Fact 4: "Identity loss is a declared fail-open (LD:81). Pinned leaks stay allowed"; Costs: audit cannot see a push with no pull request |
| 4 | Count divergence (first versus second issue) | MET | Fact 2: acceptance "was for one issue, not for the design"; g2.md "for the one first test issue ... Before any other issue runs through the flow, the worker must be bound" | NOT MET | Fact 1 cites "accepted the guard-less worker for the first test issue" but drops the clause "before any other issue", so the one-versus-standing divergence is missed (conceded in Round 2). Fact 8 "settled before the first real issue" names a boundary without analysing it |
| 5 | Interaction effects when components combine | MET | Costs: guard blocks "compound pushes (`git push origin f 2>&1 \| tail -5` is LL-PUSH-FORM)" and "inline `gh api` writes (GHWRITE)" in the pull-request flow | MET | Fact 5: "`/sc:pr-submit` resolves review threads with `gh api graphql ...` ... a class the guard blocks at every level when typed inline" |

## Subtotals

| Dimension | V1 (of 5) | V2 (of 5) |
|---|---|---|
| Completeness | 3 | 3 |
| Correctness | 3 | 5 |
| Structure | 5 | 4 |
| Clarity | 4 | 4 |
| Risk Coverage | 3 | 3 |
| Invariant and Edge Case Coverage | 4 | 4 |
| **Total (of 30)** | **22** | **23** |

## Edge-case floor check

Floor: a variant scoring below 1 of 5 on Invariant and Edge Case Coverage is ineligible as base.

| Variant | Score | Result |
|---|---|---|
| V1 OURS | 4 of 5 | Eligible |
| V2 CLAY | 4 of 5 | Eligible |

## Notes for the merge step (not scored)

- The one-point gap comes from Correctness: V1 has a verified citation swap, an overreaching Claim sentence and the X-001 contradiction; V2 has no verified false statement but over-weights unverified G2 facts and the parked #678.
- V1 alone covers the first-issue versus standing-rule divergence (its strongest unique content, confirmed by the debate, C-007). V2 alone covers the maximum-collection case (three workers at once).
- Both papers lack success criteria, an out-of-scope statement, graded risks with mitigations, and defined acronyms. Those gaps are shared and do not separate them.
- The 7 HIGH UNADDRESSED invariants in `invariant-probe.md` apply to the unified answer, not to the original papers, and are not scored here.
