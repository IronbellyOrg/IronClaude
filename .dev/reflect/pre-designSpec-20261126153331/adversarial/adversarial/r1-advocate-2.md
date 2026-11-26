# Round 1, advocate 2 (card 2, qa lens, haiku). Links reduced to file:line.

Positions defended:

- C-001 / X-004: Blocking (Decision). The named acceptance check at plan:165 demands one post for missing-key and exhausted-budget stops; both occur before transport (client.py:114-137), so the check cannot pass with the required client. Steelman of card 1: the stop classes and the no-rerun rule match the client; agreed, but that does not establish the post counts. Defended as Blocking because the check is impossible, not merely badly worded.
- C-005 / X-002: Blocking (Missing). The freeze procedure omits the human reading of the six definitions (source.md:142; plan:201 README order of work). Steelman of calibrator: the action is cheap and the source labels M-5 Medium; neither establishes its presence. Defended as Missing, since the required handoff step is absent regardless of repair size.
- C-006: Blocking (Missing). Two freeze commands lack the refusal to replace existing manifest keys (plan:103-104; source.md:144). Steelman: all freeze commands might inherit write-once semantics; but only `freeze-corpus` states it, and the spec requires it for every freeze command.
- C-007: Blocking (Missing), revised from Decision. The calibrator is right that temporary roots are the primary protection and the original Decision rationale overstated a weak test. But the spec separately requires an autouse guard detecting real-run changes (source.md:150) and descendant coverage is absent (plan:41).

Concessions:

- C-008 (T-06 label): concede Medium; scoring behaviour is already specified at plan:127 and plan:138.
- C-009 / X-003 (`sign_test_passes` signature): Medium, not a numerical-decision defect (plan:79).
- C-010 ("answered"): Medium population ambiguity (plan:81, 87).
- A-001: defend Revision 1 precedence (source.md:128). A-002: withdraw any blanket claim that the library is correct. A-003: concede grading was not uniform.
- C-002 to C-004 and C-011 to C-012: no position in card 2; silence is not a clean assessment.

Recommendation: carry C-001, C-005, C-006 and C-007 forward with C-007's revised rationale.
