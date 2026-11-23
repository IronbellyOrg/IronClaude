# Advocate: Variant 3 (haiku:backend) - C. Decision Desk

## Position Summary
Choose **V3, Decision Desk**, for the complete decision-focused MVP: one selected human question, only explicitly associated dispatch evidence, and a bounded list of other observed questions. Adopt V2's retention invariant and V1's collection-status discipline without building three screens first. The reason is data integrity: a broad worker list cannot establish which workers a decision affects, and process activity cannot establish acceptance.

This is a conditional product choice, not a claim of present live capability. The design schema is PROPOSED. The supplied baseline verifies paged worker listing and non-consuming message reads capped at 100 rows, not message identity, question classification or affected-dispatch links. Ship the synthetic walkthrough first and a clearly named worker-only preview next; call the complete screen a live Decision Desk only after QUESTION-LINK verification. If the immediate requirement is a useful live screen before that gate, V1 wins that requirement.

Keep one bounded collector and one immutable published view. Identical input must not change accepted facts or selection; missing rows in partial collection must not become deletions or resolutions. Separate source scope, collection age and evidence age. No operational controls, inferred ownership joins, invented verification badges or AGPL code. Complete history, cross-host ownership joins, admission/revision-pinned evidence, cost accounting, durable replay and native deep links remain UNVERIFIED and excluded.

## Steelman: Variant 1
V1 makes the strongest delivery argument: its main worker ledger can provide useful live inspection from the verified source before any message schema becomes available. It shows workers nobody has asked about, exposes source failure and coverage, and separates raw process facts from unavailable outcomes. That is real utility, not merely a distraction from questions.

Its adapter/model/view separation also lowers the cost of changing the screen later. The monotonic generation guard is an explicit defense against late results rolling back the display. Fixed-width tests, a concrete detail view and an explicit fallback when richer interaction exceeds Rich's scope make V1 easier to estimate than V3. Its proposed all-width signals strip is a legitimate candidate design even though the descriptions of the existing narrow prototype disagree.

## Steelman: Variant 2
V2 most directly addresses losing questions in chat: keep observed questions until explicit closure evidence, order the queue by verified original age, and make looking at an item independent of resolving it. A disappearing unread row is not a resolved question. V3 should adopt this behavior from the first live-question release, not defer basic retention to a later release.

V2 also degrades honestly. Its worker-reported next-action panel is explicitly not a question feed, and its zero interpreted rows measures parser activity, not the number of real questions. The redacted golden source sample, fake runner, required-envelope tests and separate fixture loader provide a stronger concrete verification harness than V3 currently specifies. Its deadline-based fallback to V1 is a sensible product escape hatch, although the cost of switching layouts still needs estimation.

## Key Strengths Claimed (cite variant section and line ranges)
Citations below refer to `variant-3-haiku-backend.md`; these are proposed observer requirements, not verified Orca API fields or executed tests.

- **Association integrity.** “Smallest trustworthy read-only adapter,” lines 184–199, separates worker facts from proposed question records and requires explicit-link provenance. Matching tasks, worktrees, titles or times cannot manufacture an affected-scope edge. Unknown associations remain unknown rather than an apparently complete empty set.
- **Independent clocks and conflict handling.** The same section, lines 201–210, orders liveness and evidence separately, qualifies untimestamped facts and preserves equal-time contradictions. This avoids choosing a whole row by whichever unrelated timestamp happens to be newest.
- **Idempotent observation.** The same section, lines 211–213, makes repeated accepted input leave facts, counts, selection and change badges unchanged. First collection establishes a baseline; disappearance from a partial page establishes only non-observation.
- **Bounded failure behavior.** The same section, lines 215–228, specifies single-flight collection, subprocess/time/output bounds, timeout kill/reap, coalesced refresh, cursor-loop rejection and atomic publication. The exact numeric defaults need measurement; the explicit bounds and last-good-view behavior are the strength.
- **Scoped denominators and distinct uncertainty.** “Shown as unknown / stale / partial,” lines 64–87, separates fresh collection from old evidence, source-reported counts from observed counts, and message-row limits from question coverage. It also keeps outcome, acceptance, tests and approval independent.
- **Contract-driven release naming.** “Build order from MVP to later releases,” lines 125–148, distinguishes worker preview from complete live Decision Desk and gates richer claims on separate contracts with success, missing, stale and contradictory samples. A synthetic walkthrough cannot clear a live-source gate.

## Weaknesses in Variant 1
- **Its count wording outruns its own evidence.** V1 §4, line 68, labels a count as unread and interprets 100 as cap reached; §12, line 222, explicitly leaves that meaning UNVERIFIED. The existence of a count field does not establish its semantics. The proposed pre-shipping check is useful, but until it succeeds V3's unknown question coverage is the honest display.
- **Whole-row precedence can discard newer evidence.** V1 §9, line 169, chooses duplicates using the liveness timestamp and breaks ties by later page. Evidence can advance independently, and equal-time contradictions are not settled by page order. Use component clocks and visible conflicts, while retaining V1's generation guard.
- **Its early message fan-out buys little decision value.** V1 §9, lines 163–165, permits three worker pages and ten peeks on a five-second default schedule. Even though it is bounded and single-flight, this spends reads before question semantics are established. Worker-only R1 is a smaller trustworthy allowlist; add only a verified, explicitly scoped message read later.
- **Error classes need sharper separation.** V1 §9, line 167, maps unexpected types and missing fields to the same sentinel. Absence, explicit null and invalid values are different contract conditions; preserve the distinction internally even when the summary says unknown.
- **Breadth is not affected scope.** V1 acknowledges the unrelated-worker noise in §12, line 231. The broad ledger remains valuable for fleet inspection, but it must not substitute for a proven question-to-dispatch association.

## Weaknesses in Variant 2
- **Retention needs an honest count after eviction.** V2 §12, line 218, permits disclosed removal of retained items. Disclosure is necessary but not sufficient: an eviction must not lower an apparent unresolved total as though closure occurred. Separate retained-in-memory counts from omitted/unresolved coverage; if that coverage cannot be maintained, label the count partial or unknown. V3 also needs an explicit retention bound rather than relying on session locality.
- **Its ownership label risks a false human join.** V2 §2, line 34, offers a resource owner-dispatch identifier as an acting owner. That is a useful raw reference, not verified human responsibility. Keep the dispatch label and leave the human-owner slot unknown until the association is established.
- **Its ordering rule mixes clocks.** V2 §9, line 163, allows liveness or evidence time to select the winning row and lets later collection win when times are missing. The uncertainty badge helps, but the model should preserve independently newer component facts rather than overwrite them as one row.
- **Successful polling does not refresh old evidence.** V2 §9, line 165, defines stale collection clearly. The screen also needs an independent evidence-age qualifier, otherwise a fresh transport can visually mask old supporting facts.
- **Selection can drift to a different decision.** V2 §2, line 26, moves selection to the next row after disappearance. A named placeholder is safer while a human is inspecting evidence; partial collection must not silently retarget that inspection.

These criticisms do not establish a usable question API. V2 itself marks message fields, invocation scope and classification UNVERIFIED (§12, lines 224–230); V3 must respect the same boundary.

## Concessions (where A or B is honestly stronger)
- **V1 wins earliest useful live delivery.** C's question and association contracts are UNVERIFIED. Its worker preview is not yet its central product. Do not hide that delay by calling an empty question frame a complete MVP.
- **V2 wins queue discovery.** An age-ranked observed-question ledger is better than C for finding the next neglected request. Borrow retention from the first live-question release, and keep queue discovery available through the bounded other-questions panel rather than a second full layout.
- **V2 wins verification specificity; V1 wins module clarity.** Adopt V2's recorded-source/fake-runner approach and numbered acceptance mapping, with V1's pure view boundary and generation guard. C's prose obligations alone are not an equally executable test plan.
- **C's interaction scope is not automatically cheap in Rich.** Per-panel scrolling and Tab focus trigger V1's own framework-switch rule. Run the terminal-input/restoration and reduced-height interaction spike before selecting Rich finally; choose Textual if that scope cannot stay small. Do not claim the existing house renderer already solves it.
- **C's numeric budgets are proposals, not measured capacity.** A two-second child timeout and a thirty-second evidence-age label need real latency, timestamp cadence and terminal checks. Neither a healthy worker nor a slow read is a failed task. C also needs a render responsiveness budget and a bounded retention policy.
- **C should improve its presentation.** Use V1's titled heading hierarchy, V2's criterion/test IDs and a risk table. Flat prose is not a backend correctness advantage. Adopt an explicit interactive platform boundary and plain-text fallback, rather than C's silence.

Engineering verifies cursor syntax, message identity and link semantics; the owner chooses acceptable product coverage, content-exposure policy, platform support and budget. Owner approval cannot make an UNVERIFIED contract true. No live collection or implementation testing was performed for this debate.

## Per-Point Stances
Confidence measures confidence in the design stance, not proof of an UNVERIFIED source capability. Combined preferences borrow the named behavior, not entire extra screens. Assumption verdicts apply to the assumption as written. Unique contributions are not separately debated.

| ID | Level | Preferred variant | Confidence | One-line reason |
|---|---|---|---|---|
| S-001 | L1 | V1 | 0.99 | A document title and numbered subordinate sections are easier to cite than C's flat headings. |
| S-002 | L1 | V2 | 0.96 | Subsections separate width contracts and evidence from the main argument. |
| S-003 | L1 | V1+V2+V3 | 0.99 | The common sequence already covers the required topics; no reordering is needed. |
| S-004 | L1 | V1+V2 | 0.95 | Tables make bounds, gates and tests easier to compare than C's prose lines. |
| S-005 | L2 | V3+V1 | 0.91 | Keep C's height/overflow contract but present it in A's width matrix; validate scrolling cost. |
| S-006 | L2 | V2 | 0.98 | Criterion and test IDs give clearer traceability than unnumbered obligations. |
| S-007 | L2 | V3+V2 | 0.96 | Use C's independent contract gates with B's explicit fallback decision. |
| S-008 | L2 | V3+V2 | 0.95 | Keep contract verification with engineering while adding B's capture-permission decision. |
| S-009 | L1 | V2 | 0.94 | Separate design risks from UNVERIFIED source claims instead of mixing them. |
| S-010 | L2 | V3+V1 | 0.96 | C's immutable publication and A's pure source/view seams suffice without a plugin system. |
| S-011 | L1 | V2 | 0.94 | Explicit self-weakness makes the concessions more useful than declaring a winner again. |
| C-001 | L2 | V3+V2+V1 | 0.92 | Choose C's decision screen with B's retention and A's freshness, not three initial layouts. |
| C-002 | L2 | V3+V2 | 0.94 | Prefer B's non-consuming all-rows approach only after invocation verification, within C's selected-source bound. |
| C-003 | L3 | V3+V2 | 0.99 | Both disclose the missing question contract; zero interpreted rows is not zero real questions. |
| C-004 | L2 | V3+V1 | 0.96 | Preserve the raw next-action fact in detail; never execute it or promote it to a human question. |
| C-005 | L2 | V3+V2 | 0.98 | Scope source-reported accounting separately; no invented health or settled mapping. |
| C-006 | L3 | V3 | 0.88 | Prefer explicit time, call and output bounds, but measure latency before fixing the numeric defaults. |
| C-007 | L3 | V3+V1 | 0.99 | Combine independent component clocks and equal-time conflicts with A's generation rollback guard. |
| C-008 | L3 | V3+V2 | 0.98 | Preserve absent/null/invalid distinctions and disclose unknown members in aggregate counts. |
| C-009 | L3 | V3+V2 | 0.98 | Use B's explicit local baseline action with C's non-observation rule for partial pages. |
| C-010 | L3 | V2+V3 | 0.99 | Retain from the first question release; eviction must disclose incomplete unresolved coverage, not resolution. |
| C-011 | L3 | V3+V2 | 0.95 | Separate failed collection from old evidence; calibrate age thresholds to verified source cadence. |
| C-012 | L2 | V3+V1 | 0.94 | Distinguish historical state and allow a disclosed hide toggle without removing linked decision evidence. |
| C-013 | L2 | V3+V2 | 0.99 | A reported source total is neither a filtered denominator nor a proven cross-host fleet total. |
| C-014 | L3 | V3 | 0.99 | A capped message read proves neither question count nor completeness, even below 100 rows. |
| C-015 | L1 | V3+V2 | 0.90 | Keep inspection and panel navigation plus a local mark-looked action; no Orca write keys. |
| C-016 | L1 | V1 | 0.94 | A visible trailing marker is better than C's silence; the exact glyph is secondary. |
| C-017 | L1 | V3+V2 | 0.98 | ASCII-safe export must retain full identifiers, source times, caveats and denominators. |
| C-018 | L2 | V3+V1 | 0.93 | Test C's interaction scope early and apply A's framework switch before hand-building a widget system. |
| C-019 | L1 | V1 | 0.90 | A short in-repository observer subcommand is sufficient, subject to owner naming approval. |
| C-020 | L3 | V3+V2 | 0.99 | Require safe literal rendering and a complete sanitizer; reuse only after provenance and behavior checks. |
| C-021 | L2 | V2+V3 | 0.99 | Use B's golden sample/fake runner harness while keeping synthetic tests distinct from live-source verification. |
| C-022 | L3 | V3 | 0.99 | Explicit frozen evidence remains frozen; absent evidence never establishes unfrozen. |
| C-023 | L2 | V3+V2 | 0.98 | An unavailable-cost label is honest; no unsupported numeric slot or zero. |
| C-024 | L2 | V2+V1 | 0.97 | Define POSIX interactive scope and portable text fallback instead of leaving platform support implicit. |
| C-025 | L2 | V3+V2 | 0.95 | Keep stable dispatch ordering for evidence and verified original-age ordering for other questions, unknown ages last. |
| X-001 | L2 | V1+V3 | 0.93 | Specify the proposed narrow strip explicitly; existing 116-column behavior remains disputed, not verified here. |
| X-002 | L3 | V3+V2 | 0.99 | R1 needs worker listing only; delay message reads until their invocation and interpretation gates pass. |
| X-003 | L3 | V3+V2 | 0.99 | Count semantics are UNVERIFIED, so do not label the value unread or interpret its cap. |
| X-004 | L3 | V3+V2 | 0.91 | Pin B's reported continuation syntax before use; C's verification gate does not prove the flag absent. |
| X-005 | L3 | V3 | 0.98 | Namespace identity by a verified stable source scope; cross-host uniqueness is not established. |
| X-006 | L3 | V3+V2 | 0.93 | Separate collection/evidence ages; no variant's numeric threshold establishes source health. |
| X-007 | L3 | V3 | 0.96 | A selected-source call ceiling avoids per-Run message fan-out; adjust timeouts only from measurements. |
| X-008 | L3 | V2+V3 | 0.99 | Provenance is a prerequisite to reuse, and prototype import is unnecessary; no AGPL code. |
| X-009 | L2 | V3+V1 | 0.98 | Engineering verifies semantic contracts; the owner sets product policy and grants sensitive-sample permission. |
| X-010 | L2 | V3+V1 | 0.93 | Hide unrelated historical rows with a count, but never hide explicitly linked evidence merely for being historical. |
| X-011 | L2 | V1 | 0.99 | No verified settled mapping exists; a convenient definition alone cannot establish an outcome source. |
| X-012 | L2 | V3 | 0.94 | Complete C needs verified link semantics; individual questions with missing links still show unknown affected scope. |
| X-013 | L2 | V1+V3 | 0.96 | C's focus/scrolling crosses A's switch trigger now, so settle the interaction spike before committing to Rich. |
| A-001 | L3 | QUALIFY | 0.99 | Non-consuming reads are verified; absence of lease, audit or probe side effects remains UNVERIFIED. |
| A-002 | L3 | REJECT | 0.99 | Timestamp cadence is UNVERIFIED; evidence age cannot alone distinguish a healthy worker from a stale source. |
| A-003 | L3 | QUALIFY | 0.98 | Require bounded complete JSON plus envelope validation; zero exit status alone cannot establish valid data. |
| A-004 | L2 | QUALIFY | 0.98 | Recorded cell-width checks need real-terminal validation; font and emoji behavior can differ. |
| A-005 | L3 | QUALIFY | 0.98 | Key input, redraw, resize and restoration need a combined terminal test before Rich is accepted. |
| A-006 | L2 | QUALIFY | 0.96 | Measure rendering and selection responsiveness at scale instead of assuming the collection budget covers them. |
| A-007 | L2 | QUALIFY | 0.98 | Declare terminal requirements and provide a plain ASCII-safe fallback for unsupported interactive output. |
| A-008 | L3 | REJECT | 0.99 | Per-process caps do not bound aggregate load from multiple observers; document that limit without inventing a service. |
