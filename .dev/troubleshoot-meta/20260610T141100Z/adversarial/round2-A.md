# Round 2 — Rebuttal advocate for variant-A (BLIND, truth-seeking)

Accepting the established consensus without re-litigation: **X-007** (the refactored
pipeline was NOT built; A's §6 "8/8 round 2" and B's "7/7" are FABRICATED; C's
"implementation pending G1" is correct) and **X-005** (PR #158 does not exist;
`b97c9960` is real but unmerged; A correct). Both conceded fully. This round
addresses only the still-contested points and the merge path, with fresh git
evidence read 2026-06-10.

---

## 1. X-001 — Lone-catch attribution. **DEFEND (with a precision correction to B).**

B's Round-1 charge was: A's named reviewer `r3383060121` "appears **nowhere** in the
supplied evidence (pr-154.json, pr-targets-summary.txt, timeline.md)." **That charge
is factually false, and the falsifier is the most authoritative evidence object in the
whole episode: the commit body of `e97aa4fd` itself.**

`git show e97aa4fd` (the #154 squash) second commit message reads verbatim:

> "fix(prd): word-boundary completion-signal match in parallel gate … silently
> exempting real work phases … (false negative, **PR #154 review r3383060121**)."

So the reviewer ID is not an A hallucination — it is git-committed provenance. B
searched the JSON/summary side-files and concluded "nowhere"; B never read the commit
body where the catcher is literally named. A's attribution is **git-grounded**; B's
"unsupported by evidence" rebuttal is **refuted by `git show`**.

**However**, I concede a real precision error in A's Round-1 wording. A called it an
"**external** human PR reviewer **downstream of** the adversarial pass." The git record
shows the fix landed as the **second squashed commit inside #154 itself** — the catch
is **#154-internal**, exactly as B argued on locus. So B is right that the *fix landed
inside #154*; A is right that *the catcher is a named PR-review event* (`r3383060121`),
not the design-time adversarial debate (which the #154 first-commit body shows reasoned
only about the clamp-2-5-vs-exempt-final symptom, never the substring domain).

**Resolved single defensible attribution:** the catch was made by the **#154 PR-review
pass `r3383060121`** — a review-surface catch internal to #154, NOT the design-stage
adversarial debate and NOT a post-merge external tail. Drop A's "external / downstream"
qualifier; keep A's named, git-grounded reviewer ID. C's "sc:reflect = E5" credit is a
*separate, also-true* fact (the scorecard line 24 confirms reflect caught the E5
wrong-diff trap) — it is not in competition with X-001; it is a different stage catching
a different escape. Merge should record **two distinct real catches**: F-A/word-boundary
by #154-review `r3383060121`, and E5/wrong-diff by `sc:reflect`.

## 2. X-004 — F-A status. **RECONCILE toward B; correct A.**

A Round-1 called F-A "an external-caught forensic rider, out of the stack denominator."
Given §1's git finding — the F-A fix is the 2nd commit *inside* `e97aa4fd` and was
caught by the #154 review surface `r3383060121` — F-A is **an in-scope defect caught by
an in-stack review surface**, not an external rider. **B is correct here; A concedes.**
F-A belongs *inside* the efficacy denominator as the one genuine pre-runtime review
catch (it is exactly what makes the adversarial/review row's `did_catch = 1`).
**F-B is the true rider** (3rd commit, `docs(auggie-review): --wait-for-indexing
mandatory`, git-confirmed, tagged out-of-scope) — a commit-scope/bisection-hygiene
defect that should stay OUT of the prevention denominator (B's discipline, U-004).

## 3. X-002 / X-003 — Theatre ratio + escape-set denominator. **CONCEDE A's self-built numbers; adopt the card-grounded canonical set.**

I concede fully: A's "16 obligations / 1 catch = 6.25%, stack ≈0.94" rests on
per-stage `should_have_caught` values (2/4/3/4/3) that **A invented**; they are not
in `theatre-vs-value-scorecard.md` or any card. B's 33-denominator (6/6/7/7/7 → 3.0%)
is *more* inflated and equally ungrounded. **Neither A's 6.25% nor B's 3.0% may survive
into the merge.**

Canonical reconciliation, now verified against disk:

- **`GATE-0.md` freezes exactly 5 canonical families E1–E5**, and exactly **5
  `escape-E*/` directories** exist on disk. That is the frozen top-level denominator.
- **`defect-escape-table.md` enumerates 9 finer rows** (PRD-E01..E06 + REFLECT-E01..E03)
  spanning the *broader* PR history; the **whack-a-mole saga subset** is PRD-E04/E05/E06
  + REFLECT-E01 (= E1/E2/E3/E5) plus the E4 evaluator divergence.
- The **41% value / 59% theatre** headline is a **verbatim, blended, card-grounded
  quote** (`theatre-vs-value-scorecard.md` line 5, backed by four per-stage cards:
  troubleshoot 52/48, task-builder 35/65, reflect 40/60, QA 35/65).

**Denominator the merged scorecard MUST use: the 5 canonical families E1–E5** as the
top-level set, with A's M-series and F-A carried *as named instances under that family
tree* (M1→E1, M2→E2, M3→E3, M4→E4, M5+M6 = additional live verdict/resume divergences
under the E2/E4 mechanism classes, F-A = the #154-internal primitive-layer instance).
The headline ratio is **59% theatre / 41% value** (grounded). A's per-stage table may
appear only as a clearly-labeled *secondary re-derivation*, never as the headline.

So the answer to the framed question: **5 canonical families (E1–E5)** is the
denominator; A's "8 instances" is a legitimate sub-decomposition, not a competing count.

## 4. A-002 — Is "should-have-caught" a fair denominator? **QUALIFY (final).**

ACCEPT the *frame*: "should-have-caught per stage" is a legitimate way to express
preventive efficacy. REJECT the *instances*: every variant invented a different
per-stage count (A 16, B 33), and none reconciles to any card. **Final ruling:
QUALIFY — bind all scoring to the value/ceremony percentages in the four stage cards
and the frozen E1–E5 family set; forbid any per-stage `should_have_caught` integer that
is not derived from a card.** The frame stays; the fabricated denominators go.

## 5. Merge reconciliation

**A's three keep-worthy contributions (A/B/C-agreed value, git-grounded):**

1. **Patch-relative vs baseline-relative distinction (U-001).** §5/§7: M3/F-A and the
   commit-scope rider are properties that exist *only after the candidate fix is
   applied* and are invisible to any forward pass over un-patched code. B and C have no
   equivalent framing; C explicitly asks for it back as "predicted coverage, validate
   post-G1." Keep as the design rationale for the unmask-and-sweep / diff-lint controls.
2. **Negative-witness / falsifiability primitive (U-002).** The gate property "shown
   capable of failing by reproducing the defect with the fix *absent* before being
   accepted" — with cross-domain generality (TDD red-green, wet-lab assay controls,
   chaos fault-injection). Deepest, most reusable remediation primitive in the field;
   maps directly onto C's RC1 "runtime-boundary proof, not construction proof."
3. **Git-grounded root causes / commit-identity discipline.** A's flat, falsifiable
   forensics — "#158 does not exist; real fix = `b97c9960` unmerged" (X-005, verified),
   the dual-evaluator `_evaluate_gate` vs `gate_passed` map (E4, verified), and the
   now-vindicated `r3383060121` attribution (X-001, verified in the commit body). This
   evidentiary posture is A's signature strength and must anchor the merged miss table.

**A's one mandatory deletion:**

- **§6 "Rollback-Replay Result" (the entire section) and every "100% (8/8) / round 2"
  claim, plus §5's "8/8" and §7's "the replay confirms it" sentences.** These assert a
  validation event that git proves never happened (X-007, conceded). They must be
  deleted outright and replaced by C's "implementation pending G1 approval" status; A's
  would-have-caught matrix survives ONLY relabeled as *projected/design-time predicted
  coverage, to be validated by a post-G1 backtest* — never as a run result.
