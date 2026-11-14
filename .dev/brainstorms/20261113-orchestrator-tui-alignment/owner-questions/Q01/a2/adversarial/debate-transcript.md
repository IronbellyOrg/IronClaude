# Adversarial Debate Transcript: Q1 (a2) fix shape and (b) channel scope

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% (13 of 13 points reached at least a 2-of-3 majority)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned in parallel as sub-agents (general-purpose type): Variant 1 persona security, Variant 2 architect, Variant 3 qa. No failures. Advocates were told part (a) is answered "fix" and never to specify the code.
- Variant map: Variant 1 = proposal-A (F2 refuse and report, fail closed); Variant 2 = proposal-B (author and owner pick F1 or F2 at implementation); Variant 3 = proposal-C (combination: neutralise by default, refuse where neutralising could change the answer).

## Round 1: Advocate Statements

Full statements are kept once in their own files: `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round1-advocate-V3.md`.

### Variant 1 Advocate (security)
Refusing fails in a visible way (too many `unscanned`) or leaks; the combination adds two more failure ways (a neutralisation that does not hold, an altered result shown as a normal scan). Concedes: its claim to cover "a channel nobody listed" is an overclaim (a rule can refuse only what it detects); it gives up git facts for fsmonitor-only worktrees with no security gain; Variant 3's two-sided test is better; it rests on the same decidability assumption; its environment rule is under-specified. Neutral recommendation: **Variant 1, amended, 60 percent**.

### Variant 2 Advocate (architect)
The outcome should be the owner's and the mechanism the author's. Concedes: as written it fails a gating criterion: SW-01 (1) requires "A dated owner ruling names F1, F2 or F3" (`merged-requirements.md:190`), the dependency table says "The ruling is the owner's" (`:648`), and ADJ line 206 says "The owner chooses (Q1)"; the #539 author is unnamed (Q33); no tool may design the fix. Neutral recommendation: **Variant 1, amended, about 60 percent**, with Variant 2's duty to name excluded channels and record the reason in the PR.

### Variant 3 Advocate (qa)
The only shape whose test catches both failures (a program runs; a silently wrong scan). Concedes: "could change the answer" is harder to decide than "could run"; on filters it gives the same result as Variant 1 (a selected filter is both where it could run and where disabling changes the answer), so the real difference shrinks to fsmonitor-only worktrees, a benefit that is unmeasured; two behaviours cost more inside a 1003-file PR; it has the same unlisted-channel detection problem; the spec offered F1 or F2, not a combination. Neutral recommendation: **Variant 1, amended, 60 percent**.

### Shared-assumption responses (omission check: none omitted)

| Point | V1 advocate | V2 advocate | V3 advocate |
|---|---|---|---|
| A-001 ("could run" / "could change the answer" decidable) | QUALIFY | QUALIFY | QUALIFY |
| A-002 (git-status scope kept separate from the other reads) | ACCEPT | ACCEPT (as a required addition) | ACCEPT |

Agreed: "could run for this worktree" is plausibly decidable for the named channels from the configuration git actually reads (all scopes and included files) and the worktree's attributes; whether every attribute source can be judged without git's own machinery is UNVERIFIED; when the check cannot tell, the safe reading is refuse and report. "Could change the answer" is the harder, unmeasured judgement. A-002 must be stated in the ruling whichever shape wins (SW-02 (2), INV-039).

### Amendments all three advocates proposed for the winner
1. Drop the claim that refusal covers channels nobody listed; instead state the outcome, the named channels, and the channels deliberately left out; anything the check cannot classify is refused and reported.
2. Adopt the two-sided regression test: it fails if any in-scope program runs, and fails if a worktree that should be refused is scanned.
3. State how an inherited-environment setting counts: only when it names a program `git status` could run (the session's `credential.*` keys do not).
4. State the separation of the git-status scope from the contract allow-list and transcript scans.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | none (identical) | 90% | Identical structure; agreed. |
| C-001 | L2 | Variant 1 (tied with Variant 3) | 85% | 3 of 3, V2 advocate conceded: SW-01 (1) and the owner's update require the owner to name the shape. |
| C-002 | L3 | Variant 1 | 62% | 2 of 3: withholding a result fails visibly; neutralising fails silently when a key is missed. |
| C-003 | L3 | Variant 2 | 62% | 2 of 3: no shape can detect an unknown channel; naming what is left out (SW-01 (4)) is the only auditable promise. |
| C-004 | L3 | Variant 1 | 65% | 2 of 3: the "could run for this worktree" rule turns both host facts into a testable rule. |
| C-005 | L2 | Variant 3 | 82% | 3 of 3: the two-sided test catches a running program and a silently altered result. |
| C-006 | L2 | Variant 1 | 75% | 3 of 3: one behaviour to build and review in a 1003-file PR. |
| X-001 | L3 | Variant 2 (tied with Variant 3) | 70% | 2 of 3, V1 advocate conceded: Variant 1's unlisted-channel claim contradicts its own detection-based rule. |
| X-002 | L2 | Variant 1 (tied with Variant 3) | 85% | 3 of 3, V2 advocate conceded: the record makes the shape the owner's (`merged-requirements.md:190`, `:648`; ADJ line 206). |
| X-003 | L3 | Variant 1 | 65% | 3 of 3: F2 refuses everything on this host only under a literal "defines it" rule; Variant 1 states the narrower rule. |
| A-001 | L3 | Variant 1 | 62% | 3 of 3: "could run" is the narrower, more checkable question. |
| A-002 | L2 | none (all omit; must be added) | 85% | 3 of 3 ACCEPT. |

Points won: Variant 1: 7 (C-001, C-002, C-004, C-006, X-002, X-003, A-001; two tied with Variant 3); Variant 2: 2 (C-003, X-001); Variant 3: 1 (C-005) plus two ties.

## Convergence Assessment
- Points resolved: 13 of 13 (12 scored points above plus S-001)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-001, C-005, C-006, X-002, A-002), L3 (C-002, C-003, C-004, X-001, X-003, A-001): all covered.
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick).
- Status: CONVERGED
- Unresolved points: none
- Overall neutral recommendation: Variant 1 (F2 with the "could run for this worktree" rule), 3 of 3, 60 percent each, with the four amendments above. Variant 3 is the named runner-up if a later count shows many fsmonitor-only worktrees whose git facts would be lost.
