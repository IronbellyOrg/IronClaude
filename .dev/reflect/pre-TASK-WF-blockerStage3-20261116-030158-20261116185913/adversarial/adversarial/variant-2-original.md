<!-- reviewer card saved verbatim by the orchestrator; persona: qa; model class: opus; agent type: reflect-reviewer; the card is the subagent's final message with the harness indent removed -->

## Earlier findings

- **F1 (gate ran after the edit): fixed.** Task 4 is now a read-only gate that runs first (PLAN:113, "Spawn no agent and edit nothing outside `./artifacts/`"). Task 6 checks the gate again before editing (PLAN:140), and the old-arm and new-arm texts are frozen as copies (PLAN:78). One gap remains, see F5.
- **F2 (no controlling variant or threshold): fixed in text** (PLAN:82). The threshold the plan chose creates a new defect, see F1.
- **F3 (rules 8 and 9 not edited): fixed in text** (PLAN:160, PLAN:179). Two problems remain: the new acceptance lines pass vacuously (F2), and other contradicting lines are still unedited (F3).
- **F4 to F16: fixed.** Evidence: PLAN:78 (F4), PLAN:166 and PLAN:182 (F5), PLAN:149 and PLAN:152 (F6), PLAN:44 (F7), PLAN:142 (F8), PLAN:256 (F9), PLAN:229 (F10), PLAN:240 (F11), README:45 (F12, the ledger fields are now listed), PLAN:169 (F13), PLAN:162 (F14), PLAN:158 (F15), PLAN:40 and PLAN:61 (F16).

## Findings

**F1. Blocking: yes. The two arms can be scored with different "found" thresholds.**
- Evidence: PLAN:82 "(2 of 3 with three valid reviewers, 2 of 2 with two)". PLAN:80 "the recall-equality lines are biased toward PASS and the cosmetic-fall line toward FAIL".
- Consequence: The confound mainly makes new-arm reviewers invalid, so the likely case is 3 valid old-arm reviewers against 2 valid new-arm reviewers. If each reviewer catches a defect with probability 0.9, a 2-of-3 majority catches it about 97 percent of the time, while 2 of 2 catches it 81 percent. That drop of about 16 points comes from panel size alone, so R2a and R2b can FAIL, and R3 (cosmetic block share falls) can PASS without any owner ruling, purely as an artifact. In that case the bias statement at PLAN:80 is also backwards.
- Fix: Score both arms with the same number of valid reviewers, either by spawning fresh replacement reviewers until each arm has 3, or by a pre-set rule that equalises the counts. Otherwise mark the line NOT-MEASURABLE.

**F2. Blocking: yes. Several "positive" acceptance checks pass from the digest alone.**
- Evidence: PLAN:168 "the rewritten principle 8 and rule 9 contain the words "stays open for verification"" (Task 8 repeats this at PLAN:185). The digest inserted by the same task already contains both phrases: SPEC:199 "An unverified safety claim stays open for verification" and SPEC:201 "tag the row `consumer-unknown`". The Task 6 cap check has the same problem: PLAN:147 "(`grep -c` of each sentence prints 1 or more)", while SPEC:213 says the digest's last sentence "is today's cap bullet ... word for word".
- Consequence: Rules 8 and 9 could lose their replacement wording, or the cap bullet could be deleted, and these checks would still pass. Only the checks that require a count of 0 still do real work.
- Fix: Check the rewritten lines themselves (for example, a grep on "NO LENIENCY" or "Report honestly" plus the phrase). Require the cap sentence count to be 2 in `pragmatic.md`.

**F3. Blocking: yes. Lines in `rf-qa-qualitative.md` that contradict the new Rule 6 (OD16 option b) and the digest are left unedited.**
- Evidence:
  - rf-qa-qualitative.md:593 "Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below)."
  - rf-qa-qualitative.md:611 "Severity floor: IMPORTANT"
  - rf-qa-qualitative.md:616 ">= IMPORTANT."
  - rf-qa-qualitative.md:918 "'Must resolve ALL CRITICAL and IMPORTANT issues before proceeding.'"
- Task 8 (PLAN:177) does not list these lines, and none of the stage 0 freeze patterns matches them (S0:34).
- Consequence: The pilot agent would ship the rewritten Rule 6 next to lines that still set a fixed severity floor citing Rule 6, plus an instruction to resolve every IMPORTANT finding. That contradicts the rule being shipped and can keep the M12 count flat.
- Fix: Add these lines to Task 8, each with a `grep -c -F` line that must print 0.

**F4. Blocking: no. R3 has no minimum n.**
- Evidence: S0:106 "state a minimum n per gating class (safety, decision-bearing, missing)". PLAN:96 "PASS (the rule holds and the class is at or above its minimum n)".
- Consequence: Two runs could legitimately produce different outcome words for R3. In addition, the old rule already grades cosmetic findings as minor (pragmatic.md:225 "Minor is cosmetic"), so R3 will most likely read NOT-MEASURABLE.
- Fix: State that R3 is always advisory, or have stage 0 give it a minimum n.

**F5. Blocking: no. A fix pass or retry of Task 6 can still make the edit.**
- Evidence: PLAN:21 "A halt at Task 4 or at the start of Task 6 leaves no rule file switched". SKILL.md:145 "then exactly one fix pass".
- Consequence: When the gate check fails, the digest acceptance lines also fail, and a fixer may "fix" them by editing `pragmatic.md`.
- Fix: State that no fix pass or retry of Task 6 edits `pragmatic.md` while its first acceptance line fails.

**F6. Blocking: no. Stage 4 depends on Rule 6 keeping a bold heading, and this plan does not require it.**
- Evidence: S4:39 "the label is the bold words of that line between the `**` marks".
- Fix: Task 8 requires the new Rule 6 to keep the form `6. **<heading>** — ...`.

**F7. Blocking: no. The coverage matrix is missing rows for requirement-bearing parts of SRC.**
- Missing: SRC:14 (scan-test allow-list constraints), SRC:13 (halt on a fail line), SRC:12 (fresh agents, alternated pass order), SRC:34 to SRC:38, and the F10, F13, F14 and F16 bullets.
- I checked each by hand and the plan covers them (PLAN:240, PLAN:78, PLAN:26, PLAN:209, PLAN:258).
- Fix: Regenerate the matrix.

**F8. Blocking: no. Wording mismatch in Task 6.** PLAN:142 says "except the two listed below", but PLAN:152 runs three test files. Fix: say "the three".

**F9. Blocking: no. The scan test is narrower than the spec.** PLAN:240 scans only six `src/superclaude` subfolders and `plugins/superclaude`. SPEC:845 says "searches `src/` and `plugins/`", so `core/` and other installed folders are left out. Fix: scan all `*.md` files under `src/superclaude`.

**F10. Blocking: no. Two named edits have no check, and the L1 text is incomplete.**
- rf-qa.md:389 and rf-qa.md:476 are named in Task 7's body but have no acceptance line.
- The L1 text at PLAN:158 leaves out the `reasked` flag and the "label stands, listed first" outcome (SPEC:270).
- Fix: Add `grep` lines for 389 and 476, and complete the L1 sentence.

## Checked and sound

- Task numbers 1 to 14 are contiguous, and every `Depends on:` points to an earlier task. Only Task 5 sits between the gate and the first rule edit, and it touches no rule file.
- Live line numbers cited in the plan all hold:
  - rf-qa.md: 83, 100, 108, 182 to 183, 402, 494, 548, 549.
  - rf-qa-qualitative.md: 84, 99, 240 to 784 (the eight pairs), 809, 990, 993, 994, 936 to 952.
  - pragmatic.md: 221, 225, 226, 229, 230.
- The Critical Rules window hash covers the header minus 3 to the header plus 6, which ends before Rule 6 (`test_severity_floor_unweakened.py`). The 10-line window is therefore unchanged and the block hash does change, as Task 12 says. The rewritten verdict pairs lie outside the block.
- No fixture row pins `pragmatic.md` or the lines Tasks 6 to 8 rewrite. The cap rows C-004 and C-011 survive if the L3 text is added after the sentence.
- The merge-phrase hits match the allow-list. The plugin tree has 0 hits.
- Stage 2's script output and its test match Tasks 1 and 10.
- The RT5 threshold (75 percent of the M1 mean) is right. Judging RT1 (seeded part) and RT3 now and leaving RT2 and RT4 to RT8 pending is a fair split. The M5, M6, M9 and M11 baseline sources match SPEC 13.1.
- The fields S4 needs (RT1, RT2 and M12 tokens, 11 `digest` rows, the allow-list format) are all produced.
- T1 observations: O1 is confirmed (F8). O2 and O3 are not defects. O4 does no harm, because stage 2's paragraphs are checked free of those words (S2:122). O5 is minor.
- I did not run any tests, so whether `tests/audit` passes as a whole before this stage starts is unchecked.

## Self-report

confidence: 0.82
