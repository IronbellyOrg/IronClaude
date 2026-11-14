# Diff Analysis: owner-answer proposal Comparison (Q31)

## Metadata
- Generated: 2026-11-14T00:01:00Z
- Variants compared: 3 (Variant 1 = proposal-A.md, Variant 2 = proposal-B.md, Variant 3 = proposal-C.md)
- Total differences found: 16
- Categories: structural (2), content (7), contradictions (3), unique (4), shared assumptions (2 promoted)
- Context file (not a variant): `Q31/question.md`

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|------|---------------|---------------|---------------|----------|
| S-001 | Section set | Five brief sections (Answer, What happens next, Unlocks, Costs, Unresolved) | Same five | Same five | Low |
| S-002 | "What happens next" shape | One phase: record "no", no cron | Two phases: immediate "yes" for this program, then a separate contract PR | One phase with an operational sub-list (cron, expiry handling, silent reporting, limits) | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|-------|---------------|---------------|---------------|----------|
| C-001 | Does the 10-minute check apply to this coordinator | No; WC-16 loop only | Yes, read-only | Yes, read-only | High |
| C-002 | Where the rule lives | The checked-in worker contract only (WC-16 as written) | Memory and ledger now; then a PR adds it to the contract for every coordinator | Memory note and ledger row, this program only | High |
| C-003 | Supervision of non-worker peers (PR sessions of Q25, #539 author of Q33) | Only ad hoc subscriptions when a specific reason exists | Timer renews idle subscriptions | Timer renews idle subscriptions | Medium |
| C-004 | GitHub PR read frequency | At wave gates, before edits, at coordinator wakes | About every 10 minutes on two fork repos | About every 10 minutes on two fork repos | Medium |
| C-005 | Cron lifecycle (session-only, 7-day expiry) | Avoided entirely | Says a contract rule must address expiry and resume | Ledger records job id and expiry; re-created on expiry or resume | Medium |
| C-006 | How the check reports | Not applicable | Left unresolved | Silent unless a decision is needed (2026-11-09 order) | Low |
| C-007 | Whether a cron fire is a WC-16 "wake" that triggers the sweep pass | Question avoided | To be settled in the contract text | Named as UNVERIFIED; stays within the 5-minute cap | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) Position | Variant 2 (B) Position | Variant 3 (C) Position | Impact |
|---|-------------------|------------------------|------------------------|------------------------|--------|
| X-001 | Status of the cadence record's last row | "not in force for this program" | in force | in force | High |
| X-002 | Who the rule binds | this program (as "no") | every coordinator, via the contract | this program only | Medium |
| X-003 | Reading of WC-16 "Phase 1 adds this duty, not a scheduler" | Treats WC-16 as the complete cadence (implicit) | Treats the sentence as ambiguous, to be fixed at source | Treats it as not a ban on the owner's check (follows probe INV-010) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | 2 (B) | Promote the order into the checked-in contract so later coordinators inherit it without asking again | Medium |
| U-002 | 3 (C) | Record the cron job id and its 7-day expiry in the ledger and re-create it on expiry or resume | High |
| U-003 | 3 (C) | Routine "nothing changed" runs are silent per the 2026-11-09 order | Medium |
| U-004 | 1 (A) | Whole cadence auditable from one checked-in file; no expiry to manage | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All three treat the 2026-11-05 memory as the order being asked about | The order still reflects the owner's intent as of 2026-11-14 (the note is 9 days old; the 2026-11-09 order changed how such checks report) | UNSTATED | Yes |
| A-002 | B and C rely on a cron; A rejects it on cost grounds only | A session cron only fires while the coordinator session is idle (CronCreate: "Jobs only fire while the REPL is idle"), so a busy coordinator delays the check; none says so | UNSTATED | Yes |
| A-003 | All | The checks write nothing outward (gh reads, ListAgents, `notify_when_idle` without a message) | STATED (C) | No |
| A-004 | All | GitHub rate limits are not binding at 10-minute reads | STATED (C, as UNVERIFIED) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The order is still current | All variants cite it as standing | Medium: if stale, "yes" follows an outdated order and "no" overrides nothing | Open for debate |
| A-002 | Cron fires only when the session is idle | B, C build on the cron | Medium: the check is "about every 10 minutes" only while the coordinator waits; state assumption (L3) | Open for debate |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Diff points counted for convergence (S + C + X + A): 14
