## Template-Conformance QA Report (Partition a of 2, Assigned sections: 1-5)

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4241 lines; this instance covers header, Table of Contents and Sections 1 to 5, lines 1 to 1145)
**Lens:** template conformance (QA phase: report-lens-template-conformance, instance a)
**Date:** 2026-11-14

[PARTITION NOTE: checks are limited to Sections 1-5 plus the header and Table of Contents. Section ordering is judged for Sections 1-6 boundaries only; Sections 6-10 belong to instance b.]

**Checked:**

| Item | Check | Result | Evidence |
|---|---|---|---|
| a | Sections 1-5 present and in template order | PASS | `grep -n '^## '` gives 1 Problem Statement (l.90), 2 Current State Analysis (l.105), 3 Target State (l.480), 4 Gap Analysis (l.572), 5 External Research Findings (l.775), then 6 at l.1146; template at `~/.claude/skills/tech-research/SKILL.md:1317-1493` |
| a | Template sub-structure inside each section | PASS | S1 has the three bullets The question / Why it matters / Trigger (l.92-101). S2 has 2.1-2.5 each ending in an `**Evidence:**` line (l.172, 237, 276, 382, 433) and 2.6 Current State Summary (l.435). S3 has Desired behavior, Success criteria (SC-1..SC-17), Constraints (K-1..K-11). S4 table has the exact columns Gap / Current State / Target State / Severity / Notes. S5 has topic areas 5.1-5.4 with Finding / Source / Relevance / Relationship to codebase fields (as table columns, plus Date) and 5.5 External Research Summary |
| a | Gap table integrity | PASS | 144 data rows, all 5-cell (column count 7 with the outer pipes); severity values only Critical 15, Important 65, Minor 64; matches the report's own coverage self-check (4.2: 144 rows, 15/65/64) and its sub-count (D 16 + BL 23 + MS 23 + ENS 9 + OPEN 2 + DOC 71 = 144) |
| b | Ordering and no merged sections in 1-5 | PASS | No reorder, no merge. Additions that are not in the template (citation key at the head of S2, conventions table at the head of S3, rows groups note in S4, 4.1-4.3, reading notes in S5, 3.1) are inserted without displacing any template element |
| c | Placeholder, sentinel and TODO scan over lines 1-1145 | PASS | `grep -nE 'TODO|TBD|PLACEHOLDER|FIXME|\[Topic\]|filled after|XXX|<fill|Step 5\.2|lorem'` over the whole report: no hits. A wider bracket scan (`[Topic|Name|path|count|today|URL|Option A-C|Subsystem|gap|question]`, `N/A`, `to be filled`, `???`) over 1-1145: the only hits are legitimate text (`<path>`, `CR:<n>` in the citation key, the word "pending" describing external human labels, `<output>` in command lines); none is a template remnant |
| d | ToC matches headers in names, anchors and hierarchy | PASS | A script compared all 72 ToC entries (lines 11-88) with the report headings: 0 missing headers, 0 anchor mismatches (GitHub-style slug), 0 level mismatches. No `##`/`###` heading in lines 90-1145 is absent from the ToC. The ToC lists headings to `###` depth for every section, and the `####` headings (5.1.1 etc.) are omitted consistently |
| e | Header fields | PASS | Date 2026-11-14 (matches today), Depth Deep, Research files "13 codebase + 4 web research" (the `research/` directory holds 13 `NN-*.md` and 4 `web-*.md` files, plus `research-notes.md` and `scope/`), Scope present, Scope note present (report only; no roadmap; merge via `/sc:adversarial --compare --merge`) |

Executor-note checks (inside this slice):

| Note | Result | Evidence |
|---|---|---|
| (3) 35-of-39 phrase not stated as measured cause | PASS | Line 163: "the parsed-sparse flag was set in 35 of 39 runs (34 of the 38 Tier 2 runs) and was decisive in 0 for certain, at most 1 ... counts only, cause not established"; Section 4.1 row 16 (l.746) and DOC-59 (l.713) repeat the recount and state "no causal claim". No sentence in lines 1-1145 says Tier 2 was driven by the flag as fact |
| (4) E2 cited at the single commit | PASS | `4a22d74213f93837d00c2c314075dd967b9a98e3` appears in the header, Problem Statement, citation key and MS-23; shorthand `4a22d742` is defined against it in the key (l.122) |
| (5) report only, no roadmap | PASS | Header scope note and Section 1 Trigger state it |

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | MINOR | Whole report (sections 1-5 boundaries) | The template puts a `---` rule after the header, after the ToC and between every pair of sections. The report has `---` only at lines 9 and 88; there is no rule between Sections 1/2, 2/3, 3/4, 4/5 or 5/6. Cosmetic; no content or heading is affected | Optional: insert a `---` line before each `## N.` heading |
| 2 | MINOR | 5.1-5.4 | Template shows the external findings as bullet fields (`**Finding:** / **Source:** / **Relevance:** / **Relationship to codebase:**`). The report uses tables with the same four fields as columns plus a Date column. Same required information, different layout; the tables suit the template's own "tables over prose" content rule | None needed; note only |

### Summary

- Total findings: 2
- Critical: 0
- Important: 0
- Minor: 2

Verdict: PASS (0 critical + 0 important; minor findings listed as notes)

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 4 | Glob: 0 | Bash: 6 (heading and ToC scripts, row counts, sentinel scans, `ls research`)
