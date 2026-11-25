# Round 1 Statement: Variant 2 Advocate (sonnet:analyzer)

## Position Summary
V2 is the variant that can be checked: every claim carries an [E]/[P]/[G] tag (§1), every screen is drawn from one fixture table (§2.6), and every non-default concept is tested against four states in a concept x state matrix that admits its own gaps (§8). It should supply the merged spec's evidence discipline, fixture, overflow arithmetic, evaluation protocol and hybrid default; V1 should supply the layer model, frame and OLDEST line, and V3 the two-clock, paging and partial-observation integrity rules, where each is genuinely stronger.

## Steelman of Variant 1
V1 (opus:architect) is the best-structured spec. Its four-layer model (§2: collector adapters, observation store, derivation, frame+renderer) has an owns / must-never table, and each of its 39 requirements carries a Layer column (§3), so a reviewer can see which layer must enforce each rule and no rule is left floating. Its shared frame (§4.1-4.2) puts an `OLDEST` line, an as-of line and a printed legend footer into every concept (DEC-3), which means the seed brief's main success criterion, finding the oldest blocking decision, holds whichever concept wins. It labels unknown creation time `seen>=` (DEC-5), adds a `VANISHED` delta kind (CHG-3), ranks blocker roots by distinct tasks affected (BLK-2), and keeps a 78-column content rule with a measured maximum fenced line of 77 (FMT-2). It never prints an all-clear (§12). If a reader had to pick one document to build from, V1's skeleton is the most reusable.

## Steelman of Variant 3
V3 (haiku:backend) is the most rigorous about what the collector can and cannot know. Its two-clock freshness model, where evidence older than two intervals is stale and a future timestamp prints `clock conflict` (§3, §4 rule 1), and its paging-integrity rules (repeated cursor tokens, a required terminal page) are the only treatment of timestamp and cursor failure in the set. It states the key partial-observation principle: a partial read may establish additions but never absence, resolution or negative movement, and "newly observed" is not "newly created" (§4 rules 4-5). It is the only variant that rejects "fewer than 100 returned messages" as proof of completeness: "even fewer than 100 returned messages do not prove complete unresolved history" (§3). It prints `dependency conflict` for cycles (§4 rule 6, §7), redacts secrets in quoted questions (R16), has four distinct verification labels (§10, §11), a 70-column maximum line (the most margin), and no internal contradiction in the diff analysis. For a collector author, V3 is the safest base.

## Key Strengths Claimed
1. **Auditable evidence basis.** Every claim carries [E] evidenced, [P] proposed or [G] gated (§1), and the gated items map to FG-1..FG-8 (§12.1) with "closing evidence" and "concepts affected" columns. V1 and V3 have gate tables (G1-G8, G01-G08) but no per-claim tag, so a reader cannot tell which sentences are facts about Orca and which are design proposals.
2. **One fixture world used by every screen.** The fixture table (§2.6) fixes ages, links and the shared task once, and all five screens (§4.1-4.5) and the four states (§7.1-7.4) are drawn from it. V1 only implies a fixture by reusing D-DEMO-00xx keys (diff S-005) and V3 has a short prose fixture (§1). A shared fixture is what makes the comparison matrix fair.
3. **Five distinct concepts, honestly compared.** C1-C5 ("5Q") differ in layout (ledger §4.1, bands §4.2, tree §4.3, ladder grid §4.4, changed/carried split §4.5), and the matrix (§5) counts busy-screen lines (27/26/24/25/21) and rates "gate load", rather than only assigning +/o/-. V3's D1, F1 and D2 bundles repeat almost verbatim across four screens (diff C-002).
4. **A concept that answers a question the others do not.** C2 Ball-Holder Board groups by who must move next (HUMAN / COORDINATOR / WORKER / NOBODY KNOWN, §4.2), which is the responsibility axis the operator actually asks for; V1's Control Board is location (run x lane) and V3's Run Ledger is run ownership (diff C-001).
5. **Concept x state matrix with the admitted gap.** §8 does not claim all five concepts are safe. It names the residual false-all-clear risk of C2-C5 and admits the C4/C5 gap, where V1 and V3 give a one-paragraph "state handling" per concept (diff S-006).
6. **Overflow is demonstrated, not only specified.** §7.1 draws 19 decisions with the printed arithmetic "shown + omitted = observed" (R-OVF-01), and R-FMT-03 sets a 60-line budget. V1 shows overflow as `+3 more:` inside a busy screen (§6.2) and V3 has no overflow screen (diff S-007), so neither lets a reviewer check the arithmetic.
7. **Visible suppression of heartbeats.** A worker appears only when silence crosses a printed threshold, via a WATCH row (§2.4, §4.1; 15m placeholder, §10 limit 7), so suppression is visible in the paste. This is the best available answer to A-001.
8. **Answered is not resolved.** The ANSWERED, NOT RESOLVED band (§4.1, borrowed from C2 in §6) keeps a replied-to decision in sight until a resolution linkage exists. V1 pushes it into the FLEET line, and V3 has no band (diff C-011).
9. **Evaluation protocol that can fail the design.** Reader tasks ET-1..ET-10 (§9.1) are separate from mechanical checks MC-1..MC-8 (§9.2) and a decision rule (§9.3: switch to C5 if ET-1 ties and ET-6 recall is higher), with at least 8 participants for a quantitative read and critical-failure rules. V1 does not state a participant count (diff C-018); V3 says "not statistical proof".
10. **Honest ship gate.** FG-8 makes non-consuming production a "Cannot ship" gate (§12.1), and §12.3 names FG-1 and FG-8 as the first closures. V1 states that failing a gate never blocks the default (diff C-019), so none of its gates can stop shipping.
11. **Decisions-first as a stated rule.** R-DEC-01 puts decision rows above failures and changes (§3.1), so a pinned non-decision cannot displace a waiting human decision (X-001). V3 permits the opposite.

## Weaknesses Identified in Other Variants
1. **V3 allows a non-decision item to outrank a waiting human decision (X-001).** V3's pinned "VERIFY BEFORE ACCEPTING" (owner w-DEMO-2) sits above decision DEMO-D2, and "source-backed severity may escalate an item above age order" (§4 rule 2, §5, §10). The seed brief's primary success criterion is finding the oldest blocking decision, and this rule makes that answer depend on severity data the spec elsewhere calls gated.
2. **V3's concepts are near-duplicates.** Four of five screens repeat the D1, F1 and D2 bundles almost verbatim (§5, §8, §9, §10), and V3 itself says the concepts "share truth rules, not a common dashboard" (§1). That leaves the evaluation (§11) with fewer genuinely different designs to compare than V1 or V2 offer.
3. **V3 has no comparison matrix and no overflow screen.** Its comparison is one paragraph (§10) and its overflow is prose (§4 rules 7-9, one paragraph in §10, one acceptance case in §11). The 44-line target "yields to keeping whole bundles", so the budget is not a hard line (diff C-016).
4. **V1 contradicts its own baseline rule (X-005).** CHG-2 says a partial or failed observation yields `n/a (no baseline)` (§3.4), but the busy screen shows msgs CAPPED while listing decision deltas as NEW and ESCALATED (§6.2). The screens the spec uses to demonstrate the rule break it.
5. **V1 breaks decisions-first in its non-default concepts (X-006).** DEC-1 (§3.1) says human decisions come first in every concept, but C prints VERIFY and FAILURE roots before UNROOTED decisions (§8.2) and E's journal leads with non-decision entries (§10.2).
6. **V1 treats a read under the cap as covered (X-003).** `msgs ok 37<100cap` (§6.2, COV-3, §12.1) marks a message read as complete when fewer than 100 rows came back. V2 has the same blind spot in one screen (see Concessions), but V1 builds it into a requirement.
7. **V1 lacks DEMO in `w-07` (X-010).** The synthetic-data rule lists `w-07` as an example id (§1) yet it is used without the DEMO marker as a requester (§6.2, §8.2, §9.2, §12.3).
8. **V3 ranks roots by age only.** §4 rule 6 and §7 forbid impact ranking without a complete graph, so a root blocking four tasks can sort below a root blocking one. V2 also ranks by age (§2.4, §4.3) and accepts this cost for now; it is a cost, not a strength, and V1's distinct-task ranking (BLK-2) is the better long-run rule once the graph is complete.

## Concessions
1. **Decisions-first is violated in V2's own non-default screens (X-007).** R-DEC-01 (§3.1) requires decision rows above failures, yet C3 draws ROOT 3 (a failure) before Q-DEMO-03 (§4.3) and C5 places WORSE entries before STILL OPEN decisions (§4.5). V3 has no such contradiction, because its rule and its screens agree, even though I reject the rule itself (X-001).
2. **DEMO marker misses (X-008).** The rule "DEMO in every id" (§2.1, R-INT-04, MC-7) is broken by `w-07` and `M-201` in the screens (§4, §7). V2's own mechanical check MC-7 would fail on its own document.
3. **Shared-task marker miss (X-009).** §2.4 says a shared task is marked "shared" in each row that shows it, but the C1 row for Q-DEMO-01 lists the shared task without the marker (§4.1). V1 has no such miss.
4. **Same under-cap blind spot as V1 (X-003).** `msg-peek OK 22/100` is shown with no partial marker (§7.2). A read of 22 of a possible 100 is not proof of a complete set, and V3's rule (§3) is correct.
5. **No `seen>=` fallback (C-005).** Age is always from original creation (§2.3, R-DEC-02) and no fallback is specified when creation time is absent. V1's DEC-5 and V3's `observed >=Nm` (§4 rule 1) both handle this.
6. **No VANISHED kind (C-010) and no OLDEST pointer outside C1 (C-004).** Only a resolution linkage removes a row (R-DEC-05), and C5 is rated "Weak: lives in lower block" (§5). Outside the default, the seed brief's main question depends on the reader scanning.
7. **No layer model (S-002).** The read model is one sentence marked [P] and "not specified here" (§6). V1's §2 is a real contribution V2 lacks.
8. **No printed legend or footer contract (S-004, S-011).** The symbol table (§2.2) is not printed in reports except the C4 ladder legend, and R-INT-05's fixed summary line was added late as a "common repair" (§8). The C4 and C5 mockups lack that summary line.
9. **No two-clock freshness, cursor-integrity, cycle or redaction rules (U-013..U-017).** V3 covers these and V2 does not.
10. **80-column maximum with zero margin (A-003).** V2's longest fenced line is exactly 80 columns, the most exposed of the three (V1 77, V3 70), and §12.2 Q7 says "No chat client was tested".
11. **Arbitrary thresholds.** The 15m silence placeholder (§10 limit 7) and ET-1 median of 15 s or less (§9.3) are chosen, not derived.
12. **Conditional all-clear is riskier than a never-print policy (X-004).** R-INT-01 (§3.7) permits "all clear / healthy / none" when every source is OK and fully paged. The conditions are testable, but a paste whose conditions silently fail prints a false all-clear, and V1 and V3 cannot.

## Shared Assumption Responses
- **A-001: QUALIFY.** Heartbeat versus decision classification is undefined in all three variants (V1 COM-4, V2 §2.4, V3 R06), and a misclassified decision becomes a silent false all-clear. V2 makes suppression visible: a worker is listed only when silence crosses a printed threshold (§2.4, §4.1), and counts such as "31 messages seen*, 0 shown" keep the suppressed volume on the page. The assumption holds only when the classifier is named and its misses are countable; V2 does not define the rule either, so it is not fully correct.
- **A-002: QUALIFY.** All three address the reader as the human actor. Partial mitigations exist: V3 names an owner (`human-DEMO-op`, §5), and V2 has an acting-owner field and a C2 "Use when" note about several humans (§4.2). V1 leaves the owner as `human` (§6). The assumption is valid for one operator in one chat and fails for several; no variant has a per-person assignment.
- **A-003: QUALIFY.** No platform limit is named anywhere. V1 (about 40 lines, max column 77), V3 (44 lines, max 70) have margin; V2 (60 lines, max exactly 80) has none and admits "No chat client was tested" (§12.2 Q7). A 60-line paste is the most likely to be split, and a split drops the footer that carries omitted and coverage counts.
- **A-004: QUALIFY.** As-of and prev-ok fields exist in all three (V1 §4.1, V2 §2.1, V3 §3). V1's window and TRAIL help a late reader (§10.2). No variant defines a paste sequence number or a reader-side staleness boundary, so an older paste in history can still be read as current.

## Per-Point Verdict Table

| Point | Superior | Reason (one line, with a section citation) |
|-------|----------|--------------------------------------------|
| S-001 | V2 | Fixture and shared contract come before requirements (§2) and a concept x state matrix closes the concepts (§8), so the order supports checking. |
| S-002 | V1 | Four-layer model with an owns / must-never table and a Layer column (V1 §2, §3); V2 only says "not specified here" (V2 §6). |
| S-003 | V2 | Basis column ties each of 40 IDs to the seed brief or REPORT.md section (V2 §3.1-3.7), which is more traceable than V3's R01-R16. |
| S-004 | V1 | Dedicated frame section with a field-to-requirement table covers header and footer (V1 §4.1-4.2). |
| S-005 | V2 | Explicit fixture-world table with ages, links and the shared task, reused by all screens (V2 §2.6). |
| S-006 | V2 | All four states drawn for C1 (V2 §7.1-7.4) plus a matrix naming residual risk for C2-C5 (V2 §8). |
| S-007 | V2 | Dedicated overflow screen with 19 decisions and printed arithmetic (V2 §7.1, R-OVF-01). |
| S-008 | V2 | Matrix counts busy-screen lines (27/26/24/25/21) and rates gate load (V2 §5); V3 has only a paragraph (V3 §10). |
| S-009 | V2 | Reader tasks, mechanical checks and a decision rule are separated (V2 §9.1-9.3). |
| S-010 | V2 | FG table has closing evidence and concepts affected, plus a next step (V2 §12.1, §12.3). |
| S-011 | V1 | Token legend defined and printed as a footer in every report (V1 §4.1, §4.3). |
| S-012 | V1 | Fixed 5-line frame with `===` and `---` separators gives one grammar across concepts (V1 §4.1, §6.2). |
| C-001 | V2 | Ball-Holder bands (HUMAN / COORDINATOR / WORKER / NOBODY KNOWN) use the responsibility axis the operator asks about (V2 §4.2). |
| C-002 | V2 | Five layouts that differ (V2 §4.1-4.5); V1 is close (V1 §6-10) and V3 repeats D1/F1/D2 (V3 §5, §8-10). |
| C-003 | V2 | Hybrid default with three named borrowings and a test-gated switch rule (V2 §6, §9.3). |
| C-004 | V1 | `OLDEST` line is mandatory in every concept, so the main success criterion holds whichever wins (V1 DEC-3, §4.2). |
| C-005 | V3 | `observed >=Nm`, a visible "cannot certify oldest" warning and `clock conflict` for future times (V3 §4 rule 1). |
| C-006 | V1 | Consistent `>=N observed`, `0 observed (partial)` and `N covered of ? expected` (V1 DEC-4, OVF-7, COV-2). |
| C-007 | V3 | Shared tasks counted once in a UNION footer and cycles print `dependency conflict` (V3 §4 rule 6, §7). |
| C-008 | V2 | Heartbeats collapse to a last-seen and a WATCH row appears only past a printed silence threshold (V2 §2.4, §4.1). |
| C-009 | V3 | Per-source last-success pointers; partial may add but never prove absence or resolution (V3 §4 rules 4-5). |
| C-010 | V1 | Explicit VANISHED kind keeps the item open (V1 CHG-3, DEC-6). |
| C-011 | V2 | ANSWERED, NOT RESOLVED band keeps replied-to decisions visible (V2 §4.1, §6). |
| C-012 | V2 | Closing line "NOT AN ALL-CLEAR FOR: hosts not reported, transitions between samples..." names what is unseen (V2 §7.2). |
| C-013 | V2 | `~` on every last-known row, two-line FAIL banner and "NO VALID COMPARISON" (V2 §7.3). |
| C-014 | V3 | Four distinct verification labels and absent provenance never becomes an actionable failure (V3 §10, §11). |
| C-015 | V2 | E / D / P / S / A / R ladder with a visible S column and FG-4 gate (V2 §4.4, R-COM-03). |
| C-016 | V2 | Hard 60-line budget and printed shown + omitted = observed (V2 R-FMT-03, R-OVF-01, §7.1). |
| C-017 | V3 | Wraps rather than clips the exact question and redacts secrets (V3 R03, R11, R16, §4 rule 10). |
| C-018 | V2 | At least 8 participants, ET-1 threshold, critical-failure rules and mechanical checks (V2 §9.1-9.3). |
| C-019 | V2 | FG-8 non-consuming production is "Cannot ship" and the next step closes FG-1 and FG-8 (V2 §12.1, §12.3). |
| C-020 | V1 | Explicit 78-column content rule with measured max 77, `SYNTHETIC DEMO DATA` title and fixed date (V1 §1, FMT-2). |
| X-001 | V2 | Decision rows always above failures and changes (V2 R-DEC-01, §3.1); V1 DEC-1 agrees, V3 §4 rule 2 and §10 do not. |
| X-002 | V3 | Age-only ranking is safe while the graph is incomplete and impact ranking is disallowed without it (V3 §4 rule 6, §7). |
| X-003 | V3 | Fewer than 100 returned messages do not prove completeness (V3 §3); V1 COV-3 and V2 §7.2 treat it as covered. |
| X-004 | V1 | Never prints an all-clear, so a silent failure cannot produce one (V1 §12, §12.1); V2 R-INT-01 is conditional. |
| X-005 | V3 | Partial reads may add NEW items but never prove absence, which resolves V1's CAPPED-with-deltas screen (V3 §4 rules 4-5). |
| X-006 | V3 | V3's rule and its screens agree, so there is no internal ordering contradiction (V3 §4 rule 2, §5-10). |
| X-007 | V3 | V3's screens follow its own ordering rule, unlike V2's C3 and C5 (V3 §5-10; V2 §4.3, §4.5). |
| X-008 | V3 | Every V3 id carries the DEMO prefix (V3 §1), unlike V2's `w-07` and `M-201` (V2 §4, §7). |
| X-009 | V1 | V1 makes no shared-task marker promise it fails to keep, unlike V2 (V2 §2.4 vs §4.1); V1 uses `see [n]` (V1 BLK-3, §8.1). |
| X-010 | V3 | V3 prefixes every id with DEMO, so it has no `w-07` miss (V3 §1; V1 §1, §6.2). |
| A-001 | V2 | Printed silence threshold and seen/shown counts make suppression visible, though the classifier is undefined (V2 §2.4, §4.1). |
| A-002 | V3 | Names an owner (`human-DEMO-op`), the closest to a per-person field (V3 §5). |
| A-003 | V3 | Max line 70 and 44 lines leave the most margin against a message limit (V3 §4 rule 7, §1). |
| A-004 | V1 | Window and TRAIL help a late reader place an older paste (V1 §4.1, §10.2). |
