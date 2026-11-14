# Round 1 advocate: Variant 2 (no number now; keep the interim rule)

Persona: qa (edge cases, failure scenarios). Sources read 2026-11-14: Q22 `question.md`, the three variants, `diff-analysis.md`, `merged-requirements.md` lines 279, 354-356, 549, 1196, ADJ (`alignment-findings-adjudicated.md`) lines 222, 228, 250, 634, 792, and `src/superclaude/cli/observe/{collector,view,export,commands,parse}.py`.

## Position summary

No reader of the snapshot or of a Coder workspace record exists (CO-03 and CO-04 are DEFERRED, `merged-requirements.md` lines 355-356), and the code shows that `generatedAt` measures when the file was written, not when the data was last good; so any number fixed today is fixed against an unbuilt reader and an under-specified measure. V2 defers the number until a real reader is designed, which CO-02 item (1) explicitly permits. V2's interim one-cycle rule is, however, defective (it flickers), and V1's three-interval rule is the better interim rule.

## Steelman

**Variant 1 (3 x the producer's interval).** Its strongest form: the observer already defines "stale" as three missed 15 s polls (`view.py:32-34`, `STALE_SECONDS = 45.0  # three intervals without a successful poll, on the monotonic clock`), so V1 gives a file reader the same meaning the screen uses, which directly serves the mapping-table rule "never show one as the other" (ADJ line 250). It tolerates ordinary jitter and the 15 s cycle budget (`collector.py:28-29`), it does not invent a number for the Coder producer that does not exist (it defers that number to CO-03 just as V2 does), and it adds no key to the snapshot, so "publishes nothing new in version 1" (ADJ line 222) holds. It is in substance V2's deferral plus a better interim rule.

**Variant 3 (fixed 2 minutes).** Its strongest form: the owner was asked for "the owner's number" (`merged-requirements.md` line 549), and V3 gives one, closing the visible `[N minutes: owner decides]` placeholder in Coder#477 (ADJ line 634). One number needs no lookup table, and 2 minutes is above the observer's longest backoff wait (`MAX_BACKOFF = 60.0`, `collector.py:30`), so a live observer in backoff never makes its file look stale. Setting a service level early also constrains the CO-03 and CO-04 designs before they drift.

## Strengths claimed

1. **It is the only variant that refuses to fix a requirement on code that does not exist.** No reader exists today: CO-03 and CO-04 are DEFERRED (`merged-requirements.md` lines 355-356). CO-02 item (1) already allows "the line keeps the placeholder with 'owner decides' and the reply says so" (line 354), so V2 blocks neither XC-05 nor CO-02. CO-04 itself requires that "an age rule (Q22)" be specified when it is opened (line 356), which is exactly when V2 asks again.
2. **The code shows the measure is not settled, which favours deciding against a real reader.** The live loop writes the snapshot "exactly one write per cycle, after failures too" (`commands.py:294-297`), and `generatedAt` is the write time, `format_utc_iso(clock.wall())` (`view.py:555`). A failing observer therefore keeps producing a file with a fresh `generatedAt` while its data is old; the data age is in a different key, `source.observedAt` (last successful read, `view.py:548-551`, `export.py:190`), next to `source.status` OK/STALE/ERROR (`view.py:547`, `export.py:189`). A threshold on `generatedAt` alone, whatever its value, detects a dead observer but not a stuck one. The spec already says readers must "distinguish feed age, stored-file age ... and per-row evidence age" (`merged-requirements.md` line 279). Which age gets which number is a reader design choice; none of the three variants addresses it, and V2 is the one that leaves room to decide it with the reader in hand.
3. **It errs in the safe direction.** A short threshold calls a file stale too early, never current too late; with the age always printed, a person is never told an old file is current, matching "An old snapshot is not a current process heartbeat" (line 279).
4. **No posted text needs editing later.** V3's own risk section concedes that changing the number later "means editing posted issue text"; V2 posts nothing that must be retracted.
5. **It found the defect in the ADJ default (U-002).** V2 is the only variant that states the interim one-cycle rule flickers with ordinary jitter (variant-2 "What it costs or risks"). Cycle starts are 15 s apart and a cycle may run up to 15 s (`collector.py:28-29`), and `generatedAt` is truncated to whole seconds (`parse.py:268`, format `%Y-%m-%dT%H:%M:%SZ`), so a one-cycle threshold is crossed by normal operation.

## Weaknesses identified in other variants

1. **V3 reports a dead observer as current for up to 2 minutes.** When the observer process exits, the file stays on disk with no pid or liveness flag (ADJ line 228) and its last `source.status` may read OK. Under V3, a reader calls it current until 120 s; the observer's own screen would have called the feed stale at 45 s (`view.py:32-34`). V3 concedes the 75 s gap and pushes it to the mapping table (variant-3 "costs or risks"); that is the very contradiction the mapping rule "never show one as the other" (ADJ line 250) was written to prevent.
2. **V3's "a healthy observer never looks stale" mislabels backoff as healthy.** Backoff happens only after failures (`collector.py:30`, "after failures the wait doubles"); during it, the data is not fresh. Because the file is still rewritten after failures (`commands.py:294-297`), V3's `generatedAt` clock stays green while `source.status` is STALE or ERROR. X-003's "No" is the unsafe answer.
3. **V3 fixes a number for a producer that does not exist.** Its own risk list says 2 minutes "may be too short (constant false 'stale') or too long" for CO-03. It also binds CO-04 to "deliver a copy within 2 minutes of `generatedAt`" before any transport, or its clock-skew behaviour (A-001), is known.
4. **V1 inherits the file-age versus data-age gap.** It measures "from `generatedAt`" (variant-1 step 1); because `generatedAt` advances after failed cycles (`commands.py:294-297`), V1's 45 s file rule does not mean the same as the screen's 45 s rule, which runs from the last *successful* poll (`view.py:357-358`). V1's headline benefit, "one meaning of 'stale'", holds only if the reader also uses `source.observedAt`, which V1 does not say.
5. **V1's multiplier is borrowed, not measured,** as V1 itself concedes; for a copied file (CO-04) the transport delay is to be "added" but its size and skew are unknown (UNVERIFIED until CO-04 is designed).

## Concessions

- V2's interim rule (one producer cycle, about 15 s) is the weakest threshold on offer: it flickers on ordinary timing, it needs a cycle value the file does not carry, and it reads stale during every backoff. V1's three-interval rule fixes this at no cost and should replace it as the interim rule.
- V1 already defers the Coder record's number to CO-03, so V2's main virtue (no guessed number for a non-existent producer) is shared by V1; V2's remaining distinct contribution is keeping the placeholder rather than a formula, which is largely presentation.
- V2 leaves the owner's question unanswered and the placeholder visible in Coder#477; the question returns later.
- The `generatedAt` versus `source.observedAt` gap raised in Strength 2 applies equally to V2's own interim rule; V2 does not solve it either, it only avoids freezing a number before it is solved.

## Shared assumption responses (A-001)

**QUALIFY.** On the same host, comparing `generatedAt` with the reader's clock is sound to about one second: `generatedAt` is UTC wall time from `time.time()` (`commands.py:106`, `view.py:555`) truncated to whole seconds (`parse.py:268`). Across hosts (Coder workspace to TUIBBS) the comparison depends on clock skew, which is UNVERIFIED and must be bounded or measured when CO-04 is designed; skew and the 1 s truncation hurt short thresholds most (V2's 15 s worst, V1's 45 s less, V3's 120 s least). Separately, `generatedAt` is the file's write time, not the data's age: a reader must also use `source.observedAt` and `source.status`, since the file is rewritten after failed cycles (`commands.py:294-297`).

## Per-point verdicts

| point | superior | reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V1 | A rule tied to the producer's interval fits today's observer and a future producer without a guessed number; V2's interim form is the flickering one. |
| C-002 | V1 | 45 s matches the screen's own rule and tolerates the 15 s cycle budget; 15 s flickers, 120 s hides a dead observer 75 s longer. |
| C-003 | tie | V1 and V2 both defer the Coder number to CO-03; V3 fixes a requirement on a producer that does not exist. |
| C-004 | V2 | Keeping the placeholder is explicitly allowed (line 354) and avoids posting a formula or number that may later need editing. |
| C-005 | V1 | Naming the copy delay as an input to the rule is a concrete design obligation; V2 only defers, V3 fixes a deadline before the transport exists. |
| X-001 | V1 | One meaning of stale across screen and file is what the mapping rule requires (ADJ line 250), provided data age is read from `source.observedAt`. |
| X-002 | V2 | No reader exists (lines 355-356) and the file-age versus data-age split is unresolved, so a number now is chosen without its consumer; V1's "rule now, numbers later" is a close second. |
| X-003 | V1 | A producer in backoff has no fresh data, so showing stale at 45 s is correct; V3's "no" is unsafe and V2's 15 s is noisy. |
| A-001 | V1 | All share the assumption (QUALIFY applies to all); 45 s is moderately robust to skew and truncation while still catching a dead producer promptly. |

Overall: V1
