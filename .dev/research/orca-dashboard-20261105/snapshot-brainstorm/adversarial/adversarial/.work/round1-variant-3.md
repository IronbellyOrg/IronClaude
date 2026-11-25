# Round 1 Statement: Variant 3 Advocate (haiku:backend)

## Position Summary

Variant 3 should supply the merged specification's observation and data-integrity contract: it distinguishes a successful read from a complete census, compares compatible source observations, and refuses to turn conflicting evidence into readiness (V3 sections 3-4). Its presentation is not the strongest: retain V1's fixed frame and more visibly distinct concepts, and V2's overflow demonstration, ownership treatment and evaluation structure rather than treating V3 as a complete winner.

## Steelman of Variant 1

V1's strongest argument is that truth rules must survive a change of layout. Its four-layer architecture assigns each layer both an owner and a prohibition; notably, renderers must never "read sources directly, hide coverage gaps, or drop an item without counting it as omitted" (V1 section 2). The shared OLDEST line protects the central success criterion across alternate concepts, while the per-concept dependency table makes prerequisites visible before choosing a default (V1 sections 4.2 and 11.2). Its queue, matrix, tree, ladder and journal are genuinely different whole-report organizations, a stronger answer to the seed's five-concept requirement than V3's repeated bundles (V1 sections 6-10; seed, Success Criteria).

This architecture should be retained. The case against adopting V1 unchanged is not that architecture is excessive, but that a shared derivation layer still needs precise rules for pagination races, source skew and incomplete histories; V3 supplies those rules (V3 section 3).

## Steelman of Variant 2

V2's strongest argument is that both the evidence and the operator's interpretation need explicit checks. Its [E]/[P]/[G] labels distinguish observed capability, design proposal and feasibility gate (V2 section 1). The Ball-Holder Board asks whether an item belongs to a human, coordinator, worker or nobody known, while admitting that ownership inference can be wrong (V2 section 4.2). This is a real alternative organizing principle, not a cosmetic layout change.

V2 also draws overflow with arithmetic, names each alternate concept's residual false-all-clear risk across states, separates reader tasks from mechanical checks, and makes non-consuming production a "Cannot ship" gate (V2 sections 7.1, 8, 9 and 12.1 FG-8). Those are stronger review and validation surfaces than V3's short comparison paragraph. V3 should not displace them merely because its data contract is more detailed.

## Key Strengths Claimed

1. **A returned page is not a durable decision census.** V3 says "even fewer than 100 returned messages do not prove complete unresolved history" and keeps inventory, worker and decision coverage separate (V3 section 3, Source capabilities and safe failure). This closes a concrete false-confidence path left by the under-cap OK examples in V1 section 12.1 and V2 section 7.2. It also stays inside the seed's evidence boundary: no alternate complete observer API is verified (seed, Known Context).

2. **Pagination and authority failures have defined outcomes.** Opaque tokens are passed unchanged; repeated tokens, page errors and deadlines yield partial coverage; conflicting versions remain marked unless source ordering resolves them (V3 section 3). The statement "Cursor exhaustion alone does not prove a point-in-time census" prevents a moving collection from being promoted into an exact fleet total. Work records additionally prevent superseded attempts from overwriting current outcomes, and resource identity is kept separate from work identity (V3 section 3, Logical records and authority).

3. **Comparisons have the right scope and direction.** V3 requires a last-success pointer "per source and scope" and compares compatible scope/schema/revision identities (V3 section 4, rule 4). Partial observations can establish additions, not absence or negative movement; "newly observed" is not necessarily "newly created" (rules 4-5). Thus an incomplete refresh can reveal a real new candidate without inventing a disappearance or resolution elsewhere.

4. **Freshness measures evidence, not merely transport success.** V3 distinguishes collection freshness from underlying evidence freshness: "A successful fetch of an old liveness record is not a fresh liveness observation" (V3 section 3, Observation envelope). Unknown timestamps and future timestamps get unknown age or clock-conflict treatment, not fabricated waiting time (V3 section 4, rule 1). The proposed two-interval cutoff is explicitly provisional, not a verified service guarantee.

5. **Cross-source disagreement stays visible.** V3 states "No cross-source transaction is established" and requires an immutable collection bundle with source intervals and revision provenance (V3 section 3). Wrong-revision passes, unavailable checks and current-revision failures are distinct; absent provenance must not be converted into an actionable failure (V3 section 10, completion-with-failure discussion; section 11, contract cases). This is a useful data contract without inventing API endpoints or a storage engine.

6. **Overflow preserves an item's meaning and accounting.** V3 omits whole lower-priority bundles, reserves the oldest decision and a verification contradiction, and distinguishes observed, shown, omitted and unobserved quantities (V3 section 4, rules 7-9). That is safer than satisfying a row limit by clipping away an owner or the condition attached to a question. The explicit admission that severe overflow defeats full explanation is more honest than implying an archive exists.

7. **Failure cases are specified before implementation.** V3's future contract cases include interrupted paging, duplicate records, conflicting authority, overlapping blockers, cycles, scope changes, clock conflicts and interrupted publication (V3 section 11). These are proposed acceptance cases, not tests already run. They give a future implementation concrete failure behavior instead of only a nominal successful fixture.

8. **Source text cannot become report policy or leak secrets unchecked.** V3 requires escaping fences and control sequences, marking redaction, and redacting secrets before chat delivery (V3 R16; section 4, rule 10). V1 and V2 also reject transcript instructions, but V3 explicitly addresses credential leakage as well as formatting and instruction injection (V3 section 12, risks).

## Weaknesses Identified in Other Variants

1. **Under-cap reads can look more complete than the evidence permits.** V1's empty screen labels messages `ok 37<100cap`; V2 uses `msg-peek OK 22/100` and says the wording is allowed because sources are OK and below cap (V1 section 12.1; V2 section 7.2). Both retain wider caveats, so neither should be accused of an unconditional global all-clear. Nevertheless, V3 section 3 more clearly separates successful collection from complete unresolved history, even below the cap.

2. **V1's partial-observation comparison contract contradicts its busy screen.** CHG-2 says a failed or partial collection gives `n/a (no baseline)`, but capped-message decision changes are still NEW and ESCALATED in the busy example (V1 sections 3.4 and 6.2). V3 section 4, rules 4-5 resolves this by distinguishing positive newly observed information from absence-based deductions. It does not require discarding every useful observation merely because the collection is incomplete.

3. **V1's impact-first tree depends on a prerequisite its own gates leave open.** Its root order is distinct affected tasks, then age, while G4 asks whether a complete dependency graph exists (V1 sections 8.1 and 17). The fixed OLDEST frame line mitigates discoverability, but incomplete graph coverage still cannot justify a reliable largest-impact ordering. V3 section 7 chooses age and explicitly forbids unlock-size ranking without completeness.

4. **Answered items lose too much context in V1's default.** They leave NEEDS YOU and persist only by key in FLEET (V1 section 6.1). V2's dedicated ANSWERED, NOT RESOLVED band is stronger because the unresolved handoff remains attention content rather than fleet bookkeeping (V2 sections 4.1 and 6). V3 should borrow that band too; its reply-not-resolution rule alone is not an equally visible treatment.

5. **V2's owner field can name the relay rather than the actor.** Rows under HUMAN/NEEDS YOU use `w-07 > coord`, while the actionable-row contract calls for an acting owner (V2 sections 2.3, 4.1 and 4.2). V2 correctly admits ownership is inferred, but the mockup still makes the human answerer harder to identify. V3's explicit separation of acting human and requesting worker, with unknown ownership left unknown, should govern field meaning (V3 section 3).

6. **V2's claim of coverage across every busy screen is too broad.** Its section 5 says all five carry per-source freshness and requester/owner information, then acknowledges missing references and impacts. Section 8 also admits the fixed failing/unverified summary is missing from C4/C5. The admissions are valuable, but a merged spec must carry forward the requirements, not the broader conformance claim (V2 sections 5 and 8).

7. **Both rivals need stronger collection-consistency semantics.** V1's collector records paging status, and V2 requires coverage reporting, but neither specifies repeated-token behavior or warns that exhausted pages may represent a moving dataset (V1 section 2; V2 sections 2.1 and 3.6). V3 section 3 and gate G02 address these failure modes directly. This is additional protection, not a claim that either rival proposes consuming reads.

## Concessions

1. **V3 undershoots the five visibly different concepts.** The same D1/F1/D2 bundles recur with similar shape in the brief, handoffs and journal (V3 sections 5, 8 and 9). The organizing principles differ, but V1's matrix and ladder make the alternatives easier to distinguish. Adopt V1's stronger visual differentiation without relaxing V3's data rules.

2. **V3 does not specify a reusable shared frame adequately.** W/M/V are defined outside the screens, and there is no printed legend contract (V3 section 4, closing paragraph; sections 5-10). A standalone chat reader should not need the specification to decode source labels. V1 sections 4.1-4.3 should prevail on the frame and notation.

3. **V3 needs a drawn overload fixture.** Its six-bundle policy and seven-item acceptance case are useful but do not show the operator a crowded report (V3 sections 4 and 11). V2 section 7.1 provides better review evidence with a dedicated overflow screen and printed arithmetic. The three-item fixture also does not demonstrate the dozens-of-agents load described in the seed.

4. **V3's default does not keep every human question ahead of non-human work.** Its verification item owned by a worker sits above the second human question (V3 sections 5 and 10). Pinning verification guards against accepting bad work, but the fixture supplies no severity evidence demanding that order. Prefer V1 DEC-1's decisions-first requirement for the default while reserving a visible verification block (V1 section 3.1). V1/V2 alternate mockups also need repair against their own decisions-first requirements.

5. **V3's Run Ledger mockup puts inventory before actionable bundles.** That conflicts with its later instruction to keep action bundles ahead of inventory in busy runs (V3 section 6, screen and tradeoffs). Its reconciliation model is useful; the displayed order is not the final attention-first order.

6. **The density policy does not establish transport safety.** A 44-line target that yields to full questions can exceed any assumed size bound; six bundles alone do not bound text length (V3 section 4, rule 7). No variant verifies a chat-platform message limit. A complete-bundle policy and a verified delivery limit must both hold, or the promised single-message report is infeasible for that input.

7. **Several proposed rules still need operational definitions.** V3 does not establish heartbeat classification, a per-person ownership service, an actual retention capacity, a precise severity policy, or how redaction preserves a question's meaning (V3 R06/R16; sections 4 and 12). Its proposed two-interval stale threshold needs source-specific agreement. These are not existing capabilities or solved implementation details.

## Shared Assumption Responses

- **A-001 — QUALIFY.** Suppression is safe only for positively identifiable routine traffic that contains no unresolved question; ambiguous messages must remain visible as candidate attention, not silently disappear. All variants require noise suppression without defining that classification boundary (V1 COM-4; V2 section 2.4; V3 R06). V3's candidate-question and uncertain-identity treatment is the closest foundation, but it does not itself implement reliable classification (V3 section 3).

- **A-002 — REJECT.** Reading a shared chat does not establish acting ownership. V2's Ball-Holder Board is the strongest existing distinction between human, coordinator, worker and unknown responsibility, although its message ownership inference remains gated (V2 section 4.2). Use V3's explicit acting-owner/requester distinction and unknown fallback as the data rule; do not interpret an address such as NEEDS YOU as an assignment or acknowledgement (V3 section 3 and R10).

- **A-003 — QUALIFY.** A line/column target is only a layout proposal until the target chat platform's total message limit and fence behavior are verified. V2 explicitly asks whether 60 lines is acceptable and says no chat client was tested (V2 section 12.2, question 7). V3's complete-bundle priority is worth retaining, but its yielding 44-line target cannot prove a single paste fits (V3 section 4, rule 7). Truncation must not silently remove coverage or omission accounting.

- **A-004 — REJECT.** An as-of timestamp cannot ensure that a reader sees the latest paste or reads near collection time. V3 is least exposed because it says a newly printed report does not make old observations fresh and prints source times separately (V3 section 3). Still, all variants lack a reader-side validity boundary: the merged design must explain that observations require rechecking before action when read later, without claiming the static paste updates itself.

## Per-Point Verdict Table

| Point | Superior | Reason (one line, with a section citation) |
|-------|----------|--------------------------------------------|
| S-001 | V1 | Separate model, frame, concepts and overflow sections make obligations easier to locate (V1 sections 2-4, 6-10, 13). |
| S-002 | V1 | Explicit layer ownership and prohibitions are the best architecture; populate them with V3 integrity rules (V1 section 2). |
| S-003 | V3 | Each requirement has an observable acceptance condition, including identity and provenance (V3 section 2). |
| S-004 | V1 | One mandatory header/footer contract prevents renderer-specific truth-rule drift (V1 section 4). |
| S-005 | V2 | The explicit shared fixture includes ages, shared dependencies and answered-but-unresolved work (V2 section 2.6). |
| S-006 | V2 | The alternate-concept/state matrix names residual false-all-clear risks beyond the four default screens (V2 sections 7-8). |
| S-007 | V2 | A dedicated crowded screen demonstrates omitted counts and arithmetic rather than only promising them (V2 section 7.1). |
| S-008 | V1 | Comparative ratings plus a per-concept dependency table explain both layout tradeoffs and prerequisites (V1 sections 11.1-11.2). |
| S-009 | V3 | Deterministic contract cases cover paging errors, conflicts, scope changes and interrupted publication (V3 section 11). |
| S-010 | V2 | Closing-evidence and affected-concept columns make gates reviewable rather than merely open questions (V2 section 12.1). |
| S-011 | V1 | A defined legend printed in each snapshot makes shorthand locally readable (V1 sections 4.1-4.3). |
| S-012 | V3 | Blank-separated complete bundles avoid spending lines on separators; this is a layout preference, not measured superiority (V3 section 5). |
| C-001 | V3 | Run Ledger exposes assignment, verification and execution separately for reconciliation (V3 section 6). |
| C-002 | V1 | Queue, matrix, tree, ladder and journal are the most visibly distinct whole-report concepts (V1 sections 6-10). |
| C-003 | V2 | The default has named borrowed elements and explicit evaluation conditions for changing it (V2 sections 6 and 9.3). |
| C-004 | V1 | DEC-3 and the fixed OLDEST line formally protect findability in every renderer (V1 sections 3.1 and 4.2). |
| C-005 | V3 | First-observed lower bounds, unknown-age warnings and clock conflicts prevent fabricated age rankings (V3 section 4, rule 1). |
| C-006 | V3 | Separate worker coverage and decision census prevent a successful fetch from implying complete unanswered history (V3 section 3). |
| C-007 | V3 | Age-ranked roots, task-set unions, overlap markers and cycle conflicts work without invented impact certainty (V3 sections 4 and 7). |
| C-008 | V2 | Explicitly printed silence thresholds allow meaningful liveness exceptions without heartbeat rows (V2 sections 2.4 and 4.1). |
| C-009 | V3 | Per-source/scope compatible baselines and positive-only partial observations define safe comparisons (V3 section 4, rules 4-5). |
| C-010 | V3 | Disappearance becomes last-known unresolved with current status unknown, not assumed continued current status (V3 section 4, rule 3). |
| C-011 | V2 | The ANSWERED, NOT RESOLVED band preserves both unresolved visibility and the changed next actor (V2 sections 4.1 and 6). |
| C-012 | V3 | Empty successful collection is explicitly distinct from unknown durable decisions and fleet-wide health (V3 section 10, empty state). |
| C-013 | V3 | Full last-known bundles retain context while the banner and footer state current totals are unknown (V3 section 10, stale state). |
| C-014 | V3 | Missing, stale, mismatched and failed checks remain distinct, with subject/revision provenance (V3 sections 3, 10 and 11). |
| C-015 | V1 | The y/n/? delivery ladder distinguishes transport and resolution without a permanently unknown human-seen column (V1 section 9.1). |
| C-016 | V3 | Whole-bundle omission and four-way accounting preserve actionable meaning and separate unobserved from unprinted (V3 section 4, rules 7-9). |
| C-017 | V3 | Wrapping, escaping and marked secret redaction protect meaning and chat safety together (V3 R03/R16; section 4, rule 10). |
| C-018 | V2 | Reader tasks, mechanical checks, sample-size guidance and critical-failure rules provide the fullest evaluation protocol (V2 section 9). |
| C-019 | V2 | Non-consuming production is explicitly a ship blocker, not merely a partial-label condition (V2 section 12.1, FG-8). |
| C-020 | V3 | Explicit synthetic marking and DEMO-prefixed entity references provide the cleanest naming discipline (V3 section 1 and screens in sections 5-10). |
| X-001 | V1 | Decisions-first should prevail in the default; V3's fixture supplies no severity reason to interleave a worker-owned failure (V1 DEC-1; V3 section 5). |
| X-002 | V3 | Rank roots by age and prohibit unlock-size ranking without complete graph evidence (V3 section 7). |
| X-003 | V3 | A response below the cap still cannot prove a complete unresolved-message history (V3 section 3). |
| X-004 | V3 | Scope-qualified absence must never become fleet-wide all-clear or a readiness claim (V3 section 10, empty state). |
| X-005 | V3 | Positive-only partial additions resolve the conflict between useful changes and unsafe absence deductions (V3 section 4, rules 4-5). |
| X-006 | V1 | Preserve DEC-1 and the fixed OLDEST contract; repair V1's tree/journal ordering rather than waive its invariant (V1 sections 3.1, 4.2, 8 and 10). |
| X-007 | V1 | Explicit decisions-first plus a mandatory oldest pointer should govern repairs to V2's failure-first alternate blocks (V1 DEC-1/DEC-3; V2 sections 4.3 and 4.5). |
| X-008 | V3 | Use visibly synthetic DEMO-prefixed worker and evidence IDs consistently, unlike V2's short unmarked IDs (V3 sections 5-10). |
| X-009 | V3 | Union counting plus an overlap note under both questions is the rule to retain; test it explicitly (V3 section 4, rule 6; section 11). |
| X-010 | V3 | Consistent DEMO-prefixed entity identifiers avoid V1's contradictory synthetic-worker example (V3 section 1 and sections 5-10). |
| A-001 | V3 | Candidate-question/uncertain-identity semantics are the least unsafe basis for ambiguous message classification (V3 section 3; response A-001 above). |
| A-002 | V2 | Ball-Holder explicitly separates responsibility and admits inferred ownership may be wrong (V2 section 4.2; response A-002 above). |
| A-003 | V2 | The chat-length question remains explicitly unresolved and no client testing is claimed (V2 section 12.2, question 7). |
| A-004 | V3 | Separate generation/collection/evidence times most clearly resist treating a reprinted old observation as fresh (V3 section 3). |
