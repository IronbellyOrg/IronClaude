# Variant 3 (architect): K-arm lead-in, DD-14

SW, RL, MR as in the evidence pack; I re-checked F1-F11 on disk and found no error. Real-model effects of any wording are UNVERIFIED (F9).

## 1. Position

Yes. The draft is inside the acceptable range for a fair K. It is a plain, non-leaking checklist that meets MR 1035 and REQ-40; its weak points (no verb telling the reviewer to apply the checks, "in your own review" next to CB-5, the word "checks" missing) read differently and cannot be shown to move D7.

## 2. Requirements for a fair, strong K

1. Name all eight classes in plain words, one paragraph, no recipe, sheet or ledger (MR line 1035).
2. Differ from Z0 only by the checklist, so K minus Z0 is the prompting share (REQ-40, MR line 1194; SW/DESIGN.md:788).
3. Be a real checklist, not a strawman: D7 says "otherwise K wins" (MR 1091). With D2 at 0.12 and D7 at 0.04 (SW/analysis/analyze.py LIMITS ~481-495; gate_d7 727-736, a point difference), D7 fails only if K minus Z0 exceeds about 0.08 (F6 arithmetic, derived).
4. Not exceed a checklist: no per-item verdict, location or method, or K turns into SS or RL (MR 1100, "K within 0.03 of RL").
5. Agree with the shared parts CB-2 and CB-5 (SW/briefs/cb2.txt, cb5.txt:1) and leak no hold-out detail (MR 1026, REQ-33; SW/bin/freeze.sh:43).
6. Neither push nor suppress findings (SW/briefs/base.txt: "not a minimum number of findings"; cb2.txt: "Do not leave a defect out").

## 3. My design

Exact bytes (one line, no trailing newline), followed by the existing " (1) <definition> ... (8) <definition>" from `k_paragraph` (SW/scaffold/briefs.py:90-107):

`Here are the eight checks. Apply each one to the plan. Each one says what to look for. A plan may fail none of them, one of them or several.`

140 characters, 30 words (measured with wc). The draft is 151 characters, 33 words (SW/briefs/k-lead.txt:2).

Why: "checks" is the owner's word (MR 1035) and the word CB-5 already uses ("The checks you were given", cb5.txt:1), so CB-5 no longer points at something unnamed. "Apply each one to the plan" is the smallest instruction that matches the SS sheet's "Do not skip an item" (sheet-block.txt:1) without a ledger or a method. I drop "in your own review" because CB-5 itself keeps the checks apart from the free review. I keep the symmetric "none, one or several" sentence: base.txt already says no minimum number, and CB-2 says list everything, so nothing pushes the reviewer to invent a finding or to hold one back.

## 4. Draft against design

| Difference | Bias direction | Can it change D7 or K-versus-RL? | Cost to fix |
|---|---|---|---|
| Draft has no apply verb: "Eight kinds of defect to look for in your own review" (k-lead.txt:2) against my "Apply each one" | Toward SS looking better (a softer K gives a smaller K minus Z0) | In principle yes: D7 flips only if K minus Z0 crosses about 0.08 (F6). Size of the effect UNVERIFIED (F9); the sentence still reads as a checklist | One sentence, in both workspaces, before the freeze |
| "in your own review" against CB-5 "do not replace your own review" (cb5.txt:1) | Unknowable (K reviewers may count the checks as part of free time) | No: D7 reads found fraction only (analyze.py:594-603, 727-736); time is not an input | Delete four words |
| "kinds of defect" instead of "checks"; CB-5 comes before K and names "the checks you were given" | Unknowable | No: a forward reference exists in either wording | Zero once the word is changed |
| Definition (2) says "driving document" while CB-1 may be absent (cb1.txt; SW/DESIGN.md:563, 273) | Toward K looking slightly worse on a no-source document (a vacuous check); SS gives no C2 item there | Only if scoring counts C2 items on a no-source document: UNVERIFIED (F9). Same in my design | A card edit, not a lead-in edit (cards are still unfrozen, F7) |
| Length and tone: K adds 1,226 characters, SS 1,712 plus a sheet up to 16,000 (F3); SS adds a quote-proof rule (sheet-block.txt:1) that K lacks | Unknowable | No: the difference is the tested variable (MR 1035) | None |
| Permission to find nothing: same sentence in both | None | No | None |

## 5. Answers to F11

Q1 Fair, strong control? Fair: same documents, judge and clock (F6). Strong enough: all eight classes named in the card definitions (SW/cards/C*.json), inside the owner's "plain words" range (MR 1035); a little soft on the apply verb. MR 120 predicts a plain checklist helps little, which K tests. Not blocking.

Q2 Leak? None. The lead-in carries only the number "eight" (k-lead.txt:2); definitions are target-neutral card text frozen before the ground truth (F7). Approving the lead-in does not approve the definitions (swap_test empty, F7). Not blocking.

Q3 Length and tone confound? K is plainer and shorter by design (F3, F5); the SS extras are the machinery under test. Not blocking.

Q4 Does "a plan may have none" discourage findings? No. It is symmetric ("none, one or several"), base.txt says "not a minimum number of findings" and cb2.txt says "Do not leave a defect out". SS is stricter ("Most items are fine", sheet-block.txt:1). Not blocking.

Q5 Equivalent in information to SS? No, by design: K gives eight definitions; SS gives location, literal text, tool output and a question per triggered class, and not the definition (F5; MR 1035 "No recipes, no sheet"). That gap is what D7 and the K-versus-RL row measure. Not blocking.

## 6. Verdict-rule tests

(a) Unfair to an arm: no. Same documents, judge and clock (F6); K sits last after CB-5 (SW/scaffold/briefs.py part_names, F3).
(b) Unmeasurable: no. Prompting share is K minus Z0 (DESIGN.md:788); gate_d7 is computable (analyze.py:727-736).
(c) Misleading: not on the evidence. The one live risk is a soft K making D7 pass; that needs K minus Z0 above 0.08 to flip, which is untested (F9), and D7 is reported as a point gain, not as proof (MR 1106).
(d) Breaks a stated requirement: no. MR 1035 (one paragraph, eight checks, plain words, no recipe, sheet or ledger), REQ-40 and DD-14's single governing source for class wording are all met; the draft marker is a comment that is never sent (test_briefs.py:187-204).

## 7. Strongest case against my design

It splits the shared control: RL/briefs/k-lead.txt is byte-identical (cmp, F1) and RL DESIGN.md:91 (DR-16) calls it one shared decision. Any change needs a matching RL edit before step 14.5 (VERDICT N8). My text is as untested as the draft (F9). "Apply each one" could be read as a procedure and lift K above a plain checklist, making D7 harder for SS for a wording reason: the same unfairness the other way. The owner asked for approval, not a rewrite.

## 8. Blocking?

NO. No blocking defect (BD) found.

Non-blocking notes:
- N-1 The lead-in has no verb telling the reviewer to apply the checks (k-lead.txt:2). Suggest "Apply each one to the plan." Leans toward SS winning D7 if it matters.
- N-2 "in your own review" blurs the line CB-5 draws (cb5.txt:1). Suggest dropping it.
- N-3 K never uses the word "checks", although CB-5 and MR 1035 do. Suggest "the eight checks".
- N-4 Definition (2) names a "driving document" that CB-1 never names when there is no source (DESIGN.md:563). UNVERIFIED whether any decision document lacks a source; fix, if wanted, in the card at step 14.2.
- N-5 If edited, change SW and RL together before step 14.5; the draft marker on line 1 stays, as test_briefs.py:187-204 pins it.
