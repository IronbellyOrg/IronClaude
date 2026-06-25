# QA Report — Content Actionability & FR Fidelity (Lens: actionability)

**Topic:** troubleshoot-pipeline-hardening — FR-1..FR-13 actionability/fidelity audit
**Date:** 2026-06-11
**Phase:** doc-qualitative (FINAL_ONLY QA gate, actionability lens)
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Spec:** `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` §3 FR acceptance criteria + §5.4/5.5/5.6/5.7

---

## Mandate

For each FR-1..FR-13, verify the corresponding ref states the rule **specifically enough to execute**
and each FAIL condition is **testable** (not aspirational). Zero-trust: read actual files.

Verdict is FAIL if ANY issue of ANY severity exists.

---

## Verification method (zero-trust)

Read in full: the inventory; all 6 new refs; all 4 modified files (SKILL.md hardening
sections, troubleshoot.md, report-template.md, remediation-handoff.md); all 9 test-dir
files; spec §3 (FR-1..FR-13 ACs), §5.4 truth table, §5.5 field schema, §5.6 artifact
schemas, §5.7 grammar, §8.3 E2E scenarios. Ran the suite (`uv run pytest tests/troubleshoot/`
-> **18 passed**). Diffed the 9-value `boundary_type` enum, the FR-1 trigger list, and every
`NOT PROVEN`/`ADVISORY` Report-Language line byte-for-byte between spec and refs.

## Per-FR actionability / testability matrix

| FR | Rule in ref? | Specific enough to execute? | FAIL stated as HARD (not aspirational)? | Testable surface |
|----|--------------|------------------------------|------------------------------------------|------------------|
| FR-1 (H0 applicability) | closure.md | YES — 9-value boundary scan, "looks local" invalid | YES — skip without scan invalid | h0 (2 marker tests) |
| FR-2 (mechanism stmt) | closure.md | YES — feature-agnostic + earned escapes | YES — un-earned list = defect | verdict anti-inflation test |
| FR-3 (runtime entrypoint) | runtime-entrypoint-verification.md | YES — "FAILs if proof stops at helper" | YES — hard FAIL | h1 (helper-construction marker) |
| FR-4 (negative witness) | runtime-entrypoint-verification.md | YES — fix-reverted->FAIL, 5 forbidden interps | YES — green H1 rejected w/o witness | h1 (never-failing-test marker) |
| FR-5 (contract ledger) | contract-enumeration.md | YES — empty-ledger non-vacuous | **YES — empty ledger = hard FAIL (F-N3)** | h2 (vacuously-pass marker) |
| FR-6 (sibling sweep) | contract-enumeration.md | YES — shared-concept trigger | YES — FAILs if not swept | h2 (NEW G-PRE-1 test) |
| FR-7 (whole-artifact) | unmask-and-sweep.md | YES — 4 controls + severity assertion | YES | h3 (schema markers) |
| FR-8 (word-boundary) | unmask-and-sweep.md | YES — \b/re.escape, 5 near-miss fixtures | **YES — "first-class blocking rule", not appendix** | h3 (word-boundary + near-miss markers) |
| FR-9 (unmask-sweep) | unmask-and-sweep.md | YES — K_true/K_swept | YES — FAILs if repro-only / heuristic-no-fixture | h3 (sweep-card markers) |
| FR-10 (effective-input) | effective-input-proof.md | YES — wrong-surface, E>0 insufficient | **YES — fails closed incl. wrong-surface (F-D1)** | h4 (wrong-surface marker) |
| FR-11 (off-path/waiver) | closure.md + contract H5 mapping | YES — required triggers + 4 invalid-waiver cases | YES — invalid waiver -> FAIL | verdict (H5 mapping test) |
| FR-12 (no-re-green) | hardening-output-contract.md | YES — one-way latch, downstream no-override | YES — never re-green to pass | verdict (latch + downstream tests) |
| FR-13 (output contract) | hardening-output-contract.md + report-template.md | YES — 11 additive fields, 7-row det. aggregation | YES — NOT PROVEN blockers verbatim | output_contract (3 tests) |

**Content fidelity:** every FR rule is present, specifically stated, and the named hard-FAIL
conditions (FR-5 empty-ledger, FR-8 word-boundary first-class, FR-10 wrong-surface
fail-closed) are concrete and non-aspirational. The 9-value `boundary_type` enum, the FR-1
trigger list, and all 5 `NOT PROVEN`/`ADVISORY` lines are spec-exact.

## Findings

> Adversarial stance applied: I was told to assume >=10 defects exist and to find them.
> After exhaustive zero-trust verification I did **not** find 10 content-fidelity defects —
> the refs are unusually faithful to the spec (every FR rule, every enum value, every
> blocker line checked out). I will not manufacture defects to hit a quota. The findings
> below are the genuine, evidence-backed actionability issues I located. Per the
> "FAIL on any issue of any severity" rule, their presence drives the verdict to FAIL.

### F1 — [IMPORTANT] Every FAIL condition is testable only as a doc-marker, never as an executing gate

**Location:** `tests/troubleshoot/test_hardening_h0.py`..`test_hardening_verdict.py` (all 18 tests);
the FAIL rules in all 6 refs.

**Evidence:** All 18 pytest tests are content-assertion tests. Example — `test_h2_empty_ledger_fails`
(`test_hardening_h2.py:17-33`) asserts `"vacuously pass" in low` and `"zero-row" in low`; it
reads `contract-enumeration.md` and greps for the rule *string*. It never constructs an empty
ledger and observes a FAIL. Same pattern across H1 (`"helper construction" in low`), H3
(`"word-boundary" in low`), H4 (`"wrong surface" in low`), verdict (`"{blocked, advisory}" in OC`).

**Why this is an actionability issue (not just a style note):** the mandate asks whether each
"FAIL condition is testable." These FAIL conditions are enforced at runtime *only* by Claude
faithfully following the ref prose during Wave 4.5. A regression in which the runtime ignores,
mis-applies, or short-circuits a gate (e.g., accepts an empty ledger, or treats a substring
match as behavior-controlling) would NOT be caught by any test in this suite, because the
markdown markers would still be present. The hard-FAIL semantics ("empty ledger = FAIL",
"fails closed", "first-class blocking rule") are stated specifically enough for a human/LLM to
execute, but there is no behavioral oracle that proves the gate *does* fail on the bad input.

**Mitigating context (honest):** (a) this is a prose-driven skill, so prose IS the
implementation and marker tests are a legitimate surface; (b) the inventory is honest, labelling
these "content-assertion tests"; (c) the E2E backtest file (E1–E5 + waiver re-green) documents
the behavioral replays — but it is explicitly **not pytest-collected** and deferred to milestone
M5 (`e2e-backtest-scenarios.md:5-8`). So the *behavioral* testability of every FAIL condition is
deferred, by design, to M5 / NFR-1. Until M5, "testable" = "documented + marker-asserted", not
"behaviorally enforced."

**Recommendation:** none required for this gate's scope (the deferral is spec-sanctioned via
NFR-1 "predicted until then" and M5). Flag carried so downstream does not read 18/18 PASS as
proof the gates behaviorally fail-closed. The marker-test ↔ behavioral-test gap closes at M5.

### F2 — [MINOR] H1 negative-witness FAIL hinges on "for every contract with a forbidden interpretation" — the runtime enumeration of *which* contracts have a forbidden interpretation is left to judgment

**Location:** `refs/runtime-entrypoint-verification.md:26-36` (FR-4); spec FR-4 AC1 (line 139).

**Evidence:** FR-4 requires a negative witness "for every contract with a forbidden
interpretation" and lists 5 concrete examples (local-path-as-cloud-file, advisory-as-fatal,
dirty-work-omitted, empty-artifact-accepted, non-executable-heading-as-executable). The ref
reproduces all 5 faithfully. But whether a *given run's* changed contract has a forbidden
interpretation — and therefore whether the negative witness is mandatory or optional
(`forbidden_interpretation` is the one card field marked "yes when applicable", not "yes") — is
a runtime judgment with no decision procedure. A run could under-claim "no forbidden
interpretation here" and skip the negative witness without tripping any documented FAIL.

**Why it matters:** FR-4 AC2 ("a test never observed to fail does not satisfy H1") is the
load-bearing anti-theatre rule; its bite depends on correctly classifying the contract as
having a forbidden interpretation in the first place. The 5 examples are illustrative, not a
closed checklist, so the gate's strength varies with reviewer rigor.

**Recommendation:** acceptable for the increment (the 5 examples + the H5 off-path-review
requirement provide a backstop), but a future hardening pass could add a "default: assume a
forbidden interpretation exists unless proven otherwise" fail-closed posture mirroring FR-10's
`E>0`-is-insufficient stance.

### F3 — [MINOR] `forbidden_interpretation` card field nullability is softer than FR-4's intent

**Location:** `refs/runtime-entrypoint-verification.md:21` and spec §5.6 line 464.

**Evidence:** Both spec and ref mark `forbidden_interpretation` as "yes when applicable" while
`negative_witness_command`/`negative_witness_result` are "yes". This is faithful to the spec
(no divergence), but it is an internal tension *within the spec that the ref inherits*: FR-4
AC1 makes the negative witness mandatory "for every contract with a forbidden interpretation,"
yet the field that *names* that forbidden interpretation is optional. If `forbidden_interpretation`
is omitted, the negative-witness requirement has nothing to anchor to.

**Why it matters:** the ref is a faithful mirror, so this is not a fidelity defect — but it is
an actionability seam the ref *could* have tightened (e.g., "if `negative_witness_*` is required
then `forbidden_interpretation` must be populated"). It did not, so the inherited softness
stands.

**Recommendation:** out-of-scope to fix here (the spec is the source of the softness); note for
a future spec revision.

## Candidate defects investigated and CLEARED (zero-trust, no finding)

These were live suspicions during the adversarial pass; each was disproven by reading the files.

1. **"status: success + blocked hardening verdict could re-green via handoff."** CLEARED.
   `remediation-handoff.md:3,9-11` gates the `success AND --fix` load path so a `blocked`/`advisory`
   verdict renders `success_with_hardening_blocker`/`_advisory`, never plain `success`; the
   `BUILD_REQUEST` carries `pipeline_hardening_verdict` + `waiver_status`
   (`remediation-handoff.md:68-73`). Report `status` (grounding axis) and `pipeline_hardening_verdict`
   (hardening axis) are intentionally orthogonal; no-re-green is enforced at the render layer.
2. **"advisory dropped to a 3-token enum somewhere."** CLEARED. 4-token enum
   `pass|blocked|advisory|not_applicable` present in SKILL.md:64, closure.md:13,
   hardening-output-contract.md:5,15, report-template.md (both spaced and no-space forms), and
   guarded by `test_known_escapes_requires_cited_card` + `test_report_closure_section_not_proven_blockers`.
3. **"§5.4 truth-table row ordering ambiguous (latched+missing-probe vs latched+substitute)."**
   CLEARED. `hardening-output-contract.md:29` adds "first matching row wins" + priority order;
   row 3 (blocked) precedes row 5 (advisory), so latched+missing-probe correctly resolves to
   `blocked`. This is *more* explicit than the spec, not a divergence.
4. **"E2E file provenance / test-count claim wrong."** CLEARED. `e2e-backtest-scenarios.md`
   matches spec §8.3 line-by-line (E1–E5 + waiver re-green); "13 unit + 5 integration"
   reconciles exactly (h0:2 h1:1 h2:2 h3:3 h4:2 verdict:3unit = 13 unit; verdict:2 +
   output_contract:3 = 5 integration). Spec version v1.1.0 confirmed (frontmatter line 3).
5. **"NFR-5 thinness violated by command logic."** CLEARED. `troubleshoot.md:67,169` advertise +
   surface only; no new CLI flag; the skill computes the verdict.
6. **"boundary_type enum / FR-1 trigger list drift."** CLEARED. 9 values + trigger list are
   spec-exact (diffed byte-for-byte).

## Self-Audit

1. **Factual claims independently verified against source:** ~40 — every FR rule located by section
   in its ref; the 9-value `boundary_type` enum, FR-1 trigger list, and 5 `NOT PROVEN`/`ADVISORY`
   lines diffed against spec; 11 hardening + 19 legacy output-contract fields confirmed present;
   18/18 test pass status reproduced; test-count arithmetic recomputed; e2e provenance checked
   against §8.3; handoff gating traced.
2. **Files read to verify claims:** all 6 refs, SKILL.md (hardening + wave-structure + output-contract
   sections), troubleshoot.md, report-template.md, remediation-handoff.md, all 7 test modules +
   e2e-backtest-scenarios.md, the inventory, and spec §3/§5.4/§5.5/§5.6/§5.7/§8.3/frontmatter.
3. **Why trust the verdict despite finding few content defects:** I diffed the highest-risk
   surfaces (enum, trigger list, blocker lines) at the byte level and they matched — this is
   positive evidence of fidelity, not absence of checking. The FAIL verdict rests on the genuine
   testability-surface gap (F1), not on manufactured nits. I explicitly declined to fabricate
   defects to reach an assumed count.
4. **Web research:** none performed (all verification was local-file-bound); Tavily precedence
   not exercised.

## Confidence

- **Verified:** 13/13 FRs content-verified + 6 cross-cutting checks | **Unverifiable:** 0 |
  **Unchecked:** 0 | **Confidence:** 100% (content-fidelity dimension); the F1 caveat is about
  *behavioral* enforcement, which is spec-deferred to M5, not unverified by me.
- **Tool engagement:** Read: 14 | Grep/Bash-grep: 6 | Bash(pytest+arith): 2 | Glob: 0

## Verdict rationale

Content fidelity is excellent — every FR-1..FR-13 rule is stated specifically enough to execute,
every named hard-FAIL (FR-5 empty-ledger, FR-8 word-boundary first-class, FR-10 wrong-surface
fail-closed) is concrete and non-aspirational, and the refs mirror the spec enum/trigger/blocker
text exactly. However, per the gate's "FAIL on ANY issue of ANY severity" rule, finding F1
(IMPORTANT) plus F2/F3 (MINOR) forces a FAIL. F1 is the substantive one: every FAIL condition is
currently testable only as a documentation marker, with behavioral enforcement deferred to M5 —
so "18/18 PASS" must not be read as proof the gates behaviorally fail-closed. F2/F3 are
inherited-softness seams around FR-4's negative-witness applicability.

**None of F1–F3 are blocking content-fidelity errors** (the deliverables faithfully implement
the spec); they are actionability/testability observations the downstream owner should
acknowledge before treating the hardening gates as behaviorally proven.

VERDICT: FAIL
