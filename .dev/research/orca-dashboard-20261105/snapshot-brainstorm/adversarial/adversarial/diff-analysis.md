# Diff Analysis: spec Comparison

## Metadata
- Generated: 2026-11-05T19:10:43Z
- Variants compared: 3 (V1 (opus:architect) `variant-1-opus-architect.md`; V2 (sonnet:analyzer) `variant-2-sonnet-analyzer.md`; V3 (haiku:backend) `variant-3-haiku-backend.md`)
- Total differences found: 42 (structural + content + contradictions; unique contributions and shared assumptions are listed separately)
- Categories: structural (12), content (20), contradictions (10), unique (18), shared assumptions (4)

## Structural Differences
| # | Area | V1 (opus:architect) | V2 (sonnet:analyzer) | V3 (haiku:backend) | Severity |
|---|------|---------------------|----------------------|--------------------|----------|
| S-001 | Overall document organization | 17 sections; architecture model first (s.2), then requirements (s.3), shared frame (s.4), one section per concept (s.6-10), comparison (s.11), four states (s.12), overflow (s.13), evaluation (s.14), limits (s.15), risks (s.16), gates (s.17) | 12 sections; evidence basis (s.1), shared contract plus fixture world (s.2), requirements (s.3), all five concepts in one section (s.4), comparison (s.5), default (s.6), four states (s.7), other concepts x states (s.8), evaluation (s.9), limits (s.10), risks (s.11), gates (s.12) | 12 sections; purpose plus concept set (s.1), requirements (s.2), observation/data contract (s.3), integrity and rendering rules (s.4), one section per concept (s.5-9), default plus four states (s.10), evaluation (s.11); risks, limits and gates merged into one section (s.12) | Medium |
| S-002 | Architectural model | Explicit four-layer model (collector adapters, observation store, derivation, frame+renderer) with an owns / must-never table and a logical report-model field list (s.2); requirements carry a Layer column (s.3) | One sentence: all five concepts "can be projections of one normalized read model", marked [P] and explicitly "not specified here" (s.6) | No layer model; a logical observation envelope, record table (Work, Resource, Decision, Evidence, Relation) with integrity rules, and source-capability rules (s.3) | High |
| S-003 | Requirements catalogue form | 39 IDs in 7 families (DEC 6, BLK 5, COM 6, CHG 5, VER 5, COV 6, FMT 6) with a Layer column (s.3.1-3.7) | 40 IDs in 7 groups (R-DEC 5, R-BLK 5, R-COM 5, R-CHG 5, R-VER 5, R-FLT 5, R-FMT/OVF/INT 10) with a Basis column citing seed brief or REPORT.md section (s.3.1-3.7) | 16 flat IDs R01-R16 with an "observable acceptance condition" column (s.2) | Medium |
| S-004 | Shared frame contract placement | Dedicated frame section: fixed header lines (title, as-of, scope, src, OLDEST) and footer (omitted, legend) with a field-to-requirement table (s.4.1-4.2) | Header block table (s.2.1) and symbol table (s.2.2); no footer contract; a fixed summary line added later as R-INT-05 (s.3.7) and "common repair" (s.8) | No standalone frame section; header and footer lines emerge from integrity rules (s.4 rules 2, 8, 9) and recur in mockups (s.5-10) | Medium |
| S-005 | Fixture definition | One shared busy fixture implied by reuse of D-DEMO-00xx keys across s.6-10; no fixture table | Explicit fixture-world table with ages, links and shared task (s.2.6), reused by all five screens | Small prose fixture: 3 workers, 3 tasks, 2 questions, 1 verification failure (s.1); source times defined in s.4 closing paragraph | Medium |
| S-006 | Four-state coverage of the default | All four states for concept A: empty-partial (s.12.1), busy by reference to s.6.2 (s.12.2), stale (s.12.3), checks-failing (s.12.4); other concepts get a "State handling" paragraph (s.7.3, 8.3, 9.3, 10.3) | All four states for C1 drawn (s.7.1-7.4) plus a concept x state matrix naming residual false-all-clear risk for C2-C5 (s.8) | All four states for Decision Brief drawn (s.10); other concepts get a "State behavior" paragraph (s.5-9) | Medium |
| S-007 | Overflow demonstration | Overflow shown inside the busy screen (`+3 more:` s.6.2) and specified as rules OVF-1..8 (s.13) | Dedicated overflow screen with 19 decisions and on-screen arithmetic (s.7.1) plus R-OVF-01 (s.3.7) | No overflow screen; overflow covered only by prose rules (s.4 rules 7-9), one paragraph (s.10 busy) and an acceptance case (s.11) | Medium |
| S-008 | Cross-concept comparison artifact | +/o/- matrix over 10 criteria (s.11.1) plus a data-dependency-per-concept table (s.11.2) | Word-rated matrix over 9 criteria including "gate load" and counted busy line totals (s.5), plus a by-eye requirement check paragraph | No comparison matrix; one paragraph naming each alternative's best use (s.10) | Medium |
| S-009 | Evaluation section structure | One table EV-1..EV-10, mechanical width check folded in as EV-10 (s.14) | Reader tasks ET-1..ET-10 (s.9.1), separate mechanical checks MC-1..MC-8 (s.9.2), and a default decision rule (s.9.3) | Operator tasks E01-E07 (s.11) plus a list of 12 deterministic "future contract acceptance cases" (s.11) | Medium |
| S-010 | Feasibility-gate table shape | G1-G8 with columns question / passing unlocks / if it fails (s.17) plus 4 open debate questions | FG-1..FG-8 with columns if open / closing evidence / concepts affected (s.12.1), 7 open questions (s.12.2) and a recommended next step (s.12.3) | G01-G08 with columns question / if unresolved, inside the merged risks-limits section (s.12) | Low |
| S-011 | Notation and legend | Token legend (`?`, `>=N`, `seen>=`, evidence brackets) defined (s.4.3) and printed as a footer line in every report (s.4.1) | Symbol table (`!`, `?`, `~`, `*`, `X`, `>`, ladder `+ - .`) defined (s.2.2) but not printed in reports except the C4 ladder legend (s.4.4) | Words instead of symbols (`unknown`, `PARTIAL`, `STALE`, `observed >=Nm`); single-letter source codes W/M/V defined in prose (s.4) and never printed as a legend | Medium |
| S-012 | Screen layout grammar | 5-line frame with `===` title bar and `---` section separators; body sections numbered 1-4 (s.4.1, s.6.2) | 3-4 line header then an 80-column `===` rule; sections separated by `---` rules (s.4.1) | 5-line slash-separated header, no rule lines, sections separated by blank lines and capitalized headings (s.5) | Low |

## Content Differences
| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | Second organizing axis of the concept set | B Control Board: fixed run x lane count matrix plus item list; axis = location (s.5, s.7) | C2 Ball-Holder Board: bands by who must move next (HUMAN / COORDINATOR / WORKER / NOBODY KNOWN); axis = responsibility (s.4, s.4.2) | B Run Ledger: per-run register with WORK / ASSIGNMENT / VERIFICATION / EXECUTION columns, runs sorted by oldest request; axis = run ownership (s.1, s.6) | High |
| C-002 | How distinct the five screens are | Layouts differ materially: queue (s.6.2), matrix (s.7.2), tree (s.8.2), ladder columns (s.9.2), journal with TRAIL (s.10.2) | Layouts differ: ledger (s.4.1), bands (s.4.2), tree (s.4.3), ladder grid (s.4.4), changed/carried split (s.4.5); set named "Five-Question Snapshot Set (5Q)" (s.4) | Four of five screens repeat the same three bundles (D1, F1, D2) almost verbatim under different headings (s.5, s.8, s.9, s.10); only B adds a table (s.6) and C a small tree (s.7); claims concepts "share truth rules, not a common dashboard" (s.1) | High |
| C-003 | Recommended default and switching condition | A Attention Brief; runner-up E once observation history exists; no measured switch rule (s.11.3) | C1 Oldest-Ask Ledger with three borrowed elements (C5 SINCE strip, C3 holds/shared notes, C2 ANSWERED band); switch to C5 if ET-1 ties and ET-6 recall is higher (s.6, s.9.3) | Decision Brief as "provisional default, not a validated winner"; replace only if another concept improves E01 and E06 without more false all-clears (s.10, s.11, s.12 G08) | Medium |
| C-004 | Oldest-blocking-decision findability outside the default | Mandatory `OLDEST` frame line in every concept (DEC-3, s.4.2); comparison rates B/C/E "o (frame line)" (s.11.1) | No oldest pointer required outside C1; R-INT-05 fixed line carries counts only (s.3.7, s.8); C5 rated "Weak: lives in lower block" (s.5) | Mandatory global "oldest observed" pointer in every concept header; overflow "never rotates the oldest away" (s.4 rules 2 and 8, s.6 tradeoffs, s.6-9 screens) | High |
| C-005 | Unknown original creation time | Age from first observation labelled `seen>=`; sorted by lower bound and flagged as possibly older (DEC-5, s.6.1) | Age always from original creation, never from last update; no fallback specified when creation time is absent (s.2.3, R-DEC-02) | `observed >=Nm` from first observation; separate visible warning that the oldest cannot be certified; future timestamps print `clock conflict` (s.4 rule 1) | High |
| C-006 | Partial-count and coverage notation | `>=N observed`, `0 observed (partial)`, hosts `N covered of ? expected` (DEC-4, OVF-7, COV-2) | `N observed*`, "at least", "none seen in the part read: PARTIAL*"; hosts "local only, expected list unknown" (R-DEC-04, s.2.2, s.7.2, R-FLT-01) | Words: "decision census unknown", "at least N observed affected tasks", footer "unobserved unknown"; hosts "Missing in-scope hosts: none" for a named scope (s.3, s.4 rules 6 and 8, s.5) | Medium |
| C-007 | Root-blocker grouping and shared dependents | Roots ranked by distinct tasks affected, then age; shared task drawn under first root, `see [n]` under the other, counted once (BLK-2, BLK-3, s.8.1) | Roots by age; shared task drawn under the older root and referenced under the other, counted once (s.2.4, s.4.3) | Roots by oldest decision, explicitly not by impact; shared task repeated `also under <ID>` and counted once in a UNION footer; cycles print `dependency conflict` (s.4 rule 6, s.7) | High |
| C-008 | Heartbeat and liveness suppression | Heartbeats only update last-seen (COM-4); liveness flaps are not deltas (CHG-4); D folds heartbeat-only workers into a QUIET count (s.9.2) | Heartbeats collapse to one last-seen; a worker is listed only when silence crosses a printed threshold (WATCH row, 15m placeholder) (s.2.4, s.4.1, s.10 limit 7) | Heartbeats excluded from changes (R06); no silent-worker row; "execution presence is not readiness" (s.9, s.10) | Medium |
| C-009 | Delta baseline and change vocabulary | Compare only with last successful observation of the same source (CHG-1); partial or failed gives `n/a (no baseline)` (CHG-2); kinds new / escalated / aged / resolved / vanished (CHG-3) | Compare with last successful observation, time shown (R-CHG-01); failed or partial never a baseline (R-CHG-02); kinds opened / resolved / worsened / recovered / failure new / check flipped / coverage changed (R-CHG-03); gap length stated (R-CHG-04) | Per-source, per-scope last-success pointer; only compatible scope/schema compared; partial observations may establish additions but never absence, resolution or negative movement; "newly observed" is not "newly created" (s.4 rules 4-5) | High |
| C-010 | Item that disappears without resolution | Explicit VANISHED delta kind; item kept open (CHG-3, DEC-6, s.6.2) | No vanished kind; only a resolution linkage removes a row (R-DEC-05); stale rows keep `~` (s.7.3) | "last known unresolved; current status unknown"; cancellation is a disposition, not an answer (s.4 rule 3) | Medium |
| C-011 | Answered-but-unresolved decisions | Leave NEEDS YOU (next actor not human) but stay listed by key in the FLEET line (s.6.1, s.6.2) | Dedicated ANSWERED, NOT RESOLVED band inside the attention area (s.4.1, s.6 borrowed from C2) | No band; "a reply alone does not close it"; D shows "Last relevant answer" per bundle (s.4 rule 3, s.8) | Medium |
| C-012 | Empty/healthy banner wording | Fixed banner set; realistic case prints "NO ATTENTION ITEMS OBSERVED. This is not an all-clear: coverage partial."; claim-only completions still listed (s.12, s.12.1) | "none observed" per section plus a mandatory closing line "NOT AN ALL-CLEAR FOR: hosts not reported, transitions between samples, and anything no source above can see." (s.7.2) | "NO WORK OBSERVED IN SCOPE; decision census unknown" and "This is not a fleet-wide all-clear"; empty collection and source failure get different banners (s.10) | Medium |
| C-013 | Stale/unavailable rendering | Body shrunk to one full row so the banner dominates; ages shown "if still open"; changes `n/a`; unreachable host named, its workers unknown (s.12.3) | Two-line FAIL banner; all last-known rows prefixed `~`; "NO VALID COMPARISON"; fleet `?` (s.7.3) | UNAVAILABLE banner; every last-known bundle shown in full under "not confirmed current"; ages continue from known creation; "Current item count unknown" (s.10) | Medium |
| C-014 | Verification-evidence ladder | Six evidence kinds as bracket tokens (`[claim]` .. `[human]`) (VER-2); wrong-revision checks make a `verify-gap` attention item rendered NOT VERIFIED (VER-3, s.12.4); claim-only reads `complete (claim only)` (VER-4) | Same six kinds as words (R-VER-05); REPORTED DONE, NOT ACCEPTED block splits `X` failing from `?` no current-revision result (s.7.4); stale revision shown as stale (R-VER-02) | Evidence record with kind/revision/result (s.3); four distinct labels for stale check, wrong-revision pass ("verification unknown: revision mismatch"), unavailable check and current-revision failure; absent provenance must not become an actionable failure (s.10, s.11) | High |
| C-015 | Delivery-state ladder | enq / dlv / proc / ans / res, each y/n/? (COM-2, s.9.1); person-seen excluded as not observable (s.15) | E / D / P / S / A / R including human-seen, S column `.` on every row today (R-COM-03, s.4.4, FG-4) | delivered, seen, answered, resolved kept distinct as a requirement (R05) but no ladder columns; "seen status unknown" in text (s.8) | Medium |
| C-016 | Overflow budget and placement | Per-section row budgets; `+N more:` with keys in at most two lines; footer `omitted:` totals per kind; busy target about 40 lines (OVF-1..OVF-8, s.13) | 60-line report budget; "+N more observed, not shown" plus one line of ids; printed arithmetic shown + omitted = observed (R-FMT-03, R-OVF-01, s.7.1) | At most six actionable bundles, 44-line target that yields to keeping whole bundles; omit whole lower-priority bundles; list omitted ids or the first omitted id with age; footer separates observed / shown / omitted / unobserved (s.4 rules 7-9) | Medium |
| C-017 | Question text handling | Original wording truncated with a marker, never paraphrased only (DEC-2); quoted as untrusted (COM-6) | Original text "shortened, not only a summary" (R-COM-01); control characters removed (R-COM-05) | Exact question; wrap rather than clip; "no question is shortened into an ambiguous instruction" (R03, R11, s.4 rule 10); secrets redacted (R16) | Medium |
| C-018 | Evaluation protocol | 10 tasks; pass thresholds "9 of 10 trials"; EV-1 median under 30 s; participant count not stated; counterbalanced (s.14) | 10 reader tasks plus 8 mechanical checks; at least 8 participants for a quantitative read; ET-1 median 15 s or less; critical-failure rules (s.9.1-9.3) | 7 tasks with 5 operators ("not statistical proof"); E01 within 20 s; any false all-clear in E02-E04 is a blocker; 12 contract cases (s.11) | Medium |
| C-019 | Feasibility-gate emphasis | G1-G8; failing a gate never blocks the default, only keeps labels partial (s.17); unique G7 storage durability | FG-1..FG-8; FG-8 non-consuming production is a ship blocker ("Cannot ship"); next step closes FG-1 and FG-8 first (s.12.1, s.12.3) | G01 is "the central feasibility gate"; unique G02 cursor enumeration consistency and G08 density decision (s.12) | Medium |
| C-020 | Synthetic-data and 80-column discipline | `SYNTHETIC DEMO DATA` title, DEMO ids, date 2026-01-01; 78-column content rule (s.1, FMT-2); measured max fenced line 77, 0 non-ASCII | `[DEMO]` title, rule "DEMO in every id" (s.2.1, R-INT-04, MC-7); 80-column limit (R-FMT-01); measured max fenced line 80, 0 non-ASCII | `SYNTHETIC DEMO` title, every id DEMO-prefixed; 80-column limit (s.1, R11); measured max fenced line 70, 0 non-ASCII | Low |

## Contradictions
| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Can a non-decision item outrank a waiting human decision at the top of the default? | No: human decisions first, oldest first, in every concept (DEC-1, s.3.1) | No: decision rows always above failures and changes (R-DEC-01, s.3.1) | Yes: a pinned verification contradiction (VERIFY BEFORE ACCEPTING, owner w-DEMO-2) sits above the human decision DEMO-D2, and source-backed severity may escalate an item above age order (s.4 rule 2, s.5, s.10) | High |
| X-002 | How are blocker-tree roots ranked? | By distinct tasks affected, then age (BLK-2, s.8.1) | By age of the root decision; shared task under the older root (s.2.4, s.4.3) | By oldest decision; impact ranking explicitly not allowed without a complete graph (s.4 rule 6, s.7) | High |
| X-003 | Does a message read that returns fewer than the 100-message cap prove a complete set? | Treated as covered: `msgs ok` when under cap; only a capped read is partial (COV-3, s.6.2, s.12.1) | Treated as non-partial: `msg-peek OK 22/100` shown without a partial marker (s.7.2) | No: "even fewer than 100 returned messages do not prove complete unresolved history"; the decision census stays unknown (s.3) | High |
| X-004 | May the report ever print an all-clear? | The default never prints one; the realistic empty case says "This is not an all-clear" (s.12, s.12.1) | Yes, conditionally: "all clear / healthy / none" permitted only when every source is OK and fully paged (R-INT-01, s.3.7) | Never fleet-wide: "This is not a fleet-wide all-clear" in every empty state (s.10) | Medium |
| X-005 | V1 internal: changes during a partial message read | CHG-2 says a partial or failed observation yields `n/a (no baseline)` deltas (s.3.4), yet the busy screen shows msgs CAPPED while listing decision deltas as NEW and ESCALATED (s.6.2) | n/a | n/a | Medium |
| X-006 | V1 internal: decisions-first ordering in non-default concepts | DEC-1 requires human decisions first in every concept (s.3.1), yet C prints VERIFY and FAILURE roots before UNROOTED decisions (s.8.2) and E's journal leads with non-decision entries (s.10.2) | n/a | n/a | Medium |
| X-007 | V2 internal: decisions-first ordering in non-default concepts | n/a | R-DEC-01 requires decision rows above failures (s.3.1), yet C3 draws ROOT 3 (a failure) before Q-DEMO-03 (s.4.3) and C5 places WORSE entries before STILL OPEN decisions (s.4.5) | n/a | Medium |
| X-008 | V2 internal: DEMO marker in every identifier | n/a | Rule "DEMO in every id" (s.2.1, R-INT-04, MC-7), yet ids `w-07` and `M-201` appear without DEMO in the screens (s.4, s.7) | n/a | Low |
| X-009 | V2 internal: shared-task marker on every row | n/a | s.2.4 says a shared task is marked "shared" in each row that shows it, yet the C1 row for Q-DEMO-01 lists the shared task without the marker (s.4.1) | n/a | Low |
| X-010 | V1 internal: DEMO marker in every identifier | The synthetic-data rule says identifiers use the `DEMO` marker and lists `w-07` as an example (s.1), yet `w-07` has no DEMO marker and is used as a requester in the screens (s.6.2, s.8.2, s.9.2, s.12.3) | n/a | n/a | Low |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 (opus:architect) | Four-layer architecture with an owns / must-never table, and a Layer column that ties every requirement to the layer that enforces it (s.2, s.3) | High |
| U-002 | V1 (opus:architect) | Mandatory `OLDEST` line in the shared frame of every concept, so the success criterion holds whichever concept is chosen (DEC-3, s.4.2) | High |
| U-003 | V1 (opus:architect) | TRAIL block in the Delta Journal that records collection failures between pastes (s.10.2) | Medium |
| U-004 | V1 (opus:architect) | VANISHED delta kind for an item that disappears without a resolution linkage (CHG-3) | Medium |
| U-005 | V1 (opus:architect) | Data-dependency table that names which sources each concept needs (s.11.2) | Medium |
| U-006 | V2 (sonnet:analyzer) | [E] / [P] / [G] evidence tags marking each claim as evidenced, proposed or gated (s.1) | Medium |
| U-007 | V2 (sonnet:analyzer) | Ball-Holder concept that groups items by who must move next (s.4.2) | High |
| U-008 | V2 (sonnet:analyzer) | Hybrid default with three named borrowed elements and a test-gated switch rule to C5 (s.6, s.9.3) | Medium |
| U-009 | V2 (sonnet:analyzer) | Mechanical checks MC-1..MC-8, separate from reader tasks (s.9.2) | Medium |
| U-010 | V2 (sonnet:analyzer) | Concept x state matrix naming the residual false-all-clear risk of each non-default concept (s.8) | High |
| U-011 | V2 (sonnet:analyzer) | Printed overflow arithmetic shown + omitted = observed, drawn on a dedicated overflow screen (R-OVF-01, s.7.1) | Medium |
| U-012 | V2 (sonnet:analyzer) | FG-8 makes non-consuming production a "Cannot ship" gate (s.12.1) | Medium |
| U-013 | V3 (haiku:backend) | Two-clock freshness, evidence older than 2 intervals counts as stale, and `clock conflict` for future timestamps (s.3, s.4 rule 1) | High |
| U-014 | V3 (haiku:backend) | Paging-integrity rules: repeated cursor tokens and a required terminal page before a census is complete (s.3) | High |
| U-015 | V3 (haiku:backend) | Partial observations may establish additions but never absence, resolution or negative movement; "newly observed" is not "newly created" (s.4 rules 4-5) | High |
| U-016 | V3 (haiku:backend) | Cycles in the blocker graph print `dependency conflict` instead of a tree (s.4 rule 6, s.7) | Medium |
| U-017 | V3 (haiku:backend) | Secret redaction in quoted question text (R16) | Medium |
| U-018 | V3 (haiku:backend) | Twelve deterministic future contract acceptance cases, plus G02 cursor-consistency gate (s.11, s.12) | Medium |

## Shared Assumptions
### Agreement table

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| 1 | V1 s.1/s.3 COV-3; V2 s.1, R-FLT; V3 s.3 | Non-consuming message reads are capped at 100 with no advertised paging | STATED | No |
| 2 | V1 DEC-1; V2 R-DEC-01; V3 s.4 rule 2 | Waiting decisions are ordered oldest first by default | STATED | No |
| 3 | V1 s.2 must-never; V2 s.1; V3 s.3 | The snapshot is read-only and never consumes or acknowledges messages | STATED | No |
| 4 | V1 G7; V2 FG-6; V3 G07 | A durable observation store for the last successful baseline is a feasibility gate | STATED | No |
| 5 | V1 G6; V2 FG-2; V3 G03 | An independent verification source is gated, not assumed | STATED | No |
| 6 | V1 FMT-1; V2 s.10 limit 8; V3 R11 | The chat client renders the fence in a monospace font | STATED | No |
| 7 | V1 s.6.1; V2 s.10 limit 6; V3 s.4 rule 2 | Age is the primary priority signal, absent a reliable impact source | STATED | No |
| 8 | V1 COM-4; V2 s.2.4; V3 R06 | Heartbeat or routine messages can be reliably told apart from decision requests | UNSTATED | Yes (A-001) |
| 9 | V1 s.6 "NEEDS YOU"; V2 C1/C2 HUMAN band; V3 s.5 Decision Brief | The person reading the chat is the acting owner of every human-required item | UNSTATED | Yes (A-002) |
| 10 | V1 s.13 (about 40 lines); V2 R-FMT-03 (60 lines); V3 s.4 rule 7 (44 lines) | One paste of 40-60 lines at 80 columns fits the chat platform's per-message limit with the fence intact | UNSTATED | Yes (A-003) |
| 11 | V1 s.4.1 as-of; V2 s.2.1 header; V3 s.3 two clocks | Readers read the latest paste near its as-of time and do not mistake an older paste in chat history for the current one | UNSTATED | Yes (A-004) |

### Promoted shared assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | [SHARED-ASSUMPTION] Heartbeat or routine messages are reliably distinguishable from decision requests at collection time | Row 8: all three suppress heartbeats (V1 COM-4, V2 s.2.4, V3 R06) without defining the classification rule or its failure mode | A misclassified decision is suppressed as noise, which is a silent false all-clear for that item | UNSTATED |
| A-002 | [SHARED-ASSUMPTION] The chat reader is the acting owner of all human-required items | Row 9: all three address the reader as the human actor (V1 s.6, V2 s.4.1-4.2, V3 s.5) without a per-person owner field | With several operators in one chat, items may be assumed handled by someone else | UNSTATED |
| A-003 | [SHARED-ASSUMPTION] A 40-60 line, 80-column paste fits the chat platform's per-message size limit and keeps the fence intact | Row 10: all three set line budgets (V1 s.13, V2 R-FMT-03, V3 s.4 rule 7) without naming a platform limit | A split or truncated paste can drop the footer that carries omitted and coverage counts | UNSTATED |
| A-004 | [SHARED-ASSUMPTION] Readers act on the latest paste near its as-of time and older pastes remain distinguishable | Row 11: all three rely on the as-of header (V1 s.4.1, V2 s.2.1, V3 s.3) without a reader-side staleness boundary | An older paste in history can be read as current, which reintroduces the stale-state risk the reports guard against | UNSTATED |

### Contradicted assumptions flagged for debate

- None. No agreement row is contradicted by a variant; the opposing positions found are recorded as contradictions X-001 to X-004 instead.

## Taxonomy Tags
| Diff Point | Level | Signal |
|------------|-------|--------|
| S-001 | L2 | organization |
| S-002 | L2 | architecture |
| S-003 | L2 | organization |
| S-004 | L2 | interface |
| S-005 | L2 | organization |
| S-006 | L3 | state |
| S-007 | L2 | component |
| S-008 | L2 | organization |
| S-009 | L2 | organization |
| S-010 | L2 | dependency |
| S-011 | L1 | notation / presentation |
| S-012 | L1 | formatting |
| C-001 | L2 | component |
| C-002 | L2 | component |
| C-003 | L2 | component |
| C-004 | L3 | invariant |
| C-005 | L3 | boundary |
| C-006 | L3 | state |
| C-007 | L3 | invariant |
| C-008 | L3 | guard |
| C-009 | L3 | state / transition |
| C-010 | L3 | transition |
| C-011 | L3 | state |
| C-012 | L3 | guard |
| C-013 | L3 | state |
| C-014 | L3 | validation rule |
| C-015 | L3 | state |
| C-016 | L3 | boundary |
| C-017 | L3 | boundary |
| C-018 | L2 | organization |
| C-019 | L2 | dependency |
| C-020 | L1 | formatting / naming |
| X-001 | L3 | invariant |
| X-002 | L3 | validation rule |
| X-003 | L3 | boundary |
| X-004 | L3 | guard |
| X-005 | L3 | state |
| X-006 | L3 | invariant |
| X-007 | L3 | invariant |
| X-008 | L1 | naming |
| X-009 | L1 | presentation |
| X-010 | L1 | naming |
| A-001 | L3 | validation rule |
| A-002 | L2 | interface |
| A-003 | L3 | boundary |
| A-004 | L3 | state |

## Similarity Check
- Comparable items considered: 64 (the 12 structural areas, the 20 content topics, the 4 cross-variant contradiction points and 28 further aligned points: the 7 requirement families, the 4 states, the 5 concept slots, the 8 gate slots and the 4 evaluation dimensions of task set, timing, participants and pass rule).
- Differences found: 42 (12 structural + 20 content + 10 contradictions).
- Ratio: 42 / 64, about 66%, which is far above the 10% threshold.
- Result: the variants are not near-duplicates; debate proceeds.

## Summary
- Total structural differences: 12
- Total content differences: 20
- Total contradictions: 10 (4 cross-variant: X-001 to X-004; 6 internal: V1 X-005, X-006, X-010 and V2 X-007, X-008, X-009; no internal contradiction found in V3)
- Total unique contributions: 18 (V1: 5, V2: 7, V3: 6)
- Total shared assumptions surfaced: 11 (UNSTATED: 4, STATED: 7, CONTRADICTED: 0); promoted: 4 (A-001 to A-004)
- Highest-severity items: S-002, C-001, C-002, C-004, C-005, C-007, C-009, C-014, X-001, X-002, X-003
