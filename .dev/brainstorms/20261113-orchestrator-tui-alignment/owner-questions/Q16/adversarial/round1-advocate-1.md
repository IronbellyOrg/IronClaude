# Round 1 advocate statement: Variant 1 (promise nothing about trust yet)

Advocate: Variant 1 (proposal A). Persona: analyzer (evidence quality, logical consistency). Mode A, depth quick, round 1.

Sources abbreviated: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; RDA = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/diff-analysis.md`; QF = `Q16/question.md`; DA = `Q16/adversarial/diff-analysis.md`. Line numbers below are the ones I read today.

## Position summary

Variant 1 says: do not answer Q16 now. Keep #409 decision 6 as written, post the #423 and Coder#477 texts with no trust promise either way, and ask Q16 again when the trust layer (SW-12 Phase 4) is scoped.

The case for it rests on three facts:

1. Nothing exists to promise about. MR line 129 and line 201 place the trust layer in Phase 4 of the deferred "manages work" work (SW-12), and QF fact 6 records that "No trust layer, grant format, signing scheme or relay exists today."
2. The evidence for either positive answer is weak. The only adjudication of the point is X-005 at 66 percent, judged "Not decidable from sources; this is an owner decision" (RDA line 89; ADJ line 809).
3. Variant 1 is the spec's own default. MR line 543 gives the default as "PLAN INFERENCE: OB-08 skips decision 6; #423 and Coder#477 promise neither", which is exactly Variant 1's action list.

So Variant 1 is the lowest-commitment answer that still lets OB-08, V2-01 and the CO-01 post proceed, each minus one clause.

After checking the logic, I do not think it is the best answer for the owner. Two defects (a circular hold and a kept one-design sentence) are set out under Concessions. My honest overall verdict favours Variant 3.

## Steelman of Variant 2

Strongest version: a trust mechanism is the one place where "shared words, different machinery" is most dangerous. If #339 owns the only grant format, signing and verification, there is one thing to build, review and test (Variant 2, "What it unlocks"). There is one owner for every trust question. And review 03's Edit 7 bars anyone from inventing a second format: "The grant format is the one chosen in IronbellyOrg/IronClaude#339 ... This issue does not define a second format." (RDA line 89). It also keeps #409 decision 6 unchanged, so OB-08 needs no extra edit.

What it genuinely gets right:
- Drift between three mechanisms under one vocabulary is a real failure mode. Variant 3 admits this itself ("a risk that they drift apart beneath shared words").
- Variant 2 also names its own costs honestly: different threat models, signing does not stop poisoned content, and a commitment to a design that does not exist.

Critique with counter-evidence:
- The only adjudication leans against it. X-005 recommends "One grant vocabulary and one audit record format, not one trust design" at 66 percent (ADJ line 382). The reason given is that "the three consumers have different threat models and signing does not stop poisoned content" (ADJ line 295; #339 comment 2, "encryption alone is not enough").
- Review 03, the source of Edit 7, undercuts its own position. RDA line 89: "V3 itself notes under option A the watcher's trust is 'a different, local model', which supports V4."
- One of the three consumers may never exist. MR line 79 records the Coder#477 listener as "NOT BUILT; premise contradicts the built watcher (design decision D1 option A: no listener)". MR line 353 recommends CO-01 text A "narrow". Binding a not-yet-designed mechanism to a consumer whose premise is contested multiplies the walk-back risk Variant 2 itself names ("three issue texts must change").
- Variant 2 promises a design while also listing, under "What stays unresolved", that "What the design actually is (signing, key handling, scopes); none of it is specified." Promising the shape of a thing whose content is entirely unspecified is the strongest form of the over-promise X-005 warns against.

## Steelman of Variant 3

Strongest version: promise only the part that must be shared for people to read across programs. That part is the names for who may do what, plus one audit record shape. Each consumer keeps the mechanism its own threat model needs. This settles every gated clause today with text the spec has already drafted:
- MR line 456, XC-08 (2): "#409 decision 6 wording becomes 'Decide one grant vocabulary and one audit record.'"
- ADJ line 567: V4 edit 1.

It defers the actual terms to SW-12 Phase 4 (MR line 456, XC-08 (3)). So Variant 3 commits almost as little content as Variant 1, but it removes the blocking question from V2-03, V2-04 and OB-09.

What it genuinely gets right:
- It matches the only adjudicated lean (X-005, 66 percent; ADJ lines 295, 382, 809).
- It is the spec's recommended answer (MR line 543).
- It is consistent with review 03's own note on the watcher's local model (RDA line 89).
- Its unique contribution U-003 (grants from three programs readable side by side) gives OB-09 (4) a concrete target: "every answer path is audited in the vocabulary of XC-08" (MR line 257).
- It states its own limit correctly. MR line 574 says "Q16's vocabulary does not authorize relay", and Variant 3 repeats it.

Critique with counter-evidence:
- The 66 percent is not strong evidence. The point is "Not decidable from sources" (RDA line 89). Variant 3 still turns a coin-flip-plus adjudication into public text in three issues.
- Shared words can hide unequal protection. Variant 3 concedes "the same word ('grant', 'read') may mean weaker protection in one program than in another". It offers no guard beyond deferring the definitions.
- Evidence hygiene: Variant 3 cites OB-09 at "(line 398)". On my read, MR line 398 is the V2-01 row, and OB-09 is at MR line 257. The fact is right, but the citation is wrong.
- The vocabulary-plus-audit promise inherits a dependency on SW-12 Phase 4, which is DEFERRED with no date (MR line 201). The promise could stay an empty commitment for a long time. That is still less harmful than an empty design promise.

## Strengths claimed

1. It is the default, so choosing it costs zero new decisions. MR line 543's default column matches Variant 1 step for step: OB-08 skips decision 6; #423 and Coder#477 promise neither.
2. No public text commits to a trust shape before a design exists. QF fact 6 and MR line 201 confirm that the trust layer is unbuilt and deferred. Variant 1 is the only answer that adds no new trust wording to any issue.
3. The non-trust work is not blocked. OB-08, V2-01 and the CO-01 post proceed with one clause left out (Variant 1, "What it unlocks"). This matches MR line 256, OB-08 (4): "decision 6 only if Q16 = vocabulary", so the pass is designed to run without it.
4. It respects the evidence grade. Given "Not decidable from sources" (RDA line 89), declining to choose is a defensible reading of weak evidence.
5. U-001, re-asking with a real design in view, is a sound principle. Even the recommended Variant 3 leaves the actual terms to SW-12 Phase 4. So the substantive trust choice is made later in every variant.

## Weaknesses identified in others

- Variant 2: it commits three issues to an unspecified design. It runs against the only adjudication (ADJ line 382). It binds a consumer (Coder#477) whose premise the spec says contradicts the built watcher (MR line 79). It keeps #409 decision 6 "as intended" although two reviews flagged the sentence (ADJ line 567, line 809).
- Variant 3: it relies on a 66 percent, not-decidable-from-sources lean. It names a drift risk without a guard. It has one wrong line citation (OB-09 "line 398").
- Both positive variants treat Coder#477 as a settled consumer. MR line 79 and line 353 show that its scope is still open (Q3 picks text A, B or C).

## Concessions

These are the genuine weaknesses of Variant 1. As analyzer I weigh them as decisive.

1. **Internal inconsistency.** Variant 1 is titled "promise nothing about trust yet", yet it keeps #409 decision 6: "Decide one design, not two." That sentence is itself a one-design promise, live in a public issue. So Variant 1 does not promise nothing. By default it leaves Variant 2's promise in #409 while withholding it from #423 and Coder#477. That inconsistency across issues is worse than either positive answer, and Variant 1's own cost list admits it: "Readers of #409 may keep designing toward one shared design."
2. **Circular hold.** Variant 1 says held work waits "until the question is asked again when SW-12's Phase 4 row in #534 is opened". But MR line 201 lists XC-08 among SW-12's blocked-by items, and says "Phase 4 uses the vocabulary from XC-08". MR line 830 shows "Q16 -> XC-08 -> {OB-08, V2-01, V2-03, SW-12, V2-04, OB-09}". So the trigger Variant 1 names for re-asking depends on the answer it postpones. In practice, someone must break the cycle by hand, or the ledger's "deferred, default applies" must be read as satisfying XC-08 (1). The second reading is UNVERIFIED: XC-08 (2) and (3) are written only for the vocabulary answer.
3. **Its main benefit is available inside Variant 3.** Variant 3 also defers the actual terms to SW-12 Phase 4 (XC-08 (3)), so U-001's "decide content with a design in view" is preserved there. Variant 1's remaining distinct benefit is only that no new trust wording is posted. That is small, because the vocabulary wording is narrow and reversible by issue history (ADJ line 189, "Undo: yes, issue history").
4. **Evidence hygiene.** Variant 1 cites "merged-requirements.md line 257, step (4)" for OB-08's decision 6 step. On my read, OB-08 is at MR line 256 and line 257 is OB-09. The same kind of off-row citation appears in QF: V2-01 is given as "lines 401 and 730", but V2-01 is at MR line 398 and V2-04 at line 401; CO-03 is given as "line 400", but it is at MR line 355. The facts survive, but the row numbers do not.
5. **The question returns at a worse time.** Variant 1 says so itself. Later text may rest on the kept sentence, and an extra round of issue edits is guaranteed.

## Shared assumptions

- **A-001** (the three consumers are the complete set; the watcher is outside it): **QUALIFY.** The set may be smaller, not larger. The Coder#477 listener is NOT BUILT and its premise contradicts the built watcher (MR line 79). The watcher's own trust is a local model under option A (RDA line 89), and D1 option A means "no listener, inbound port or address registry" (MR line 294). This matters most for Variant 2, which binds all three. Variant 3's separate-mechanisms answer tolerates a changing consumer set best.
- **A-002** (issue text is cheap and reversible): **QUALIFY.** It is true today: ADJ line 189 and line 382 mark the edits "Undo: yes, issue history". It stops being true once SW-12 Phase 4 code is built against the promise. Variant 2 is most exposed, because it scopes Phase 4 as the single design that all consumers import. Variant 1 is also exposed, because code may be designed toward the kept "one design" sentence in #409.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie; Variant 3 if forced | 40% | All three use the same five sections, so there is no real difference. |
| C-001 | Variant 3 | 65% | The rewrite matches the adjudicated lean (ADJ line 382) and the drafted text (MR line 456). Variant 1 leaves a flagged one-design sentence live. Variant 2 endorses it against the evidence. |
| C-002 | Variant 3 | 65% | It promises only what can be shared across different threat models. Variant 2's Edit 7 binds a contested consumer (MR line 79). Variant 1 makes #423 and Coder#477 inconsistent with #409. |
| C-003 | Variant 3 | 60% | It gives a named home (SW-12 Phase 4, XC-08 (3)) without the cycle in Variant 1's trigger (MR lines 201, 830). Variant 2 names the same home for a much larger commitment. |
| C-004 | Variant 3 | 70% | Every gated item gets a settled clause at low commitment. Variant 1 leaves V2-03, V2-04, OB-09 and SW-12 Phase 4 held behind a circular trigger. |
| C-005 | Variant 3 | 70% | It routes poisoned content to an existing separate rule (relayed text stays data, V2-04; MR line 401). Variant 2 only names the risk, and Variant 1 does not address it. |
| X-001 | Variant 3 | 62% | Different threat models (ADJ line 295) and review 03's own local-model note (RDA line 89) favour separate mechanisms. Undecided (Variant 1) settles nothing. |
| X-002 | Variant 3 | 65% | The narrow promise is cheap and reversible (A-002 holds today). Variant 1's "premature" is right for a design but not for words plus a record shape. |
| X-003 | Variant 3 | 64% | Two reviews flagged the sentence, and the adjudication rewrites it only if Q16 = vocabulary (ADJ line 567). Keeping it is a live over-promise. |
| U-001 | Variant 1 | 70% | Re-asking with a real design in view is sound and unique to Variant 1, though Variant 3 can absorb it by deferring the terms. |
| U-002 | Variant 2 | 60% | A bar on a second format is a real anti-drift guard that neither other variant offers in that strength. |
| U-003 | Variant 3 | 70% | One audit format gives OB-09 (4) a concrete target (MR line 257) and keeps grants readable side by side. |
| A-001 | Variant 3 | 55% | Separate mechanisms survive a consumer set that shrinks (Coder#477) or grows (the watcher). |
| A-002 | Variant 3 | 55% | Its committed text is the smallest that still settles the clauses. Variant 1's kept sentence and Variant 2's single design are both what code could harden around. |

## Overall

Variant 1 is the spec's default and honestly the most cautious answer. But it is internally inconsistent: it keeps a one-design sentence in #409 while promising nothing in #423 and Coder#477. Its re-ask trigger is also circular: SW-12 Phase 4 is itself blocked by XC-08, which needs Q16. Variant 3 keeps Variant 1's main virtue, because the actual trust content still waits for SW-12 Phase 4. It also matches the only adjudication (66 percent, weak but non-zero) and settles every gated clause with reversible text. Variant 2 commits the most against the evidence, and binds a consumer whose premise is contested.

Overall: the variant I judge best for the owner is Variant 3, confidence 65%
