# Variant 1: architect, defend the cuts (concede where a blocker, safety case or owner requirement would go unprotected)

Source: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/cuts-debate/source.md`

## Facts verified on disk

- **F1. One test locks the rule text into ten files.** `canonical_rule_bullets()` reads S1 to S5 from `pragmatic.md` (`tests/skills/test_review_severity_rule.py:79-96`). S1 is the definition sentence behind run 2's over-blocking (`src/superclaude/output-styles/pragmatic.md:225`). `test_c_s1_s3_copied_verbatim` requires S1 to S3 in all ten `S1_S3_FILES` (`test_review_severity_rule.py:181-203`): both MDTM templates (`:186-187`), both document templates (`:184-185`) and all four rule prompts (`:188-191`). Changing S1 in `pragmatic.md` fails the test in every one of the ten files not updated in the same change.
- **F2. `/sc:implement` does not always print minors.** It writes them to `<retries>/T<id>/notes.md` (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:200`). The final summary prints them only "when no FINAL that can block will run" (legacy runs, N=1, `--skip-final-review`) and never asks (`qa.md:225`, `:301`). In a normal run they stay unprinted in notes files. The source's claim that the summary already carries minors holds only for those cases.
- **F3.** The owner approved `/sc:implement`'s final review step as the follow-up carrier, "record and print only" (`OPEN-QUESTIONS.md:111`).
- **F4.** The Medium offer is "once per loop" today (`pragmatic.md:230`). The reviewer already lists Medium findings under `follow-up candidates` in its own report (same line).
- **F5.** The classifier has no authority in version 1 and gates nothing (`OPEN-QUESTIONS.md:14`, `:96`). The safety question is the only one with a usable signal: S (safety, data loss, wrong target) AUC 0.73 (`08-test/results.md:60`).
- **F6.** Section 0 of the open questions is a "proposal, not yet approved by the owner" (`OPEN-QUESTIONS.md:5`). The owner has already removed the salvage of malformed reports (`OPEN-QUESTIONS.md:77`).
- **F7.** `test_h_implement_protocol_plugin_twins_byte_equal` (`test_review_severity_rule.py:371`) requires the `/sc:implement` protocol's plugin twins to match the source byte for byte. Any edit to that protocol must go to its twin too, so the twin copy cannot be cut.

Not verified: the definition of revert trigger RT1, the "11 safety rows", the purpose of stage 3 T5, and whether any test or hook reads the stage ledger `stage-requests/README.md`.

## 1. Verdict per cut

| Cut | Verdict | Risk of this verdict (evidence) | Reward | Do NOT make the cut if |
|---|---|---|---|---|
| C1 classifier | CUT. Keep stage 1 T13 as a safety vocabulary scan only. | Low. The classifier gates nothing (F5). Its only useful signal, the safety question (AUC 0.73, `results.md:60`), is covered by the vocabulary scan. Lost: future evidence on Jev, which stays deferred under OD3. | 8 tasks (S1 T5, T9 to T12; S2 T7; S0 T6, T8). | the owner overturns OD4 (gives the classifier authority) or opens OD3 for Jev before the rule change ships. |
| C2 ledger tooling | CUT. Go further than proposed: see missed cut M1, which drops the plain list file too. | Low. Nobody has been shown to file from a ledger, and `/sc:implement` writes none (`OPEN-QUESTIONS.md:15`). The safety route loses its recorded rows. That is acceptable only because a safety-scan hit stays blocking and is never deferred. | 8 tasks (S1 T4, T7, T8; S2 T1, T2, T5, T6, T8). Stage 3 T5 is not decided here (purpose not verified). | RT1 is defined on a count that only a ledger state field can supply (check `02-brainstorm/merged-requirements.md` before cutting). |
| C3 `/sc:implement` carrier | SHRINK, do not cut (concede). Keep stage 2 T3 as: the final step prints every non-`superseded` line of every task's `notes.md`. No sweep command, no ledger. Cut stage 3 T10 (promote switch). | A full cut drops an owner approval (F3) and leaves normal-run Medium findings unprinted (F2). `test_h` forces the twin edit (F7). | 1 task (S3 T10). The sweep dependency is gone with C2. | (no condition: the shrink is the safe form). |
| C4 skill folder, registry, scale map, doctor, drift tests | CUT. The "one verbatim-copy test over a hardcoded file tuple" already exists: `test_c_s1_s3_copied_verbatim` over `S1_S3_FILES` (F1). Keep the reverse scan (S3 T13). | Low. No drift incident is on record, and the existing test fails on any drift in ten files. No digests means nothing for an install check to check. | 6 tasks (S1 T1, T2, T3, T6, T14, T15). One new skill folder fewer. | a carrier the reviewers read at run time sits outside the ten-file tuple and outside the plugin-twin test, with no other test pinning it. |
| C5 allow-list, MDTM digest rows, plugin parity | SHRINK. Cut the allow-list concept and digest rows. Do NOT leave the two MDTM templates untouched: copy the new S1 to S3 into them. | Leaving them untouched fails `test_c` (`test_review_severity_rule.py:201`) for `:186-187` (F1). Copying is two edits; narrowing the tuple would bring the allow-list back. | Parts of S1 T3, S4 T1, T2. | (no condition: as proposed, the cut breaks an existing test). |
| C6 seeded recall, hash-bound rulings | CUT. | Medium. This was the only direct measure of planted-defect recall. What still protects real blockers: the S0 T4 regrade over the 82 panel blockers, plus the safety scan. Both arms carry the old style, so it was confounded. | 3 tasks (S0 T7, S3 T3, T4). | the S0 T4 regrade shows any of the 82 blockers lost under the new text. Then a targeted recall check of that class is needed before the switch. |
| C7 shadow stage | CUT stage 2 except the shrunk T3 (C3). Cut S3 T1. Replace with one run proving follow-up candidates are written. | Low. Zero misses in 5 runs still allows about 45% (1 − 0.05^(1/5) = 0.451), so the gate proves little. Cutting T3 too would break C3. | 7 tasks (S2 T1, T2, T4 to T8; S3 T1). | the owner wants observed-in-practice evidence before the switch. Then take the C8 alternative: owner reads the first 5 runs after the switch. |
| C8 audit window, baselines | SHRINK to RT1 plus the owner reading the first five runs' Medium lists. Cut S3 T2, T14. | Low. n = 60 can show only "under 5%" (rule of three: 3/60). | 2 tasks. | RT1 needs M1, M12 or M10b as its baseline number (not verified). |
| C9 stage 0 | CUT T2, T3, T5 to T9. Keep T1 and T4. Fold T10 into T4's output (see C10). | Low. T3 duplicates `08-test/results.md`, which already exists. T9 leaves stale spec statements, but no runtime reads the spec. T4 stays: it is the one check that the 82 blockers survive the new text. | 7 tasks (8 with T10). | a kept task cites a spec statement that T9 would have corrected as its source of truth. |
| C10 owner summaries, ledger fields | CUT. | Low. The owner's go is a chat message and the git log is the record. | 5 tasks. | a test or hook reads the hash or ruling fields of `stage-requests/README.md` (not verified; grep before cutting). |
| C11 merge stages 3 and 4 | CUT (merge). | Lower risk than staging. F1 shows that a staged S1 change cannot pass `test_c` in between: stage 3 changes `pragmatic.md`, while the rule prompts and templates (`:184-191`) are edited only in stage 4. | One package and its entry gate fewer. | (no condition: staging is the riskier option). |
| C12 defer rule prompts and templates | SHRINK. Copy S1 to S3 into the four rule prompts and both document templates in the same change as `pragmatic.md`. Defer only the edits beyond that copy. | Deferring the copy fails `test_c` for `:184-185` and `:188-191` (F1). Who dispatches the prompts does not matter for a byte copy that the test already requires. | Whatever S4 T1 and T2 do beyond the copy. | (no condition: as proposed, the cut breaks an existing test). |
| C13 Review Panel scope | CUT the listed build items. | Low. The kept items (2,000-character cap, two-report quorum, clustering fix) target the stated causes (92 dropped lines, 83 mega-rows). Salvage is already owner-removed (F6). | Launcher, telemetry, `verify-run`, per-slot keys, older-engine fix. | the 49 dropped blocking lines trace to the older engine. Then its clustering fix stays. |
| C14 open questions | SHRINK. Record the "answer today" items as recommendations that wait for the owner's answer. Accept the defer and drop lists. | Writing them as answers would put agent proposals where the owner's decisions belong (F6, `OPEN-QUESTIONS.md:5`). | Shorter open-questions file. | (no condition: always mark them pending). |

## 2. Cuts or keeps the list misses

- **M1 (cut): drop the plain follow-ups list file too.** Reviewers already list Medium findings under `follow-up candidates` (`pragmatic.md:230`), and `/sc:implement` writes `notes.md` (`qa.md:200`). A third file adds a writer and a format with no reader. Keep explicit `--repo` and the per-run offer (S3 T6). Do not cut it if the owner wants one cross-reviewer list per run outside `/sc:implement`.
- **M2 (keep): the S1 to S3 copy into all ten tuple files is one atomic task.** F1 makes C5, C11 and C12 the same constraint: `pragmatic.md` and the ten files change in one commit, or `test_c` fails. The plans must state this as one task with `uv run pytest tests/skills/test_review_severity_rule.py` as its check.
- **M3 (keep): the re-pin tasks (S3 T11, T12) must cover the other two tests that read `pragmatic.md`.** These are `tests/skills/test_review_severity_mapping.py:23` and `tests/skills/test_review_prompt_overrides.py:24`. The cut list does not name them.
- **M4 (keep): the plugin twin of `/sc:implement`.** It is forced by `test_h` (F7) and cannot be traded away in C3 or C5.
- **M5 (keep): the reverse scan (S3 T13), with no exemption list.** One search for the S1 opening or "highest severity wins" matches 11 files under `src/superclaude` today; after M2, none should keep the old text. The scan must target the old sentence after the opening ("Blocking is a real defect: ..."). The test requires the opening itself to stay (`test_review_severity_rule.py:70`).

## 3. Final list of cuts to proceed with

Ordered by reward over risk:

1. **C1** classifier (8 tasks).
2. **C2 plus M1**: the ledger tooling and the plain list file (8 tasks).
3. **C7** shadow stage, except the shrunk S2 T3 (7 tasks).
4. **C9**: keep stage 0 T1 and T4 only (8 tasks).
5. **C4**: no skill folder or registry (6 tasks).
6. **C10** owner summaries (5 tasks, after the README grep).
7. **C11** merge stages 3 and 4.
8. **C13** Review Panel build items.
9. **C8**, shrunk (2 tasks).
10. **C6** seeded recall (3 tasks), with the gate on the T4 regrade.
11. **C5 and C12**, shrunk to the atomic copy (M2).
12. **C14**, shrunk to recommendations pending the owner.
13. **C3**: shrink only, which cuts S3 T10. It stays in its approved print-only form, so no reversal flag to the owner is needed.

Result: about 15 tasks in 3 packages, down from 54 in 5. The three packages:

- **Package 1 (stage 0):** T1 and T4.
- **Package 2 (what is left of stages 1 and 2):** the safety scan, and the `/sc:implement` print plus its plugin twin.
- **Package 3 (stages 3 and 4 merged):** the per-run offer; the atomic S1 to S3 copy into `pragmatic.md` and the ten files; `rf-qa`, `rf-qa-qualitative` (OD16) and `rf-analyst`; the merge-rule lines in four skills and `spec-panel`; re-pins of three test files; the reverse scan; and one final test run. Real blockers keep their review path; security, data-loss and safety findings stay blocking through S1 and the scan; the owner approval (F3) is kept.
