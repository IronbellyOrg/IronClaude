## Anti-Omission Report

**Report reviewed:** `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Input files checked (Partition 2):** `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`
**Total findings enumerated:** about 125 (estimate; see Summary)
**Date:** 2026-11-07
**Method:** every distinct finding, rule, recommendation, open question and gaps row in the four files was enumerated; the report was searched by meaning (not by ID or citation) for each. Fix authorization: false (no file other than this one was edited).

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

### Omissions Found

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| 1 | Imported evidence is inert. Sanitize ESC/CSI/OSC, C0/C1 controls, carriage returns and bidi controls before any renderer (`PKG/PLAN.md:38`; implemented by `sanitize()` at `canvas.py:10-17`). The sweep copies untrusted text (`blocked_question`, transcript-derived text, Orca body text) into a Markdown file that a coordinator agent then reads. The report never states this rule: it is absent from the 3.1 report rules, the step 1.5 renderer and the step 1.12 report tests. | `scope-04-409-layout.md:219` | OMITTED | - | IMPORTANT (trust-boundary rule for the only write; arguably CRITICAL) |
| 2 | B-14 source field per column. Lifecycle comes from `projection.outcome` and `stage.detail`. Health comes from contract failed, and `unverifiable` maps to unknown. Freshness comes from `evidence.liveStatus` and `observedAt`, or the transcript mtime. Evidence is derived from `report_path` plus the existence of the artifacts. Phase and Admission are always "not observed", and Tests/review is null. Owner and Worktree have their own named sources. Step 1.5 reduces all of this to the bare citation "Column sources per scope-04:336-351", which does not count as coverage. The derivation rules that decide each cell are not in the report. | `scope-04-409-layout.md:334-351` | OMITTED | - | IMPORTANT |
| 3 | B-12 fallback sources for the question, requester, decision-owner and evidence cells, and the column set of the (a) explicit-questions table: ID / Age / Question / Requested by / Decision owner / Affected / Evidence. The report's (a) list and wide view drop the ID and Evidence columns. It never says which fallback source fills a cell when the primary one is absent. | `scope-04-409-layout.md:129`, `:311`, `:322-330` | OMITTED | - | IMPORTANT |
| 4 | Empty-state rule: "No matching records. This is not an all-clear." (`PKG/render.py:116`). The derived skeleton also places "This is not an all-clear." under the waiting / explicit-questions heading. In the report, "not an all-clear" appears only where 2.5 describes #409's Shift Brief. It is missing from the 3.1 skeleton, the step 1.5 fixed strings and the step 1.12 tests. When messages coverage is partial, an empty (a) list can be read as "nobody is waiting". | `scope-04-409-layout.md:225`, `:276` | OMITTED | - | IMPORTANT |
| 5 | "Source loss does not resolve questions, fail sessions, unlock a policy freeze or authorize retries" (`PKG/integration-gaps.md:24`). The report has "Seen is not resolved", the Orca-unavailable banner and the `unscanned:` markers. It never states that a lost or unavailable source cannot resolve a question, fail a session, lift a freeze or justify a retry. SC-7 and step 1.12 drop items absent from their source, and they do not separate "read the source and the item is absent" from "lost the source". | `scope-04-409-layout.md:101`, `:221` | OMITTED | - | IMPORTANT |
| 6 | "Workspace co-location alone is not ownership" (`PKG/integration-gaps.md:12`). The sweep maps sessions to worktrees by path, and the report never warns that sharing a workspace path does not prove a session owns the worktree or its work. | `scope-04-409-layout.md:222` | OMITTED | - | IMPORTANT |
| 7 | A peer row's ownership is unknown unless it carries `linked: true`, so a peer must never be attributed by workspace membership. The report says peers appear only in `worktree ps` and `reference find`, but it never gives the attribution rule. Without it, an unlinked peer session would be credited to whatever worktree its path falls in. Closely related to row 6, but it comes from a separate Orca-schema source and adds a concrete field test. | `06-orca-open-questions.md:99`, `:110` | OMITTED | - | IMPORTANT |
| 8 | `worktree ps` reports some hosts as "not covered". For those hosts the sweep must print "could not determine", never "no sessions". `worktree ps` is also paged by a shared `--limit`, so a truncated page under-reports sessions. The report calls `worktree ps --json` but states neither rule. | `06-orca-open-questions.md:97`, `:109` | OMITTED | - | IMPORTANT |
| 9 | "The sweep must not propose stop/abandon/retry/release; those need positive proof and are coordinator decisions." Steps 1.15 and 1.17 have the sweep recommend the `:74`/`:107`/WC-6 actions. The report names only the conflict with #409 rule 5 and never records this source position against the sweep proposing those actions. | `06-orca-open-questions.md:138` | OMITTED | - | IMPORTANT |
| 10 | "Global counts must name scope and collection completeness; a selected filter must state its denominator" (`PKG/integration-gaps.md:24`). The report's header prints the source list and the scope line, but the `--run` and time-window filters print no denominator. A filtered count such as "3 waiting" therefore cannot be told apart from a fleet-wide count. | `scope-04-409-layout.md:67` | OMITTED | - | IMPORTANT |
| 11 | Affected counts are a set union: "Distinct affected sessions: N (set union, not a sum)". | `scope-04-409-layout.md:194`, `:217`, `:283` | OMITTED | - | MINOR (sweep rows are per session, so double counting is unlikely in Phase 1) |
| 12 | Meaning is carried in words, not color, and stale or frozen states must not use failure semantics. | `scope-04-409-layout.md:220` | OMITTED | - | MINOR (the report output is plain Markdown) |
| 13 | Events are deduplicated by id, the latest seq is kept, and they are shown in seq order. | `scope-04-409-layout.md:174`, `:227` | OMITTED | - | MINOR (Phase 1 reads no event stream) |
| 14 | Do not clip IDs in a static report. | `scope-04-409-layout.md:245` | OMITTED | - | MINOR |
| 15 | The footer line "Source coverage is not fleet-wide assurance", and "Dirty is not dangerous. Shared paths are not a proven conflict" under Worktrees. | `scope-04-409-layout.md:74`, `:300`, `:307` | COVERED-BY-DEDUP (dirty/overlap part only); footer part OMITTED | Report 2.5, rule 3 (dirty/overlap is not a conflict) | MINOR (footer part) |
| 16 | Scope-line detail: current sessions only, with historical ones counted separately; inventory worktrees vs mapped worktrees; a count of unmapped sessions. | `scope-04-409-layout.md:60-61`, `:272` | OMITTED | - | MINOR |
| 17 | Join on stable IDs, never on joins inferred from display names (`PKG/PLAN.md:33`). | `scope-04-409-layout.md:218` | OMITTED | - | MINOR |
| 18 | Request age is labelled "oldest observed" when messages coverage is incomplete, and a gap in the timeline is missing observation, not idle time. | `scope-04-409-layout.md:194` | OMITTED | - | MINOR |
| 19 | The "Not registries" list: `/sc:help` reads the command tree live; the install test checks only 4 commands; sync-dev uses globs; plugin command mirrors are required only for help, recommend, workflow and implement. This tells the implementer which places need no edit when a new command is added. | `scope-03-cli-patterns.md:159-164` | OMITTED | - | MINOR |
| 20 | Heavy imports are deferred inside each command body (the CLI start-up convention). | `scope-03-cli-patterns.md:74` | OMITTED | - | MINOR |
| 21 | `_ORCA_NAME_RE` bans naming an Orca command inside an Unattended section. | `scope-03-cli-patterns.md:156` | COVERED-BY-DEDUP | Step 1.14 ("No ## Unattended mode section"): with no Unattended section, the regex can never fire | MINOR |
| 22 | `--peek` hides questions that were already read; only `--all` could show read-but-unanswered ones. | `06-orca-open-questions.md:74` | OMITTED | - | MINOR (`check` is forbidden by default in Phase 1) |
| 23 | Caller identity: passing another session's handle acts on that session's mailbox, so a peek must use the coordinator's own identity. The report's S9 row 78 says only "Same as GQ-53". | `06-orca-open-questions.md:67` | OMITTED | - | MINOR |
| 24 | Line 28 of integration-gaps, "locate a frozen worktree", is a walkthrough step that has never been tested. | `06-orca-open-questions.md:139` | OMITTED | - | MINOR |
| 25 | "Treat unknown optional fields as absent; absence never authorizes action" (from the guide). | `05-orca-row-schema.md:65`, `:77` | COVERED-BY-DEDUP | Report 4.4 GQ-15 row (unknown field = could not determine) and the WC-10 rules | MINOR |

### Summary

- **Findings enumerated:** about 125 (scope-03 about 30, scope-04 about 50, 05 about 15, 06 about 30). This is an estimate: some source lines bundle several rules, and those were counted as one finding each.
- **Represented:** about 100 (see the method line; the represented findings are not tabulated, by format).
- **Covered by dedup:** 3 (rows 15 dirty/overlap part, 21, 25).
- **Omitted, blocking:** 10 (0 CRITICAL, 10 IMPORTANT: rows 1-10).
- **Omitted, MINOR:** 13 (rows 11-14, 15 footer part, 16-20, 22-24).

The blocking omissions cluster in two areas:

- **Rendering-trust rules from #409 that the sweep's renderer does not carry over:** rows 1-5 and 10. These are the sanitize rule, the per-column derivation, the (a) table columns, the not-an-all-clear empty state, the source-loss rule and filter denominators.
- **Orca attribution and coverage limits:** rows 6-9. These are co-location vs ownership, peer `linked: true`, `worktree ps` "not covered" and paging, and the ban on the sweep proposing stop/abandon/retry/release.

Row 1 is the strongest candidate for promotion to CRITICAL when the partition reports are merged.

Verdict: FAIL
