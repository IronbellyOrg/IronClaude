# Diff Analysis: owner-answer proposals for Q1 (INV-008, the git-config hole)

## Metadata
- Generated: 2026-11-14 (Step 1, sc-adversarial-protocol Mode A, depth quick)
- Variants compared: 3 (variant-1 = proposal-A "accept now, fix later with a trigger"; variant-2 = proposal-B "fix before merge"; variant-3 = proposal-C "accept with caveats, no code change")
- Total differences found: 17
- Categories: structural (1), content (6), contradictions (3), unique (5), shared assumptions (3 promoted)
- Context file for all advocates: `../question.md` (facts and sources)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set and order | Answer; What happens next; Unlocks; Costs or risks; Unresolved | same five sections, same order | same five sections, same order | Low (identical by design of the brief) |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | When the hole is closed relative to the #539 merge | After merge, in a follow-up PR, before a named trigger | Before merge, inside #539 | Never (accepted) | High |
| C-002 | "Read-only" claims (at least 16 locations, INV-011) | Caveat all now, remove caveats later | No caveat needed; claims become true | Caveat all, permanently | Medium |
| C-003 | The one real-id comparison lane (XC-04), which must never run the unfixed sweep | Waits for the follow-up fix (variant concedes) | Runs on master once the sweep is runnable | Blocked unless a later fix or an owner exception the spec does not provide | High |
| C-004 | Premise the ruling relies on (SW-01 (2)) | Single owner, single host, sessions already run permission-free (ADJ E-11) | Not stated; states the allow-list edit is authorised for this purpose only | Same as variant 1, plus "a clone cannot ship config; .gitattributes alone ran nothing" | Medium |
| C-005 | Reversibility | Acceptance reversible only before merge; fix later | A fix is reversible (SW-01 undo column) | Acceptance reversible only before merge; reversing after merge needs a new fix PR | Medium |
| C-006 | Part (b) channel scope | All measured channels, in both the acceptance and the follow-up | All channels, and the ruling names any it leaves out | All channels named as accepted, so nothing is accepted by silence | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Which answer reaches downstream work fastest | "Everything behind the merge ... can start sooner" (Unlocks) | "The one real-id comparison (XC-04) can run on master code as soon as the sweep is runnable" (Unlocks) | "The shortest path to merging #539" (Unlocks) | Medium: depends on whether the slowest lane (XC-04) or the merge itself is the bottleneck |
| X-002 | Whether the hole is acceptable on this setup | Acceptable temporarily, under a trigger | Not acceptable; the claims must be made true | Acceptable; "matches the measured severity: Medium in practice" | High: the core owner choice |
| X-003 | Whether the sweep adds privilege | Implies a temporary exposure worth tracking | Implies a real exposure worth closing | "The sweep grants no privilege a session does not already have", yet lists that anything able to write host git config can make every sweep run a program in every listed worktree | Medium: variant 3's own risk section qualifies its premise |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | A named trigger list for the follow-up fix: before XC-04, before any unattended or scheduled sweep, before a second user or host | High |
| U-002 | 1 | The fix gets its own focused review instead of riding in a 1003-file PR (ADJ E-08) | Medium |
| U-003 | 2 | The git-status scope is separated from the contract allow-list and transcript scans (INV-039), and the regression test reproduces the 2026-11-13 probe | High |
| U-004 | 3 | The acceptance records its own void conditions (second user, second host, untrusted config) in the ledger | Medium |
| U-005 | 2 | "Names any channel it deliberately leaves out", making an unlisted channel visible | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-006 (all cover the same channel list) | The channels measured on 2026-11-13 (fsmonitor, clean and process filters, include.path/includeIf, per-worktree config, GIT_CONFIG_* variables) are the complete set by which `git status` can start a program | UNSTATED | Yes |
| A-002 | All "What happens next" sections | The #539 author exists and acts, and the owner (or a grantee) posts the ruling on the Codex thread; Q33 (who the #539 author is) is unanswered | UNSTATED | Yes |
| A-003 | X-003, C-004 | The sweep's `git status` is the marginal exposure: no other routine process on this host already runs `git status` (with the same config) in the same worktrees, so fixing or accepting it changes the real risk | UNSTATED | Yes |
| A-004 | C-004 (variants 1 and 3) | Single owner, single OS user, single host holds for the lifetime of the decision | STATED (variants 1 and 3) | No |
| A-005 | Variant 2 Unresolved | git versions other than 2.47.3 behave the same | STATED (variant 2) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The measured channel list is complete | C-006 | A fix built from the list could miss a channel; an acceptance built from it could accept less than the real exposure (L3, guard) | UNSTATED |
| A-002 | The #539 author and the ruling poster are available | all next-step sections | Every option stalls until Q33 is answered (L2, dependency) | UNSTATED |
| A-003 | The sweep is the marginal exposure | X-003 | If other sessions already run `git status` in the same worktrees with the same config (UNVERIFIED; the Claude Code harness reports a git status at session start), the fix narrows the sweep's own claim but not the host's exposure (L3, boundary) | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, X-002
- Taxonomy levels: L1 (S-001, C-006), L2 (C-001, C-002, C-004, C-005, X-001, A-002), L3 (C-003, X-002, X-003, A-001, A-003)
- Similarity check: differences are well above 10 percent; debate proceeds.
