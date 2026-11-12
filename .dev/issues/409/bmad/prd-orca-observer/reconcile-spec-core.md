# Input reconciliation: spec core vs PRD

- Input set: `_bmad-output/specs/spec-orca-observer/` SPEC.md, acceptance-tests.md, release-gates.md, owner-decisions-and-risks.md
- Under review: `_bmad-output/planning-artifacts/orca-observer/prd.md`, `addendum.md`
- Reviewer date: 2026-11-08. Read-only review; no source file edited.
- Paths below: `S` = SPEC.md, `AT` = acceptance-tests.md, `RG` = release-gates.md, `OD` = owner-decisions-and-risks.md, `P` = prd.md, `AD` = addendum.md.

## What passed (checked, no gap)

- All 15 SPEC open questions (S:99-113) appear verbatim as OQ-1..OQ-15 (P:412-426); confirmed by a mechanical diff. None is resolved.
- CAP-1..CAP-12 each map to an FR or NFR (AD:32-43). All six SPEC non-goals (S:80-85) are in P:281-286.
- Recorded owner decisions 1-5 (OD:9-13) are carried: 1 at P:94, 2 at P:129, 3 at P:382, 4 at P:89/P:276, 5 at P:18-19.
- Risk table (OD:39-52) copied verbatim as K1-K12 (P:354-365). All five dissents (OD:56-60) are at P:367.
- Data-gate rule with the four sample kinds (RG:5) is quoted at P:96 and SM-3 (P:335). Stricter production-integration reading (RG:29-34) is at P:109 and P:287.
- SPEC Assumptions (S:93-95) are at P:457-459. Every T1-T51 is cited somewhere in prd.md (mechanical check). Evidence labels UNVERIFIED / PROPOSED / CONTRADICTION are kept where the sources use them.

## Gaps

### G1 BLOCKING - Open owner decisions 1-10 and their recommendations are not carried
- Source: OD:15-26. Each open decision carries a recommendation and conditions: (1) "A plus the COUNTS strip for R1; B after QUESTION-OBSERVATION with A one key away; C behind QUESTION-LINK. V3 dissents"; (3) register in `cli/main.py` (deferred import, then `add_command`); (5) "Recommend A on the same adapter as the re-confirm option"; (6) acquisition permission "must cover the actual read scope before any message call, separate from display and export. Recommend yes, owner sets redaction rules"; (7) display and export "kept as separate permissions"; (8) "Recommend an explicit message type, never text inference"; (9) "Caps are per process, no singleton. Recommend disclosure only".
- PRD: P:20 promises "Open owner decisions are carried, never decided (section 12)", but section 12 (P:408-451) carries only the one-line SPEC open questions. None of the recommendations, the separation of acquisition vs display vs export permission, or "never text inference" appears anywhere (grep for `one key away`, `cli/main.py`, `redaction`, `text inference`, `singleton`, `disclosure only` in prd.md: no hits).
- Fix: add a 12.x "Open owner decisions (OD:17-26)" list with each recommendation verbatim, labelled as a recommendation, not a decision.

### G2 BLOCKING - CAP-4 "mismatch" form and T47's notes dropped from the FRs
- Source: S:41 CAP-4 success "PARTIAL, STALE, FAILED, mismatch and `n+? (k unknown)` forms render exactly as pinned"; AT:41 T47 "`changed during read`, mismatch, `revisit ~Ns` and empty-rotation-set notes render per `rendering-rules.md`".
- PRD: FR-8..FR-10 (P:168-184) cover PARTIAL, STALE, FAILED and `n+?` but never the mismatch form; FR-7 (P:161-162) cites T47 only for the notice and `result.count`. No hit for `mismatch`, `changed during read`, `revisit`, `rotation` in prd.md.
- Fix: add a FR-8 or FR-10 consequence for mismatch / `changed during read` / `revisit ~Ns` / empty rotation set, citing T47.

### G3 BLOCKING - QUESTION-OBSERVATION gate content distorted by omission
- Source: RG:38 candidate verb `orca orchestration check --all --run <runId> --json`, "A candidate, never an available source, until all are recorded"; RG:42 the label stays after the gate including "bursts over 100 rows between reads may be lost"; RG:43 "Help text and an empty peek `count` cannot clear the gate"; RG:44 "A worker `dispatchId` is never a question's identity"; RG:45 decision 6 must cover the read scope "before any call".
- PRD: the R2 gate row (P:103) lists proofs (a)-(c) but omits the candidate verb and its "never an available source" status, the help-text/empty-peek exclusion, the "dispatchId is never a question's identity" rule, and "before any call". FR-17 (P:245) keeps "bounded best effort; coverage unknown" but drops the "bursts over 100 rows ... may be lost" clause and that the label survives the gate.
- Fix: extend P:103 / FR-17 with these clauses verbatim.

### G4 MINOR - DIRECTION-SELECTED evidence kinds and fallback rule shortened
- Source: RG:25 Stale: "a later gate that changes what a direction can show, or the fallback date passing, triggers a re-confirm"; RG:26 Contradictory: a selection whose data gate has not passed "ships only an owner-accepted gated fallback with the reason on screen, or stays blocked"; RG:48 "If A is picked, A stays the default on the same adapter and renderer; B's retention model stays in the code ... (one layout function, not a rewrite)".
- PRD: P:111 keeps "never grants permission to switch" and "a selection never clears a gate", but drops the gated-fallback-with-reason-on-screen behaviour, the "later gate changes what a direction can show" trigger, and the A-stays-default / B-retention-kept clause. Also P:111 attributes the "expiry never grants permission" sentence to the fallback rule; in the source it is the DIRECTION-SELECTED Stale clause (RG:25).

### G5 MINOR - Test consequences dropped from FR text (tests still cited)
- T32 (AT:21): `FAILED (shape)` with the last good snapshot kept; `page.total` absent shows `reported unknown`; inner `projection.*` field missing gives `unknown`, not an error. P:138 says only "fails on any missing required field" (faithful to S:35 but loses the graded behaviour and the last-good-snapshot rule). `reported unknown` also absent from FR-8 (P:170).
- T22 (AT:18): older `observedAt` never overwrites newer; `order unknown`; `conflict (time went back)`. P:144 keeps only `k duplicate rows ignored`.
- T20 (AT:17): `worktree unknown`; "no count divides one by the other". P:145 omits both.
- T16 (AT:16): every count line `k of n`, hidden overflow `x/y shown` with y = fixture total. P:124 omits.
- T40 (AT:34): overrunning call killed, strip shows `cycle overran (Ns)`. P:176 omits.
- T46 (AT:40): `unknown (retention exceeded)` with the retained count, oldest first. P:244 omits (only in risk K7, P:360).
- T19 (AT:16): `at most 100 rows per read, not 100 questions`. P:246 omits the string.
- T21 (AT:18): historical rows "listed with `terminalState`, not counted active". P:150 omits.
- T34 (AT:28): fixture mode renders `FROZEN`. P:191 carries only the live half.

### G6 MINOR - Later-stage gates collapsed into one inaccurate row
- Source: RG:15 closure evidence gate "A source recording explicit resolution (e.g. a reply row linked to the question ID)", adds "closed items move to a closed list"; RG:16 history gate "Durable, non-consuming message history or event replay"; RG:17 "Each needs its own feed" applies only to admission/verification, cost, deep links.
- PRD: P:106 merges all into one row with "Each needs its own feed", misattributing that gate to closure evidence and history.

### G7 MINOR - R0 deliverables and settled items shortened
- RG:9 R0 adds "Render timing and per-call timeouts measured" and lists the degraded versions (unavailable, PARTIAL, gap notice, `read k of N Runs since start`, "bounded best effort", "affected scope unknown") plus C's walkthrough task. P:100 says only "renders of A, B and C for review"; render timing is absent everywhere; the walkthrough appears only as UJ-5 (P:67), not as an R0 deliverable.
- OD:31 "100-row window for the question panel, with disclosure and observer-side retention, until durable history exists". P:113 drops "with disclosure and observer-side retention, until durable history exists".

### G8 MINOR - Debate-record notes (qualitative) dropped
- OD:62-66: 16 vs 14 MEDIUM findings both correct; X-001 "the design prototype does not match the seed brief's claim that Signal Bridge collapses at 116 columns; the prototype is visual reference only"; INV-019 design defect resolved but no selection record exists. None appears in the PRD (no hit for `X-001`, `INV-019`, `16 MEDIUM`; `prototype` only in NFR-14 at P:276). X-001 is a design-relevant caution for the UX step.

### G9 MINOR - Untagged PRD additions
- P:104 "No named decider beyond that." Not in RG:13; untagged.
- P:434 OI-4 "two of three advocates recommend B". OD:17/OD:57 say only "V3 dissents (C post-link)"; the "two of three recommend B" claim is not in this input set (may be in merged requirements, outside it). Cite or tag `[ASSUMPTION]`.
- P:443 OI-9 applies the CONTRADICTION label to OD:17 vs OD:57; the source does not label it so. It sits under "found while writing this PRD" (P:428) but is not tagged `[ASSUMPTION]`.
- AD:32-39 traceability lists add tests the spec does not cite for that CAP (CAP-1 adds T7; CAP-2 adds T13, T17, T45; CAP-4 adds T5; CAP-8 adds T3, T25, T35) without marking which are PRD additions versus spec citations (S:32-53).

### G10 MINOR - Owner-decision label convention not followed
- OD:3 requires "recorded owner decision N" vs "open owner decision N". P:129 "owner decision 2", P:382 "owner decision 3", P:451 "owner decision 4" drop the qualifier. P:451 is ambiguous: open owner decision 4 is the production-integration boundary (OD:20), while recorded decision 4 is the TUIBBS one (OD:12) that P:451 means.

### G11 MINOR - Test harness and fixture variant list not referenced
- AT:5 harness (`Console(width=W, record=True, ...)`, `export_text()`, fake runner, no TTY, no live Orca) and AT:7 the ten fixture variants. The PRD names only some variants in passing (P:137, P:243, P:359) and never lists the set; AD:22 points to `acceptance-tests.md` generally. Acceptable given the addendum pointer; flagged so step 4 does not miss it.

