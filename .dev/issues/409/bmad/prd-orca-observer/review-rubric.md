# PRD Quality Review — Orca Read-Only Terminal Observer (orca-observer)

Reviewed: `prd.md` (516 lines) and `addendum.md` (52 lines), 2026-11-08. Spot-checked against `_bmad-output/specs/spec-orca-observer/` (SPEC.md, acceptance-tests.md, rendering-rules.md, owner-decisions-and-risks.md, stack.md). Binding owner decisions (staged releases, R1 = worker ledger with the UNVERIFIED question notice, Python + Rich, R1 read-only, write-back as a future stage, open questions carried verbatim, evidence labels) are treated as given and not faulted.

Each finding carries a severity (critical / high / medium / low) and a class: **BLOCKING** (wrong claim, missing required content, untestable requirement, misleading contradiction) or **MINOR** (wording, style, citation format, length).

## Overall verdict
This is a usable, honest PRD for a gated, R0-only internal tool: decisions, gates and their status, dissents, evidence labels and FR-to-test traceability are unusually solid, and the open questions are genuinely open and carried verbatim (checked against SPEC.md:99-113). The risk is concentrated in four requirements that cannot be tested as written (FR-8 mismatch form, NFR-1 height threshold, NFR-13 Windows claim, FR-17/FR-18 "why it matters") and in success metrics that measure delivery rather than the thesis. None of this blocks R0 or the UX/architecture steps; the four BLOCKING items should be fixed before stories are cut for R1/R2.

## Decision-readiness — strong
Decisions are stated as decisions and kept separate from recommendations. Section 4 gives every stage its gate and a literal status (`DIRECTION-SELECTED ... **NOT passed**`, R1-R4 "Closed"), and the production-integration boundary says plainly what applies today: "the stricter reading applies: **offline R0 work only**". Section 4 "Settled by engineering, not by owner vote" names what the owner does not need to decide, and section 12.3 opens with "The recommendations are the spec's, recorded for the owner. None is a decision." Dissents are recorded with who holds them (section 10.1 "Recorded dissents"; OI-3, OI-4), and source contradictions are carried with both sides quoted (OI-9 to OI-12). Trade-offs are named with what is given up: the fallback rule (section 4) says "expiry never grants permission to switch direction", and risk K1 states the cost of the staged bet ("product becomes relabelled A").

A decision-maker knows exactly which two records unblock R1 (OQ-1, OQ-2; risk P1). The only friction is navigational and citation-level.

### Findings
- **low** Open questions are not tagged with the release they block (§12.1) — OQ-1/OQ-2 block R1, OQ-5/OQ-7 block R2, OQ-9 blocks the Go consumer, OQ-11 blocks write-back; the reader has to reconstruct this from section 4. *Fix:* add a "blocks" marker per OQ. MINOR.
- **low** Owner-decision numbering collides within one source file (§5.1 FR-2, §11, §12.2 line 454, §12.3 item 10) — FR-2 cites "owner-decisions-20261108.md item 5" for the stack, while line 454 and §12.3 item 10 cite "decision 5" of the same file for "TUIBBS as staff platform"; §11 calls write-back "owner decision 3, binding" while §12.3 item 10 lists "write-back stage (summary decision 3)" as "Still open". OI-11 flags only part of this. *Fix:* cite one numbering scheme (item vs summary decision) consistently, and say in §12.3 item 10 that the open part is the boundary change (OQ-11), not the future-stage placement. MINOR.

## Substance over theater — strong
No persona theater: one primary user (the supervisor), with secondary users who each drive something concrete (the Reviewer drives FR-1/T50; the Owner drives every gate; the snapshot consumer drives FR-16 and OQ-9). The Vision (§1) is specific to this product and could not be swapped into another PRD ("'read' gets treated as 'handled'"; "It is not github.com/orca-cli/orca, not a scheduler and not a session manager"). NFRs carry thresholds, not adjectives: 15 s cycle, 5 subprocesses, 8 MiB per call, 45 s STALE on a monotonic clock, 60 s back-off cap, 2 KiB stderr, `cell_len <= W` at 160/116/80 (NFR-1, NFR-7). There is no innovation or differentiation section to fault.

The only furniture is process residue from the generating chain.

### Findings
- **low** Pipeline commentary inside the product body (§12.2 line 452, OI-13) — the note that "step-1 review minor 7 ... is wrong" is about the previous chain step, not the product; OI-13 is a pointer-only item that repeats OQ-12/13/15. *Fix:* move the step-1 rebuttal to a review log and drop OI-13 (or keep it as a one-line cross-reference outside the numbered list). MINOR.

## Strategic coherence — adequate
The thesis is clear and stated twice (§1, citing the issue's root cause): human questions get lost in recency-ordered chat and reading is mistaken for handling, so the observer must keep observed questions until closure evidence and say what it cannot see. The staged releases follow from that thesis plus the data reality — R1 ships the one verified source and loudly discloses the question gap (FR-7) rather than faking it — which is coherent problem-solving MVP logic, not "what's easy first". Counter-metrics are present and well chosen (SM-C1 to SM-C4 each guard a thesis failure: "no questions" misread, out-of-allow-list argv, unknown-as-zero, mark lowering a count).

What is thin is the positive metrics. SM-1 is R0's definition of done, SM-2 is the spec's R1 success signal (a delivery checklist), and SM-3 restates the data-gate rule. Nothing measures whether the supervisor is actually helped, and R2 — the release that carries the thesis — has no success metric of its own at all.

### Findings
- **medium** Success metrics measure delivery, not the thesis (§9.2) — SM-1/SM-2/SM-3 would all pass on a product that no supervisor can use to find a changed row or a stale fleet faster; R2 (FR-17) has no SM, only the counter-metric SM-C4. *Fix:* add one thesis metric per release, e.g. R1: in a reviewer walkthrough on the golden samples, the supervisor states collected/reported, freshness and question-source status from one screen without opening the inspector; R2: 100% of observed questions leave the open set only on closure evidence across the T10-T12/T46 fixtures plus one recorded live session. MINOR (the PRD is still actionable without it).

## Done-ness clarity — adequate
Most FRs are excellent for story creation: every FR has a "Consequences (testable)" list, nearly every consequence names a pinned literal string and a test ID, and the PRD is honest where no test exists ("No spec test; reviewer-checked", "Test ID not yet assigned"). All 51 spec tests T1-T51 are cited in prd.md (checked by search), and FR consequences match acceptance-tests.md wherever spot-checked (e.g. FR-8's `PARTIAL: collected 500 of reported T` = T4, acceptance-tests.md:12; FR-14's `changed since HH:MM (1)` = T8, :13). There are no "gracefully" / "reasonable" / "user-friendly" adjectives.

Four requirements are not testable as written, though, and one verification claim is wrong.

### Findings
- **medium** FR-8 contradicts itself on the mismatch form (§5.4 FR-8, bullet 2) — the bullet says "PARTIAL, STALE, FAILED, mismatch and `n+? (k unknown)` forms render exactly as pinned" and, in the same bullet, "rendering-rules.md pins no literal mismatch string; the exact form is left to UX." A test cannot assert "exactly as pinned" against nothing; T47 inherits the gap ("mismatch ... render per `rendering-rules.md`", acceptance-tests.md:41). *Fix:* remove "mismatch" from the exactly-pinned list, state that the mismatch string is to be set by the UX step, and mark the mismatch part of T47 as pending that decision. BLOCKING.
- **medium** NFR-1's too-small-height diagnostic has no threshold (§6 NFR-1) — "When height cannot hold coverage, scope and PARTIAL ahead of optional panels, a too-small diagnostic shows" gives no minimum row count; rendering-rules.md:13 ties height to "C's 44-row height contract (drop order, minimum rows)", which OQ-14 says the sources "name ... but do not define". T49 therefore cannot be written deterministically for the R1 view. *Fix:* state the minimum height for the R1 (A) view, or mark NFR-1's height clause and T49 as blocked on OQ-14. BLOCKING.
- **medium** NFR-13's Windows claim is verified by a test that does not test Windows (§6 NFR-13) — "`--once` text export works on every platform, including Windows" lists T27 as its verification, but T27 (acceptance-tests.md:19) is a headless export assertion ("no ESC byte, full IDs, no truncation") with no platform dimension, and the harness (acceptance-tests.md:5) runs one fake runner with no TTY. Issue AC 5 and §2.4 UJ-4 ("any platform") rest on this. *Fix:* change the verification cell to "no spec test; Windows behaviour UNVERIFIED" or require T27 to run on a Windows CI runner. BLOCKING (wrong verification claim).
- **medium** "Why it matters" has no defined source (§5.10 FR-17 bullet 5; §5.11 FR-18 bullet 3) — "Each item states why it matters" and "The selected question shows why it matters" cannot be tested: the PRD does not say where the reason comes from, and message fields are UNVERIFIED (U1). Both are gated (R2/R3), so this does not block R1. *Fix:* define the reason as a sourced field shown verbatim, or `reason unknown` when absent, and tie it to OQ-7 (what identifies a human question). BLOCKING for R2/R3 story creation only.
- **low** Two consequences are untestable or vacuous in R1 (§5.4 FR-9 bullet 4; §5.2 FR-6 bullet 1) — "Each fact is in one of four states" cites only rendering-rules.md and no test; FR-6's "default view is chosen once at start-up from the runtime state of the question source" has only one possible view in R1, so T45's "never switches" is trivially true until R2. *Fix:* map the four-state rule to T13/T15/T40/T42; note that FR-6's view choice becomes meaningful at R2. MINOR.
- **low** FR-8 omits a pinned form (§5.4 FR-8) — T18 and T32 also pin `page.total` absent → `reported unknown` (acceptance-tests.md:16, :21); FR-8 lists only the present case. *Fix:* add the `reported unknown` consequence. MINOR.

## Scope honesty — strong
Omissions are explicit everywhere they could be silently assumed. Section 7 is a real Non-Goals list (operational controls, `r` key, persisted last look, Windows interactive input, the TUIBBS Go screen), and section 8 splits "In R1" from "Not in R1" and states the gating up front ("Today only R0 work is allowed"). De-scoping is proposed honestly: FR-12 bullet 3 says the partial-subtotal rule "binds whichever later stage adds cost"; §9.1 row 11 (design images) is carried open as a delivery item rather than quietly dropped (OI-7, A6). Section 11 fences write-back with "Nothing in this section is in R0, R1, R2 or R3, and nothing here is approved." Gaps between the issue and the spec are surfaced, not hidden (§9.1 "no spec test" cells; risk P2).

Open-items density is high (15 OQs, 13 OIs, 9 inline `[ASSUMPTION]` tags, 19 unverified-register rows), but this PRD is explicitly not a green light — R1 through R4 are all "Closed" — so the density is appropriate to the stakes, not a blocker. The Assumptions Index roundtrip has small gaps (see Mechanical notes).

## Downstream usability — adequate
This PRD feeds UX (step 3) and architecture (step 4), so this dimension matters. The structure supports source-extraction well: a Glossary (§3), contiguous unique IDs (FR-1..18, NFR-1..14, UJ-1..5, JTBD-1..6, SM-1..3, SM-C1..4, OQ-1..15, OI-1..13), and an addendum that names the single source file for each kind of technical detail (addendum §A) plus a CAP → FR → test matrix (addendum §B). Each FR names its CAP and release in its heading, so it reads correctly when pulled out alone. UJs all have the same named protagonist, the supervisor.

What hurts extraction is citation to things a downstream reader cannot open, and a few normative nouns missing from the Glossary.

### Findings
- **medium** Citations to chain-internal artifacts a downstream reader cannot resolve (§5.5 FR-12 bullet 6, §5.6 FR-13 bullet 4, §5.9 FR-16 bullet 1, §9.1 row 11, §10.1 intro, §12.2 OI-6/OI-7/OI-8, §13.2 intro) — "step-1 minor 3/4/5", "step-1 coverage gaps G1-G3, G5-G7", "gap G4", "gap G10", "K1-K12 are extractor row numbers", "U1-U19 are extractor row numbers", plus line-tag shorthands "I:91", "M:463", "V1/V3" with no key. The UX and architecture steps will see these as dangling references. *Fix:* add a one-line key (which file each tag refers to — e.g. `extract-originals.md` for I:n, the step-1 review file path for "step-1 minor n") or restate the content in place. MINOR.
- **low** Glossary misses nouns used normatively (§3) — COUNTS strip, freshness strip, header, "source window", "mark a look"/"last look", `scope=bound`, and "historical row" are used in pinned requirements but undefined; "stage" is overloaded (release stage in §4 vs `projection.stage` in FR-13/FR-14/OQ-15). *Fix:* add these terms; call the releases "release stages" or "R-stages" consistently. MINOR.
- **low** Addendum matrix and FR citation disagree on T9 (addendum §B CAP-2 row; prd §5.2 FR-3 bullet 3) — the matrix lists T9 under CAP-2, and T9 does pin the ledger title `worker-reported, not questions` (acceptance-tests.md:13), but FR-3 cites only rendering-rules.md and owner-decisions-and-risks.md for it. *Fix:* add T9 to FR-3 bullet 3. MINOR.

## Shape fit — strong
This is an internal tool for a single operator role, at the top of a UX → architecture chain. The PRD takes the right shape: a capability spec (FRs with testable consequences, NFRs with thresholds) with light user journeys, and operational rather than user-facing metrics. It is brownfield-aware in the right places (`_find_orca()` in `install_user_setup.py`, risk K9; `cli/main.py` registration, §12.3 item 3) and does not pretend existing code is new. It is not over-formalized relative to the stakes, with one small redundancy.

### Findings
- **low** Jobs are encoded three times (§2.1 JTBD table, §2.1 issue user story, §2.4 UJ list); UJ-5 is a quoted task, not a journey — for a single-operator tool, JTBD-1..4 and UJ-1..4 say the same thing twice. *Fix:* keep one form (the UJs map more directly to the UX step) or accept as-is. MINOR.

## Mechanical notes
- **Assumptions Index roundtrip (low, MINOR).** Inline `[ASSUMPTION]` tags in §5.10 FR-17 bullet 5 and §5.11 FR-18 bullet 3 have no entry in §13.3. Conversely, A1 (§4, "R1 / B / C" maps to R1 / R2 / R3) and A6 (AC 11 as a delivery item, §9.1 row 11 / OI-7) have no inline `[ASSUMPTION]` tag at their location. *Fix:* add A7/A8 for the two "why it matters" assumptions and tag A1 and A6 inline.
- **ID continuity:** FR, NFR, UJ, JTBD, SM, SM-C, OQ, OI and A ids are contiguous and unique. K1-K12 and U1-U19 are declared as extractor row numbers, not source ids (honestly labelled).
- **Coverage claims verified:** addendum §B "every test ID T1-T51 in `acceptance-tests.md` is cited at least once in `prd.md`" — confirmed by search. Addendum §C counts (18 FRs: R0 2, R1 14, R2 1, R3 1; 14 NFRs; 15 OQs; 13 OIs) — confirmed.
- **Verbatim claim verified:** OQ-1..OQ-15 match SPEC.md:99-113 word for word.
- **Stack/spike consistency:** FR-2's "Textual replaces Rich only if it fails" is consistent with the owner-confirmed stack (owner-decisions-and-risks.md:10 records the spike-then-Textual rule as part of the CONFIRMED decision); not a contradiction.
- **Required sections:** present for the stakes — purpose, vision, users, journeys, glossary, staged releases and gates, FRs, NFRs, non-goals, R1 scope, success criteria with counter-metrics, risks, future stage, open questions, assumptions index.

## Finding counts
| Severity | BLOCKING | MINOR | Total |
|---|---|---|---|
| critical | 0 | 0 | 0 |
| high | 0 | 0 | 0 |
| medium | 4 | 2 | 6 |
| low | 0 | 9 | 9 |
| **Total** | **4** | **11** | **15** |

BLOCKING items (all in Done-ness clarity): FR-8 mismatch form; NFR-1 height threshold; NFR-13 Windows verification; FR-17/FR-18 "why it matters" source (R2/R3 only).
