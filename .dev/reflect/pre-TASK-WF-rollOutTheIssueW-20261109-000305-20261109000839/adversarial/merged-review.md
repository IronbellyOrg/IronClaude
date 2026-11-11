# Merged Pre-Execution Review
<!-- Provenance: Approved four-change merge; Base: Variant B (haiku:qa) -->

## Review metadata
<!-- Source: Variant A/B calibration metadata; base-selection final selection; debate-transcript scoring; refactor-plan changes 1–4 -->
- **Mode / scope:** pre-execution review-artifact merge only; incomplete coverage, not rollout approval. Six retained required fixes: five medium and one low; two separate medium probe residuals below.
- **Selected base:** B (haiku:qa), score .8417 versus A .7583; selection does not approve the gated plan. Final debate: A four wins, B three, four ties; comparison confidence is not readiness confidence.
- **Confidence:** independently calibrated A .74 and B .72; conservative merged .72 is inherited review metadata, NOT a new measurement. Self-reported .88/.95 are not substituted.
- **Evidence convention:** artifact citations below point to frozen review snapshots, not newly verified source or future line numbers. P denotes the reviewed task plan; S its sibling `source.md`, in `.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/`. No new source investigation or execution was performed.
- **Source cards:** [A](adversarial/variant-1-original.md) and [B](adversarial/variant-2-original.md); “Round 2 A/B” means [A rebuttal](adversarial/round-2-rebuttal-A.md) / [B rebuttal](adversarial/round-2-rebuttal-B.md), not the cards.
- **Governing artifacts:** [approved four-change plan](adversarial/refactor-plan.md), [final base selection](adversarial/base-selection.md), [debate scoring](adversarial/debate-transcript.md), [invariant probe](adversarial/invariant-probe.md). Probe IDs below resolve to its table.

## Retained plan gaps
All six findings are `plan-gap` (pre-execution), not post-execution deviations. Original IDs are retained; A/B aliases identify reviewer-1/variant-1 and reviewer-2/variant-2 respectively.

### F2 — Medium — Capture redaction verification surface (alias B:F2; confirmed T1 F2)
<!-- Source: Variant B, F2; Round 2 A:18 and B:12; invariant probe INV-005 -->
- **Mapped task / obligation:** owner capture handover and Task 5; verify required redaction, not merely require it.
- **Evidence:** B:13–15 records P:29 retaining redacted copies in package `./artifacts/captured/`, while P:118 scans only `tests/issue_watch/fixtures/`; Round 2 B:12 adds the P:78 redaction requirement.
- **Gap / remedy:** Require owner redaction before package entry and extend secret/private-identifier verification to retained captures as well as fixtures. Keep staging task artifacts. No actual leak is proven; extending a token-pattern scan cannot establish complete redaction of logins, IDs, titles or bodies.

### QA-02 — Medium — Every-fixture gate conflicts with partial completion (alias B:QA-02)
<!-- Source: Variant B, QA-02; Round 2 A:15 and B:9; invariant probe INV-004 -->
- **Mapped task / spec:** Task 5; S:22 requires replacement of every guessed fixture.
- **Evidence:** Round 2 B:9 contrasts P:15's all-19 goal and P:108's one-capture-per-fixture prerequisite with P:110,117 allowing uncaptured fixtures to remain; B:22 quotes retention of `"_assumed_shape": true`.
- **Gap / remedy:** Partial captures may be recorded, but FU-1 remains blocked until every fixture is replaced unless the owner approves a revised gate; record the every-fixture obligation separately. S:24's “about 12+” effort estimate is NOT an exception. The unverified coverage-matrix allegation is dropped; original high severity is replaced by medium.

### QA-03 — Medium — Instructions miss the demonstrated consumed raw field (alias B:QA-03)
<!-- Source: Variant B, QA-03; Round 2 A:19 and B:10; invariant probe INV-006 -->
- **Mapped task / obligation:** Task 5 capture replacement; update the data consumed by the test.
- **Evidence:** B:30–32 cites P:110's `payload` instruction, the include fixture's `raw` envelope, and `tests/issue_watch/test_github.py:563` passing `fixture["raw"]` to the runner; Round 2 B:10 confirms P:110 already accommodates stderr layouts.
- **Gap / remedy:** Name the capture stream and consumed destination for this `raw` envelope, then verify it holds the sanitized capture. Do not generalize to all non-payload/stderr layouts or authorize a parser rewrite.

### QA-04 — Medium — Capture-dependent expected values lack explicit instructions (alias B:QA-04)
<!-- Source: Variant B, QA-04; Round 2 A:17 and B:11; invariant probe INV-007/010 -->
- **Mapped task / obligation:** Task 5 expected-value maintenance, separate from parser-shape follow-up.
- **Evidence:** B:39–40 and Round 2 B:11 cite fixed login/ID/Date assertions at `tests/issue_watch/test_github.py:566–568`; P:112 explicitly directs the metadata-test edit, while P:120 permits the whole test file.
- **Gap / remedy:** Explicitly include fixture-dependent expected-value updates in the already-permitted test file. A different retained Date fails the fixed assertion, but not every capture necessarily fails. This is an instruction omission, not a forbidden-file problem; parser mismatches remain follow-up scope.

### F1 — Medium — Literal reason-token acceptance check cannot pass (alias A:F1; confirmed T1 F1)
<!-- Source: Variant A, F1; Round 2 A:7 and B:7; invariant probe INV-002 -->
- **Mapped task / obligation:** Task 2 acceptance criterion 4; zero unexplained reason-key misses before dependent Task 3.
- **Evidence:** A:11–15 and Round 2 A:7 cite backticked `failed`, `unknown`, `abandoned` at `docs/designs/issue-watcher.md:163` and `once` added by P:59; none is a REASON_TABLE key at `src/superclaude/cli/issue_watch/audit.py:26–102`, but P:65 demands zero misses.
- **Gap / remedy:** Restrict extraction to the table's third column, “Reasons that produce it,” and require zero unexplained misses. Do not broaden the remedy to a non-key allowlist.

### F4 — Low — Section map omits the planned section 16 (alias A:F4)
<!-- Source: Variant A, F4; Round 2 A:9 and B:13; invariant probe INV-008 -->
- **Mapped task / obligation:** Task 4 runbook section-map consistency.
- **Evidence:** A:28–32 and Round 2 A:9 cite `docs/designs/issue-watcher-setup.md:5` mapping sections 8–15, while P:93 adds section 16.
- **Gap / remedy:** Add the in-place map update naming section 16. This low-severity omission does not block Task 4 acceptance; “Before cron” can include transition to installation and is not a title defect.

## Dispositions and checked negatives
<!-- Source: Variant A, F3/F5 and self_audit; Round 2 A:8–11 and B:13; probe INV-003/008 -->
- **F3 withdrawn (alias A:F3; formerly confirmed T1 F3):** P:96 already implies two schedule occurrences: one in section 8.7 plus the unchanged FU-2 row. Stating the numeral is optional clarification, not a required defect fix.
- **F5 withdrawn (alias A:F5):** locating the scheduler-choice sentence at `docs/designs/issue-watcher-setup.md:202` is navigation advice; P:92 already preserves it. Excluded from required-fix count.
- **Checked negatives, not execution evidence:** A:41 records unique Task 1 status line, 59 REASON_TABLE keys, “spec reason table” references only at :709/:718, existing checklist targets, proposal rows, absence of section 16, and the false configuration example. This source self-audit certifies neither complete coverage nor Task 5. Both rebuttals withdraw the claim that A never checked Task 1.

## Limitations and owner boundaries
<!-- Source: invariant-probe INV-001/009/010/011; both Round 2 rebuttals; refactor-plan Change 4 -->
- **MEDIUM residual — INV-009, Task 3 review coverage:** P:74,78,81–85 requires 19 situation/command rows matched to builders and byte-identical preservation of existing prose. Neither card supplies full row-by-row argv/builder and preservation evidence. Counts, builder-name logs and agreement do not establish fidelity. This is unreviewed coverage, not a demonstrated new Task 3 defect.
- **MEDIUM residual — INV-011, conditional CRLF adapter interaction:** probe:21 reports that an already-CRLF `raw` capture would become CRCRLF under `test_github.py:2022–2023`'s LF-to-CRLF replacement, obstructing framing assertions/parser gates; `conftest.py:765–785` also partitions on LF/LF. Inspect actual capture framing before calling such failure a production-parser mismatch. No actual capture format or runtime failure is established.
- **Sufficiency limit — INV-010:** raw-field and expected-value repairs alone do not guarantee a passing user test or suite: timeout/exit, HTTP framing, JSON/type, Date, exact-call and metadata/readership gates remain. Probe:20 enumerates them; none was traversed with captures. P:24,114 keeps genuine parser mismatches in follow-up scope.
- **Owner boundary — INV-001:** preserve `enabled: false`. Live tests, shadow run, lock/restart tests, cron installation, live-test record and enablement/configuration changes remain owner-only (P:19–22,26–34; Round 2 A:34, B:14,31). Review artifacts authorize none of these actions.
- **Conclusion:** zero HIGH UNADDRESSED probe rows allows debate convergence only; two MEDIUM residuals remain. Neither agreement, selection nor this approved merge establishes a repaired plan, complete review, passing tests, implementation or rollout readiness.
