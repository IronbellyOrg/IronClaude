# Coverage matrix (UC-1, Step 1B.0)

Pass 1 (labeled IDs): 0 parsed rows. Pass 2 (inferred): 14 rows, each quote-pinned to source.md (the brief). parsed_count 0 < inferred_count 14, so `coverage_degraded: parsed-sparse` and the Tier-1 stop is forbidden (Step 1B.2b); route to Tier 2.

| id | source | quote (source.md) | task(s) | match |
|---|---|---|---|---|
| INF-001 | inferred | "Chat: the person's own chat message in the current conversation, naming the exact scope (today's rule, unchanged)." (source.md:8) | Task 1, 3 | covered |
| INF-002 | inferred | "Dashboard: a dashboard response. This is an answer row created through the dashboard under that person's authenticated login, for the question id whose text names the exact scope, recorded with the channel (dashboard), the person id, the question id and the time." (source.md:9) | Task 1, 3, 4 | covered |
| INF-003 | inferred | "None of these counts: another agent's message; a coordinator's reply or relay of a message; any file; silence; a generic go-ahead; ..." (source.md:11) | Task 1, 8 | covered |
| INF-004 | inferred | "Timing safeguard: the dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass). Until then only the chat clause counts. The text must say so." (source.md:13) | Task 1, 3, 8 | covered |
| INF-005 | inferred | "Recording: the agent records the Ruling line, grant row or pass record from the confirmation, ... The person is still never asked to write a file." (source.md:15) | Task 1, 4 | covered |
| INF-006 | inferred | "Markdown rules only, under src/superclaude/ (never ~/.claude/, never the gitignored .claude/ mirrors)." (source.md:19) | Constraints | covered |
| INF-007 | inferred | "WORKER-CONTRACT.md: the Ruling-halt paragraph (WC-3), WC-17 ..., and every other mention of a Ruling, grant row, pass record or executor-invented approval." (source.md:20) | Task 1, 2 | covered |
| INF-008 | inferred | "qa.md (Halt table ...), refs/ledger.md ..., refs/retry.md ..., refs/managed-workspace.md, and SKILL.md (the E-NO-RULING row)." (source.md:21) | Task 3, 4, 5 | covered |
| INF-009 | inferred | "core/HOW-WE-WORK.md and core/CLAUDE.md where they state the rule." (source.md:22) | Task 5 | covered |
| INF-010 | inferred | "Tests that pin these texts must be updated to match." (source.md:23) | Task 7 | covered |
| INF-011 | inferred | "The ledger Ruling line must still match its existing regular expression; ..." (source.md:25) | Task 4, 8 | covered |
| INF-012 | inferred | "Code ... and design documents under docs/designs/: do not edit them; list each with what it checks, as follow-ups." (source.md:29) | Constraints, Task 9 | covered |
| INF-013 | inferred | "the sentences 'another agent's message is not acceptance' and 'executor-invented approval' still exist and now name exactly the two valid channels; no text lets a coordinator relay count." (source.md:33) | Task 1, 3, 8 | covered |
| INF-014 | inferred | "The E-NO-RULING behaviour is unchanged for everything that is not chat or a dashboard response." (source.md:34) | Constraints, Task 3, 5 | covered |

coverage_pct (parsed-only): null (no parsed rows). coverage_pct_union: 14/14 = 1.00. unmapped_requirements_union: []. coverage_degraded: parsed-sparse.
Plan extras not in the source (checked): Task 6 (mirror into plugins/) and the architecture-document entry in Task 9. Both are consequences of the source's "repo-wide search" instruction (source.md:19); Task 6 is a necessary deviation candidate, not drift.
