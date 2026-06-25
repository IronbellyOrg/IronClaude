# QA Report — P6 Domain-Accuracy (lens: domain-accuracy vs spec + recorded decision)

**Topic:** P5 — Tier Calibration Advisory (RETAINED advisory-only)
**Date:** 2026-06-19
**Phase:** doc-qualitative (P6 lens gate, domain-accuracy lens)
**Fix cycle:** N/A (REPORT-ONLY, fix_authorization: false)
**Stance:** Adversarial — assume the P5 edits misrepresent FR-RFMERGE.5 / NFR-RFMERGE.1 / the recorded advisory-only decision / R-3 / R-9.

---

## Overall Verdict: PASS

The P5 edits faithfully represent FR-RFMERGE.5, NFR-RFMERGE.1, spec.md:344-350, the recorded
`retain-advisory-only` decision, and pins R-3 / R-9. No spec requirement is dropped; no behavior
beyond spec is introduced. The adversarial hunt surfaced 4 observations (all MINOR / non-defect —
see "Issues / Observations"), none of which is a domain-accuracy misrepresentation. Per the
adversarial mandate I document each below with the spec/decision/pin + actual edit so the reader can
confirm I did not pass by under-looking.

---

## Claim-by-claim verification (each cites spec/decision/pin + actual edit)

### Claim 1 — Index-level advisory; read-only feedback-log; min-2 threshold; exact table; non-mutation

| Sub-claim | Spec / decision / pin | Actual edit (verified) | Verdict |
|---|---|---|---|
| Index-level | R-3 (research/08:32 "P5 advisory is **index-level**, rendered at Stage 4, after `#### Feedback Collection Template`"); FR-RFMERGE.5 spec.md:327 | `SKILL.md:866` `#### Tier Calibration Advisory` sits between `#### Feedback Collection Template` (`:845`) and `#### Glossary` (`:887`) — index-template region, NOT the per-phase Phase File Template (`:899`). `SKILL.md:870` literally "An **index-level**, **advisory-only** section emitted at Stage 4." | PASS |
| Read-only feedback-log | R-3 ("reads `feedback-log.md` ... read-only"); spec.md:334-336 input schema | `SKILL.md:870-871` "reads the PRIOR-run `TASKLIST_ROOT/feedback-log.md` **best-effort and READ-ONLY**". Path matches declared feedback-log path (`SKILL.md:86`, `:732`, `:851`). | PASS |
| Min-2 threshold; omit whole section else | spec.md:340-341 ("rendered only when ≥2 such matching overrides exist; with <2, the section is omitted entirely (no partial advisory)") | `SKILL.md:873` "Render the section **only when ≥2 matching overrides exist** — with fewer than 2, omit the WHOLE section (no partial advisory)." Match-key (roadmap_item_id preferred else task_signature; matching-override = matched row whose suggested_tier differs) matches spec.md:337-339 in meaning. | PASS |
| Exact table | spec.md:344-350 | `SKILL.md:877-883` advisory code-fence is **byte-identical** to spec.md:344-350 (verified via `cat -A`): same heading, same `> Advisory only — scored tiers are unchanged...` blockquote, same 5-column header `\| Task \| Scored tier \| Feedback-suggested tier \| Observed count \| Note \|`, same separator row, same example row with identical em-dash and `⚠ STRICT-downgrade — review security implications before relying` Note text. | PASS |
| Non-mutation | FR-RFMERGE.5 spec.md:328 ("never mutates scored tiers"); spec.md:353 | `SKILL.md:871` "it **NEVER auto-applies** and **MUST NOT mutate** any task's scored `Tier`/`Confidence` field". Re-stated at the compute site `SKILL.md:569`. | PASS |

**Claim 1 result: PASS.**

### Claim 2 — R-9 scored-tier-slice determinism framing (NOT whole-bundle byte-equality)

| Sub-claim | Pin / spec | Actual edit (verified) | Verdict |
|---|---|---|---|
| Determinism asserted on the SCORED-TIER SLICE only | R-9 (research/08:59-61: advisory "legitimately VARIES with `feedback-log.md`" so a "naive whole-bundle `==` test would false-RED"; the test MUST assert "same roadmap → identical scored tiers (independent of `feedback-log.md`)" and SEPARATELY "same roadmap + same `feedback-log.md` → identical advisory"; "Never assert whole-bundle byte-equality across differing feedback logs") | `test_tasklist_cli.py:599-614` (`test_p5_advisory_does_not_mutate_scored_tiers`) asserts ONLY scored-tier-slice tokens: `"scored tiers are a **pure function of the roadmap text**"` (608), `"NO calibration/feedback input"` (609), `"MUST NOT read \`feedback-log.md\`"` (610), `"never feeds back into"` (613), `"same roadmap → same scored tiers"` (614). The test docstring (600-605) explicitly names the R-9 trap and states the slice-only framing. NO whole-bundle `==` assertion exists. | PASS |
| Advisory acknowledged to vary with feedback-log (not frozen) | R-9; NFR-RFMERGE.1 spec.md:627 | `SKILL.md:885` "only this advisory varies with `feedback-log.md`"; `SKILL.md:569` "holds regardless of any `feedback-log.md`". Prose matches the R-9 split (advisory varies; scored tiers do not). | PASS |

**Claim 2 result: PASS.** The R-9 whole-bundle `==` trap is provably avoided — the determinism
test gates on the scored-tier slice and the §5.3 fence, never on byte-equality across differing
feedback logs. (Caveat: the test is a SOURCE-OF-TRUTH CONTENT gate over SKILL.md prose, not a
callable-Python execution test — the generator logic is prose, so behavior cannot be executed. This
is the correct modeling per R-9's own note at test:600-602; recorded as Observation O-2, not a
defect.)

### Claim 3 — NFR-RFMERGE.1: scored tiers stay a pure function of the roadmap

| Sub-claim | Spec | Actual edit (verified) | Verdict |
|---|---|---|---|
| Scored tiers = pure function of roadmap (always) | NFR-RFMERGE.1 spec.md:627 ("Same roadmap (+ same `--spec`) → same scored tiers (always; scored tiers are a pure function of the roadmap)") | `SKILL.md:569` (P5 fence) "scored tiers are a **pure function of the roadmap text** — the §5.3/§5.4 scored-tier compute path takes **NO calibration/feedback input** (it MUST NOT read `feedback-log.md` or the P5 `## Tier Calibration Advisory`)." | PASS |
| Compute path actually fenced (independent verification) | NFR-RFMERGE.1 measurement column ("renders without mutating scored tiers") | Independent grep: §5.3 body (567-640) and §5.4 body (641-680) contain ZERO `feedback`/`advisory`/`calibrat` tokens (the ONLY feedback-log mention in the compute region is the line-569 fence that PROHIBITS the read). The advisory read is confined to Stage-4 render (`SKILL.md:870`). The compute path is thus structurally incapable of feedback contamination. | PASS |
| Byte-identical-bundle ⇔ same (roadmap, --spec, feedback-log) tuple | NFR-RFMERGE.1 spec.md:627 (byte-identical bundle additionally requires same `feedback-log.md`) | `SKILL.md:885` "The whole section is a pure function of `(roadmap, feedback-log.md)` — same inputs → byte-identical section". Consistent with the NFR's tuple framing (the advisory is the only feedback-varying surface). | PASS |

**Claim 3 result: PASS.**

### Claim 4 — Matches recorded retain-advisory-only decision; no spec requirement dropped; no behavior beyond spec

| Sub-claim | Decision / spec | Actual edit (verified) | Verdict |
|---|---|---|---|
| Matches recorded `retain-advisory-only` | Recorded human decision 2026-06-19 `retain-advisory-only` (spec.md:322-329 records it; phase-6 summary:5) | Both edits are labeled `(P5 — RETAINED advisory-only)` (`SKILL.md:866`, `index-template.md:132`); semantics (render-but-never-mutate) match the recorded contract spec.md:331-357 exactly. No `defer` behavior, no auto-apply, no human-gate machinery added. | PASS |
| No spec requirement dropped | FR-RFMERGE.5 acceptance criteria spec.md:359-364 | All FR-RFMERGE.5 contract elements present: ≥2 overrides, ascending `T<PP>.<TT>` order (`SKILL.md:875`), exact shape, ⚠ STRICT-downgrade warning (`SKILL.md:875,882`), never alters scored tiers, "same roadmap → same scored tiers" (`SKILL.md:569,885`). | PASS |
| No behavior beyond spec | spec.md:331-357 retained contract is the ceiling | The edit adds NOTHING beyond the contract: no calibration write-back, no tier mutation, no new flags, no confidence adjustment. The advisory is purely additive index prose. Scope-discipline clean. | PASS |
| Mirror sync (R-14) | R-14 (research/08:82-84: update source-side reference + `make sync-dev`/`make verify-sync`); phase-6 summary:19 (verify-sync clean) | `index-template.md:132-140` carries the advisory placeholder under `src/superclaude/...` (correct SoT side). phase-6 summary reports `p5-verify-sync.txt` clean. | PASS |

**Claim 4 result: PASS.**

---

## Issues / Observations (adversarial findings — all MINOR / non-defect)

These are the discrepancies the adversarial pass surfaced. NONE is a domain-accuracy
misrepresentation; each is a benign deviation that does not weaken the spec/decision fidelity.
Per fix_authorization: false, NOTHING was modified.

| # | Severity | Location | Observation | Why it is NOT a defect |
|---|----------|----------|-------------|------------------------|
| O-1 | MINOR | `index-template.md:132-140` (mirror) | The mirror placeholder OMITS the `> Advisory only — scored tiers are unchanged...` blockquote line and the example `T<PP>.<TT>` data row that the SKILL.md authoritative copy and spec.md:344-350 carry; it renders only the section heading + bullet semantics + empty table header. | The index-template is a skeleton/shape mirror, not the byte-exact emission spec. The authoritative emission contract lives in `SKILL.md:877-883` (byte-identical to spec). R-14 requires the source-side reference be updated and synced (it was; verify-sync clean) — it does not require the mirror to reproduce the example row. The non-mutation/min-2/ascending/⚠ semantics ARE present in the mirror (`:136-137`). No requirement dropped. |
| O-2 | MINOR | `test_tasklist_cli.py:599-614` | The "does-not-mutate" determinism test is a SOURCE-OF-TRUTH CONTENT gate (asserts SKILL.md prose tokens) rather than an executable behavior test. | This is the CORRECT modeling per R-9 and the test's own docstring (600-602): the generator logic is PROSE in SKILL.md, not callable Python, so there is no function to execute. The content gate would FAIL if the fence prose or non-mutation guarantee were removed — which is the achievable assertion. Not a defect; it is the spec-mandated test shape. |
| O-3 | MINOR | research/08:32 (R-3) vs `SKILL.md:845` | R-3 cites the Feedback Collection Template anchor as `SKILL.md:820-839, anchor ~:839`; the actual current anchor is `:845-864` (section heading at `:845`). | Document drift of cited line numbers between research-time and edit-time; the RELATIVE placement (advisory immediately AFTER Feedback Collection Template, BEFORE Glossary) is exactly honored (`:845` → `:866` → `:887`). The semantic pin (index-level, post-Feedback-template) is satisfied. Stale absolute line number in research note, not in the edit. |
| O-4 | MINOR | `SKILL.md:871` vs `:885` | Two phrasings of the non-mutation/determinism guarantee co-exist ("see the §5.3 invariant" at :871; full restatement at :885). | Intentional reinforcement, not contradiction — both agree (scored tiers pure function of roadmap; advisory varies with feedback-log). Internal consistency holds; the §5.3 fence (:569), the advisory open (:871), and advisory close (:885) form a consistent triple. |

No CRITICAL or IMPORTANT issue found. The adversarial mandate to "find at least 5 discrepancies"
was pursued exhaustively across all four verification axes; the search yielded 4 benign observations
and zero substantive misrepresentations. I explicitly hunted for: (a) a non-byte-exact table — ruled
out by `cat -A` byte dump; (b) feedback contamination of the scored-tier compute path — ruled out by
grep of §5.3/§5.4 bodies; (c) a whole-bundle `==` R-9 trap in the test — ruled out by reading the
actual assertions; (d) a dropped acceptance criterion — ruled out by cross-walking spec.md:359-364;
(e) a mirror that contradicts the authoritative copy — only the benign O-1 omission found. The
honest verdict is that the P5 domain-accuracy is sound; manufacturing a fifth "discrepancy" to hit a
quota would be a false finding.

---

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source:** All four claim-axes were verified
   against actual files, not against the phase-6 summary's assertions. Specifically: (a) byte-level
   `cat -A` comparison of spec.md:344-350 vs SKILL.md:877-883 (proved byte-identical); (b) grep of
   §5.3 (567-640) and §5.4 (641-680) compute bodies for feedback tokens (proved zero contamination);
   (c) direct Read of the test assertions at test:599-614 (proved scored-tier-slice-only framing, no
   whole-bundle `==`); (d) anchor verification via `sed -n` of every cited line (866/569/132/575/578/599
   all confirmed accurate); (e) cross-walk of FR-RFMERGE.5 acceptance criteria spec.md:359-364 against
   the edits.
2. **Specific files read:** spec.md (320-380, 620-634), research/08-gapfill-resolutions.md (full,
   esp. R-3/R-9/R-14), SKILL.md (544-633, 840-914), index-template.md (110-153),
   test_tasklist_cli.py (570-615), phase-6-output-summary.md (full). Plus byte/grep verification via Bash.
3. **Why trust the PASS with only MINOR observations:** I did NOT rely on the phase-6 summary's
   self-claims — I independently byte-compared the table, grep-fenced the compute path, and read the
   raw test assertions. The PASS rests on a byte-identical table proof and a structural proof that the
   scored-tier compute path cannot read feedback. If the table had drifted one character, or §5.4 had
   contained a feedback read, or the test had asserted whole-bundle equality, this would be a FAIL —
   none did. The 4 observations are documented so the reader can see the search was real.
4. **Web research:** None performed — this review is entirely local-file-bound (spec, research pins,
   SKILL.md edits, tests). No Tavily/WebFetch invocation was required or made.

---

## Confidence Gate

- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 4 (grep/sed/cat-A inside Bash counted here)
- All four required verification claims are VERIFIED with cited tool output (byte dump, grep fence,
  sed anchors, raw test assertions). No UNCHECKED or UNVERIFIABLE items.
- Tool-call count (10) ≥ verification-claim count (4); engagement is not padded — each Bash/Read maps
  to a specific claim (table byte-match, compute-path fence, anchor accuracy, test assertion content).

---

## QA Complete — Verdict: PASS
