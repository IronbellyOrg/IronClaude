# Round 1 Statement: Variant 1 Advocate (opus:architect)

## Position Summary

Variant 1 is the only variant that builds the honesty rules into its structure rather than into each screen. Its s.2 four-layer model ("one report model, many renderers") has an owns / must-never table, so partial coverage, unknown-is-not-zero and no-false-all-clear each live in one place and survive a change of default or source. The merged spec should keep V1's skeleton (layers, Layer-tagged requirements, the frame contract, the OLDEST line, the data-dependency table). It should import V3's observation-integrity rules and V2's evaluation, overflow screen and concept x state matrix, which are better than V1's on those points.

## Steelman of Variant 2

Strongest version: V2 is the most decision-ready document for a human reviewer.

- It tags every claim [E], [P] or [G] (s.1), so a reader knows what is evidence, what is a proposal and what is gated.
- Its second axis, C2 Ball-Holder (s.4.2), organizes by responsibility rather than location. That makes it the most structurally distinct alternative to a decision queue in any variant.
- Its default is a hybrid (C1 plus three borrowed elements) with a test-gated switch to C5 under an explicit decision rule (s.9.3). The default can be proven wrong instead of only asserted.
- It is the only variant with a dedicated overflow screen (s.7.1).
- It has a concept x state residual-risk matrix with a common repair, R-INT-05 (s.8).
- It has a fixture table (s.2.6) that includes an answered-not-resolved case.
- Its evaluation is sized ("at least 8 for a quantitative read", s.9).
- Its no-consumption gate is binding: FG-8 says "Cannot ship" (s.12.1), and s.12.3 gives a next step.
- Its empty state keeps "observed" wording and prints a mandatory "NOT AN ALL-CLEAR FOR" line (s.7.2).

On evaluation, overflow, the fixture and state coverage, V2 should prevail, and I vote for it there.

Critique, with counter-evidence:
1. Honesty is per screen, not structural. s.6 says the concepts could reuse one model, "but the model is not specified here". With no model, nothing stops a renderer from summing partial counts or dropping a coverage gap. V1 s.2 forbids both at the layer boundary.
2. R-INT-01 allows "all clear", "healthy" or "none" when every source is OK and fully paged (s.3.7). s.7.2 then treats `msg-peek OK 22/100` as OK because it was "read below its cap". A capped, cursorless peek that returns fewer rows than the cap does not prove completeness (X-003, X-004). V1 COV-4 never prints an all-clear in the default, and V1 s.12.1 keeps the OLDEST line qualified ("inbox has no cursor: completeness unverified").
3. s.2.3 says age is measured from original creation but gives no fallback when the creation time is missing (C-005).
4. C3 and C5 do not lead with decisions (X-007), and C5 has no oldest pointer outside C1 (C-004). In two of the five concepts, the seed brief's main success measure depends on scrolling.
5. `w-07` and `M-201` carry no DEMO marker (s.2.6, s.7.1; X-008).
6. The stale state picks the oldest "(by timestamp)" without naming which timestamp (s.7.3).
7. The 60-line budget (R-FMT-03) is the least conservative of the three against an unverified chat limit (A-003).

## Steelman of Variant 3

Strongest version: V3 is the most rigorous about what an observation can and cannot prove, which is exactly where a static snapshot fails without anyone noticing.

- s.3 defines an observation envelope: source, scope, collection start and end, last success, a status of `ok`, `partial`, `unavailable` or `invalid`, and paging status.
- It keeps two clocks apart: "A successful fetch of an old liveness record is not a fresh liveness observation."
- Its paging rule is precise: "Completion means a successful terminal page, not merely receiving fewer rows than requested". For messages: "Even fewer than 100 returned messages do not prove complete unresolved history" (s.3).
- s.4 rule 1 gives a fallback when creation time is missing (`observed >=Nm`), a visible warning that the oldest cannot be certified, and `clock conflict` for future timestamps.
- Rule 4: "Partial observations can establish positive additions, but not absence, resolution or negative movement."
- Rule 5: "`Newly observed` is not necessarily newly created."
- Rule 6 counts sets, not rows, with an overlap note.
- Concept C orders roots by the oldest observed decision rather than by impact, shows cycles as `dependency conflict`, and adds a UNION footer (s.7).
- R16 treats transcript text as untrusted and redacts secrets.
- s.11 lists deterministic contract cases, including four distinct verification labels and "A collection interruption cannot advance a source's last-success pointer."
- G01 correctly names the durable decision source as the central feasibility gate.
- The s.10 stale screen ("LAST KNOWN UNRESOLVED / not confirmed current", with ages still counting) is the best stale rendering of the three.

On C-005, C-007, C-009, C-013, C-014, C-017 and most X points, I vote V3.

Critique, with counter-evidence:
1. **Weakly distinct concepts (C-002).** All five concepts render the same three bundles (DEMO-D1, DEMO-F1, DEMO-D2) under the same header block (s.5-s.9). Concept B's ledger and Concept D's handoffs mostly regroup the s.5 brief. The seed brief asks for five structurally different concepts.
2. **Decisions are not strictly first (X-001).** s.4 rule 2 pins "one verification contradiction". Concept A therefore places `VERIFY BEFORE ACCEPTING` (DEMO-F1, owned by a worker) above `ALSO WAITING` (DEMO-D2, a human decision) (s.5). That trades the seed's attention-first ordering for a mixed priority list.
3. **No frame contract or printed legend (S-004, S-011).** Each concept restates its own header lines, so nothing in the structure stops the five headers from drifting apart.
4. **Flat requirements (S-003).** R01-R16 (s.2) have no owning component, so a maintainer cannot tell whether R09 is enforced at collection, in the model or at render time. V1's Layer column answers that.
5. **Prose-only overflow (S-007).** s.4 rules 7-9 describe the policy, but no overflow screen exists to run E06 against.
6. **Provisional default (C-003, C-018).** The default is "provisional" (s.10, G08). The switch criterion is only "Prefer Decision Brief unless another concept improves E01 and E06" (s.11), tested on five operators, which V3 itself calls "not statistical proof".

## Key Strengths Claimed

1. **The structure enforces honesty, not each screen (S-002, U-001).** s.2 separates collection, the observation store, the report model, the frame and the renderers. "Why this shape" point 1: "A new renderer cannot accidentally print an all-clear because it never decides coverage." Points 2-5 add a reversible default, contained source churn, golden-text testing and reuse in a later interactive view. V2 leaves its model "not specified here" (s.6). V3 has an envelope and a record table but no component boundary for rendering.
2. **Every requirement has an owning layer (S-003).** s.3: "The layer column shows where the requirement is enforced in the section 2 model." Each DEC, BLK, COM, CHG, VER and COV rule has one place of enforcement, which is what keeps a five-renderer design maintainable.
3. **One frame contract for every concept (S-004, S-011).** s.4.1 fixes the header and footer, s.4.2 fixes the field set, including a `legend` row ("Fixed glossary for `?`, `>=N`, `seen>=N`"), and s.4.4 marks derived identities `id:derived` (R-3). A change of default concept cannot drop the coverage line or the legend.
4. **The oldest blocking decision is in every concept (C-004, U-002).** DEC-3: "other concepts must repeat it in a fixed `OLDEST` line in the frame". The s.4.2 OLDEST field becomes `none observed (partial)` when sources are incomplete.
5. **No false all-clear, by rule (X-004, C-012).** COV-4: "The default renderer never prints it; the best possible state is `no attention items observed; coverage complete`." s.12 fixes the banner set ("NO ATTENTION ITEMS OBSERVED. This is not an all-clear: coverage partial."). s.12.1 keeps `OLDEST none observed (inbox has no cursor: completeness unverified)`.
6. **Partial totals are never summed (C-006).** s.7.2: "Totals that mix current and last-good values are never added together: `1+1*` reads '1 current plus 1 last-good'." DEC-5 labels first-observation ages `seen>=`.
7. **Change semantics cover disappearance and failed collection (C-010).** s.10.1 includes a VANISHED kind, and the s.10.2 busy screen shows `VANISHED D-DEMO-0040 no resolution observed: kept open below`. CHG-2: a failed or partial collection "never supplies a zero baseline". R-2 keeps last-good observations plus gap records in layer 2.
8. **The delivery ladder admits what it cannot see (C-015).** COM-5: a read that would consume is reported as `unavailable (would consume)`.
9. **Verification never borrows a pass.** s.12.4: "a check that passed for an older revision does not count as verification (VER-3)". The row reads `NOT VERIFIED`.
10. **The comparison rests on source coupling (S-008, U-005).** The s.11.2 table lists the data each concept depends on, and s.11.3 picks the default with a coupling rationale the other variants lack.
11. **The most conservative size budget (C-020, A-003).** Content is at most 78 columns inside an 80-column budget (s.1, FMT-2). OVF-8 targets "at most about 40 lines" and labels it "a design target, not a measured constraint" (s.13). EV-10 adds a mechanical paste check (s.14).

## Weaknesses Identified in Other Variants

1. **V2 has no specified model (S-002).** s.6: "the model is not specified here". Each concept must re-implement every honesty rule, and that is where drift happens.
2. **V2 allows an all-clear under a condition it cannot verify (X-004).** R-INT-01 (s.3.7) permits "all clear", "healthy" or "none" when every source is OK and fully paged. The no-false-all-clear rule then hangs on a completeness test that the capped peek cannot pass.
3. **V2 treats a read under the cap as complete (X-003).** s.7.2: `msg-peek OK 22/100`, and "none observed" is allowed "because every source is OK and read below its cap". V3 s.3 states the correct rule.
4. **V2 has no fallback for a missing creation time (C-005).** s.2.3 and R-DEC-02 require age from original creation but do not say what to print when that time is absent.
5. **In V2, C3 and C5 do not lead with decisions, and C5 has no oldest pointer (X-007, C-004).**
6. **V2 breaks the synthetic-marker rule (X-008, X-009).** `w-07` (s.2.6) and `M-201` (s.7.1) carry no DEMO marker.
7. **V2's stale state is ambiguous.** It labels the oldest "(by timestamp)" without saying which clock (s.7.3). V3's two-clock rule (s.3) avoids this.
8. **V3's concepts are near-duplicates (C-002).** s.5-s.9 render the same DEMO-D1, DEMO-F1 and DEMO-D2 bundles under the same five-line header. B and D regroup A instead of changing the organizing structure.
9. **V3 puts a worker-owned check above a human decision (X-001).** Concept A orders `VERIFY BEFORE ACCEPTING` (DEMO-F1) above `ALSO WAITING` (DEMO-D2), following the pin in s.4 rule 2.
10. **V3 has no frame contract or legend (S-004, S-011).** Each concept restates its header, and nothing in the structure keeps the five headers identical.
11. **V3's requirements have no owning component (S-003).** R01-R16 (s.2) are flat, and where each is enforced is unstated.
12. **V3's overflow is prose only (S-007).** s.4 rules 7-9 describe the policy, but there is no screen for E06, one of its two default-switch criteria (s.11), to test against.
13. **V3's evaluation is too small for its own decision (C-018).** It uses five operators (s.11), which it calls "not statistical proof", to choose among five concepts.

## Concessions

1. **X-005, internal contradiction.** CHG-2 says partial collections give `n/a (no baseline)` deltas, yet the s.10.2 Delta Journal busy screen lists NEW and ESCALATED entries while the frame shows `msgs CAPPED 100/100`. V3 s.4 rule 4 ("Partial observations can establish positive additions, but not absence") is the correct repair and should replace CHG-2's wording.
2. **X-006, internal contradiction.** Concepts C and E do not put decisions first, against DEC-1. The OLDEST frame line limits the damage (s.8.3 admits "the oldest is only guaranteed in the frame `OLDEST` line"), but it does not remove the contradiction.
3. **X-010, synthetic marker.** s.1 cites `w-07` as an example of a DEMO-marked identifier, but `w-07` contains no DEMO marker.
4. **X-003, under-cap reads.** COV-3 and s.12.1 render `msgs ok 37<100cap`, so the source token reads as complete. The OLDEST line stays qualified because the inbox has no cursor, but the token itself overstates. V3 s.3 is right.
5. **C-007, roots ranked by impact.** Concept C ranks roots by impact (s.8.3: "Ranking by impact can push an old, low-impact decision down"). V3 s.7 orders by age and allows "No critical-path or unlock-size ranking without a complete graph". V3 is better here.
6. **C-005, `seen>=` is incomplete.** DEC-5 has no clock-conflict rule and no visible "oldest cannot be certified" warning. V3 s.4 rule 1 has both.
7. **No cursor-integrity rule (U-014).** V1 does not say that receiving fewer rows is not completion, or how repeated and invalid tokens are handled.
8. **No cycle handling and no secret redaction (U-016, U-017).** V3 s.7 and R16 cover both. V1 does not.
9. **Overflow, fixture and evaluation are thinner than V2's.** V1 has no dedicated overflow screen (s.13 gives only the OVF rules), no fixture table, and no participant count or decision rule in EV-1..10 (s.14).
10. **Answered-but-unresolved items have no band of their own (C-011).** V2 s.4.1 gives them a dedicated `ANSWERED, NOT RESOLVED` band.
11. **No switch rule for the default (C-003).** s.11.3 picks A, but no stated result would flip it. V2 s.9.3 has such a rule.
12. **Five renderers have a cost.** R-8 (renderer drift) is real. The layer model contains it, but it does not make five renderers cheap.

## Shared Assumption Responses

- **A-001 (heartbeats can be reliably told apart from decision requests): QUALIFY.** This holds only when the source labels each message's kind. Where it does not, an unclassified message must be treated as needing attention, or at least counted visibly; it must never be dropped. V1 s.9.1 keeps a QUIET line ("heartbeat-only workers folded into a count with last-seen bound"), so a misclassification surfaces as a number the reader can question. V3 R06 and V2 s.2.4 exclude heartbeats and leave no visible trace. Closest: V1.
- **A-002 (the chat reader is the acting owner of every human-required item): QUALIFY.** This holds only when one operator runs the deployment. Owner must be an explicit field, and an owner that cannot be mapped must stay `unknown`. V1 G8 keeps the owner as plain `human` until a gated ownership source exists. V3 handles this best. s.3 says "Actor mappings must distinguish acting human from requesting worker; missing owner stays unknown". Concept D groups by `WAITING ON <owner>`, and G05 makes requester, owner, answerer and resolver a gate. Closest: V3.
- **A-003 (a 40-60 line, 80-column paste fits the chat limit with the fence intact): QUALIFY.** No variant verifies the platform limit, so the budget must be a gate, not an assumption. The renderer must also drop whole lower-priority bundles rather than split the fence. V1 is the least exposed: at most about 40 lines (OVF-8, s.13), 78-column content (FMT-2), and a paste check (EV-10, s.14). V3's 44 lines, with "The target yields to preserving a complete question" (s.4 rule 7), is a close second. V2's 60 lines (R-FMT-03) is the most exposed. Closest: V1.
- **A-004 (readers act on the latest paste near its as-of time and can tell older pastes apart): QUALIFY.** Chat history keeps old pastes, and a reader can scroll back to one. Every paste therefore needs a prominent as-of time, a last-success time for each source and the comparison window (V1 s.4.1 header). V3 goes further. It keeps two clocks, says "A newly printed report does not make old observations fresh" (s.3), and has a stale screen whose ages keep running (s.10). Closest: V3.

## Per-Point Verdict Table

| Point | Superior | Reason (one line, with a section citation) |
|-------|----------|--------------------------------------------|
| S-001 | V1 | 17 sections keep model, frame, concepts and gates apart so each can change alone (V1 s.2-s.4, s.17). |
| S-002 | V1 | Only layer model with owns/must-never; V2 says the model is "not specified here" (V1 s.2; V2 s.6). |
| S-003 | V1 | Layer column shows where each requirement is enforced (V1 s.3); V3 R01-R16 are flat. |
| S-004 | V1 | One frame contract shared by all concepts (V1 s.4.1-s.4.2); V3 has none standalone. |
| S-005 | V2 | Explicit fixture table makes every screen checkable (V2 s.2.6). |
| S-006 | V2 | Concept x state matrix covers four states for all five concepts (V2 s.8). |
| S-007 | V2 | Only dedicated overflow screen with explicit counts (V2 s.7.1). |
| S-008 | V1 | Data-dependency table and coupling rationale ground the comparison (V1 s.11.2-s.11.3). |
| S-009 | V2 | Reader tasks, mechanical checks and a decision rule (V2 s.9.1-s.9.3). |
| S-010 | V2 | Gates carry closing evidence and a next step (V2 s.12.1, s.12.3). |
| S-011 | V1 | Fixed legend in the frame makes notation explain itself in chat (V1 s.4.2-s.4.3). |
| S-012 | V1 | One shared layout grammar keeps five renderers consistent (V1 s.4, s.6.1). |
| C-001 | V2 | Ball-Holder organizes by responsibility, the most distinct second axis (V2 s.4.2). |
| C-002 | V1 | Concepts differ by structure (age, location, cause, talk, time); V3 regroups the same bundles (V1 s.5). |
| C-003 | V2 | Hybrid default with a test-gated switch rule (V2 s.9.3). |
| C-004 | V1 | OLDEST line is mandatory in the frame of every concept (V1 DEC-3, s.4.2). |
| C-005 | V3 | `observed >=Nm`, oldest-not-certified warning and `clock conflict` (V3 s.4 rule 1). |
| C-006 | V1 | `>=N` and `1+1*` never sum partial or last-good totals (V1 s.7.2, BLK-3). |
| C-007 | V3 | Roots ranked by age, cycles shown as `dependency conflict`, UNION footer (V3 s.7). |
| C-008 | V1 | QUIET count keeps heartbeat suppression visible and checkable (V1 s.9.1, COM-4). |
| C-009 | V3 | Partial data proves additions only; newly observed is not newly created (V3 s.4 rules 4-5). |
| C-010 | V1 | Explicit VANISHED kind kept open without a resolution (V1 s.10.1-s.10.2). |
| C-011 | V2 | Dedicated `ANSWERED, NOT RESOLVED` band (V2 s.4.1). |
| C-012 | V1 | Fixed banner set; default never prints all-clear (V1 s.12, COV-4). |
| C-013 | V3 | "LAST KNOWN UNRESOLVED / not confirmed current" with running ages (V3 s.10). |
| C-014 | V3 | Stale, wrong-revision, unavailable and failing checks get four labels (V3 s.11). |
| C-015 | V1 | Distinct ladder plus `unavailable (would consume)` (V1 COM-5). |
| C-016 | V2 | Overflow budget with stated counts and footer rule (V2 s.2.5, s.7.1). |
| C-017 | V3 | Exact question text, wrapping not clipping, secret redaction (V3 R03, R16, s.4 rule 10). |
| C-018 | V2 | Sized evaluation (at least 8) with a decision rule (V2 s.9, s.9.3). |
| C-019 | V2 | FG-8 "Cannot ship" makes gate failure binding (V2 s.12.1). |
| C-020 | V1 | 78-column content inside the 80 budget plus a paste check (V1 FMT-2, EV-10). |
| X-001 | V1 | Human decisions lead; V3 A puts worker-owned DEMO-F1 above DEMO-D2 (V1 DEC-1; V3 s.5). |
| X-002 | V3 | Rank roots by oldest, never by unproven impact (V3 s.7). |
| X-003 | V3 | Under-cap reads do not prove completeness (V3 s.3). |
| X-004 | V1 | Default never prints all-clear; V2 R-INT-01 allows it on a condition (V1 COV-4). |
| X-005 | V3 | Additions-only rule replaces V1's CHG-2 vs s.10.2 conflict (V3 s.4 rule 4). |
| X-006 | V3 | Every concept keeps a global oldest pointer above its own grouping (V3 s.6, s.9). |
| X-007 | V3 | Same repair: a mandatory oldest pointer and carried-forward register (V3 s.9). |
| X-008 | V3 | Every identifier is DEMO-prefixed (V3 s.1). |
| X-009 | V3 | `SYNTHETIC DEMO` heads every screen (V3 s.5-s.10). |
| X-010 | V3 | DEMO markers on every worker ID (V3 s.1); V1's `w-07` lacks one. |
| A-001 | V1 | QUIET count keeps misclassified traffic visible (V1 s.9.1). |
| A-002 | V3 | Acting owner and requester kept apart; missing owner unknown; G05 (V3 s.3, s.12). |
| A-003 | V1 | Smallest budget, about 40 lines at 78 columns, plus a paste check (V1 OVF-8, EV-10). |
| A-004 | V3 | Two clocks; a new paste does not make old observations fresh (V3 s.3). |
