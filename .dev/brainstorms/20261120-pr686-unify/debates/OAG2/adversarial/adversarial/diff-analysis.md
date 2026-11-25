# Diff Analysis: OAG2 position paper comparison (OURS vs CLAY)

## Metadata

- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (Variant 1 = OURS position paper, 996 words; Variant 2 = CLAY position paper, 865 words)
- Mode: A (compare), depth quick, unattended
- Topic: OAG2, sub-questions OA-9 (where the sweep JSON lives), OA-17a (observer shows entry text?), OA-17b (questions panel exception?)
- Total differences found: 19 diff points in the convergence denominator (structural 2, content 11, contradictions 2, shared assumptions 4) plus 8 unique contributions (not in the denominator)
- Taxonomy level counts (denominator points): L1 = 3, L2 = 8, L3 = 7 (see the Level column)

## Structural Differences

| # | Area | V1 (OURS) | V2 (CLAY) | Severity | Level |
|---|---|---|---|---|---|
| S-001 | Order of cited facts | Facts follow the sub-questions (OA-9 first, then 17a, then 17b) | Facts follow argument strength (window dependence first), sub-questions mixed | Low | L1 (presentation) |
| S-002 | Framing disclaimer | None; states the owner's line as the recorded default | Opens with "Clay posted no text on OA-9 or OA-17 (UNVERIFIED that they hold these views)" and names the alternative as the TOPICS.md alternative | Medium | L1 (wording of attribution) |

## Content Differences

| # | Topic | V1 (OURS) approach | V2 (CLAY) approach | Severity | Level |
|---|---|---|---|---|---|
| C-001 | OA-9: does a sweep JSON file exist beside the report | Yes, `<UTC>-sweep.json`, one file for every reader | No file; each reader gets its own collection | High | L2 (component, file layout) |
| C-002 | What the observer does under the no-file option | Cannot run a sweep per cycle (90 s cap `probes.py:130` vs 15 s cycle `collector.py:28-29`), so a file is the only way to give it sweep classes | Same numbers; the observer keeps its own worker-list read and loses the eight classes, so screen and report may show different class words | Medium | L2 (interface) |
| C-003 | Window dependence of the classes (`classify.py:303-324`, `:922`) | A risk; mitigation: the report runs `sweep run --window` itself, which also saves a file | The main argument against one shared file: a coordinator's short window gives the report a different answer | High | L3 (state: classes depend on a producer parameter) |
| C-004 | Where the file lives (`<root>/.dev/sweeps/`, one checkout) | Risk noted: "a reader must be told which root" | Argument: the watcher serves many repos, so one root cannot show the others | Medium | L2 (organization) |
| C-005 | A second persisted artifact under a read-only command | Extends an atomic, tested publish path (`commands.py:153-193`) | Enlarges what sits on disk (rows[].evidence), untracked folder, no retention rule found (UNVERIFIED) | Medium | L2 (dependency, storage) |
| C-006 | OA-17a: entry text on the observer screen | Show it, always through `sanitize.py`; titles-only sends the person back to a second report | Titles and links only; the report keeps the text | High | L2 (interface) |
| C-007 | Which entry fields may be shown (`common.py:139-141`: `recommend`, `suggested`, `needs`, `how`) | Spec must list the fields (risk bullet) | Titles-only avoids a Recommendation on a "navigation only" screen without needing a list | Medium | L3 (guard condition: a field allowlist) |
| C-008 | Is `sanitize.py` enough for free model text | Closes the terminal-control item (CSI, OSC 8, bidi, C1, CR all removed); renderers use `rich.Text` | Controls only: Rich markup and plain-text instructions pass, no length cap (5,000 stays 5,000); markup safety is left to renderers | Medium | L3 (validation rule, boundary on length) |
| C-009 | OA-17b: questions panel exception | Keep the panel's own Orca call, labelled; it is built, gated (`commands.py:67,70`), fixed argv (`adapter.py:32,111`) | End it now; design one shared questions block with one question id before the observer ships | High | L2 (interface, component) |
| C-010 | Open versus handled questions | Not addressed in V1 | The ledger cannot tell handled from open (`questions.py:9-12`); a shared id is the only fix | Medium | L3 (state) |
| C-011 | Is "one data source" true while the panel calls Orca | An "honest exception" makes the claim honest (D11 "One honest exception") | A false statement is not made true by calling it an exception (D11 verdict wording) | Low | L1 (wording, label) |

## Contradictions

| # | Point of Conflict | V1 position | V2 position | Impact |
|---|---|---|---|---|
| X-001 | Is the JSON write inside the sweep's existing contract | Fact 1: a second file "extends a path that already exists and is already tested" | Fact 3: the sweep is read-only and its Will Not list says "Edit, stage or delete a file" (`SKILL.md:61-62`); a second artifact enlarges the disk footprint | Medium: the Will Not text lists what the skill session may do (`Edit, stage or delete a file`); it does not mention the command's own report write, so neither reading is excluded by the text; settled by what the command already does (it writes a Markdown report) |
| X-002 | Who runs the sweep for the work report | Claim 1 plus "What it gets right": one shared file, but the report may run `sweep run --window <time since its last report>` itself | Claim 1: each reader runs its own collection with its own window | Medium: for the report the two positions nearly coincide; the open difference is whether the observer reads a file |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Staleness handling: the screen shows `observed_at` and an age; a missing or old file is its own state, never "no sessions"; the observer already derives STALE after 45 s (`view.py:33-34`) | High |
| U-002 | V1 | A built, gated questions read with a fixed argv and forbidden-verb list (`adapter.py:34-50,111`), and the fact that sweep JSON v1 has no questions block (12 keys, `report.py:613-640`) | High |
| U-003 | V1 | The hybrid for the report: run `sweep run --window <since last report>` itself, which also saves a file | High |
| U-004 | V1 | "No sweep reference in `observe/*.py`" (grep) and the observer already makes its own worker-list read (`adapter.py:29`) | Low |
| U-005 | V2 | Multi-repo location problem for a per-checkout `.dev/sweeps/` | Medium |
| U-006 | V2 | The ledger limit: handled questions are listed open again (`questions.py:9-12`) | Medium |
| U-007 | V2 | Sanitizer gaps shown by test: Rich markup text and instructions pass, no length cap | Medium |
| U-008 | V2 | Three text sanitizers already exist (observer, sweep report `report.py:569-599`, report skill); entry text adds a fourth path | Low |

## Shared Assumptions

Agreement points scanned: (1) the observer cannot sweep every 15 s; (2) entry text is untrusted and must be sanitized; (3) "one data source" is not literally true while the panel calls Orca; (4) the sweep stays read-only and recommends nothing; (5) the report should be able to use its own window.

| A-NNN | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | Entry files exist for the observer to read. | Both papers describe entry text or entry titles taken from `.dev/coordinator/orchestrated/` | UNSTATED, and CONTRADICTED in part: the techref says the only writer, `superclaude orchestrator report-entry`, is designed and absent (`OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:805,820`); only `run.py` moves closed files | Yes |
| A-002 | The observer will be changed to read the sweep file or entry files at all | Both argue a design the observer does not implement today (no import of sweep; no entry-file reader in `observe/`) | STATED by V1 fact 4; V2 does not state it | No |
| A-003 | The 90 s `Budget(total_s)` is how long a sweep takes | Both cite `probes.py:130` against the 15 s cycle | UNSTATED: it is a cap, not a measurement; the per-call timeout is "UNVERIFIED until the first permitted live read measures it" (`adapter.py:60-62`); a sweep that usually takes 5 s would change the cost argument but not WC-16's one-per-5-minutes rule | Yes |
| A-004 | The screen is read by a person, not by an agent that could follow text on it | Both argue about what text is safe to show | UNSTATED; matters for the "plain-text instruction passes" finding (V2 fact 5), which is only a risk if a model reads the screen | Yes |

Promoted (UNSTATED) assumptions: A-001, A-003, A-004.

## Summary

- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 4 (UNSTATED: 3 promoted, STATED: 1, CONTRADICTED in part: 1 (A-001))
- Highest-severity items: C-001, C-003, C-006, C-009
- Taxonomy coverage: L1 = S-001, S-002, C-011; L2 = C-001, C-002, C-004, C-005, C-006, C-009, X-001, X-002; L3 = C-003, C-007, C-008, C-010, A-001, A-003, A-004
- Total diff points in the convergence denominator: 19 (2 + 11 + 2 + 4)
