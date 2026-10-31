a627f449e6bc1223ddb2dfd427fb2095a16847bc
## family s5-attribution-wording
defect form: S5 attribution stated as "at least one re-triggered reviewer reaches a classified review / clean-findings" without the Augment-declined precedence of merge_wait
command: grep -rn -i "at least one" src/superclaude/skills/sc-pr-submit-protocol/ src/superclaude/commands/pr-submit.md
before:
refs/state-machine.md:66 (defect)
refs/review-retrigger.md:85 (defect; decline exception only stated later at :92-93)
SKILL.md:196 (outside T14's touched files, written in T12; it lists "declined when Augment declines (existing)" in the same sentence; listed, not edited)
refs/augment-poll.md:73, refs/finding-verify.md:68, refs/state-machine.md:165, SKILL.md:271 (other meanings, not the defect form)
coupled sites: design section 6 "attributed when at least one re-triggered reviewer reaches done" (specification, not edited)
after:
src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md:85:re-triggered in this cycle; the re-review is attributed when at least one of them reaches a gated
src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md:73:true and at least one formal review exists; otherwise `polling`) is an Augment-era hint only;
src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md:68:member keeps its own verdict: a group is dispatched to C3b only when at least one member is
src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:67:the INV-001 edge fires once when at least one of them reaches `clean` or `findings` on the pushed SHA
src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:165:> (4) `round_counter < max_rounds`; (5) the cycle produced at least one grounded, applied edit
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:196:watermark. The re-review is **attributed** (the INV-001 edge, one tick per cycle) when at least one
src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:271:- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces (one verdict per finding, Augment and Codex in one batch). `unverified` → REPORT_ONLY, consuming NO round. A dedup group is dispatched only when at least one member is verified.
