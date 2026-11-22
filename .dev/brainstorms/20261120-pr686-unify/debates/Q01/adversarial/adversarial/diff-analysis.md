# Diff Analysis: position-paper Comparison (Q01, who writes a per-issue grant row)

## Metadata
- Generated: 2026-11-20
- Variants compared: 2 (Variant 1 = OURS, `variant-1-original.md`; Variant 2 = CLAY, `variant-2-original.md`)
- Total differences found: 14
- Categories: structural (3), content (6), contradictions (2), unique (8), shared assumptions (3)

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|------|------------------|------------------|----------|-------|
| S-001 | Section skeleton | Abbreviations, Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right (6 H2) | Same six H2 headings | Low | L1 |
| S-002 | Mechanism format | 3 numbered steps of a human process (owner says go, agent records, invented rows refused) | 4 numbered enforcement components (standing list, refusal verb, answer gate, answer-check test) | Medium | L2 |
| S-003 | Cited-fact count and order | 9 facts, owner records first, then master text, then precedent | 8 facts, design lines first, then owner rule and D04/D13 | Low | L1 |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity | Level |
|---|-------|---------------------------|---------------------------|----------|-------|
| C-001 | Who creates the record | The agent in the owner's session records the row from the owner's chat go, quoting the words and date | No row exists; a typed answer is accepted by a script (`answer-check`) and the action log keeps it | High | L2 |
| C-002 | Unit of consent | One row per issue, naming the writes; bulk standing grants for merge and close refused | A standing `grants` list of six entries, incl. `pr.merge` and `issue.close` | High | L2 |
| C-003 | Check on the source of the go | None in code today; rests on the "executor-invented approval" rule and the agent's honesty | Source test, entry test, freshness test, question key (D:694), but only designed (PR B not built) | Medium | L3 |
| C-004 | What master contains today | Master has no per-issue row writer or checker; line 241 already makes a chat instruction the route for outward actions; line 57 still says "written by the owner" | Master has no per-issue row writer or checker (PR 682); line 57 still says "written by the owner" | Low (agreement) | L2 |
| C-005 | Treatment of `pr.merge` and `issue.close` | Never standing; needs a per-action chat go | On the standing list; cost section admits D04 rejected this | Medium | L2 |
| C-006 | Fail-closed and refusal in code | Not covered | Missing `grants` reads as empty (`repos.py:295`); `E-NO-GRANT` refuses and logs; covers at most 2 of 6 entries | Medium | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------|-------|
| X-001 | Does the owner write the row? | Claim: the owner is never asked to write a file (fact 2). Fact 3 and fact 1: `WORKER-CONTRACT.md:57` and Decision 8 say the row is "written by the owner". The paper lists this as a risk but does not rule on it (intra-variant) | Claim: no row is written by any person; fact 7 notes line 57 still says owner-written but treats it as irrelevant to its design | High | L2 |
| X-002 | Is a check on a typed chat answer unique to Clay's design? | Fact 6: the Ruling-line rule (`qa.md:248-249`) already accepts only "clear user confirmation" and refuses "executor-invented approval" | Gets-right section: "the only design with a check on a typed chat answer" | Medium | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Provenance of line 57: the owner said only "narrow d2"; the grant-row sentence came from the fix agent's reading of Decision 8 (PR 585 body) | High |
| U-002 | 1 | Master line 241 already makes the user's named instruction, possibly in the live conversation, the route for every outward action | High |
| U-003 | 1 | `issue-pipeline-fu1.md:106` pairs a live-test grant row (line 24) with "the owner never has to write a file" | Medium |
| U-004 | 2 | `answer-check` mechanics: source, entry, freshness, question key `merge_safety:<PR>:<head sha>` | High |
| U-005 | 2 | `E-NO-GRANT` refusal with a log of each grant used | Medium |
| U-006 | 2 | Fail-closed default for a missing `grants` key (`repos.py:295` in PR 686 head) | Medium |
| U-007 | 2 | Unknown U37: any agent with the Orca CLI can type into a terminal, so "typed by a person" is not provable | Medium |
| U-008 | 2 | The `grants` file lies inside the orchestrator's own write reach and is guarded only by a verb and a test (D:688) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status | Level |
|-------|------------|------------------|----------------|--------|--------|-------|
| A-001 | The owner's 2026-11-17 chat-only rule (memory) is the controlling statement of owner intent about mechanics, and the later "narrow d2" instruction (04:46, same day, timezone unverified) did not restore an owner-written row | Both cite the memory rule as the owner's order and neither orders the two statements in time or settles which one the owner meant | UNSTATED | High | Promoted | L2 |
| A-002 | A per-issue grant row is still a live thing to rule on after PR 682 removed its only writer and checker and D04 moved the old row's writes to standing grants | Both discuss "the row" although both note master has no code that reads one (OURS fact 7, CLAY fact 5) | UNSTATED | High | Promoted | L2 |
| A-003 | A recorded go has an expiry and a revocation path (what ends it, who can void it) | Both describe how a go is created; neither says how it ends. The old design had a "lifetime and revocation" column (merged-spec 6.8) that neither paper cites | UNSTATED | Medium | Promoted | L3 |

(Other shared assumptions checked and classed STATED, not promoted: the shared `ironbelly` login means a chat message does not prove its typist, stated in OURS "What it risks" and CLAY "What it risks" via U37.)

## Summary
- Total structural differences: 3
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 1 not promoted, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001, A-001, A-002
- Taxonomy counts for the debate (diff points S+C+X+A = 14): L1: S-001, S-003 (2); L2: S-002, C-001, C-002, C-004, C-005, X-001, A-001, A-002 (8); L3: C-003, C-006, X-002, A-003 (4)
