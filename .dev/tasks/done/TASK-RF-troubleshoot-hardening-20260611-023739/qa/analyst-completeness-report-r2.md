# Research Completeness Verification — Round 2 (RE-GATE)

**Topic:** Pipeline Hardening Closure mode (H0-H5 + waiver/no-re-greening latch) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Analysis type:** completeness-verification (re-gate after gap-fill)
**Lens:** completeness
**Authoritative spec:** troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)

---

## Round-1 FAIL gaps being re-checked
- **C1:** 6th ref `hardening-output-contract.md` missing
- **I1/C3:** 8 vs 11 fields (incl. contract_version / waiver_status / backtest_status)
- **I2/C2:** 06 said tests=NONE vs spec §8's 17+6
- **I3:** stale §6.2/§7/§9 anchors

_Report written incrementally below._

---

## Files in scope (actual names — brief used placeholder names)

The brief referenced `01-skill-structure.md`, `02-output-contract.md`, `03-refs-house-style.md`, `04-mdtm-template.md`, `06-testing-requirements.md`. Actual on-disk names:

| Brief placeholder | Actual file |
|-------------------|-------------|
| 01-skill-structure | `01-skill-structure-inventory.md` |
| 02-output-contract | `02-command-and-contract-integration.md` |
| 03-refs-house-style | `03-refs-conventions-and-report-template.md` |
| 04-mdtm-template | `04-mdtm-template-and-examples.md` |
| 06-testing-requirements | `06-sync-verify-and-tests.md` |

Authoritative trio per brief: `05-doc-crossvalidation-spec-vs-code-v2.md`, `07-release-spec-structure.md`, `08-v1.1.0-deliverable-reconciliation.md` — all present.

---

## Verification methodology

I cross-checked the authoritative trio (05/07/08) NOT just against each other but against the RELEASE-SPEC v1.1.0 directly: I re-Read spec §4.1 (L261-271), §4.5 (L304-318), §4.6 (L320-332), §4.7 (L334-348), and §5.5 (L425-439). Every claim below is confirmed against the spec source, not merely against the research's self-report.

---

## VERIFY-1: Does 08 establish 6 refs INCLUDING hardening-output-contract.md? — PASS

08 RECON-1 enumerates **6** refs and explicitly names `hardening-output-contract.md` as "THE 6th — do NOT omit". 07 §2.1 reproduces the spec §4.1 table with all 6 rows. I confirmed against spec §4.1 L270 directly: row 6 is `…/refs/hardening-output-contract.md` with purpose "Field schema, verdict aggregation truth table, waiver latch propagation contract, and downstream consumer obligations". 

Required content for the 6th ref (08 RECON-1 row 2) is correct and spec-anchored: §5.5 field schema, §5.4 verdict-aggregation truth table (7 rows incl. advisory rows 5/6), H5 decision-to-status mapping (4 rows), backtest-status-vs-run-verdict (3 rows), waiver-latch propagation, and the §5.4 L411 `success_with_hardening_blocker`/`_advisory` downstream rendering rule. This maps to spec §4.6 group 2 ("resolves OI-1/OI-6 before downstream wiring") and §4.7 component 1, both verified.

**Round-1 C1 gap (missing 6th ref) is CLOSED.**

## VERIFY-2: Does 08 establish the full 11-field contract incl. contract_version / waiver_status / backtest_status? — PASS

08 RECON-2 lists all 11 fields (10 result fields + `backtest_status`). I confirmed every field against spec §5.5 L427-439 directly. The three previously-missing fields are all present and correctly specified:
- `contract_version` (semver, default `1.0.0`, FR-13; missing ⇒ legacy) — matches spec L429.
- `waiver_status` (enum `none|latched`, one-way latch, FR-12) — matches spec L432.
- `backtest_status` (enum `not_run|partial|complete`, NFR-1; keeps signoff advisory until complete) — matches spec L433.

07 §4 reproduces the spec §5.5 table verbatim (all 11 rows) and 07 §2.4 reproduces the §4.5 registry (15 vars) including all three. The "10 distinct fields + backtest_status = 11 rows" framing matches the spec's own NOTE at L257/§5.5.

**Round-1 I1/C3 gap (8 vs 11 fields) is CLOSED.**

## VERIFY-3: Does 08 establish testing = 17 unit/integration + 6 E2E + new FR-6 test + tests/troubleshoot/ creation (overriding 06's NONE)? — PASS

08 RECON-3 explicitly REJECTS 06's `TESTING_REQUIREMENTS = NONE`, correctly scoping 06's "NONE" to "not breaking existing tests" only. It establishes:
- **13 unit** (§8.1's 12 + the G-PRE-1 net-new `test_h2_sibling_sweep_required_when_concept_shared` for FR-6).
- **5 integration** (§8.2) including the FR-12↔NFR-4 pairing test `test_downstream_success_cannot_override_latched_hardening_verdict`.
- **6 E2E backtests** (§8.3: E1-E5 + Waiver-re-green).
- **tests/troubleshoot/ creation**: 08 RECON-3 + 05-v2 (Claim 4, `[CODE-CONTRADICTED]`) both confirm the dir does NOT exist; builder must CREATE dir + `__init__.py` + 7 test files, following the `tests/skills/` content-assertion pattern (`REPO_ROOT = parents[2]`).

Note on arithmetic: brief frames this as "17 unit/integration". 13 unit + 5 integration = 18, but 08's heading says "17 unit/integration + 6 E2E". The "17" derives from the spec's native 12 unit + 5 integration = 17; the +1 (G-PRE-1) is the net-new addition, making 18 net once the FR-6 test is added. This is a cosmetic heading-vs-body discrepancy in 08 (RECON-3 heading says "17 ... + 6 E2E (NOT NONE)" then its body table lists 13 unit). It is NOT a content gap — the body correctly enumerates 13 unit + 5 integration + 6 E2E and the new FR-6 test. 07 §9.1/§9.2/§9.3 reproduces all 12+5+6 verbatim and §10 mandates the 13th. Flagged as MINOR for builder clarity, not blocking.

**Round-1 I2/C2 gap (06 said NONE) is CLOSED** (06 now carries SUPERSEDED banner + 08 authoritatively overrides).

## VERIFY-4: Does 08's section-remap (RECON-5) correctly map draft→v1.1.0 anchors? — PASS

08 RECON-5 maps every stale draft anchor to its v1.1.0 home: §6/§6.1→§3/§2, §6.2→§5.5+§4.5, §7→§3+§5.3, §8→§5.4+§5.5+FR-13, §9→§4.1+§4.2, and replaces draft line numbers with §-anchors + heading TEXT. The targets are consistent with what I verified in the spec (§5.5 = field schema, §4.1 = new files, §4.2 = modified files). The builder rule "anchor on heading TEXT not line numbers" is sound and echoed by 05-v2 (anchor-drift warnings) and the markdownlint scope note.

**Round-1 I3 gap (stale §6.2/§7/§9 anchors) is CLOSED.**

## VERIFY-5: Are the SUPERSEDED banners present on 01/02/03/04/06? — PASS

All five carried-over files carry an IDENTICAL, correct banner at line 3:
> ⚠️ SUPERSEDED (design conclusions only): ... CODEBASE anchors ... VALID and re-verified. But ... DESIGN CONCLUSIONS (ref count, output-contract field count, testing scope, draft §6.2/§7/§9 section numbers) are STALE — see 08 + 07 (AUTHORITATIVE for v1.1.0: 6 refs, 10+1 fields incl. waiver_status/contract_version/backtest_status, 17+6 tests, advisory REQUIRED).

The banner correctly (a) preserves codebase anchors as valid, (b) names the exact stale dimensions, (c) points to the authoritative pair, and (d) inlines the corrected numbers so a builder reading the stale file cannot be misled. Confirmed on: 01-skill-structure-inventory.md (L3), 02-command-and-contract-integration.md (L3), 03-refs-conventions-and-report-template.md (L3), 04-mdtm-template-and-examples.md (L3), 06-sync-verify-and-tests.md (L3).

One residual nuance (MINOR): 02-command-and-contract-integration.md's BODY still contains stale inline phrasing ("spec §6.2's 8 fields append cleanly after L61") in its Summary paragraph. The banner overrides it, but the stale "8 fields / §6.2" text remains in-body. Since 02 also carries the most load-bearing CODEBASE anchors (SKILL.md L37-61 output-contract table location, Wave-5 close L411-433, Tier-3 success-gate L439), the builder will read its body. The banner is sufficient to prevent misleading, but the in-body "8 fields" was not scrubbed. Non-blocking — flagged for awareness.

## VERIFY-6 (CRITICAL): advisory still REQUIRED (4-token enum) everywhere — no regression? — PASS

The 4-token enum `pass|blocked|advisory|not_applicable` is intact and `advisory` is explicitly mandated across all authoritative sources:
- 07 §3.0 has a dedicated "⚠️ ENUM TRUTH (do NOT drop advisory)" callout; §3.1 reproduces the §5.4 7-row truth table with ROWS 5 and 6 emitting `advisory`. Verified against spec §5.4 (07 quotes L392-400 verbatim).
- 07 §2.4 (§4.5 registry) and §4 (§5.5 schema) both carry the 4-token enum; I confirmed against spec §4.5 L311 and §5.5 L431 directly — both show `pass\|blocked\|advisory\|not_applicable`.
- 08 RECON-2 field row marks `pipeline_hardening_verdict` "**4-token — advisory REQUIRED.**"
- 05-v2 §E Claim 6 + Summary: "advisory is MANDATED by the spec (§4.5, §5.4 rows 5-6, FR-13) — do NOT drop it."
- The SUPERSEDED banner on all 5 stale files ends with "advisory REQUIRED."

**No regression. The CRITICAL enum check PASSES** — advisory is reinforced in 5 independent places, including a dedicated callout and the truth table's advisory rows.

## VERIFY-7: With 05+07+08 authoritative, is the research set NOW complete enough to build a correct tasklist? — PASS

All build-critical inventory is now authoritative and spec-confirmed:
- **6 refs** (§4.1, VERIFY-1) — confirmed incl. hardening-output-contract.md.
- **4 modified files** (§4.2) — 07 §2.2 + 05-v2 §B/C/D/E confirm all 4 exist at spec paths with exact anchors (command Behavioral-Summary step 4; SKILL.md insertion after Wave 1.7 / before Wave 5; report-template post-template rule region; remediation-handoff BUILD_REQUEST + user-offer).
- **Tests = 13 unit + 5 integration + 6 E2E** (§8 + G-PRE-1), with tests/troubleshoot/ creation + `tests/skills/` pattern (VERIFY-3).
- **FR-6 NEW test + FR-12↔NFR-4 pairing** — both established (08 RECON-3, 07 §10).
- **HALT items OI-2/OI-3/OI-5** — 07 §11 + 08 RECON-6 correctly identify these as the needs_human_decision items and explicitly correct the task-brief framing (OI-1/4/6 are RESOLVED in-spec, NOT HALT). This matches project rule feedback_human_decision_items_must_halt.
- **G1 HALT constraint** — 07 §12 + 08 RECON-7 require the tasklist be PRODUCED but execution gated; no src/.claude edits pre-approval; rollback note (revert SKILL.md trigger + remove 6 refs + sync/verify) captured.
- **Build mechanics** — 6-ref §4.6 ordered build (group 3 = 3 parallel refs), §4.7 component→test map, markdownlint scope (src/ linted, .dev/ excluded), sync/verify model — all present in 05-v2 §F + 07 §2.5/§2.6 + carried-over codebase anchors (still valid).

The research set is COMPLETE enough to build a correct tasklist.

---

## Contradictions Found

None blocking. The only inter-file tension (06's "TESTING = NONE" vs 08's "17+6") is RESOLVED by design: 06 carries a SUPERSEDED banner and 08 authoritatively overrides, correctly explaining 06's NONE was scoped to "don't break existing tests." This is a managed supersession, not an unresolved contradiction.

## Compiled Residual Gaps

### Critical Gaps (block tasklist build)
- NONE.

### Important Gaps (affect quality)
- NONE.

### Minor Gaps (non-blocking; fix for builder clarity)
1. **08 RECON-3 heading arithmetic** — heading says "17 unit/integration + 6 E2E" while body correctly lists 13 unit + 5 integration (= 18 net once FR-6 added). "17" is the spec-native 12+5; the +1 G-PRE-1 makes it 18. Cosmetic heading-vs-body mismatch; body is authoritative and correct. Builder should target 13 unit + 5 integration + 6 E2E = 24 test artifacts (across 7 files).
2. **02 body retains stale "8 fields / §6.2" phrasing** in its Summary paragraph despite the correct SUPERSEDED banner. Banner overrides it; builder reads 02 mainly for its (valid) codebase anchors. Non-blocking; the inline stale text was not scrubbed.

## Depth Assessment
**Expected depth:** Deep (spec-driven implementation tasklist). 
**Actual depth achieved:** Deep. The trio provides verbatim spec tables (07), code-traced [CODE-VERIFIED]/[CODE-CONTRADICTED] anchors (05-v2), and an authoritative reconciliation that explicitly supersedes stale conclusions with spec anchors (08). All H0-H5 schemas, the 7-row truth table, the §5.6 artifact schemas, and the §4.6/§4.7 build order + test map are captured. No missing depth elements for the build.

## Recommendations
1. Proceed to build the tasklist using 05-v2 + 07 + 08 as authoritative; treat 01/02/03/04/06 ONLY for codebase anchors (heading/line locations, refs house-style, sync/verify, MDTM mechanics).
2. In the tasklist, encode the test count as **13 unit + 5 integration + 6 E2E** (not the "17" heading shorthand) to avoid the G-PRE-1 off-by-one.
3. Keep the 4-token `pass|blocked|advisory|not_applicable` enum and §5.4 7-row truth table (advisory rows 5/6) as a first-class acceptance criterion on the verdict-aggregation task — this was the round-1-adjacent regression risk and remains the highest-value invariant to guard.
4. Author OI-2/OI-3/OI-5 as `needs_human_decision` HALT items (PENDING + halt dependent mutation, no auto-default); do NOT treat OI-1/4/6 as HALT.
5. Gate the whole tasklist behind G1 approval (no src/.claude edits pre-approval) per §1.2/§9.

---

## VERDICT: PASS

All four round-1 FAIL gaps (C1, I1/C3, I2/C2, I3) are CLOSED. The authoritative trio (05-v2/07/08) is internally consistent AND confirmed against the RELEASE-SPEC v1.1.0 directly (§4.1/§4.5/§4.6/§4.7/§5.5 re-Read). The CRITICAL advisory 4-token enum shows NO regression (reinforced in 5 places + a dedicated callout + truth-table rows 5/6). SUPERSEDED banners are present and correct on all five carried-over files. Two MINOR non-blocking nits (08 heading arithmetic; 02 in-body stale "8 fields"). The research set is COMPLETE enough to build a correct tasklist for the Pipeline Hardening Closure mode.
