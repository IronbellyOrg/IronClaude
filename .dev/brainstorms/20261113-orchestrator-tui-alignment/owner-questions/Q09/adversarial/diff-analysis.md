# Diff Analysis: owner-answer proposals for Q9 (keeping the sweep's JSON)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C; Mode A copies)
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (2), unique (3), shared assumptions (2 promoted)
- Prerequisites validated: output path is under `.dev/`, not a forbidden `.claude/` prefix; all three inputs exist.
- Orchestrator fact check (2026-11-14): sweep reports are written to `<root>/.dev/sweeps/`, which is gitignored (`.gitignore:256`; design `docs/designs/orchestrator-mode.md:63`, GQ-106); report retention is out of scope, "the person deletes old reports by hand" (design `:35`, SP-22).

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Section set | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Is the JSON kept? | Not now; Phase 2 caller capture first, stored file only if needed | Yes: appended as a fenced block inside the dated report | Never; stdout-only by standing rule | High |
| C-002 | NFR-001 ("a sweep adds exactly one report file") | Unchanged now; may be relaxed later with its two tests | Unchanged (still one file) | Unchanged permanently | Medium |
| C-003 | Work item SW-11 | Stays deferred in wave W5 with a trigger | Becomes a small Phase 2 item after the #539 merge | Closed as "will not do" | Medium |
| C-004 | Who owns storage rules (location, retention, file mode) | Each caller | The sweep, through its reports | Nobody | Medium |
| C-005 | Effect on later readers (v2, a Coder#477 status record, Q17 observer) | Left open until a reader is named | Enabled with no new producer work | Closed; a new owner question is needed | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | Should anything be kept before a named reader exists? | No: "Lets the first real reader ... define the field list and retention before anything is stored" | Yes: "readers find facts by report date" with no reader named | No, and not later either | High |
| X-002 | Does keeping the JSON require relaxing NFR-001? | A stored file would ("relaxes NFR-001 and changes the two tests") | No: embedding keeps one file, so "NFR-001's two tests ... should pass unchanged" | Not applicable | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | Ordered fallback: caller capture first, a stored file only if capture fails a named need, with an explicit trigger | Medium |
| U-002 | B | Embedding the JSON in the one report keeps the file count and avoids a sidecar | Medium |
| U-003 | C | Removes an open item permanently and records in the contract note that the JSON has no stored form | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | B relies on reports as the store; A and C point later readers to the Markdown report | The dated reports themselves last long enough to serve as a record (they are in the gitignored `.dev/sweeps/` folder of the coordinator's checkout and are deleted by hand) | UNSTATED | Yes |
| A-002 | All three describe a reader of sweep facts without saying where it runs | Any later reader runs on the same host and checkout as the sweep (the reports and the stdout reply never leave that checkout) | UNSTATED | Yes |

### Promoted shared assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Reports last long enough to be a record | All three | If false, B's embedded copy is lost with the report, and "read the Markdown report" in A and C is not a durable fallback | Open |
| A-002 | Readers share the sweep's host and checkout | All three | A reader on another host (for example a Coder#477 status record) needs a transport none of the three provides | Open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- Taxonomy tags: L3 (guard and state): C-002, X-002, A-001; L2 (structure and dependency): C-001, C-003, C-004, C-005, X-001, A-002; L1: S-001.
