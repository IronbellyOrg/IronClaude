# Round 2 Rebuttal: Variant 2 Advocate (sonnet:analyzer)

## Response to Criticisms

Line numbers are for `variant-1-opus-architect.md` (V1), `variant-2-sonnet-analyzer.md` (V2) and `variant-3-haiku-backend.md` (V3). I re-opened all three files for this round and re-checked every number below. Where a Round 1 citation of mine was wrong, the correction is under New Evidence.

**CR-1. `msg-peek OK 22/100` treats an under-cap read as complete (X-003; V3 W1, V1 CR-3).** Conceded. V2 §7.2 prints `msg-peek OK 22/100` (V2 l.583) beside "NEEDS YOU none observed" (l.586), and the rule text allows that wording "because every source is OK and read below its cap" (l.596-598). V3 is right that a short read does not prove a complete unresolved history (V3 l.66).
- Mitigation, offered as a limit and not a defence: the same screen carries "NOT AN ALL-CLEAR FOR" (l.592-593) and says the wording stays "observed" until FG-1 is closed (l.597-598).
- The repair is V3's census-unknown wording plus `ok N/100, census ?` in the token.

**CR-2. R-INT-01 contradicts V2's own §7.2 (new, found while re-reading).** Conceded. R-INT-01 (V2 l.201) gives "none observed" as the wording when a source is not fully paged. §7.2 allows "none observed" only when sources are OK and below the cap (l.596-598), and uses "none seen in the part read: PARTIAL*" for partial sources (l.599-601). One of the two rules must change. I propose that "none observed" is only permitted under gate FG-1, and until then V3's "decision census unknown" applies.

**CR-3. Conditional all-clear (X-004; V1 R1 W4, V1 R2 Updated Assessment).** Conceded in part. R-INT-01 (l.201) is conditional, and MC-4 (l.717) checks the condition mechanically. V1's COV-4 (V1 l.128) has the same shape, so this is not a V1 advantage. V3 never goes fleet-wide (V3 §10, l.298-311), and that is the safer rule. X-004 moves to V3.

**CR-4. Decisions-first broken in C3 and C5 (X-007; V1 R1, V3 R1).** Conceded. R-DEC-01 (V2 l.136) puts decision rows above failures. The C3 mockup draws a failure root before Q-DEMO-03, and C5 puts WORSE before STILL OPEN decisions (§4.3 l.322-346, §4.5 l.409-430). C5 has no oldest pointer at all, and the §5 matrix says so ("Weak"). The repair is V1's mandatory OLDEST line (DEC-3, V1 l.73; frame V1 l.154). C-004 stays with V1.

**CR-5. DEMO marker missing on `w-07` and `M-201` (X-008; V1 R1 W7).** Conceded. §2.1 says "DEMO in every id" (V2 l.62), R-INT-04 repeats it (l.204) and MC-7 checks it (l.720). `w-07` appears at l.112, l.234, l.327 and other rows, and `M-201` at l.559. V2's own MC-7 would fail on V2's mockups. V1 has the same flaw with `w-07` (X-010), so this is a draw, not a V2 advantage.

**CR-6. Shared-task marker (X-009).** Conceded. §2.4 says a task blocked by two decisions is marked "shared" in each decision's row (V2 l.91-92). The C1 row for Q-DEMO-01 reads "holds 4 (1 direct, 3 indirect)" with no marker (l.235), while the Q-DEMO-02 row has "shared with Q-DEMO-01" (l.237). The marker is in one of the two rows. V3's repeated `also under <ID>` plus a UNION footer (V3 rule 6, l.77) keeps the promise in both rows and is tested in V3's contract cases. X-009 moves to V3.

**CR-7. "All five carry these" overclaim (V3 W6).** Conceded. §5 says "All five carry these in the busy state" (V2 l.466-467), then lists known misses (l.468-470), and says the by-eye check is "not a conformance test" (l.470). §8 admits C4 and C5 lack the fixed failing/unverified summary (l.671-679). The merged spec should carry the requirements, not the broader conformance wording. The by-eye check, as written, over-reaches its own method.

**CR-8. Owner field names the relay (V3 W5).** Conceded. `w-07 > coord` (V2 l.234) names the requester and the relay, not the human who has to answer. V2 admits ownership is inferred (§4.2, l.308-310), but the mockup still hides the acting human. V3's acting-owner/requester split with unknown left unknown (V3 l.60) should govern the field.

**CR-9. No cursor-integrity or moving-dataset semantics (V3 W7).** Conceded. V2 §2.1 and §3.6 require coverage reporting but say nothing about repeated cursor tokens, and nothing about a moving dataset. V3 l.64 ("Cursor exhaustion alone does not prove a point-in-time census") and gate G02 (V3 l.462-469) fill that gap.

**CR-10. No creation-time fallback, no printed legend, no layer model (S-002, S-004, S-011, C-005; V1 R1).** Conceded.
- Age is always from creation (R-ROW l.77-82; R-DEC-02 l.137), and no fallback is named. V1 DEC-5 (V1 l.77) and V3 rule 1 (V3 l.72) are better.
- The symbol table (§2.2, l.63-75) is not printed in reports. V1 §4 prints a legend footer.
- The read model is one sentence, "not specified here" (V2 l.536-537). V1 §2 (V1 l.25-55) is a real model.

**CR-11. 80-column zero margin and no tested client (A-003; V1 R2 NE-6, V3 W6).** Conceded. V2's rule lines are exactly 80 characters, V1's maximum is 77 and V3's is 70. §12.2 Q7 says "No chat client was tested" (V2 l.816-817). MC-1 and MC-2 check width and line count only, not message size. V1's EV-10 (V1 l.704) is the same kind of check. The 60-line budget (R-FMT-03, l.198) is untested.

**CR-12. "(by timestamp)" names no clock (§7.3).** Conceded. §7.3 says "(by timestamp)" (V2 l.613) without saying which clock, while the age-from-creation note sits two screens later (l.626-628). V1's "if open" wording and V3's two clocks (V3 l.48) are clearer.

**What I hold.**
- The WATCH row. V1 R2 credits it (V2 l.251; threshold §2.4, l.84-94). Visible suppression of heartbeat silence is in the default, while V1's QUIET count is in concept D only.
- The shared fixture (§2.6, l.104-125), which every screen is drawn from. V1 and V3 both concede it.
- The dedicated 19-decision overflow screen with printed arithmetic (§7.1, l.552-572, "shown 3 + omitted 16 = 19*" at l.562). V1 concedes the missing screen (V1 R2 CR-7), and V3 has words only.
- The concept x state matrix and the by-name admission of residual risk (§8, l.664-679).
- The ET/MC split and decision rule (§9, l.697-728), and the FG-8 "Cannot ship" gate (l.798). V1 concedes both (V1 R2 CR-8, CR-9).
- The hybrid default with three named borrowings and a switch condition tied to ET-1 and ET-6 (§6, l.487-491, l.529-532).

## Updated Assessment

V2 is the review and validation surface of the three. It is not the skeleton and it is not the data contract.
- The skeleton is V1 (layers, frame, OLDEST, legend).
- The data contract is V3 (two clocks, cursor integrity, positive-only partial deltas, census-unknown, candidate-question semantics).
- V2 supplies the fixture, the drawn overflow screen, the WATCH row, the ANSWERED NOT RESOLVED band, the evaluation split, the ship gate and the [E]/[P]/[G] tags.

After the concessions above, my votes moved on eight points: C-006 (V1 to V3), C-012 (V2 to V3), C-015 (V2 to V1), C-020 (V1 to V3), X-004 (V1 to V3), X-009 (V1 to V3), A-001 (V2 to V3) and A-004 (V1 to V3). Five of these move toward V3, which matches V1's own movement. I did not move on points where V1 or V3 simply voted against me without new evidence (for example S-003, S-008, S-009, C-001, C-016).

**Merge consequence.**
- V2's mockups need repair against R-DEC-01, R-INT-04 and §2.4 before they are used as a reference.
- V2's under-cap wording needs V3's census-unknown wording.
- Fixing V2's own R-INT-01 versus §7.2 conflict is a precondition for using R-INT-01 in a merged spec.

## New Evidence

**NE-1. Round 1 citation correction: the V1 under-cap flaw is not in COV-3.** My Round 1 attributed it to COV-3. COV-3 (V1 l.127) only requires markers for failed, capped or stale sources. The flaw is in OVF-7 (V1 l.684: only a capped read, rows equal to the cap, marks counts `>=N`) and the token `msgs ok 37<100cap` (V1 l.584). V1 mitigates it in the same screen with `0 observed (partial ...)` (V1 l.587), "NOT an all-clear: coverage partial" (l.599) and the rule at l.576, and V1's own R2 (CR-3) agrees with this correction. V2 has the same class of flaw in `msg-peek OK 22/100` (V2 l.583), with the same mitigations (l.592-593, l.597-598).

**NE-2. Round 1 wording correction: E's journal does not lead with non-decision entries.** My Round 1 said "E's journal leads with non-decision entries". That is wrong. THIS WINDOW opens with three decision entries: NEW (V1 l.484), ESCALATED (l.485) and AGED (l.486). The accurate statement: non-decisions interleave below them. A VERIFY-GAP (l.487) sits above the VANISHED decision (l.489), and in STILL OPEN `F T-DEMO-B2` (l.494) sits above D-DEMO-0051 (l.495). X-006 stays a V1 internal contradiction on the strength of concept C (V1 §8.2) and this interleaving, and V1 R2 (CR-2) agrees.

**NE-3. Round 1 citation correction: TRAIL and DEC-5.** TRAIL exists only in concept E (V1 §10.2, l.499-502), not in the default frame. I used it in Round 1 as an A-004 mitigation for V1. Because it is not in the default, that credit is withdrawn (A-004 moves to V3). DEC-5 is in V1 §3.1 at l.77 (`seen>=`), not in a later section.

**NE-4. Other Round 1 cites re-checked and correct.** V2 §5 busy line counts 27/26/24/25/21 and quiet 13 (V2 l.449-461, counted against §4.1-4.5 at l.226-254, l.278-304, l.322-346, l.364-389, l.409-430); V2 §7.2 (l.581-601); V2 §10 limit 7 (l.754); V2 §12.1 FG-8 (l.798); V2 §12.2 Q7 (l.816-817). V1 OVF-8 "about 40 lines" is at V1 l.685.

**NE-5. V3 also has a gap of the kind it criticizes.** V3's empty screen asserts "Missing in-scope hosts: none" for a named scope, although its own gate G04 admits there is no host inventory (V3 §12, l.462-469). I state this cautiously, because the scope in V3's fixture is named, but the assertion is only as good as that named scope.

**NE-6. V3 has no drawn overflow screen and no printed legend.** Overflow is covered in words (V3 l.340) and the W/M/V codes are defined in prose (V3 §4). This supports S-007 and S-011 as already voted.

## Shared Assumption Responses

- **A-001: QUALIFY (superior moves from V2 to V3).** Suppression is safe only for positively identified routine traffic. V2's printed silence threshold (WATCH row, V2 l.251; §2.4) makes silence visible but does not classify anything (R-COM-04, l.159). V3's candidate-question rule (V3 l.60) keeps an ambiguous message on the page as a candidate with uncertain identity, which is the safer default. The merge should take V3's rule and V2's WATCH row. No variant defines the classifier itself.
- **A-002: QUALIFY.** `NEEDS YOU` is not an assignment or an acknowledgement. Ownership is inferred (V2 §4.2, l.308-310), and V2's `w-07 > coord` names the relay, not the human (CR-8). The assumption holds for one operator in one chat and fails for several. V3's acting-owner and requester split with an unknown fallback (V3 l.60) is the right data rule.
- **A-003: QUALIFY.** No platform limit is named anywhere. V2's 60-line budget (R-FMT-03, l.198) and exactly-80-column lines are untested (Q7, l.816-817). V1's about-40-line target is "not a measured constraint" (V1 l.685), and V3's 44-line target yields to whole bundles (V3 l.78). A split paste drops the footer that carries omitted and coverage counts.
- **A-004: QUALIFY.** An as-of timestamp does not prove freshness at read time. V2's header and R-CHG rules give times but no reader-side boundary (§2.1 l.52-61; §10 limit 2). V1's TRAIL is concept E only (NE-3). V3's two clocks (V3 l.48) are the strongest treatment, but no variant has a paste sequence number or a "recheck before acting" marker.

## Per-Point Verdict Table

| Point | Superior | Reason (one line, with a section citation) |
|-------|----------|--------------------------------------------|
| S-001 | V2 | Fixture and shared contract precede requirements (V2 §2) and a concept x state matrix closes the concepts (V2 §8). |
| S-002 | V1 | Four-layer model with owns / must-never table; V2 only says "not specified here" (V1 §2; V2 §6, l.536-537). |
| S-003 | V2 | Basis column ties each of 40 IDs to the seed brief or REPORT.md (V2 §3.1-3.7); V1 Layer column is a close second. |
| S-004 | V1 | Dedicated frame section with a field-to-requirement table and a printed footer (V1 §4.1-4.2). |
| S-005 | V2 | Explicit fixture-world table reused by every screen (V2 §2.6, l.104-125). |
| S-006 | V2 | All four states drawn for C1 plus a matrix naming residual risk for C2-C5 (V2 §7.1-7.4, §8). |
| S-007 | V2 | Only drawn overflow screen with printed arithmetic, 3 + 16 = 19 (V2 §7.1, l.562). |
| S-008 | V2 | Matrix counts busy-screen lines 27/26/24/25/21 and rates gate load, though its by-eye check over-reaches (V2 §5, l.449-470). |
| S-009 | V2 | Reader tasks ET-1..ET-10, checks MC-1..MC-8 and a decision rule are separate (V2 §9.1-9.3, l.697-728). |
| S-010 | V2 | Gates carry closing evidence, concepts affected and a next step (V2 §12.1, §12.3). |
| S-011 | V1 | Legend defined and printed as a footer in every report; V2 prints none (V1 §4.1-4.3; V2 §2.2). |
| S-012 | V1 | One fixed frame grammar across all five concepts (V1 §4.1, §6.2). |
| C-001 | V2 | Ball-Holder bands use the responsibility axis the operator asks about (V2 §4.2, l.278-304). |
| C-002 | V2 | Five layouts that differ (V2 §4.1-4.5); V1 is close (V1 §6-10) and V3 repeats D1/F1/D2 (V3 §5, §8-10). |
| C-003 | V2 | Hybrid default with three named borrowings and a test-gated switch rule (V2 §6, §9.3). |
| C-004 | V1 | Mandatory OLDEST frame line holds in every concept, the repair for V2's C3/C5 (V1 DEC-3, §4.2). |
| C-005 | V3 | `observed >=Nm`, an oldest-not-certified warning and `clock conflict` (V3 §4 rule 1). |
| C-006 | V3 | "Decision census unknown" holds below the cap; V1 OVF-7 marks `>=N` only at the cap (V3 §3; V1 OVF-7) (changed from V1). |
| C-007 | V3 | Age-ranked roots, UNION counts and `dependency conflict` work on a partial graph (V3 §4 rule 6, §7). |
| C-008 | V2 | Printed-threshold WATCH row in the default; V1's QUIET count is concept D only (V2 §2.4, §4.1; V1 §9.2). |
| C-009 | V3 | Per-source and per-scope baselines; partial reads add but never prove absence (V3 §4 rules 4-5). |
| C-010 | V1 | VANISHED is an explicit, testable delta kind kept open, with the capped-read qualifier added (V1 CHG-3, DEC-6). |
| C-011 | V2 | ANSWERED, NOT RESOLVED band keeps replied-to decisions in the attention area (V2 §4.1, §6). |
| C-012 | V3 | "NO WORK OBSERVED IN SCOPE; decision census unknown" names the gap V2's `msg-peek OK 22/100` hides (V3 §10; V2 §7.2) (changed from V2). |
| C-013 | V2 | `~` on every last-known row, two-line FAIL banner and "NO VALID COMPARISON" (V2 §7.3, l.606-624). |
| C-014 | V3 | Four distinct verification labels; absent provenance never becomes an actionable failure (V3 §10, §11). |
| C-015 | V1 | y/n/? ladder without a permanently empty human-seen column, plus `unavailable (would consume)` (V1 COM-2, COM-5; V2 §4.4, FG-4) (changed from V2). |
| C-016 | V2 | Hard 60-line budget with printed shown + omitted = observed, demonstrated (V2 R-FMT-03, R-OVF-01, §7.1). |
| C-017 | V3 | Wraps rather than clips, escapes control sequences and redacts secrets (V3 R03, R11, R16, §4 rule 10). |
| C-018 | V2 | At least 8 participants, ET-1 threshold, critical-failure rules and mechanical checks (V2 §9.1-9.3). |
| C-019 | V2 | FG-8 non-consuming production is "Cannot ship"; V1's gates never block (V2 §12.1, l.798; V1 §17). |
| C-020 | V3 | Every id DEMO-prefixed and the longest fenced line is 70; V1 `w-07` and V2 `w-07`/`M-201` break the rule (V3 §1; V1 §1; V2 §2.1) (changed from V1). |
| X-001 | V2 | Decision rows always above failures and changes in the default; V3 pins a verification item above DEMO-D2 (V2 R-DEC-01, §3.1; V3 §4 rule 2, §5). |
| X-002 | V3 | Age-only ranking is safe while the graph is incomplete; impact ranking needs a complete graph (V3 §4 rule 6, §7). |
| X-003 | V3 | Fewer than 100 returned messages do not prove completeness (V3 §3, l.66); V1 OVF-7 and V2 §7.2 both fall short. |
| X-004 | V3 | Never fleet-wide in any empty state; V1 COV-4 and V2 R-INT-01 are both conditional (V3 §10; V1 COV-4; V2 R-INT-01) (changed from V1). |
| X-005 | V3 | Partial reads may add NEW items but not absence, which resolves V1's CAPPED-with-deltas screen (V3 §4 rules 4-5; V1 CHG-2, §6.2). |
| X-006 | V3 | V3's rule and screens agree; V1's concept C puts VERIFY and FAILURE above decisions (V3 §4 rule 2, §5-10; V1 §8.2, §10.2). |
| X-007 | V3 | V3's screens follow its own ordering rule, unlike V2's C3 and C5 (V3 §5-10; V2 §4.3, §4.5). |
| X-008 | V3 | Every V3 id carries DEMO, unlike V2's `w-07` and `M-201` (V3 §1; V2 §2.1, §4.1, §7.1). |
| X-009 | V3 | UNION footer and `also under <ID>` on each row keep the shared-task promise V2 §4.1 misses (V3 §4 rule 6; V2 §2.4, l.235) (changed from V1). |
| X-010 | V3 | V3 prefixes every id with DEMO, so it has no `w-07` miss (V3 §1; V1 §1, §6.2). |
| A-001 | V3 | Candidate-question and uncertain-identity rule keeps ambiguous messages visible; V2's WATCH row only shows silence (V3 §3; V2 §2.4) (changed from V2). |
| A-002 | V3 | Acting owner and requester kept apart, with unknown left unknown (V3 §3, G05). |
| A-003 | V3 | 70-column maximum and 44 lines leave the most margin; V2 has none (V3 §4 rule 7, §1; V2 R-FMT-01). |
| A-004 | V3 | Two clocks and per-source times resist reading a reprint as fresh; V1's TRAIL is concept E only (V3 §3; V1 §10.2) (changed from V1). |
