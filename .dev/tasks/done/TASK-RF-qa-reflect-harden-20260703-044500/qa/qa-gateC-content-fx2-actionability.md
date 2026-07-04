# QA Report — task-qualitative (FX2 code-scoping + actionability)

**Topic:** FX2 cross-symbol input-shape invariant augmentation (rf-qa-qualitative.md item 5)
**Date:** 2026-07-03
**Phase:** task-qualitative
**Lens:** fx2-code-scoping-actionability
**Fix cycle:** N/A
**fix_authorization:** false (REPORT ONLY)

---

## Overall Verdict: PASS

The FX2 augmentation is a genuine, code-scoped, executable sharpening of the
task-qualitative Code-Compatibility group. All four target criteria are met with
verified source evidence. One candidate concern was chased to ground (module vs
package precision) and resolved as NON-BLOCKING — it does not affect scope,
executability, sharpening-vs-creep, or the example's reality/actionability.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| C1 | FX2 scoped to CODE, not a doc-only check | none | PASS | Augmentation lives inside item 5 "Module context analysis" under the `##### Code Compatibility` group (`rf-qa-qualitative.md:670,674`). It directs "Read the ACTUAL sibling functions in the module." The Adaptation-Guidance row 5 (`:705`) confines the invariant to the **Code Task** column; the **Doc Task Adaptation** column stays "Read surrounding doc sections for consistency" — the sharpening does NOT bleed onto the doc-QA surface. |
| C2 | Specific enough for a reviewer to EXECUTE; yields concrete AX-2 ≥ IMPORTANT finding | none | PASS | Text (`:674`) gives concrete verbs ("Read the ACTUAL sibling functions... compare how each handles the shared input"), enumerated shapes (file vs dir, `str` vs `Path`, scalar vs list), a concrete output contract ("annotate any disagreement `axis: AX-2` (Contradictions) at severity ≥ IMPORTANT"), and a worked example with named symbols. AX-2 severity floor IMPORTANT is consistent with the Five-Axes AX-2 line and Critical Rule #6. |
| C3 | Genuine sharpening of the Code-Compatibility group, not scope creep | none | PASS | Research §G3 (`08-gap-fill.md:142-174`) establishes items 4-6 (`:672-676`) already direct reading source symbols (signatures, module context, call sites, downstream consumers). FX2 augments item 5 **in place** (Branch A): checklist header still "(15 items)" (`:660`), prose counts "across all 15 checks" (`:580`) and "the existing 15-item checklist" (`:582`) intact, items still numbered 1-15. Strictly additive prose within an existing item; no new item, no doc-QA surface, no count bump. src↔mirror byte-identical (`diff -q` → FILES IDENTICAL). |
| C4 | Concrete example is a real, actionable F1-class pattern | none | PASS | All three named symbols exist and are genuine siblings in the `pr_submit/contract_setup` cluster sharing the evidence-path input: `diagnose()` (`diagnosis.py:63`), `load_evidence(probe_dir: Path)` (`evidence.py:56`), `_evidence_sha256(path: Path)` (`diagnosis.py:294`). The actual code at `diagnosis.py:134-160` **is the remediated F1/PR #209 surface**: the inline comment (`:135-137`) explicitly reconciles "probe_evidence may be a captured payload FILE or the probe DIRECTORY; both are valid (load_evidence()/_evidence_sha256() accept either)." The pre-fix bug (diagnose file-only guard vs sibling dir-acceptance) is exactly the archetype FX2 teaches. The codebase's own `deviation-taxonomy.md:160` uses the identical trio as its canonical no-spec-correctness example — FX2 mirrors an established, code-grounded canonical pattern. |

<!-- task-qualitative Axis column: closed set {AX-1..AX-5, none}. All four
checks PASSED → `none` sentinel (five-axis lens applied, nothing fired). No
FAIL rows, so no AX-1..AX-5 cells. -->

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT ONLY — fix_authorization:false)
- Axis lens status: `drift-axis-inactive` — no BUILD_REQUEST.GOAL verbatim was injected in this lens-scoped spawn; AX-1 Drift disabled for this review. AX-2..AX-5 applied normally.

## Issues Found
None blocking. One non-blocking observation recorded below.

| # | Severity | Location | Observation | Disposition |
|---|----------|----------|-------------|-------------|
| O-1 | OBSERVATION (non-blocking) | `rf-qa-qualitative.md:674` | Item 5 is framed as intra-**module** ("read the full module"), but one of the three example siblings — `load_evidence()` — lives in a neighboring module (`evidence.py`), not `diagnosis.py`. The invariant thus spans the `contract_setup` **package/cluster**, slightly broader than the literal word "module." | NON-BLOCKING. The same-module pair `diagnose()` + `_evidence_sha256()` (both in `diagnosis.py`) fully satisfies the strict intra-module framing and demonstrates the pattern on its own; the cross-file `load_evidence()` merely broadens the illustration. Item 6 ("Downstream consumer analysis") already covers cross-module reach. The codebase's own canonical example (`deviation-taxonomy.md:160`) uses the identical cross-file trio, so FX2 is faithful to the established framing. Does not affect any of C1-C4. |

## Adversarial Search Log (candidate concerns chased to ground)
A 0-issue verdict is suspect, so each candidate defect was actively hunted and resolved with evidence:
1. **"Mis-scoped to docs?"** — Refuted. Adaptation row 5 Doc column omits the invariant; it sits only in the Code column and item text says "Read the ACTUAL sibling functions in the module." (C1)
2. **"Example symbols invented / stale?"** — Refuted by grep: all three exist at the cited paths; `diagnosis.py:134-160` is the live remediated F1 surface. (C4)
3. **"`_evidence_sha256` really 'accepts a directory'?"** — At HEAD it accepts **either** (`diagnosis.py:296`: `probe_dir = path.parent if path.is_file() else path`). The example's "accept a directory" is the pre-fix F1 **archetype** framing (F1 is fixed at HEAD per research preamble), not a current-state claim. Faithful as a bug-class illustration; not a defect.
4. **"Scope creep / count bump / new item?"** — Refuted. Branch-A in-place augmentation; header "(15 items)" and both prose counts intact; items 1-15 unchanged.
5. **"AX-6 / vocab regression?"** — FX2 annotates strictly within `{AX-1..AX-5}` (uses AX-2); no AX-6 token introduced. Closed-set declaration (`:639`) and `test_axis_column_populated.py` VOCAB_PATTERN not violated.
6. **"src↔mirror drift → byte-parity test break?"** — Refuted. `diff -q` src vs `.claude` mirror → FILES IDENTICAL; FX2 line 674 byte-identical. `make sync-dev` state clean.
7. **"module vs package precision"** — Surfaced as O-1, evaluated NON-BLOCKING (see above).

## Self-Audit (INV-019)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- N/A — this is a lens-scoped content review of a single augmentation, not a full task-file gate; no `## Inherited Structural Verdict` block was injected. No structural PASS items relied upon.

**(b) Independent semantic checks (≥1 required):**
- Cross-symbol example reality — verified by `grep -rn "def diagnose\|def load_evidence\|_evidence_sha256"` + `Read diagnosis.py:63-160,294-303` and `evidence.py:56`. Confirmed all three are real sibling symbols sharing the evidence-path input, and `diagnosis.py:134-160` is the actual F1/PR #209 remediated surface (not a fabricated example).
- Scope confinement — verified by reading Adaptation-Guidance row 5 (`:705`): invariant in Code column only, Doc column unchanged. Not derivable from structure alone; required reading the content.
- Count/parity non-regression — verified by `grep` on `:580/:582/:660` (counts intact) and `diff -q src vs .claude` (byte-identical) — confirms Branch-A additive-in-place with no test-count or byte-parity regression.

Self-Audit answers:
1. Factual claims verified against source: 8+ (3 symbol existences, 3 signatures/bodies, count header + 2 prose counts, src↔mirror parity, F1 remediation comment).
2. Files read: `research/08-gap-fill.md`; `src/superclaude/agents/rf-qa-qualitative.md` (items 4-15 + Adaptation Guidance); `src/superclaude/pr_submit/contract_setup/diagnosis.py` (`:63-160`, `:294-303`); grep on `evidence.py:56`; `.claude/agents/rf-qa-qualitative.md` (parity diff).
3. Trust basis for near-0-issue verdict: 7 candidate defects were actively hunted (log above); 6 refuted with tool evidence, 1 downgraded to a documented non-blocking observation. The concrete example was verified to be the LIVE remediated F1 surface in the codebase, not a plausible-looking fabrication.
4. Web research: none performed (all verification local-file-bound); Tavily-first N/A this review.

## Confidence
Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 3 | Grep/Bash: 4 | Glob: 0

## Recommendations
- PROCEED. FX2 is code-scoped, executable, a genuine in-place sharpening (Branch A), and its concrete example is a real F1-class pattern drawn from the live PR #209 remediation surface.
- OPTIONAL (non-blocking, author discretion): if strict intra-module framing is desired, reword item 5's "in the module" to "in the module/package" so the cross-file `load_evidence()` sibling reads as in-scope. Not required — the codebase's own canonical example uses the same cross-file trio.

## QA Complete
