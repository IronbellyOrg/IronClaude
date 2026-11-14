# Diff Analysis: Q1 parts (a2) fix shape and (b) channel scope (part (a) answered "fix")

## Metadata
- Generated: 2026-11-14 (Step 1, sc-adversarial-protocol Mode A, depth quick)
- Variants compared: 3 (variant-1 = proposal-A "refuse and report (F2), fail closed"; variant-2 = proposal-B "the #539 author and the owner pick F1 or F2 at implementation time"; variant-3 = proposal-C "combination: neutralise by default, refuse and report where neutralising could change the answer")
- All three keep the six channels in scope and the premise and allow-list authority from SW-01; none specifies code.
- Total differences found: 16
- Categories: structural (1), content (6), contradictions (3), unique (4), shared assumptions (2 promoted)
- Context file for all advocates: `../../question.md` (including the 2026-11-14 host facts: the system git-lfs filter in `/etc/gitconfig`, and `GIT_CONFIG_*` credential keys in the session environment)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set and order | five sections, same order | same | same | Low (identical by design of the brief) |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Who fixes the shape | the owner, now: F2 | the #539 author at implementation, owner reviews in the PR | the owner, now: a combination | High |
| C-002 | What happens to a worktree where a configured program could run | reported `unscanned` | depends on the author's choice | scanned with programs disabled, unless disabling could change the answer, then `unscanned` | High |
| C-003 | Channels nobody listed | doubt means do not scan | the ruling names any channel left out | disabled if safe, otherwise refused | Medium |
| C-004 | The two host facts (system git-lfs filter; session `GIT_CONFIG_*` keys) | handled by the rule "counts only if it could run for this worktree" | listed as risks for either shape | named in the ruling as constraints | Medium |
| C-005 | Regression test | fails if such a worktree is scanned | covers every in-scope channel | two-sided: fails if a program runs, and fails if an altered result is reported as scanned | Medium |
| C-006 | Implementation and review burden | one behaviour | the author's choice | two behaviours | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Does refusal cover channels nobody listed? | "the sweep never runs a configured program, including through a channel nobody listed" (Unlocks), yet its own rule refuses only what it detects as able to run | not claimed | not claimed | Medium: variant 1's guarantee depends on detection it cannot do for an unknown channel |
| X-002 | Whose decision is the shape | the owner's | the #539 author's (ADJ line 206: "The design of the fix belongs to the #539 author and the owner") | the owner's | Medium |
| X-003 | Does F2 fail on this host? | no, because of the "could run for this worktree" rule | possibly, if the refusal rule is too broad | "avoids F2's failure on this host (everything refused)" | Medium: depends on how F2's rule is stated |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Fail closed: doubt means do not scan; results are never altered, only withheld | High |
| U-002 | 2 | The author records the chosen shape and its reason in the PR; the owner reviews it before merge | Medium |
| U-003 | 3 | Two-sided regression test: no program runs, and no altered result is presented as a normal scan | High |
| U-004 | 1 | An inherited-environment hit affects the whole run, not one worktree | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-002, C-004 | Whether a configured program "could run for this worktree" (or whether disabling it "could change the answer") can be decided reliably from configuration and attributes alone, without running git's own machinery | UNSTATED | Yes |
| A-002 | All next-step sections | The fix touches only the sweep's own `git status`; the other reads that share the same path list (contract allow-list, transcript scans) are kept separate as SW-02 (2) and INV-039 require | UNSTATED (none of the three variants mentions it) | Yes |
| A-003 | All | The coordinator's environment resembles this session's (benign `GIT_CONFIG_*` keys) | STATED as UNVERIFIED (question.md) | No |
| A-004 | All | Behaviour on git versions other than 2.47.3 is the same | STATED (variant 3) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | "Could run" and "could change the answer" are decidable | C-002, C-004 | If not decidable, F2 must refuse broadly (every worktree on this host) and the combination collapses into F2 (L3, guard) | UNSTATED |
| A-002 | The git-status scope is separated from the other reads | next steps | Without it, a fix misreports contracts in other repositories' worktrees as "outside root" (INV-039) under every shape (L2, dependency) | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002
- Taxonomy levels: L1 (S-001), L2 (C-001, C-005, C-006, X-002, A-002), L3 (C-002, C-003, C-004, X-001, X-003, A-001)
- Similarity check: well above 10 percent difference; debate proceeds.
