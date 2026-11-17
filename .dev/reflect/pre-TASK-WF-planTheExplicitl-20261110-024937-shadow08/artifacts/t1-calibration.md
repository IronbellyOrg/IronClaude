# Wave 1D — T1 card blind calibration

calibrator_class: opus
formation_context: stripped

## Scores
| Dimension | Score |
|---|---|
| Citation grounding | 0.82 |
| Coverage completeness | 0.80 |
| Deviation-classification clarity | 0.72 |
| Risk surface coverage | 0.75 |
| Recommendation actionability | 0.70 |

**C = 0.76** (self-assessed 0.85; delta -0.09). Escalation recommendation: ESCALATE to T2.

Citations checked and found accurate:
- Tasklist lines 19, 25-31, 27, 39 and 43 match the card's quotes.
- Test line 36 does assert `"coordinator under another orchestrator" not in section`.
- Test lines 33-34 pin the person-opened and worker-ban phrases. The card says lines 24-35, which is loose but covers them.
- `CLAUDE.md:312` holds the narrowed wording.
- `src/superclaude/core/CLAUDE.md:57-61` holds the narrowed wording.
- The asymmetry in F1 is real. The test reads only the two `src/superclaude` files, so root `CLAUDE.md:312` has no test.

Citations not verified (point outside the files provided): hook script lines 355-356, `README.md:241-243`, `WORKER-CONTRACT.md:62`, research report lines 2272 and 2335-2339, the sha256 `79a22b...` claim.

## Calibrator-noted gaps in the T1 card (feed T2)
- **Unverified citations (card lines 40, 41, 47).** The sha256, research-report line numbers, README and hook line numbers, and WC-13 at `WORKER-CONTRACT.md:62` are asserted with no quoted text. T2 should re-read them.
- **Root vs core wording asymmetry not flagged (card lines 39, 47).** Root `CLAUDE.md:312` says "An Orca coordinator is person-opened"; `core/CLAUDE.md:58` says "A supervised orchestrator's coordinator is person-opened"; root lacks the worker-contract parenthetical core has at 55-57. The test phrase `coordinator is person-opened` passes both, hiding the difference. F1 notes root is untested but never says the wording differs, which is the actual risk.
- **Matrix row INF-003 over-credited.** Marked "covered" while Task 2's test additions are hedged ("where necessary", tasklist:39); lists `test_require_orca_worktree_agent_governed.py` as a surface but the tasklist only runs it (tasklist:43) and never edits it.
- **INF-002 grounding omits `WORKER-CONTRACT.md`.** Task 1 (tasklist:27) also cites WC-13 and coordinator eligibility; the card credits only the research report.
- **Deviation classification thin.** Findings carry severity/category tags but none classified as spec-vs-plan deviation, over- or under-scope. The plan adds `ccsession-tag/README.md` as a named target where the spec says only "canonical guidance" — covered without being called an inference. F3 labelled positive is not a deviation at all.
- **F2 muddled:** titled as a gap, concludes "No gap found", no reader action.
- **F1's recommendation only partly actionable:** the negative-phrase assertion at test line 36 sits inside the `required` loop (redundant but harmless — card does not say so); no check recommended for root `CLAUDE.md`, the one untested surface.
- **F4 has no fix:** notes the weak pass gate, gives no concrete AC rewording.
- **Research report existence never checked** (source.md points at a `to-do` path).
- **No test-gap finding for the hook-message text beyond a bare citation.**
- **Card line 8 caveat:** mixes post-hoc on-disk state with a pre-execution audit, blurring "plan covers spec" vs "executor did the work".

## Resolution
The rubric does not conflict with the `--tier 2` pin; the pin wins, and ESCALATE to T2 is consistent with it.
