---
topic: "Task 11 token-only gaps: remediate or accept"
adversarial_status: success (condensed pipeline; see adversarial/debate-transcript.md)
convergence: 0.78
verdict: HYBRID
---

# Verdict: HYBRID (fix 4 publish/status-path gaps with full-sentence needles; accept 6 with a written Ruling; end the review loop with a finite definition of done)

Analysis only. No file under src/ or tests/ was changed. All probe scripts ran in memory.

## Evidence (verified this session)
- 27 of 28 probed mutations survive the current 44 tests (only G7-gate copy and S7 are caught). Raw: enrichment/mutation-probe-results.json.
- Reviewer standard is unbounded: untargeted sweep over the 7 protocol files (jq block excluded): 81% of 467 modal/negation flips and 81% of 1,112 sentence deletions survive.
- Proposed needles: all exact substrings of current text; base passes; each of 9 gap mutations (G2a-c, G3a-d, G7, G9) is caught when added (enrichment/verify-fix.py).

## R1. Fix now (tests/skills/test_auggie_claim_gate_contract.py only)
Add full-sentence `need()` assertions in existing checks, plus one MUTATIONS row per gap:

| Gap | Check | Sentence(s) to assert |
|---|---|---|
| G2 | check_at04, "Claim scope" | "The admitted record keeps only supported consequences in `claim.harm`." ; "at least one consequence is supported and every other table condition holds" ; "and all consequences are listed in `excluded_consequences[]`" |
| G3 | check_at14 (Wave 2, Status mapping) and an "Invariant check" needle | "the status is `failed` with reason `invariant_check_unavailable`" (Wave 2 step 5) ; "`allowed-tools` is not a prerequisite check" ; "or `jq` absent at the preflight (reason `invariant_check_unavailable`)" ; gate preflight "If it is not, the status is `failed` with reason `invariant_check_unavailable`" |
| G7 | check_at10 | "whose category is not `security` or `data-integrity` and whose harm does not meet a Critical definition" (rubric "Admission precedes grading") |
| G9 | check_at07 | "any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`" (gate "Evidence-source rules") |

Size: about 14 lines of assertions + 4 to 5 MUTATIONS rows (one per gap; G3 one row for the Wave 2 sentence, one for the gate sentence). Time 30 to 45 minutes including re-running the 44 tests and the probe. No src/, plan, spec, marker, conftest or pyproject change.

## R2. Accept by Ruling (6 gaps and the smalls)
Paste-ready:

`T11: Ruling: Close G2, G3, G7, G9 with full-sentence assertions; accept G1, G4, G5, G6, G8, G10 and the smaller token gaps (REQ-003 wording, REQ-014 then-A7, REQ-016 exception, REQ-019 one-entry, REQ-020 base null, REQ-023/024 distinct ref) as residuals, and stop needle rounds — each accepted mutation changes only local records, or is contradicted by another asserted sentence, a jq invariant, or the line-22 byte-identity check (Task 13), and static substring checks cannot reach zero survivors (81% of untargeted flips/deletions survive) — cost if wrong is a model following an unpinned paraphrase of a local-record rule, which the Task 12 oracle table check, the Task 13 regression, the final plan review or the spec 11.3 live evaluation must catch, not this suite.`

Never-accept list (keeps the Ruling honest): deletion of the last copy of "missing `jq_exit` makes the status `failed`", "Nothing is posted when the status is `failed`", the A1-A7 disposition list, or the qualification cap in the gate.

## R3. Definition of done for static contract tests of a prose protocol
Done when: (1) every AT id assigned to the task has a presence check; (2) deleting any asserted sentence fails a test (the 27 mutation rows plus R1 rows); (3) every sentence whose mutation can change published content, published severity, remediation scope or run status (the publish-path class) is either asserted in full or has a named independent backstop in the gap table; (4) a fixed mutation probe over the publish-path class shows zero survivors, and survivors elsewhere are listed in the Ruling; (5) the operator signs the Ruling. A reviewer finding that is a synonym, a second copy, a local-record rule, or a "is the rule correct" question is recorded, not turned into a new needle (the last belongs to the final plan review and the live evaluation). "No reviewer can find a surviving sentence" is not a valid target.

## R4. Gap-by-gap table
| # | Gap | Backstop | Severity if it slips | Action |
|---|---|---|---|---|
| 1 | REQ-012 narrow contract ("Any claim"; anchors swapped) | partly jq (J3 needs entrypoint, evidence_kind != speculative); "Both anchors must be verified" and anchor definitions asserted | Low-Med: admits a non-literal claim as a narrow defect, anchors still required | Accept |
| 2 | REQ-008..010 claim scope | none (J5 checks reason prefix only; oracle not bound to prose) | High: unsupported consequences graded and published | Fix |
| 3 | REQ-037 jq-absent status | step 6b + Status mapping "failed otherwise" asserted (jq-absent cannot reach success) | Medium: unchecked status sentence, Wave 4 could post | Fix (4 needles) |
| 4 | REQ-004 agent resp. 5 | asserted Output Format and Wave 0/3 `in_diff: false` sentences; cross-cutting entries also pass admission | Low | Accept |
| 5 | REQ-022 explicit --diff reads | sibling "use `git show HEAD:<path>`, not the working tree" asserted; J13 is PR-mode only (not a backstop) | Low-Med: uncommitted edits as evidence, local | Accept |
| 6 | REQ-026 merge ranking | strict dominance + equal rank asserted; J7/J8 structure | Low: non-defect group disposition, local | Accept |
| 7 | REQ-018/030 rubric cap | gate copy asserted; J14 only catches uncapped non-security | Med-High: security defect capped to Medium loses inline comment and remediation | Fix |
| 8 | REQ-013 table intro, "Verified" def | row order + dispositions asserted; AT-16 (Task 12, not built) binds table; "Verified" also at file line 5 | Low | Accept |
| 9 | REQ-021 head-object fallback | A6 "not verified"; Location grounding copy; J13 cannot detect false diff_new_side | Medium: defect admitted on unverifiable context | Fix |
| 10 | REQ-005 drop vs downgrade | SKILL line 22 "dropped, not downgraded" byte-identical (Task 13 AT-21, not Task 11); Output Contract partial row; J6 | Low | Accept |

Classes: backstopped by jq runtime only (partly): 1, 7. Will be backstopped by Task 12 oracle (table text only): 8 partly. Backstopped by sibling asserted sentence: 1, 3, 4, 5, 6. Backstopped outside Task 11 (Task 13): 10. Uncovered: 2, 9 (and 7 for the over-cap direction).

## R5. Options considered
| Option | Verdict | Why |
|---|---|---|
| A add 10 needles | partly adopted (as R1) | cheap; but does not end the loop alone |
| B auto-mutation harness for every needle | rejected | tests the needles, not the prose; large build; same unbounded set |
| C hash seal of rule sections (V1) | rejected | ~29 KB sealed text; files are edited now (Task 12 findings, final review); reflexive re-seal; freezes current errors; AT-20 collides with `#### C1.` in SKILL:215/gate:224 if stored as fixture |
| D accept all (V3) | rejected | G2/G7/G9 reach published content/severity with no backstop of the mutated meaning; V3 backstop claims for G4/G5 were wrong |
| E hybrid | recommended | fixes what flips publish/status/severity, rules on the rest |

## R6. ROI
- Fix: about 40 minutes, about 14 test lines, closes the only gaps with a publish, severity or status consequence and no backstop. Future cost: legitimate rewording of those 6 sentences breaks a test, fix is a one-line test edit.
- Accept 6: saves roughly 20 more needles and one more review round; their slip costs a wrong local record or a conflict with a sibling sentence, noticed by the Task 12/13 checks or the final review.
- Not worth it: seal (C), harness (B), a fourth open-ended needle round (counts 43 -> 9 -> 10 per 179 is not converging).

## R7. Top 3 risks of the recommended path
1. A fourth reviewer round names new survivors anyway (already visible: REQ-014 "then A7", REQ-019 "one entry per row", REQ-020 base null, REQ-023 distinct ref) and reads it as failure. Mitigation: the Ruling and R3 define done; reviewer must show a publish-path or status consequence.
2. Accepted gaps lean on checks outside the contract module that do not exist yet (Task 12 oracle, unbuilt) or run later (Task 13 line-22 check; Task 11 does not assert line 22). If those are skipped or weakened, G8 and G10 lose their backstop. Mitigation: name them in the Ruling.
3. False confidence: pinned wording proves the sentence is present, not that a model follows it; jq certifies a consistent wrong ledger. Semantic effectiveness stays unproven until the separately authorized live evaluation (spec 0 / 11.3). Also, full-sentence needles become change detectors for legitimate rewording.

## Unverified
- Whether Task 12's AT-16 compares A1-A7 Condition text or only rows, order and dispositions (plan wording lists the latter). If only the latter, optional G0 (assert the seven Condition cells) is worth adding, since A7 "no blocking entry" has no other binding.
- The condensed debate: Round 2 rebuttals were by the orchestrator, not separate agents.
