# Diff Analysis: D13 position papers comparison

## Metadata
- Generated: 2026-11-20
- Variants compared: 2 (variant-1 = OURS, variant-2 = CLAY; both `*-original.md` copies of the position papers)
- Total differences found: 17
- Categories: structural (2), content (6), contradictions (2), unique (5), shared assumptions (4 promoted: 3 UNSTATED, 1 STATED)

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Heading set | Claim, Mechanism, Cited facts (9), Costs, Risks, Gets right | Same six headings, 9 cited facts | Low |
| S-002 | Mechanism section | Argues about duties and who owns them (role view) | Describes how the three tools work (tool view) | Medium |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|-------|---------------------------|---------------------------|----------|
| C-001 | Relation of the three pieces to issue 339 | Read them under 339's scope; one coordinator role owns sweep, close, cleanup | Complementary tools; each fills a gap 339 lists; keep separate | Medium |
| C-002 | Who performs worktree and branch removal | The coordinator role (owner comment 2026-11-05) | A script run by an opt-in automation with no agent; the orchestrator never removes (design line 628, issue 687) | High |
| C-003 | Meaning of the 16-workspace incident (issue 687, two open issues #354, #419) | A risk of letting the coordinator delete | The reason for the nine mechanical rules | Medium |
| C-004 | Owner approval on record | None by `ironbelly` on 655, 668, 681 to 684, 686, 687; closeout spec says "owner approved" | Closeout spec and PR body say owner approved the spec and adoption; no approval of cleanup on record | Low |
| C-005 | Hourly sweep | `/sc:sweep` (PR 539) built; WC-16 runs it each wake | No Clay piece repeats it; `/sc:sweep` is read-only | Low (agreement) |
| C-006 | PR log (PR 670) | No 339 duty overlaps it | Same; merged by the owner | Low (agreement) |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is worktree and branch cleanup a coordinator responsibility? | Owner comment 2026-11-05 on issue 339: "part of this roles responsibilities ... extra rigid and strict validation" (OURS fact 2) | `docs/designs/orchestrator.md` line 628 and issue 687: removal "is not done by the orchestrator"; line 139: deleting branches is human-only (CLAY facts 6, 8) | High |
| X-002 | Are Clay's pieces separate duties or part of 339's scope? | "must be read under 339's scope, not as a separate duty set" | "complementary, not duplicates ... keep all three" | Medium (largely wording: both agree none is a duplicate of another) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | OURS | Owner 2026-11-05 comment: orchestrator keeps polling until sessions are finished, cleanup commenced and session closed | High |
| U-002 | OURS | WC-16 in `WORKER-CONTRACT.md` runs `/sc:sweep` on every coordinator wake, so the hourly duty has a built home | Medium |
| U-003 | CLAY | Issue 687 reuses closeout's `branch-landed.sh`, so both tools share one truth check | High |
| U-004 | CLAY | Issue 687's nine rules, evidence repo save, never `--force`, never `git branch -D`: the "rigid and strict validation" the owner asked for | High |
| U-005 | CLAY | PR 683 evidence: 22864 passed, 2 environment failures; closeout is never-as-worker (`WORKER-CONTRACT.md` line 23) so it is coordinator or person only | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | "The orchestrator" of Clay's design, the "orchestrator" of issue 339 and the "coordinator" of `WORKER-CONTRACT.md` are the same role | Both papers use the words for one role | UNSTATED | High: X-001 may be a naming mismatch, not a conflict | Promoted |
| A-002 | A script run by an automation with no agent is not "the orchestrator removing a worktree" | CLAY states it; OURS never engages it | UNSTATED | High: decides whether X-001 can be satisfied by both | Promoted |
| A-003 | A coordinator running closeout writes (close issue, note, Orca task) is allowed under the contract's rule that the coordinator performs outward actions only when the user's instruction names that action (`WORKER-CONTRACT.md` section 4, Git and GitHub ownership) | Both treat closeout as a coordinator step | UNSTATED | High: adoption needs a grant row; H-design681-map.md row 2 lists the merge and close authority as a conflict | Promoted |
| A-004 | Issue 687 is a design only (nothing built; spec items marked proved-first) | Both papers say "issue" and "not built" | STATED | Medium | Not promoted |

## Summary
- Total structural differences: 2
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-002, X-001, A-001, A-002, A-003
