# QA Report — Phase 4 (H3 unmask-and-sweep.md) + Cross-Ref Integrity

**Topic:** H3 Classifier Ref verification + inter-ref link integrity across all 6 hardening refs
**Date:** 2026-06-11
**Phase:** phase-gate (Phase 4)
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Overall Verdict: PASS (with 4 MINOR findings — none blocking)

`unmask-and-sweep.md` is a faithful, near-verbatim implementation of the H3 spec
(§3 FR-7/8/9, §5.6 card, §5.7 grammar). The §5.6 card rows are byte-identical to the
spec (`diff` IDENTICAL). The §5.7 4-rule grammar, the FR-8 word-boundary rule + all 5
near-miss negatives, the FR-7 4 required controls, and the FR-9 regression rule are all
present and accurate. markdownlint clean (1 H1, unique H2s, no placeholders). All 6
hardening refs exist and every inter-ref link resolves — the Phase-2 forward-ref finding
is RESOLVED. Findings below are MINOR fidelity/observational gaps; none block the gate.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | §5.7 grammar = 4 rules verbatim | PASS | File L9-12 match spec L512-515 rule-for-rule (ATX+space, exact-token/`\b`/`re.escape`, setext/decorated/wrong-case=fixtures, every expansion needs pos+near-miss+full-artifact) |
| 2 | "NOT CommonMark AND NOT ad hoc substring for this increment" | PASS | File L7: "small formal allow-list grammar **for this increment** — **not** ad hoc substring matching and **not** a full CommonMark parser" |
| 3 | substring containment NEVER behavior-controlling | PASS | File L10: "substring containment is **never** behavior-controlling" |
| 4 | FR-8 word-boundary = FIRST-CLASS BLOCKING (not appendix) | PASS | File L16: "**first-class blocking rule**, not an appendix note (fixes adversarial F-SC1)" |
| 5 | FR-8 mandatory near-miss negatives (all 5) | PASS | File L20-24: `incomplete`/`representation`/decorated-bolded/wrong-case/setext — match spec L185 exactly |
| 6 | FR-8 regex-timeout = guardrail not substitute | PASS | File L18: "regex timeouts are a guardrail, **not** a substitute for these" |
| 7 | FR-7 required controls (pos + sibling-neg + full-artifact-mixed + per-consumer severity) | PASS | File L30-33: all 4 present incl. "severity assertion (`HALT`/`WARN`/`CONTINUE`) per runtime consumer" |
| 8 | FR-9 sibling-surface search OR hard-fatal-without-fixtures+cost = FAIL | PASS | File L37 reproduces both FAIL conditions verbatim |
| 9 | FR-9 documents K_true/K_swept; K_swept covers full sibling family | PASS | File L37: "documents `K_true` and `K_swept` and asserts `K_swept` covers the full sibling family"; card rows L45-46 |
| 10 | §5.6 card — all 10 fields VERBATIM | PASS | `diff` spec L484-493 vs file L43-52 = IDENTICAL (names, Required, Meaning) |
| 11 | `heuristic_cost_rationale` conditional ("required for hard-fatal heuristic parser") | PASS | File L52 matches spec L493 exactly |
| 12 | markdownlint MD025 (one H1) | PASS | grep `^# `: only L1 |
| 13 | markdownlint MD024 (sibling-only H2s) | PASS | 5 distinct H2 headings, no duplicates |
| 14 | No placeholders / no fabricated field names | PASS | placeholder grep: none; all field names trace to spec §5.6 |
| 15 | Cross-ref: 6 refs exist | PASS | `ls` confirms all 6 present in refs/ |
| 16 | Cross-ref: every `[..](X.md)` link resolves | PASS | All links target the 5 sibling hardening refs; 0 broken/typo'd |
| 17 | E2/E3 closure attribution accurate | PASS | File L3 (FR-7 closes E2+E3), L16 (FR-8 closes E2) consistent with spec L174/186/198 |

## Summary
- Checks passed: 17 / 17 (acceptance + cross-ref)
- Checks failed: 0
- Critical issues: 0
- Findings (MINOR, non-blocking): 4

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | unmask-and-sweep.md §5.7 (L5-12) | Spec §5.7 closing sentence (spec L517) — "This resolves **OI-4** for the release increment while preserving a future option to replace the grammar with a CommonMark-derived parser if fixture pressure or false-positive measurement justifies it" — is NOT reproduced in the file. The "for this increment" phrasing (L7) implies a future increment but the explicit OI-4 resolution + the documented future-CommonMark option is absent. This is a fidelity gap, not an acceptance-criteria miss (the AC requires the NOT-CommonMark/NOT-substring statement, which is present). | OPTIONAL: append a sentence to the §5.7 section noting this resolves OI-4 for the release increment and preserves the future CommonMark-derived-parser option per spec L517. Non-blocking — AC does not mandate it. |
| 2 | MINOR | unmask-and-sweep.md L9 (grammar rule 1) | Grammar rule 1 lists "explicit verdict/status lines" as behavior-controlling alongside ATX headings, matching spec §5.7 rule 1. However the file never enumerates what an "explicit verdict/status line" syntactically IS (e.g., a leading `VERDICT:` / `STATUS:` token at line start), leaving the grammar's second behavior-controlling production under-specified relative to the precision applied to ATX headings ("required post-marker space"). Spec is equally terse here, so this is inherited, not introduced. | OPTIONAL: add a one-line gloss of the verdict/status-line production (anchored token, line-start) so the allow-list grammar is fully self-describing. Non-blocking. |
| 3 | MINOR | unmask-and-sweep.md L11 (grammar rule 3) | Rule 3 says setext/decorated/wrong-case/sibling sections are "**fixtures**, not accepted control syntax **unless explicitly added to the grammar later**." The AC phrasing is "setext/decorated/wrong-case/sibling = fixtures NOT control syntax." The trailing "unless explicitly added to the grammar later" is an addition beyond the AC. It is consistent with rule 4 (expansion requires fixtures) and the §5.7 future-option intent, so it is a benign clarification, but it slightly softens the "NOT control syntax" absolute. | No fix required — the clause is internally consistent with the expansion rule (rule 4) and does not weaken behavior for THIS increment. Flagged for executor awareness only. |
| 4 | MINOR | unmask-and-sweep.md §5.6 card (L39-52) | The §5.6 card is rendered identically to the spec, but the file does NOT cross-link the card's `severity_assertions_by_consumer` field to the §4.7 "Classifier fixture harness" executable validation surface (`tests/troubleshoot/` H3 fixtures) that the spec §4.7 (L343) ties to this ref ("assert HALT/WARN/CONTINUE by runtime consumer"). The card stays purely declarative. Sibling refs (e.g., contract-enumeration, effective-input-proof) similarly defer test wiring to SKILL.md/tests phase, so this is consistent with the implementation order (§4.6 step 7 = tests). | No fix required at this phase — test wiring is §4.6 step 7, downstream of this ref. Flagged so the executor confirms the H3 fixture harness is wired when SKILL.md + tests land. |

## Cross-Ref Integrity Re-Check (resolves Phase-2 forward-ref finding)
All 6 hardening refs exist in `src/superclaude/skills/sc-troubleshoot-protocol/refs/`:
`pipeline-hardening-closure.md`, `hardening-output-contract.md`,
`runtime-entrypoint-verification.md`, `contract-enumeration.md`,
`effective-input-proof.md`, `unmask-and-sweep.md`. PASS

Inter-ref link audit (every `[..](X.md)` target):
- `pipeline-hardening-closure.md` -> links to hardening-output-contract.md (x7),
  runtime-entrypoint-verification.md (x2), contract-enumeration.md (x2),
  unmask-and-sweep.md (x2), effective-input-proof.md (x2) — ALL resolve. PASS
- `hardening-output-contract.md` -> no outbound .md links (terminal contract ref). PASS
- `runtime-entrypoint-verification.md` -> hardening-output-contract.md — resolves. PASS
- `contract-enumeration.md` -> hardening-output-contract.md — resolves. PASS
- `effective-input-proof.md` -> hardening-output-contract.md — resolves. PASS
- `unmask-and-sweep.md` -> hardening-output-contract.md — resolves. PASS

**0 broken links, 0 typo'd targets.** The Phase-2 forward-reference finding (unmask-and-sweep.md
referenced before it existed) is RESOLVED — the file now exists and is the link target/source as expected.

## Actions Taken
None — fix_authorization: false. All findings are REPORT ONLY for the executor.

## Recommendations
- Findings #3 and #4 require NO action (internally consistent / downstream-phase concerns).
- Findings #1 and #2 are OPTIONAL fidelity improvements (reproduce spec L517 OI-4/future-CommonMark
  note; gloss the verdict/status-line production). Neither blocks the H3 gate — the binding
  acceptance criteria are all satisfied verbatim.
- Executor reminder (carries from finding #4): confirm the H3 classifier fixture harness
  (`tests/troubleshoot/` per §4.7) asserts HALT/WARN/CONTINUE per consumer when SKILL.md + tests land (§4.6 step 7).

## Confidence Gate
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 6
  (Bash calls each map to a specific verification: link extraction, markdownlint/placeholder scan,
  verbatim card-row `diff`, FR-8 near-miss list compare, §5.7 future-option fidelity, FR-section/E2-E3 attribution.
  No web research performed — all claims are source-truth-local, so no Tavily/WebSearch needed.)
- No UNCHECKED items. No UNVERIFIABLE items.

## VERDICT: PASS

The H3 ref satisfies all binding acceptance criteria verbatim, passes markdownlint, and
all cross-ref integrity links resolve (Phase-2 forward-ref finding resolved). The 4 findings
are MINOR/observational and non-blocking. Green light to proceed.

## QA Complete
