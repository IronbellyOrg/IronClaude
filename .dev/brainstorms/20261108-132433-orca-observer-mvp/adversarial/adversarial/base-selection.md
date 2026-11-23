# Base Selection Report

Variants: V1 = opus:architect (A Signal Bridge), V2 = opus:analyzer (B Attention Ledger), V3 = haiku:backend (C Decision Desk).
Template: sc-adversarial-protocol refs/artifact-templates.md Section 3, extended to the 6 dimensions of refs/scoring-protocol.md.

## Quantitative Scoring (50% weight)

Source requirements (seed-brief.md has no formal IDs, so section-level topic matching is used, per the RC edge-case rule): 24 items in total. R1-R9 are the nine "Every proposal must cover" items (line 31); K1-K8 are the eight Constraints bullets (lines 48-55); S1-S7 are the seven Success Criteria bullets (lines 59-65). A bundled bullet counts as matched only when every element in it is addressed.

| Metric | Weight | V1 (opus:architect) | V2 (opus:analyzer) | V3 (haiku:backend) |
|--------|--------|---------------------|--------------------|--------------------|
| requirement_coverage | 0.30 | 1.000 (24/24: R1-R9 map to sections 2-11; K4 "no blinking" = T20 line 198; K8 = T5 line 183; S6 = T2/T3/T7/T8/T9/T10 lines 180-188) | 1.000 (24/24: R1-R9 map to sections 2-11; K4 blink = line 103 and T28 line 185; K8 = AC-7 line 183; S6 = T7/T16/T22/T11/T13 lines 179-185) | 0.958 (23/24: K4 not fully matched. A search for "blink" returns no match in V3, so the "no blinking" element of K4 is not addressed. Every other item is matched, e.g. S6 = lines 238, 255, 243, 260) |
| internal_consistency | 0.25 | 0.993 (1 contradiction / 136 scorable claims: line 6 calls `result.count` "a verified count" and line 68 renders it as "100+ unread", but line 222 lists "Whether `result.count` is total unread or rows returned" as UNVERIFIED) | 0.988 (2 / 166: (a) line 76 says "Each is pinned by a test in section 10", but the policy-frozen rule (line 87) and the `empty` fixture rule (line 85) have no test in T1-T32; (b) line 152 makes the renderer `(model, width, color) -> list[str]`, while the harness at line 173 renders through `Console(... record=True)` and reads `export_text()`, two different output contracts for the same renderer) | 1.000 (0 / 226: stale threshold 30 s (line 65) matches the backoff rule (line 226); 4 worker pages plus 1 message read (lines 216-217) fit the 5-subprocess cap (line 219); cursor caution at line 51 matches lines 130 and 221) |
| specificity_ratio | 0.15 | 0.895 (137 concrete / 153 substantive lines) | 0.927 (139 / 150) | 0.504 (122 / 242) |
| dependency_completeness | 0.15 | 1.000 (10/10 numbered cross-references resolve: "section 9" (66, 195), "decision 11.5" (86), "11.4" (100), "11.2" (123), "section 7" (148), "11.6" (161), "section 2" (179, 207), "section 4" (222); every R0-R8 in the text is defined in the section 7 table) | 1.000 (12/12 resolve: "section 10" (76), "decision 8" (99), "decision 9" (100), "gate (section 7)" (113), "section 4" (199), "section 7" (204), "decision 5"/"decision 12" (212), "T9" (213), "T18" (214), "T29" (217), "section 3" (219); Release 0-3 references resolve to the section 7 table) | 0.929 (13/14: "Release 2" (274), QUESTION-LINK (181, 194, 239 -> defined 134-137), OFFLINE-FIXTURE (125), WORKER-SNAPSHOT (129), QUESTION-CLOSURE and OWNERSHIP-JOIN (141-142), REVISION-VERIFICATION and ADMISSION-HUMAN-LINK (145-146), COST-COVERAGE and DURABLE-REPLAY (147), association edges (198 -> 196) resolve. COMPLETE-MESSAGE-ENUMERATION (143) is named but its content is never defined) |
| section_coverage | 0.15 | 1.000 (12 top-level H2 sections) | 1.000 (12 top-level H2 sections) | 1.000 (12 top-level sections; V3 has no H2, so its 12 "# " headings at lines 1-285 are treated as its top level) |
| **quant_score** | | **0.982** | **0.986** | **0.902** |

Computation details:

- **quant_score** = 0.30*RC + 0.25*IC + 0.15*SR + 0.15*DC + 0.15*SC.
  - V1: 0.300 + 0.248 + 0.134 + 0.150 + 0.150 = 0.98247.
  - V2: 0.300 + 0.247 + 0.139 + 0.150 + 0.150 = 0.98599.
  - V3: 0.2875 + 0.250 + 0.0756 + 0.1393 + 0.150 = 0.90241.
- **SR method.** The protocol's strict vague-word list ("appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practice", "industry standard") finds 0 hits in V1, 0 in V2 and 0 in V3. V3's single raw hit, line 37 "was needed", is a false positive of "as needed". With 0 hits everywhere the list cannot tell the variants apart. So SR counts substantive lines (not headings, blank lines, table separators or code fences) and treats a line as concrete when it contains a number, a backticked identifier, an upper-case token (e.g. `NO_COLOR`, `STALE`, `QUESTION-LINK`) or a named product (Rich, Textual, Bubble Tea, Ratatui, Go, Orca, Python, POSIX, Windows). Every other line counts as non-specific.
  - Known bias: V3 writes one sentence per line, while V1 and V2 pack several statements into one table row. That pulls V3's ratio down somewhat. The size of the gap (0.50 against 0.90 or more) still shows a real difference; for example, V3's acceptance table (lines 236-249) names no fixture variants and no expected strings.
- **IC claim counts** are approximate tallies of falsifiable statements, by section: table rows, bullets, numbered tests and recommendation items. One contradiction moves IC by less than 0.01, so a rounding difference in the tally cannot change the result.
- **SC.** All three variants have the shared 12-section order (debate point S-003).

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence (CEV) | V2 | V2 evidence (CEV) | V3 | V3 evidence (CEV) |
|-----------|----|-------------------|----|-------------------|----|-------------------|
| Covers all explicit requirements | MET | 24/24 seed items matched; e.g. line 198 "T20 \| No blinking \| Rendered segments never carry the blink style" closes the last K4 element | MET | 24/24; e.g. line 185 "T28: the blink attribute (SGR 5/6) never appears"; line 183 "AC-7 \| No one-to-one session/worktree assumption" | NOT MET | No evidence found for K4 "no blinking": searched every section (no "blink" anywhere). The rest is covered (line 264 NO_COLOR, line 265 export, line 246 full identifiers) |
| Addresses edge cases/failures | MET | Line 65 "when a call fails, times out or returns unparsable JSON, the source row ... turns to `STALE since HH:MM:SS (reason)`"; T7-T10 (lines 185-188) | MET | Line 80 "A failed poll shows `FAILED (<exit code or timeout>) <age>`"; line 85 "Empty states: `0 rows interpreted (contract UNVERIFIED)` is not `no questions`" | MET | Line 256 "Conflicting timestamps: equal-time contradictions, missing times, invalid times and future clock skew display uncertainty, never negative age" |
| Includes dependencies/prerequisites | MET | Line 111 "\| Release \| Contents \| Gate (must be verified before work starts) \|"; line 114 "One more check: that `check --peek --run <id>` works from an unbound observer terminal (UNVERIFIED)" | MET | Line 117 "Each release ships only after its named source contract is verified by a recorded, redacted sample pinned in a contract test"; line 123 R2 gate lists the message fields required | MET | Line 134 "Release 2 — first complete live Decision Desk MVP; gate: QUESTION-LINK contract"; line 148 "Every gate needs representative success, missing, stale and contradictory source samples plus parser tests" |
| Defines success/completion criteria | MET | Section 10, lines 177-199: T1-T21, each mapped to a paraphrased issue criterion with a pass condition, e.g. T7 "one row kept (newer), `duplicates merged: 1` shown" | MET | Section 10, lines 175-187: AC-1 to AC-10 plus a contract row, T1-T32, e.g. T18 "shows `fetched 100 of page.total 287`, never `287 workers`" | MET | Line 236 "\| Seed-carried issue criterion \| Required acceptance evidence \|" plus lines 251-267 test obligations, e.g. line 257 "Paging: totals 0, 80, 100 and above 400" |
| Specifies out-of-scope items | MET | Section 5 table, lines 74-86, each item with a "Why", e.g. line 81 "Cost, tokens, usage \| Coverage not established. No slot at all in the MVP" | MET | Section 5 table, lines 91-103, e.g. line 97 "Affected-session evidence ledger (C's core) \| It needs authoritative joins" | MET | Section "Deliberately left out", lines 91-104, e.g. line 100 "No durable event store, SQLite service, background server or external network listener in the slice" |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence (CEV) | V2 | V2 evidence (CEV) | V3 | V3 evidence (CEV) |
|-----------|----|-------------------|----|-------------------|----|-------------------|
| No factual errors / hallucinated claims | MET | Line 152 "`_find_orca()` ... (defined at line 198 ...)" matches seed line 85 ("`install_user_setup.py:198-221`"). Line 28 says the built 116-column branch "drops the counts entirely"; that differs from seed line 44 but is confirmed by debate X-001 ("A and B static reads: built layout drops the counts line at 116"). No claim found that contradicts Known Context | MET | Line 13 quotes `--all` as "every message for the handle; does not mark read" and the 100-row cap, consistent with seed line 38. Line 108 "Its 116- and 80-column builds also drop the SIGNALS panel (seed brief discrepancy)". Line 153 openly says "I did not re-check" the provenance of `canvas.py`. No claim found that contradicts Known Context | MET | Lines 163-164 "Seed comparison versions are Go 2.1.1 / 2.0.6 / 2.2.1 ... The reference manifest's Go pins 2.0.6 / 2.0.3 / 2.1.0 are different" match seed lines 43 and 95 exactly. Line 60 "`totalCount` wording is superseded by the seed's verified `page.total`" matches seed line 37 |
| Technical approaches feasible | MET | Line 146 "POSIX `termios`/`tty` cbreak mode on a daemon thread feeding a queue, the same thread-plus-`Event` shape as `sprint/monitor.py`'s `OutputMonitor`" builds only on the stdlib and Rich | MET | Line 151 "a small stdlib reader, POSIX-only, needed for j/k/Enter/Esc/m/e/q ... It costs less than a new language toolchain"; line 161 reuses the `OutputMonitor` thread pattern | MET | Line 168 "Budget a small, tested terminal-input boundary; do not pretend Live alone provides stable selection"; line 170 Textual fallback "only if a keyboard/terminal restoration spike exceeds the agreed maintenance budget" |
| Terminology consistent | MET | Line 54 "Grouping uses `runId` and labels it 'run', never 'orchestrator'"; `absent` vs `empty` defined once at line 62 and used the same way in T10 (line 188) | MET | `unknown` defined at line 78 and kept as the `UNKNOWN` sentinel at line 162 and in T13 (line 181); `no source` is used the same way for report, acceptance, tests and approval (lines 79, 181) | MET | Line 64 "UNKNOWN means not established; UNAVAILABLE means no usable source"; STALE and PARTIAL defined at lines 65-66 and used the same way at lines 224-226 |
| No internal contradictions | NOT MET | Line 6 "degrades to a verified count (`result.count`)" and line 68 "When `result.count` is 100 or more it says `100+ unread`" conflict with line 222: "Whether `result.count` is total unread or rows returned ... \| UNVERIFIED" (IC = 0.993) | NOT MET | Line 76 "Rendering rules. Each is pinned by a test in section 10." The policy-frozen rule (line 87) and the `empty` rule (line 85) have no test among T1-T32 (lines 177-187) (IC = 0.988) | MET | No contradiction found in 226 claims (IC = 1.000); the numeric bounds agree across lines 65, 216-219 and 226 |
| Claims supported by evidence/rationale | MET | Lines 143-146 give four numbered reasons for Rich; every left-out row has a "Why" (lines 74-86) | MET | Lines 11-15 "Evidence chain behind the recommendation" derive the retention need from the `--peek` semantics | MET | Lines 165-171 give the reasons for Rich: Go NO_COLOR override, export validation and keyboard budget; line 287 "C requires trustworthy question-to-evidence links that are not verified today" |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence (CEV) | V2 | V2 evidence (CEV) | V3 | V3 evidence (CEV) |
|-----------|----|-------------------|----|-------------------|----|-------------------|
| Logical section ordering | MET | Headings at lines 3-216 run Summary -> Slice -> Sources -> Unknown -> Left out -> ... -> Owner decisions -> Risks: sources (38) come before the adapter (150) and the tests (173) | MET | Same 12-section order (lines 3-206); sources (48) come before the adapter (155) and the tests (169) | MET | Same order (lines 1-285); sources (34) come before the adapter (173) and the tests (230) |
| Consistent hierarchy depth | MET | H1 title (line 1), then only H2 sections (lines 3-216); no lone subsection | MET | H1 -> H2 -> H3 with no skipped level; H3s sit under sections 1 (line 11), 2 (lines 21-44) and 12 (lines 208, 222). The single H3 under section 1 is a labelled evidence block, not an orphan (see the position-bias table) | MET | One flat level: all 12 headings are "# " (lines 1-285); no subsections, so nothing is orphaned |
| Clear separation of concerns | MET | Line 60 "Rendering rules live in the snapshot model, not in each layout"; line 109 "Two seams only: a source returns `SourceResult(...)`, and a view is a pure function" | MET | Line 152 "keeping the renderer a pure function, `(model, width, color) -> list[str]`, with the adapter separate"; fixture mode is "a separate loader" (line 219) | MET | Line 176 "Use one collector and one immutable published view; rendering never invokes the CLI" |
| Navigation aids | MET | Numbered sections (lines 3-216) and section and decision cross-references, e.g. line 86 "(owner decision 11.5)", line 148 "the snapshot seam in section 7" | MET | Numbered sections plus cross-references, e.g. line 76 "pinned by a test in section 10", line 213 "and T9", line 212 "Owner decision 5 and decision 12" | NOT MET | No evidence found: the headings are unnumbered, there is no table of contents, and no "section X" or "see ..." reference exists; the only pointers are gate names (e.g. line 181 "QUESTION-LINK") and "Release 2" (line 274) |
| Follows artifact-type conventions | MET | Line 1 single H1 title "# Variant 1 (architect): A. Signal Bridge as the Orca observer MVP", then numbered H2 sections in the seed's line-31 order | MET | Line 1 single H1 title "# Variant 2 (analyzer): B. Attention Ledger as the MVP ...", then numbered H2 sections | NOT MET | Line 1 "# Summary": there is no document title, and every section uses H1, against the Markdown design-document convention of one H1 title with H2 sections |
| **Subtotal** | **5/5** | | **5/5** | | **3/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence (CEV) | V2 | V2 evidence (CEV) | V3 | V3 evidence (CEV) |
|-----------|----|-------------------|----|-------------------|----|-------------------|
| Unambiguous language | MET | 0 hits from the protocol's vague list; the hedged "may" lines are limited to the risk table (lines 222-231), where they describe possible effects | MET | 0 hits from the protocol's vague list | MET | 0 real hits (the only raw match, line 37 "was needed", is a false positive) |
| Concrete rather than abstract | MET | SR 0.895; line 163 "Default interval 5 s, minimum 2 s ... worker-list up to 3 pages (300 rows ...), then one `check --peek` per distinct `runId` seen, capped at 10 runs" | MET | SR 0.927; line 161 "at most 3 pages (300 rows), a 10 s timeout per call, a 30 s deadline for the cycle, and an interval of 15 s (minimum 5 s ...)" | NOT MET | SR 0.504. The adapter bounds are concrete (line 216, "at most four worker pages of at most 100 rows"), but the acceptance table, the part meant to be acted on, is abstract: line 243 "Missing field, timeout, parse error, source loss, page drift and incomplete traversal each show explicit status and last success" names no fixture variant and no expected string |
| Each section has a clear purpose | MET | Line 13 "One screen plus one detail view, the same panels at every width"; line 40 "Only two CLI verbs, both non-consuming"; line 60 "Rendering rules live in the snapshot model" | MET | Line 50 "The MVP (Release 0 and Release 1) needs exactly one live source"; line 157 "Scope: one verb" | MET | Line 36 "The seed brief is the contract baseline"; line 175 "This is a proposed application contract, not a claim that Orca returns these normalized names" |
| Acronyms/domain terms defined | NOT MET | Line 171 "strip CSI, OSC (terminated or not), DCS/APC/PM/SOS, 8-bit C1 controls": CSI, OSC, DCS, APC, PM and SOS are never expanded. Only Cf is explained ("category Cf, including bidirectional overrides") | NOT MET | Line 166 "removes CSI/OSC sequences": not expanded. AC is defined at line 171, but CSI, OSC, SGR (line 185) and C1 are not | NOT MET | Line 261 "ESC/C1 CSI, OSC hyperlinks/clipboard/title": not expanded. Only UNKNOWN, UNAVAILABLE, STALE and PARTIAL are defined (lines 64-66) |
| Actionable next steps / decision points | MET | Section 11, lines 205-214: eight decisions, each with "Recommendation: ..." | MET | Section 11, lines 191-204: twelve decisions, each with "Recommend ..."; line 197 names the unblocking decision | MET | Lines 271-281: five decisions, each with "Recommendation: ..."; line 282 separates engineering obligations from owner votes |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence (CEV) | V2 | V2 evidence (CEV) | V3 | V3 evidence (CEV) |
|-----------|----|-------------------|----|-------------------|----|-------------------|
| >=3 risks with probability and impact | NOT MET | Line 218 "\| Item \| Status \| Effect on this proposal \| Mitigation \|": impact is given, but "Status" holds a category (UNVERIFIED / Risk / Design risk), not a probability | NOT MET | Line 210 "\| Risk \| Effect \| Mitigation \|": impact is given, but no row has a probability | NOT MET | Lines 287-298 are prose risks with no probability and no impact rating |
| Mitigation for each risk | MET | Every row in lines 220-232 fills the Mitigation column, e.g. line 229 "`finally` restore plus signal handlers; non-TTY falls back to export; Textual switch rule" | MET | Every row in lines 212-220 fills the Mitigation column, e.g. line 218 "Cap retained items (for example 1,000), with `older retained items dropped: k` disclosed" | NOT MET | Line 292 "cross-page drift remains possible" and line 297 "inherited evidence, not fresh dependency or production certification" give no mitigation in the risk section |
| Failure modes and recovery | MET | Line 165 "A timed-out call is killed, its source marked `STALE (timeout)` ... interval for that source doubles, up to 60 s; one success resets it" | MET | Line 165 "a non-zero exit, a timeout or invalid JSON marks the source `FAILED` ... The last good snapshot stays on screen"; line 216 terminal restore | MET | Line 226 "Keep last successful view on decode/exit failure; back off to 30 then 60 seconds"; line 266 "Ctrl-C restore the terminal" |
| External dependencies and their failures | MET | Line 152 "If it returns `None`, the screen opens in an 'Orca CLI not found' state with every source `unavailable`"; line 138 Textual maintenance risk | MET | Line 159 "If no binary is found, the freshness cell reads `worker-list NOT AVAILABLE (orca binary not found)`. That is not shown as an empty fleet." | MET | Line 179 "a missing or wrong executable becomes a source error, not a crash loop" |
| Monitoring/validation for risk detection | MET | Line 154 "a unit test asserts the forbidden set ... can never be produced"; line 222 "Test against a run with more than 100 unread before R1 ships" | MET | Line 122 "a contract test that fails on any missing top-level key"; T32 (line 187) | MET | Line 148 "Every gate needs representative success, missing, stale and contradictory source samples plus parser tests"; line 228 "diagnostics include duration, counts and errors" |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence (CEV) | V2 | V2 evidence (CEV) | V3 | V3 evidence (CEV) |
|-----------|----|-------------------|----|-------------------|----|-------------------|
| Collection boundaries (empty/single/max) | MET | Line 181 "at 100 rows exactly one page; a 101-row variant forces a second page"; line 182 has runs with 1 row; line 68 the count-0 wording | MET | Line 85 "The fixture variant `empty` must render `no observed items in this source window; not proof none exist`"; T4 (line 178) page cap | MET | Line 257 "Paging: totals 0, 80, 100 and above 400"; line 258 "99 and 100 rows both retain unknown completeness" |
| State interactions across components | MET | Line 169 "Rows from an older cycle never overwrite a newer cycle (each snapshot carries a monotonic cycle number)"; line 26 selection is keyed by `dispatchId` across refresh | MET | Line 84 "`m` (mark looked) moves an item from `not marked` to `marked looked`, and the big count stays the same ... No key, timer or source loss can lower the open count" | MET | Line 211 "Refreshing identical input changes only collection metadata, not facts, selection, counts or change badges"; line 225 atomic publication |
| Guard condition gaps | MET | Line 167 "`result.workers` must be a list and `result.page.total` an integer, else the whole response is `unparsable`"; line 161 "`runId` and handles are validated against a conservative character set" | MET | Line 162 "Top-level keys `result.workers`, `result.page` and `result.scope` are required. If any is missing, the cycle counts as `FAILED (shape)`" | MET | Line 227 "Validate envelope/types and bound strings before normalization"; line 192 "Each optional fact distinguishes absent, explicit null, valid value and invalid value" |
| Count divergence (off-by-one, ranges) | MET | Line 68 "When `result.count` is 100 or more it says `100+ unread`"; line 181 tests the 100/101 page boundary | MET | Line 164 "if `page.total` changes between pages of one cycle, the cycle is marked `PARTIAL (total changed during read)`"; line 83 "`latest <=100 message rows per Run`" (inclusive bound) | MET | Line 84 "y excludes the selected question ... 2 / 7 means two displayed from seven other observed questions"; line 87 "One hundred message rows are not necessarily one hundred questions" |
| Feature interaction effects | MET | Line 184 "`h` shows them; TERMINAL counts unchanged by the toggle"; line 67 filtered, fetched and global denominators side by side | MET | Line 82 "a filter ... always shows `filter <expr>: k of n fetched`, next to the unfiltered `result.counts` line ... never summed into 'workers'" | MET | Line 82 "not added to page-derived counts or assumed to describe the selected filter"; line 68 "collection fresh / evidence stale" |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | V1 (opus:architect) | V2 (opus:analyzer) | V3 (haiku:backend) |
|-----------|---------------------|--------------------|--------------------|
| Completeness | 5/5 | 5/5 | 4/5 |
| Correctness | 4/5 | 4/5 | 5/5 |
| Structure | 5/5 | 5/5 | 3/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 4/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 5/5 |
| **qual_score** | **27/30 = 0.900** | **27/30 = 0.900** | **23/30 = 0.767** |

Shared misses: none of the three variants gives risk probabilities, and none expands the terminal-control acronyms CSI and OSC.

## Edge-Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>=1/5) | Eligible as base |
|---------|-----------------------------|---------------|------------------|
| V1 (opus:architect) | 5/5 | PASS | Yes |
| V2 (opus:analyzer) | 5/5 | PASS | Yes |
| V3 (haiku:backend) | 5/5 | PASS | Yes |

The floor is not suspended, because no variant scores 0/5. No variant is excluded.

## Position-Bias Mitigation

Pass 1 evaluated the variants in the order V1, V2, V3; pass 2 in the order V3, V2, V1. Both passes applied all 30 criteria to every variant (90 verdicts per pass). The table lists only the criteria where the two passes disagreed. Each one was re-evaluated by comparing the evidence the two passes cited, and the re-evaluation verdict is final. It is the verdict used in the dimension tables above.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (re-evaluation) |
|-----------|---------|--------|--------|-----------|-----------------------|
| Completeness 1: covers all explicit requirements | V3 | MET (topic coverage 23/24 read as complete) | NOT MET | DISAGREE | NOT MET: K4 lists "no blinking" as a separate constraint, and V3 never mentions it |
| Correctness 4: no internal contradictions | V1 | MET (line 222 read as a disclosed caveat) | NOT MET | DISAGREE | NOT MET: line 6 calls the count "verified" and line 68 renders "100+ unread" semantics, while line 222 says those semantics are UNVERIFIED. A caveat elsewhere in the document does not cancel the opposing claims |
| Correctness 4: no internal contradictions | V2 | NOT MET | MET (read as a test-coverage gap) | DISAGREE | NOT MET: line 76 "Each is pinned by a test in section 10" is a specific, falsifiable claim, and the test list shows it false for the rules at lines 85 and 87 |
| Structure 2: consistent hierarchy depth | V2 | NOT MET (lone H3 under section 1, line 11) | MET | DISAGREE | MET: no heading level is skipped, and every H3 has an H2 parent. A single labelled evidence block is not an orphaned subsection |
| Structure 4: navigation aids | V3 | MET (gate names used as cross-references, line 181) | NOT MET | DISAGREE | NOT MET: the gate names refer to terms, not to sections. There is no section numbering, no table of contents and no section reference |
| Clarity 2: concrete rather than abstract | V3 | MET (adapter bounds, lines 216-219) | NOT MET | DISAGREE | NOT MET: SR 0.504, and the acceptance table (lines 236-249) gives no fixture names and no expected output |
| Risk 1: >=3 risks with probability and impact | V1 | MET (Status column read as a likelihood proxy) | NOT MET | DISAGREE | NOT MET: "UNVERIFIED / Risk / Design risk" names a category, not a probability |

- Disagreements re-evaluated: 7 of 90 variant-criterion pairs.
- Final verdict differs from pass 1 in 6 cases and from pass 2 in 1 case (V2 Correctness 4).
- Effect of the re-evaluation on the totals, compared with pass 1: V1 -2, V2 +1, V3 -3.
- Pass 1 order (V1 first) favoured the first-read variant, V1 (two lenient verdicts). Pass 2 order (V3 first) was stricter on V3. Re-evaluating every disagreement removes both order effects.
- Caveat: both passes were run by the same evaluator within this step, so position-bias mitigation reduces order effects but does not make the passes independent.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (diff points won, of 57) |
|---------|---------------|--------------|-----------------|--------------------------------------------|
| V1 (opus:architect, A Signal Bridge) | 0.4912 (0.98247) | 0.4500 (0.900) | **0.9412** | 35 (61.4%) |
| V2 (opus:analyzer, B Attention Ledger) | 0.4930 (0.98599) | 0.4500 (0.900) | **0.9430** | 44 (77.2%) |
| V3 (haiku:backend, C Decision Desk) | 0.4512 (0.90241) | 0.3833 (0.767) | **0.8345** | 40 (70.2%) |

How debate points were counted:

- Source: the "## Scoring Matrix" in debate-transcript.md, lines 163-221. It has 57 diff points: S-001 to S-011, C-001 to C-025, X-001 to X-013 and A-001 to A-008.
- A variant earns one point for every row whose Winner cell names its letter, including shared winners and letters in parentheses. For example, S-010 "A+C (+B signature)" gives one point each to A, B and C. C-001 "Merged (A R0-R1, B after question-row gate, C later)" also gives one point to each.
- Rows won outright by one variant: A has S-001, C-016, C-019, X-001, X-010, X-011 and X-013; B has S-002, S-006, S-009 and S-011; C has X-005.
- The Round 3 results (debate-r3) were not read, as instructed. The counts come from the Round 2 matrix only.

## Margin Analysis

- **Top two:** V2 0.9430 and V1 0.9412. **Margin:** 0.0018 (0.18 points), below the 0.05 threshold.
- **Tiebreaker applied:** Yes, step 1 (debate performance). V2 won 44 diff points and V1 won 35. The gap is 9 points, or 15.8 percentage points of the 57, so the debate result is not itself a tie, and step 2 (correctness count, 4/5 for both) and step 3 (input order) are not reached.
- **V3** trails V2 by 0.1085. It is not in the tiebreak, although its 40 debate points are second.
- **Sensitivity:** V1 and V2 have identical qualitative scores (27/30). V2's quantitative lead comes from specificity (0.927 against 0.895). V1's IC lead (0.993 against 0.988) partly offsets it. If any one qualitative verdict flipped between V1 and V2, the order of the top two would change, which is why the tiebreaker decides this selection.

## Selected Base

**Variant 2, opus:analyzer** (`variant-2-opus-analyzer.md`, direction B Attention Ledger). Final score 0.9430. Selected by tiebreaker step 1 (debate points won: 44 against V1's 35).

### Selection Rationale

1. **The scores do not separate V1 and V2.** Both reach 27/30 on the qualitative layer and differ by 0.0018 overall. The binding tiebreaker (debate performance) is decisive: V2's approach won 44 of 57 diff points and V1's won 35. V2 won outright the structural points S-002, S-006, S-009 and S-011. It also shared most of the content points that settled the MVP's honesty rules: C-003, C-008 to C-011, C-013, C-014, X-002, X-003 and X-006.
2. **V2 already carries the converged R1 contract.** Debate X-002 ("R1 allow-list is `worker-list` only") and X-003 ("No number from `result.count` until its meaning is verified") were won by B+C against A. V2 section 9 already has this shape: line 157 "Scope: one verb. `orca orchestration worker-list --json --limit 100 [--cursor <c>]`. Nothing else is executed against Orca in R0 or R1". V1 would need its second adapter template (lines 157-158) and its count rendering (line 68) removed, and that rendering is V1's one internal contradiction.
3. **V2 matches the converged build order.** C-001 (2 of 3) makes B's ledger the default screen once the question-row gate passes, after an A-style R0-R1. V2 section 7 already gates the ledger on R2 (line 123) and has the A fallback (line 130 "swap the default screen to A (Signal Bridge) built on the same adapter and renderer"). It also has C-010's retention rule (line 84 "No key, timer or source loss can lower the open count").
4. **V2's acceptance tests are the most traceable.** They are labelled AC-1 to AC-10, with numbered T1-T32 (lines 175-187), which debate S-006 adopted. Its risk table and its separate UNVERIFIED list (lines 208-233) were adopted as S-009.
5. **Why not V3**, despite its 5/5 Correctness and 40 debate points: its quantitative score (0.902) and qualitative score (0.767) are both lowest. It lacks section numbering, a title heading and concrete acceptance evidence (SR 0.504). Its own MVP cannot show its core panel live (line 31 "The complete decision-first live MVP is blocked until the question-link contract is verified").
6. **Known weakness of the base**, which the refactor plan must fix:
   - Correctness 4: V2 line 76 claims a test for every rendering rule, but policy-frozen (line 87) and `empty` (line 85) have none.
   - The proxy panel (lines 32, 213) was withdrawn by its own advocate under C-004.
   - The interval and timeout values (line 161) must be replaced by the C-006 values.

### Strengths to Preserve from Base

1. **Evidence chain for retention** (V2 section 1, lines 11-15). `--peek` drops read-but-unanswered rows, so the observer must retain observed questions until explicit closure evidence appears. This is the core argument behind C-002 and C-010.
2. **"Seen is not resolved" made mechanical** (section 2 line 46; section 4 line 84). The `m` look marker never changes the open count. `closed by evidence` stays `unavailable` until a closure source exists.
3. **One-verb R1 adapter** (section 9, lines 157-167). It covers a fixed argv tuple, an allow-list test, the required top-level keys with `FAILED (shape)`, `PARTIAL (total changed during read)` and `scope.source` honesty. Debate: X-002, C-013.
4. **Gated release table with a fallback rule** (section 7, lines 117-130). Every gate requires a recorded, redacted sample pinned in a contract test; the A fallback is triggered by an owner deadline (owner decision 12, line 204).
5. **Acceptance table AC-1 to AC-10 with T1-T32** (section 10, lines 175-187). This includes the 27-render scenario matrix (T16), the `fetched 100 of page.total 287` test (T18) and the golden-sample contract test (T32). Debate: S-006, C-021.
6. **Separate risks table and UNVERIFIED list** (section 12, lines 208-233), plus the plain statement of B's own weakness (section 6, line 113). Debate: S-009, S-011.
7. **Denominator and unknown wording** (section 4, lines 78-85). This covers `n+? (k unknown)`, `PARTIAL: fetched 300 of page.total 412`, filtered counts beside `result.counts` (never summed) and the empty-state text. Debate: C-005, C-008.
8. **Owner decision 5** (line 197). Permission to capture one redacted non-empty `check --all --json` sample; this is the decision that unblocks R2.

### Strengths to Incorporate from Non-Base Variants

From V1 (opus:architect):

1. **Source-counts strip at every width** (V1 section 2, lines 28-36), without bars or a health name. `TERMINAL` comes from `result.counts` with `scope.source`, and `LIVENESS` is a verbatim histogram `of N fetched / page.total T`. Debate: C-005, X-001.
2. **Snapshot model with two seams and a monotonic cycle number** (V1 section 7, line 109; section 9, line 169). A source returns `SourceResult`; a view is a pure function of the snapshot and the width; a slow late call can never roll the screen back. Debate: S-010, C-007.
3. **Historical rows hidden by default** behind `h`, with `140 historical hidden (h)` and counts unchanged by the toggle (V1 section 4, line 67; T6, line 184). Debate: X-010, C-012.
4. **SETTLED and POLICY FROZEN shown as `unavailable`**, never `0` (V1 section 2, line 34; section 4, line 69). Debate: X-011, C-022.
5. **Key set** `/`, `h`, `r`, `e`, `q` with ID-anchored selection and the "selected row no longer observed" placeholder (V1 section 2, line 26). Debate: C-015, C-025.
6. **Trailing `>` truncation marker and the `--ascii` export** with box-drawing replacement (V1 section 2, line 36; T15, line 193). Debate: C-016, C-017.
7. **Allow-list test with `subprocess` patched to fail if reached** (T17, line 195). Also NO_COLOR for any non-empty value, including `yes` (T14, line 192).
8. **Placement and stack switch rule.** `superclaude observe`, registered the house way (V1 section 11, line 210). Textual takes over if R2 or R3 needs scrolling panes or multi-pane focus (V1 section 8, line 148). Debate: C-019, C-018, X-013.

From V3 (haiku:backend):

9. **Four states per fact**: absent, explicit null, valid and invalid (V3 "Smallest trustworthy read-only adapter", line 192). Debate: C-008.
10. **Independent clocks and visible equal-time conflicts.** Liveness is ordered by `observedAt`, evidence by `lastObservedAt`, and conflicts are never resolved as "last row wins" (V3 lines 204-208). Dedup key is source namespace plus `dispatchId` (line 202). Debate: C-007, X-005.
11. **Per-cycle resource caps** (V3 lines 216-220): 15 s cycle, at most 5 subprocesses, 8 MiB stdout, kill and reap, coalesced manual refresh. These replace V2's line-161 values. Debate: C-006, X-007.
12. **"Since last look" baseline rules** (V3 lines 211-213): the first observation is a baseline, and a missing row in a partial page is "not reobserved", not resolved. Debate: C-009.
13. **Collection versus evidence freshness** (V3 line 68: "collection fresh / evidence stale"). Source STALE comes from poll success, with no row verdict. Debate: C-011, X-006.
14. **Overflow denominator that excludes the selected item** (V3 "Shown as unknown / stale / partial", lines 83-87): "y excludes the selected question", and 100 rows are not 100 questions. Debate: C-014.
15. **Gate vocabulary with four sample kinds per gate** (V3 "Build order", lines 125-148, especially line 148). Also the R2 rule "If affected references are absent ... show unknown scope and no affected ledger" (line 138). Debate: S-007.
16. **Literal Rich text, never markup, for external strings** (V3 line 262). Plus the operations tests for timeout and reap, oversized JSON, discovery failure and Ctrl-C restore (line 266). Debate: C-020.
17. **Cost shown as `cost unavailable`, never `$0`** (V3 line 75). Debate: C-023.

Base fixes required by the debate:

18. **Remove the proxy panel.** Drop V2's `WORKER-REPORTED NEXT ACTIONS` panel (V2 section 2, line 32) and show `projection.nextAction.kind` as a verbatim ledger column and filter, as in V1 section 3 line 47. Debate: C-004, which B withdrew.
19. **Close the test-coverage gap.** Add tests for the policy-frozen rule (V2 line 87) and the `empty` rule (V2 line 85), so that V2's line-76 claim becomes true.
20. **Settle the renderer contract.** Choose one renderer output type for V2 lines 152 and 173.
